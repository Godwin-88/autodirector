# QUANTIFAYA — EPISODE 1
## "Why the Normal Distribution Fails in Finance: Fat Tails, Kurtosis & the Lies Your Risk Model Tells You"

**Channel:** Quantifaya | **Target Duration:** 25 minutes  
**Production Stack:** Python Manim (Community Edition) + TTS Voice-Over  
**SEO Title:** Why the Normal Distribution FAILS in Finance | Fat Tails & Kurtosis Explained  
**SEO Description:** Every finance textbook assumes returns are normally distributed. Every quant knows that's wrong. In this video, we build the math from scratch — probability density functions, kurtosis, excess kurtosis, VaR failures, Lévy-stable distributions, and what you should use instead. If you're studying for a quant interview, CFA, FRM, or building a trading model, this is essential.  
**SEO Tags:** normal distribution finance, fat tails explained, kurtosis finance, leptokurtic distribution, VaR failure, quant finance, financial engineering, black swan, Mandelbrot finance, Student-t distribution, Lévy distribution, quantitative finance, financial mathematics, portfolio risk, tail risk

---

## PRODUCTION NOTES FOR MANIM

**Scene class naming convention:** Each section below maps to one `Scene` class.  
**Voice-over:** Insert `self.wait()` pauses at `[PAUSE]` markers. All equations rendered with `MathTex`. All graphs use `Axes` + `ParametricFunction` or `FunctionGraph`.  
**Color palette:**
- Background: `#0D1117` (near-black)
- Primary text: `#E6EDF3` (near-white)
- Accent gold: `#F0B429`
- Danger red: `#FF4D4F`
- Safe green: `#52C41A`
- Normal curve blue: `#4C9BE8`
- Fat tail orange: `#FF7A00`
- Quantifaya brand purple: `#7C3AED`

**Manim render command:**
```bash
manim -pqh quantifaya_ep1.py FullEpisode --fps 60
```
To render individual scenes for testing:
```bash
manim -pql quantifaya_ep1.py SceneIntro
```

---

## SCENE 1: COLD OPEN — THE SHOCK HOOK
**Class:** `SceneIntro` | **Duration:** ~1:30

### MANIM ANIMATION SEQUENCE

```
1. Black screen. Single white text fades in:
   "On August 9, 2007"

2. Text transforms to:
   "Goldman Sachs lost 30% of its 'Quant Fund' in a single week."

3. Text transforms to:
   "Their models said it could only happen once every 100,000 years."

4. Big pause. Then blood-red text slams in:
   "It happened."

5. Cut to: A normal distribution curve drawn in blue on dark background.
   Label appears: "What the model assumed"
   
6. The tails of the curve animate — they GROW outward, turning orange.
   Label appears: "What the market actually did"

7. Title card animates in from bottom:
   QUANTIFAYA
   "Why the Normal Distribution Fails in Finance"
   Subtitle: "Fat Tails | Kurtosis | What Quants Actually Use"
```

### VOICE-OVER SCRIPT

"August 2007. Goldman Sachs — one of the most sophisticated quantitative trading operations on earth — watched their flagship quant fund bleed thirty percent in a single week.

Their risk models — built on decades of financial theory, PhDs, and hundreds of millions of dollars of compute — said this was a once-in-a-hundred-thousand-year event.

It wasn't.

And the reason it wasn't — the reason nearly every financial crisis in modern history was 'impossible' according to the models — comes down to one single assumption. One equation. One bell curve.

The Normal Distribution.

Welcome to Quantifaya. I'm your host — a financial engineer with degrees from WorldQuant University — and today we're going to destroy the most dangerous assumption in all of quantitative finance. And then we're going to build something better.

Let's get into it."

---

## SCENE 2: THE NORMAL DISTRIBUTION — WHAT IT IS AND WHY FINANCE ADOPTED IT
**Class:** `SceneNormalDist` | **Duration:** ~4:00

### MANIM ANIMATION SEQUENCE

```
1. Title text: "The Normal Distribution — A Love Story"
   (ironic tone, gold text)

2. Draw axes: x from -4 to +4, y from 0 to 0.45
   Label x-axis: "Return (σ units)", y-axis: "Probability Density"

3. Animate the PDF curve being drawn left to right in blue:
   f(x) = (1/√(2πσ²)) * exp(-(x-μ)²/(2σ²))

4. As curve draws, MathTex formula fades in:
   f(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)

5. Label: μ = 0, σ = 1 (standard normal)

6. Shade area between -1σ and +1σ in green, label "68.27%"
7. Shade area between -2σ and +2σ in yellow, label "95.45%"  
8. Shade area between -3σ and +3σ in orange, label "99.73%"

9. Arrow pointing to each tail: "Only 0.27% beyond ±3σ"

10. Text box appears:
    "A -5σ event has probability: 2.87 × 10⁻⁷"
    "= Once every 14,000 years (assuming daily returns)"

11. Dotted timeline: 1987 Black Monday, 1998 LTCM, 2008 GFC
    Each labeled: "5σ+", "6σ+", "25σ event (Goldman)"
    
12. Each event flashes red. Counter ticks up: "Events that 'shouldn't exist': 47+"
```

### VOICE-OVER SCRIPT

"Before we burn it down, we need to understand why the Normal Distribution became finance's default assumption in the first place.

The Normal Distribution — also called the Gaussian distribution — is described by this probability density function.

[PAUSE — show equation]

f of x equals one over the square root of two pi sigma squared, times e to the negative x minus mu, squared, over two sigma squared.

Two parameters. That's it. Mu — the mean. Sigma — the standard deviation. It's mathematically beautiful. Symmetric around the mean. And it has this incredible empirical property called the Central Limit Theorem: the average of independent random variables converges to it, regardless of the underlying distribution. That's why it appears everywhere in nature.

So in the 1950s and 60s, when Harry Markowitz was building Modern Portfolio Theory and Fischer Black and Myron Scholes were pricing options, they did what any good scientist does — they reached for the most tractable distributional assumption available. They assumed returns are normally distributed.

[PAUSE — show shaded regions]

Under this assumption, a one-sigma daily move happens 32% of the time. A two-sigma move? About 4.5% of the time. A three-sigma move? Less than 0.3%. And a five-sigma event? The probability is about 2.87 times ten to the negative seven. If you assume 252 trading days per year, that's one five-sigma event every 14,000 years.

[PAUSE — show timeline]

Except the 1987 Black Monday crash was a 22-sigma event. Long Term Capital Management's 1998 blowup involved returns beyond six sigma. And Goldman's 'quant quake' in 2007? Twenty-five sigma — on multiple consecutive days.

The model doesn't just get it slightly wrong. It gets it catastrophically wrong in precisely the scenarios where getting it right matters most — market crashes, liquidity crises, contagion events.

So why does finance keep using it? Partly inertia. Partly tractability. And partly because in calm markets, with short windows and diversified portfolios, it's a reasonable approximation.

The problem is the tails. And that's what we need to talk about."

---

## SCENE 3: MOMENTS, KURTOSIS AND THE MATHEMATICS OF FAT TAILS
**Class:** `SceneMoments` | **Duration:** ~5:00

### MANIM ANIMATION SEQUENCE

```
1. Title: "The Four Moments — What Your Distribution Is Hiding"

2. Build a 2x2 grid, each cell animating in sequence:

   CELL 1 — Mean (1st moment):
   E[X] = \mu = \int_{-\infty}^{\infty} x \, f(x) \, dx
   Label: "Where are returns centered?"

   CELL 2 — Variance (2nd moment):
   \text{Var}(X) = \sigma^2 = E[(X - \mu)^2]
   Label: "How spread out are returns?"

   CELL 3 — Skewness (3rd standardized moment):
   \gamma_1 = \frac{E[(X-\mu)^3]}{\sigma^3}
   Label: "Are losses bigger than gains? (usually yes)"

   CELL 4 — Kurtosis (4th standardized moment):
   \kappa = \frac{E[(X-\mu)^4]}{\sigma^4}
   Label: "How fat are the tails?"

3. Highlight CELL 4 with gold border — this is the star today

4. New panel: "Excess Kurtosis (Fisher's definition)"
   \kappa_{\text{excess}} = \frac{E[(X-\mu)^4]}{\sigma^4} - 3

5. Annotation: "Why subtract 3? Because the Normal Distribution has kurtosis = 3 exactly."
   Proof shown:
   \kappa_{\text{Normal}} = \frac{3\sigma^4}{\sigma^4} = 3

6. Score card animates:
   | Distribution      | Excess Kurtosis |
   |-------------------|-----------------|
   | Normal            | 0               |
   | Student-t (ν=5)   | 6               |
   | Student-t (ν=4)   | ∞ (undefined!)  |
   | S&P 500 daily ret.| ~4 to 7         |
   | BTC daily returns | ~12+            |

7. Term appears: "LEPTOKURTIC"
   Arrow pointing: "Excess kurtosis > 0 → fatter tails than Normal"

8. Side-by-side curves:
   Left: Normal (blue, thin tails)
   Right: Leptokurtic (orange, fatter tails, higher peak)
   Both have same σ. Show the tails zoomed in 10x.
   Gap between them highlighted in red: "THIS is where crashes live"
```

