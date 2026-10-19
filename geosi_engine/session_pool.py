# -*- coding: utf-8 -*-
"""
GeoSI v2 — Session Pool
════════════════════════════════════════════════════════════════════
Replaces the global singleton ``_engine = None`` (G10 fix).

Each (session_id / API-key) gets its own GeoSI engine instance so
two concurrent users can never see each other's workspace state.

Design
------
* LRU cache backed by ``collections.OrderedDict`` — O(1) get/promote.
* TTL eviction on access: idle sessions are expired lazily on the next
  ``get_or_create`` call.  A background thread could also run periodic
  eviction, but lazy eviction is simpler and correct for single-process
  deployments.
* Thread-safe via ``threading.RLock`` (reentrant to allow internal
  helpers to call ``_evict_expired`` safely).

PRD references: FR-6.1, FR-6.2 (G10 fix)
"""
from __future__ import annotations

import logging
import time
import threading
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

logger = logging.getLogger("geosi_engine.session_pool")


@dataclass
class _SessionEntry:
    """Internal record stored per session."""

    engine: Any  # GeoSI instance — typed as Any to avoid circular import
    created_at: float = field(default_factory=time.monotonic)
    last_accessed: float = field(default_factory=time.monotonic)
    access_count: int = 0

    def touch(self) -> None:
        self.last_accessed = time.monotonic()
        self.access_count += 1

    def is_expired(self, ttl_seconds: float) -> bool:
        return (time.monotonic() - self.last_accessed) > ttl_seconds


class SessionPool:
    """
    LRU cache of ``GeoSI`` engine instances keyed by session/API-key.

    Parameters
    ----------
    max_size:
        Maximum number of concurrent sessions.  When the pool is full the
        least-recently-used session is evicted before the new one is created.
    ttl_seconds:
        Seconds of idle time after which a session is considered expired and
        will be evicted on the next access.

    Usage
    -----
    ::

        pool = SessionPool(max_size=50, ttl_seconds=1800)
        engine = pool.get_or_create("user-session-abc")
        # … use engine …
        pool.close_session("user-session-abc")
    """

    def __init__(
        self,
        max_size: int = 50,
        ttl_seconds: float = 1800.0,
        factory: Optional[Callable[[str], Any]] = None,
    ) -> None:
        self._max_size = max_size
        self._ttl = ttl_seconds
        # factory(session_id) → engine. The server passes one that installs
        # the headless QGIS tools; the plugin passes its own engine.
        self._factory = factory
        self._sessions: OrderedDict[str, _SessionEntry] = OrderedDict()
        self._lock = threading.RLock()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_or_create(self, session_id: str) -> Any:
        """
        Return the existing ``GeoSI`` instance for *session_id*, or create a
        fresh one.

        On each call the session's LRU position is promoted to the front and
        its ``last_accessed`` timestamp is refreshed.  Expired sessions are
        evicted lazily before new ones are created.

        Parameters
        ----------
        session_id:
            Opaque string identifying the caller — typically the API key or
            a per-request session token extracted by the auth middleware.

        Returns
        -------
        GeoSI
            A per-session engine instance.
        """
        with self._lock:
            self._evict_expired()

            if session_id in self._sessions:
                entry = self._sessions[session_id]
                entry.touch()
                # Promote to front (most-recently used)
                self._sessions.move_to_end(session_id, last=False)
                logger.debug(
                    "Session cache hit: %s (access #%d)",
                    session_id,
                    entry.access_count,
                )
                return entry.engine

            # Create a new engine
            if len(self._sessions) >= self._max_size:
                self._evict_lru()

            engine = self._factory(session_id) if self._factory else self._create_engine(session_id)
            try:
                engine._session_id = session_id  # used by audit log entries
            except Exception:
                logger.debug("suppressed exception", exc_info=True)
            entry = _SessionEntry(engine=engine)
            self._sessions[session_id] = entry
            self._sessions.move_to_end(session_id, last=False)
            logger.info("Session created: %s (pool size=%d)", session_id, len(self._sessions))
            return engine

    def close_session(self, session_id: str) -> bool:
        """
        Immediately close and remove the session.

        Returns ``True`` if the session existed and was removed.
        """
        with self._lock:
            if session_id not in self._sessions:
                return False
            self._destroy_entry(session_id, self._sessions.pop(session_id))
            logger.info("Session closed: %s (pool size=%d)", session_id, len(self._sessions))
            return True

    def cleanup(self) -> int:
        """
        Close and destroy ALL sessions (called on server shutdown).

        Returns the number of sessions that were closed. Safe to call
        multiple times.
        """
        with self._lock:
            count = len(self._sessions)
            for sid, entry in list(self._sessions.items()):
                self._destroy_entry(sid, entry)
            self._sessions.clear()
            if count:
                logger.info("Session pool cleaned up: %d session(s) closed", count)
            return count

    # ``shutdown_all`` kept as an alias for callers that expect that name.
    shutdown_all = cleanup

    def evict_expired(self) -> int:
        """
        Explicitly evict all expired sessions.  Can be called from a
        background maintenance task.

        Returns the number of sessions evicted.
        """
        with self._lock:
            return self._evict_expired()

    def size(self) -> int:
        """Return current number of active sessions."""
        with self._lock:
            return len(self._sessions)

    def stats(self) -> dict[str, Any]:
        """Return a summary dict for the ``/health`` endpoint."""
        with self._lock:
            now = time.monotonic()
            return {
                "active_sessions": len(self._sessions),
                "max_size": self._max_size,
                "ttl_seconds": self._ttl,
                "session_ids": list(self._sessions.keys()),
                "oldest_idle_seconds": max(
                    (now - e.last_accessed for e in self._sessions.values()),
                    default=0.0,
                ),
            }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _evict_expired(self) -> int:
        """Evict all sessions whose idle time exceeds ``_ttl``. NOT thread-safe
        on its own — must be called inside the lock."""
        expired = [sid for sid, e in self._sessions.items() if e.is_expired(self._ttl)]
        for sid in expired:
            entry = self._sessions.pop(sid)
            self._destroy_entry(sid, entry)
            logger.info("Session TTL-evicted: %s", sid)
        return len(expired)

    def _evict_lru(self) -> None:
        """Evict the least-recently-used session. NOT thread-safe on its own."""
        if not self._sessions:
            return
        # LRU is at the end (OrderedDict, last=False means MRU at front)
        sid, entry = self._sessions.popitem(last=True)
        self._destroy_entry(sid, entry)
        logger.info("Session LRU-evicted: %s", sid)

    @staticmethod
    def _destroy_entry(session_id: str, entry: _SessionEntry) -> None:
        """Clean up a GeoSI engine instance on eviction."""
        try:
            # GeoSI exposes an optional cleanup method; ignore if absent
            if hasattr(entry.engine, "shutdown"):
                entry.engine.shutdown()
        except Exception as exc:
            logger.warning("Error shutting down session %s: %s", session_id, exc)

    @staticmethod
    def _create_engine(session_id: str) -> Any:
        """Instantiate a fresh, isolated GeoSI engine for this session."""
        import os

        from geosi_engine import GeoSI  # local import to avoid circular deps

        knowledge = os.environ.get("GEOSI_ENABLE_KNOWLEDGE", "").lower() in ("1", "true", "yes")
        engine = GeoSI(enable_knowledge=knowledge)
        # Attach the session ID so agents can include it in audit log entries
        engine._session_id = session_id  # type: ignore[attr-defined]
        return engine
