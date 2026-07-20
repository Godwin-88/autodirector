# QUANTIFAYA — EPISODE 3
## "Black-Scholes Derived From Scratch — The Most Famous Equation in Finance"

**Channel:** Quantifaya
**Target Duration:** 25 minutes
**Production Stack:** Python Manim (Community Edition v0.18+) + TTS Voice-Over
**Persona:** Taylor-meets-Axe-Capital. Taleb-level intellectual ruthlessness. Zero tolerance for hand-waving.
**Tone:** Confident, surgical, occasionally lethal. Every assumption gets interrogated. Every term gets named.

---

**SEO Title:** Black-Scholes Formula DERIVED From Scratch | Every Step Explained | Quantifaya Ep.3
**SEO Description:** The Black-Scholes formula won a Nobel Prize, underpins a $600 trillion derivatives market, and is taught in every finance program on earth — usually without derivation. Today we fix that. Full PDE derivation using Itô's Lemma, heat equation transformation, risk-neutral pricing, and a brutally honest breakdown of every assumption and where it breaks. If you're a quant, a trader, or just someone who wants to understand what everyone else is pretending to understand — this is the video.
**SEO Tags:** black scholes formula derivation, black scholes explained, options pricing math, black scholes PDE, heat equation options, risk neutral pricing, ito lemma black scholes, put call parity, implied volatility, delta hedging, quant finance, financial engineering, derivatives pricing, Nobel Prize finance, options trading math, d1 d2 explained

---

## VERIFIED ACADEMIC SOURCES

| # | Citation | Scene |
|---|---|---|
| [1] | Black, F. & Scholes, M. (1973). *The pricing of options and corporate liabilities.* J. Political Economy, 81(3), 637–654. | 1, 4, 6, 7 |
| [2] | Merton, R.C. (1973). *Theory of rational option pricing.* Bell J. Economics, 4(1), 141–183. | 1, 7 |
| [3] | Itô, K. (1944). *Stochastic integral.* Proc. Imperial Academy Tokyo, 20(8), 519–524. | 4 |
| [4] | Samuelson, P.A. (1965). *Rational theory of warrant pricing.* Industrial Mgmt Review, 6(2), 13–32. | 2 |
| [5] | Bachelier, L. (1900). *Théorie de la spéculation.* Ann. Sci. École Normale Sup., 17, 21–86. | 2 |
| [6] | Shreve, S.E. (2004). *Stochastic Calculus for Finance II.* Springer. | 4, 5, 7 |
| [7] | Hull, J.C. (2018). *Options, Futures, and Other Derivatives*, 10th ed. Pearson. | 2, 6 |
| [8] | Wilmott, P. (2006). *Paul Wilmott on Quantitative Finance*, 2nd ed. Wiley. | 3, 8 |
| [9] | Taleb, N.N. (1997). *Dynamic Hedging.* Wiley. | 3, 9 |
| [10] | Taleb, N.N. (2007). *The Black Swan.* Random House. | 8, 9 |
| [11] | Cox, J.C. & Ross, S.A. (1976). *Valuation of options for alternative stochastic processes.* J. Financial Economics, 3(1–2), 145–166. | 7 |
| [12] | Harrison, J.M. & Kreps, D.M. (1979). *Martingales and arbitrage in multiperiod securities markets.* J. Economic Theory, 20(3), 381–408. | 7 |
| [13] | Harrison, J.M. & Pliska, S.R. (1981). *Martingales and stochastic integrals in the theory of continuous trading.* Stochastic Processes & Applications, 11(3), 215–260. | 7 |
| [14] | Karatzas, I. & Shreve, S.E. (1991). *Brownian Motion and Stochastic Calculus*, 2nd ed. Springer. | 5 |
| [15] | Derman, E. & Kani, I. (1994). *Riding on a smile.* Risk Magazine, 7(2), 32–39. | 8 |
| [16] | Nobel Committee (1997). *Scientific Background: Derivatives and Hedging.* Royal Swedish Academy of Sciences. | 1 |

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
manim -pqh quantifaya_ep3.py FullEpisode --fps 60 --resolution 1920x1080
manim -pql quantifaya_ep3.py SceneIntro   # single scene test
```

---

---

## SCENE 1: COLD OPEN — THE NOBEL PRIZE HOOK
**Class:** `SceneIntro` | **Duration:** ~1:30

### MANIM ANIMATION SEQUENCE

```
1. Black screen. Two names fade in — one by one, large:
   "Fischer Black"     (white)
   "Myron Scholes"     (white)
   "Robert Merton"     (white)

2. Gold text below:
   "1997 Nobel Prize in Economics."

3. Beat. Then — a red X appears over "Fischer Black."
   Text beneath: "Died: August 30, 1995."
   Small text: "Nobel Prizes are not awarded posthumously."

4. Source citation fades in bottom-right:
   "[16] Nobel Committee (1997), Royal Swedish Academy of Sciences"

5. The formula appears — written in blood red, large, centred:
   C = SN(d₁) − Ke^{−rT}N(d₂)

6. Text: "The most famous equation in finance.
          Taught in every program. Understood by almost none.
          Derived by almost fewer."

7. Slow zoom into the formula. Each term pulses once.

8. Cut to black. Then white text:
   "Today we derive it. All of it. From first principles.
    No hand-waving. No 'it can be shown.'
    We show."

9. QUANTIFAYA logo + episode title:
   Episode 3: "Black-Scholes — Derived From Scratch"
   Subtitle: "PDE → Heat Equation → Formula → Nobel Prize"
```

### VOICE-OVER SCRIPT

"1997. The Nobel Committee in Stockholm awarded the Prize in Economics to Myron Scholes and Robert Merton — for a pricing formula that had already been running the derivatives markets for twenty-four years.

Fischer Black, the third architect of the model, was not there. He had died two years earlier. The Nobel Prize is not awarded posthumously. [16]

[PAUSE — red X animation]

The most famous equation in quantitative finance has a body count. And a Nobel Prize. And approximately six hundred trillion dollars of notional derivatives outstanding that price off of it every single day.

[PAUSE — formula appears in red]

This is it. The Black-Scholes formula for a European call option. [1] Every quant knows it. Most people in finance can recite it. Very few can derive it from first principles. Almost none can explain why every single term is there.

After this video, you'll be in that last category.

[PAUSE — cut to black]

No hand-waving. No 'it can be shown.' We show.

Welcome to Episode Three of Quantifaya. Let's go."

---

## SCENE 2: THE PROBLEM — WHAT ARE WE ACTUALLY PRICING?
**Class:** `SceneProblemSetup` | **Duration:** ~2:30

### MANIM ANIMATION SEQUENCE

```
1. Title: "Step 0: What Are We Trying to Price?"

2. European Call Option — payoff diagram:
   Axes: x = S_T (stock price at expiry), y = Payoff
   
   Flat line at y=0 for S_T < K
   Line rising at 45° for S_T > K
   
   Label the kink: "K = Strike price"
   Formula: max(S_T − K, 0)
   
   "If the stock finishes above K, you profit. Below K, you get nothing.
    Simple terminal payoff. Hard present-day price."

3. European Put — same axes, mirror:
   max(K − S_T, 0)
   
   Falling line for S_T < K, flat at 0 for S_T > K.

4. The fundamental problem — animated question:
   
   "Today is t=0. Expiry is T.
    S_T is unknown — it hasn't happened yet.
    S_T could be anything from 0 to ∞.
    
    What should you pay for this contract TODAY?"

5. Timeline appears:
   
   t=0 ──────────────────────── t=T
   "Pay C"                    "Receive max(S_T−K,0)"
   "We know S₀, K, r, σ"     "We don't know S_T"

6. Historical context — two names appear:
   
   "Louis Bachelier, 1900 [5] — first mathematical option pricing model.
    Used Arithmetic Brownian Motion. Allowed negative prices. Heroic attempt."
   
   "Paul Samuelson, 1965 [4] — used Geometric Brownian Motion.
    Got the dynamics right. Still couldn't close-form the price."
   
   "Black, Scholes, Merton, 1973 [1][2] — closed-form solution.
    Nobel Prize. Permanent fixture of civilization."

7. Source tags: "[5] Bachelier (1900) | [4] Samuelson (1965) | [7] Hull (2018)"
```

### VOICE-OVER SCRIPT

"Before we derive anything, let's be precise about what we're pricing.

[PAUSE — show call payoff]

A European call option is a contract that gives the buyer the right — but not the obligation — to purchase a stock at a fixed price K, called the strike, at a fixed future date T, called the expiry. [7] The payoff at expiry is max of S_T minus K, zero. If the stock finishes above the strike, you exercise and pocket the difference. If it finishes below, you walk away.

[PAUSE — show put]

The put is the mirror image. The right to sell at K. Payoff is max of K minus S_T, zero.

[PAUSE — fundamental problem]

Both of these are trivially easy to understand at expiry. The problem is pricing them *today*. S_T is unknown. It's a random variable. The stock could finish at any positive value. You need to commit to a price — right now — for a payoff that depends on something that hasn't happened yet.

[PAUSE — timeline]

Today you know: the current stock price S₀. The strike K. The risk-free interest rate r. The volatility sigma. You don't know where the stock will be at T. That's the game.

[PAUSE — historical context]

People tried to solve this problem long before Black and Scholes. Louis Bachelier in 1900 — in his PhD thesis, which his committee graded 'honorable' rather than 'très honorable,' a slight he never recovered from — wrote the first mathematical model of option pricing. [5] He used Arithmetic Brownian Motion, which allows negative stock prices. Not ideal, but a century ahead of its time.

Paul Samuelson improved it in 1965 with Geometric Brownian Motion, which keeps prices positive. [4] Better dynamics. Still no clean closed-form price.

Then in 1973, Black, Scholes, and Merton closed the problem. [1][2] Permanently. With a formula anyone can compute on a pocket calculator. Here's how they did it."

---

## SCENE 3: THE FOUR ASSUMPTIONS — THE PRICE OF TRACTABILITY
**Class:** `SceneAssumptions` | **Duration:** ~3:00

### MANIM ANIMATION SEQUENCE

```
1. Title: "The Four Assumptions — What Black-Scholes Requires You to Believe"
   Subtitle in gold italic: "Every model is wrong. Some are useful. This one won a Nobel."

