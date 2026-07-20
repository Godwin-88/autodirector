# QUANTIFAYA — EPISODE 4
## "The Greeks: Delta, Gamma, Vega — Built Intuitively"

**Channel:** Quantifaya
**Target Duration:** 25 minutes
**Production Stack:** Python Manim (Community Edition v0.18+) + TTS Voice-Over
**Persona:** Taylor-meets-Axe-Capital. Taleb-level clinical ruthlessness about risk.
**Primary Sources:** Taleb (1997) Dynamic Hedging [T] | Hull (2018) Options, Futures & Derivatives [H]
**Tone:** The Greeks are weapons. We build them from scratch, show what traders actually use them for,
and — unlike every textbook — show exactly where each one fails and what you do about it.

---

**SEO Title:** The Options Greeks ACTUALLY Explained | Delta, Gamma, Vega Built From Scratch | Quantifaya Ep.4
**SEO Description:** Delta. Gamma. Vega. Theta. Rho. Every options course mentions them. Almost none build them from the Black-Scholes formula, explain why they break on a real trading book, or tell you what Nassim Taleb says about the difference between a single option and a book of options. Today we do all three. If you're a quant, trader, or serious finance student — this is the Greeks episode you actually needed.
**SEO Tags:** options greeks explained, delta gamma vega theta, options delta hedging, gamma risk explained, vega volatility sensitivity, theta decay options, options greeks derivation, black scholes greeks, dynamic hedging taleb, quant finance, financial engineering, derivatives trading, options trading math, implied volatility greeks, quant interview greeks

---

## VERIFIED ACADEMIC SOURCES

| # | Citation | Scene |
|---|---|---|
| [T1] | Taleb, N.N. (1997). *Dynamic Hedging: Managing Vanilla and Exotic Options.* Wiley. Ch.7 — The Delta. p.103–125. | 2, 3 |
| [T2] | Taleb, N.N. (1997). *Dynamic Hedging.* Ch.8 — Gamma and Shadow Gamma. p.127–162. | 4, 5 |
| [T3] | Taleb, N.N. (1997). *Dynamic Hedging.* Ch.9 — Vega and the Volatility Surface. p.147–170. | 6 |
| [T4] | Taleb, N.N. (1997). *Dynamic Hedging.* p.112 — Greeks and Their Shortcomings (Table). | 1, 9 |
| [T5] | Taleb, N.N. (1997). *Dynamic Hedging.* p.118 — "Orthodox definition of the delta." | 2 |
| [H1] | Hull, J.C. (2018). *Options, Futures, and Other Derivatives*, 10th ed. Pearson. Ch.19 — The Greek Letters. | 2, 3, 4, 6, 7 |
| [H2] | Hull, J.C. (2018). Ch.19, p.418 — Delta of a European call: N(d₁). | 2 |
| [H3] | Hull, J.C. (2018). Ch.19, p.428 — Gamma of a European call. | 4 |
| [H4] | Hull, J.C. (2018). Ch.19, p.434 — Vega of a European call. | 6 |
| [H5] | Hull, J.C. (2018). Ch.19, p.431 — Theta of a European call. | 7 |
| [BS] | Black, F. & Scholes, M. (1973). *The pricing of options and corporate liabilities.* J. Political Economy, 81(3), 637–654. | All |
| [IT] | Itô, K. (1944). *Stochastic integral.* Proc. Imperial Academy Tokyo, 20(8), 519–524. | 1 |

---

## PRODUCTION NOTES

```python
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
```

**Render commands:**
```bash
manim -pqh quantifaya_ep4.py FullEpisode --fps 60 --resolution 1920x1080
manim -pql quantifaya_ep4.py SceneDelta   # single scene test
```

---

---

## SCENE 1: COLD OPEN — THE WEAPONS RACK
**Class:** `SceneIntro` | **Duration:** ~1:30

### MANIM ANIMATION SEQUENCE

```
1. Black screen. Five Greek letters appear one by one — each with a
   physical-force animation, slamming into position from off-screen:

   Δ  —  slams in from left, gold, massive
   Γ  —  slams in from right, orange
   𝒱  —  drops from top, teal
   Θ  —  rises from bottom, red
   ρ  —  fades in last, purple (the quiet one)

2. Hold for 2 seconds. All five on screen simultaneously.
   Each letter pulses once.

3. Text appears below, letter by letter:
   "These are not symbols.
    They are the control panel of a $600 trillion market."

4. Each Greek letter gets a one-line label in small text:
   Δ → "How much the option moves when the stock moves"
   Γ → "How much Delta changes — the curvature you can't ignore"
   𝒱 → "The volatility exposure that bites harder than Delta"
   Θ → "The rent you pay every night for holding the position"
   ρ → "Interest rate sensitivity — the quiet assassin"

5. Taleb quote appears in gold italic:
   "The Greeks are derivatives of the option price.
    They are meaningful for a single option.
    They are treacherous for a book."
   — N.N. Taleb, Dynamic Hedging [T4]

6. Beat. Red text:
   "Your textbook taught you the formula.
    Today we teach you what they mean on a real desk."

7. QUANTIFAYA logo + episode title:
   "Episode 4: The Greeks — Delta, Gamma, Vega Built Intuitively"
   Subtitle: "From BS Formula → Real Trading Desk → Where They Break"
```

### VOICE-OVER SCRIPT

"Five letters. Delta. Gamma. Vega. Theta. Rho.

[PAUSE — letters slam in]

If you've spent any time around options, you've heard these words. Your textbook defined them. Your professor gave you the formulas. Your first Bloomberg terminal showed you the numbers.

What nobody told you — and what Nassim Taleb spells out in the opening chapters of Dynamic Hedging — is that these measures are meaningful for a single vanilla option, and treacherous the moment you run a book. [T4]

[PAUSE — Taleb quote]

The Greeks are partial derivatives of the option price with respect to market variables. They're local, first-and-second-order approximations of a nonlinear, path-dependent, volatility-sensitive payoff. On a single position, they're extraordinarily useful. Across a portfolio mixing long and short options of different strikes and maturities, they compound, cancel, and interact in ways that have ended more than a few careers.

[PAUSE — red text]

Today we build every major Greek from the Black-Scholes formula by differentiation. We show what each one means economically. We show what happens when you hedge with each one. And we tell you exactly where Taleb says they break — and what the professionals use instead.

Welcome to Episode 4. Let's arm up."

---

## SCENE 2: DELTA — THE FIRST DERIVATIVE
**Class:** `SceneDelta` | **Duration:** ~4:00

### MANIM ANIMATION SEQUENCE

```
1. Title: "Δ — Delta: The Hedge Ratio That Lies to You"
   Sources: "[T1] Taleb Ch.7 | [H1] Hull Ch.19 | [BS] Black & Scholes (1973)"

2. DEFINITION — two panels side by side:

   LEFT — Mathematical:
   \Delta = \frac{\partial C}{\partial S} = N(d_1)
   
   "The first partial derivative of the call price
    with respect to the stock price. [H2]"

   RIGHT — Practical:
   "The number of shares of stock you need to hold
    to replicate the option's price movement
    for an infinitely small move in S."

3. Delta derivation from Black-Scholes:
   
   C = S_0 N(d_1) - K e^{-rT} N(d_2)
   
   \frac{\partial C}{\partial S} = N(d_1) + S \cdot N'(d_1)\frac{\partial d_1}{\partial S}
                                   - Ke^{-rT} N'(d_2)\frac{\partial d_2}{\partial S}
   
   After simplification (the two cross-terms cancel):
   \Delta_{\text{call}} = N(d_1)
   
   Gold box. Hold.
   
   By put-call parity:
   \Delta_{\text{put}} = N(d_1) - 1 = -N(-d_1)

4. VISUAL — Delta as function of stock price:
   
   Axes: x = S (40 to 160), y = Delta (0 to 1)
   K = 100, T = 0.5, σ = 0.2, r = 0.05
   
   S-shaped sigmoid curve from 0 to 1 in blue.
   
   Key points labeled:
   • Deep OTM (S=70): Δ ≈ 0.05    "Lottery ticket"
   • ATM (S=100):     Δ ≈ 0.50    "50-50 call"
   • Deep ITM (S=140): Δ ≈ 0.98   "Stock equivalent"
   
   Tangent line drawn at S=100 — THIS is the instantaneous hedge.
   
   Arrow: "As S moves from 100 to 101, option gains ≈ Δ × $1"

5. DELTA ACROSS TIME TO EXPIRY:
   
   Three curves — T = 1 year (smooth), T = 1 month (steeper),
   T = 1 day (nearly binary — almost a step function)
   
   "As expiry approaches, the S-curve steepens.
    A 1-day ATM option goes from Δ=0 to Δ=1 as the stock crosses the strike.
    Gamma explosion — preview of Scene 4."

6. TALEB ON DELTA — flash quote:
   
   "Orthodox definition of delta: dF/dU — the derivative of
    the option price to the underlying.
    From a standpoint of trading, it offers no significance,
    for the following reasons:
    There is no such thing as an infinitely small move in the market.
    If there were such microscopic moves they would be nobody's concern."
   — Taleb, Dynamic Hedging, p.118 [T5]
   
   Beat. Then:
   "The delta is the tangent line.
    Markets don't move along tangent lines.
    They gap. They jump. They close on Fridays and open Monday 3% away."

7. DELTA HEDGING — how it actually works:

   Numerical example:
   S = $100, K = $100, T = 6 months, σ = 20%, r = 5%
   Call price C = $10.45  (BS formula)
   Δ = N(d₁) = 0.5793
   
   "Short 1 call option. Need to buy 0.5793 shares to be delta-neutral."
   
   Π = 0.5793 × S - C = 0.5793 × 100 - 10.45 = $47.48
   
   "If S moves to $101 — one dollar move:"
   New C ≈ $10.45 + 0.5793 × $1 = $11.03  (Delta approx)
   New Π = 0.5793 × 101 - 11.03 = $47.49  ← nearly unchanged
   
   "That's delta hedging. Local. Instantaneous. Requires continuous rebalancing.
    In continuous time: perfect. In real markets: an approximation."

8. Source tags: "[T1] Taleb, Dynamic Hedging, Ch.7 | [H2] Hull (2018), p.418"
```

### VOICE-OVER SCRIPT

"Delta. The first Greek. The first derivative of the call price with respect to the stock price. And the most misunderstood number in options trading.

[PAUSE — definition panels]

Mathematically, Delta is the partial derivative of the call price C with respect to the stock price S. From the Black-Scholes formula, this turns out to equal N of d₁ — the Normal CDF evaluated at d₁. For a put, it's N of d₁ minus one — which is always negative, because puts move inversely with the stock. [H2]

[PAUSE — show derivation]

We can derive this cleanly. Differentiate the Black-Scholes formula for C. You get N of d₁ plus two cross-terms involving the Normal density. Those two cross-terms cancel exactly — it's a clean cancellation that requires a few lines of algebra to verify but is a standard result. You're left with Delta equals N of d₁. [BS]

[PAUSE — show S-curve]

