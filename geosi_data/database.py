# -*- coding: utf-8 -*-
"""
GeoSI v2 — Database Connection Manager
═══════════════════════════════════════════════════════════════════

Manages SQLAlchemy engine, session factory, and table initialization
for the PostGIS backend.

Configuration (G3 fix — no hardcoded fallback credentials)
──────────────────────────────────────────────────────────
Set the DATABASE_URL environment variable. There is NO default.

  GEOSI_ENV=production  + no DATABASE_URL  → RuntimeError at startup (fail-closed)
  GEOSI_ENV=development + no DATABASE_URL  → warning logged, availability=False
                                             (graceful degradation for dev/test)

Design:
    - Thread-safe session factory via SQLAlchemy sessionmaker.
    - All schema changes managed by Alembic migrations (not create_all).
"""

import os
import logging
from contextlib import contextmanager
from typing import Optional

logger = logging.getLogger("geosi_data.database")

# ---------------------------------------------------------------------------
# G3 fix: _DEFAULT_URL removed entirely.
# The application MUST be configured with DATABASE_URL.
# There is no silent fallback to any default credentials.
# ---------------------------------------------------------------------------


class Database:
    """
    SQLAlchemy-based connection manager for PostGIS.

    Usage::

        db = Database()
        with db.get_session() as session:
            session.add(record)
            # auto-commits on success, auto-rolls-back on error
    """

    def __init__(self, database_url: Optional[str] = None) -> None:
        """
        Initialise the database connection.

        Parameters
        ----------
        database_url:
            PostgreSQL connection string.  Falls back to the ``DATABASE_URL``
            environment variable.  If neither is provided:

            * ``GEOSI_ENV=production`` → raises ``RuntimeError`` (fail-closed).
            * ``GEOSI_ENV=development`` → logs a warning and sets
              ``self.available = False`` (graceful degradation).
        """
        url = database_url or os.environ.get("DATABASE_URL", "")

        if not url:
            env = os.environ.get("GEOSI_ENV", "development").lower()
            if env == "production":
                raise RuntimeError(
                    "DATABASE_URL is required in production mode but was not set. "
                    "Set the DATABASE_URL environment variable to a valid PostgreSQL "
                    "connection string before starting the server. "
                    "GeoSI refuses to start without a configured database in production."
                )
            else:
                logger.warning(
                    "DATABASE_URL not set. PostGIS persistence is DISABLED. "
                    "This is acceptable in development/test mode only. "
                    "Set DATABASE_URL before deploying to production."
                )
                self.url = ""
                self.available = False
                self._engine = None
                self._session_factory = None
                return

        self.url = url
        self.available = False
        self._engine = None
        self._session_factory = None

        try:
            from sqlalchemy import create_engine, text
            from sqlalchemy.orm import sessionmaker

            self._engine = create_engine(
                self.url,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=1800,
                echo=False,
            )

            # Test the connection
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            self._session_factory = sessionmaker(bind=self._engine)
            self.available = True
            logger.info("PostGIS connected: %s", self._mask_url(self.url))

        except Exception as exc:
            logger.warning(
                "PostGIS unavailable — persistence disabled. Error: %s", exc
            )
            self.available = False

    def init_db(self) -> bool:
        """
        Create all tables defined in db_models.py.

        .. deprecated::
            In production, use Alembic migrations:
            ``alembic upgrade head``
            ``create_all()`` is kept ONLY for development/testing convenience.

        Returns True if tables created successfully, False otherwise.
        """
        if not self.available:
            logger.warning("Cannot init DB — PostGIS not available")
            return False

        env = os.environ.get("GEOSI_ENV", "development").lower()
        if env == "production":
            logger.error(
                "init_db() (create_all) must NOT be called in production. "
                "Run 'alembic upgrade head' instead."
            )
            return False

        try:
            from geosi_data.db_models import Base

            logger.warning(
                "Using create_all() — development/test mode only. "
                "Run 'alembic upgrade head' before deploying to production."
            )
            Base.metadata.create_all(self._engine)
            logger.info("PostGIS tables created successfully (dev mode)")
            return True
        except Exception as exc:
            logger.error("Failed to create tables: %s", exc)
            return False

    @contextmanager
    def get_session(self):
        """
        Context manager for database sessions.

        Usage:
            with db.get_session() as session:
                session.add(record)
                # auto-commits on success, auto-rolls-back on error

        Yields:
            SQLAlchemy Session instance

        Raises:
            RuntimeError: If PostGIS is not available
        """
        if not self.available or self._session_factory is None:
            raise RuntimeError(
                "PostGIS is not available. Check DATABASE_URL and ensure "
                "PostgreSQL with PostGIS extension is running."
            )

        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def dispose(self):
        """Close all connections in the pool."""
        if self._engine:
            self._engine.dispose()
            logger.info("Database connections disposed")

    @staticmethod
    def _mask_url(url: str) -> str:
        """Mask password in connection URL for logging."""
        try:
            from urllib.parse import urlparse, urlunparse
            parsed = urlparse(url)
            if parsed.password:
                masked = parsed._replace(
                    netloc=f"{parsed.username}:***@{parsed.hostname}"
                    + (f":{parsed.port}" if parsed.port else "")
                )
                return urlunparse(masked)
        except Exception:
            pass
        return url.split("@")[-1] if "@" in url else url

    def __repr__(self):
        status = "connected" if self.available else "disconnected"
        return f"Database({status}, {self._mask_url(self.url)})"