2. ASSUMPTION 1 — Stock follows GBM:
   dS = μS dt + σS dB
   
   Visual: GBM fan of paths (from Ep.2)
   
   "What it means: log-returns are i.i.d. Normal. Volatility is constant.
    What it costs: fat tails (Ep.1), vol clustering, jumps — all ignored.
    What Taleb says: 'Those who gave us the Normal distribution as a
    description of market randomness... have a lot to answer for.' [10]"

3. ASSUMPTION 2 — Constant volatility σ and risk-free rate r:
   
   Visual: flat horizontal line σ = const vs real vol smile (curved, smirking)
   
   "What it means: vol is a fixed number. Same for all strikes. All maturities.
    What it costs: the entire implied volatility surface.
    What happened: the 1987 crash. After Black Monday, vol smiles appeared
    and never left. BS has been 'wrong' about vol since 1987 — and is still
    the benchmark. Figure that out."

4. ASSUMPTION 3 — Continuous trading, no transaction costs:
   
   Visual: continuous delta-hedge rebalancing animation — 
   a portfolio value tracking option price perfectly in continuous time.
   
   "What it means: you can trade infinitely often, for free.
    What it costs: in practice, you rebalance discretely. You pay bid-ask.
    You pay slippage. The hedge bleeds transaction costs constantly.
    Taleb called this 'the dynamic hedging trap.' [9]"

5. ASSUMPTION 4 — No dividends, European exercise only:
   
   "European means you can only exercise at expiry — not before.
    American options allow early exercise. BS doesn't price them.
    No dividends means no leakage from holding the stock. 
    Both are fixable extensions. But not today."

6. Summary scoreboard:
   ┌────────────────────────────┬──────────────┬──────────────────────────┐
   │ Assumption                 │ Tractability │ Real-World Cost          │
   ├────────────────────────────┼──────────────┼──────────────────────────┤
   │ GBM stock dynamics         │ ★★★★★        │ Fat tails, no jumps      │
   │ Constant σ and r           │ ★★★★★        │ Vol smile, term structure │
   │ Continuous, free trading   │ ★★★★★        │ Hedging costs bleed P&L  │
   │ No dividends, European     │ ★★★          │ Fixable extensions exist  │
   └────────────────────────────┴──────────────┴──────────────────────────┘

7. Wilmott quote in gold:
   "All models are wrong. The question is whether they are wrong
    in a useful way."
   — P. Wilmott [8]
```

### VOICE-OVER SCRIPT

"Every model is a lie. The question is whether it's a productive one. Black-Scholes makes four assumptions that are all, to varying degrees, empirically false. And it's still the benchmark every options desk on earth prices off of. Let's understand why.

[PAUSE — Assumption 1]

First assumption: stock prices follow Geometric Brownian Motion. We covered this in Episode 2. Log-returns are independent and identically Normally distributed. Volatility is constant in time. [1]

What does this cost? Everything we covered in Episode 1. Fat tails — gone. Volatility clustering — gone. Jumps — gone. Nassim Taleb put it bluntly: 'Those who gave us the Normal distribution as a description of market randomness have a lot to answer for.' [10] He's right. And yet.

[PAUSE — Assumption 2]

Second assumption: volatility sigma and the risk-free rate r are constant. This is perhaps the most operationally important lie in all of quantitative finance.

[PAUSE — show vol smile]

Look at this. This is what the market *implies* about volatility across strikes and maturities — the implied vol surface. It's curved. It smirks. It has a term structure. It is emphatically not a flat constant. The Black-Scholes model has been wrong about volatility since October 19th, 1987 — Black Monday — when the crash permanently bent the smile into existence. It has never unsmiled since. And BS is still the benchmark. Make of that what you will.

[PAUSE — Assumption 3]

Third assumption: you can trade continuously, for free, in any size. This allows the delta hedge to be maintained perfectly, moment to moment, eliminating all risk from the portfolio. [1]

In practice: you rebalance daily, or hourly. You pay bid-ask spreads. You pay market impact. The hedging errors accumulate. Taleb, who spent years on derivatives desks, called this the dynamic hedging trap — the theoretical perfection of continuous hedging dissolves the moment real friction enters the system. [9]

[PAUSE — Assumption 4]

Fourth: no dividends, and the option is European. Both are fixable. Dividends can be incorporated via a continuous yield adjustment. American options require numerical methods — PDE or binomial trees. Extensions exist and are well-understood. They're just not today's problem.

[PAUSE — scoreboard]

So: four assumptions, all wrong, model still dominant. That's the power of a closed-form solution. People will tolerate a wrong model if it gives them a number they can act on and hedge with. Black-Scholes gives you that. Which is exactly why we're deriving it today."

---

## SCENE 4: THE PDE DERIVATION — ITÔ PLUS NO-ARBITRAGE
**Class:** `ScenePDE` | **Duration:** ~4:00

### MANIM ANIMATION SEQUENCE

```
1. Title: "The Derivation — Itô's Lemma + No-Arbitrage = Black-Scholes PDE"
   Sources: "[1] Black & Scholes (1973) | [3] Itô (1944) | [6] Shreve (2004)"

2. SETUP — write on screen, each line animating in:

   Stock:  dS = μS dt + σS dB           (GBM)
   Option: V = V(S, t)                   (unknown function we want)
   Goal:   Find V(S, t) explicitly.

3. STEP 1 — Apply Itô's Lemma to V(S,t):
   
   Reference flash: "From Episode 2 — Itô's Lemma:"
   MathTex:
   dV = \frac{\partial V}{\partial t}dt
      + \frac{\partial V}{\partial S}dS
      + \frac{1}{2}\frac{\partial^2 V}{\partial S^2}(dS)^2
   
   Substitute dS = μS dt + σS dB and (dS)² = σ²S²dt:
   
   dV = \!\left(\frac{\partial V}{\partial t}
        + \mu S\frac{\partial V}{\partial S}
        + \frac{1}{2}\sigma^2 S^2\frac{\partial^2 V}{\partial S^2}\right)dt
        + \sigma S\frac{\partial V}{\partial S}\,dB

4. STEP 2 — Construct the Delta-Hedge Portfolio:
   
   \Pi = V - \Delta \cdot S
   
   where \Delta = \frac{\partial V}{\partial S}
   
   Visual: 
   Left column: "LONG 1 option  +V"  (green)
   Right column: "SHORT Δ shares  −ΔS"  (red)
   
   Arrow to: "Net portfolio Π — value known, hedge chosen"

5. STEP 3 — Compute dΠ:
   
   d\Pi = dV - \Delta\,dS
        = dV - \frac{\partial V}{\partial S}(μS\,dt + σS\,dB)

   Expand and substitute dV:
   
   d\Pi = \!\left(\frac{\partial V}{\partial t}
          + \mu S\frac{\partial V}{\partial S}
          + \frac{1}{2}\sigma^2 S^2\frac{\partial^2 V}{\partial S^2}\right)dt
          + \sigma S\frac{\partial V}{\partial S}\,dB
          - \frac{\partial V}{\partial S}\mu S\,dt
          - \frac{\partial V}{\partial S}\sigma S\,dB

6. STEP 4 — THE CANCELLATION (visual climax):
   
   Highlight in orange: "+σS(∂V/∂S)dB"
   Highlight in red:    "−σS(∂V/∂S)dB"
   
   ANIMATION: Both terms flash, then EXPLODE off screen with a satisfying pop.
   Sparks. Then silence.
   
   ALSO highlight: "+μS(∂V/∂S)dt" and "−μS(∂V/∂S)dt" → same treatment.
   
   d\Pi = \!\left(\frac{\partial V}{\partial t}
          + \frac{1}{2}\sigma^2 S^2\frac{\partial^2 V}{\partial S^2}\right)dt
   
   Gold box around this result:
   "The portfolio is RISKLESS. No dB. No μ.
    Randomness: eliminated. Expected return: irrelevant."

7. STEP 5 — No-Arbitrage Condition:
   
   "A riskless portfolio must earn exactly the risk-free rate r.
    If it earned more: borrow at r, invest in Π — free money.
    If it earned less: short Π, lend at r — free money.
    Neither persists. Therefore:"
   
   d\Pi = r\Pi\,dt = r(V - \Delta S)\,dt = r\!\left(V - S\frac{\partial V}{\partial S}\right)dt

8. STEP 6 — Set equal and rearrange:
   
   \frac{\partial V}{\partial t}
   + \frac{1}{2}\sigma^2 S^2\frac{\partial^2 V}{\partial S^2}
   = r\!\left(V - S\frac{\partial V}{\partial S}\right)

9. THE BLACK-SCHOLES PDE — box pulses purple, hold 4 seconds:
   
   ┌──────────────────────────────────────────────────────────────┐
   │                                                              │
   │   ∂V/∂t  +  rS·∂V/∂S  +  ½σ²S²·∂²V/∂S²  −  rV  =  0     │
   │                                                              │
   └──────────────────────────────────────────────────────────────┘
   
   Label each term underneath in TEAL:
   ∂V/∂t        → "theta — time decay"
   rS·∂V/∂S     → "rate × delta"
   ½σ²S²·∂²V/∂S² → "gamma term — convexity (Itô's correction)"
   −rV           → "discounting"

10. Boundary condition for a call:
    V(S,T) = max(S − K, 0)   at expiry
    V(0,t) = 0               stock goes to 0, option worthless
    V(S,t) → S − Ke^{−r(T−t)} as S → ∞  (deep in-the-money)
