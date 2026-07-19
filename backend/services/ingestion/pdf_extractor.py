"""
PDF Extraction Service — Phase C of Source Intelligence Layer.

Extracts text and metadata from uploaded PDF files using pypdf.
Supports:
  - Title, author, year extraction from PDF metadata
  - Full text extraction with cleaning
  - Year parsing from /CreationDate metadata
  - Page count tracking
"""

import re
import logging
from pathlib import Path
from typing import Optional

from core.config import get_settings

logger = logging.getLogger(__name__)


class PDFExtractor:
    """
    Extracts text and metadata from PDF files.
    """

    MAX_FILE_SIZE_MB = 50

    def __init__(self):
        self.settings = get_settings()
        self.max_size_bytes = (
            getattr(self.settings, "MAX_PDF_SIZE_MB", self.MAX_FILE_SIZE_MB) * 1024 * 1024
        )

    async def extract(self, file_path: str | Path) -> dict:
        """
        Extract text and metadata from a PDF file.

        Args:
            file_path: Path to the PDF file on disk.

        Returns:
            dict with keys: title, authors, year, text, pages, metadata
        """
        file_path = Path(file_path)

        if not file_path.exists():
            return {"error": "file_not_found", "path": str(file_path)}

        if file_path.stat().st_size > self.max_size_bytes:
            return {
                "error": "file_too_large",
                "path": str(file_path),
                "max_size_mb": self.max_size_bytes / (1024 * 1024),
            }

        if file_path.suffix.lower() != ".pdf":
            return {"error": "not_a_pdf", "path": str(file_path)}

        return self._extract_with_pypdf(file_path)

    def _extract_with_pypdf(self, file_path: Path) -> dict:
        """Extract using pypdf library."""
        try:
            from pypdf import PdfReader
        except ImportError:
            return {"error": "pypdf_not_installed", "path": str(file_path)}

        try:
            reader = PdfReader(str(file_path))
        except Exception as e:
            logger.error("pypdf failed to open %s: %s", file_path, e)
            return {"error": "pdf_read_failed", "path": str(file_path), "message": str(e)}

        # Extract metadata
        meta = reader.metadata or {}
        title = str(meta.get("/Title", "")).strip()
        author = str(meta.get("/Author", "")).strip()
        subject = str(meta.get("/Subject", "")).strip()

        # Extract year from /CreationDate
        year = self._extract_year_from_metadata(meta)

        # Extract text from all pages
        pages_text = []
        for i, page in enumerate(reader.pages):
            try:
                text = page.extract_text() or ""
                pages_text.append(text)
            except Exception as e:
                logger.warning("Failed to extract text from page %d of %s: %s", i, file_path, e)
                pages_text.append("")

        raw_text = "\n\n".join(pages_text)
        cleaned_text = self._clean_text(raw_text)

        return {
            "title": title or file_path.stem,
            "authors": author or "",
            "year": year,
            "text": cleaned_text,
            "pages": len(reader.pages),
            "metadata": {
                "subject": subject,
                "pdf_metadata": {k: str(v) for k, v in meta.items()},
                "filename": file_path.name,
            },
        }

    def _clean_text(self, raw_text: str) -> str:
        """
        Clean extracted PDF text:
        - Remove page headers/footers (repeated lines)
        - Fix broken words across lines: "deriva-\ntion" → "derivation"
        - Normalize whitespace
        - Remove reference list markers that confuse chunking
        """
        # Fix hyphenated line breaks
        text = re.sub(r'(\w)-\n(\w)', r'\1\2', raw_text)

        # Normalize whitespace
        text = re.sub(r'[ \t]+', ' ', text)

        # Remove excessive blank lines (keep max 2)
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Strip each line
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)

        # Remove repeated lines (common page headers/footers)
        # If a line appears 3+ times in the document, it's likely a header/footer
        line_counts = {}
        for line in lines:
            if len(line) > 10 and len(line) < 100:
                line_counts[line] = line_counts.get(line, 0) + 1

        repeated_lines = {line for line, count in line_counts.items() if count >= 3}
        if repeated_lines:
            cleaned_lines = [line for line in lines if line not in repeated_lines]
            text = '\n'.join(cleaned_lines)

        return text.strip()

    def _extract_year_from_metadata(self, metadata) -> Optional[int]:
        """
        Parse year from PDF metadata.
        /CreationDate format: "D:20040101120000" → 2004
        """
        creation_date = str(metadata.get("/CreationDate", ""))
        if creation_date:
            match = re.search(r'D:(\d{4})', creation_date)
            if match:
                year = int(match.group(1))
                if 1900 <= year <= 2100:
                    return year

        # Fallback: search for 4-digit year in title or subject
        for field in ["/Title", "/Subject"]:
            val = str(metadata.get(field, ""))
            match = re.search(r'\b(19|20)\d{2}\b', val)
            if match:
                return int(match.group(0))

        return None