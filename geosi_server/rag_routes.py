# -*- coding: utf-8 -*-
"""
GeoSI Server — RAG Routes
═══════════════════════════════════════════════════════════════════

Endpoints:
    POST /rag/search  — Semantic search across GIS documentation
    POST /rag/query   — Full RAG query (retrieve + rerank + context)
    POST /rag/ingest  — Ingest documents from a directory
"""

import logging
from typing import Optional, List

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from geosi_server.auth import api_key_auth

logger = logging.getLogger("geosi_server.rag")
router = APIRouter()


# ── Request/Response models ────────────────────────────────────────────

class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query text")
    collection: str = Field("gis_docs", description="Qdrant collection to search")
    limit: int = Field(10, ge=1, le=50, description="Max results")


class SearchResultItem(BaseModel):
    text: str
    score: float
    source: str
    metadata: dict = {}


class SearchResponse(BaseModel):
    query: str
    results: List[SearchResultItem]
    total: int


class RAGQueryRequest(BaseModel):
    query: str = Field(..., description="Natural language GIS query")
    doc_limit: int = Field(5, ge=1, le=20)
    workflow_limit: int = Field(3, ge=1, le=10)


class RAGQueryResponse(BaseModel):
    query: str
    documents: List[SearchResultItem]
    workflows: List[SearchResultItem]
    context_prompt: str
    sources: List[str]


class IngestRequest(BaseModel):
    directory: str = Field(..., description="Path to documents directory")
    collection: str = Field("gis_docs", description="Target collection")
    chunk_size: int = Field(512, ge=64, le=4096)
    overlap: int = Field(64, ge=0, le=512)


class IngestResponse(BaseModel):
    directory: str
    collection: str
    chunks_ingested: int


# ── Endpoints ──────────────────────────────────────────────────────────

@router.post("/search", response_model=SearchResponse)
async def rag_search(req: SearchRequest, api_key: str = Depends(api_key_auth)):
    """
    Semantic search across GIS documentation.

    Searches the specified Qdrant collection using hybrid
    (semantic + keyword) search with RRF fusion.
    """
    from geosi_server.app import get_pool
    engine = get_pool().get_or_create(api_key)

    # Force lazy RAG init so a cold session doesn't falsely report 503.
    if engine.knowledge:
        engine.knowledge.ensure_rag()
    if not engine.knowledge or not engine.knowledge.rag:
        raise HTTPException(
            status_code=503,
            detail="RAG service unavailable. Enable knowledge layer."
        )

    rag = engine.knowledge.rag
    results = rag.retriever.hybrid_search(
        query=req.query,
        collection=req.collection,
        limit=req.limit,
    )

    items = [
        SearchResultItem(
            text=r.text,
            score=r.score,
            source=r.source,
            metadata=r.metadata,
        )
        for r in results
    ]

    return SearchResponse(query=req.query, results=items, total=len(items))


@router.post("/query", response_model=RAGQueryResponse)
async def rag_query(req: RAGQueryRequest, api_key: str = Depends(api_key_auth)):
    """
    Full RAG query — retrieves docs + workflows, reranks, builds context.

    Returns both the raw results and the assembled context prompt
    that would be injected into the planning agent's LLM call.
    """
    from geosi_server.app import get_pool
    engine = get_pool().get_or_create(api_key)

    # Force lazy RAG init so a cold session doesn't falsely report 503.
    if engine.knowledge:
        engine.knowledge.ensure_rag()
    if not engine.knowledge or not engine.knowledge.rag:
        raise HTTPException(
            status_code=503,
            detail="RAG service unavailable. Enable knowledge layer."
        )

    rag = engine.knowledge.rag
    result = rag.query(
        user_query=req.query,
        doc_limit=req.doc_limit,
        workflow_limit=req.workflow_limit,
    )

    docs = [
        SearchResultItem(
            text=r.text, score=r.score, source=r.source, metadata=r.metadata
        )
        for r in result.documents
    ]
    workflows = [
        SearchResultItem(
            text=r.text, score=r.score, source=r.source, metadata=r.metadata
        )
        for r in result.workflows
    ]

    return RAGQueryResponse(
        query=req.query,
        documents=docs,
        workflows=workflows,
        context_prompt=result.context_prompt,
        sources=result.sources,
    )


@router.post("/ingest", response_model=IngestResponse)
async def rag_ingest(req: IngestRequest, api_key: str = Depends(api_key_auth)):
    """
    Ingest documents from a local directory into Qdrant.

    Pipeline: load files → chunk → embed → store in Qdrant.
    """
    from geosi_server.app import get_pool
    engine = get_pool().get_or_create(api_key)

    count = engine.ingest_documents(req.directory, req.collection)

    return IngestResponse(
        directory=req.directory,
        collection=req.collection,
        chunks_ingested=count,
    )