```

### VOICE-OVER SCRIPT

"Alright. This is the main event. We're deriving the Black-Scholes PDE — the partial differential equation whose solution is the formula. Every step will be explicit. [1][3]

[PAUSE — setup]

The setup: stock price S follows Geometric Brownian Motion with drift mu and volatility sigma. The option price V is some function of S and t that we don't yet know. Our goal is to find it.

[PAUSE — Step 1: Itô applied to V]

Step one: apply Itô's Lemma to V of S and t. We covered this in Episode 2. [3] The drift of V picks up three terms: the partial derivative of V with respect to time, mu S times the delta of V, and crucially — the Itô correction — one-half sigma squared S squared times the gamma of V, the second derivative with respect to S. Plus a diffusion term: sigma S delta dB.

This is the full dynamics of the option under the physical measure. Now we build the hedge.

[PAUSE — Step 2: delta-hedge construction]

Step two: construct a portfolio Pi — long one option, short Delta units of stock, where Delta equals the partial derivative of V with respect to S. The portfolio value is V minus Delta times S.

Why this particular Delta? Watch what happens when we compute the portfolio's dynamics.

[PAUSE — Step 3: compute dPi]

Step three: dPi equals dV minus Delta times dS. Substitute the Itô expression for dV and the GBM expression for dS. Expand everything.

[PAUSE — Step 4: THE CANCELLATION]

Step four. Look at the dB terms. We have plus sigma S partial V over partial S times dB from the option. And minus partial V over partial S times sigma S dB from the stock position. These are exactly equal and opposite.

[PAUSE — explosion animation]

They cancel. Perfectly. Completely. That was not an accident — we chose Delta *precisely* to make this happen. The delta is the exact hedge ratio that eliminates the randomness.

And look — the mu terms cancel too. The expected return of the stock is completely gone from the portfolio dynamics. A portfolio of an option and exactly Delta shares of stock has zero exposure to either the randomness or the expected return of the underlying. It is riskless.

[PAUSE — Step 5: no-arbitrage]

Step five: a riskless portfolio must earn the risk-free rate. This is the no-arbitrage condition. If the portfolio earned more than r, you could borrow at r and invest in Pi indefinitely — a money machine. If it earned less, short Pi and lend at r. Markets eliminate both possibilities instantly.

So dPi equals r times Pi times dt. Substitute Pi equals V minus Delta S.

[PAUSE — Step 6: assemble]

Set the two expressions for dPi equal. Collect terms. Rearrange.

[PAUSE — PDE appears]

And there it is. The Black-Scholes partial differential equation. [1]

Partial V over partial t, plus rS times partial V over partial S, plus one-half sigma squared S squared times the second partial of V over S squared, minus rV equals zero.

[PAUSE — label the Greeks]

Every term has a name traders use daily. The time derivative — theta. The rS delta term — the discounted delta contribution. The gamma term — the Itô correction, the convexity of the option, the reason options have curvature in their payoff. The minus rV — the discounting.

[PAUSE — boundary conditions]

This PDE, combined with three boundary conditions — the terminal payoff, the value when the stock hits zero, and the deep in-the-money limit — has a unique solution. Finding it analytically requires one more trick."

---

## SCENE 5: SOLVING THE PDE — THE HEAT EQUATION TRANSFORM
**Class:** `SceneHeatEquation` | **Duration:** ~3:30

### MANIM ANIMATION SEQUENCE

```
1. Title: "Solving the PDE — The Heat Equation Trick"
   Subtitle: "Physics from 1822. Finance from 1973. Same equation."
   Sources: "[6] Shreve (2004), Ch.4 | [14] Karatzas & Shreve (1991)"

2. The BS PDE again:
   \frac{\partial V}{\partial t} + rS\frac{\partial V}{\partial S}
   + \frac{1}{2}\sigma^2 S^2\frac{\partial^2 V}{\partial S^2} - rV = 0

   "This is a parabolic PDE in S and t.
    It's not in standard form. We need to massage it."

3. CHANGE OF VARIABLES — three substitutions animate in sequence:

   Step A: Time reversal
   τ = T − t   (time to expiry, running forward from 0)
   "\partial V/\partial t = -\partial V/\partial \tau"

   Step B: Log-price substitution
   x = \ln(S/K)   (log moneyness — centers the problem at x=0)
   S = Ke^x
   \frac{\partial V}{\partial S} = \frac{1}{S}\frac{\partial V}{\partial x}
   \frac{\partial^2 V}{\partial S^2} = \frac{1}{S^2}\!\left(\frac{\partial^2 V}{\partial x^2}
   - \frac{\partial V}{\partial x}\right)

   Step C: Discounting substitution
   V(S,t) = e^{-r\tau} u(x, \tau)
   (remove the discounting so we work with undiscounted price u)

4. After substitution — THE HEAT EQUATION emerges:
   
   \frac{\partial u}{\partial \tau}
   = \frac{1}{2}\sigma^2\frac{\partial^2 u}{\partial x^2}
   + \!\left(r - \frac{1}{2}\sigma^2\right)\frac{\partial u}{\partial x}

   "One more substitution to eliminate the first-order term:"
   \xi = x + \!\left(r - \frac{1}{2}\sigma^2\right)\tau

   \frac{\partial u}{\partial \tau} = \frac{1}{2}\sigma^2\frac{\partial^2 u}{\partial \xi^2}

5. BOX THIS — HEAT EQUATION IN GOLD:
   ┌─────────────────────────────────────────────┐
   │                                             │
   │   ∂u/∂τ  =  ½σ²  ∂²u/∂ξ²                 │
   │                                             │
   └─────────────────────────────────────────────┘
   
   "This is the heat equation. Joseph Fourier, 1822.
    It describes how heat diffuses through a metal rod.
    It also, apparently, prices European options.
    Physics and finance: more similar than either would like to admit."

6. Visual: Split screen
   Left:  A metal rod with temperature gradient diffusing (orange → blue gradient)
   Right: Option price surface diffusing toward payoff (same visual language)
   Label: "Same PDE. Different interpretation."

7. SOLUTION via Green's function / fundamental solution:
   
   u(\xi, \tau) = \int_{-\infty}^{\infty} u(\xi_0, 0)
   \cdot \frac{1}{\sigma\sqrt{2\pi\tau}}
   \exp\!\left(-\frac{(\xi - \xi_0)^2}{2\sigma^2\tau}\right) d\xi_0

   "The initial condition u(ξ, 0) is the option payoff max(Ke^x − K, 0)
    transformed. We integrate it against a Normal kernel — a Gaussian blur
    of the payoff backward in time."

8. After carrying out the integral (show key steps):
   
   Evaluate the integral → two terms emerge naturally:
   → SN(d₁)  from the S·1_{S>K} part of the payoff
   → Ke^{-rT}N(d₂)  from the K·1_{S>K} part
   
   Transform back: V = e^{-rτ}u
   
   ARRIVE AT THE FORMULA:
   C = S₀N(d₁) − Ke^{-rT}N(d₂)

9. Source: "[6] Shreve (2004), pp. 168–176 | [14] Karatzas & Shreve (1991)"
```

### VOICE-OVER SCRIPT

"The PDE is in hand. Now we need to solve it. And we're going to use a trick that connects the 1973 Nobel Prize to a French mathematician named Joseph Fourier who died 141 years before Black and Scholes were even born.

[PAUSE — show PDE again]

The Black-Scholes PDE is a parabolic second-order PDE in S and t. It's not in canonical form. It has a variable coefficient S squared in front of the second derivative, and it mixes time and space derivatives in a way that's hard to work with directly. We need to change variables to simplify it. [6]

[PAUSE — Change A: time reversal]

First substitution: let tau equal T minus t — time to expiry rather than calendar time. This reverses the time direction so that tau runs forward from zero at expiry to T at inception. This is standard for parabolic PDEs — we solve forward from the initial condition.

[PAUSE — Change B: log-price]

Second substitution: let x equal the natural log of S over K — the log moneyness. When S equals the strike K, x equals zero. We're centering the problem at the money. [6]

Compute the chain rule transformations for the partials. The second derivative in S becomes one over S squared times the second derivative in x minus the first derivative in x. This is where the log-price substitution earns its keep — it converts the variable-coefficient S-squared term into a constant-coefficient second derivative in x.

[PAUSE — Change C: discounting]

Third substitution: factor out the discounting. Write V as e to the minus r tau times u of x tau. This absorbs the minus rV term in the PDE.

[PAUSE — heat equation emerges]

Substitute all three changes. After algebra — which I'll spare you the step-by-step of, it's in Shreve Chapter 4 — we arrive at this: partial u over partial tau equals one-half sigma squared times the second partial of u over xi squared, where xi accounts for the drift. [6]

[PAUSE — GOLD BOX]

This. Is. The. Heat. Equation. Partial u over partial tau equals one-half sigma squared times the second partial over xi squared. Joseph Fourier derived this in 1822 to describe heat diffusing through a metal rod. [14]

[PAUSE — split screen physics vs finance]

The same equation governs how temperature profiles smooth out over time in a rod — and how option value diffuses backward from the payoff at expiry to the price today. The mathematics does not care about the interpretation. It's the same differential operator.

[PAUSE — Green's function solution]

The heat equation has a classical solution via its fundamental solution — the Green's function. The option price at any earlier time is the terminal payoff convolved with a Normal kernel. Conceptually: we're taking the payoff at expiry, smearing it backward in time through a Gaussian filter, and the result is the fair price today.

[PAUSE — show the integral and emerging terms]

When you carry out this integral explicitly — substituting the call option payoff max of S_T minus K zero, splitting the integral at S_T equals K, and evaluating each half — two terms emerge naturally. The first integral gives S₀ times N of d₁. The second gives K e to the minus rT times N of d₂.

Transform back from u to V by multiplying by e to the minus r tau.

[PAUSE — formula arrives]

And we have arrived. The Black-Scholes formula. Not from nowhere. Not from magic. From Fourier's heat equation, Itô's stochastic calculus, and the no-arbitrage principle — three ideas from three centuries, combined into one formula."

---

## SCENE 6: THE FORMULA — ANATOMY OF EVERY TERM
**Class:** `SceneFormula` | **Duration:** ~3:00

### MANIM ANIMATION SEQUENCE

```
1. Title: "The Black-Scholes Formula — Every Term Has a Job"
   Source: "[1] Black & Scholes (1973) | [7] Hull (2018)"

2. The full formula, large, centred, gold:
   C = S₀N(d₁) − Ke^{−rT}N(d₂)
   
   d₁ = [ln(S₀/K) + (r + ½σ²)T] / (σ√T)
   d₂ = d₁ − σ√T

