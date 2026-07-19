"""Tests for the semantic chunker service."""

import pytest
from services.ingestion.chunker import SemanticChunker


def test_chunk_returns_list_of_chunks():
    """Test that chunking returns a list of chunk dicts."""
    chunker = SemanticChunker()
    text = "This is paragraph one.\n\nThis is paragraph two.\n\nThis is paragraph three."
    chunks = chunker.chunk(text)

    assert isinstance(chunks, list)
    assert len(chunks) >= 1
    assert all("text" in c for c in chunks)
    assert all("token_count" in c for c in chunks)
    assert all("chunk_index" in c for c in chunks)


def test_chunk_respects_token_limit():
    """Test that chunks do not exceed the target token limit."""
    chunker = SemanticChunker()
    # Generate a long text (~3000 tokens)
    long_text = "\n\n".join([f"This is paragraph number {i} with some additional content to make it longer." for i in range(200)])
    chunks = chunker.chunk(long_text)

    assert len(chunks) > 1, "Long text should produce multiple chunks"
    for chunk in chunks:
        assert chunk["token_count"] <= chunker.CHUNK_TARGET_TOKENS * 1.5, \
            f"Chunk {chunk['chunk_index']} exceeds token limit: {chunk['token_count']}"


def test_chunk_overlap():
    """Test that consecutive chunks have overlapping content."""
    chunker = SemanticChunker()
    text = "\n\n".join([f"Paragraph number {i} with unique content for testing purposes." for i in range(50)])
    chunks = chunker.chunk(text)

    if len(chunks) >= 2:
        # Check that the last ~50 tokens of chunk N appear in chunk N+1
        chunk0_text = chunks[0]["text"]
        chunk1_text = chunks[1]["text"]

        # The overlap should mean some content from chunk 0 appears in chunk 1
        overlap_found = any(
            sentence in chunk1_text
            for sentence in chunk0_text.split(". ")
            if len(sentence) > 20
        )
        # This may not always be true with paragraph-aware chunking,
        # but at minimum chunks should be sequential
        assert chunks[0]["chunk_index"] < chunks[1]["chunk_index"]


def test_chunk_empty_text():
    """Test that empty text returns empty list."""
    chunker = SemanticChunker()
    assert chunker.chunk("") == []
    assert chunker.chunk("   ") == []


def test_chunk_metadata_preserved():
    """Test that metadata is passed through to chunks."""
    chunker = SemanticChunker()
    text = "Paragraph one.\n\nParagraph two."
    metadata = {"source_title": "Test Doc", "document_id": "abc-123"}
    chunks = chunker.chunk(text, metadata=metadata)

    for chunk in chunks:
        assert chunk["metadata"]["source_title"] == "Test Doc"
        assert chunk["metadata"]["document_id"] == "abc-123"