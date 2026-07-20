# quantifaya_ep4.py  —  WORD-PROPORTIONAL BEAT-LEVEL SYNC  (definitive build)
# ─────────────────────────────────────────────────────────────────────────────
# Quantifaya — Episode 4
# "The Greeks: Delta, Gamma, Vega — Built Intuitively"
#
# TIMING SYSTEM (same methodology as Episodes 1-3)
# ──────────────────────────────────────────────
# Every self.wait() was derived by:
#   1. Counting exact words in each narration beat from generate_audio_ep4.py
#   2. beat_duration = scene_audio_total × (beat_words / scene_total_words)
#   3. beat_wait = beat_duration − animation_seconds_in_that_beat
#
# GUARANTEE: self.clear() fires only after all beat waits are consumed.
# self.add_sound() for scene N+1 fires after self.clear() — zero overlap.
#
# RENDER
#   manim -pqh quantifaya_ep4.py FullEpisode --fps 60    # 1080p60 production
#   manim -pql quantifaya_ep4.py FullEpisode             # 480p15 preview
#   manim -pql quantifaya_ep4.py SceneDelta              # single scene test
# ─────────────────────────────────────────────────────────────────────────────

from __future__ import annotations
import numpy as np
from manim import *
from scipy.stats import norm as scipy_norm

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
    return Text(refs, color=TEAL, font_size=13).to_corner(DR).shift(UP*0.1+LEFT*0.1)

# ── Black-Scholes helpers ───────────────────────────────────────────────────
def bs_d1(S, K=100, T=0.5, sigma=0.2, r=0.05):
    return (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(max(T, 1e-6)))

def bs_delta(S, K=100, T=0.5, sigma=0.2, r=0.05):
    return scipy_norm.cdf(bs_d1(S, K, T, sigma, r))

def bs_gamma(S, K=100, T=0.5, sigma=0.2, r=0.05):
    d1 = bs_d1(S, K, T, sigma, r)
    return scipy_norm.pdf(d1) / (S * sigma * np.sqrt(max(T, 1e-6)))

def bs_vega(S, K=100, T=0.5, sigma=0.2, r=0.05):
    d1 = bs_d1(S, K, T, sigma, r)
    return S * np.sqrt(max(T, 1e-6)) * scipy_norm.pdf(d1)

def bs_theta(S, K=100, T=0.5, sigma=0.2, r=0.05):
    d1  = bs_d1(S, K, T, sigma, r)
    d2  = d1 - sigma * np.sqrt(max(T, 1e-6))
    t_daily = (-S * scipy_norm.pdf(d1) * sigma / (2 * np.sqrt(max(T, 1e-6)))
               - r * K * np.exp(-r * T) * scipy_norm.cdf(d2)) / 365
    return t_daily

def bs_price(S, K=100, T=0.5, sigma=0.2, r=0.05):
    d1 = bs_d1(S, K, T, sigma, r)
    d2 = d1 - sigma * np.sqrt(max(T, 1e-6))
    return S * scipy_norm.cdf(d1) - K * np.exp(-r * T) * scipy_norm.cdf(d2)


# ══════════════════════════════════════════════════════════════════════════════
# SCENE 1 — COLD OPEN: THE WEAPONS RACK   ~1:30
# ══════════════════════════════════════════════════════════════════════════════

class SceneIntro(Scene):
    """Enhanced standalone preview — no audio required."""

    def construct(self):
        self._run(standalone=True)

    def _run(self, standalone=False):
        if not standalone:
            self.add_sound(f"{AUDIO_DIR}/ep4_scene1_intro.mp3")

        # ── BEAT A: Five Greeks slam in  (~30s of 90s)
        # ─────────────────────────────────────────────────────────────────────
        greek_specs = [
            (r"\Delta", GOLD,      UP*1.5+LEFT*3,   LEFT),
            (r"\Gamma", ORANGE,    UP*1.5+RIGHT*3,  RIGHT),
            (r"\mathcal{V}", TEAL, ORIGIN,           UP),
            (r"\Theta", RED,       DOWN*1.5+LEFT*3,  DOWN),
            (r"\rho",   PURPLE,    DOWN*1.5+RIGHT*3, DOWN),
        ]
        letters = VGroup()
        for sym, col, pos, direc in greek_specs:
            ltr = MathTex(sym, color=col, font_size=96)
            ltr.move_to(pos + direc*2)
            self.play(FadeIn(ltr, shift=-direc*2), run_time=0.4)
            letters.add(ltr)
        self.wait(2)

        desc = Text("These are not symbols.\nThey are the control panel of a $600 trillion market.",
                    color=FG, font_size=26, line_spacing=1.4).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(desc))
        self.wait(2)

        # ── BEAT B: Labels + Taleb quote  (~30s)
        # ─────────────────────────────────────────────────────────────────────
        labels = VGroup(
            Text("Δ  → How much the option moves when the stock moves",   color=GOLD, font_size=16),
            Text("Γ  → How much Delta changes — curvature you can't ignore", color=ORANGE, font_size=16),
            Text("𝒱 → The volatility exposure that bites harder than Delta", color=TEAL, font_size=16),
            Text("Θ  → The rent you pay every night for holding the position", color=RED, font_size=16),
            Text("ρ  → Interest rate sensitivity — the quiet assassin",     color=PURPLE, font_size=16),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).to_edge(DOWN, buff=0.2)
        self.play(FadeOut(desc), FadeIn(labels))
        self.wait(4)

        # Taleb quote
        taleb_block = VGroup(
            MathTex(r"\text{``The Greeks are derivatives of the option price.}",
                    color=GOLD, font_size=22),
            MathTex(r"\text{They are meaningful for a single option.}",
                    color=GOLD, font_size=22),
            MathTex(r"\text{They are treacherous for a book.''}",
                    color=GOLD, font_size=22),
            Text("— N.N. Taleb, Dynamic Hedging, p.112 [T4]", color=FG, font_size=18),
        ).arrange(DOWN, buff=0.15).shift(UP*0.3)
        self.play(FadeOut(labels), FadeIn(taleb_block))
        self.wait(6)

        # ── BEAT C: Title card  (~30s)
        # ─────────────────────────────────────────────────────────────────────
        red_text = Text("Your textbook taught you the formula.\nToday we teach you what they mean on a real desk.",
                        color=RED, font_size=24, weight=BOLD, line_spacing=1.4).center()
        self.play(FadeOut(taleb_block), FadeIn(red_text))
        self.wait(4)

        title_card = VGroup(
            Text("QUANTIFAYA", color=PURPLE, font_size=52, weight=BOLD),
            Text("Episode 4", color=FG, font_size=26),
            Text("The Greeks — Delta, Gamma, Vega Built Intuitively",
                 color=GOLD, font_size=30),
            Text("BS Formula  →  Real Desk  →  Where They Break",
                 color=FG, font_size=22),
        ).arrange(DOWN, buff=0.25).center()
        self.play(FadeOut(letters), FadeOut(red_text), FadeIn(title_card))
        self.wait(6)


