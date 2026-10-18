# -*- coding: utf-8 -*-
"""
GeoSI RAG — RAG Service
═══════════════════════════════════════════════════════════════════

End-to-end Retrieval-Augmented Generation pipeline:
    1. Retrieve relevant GIS docs via hybrid search
    2. Retrieve similar workflow examples
    3. Rerank combined results
    4. Assemble context prompt for the planning agent

This is the main service that KnowledgeManager delegates to
for document retrieval.
"""

import logging
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

from geosi_rag.document_loader import DocumentLoader
from geosi_rag.chunker import Chunker
from geosi_rag.embedding_service import EmbeddingService
from geosi_rag.qdrant_store import QdrantStore
from geosi_rag.retriever import Retriever, SearchResult
from geosi_rag.reranker import Reranker

logger = logging.getLogger("geosi_rag.rag_service")


@dataclass
class RAGResult:
    """
    Result from a RAG query.

    Attributes:
        documents: Retrieved GIS documentation snippets
        workflows: Retrieved workflow examples
        context_prompt: Assembled prompt section for the LLM
        sources: List of source file paths referenced
    """
    documents: List[SearchResult] = field(default_factory=list)
    workflows: List[SearchResult] = field(default_factory=list)
    context_prompt: str = ""
    sources: List[str] = field(default_factory=list)

    def __repr__(self):
        return (
            f"RAGResult(docs={len(self.documents)}, "
            f"workflows={len(self.workflows)}, "
            f"prompt_len={len(self.context_prompt)})"
        )


