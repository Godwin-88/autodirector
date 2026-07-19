import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from core.database import Base


class Episode(Base):
    __tablename__ = "episodes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic = Column(Text, nullable=False)
    episode_number = Column(Integer, nullable=True)
    series = Column(String, default="quantifaya")
    status = Column(String, default="pending")
    wan_fallback = Column(Boolean, default=False)
    script_json = Column(JSONB, nullable=True)
    sources_json = Column(JSONB, nullable=True)
    seo_json = Column(JSONB, nullable=True)
    wan_prompt = Column(Text, nullable=True)
    output_path = Column(Text, nullable=True)
    youtube_id = Column(Text, nullable=True)
    duration_secs = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime(timezone=True), nullable=True)

    scenes = relationship("Scene", back_populates="episode", cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="episode", cascade="all, delete-orphan")
    source_links = relationship("EpisodeSource", back_populates="episode", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Episode(id={self.id}, topic='{self.topic[:50]}', status='{self.status}')>"