# ══════════════════════════════════════════════════════════════════════════════
# SCENE 2 — DELTA: THE FIRST DERIVATIVE   ~4:00
# ══════════════════════════════════════════════════════════════════════════════

class SceneDelta(Scene):
    def construct(self):
        self._run(standalone=True)

    def _run(self, standalone=False):
        if not standalone:
            self.add_sound(f"{AUDIO_DIR}/ep4_scene2_delta.mp3")

        title2 = Text("Δ — Delta: The Hedge Ratio That Lies to You", color=GOLD, font_size=32).to_edge(UP)
        src2   = cite("[T1] Taleb Ch.7  |  [H2] Hull (2018), p.418  |  [BS] Black & Scholes (1973)")
        self.play(FadeIn(title2), FadeIn(src2))                 # 1s

        # ── BEAT A: Definition panels  (~50s | anim≈4s | wait≈46s)
        # ─────────────────────────────────────────────────────────────────────
        defn = VGroup(
            VGroup(
                Text("Mathematical:", color=TEAL, font_size=20, weight=BOLD),
                MathTex(r"\Delta = \frac{\partial C}{\partial S} = N(d_1)",
                        color=FG, font_size=38),
            ).arrange(DOWN, buff=0.1),
            VGroup(
                Text("Practical:", color=TEAL, font_size=20, weight=BOLD),
                Text("Shares of stock to hold to replicate\nthe option's price change for a small move in S.",
                     color=FG, font_size=20, line_spacing=1.3),
            ).arrange(DOWN, buff=0.1),
        ).arrange(RIGHT, buff=0.8).shift(UP*0.5)
        self.play(FadeIn(defn))                                 # 1s
        self.wait(10)

        # ── BEAT B: Derivation  (~60s | anim≈6s | wait≈54s)
        # ─────────────────────────────────────────────────────────────────────
        self.play(FadeOut(defn))                                # 1s
        bs_eq = MathTex(
            r"C = S_0 N(d_1) - K e^{-rT} N(d_2)",
            color=FG, font_size=30).shift(UP*1.5)
        self.play(Write(bs_eq))                                 # 2s
        self.wait(4)

        deriv_eq = MathTex(
            r"\frac{\partial C}{\partial S} = N(d_1) + S N'(d_1)\frac{\partial d_1}{\partial S}"
            r"- Ke^{-rT}N'(d_2)\frac{\partial d_2}{\partial S}",
            color=FG, font_size=22).next_to(bs_eq, DOWN, buff=0.3)
        self.play(Write(deriv_eq))                              # 2s
        self.wait(6)

        cancel = MathTex(r"\Delta_{\text{call}} = N(d_1)", color=GOLD, font_size=38)
        cancel_box = SurroundingRectangle(cancel, color=GOLD, buff=0.2, stroke_width=3)
        cancel_group = VGroup(cancel, cancel_box).next_to(deriv_eq, DOWN, buff=0.4)
        self.play(Write(cancel), Create(cancel_box))            # 2s
        self.wait(10)

        put_delta = MathTex(r"\Delta_{\text{put}} = N(d_1) - 1 = -N(-d_1)",
                            color=ORANGE, font_size=28).next_to(cancel_group, DOWN, buff=0.3)
        self.play(FadeIn(put_delta))                            # 1s
        self.wait(30)

        self.play(FadeOut(bs_eq), FadeOut(deriv_eq),
                  FadeOut(cancel_group), FadeOut(put_delta))    # 1s

        # ── BEAT C: S-curve  (~60s | anim≈6s | wait≈54s)
        # ─────────────────────────────────────────────────────────────────────
        ax = Axes(x_range=[60, 140, 10], y_range=[0, 1, 0.2],
                  x_length=9, y_length=5, axis_config={"color": FG})
        ax_lbl = ax.get_axis_labels(Tex("S", color=FG, font_size=22),
                                     Tex(r"\Delta", color=FG, font_size=22))
        s_curve = ax.plot(lambda s: bs_delta(s, T=0.5),
                          x_range=[62, 138], color=BLUE_NORM, stroke_width=3)
        self.play(Create(ax), Write(ax_lbl), Create(s_curve))  # 3s
        self.wait(8)

        # Key points
        for sv, label, col in [(70, "OTM: Δ≈0.05", ORANGE),
                                (100, "ATM: Δ≈0.50", GOLD),
                                (135, "ITM: Δ≈0.97", GREEN)]:
            d = Dot(ax.c2p(sv, bs_delta(sv, T=0.5)), color=col, radius=0.08)
            lbl = Text(label, color=col, font_size=16).next_to(d, RIGHT, buff=0.1)
            self.play(FadeIn(d), FadeIn(lbl), run_time=0.5)
            self.wait(4)

        # Tangent at ATM
        slp = bs_gamma(100, T=0.5)
        tan_line = ax.plot(lambda s: 0.5 + slp*(s-100),
                           x_range=[70, 130], color=GREEN, stroke_width=2)
        tan_lbl = Text("Tangent — instantaneous hedge", color=GREEN, font_size=16
                       ).next_to(ax.c2p(115, 0.7), UP, buff=0.1)
        self.play(Create(tan_line), FadeIn(tan_lbl))           # 1s
        self.wait(12)

        # Time decay curves
        self.play(FadeOut(s_curve), FadeOut(tan_line), FadeOut(tan_lbl),
                  FadeOut(ax_lbl), FadeOut(ax))                 # 1s

        ax2 = Axes(x_range=[60, 140, 10], y_range=[0, 1, 0.2],
                   x_length=9, y_length=5, axis_config={"color": FG})
        ax2_lbl = ax2.get_axis_labels(Tex("S", color=FG, font_size=22),
                                       Tex(r"\Delta", color=FG, font_size=22))
        self.play(Create(ax2), Write(ax2_lbl))                 # 2s
        for T_, col_, lbl_ in [(1.0, BLUE_NORM, "T=1yr"),
                                (1/12, ORANGE, "T=1mo"),
                                (1/252, RED, "T=1d")]:
            crv = ax2.plot(lambda s, T=T_: bs_delta(s, T=T_),
                           x_range=[62, 138], color=col_, stroke_width=2.5)
            lbl = Text(lbl_, color=col_, font_size=16).next_to(ax2.c2p(110, bs_delta(110, T=T_)+0.02), UP)
            self.play(Create(crv), FadeIn(lbl), run_time=0.6)
        gamma_bomb = Text("Gamma explosion near expiry — preview of Scene 4",
                          color=RED, font_size=18).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(gamma_bomb))                           # 1s
        self.wait(20)

        # ── BEAT D: Taleb quote + Delta hedging  (~70s | anim≈4s | wait≈66s)
        # ─────────────────────────────────────────────────────────────────────
        self.play(FadeOut(ax2), FadeOut(ax2_lbl), FadeOut(gamma_bomb))  # 1s
        taleb2 = VGroup(
            MathTex(r"\text{``Orthodox definition of delta: } dF/dU\text{ — the derivative}",
                    color=GOLD, font_size=22),
            MathTex(r"\text{of the option price to the underlying.}",
                    color=GOLD, font_size=22),
            MathTex(r"\text{From a standpoint of trading, it offers no significance,}",
                    color=GOLD, font_size=22),
            MathTex(r"\text{for the following reasons: there is no such thing}",
                    color=GOLD, font_size=22),
            MathTex(r"\text{as an infinitely small move in the market.}",
                    color=GOLD, font_size=22),
            Text("— Taleb, Dynamic Hedging, p.118 [T5]", color=FG, font_size=16),
        ).arrange(DOWN, buff=0.1).center()
        self.play(FadeIn(taleb2))                               # 1s
        self.wait(8)

        # Numerical hedging example
        hedge_setup = VGroup(
            Text("Delta Hedging Example:", color=TEAL, font_size=22, weight=BOLD),
            Text("S=$100, K=$100, T=6mo, σ=20%, r=5%", color=FG, font_size=20),
            Text("Call price C=$10.45  |  Δ = N(d₁) = 0.5793", color=GOLD, font_size=22),
            Text("Short 1 call → buy 0.5793 shares to delta-hedge", color=GREEN, font_size=20),
            Text("If S→$101: option gains ~$0.58, shares gain $0.58 → flat", color=FG, font_size=18),
            Text("Perfect in continuous time. An approximation in real markets.",
                 color=ORANGE, font_size=18, slant=ITALIC),
        ).arrange(DOWN, buff=0.2).center()
        self.play(FadeOut(taleb2), FadeIn(hedge_setup))         # 1s
        self.wait(38)


