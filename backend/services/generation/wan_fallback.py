from pathlib import Path
import subprocess
import tempfile
from core.config import get_settings
from core.logging import get_logger

logger = get_logger("wan_fallback")


class WanFallback:
    """Fallback when Wan API is unavailable. Generates Manim title card."""

    FALLBACK_TEMPLATE = """
from manim import *
import numpy as np

config.background_color = "#0D1117"

class WanFallbackCard(Scene):
    def construct(self):
        # Episode title
        title = Text("{title}", color="#F0B429", font_size=48)
        title.to_edge(UP, buff=1.0)
        self.play(Write(title), run_time=1.5)

        # Episode topic
        topic = Text("{topic}", color="#E6EDF3", font_size=36)
        topic.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(topic, shift=UP), run_time=1.0)

        # Key equation
        if "{equation}":
            eq = MathTex(r"{equation}", color="#7C3AED", font_size=44)
            eq.next_to(topic, DOWN, buff=0.8)
            self.play(Write(eq), run_time=1.5)

        # Quantifaya branding
        brand = Text("QUANTIFAYA", color="#7C3AED", font_size=24, weight=BOLD)
        brand.to_corner(DR)
        self.play(FadeIn(brand), run_time=0.5)

        self.wait(2)
"""

    async def render(self, topic: str, episode_id: str, output_path: str,
                     key_equation: str = "", episode_title: str = "") -> Path:
        """Generate and render a Manim title card as Wan fallback."""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory() as tmpdir:
            script_path = Path(tmpdir) / "wan_fallback.py"
            script_content = self.FALLBACK_TEMPLATE.format(
                title=episode_title or "Quantifaya",
                topic=topic[:80],
                equation=key_equation,
            )
            script_path.write_text(script_content)

            quality = get_settings().manim_quality
            cmd = [
                "manim", f"-pq{quality}",
                str(script_path),
                "WanFallbackCard",
                "--media_dir", str(output.parent),
            ]

            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                if result.returncode != 0:
                    logger.error("wan_fallback_render_failed", stderr=result.stderr)
                    raise RuntimeError(f"Manim render failed: {result.stderr}")

                # Find the generated MP4
                video_dir = output.parent / "videos" / "wan_fallback"
                if video_dir.exists():
                    mp4s = list(video_dir.glob("*.mp4"))
                    if mp4s:
                        mp4s[0].rename(output)
                        logger.info("wan_fallback_rendered", path=str(output))
                        return output

                raise FileNotFoundError(f"No MP4 found in {video_dir}")
            except subprocess.TimeoutExpired:
                raise TimeoutError("Manim fallback render timed out")