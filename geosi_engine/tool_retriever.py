"""
GeoSI Tool Retriever — semantic tool selection with an embedding model
══════════════════════════════════════════════════════════════════════

With 700+ QGIS algorithms the planner can only show the LLM a handful of
tools. This module picks them by meaning rather than by keywords:

    1. Each tool's name + display name + description is encoded once with
       an Ollama embedding model (default: nomic-embed-text).
    2. Vectors are cached on disk, keyed by model + a hash of the tool text,
       so only new or changed tools are re-encoded on the next start.
    3. A query is encoded and tools are ranked by cosine similarity.

nomic-embed-text expects task prefixes: "search_document: " for the
indexed text and "search_query: " for the query.

If the embedding model is unavailable, rank() returns [] and the caller
falls back to keyword ranking.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import os
import threading
from typing import Dict, List, Optional

logger = logging.getLogger("geosi_engine.tool_retriever")

_BATCH = 64


def _default_cache_path() -> str:
    base = os.environ.get("GEOSI_CACHE_DIR") or os.path.join(os.path.expanduser("~"), ".geosi")
    return os.path.join(base, "tool_embeddings.json")


def _normalize(vec: List[float]) -> List[float]:
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


class ToolRetriever:
    """Embedding index over a ToolRegistry, backed by Ollama /api/embed."""

    def __init__(
        self,
        registry,
        endpoint: Optional[str] = None,
        model: Optional[str] = None,
        cache_path: Optional[str] = None,
    ):
        self.registry = registry
        self.endpoint = endpoint or os.environ.get("OLLAMA_ENDPOINT", "http://localhost:11434")
        self.model = model or os.environ.get("GEOSI_EMBED_MODEL", "nomic-embed-text")
        self.cache_path = cache_path or _default_cache_path()
        self._vectors: Dict[str, List[float]] = {}
        self._indexed_count = -1
        self._disabled = False
        self._lock = threading.Lock()

    # ── Embedding calls ───────────────────────────────────────────────

    def _embed(self, texts: List[str]) -> List[List[float]]:
        import requests

        resp = requests.post(
            f"{self.endpoint}/api/embed",
            json={"model": self.model, "input": texts},
            timeout=120,
        )
        resp.raise_for_status()
        return [_normalize(v) for v in resp.json()["embeddings"]]

    @staticmethod
    def _tool_text(spec) -> str:
        return f"{spec.display_name} ({spec.name}): {spec.description[:400]}"

    # ── Index build (incremental, cached) ─────────────────────────────

    def _load_cache(self) -> Dict[str, List[float]]:
        try:
            with open(self.cache_path, encoding="utf-8") as fh:
                data = json.load(fh)
            if data.get("model") == self.model:
                return data.get("vectors", {})
        except (OSError, ValueError):
            pass
        return {}

    def _save_cache(self, vectors: Dict[str, List[float]]) -> None:
        try:
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            tmp = self.cache_path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump({"model": self.model, "vectors": vectors}, fh)
            os.replace(tmp, self.cache_path)
        except OSError as e:
            logger.warning(f"Could not write embedding cache: {e}")

    def _ensure_index(self) -> bool:
        if self._disabled:
            return False
        specs = self.registry.list_tools()
        if self._indexed_count == len(specs):
            return True
        with self._lock:
            cache = self._load_cache()
            vectors: Dict[str, List[float]] = {}
            missing = []
            for spec in specs:
                text = self._tool_text(spec)
                key = hashlib.sha1(text.encode("utf-8"), usedforsecurity=False).hexdigest()  # noqa: S324
                if key in cache:
                    vectors[spec.name] = cache[key]
                else:
                    missing.append((spec.name, key, text))
            try:
                for i in range(0, len(missing), _BATCH):
                    batch = missing[i : i + _BATCH]
                    embs = self._embed([f"search_document: {t}" for _, _, t in batch])
                    for (name, key, _), vec in zip(batch, embs):
                        vectors[name] = vec
                        cache[key] = vec
            except Exception as e:
                logger.warning(f"Embedding model '{self.model}' unavailable, using keyword ranking: {e}")
                self._disabled = True
                return False
            if missing:
                self._save_cache(cache)
                logger.info(f"Embedded {len(missing)} tool(s) with {self.model}")
            self._vectors = vectors
            self._indexed_count = len(specs)
        return True

    # ── Query ─────────────────────────────────────────────────────────

    def rank(self, query: str, top_k: int = 12) -> List[str]:
        """Return up to top_k tool names, most semantically similar first."""
        if not query or not self._ensure_index():
            return []
        try:
            q = self._embed([f"search_query: {query}"])[0]
        except Exception as e:
            logger.warning(f"Query embedding failed: {e}")
            return []
        scored = [(sum(a * b for a, b in zip(q, vec)), name) for name, vec in self._vectors.items()]
        scored.sort(reverse=True)
        return [name for _, name in scored[:top_k]]
