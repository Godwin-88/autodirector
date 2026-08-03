"""Tests for the Backblaze B2 storage service."""
import os
import sys
import json
from pathlib import Path

# Set B2 env vars before importing the service (module reads settings on import)
os.environ.setdefault("B2_KEY_ID", "test-key-id")
os.environ.setdefault("B2_APPLICATION_KEY", "test-app-key")
os.environ.setdefault("B2_BUCKET_NAME", "quantifaya")
os.environ.setdefault(
    "B2_ENDPOINT_URL", "https://s3.us-east-005.backblazeb2.com"
)
os.environ.setdefault(
    "B2_PUBLIC_URL_BASE", "https://f005.backblazeb2.com/file/quantifaya"
)

import asyncio

import pytest
from unittest.mock import MagicMock, patch

from services.delivery.b2_storage import B2StorageService


def _make_service(mock_client: MagicMock) -> B2StorageService:
    """Construct a B2StorageService with a mocked boto3 client."""
    with patch("boto3.client", return_value=mock_client):
        service = B2StorageService()
    return service


def _write_temp_file(path: Path, content: bytes = b"test-data") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path


@pytest.mark.asyncio
async def test_upload_file():
    """upload_file uploads with correct content type and returns public URL."""
    mock_client = MagicMock()
    service = _make_service(mock_client)

    test_file = _write_temp_file(Path("/tmp/test_b2/hello.txt"))

    result = await service.upload_file(test_file, "episodes/abc-123/final.mp4")

    mock_client.upload_file.assert_called_once()
    call_args = mock_client.upload_file.call_args
    assert call_args[0][0] == str(test_file)
    assert call_args[0][1] == "quantifaya"
    assert call_args[0][2] == "episodes/abc-123/final.mp4"
    assert call_args[1]["ExtraArgs"]["ContentType"] == "text/plain"
    assert call_args[1]["ExtraArgs"]["ACL"] == "public-read"

    assert result["b2_key"] == "episodes/abc-123/final.mp4"
    assert result["url"] == (
        "https://f005.backblazeb2.com/file/quantifaya/"
        "episodes/abc-123/final.mp4"
    )
    assert result["size_bytes"] == len(b"test-data")


@pytest.mark.asyncio
async def test_upload_missing_file_raises():
    """upload_file raises FileNotFoundError for missing local files."""
    service = _make_service(MagicMock())
    with pytest.raises(FileNotFoundError):
        await service.upload_file(
            Path("/tmp/does-not-exist.mp4"), "episodes/x/final.mp4"
        )


@pytest.mark.asyncio
async def test_upload_episode_assets_uses_correct_keys():
    """upload_episode_assets uploads permanent assets under episodes/ and
    raw intermediates under intermediates/ (for 7-day lifecycle expiry)."""
    mock_client = MagicMock()
    service = _make_service(mock_client)

    ep_id = "ep-123"
    # Create all local output files
    _write_temp_file(Path(f"./output/episodes/{ep_id}/quantifaya_ep_final.mp4"))
    _write_temp_file(Path(f"./output/thumbnails/{ep_id}.jpg"))
    _write_temp_file(Path(f"./output/wan/{ep_id}_intro.mp4"))
    _write_temp_file(Path(f"./output/scenes/{ep_id}/scene_01_synced.mp4"))
    _write_temp_file(Path(f"./output/scenes/{ep_id}/scene_02_synced.mp4"))
    _write_temp_file(Path(f"./output/audio/{ep_id}/scene_01.wav"))

    manifest = await service.upload_episode_assets(ep_id)

    # Collect all upload_file keys
    uploaded_keys = []
    for call in mock_client.upload_file.call_args_list:
        uploaded_keys.append(call.args[2])

    # Permanent assets under episodes/{id}/
    assert "episodes/ep-123/final.mp4" in uploaded_keys
    assert "episodes/ep-123/thumbnail.jpg" in uploaded_keys
    assert "episodes/ep-123/wan_intro.mp4" in uploaded_keys

    # Raw intermediates under intermediates/{id}/
    assert "intermediates/ep-123/scenes/scene_01_synced.mp4" in uploaded_keys
    assert "intermediates/ep-123/scenes/scene_02_synced.mp4" in uploaded_keys
    assert "intermediates/ep-123/audio/scene_01.wav" in uploaded_keys

    # Manifest is uploaded as JSON
    assert manifest["episode_id"] == ep_id
    assert manifest["assets"]["final_video"]["url"].startswith(
        "https://f005.backblazeb2.com/file/quantifaya/episodes/ep-123/"
    )
    assert len(manifest["assets"]["scenes"]) == 2
    assert len(manifest["assets"]["audio"]) == 1
    assert "manifest_url" in manifest

    # Verify manifest.json put_object call
    put_calls = [
        c for c in mock_client.put_object.call_args_list
        if c.kwargs.get("Key") == "episodes/ep-123/manifest.json"
    ]
    assert len(put_calls) == 1
    assert put_calls[0].kwargs["ContentType"] == "application/json"
    assert put_calls[0].kwargs["ACL"] == "public-read"
    # Body should be valid JSON
    body = put_calls[0].kwargs["Body"].decode()
    parsed = json.loads(body)
    assert parsed["episode_id"] == ep_id


