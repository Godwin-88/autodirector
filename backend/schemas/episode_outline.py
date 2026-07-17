from pydantic import BaseModel
from typing import List


class SceneOutlineItem(BaseModel):
    scene_number: int
    scene_class_name: str        # e.g. "SceneDelta"
    title: str
    duration_target_secs: int
    key_equations: List[str]     # LaTeX strings
    key_sources: List[str]       # "Author (Year)" format
    voiceover_hint: str          # 1-sentence description of what to say


class EpisodeOutline(BaseModel):
    topic: str
    episode_number: int
    series: str
    seo_title: str
    scenes: List[SceneOutlineItem]

    @property
    def total_duration_target(self) -> int:
        return sum(s.duration_target_secs for s in self.scenes)