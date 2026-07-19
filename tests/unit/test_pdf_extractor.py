"""Tests for the PDF extraction service."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock


@pytest.fixture
def minimal_pdf():
    """Create a minimal valid PDF for testing."""
    # Minimal PDF content (valid PDF with "Hello World" text)
    pdf_content = (
        b"%PDF-1.4\n"
        b"1 0 obj\n"
        b"<< /Type /Catalog /Pages 2 0 R >>\n"
        b"endobj\n"
        b"2 0 obj\n"
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>\n"
        b"endobj\n"
        b"3 0 obj\n"
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]\n"
        b"   /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\n"
        b"endobj\n"
        b"4 0 obj\n"
        b"<< /Length 44 >>\n"
        b"stream\n"
        b"BT /F1 12 Tf 100 700 Td (Hello World) Tj ET\n"
        b"endstream\n"
        b"endobj\n"
        b"5 0 obj\n"
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\n"
        b"endobj\n"
        b"xref\n"
        b"0 6\n"
        b"0000000000 65535 f \n"
        b"0000000009 00000 n \n"
        b"0000000058 00000 n \n"
        b"0000000115 00000 n \n"
        b"0000000266 00000 n \n"
        b"0000000363 00000 n \n"
        b"trailer\n"
        b"<< /Size 6 /Root 1 0 R >>\n"
        b"startxref\n"
        b"435\n"
        b"%%EOF"
    )
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f.write(pdf_content)
        path = f.name
    yield path
    Path(path).unlink(missing_ok=True)


@pytest.mark.asyncio
async def test_pdf_extraction_returns_title_and_text(minimal_pdf):
    """Test that PDF extraction returns title and text content."""
    from services.ingestion.pdf_extractor import PDFExtractor

    extractor = PDFExtractor()
    result = await extractor.extract(minimal_pdf)

    assert "error" not in result, f"Extraction failed: {result.get('error')}"
    assert result["title"] is not None
    assert result["pages"] >= 1
    assert isinstance(result["text"], str)


@pytest.mark.asyncio
async def test_pdf_year_parsed_from_metadata():
    """Test that year is parsed from /CreationDate metadata."""
    from services.ingestion.pdf_extractor import PDFExtractor

    extractor = PDFExtractor()

    # Mock metadata with /CreationDate
    mock_metadata = MagicMock()
    mock_metadata.get = MagicMock(side_effect=lambda key, default=None: {
        "/CreationDate": "D:20240101120000",
        "/Title": "Test Paper",
    }.get(key, default))

    year = extractor._extract_year_from_metadata(mock_metadata)
    assert year == 2024


@pytest.mark.asyncio
async def test_pdf_file_not_found():
    """Test that missing file returns error."""
    from services.ingestion.pdf_extractor import PDFExtractor

    extractor = PDFExtractor()
    result = await extractor.extract("/nonexistent/path.pdf")

    assert result.get("error") == "file_not_found"


@pytest.mark.asyncio
async def test_pdf_not_a_pdf():
    """Test that non-PDF file returns error."""
    from services.ingestion.pdf_extractor import PDFExtractor

    extractor = PDFExtractor()
    result = await extractor.extract("/tmp/test.txt")

    assert result.get("error") == "not_a_pdf"