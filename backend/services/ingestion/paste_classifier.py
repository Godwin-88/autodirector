"""
Smart Paste Handler — classifies pasted content and routes to the appropriate
ingestion service.

Supports:
  - URLs (any http/https/www)
  - YouTube URLs (special handling)
  - DOIs (10.XXXX/... — resolves via CrossRef)
  - arXiv IDs (2301.12345)
  - BibTeX entries (@article{...})
  - Plain text blocks (>200 chars)
"""
import re
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class PasteType(str, Enum):
    URL = "url"
    DOI = "doi"
    ARXIV_ID = "arxiv_id"
    BIBTEX = "bibtex"
    PLAIN_TEXT = "plain_text"
    YOUTUBE_URL = "youtube_url"
    UNKNOWN = "unknown"


class PasteClassifier:
    """Classifies pasted content and routes to the appropriate ingestion service."""

    URL_PATTERN = re.compile(r'^https?://|^www\.')
    DOI_PATTERN = re.compile(r'^10\.\d{4,}/\S+')
    ARXIV_PATTERN = re.compile(r'(\d{4}\.\d{4,5}(v\d+)?)$')
    ARXIV_URL_PATTERN = re.compile(r'arxiv\.org/abs/(\d{4}\.\d{4,5})')
    YOUTUBE_PATTERN = re.compile(r'(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)')
    BIBTEX_PATTERN = re.compile(r'^@\w+\{')

    def classify(self, text: str) -> PasteType:
        """Classify the pasted text into a PasteType."""
        text = text.strip()

        # Check for YouTube URLs first (they're also URLs)
        if self.YOUTUBE_PATTERN.search(text):
            return PasteType.YOUTUBE_URL

        # Check for arXiv URLs
        if self.ARXIV_URL_PATTERN.search(text):
            return PasteType.ARXIV_ID

        # Generic URL
        if self.URL_PATTERN.match(text):
            return PasteType.URL

        # DOI
        if self.DOI_PATTERN.match(text):
            return PasteType.DOI

        # arXiv ID
        if self.ARXIV_PATTERN.match(text):
            return PasteType.ARXIV_ID

        # BibTeX entry
        if self.BIBTEX_PATTERN.match(text):
            return PasteType.BIBTEX

        # Plain text (longer than 200 chars)
        if len(text) > 200:
            return PasteType.PLAIN_TEXT

        return PasteType.UNKNOWN

    async def route(self, text: str, episode_id: str = None) -> dict:
        """Classify and route pasted content. Returns an action dict."""
        paste_type = self.classify(text)
        text = text.strip()

        if paste_type == PasteType.URL:
            return {
                "action": "ingest_url",
                "url": text,
                "episode_id": episode_id,
                "paste_type": "url",
            }

        if paste_type == PasteType.YOUTUBE_URL:
            return {
                "action": "ingest_url",
                "url": text,
                "episode_id": episode_id,
                "hint": "youtube",
                "paste_type": "youtube_url",
            }

        if paste_type == PasteType.DOI:
            metadata = await self._resolve_crossref(text)
            url = f"https://doi.org/{text}"
            return {
                "action": "ingest_url",
                "url": url,
                "episode_id": episode_id,
                "metadata": metadata,
                "paste_type": "doi",
            }

        if paste_type == PasteType.ARXIV_ID:
            # Extract the arxiv ID from the text
            match = self.ARXIV_URL_PATTERN.search(text) or self.ARXIV_PATTERN.search(text)
            arxiv_id = match.group(1) if match else text
            return {
                "action": "ingest_arxiv",
                "arxiv_id": arxiv_id,
                "episode_id": episode_id,
                "paste_type": "arxiv_id",
            }

        if paste_type == PasteType.BIBTEX:
            metadata = self._parse_bibtex(text)
            return {
                "action": "create_manual_source",
                "metadata": metadata,
                "episode_id": episode_id,
                "paste_type": "bibtex",
            }

        if paste_type == PasteType.PLAIN_TEXT:
            return {
                "action": "create_text_source",
                "text": text,
                "episode_id": episode_id,
                "paste_type": "plain_text",
            }

        return {
            "action": "unknown",
            "raw": text[:200],
            "paste_type": "unknown",
        }

    async def _resolve_crossref(self, doi: str) -> dict:
        """Resolve a DOI to metadata via the CrossRef API."""
        import httpx

        url = f"https://api.crossref.org/works/{doi}"
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(url)
                if r.status_code == 200:
                    work = r.json()["message"]
                    return {
                        "title": (work.get("title") or [""])[0],
                        "authors": ", ".join(
                            f"{a.get('family', '')} {a.get('given', '')}"
                            for a in work.get("author", [])
                        ),
                        "year": (work.get("published") or {}).get("date-parts", [[None]])[0][0],
                        "journal": (work.get("container-title") or [""])[0],
                        "doi": doi,
                        "publisher": work.get("publisher", ""),
                        "url": work.get("URL", f"https://doi.org/{doi}"),
                    }
        except Exception as e:
            logger.warning("CrossRef lookup failed for DOI %s: %s", doi, e)
            return {"doi": doi}

        return {"doi": doi}

    def _parse_bibtex(self, text: str) -> dict:
        """Simple BibTeX field extractor. Not a full parser."""
        fields = {}
        for match in re.finditer(r'(\w+)\s*=\s*\{([^}]+)\}', text):
            fields[match.group(1).lower()] = match.group(2)

        authors = fields.get("author", "")
        year_raw = fields.get("year", "")
        year = int(year_raw) if year_raw.isdigit() else None

        return {
            "title": fields.get("title", ""),
            "authors": authors,
            "year": year,
            "journal": fields.get("journal", fields.get("booktitle", "")),
            "doi": fields.get("doi", ""),
            "publisher": fields.get("publisher", ""),
            "volume": fields.get("volume", ""),
            "pages": fields.get("pages", ""),
            "source_type": "bibtex",
        }