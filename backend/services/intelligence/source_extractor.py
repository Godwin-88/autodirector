from typing import List
from schemas.episode_outline import SceneOutlineItem
from schemas.source import AcademicSource, SourcesPackage
from services.intelligence.qwen_client import QwenClient, QWEN_MAX
from core.logging import get_logger

logger = get_logger("source_extractor")

SOURCE_EXTRACTOR_PROMPT = """
You are a financial economics research librarian. Your task is to find real, verifiable academic 
sources for a specific scene in a Quantifaya episode.

CRITICAL RULES:
1. Return ONLY real, verifiable academic works. If you are not certain a work exists with 
   this exact author, year, and title, omit it. Do not invent sources.
2. Each source must have a plausible author, year, title, and journal.
3. Return valid JSON only. No markdown fences. No preamble.
"""


class SourceExtractor:
    def __init__(self, qwen: QwenClient):
        self.qwen = qwen

    async def extract(self, scene: SceneOutlineItem, episode_topic: str) -> List[AcademicSource]:
        messages = [
            {"role": "system", "content": SOURCE_EXTRACTOR_PROMPT},
            {"role": "user", "content": (
                f"Episode topic: {episode_topic}\n"
                f"Scene {scene.scene_number}: {scene.title}\n"
                f"Key sources needed: {scene.key_sources}\n"
                f"Voiceover hint: {scene.voiceover_hint}\n\n"
                "Return a JSON object with a 'sources' array. Each source has:\n"
                "- ref_number: int\n"
                "- authors: str\n"
                "- year: int\n"
                "- title: str\n"
                "- journal_or_publisher: str\n"
                "- doi_or_url: str (optional)\n"
                "- scene_usage_note: str\n"
                "- confidence: str ('high' or 'low')\n\n"
                "Return at least 2 and at most 4 sources per scene."
            )},
        ]

        try:
            data = await self.qwen.complete_json(QWEN_MAX, messages, temperature=0.3)
            sources = [AcademicSource(**s) for s in data.get("sources", [])]

            # Run self-review for consistency
            sources = await self._self_review(sources, episode_topic, scene)
            return sources
        except Exception as e:
            logger.warning("source_extraction_failed", scene=scene.scene_number, error=str(e))
            return []

    async def _self_review(self, sources: List[AcademicSource], topic: str, scene: SceneOutlineItem) -> List[AcademicSource]:
        """Run a self-review Qwen call to check source consistency."""
        review_messages = [
            {"role": "system", "content": "Check each academic source for internal consistency. "
                                          "Author + year + title + journal must all be plausible together. "
                                          "Flag inconsistent sources with confidence: 'low'. Return JSON with sources array."},
            {"role": "user", "content": (
                f"Review these sources for scene '{scene.title}' on topic '{topic}':\n"
                + "\n".join(f"[{s.ref_number}] {s.authors} ({s.year}) '{s.title}' - {s.journal_or_publisher}"
                           for s in sources)
            )},
        ]
        try:
            data = await self.qwen.complete_json(QWEN_MAX, review_messages, temperature=0.2)
            reviewed = data.get("sources", [])
            if reviewed:
                return [AcademicSource(**s) if isinstance(s, dict) else s for s in reviewed]
        except Exception as e:
            logger.warning("source_self_review_failed", error=str(e))

        return sources