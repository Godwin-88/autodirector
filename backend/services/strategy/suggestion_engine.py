"""
Daily Suggestion Engine — computes the suggested episode for any given date.

Logic:
1. Look up the day of week → find the active pillar for that day
2. Find the lowest sequence_number planned episode for that pillar
   with status='planned' (not yet produced or skipped)
3. Check schedule_overrides for the date — if exists, use that instead
4. Return the suggested PlannedEpisode with its pillar context
"""
import logging
from datetime import date, timedelta
from typing import Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_async_session_local
from models.pillar import Pillar
from models.planned_episode import PlannedEpisode
from models.schedule_override import ScheduleOverride

logger = logging.getLogger(__name__)


class SuggestionEngine:
    """Computes daily episode suggestions from the strategy board."""

    DAY_MAP = {
        "monday": 0, "tuesday": 1, "wednesday": 2,
        "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6,
    }

    async def get_suggestion(self, target_date: date = None,
                              series: str = "quantifaya") -> dict:
        """
        Get the suggested episode for a given date.
        Returns dict with status, pillar info, and episode suggestion.
        """
        if target_date is None:
            target_date = date.today()

        async with get_async_session_local() as session:
            # 1. Check schedule_overrides first
            override = await self._get_override(session, target_date)
            if override:
                episode = await self._get_planned_episode(session, override.planned_episode_id)
                if episode:
                    pillar = await self._get_pillar(session, episode.pillar_id)
                    return self._format_suggestion(episode, pillar, target_date, "override")

            # 2. Get day of week → pillar
            day_name = target_date.strftime("%A").lower()
            pillar = await self._get_pillar_for_day(session, day_name, series)
            if not pillar:
                return {
                    "status": "no_pillar_for_day",
                    "date": str(target_date),
                    "day": day_name,
                    "series": series,
                    "suggestion": None,
                }

            # 3. Find next unproduced episode in pillar
            episode = await self._get_next_unproduced(session, pillar.id)
            if not episode:
                return {
                    "status": "pillar_complete",
                    "date": str(target_date),
                    "pillar": {"id": str(pillar.id), "name": pillar.name, "code": pillar.code},
                    "suggestion": None,
                }

            return self._format_suggestion(episode, pillar, target_date, "scheduled")

    async def get_week_preview(self, series: str = "quantifaya") -> list[dict]:
        """Returns suggestions for the next 7 days."""
        today = date.today()
        results = []
        for i in range(7):
            d = today + timedelta(days=i)
            suggestion = await self.get_suggestion(d, series)
            results.append(suggestion)
        return results

    async def get_pillar_with_episodes(self, pillar_id: str) -> dict:
        """Get a pillar with all its planned episodes."""
        async with get_async_session_local() as session:
            pillar = await self._get_pillar(session, pillar_id)
            if not pillar:
                return {"status": "not_found"}
            result = await session.execute(
                select(PlannedEpisode)
                .where(PlannedEpisode.pillar_id == pillar_id)
                .order_by(PlannedEpisode.sequence_number)
            )
            episodes = result.scalars().all()
            return {
                "pillar": {
                    "id": str(pillar.id),
                    "series": pillar.series,
                    "pillar_number": pillar.pillar_number,
                    "name": pillar.name,
                    "code": pillar.code,
                    "publish_day": pillar.publish_day,
                    "description": pillar.description,
                    "color": pillar.color,
                    "active": pillar.active,
                },
                "episodes": [
                    {
                        "id": str(ep.id),
                        "sequence_number": ep.sequence_number,
                        "topic": ep.topic,
                        "suggested_title": ep.suggested_title,
                        "status": ep.status,
                        "target_date": str(ep.target_date) if ep.target_date else None,
                        "episode_id": str(ep.episode_id) if ep.episode_id else None,
                    }
                    for ep in episodes
                ],
                "produced_count": sum(1 for ep in episodes if ep.status == "produced"),
                "total_count": len(episodes),
            }

    async def get_all_pillars(self, series: str = "quantifaya") -> list[dict]:
        """Get all active pillars for a series."""
        async with get_async_session_local() as session:
            result = await session.execute(
                select(Pillar)
                .where(and_(Pillar.series == series, Pillar.active == True))
                .order_by(Pillar.pillar_number)
            )
            pillars = result.scalars().all()
            return [
                {
                    "id": str(p.id),
                    "series": p.series,
                    "pillar_number": p.pillar_number,
                    "name": p.name,
                    "code": p.code,
                    "publish_day": p.publish_day,
                    "description": p.description,
                    "color": p.color,
                    "active": p.active,
                }
                for p in pillars
            ]

    async def mark_skipped(self, planned_episode_id: str) -> dict:
        """Mark a planned episode as skipped."""
        async with get_async_session_local() as session:
            result = await session.execute(
                select(PlannedEpisode).where(PlannedEpisode.id == planned_episode_id)
            )
            episode = result.scalar_one_or_none()
            if not episode:
                return {"status": "not_found"}
            episode.status = "skipped"
            await session.commit()
            return {"status": "ok", "id": planned_episode_id, "new_status": "skipped"}

    async def reorder_pillar(self, pillar_id: str,
                              episode_ids: list[str]) -> dict:
        """Reorder episodes within a pillar. episode_ids is the new order."""
        async with get_async_session_local() as session:
            for i, ep_id in enumerate(episode_ids):
                result = await session.execute(
                    select(PlannedEpisode).where(
                        and_(PlannedEpisode.id == ep_id,
                             PlannedEpisode.pillar_id == pillar_id)
                    )
                )
                ep = result.scalar_one_or_none()
                if ep:
                    ep.sequence_number = i + 1
            await session.commit()
            return {"status": "ok", "pillar_id": pillar_id, "reordered": len(episode_ids)}

    async def create_custom_episode(self, pillar_id: str, topic: str,
                                     suggested_title: str = None,
                                     notes: str = None) -> dict:
        """Add a custom episode to a pillar."""
        from uuid import uuid4
        async with get_async_session_local() as session:
            # Get next sequence number
            result = await session.execute(
                select(PlannedEpisode)
                .where(PlannedEpisode.pillar_id == pillar_id)
                .order_by(PlannedEpisode.sequence_number.desc())
                .limit(1)
            )
            last = result.scalar_one_or_none()
            next_seq = (last.sequence_number + 1) if last else 1

            episode = PlannedEpisode(
                id=uuid4(),
                pillar_id=pillar_id,
                sequence_number=next_seq,
                topic=topic,
                suggested_title=suggested_title or topic,
                notes=notes,
                status="planned",
            )
            session.add(episode)
            await session.commit()
            return {
                "status": "created",
                "id": str(episode.id),
                "sequence_number": next_seq,
                "topic": topic,
            }

    # ── Internal helpers ────────────────────────────────────────────

    async def _get_override(self, session: AsyncSession, target_date: date):
        result = await session.execute(
            select(ScheduleOverride).where(ScheduleOverride.target_date == target_date)
        )
        return result.scalar_one_or_none()

    async def _get_pillar_for_day(self, session: AsyncSession, day_name: str, series: str):
        result = await session.execute(
            select(Pillar).where(
                and_(Pillar.publish_day == day_name,
                     Pillar.series == series,
                     Pillar.active == True)
            )
        )
        return result.scalar_one_or_none()

    async def _get_next_unproduced(self, session: AsyncSession, pillar_id: str):
        result = await session.execute(
            select(PlannedEpisode)
            .where(and_(PlannedEpisode.pillar_id == pillar_id,
                        PlannedEpisode.status == "planned"))
            .order_by(PlannedEpisode.sequence_number)
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def _get_planned_episode(self, session: AsyncSession, episode_id: str):
        result = await session.execute(
            select(PlannedEpisode).where(PlannedEpisode.id == episode_id)
        )
        return result.scalar_one_or_none()

    async def _get_pillar(self, session: AsyncSession, pillar_id: str):
        result = await session.execute(
            select(Pillar).where(Pillar.id == pillar_id)
        )
        return result.scalar_one_or_none()

    def _format_suggestion(self, episode, pillar, target_date: date,
                            source: str) -> dict:
        return {
            "status": "suggestion",
            "date": str(target_date),
            "day": target_date.strftime("%A").lower(),
            "source": source,
            "pillar": {
                "id": str(pillar.id),
                "name": pillar.name,
                "code": pillar.code,
                "color": pillar.color,
            },
            "suggestion": {
                "id": str(episode.id),
                "sequence_number": episode.sequence_number,
                "topic": episode.topic,
                "suggested_title": episode.suggested_title,
                "status": episode.status,
            },
        }