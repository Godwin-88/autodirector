"""
End-to-end integration test for the intelligence phase of the pipeline.
Requires live Qwen API key and PostgreSQL.

Run with: pytest tests/integration/test_pipeline_e2e.py -v
"""
import pytest
from schemas.episode_outline import EpisodeOutline
from schemas.source import SourcesPackage
from services.intelligence.qwen_client import QwenClient
from services.intelligence.outline_generator import OutlineGenerator
from services.intelligence.source_extractor import SourceExtractor
from services.intelligence.script_generator import ScriptGenerator


@pytest.fixture
def qwen():
    return QwenClient()


@pytest.mark.skip(reason="Requires live Qwen API key")
@pytest.mark.asyncio
async def test_intelligence_phase_e2e(qwen):
    """Test the full intelligence phase with a real Qwen call."""
    topic = "The Normal Distribution Fails in Finance"

    # Step 1: Generate outline
    outline_gen = OutlineGenerator(qwen)
    outline = await outline_gen.generate(topic, 1, "quantifaya")
    assert isinstance(outline, EpisodeOutline)
    assert len(outline.scenes) >= 8
    assert 1400 <= outline.total_duration_target <= 1600
    assert len(outline.seo_title) <= 100

    # Step 2: Extract sources
    source_ext = SourceExtractor(qwen)
    all_sources = []
    for scene in outline.scenes[:3]:  # Only first 3 scenes to save quota
        sources = await source_ext.extract(scene, topic)
        all_sources.extend(sources)

    assert len(all_sources) >= 1  # At least one real citation

    sources_pkg = SourcesPackage(episode_topic=topic, sources=all_sources)

    # Step 3: Generate script
    script_gen = ScriptGenerator(qwen)
    script = await script_gen.generate(outline, sources_pkg)
    assert "scenes" in script
    total_words = sum(
        len(s.get("voiceover_text", "").split())
        for s in script.get("scenes", [])
    )
    assert total_words >= 2000  # Script should be > 2000 words