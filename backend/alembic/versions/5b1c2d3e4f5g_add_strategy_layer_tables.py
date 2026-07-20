"""Add strategy layer tables (pillars, planned_episodes, schedule_overrides)

Revision ID: 5b1c2d3e4f5g
Revises: 4a1b2c3d4e5f
Create Date: 2026-07-20 09:15:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from uuid import uuid4

revision = "5b1c2d3e4f5g"
down_revision = "4a1b2c3d4e5f"
branch_labels = None
depends_on = None


def upgrade():
    # ── PILLARS TABLE ────────────────────────────────────────────────
    op.create_table(
        "pillars",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("series", sa.String(50), nullable=False, server_default="quantifaya"),
        sa.Column("pillar_number", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("code", sa.String(10), nullable=False),
        sa.Column("publish_day", sa.String(20), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("color", sa.String(20), server_default="#F0B429"),
        sa.Column("active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
        sa.UniqueConstraint("series", "pillar_number"),
    )

    # ── PLANNED EPISODES TABLE ──────────────────────────────────────
    op.create_table(
        "planned_episodes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("pillar_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("pillars.id"), nullable=False),
        sa.Column("sequence_number", sa.Integer(), nullable=False),
        sa.Column("topic", sa.String(500), nullable=False),
        sa.Column("suggested_title", sa.String(500), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("target_date", sa.Date(), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="planned"),
        sa.Column("episode_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("episodes.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
        sa.UniqueConstraint("pillar_id", "sequence_number"),
    )

    # ── SCHEDULE OVERRIDES TABLE ────────────────────────────────────
    op.create_table(
        "schedule_overrides",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("target_date", sa.Date(), nullable=False, unique=True),
        sa.Column("planned_episode_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("planned_episodes.id"), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
    )

    # ── SEED PILLARS (5 Quantifaya pillars) ─────────────────────────
    pillars_table = sa.table(
        "pillars",
        sa.column("id", postgresql.UUID),
        sa.column("series", sa.String),
        sa.column("pillar_number", sa.Integer),
        sa.column("name", sa.String),
        sa.column("code", sa.String),
        sa.column("publish_day", sa.String),
        sa.column("description", sa.String),
        sa.column("color", sa.String),
        sa.column("active", sa.Boolean),
    )

    pillar_data = [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "series": "quantifaya",
            "pillar_number": 1,
            "name": "The Math Behind the Market",
            "code": "P1",
            "publish_day": "monday",
            "description": "Pure financial mathematics explained with intuition. Targets finance students, CFA candidates, and self-taught traders.",
            "color": "#3B82F6",
            "active": True,
        },
        {
            "id": "00000000-0000-0000-0000-000000000002",
            "series": "quantifaya",
            "pillar_number": 2,
            "name": "WorldQuant to Wall Street",
            "code": "P2",
            "publish_day": "tuesday",
            "description": "Career-first content. Highest monetization pillar — aspiring quants.",
            "color": "#10B981",
            "active": True,
        },
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "series": "quantifaya",
            "pillar_number": 3,
            "name": "DeFi × Quant",
            "code": "P3",
            "publish_day": "wednesday",
            "description": "Blue ocean content bridging rigorous financial engineering with DeFi math.",
            "color": "#F59E0B",
            "active": True,
        },
        {
            "id": "00000000-0000-0000-0000-000000000004",
            "series": "quantifaya",
            "pillar_number": 4,
            "name": "Systematic Strategies Unpacked",
            "code": "P4",
            "publish_day": "thursday",
            "description": "Live strategy breakdowns. Drives highest watch time.",
            "color": "#EF4444",
            "active": True,
        },
        {
            "id": "00000000-0000-0000-0000-000000000005",
            "series": "quantifaya",
            "pillar_number": 5,
            "name": "Quant Book Club",
            "code": "P5",
            "publish_day": "friday",
            "description": "Deep book reviews from a quant perspective. Direct book sales engine.",
            "color": "#8B5CF6",
            "active": True,
        },
    ]
    op.bulk_insert(pillars_table, pillar_data)

    # ── SEED PLANNED EPISODES (25 per pillar) ────────────────────────
    # P1: The Math Behind the Market (Monday)
    # P2: WorldQuant to Wall Street (Tuesday)
    # P3: DeFi × Quant (Wednesday)
    # P4: Systematic Strategies Unpacked (Thursday)
    # P5: Quant Book Club (Friday)

    episodes_table = sa.table(
        "planned_episodes",
        sa.column("id", postgresql.UUID),
        sa.column("pillar_id", postgresql.UUID),
        sa.column("sequence_number", sa.Integer),
        sa.column("topic", sa.String),
        sa.column("suggested_title", sa.String),
        sa.column("status", sa.String),
    )
    episode_seed_data = []

    p1_topics = [
        ("Why the Normal Distribution Fails in Finance", "Why the Normal Distribution Fails in Finance — Fat Tails, Kurtosis"),
        ("Itô's Lemma — What It Actually Means", "Itô's Lemma — What It Actually Means (Geometric Brownian Motion)"),
        ("Black-Scholes Derived From Scratch", "Black-Scholes Derived From Scratch"),
        ("The Greeks: Delta, Gamma, Vega — Built Intuitively", "The Greeks: Delta, Gamma, Vega — Built Intuitively"),
        ("Stochastic Calculus Without the Terror", "Stochastic Calculus Without the Terror"),
        ("The Efficient Frontier — Markowitz Done Right", "The Efficient Frontier — Markowitz Done Right"),
        ("Risk Parity: The Math Kelly Criterion Won't Tell You", "Risk Parity: The Math Kelly Criterion Won't Tell You"),
        ("Fixed Income Math — Duration, Convexity, DV01", "Fixed Income Math — Duration, Convexity, DV01"),
        ("The Kalman Filter in Trading", "The Kalman Filter in Trading (State-Space Models)"),
        ("PCA for Portfolio Construction", "PCA for Portfolio Construction"),
        ("Cointegration vs. Correlation — Why Quants Care", "Cointegration vs. Correlation — Why Quants Care"),
        ("The Heston Model — When Volatility Has Volatility", "The Heston Model — When Volatility Has Volatility"),
        ("SABR Model Explained", "SABR Model Explained"),
        ("Yield Curve Modeling", "Yield Curve Modeling (Nelson-Siegel, Vasicek)"),
        ("CVaR vs VaR — Why VaR Fails in Tails", "CVaR vs VaR — Why VaR Fails in Tails"),
        ("Copulas and Tail Dependence", "Copulas and Tail Dependence"),
        ("Moment Generating Functions in Risk", "Moment Generating Functions in Risk"),
        ("Characteristic Functions and Option Pricing", "Characteristic Functions and Option Pricing"),
        ("The Feynman-Kac Formula", "The Feynman-Kac Formula"),
        ("Girsanov's Theorem — Change of Measure", "Girsanov's Theorem — Change of Measure"),
        ("Monte Carlo in 25 Minutes", "Monte Carlo in 25 Minutes (Variance Reduction)"),
        ("FFT Option Pricing", "FFT Option Pricing (Carr-Madan)"),
        ("GARCH Models — Volatility Clustering", "GARCH Models — Volatility Clustering"),
        ("Markov Chains in Credit Risk", "Markov Chains in Credit Risk"),
        ("Entropy in Finance", "Entropy in Finance (Maximum Entropy Portfolios)"),
    ]

    p2_topics = [
        ("What Financial Engineers Actually Do", "What Financial Engineers Actually Do Day-to-Day"),
        ("How WorldQuant's Alpha Research Works", "How WorldQuant's Alpha Research Works (What I Learned)"),
        ("The Quant Interview Breakdown", "The Quant Interview Breakdown (Math, Stats, Brainteasers)"),
        ("How to Build Your First Alpha Factor", "How to Build Your First Alpha Factor"),
        ("Quant vs Quant Dev vs Risk Quant", "Quant vs. Quant Dev vs. Risk Quant — Which Role Fits You?"),
        ("The Honest Salary Guide for Financial Engineers", "The Honest Salary Guide for Financial Engineers"),
        ("How to Read a Research Paper in Quant Finance", "How to Read a Research Paper in Quant Finance"),
        ("Building a Quant Portfolio From Scratch", "Building a Quant Portfolio From Scratch (GitHub Strategy)"),
        ("What MSFE Programs Don't Teach You", "What MSFE Programs Don't Teach You"),
        ("How to Network into Hedge Funds From Africa", "How to Network into Hedge Funds From Africa/Emerging Markets"),
        ("CFA vs FRM vs MSFE", "CFA vs FRM vs MSFE — Which Credential Actually Pays"),
        ("The Tools Every Quant Must Know", "The Tools Every Quant Must Know (Python, Julia, R, Bloomberg)"),
        ("Getting Remote Quant Work as a Non-US/UK Resident", "Getting Remote Quant Work as a Non-US/UK Resident"),
        ("Breaking into DeFi Quant from Traditional Finance", "Breaking into DeFi Quant from Traditional Finance"),
        ("How I Would Start Over If I Were 22", "How I Would Start Over If I Were 22 (Honest Roadmap)"),
    ]

    p3_topics = [
        ("AMM Math — How Uniswap V3 Actually Works", "AMM Math — How Uniswap V3 Actually Works"),
        ("Impermanent Loss — The Real Formula", "Impermanent Loss — The Real Formula"),
        ("Options Pricing on DeFi", "Options Pricing on DeFi (Lyra, Hegic, Dopex Explained)"),
        ("Zero-Knowledge Proofs for Finance People", "Zero-Knowledge Proofs for Finance People (No CS Degree Needed)"),
        ("KYC Compliance Without Revealing Identity", "KYC Compliance Without Revealing Identity — ZK-KYC Explained"),
        ("DeFi Yield Curves — Are They Real?", "DeFi Yield Curves — Are They Real?"),
        ("On-Chain Risk Management", "On-Chain Risk Management (Liquidation Math, Collateral Ratios)"),
        ("Flash Loans as Arbitrage", "Flash Loans as Arbitrage — The Quant View"),
        ("MEV — Market Microstructure on Chain", "MEV (Maximal Extractable Value) — Market Microstructure on Chain"),
        ("Stablecoin Mechanics", "Stablecoin Mechanics — USDC vs DAI vs Algorithmic"),
        ("Cross-Chain Bridges — Risk Pricing", "Cross-Chain Bridges — Risk Pricing"),
        ("Tokenomics as Financial Engineering", "Tokenomics as Financial Engineering"),
        ("DeFi Portfolio Construction", "DeFi Portfolio Construction (Correlations, Rebalancing)"),
        ("Smart Contract Auditing from a Quant Risk Lens", "Smart Contract Auditing from a Quant Risk Lens"),
        ("The Future of Quant Finance on Blockchain", "The Future of Quant Finance on Blockchain"),
    ]

    p4_topics = [
        ("Pairs Trading — Full Implementation", "Pairs Trading — Full Implementation Walk-Through"),
        ("Momentum Factor — Why It Works", "Momentum Factor — Why It Works and When It Doesn't"),
        ("The Low Volatility Anomaly", "The Low Volatility Anomaly"),
        ("Statistical Arbitrage in 25 Minutes", "Statistical Arbitrage in 25 Minutes"),
        ("Trend Following — The Math", "Trend Following (CTA-Style) — The Math"),
        ("Risk Parity Strategy Built from Scratch", "Risk Parity Strategy Built from Scratch"),
        ("Mean Reversion on Crypto vs Equities", "Mean Reversion on Crypto vs. Equities"),
        ("Kelly Criterion — Sizing Bets Correctly", "Kelly Criterion — Sizing Your Bets Correctly"),
        ("Walk-Forward Backtesting with Embargo Gap", "Walk-Forward Backtesting with Embargo Gap (Your MScFE Method)"),
        ("How Funds Avoid Overfitting", "How Funds Avoid Overfitting (Combinatorial Purged CV)"),
        ("CNN-GAF for Price Pattern Recognition", "CNN-GAF for Price Pattern Recognition (Your GWP1 Work)"),
        ("Ensemble Models in Systematic Trading", "Ensemble Models in Systematic Trading"),
        ("Building a Factor Zoo", "Building a Factor Zoo — Which Factors Survive"),
        ("Market Regime Detection", "Market Regime Detection (HMM, Clustering)"),
        ("Portfolio Rebalancing", "Portfolio Rebalancing — Costs, Taxes, Slippage"),
    ]

    p5_topics = [
        ("Options, Futures and Other Derivatives — Hull", "Book: Options, Futures and Other Derivatives — Hull"),
        ("The Concepts and Practice of Mathematical Finance — Joshi", "Book: The Concepts and Practice of Mathematical Finance — Joshi"),
        ("Quantitative Risk Management — McNeil, Frey, Embrechts", "Book: Quantitative Risk Management — McNeil, Frey, Embrechts"),
        ("Machine Learning for Asset Managers — López de Prado", "Book: Machine Learning for Asset Managers — López de Prado"),
        ("Python for Finance — Yves Hilpisch", "Book: Python for Finance — Yves Hilpisch"),
        ("The Mathematics of Financial Derivatives — Wilmott", "Book: The Mathematics of Financial Derivatives — Wilmott"),
        ("Inside the Black Box — Narang", "Book: Inside the Black Box — Narang"),
        ("When Genius Failed — Lowenstein", "Book: When Genius Failed — Lowenstein"),
        ("The Big Short — Lewis (Deconstructed for Quants)", "Book: The Big Short — Lewis (Deconstructed for Quants)"),
        ("Heard on the Street — Crack", "Book: Heard on the Street — Crack (Interview Prep)"),
        ("Paul Wilmott on Quantitative Finance", "Book: Paul Wilmott on Quantitative Finance"),
        ("Stochastic Calculus for Finance — Shreve", "Book: Stochastic Calculus for Finance — Shreve"),
        ("My Life as a Quant — Derman", "Book: My Life as a Quant — Derman"),
        ("The Quant — Patterson", "Book: The Quant — Patterson"),
        ("How to Be a Quant — Joshi", "Book: How to Be a Quant — Joshi"),
        ("DeFi and the Future of Finance — Harvey et al.", "Book: DeFi and the Future of Finance — Harvey et al."),
        ("Mastering Ethereum — Antonopoulos", "Book: Mastering Ethereum — Antonopoulos"),
        ("Advances in Financial Machine Learning — López de Prado", "Book: Advances in Financial Machine Learning — López de Prado"),
        ("Systematic Trading — Carver", "Book: Systematic Trading — Carver"),
        ("Active Portfolio Management — Grinold & Kahn", "Book: Active Portfolio Management — Grinold & Kahn"),
        ("The Black-Scholes Model — Historical Context", "Book: The Black-Scholes Model — Historical Context"),
        ("Fixed Income Analysis — Fabozzi", "Book: Fixed Income Analysis — Fabozzi"),
        ("Dynamic Hedging — Taleb", "Book: Dynamic Hedging — Taleb"),
        ("Financial Calculus — Baxter & Rennie", "Book: Financial Calculus — Baxter & Rennie"),
        ("The Volatility Surface — Gatheral", "Book: The Volatility Surface — Gatheral"),
    ]

    pillars = ["00000000-0000-0000-0000-000000000001",
               "00000000-0000-0000-0000-000000000002",
               "00000000-0000-0000-0000-000000000003",
               "00000000-0000-0000-0000-000000000004",
               "00000000-0000-0000-0000-000000000005"]

    for pillar_idx, topics in enumerate([p1_topics, p2_topics, p3_topics, p4_topics, p5_topics]):
        for seq, (topic, title) in enumerate(topics, 1):
            episode_seed_data.append({
                "id": str(uuid4()),
                "pillar_id": pillars[pillar_idx],
                "sequence_number": seq,
                "topic": topic,
                "suggested_title": title,
                "status": "planned",
            })

    op.bulk_insert(episodes_table, episode_seed_data)


def downgrade():
    op.drop_table("schedule_overrides")
    op.drop_table("planned_episodes")
    op.drop_table("pillars")