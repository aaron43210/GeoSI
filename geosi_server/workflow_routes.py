"""
GeoSI Server — Workflow Routes
═══════════════════════════════════════════════════════════════════

Endpoints:
    POST /workflow/search   — Search workflow knowledge base
    POST /workflow/suggest  — Get workflow suggestion for a query
    GET  /workflow/history   — Get execution history
    GET  /workflow/stats     — Get tool reliability statistics
"""

import logging

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from geosi_server.auth import api_key_auth

logger = logging.getLogger("geosi_server.workflow")
router = APIRouter()


# ── Request/Response models ────────────────────────────────────────────


class WorkflowSearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    limit: int = Field(5, ge=1, le=20)


class WorkflowItem(BaseModel):
    name: str
    description: str
    user_query: str
    tool_sequence: list[str]
    success: bool = True
    tags: list[str] = []


class WorkflowSearchResponse(BaseModel):
    query: str
    workflows: list[WorkflowItem]
    total: int


class WorkflowSuggestRequest(BaseModel):
    query: str = Field(..., description="User query to get workflow suggestion")


class WorkflowSuggestResponse(BaseModel):
    query: str
    suggested_workflows: list[WorkflowItem]
    knowledge_context: str
    tool_warnings: list[str]


class HistoryItem(BaseModel):
    id: str
    query: str
    status: str
    tool_sequence: list[str] = []
    duration_ms: float = 0.0
    created_at: str | None = None


# ── Endpoints ──────────────────────────────────────────────────────────


@router.post("/search", response_model=WorkflowSearchResponse)
async def workflow_search(req: WorkflowSearchRequest, api_key: str = Depends(api_key_auth)):
    """
    Search the workflow knowledge base for similar past workflows.
    """
    from geosi_server.app import get_pool

    engine = get_pool().get_or_create(api_key)

    workflows = []
    if engine.knowledge:
        similar = engine.knowledge.workflow_memory.find_similar(req.query, limit=req.limit)
        workflows = [
            WorkflowItem(
                name=wf.name,
                description=wf.description,
                user_query=wf.user_query,
                tool_sequence=wf.tool_sequence,
                success=wf.success,
                tags=wf.tags,
            )
            for wf in similar
        ]

    return WorkflowSearchResponse(
        query=req.query,
        workflows=workflows,
        total=len(workflows),
    )


@router.post("/suggest", response_model=WorkflowSuggestResponse)
async def workflow_suggest(req: WorkflowSuggestRequest, api_key: str = Depends(api_key_auth)):
    """
    Get workflow suggestions for a query using the full knowledge layer.

    Returns matching workflows plus the assembled knowledge context
    that would enhance the planning agent's decision-making.
    """
    from geosi_server.app import get_pool

    engine = get_pool().get_or_create(api_key)

    suggested = []
    context = ""
    warnings = []

    if engine.knowledge:
        ctx = engine.knowledge.retrieve_context(req.query)
        context = ctx.context_prompt
        warnings = ctx.tool_warnings

        suggested = [
            WorkflowItem(
                name=wf.name,
                description=wf.description,
                user_query=wf.user_query,
                tool_sequence=wf.tool_sequence,
                success=wf.success,
                tags=wf.tags,
            )
            for wf in ctx.similar_workflows
        ]

    return WorkflowSuggestResponse(
        query=req.query,
        suggested_workflows=suggested,
        knowledge_context=context,
        tool_warnings=warnings,
    )


@router.get("/history", response_model=list[HistoryItem])
async def workflow_history(limit: int = 50, api_key: str = Depends(api_key_auth)):
    """Get recent workflow execution history."""
    from geosi_server.app import get_pool

    engine = get_pool().get_or_create(api_key)

    history = engine.get_workflow_history()

    return [
        HistoryItem(
            id=h.get("id", ""),
            query=h.get("query", ""),
            status=h.get("status", "unknown"),
            tool_sequence=h.get("tool_sequence", []),
            duration_ms=h.get("duration_ms", 0.0),
            created_at=h.get("created_at"),
        )
        for h in history[:limit]
    ]


@router.get("/stats")
async def workflow_stats(api_key: str = Depends(api_key_auth)):
    """Get tool reliability and usage statistics."""
    from geosi_server.app import get_pool

    engine = get_pool().get_or_create(api_key)

    stats = {}
    if engine.knowledge:
        stats["tool_reliability"] = engine.knowledge.feedback_memory.get_tool_reliability()
        stats["failure_patterns"] = [
            {
                "tool": p.tool_name,
                "error_type": p.error_type,
                "frequency": p.frequency,
                "workaround": p.workaround,
            }
            for p in engine.knowledge.feedback_memory.get_failure_patterns()
        ]
        stats["frequent_operations"] = engine.knowledge.query_memory.get_frequent_operations()
        stats["user_preferences"] = engine.knowledge.query_memory.get_user_preferences()

    return stats
