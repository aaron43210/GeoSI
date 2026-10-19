"""
GeoSI RAG — Embedding Service
═══════════════════════════════════════════════════════════════════

Generates vector embeddings using local sentence-transformers.
Default model: BAAI/bge-large-en-v1.5 (1024-dim, ~1.3GB)

No OpenAI — fully local embedding pipeline.
"""

import logging
import os
from typing import List, Optional

logger = logging.getLogger("geosi_rag.embedding_service")

# Default embedding model
_DEFAULT_MODEL = "BAAI/bge-large-en-v1.5"


class EmbeddingService:
    """
    Local embedding service using sentence-transformers.

    Usage:
        svc = EmbeddingService()
        vector = svc.embed_text("Calculate NDVI from Sentinel imagery")
        vectors = svc.embed_batch(["NDVI", "slope analysis", "buffer"])
    """

    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize the embedding service.

        Args:
            model_name: HuggingFace model ID. Defaults to BAAI/bge-large-en-v1.5.
                        Override via EMBEDDING_MODEL env var.
        """
        self.model_name = model_name or os.environ.get("EMBEDDING_MODEL", _DEFAULT_MODEL)
        self._model = None
        self._vector_size = None
        self.available = False

        self._init_model()

    def _init_model(self):
        """Load the sentence-transformer model."""
        try:
            from sentence_transformers import SentenceTransformer

            logger.info(f"Loading embedding model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)

            # Determine vector dimensionality
            test_embedding = self._model.encode(["test"], show_progress_bar=False)
            self._vector_size = len(test_embedding[0])
            self.available = True

            logger.info(f"Embedding model loaded: {self.model_name} " f"(dim={self._vector_size})")

        except ImportError:
            logger.warning("sentence-transformers not installed. " "Install with: pip install sentence-transformers")
            self.available = False

        except Exception as e:
            logger.warning(f"Failed to load embedding model: {e}")
            self.available = False

    @property
    def vector_size(self) -> int:
        """Return the dimensionality of embeddings."""
        if self._vector_size is None:
            raise RuntimeError("Embedding model not loaded")
        return self._vector_size

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        For BGE models, prepends "Represent this sentence: " instruction
        for better retrieval quality.

        Args:
            text: Input text to embed.

        Returns:
            List of floats (embedding vector).

        Raises:
            RuntimeError: If embedding model is not available.
        """
        if not self.available or self._model is None:
            raise RuntimeError("Embedding service not available. " "Install sentence-transformers and try again.")

        # BGE models work better with an instruction prefix for queries
        if "bge" in self.model_name.lower():
            text = f"Represent this sentence: {text}"

        embedding = self._model.encode(
            [text],
            show_progress_bar=False,
            normalize_embeddings=True,
        )
        return embedding[0].tolist()

    def embed_batch(
        self,
        texts: List[str],
        batch_size: int = 32,
        show_progress: bool = False,
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of input texts.
            batch_size: Processing batch size.
            show_progress: Show progress bar.

        Returns:
            List of embedding vectors.

        Raises:
            RuntimeError: If embedding model is not available.
        """
        if not self.available or self._model is None:
            raise RuntimeError("Embedding service not available")

        if not texts:
            return []

        # BGE instruction prefix for document embeddings
        processed = texts
        if "bge" in self.model_name.lower():
            processed = [f"Represent this sentence: {t}" for t in texts]

        embeddings = self._model.encode(
            processed,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            normalize_embeddings=True,
        )
        return [e.tolist() for e in embeddings]

    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a search query.

        For BGE models, uses the query-specific instruction prefix
        for better retrieval performance.

        Args:
            query: Search query text.

        Returns:
            Query embedding vector.
        """
        if not self.available or self._model is None:
            raise RuntimeError("Embedding service not available")

        # BGE uses a different prefix for queries vs documents
        if "bge" in self.model_name.lower():
            query = f"Represent this sentence for searching relevant passages: {query}"

        embedding = self._model.encode(
            [query],
            show_progress_bar=False,
            normalize_embeddings=True,
        )
        return embedding[0].tolist()

    def __repr__(self):
        status = "ready" if self.available else "unavailable"
        dim = self._vector_size or "?"
        return f"EmbeddingService(model={self.model_name}, dim={dim}, {status})"
