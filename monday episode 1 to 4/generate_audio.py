"""
generate_audio.py
─────────────────────────────────────────────────────────────────────────────
Quantifaya Episode 1 — Voice-over generator
Uses edge-tts with en-US-AndrewNeural (warm, authoritative, educational).

After generating all MP3s this script writes audio/timing_manifest.json with
the EXACT duration of every audio file in seconds.  quantifaya_ep1.py reads
that manifest at render-time so every scene's self.wait() is calibrated to
the real audio — not a hand-waved estimate.

Usage:
    pip install edge-tts mutagen
    python generate_audio.py

Output:
    audio/scene1_intro.mp3  …  audio/scene9_outro.mp3
    audio/timing_manifest.json
"""

import asyncio
import json
import os

import edge_tts
from mutagen.mp3 import MP3

# ── CONFIG ────────────────────────────────────────────────────────────────────
VOICE      = "en-US-AndrewNeural"   # warm, confident, educational male voice
OUTPUT_DIR = "audio"
MANIFEST   = os.path.join(OUTPUT_DIR, "timing_manifest.json")

# Slight slowdown gives students time to absorb dense quant content
RATE  = "-5%"    # 5 % slower than default — keeps Andrew natural, not rushed
PITCH = "+0Hz"   # no pitch shift

# ── VOICE-OVER SCRIPTS ───────────────────────────────────────────────────────
# Each entry is (scene_key, narration_text).
# The ORDER here also defines the JSON manifest order and should match the
# scene order in quantifaya_ep1.py FullEpisode.
#
# [BEAT] markers in comments below indicate where the animation should sync —
# they are NOT spoken; they are removed from the TTS text.  The corresponding
# self.wait() durations in quantifaya_ep1.py are derived from the audio
# duration minus the total animation time for that segment.

