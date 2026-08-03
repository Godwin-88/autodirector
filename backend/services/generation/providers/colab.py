"""Colab GPU worker provider — queue-based, zero infrastructure on Render.

CogVideoX (and any GPU diffusion model) needs CUDA, which Render's free tier
does not provide. The ``ColabProvider`` bridges this: the API enqueues a job
to Upstash Redis, and the ``colab/cogvideox_worker.ipynb`` notebook (running
on a Colab T4 GPU, free tier) picks it up, generates the clip with
CogVideoX-2b, uploads the mp4 to Backblaze B2, and pushes the result back to
Redis. The provider polls for the result and downloads the file, keeping the
``generate() -> Path`` output contract intact.

Integration: CogVideoX(self-host) -> Colab(queue) -> Wan(API) -> Manim(fallback)
"""
import asyncio
import json
import tempfile
import uuid
from pathlib import Path
from typing import Dict

import httpx

from core.config import get_settings
from core.logging import get_logger

from services.generation.providers.base import (
    VideoGenError,
    VideoGenProvider,
    VideoGenTimeoutError,
)

logger = get_logger("providers.colab")


class ColabProvider(VideoGenProvider):
    """Enqueue GPU generation jobs to a Colab worker via Redis."""

    name = "colab"

    def __init__(self):
        settings = get_settings()
        self.redis_url = settings.colab_redis_url or settings.redis_url
        self.poll_interval = settings.colab_poll_interval_secs
        self.timeout = settings.colab_job_timeout_secs
        self.prefix = settings.colab_result_prefix
        self.b2_public_url_base = settings.b2_public_url_base

    async def _get_redis(self):
        from redis.asyncio import Redis
        return Redis.from_url(self.redis_url, decode_responses=True)

    async def generate(
        self,
        prompt: str,
        negative_prompt: str,
        output_path: str,
        duration_secs: int = 8,
        resolution: str = "1920*1080",
        episode_id: str = "",
    ) -> Path:
        """Enqueue a generation job and poll for the worker's result."""
        job_id = str(uuid.uuid4())[:8]
        queue_key = f"{self.prefix}:videojobs"
        result_key = f"{self.prefix}:results:{job_id}"

        payload = {
            "job_id": job_id,
            "episode_id": episode_id,
            "output_key": f"episodes/{episode_id}/intro.mp4" if episode_id else "",
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "duration_secs": duration_secs,
            "resolution": resolution,
            "output_path": output_path,
            "result_key": result_key,
        }

        redis = await self._get_redis()
        try:
            # Enqueue the job
            await redis.lpush(queue_key, json.dumps(payload))
            logger.info(
                "colab_job_enqueued",
                job_id=job_id,
                queue=queue_key,
            )

            # Poll for the result
            deadline = asyncio.get_event_loop().time() + self.timeout
            while True:
                raw = await redis.rpop(result_key)
                if raw:
                    result = json.loads(raw)
                    if result.get("status") == "success":
                        return await self._download_clip(
                            result["url"], output_path
                        )
                    raise VideoGenError(
                        f"Colab job failed: {result.get('error', 'unknown')}"
                    )
                if asyncio.get_event_loop().time() >= deadline:
                    raise VideoGenTimeoutError(
                        f"Colab job {job_id} did not complete in {self.timeout}s"
                    )
                await asyncio.sleep(self.poll_interval)
        finally:
            await redis.close()

    async def _download_clip(self, url: str, output_path: str) -> Path:
        """Download the generated clip from a public URL."""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=120)
            output.write_bytes(resp.content)
        logger.info("colab_clip_downloaded", path=str(output), url=url)
        return output


# Register with the provider registry
from services.generation.providers import register_provider  # noqa: E402

register_provider("colab", ColabProvider)