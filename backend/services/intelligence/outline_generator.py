from typing import List
from schemas.episode_outline import EpisodeOutline, SceneOutlineItem
from services.intelligence.qwen_client import QwenClient, QWEN_MAX
from services.intelligence.persona import QUANTIFAYA_PERSONA
from core.logging import get_logger

logger = get_logger("outline_generator")

OUTLINE_SYSTEM_PROMPT = QUANTIFAYA_PERSONA + """

You are generating a structured episode outline for a Quantifaya episode.
Return ONLY valid JSON matching the schema. No preamble, no postamble.
"""

OUTLINE_USER_TEMPLATE = """
Generate a structured episode outline for a 25-minute Quantifaya episode on: "{topic}"

Return JSON matching this exact schema:
{{
  "topic": str,
  "episode_number": int,
  "series": "quantifaya",
  "seo_title": str,  // ≤100 chars, keyword-front-loaded
  "scenes": [
    {{
      "scene_number": int,
      "scene_class_name": str,  // PascalCase, e.g. "SceneDelta"
      "title": str,
      "duration_target_secs": int,  // 90-300 per scene
      "key_equations": [str],  // LaTeX strings, no $ wrappers
      "key_sources": [str],  // "Author (Year)" format
      "voiceover_hint": str  // one sentence: what this scene argues
    }}
  ]
}}

Rules:
- 8-12 scenes
- Scene durations must sum to 1400-1600 seconds
- Scene 1 must be a cold open with a shocking hook (a crisis, a failure, a number)
- Final scene must be outro with challenge question and next episode tease
- scene_class_name must be unique per episode
"""


class OutlineGenerator:
    def __init__(self, qwen: QwenClient):
        self.qwen = qwen

    async def generate(self, topic: str, episode_number: int, series: str) -> EpisodeOutline:
        messages = [
            {"role": "system", "content": OUTLINE_SYSTEM_PROMPT},
            {"role": "user", "content": OUTLINE_USER_TEMPLATE.format(topic=topic)},
        ]

        for attempt in range(3):
            try:
                data = await self.qwen.complete_json(QWEN_MAX, messages)
                data["episode_number"] = episode_number
                data["series"] = series
                outline = EpisodeOutline(**data)
                logger.info("outline_generated", topic=topic, scenes=len(outline.scenes),
                            total_duration=outline.total_duration_target)
                return outline
            except Exception as e:
                logger.warning("outline_validation_failed", attempt=attempt + 1, error=str(e))
                if attempt < 2:
                    messages.append({
                        "role": "user",
                        "content": f"Validation error: {e}. Please fix and return valid JSON."
                    })
                else:
                    raise