SCRIPTS: dict[str, str] = {

    # ── SCENE 1  ~1:30  ──────────────────────────────────────────────────────
    "scene1_intro": (
        "August 2007. Goldman Sachs — one of the most sophisticated quantitative "
        "trading operations on earth — watched their flagship quant fund bleed thirty "
        "percent in a single week. "
        "Their risk models — built on decades of financial theory, PhDs, and hundreds "
        "of millions of dollars of compute — said this was a once-in-a-hundred-thousand-year "
        "event. "
        "It wasn't. "
        "And the reason it wasn't — the reason nearly every financial crisis in modern "
        "history was impossible according to the models — comes down to one single "
        "assumption. One equation. One bell curve. "
        "The Normal Distribution. "
        "Welcome to Quantifaya. I'm your host — a financial engineer with Masters in Financial Engineering from "
        "WorldQuant University — and today we're going to destroy the most dangerous "
        "assumption in all of quantitative finance. And then we're going to build "
        "something better. "
        "Let's get into it."
    ),

    # ── SCENE 2  ~4:00  ──────────────────────────────────────────────────────
    "scene2_normal_dist": (
        "Before we burn it down, we need to understand why the Normal Distribution "
        "became finance's default assumption in the first place. "
        "The Normal Distribution — also called the Gaussian distribution — is described "
        "by this probability density function. "
        "f of x equals one over the square root of two pi sigma squared, times e to the "
        "negative x minus mu, squared, over two sigma squared. "
        "Two parameters. That's it. Mu — the mean. Sigma — the standard deviation. "
        "It's mathematically beautiful. Symmetric around the mean. And it has this "
        "incredible empirical property called the Central Limit Theorem: the average of "
        "independent random variables converges to it, regardless of the underlying "
        "distribution. That's why it appears everywhere in nature. "
        "So in the 1950s and 60s, when Harry Markowitz was building Modern Portfolio "
        "Theory and Fischer Black and Myron Scholes were pricing options, they did what "
        "any good scientist does — they reached for the most tractable distributional "
        "assumption available. They assumed returns are normally distributed. "
        "Under this assumption, a one-sigma daily move happens 32 percent of the time. "
        "A two-sigma move? About 4.5 percent of the time. "
        "A three-sigma move? Less than 0.3 percent. "
        "And a five-sigma event? The probability is about 2.87 times ten to the negative "
        "seven. If you assume 252 trading days per year, that's one five-sigma event "
        "every 14,000 years. "
        "Except the 1987 Black Monday crash was a 22-sigma event. "
        "Long Term Capital Management's 1998 blowup involved returns beyond six sigma. "
        "And Goldman's quant quake in 2007? Twenty-five sigma — on multiple consecutive days. "
        "The model doesn't just get it slightly wrong. It gets it catastrophically wrong "
        "in precisely the scenarios where getting it right matters most — market crashes, "
        "liquidity crises, contagion events. "
        "So why does finance keep using it? Partly inertia. Partly tractability. And "
        "partly because in calm markets, with short windows and diversified portfolios, "
        "it's a reasonable approximation. "
        "The problem is the tails. And that's what we need to talk about."
    ),

    # ── SCENE 3  ~5:00  ──────────────────────────────────────────────────────
    "scene3_moments": (
        "To understand fat tails mathematically, we need to talk about moments. "
        "Not moments in time — statistical moments. These are summary statistics that "
        "describe the shape of a distribution. "
        "The first moment is the mean — where are returns centered on average. "
        "The second moment is variance — how dispersed are returns around that mean. "
        "The third standardized moment is skewness — whether the distribution is "
        "symmetric or if one tail is longer than the other. "
        "And the fourth standardized moment is kurtosis — and this is today's protagonist. "
        "Kurtosis is defined as the expected value of X minus mu to the fourth power, "
        "divided by sigma to the fourth. More precisely, we work with excess kurtosis — "
        "sometimes called Fisher's kurtosis — which subtracts three. "
        "Why subtract three? Because when you compute kurtosis for the Normal "
        "Distribution exactly, you get three. So excess kurtosis measures how much "
        "heavier your tails are compared to Normal. "
        "Excess kurtosis of zero — Normal. Greater than zero — your distribution is "
        "leptokurtic, meaning it has fatter tails and a higher, sharper peak than Normal. "
        "Now look at real data. The S&P 500 daily returns have excess kurtosis somewhere "
        "between four and seven, depending on the sample period. Bitcoin? Often above "
        "twelve. Student-t distributions with few degrees of freedom can have infinite "
        "kurtosis. Infinite — meaning no finite fourth moment exists. "
        "And here's the critical consequence. "
        "When you zoom into the tails of a leptokurtic distribution versus the Normal, "
        "you see the gap. That gap — that seemingly tiny strip of extra probability mass "
        "out in the extreme tails — is where five-sigma events live. Is where "
        "twenty-five sigma events live. Is where every financial crisis in modern "
        "history lives. "
        "The Normal Distribution assigns these regions a probability indistinguishable "
        "from zero. Real financial returns do not. "
        "This is not a minor calibration error. This is a model that is fundamentally, "
        "architecturally wrong about the most important part of the distribution."
    ),

    # ── SCENE 4  ~4:00  ──────────────────────────────────────────────────────
    "scene4_empirical": (
        "Theory is one thing. Let's look at what the data actually shows. "
        "Here's a stylized histogram of daily S&P 500 returns — the kind of empirical "
        "distribution you get when you pull decades of price data. The x-axis is daily "
        "return, the y-axis is frequency. I've overlaid the Normal Distribution fitted "
        "to the same mean and standard deviation. "
        "See the problem immediately? The bars in the middle are roughly in line with "
        "the curve — that's fine. But look at the tails. The empirical bars extend well "
        "beyond where the Normal Distribution says there should be almost no probability. "
        "The bars in the tails are taller than the curve. Sometimes dramatically so. "
        "At four sigma, the Normal Distribution predicts a probability density of "
        "roughly 1.34 times ten to the negative four. Real equity return data at that "
        "level is typically ten times more frequent. And at five, six, seven sigma, "
        "the gap becomes astronomically large. "
        "There's a standard diagnostic tool for this — the Quantile-Quantile plot, "
        "or Q-Q plot. If your data were perfectly Normal, every point would fall on "
        "this straight diagonal line. What we actually see with financial return data "
        "is an S-shape — and crucially, the tails curl above the line. That curl is "
        "the signature of fat tails. The empirical distribution puts more probability "
        "mass in the extremes than Normal predicts. "
        "And now we can locate every major market crisis on this distribution. "
        "Black Monday 1987 — twenty-two sigma under Normal assumptions. "
        "LTCM in 1998 — beyond six sigma. "
        "The Global Financial Crisis of 2008 produced multiple single-day moves beyond "
        "seven sigma. "
        "The COVID crash of March 16th, 2020 — eight sigma. "
        "Goldman's quant quake — twenty-five sigma on multiple consecutive days. "
        "Under a Normal Distribution, each of these events has a probability so small "
        "it should never occur in the entire age of the universe — let alone in a "
        "single century of stock market history. "
        "And yet here they are. Every decade. Like clockwork. "
        "The data is telling us something the models refuse to hear."
    ),

    # ── SCENE 5  ~3:30  ──────────────────────────────────────────────────────
    "scene5_mechanisms": (
        "So now we know the Normal Distribution fails, and we've seen the empirical "
        "evidence. But why do fat tails exist? What generates them mechanically in "
        "financial markets? "
        "There are three key mechanisms, and understanding them matters for building "
        "better models. "
        "First: volatility clustering. This is the GARCH effect — named for the "
        "Generalized Autoregressive Conditional Heteroskedasticity model developed by "
        "Tim Bollerslev in 1986. "
        "In real markets, volatility is not constant. Large moves tend to cluster "
        "together. A turbulent day is followed by more turbulent days. A calm period "
        "begets calm. "
        "In GARCH one-one, today's variance depends on yesterday's squared shock and "
        "yesterday's variance — a feedback loop. Even if individual shocks are "
        "conditionally Normal, the unconditional distribution — what you observe over "
        "time — has fat tails. This mechanism alone is powerful enough to generate "
        "much of the excess kurtosis we observe in equity returns. "
        "Second: jumps. The standard Black-Scholes model assumes prices follow a "
        "continuous diffusion — Geometric Brownian Motion. But real prices jump. "
        "A company misses earnings and gaps down fifteen percent overnight. A central "
        "bank surprises the market. A geopolitical shock hits. "
        "Robert Merton's 1976 jump-diffusion model augments standard Brownian motion "
        "with a compound Poisson jump process. The jump intensity lambda controls how "
        "often jumps arrive. These discontinuities are impossible to hedge continuously, "
        "and they inject extreme outcomes into the tail of the return distribution. "
        "Third, and perhaps most insidious: correlation breakdown. "
        "In normal markets, assets in a diversified portfolio have modest correlations. "
        "The diversification benefit is real. "
        "But in crises, correlations spike dramatically — often approaching one across "
        "all asset classes simultaneously. "
        "This is the cruel joke of financial risk. The moment a tail event occurs is "
        "the exact moment your diversification vanishes. Assets you thought were "
        "independent move together, amplifying losses across your portfolio far beyond "
        "what any Normal-based model predicted. "
        "These three mechanisms — volatility clustering, jumps, and correlation "
        "breakdown — combine to generate the fat-tailed, negatively skewed, "
        "heteroskedastic reality of financial returns. "
        "The Normal Distribution assumes none of them."
    ),

    # ── SCENE 6  ~3:00  ──────────────────────────────────────────────────────
    "scene6_var": (
        "Now let's translate this mathematical failure into something tangible: "
        "Value at Risk — the dominant risk metric used by banks, hedge funds, and "
        "regulators worldwide. "
        "VaR at confidence level alpha is formally defined as the negative of the "
        "infimum of x such that the CDF of X exceeds one minus alpha. "
        "In plain English — the VaR at 95 percent confidence is the number such that "
        "on 95 percent of trading days, your loss will be smaller. "
        "It's a quantile of the loss distribution. "
        "Under a Normal Distribution, computing VaR is trivial. "
        "The 95 percent one-day VaR is simply mu minus 1.645 sigma. "
        "The 99 percent VaR is mu minus 2.326 sigma. "
        "These z-scores come straight from the Normal quantile table. "
        "Simple. Fast. Analytically clean. And catastrophically wrong. "
        "Compare Normal VaR to the VaR from a Student-t distribution with four degrees "
        "of freedom — a distribution with fat tails but the same mean and standard "
        "deviation. "
        "At 99 percent confidence, the fat-tail VaR is roughly 1.8 times larger. "
        "That gap represents losses the Normal model simply cannot see. Cannot price. "
        "Cannot reserve capital for. "
        "In practice, this means a trading desk using Normal VaR might believe it needs "
        "100 million dollars in capital to cover its tail risk. The actual fat-tailed "
        "distribution of its positions requires 180 million dollars. "
        "That 80 million dollar gap is not a rounding error. "
        "It's the gap between solvency and failure in a crisis. "
        "This is why we have Conditional Value at Risk — also called Expected Shortfall. "
        "CVaR is the expected loss conditional on being in the tail — the average loss "
        "when things go very wrong, not just the threshold. It integrates the shape of "
        "the tail rather than just reading off a single quantile. "
        "And it's worth noting: regulators figured this out. "
        "The Basel III Fundamental Review of the Trading Book, adopted in 2016, mandated "
        "a shift from VaR to Expected Shortfall as the primary capital measure precisely "
        "because VaR under-captures tail risk. "
        "The question is whether your models caught up."
    ),

    # ── SCENE 7  ~4:00  ──────────────────────────────────────────────────────
    "scene7_better_models": (
        "Alright — we've established the problem rigorously. Now let's talk solutions. "
        "What do actual quants and risk models use? "
        "The first and most accessible upgrade is the Student-t distribution. "
        "Originally developed for small-sample statistical testing, it has found a "
        "permanent home in quantitative finance because of one key property: its tails "
        "decay as a power law rather than exponentially. "
        "The probability density function involves the Gamma function and a single extra "
        "parameter — nu, the degrees of freedom. As nu increases, the distribution "
        "converges to Normal. "
        "At nu equals five, the excess kurtosis is six. "
        "At nu equals four, excess kurtosis is theoretically infinite. "
        "At nu of three or below, the variance itself becomes undefined. "
        "When practitioners fit the Student-t to equity return data using maximum "
        "likelihood estimation, they typically find nu between three and six. "
        "Goldman Sachs's models in 2007 reportedly used around six degrees of freedom — "
        "still underestimating the true tail thickness, as 2007 demonstrated. "
        "The second class of models takes Benoit Mandelbrot's insight from 1963 — "
        "that financial data follows Lévy-stable distributions, not Normal. "
        "The characteristic function of a Lévy-stable distribution has four parameters. "
        "Alpha, the tail index, controls how heavy the tails are. "
        "When alpha equals two, you recover the Normal. "
        "When alpha equals one, you get the Cauchy distribution, which has no finite "
        "mean and no finite variance at all. "
        "The key visual insight is on a log-log plot. The Normal tail curves downward "
        "rapidly — exponential decay. A power-law tail — the signature of Lévy-stable "
        "distributions — appears as a straight line. That straight line represents "
        "dramatically more probability mass at extreme values. "
        "Mandelbrot's empirical estimate for cotton prices was an alpha of about 1.7 — "
        "comfortably in fat-tail territory. "
        "The third approach, and the current industry standard, combines GARCH volatility "
        "dynamics with fat-tailed innovations. "
        "The standard GARCH with Student-t errors captures both the clustering mechanism "
        "— why volatility persists — and the tail thickness within each period. "
        "Extend to GJR-GARCH and you also capture the leverage effect — the asymmetry "
        "where negative shocks hit volatility harder than positive ones. "
        "No single model captures everything. If you want to be closest to the full "
        "complexity of real markets — fat tails, asymmetry, volatility clustering, and "
        "occasional jumps — you need a model that combines all four features."
    ),

    # ── SCENE 8  ~3:00  ──────────────────────────────────────────────────────
    "scene8_lessons": (
        "So what do we take away from all of this? "
        "Three practical commandments for every quant, risk manager, and serious investor. "
        "First: test your distributional assumption. "
        "Never assume normality for risk calculations without empirically verifying it. "
        "The Jarque-Bera test — which jointly tests whether the skewness and excess "
        "kurtosis of your data are consistent with Normal — is fast and easy to implement. "
        "Under the null hypothesis of normality, the JB statistic follows a chi-squared "
        "distribution with two degrees of freedom. "
        "If your p-value is small, your data isn't Normal. That's not a minor issue. "
        "That's a mandate to use a different distribution. "
        "Second: switch to Expected Shortfall. "
        "The formula for ES at confidence level alpha is the integral of VaR from alpha "
        "to one, divided by one minus alpha. "
        "It's the average loss across the entire tail beyond your VaR threshold. "
        "Unlike VaR, it's sensitive to how bad the bad days actually are — not just "
        "how many of them there are. It's also subadditive — it respects portfolio "
        "diversification in a way that VaR does not. Basel III mandated Expected "
        "Shortfall for a reason. "
        "Third: model your volatility. A GARCH one-one with Student-t innovations has "
        "four parameters — omega, alpha, beta, and nu. That's just four parameters. "
        "And it consistently, dramatically outperforms Normal i.i.d. assumptions in "
        "out-of-sample backtesting studies across every major equity market. "
        "The cost of ignoring volatility clustering is large. "
        "The cost of fitting a four-parameter model is negligible. "
        "Practically speaking: every time you build a return model, run through this "
        "checklist. Compute your excess kurtosis. Test for normality. Model volatility "
        "with GARCH or at minimum report CVaR alongside VaR. Do not calibrate "
        "exclusively on recent data — recency bias creates tail blindness. "
        "And always stress test beyond three sigma. "
        "Keynes said markets can remain irrational longer than you can remain solvent. "
        "I'll add a corollary for quants: models can remain wrong longer than you can "
        "remain employed. "
        "Build for the tail."
    ),

    # ── SCENE 9  ~1:00  ──────────────────────────────────────────────────────
    "scene9_outro": (
        "That's a wrap on Episode One of Quantifaya. "
        "We covered a lot of ground today. "
        "We started with the Normal Distribution — its PDF, its assumptions, why finance "
        "adopted it. We built the mathematics of moments and kurtosis from the ground up. "
        "We looked at the empirical evidence in real return data — the Q-Q plots, the "
        "histograms, the historical crises that should be impossible but keep happening. "
        "We explored the three mechanisms — GARCH clustering, jumps, and correlation "
        "breakdown — that generate fat tails in practice. "
        "We dissected the VaR failure and built the CVaR solution. "
        "And we surveyed the better distributional models: Student-t, Lévy-stable, "
        "and GARCH-t. "
        "If you want to go deeper, the single best book on this topic is Benoit "
        "Mandelbrot and Richard Hudson's The Misbehaviour of Markets. Mandelbrot spent "
        "fifty years proving that financial returns follow power laws, not bells. "
        "It's readable, rigorous, and genuinely important. Link is in the description. "
        "Next week, we're building Itô's Lemma from the ground up — the mathematical "
        "engine behind Black-Scholes, interest rate models, and virtually every "
        "derivative pricing formula in existence. We'll show exactly why classical "
        "calculus breaks in continuous time and what stochastic calculus does instead. "
        "Subscribe so you don't miss it. "
        "Drop a comment below — what's the most extreme sigma event you've personally "
        "lived through in the markets? I want to hear from you. "
        "This is Quantifaya. See you next week."
    ),
}


