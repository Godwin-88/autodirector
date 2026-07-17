from pydantic import BaseModel
from typing import List


class ChapterMark(BaseModel):
    timestamp: str           # "00:00"
    title: str


class SEOMetadata(BaseModel):
    youtube_title: str       # ≤100 chars
    youtube_description: str # ≥300 chars
    tags: List[str]          # 25-30 tags
    chapters: List[ChapterMark]
    pinned_comment: str