3. DISSECTION — each piece highlighted and explained:

   TERM 1: Ke^{−rT}
   "The present value of the strike price.
    If you exercise at T, you pay K. Discounted at the risk-free rate.
    This is what the option costs you to exercise."
   → Blue highlight

   TERM 2: N(d₂)
   "The risk-neutral probability that S_T > K at expiry.
    N(d₂) = Prob^Q(S_T > K)
    Under the risk-neutral measure Q. Not the real world P.
    The probability of being in the money."
   → Green highlight
   Animate: normal distribution, shade area beyond d₂

   TERM 3: Ke^{−rT} · N(d₂)
   "Present value of what you pay, conditional on exercising.
    You only pay K if the option is in the money.
    Probability-weighted, discounted."
   → Blue + Green combined

   TERM 4: N(d₁) = Δ (Delta)
   "The option's Delta — the hedge ratio.
    The number of shares to hold to replicate the option.
    Also: approximately the probability of expiring in the money
    under the STOCK MEASURE (not Q).
    N(d₁) ≠ N(d₂) — they live in different probability measures."
   → Orange highlight

   TERM 5: S₀ · N(d₁)
   "The present value of the stock you receive, conditional on exercise.
    Delta-weighted current stock price."
   → Orange highlight

4. WHY d₁ ≠ d₂ — the Itô connection:
   
   d₁ = d₂ + σ√T
   
   "The difference between d₁ and d₂ is exactly σ√T.
    This is the Itô correction from Episode 2.
    d₂ uses the geometric mean drift (μ − ½σ²).
    d₁ uses the arithmetic mean drift (μ + ½σ²).
    The ½σ² lives inside Black-Scholes permanently."
   
   MathTex showing d₁ and d₂ with ½σ²T term highlighted in orange.

5. PUT-CALL PARITY — derived in 30 seconds:
   
   "If you hold a call and lend PV(K), or hold a put and hold the stock:
    both replicate each other by no-arbitrage."
   
   C − P = S₀ − Ke^{−rT}
   
   "Buy a call, sell a put, same strike same expiry:
    you synthetically own the stock minus PV(strike).
    No optionality. Pure forward exposure."
   
   Visual: payoff diagrams of call minus put = stock minus bond.

6. Source: "[1] Black & Scholes (1973), p.644 | [7] Hull (2018), Ch.19"
```

### VOICE-OVER SCRIPT

"The formula is in hand. Let's take it apart — every single term. Because if you can't explain every component, you don't actually understand the price.

[PAUSE — show full formula]

The Black-Scholes formula for a European call is: C equals S₀ N of d₁, minus K e to the minus rT, times N of d₂. [1]

[PAUSE — Term: Ke^{-rT}]

Start with the simplest piece: K e to the minus rT. This is the present value of the strike price — what you will pay at expiry if you exercise, discounted back to today. In a world with no uncertainty, that's exactly what the option would cost. The interesting part is everything multiplying it.

[PAUSE — Term: N(d₂)]

N of d₂ is the risk-neutral probability that the option expires in the money — that S_T exceeds K at expiry. [7] Not the real-world probability. The risk-neutral probability. Under the risk-neutral measure Q, where we've replaced the stock's actual drift mu with the risk-free rate r. More on that distinction in a moment.

[PAUSE — Term: N(d₁) = Delta]

N of d₁ is the option's delta — the number of shares of stock you need to hold to replicate the option at every instant. It's also the probability of expiring in the money under a different measure — the stock measure, where we use the stock as the numeraire rather than the bond. These two probability measures differ by exactly the Itô correction.

[PAUSE — d₁ vs d₂ gap]

And here it is again — our old friend from Episode 2. d₁ minus d₂ equals sigma root T. The difference between the hedge ratio probability and the exercise probability is the Itô correction. [3] d₂ uses the geometric mean drift — mu minus one-half sigma squared. d₁ uses the arithmetic mean drift. The one-half sigma squared is permanently embedded in the Black-Scholes formula, as it must be, because Brownian motion lives in Itô's universe.

[PAUSE — Put-Call Parity]

Before we move on — Put-Call Parity. It takes thirty seconds to derive. A portfolio of long call, short put, same strike same expiry, must equal a long forward on the stock minus the present value of the strike. That's no-arbitrage. No stochastic calculus required. Just the law of one price. C minus P equals S₀ minus K e to the minus rT.

[PAUSE]

If you know the call price, you know the put price. The two are not independent. The market respects this to the tick — if it doesn't, there's an arbitrage, and arbitrageurs close it within seconds."

---

## SCENE 7: THE RISK-NEUTRAL WORLD — THE DEEP INSIGHT
**Class:** `SceneRiskNeutral` | **Duration:** ~2:30

### MANIM ANIMATION SEQUENCE

```
1. Title: "The Risk-Neutral World — The Most Important Idea in Derivatives Pricing"
   Sources: "[12] Harrison & Kreps (1979) | [13] Harrison & Pliska (1981) | [11] Cox & Ross (1976)"

2. The mystery restated:
   "When we derived the PDE, the drift μ disappeared.
    The option price doesn't depend on μ.
    A stock you think will return 5% and a stock you think will return 25%
    have the SAME option price if they have the same σ.
    Why?"

3. Risk-Neutral Measure Q — formal definition:
   
   "Under the REAL measure P:  dS = μS dt + σS dB^P
    Under the RISK-NEUTRAL measure Q:  dS = rS dt + σS dB^Q
    
    We replace μ with r. The drift changes.
    The Brownian motion changes. The volatility stays the same."
   
   Girsanov's theorem reference:
   B^Q_t = B^P_t + [(μ−r)/σ]·t     (change of measure)
   "The market price of risk: λ = (μ−r)/σ"
   "[6] Shreve (2004) — Girsanov's Theorem, Ch.5"

4. The risk-neutral pricing formula:
   
   C = e^{−rT} \mathbb{E}^Q[\max(S_T − K, 0)]
   
   "The option price equals the discounted expectation of the payoff
    under the risk-neutral measure Q.
    Not the real probability. The risk-adjusted probability.
    This is the Fundamental Theorem of Asset Pricing."
   
   Sources:
   "[12] Harrison & Kreps (1979) — no arbitrage ↔ existence of Q"
   "[13] Harrison & Pliska (1981) — completeness ↔ uniqueness of Q"

5. Visual: Two worlds side by side
   
   Left:  "Real World P"
          Stock drifts at μ
          Investors are risk-averse
          Higher return demanded for risk
          Option price depends on μ (problem)
   
   Right: "Risk-Neutral World Q"
          Stock drifts at r
          Investors are risk-neutral
          All assets earn r
          Option price doesn't depend on μ (solved)
   
   Arrow: "Girsanov's Theorem bridges the two"

6. The fundamental theorem — clean, gold, boxed:
   
   "No arbitrage ↔ there exists a risk-neutral measure Q
    Market completeness ↔ Q is unique
    Option price = e^{−rT} E^Q[Payoff]"
   
   "[12] Harrison & Kreps (1979) | [13] Harrison & Pliska (1981)"

7. Taleb note (sarcastic, gold italic):
   "The risk-neutral world is not a description of reality.
    It is a computational trick that gives the right answer
    by construction. Do not confuse it with how investors
    actually behave. Most of them don't even know it exists."
   — Quantifaya, channelling Taleb [9]
```

### VOICE-OVER SCRIPT

"Here's the question that should be bothering you. When we derived the PDE, the drift mu — the expected return of the stock — disappeared entirely. The option price doesn't depend on whether you think the stock will return five percent or fifty percent. As long as sigma is the same, the option price is the same.

This is not obvious. This is profound. And it has a precise mathematical explanation.

[PAUSE — show two measures]

The answer is the risk-neutral measure. [11]

Under the real-world probability measure P, the stock drifts at mu — its actual expected return, reflecting investors' risk preferences and compensation for bearing equity risk. Under the risk-neutral measure Q, we instead assume the stock drifts at r — the risk-free rate. Everyone is indifferent to risk. All assets earn the same return.

[PAUSE — Girsanov]

The transition between these two worlds is governed by Girsanov's Theorem. [6] We change the Brownian motion by subtracting the market price of risk — lambda equals mu minus r over sigma — multiplied by time. Under Q, the new Brownian motion makes the stock drift at r.

[PAUSE — risk-neutral pricing formula]

This gives us the risk-neutral pricing formula: option price equals the discounted expectation of the payoff under Q. [12] This is the Fundamental Theorem of Asset Pricing — the deepest result in modern derivatives theory.

Harrison and Kreps in 1979 proved that the absence of arbitrage is equivalent to the existence of at least one risk-neutral measure. [12] Harrison and Pliska in 1981 proved that market completeness — the ability to replicate any payoff — is equivalent to the uniqueness of that measure. [13] The Black-Scholes model is complete: one stock, one Brownian motion, one Q.

[PAUSE — two-world diagram]

The risk-neutral world is not a description of how investors actually behave. Nobody genuinely expects all assets to earn the risk-free rate. It is a computational device. A change of probability measure that makes option pricing tractable while preserving the no-arbitrage constraint. The answer it gives is correct — by construction.

[PAUSE — sarcastic note]

Do not confuse the risk-neutral measure with reality. Most people in finance don't. Because most people in finance don't know it exists."

---

## SCENE 8: WHERE BLACK-SCHOLES BREAKS — AND WHAT CAME AFTER
**Class:** `SceneBreaks` | **Duration:** ~2:30

### MANIM ANIMATION SEQUENCE

```
1. Title: "Where Black-Scholes Breaks — The Vol Smile and What Came After"
   Sources: "[15] Derman & Kani (1994) | [8] Wilmott (2006) | [10] Taleb (2007)"

2. THE VOLATILITY SMILE — animated:
   
   Axes: x = Strike K (or moneyness K/S), y = Implied Volatility σ_imp
   
   Flat line: "Black-Scholes prediction: σ_imp = constant"  (blue, dashed)
   
   Curved, smirking line appears:
   "Market reality: vol smile post-1987"  (orange)
   
   The real line dips at ATM and rises on both wings — the smile.
   For equities specifically, it skews left — the smirk:
   "Equity vol skew: OTM puts are expensive (tail insurance demand)"
   
   "If BS were true, all strikes would imply the same σ.
    They don't. Every strike implies a different vol.
    The 'constant σ' assumption collapsed on October 19, 1987."

3. WHY THE SMILE EXISTS — three bullets:
   
   ① "Fat tails (Ep.1) — OTM options more likely than BS predicts"
   ② "Jump risk — large moves make far OTM options valuable"  
   ③ "Supply/demand — institutional demand for put protection"

