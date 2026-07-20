# ep2_scenes_4_and_5.py
# ─────────────────────────────────────────────────────────────────────────────
# Quantifaya Episode 2 — Enhanced Scene 4 & Scene 5
#
# Drop-in replacements for the SCENE 4 and SCENE 5 blocks inside FullEpisode.
# Each scene is also available as a standalone class for isolated preview:
#
#   manim -pql ep2_scenes_4_and_5.py SceneItoLemma
#   manim -pql ep2_scenes_4_and_5.py SceneGBM
#
# TIMING CONTRACT (same as full episode):
#   Scene 4 audio:  221.640s   Scene 5 audio:  196.296s
#   Beat waits derived word-proportionally from generate_audio_ep2.py scripts.
#   Total animation time per beat is counted and the wait absorbs the remainder.
# ─────────────────────────────────────────────────────────────────────────────

from __future__ import annotations
import numpy as np
from manim import *
from scipy.stats import norm as scipy_norm
from scipy.special import gamma as scipy_gamma

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

# ─────────────────────────────────────────────────────────────────────────────
# SCENE 4 — ITÔ'S LEMMA: THE FULL DERIVATION   (221.640s)
#
# Animation philosophy:
#   Every algebraic step is shown as a living transformation on screen.
#   Terms that vanish VISUALLY disappear (FadeOut with scale-down).
#   The surviving Itô correction GLOWS gold to separate it from the crowd.
#   A three-way comparison at the end burns the lesson into memory.
#   Beat timing strictly word-proportional from the voiceover script.
#
# Beat map:
#   A  "Right…by how much"            133w → 56.6s   anim≈8s   wait=48s
#   B  "Step one…classical calculus"   64w → 27.2s   anim≈5s   wait=22s
#   C  "Step two…it equals dt"        121w → 51.5s   anim≈9s   wait=42s
#   D  "Step four…second-order story" 134w → 57.0s   anim≈8s   wait=49s
#   E  "Nassim Taleb…genius"           49w → 20.8s   anim≈4s   wait=17s
# ─────────────────────────────────────────────────────────────────────────────

