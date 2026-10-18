# -*- coding: utf-8 -*-
"""
GeoSI v2 — Admin Routes (Phase P1 gap)
════════════════════════════════════════════════════════════════════
Admin-only endpoints (PRD §5.4, §11, FR-2.3):

  POST /admin/policy          — create or update a PolicyOverrideRecord
  DELETE /admin/policy/{id}   — remove an override
  GET  /admin/policy          — list all overrides
"""
from __future__ import annotations

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from geosi_server.auth import admin_auth

logger = logging.getLogger("geosi_server.admin")
router = APIRouter()


# ── Request / Response models ─────────────────────────────────────────

class PolicyOverrideIn(BaseModel):
    """Body for creating / updating a policy override."""

    algorithm_id: str = Field(
        ...,
        description="QGIS algorithm ID, e.g. 'native:buffer' or 'gdal:translate'",
        min_length=1,
        max_length=255,
    )
    decision: str = Field(
        ...,
        pattern="^(allow|ask|deny)$",
        description="Override decision: 'allow' | 'ask' | 'deny'",
    )
    note: Optional[str] = Field(None, description="Human-readable reason for this override")


class PolicyOverrideOut(BaseModel):
    id: str
    algorithm_id: str
    decision: str
    set_by: str
    note: Optional[str] = None
    created_at: str
    updated_at: str


# ── Endpoints ─────────────────────────────────────────────────────────

@router.get("/policy", response_model=List[PolicyOverrideOut], tags=["Admin"])
async def list_policy_overrides(api_key: str = Depends(admin_auth)):
    """
    List all per-algorithm policy overrides (FR-2.3).

    Returns the full contents of ``geosi_policy_overrides``.
    """
    from geosi_server.app import get_pool
    from geosi_data.db_models import PolicyOverrideRecord

    engine = get_pool().get_or_create(api_key)
    db = _get_db(engine)
    if db is None:
        return []

    try:
        with db.get_session() as session:
            records = session.query(PolicyOverrideRecord).all()
            return [
                PolicyOverrideOut(
                    id=r.id,
                    algorithm_id=r.algorithm_id,
                    decision=r.decision,
                    set_by=r.set_by,
                    note=r.note,
                    created_at=str(r.created_at),
                    updated_at=str(r.updated_at),
                )
                for r in records
            ]
    except Exception as exc:
        logger.error("Failed to list policy overrides: %s", exc)
        raise HTTPException(status_code=500, detail="Database error listing policies.")


@router.post("/policy", response_model=PolicyOverrideOut, status_code=status.HTTP_201_CREATED, tags=["Admin"])
async def upsert_policy_override(
    req: PolicyOverrideIn,
    api_key: str = Depends(admin_auth),
):
    """
    Create or update a per-algorithm policy override (FR-2.3).

    If an override already exists for ``algorithm_id``, it is updated in-place.
    The ``PermissionSafetyAgent`` consults this table on every tool invocation.

    Examples
    --------
    - Lock down ``native:deletefield`` → deny for all users:
      ``{"algorithm_id": "native:deletefield", "decision": "deny"}``
    - Fast-track ``native:buffer`` → allow (skip HITL for this trusted op):
      ``{"algorithm_id": "native:buffer", "decision": "allow"}``
    """
    from geosi_server.app import get_pool
    from geosi_data.db_models import PolicyOverrideRecord
    from datetime import datetime, timezone

    engine = get_pool().get_or_create(api_key)
    db = _get_db(engine)
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="PostGIS is not available — policy overrides require a database connection.",
        )

    try:
        with db.get_session() as session:
            existing = (
                session.query(PolicyOverrideRecord)
                .filter(PolicyOverrideRecord.algorithm_id == req.algorithm_id)
                .first()
            )
            if existing:
                existing.decision = req.decision
                existing.set_by = api_key[:8] + "..."  # anonymise key
                existing.note = req.note
                existing.updated_at = datetime.now(timezone.utc)
                record = existing
            else:
                record = PolicyOverrideRecord(
                    algorithm_id=req.algorithm_id,
                    decision=req.decision,
                    set_by=api_key[:8] + "...",
                    note=req.note,
                )
                session.add(record)

        logger.info(
            "Policy override upserted: algorithm=%s decision=%s by=%s",
            req.algorithm_id,
            req.decision,
            api_key[:8],
        )
        # Re-query after commit to return the persisted object
        with db.get_session() as session:
            record = (
                session.query(PolicyOverrideRecord)
                .filter(PolicyOverrideRecord.algorithm_id == req.algorithm_id)
                .first()
            )
            return PolicyOverrideOut(
                id=record.id,
                algorithm_id=record.algorithm_id,
                decision=record.decision,
                set_by=record.set_by,
                note=record.note,
                created_at=str(record.created_at),
                updated_at=str(record.updated_at),
            )

    except Exception as exc:
        logger.error("Failed to upsert policy override: %s", exc)
        raise HTTPException(status_code=500, detail=f"Database error: {exc}")


@router.delete(
    "/policy/{algorithm_id:path}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Admin"],
)
async def delete_policy_override(
    algorithm_id: str,
    api_key: str = Depends(admin_auth),
):
    """
    Remove a policy override, restoring the default risk-based policy for that algorithm.
    """
    from geosi_server.app import get_pool
    from geosi_data.db_models import PolicyOverrideRecord

    engine = get_pool().get_or_create(api_key)
    db = _get_db(engine)
    if db is None:
        raise HTTPException(status_code=503, detail="PostGIS not available.")

    try:
        with db.get_session() as session:
            deleted = (
                session.query(PolicyOverrideRecord)
                .filter(PolicyOverrideRecord.algorithm_id == algorithm_id)
                .delete()
            )
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No policy override found for algorithm_id={algorithm_id!r}",
            )
        logger.info("Policy override deleted: algorithm=%s by=%s", algorithm_id, api_key[:8])
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Failed to delete policy override: %s", exc)
        raise HTTPException(status_code=500, detail=f"Database error: {exc}")


# ── Helper ────────────────────────────────────────────────────────────

def _get_db(engine):
    """Extract the Database object from a GeoSI engine instance."""
    if engine and engine.data:
        return engine.data.get("database")
    return None