### VOICE-OVER SCRIPT

"To understand fat tails mathematically, we need to talk about moments. Not moments in time — statistical moments. These are summary statistics that describe the shape of a distribution.

[PAUSE — show 2x2 grid building]

The first moment is the mean — where are returns centered on average. The second moment is variance — how dispersed are returns around that mean. The third standardized moment is skewness — whether the distribution is symmetric or if one tail is longer than the other. And the fourth standardized moment is kurtosis — and this is today's protagonist.

[PAUSE — highlight kurtosis]

Kurtosis is defined as the expected value of X minus mu to the fourth power, divided by sigma to the fourth. More precisely, we work with excess kurtosis — sometimes called Fisher's kurtosis — which subtracts three.

[PAUSE — show excess kurtosis formula]

Why subtract three? Because when you compute kurtosis for the Normal Distribution exactly, you get three. So excess kurtosis measures how much heavier your tails are compared to Normal. Excess kurtosis of zero — Normal. Greater than zero — your distribution is leptokurtic, meaning it has fatter tails and a higher, sharper peak than Normal.

[PAUSE — show table]

Now look at real data. The S&P 500 daily returns have excess kurtosis somewhere between four and seven, depending on the sample period. Bitcoin? Often above twelve. Student-t distributions with few degrees of freedom can have infinite kurtosis. Infinite — meaning no finite fourth moment exists.

And here's the critical consequence.

[PAUSE — show side-by-side curves with zoomed tails]

When you zoom into the tails of a leptokurtic distribution versus the Normal, you see the gap. That gap — that seemingly tiny strip of extra probability mass out in the extreme tails — is where five-sigma events live. Is where twenty-five sigma events live. Is where every financial crisis in modern history lives.

The Normal Distribution assigns these regions a probability indistinguishable from zero. Real financial returns do not.

This is not a minor calibration error. This is a model that is fundamentally, architecturally wrong about the most important part of the distribution."

---

## SCENE 4: EMPIRICAL EVIDENCE — SHOWING REAL RETURN DATA
**Class:** `SceneEmpiricalEvidence` | **Duration:** ~4:00

### MANIM ANIMATION SEQUENCE

```
1. Title: "Let the Data Speak"

2. Simulated histogram of daily S&P 500 returns (use stylized bars)
   x-axis: -8% to +8%, y-axis: Frequency
   Color: steel blue bars

3. Overlay Normal Distribution curve fitted to same mean and σ
   Color: blue curve

4. The histogram bars in the tails are dramatically TALLER than the normal curve
   Highlight bars beyond ±3% in red
   Label: "Normal predicts: nearly zero"
   Label: "Reality: these happen regularly"

5. Zoom into right tail. Show:
   Normal PDF at x=4σ: f(4σ) ≈ 1.34 × 10⁻⁴
   Real data frequency at x=4σ: ~10× higher

6. Introduce Q-Q Plot (Quantile-Quantile):
   Axes: x = "Theoretical Normal Quantile", y = "Empirical Quantile"
   If returns were Normal → straight diagonal line
   Real data Q-Q plot → S-shape, with tails curling ABOVE the line
   Label the curl: "Fat tail deviation"

7. Historical events pinned to the distribution:
   - Black Monday 1987: arrow → "22σ under Normal assumptions"
   - LTCM 1998: "6σ+"
   - Dot-com bust 2000–2002: "clustered 4σ+ moves"  
   - GFC 2008: "7σ+ single days"
   - COVID March 2020: "8σ event (March 16)"
   - Quant Quake 2007: "25σ (Goldman)"

8. Text: "If returns were truly Normal, none of these should have occurred in recorded human history."

9. Split screen comparison:
   Left panel: "Normal World"  — calm sine wave
   Right panel: "Real Markets" — jagged volatile line with spikes
```

### VOICE-OVER SCRIPT

"Theory is one thing. Let's look at what the data actually shows.

[PAUSE — show histogram]

Here's a stylized histogram of daily S&P 500 returns — the kind of empirical distribution you get when you pull decades of price data. The x-axis is daily return, the y-axis is frequency. I've overlaid the Normal Distribution fitted to the same mean and standard deviation.

See the problem immediately? The bars in the middle are roughly in line with the curve — that's fine. But look at the tails. The empirical bars extend well beyond where the Normal Distribution says there should be almost no probability. The bars in the tails are taller than the curve. Sometimes dramatically so.

[PAUSE — zoom into tail]

At four sigma, the Normal Distribution predicts a probability density of roughly 1.34 times ten to the negative four. Real equity return data at that level is typically ten times more frequent. And at five, six, seven sigma, the gap becomes astronomically large.

[PAUSE — show Q-Q plot]

There's a standard diagnostic tool for this — the Quantile-Quantile plot, or Q-Q plot. If your data were perfectly Normal, every point would fall on this straight diagonal line. What we actually see with financial return data is an S-shape — and crucially, the tails curl above the line. That curl is the signature of fat tails. The empirical distribution puts more probability mass in the extremes than Normal predicts.

[PAUSE — pin historical events]

And now we can locate every major market crisis on this distribution. Black Monday 1987 — twenty-two sigma under Normal assumptions. LTCM in 1998 — beyond six sigma. The Global Financial Crisis of 2008 produced multiple single-day moves beyond seven sigma. The COVID crash of March 16th, 2020 — eight sigma. Goldman's quant quake — twenty-five sigma on multiple consecutive days.

Under a Normal Distribution, each of these events has a probability so small it should never occur in the entire age of the universe — let alone in a single century of stock market history.

And yet here they are. Every decade. Like clockwork.

The data is telling us something the models refuse to hear."

---

## SCENE 5: WHY THE TAILS ARE FAT — THE MECHANISMS
**Class:** `SceneMechanisms` | **Duration:** ~3:30

### MANIM ANIMATION SEQUENCE

```
1. Title: "Why Do Fat Tails Exist? — Three Real Mechanisms"

2. MECHANISM 1 — Volatility Clustering (GARCH effects)
   Show two time series side by side:
   Left: i.i.d. Normal returns — uniform scatter
   Right: GARCH(1,1) process — calm periods, then explosive bursts
   
   Equation for GARCH(1,1):
   \sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2 + \beta \sigma_{t-1}^2
   
   Text: "Volatility is NOT constant. High-vol periods cluster together.
          This alone generates fat tails even with conditionally Normal shocks."

3. MECHANISM 2 — Jumps (Discontinuous Price Processes)
   Show smooth Brownian motion path (blue)
   Overlay: same path but with sudden jumps (orange spikes)
   
   Merton (1976) Jump-Diffusion:
   dS_t = \mu S_t \, dt + \sigma S_t \, dW_t + S_t \, dJ_t
   
   where J_t is a compound Poisson process with jump intensity λ
   
   Text: "Real prices can gap — earnings shocks, geopolitical events,
          circuit breakers. Continuous diffusion can't capture this."

4. MECHANISM 3 — Correlation Breakdown & Contagion
   Show correlation matrix in calm times: most off-diagonals near 0
   Show correlation matrix in crisis: ALL correlations spike to near 1
   
   Stylized heatmap transition: greens → deep reds
   
   Text: "Diversification disappears precisely when you need it most.
          The portfolio assumption of independence fails in crises."

5. Combine: three arrows pointing to one box:
   "Result: Empirical return distributions are:
    ✓ Leptokurtic (fat tails)
    ✓ Negatively skewed (larger left tail)  
    ✓ Heteroskedastic (time-varying volatility)
    ✗ NOT i.i.d. Normal"
```

### VOICE-OVER SCRIPT

"So now we know the Normal Distribution fails, and we've seen the empirical evidence. But *why* do fat tails exist? What generates them mechanically in financial markets?

There are three key mechanisms, and understanding them matters for building better models.

[PAUSE — show Mechanism 1]

First: volatility clustering. This is the GARCH effect — named for the Generalized Autoregressive Conditional Heteroskedasticity model developed by Tim Bollerslev in 1986. In real markets, volatility is not constant. Large moves tend to cluster together. A turbulent day is followed by more turbulent days. A calm period begets calm. 

