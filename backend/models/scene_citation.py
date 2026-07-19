import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.database import Base


class SceneCitation(Base):
    __tablename__ = "scene_citations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scene_id = Column(UUID(as_uuid=True), ForeignKey("scenes.id", ondelete="CASCADE"), nullable=False)
    chunk_id = Column(UUID(as_uuid=True), ForeignKey("source_chunks.id", ondelete="CASCADE"), nullable=False)
    citation_text = Column(Text, nullable=True)
    relevance_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    chunk = relationship("SourceChunk", back_populates="citations")

    def __repr__(self) -> str:
        return f"<SceneCitation(id={self.id}, scene={self.scene_id}, chunk={self.chunk_id})>"