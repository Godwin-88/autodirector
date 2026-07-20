"""
Content pillar model — represents a content series/column.
Quantifaya has 5 pillars (one per weekday), Legalese has 5.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base


class Pillar(Base):
    __tablename__ = "pillars"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    series = Column(String(50), nullable=False, default="quantifaya")
    pillar_number = Column(Integer, nullable=False)
    name = Column(String(200), nullable=False)
    code = Column(String(10), nullable=False)  # e.g. "P1", "P2"
    publish_day = Column(String(20), nullable=False)  # "monday", "tuesday", etc.
    description = Column(Text, nullable=True)
    color = Column(String(20), default="#F0B429")
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    def __repr__(self):
        return f"<Pillar {self.code}: {self.name}>"