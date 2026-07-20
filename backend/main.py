from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.database import get_engine
from core.redis_client import get_redis
from core.logging import setup_logging, get_logger
from core.config import get_settings

# Setup logging on import
setup_logging()
logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: verify connections on startup, close on shutdown."""
    settings = get_settings()
    logger.info("starting_quantifaya_autodirector", version="1.0.0")

    # Verify DB connection
    try:
        engine = get_engine()
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        logger.info("database_connected")
    except Exception as e:
        logger.warning("database_connection_failed", error=str(e))

    # Verify Redis connection
    try:
        async for redis in get_redis():
            await redis.ping()
        logger.info("redis_connected")
    except Exception as e:
        logger.warning("redis_connection_failed", error=str(e))

    # Connect Memgraph
    from services.ingestion.memgraph_client import MemgraphClient
    memgraph_client = MemgraphClient()
    await memgraph_client.connect()
    app.state.memgraph = memgraph_client

    logger.info("config", auto_approve=settings.auto_approve,
                manim_workers=settings.manim_workers,
                log_level=settings.log_level)

    yield

    # Shutdown
    await memgraph_client.close()
    logger.info("shutting_down")


def get_memgraph(request: Request):
    """FastAPI dependency for injecting MemgraphClient."""
    return request.app.state.memgraph


app = FastAPI(
    title="Quantifaya AutoDirector API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from api.routes import health, episodes, stream, sources, strategy
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(episodes.router, prefix="/api/v1/episodes", tags=["episodes"])
app.include_router(stream.router, prefix="/api/v1/stream", tags=["stream"])
app.include_router(sources.router, tags=["sources"])
app.include_router(strategy.router, tags=["strategy"])


@app.get("/")
async def root():
    return {"service": "Quantifaya AutoDirector", "version": "1.0.0", "status": "running"}