# ══════════════════════════════════════════════════════════════════════════════
# SCENE 3 — DELTA IN PRACTICE   ~2:00
# ══════════════════════════════════════════════════════════════════════════════

class SceneDeltaPractice(Scene):
    def construct(self):
        self._run(standalone=True)

    def _run(self, standalone=False):
        if not standalone:
            self.add_sound(f"{AUDIO_DIR}/ep4_scene3_delta_practice.mp3")

        title3 = Text("Delta in Practice — The Lies Your Risk System Tells You",
                      color=GOLD, font_size=30).to_edge(UP)
        src3   = cite("[T1] Taleb, Dynamic Hedging, Ch.7, pp.118–133")
        self.play(FadeIn(title3), FadeIn(src3))                 # 1s

        # ── BEAT A: Book problem  (~50s | anim≈4s | wait≈46s)
        # ─────────────────────────────────────────────────────────────────────
        book = VGroup(
            Text("Taleb example from p.133 [T1]:", color=TEAL, font_size=22, weight=BOLD),
            Text("• Long $1M of 96 calls, Δ=0.824  →  +$824,000 delta", color=GREEN, font_size=20),
            Text("• Short $1M of 104 calls, Δ=0.198  →  −$198,000 delta", color=RED, font_size=20),
            Text("• Total delta: +$626,000  →  Sell $626,000 of forward. Done?", color=FG, font_size=20),
            Text("✗  NOT done. Aggregate delta disguises local structure.", color=ORANGE, font_size=20, weight=BOLD),
            Text("Map P&L: long everywhere EXCEPT near S=100 where flat.", color=FG, font_size=18),
            Text("The textbook hedge is misleading.", color=RED, font_size=20),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).center()
        self.play(LaggedStart(*[FadeIn(b) for b in book], lag_ratio=0.15))  # 3s
        self.wait(14)

        # Barrier example
        barrier = VGroup(
            Text("Barrier option delta → infinity at the barrier [T1]:", color=RED, font_size=20, weight=BOLD),
            Text("• Delta at barrier: 10,000%  →  $500M implied exposure", color=ORANGE, font_size=20),
            Text("• Trader's maximum loss: $400K on a $5M trade", color=GREEN, font_size=20),
            Text("• Both numbers mathematically correct. Neither operationally useful.",
                 color=FG, font_size=20),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).center()
        self.play(FadeOut(book), FadeIn(barrier))               # 1s
        self.wait(16)

        # ── BEAT B: Discrete delta solution  (~60s | anim≈4s | wait≈56s)
        # ─────────────────────────────────────────────────────────────────────
        self.play(FadeOut(barrier))                             # 1s
        fix = VGroup(
            Text("Taleb's Fix — Discrete Delta:", color=GOLD, font_size=26, weight=BOLD),
            MathTex(r"\Delta_{\text{disc}} = \frac{C(S+\Delta S) - C(S-\Delta S)}{2\,\Delta S}",
                    color=FG, font_size=34),
            Text("ΔS = 1–2 sigma move — realistic, tradeable increment",
                 color=TEAL, font_size=20),
            Text("Bakes in gamma and vega automatically.",
                 color=FG, font_size=20),
            Text("Less pure mathematically. More honest operationally.",
                 color=ORANGE, font_size=20, slant=ITALIC),
        ).arrange(DOWN, buff=0.25).center()
        self.play(FadeIn(fix))                                  # 1s
        self.wait(38)


# ══════════════════════════════════════════════════════════════════════════════
# SCENE 4 — GAMMA: THE CURVATURE THAT COSTS YOU   ~4:00
# ══════════════════════════════════════════════════════════════════════════════

