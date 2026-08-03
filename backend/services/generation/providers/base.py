"""Abstract interface for video generation providers.

Every provider (CogVideoX, Kling, Wan, ...) implements this contract so the
rest of the pipeline can treat them interchangeably. The key invariant is the
output contract: ``generate()`` returns a ``Path`` to a local ``.mp4`` file.

Providers that support image-to-video (for character consistency) may
optionally implement ``generate_from_image()``.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class VideoGenError(Exception):
    """Base error for all video generation failures."""


class VideoGenTimeoutError(VideoGenError):
    """Raised when a generation job does not complete in time."""


class VideoGenAPIError(VideoGenError):
    """Raised when a provider API returns an error."""


class VideoGenProvider(ABC):
    """Common interface for all video generation backends."""

    name: str = "base"

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        negative_prompt: str,
        output_path: str,
        duration_secs: int = 8,
        resolution: str = "1920*1080",
    ) -> Path:
        """Generate a video clip from a text prompt.

        Args:
            prompt: The positive text prompt describing the scene.
            negative_prompt: Things to avoid in the output.
            output_path: Where to write the resulting .mp4.
            duration_secs: Target clip duration in seconds.
            resolution: e.g. "1920*1080" or "1080*1920".

        Returns:
            Path to the generated .mp4 file.

        Raises:
            VideoGenError: on any generation failure.
        """
        raise NotImplementedError

    async def generate_from_image(
        self,
        image_path: str,
        prompt: str,
        output_path: str,
        duration_secs: int = 8,
        resolution: str = "1920*1080",
    ) -> Path:
        """Generate a video clip seeded from a reference image.

        Used for character consistency (recurring host persona). Providers
        that do not support image-to-video should leave this unimplemented;
        the caller will fall back to text-only generation.
        """
        raise NotImplementedError(
            f"Provider '{self.name}' does not support image-to-video"
        )

    @property
    def default_negative_prompt(self) -> str:
        """Provider-specific default negative prompt."""
        return "blurry, watermark, text artifacts, unrealistic anatomy, cartoon, anime, drawing"