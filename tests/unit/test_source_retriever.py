"""Tests for the source retriever service."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from services.intelligence.source_retriever import SourceRetriever, RetrievalPackage, SceneRetrievalResult


@pytest.mark.asyncio
async def test_retrieve_for_episode_empty_when_no_sources():
    """Test that retrieval returns empty package when no sources exist."""
    retriever = SourceRetriever(db_session=None, memgraph_client=None, embedder=None)
    outline = MagicMock()
    outline.title = "Test Topic"

    result = await retriever.retrieve_for_episode(
        topic="Test Topic",
        outline=outline,
        episode_id="some-episode-id",
        top_k=5,
    )

    assert isinstance(result, RetrievalPackage)
    assert result.topic == "Test Topic"
    assert result.vector_chunks == []
    assert result.graphrag_data is None
    assert result.total_sources == 0
    assert "VERIFIED SOURCE MATERIAL" in result.context_block


@pytest.mark.asyncio
async def test_context_block_formatting():
    """Test that context block is properly formatted."""
    retriever = SourceRetriever()

    vector_chunks = [
        {
            "id": "chunk-1",
            "text": "Fat tails are a key concept in extreme value theory.",
            "title": "Extreme Value Theory",
            "authors": "Taleb, N.",
            "year": 2020,
            "source_type": "url",
            "origin_url": "https://example.com/evt",
        }
    ]

    graphrag_data = {
        "concepts": [{"name": "Fat Tails", "definition": "A distribution with heavier tails than the normal distribution."}],
        "equations": [{"latex": "P(X > x) \\sim x^{-\\alpha}"}],
        "papers": [{"authors": "Mandelbrot, B.", "year": 1963, "title": "The Variation of Certain Speculative Prices"}],
    }

    context = retriever.build_context_block("Fat Tails", vector_chunks, graphrag_data)

    assert "VERIFIED SOURCE MATERIAL" in context
    assert "GRAPHRAG KNOWLEDGE" in context
    assert "Taleb" in context
    assert "Mandelbrot" in context
    assert "[UNVERIFIED" in context or "Ground every factual claim" in context
    assert "\\alpha" in context or "alpha" in context


@pytest.mark.asyncio
async def test_retrieve_for_scene_returns_empty_when_no_retriever():
    """Test scene retrieval returns empty result when no retriever configured."""
    retriever = SourceRetriever()
    scene = MagicMock()
    scene.title = "Fat Tails"
    scene.scene_number = 1
    scene.key_equations = []

    result = await retriever.retrieve_for_scene(scene, "episode-id")

    assert isinstance(result, SceneRetrievalResult)
    assert result.scene_number == 1
    assert result.chunks == []
    assert result.citations == []
    assert result.equations_from_graph == []


def test_citation_formatting():
    """Test citation formatting from chunk data."""
    retriever = SourceRetriever()

    chunk = {
        "authors": "Taleb, N.",
        "year": 1997,
        "title": "Dynamic Hedging",
        "source_type": "url",
        "origin_url": "https://example.com",
    }

    citation = retriever._format_as_citation(chunk)
    assert "Taleb" in citation
    assert "1997" in citation
    assert "Dynamic Hedging" in citation


def test_citation_formatting_unknown():
    """Test citation formatting with missing metadata."""
    retriever = SourceRetriever()

    chunk = {
        "authors": "",
        "year": None,
        "title": "",
        "source_type": "",
        "origin_url": None,
    }

    citation = retriever._format_as_citation(chunk)
    assert citation == "Unknown source"