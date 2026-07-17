import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    episode_id = Column(UUID(as_uuid=True), ForeignKey("episodes.id"), nullable=False)
    job_type = Column(String, nullable=False)
    payload = Column(JSONB, nullable=True)
    status = Column(String, default="queued")
    attempts = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    error_msg = Column(Text, nullable=True)
    celery_task_id = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime(timezone=True), nullable=True)

    episode = relationship("Episode", back_populates="jobs")

    def __repr__(self) -> str:
        return f"<Job(id={self.id}, type='{self.job_type}', status='{self.status}')>"