"""
Source Ingestion and Retrieval API Routes — Phase I of Source Intelligence Layer.

Endpoints:
  POST   /api/v1/sources/url          — ingest a URL (async, returns task_id)
  POST   /api/v1/sources/pdf          — upload and ingest a PDF file
  GET    /api/v1/sources              — list all ingested sources
  GET    /api/v1/sources/{id}         — get source detail + chunk count
  DELETE /api/v1/sources/{id}         — delete source + all chunks
  POST   /api/v1/sources/{id}/assign  — assign source to an episode
  GET    /api/v1/sources/{id}/chunks  — list chunks (paginated)
  POST   /api/v1/sources/search       — semantic search across all sources
  GET    /api/v1/sources/ingest/{task_id} — check ingestion task status

  POST   /api/v1/episodes/{id}/sources         — add a source to this episode
  GET    /api/v1/episodes/{id}/sources         — list sources for this episode
  DELETE /api/v1/episodes/{id}/sources/{src_id} — remove source from episode

  GET    /api/v1/memgraph/health       — check Memgraph connection
  GET    /api/v1/memgraph/concept/{name} — retrieve concept subgraph
  POST   /api/v1/memgraph/search       — search concepts by text
"""

import uuid
import json
import logging
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from pydantic import BaseModel

from core.config import get_settings
from core.database import get_async_session_local
from services.ingestion.url_scraper import URLScraper
from services.ingestion.pdf_extractor import PDFExtractor
from services.ingestion.chunker import SemanticChunker
from services.ingestion.embedder import ChunkEmbedder
from services.ingestion.ingest_pipeline import IngestPipeline
from services.ingestion.memgraph_client import MemgraphClient

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["sources"])


# --- Request/Response Models ---

class URLIngestRequest(BaseModel):
    url: str
    episode_id: Optional[str] = None
    manual_title: Optional[str] = None
    manual_authors: Optional[str] = None
    manual_year: Optional[int] = None


class URLIngestResponse(BaseModel):
    task_id: str
    document_id: str
    status: str = "queued"


class SourceSearchRequest(BaseModel):
    query: str
    episode_id: Optional[str] = None
    top_k: int = 5


class MemgraphSearchRequest(BaseModel):
    query: str
    limit: int = 10


# --- Dependency Injection ---

async def get_ingest_pipeline(db=Depends(get_async_session_local)) -> IngestPipeline:
    scraper = URLScraper()
    extractor = PDFExtractor()
    chunker = SemanticChunker()
    embedder = ChunkEmbedder()
    return IngestPipeline(
        db_session=db,
        scraper=scraper,
        extractor=extractor,
        chunker=chunker,
        embedder=embedder,
    )


async def get_memgraph_client() -> MemgraphClient:
    return MemgraphClient()


# --- Source Ingestion Endpoints ---

