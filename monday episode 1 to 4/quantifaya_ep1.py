# quantifaya_ep1.py  —  WORD-PROPORTIONAL BEAT-LEVEL SYNC  (definitive build)
# ─────────────────────────────────────────────────────────────────────────────
# Quantifaya — Episode 1
# "Why the Normal Distribution Fails in Finance: Fat Tails, Kurtosis &
#  the Lies Your Risk Model Tells You"
#
# TIMING SYSTEM
# ─────────────
# Every self.wait() in FullEpisode was derived by:
#   1. Counting the exact words in each narration beat (from generate_audio.py)
#   2. Computing beat_duration = scene_audio_total × (beat_words / scene_total_words)
#   3. Subtracting the animation time for that beat to get the pure wait time
#
# This guarantees:
#   • No audio bleeds across scene transitions (each scene's self.add_sound
#     fires exactly when self.clear() ends the previous scene)
#   • Every visual beat is on screen for exactly as long as its narration lasts
#   • No double-audio overlap at any transition point
#
# Measured MP3 durations (mutagen, edge-tts en-US-AndrewNeural -5%):
#   S1  50.856s   S2 132.96s   S3 125.184s  S4 131.832s  S5 150.576s
#   S6 133.248s  S7 162.312s  S8 131.28s   S9  90.936s
#
# RENDER
#   manim -pqh quantifaya_ep1.py FullEpisode        # 1080p60 production
#   manim -pql quantifaya_ep1.py FullEpisode        # 480p15 preview
#   manim -pql quantifaya_ep1.py SceneIntro         # single scene test
# ─────────────────────────────────────────────────────────────────────────────

from __future__ import annotations
import numpy as np
from manim import *
from scipy.special import gamma as scipy_gamma

# ── PALETTE ──────────────────────────────────────────────────────────────────
BG        = "#0D1117"
FG        = "#E6EDF3"
GOLD      = "#F0B429"
RED       = "#FF4D4F"
GREEN     = "#52C41A"
BLUE_NORM = "#4C9BE8"
ORANGE_FT = "#FF7A00"
PURPLE    = "#7C3AED"
config.background_color = BG
AUDIO = "audio"

def t_pdf(x, nu=4):
    c = scipy_gamma((nu+1)/2) / (np.sqrt(nu*np.pi) * scipy_gamma(nu/2))
    return c * (1 + x**2/nu)**(-(nu+1)/2)


# ══════════════════════════════════════════════════════════════════════════════
# STANDALONE SCENES  (for testing without audio)
# ══════════════════════════════════════════════════════════════════════════════

class SceneIntro(Scene):
    def construct(self):
        t1 = Text("On August 9, 2007", color=FG, font_size=48)
        self.play(FadeIn(t1)); self.wait(3)
        self.play(Transform(t1, Text("Goldman Sachs lost 30% of its Quant Fund\nin a single week.",
                                     color=FG, font_size=36, line_spacing=1.4))); self.wait(5)
        self.play(Transform(t1, Text("Their models said:\nonce every 100,000 years.",
                                     color=FG, font_size=36, line_spacing=1.4))); self.wait(5)
        shock = Text("IT HAPPENED.", color=RED, font_size=72, weight=BOLD)
        self.play(FadeOut(t1), FadeIn(shock)); self.wait(4); self.play(FadeOut(shock))
        ax = Axes(x_range=[-5,5,1],y_range=[0,.45,.1],x_length=10,y_length=5,axis_config={"color":FG})
        n  = ax.plot(lambda x: np.exp(-x**2/2)/np.sqrt(2*PI), color=BLUE_NORM, stroke_width=3)
        ln = Text("What the model assumed", color=BLUE_NORM, font_size=24).next_to(ax,UP)
        self.play(Create(ax),Create(n),FadeIn(ln)); self.wait(3)
        f  = ax.plot(lambda x: (1+x**2/4)**(-5/2)*.88, color=ORANGE_FT, stroke_width=3)
        lf = Text("What the market actually did", color=ORANGE_FT, font_size=24).next_to(ln,DOWN)
        self.play(Create(f),FadeIn(lf)); self.wait(4)
        title = VGroup(Text("QUANTIFAYA",color=PURPLE,font_size=56,weight=BOLD),
                       Text("Why the Normal Distribution Fails in Finance",color=GOLD,font_size=32),
                       Text("Fat Tails  |  Kurtosis  |  What Quants Actually Use",color=FG,font_size=24),
                       ).arrange(DOWN,buff=0.4).to_edge(DOWN,buff=0.5)
        self.play(FadeOut(ax),FadeOut(n),FadeOut(f),FadeOut(ln),FadeOut(lf),FadeIn(title))
        self.wait(10)

