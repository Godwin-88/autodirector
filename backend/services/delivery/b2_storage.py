"""Backblaze B2 storage via S3-compatible API.

All generated media assets (MP4, WAV, JPEG, JSON) are uploaded to B2
after local generation. B2 becomes the source of truth for all media.

B2 key structure:
  episodes/{episode_id}/final.mp4            ← permanent (final deliverable)
  episodes/{episode_id}/thumbnail.jpg        ← permanent
  episodes/{episode_id}/wan_intro.mp4        ← permanent
  episodes/{episode_id}/manifest.json        ← permanent
  intermediates/{episode_id}/scenes/scene_01_synced.mp4  ← expires after 7 days
  intermediates/{episode_id}/audio/scene_01.wav          ← expires after 7 days

Using a top-level `intermediates/` prefix lets B2 lifecycle rules expire raw
scene/audio files (7 days) without ever touching the permanent episode assets.
"""
import json
import mimetypes
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Union

import boto3
from botocore.config import Config

from core.config import get_settings
from core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


class B2StorageService:
    """Backblaze B2 storage service using S3-compatible API."""

    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.b2_endpoint_url,
            aws_access_key_id=settings.b2_key_id,
            aws_secret_access_key=settings.b2_application_key,
            config=Config(signature_version="s3v4"),
            region_name="us-east-005",
        )
        self.bucket = settings.b2_bucket_name
        self.public_url_base = settings.b2_public_url_base

    # ── UPLOAD ────────────────────────────────────────────────────────────

    async def upload_file(
        self,
        local_path: Union[str, Path],
        b2_key: str,
        content_type: Optional[str] = None,
        public: bool = True,
    ) -> dict:
        """Upload a local file to B2.

        Returns: {"b2_key": str, "url": str, "size_bytes": int, "content_type": str}
        """
        local_path = Path(local_path)
        if not local_path.exists():
            raise FileNotFoundError(f"File not found: {local_path}")

        if content_type is None:
            content_type, _ = mimetypes.guess_type(str(local_path))
            content_type = content_type or "application/octet-stream"

        extra_args = {"ContentType": content_type}
        if public:
            extra_args["ACL"] = "public-read"

        file_size = local_path.stat().st_size

        logger.info(
            "b2_upload_start",
            local=str(local_path),
            key=b2_key,
            size_mb=round(file_size / 1024 / 1024, 2),
        )

        self.client.upload_file(
            str(local_path),
            self.bucket,
            b2_key,
            ExtraArgs=extra_args,
        )

        url = f"{self.public_url_base}/{b2_key}"
        logger.info("b2_upload_complete", key=b2_key, url=url)

        return {
            "b2_key": b2_key,
            "url": url,
            "size_bytes": file_size,
            "content_type": content_type,
        }

    async def upload_episode_assets(self, episode_id: str) -> dict:
        """Upload ALL assets for an episode to B2.

        Called after ffmpeg composition completes.
        Returns a manifest dict with URLs for every asset.
        """
        base_key = f"episodes/{episode_id}"
        intermediates_key = f"intermediates/{episode_id}"
        manifest = {
            "episode_id": episode_id,
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
            "assets": {},
        }

        # 1. Final video (largest — upload first)
        final_path = Path(f"./output/episodes/{episode_id}") / "quantifaya_ep_final.mp4"
        if final_path.exists():
            result = await self.upload_file(
                final_path,
                f"{base_key}/final.mp4",
                content_type="video/mp4",
            )
            manifest["assets"]["final_video"] = result
        else:
            logger.warning("b2_final_video_missing", episode_id=episode_id)

        # 2. Thumbnail
        thumb_path = Path(f"./output/thumbnails/{episode_id}.jpg")
        if thumb_path.exists():
            result = await self.upload_file(
                thumb_path,
                f"{base_key}/thumbnail.jpg",
                content_type="image/jpeg",
            )
            manifest["assets"]["thumbnail"] = result

        # 3. Wan intro clip
        wan_path = Path(f"./output/wan/{episode_id}_intro.mp4")
        if wan_path.exists():
            result = await self.upload_file(
                wan_path,
                f"{base_key}/wan_intro.mp4",
                content_type="video/mp4",
            )
            manifest["assets"]["wan_intro"] = result

        # 4. Individual scene videos (intermediates — expire after 7 days)
        scenes_dir = Path(f"./output/scenes/{episode_id}")
        if scenes_dir.exists():
            manifest["assets"]["scenes"] = []
            for scene_file in sorted(scenes_dir.glob("*_synced.mp4")):
                result = await self.upload_file(
                    scene_file,
                    f"{intermediates_key}/scenes/{scene_file.name}",
                    content_type="video/mp4",
                )
                manifest["assets"]["scenes"].append(result)

        # 5. Audio files (intermediates — expire after 7 days)
        audio_dir = Path(f"./output/audio/{episode_id}")
        if audio_dir.exists():
            manifest["assets"]["audio"] = []
            for audio_file in sorted(audio_dir.glob("*.wav")):
                result = await self.upload_file(
                    audio_file,
                    f"{intermediates_key}/audio/{audio_file.name}",
                    content_type="audio/wav",
                )
                manifest["assets"]["audio"].append(result)

        # 6. Upload the manifest itself as JSON
        manifest_json = json.dumps(manifest, indent=2)
        manifest_key = f"{base_key}/manifest.json"
        self.client.put_object(
            Bucket=self.bucket,
            Key=manifest_key,
            Body=manifest_json.encode(),
            ContentType="application/json",
            ACL="public-read",
        )
        manifest["manifest_url"] = f"{self.public_url_base}/{manifest_key}"

        logger.info(
            "b2_episode_upload_complete",
            episode_id=episode_id,
            asset_count=len(manifest["assets"]),
        )
        return manifest

    # ── PRESIGNED URLS (for private content) ─────────────────────────────

    def get_presigned_url(self, b2_key: str, expires_in: int = 3600) -> str:
        """Generate a presigned URL for temporary private access."""
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": b2_key},
            ExpiresIn=expires_in,
        )

    # ── LIST & GET ────────────────────────────────────────────────────────

    async def list_episode_assets(self, episode_id: str) -> dict:
        """Fetch the manifest.json for an episode from B2."""
        manifest_key = f"episodes/{episode_id}/manifest.json"
        try:
            response = self.client.get_object(
                Bucket=self.bucket, Key=manifest_key
            )
            return json.loads(response["Body"].read().decode())
        except self.client.exceptions.NoSuchKey:
            return {}

    async def list_all_episodes(self) -> list[dict]:
        """List all episode manifests in B2.

        Used for the media library dashboard tab.
        Note: boto3 paginators are synchronous — iterate without awaiting.
        """
        paginator = self.client.get_paginator("list_objects_v2")
        episodes = []
        for page in paginator.paginate(
            Bucket=self.bucket,
            Prefix="episodes/",
            Delimiter="/",
        ):
            for prefix in page.get("CommonPrefixes", []):
                episode_id = prefix["Prefix"].split("/")[1]
                if not episode_id:
                    continue
                manifest = await self.list_episode_assets(episode_id)
                if manifest:
                    episodes.append(manifest)
        return episodes

    async def delete_episode(self, episode_id: str) -> int:
        """Delete all B2 objects for an episode. Returns count deleted."""
        prefixes = [
            f"episodes/{episode_id}/",
            f"intermediates/{episode_id}/",
        ]
        paginator = self.client.get_paginator("list_objects_v2")
        deleted = 0
        for prefix in prefixes:
            for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
                objects = [{"Key": obj["Key"]} for obj in page.get("Contents", [])]
                if objects:
                    self.client.delete_objects(
                        Bucket=self.bucket,
                        Delete={"Objects": objects},
                    )
                    deleted += len(objects)
        return deleted

    # ── BUCKET SETUP (run once) ───────────────────────────────────────────

    def ensure_bucket(self) -> None:
        """Create the B2 bucket if it doesn't exist.

        Apply lifecycle rules:
          - Raw scene/audio files expire after 7 days.
          - Final video + thumbnail are retained indefinitely.
        Call this during FastAPI lifespan startup.
        """
        try:
            self.client.head_bucket(Bucket=self.bucket)
            logger.info("b2_bucket_exists", bucket=self.bucket)
        except Exception:
            self.client.create_bucket(Bucket=self.bucket)
            logger.info("b2_bucket_created", bucket=self.bucket)

        # Lifecycle: delete raw intermediate files after 7 days.
        # The `intermediates/` prefix never contains final deliverables,
        # so finals/thumbnails/manifests under `episodes/` are untouched.
        try:
            self.client.put_bucket_lifecycle_configuration(
                Bucket=self.bucket,
                LifecycleConfiguration={
                    "Rules": [
                        {
                            "ID": "expire-raw-intermediates",
                            "Filter": {"Prefix": "intermediates/"},
                            "Status": "Enabled",
                            "Expiration": {"Days": 7},
                        },
                    ]
                },
            )
            logger.info("b2_lifecycle_configured", bucket=self.bucket)
        except Exception as e:
            logger.warning("b2_lifecycle_config_failed", error=str(e))

    def health_check(self) -> dict:
        try:
            self.client.head_bucket(Bucket=self.bucket)
            return {
                "status": "connected",
                "bucket": self.bucket,
                "endpoint": settings.b2_endpoint_url,
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}