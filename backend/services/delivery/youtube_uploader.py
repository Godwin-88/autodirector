from pathlib import Path
from typing import Optional
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from schemas.seo import SEOMetadata
from core.config import get_settings
from core.logging import get_logger

logger = get_logger("youtube_uploader")


class YouTubeUploader:
    SCOPES = [
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube",
    ]

    def __init__(self):
        self.settings = get_settings()

    def _get_service(self):
        """Build YouTube API service from client secrets."""
        flow = InstalledAppFlow.from_client_secrets_file(
            self.settings.youtube_client_secrets_file, self.SCOPES
        )
        credentials = flow.run_local_server(port=0)
        return build("youtube", "v3", credentials=credentials)

    async def upload(self, video_path: str, thumbnail_path: str,
                     seo_metadata: SEOMetadata, channel_id: str) -> str:
        """Upload video to YouTube. Returns video_id."""
        service = self._get_service()

        # Build description with chapters
        description = seo_metadata.youtube_description
        if seo_metadata.chapters:
            chapters_text = "\n".join(
                f"{c.timestamp} {c.title}" for c in seo_metadata.chapters
            )
            description = f"{chapters_text}\n\n{description}"

        body = {
            "snippet": {
                "title": seo_metadata.youtube_title[:100],
                "description": description,
                "tags": seo_metadata.tags[:30],
                "channelId": channel_id,
            },
            "status": {
                "privacyStatus": "unlisted",
                "selfDeclaredMadeForKids": False,
            },
        }

        media = MediaFileUpload(video_path, chunksize=1024 * 1024, resumable=True)

        request = service.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media,
        )

        response = None
        for attempt in range(3):
            try:
                response = request.execute()
                break
            except Exception as e:
                logger.warning("youtube_upload_attempt_failed", attempt=attempt + 1, error=str(e))
                if attempt == 2:
                    raise

        video_id = response.get("id", "")
        logger.info("youtube_uploaded", video_id=video_id, title=seo_metadata.youtube_title)

        # Set thumbnail
        if thumbnail_path and Path(thumbnail_path).exists():
            try:
                service.thumbnails().set(
                    videoId=video_id,
                    media_body=MediaFileUpload(thumbnail_path),
                ).execute()
                logger.info("youtube_thumbnail_set", video_id=video_id)
            except Exception as e:
                logger.warning("youtube_thumbnail_failed", error=str(e))

        return video_id