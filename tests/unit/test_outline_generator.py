"""Tests for the outline generator."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from schemas.episode_outline import EpisodeOutline, SceneOutlineItem
from services.intelligence.outline_generator import OutlineGenerator


@pytest.fixture
def mock_qwen():
    qwen = MagicMock()
    qwen.complete_json = AsyncMock()
    return qwen


@pytest.mark.asyncio
async def test_outline_generates_valid_structure(mock_qwen):
    """Test that outline generator returns valid EpisodeOutline."""
    mock_qwen.complete_json.return_value = {
        "topic": "The Black-Scholes Model",
        "episode_number": 1,
        "series": "quantifaya",
        "seo_title": "Black-Scholes Model Explained | Quantifaya Ep.1",
        "scenes": [
            {
                "scene_number": 1,
                "scene_class_name": "SceneColdOpen",
                "title": "The Day the Models Failed",
                "duration_target_secs": 120,
                "key_equations": ["C = SN(d_1) - Ke^{-rT}N(d_2)"],
                "key_sources": ["Black & Scholes (1973)"],
                "voiceover_hint": "Open with 1987 crash and how models failed",
            },
            {
                "scene_number": 2,
                "scene_class_name": "SceneDelta",
                "title": "Delta: The First Greek",
                "duration_target_secs": 180,
                "key_equations": ["\\Delta = N(d_1)"],
                "key_sources": ["Hull (2022)"],
                "voiceover_hint": "Derive delta from first principles",
            },
        ],
    }

    generator = OutlineGenerator(mock_qwen)
    result = await generator.generate("The Black-Scholes Model", 1, "quantifaya")

    assert isinstance(result, EpisodeOutline)
    assert len(result.scenes) >= 2
    assert result.total_duration_target >= 200


@pytest.mark.asyncio
async def test_outline_scene_count_within_bounds(mock_qwen):
    """Test that scene count is between 8-12."""
    mock_qwen.complete_json.return_value = {
        "topic": "Test Topic",
        "episode_number": 1,
        "series": "quantifaya",
        "seo_title": "Test | Quantifaya Ep.1",
        "scenes": [
            {
                "scene_number": i,
                "scene_class_name": f"Scene{i}",
                "title": f"Scene {i}",
                "duration_target_secs": 150,
                "key_equations": ["x = y"],
                "key_sources": ["Author (2020)"],
                "voiceover_hint": f"Scene {i} description",
            }
            for i in range(1, 11)
        ],
    }

    generator = OutlineGenerator(mock_qwen)
    result = await generator.generate("Test Topic", 1, "quantifaya")

    assert 8 <= len(result.scenes) <= 12
    assert 1400 <= result.total_duration_target <= 1600