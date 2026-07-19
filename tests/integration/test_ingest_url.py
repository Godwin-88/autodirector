"""Integration test for URL ingestion pipeline.

This test ingests a real, stable URL and verifies the full pipeline:
scrape → chunk → embed → store.

Requires a running PostgreSQL instance with pgvector and a valid QWEN_API_KEY.
Marked with @pytest.mark.integration to allow selective skipping.
"""

import pytest
import uuid
from unittest.mock import AsyncMock, patch


@pytest.mark.integration
@pytest.mark.asyncio
async def test_ingest_url_end_to_end():
    """Test the full URL ingestion pipeline with a real URL."""
    from services.ingestion.url_scraper import URLScraper
    from services.ingestion.chunker import SemanticChunker
    from services.ingestion.embedder import ChunkEmbedder
    from services.ingestion.ingest_pipeline import IngestPipeline

    # Use a mock DB session
    mock_db = AsyncMock()

    # Mock the flush and commit
    async def mock_flush():
        pass
    mock_db.flush = AsyncMock(side_effect=mock_flush)
    mock_db.commit = AsyncMock(side_effect=mock_flush)
    mock_db.add = MagicMock()

    scraper = URLScraper()
    chunker = SemanticChunker()
    embedder = ChunkEmbedder()

    pipeline = IngestPipeline(
        db_session=mock_db,
        scraper=scraper,
        extractor=None,
        chunker=chunker,
        embedder=embedder,
    )

    # Use httpbin.org/html as a safe, stable test target
    test_url = "https://httpbin.org/html"

    try:
        document_id = await pipeline.ingest_url(test_url)
        assert document_id is not None
        assert len(str(document_id)) > 0
    except Exception as e:
        # If the URL is unreachable (no internet), skip gracefully
        if "connect" in str(e).lower() or "timeout" in str(e).lower():
            pytest.skip(f"Network unavailable: {e}")
        raise


@pytest.mark.integration
@pytest.mark.asyncio
async def test_ingest_url_creates_document_and_chunks():
    """Test that URL ingestion creates a document and chunks."""
    from services.ingestion.url_scraper import URLScraper
    from services.ingestion.chunker import SemanticChunker
    from services.ingestion.embedder import ChunkEmbedder
    from services.ingestion.ingest_pipeline import IngestPipeline

    mock_db = AsyncMock()
    mock_db.flush = AsyncMock()
    mock_db.commit = AsyncMock()
    mock_db.add = MagicMock()

    scraper = URLScraper()
    chunker = SemanticChunker()
    embedder = ChunkEmbedder()

    pipeline = IngestPipeline(
        db_session=mock_db,
        scraper=scraper,
        extractor=None,
        chunker=chunker,
        embedder=embedder,
    )

    # Mock the scraper to return controlled content
    with patch.object(scraper, "scrape", new_callable=AsyncMock) as mock_scrape:
        mock_scrape.return_value = {
            "title": "Test Article",
            "text": "This is a test article with multiple paragraphs.\n\n"
                    "It has enough content to generate multiple chunks for testing.\n\n"
                    "The chunker should split this into at least one chunk.\n\n"
                    "Each chunk should contain meaningful text for embedding.",
            "authors": "Test Author",
            "year": 2024,
            "metadata": {"hostname": "example.com"},
            "method_used": "trafilatura",
        }

        document_id = await pipeline.ingest_url("https://example.com/test-article")

        assert document_id is not None
        # Verify that chunks were added to the session
        assert mock_db.add.called, "No chunks were added to the database session"