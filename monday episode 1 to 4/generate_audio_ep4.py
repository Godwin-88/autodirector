"""
generate_audio_ep4.py
─────────────────────────────────────────────────────────────────────────────
Quantifaya Episode 4 — Voice-over generator
Uses edge-tts with en-US-AndrewNeural (same voice as Episode 1).

After generating all MP3s this script writes audio/timing_manifest_ep4.json with
the EXACT duration of every audio file in seconds.

Usage:
    pip install edge-tts mutagen
    python generate_audio_ep4.py

Output:
    audio/ep4_scene*.mp3
    audio/timing_manifest_ep4.json
"""

import asyncio
import json
import os

import edge_tts
from mutagen.mp3 import MP3

# ── CONFIG ────────────────────────────────────────────────────────────────────
VOICE      = "en-US-AndrewNeural"   # same authoritative voice as Episode 1
OUTPUT_DIR = "audio"
MANIFEST   = os.path.join(OUTPUT_DIR, "timing_manifest_ep4.json")

RATE  = "-5%"    # slight slowdown for dense quant content
PITCH = "+0Hz"

# ── VOICE-OVER SCRIPTS ───────────────────────────────────────────────────────
# Each entry is (scene_key, narration_text).
# The ORDER here also defines the JSON manifest order and should match the
# scene order in quantifaya_ep4.py FullEpisode.

