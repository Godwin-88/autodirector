# QUANTIFAYA — EPISODE 2
## "Itô's Lemma — What It Actually Means (And Why Your Calculus Is Useless Here)"

**Channel:** Quantifaya  
**Target Duration:** 25 minutes  
**Production Stack:** Python Manim (Community Edition v0.18+) + TTS Voice-Over  
**Persona:** Taylor-meets-Axe-Capital. Brilliant. Ruthless. Occasionally insufferable. Always right.  
**Tone:** Taleb-level intellectual confidence, Billions-level swagger, zero patience for mediocrity.

---

**SEO Title:** Itô's Lemma Explained — The Math Behind Every Derivative on Earth | Quantifaya  
**SEO Description:** Kiyosi Itô wrote four pages in 1944 that became the foundation of a $600 trillion derivatives market. Most quant courses teach you the formula. We teach you *why* it's true — from Brownian motion and quadratic variation, through the full Taylor expansion proof, to Black-Scholes derived live. If you're in a quant interview and can't derive Itô's Lemma, you're not getting the job.  
**SEO Tags:** ito lemma explained, stochastic calculus finance, geometric brownian motion, black scholes derivation, ito formula proof, quadratic variation, wiener process, stochastic differential equations, quant finance math, financial engineering, derivatives pricing math, brownian motion finance, quant interview prep, worldquant, financial mathematics

---

## VERIFIED ACADEMIC SOURCES (cite on-screen and in description)

| # | Citation | Used In |
|---|---|---|
| [1] | Itô, K. (1944). *Stochastic integral.* Proc. Imperial Academy Tokyo, 20(8), 519–524. | Scenes 1, 4 |
| [2] | Itô, K. (1951). *On a formula concerning stochastic differentials.* Nagoya Math. J., 3, 55–65. | Scene 4 |
| [3] | Black, F. & Scholes, M. (1973). *The pricing of options and corporate liabilities.* J. Political Economy, 81(3), 637–654. | Scenes 7, 8 |
| [4] | Merton, R.C. (1973). *Theory of rational option pricing.* Bell J. Economics, 4(1), 141–183. | Scene 7 |
| [5] | Wiener, N. (1923). *Differential space.* J. Mathematics and Physics, 2, 131–174. | Scene 2 |
| [6] | Shreve, S.E. (2004). *Stochastic Calculus for Finance II.* Springer. | Scenes 3, 4, 5 |
| [7] | Øksendal, B. (2003). *Stochastic Differential Equations*, 6th ed. Springer. | Scenes 4, 5 |
| [8] | Karatzas, I. & Shreve, S.E. (1991). *Brownian Motion and Stochastic Calculus.* Springer. | Scene 3 |
| [9] | Taleb, N.N. (2007). *The Black Swan.* Random House. | Scenes 1, 9 |
| [10] | Hull, J.C. (2018). *Options, Futures, and Other Derivatives*, 10th ed. Pearson. | Scenes 6, 7 |
| [11] | Wilmott, P. (2006). *Paul Wilmott on Quantitative Finance*, 2nd ed. Wiley. | Scene 8 |
| [12] | Mandelbrot, B. & Hudson, R. (2004). *The Misbehaviour of Markets.* Basic Books. | Scene 9 |
| [13] | Protter, P. (2005). *Stochastic Integration and Differential Equations.* Springer. | Scene 5 |

---

## PRODUCTION NOTES

**Color palette (same as Ep. 1 — brand consistency):**
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
```

**Render commands:**
```bash
# Full 1080p60 episode
manim -pqh quantifaya_ep2.py FullEpisode --fps 60 --resolution 1920x1080

# Quick scene test
manim -pql quantifaya_ep2.py SceneIntro
```

---

---

## SCENE 1: COLD OPEN — THE POWER MOVE
**Class:** `SceneIntro` | **Duration:** ~1:45

### MANIM ANIMATION SEQUENCE

```
1. Black screen. Slow fade in — white text, large, centered:
   "1944."

2. Transform to:
   "A Japanese mathematician named Kiyosi Itô
    wrote four pages."

3. Transform to:
   "Those four pages are worth
    $600,000,000,000,000."

4. Beat. Then in gold:
   "Six hundred trillion dollars.
    The size of the global derivatives market."

5. Source tag fades in bottom-right (small, academic style):
   "[1] Itô (1944), Proc. Imperial Academy Tokyo"

6. Blood red text, bold:
   "Your calculus professor never mentioned this.
    There's a reason."

7. Cut to: A smooth curve. Label: "f(x) — classical calculus"
   Classic tangent line touching it. Clean. Neat.

8. That curve GLITCHES and becomes jagged, random, violent.
   Label: "B(t) — Brownian motion"
   The tangent line FAILS — it can't touch the jagged path.
   Red X over the tangent line.

9. Text: "Classical calculus assumes smooth functions.
          Markets are not smooth.
          Itô fixed this. Today we understand how."

10. QUANTIFAYA logo + episode title slam in from bottom:
    Episode 2: "Itô's Lemma — What It Actually Means"
    Subtitle: "Stochastic Calculus | GBM | The Engine of Black-Scholes"
```

### VOICE-OVER SCRIPT

"1944. World War II is still being fought. And somewhere in Japan, a 29-year-old mathematician named Kiyosi Itô — working in near-total isolation, with limited access to Western literature — writes four pages. [1]

Four pages that would eventually underpin every option, every swap, every structured product, every exotic derivative traded on this planet.

Six hundred trillion dollars. That's the notional size of the global derivatives market. Built on four pages.

Your calculus professor never mentioned Itô's name. I'm going to tell you why.

[PAUSE — show smooth curve]

Classical calculus — the Newton-Leibniz version you were tortured with in school — works beautifully on smooth, differentiable functions. You have a curve. You draw a tangent. You compute a derivative. Everything is clean, everything is deterministic.

[PAUSE — show Brownian motion glitch]

Financial markets are none of those things.

This jagged, violent, non-differentiable path — Brownian motion — is what actually drives stock prices. You cannot draw a tangent line on it. It has no derivative in the classical sense. Everywhere you look, it's rough.

Itô's genius was building a calculus *for* rough paths. A calculus where the correction term isn't just a philosophical nicety — it's a trading signal worth hundreds of billions of dollars.

Welcome back to Quantifaya. Let's get into it."

---

## SCENE 2: BROWNIAN MOTION — THE FOUNDATION
**Class:** `SceneBrownianMotion` | **Duration:** ~3:30

### MANIM ANIMATION SEQUENCE

```
1. Title: "Step 0: What Is Brownian Motion?"
   Subtitle in smaller text: "[5] Wiener (1923) — the mathematical formalization"

2. Three axioms of Standard Brownian Motion (Wiener Process) appear
   one by one, each with a visual:

   AXIOM 1:
   B(0) = 0
   Visual: dot at origin on a timeline

   AXIOM 2:
   B(t) - B(s) ~ N(0, t-s)  for  0 ≤ s < t
   Visual: Distribution bell appears over an increment.
   "Increments are Normal with variance equal to the time elapsed."

   AXIOM 3:
   Independent increments.
   Visual: Timeline divided into chunks. Each chunk randomly colored.
   "What happened yesterday is irrelevant. The process has no memory."

   BONUS AXIOM:
   B(t) is almost surely continuous but nowhere differentiable.
   Visual: Zoom into the path — the more you zoom, the rougher it gets.
   Fractal-like self-similarity animation.

3. Key properties panel (right side):
   E[B(t)] = 0
   Var[B(t)] = t
   E[B(t)²] = t
   E[(dB)²] = dt   ← FLASH THIS IN GOLD, this is the key

4. Simulation: Animate 5 sample Brownian motion paths simultaneously
   using the random walk approximation:
   B(t) ≈ Σ εᵢ√(Δt),  εᵢ ~ N(0,1)
   Show paths diverging wildly from the same origin.

5. Text box:
   "This is NOT a sine wave.
    This is NOT a trend.
    This is pure, weaponised randomness.
    And every stock price model uses it as a building block."

6. Source citation bottom:
   "[5] Wiener, N. (1923). Differential Space. J. Math. Phys."
   "[8] Karatzas & Shreve (1991). Brownian Motion and Stochastic Calculus."
```

### VOICE-OVER SCRIPT

"Before we can understand Itô's Lemma, we need to understand what it's operating on. And that means understanding Brownian motion — the mathematical object that Norbert Wiener formalized in 1923. [5]

Brownian motion — also written B(t) or W(t) — is defined by three axioms. [8]

[PAUSE — Axiom 1]

First: it starts at zero. B of zero equals zero. Clean slate.

[PAUSE — Axiom 2]

Second: increments are Normally distributed with variance equal to the elapsed time. The increment from time s to time t — B(t) minus B(s) — follows a Normal distribution with mean zero and variance t minus s. This is crucial: the uncertainty grows proportionally to *time*, not to time squared. That square-root-of-time scaling is why volatility scales with the square root of the holding period — a fact every risk manager on earth uses daily.

[PAUSE — Axiom 3]

Third: the increments are independent. Yesterday's move tells you nothing about today's move. The process has no memory. It's the financial equivalent of a goldfish.

[PAUSE — zoom into path]

And here's the property that breaks classical calculus completely: Brownian motion is almost surely continuous — no jumps — but nowhere differentiable. Zoom into any segment, no matter how small, and it's still rough. It's a fractal. It has no tangent anywhere.

[PAUSE — flash key property]

Now look at this property. The expected value of dB squared — the instantaneous variance — equals dt. The square of the random increment is deterministic in expectation. This is the single fact that makes Itô's correction term exist. Hold onto it. It will become everything.

Think of Brownian motion as the raw material. What Itô did was build the machinery to *work* with it — to differentiate and integrate functions of this chaotic object. Like building a lathe to cut stone that no blade had touched before."

---

## SCENE 3: QUADRATIC VARIATION — WHY CLASSICAL CALCULUS DIES
**Class:** `SceneQuadraticVariation` | **Duration:** ~3:30

### MANIM ANIMATION SEQUENCE

```
1. Title: "The Moment Classical Calculus Dies"
   Subtitle: "Quadratic Variation — the concept your professor skipped"

2. Classical Taylor expansion review:
   f(x + dx) = f(x) + f'(x)dx + ½f''(x)(dx)² + ...

   "In classical calculus, (dx)² → 0 as dx → 0.
    So we throw it away. No problem."

   Visual: (dx)² term with a big red TRASH icon. Satisfying animation.

3. Now: Stochastic Taylor expansion for f(B(t)):
   f(B(t) + dB) = f(B(t)) + f'(B(t))dB + ½f''(B(t))(dB)² + ...

   Question appears: "Can we throw away (dB)²?"