[PAUSE — show GARCH equation]

In GARCH(1,1), today's variance depends on yesterday's squared shock and yesterday's variance — a feedback loop. Even if individual shocks are conditionally Normal, the unconditional distribution — what you observe over time — has fat tails. This mechanism alone is powerful enough to generate much of the excess kurtosis we observe in equity returns.

[PAUSE — show Mechanism 2]

Second: jumps. The standard Black-Scholes model assumes prices follow a continuous diffusion — Geometric Brownian Motion. But real prices jump. A company misses earnings and gaps down fifteen percent overnight. A central bank surprises the market. A geopolitical shock hits. 

[PAUSE — show jump-diffusion equation]

Robert Merton's 1976 jump-diffusion model augments standard Brownian motion with a compound Poisson jump process. The jump intensity lambda controls how often jumps arrive. These discontinuities are impossible to hedge continuously, and they inject extreme outcomes into the tail of the return distribution.

[PAUSE — show Mechanism 3]

Third, and perhaps most insidious: correlation breakdown. In normal markets, assets in a diversified portfolio have modest correlations. The diversification benefit is real. But in crises, correlations spike dramatically — often approaching one across all asset classes simultaneously.

[PAUSE — show heatmap transition]

This is the cruel joke of financial risk. The moment a tail event occurs is the exact moment your diversification vanishes. Assets you thought were independent move together, amplifying losses across your portfolio far beyond what any Normal-based model predicted.

These three mechanisms — volatility clustering, jumps, and correlation breakdown — combine to generate the fat-tailed, negatively skewed, heteroskedastic reality of financial returns. The Normal Distribution assumes none of them."

---

## SCENE 6: THE VaR DISASTER — WHERE THIS KILLS REAL PORTFOLIOS
**Class:** `SceneVaR` | **Duration:** ~3:00

### MANIM ANIMATION SEQUENCE

```
1. Title: "Value at Risk — The Metric Built on a Lie"

2. Definition panel:
   "Value at Risk (VaR) at confidence level α:"
   \text{VaR}_\alpha = -\inf\{x \in \mathbb{R} : F_X(x) > 1 - \alpha\}
   
   Plain English: "The loss you will NOT exceed with probability α"
   Example: "95% 1-day VaR = $1M means: on 95% of days, you lose less than $1M"

3. Normal-based VaR calculation:
   \text{VaR}_{95\%} = \mu - 1.645\,\sigma
   \text{VaR}_{99\%} = \mu - 2.326\,\sigma
   \text{VaR}_{99.9\%} = \mu - 3.090\,\sigma
   
   These z-scores come from the Normal quantile function.

4. Side-by-side: Normal VaR vs Fat-Tail VaR
   Same σ. Two distribution tails shown.
   At 99% confidence:
   Normal VaR: $X
   Actual (Student-t, ν=4) VaR: $1.8X
   
   Red bracket showing the UNDERESTIMATION gap.
   Label: "VaR gap — the loss the model doesn't see"

5. Real-world consequence diagram:
   Bank A uses Normal VaR → holds $100M capital
   Reality (fat tails) → needs $180M capital
   Gap: $80M UNDERCAPITALIZED
   Flash: "Basel II / III VaR backtesting requirements"

6. CVaR (Conditional VaR / Expected Shortfall) introduced:
   \text{CVaR}_\alpha = E[X \mid X \leq -\text{VaR}_\alpha]
   
   "The average loss IN the tail — not just the threshold"
   Show how CVaR captures the tail shape; VaR does not.

7. Text: "Basel III / FRTB (2016) moved from VaR to Expected Shortfall.
           Regulators figured this out. Has your model?"
```

### VOICE-OVER SCRIPT

"Now let's translate this mathematical failure into something tangible: Value at Risk — the dominant risk metric used by banks, hedge funds, and regulators worldwide.

[PAUSE — show definition]

VaR at confidence level alpha is formally defined as the negative of the infimum of x such that the CDF of X exceeds one minus alpha. In plain English — the VaR at 95% confidence is the number such that on 95% of trading days, your loss will be smaller. It's a quantile of the loss distribution.

[PAUSE — show Normal-based VaR formulas]

Under a Normal Distribution, computing VaR is trivial. The 95% one-day VaR is simply mu minus 1.645 sigma. The 99% VaR is mu minus 2.326 sigma. These z-scores come straight from the Normal quantile table. Simple. Fast. Analytically clean.

And catastrophically wrong.

[PAUSE — show comparison]

Compare Normal VaR to the VaR from a Student-t distribution with four degrees of freedom — a distribution with fat tails but the same mean and standard deviation. At 99% confidence, the fat-tail VaR is roughly 1.8 times larger. That gap — that red bracket — represents losses the Normal model simply cannot see. Cannot price. Cannot reserve capital for.

[PAUSE — show bank example]

In practice, this means a trading desk using Normal VaR might believe it needs $100 million in capital to cover its tail risk. The actual fat-tailed distribution of its positions requires $180 million. That $80 million gap is not a rounding error. It's the gap between solvency and failure in a crisis.

[PAUSE — show CVaR]

This is why we have Conditional Value at Risk — also called Expected Shortfall. CVaR is the expected loss conditional on being in the tail — the average loss when things go very wrong, not just the threshold. It integrates the shape of the tail rather than just reading off a single quantile.

And it's worth noting: regulators figured this out. The Basel III Fundamental Review of the Trading Book, adopted in 2016, mandated a shift from VaR to Expected Shortfall as the primary capital measure precisely because VaR under-captures tail risk.

The question is whether your models caught up."

---

## SCENE 7: BETTER DISTRIBUTIONS — WHAT QUANTS ACTUALLY USE
**Class:** `SceneBetterModels` | **Duration:** ~4:00

### MANIM ANIMATION SEQUENCE

```
1. Title: "So What Do We Use Instead?"

2. OPTION 1 — Student-t Distribution
   
   PDF:
   f(x;\nu) = \frac{\Gamma\!\left(\frac{\nu+1}{2}\right)}{\sqrt{\nu\pi}\;\Gamma\!\left(\frac{\nu}{2}\right)}
   \left(1+\frac{x^2}{\nu}\right)^{-\frac{\nu+1}{2}}
   
   Animation: Draw curves for ν = 3, 5, 10, 30, ∞ (→ Normal)
   As ν increases, curve converges to Normal in blue.
   ν = 3–5: noticeably fatter tails in orange.
   
   Key property: Excess kurtosis = 6/(ν-4) for ν > 4
   At ν = 5: excess kurtosis = 6
   At ν = 4: excess kurtosis → ∞
   At ν ≤ 2: variance undefined
   
   Text: "MLE fitting ν to equity returns typically yields ν ≈ 3–6"
   "Goldman's model (pre-2007): ν ≈ 6. Still too thin-tailed."

3. OPTION 2 — Stable / Lévy-Stable Distributions (Mandelbrot's insight)
   
   Characteristic function (no closed-form PDF in general):
   \varphi(t) = \exp\!\left(i\mu t - |ct|^\alpha(1 - i\beta\,\text{sgn}(t)\tan\frac{\pi\alpha}{2})\right)
   
   Parameters: α ∈ (0,2] (tail index), β (skewness), c (scale), μ (location)
   α = 2 → Normal distribution
   α = 1 → Cauchy distribution (NO finite mean, NO finite variance)
   
   Text: "Mandelbrot (1963): cotton prices follow Lévy-stable with α ≈ 1.7"
   "Power-law tails: P(X > x) ~ x^{-α}"
   
   Visual: log-log plot showing Normal tail (curves down rapidly) vs power-law tail (straight line)

4. OPTION 3 — GARCH-based Models
   Reminder of GARCH(1,1):
   \varepsilon_t = \sigma_t z_t, \quad z_t \sim \text{i.i.d.}(0,1)
   \sigma_t^2 = \omega + \alpha_1 \varepsilon_{t-1}^2 + \beta_1 \sigma_{t-1}^2
   
   Extension: GJR-GARCH (asymmetric — leverage effect)
   \sigma_t^2 = \omega + (\alpha + \gamma \mathbf{1}_{[\varepsilon_{t-1}<0]})\varepsilon_{t-1}^2 + \beta \sigma_{t-1}^2
   
   Text: "Combine GARCH volatility with Student-t innovations = industry standard"

5. Comparison table animates:
   | Model          | Tail Thickness | Skew | Vol Clustering | Jump |
   |----------------|---------------|------|----------------|------|
   | Normal         | Thin          | No   | No             | No   |
   | Student-t      | Fat           | No   | No             | No   |
   | Lévy-Stable    | Very Fat      | Yes  | No             | No   |
   | GARCH-Normal   | Moderate      | No   | Yes            | No   |
   | GARCH-t        | Fat           | No   | Yes            | No   |
   | Jump-Diffusion | Fat           | Yes  | No             | Yes  |
   | Full Model     | Fat           | Yes  | Yes            | Yes  |

6. "The full model" lights up green at the bottom.
```