@router.post("/sources/url", response_model=URLIngestResponse)
async def ingest_url(
    request: URLIngestRequest,
    pipeline: IngestPipeline = Depends(get_ingest_pipeline),
):
    """Ingest a URL: scrape → chunk → embed → store."""
    try:
        document_id = await pipeline.ingest_url(
            url=request.url,
            assigned_episode_id=request.episode_id,
            manual_title=request.manual_title,
            manual_authors=request.manual_authors,
            manual_year=request.manual_year,
        )
        return URLIngestResponse(
            task_id=str(uuid.uuid4()),
            document_id=document_id,
            status="completed",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("URL ingestion failed")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")


@router.post("/sources/pdf", response_model=URLIngestResponse)
async def ingest_pdf(
    file: UploadFile = File(...),
    episode_id: Optional[str] = Form(None),
    title: Optional[str] = Form(None),
    authors: Optional[str] = Form(None),
    year: Optional[int] = Form(None),
    pipeline: IngestPipeline = Depends(get_ingest_pipeline),
):
    """Upload and ingest a PDF file."""
    # Validate file type
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    # Validate file size (50MB max)
    max_size = 50 * 1024 * 1024
    contents = await file.read()
    if len(contents) > max_size:
        raise HTTPException(status_code=400, detail="File exceeds 50MB limit")

    # Save to output/uploads/
    output_dir = Path("output/uploads")
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / f"{uuid.uuid4()}_{file.filename}"

    with open(pdf_path, "wb") as f:
        f.write(contents)

    try:
        document_id = await pipeline.ingest_pdf(
            file_path=str(pdf_path),
            manual_metadata={
                "title": title,
                "authors": authors,
                "year": year,
            },
            assigned_episode_id=episode_id,
        )
        return URLIngestResponse(
            task_id=str(uuid.uuid4()),
            document_id=document_id,
            status="completed",
        )
    except ValueError as e:
        # Clean up failed file
        if pdf_path.exists():
            pdf_path.unlink()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("PDF ingestion failed")
        if pdf_path.exists():
            pdf_path.unlink()
        raise HTTPException(status_code=500, detail=f"PDF ingestion failed: {e}")


@router.get("/sources")
async def list_sources(
    source_type: Optional[str] = Query(None, description="Filter by source type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    db=Depends(get_async_session_local),
):
    """List all ingested sources with optional filters."""
    from models.source_document import SourceDocument
    from sqlalchemy import select, func

    query = select(SourceDocument).order_by(SourceDocument.ingested_at.desc())

    if source_type:
        query = query.where(SourceDocument.source_type == source_type)
    if status:
        query = query.where(SourceDocument.status == status)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Get paginated results
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    docs = result.scalars().all()

    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "sources": [
            {
                "id": str(doc.id),
                "title": doc.title,
                "authors": doc.authors,
                "year": doc.year,
                "source_type": doc.source_type,
                "origin_url": doc.origin_url,
                "chunk_count": doc.chunk_count,
                "status": doc.status,
                "ingested_at": doc.ingested_at.isoformat() if doc.ingested_at else None,
            }
            for doc in docs
        ],
    }


@router.get("/sources/{source_id}")
async def get_source(
    source_id: str,
    db=Depends(get_async_session_local),
):
    """Get source detail including chunk count."""
    from models.source_document import SourceDocument
    from sqlalchemy import select

    try:
        uid = uuid.UUID(source_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid source ID")

    result = await db.execute(
        select(SourceDocument).where(SourceDocument.id == uid)
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Source not found")

    return {
        "id": str(doc.id),
        "title": doc.title,
        "authors": doc.authors,
        "year": doc.year,
        "source_type": doc.source_type,
        "origin_url": doc.origin_url,
        "file_path": doc.file_path,
        "chunk_count": doc.chunk_count,
        "status": doc.status,
        "metadata": doc.metadata_json,
        "ingested_at": doc.ingested_at.isoformat() if doc.ingested_at else None,
    }


@router.delete("/sources/{source_id}")
async def delete_source(
    source_id: str,
    db=Depends(get_async_session_local),
):
    """Delete a source document and all its chunks."""
    from models.source_document import SourceDocument
    from sqlalchemy import select, delete

    try:
        uid = uuid.UUID(source_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid source ID")

    result = await db.execute(
        select(SourceDocument).where(SourceDocument.id == uid)
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Source not found")

    # Delete file if it exists
    if doc.file_path and Path(doc.file_path).exists():
        Path(doc.file_path).unlink()

    await db.delete(doc)
    await db.commit()

    return {"status": "deleted", "id": source_id}


@router.post("/sources/{source_id}/assign")
async def assign_source_to_episode(
    source_id: str,
    episode_id: str = Query(..., description="Episode ID to assign to"),
    pipeline: IngestPipeline = Depends(get_ingest_pipeline),
):
    """Assign a source document to an episode."""
    try:
        await pipeline.assign_to_episode(source_id, episode_id)
        return {"status": "assigned", "source_id": source_id, "episode_id": episode_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sources/{source_id}/chunks")
async def get_source_chunks(
    source_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, le=100),
    db=Depends(get_async_session_local),
):
    """List chunks for a source document (paginated)."""
    from models.source_chunk import SourceChunk
    from sqlalchemy import select, func

    try:
        uid = uuid.UUID(source_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid source ID")

    # Count
    count_query = select(func.count()).where(SourceChunk.document_id == uid)
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Fetch
    query = (
        select(SourceChunk)
        .where(SourceChunk.document_id == uid)
        .order_by(SourceChunk.chunk_index)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(query)
    chunks = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "chunks": [
            {
                "id": str(c.id),
                "chunk_index": c.chunk_index,
                "text": c.text[:500],  # Truncate for listing
                "token_count": c.token_count,
                "created_at": c.created_at.isoformat() if c.created_at else None,
            }
            for c in chunks
        ],
    }


@router.post("/sources/search")
async def search_sources(
    request: SourceSearchRequest,
    db=Depends(get_async_session_local),
):
    """Semantic search across all ingested sources."""
    embedder = ChunkEmbedder()
    try:
        query_embedding = await embedder.embed_batch([request.query])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {e}")

    if not query_embedding:
        return {"results": []}

    from services.intelligence.source_retriever import SourceRetriever
    retriever = SourceRetriever(db_session=db, embedder=embedder)

    try:
        chunks = await retriever._vector_search(
            query_embedding[0],
            episode_id=request.episode_id or "",
            top_k=request.top_k,
        )
    except Exception as e:
        logger.exception("Vector search failed")
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")

    return {
        "query": request.query,
        "results": [
            {
                "chunk_id": c.get("id"),
                "text": c.get("text", "")[:500],
                "title": c.get("title"),
                "authors": c.get("authors"),
                "year": c.get("year"),
                "source_type": c.get("source_type"),
                "origin_url": c.get("origin_url"),
                "distance": c.get("distance"),
            }
            for c in chunks
        ],
    }


@router.get("/sources/ingest/{task_id}")
async def get_ingest_status(task_id: str):
    """Check ingestion task status (placeholder — real SSE via Redis)."""
    return {
        "task_id": task_id,
        "status": "unknown",
        "message": "Real-time status available via SSE at /api/v1/stream/ingest/{task_id}",
    }


# --- Episode-Source Association Endpoints ---

@router.post("/episodes/{episode_id}/sources")
async def add_source_to_episode(
    episode_id: str,
    source_id: str = Query(..., description="Source document ID"),
    pipeline: IngestPipeline = Depends(get_ingest_pipeline),
):
    """Add a source to an episode."""
    try:
        await pipeline.assign_to_episode(source_id, episode_id)
        return {"status": "added", "episode_id": episode_id, "source_id": source_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/episodes/{episode_id}/sources")
async def list_episode_sources(
    episode_id: str,
    db=Depends(get_async_session_local),
):
    """List sources assigned to an episode."""
    from models.episode_source import EpisodeSource
    from models.source_document import SourceDocument
    from sqlalchemy import select

    try:
        eid = uuid.UUID(episode_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid episode ID")

    query = (
        select(SourceDocument, EpisodeSource.relevance_score)
        .join(EpisodeSource, SourceDocument.id == EpisodeSource.document_id)
        .where(EpisodeSource.episode_id == eid)
    )
    result = await db.execute(query)
    rows = result.all()

    return {
        "episode_id": episode_id,
        "sources": [
            {
                "id": str(doc.id),
                "title": doc.title,
                "authors": doc.authors,
                "year": doc.year,
                "source_type": doc.source_type,
                "origin_url": doc.origin_url,
                "chunk_count": doc.chunk_count,
                "status": doc.status,
                "relevance_score": score,
            }
            for doc, score in rows
        ],
    }


@router.delete("/episodes/{episode_id}/sources/{source_id}")
async def remove_source_from_episode(
    episode_id: str,
    source_id: str,
    db=Depends(get_async_session_local),
):
    """Remove a source from an episode."""
    from models.episode_source import EpisodeSource
    from sqlalchemy import select, delete

    try:
        eid = uuid.UUID(episode_id)
        sid = uuid.UUID(source_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID")

    stmt = delete(EpisodeSource).where(
        EpisodeSource.episode_id == eid,
        EpisodeSource.document_id == sid,
    )
    result = await db.execute(stmt)
    await db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Association not found")

    return {"status": "removed", "episode_id": episode_id, "source_id": source_id}


# --- Memgraph Endpoints ---

@router.get("/memgraph/health")
async def memgraph_health(
    client: MemgraphClient = Depends(get_memgraph_client),
):
    """Check Memgraph connection health."""
    healthy = await client.health_check()
    return {
        "enabled": client.enabled,
        "connected": healthy,
    }


@router.get("/memgraph/concept/{concept_name}")
async def get_concept(
    concept_name: str,
    client: MemgraphClient = Depends(get_memgraph_client),
):
    """Retrieve a concept and its subgraph from Memgraph."""
    if not client.enabled:
        raise HTTPException(status_code=503, detail="Memgraph is not enabled")

    concept = await client.query_concept(concept_name)
    if not concept.get("found"):
        raise HTTPException(status_code=404, detail=f"Concept '{concept_name}' not found")

    subgraph = await client.get_concept_subgraph(concept_name)
    concept["subgraph"] = subgraph
    return concept


@router.post("/memgraph/search")
async def search_concepts(
    request: MemgraphSearchRequest,
    client: MemgraphClient = Depends(get_memgraph_client),
):
    """Search concepts in Memgraph by text."""
    if not client.enabled:
        raise HTTPException(status_code=503, detail="Memgraph is not enabled")

    concepts = await client.find_related_concepts(request.query, limit=request.limit)
    return {
        "query": request.query,
        "concepts": concepts,
    }


# ── Smart Paste Endpoint ─────────────────────────────────────────────────


class PasteRequest(BaseModel):
    text: str
    episode_id: Optional[str] = None


@router.post("/paste", summary="Smart paste — classify and route pasted content")
async def smart_paste(request: PasteRequest):
    """
    Accept pasted content (URL, DOI, arXiv ID, BibTeX, plain text),
    classify it, and return the appropriate action for the frontend to execute.
    """
    from services.ingestion.paste_classifier import PasteClassifier
    classifier = PasteClassifier()
    result = await classifier.route(request.text, request.episode_id)
    return result