4. ANSWER: NO.
   Red X. Then show why:

   Table of orders:
   | Term   | Classical (smooth) | Stochastic (Brownian) |
   |--------|--------------------|-----------------------|
   | dt     | O(dt)              | O(dt)                 |
   | dB     | O(√dt)             | O(√dt)                |
   | (dt)²  | O(dt²) → 0 ✓      | O(dt²) → 0 ✓          |
   | dt·dB  | O(dt^(3/2)) → 0 ✓ | O(dt^(3/2)) → 0 ✓     |
   | (dB)²  | O(dt) → 0 ✓       | O(dt) ← DOES NOT → 0! |

   Flash the last row in orange. Alarm bell animation.

5. Formal result — Quadratic Variation of Brownian Motion:
   [B, B]_t = lim_{n→∞} Σ (B(tᵢ) - B(tᵢ₋₁))² = t   a.s.

   "The sum of squared increments converges to t — not to zero.
    This is NOT in your calculus textbook."

   Source: "[6] Shreve (2004), Theorem 3.4.3"

6. Multiplication table for stochastic differentials:
   Box with multiplication table:
   ┌────────┬────┬────┐
   │   ×    │ dt │ dB │
   ├────────┼────┼────┤
   │   dt   │  0 │  0 │
   │   dB   │  0 │ dt │
   └────────┴────┴────┘

   "(dB)² = dt is the central fact. Not an approximation. An equality."
   Source: "[7] Øksendal (2003), Lemma 4.1.7"

7. Sarcastic comment text in gold italics:
   "Yes. The square of a random term is deterministic.
    Stochastic calculus is built on this audacity."
```

### VOICE-OVER SCRIPT

"Now here's where things get genuinely interesting — and where every student who learned calculus and thought they were done gets a very rude awakening.

[PAUSE — show Taylor expansion]

In classical calculus, when you expand a smooth function f of x plus dx using a Taylor series, you get f of x, plus the first derivative times dx, plus one-half the second derivative times dx squared, and so on. And as dx goes to zero, the squared term goes to zero *faster* — it's order dx squared, which is negligible compared to dx. So you throw it away. That's the entire story of classical differentiation. [6]

[PAUSE — show stochastic version]

Now try the same trick with Brownian motion. Replace dx with dB — the infinitesimal Brownian increment. You get the same expansion: f prime times dB, plus one-half f double-prime times dB squared.

And here's the question that defines stochastic calculus: can we throw away dB squared the same way?

[PAUSE — show table]

The answer is a categorical no — and the reason is in this table of orders. In classical calculus, dt squared goes to zero — fine. dt times dB goes to zero — fine. But dB squared? dB is of order square root of dt. So dB squared is of order dt. Which does NOT go to zero. It stays. It matters. It changes the answer.

[PAUSE — show quadratic variation formula]

This fact has a name: the quadratic variation of Brownian motion. The sum of squared increments of B over any partition of the time interval converges — almost surely — not to zero but to t. The length of the time interval. [6]

This result — which goes by Theorem 3.4.3 in Shreve's Stochastic Calculus for Finance — is what separates Itô's world from Newton's world.

[PAUSE — show multiplication table]

We can write this compactly as a multiplication table for stochastic differentials. dt times dt is zero. dt times dB is zero. But dB times dB equals dt. [7]

Not approximately. Not in some limiting sense. Equals.

[PAUSE — sarcastic comment]

The square of a random quantity is deterministic. Stochastic calculus is built on this audacity. And if your first instinct is that this feels wrong — good. That means your mathematical instincts are working. They're just calibrated for the wrong universe.

Markets live in Itô's universe. Not Newton's."

---

## SCENE 4: ITÔ'S LEMMA — THE FULL DERIVATION
**Class:** `SceneItoLemma` | **Duration:** ~5:00

### MANIM ANIMATION SEQUENCE

```
1. Title: "Itô's Lemma — The Full Proof"
   Source block top-right (small):
   "[1] Itô (1944) | [2] Itô (1951) | [6] Shreve (2004)"

2. Setup: Let X(t) be an Itô process:
   dX = μ(X,t)dt + σ(X,t)dB

   Label each term:
   μ(X,t)dt  → "Drift term — deterministic direction"
   σ(X,t)dB  → "Diffusion term — random shock"

   Visual: Arrow pointing right (drift) + zigzag overlay (diffusion)

3. Goal: Find df(X(t), t) for a smooth function f.

4. Step 1 — Taylor expand to second order:
   df = ∂f/∂t · dt + ∂f/∂X · dX + ½∂²f/∂X² · (dX)² + (higher order)

   Each partial derivative lights up as it's introduced.

5. Step 2 — Substitute dX:
   dX = μdt + σdB

   (dX)² = (μdt + σdB)²
          = μ²(dt)² + 2μσ(dt)(dB) + σ²(dB)²

6. Step 3 — Apply Itô's multiplication table:
   (dt)² → 0
   dt·dB → 0
   (dB)² → dt

   So: (dX)² = σ²dt

   The two zero terms vanish with dramatic animation (fade + poof).
   The σ²dt term GLOWS gold.

7. Step 4 — Assemble:
   df = ∂f/∂t · dt + ∂f/∂X · (μdt + σdB) + ½ · ∂²f/∂X² · σ²dt

8. Step 5 — Collect dt and dB terms:
   ┌─────────────────────────────────────────────────────────┐
   │                                                         │
   │  df = (∂f/∂t + μ∂f/∂X + ½σ²∂²f/∂X²)dt + σ∂f/∂X dB   │
   │                                                         │
   └─────────────────────────────────────────────────────────┘

   Box pulses gold. This is the result.

9. Label the correction term with a glowing bracket:
   "½σ²∂²f/∂X²  ← THE ITÔ CORRECTION"
   "This term does not exist in classical calculus.
    This term is the difference between being right and being broke."

10. Three-way comparison panel:
    Classical chain rule:   df = f'(x)dx
    Classical total deriv:  df = ∂f/∂t dt + ∂f/∂x dx
    Itô's Lemma:           df = (∂f/∂t + μ∂f/∂x + ½σ²∂²f/∂x²)dt + σ∂f/∂x dB

    The extra term blazes in orange.

11. Taleb quote fades in gold italics at bottom:
    "The problem with experts is that they do not know what they do not know."
    — N.N. Taleb, The Black Swan [9]
    
    Beat. Then:
    "Itô knew what the experts didn't know they didn't know."
    — Quantifaya
```

### VOICE-OVER SCRIPT

"Right. Gloves off. We're deriving Itô's Lemma from first principles. No hand-waving. No 'it can be shown.' We're doing the actual proof. [1][2]

[PAUSE — show Itô process]

Let X(t) be an Itô process — a stochastic process described by this SDE: dX equals mu dt plus sigma dB. The mu term is the drift — the deterministic trend. The sigma dB term is the diffusion — the random shock. Every continuous-time financial model you've ever seen is a special case of this structure.

[PAUSE — state the goal]

The question Itô asked — and answered — is this: if X follows this process, and f is a smooth function of X and t, what process does f follow?

In classical calculus, the answer is just the chain rule. In stochastic calculus, the chain rule is wrong. And Itô's Lemma tells you why, and by how much.

[PAUSE — Step 1: Taylor expansion]

Step one. Taylor expand f to second order in dX and dt.

df equals partial f over partial t, times dt — the time derivative — plus partial f over partial X, times dX — the space derivative — plus one-half partial squared f over partial X squared, times dX squared. And higher-order terms.

So far this looks like classical calculus. The crime happens in the next step.

[PAUSE — Step 2: substitute dX]

Step two. Substitute dX equals mu dt plus sigma dB. Now compute dX squared. That's mu dt plus sigma dB, all squared, which gives mu squared dt squared, plus two mu sigma dt dB, plus sigma squared dB squared.

[PAUSE — Step 3: apply multiplication table]

Step three. Apply Itô's multiplication table. dt squared is zero — negligible. dt times dB is zero — negligible. But dB squared equals dt.

Watch what happens. Two of the three terms in dX squared vanish — gone — and we're left with sigma squared dt.

[PAUSE — glow on σ²dt]

That's the Itô correction. It came from the squared term in the Taylor expansion that classical calculus told you to throw away. Except in Itô's world, you cannot throw it away, because dB squared is not small — it equals dt.

[PAUSE — Step 5: assemble final result]

Step four and five — substitute back and collect terms. Group everything multiplying dt and everything multiplying dB. And we arrive at Itô's Lemma:

df equals — open bracket — partial f over partial t, plus mu times partial f over partial X, plus ONE HALF sigma squared times the second partial of f over X squared — close bracket — times dt, plus sigma times partial f over partial X, times dB.

[PAUSE — highlight correction term]

This term. One-half sigma squared times the second derivative of f. This is the Itô correction. This is the term that does not exist in classical calculus. This is the term that, when you ignore it, leads to mispriced derivatives and blown-up funds.

In classical calculus, the chain rule is a first-order story. Itô's Lemma is a second-order story — because randomness lives at the second-order level.

[PAUSE — Taleb quote]

Nassim Taleb once wrote: 'The problem with experts is that they do not know what they do not know.' [9] Pre-Itô quants didn't know they were missing a correction term. They were confidently, expensively wrong. Itô knew what the experts didn't know they didn't know. That's what genius looks like."

---

## SCENE 5: GEOMETRIC BROWNIAN MOTION — APPLYING ITÔ
**Class:** `SceneGBM` | **Duration:** ~3:30

### MANIM ANIMATION SEQUENCE

```
1. Title: "Geometric Brownian Motion — Itô's Lemma in Action"

2. The canonical model for stock prices:
   dS = μS dt + σS dB

   Label each term:
   S    → stock price
   μ    → expected return (drift)
   σ    → volatility
   dB   → Brownian shock

   Visual: S(t) paths — multiple GBM sample paths fan out from S₀.
   Some go up, some crash. All positive (GBM stays positive).

3. Question: "What does ln(S) follow?"

4. Apply Itô's Lemma with f(S,t) = ln(S):

   ∂f/∂t = 0
   ∂f/∂S = 1/S
   ∂²f/∂S² = -1/S²

   Substituting into Itô's Lemma:

   d(ln S) = (0 + μS · 1/S + ½σ²S² · (-1/S²))dt + σS · (1/S)dB

           = (μ - ½σ²)dt + σ dB

5. Box this result — it deserves its own moment:
   ┌─────────────────────────────────────────────────────┐
   │                                                     │
   │     d(ln S) = (μ - ½σ²)dt + σdB                   │
   │                                                     │
   │     ln S(T) - ln S(0) ~ N((μ - ½σ²)T, σ²T)        │
   │                                                     │
   │     S(T) = S(0) · exp((μ - ½σ²)T + σ√T · Z)       │
   │            where Z ~ N(0,1)                         │
   └─────────────────────────────────────────────────────┘

6. CRUCIAL INSIGHT — animate the ½σ² gap:

   Side by side:
   Left:  "Arithmetic mean return: μ"
   Right: "Geometric mean return:  μ - ½σ²"
   Gap:   "½σ² — the volatility drag"
   
   Concrete example:
   σ = 20%, ½σ² = 2%
   "Even if your expected return is 10%, your geometric mean is only 8%.
    Volatility eats your compounding. Every year. Silently."