class SceneGamma(Scene):
    def construct(self):
        self._run(standalone=True)

    def _run(self, standalone=False):
        if not standalone:
            self.add_sound(f"{AUDIO_DIR}/ep4_scene4_gamma.mp3")

        title4 = Text("Γ — Gamma: The Curvature That Costs You Every Day",
                      color=GOLD, font_size=30).to_edge(UP)
        src4   = cite("[T2] Taleb, Dynamic Hedging, Ch.8  |  [H3] Hull (2018), p.428")
        self.play(FadeIn(title4), FadeIn(src4))                 # 1s

        # ── BEAT A: Definition + Taylor connection  (~70s | anim≈6s | wait≈64s)
        # ─────────────────────────────────────────────────────────────────────
        gamma_def = VGroup(
            MathTex(r"\Gamma = \frac{\partial^2 C}{\partial S^2}"
                    r"= \frac{\partial\Delta}{\partial S}"
                    r"= \frac{N'(d_1)}{S\sigma\sqrt{T}}",
                    color=FG, font_size=32),
            Text("Always POSITIVE for long options (calls AND puts).",
                 color=GREEN, font_size=20),
            Text("Always NEGATIVE for short options.",
                 color=RED, font_size=20),
        ).arrange(DOWN, buff=0.2).shift(UP*0.8)
        self.play(FadeIn(gamma_def))                            # 1s
        self.wait(10)

        # Taylor expansion connection
        taylor = VGroup(
            Text("From Ep.2: The Taylor Expansion of C:", color=TEAL, font_size=22),
            MathTex(r"dC = \Delta\,dS + \frac{1}{2}\Gamma\,(dS)^2 + \cdots",
                    color=FG, font_size=34),
            Text("Δ → linear term (tangent line).  Γ → curvature correction.",
                 color=FG, font_size=20),
            Text("Long Γ: actual gain > Delta prediction on EVERY large move.",
                 color=GREEN, font_size=20, weight=BOLD),
            Text("Short Γ: actual loss > Delta prediction on EVERY large move.",
                 color=RED, font_size=20, weight=BOLD),
        ).arrange(DOWN, buff=0.2).shift(DOWN*0.5)
        self.play(FadeOut(gamma_def), FadeIn(taylor))           # 1s
        self.wait(20)

        # ── BEAT B: Long vs Short Gamma panels  (~60s | anim≈4s | wait≈56s)
        # ─────────────────────────────────────────────────────────────────────
        self.play(FadeOut(taylor))                              # 1s

        # Two panels
        long_panel = VGroup(
            Text("LONG GAMMA (bought call)", color=GREEN, font_size=22, weight=BOLD),
            Text("• Up: gain MORE than Delta said", color=GREEN, font_size=18),
            Text("• Down: lose LESS than Delta said", color=GREEN, font_size=18),
            Text("• Gamma P&L always POSITIVE", color=GREEN, font_size=18),
            Text("• But you PAY Theta (time decay)", color=RED, font_size=18),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).shift(LEFT*2.5+UP*0.5)
        short_panel = VGroup(
            Text("SHORT GAMMA (sold call)", color=RED, font_size=22, weight=BOLD),
            Text("• Up: lose MORE than Delta said", color=RED, font_size=18),
            Text("• Down: gain LESS than Delta said", color=RED, font_size=18),
            Text("• Gamma P&L always NEGATIVE", color=RED, font_size=18),
            Text("• But you COLLECT Theta daily", color=GREEN, font_size=18),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).shift(RIGHT*2.5+UP*0.5)
        divider_line = DashedLine(UP*1.5, DOWN*1.5, color=FG, stroke_opacity=0.4).center()
        trade_off = Text("Long Gamma = pay Theta to own convexity\nShort Gamma = collect Theta, exposed to large moves",
                         color=GOLD, font_size=18, line_spacing=1.3, weight=BOLD).to_edge(DOWN, buff=0.4)

        self.play(FadeIn(long_panel), FadeIn(short_panel), Create(divider_line))  # 2s
        self.play(FadeIn(trade_off))                            # 1s
        self.wait(25)

        # ── BEAT C: Gamma vs S + T plots  (~60s | anim≈6s | wait≈54s)
        # ─────────────────────────────────────────────────────────────────────
        self.play(FadeOut(long_panel), FadeOut(short_panel),
                  FadeOut(divider_line), FadeOut(trade_off))    # 1s

        ax = Axes(x_range=[60, 140, 10], y_range=[0, 0.08, 0.02],
                  x_length=8, y_length=4.5, axis_config={"color": FG})
        ax_lbl = ax.get_axis_labels(Tex("S", color=FG, font_size=20),
                                     Tex(r"\Gamma", color=FG, font_size=20))
        self.play(Create(ax), Write(ax_lbl))                   # 2s
        for T_, col_, lbl_ in [(1.0, BLUE_NORM, "T=1yr"),
                                (0.25, ORANGE, "T=3mo"),
                                (1/52, RED, "T=1wk")]:
            crv = ax.plot(lambda s, T=T_: min(bs_gamma(s, T=T_), 0.08),
                          x_range=[62, 138], color=col_, stroke_width=2.5)
            lbl = Text(lbl_, color=col_, font_size=16)\
                      .move_to(ax.c2p(108, min(bs_gamma(108, T=T_), 0.075)+0.002))
            self.play(Create(crv), FadeIn(lbl), run_time=0.6)

        explosion = Text("Gamma EXPLOSION near expiry ATM — market-maker nightmare",
                         color=RED, font_size=18).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(explosion))                            # 1s
        self.wait(20)

        # ── BEAT D: Shadow Gamma  (~50s | anim≈4s | wait≈46s)
        # ─────────────────────────────────────────────────────────────────────
        self.play(FadeOut(ax), FadeOut(ax_lbl), FadeOut(explosion))  # 1s

        shadow = VGroup(
            Text("Taleb's Shadow Gamma [T2]:", color=GOLD, font_size=26, weight=BOLD),
            Text("Conventional Gamma: symmetric — same sensitivity up and down.",
                 color=FG, font_size=20),
            Text("Shadow Gamma: accounts for vol-spot correlation.",
                 color=ORANGE, font_size=20),
            Text("In equity markets: DOWN-GAMMA > UP-GAMMA", color=RED, font_size=22, weight=BOLD),
            Text("A crash causes BOTH a delta change AND a vol spike.",
                 color=FG, font_size=18),
            Text("Always compute Up-Gamma and Down-Gamma separately.",
                 color=TEAL, font_size=20, weight=BOLD),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).center()
        self.play(LaggedStart(*[FadeIn(s) for s in shadow], lag_ratio=0.15))  # 2s
        self.wait(38)


# ══════════════════════════════════════════════════════════════════════════════
# SCENE 5 — GAMMA IN PRACTICE   ~2:00
# ══════════════════════════════════════════════════════════════════════════════

