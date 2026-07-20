"""
Planned episode model — represents a pre-planned episode in the content calendar.
Seeded from the content strategy document with 125 Quantifaya episodes.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Date, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base


class PlannedEpisode(Base):
    __tablename__ = "planned_episodes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pillar_id = Column(UUID(as_uuid=True), ForeignKey("pillars.id"), nullable=False)
    sequence_number = Column(Integer, nullable=False)  # position within pillar (1-25)
    topic = Column(String(500), nullable=False)
    suggested_title = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)  # user's own notes on this episode
    target_date = Column(Date, nullable=True)
    status = Column(String(20), nullable=False, default="planned")
    # planned | scheduled | in_production | produced | skipped
    episode_id = Column(UUID(as_uuid=True), ForeignKey("episodes.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<PlannedEpisode P{self.sequence_number}: {self.topic[:50]}>"