def test_ensure_bucket_sets_lifecycle_for_intermediates_only():
    """ensure_bucket applies a lifecycle rule that expires ONLY intermediates/,
    never the permanent episodes/ assets."""
    mock_client = MagicMock()
    # First call to head_bucket raises => bucket does not exist => create it
    mock_client.head_bucket.side_effect = [Exception("not found")]
    service = _make_service(mock_client)

    service.ensure_bucket()

    mock_client.create_bucket.assert_called_once_with(Bucket="quantifaya")
    mock_client.put_bucket_lifecycle_configuration.assert_called_once()

    lifecycle_call = mock_client.put_bucket_lifecycle_configuration.call_args
    rules = lifecycle_call.kwargs["LifecycleConfiguration"]["Rules"]
    assert len(rules) == 1
    rule = rules[0]
    assert rule["ID"] == "expire-raw-intermediates"
    assert rule["Filter"] == {"Prefix": "intermediates/"}
    assert rule["Expiration"] == {"Days": 7}


def test_ensure_bucket_skips_create_when_exists():
    """ensure_bucket does not re-create an existing bucket."""
    mock_client = MagicMock()
    service = _make_service(mock_client)

    service.ensure_bucket()

    mock_client.create_bucket.assert_not_called()
    mock_client.put_bucket_lifecycle_configuration.assert_called_once()


def test_list_all_episodes_uses_sync_paginator():
    """list_all_episodes uses boto3's synchronous paginator correctly."""
    mock_client = MagicMock()

    # Mock paginator: one page with two episode prefixes
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {
            "CommonPrefixes": [
                {"Prefix": "episodes/ep-1/"},
                {"Prefix": "episodes/ep-2/"},
            ]
        }
    ]
    mock_client.get_paginator.return_value = mock_paginator

    # Mock manifest fetch for each episode
    def fake_get_object(**kwargs):
        key = kwargs["Key"]
        ep_id = key.split("/")[1]
        manifest = {
            "episode_id": ep_id,
            "uploaded_at": "2026-08-03T00:00:00",
            "assets": {},
            "manifest_url": f"https://f005.backblazeb2.com/file/quantifaya/{key}",
        }
        body = MagicMock()
        body.read.return_value = json.dumps(manifest).encode()
        return {"Body": body}

    mock_client.get_object.side_effect = fake_get_object
    service = _make_service(mock_client)

    episodes = asyncio.run(service.list_all_episodes())

    assert len(episodes) == 2
    ids = {e["episode_id"] for e in episodes}
    assert ids == {"ep-1", "ep-2"}

    # Verify sync iteration (not async) over paginator
    mock_paginator.paginate.assert_called_once_with(
        Bucket="quantifaya",
        Prefix="episodes/",
        Delimiter="/",
    )


def test_health_check():
    """health_check returns connected status when bucket exists."""
    mock_client = MagicMock()
    service = _make_service(mock_client)

    result = service.health_check()
    assert result["status"] == "connected"
    assert result["bucket"] == "quantifaya"
    assert result["endpoint"] == "https://s3.us-east-005.backblazeb2.com"