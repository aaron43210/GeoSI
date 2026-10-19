"""
GeoSI RAG — Retrieval-Augmented Generation Pipeline
═══════════════════════════════════════════════════════════════════

Vector search and document processing for GIS knowledge retrieval:
    - DocumentLoader: Multi-format document ingestion
    - Chunker: Sentence-aware text splitting
    - EmbeddingService: Local BGE embeddings via sentence-transformers
    - QdrantStore: Vector storage and search
    - Retriever: Semantic + keyword hybrid search
    - Reranker: Cross-encoder result re-scoring
    - RAGService: End-to-end RAG pipeline
"""

from geosi_rag.chunker import Chunk, Chunker
from geosi_rag.document_loader import Document, DocumentLoader
from geosi_rag.embedding_service import EmbeddingService
from geosi_rag.qdrant_store import QdrantStore
from geosi_rag.rag_service import RAGService
from geosi_rag.reranker import Reranker
from geosi_rag.retriever import Retriever, SearchResult

__all__ = [
    "DocumentLoader",
    "Document",
    "Chunker",
    "Chunk",
    "EmbeddingService",
    "QdrantStore",
    "Retriever",
    "SearchResult",
    "Reranker",
    "RAGService",
]
