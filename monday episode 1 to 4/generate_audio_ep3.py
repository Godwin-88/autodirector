"""
generate_audio_ep3.py
─────────────────────────────────────────────────────────────────────────────
Quantifaya Episode 3 — Voice-over generator
Uses edge-tts with en-US-AndrewNeural (warm, authoritative, educational).

After generating all MP3s this script writes audio/timing_manifest_ep3.json with
the EXACT duration of every audio file in seconds.  quantifaya_ep3.py reads
that manifest at render-time so every scene's self.wait() is calibrated to
the real audio — not a hand-waved estimate.

Usage:
    pip install edge-tts mutagen
    python generate_audio_ep3.py

Output:
    audio/ep3_scene*.mp3
    audio/timing_manifest_ep3.json
"""

import asyncio
import json
import os

import edge_tts
from mutagen.mp3 import MP3

# ── CONFIG ────────────────────────────────────────────────────────────────────
VOICE      = "en-US-AndrewNeural"   # warm, confident, educational male voice
OUTPUT_DIR = "audio"
MANIFEST   = os.path.join(OUTPUT_DIR, "timing_manifest_ep3.json")

RATE  = "-5%"    # slightly slower for dense quant content
PITCH = "+0Hz"

# ── VOICE-OVER SCRIPTS ───────────────────────────────────────────────────────
# Each entry is (scene_key, narration_text).
# The ORDER here also defines the JSON manifest order and should match the
# scene order in quantifaya_ep3.py FullEpisode.

