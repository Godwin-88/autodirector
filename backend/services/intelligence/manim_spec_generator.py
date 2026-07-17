from typing import List
from schemas.episode_outline import SceneOutlineItem
from schemas.source import AcademicSource
from schemas.manim_spec import ManimSceneSpec, EquationSpec, TextBlockSpec, AnimationStep
from services.intelligence.qwen_client import QwenClient, QWEN_MAX
from core.logging import get_logger

logger = get_logger("manim_spec_generator")

MANIM_SPEC_PROMPT = """
You are a Manim animation engineer. Given a scene outline and voiceover text, 
generate a structured Manim scene specification as JSON.

The spec must include:
- scene_class_name: PascalCase unique name
- equations: list of {id, latex, color, position, animation_type}
- text_blocks: list of {id, content, color, font_size, weight, slant}
- axes_config: optional {x_range, y_range, x_label, y_label, x_length, y_length}
- animation_sequence: ordered list of {step_number, type, target_id, duration_secs, notes}
- cite_string: academic citation text for on-screen display
- background_color: "#0D1117"

Animation types: Write, FadeIn, Create, Transform, FadeOut, SurroundingRectangle, wait, FadeInFromLeft
Colors: FG, GOLD, RED, GREEN, BLUE_NORM, ORANGE, PURPLE, TEAL

Return valid JSON only. No markdown fences. No preamble.
"""


class ManimSpecGenerator:
    def __init__(self, qwen: QwenClient):
        self.qwen = qwen

    async def generate(self, scene_outline: SceneOutlineItem, voiceover: str,
                       sources: List[AcademicSource]) -> ManimSceneSpec:
        sources_text = "; ".join(f"{s.authors} ({s.year})" for s in sources)

        messages = [
            {"role": "system", "content": MANIM_SPEC_PROMPT},
            {"role": "user", "content": (
                f"Scene {scene_outline.scene_number}: {scene_outline.title}\n"
                f"Scene class: {scene_outline.scene_class_name}\n"
                f"Duration target: {scene_outline.duration_target_secs}s\n"
                f"Key equations: {', '.join(scene_outline.key_equations)}\n"
                f"Sources: {sources_text}\n"
                f"Voiceover: {voiceover[:500]}\n\n"
                "Generate the Manim scene spec JSON."
            )},
        ]

        data = await self.qwen.complete_json(QWEN_MAX, messages, temperature=0.4)
        data["scene_class_name"] = scene_outline.scene_class_name
        return ManimSceneSpec(**data)