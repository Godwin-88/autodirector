"""
Strategy Layer API Routes — content planning, suggestion engine, calendar management.
"""
import logging
from datetime import date
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.strategy.suggestion_engine import SuggestionEngine

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/strategy", tags=["strategy"])
engine = SuggestionEngine()


# ── Request/Response Schemas ──────────────────────────────────────────────

class CreateEpisodeRequest(BaseModel):
    pillar_id: str
    topic: str
    suggested_title: Optional[str] = None
    notes: Optional[str] = None


class ReorderRequest(BaseModel):
    pillar_id: str
    episode_ids: list[str]


class OverrideRequest(BaseModel):
    planned_episode_id: str
    reason: Optional[str] = None


class ProduceRequest(BaseModel):
    auto_approve: bool = False
    additional_source_ids: list[str] = []
    memgraph_augment: bool = True


# ── Endpoints ─────────────────────────────────────────────────────────────

@router.get("/today")
async def get_today_suggestion(series: str = "quantifaya"):
    """Get today's suggested episode."""
    return await engine.get_suggestion(series=series)


@router.get("/week")
async def get_week_preview(series: str = "quantifaya"):
    """Get 7-day preview of suggested episodes."""
    return await engine.get_week_preview(series=series)


@router.get("/pillars")
async def get_pillars(series: str = "quantifaya"):
    """Get all active pillars for a series."""
    return await engine.get_all_pillars(series=series)


@router.get("/pillars/{pillar_id}")
async def get_pillar_detail(pillar_id: str):
    """Get a pillar with all its planned episodes."""
    result = await engine.get_pillar_with_episodes(pillar_id)
    if result.get("status") == "not_found":
        raise HTTPException(status_code=404, detail="Pillar not found")
    return result


@router.post("/pillars")
async def create_pillar():
    """Create a custom pillar. (Stub — full implementation requires Pillar model write.)"""
    raise HTTPException(status_code=501, detail="Not implemented — use DB migration to add pillars")


@router.get("/episodes")
async def get_planned_episodes(pillar_id: Optional[str] = None,
                                status: Optional[str] = None,
                                series: str = "quantifaya"):
    """Get all planned episodes, optionally filtered by pillar or status."""
    if pillar_id:
        result = await engine.get_pillar_with_episodes(pillar_id)
        return result.get("episodes", [])
    # Return all pillars with episodes
    pillars = await engine.get_all_pillars(series=series)
    all_episodes = []
    for p in pillars:
        detail = await engine.get_pillar_with_episodes(p["id"])
        all_episodes.extend(detail.get("episodes", []))
    if status:
        all_episodes = [e for e in all_episodes if e["status"] == status]
    return all_episodes


@router.post("/episodes")
async def create_episode(req: CreateEpisodeRequest):
    """Add a custom episode to a pillar."""
    result = await engine.create_custom_episode(
        pillar_id=req.pillar_id,
        topic=req.topic,
        suggested_title=req.suggested_title,
        notes=req.notes,
    )
    return result


@router.put("/episodes/{episode_id}")
async def update_episode(episode_id: str):
    """Edit a planned episode. (Stub — full implementation requires update logic.)"""
    raise HTTPException(status_code=501, detail="Not implemented — use DB directly")


@router.post("/episodes/{episode_id}/skip")
async def skip_episode(episode_id: str):
    """Mark a planned episode as skipped."""
    return await engine.mark_skipped(episode_id)


@router.post("/episodes/{episode_id}/produce")
async def produce_episode(episode_id: str, req: ProduceRequest = None):
    """
    Fire the AutoDirector pipeline for a planned episode.
    Creates an episode record and dispatches the Celery task.
    """
    from uuid import uuid4
    from datetime import datetime
    from models.episode import Episode
    from core.database import get_async_session_local
    from sqlalchemy import select
    from models.planned_episode import PlannedEpisode

    async with get_async_session_local() as session:
        # Get the planned episode
        result = await session.execute(
            select(PlannedEpisode).where(PlannedEpisode.id == episode_id)
        )
        planned = result.scalar_one_or_none()
        if not planned:
            raise HTTPException(status_code=404, detail="Planned episode not found")

        # Create the actual episode record
        episode = Episode(
            id=uuid4(),
            topic=planned.topic,
            episode_number=planned.sequence_number,
            status="queued",
        )
        session.add(episode)
        await session.flush()

        # Link back
        planned.episode_id = episode.id
        planned.status = "in_production"
        await session.commit()

        # Dispatch Celery task
        from workers.tasks import run_episode_graph
        run_episode_graph.delay(
            str(episode.id),
            auto_approve=req.auto_approve if req else False,
        )

        return {
            "status": "dispatched",
            "episode_id": str(episode.id),
            "planned_episode_id": episode_id,
            "topic": planned.topic,
        }


@router.post("/episodes/reorder")
async def reorder_episodes(req: ReorderRequest):
    """Bulk reorder episodes within a pillar."""
    return await engine.reorder_pillar(req.pillar_id, req.episode_ids)


@router.post("/schedule/{target_date}/override")
async def override_schedule(target_date: date, req: OverrideRequest):
    """Assign a specific episode to a specific date."""
    from uuid import uuid4
    from models.schedule_override import ScheduleOverride
    from core.database import get_async_session_local
    from sqlalchemy import select

    async with get_async_session_local() as session:
        # Check existing override
        result = await session.execute(
            select(ScheduleOverride).where(ScheduleOverride.target_date == target_date)
        )
        existing = result.scalar_one_or_none()
        if existing:
            existing.planned_episode_id = req.planned_episode_id
            existing.reason = req.reason
        else:
            override = ScheduleOverride(
                id=uuid4(),
                target_date=target_date,
                planned_episode_id=req.planned_episode_id,
                reason=req.reason,
            )
            session.add(override)
        await session.commit()
        return {"status": "ok", "target_date": str(target_date)}


@router.get("/calendar")
async def get_calendar(series: str = "quantifaya", weeks: int = 4):
    """Get full calendar view — suggestions for the next N weeks."""
    from datetime import timedelta
    today = date.today()
    results = []
    for i in range(weeks * 7):
        d = today + timedelta(days=i)
        suggestion = await engine.get_suggestion(d, series)
        results.append(suggestion)
    return {"weeks": weeks, "days": results}