7. Plot: Two paths on same axes:
   - E[S(t)] = S₀ exp(μt)   (arithmetic mean — goes up fast, blue)
   - Median S(t) = S₀ exp((μ-½σ²)t)  (geometric mean — slower, orange)
   - The GAP widens over time

8. Source: "[6] Shreve (2004), Ch.4 | [13] Protter (2005)"
   "[10] Hull (2018), Ch.15 — GBM as the Black-Scholes foundation"
```

### VOICE-OVER SCRIPT

"Now let's use Itô's Lemma to do something concrete — derive the solution to the most important SDE in quantitative finance: Geometric Brownian Motion. [6][10]

[PAUSE — show GBM equation]

The standard model for stock prices under the risk-neutral measure is: dS equals mu S dt plus sigma S dB. The drift scales with the price — so we get percentage returns, not dollar returns. The diffusion also scales with price — so volatility is proportional, which is why we talk about 20% annual volatility rather than twenty dollars per share.

[PAUSE — multiple sample paths]

These are sample paths from this process. Notice they can go up or down, but they never touch zero — because the percentage changes scale with S, so you can never lose more than a hundred percent. GBM respects limited liability. It's a feature.

[PAUSE — pose question]

Now here's the question. What does the logarithm of S follow? Because log-returns are what we actually compute in practice, and understanding their distribution gives us the analytical solution for S(T).

[PAUSE — apply Itô step by step]

Set f equal to log S. The partial derivative with respect to t is zero — f has no explicit time dependence. The first partial with respect to S is one over S. The second partial with respect to S is negative one over S squared.

Plug these into Itô's Lemma. The drift contribution gives us mu S times one over S — which is just mu — plus one-half sigma squared S squared times negative one over S squared — which gives negative one-half sigma squared. The diffusion contribution gives sigma S times one over S — which simplifies to sigma.

[PAUSE — box the result]

The result is beautiful. d of log S equals mu minus one-half sigma squared, all times dt, plus sigma dB. This is just a constant-coefficient SDE. Its solution is trivial: log S is Normally distributed with mean mu minus one-half sigma squared times T, and variance sigma squared T.

Which means S itself is log-normally distributed — and we can write out the explicit closed-form solution for S at any future time T.

[PAUSE — volatility drag illustration]

But look at the drift of the log-return: mu minus one-half sigma squared. Not mu. There's a haircut. A drag.

This is the volatility drag — and it's one of the most underappreciated facts in portfolio management. [13] If your annual expected return is ten percent and your annual volatility is twenty percent, your geometric mean compound return is not ten percent — it's eight percent. Two percent per year, compounding quietly against you, forever.

[PAUSE — show diverging paths]

Watch what happens over a long horizon. The arithmetic mean of S — which is S₀ times e to the mu t — grows faster than the typical outcome. The median of S — S₀ times e to the mu minus half sigma squared times t — is what most investors actually experience. And the gap between them widens every year. [6]

Itô's correction term isn't abstract mathematics. It's the gap between what a fund advertises and what investors actually receive."

---

## SCENE 6: THE ITÔ INTEGRAL — WHAT INTEGRATION MEANS HERE
**Class:** `SceneItoIntegral` | **Duration:** ~2:30

### MANIM ANIMATION SEQUENCE

```
1. Title: "The Itô Integral — You Can't Use Riemann Here Either"

2. Classical Riemann integral setup:
   ∫₀ᵀ f(t) dt = lim Σ f(tᵢ*)(tᵢ - tᵢ₋₁)
   
   "You evaluate f at any point in each interval. Result is the same.
    Order doesn't matter. Time doesn't matter."

3. Now: the stochastic integral ∫₀ᵀ H(t) dB(t)
   "You CANNOT evaluate H at the right endpoint of each interval.
    The future hasn't happened yet.
    You must use the LEFT endpoint — you can only know the PAST."

4. This is the Itô convention — non-anticipating (adapted) integrands:
   ∫₀ᵀ H(t) dB(t) = lim Σ H(tᵢ₋₁)(B(tᵢ) - B(tᵢ₋₁))
   
   "H must be ℱ(t)-measurable — it can only use information
    available up to time t. No peeking at the future."
   
   Source: "[6] Shreve (2004), Ch.3 | [7] Øksendal (2003), Ch.3"

5. Key properties box:
   E[∫₀ᵀ H dB] = 0         ← "The integral has zero mean"
   E[(∫₀ᵀ H dB)²] = E[∫₀ᵀ H² dt]   ← "Itô Isometry"
   
   The Itô Isometry equation glows:
   \mathbb{E}\!\left[\left(\int_0^T H\,dB\right)^{\!2}\right]
   = \mathbb{E}\!\left[\int_0^T H^2\,dt\right]

6. Plain-English translation:
   "The variance of a stochastic integral equals
    the expected integral of the squared integrand.
    This is why dB² = dt is not just a trick — it's a theorem."

7. Sarcastic aside in gold:
   "If you're thinking 'this seems needlessly complicated' —
    you're right. But the alternative is mispricing derivatives.
    Your call."
```

### VOICE-OVER SCRIPT

"Before we get to Black-Scholes, we need one more piece: the Itô integral. Because just as differentiation doesn't work classically here, neither does integration.

[PAUSE — show Riemann integral]

In classical calculus, the Riemann integral doesn't care where in each interval you evaluate the function. Left endpoint, right endpoint, midpoint — in the limit, they all give the same answer. The integral is path-independent.

[PAUSE — show stochastic integral]

Not here. When we integrate a process H with respect to Brownian motion, we are forced to use the left endpoint of each interval. Always. Not because it's convenient — because it's the *only* causally consistent choice. [6]

In financial terms: when you hold a position H(t) over the interval from t to t plus dt, you must decide your position size *before* observing the Brownian shock in that interval. You can't know the future. The integral enforces this.

[PAUSE — show Itô integral definition]

This non-anticipating requirement means the integrand H must be adapted to the filtration — it can only use information available up to the current time t. If you use future information, you're not computing an Itô integral. You're cheating. And in trading, cheating is called insider trading. [7]

[PAUSE — show Itô isometry]

The Itô integral has two key properties. First, its expected value is zero — because Brownian increments are mean-zero, and we're evaluating H before seeing them. No free lunch. Second — and this is the jewel — the Itô Isometry: the variance of the stochastic integral equals the expected value of the integral of H squared. This is the stochastic analogue of Parseval's theorem. [6]

[PAUSE — sarcastic aside]

If this feels complicated — it is. But the Itô integral is the only mathematically honest way to price a derivative. Every other approach is either an approximation or a prayer. The derivatives desk doesn't do prayers."

---

## SCENE 7: BLACK-SCHOLES — ITÔ'S LEMMA DEPLOYED IN BATTLE
**Class:** `SceneBlackScholes` | **Duration:** ~4:00

### MANIM ANIMATION SEQUENCE

```
1. Title: "Black-Scholes — Itô's Lemma Goes to War"
   Sources: "[3] Black & Scholes (1973) | [4] Merton (1973)"

2. Setup: 
   Stock follows GBM: dS = μS dt + σS dB
   Option price: V = V(S, t)
   
   "We want to price V. We know nothing about μ.
    Watch how Itô's Lemma eliminates it entirely."

3. Apply Itô's Lemma to V(S,t):

   dV = (∂V/∂t + μS∂V/∂S + ½σ²S²∂²V/∂S²)dt + σS∂V/∂S dB

   Label the bracket as "the full dynamics of V"