### VOICE-OVER SCRIPT

"Alright — we've established the problem rigorously. Now let's talk solutions. What do actual quants and risk models use?

[PAUSE — show Student-t]

The first and most accessible upgrade is the Student-t distribution. Originally developed for small-sample statistical testing, it has found a permanent home in quantitative finance because of one key property: its tails decay as a power law rather than exponentially.

[PAUSE — show PDF and curves]

The probability density function involves the Gamma function and a single extra parameter — nu, the degrees of freedom. As nu increases, the distribution converges to Normal. At nu equals five, the excess kurtosis is six. At nu equals four, excess kurtosis is theoretically infinite. At nu of three or below, the variance itself becomes undefined.

When practitioners fit the Student-t to equity return data using maximum likelihood estimation, they typically find nu between three and six. Goldman Sachs's models in 2007 reportedly used around six degrees of freedom — still underestimating the true tail thickness, as 2007 demonstrated.

[PAUSE — show Lévy-stable / Mandelbrot]

The second class of models takes Benoit Mandelbrot's insight from 1963 — that financial data follows Lévy-stable distributions, not Normal. The characteristic function of a Lévy-stable distribution has four parameters — alpha, the tail index, controls how heavy the tails are. When alpha equals two, you recover the Normal. When alpha equals one, you get the Cauchy distribution, which has no finite mean and no finite variance at all.

[PAUSE — show power-law tail on log-log plot]

The key visual insight is on a log-log plot. The Normal tail curves downward rapidly — exponential decay. A power-law tail — the signature of Lévy-stable distributions — appears as a straight line. That straight line represents dramatically more probability mass at extreme values. Mandelbrot's empirical estimate for cotton prices was an alpha of about 1.7 — comfortably in fat-tail territory.

[PAUSE — show GARCH models]

The third approach, and the current industry standard, combines GARCH volatility dynamics with fat-tailed innovations. The standard GARCH with Student-t errors captures both the clustering mechanism — why volatility persists — and the tail thickness within each period. Extend to GJR-GARCH and you also capture the leverage effect — the asymmetry where negative shocks hit volatility harder than positive ones.

[PAUSE — show comparison table]

No single model captures everything. The comparison table shows the tradeoffs. If you want to be closest to the full complexity of real markets — fat tails, asymmetry, volatility clustering, and occasional jumps — you need a model that combines all four features."

---

## SCENE 8: THE REAL LESSON — WHAT THIS MEANS FOR YOU AS A QUANT
**Class:** `SceneLessons` | **Duration:** ~3:00

### MANIM ANIMATION SEQUENCE

```
1. Title: "The Practical Takeaways — For Your Models, Your Career, Your Risk"

2. THREE COMMANDMENTS of Fat-Tail Awareness — appear one by one:

   COMMANDMENT I:
   Icon: histogram
   "Never assume Normal returns for risk calculations.
    Always fit and test the distributional assumption.
    Run Jarque-Bera, Kolmogorov-Smirnov, or Anderson-Darling tests."
   
   Jarque-Bera statistic:
   JB = \frac{n}{6}\!\left(\gamma_1^2 + \frac{(\kappa-3)^2}{4}\right)
   
   "Under H₀ of Normality, JB ~ χ²(2)"

   COMMANDMENT II:
   Icon: shield
   "Use Expected Shortfall (CVaR), not VaR, for tail risk.
    ES captures the shape of the tail. VaR just reads a quantile.
    Basel III agrees with you."
   
   \text{ES}_\alpha = \frac{1}{1-\alpha}\int_\alpha^1 \text{VaR}_u \, du

   COMMANDMENT III:
   Icon: brain
   "Model your volatility, don't assume it's constant.
    A GARCH(1,1)-t model with 4 parameters outperforms
    Normal i.i.d. assumptions in virtually every backtesting study."

3. BONUS — Stress Testing philosophy:
   "Your model's job in calm markets: approximate.
    Your model's job in crises: survive.
    Build for the tail. The body takes care of itself."

4. Checklist fades in:
   □ Test for fat tails in your return data (excess kurtosis > 0?)
   □ Use t-distribution or GARCH-t for volatility modeling
   □ Report CVaR alongside VaR
   □ Run scenario analysis beyond 3σ
   □ Do NOT calibrate only on recent calm data (recency bias = tail blindness)

5. Quote appears in gold:
   "Markets can remain irrational longer than you can remain solvent."
   — John Maynard Keynes
   
   "But models can remain wrong longer than you can remain employed."
   — Quantifaya
```

### VOICE-OVER SCRIPT

"So what do we take away from all of this? Three practical commandments for every quant, risk manager, and serious investor.

[PAUSE — show Commandment I]

First: test your distributional assumption. Never assume normality for risk calculations without empirically verifying it. The Jarque-Bera test — which jointly tests whether the skewness and excess kurtosis of your data are consistent with Normal — is fast and easy to implement. Under the null hypothesis of normality, the JB statistic follows a chi-squared distribution with two degrees of freedom. If your p-value is small, your data isn't Normal. That's not a minor issue. That's a mandate to use a different distribution.

[PAUSE — show Commandment II]

Second: switch to Expected Shortfall. The formula for ES at confidence level alpha is the integral of VaR from alpha to one, divided by one minus alpha. It's the average loss across the entire tail beyond your VaR threshold. Unlike VaR, it's sensitive to how bad the bad days actually are — not just how many of them there are. It's also subadditive — it respects portfolio diversification in a way that VaR does not. Basel III mandated Expected Shortfall for a reason.

[PAUSE — show Commandment III]

Third: model your volatility. A GARCH(1,1) with Student-t innovations has four parameters — omega, alpha, beta, and nu. That's just four parameters. And it consistently, dramatically outperforms Normal i.i.d. assumptions in out-of-sample backtesting studies across every major equity market. The cost of ignoring volatility clustering is large. The cost of fitting a four-parameter model is negligible.

[PAUSE — show checklist]

Practically speaking: every time you build a return model, run through this checklist. Compute your excess kurtosis. Test for normality. Model volatility with GARCH or at minimum report CVaR alongside VaR. Do not calibrate exclusively on recent data — recency bias creates tail blindness. And always stress test beyond three sigma.

[PAUSE — show quotes]

Keynes said markets can remain irrational longer than you can remain solvent. I'll add a corollary for quants: models can remain wrong longer than you can remain employed.

Build for the tail."

---

## SCENE 9: OUTRO — CHANNEL CTA & NEXT EPISODE TEASE
**Class:** `SceneOutro` | **Duration:** ~1:00

### MANIM ANIMATION SEQUENCE

```
1. Quantifaya logo pulses in brand purple. Channel tagline:
   "Financial Engineering. Explained Rigorously. Applied Practically."

2. Episode summary recap — bullets fly in from left:
   ✓ Normal Distribution PDF and its assumptions
   ✓ Kurtosis, excess kurtosis, and leptokurtic distributions
   ✓ Empirical evidence: Q-Q plots and historical crises
   ✓ Three mechanisms generating fat tails
   ✓ VaR failure and the CVaR upgrade
   ✓ Student-t, Lévy-stable, and GARCH-t alternatives

3. Book recommendation appears with cover placeholder:
   📚 "The (Mis)behaviour of Markets" — Benoit Mandelbrot & Richard Hudson
   "This is the book that exposed the Normal Distribution's lie in finance.
    Link in description — your library needs this."

4. Next episode tease:
   Equation flashes: dS = μS dt + σS dW_t
   Text: "Next Week on Quantifaya:"
   "Itô's Lemma — What It Actually Means"
   "How the most important equation in derivatives pricing was discovered
    and why your calculus intuition completely breaks down in continuous time."

5. Subscribe button animation. Comment prompt:
   "Drop a comment: What's the most extreme sigma-event you've 
    personally witnessed in the markets?"

6. End card — dark background, Quantifaya logo, social handles.
```

### VOICE-OVER SCRIPT

"That's a wrap on Episode One of Quantifaya.

[PAUSE — show recap]

We covered a lot of ground today. We started with the Normal Distribution — its PDF, its assumptions, why finance adopted it. We built the mathematics of moments and kurtosis from the ground up. We looked at the empirical evidence in real return data — the Q-Q plots, the histograms, the historical crises that should be impossible but keep happening. We explored the three mechanisms — GARCH clustering, jumps, and correlation breakdown — that generate fat tails in practice. We dissected the VaR failure and built the CVaR solution. And we surveyed the better distributional models: Student-t, Lévy-stable, and GARCH-t.

