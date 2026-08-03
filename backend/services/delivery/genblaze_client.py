"""Backblaze Genblaze SDK integration.

Genblaze is Backblaze's open-source Python SDK for orchestrating generative
media workflows. This client uses Genblaze's S3StorageBackend + AssetTransfer
to manage the same B2 bucket used by the boto3-based B2StorageService.

It complements (not replaces) the boto3 layer:
  - b2_storage.py  → low-level uploads during the pipeline (tested, stable)
  - genblaze_client.py → official-SDK asset management for the media library

This demonstrates official Backblaze SDK usage for the hackathon submission.
"""
import hashlib
from pathlib import Path
from typing import Optional, Union

from genblaze import Asset, AssetTransfer, KeyStrategy
from genblaze_s3 import S3StorageBackend

from core.config import get_settings
from core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


class GenblazeClient:
    """Backblaze Genblaze SDK client for B2 asset management."""

    def __init__(self):
        self.backend = S3StorageBackend(
            settings.b2_bucket_name,
            endpoint_url=settings.b2_endpoint_url,
            region="us-east-005",
            public_url_base=settings.b2_public_url_base,
            aws_access_key_id=settings.b2_key_id,
            aws_secret_access_key=settings.b2_application_key,
        )
        self.bucket = settings.b2_bucket_name
        self.public_url_base = settings.b2_public_url_base
        # AssetTransfer uses a deterministic key strategy so re-uploads
        # of the same content are idempotent.
        self.transfer = AssetTransfer(
            self.backend,
            prefix="episodes",
            key_strategy=KeyStrategy.CONTENT_ADDRESSABLE,
        )

    # ── UPLOAD ────────────────────────────────────────────────────────────

    def upload_asset(
        self,
        local_path: Union[str, Path],
        media_type: str,
        *,
        asset_id: Optional[str] = None,
    ) -> Asset:
        """Upload a local file to B2 via Genblaze's AssetTransfer.

        Returns the Genblaze Asset with its public URL.
        """
        local_path = Path(local_path)
        if not local_path.exists():
            raise FileNotFoundError(f"File not found: {local_path}")

        data = local_path.read_bytes()
        sha256 = hashlib.sha256(data).hexdigest()

        asset = Asset(
            asset_id=asset_id or local_path.stem,
            url=f"file://{local_path}",
            media_type=media_type,
            sha256=sha256,
            size_bytes=len(data),
        )

        # transfer() returns the durable public URL for the uploaded asset
        url = self.transfer.transfer(asset)
        logger.info(
            "genblaze_upload_complete",
            asset_id=asset.asset_id,
            url=url,
            size_bytes=len(data),
        )
        return asset

    # ── LISTING (media library) ───────────────────────────────────────────

    def list_episode_keys(self, prefix: str = "episodes/") -> list[str]:
        """List all object keys under a prefix using Genblaze's backend.

        Used by the media library dashboard to enumerate stored episodes.
        """
        keys: list[str] = []
        continuation = None
        while True:
            page = self.backend.list(prefix, continuation_token=continuation)
            keys.extend(item.key for item in page.items)
            if not page.next_token:
                break
            continuation = page.next_token
        return keys

    def list_episode_ids(self) -> list[str]:
        """Return the distinct episode IDs stored in B2."""
        keys = self.list_episode_keys("episodes/")
        ids: set[str] = set()
        for key in keys:
            parts = key.split("/")
            if len(parts) >= 2 and parts[0] == "episodes" and parts[1]:
                ids.add(parts[1])
        return sorted(ids)

    # ── URLS ──────────────────────────────────────────────────────────────

    def get_public_url(self, key: str) -> str:
        """Return the durable public URL for a B2 object."""
        return f"{self.public_url_base}/{key}"

    def get_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        """Generate a presigned URL via Genblaze's backend."""
        return self.backend.get_url(key, expires_in=expires_in)

    # ── DELETE ────────────────────────────────────────────────────────────

    def delete_episode(self, episode_id: str) -> int:
        """Delete all B2 objects for an episode. Returns count deleted."""
        result = self.backend.delete_prefix(
            f"episodes/{episode_id}/", dry_run=False
        )
        logger.info(
            "genblaze_delete_complete",
            episode_id=episode_id,
            deleted=result.deleted,
        )
        return result.deleted

    # ── HEALTH ────────────────────────────────────────────────────────────

    def health_check(self) -> dict:
        try:
            # Probe the bucket by listing a single key
            self.backend.list("episodes/", max_keys=1)
            return {
                "status": "connected",
                "bucket": self.bucket,
                "endpoint": settings.b2_endpoint_url,
                "sdk": "genblaze",
            }
        except Exception as e:
            return {"status": "error", "error": str(e), "sdk": "genblaze"}