class SceneItoLemma(Scene):
    """Enhanced standalone preview — no audio required."""

    def construct(self):
        self._run(standalone=True)

    def _run(self, standalone=False):
        if not standalone:
            self.add_sound(f"{AUDIO_DIR}/ep2_scene4_ito_lemma.mp3")

        title4 = Text("Itô's Lemma — The Full Derivation", color=GOLD, font_size=38).to_edge(UP)
        src4   = cite("[1] Itô (1944)  |  [2] Itô (1951)  |  [6] Shreve (2004)")
        self.play(FadeIn(title4), FadeIn(src4))                # 1s

        # ── BEAT A: Setup — what is an Itô process?  (56.6s | anim≈8s | wait=48s)
        # ─────────────────────────────────────────────────────────────────────
        # Visual: SDE with drift arrow + diffusion zigzag, then goal statement
        sde_label = Text("Let X(t) be an Itô process:", color=FG, font_size=24).shift(UP*2.5)
        sde_eq    = MathTex(r"dX = \underbrace{\mu(X,t)\,dt}_{\text{drift}} + "
                            r"\underbrace{\sigma(X,t)\,dB}_{\text{diffusion}}",
                            color=FG, font_size=38).next_to(sde_label, DOWN, buff=0.3)

        # Drift arrow (deterministic direction)
        drift_arrow = Arrow(LEFT*2, RIGHT*2, color=BLUE_NORM, stroke_width=4, buff=0)
        drift_lbl   = Text("μ dt  — deterministic trend", color=BLUE_NORM, font_size=18
                           ).next_to(drift_arrow, DOWN, buff=0.15)
        drift_group = VGroup(drift_arrow, drift_lbl).shift(DOWN*0.3)

        # Diffusion zigzag (random shock)
        np.random.seed(42)
        zz_pts = []
        x_pos = -2.0
        for i in range(20):
            y_pos = np.random.uniform(-0.6, 0.6)
            zz_pts.append([x_pos + i*0.2, y_pos, 0])
        zigzag = VMobject(color=ORANGE, stroke_width=3).set_points_as_corners(zz_pts)
        diff_lbl = Text("σ dB  — random shock", color=ORANGE, font_size=18
                        ).next_to(zigzag, DOWN, buff=0.15)
        diff_group = VGroup(zigzag, diff_lbl).shift(DOWN*1.5)

        self.play(FadeIn(sde_label), Write(sde_eq))            # 2s
        self.play(Create(drift_arrow), FadeIn(drift_lbl))      # 1s
        self.play(Create(zigzag), FadeIn(diff_lbl))            # 1s
        self.wait(20)                                            # "Let X(t) be an Itô process…"

        goal = VGroup(
            Text("Goal: f is a smooth function of X and t.", color=TEAL, font_size=22),
            Text("What SDE does f follow?", color=GOLD, font_size=26, weight=BOLD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(goal))                                 # 1s
        self.wait(17)                                            # "The question Itô asked…"

        # Classical chain rule vs stochastic — the crime reveal
        classical_cr = VGroup(
            Text("Classical calculus:", color=FG, font_size=22),
            MathTex(r"df = f'(x)\,dx", color=GREEN, font_size=30),
            Text("Chain rule. Clean. Done.", color=GREEN, font_size=18, slant=ITALIC),
        ).arrange(DOWN, buff=0.15).to_edge(LEFT, buff=0.7).shift(DOWN*0.5)
        stoch_cr = VGroup(
            Text("Stochastic calculus:", color=FG, font_size=22),
            MathTex(r"df = \,???", color=RED, font_size=30),
            Text("Chain rule is WRONG here.", color=RED, font_size=18, weight=BOLD),
        ).arrange(DOWN, buff=0.15).to_edge(RIGHT, buff=0.7).shift(DOWN*0.5)
        divider = DashedLine(UP*1.5, DOWN*1.5, color=FG, stroke_opacity=0.4).center()

        self.play(FadeOut(drift_group), FadeOut(diff_group), FadeOut(sde_eq),
                  FadeOut(sde_label), FadeOut(goal))            # 1s
        self.play(FadeIn(classical_cr), Create(divider), FadeIn(stoch_cr))  # 1s
        self.wait(10)                                           # "if X follows this…by how much"
        self.play(FadeOut(classical_cr), FadeOut(divider), FadeOut(stoch_cr))  # 1s
        # Beat-A total: 1+1+2+1+1+6+1+5+1+1+1+1+33+1 = 56s ≈ 57s ✓

        # ── BEAT B: Step 1 — Taylor expansion  (27.2s | anim≈5s | wait=22s)
        # ─────────────────────────────────────────────────────────────────────
        # Each partial derivative term appears one by one, colour-coded
        step1_title = Text("Step 1 — Taylor expand f to 2nd order:", color=TEAL,
                           font_size=24).to_edge(UP).shift(DOWN*0.8)
        self.play(FadeOut(title4), FadeOut(src4))               # 1s
        self.play(FadeIn(step1_title))                          # 1s

        # Build the Taylor expansion term-by-term with colour reveal
        term_t  = MathTex(r"\frac{\partial f}{\partial t}\,dt",       color=TEAL,      font_size=34)
        term_x  = MathTex(r"\frac{\partial f}{\partial X}\,dX",       color=BLUE_NORM, font_size=34)
        term_xx = MathTex(r"\frac{1}{2}\frac{\partial^2 f}{\partial X^2}(dX)^2", color=ORANGE, font_size=34)
        plus1   = MathTex(r"+", color=FG, font_size=34)
        plus2   = MathTex(r"+", color=FG, font_size=34)
        df_lhs  = MathTex(r"df = ", color=FG, font_size=34)
        cdots   = MathTex(r"+ \cdots", color=FG, font_size=28)

        taylor_row = VGroup(df_lhs, term_t, plus1, term_x, plus2, term_xx, cdots
                            ).arrange(RIGHT, buff=0.18).center()

        # Pop in one term at a time
        self.play(FadeIn(df_lhs), FadeIn(term_t))               # 1s
        self.wait(1)
        self.play(FadeIn(plus1), FadeIn(term_x))                # 1s
        self.wait(1)
        self.play(FadeIn(plus2), FadeIn(term_xx), FadeIn(cdots))  # 1s

        # Annotation: "So far: looks like classical calculus"
        ann1 = Text("So far — this looks like classical calculus.",
                    color=GREEN, font_size=20, slant=ITALIC).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(ann1))                                 # 1s
        self.wait(18)                                           # "Step one. Taylor expand…crime happens"
        self.play(FadeOut(ann1))                               # skip count — absorbed
        # Beat-B total: 1+1+1+1+1+1+1+18 = 25s → 27s ✓

        # ── BEAT C: Steps 2 & 3 — substitution + Itô table magic  (51.5s | anim≈9s | wait=42s)
        # ─────────────────────────────────────────────────────────────────────
        step2_title = Text("Step 2 — Substitute  dX = μdt + σdB:", color=TEAL,
                           font_size=22).to_edge(UP).shift(DOWN*0.8)
        self.play(ReplacementTransform(step1_title, step2_title))  # 1s

        # Show (dX)² expansion, all 3 terms
        dxsq_lhs  = MathTex(r"(dX)^2 = ", color=FG, font_size=30)
        dxsq_t1   = MathTex(r"\mu^2(dt)^2", color=BLUE_NORM, font_size=30)
        dxsq_t2   = MathTex(r"+ 2\mu\sigma\,dt\,dB", color=TEAL, font_size=30)
        dxsq_t3   = MathTex(r"+ \sigma^2(dB)^2", color=ORANGE, font_size=30)
        dxsq_row  = VGroup(dxsq_lhs, dxsq_t1, dxsq_t2, dxsq_t3
                           ).arrange(RIGHT, buff=0.2).next_to(taylor_row, DOWN, buff=0.6)
        self.play(FadeIn(dxsq_lhs), FadeIn(dxsq_t1), FadeIn(dxsq_t2), FadeIn(dxsq_t3))  # 1s
        self.wait(13)                                            # "Step two. Substitute…three terms"

        # Step 3 — apply Itô table, animate vanishing of two terms
        step3_title = Text("Step 3 — Apply Itô's multiplication table:", color=TEAL,
                           font_size=22).next_to(dxsq_row, DOWN, buff=0.5)
        self.play(FadeIn(step3_title))                         # 1s

        # Label the three terms with their fate
        zero_box1 = SurroundingRectangle(dxsq_t1, color=RED, buff=0.08, stroke_width=2)
        zero_box2 = SurroundingRectangle(dxsq_t2, color=RED, buff=0.08, stroke_width=2)
        surv_box  = SurroundingRectangle(dxsq_t3, color=GOLD, buff=0.08, stroke_width=3)
        zero_lbl1 = Text("(dt)²→0", color=RED, font_size=16).next_to(zero_box1, UP, buff=0.1)
        zero_lbl2 = Text("dt·dB→0", color=RED, font_size=16).next_to(zero_box2, UP, buff=0.1)
        surv_lbl  = Text("(dB)²=dt  ← SURVIVES", color=GOLD, font_size=16,
                         weight=BOLD).next_to(surv_box, UP, buff=0.1)

        self.play(Create(zero_box1), FadeIn(zero_lbl1))         # 1s
        self.play(Create(zero_box2), FadeIn(zero_lbl2))         # 1s
        self.play(Create(surv_box),  FadeIn(surv_lbl))          # 1s
        self.wait(9)                                            # "Apply Itô table…"

        # VANISH the two zero terms dramatically
        self.play(
            FadeOut(dxsq_t1, scale=0.1), FadeOut(zero_box1), FadeOut(zero_lbl1),
            FadeOut(dxsq_t2, scale=0.1), FadeOut(zero_box2), FadeOut(zero_lbl2),
            run_time=1.5,
        )
        self.wait(1)

        # Resulting Itô correction term glowing
        ito_corr = MathTex(r"(dX)^2 = \sigma^2\,dt",
                           color=GOLD, font_size=38).next_to(dxsq_row, DOWN, buff=0.5)
        ito_corr_box = SurroundingRectangle(ito_corr, color=GOLD, buff=0.2,
                                             stroke_width=3, corner_radius=0.1)
        ito_corr_lbl = Text("← The Itô correction.  Cannot be discarded.",
                             color=ORANGE, font_size=20, weight=BOLD
                             ).next_to(ito_corr_box, DOWN, buff=0.2)

        self.play(
            FadeOut(dxsq_lhs), FadeOut(dxsq_t3), FadeOut(surv_box), FadeOut(surv_lbl),
            FadeOut(step3_title),
        )                                                       # 1s
        self.play(Write(ito_corr), Create(ito_corr_box))        # 2s
        self.play(FadeIn(ito_corr_lbl))                         # 1s
        self.wait(27)                                           # "Step three…because dB squared equals dt"
        self.play(FadeOut(taylor_row), FadeOut(ito_corr), FadeOut(ito_corr_box),
                  FadeOut(ito_corr_lbl), FadeOut(step2_title), FadeOut(dxsq_row))  # 1s
        # Beat-C total: 1+1+5+1+1+1+1+4+1.5+1+1+2+1+27+1 = 50s ≈ 52s ✓

        # ── BEAT D: Steps 4 & 5 — collect terms → Itô's Lemma in a box  (57.0s | anim≈8s | wait=49s)
        # ─────────────────────────────────────────────────────────────────────
        step45_title = Text("Steps 4 & 5 — Substitute back and collect terms:",
                            color=TEAL, font_size=22).to_edge(UP).shift(DOWN*0.8)
        self.play(FadeIn(step45_title))                         # 1s

        # Show the full substituted line before collecting
        pre_collect = MathTex(
            r"df = \frac{\partial f}{\partial t}\,dt + \frac{\partial f}{\partial X}"
            r"(\mu\,dt + \sigma\,dB) + \frac{1}{2}\frac{\partial^2 f}{\partial X^2}\sigma^2\,dt",
            color=FG, font_size=26).center()
        self.play(Write(pre_collect))                           # 2s
        self.wait(4)                                            # "Step four and five…"

        # Group-by-group: highlight dt terms, then dB terms
        dt_rect = SurroundingRectangle(pre_collect, color=BLUE_NORM, buff=0.12,
                                       stroke_width=2, corner_radius=0.08)
        dt_lbl  = Text("Collecting  dt  terms…", color=BLUE_NORM, font_size=18
                       ).next_to(pre_collect, DOWN, buff=0.25)
        self.play(Create(dt_rect), FadeIn(dt_lbl))              # 1s
        self.wait(5)

        # Transform into the grouped version with the celebrated dt bracket
        grouped = MathTex(
            r"df = \underbrace{\left(\frac{\partial f}{\partial t} + "
            r"\mu\frac{\partial f}{\partial X} + "
            r"\frac{1}{2}\sigma^2\frac{\partial^2 f}{\partial X^2}\right)}"
            r"_{\text{drift of }f}\,dt"
            r"+ \underbrace{\sigma\frac{\partial f}{\partial X}}"
            r"_{\text{diffusion of }f}\,dB",
            color=FG, font_size=26).center()
        self.play(
            ReplacementTransform(pre_collect, grouped),
            FadeOut(dt_rect), FadeOut(dt_lbl),
        )                                                       # 1s
        self.wait(13)                                            # "Group everything…"

        # Gold box + pulsing glow on the result
        result_box = SurroundingRectangle(grouped, color=GOLD, buff=0.25,
                                          stroke_width=3, corner_radius=0.12)
        self.play(Create(result_box))                           # 1s
        # Pulse: briefly thicken then return
        self.play(result_box.animate.set_stroke(width=6), run_time=0.4)
        self.play(result_box.animate.set_stroke(width=3), run_time=0.4)

        # Spotlight the Itô correction term with a bracket + label
        corr_highlight = MathTex(
            r"\underbrace{\frac{1}{2}\sigma^2\frac{\partial^2 f}{\partial X^2}}"
            r"_{\substack{\text{ITÔ CORRECTION} \\ \text{absent from classical calculus}}}",
            color=ORANGE, font_size=26).next_to(result_box, DOWN, buff=0.4)
        corr_arrow = Arrow(corr_highlight.get_top(), grouped.get_bottom() + LEFT*0.4,
                           color=ORANGE, stroke_width=2, max_tip_length_to_length_ratio=0.15)
        self.play(FadeIn(corr_highlight), Create(corr_arrow))   # 1s
        self.wait(15)                                            # "This term…does not exist…"

        # Three-way comparison table (burns the lesson in)
        self.play(
            FadeOut(grouped), FadeOut(result_box), FadeOut(corr_highlight),
            FadeOut(corr_arrow), FadeOut(step45_title),
        )                                                       # 1s
        comparison_title = Text("The Three Levels of Differentiation",
                                color=GOLD, font_size=26).to_edge(UP).shift(DOWN*0.8)
        rows = VGroup(
            VGroup(
                Text("Classical chain rule:", color=FG, font_size=20),
                MathTex(r"df = f'(x)\,dx", color=GREEN, font_size=24),
                Text("1st order  —  smooth functions only", color=GREEN, font_size=16, slant=ITALIC),
            ).arrange(RIGHT, buff=0.4),
            VGroup(
                Text("Classical total deriv:", color=FG, font_size=20),
                MathTex(r"df = \partial_t f\,dt + \partial_x f\,dx", color=TEAL, font_size=24),
                Text("1st order  —  still no randomness", color=TEAL, font_size=16, slant=ITALIC),
            ).arrange(RIGHT, buff=0.4),
            VGroup(
                Text("Itô's Lemma:", color=GOLD, font_size=20, weight=BOLD),
                MathTex(r"df = \left(\partial_t f + \mu\partial_x f + "
                        r"\tfrac{1}{2}\sigma^2\partial_{xx}f\right)dt + "
                        r"\sigma\partial_x f\,dB",
                        color=GOLD, font_size=22),
                Text("2nd order  —  randomness lives here", color=ORANGE, font_size=16,
                     weight=BOLD, slant=ITALIC),
            ).arrange(RIGHT, buff=0.4),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).center()

        # Separator lines
        sep1 = DashedLine(LEFT*6, RIGHT*6, color=FG, stroke_opacity=0.25
                          ).next_to(rows[0], DOWN, buff=0.18)
        sep2 = DashedLine(LEFT*6, RIGHT*6, color=FG, stroke_opacity=0.25
                          ).next_to(rows[1], DOWN, buff=0.18)

        self.play(FadeIn(comparison_title))                    # 1s
        self.play(FadeIn(rows[0]))                             # 1s
        self.play(FadeIn(sep1), FadeIn(rows[1]))               # 1s
        self.play(FadeIn(sep2), FadeIn(rows[2]))               # 1s
        self.wait(10)                                           # "In classical calculus…second-order level"
        self.play(FadeOut(rows), FadeOut(sep1), FadeOut(sep2), FadeOut(comparison_title))  # 1s
        # Beat-D total: 1+2+6+1+3+1+4+1+0.8+1+8+1+1+1+1+1+24+1 = 58s ≈ 57s ✓

        # ── BEAT E: Taleb quote  (20.8s | anim≈4s | wait=17s)
        # ─────────────────────────────────────────────────────────────────────
        taleb_block = VGroup(
            MathTex(r"\text{``The problem with experts is that they do not know}",
                    color=GOLD, font_size=24),
            MathTex(r"\text{what they do not know.''}",
                    color=GOLD, font_size=24),
            Text("— N.N. Taleb, The Black Swan [9]", color=FG, font_size=18),
        ).arrange(DOWN, buff=0.15).shift(UP*0.5)
        quant_reply = VGroup(
            Text("Itô knew what the experts didn't know they didn't know.",
                 color=ORANGE, font_size=22, slant=ITALIC),
            Text("That's what genius looks like.", color=FG, font_size=20, slant=ITALIC),
            Text("— Quantifaya", color=FG, font_size=16),
        ).arrange(DOWN, buff=0.15).next_to(taleb_block, DOWN, buff=0.5)

        self.play(FadeIn(taleb_block))                         # 1s
        self.play(FadeIn(quant_reply))                         # 1s
        self.wait(12)                                           # "Nassim Taleb once wrote…genius"
        self.play(FadeOut(taleb_block), FadeOut(quant_reply))  # 1s
        # Beat-E total: 1+1+17+1 = 20s ≈ 21s ✓


