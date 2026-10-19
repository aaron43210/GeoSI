"""
GeoSI v2 — GraphRAG Engine (Phase P10, FR-8.4)
════════════════════════════════════════════════════════════════════
Hybrid retrieval combining Qdrant vector search and Neo4j graph
traversal, merged with Reciprocal Rank Fusion (RRF).

Architecture:
  Qdrant (semantic)  +  Neo4j (structural)  →  RRF fusion  →  ranked results

Time complexity:
  - Qdrant top-k:       O(log N) with HNSW index
  - Neo4j graph hop:    O(d) per hop, d = node degree
  - RRF merge:          O(k log k) where k = total candidate results

Space complexity:
  - O(k) — only k candidates held in memory at any point

PRD references: §4.2 Research Agent, §4.1 Geology Agent, FR-8.4
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger("geosi_engine.graph_rag")

_RRF_K = 60  # RRF constant (standard recommendation)


@dataclass
class GraphRAGResult:
    """A single merged result from GraphRAG retrieval."""

    text: str
    source: str  # "qdrant" | "neo4j" | "merged"
    score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    node_type: Optional[str] = None  # Neo4j label if from graph


class GraphRAGEngine:
    """
    GraphRAG: Hybrid vector + graph retrieval with RRF fusion (P10).

    Used by the Research Agent and Geology Agent for cross-reference
    lookups that benefit from both semantic similarity (Qdrant) and
    structural relationships (Neo4j).

    Parameters
    ----------
    engine:
        Session-scoped GeoSI instance (for Qdrant access).
    neo4j_client:
        Neo4j client for graph traversal.
    """

    def __init__(self, engine: Any, neo4j_client: Optional[Any] = None) -> None:
        self._engine = engine
        self._neo4j = neo4j_client or self._get_neo4j()

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
        collection: str = "gis_docs",
        top_k: int = 10,
        graph_hops: int = 1,
        neo4j_start_id: Optional[str] = None,
    ) -> List[GraphRAGResult]:
        """
        Hybrid GraphRAG search.

        1. Qdrant semantic search → top-k candidates (O(log N))
        2. Neo4j graph traversal from related nodes (O(d^hops))
        3. RRF fusion of both ranked lists (O(k log k))

        Parameters
        ----------
        query:
            Natural language query string.
        collection:
            Qdrant collection to search.
        top_k:
            Number of final results to return.
        graph_hops:
            Depth of Neo4j traversal (keep ≤ 3 for production).
        neo4j_start_id:
            Optional dataset_id or plan_id to start graph traversal from.
        """
        # Step 1: Qdrant semantic search
        qdrant_results = self._qdrant_search(query, collection, top_k * 2)

        # Step 2: Neo4j graph traversal
        graph_results = self._graph_search(query, neo4j_start_id, graph_hops)

        # Step 3: RRF fusion
        fused = self._rrf_merge(qdrant_results, graph_results, top_k)

        logger.debug(
            "GraphRAG: query='%s' qdrant=%d graph=%d fused=%d",
            query[:60],
            len(qdrant_results),
            len(graph_results),
            len(fused),
        )
        return fused

    def cross_reference(
        self,
        dataset_id: str,
        rel_types: Optional[List[str]] = None,
        hops: int = 2,
    ) -> List[GraphRAGResult]:
        """
        Find datasets structurally related to a given dataset via Neo4j.

        Used by Geology Agent for stratigraphic cross-reference and
        Research Agent for citation graph traversal.

        Complexity: O(d^hops) — bounded by graph_hops.
        """
        if not self._neo4j or not self._neo4j.available:
            return []

        from geosi_data.graph_schema import RelType

        rel_filter = "|".join(rel_types or [RelType.RELATED_TO, RelType.DERIVED_FROM])

        cypher = f"""
        MATCH (a:Dataset {{dataset_id: $did}})-[:{rel_filter}*1..{hops}]-(b)
        RETURN DISTINCT b.name AS name, b.path AS path,
               labels(b) AS labels, b.dataset_id AS did
        LIMIT 20
        """
        records = self._neo4j.cypher_query(cypher, {"did": dataset_id})

        results: list[GraphRAGResult] = []
        for r in records:
            results.append(
                GraphRAGResult(
                    text=str(r.get("name", "")),
                    source="neo4j",
                    score=1.0,
                    metadata={"path": r.get("path", ""), "dataset_id": r.get("did", "")},
                    node_type=str(r.get("labels", ["Dataset"])[0]),
                )
            )
        return results

    # ------------------------------------------------------------------
    # Internal: retrieval steps
    # ------------------------------------------------------------------

    def _qdrant_search(self, query: str, collection: str, limit: int) -> List[GraphRAGResult]:
        """Vector search via Qdrant. O(log N) with HNSW index."""
        results: list[GraphRAGResult] = []
        try:
            if not self._engine or not self._engine.knowledge:
                return []
            if hasattr(self._engine.knowledge, "search_gis_docs"):
                try:
                    raw = self._engine.knowledge.search_gis_docs(query, collection=collection, limit=limit)
                except TypeError:
                    raw = self._engine.knowledge.search_gis_docs(query)
            else:
                ctx = self._engine.knowledge.retrieve_context(query, doc_limit=limit)
                raw = getattr(ctx, "relevant_docs", []) or []
            for r in raw:
                results.append(
                    GraphRAGResult(
                        text=getattr(r, "text", str(r)),
                        source="qdrant",
                        score=float(getattr(r, "score", 0.0)),
                        metadata=getattr(r, "metadata", {}),
                    )
                )
        except Exception as exc:
            logger.debug("Qdrant search failed: %s", exc)
        return results

    def _graph_search(self, query: str, start_id: Optional[str], hops: int) -> List[GraphRAGResult]:
        """Neo4j graph traversal for structurally related knowledge."""
        if not self._neo4j or not self._neo4j.available:
            return []
        results: list[GraphRAGResult] = []
        try:
            if start_id:
                # Traverse from known node
                nodes = self._neo4j.find_related("Dataset", "dataset_id", start_id, "RELATED_TO", depth=hops)
                for n in nodes:
                    results.append(
                        GraphRAGResult(
                            text=n.properties.get("name", str(n.node_id)),
                            source="neo4j",
                            score=0.8,
                            metadata=n.properties,
                            node_type=n.labels[0] if n.labels else "Unknown",
                        )
                    )
            else:
                # Full-text keyword search in Neo4j (graceful if FT index not set up)
                cypher = """
                MATCH (d:Dataset) WHERE toLower(d.name) CONTAINS toLower($q)
                RETURN d.name AS name, d.path AS path, d.dataset_id AS did
                LIMIT 10
                """
                records = self._neo4j.cypher_query(cypher, {"q": query[:50]})
                for r in records:
                    results.append(
                        GraphRAGResult(
                            text=str(r.get("name", "")),
                            source="neo4j",
                            score=0.7,
                            metadata={"path": r.get("path", ""), "dataset_id": r.get("did", "")},
                        )
                    )
        except Exception as exc:
            logger.debug("Neo4j graph search failed: %s", exc)
        return results

    # ------------------------------------------------------------------
    # RRF fusion
    # ------------------------------------------------------------------

    def _rrf_merge(
        self,
        list_a: List[GraphRAGResult],
        list_b: List[GraphRAGResult],
        top_k: int,
    ) -> List[GraphRAGResult]:
        """
        Reciprocal Rank Fusion of two ranked lists.

        RRF score: sum(1 / (k + rank_i)) across all lists.
        A document appearing in both lists gets boosted.

        Time complexity: O((|A| + |B|) log(|A| + |B|)) for sorting.
        Space complexity: O(|A| + |B|) for the score accumulator dict.
        """
        # Accumulate RRF scores keyed by text (deduplicate by content)
        rrf_scores: dict[str, float] = {}
        rrf_meta: dict[str, GraphRAGResult] = {}

        for rank, result in enumerate(list_a, start=1):
            key = result.text[:200]  # use truncated text as dedup key
            rrf_scores[key] = rrf_scores.get(key, 0.0) + 1.0 / (_RRF_K + rank)
            rrf_meta[key] = result

        for rank, result in enumerate(list_b, start=1):
            key = result.text[:200]
            rrf_scores[key] = rrf_scores.get(key, 0.0) + 1.0 / (_RRF_K + rank)
            if key not in rrf_meta:
                rrf_meta[key] = result

        # Sort by RRF score descending — O(k log k)
        sorted_keys = sorted(rrf_scores, key=rrf_scores.__getitem__, reverse=True)

        fused: list[GraphRAGResult] = []
        for key in sorted_keys[:top_k]:
            result = rrf_meta[key]
            result.score = rrf_scores[key]
            result.source = "merged"
            fused.append(result)
        return fused

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_neo4j(self):
        try:
            from geosi_data.neo4j_client import get_neo4j_client

            return get_neo4j_client()
        except Exception:
            return None
