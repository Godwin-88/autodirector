"""Tests for the episode compositor."""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from services.composition.episode_compositor import EpisodeCompositor


@pytest.mark.asyncio
async def test_compose_creates_manifest():
    """Test that compositor builds correct concat manifest."""
    compositor = EpisodeCompositor()

    with patch("services.composition.episode_compositor.asyncio.create_subprocess_exec") as mock_subprocess:
        mock_proc = MagicMock()
        mock_proc.communicate = AsyncMock(return_value=(b"", b""))
        mock_subprocess.return_value = mock_proc

        with patch("services.composition.episode_compositor.Path.exists") as mock_exists:
            mock_exists.return_value = True
            result = await compositor.compose(
                "test-ep-001",
                "/tmp/wan_intro.mp4",
                ["/tmp/scene_1.mp4", "/tmp/scene_2.mp4"],
            )

    assert result is not None
    assert "test-ep-001" in str(result)


@pytest.mark.asyncio
async def test_compose_handles_empty_scenes():
    """Test compositor handles missing scene files gracefully."""
    compositor = EpisodeCompositor()

    with patch("services.composition.episode_compositor.asyncio.create_subprocess_exec") as mock_subprocess:
        mock_proc = MagicMock()
        mock_proc.communicate = AsyncMock(return_value=(b"", b""))
        mock_subprocess.return_value = mock_proc

        result = await compositor.compose(
            "test-ep-002",
            "",
            [],
        )

    assert result is not None