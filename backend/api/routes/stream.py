import json
from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
from core.redis_client import get_redis
from core.logging import get_logger

logger = get_logger("stream")
router = APIRouter()


@router.get("/{episode_id}/progress")
async def stream_progress(episode_id: str):
    """SSE endpoint for episode generation progress."""

    async def event_generator():
        async for redis in get_redis():
            pubsub = redis.pubsub()
            await pubsub.subscribe(f"episode:{episode_id}:progress")
            try:
                async for message in pubsub.listen():
                    if message["type"] == "message":
                        data = json.loads(message["data"])
                        yield {
                            "event": "progress",
                            "data": json.dumps(data),
                        }
                        if data.get("phase") in ("delivered", "failed"):
                            break
            finally:
                await pubsub.unsubscribe(f"episode:{episode_id}:progress")

    return EventSourceResponse(event_generator())