4. WHAT REPLACED BS (PREVIEW):
   
   LOCAL VOLATILITY — Derman & Kani (1994) [15]:
   σ = σ(S, t)   ← vol is a function of stock price AND time
   "Fits the smile exactly by construction. Loses intuition."
   
   STOCHASTIC VOLATILITY — Heston (1993):
   dσ² = κ(θ − σ²)dt + ξσ√(σ²) dW_t
   "Vol itself follows a mean-reverting process. Two random sources.
    More realistic. Still analytically tractable (barely)."
   
   JUMP-DIFFUSION — Merton (1976) [2]:
   dS = μS dt + σS dB + S dJ_t
   "Adds compound Poisson jumps. Captures crash risk."

5. The irony panel — gold italic:
   "Black-Scholes is used as the UNIT OF MEASUREMENT for options.
    Traders quote options in implied vol — which IS the BS vol
    that makes the BS price equal to the market price.
    
    The model is wrong.
    The market prices options using the model's implied vol surface.
    The wrong model is the language of the right market.
    
    This is either profound or farcical. Possibly both."
   — Quantifaya

6. Taleb:
   "The Black-Scholes formula is just a transformation of variables.
    Using it to price tail risk is like using a thermometer to measure earthquakes."
   — Paraphrased from Taleb, Dynamic Hedging [9]
```

### VOICE-OVER SCRIPT

"We'd be lying to you if we derived Black-Scholes without telling you where it breaks. And it breaks — spectacularly — in at least one place.

[PAUSE — vol smile animation]

The volatility smile. If Black-Scholes were correct, every option on the same underlying, regardless of strike or maturity, would imply the same volatility sigma. That's what constant sigma means. You'd see a flat line across all strikes.

[PAUSE — curved reality]

What you actually see, in every liquid options market in the world, is a curve. OTM puts are expensive relative to Black-Scholes. OTM calls vary by market. In equities, you typically see a skew — a smirk — where out-of-the-money puts carry significantly higher implied vol than at-the-money options. This is the market pricing in the fat left tail — crash risk — that Black-Scholes says is nearly impossible. [10]

This phenomenon did not exist before October 1987. The 1987 Black Monday crash bent the smile into existence. It has never straightened since. The constant vol assumption has been empirically violated for 37 years. [15]

[PAUSE — why the smile exists]

Three reasons. First: fat tails. As we showed in Episode 1, real returns have excess kurtosis — more probability mass in the tails than Normal distributions predict. OTM options are worth more than BS says. Second: jump risk. Crash events are discrete, large, and fast — not continuous diffusions. OTM puts insure against crashes. They're valuable. Third: supply and demand. Institutional investors systematically buy OTM puts as portfolio insurance. This demand pushes their prices — and thus their implied vols — above Black-Scholes.

[PAUSE — what replaced BS]

The industry response was a hierarchy of increasingly sophisticated models. Derman and Kani in 1994 introduced local volatility — sigma as a function of both the stock price and time, calibrated to match the observed smile exactly. [15] Heston's stochastic volatility model in 1993 makes vol itself a random process — a mean-reverting diffusion. Merton's jump-diffusion adds compound Poisson jumps. [2]

All of these are extensions of Black-Scholes. All of them inherit its structure. None of them replace the fundamental insight.

[PAUSE — the irony]

Here's the irony that professional options traders live with every day. Black-Scholes is wrong. And the market uses it as the unit of measurement. Traders quote option prices not in dollars — they quote them in implied volatility. Which is the Black-Scholes sigma that makes the formula match the market price. The wrong model is the language in which the correct prices are communicated.

This is either profound or farcical. I'll let you decide."

---

## SCENE 9: LESSONS — AXE CAPITAL TAKEAWAYS
**Class:** `SceneLessons` | **Duration:** ~1:30

### MANIM ANIMATION SEQUENCE

```
1. Title: "What This Means For You — No Softening"
   Subtitle: "Axe Capital doesn't softening anything either."

2. TRUTH I — RED:
   "The Black-Scholes formula is not magic.
    It is Itô's Lemma + no-arbitrage + heat equation.
    Three ideas. All derivable. All yours now."
   Source: "[1][3][6]"

3. TRUTH II — GOLD:
   "μ doesn't matter. The option price is independent of
    the stock's expected return. This is counterintuitive.
    It is also one of the most important results in finance.
    Understand WHY before your next interview."
   Source: "[12] Harrison & Kreps (1979)"

4. TRUTH III — TEAL:
   "Black-Scholes is simultaneously wrong and the industry standard.
    Learn it deeply enough to know exactly HOW it is wrong.
    That knowledge is worth more than knowing it's wrong."
   Source: "[15] Derman & Kani (1994)"

5. TRUTH IV — PURPLE (interview gold):
   "In a quant interview:
    → Can you derive the BS PDE from Itô + no-arbitrage?  ← Top 5%
    → Can you explain why N(d₂) ≠ N(d₁)?  ← Top 10%
    → Can you explain the smile?  ← Top 20%
    → Can you just state the formula?  ← Everyone else."

6. Taleb final quote — large, gold, centred:
   "The answer is that the hedging errors are generally small
    for vanilla options but can be monstrous for exotics."
   — N.N. Taleb, Dynamic Hedging [9]
   
   Beat. Quantifaya response:
   "Know your model. Know its limits. Know when it fails.
    That's what separates a quant from someone who Googled the formula."
   — Quantifaya

7. Rolling citation credits across bottom.
```

### VOICE-OVER SCRIPT

"Four truths. No softening.

[PAUSE — Truth I]

The Black-Scholes formula is not magic and it is not a black box. It is Itô's Lemma applied to a delta-hedged portfolio, plus the no-arbitrage condition, plus the classical heat equation solution. Three ideas. All derivable in under an hour. All yours now. [1][3][6]

[PAUSE — Truth II]

The expected return of the stock doesn't affect the option price. This seems wrong. It isn't. The risk-neutral measure explains it: under Q, all assets earn r by construction, so mu is simply irrelevant to the pricing problem. Harrison and Kreps proved this rigorously in 1979. [12] If you go into a quant interview and can explain *why* mu disappears — not just that it does — you are already in the top ten percent of candidates.

[PAUSE — Truth III]

Black-Scholes has been empirically wrong about volatility since 1987. The smile proves it. And it's still the benchmark. Learn it deeply enough to know exactly how it's wrong, where it's wrong, and what the smile tells you about the assumptions it's violating. That knowledge is worth more than knowing it fails. [15]

[PAUSE — Truth IV]

Interview calibration. Can you derive the PDE from Itô and no-arbitrage? Top five percent. Can you explain why N of d₁ and N of d₂ are different? Top ten. Can you explain the vol smile qualitatively? Top twenty. Can you just recite the formula? That's everyone.

[PAUSE — Taleb]

Taleb wrote in Dynamic Hedging: 'The hedging errors are generally small for vanilla options but can be monstrous for exotics.' [9] Know your model. Know its limits. Know when it fails. That's what separates a quant from someone who Googled the formula."

---

## SCENE 10: OUTRO — CTA AND NEXT EPISODE
**Class:** `SceneOutro` | **Duration:** ~1:00

### MANIM ANIMATION SEQUENCE

```
1. Quantifaya logo pulses in purple.
   "Financial Engineering. Explained Rigorously. Applied Practically."

2. Episode recap — bullets fly in:
   ✓ Option payoff structure and the pricing problem
   ✓ Bachelier (1900), Samuelson (1965) — the road to 1973
   ✓ Four BS assumptions — and the cost of each
   ✓ PDE derived from Itô's Lemma + delta-hedge + no-arbitrage
   ✓ Heat equation transformation and the analytical solution
   ✓ Formula anatomy: N(d₁), N(d₂), d₁ vs d₂, put-call parity
   ✓ Risk-neutral measure Q and the Fundamental Theorem
   ✓ Vol smile, local vol, stochastic vol — where BS breaks

3. Book recommendations:
   📚 "Options, Futures, and Other Derivatives" — Hull (2018) [7]
   "The practitioner's BS bible. Chapters 15 and 19. Non-negotiable."
   
   📚 "Dynamic Hedging" — Taleb (1997) [9]
   "The book that tells you everything BS gets wrong in practice.
    Read Hull first. Then read Taleb to understand why Hull's world
    is cleaner than the real one."

4. Comment challenge:
   "Derive the BS price of a cash-or-nothing digital call —
    a contract that pays $1 if S_T > K, zero otherwise.
    Hint: the answer involves N(d₂). Why does only d₂ appear?
    First correct full answer gets pinned."
   
   (Answer: e^{−rT}N(d₂) — only N(d₂) because there's no stock-leg,
    only the risk-neutral probability of exercise)

5. Next episode tease:
   Equations flash rapidly:
   Δ = N(d₁)
   Γ = N'(d₁)/(Sσ√T)
   Θ = −SN'(d₁)σ/(2√T) − rKe^{−rT}N(d₂)
   𝒱 = S√T·N'(d₁)
   
   "Next on Quantifaya:"
   "The Greeks: Delta, Gamma, Vega, Theta — Built From First Principles"
   "Why Gamma is dangerous. Why Vega is often more important than Delta.
    And why your Theta bleeds every single night."

