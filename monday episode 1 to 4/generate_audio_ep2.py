"""
generate_audio_ep2.py
─────────────────────────────────────────────────────────────────────────────
Quantifaya Episode 2 — Voice-over generator
Uses edge-tts with en-US-AriaNeural.

After generating all MP3s this script writes audio/timing_manifest_ep2.json with
the EXACT duration of every audio file in seconds.  quantifaya_ep2.py reads
that manifest at render-time so every scene's self.wait() is calibrated to
the real audio — not a hand-waved estimate.

Usage:
    pip install edge-tts mutagen
    python generate_audio_ep2.py

Output:
    audio/ep2_scene*.mp3
    audio/timing_manifest_ep2.json
"""

import asyncio
import json
import os

import edge_tts
from mutagen.mp3 import MP3

# ── CONFIG ────────────────────────────────────────────────────────────────────
VOICE      = "en-US-AndrewNeural"  # male, confident, positive
OUTPUT_DIR = "audio"
MANIFEST   = os.path.join(OUTPUT_DIR, "timing_manifest_ep2.json")

RATE  = "-5%"    # slightly slower for dense quant content
PITCH = "+0Hz"

# ── VOICE-OVER SCRIPTS ───────────────────────────────────────────────────────
# Each entry is (scene_key, narration_text).
# The ORDER here also defines the JSON manifest order and should match the
# scene order in quantifaya_ep2.py FullEpisode.

