from manim import *

config.background_color = "#0D1117"


class BrandOutro(Scene):
    def construct(self):
        # Subscribe prompt
        subscribe = Text(
            "Subscribe for rigorous financial engineering",
            color="#E6EDF3",
            font_size=32,
        )
        subscribe.to_edge(UP, buff=1.5)
        self.play(Write(subscribe), run_time=1.5)

        # Channel handle
        handle = Text(
            "@Quantifaya",
            color="#F0B429",
            font_size=48,
            weight=BOLD,
        )
        handle.next_to(subscribe, DOWN, buff=0.8)
        self.play(FadeIn(handle, shift=UP), run_time=1.0)

        # Next episode tease
        next_ep = Text(
            "Next Episode:\nComing Soon",
            color="#7C3AED",
            font_size=28,
            line_spacing=1.2,
        )
        next_ep.next_to(handle, DOWN, buff=1.0)
        self.play(FadeIn(next_ep, shift=UP), run_time=1.0)

        # Decorative line
        line = Line(
            LEFT * 2, RIGHT * 2,
            color="#4C9BE8",
            stroke_width=1,
        )
        line.next_to(next_ep, DOWN, buff=0.5)
        self.play(Create(line), run_time=0.5)

        self.wait(1.5)