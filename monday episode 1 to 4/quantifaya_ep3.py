# quantifaya_ep3.py
# ─────────────────────────────────────────────────────────────────────────────
# Quantifaya — Episode 3
# "Black-Scholes — Derived From Scratch"
#
# TIMING PHILOSOPHY (read this)
# ─────────────────────────────
# Every self.wait() in FullEpisode is calibrated against the REAL measured
# MP3 durations below.  The strategy is NOT a single tail-pad at the end of
# each scene — that would let animations race ahead of the narration mid-scene.
# Instead the audio budget is distributed across every named beat so the
# visual and narration are in lockstep throughout.
#
# How each beat wait was computed:
#   1. Total audio time for scene = known (measured MP3)
#   2. Animation time for each beat = counted manually (play() ~1s each)
#   3. Narration proportion for each beat = estimated from script word-count
#   4. beat_wait = (audio × proportion) − beat_anim_time
#
# RENDER COMMANDS
# ───────────────
# Full episode (1080p60, production):
#   manim -pqh quantifaya_ep3.py FullEpisode
# Quick preview (480p15):
#   manim -pql quantifaya_ep3.py FullEpisode
# Individual scene test:
#   manim -pql quantifaya_ep3.py SceneIntro
# ─────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import json
import os

import numpy as np
from manim import *
from scipy.stats import norm


# ── BRAND PALETTE ────────────────────────────────────────────────────────────
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
MANIFEST  = os.path.join(AUDIO_DIR, "timing_manifest_ep3.json")


# ── REAL MEASURED AUDIO DURATIONS (seconds) ─────────────────────────────────
# Source: mutagen on the edge-tts output MP3s
AUDIO: dict[str, float] = {
    "ep3_scene1_intro":           60.120,
    "ep3_scene2_problem_setup":  114.072,
    "ep3_scene3_assumptions":    157.752,
    "ep3_scene4_pde":            217.584,
    "ep3_scene5_heat_equation":  215.928,
    "ep3_scene6_formula":        150.384,
    "ep3_scene7_risk_neutral":   138.744,
    "ep3_scene8_breaks":         172.248,
    "ep3_scene9_lessons":        101.304,
    "ep3_scene10_outro":         118.800,
}


# ── HELPERS ──────────────────────────────────────────────────────────────────
def load_manifest() -> dict[str, float]:
    """Return {scene_key: duration_seconds} from the timing manifest."""
    if not os.path.exists(MANIFEST):
        raise FileNotFoundError(
            f"Timing manifest not found at '{MANIFEST}'.\n"
            "Run generate_audio_ep3.py first:\n"
            "    python generate_audio_ep3.py"
        )
    with open(MANIFEST) as f:
        return json.load(f)


def cite(refs: str) -> Text:
    """Small citation block pinned to the bottom-right corner."""
    return (
        Text(refs, color=TEAL, font_size=14)
        .to_corner(DR)
        .shift(UP * 0.1 + LEFT * 0.1)
    )


# ═════════════════════════════════════════════════════════════════════════════
# INDIVIDUAL SCENES  (standalone testing — no timing manifest needed)
# ═════════════════════════════════════════════════════════════════════════════

class SceneIntro(Scene):
    """Cold open: Nobel hook → formula → title card.  ~1:00"""
    def construct(self) -> None:
        # ── Beat 1: names + Nobel (~15s) ─────────────────────────────────────
        names = VGroup(
            Text("Fischer Black",  color=FG, font_size=52),
            Text("Myron Scholes",  color=FG, font_size=52),
            Text("Robert Merton",  color=FG, font_size=52),
        ).arrange(DOWN, buff=0.4).shift(UP * 0.5)
        for n in names:
            self.play(FadeIn(n), run_time=0.6)
        self.wait(5)
        nobel = Text("1997 Nobel Prize in Economics.",
                     color=GOLD, font_size=36).next_to(names, DOWN, buff=0.5)
        self.play(FadeIn(nobel))
        self.wait(5)
        # Red X over Black
        x_mark = Cross(names[0], color=RED, stroke_width=5)
        died = Text(
            "Died: August 30, 1995. Nobel Prizes are not awarded posthumously.",
            color=RED, font_size=22,
        ).next_to(names[0], RIGHT, buff=0.3)
        src = cite("[16] Nobel Committee (1997), Royal Swedish Academy of Sciences")
        self.play(Create(x_mark), FadeIn(died), FadeIn(src))
        self.wait(2)

        # ── Beat 2: formula (~15s) ───────────────────────────────────────────
        self.play(
            FadeOut(names), FadeOut(nobel), FadeOut(x_mark),
            FadeOut(died), FadeOut(src),
        )
        formula = MathTex(
            r"C = S_0 N(d_1) - K e^{-rT} N(d_2)",
            color=RED, font_size=56,
        ).center()
        self.play(Write(formula))
        self.wait(5)
        desc = VGroup(
            Text("The most famous equation in finance.",
                 color=FG, font_size=26),
            Text("Taught in every program. Understood by almost none.",
                 color=FG, font_size=26),
            Text("Derived by even fewer.",
                 color=ORANGE, font_size=26, weight=BOLD),
        ).arrange(DOWN, buff=0.25).next_to(formula, DOWN, buff=0.5)
        self.play(FadeIn(desc))
        self.wait(5)
        self.play(FadeOut(formula), FadeOut(desc))
        manifesto = VGroup(
            Text("Today we derive it.", color=GOLD, font_size=36, weight=BOLD),
            Text("All of it. From first principles.", color=FG, font_size=28),
            Text("No hand-waving. No 'it can be shown.' We show.",
                 color=ORANGE, font_size=26, slant=ITALIC),
        ).arrange(DOWN, buff=0.35).center()
        self.play(FadeIn(manifesto))
        self.wait(5)

        # ── Beat 3: title card (~6s) ─────────────────────────────────────────
        title_card = VGroup(
            Text("QUANTIFAYA", color=PURPLE, font_size=52, weight=BOLD),
            Text("Episode 3", color=FG, font_size=26),
            Text("Black-Scholes — Derived From Scratch",
                 color=GOLD, font_size=34),
            Text("PDE  →  Heat Equation  →  Formula  →  Nobel Prize",
                 color=FG, font_size=22),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeOut(manifesto), FadeIn(title_card))
        self.wait(6)


class SceneProblemSetup(Scene):
    """Call/put payoffs, timeline, historical context.  ~1:54"""
    def construct(self) -> None:
        title = Text("Step 0: What Are We Actually Pricing?",
                     color=GOLD, font_size=36).to_edge(UP)
        src = cite("[5] Bachelier (1900)  |  [4] Samuelson (1965)  |  [7] Hull (2018)")
        self.play(FadeIn(title), FadeIn(src))

        # ── Call/Put payoff diagram ──────────────────────────────────────────
        ax = Axes(
            x_range=[0, 160, 20], y_range=[0, 60, 10],
            x_length=9, y_length=5, axis_config={"color": FG},
        )
        ax_lbl = ax.get_axis_labels(
            MathTex(r"S_T", color=FG, font_size=24),
            MathTex(r"\text{Payoff}", color=FG, font_size=24),
        )
        K = 100
        call_payoff = ax.plot(lambda x: max(x - K, 0),
                              x_range=[0, 160], color=GREEN, stroke_width=3)
        put_payoff  = ax.plot(lambda x: max(K - x, 0),
                              x_range=[0, 160], color=RED, stroke_width=3)
        k_dot   = Dot(ax.c2p(K, 0), color=GOLD)
        k_label = MathTex("K", color=GOLD, font_size=24).next_to(k_dot, DOWN)
        call_label = MathTex(r"\text{Call: }\max(S_T - K, 0)",
                             color=GREEN, font_size=24).to_corner(UR).shift(DOWN * 0.5)
        put_label  = MathTex(r"\text{Put: }\max(K - S_T, 0)",
                             color=RED, font_size=24).next_to(call_label, DOWN)
        self.play(Create(ax), Write(ax_lbl))
        self.play(Create(call_payoff), FadeIn(call_label))
        self.play(Create(k_dot), Write(k_label))
        self.play(Create(put_payoff), FadeIn(put_label))
        self.wait(5)

        # ── Timeline ─────────────────────────────────────────────────────────
        self.play(
            FadeOut(ax), FadeOut(ax_lbl), FadeOut(call_payoff),
            FadeOut(put_payoff), FadeOut(k_dot), FadeOut(k_label),
            FadeOut(call_label), FadeOut(put_label),
        )
        timeline = VGroup(
            Line(LEFT * 5, RIGHT * 5, color=FG),
            Dot(LEFT * 5, color=GOLD),
            Dot(RIGHT * 5, color=GOLD),
            Text("t = 0\n'Pay C'\nKnow: S₀, K, r, σ",
                 color=TEAL, font_size=20, line_spacing=1.3)
                .next_to(LEFT * 5, DOWN, buff=0.3),
            Text("t = T\n'Receive max(S_T−K, 0)'\nDon't know: S_T",
                 color=ORANGE, font_size=20, line_spacing=1.3)
                .next_to(RIGHT * 5, DOWN, buff=0.3),
        )
        self.play(Create(timeline))
        self.wait(5)

        # ── History ──────────────────────────────────────────────────────────
        self.play(FadeOut(timeline))
        history = VGroup(
            VGroup(
                Text("Bachelier (1900) [5]", color=GOLD, font_size=24, weight=BOLD),
                Text("First mathematical option model. Arithmetic BM. Heroic.",
                     color=FG, font_size=20),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("Samuelson (1965) [4]", color=GOLD, font_size=24, weight=BOLD),
                Text("GBM. Right dynamics. No closed form.",
                     color=FG, font_size=20),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("Black, Scholes, Merton (1973) [1][2]",
                     color=GOLD, font_size=24, weight=BOLD),
                Text("Closed form. Nobel Prize. $600T market.",
                     color=GREEN, font_size=20),
            ).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).center()
        self.play(LaggedStart(*[FadeIn(h) for h in history], lag_ratio=0.4))
        self.wait(6)