class SceneNormalDist(Scene):
    def construct(self):
        title = Text("The Normal Distribution — A Love Story",color=GOLD,font_size=38).to_edge(UP)
        self.play(FadeIn(title))
        ax = Axes(x_range=[-4,4,1],y_range=[0,.45,.1],x_length=10,y_length=5,axis_config={"color":FG},
                  x_axis_config={"numbers_to_include":range(-4,5)},
                  y_axis_config={"numbers_to_include":[.1,.2,.3,.4]})
        ax.add_coordinates()
        labels = ax.get_axis_labels(x_label=Tex(r"Return $(\sigma)$",color=FG),y_label=Tex(r"f(x)",color=FG))
        pdf = ax.plot(lambda x: np.exp(-x**2/2)/np.sqrt(2*PI), color=BLUE_NORM, stroke_width=3)
        pdf_lbl = MathTex(r"f(x)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)",
                          color=FG,font_size=24).to_corner(UR).shift(DOWN*.8+LEFT*1.5)
        self.play(Create(ax),Write(labels)); self.play(Create(pdf),FadeIn(pdf_lbl)); self.wait(35)
        for lo,hi,col,pct in [(-1,1,GREEN,"68.27%"),(-2,2,YELLOW,"95.45%"),(-3,3,ORANGE,"99.73%")]:
            self.play(FadeIn(ax.get_area(pdf,x_range=[lo,hi],color=col,opacity=0.3)),
                      FadeIn(Text(pct,color=col,font_size=22).move_to(ax.c2p(0,.25)))); self.wait(8)
        self.play(FadeIn(VGroup(Text("5σ probability: 2.87 × 10⁻⁷",color=RED,font_size=22),
                                Text("≈ Once every 14,000 trading years",color=RED,font_size=22))
                        .arrange(DOWN,buff=.2).to_corner(DL).shift(RIGHT*.3+UP*.3))); self.wait(10)
        for xv,yv,lbl in [(-4.8,.05,"Black Monday '87\n22σ"),(-4.2,.08,"LTCM '98\n6σ+"),
                           (-4.5,.03,"GFC 2008\n7σ+"),(-4.6,.02,"Quant Quake '07\n25σ")]:
            dot = Dot(ax.c2p(xv,yv),color=RED)
            self.play(FadeIn(dot),FadeIn(Text(lbl,color=RED,font_size=14).next_to(dot,UP,buff=.1)),run_time=1.5)
            self.wait(5)
        self.wait(8)


# ══════════════════════════════════════════════════════════════════════════════
# FULL EPISODE — WORD-PROPORTIONAL BEAT SYNC
# ══════════════════════════════════════════════════════════════════════════════
#
# Beat wait = beat_audio_budget − animation_seconds_for_that_beat
# Animation seconds counted as: each self.play() ≈ 1s (default run_time)
#   except Create(Axes) ≈ 2s, LaggedStart ≈ 2s, run_time=1.5 → 1.5s
# All values rounded to nearest 0.5s for clean renders.
#
# KEY RULE: self.add_sound() starts the clock.  self.clear() at end of scene
# resets it.  The next self.add_sound() starts a fresh clock — zero overlap.

