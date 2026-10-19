"""
GeoSI v2 — Server Authentication (Phase 1 — G2 fix)
════════════════════════════════════════════════════════════════════
FastAPI dependency functions for API key authentication.

Design (PRD §7, FR-5)
──────────────────────
* API keys are loaded from ``GEOSI_API_KEYS`` env var (comma-separated).
* Admin keys from ``GEOSI_ADMIN_KEYS`` (must also be in GEOSI_API_KEYS).
* ``Authorization: Bearer <key>`` header is required on all endpoints.
* 401 if key is missing or invalid.
* 403 if valid key is used on an admin-only endpoint but is not an admin key.

Usage in route files::

    from geosi_server.auth import api_key_auth, admin_auth

    @router.get("/layers")
    async def list_layers(api_key: str = Depends(api_key_auth)):
        ...

    @router.delete("/layers/{name}")
    async def delete_layer(name: str, api_key: str = Depends(admin_auth)):
        ...
"""

from __future__ import annotations

import logging
import os

from fastapi import Depends, Header, HTTPException, status

logger = logging.getLogger("geosi_server.auth")


def _load_keys(env_var: str) -> frozenset[str]:
    """Load a comma-separated set of API keys from an environment variable."""
    raw = os.environ.get(env_var, "")
    keys = {k.strip() for k in raw.split(",") if k.strip()}
    return frozenset(keys)


def _get_api_keys() -> frozenset[str]:
    """Return the current set of valid API keys (re-read on each call for hot-reload)."""
    return _load_keys("GEOSI_API_KEYS")


def _get_admin_keys() -> frozenset[str]:
    """Return the current set of admin API keys."""
    return _load_keys("GEOSI_ADMIN_KEYS")


def _extract_bearer_token(authorization: str | None) -> str | None:
    """
    Extract the token from an ``Authorization: Bearer <token>`` header.

    Returns ``None`` if the header is missing or malformed.
    """
    if not authorization:
        return None
    parts = authorization.strip().split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None


async def api_key_auth(
    authorization: str | None = Header(default=None),
) -> str:
    """
    FastAPI dependency: validate API key from ``Authorization: Bearer <key>`` header.

    Raises
    ------
    HTTP 401:
        If the Authorization header is missing, malformed, or the key is invalid.

    Returns
    -------
    str
        The validated API key (for downstream use as a session identifier).
    """
    token = _extract_bearer_token(authorization)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed Authorization header. Use: Bearer <api_key>",
            headers={"WWW-Authenticate": "Bearer"},
        )

    valid_keys = _get_api_keys()
    if not valid_keys:
        # No keys configured — warn loudly and deny all in production
        env = os.environ.get("GEOSI_ENV", "development").lower()
        if env == "production":
            logger.error("GEOSI_API_KEYS is not set in production mode. All requests denied.")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Server configuration error: authentication not configured.",
            )
        else:
            # Dev mode: log warning but allow (for local testing)
            logger.warning(
                "GEOSI_API_KEYS not set — authentication disabled in development mode. "
                "This is NOT safe for production."
            )
            return token  # accept any key in dev mode

    if token not in valid_keys:
        logger.warning("Invalid API key attempt: %s...", token[:8])
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token


async def admin_auth(
    api_key: str = Depends(api_key_auth),
) -> str:
    """
    FastAPI dependency: validate API key AND require admin privileges.

    Must be used after (or instead of) ``api_key_auth`` on admin endpoints.
    ``DELETE /layers/{name}`` and ``POST /admin/policy`` use this.

    Raises
    ------
    HTTP 403:
        If the key is valid but not in the admin key set.

    Returns
    -------
    str
        The validated admin API key.
    """
    admin_keys = _get_admin_keys()
    if not admin_keys:
        env = os.environ.get("GEOSI_ENV", "development").lower()
        if env == "production":
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Admin authentication not configured.",
            )
        # Dev mode: any authenticated key is treated as admin
        return api_key

    if api_key not in admin_keys:
        logger.warning("Non-admin key used on admin endpoint: %s...", api_key[:8])
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required for this endpoint.",
        )

    return api_key