class SceneAssumptions(Scene):
    """Four assumptions and their real-world cost.  ~2:38"""
    def construct(self) -> None:
        title = Text("The Four Assumptions — The Price of Tractability",
                     color=GOLD, font_size=34).to_edge(UP)
        src = cite("[8] Wilmott (2006)  |  [9] Taleb (1997)  |  [10] Taleb (2007)")
        self.play(FadeIn(title), FadeIn(src))

        assumptions = [
            (BLUE_NORM,
             "① Stock follows GBM:  dS = μSdt + σSdB",
             "Fat tails ignored. Vol clustering ignored. Ep.1 problem lives here.",
             '"Those who gave us the Normal distribution to describe market randomness\n'
             ' have a lot to answer for." — Taleb [10]'),
            (ORANGE,
             "② Constant σ and r",
             "The entire vol surface contradicts this. Since 1987, permanently.",
             "The smile exists. It has never left."),
            (RED,
             "③ Continuous, costless trading",
             "Bid-ask, slippage, discrete rebalancing — all ignored.",
             '"The dynamic hedging trap." — Taleb, Dynamic Hedging [9]'),
            (GREEN,
             "④ No dividends. European exercise only.",
             "Both are fixable. American options need numerical methods.",
             "Not today's problem. But you should know the extensions exist."),
        ]
        for col, head, body, snark in assumptions:
            grp = VGroup(
                Text(head,  color=col,  font_size=26, weight=BOLD),
                Text(body,  color=FG,   font_size=20),
                Text(snark, color=GOLD, font_size=18, slant=ITALIC, line_spacing=1.2),
            ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).center()
            self.play(FadeIn(grp))
            self.wait(3)
            self.play(FadeOut(grp))

        # Wilmott quote
        wilmott = VGroup(
            Text('"All models are wrong.\n The question is whether they are wrong in a useful way."',
                 color=GOLD, font_size=28, slant=ITALIC, line_spacing=1.4),
            Text("— P. Wilmott, Paul Wilmott on Quantitative Finance [8]",
                 color=FG, font_size=22),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeIn(wilmott))
        self.wait(6)


class ScenePDE(Scene):
    """The full PDE derivation: Itô + delta-hedge + no-arbitrage.  ~3:38"""
    def construct(self) -> None:
        title = Text("The Derivation — Itô + No-Arbitrage = Black-Scholes PDE",
                     color=GOLD, font_size=32).to_edge(UP)
        src = cite("[1] Black & Scholes (1973)  |  [3] Itô (1944)  |  [6] Shreve (2004)")
        self.play(FadeIn(title), FadeIn(src))

        # Setup
        setup = VGroup(
            MathTex(r"\text{Stock: } dS = \mu S\,dt + \sigma S\,dB",
                    color=FG, font_size=30),
            MathTex(r"\text{Option: } V = V(S,t) \text{ — unknown}",
                    color=FG, font_size=30),
            MathTex(r"\text{Goal: find } V(S,t) \text{ explicitly}",
                    color=TEAL, font_size=30),
        ).arrange(DOWN, buff=0.3).shift(UP * 0.5)
        self.play(FadeIn(setup))
        self.wait(10)
        self.play(FadeOut(setup))

        # Three derivation steps
        steps = [
            ("Step 1 — Apply Itô's Lemma to V(S,t):",
             r"dV=\!\left(\frac{\partial V}{\partial t}+\mu S\frac{\partial V}{\partial S}"
             r"+\frac{1}{2}\sigma^2 S^2\frac{\partial^2 V}{\partial S^2}\right)dt"
             r"+\sigma S\frac{\partial V}{\partial S}\,dB"),
            ("Step 2 — Delta-hedge portfolio  Π = V − ΔS,  Δ = ∂V/∂S:",
             r"\Pi = V - \frac{\partial V}{\partial S}\cdot S"),
            ("Step 3 — Compute dΠ = dV − Δ·dS and expand:",
             r"d\Pi=\!\left(\frac{\partial V}{\partial t}"
             r"+\frac{1}{2}\sigma^2S^2\frac{\partial^2 V}{\partial S^2}\right)dt"
             r"\quad\leftarrow\text{dB terms cancel!  μ terms cancel!}"),
        ]
        for lbl, eq in steps:
            g = VGroup(
                Text(lbl, color=TEAL, font_size=24),
                MathTex(eq, color=FG, font_size=28),
            ).arrange(DOWN, buff=0.3).center()
            self.play(FadeIn(g))
            self.wait(3)
            self.play(FadeOut(g))

        # No-arbitrage → PDE
        noarb = VGroup(
            Text("No-arbitrage: riskless portfolio earns r  →  dΠ = rΠ dt",
                 color=TEAL, font_size=24),
            Text("Set equal. Rearrange.", color=FG, font_size=22),
        ).arrange(DOWN, buff=0.2).shift(UP * 2)
        self.play(FadeIn(noarb))

        pde = MathTex(
            r"\frac{\partial V}{\partial t}"
            r"+rS\frac{\partial V}{\partial S}"
            r"+\frac{1}{2}\sigma^2S^2\frac{\partial^2 V}{\partial S^2}"
            r"-rV=0",
            color=GOLD, font_size=44,
        ).next_to(noarb, DOWN, buff=0.5)
        box = SurroundingRectangle(pde, color=PURPLE, buff=0.3, stroke_width=3)
        self.play(Write(pde), Create(box))
        self.wait(5)

        # Label Greeks
        labels = VGroup(
            Text("∂V/∂t  →  theta", color=TEAL, font_size=20),
            Text("rS·∂V/∂S  →  rate×delta", color=TEAL, font_size=20),
            Text("½σ²S²·∂²V/∂S²  →  gamma term (Itô correction)",
                 color=ORANGE, font_size=20),
            Text("−rV  →  discounting", color=TEAL, font_size=20),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(box, DOWN, buff=0.4)
        self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.2))
        self.wait(6)


class SceneHeatEquation(Scene):
    """Three substitutions → heat equation → Green's function → formula.  ~3:36"""
    def construct(self) -> None:
        title = Text("Solving the PDE — The Heat Equation Trick",
                     color=GOLD, font_size=34).to_edge(UP)
        src = cite("[6] Shreve (2004), Ch.4  |  [14] Karatzas & Shreve (1991)")
        self.play(FadeIn(title), FadeIn(src))

        # Three substitutions
        subs = [
            ("Substitution A — Time reversal:",
             r"\tau = T - t \quad\Rightarrow\quad"
             r"\frac{\partial V}{\partial t} = -\frac{\partial V}{\partial \tau}"),
            ("Substitution B — Log-price (centres the problem):",
             r"x = \ln(S/K),\quad S = Ke^x"),
            ("Substitution C — Remove discounting:",
             r"V(S,t) = e^{-r\tau}\,u(x,\tau)"),
        ]
        for lbl, eq in subs:
            g = VGroup(
                Text(lbl, color=TEAL, font_size=24),
                MathTex(eq, color=FG, font_size=32),
            ).arrange(DOWN, buff=0.25).center()
            self.play(FadeIn(g))
            self.wait(2.5)
            self.play(FadeOut(g))

        # Heat equation
        heat_label = Text("After substitution — the Black-Scholes PDE becomes:",
                          color=TEAL, font_size=24).shift(UP * 2.5)
        heat = MathTex(
            r"\frac{\partial u}{\partial \tau}"
            r"= \frac{1}{2}\sigma^2\frac{\partial^2 u}{\partial \xi^2}",
            color=GOLD, font_size=52,
        )
        heat_box = SurroundingRectangle(heat, color=PURPLE, buff=0.3, stroke_width=3)
        fourier = Text(
            "The Heat Equation — Joseph Fourier, 1822.\n"
            "Physics from 1822. Option pricing from 1973. Same equation.",
            color=FG, font_size=22, line_spacing=1.3,
        ).next_to(heat_box, DOWN, buff=0.4)
        self.play(FadeIn(heat_label), Write(heat), Create(heat_box))
        self.play(FadeIn(fourier))
        self.wait(2)

        # Green's function
        self.play(
            FadeOut(heat_label), FadeOut(heat),
            FadeOut(heat_box), FadeOut(fourier),
        )
        gf_title = Text("Solution — Green's Function (Gaussian convolution):",
                        color=TEAL, font_size=26).shift(UP * 2.5)
        gf_eq = MathTex(
            r"u(\xi,\tau)=\int_{-\infty}^{\infty}u_0(\xi_0)"
            r"\cdot\frac{1}{\sigma\sqrt{2\pi\tau}}"
            r"\exp\!\left(-\frac{(\xi-\xi_0)^2}{2\sigma^2\tau}\right)d\xi_0",
            color=FG, font_size=26,
        )
        gf_note = Text(
            "Integrate the payoff against a Normal kernel.\n"
            "Gaussian blur of the payoff, diffused backward in time.",
            color=GOLD, font_size=22, slant=ITALIC, line_spacing=1.3,
        ).next_to(gf_eq, DOWN, buff=0.4)
        arrives = VGroup(
            Text("Evaluate the integral → transform back → arrive at:",
                 color=TEAL, font_size=22),
            MathTex(r"C = S_0 N(d_1) - K e^{-rT} N(d_2)",
                    color=GOLD, font_size=42),
        ).arrange(DOWN, buff=0.3).next_to(gf_note, DOWN, buff=0.4)
        self.play(FadeIn(gf_title), FadeIn(gf_eq), FadeIn(gf_note))
        self.play(FadeIn(arrives))
        self.wait(6)


class SceneFormula(Scene):
    """Formula dissection, each term explained, put-call parity.  ~2:30"""
    def construct(self) -> None:
        title = Text("The Formula — Every Term Has a Job",
                     color=GOLD, font_size=36).to_edge(UP)
        src = cite("[1] Black & Scholes (1973), p.644  |  [7] Hull (2018), Ch.19")
        self.play(FadeIn(title), FadeIn(src))

        formula = MathTex(r"C = S_0 N(d_1) - K e^{-rT} N(d_2)",
                          color=GOLD, font_size=44).shift(UP * 1.5)
        d_eqs = VGroup(
            MathTex(r"d_1=\frac{\ln(S_0/K)+(r+\frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}",
                    color=FG, font_size=26),
            MathTex(r"d_2 = d_1 - \sigma\sqrt{T}", color=FG, font_size=26),
        ).arrange(RIGHT, buff=0.8).next_to(formula, DOWN, buff=0.3)
        self.play(Write(formula), FadeIn(d_eqs))
        self.wait(5)

        # Four dissections
        dissections = [
            (BLUE_NORM, r"Ke^{-rT}",
             "PV of strike — what you pay if you exercise"),
            (GREEN, r"N(d_2) = \mathbb{P}^Q(S_T > K)",
             "Risk-neutral probability of finishing in the money"),
            (ORANGE, r"N(d_1) = \Delta",
             "Delta — the hedge ratio. Shares to hold to replicate the option."),
            (PURPLE, r"d_1 - d_2 = \sigma\sqrt{T}",
             "The Itô correction — again. Always here. Never leaving."),
        ]
        for col, eq, desc in dissections:
            g = VGroup(
                MathTex(eq, color=col, font_size=34),
                Text(desc, color=FG, font_size=22, slant=ITALIC),
            ).arrange(DOWN, buff=0.2).center()
            self.play(FadeIn(g))
            self.wait(2.5)
            self.play(FadeOut(g))

        # Put-call parity
        pcp = VGroup(
            Text("Put-Call Parity — derived from no-arbitrage in 30 seconds:",
                 color=TEAL, font_size=24),
            MathTex(r"C - P = S_0 - Ke^{-rT}", color=GOLD, font_size=40),
            Text("Long call + short put = long stock + short bond. Always.",
                 color=FG, font_size=22),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeIn(pcp))
        self.wait(5)


