from manim import *

config.background_color = "#0D1117"


class BrandIntro(Scene):
    def construct(self):
        # Quantifaya logo text in purple
        logo = Text("QUANTIFAYA", color="#7C3AED", font_size=72, weight=BOLD)
        logo.scale(0.8)
        self.play(Write(logo), run_time=1.5)
        self.play(logo.animate.scale(1.1), run_time=0.5)
        self.play(logo.animate.scale(1.0), run_time=0.5)

        # Tagline in gold
        tagline = Text(
            "Financial Engineering.\nExplained Rigorously.\nApplied Practically.",
            color="#F0B429",
            font_size=28,
            line_spacing=1.2,
        )
        tagline.next_to(logo, DOWN, buff=0.8)
        self.play(FadeIn(tagline, shift=UP), run_time=1.5)

        # Decorative line
        line = Line(
            LEFT * 3, RIGHT * 3,
            color="#4C9BE8",
            stroke_width=2,
        )
        line.next_to(tagline, DOWN, buff=0.5)
        self.play(Create(line), run_time=0.8)

        self.wait(1)