4. CONSTRUCTION: The Delta-Hedged Portfolio
   
   Π = V - ΔS    (long option, short Δ shares)
   
   where Δ = ∂V/∂S  (the option's delta)

5. Compute dΠ:
   dΠ = dV - Δ dS
      = dV - (∂V/∂S)(μS dt + σS dB)

   Substitute dV from Itô:
   dΠ = (∂V/∂t + μS∂V/∂S + ½σ²S²∂²V/∂S²)dt + σS∂V/∂S dB
        - ∂V/∂S · μS dt - ∂V/∂S · σS dB

6. MAGIC: The dB terms cancel exactly!
   Animate the two σS(∂V/∂S)dB terms highlighting and cancelling.
   BIG visual — sparks, cross-out, dramatic.
   
   dΠ = (∂V/∂t + ½σ²S²∂²V/∂S²)dt

   "The randomness is gone. The portfolio is RISKLESS."
   μ has also vanished. Label: "The drift disappears too."

7. No-arbitrage argument:
   A riskless portfolio must earn the risk-free rate r:
   dΠ = rΠ dt = r(V - ΔS)dt = r(V - S∂V/∂S)dt

8. Set the two expressions for dΠ equal:
   ∂V/∂t + ½σ²S²∂²V/∂S² = r(V - S∂V/∂S)

9. Rearrange — THE BLACK-SCHOLES PDE:
   ┌──────────────────────────────────────────────────┐
   │                                                  │
   │  ∂V/∂t + rS∂V/∂S + ½σ²S²∂²V/∂S² - rV = 0     │
   │                                                  │
   └──────────────────────────────────────────────────┘
   
   Box pulses purple. Hold for 3 seconds. Let it breathe.

10. Label each term:
    ∂V/∂t          → "theta — time decay"
    rS∂V/∂S        → "rho-delta — rate × delta"
    ½σ²S²∂²V/∂S²  → "gamma term — convexity"
    -rV             → "discounting"

11. The analytical solution for a European call:
    C(S,t) = SN(d₁) - Ke^{-r(T-t)}N(d₂)
    
    d₁ = [ln(S/K) + (r + ½σ²)(T-t)] / (σ√(T-t))
    d₂ = d₁ - σ√(T-t)
    
    "Notice d₁ contains ½σ² — Itô's correction.
     It was there the whole time, hiding in plain sight."

12. Source box bottom:
    "[3] Black & Scholes (1973), J. Political Economy, 81(3)"
    "[4] Merton (1973), Bell J. Economics, 4(1)"
```

### VOICE-OVER SCRIPT

"Here it is. The application that made Itô a billionaire-maker — even though he never cared about money. Black-Scholes. Derived live, from scratch, using Itô's Lemma. [3][4]

[PAUSE — show setup]

Stock price S follows Geometric Brownian Motion: dS equals mu S dt plus sigma S dB. Option price V depends on S and t. We want to know what V is worth today. And here's the first remarkable thing: we're going to get the answer without ever knowing mu — the expected return of the stock. That's not a typo. Watch.

[PAUSE — apply Itô to V]

Apply Itô's Lemma to V of S and t. We get: dV equals the bracket — partial V over partial t, plus mu S partial V over partial S, plus one-half sigma squared S squared times the second partial of V over S squared — close bracket — times dt, plus sigma S partial V over partial S, times dB.

This describes how the option value changes over an instant. Now here's the cleverness.

[PAUSE — construct delta-hedge]

Construct a portfolio Pi: long one option, short Delta units of stock, where Delta equals partial V over partial S — the option's delta. The portfolio value is V minus Delta times S.

Compute dPi. It's dV minus Delta times dS. Substitute Itô's dV and the GBM dS.

[PAUSE — MAGIC: cancellation animation]

Watch what happens to the dB terms. We have sigma S partial V over partial S times dB from the dV term. And we subtract partial V over partial S times sigma S dB from the Delta-dS term. These are identical. They cancel. Exactly. Completely.

The randomness is gone.

And look — mu — the drift, the expected return — it also cancels. The delta-hedged portfolio's dynamics depend on *neither* the expected return of the stock *nor* the random Brownian shock. Both annihilated by the hedge.

[PAUSE — show deterministic portfolio]

dPi equals partial V over partial t, plus one-half sigma squared S squared times the second partial of V over S squared, times dt. A deterministic expression. A riskless portfolio.

[PAUSE — no-arbitrage condition]

In an efficient market, a riskless portfolio must earn exactly the risk-free rate r. Otherwise there's an arbitrage — a money machine — and money machines don't persist. Set the two expressions for dPi equal and rearrange.

[PAUSE — Black-Scholes PDE]

And we have it. The Black-Scholes partial differential equation.

Partial V over partial t, plus rS times partial V over partial S, plus one-half sigma squared S squared times the second partial of V over S squared, minus rV equals zero. [3]

[PAUSE — label the Greeks]

Each term has a name traders use every day. Theta — time decay. The gamma term — convexity, the curvature of the option's value. And the discounting term. This PDE, subject to the terminal boundary condition V equals max of S minus K, zero, at expiry, gives the Black-Scholes formula.

[PAUSE — show formula and highlight d₁]

Notice d₁ in the Black-Scholes formula contains one-half sigma squared. Itô's correction, embedded permanently in the price of every option traded on every exchange on earth. [4]

Itô wrote four pages in 1944. In 1973, Black and Scholes weaponized them. In 1997, Scholes won the Nobel Prize. Itô won the Gauss Prize in 2006 — mathematics' equivalent.

The market paid better."

---

## SCENE 8: ITÔ VS. STRATONOVICH — THE CONVENTION WAR
**Class:** `SceneItoVsStrat` | **Duration:** ~2:00

### MANIM ANIMATION SEQUENCE

```
1. Title: "The Convention War Nobody Tells You About"

2. Two integrals side by side:

   ITÔ:          ∫₀ᵀ H(t) dB = lim Σ H(tᵢ₋₁)(B(tᵢ)-B(tᵢ₋₁))
   STRATONOVICH: ∫₀ᵀ H(t) ∘ dB = lim Σ H((tᵢ+tᵢ₋₁)/2)(B(tᵢ)-B(tᵢ₋₁))

   "Stratonovich uses the MIDPOINT instead of the left endpoint."

3. Consequences table:
   | Property               | Itô          | Stratonovich        |
   |------------------------|--------------|---------------------|
   | Classical chain rule   | ✗ (needs correction) | ✓ (works!)  |
   | Zero-mean integral     | ✓            | ✗                   |
   | Itô Isometry           | ✓            | ✗                   |
   | Financial modeling     | ✓ (causal)   | ✗ (uses future info)|
   | Physics / Engineering  | ✓ sometimes  | ✓ (preferred)       |

4. Key message:
   "Stratonovich satisfies the classical chain rule — which is WHY
    physicists prefer it. Itô forces the correction — which is WHY
    finance requires it."

5. Conversion formula:
   ∫₀ᵀ H ∘ dB = ∫₀ᵀ H dB + ½∫₀ᵀ (∂H/∂B) dt

   "You can always convert between them.
    But in finance, Itô is not optional."

6. Wilmott quote in gold:
   "The Itô correction is not an error. It is the price of randomness."
   — P. Wilmott, Paul Wilmott on Quantitative Finance [11]
```

### VOICE-OVER SCRIPT

"One thing nobody tells you in a quant course: Itô's convention is not the only one. There's a parallel universe called Stratonovich calculus that physicists and engineers often prefer — and understanding why finance rejects it is important. [11]

[PAUSE — show two integrals]

The difference is subtle but profound. Itô uses the left endpoint of each time interval — we evaluate H before seeing the Brownian shock. Stratonovich uses the midpoint — which requires partial information about the future. This gives Stratonovich a beautiful property: the classical chain rule holds without any correction term. Newton's ghost is happy.

[PAUSE — show table]

But for finance, Stratonovich is inadmissible. Using the midpoint means using information that doesn't exist yet at the time you need to make a trading decision. It violates causality. It's the mathematical equivalent of front-running. [11]

Itô's convention enforces the reality constraint: you can only act on what you know now.

[PAUSE — show conversion formula]

The two integrals differ by exactly one-half the integral of the derivative of H with respect to B. You can always convert between them. But in financial modeling, Itô is not a preference — it's a constraint imposed by the arrow of time.

The Itô correction isn't an inconvenience. It's the mathematical price of operating in a world where time flows in only one direction and information arrives sequentially. Which is, inconveniently, the world we live in."

---

## SCENE 9: THE REAL LESSON — AXELROD-LEVEL TAKEAWAYS
**Class:** `SceneLessons` | **Duration:** ~2:00

### MANIM ANIMATION SEQUENCE

```
1. Title: "What This Actually Means For You"
   Subtitle in gold: "— the version your textbook was too polite to say"

2. TRUTH 1 — in red bold:
   "Every time you ignore the Itô correction,
    you are systematically mispricing convexity."
   
   Visual: Two P&L curves — with and without Itô correction — diverge over time.
   Gap labeled: "The cost of classical thinking"

3. TRUTH 2 — in gold:
   "Volatility drag is real. Compound returns ≠ expected returns.
    μ - ½σ² is what you actually earn. Not μ."
   
   Numerical example:
   μ = 12%, σ = 25%
   ½σ² = 3.125%
   Geometric mean = 8.875%
   "You're giving up 3.1% per year. Forever. To volatility."

4. TRUTH 3 — in teal:
   "Itô's Lemma is the reason delta-hedging works.
    Without it, there is no Black-Scholes.
    Without Black-Scholes, the $600T derivatives market has no foundation."

5. TRUTH 4 — in purple (most important):
   "Every quant interview will ask you to derive this.
    Not the formula. The DERIVATION.
    The correction term is the signal. If you can explain why,
    you're in the top 5% of candidates."

6. Taleb final quote — large, gold, centred:
   "Anything that has been around for a long time
    has proven its antifragility."
   — N.N. Taleb, Antifragile [9]
   
   Beat. Then:
   "Itô's Lemma has been around since 1944.
    It is not going anywhere.
    Learn it. Own it."
   — Quantifaya

7. Sources scroll across bottom (like film credits):
   [1] Itô (1944) | [2] Itô (1951) | [3] Black & Scholes (1973) |
   [4] Merton (1973) | [5] Wiener (1923) | [6] Shreve (2004) |
   [7] Øksendal (2003) | [8] Karatzas & Shreve (1991) |
   [9] Taleb (2007, 2012) | [10] Hull (2018) | [11] Wilmott (2006) |
   [12] Mandelbrot & Hudson (2004) | [13] Protter (2005)
```

### VOICE-OVER SCRIPT

"Let's land this plane with four truths — the version the textbooks are too polite to state directly.

[PAUSE — Truth 1]

First: every time you ignore the Itô correction, you are systematically mispricing convexity. Not occasionally. Not under edge cases. Systematically. Every model without the second-order term understates the value of options, underestimates the cost of hedging, and overstates the performance of leveraged strategies. The correction is not optional.

[PAUSE — Truth 2]

Second: volatility drag is real money. If your fund earns a 12% expected return with 25% volatility, your geometric compound return is not twelve percent — it's 8.875%. You are surrendering over three percent per year to the Itô correction. Compounding over twenty years, that's the difference between retiring and working until you're seventy. Nobody told you this at the fundraise.

[PAUSE — Truth 3]

Third: Itô's Lemma is the reason delta-hedging works. It's the reason Black-Scholes exists. It's the mathematical foundation of a six-hundred-trillion dollar market. This isn't an academic curiosity. This is the bedrock of modern finance — and it lives in four pages written by a Japanese mathematician during World War II. [3][4]

[PAUSE — Truth 4]

Fourth, and most practical: in a quant interview, you will be asked about this. Not the formula — the derivation. Knowing that dB squared equals dt and being able to explain why it can't be discarded is the signal that separates candidates who understand the mathematics from those who memorized it. The Itô correction is the differentiator. Literally.

[PAUSE — Taleb quote]

Nassim Taleb wrote in Antifragile: 'Anything that has been around for a long time has proven its antifragility.' [9] Itô's Lemma has been around since 1944. Through every market crash, every quantitative revolution, every Nobel Prize in economics — it's still here. Still right. Still running every derivatives desk on earth.

Learn it. Own it. It might be the most important four pages ever written."

---

## SCENE 10: OUTRO — CTA & NEXT EPISODE
**Class:** `SceneOutro` | **Duration:** ~1:00

### MANIM ANIMATION SEQUENCE

```
1. Quantifaya logo pulses in purple. Tagline:
   "Financial Engineering. Explained Rigorously. Applied Practically."

2. Episode recap — bullets fly in:
   ✓ Brownian motion: axioms, properties, nowhere differentiable
   ✓ Quadratic variation: why (dB)² = dt and cannot be discarded
   ✓ Itô's Lemma: full Taylor-expansion derivation
   ✓ GBM: log-return distribution and volatility drag
   ✓ Itô integral: non-anticipating, Itô isometry
   ✓ Black-Scholes PDE: derived live from Itô + no-arbitrage
   ✓ Itô vs. Stratonovich: why finance requires Itô's convention

3. Book recommendations (two covers):
   📚 "Stochastic Calculus for Finance II" — Shreve (2004) [6]
   "The rigorous Bible. Chapter 3 and 4 are this entire video."
   
   📚 "Paul Wilmott on Quantitative Finance" — Wilmott (2006) [11]
   "The applied Bible. Volume 1, the GBM chapter. Non-negotiable."

4. Next episode tease:
   MathTex: Black-Scholes formula glows
   C = SN(d₁) - Ke^{-rT}N(d₂)
   
   "Next on Quantifaya:"
   "The Greeks: Delta, Gamma, Vega — Built Intuitively"
   "What do they really measure? Why does Gamma hurt you?
    And why every options trader thinks in Greek."

5. Comment prompt:
   "Drop your answer below:
    What is the Itô correction term for f(S) = S²?
    First correct derivation in the comments gets pinned."
   (Answer: df = 2S dS + σ²S² dt = (2μS² + σ²S²)dt + 2σS² dB)

6. Subscribe animation. End card.
```

### VOICE-OVER SCRIPT

"That's Episode 2 of Quantifaya.

[PAUSE — recap]

We covered the complete story — from Brownian motion's axioms, through quadratic variation and why dB squared equals dt and cannot be thrown away, through the full derivation of Itô's Lemma, through Geometric Brownian Motion and the volatility drag, through the Itô integral and its isometry, and finally to Black-Scholes — derived from scratch, live, in real time.

[PAUSE — book recommendations]

Two books belong on your desk after this video. Shreve's Stochastic Calculus for Finance II — the rigorous version of everything we covered, Chapters 3 and 4 specifically. And Paul Wilmott on Quantitative Finance — the applied version, with the intuition and the worked examples. Both links are in the description.

[PAUSE — next episode tease]

Next week, we take the Black-Scholes formula and extract its weapons: Delta, Gamma, Vega, Theta, Rho — the Greeks. We'll build every single one from first principles, show you what they mean economically, and explain why Gamma exposure is the most dangerous thing a derivatives desk can run. Don't miss it.

[PAUSE — comment challenge]

One final thing. Here's a challenge: using today's tools, derive the Itô correction for f of S equals S squared. If your expected return is mu and your vol is sigma, what does d of S squared equal? First correct full derivation in the comments gets pinned for a week.

Subscribe. Share this with one person studying for a quant interview — it'll probably get them the job.

This is Quantifaya."

---

---

## APPENDIX A — FULL EQUATION REFERENCE

| Equation | LaTeX | Scene |
|---|---|---|
| Standard BM definition | `B(0)=0,\; B(t)-B(s)\sim\mathcal{N}(0,t-s)` | 2 |
| Key BM property | `E[(dB)^2]=dt` | 2 |
| Quadratic variation | `[B,B]_t=\lim_{n\to\infty}\sum_{i=1}^n(B(t_i)-B(t_{i-1}))^2=t` | 3 |
| Stochastic multiplication | `(dB)^2=dt,\; dt\cdot dB=0,\; (dt)^2=0` | 3 |
| Itô process | `dX=\mu(X,t)\,dt+\sigma(X,t)\,dB` | 4 |
| Itô's Lemma | `df=\!\left(\tfrac{\partial f}{\partial t}+\mu\tfrac{\partial f}{\partial X}+\tfrac{1}{2}\sigma^2\tfrac{\partial^2 f}{\partial X^2}\right)dt+\sigma\tfrac{\partial f}{\partial X}\,dB` | 4 |
| GBM | `dS=\mu S\,dt+\sigma S\,dB` | 5 |
| Log-return SDE | `d(\ln S)=(\mu-\tfrac{1}{2}\sigma^2)\,dt+\sigma\,dB` | 5 |
| GBM closed form | `S(T)=S(0)\exp\!\left((\mu-\tfrac{1}{2}\sigma^2)T+\sigma\sqrt{T}\,Z\right)` | 5 |
| Itô integral | `\int_0^T H\,dB=\lim\sum H(t_{i-1})(B(t_i)-B(t_{i-1}))` | 6 |
| Itô Isometry | `E\!\left[\left(\int_0^T H\,dB\right)^2\right]=E\!\left[\int_0^T H^2\,dt\right]` | 6 |
| Delta-hedge portfolio | `\Pi=V-\tfrac{\partial V}{\partial S}\cdot S` | 7 |
| Black-Scholes PDE | `\tfrac{\partial V}{\partial t}+rS\tfrac{\partial V}{\partial S}+\tfrac{1}{2}\sigma^2S^2\tfrac{\partial^2 V}{\partial S^2}-rV=0` | 7 |
| BS Call Formula | `C=SN(d_1)-Ke^{-r(T-t)}N(d_2)` | 7 |
| d₁, d₂ | `d_1=\frac{\ln(S/K)+(r+\frac{1}{2}\sigma^2)(T-t)}{\sigma\sqrt{T-t}},\; d_2=d_1-\sigma\sqrt{T-t}` | 7 |
| Stratonovich conversion | `\int_0^T H\circ dB=\int_0^T H\,dB+\tfrac{1}{2}\int_0^T\tfrac{\partial H}{\partial B}\,dt` | 8 |
| Volatility drag | `\text{Geometric mean}=\mu-\tfrac{1}{2}\sigma^2` | 5, 9 |

---

## APPENDIX B — COMPLETE MANIM PYTHON SKELETON

```python
# quantifaya_ep2.py
# Run: manim -pqh quantifaya_ep2.py FullEpisode --fps 60 --resolution 1920x1080

from manim import *
import numpy as np
from scipy.stats import norm

# ── BRAND COLOURS ──────────────────────────────────────────────────────────
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

# ── HELPER: citation tag ────────────────────────────────────────────────────
def cite(refs: str) -> Text:
    return Text(refs, color=TEAL, font_size=14).to_corner(DR).shift(UP*0.1+LEFT*0.1)


# ═══════════════════════════════════════════════════════════════════════════
# SCENE 1 — COLD OPEN
# ═══════════════════════════════════════════════════════════════════════════
class SceneIntro(Scene):
    def construct(self):
        # Year hook
        year = Text("1944.", color=FG, font_size=72, weight=BOLD)
        self.play(FadeIn(year)); self.wait(1.5)

        t2 = Text("A Japanese mathematician named Kiyosi Itô\nwrote four pages.",
                  color=FG, font_size=40, line_spacing=1.4)
        self.play(Transform(year, t2)); self.wait(2)

        t3 = Text("Those four pages are worth\n$600,000,000,000,000.",
                  color=FG, font_size=40, line_spacing=1.4)
        self.play(Transform(year, t3)); self.wait(2)

        t4 = Text("Six hundred trillion dollars.\nThe global derivatives market.",
                  color=GOLD, font_size=44, weight=BOLD, line_spacing=1.4)
        self.play(Transform(year, t4)); self.wait(2)

        src = cite("[1] Itô (1944), Proc. Imperial Academy Tokyo, 20(8), 519–524")
        self.play(FadeIn(src))

        shock = Text("Your calculus professor never mentioned this.\nThere's a reason.",
                     color=RED, font_size=36, line_spacing=1.4)
        self.play(Transform(year, shock), FadeOut(src)); self.wait(2)
        self.play(FadeOut(year))

        # Smooth curve → Brownian glitch
        ax = Axes(x_range=[0,10,1], y_range=[-2,3,1],
                  x_length=10, y_length=5, axis_config={"color": FG})
        smooth = ax.plot(lambda x: 0.3*x + np.sin(x)*0.3,
                         color=BLUE_NORM, stroke_width=3)
        lbl_s = Text("f(x) — classical calculus", color=BLUE_NORM, font_size=22)\
                    .next_to(ax, UP)
        tangent = ax.plot(lambda x: 0.3*x + 0.3, color=GREEN, stroke_width=2)

        self.play(Create(ax), Create(smooth), FadeIn(lbl_s))
        self.play(Create(tangent))
        self.wait(1)

        # Generate BM path
        np.random.seed(7)
        n = 200
        dt_ = 10/n
        bm = np.cumsum(np.random.randn(n)*np.sqrt(dt_))
        bm_points = [ax.c2p(i*dt_, bm[i]) for i in range(n)]
        bm_curve = VMobject(color=ORANGE, stroke_width=2).set_points_as_corners(bm_points)
        lbl_bm = Text("B(t) — Brownian motion", color=ORANGE, font_size=22)\
                     .next_to(lbl_s, DOWN)
        cross = Cross(tangent, color=RED, stroke_width=4)

        self.play(
            ReplacementTransform(smooth, bm_curve),
            ReplacementTransform(lbl_s, lbl_bm),
            FadeOut(tangent)
        )
        self.play(Create(cross)); self.wait(1)

        # Title card
        title_group = VGroup(
            Text("QUANTIFAYA", color=PURPLE, font_size=52, weight=BOLD),
            Text("Episode 2", color=FG, font_size=28),
            Text("Itô's Lemma — What It Actually Means",
                 color=GOLD, font_size=34),
            Text("Stochastic Calculus  |  GBM  |  The Engine of Black-Scholes",
                 color=FG, font_size=22),
        ).arrange(DOWN, buff=0.35).center()
        self.play(FadeOut(ax), FadeOut(bm_curve), FadeOut(lbl_bm),
                  FadeOut(cross), FadeIn(title_group))
        self.wait(3)


# ═══════════════════════════════════════════════════════════════════════════
# SCENE 2 — BROWNIAN MOTION
# ═══════════════════════════════════════════════════════════════════════════
class SceneBrownianMotion(Scene):
    def construct(self):
        title = Text("Step 0: What Is Brownian Motion?",
                     color=GOLD, font_size=38).to_edge(UP)
        src   = cite("[5] Wiener (1923)  |  [8] Karatzas & Shreve (1991)")
        self.play(FadeIn(title), FadeIn(src))

        axioms = VGroup(
            VGroup(
                MathTex(r"B(0) = 0", color=FG, font_size=34),
                Text("Starts at zero", color=TEAL, font_size=20)
            ).arrange(DOWN, buff=0.1),
            VGroup(
                MathTex(r"B(t)-B(s)\sim\mathcal{N}(0,\,t-s)\quad 0\le s<t",
                        color=FG, font_size=28),
                Text("Normal increments — variance = elapsed time",
                     color=TEAL, font_size=20)
            ).arrange(DOWN, buff=0.1),
            VGroup(
                Text("Independent increments — no memory (the process is a goldfish)",
                     color=FG, font_size=22),
            ),
            VGroup(
                Text("Continuous but NOWHERE DIFFERENTIABLE — zoom in, still rough",
                     color=RED, font_size=22),
            ),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).shift(DOWN*0.3)

        for ax in axioms:
            self.play(FadeIn(ax), run_time=0.7); self.wait(0.7)

        # Key property flash
        self.play(FadeOut(axioms))
        key = VGroup(
            Text("The single most important property:", color=FG, font_size=28),
            MathTex(r"E[(dB)^2] = dt", color=GOLD, font_size=56),
            Text("The square of the random increment is deterministic in expectation.",
                 color=FG, font_size=22),
            Text("Hold onto this. It will become everything.",
                 color=ORANGE, font_size=22, slant=ITALIC),
        ).arrange(DOWN, buff=0.4).center()
        self.play(FadeIn(key)); self.wait(3)

        # Simulate BM paths
        self.play(FadeOut(key), FadeOut(title), FadeOut(src))
        ax = Axes(x_range=[0,5,1], y_range=[-3,3,1],
                  x_length=10, y_length=6, axis_config={"color": FG})
        ax_labels = ax.get_axis_labels(
            Tex("t", color=FG, font_size=24),
            Tex("B(t)", color=FG, font_size=24))
        self.play(Create(ax), Write(ax_labels))

        colors = [BLUE_NORM, ORANGE, GREEN, RED, TEAL]
        for seed, col in enumerate(colors):
            np.random.seed(seed*7+3)
            n = 100; dt_ = 5/n
            path = np.cumsum(np.sqrt(dt_)*np.random.randn(n))
            pts = [ax.c2p(i*dt_, path[i]) for i in range(n)]
            crv = VMobject(color=col, stroke_width=1.5, stroke_opacity=0.8)\
                      .set_points_as_corners(pts)
            self.play(Create(crv), run_time=0.8)

        lbl = Text("5 sample paths — same start, wildly different futures",
                   color=GOLD, font_size=22).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(lbl)); self.wait(3)