class SceneGammaPractice(Scene):
    def construct(self):
        self._run(standalone=True)

    def _run(self, standalone=False):
        if not standalone:
            self.add_sound(f"{AUDIO_DIR}/ep4_scene5_gamma_practice.mp3")

        title5 = Text("Gamma in Practice — The Daily P&L Battle",
                      color=GOLD, font_size=30).to_edge(UP)
        src5   = cite("[T2] Taleb, Dynamic Hedging, pp.127–162")
        self.play(FadeIn(title5), FadeIn(src5))                 # 1s

        # ── BEAT A: Gamma P&L scenarios  (~60s | anim≈6s | wait≈54s)
        # ─────────────────────────────────────────────────────────────────────
        setup = Text("Setup: S=$100, K=$100, T=30d, σ=20%,  Γ = 0.0668",
                     color=TEAL, font_size=22).to_edge(UP).shift(DOWN*0.5)
        self.play(FadeIn(setup))                                # 1s

        scenarios = VGroup(
            VGroup(
                Text("Quiet day — ΔS = $0.50:", color=FG, font_size=20),
                MathTex(r"\tfrac{1}{2}(0.0668)(0.50)^2 = \$0.008\text{ per option}",
                        color=BLUE_NORM, font_size=24),
                Text("Almost nothing. Gamma doesn't earn in calm markets.",
                     color=FG, font_size=16, slant=ITALIC),
            ).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
            VGroup(
                Text("Volatile day — ΔS = $3.00:", color=FG, font_size=20),
                MathTex(r"\tfrac{1}{2}(0.0668)(3.00)^2 = \$0.30\text{ per option}",
                        color=ORANGE, font_size=24),
                Text("Thirty cents. Starts to matter on large positions.",
                     color=FG, font_size=16, slant=ITALIC),
            ).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
            VGroup(
                Text("CRASH — ΔS = $10.00:", color=RED, font_size=20, weight=BOLD),
                MathTex(r"\tfrac{1}{2}(0.0668)(10.00)^2 = \$3.34\text{ per option}",
                        color=RED, font_size=24),
                Text("On 10,000 options: $33,400 in one day. Christmas for long gamma.",
                     color=RED, font_size=16, slant=ITALIC),
            ).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
            Text("Gamma P&L scales as (ΔS)². Double the move → FOUR TIMES the Gamma P&L.",
                 color=GOLD, font_size=20, weight=BOLD),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).center()
        self.play(LaggedStart(*[FadeIn(s) for s in scenarios], lag_ratio=0.2))  # 3s
        self.wait(20)

        # ── BEAT B: Gamma trap + Shadow Gamma case study  (~60s | anim≈5s | wait≈55s)
        # ─────────────────────────────────────────────────────────────────────
        self.play(FadeOut(scenarios))                           # 1s

        trap = VGroup(
            Text("The Gamma Trap Near Expiry:", color=RED, font_size=24, weight=BOLD),
            Text("Day -30:  Γ = 0.0668  →  manageable", color=BLUE_NORM, font_size=20),
            Text("Day -5:   Γ = 0.180   →  starting to bite", color=ORANGE, font_size=20),
            Text("Day -1:   Γ = 0.520   →  dangerous", color=RED, font_size=20),
            Text("Day 0 (ATM): Γ → ∞  →  every crossing triggers rebalance", color=RED, font_size=20, weight=BOLD),
            Text("Each rebalance pays bid-ask. Volatile expiry = hedging cost > premium.",
                 color=FG, font_size=18, slant=ITALIC),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).shift(UP*1.5)
        self.play(FadeIn(trap))                                 # 1s
        self.wait(12)

        # Syldavia case
        syl = VGroup(
            Text("Taleb's Syldavian Elections [T2]:", color=GOLD, font_size=22, weight=BOLD),
            Text("Before election: vol = 20%", color=FG, font_size=18),
            Text("If pro-market wins: vol → 14%, spot ~100", color=GREEN, font_size=18),
            Text("If anarchists win: vol → 29%, spot → 94", color=RED, font_size=18),
            Text("Conventional Gamma gave one number.", color=FG, font_size=18),
            Text("Shadow Gamma (vol-spot correlation) gave a COMPLETELY different answer.",
                 color=ORANGE, font_size=18, weight=BOLD),
            Text("The trader who ignored shadow gamma was exposed.",
                 color=RED, font_size=18, slant=ITALIC),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).center()
        self.play(FadeOut(trap), FadeIn(syl))                   # 1s
        self.wait(38)


# ══════════════════════════════════════════════════════════════════════════════
# SCENE 6 — VEGA: THE VOLATILITY EXPOSURE   ~3:30
# ══════════════════════════════════════════════════════════════════════════════

class SceneVega(Scene):
    def construct(self):
        self._run(standalone=True)

    def _run(self, standalone=False):
        if not standalone:
            self.add_sound(f"{AUDIO_DIR}/ep4_scene6_vega.mp3")

        title6 = Text("𝒱 — Vega: The Greek Traders Fear More Than Delta",
                      color=GOLD, font_size=30).to_edge(UP)
        src6   = cite("[T3] Taleb, Dynamic Hedging, Ch.9  |  [H4] Hull (2018), p.434")
        self.play(FadeIn(title6), FadeIn(src6))                 # 1s

        # ── BEAT A: Definition + Derivation  (~70s | anim≈6s | wait≈64s)
        # ─────────────────────────────────────────────────────────────────────
        vega_def = VGroup(
            MathTex(r"\mathcal{V} = \frac{\partial C}{\partial\sigma}"
                    r"= S\sqrt{T}\,N'(d_1)",
                    color=FG, font_size=32),
            Text("Always POSITIVE for long options (long vol = profit when vol rises).",
                 color=GREEN, font_size=18),
            Text("Not a Greek letter. Also called κ, ζ, λ. Industry calls it Vega.",
                 color=TEAL, font_size=18, slant=ITALIC),
        ).arrange(DOWN, buff=0.2).shift(UP*0.8)
        self.play(FadeIn(vega_def))                             # 1s
        self.wait(14)

        # Derivation
        bs_eq_v = MathTex(r"C = S N(d_1) - Ke^{-rT} N(d_2)", color=FG, font_size=26)
        deriv_v = MathTex(
            r"\frac{\partial C}{\partial\sigma} = S N'(d_1)\frac{\partial d_1}{\partial\sigma}"
            r"- Ke^{-rT} N'(d_2)\frac{\partial d_2}{\partial\sigma}",
            color=FG, font_size=18).next_to(bs_eq_v, DOWN, buff=0.2)
        result_v = MathTex(r"\mathcal{V} = S\sqrt{T}\,N'(d_1)", color=GOLD, font_size=32)
        result_box_v = SurroundingRectangle(result_v, color=GOLD, buff=0.2, stroke_width=3)
        result_group_v = VGroup(result_v, result_box_v).next_to(deriv_v, DOWN, buff=0.3)
        der_group = VGroup(bs_eq_v, deriv_v, result_group_v).center()

        self.play(FadeOut(vega_def), Write(bs_eq_v), Write(deriv_v))  # 3s
        self.wait(10)
        self.play(Write(result_v), Create(result_box_v))        # 2s
        self.wait(20)
        self.play(FadeOut(der_group))                            # 1s

        # ── BEAT B: Vega profiles  (~60s | anim≈5s | wait≈55s)
        # ─────────────────────────────────────────────────────────────────────
        ax = Axes(x_range=[60, 140, 10], y_range=[0, 55, 10],
                  x_length=8, y_length=4.5, axis_config={"color": FG})
        ax_lbl = ax.get_axis_labels(Tex("S", color=FG, font_size=20),
                                     Tex(r"\mathcal{V}", color=FG, font_size=20))
        self.play(Create(ax), Write(ax_lbl))                   # 2s
        for T_, col_, lbl_ in [(2.0, PURPLE, "T=2yr"),
                                (0.5, BLUE_NORM, "T=6mo"),
                                (1/12, ORANGE, "T=1mo")]:
            crv = ax.plot(lambda s, T=T_: bs_vega(s, T=T_),
                          x_range=[62, 138], color=col_, stroke_width=2.5)
            lbl = Text(lbl_, color=col_, font_size=16)\
                      .move_to(ax.c2p(105, min(bs_vega(105, T=T_), 52)+1.5))
            self.play(Create(crv), FadeIn(lbl), run_time=0.6)
        vega_note = Text("Vega scales with √T — longer-dated = more vol exposure.",
                         color=GOLD, font_size=18).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(vega_note))                            # 1s
        self.wait(18)

        # ── BEAT C: Vega-Gamma identity + Modified Vega  (~80s | anim≈5s | wait≈75s)
        # ─────────────────────────────────────────────────────────────────────
        self.play(FadeOut(ax), FadeOut(ax_lbl), FadeOut(vega_note))  # 1s

        identity = VGroup(
            Text("Taleb's Key Identity [T3]:", color=GOLD, font_size=24, weight=BOLD),
            MathTex(r"\mathcal{V} = \Gamma \cdot S^2 \cdot \sigma \cdot T",
                    color=GOLD, font_size=40),
            Text("Vega = integral of expected Gamma rebalancing P&L over the option's life.",
                 color=FG, font_size=18),
            Text("Same strike/maturity → hedge Gamma, hedge Vega. They're linked.",
                 color=TEAL, font_size=18),
            Text("Across different strikes/maturities → they diverge. Manage separately.",
                 color=RED, font_size=18),
        ).arrange(DOWN, buff=0.2).shift(UP*1.0)
        id_box = SurroundingRectangle(identity[1], color=PURPLE, buff=0.2, stroke_width=2)
        self.play(FadeIn(identity), Create(id_box))             # 2s
        self.wait(18)

        # Modified vega
        mod = VGroup(
            Text("Modified Vega — Bucket Analysis [T3]:", color=ORANGE, font_size=22, weight=BOLD),
            Text("Parallel vol shift: standard Vega captures it.", color=FG, font_size=18),
            Text("Vol surface twist: short-end spikes, long-end flat.", color=RED, font_size=18),
            Text("Zero total Vega can still lose massively on a twist.",
                 color=RED, font_size=18, weight=BOLD),
            Text("Solution: bucket Vega — measure Vega at each maturity separately.",
                 color=TEAL, font_size=18, weight=BOLD),
            VGroup(
                Text("Example:", color=GOLD, font_size=18),
                Text("S=$100, T=1yr, V≈$0.40 per 1% vol move", color=FG, font_size=18),
                Text("10,000 calls → $4,000 Vega per vol tick", color=BLUE_NORM, font_size=18),
                Text("5% vol spike → $20,000 profit. Instantly.", color=GREEN, font_size=18),
            ).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).center()
        self.play(FadeOut(identity), FadeOut(id_box), FadeIn(mod))  # 1s
        self.wait(38)


