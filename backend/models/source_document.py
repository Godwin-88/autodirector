import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, Float, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from core.database import Base


class SourceDocument(Base):
    __tablename__ = "source_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    authors = Column(Text, nullable=True)
    year = Column(Integer, nullable=True)
    source_type = Column(String, nullable=False)  # 'url' | 'pdf' | 'memgraph' | 'manual'
    origin_url = Column(Text, nullable=True)
    file_path = Column(Text, nullable=True)
    raw_text = Column(Text, nullable=True)
    metadata_json = Column(JSONB, nullable=True)
    ingested_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    chunk_count = Column(Integer, default=0)
    status = Column(String, default="pending")  # pending | chunked | embedded | failed

    chunks = relationship("SourceChunk", back_populates="document", cascade="all, delete-orphan")
    episode_links = relationship("EpisodeSource", back_populates="document", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<SourceDocument(id={self.id}, title='{self.title[:60]}', type='{self.source_type}')>"