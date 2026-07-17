import json
from typing import List, Dict, Any
from schemas.episode_outline import EpisodeOutline
from schemas.source import SourcesPackage, AcademicSource
from services.intelligence.qwen_client import QwenClient, QWEN_MAX
from services.intelligence.persona import QUANTIFAYA_PERSONA, PERSONA_SELF_REVIEW_CHECKLIST
from core.logging import get_logger

logger = get_logger("script_generator")

SCRIPT_SYSTEM_PROMPT = QUANTIFAYA_PERSONA + """

You are writing the full voice-over script for a Quantifaya episode.
Each scene must have:
- voiceover_text: The spoken narration (300-500 words per scene)
- stage_directions: List of visual/audio cues for the editor

Return JSON with structure:
{
  "episode_id": str,
  "scenes": [
    {
      "scene_number": int,
      "scene_class": str,
      "voiceover_text": str,
      "stage_directions": [str]
    }
  ]
}
"""


class ScriptGenerator:
    def __init__(self, qwen: QwenClient):
        self.qwen = qwen

    async def generate(self, outline: EpisodeOutline, sources: SourcesPackage) -> dict:
        sources_text = "\n".join(
            f"[{s.ref_number}] {s.authors} ({s.year}) '{s.title}' - {s.journal_or_publisher}"
            for s in sources.sources
        )

        scenes_text = "\n".join(
            f"Scene {s.scene_number} ({s.scene_class_name}): {s.title}\n"
            f"  Duration: {s.duration_target_secs}s\n"
            f"  Key equations: {', '.join(s.key_equations)}\n"
            f"  Voiceover hint: {s.voiceover_hint}"
            for s in outline.scenes
        )

        messages = [
            {"role": "system", "content": SCRIPT_SYSTEM_PROMPT},
            {"role": "user", "content": (
                f"Write a full script for episode {outline.episode_number} of Quantifaya.\n"
                f"Topic: {outline.topic}\n"
                f"SEO Title: {outline.seo_title}\n\n"
                f"Available academic sources:\n{sources_text}\n\n"
                f"Scene structure:\n{scenes_text}\n\n"
                "Write the complete script. Every scene must have voiceover_text and stage_directions. "
                "Include [PAUSE] markers. Include *stage directions* in asterisks. "
                "Quote Taleb at least once with exact source. End with a challenge question."
            )},
        ]

        data = await self.qwen.complete_json(QWEN_MAX, messages, temperature=0.7)

        # Run self-review checklist
        review_result = await self._self_review(data)
        if review_result.get("fixes_required"):
            logger.info("script_self_review_fixes_needed", fixes=review_result["fixes_required"])
            # Regenerate flagged scenes
            for fix in review_result["fixes_required"]:
                scene_num = fix.get("scene_number")
                if scene_num:
                    data = await self._regenerate_scene(data, scene_num, fix.get("fix", ""))

        return data

    async def _self_review(self, script: dict) -> dict:
        messages = [
            {"role": "system", "content": PERSONA_SELF_REVIEW_CHECKLIST},
            {"role": "user", "content": json.dumps(script)},
        ]
        try:
            return await self.qwen.complete_json(QWEN_MAX, messages, temperature=0.2)
        except Exception as e:
            logger.warning("script_self_review_failed", error=str(e))
            return {"scores": {}, "fixes_required": []}

    async def _regenerate_scene(self, script: dict, scene_number: int, fix_instruction: str) -> dict:
        messages = [
            {"role": "system", "content": QUANTIFAYA_PERSONA},
            {"role": "user", "content": (
                f"Regenerate scene {scene_number} of the following script. "
                f"Fix required: {fix_instruction}\n\n"
                f"Current script: {json.dumps(script)}"
            )},
        ]
        try:
            updated = await self.qwen.complete_json(QWEN_MAX, messages, temperature=0.7)
            if "scenes" in updated:
                for scene in updated["scenes"]:
                    if scene.get("scene_number") == scene_number:
                        for i, s in enumerate(script.get("scenes", [])):
                            if s.get("scene_number") == scene_number:
                                script["scenes"][i] = scene
                                break
        except Exception as e:
            logger.warning("scene_regeneration_failed", scene=scene_number, error=str(e))
        return script