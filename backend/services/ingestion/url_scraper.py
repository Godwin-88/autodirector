"""
URL Scraper Service — Phase B of Source Intelligence Layer.

Strategy cascade:
  1. trafilatura (fastest, best for articles/papers)
  2. BeautifulSoup fallback (for non-standard layouts)
  3. Playwright headless browser (for JS-rendered pages — last resort)

Special URL patterns handled:
  - arxiv.org/abs/XXXX → scrape abstract + fetch PDF link
  - doi.org/... → resolve DOI redirect, then scrape
  - youtube.com/watch?v=... → extract transcript via youtube_transcript_api
  - *.pdf URL → download and route to PDF extractor
"""

import re
import json
import logging
from typing import Optional
from urllib.parse import urlparse, parse_qs

import httpx
from bs4 import BeautifulSoup

from core.config import get_settings

logger = logging.getLogger(__name__)


class URLScraper:
    """
    Scrapes a URL and extracts clean article text using a strategy cascade.
    """

    def __init__(self):
        self.settings = get_settings()
        self.playwright_enabled = getattr(self.settings, "PLAYWRIGHT_ENABLED", True)

    async def scrape(self, url: str) -> dict:
        """
        Main entry point. Scrapes the given URL and returns structured content.

        Returns:
            dict with keys: title, text, authors, year, metadata, method_used
        """
        url = url.strip()

        # Route to specialised handlers based on URL pattern
        if re.match(r'^https?://(www\.)?arxiv\.org/abs/', url):
            return await self._scrape_arxiv(url)
        elif re.match(r'^https?://(www\.)?doi\.org/', url):
            return await self._scrape_doi(url)
        elif re.match(r'^https?://(www\.)?youtube\.com/watch', url) or \
             re.match(r'^https?://youtu\.be/', url):
            return await self._scrape_youtube(url)
        elif url.lower().endswith('.pdf'):
            return {"error": "pdf_url", "url": url,
                    "message": "Route to PDF extractor for PDF URLs"}

        # Generic URL: try strategy cascade
        result = await self._scrape_trafilatura(url)
        if result:
            return result

        result = await self._scrape_beautifulsoup(url)
        if result:
            return result

        if self.playwright_enabled:
            result = await self._scrape_playwright(url)
            if result:
                return result

        return {"error": "all_scrapers_failed", "url": url,
                "message": "Could not extract content from URL"}

    async def _scrape_trafilatura(self, url: str) -> Optional[dict]:
        """Try trafilatura extraction (fastest, best for articles)."""
        try:
            import trafilatura
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                logger.info("trafilatura: no content downloaded from %s", url)
                return None

            result_json = trafilatura.extract(
                downloaded,
                include_metadata=True,
                output_format="json",
                include_comments=False,
                include_tables=True,
                no_fallback=False,
            )
            if not result_json:
                return None

            data = json.loads(result_json)
            confidence = data.get("docmeta", {}).get("confidence", 0)
            if confidence < 0.5:
                logger.info("trafilatura: confidence %.2f too low for %s", confidence, url)
                return None

            title = data.get("title", "")
            text = data.get("text", "")
            author_raw = data.get("author", "")
            date_raw = data.get("date", "")
            year = None
            if date_raw:
                match = re.search(r'\b(19|20)\d{2}\b', date_raw)
                if match:
                    year = int(match.group(0))

            return {
                "title": title or "Untitled",
                "text": text,
                "authors": author_raw or "",
                "year": year,
                "metadata": {
                    "hostname": urlparse(url).hostname,
                    "trafilatura_confidence": confidence,
                },
                "method_used": "trafilatura",
            }
        except ImportError:
            logger.warning("trafilatura not installed, skipping")
            return None
        except Exception as e:
            logger.warning("trafilatura failed for %s: %s", url, e)
            return None

    async def _scrape_beautifulsoup(self, url: str) -> Optional[dict]:
        """Fallback: BeautifulSoup extraction for non-standard layouts."""
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
                response = await client.get(url, headers={
                    "User-Agent": (
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                    ),
                })
                response.raise_for_status()
        except Exception as e:
            logger.warning("httpx failed for %s: %s", url, e)
            return None

        soup = BeautifulSoup(response.text, "lxml")

        # Remove unwanted elements
        for tag in soup(["nav", "header", "footer", "aside", "script", "style",
                         "noscript", "iframe", "form"]):
            tag.decompose()

        # Extract title
        title = ""
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        if not title:
            h1 = soup.find("h1")
            if h1:
                title = h1.get_text(strip=True)

        # Extract body text — prefer <article> or <main>
        article = soup.find("article") or soup.find("main") or soup.find("body")
        text = article.get_text(separator="\n", strip=True) if article else ""

        # Clean text
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        text = "\n".join(lines)

        # Extract academic metadata
        meta = self._detect_academic_metadata(url, soup)

        return {
            "title": title or "Untitled",
            "text": text,
            "authors": ", ".join(meta.get("authors", [])),
            "year": meta.get("year"),
            "metadata": {
                "hostname": urlparse(url).hostname,
                "doi": meta.get("doi"),
                "journal": meta.get("journal"),
            },
            "method_used": "beautifulsoup",
        }

    async def _scrape_playwright(self, url: str) -> Optional[dict]:
        """Last resort: Playwright headless browser for JS-rendered pages."""
        if not self.playwright_enabled:
            return None
        try:
            from playwright.async_api import async_playwright

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                try:
                    await page.goto(url, wait_until="networkidle", timeout=30000)
                except Exception:
                    # Fallback to domcontentloaded if networkidle times out
                    await page.goto(url, wait_until="domcontentloaded", timeout=30000)

                content = await page.content()
                await browser.close()

            soup = BeautifulSoup(content, "lxml")
            for tag in soup(["nav", "header", "footer", "aside", "script", "style"]):
                tag.decompose()

            title = ""
            if soup.title and soup.title.string:
                title = soup.title.string.strip()
            if not title:
                h1 = soup.find("h1")
                if h1:
                    title = h1.get_text(strip=True)

            article = soup.find("article") or soup.find("main") or soup.find("body")
            text = article.get_text(separator="\n", strip=True) if article else ""

            # Check for paywall indicators
            paywall_keywords = ["subscribe to access", "purchase this article",
                                "paywall", "subscription required"]
            if any(kw in text.lower()[:2000] for kw in paywall_keywords):
                return {"error": "paywall_detected", "url": url,
                        "message": "Content is behind a paywall"}

            meta = self._detect_academic_metadata(url, soup)

            return {
                "title": title or "Untitled",
                "text": text,
                "authors": ", ".join(meta.get("authors", [])),
                "year": meta.get("year"),
                "metadata": {
                    "hostname": urlparse(url).hostname,
                    "doi": meta.get("doi"),
                    "journal": meta.get("journal"),
                },
                "method_used": "playwright",
            }
        except ImportError:
            logger.warning("playwright not installed, skipping")
            return None
        except Exception as e:
            logger.warning("playwright failed for %s: %s", url, e)
            return None

    async def _scrape_arxiv(self, url: str) -> dict:
        """Handle arxiv.org/abs/XXXX — scrape abstract + fetch PDF link."""
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
                response = await client.get(url, headers={
                    "User-Agent": "QuantifayaAutoDirector/1.0"
                })
                response.raise_for_status()
        except Exception as e:
            return {"error": "arxiv_fetch_failed", "url": url, "message": str(e)}

        soup = BeautifulSoup(response.text, "lxml")

        # Extract arXiv ID
        arxiv_id = url.rstrip("/").split("/")[-1]

        # Title
        title_tag = soup.find("h1", class_="title")
        title = title_tag.get_text(strip=True).replace("Title:", "").strip() if title_tag else ""

        # Authors
        authors_tag = soup.find("div", class_="authors")
        authors = authors_tag.get_text(strip=True).replace("Authors:", "").strip() if authors_tag else ""

        # Abstract
        abstract_tag = soup.find("blockquote", class_="abstract")
        abstract = abstract_tag.get_text(strip=True).replace("Abstract:", "").strip() if abstract_tag else ""

        # Year from dateline
        year = None
        dateline = soup.find("div", class_="dateline")
        if dateline:
            match = re.search(r'\b(19|20)\d{2}\b', dateline.get_text())
            if match:
                year = int(match.group(0))

        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

        return {
            "title": title or f"arXiv:{arxiv_id}",
            "text": abstract,
            "authors": authors,
            "year": year,
            "metadata": {
                "arxiv_id": arxiv_id,
                "pdf_url": pdf_url,
                "hostname": "arxiv.org",
            },
            "method_used": "arxiv_specialized",
        }

    async def _scrape_doi(self, url: str) -> dict:
        """Handle doi.org/... — resolve DOI redirect, then scrape."""
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
                response = await client.get(url, headers={
                    "User-Agent": "QuantifayaAutoDirector/1.0"
                })
                final_url = str(response.url)
                response.raise_for_status()
        except Exception as e:
            return {"error": "doi_resolve_failed", "url": url, "message": str(e)}

        # If redirected to a known publisher, scrape the final URL
        return await self.scrape(final_url)

    async def _scrape_youtube(self, url: str) -> dict:
        """Extract YouTube transcript and metadata."""
        try:
            from youtube_transcript_api import YouTubeTranscriptApi

            # Extract video_id from URL
            parsed = urlparse(url)
            if "youtu.be" in parsed.netloc:
                video_id = parsed.path.lstrip("/")
            else:
                query_params = parse_qs(parsed.query)
                video_id = query_params.get("v", [None])[0]

            if not video_id:
                return {"error": "invalid_youtube_url", "url": url}

            # Get transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            full_text = " ".join(entry["text"] for entry in transcript_list)

            # Get title/author via oEmbed (no API key required)
            title = ""
            author = ""
            try:
                oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.get(oembed_url)
                    if resp.status_code == 200:
                        data = resp.json()
                        title = data.get("title", "")
                        author = data.get("author_name", "")
            except Exception:
                pass

            return {
                "title": title or f"YouTube Video ({video_id})",
                "text": full_text,
                "authors": author,
                "year": None,
                "metadata": {
                    "video_id": video_id,
                    "source": "youtube_transcript",
                    "hostname": "youtube.com",
                },
                "method_used": "youtube_transcript",
            }
        except ImportError:
            return {"error": "youtube_transcript_api_not_installed", "url": url}
        except Exception as e:
            return {"error": "youtube_failed", "url": url, "message": str(e)}

    def _detect_academic_metadata(self, url: str, soup: BeautifulSoup) -> dict:
        """
        Extract academic metadata from HTML meta tags.
        Handles Google Scholar citation meta tags used by most academic publishers.
        """
        result: dict = {"doi": None, "journal": None, "authors": [], "year": None}

        # DOI from URL or meta tags
        doi_match = re.search(r'10\.\d{4,}/[\w\.\-/]+', url)
        if doi_match:
            result["doi"] = doi_match.group(0)

        for meta in soup.find_all("meta"):
            name = (meta.get("name") or "").lower()
            content = (meta.get("content") or "").strip()

            if name == "citation_doi" and not result["doi"]:
                result["doi"] = content
            elif name == "citation_journal_title":
                result["journal"] = content
            elif name == "citation_author":
                result["authors"].append(content)
            elif name == "citation_date" or name == "citation_publication_date":
                match = re.search(r'\b(19|20)\d{2}\b', content)
                if match:
                    result["year"] = int(match.group(0))
            elif name == "citation_title" and not soup.title:
                pass  # title already extracted

        return result