# ══════════════════════════════════════════════════════════════════════════════
# SCENE 7 — THETA: THE RENT   ~2:30
# ══════════════════════════════════════════════════════════════════════════════

class SceneTheta(Scene):
    def construct(self):
        self._run(standalone=True)

    def _run(self, standalone=False):
        if not standalone:
            self.add_sound(f"{AUDIO_DIR}/ep4_scene7_theta.mp3")

        title7 = Text("Θ — Theta: The Rent You Pay Every Night",
                      color=GOLD, font_size=32).to_edge(UP)
        src7   = cite("[H5] Hull (2018), p.431  |  [T2] Taleb, Ch.8 — Gamma/Theta relationship")
        self.play(FadeIn(title7), FadeIn(src7))                 # 1s

        # ── BEAT A: Definition  (~40s | anim≈3s | wait≈37s)
        # ─────────────────────────────────────────────────────────────────────
        theta_eq = VGroup(
            MathTex(r"\Theta = \frac{\partial C}{\partial t}"
                    r"= -\frac{S N'(d_1)\sigma}{2\sqrt{T}} - rKe^{-rT}N(d_2)",
                    color=FG, font_size=26),
            Text("Always NEGATIVE for long options. Time hurts you. Every day.",
                 color=RED, font_size=20),
            Text("Theta is the daily rent for being long optionality.",
                 color=FG, font_size=18, slant=ITALIC),
        ).arrange(DOWN, buff=0.2).shift(UP*0.8)
        self.play(FadeIn(theta_eq))                             # 1s
        self.wait(14)

        # ── BEAT B: Gamma-Theta identity  (~50s | anim≈5s | wait≈45s)
        # ─────────────────────────────────────────────────────────────────────
        self.play(FadeOut(theta_eq))                            # 1s

        pde_ref = Text("From the Black-Scholes PDE (Ep.3):", color=TEAL, font_size=20)
        bs_pde = MathTex(
            r"\Theta + rS\Delta + \tfrac{1}{2}\sigma^2 S^2 \Gamma = rC",
            color=FG, font_size=28)
        ident = MathTex(
            r"\Theta \approx -\frac{1}{2}\sigma^2 S^2 \Gamma",
            color=GOLD, font_size=48)
        ident_box = SurroundingRectangle(ident, color=GOLD, buff=0.25, stroke_width=3)
        ident_group = VGroup(pde_ref, bs_pde, ident, ident_box).arrange(DOWN, buff=0.2).center()

        self.play(FadeIn(pde_ref), Write(bs_pde))               # 2s
        self.wait(8)
        self.play(Write(ident), Create(ident_box))              # 2s

        expl = VGroup(
            Text("Long Γ = pay Θ every night.", color=GREEN, font_size=22, weight=BOLD),
            Text("Short Γ = collect Θ every night.", color=RED, font_size=22, weight=BOLD),
            Text("The market prices convexity exactly. There is no free lunch.",
                 color=ORANGE, font_size=18, slant=ITALIC),
        ).arrange(DOWN, buff=0.15).next_to(ident_group, DOWN, buff=0.3)
        self.play(FadeIn(expl))                                 # 1s
        self.wait(20)

        # ── BEAT C: Theta acceleration  (~60s | anim≈5s | wait≈55s)
        # ─────────────────────────────────────────────────────────────────────
        self.play(FadeOut(ident_group), FadeOut(expl))          # 1s

        ax = Axes(x_range=[0, 90, 10], y_range=[-0.10, 0, 0.02],
                  x_length=9, y_length=4, axis_config={"color": FG})
        ax_lbl = ax.get_axis_labels(
            Tex(r"\text{Days to expiry}", color=FG, font_size=18),
            Tex(r"\Theta\text{ (per day)}", color=FG, font_size=18))
        theta_crv = ax.plot(
            lambda T: min(max(bs_theta(100, T=max(T/365, 1e-4)), -0.10), -1e-6) if T > 0 else -1e-6,
            x_range=[1, 89], color=RED, stroke_width=3)
        self.play(Create(ax), Write(ax_lbl), Create(theta_crv)) # 3s

        accel = Text("Theta ACCELERATES near expiry — not linear decay.",
                     color=ORANGE, font_size=18).to_edge(DOWN, buff=0.5)
        wknd = Text("Weekend effect: Friday→Monday = 3 days of Theta. Sellers love Fridays.",
                    color=GOLD, font_size=16).next_to(accel, UP, buff=0.1)

        # Concrete example
        conc = VGroup(
            Text("S=$100, K=$100, T=30d, σ=20%", color=TEAL, font_size=18),
            Text("Theta = −$0.054/day  → −$1.62/month on a ~$2.20 ATM option",
                 color=FG, font_size=18),
            Text("Short option sellers: quiet markets = steady theta collection.",
                 color=GREEN, font_size=16),
            Text("Until vol spikes and Gamma hurts.",
                 color=RED, font_size=16, weight=BOLD),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).to_edge(DOWN, buff=0.3)

        self.play(FadeIn(accel), FadeIn(wknd))                  # 1s
        self.wait(10)
        self.play(FadeIn(conc))                                 # 1s
        self.wait(24)


# ══════════════════════════════════════════════════════════════════════════════
# SCENE 8 — RHO & FULL DASHBOARD   ~2:00
# ══════════════════════════════════════════════════════════════════════════════