6. End card. Subscribe. Share.
```

### VOICE-OVER SCRIPT

"That's Episode Three.

[PAUSE — recap]

We covered the full Black-Scholes arc. The option pricing problem and the century of failed attempts before 1973. The four assumptions and their real-world cost. The PDE derivation — Itô's Lemma, delta hedge, dB cancellation, no-arbitrage condition. The heat equation transformation that gave us the analytical solution. The anatomy of every term in the formula. The risk-neutral measure and the Fundamental Theorem of Asset Pricing. And finally — where it all breaks, and what the profession built to replace it.

[PAUSE — book recommendations]

Two books. Hull's Options, Futures, and Other Derivatives — the practitioner's bible. Chapters fifteen and nineteen cover Black-Scholes as thoroughly as any textbook. Read it first. [7] Then read Taleb's Dynamic Hedging — the book that tells you everything Hull's clean framework glosses over when you're actually on a derivatives desk running a book with real P&L. [9]

[PAUSE — comment challenge]

Comment challenge: price a cash-or-nothing digital call — a contract that pays exactly one dollar if S_T exceeds K, zero otherwise. Use the risk-neutral pricing formula. The answer involves N of d₂. I want to see the full derivation and an explanation of why only d₂ appears and not d₁. First complete correct answer gets pinned.

[PAUSE — next episode tease]

Next week: the Greeks. Delta, Gamma, Vega, Theta — derived from the Black-Scholes formula by differentiation. We'll build every single one from first principles, explain what each one means economically, and talk about why Gamma exposure is the most dangerous thing a derivatives desk can run. Your theta bleeds every night. Next week you'll know exactly why.

Subscribe. Share this with one person who's ever pretended to understand Black-Scholes without being able to derive it. There are more of them than you think.

This is Quantifaya."

---

---

## APPENDIX A — FULL EQUATION REFERENCE

| Equation | LaTeX | Scene |
|---|---|---|
| Call payoff | `\max(S_T - K, 0)` | 2 |
| Put payoff | `\max(K - S_T, 0)` | 2 |
| GBM | `dS = \mu S\,dt + \sigma S\,dB` | 3, 4 |
| Itô applied to V | `dV=\!\left(\frac{\partial V}{\partial t}+\mu S\frac{\partial V}{\partial S}+\frac{1}{2}\sigma^2S^2\frac{\partial^2 V}{\partial S^2}\right)dt+\sigma S\frac{\partial V}{\partial S}dB` | 4 |
| Delta-hedge portfolio | `\Pi = V - \frac{\partial V}{\partial S}\cdot S` | 4 |
| Riskless dΠ | `d\Pi=\!\left(\frac{\partial V}{\partial t}+\frac{1}{2}\sigma^2S^2\frac{\partial^2 V}{\partial S^2}\right)dt` | 4 |
| Black-Scholes PDE | `\frac{\partial V}{\partial t}+rS\frac{\partial V}{\partial S}+\frac{1}{2}\sigma^2S^2\frac{\partial^2 V}{\partial S^2}-rV=0` | 4 |
| Boundary condition (call) | `V(S,T)=\max(S-K,0)` | 4 |
| Heat equation | `\frac{\partial u}{\partial\tau}=\frac{1}{2}\sigma^2\frac{\partial^2 u}{\partial\xi^2}` | 5 |
| Green's function solution | `u(\xi,\tau)=\int_{-\infty}^{\infty}u_0(\xi_0)\frac{1}{\sigma\sqrt{2\pi\tau}}\exp\!\left(-\frac{(\xi-\xi_0)^2}{2\sigma^2\tau}\right)d\xi_0` | 5 |
| BS call formula | `C=S_0N(d_1)-Ke^{-rT}N(d_2)` | 6 |
| d₁ | `d_1=\frac{\ln(S_0/K)+(r+\frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}` | 6 |
| d₂ | `d_2=d_1-\sigma\sqrt{T}` | 6 |
| d₁ − d₂ (Itô correction) | `d_1-d_2=\sigma\sqrt{T}` | 6 |
| N(d₂) interpretation | `N(d_2)=\mathbb{P}^Q(S_T>K)` | 6 |
| Put-Call Parity | `C-P=S_0-Ke^{-rT}` | 6 |
| Risk-neutral pricing | `C=e^{-rT}\mathbb{E}^Q[\max(S_T-K,0)]` | 7 |
| Girsanov / market price of risk | `\lambda=\frac{\mu-r}{\sigma}` | 7 |
| Digital call price | `C_{\text{digital}}=e^{-rT}N(d_2)` | 10 |

---

## APPENDIX B — COMPLETE MANIM PYTHON SKELETON

```python
# quantifaya_ep3.py
# Render: manim -pqh quantifaya_ep3.py FullEpisode --fps 60 --resolution 1920x1080

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
    return Text(refs, color=TEAL, font_size=14).to_corner(DR).shift(UP*0.1+LEFT*0.1)


# ══════════════════════════════════════════════════════════════════════════
class SceneIntro(Scene):
    def construct(self):
        names = VGroup(
            Text("Fischer Black",  color=FG, font_size=52),
            Text("Myron Scholes",  color=FG, font_size=52),
            Text("Robert Merton",  color=FG, font_size=52),
        ).arrange(DOWN, buff=0.4).shift(UP*0.5)
        for n in names:
            self.play(FadeIn(n), run_time=0.6)
        self.wait(1)

        nobel = Text("1997 Nobel Prize in Economics.", color=GOLD, font_size=36)\
                    .next_to(names, DOWN, buff=0.5)
        self.play(FadeIn(nobel)); self.wait(1)

        # Red X over Black
        x_mark = Cross(names[0], color=RED, stroke_width=5)
        died   = Text("Died: August 30, 1995. Nobel Prizes are not awarded posthumously.",
                      color=RED, font_size=22).next_to(names[0], RIGHT, buff=0.3)
        src    = cite("[16] Nobel Committee (1997), Royal Swedish Academy of Sciences")
        self.play(Create(x_mark), FadeIn(died), FadeIn(src)); self.wait(2)

        # Formula in blood red
        self.play(FadeOut(names), FadeOut(nobel), FadeOut(x_mark),
                  FadeOut(died), FadeOut(src))
        formula = MathTex(r"C = S_0 N(d_1) - K e^{-rT} N(d_2)",
                          color=RED, font_size=56).center()
        self.play(Write(formula)); self.wait(1)

        desc = VGroup(
            Text("The most famous equation in finance.", color=FG, font_size=26),
            Text("Taught in every program. Understood by almost none.", color=FG, font_size=26),
            Text("Derived by even fewer.", color=ORANGE, font_size=26, weight=BOLD),
        ).arrange(DOWN, buff=0.25).next_to(formula, DOWN, buff=0.5)
        self.play(FadeIn(desc)); self.wait(1.5)

        self.play(FadeOut(formula), FadeOut(desc))
        manifesto = VGroup(
            Text("Today we derive it.", color=GOLD, font_size=36, weight=BOLD),
            Text("All of it. From first principles.", color=FG, font_size=28),
            Text("No hand-waving. No 'it can be shown.' We show.",
                 color=ORANGE, font_size=26, slant=ITALIC),
        ).arrange(DOWN, buff=0.35).center()
        self.play(FadeIn(manifesto)); self.wait(1.5)

        title_card = VGroup(
            Text("QUANTIFAYA", color=PURPLE, font_size=52, weight=BOLD),
            Text("Episode 3", color=FG, font_size=26),
            Text("Black-Scholes — Derived From Scratch", color=GOLD, font_size=34),
            Text("PDE  →  Heat Equation  →  Formula  →  Nobel Prize",
                 color=FG, font_size=22),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeOut(manifesto), FadeIn(title_card)); self.wait(3)


# ══════════════════════════════════════════════════════════════════════════
class SceneProblemSetup(Scene):
    def construct(self):
        title = Text("Step 0: What Are We Actually Pricing?",
                     color=GOLD, font_size=36).to_edge(UP)
        src   = cite("[5] Bachelier (1900)  |  [4] Samuelson (1965)  |  [7] Hull (2018)")
        self.play(FadeIn(title), FadeIn(src))

        # Call payoff
        ax = Axes(x_range=[0, 160, 20], y_range=[0, 60, 10],
                  x_length=9, y_length=5, axis_config={"color": FG})
        ax_lbl = ax.get_axis_labels(
            Tex(r"S_T", color=FG, font_size=24),
            Tex(r"\text{Payoff}", color=FG, font_size=24))
        K = 100
        call_payoff = ax.plot(lambda x: max(x - K, 0),
                               x_range=[0, 160], color=GREEN, stroke_width=3)
        put_payoff  = ax.plot(lambda x: max(K - x, 0),
                               x_range=[0, 160], color=RED, stroke_width=3)
        k_dot   = Dot(ax.c2p(K, 0), color=GOLD)
        k_label = MathTex("K", color=GOLD, font_size=24).next_to(k_dot, DOWN)

        call_label = MathTex(r"\text{Call: }\max(S_T - K, 0)",
                              color=GREEN, font_size=24).to_corner(UR).shift(DOWN*0.5)
        put_label  = MathTex(r"\text{Put: }\max(K - S_T, 0)",
                              color=RED, font_size=24).next_to(call_label, DOWN)

        self.play(Create(ax), Write(ax_lbl))
        self.play(Create(call_payoff), FadeIn(call_label))
        self.play(Create(k_dot), Write(k_label))
        self.play(Create(put_payoff), FadeIn(put_label))
        self.wait(1.5)

        # Timeline
        self.play(FadeOut(ax), FadeOut(ax_lbl), FadeOut(call_payoff),
                  FadeOut(put_payoff), FadeOut(k_dot), FadeOut(k_label),
                  FadeOut(call_label), FadeOut(put_label))

        timeline = VGroup(
            Line(LEFT*5, RIGHT*5, color=FG),
            Dot(LEFT*5, color=GOLD),
            Dot(RIGHT*5, color=GOLD),
            Text("t = 0\n'Pay C'\nKnow: S₀, K, r, σ",
                 color=TEAL, font_size=20, line_spacing=1.3).next_to(LEFT*5, DOWN, buff=0.3),
            Text("t = T\n'Receive max(S_T−K, 0)'\nDon't know: S_T",
                 color=ORANGE, font_size=20, line_spacing=1.3).next_to(RIGHT*5, DOWN, buff=0.3),
        )
        self.play(Create(timeline)); self.wait(1.5)

        # History
        self.play(FadeOut(timeline))
        history = VGroup(
            VGroup(
                Text("Bachelier (1900) [5]", color=GOLD, font_size=24, weight=BOLD),
                Text("First mathematical option model. Arithmetic BM. Heroic.", color=FG, font_size=20),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("Samuelson (1965) [4]", color=GOLD, font_size=24, weight=BOLD),
                Text("GBM. Right dynamics. No closed form.", color=FG, font_size=20),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("Black, Scholes, Merton (1973) [1][2]", color=GOLD, font_size=24, weight=BOLD),
                Text("Closed form. Nobel Prize. $600T market.", color=GREEN, font_size=20),
            ).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).center()
        self.play(LaggedStart(*[FadeIn(h) for h in history], lag_ratio=0.4))
        self.wait(3)


# ══════════════════════════════════════════════════════════════════════════
class SceneAssumptions(Scene):
    def construct(self):
        title = Text("The Four Assumptions — The Price of Tractability",
                     color=GOLD, font_size=34).to_edge(UP)
        src   = cite("[8] Wilmott (2006)  |  [9] Taleb (1997)  |  [10] Taleb (2007)")
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
            self.play(FadeIn(grp)); self.wait(2.5); self.play(FadeOut(grp))

        # Wilmott quote
        wilmott = VGroup(
            Text('"All models are wrong.\n The question is whether they are wrong in a useful way."',
                 color=GOLD, font_size=28, slant=ITALIC, line_spacing=1.4),
            Text("— P. Wilmott, Paul Wilmott on Quantitative Finance [8]",
                 color=FG, font_size=22),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeIn(wilmott)); self.wait(3)


# ══════════════════════════════════════════════════════════════════════════
class ScenePDE(Scene):
    def construct(self):
        title = Text("The Derivation — Itô + No-Arbitrage = Black-Scholes PDE",
                     color=GOLD, font_size=32).to_edge(UP)
        src   = cite("[1] Black & Scholes (1973)  |  [3] Itô (1944)  |  [6] Shreve (2004)")
        self.play(FadeIn(title), FadeIn(src))

        # Setup
        setup = VGroup(
            MathTex(r"\text{Stock: } dS = \mu S\,dt + \sigma S\,dB",
                    color=FG, font_size=30),
            MathTex(r"\text{Option: } V = V(S,t) \text{ — unknown}",
                    color=FG, font_size=30),
            MathTex(r"\text{Goal: find } V(S,t) \text{ explicitly}",
                    color=TEAL, font_size=30),
        ).arrange(DOWN, buff=0.3).shift(UP*0.5)
        self.play(FadeIn(setup)); self.wait(1); self.play(FadeOut(setup))

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
            self.play(FadeIn(g)); self.wait(2.5); self.play(FadeOut(g))

        # No-arbitrage → PDE
        noarb = VGroup(
            Text("No-arbitrage: riskless portfolio earns r  →  dΠ = rΠ dt",
                 color=TEAL, font_size=24),
            Text("Set equal. Rearrange.", color=FG, font_size=22),
        ).arrange(DOWN, buff=0.2).shift(UP*2)
        self.play(FadeIn(noarb))

        pde = MathTex(
            r"\frac{\partial V}{\partial t}"
            r"+rS\frac{\partial V}{\partial S}"
            r"+\frac{1}{2}\sigma^2S^2\frac{\partial^2 V}{\partial S^2}"
            r"-rV=0",
            color=GOLD, font_size=44).next_to(noarb, DOWN, buff=0.5)
        box = SurroundingRectangle(pde, color=PURPLE, buff=0.3, stroke_width=3)
        self.play(Write(pde), Create(box)); self.wait(1.5)

        # Label Greeks
        labels = VGroup(
            Text("∂V/∂t  →  theta", color=TEAL, font_size=20),
            Text("rS·∂V/∂S  →  rate×delta", color=TEAL, font_size=20),
            Text("½σ²S²·∂²V/∂S²  →  gamma term (Itô correction)", color=ORANGE, font_size=20),
            Text("−rV  →  discounting", color=TEAL, font_size=20),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(box, DOWN, buff=0.4)
        self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.2))
        self.wait(3)


