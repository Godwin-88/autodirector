"""Tests for the Backblaze Genblaze SDK client."""
import os
import sys
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

import pytest
from unittest.mock import MagicMock, patch

from services.delivery.genblaze_client import GenblazeClient


def _make_client(mock_backend: MagicMock, mock_transfer: MagicMock) -> GenblazeClient:
    """Construct a GenblazeClient with mocked backend + transfer.

    Note: genblaze_client.py binds S3StorageBackend and AssetTransfer into its
    module namespace via `from ... import ...`, so we must patch them where
    they are used (services.delivery.genblaze_client.*), not the source module.
    """
    with patch(
        "services.delivery.genblaze_client.S3StorageBackend",
        return_value=mock_backend,
    ), patch(
        "services.delivery.genblaze_client.AssetTransfer",
        return_value=mock_transfer,
    ):
        client = GenblazeClient()
    return client


def test_upload_asset_transfers_file():
    """upload_asset reads the local file, builds an Asset, and transfers it."""
    mock_backend = MagicMock()
    mock_transfer = MagicMock()
    mock_transfer.transfer.return_value = (
        "https://f005.backblazeb2.com/file/quantifaya/episodes/test-final.mp4"
    )
    client = _make_client(mock_backend, mock_transfer)

    test_file = Path("/tmp/test_genblaze/final.mp4")
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_bytes(b"binary-video-data")

    asset = client.upload_asset(test_file, "video/mp4", asset_id="ep-final")

    # Asset metadata is correct
    assert asset.asset_id == "ep-final"
    assert asset.media_type == "video/mp4"
    assert asset.size_bytes == len(b"binary-video-data")
    assert asset.sha256 is not None

    # transfer() was called with the asset
    mock_transfer.transfer.assert_called_once()
    transferred_asset = mock_transfer.transfer.call_args.args[0]
    assert transferred_asset.asset_id == "ep-final"


def test_upload_missing_file_raises():
    """upload_asset raises FileNotFoundError for missing local files."""
    client = _make_client(MagicMock(), MagicMock())
    with pytest.raises(FileNotFoundError):
        client.upload_asset(Path("/tmp/does-not-exist.mp4"), "video/mp4")


def test_list_episode_ids_derives_ids_from_keys():
    """list_episode_ids derives unique episode IDs from the object keys."""
    mock_backend = MagicMock()
    mock_transfer = MagicMock()

    # Simulate two pages of listing with a paginated response
    class FakeItem:
        def __init__(self, key):
            self.key = key

    class FakePage:
        def __init__(self, items, next_token):
            self.items = items
            self.next_token = next_token

    mock_backend.list.side_effect = [
        FakePage(
            items=[
                FakeItem("episodes/ep-1/final.mp4"),
                FakeItem("episodes/ep-1/thumbnail.jpg"),
                FakeItem("episodes/ep-2/final.mp4"),
                FakeItem("intermediates/ep-2/scenes/scene_01_synced.mp4"),
            ],
            next_token="token-1",
        ),
        FakePage(
            items=[FakeItem("episodes/ep-2/manifest.json")],
            next_token=None,
        ),
    ]

    client = _make_client(mock_backend, mock_transfer)
    ids = client.list_episode_ids()

    assert ids == ["ep-1", "ep-2"]

    # Verify pagination: called with prefix, then with continuation token
    assert mock_backend.list.call_count == 2
    first_call = mock_backend.list.call_args_list[0]
    assert first_call.args == ("episodes/",)
    assert first_call.kwargs["continuation_token"] is None
    second_call = mock_backend.list.call_args_list[1]
    assert second_call.kwargs["continuation_token"] == "token-1"


def test_get_public_url_and_presigned():
    """get_public_url builds durable URL; get_presigned_url delegates."""
    mock_backend = MagicMock()
    mock_transfer = MagicMock()
    mock_backend.get_url.return_value = "https://presigned.example/foo"

    client = _make_client(mock_backend, mock_transfer)

    durable = client.get_public_url("episodes/ep-1/final.mp4")
    assert durable == (
        "https://f005.backblazeb2.com/file/quantifaya/"
        "episodes/ep-1/final.mp4"
    )

    presigned = client.get_presigned_url("episodes/ep-1/final.mp4", expires_in=600)
    assert presigned == "https://presigned.example/foo"
    mock_backend.get_url.assert_called_once_with(
        "episodes/ep-1/final.mp4", expires_in=600
    )


def test_delete_episode_calls_delete_prefix():
    """delete_episode deletes all objects under the episode prefix."""
    mock_backend = MagicMock()
    mock_transfer = MagicMock()
    mock_backend.delete_prefix.return_value = MagicMock(deleted=5)

    client = _make_client(mock_backend, mock_transfer)
    count = client.delete_episode("ep-1")

    assert count == 5
    mock_backend.delete_prefix.assert_called_once_with(
        "episodes/ep-1/", dry_run=False
    )


def test_health_check_connected():
    """health_check returns connected when the bucket is reachable."""
    mock_backend = MagicMock()
    mock_transfer = MagicMock()
    client = _make_client(mock_backend, mock_transfer)

    result = client.health_check()
    assert result["status"] == "connected"
    assert result["bucket"] == "quantifaya"
    assert result["sdk"] == "genblaze"
    assert "endpoint" in result