SCRIPTS: dict[str, str] = {

    # ── SCENE 1  ~1:30  ──────────────────────────────────────────────────────
    "ep4_scene1_intro": (
        "Five letters. Delta. Gamma. Vega. Theta. Rho. "
        "If you've spent any time around options, you've heard these words. "
        "Your textbook defined them. Your professor gave you the formulas. "
        "Your first Bloomberg terminal showed you the numbers. "
        "What nobody told you — and what Nassim Taleb spells out in the opening "
        "chapters of Dynamic Hedging — is that these measures are meaningful "
        "for a single vanilla option, and treacherous the moment you run a book. "
        "The Greeks are partial derivatives of the option price with respect "
        "to market variables. They're local, first-and-second-order approximations "
        "of a nonlinear, path-dependent, volatility-sensitive payoff. "
        "On a single position, they're extraordinarily useful. "
        "Across a portfolio mixing long and short options of different strikes "
        "and maturities, they compound, cancel, and interact in ways that "
        "have ended more than a few careers. "
        "Today we build every major Greek from the Black-Scholes formula "
        "by differentiation. We show what each one means economically. "
        "We show what happens when you hedge with each one. "
        "And we tell you exactly where Taleb says they break — "
        "and what the professionals use instead. "
        "Welcome to Episode 4. Let's arm up."
    ),

    # ── SCENE 2  ~4:00  ──────────────────────────────────────────────────────
    "ep4_scene2_delta": (
        "Delta. The first Greek. The first derivative of the call price "
        "with respect to the stock price. And the most misunderstood number "
        "in options trading. "
        "Mathematically, Delta is the partial derivative of the call price C "
        "with respect to the stock price S. From the Black-Scholes formula, "
        "this turns out to equal N of d one — the Normal CDF evaluated at d one. "
        "For a put, it's N of d one minus one — which is always negative, "
        "because puts move inversely with the stock. "
        "We can derive this cleanly. Differentiate the Black-Scholes formula for C. "
        "You get N of d one plus two cross-terms involving the Normal density. "
        "Those two cross-terms cancel exactly — it's a clean cancellation "
        "that requires a few lines of algebra to verify but is a standard result. "
        "You're left with Delta equals N of d one. "
        "Economically, Delta ranges from zero to one for calls, "
        "from negative one to zero for puts. A deep out-of-the-money call "
        "with Delta of five percent behaves like five cents of stock per dollar. "
        "A deep in-the-money call with Delta of ninety-eight percent behaves "
        "almost identically to holding the stock outright. "
        "At the money, Delta is approximately fifty percent — which is why "
        "options traders sometimes call an ATM option a fifty-delta. "
        "As expiry approaches, the Delta curve steepens. "
        "A one-day ATM option has Delta that flips from near-zero to near-one "
        "as the stock crosses the strike. That's the Gamma bomb "
        "we'll discuss in Scene 4. "
        "But here's where Taleb draws first blood. His Chapter 7 is titled "
        "'Adapting Black-Scholes-Merton: The Delta,' and he opens with "
        "a direct attack on the textbook definition. "
        "The mathematical delta — dF over dU — is the hedge ratio "
        "for an infinitely small move. "
        "In practice: there is no such thing as an infinitely small move "
        "in the market. Markets gap. Markets close on Friday and open "
        "on Monday three percent away. The delta is a tangent line, "
        "and markets don't move along tangent lines. "
        "Here's what delta hedging actually looks like. "
        "Stock at a hundred, ATM call, six-month maturity, twenty percent vol. "
        "Black-Scholes gives us a call price of roughly ten forty-five "
        "and a delta of fifty-eight percent. "
        "To delta-hedge a short call, I buy 0.5793 shares. "
        "My portfolio value is flat to small stock moves. "
        "If the stock moves one dollar, the option gains approximately "
        "fifty-eight cents — covered by my share position. "
        "Perfect in continuous time. An approximation in discrete time, "
        "with a residual error that grows with the square of the move. "
        "That residual error is Gamma. We'll get there."
    ),

    # ── SCENE 3  ~2:00  ──────────────────────────────────────────────────────
    "ep4_scene3_delta_practice": (
        "Let's go one level deeper — to where the textbook definition of delta "
        "breaks in practice. Taleb devotes most of Chapter 7 to this, "
        "and it's worth understanding. "
        "Consider a portfolio: long one million of the ninety-six calls, "
        "short one million of the one-oh-four calls. "
        "The system computes total delta as positive six hundred and twenty-six "
        "thousand. Hedge accordingly — sell six-twenty-six of forward. "
        "Done. Clean. "
        "Except it's not. Map the P&L across spot levels and you see a position "
        "that looks like a long everywhere — except near the origin, "
        "where it's locally flat. "
        "The total delta is an aggregate that disguises the local structure. "
        "The hedge is misleading. "
        "The second failure is more dramatic. "
        "Taleb describes a real argument on a trading floor: "
        "a risk manager vetoed a barrier option trade because the delta "
        "at the barrier was ten thousand percent — implying five hundred million "
        "dollars of equivalent stock exposure on a five-million-dollar trade. "
        "The trader's maximum loss was four hundred thousand dollars. "
        "Both numbers were mathematically correct. "
        "Neither was operationally useful. "
        "Taleb's prescription: use the discrete delta. "
        "Instead of the continuous partial derivative, compute the option price "
        "change over a realistic — one or two sigma — move up and down, "
        "and divide by twice the move size. "
        "This naturally incorporates a portion of the gamma and vega exposure. "
        "Less elegant mathematically. Far more honest as a risk measure. "
        "This is the difference between a textbook and a trading desk."
    ),

    # ── SCENE 4  ~4:00  ──────────────────────────────────────────────────────
    "ep4_scene4_gamma": (
        "Gamma. The second derivative of the option price "
        "with respect to the stock price. Or equivalently — "
        "the rate of change of Delta. "
        "And the most important risk measure that junior traders "
        "systematically underestimate. "
        "From Black-Scholes, Gamma equals the Normal density N prime of d one, "
        "divided by S times sigma times the square root of T. "
        "The Normal density is always positive. "
        "So Gamma is always positive for long options — whether calls or puts — "
        "and always negative for short options. "
        "Here's the key geometric insight, and it connects directly to Episode 2. "
        "The full change in option price for a stock move dS is Delta times dS "
        "plus one-half Gamma times dS squared — "
        "this is the Taylor expansion, with the Itô correction sitting "
        "right there in the Gamma term. "
        "Delta is the linear approximation. Gamma is the curvature correction. "
        "If you're long Gamma, the actual price change is always larger "
        "than Delta predicts — you gain more on up moves and lose less "
        "on down moves than a linear hedge would suggest. Always. "
        "This is the central trade in options. Long Gamma means you own convexity — "
        "every large move benefits you. Short Gamma means you sold convexity — "
        "every large move hurts you. "
        "The catch: you pay for long Gamma through time decay — "
        "Theta bleeds you every night. And you collect Theta by being short Gamma — "
        "but you're exposed to every gap, every earnings surprise, "
        "every central bank shock. "
        "This trade-off is the engine of every options desk on earth. "
        "The Gamma profile across spot is a bell curve — maximum at-the-money, "
        "collapsing toward zero for deep in-the-money and out-of-the-money options. "
        "Across time, Gamma concentrates. "
        "A one-year ATM option has low, stable Gamma. "
        "A one-day ATM option has Gamma that spikes violently — "
        "essentially infinite right at the strike. "
        "Being short a one-day ATM straddle with the stock oscillating "
        "around the strike is how options market makers have career-ending days. "
        "Now here's what Taleb adds that Hull doesn't emphasize. "
        "The conventional Gamma assumes symmetry — "
        "same sensitivity to up moves and down moves. "
        "In markets with a volatility skew — which is all equity markets "
        "since 1987 — this is wrong. "
        "When a stock falls, volatility typically rises simultaneously. "
        "The effective Gamma on a down move is larger than the mathematical Gamma, "
        "because you're getting both the delta change and the vol move "
        "compounding against you. "
        "Taleb calls this the Shadow Gamma. "
        "And his prescription: compute Up-Gamma and Down-Gamma separately. "
        "The textbook number is the average of two different risk numbers."
    ),

    # ── SCENE 5  ~2:00  ──────────────────────────────────────────────────────
    "ep4_scene5_gamma_practice": (
        "Let's make Gamma concrete with numbers, "
        "because this is where the money is. "
        "ATM option, thirty days to expiry, twenty percent vol. "
        "Gamma is approximately 0.0668. "
        "On a quiet day where the stock moves fifty cents — "
        "Gamma earns less than one cent per option. Barely visible. "
        "On a three-dollar move, Gamma earns thirty cents per option. "
        "On a ten-dollar move — a crash — "
        "Gamma earns three dollars and thirty-four cents per option. "
        "On a position of ten thousand options, "
        "that's thirty-four thousand dollars in a single day. "
        "The crucial point: Gamma P&L scales with the square of the move. "
        "Double the move, four times the Gamma P&L. "
        "This is why large moves are Christmas for long gamma books "
        "and catastrophic for short gamma desks. "
        "Near expiry, the trap closes. "
        "Gamma of an ATM option explodes as time runs out. "
        "A market maker short ATM options on expiry day faces Gamma "
        "that approaches infinity as the stock oscillates around the strike. "
        "Every time the stock crosses the strike price, "
        "Delta flips from zero to one — the option goes from worthless "
        "to dollar-for-dollar with the stock in a single tick. "
        "The market maker must delta-hedge every time. "
        "Each rebalance pays bid-ask spread. "
        "On a volatile expiry day with ten crossings, "
        "the hedging cost can exceed the entire premium collected "
        "for selling the option. "
        "Taleb illustrates shadow Gamma with his Syldavian elections case study — "
        "one of the best pedagogical examples in Dynamic Hedging. "
        "A currency facing a binary political outcome: "
        "anarchists win and the currency drops ten percent "
        "with volatility spiking to twenty-nine percent; "
        "the pro-market party wins and spot holds with vol dropping to fourteen. "
        "The conventional Gamma gave a number. "
        "The shadow Gamma — which accounts for the correlated vol and spot move — "
        "gave a completely different position sizing. "
        "The trader who relied on the textbook Gamma was exposed. "
        "The one who computed shadow Gamma was prepared."
    ),

    # ── SCENE 6  ~3:30  ──────────────────────────────────────────────────────
    "ep4_scene6_vega": (
        "Vega. The volatility Greek. Not technically a Greek letter — "
        "Taleb notes it's sometimes called kappa or zeta or lambda "
        "depending on which desk you're on. "
        "The industry standardized on Vega. We'll go with the industry. "
        "Vega is the partial derivative of the option price "
        "with respect to implied volatility. "
        "From Black-Scholes, it equals S times the square root of T "
        "times the standard Normal density evaluated at d one. "
        "It's always positive for long options — more volatility means "
        "higher option price, regardless of direction. "
        "Differentiate the Black-Scholes formula with respect to sigma. "
        "You get two terms involving the Normal density "
        "N prime of d one and N prime of d two. "
        "There's a useful identity: S times N prime of d one "
        "equals K e to the minus rT times N prime of d two. "
        "The two terms collapse. Vega equals S root T N prime of d one. Clean. "
        "The Vega profile across spot is the same bell shape as Gamma — "
        "maximum at-the-money, zero deep in or out of the money. "
        "But across time, Vega behaves differently from Gamma. "
        "Vega scales with the square root of T — "
        "longer-dated options carry more Vega. "
        "A one-year option has twice the Vega of a three-month option. "
        "Long-dated positions are long-dated volatility bets. "
        "Here's the connection Taleb draws in Chapter 9 "
        "that most textbooks miss. "
        "Vega is actually the integral of expected Gamma rebalancing profits "
        "over the option's life. "
        "Mathematically, Vega equals Gamma times S squared times sigma times T. "
        "They're not independent measures — they're related "
        "by the volatility and time parameters. "
        "Which means a portfolio that hedges Gamma and Vega "
        "at the same strike and maturity is fully hedged. "
        "But across a book with different strikes and maturities, "
        "Gamma and Vega can diverge — your Gamma exposure is concentrated "
        "near-term ATM while your Vega exposure is spread across the vol surface. "
        "They require separate management. "
        "Taleb's Chapter 9 introduces modified Vega — "
        "sensitivity to non-parallel shifts in the vol surface. "
        "A book with zero total Vega can still lose money "
        "if the short end of the vol curve spikes "
        "while the long end stays flat. "
        "That's a twist, not a parallel shift. "
        "Bucket Vega — Vega at each maturity separately — "
        "is what risk managers on serious books actually monitor. "
        "One-year ATM option on a hundred-dollar stock. "
        "Vega is approximately forty cents per one-percent vol move. "
        "A desk long ten thousand of these has four thousand dollars "
        "of Vega per vol tick. "
        "A five-percent vol spike generates twenty thousand dollars "
        "of profit — instantly, before the delta even moves. "
        "Vol can move five percent in a morning. "
        "Vega is not a secondary concern."
    ),

    # ── SCENE 7  ~2:30  ──────────────────────────────────────────────────────
    "ep4_scene7_theta": (
        "Theta. The time decay Greek. The one that makes option selling "
        "feel like being a landlord — collect rent every day, "
        "hope there are no catastrophes. "
        "From Black-Scholes, Theta for a European call is negative one-half "
        "times S times N prime of d one times sigma, "
        "divided by the square root of T, minus r times K times "
        "e to the minus rT times N of d two. "
        "It's always negative for long options. "
        "Time passing — with everything else held constant — "
        "reduces an option's value. Every single day. "
        "The Theta profile mirrors the Gamma bell curve — "
        "maximum magnitude at-the-money, smaller for deep in "
        "or out-of-the-money options. "
        "ATM options have the most time value and decay fastest. "
        "This is not a coincidence — it's built into the structure "
        "of Black-Scholes. "
        "Here's the most important single identity in options risk management — "
        "and it falls directly out of the Black-Scholes PDE from Episode 3. "
        "For a delta-hedged position, Theta is approximately equal to "
        "minus one-half sigma squared S squared times Gamma. "
        "Read that again. "
        "Theta equals negative Gamma times a constant. "
        "If you're long Gamma, you're paying Theta every night. "
        "If you're short Gamma, you're collecting it. "
        "The Gamma-Theta trade-off is not a coincidence — "
        "it's a mathematical identity embedded in the PDE. "
        "Being long convexity costs time. "
        "Being short convexity earns time. "
        "The market prices this exactly. "
        "And Theta accelerates. "
        "An option doesn't decay linearly. "
        "It loses roughly a third of its time value "
        "in the final month of a three-month option's life — "
        "far more than in the first month. "
        "Weekend effect: a position held over Friday close "
        "decays three calendar days by Monday open, "
        "because Theta ticks through weekends even when markets are closed. "
        "This is why options sellers love Fridays "
        "and options buyers dread them."
    ),

    # ── SCENE 8  ~2:00  ──────────────────────────────────────────────────────
    "ep4_scene8_rho_and_dashboard": (
        "Before we put it all together — Rho. The interest rate Greek. "
        "From Black-Scholes, Rho for a call equals K times T times "
        "e to the minus rT times N of d two. "
        "Positive for calls — higher rates reduce the present value "
        "of the strike you pay, making the call more valuable. "
        "For equity options at typical rates and maturities, "
        "Rho is the smallest Greek and receives the least attention. "
        "For long-dated interest rate derivatives or currencies "
        "where the rate differential IS the trade — Rho is everything. "
        "Now the complete dashboard. "
        "For an ATM six-month option on a hundred-dollar stock "
        "with twenty percent vol and five percent rates: "
        "Delta is fifty-eight percent, Gamma is 0.0267, "
        "Vega is twenty-eight cents per one percent vol move, "
        "Theta is negative three point eight cents per day, "
        "and Rho is twenty-three dollars per one percent rate move. "
        "Here's why this matters operationally. "
        "The change in option value for any set of market moves "
        "decomposes exactly across the Greeks: "
        "Delta times the stock move, plus half Gamma times "
        "the squared stock move, plus Vega times the vol move, "
        "plus Theta times the time elapsed, plus Rho times the rate move. "
        "This is the options trader's daily P&L equation. "
        "If you can compute your Greeks every morning, "
        "and you observe what moved during the day, "
        "you can attribute every dollar of P&L to its source. "
        "Delta gave you this. Gamma gave you that. "
        "Vol hurt you here. Theta bled you there. "
        "Concretely: stock up two dollars, vol down half a percent, "
        "one day of time. "
        "Delta P&L: one dollar fifteen. Gamma P&L: five cents. "
        "Vega P&L: minus fourteen cents. Theta: minus four cents. "
        "Net: the option gained about a dollar three. "
        "That's P&L attribution. "
        "That's how a real desk understands what happened each day."
    ),

    # ── SCENE 9  ~2:30  ──────────────────────────────────────────────────────
    "ep4_scene9_taleb_shortcomings": (
        "Now for the most important two minutes of this episode — "
        "and they come directly from page one-twelve of Dynamic Hedging. "
        "Taleb includes a table — and I'm going to reproduce it "
        "because it should be mandatory reading for every quant "
        "and every options student. "
        "Delta. Definition: sensitivity to the underlying price. "
        "Textbook. Clean. "
        "Shortcoming, per Taleb: 'Delta does not work on a portfolio "
        "of options that mixes longs and shorts. "
        "It is an extremely weak measure of risks.' "
        "The prescription: use a discrete delta with realistic move sizes. "
        "The Shadow Delta adds vega and gamma contributions. "
        "Gamma. Definition: rate of change of delta. Textbook. "
        "Shortcoming: 'It is meaningless for a portfolio of options. "
        "It does not take into account changes in volatility "
        "when the market moves.' "
        "The prescription: Up-Gamma and Down-Gamma separately. "
        "Shadow Gamma accounts for the vol-spot correlation. "
        "Theta: 'Does not take into account changes in volatility "
        "that co-occur with time passage.' "
        "Vega: 'Parallel shift assumption' — "
        "assumes all maturities move simultaneously. "
        "Neither is true in real markets. "
        "The meta-lesson is this. "
        "Taleb writes in Chapter 9 — and I'm quoting directly: "
        "'The conventional training of people, which consists of toying "
        "with the conventional derivatives of the Black-Scholes formula, "
        "has a negative effect on their operating style. "
        "Trading an option bears little relevance to trading a book.' "
        "Single option Greeks: well-defined, analytically clean, "
        "useful for intuition. "
        "Book-level Greeks: they aggregate, they interact, "
        "they cancel in ways the formulas don't warn you about. "
        "The Greeks are the starting vocabulary. "
        "Scenario analysis — 'what if spot drops ten percent "
        "AND vol spikes five' — is the actual risk management. "
        "If you're running a real options book on anything more complex "
        "than a single vanilla, you're running bucket Vegas, "
        "up-and-down gammas, and scenario matrices. "
        "The formulas from today are the foundation. "
        "The practice is considerably more demanding."
    ),

    # ── SCENE 10  ~1:00  ─────────────────────────────────────────────────────
    "ep4_scene10_outro": (
        "That's Episode 4. "
        "We built every major Greek from the Black-Scholes formula "
        "by differentiation. "
        "Delta equals N of d one — but Taleb's discrete delta "
        "is more honest operationally. "
        "Gamma equals N prime of d one over S sigma root T — "
        "always positive for long options, with Up-Gamma and Down-Gamma "
        "required in skewed markets. "
        "The Gamma-Theta identity — Theta approximately equals "
        "minus one-half sigma squared S squared times Gamma — "
        "is the mathematical heart of the long-vol versus short-vol trade-off. "
        "Vega equals S root T times N prime of d one — "
        "scales with root-T, requires bucket analysis across the vol surface. "
        "And Taleb's shortcomings table from page one-twelve "
        "is required reading for anyone who plans to run a real book. "
        "Two books to keep beside you. "
        "Taleb's Dynamic Hedging — Chapters seven through eleven "
        "for the Greeks, with particular attention to the shadow gamma "
        "and modified vega sections. This is the practitioner's manual. "
        "And Hull's Chapter nineteen for the analytical formulas "
        "and their derivations. "
        "Read Hull first for the structure, "
        "then Taleb to understand why structure alone isn't enough. "
        "Challenge for this week: prove the Gamma-Theta identity "
        "directly from the Black-Scholes PDE. "
        "Start from the PDE, substitute Theta and Gamma, "
        "apply the delta-hedge condition, "
        "and show that Theta plus one-half sigma squared S squared Gamma "
        "equals approximately zero. "
        "First full proof in the comments gets pinned. "
        "Next week: the Heston model. "
        "Because the volatility smile told us Black-Scholes was wrong "
        "about vol being constant. "
        "Heston made vol itself a mean-reverting stochastic process — "
        "and produced one of the few non-Black-Scholes models "
        "with a quasi-analytical option pricing formula. "
        "We derive it. "
        "Subscribe. Share. This is Quantifaya."
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
    print("  Quantifaya Ep 4 — Audio Generator")
    print(f"  Voice : {VOICE}  |  Rate : {RATE}  |  Pitch : {PITCH}")
    print("═" * 60)
    durations = await generate_all()
    write_manifest(durations)
    print("\nAll done.  Run quantifaya_ep4.py after this step.\n")


if __name__ == "__main__":
    asyncio.run(main())