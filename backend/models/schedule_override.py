"""
Schedule override model — allows the user to manually assign an episode to a specific date,
overriding the default day-of-week pillar rotation.
"""
import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Date, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base


class ScheduleOverride(Base):
    __tablename__ = "schedule_overrides"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_date = Column(Date, nullable=False, unique=True)
    planned_episode_id = Column(UUID(as_uuid=True), ForeignKey("planned_episodes.id"), nullable=True)
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    def __repr__(self):
        return f"<ScheduleOverride {self.target_date}>"