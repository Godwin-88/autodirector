import uuid
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from core.database import get_db
from models.episode import Episode
from models.scene import Scene
from models.job import Job
from core.logging import get_logger

logger = get_logger("episodes")

router = APIRouter()


class CreateEpisodeRequest(BaseModel):
    topic: str
    episode_number: int = 1
    series: str = "quantifaya"


class EpisodeResponse(BaseModel):
    id: str
    topic: str
    episode_number: Optional[int]
    series: str
    status: str
    created_at: str
    completed_at: Optional[str] = None


@router.post("", status_code=201)
async def create_episode(req: CreateEpisodeRequest, db: AsyncSession = Depends(get_db)):
    """Create a new episode and enqueue generation."""
    episode = Episode(
        id=uuid.uuid4(),
        topic=req.topic,
        episode_number=req.episode_number,
        series=req.series,
        status="pending",
    )
    db.add(episode)
    await db.flush()

    # Enqueue Celery task
    from workers.tasks import run_episode_graph
    run_episode_graph.delay(
        str(episode.id),
        req.topic,
        req.episode_number,
        req.series,
    )

    logger.info("episode_created", id=str(episode.id), topic=req.topic)
    return {
        "episode_id": str(episode.id),
        "status": "pending",
        "topic": req.topic,
    }


@router.get("/{episode_id}")
async def get_episode(episode_id: str, db: AsyncSession = Depends(get_db)):
    """Get episode details including scenes."""
    result = await db.execute(
        select(Episode).where(Episode.id == uuid.UUID(episode_id))
    )
    episode = result.scalar_one_or_none()
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")

    scenes_result = await db.execute(
        select(Scene).where(Scene.episode_id == episode.id).order_by(Scene.scene_number)
    )
    scenes = scenes_result.scalars().all()

    return {
        "id": str(episode.id),
        "topic": episode.topic,
        "episode_number": episode.episode_number,
        "series": episode.series,
        "status": episode.status,
        "wan_fallback": episode.wan_fallback,
        "script": episode.script_json,
        "sources": episode.sources_json,
        "seo": episode.seo_json,
        "wan_prompt": episode.wan_prompt,
        "output_path": episode.output_path,
        "youtube_id": episode.youtube_id,
        "duration_secs": episode.duration_secs,
        "created_at": episode.created_at.isoformat() if episode.created_at else None,
        "completed_at": episode.completed_at.isoformat() if episode.completed_at else None,
        "scenes": [
            {
                "id": str(s.id),
                "scene_number": s.scene_number,
                "scene_class": s.scene_class,
                "status": s.status,
                "audio_path": s.audio_path,
                "video_path": s.video_path,
                "synced_path": s.synced_path,
            }
            for s in scenes
        ],
    }


@router.get("/{episode_id}/script")
async def get_episode_script(episode_id: str, db: AsyncSession = Depends(get_db)):
    """Get episode script JSON."""
    result = await db.execute(
        select(Episode).where(Episode.id == uuid.UUID(episode_id))
    )
    episode = result.scalar_one_or_none()
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    return {"script": episode.script_json}


@router.post("/{episode_id}/resume")
async def resume_episode(episode_id: str, db: AsyncSession = Depends(get_db)):
    """Resume episode from human review gate."""
    result = await db.execute(
        select(Episode).where(Episode.id == uuid.UUID(episode_id))
    )
    episode = result.scalar_one_or_none()
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")

    # Update status to trigger resume
    episode.status = "generating"
    await db.flush()

    # Re-enqueue
    from workers.tasks import run_episode_graph
    run_episode_graph.delay(
        str(episode.id),
        episode.topic,
        episode.episode_number or 1,
        episode.series,
    )

    return {"episode_id": episode_id, "status": "resumed"}


@router.get("")
async def list_episodes(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List episodes with pagination."""
    result = await db.execute(
        select(Episode).order_by(Episode.created_at.desc()).offset(skip).limit(limit)
    )
    episodes = result.scalars().all()
    return [
        {
            "id": str(e.id),
            "topic": e.topic,
            "episode_number": e.episode_number,
            "status": e.status,
            "created_at": e.created_at.isoformat() if e.created_at else None,
        }
        for e in episodes
    ]


@router.delete("/{episode_id}")
async def delete_episode(episode_id: str, db: AsyncSession = Depends(get_db)):
    """Delete an episode."""
    result = await db.execute(
        select(Episode).where(Episode.id == uuid.UUID(episode_id))
    )
    episode = result.scalar_one_or_none()
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")

    await db.delete(episode)
    return {"episode_id": episode_id, "status": "deleted"}