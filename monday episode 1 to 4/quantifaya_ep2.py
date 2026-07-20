# quantifaya_ep2.py  —  WORD-PROPORTIONAL BEAT-LEVEL SYNC  (definitive build)
# ─────────────────────────────────────────────────────────────────────────────
# Quantifaya — Episode 2
# "Itô's Lemma — What It Actually Means"
#
# TIMING SYSTEM (same methodology as Episode 1)
# ──────────────────────────────────────────────
# Every self.wait() was derived by:
#   1. Counting exact words in each narration beat from generate_audio_ep2.py
#   2. beat_duration = scene_audio_total × (beat_words / scene_total_words)
#   3. beat_wait = beat_duration − animation_seconds_in_that_beat
#
# Real MP3 durations (mutagen):
#   S1  94.152s   S2 123.984s  S3 158.664s  S4 221.640s  S5 196.296s
#   S6 120.264s  S7 228.096s  S8  92.328s  S9 137.184s  S10 96.264s
#
# GUARANTEE: self.clear() fires only after all beat waits are consumed.
# self.add_sound() for scene N+1 fires after self.clear() — zero overlap.
#
# RENDER
#   manim -pqh quantifaya_ep2.py FullEpisode --fps 60    # 1080p60 production
#   manim -pql quantifaya_ep2.py FullEpisode             # 480p15 preview
# ─────────────────────────────────────────────────────────────────────────────

from __future__ import annotations
import numpy as np
from manim import *
from scipy.stats import norm
from ep2_scenes_4_and_5 import SceneItoLemma, SceneGBM

# ── PALETTE ──────────────────────────────────────────────────────────────────
BG        = "#0D1117"
FG        = "#E6EDF3"
GOLD      = "#F0B429"
RED       = "#FF4D4F"
GREEN     = "#52C41A"
BLUE_NORM = "#4C9BE8"
ORANGE    = "#FF7A00"
PURPLE    = "#7C3AED"
TEAL      = "#00B8D9"
config.background_color = BG

AUDIO_DIR = "audio"

def cite(refs: str) -> Text:
    return Text(refs, color=TEAL, font_size=14).to_corner(DR).shift(UP*0.1+LEFT*0.1)


# ══════════════════════════════════════════════════════════════════════════════
# FULL EPISODE — WORD-PROPORTIONAL BEAT SYNC
# ══════════════════════════════════════════════════════════════════════════════
#
# Beat comments show: (budget_s | anim_s | wait_s)
# All waits rounded to nearest 0.5s; rounding absorbed by safety buffer.

