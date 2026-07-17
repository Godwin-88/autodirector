"""Tests for the Wan client."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from services.generation.wan_client import WanClient, WanTimeoutError, WanAPIError


@pytest.mark.asyncio
async def test_wan_submit_job():
    """Test Wan job submission."""
    client = WanClient()
    # Mock the httpx post
    with patch("httpx.AsyncClient") as mock_client:
        mock_instance = MagicMock()
        mock_instance.post = AsyncMock()
        mock_instance.post.return_value.status_code = 200
        mock_instance.post.return_value.json.return_value = {
            "output": {"task_id": "test-job-123"},
            "request_id": "req-456",
        }
        mock_client.return_value.__aenter__.return_value = mock_instance

        job_id = await client.submit_job("test prompt", "negative", 8)
        assert job_id == "test-job-123"


@pytest.mark.asyncio
async def test_wan_timeout():
    """Test Wan timeout after max polls."""
    client = WanClient()
    with patch("httpx.AsyncClient") as mock_client:
        mock_instance = MagicMock()
        mock_instance.get = AsyncMock()
        mock_instance.get.return_value.status_code = 200
        mock_instance.get.return_value.json.return_value = {"status": "PENDING"}
        mock_client.return_value.__aenter__.return_value = mock_instance

        with pytest.raises(WanTimeoutError):
            await client.download_clip("test-job", "/tmp/test.mp4")