from pydantic import BaseModel
from typing import List, Optional


class SceneBeat(BaseModel):
    """A single narrative beat within a scene."""
    beat_id: str                            # e.g. "A", "B", "C_1"
    narration_text: str                     # full voiceover for this beat
    function: str = "derivation"            # hook|definition|derivation|example|comparison|critique|summary|citation|challenge
    duration_proportion: float = 0.0        # proportion of scene audio this beat consumes (computed from word count)


class SceneOutlineItem(BaseModel):
    scene_number: int
    scene_class_name: str        # e.g. "SceneDelta"
    title: str
    duration_target_secs: int
    key_equations: List[str]     # LaTeX strings
    key_sources: List[str]       # "Author (Year)" format
    voiceover_hint: str          # 1-sentence description of what to say
    full_voiceover: str = ""     # NEW: full voiceover text for the entire scene
    beats: List[SceneBeat] = []  # NEW: structured beats with per-beat narration text
    narrative_function: str = "derivation"  # hook|definition|derivation|example|comparison|critique|summary|citation|challenge


class EpisodeOutline(BaseModel):
    topic: str
    episode_number: int
    series: str
    seo_title: str
    scenes: List[SceneOutlineItem]

    @property
    def total_duration_target(self) -> int:
        return sum(s.duration_target_secs for s in self.scenes)

    def compute_beat_proportions(self) -> None:
        """Compute proportional duration for each beat based on word count."""
        for scene in self.scenes:
            total_words = sum(len(b.narration_text.split()) for b in scene.beats)
            if total_words == 0:
                continue
            for beat in scene.beats:
                beat.duration_proportion = len(beat.narration_text.split()) / total_words