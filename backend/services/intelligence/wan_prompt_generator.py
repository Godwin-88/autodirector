from schemas.episode_outline import EpisodeOutline
from services.intelligence.qwen_client import QwenClient, QWEN_TURBO
from core.logging import get_logger

logger = get_logger("wan_prompt_generator")

WAN_PROMPT_TEMPLATE = """
A sharp, confident financial engineer in his early 30s sits at a sleek 
modern trading desk. Multiple monitors glow behind him showing real-time 
charts and floating mathematical equations. He looks directly at camera 
with intense, calculated focus — the expression of someone who has seen 
every market crash and learned from all of them. The lighting is dramatic: 
high-contrast, blue-tinted ambient light from the screens. Cinematic.
Photorealistic. Professional. Topic context: {topic}.
Camera: slow dolly in, starting wide, ending medium close-up. 8 seconds.
"""

WAN_NEGATIVE_PROMPT = "blurry, watermark, text artifacts, unrealistic anatomy, cartoon, anime, drawing"


class WanPromptGenerator:
    def __init__(self, qwen: QwenClient):
        self.qwen = qwen

    async def generate(self, outline: EpisodeOutline) -> str:
        """Generate a Wan prompt incorporating episode topic into the template."""
        prompt = WAN_PROMPT_TEMPLATE.format(topic=outline.topic)
        return prompt.strip()

    @property
    def negative_prompt(self) -> str:
        return WAN_NEGATIVE_PROMPT