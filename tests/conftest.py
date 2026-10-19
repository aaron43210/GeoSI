"""
GeoSI v2 — Test Suite Root
===========================
Shared pytest fixtures available to all test modules.
"""

from __future__ import annotations

import pytest

# ---------------------------------------------------------------------------
# Environment bootstrap — ensure tests never accidentally hit production
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _isolate_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Force development mode and block real secrets in unit tests."""
    monkeypatch.setenv("GEOSI_ENV", "development")
    # Ensure no real DB URL leaks into unit tests
    monkeypatch.delenv("DATABASE_URL", raising=False)
    # Admin key must also be in GEOSI_API_KEYS (api_key_auth runs first in admin_auth chain)
    monkeypatch.setenv("GEOSI_API_KEYS", "test-key-unit,test-admin-key-unit")
    monkeypatch.setenv("GEOSI_ADMIN_KEYS", "test-admin-key-unit")
    monkeypatch.setenv("GEOSI_ALLOWED_ORIGINS", "http://localhost:3000")


# ---------------------------------------------------------------------------
# Re-usable mock factories
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_session_id() -> str:
    return "test-session-001"


@pytest.fixture
def mock_api_key() -> str:
    return "test-key-unit"


@pytest.fixture
def mock_admin_key() -> str:
    return "test-admin-key-unit"