[PAUSE — book recommendation]

If you want to go deeper, the single best book on this topic is Benoit Mandelbrot and Richard Hudson's 'The Misbehaviour of Markets.' Mandelbrot spent fifty years proving that financial returns follow power laws, not bells. It's readable, rigorous, and genuinely important. Link is in the description.

[PAUSE — next episode tease]

Next week, we're building Itô's Lemma from the ground up — the mathematical engine behind Black-Scholes, interest rate models, and virtually every derivative pricing formula in existence. We'll show exactly why classical calculus breaks in continuous time and what stochastic calculus does instead.

Subscribe so you don't miss it. Drop a comment below — what's the most extreme sigma event you've personally lived through in the markets? I want to hear from you.

This is Quantifaya. See you next week."

---

## APPENDIX A — FULL EQUATION REFERENCE

| Equation | LaTeX | Scene |
|---|---|---|
| Normal PDF | `f(x)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)` | 2 |
| Kurtosis | `\kappa=\frac{E[(X-\mu)^4]}{\sigma^4}` | 3 |
| Excess Kurtosis | `\kappa_{\text{excess}}=\frac{E[(X-\mu)^4]}{\sigma^4}-3` | 3 |
| Student-t PDF | `f(x;\nu)=\frac{\Gamma(\frac{\nu+1}{2})}{\sqrt{\nu\pi}\,\Gamma(\frac{\nu}{2})}\!\left(1+\frac{x^2}{\nu}\right)^{-\frac{\nu+1}{2}}` | 7 |
| GARCH(1,1) | `\sigma_t^2=\omega+\alpha\varepsilon_{t-1}^2+\beta\sigma_{t-1}^2` | 5, 7 |
| Jump-Diffusion | `dS_t=\mu S_t\,dt+\sigma S_t\,dW_t+S_t\,dJ_t` | 5 |
| VaR (Normal) 95% | `\text{VaR}_{95\%}=\mu-1.645\sigma` | 6 |
| Formal VaR | `\text{VaR}_\alpha=-\inf\{x:F_X(x)>1-\alpha\}` | 6 |
| CVaR / ES | `\text{ES}_\alpha=\frac{1}{1-\alpha}\int_\alpha^1\text{VaR}_u\,du` | 6, 8 |
| Lévy-Stable CF | `\varphi(t)=\exp\!\left(i\mu t-\|ct\|^\alpha(1-i\beta\,\text{sgn}(t)\tan\frac{\pi\alpha}{2})\right)` | 7 |
| Jarque-Bera | `JB=\frac{n}{6}\!\left(\gamma_1^2+\frac{(\kappa-3)^2}{4}\right)` | 8 |
| GJR-GARCH | `\sigma_t^2=\omega+(\alpha+\gamma\mathbf{1}_{[\varepsilon_{t-1}<0]})\varepsilon_{t-1}^2+\beta\sigma_{t-1}^2` | 7 |

---

## APPENDIX B — MANIM SCENE CLASS SKELETON

