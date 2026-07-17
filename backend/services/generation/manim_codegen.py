from pathlib import Path
from typing import List, Optional
import py_compile
import tempfile
from jinja2 import Environment, FileSystemLoader
from schemas.manim_spec import ManimSceneSpec
from services.intelligence.qwen_client import QwenClient, QWEN_MAX
from core import brand
from core.logging import get_logger

logger = get_logger("manim_codegen")

BRAND_CONSTANTS_BLOCK = f"""
# QUANTIFAYA BRAND — DO NOT MODIFY
BG        = "{brand.BG}"
FG        = "{brand.FG}"
GOLD      = "{brand.GOLD}"
RED       = "{brand.RED}"
GREEN     = "{brand.GREEN}"
BLUE_NORM = "{brand.BLUE_NORM}"
ORANGE    = "{brand.ORANGE}"
PURPLE    = "{brand.PURPLE}"
TEAL      = "{brand.TEAL}"
config.background_color = BG

def cite(refs: str):
    return Text(refs, color=TEAL, font_size=13).to_corner(DR).shift(UP*0.1+LEFT*0.1)
"""

TEMPLATE_MAP = {
    "equation_reveal": "equation_reveal.py.j2",
    "axes_curve": "axes_curve.py.j2",
    "two_column": "two_column.py.j2",
    "quote_box": "quote_box.py.j2",
}


class ManimCodeGenerator:
    def __init__(self, qwen: Optional[QwenClient] = None):
        self.qwen = qwen
        template_dir = Path(__file__).parent.parent.parent.parent / "manim_templates"
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))

    def _detect_template(self, spec: ManimSceneSpec) -> str:
        """Detect which template to use for a scene spec."""
        if spec.axes_config:
            return "axes_curve"
        if len(spec.equations) >= 2 and len(spec.text_blocks) >= 2:
            return "two_column"
        if any("quote" in tb.content.lower() or '"' in tb.content for tb in spec.text_blocks):
            return "quote_box"
        return "equation_reveal"

    async def generate_scene_code(self, spec: ManimSceneSpec) -> str:
        """Generate Python code for a single scene."""
        template_name = self._detect_template(spec)
        if template_name in TEMPLATE_MAP:
            template = self.env.get_template(TEMPLATE_MAP[template_name])
            return template.render(scene=spec)

        # If no template matches and we have Qwen, use LLM for complex scenes
        if self.qwen:
            return await self._generate_with_qwen(spec)

        # Fallback to equation_reveal
        template = self.env.get_template(TEMPLATE_MAP["equation_reveal"])
        return template.render(scene=spec)

    async def _generate_with_qwen(self, spec: ManimSceneSpec) -> str:
        """Use Qwen to generate Manim code for complex scenes."""
        messages = [
            {"role": "system", "content": (
                "You are a Manim animation expert. Generate a complete Manim scene class "
                "as Python code. Use the Quantifaya brand colors (BG, FG, GOLD, RED, GREEN, "
                "BLUE_NORM, ORANGE, PURPLE, TEAL) imported from constants. "
                "Include proper imports. Return ONLY valid Python code. No markdown fences."
            )},
            {"role": "user", "content": (
                f"Generate a Manim scene class named '{spec.scene_class_name}' with:\n"
                f"- Equations: {[e.latex for e in spec.equations]}\n"
                f"- Text blocks: {[tb.content for tb in spec.text_blocks]}\n"
                f"- Animation sequence: {[(a.type, a.target_id, a.duration_secs) for a in spec.animation_sequence]}\n"
                f"- Citation: {spec.cite_string}\n\n"
                "Return complete Python code for the scene class."
            )},
        ]
        code = await self.qwen.complete(QWEN_MAX, messages, temperature=0.3)
        # Clean up markdown fences
        code = code.strip()
        if code.startswith("```python"):
            code = code[9:]
        elif code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
        return code.strip()

    async def generate_episode_file(self, episode_id: str, scenes: List[ManimSceneSpec],
                                     output_dir: str = "./output/scripts") -> Path:
        """Generate complete episode Manim file with all scenes."""
        output_path = Path(output_dir) / f"quantifaya_ep{scenes[0].scene_class_name[:8]}_{episode_id[:8]}.py"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate code for each scene
        scene_data = []
        for spec in scenes:
            rendered_code = await self.generate_scene_code(spec)
            scene_data.append({
                "scene_class_name": spec.scene_class_name,
                "rendered_code": rendered_code,
            })

        # Render the full episode file
        template = self.env.get_template("base_template.py.j2")
        full_code = template.render(
            scenes=scene_data,
            brand_constants=BRAND_CONSTANTS_BLOCK,
        )

        # Validate syntax
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(full_code)
            tmp_path = f.name

        try:
            py_compile.compile(tmp_path, doraise=True)
        except py_compile.PyCompileError as e:
            logger.warning("manim_code_syntax_error", error=str(e))
            if self.qwen:
                full_code = await self._fix_syntax(full_code, str(e))

        output_path.write_text(full_code)
        logger.info("manim_episode_file_generated", path=str(output_path), scenes=len(scenes))
        return output_path

    async def _fix_syntax(self, code: str, error: str) -> str:
        """Send code + error to Qwen for syntax fix."""
        messages = [
            {"role": "system", "content": "Fix the syntax error in the following Python Manim code. Return ONLY the fixed code."},
            {"role": "user", "content": f"Error: {error}\n\nCode:\n{code}"},
        ]
        fixed = await self.qwen.complete(QWEN_MAX, messages, temperature=0.2)
        fixed = fixed.strip()
        if fixed.startswith("```python"):
            fixed = fixed[9:]
        elif fixed.startswith("```"):
            fixed = fixed[3:]
        if fixed.endswith("```"):
            fixed = fixed[:-3]
        return fixed.strip()