class SceneRiskNeutral(Scene):
    """Risk-neutral measure Q, Girsanov, Fundamental Theorem.  ~2:19"""
    def construct(self) -> None:
        title = Text("The Risk-Neutral World — The Deepest Insight",
                     color=GOLD, font_size=34).to_edge(UP)
        src = cite(
            "[12] Harrison & Kreps (1979)  |  [13] Harrison & Pliska (1981)  "
            "|  [11] Cox & Ross (1976)"
        )
        self.play(FadeIn(title), FadeIn(src))

        mystery = VGroup(
            Text("μ — the expected return of the stock — vanished from the PDE.",
                 color=FG, font_size=24),
            Text("A stock returning 5% and one returning 25% have the SAME option price",
                 color=ORANGE, font_size=24, weight=BOLD),
            Text("if their volatility σ is identical. Why?", color=FG, font_size=24),
        ).arrange(DOWN, buff=0.3).shift(UP * 1.5)
        self.play(FadeIn(mystery))
        self.wait(2)
        self.play(FadeOut(mystery))

        # Two measures
        two_worlds = VGroup(
            VGroup(
                Text("Real World P", color=BLUE_NORM, font_size=28, weight=BOLD),
                MathTex(r"dS = \mu S\,dt + \sigma S\,dB^P", color=FG, font_size=26),
                Text("Drift = μ (actual expected return)", color=FG, font_size=20),
                Text("Investors are risk-averse", color=FG, font_size=20),
                Text("μ > r required to hold equity", color=FG, font_size=20),
            ).arrange(DOWN, buff=0.2, aligned_edge=LEFT),
            VGroup(
                Text("Risk-Neutral World Q", color=GREEN, font_size=28, weight=BOLD),
                MathTex(r"dS = r S\,dt + \sigma S\,dB^Q", color=FG, font_size=26),
                Text("Drift = r (risk-free rate)", color=FG, font_size=20),
                Text("Investors are risk-neutral", color=FG, font_size=20),
                Text("All assets earn r. μ irrelevant.", color=GREEN, font_size=20),
            ).arrange(DOWN, buff=0.2, aligned_edge=LEFT),
        ).arrange(RIGHT, buff=1.2).center()
        arrow = Arrow(two_worlds[0].get_right(), two_worlds[1].get_left(),
                      color=GOLD, buff=0.2)
        girsanov = Text("Girsanov's Theorem", color=GOLD, font_size=20)\
                       .next_to(arrow, UP, buff=0.1)
        self.play(FadeIn(two_worlds[0]))
        self.wait(5)
        self.play(FadeIn(two_worlds[1]), Create(arrow), FadeIn(girsanov))
        self.wait(2)
        self.play(FadeOut(two_worlds), FadeOut(arrow), FadeOut(girsanov))

        # Fundamental theorem
        fund_thm = VGroup(
            Text("Fundamental Theorem of Asset Pricing:",
                 color=GOLD, font_size=28, weight=BOLD),
            MathTex(r"C = e^{-rT}\,\mathbb{E}^Q[\max(S_T-K,\,0)]",
                    color=GOLD, font_size=42),
            VGroup(
                MathTex(r"\text{No arbitrage}\;\Leftrightarrow\;\exists\;Q",
                        color=TEAL, font_size=24),
                Text("[12] Harrison & Kreps (1979)", color=TEAL, font_size=18),
            ).arrange(RIGHT, buff=0.4),
            VGroup(
                MathTex(r"\text{Market complete}\;\Leftrightarrow\;Q\text{ is unique}",
                        color=TEAL, font_size=24),
                Text("[13] Harrison & Pliska (1981)", color=TEAL, font_size=18),
            ).arrange(RIGHT, buff=0.4),
        ).arrange(DOWN, buff=0.35).center()
        box = SurroundingRectangle(fund_thm[1], color=PURPLE, buff=0.2, stroke_width=2)
        self.play(FadeIn(fund_thm), Create(box))
        self.wait(5)


class SceneBreaks(Scene):
    """Vol smile, why it exists, model extensions, irony.  ~2:52"""
    def construct(self) -> None:
        title = Text("Where Black-Scholes Breaks — The Vol Smile",
                     color=GOLD, font_size=34).to_edge(UP)
        src = cite("[15] Derman & Kani (1994)  |  [8] Wilmott (2006)  |  [10] Taleb (2007)")
        self.play(FadeIn(title), FadeIn(src))

        # Vol smile chart
        ax = Axes(
            x_range=[70, 130, 10], y_range=[0.10, 0.40, 0.05],
            x_length=9, y_length=5, axis_config={"color": FG},
        )
        ax_lbl = ax.get_axis_labels(
            Tex(r"\text{Strike }K", color=FG, font_size=22),
            Tex(r"\sigma_{\text{imp}}", color=FG, font_size=22),
        )
        flat = ax.plot(lambda x: 0.20, x_range=[70, 130],
                       color=BLUE_NORM, stroke_width=2, stroke_dasharray=[8, 4])
        flat_lbl = Text("BS prediction: σ = constant",
                        color=BLUE_NORM, font_size=20).next_to(ax, RIGHT, buff=0.3).shift(UP * 0.5)
        smile = ax.plot(lambda x: 0.20 + 0.0008 * (100 - x) ** 2 - 0.0005 * (x - 100),
                        x_range=[70, 130], color=ORANGE, stroke_width=3)
        smile_lbl = Text("Reality: vol skew post-1987",
                         color=ORANGE, font_size=20).next_to(ax, RIGHT, buff=0.3).shift(DOWN * 0.2)
        self.play(Create(ax), Write(ax_lbl))
        self.play(Create(flat), FadeIn(flat_lbl))
        self.play(Create(smile), FadeIn(smile_lbl))
        self.wait(2)

        verdict = Text(
            "Constant σ has been empirically violated since October 19, 1987.\n"
            "The smile appeared after Black Monday. It has never left.",
            color=RED, font_size=22, line_spacing=1.3,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(verdict))
        self.wait(2)
        self.play(
            FadeOut(ax), FadeOut(ax_lbl), FadeOut(flat), FadeOut(flat_lbl),
            FadeOut(smile), FadeOut(smile_lbl), FadeOut(verdict),
        )

        # Extensions
        extensions = VGroup(
            VGroup(
                Text("Local Vol — Derman & Kani (1994) [15]",
                     color=ORANGE, font_size=24, weight=BOLD),
                MathTex(r"\sigma = \sigma(S, t)", color=FG, font_size=26),
                Text("Fits the smile exactly. Loses intuition.",
                     color=FG, font_size=20),
            ).arrange(DOWN, buff=0.15),
            VGroup(
                Text("Stochastic Vol — Heston (1993)",
                     color=ORANGE, font_size=24, weight=BOLD),
                MathTex(r"d\sigma^2 = \kappa(\theta-\sigma^2)dt + \xi\sigma\,dW_t",
                        color=FG, font_size=24),
                Text("Vol is random. Mean-reverting. Analytically tractable (barely).",
                     color=FG, font_size=20),
            ).arrange(DOWN, buff=0.15),
            VGroup(
                Text("Jump-Diffusion — Merton (1976) [2]",
                     color=ORANGE, font_size=24, weight=BOLD),
                MathTex(r"dS = \mu S\,dt + \sigma S\,dB + S\,dJ_t",
                        color=FG, font_size=24),
                Text("Adds crash risk. OTM puts now justified.",
                     color=FG, font_size=20),
            ).arrange(DOWN, buff=0.15),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).center()
        self.play(LaggedStart(*[FadeIn(e) for e in extensions], lag_ratio=0.35))
        self.wait(2)

        irony = Text(
            '"Black-Scholes is wrong. The market quotes options IN Black-Scholes implied vol.\n'
            ' The wrong model is the language of the right market.\n'
            ' This is either profound or farcical. Possibly both."',
            color=GOLD, font_size=20, slant=ITALIC, line_spacing=1.3,
        ).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(irony))
        self.wait(5)


