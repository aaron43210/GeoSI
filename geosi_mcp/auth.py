"""
GeoSI v2 — MCP Auth Middleware (FR-5.3)
════════════════════════════════════════════════════════════════════
Token-based authentication for the MCP server.

Security model:
  - Bearer token from ``GEOSI_MCP_TOKEN`` environment variable
  - Constant-time comparison to prevent timing attacks (hmac.compare_digest)
  - development + no token  → allow  (dev convenience)
  - production   + no token → DENY   (fail closed — same as main API)
  - All MCP calls pass through Supervisor + Permission & Safety (FR-5.2) —
    never bypass path.
"""

from __future__ import annotations

import hmac
import logging
import os

logger = logging.getLogger("geosi_mcp.auth")


def get_mcp_token() -> str | None:
    """Return the configured MCP token from environment."""
    return os.environ.get("GEOSI_MCP_TOKEN", "").strip() or None


def verify_mcp_token(provided: str) -> bool:
    """
    Constant-time comparison of provided token against the configured MCP token.
    Uses ``hmac.compare_digest`` to prevent timing-based side-channel attacks.

    Security contract (mirrors geosi_server/auth.py):
    - development + no token → True   (local testing convenience)
    - production   + no token → False  (FAIL CLOSED — Bug #2 fix)
    - any env      + token set → constant-time compare, True only on match
    """
    expected = get_mcp_token()
    env = os.environ.get("GEOSI_ENV", "development").lower()

    if not expected:
        if env == "production":
            # FAIL CLOSED in production: same contract as main API (geosi_server/auth.py
            # raises HTTP 503 when GEOSI_API_KEYS is unset in production).
            # A forgotten GEOSI_MCP_TOKEN must never silently open MCP to everyone.
            logger.error(
                "GEOSI_MCP_TOKEN is not set in GEOSI_ENV=production — "
                "MCP access DENIED. Set GEOSI_MCP_TOKEN before deploying."
            )
            return False
        # Dev / staging only: allow without token for local testing convenience.
        logger.warning(
            "GEOSI_MCP_TOKEN is not set — MCP auth disabled (development mode only). "
            "Set GEOSI_ENV=production and GEOSI_MCP_TOKEN before any production deploy."
        )
        return True

    return hmac.compare_digest(
        provided.encode("utf-8"),
        expected.encode("utf-8"),
    )


def extract_bearer_token(authorization: str) -> str | None:
    """Extract token from 'Bearer <token>' Authorization header."""
    if not authorization:
        return None
    parts = authorization.split(" ", 1)
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1].strip()
    return None
