import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from core.database import Base


class Scene(Base):
    __tablename__ = "scenes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    episode_id = Column(UUID(as_uuid=True), ForeignKey("episodes.id", ondelete="CASCADE"), nullable=False)
    scene_number = Column(Integer, nullable=False)
    scene_class = Column(String, nullable=False)
    voiceover_text = Column(Text, nullable=False)
    manim_spec = Column(JSONB, nullable=True)
    wan_prompt = Column(Text, nullable=True)
    audio_path = Column(Text, nullable=True)
    video_path = Column(Text, nullable=True)
    synced_path = Column(Text, nullable=True)
    audio_duration_secs = Column(Float, nullable=True)
    video_duration_secs = Column(Float, nullable=True)
    status = Column(String, default="pending")

    episode = relationship("Episode", back_populates="scenes")

    def __repr__(self) -> str:
        return f"<Scene(id={self.id}, ep={self.episode_id}, scene={self.scene_number}, status='{self.status}')>"