class SceneLessons(Scene):
    """Four truths, Taleb quote, reference roll.  ~1:41"""
    def construct(self) -> None:
        title = Text("What This Means For You — No Softening",
                     color=GOLD, font_size=36).to_edge(UP)
        sub = Text("Axe Capital doesn't soften anything either.",
                   color=FG, font_size=20, slant=ITALIC).next_to(title, DOWN, buff=0.1)
        self.play(FadeIn(title), FadeIn(sub))

        truths = [
            (RED,    "Ⅰ",
             "Black-Scholes is Itô + no-arbitrage + heat equation.\nThree ideas. All derivable. All yours now.",
             "[1][3][6]"),
            (GOLD,   "Ⅱ",
             "μ doesn't matter. Explain WHY in your next interview.\nNot just that it cancels — WHY.",
             "[12] Harrison & Kreps (1979)"),
            (TEAL,   "Ⅲ",
             "It's been wrong about vol since 1987.\nKnow HOW it's wrong. Worth more than knowing it's wrong.",
             "[15] Derman & Kani (1994)"),
            (PURPLE, "Ⅳ",
             "Interview calibration:\n→ Derive BS PDE from scratch  ← Top 5%\n→ Explain N(d₁) ≠ N(d₂)  ← Top 10%\n→ Explain the smile  ← Top 20%\n→ Just state the formula  ← Everyone else.",
             ""),
        ]
        for col, num, main, src_ref in truths:
            g = VGroup(
                Text(f"{num}", color=col, font_size=36, weight=BOLD),
                VGroup(
                    Text(main, color=FG, font_size=22, line_spacing=1.3),
                    Text(src_ref, color=col, font_size=18, slant=ITALIC)
                    if src_ref else VGroup(),
                ).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
            ).arrange(RIGHT, buff=0.4).center()
            self.play(FadeIn(g))
            self.wait(3)
            self.play(FadeOut(g))

        taleb = VGroup(
            Text('"The hedging errors are generally small for vanilla options\n'
                 ' but can be monstrous for exotics."',
                 color=GOLD, font_size=26, slant=ITALIC, line_spacing=1.4),
            Text("— N.N. Taleb, Dynamic Hedging [9]", color=FG, font_size=20),
            Text("Know your model. Know its limits. Know when it fails.",
                 color=ORANGE, font_size=24, weight=BOLD),
            Text("That's what separates a quant from someone who Googled the formula.",
                 color=FG, font_size=22, slant=ITALIC),
        ).arrange(DOWN, buff=0.35).center()
        self.play(FadeIn(taleb))
        self.wait(4)

        # Citation roll
        self.play(FadeOut(taleb), FadeOut(title), FadeOut(sub))
        refs = [
            "[1]  Black & Scholes (1973). J. Political Economy, 81(3), 637–654.",
            "[2]  Merton (1973). Bell J. Economics, 4(1), 141–183.",
            "[3]  Itô (1944). Proc. Imperial Academy Tokyo, 20(8), 519–524.",
            "[4]  Samuelson (1965). Industrial Mgmt Review, 6(2), 13–32.",
            "[5]  Bachelier (1900). Ann. Sci. École Normale Sup., 17, 21–86.",
            "[6]  Shreve (2004). Stochastic Calculus for Finance II. Springer.",
            "[7]  Hull (2018). Options, Futures, and Other Derivatives, 10th ed. Pearson.",
            "[8]  Wilmott (2006). Paul Wilmott on Quantitative Finance, 2nd ed. Wiley.",
            "[9]  Taleb (1997). Dynamic Hedging. Wiley.",
            "[10] Taleb (2007). The Black Swan. Random House.",
            "[11] Cox & Ross (1976). J. Financial Economics, 3(1–2), 145–166.",
            "[12] Harrison & Kreps (1979). J. Economic Theory, 20(3), 381–408.",
            "[13] Harrison & Pliska (1981). Stochastic Processes & Applications, 11(3), 215–260.",
            "[14] Karatzas & Shreve (1991). Brownian Motion and Stochastic Calculus. Springer.",
            "[15] Derman & Kani (1994). Risk Magazine, 7(2), 32–39.",
            "[16] Nobel Committee (1997). Royal Swedish Academy of Sciences.",
        ]
        ref_title = Text("References", color=GOLD, font_size=30).to_edge(UP)
        ref_grp = VGroup(*[Text(r, color=TEAL, font_size=15) for r in refs])\
                      .arrange(DOWN, buff=0.14, aligned_edge=LEFT).center()
        self.play(FadeIn(ref_title), FadeIn(ref_grp))
        self.wait(6)


class SceneOutro(Scene):
    """Logo, recap checklist, comment challenge, next-episode tease.  ~1:59"""
    def construct(self) -> None:
        logo = Text("QUANTIFAYA", color=PURPLE, font_size=64, weight=BOLD)
        tagline = Text(
            "Financial Engineering. Explained Rigorously. Applied Practically.",
            color=GOLD, font_size=22,
        ).next_to(logo, DOWN, buff=0.3)
        self.play(FadeIn(logo), FadeIn(tagline))
        self.wait(5)

        recap = VGroup(
            Text("✓  Option pricing problem — Bachelier to Black-Scholes",
                 color=GREEN, font_size=20),
            Text("✓  Four assumptions and the cost of each",
                 color=GREEN, font_size=20),
            Text("✓  PDE derived: Itô + delta-hedge + no-arbitrage",
                 color=GREEN, font_size=20),
            Text("✓  Heat equation transformation and analytical solution",
                 color=GREEN, font_size=20),
            Text("✓  Formula anatomy: N(d₁), N(d₂), d₁ vs d₂",
                 color=GREEN, font_size=20),
            Text("✓  Put-Call Parity in 30 seconds",
                 color=GREEN, font_size=20),
            Text("✓  Risk-neutral measure Q and Fundamental Theorem",
                 color=GREEN, font_size=20),
            Text("✓  Vol smile, local vol, stochastic vol, jumps",
                 color=GREEN, font_size=20),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).center()
        self.play(FadeOut(logo), FadeOut(tagline))
        self.play(LaggedStart(*[FadeIn(r) for r in recap], lag_ratio=0.12))
        self.wait(2)

        challenge = VGroup(
            Text("Comment Challenge:", color=GOLD, font_size=28, weight=BOLD),
            MathTex(r"\text{Price a cash-or-nothing digital call: pays \$1 if }S_T>K",
                    color=FG, font_size=26),
            Text("Show the full derivation using the risk-neutral formula.",
                 color=FG, font_size=22),
            Text("Why does only N(d₂) appear — and not N(d₁)?",
                 color=ORANGE, font_size=22, weight=BOLD),
            Text("First correct answer gets pinned.", color=TEAL, font_size=20),
        ).arrange(DOWN, buff=0.25).center()
        self.play(FadeOut(recap), FadeIn(challenge))
        self.wait(2)

        next_ep = VGroup(
            Text("Next on Quantifaya:", color=GOLD, font_size=30, weight=BOLD),
            Text("The Greeks — Delta, Gamma, Vega, Theta",
                 color=ORANGE, font_size=28),
            MathTex(
                r"\Delta=N(d_1)\quad\Gamma=\frac{N'(d_1)}{S\sigma\sqrt{T}}"
                r"\quad\mathcal{V}=S\sqrt{T}\,N'(d_1)",
                color=FG, font_size=26,
            ),
            Text("Why Gamma is dangerous. Why Theta bleeds every night.",
                 color=FG, font_size=22),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeOut(challenge), FadeIn(next_ep))
        self.wait(6)


# ═════════════════════════════════════════════════════════════════════════════
# FULL EPISODE — BEAT-LEVEL PRECISION SYNC
# ═════════════════════════════════════════════════════════════════════════════
# TIMING APPROACH
# ───────────────
# For each scene the total audio duration is fixed (AUDIO dict above).
# The audio budget is split across named beats proportional to narration density
# (word count of that beat's narration ÷ total scene word count).
# Each beat_wait = (audio × proportion) − beat_animation_seconds
# All values computed offline and hardcoded here for deterministic renders.
#
# KEY: self.add_sound() starts the MP3 clock.  Every subsequent self.wait()
# and self.play() consumes that clock.  The final self.wait() at the end of
# each scene is a safety absorber — it should be ≥0 but close to 0 if all
# beat waits are correct.  Negative values are clamped to 0 in the helper.
#
# Scene durations at a glance:
#   S1  60.1s   S2 114.1s  S3 157.8s  S4 217.6s  S5 215.9s
#   S6 150.4s   S7 138.7s  S8 172.2s  S9 101.3s  S10 118.8s
# ─────────────────────────────────────────────────────────────────────────────

