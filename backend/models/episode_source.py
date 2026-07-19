import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, Float, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.database import Base


class EpisodeSource(Base):
    __tablename__ = "episode_sources"

    episode_id = Column(UUID(as_uuid=True), ForeignKey("episodes.id", ondelete="CASCADE"), nullable=False)
    document_id = Column(UUID(as_uuid=True), ForeignKey("source_documents.id", ondelete="CASCADE"), nullable=False)
    relevance_score = Column(Float, nullable=True)
    assigned_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        PrimaryKeyConstraint("episode_id", "document_id"),
    )

    episode = relationship("Episode", back_populates="source_links")
    document = relationship("SourceDocument", back_populates="episode_links")

    def __repr__(self) -> str:
        return f"<EpisodeSource(episode={self.episode_id}, doc={self.document_id})>"