"""
Chunk Embedder — Phase D of Source Intelligence Layer.

Embeds text chunks using Qwen's text-embedding-v3 model.
Falls back to sentence-transformers if Qwen embedding quota exceeded.
"""

import logging
from typing import List, Optional

from core.config import get_settings

logger = logging.getLogger(__name__)


class ChunkEmbedder:
    """
    Embeds text chunks using Qwen's text-embedding model.
    Falls back to sentence-transformers if Qwen embedding quota exceeded.
    """

    QWEN_EMBEDDING_MODEL = "text-embedding-v3"
    LOCAL_FALLBACK_MODEL = "all-MiniLM-L6-v2"
    BATCH_SIZE = 32

    def __init__(self):
        self.settings = get_settings()
        self._local_model = None
        self._qwen_client = None

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a batch of texts. Tries Qwen API first, falls back to local model.

        Args:
            texts: List of text strings to embed.

        Returns:
            List of embedding vectors (list of floats).
        """
        if not texts:
            return []

        # Try Qwen embedding API
        try:
            return await self._embed_with_qwen(texts)
        except Exception as e:
            logger.warning("Qwen embedding failed, falling back to local model: %s", e)
            return self._embed_with_local(texts)

    async def _embed_with_qwen(self, texts: List[str]) -> List[List[float]]:
        """Embed using Qwen's text-embedding-v3 API."""
        from openai import AsyncOpenAI

        client = AsyncOpenAI(
            api_key=self.settings.QWEN_API_KEY,
            base_url=self.settings.QWEN_BASE_URL,
        )

        all_embeddings = []
        for i in range(0, len(texts), self.BATCH_SIZE):
            batch = texts[i:i + self.BATCH_SIZE]
            response = await client.embeddings.create(
                model=self.QWEN_EMBEDDING_MODEL,
                input=batch,
            )
            # Sort by index to maintain order
            sorted_data = sorted(response.data, key=lambda x: x.index)
            all_embeddings.extend([item.embedding for item in sorted_data])

        return all_embeddings

    def _embed_with_local(self, texts: List[str]) -> List[List[float]]:
        """Fallback: embed using local sentence-transformers model."""
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            logger.error("sentence-transformers not installed, cannot embed locally")
            return [[0.0] * 384 for _ in texts]  # Return zero vectors as last resort

        if self._local_model is None:
            logger.info("Loading local embedding model: %s", self.LOCAL_FALLBACK_MODEL)
            self._local_model = SentenceTransformer(self.LOCAL_FALLBACK_MODEL)

        embeddings = self._local_model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()

    async def embed_document_chunks(
        self,
        chunks: List[dict],
        document_id: str,
        db_session,
    ) -> int:
        """
        Embed all chunks for a document and store them in the database.

        Args:
            chunks: List of chunk dicts from SemanticChunker.
            document_id: UUID of the source_document.
            db_session: SQLAlchemy async session.

        Returns:
            Number of chunks embedded.
        """
        if not chunks:
            return 0

        texts = [chunk["text"] for chunk in chunks]
        embeddings = await self.embed_batch(texts)

        from models.source_chunk import SourceChunk
        from models.source_document import SourceDocument
        from sqlalchemy import select, update

        for i, chunk_data in enumerate(chunks):
            embedding = embeddings[i] if i < len(embeddings) else [0.0] * 384
            db_chunk = SourceChunk(
                document_id=document_id,
                chunk_index=chunk_data["chunk_index"],
                text=chunk_data["text"],
                token_count=chunk_data["token_count"],
                embedding=embedding,  # stored as JSONB list
                metadata_json=chunk_data.get("metadata"),
            )
            db_session.add(db_chunk)

        # Update document status
        stmt = (
            update(SourceDocument)
            .where(SourceDocument.id == document_id)
            .values(
                chunk_count=len(chunks),
                status="embedded",
            )
        )
        await db_session.execute(stmt)
        await db_session.commit()

        logger.info(
            "Embedded %d chunks for document %s",
            len(chunks), document_id
        )
        return len(chunks)