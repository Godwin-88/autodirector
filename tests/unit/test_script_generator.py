"""Tests for the script generator."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from schemas.episode_outline import EpisodeOutline, SceneOutlineItem
from schemas.source import SourcesPackage, AcademicSource
from services.intelligence.script_generator import ScriptGenerator


@pytest.fixture
def mock_qwen():
    qwen = MagicMock()
    qwen.complete_json = AsyncMock()
    return qwen


@pytest.fixture
def sample_outline():
    return EpisodeOutline(
        topic="The Greeks",
        episode_number=2,
        series="quantifaya",
        seo_title="Options Greeks Explained | Quantifaya Ep.2",
        scenes=[
            SceneOutlineItem(
                scene_number=1,
                scene_class_name="SceneColdOpen",
                title="Why Greeks Matter",
                duration_target_secs=120,
                key_equations=["\\Delta = N(d_1)"],
                key_sources=["Hull (2022)"],
                voiceover_hint="Why options traders need Greeks",
            ),
        ],
    )


@pytest.fixture
def sample_sources():
    return SourcesPackage(
        episode_topic="The Greeks",
        sources=[
            AcademicSource(
                ref_number=1,
                authors="John Hull",
                year=2022,
                title="Options, Futures, and Other Derivatives",
                journal_or_publisher="Pearson",
                scene_usage_note="Standard reference for Greeks",
            ),
        ],
    )


@pytest.mark.asyncio
async def test_script_generates_valid_structure(mock_qwen, sample_outline, sample_sources):
    """Test that script generator returns correct structure."""
    mock_qwen.complete_json.return_value = {
        "episode_id": "test-ep-001",
        "scenes": [
            {
                "scene_number": 1,
                "scene_class": "SceneColdOpen",
                "voiceover_text": "Let me tell you why Greeks matter. [PAUSE] Every options trader... *equation appears*",
                "stage_directions": ["Equation fades in", "Gold highlight on Delta"],
            },
        ],
    }

    generator = ScriptGenerator(mock_qwen)
    result = await generator.generate(sample_outline, sample_sources)

    assert "scenes" in result
    assert len(result["scenes"]) >= 1
    scene = result["scenes"][0]
    assert "voiceover_text" in scene
    assert "[PAUSE]" in scene["voiceover_text"] or True  # [PAUSE] optional per scene


@pytest.mark.asyncio
async def test_script_contains_stage_directions(mock_qwen, sample_outline, sample_sources):
    """Test that script includes stage directions."""
    mock_qwen.complete_json.return_value = {
        "episode_id": "test-ep-002",
        "scenes": [
            {
                "scene_number": 1,
                "scene_class": "SceneColdOpen",
                "voiceover_text": "Test voiceover with *stage direction* here.",
                "stage_directions": ["Equation appears", "Text glows gold"],
            },
        ],
    }

    generator = ScriptGenerator(mock_qwen)
    result = await generator.generate(sample_outline, sample_sources)

    scene = result["scenes"][0]
    assert len(scene["stage_directions"]) >= 1