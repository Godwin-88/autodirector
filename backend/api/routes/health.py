from fastapi import APIRouter
from core.database import get_async_session_local
from core.redis_client import get_redis
from core.config import get_settings
from core.logging import get_logger

router = APIRouter()
logger = get_logger("health")


@router.get("")
async def health():
    return {"status": "ok", "version": "1.0.0"}


@router.get("/db")
async def health_db():
    try:
        session_local = get_async_session_local()
        async with session_local() as session:
            await session.execute("SELECT 1")
        return {"status": "ok"}
    except Exception as e:
        logger.warning("health_db_failed", error=str(e))
        return {"status": "error", "detail": str(e)}


@router.get("/redis")
async def health_redis():
    try:
        async for redis in get_redis():
            await redis.ping()
        return {"status": "ok"}
    except Exception as e:
        logger.warning("health_redis_failed", error=str(e))
        return {"status": "error", "detail": str(e)}


@router.get("/qwen")
async def health_qwen():
    from services.intelligence.qwen_client import QwenClient, QWEN_TURBO
    try:
        client = QwenClient()
        result = await client.complete(
            QWEN_TURBO,
            [{"role": "user", "content": "Reply with just: ok"}],
            max_tokens=10,
        )
        return {"status": "ok" if "ok" in result.lower() else "degraded", "response": result}
    except Exception as e:
        logger.warning("health_qwen_failed", error=str(e))
        return {"status": "error", "detail": str(e)}