Economically, Delta ranges from zero to one for calls, from negative one to zero for puts. A deep out-of-the-money call with Delta of five percent behaves like five cents of stock per dollar. A deep in-the-money call with Delta of ninety-eight percent behaves almost identically to holding the stock outright. At the money, Delta is approximately fifty percent — which is why options traders sometimes call an ATM option a 'fifty-delta.' [H1]

[PAUSE — show time curves]

As expiry approaches, the Delta curve steepens. A one-day ATM option has Delta that flips from near-zero to near-one as the stock crosses the strike. That's the Gamma bomb we'll discuss in Scene 4.

[PAUSE — Taleb quote]

But here's where Taleb draws first blood. His Chapter 7 is titled 'Adapting Black-Scholes-Merton: The Delta,' and he opens with a direct attack on the textbook definition. [T5] The mathematical delta — dF over dU — is the hedge ratio for an infinitely small move. In practice: there is no such thing as an infinitely small move in the market. Markets gap. Markets close on Friday and open on Monday three percent away. The delta is a tangent line, and markets don't move along tangent lines.

[PAUSE — numerical example]

Here's what delta hedging actually looks like. Stock at a hundred, ATM call, six-month maturity, twenty percent vol. Black-Scholes gives us a call price of roughly ten forty-five and a delta of fifty-eight percent. To delta-hedge a short call, I buy 0.5793 shares. My portfolio value is flat to small stock moves. If the stock moves one dollar, the option gains approximately fifty-eight cents — covered by my share position. Perfect in continuous time. An approximation in discrete time, with a residual error that grows with the square of the move. That residual error is Gamma. We'll get there."

---

## SCENE 3: DELTA IN PRACTICE — WHERE THE TEXTBOOK ENDS
**Class:** `SceneDeltaPractice` | **Duration:** ~2:00

### MANIM ANIMATION SEQUENCE

```
1. Title: "Delta in Practice — The Lies Your Risk System Tells You"
   Source: "[T1] Taleb, Dynamic Hedging, Ch.7, pp.118–125"

2. PROBLEM 1 — Delta doesn't aggregate cleanly across a book:
   
   Taleb example from p.133 [T1]:
   
   Position:
   • Long $1M of 96 calls, Δ = 0.824  →  Net delta: +$824,000
   • Short $1M of 104 calls, Δ = 0.198  →  Net delta: −$198,000
   • Total delta: +$626,000
   
   "Risk system says: hedge by selling $626,000 of forward.
    But look at the P&L across spot levels..."
   
   Show P&L chart: position has long delta everywhere EXCEPT
   near S=100 where it's locally flat.
   
   "The TOTAL delta is useless. The LOCAL delta at each spot level
    is what matters. This is a call spread. It looks like
    a long position at every spot — except the origin.
    The textbook hedge is wrong."

3. PROBLEM 2 — Delta breaks entirely on barrier options:
   
   Taleb anecdote from p.131 [T1]:
   "A risk manager vetoed a barrier option trade because the delta
    reached 10,000% at the barrier.
    The trader's maximum loss was $400,000 on a $5M trade.
    The delta implied $500M of equivalent exposure.
    Both numbers were technically correct. Neither was useful."
   
   Visual: Delta of a knock-out option — spikes to infinity at barrier.
   
   "Delta can be infinite. The loss cannot be.
    This is what Taleb means by 'the delta is a weak measure of risk.'" [T4]

4. SOLUTION — Discrete Delta:
   
   "Use the DISCRETE DELTA:
    Δ_discrete = [C(S+ΔS) − C(S−ΔS)] / (2ΔS)
    
    with ΔS chosen to match realistic move size — say 1 or 2 sigma."
   
   "This bakes in a little gamma and a little vega automatically.
    It's less 'pure' mathematically. It's more honest operationally." [T1]
```

### VOICE-OVER SCRIPT

"Let's go one level deeper — to where the textbook definition of delta breaks in practice. Taleb devotes most of Chapter 7 to this, and it's worth understanding. [T1]

[PAUSE — book problem]

Consider a portfolio: long one million of the ninety-six calls, short one million of the one-oh-four calls. The system computes total delta as positive six hundred and twenty-six thousand. Hedge accordingly — sell six-twenty-six of forward. Done. Clean.

Except it's not. Map the P&L across spot levels and you see a position that looks like a long everywhere — except near the origin, where it's locally flat. The total delta is an aggregate that disguises the local structure. The hedge is misleading. [T1]

[PAUSE — barrier problem]

The second failure is more dramatic. Taleb describes a real argument on a trading floor: a risk manager vetoed a barrier option trade because the delta at the barrier was ten thousand percent — implying five hundred million dollars of equivalent stock exposure on a five-million-dollar trade. The trader's maximum loss was four hundred thousand dollars. Both numbers were mathematically correct. Neither was operationally useful. [T1]

[PAUSE — discrete delta solution]

Taleb's prescription: use the discrete delta. Instead of the continuous partial derivative, compute the option price change over a realistic — one or two sigma — move up and down, and divide by twice the move size. This naturally incorporates a portion of the gamma and vega exposure. Less elegant mathematically. Far more honest as a risk measure. This is the difference between a textbook and a trading desk."

---

## SCENE 4: GAMMA — THE CURVATURE THAT COSTS YOU
**Class:** `SceneGamma` | **Duration:** ~4:00

### MANIM ANIMATION SEQUENCE

```
1. Title: "Γ — Gamma: The Curvature That Costs You Every Day"
   Sources: "[T2] Taleb Ch.8 | [H3] Hull (2018), p.428"

2. DEFINITION:
   \Gamma = \frac{\partial^2 C}{\partial S^2}
          = \frac{\partial \Delta}{\partial S}
          = \frac{N'(d_1)}{S\sigma\sqrt{T}}
   
   where N'(d_1) = \frac{1}{\sqrt{2\pi}} e^{-d_1^2/2}
   (the standard Normal PDF — always positive)
   
   "Gamma is always positive for long options — calls AND puts.
    Gamma is always negative for short options.
    It measures the curvature of the option's price — the acceleration
    of Delta as S moves."

3. GEOMETRIC INTUITION — the Taylor expansion connection:

   From Ep.2: the Taylor expansion of C in dS:
   dC = \Delta\,dS + \frac{1}{2}\Gamma\,(dS)^2 + \cdots
   
   "Delta gives you the linear term.
    Gamma gives you the quadratic term — the curvature correction.
    If Gamma is positive, you always make MORE than Delta predicts
    on large moves. You gain on the upside AND downside.
    This is called being LONG GAMMA."
   
   Visual: Parabola opening UPWARD for long gamma.
   vs. Tangent line (Delta-only approximation).
   Gap between parabola and line = Gamma P&L.

4. LONG GAMMA vs SHORT GAMMA — the battle:

   Two panels animated side by side:
   
   LEFT — LONG GAMMA (e.g., you bought a call):
   • Big up move: you gain MORE than Delta said
   • Big down move: you lose LESS than Delta said
   • Gamma P&L always POSITIVE: ½Γ(ΔS)² > 0
   • But: you PAID for this via time decay (Theta — see Scene 7)
   
   RIGHT — SHORT GAMMA (e.g., you sold a call):
   • Big up move: you lose MORE than Delta said
   • Big down move: you gain LESS than Delta said
   • Gamma P&L always NEGATIVE: ½Γ(ΔS)² < 0
   • But: you RECEIVE time decay daily
   
   The fundamental trade-off:
   "Long Gamma = pay Theta to own convexity
    Short Gamma = collect Theta, exposed to large moves"

5. GAMMA AS FUNCTION OF S AND T:

   Two plots:
   
   Plot A (Gamma vs S):
   Bell-shaped curve peaked at ATM (S ≈ K)
   "Gamma is maximum at-the-money. Zero deep OTM and ITM."
   
   Plot B (Gamma vs T):
   Three curves: T=1yr (flat, low), T=1mo (taller, narrower),
   T=1day (very tall, very narrow spike at S=K)
   
   "GAMMA EXPLOSION near expiry at-the-money.
    A 1-day ATM option has essentially infinite Gamma at S=K.
    A market maker short that option on expiry day is in trouble
    if the stock oscillates around the strike."

6. TALEB: UP-GAMMA and DOWN-GAMMA [T2]:
   
   "The conventional gamma is symmetric — same up and down.
    On a book with a vol skew, you need asymmetric gamma.
    
    UP-GAMMA: ΔDelta / ΔS for an upward move
    DOWN-GAMMA: ΔDelta / ΔS for a downward move
    
    In equity markets with skew: DOWN-GAMMA > UP-GAMMA
    A down move causes both a delta change AND a vol increase —
    the shadow gamma is larger than the conventional gamma."
   
   Show Table 8.2 data from Taleb p.136 [T2]:
   Example risk reversal — down-gamma consistently > up-gamma.
   
   "This is what Taleb calls SHADOW GAMMA — the gamma that
    accounts for the correlation between spot moves and vol moves." [T2]

7. GAMMA P&L FORMULA — the daily mark:
   
   Daily Gamma P&L = ½ × Γ × (ΔS)²
   
   Annualized gamma P&L per day:
   ½ × Γ × σ²S² = ½ × σ²S² × N'(d₁)/(Sσ√T)
                  = ½ × σ√(1/T) × S × N'(d₁)
   
   "If you're long gamma, you earn this P&L on every large move.
    If you're short gamma, you lose it.
    And the market extracts it from you via Theta — every single night."

8. Source box: "[T2] Taleb, Dynamic Hedging, Ch.8, pp.127–162
               [H3] Hull (2018), Options..., p.428"
```

### VOICE-OVER SCRIPT

"Gamma. The second derivative of the option price with respect to the stock price. Or equivalently — the rate of change of Delta. And the most important risk measure that junior traders systematically underestimate. [H3]

[PAUSE — definition]

From Black-Scholes, Gamma equals the Normal density N prime of d₁, divided by S times sigma times the square root of T. The Normal density is always positive. So Gamma is always positive for long options — whether calls or puts — and always negative for short options.

[PAUSE — Taylor expansion connection]

Here's the key geometric insight, and it connects directly to Episode 2. The full change in option price for a stock move dS is Delta times dS plus one-half Gamma times dS squared — this is the Taylor expansion, with the Itô correction sitting right there in the Gamma term. [IT] Delta is the linear approximation. Gamma is the curvature correction. If you're long Gamma, the actual price change is always larger than Delta predicts — you gain more on up moves and lose less on down moves than a linear hedge would suggest. Always.

[PAUSE — long vs short gamma panels]

This is the central trade in options. Long Gamma means you own convexity — every large move benefits you. Short Gamma means you sold convexity — every large move hurts you. The catch: you pay for long Gamma through time decay — Theta bleeds you every night. And you collect Theta by being short Gamma — but you're exposed to every gap, every earnings surprise, every central bank shock. This trade-off is the engine of every options desk on earth.

[PAUSE — Gamma vs S, Gamma vs T]

The Gamma profile across spot is a bell curve — maximum at-the-money, collapsing toward zero for deep in-the-money and out-of-the-money options. [H3] Across time, Gamma concentrates. A one-year ATM option has low, stable Gamma. A one-day ATM option has Gamma that spikes violently — essentially infinite right at the strike. Being short a one-day ATM straddle with the stock oscillating around the strike is how options market makers have career-ending days.