# ══════════════════════════════════════════════════════════════════════════
class SceneHeatEquation(Scene):
    def construct(self):
        title = Text("Solving the PDE — The Heat Equation Trick",
                     color=GOLD, font_size=34).to_edge(UP)
        src   = cite("[6] Shreve (2004), Ch.4  |  [14] Karatzas & Shreve (1991)")
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
            self.play(FadeIn(g)); self.wait(2); self.play(FadeOut(g))

        # Heat equation
        heat_label = Text("After substitution — the Black-Scholes PDE becomes:",
                          color=TEAL, font_size=24).shift(UP*2.5)
        heat = MathTex(
            r"\frac{\partial u}{\partial \tau}"
            r"= \frac{1}{2}\sigma^2\frac{\partial^2 u}{\partial \xi^2}",
            color=GOLD, font_size=52)
        heat_box = SurroundingRectangle(heat, color=PURPLE, buff=0.3, stroke_width=3)
        fourier = Text("The Heat Equation — Joseph Fourier, 1822.\n"
                       "Physics from 1822. Option pricing from 1973. Same equation.",
                       color=FG, font_size=22, line_spacing=1.3)\
                      .next_to(heat_box, DOWN, buff=0.4)
        self.play(FadeIn(heat_label), Write(heat), Create(heat_box))
        self.play(FadeIn(fourier)); self.wait(2)

        # Green's function
        self.play(FadeOut(heat_label), FadeOut(heat), FadeOut(heat_box), FadeOut(fourier))
        gf_title = Text("Solution — Green's Function (Gaussian convolution):",
                        color=TEAL, font_size=26).shift(UP*2.5)
        gf_eq = MathTex(
            r"u(\xi,\tau)=\int_{-\infty}^{\infty}u_0(\xi_0)"
            r"\cdot\frac{1}{\sigma\sqrt{2\pi\tau}}"
            r"\exp\!\left(-\frac{(\xi-\xi_0)^2}{2\sigma^2\tau}\right)d\xi_0",
            color=FG, font_size=26)
        gf_note = Text("Integrate the payoff against a Normal kernel.\n"
                       "Gaussian blur of the payoff, diffused backward in time.",
                       color=GOLD, font_size=22, slant=ITALIC, line_spacing=1.3)\
                      .next_to(gf_eq, DOWN, buff=0.4)
        arrives = VGroup(
            Text("Evaluate the integral → transform back → arrive at:", color=TEAL, font_size=22),
            MathTex(r"C = S_0 N(d_1) - K e^{-rT} N(d_2)", color=GOLD, font_size=42),
        ).arrange(DOWN, buff=0.3).next_to(gf_note, DOWN, buff=0.4)
        self.play(FadeIn(gf_title), FadeIn(gf_eq), FadeIn(gf_note))
        self.play(FadeIn(arrives)); self.wait(3)


# ══════════════════════════════════════════════════════════════════════════
class SceneFormula(Scene):
    def construct(self):
        title = Text("The Formula — Every Term Has a Job",
                     color=GOLD, font_size=36).to_edge(UP)
        src   = cite("[1] Black & Scholes (1973), p.644  |  [7] Hull (2018), Ch.19")
        self.play(FadeIn(title), FadeIn(src))

        formula = MathTex(r"C = S_0 N(d_1) - K e^{-rT} N(d_2)",
                          color=GOLD, font_size=44).shift(UP*1.5)
        d_eqs = VGroup(
            MathTex(r"d_1=\frac{\ln(S_0/K)+(r+\frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}",
                    color=FG, font_size=26),
            MathTex(r"d_2 = d_1 - \sigma\sqrt{T}", color=FG, font_size=26),
        ).arrange(RIGHT, buff=0.8).next_to(formula, DOWN, buff=0.3)
        self.play(Write(formula), FadeIn(d_eqs)); self.wait(1)

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
            self.play(FadeIn(g)); self.wait(2.2); self.play(FadeOut(g))

        # Put-call parity
        pcp = VGroup(
            Text("Put-Call Parity — derived from no-arbitrage in 30 seconds:",
                 color=TEAL, font_size=24),
            MathTex(r"C - P = S_0 - Ke^{-rT}", color=GOLD, font_size=40),
            Text("Long call + short put = long stock + short bond. Always.",
                 color=FG, font_size=22),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeIn(pcp)); self.wait(3)