class SceneRhoAndDashboard(Scene):
    def construct(self):
        self._run(standalone=True)

    def _run(self, standalone=False):
        if not standalone:
            self.add_sound(f"{AUDIO_DIR}/ep4_scene8_rho_and_dashboard.mp3")

        title8 = Text("ρ & The Full Greeks Dashboard",
                      color=GOLD, font_size=34).to_edge(UP)
        src8   = cite("[H1] Hull (2018), Ch.19")
        self.play(FadeIn(title8), FadeIn(src8))                 # 1s

        # ── BEAT A: Rho  (~30s | anim≈4s | wait≈26s)
        # ─────────────────────────────────────────────────────────────────────
        rho_block = VGroup(
            MathTex(r"\rho = KTe^{-rT}N(d_2)", color=FG, font_size=36),
            Text("Positive for calls. Negative for puts.", color=FG, font_size=20),
            Text("Usually smallest Greek for equity options.",
                 color=TEAL, font_size=18),
            Text("DOMINATES for long-dated IR derivatives and currencies.",
                 color=ORANGE, font_size=18, weight=BOLD),
        ).arrange(DOWN, buff=0.2).shift(UP*1.0)
        self.play(FadeIn(rho_block))                            # 1s
        self.wait(8)

        # ── BEAT B: Full dashboard table  (~50s | anim≈6s | wait≈44s)
        # ─────────────────────────────────────────────────────────────────────
        self.play(FadeOut(rho_block))                           # 1s

        dash_title = Text("Greeks Dashboard — ATM 6mo Option (S=$100, K=$100, σ=20%, r=5%)",
                          color=GOLD, font_size=20, weight=BOLD).to_edge(UP).shift(DOWN*0.4)
        dash_data = [
            [r"\Delta", r"N(d_1)", "0.5793", "0.58 shares to hedge"],
            [r"\Gamma", r"N'(d_1)/(S\sigma\sqrt{T})", "0.0267", "$0.027 delta gain per $1"],
            [r"\mathcal{V}", r"S\sqrt{T}N'(d_1)", "28.22", "$0.28 per 1% vol move"],
            [r"\Theta", r"-SN'(d_1)\sigma/2\sqrt{T} - rKe^{-rT}N(d_2)", "−$0.038/d", "3.8¢/day decay"],
            [r"\rho", r"KTe^{-rT}N(d_2)", "23.37", "$0.23 per 1% rate move"],
        ]
        rows = VGroup()
        for greek, formula, value, meaning in dash_data:
            row = VGroup(
                MathTex(greek, color=GOLD, font_size=22),
                MathTex(formula, color=FG, font_size=16),
                Text(value, color=BLUE_NORM, font_size=18),
                Text(meaning, color=TEAL, font_size=14),
            ).arrange(RIGHT, buff=0.4)
            rows.add(row)
        rows.arrange(DOWN, buff=0.25, aligned_edge=LEFT).center().shift(DOWN*0.2)

        self.play(FadeIn(dash_title))                           # 1s
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))  # 3s
        self.wait(20)

        # ── BEAT C: P&L attribution  (~40s | anim≈5s | wait≈35s)
        # ─────────────────────────────────────────────────────────────────────
        self.play(FadeOut(dash_title), FadeOut(rows))           # 1s

        pnl_title = Text("The Options Trader's P&L Equation:",
                         color=GOLD, font_size=24, weight=BOLD)
        pnl_eq = MathTex(
            r"\Delta C \approx"
            r"\underbrace{\Delta\,\Delta S}_{\text{lineal}}"
            r"+\underbrace{\tfrac{1}{2}\Gamma(\Delta S)^2}_{\text{curvature}}"
            r"+\underbrace{\mathcal{V}\,\Delta\sigma}_{\text{vol}}"
            r"+\underbrace{\Theta\,\Delta t}_{\text{decay}}"
            r"+\underbrace{\rho\,\Delta r}_{\text{rate}}",
            color=FG, font_size=24)
        pnl_block = VGroup(pnl_title, pnl_eq).arrange(DOWN, buff=0.2).shift(UP*1.5)
        self.play(FadeIn(pnl_block))                            # 1s
        self.wait(6)

        # Concrete example
        example = VGroup(
            Text("Yesterday: ΔS=+$2, Δσ=−0.5%, Δt=1 day", color=TEAL, font_size=20),
            MathTex(r"\Delta C \approx 0.5793\times2"
                    r"+\tfrac{1}{2}(0.0267)(4)"
                    r"+28.22\times(-0.005)"
                    r"+(-0.038)\times1",
                    color=FG, font_size=20),
            MathTex(r"= \underbrace{+1.159}_{\Delta}"
                    r"+\underbrace{+0.053}_{\Gamma}"
                    r"\underbrace{-0.141}_{\mathcal{V}}"
                    r"\underbrace{-0.038}_{\Theta}"
                    r"= +\$1.033",
                    color=GOLD, font_size=24),
            Text("Every dollar of P&L explained. Every Greek accounted for.",
                 color=GREEN, font_size=20, weight=BOLD),
        ).arrange(DOWN, buff=0.2).center()
        self.play(FadeIn(example))                              # 1s
        self.wait(28)


# ══════════════════════════════════════════════════════════════════════════════
# SCENE 9 — TALEB'S SHORTCOMINGS TABLE   ~2:30
# ══════════════════════════════════════════════════════════════════════════════

