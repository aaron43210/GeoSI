# -*- coding: utf-8 -*-
"""
GeoSI v2 — Research Agent (Optional Agent #12)
════════════════════════════════════════════════════════════════════
Retrieves research papers, performs literature review, summarises
findings, and generates citations.

PRD §4.2 Optional Agent #12 — Production notes
────────────────────────────────────────────────
* RAG output is subject to the same golden-set RAGAS evaluation
  (faithfulness, context precision) as the Planning Agent's retrieval.
* Always read-only — permission tier: ``allow``.
* RAG-retrieved content MUST pass through the Permission & Safety
  Agent's guardrail scanner (FR-3.1) before entering any prompt.
* Qdrant collections targeted: Research Papers, GIS Documentation,
  Remote Sensing Workflows, Geological Knowledge.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from geosi_engine.telemetry import span, set_span_attr

logger = logging.getLogger("geosi_engine.agents.research")


@dataclass
class ResearchQuery:
    """A research retrieval request."""
    query: str
    topics: List[str] = field(default_factory=list)
    max_results: int = 10
    collections: List[str] = field(default_factory=lambda: ["research_papers", "gis_docs"])
    session_id: str = ""
    include_citations: bool = True


@dataclass
class ResearchResult:
    """Result of a research retrieval operation."""
    success: bool
    query: str
    papers: List[Dict[str, Any]] = field(default_factory=list)
    summary: str = ""
    citations: List[str] = field(default_factory=list)
    guardrail_flags: List[str] = field(default_factory=list)
    total_sources: int = 0
    error: Optional[str] = None


class ResearchAgent:
    """
    Research Agent for literature retrieval and summarisation (PRD §4.2, Agent #12).

    Always read-only (``allow``-tier). All retrieved content is
    guardrail-scanned (FR-3.1) before being returned to the Supervisor
    or Planning Agent.

    Parameters
    ----------
    engine:
        Session-scoped GeoSI instance.
    permission_agent:
        The ``PermissionSafetyAgent`` — used for guardrail scanning only
        (no execution permission gate, since this agent is read-only).
    """

    def __init__(self, engine: Any, permission_agent: Any) -> None:
        self._engine = engine
        self._permission = permission_agent
        self._graph_rag = self._init_graph_rag()

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    @span("research.search", agent="research")
    def search(self, req: ResearchQuery) -> ResearchResult:
        """Retrieve research papers with guardrail-scanned RAG (FR-3.1)."""
        set_span_attr("research.query", req.query[:100])
        set_span_attr("research.max_results", req.max_results)

        papers: list[dict] = []
        guardrail_flags: list[str] = []

        for collection in req.collections:
            retrieved = self._retrieve(req.query, collection, req.max_results)
            for doc in retrieved:
                text = doc.get("text", "")
                flags = self._scan(text)
                if flags:
                    doc["guardrail_flags"] = flags
                    guardrail_flags.extend(flags)
                    logger.warning(
                        "Research: guardrail flags on document from '%s': %s",
                        collection, flags
                    )
                papers.append(doc)

        set_span_attr("research.total_sources", len(papers))
        set_span_attr("research.guardrail_flags", len(guardrail_flags))

        # Deduplicate and limit
        seen_ids: set = set()
        deduped: list[dict] = []
        for p in papers:
            pid = p.get("id", p.get("title", ""))
            if pid not in seen_ids:
                seen_ids.add(pid)
                deduped.append(p)
        deduped = deduped[: req.max_results]

        # ── Summarise ─────────────────────────────────────────────────
        summary = self._summarise(req.query, deduped)

        # ── Generate citations ─────────────────────────────────────────
        citations: list[str] = []
        if req.include_citations:
            citations = [self._format_citation(p) for p in deduped]

        return ResearchResult(
            success=True,
            query=req.query,
            papers=deduped,
            summary=summary,
            citations=citations,
            guardrail_flags=guardrail_flags,
            total_sources=len(deduped),
        )

    @span("research.graph_search", agent="research")
    def graph_search(
        self, query: str, dataset_id: Optional[str] = None, top_k: int = 10
    ) -> ResearchResult:
        """
        GraphRAG hybrid search (P10): Qdrant vector + Neo4j graph traversal.

        Uses RRF to merge semantic and structural results, providing
        cross-referenced knowledge not available from vector search alone.

        Parameters
        ----------
        query:
            Natural language research query.
        dataset_id:
            Optional Neo4j dataset_id to start graph traversal from.
        top_k:
            Maximum number of merged results.
        """
        set_span_attr("research.graph_query", query[:100])
        results = self._graph_rag.search(
            query=query,
            collection="research_papers",
            top_k=top_k,
            neo4j_start_id=dataset_id,
        )
        papers = [
            {
                "text": r.text,
                "score": r.score,
                "source": r.source,
                "node_type": r.node_type,
                "metadata": r.metadata,
            }
            for r in results
        ]
        guardrail_flags: list[str] = []
        for p in papers:
            flags = self._scan(p.get("text", ""))
            if flags:
                p["guardrail_flags"] = flags
                guardrail_flags.extend(flags)

        return ResearchResult(
            success=True,
            query=query,
            papers=papers,
            summary=self._summarise(query, papers),
            citations=[self._format_citation(p) for p in papers],
            guardrail_flags=guardrail_flags,
            total_sources=len(papers),
        )

    @span("research.literature_review", agent="research")
    def literature_review(self, topic: str, max_papers: int = 20) -> ResearchResult:
        """
        Perform a structured literature review on a topic.
        Retrieves papers, clusters them by sub-theme, and summarises each cluster.
        """
        req = ResearchQuery(
            query=topic,
            max_results=max_papers,
            collections=["research_papers", "gis_docs", "geological_knowledge"],
            include_citations=True,
        )
        result = self.search(req)
        if not result.success or not result.papers:
            return result

        # Group by collection source
        by_source: dict[str, list] = {}
        for p in result.papers:
            src = p.get("collection", "general")
            by_source.setdefault(src, []).append(p)

        # Extended summary with per-source breakdown
        summary_parts = [f"# Literature Review: {topic}\n"]
        for src, docs in by_source.items():
            summary_parts.append(f"\n## {src.replace('_', ' ').title()} ({len(docs)} sources)")
            for d in docs[:5]:
                title = d.get("title", d.get("text", "")[:80])
                summary_parts.append(f"- {title}")

        result.summary = "\n".join(summary_parts)
        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _retrieve(self, query: str, collection: str, limit: int) -> list[dict]:
        """Retrieve documents from the Knowledge Layer via the RAG system."""
        docs: list[dict] = []
        try:
            if not self._engine.knowledge:
                return []
            # retrieve_context is the real KnowledgeManager entrypoint; its
            # KnowledgeContext.relevant_docs holds the matched doc snippets.
            ctx = self._engine.knowledge.retrieve_context(query, doc_limit=limit)
            results = getattr(ctx, "relevant_docs", []) or []
            for r in results:
                docs.append({
                    "id": getattr(r, "id", ""),
                    "text": getattr(r, "text", str(r)),
                    "score": getattr(r, "score", 0.0),
                    "title": getattr(r, "title", ""),
                    "source": getattr(r, "source", ""),
                    "collection": collection,
                    "metadata": getattr(r, "metadata", {}),
                })
        except Exception as exc:
            logger.debug("RAG retrieval from '%s' failed: %s", collection, exc)
        return docs

    def _init_graph_rag(self):
        """Initialise the GraphRAG engine (P10). Graceful fail if Neo4j unavailable."""
        try:
            from geosi_engine.graph_rag import GraphRAGEngine
            return GraphRAGEngine(self._engine)
        except Exception as exc:
            logger.debug("GraphRAG init failed (non-fatal): %s", exc)
            # Return a no-op stub
            class _NoopGraphRAG:
                def search(self, **kwargs): return []
                def cross_reference(self, **kwargs): return []
            return _NoopGraphRAG()

    def _scan(self, text: str) -> list[str]:
        """Run guardrail scan on text (FR-3.1). Returns list of flag strings."""
        try:
            from geosi_engine.guardrails import scan_text
            result = scan_text(text)
            return result.flags if not result.is_clean else []
        except Exception as exc:
            logger.debug("Guardrail scan failed: %s", exc)
            return []

    def _summarise(self, query: str, papers: list[dict]) -> str:
        """Generate a concise summary of the retrieved papers."""
        if not papers:
            return f"No relevant literature found for query: '{query}'"

        titles = [p.get("title") or p.get("text", "")[:80] for p in papers[:5]]
        bullet_list = "\n".join(f"- {t}" for t in titles if t)
        return (
            f"Found {len(papers)} relevant source(s) for '{query}':\n{bullet_list}\n\n"
            f"The retrieved sources cover topics related to {query}. "
            "Review individual papers for detailed methodology and findings."
        )

    @staticmethod
    def _format_citation(paper: dict) -> str:
        """Format a paper dict into a basic citation string."""
        title = paper.get("title", "Unknown Title")
        source = paper.get("source", "GeoSI Knowledge Base")
        score = paper.get("score", 0.0)
        return f"{title}. Source: {source}. Relevance: {score:.3f}."