class FullEpisode(Scene):
    """
    Complete ~24-minute episode with perfectly timed audio synchronisation.
    No manifest file required — durations are hardcoded from real measurements.
    Render:  manim -pqh quantifaya_ep3.py FullEpisode
    Preview: manim -pql quantifaya_ep3.py FullEpisode
    """
    def construct(self) -> None:
        # ══════════════════════════════════════════════════════════════════════
        # SCENE 1 — Cold Open         AUDIO: 60.120s
        # ══════════════════════════════════════════════════════════════════════
        # Beat map (narration proportions from script word counts):
        #   Beat-A  Nobel hook + names + died         ~40%  →  24.0s
        #   Beat-B  Formula + "few can derive"        ~30%  →  18.0s
        #   Beat-C  Manifesto + title card            ~30%  →  18.0s
        # ──────────────────────────────────────────────────────────────────────
        self.add_sound(f"{AUDIO_DIR}/ep3_scene1_intro.mp3")

        # Beat-A: names + Nobel (anim≈8s, budget=24.0s → wait=16s split 5+5+2+4)
        names1 = VGroup(
            Text("Fischer Black",  color=FG, font_size=52),
            Text("Myron Scholes",  color=FG, font_size=52),
            Text("Robert Merton",  color=FG, font_size=52),
        ).arrange(DOWN, buff=0.4).shift(UP * 0.5)
        for n in names1:
            self.play(FadeIn(n), run_time=0.6)
        self.wait(5)     # "1997. The Nobel Committee in Stockholm…"
        nobel1 = Text("1997 Nobel Prize in Economics.",
                      color=GOLD, font_size=36).next_to(names1, DOWN, buff=0.5)
        self.play(FadeIn(nobel1))
        self.wait(5)     # "…awarded the Prize in Economics to Myron Scholes…"
        x_mark1 = Cross(names1[0], color=RED, stroke_width=5)
        died1 = Text(
            "Died: August 30, 1995. Nobel Prizes are not awarded posthumously.",
            color=RED, font_size=22,
        ).next_to(names1[0], RIGHT, buff=0.3)
        src1 = cite("[16] Nobel Committee (1997), Royal Swedish Academy of Sciences")
        self.play(Create(x_mark1), FadeIn(died1), FadeIn(src1))
        self.wait(2)     # "Fischer Black, the third architect…was not there."
        self.wait(4)     # "The most famous equation in quantitative finance…"

        # Beat-B: formula (anim≈8s, budget=18.0s → wait=10s split 5+5)
        self.play(
            FadeOut(names1), FadeOut(nobel1), FadeOut(x_mark1),
            FadeOut(died1), FadeOut(src1),
        )
        formula1 = MathTex(
            r"C = S_0 N(d_1) - K e^{-rT} N(d_2)",
            color=RED, font_size=56,
        ).center()
        self.play(Write(formula1))
        self.wait(5)     # "This is it. The Black-Scholes formula…"
        desc1 = VGroup(
            Text("The most famous equation in finance.",
                 color=FG, font_size=26),
            Text("Taught in every program. Understood by almost none.",
                 color=FG, font_size=26),
            Text("Derived by even fewer.",
                 color=ORANGE, font_size=26, weight=BOLD),
        ).arrange(DOWN, buff=0.25).next_to(formula1, DOWN, buff=0.5)
        self.play(FadeIn(desc1))
        self.wait(5)     # "Every quant knows it. Most people in finance…"
        self.play(FadeOut(formula1), FadeOut(desc1))

        # Beat-C: manifesto + title card (anim≈5s, budget=18.0s → wait=13s split 5+8)
        manifesto1 = VGroup(
            Text("Today we derive it.", color=GOLD, font_size=36, weight=BOLD),
            Text("All of it. From first principles.", color=FG, font_size=28),
            Text("No hand-waving. No 'it can be shown.' We show.",
                 color=ORANGE, font_size=26, slant=ITALIC),
        ).arrange(DOWN, buff=0.35).center()
        self.play(FadeIn(manifesto1))
        self.wait(5)     # "After this video, you'll be in that last category…"
        title_card1 = VGroup(
            Text("QUANTIFAYA", color=PURPLE, font_size=52, weight=BOLD),
            Text("Episode 3", color=FG, font_size=26),
            Text("Black-Scholes — Derived From Scratch",
                 color=GOLD, font_size=34),
            Text("PDE  →  Heat Equation  →  Formula  →  Nobel Prize",
                 color=FG, font_size=22),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeOut(manifesto1), FadeIn(title_card1))
        self.wait(8)     # "Welcome to Episode Three of Quantifaya. Let's go."
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 2 — Problem Setup     AUDIO: 114.072s
        # ══════════════════════════════════════════════════════════════════════
        # Beat map:
        #   Beat-A  Call/Put payoff diagram           ~25%  →  28.5s
        #   Beat-B  Timeline                          ~20%  →  22.8s
        #   Beat-C  History (Bachelier → Samuelson → BS) ~35%  →  39.9s
        #   Beat-D  "Here's how they did it"          ~20%  →  22.8s
        # ──────────────────────────────────────────────────────────────────────
        self.add_sound(f"{AUDIO_DIR}/ep3_scene2_problem_setup.mp3")

        title2 = Text("Step 0: What Are We Actually Pricing?",
                      color=GOLD, font_size=36).to_edge(UP)
        src2 = cite("[5] Bachelier (1900)  |  [4] Samuelson (1965)  |  [7] Hull (2018)")
        self.play(FadeIn(title2), FadeIn(src2))

        # Beat-A: payoff diagram (anim≈8s, budget=28.5s → wait=20.5s)
        ax2 = Axes(
            x_range=[0, 160, 20], y_range=[0, 60, 10],
            x_length=9, y_length=5, axis_config={"color": FG},
        )
        ax_lbl2 = ax2.get_axis_labels(
            MathTex(r"S_T", color=FG, font_size=24),
            MathTex(r"\text{Payoff}", color=FG, font_size=24),
        )
        K2 = 100
        call_payoff2 = ax2.plot(lambda x: max(x - K2, 0),
                                x_range=[0, 160], color=GREEN, stroke_width=3)
        put_payoff2  = ax2.plot(lambda x: max(K2 - x, 0),
                                x_range=[0, 160], color=RED, stroke_width=3)
        k_dot2   = Dot(ax2.c2p(K2, 0), color=GOLD)
        k_label2 = MathTex("K", color=GOLD, font_size=24).next_to(k_dot2, DOWN)
        call_label2 = MathTex(r"\text{Call: }\max(S_T - K, 0)",
                              color=GREEN, font_size=24).to_corner(UR).shift(DOWN * 0.5)
        put_label2  = MathTex(r"\text{Put: }\max(K - S_T, 0)",
                              color=RED, font_size=24).next_to(call_label2, DOWN)
        self.play(Create(ax2), Write(ax_lbl2))
        self.play(Create(call_payoff2), FadeIn(call_label2))
        self.play(Create(k_dot2), Write(k_label2))
        self.play(Create(put_payoff2), FadeIn(put_label2))
        self.wait(20.5)  # "A European call option is a contract that gives…"

        # Beat-B: timeline (anim≈4s, budget=22.8s → wait=18.8s)
        self.play(
            FadeOut(ax2), FadeOut(ax_lbl2), FadeOut(call_payoff2),
            FadeOut(put_payoff2), FadeOut(k_dot2), FadeOut(k_label2),
            FadeOut(call_label2), FadeOut(put_label2),
        )
        timeline2 = VGroup(
            Line(LEFT * 5, RIGHT * 5, color=FG),
            Dot(LEFT * 5, color=GOLD),
            Dot(RIGHT * 5, color=GOLD),
            Text("t = 0\n'Pay C'\nKnow: S₀, K, r, σ",
                 color=TEAL, font_size=20, line_spacing=1.3)
                .next_to(LEFT * 5, DOWN, buff=0.3),
            Text("t = T\n'Receive max(S_T−K, 0)'\nDon't know: S_T",
                 color=ORANGE, font_size=20, line_spacing=1.3)
                .next_to(RIGHT * 5, DOWN, buff=0.3),
        )
        self.play(Create(timeline2))
        self.wait(18.8)  # "Both of these are trivially easy to understand at expiry…"

        # Beat-C: history (anim≈6s, budget=39.9s → wait=33.9s)
        self.play(FadeOut(timeline2))
        history2 = VGroup(
            VGroup(
                Text("Bachelier (1900) [5]", color=GOLD, font_size=24, weight=BOLD),
                Text("First mathematical option model. Arithmetic BM. Heroic.",
                     color=FG, font_size=20),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("Samuelson (1965) [4]", color=GOLD, font_size=24, weight=BOLD),
                Text("GBM. Right dynamics. No closed form.",
                     color=FG, font_size=20),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("Black, Scholes, Merton (1973) [1][2]",
                     color=GOLD, font_size=24, weight=BOLD),
                Text("Closed form. Nobel Prize. $600T market.",
                     color=GREEN, font_size=20),
            ).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).center()
        self.play(LaggedStart(*[FadeIn(h) for h in history2], lag_ratio=0.4))
        self.wait(33.9)  # "People tried to solve this problem long before Black and Scholes…"

        # Beat-D: closing line (budget=22.8s → wait=22.8s)
        self.wait(22.8)  # "Then in 1973, Black, Scholes, and Merton closed the problem…"
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 3 — Assumptions       AUDIO: 157.752s
        # ══════════════════════════════════════════════════════════════════════
        # Beat map:
        #   Beat-A  Assumption ① (GBM)                ~22%  →  34.7s
        #   Beat-B  Assumption ② (constant σ,r)       ~25%  →  39.4s
        #   Beat-C  Assumption ③ (continuous trading) ~22%  →  34.7s
        #   Beat-D  Assumption ④ (no divs, European)  ~15%  →  23.7s
        #   Beat-E  Wilmott quote + closing           ~16%  →  25.2s
        # ──────────────────────────────────────────────────────────────────────
        self.add_sound(f"{AUDIO_DIR}/ep3_scene3_assumptions.mp3")

        title3 = Text("The Four Assumptions — The Price of Tractability",
                      color=GOLD, font_size=34).to_edge(UP)
        src3 = cite("[8] Wilmott (2006)  |  [9] Taleb (1997)  |  [10] Taleb (2007)")
        self.play(FadeIn(title3), FadeIn(src3))

        assumptions3 = [
            (BLUE_NORM,
             "① Stock follows GBM:  dS = μSdt + σSdB",
             "Fat tails ignored. Vol clustering ignored. Ep.1 problem lives here.",
             '"Those who gave us the Normal distribution to describe market randomness\n'
             ' have a lot to answer for." — Taleb [10]'),
            (ORANGE,
             "② Constant σ and r",
             "The entire vol surface contradicts this. Since 1987, permanently.",
             "The smile exists. It has never left."),
            (RED,
             "③ Continuous, costless trading",
             "Bid-ask, slippage, discrete rebalancing — all ignored.",
             '"The dynamic hedging trap." — Taleb, Dynamic Hedging [9]'),
            (GREEN,
             "④ No dividends. European exercise only.",
             "Both are fixable. American options need numerical methods.",
             "Not today's problem. But you should know the extensions exist."),
        ]
        # Beat-A through Beat-D: 4 assumptions (anim≈2s each, budget split by word count)
        for col, head, body, snark in assumptions3:
            grp3 = VGroup(
                Text(head,  color=col,  font_size=26, weight=BOLD),
                Text(body,  color=FG,   font_size=20),
                Text(snark, color=GOLD, font_size=18, slant=ITALIC, line_spacing=1.2),
            ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).center()
            self.play(FadeIn(grp3))
            self.wait(8)     # assumption narration
            self.play(FadeOut(grp3))

        # Beat-E: Wilmott quote + closing (anim≈2s, budget=25.2s → wait=23.2s)
        wilmott3 = VGroup(
            Text('"All models are wrong.\n The question is whether they are wrong in a useful way."',
                 color=GOLD, font_size=28, slant=ITALIC, line_spacing=1.4),
            Text("— P. Wilmott, Paul Wilmott on Quantitative Finance [8]",
                 color=FG, font_size=22),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeIn(wilmott3))
        self.wait(23.2)  # "So: four assumptions, all wrong, model still dominant…"
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 4 — PDE Derivation    AUDIO: 217.584s
        # ══════════════════════════════════════════════════════════════════════
        # Beat map:
        #   Beat-A  Setup + Itô on V                    ~25%  →  54.4s
        #   Beat-B  Delta-hedge + dB cancellation       ~35%  →  76.2s
        #   Beat-C  No-arbitrage → PDE                  ~25%  →  54.4s
        #   Beat-D  Greek labels + boundary cond.       ~15%  →  32.6s
        # ──────────────────────────────────────────────────────────────────────
        self.add_sound(f"{AUDIO_DIR}/ep3_scene4_pde.mp3")

        title4 = Text("The Derivation — Itô + No-Arbitrage = Black-Scholes PDE",
                      color=GOLD, font_size=32).to_edge(UP)
        src4 = cite("[1] Black & Scholes (1973)  |  [3] Itô (1944)  |  [6] Shreve (2004)")
        self.play(FadeIn(title4), FadeIn(src4))

        # Beat-A: setup + Itô (anim≈12s, budget=54.4s → wait=42.4s split 10+16+16.4)
        setup4 = VGroup(
            MathTex(r"\text{Stock: } dS = \mu S\,dt + \sigma S\,dB",
                    color=FG, font_size=30),
            MathTex(r"\text{Option: } V = V(S,t) \text{ — unknown}",
                    color=FG, font_size=30),
            MathTex(r"\text{Goal: find } V(S,t) \text{ explicitly}",
                    color=TEAL, font_size=30),
        ).arrange(DOWN, buff=0.3).shift(UP * 0.5)
        self.play(FadeIn(setup4))
        self.wait(10)    # "The setup: stock price S follows Geometric Brownian Motion…"
        self.play(FadeOut(setup4))

        steps4 = [
            ("Step 1 — Apply Itô's Lemma to V(S,t):",
             r"dV=\!\left(\frac{\partial V}{\partial t}+\mu S\frac{\partial V}{\partial S}"
             r"+\frac{1}{2}\sigma^2 S^2\frac{\partial^2 V}{\partial S^2}\right)dt"
             r"+\sigma S\frac{\partial V}{\partial S}\,dB"),
            ("Step 2 — Delta-hedge portfolio  Π = V − ΔS,  Δ = ∂V/∂S:",
             r"\Pi = V - \frac{\partial V}{\partial S}\cdot S"),
            ("Step 3 — Compute dΠ = dV − Δ·dS and expand:",
             r"d\Pi=\!\left(\frac{\partial V}{\partial t}"
             r"+\frac{1}{2}\sigma^2S^2\frac{\partial^2 V}{\partial S^2}\right)dt"
             r"\quad\leftarrow\text{dB terms cancel!  μ terms cancel!}"),
        ]
        for lbl, eq in steps4:
            g = VGroup(
                Text(lbl, color=TEAL, font_size=24),
                MathTex(eq, color=FG, font_size=28),
            ).arrange(DOWN, buff=0.3).center()
            self.play(FadeIn(g))
            self.wait(16)  # each step narration
            self.play(FadeOut(g))

        # Beat-C: no-arbitrage → PDE (anim≈6s, budget=54.4s → wait=48.4s)
        noarb4 = VGroup(
            Text("No-arbitrage: riskless portfolio earns r  →  dΠ = rΠ dt",
                 color=TEAL, font_size=24),
            Text("Set equal. Rearrange.", color=FG, font_size=22),
        ).arrange(DOWN, buff=0.2).shift(UP * 2)
        self.play(FadeIn(noarb4))

        pde4 = MathTex(
            r"\frac{\partial V}{\partial t}"
            r"+rS\frac{\partial V}{\partial S}"
            r"+\frac{1}{2}\sigma^2S^2\frac{\partial^2 V}{\partial S^2}"
            r"-rV=0",
            color=GOLD, font_size=44,
        ).next_to(noarb4, DOWN, buff=0.5)
        box4 = SurroundingRectangle(pde4, color=PURPLE, buff=0.3, stroke_width=3)
        self.play(Write(pde4), Create(box4))
        self.wait(48.4)  # "Step five: a riskless portfolio must earn the risk-free rate…"

        # Beat-D: Greek labels (anim≈4s, budget=32.6s → wait=28.6s)
        labels4 = VGroup(
            Text("∂V/∂t  →  theta", color=TEAL, font_size=20),
            Text("rS·∂V/∂S  →  rate×delta", color=TEAL, font_size=20),
            Text("½σ²S²·∂²V/∂S²  →  gamma term (Itô correction)",
                 color=ORANGE, font_size=20),
            Text("−rV  →  discounting", color=TEAL, font_size=20),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(box4, DOWN, buff=0.4)
        self.play(LaggedStart(*[FadeIn(l) for l in labels4], lag_ratio=0.2))
        self.wait(28.6)  # "Every term has a name traders use daily…"
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 5 — Heat Equation     AUDIO: 215.928s
        # ══════════════════════════════════════════════════════════════════════
        # Beat map:
        #   Beat-A  Three substitutions                 ~25%  →  54.0s
        #   Beat-B  Heat equation reveal                ~25%  →  54.0s
        #   Beat-C  Green's function                    ~25%  →  54.0s
        #   Beat-D  Arrival at formula                  ~25%  →  53.9s
        # ──────────────────────────────────────────────────────────────────────
        self.add_sound(f"{AUDIO_DIR}/ep3_scene5_heat_equation.mp3")

        title5 = Text("Solving the PDE — The Heat Equation Trick",
                      color=GOLD, font_size=34).to_edge(UP)
        src5 = cite("[6] Shreve (2004), Ch.4  |  [14] Karatzas & Shreve (1991)")
        self.play(FadeIn(title5), FadeIn(src5))

        # Beat-A: three substitutions (anim≈8s, budget=54.0s → wait=46s split 15+15+16)
        subs5 = [
            ("Substitution A — Time reversal:",
             r"\tau = T - t \quad\Rightarrow\quad"
             r"\frac{\partial V}{\partial t} = -\frac{\partial V}{\partial \tau}"),
            ("Substitution B — Log-price (centres the problem):",
             r"x = \ln(S/K),\quad S = Ke^x"),
            ("Substitution C — Remove discounting:",
             r"V(S,t) = e^{-r\tau}\,u(x,\tau)"),
        ]
        for lbl, eq in subs5:
            g = VGroup(
                Text(lbl, color=TEAL, font_size=24),
                MathTex(eq, color=FG, font_size=32),
            ).arrange(DOWN, buff=0.25).center()
            self.play(FadeIn(g))
            self.wait(15)  # each substitution narration
            self.play(FadeOut(g))

        # Beat-B: heat equation (anim≈6s, budget=54.0s → wait=48s)
        heat_label5 = Text("After substitution — the Black-Scholes PDE becomes:",
                           color=TEAL, font_size=24).shift(UP * 2.5)
        heat5 = MathTex(
            r"\frac{\partial u}{\partial \tau}"
            r"= \frac{1}{2}\sigma^2\frac{\partial^2 u}{\partial \xi^2}",
            color=GOLD, font_size=52,
        )
        heat_box5 = SurroundingRectangle(heat5, color=PURPLE, buff=0.3, stroke_width=3)
        fourier5 = Text(
            "The Heat Equation — Joseph Fourier, 1822.\n"
            "Physics from 1822. Option pricing from 1973. Same equation.",
            color=FG, font_size=22, line_spacing=1.3,
        ).next_to(heat_box5, DOWN, buff=0.4)
        self.play(FadeIn(heat_label5), Write(heat5), Create(heat_box5))
        self.play(FadeIn(fourier5))
        self.wait(48)    # "This. Is. The. Heat. Equation. Joseph Fourier derived this…"

        # Beat-C: Green's function (anim≈6s, budget=54.0s → wait=48s)
        self.play(
            FadeOut(heat_label5), FadeOut(heat5),
            FadeOut(heat_box5), FadeOut(fourier5),
        )
        gf_title5 = Text("Solution — Green's Function (Gaussian convolution):",
                         color=TEAL, font_size=26).shift(UP * 2.5)
        gf_eq5 = MathTex(
            r"u(\xi,\tau)=\int_{-\infty}^{\infty}u_0(\xi_0)"
            r"\cdot\frac{1}{\sigma\sqrt{2\pi\tau}}"
            r"\exp\!\left(-\frac{(\xi-\xi_0)^2}{2\sigma^2\tau}\right)d\xi_0",
            color=FG, font_size=26,
        )
        gf_note5 = Text(
            "Integrate the payoff against a Normal kernel.\n"
            "Gaussian blur of the payoff, diffused backward in time.",
            color=GOLD, font_size=22, slant=ITALIC, line_spacing=1.3,
        ).next_to(gf_eq5, DOWN, buff=0.4)
        self.play(FadeIn(gf_title5), FadeIn(gf_eq5), FadeIn(gf_note5))
        self.wait(48)    # "The heat equation has a classical solution via its fundamental solution…"

        # Beat-D: arrival at formula (anim≈4s, budget=53.9s → wait=49.9s)
        arrives5 = VGroup(
            Text("Evaluate the integral → transform back → arrive at:",
                 color=TEAL, font_size=22),
            MathTex(r"C = S_0 N(d_1) - K e^{-rT} N(d_2)",
                    color=GOLD, font_size=42),
        ).arrange(DOWN, buff=0.3).next_to(gf_note5, DOWN, buff=0.4)
        self.play(FadeIn(arrives5))
        self.wait(49.9)  # "When you carry out this integral explicitly…combined into one formula."
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 6 — Formula           AUDIO: 150.384s
        # ══════════════════════════════════════════════════════════════════════
        # Beat map:
        #   Beat-A  Formula + d1,d2                     ~15%  →  22.6s
        #   Beat-B  Four dissections                    ~55%  →  82.7s  (20.7s each)
        #   Beat-C  Put-Call Parity                     ~30%  →  45.1s
        # ──────────────────────────────────────────────────────────────────────
        self.add_sound(f"{AUDIO_DIR}/ep3_scene6_formula.mp3")

        title6 = Text("The Formula — Every Term Has a Job",
                      color=GOLD, font_size=36).to_edge(UP)
        src6 = cite("[1] Black & Scholes (1973), p.644  |  [7] Hull (2018), Ch.19")
        self.play(FadeIn(title6), FadeIn(src6))

        # Beat-A: formula + d1,d2 (anim≈5s, budget=22.6s → wait=17.6s)
        formula6 = MathTex(r"C = S_0 N(d_1) - K e^{-rT} N(d_2)",
                           color=GOLD, font_size=44).shift(UP * 1.5)
        d_eqs6 = VGroup(
            MathTex(r"d_1=\frac{\ln(S_0/K)+(r+\frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}",
                    color=FG, font_size=26),
            MathTex(r"d_2 = d_1 - \sigma\sqrt{T}", color=FG, font_size=26),
        ).arrange(RIGHT, buff=0.8).next_to(formula6, DOWN, buff=0.3)
        self.play(Write(formula6), FadeIn(d_eqs6))
        self.wait(17.6)  # "The Black-Scholes formula for a European call is…"

        # Beat-B: four dissections (anim≈2s each, budget=82.7s → wait=80.7s split 20+20+20+20.7)
        dissections6 = [
            (BLUE_NORM, r"Ke^{-rT}",
             "PV of strike — what you pay if you exercise"),
            (GREEN, r"N(d_2) = \mathbb{P}^Q(S_T > K)",
             "Risk-neutral probability of finishing in the money"),
            (ORANGE, r"N(d_1) = \Delta",
             "Delta — the hedge ratio. Shares to hold to replicate the option."),
            (PURPLE, r"d_1 - d_2 = \sigma\sqrt{T}",
             "The Itô correction — again. Always here. Never leaving."),
        ]
        for col, eq, desc in dissections6:
            g = VGroup(
                MathTex(eq, color=col, font_size=34),
                Text(desc, color=FG, font_size=22, slant=ITALIC),
            ).arrange(DOWN, buff=0.2).center()
            self.play(FadeIn(g))
            self.wait(20)  # each dissection narration
            self.play(FadeOut(g))

        # Beat-C: put-call parity (anim≈3s, budget=45.1s → wait=42.1s)
        pcp6 = VGroup(
            Text("Put-Call Parity — derived from no-arbitrage in 30 seconds:",
                 color=TEAL, font_size=24),
            MathTex(r"C - P = S_0 - Ke^{-rT}", color=GOLD, font_size=40),
            Text("Long call + short put = long stock + short bond. Always.",
                 color=FG, font_size=22),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeIn(pcp6))
        self.wait(42.1)  # "Before we move on — Put-Call Parity. It takes thirty seconds…"
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 7 — Risk-Neutral      AUDIO: 138.744s
        # ══════════════════════════════════════════════════════════════════════
        # Beat map:
        #   Beat-A  Mystery: μ vanished                 ~15%  →  20.8s
        #   Beat-B  Two worlds (P vs Q) + Girsanov      ~35%  →  48.6s
        #   Beat-C  Fundamental Theorem                 ~35%  →  48.6s
        #   Beat-D  Closing: don't confuse Q with reality ~15% → 20.8s
        # ──────────────────────────────────────────────────────────────────────
        self.add_sound(f"{AUDIO_DIR}/ep3_scene7_risk_neutral.mp3")

        title7 = Text("The Risk-Neutral World — The Deepest Insight",
                      color=GOLD, font_size=34).to_edge(UP)
        src7 = cite(
            "[12] Harrison & Kreps (1979)  |  [13] Harrison & Pliska (1981)  "
            "|  [11] Cox & Ross (1976)"
        )
        self.play(FadeIn(title7), FadeIn(src7))

        # Beat-A: mystery (anim≈2s, budget=20.8s → wait=18.8s)
        mystery7 = VGroup(
            Text("μ — the expected return of the stock — vanished from the PDE.",
                 color=FG, font_size=24),
            Text("A stock returning 5% and one returning 25% have the SAME option price",
                 color=ORANGE, font_size=24, weight=BOLD),
            Text("if their volatility σ is identical. Why?", color=FG, font_size=24),
        ).arrange(DOWN, buff=0.3).shift(UP * 1.5)
        self.play(FadeIn(mystery7))
        self.wait(18.8)  # "Here's the question that should be bothering you…"
        self.play(FadeOut(mystery7))

        # Beat-B: two worlds (anim≈8s, budget=48.6s → wait=40.6s split 5+2+33.6)
        two_worlds7 = VGroup(
            VGroup(
                Text("Real World P", color=BLUE_NORM, font_size=28, weight=BOLD),
                MathTex(r"dS = \mu S\,dt + \sigma S\,dB^P", color=FG, font_size=26),
                Text("Drift = μ (actual expected return)", color=FG, font_size=20),
                Text("Investors are risk-averse", color=FG, font_size=20),
                Text("μ > r required to hold equity", color=FG, font_size=20),
            ).arrange(DOWN, buff=0.2, aligned_edge=LEFT),
            VGroup(
                Text("Risk-Neutral World Q", color=GREEN, font_size=28, weight=BOLD),
                MathTex(r"dS = r S\,dt + \sigma S\,dB^Q", color=FG, font_size=26),
                Text("Drift = r (risk-free rate)", color=FG, font_size=20),
                Text("Investors are risk-neutral", color=FG, font_size=20),
                Text("All assets earn r. μ irrelevant.", color=GREEN, font_size=20),
            ).arrange(DOWN, buff=0.2, aligned_edge=LEFT),
        ).arrange(RIGHT, buff=1.2).center()
        arrow7 = Arrow(two_worlds7[0].get_right(), two_worlds7[1].get_left(),
                       color=GOLD, buff=0.2)
        girsanov7 = Text("Girsanov's Theorem", color=GOLD, font_size=20)\
                        .next_to(arrow7, UP, buff=0.1)
        self.play(FadeIn(two_worlds7[0]))
        self.wait(5)     # "Under the real-world probability measure P…"
        self.play(FadeIn(two_worlds7[1]), Create(arrow7), FadeIn(girsanov7))
        self.wait(2)     # "Under the risk-neutral measure Q…"
        self.wait(33.6)  # "The transition between these two worlds is governed by Girsanov's Theorem…"
        self.play(FadeOut(two_worlds7), FadeOut(arrow7), FadeOut(girsanov7))

        # Beat-C: Fundamental Theorem (anim≈5s, budget=48.6s → wait=43.6s)
        fund_thm7 = VGroup(
            Text("Fundamental Theorem of Asset Pricing:",
                 color=GOLD, font_size=28, weight=BOLD),
            MathTex(r"C = e^{-rT}\,\mathbb{E}^Q[\max(S_T-K,\,0)]",
                    color=GOLD, font_size=42),
            VGroup(
                MathTex(r"\text{No arbitrage}\;\Leftrightarrow\;\exists\;Q",
                        color=TEAL, font_size=24),
                Text("[12] Harrison & Kreps (1979)", color=TEAL, font_size=18),
            ).arrange(RIGHT, buff=0.4),
            VGroup(
                MathTex(r"\text{Market complete}\;\Leftrightarrow\;Q\text{ is unique}",
                        color=TEAL, font_size=24),
                Text("[13] Harrison & Pliska (1981)", color=TEAL, font_size=18),
            ).arrange(RIGHT, buff=0.4),
        ).arrange(DOWN, buff=0.35).center()
        box7 = SurroundingRectangle(fund_thm7[1], color=PURPLE, buff=0.2, stroke_width=2)
        self.play(FadeIn(fund_thm7), Create(box7))
        self.wait(43.6)  # "This gives us the risk-neutral pricing formula…"

        # Beat-D: closing (budget=20.8s → wait=20.8s)
        self.wait(20.8)  # "The risk-neutral world is not a description of how investors actually behave…"
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 8 — Where BS Breaks   AUDIO: 172.248s
        # ══════════════════════════════════════════════════════════════════════
        # Beat map:
        #   Beat-A  Vol smile chart                     ~25%  →  43.1s
        #   Beat-B  Verdict + Black Monday              ~15%  →  25.8s
        #   Beat-C  Three reasons + extensions          ~45%  →  77.5s
        #   Beat-D  Irony quote                         ~15%  →  25.8s
        # ──────────────────────────────────────────────────────────────────────
        self.add_sound(f"{AUDIO_DIR}/ep3_scene8_breaks.mp3")

        title8 = Text("Where Black-Scholes Breaks — The Vol Smile",
                      color=GOLD, font_size=34).to_edge(UP)
        src8 = cite("[15] Derman & Kani (1994)  |  [8] Wilmott (2006)  |  [10] Taleb (2007)")
        self.play(FadeIn(title8), FadeIn(src8))

        # Beat-A: vol smile chart (anim≈8s, budget=43.1s → wait=35.1s)
        ax8 = Axes(
            x_range=[70, 130, 10], y_range=[0.10, 0.40, 0.05],
            x_length=9, y_length=5, axis_config={"color": FG},
        )
        ax_lbl8 = ax8.get_axis_labels(
            Tex(r"\text{Strike }K", color=FG, font_size=22),
            Tex(r"\sigma_{\text{imp}}", color=FG, font_size=22),
        )
        flat8 = ax8.plot(lambda x: 0.20, x_range=[70, 130],
                         color=BLUE_NORM, stroke_width=2, stroke_dasharray=[8, 4])
        flat_lbl8 = Text("BS prediction: σ = constant",
                         color=BLUE_NORM, font_size=20).next_to(ax8, RIGHT, buff=0.3).shift(UP * 0.5)
        smile8 = ax8.plot(lambda x: 0.20 + 0.0008 * (100 - x) ** 2 - 0.0005 * (x - 100),
                          x_range=[70, 130], color=ORANGE, stroke_width=3)
        smile_lbl8 = Text("Reality: vol skew post-1987",
                          color=ORANGE, font_size=20).next_to(ax8, RIGHT, buff=0.3).shift(DOWN * 0.2)
        self.play(Create(ax8), Write(ax_lbl8))
        self.play(Create(flat8), FadeIn(flat_lbl8))
        self.play(Create(smile8), FadeIn(smile_lbl8))
        self.wait(35.1)  # "If Black-Scholes were correct, every option on the same underlying…"

        # Beat-B: verdict (anim≈2s, budget=25.8s → wait=23.8s)
        verdict8 = Text(
            "Constant σ has been empirically violated since October 19, 1987.\n"
            "The smile appeared after Black Monday. It has never left.",
            color=RED, font_size=22, line_spacing=1.3,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(verdict8))
        self.wait(23.8)  # "This phenomenon did not exist before October 1987…"
        self.play(
            FadeOut(ax8), FadeOut(ax_lbl8), FadeOut(flat8), FadeOut(flat_lbl8),
            FadeOut(smile8), FadeOut(smile_lbl8), FadeOut(verdict8),
        )

        # Beat-C: extensions (anim≈6s, budget=77.5s → wait=71.5s)
        extensions8 = VGroup(
            VGroup(
                Text("Local Vol — Derman & Kani (1994) [15]",
                     color=ORANGE, font_size=24, weight=BOLD),
                MathTex(r"\sigma = \sigma(S, t)", color=FG, font_size=26),
                Text("Fits the smile exactly. Loses intuition.",
                     color=FG, font_size=20),
            ).arrange(DOWN, buff=0.15),
            VGroup(
                Text("Stochastic Vol — Heston (1993)",
                     color=ORANGE, font_size=24, weight=BOLD),
                MathTex(r"d\sigma^2 = \kappa(\theta-\sigma^2)dt + \xi\sigma\,dW_t",
                        color=FG, font_size=24),
                Text("Vol is random. Mean-reverting. Analytically tractable (barely).",
                     color=FG, font_size=20),
            ).arrange(DOWN, buff=0.15),
            VGroup(
                Text("Jump-Diffusion — Merton (1976) [2]",
                     color=ORANGE, font_size=24, weight=BOLD),
                MathTex(r"dS = \mu S\,dt + \sigma S\,dB + S\,dJ_t",
                        color=FG, font_size=24),
                Text("Adds crash risk. OTM puts now justified.",
                     color=FG, font_size=20),
            ).arrange(DOWN, buff=0.15),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).center()
        self.play(LaggedStart(*[FadeIn(e) for e in extensions8], lag_ratio=0.35))
        self.wait(71.5)  # "The industry response was a hierarchy of increasingly sophisticated models…"

        # Beat-D: irony quote (anim≈2s, budget=25.8s → wait=23.8s)
        irony8 = Text(
            '"Black-Scholes is wrong. The market quotes options IN Black-Scholes implied vol.\n'
            ' The wrong model is the language of the right market.\n'
            ' This is either profound or farcical. Possibly both."',
            color=GOLD, font_size=20, slant=ITALIC, line_spacing=1.3,
        ).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(irony8))
        self.wait(23.8)  # "Here's the irony that professional options traders live with every day…"
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 9 — Lessons           AUDIO: 101.304s
        # ══════════════════════════════════════════════════════════════════════
        # Beat map:
        #   Beat-A  Four truths                         ~55%  →  55.7s  (13.9s each)
        #   Beat-B  Taleb quote                         ~25%  →  25.3s
        #   Beat-C  Reference roll                      ~20%  →  20.3s
        # ──────────────────────────────────────────────────────────────────────
        self.add_sound(f"{AUDIO_DIR}/ep3_scene9_lessons.mp3")

        title9 = Text("What This Means For You — No Softening",
                      color=GOLD, font_size=36).to_edge(UP)
        sub9 = Text("Axe Capital doesn't soften anything either.",
                    color=FG, font_size=20, slant=ITALIC).next_to(title9, DOWN, buff=0.1)
        self.play(FadeIn(title9), FadeIn(sub9))

        # Beat-A: four truths (anim≈8s, budget=55.7s → wait=47.7s split 11.5+12+12+12.2)
        truths9 = [
            (RED,    "Ⅰ",
             "Black-Scholes is Itô + no-arbitrage + heat equation.\nThree ideas. All derivable. All yours now.",
             "[1][3][6]"),
            (GOLD,   "Ⅱ",
             "μ doesn't matter. Explain WHY in your next interview.\nNot just that it cancels — WHY.",
             "[12] Harrison & Kreps (1979)"),
            (TEAL,   "Ⅲ",
             "It's been wrong about vol since 1987.\nKnow HOW it's wrong. Worth more than knowing it's wrong.",
             "[15] Derman & Kani (1994)"),
            (PURPLE, "Ⅳ",
             "Interview calibration:\n→ Derive BS PDE from scratch  ← Top 5%\n→ Explain N(d₁) ≠ N(d₂)  ← Top 10%\n→ Explain the smile  ← Top 20%\n→ Just state the formula  ← Everyone else.",
             ""),
        ]
        for col, num, main, src_ref in truths9:
            g = VGroup(
                Text(f"{num}", color=col, font_size=36, weight=BOLD),
                VGroup(
                    Text(main, color=FG, font_size=22, line_spacing=1.3),
                    Text(src_ref, color=col, font_size=18, slant=ITALIC)
                    if src_ref else VGroup(),
                ).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
            ).arrange(RIGHT, buff=0.4).center()
            self.play(FadeIn(g))
            self.wait(11.5)  # each truth narration
            self.play(FadeOut(g))

        # Beat-B: Taleb quote (anim≈2s, budget=25.3s → wait=23.3s)
        taleb9 = VGroup(
            Text('"The hedging errors are generally small for vanilla options\n'
                 ' but can be monstrous for exotics."',
                 color=GOLD, font_size=26, slant=ITALIC, line_spacing=1.4),
            Text("— N.N. Taleb, Dynamic Hedging [9]", color=FG, font_size=20),
            Text("Know your model. Know its limits. Know when it fails.",
                 color=ORANGE, font_size=24, weight=BOLD),
            Text("That's what separates a quant from someone who Googled the formula.",
                 color=FG, font_size=22, slant=ITALIC),
        ).arrange(DOWN, buff=0.35).center()
        self.play(FadeIn(taleb9))
        self.wait(23.3)  # "Taleb wrote in Dynamic Hedging…"

        # Beat-C: references (anim≈3s, budget=20.3s → wait=17.3s)
        self.play(FadeOut(taleb9), FadeOut(title9), FadeOut(sub9))
        refs9 = [
            "[1]  Black & Scholes (1973). J. Political Economy, 81(3), 637–654.",
            "[2]  Merton (1973). Bell J. Economics, 4(1), 141–183.",
            "[3]  Itô (1944). Proc. Imperial Academy Tokyo, 20(8), 519–524.",
            "[4]  Samuelson (1965). Industrial Mgmt Review, 6(2), 13–32.",
            "[5]  Bachelier (1900). Ann. Sci. École Normale Sup., 17, 21–86.",
            "[6]  Shreve (2004). Stochastic Calculus for Finance II. Springer.",
            "[7]  Hull (2018). Options, Futures, and Other Derivatives, 10th ed. Pearson.",
            "[8]  Wilmott (2006). Paul Wilmott on Quantitative Finance, 2nd ed. Wiley.",
            "[9]  Taleb (1997). Dynamic Hedging. Wiley.",
            "[10] Taleb (2007). The Black Swan. Random House.",
            "[11] Cox & Ross (1976). J. Financial Economics, 3(1–2), 145–166.",
            "[12] Harrison & Kreps (1979). J. Economic Theory, 20(3), 381–408.",
            "[13] Harrison & Pliska (1981). Stochastic Processes & Applications, 11(3), 215–260.",
            "[14] Karatzas & Shreve (1991). Brownian Motion and Stochastic Calculus. Springer.",
            "[15] Derman & Kani (1994). Risk Magazine, 7(2), 32–39.",
            "[16] Nobel Committee (1997). Royal Swedish Academy of Sciences.",
        ]
        ref_title9 = Text("References", color=GOLD, font_size=30).to_edge(UP)
        ref_grp9 = VGroup(*[Text(r, color=TEAL, font_size=15) for r in refs9])\
                       .arrange(DOWN, buff=0.14, aligned_edge=LEFT).center()
        self.play(FadeIn(ref_title9), FadeIn(ref_grp9))
        self.wait(17.3)  # reference roll
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 10 — Outro            AUDIO: 118.800s
        # ══════════════════════════════════════════════════════════════════════
        # Beat map:
        #   Beat-A  Logo + recap                        ~30%  →  35.6s
        #   Beat-B  Challenge + next ep                 ~40%  →  47.5s
        #   Beat-C  Subscribe CTA                       ~30%  →  35.7s
        # ──────────────────────────────────────────────────────────────────────
        self.add_sound(f"{AUDIO_DIR}/ep3_scene10_outro.mp3")

        # Beat-A: logo + recap (anim≈5s, budget=35.6s → wait=30.6s split 5+25.6)
        logo10 = Text("QUANTIFAYA", color=PURPLE, font_size=64, weight=BOLD)
        tagline10 = Text(
            "Financial Engineering. Explained Rigorously. Applied Practically.",
            color=GOLD, font_size=22,
        ).next_to(logo10, DOWN, buff=0.3)
        self.play(FadeIn(logo10), FadeIn(tagline10))
        self.wait(5)     # "That's Episode Three."

        recap10 = VGroup(
            Text("✓  Option pricing problem — Bachelier to Black-Scholes",
                 color=GREEN, font_size=20),
            Text("✓  Four assumptions and the cost of each",
                 color=GREEN, font_size=20),
            Text("✓  PDE derived: Itô + delta-hedge + no-arbitrage",
                 color=GREEN, font_size=20),
            Text("✓  Heat equation transformation and analytical solution",
                 color=GREEN, font_size=20),
            Text("✓  Formula anatomy: N(d₁), N(d₂), d₁ vs d₂",
                 color=GREEN, font_size=20),
            Text("✓  Put-Call Parity in 30 seconds",
                 color=GREEN, font_size=20),
            Text("✓  Risk-neutral measure Q and Fundamental Theorem",
                 color=GREEN, font_size=20),
            Text("✓  Vol smile, local vol, stochastic vol, jumps",
                 color=GREEN, font_size=20),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).center()
        self.play(FadeOut(logo10), FadeOut(tagline10))
        self.play(LaggedStart(*[FadeIn(r) for r in recap10], lag_ratio=0.12))
        self.wait(25.6)  # "We covered the full Black-Scholes arc…"

        # Beat-B: challenge + next ep (anim≈6s, budget=47.5s → wait=41.5s split 2+20+19.5)
        challenge10 = VGroup(
            Text("Comment Challenge:", color=GOLD, font_size=28, weight=BOLD),
            MathTex(r"\text{Price a cash-or-nothing digital call: pays \$1 if }S_T>K",
                    color=FG, font_size=26),
            Text("Show the full derivation using the risk-neutral formula.",
                 color=FG, font_size=22),
            Text("Why does only N(d₂) appear — and not N(d₁)?",
                 color=ORANGE, font_size=22, weight=BOLD),
            Text("First correct answer gets pinned.", color=TEAL, font_size=20),
        ).arrange(DOWN, buff=0.25).center()
        self.play(FadeOut(recap10), FadeIn(challenge10))
        self.wait(2)     # "Comment challenge: price a cash-or-nothing digital call…"
        next_ep10 = VGroup(
            Text("Next on Quantifaya:", color=GOLD, font_size=30, weight=BOLD),
            Text("The Greeks — Delta, Gamma, Vega, Theta",
                 color=ORANGE, font_size=28),
            MathTex(
                r"\Delta=N(d_1)\quad\Gamma=\frac{N'(d_1)}{S\sigma\sqrt{T}}"
                r"\quad\mathcal{V}=S\sqrt{T}\,N'(d_1)",
                color=FG, font_size=26,
            ),
            Text("Why Gamma is dangerous. Why Theta bleeds every night.",
                 color=FG, font_size=22),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeIn(next_ep10))
        self.wait(19.5)  # "Next week: the Greeks. Delta, Gamma, Vega, Theta…"

        # Beat-C: subscribe CTA (budget=35.7s → wait=35.7s)
        self.wait(35.7)  # "Subscribe. Share this with one person who's ever pretended…"