```python
# quantifaya_ep1.py
# Run: manim -pqh quantifaya_ep1.py FullEpisode --fps 60

from manim import *

# ── BRAND COLOURS ──────────────────────────────────────
BG        = "#0D1117"
FG        = "#E6EDF3"
GOLD      = "#F0B429"
RED       = "#FF4D4F"
GREEN     = "#52C41A"
BLUE_NORM = "#4C9BE8"
ORANGE_FT = "#FF7A00"
PURPLE    = "#7C3AED"

config.background_color = BG

# ── SCENE 1 ────────────────────────────────────────────
class SceneIntro(Scene):
    def construct(self):
        # Hook text
        t1 = Text("On August 9, 2007", color=FG, font_size=48)
        self.play(FadeIn(t1)); self.wait(2)

        t2 = Text("Goldman Sachs lost 30% of its Quant Fund\nin a single week.",
                  color=FG, font_size=36, line_spacing=1.4)
        self.play(Transform(t1, t2)); self.wait(2)

        t3 = Text("Their models said:\nonce every 100,000 years.",
                  color=FG, font_size=36, line_spacing=1.4)
        self.play(Transform(t1, t3)); self.wait(2)

        shock = Text("IT HAPPENED.", color=RED, font_size=72, weight=BOLD)
        self.play(FadeOut(t1), FadeIn(shock)); self.wait(2)
        self.play(FadeOut(shock))

        # Normal curve with growing fat tails
        ax = Axes(x_range=[-5,5,1], y_range=[0,0.45,0.1],
                  x_length=10, y_length=5,
                  axis_config={"color": FG})
        normal = ax.plot(lambda x: np.exp(-x**2/2)/np.sqrt(2*PI),
                         color=BLUE_NORM, stroke_width=3)
        lbl_normal = Text("What the model assumed", color=BLUE_NORM, font_size=24)\
                         .next_to(ax, UP)
        self.play(Create(ax), Create(normal), FadeIn(lbl_normal))
        self.wait(1)

        fat = ax.plot(lambda x: (1 + x**2/4)**(-5/2) * 0.88,
                      color=ORANGE_FT, stroke_width=3)
        lbl_fat = Text("What the market actually did", color=ORANGE_FT, font_size=24)\
                      .next_to(lbl_normal, DOWN)
        self.play(Create(fat), FadeIn(lbl_fat))
        self.wait(2)

        # Title card
        title = VGroup(
            Text("QUANTIFAYA", color=PURPLE, font_size=56, weight=BOLD),
            Text("Why the Normal Distribution Fails in Finance",
                 color=GOLD, font_size=32),
            Text("Fat Tails  |  Kurtosis  |  What Quants Actually Use",
                 color=FG, font_size=24)
        ).arrange(DOWN, buff=0.4).to_edge(DOWN, buff=0.5)
        self.play(FadeOut(ax), FadeOut(normal), FadeOut(fat),
                  FadeOut(lbl_normal), FadeOut(lbl_fat),
                  FadeIn(title))
        self.wait(3)


# ── SCENE 2 ────────────────────────────────────────────
class SceneNormalDist(Scene):
    def construct(self):
        title = Text("The Normal Distribution — A Love Story",
                     color=GOLD, font_size=38).to_edge(UP)
        self.play(FadeIn(title))

        ax = Axes(x_range=[-4,4,1], y_range=[0,0.45,0.1],
                  x_length=10, y_length=5,
                  axis_config={"color": FG},
                  x_axis_config={"numbers_to_include": range(-4,5)},
                  y_axis_config={"numbers_to_include": [0.1,0.2,0.3,0.4]})
        ax.add_coordinates()
        labels = ax.get_axis_labels(
            x_label=Tex(r"Return $(\sigma)$", color=FG),
            y_label=Tex(r"f(x)", color=FG))

        pdf = ax.plot(lambda x: np.exp(-x**2/2)/np.sqrt(2*PI),
                      color=BLUE_NORM, stroke_width=3)
        pdf_label = MathTex(
            r"f(x)=\frac{1}{\sqrt{2\pi\sigma^2}}"
            r"\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)",
            color=FG, font_size=28).to_corner(UR).shift(LEFT*0.5)

        self.play(Create(ax), Write(labels))
        self.play(Create(pdf), FadeIn(pdf_label))
        self.wait(1)

        # Shaded regions
        for (lo, hi, col, pct) in [(-1,1,GREEN,"68.27%"),
                                    (-2,2,YELLOW,"95.45%"),
                                    (-3,3,ORANGE,"99.73%")]:
            region = ax.get_area(pdf, x_range=[lo,hi], color=col, opacity=0.3)
            lbl = Text(pct, color=col, font_size=22).move_to(ax.c2p((lo+hi)/2, 0.25))
            self.play(FadeIn(region), FadeIn(lbl))
            self.wait(0.5)

        # Sigma event table
        sigma_box = VGroup(
            Text("5σ event probability: 2.87 × 10⁻⁷", color=RED, font_size=22),
            Text("≈ Once every 14,000 trading years", color=RED, font_size=22),
        ).arrange(DOWN, buff=0.2).to_corner(DL).shift(RIGHT*0.3+UP*0.3)
        self.play(FadeIn(sigma_box))
        self.wait(2)

        # Historical crisis pins
        events = [
            (-4.8, 0.05, "Black Monday '87\n22σ"),
            (-4.2, 0.08, "LTCM '98\n6σ+"),
            (-4.5, 0.03, "GFC 2008\n7σ+"),
            (-4.6, 0.02, "Quant Quake '07\n25σ"),
        ]
        for (xv, yv, lbl) in events:
            dot = Dot(ax.c2p(xv, yv), color=RED)
            t = Text(lbl, color=RED, font_size=16).next_to(dot, UP, buff=0.1)
            self.play(FadeIn(dot), FadeIn(t), run_time=0.5)
        self.wait(3)


# ── SCENE 3 ────────────────────────────────────────────
class SceneMoments(Scene):
    def construct(self):
        title = Text("The Four Moments", color=GOLD, font_size=40).to_edge(UP)
        self.play(FadeIn(title))

        equations = [
            (r"E[X]=\mu=\int_{-\infty}^{\infty}x\,f(x)\,dx",
             "Mean — where returns center"),
            (r"\text{Var}(X)=\sigma^2=E[(X-\mu)^2]",
             "Variance — spread of returns"),
            (r"\gamma_1=\frac{E[(X-\mu)^3]}{\sigma^3}",
             "Skewness — tail asymmetry"),
            (r"\kappa=\frac{E[(X-\mu)^4]}{\sigma^4}",
             "Kurtosis — tail thickness ★"),
        ]
        grid = VGroup()
        for eq, desc in equations:
            box = VGroup(
                MathTex(eq, color=FG, font_size=26),
                Text(desc, color=GOLD if "★" in desc else FG,
                     font_size=18, slant=ITALIC)
            ).arrange(DOWN, buff=0.15)
            rect = SurroundingRectangle(
                box, color=(GOLD if "★" in desc else FG),
                buff=0.2, stroke_width=(3 if "★" in desc else 1))
            grid.add(VGroup(rect, box))

        grid.arrange_in_grid(rows=2, cols=2, buff=0.5).shift(DOWN*0.3)
        for g in grid:
            self.play(FadeIn(g), run_time=0.6)
        self.wait(1)

        # Excess kurtosis
        self.play(FadeOut(grid), FadeOut(title))
        ek_title = Text("Excess Kurtosis (Fisher)", color=GOLD, font_size=36).to_edge(UP)
        ek_eq = MathTex(
            r"\kappa_{\text{excess}}=\frac{E[(X-\mu)^4]}{\sigma^4}-3",
            color=FG, font_size=40)
        proof = MathTex(
            r"\kappa_{\text{Normal}}=\frac{3\sigma^4}{\sigma^4}=3",
            color=BLUE_NORM, font_size=32).next_to(ek_eq, DOWN, buff=0.4)
        why = Text("Subtracting 3 benchmarks against the Normal",
                   color=FG, font_size=22).next_to(proof, DOWN, buff=0.3)
        self.play(FadeIn(ek_title), Write(ek_eq))
        self.play(FadeIn(proof), FadeIn(why))
        self.wait(2)

        # Kurtosis comparison table
        table_data = [
            ["Distribution", "Excess Kurtosis"],
            ["Normal", "0"],
            ["Student-t  (ν=10)", "1"],
            ["Student-t  (ν=5)", "6"],
            ["Student-t  (ν=4)", "∞"],
            ["S&P 500 daily", "~4–7"],
            ["Bitcoin daily", "~12+"],
        ]
        tbl = Table(table_data,
                    include_outer_lines=True,
                    line_config={"color": FG, "stroke_width": 1},
                    element_to_mobject_config={"color": FG, "font_size": 22}
                    ).scale(0.7).to_edge(DOWN)
        self.play(FadeOut(proof), FadeOut(why), FadeOut(ek_eq), FadeOut(ek_title))
        self.play(Create(tbl))
        self.wait(3)


# ── SCENE 4 ────────────────────────────────────────────
class SceneEmpiricalEvidence(Scene):
    def construct(self):
        title = Text("Let the Data Speak", color=GOLD, font_size=40).to_edge(UP)
        self.play(FadeIn(title))

        ax = Axes(x_range=[-8,8,2], y_range=[0,0.6,0.1],
                  x_length=11, y_length=5,
                  axis_config={"color":FG})
        # Simulate stylised histogram bars
        import numpy as np
        bars = VGroup()
        np.random.seed(42)
        xs = np.linspace(-7.5, 7.5, 16)
        # Fat-tailed heights (stylised Student-t density)
        def student_t_pdf(x, nu=4):
            from scipy.special import gamma as G
            coeff = G((nu+1)/2) / (np.sqrt(nu*np.pi)*G(nu/2))
            return coeff * (1 + x**2/nu)**(-(nu+1)/2)

        for xi in xs:
            h = student_t_pdf(xi, nu=4) * 3.5
            bar = Rectangle(
                width=0.6, height=max(h*4, 0.02),
                fill_color=BLUE_NORM, fill_opacity=0.7,
                stroke_color=FG, stroke_width=0.5)
            bar.move_to(ax.c2p(xi, h*2))
            if abs(xi) > 4:
                bar.set_fill(RED, opacity=0.85)
            bars.add(bar)

        normal_curve = ax.plot(
            lambda x: np.exp(-x**2/2)/np.sqrt(2*np.pi)*3.5,
            color=BLUE_NORM, stroke_width=3)

        self.play(Create(ax))
        self.play(Create(bars))
        self.play(Create(normal_curve))

        lbl_tail = Text("Tails: reality >> Normal prediction",
                        color=RED, font_size=22).to_corner(UR).shift(LEFT*0.3)
        self.play(FadeIn(lbl_tail))
        self.wait(2)

        # Q-Q plot schematic
        self.play(FadeOut(ax), FadeOut(bars), FadeOut(normal_curve),
                  FadeOut(lbl_tail), FadeOut(title))
        qq_title = Text("Q-Q Plot: Normal vs Real Returns", color=GOLD, font_size=34).to_edge(UP)
        ax2 = Axes(x_range=[-3,3,1], y_range=[-3,3,1],
                   x_length=6, y_length=6,
                   axis_config={"color": FG})
        ax2_labels = ax2.get_axis_labels(
            Tex(r"Theoretical Quantile", color=FG, font_size=20),
            Tex(r"Empirical Quantile", color=FG, font_size=20))
        diag = ax2.plot(lambda x: x, color=FG, stroke_width=2,
                        stroke_opacity=0.5)
        # S-curve for fat tails
        fat_qq = ax2.plot(lambda x: x + 0.4*x**3/9,
                          x_range=[-2.5,2.5], color=ORANGE_FT, stroke_width=3)
        fat_lbl = Text("Real returns (fat tails)", color=ORANGE_FT, font_size=20)\
                      .to_corner(UR).shift(LEFT*0.3+DOWN*0.3)
        normal_lbl = Text("Perfect Normal → diagonal", color=FG, font_size=20)\
                         .to_corner(DL).shift(RIGHT*0.3+UP*0.3)
        curl_arrow = Arrow(ax2.c2p(2,2.4), ax2.c2p(2.2, 2.7),
                           color=ORANGE_FT, stroke_width=2)
        curl_lbl = Text("Fat tail\ncurl", color=ORANGE_FT, font_size=18)\
                       .next_to(curl_arrow, RIGHT, buff=0.1)

        self.play(FadeIn(qq_title), Create(ax2), Write(ax2_labels))
        self.play(Create(diag), FadeIn(normal_lbl))
        self.play(Create(fat_qq), FadeIn(fat_lbl))
        self.play(Create(curl_arrow), FadeIn(curl_lbl))
        self.wait(3)


# ── SCENE 5 ────────────────────────────────────────────
class SceneMechanisms(Scene):
    def construct(self):
        title = Text("Why Do Fat Tails Exist? — Three Mechanisms",
                     color=GOLD, font_size=34).to_edge(UP)
        self.play(FadeIn(title))

        # Mechanism 1 — GARCH
        m1_title = Text("① Volatility Clustering (GARCH)", color=ORANGE_FT, font_size=28)
        m1_eq = MathTex(
            r"\sigma_t^2=\omega+\alpha\varepsilon_{t-1}^2+\beta\sigma_{t-1}^2",
            color=FG, font_size=30)
        m1_desc = Text("Volatility is NOT constant — it clusters.\nThis alone generates fat tails.",
                       color=FG, font_size=20, line_spacing=1.3)
        m1 = VGroup(m1_title, m1_eq, m1_desc).arrange(DOWN, buff=0.3).shift(UP*0.5)
        self.play(FadeIn(m1))
        self.wait(2)
        self.play(FadeOut(m1))

        # Mechanism 2 — Jumps
        m2_title = Text("② Jump Processes (Merton 1976)", color=ORANGE_FT, font_size=28)
        m2_eq = MathTex(
            r"dS_t=\mu S_t\,dt+\sigma S_t\,dW_t+S_t\,dJ_t",
            color=FG, font_size=30)
        m2_desc = Text("Real prices gap: earnings shocks, central bank surprises.\nContinuous diffusion cannot capture discontinuities.",
                       color=FG, font_size=20, line_spacing=1.3)
        m2 = VGroup(m2_title, m2_eq, m2_desc).arrange(DOWN, buff=0.3).shift(UP*0.5)
        self.play(FadeIn(m2))
        self.wait(2)
        self.play(FadeOut(m2))

        # Mechanism 3 — Correlation breakdown
        m3_title = Text("③ Correlation Breakdown in Crises", color=ORANGE_FT, font_size=28)
        m3_desc = Text("In calm markets: correlations ≈ 0\n"
                       "In crises: correlations → 1 simultaneously\n"
                       "Diversification vanishes exactly when needed most.",
                       color=FG, font_size=22, line_spacing=1.4)
        m3 = VGroup(m3_title, m3_desc).arrange(DOWN, buff=0.4).shift(UP*0.5)
        self.play(FadeIn(m3))
        self.wait(2)
        self.play(FadeOut(m3))

        # Summary
        result_box = VGroup(
            Text("Result: Real Return Distributions Are...", color=GOLD, font_size=26),
            Text("✓  Leptokurtic (fat tails)", color=GREEN, font_size=22),
            Text("✓  Negatively skewed (larger left tail)", color=GREEN, font_size=22),
            Text("✓  Heteroskedastic (time-varying volatility)", color=GREEN, font_size=22),
            Text("✗  NOT i.i.d. Normal", color=RED, font_size=22),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).center()
        self.play(FadeIn(result_box))
        self.wait(3)


# ── SCENE 6 ────────────────────────────────────────────
class SceneVaR(Scene):
    def construct(self):
        title = Text("Value at Risk — The Metric Built on a Lie",
                     color=GOLD, font_size=36).to_edge(UP)
        self.play(FadeIn(title))

        var_def = MathTex(
            r"\text{VaR}_\alpha=-\inf\{x\in\mathbb{R}:F_X(x)>1-\alpha\}",
            color=FG, font_size=30)
        plain = Text("The loss you will NOT exceed with probability α",
                     color=FG, font_size=22, slant=ITALIC)
        normal_vars = VGroup(
            MathTex(r"\text{VaR}_{95\%}=\mu-1.645\,\sigma", color=BLUE_NORM, font_size=28),
            MathTex(r"\text{VaR}_{99\%}=\mu-2.326\,\sigma", color=BLUE_NORM, font_size=28),
            MathTex(r"\text{VaR}_{99.9\%}=\mu-3.090\,\sigma", color=BLUE_NORM, font_size=28),
        ).arrange(DOWN, buff=0.2)

        block = VGroup(var_def, plain, normal_vars).arrange(DOWN, buff=0.35).shift(UP*0.5)
        self.play(Write(var_def))
        self.play(FadeIn(plain))
        self.play(FadeIn(normal_vars))
        self.wait(2)
        self.play(FadeOut(block))

        # Gap visualisation
        gap_title = Text("The VaR Gap — What Normal Misses", color=RED, font_size=30)
        gap_data = VGroup(
            Text("Normal VaR @ 99%:   $1.00M", color=BLUE_NORM, font_size=26),
            Text("Fat-tail VaR @ 99%: $1.80M", color=ORANGE_FT, font_size=26),
            Text("GAP:   $0.80M UNDERCAPITALISED", color=RED, font_size=28, weight=BOLD),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        gap_group = VGroup(gap_title, gap_data).arrange(DOWN, buff=0.4).center()
        self.play(FadeIn(gap_group))
        self.wait(2)
        self.play(FadeOut(gap_group))

        # CVaR
        cvar_title = Text("Expected Shortfall (CVaR) — The Fix",
                          color=GREEN, font_size=30).to_edge(UP).shift(DOWN*0.5)
        cvar_eq = MathTex(
            r"\text{ES}_\alpha=\frac{1}{1-\alpha}\int_\alpha^1\text{VaR}_u\,du",
            color=FG, font_size=36)
        cvar_desc = Text(
            "Average loss IN the tail — integrates the tail shape.\n"
            "Basel III / FRTB (2016) mandated ES over VaR.",
            color=FG, font_size=22, line_spacing=1.3)
        cvar_block = VGroup(cvar_title, cvar_eq, cvar_desc).arrange(DOWN, buff=0.4).center()
        self.play(FadeIn(cvar_block))
        self.wait(3)


# ── SCENE 7 ────────────────────────────────────────────
class SceneBetterModels(Scene):
    def construct(self):
        title = Text("So What Do We Use Instead?", color=GOLD, font_size=40).to_edge(UP)
        self.play(FadeIn(title))

        # Student-t
        st_title = Text("① Student-t Distribution", color=ORANGE_FT, font_size=28)
        st_eq = MathTex(
            r"f(x;\nu)=\frac{\Gamma\!\left(\frac{\nu+1}{2}\right)}"
            r"{\sqrt{\nu\pi}\,\Gamma\!\left(\frac{\nu}{2}\right)}"
            r"\!\left(1+\frac{x^2}{\nu}\right)^{-\frac{\nu+1}{2}}",
            color=FG, font_size=26)
        st_kurt = MathTex(
            r"\kappa_{\text{excess}}=\frac{6}{\nu-4}\quad(\nu>4)",
            color=GOLD, font_size=26)
        st_block = VGroup(st_title, st_eq, st_kurt).arrange(DOWN, buff=0.3).shift(UP*0.5)
        self.play(FadeIn(st_block))

        # Draw Student-t curves on axes
        ax = Axes(x_range=[-5,5,1], y_range=[0,0.45,0.1],
                  x_length=9, y_length=3.5,
                  axis_config={"color":FG}).to_edge(DOWN)
        curves = {
            3: RED,
            5: ORANGE_FT,
            10: YELLOW,
            30: GREEN,
        }
        for nu, col in curves.items():
            from scipy.special import gamma as G
            coeff = G((nu+1)/2) / (np.sqrt(nu*np.pi)*G(nu/2))
            curve = ax.plot(lambda x, n=nu: G((n+1)/2)/(np.sqrt(n*np.pi)*G(n/2))
                            * (1+x**2/n)**(-(n+1)/2),
                            color=col, stroke_width=2)
            lbl = Text(f"ν={nu}", color=col, font_size=16).move_to(ax.c2p(3.5, 0.05+nu*0.002))
            self.play(Create(curve), FadeIn(lbl), run_time=0.5)
        normal_c = ax.plot(lambda x: np.exp(-x**2/2)/np.sqrt(2*np.pi),
                           color=BLUE_NORM, stroke_width=3, stroke_opacity=0.7)
        self.play(Create(normal_c))
        self.wait(2)
        self.play(FadeOut(st_block), FadeOut(ax), FadeOut(normal_c))

        # Lévy-Stable
        ls_title = Text("② Lévy-Stable Distributions (Mandelbrot 1963)",
                        color=ORANGE_FT, font_size=26)
        ls_eq = MathTex(
            r"\varphi(t)=\exp\!\left(i\mu t-|ct|^\alpha"
            r"\!\left(1-i\beta\,\text{sgn}(t)\tan\frac{\pi\alpha}{2}\right)\right)",
            color=FG, font_size=24)
        ls_note = VGroup(
            Text("α=2 → Normal | α=1 → Cauchy (no finite mean!)", color=GOLD, font_size=20),
            Text("P(X>x) ~ x⁻ᵅ  (power-law tail)", color=GOLD, font_size=20),
        ).arrange(DOWN, buff=0.15)
        ls_block = VGroup(ls_title, ls_eq, ls_note).arrange(DOWN, buff=0.3).center()
        self.play(FadeIn(ls_block))
        self.wait(2)
        self.play(FadeOut(ls_block))

        # GARCH-t
        gt_title = Text("③ GARCH-t — The Industry Standard", color=ORANGE_FT, font_size=28)
        gt_eq1 = MathTex(r"\varepsilon_t=\sigma_t z_t,\quad z_t\sim t_\nu",
                         color=FG, font_size=28)
        gt_eq2 = MathTex(r"\sigma_t^2=\omega+\alpha\varepsilon_{t-1}^2+\beta\sigma_{t-1}^2",
                         color=FG, font_size=28)
        gt_gjr = MathTex(
            r"\sigma_t^2=\omega+(\alpha+\gamma\mathbf{1}_{[\varepsilon_{t-1}<0]})"
            r"\varepsilon_{t-1}^2+\beta\sigma_{t-1}^2",
            color=GOLD, font_size=24)
        gt_block = VGroup(gt_title, gt_eq1, gt_eq2, gt_gjr).arrange(DOWN, buff=0.3).center()
        self.play(FadeIn(gt_block))
        self.wait(3)


# ── SCENE 8 ────────────────────────────────────────────
class SceneLessons(Scene):
    def construct(self):
        title = Text("Three Commandments for Every Quant",
                     color=GOLD, font_size=36).to_edge(UP)
        self.play(FadeIn(title))

        # Commandment I
        c1 = VGroup(
            Text("Ⅰ  Test Your Distribution", color=ORANGE_FT, font_size=26, weight=BOLD),
            MathTex(r"JB=\frac{n}{6}\!\left(\gamma_1^2+\frac{(\kappa-3)^2}{4}\right)\sim\chi^2(2)",
                    color=FG, font_size=26),
            Text("Reject H₀ → your data is not Normal → use a different model",
                 color=FG, font_size=20),
        ).arrange(DOWN, buff=0.25).shift(UP*1.5)
        self.play(FadeIn(c1)); self.wait(2)

        # Commandment II
        c2 = VGroup(
            Text("Ⅱ  Use Expected Shortfall, Not VaR", color=ORANGE_FT, font_size=26, weight=BOLD),
            MathTex(r"\text{ES}_\alpha=\frac{1}{1-\alpha}\int_\alpha^1\text{VaR}_u\,du",
                    color=FG, font_size=26),
            Text("Basel III mandated ES in 2016. Your risk report should too.",
                 color=FG, font_size=20),
        ).arrange(DOWN, buff=0.25).next_to(c1, DOWN, buff=0.4)
        self.play(FadeIn(c2)); self.wait(2)

        # Commandment III
        c3 = VGroup(
            Text("Ⅲ  Model Your Volatility", color=ORANGE_FT, font_size=26, weight=BOLD),
            Text("GARCH(1,1)-t: 4 parameters, massive improvement over i.i.d. Normal",
                 color=FG, font_size=20),
        ).arrange(DOWN, buff=0.25).next_to(c2, DOWN, buff=0.4)
        self.play(FadeIn(c3)); self.wait(2)

        self.play(FadeOut(c1), FadeOut(c2), FadeOut(c3), FadeOut(title))

        # Final quote
        q1 = Text('"Markets can remain irrational\nlonger than you can remain solvent."',
                  color=GOLD, font_size=28, slant=ITALIC, line_spacing=1.4)
        q1_attr = Text("— John Maynard Keynes", color=FG, font_size=20).next_to(q1, DOWN)
        q2 = Text('"Models can remain wrong\nlonger than you can remain employed."',
                  color=ORANGE_FT, font_size=28, slant=ITALIC, line_spacing=1.4)
        q2_attr = Text("— Quantifaya", color=FG, font_size=20).next_to(q2, DOWN)
        quotes = VGroup(q1, q1_attr, q2, q2_attr).arrange(DOWN, buff=0.5).center()
        self.play(FadeIn(quotes))
        self.wait(4)


# ── SCENE 9 — OUTRO ───────────────────────────────────
class SceneOutro(Scene):
    def construct(self):
        logo = Text("QUANTIFAYA", color=PURPLE, font_size=64, weight=BOLD)
        tagline = Text("Financial Engineering. Explained Rigorously. Applied Practically.",
                       color=GOLD, font_size=22)
        self.play(FadeIn(logo), FadeIn(tagline.next_to(logo, DOWN, buff=0.3)))
        self.wait(1)

        recap = VGroup(
            Text("✓  Normal Distribution PDF & assumptions", color=GREEN, font_size=20),
            Text("✓  Kurtosis, excess kurtosis, leptokurtic distributions", color=GREEN, font_size=20),
            Text("✓  Empirical evidence: Q-Q plots & historical crises", color=GREEN, font_size=20),
            Text("✓  Three fat-tail mechanisms (GARCH, Jumps, Correlation)", color=GREEN, font_size=20),
            Text("✓  VaR failure and the CVaR upgrade", color=GREEN, font_size=20),
            Text("✓  Student-t, Lévy-stable, and GARCH-t alternatives", color=GREEN, font_size=20),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(LEFT).shift(DOWN*0.5)
        self.play(FadeOut(logo), FadeOut(tagline))
        self.play(LaggedStart(*[FadeIn(r) for r in recap], lag_ratio=0.15))
        self.wait(2)

        next_ep = VGroup(
            Text("Next Episode:", color=GOLD, font_size=30, weight=BOLD),
            MathTex(r"dS=\mu S\,dt+\sigma S\,dW_t", color=FG, font_size=36),
            Text("Itô's Lemma — What It Actually Means", color=ORANGE_FT, font_size=28),
        ).arrange(DOWN, buff=0.3).center()
        self.play(FadeOut(recap))
        self.play(FadeIn(next_ep))
        self.wait(3)


# ── FULL EPISODE COMPOSITOR ────────────────────────────
class FullEpisode(Scene):
    """
    Renders all scenes back-to-back into one file.
    Each sub-scene is instantiated and its animations are
    replayed in this scene's construct().
    
    For a 25-minute video, render at 1080p60:
        manim -pqh quantifaya_ep1.py FullEpisode --fps 60 --resolution 1920x1080
    
    For a quick preview at 480p:
        manim -pql quantifaya_ep1.py FullEpisode
    """
    def construct(self):
        scenes = [
            SceneIntro,
            SceneNormalDist,
            SceneMoments,
            SceneEmpiricalEvidence,
            SceneMechanisms,
            SceneVaR,
            SceneBetterModels,
            SceneLessons,
            SceneOutro,
        ]
        for SceneClass in scenes:
            instance = SceneClass()
            instance.camera = self.camera
            instance.renderer = self.renderer
            instance.construct()
            self.wait(0.5)
```