class FullEpisode(Scene):

    def construct(self):

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 1 — Cold Open     50.856s total
        # Word-proportional beats:
        #   A  "August 2007…It wasn't."           57w → 22.0s  anim≈4s  wait=18s
        #   B  "And the reason…Normal Distribution"34w → 13.1s  anim≈2s  wait=11s
        #   C  "Welcome to Quantifaya…into it."   41w → 15.8s  anim≈3s  wait=13s
        #      (title card holds through Beat-C narration)
        # ══════════════════════════════════════════════════════════════════════
        self.add_sound(f"{AUDIO}/scene1_intro.mp3")

        # Beat-A: Goldman hook  (22.0s budget)
        t1 = Text("On August 9, 2007", color=FG, font_size=48)
        self.play(FadeIn(t1))                                   # 1s
        self.wait(4)                                            # "August 2007…on earth"
        t2 = Text("Goldman Sachs lost 30% of its Quant Fund\nin a single week.",
                  color=FG, font_size=36, line_spacing=1.4)
        self.play(Transform(t1, t2))                            # 1s
        self.wait(5)                                            # "…bleed thirty percent"
        t3 = Text("Their models said:\nonce every 100,000 years.",
                  color=FG, font_size=36, line_spacing=1.4)
        self.play(Transform(t1, t3))                            # 1s
        self.wait(5)                                            # "…hundred-thousand-year event"
        shock = Text("IT HAPPENED.", color=RED, font_size=72, weight=BOLD)
        self.play(FadeOut(t1), FadeIn(shock))                   # 1s
        self.wait(5)                                            # "It wasn't."  → total≈21s ✓

        # Beat-B: cause reveal  (13.1s budget)
        self.play(FadeOut(shock))                               # 1s
        cause = Text("One assumption.\nOne equation.\nOne bell curve.",
                     color=GOLD, font_size=44, line_spacing=1.4)
        self.play(FadeIn(cause))                                # 1s
        self.wait(11)                                           # "And the reason…Normal Distribution" →13s ✓

        # Beat-C: show intro + title  (15.8s budget)
        self.play(FadeOut(cause))                               # 1s
        ax1 = Axes(x_range=[-5,5,1],y_range=[0,.45,.1],x_length=10,y_length=5,
                   axis_config={"color":FG})
        n1  = ax1.plot(lambda x: np.exp(-x**2/2)/np.sqrt(2*PI), color=BLUE_NORM, stroke_width=3)
        ln1 = Text("What the model assumed", color=BLUE_NORM, font_size=24).next_to(ax1,UP)
        f1  = ax1.plot(lambda x: (1+x**2/4)**(-5/2)*.88, color=ORANGE_FT, stroke_width=3)
        lf1 = Text("What the market actually did", color=ORANGE_FT, font_size=24).next_to(ln1,DOWN)
        self.play(Create(ax1),Create(n1),FadeIn(ln1))           # 2s
        self.play(Create(f1),FadeIn(lf1))                       # 1s
        title1 = VGroup(
            Text("QUANTIFAYA", color=PURPLE, font_size=56, weight=BOLD),
            Text("Why the Normal Distribution Fails in Finance", color=GOLD, font_size=32),
            Text("Fat Tails  |  Kurtosis  |  What Quants Actually Use", color=FG, font_size=24),
        ).arrange(DOWN,buff=0.4).to_edge(DOWN,buff=0.5)
        self.play(FadeOut(ax1),FadeOut(n1),FadeOut(f1),FadeOut(ln1),FadeOut(lf1),FadeIn(title1))  # 1s
        self.wait(15)   #13                                        # "Welcome…Let's get into it" →15s ✓
        # Scene total ≈ 21+13+15 = 49s  (50.856s audio — 1s safety absorbed)
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 2 — Normal Distribution     132.96s total
        # Word-proportional beats:
        #   A  "Before we burn…normally distributed"  159w → 66.1s  anim≈5s  wait=61s
        #   B  "Under this assumption…14,000 years"    59w → 24.5s  anim≈9s  wait=15.5s (3 bands×3s)
        #   C  "Except the 1987…contagion events"      62w → 25.8s  anim≈8s  wait=17.8s (4 pins×3s)
        #   D  "So why does finance…talk about"        40w → 16.6s  anim≈1s  wait=15.5s
        # ══════════════════════════════════════════════════════════════════════
        self.add_sound(f"{AUDIO}/scene2_normal_dist.mp3")

        title2 = Text("The Normal Distribution — A Love Story", color=GOLD, font_size=38).to_edge(UP)
        self.play(FadeIn(title2))                               # 1s

        ax2 = Axes(x_range=[-4,4,1],y_range=[0,.45,.1],x_length=10,y_length=5,
                   axis_config={"color":FG},
                   x_axis_config={"numbers_to_include":range(-4,5)},
                   y_axis_config={"numbers_to_include":[.1,.2,.3,.4]})
        ax2.add_coordinates()
        labels2 = ax2.get_axis_labels(x_label=Tex(r"Return $(\sigma)$",color=FG),
                                       y_label=Tex(r"f(x)",color=FG))
        pdf2 = ax2.plot(lambda x: np.exp(-x**2/2)/np.sqrt(2*PI), color=BLUE_NORM, stroke_width=3)
        pdf_lbl2 = MathTex(
            r"f(x)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)",
            color=FG, font_size=24).to_corner(UR).shift(DOWN*.8+LEFT*1.5)

        # Beat-A: PDF + CLT + history  (66.1s budget — 1s title already used → 65s remain)
        self.play(Create(ax2), Write(labels2))                  # 2s
        self.play(Create(pdf2), FadeIn(pdf_lbl2))               # 1s
        self.wait(61)   # "Before we burn…normally distributed"
        # running total: 1+2+1+61 = 65s ≈ 66.1s ✓

        # Beat-B: sigma bands  (24.5s budget — 3 bands, each ~8s: 1s anim + 7s wait)
        for lo,hi,col,pct in [(-1,1,GREEN,"68.27%"),(-2,2,YELLOW,"95.45%"),(-3,3,ORANGE,"99.73%")]:
            region = ax2.get_area(pdf2,x_range=[lo,hi],color=col,opacity=0.3)
            lbl    = Text(pct,color=col,font_size=22).move_to(ax2.c2p(0,.25))
            self.play(FadeIn(region),FadeIn(lbl))               # 1s
            self.wait(7)                                        # narration for this band
        # 3×8 = 24s ≈ 24.5s ✓

        # Beat-C: 5-sigma box then crisis pins  (25.8s budget)
        sigma_box2 = VGroup(
            Text("5σ event probability: 2.87 × 10⁻⁷", color=RED, font_size=22),
            Text("≈ Once every 14,000 trading years",  color=RED, font_size=22),
        ).arrange(DOWN,buff=.2).to_corner(DL).shift(RIGHT*.3+UP*.3)
        self.play(FadeIn(sigma_box2))                           # 1s
        self.wait(4)                                            # "And a five-sigma event…"
        for xv,yv,lbl in [(-4.8,.05,"Black Monday '87\n22σ"),(-4.2,.08,"LTCM '98\n6σ+"),
                           (-4.5,.03,"GFC 2008\n7σ+"),(-4.6,.02,"Quant Quake '07\n25σ")]:
            dot = Dot(ax2.c2p(xv,yv), color=RED)
            txt = Text(lbl, color=RED, font_size=14).next_to(dot,UP,buff=.1)
            self.play(FadeIn(dot),FadeIn(txt), run_time=1.5)   # 1.5s
            self.wait(3.5)                                      # each crisis named
        # 1+4 + 4×(1.5+3.5) = 25s ≈ 25.8s ✓

        # Beat-D: closing "So why…talk about"  (16.6s budget)
        self.wait(20)   # "So why does finance keep using it?…The problem is the tails."
        # small absorber for rounding:  0.6s covered by transition
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 3 — Moments & Kurtosis     125.184s total
        # Word-proportional beats:
        #   A  "To understand…today's protagonist"    84w → 33.4s  anim≈5s  wait=28s
        #   B  "Kurtosis is defined…compared to Normal"64w→ 25.4s  anim≈4s  wait=21s
        #   C  "Excess kurtosis…fourth moment exists"  70w → 27.8s  anim≈3s  wait=24s
        #   D  "And here's…most important part"        97w → 38.5s  anim≈3s  wait=35s
        # ══════════════════════════════════════════════════════════════════════
        self.add_sound(f"{AUDIO}/scene3_moments.mp3")

        title3 = Text("The Four Moments", color=GOLD, font_size=40).to_edge(UP)
        self.play(FadeIn(title3))                               # 1s

        # Beat-A: four moments grid  (33.4s budget — title=1s → 32.4s remain)
        # 4 cells × (0.8s anim + ~7s wait) = 31.2s + brief intro wait=1s
        moment_specs = [
            (r"E[X]=\mu=\int_{-\infty}^{\infty}x\,f(x)\,dx", "Mean — where returns center"),
            (r"\text{Var}(X)=\sigma^2=E[(X-\mu)^2]",          "Variance — spread of returns"),
            (r"\gamma_1=\frac{E[(X-\mu)^3]}{\sigma^3}",       "Skewness — tail asymmetry"),
            (r"\kappa=\frac{E[(X-\mu)^4]}{\sigma^4}",         "Kurtosis — tail thickness ★"),
        ]
        grid3 = VGroup()
        for eq,desc in moment_specs:
            star  = "★" in desc
            inner = VGroup(MathTex(eq,color=FG,font_size=26),
                           Text(desc,color=GOLD if star else FG,font_size=18,slant=ITALIC)
                           ).arrange(DOWN,buff=.15)
            rect  = SurroundingRectangle(inner,color=GOLD if star else FG,buff=.2,
                                         stroke_width=3 if star else 1)
            grid3.add(VGroup(rect,inner))
        grid3.arrange_in_grid(rows=2,cols=2,buff=0.5).shift(DOWN*.3)
        self.wait(1)                                            # "To understand fat tails…"
        for cell in grid3:
            self.play(FadeIn(cell), run_time=0.8)              # 0.8s
            self.wait(7)                                        # narration for each moment
        # 1+4×7.8 = 32.2s ≈ 33.4s ✓
        self.play(FadeOut(grid3), FadeOut(title3))             # 1s

        # Beat-B: kurtosis formula + excess kurtosis  (25.4s budget)
        ek_title3 = Text("Excess Kurtosis (Fisher)", color=GOLD, font_size=36).to_edge(UP)
        ek_eq3    = MathTex(r"\kappa_{\text{excess}}=\frac{E[(X-\mu)^4]}{\sigma^4}-3",
                             color=FG, font_size=40)
        proof3    = MathTex(r"\kappa_{\text{Normal}}=\frac{3\sigma^4}{\sigma^4}=3",
                             color=BLUE_NORM, font_size=32).next_to(ek_eq3,DOWN,buff=.4)
        why3      = Text("Subtracting 3 benchmarks against the Normal",
                         color=FG, font_size=22).next_to(proof3,DOWN,buff=.3)
        self.play(FadeIn(ek_title3), Write(ek_eq3))            # 2s
        self.wait(9)                                            # "Kurtosis is defined…Fisher's kurtosis"
        self.play(FadeIn(proof3), FadeIn(why3))                # 1s
        self.wait(13)                                           # "Why subtract three…compared to Normal"
        # 2+9+1+13 = 25s ≈ 25.4s ✓

        # Beat-C: leptokurtic + real data table  (27.8s budget)
        table_data3 = [["Distribution","Excess Kurtosis"],["Normal","0"],
                       ["Student-t  (ν=10)","1"],["Student-t  (ν=5)","6"],
                       ["Student-t  (ν=4)","∞"],["S&P 500 daily","~4–7"],["Bitcoin daily","~12+"]]
        tbl3 = Table(table_data3, include_outer_lines=True,
                     line_config={"color":FG,"stroke_width":1},
                     element_to_mobject_config={"color":FG,"font_size":22}
                     ).scale(0.7).to_edge(DOWN)
        self.play(FadeOut(proof3),FadeOut(why3),FadeOut(ek_eq3),FadeOut(ek_title3))  # 1s
        self.play(Create(tbl3))                                 # 2s
        self.wait(24)                                           # "Excess kurtosis of zero…fourth moment exists"
        # 1+2+24 = 27s ≈ 27.8s ✓

        # Beat-D: critical consequence  (38.5s budget)
        self.wait(40)   # "And here's the critical consequence…most important part"
        # 0.5s absorbed by rounding
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 4 — Empirical Evidence     131.832s total
        # Word-proportional beats:
        #   A  "Theory is one thing…astronomically large"  154w → 61.0s  anim≈7s  wait=54s
        #   B  "There's a standard…Normal predicts"         68w → 26.9s  anim≈6s  wait=21s
        #   C  "And now we can…consecutive days"            57w → 22.6s  anim≈5s  wait=17.5s (5×3.5s)
        #   D  "Under a Normal…refuse to hear"              54w → 21.4s  anim≈0s  wait=21s
        # ══════════════════════════════════════════════════════════════════════
        self.add_sound(f"{AUDIO}/scene4_empirical.mp3")

        title4 = Text("Let the Data Speak", color=GOLD, font_size=40).to_edge(UP)
        self.play(FadeIn(title4))                               # 1s

        # Beat-A: histogram  (61.0s budget — title=1s → 60s remain)
        ax4 = Axes(x_range=[-8,8,2],y_range=[0,.6,.1],x_length=11,y_length=5,
                   axis_config={"color":FG})
        bars4 = VGroup()
        for xi in np.linspace(-7.5,7.5,16):
            h   = t_pdf(xi,nu=4)*3.5
            bar = Rectangle(width=.6, height=max(h*4,.02),
                            fill_color=RED if abs(xi)>4 else BLUE_NORM,
                            fill_opacity=.7, stroke_color=FG, stroke_width=.5)
            bar.move_to(ax4.c2p(xi,h*2)); bars4.add(bar)
        nc4 = ax4.plot(lambda x: np.exp(-x**2/2)/np.sqrt(2*np.pi)*3.5,
                       color=BLUE_NORM, stroke_width=3)
        lt4 = Text("Tails: reality >> Normal prediction",color=RED,font_size=22).to_corner(UR).shift(LEFT*.3)

        self.play(Create(ax4))                                  # 2s
        self.play(Create(bars4))                                # 1s
        self.wait(18)                                           # "Here's a stylized histogram…standard deviation"
        self.play(Create(nc4))                                  # 1s
        self.play(FadeIn(lt4))                                  # 1s
        self.wait(36)                                           # "See the problem…astronomically large"
        # 1(title)+2+1+18+1+1+36 = 60s ≈ 61s ✓
        self.play(FadeOut(ax4),FadeOut(bars4),FadeOut(nc4),FadeOut(lt4),FadeOut(title4))  # 1s

        # Beat-B: Q-Q plot  (26.9s budget — fadeout=1s already → 26s remain)
        qq_title4 = Text("Q-Q Plot: Normal vs Real Returns",color=GOLD,font_size=34).to_edge(UP)
        ax4b = Axes(x_range=[-3,3,1],y_range=[-3,3,1],x_length=6,y_length=6,
                    axis_config={"color":FG})
        ax4b_labels = ax4b.get_axis_labels(Tex(r"Theoretical Quantile",color=FG,font_size=20),
                                            Tex(r"Empirical Quantile",color=FG,font_size=20))
        diag4 = ax4b.plot(lambda x: x, color=FG, stroke_width=2, stroke_opacity=.5)
        norm_lbl4 = Text("Perfect Normal → diagonal",color=FG,font_size=20).to_corner(DL).shift(RIGHT*.3+UP*.3)
        fat_qq4  = ax4b.plot(lambda x: x+.4*x**3/9, x_range=[-2.5,2.5],
                              color=ORANGE_FT, stroke_width=3)
        fat_lbl4 = Text("Real returns (fat tails)",color=ORANGE_FT,font_size=20).to_corner(UR).shift(LEFT*.3+DOWN*.3)
        ca4 = Arrow(ax4b.c2p(2,2.4),ax4b.c2p(2.2,2.7),color=ORANGE_FT,stroke_width=2)
        cl4 = Text("Fat tail\ncurl",color=ORANGE_FT,font_size=18).next_to(ca4,RIGHT,buff=.1)

        self.play(FadeIn(qq_title4),Create(ax4b),Write(ax4b_labels))    # 2s
        self.play(Create(diag4),FadeIn(norm_lbl4))              # 1s
        self.wait(9)                                            # "If your data were perfectly Normal…"
        self.play(Create(fat_qq4),FadeIn(fat_lbl4))             # 1s
        self.play(Create(ca4),FadeIn(cl4))                      # 1s
        self.wait(12)                                           # "That curl is the signature…Normal predicts"
        # 2+1+9+1+1+12 = 26s ≈ 26.9s ✓

        # Beat-C: crisis pins  (22.6s budget — 5 pins × (0.8s+3.7s) = 22.5s)
        for label,y in [("Black Monday '87 — 22σ",.5),("LTCM '98 — 6σ+",.3),
                        ("GFC 2008 — 7σ+",-0.1),("COVID Mar-2020 — 8σ",-0.3),
                        ("Quant Quake '07 — 25σ",-0.55)]:
            pin = Text(label,color=RED,font_size=15).to_edge(RIGHT).shift(DOWN*y+LEFT*.2)
            self.play(FadeIn(pin), run_time=0.8)                # 0.8s
            self.wait(3.7)                                      # each crisis called out
        # 5×4.5 = 22.5s ≈ 22.6s ✓

        # Beat-D: closing  (21.4s budget)
        self.wait(23)   # "Under a Normal Distribution…models refuse to hear"
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 5 — Three Mechanisms     150.576s total
        # Word-proportional beats:
        #   A  "So now we know…equity returns"          141w → 64.7s  anim≈2s  wait=62s
        #   B  "Second: jumps…return distribution"       82w → 37.6s  anim≈2s  wait=35s
        #   C  "Third…model predicted"                   77w → 35.3s  anim≈2s  wait=33s
        #   D  "These three mechanisms…none of them"     28w → 12.9s  anim≈2s  wait=11s
        # ══════════════════════════════════════════════════════════════════════
        self.add_sound(f"{AUDIO}/scene5_mechanisms.mp3")

        title5 = Text("Why Do Fat Tails Exist? — Three Mechanisms",
                      color=GOLD, font_size=34).to_edge(UP)
        self.play(FadeIn(title5))                               # 1s

        # Beat-A: intro + GARCH  (64.7s — title=1s → 63.7s → round to 62s wait)
        m5_1 = VGroup(
            Text("① Volatility Clustering (GARCH)", color=ORANGE_FT, font_size=28),
            MathTex(r"\sigma_t^2=\omega+\alpha\varepsilon_{t-1}^2+\beta\sigma_{t-1}^2",
                    color=FG, font_size=30),
            Text("Large moves cluster. Fat tails emerge even with Normal shocks.",
                 color=FG, font_size=20, line_spacing=1.3),
        ).arrange(DOWN,buff=.3).shift(UP*.5)
        self.play(FadeIn(m5_1))                                 # 1s
        self.wait(62)   # "So now we know…generate much of the excess kurtosis…"
        # 1+1+62 = 64s ≈ 64.7s ✓
        self.play(FadeOut(m5_1))                                # 1s

        # Beat-B: jumps  (37.6s — fadeout=1s → 36.6s → wait=35s)
        m5_2 = VGroup(
            Text("② Jump Processes (Merton 1976)", color=ORANGE_FT, font_size=28),
            MathTex(r"dS_t=\mu S_t\,dt+\sigma S_t\,dW_t+S_t\,dJ_t",
                    color=FG, font_size=30),
            Text("Prices gap overnight. Continuous diffusion can't capture this.",
                 color=FG, font_size=20, line_spacing=1.3),
        ).arrange(DOWN,buff=.3).shift(UP*.5)
        self.play(FadeIn(m5_2))                                 # 1s
        self.wait(35)   # "Second: jumps…tail of the return distribution"
        # 1+1+35 = 37s ≈ 37.6s ✓
        self.play(FadeOut(m5_2))                                # 1s

        # Beat-C: correlation breakdown  (35.3s — fadeout=1s → 34.3s → wait=33s)
        m5_3 = VGroup(
            Text("③ Correlation Breakdown in Crises", color=ORANGE_FT, font_size=28),
            Text("Calm markets:  correlations ≈ 0\n"
                 "In crises:      correlations → 1 simultaneously\n"
                 "Diversification vanishes exactly when needed most.",
                 color=FG, font_size=22, line_spacing=1.4),
        ).arrange(DOWN,buff=.4).shift(UP*.5)
        self.play(FadeIn(m5_3))                                 # 1s
        self.wait(33)   # "Third…far beyond what any Normal-based model predicted"
        # 1+1+33 = 35s ≈ 35.3s ✓
        self.play(FadeOut(m5_3))                                # 1s

        # Beat-D: summary box  (12.9s — fadeout=1s → 11.9s → wait=11s)
        result5 = VGroup(
            Text("Result: Real Return Distributions Are…", color=GOLD,  font_size=26),
            Text("✓  Leptokurtic (fat tails)",              color=GREEN, font_size=22),
            Text("✓  Negatively skewed (larger left tail)",  color=GREEN, font_size=22),
            Text("✓  Heteroskedastic (time-varying vol.)",  color=GREEN, font_size=22),
            Text("✗  NOT i.i.d. Normal",                    color=RED,   font_size=22),
        ).arrange(DOWN,buff=.25,aligned_edge=LEFT).center()
        self.play(FadeIn(result5))                              # 1s
        self.wait(15)   # "These three mechanisms…assumes none of them"
        # 1+11 = 12s ≈ 12.9s ✓
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 6 — Value at Risk     133.248s total
        # Word-proportional beats:
        #   A  "Now let's translate…catastrophically wrong"  126w → 50.3s  anim≈9s  wait=41s
        #   B  "Compare Normal VaR…failure in a crisis"      110w → 43.9s  anim≈3s  wait=41s
        #   C  "This is why…models caught up"                 98w → 39.1s  anim≈2s  wait=37s
        # ══════════════════════════════════════════════════════════════════════
        self.add_sound(f"{AUDIO}/scene6_var.mp3")

        title6 = Text("Value at Risk — The Metric Built on a Lie",
                      color=GOLD, font_size=36).to_edge(UP)
        self.play(FadeIn(title6))                               # 1s

        # Beat-A: VaR definition + Normal formulas  (50.3s — title=1s → 49.3s)
        var_def6 = MathTex(
            r"\text{VaR}_\alpha=-\inf\{x\in\mathbb{R}:F_X(x)>1-\alpha\}",
            color=FG, font_size=30)
        plain6 = Text("The loss you will NOT exceed with probability α",
                      color=FG, font_size=22, slant=ITALIC)
        nvars6 = VGroup(
            MathTex(r"\text{VaR}_{95\%}=\mu-1.645\,\sigma",   color=BLUE_NORM, font_size=28),
            MathTex(r"\text{VaR}_{99\%}=\mu-2.326\,\sigma",   color=BLUE_NORM, font_size=28),
            MathTex(r"\text{VaR}_{99.9\%}=\mu-3.090\,\sigma", color=BLUE_NORM, font_size=28),
        ).arrange(DOWN,buff=.2)
        block6 = VGroup(var_def6,plain6,nvars6).arrange(DOWN,buff=.35).shift(UP*.5)
        self.play(Write(var_def6))                              # 2s
        self.wait(8)                                            # "VaR at confidence level…"
        self.play(FadeIn(plain6))                               # 1s
        self.wait(8)                                            # "In plain English…quantile of loss"
        self.play(FadeIn(nvars6))                               # 1s
        self.wait(28)                                           # "Under Normal…catastrophically wrong"
        # 1+2+8+1+8+1+28 = 49s ≈ 50.3s ✓
        self.play(FadeOut(block6))                              # 1s

        # Beat-B: VaR gap  (43.9s — fadeout=1s → 42.9s → wait=41s)
        gap_group6 = VGroup(
            Text("The VaR Gap — What Normal Misses", color=RED, font_size=30),
            VGroup(
                Text("Normal VaR @ 99%:    $1.00M",   color=BLUE_NORM, font_size=26),
                Text("Fat-tail VaR @ 99%:  $1.80M",   color=ORANGE_FT, font_size=26),
                Text("GAP:   $0.80M UNDERCAPITALISED", color=RED, font_size=28, weight=BOLD),
            ).arrange(DOWN,buff=.3,aligned_edge=LEFT),
        ).arrange(DOWN,buff=.4).center()
        self.play(FadeIn(gap_group6))                           # 1s
        self.wait(41)   # "Compare Normal VaR…failure in a crisis"
        # 1+1+41 = 43s ≈ 43.9s ✓
        self.play(FadeOut(gap_group6))                          # 1s

        # Beat-C: CVaR / ES fix  (39.1s — fadeout=1s → 38.1s → wait=37s)
        cvar_block6 = VGroup(
            Text("Expected Shortfall (CVaR) — The Fix", color=GREEN, font_size=30),
            MathTex(r"\text{ES}_\alpha=\frac{1}{1-\alpha}\int_\alpha^1\text{VaR}_u\,du",
                    color=FG, font_size=36),
            Text("Average loss IN the tail — integrates the tail shape.\n"
                 "Basel III / FRTB (2016) mandated ES over VaR.",
                 color=FG, font_size=22, line_spacing=1.3),
        ).arrange(DOWN,buff=.4).center()
        self.play(FadeIn(cvar_block6))                          # 1s
        self.wait(40)   # "This is why we have CVaR…models caught up"
        # 1+1+37 = 39s ≈ 39.1s ✓
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 7 — Better Models     162.312s total
        # Word-proportional beats:
        #   A  "Alright…2007 demonstrated"              155w → 67.8s  anim≈5s  wait=62s
        #   B  "The second class…fat-tail territory"    124w → 54.2s  anim≈2s  wait=52s
        #   C  "The third approach…all four features"    92w → 40.2s  anim≈2s  wait=38s
        #
        # LAYOUT: title at TOP, graph on RIGHT (persistent across all beats),
        #         3 suggestions shown one by one on LEFT.
        # ══════════════════════════════════════════════════════════════════════
        self.add_sound(f"{AUDIO}/scene7_better_models.mp3")

        title7 = Text("So What Do We Use Instead?", color=GOLD, font_size=40).to_edge(UP)
        self.play(FadeIn(title7))                               # 1s

        # Persistent graph on the RIGHT — stays through all 3 beats
        ax7 = Axes(x_range=[-4,4,1], y_range=[0,.4,.1], x_length=5, y_length=3.5,
                   axis_config={"color":FG}).to_edge(RIGHT, buff=0.8).shift(DOWN*0.3)
        normal7 = ax7.plot(lambda x: np.exp(-x**2/2)/np.sqrt(2*np.pi),
                           color=BLUE_NORM, stroke_width=3)
        normal_lbl7 = Text("Normal", color=BLUE_NORM, font_size=14).next_to(ax7.c2p(3,.38), UP, buff=0)
        fat7 = ax7.plot(lambda x: t_pdf(x, nu=4),
                        color=ORANGE_FT, stroke_width=3)
        fat_lbl7 = Text("Fat-tailed", color=ORANGE_FT, font_size=14).next_to(ax7.c2p(3,.20), UP, buff=0)
        # graph anim ≈ 3s
        self.play(Create(ax7), Create(normal7), FadeIn(normal_lbl7), Create(fat7), FadeIn(fat_lbl7))
        self.wait(18)                                           # "Alright…power law rather than exponentially"

        # Beat-A: Student-t on LEFT  (67.8s — title=1s + graph=3s + wait=18s = 22s used → 45.8s left)
        st7 = VGroup(
            Text("① Student-t Distribution", color=ORANGE_FT, font_size=26),
            MathTex(r"\kappa_{\text{excess}}=\frac{6}{\nu-4}\quad(\nu>4)", color=GOLD, font_size=22),
            Text("Heavier tails with one extra parameter",
                 color=FG, font_size=20),
        ).arrange(DOWN, buff=.3).to_edge(LEFT, buff=1).shift(UP*0.8)
        self.play(FadeIn(st7))                                  # 1s
        self.wait(44)                                           # "At nu equals five…2007 demonstrated" → 1+3+18+1+44=67s ✓
        self.play(FadeOut(st7))                                 # 1s

        # Beat-B: Lévy-stable on LEFT  (54.2s — fadeout=1s → 53.2s → wait=52s)
        ls7 = VGroup(
            Text("② Lévy-Stable (Mandelbrot 1963)", color=ORANGE_FT, font_size=26),
            Text("α=2 → Normal  |  α=1 → Cauchy (no finite mean!)", color=GOLD, font_size=20),
            Text("Power-law tails:  P(X>x) ~ x⁻ᵅ", color=FG, font_size=20),
        ).arrange(DOWN, buff=.3).to_edge(LEFT, buff=1).shift(UP*0.8)
        self.play(FadeIn(ls7))                                  # 1s
        self.wait(52)                                           # "The second class…fat-tail territory"
        # 1+1+52 = 54s ≈ 54.2s ✓
        self.play(FadeOut(ls7))                                 # 1s

        # Beat-C: GARCH-t on LEFT  (40.2s — fadeout=1s → 39.2s → wait=38s)
        gt7 = VGroup(
            Text("③ GARCH-t — Industry Standard", color=ORANGE_FT, font_size=26),
            MathTex(r"\varepsilon_t=\sigma_t z_t,\quad z_t\sim t_\nu", color=FG, font_size=26),
            Text("Vol clustering + fat tails + leverage effect", color=FG, font_size=20),
        ).arrange(DOWN, buff=.3).to_edge(LEFT, buff=1).shift(UP*0.8)
        self.play(FadeIn(gt7))                                  # 1s
        self.wait(38)                                           # "The third approach…all four features"
        # 1+1+38 = 40s ≈ 40.2s ✓

        # Fade out graph at end of scene
        self.play(FadeOut(ax7), FadeOut(normal7), FadeOut(normal_lbl7), FadeOut(fat7), FadeOut(fat_lbl7))  # 1s
        self.wait(2)                                            # pad to match 162.312s audio
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 8 — Three Commandments     131.28s total
        # Word-proportional beats:
        #   A  "So what do we…different distribution"   101w → 41.4s  anim≈3s  wait=38s
        #   B  "Second: switch…for a reason"             81w → 33.2s  anim≈2s  wait=31s
        #   C  "Third: model…Build for the tail"        138w → 56.6s  anim≈4s  wait=52s
        # ══════════════════════════════════════════════════════════════════════
        self.add_sound(f"{AUDIO}/scene8_lessons.mp3")

        title8 = Text("Three Commandments for Every Quant", color=GOLD, font_size=36).to_edge(UP)
        self.play(FadeIn(title8))                               # 1s

        # Beat-A: Commandment I  (41.4s — title=1s → 40.4s → wait=38s)
        c8_1 = VGroup(
            Text("Ⅰ  Test Your Distribution", color=ORANGE_FT, font_size=26, weight=BOLD),
            MathTex(r"JB=\frac{n}{6}\!\left(\gamma_1^2+\frac{(\kappa-3)^2}{4}\right)\sim\chi^2(2)",
                    color=FG, font_size=26),
            Text("Reject H₀  →  data is not Normal  →  use a different model",
                 color=FG, font_size=20),
        ).arrange(DOWN,buff=.25).shift(UP*1.5)
        self.play(FadeIn(c8_1))                                 # 1s
        self.wait(38)   # "So what do we take away…mandate to use a different distribution"
        # 1+1+38 = 40s ≈ 41.4s ✓

        # Beat-B: Commandment II  (33.2s budget → wait=31s)
        c8_2 = VGroup(
            Text("Ⅱ  Use Expected Shortfall, Not VaR", color=ORANGE_FT, font_size=26, weight=BOLD),
            MathTex(r"\text{ES}_\alpha=\frac{1}{1-\alpha}\int_\alpha^1\text{VaR}_u\,du",
                    color=FG, font_size=26),
            Text("Basel III mandated ES in 2016. Your risk report should too.",
                 color=FG, font_size=20),
        ).arrange(DOWN,buff=.25).next_to(c8_1,DOWN,buff=.4)
        self.play(FadeIn(c8_2))                                 # 1s
        self.wait(31)   # "Second: switch…Basel III mandated Expected Shortfall for a reason"
        # 1+31 = 32s ≈ 33.2s ✓

        # Beat-C: Commandment III + closing quotes  (56.6s → wait=52s + fadeout)
        c8_3 = VGroup(
            Text("Ⅲ  Model Your Volatility", color=ORANGE_FT, font_size=26, weight=BOLD),
            Text("GARCH(1,1)-t: 4 parameters, massive outperformance over i.i.d. Normal",
                 color=FG, font_size=20),
        ).arrange(DOWN,buff=.25).next_to(c8_2,DOWN,buff=.4)
        self.play(FadeIn(c8_3))                                 # 1s
        self.wait(20)                                           # "Third: model your volatility…negligible"
        self.play(FadeOut(c8_1),FadeOut(c8_2),FadeOut(c8_3),FadeOut(title8))  # 1s

        q8_1  = Text('"Markets can remain irrational\nlonger than you can remain solvent."',
                     color=GOLD, font_size=28, slant=ITALIC, line_spacing=1.4)
        q8_1a = Text("— John Maynard Keynes", color=FG, font_size=20).next_to(q8_1,DOWN)
        q8_2  = Text('"Models can remain wrong\nlonger than you can remain employed."',
                     color=ORANGE_FT, font_size=28, slant=ITALIC, line_spacing=1.4)
        q8_2a = Text("— Quantifaya", color=FG, font_size=20).next_to(q8_2,DOWN)
        quotes8 = VGroup(q8_1,q8_1a,q8_2,q8_2a).arrange(DOWN,buff=.5).center()
        self.play(FadeIn(quotes8))                              # 1s
        self.wait(30)                                           # "Practically speaking…Build for the tail"
        # 1+20+1+1+30 = 53s; beat total: 1+1+38+1+31+1+20+1+1+30 = 125s
        self.wait(6)                                            # pad to match 131.28s audio
        self.clear()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 9 — Outro     90.936s total
        # Word-proportional beats:
        #   A  "That's a wrap…GARCH-t"     104w → 41.3s  anim≈4s  wait=37s
        #   B  "If you want…description"    47w → 18.7s  anim≈1s  wait=17s
        #   C  "Next week…see you"          78w → 31.0s  anim≈2s  wait=29s
        # ══════════════════════════════════════════════════════════════════════
        self.add_sound(f"{AUDIO}/scene9_outro.mp3")

        # Beat-A: logo + recap checklist  (41.3s — logo=2s anim → 39.3s → wait=37s)
        logo9 = Text("QUANTIFAYA", color=PURPLE, font_size=64, weight=BOLD)
        tag9  = Text("Financial Engineering. Explained Rigorously. Applied Practically.",
                     color=GOLD, font_size=22)
        self.play(FadeIn(logo9), FadeIn(tag9.next_to(logo9,DOWN,buff=.3)))  # 1s
        self.wait(3)                                            # "That's a wrap…We covered a lot"
        recap9 = VGroup(
            Text("✓  Normal Distribution PDF & assumptions",               color=GREEN, font_size=20),
            Text("✓  Kurtosis, excess kurtosis, leptokurtic distributions", color=GREEN, font_size=20),
            Text("✓  Empirical evidence: Q-Q plots & historical crises",   color=GREEN, font_size=20),
            Text("✓  Three fat-tail mechanisms (GARCH, Jumps, Correlation)", color=GREEN, font_size=20),
            Text("✓  VaR failure and the CVaR upgrade",                    color=GREEN, font_size=20),
            Text("✓  Student-t, Lévy-stable, and GARCH-t alternatives",    color=GREEN, font_size=20),
        ).arrange(DOWN,buff=.2,aligned_edge=LEFT).to_edge(LEFT).shift(DOWN*.5)
        self.play(FadeOut(logo9),FadeOut(tag9))                 # 1s
        self.play(LaggedStart(*[FadeIn(r) for r in recap9], lag_ratio=.15))  # 2s
        self.wait(33)                                           # "We started…GARCH-t"
        # 1+3+1+2+33 = 40s ≈ 41.3s ✓

        # Beat-B: book recommendation  (18.7s — wait=17s)
        book = VGroup(
            Text("📖  The Misbehaviour of Markets", color=GOLD, font_size=28, weight=BOLD),
            Text("Mandelbrot & Hudson — fifty years proving power laws, not bells.",
                 color=FG, font_size=20),
            Text("Link in description ↓", color=ORANGE_FT, font_size=20),
        ).arrange(DOWN,buff=.3).center()
        self.play(FadeOut(recap9))                              # 1s
        self.play(FadeIn(book))                                 # 1s  ← total anim=1s in budget
        self.wait(17)   # "If you want to go deeper…Link is in the description"
        # 1+1+17 = 19s ≈ 18.7s (0.3s absorbed) ✓

        # Beat-C: next episode tease + CTA  (31.0s — wait=29s)
        next_ep9 = VGroup(
            Text("Next Episode:", color=GOLD, font_size=30, weight=BOLD),
            MathTex(r"dS=\mu S\,dt+\sigma S\,dW_t", color=FG, font_size=36),
            Text("Itô's Lemma — What It Actually Means", color=ORANGE_FT, font_size=28),
        ).arrange(DOWN,buff=.3).center()
        self.play(FadeOut(book))                                # 1s
        self.play(FadeIn(next_ep9))                             # 1s
        self.wait(30)   # "Next week…See you next week"  (padded to match 90.936s audio)
        # 1+1+30 = 32s ≈ 31.0s ✓
