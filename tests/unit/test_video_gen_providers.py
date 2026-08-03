"""Tests for the video generation provider abstraction layer."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from services.generation.providers import (
    get_video_gen_provider,
    get_video_gen_fallback_provider,
    register_provider,
    _REGISTRY,
)
from services.generation.providers.base import (
    VideoGenError,
    VideoGenProvider,
    VideoGenTimeoutError,
)


class FakeProvider(VideoGenProvider):
    """Test double implementing the provider interface."""
    name = "fake"

    def __init__(self):
        self.generate_calls = 0

    async def generate(self, prompt, negative_prompt, output_path,
                       duration_secs=8, resolution="1920*1080"):
        self.generate_calls += 1
        from pathlib import Path
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"fake-video")
        return p


def test_register_provider():
    """Test that providers can be registered in the registry."""
    register_provider("fake", FakeProvider)
    assert "fake" in _REGISTRY
    assert _REGISTRY["fake"] is FakeProvider


def test_get_video_gen_provider_returns_configured():
    """Test factory returns the configured provider instance."""
    register_provider("fake", FakeProvider)
    with patch("services.generation.providers.get_settings") as mock_settings:
        mock_settings.return_value.video_gen_provider = "fake"
        provider = get_video_gen_provider()
        assert isinstance(provider, FakeProvider)


def test_get_video_gen_provider_unknown_falls_back_to_wan():
    """Test unknown provider name falls back to wan."""
    with patch("services.generation.providers.get_settings") as mock_settings:
        mock_settings.return_value.video_gen_provider = "nonexistent"
        provider = get_video_gen_provider()
        assert provider.name == "wan"


def test_get_video_gen_fallback_provider():
    """Test fallback provider selection."""
    register_provider("fake", FakeProvider)
    with patch("services.generation.providers.get_settings") as mock_settings:
        mock_settings.return_value.video_gen_fallback_provider = "fake"
        provider = get_video_gen_fallback_provider()
        assert isinstance(provider, FakeProvider)


@pytest.mark.asyncio
async def test_provider_generate_returns_path():
    """Test that a provider's generate() returns a Path to an mp4."""
    provider = FakeProvider()
    path = await provider.generate("prompt", "negative", "/tmp/test_out.mp4")
    assert path.exists()
    assert path.suffix == ".mp4"


@pytest.mark.asyncio
async def test_provider_generate_from_image_not_implemented():
    """Test that generate_from_image raises NotImplementedError by default."""
    provider = FakeProvider()
    with pytest.raises(NotImplementedError):
        await provider.generate_from_image(
            "/tmp/img.png", "prompt", "/tmp/out.mp4"
        )


@pytest.mark.asyncio
async def test_wan_provider_generate_chain():
    """Test the WanProvider implements the interface and generates."""
    from services.generation.providers.wan import WanProvider

    provider = WanProvider()
    with patch("httpx.AsyncClient") as mock_client:
        # Submit response (sync .json() returns the task id)
        submit_response = MagicMock()
        submit_response.status_code = 200
        submit_response.json.return_value = {
            "output": {"task_id": "test-job-123"},
        }

        # Status response: SUCCEEDED with video_url; content for download
        status_response = MagicMock()
        status_response.status_code = 200
        status_response.json.return_value = {
            "status": "SUCCEEDED",
            "output": {"video_url": "https://example.com/video.mp4"},
        }
        status_response.content = b"fake-video"

        # Async client: .post and .get are awaited, so they must be AsyncMock
        # whose return_value is the (sync) response object.
        mock_instance = AsyncMock()
        mock_instance.post = AsyncMock(return_value=submit_response)
        mock_instance.get = AsyncMock(return_value=status_response)
        mock_client.return_value.__aenter__.return_value = mock_instance

        path = await provider.generate("prompt", "negative", "/tmp/wan_out.mp4")
        assert path.exists()
        assert path.suffix == ".mp4"
