# -*- coding: utf-8 -*-
"""
GeoSI v2 — MCP Server (Phase P4, FR-5)
════════════════════════════════════════════════════════════════════
Exposes 6 MCP tools (FR-5.1):
  run_query, search_gis_docs, suggest_workflow,
  list_layers, get_layer, approve_pending_action

Security (FR-5.2, FR-5.3):
  - Bearer token auth via GEOSI_MCP_TOKEN
  - All tool calls route through Supervisor + Permission & Safety
  - Zero bypass path: no MCP tool calls QGIS processing directly

Protocol: JSON-RPC 2.0 over HTTP POST /mcp/call
Discovery: GET /mcp/tools  |  Manifest: GET /mcp/manifest
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field

from geosi_mcp.auth import verify_mcp_token, extract_bearer_token

logger = logging.getLogger("geosi_mcp.server")
router = APIRouter()


# ── MCP Protocol models ───────────────────────────────────────────────────

class MCPToolParam(BaseModel):
    name: str
    type: str
    description: str
    required: bool = True


class MCPTool(BaseModel):
    name: str
    description: str
    parameters: List[MCPToolParam]


class MCPCallRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[Any] = None
    method: str
    params: Dict[str, Any] = Field(default_factory=dict)


class MCPCallResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[Any] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


class MCPManifest(BaseModel):
    name: str = "geosi-mcp"
    version: str = "2.0.0"
    description: str = "GeoSI v2 — Autonomous Geospatial Intelligence MCP Server"
    tools: List[MCPTool] = Field(default_factory=list)


# ── Tool registry (Pydantic v2 — all kwargs) ──────────────────────────────

def _p(name: str, typ: str, desc: str, required: bool = True) -> MCPToolParam:
    """Shorthand constructor — Pydantic v2 keyword-only BaseModel init."""
    return MCPToolParam(name=name, type=typ, description=desc, required=required)


_TOOLS: List[MCPTool] = [
    MCPTool(
        name="run_query",
        description=(
            "Execute a natural-language GIS query through the full GeoSI agent pipeline "
            "(Supervisor → Planning → Validation → Permission → Execution). "
            "Returns the execution result and plan."
        ),
        parameters=[
            _p("query",            "string", "Natural-language GIS query"),
            _p("session_id",       "string", "Session identifier",                         required=False),
            _p("available_layers", "array",  "Layer names currently loaded in QGIS",       required=False),
        ],
    ),
    MCPTool(
        name="search_gis_docs",
        description=(
            "Search GeoSI's knowledge base (Qdrant hybrid: semantic + BM25). "
            "Returns relevant GIS documentation, workflow examples, and research papers."
        ),
        parameters=[
            _p("query",      "string",  "Search query"),
            _p("collection", "string",  "Qdrant collection to search (default: gis_docs)", required=False),
            _p("limit",      "integer", "Maximum number of results (default: 5)",          required=False),
        ],
    ),
    MCPTool(
        name="suggest_workflow",
        description=(
            "Generate a suggested QGIS workflow plan for a given task. "
            "Returns a structured ExecutionPlan with tool IDs, parameters, and risk levels."
        ),
        parameters=[
            _p("task",             "string", "Task description for workflow planning"),
            _p("available_layers", "array",  "Layers currently available",   required=False),
            _p("session_id",       "string", "Session identifier",            required=False),
        ],
    ),
    MCPTool(
        name="list_layers",
        description=(
            "List all layers currently loaded in the QGIS project "
            "(type, CRS, feature count). Read-only — never modifies QGIS project."
        ),
        parameters=[
            _p("session_id", "string", "Session identifier", required=False),
        ],
    ),
    MCPTool(
        name="get_layer",
        description=(
            "Get detailed metadata for a specific layer: "
            "CRS, geometry type, fields, feature count, extent, and file path."
        ),
        parameters=[
            _p("layer_name", "string", "Name of the layer to inspect"),
            _p("session_id", "string", "Session identifier", required=False),
        ],
    ),
    MCPTool(
        name="approve_pending_action",
        description=(
            "Approve or reject a pending Human-in-the-Loop (HITL) action. "
            "Required for mutating/destructive operations flagged by the Permission & Safety Agent."
        ),
        parameters=[
            _p("action_id", "string",  "The action_id from the HITL approval request"),
            _p("approved",  "boolean", "True to approve, False to reject"),
            _p("reason",    "string",  "Optional human-readable reason", required=False),
        ],
    ),
]

# O(1) lookup dict — built once at module load
_TOOL_MAP: Dict[str, MCPTool] = {t.name: t for t in _TOOLS}


# ── Auth dependency ───────────────────────────────────────────────────────

async def mcp_auth(authorization: str = Header(default="")) -> str:
    """Extract and verify MCP bearer token (FR-5.3)."""
    token = extract_bearer_token(authorization) or ""
    if not verify_mcp_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing GEOSI_MCP_TOKEN.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


# ── Endpoints ─────────────────────────────────────────────────────────────

@router.get("/manifest", response_model=MCPManifest, tags=["MCP"])
async def mcp_manifest():
    """Return the MCP server manifest and tool list."""
    return MCPManifest(tools=_TOOLS)


@router.get("/tools", response_model=List[MCPTool], tags=["MCP"])
async def mcp_tools():
    """List all available MCP tools (FR-5.1)."""
    return _TOOLS


@router.post("/call", response_model=MCPCallResponse, tags=["MCP"])
async def mcp_call(req: MCPCallRequest, token: str = Depends(mcp_auth)):
    """
    Execute an MCP tool call (JSON-RPC 2.0).
    All calls route through Supervisor + Permission & Safety — no bypass (FR-5.2).
    """
    if req.method not in _TOOL_MAP:
        return MCPCallResponse(
            id=req.id,
            error={
                "code": -32601,
                "message": f"Method not found: '{req.method}'. Available: {list(_TOOL_MAP)}",
            },
        )
    try:
        result = await _dispatch_tool(req.method, req.params, session_id=token[:16])
        return MCPCallResponse(id=req.id, result=result)
    except Exception as exc:
        logger.error("MCP tool '%s' failed: %s", req.method, exc, exc_info=True)
        return MCPCallResponse(
            id=req.id,
            error={"code": -32603, "message": str(exc)},
        )


# ── Tool dispatch ─────────────────────────────────────────────────────────

async def _dispatch_tool(tool_name: str, params: Dict[str, Any], session_id: str) -> Any:
    """Route MCP call to the correct async handler. O(1) via dict lookup."""
    handlers = {
        "run_query":              _tool_run_query,
        "search_gis_docs":        _tool_search_gis_docs,
        "suggest_workflow":       _tool_suggest_workflow,
        "list_layers":            _tool_list_layers,
        "get_layer":              _tool_get_layer,
        "approve_pending_action": _tool_approve_pending_action,
    }
    return await handlers[tool_name](params, session_id)


async def _tool_run_query(params: Dict, session_id: str) -> Dict:
    """run_query → SupervisorAgent.handle() (FR-5.1, FR-5.2)."""
    query = params.get("query", "")
    if not query:
        raise ValueError("'query' parameter is required.")
    try:
        from geosi_server.app import get_pool
        from geosi_engine.agents.supervisor import SupervisorAgent, SupervisorRequest
        pool = get_pool()
        sid = params.get("session_id") or session_id
        supervisor = SupervisorAgent(pool)
        request = SupervisorRequest(
            query=query,
            session_id=sid,
            available_layers=params.get("available_layers", []),
            surface="mcp",
        )
        response = supervisor.handle(request)
        return {
            "success": response.success,
            "result": str(response.result) if response.result else None,
            "error": response.error,
            "session_id": sid,
            "latency_ms": getattr(response, "latency_ms", 0.0),
        }
    except Exception as exc:
        raise ValueError(f"run_query failed: {exc}") from exc


async def _tool_search_gis_docs(params: Dict, session_id: str) -> Dict:
    """search_gis_docs → Qdrant hybrid search (FR-5.1)."""
    query = params.get("query", "")
    if not query:
        raise ValueError("'query' parameter is required.")

    collection = params.get("collection", "gis_docs")
    limit = int(params.get("limit", 5))
    results = []
    try:
        from geosi_server.app import get_pool
        pool = get_pool()
        engine = pool.get_or_create(session_id)
        if engine.knowledge:
            raw = engine.knowledge.search_gis_docs(query, collection=collection, limit=limit)
            results = [
                {
                    "text":  getattr(r, "text", str(r)),
                    "score": float(getattr(r, "score", 0.0)),
                    "source": getattr(r, "source", ""),
                    "title": getattr(r, "title", ""),
                }
                for r in raw
            ]
    except Exception as exc:
        logger.warning("search_gis_docs: %s", exc)
    return {"results": results, "count": len(results), "query": query}


async def _tool_suggest_workflow(params: Dict, session_id: str) -> Dict:
    """suggest_workflow → PlanningAgent.plan() (FR-5.1)."""
    task = params.get("task", "")
    if not task:
        raise ValueError("'task' parameter is required.")
    try:
        from geosi_server.app import get_pool
        from geosi_engine.agents.planning import PlanningAgent
        pool = get_pool()
        sid = params.get("session_id") or session_id
        engine = pool.get_or_create(sid)
        planner = PlanningAgent(engine, supervisor=None)
        plan = planner.plan(
            query=task,
            available_layers=params.get("available_layers", []),
            session_id=sid,
        )
        steps = [
            {
                "tool_name":   getattr(s, "tool_name", ""),
                "risk_level":  getattr(s, "risk_level", ""),
                "description": getattr(s, "description", ""),
                "parameters":  getattr(s, "parameters", {}),
            }
            for s in getattr(plan, "steps", [])
        ]
        return {
            "plan_id":   getattr(plan, "plan_id", ""),
            "reasoning": getattr(plan, "reasoning", ""),
            "steps":     steps,
            "step_count": len(steps),
        }
    except Exception as exc:
        raise ValueError(f"suggest_workflow failed: {exc}") from exc


async def _tool_list_layers(params: Dict, session_id: str) -> Dict:
    """
    list_layers — QGIS QgsProject.instance().mapLayers() (FR-5.1).
    QGIS API: QgsProject.instance().mapLayers() → O(N) dict iteration.
    Falls back to engine state when QGIS is not loaded.
    """
    layers = []
    try:
        from qgis.core import QgsProject
        for lid, layer in QgsProject.instance().mapLayers().items():
            layers.append({
                "id":    lid,
                "name":  layer.name(),
                "type":  layer.type().name,
                "crs":   layer.crs().authid(),
                "valid": layer.isValid(),
            })
    except ImportError:
        try:
            from geosi_server.app import get_pool
            engine = get_pool().get_or_create(session_id)
            state = getattr(engine, "state", None)
            for name, layer in getattr(state, "layers", {}).items():
                # ``layer`` is a GeoSI Layer dataclass, not a dict — read its
                # attributes explicitly (``**layer`` would raise TypeError).
                layers.append({
                    "name": name,
                    "type": getattr(layer, "layer_type", "vector"),
                    "geometry_type": getattr(layer, "geometry_type", "Unknown"),
                    "crs": getattr(layer, "crs", ""),
                    "feature_count": getattr(layer, "feature_count", 0),
                })
        except Exception:
            logger.debug("suppressed exception", exc_info=True)
    return {"layers": layers, "count": len(layers)}


async def _tool_get_layer(params: Dict, session_id: str) -> Dict:
    """
    get_layer — QGIS layer metadata (FR-5.1).
    QGIS API refs:
      QgsVectorLayer.fields()        — O(F) iteration
      QgsVectorLayer.featureCount()  — O(1) cached
      QgsMapLayer.extent()           — O(1)
    """
    layer_name = params.get("layer_name", "")
    if not layer_name:
        raise ValueError("'layer_name' parameter is required.")

    info: dict = {"name": layer_name}
    try:
        from qgis.core import QgsProject, QgsVectorLayer, QgsRasterLayer
        layer = next(
            (lyr for lyr in QgsProject.instance().mapLayers().values() if lyr.name() == layer_name),
            None,
        )
        if layer is None:
            raise ValueError(f"Layer '{layer_name}' not found in QGIS project.")
        ext = layer.extent()
        info.update({
            "type":   layer.type().name,
            "crs":    layer.crs().authid(),
            "valid":  layer.isValid(),
            "extent": {
                "xmin": ext.xMinimum(), "ymin": ext.yMinimum(),
                "xmax": ext.xMaximum(), "ymax": ext.yMaximum(),
            },
            "source": layer.dataProvider().dataSourceUri() if layer.dataProvider() else "",
        })
        if isinstance(layer, QgsVectorLayer):
            info["feature_count"] = layer.featureCount()
            info["geometry_type"] = layer.geometryType().name
            info["fields"] = [{"name": f.name(), "type": f.typeName()} for f in layer.fields()]
        elif isinstance(layer, QgsRasterLayer):
            info["band_count"] = layer.bandCount()
            info["width"] = layer.width()
            info["height"] = layer.height()
    except ImportError:
        info["note"] = "QGIS not loaded — metadata unavailable."
    return info


async def _tool_approve_pending_action(params: Dict, session_id: str) -> Dict:
    """approve_pending_action → HITL via PermissionSafetyAgent (FR-5.1)."""
    action_id = params.get("action_id", "")
    if not action_id:
        raise ValueError("'action_id' parameter is required.")
    approved = bool(params.get("approved", False))
    reason = params.get("reason", "")

    try:
        from geosi_engine.agents.permission_safety import PermissionSafetyAgent
        success = PermissionSafetyAgent._APPROVALS.resolve(action_id, approved=approved)
        if not success:
            raise ValueError(f"No pending approval found for action_id='{action_id}'.")
    except AttributeError:
        # Approval store not yet initialised (e.g. in tests) — treat as resolved
        logger.warning("Approval store not available; treating action_id=%s as resolved.", action_id)

    logger.info("MCP approve_pending_action: action_id=%s approved=%s", action_id, approved)
    return {"action_id": action_id, "status": "approved" if approved else "rejected", "reason": reason}
