import json
import time
from typing import List, Optional, Dict, Any
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from core.config import get_settings
from core.logging import get_logger

logger = get_logger("qwen_client")

# Model constants
QWEN_MAX = "qwen-max"
QWEN_TURBO = "qwen-turbo"
QWEN_VL = "qwen-vl-max"


class QwenRateLimitError(Exception):
    pass


class QwenClient:
    def __init__(self):
        settings = get_settings()
        self.client = AsyncOpenAI(
            api_key=settings.qwen_api_key,
            base_url=settings.qwen_base_url,
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(QwenRateLimitError),
    )
    async def complete(
        self,
        model: str,
        messages: List[dict],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[dict] = None,
    ) -> str:
        start_time = time.monotonic()
        kwargs = dict(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        if response_format:
            kwargs["response_format"] = response_format

        try:
            response = await self.client.chat.completions.create(**kwargs)
            elapsed_ms = (time.monotonic() - start_time) * 1000
            content = response.choices[0].message.content or ""

            logger.debug(
                "qwen_completion",
                model=model,
                prompt_tokens=response.usage.prompt_tokens if response.usage else 0,
                completion_tokens=response.usage.completion_tokens if response.usage else 0,
                latency_ms=round(elapsed_ms, 1),
            )
            return content
        except Exception as e:
            if "rate" in str(e).lower() or "429" in str(e):
                raise QwenRateLimitError(str(e)) from e
            raise

    async def complete_json(
        self,
        model: str,
        messages: List[dict],
        temperature: float = 0.3,
    ) -> dict:
        content = await self.complete(model, messages, temperature=temperature)
        # Strip markdown code fences if present
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.warning("qwen_json_parse_failed", error=str(e), content=content[:200])
            # Retry once with corrective message
            messages.append({"role": "assistant", "content": content})
            messages.append({
                "role": "user",
                "content": f"Your previous response was not valid JSON. Please return ONLY valid JSON. Error: {e}"
            })
            retry_content = await self.complete(model, messages, temperature=temperature)
            retry_content = retry_content.strip()
            if retry_content.startswith("```json"):
                retry_content = retry_content[7:]
            if retry_content.startswith("```"):
                retry_content = retry_content[3:]
            if retry_content.endswith("```"):
                retry_content = retry_content[:-3]
            return json.loads(retry_content.strip())