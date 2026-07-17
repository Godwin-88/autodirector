from pydantic import BaseModel
from typing import List


class AcademicSource(BaseModel):
    ref_number: int
    authors: str
    year: int
    title: str
    journal_or_publisher: str
    doi_or_url: str = ""
    scene_usage_note: str
    confidence: str = "high"     # high|low — low = flagged for human review


class SourcesPackage(BaseModel):
    episode_topic: str
    sources: List[AcademicSource]