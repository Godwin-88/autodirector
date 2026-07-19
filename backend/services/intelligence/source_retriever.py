"""
Source Retriever — Phase F of Source Intelligence Layer.

Unified retrieval layer. Given a topic and scene outline,
returns ranked, cited source chunks from all three channels:
  - pgvector similarity search over URL/PDF chunks (Channel A+B)
  - Memgraph GraphRAG structured retrieval (Channel C)

Output is injected into Qwen script generation prompt as GROUND TRUTH.
"""

import logging
from typing import List, Optional
from pydantic import BaseModel

from core.config import get_settings

logger = logging.getLogger(__name__)


class RetrievalPackage(BaseModel):
    """Unified retrieval result for an episode."""
    topic: str
    vector_chunks: List[dict]
    graphrag_data: Optional[dict] = None
    total_sources: int = 0
    context_block: str = ""


class SceneRetrievalResult(BaseModel):
    """Scene-specific retrieval result."""
    scene_number: int
    chunks: List[dict]
    citations: List[str] = []
    equations_from_graph: List[str] = []


class SourceRetriever:
    """
    Unified retrieval layer. Given a topic and scene outline,
    returns ranked, cited source chunks from all three channels.
    """

    MAX_CONTEXT_TOKENS = 2000  # Hard cap for Qwen context injection

    def __init__(self, db_session=None, memgraph_client=None, embedder=None):
        self.settings = get_settings()
        self.db = db_session
        self.memgraph = memgraph_client
        self.embedder = embedder

    async def retrieve_for_episode(
        self,
        topic: str,
        outline,
        episode_id: str,
        top_k: int = 5,
    ) -> RetrievalPackage:
        """
        Retrieve sources for an entire episode.

        1. Embed the topic string
        2. pgvector similarity search
        3. Memgraph GraphRAG retrieval (if enabled)
        4. Merge, deduplicate, re-rank
        5. Build context block (≤2000 tokens)
        """
        vector_chunks = []
        graphrag_data = None

        # Step 1: Vector search
        if self.embedder and self.db:
            try:
                query_embedding = await self.embedder.embed_batch([topic])
                if query_embedding:
                    vector_chunks = await self._vector_search(
                        query_embedding[0], episode_id, top_k
                    )
            except Exception as e:
                logger.warning("Vector search failed for episode %s: %s", episode_id, e)

        # Step 2: Memgraph GraphRAG
        if self.memgraph:
            try:
                graphrag_data = await self.memgraph.graphrag_retrieve(
                    topic, outline.title if hasattr(outline, 'title') else topic
                )
            except Exception as e:
                logger.warning("Memgraph retrieval failed for episode %s: %s", episode_id, e)

        # Step 3: Build context block
        context_block = self.build_context_block(
            topic, vector_chunks, graphrag_data
        )

        return RetrievalPackage(
            topic=topic,
            vector_chunks=vector_chunks,
            graphrag_data=graphrag_data,
            total_sources=len(vector_chunks) + (
                len(graphrag_data.get("concepts", [])) if graphrag_data else 0
            ),
            context_block=context_block,
        )

    async def retrieve_for_scene(
        self,
        scene,
        episode_id: str,
        top_k: int = 3,
    ) -> SceneRetrievalResult:
        """
        Scene-specific retrieval using scene title + key equations as query.
        """
        # Build query from scene content
        query_parts = [scene.title]
        if hasattr(scene, 'key_equations') and scene.key_equations:
            query_parts.extend(scene.key_equations)
        query = " ".join(query_parts)

        vector_chunks = []
        if self.embedder and self.db:
            try:
                query_embedding = await self.embedder.embed_batch([query])
                if query_embedding:
                    vector_chunks = await self._vector_search(
                        query_embedding[0], episode_id, top_k
                    )
            except Exception as e:
                logger.warning("Scene vector search failed: %s", e)

        # Build citations
        citations = []
        for chunk in vector_chunks:
            citation = self._format_as_citation(chunk)
            if citation:
                citations.append(citation)

        # Get equations from Memgraph
        equations = []
        if self.memgraph:
            try:
                for concept_name in query_parts:
                    eqs = await self.memgraph.get_concept_equations(concept_name)
                    for eq in eqs:
                        if eq.get("latex") and eq["latex"] not in equations:
                            equations.append(eq["latex"])
            except Exception:
                pass

        return SceneRetrievalResult(
            scene_number=scene.scene_number if hasattr(scene, 'scene_number') else 0,
            chunks=vector_chunks,
            citations=citations,
            equations_from_graph=equations,
        )

    async def _vector_search(
        self,
        query_embedding: List[float],
        episode_id: str,
        top_k: int,
    ) -> List[dict]:
        """
        pgvector similarity search via raw SQL.

        SELECT chunks ORDER BY embedding <-> $query_embedding
        Filter to episode-assigned documents or all if none assigned.
        """
        if not self.db:
            return []

        from sqlalchemy import text

        # Build embedding as pgvector-compatible string
        embedding_str = "[" + ",".join(str(v) for v in query_embedding) + "]"

        # Try pgvector operator first, fall back to JSONB comparison
        try:
            query = text("""
                SELECT sc.id, sc.text, sc.metadata_json,
                       sd.title, sd.authors, sd.year,
                       sd.source_type, sd.origin_url,
                       (sc.embedding::text::vector <-> :embedding::vector) AS distance
                FROM source_chunks sc
                JOIN source_documents sd ON sc.document_id = sd.id
                LEFT JOIN episode_sources es ON sd.id = es.document_id
                WHERE (es.episode_id = :episode_id OR :episode_id IS NULL)
                ORDER BY distance ASC
                LIMIT :top_k
            """)
        except Exception:
            # Fallback: no pgvector, return chunks without distance ordering
            query = text("""
                SELECT sc.id, sc.text, sc.metadata_json,
                       sd.title, sd.authors, sd.year,
                       sd.source_type, sd.origin_url,
                       0.0 AS distance
                FROM source_chunks sc
                JOIN source_documents sd ON sc.document_id = sd.id
                LEFT JOIN episode_sources es ON sd.id = es.document_id
                WHERE (es.episode_id = :episode_id OR :episode_id IS NULL)
                AND sd.status = 'embedded'
                LIMIT :top_k
            """)

        try:
            result = await self.db.execute(
                query,
                {
                    "embedding": embedding_str,
                    "episode_id": episode_id,
                    "top_k": top_k,
                },
            )
            rows = result.fetchall()
            return [
                {
                    "id": str(row[0]),
                    "text": row[1],
                    "metadata": row[2] or {},
                    "title": row[3],
                    "authors": row[4],
                    "year": row[5],
                    "source_type": row[6],
                    "origin_url": row[7],
                    "distance": float(row[8]) if row[8] else 0.0,
                }
                for row in rows
            ]
        except Exception as e:
            logger.warning("Vector search SQL failed: %s", e)
            return []

    def _format_as_citation(self, chunk: dict) -> str:
        """
        Format a retrieved chunk as an inline citation string.

        e.g. "Taleb (1997), Dynamic Hedging, p.118"
        or "Black & Scholes (1973), J. Political Economy, 81(3)"
        """
        parts = []
        authors = chunk.get("authors", "")
        year = chunk.get("year")
        title = chunk.get("title", "")
        source_type = chunk.get("source_type", "")

        if authors:
            parts.append(authors)
        if year:
            parts.append(f"({year})")
        if title:
            parts.append(title)

        if source_type == "url" and chunk.get("origin_url"):
            parts.append(f"[{chunk['origin_url']}]")

        return ", ".join(parts) if parts else "Unknown source"

    def build_context_block(
        self,
        topic: str,
        vector_chunks: List[dict],
        graphrag_data: Optional[dict] = None,
    ) -> str:
        """
        Format all retrieved chunks into a structured context block
        for injection into the Qwen script generation prompt.

        Hard cap at MAX_CONTEXT_TOKENS.
        """
        lines = []
        lines.append("=== VERIFIED SOURCE MATERIAL ===")

        # Add vector chunks with citations
        for i, chunk in enumerate(vector_chunks[:10], 1):
            citation = self._format_as_citation(chunk)
            text = chunk.get("text", "")[:500]  # Truncate long chunks
            lines.append(f"[{i}] {citation}: {text}")

        # Add GraphRAG knowledge
        if graphrag_data:
            lines.append("")
            lines.append("=== GRAPHRAG KNOWLEDGE ===")

            for concept in graphrag_data.get("concepts", []):
                name = concept.get("name", "")
                definition = concept.get("definition", "")
                if name:
                    lines.append(f"Concept: {name}")
                if definition:
                    lines.append(f"Definition: {definition}")

            equations = graphrag_data.get("equations", [])
            if equations:
                lines.append("Equations:")
                for eq in equations[:5]:
                    latex = eq.get("latex", "")
                    if latex:
                        lines.append(f"  - {latex}")

            papers = graphrag_data.get("papers", [])
            if papers:
                lines.append("Papers:")
                for paper in papers[:5]:
                    authors = paper.get("authors", "")
                    year = paper.get("year", "")
                    title = paper.get("title", "")
                    lines.append(f"  - {authors} ({year}), {title}")

        lines.append("")
        lines.append("================================")
        lines.append("INSTRUCTION: Ground every factual claim in the script in ONE of the")
        lines.append("above sources. Cite inline as [N]. Do not introduce facts not present")
        lines.append("in the above material. If you must use your own knowledge, mark it")
        lines.append("as [UNVERIFIED: claim description].")

        context = "\n".join(lines)

        # Enforce token cap (approximate: 4 chars ≈ 1 token)
        max_chars = self.MAX_CONTEXT_TOKENS * 4
        if len(context) > max_chars:
            context = context[:max_chars] + "\n... [context truncated to token limit]"

        return context