SCRIPTS: dict[str, str] = {

    # ── SCENE 1  ~1:30  ──────────────────────────────────────────────────────
    "ep2_scene1_intro": (
        "1944. World War II is still being fought. And somewhere in Japan, "
        "a 29-year-old mathematician named Kiyosi Itô — working in near-total isolation, "
        "with limited access to Western literature — writes four pages. "
        "Four pages that would eventually underpin every option, every swap, "
        "every structured product, every exotic derivative traded on this planet. "
        "Six hundred trillion dollars. That's the notional size of the global derivatives market. "
        "Built on four pages. "
        "Your calculus professor never mentioned Itô's name. I'm going to tell you why. "
        "Classical calculus — the Newton-Leibniz version you were tortured with in school — "
        "works beautifully on smooth, differentiable functions. You have a curve. "
        "You draw a tangent. You compute a derivative. Everything is clean, everything is deterministic. "
        "Financial markets are none of those things. "
        "This jagged, violent, non-differentiable path — Brownian motion — "
        "is what actually drives stock prices. You cannot draw a tangent line on it. "
        "It has no derivative in the classical sense. Everywhere you look, it's rough. "
        "Itô's genius was building a calculus for rough paths. "
        "A calculus where the correction term isn't just a philosophical nicety — "
        "it's a trading signal worth hundreds of billions of dollars. "
        "Welcome back to Quantifaya. Let's get into it."
    ),

    # ── SCENE 2  ~2:00  ──────────────────────────────────────────────────────
    "ep2_scene2_brownian": (
        "Before we can understand Itô's Lemma, we need to understand what it's operating on. "
        "And that means understanding Brownian motion — the mathematical object "
        "that Norbert Wiener formalized in 1923. "
        "Brownian motion — also written B of t or W of t — is defined by three axioms. "
        "First: it starts at zero. B of zero equals zero. Clean slate. "
        "Second: increments are Normally distributed with variance equal to the elapsed time. "
        "The increment from time s to time t — B of t minus B of s — follows a Normal distribution "
        "with mean zero and variance t minus s. This is crucial: "
        "the uncertainty grows proportionally to time, not to time squared. "
        "That square-root-of-time scaling is why volatility scales with the square root "
        "of the holding period — a fact every risk manager on earth uses daily. "
        "Third: the increments are independent. Yesterday's move tells you nothing about today's move. "
        "The process has no memory. It's the financial equivalent of a goldfish. "
        "And here's the property that breaks classical calculus completely: "
        "Brownian motion is almost surely continuous — no jumps — but nowhere differentiable. "
        "Zoom into any segment, no matter how small, and it's still rough. "
        "It's a fractal. It has no tangent anywhere. "
        "Now look at this property. The expected value of dB squared — "
        "the instantaneous variance — equals dt. The square of the random increment "
        "is deterministic in expectation. This is the single fact that makes "
        "Itô's correction term exist. Hold onto it. It will become everything. "
        "Think of Brownian motion as the raw material. "
        "What Itô did was build the machinery to work with it — "
        "to differentiate and integrate functions of this chaotic object. "
        "Like building a lathe to cut stone that no blade had touched before."
    ),

    # ── SCENE 3  ~2:40  ──────────────────────────────────────────────────────
    "ep2_scene3_quadratic_variation": (
        "Now here's where things get genuinely interesting — "
        "and where every student who learned calculus and thought they were done "
        "gets a very rude awakening. "
        "In classical calculus, when you expand a smooth function f of x plus dx "
        "using a Taylor series, you get f of x, plus the first derivative times dx, "
        "plus one-half the second derivative times dx squared, and so on. "
        "And as dx goes to zero, the squared term goes to zero faster — "
        "it's order dx squared, which is negligible compared to dx. "
        "So you throw it away. That's the entire story of classical differentiation. "
        "Now try the same trick with Brownian motion. "
        "Replace dx with dB — the infinitesimal Brownian increment. "
        "You get the same expansion: f prime times dB, "
        "plus one-half f double-prime times dB squared. "
        "And here's the question that defines stochastic calculus: "
        "can we throw away dB squared the same way? "
        "The answer is a categorical no — "
        "and the reason is in this table of orders. "
        "In classical calculus, dt squared goes to zero — fine. "
        "dt times dB goes to zero — fine. "
        "But dB squared? dB is of order square root of dt. "
        "So dB squared is of order dt. Which does NOT go to zero. "
        "It stays. It matters. It changes the answer. "
        "This fact has a name: the quadratic variation of Brownian motion. "
        "The sum of squared increments of B over any partition of the time interval converges — "
        "almost surely — not to zero but to t. The length of the time interval. "
        "This result — which goes by Theorem 3.4.3 in Shreve's "
        "Stochastic Calculus for Finance — is what separates Itô's world from Newton's world. "
        "We can write this compactly as a multiplication table for stochastic differentials. "
        "dt times dt is zero. dt times dB is zero. But dB times dB equals dt. "
        "Not approximately. Not in some limiting sense. Equals. "
        "The square of a random quantity is deterministic. "
        "Stochastic calculus is built on this audacity. "
        "And if your first instinct is that this feels wrong — good. "
        "That means your mathematical instincts are working. "
        "They're just calibrated for the wrong universe. "
        "Markets live in Itô's universe. Not Newton's."
    ),

    # ── SCENE 4  ~3:40  ──────────────────────────────────────────────────────
    "ep2_scene4_ito_lemma": (
        "Right. Gloves off. We're deriving Itô's Lemma from first principles. "
        "No hand-waving. No 'it can be shown.' We're doing the actual proof. "
        "Let X of t be an Itô process — a stochastic process described by this SDE: "
        "dX equals mu dt plus sigma dB. The mu term is the drift — the deterministic trend. "
        "The sigma dB term is the diffusion — the random shock. "
        "Every continuous-time financial model you've ever seen is a special case of this structure. "
        "The question Itô asked — and answered — is this: "
        "if X follows this process, and f is a smooth function of X and t, what process does f follow? "
        "In classical calculus, the answer is just the chain rule. "
        "In stochastic calculus, the chain rule is wrong. "
        "And Itô's Lemma tells you why, and by how much. "
        "Step one. Taylor expand f to second order in dX and dt. "
        "df equals partial f over partial t, times dt — the time derivative — "
        "plus partial f over partial X, times dX — the space derivative — "
        "plus one-half partial squared f over partial X squared, times dX squared. "
        "And higher-order terms. "
        "So far this looks like classical calculus. The crime happens in the next step. "
        "Step two. Substitute dX equals mu dt plus sigma dB. "
        "Now compute dX squared. That's mu dt plus sigma dB, all squared, "
        "which gives mu squared dt squared, plus two mu sigma dt dB, plus sigma squared dB squared. "
        "Step three. Apply Itô's multiplication table. dt squared is zero — negligible. "
        "dt times dB is zero — negligible. But dB squared equals dt. "
        "Watch what happens. Two of the three terms in dX squared vanish — gone — "
        "and we're left with sigma squared dt. "
        "That's the Itô correction. It came from the squared term in the Taylor expansion "
        "that classical calculus told you to throw away. "
        "Except in Itô's world, you cannot throw it away, "
        "because dB squared is not small — it equals dt. "
        "Step four and five — substitute back and collect terms. "
        "Group everything multiplying dt and everything multiplying dB. "
        "And we arrive at Itô's Lemma. "
        "df equals — open bracket — partial f over partial t, "
        "plus mu times partial f over partial X, "
        "plus ONE HALF sigma squared times the second partial of f over X squared — "
        "close bracket — times dt, plus sigma times partial f over partial X, times dB. "
        "This term. One-half sigma squared times the second derivative of f. "
        "This is the Itô correction. This is the term that does not exist in classical calculus. "
        "This is the term that, when you ignore it, "
        "leads to mispriced derivatives and blown-up funds. "
        "In classical calculus, the chain rule is a first-order story. "
        "Itô's Lemma is a second-order story — because randomness lives at the second-order level. "
        "Nassim Taleb once wrote: "
        "'The problem with experts is that they do not know what they do not know.' "
        "Pre-Itô quants didn't know they were missing a correction term. "
        "They were confidently, expensively wrong. "
        "Itô knew what the experts didn't know they didn't know. "
        "That's what genius looks like."
    ),

    # ── SCENE 5  ~3:15  ──────────────────────────────────────────────────────
    "ep2_scene5_gbm": (
        "Now let's use Itô's Lemma to do something concrete — "
        "derive the solution to the most important SDE in quantitative finance: "
        "Geometric Brownian Motion. "
        "The standard model for stock prices under the risk-neutral measure is: "
        "dS equals mu S dt plus sigma S dB. "
        "The drift scales with the price — so we get percentage returns, not dollar returns. "
        "The diffusion also scales with price — so volatility is proportional, "
        "which is why we talk about 20 percent annual volatility "
        "rather than twenty dollars per share. "
        "These are sample paths from this process. "
        "Notice they can go up or down, but they never touch zero — "
        "because the percentage changes scale with S, "
        "so you can never lose more than a hundred percent. "
        "GBM respects limited liability. It's a feature. "
        "Now here's the question. What does the logarithm of S follow? "
        "Because log-returns are what we actually compute in practice, "
        "and understanding their distribution gives us the analytical solution for S of T. "
        "Set f equal to log S. The partial derivative with respect to t is zero — "
        "f has no explicit time dependence. The first partial with respect to S is one over S. "
        "The second partial with respect to S is negative one over S squared. "
        "Plug these into Itô's Lemma. The drift contribution gives us mu S times one over S — "
        "which is just mu — plus one-half sigma squared S squared times negative one over S squared — "
        "which gives negative one-half sigma squared. "
        "The diffusion contribution gives sigma S times one over S — "
        "which simplifies to sigma. "
        "The result is beautiful. d of log S equals mu minus one-half sigma squared, "
        "all times dt, plus sigma dB. This is just a constant-coefficient SDE. "
        "Its solution is trivial: log S is Normally distributed with mean "
        "mu minus one-half sigma squared times T, and variance sigma squared T. "
        "Which means S itself is log-normally distributed — "
        "and we can write out the explicit closed-form solution for S at any future time T. "
        "But look at the drift of the log-return: mu minus one-half sigma squared. Not mu. "
        "There's a haircut. A drag. "
        "This is the volatility drag — and it's one of the most underappreciated facts "
        "in portfolio management. If your annual expected return is ten percent "
        "and your annual volatility is twenty percent, "
        "your geometric mean compound return is not ten percent — it's eight percent. "
        "Two percent per year, compounding quietly against you, forever. "
        "Watch what happens over a long horizon. "
        "The arithmetic mean of S — which is S naught times e to the mu t — "
        "grows faster than the typical outcome. "
        "The median of S — S naught times e to the mu minus half sigma squared times t — "
        "is what most investors actually experience. "
        "And the gap between them widens every year. "
        "Itô's correction term isn't abstract mathematics. "
        "It's the gap between what a fund advertises and what investors actually receive."
    ),

    # ── SCENE 6  ~2:00  ──────────────────────────────────────────────────────
    "ep2_scene6_ito_integral": (
        "Before we get to Black-Scholes, we need one more piece: "
        "the Itô integral. Because just as differentiation doesn't work classically here, "
        "neither does integration. "
        "In classical calculus, the Riemann integral doesn't care where "
        "in each interval you evaluate the function. "
        "Left endpoint, right endpoint, midpoint — "
        "in the limit, they all give the same answer. The integral is path-independent. "
        "Not here. When we integrate a process H with respect to Brownian motion, "
        "we are forced to use the left endpoint of each interval. Always. "
        "Not because it's convenient — because it's the only causally consistent choice. "
        "In financial terms: when you hold a position H of t over the interval "
        "from t to t plus dt, you must decide your position size "
        "before observing the Brownian shock in that interval. "
        "You can't know the future. The integral enforces this. "
        "This non-anticipating requirement means the integrand H must be adapted "
        "to the filtration — it can only use information available up to the current time t. "
        "If you use future information, you're not computing an Itô integral. You're cheating. "
        "And in trading, cheating is called insider trading. "
        "The Itô integral has two key properties. "
        "First, its expected value is zero — because Brownian increments are mean-zero, "
        "and we're evaluating H before seeing them. No free lunch. "
        "Second — and this is the jewel — the Itô Isometry: "
        "the variance of the stochastic integral equals "
        "the expected value of the integral of H squared. "
        "This is the stochastic analogue of Parseval's theorem. "
        "If this feels complicated — it is. "
        "But the Itô integral is the only mathematically honest way to price a derivative. "
        "Every other approach is either an approximation or a prayer. "
        "The derivatives desk doesn't do prayers."
    ),

    # ── SCENE 7  ~3:48  ──────────────────────────────────────────────────────
    "ep2_scene7_black_scholes": (
        "Here it is. The application that made Itô a billionaire-maker — "
        "even though he never cared about money. "
        "Black-Scholes. Derived live, from scratch, using Itô's Lemma. "
        "Stock price S follows Geometric Brownian Motion: "
        "dS equals mu S dt plus sigma S dB. "
        "Option price V depends on S and t. "
        "We want to know what V is worth today. "
        "And here's the first remarkable thing: "
        "we're going to get the answer without ever knowing mu — "
        "the expected return of the stock. That's not a typo. Watch. "
        "Apply Itô's Lemma to V of S and t. "
        "We get: dV equals the bracket — partial V over partial t, "
        "plus mu S partial V over partial S, "
        "plus one-half sigma squared S squared times the second partial of V over S squared — "
        "close bracket — times dt, plus sigma S partial V over partial S, times dB. "
        "This describes how the option value changes over an instant. "
        "Now here's the cleverness. "
        "Construct a portfolio Pi: long one option, short Delta units of stock, "
        "where Delta equals partial V over partial S — the option's delta. "
        "The portfolio value is V minus Delta times S. "
        "Compute dPi. It's dV minus Delta times dS. "
        "Substitute Itô's dV and the GBM dS. "
        "Watch what happens to the dB terms. "
        "We have sigma S partial V over partial S times dB from the dV term. "
        "And we subtract partial V over partial S times sigma S dB from the Delta-dS term. "
        "These are identical. They cancel. Exactly. Completely. "
        "The randomness is gone. "
        "And look — mu — the drift, the expected return — it also cancels. "
        "The delta-hedged portfolio's dynamics depend on neither "
        "the expected return of the stock nor the random Brownian shock. "
        "Both annihilated by the hedge. "
        "dPi equals partial V over partial t, "
        "plus one-half sigma squared S squared times the second partial of V over S squared, "
        "times dt. A deterministic expression. A riskless portfolio. "
        "In an efficient market, a riskless portfolio must earn exactly "
        "the risk-free rate r. Otherwise there's an arbitrage — a money machine — "
        "and money machines don't persist. Set the two expressions for dPi equal and rearrange. "
        "And we have it. The Black-Scholes partial differential equation. "
        "Partial V over partial t, plus r S times partial V over partial S, "
        "plus one-half sigma squared S squared times the second partial of V over S squared, "
        "minus r V, equals zero. "
        "Each term has a name traders use every day. Theta — time decay. "
        "The gamma term — convexity, the curvature of the option's value. "
        "And the discounting term. This PDE, subject to the terminal boundary condition "
        "V equals max of S minus K, zero, at expiry, gives the Black-Scholes formula. "
        "Notice d one in the Black-Scholes formula contains one-half sigma squared. "
        "Itô's correction, embedded permanently in the price of every option "
        "traded on every exchange on earth. "
        "Itô wrote four pages in 1944. In 1973, Black and Scholes weaponized them. "
        "In 1997, Scholes won the Nobel Prize. "
        "Itô won the Gauss Prize in 2006 — mathematics' equivalent. "
        "The market paid better."
    ),

    # ── SCENE 8  ~1:30  ──────────────────────────────────────────────────────
    "ep2_scene8_ito_vs_strat": (
        "One thing nobody tells you in a quant course: "
        "Itô's convention is not the only one. "
        "There's a parallel universe called Stratonovich calculus "
        "that physicists and engineers often prefer — "
        "and understanding why finance rejects it is important. "
        "The difference is subtle but profound. "
        "Itô uses the left endpoint of each time interval — "
        "we evaluate H before seeing the Brownian shock. "
        "Stratonovich uses the midpoint — "
        "which requires partial information about the future. "
        "This gives Stratonovich a beautiful property: "
        "the classical chain rule holds without any correction term. "
        "Newton's ghost is happy. "
        "But for finance, Stratonovich is inadmissible. "
        "Using the midpoint means using information that doesn't exist yet "
        "at the time you need to make a trading decision. "
        "It violates causality. It's the mathematical equivalent of front-running. "
        "Itô's convention enforces the reality constraint: "
        "you can only act on what you know now. "
        "The two integrals differ by exactly one-half "
        "the integral of the derivative of H with respect to B. "
        "You can always convert between them. "
        "But in financial modeling, Itô is not a preference — "
        "it's a constraint imposed by the arrow of time. "
        "The Itô correction isn't an inconvenience. "
        "It's the mathematical price of operating in a world "
        "where time flows in only one direction and information arrives sequentially. "
        "Which is, inconveniently, the world we live in."
    ),

    # ── SCENE 9  ~2:20  ──────────────────────────────────────────────────────
    "ep2_scene9_lessons": (
        "Let's land this plane with four truths — "
        "the version the textbooks are too polite to state directly. "
        "First: every time you ignore the Itô correction, "
        "you are systematically mispricing convexity. "
        "Not occasionally. Not under edge cases. Systematically. "
        "Every model without the second-order term understates the value of options, "
        "underestimates the cost of hedging, "
        "and overstates the performance of leveraged strategies. "
        "The correction is not optional. "
        "Second: volatility drag is real money. "
        "If your fund earns a 12 percent expected return with 25 percent volatility, "
        "your geometric compound return is not twelve percent — it's 8.875 percent. "
        "You are surrendering over three percent per year to the Itô correction. "
        "Compounding over twenty years, that's the difference between retiring "
        "and working until you're seventy. Nobody told you this at the fundraise. "
        "Third: Itô's Lemma is the reason delta-hedging works. "
        "It's the reason Black-Scholes exists. "
        "It's the mathematical foundation of a six-hundred-trillion dollar market. "
        "This isn't an academic curiosity. "
        "This is the bedrock of modern finance — "
        "and it lives in four pages written by a Japanese mathematician during World War Two. "
        "Fourth, and most practical: in a quant interview, "
        "you will be asked about this. Not the formula — the derivation. "
        "Knowing that dB squared equals dt and being able to explain why it can't be discarded "
        "is the signal that separates candidates who understand the mathematics "
        "from those who memorized it. "
        "The Itô correction is the differentiator. Literally. "
        "Nassim Taleb wrote in Antifragile: "
        "'Anything that has been around for a long time has proven its antifragility.' "
        "Itô's Lemma has been around since 1944. "
        "Through every market crash, every quantitative revolution, "
        "every Nobel Prize in economics — it's still here. Still right. "
        "Still running every derivatives desk on earth. "
        "Learn it. Own it. "
        "It might be the most important four pages ever written."
    ),

    # ── SCENE 10  ~1:40  ─────────────────────────────────────────────────────
    "ep2_scene10_outro": (
        "That's Episode 2 of Quantifaya. "
        "We covered the complete story — from Brownian motion's axioms, "
        "through quadratic variation and why dB squared equals dt and cannot be thrown away, "
        "through the full derivation of Itô's Lemma, "
        "through Geometric Brownian Motion and the volatility drag, "
        "through the Itô integral and its isometry, "
        "and finally to Black-Scholes — derived from scratch, live, in real time. "
        "Two books belong on your desk after this video. "
        "Shreve's Stochastic Calculus for Finance Two — "
        "the rigorous version of everything we covered, Chapters 3 and 4 specifically. "
        "And Paul Wilmott on Quantitative Finance — "
        "the applied version, with the intuition and the worked examples. "
        "Both links are in the description. "
        "Next week, we take the Black-Scholes formula and extract its weapons: "
        "Delta, Gamma, Vega, Theta, Rho — the Greeks. "
        "We'll build every single one from first principles, "
        "show you what they mean economically, "
        "and explain why Gamma exposure is the most dangerous thing "
        "a derivatives desk can run. Don't miss it. "
        "One final thing. Here's a challenge: "
        "using today's tools, derive the Itô correction for f of S equals S squared. "
        "If your expected return is mu and your vol is sigma, what does d of S squared equal? "
        "First correct full derivation in the comments gets pinned for a week. "
        "Subscribe. Share this with one person studying for a quant interview — "
        "it'll probably get them the job. "
        "This is Quantifaya."
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
    print("  Quantifaya Ep 2 — Audio Generator")
    print(f"  Voice : {VOICE}  |  Rate : {RATE}  |  Pitch : {PITCH}")
    print("═" * 60)
    durations = await generate_all()
    write_manifest(durations)
    print("\nAll done.  Run quantifaya_ep2.py after this step.\n")


if __name__ == "__main__":
    asyncio.run(main())