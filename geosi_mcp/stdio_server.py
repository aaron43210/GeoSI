# -*- coding: utf-8 -*-
"""
GeoSI MCP — stdio transport entry point for Claude Desktop.

This module is the target of:
    fastmcp run /path/to/geosi_mcp/stdio_server.py

It exposes all 6 GeoSI MCP tools over JSON-RPC 2.0 on stdin/stdout,
using fastmcp's stdio transport so Claude Desktop can spawn it as a
local subprocess — no HTTP server required.

Claude Desktop config (claude_desktop_config.json):
    {
      "mcpServers": {
        "geosi": {
          "command": "fastmcp",
          "args": ["run", "/Users/aaronr/Desktop/GEOSI/geosi_mcp/stdio_server.py"]
        }
      }
    }

Security: GEOSI_MCP_TOKEN is checked the same way as the HTTP transport.
In dev mode (no token set) it runs unrestricted — set the env var for
any shared or production deployment.

Streamable HTTP: set GEOSI_MCP_TRANSPORT=streamable-http to run on
0.0.0.0:${GEOSI_MCP_PORT:-8001} instead of stdio.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional

logger = logging.getLogger("geosi_mcp.stdio_server")

# ── Try to import fastmcp; fall back to a minimal hand-rolled stdio loop ──

import importlib.util

_HAS_FASTMCP = importlib.util.find_spec("fastmcp") is not None


# ── Tool definitions reused from server.py ───────────────────────────────

def _get_tools() -> List[Dict[str, Any]]:
    """Return the MCP tool list in fastmcp-compatible format."""
    from geosi_mcp.server import _TOOLS
    return [
        {
            "name": t.name,
            "description": t.description,
            "inputSchema": {
                "type": "object",
                "properties": {
                    p.name: {"type": p.type, "description": p.description}
                    for p in t.parameters
                },
                "required": [p.name for p in t.parameters if p.required],
            },
        }
        for t in _TOOLS
    ]


async def _dispatch(tool_name: str, params: Dict[str, Any]) -> Any:
    """Route a tool call to the matching async handler in server.py."""
    from geosi_mcp.server import _dispatch_tool
    # Use the bearer token as a short session ID (dev: empty)
    token = os.environ.get("GEOSI_MCP_TOKEN", "")[:16] or "stdio-session"
    return await _dispatch_tool(tool_name, params, session_id=token)


# ── fastmcp path ─────────────────────────────────────────────────────────

def _run_fastmcp() -> None:
    """Launch via fastmcp's native transport."""
    import fastmcp  # type: ignore

    transport = os.environ.get("GEOSI_MCP_TRANSPORT", "stdio")
    host = os.environ.get("GEOSI_MCP_HOST", "127.0.0.1")  # nosec B104 — override via env for production
    port = int(os.environ.get("GEOSI_MCP_PORT", "8001"))

    mcp = fastmcp.FastMCP("GeoSI")

    # Dynamically register each tool from the server catalog
    from geosi_mcp.server import _TOOLS

    for tool_def in _TOOLS:
        _register_fastmcp_tool(mcp, tool_def)

    if transport == "streamable-http":
        logger.info("GeoSI MCP starting streamable-HTTP on %s:%s", host, port)
        mcp.run(transport="streamable-http", host=host, port=port)
    else:
        logger.info("GeoSI MCP starting stdio transport")
        mcp.run()


def _register_fastmcp_tool(mcp: Any, tool_def: Any) -> None:
    """Wrap one MCPTool definition as a fastmcp async tool."""
    name = tool_def.name

    async def _handler(**kwargs: Any) -> str:
        try:
            result = await _dispatch(name, kwargs)
            return json.dumps(result, ensure_ascii=False, default=str)
        except Exception as exc:
            return json.dumps({"error": str(exc)})

    _handler.__name__ = name
    _handler.__doc__ = tool_def.description
    mcp.tool(name=name, description=tool_def.description)(_handler)


# ── Minimal hand-rolled stdio path (no fastmcp dependency) ───────────────

def _run_stdio_fallback() -> None:
    """
    Minimal JSON-RPC 2.0 stdio loop used when fastmcp is not installed.
    Reads newline-delimited JSON from stdin, writes responses to stdout.
    Compatible with the MCP stdio protocol Claude Desktop uses.
    """
    logger.info("GeoSI MCP fallback stdio loop (fastmcp not installed)")

    async def _handle_one(line: str) -> Optional[str]:
        try:
            req = json.loads(line)
        except json.JSONDecodeError as exc:
            return json.dumps({
                "jsonrpc": "2.0", "id": None,
                "error": {"code": -32700, "message": f"Parse error: {exc}"},
            })

        req_id = req.get("id")
        method = req.get("method", "")

        # MCP initialization handshake
        if method == "initialize":
            return json.dumps({
                "jsonrpc": "2.0", "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "geosi-mcp", "version": "2.0.0"},
                },
            })

        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0", "id": req_id,
                "result": {"tools": _get_tools()},
            })

        if method == "tools/call":
            tool_name = req.get("params", {}).get("name", "")
            arguments  = req.get("params", {}).get("arguments", {})
            try:
                result = await _dispatch(tool_name, arguments)
                return json.dumps({
                    "jsonrpc": "2.0", "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(result, default=str)}],
                        "isError": False,
                    },
                })
            except Exception as exc:
                return json.dumps({
                    "jsonrpc": "2.0", "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": str(exc)}],
                        "isError": True,
                    },
                })

        # notifications (initialized, cancelled) — no response needed
        if method.startswith("notifications/"):
            return None

        return json.dumps({
            "jsonrpc": "2.0", "id": req_id,
            "error": {"code": -32601, "message": f"Method not found: {method!r}"},
        })

    async def _loop() -> None:
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        while True:
            try:
                line_bytes = await reader.readline()
            except Exception:
                break
            if not line_bytes:
                break
            line = line_bytes.decode("utf-8").strip()
            if not line:
                continue
            response = await _handle_one(line)
            if response is not None:
                sys.stdout.write(response + "\n")
                sys.stdout.flush()

    asyncio.run(_loop())


# ── Entry point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    # Add repo root to path so geosi_* packages are importable
    _repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _repo_root not in sys.path:
        sys.path.insert(0, _repo_root)

    from geosi_mcp.auth import verify_mcp_token
    # In production, a missing token causes verify_mcp_token to return False.
    # For stdio, we do a one-time startup check and warn; individual tool calls
    # still gate through _dispatch → server.py auth if needed.
    if not verify_mcp_token(os.environ.get("GEOSI_MCP_TOKEN", "")):
        env = os.environ.get("GEOSI_ENV", "development").lower()
        if env == "production":
            logger.error("GEOSI_MCP_TOKEN not set in production — refusing to start.")
            sys.exit(1)

    if _HAS_FASTMCP:
        _run_fastmcp()
    else:
        _run_stdio_fallback()