class RAGService:
    """
    End-to-end RAG pipeline for GIS knowledge retrieval.

    Usage:
        rag = RAGService()
        result = rag.query("Calculate NDVI from Sentinel imagery")
        print(result.context_prompt)  # → feed to planning agent
    """

    def __init__(
        self,
        embedding_service: Optional[EmbeddingService] = None,
        qdrant_store: Optional[QdrantStore] = None,
        reranker: Optional[Reranker] = None,
    ):
        """
        Initialize the RAG service.

        If components are not provided, creates them with defaults.
        """
        self.embeddings = embedding_service or EmbeddingService()
        self.store = qdrant_store or QdrantStore()
        self.retriever = Retriever(self.embeddings, self.store)
        self.reranker = reranker or Reranker()
        self.loader = DocumentLoader()
        self.chunker = Chunker()

        # Ensure default collections exist
        if self.embeddings.available and self.store.available:
            self.store.ensure_collections(self.embeddings.vector_size)

        self.available = self.embeddings.available and self.store.available

    def query(
        self,
        user_query: str,
        doc_limit: int = 5,
        workflow_limit: int = 3,
    ) -> RAGResult:
        """
        Full RAG query: retrieve docs + workflows, rerank, build prompt.

        Args:
            user_query: The user's natural language query.
            doc_limit: Max documentation results.
            workflow_limit: Max workflow results.

        Returns:
            RAGResult with documents, workflows, and assembled prompt.
        """
        if not self.available:
            logger.debug("RAG service unavailable — returning empty result")
            return RAGResult()

        # 1. Search GIS documentation
        doc_results = self.retriever.hybrid_search(
            query=user_query,
            collection="gis_docs",
            limit=doc_limit * 2,  # Fetch extra for reranking
        )

        # 2. Search workflow examples
        workflow_results = self.retriever.hybrid_search(
            query=user_query,
            collection="gis_workflows",
            limit=workflow_limit * 2,
        )

        # 3. Rerank
        doc_results = self.reranker.rerank(user_query, doc_results, top_k=doc_limit)
        workflow_results = self.reranker.rerank(user_query, workflow_results, top_k=workflow_limit)

        # 4. Collect unique sources
        sources = list(set(
            r.source for r in doc_results + workflow_results if r.source
        ))

        # 5. Build context prompt
        context_prompt = self._build_context_prompt(
            user_query, doc_results, workflow_results
        )

        result = RAGResult(
            documents=doc_results,
            workflows=workflow_results,
            context_prompt=context_prompt,
            sources=sources,
        )

        logger.info(
            f"RAG query: '{user_query[:50]}...' → "
            f"{len(doc_results)} docs, {len(workflow_results)} workflows"
        )
        return result

    def ingest_documents(
        self,
        directory: str,
        collection: str = "gis_docs",
        chunk_size: int = 512,
        overlap: int = 64,
    ) -> int:
        """
        Ingest documents from a directory into Qdrant.

        Pipeline: load → chunk → embed → store

        Args:
            directory: Path to directory containing documents.
            collection: Target Qdrant collection.
            chunk_size: Text chunk size in characters.
            overlap: Overlap between chunks.

        Returns:
            Number of chunks ingested.
        """
        if not self.available:
            logger.warning("RAG service unavailable — cannot ingest")
            return 0

        # 1. Load documents
        docs = self.loader.load_directory(directory)
        if not docs:
            logger.warning(f"No documents found in '{directory}'")
            return 0

        # 2. Chunk documents
        chunker = Chunker(chunk_size=chunk_size, overlap=overlap)
        chunks = chunker.chunk_documents(docs)
        if not chunks:
            logger.warning("No chunks generated from documents")
            return 0

        # 3. Ensure collection exists
        self.store.create_collection(
            collection, self.embeddings.vector_size
        )

        # 4. Generate embeddings
        logger.info(f"Generating embeddings for {len(chunks)} chunks...")
        texts = [c.text for c in chunks]
        embeddings = self.embeddings.embed_batch(texts, show_progress=True)

        # 5. Store in Qdrant
        count = self.store.upsert(chunks, embeddings, collection)

        logger.info(
            f"Ingested {count} chunks from '{directory}' → '{collection}'"
        )
        return count

    def ingest_workflow(
        self,
        workflow: Dict[str, Any],
        collection: str = "gis_workflows",
    ) -> bool:
        """
        Store a single workflow example in Qdrant.

        Args:
            workflow: Dict with keys: name, description, user_query,
                      tool_sequence, plan_json
            collection: Target collection.

        Returns:
            True if stored successfully.
        """
        if not self.available:
            return False

        from geosi_rag.chunker import Chunk

        # Build searchable text from workflow
        text_parts = [
            workflow.get("name", ""),
            workflow.get("description", ""),
            workflow.get("user_query", ""),
            " ".join(workflow.get("tool_sequence", [])),
        ]
        text = " | ".join(part for part in text_parts if part)

        chunk = Chunk(
            text=text,
            source=f"workflow:{workflow.get('name', 'unknown')}",
            chunk_index=0,
            metadata={
                "type": "workflow",
                "name": workflow.get("name", ""),
                "tool_sequence": workflow.get("tool_sequence", []),
                "description": workflow.get("description", ""),
            },
        )

        embedding = self.embeddings.embed_text(text)
        count = self.store.upsert([chunk], [embedding], collection)
        return count > 0

    def _build_context_prompt(
        self,
        query: str,
        docs: List[SearchResult],
        workflows: List[SearchResult],
    ) -> str:
        """
        Assemble a context prompt section from retrieved knowledge.

        This prompt section is injected into the LLM prompt before
        the planning instruction, giving the agent contextual GIS knowledge.
        """
        sections = []

        if docs:
            sections.append("## Relevant GIS Documentation\n")
            for i, doc in enumerate(docs, 1):
                source_label = doc.source.split("/")[-1] if doc.source else "unknown"
                sections.append(
                    f"### [{i}] {source_label} (relevance: {doc.score:.2f})\n"
                    f"{doc.text[:500]}\n"
                )

        if workflows:
            sections.append("## Similar Workflow Examples\n")
            for i, wf in enumerate(workflows, 1):
                name = wf.metadata.get("name", "unnamed")
                tools = wf.metadata.get("tool_sequence", [])
                sections.append(
                    f"### [{i}] Workflow: {name}\n"
                    f"Tools: {' → '.join(tools) if tools else 'N/A'}\n"
                    f"{wf.text[:300]}\n"
                )

        if not sections:
            return ""

        return (
            "─── GIS Knowledge Context ───\n"
            "The following information was retrieved from the GIS knowledge base "
            "and may help with planning the workflow.\n\n"
            + "\n".join(sections)
            + "\n─── End Knowledge Context ───\n"
        )

    def __repr__(self):
        status = "ready" if self.available else "unavailable"
        return f"RAGService({status}, embeddings={self.embeddings}, store={self.store})"
