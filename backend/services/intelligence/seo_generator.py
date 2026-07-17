from typing import List
from schemas.episode_outline import EpisodeOutline
from schemas.seo import SEOMetadata, ChapterMark
from services.intelligence.qwen_client import QwenClient, QWEN_TURBO
from core.logging import get_logger

logger = get_logger("seo_generator")

SEO_PROMPT = """
You are a YouTube SEO specialist for a quantitative finance channel.
Generate YouTube metadata for an episode.

Return JSON with:
- youtube_title: str (≤100 chars, keyword-front-loaded, include "| Quantifaya Ep.N")
- youtube_description: str (≥300 chars, first 200 chars are hook, include academic sources summary)
- tags: [str] (25-30 tags, mix of broad and specific)
- chapters: [{timestamp: "MM:SS", title: str}]
- pinned_comment: str (references list + challenge question)

Return valid JSON only. No markdown fences. No preamble.
"""


class SEOGenerator:
    def __init__(self, qwen: QwenClient):
        self.qwen = qwen

    async def generate(self, outline: EpisodeOutline) -> SEOMetadata:
        scenes_text = "\n".join(
            f"Scene {s.scene_number}: {s.title} ({s.duration_target_secs}s)"
            for s in outline.scenes
        )

        messages = [
            {"role": "system", "content": SEO_PROMPT},
            {"role": "user", "content": (
                f"Generate SEO metadata for Quantifaya Episode {outline.episode_number}.\n"
                f"Topic: {outline.topic}\n"
                f"SEO Title hint: {outline.seo_title}\n\n"
                f"Scene structure:\n{scenes_text}\n\n"
                "Generate the complete SEO metadata JSON."
            )},
        ]

        data = await self.qwen.complete_json(QWEN_TURBO, messages, temperature=0.3)

        # Auto-compute chapter timestamps from scene durations if not provided
        if not data.get("chapters"):
            data["chapters"] = self._compute_chapters(outline)

        return SEOMetadata(**data)

    def _compute_chapters(self, outline: EpisodeOutline) -> List[dict]:
        """Compute chapter timestamps from cumulative scene durations."""
        chapters = []
        cumulative = 0
        for scene in outline.scenes:
            minutes = cumulative // 60
            seconds = cumulative % 60
            timestamp = f"{minutes:02d}:{seconds:02d}"
            chapters.append({"timestamp": timestamp, "title": scene.title})
            cumulative += scene.duration_target_secs
        return chapters