# ═══════════════════════════════════════════════════════════════════════════
# SCENE 3 — QUADRATIC VARIATION
# ═══════════════════════════════════════════════════════════════════════════
class SceneQuadraticVariation(Scene):
    def construct(self):
        title = Text("The Moment Classical Calculus Dies",
                     color=RED, font_size=38).to_edge(UP)
        src = cite("[6] Shreve (2004), Thm 3.4.3  |  [7] Øksendal (2003)")
        self.play(FadeIn(title), FadeIn(src))

        # Classical Taylor
        classical = VGroup(
            Text("Classical Taylor expansion:", color=FG, font_size=26),
            MathTex(r"f(x+dx)=f(x)+f'(x)dx+\tfrac{1}{2}f''(x)(dx)^2+\cdots",
                    color=FG, font_size=28),
            Text("(dx)²  →  0.  Discard. No problem. ✓",
                 color=GREEN, font_size=22),
        ).arrange(DOWN, buff=0.3).shift(UP*1.2)
        self.play(FadeIn(classical)); self.wait(1.5)

        # Stochastic Taylor
        stoch = VGroup(
            Text("Stochastic Taylor expansion:", color=FG, font_size=26),
            MathTex(r"f(B+dB)=f(B)+f'(B)dB+\tfrac{1}{2}f''(B)(dB)^2+\cdots",
                    color=FG, font_size=28),
            Text("Can we discard (dB)²?", color=ORANGE, font_size=24,
                 weight=BOLD),
        ).arrange(DOWN, buff=0.3).next_to(classical, DOWN, buff=0.5)
        self.play(FadeIn(stoch)); self.wait(1)

        no = Text("NO.", color=RED, font_size=72, weight=BOLD).center()
        self.play(FadeOut(classical), FadeOut(stoch), FadeIn(no)); self.wait(1)
        self.play(FadeOut(no))

        # Order table
        table = MathTable(
            [["\\text{Term}", "\\text{Classical}", "\\text{Stochastic (BM)}"],
             ["dt",           "O(dt)",            "O(dt)"],
             ["dB",           "O(\\sqrt{dt})",    "O(\\sqrt{dt})"],
             ["(dt)^2",       "O(dt^2)\\to 0\\;✓","O(dt^2)\\to 0\\;✓"],
             ["dt\\cdot dB",  "O(dt^{3/2})\\to 0\\;✓","O(dt^{3/2})\\to 0\\;✓"],
             ["(dB)^2",       "O(dt)\\to 0\\;✓",
              "\\mathbf{O(dt)\\not\\to 0!}\\;{\\color{red}✗}"],
            ],
            include_outer_lines=True,
            line_config={"color": FG, "stroke_width": 0.8},
            element_to_mobject_config={"color": FG, "font_size": 20}
        ).scale(0.65).center()
        self.play(Create(table)); self.wait(2)

        # Highlight last row
        last_row = table.get_rows()[5]
        rect = SurroundingRectangle(last_row, color=ORANGE, buff=0.05, stroke_width=2)
        self.play(Create(rect)); self.wait(1)

        # Multiplication table
        self.play(FadeOut(table), FadeOut(rect))
        mult_title = Text("Itô Multiplication Table",
                          color=GOLD, font_size=32).to_edge(UP)
        mult = MathTable(
            [["\\times", "dt",  "dB"],
             ["dt",      "0",   "0"],
             ["dB",      "0",   "dt"]],
            include_outer_lines=True,
            line_config={"color": FG},
            element_to_mobject_config={"color": FG, "font_size": 32}
        ).scale(0.9).center()
        key_entry = Text("(dB)² = dt  — not an approximation. An equality.",
                         color=GOLD, font_size=26).next_to(mult, DOWN, buff=0.4)
        snark = Text("Yes. The square of a random term is deterministic.\nStochastic calculus is built on this audacity.",
                     color=ORANGE, font_size=22, slant=ITALIC, line_spacing=1.3)\
                    .next_to(key_entry, DOWN, buff=0.3)
        self.play(FadeIn(mult_title), Create(mult))
        self.play(FadeIn(key_entry)); self.play(FadeIn(snark)); self.wait(3)


