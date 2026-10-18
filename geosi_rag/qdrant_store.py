# -*- coding: utf-8 -*-
"""
GeoSI RAG — Qdrant Vector Store
═══════════════════════════════════════════════════════════════════

Manages Qdrant collections for vector storage and search.
Supports both local (in-memory / on-disk) and remote Qdrant instances.

Default collections:
    - gis_docs: GIS documentation embeddings
    - gis_workflows: Workflow example embeddings
    - geosi_history: Past execution embeddings
"""

import os
import uuid
import logging
from typing import List, Dict, Any, Optional

from geosi_rag.chunker import Chunk

logger = logging.getLogger("geosi_rag.qdrant_store")

# Default Qdrant connection settings
_DEFAULT_QDRANT_URL = "http://localhost:6333"
_DEFAULT_COLLECTIONS = ["gis_docs", "gis_workflows", "geosi_history"]


class QdrantStore:
    """
    Manages Qdrant vector collections.

    Usage:
        store = QdrantStore()
        store.create_collection("gis_docs", vector_size=1024)
        store.upsert(chunks, embeddings, "gis_docs")
        results = store.search(query_vector, "gis_docs", limit=10)
    """

    def __init__(
        self,
        url: Optional[str] = None,
        api_key: Optional[str] = None,
        path: Optional[str] = None,
    ):
        """
        Initialize Qdrant connection.

        Connection priority:
            1. path (local on-disk storage)
            2. url + api_key (remote Qdrant)
            3. In-memory (default for development)

        Args:
            url: Qdrant server URL (default: http://localhost:6333)
            api_key: Qdrant API key (for cloud instances)
            path: Local on-disk storage path (overrides url)
        """
        self.url = url or os.environ.get("QDRANT_URL", "")
        self.api_key = api_key or os.environ.get("QDRANT_API_KEY", "")
        self.path = path or os.environ.get("QDRANT_PATH", "")
        self._client = None
        self.available = False

        self._init_client()

    def _init_client(self):
        """Initialize the Qdrant client."""
        try:
            from qdrant_client import QdrantClient

            if self.path:
                # Local on-disk storage
                self._client = QdrantClient(path=self.path)
                logger.info(f"Qdrant connected: local storage at {self.path}")
            elif self.url:
                # Remote Qdrant server
                self._client = QdrantClient(
                    url=self.url,
                    api_key=self.api_key or None,
                    timeout=30,
                )
                logger.info(f"Qdrant connected: {self.url}")
            else:
                # In-memory (development mode)
                self._client = QdrantClient(":memory:")
                logger.info("Qdrant connected: in-memory mode")

            self.available = True

        except ImportError:
            logger.warning(
                "qdrant-client not installed. "
                "Install with: pip install qdrant-client"
            )
            self.available = False

        except Exception as e:
            logger.warning(f"Failed to connect to Qdrant: {e}")
            self.available = False

    def create_collection(
        self,
        name: str,
        vector_size: int,
        distance: str = "Cosine",
        recreate: bool = False,
    ) -> bool:
        """
        Create a Qdrant collection.

        Args:
            name: Collection name.
            vector_size: Embedding vector dimensionality.
            distance: Distance metric (Cosine, Euclid, Dot).
            recreate: If True, delete and recreate if exists.

        Returns:
            True if collection created/exists.
        """
        if not self.available or not self._client:
            return False

        from qdrant_client.models import Distance, VectorParams

        distance_map = {
            "Cosine": Distance.COSINE,
            "Euclid": Distance.EUCLID,
            "Dot": Distance.DOT,
        }

        try:
            # Check if collection already exists
            collections = self._client.get_collections().collections
            exists = any(c.name == name for c in collections)

            if exists and not recreate:
                logger.debug(f"Collection '{name}' already exists")
                return True

            if exists and recreate:
                self._client.delete_collection(name)
                logger.info(f"Deleted existing collection '{name}'")

            self._client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=distance_map.get(distance, Distance.COSINE),
                ),
            )
            logger.info(
                f"Created collection '{name}' (dim={vector_size}, {distance})"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to create collection '{name}': {e}")
            return False

    def upsert(
        self,
        chunks: List[Chunk],
        embeddings: List[List[float]],
        collection: str,
    ) -> int:
        """
        Insert or update vectors in a collection.

        Args:
            chunks: Text chunks with metadata.
            embeddings: Corresponding embedding vectors.
            collection: Target collection name.

        Returns:
            Number of points upserted.
        """
        if not self.available or not self._client:
            return 0

        if len(chunks) != len(embeddings):
            raise ValueError(
                f"Chunks ({len(chunks)}) and embeddings ({len(embeddings)}) "
                f"must have the same length"
            )

        from qdrant_client.models import PointStruct

        points = []
        for chunk, embedding in zip(chunks, embeddings):
            point_id = str(uuid.uuid4())
            payload = {
                "text": chunk.text,
                "source": chunk.source,
                "chunk_index": chunk.chunk_index,
                **chunk.metadata,
            }
            points.append(PointStruct(
                id=point_id,
                vector=embedding,
                payload=payload,
            ))

        try:
            # Batch upsert in groups of 100
            batch_size = 100
            for i in range(0, len(points), batch_size):
                batch = points[i:i + batch_size]
                self._client.upsert(
                    collection_name=collection,
                    points=batch,
                )

            logger.info(
                f"Upserted {len(points)} points to collection '{collection}'"
            )
            return len(points)

        except Exception as e:
            logger.error(f"Failed to upsert to '{collection}': {e}")
            return 0

    def search(
        self,
        query_vector: List[float],
        collection: str,
        limit: int = 10,
        score_threshold: Optional[float] = None,
        filters: Optional[Dict] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in a collection.

        Args:
            query_vector: Query embedding vector.
            collection: Collection to search.
            limit: Maximum results to return.
            score_threshold: Minimum similarity score.
            filters: Qdrant filter conditions.

        Returns:
            List of dicts with text, score, source, and metadata.
        """
        if not self.available or not self._client:
            return []

        try:
            from qdrant_client.models import Filter, FieldCondition, MatchValue

            # Build filter if provided
            qdrant_filter = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    conditions.append(
                        FieldCondition(key=key, match=MatchValue(value=value))
                    )
                qdrant_filter = Filter(must=conditions)

            results = self._client.search(
                collection_name=collection,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold,
                query_filter=qdrant_filter,
            )

            return [
                {
                    "text": hit.payload.get("text", ""),
                    "score": hit.score,
                    "source": hit.payload.get("source", ""),
                    "chunk_index": hit.payload.get("chunk_index", 0),
                    "metadata": {
                        k: v for k, v in hit.payload.items()
                        if k not in ("text", "source", "chunk_index")
                    },
                    "id": str(hit.id),
                }
                for hit in results
            ]

        except Exception as e:
            logger.error(f"Search failed in '{collection}': {e}")
            return []

    def delete_collection(self, name: str) -> bool:
        """Delete a collection."""
        if not self.available or not self._client:
            return False

        try:
            self._client.delete_collection(name)
            logger.info(f"Deleted collection '{name}'")
            return True
        except Exception as e:
            logger.error(f"Failed to delete collection '{name}': {e}")
            return False

    def collection_exists(self, name: str) -> bool:
        """Check if a collection exists."""
        if not self.available or not self._client:
            return False

        try:
            collections = self._client.get_collections().collections
            return any(c.name == name for c in collections)
        except Exception:
            return False

    def collection_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get collection statistics."""
        if not self.available or not self._client:
            return None

        try:
            info = self._client.get_collection(name)
            return {
                "name": name,
                "points_count": info.points_count,
                "vectors_count": info.vectors_count,
                "status": str(info.status),
            }
        except Exception:
            return None

    def ensure_collections(self, vector_size: int) -> None:
        """Create all default collections if they don't exist."""
        for name in _DEFAULT_COLLECTIONS:
            if not self.collection_exists(name):
                self.create_collection(name, vector_size)

    def __repr__(self):
        status = "ready" if self.available else "unavailable"
        if self.path:
            loc = f"local:{self.path}"
        elif self.url:
            loc = self.url
        else:
            loc = "in-memory"
        return f"QdrantStore({loc}, {status})"
