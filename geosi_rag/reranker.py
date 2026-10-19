"""
GeoSI RAG — Reranker
═══════════════════════════════════════════════════════════════════

Re-scores retrieved results for relevance using a cross-encoder model.

Uses cross-encoder/ms-marco-MiniLM-L-6-v2 when available.
Falls back to score-based truncation if no cross-encoder installed.
"""

import logging
from typing import List, Optional

from geosi_rag.retriever import SearchResult

logger = logging.getLogger("geosi_rag.reranker")


class Reranker:
    """
    Re-scores search results for improved relevance.

    Usage:
        reranker = Reranker()
        reranked = reranker.rerank("Calculate NDVI", results, top_k=5)
    """

    def __init__(self, model_name: Optional[str] = None):
        """
        Args:
            model_name: Cross-encoder model ID.
                        Default: cross-encoder/ms-marco-MiniLM-L-6-v2
        """
        self.model_name = model_name or "cross-encoder/ms-marco-MiniLM-L-6-v2"
        self._model = None
        self.available = False

        self._init_model()

    def _init_model(self):
        """Load the cross-encoder model."""
        try:
            from sentence_transformers import CrossEncoder

            self._model = CrossEncoder(self.model_name)
            self.available = True
            logger.info(f"Reranker loaded: {self.model_name}")

        except ImportError:
            logger.debug(
                "CrossEncoder not available — reranker will use score fallback. "
                "Install with: pip install sentence-transformers"
            )
            self.available = False

        except Exception as e:
            logger.debug(f"Failed to load reranker model: {e}")
            self.available = False

    def rerank(
        self,
        query: str,
        results: List[SearchResult],
        top_k: int = 5,
    ) -> List[SearchResult]:
        """
        Re-rank search results by relevance to the query.

        Uses cross-encoder scoring if available, otherwise falls
        back to the original similarity scores.

        Args:
            query: The user's search query.
            results: Search results to re-rank.
            top_k: Number of top results to return.

        Returns:
            Re-ranked list of SearchResult objects.
        """
        if not results:
            return []

        if len(results) <= top_k and not self.available:
            return results

        if self.available and self._model is not None:
            return self._rerank_with_model(query, results, top_k)
        else:
            return self._rerank_by_score(results, top_k)

    def _rerank_with_model(
        self,
        query: str,
        results: List[SearchResult],
        top_k: int,
    ) -> List[SearchResult]:
        """Re-rank using cross-encoder model."""
        try:
            # Create query-document pairs
            pairs = [(query, r.text) for r in results]

            # Score all pairs
            scores = self._model.predict(pairs)

            # Update results with cross-encoder scores
            for result, score in zip(results, scores):
                result.score = float(score)

            # Sort by cross-encoder score (descending)
            results.sort(key=lambda r: r.score, reverse=True)

            logger.debug(
                f"Reranked {len(results)} results → top {top_k} "
                f"(scores: {results[0].score:.3f} to {results[min(top_k, len(results))-1].score:.3f})"
            )
            return results[:top_k]

        except Exception as e:
            logger.warning(f"Cross-encoder reranking failed: {e}")
            return self._rerank_by_score(results, top_k)

    @staticmethod
    def _rerank_by_score(
        results: List[SearchResult],
        top_k: int,
    ) -> List[SearchResult]:
        """Fallback: just sort by existing score and truncate."""
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]

    def __repr__(self):
        status = "ready" if self.available else "score-fallback"
        return f"Reranker(model={self.model_name}, {status})"