---

## APPENDIX C — VOICE-OVER TIMING GUIDE

| Scene | Class | Target Duration | Key Pauses |
|---|---|---|---|
| 1 | SceneIntro | 1:30 | After each text transform; after fat tail appears |
| 2 | SceneNormalDist | 4:00 | After PDF eq; after each shaded region; after crisis pins |
| 3 | SceneMoments | 5:00 | After each cell in 2x2; after excess kurtosis formula; after table |
| 4 | SceneEmpiricalEvidence | 4:00 | After histogram; after Q-Q curve; after each crisis pin |
| 5 | SceneMechanisms | 3:30 | After each mechanism equation; after summary box |
| 6 | SceneVaR | 3:00 | After VaR definition; after gap visualization; after CVaR equation |
| 7 | SceneBetterModels | 4:00 | After each model class; after comparison table |
| 8 | SceneLessons | 3:00 | After each commandment; after final quote |
| 9 | SceneOutro | 1:00 | After recap; after next episode tease |
| **TOTAL** | | **~29:00** | *(trim pauses for 25 min target)* |

---

## APPENDIX D — YOUTUBE UPLOAD CHECKLIST

```
Title:
Why the Normal Distribution FAILS in Finance | Fat Tails & Kurtosis Explained | Quantifaya

Description (first 200 chars — shown before "more"):
Every quant model assumes Normal returns. Every financial crisis proves that wrong.
Today we build the fat-tail math from scratch. Episode 1 of Quantifaya.

Chapters (paste into description):
00:00 — The Goldman Sachs 25-Sigma Shock
01:30 — The Normal Distribution: PDF and Assumptions
05:30 — Moments, Kurtosis and Excess Kurtosis
10:30 — Empirical Evidence: Q-Q Plots and Real Crisis Data
14:30 — Why Fat Tails Exist: 3 Mechanisms
18:00 — VaR Failure and Expected Shortfall
21:00 — Better Models: Student-t, Lévy-Stable, GARCH-t
25:00 — Three Commandments for Every Quant
28:00 — Next Episode: Itô's Lemma

Tags:
normal distribution finance, fat tails explained, kurtosis finance, excess kurtosis,
leptokurtic distribution, value at risk failure, expected shortfall CVaR,
GARCH model explained, Student t distribution finance, Lévy stable distribution,
Mandelbrot finance, Black Monday 1987, quant finance, financial engineering,
quantitative finance, portfolio risk, tail risk, financial mathematics,
WorldQuant, quant interview prep, CFA FRM exam

Thumbnail text:
"The Bell Curve is a Lie" — Your Risk Model is WRONG
(use split image: calm blue bell curve vs jagged orange fat-tail spike)

End screen: Subscribe + next video card (Itô's Lemma episode)
Pinned comment: "Book recommendation: The Misbehaviour of Markets by Mandelbrot"
```