# ═══════════════════════════════════════════════════════════════════════════
# SCENE 4 — ITÔ'S LEMMA DERIVATION
# ═══════════════════════════════════════════════════════════════════════════
class SceneItoLemma(Scene):
    def construct(self):
        title = Text("Itô's Lemma — The Full Derivation",
                     color=GOLD, font_size=38).to_edge(UP)
        src = cite("[1] Itô (1944)  |  [2] Itô (1951)  |  [6] Shreve (2004)")
        self.play(FadeIn(title), FadeIn(src))

        # Setup
        setup = VGroup(
            Text("Let X(t) be an Itô process:", color=FG, font_size=26),
            MathTex(r"dX = \mu(X,t)\,dt + \sigma(X,t)\,dB",
                    color=FG, font_size=36),
            Text("Goal: find df(X(t), t) for smooth f",
                 color=TEAL, font_size=24),
        ).arrange(DOWN, buff=0.3).shift(UP*1.0)
        self.play(FadeIn(setup)); self.wait(1.5); self.play(FadeOut(setup))

        steps = [
            ("Step 1 — Taylor expand to 2nd order:",
             r"df = \frac{\partial f}{\partial t}dt + \frac{\partial f}{\partial X}dX"
             r" + \frac{1}{2}\frac{\partial^2 f}{\partial X^2}(dX)^2 + \cdots"),
            ("Step 2 — Expand (dX)²:",
             r"(dX)^2 = \mu^2(dt)^2 + 2\mu\sigma\,dt\,dB + \sigma^2(dB)^2"),
            ("Step 3 — Apply Itô table  →  (dt)²=0,  dt·dB=0,  (dB)²=dt:",
             r"(dX)^2 = \sigma^2\,dt\quad\leftarrow\text{ the Itô correction}"),
        ]
        for label, eq in steps:
            grp = VGroup(
                Text(label, color=TEAL, font_size=24),
                MathTex(eq, color=FG, font_size=30),
            ).arrange(DOWN, buff=0.25).center()
            self.play(FadeIn(grp)); self.wait(2); self.play(FadeOut(grp))

        # THE RESULT
        result_label = Text("Itô's Lemma:", color=GOLD, font_size=32).shift(UP*2)
        result_eq = MathTex(
            r"df = \underbrace{\left(\frac{\partial f}{\partial t}"
            r"+\mu\frac{\partial f}{\partial X}"
            r"+\frac{1}{2}\sigma^2\frac{\partial^2 f}{\partial X^2}"
            r"\right)}_{\text{drift of }f}dt"
            r"+\underbrace{\sigma\frac{\partial f}{\partial X}}_{\text{diffusion of }f}dB",
            color=FG, font_size=30).next_to(result_label, DOWN, buff=0.4)
        correction = MathTex(
            r"\underbrace{\frac{1}{2}\sigma^2\frac{\partial^2 f}{\partial X^2}}"
            r"_{\text{ITÔ CORRECTION — does not exist in classical calculus}}",
            color=ORANGE, font_size=26).next_to(result_eq, DOWN, buff=0.4)
        box = SurroundingRectangle(result_eq, color=GOLD, buff=0.25, stroke_width=2)

        self.play(FadeIn(result_label), Write(result_eq))
        self.play(Create(box))
        self.play(FadeIn(correction)); self.wait(1)

        taleb = VGroup(
            Text('"The problem with experts is that they do not know what they do not know."',
                 color=GOLD, font_size=20, slant=ITALIC),
            Text("— N.N. Taleb, The Black Swan [9]", color=FG, font_size=18),
            Text("Itô knew what the experts didn't know they didn't know.",
                 color=ORANGE, font_size=20, slant=ITALIC),
            Text("— Quantifaya", color=FG, font_size=18),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(taleb)); self.wait(3)


