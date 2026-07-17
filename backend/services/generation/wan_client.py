import httpx
from pathlib import Path
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from core.config import get_settings
from core.logging import get_logger

logger = get_logger("wan_client")


class WanTimeoutError(Exception):
    pass


class WanAPIError(Exception):
    pass


class WanClient:
    def __init__(self):
        settings = get_settings()
        self.api_key = settings.wan_api_key
        self.base_url = settings.wan_api_base_url

    async def submit_job(self, prompt: str, negative_prompt: str,
                         duration_secs: int = 8,
                         resolution: str = "1920*1080") -> str:
        """Submit a video generation job to Wan API. Returns job_id."""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/services/aigc/video-generation/video-synthesis",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "X-DashScope-Async": "enable",
                },
                json={
                    "model": "wan2.1-t2v-plus",
                    "input": {
                        "text": prompt,
                        "negative_prompt": negative_prompt,
                    },
                    "parameters": {
                        "size": resolution,
                        "duration": duration_secs,
                    },
                },
                timeout=60,
            )
            if resp.status_code != 200:
                raise WanAPIError(f"Submit failed: {resp.status_code} {resp.text}")
            data = resp.json()
            job_id = data.get("output", {}).get("task_id", data.get("request_id", ""))
            logger.info("wan_job_submitted", job_id=job_id)
            return job_id

    async def poll_status(self, task_id: str) -> dict:
        """Poll Wan API for job status."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/tasks/{task_id}",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=30,
            )
            if resp.status_code != 200:
                raise WanAPIError(f"Poll failed: {resp.status_code} {resp.text}")
            return resp.json()

    async def download_clip(self, task_id: str, output_path: str) -> Path:
        """Poll until SUCCEEDED, then download video."""
        output = Path(output_path)
        for attempt in range(20):
            status_data = await self.poll_status(task_id)
            status = status_data.get("status", "")
            if status == "SUCCEEDED":
                video_url = status_data.get("output", {}).get("video_url", "")
                if video_url:
                    async with httpx.AsyncClient() as client:
                        resp = await client.get(video_url, timeout=120)
                        output.write_bytes(resp.content)
                    logger.info("wan_clip_downloaded", task_id=task_id, path=str(output))
                    return output
                raise WanAPIError("No video_url in succeeded response")
            elif status == "FAILED":
                raise WanAPIError(f"Job failed: {status_data}")
            elif status in ("PENDING", "RUNNING"):
                import asyncio
                await asyncio.sleep(10)
            else:
                raise WanAPIError(f"Unknown status: {status}")
        raise WanTimeoutError(f"Job {task_id} did not complete in 200s")

    async def generate(self, prompt: str, negative_prompt: str,
                       output_path: str, duration_secs: int = 8) -> Path:
        """Convenience: submit → poll → download."""
        job_id = await self.submit_job(prompt, negative_prompt, duration_secs)
        return await self.download_clip(job_id, output_path)