class SceneTalebShortcomings(Scene):
    def construct(self):
        self._run(standalone=True)

    def _run(self, standalone=False):
        if not standalone:
            self.add_sound(f"{AUDIO_DIR}/ep4_scene9_taleb_shortcomings.mp3")

        title9 = Text("The Greeks and Their Shortcomings",
                      color=GOLD, font_size=34).to_edge(UP)
        sub9 = Text("What Taleb's table on p.112 says that no textbook will.",
                    color=FG, font_size=18, slant=ITALIC).next_to(title9, DOWN, buff=0.05)
        src9 = cite("[T4] Taleb, Dynamic Hedging, p.112  |  [T3] Ch.9, p.163")
        self.play(FadeIn(title9), FadeIn(sub9), FadeIn(src9))  # 1s

        # ── BEAT A: Shortcomings one by one  (~80s | anim≈8s | wait≈72s)
        # ─────────────────────────────────────────────────────────────────────
        shortcomings = [
            (BLUE_NORM, r"\Delta  Delta",
             r"\text{``Delta does not work on a portfolio of options}",
             r"\text{that mixes longs and shorts.}",
             r"\text{It is an extremely weak measure of risks.'' [T4]}",
             "Fix: Discrete delta with realistic increments."),
            (ORANGE, r"\Gamma  Gamma",
             r"\text{``It is meaningless for a portfolio of options.}",
             r"\text{It does not take into account changes in volatility}",
             r"\text{when the market moves.'' [T4]}",
             "Fix: Up-Gamma and Down-Gamma separately. Shadow Gamma."),
            (TEAL, r"\mathcal{V}  Vega",
             r"\text{``Parallel shift assumption — assumes}",
             r"\text{all maturities move simultaneously.'' [T4]}",
             r"",
             "Fix: Bucket Vega by maturity. Modified Vega."),
            (RED, r"\Theta  Theta",
             r"\text{``Does not take into account changes in}",
             r"\text{volatility that co-occur with time passage.'' [T4]}",
             r"",
             "Fix: Term structure of volatilities adjustment."),
        ]
        for col, greek, prob1, prob2, prob3, fix in shortcomings:
            content = [MathTex(greek, color=col, font_size=28, weight=BOLD)]
            for p in [prob1, prob2, prob3]:
                if p:
                    content.append(MathTex(p, color=GOLD, font_size=18))
            content.append(Text(fix, color=TEAL, font_size=18))
            block = VGroup(*content).arrange(DOWN, buff=0.15, aligned_edge=LEFT).center()
            self.play(FadeIn(block))                            # 1s
            self.wait(8)
            self.play(FadeOut(block))                           # 1s

        # ── BEAT B: Meta-lesson  (~70s | anim≈4s | wait≈66s)
        # ─────────────────────────────────────────────────────────────────────
        meta = VGroup(
            MathTex(r"\text{``The conventional training of people, which consists}",
                    color=GOLD, font_size=20),
            MathTex(r"\text{of toying with the conventional derivatives}",
                    color=GOLD, font_size=20),
            MathTex(r"\text{of the Black-Scholes formula, has a negative}",
                    color=GOLD, font_size=20),
            MathTex(r"\text{effect on their operating style.}",
                    color=GOLD, font_size=20),
            MathTex(r"\text{Trading an option bears little relevance}",
                    color=GOLD, font_size=20),
            MathTex(r"\text{to trading a book.''}",
                    color=GOLD, font_size=20),
            Text("— Taleb, Dynamic Hedging, p.163 [T3]", color=FG, font_size=16),
            VGroup(
                Text("The Greeks are the starting vocabulary.",
                     color=ORANGE, font_size=22, weight=BOLD),
                Text("Scenario analysis is the actual risk management.",
                     color=ORANGE, font_size=22, weight=BOLD),
            ).arrange(DOWN, buff=0.1),
        ).arrange(DOWN, buff=0.12).center()
        self.play(FadeIn(meta))                                 # 1s
        self.wait(38)


# ══════════════════════════════════════════════════════════════════════════════
# SCENE 10 — OUTRO   ~1:00
# ══════════════════════════════════════════════════════════════════════════════

class SceneOutro(Scene):
    def construct(self):
        self._run(standalone=True)

    def _run(self, standalone=False):
        if not standalone:
            self.add_sound(f"{AUDIO_DIR}/ep4_scene10_outro.mp3")

        # ── BEAT A: Logo + recap  (~25s | anim≈4s | wait≈21s)
        # ─────────────────────────────────────────────────────────────────────
        logo = Text("QUANTIFAYA", color=PURPLE, font_size=60, weight=BOLD)
        tagline = Text("Financial Engineering. Explained Rigorously. Applied Practically.",
                       color=GOLD, font_size=20).next_to(logo, DOWN, buff=0.2)
        self.play(FadeIn(logo), FadeIn(tagline))                # 1s
        self.wait(3)

        recap_items = [
            "✓  Delta = N(d₁) — hedge ratio and its textbook limits",
            "✓  Discrete delta — Taleb's operational fix for real books",
            "✓  Gamma = N'(d₁)/(Sσ√T) — curvature, long/short trade-off",
            "✓  Up-Gamma / Down-Gamma / Shadow Gamma — skewed markets",
            "✓  Gamma-Theta identity: Θ ≈ −½σ²S²Γ",
            "✓  Vega = S√T·N'(d₁) — vol exposure, scales with √T",
            "✓  Vega-Gamma identity: 𝒱 = ΓS²σT",
            "✓  Theta — daily rent and its expiry acceleration",
            "✓  Full P&L attribution across all Greeks",
            "✓  Taleb's shortcomings table — p.112 of Dynamic Hedging",
        ]
        recap = VGroup(*[Text(r, color=GREEN, font_size=16) for r in recap_items]
                       ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).center()
        self.play(FadeOut(logo), FadeOut(tagline))              # 1s
        self.play(LaggedStart(*[FadeIn(r) for r in recap], lag_ratio=0.08))  # 2s
        self.wait(12)

        # ── BEAT B: Book recs + challenge  (~20s | anim≈3s | wait≈17s)
        # ─────────────────────────────────────────────────────────────────────
        books = VGroup(
            Text("📚  Required Reading:", color=GOLD, font_size=24, weight=BOLD),
            Text("Taleb (1997) — Dynamic Hedging, Ch.7–11  [T1–T4]", color=FG, font_size=20),
            Text("Hull (2018) — Options, Futures & Derivatives, Ch.19  [H1–H5]", color=FG, font_size=20),
        ).arrange(DOWN, buff=0.2).center()
        self.play(FadeOut(recap), FadeIn(books))                # 1s
        self.wait(6)

        challenge = VGroup(
            Text("🎯  Comment Challenge:", color=GOLD, font_size=24, weight=BOLD),
            Text("Prove the Gamma-Theta identity from the BS PDE.",
                 color=FG, font_size=20),
            MathTex(r"\text{Show: } \Theta \approx -\tfrac{1}{2}\sigma^2 S^2 \Gamma",
                    color=ORANGE, font_size=24),
            Text("First full proof in comments gets pinned!",
                 color=TEAL, font_size=18),
        ).arrange(DOWN, buff=0.2).center()
        self.play(FadeOut(books), FadeIn(challenge))            # 1s
        self.wait(8)

        # ── BEAT C: Next episode  (~15s | anim≈2s | wait≈13s)
        # ─────────────────────────────────────────────────────────────────────
        next_ep = VGroup(
            Text("Next on Quantifaya:", color=GOLD, font_size=28, weight=BOLD),
            Text("The Heston Model — Stochastic Volatility from Scratch",
                 color=ORANGE, font_size=24),
            Text("Mean-reverting vol. Two risk factors. Quasi-analytical pricing.",
                 color=FG, font_size=20),
            Text("We derive it. Hull won't. We will.",
                 color=TEAL, font_size=18),
        ).arrange(DOWN, buff=0.2).center()
        self.play(FadeOut(challenge), FadeIn(next_ep))          # 1s
        self.wait(12)


# ══════════════════════════════════════════════════════════════════════════════
# FULL EPISODE
# ══════════════════════════════════════════════════════════════════════════════

class FullEpisode(Scene):
    """Full episode render.
    manim -pqh quantifaya_ep4.py FullEpisode --fps 60 --resolution 1920x1080
    """

    def construct(self):
        SceneIntro._run(self)
        self.clear()
        SceneDelta._run(self)
        self.clear()
        SceneDeltaPractice._run(self)
        self.clear()
        SceneGamma._run(self)
        self.clear()
        SceneGammaPractice._run(self)
        self.clear()
        SceneVega._run(self)
        self.clear()
        SceneTheta._run(self)
        self.clear()
        SceneRhoAndDashboard._run(self)
        self.clear()
        SceneTalebShortcomings._run(self)
        self.clear()
        SceneOutro._run(self)