# ═══════════════════════════════════════════════════════════════════════════
# SCENE 5 — GEOMETRIC BROWNIAN MOTION
# ═══════════════════════════════════════════════════════════════════════════
class SceneGBM(Scene):
    def construct(self):
        title = Text("Geometric Brownian Motion — Itô's Lemma in Action",
                     color=GOLD, font_size=34).to_edge(UP)
        src = cite("[6] Shreve (2004), Ch.4  |  [10] Hull (2018), Ch.15  |  [13] Protter (2005)")
        self.play(FadeIn(title), FadeIn(src))

        gbm_eq = VGroup(
            MathTex(r"dS = \mu S\,dt + \sigma S\,dB", color=FG, font_size=42),
            Text("The canonical stock price model  (μ = drift, σ = volatility)",
                 color=TEAL, font_size=22),
        ).arrange(DOWN, buff=0.25).shift(UP*1.5)
        self.play(FadeIn(gbm_eq)); self.wait(1)

        # Apply Itô with f = ln S
        step_label = Text("Apply Itô's Lemma with  f(S,t) = ln S:",
                          color=TEAL, font_size=24).shift(UP*0.3)
        partials = VGroup(
            MathTex(r"\frac{\partial f}{\partial t}=0,\quad"
                    r"\frac{\partial f}{\partial S}=\frac{1}{S},\quad"
                    r"\frac{\partial^2 f}{\partial S^2}=-\frac{1}{S^2}",
                    color=FG, font_size=28),
        ).next_to(step_label, DOWN, buff=0.3)
        result = MathTex(
            r"d(\ln S)=\left(\mu-\frac{1}{2}\sigma^2\right)dt+\sigma\,dB",
            color=GOLD, font_size=38).next_to(partials, DOWN, buff=0.4)
        box = SurroundingRectangle(result, color=GOLD, buff=0.2, stroke_width=2)
        self.play(FadeOut(gbm_eq))
        self.play(FadeIn(step_label), FadeIn(partials))
        self.play(Write(result), Create(box)); self.wait(2)

        # Closed form
        closed = VGroup(
            MathTex(r"S(T)=S(0)\exp\!\left(\left(\mu-\tfrac{1}{2}\sigma^2\right)T"
                    r"+\sigma\sqrt{T}\,Z\right),\quad Z\sim\mathcal{N}(0,1)",
                    color=FG, font_size=26),
        ).next_to(result, DOWN, buff=0.4)
        self.play(FadeIn(closed)); self.wait(1)
        self.play(FadeOut(step_label), FadeOut(partials), FadeOut(result),
                  FadeOut(box), FadeOut(closed))

        # Volatility drag
        drag_title = Text("The Volatility Drag — What Itô Is Telling You About Your Returns",
                          color=RED, font_size=28).to_edge(UP).shift(DOWN*0.5)
        drag_data = VGroup(
            MathTex(r"\text{Arithmetic mean: }\mu", color=BLUE_NORM, font_size=32),
            MathTex(r"\text{Geometric mean: }\mu - \tfrac{1}{2}\sigma^2",
                    color=ORANGE, font_size=32),
            MathTex(r"\text{Drag: }\tfrac{1}{2}\sigma^2", color=RED, font_size=32),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        example = VGroup(
            Text("Example:  μ=12%,  σ=25%", color=FG, font_size=24),
            Text("½σ² = 3.125%", color=RED, font_size=24),
            Text("Geometric mean = 8.875%  ← what you ACTUALLY compound",
                 color=ORANGE, font_size=24),
            Text("You surrender 3.1% per year. Every year. Silently.",
                 color=RED, font_size=22, weight=BOLD),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)

        block = VGroup(drag_data, example).arrange(DOWN, buff=0.5).center()
        self.play(FadeIn(drag_title), FadeIn(block)); self.wait(3)


# ═══════════════════════════════════════════════════════════════════════════
# SCENE 6 — ITÔ INTEGRAL
# ═══════════════════════════════════════════════════════════════════════════
class SceneItoIntegral(Scene):
    def construct(self):
        title = Text("The Itô Integral — You Can't Use Riemann Here Either",
                     color=GOLD, font_size=34).to_edge(UP)
        src = cite("[6] Shreve (2004), Ch.3  |  [7] Øksendal (2003), Ch.3")
        self.play(FadeIn(title), FadeIn(src))

        riemann = VGroup(
            Text("Classical Riemann:", color=TEAL, font_size=26),
            MathTex(r"\int_0^T f(t)\,dt = \lim\sum f(t_i^*)(t_i-t_{i-1})",
                    color=FG, font_size=28),
            Text("Evaluate at ANY point in interval. Result identical. ✓",
                 color=GREEN, font_size=20),
        ).arrange(DOWN, buff=0.2).shift(UP*1.5)

        ito_int = VGroup(
            Text("Itô integral:", color=TEAL, font_size=26),
            MathTex(r"\int_0^T H(t)\,dB = \lim\sum H(t_{i-1})(B(t_i)-B(t_{i-1}))",
                    color=FG, font_size=28),
            Text("MUST use LEFT endpoint. H must be non-anticipating (ℱₜ-adapted).",
                 color=ORANGE, font_size=20),
            Text("You decide your position BEFORE seeing the shock. No peeking at the future.",
                 color=RED, font_size=20, slant=ITALIC),
        ).arrange(DOWN, buff=0.2).next_to(riemann, DOWN, buff=0.4)

        self.play(FadeIn(riemann)); self.wait(1)
        self.play(FadeIn(ito_int)); self.wait(2)
        self.play(FadeOut(riemann), FadeOut(ito_int))

        # Itô Isometry
        iso_title = Text("The Itô Isometry — a jewel", color=GOLD, font_size=30).to_edge(UP)
        props = VGroup(
            VGroup(
                MathTex(r"E\!\left[\int_0^T H\,dB\right] = 0",
                        color=FG, font_size=34),
                Text("Zero mean — no free lunch", color=TEAL, font_size=20)
            ).arrange(DOWN, buff=0.15),
            VGroup(
                MathTex(r"E\!\left[\left(\int_0^T H\,dB\right)^{\!2}\right]"
                        r"= E\!\left[\int_0^T H^2\,dt\right]",
                        color=GOLD, font_size=34),
                Text("Variance of stochastic integral = expected integral of H² — the Itô Isometry",
                     color=TEAL, font_size=20)
            ).arrange(DOWN, buff=0.15),
        ).arrange(DOWN, buff=0.5).center()

        snark = Text('"If you're thinking this seems needlessly complicated — you're right.\n'
                     'But the alternative is mispricing derivatives. Your call."',
                     color=ORANGE, font_size=20, slant=ITALIC, line_spacing=1.3)\
                    .to_edge(DOWN, buff=0.4)
        self.play(FadeIn(iso_title), FadeIn(props)); self.play(FadeIn(snark)); self.wait(3)


# ═══════════════════════════════════════════════════════════════════════════
# SCENE 7 — BLACK-SCHOLES DERIVATION
# ═══════════════════════════════════════════════════════════════════════════
class SceneBlackScholes(Scene):
    def construct(self):
        title = Text("Black-Scholes — Itô's Lemma Goes to War",
                     color=GOLD, font_size=36).to_edge(UP)
        src = cite("[3] Black & Scholes (1973), JPE 81(3)  |  [4] Merton (1973), Bell J. Econ. 4(1)")
        self.play(FadeIn(title), FadeIn(src))

        # Apply Itô to V
        dv = MathTex(
            r"dV=\left(\frac{\partial V}{\partial t}+\mu S\frac{\partial V}{\partial S}"
            r"+\frac{1}{2}\sigma^2S^2\frac{\partial^2 V}{\partial S^2}\right)dt"
            r"+\sigma S\frac{\partial V}{\partial S}\,dB",
            color=FG, font_size=24).shift(UP*1.5)
        self.play(Write(dv)); self.wait(1.5)

        # Delta-hedge
        hedge = VGroup(
            MathTex(r"\Pi = V - \Delta S,\quad \Delta=\frac{\partial V}{\partial S}",
                    color=TEAL, font_size=30),
            Text("Long 1 option, short Δ shares — the delta-hedge",
                 color=FG, font_size=22),
        ).arrange(DOWN, buff=0.2).next_to(dv, DOWN, buff=0.4)
        self.play(FadeIn(hedge)); self.wait(1)

        # Cancellation
        self.play(FadeOut(dv), FadeOut(hedge))
        cancel_text = Text("Compute dΠ = dV − Δ·dS   →   the dB terms cancel exactly:",
                           color=TEAL, font_size=24).shift(UP*2)
        before = MathTex(
            r"dB\text{ terms: }\sigma S\frac{\partial V}{\partial S}dB"
            r"-\frac{\partial V}{\partial S}\sigma S\,dB = 0",
            color=ORANGE, font_size=30)
        after = VGroup(
            MathTex(r"d\Pi=\left(\frac{\partial V}{\partial t}"
                    r"+\frac{1}{2}\sigma^2S^2\frac{\partial^2 V}{\partial S^2}\right)dt",
                    color=GREEN, font_size=30),
            Text("Randomness: gone.  Drift μ: gone.  Portfolio: riskless.",
                 color=GREEN, font_size=22, weight=BOLD),
        ).arrange(DOWN, buff=0.2)
        cross = Cross(before, color=RED, stroke_width=4)

        self.play(FadeIn(cancel_text), FadeIn(before))
        self.play(Create(cross)); self.wait(1)
        self.play(FadeOut(before), FadeOut(cross), FadeIn(after)); self.wait(1.5)
        self.play(FadeOut(cancel_text), FadeOut(after))

        # Black-Scholes PDE
        pde_label = Text("No-arbitrage  →  riskless portfolio earns r  →  Black-Scholes PDE:",
                         color=TEAL, font_size=24).shift(UP*2.5)
        pde = MathTex(
            r"\frac{\partial V}{\partial t}"
            r"+rS\frac{\partial V}{\partial S}"
            r"+\frac{1}{2}\sigma^2S^2\frac{\partial^2 V}{\partial S^2}"
            r"-rV=0",
            color=GOLD, font_size=44)
        pde_box = SurroundingRectangle(pde, color=PURPLE, buff=0.3, stroke_width=3)
        self.play(FadeIn(pde_label), Write(pde), Create(pde_box))
        self.wait(2)

        # BS Formula
        self.play(FadeOut(pde_label))
        bs_label = Text("Analytical solution (European call):", color=TEAL, font_size=24)\
                       .next_to(pde_box, DOWN, buff=0.4)
        bs = MathTex(
            r"C=SN(d_1)-Ke^{-r(T-t)}N(d_2)",
            color=FG, font_size=32).next_to(bs_label, DOWN, buff=0.2)
        d1d2 = MathTex(
            r"d_1=\frac{\ln(S/K)+(r+\frac{1}{2}\sigma^2)(T-t)}{\sigma\sqrt{T-t}}"
            r",\quad d_2=d_1-\sigma\sqrt{T-t}",
            color=FG, font_size=24).next_to(bs, DOWN, buff=0.2)
        ito_note = Text("Note ½σ² in d₁ — Itô's correction, living inside every option price on earth.",
                        color=ORANGE, font_size=20, slant=ITALIC).next_to(d1d2, DOWN, buff=0.2)
        self.play(FadeIn(bs_label), FadeIn(bs), FadeIn(d1d2), FadeIn(ito_note)); self.wait(3)


# ═══════════════════════════════════════════════════════════════════════════
# SCENE 8 — ITÔ VS STRATONOVICH
# ═══════════════════════════════════════════════════════════════════════════
class SceneItoVsStrat(Scene):
    def construct(self):
        title = Text("The Convention War Nobody Tells You About",
                     color=GOLD, font_size=36).to_edge(UP)
        src = cite("[7] Øksendal (2003)  |  [11] Wilmott (2006), Vol.1")
        self.play(FadeIn(title), FadeIn(src))

        two_integrals = VGroup(
            VGroup(
                Text("Itô:", color=BLUE_NORM, font_size=26, weight=BOLD),
                MathTex(r"\int_0^T H\,dB=\lim\sum H(t_{i-1})\Delta B_i",
                        color=FG, font_size=26),
                Text("Left endpoint — causal", color=BLUE_NORM, font_size=20),
            ).arrange(DOWN, buff=0.2),
            VGroup(
                Text("Stratonovich:", color=ORANGE, font_size=26, weight=BOLD),
                MathTex(r"\int_0^T H\circ dB=\lim\sum H\!\left(\tfrac{t_i+t_{i-1}}{2}\right)\Delta B_i",
                        color=FG, font_size=26),
                Text("Midpoint — needs partial future info", color=ORANGE, font_size=20),
            ).arrange(DOWN, buff=0.2),
        ).arrange(RIGHT, buff=1.0).shift(UP*0.5)
        self.play(FadeIn(two_integrals)); self.wait(1.5)

        verdict = VGroup(
            Text("Stratonovich satisfies the classical chain rule → physicists love it.",
                 color=ORANGE, font_size=22),
            Text("Itô requires the correction term → finance requires Itô.",
                 color=BLUE_NORM, font_size=22),
            Text("Using Stratonovich in finance = using tomorrow's prices today = insider trading.",
                 color=RED, font_size=22, weight=BOLD),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(two_integrals, DOWN, buff=0.5)
        self.play(FadeIn(verdict)); self.wait(2)

        wilmott = VGroup(
            Text('"The Itô correction is not an error. It is the price of randomness."',
                 color=GOLD, font_size=24, slant=ITALIC),
            Text("— P. Wilmott, Paul Wilmott on Quantitative Finance [11]",
                 color=FG, font_size=20),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(wilmott)); self.wait(3)


# ═══════════════════════════════════════════════════════════════════════════
# SCENE 9 — LESSONS / AXELROD TAKEAWAYS
# ═══════════════════════════════════════════════════════════════════════════
class SceneLessons(Scene):
    def construct(self):
        title = Text("What This Actually Means For You",
                     color=GOLD, font_size=38).to_edge(UP)
        sub   = Text("— the version your textbook was too polite to say",
                     color=FG, font_size=22, slant=ITALIC).next_to(title, DOWN, buff=0.1)
        self.play(FadeIn(title), FadeIn(sub))

        truths = [
            (RED,   "Ⅰ",
             "Every time you ignore the Itô correction,\nyou are systematically mispricing convexity.",
             "Not occasionally. Systematically."),
            (GOLD,  "Ⅱ",
             "Compound returns ≠ expected returns.\nμ − ½σ² is what you actually earn.",
             "You're giving up ½σ² per year. Every year. To volatility."),
            (TEAL,  "Ⅲ",
             "Itô is why delta-hedging works.\nWithout it there is no Black-Scholes.\nWithout Black-Scholes the $600T market has no foundation.",
             "[3][4]"),
            (PURPLE,"Ⅳ",
             "Every quant interview will ask you to derive this.\nNot the formula. The derivation.\nThe correction term is the differentiator.",
             "Can you explain why (dB)² = dt?  Then you're in the top 5%."),
        ]
        for col, num, main, sub_ in truths:
            grp = VGroup(
                Text(f"{num}  ", color=col, font_size=32, weight=BOLD),
                VGroup(
                    Text(main, color=FG, font_size=22, line_spacing=1.3),
                    Text(sub_, color=col, font_size=18, slant=ITALIC),
                ).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
            ).arrange(RIGHT, buff=0.3).center()
            self.play(FadeIn(grp)); self.wait(2.5); self.play(FadeOut(grp))

        # Taleb final
        taleb = VGroup(
            Text('"Anything that has been around for a long time\nhas proven its antifragility."',
                 color=GOLD, font_size=30, slant=ITALIC, line_spacing=1.4),
            Text("— N.N. Taleb, Antifragile [9]", color=FG, font_size=22),
            Text("Itô's Lemma: 1944 → present.\nStill running every derivatives desk on earth.",
                 color=ORANGE, font_size=26, line_spacing=1.3),
            Text("Learn it. Own it.", color=PURPLE, font_size=36, weight=BOLD),
        ).arrange(DOWN, buff=0.4).center()
        self.play(FadeIn(taleb)); self.wait(4)

        # Rolling citation credits
        self.play(FadeOut(taleb), FadeOut(title), FadeOut(sub))
        refs = [
            "[1] Itô, K. (1944). Stochastic integral. Proc. Imperial Academy Tokyo, 20(8), 519–524.",
            "[2] Itô, K. (1951). On a formula concerning stochastic differentials. Nagoya Math. J., 3, 55–65.",
            "[3] Black, F. & Scholes, M. (1973). The pricing of options. J. Political Economy, 81(3), 637–654.",
            "[4] Merton, R.C. (1973). Theory of rational option pricing. Bell J. Economics, 4(1), 141–183.",
            "[5] Wiener, N. (1923). Differential space. J. Mathematics and Physics, 2, 131–174.",
            "[6] Shreve, S.E. (2004). Stochastic Calculus for Finance II. Springer.",
            "[7] Øksendal, B. (2003). Stochastic Differential Equations, 6th ed. Springer.",
            "[8] Karatzas, I. & Shreve, S.E. (1991). Brownian Motion and Stochastic Calculus. Springer.",
            "[9] Taleb, N.N. (2007). The Black Swan. Random House.  |  (2012). Antifragile. Random House.",
            "[10] Hull, J.C. (2018). Options, Futures, and Other Derivatives, 10th ed. Pearson.",
            "[11] Wilmott, P. (2006). Paul Wilmott on Quantitative Finance, 2nd ed. Wiley.",
            "[12] Mandelbrot, B. & Hudson, R. (2004). The Misbehaviour of Markets. Basic Books.",
            "[13] Protter, P. (2005). Stochastic Integration and Differential Equations. Springer.",
        ]
        ref_label = Text("References", color=GOLD, font_size=28).to_edge(UP)
        self.play(FadeIn(ref_label))
        ref_group = VGroup(*[Text(r, color=TEAL, font_size=16) for r in refs])\
                        .arrange(DOWN, buff=0.18, aligned_edge=LEFT)\
                        .center()
        self.play(FadeIn(ref_group)); self.wait(5)


# ═══════════════════════════════════════════════════════════════════════════
# SCENE 10 — OUTRO
# ═══════════════════════════════════════════════════════════════════════════
class SceneOutro(Scene):
    def construct(self):
        logo = Text("QUANTIFAYA", color=PURPLE, font_size=64, weight=BOLD)
        tagline = Text("Financial Engineering. Explained Rigorously. Applied Practically.",
                       color=GOLD, font_size=22).next_to(logo, DOWN, buff=0.3)
        self.play(FadeIn(logo), FadeIn(tagline)); self.wait(1)

        recap = VGroup(
            Text("✓  Brownian motion axioms & nowhere-differentiable paths", color=GREEN, font_size=20),
            Text("✓  Quadratic variation: why (dB)² = dt", color=GREEN, font_size=20),
            Text("✓  Itô's Lemma: full Taylor-expansion derivation", color=GREEN, font_size=20),
            Text("✓  GBM: log-return distribution & volatility drag", color=GREEN, font_size=20),
            Text("✓  Itô integral: non-anticipating, Itô Isometry", color=GREEN, font_size=20),
            Text("✓  Black-Scholes PDE: derived from Itô + no-arbitrage", color=GREEN, font_size=20),
            Text("✓  Itô vs. Stratonovich: why finance demands Itô's convention", color=GREEN, font_size=20),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).center()
        self.play(FadeOut(logo), FadeOut(tagline))
        self.play(LaggedStart(*[FadeIn(r) for r in recap], lag_ratio=0.15))
        self.wait(2)

        challenge = VGroup(
            Text("Comment Challenge:", color=GOLD, font_size=28, weight=BOLD),
            MathTex(r"\text{Using Itô's Lemma, derive }d(S^2)\text{ if }dS=\mu S\,dt+\sigma S\,dB",
                    color=FG, font_size=26),
            Text("First correct full derivation gets pinned.", color=TEAL, font_size=22),
            Text("Answer includes the Itô correction. Good luck.", color=ORANGE, font_size=20, slant=ITALIC),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeOut(recap), FadeIn(challenge)); self.wait(2)

        next_ep = VGroup(
            Text("Next on Quantifaya:", color=GOLD, font_size=30, weight=BOLD),
            Text("The Greeks: Delta, Gamma, Vega — Built From First Principles",
                 color=ORANGE, font_size=26),
            Text("Why Gamma exposure is the most dangerous thing a desk can run.",
                 color=FG, font_size=22),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeOut(challenge), FadeIn(next_ep)); self.wait(3)


# ═══════════════════════════════════════════════════════════════════════════
# FULL EPISODE COMPOSITOR
# ═══════════════════════════════════════════════════════════════════════════
class FullEpisode(Scene):
    """
    Chains all scenes into one render.

    Render commands:
    Full 1080p60:
        manim -pqh quantifaya_ep2.py FullEpisode --fps 60 --resolution 1920x1080
    Quick 480p preview:
        manim -pql quantifaya_ep2.py FullEpisode
    Single scene test:
        manim -pql quantifaya_ep2.py SceneItoLemma
    """
    def construct(self):
        for SceneClass in [
            SceneIntro,
            SceneBrownianMotion,
            SceneQuadraticVariation,
            SceneItoLemma,
            SceneGBM,
            SceneItoIntegral,
            SceneBlackScholes,
            SceneItoVsStrat,
            SceneLessons,
            SceneOutro,
        ]:
            instance = SceneClass()
            instance.camera = self.camera
            instance.renderer = self.renderer
            instance.construct()
            self.wait(0.5)
```

---

## APPENDIX C — TIMING GUIDE

| # | Scene Class | Target | Notes |
|---|---|---|---|
| 1 | SceneIntro | 1:45 | Hook must land hard — don't rush the $600T reveal |
| 2 | SceneBrownianMotion | 3:30 | Pause on (dB)²=dt — repeat it twice |
| 3 | SceneQuadraticVariation | 3:30 | Let the multiplication table breathe |
| 4 | SceneItoLemma | 5:00 | Longest scene — step-by-step, no rushing |
| 5 | SceneGBM | 3:30 | Volatility drag example — say the numbers slowly |
| 6 | SceneItoIntegral | 2:30 | Insider trading analogy lands well — pause after it |
| 7 | SceneBlackScholes | 4:00 | Cancellation animation is the visual climax — hold it |
| 8 | SceneItoVsStrat | 2:00 | Fast-paced — convention war is supporting, not main |
| 9 | SceneLessons | 2:00 | Taleb quote — slow down here |
| 10 | SceneOutro | 1:00 | Challenge question — speak it clearly |
| **TOTAL** | | **~29:15** | Trim pauses on Scenes 3 and 8 to hit 25 min |

---

## APPENDIX D — YOUTUBE UPLOAD CHECKLIST

```
TITLE:
Itô's Lemma Explained | Geometric Brownian Motion & Black-Scholes Derived | Quantifaya Ep.2

DESCRIPTION (first 200 chars):
Kiyosi Itô wrote 4 pages in 1944 that underpin a $600T derivatives market.
Today we derive Itô's Lemma from scratch — and use it to derive Black-Scholes live.

CHAPTERS:
00:00 — The $600 Trillion Four Pages (Hook)
01:45 — Brownian Motion: Axioms, Properties, (dB)²=dt
05:15 — Quadratic Variation: Why Classical Calculus Fails
08:45 — Itô's Lemma: The Full Derivation Step-by-Step
13:45 — Geometric Brownian Motion & The Volatility Drag
17:15 — The Itô Integral and the Itô Isometry
19:45 — Black-Scholes Derived From Itô's Lemma Live
23:45 — Itô vs. Stratonovich: The Convention War
25:45 — Takeaways, Taleb, References
27:45 — Next Episode: The Greeks

TAGS:
ito lemma explained, stochastic calculus finance, geometric brownian motion,
black scholes derivation ito lemma, quadratic variation brownian motion,
ito integral finance, wiener process, SDE finance, quant finance math,
financial engineering, derivatives pricing, volatility drag,
stochastic differential equations, quant interview, worldquant university,
nassim taleb finance, kiyosi ito mathematician, ito vs stratonovich,
financial mathematics explained

THUMBNAIL BRIEF:
Split screen: Left = clean Newton calculus graph (blue, smooth)
Right = jagged Brownian motion path (orange, violent)
Bold text overlay: "Your Calculus Is Wrong"
Sub-text: "Itô Fixed It in 4 Pages"
Quantifaya logo bottom-right.

PINNED COMMENT:
📌 References for this episode:
[1] Itô (1944) — Proc. Imperial Academy Tokyo
[3] Black & Scholes (1973) — J. Political Economy
[6] Shreve (2004) — Stochastic Calculus for Finance II (Springer)
[9] Taleb (2007) — The Black Swan | (2012) — Antifragile
Full list in the video at 27:45.

🎯 Challenge: Derive d(S²) using Itô's Lemma. First correct answer gets pinned!
```