SCRIPTS: dict[str, str] = {

    # ── SCENE 1  ~1:30  ──────────────────────────────────────────────────────
    "ep3_scene1_intro": (
        "1997. The Nobel Committee in Stockholm awarded the Prize in Economics "
        "to Myron Scholes and Robert Merton — for a pricing formula that had "
        "already been running the derivatives markets for twenty-four years. "
        "Fischer Black, the third architect of the model, was not there. "
        "He had died two years earlier. The Nobel Prize is not awarded posthumously. "
        "The most famous equation in quantitative finance has a body count. "
        "And a Nobel Prize. And approximately six hundred trillion dollars "
        "of notional derivatives outstanding that price off of it every single day. "
        "This is it. The Black-Scholes formula for a European call option. "
        "Every quant knows it. Most people in finance can recite it. "
        "Very few can derive it from first principles. "
        "Almost none can explain why every single term is there. "
        "After this video, you'll be in that last category. "
        "No hand-waving. No 'it can be shown.' We show. "
        "Welcome to Episode Three of Quantifaya. Let's go."
    ),

    # ── SCENE 2  ~2:30  ──────────────────────────────────────────────────────
    "ep3_scene2_problem_setup": (
        "Before we derive anything, let's be precise about what we're pricing. "
        "A European call option is a contract that gives the buyer the right — "
        "but not the obligation — to purchase a stock at a fixed price K, "
        "called the strike, at a fixed future date T, called the expiry. "
        "The payoff at expiry is max of S_T minus K, zero. "
        "If the stock finishes above the strike, you exercise and pocket the difference. "
        "If it finishes below, you walk away. "
        "The put is the mirror image. The right to sell at K. "
        "Payoff is max of K minus S_T, zero. "
        "Both of these are trivially easy to understand at expiry. "
        "The problem is pricing them today. S_T is unknown. It's a random variable. "
        "The stock could finish at any positive value. "
        "You need to commit to a price — right now — "
        "for a payoff that depends on something that hasn't happened yet. "
        "Today you know: the current stock price S₀. The strike K. "
        "The risk-free interest rate r. The volatility sigma. "
        "You don't know where the stock will be at T. That's the game. "
        "People tried to solve this problem long before Black and Scholes. "
        "Louis Bachelier in 1900 — in his PhD thesis, which his committee "
        "graded 'honorable' rather than 'très honorable,' "
        "a slight he never recovered from — wrote the first mathematical model "
        "of option pricing. He used Arithmetic Brownian Motion, "
        "which allows negative stock prices. Not ideal, but a century ahead of its time. "
        "Paul Samuelson improved it in 1965 with Geometric Brownian Motion, "
        "which keeps prices positive. Better dynamics. Still no clean closed-form price. "
        "Then in 1973, Black, Scholes, and Merton closed the problem. "
        "Permanently. With a formula anyone can compute on a pocket calculator. "
        "Here's how they did it."
    ),

    # ── SCENE 3  ~3:00  ──────────────────────────────────────────────────────
    "ep3_scene3_assumptions": (
        "Every model is a lie. The question is whether it's a productive one. "
        "Black-Scholes makes four assumptions that are all, to varying degrees, "
        "empirically false. And it's still the benchmark every options desk "
        "on earth prices off of. Let's understand why. "
        "First assumption: stock prices follow Geometric Brownian Motion. "
        "We covered this in Episode 2. Log-returns are independent and identically "
        "Normally distributed. Volatility is constant in time. "
        "What does this cost? Everything we covered in Episode 1. "
        "Fat tails — gone. Volatility clustering — gone. Jumps — gone. "
        "Nassim Taleb put it bluntly: 'Those who gave us the Normal distribution "
        "as a description of market randomness have a lot to answer for.' "
        "He's right. And yet. "
        "Second assumption: volatility sigma and the risk-free rate r are constant. "
        "This is perhaps the most operationally important lie in all of quantitative finance. "
        "Look at this. This is what the market implies about volatility across strikes "
        "and maturities — the implied vol surface. It's curved. It smirks. "
        "It has a term structure. It is emphatically not a flat constant. "
        "The Black-Scholes model has been wrong about volatility since October 19th, 1987 — "
        "Black Monday — when the crash permanently bent the smile into existence. "
        "It has never unsmiled since. And BS is still the benchmark. "
        "Make of that what you will. "
        "Third assumption: you can trade continuously, for free, in any size. "
        "This allows the delta hedge to be maintained perfectly, moment to moment, "
        "eliminating all risk from the portfolio. "
        "In practice: you rebalance daily, or hourly. You pay bid-ask spreads. "
        "You pay market impact. The hedging errors accumulate. "
        "Taleb, who spent years on derivatives desks, called this "
        "the dynamic hedging trap — the theoretical perfection of continuous hedging "
        "dissolves the moment real friction enters the system. "
        "Fourth: no dividends, and the option is European. "
        "Both are fixable. Dividends can be incorporated via a continuous yield adjustment. "
        "American options require numerical methods — PDE or binomial trees. "
        "Extensions exist and are well-understood. They're just not today's problem. "
        "So: four assumptions, all wrong, model still dominant. "
        "That's the power of a closed-form solution. People will tolerate a wrong model "
        "if it gives them a number they can act on and hedge with. "
        "Black-Scholes gives you that. "
        "Which is exactly why we're deriving it today."
    ),

    # ── SCENE 4  ~4:00  ──────────────────────────────────────────────────────
    "ep3_scene4_pde": (
        "Alright. This is the main event. We're deriving the Black-Scholes PDE — "
        "the partial differential equation whose solution is the formula. "
        "Every step will be explicit. "
        "The setup: stock price S follows Geometric Brownian Motion "
        "with drift mu and volatility sigma. "
        "The option price V is some function of S and t that we don't yet know. "
        "Our goal is to find it. "
        "Step one: apply Itô's Lemma to V of S and t. "
        "We covered this in Episode 2. "
        "The drift of V picks up three terms: the partial derivative of V with respect to time, "
        "mu S times the delta of V, and crucially — the Itô correction — "
        "one-half sigma squared S squared times the gamma of V, "
        "the second derivative with respect to S. "
        "Plus a diffusion term: sigma S delta dB. "
        "This is the full dynamics of the option under the physical measure. "
        "Now we build the hedge. "
        "Step two: construct a portfolio Pi — long one option, short Delta units of stock, "
        "where Delta equals the partial derivative of V with respect to S. "
        "The portfolio value is V minus Delta times S. "
        "Why this particular Delta? Watch what happens when we compute the portfolio's dynamics. "
        "Step three: dPi equals dV minus Delta times dS. "
        "Substitute the Itô expression for dV and the GBM expression for dS. "
        "Expand everything. "
        "Step four. Look at the dB terms. We have plus sigma S partial V over partial S "
        "times dB from the option. And minus partial V over partial S times sigma S dB "
        "from the stock position. These are exactly equal and opposite. "
        "They cancel. Perfectly. Completely. "
        "That was not an accident — we chose Delta precisely to make this happen. "
        "The delta is the exact hedge ratio that eliminates the randomness. "
        "And look — the mu terms cancel too. "
        "The expected return of the stock is completely gone from the portfolio dynamics. "
        "A portfolio of an option and exactly Delta shares of stock has zero exposure "
        "to either the randomness or the expected return of the underlying. "
        "It is riskless. "
        "Step five: a riskless portfolio must earn the risk-free rate. "
        "This is the no-arbitrage condition. "
        "If the portfolio earned more than r, you could borrow at r and invest in Pi indefinitely — "
        "a money machine. If it earned less, short Pi and lend at r. "
        "Markets eliminate both possibilities instantly. "
        "So dPi equals r times Pi times dt. Substitute Pi equals V minus Delta S. "
        "Set the two expressions for dPi equal. Collect terms. Rearrange. "
        "And there it is. The Black-Scholes partial differential equation. "
        "Partial V over partial t, plus rS times partial V over partial S, "
        "plus one-half sigma squared S squared times the second partial of V over S squared, "
        "minus rV equals zero. "
        "Every term has a name traders use daily. "
        "The time derivative — theta. The rS delta term — the discounted delta contribution. "
        "The gamma term — the Itô correction, the convexity of the option, "
        "the reason options have curvature in their payoff. The minus rV — the discounting. "
        "This PDE, combined with three boundary conditions — the terminal payoff, "
        "the value when the stock hits zero, and the deep in-the-money limit — "
        "has a unique solution. Finding it analytically requires one more trick."
    ),

    # ── SCENE 5  ~3:30  ──────────────────────────────────────────────────────
    "ep3_scene5_heat_equation": (
        "The PDE is in hand. Now we need to solve it. "
        "And we're going to use a trick that connects the 1973 Nobel Prize "
        "to a French mathematician named Joseph Fourier who died 141 years "
        "before Black and Scholes were even born. "
        "The Black-Scholes PDE is a parabolic second-order PDE in S and t. "
        "It's not in canonical form. It has a variable coefficient S squared "
        "in front of the second derivative, and it mixes time and space derivatives "
        "in a way that's hard to work with directly. We need to change variables "
        "to simplify it. "
        "First substitution: let tau equal T minus t — time to expiry "
        "rather than calendar time. This reverses the time direction "
        "so that tau runs forward from zero at expiry to T at inception. "
        "This is standard for parabolic PDEs — we solve forward from the initial condition. "
        "Second substitution: let x equal the natural log of S over K — "
        "the log moneyness. When S equals the strike K, x equals zero. "
        "We're centering the problem at the money. "
        "Compute the chain rule transformations for the partials. "
        "The second derivative in S becomes one over S squared times "
        "the second derivative in x minus the first derivative in x. "
        "This is where the log-price substitution earns its keep — "
        "it converts the variable-coefficient S-squared term "
        "into a constant-coefficient second derivative in x. "
        "Third substitution: factor out the discounting. "
        "Write V as e to the minus r tau times u of x tau. "
        "This absorbs the minus rV term in the PDE. "
        "Substitute all three changes. After algebra — which I'll spare you "
        "the step-by-step of, it's in Shreve Chapter 4 — we arrive at this: "
        "partial u over partial tau equals one-half sigma squared times "
        "the second partial of u over xi squared, where xi accounts for the drift. "
        "This. Is. The. Heat. Equation. "
        "Partial u over partial tau equals one-half sigma squared times "
        "the second partial over xi squared. "
        "Joseph Fourier derived this in 1822 to describe heat diffusing through a metal rod. "
        "The same equation governs how temperature profiles smooth out over time "
        "in a rod — and how option value diffuses backward from the payoff at expiry "
        "to the price today. The mathematics does not care about the interpretation. "
        "It's the same differential operator. "
        "The heat equation has a classical solution via its fundamental solution — "
        "the Green's function. The option price at any earlier time "
        "is the terminal payoff convolved with a Normal kernel. "
        "Conceptually: we're taking the payoff at expiry, smearing it backward in time "
        "through a Gaussian filter, and the result is the fair price today. "
        "When you carry out this integral explicitly — substituting the call option payoff "
        "max of S_T minus K zero, splitting the integral at S_T equals K, "
        "and evaluating each half — two terms emerge naturally. "
        "The first integral gives S₀ times N of d₁. "
        "The second gives K e to the minus rT times N of d₂. "
        "Transform back from u to V by multiplying by e to the minus r tau. "
        "And we have arrived. The Black-Scholes formula. "
        "Not from nowhere. Not from magic. From Fourier's heat equation, "
        "Itô's stochastic calculus, and the no-arbitrage principle — "
        "three ideas from three centuries, combined into one formula."
    ),

    # ── SCENE 6  ~3:00  ──────────────────────────────────────────────────────
    "ep3_scene6_formula": (
        "The formula is in hand. Let's take it apart — every single term. "
        "Because if you can't explain every component, you don't actually understand the price. "
        "The Black-Scholes formula for a European call is: "
        "C equals S₀ N of d₁, minus K e to the minus rT, times N of d₂. "
        "Start with the simplest piece: K e to the minus rT. "
        "This is the present value of the strike price — what you will pay at expiry "
        "if you exercise, discounted back to today. "
        "In a world with no uncertainty, that's exactly what the option would cost. "
        "The interesting part is everything multiplying it. "
        "N of d₂ is the risk-neutral probability that the option expires in the money — "
        "that S_T exceeds K at expiry. Not the real-world probability. "
        "The risk-neutral probability. Under the risk-neutral measure Q, "
        "where we've replaced the stock's actual drift mu with the risk-free rate r. "
        "More on that distinction in a moment. "
        "N of d₁ is the option's delta — the number of shares of stock "
        "you need to hold to replicate the option at every instant. "
        "It's also the probability of expiring in the money under a different measure — "
        "the stock measure, where we use the stock as the numeraire rather than the bond. "
        "These two probability measures differ by exactly the Itô correction. "
        "And here it is again — our old friend from Episode 2. "
        "d₁ minus d₂ equals sigma root T. "
        "The difference between the hedge ratio probability and the exercise probability "
        "is the Itô correction. d₂ uses the geometric mean drift — "
        "mu minus one-half sigma squared. d₁ uses the arithmetic mean drift. "
        "The one-half sigma squared is permanently embedded in the Black-Scholes formula, "
        "as it must be, because Brownian motion lives in Itô's universe. "
        "Before we move on — Put-Call Parity. It takes thirty seconds to derive. "
        "A portfolio of long call, short put, same strike same expiry, "
        "must equal a long forward on the stock minus the present value of the strike. "
        "That's no-arbitrage. No stochastic calculus required. Just the law of one price. "
        "C minus P equals S₀ minus K e to the minus rT. "
        "If you know the call price, you know the put price. "
        "The two are not independent. The market respects this to the tick — "
        "if it doesn't, there's an arbitrage, and arbitrageurs close it within seconds."
    ),

    # ── SCENE 7  ~2:30  ──────────────────────────────────────────────────────
    "ep3_scene7_risk_neutral": (
        "Here's the question that should be bothering you. "
        "When we derived the PDE, the drift mu — the expected return of the stock — "
        "disappeared entirely. The option price doesn't depend on whether "
        "you think the stock will return five percent or fifty percent. "
        "As long as sigma is the same, the option price is the same. "
        "This is not obvious. This is profound. "
        "And it has a precise mathematical explanation. "
        "The answer is the risk-neutral measure. "
        "Under the real-world probability measure P, the stock drifts at mu — "
        "its actual expected return, reflecting investors' risk preferences "
        "and compensation for bearing equity risk. "
        "Under the risk-neutral measure Q, we instead assume the stock drifts at r — "
        "the risk-free rate. Everyone is indifferent to risk. "
        "All assets earn the same return. "
        "The transition between these two worlds is governed by Girsanov's Theorem. "
        "We change the Brownian motion by subtracting the market price of risk — "
        "lambda equals mu minus r over sigma — multiplied by time. "
        "Under Q, the new Brownian motion makes the stock drift at r. "
        "This gives us the risk-neutral pricing formula: "
        "option price equals the discounted expectation of the payoff under Q. "
        "This is the Fundamental Theorem of Asset Pricing — "
        "the deepest result in modern derivatives theory. "
        "Harrison and Kreps in 1979 proved that the absence of arbitrage "
        "is equivalent to the existence of at least one risk-neutral measure. "
        "Harrison and Pliska in 1981 proved that market completeness — "
        "the ability to replicate any payoff — is equivalent to the uniqueness of that measure. "
        "The Black-Scholes model is complete: one stock, one Brownian motion, one Q. "
        "The risk-neutral world is not a description of how investors actually behave. "
        "Nobody genuinely expects all assets to earn the risk-free rate. "
        "It is a computational device. A change of probability measure "
        "that makes option pricing tractable while preserving the no-arbitrage constraint. "
        "The answer it gives is correct — by construction. "
        "Do not confuse the risk-neutral measure with reality. "
        "Most people in finance don't. "
        "Because most people in finance don't know it exists."
    ),

    # ── SCENE 8  ~2:30  ──────────────────────────────────────────────────────
    "ep3_scene8_breaks": (
        "We'd be lying to you if we derived Black-Scholes without telling you "
        "where it breaks. And it breaks — spectacularly — in at least one place. "
        "The volatility smile. If Black-Scholes were correct, every option "
        "on the same underlying, regardless of strike or maturity, "
        "would imply the same volatility sigma. That's what constant sigma means. "
        "You'd see a flat line across all strikes. "
        "What you actually see, in every liquid options market in the world, "
        "is a curve. OTM puts are expensive relative to Black-Scholes. "
        "OTM calls vary by market. In equities, you typically see a skew — "
        "a smirk — where out-of-the-money puts carry significantly higher implied vol "
        "than at-the-money options. This is the market pricing in the fat left tail — "
        "crash risk — that Black-Scholes says is nearly impossible. "
        "This phenomenon did not exist before October 1987. "
        "The 1987 Black Monday crash bent the smile into existence. "
        "It has never straightened since. "
        "The constant vol assumption has been empirically violated for 37 years. "
        "Three reasons. First: fat tails. As we showed in Episode 1, "
        "real returns have excess kurtosis — more probability mass in the tails "
        "than Normal distributions predict. OTM options are worth more than BS says. "
        "Second: jump risk. Crash events are discrete, large, and fast — "
        "not continuous diffusions. OTM puts insure against crashes. They're valuable. "
        "Third: supply and demand. Institutional investors systematically buy "
        "OTM puts as portfolio insurance. This demand pushes their prices — "
        "and thus their implied vols — above Black-Scholes. "
        "The industry response was a hierarchy of increasingly sophisticated models. "
        "Derman and Kani in 1994 introduced local volatility — "
        "sigma as a function of both the stock price and time, "
        "calibrated to match the observed smile exactly. "
        "Heston's stochastic volatility model in 1993 makes vol itself a random process — "
        "a mean-reverting diffusion. "
        "Merton's jump-diffusion adds compound Poisson jumps. "
        "All of these are extensions of Black-Scholes. "
        "All of them inherit its structure. "
        "None of them replace the fundamental insight. "
        "Here's the irony that professional options traders live with every day. "
        "Black-Scholes is wrong. And the market uses it as the unit of measurement. "
        "Traders quote option prices not in dollars — "
        "they quote them in implied volatility. "
        "Which is the Black-Scholes sigma that makes the formula match the market price. "
        "The wrong model is the language in which the correct prices are communicated. "
        "This is either profound or farcical. I'll let you decide."
    ),

    # ── SCENE 9  ~1:30  ──────────────────────────────────────────────────────
    "ep3_scene9_lessons": (
        "Four truths. No softening. "
        "The Black-Scholes formula is not magic and it is not a black box. "
        "It is Itô's Lemma applied to a delta-hedged portfolio, "
        "plus the no-arbitrage condition, plus the classical heat equation solution. "
        "Three ideas. All derivable in under an hour. All yours now. "
        "The expected return of the stock doesn't affect the option price. "
        "This seems wrong. It isn't. "
        "The risk-neutral measure explains it: under Q, all assets earn r by construction, "
        "so mu is simply irrelevant to the pricing problem. "
        "Harrison and Kreps proved this rigorously in 1979. "
        "If you go into a quant interview and can explain why mu disappears — "
        "not just that it does — you are already in the top ten percent of candidates. "
        "Black-Scholes has been empirically wrong about volatility since 1987. "
        "The smile proves it. And it's still the benchmark. "
        "Learn it deeply enough to know exactly how it's wrong, "
        "where it's wrong, and what the smile tells you about the assumptions "
        "it's violating. That knowledge is worth more than knowing it fails. "
        "Interview calibration. Can you derive the PDE from Itô and no-arbitrage? "
        "Top five percent. Can you explain why N of d₁ and N of d₂ are different? "
        "Top ten. Can you explain the vol smile qualitatively? Top twenty. "
        "Can you just recite the formula? That's everyone. "
        "Taleb wrote in Dynamic Hedging: "
        "'The hedging errors are generally small for vanilla options "
        "but can be monstrous for exotics.' "
        "Know your model. Know its limits. Know when it fails. "
        "That's what separates a quant from someone who Googled the formula."
    ),

    # ── SCENE 10  ~1:00  ─────────────────────────────────────────────────────
    "ep3_scene10_outro": (
        "That's Episode Three. "
        "We covered the full Black-Scholes arc. "
        "The option pricing problem and the century of failed attempts before 1973. "
        "The four assumptions and their real-world cost. "
        "The PDE derivation — Itô's Lemma, delta hedge, dB cancellation, no-arbitrage condition. "
        "The heat equation transformation that gave us the analytical solution. "
        "The anatomy of every term in the formula. "
        "The risk-neutral measure and the Fundamental Theorem of Asset Pricing. "
        "And finally — where it all breaks, and what the profession built to replace it. "
        "Two books. Hull's Options, Futures, and Other Derivatives — "
        "the practitioner's bible. Chapters fifteen and nineteen cover Black-Scholes "
        "as thoroughly as any textbook. Read it first. "
        "Then read Taleb's Dynamic Hedging — the book that tells you everything "
        "Hull's clean framework glosses over when you're actually on a derivatives desk "
        "running a book with real P&L. "
        "Comment challenge: price a cash-or-nothing digital call — "
        "a contract that pays exactly one dollar if S_T exceeds K, zero otherwise. "
        "Use the risk-neutral pricing formula. "
        "The answer involves N of d₂. I want to see the full derivation "
        "and an explanation of why only d₂ appears and not d₁. "
        "First complete correct answer gets pinned. "
        "Next week: the Greeks. Delta, Gamma, Vega, Theta — "
        "derived from the Black-Scholes formula by differentiation. "
        "We'll build every single one from first principles, "
        "explain what each one means economically, "
        "and talk about why Gamma exposure is the most dangerous thing "
        "a derivatives desk can run. Your theta bleeds every night. "
        "Next week you'll know exactly why. "
        "Subscribe. Share this with one person who's ever pretended "
        "to understand Black-Scholes without being able to derive it. "
        "There are more of them than you think. "
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
    print("  Quantifaya Ep 3 — Audio Generator")
    print(f"  Voice : {VOICE}  |  Rate : {RATE}  |  Pitch : {PITCH}")
    print("═" * 60)
    durations = await generate_all()
    write_manifest(durations)
    print("\nAll done.  Run quantifaya_ep3.py after this step.\n")


if __name__ == "__main__":
    asyncio.run(main())