[PAUSE — Taleb's up/down gamma]

Now here's what Taleb adds that Hull doesn't emphasize. [T2] The conventional Gamma assumes symmetry — same sensitivity to up moves and down moves. In markets with a volatility skew — which is all equity markets since 1987 — this is wrong. When a stock falls, volatility typically rises simultaneously. The effective Gamma on a down move is larger than the mathematical Gamma, because you're getting both the delta change and the vol move compounding against you. Taleb calls this the Shadow Gamma. And his prescription: compute Up-Gamma and Down-Gamma separately. The textbook number is the average of two different risk numbers."

---

## SCENE 5: GAMMA IN PRACTICE — THE DAILY BATTLE
**Class:** `SceneGammaPractice` | **Duration:** ~2:00

### MANIM ANIMATION SEQUENCE

```
1. Title: "Gamma in Practice — What the Daily P&L Actually Looks Like"
   Source: "[T2] Taleb, Dynamic Hedging, pp.127–145"

2. THE GAMMA P&L EQUATION — concrete numbers:
   
   Setup:
   S = $100, K = $100, T = 30 days, σ = 20%, r = 5%
   Γ = 0.0668  (per dollar squared)
   
   Scenario A — Quiet day, ΔS = $0.50:
   Gamma P&L = ½ × 0.0668 × (0.50)² = $0.0084 per option
   "Almost nothing. Gamma earns nothing in calm markets."
   
   Scenario B — Big day, ΔS = $3.00:
   Gamma P&L = ½ × 0.0668 × (3.00)² = $0.30 per option
   "Thirty cents of gamma profit on a single option, single day."
   
   Scenario C — Crash, ΔS = $10.00:
   Gamma P&L = ½ × 0.0668 × (10.00)² = $3.34 per option
   "A crisis is Christmas for long gamma."
   
   Key: Gamma P&L scales as (ΔS)². Double the move, FOUR TIMES the gamma P&L.

3. THE GAMMA TRAP — being short near expiry:
   
   Visual timeline:
   Day -30: Gamma = 0.0668. Manageable.
   Day -5:  Gamma = 0.180. Starting to bite.
   Day -1:  Gamma = 0.520. Dangerous.
   Day 0 (expiry, ATM): Gamma → ∞
   
   "The market maker who sold you that option needs to delta-hedge
    continuously on expiry day. Every time the stock crosses the strike,
    the delta flips from 0 to 1.
    If the stock oscillates across the strike 10 times — he rebalances 10 times.
    Each rebalancing costs bid-ask. He bleeds to death hedging costs."

4. TALEB SYLDAVIA CASE STUDY — Shadow Gamma in action [T2]:
   
   "Taleb's Chapter 8 illustrates this with the 'Syldavian elections' —
    a fictional currency facing binary political outcomes.
    
    Before election: vol = 20%
    If pro-market wins: vol drops to 14%, spot stays ~100
    If anarchists win: vol jumps to 29%, spot drops to 94
    
    The conventional gamma said one thing.
    The shadow gamma — accounting for the vol jump on the down move —
    said something completely different.
    
    The trader who ignored shadow gamma was positioned wrong." [T2]
   
   "Markets don't move independently of volatility.
    Vol and spot are correlated. Your gamma model needs to know that."
```

### VOICE-OVER SCRIPT

"Let's make Gamma concrete with numbers, because this is where the money is.

[PAUSE — gamma P&L scenarios]

ATM option, thirty days to expiry, twenty percent vol. Gamma is approximately 0.0668. On a quiet day where the stock moves fifty cents — Gamma earns less than one cent per option. Barely visible. On a three-dollar move, Gamma earns thirty cents per option. On a ten-dollar move — a crash — Gamma earns three dollars and thirty-four cents per option. On a position of ten thousand options, that's thirty-four thousand dollars in a single day.

The crucial point: Gamma P&L scales with the square of the move. Double the move, four times the Gamma P&L. This is why large moves are Christmas for long gamma books and catastrophic for short gamma desks.

[PAUSE — gamma trap near expiry]

Near expiry, the trap closes. Gamma of an ATM option explodes as time runs out. A market maker short ATM options on expiry day faces Gamma that approaches infinity as the stock oscillates around the strike. Every time the stock crosses the strike price, Delta flips from zero to one — the option goes from worthless to dollar-for-dollar with the stock in a single tick. The market maker must delta-hedge every time. Each rebalance pays bid-ask spread. On a volatile expiry day with ten crossings, the hedging cost can exceed the entire premium collected for selling the option.

[PAUSE — Taleb Syldavia case]

Taleb illustrates shadow Gamma with his 'Syldavian elections' case study — one of the best pedagogical examples in Dynamic Hedging. [T2] A currency facing a binary political outcome: anarchists win and the currency drops ten percent with volatility spiking to twenty-nine percent; the pro-market party wins and spot holds with vol dropping to fourteen. The conventional Gamma gave a number. The shadow Gamma — which accounts for the correlated vol and spot move — gave a completely different position sizing. The trader who relied on the textbook Gamma was exposed. The one who computed shadow Gamma was prepared."

---

## SCENE 6: VEGA — THE VOLATILITY EXPOSURE
**Class:** `SceneVega` | **Duration:** ~3:30

### MANIM ANIMATION SEQUENCE

```
1. Title: "𝒱 — Vega: The Greek That Traders Fear More Than Delta"
   Sources: "[T3] Taleb, Dynamic Hedging, Ch.9 | [H4] Hull (2018), p.434"

2. DEFINITION from Black-Scholes:
   
   \mathcal{V} = \frac{\partial C}{\partial \sigma}
               = S\sqrt{T}\,N'(d_1)
   
   where N'(d_1) = \frac{1}{\sqrt{2\pi}} e^{-d_1^2/2}
   
   "Vega is the sensitivity of the option price to a one-unit
    change in implied volatility.
    A Vega of 0.20 means: if vol rises 1% (say from 20% to 21%),
    the option price increases by $0.20."
   
   Note: "Vega is NOT a Greek letter. It's made up.
    Some firms call it kappa (κ) or zeta (ζ).
    Taleb notes traders also call it lambda.
    The industry uses Vega. We use Vega." [T3]

3. DERIVATION — differentiate BS with respect to σ:
   
   C = S N(d_1) - K e^{-rT} N(d_2)
   
   \frac{\partial C}{\partial\sigma} = S N'(d_1)\frac{\partial d_1}{\partial\sigma}
                                      - Ke^{-rT} N'(d_2)\frac{\partial d_2}{\partial\sigma}
   
   Since d_1 - d_2 = σ√T:
   \frac{\partial d_1}{\partial\sigma} = \frac{\partial d_2}{\partial\sigma} + \sqrt{T}
   
   After simplification (using S N'(d₁) = K e^{-rT} N'(d₂)):
   \mathcal{V} = S\sqrt{T}\,N'(d_1)
   
   Gold box. "Simple. Beautiful. Powerful."

4. VEGA PROFILE — two plots:
   
   Plot A (Vega vs S):
   Bell curve peaked at ATM. Same shape as Gamma but different scaling.
   "Maximum Vega at-the-money. Collapses OTM and ITM.
    OTM options that are deeply out: low Vega — vol doesn't matter much
    if you're not going to exercise."
   
   Plot B (Vega vs T):
   Vega INCREASES with time to expiry.
   V = S√T × N'(d₁) — the √T factor.
   "A 1-year option has twice the Vega of a 3-month option.
    Long-dated options carry more vol risk. Always."
   
   "This is why a 2-year ATM swaption has massive Vega —
    you're long a lot of volatility for a long time."

5. TALEB ON VEGA AND GAMMA RELATIONSHIP [T3]:
   
   Key insight from p.163 [T3]:
   "Vega is related to gamma in a strange way.
    Vega is the integral of the gamma profits
    (the expected gamma rebalancing P&L over the option's life)."
   
   Mathematical relationship:
   \mathcal{V} = \Gamma \cdot S^2 \cdot \sigma \cdot T
   
   "If you know your Gamma and your vol, you know your Vega.
    They are not independent sensitivities.
    A portfolio that is Gamma-neutral and Vega-neutral at the same
    strike and maturity is actually flat everything.
    But across strikes and maturities, they diverge." [T3]

6. VEGA AND THE VOL SURFACE — modified vega [T3]:
   
   Taleb p.165 [T3]:
   "The modified vega corresponds to the sensitivity of the options
    portfolio to nonparallel changes in the general level of volatility."
   
   \mathcal{V}_{\text{modified}} = \sum_{i=1}^{n} \mathcal{V}_i \cdot F_i
   
   "where F_i is the volatility weight for each maturity bucket.
    Shorter maturities are usually more sensitive to spot vol moves.
    Longer maturities are more sensitive to term structure changes."
   
   Visual: Vol surface — parallel shift vs. twisting rotation.
   "Parallel shift: normal vega captures it.
    Vol surface twisting: you need bucket vega — vega at each maturity.
    A book with zero total vega can still lose massively
    if the short end spikes and the long end stays flat."

7. VEGA RISK MANAGEMENT:
   
   Scoreboard:
   ATM option Vega = S√T × N'(d₁) ≈ S√T × 0.3989
   
   Example: S=$100, T=1yr:
   V ≈ 100 × 1 × 0.3989 = $39.89 per 100% vol change
   ≈ $0.399 per 1% vol change
   
   "A desk long 10,000 calls:
    Vega exposure = 10,000 × $0.399 = $3,990 per 1% vol move.
    A 5% vol spike = $19,950 gain. Instantly.
    A 5% vol collapse = $19,950 loss. Instantly.
    And vol can move 5% in a morning."
```

### VOICE-OVER SCRIPT

"Vega. The volatility Greek. Not technically a Greek letter — Taleb notes it's sometimes called kappa or zeta or lambda depending on which desk you're on. The industry standardized on Vega. We'll go with the industry. [T3]

[PAUSE — definition]

Vega is the partial derivative of the option price with respect to implied volatility. From Black-Scholes, it equals S times the square root of T times the standard Normal density evaluated at d₁. [H4] It's always positive for long options — more volatility means higher option price, regardless of direction.

[PAUSE — derivation]

Differentiate the Black-Scholes formula with respect to sigma. You get two terms involving the Normal density N prime of d₁ and N prime of d₂. There's a useful identity: S times N prime of d₁ equals K e to the minus rT times N prime of d₂. The two terms collapse. Vega equals S root T N prime of d₁. Clean.

[PAUSE — vega profiles]

The Vega profile across spot is the same bell shape as Gamma — maximum at-the-money, zero deep in or out of the money. But across time, Vega behaves differently from Gamma. Vega scales with the square root of T — longer-dated options carry more Vega. A one-year option has twice the Vega of a three-month option. Long-dated positions are long-dated volatility bets. [H4]

[PAUSE — Taleb on Vega-Gamma relationship]

Here's the connection Taleb draws in Chapter 9 that most textbooks miss. [T3] Vega is actually the integral of expected Gamma rebalancing profits over the option's life. Mathematically, Vega equals Gamma times S squared times sigma times T. They're not independent measures — they're related by the volatility and time parameters. Which means a portfolio that hedges Gamma and Vega at the same strike and maturity is fully hedged. But across a book with different strikes and maturities, Gamma and Vega can diverge — your Gamma exposure is concentrated near-term ATM while your Vega exposure is spread across the vol surface. They require separate management.

[PAUSE — modified vega and vol surface]

Taleb's Chapter 9 introduces modified Vega — sensitivity to non-parallel shifts in the vol surface. [T3] A book with zero total Vega can still lose money if the short end of the vol curve spikes while the long end stays flat. That's a twist, not a parallel shift. Bucket Vega — Vega at each maturity separately — is what risk managers on serious books actually monitor.

[PAUSE — concrete numbers]

One-year ATM option on a hundred-dollar stock. Vega is approximately forty cents per one-percent vol move. A desk long ten thousand of these has four thousand dollars of Vega per vol tick. A five-percent vol spike generates twenty thousand dollars of profit — instantly, before the delta even moves. Vol can move five percent in a morning. Vega is not a secondary concern."

---

## SCENE 7: THETA — THE RENT
**Class:** `SceneTheta` | **Duration:** ~2:30

### MANIM ANIMATION SEQUENCE

```
1. Title: "Θ — Theta: The Rent You Pay Every Night"
   Sources: "[H5] Hull (2018), p.431 | [T2] Taleb, Ch.8 (Gamma/Theta relationship)"

2. DEFINITION:
   \Theta = \frac{\partial C}{\partial t} = -\frac{\partial C}{\partial \tau}
   
   For a European call (no dividends):
   \Theta = -\frac{S N'(d_1)\sigma}{2\sqrt{T}} - rKe^{-rT}N(d_2)
   
   "Theta is NEGATIVE for long options.
    Time passing HURTS option holders. Every day you hold an option,
    it loses some of its time value.
    Theta is the daily rent for being long optionality."

3. THETA vs S — the curve:
   
   Plot: x = S (60 to 140), y = Theta (negative, below zero)
   
   Theta is most negative at ATM — peaks in magnitude near K.
   Deep OTM and ITM: smaller Theta (less time value to decay).
   
   "ATM options have the most time value. They decay fastest.
    Deep OTM options cost little — they also decay to zero, but slowly.
    Deep ITM options decay slowly because they're mostly intrinsic value."

4. THE GAMMA-THETA TRADE-OFF — the most important identity in options:
   
   From the Black-Scholes PDE (Episode 3):
   \Theta + \frac{1}{2}\sigma^2 S^2 \Gamma = rC - rS\Delta
   
   For a delta-hedged position where rC ≈ rSΔ (ATM approximation):
   \Theta \approx -\frac{1}{2}\sigma^2 S^2 \Gamma
   
   Gold box. Hold 3 seconds.
   
   "THE GAMMA-THETA IDENTITY:
    Theta ≈ −½σ²S²Γ
    
    If you're long Gamma, you PAY Theta every night.
    If you're short Gamma, you COLLECT Theta every night.
    
    The question is ALWAYS:
    'Am I collecting enough Theta to compensate for my Gamma exposure?'"

5. THETA ACCELERATION near expiry:
   
   Plot: x = Days to expiry (90 to 0), y = |Theta|
   
   Curve accelerates as expiry approaches — not linear.
   
   "Theta decay is not uniform. It accelerates.
    An option loses roughly:
    ~1/3 of its time value in the LAST MONTH of a 3-month option
    ~50% of its remaining value in the LAST WEEK.
    Weekend effect: Friday close to Monday open = 3 days of Theta.
    That's why option sellers love Fridays." [H5]

6. Concrete example:
   S=$100, K=$100, T=30 days, σ=20%
   Theta = −$0.054 per day
   "This option decays 5.4 cents per calendar day.
    $1.62 per month — on a ~$2.20 ATM option.
    That's why short option sellers sleep well in quiet markets
    and very badly when vol spikes."
```

### VOICE-OVER SCRIPT

"Theta. The time decay Greek. The one that makes option selling feel like being a landlord — collect rent every day, hope there are no catastrophes.

[PAUSE — definition]

From Black-Scholes, Theta for a European call is negative one-half times S times N prime of d₁ times sigma, divided by the square root of T, minus r times K times e to the minus rT times N of d₂. [H5] It's always negative for long options. Time passing — with everything else held constant — reduces an option's value. Every single day.

[PAUSE — show Theta profile]

The Theta profile mirrors the Gamma bell curve — maximum magnitude at-the-money, smaller for deep in or out-of-the-money options. ATM options have the most time value and decay fastest. This is not a coincidence — it's built into the structure of Black-Scholes.

[PAUSE — GAMMA-THETA IDENTITY]

Here's the most important single identity in options risk management — and it falls directly out of the Black-Scholes PDE from Episode 3. For a delta-hedged position, Theta is approximately equal to minus one-half sigma squared S squared times Gamma.

[PAUSE — hold on identity]

Read that again. Theta equals negative Gamma times a constant. If you're long Gamma, you're paying Theta every night. If you're short Gamma, you're collecting it. The Gamma-Theta trade-off is not a coincidence — it's a mathematical identity embedded in the PDE. Being long convexity costs time. Being short convexity earns time. The market prices this exactly.

[PAUSE — Theta acceleration]

And Theta accelerates. An option doesn't decay linearly. It loses roughly a third of its time value in the final month of a three-month option's life — far more than in the first month. Weekend effect: a position held over Friday close decays three calendar days by Monday open, because Theta ticks through weekends even when markets are closed. This is why options sellers love Fridays and options buyers dread them."

---

## SCENE 8: RHO & THE GREEKS TOGETHER — THE FULL DASHBOARD
**Class:** `SceneRhoAndDashboard` | **Duration:** ~2:00

### MANIM ANIMATION SEQUENCE

```
1. Title: "ρ — Rho & The Full Greeks Dashboard"
   Source: "[H1] Hull (2018), Ch.19"

2. RHO — the quiet assassin:
   \rho = \frac{\partial C}{\partial r} = KTe^{-rT}N(d_2)
   
   "Rho is the sensitivity to the risk-free rate.
    Positive for calls — higher rates increase call value
    (you save on the cost of holding the stock).
    Negative for puts.
    
    Usually the smallest Greek for equity options.
    DOMINATES for long-dated interest rate derivatives
    and currency options where the rate differential is the point."

3. THE FULL GREEKS DASHBOARD — animated table:
   
   Example: S=$100, K=$100, T=6mo, σ=20%, r=5%
   
   ┌──────┬────────────────────┬──────────────────┬───────────────────────────┐
   │Greek │ Formula            │ Value            │ Meaning                   │
   ├──────┼────────────────────┼──────────────────┼───────────────────────────┤
   │  Δ   │ N(d₁)              │  0.5793          │ 0.58 shares to hedge      │
   │  Γ   │ N'(d₁)/(Sσ√T)     │  0.0267          │ $0.027 delta gain per $1  │
   │  𝒱   │ S√T·N'(d₁)        │ 28.22            │ $0.28 per 1% vol move     │
   │  Θ   │ −SN'(d₁)σ/2√T−rKe^{−rT}N(d₂) │ −$0.038/day │ 3.8¢/day decay │
   │  ρ   │ KTe^{−rT}N(d₂)    │ 23.37            │ $0.23 per 1% rate move    │
   └──────┴────────────────────┴──────────────────┴───────────────────────────┘

4. TAYLOR EXPANSION — the full P&L equation:
   
   \Delta C \approx \Delta\,\Delta S
                  + \frac{1}{2}\Gamma\,(\Delta S)^2
                  + \mathcal{V}\,\Delta\sigma
                  + \Theta\,\Delta t
                  + \rho\,\Delta r
   
   "THIS is the options trader's P&L equation.
    Every morning, before the market opens, you know your greeks.
    Every afternoon, you know what moved.
    You can attribute every dollar of P&L to a Greek.
    If you can't, you don't understand your book."
   
   Each term labelled:
   Δ·ΔS     → "Linear stock move P&L"
   ½Γ(ΔS)²  → "Gamma P&L — curvature benefit"
   𝒱·Δσ     → "Vega P&L — vol move"
   Θ·Δt     → "Time decay — the daily rent"
   ρ·Δr     → "Rate move P&L"

5. P&L ATTRIBUTION EXAMPLE:
   
   Yesterday's moves: ΔS = +$2, Δσ = −0.5%, Δt = 1 day
   
   ΔC ≈ 0.5793×2 + ½×0.0267×4 + 28.22×(−0.005) + (−0.038)×1
       ≈ $1.159  + $0.053   − $0.141           − $0.038
       ≈ $1.033
   
   "The stock helped. Gamma helped. Vol hurt. Theta hurt.
    Net: the option gained about a dollar.
    Every options trader runs this calculation daily."
```

### VOICE-OVER SCRIPT

"Before we put it all together — Rho. The interest rate Greek. From Black-Scholes, Rho for a call equals K times T times e to the minus rT times N of d₂. [H1] Positive for calls — higher rates reduce the present value of the strike you pay, making the call more valuable. For equity options at typical rates and maturities, Rho is the smallest Greek and receives the least attention. For long-dated interest rate derivatives or currencies where the rate differential IS the trade — Rho is everything.

[PAUSE — full dashboard]

Now the complete dashboard. For an ATM six-month option on a hundred-dollar stock with twenty percent vol and five percent rates: Delta is fifty-eight percent, Gamma is 0.0267, Vega is twenty-eight dollars per hundred percent vol change — or twenty-eight cents per one percent move — Theta is negative three point eight cents per day, and Rho is twenty-three dollars per one percent rate move.

[PAUSE — Taylor expansion P&L]

Here's why this matters operationally. The change in option value for any set of market moves decomposes exactly across the Greeks: Delta times the stock move, plus half Gamma times the squared stock move, plus Vega times the vol move, plus Theta times the time elapsed, plus Rho times the rate move.

This is the options trader's daily P&L equation. If you can compute your Greeks every morning, and you observe what moved during the day, you can attribute every dollar of P&L to its source. Delta gave you this. Gamma gave you that. Vol hurt you here. Theta bled you there.

[PAUSE — P&L attribution example]

Concretely: stock up two dollars, vol down half a percent, one day of time. Delta P&L: one dollar fifteen. Gamma P&L: five cents. Vega P&L: minus fourteen cents. Theta: minus four cents. Net: the option gained about a dollar three. That's P&L attribution. That's how a real desk understands what happened each day."

---

## SCENE 9: TALEB'S SHORTCOMINGS TABLE — THE REAL TALK
**Class:** `SceneTalebShortcomings` | **Duration:** ~2:30

### MANIM ANIMATION SEQUENCE

```
1. Title: "The Greeks — And Their Shortcomings"
   Subtitle (gold italic): "What Taleb's table on page 112 says that no textbook will."
   Source: "[T4] Taleb, Dynamic Hedging, p.112"

2. REPRODUCE Taleb's shortcomings table (p.112) — animated, one Greek at a time:
   
   DELTA:
   Definition: "Sensitivity to underlying price"
   Shortcoming [T4]: "Continuous-time hedging is for the textbook.
                       Delta does not work on a portfolio of options
                       that mixes longs and shorts.
                       It is an extremely weak measure of risks."
   Modification: "Use a discrete delta with realistic increments.
                  Shadow delta adds some vegas and gammas to it."
   
   → Visual: Discontinuous P&L vs delta's straight-line prediction

   GAMMA:
   Definition: "Rate of change / curvature of the delta"
   Shortcoming [T4]: "It is meaningless for a portfolio of options.
                       It does not take into account changes in volatility
                       when the market moves."
   Modification: "Use discrete increments. Examine Up-Gamma and Down-Gamma.
                  Shadow gamma accounts for the vol smile."
   
   → Visual: Normal gamma vs shadow gamma on a skewed market

   THETA:
   Definition: "Sensitivity of portfolio to time passage"
   Shortcoming [T4]: "It does not take into account changes in volatility
                       that co-occur with time passage."
   Modification: "Use a term structure of volatilities to adjust."
   
   → Visual: Theta bleeding — flat line vs curved actual decay

   VEGA:
   Definition: "Sensitivity to implied volatility"
   Shortcoming [T4]: "Parallel shift assumption — it assumes all maturities
                       move by the same amount simultaneously."
   Modification: "Bucket vega — separate vega by maturity.
                  Modified vega uses volatility weights per maturity."
   
   → Visual: Vol surface twist vs parallel shift

3. THE META-LESSON — Taleb's point:
   
   Quote [T4]:
   "The conventional training of people, which consists of toying with
    the conventional derivatives of the Black-Scholes formula, has a
    negative effect on their operating style.
    Trading an option bears little relevance to trading a book."
   — Taleb, Dynamic Hedging, p.163 [T3]
   
   "A single option's Greeks are well-defined and useful.
    A book of options has Greeks that interact, cancel, and amplify
    in ways the formulas don't capture.
    The difference between knowing the formulas and managing a book
    is the difference between knowing piano scales and playing Carnegie Hall."
   — Quantifaya

4. WHAT THE DESK ACTUALLY RUNS:
   
   Visual: Risk dashboard of a real desk (stylized)
   
   Not just: Δ = 0.58, Γ = 0.027, 𝒱 = 28.22
   
   But:
   → Delta by strike bucket (not aggregate)
   → Gamma by maturity (near-dated vs. long-dated separately)
   → Vega by maturity bucket (bucket vega)
   → Up-Gamma and Down-Gamma (asymmetric)
   → Shadow gamma including vol-spot correlation
   → Scenario P&L: "What if spot drops 10% AND vol spikes 5%?"
   
   "THAT is a risk dashboard. The Greeks are the starting point.
    The scenario analysis is the actual risk management."
```

### VOICE-OVER SCRIPT

"Now for the most important two minutes of this episode — and they come directly from page one-twelve of Dynamic Hedging. Taleb includes a table — and I'm going to reproduce it because it should be mandatory reading for every quant and every options student.

[PAUSE — Delta shortcomings]

Delta. Definition: sensitivity to the underlying price. Textbook. Clean. Shortcoming, per Taleb: 'Delta does not work on a portfolio of options that mixes longs and shorts. It is an extremely weak measure of risks.' [T4] The prescription: use a discrete delta with realistic move sizes. The Shadow Delta adds vega and gamma contributions.

[PAUSE — Gamma shortcomings]

Gamma. Definition: rate of change of delta. Textbook. Shortcoming: 'It is meaningless for a portfolio of options. It does not take into account changes in volatility when the market moves.' [T4] The prescription: Up-Gamma and Down-Gamma separately. Shadow Gamma accounts for the vol-spot correlation.

[PAUSE — Theta and Vega shortcomings]

Theta: 'Does not take into account changes in volatility that co-occur with time passage.' Vega: 'Parallel shift assumption' — assumes all maturities move simultaneously. Neither is true in real markets. [T4]

[PAUSE — the meta-lesson]

The meta-lesson is this. Taleb writes in Chapter 9 — and I'm quoting directly: 'The conventional training of people, which consists of toying with the conventional derivatives of the Black-Scholes formula, has a negative effect on their operating style. Trading an option bears little relevance to trading a book.' [T3]

Single option Greeks: well-defined, analytically clean, useful for intuition. Book-level Greeks: they aggregate, they interact, they cancel in ways the formulas don't warn you about. The Greeks are the starting vocabulary. Scenario analysis — 'what if spot drops ten percent AND vol spikes five' — is the actual risk management.

If you're running a real options book on anything more complex than a single vanilla, you're running bucket Vegas, up-and-down gammas, and scenario matrices. The formulas from today are the foundation. The practice is considerably more demanding."

---

## SCENE 10: OUTRO — CTA AND NEXT EPISODE
**Class:** `SceneOutro` | **Duration:** ~1:00

### MANIM ANIMATION SEQUENCE

```
1. QUANTIFAYA logo pulses in purple.
   "Financial Engineering. Explained Rigorously. Applied Practically."

2. Episode recap — fly in:
   ✓  Delta = N(d₁) — the hedge ratio and its limits
   ✓  Discrete delta — Taleb's operational fix
   ✓  Gamma = N'(d₁)/(Sσ√T) — curvature, long/short gamma trade-off
   ✓  Up-Gamma / Down-Gamma / Shadow Gamma — skewed markets
   ✓  Gamma-Theta identity: Θ ≈ −½σ²S²Γ
   ✓  Vega = S√T·N'(d₁) — vol exposure and bucket vega
   ✓  Vega-Gamma relationship: 𝒱 = ΓS²σT
   ✓  Theta — the daily rent and its acceleration
   ✓  Full P&L attribution equation across all Greeks
   ✓  Taleb's shortcomings table — what the textbook won't tell you

3. Book recommendations:
   📚 "Dynamic Hedging" — Nassim Taleb (1997) [T1-T4]
   "The single best book on practitioner Greeks.
    Part II, Chapters 7–11. Read it twice.
    The second time you'll catch what the first time missed."
   
   📚 "Options, Futures, and Other Derivatives" — Hull (2018) [H1-H5]
   "Chapter 19 — The Greek Letters.
    The textbook foundation. Read Hull for the formulas,
    read Taleb for why the formulas aren't enough."

4. Comment challenge:
   "Prove the Gamma-Theta identity from the Black-Scholes PDE.
    Hint: start from ∂C/∂t + rS∂C/∂S + ½σ²S²∂²C/∂S² − rC = 0
    and substitute into a delta-hedged portfolio.
    First full proof in the comments gets pinned."
   
   (Answer: substitute ∂C/∂t = Θ, ∂²C/∂S² = Γ, and for ATM where
    rC ≈ rSΔ, you get Θ + ½σ²S²Γ ≈ 0, hence Θ ≈ −½σ²S²Γ)

5. Next episode tease:
   "Next on Quantifaya:"
   "Stochastic Volatility — The Heston Model"
   "Because the vol smile told us Black-Scholes was wrong.
    The Heston model is what we built instead.
    Mean-reverting vol, two risk factors, a PDE that Hull
    won't derive for you. We will."

6. End card. Subscribe. Share.
```

### VOICE-OVER SCRIPT

"That's Episode 4.

[PAUSE — recap]

We built every major Greek from the Black-Scholes formula by differentiation. Delta equals N of d₁ — but Taleb's discrete delta is more honest operationally. Gamma equals N prime of d₁ over S sigma root T — always positive for long options, with Up-Gamma and Down-Gamma required in skewed markets. The Gamma-Theta identity — Theta approximately equals minus one-half sigma squared S squared times Gamma — is the mathematical heart of the long-vol versus short-vol trade-off. Vega equals S root T times N prime of d₁ — scales with root-T, requires bucket analysis across the vol surface. And Taleb's shortcomings table from page one-twelve is required reading for anyone who plans to run a real book.

[PAUSE — book recommendations]

Two books to keep beside you. Taleb's Dynamic Hedging — Chapters seven through eleven for the Greeks, with particular attention to the shadow gamma and modified vega sections. This is the practitioner's manual. [T1-T4] And Hull's Chapter nineteen for the analytical formulas and their derivations. [H1-H5] Read Hull first for the structure, then Taleb to understand why structure alone isn't enough.

[PAUSE — comment challenge]

Challenge for this week: prove the Gamma-Theta identity directly from the Black-Scholes PDE. Start from the PDE, substitute Theta and Gamma, apply the delta-hedge condition, and show that Theta plus one-half sigma squared S squared Gamma equals approximately zero. First full proof in the comments gets pinned.

[PAUSE — next episode]

Next week: the Heston model. Because the volatility smile told us Black-Scholes was wrong about vol being constant. Heston made vol itself a mean-reverting stochastic process — and produced one of the few non-Black-Scholes models with a quasi-analytical option pricing formula. We derive it.

Subscribe. Share. This is Quantifaya."

---

---

## APPENDIX A — FULL EQUATION REFERENCE

| Equation | LaTeX | Scene |
|---|---|---|
| Delta (call) | `\Delta_C = N(d_1)` | 2 |
| Delta (put) | `\Delta_P = N(d_1)-1 = -N(-d_1)` | 2 |
| Option P&L (1st order) | `dC \approx \Delta\,dS` | 2 |
| Discrete delta | `\Delta_{\text{disc}} = \frac{C(S+\Delta S)-C(S-\Delta S)}{2\Delta S}` | 3 |
| Gamma | `\Gamma = \frac{\partial^2 C}{\partial S^2} = \frac{N'(d_1)}{S\sigma\sqrt{T}}` | 4 |
| Normal density | `N'(d_1) = \frac{1}{\sqrt{2\pi}}e^{-d_1^2/2}` | 4 |
| Gamma P&L | `\text{P\&L}_\Gamma = \tfrac{1}{2}\Gamma(\Delta S)^2` | 5 |
| Vega | `\mathcal{V} = \frac{\partial C}{\partial\sigma} = S\sqrt{T}\,N'(d_1)` | 6 |
| Vega-Gamma identity | `\mathcal{V} = \Gamma S^2\sigma T` | 6 |
| Modified vega | `\mathcal{V}_{\text{mod}} = \sum_{i=1}^n \mathcal{V}_i F_i` | 6 |
| Theta (call) | `\Theta = -\frac{SN'(d_1)\sigma}{2\sqrt{T}} - rKe^{-rT}N(d_2)` | 7 |
| Gamma-Theta identity | `\Theta \approx -\tfrac{1}{2}\sigma^2 S^2 \Gamma` | 7 |
| Rho (call) | `\rho = KTe^{-rT}N(d_2)` | 8 |
| Full P&L attribution | `\Delta C \approx \Delta\,\Delta S + \tfrac{1}{2}\Gamma(\Delta S)^2 + \mathcal{V}\,\Delta\sigma + \Theta\,\Delta t + \rho\,\Delta r` | 8 |
| BS PDE | `\Theta + rS\Delta + \tfrac{1}{2}\sigma^2 S^2\Gamma = rC` | 9 |

---

## APPENDIX B — COMPLETE MANIM PYTHON SKELETON

```python
# quantifaya_ep4.py
# Render: manim -pqh quantifaya_ep4.py FullEpisode --fps 60 --resolution 1920x1080

from manim import *
import numpy as np
from scipy.stats import norm

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

def cite(refs: str) -> Text:
    return Text(refs, color=TEAL, font_size=13).to_corner(DR).shift(UP*0.1+LEFT*0.1)

# ── Black-Scholes helpers ───────────────────────────────────────────────
def bs_d1(S, K=100, T=0.5, sigma=0.2, r=0.05):
    return (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))

def bs_delta(S, K=100, T=0.5, sigma=0.2, r=0.05):
    return norm.cdf(bs_d1(S,K,T,sigma,r))

def bs_gamma(S, K=100, T=0.5, sigma=0.2, r=0.05):
    d1 = bs_d1(S,K,T,sigma,r)
    return norm.pdf(d1) / (S*sigma*np.sqrt(T))

def bs_vega(S, K=100, T=0.5, sigma=0.2, r=0.05):
    d1 = bs_d1(S,K,T,sigma,r)
    return S*np.sqrt(T)*norm.pdf(d1)

def bs_theta(S, K=100, T=0.5, sigma=0.2, r=0.05):
    d1  = bs_d1(S,K,T,sigma,r)
    d2  = d1 - sigma*np.sqrt(T)
    return (-S*norm.pdf(d1)*sigma/(2*np.sqrt(T)) - r*K*np.exp(-r*T)*norm.cdf(d2)) / 365


# ═══════════════════════════════════════════════════════════════════════
class SceneIntro(Scene):
    def construct(self):
        greeks = [
            (r"\Delta", GOLD,      UP*1.5+LEFT*3),
            (r"\Gamma", ORANGE,    UP*1.5+RIGHT*3),
            (r"\mathcal{V}", TEAL, ORIGIN),
            (r"\Theta", RED,       DOWN*1.5+LEFT*3),
            (r"\rho",   PURPLE,    DOWN*1.5+RIGHT*3),
        ]
        letters = VGroup()
        for sym, col, pos in greeks:
            ltr = MathTex(sym, color=col, font_size=90).move_to(pos)
            letters.add(ltr)
            self.play(FadeIn(ltr, shift=DOWN*0.3), run_time=0.4)
        self.wait(1.5)

        desc = Text("These are not symbols.\nThey are the control panel of a $600 trillion market.",
                    color=FG, font_size=28, line_spacing=1.4).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(desc)); self.wait(1.5)

        taleb = VGroup(
            Text('"The Greeks are meaningful for a single option.\n'
                 ' They are treacherous for a book."',
                 color=GOLD, font_size=24, slant=ITALIC, line_spacing=1.3),
            Text("— N.N. Taleb, Dynamic Hedging, p.112 [T4]",
                 color=FG, font_size=18),
        ).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.4)
        self.play(FadeOut(desc), FadeIn(taleb)); self.wait(2)

        self.play(FadeOut(letters), FadeOut(taleb))
        title_card = VGroup(
            Text("QUANTIFAYA", color=PURPLE, font_size=52, weight=BOLD),
            Text("Episode 4", color=FG, font_size=26),
            Text("The Greeks — Delta, Gamma, Vega Built Intuitively",
                 color=GOLD, font_size=32),
            Text("BS Formula  →  Real Desk  →  Where They Break",
                 color=FG, font_size=22),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeIn(title_card)); self.wait(3)


# ═══════════════════════════════════════════════════════════════════════
class SceneDelta(Scene):
    def construct(self):
        title = Text("Δ — Delta: The Hedge Ratio That Lies to You",
                     color=GOLD, font_size=34).to_edge(UP)
        src   = cite("[T1] Taleb Ch.7  |  [H2] Hull (2018), p.418  |  [BS] Black & Scholes (1973)")
        self.play(FadeIn(title), FadeIn(src))

        # Definition
        defn = VGroup(
            VGroup(
                Text("Mathematical:", color=TEAL, font_size=22, weight=BOLD),
                MathTex(r"\Delta = \frac{\partial C}{\partial S} = N(d_1)",
                        color=FG, font_size=34),
            ).arrange(DOWN, buff=0.15),
            VGroup(
                Text("Practical:", color=TEAL, font_size=22, weight=BOLD),
                Text("Shares of stock to hold to replicate\nthe option's price change for a small move in S.",
                     color=FG, font_size=22, line_spacing=1.3),
            ).arrange(DOWN, buff=0.15),
        ).arrange(RIGHT, buff=1.0).shift(UP*0.5)
        self.play(FadeIn(defn)); self.wait(1.5); self.play(FadeOut(defn))

        # Delta vs S plot
        ax = Axes(x_range=[60,140,10], y_range=[0,1,0.2],
                  x_length=9, y_length=5, axis_config={"color":FG})
        ax_lbl = ax.get_axis_labels(
            Tex("S", color=FG, font_size=22),
            Tex(r"\Delta", color=FG, font_size=22))
        delta_curve = ax.plot(lambda S: bs_delta(S, T=0.5),
                               x_range=[62,138], color=BLUE_NORM, stroke_width=3)
        self.play(Create(ax), Write(ax_lbl), Create(delta_curve))

        for (sv, label, col) in [(70,"OTM: Δ≈0.05",ORANGE),
                                  (100,"ATM: Δ≈0.50",GOLD),
                                  (135,"ITM: Δ≈0.97",GREEN)]:
            d  = Dot(ax.c2p(sv, bs_delta(sv, T=0.5)), color=col)
            lbl= Text(label, color=col, font_size=16).next_to(d, RIGHT, buff=0.1)
            self.play(FadeIn(d), FadeIn(lbl), run_time=0.5)
        self.wait(2)

        # Taleb quote on Delta
        self.play(FadeOut(ax), FadeOut(ax_lbl), FadeOut(delta_curve))
        taleb_delta = VGroup(
            Text('"From a standpoint of trading, [the mathematical delta]\n'
                 ' offers no significance.\n'
                 ' There is no such thing as an infinitely small move in the market."',
                 color=GOLD, font_size=22, slant=ITALIC, line_spacing=1.4),
            Text("— Taleb, Dynamic Hedging, p.118 [T5]", color=FG, font_size=18),
            Text("Markets gap. They jump. They close Friday and open Monday 3% away.",
                 color=ORANGE, font_size=22, weight=BOLD),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeIn(taleb_delta)); self.wait(3)


# ═══════════════════════════════════════════════════════════════════════
class SceneDeltaPractice(Scene):
    def construct(self):
        title = Text("Delta in Practice — The Lies Your Risk System Tells You",
                     color=GOLD, font_size=32).to_edge(UP)
        src   = cite("[T1] Taleb, Dynamic Hedging, Ch.7, pp.118–133")
        self.play(FadeIn(title), FadeIn(src))

        # Book problem
        book = VGroup(
            Text("A Real Book (Taleb, p.133):", color=TEAL, font_size=24, weight=BOLD),
            Text("• Long $1M 96 calls, Δ=0.824  →  +$824,000 delta", color=GREEN, font_size=22),
            Text("• Short $1M 104 calls, Δ=0.198  →  −$198,000 delta", color=RED, font_size=22),
            Text("• Total delta: +$626,000  →  Sell $626,000 forward. Done?", color=FG, font_size=22),
            Text("NOT done. The aggregate delta disguises the local structure.",
                 color=ORANGE, font_size=22, weight=BOLD),
            Text("Map the P&L across spot: it looks long everywhere except near S=100.",
                 color=FG, font_size=20),
            Text("The hedge is misleading. The textbook answer is wrong.", color=RED, font_size=22),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).center()
        self.play(LaggedStart(*[FadeIn(b) for b in book], lag_ratio=0.2))
        self.wait(2); self.play(FadeOut(book))

        # Discrete delta solution
        fix = VGroup(
            Text("Taleb's Fix — Discrete Delta:", color=GOLD, font_size=28, weight=BOLD),
            MathTex(r"\Delta_{\text{disc}} = \frac{C(S+\Delta S)-C(S-\Delta S)}{2\,\Delta S}",
                    color=FG, font_size=36),
            Text("ΔS = 1–2 sigma move — a realistic, tradeable increment.",
                 color=FG, font_size=22),
            Text("Automatically incorporates gamma and vega.\nMore honest. Less pure. Much safer.",
                 color=TEAL, font_size=22, line_spacing=1.3),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeIn(fix)); self.wait(3)


# ═══════════════════════════════════════════════════════════════════════
class SceneGamma(Scene):
    def construct(self):
        title = Text("Γ — Gamma: The Curvature That Costs You Every Day",
                     color=GOLD, font_size=32).to_edge(UP)
        src   = cite("[T2] Taleb, Dynamic Hedging, Ch.8  |  [H3] Hull (2018), p.428")
        self.play(FadeIn(title), FadeIn(src))

        # Definition
        gamma_def = VGroup(
            MathTex(r"\Gamma = \frac{\partial^2 C}{\partial S^2}"
                    r"= \frac{\partial\Delta}{\partial S}"
                    r"= \frac{N'(d_1)}{S\sigma\sqrt{T}}",
                    color=FG, font_size=34),
            Text("Always POSITIVE for long options (calls and puts).",
                 color=GREEN, font_size=22),
            Text("Always NEGATIVE for short options.",
                 color=RED, font_size=22),
        ).arrange(DOWN, buff=0.3).shift(UP*1.0)
        self.play(FadeIn(gamma_def)); self.wait(1.5); self.play(FadeOut(gamma_def))

        # Taylor expansion intuition
        taylor = VGroup(
            Text("The Taylor Expansion Connection (from Ep.2):", color=TEAL, font_size=24),
            MathTex(r"dC = \Delta\,dS + \frac{1}{2}\Gamma\,(dS)^2 + \cdots",
                    color=FG, font_size=34),
            Text("Δ → linear term.  Γ → curvature correction.",
                 color=FG, font_size=22),
            Text("Long Γ: actual gain > Delta prediction on EVERY large move.",
                 color=GREEN, font_size=22, weight=BOLD),
            Text("Short Γ: actual loss > Delta prediction on EVERY large move.",
                 color=RED, font_size=22, weight=BOLD),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeIn(taylor)); self.wait(2); self.play(FadeOut(taylor))

        # Gamma vs S — bell curve
        ax = Axes(x_range=[60,140,10], y_range=[0,0.08,0.02],
                  x_length=9, y_length=4.5, axis_config={"color":FG})
        ax_lbl = ax.get_axis_labels(Tex("S",color=FG,font_size=22),
                                     Tex(r"\Gamma",color=FG,font_size=22))
        for T_, col_, lbl_ in [(1.0, BLUE_NORM,"T=1yr"),
                                 (0.25,ORANGE,   "T=3mo"),
                                 (1/52,GREEN,    "T=1wk")]:
            crv = ax.plot(lambda S, T=T_: bs_gamma(S,T=T),
                           x_range=[62,138], color=col_, stroke_width=2.5)
            lbl = Text(lbl_, color=col_, font_size=18)\
                      .move_to(ax.c2p(108, bs_gamma(108,T=T_)+0.003))
            self.play(Create(crv), FadeIn(lbl), run_time=0.6)

        self.play(Create(ax), Write(ax_lbl))
        explosion = Text("GAMMA EXPLOSION near expiry at ATM — the options market maker's nightmare",
                         color=RED, font_size=20).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(explosion)); self.wait(2.5)

        # Shadow Gamma
        self.play(FadeOut(ax), FadeOut(ax_lbl), FadeOut(explosion))
        shadow = VGroup(
            Text("Taleb's Shadow Gamma [T2]:", color=GOLD, font_size=28, weight=BOLD),
            Text("Conventional Gamma: symmetric — same up and down.", color=FG, font_size=22),
            Text("Shadow Gamma: accounts for vol-spot correlation.", color=ORANGE, font_size=22),
            Text("In equity markets: DOWN-GAMMA > UP-GAMMA", color=RED, font_size=24, weight=BOLD),
            Text("A crash causes BOTH a delta change AND a vol spike.\n"
                 "The effective Gamma on the downside is larger than the formula shows.",
                 color=FG, font_size=20, line_spacing=1.3),
            Text("Always compute Up-Gamma and Down-Gamma separately.", color=TEAL, font_size=22),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT).center()
        self.play(LaggedStart(*[FadeIn(s) for s in shadow], lag_ratio=0.2))
        self.wait(3)


# ═══════════════════════════════════════════════════════════════════════
class SceneGammaPractice(Scene):
    def construct(self):
        title = Text("Gamma in Practice — The Daily P&L Battle",
                     color=GOLD, font_size=34).to_edge(UP)
        src   = cite("[T2] Taleb, Dynamic Hedging, pp.127–162")
        self.play(FadeIn(title), FadeIn(src))

        scenarios = VGroup(
            Text("Setup: S=$100, K=$100, T=30d, σ=20%,  Γ = 0.0668", color=TEAL, font_size=22),
            VGroup(
                Text("Quiet day — ΔS=$0.50:", color=FG, font_size=22),
                MathTex(r"\tfrac{1}{2}(0.0668)(0.50)^2 = \$0.008\text{ per option}",
                        color=BLUE_NORM, font_size=24),
                Text("Almost nothing. Gamma earns nothing in calm markets.", color=FG, font_size=19, slant=ITALIC),
            ).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
            VGroup(
                Text("Volatile day — ΔS=$3.00:", color=FG, font_size=22),
                MathTex(r"\tfrac{1}{2}(0.0668)(3.00)^2 = \$0.30\text{ per option}",
                        color=ORANGE, font_size=24),
                Text("Thirty cents. Starts to matter.", color=FG, font_size=19, slant=ITALIC),
            ).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
            VGroup(
                Text("CRASH — ΔS=$10.00:", color=RED, font_size=22, weight=BOLD),
                MathTex(r"\tfrac{1}{2}(0.0668)(10.00)^2 = \$3.34\text{ per option}",
                        color=RED, font_size=24),
                Text("On 10,000 options: $33,400 in one day. A crisis is Christmas for long gamma.",
                     color=RED, font_size=19, slant=ITALIC),
            ).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
            Text("Gamma P&L scales as (ΔS)². Double the move = FOUR TIMES the Gamma P&L.",
                 color=GOLD, font_size=22, weight=BOLD),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).center()
        self.play(LaggedStart(*[FadeIn(s) for s in scenarios], lag_ratio=0.25))
        self.wait(3)


# ═══════════════════════════════════════════════════════════════════════
class SceneVega(Scene):
    def construct(self):
        title = Text("𝒱 — Vega: The Greek Traders Fear More Than Delta",
                     color=GOLD, font_size=34).to_edge(UP)
        src   = cite("[T3] Taleb, Dynamic Hedging, Ch.9  |  [H4] Hull (2018), p.434")
        self.play(FadeIn(title), FadeIn(src))

        # Definition
        vega_def = VGroup(
            MathTex(r"\mathcal{V} = \frac{\partial C}{\partial\sigma}"
                    r"= S\sqrt{T}\,N'(d_1)",
                    color=FG, font_size=38),
            Text("Always POSITIVE for long options (long vol = want vol to rise).",
                 color=GREEN, font_size=22),
            Text("Not a Greek letter. Made up. Also called κ, ζ, λ. Industry calls it Vega.",
                 color=TEAL, font_size=20, slant=ITALIC),
        ).arrange(DOWN, buff=0.3).shift(UP*0.8)
        self.play(FadeIn(vega_def)); self.wait(1.5); self.play(FadeOut(vega_def))

        # Vega vs T — scales with √T
        ax = Axes(x_range=[60,140,10], y_range=[0,55,10],
                  x_length=9, y_length=4.5, axis_config={"color":FG})
        ax_lbl = ax.get_axis_labels(Tex("S",color=FG,font_size=22),
                                     Tex(r"\mathcal{V}",color=FG,font_size=22))
        self.play(Create(ax), Write(ax_lbl))
        for T_, col_, lbl_ in [(2.0,PURPLE,"T=2yr"),
                                (0.5,BLUE_NORM,"T=6mo"),
                                (1/12,ORANGE,"T=1mo")]:
            crv = ax.plot(lambda S, T=T_: bs_vega(S,T=T),
                           x_range=[62,138], color=col_, stroke_width=2.5)
            lbl = Text(lbl_, color=col_, font_size=18)\
                      .move_to(ax.c2p(105, bs_vega(105,T=T_)+1.5))
            self.play(Create(crv), FadeIn(lbl), run_time=0.6)
        vega_note = Text("Vega scales with √T — longer-dated = more vol exposure.",
                         color=GOLD, font_size=22).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(vega_note)); self.wait(2)

        # Vega-Gamma identity
        self.play(FadeOut(ax), FadeOut(ax_lbl), FadeOut(vega_note))
        identity = VGroup(
            Text("Taleb's Key Identity [T3]:", color=GOLD, font_size=26, weight=BOLD),
            MathTex(r"\mathcal{V} = \Gamma \cdot S^2 \cdot \sigma \cdot T",
                    color=GOLD, font_size=42),
            Text("Vega is the integral of expected Gamma P&L over the option's life.",
                 color=FG, font_size=22),
            Text("They are NOT independent. Same strike/maturity: hedge one, hedge both.",
                 color=ORANGE, font_size=22),
            Text("Across strikes/maturities: they diverge. Manage separately.",
                 color=RED, font_size=22),
        ).arrange(DOWN, buff=0.3).center()
        box = SurroundingRectangle(identity[1], color=PURPLE, buff=0.2, stroke_width=2)
        self.play(FadeIn(identity), Create(box)); self.wait(3)


# ═══════════════════════════════════════════════════════════════════════
class SceneTheta(Scene):
    def construct(self):
        title = Text("Θ — Theta: The Rent You Pay Every Night",
                     color=GOLD, font_size=36).to_edge(UP)
        src   = cite("[H5] Hull (2018), p.431  |  [T2] Taleb, Ch.8 — Gamma/Theta relationship")
        self.play(FadeIn(title), FadeIn(src))

        # Formula
        theta_eq = VGroup(
            MathTex(r"\Theta = -\frac{S N'(d_1)\sigma}{2\sqrt{T}}"
                    r"- rKe^{-rT}N(d_2)",
                    color=FG, font_size=32),
            Text("Always NEGATIVE for long options. Time hurts you.",
                 color=RED, font_size=22),
        ).arrange(DOWN, buff=0.3).shift(UP*1.5)
        self.play(FadeIn(theta_eq)); self.wait(1)

        # Gamma-Theta identity
        identity = VGroup(
            Text("The Gamma-Theta Identity (from the BS PDE):", color=TEAL, font_size=24, weight=BOLD),
            MathTex(r"\Theta \approx -\frac{1}{2}\sigma^2 S^2 \Gamma",
                    color=GOLD, font_size=48),
            Text("Long Γ = pay Θ every night.", color=GREEN, font_size=24),
            Text("Short Γ = collect Θ every night.", color=RED, font_size=24),
            Text("The market prices convexity exactly. There is no free lunch.",
                 color=ORANGE, font_size=22, slant=ITALIC),
        ).arrange(DOWN, buff=0.3).center()
        box = SurroundingRectangle(identity[1], color=GOLD, buff=0.25, stroke_width=3)
        self.play(FadeOut(theta_eq), FadeIn(identity), Create(box)); self.wait(2)

        # Theta acceleration plot
        self.play(FadeOut(identity), FadeOut(box))
        ax = Axes(x_range=[0,90,10], y_range=[-0.10,0,0.02],
                  x_length=9, y_length=4, axis_config={"color":FG})
        ax_lbl = ax.get_axis_labels(
            Tex(r"\text{Days to expiry}", color=FG, font_size=20),
            Tex(r"\Theta\text{(per day)}", color=FG, font_size=20))
        theta_crv = ax.plot(
            lambda T: bs_theta(100, T=max(T/365, 1e-4)) if T>0 else 0,
            x_range=[1,89], color=RED, stroke_width=3)
        self.play(Create(ax), Write(ax_lbl), Create(theta_crv))
        accel = Text("Theta ACCELERATES near expiry — not linear decay.",
                     color=ORANGE, font_size=22).to_edge(DOWN, buff=0.4)
        wknd  = Text("Weekend effect: Friday → Monday = 3 days of Theta. Sellers love Fridays.",
                     color=GOLD, font_size=20).next_to(accel, UP, buff=0.15)
        self.play(FadeIn(accel), FadeIn(wknd)); self.wait(3)


# ═══════════════════════════════════════════════════════════════════════
class SceneRhoAndDashboard(Scene):
    def construct(self):
        title = Text("ρ & The Full Greeks Dashboard", color=GOLD, font_size=36).to_edge(UP)
        src   = cite("[H1] Hull (2018), Ch.19")
        self.play(FadeIn(title), FadeIn(src))

        # Rho
        rho_block = VGroup(
            MathTex(r"\rho = KTe^{-rT}N(d_2)", color=FG, font_size=36),
            Text("Positive for calls. Negative for puts.", color=FG, font_size=22),
            Text("Usually smallest Greek for equities. Dominates in long-dated IR derivatives.",
                 color=TEAL, font_size=20),
        ).arrange(DOWN, buff=0.25).shift(UP*1.5)
        self.play(FadeIn(rho_block)); self.wait(1.5); self.play(FadeOut(rho_block))

        # Full P&L attribution
        pnl = VGroup(
            Text("The Options Trader's P&L Equation:", color=GOLD, font_size=26, weight=BOLD),
            MathTex(r"\Delta C \approx"
                    r"\underbrace{\Delta\,\Delta S}_{\text{linear}}"
                    r"+\underbrace{\tfrac{1}{2}\Gamma(\Delta S)^2}_{\text{curvature}}"
                    r"+\underbrace{\mathcal{V}\,\Delta\sigma}_{\text{vol move}}"
                    r"+\underbrace{\Theta\,\Delta t}_{\text{time decay}}"
                    r"+\underbrace{\rho\,\Delta r}_{\text{rate move}}",
                    color=FG, font_size=28),
        ).arrange(DOWN, buff=0.3).shift(UP*0.5)
        self.play(FadeIn(pnl)); self.wait(1.5)

        # Concrete P&L attribution example
        example = VGroup(
            Text("Yesterday: ΔS=+$2, Δσ=−0.5%, Δt=1 day",
                 color=TEAL, font_size=22),
            MathTex(r"\Delta C \approx 0.5793\times2"
                    r"+\tfrac{1}{2}(0.0267)(4)"
                    r"+28.22\times(-0.005)"
                    r"+(-0.038)\times1",
                    color=FG, font_size=24),
            MathTex(r"= \underbrace{+1.159}_{\Delta}"
                    r"+\underbrace{+0.053}_{\Gamma}"
                    r"\underbrace{-0.141}_{\mathcal{V}}"
                    r"\underbrace{-0.038}_{\Theta}"
                    r"= +\$1.033",
                    color=GOLD, font_size=28),
            Text("Every dollar of P&L explained. Every Greek accounted for.",
                 color=GREEN, font_size=22, weight=BOLD),
        ).arrange(DOWN, buff=0.3).next_to(pnl, DOWN, buff=0.4)
        self.play(FadeIn(example)); self.wait(3)


# ═══════════════════════════════════════════════════════════════════════
class SceneTalebShortcomings(Scene):
    def construct(self):
        title = Text("The Greeks and Their Shortcomings",
                     color=GOLD, font_size=36).to_edge(UP)
        sub   = Text("What Taleb's table on p.112 says that no textbook will.",
                     color=FG, font_size=20, slant=ITALIC).next_to(title, DOWN, buff=0.05)
        src   = cite("[T4] Taleb, Dynamic Hedging, p.112  |  [T3] Ch.9, p.163")
        self.play(FadeIn(title), FadeIn(sub), FadeIn(src))

        shortcomings = [
            (BLUE_NORM, "Δ Delta",
             '"Delta does not work on a portfolio of options\nthat mixes longs and shorts.\nIt is an extremely weak measure of risks." [T4]',
             "Fix: discrete delta with realistic increments"),
            (ORANGE, "Γ Gamma",
             '"It is meaningless for a portfolio of options.\nIt does not take into account changes in volatility\nwhen the market moves." [T4]',
             "Fix: Up-Gamma, Down-Gamma, Shadow Gamma"),
            (TEAL, "𝒱 Vega",
             '"Parallel shift assumption — assumes all maturities\nmove simultaneously. Not realistic." [T4]',
             "Fix: bucket vega by maturity, modified vega"),
            (RED, "Θ Theta",
             '"Does not take into account changes in volatility\nthat co-occur with time passage." [T4]',
             "Fix: term structure of vol adjustments"),
        ]
        for col, greek, problem, fix in shortcomings:
            g = VGroup(
                Text(greek, color=col, font_size=28, weight=BOLD),
                Text(problem, color=GOLD, font_size=20, slant=ITALIC, line_spacing=1.3),
                Text(fix, color=FG, font_size=19),
            ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).center()
            self.play(FadeIn(g)); self.wait(2.5); self.play(FadeOut(g))

        # Meta-lesson Taleb quote
        meta = VGroup(
            Text('"Trading an option bears little relevance to trading a book.\n'
                 ' An option book is not as compact as mathematicians believe.\n'
                 ' It will generally be neutral in the lower moments\n'
                 ' and exposed to various risks in the higher moments."',
                 color=GOLD, font_size=22, slant=ITALIC, line_spacing=1.4),
            Text("— Taleb, Dynamic Hedging, p.163 [T3]", color=FG, font_size=18),
            Text("The Greeks are the starting vocabulary.\nScenario analysis is the actual risk management.",
                 color=ORANGE, font_size=22, weight=BOLD, line_spacing=1.3),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeIn(meta)); self.wait(4)


# ═══════════════════════════════════════════════════════════════════════
class SceneOutro(Scene):
    def construct(self):
        logo    = Text("QUANTIFAYA", color=PURPLE, font_size=64, weight=BOLD)
        tagline = Text("Financial Engineering. Explained Rigorously. Applied Practically.",
                       color=GOLD, font_size=22).next_to(logo, DOWN, buff=0.3)
        self.play(FadeIn(logo), FadeIn(tagline)); self.wait(1)

        recap = VGroup(
            Text("✓  Delta = N(d₁) — the hedge ratio and its textbook limits",    color=GREEN, font_size=19),
            Text("✓  Discrete delta — Taleb's operational fix for real books",     color=GREEN, font_size=19),
            Text("✓  Gamma = N'(d₁)/(Sσ√T) — curvature, long/short trade-off",   color=GREEN, font_size=19),
            Text("✓  Up-Gamma / Down-Gamma / Shadow Gamma — skewed markets",       color=GREEN, font_size=19),
            Text("✓  Gamma-Theta identity: Θ ≈ −½σ²S²Γ",                         color=GREEN, font_size=19),
            Text("✓  Vega = S√T·N'(d₁) — vol exposure, scales with √T",           color=GREEN, font_size=19),
            Text("✓  Vega-Gamma identity: 𝒱 = ΓS²σT",                            color=GREEN, font_size=19),
            Text("✓  Theta — the daily rent and its expiry acceleration",           color=GREEN, font_size=19),
            Text("✓  Full P&L attribution: Δ·ΔS + ½Γ(ΔS)² + 𝒱·Δσ + Θ·Δt",      color=GREEN, font_size=19),
            Text("✓  Taleb's shortcomings table — what the textbook won't say",    color=GREEN, font_size=19),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).center()
        self.play(FadeOut(logo), FadeOut(tagline))
        self.play(LaggedStart(*[FadeIn(r) for r in recap], lag_ratio=0.10))
        self.wait(2)

        challenge = VGroup(
            Text("Comment Challenge:", color=GOLD, font_size=28, weight=BOLD),
            Text("Prove the Gamma-Theta identity from the Black-Scholes PDE.",
                 color=FG, font_size=22),
            MathTex(r"\text{Start from: }\Theta + rS\Delta + \tfrac{1}{2}\sigma^2S^2\Gamma = rC",
                    color=FG, font_size=24),
            Text("Show that for a delta-hedged portfolio, Θ ≈ −½σ²S²Γ.",
                 color=ORANGE, font_size=22),
            Text("First full proof in comments gets pinned.", color=TEAL, font_size=20),
        ).arrange(DOWN, buff=0.25).center()
        self.play(FadeOut(recap), FadeIn(challenge)); self.wait(2)

        next_ep = VGroup(
            Text("Next on Quantifaya:", color=GOLD, font_size=30, weight=BOLD),
            Text("The Heston Model — Stochastic Volatility from Scratch",
                 color=ORANGE, font_size=26),
            Text("Vol is not constant. Heston made it a mean-reverting process.\n"
                 "We derive the quasi-analytical pricing formula.\n"
                 "Hull won't do this for you. We will.",
                 color=FG, font_size=22, line_spacing=1.3),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeOut(challenge), FadeIn(next_ep)); self.wait(3)


# ═══════════════════════════════════════════════════════════════════════
class FullEpisode(Scene):
    """
    Full episode render.
    manim -pqh quantifaya_ep4.py FullEpisode --fps 60 --resolution 1920x1080
    Single scene test:
    manim -pql quantifaya_ep4.py SceneGamma
    """
    def construct(self):
        for SceneClass in [
            SceneIntro,
            SceneDelta,
            SceneDeltaPractice,
            SceneGamma,
            SceneGammaPractice,
            SceneVega,
            SceneTheta,
            SceneRhoAndDashboard,
            SceneTalebShortcomings,
            SceneOutro,
        ]:
            instance = SceneClass()
            instance.camera   = self.camera
            instance.renderer = self.renderer
            instance.construct()
            self.wait(0.5)
```

---

## APPENDIX C — TIMING GUIDE

| # | Class | Target | Pacing Note |
|---|---|---|---|
| 1 | SceneIntro | 1:30 | Five letter slams — don't rush. Taleb quote needs a beat after it |
| 2 | SceneDelta | 4:00 | S-curve needs time. Taleb attack on continuous-time delta — pause after it |
| 3 | SceneDeltaPractice | 2:00 | Taleb book example p.133 — read it slowly, the punchline is the chart |
| 4 | SceneGamma | 4:00 | Long/short gamma trade-off — say it twice. Gamma explosion visual — hold |
| 5 | SceneGammaPractice | 2:00 | Crash scenario — say the thirty-four thousand number slowly |
| 6 | SceneVega | 3:30 | Vega-Gamma identity is the surprise — let it land |
| 7 | SceneTheta | 2:30 | Gamma-Theta identity box — hold 4 seconds. It's the key |
| 8 | SceneRhoAndDashboard | 2:00 | P&L attribution example — read each number out loud |
| 9 | SceneTalebShortcomings | 2:30 | Meta-lesson Taleb quote — slowest delivery of the episode |
| 10 | SceneOutro | 1:00 | Challenge — speak it precisely |
| **TOTAL** | | **~25:00** | On target — minimal trimming needed |

---

## APPENDIX D — YOUTUBE UPLOAD CHECKLIST

```
TITLE:
The Options Greeks ACTUALLY Explained | Delta Gamma Vega Built From Scratch | Quantifaya Ep.4

DESCRIPTION (first 200 chars):
Delta. Gamma. Vega. Theta. Every options course mentions them.
Almost none derive them, show what they mean on a real desk,
or tell you what Taleb says about where they break.

CHAPTERS:
00:00 — The Five Control Panel Letters
01:30 — Delta: Formula, Derivation, S-Curve
05:30 — Delta in Practice: The Lies Your Risk System Tells You (Taleb Ch.7)
07:30 — Gamma: Curvature, Long vs Short, Gamma Explosion
11:30 — Gamma in Practice: Daily P&L Scenarios & Shadow Gamma
13:30 — Vega: Derivation, √T Scaling, Vega-Gamma Identity
17:00 — Theta: The Daily Rent, Gamma-Theta Identity
19:30 — Rho & Full P&L Attribution Dashboard
21:30 — Taleb's Shortcomings Table — What No Textbook Says
24:00 — Next Episode: Heston Stochastic Vol

TAGS:
options greeks explained, delta gamma vega theta black scholes,
options greeks derivation, gamma theta identity, vega options explained,
shadow gamma taleb, dynamic hedging taleb, discrete delta,
up gamma down gamma, bucket vega, vega gamma relationship,
options P&L attribution, theta decay acceleration, gamma explosion expiry,
quant finance, financial engineering, derivatives trading math,
options trading risk management, quant interview greeks, worldquant

THUMBNAIL BRIEF:
Dark background. Five Greek letters (Δ Γ 𝒱 Θ ρ) each in a different bold colour.
Above: "The 5 Numbers That Run a $600T Market"
Below: "Built From Scratch | Taleb + Hull"
Quantifaya logo bottom right.

PINNED COMMENT:
📌 Sources for this episode:
[T] Taleb, N.N. (1997). Dynamic Hedging. Wiley.
    — Ch.7 (Delta, p.103), Ch.8 (Gamma, p.127), Ch.9 (Vega, p.147)
    — Shortcomings table: p.112
[H] Hull, J.C. (2018). Options, Futures, and Other Derivatives, 10th ed.
    — Ch.19: The Greek Letters

🎯 Challenge: Prove the Gamma-Theta identity from the BS PDE.
Start from Θ + rSΔ + ½σ²S²Γ = rC.
Show that for a delta-hedged position, Θ ≈ −½σ²S²Γ.
First full derivation in comments gets pinned!
```
