"""
Ingestion Pipeline Orchestrator — Phase G of Source Intelligence Layer.

Orchestrates the full ingestion flow for a single source:
  URL → scrape → chunk → embed → store
  PDF → extract → chunk → embed → store

Publishes progress events to Redis for SSE streaming.
"""

import logging
import uuid
from pathlib import Path
from typing import Optional
from datetime import datetime, timezone

from core.config import get_settings

logger = logging.getLogger(__name__)


class IngestPipeline:
    """
    Orchestrates the full ingestion flow for a single source.
    """

    def __init__(self, db_session, scraper, extractor, chunker, embedder):
        self.settings = get_settings()
        self.db = db_session
        self.scraper = scraper
        self.extractor = extractor
        self.chunker = chunker
        self.embedder = embedder
        self._redis = None

    async def _get_redis(self):
        """Lazy init Redis client for progress publishing."""
        if self._redis is None:
            try:
                from core.redis_client import get_redis_client
                self._redis = await get_redis_client()
            except Exception as e:
                logger.warning("Redis unavailable, progress events disabled: %s", e)
        return self._redis

    async def _publish_progress(self, task_id: str, stage: str, progress: int, message: str):
        """Publish ingestion progress to Redis for SSE streaming."""
        redis_conn = await self._get_redis()
        if not redis_conn:
            return
        try:
            import json
            payload = json.dumps({
                "task_id": task_id,
                "stage": stage,
                "progress": progress,
                "message": message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            await redis_conn.publish(f"ingest:{task_id}", payload)
        except Exception as e:
            logger.warning("Failed to publish progress: %s", e)

    async def ingest_url(
        self,
        url: str,
        assigned_episode_id: Optional[str] = None,
        manual_title: Optional[str] = None,
        manual_authors: Optional[str] = None,
        manual_year: Optional[int] = None,
    ) -> str:
        """
        Ingest a URL: scrape → chunk → embed → store.

        Returns:
            document_id (UUID as string)
        """
        from models.source_document import SourceDocument
        from models.source_chunk import SourceChunk
        from models.episode_source import EpisodeSource
        from sqlalchemy import select

        task_id = str(uuid.uuid4())
        await self._publish_progress(task_id, "pending", 0, f"Starting URL ingestion: {url}")

        # 1. Create source_documents record
        doc = SourceDocument(
            id=uuid.uuid4(),
            title=manual_title or url,
            authors=manual_authors or "",
            year=manual_year,
            source_type="url",
            origin_url=url,
            status="pending",
        )
        self.db.add(doc)
        await self.db.flush()
        document_id = str(doc.id)

        await self._publish_progress(task_id, "scraping", 10, f"Scraping URL: {url}")

        # 2. Scrape URL
        try:
            scraped = await self.scraper.scrape(url)
        except Exception as e:
            doc.status = "failed"
            await self.db.commit()
            await self._publish_progress(task_id, "failed", 0, f"Scraping failed: {e}")
            raise

        if scraped.get("error"):
            doc.status = "failed"
            doc.metadata_json = {"error": scraped.get("message", scraped["error"])}
            await self.db.commit()
            await self._publish_progress(task_id, "failed", 0, f"Scraping error: {scraped.get('message')}")
            raise ValueError(f"URL scraping failed: {scraped.get('message')}")

        # If PDF URL, route to PDF ingestion
        if scraped.get("error") == "pdf_url":
            await self._publish_progress(task_id, "redirecting", 15, "PDF URL detected, downloading...")
            # Download PDF
            import httpx
            async with httpx.AsyncClient(follow_redirects=True, timeout=60.0) as client:
                resp = await client.get(url)
                resp.raise_for_status()

            output_dir = Path("output/uploads")
            output_dir.mkdir(parents=True, exist_ok=True)
            pdf_filename = f"{uuid.uuid4()}.pdf"
            pdf_path = output_dir / pdf_filename

            with open(pdf_path, "wb") as f:
                f.write(resp.content)

            doc.file_path = str(pdf_path)
            doc.source_type = "pdf"
            doc.metadata_json = {"original_url": url}
            await self.db.flush()

            # Recurse into PDF ingestion
            return await self.ingest_pdf(
                str(pdf_path),
                assigned_episode_id=assigned_episode_id,
            )

        # 3. Update record with scraped content
        doc.title = manual_title or scraped.get("title") or doc.title
        doc.authors = manual_authors or scraped.get("authors", "")
        doc.year = manual_year or scraped.get("year")
        doc.raw_text = scraped.get("text", "")
        doc.metadata_json = scraped.get("metadata", {})
        doc.metadata_json["method_used"] = scraped.get("method_used")
        await self.db.flush()

        await self._publish_progress(task_id, "chunking", 40, "Chunking text...")

        # 4. Chunk the text
        chunks = self.chunker.chunk(
            scraped.get("text", ""),
            metadata={
                "document_id": document_id,
                "source_title": doc.title,
            },
        )

        if not chunks:
            doc.status = "failed"
            doc.metadata_json["error"] = "No text chunks extracted"
            await self.db.commit()
            await self._publish_progress(task_id, "failed", 0, "No text extracted from URL")
            raise ValueError("No text extracted from URL")

        await self._publish_progress(task_id, "embedding", 60, f"Embedding {len(chunks)} chunks...")

        # 5. Embed and store chunks
        texts = [c["text"] for c in chunks]
        try:
            embeddings = await self.embedder.embed_batch(texts)
        except Exception as e:
            doc.status = "failed"
            await self.db.commit()
            await self._publish_progress(task_id, "failed", 0, f"Embedding failed: {e}")
            raise

        for i, chunk_data in enumerate(chunks):
            embedding = embeddings[i] if i < len(embeddings) else [0.0] * 384
            db_chunk = SourceChunk(
                id=uuid.uuid4(),
                document_id=doc.id,
                chunk_index=chunk_data["chunk_index"],
                text=chunk_data["text"],
                token_count=chunk_data["token_count"],
                embedding=embedding,
                metadata_json=chunk_data.get("metadata"),
            )
            self.db.add(db_chunk)

        doc.chunk_count = len(chunks)
        doc.status = "embedded"
        await self.db.flush()

        # 6. Assign to episode if specified
        if assigned_episode_id:
            episode_link = EpisodeSource(
                episode_id=uuid.UUID(assigned_episode_id),
                document_id=doc.id,
            )
            self.db.add(episode_link)

        await self.db.commit()

        await self._publish_progress(
            task_id, "done", 100,
            f"Ingested {len(chunks)} chunks from: {doc.title[:60]}"
        )

        return document_id

    async def ingest_pdf(
        self,
        file_path: str,
        manual_metadata: dict = None,
        assigned_episode_id: Optional[str] = None,
    ) -> str:
        """
        Ingest a PDF file: extract → chunk → embed → store.

        Returns:
            document_id (UUID as string)
        """
        from models.source_document import SourceDocument
        from models.source_chunk import SourceChunk
        from models.episode_source import EpisodeSource

        manual_metadata = manual_metadata or {}
        task_id = str(uuid.uuid4())

        await self._publish_progress(task_id, "pending", 0, f"Starting PDF ingestion: {file_path}")

        # 1. Create source_documents record
        doc = SourceDocument(
            id=uuid.uuid4(),
            title=manual_metadata.get("title", Path(file_path).stem),
            authors=manual_metadata.get("authors", ""),
            year=manual_metadata.get("year"),
            source_type="pdf",
            file_path=file_path,
            status="pending",
        )
        self.db.add(doc)
        await self.db.flush()
        document_id = str(doc.id)

        await self._publish_progress(task_id, "extracting", 20, "Extracting PDF text...")

        # 2. Extract text
        try:
            extracted = await self.extractor.extract(file_path)
        except Exception as e:
            doc.status = "failed"
            await self.db.commit()
            await self._publish_progress(task_id, "failed", 0, f"PDF extraction failed: {e}")
            raise

        if extracted.get("error"):
            doc.status = "failed"
            doc.metadata_json = {"error": extracted.get("message", extracted["error"])}
            await self.db.commit()
            await self._publish_progress(task_id, "failed", 0, f"PDF error: {extracted.get('message')}")
            raise ValueError(f"PDF extraction failed: {extracted.get('message')}")

        doc.title = manual_metadata.get("title") or extracted.get("title") or doc.title
        doc.authors = manual_metadata.get("authors") or extracted.get("authors", "")
        doc.year = manual_metadata.get("year") or extracted.get("year")
        doc.raw_text = extracted.get("text", "")
        doc.metadata_json = extracted.get("metadata", {})
        await self.db.flush()

        await self._publish_progress(task_id, "chunking", 40, "Chunking text...")

        # 3. Chunk
        chunks = self.chunker.chunk(
            extracted.get("text", ""),
            metadata={
                "document_id": document_id,
                "source_title": doc.title,
                "pages": extracted.get("pages", 0),
            },
        )

        if not chunks:
            doc.status = "failed"
            doc.metadata_json["error"] = "No text chunks extracted"
            await self.db.commit()
            await self._publish_progress(task_id, "failed", 0, "No text extracted from PDF")
            raise ValueError("No text extracted from PDF")

        await self._publish_progress(task_id, "embedding", 60, f"Embedding {len(chunks)} chunks...")

        # 4. Embed and store
        texts = [c["text"] for c in chunks]
        try:
            embeddings = await self.embedder.embed_batch(texts)
        except Exception as e:
            doc.status = "failed"
            await self.db.commit()
            await self._publish_progress(task_id, "failed", 0, f"Embedding failed: {e}")
            raise

        for i, chunk_data in enumerate(chunks):
            embedding = embeddings[i] if i < len(embeddings) else [0.0] * 384
            db_chunk = SourceChunk(
                id=uuid.uuid4(),
                document_id=doc.id,
                chunk_index=chunk_data["chunk_index"],
                text=chunk_data["text"],
                token_count=chunk_data["token_count"],
                embedding=embedding,
                metadata_json=chunk_data.get("metadata"),
            )
            self.db.add(db_chunk)

        doc.chunk_count = len(chunks)
        doc.status = "embedded"
        await self.db.flush()

        if assigned_episode_id:
            episode_link = EpisodeSource(
                episode_id=uuid.UUID(assigned_episode_id),
                document_id=doc.id,
            )
            self.db.add(episode_link)

        await self.db.commit()

        await self._publish_progress(
            task_id, "done", 100,
            f"Ingested {len(chunks)} chunks from: {doc.title[:60]}"
        )

        return document_id

    async def ingest_status(self, document_id: str) -> dict:
        """Returns current ingestion status from source_documents table."""
        from models.source_document import SourceDocument
        from sqlalchemy import select

        result = await self.db.execute(
            select(SourceDocument).where(SourceDocument.id == document_id)
        )
        doc = result.scalar_one_or_none()
        if not doc:
            return {"error": "not_found", "document_id": document_id}

        return {
            "id": str(doc.id),
            "title": doc.title,
            "source_type": doc.source_type,
            "status": doc.status,
            "chunk_count": doc.chunk_count,
            "ingested_at": doc.ingested_at.isoformat() if doc.ingested_at else None,
        }

    async def assign_to_episode(
        self, document_id: str, episode_id: str
    ) -> None:
        """Assign a source document to an episode."""
        from models.episode_source import EpisodeSource
        from sqlalchemy import select

        # Check if already assigned
        result = await self.db.execute(
            select(EpisodeSource).where(
                EpisodeSource.episode_id == episode_id,
                EpisodeSource.document_id == document_id,
            )
        )
        if result.scalar_one_or_none():
            logger.info("Document %s already assigned to episode %s", document_id, episode_id)
            return

        link = EpisodeSource(
            episode_id=uuid.UUID(episode_id),
            document_id=uuid.UUID(document_id),
        )
        self.db.add(link)
        await self.db.commit()