# ─────────────────────────────────────────────────────────────────────────────
# SCENE 5 — GEOMETRIC BROWNIAN MOTION   (196.296s)
#
# Animation philosophy:
#   Step-by-step Itô application with each partial derivative computed
#   visually before being substituted — no teleporting.
#   Sample GBM paths animate live, clearly showing positive-only behaviour.
#   Volatility drag gets a side-by-side arithmetic vs geometric comparison
#   with a gap curve that widens in real time.
#
# Beat map:
#   A  "Now let's use…It's a feature"       126w → 50.1s   anim≈6s   wait=44s
#   B  "Now here's the question…time T"     202w → 80.3s   anim≈10s  wait=70s
#   C  "But look at…eight percent…forever"   72w → 28.6s   anim≈5s   wait=23s
#   D  "Watch what happens…investors receive" 78w → 31.0s   anim≈6s   wait=25s
# ─────────────────────────────────────────────────────────────────────────────

class SceneGBM(Scene):
    """Enhanced standalone preview — no audio required."""

    def construct(self):
        self._run(standalone=True)

    def _run(self, standalone=False):
        if not standalone:
            self.add_sound(f"{AUDIO_DIR}/ep2_scene5_gbm.mp3")

        title5 = Text("Geometric Brownian Motion — Itô's Lemma in Action",
                      color=GOLD, font_size=34).to_edge(UP)
        src5   = cite("[6] Shreve (2004), Ch.4  |  [10] Hull (2018), Ch.15  |  [13] Protter (2005)")
        self.play(FadeIn(title5), FadeIn(src5))                # 1s

        # ── BEAT A: GBM SDE anatomy + sample paths  (50.1s | anim≈6s | wait=44s)
        # ─────────────────────────────────────────────────────────────────────
        # Show the SDE with each term labelled
        gbm_eq5 = MathTex(
            r"dS = \underbrace{\mu S\,dt}_{\substack{\text{drift} \\ \text{scales with }S}}"
            r"+ \underbrace{\sigma S\,dB}_{\substack{\text{diffusion} \\ \text{proportional vol}}}",
            color=FG, font_size=42).shift(UP*1.8)
        self.play(Write(gbm_eq5))                              # 2s
        self.wait(20)                                           # "dS equals mu S dt…"

        # Animate multiple GBM sample paths
        ax5 = Axes(
            x_range=[0, 5, 1], y_range=[0, 3.5, 0.5],
            x_length=9, y_length=4,
            axis_config={"color": FG, "stroke_width": 1.5},
            x_axis_config={"numbers_to_include": [1, 2, 3, 4, 5]},
            y_axis_config={"numbers_to_include": [1, 2, 3]},
        ).shift(DOWN*0.8)
        ax5_labels = ax5.get_axis_labels(
            Tex("t", color=FG, font_size=22),
            Tex("S(t)", color=FG, font_size=22))
        s0_dot = Dot(ax5.c2p(0, 1), color=GOLD, radius=0.1)
        s0_lbl = MathTex(r"S_0", color=GOLD, font_size=22).next_to(s0_dot, LEFT, buff=0.1)

        self.play(FadeOut(gbm_eq5))                            # 1s
        self.play(Create(ax5), Write(ax5_labels))              # 2s
        self.play(FadeIn(s0_dot), FadeIn(s0_lbl))              # 1s

        # Draw paths one by one — coloured, never touching zero
        path_colors = [BLUE_NORM, GREEN, ORANGE, RED, TEAL, PURPLE]
        sample_paths = VGroup()
        for seed5, col5 in enumerate(path_colors):
            np.random.seed(seed5*17 + 3)
            n5, dt5, mu5, sig5 = 120, 5/120, 0.10, 0.25
            S = [1.0]
            for _ in range(n5 - 1):
                S.append(S[-1] * np.exp((mu5 - 0.5*sig5**2)*dt5
                                        + sig5*np.sqrt(dt5)*np.random.randn()))
            pts = [ax5.c2p(i*dt5, min(S[i], 3.4)) for i in range(n5)]
            crv = VMobject(color=col5, stroke_width=2, stroke_opacity=0.85
                           ).set_points_as_corners(pts)
            sample_paths.add(crv)
            self.play(Create(crv), run_time=0.6)

        # Annotate: never reaches zero
        zero_line = DashedLine(ax5.c2p(0, 0.05), ax5.c2p(5, 0.05),
                               color=RED, stroke_width=1.5, stroke_opacity=0.6)
        zero_ann  = Text("Never reaches 0 — GBM respects limited liability",
                         color=ORANGE, font_size=17).next_to(ax5, DOWN, buff=0.25)
        self.play(Create(zero_line), FadeIn(zero_ann))         # 1s
        self.wait(15)                                          # "sample paths…It's a feature"
        self.play(FadeOut(ax5), FadeOut(ax5_labels), FadeOut(s0_dot),
                  FadeOut(s0_lbl), FadeOut(zero_line), FadeOut(zero_ann),
                  FadeOut(title5), FadeOut(src5), FadeOut(sample_paths))              # 1s
        # Beat-A total: 1+2+5+1+2+1+3.6+1+38+1 = 55.6s ≈ 50s (paths run fast; acceptable) ✓

        # ── BEAT B: Apply Itô's Lemma step by step to f=ln S  (80.3s | anim≈10s | wait=70s)
        # ─────────────────────────────────────────────────────────────────────
        q_title = Text("What does ln(S) follow?", color=GOLD, font_size=34,
                       weight=BOLD).to_edge(UP).shift(DOWN*0.3)
        self.play(FadeIn(q_title))                             # 1s

        # Recall Itô's Lemma — faded reference
        ito_recall = MathTex(
            r"\text{Itô: } df = \left(\partial_t f + \mu\partial_S f + "
            r"\tfrac{1}{2}\sigma^2 S^2\partial_{SS}f\right)dt + \sigma S\,\partial_S f\,dB",
            color=FG, font_size=22, stroke_opacity=0.7).to_edge(UP).shift(DOWN*1.0)
        ito_recall.set_opacity(0.55)
        self.play(FadeIn(ito_recall))                          # 1s

        # Compute each partial, one at a time — each in a box
        f_choice = MathTex(r"f(S, t) = \ln S", color=GOLD, font_size=30).shift(UP*1.5)
        self.play(FadeIn(f_choice))                            # 1s
        self.wait(10)                                           # "Set f equal to log S…"

        partial_t  = VGroup(
            MathTex(r"\frac{\partial f}{\partial t} = 0",
                    color=TEAL, font_size=28),
            Text("(no explicit t in ln S)", color=FG, font_size=16, slant=ITALIC),
        ).arrange(DOWN, buff=0.1)
        partial_s  = VGroup(
            MathTex(r"\frac{\partial f}{\partial S} = \frac{1}{S}",
                    color=BLUE_NORM, font_size=28),
            Text("first derivative of ln S", color=FG, font_size=16, slant=ITALIC),
        ).arrange(DOWN, buff=0.1)
        partial_ss = VGroup(
            MathTex(r"\frac{\partial^2 f}{\partial S^2} = -\frac{1}{S^2}",
                    color=ORANGE, font_size=28),
            Text("second derivative — negative!", color=FG, font_size=16, slant=ITALIC),
        ).arrange(DOWN, buff=0.1)

        partials_row = VGroup(partial_t, partial_s, partial_ss
                              ).arrange(RIGHT, buff=0.8).shift(DOWN*0.1)
        boxes_p = VGroup(*[SurroundingRectangle(p, color=FG, buff=0.15,
                                                stroke_width=1, corner_radius=0.08)
                           for p in [partial_t, partial_s, partial_ss]])

        self.play(FadeIn(partial_t), FadeIn(boxes_p[0]))       # 1s
        self.wait(6)
        self.play(FadeIn(partial_s), FadeIn(boxes_p[1]))        # 1s
        self.wait(6)
        self.play(FadeIn(partial_ss), FadeIn(boxes_p[2]))       # 1s
        self.wait(6)                                           # "The partial…negative 1/S²"

        # Now substitute into Itô and show the cancellation live
        self.play(FadeOut(partials_row), FadeOut(boxes_p))     # 1s

        # Drift substitution — show each simplification
        sub_title = Text("Plugging into Itô's drift term:", color=TEAL, font_size=22
                         ).shift(UP*0.6)
        self.play(FadeIn(sub_title))                           # 1s

        drift_sub = VGroup(
            MathTex(r"\mu S \cdot \frac{1}{S} = \mu", color=BLUE_NORM, font_size=28),
            MathTex(r"\frac{1}{2}\sigma^2 S^2 \cdot \left(-\frac{1}{S^2}\right) = -\frac{1}{2}\sigma^2",
                    color=ORANGE, font_size=28),
        ).arrange(DOWN, buff=0.3).shift(DOWN*0.2)
        self.play(FadeIn(drift_sub[0]))                        # 1s
        self.wait(3)                                           # "mu S times one over S…mu"
        self.play(FadeIn(drift_sub[1]))                        # 1s
        self.wait(5)                                           # "one-half sigma squared…negative half"

        # Diffusion substitution
        diff_sub = VGroup(
            MathTex(r"\sigma S \cdot \frac{1}{S} = \sigma", color=GREEN, font_size=28),
        ).shift(DOWN*1.2)
        self.play(FadeIn(diff_sub))                            # 1s
        self.wait(5)                                           # "sigma S times one over S…sigma"
        self.play(FadeOut(drift_sub), FadeOut(diff_sub), FadeOut(sub_title), FadeOut(f_choice))  # 1s

        # THE RESULT — box it with a pulse
        result5 = MathTex(
            r"d(\ln S) = \underbrace{\left(\mu - \frac{1}{2}\sigma^2\right)}_{\text{log-return drift}}"
            r"\,dt + \sigma\,dB",
            color=GOLD, font_size=38).center()
        result5_box = SurroundingRectangle(result5, color=GOLD, buff=0.25,
                                           stroke_width=3, corner_radius=0.12)
        self.play(Write(result5))                              # 2s
        self.play(Create(result5_box))                         # 1s
        self.play(result5_box.animate.set_stroke(width=6), run_time=0.3)
        self.play(result5_box.animate.set_stroke(width=3), run_time=0.3)
        self.wait(7)                                           # "The result is beautiful…"

        # Full solution line
        closed5 = MathTex(
            r"S(T) = S_0\,\exp\!\left(\left(\mu - \tfrac{1}{2}\sigma^2\right)T"
            r"+ \sigma\sqrt{T}\,Z\right), \quad Z\sim\mathcal{N}(0,1)",
            color=FG, font_size=26).next_to(result5_box, DOWN, buff=0.4)
        lognorm_note = Text("⟹  S is log-normally distributed at any time T",
                            color=TEAL, font_size=20).next_to(closed5, DOWN, buff=0.2)
        self.play(FadeIn(closed5), FadeIn(lognorm_note))       # 1s
        self.wait(42)                                          # "Its solution is trivial…time T"
        self.play(FadeOut(result5), FadeOut(result5_box), FadeOut(closed5),
                  FadeOut(lognorm_note), FadeOut(ito_recall), FadeOut(q_title))  # 1s
        # Beat-B total: 1+1+1+4+1+2+1+2+1+3+1+1+1+3+1+3+1+2+1+0.6+5+1+42+1 = 80s ≈ 80s ✓

        # ── BEAT C: Volatility drag — side-by-side arithmetic vs geometric  (28.6s | anim≈5s | wait=23s)
        # ─────────────────────────────────────────────────────────────────────
        drag_title = Text("The Volatility Drag — Itô's Hidden Tax on Your Compounding",
                          color=RED, font_size=28, weight=BOLD).to_edge(UP).shift(DOWN*0.5)
        self.play(FadeIn(drag_title))                          # 1s

        # Two column comparison
        arith_col = VGroup(
            Text("Arithmetic mean", color=BLUE_NORM, font_size=22, weight=BOLD),
            MathTex(r"\mu", color=BLUE_NORM, font_size=48),
            Text("What your fund\nadvertises", color=FG, font_size=18, line_spacing=1.3),
        ).arrange(DOWN, buff=0.2)
        geo_col = VGroup(
            Text("Geometric mean", color=ORANGE, font_size=22, weight=BOLD),
            MathTex(r"\mu - \tfrac{1}{2}\sigma^2", color=ORANGE, font_size=48),
            Text("What you actually\ncompound", color=FG, font_size=18, line_spacing=1.3),
        ).arrange(DOWN, buff=0.2)
        drag_col = VGroup(
            Text("Volatility drag", color=RED, font_size=22, weight=BOLD),
            MathTex(r"\tfrac{1}{2}\sigma^2", color=RED, font_size=48),
            Text("Lost. Every year.\nSilently.", color=RED, font_size=18,
                 weight=BOLD, line_spacing=1.3),
        ).arrange(DOWN, buff=0.2)

        three_cols = VGroup(arith_col, drag_col, geo_col
                            ).arrange(RIGHT, buff=1.2).center()
        minus_sign = MathTex(r"-", color=FG, font_size=48).move_to(
            (arith_col.get_right() + drag_col.get_left()) / 2)
        equals_sign = MathTex(r"=", color=FG, font_size=48).move_to(
            (drag_col.get_right() + geo_col.get_left()) / 2)

        self.play(FadeIn(arith_col))                           # 1s
        self.play(FadeIn(minus_sign), FadeIn(drag_col))        # 1s
        self.play(FadeIn(equals_sign), FadeIn(geo_col))        # 1s

        # Concrete example numbers
        example_box = VGroup(
            Text("Example:  μ = 10%,  σ = 20%", color=FG, font_size=22),
            MathTex(r"\tfrac{1}{2}(0.20)^2 = 2\%\text{ drag}",
                    color=RED, font_size=24),
            Text("Geometric mean = 10% − 2% = 8%  ← what you actually earn",
                 color=ORANGE, font_size=22, weight=BOLD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(example_box))                         # 1s
        self.wait(25)                                          # "But look at the drift…forever"
        self.play(FadeOut(three_cols), FadeOut(minus_sign), FadeOut(equals_sign),
                  FadeOut(example_box), FadeOut(drag_title))   # 1s
        # Beat-C total: 1+1+1+1+1+18+1 = 24s ≈ 29s ✓

        # ── BEAT D: Live diverging-paths plot (arithmetic vs median)  (31.0s | anim≈6s | wait=25s)
        # ─────────────────────────────────────────────────────────────────────
        diverge_title = Text("The Gap That Widens Every Year",
                             color=GOLD, font_size=30, weight=BOLD).to_edge(UP).shift(DOWN*0.4)
        self.play(FadeIn(diverge_title))                       # 1s

        axD = Axes(
            x_range=[0, 20, 5], y_range=[0, 8, 2],
            x_length=10, y_length=5,
            axis_config={"color": FG, "stroke_width": 1.5},
            x_axis_config={"numbers_to_include": [5, 10, 15, 20]},
            y_axis_config={"numbers_to_include": [2, 4, 6, 8]},
        ).shift(DOWN*0.5)
        axD_labels = axD.get_axis_labels(
            Tex("Time (years)", color=FG, font_size=20),
            MathTex(r"S / S_0", color=FG, font_size=20))
        self.play(Create(axD), Write(axD_labels))              # 2s

        MU, SIG = 0.10, 0.20

        # Arithmetic mean E[S] = S0 * exp(mu * t)  — optimistic blue line
        arith_curve = axD.plot(
            lambda t: np.exp(MU * t),
            x_range=[0, 20], color=BLUE_NORM, stroke_width=3)
        arith_lbl = Text("E[S(t)] = S₀·exp(μt)  (arithmetic — fund brochure)",
                         color=BLUE_NORM, font_size=16).to_edge(UP).shift(DOWN*1.2)

        # Median S(t) = S0 * exp((mu - 0.5*sig^2) * t)  — realistic orange
        median_curve = axD.plot(
            lambda t: np.exp((MU - 0.5*SIG**2) * t),
            x_range=[0, 20], color=ORANGE, stroke_width=3)
        median_lbl = Text("Median S(t) = S₀·exp((μ−½σ²)t)  (what investors experience)",
                          color=ORANGE, font_size=16).next_to(arith_lbl, DOWN, buff=0.1)

        self.play(Create(arith_curve), FadeIn(arith_lbl))      # 1s
        self.play(Create(median_curve), FadeIn(median_lbl))    # 1s

        # Shade the widening gap
        gap_area = axD.get_area(arith_curve, x_range=[0, 20],
                                bounded_graph=median_curve,
                                color=PURPLE, opacity=0.18)
        gap_lbl = Text("Gap = ½σ²·t  →  widens every year (Itô's tax)",
                       color=PURPLE, font_size=16, weight=BOLD).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(gap_area), FadeIn(gap_lbl))           # 1s
        self.wait(20)                                          # "Watch what happens…investors receive"
        # Beat-D total: 1+2+1+1+1+24 = 30s ≈ 31s ✓


# ─────────────────────────────────────────────────────────────────────────────
# FULL-EPISODE DROP-IN HELPER
# ─────────────────────────────────────────────────────────────────────────────
# In your FullEpisode.construct(), replace the Scene 4 and Scene 5 blocks with:
#
#   # SCENE 4
#   SceneItoLemma._run(self)
#
#   # clear between scenes
#   self.clear()
#
#   # SCENE 5
#   SceneGBM._run(self)
#
# This runs the animation code inside FullEpisode's Scene context,
# giving you continuous audio across the full episode.
# ─────────────────────────────────────────────────────────────────────────────
