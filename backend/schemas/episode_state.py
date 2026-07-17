# LangGraph state — TypedDict, not Pydantic
from typing import TypedDict, Optional, List, Dict, Any


class EpisodeState(TypedDict):
    episode_id: str
    topic: str
    episode_number: int
    series: str
    outline: Optional[Dict[str, Any]]
    sources: Optional[Dict[str, Any]]
    script: Optional[Dict[str, Any]]
    manim_specs: Optional[List[Dict[str, Any]]]
    wan_prompt: Optional[str]
    seo_metadata: Optional[Dict[str, Any]]
    scene_video_paths: Optional[List[str]]
    scene_audio_paths: Optional[List[str]]
    scene_synced_paths: Optional[List[str]]
    wan_clip_path: Optional[str]
    final_video_path: Optional[str]
    youtube_id: Optional[str]
    wan_fallback: bool
    errors: List[str]
    current_phase: str