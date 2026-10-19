"""
GeoSI RAG — Retriever
═══════════════════════════════════════════════════════════════════

Orchestrates search across Qdrant collections with support for:
    - Semantic search (vector similarity)
    - Keyword search (payload text matching)
    - Hybrid search (Reciprocal Rank Fusion of semantic + keyword)
"""

import logging
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger("geosi_rag.retriever")


@dataclass
class SearchResult:
    """
    A single search result from the retriever.

    Attributes:
        text: Retrieved text content
        score: Relevance score (0.0 to 1.0)
        source: Source file path
        metadata: Additional metadata
    """

    text: str
    score: float = 0.0
    source: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self):
        preview = self.text[:60].replace("\n", " ")
        return f"SearchResult(score={self.score:.3f}, '{preview}...')"


class Retriever:
    """
    Orchestrates search across Qdrant collections.

    Supports semantic, keyword, and hybrid (RRF) search strategies.

    Usage:
        retriever = Retriever(embedding_service, qdrant_store)
        results = retriever.hybrid_search("Calculate NDVI", "gis_docs")
    """

    def __init__(self, embedding_service, qdrant_store):
        """
        Args:
            embedding_service: EmbeddingService for query vectorization.
            qdrant_store: QdrantStore for vector search.
        """
        self.embeddings = embedding_service
        self.store = qdrant_store

    def semantic_search(
        self,
        query: str,
        collection: str,
        limit: int = 10,
        score_threshold: Optional[float] = None,
        filters: Optional[Dict] = None,
    ) -> List[SearchResult]:
        """
        Search using vector similarity.

        Pipeline: query → embed → Qdrant vector search → results

        Args:
            query: Natural language search query.
            collection: Qdrant collection to search.
            limit: Maximum results.
            score_threshold: Minimum similarity score.
            filters: Qdrant filter conditions.

        Returns:
            Ranked list of SearchResult objects.
        """
        if not self.embeddings.available or not self.store.available:
            logger.warning("Semantic search unavailable — missing embeddings or store")
            return []

        try:
            # Generate query embedding
            query_vector = self.embeddings.embed_query(query)

            # Search Qdrant
            raw_results = self.store.search(
                query_vector=query_vector,
                collection=collection,
                limit=limit,
                score_threshold=score_threshold,
                filters=filters,
            )

            return [
                SearchResult(
                    text=r["text"],
                    score=r["score"],
                    source=r["source"],
                    metadata=r.get("metadata", {}),
                )
                for r in raw_results
            ]

        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return []

    def keyword_search(
        self,
        query: str,
        collection: str,
        limit: int = 10,
    ) -> List[SearchResult]:
        """
        Search using keyword matching on stored text payloads.

        Uses Qdrant scroll + client-side keyword scoring.

        Args:
            query: Search query (keywords extracted automatically).
            collection: Qdrant collection to search.
            limit: Maximum results.

        Returns:
            Ranked list of SearchResult objects.
        """
        if not self.store.available:
            return []

        try:
            # Extract keywords from query
            keywords = self._extract_keywords(query)
            if not keywords:
                return []

            # Scroll through collection and score by keyword match
            # (Qdrant doesn't have native full-text search, so we do
            # client-side scoring on the text payload)
            all_points = []
            offset = None

            while True:
                result = self.store._client.scroll(
                    collection_name=collection,
                    limit=100,
                    offset=offset,
                    with_payload=True,
                    with_vectors=False,
                )
                points, next_offset = result
                all_points.extend(points)
                if next_offset is None or len(all_points) >= 1000:
                    break
                offset = next_offset

            # Score each point by keyword overlap
            scored = []
            for point in all_points:
                text = point.payload.get("text", "").lower()
                # Count keyword matches
                matches = sum(1 for kw in keywords if kw in text)
                if matches > 0:
                    score = matches / len(keywords)
                    scored.append(
                        SearchResult(
                            text=point.payload.get("text", ""),
                            score=score,
                            source=point.payload.get("source", ""),
                            metadata={k: v for k, v in point.payload.items() if k not in ("text", "source")},
                        )
                    )

            # Sort by score descending, take top results
            scored.sort(key=lambda r: r.score, reverse=True)
            return scored[:limit]

        except Exception as e:
            logger.error(f"Keyword search failed: {e}")
            return []

    def hybrid_search(
        self,
        query: str,
        collection: str,
        limit: int = 10,
        alpha: float = 0.7,
        score_threshold: Optional[float] = None,
    ) -> List[SearchResult]:
        """
        Hybrid search combining semantic and keyword results via RRF.

        Algorithm: Reciprocal Rank Fusion
            RRF_score(d) = Σ 1 / (k + rank_i(d))
            where k=60 (standard constant), i ∈ {semantic, keyword}

        Args:
            query: Search query.
            collection: Qdrant collection.
            limit: Maximum results.
            alpha: Weight for semantic vs keyword (0.0=keyword, 1.0=semantic).
            score_threshold: Minimum similarity for semantic search.

        Returns:
            Fused, ranked list of SearchResult objects.
        """
        # Get results from both strategies
        semantic_limit = int(limit * 2)  # Fetch more for better fusion
        keyword_limit = int(limit * 2)

        semantic_results = self.semantic_search(
            query,
            collection,
            limit=semantic_limit,
            score_threshold=score_threshold,
        )
        keyword_results = self.keyword_search(
            query,
            collection,
            limit=keyword_limit,
        )

        # If only one strategy returned results, use that
        if not semantic_results and not keyword_results:
            return []
        if not keyword_results:
            return semantic_results[:limit]
        if not semantic_results:
            return keyword_results[:limit]

        # Reciprocal Rank Fusion
        k = 60  # Standard RRF constant
        rrf_scores: Dict[str, float] = {}
        result_map: Dict[str, SearchResult] = {}

        # Score semantic results
        for rank, result in enumerate(semantic_results):
            key = self._result_key(result)
            rrf_scores[key] = rrf_scores.get(key, 0) + alpha / (k + rank + 1)
            result_map[key] = result

        # Score keyword results
        for rank, result in enumerate(keyword_results):
            key = self._result_key(result)
            rrf_scores[key] = rrf_scores.get(key, 0) + (1 - alpha) / (k + rank + 1)
            if key not in result_map:
                result_map[key] = result

        # Sort by fused score
        ranked_keys = sorted(rrf_scores.keys(), key=lambda k: rrf_scores[k], reverse=True)

        fused = []
        for key in ranked_keys[:limit]:
            result = result_map[key]
            result.score = rrf_scores[key]
            fused.append(result)

        logger.debug(
            f"Hybrid search: {len(semantic_results)} semantic + " f"{len(keyword_results)} keyword → {len(fused)} fused"
        )
        return fused

    @staticmethod
    def _extract_keywords(query: str) -> List[str]:
        """
        Extract meaningful keywords from a query.

        Removes common stop words and short tokens.
        """
        stop_words = {
            "a",
            "an",
            "the",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "can",
            "shall",
            "to",
            "of",
            "in",
            "for",
            "on",
            "with",
            "at",
            "by",
            "from",
            "as",
            "into",
            "through",
            "during",
            "before",
            "after",
            "above",
            "below",
            "between",
            "and",
            "but",
            "or",
            "not",
            "no",
            "nor",
            "so",
            "yet",
            "both",
            "either",
            "neither",
            "each",
            "every",
            "all",
            "any",
            "few",
            "more",
            "most",
            "other",
            "some",
            "such",
            "than",
            "too",
            "very",
            "just",
            "about",
            "how",
            "what",
            "which",
            "who",
            "whom",
            "this",
            "that",
            "these",
            "those",
            "i",
            "me",
            "my",
            "we",
            "our",
            "you",
            "your",
            "it",
            "its",
            "they",
            "them",
            "their",
            "he",
            "she",
            "him",
            "her",
            "his",
        }

        # Tokenize and filter
        tokens = re.findall(r"\b[a-zA-Z0-9_]+\b", query.lower())
        keywords = [t for t in tokens if t not in stop_words and len(t) > 2]
        return keywords

    @staticmethod
    def _result_key(result: SearchResult) -> str:
        """Generate a dedup key for a search result."""
        # Use first 100 chars of text + source as key
        return f"{result.source}:{result.text[:100]}"