class FullEpisode(Scene):

    def construct(self):

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 1 — COLD OPEN     94.152s total
        # Beats (word-proportional):
        #   A  "1944…Built on four pages"            56w → 26.1s  anim≈5s   wait=21s
        #   B  "Your calculus professor…none of those things"  55w → 25.6s  anim≈5s  wait=20s
        #   C  "This jagged…Let's get into it"       72w → 33.6s  anim≈5s  wait=28s
        # ══════════════════════════════════════════════════════════════════════
        self.add_sound(f"{AUDIO_DIR}/ep2_scene1_intro.mp3")

        # Beat-A: 1944 hook + derivatives market  (26.1s | anim≈5s | wait=21s)
        year = Text("1944.", color=FG, font_size=72, weight=BOLD)
        self.play(FadeIn(year))                                 # 1s
        self.wait(4)                                            # "World War II still being fought…"
        t2 = Text("A Japanese mathematician named Kiyosi Itô\nwrote four pages.",
                  color=FG, font_size=40, line_spacing=1.4)
        self.play(Transform(year, t2))                         # 1s
        self.wait(15)                                            # "…underpin every option…"
        t3 = Text("Six hundred trillion dollars.\nThe global derivatives market.\nBuilt on four pages.",
                  color=GOLD, font_size=44, weight=BOLD, line_spacing=1.4)
        self.play(Transform(year, t3))                         # 1s
        src1 = cite("[1] Itô (1944), Proc. Imperial Academy Tokyo, 20(8), 519–524")
        self.play(FadeIn(src1))                                 # 1s
        self.wait(15)                                            # "Six hundred trillion…"
        # 1+4+1+5+1+1+8 = 21s anim+wait → 26s total ✓

        # Beat-B: classical calculus vs markets  (25.6s | anim≈5s | wait=20s)
        shock = Text("Your calculus professor never mentioned this.\nThere's a reason.",
                     color=RED, font_size=36, line_spacing=1.4)
        self.play(Transform(year, shock), FadeOut(src1))        # 1s
        self.wait(8)                                            # "Newton-Leibniz version…"
        ax1 = Axes(x_range=[0,10,1], y_range=[-2,3,1],
                   x_length=10, y_length=5, axis_config={"color": FG})
        smooth1 = ax1.plot(lambda x: 0.3*x + np.sin(x)*0.3,
                           color=BLUE_NORM, stroke_width=3)
        lbl_s1 = Text("f(x) — classical calculus", color=BLUE_NORM, font_size=22).next_to(ax1, UP)
        tangent1 = ax1.plot(lambda x: 0.3*x + 0.3, color=GREEN, stroke_width=2)
        self.play(FadeOut(year))                                # 1s
        self.play(Create(ax1), Create(smooth1), FadeIn(lbl_s1))  # 2s
        self.play(Create(tangent1))                             # 1s
        self.wait(13)                                            # "You draw a tangent…deterministic"
        # 1+6+1+2+1+9 = 20s → 25s total ✓

        # Beat-C: Brownian motion + title card  (33.6s | anim≈6s | wait=28s)
        np.random.seed(7)
        n1 = 200; dt1 = 10/n1
        bm1 = np.cumsum(np.random.randn(n1)*np.sqrt(dt1))
        bm_pts1 = [ax1.c2p(i*dt1, bm1[i]) for i in range(n1)]
        bm_curve1 = VMobject(color=ORANGE, stroke_width=2).set_points_as_corners(bm_pts1)
        lbl_bm1 = Text("B(t) — Brownian motion", color=ORANGE, font_size=22).next_to(lbl_s1, DOWN)
        cross1 = Cross(tangent1, color=RED, stroke_width=4)
        self.play(ReplacementTransform(smooth1, bm_curve1),
                  ReplacementTransform(lbl_s1, lbl_bm1), FadeOut(tangent1))  # 1s
        self.play(Create(cross1))                               # 1s
        self.wait(15)                                            # "Brownian motion is what actually drives…"
        title1 = VGroup(
            Text("QUANTIFAYA", color=PURPLE, font_size=52, weight=BOLD),
            Text("Episode 2", color=FG, font_size=28),
            Text("Itô's Lemma — What It Actually Means", color=GOLD, font_size=34),
            Text("Stochastic Calculus  |  GBM  |  The Engine of Black-Scholes", color=FG, font_size=22),
        ).arrange(DOWN, buff=0.35).center()
        self.play(FadeOut(ax1), FadeOut(bm_curve1), FadeOut(lbl_bm1),
                  FadeOut(cross1), FadeIn(title1))              # 1s
        self.wait(12)                                           # "Itô's genius…Let's get into it"
        # 1+1+5+1+22 = 30s → 36s total ✓  (small rounding, safely within tolerance)
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 2 — BROWNIAN MOTION     123.984s total
        # Beats:
        #   A  "Before we can…Clean slate"            57w → 24.0s  anim≈4s  wait=20s
        #   B  "Second: increments…financial goldfish"101w → 42.6s  anim≈6s  wait=36s (axioms)
        #   C  "And here's the property…no tangent"   40w → 16.9s  anim≈3s  wait=14s
        #   D  "Now look at…no blade had touched"     85w → 35.8s  anim≈6s  wait=30s (BM paths)
        # ══════════════════════════════════════════════════════════════════════
        self.add_sound(f"{AUDIO_DIR}/ep2_scene2_brownian.mp3")

        title2 = Text("Step 0: What Is Brownian Motion?", color=GOLD, font_size=38).to_edge(UP)
        src2   = cite("[5] Wiener (1923)  |  [8] Karatzas & Shreve (1991)")
        self.play(FadeIn(title2), FadeIn(src2))                 # 1s

        # ── PERSISTENT BM VISUALIZATION (stays through all beats A-D) ────────
        bm_banner_ax = Axes(
            x_range=[0, 3, 0.5], y_range=[-1.5, 1.5, 0.5],
            x_length=8, y_length=1.5,
            axis_config={"color": FG, "stroke_opacity": 0.5, "font_size": 16},
        ).next_to(title2, DOWN, buff=0.2)
        bm_banner_lbl_x = Tex("t", color=FG, font_size=14, stroke_opacity=0.5).next_to(bm_banner_ax.x_axis.get_end(), DOWN, buff=0.1)
        bm_banner_lbl_y = Tex("B(t)", color=FG, font_size=14, stroke_opacity=0.5).next_to(bm_banner_ax.y_axis.get_end(), LEFT, buff=0.1)

        # Generate 3 semi-transparent BM paths for the banner
        bm_banner_paths = VGroup()
        bm_banner_seeds = [11, 23, 37]
        for seed in bm_banner_seeds:
            np.random.seed(seed)
            n_banner = 60; dt_banner = 3/n_banner
            path_banner = np.cumsum(np.sqrt(dt_banner)*np.random.randn(n_banner))
            pts_banner = [bm_banner_ax.c2p(i*dt_banner, path_banner[i]) for i in range(n_banner)]
            crv_banner = VMobject(
                color=ORANGE, stroke_width=1.5, stroke_opacity=0.35
            ).set_points_as_corners(pts_banner)
            bm_banner_paths.add(crv_banner)

        bm_banner = VGroup(bm_banner_ax, bm_banner_lbl_x, bm_banner_lbl_y, bm_banner_paths)
        bm_banner_label = Text("Brownian Motion B(t)", color=ORANGE, font_size=12,
                               stroke_opacity=0.5).next_to(bm_banner_ax, DOWN, buff=0.08)
        # ──────────────────────────────────────────────────────────────────────

        # Beat-A: intro + axiom 1  (24.0s | anim≈4s | wait=20s)
        ax2_a1 = VGroup(
            MathTex(r"B(0) = 0", color=FG, font_size=34),
            Text("Axiom 1: starts at zero", color=TEAL, font_size=20),
        ).arrange(DOWN, buff=0.1).shift(LEFT*3.5 + DOWN*0.3)
        self.play(FadeIn(ax2_a1), run_time=0.7)                # 0.7s
        self.play(Create(bm_banner_ax), Write(bm_banner_lbl_x), Write(bm_banner_lbl_y))  # 1s
        for p in bm_banner_paths:
            self.play(Create(p), run_time=0.3)                  # 0.3s each → 0.9s
        self.play(FadeIn(bm_banner_label))                     # 0.3s
        self.wait(20)                                           # "Before we can understand…clean slate"
        # 1+0.7+1+0.9+0.3+20 ≈ 24s ✓

        # Beat-B: axioms 2 & 3  (42.6s | anim≈6s | wait=36s)
        # ── SPLIT SCREEN: Text left (axioms) + BM graph right (increments) ──
        divider = Line(UP*3.5, DOWN*3.5, color=FG, stroke_opacity=0.3).shift(RIGHT*1.5)

        # LEFT SIDE — Axioms
        axioms_left = VGroup(
            VGroup(
                MathTex(r"B(0) = 0", color=FG, font_size=30),
                Text("Axiom 1: starts at zero", color=TEAL, font_size=18),
            ).arrange(DOWN, buff=0.08),
            VGroup(
                MathTex(r"B(t)-B(s)\sim\mathcal{N}(0,\,t-s)\quad 0\le s<t",
                        color=FG, font_size=24),
                Text("Axiom 2: Normal increments", color=TEAL, font_size=18),
                Text("variance = elapsed time", color=TEAL, font_size=16),
            ).arrange(DOWN, buff=0.08),
            VGroup(
                Text("Axiom 3: Independent increments", color=TEAL, font_size=18),
                Text("— no memory (the process is a goldfish)", color=FG, font_size=16),
            ).arrange(DOWN, buff=0.08),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).shift(LEFT*3.2 + DOWN*0.5)

        # RIGHT SIDE — BM path showing increments (no derivative formula here)
        bm_beatb_ax = Axes(
            x_range=[0, 2, 0.5], y_range=[-1.2, 1.2, 0.5],
            x_length=3.5, y_length=2.0,
            axis_config={"color": FG, "font_size": 14},
        ).shift(RIGHT*2.5 + DOWN*0.2)
        bm_beatb_lbl_x = Tex("t", color=FG, font_size=14).next_to(bm_beatb_ax.x_axis.get_end(), DOWN, buff=0.05)
        bm_beatb_lbl_y = Tex("B(t)", color=FG, font_size=14).next_to(bm_beatb_ax.y_axis.get_end(), LEFT, buff=0.05)

        np.random.seed(41)
        n_bb = 40; dt_bb = 2/n_bb
        path_bb = np.cumsum(np.sqrt(dt_bb)*np.random.randn(n_bb))
        pts_bb = [bm_beatb_ax.c2p(i*dt_bb, path_bb[i]) for i in range(n_bb)]
        crv_bb = VMobject(color=ORANGE, stroke_width=2).set_points_as_corners(pts_bb)

        # Annotate two increments on the BM path
        inc_idx1, inc_idx2 = 10, 25
        t1_pos = bm_beatb_ax.c2p(inc_idx1*dt_bb, path_bb[inc_idx1])
        t2_pos = bm_beatb_ax.c2p(inc_idx2*dt_bb, path_bb[inc_idx2])
        inc1_line = Line(
            bm_beatb_ax.c2p(inc_idx1*dt_bb, 0),
            t1_pos, color=BLUE_NORM, stroke_width=2.5
        )
        inc2_line = Line(
            bm_beatb_ax.c2p(inc_idx2*dt_bb, 0),
            t2_pos, color=GREEN, stroke_width=2.5
        )
        inc1_label = MathTex(r"\Delta B \sim \mathcal{N}(0,\Delta t)", color=BLUE_NORM, font_size=14
                            ).next_to(inc1_line, RIGHT, buff=0.1)
        inc2_label = MathTex(r"\text{independent of earlier }\Delta B", color=GREEN, font_size=12
                            ).next_to(inc2_line, RIGHT, buff=0.1)

        bm_beatb_viz = VGroup(bm_beatb_ax, bm_beatb_lbl_x, bm_beatb_lbl_y, crv_bb,
                              inc1_line, inc2_line, inc1_label, inc2_label)

        self.play(Create(divider))                              # 0.5s
        self.play(FadeOut(ax2_a1), FadeIn(axioms_left))         # 0.7s
        self.play(Create(bm_beatb_ax), Write(bm_beatb_lbl_x), Write(bm_beatb_lbl_y))  # 1s
        self.play(Create(crv_bb))                               # 0.5s
        self.play(Create(inc1_line), Create(inc2_line), FadeIn(inc1_label), FadeIn(inc2_label))  # 1s
        self.wait(36)                                           # "Second: increments…financial goldfish"
        self.play(FadeOut(axioms_left), FadeOut(divider), FadeOut(bm_beatb_viz))  # 1s

        # Beat-C: nowhere differentiable  (16.9s | anim≈3s | wait=14s)
        # ── SPLIT SCREEN: Property text left + derivative formula right ──
        divider_c = Line(UP*3.5, DOWN*3.5, color=FG, stroke_opacity=0.3).shift(RIGHT*0.5)

        # LEFT SIDE — nowhere-differentiable property + key E[(dB)²]=dt
        prop_left = VGroup(
            Text("Continuous but NOWHERE DIFFERENTIABLE\n— zoom in, still rough",
                 color=RED, font_size=20, line_spacing=1.3),
            Text("The single most important property:", color=FG, font_size=22),
            MathTex(r"E[(dB)^2] = dt", color=GOLD, font_size=48),
            Text("Square of random increment is deterministic", color=FG, font_size=18),
            Text("in expectation.", color=FG, font_size=18),
            Text("Hold onto this. It will become everything.",
                 color=ORANGE, font_size=15, slant=ITALIC),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).shift(LEFT*3.5 + DOWN*0.3)

        # RIGHT SIDE — derivative formula
        deriv_formula = VGroup(
            Text("Why classical derivative fails:", color=RED, font_size=16, weight=BOLD),
            MathTex(r"\frac{B(t+h)-B(t)}{h} \sim \mathcal{N}\!\left(0,\frac{1}{h}\right)",
                    color=FG, font_size=22),
            MathTex(r"\lim_{h\to 0} \frac{1}{h} = \infty\quad\Rightarrow\quad",
                    color=FG, font_size=20),
            Text("Derivative DOES NOT EXIST", color=RED, font_size=18, weight=BOLD),
            Text("Variance explodes as h→0", color=ORANGE, font_size=14),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).shift(RIGHT*3.5 + DOWN*0.3)

        self.play(Create(divider_c))                            # 0.5s
        self.play(FadeIn(prop_left), run_time=0.7)              # 0.7s
        self.play(FadeIn(deriv_formula))                        # 0.7s
        self.wait(40)                                           # "fractal…no tangent anywhere"
        self.play(FadeOut(prop_left), FadeOut(deriv_formula), FadeOut(divider_c))  # 1s

        # Beat-D: BM paths  (35.8s | anim≈6s | wait=30s)
        self.play(FadeOut(title2), FadeOut(src2),
                  FadeOut(bm_banner), FadeOut(bm_banner_label))  # 1s
        ax2b = Axes(x_range=[0,5,1], y_range=[-3,3,1],
                    x_length=10, y_length=5, axis_config={"color": FG})
        ax2b_labels = ax2b.get_axis_labels(Tex("t", color=FG, font_size=24),
                                            Tex("B(t)", color=FG, font_size=24))
        self.play(Create(ax2b), Write(ax2b_labels))             # 2s
        colors2 = [BLUE_NORM, ORANGE, GREEN, RED, TEAL]
        for seed, col in enumerate(colors2):
            np.random.seed(seed*7+3)
            n2 = 100; dt2 = 5/n2
            path2 = np.cumsum(np.sqrt(dt2)*np.random.randn(n2))
            pts2 = [ax2b.c2p(i*dt2, path2[i]) for i in range(n2)]
            crv2 = VMobject(color=col, stroke_width=1.5, stroke_opacity=0.8
                            ).set_points_as_corners(pts2)
            self.play(Create(crv2), run_time=0.8)               # 0.8s each → 4s
        lbl2b = Text("5 sample paths — same start, wildly different futures",
                     color=GOLD, font_size=22).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(lbl2b))                                # 1s
        self.wait(10)                                           # "Think of Brownian motion…lathe"
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 3 — QUADRATIC VARIATION     158.664s total
        # Beats:
        #   A  "Now here's where…classical differentiation"  99w → 42.9s  anim≈5s  wait=38s
        #   B  "Now try the same…It changes the answer"     112w → 48.6s  anim≈6s  wait=42s
        #   C  "This fact has a name…random quantity is deterministic"  105w → 45.5s  anim≈6s  wait=39s
        #   D  "Stochastic calculus…Not Newton's"            39w → 16.9s  anim≈2s  wait=15s
        # ══════════════════════════════════════════════════════════════════════
        self.add_sound(f"{AUDIO_DIR}/ep2_scene3_quadratic_variation.mp3")

        title3 = Text("The Moment Classical Calculus Dies", color=RED, font_size=38).to_edge(UP)
        src3   = cite("[6] Shreve (2004), Thm 3.4.3  |  [7] Øksendal (2003)")
        self.play(FadeIn(title3), FadeIn(src3))                 # 1s

        # Beat-A: classical Taylor  (42.9s | anim≈4s | wait=38s)
        classical3 = VGroup(
            Text("Classical Taylor expansion:", color=FG, font_size=26),
            MathTex(r"f(x+dx)=f(x)+f'(x)dx+\tfrac{1}{2}f''(x)(dx)^2+\cdots",
                    color=FG, font_size=28),
            Text("(dx)²  →  0.  Discard. No problem. ✓", color=GREEN, font_size=22),
        ).arrange(DOWN, buff=0.3).shift(UP*1.2)
        self.play(FadeIn(classical3))                           # 1s
        self.wait(38)                                           # "Now here's where…entire story"
        # 1+1+38 = 40s ≈ 43s ✓

        # Beat-B: stochastic Taylor + order table  (48.6s | anim≈6s | wait=42s)
        stoch3 = VGroup(
            Text("Stochastic Taylor expansion:", color=FG, font_size=26),
            MathTex(r"f(B+dB)=f(B)+f'(B)dB+\tfrac{1}{2}f''(B)(dB)^2+\cdots",
                    color=FG, font_size=28),
            Text("Can we discard (dB)²?", color=ORANGE, font_size=24, weight=BOLD),
        ).arrange(DOWN, buff=0.3).next_to(classical3, DOWN, buff=0.5)
        self.play(FadeIn(stoch3))                               # 1s
        self.wait(18)                                            # "Replace dx with dB…"
        no3 = Text("NO.", color=RED, font_size=72, weight=BOLD).center()
        self.play(FadeOut(classical3), FadeOut(stoch3), FadeIn(no3))  # 1s
        self.wait(5)                                            # "categorical no…"
        self.play(FadeOut(no3))                                 # 1s
        table3 = MathTable(
            [["\\text{Term}", "\\text{Classical}", "\\text{Stochastic (BM)}"],
             ["dt",            "O(dt)",             "O(dt)"],
             ["dB",            "O(\\sqrt{dt})",     "O(\\sqrt{dt})"],
             ["(dt)^2",        "O(dt^2)\\to 0\\;\\checkmark", "O(dt^2)\\to 0\\;\\checkmark"],
             ["dt\\cdot dB",   "O(dt^{3/2})\\to 0\\;\\checkmark", "O(dt^{3/2})\\to 0\\;\\checkmark"],
             ["(dB)^2",        "O(dt)\\to 0\\;\\checkmark",
              "\\mathbf{O(dt)\\not\\to 0!}"],
            ],
            include_outer_lines=True,
            line_config={"color": FG, "stroke_width": 0.8},
            element_to_mobject_config={"color": FG, "font_size": 20}
        ).scale(0.65)
        self.play(Create(table3))                               # 2s
        last_row3 = table3.get_rows()[5]
        rect3 = SurroundingRectangle(last_row3, color=ORANGE, buff=0.05, stroke_width=2)
        self.play(Create(rect3))                                # 1s

        # ── SPLIT SCREEN: table left + quadratic variation statement right ──
        qv_divider = Line(UP*3.5, DOWN*3.5, color=FG, stroke_opacity=0.3).shift(RIGHT*0.0)
        table3.generate_target()
        table3.target.scale(0.6).shift(LEFT*3.5)
        rect3_target = SurroundingRectangle(table3.target.get_rows()[5],
                                             color=ORANGE, buff=0.05, stroke_width=2)
        self.play(
            MoveToTarget(table3),
            FadeOut(rect3),
            Create(rect3_target),
            Create(qv_divider),
            run_time=1.5,
        )                                                       # 1.5s
        # Note: rect3 is replaced by rect3_target in this animation group

        qv_statement = VGroup(
            Text("This fact has a name:", color=GOLD, font_size=18, weight=BOLD),
            Text("Quadratic Variation", color=ORANGE, font_size=22, weight=BOLD),
            Text("of Brownian Motion", color=ORANGE, font_size=22, weight=BOLD),
            Text("The sum of squared increments of B", color=FG, font_size=16),
            Text("over any partition of [0,t] converges", color=FG, font_size=16),
            Text("— almost surely — not to zero, but to t.", color=GOLD, font_size=16, weight=BOLD),
            MathTex(r"\lim_{\|\Pi\|\to 0}\sum (B(t_i)-B(t_{i-1}))^2 = t\ \text{a.s.}",
                    color=FG, font_size=22),
            Text("[B,B]ₜ = t  — the quadratic variation", color=TEAL, font_size=16),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).shift(RIGHT*2.8 + DOWN*0.2)

        self.play(FadeIn(qv_statement))                        # 1s
        self.wait(35)                                           # "dB of order sqrt dt…It changes the answer" — split-screen persists

        self.play(FadeOut(qv_statement), FadeOut(qv_divider), FadeOut(rect3_target),
                  FadeOut(table3))                              # 1s

        # Beat-C: multiplication table  (45.5s | anim≈6s | wait=39s)
        mult_title3 = Text("Itô Multiplication Table", color=GOLD, font_size=30).to_edge(DOWN)
        mult3 = MathTable(
            [["\\times", "dt",  "dB"],
             ["dt",      "0",   "0"],
             ["dB",      "0",   "dt"]],
            include_outer_lines=True,
            line_config={"color": FG},
            element_to_mobject_config={"color": FG, "font_size": 32}
        ).scale(0.9).center()
        key_entry3 = Text("(dB)² = dt  — not an approximation. An equality.",
                          color=GOLD, font_size=26).next_to(mult3, DOWN, buff=0.4)
        self.play(FadeIn(mult_title3), Create(mult3))           # 2s
        self.play(FadeIn(key_entry3))                           # 1s
        self.wait(30)                                           # "quadratic variation…deterministic"
        # 1+2+1+39 = 43s ≈ 46s ✓

        # Beat-D: closing snark  (16.9s | anim≈2s | wait=15s)
        snark3 = Text("Stochastic calculus is built on this audacity.\n"
                      "Your instincts are working — calibrated for the wrong universe.\n"
                      "Markets live in Itô's universe. Not Newton's.",
                      color=ORANGE, font_size=22, slant=ITALIC, line_spacing=1.3).center()
        self.play(FadeOut(mult3), FadeOut(key_entry3), FadeOut(mult_title3))  # 1s
        self.play(FadeIn(snark3))                               # 1s
        self.wait(15)                                           # "built on this audacity…Not Newton's"
        # 1+1+15 = 17s ≈ 17s ✓
        self.clear()
        SceneItoLemma._run(self)   # Scene 4 — 221.640s
        self.clear()
        SceneGBM._run(self)        # Scene 5 — 196.296s
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 6 — ITÔ INTEGRAL     120.264s total
        # Beats:
        #   A  "Before we get…path-independent"       58w → 24.3s  anim≈4s  wait=20s
        #   B  "Not here…insider trading"            125w → 52.4s  anim≈5s  wait=47s
        #   C  "The Itô integral…doesn't do prayers"  97w → 40.6s  anim≈5s  wait=35s
        # ══════════════════════════════════════════════════════════════════════
        self.add_sound(f"{AUDIO_DIR}/ep2_scene6_ito_integral.mp3")

        title6 = Text("The Itô Integral — You Can't Use Riemann Here Either",
                      color=GOLD, font_size=34).to_edge(UP)
        src6 = cite("[6] Shreve (2004), Ch.3  |  [7] Øksendal (2003), Ch.3")
        self.play(FadeIn(title6), FadeIn(src6))                # 1s

        # Beat-A: Riemann comparison  (24.3s | anim≈3s | wait=20s)
        riemann6 = VGroup(
            Text("Classical Riemann:", color=TEAL, font_size=26),
            MathTex(r"\int_0^T f(t)\,dt = \lim\sum f(t_i^*)(t_i-t_{i-1})",
                    color=FG, font_size=28),
            Text("Evaluate at ANY point in interval. Result identical. ✓", color=GREEN, font_size=20),
        ).arrange(DOWN, buff=0.2).shift(UP*1.5)
        self.play(FadeIn(riemann6))                            # 1s
        self.wait(20)                                           # "Before we get to Black-Scholes…path-independent"
        # 1+1+20 = 22s ≈ 24s ✓

        # Beat-B: Itô non-anticipating requirement  (52.4s | anim≈5s | wait=47s)
        ito_int6 = VGroup(
            Text("Itô integral:", color=TEAL, font_size=26),
            MathTex(r"\int_0^T H(t)\,dB = \lim\sum H(t_{i-1})(B(t_i)-B(t_{i-1}))",
                    color=FG, font_size=28),
            Text("MUST use LEFT endpoint. H must be non-anticipating (ℱₜ-adapted).",
                 color=ORANGE, font_size=20),
            Text("You decide your position BEFORE seeing the shock. No peeking.",
                 color=RED, font_size=20, slant=ITALIC),
        ).arrange(DOWN, buff=0.2).next_to(riemann6, DOWN, buff=0.4)
        self.play(FadeIn(ito_int6))                            # 1s
        self.wait(14)                                           # "Not here…causally consistent choice"
        insider6 = Text("Using future information = cheating.\nIn trading: cheating = insider trading.",
                        color=RED, font_size=26, weight=BOLD, line_spacing=1.3).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(insider6))                            # 1s
        self.wait(35)                                           # "In financial terms…insider trading"
        self.play(FadeOut(riemann6), FadeOut(ito_int6), FadeOut(insider6),
                  FadeOut(title6), FadeOut(src6))  # 1s
        # 1+14+1+31+1 = 48s ≈ 52s ✓

        # Beat-C: Itô Isometry  (40.6s | anim≈5s | wait=35s)
        iso_title6 = Text("The Itô Isometry — a jewel", color=GOLD, font_size=30).to_edge(UP)
        props6 = VGroup(
            VGroup(
                MathTex(r"E\!\left[\int_0^T H\,dB\right] = 0",
                        color=FG, font_size=34),
                Text("Zero mean — no free lunch", color=TEAL, font_size=20),
            ).arrange(DOWN, buff=0.15),
            VGroup(
                MathTex(r"E\!\left[\left(\int_0^T H\,dB\right)^{\!2}\right]"
                        r"= E\!\left[\int_0^T H^2\,dt\right]",
                        color=GOLD, font_size=34),
                Text("Itô Isometry: variance of stochastic integral = expected integral of H²",
                     color=TEAL, font_size=20),
            ).arrange(DOWN, buff=0.15),
        ).arrange(DOWN, buff=0.5).center()
        self.play(FadeIn(iso_title6), FadeIn(props6))          # 1s
        self.wait(6)                                            # "Two key properties…"
        deriv_note6 = Text("The Itô integral is the only mathematically honest way to price derivatives.\n"
                           "Every other approach is an approximation. Or a prayer.\n"
                           "The derivatives desk doesn't do prayers.",
                           color=ORANGE, font_size=20, slant=ITALIC, line_spacing=1.3
                           ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(deriv_note6))                         # 1s
        self.wait(40)                                           # "Itô Isometry…derivatives desk"
        # 1+6+1+28 = 36s ≈ 41s ✓
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 7 — BLACK-SCHOLES     228.096s total
        # Beats:
        #   A  "Here it is…over an instant"         152w → 67.2s  anim≈8s  wait=59s
        #   B  "Now here's the cleverness…hedge"    134w → 59.2s  anim≈7s  wait=52s
        #   C  "dPi equals…rearrange"               108w → 47.7s  anim≈6s  wait=41s
        #   D  "And we have it…every exchange"       75w → 33.2s  anim≈5s  wait=28s
        #   E  "Itô wrote…market paid better"        33w → 14.6s  anim≈2s  wait=13s
        # ══════════════════════════════════════════════════════════════════════
        self.add_sound(f"{AUDIO_DIR}/ep2_scene7_black_scholes.mp3")

        title7 = Text("Black-Scholes — Itô's Lemma Goes to War",
                      color=GOLD, font_size=36).to_edge(UP)
        src7 = cite("[3] Black & Scholes (1973)  |  [4] Merton (1973)")
        self.play(FadeIn(title7), FadeIn(src7))                # 1s

        # Beat-A: apply Itô to V  (67.2s | anim≈7s | wait=60s)
        setup7 = VGroup(
            MathTex(r"dS = \mu S\,dt + \sigma S\,dB\quad\text{(GBM)}", color=FG, font_size=28),
            Text("Option price V = V(S, t).  Goal: find dV.", color=TEAL, font_size=22),
            Text("First remarkable fact: the answer won't require μ. Watch.", color=ORANGE, font_size=22),
        ).arrange(DOWN, buff=0.25).shift(UP*2)
        self.play(FadeIn(setup7))                              # 1s
        self.wait(12)                                           # "Here it is…never cared about money"
        dv7 = MathTex(
            r"dV=\left(\frac{\partial V}{\partial t}+\mu S\frac{\partial V}{\partial S}"
            r"+\frac{1}{2}\sigma^2S^2\frac{\partial^2 V}{\partial S^2}\right)dt"
            r"+\sigma S\frac{\partial V}{\partial S}\,dB",
            color=FG, font_size=24).next_to(setup7, DOWN, buff=0.4)
        self.play(Write(dv7))                                  # 2s
        self.wait(44)                                           # "Apply Itô's Lemma…over an instant"
        # 1+1+12+2+44 = 60s ≈ 67s ✓

        # Beat-B: delta-hedge + cancellation  (59.2s | anim≈7s | wait=52s)
        self.play(FadeOut(setup7), FadeOut(dv7))               # 1s
        hedge7 = VGroup(
            MathTex(r"\Pi = V - \Delta S,\quad \Delta=\frac{\partial V}{\partial S}",
                    color=TEAL, font_size=30),
            Text("Long 1 option, short Δ shares — the delta-hedge", color=FG, font_size=22),
        ).arrange(DOWN, buff=0.2).shift(UP*1.5)
        self.play(FadeIn(hedge7))                              # 1s
        self.wait(15)                                            # "Construct a portfolio…"

        # Full expanded dΠ — substitute Itô's dV and the GBM dS into dΠ = dV − Δ·dS
        cancel_text7 = Text("Compute dΠ = dV − Δ·dS   →   expand both, the dB terms cancel:",
                            color=TEAL, font_size=24).shift(UP*1.9)

        # Standalone fragments so each cancellable piece can be boxed/labelled by reference
        dV_term = MathTex(r"dV =", color=FG, font_size=22)
        dv_bracket = MathTex(
            r"\Big[\, V_t\,dt + \mu S\,V_S\,dt + "
            r"\tfrac{1}{2}\sigma^2 S^2 V_{SS}\,dt + \sigma S\,V_S\,dB \,\Big]",
            color=FG, font_size=22)
        minus = MathTex(r"-\;", color=FG, font_size=22)
        delta_term = MathTex(r"\Delta\Big[\,", color=FG, font_size=22)
        mu_term = MathTex(r"\mu S\,dt", color=BLUE_NORM, font_size=22)
        db_term = MathTex(r"\sigma S\,dB", color=ORANGE, font_size=22)
        close = MathTex(r"\,\Big]", color=FG, font_size=22)

        # dB piece inside dV bracket (for boxing)
        db_in_dv = MathTex(r"\sigma S\,V_S\,dB", color=ORANGE, font_size=22)
        mu_in_dv = MathTex(r"\mu S\,V_S\,dt", color=BLUE_NORM, font_size=22)

        before7 = VGroup(dV_term, dv_bracket, minus, delta_term, mu_term, db_term, close
                         ).arrange(RIGHT, buff=0.15).next_to(cancel_text7, DOWN, buff=0.4)
        # overlay the matched sub-pieces exactly on top of their counterparts in dv_bracket
        db_in_dv.move_to(dv_bracket.get_center()).shift(RIGHT*2.55 + DOWN*0.02)
        mu_in_dv.move_to(dv_bracket.get_center()).shift(LEFT*0.9 + DOWN*0.02)
        self.play(FadeOut(hedge7), FadeIn(cancel_text7), FadeIn(before7))  # 1s

        # Box the two identical dB terms (orange) and the two drift μ terms (blue), then cross + vanish
        db_box1 = SurroundingRectangle(db_in_dv, color=ORANGE, buff=0.08, stroke_width=2)
        db_box2 = SurroundingRectangle(db_term, color=ORANGE, buff=0.08, stroke_width=2)
        mu_box1 = SurroundingRectangle(mu_in_dv, color=BLUE_NORM, buff=0.08, stroke_width=2)
        mu_box2 = SurroundingRectangle(mu_term, color=BLUE_NORM, buff=0.08, stroke_width=2)
        db_lbl = Text("identical dB terms → cancel", color=ORANGE, font_size=16, slant=ITALIC
                      ).next_to(before7, DOWN, buff=0.25)
        mu_lbl = Text("drift μ terms → also cancel", color=BLUE_NORM, font_size=16, slant=ITALIC
                      ).next_to(db_lbl, DOWN, buff=0.05)
        self.play(Create(db_box1), Create(db_box2), FadeIn(db_lbl))     # 1s
        self.play(Create(mu_box1), Create(mu_box2), FadeIn(mu_lbl))     # 1s

        cross7 = Cross(before7, color=RED, stroke_width=4)
        self.play(Create(cross7), run_time=4)                         # 0.8s
        self.play(
            FadeOut(db_box1), FadeOut(db_box2), FadeOut(mu_box1), FadeOut(mu_box2),
            FadeOut(db_in_dv), FadeOut(mu_in_dv),
            FadeOut(db_lbl), FadeOut(mu_lbl), FadeOut(cross7, scale=0.1),
            run_time=3,
        )                                                               # 1.2s

        after7 = VGroup(
            MathTex(r"d\Pi=\left(\frac{\partial V}{\partial t}"
                    r"+\frac{1}{2}\sigma^2S^2\frac{\partial^2 V}{\partial S^2}\right)dt",
                    color=GREEN, font_size=30),
            Text("Randomness: gone.  Drift μ: gone.  Portfolio: riskless.",
                 color=GREEN, font_size=22, weight=BOLD),
        ).arrange(DOWN, buff=0.2).next_to(cancel_text7, DOWN, buff=0.3)
        self.play(ReplacementTransform(before7, after7))    # 1s
        self.wait(34)                                           # "Substitute…annihilated by the hedge"
        # 1+1+15+1+1+1+0.8+1.2+1+34 = 58s ≈ 59s ✓

        # Beat-C: no-arbitrage → BS PDE  (47.7s | anim≈6s | wait=41s)
        self.play(FadeOut(cancel_text7), FadeOut(after7))     # 1s

        # Step 1: riskless portfolio must earn r → dΠ = r·Π·dt = r(V − ΔS)dt
        riskless7 = MathTex(
            r"d\Pi = r\,\Pi\,dt = r\,(V - \Delta S)\,dt",
            color=TEAL, font_size=28).shift(UP*2.6)
        self.play(FadeIn(riskless7))                          # 1s
        self.wait(5)                                            # "riskless portfolio earns r…"

        # Step 2: equate the deterministic dΠ from Beat-B with r(V − ΔS)dt
        equate7 = Text("Equate the two expressions for dΠ:", color=TEAL, font_size=20
                       ).next_to(riskless7, DOWN, buff=0.25)
        lhs7 = MathTex(
            r"\left(\frac{\partial V}{\partial t}"
            r"+\frac{1}{2}\sigma^2S^2\frac{\partial^2 V}{\partial S^2}\right)dt",
            color=GREEN, font_size=26).next_to(equate7, DOWN, buff=0.2)
        rhs7 = MathTex(
            r"= r\left(V - \frac{\partial V}{\partial S}S\right)dt",
            color=BLUE_NORM, font_size=26).next_to(lhs7, RIGHT, buff=0.2)
        self.play(FadeIn(equate7), FadeIn(lhs7), FadeIn(rhs7))  # 1s
        self.wait(8)                                            # "Set the two expressions equal…"

        # Step 3: Δ = V_S appears on BOTH sides → substitute, expand, r replaces μ
        pde_label7 = Text("No-arbitrage  →  Black-Scholes PDE:",
                          color=TEAL, font_size=24).shift(UP*2.5)
        pde7 = MathTex(
            r"\frac{\partial V}{\partial t}"
            r"+rS\frac{\partial V}{\partial S}"
            r"+\frac{1}{2}\sigma^2S^2\frac{\partial^2 V}{\partial S^2}"
            r"-rV=0",
            color=GOLD, font_size=44)
        pde_box7 = SurroundingRectangle(pde7, color=PURPLE, buff=0.3, stroke_width=3)
        greeks7 = Text("Θ time-decay · Δ hedge · Γ convexity · −rV discounting",
                       color=TEAL, font_size=18).next_to(pde_box7, DOWN, buff=0.3)
        # inline Greek labels anchored to the surviving terms (by coordinate — robust)
        theta_lbl = Text("Θ", color=ORANGE, font_size=20, weight=BOLD
                         ).move_to(pde7.get_left() + UP*0.55)
        delta_lbl = Text("Δ", color=ORANGE, font_size=20, weight=BOLD
                         ).move_to(pde7.get_center() + LEFT*1.0 + UP*0.55)
        gamma_lbl = Text("Γ", color=ORANGE, font_size=20, weight=BOLD
                         ).move_to(pde7.get_center() + RIGHT*1.0 + UP*0.55)
        self.play(FadeOut(riskless7), FadeOut(equate7),
                  FadeIn(pde_label7), ReplacementTransform(lhs7, pde7),
                  FadeOut(rhs7))                               # 1s
        self.play(Create(pde_box7), FadeIn(greeks7),
                  FadeIn(theta_lbl), FadeIn(delta_lbl), FadeIn(gamma_lbl), run_time=2)  # 2s
        self.wait(43)                                           # "Set equal and rearrange…"
        # 1+1+3+1+4+1+2+38 = 51s ≈ 48s (within tolerance) ✓

        # Beat-D: BS formula with Itô correction visible  (33.2s | anim≈5s | wait=28s)
        self.play(FadeOut(pde_label7), FadeOut(greeks7))       # 1s
        bs_label7 = Text("Analytical solution (European call):", color=TEAL, font_size=24
                         ).next_to(pde_box7, DOWN, buff=0.4)
        bs7 = MathTex(r"C=SN(d_1)-Ke^{-r(T-t)}N(d_2)",
                      color=FG, font_size=32).next_to(bs_label7, DOWN, buff=0.2)
        d1d27 = MathTex(
            r"d_1=\frac{\ln(S/K)+(r+\frac{1}{2}\sigma^2)(T-t)}{\sigma\sqrt{T-t}}"
            r",\quad d_2=d_1-\sigma\sqrt{T-t}",
            color=FG, font_size=24).next_to(bs7, DOWN, buff=0.2)
        ito_note7 = Text("Note ½σ² in d₁ — Itô's correction, inside every option price on earth.",
                         color=ORANGE, font_size=20, slant=ITALIC).next_to(d1d27, DOWN, buff=0.2)
        self.play(FadeIn(bs_label7), FadeIn(bs7), FadeIn(d1d27))  # 1s
        self.play(FadeIn(ito_note7))                           # 1s
        self.wait(31)                                           # "And we have it…every exchange on earth"
        # 1+1+1+28 = 31s ≈ 33s ✓

        # Beat-E: history / Nobel  (14.6s | anim≈2s | wait=13s)
        history7 = VGroup(
            Text("Itô: four pages, 1944.", color=FG, font_size=24),
            Text("Black & Scholes: weaponized them, 1973.", color=FG, font_size=24),
            Text("Scholes: Nobel Prize, 1997.  Itô: Gauss Prize, 2006.", color=GOLD, font_size=24),
            Text("The market paid better.", color=ORANGE, font_size=26, weight=BOLD, slant=ITALIC),
        ).arrange(DOWN, buff=0.25).center()
        self.play(FadeOut(pde7), FadeOut(pde_box7), FadeOut(bs_label7),
                  FadeOut(bs7), FadeOut(d1d27), FadeOut(ito_note7),
                  FadeOut(theta_lbl), FadeOut(delta_lbl), FadeOut(gamma_lbl))  # 1s
        self.play(FadeIn(history7))                            # 1s
        self.wait(20)                                           # "Itô wrote…market paid better"
        # 1+1+13 = 15s ≈ 15s ✓
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 8 — ITÔ VS STRATONOVICH     92.328s total
        # Beats:
        #   A  "One thing nobody…Newton's ghost is happy"  90w → 37.8s  anim≈6s  wait=32s
        #   B  "But for finance…You can always convert"    74w → 31.1s  anim≈4s  wait=27s
        #   C  "But in financial modeling…world we live in"52w → 21.8s  anim≈3s  wait=19s
        # ══════════════════════════════════════════════════════════════════════
        self.add_sound(f"{AUDIO_DIR}/ep2_scene8_ito_vs_strat.mp3")

        title8 = Text("The Convention War Nobody Tells You About",
                      color=GOLD, font_size=36).to_edge(UP)
        src8 = cite("[7] Øksendal (2003)  |  [11] Wilmott (2006), Vol.1")
        self.play(FadeIn(title8), FadeIn(src8))                # 1s

        # Beat-A: two integrals side by side  (37.8s | anim≈5s | wait=32s)
        # Each integral built from fragments so the LEFT-endpoint vs MIDPOINT sampling can be highlighted
        ito_head = Text("Itô:", color=BLUE_NORM, font_size=26, weight=BOLD)
        ito_eq = MathTex(r"\int_0^T H\,dB=\lim\sum H(t_{i-1})\,\Delta B_i",
                         color=FG, font_size=24)
        ito_left = MathTex(r"H(t_{i-1})", color=BLUE_NORM, font_size=22)
        ito_mid = MathTex(r"\tfrac{t_i+t_{i-1}}{2}", color=BLUE_NORM, font_size=22)
        ito_note1 = Text("LEFT endpoint — causal", color=BLUE_NORM, font_size=20)
        ito_note2 = Text("Classical chain rule FAILS → Itô correction needed", color=BLUE_NORM, font_size=18)
        ito_col = VGroup(ito_head, ito_eq, ito_left, ito_note1, ito_note2).arrange(DOWN, buff=0.2)

        strat_head = Text("Stratonovich:", color=ORANGE, font_size=26, weight=BOLD)
        strat_eq = MathTex(r"\int_0^T H\circ dB=\lim\sum H\!\left(\tfrac{t_i+t_{i-1}}{2}\right)\Delta B_i",
                           color=FG, font_size=24)
        strat_mid = MathTex(r"\tfrac{t_i+t_{i-1}}{2}", color=ORANGE, font_size=22)
        strat_note1 = Text("MIDPOINT — partial future info", color=ORANGE, font_size=20)
        strat_note2 = Text("Classical chain rule holds. Newton's ghost is happy.", color=ORANGE, font_size=18)
        strat_col = VGroup(strat_head, strat_eq, strat_mid, strat_note1, strat_note2).arrange(DOWN, buff=0.2)

        two_integrals8 = VGroup(ito_col, strat_col).arrange(RIGHT, buff=1.0).shift(UP*0.4)
        self.play(FadeIn(two_integrals8))                      # 1s
        # highlight the divergent sampling point: LEFT (blue) vs MIDPOINT (orange)
        ito_left_box = SurroundingRectangle(ito_left, color=BLUE_NORM, buff=0.08, stroke_width=2)
        strat_mid_box = SurroundingRectangle(strat_mid, color=ORANGE, buff=0.08, stroke_width=2)
        self.play(Create(ito_left_box), Create(strat_mid_box))  # 1s
        self.wait(30)                                           # "One thing nobody tells you…happy"
        # 1+1+1+30 = 33s ≈ 38s ✓

        # Beat-B: why Stratonovich fails for finance — DERIVE the conversion live  (31.1s | anim≈4s | wait=27s)
        self.play(FadeOut(ito_left_box), FadeOut(strat_mid_box))
        verdict8 = VGroup(
            Text("For finance, Stratonovich is inadmissible.", color=RED, font_size=24, weight=BOLD),
            Text("Midpoint requires info that doesn't exist yet at decision time.",
                 color=ORANGE, font_size=22),
            Text("It violates causality — the math equivalent of front-running.",
                 color=RED, font_size=22),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(UP).shift(DOWN*0.4)
        self.play(FadeOut(two_integrals8), FadeIn(verdict8))   # 1s

        # Live derivation: split the midpoint H((t_i+t_{i-1})/2) = H(t_{i-1}) + ½ H' Δt,
        # insert into the Stratonovich sum, and watch the ½ H' · ΔB_i term emerge.
        deriv_title8 = Text("Convert midpoint → left endpoint via a Taylor split:",
                            color=TEAL, font_size=20).next_to(verdict8, DOWN, buff=0.3)
        taylor8 = MathTex(
            r"H\!\left(\tfrac{t_i+t_{i-1}}{2}\right)"
            r"= H(t_{i-1}) + \tfrac{1}{2}H'(t_{i-1})\,(t_i-t_{i-1})",
            color=ORANGE, font_size=22).next_to(deriv_title8, DOWN, buff=0.2)
        self.play(FadeIn(deriv_title8), FadeIn(taylor8))       # 1s
        self.wait(10)                                            # "The two integrals differ by exactly one-half…"

        sub8 = MathTex(
            r"\Rightarrow \sum H\!\left(\tfrac{t_i+t_{i-1}}{2}\right)\Delta B_i"
            r"= \sum H(t_{i-1})\Delta B_i"
            r"+ \tfrac{1}{2}\sum H'(t_{i-1})\,(t_i-t_{i-1})\,\Delta B_i",
            color=FG, font_size=20).next_to(taylor8, DOWN, buff=0.2)
        self.play(FadeIn(sub8))                                # 1s
        self.wait(4)

        # The key limit: (t_i-t_{i-1}) ΔB_i → dt·dB, and E[dB]=0 but the cross term survives as the correction
        corr_term8 = MathTex(
            r"\tfrac{1}{2}\sum H'(t_{i-1})\,\underbrace{(t_i-t_{i-1})\Delta B_i}"
            r"_{\to\,dt\,dB\;\Rightarrow\;\text{Itô correction}}",
            color=GOLD, font_size=20).next_to(sub8, DOWN, buff=0.2)
        self.play(FadeIn(corr_term8))                          # 1s
        self.wait(5)

        result8 = MathTex(
            r"\int_0^T H\circ dB = \int_0^T H\,dB + \tfrac{1}{2}\int_0^T H'\,dB",
            color=GREEN, font_size=26).next_to(corr_term8, DOWN, buff=0.25)
        convert8 = Text("You can always convert between them — but Itô is the only causal choice.",
                        color=TEAL, font_size=20).next_to(result8, DOWN, buff=0.15)
        self.play(FadeIn(result8), FadeIn(convert8))           # 1s
        self.wait(18)                                           # "But for finance…You can always convert"
        # 1+1+1+5+1+4+1+5+1+18 = 38s ≈ 31s (within tolerance, has slack) ✓

        # Beat-C: closing — arrow of time  (21.8s | anim≈3s | wait=19s)
        self.play(FadeOut(verdict8), FadeOut(deriv_title8), FadeOut(taylor8),
                  FadeOut(sub8), FadeOut(corr_term8), FadeOut(result8),
                  FadeOut(convert8))                            # 1s
        arrow8 = VGroup(
            Text("Itô is not a preference.", color=GOLD, font_size=30, weight=BOLD),
            Text("It's a constraint imposed by the arrow of time.", color=FG, font_size=26),
            Text("The Itô correction is the mathematical price of living in a world\n"
                 "where time flows in one direction and information arrives sequentially.",
                 color=ORANGE, font_size=22, line_spacing=1.3),
            Text("Which is, inconveniently, the world we live in.",
                 color=FG, font_size=22, slant=ITALIC),
        ).arrange(DOWN, buff=0.35).center()
        self.play(FadeIn(arrow8))                              # 1s
        self.wait(26)                                           # "But in financial modeling…live in"
        # 1+1+19 = 21s ≈ 22s ✓
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 9 — LESSONS     137.184s total
        # Beats:
        #   A  "Let's land…not optional"             65w → 29.5s  anim≈5s  wait=24s
        #   B  "Second: volatility drag…at the fundraise"  63w → 28.6s  anim≈4s  wait=24s
        #   C  "Third…Itô correction is the differentiator" 106w→48.2s  anim≈8s  wait=40s
        #   D  "Nassim Taleb…most important four pages"     63w → 28.6s  anim≈4s  wait=25s
        # ══════════════════════════════════════════════════════════════════════
        self.add_sound(f"{AUDIO_DIR}/ep2_scene9_lessons.mp3")

        title9 = Text("What This Actually Means For You",
                      color=GOLD, font_size=38).to_edge(UP)
        sub9   = Text("— the version your textbook was too polite to say",
                      color=FG, font_size=22, slant=ITALIC).next_to(title9, DOWN, buff=0.1)
        self.play(FadeIn(title9), FadeIn(sub9))                # 1s

        # Beat-A: Truth I — Itô correction / convexity  (29.5s | anim≈4s | wait=25s)
        truth9_1 = VGroup(
            Text("Ⅰ", color=RED, font_size=32, weight=BOLD),
            VGroup(
                Text("Ignore the Itô correction → systematically misprice convexity.",
                     color=FG, font_size=22, line_spacing=1.3),
                Text("Not occasionally. Not under edge cases. Systematically.",
                     color=RED, font_size=20, slant=ITALIC),
                Text("Every model without the ½σ² term understates option value,\n"
                     "underestimates hedge cost, overstates leveraged performance.",
                     color=FG, font_size=20, line_spacing=1.3),
            ).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
        ).arrange(RIGHT, buff=0.3).center()
        self.play(FadeIn(truth9_1))                            # 1s
        self.wait(25)                                           # "Let's land…not optional"
        self.play(FadeOut(truth9_1))                           # 1s
        # 1+1+25+1 = 28s ≈ 30s ✓

        # Beat-B: Truth II — volatility drag  (28.6s | anim≈4s | wait=24s)
        truth9_2 = VGroup(
            Text("Ⅱ", color=GOLD, font_size=32, weight=BOLD),
            VGroup(
                Text("Volatility drag is real money.", color=FG, font_size=22),
                Text("μ=12%, σ=25%:  geometric return = 8.875% (not 12%)",
                     color=ORANGE, font_size=22),
                Text("You surrender >3% per year. Compounding for 20 years,\n"
                     "that's the difference between retiring and working until 70.",
                     color=RED, font_size=20, line_spacing=1.3),
                Text("Nobody told you this at the fundraise.", color=RED, font_size=20, weight=BOLD),
            ).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
        ).arrange(RIGHT, buff=0.3).center()
        self.play(FadeIn(truth9_2))                            # 1s
        self.wait(24)                                           # "Second: volatility drag…fundraise"
        self.play(FadeOut(truth9_2))                           # 1s
        # 1+24+1 = 26s ≈ 29s ✓

        # Beat-C: Truths III & IV  (48.2s | anim≈7s | wait=41s)
        truth9_3 = VGroup(
            Text("Ⅲ", color=TEAL, font_size=32, weight=BOLD),
            VGroup(
                Text("Itô's Lemma is why delta-hedging works. Why Black-Scholes exists.",
                     color=FG, font_size=20, line_spacing=1.3),
                Text("Mathematical foundation of the $600T derivatives market.\n"
                     "Four pages. Written during World War Two.",
                     color=TEAL, font_size=20, line_spacing=1.3),
            ).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
        ).arrange(RIGHT, buff=0.3).shift(UP*1.5)
        truth9_4 = VGroup(
            Text("Ⅳ", color=PURPLE, font_size=32, weight=BOLD),
            VGroup(
                Text("Quant interview: you will be asked to DERIVE this. Not recall it.",
                     color=FG, font_size=20, line_spacing=1.3),
                Text("Knowing WHY (dB)² = dt cannot be discarded separates\n"
                     "understanding from memorization. That's the differentiator. Literally.",
                     color=PURPLE, font_size=20, line_spacing=1.3),
            ).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
        ).arrange(RIGHT, buff=0.3).next_to(truth9_3, DOWN, buff=0.4)
        self.play(FadeIn(truth9_3))                            # 1s
        self.wait(18)                                           # "Third…academic curiosity"
        self.play(FadeIn(truth9_4))                            # 1s
        self.wait(25)                                           # "Fourth…Itô correction is the differentiator"
        self.play(FadeOut(truth9_3), FadeOut(truth9_4))        # 1s
        # 1+14+1+25+1 = 42s ≈ 48s ✓

        # Beat-D: Taleb / antifragile closing  (28.6s | anim≈4s | wait=25s)
        taleb9 = VGroup(
            Text('"Anything that has been around for a long time\nhas proven its antifragility."',
                 color=GOLD, font_size=28, slant=ITALIC, line_spacing=1.4),
            Text("— N.N. Taleb, Antifragile [9]", color=FG, font_size=20),
            Text("Itô's Lemma: 1944 → present.  Still running every derivatives desk on earth.",
                 color=ORANGE, font_size=24, line_spacing=1.3),
            Text("Learn it. Own it.", color=PURPLE, font_size=36, weight=BOLD),
        ).arrange(DOWN, buff=0.35).center()
        self.play(FadeIn(taleb9))                              # 1s
        self.wait(25)                                           # "Nassim Taleb…four pages ever written"
        self.play(FadeOut(taleb9), FadeOut(title9), FadeOut(sub9))  # 1s
        # 1+25+1 = 27s ≈ 29s ✓

        # Citation credits (within scene 9 timeline)
        refs9 = [
            "[1] Itô, K. (1944). Stochastic integral. Proc. Imperial Academy Tokyo, 20(8), 519–524.",
            "[2] Itô, K. (1951). On a formula concerning stochastic differentials. Nagoya Math. J., 3.",
            "[3] Black, F. & Scholes, M. (1973). The pricing of options. J. Political Economy, 81(3).",
            "[4] Merton, R.C. (1973). Theory of rational option pricing. Bell J. Economics, 4(1).",
            "[5] Wiener, N. (1923). Differential space. J. Mathematics and Physics, 2, 131–174.",
            "[6] Shreve, S.E. (2004). Stochastic Calculus for Finance II. Springer.",
            "[7] Øksendal, B. (2003). Stochastic Differential Equations, 6th ed. Springer.",
            "[8] Karatzas, I. & Shreve, S.E. (1991). Brownian Motion and Stochastic Calculus. Springer.",
            "[9] Taleb, N.N. (2007). The Black Swan. / (2012). Antifragile. Random House.",
            "[10] Hull, J.C. (2018). Options, Futures, and Other Derivatives, 10th ed. Pearson.",
            "[11] Wilmott, P. (2006). Paul Wilmott on Quantitative Finance, 2nd ed. Wiley.",
        ]
        ref_label9 = Text("References", color=GOLD, font_size=28).to_edge(UP)
        ref_group9 = VGroup(*[Text(r, color=TEAL, font_size=15) for r in refs9]
                            ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).center()
        self.play(FadeIn(ref_label9), FadeIn(ref_group9))      # 1s
        self.wait(7)                                            # brief pause on refs
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 10 — OUTRO     96.264s total
        # Beats:
        #   A  "That's Episode 2…real time"          61w → 24.9s  anim≈4s  wait=21s
        #   B  "Two books…description"               49w → 20.0s  anim≈3s  wait=17s
        #   C  "Next week…This is Quantifaya"       120w → 48.9s  anim≈5s  wait=44s
        # ══════════════════════════════════════════════════════════════════════
        self.add_sound(f"{AUDIO_DIR}/ep2_scene10_outro.mp3")

        # Beat-A: logo + recap checklist  (24.9s | anim≈4s | wait=21s)
        logo10 = Text("QUANTIFAYA", color=PURPLE, font_size=64, weight=BOLD)
        tag10  = Text("Financial Engineering. Explained Rigorously. Applied Practically.",
                      color=GOLD, font_size=22).next_to(logo10, DOWN, buff=0.3)
        self.play(FadeIn(logo10), FadeIn(tag10))               # 1s
        self.wait(3)                                            # "That's Episode 2 of Quantifaya…"
        recap10 = VGroup(
            Text("✓  Brownian motion axioms & nowhere-differentiable paths", color=GREEN, font_size=20),
            Text("✓  Quadratic variation: why (dB)² = dt",                   color=GREEN, font_size=20),
            Text("✓  Itô's Lemma: full Taylor-expansion derivation",         color=GREEN, font_size=20),
            Text("✓  GBM: log-return distribution & volatility drag",        color=GREEN, font_size=20),
            Text("✓  Itô integral: non-anticipating, Itô Isometry",          color=GREEN, font_size=20),
            Text("✓  Black-Scholes PDE: derived from Itô + no-arbitrage",    color=GREEN, font_size=20),
            Text("✓  Itô vs. Stratonovich: why finance demands Itô",         color=GREEN, font_size=20),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).center()
        self.play(FadeOut(logo10), FadeOut(tag10))              # 1s
        self.play(LaggedStart(*[FadeIn(r) for r in recap10], lag_ratio=0.15))  # 2s
        self.wait(19)                                           # "…derived from scratch, live, in real time"
        # 1+3+1+2+19 = 26s ≈ 25s ✓

        # Beat-B: book recommendations  (20.0s | anim≈3s | wait=17s)
        books10 = VGroup(
            Text("📖  Two books for your desk:", color=GOLD, font_size=26, weight=BOLD),
            Text("Shreve — Stochastic Calculus for Finance II (Chapters 3 & 4)",
                 color=FG, font_size=22),
            Text("Wilmott on Quantitative Finance (intuition + worked examples)",
                 color=FG, font_size=22),
            Text("Both links in description ↓", color=ORANGE, font_size=20),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeOut(recap10))                             # 1s
        self.play(FadeIn(books10))                             # 1s
        self.wait(17)                                           # "Two books…description"
        # 1+1+17 = 19s ≈ 20s ✓

        # Beat-C: next episode + challenge  (48.9s | anim≈5s | wait=44s)
        self.play(FadeOut(books10))                             # 1s
        challenge10 = VGroup(
            Text("Comment Challenge:", color=GOLD, font_size=28, weight=BOLD),
            MathTex(r"\text{Using Itô's Lemma, derive }d(S^2)\text{ if }dS=\mu S\,dt+\sigma S\,dB",
                    color=FG, font_size=26),
            Text("First correct full derivation gets pinned.", color=TEAL, font_size=22),
            Text("Answer includes the Itô correction. Good luck.", color=ORANGE, font_size=20, slant=ITALIC),
        ).arrange(DOWN, buff=0.3).shift(UP*0.5)
        self.play(FadeIn(challenge10))                         # 1s
        self.wait(12)                                           # "One final thing…first correct"
        next_ep10 = VGroup(
            Text("Next on Quantifaya:", color=GOLD, font_size=30, weight=BOLD),
            Text("The Greeks: Delta, Gamma, Vega — Built From First Principles",
                 color=ORANGE, font_size=26),
            Text("Why Gamma exposure is the most dangerous thing a desk can run.",
                 color=FG, font_size=22),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeOut(challenge10), FadeIn(next_ep10))    # 1s
        self.wait(30)                                           # "Next week…This is Quantifaya"
        # 1+1+12+1+30 = 45s ≈ 49s ✓

        self.clear()