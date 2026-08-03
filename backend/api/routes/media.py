from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
import httpx

from services.delivery.b2_storage import B2StorageService
from services.delivery.genblaze_client import GenblazeClient

router = APIRouter()


def get_b2(request: Request) -> B2StorageService:
    """FastAPI dependency for injecting the B2 storage service."""
    b2 = getattr(request.app.state, "b2", None)
    if not b2:
        raise HTTPException(503, "B2 storage not available")
    return b2


# ── B2 (boto3 S3-compatible API) endpoints ───────────────────────────────

@router.get("/health")
async def b2_health(b2: B2StorageService = Depends(get_b2)):
    return b2.health_check()


@router.get("/library")
async def get_media_library(b2: B2StorageService = Depends(get_b2)):
    """List all episodes stored in B2.

    Returns manifests with URLs for the dashboard media library.
    """
    episodes = await b2.list_all_episodes()
    return {"episodes": episodes, "count": len(episodes)}


@router.get("/episodes/{episode_id}/manifest")
async def get_episode_manifest(
    episode_id: str,
    b2: B2StorageService = Depends(get_b2),
):
    """Fetch B2 manifest JSON for a specific episode."""
    manifest = await b2.list_episode_assets(episode_id)
    if not manifest:
        raise HTTPException(404, "No B2 assets found for this episode")
    return manifest


@router.get("/episodes/{episode_id}/video/presigned")
async def get_video_presigned(
    episode_id: str,
    expires: int = 3600,
    b2: B2StorageService = Depends(get_b2),
):
    """Get a presigned URL for private video access."""
    key = f"episodes/{episode_id}/final.mp4"
    url = b2.get_presigned_url(key, expires_in=expires)
    return {"presigned_url": url, "expires_in": expires}


@router.get("/episodes/{episode_id}/stream")
async def stream_video(
    episode_id: str,
    b2: B2StorageService = Depends(get_b2),
):
    """Proxy stream the video from B2.

    Used for in-dashboard video preview without exposing B2 credentials.
    """
    key = f"episodes/{episode_id}/final.mp4"
    presigned = b2.get_presigned_url(key, expires_in=300)

    async def video_generator():
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", presigned) as response:
                async for chunk in response.aiter_bytes(chunk_size=8192):
                    yield chunk

    return StreamingResponse(
        video_generator(),
        media_type="video/mp4",
        headers={"Accept-Ranges": "bytes"},
    )


# ── Genblaze SDK endpoints (official Backblaze SDK) ──────────────────────

@router.get("/genblaze/health")
async def genblaze_health():
    """Health check via the official Backblaze Genblaze SDK."""
    client = GenblazeClient()
    return client.health_check()


@router.get("/genblaze/episodes")
async def genblaze_list_episodes():
    """List episode IDs stored in B2 using the Genblaze SDK backend."""
    client = GenblazeClient()
    episode_ids = client.list_episode_ids()
    return {"episodes": episode_ids, "count": len(episode_ids), "sdk": "genblaze"}


@router.get("/genblaze/episodes/{episode_id}/presigned")
async def genblaze_presigned(episode_id: str, expires: int = 3600):
    """Get a presigned URL for a B2 object via the Genblaze SDK."""
    client = GenblazeClient()
    key = f"episodes/{episode_id}/final.mp4"
    url = client.get_presigned_url(key, expires_in=expires)
    return {"presigned_url": url, "expires_in": expires, "sdk": "genblaze"}