# ── AUDIO GENERATION ─────────────────────────────────────────────────────────

async def _generate_one(name: str, text: str, path: str) -> None:
    """Generate a single MP3 via edge-tts."""
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH)
    await communicate.save(path)


async def generate_all() -> dict[str, float]:
    """Generate all audio files and return {scene_key: duration_seconds}."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    durations: dict[str, float] = {}

    for name, text in SCRIPTS.items():
        out = os.path.join(OUTPUT_DIR, f"{name}.mp3")
        if os.path.exists(out):
            print(f"  ✓  Already exists: {out}")
        else:
            print(f"  →  Generating {name} …", end="", flush=True)
            await _generate_one(name, text, out)
            print(" done")

        audio    = MP3(out)
        dur      = audio.info.length
        durations[name] = dur
        mm, ss   = int(dur // 60), int(dur % 60)
        print(f"     duration: {mm}:{ss:02d}  ({dur:.2f}s)")

    return durations


def write_manifest(durations: dict[str, float]) -> None:
    """Write timing manifest so the Manim script can read exact durations."""
    with open(MANIFEST, "w") as f:
        json.dump(durations, f, indent=2)
    print(f"\n  ✓  Manifest written → {MANIFEST}")
    total = sum(durations.values())
    mm, ss = int(total // 60), int(total % 60)
    print(f"  ✓  Total narration time: {mm}:{ss:02d}")


# ── ENTRY POINT ───────────────────────────────────────────────────────────────

async def main() -> None:
    print("═" * 60)
    print("  Quantifaya Ep 1 — Audio Generator")
    print(f"  Voice : {VOICE}  |  Rate : {RATE}  |  Pitch : {PITCH}")
    print("═" * 60)
    durations = await generate_all()
    write_manifest(durations)
    print("\nAll done.  Run quantifaya_ep1.py after this step.\n")


if __name__ == "__main__":
    asyncio.run(main())