# ══════════════════════════════════════════════════════════════════════════
class SceneRiskNeutral(Scene):
    def construct(self):
        title = Text("The Risk-Neutral World — The Deepest Insight",
                     color=GOLD, font_size=34).to_edge(UP)
        src   = cite("[12] Harrison & Kreps (1979)  |  [13] Harrison & Pliska (1981)  |  [11] Cox & Ross (1976)")
        self.play(FadeIn(title), FadeIn(src))

        mystery = VGroup(
            Text("μ — the expected return of the stock — vanished from the PDE.", color=FG, font_size=24),
            Text("A stock returning 5% and one returning 25% have the SAME option price",
                 color=ORANGE, font_size=24, weight=BOLD),
            Text("if their volatility σ is identical. Why?", color=FG, font_size=24),
        ).arrange(DOWN, buff=0.3).shift(UP*1.5)
        self.play(FadeIn(mystery)); self.wait(2); self.play(FadeOut(mystery))

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
        self.play(FadeIn(two_worlds[0])); self.wait(1)
        self.play(FadeIn(two_worlds[1]), Create(arrow), FadeIn(girsanov))
        self.wait(2)

        self.play(FadeOut(two_worlds), FadeOut(arrow), FadeOut(girsanov))
        # Fundamental theorem
        fund_thm = VGroup(
            Text("Fundamental Theorem of Asset Pricing:", color=GOLD, font_size=28, weight=BOLD),
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
        self.play(FadeIn(fund_thm), Create(box)); self.wait(3)


# ══════════════════════════════════════════════════════════════════════════
class SceneBreaks(Scene):
    def construct(self):
        title = Text("Where Black-Scholes Breaks — The Vol Smile",
                     color=GOLD, font_size=34).to_edge(UP)
        src   = cite("[15] Derman & Kani (1994)  |  [8] Wilmott (2006)  |  [10] Taleb (2007)")
        self.play(FadeIn(title), FadeIn(src))

        ax = Axes(x_range=[70, 130, 10], y_range=[0.10, 0.40, 0.05],
                  x_length=9, y_length=5, axis_config={"color": FG})
        ax_lbl = ax.get_axis_labels(
            Tex(r"\text{Strike }K", color=FG, font_size=22),
            Tex(r"\sigma_{\text{imp}}", color=FG, font_size=22))

        flat = ax.plot(lambda x: 0.20, x_range=[70,130], color=BLUE_NORM,
                       stroke_width=2, stroke_dasharray=[8, 4])
        flat_lbl = Text("BS prediction: σ = constant", color=BLUE_NORM, font_size=20)\
                       .next_to(ax, RIGHT, buff=0.3).shift(UP*0.5)

        # Equity smirk — OTM puts expensive
        smile = ax.plot(lambda x: 0.20 + 0.0008*(100-x)**2 - 0.0005*(x-100),
                         x_range=[70, 130], color=ORANGE, stroke_width=3)
        smile_lbl = Text("Reality: vol skew post-1987", color=ORANGE, font_size=20)\
                        .next_to(ax, RIGHT, buff=0.3).shift(DOWN*0.2)

        self.play(Create(ax), Write(ax_lbl))
        self.play(Create(flat), FadeIn(flat_lbl))
        self.play(Create(smile), FadeIn(smile_lbl))
        self.wait(2)

        verdict = Text("Constant σ has been empirically violated since October 19, 1987.\n"
                       "The smile appeared after Black Monday. It has never left.",
                       color=RED, font_size=22, line_spacing=1.3)\
                      .to_edge(DOWN, buff=0.5)
        self.play(FadeIn(verdict)); self.wait(2)
        self.play(FadeOut(ax), FadeOut(ax_lbl), FadeOut(flat), FadeOut(flat_lbl),
                  FadeOut(smile), FadeOut(smile_lbl), FadeOut(verdict))

        # Extensions
        extensions = VGroup(
            VGroup(
                Text("Local Vol — Derman & Kani (1994) [15]", color=ORANGE, font_size=24, weight=BOLD),
                MathTex(r"\sigma = \sigma(S, t)", color=FG, font_size=26),
                Text("Fits the smile exactly. Loses intuition.", color=FG, font_size=20),
            ).arrange(DOWN, buff=0.15),
            VGroup(
                Text("Stochastic Vol — Heston (1993)", color=ORANGE, font_size=24, weight=BOLD),
                MathTex(r"d\sigma^2 = \kappa(\theta-\sigma^2)dt + \xi\sigma\,dW_t",
                        color=FG, font_size=24),
                Text("Vol is random. Mean-reverting. Analytically tractable (barely).", color=FG, font_size=20),
            ).arrange(DOWN, buff=0.15),
            VGroup(
                Text("Jump-Diffusion — Merton (1976) [2]", color=ORANGE, font_size=24, weight=BOLD),
                MathTex(r"dS = \mu S\,dt + \sigma S\,dB + S\,dJ_t", color=FG, font_size=24),
                Text("Adds crash risk. OTM puts now justified.", color=FG, font_size=20),
            ).arrange(DOWN, buff=0.15),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).center()
        self.play(LaggedStart(*[FadeIn(e) for e in extensions], lag_ratio=0.35))
        self.wait(2)

        irony = Text(
            '"Black-Scholes is wrong. The market quotes options IN Black-Scholes implied vol.\n'
            ' The wrong model is the language of the right market.\n'
            ' This is either profound or farcical. Possibly both."',
            color=GOLD, font_size=20, slant=ITALIC, line_spacing=1.3)\
            .to_edge(DOWN, buff=0.3)
        self.play(FadeIn(irony)); self.wait(3)


# ══════════════════════════════════════════════════════════════════════════
class SceneLessons(Scene):
    def construct(self):
        title = Text("What This Means For You — No Softening",
                     color=GOLD, font_size=36).to_edge(UP)
        sub   = Text("Axe Capital doesn't soften anything either.",
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
        for col, num, main, src in truths:
            g = VGroup(
                Text(f"{num}", color=col, font_size=36, weight=BOLD),
                VGroup(
                    Text(main, color=FG, font_size=22, line_spacing=1.3),
                    Text(src,  color=col, font_size=18, slant=ITALIC) if src else VGroup(),
                ).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
            ).arrange(RIGHT, buff=0.4).center()
            self.play(FadeIn(g)); self.wait(2.5); self.play(FadeOut(g))

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
        self.play(FadeIn(taleb)); self.wait(4)

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
        ref_grp   = VGroup(*[Text(r, color=TEAL, font_size=15) for r in refs])\
                        .arrange(DOWN, buff=0.14, aligned_edge=LEFT).center()
        self.play(FadeIn(ref_title), FadeIn(ref_grp)); self.wait(6)


# ══════════════════════════════════════════════════════════════════════════
class SceneOutro(Scene):
    def construct(self):
        logo    = Text("QUANTIFAYA", color=PURPLE, font_size=64, weight=BOLD)
        tagline = Text("Financial Engineering. Explained Rigorously. Applied Practically.",
                       color=GOLD, font_size=22).next_to(logo, DOWN, buff=0.3)
        self.play(FadeIn(logo), FadeIn(tagline)); self.wait(1)

        recap = VGroup(
            Text("✓  Option pricing problem — Bachelier to Black-Scholes", color=GREEN, font_size=20),
            Text("✓  Four assumptions and the cost of each",               color=GREEN, font_size=20),
            Text("✓  PDE derived: Itô + delta-hedge + no-arbitrage",       color=GREEN, font_size=20),
            Text("✓  Heat equation transformation and analytical solution", color=GREEN, font_size=20),
            Text("✓  Formula anatomy: N(d₁), N(d₂), d₁ vs d₂",           color=GREEN, font_size=20),
            Text("✓  Put-Call Parity in 30 seconds",                       color=GREEN, font_size=20),
            Text("✓  Risk-neutral measure Q and Fundamental Theorem",       color=GREEN, font_size=20),
            Text("✓  Vol smile, local vol, stochastic vol, jumps",         color=GREEN, font_size=20),
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
        self.play(FadeOut(recap), FadeIn(challenge)); self.wait(2)

        next_ep = VGroup(
            Text("Next on Quantifaya:", color=GOLD, font_size=30, weight=BOLD),
            Text("The Greeks — Delta, Gamma, Vega, Theta",
                 color=ORANGE, font_size=28),
            MathTex(r"\Delta=N(d_1)\quad\Gamma=\frac{N'(d_1)}{S\sigma\sqrt{T}}"
                    r"\quad\mathcal{V}=S\sqrt{T}\,N'(d_1)",
                    color=FG, font_size=26),
            Text("Why Gamma is dangerous. Why Theta bleeds every night.",
                 color=FG, font_size=22),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeOut(challenge), FadeIn(next_ep)); self.wait(3)


# ══════════════════════════════════════════════════════════════════════════
class FullEpisode(Scene):
    """
    Chains all scenes into one render.

    Full 1080p60:
        manim -pqh quantifaya_ep3.py FullEpisode --fps 60 --resolution 1920x1080

    Quick preview:
        manim -pql quantifaya_ep3.py FullEpisode

    Single scene test:
        manim -pql quantifaya_ep3.py ScenePDE
    """
    def construct(self):
        for SceneClass in [
            SceneIntro,
            SceneProblemSetup,
            SceneAssumptions,
            ScenePDE,
            SceneHeatEquation,
            SceneFormula,
            SceneRiskNeutral,
            SceneBreaks,
            SceneLessons,
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

| # | Class | Target | Key Pacing Note |
|---|---|---|---|
| 1 | SceneIntro | 1:30 | Red X over Black must land silently — hold 2 seconds |
| 2 | SceneProblemSetup | 2:30 | History panel — say all three names slowly |
| 3 | SceneAssumptions | 3:00 | One assumption at a time — don't rush the vol smile |
| 4 | ScenePDE | 4:00 | Cancellation animation is the visual climax — 3-second hold |
| 5 | SceneHeatEquation | 3:30 | "Same equation" split screen — let it breathe |
| 6 | SceneFormula | 3:00 | d₁ ≠ d₂ Itô connection — say it twice |
| 7 | SceneRiskNeutral | 2:30 | Fundamental Theorem box — hold 4 seconds |
| 8 | SceneBreaks | 2:30 | Irony panel at end — slower delivery, smile at camera |
| 9 | SceneLessons | 1:30 | Truth IV interview calibration — land each bullet hard |
| 10 | SceneOutro | 1:00 | Challenge question — speak it precisely |
| **TOTAL** | | **~25:30** | Trim pauses in Scenes 3 and 8 to hit 25 min |

---

## APPENDIX D — YOUTUBE UPLOAD CHECKLIST

```
TITLE:
Black-Scholes Formula DERIVED From Scratch | PDE → Heat Equation → Nobel Prize | Quantifaya Ep.3

DESCRIPTION (first 200 chars):
Fischer Black died before the Nobel. The formula lived on.
Today we derive it completely — PDE, heat equation, risk-neutral measure, and where it breaks.

CHAPTERS:
00:00 — The Nobel Prize That One Man Didn't Receive
01:30 — What Are We Pricing? (Options 101)
04:00 — The Four Assumptions and Their Real-World Cost
07:00 — The PDE Derivation: Itô + Delta-Hedge + No-Arbitrage
11:00 — Solving the PDE: The Heat Equation Transform
14:30 — Formula Anatomy: N(d₁), N(d₂), d₁ vs d₂
17:30 — The Risk-Neutral World and the Fundamental Theorem
20:00 — Where Black-Scholes Breaks: The Vol Smile
22:30 — Takeaways, Taleb, Full References
24:30 — Next Episode: The Greeks

TAGS:
black scholes derivation, black scholes formula explained, options pricing math,
black scholes PDE derivation, heat equation finance, risk neutral pricing explained,
ito lemma black scholes, N d1 d2 explained, put call parity proof,
implied volatility smile, volatility skew explained, delta hedging explained,
fundamental theorem asset pricing, harrison kreps 1979, quant finance,
financial engineering, derivatives pricing math, Nobel Prize finance 1997,
quant interview prep, worldquant university

THUMBNAIL BRIEF:
Left side: Clean formula in white on dark:  C = SN(d₁) − Ke^{−rT}N(d₂)
Right side: Full derivation tree (PDE → Heat Eq → Formula) in gold
Bold overlay text: "Derived From Scratch"
Red accent: "Nobel Prize. $600 Trillion. 4 Assumptions. All Wrong."
Quantifaya logo bottom-right.

PINNED COMMENT:
📌 Full reference list for this episode:
[1] Black & Scholes (1973) — J. Political Economy
[2] Merton (1973) — Bell J. Economics
[5] Bachelier (1900) — the forgotten pioneer
[6] Shreve (2004) — Stochastic Calculus for Finance II
[9] Taleb (1997) — Dynamic Hedging
Full list shown at 22:30 in the video.

🎯 Challenge: Price the cash-or-nothing digital call.
Pays $1 if S_T > K, zero otherwise. Show the derivation.
Why does only N(d₂) appear? First correct answer gets pinned!
```
