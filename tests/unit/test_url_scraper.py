"""Tests for the URL scraper service."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock


@pytest.mark.asyncio
async def test_trafilatura_path_returns_content():
    """Test that trafilatura extraction returns dict with title and text."""
    from services.ingestion.url_scraper import URLScraper

    scraper = URLScraper()

    mock_result = {
        "title": "Test Article",
        "text": "This is the article content.",
        "author": "John Doe",
        "date": "2024-01-15",
    }

    with patch("services.ingestion.url_scraper.trafilatura") as mock_traf:
        mock_traf.fetch_url.return_value = "<html>mock</html>"
        mock_traf.extract.return_value = '{"title": "Test Article", "text": "This is the article content.", "author": "John Doe", "date": "2024-01-15", "docmeta": {"confidence": 0.95}}'

        result = await scraper._scrape_trafilatura("https://example.com/article")

        assert result is not None
        assert result["title"] == "Test Article"
        assert "This is the article content" in result["text"]
        assert result["authors"] == "John Doe"
        assert result["year"] == 2024
        assert result["method_used"] == "trafilatura"


@pytest.mark.asyncio
async def test_youtube_url_routes_to_youtube_scraper():
    """Test that YouTube URLs are routed to the YouTube handler."""
    from services.ingestion.url_scraper import URLScraper

    scraper = URLScraper()

    with patch.object(scraper, "_scrape_youtube", new_callable=AsyncMock) as mock_yt:
        mock_yt.return_value = {
            "title": "Test Video",
            "text": "Transcript text here",
            "authors": "Channel Name",
            "year": None,
            "metadata": {"video_id": "abc123"},
            "method_used": "youtube_transcript",
        }

        result = await scraper.scrape("https://www.youtube.com/watch?v=abc123")

        mock_yt.assert_called_once()
        assert result["title"] == "Test Video"
        assert result["method_used"] == "youtube_transcript"


@pytest.mark.asyncio
async def test_pdf_url_routes_to_pdf_extractor():
    """Test that .pdf URLs return a redirect message."""
    from services.ingestion.url_scraper import URLScraper

    scraper = URLScraper()
    result = await scraper.scrape("https://example.com/paper.pdf")

    assert result.get("error") == "pdf_url"
    assert "Route to PDF extractor" in result.get("message", "")


@pytest.mark.asyncio
async def test_all_scrapers_fail_returns_error():
    """Test that when all scrapers fail, an error dict is returned."""
    from services.ingestion.url_scraper import URLScraper

    scraper = URLScraper()

    with patch.object(scraper, "_scrape_trafilatura", new_callable=AsyncMock, return_value=None):
        with patch.object(scraper, "_scrape_beautifulsoup", new_callable=AsyncMock, return_value=None):
            with patch.object(scraper, "_scrape_playwright", new_callable=AsyncMock, return_value=None):
                result = await scraper.scrape("https://example.com/nonexistent")

                assert result.get("error") == "all_scrapers_failed"