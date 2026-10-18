# -*- coding: utf-8 -*-
"""
GeoSI Engine — Tool Registry (v2: Dynamic Registration)
═══════════════════════════════════════════════════════════════════

The ToolRegistry is a hash-table-backed catalog of all available GIS
tools. In v2, tools are NOT hardcoded — they are dynamically registered
at plugin startup by auto_discover_qgis_tools() in qgis_bridge.py.

Architecture
────────────
    ToolRegistry
    ├── _tools: Dict[str, GISTool]      ← O(1) lookup by name
    ├── _alias_index: Dict[str, str]    ← O(1) alias → canonical name
    └── _category_index: Dict[str, List] ← O(1) category → tool list

    Tool Registration Flow:
        Plugin startup → qgis_bridge.install() → auto_discover_qgis_tools()
        → For each QGIS algorithm:
            BackendTool(...) → registry.register_tool(tool) → stored in _tools

Data Structures & Complexity
────────────────────────────
    register_tool()   : O(A) where A = number of aliases generated
    get_tool()        : O(1) amortized (dict lookup + alias fallback)
    execute_tool()    : O(1) lookup + O(tool) execution
    list_tools()      : O(N) where N = total tools
    search_tools()    : O(N * K) where K = search term length
    discover_tools()  : O(M) where M = portable tool modules

Thread Safety
─────────────
    The registry itself is NOT thread-safe. All registration happens
    on the main thread during plugin initialization. Reads (get_tool,
    list_tools) can happen from any thread after initialization completes.
"""

import logging
import pkgutil
import importlib
from typing import Dict, List, Optional, Any

from geosi_engine.models import ToolSpec, ToolResult

logger = logging.getLogger("geosi_engine.registry")


class ToolRegistry:
    """
    Central catalog of all registered GIS tools.

    Supports three lookup strategies (all O(1) amortized):
        1. Exact name match:  get_tool("native_buffer")
        2. Alias match:       get_tool("buffer") → resolves to "native_buffer"
        3. Category filter:   get_tools_by_category("vector")
    """

    def __init__(self):
        # ── Primary storage: name → GISTool (hash table, O(1) lookup) ──
        self._tools: Dict[str, Any] = {}

        # ── Alias index: short_name → canonical_name ────────────────────
        # Allows the LLM to use "buffer" instead of "native_buffer"
        # Built automatically during register_tool()
        self._alias_index: Dict[str, str] = {}

        # ── Category index: category → [tool_name, ...] ────────────────
        # Pre-computed for O(1) category filtering
        self._category_index: Dict[str, List[str]] = {}

    # ── Registration ─────────────────────────────────────────────────────

    def register_tool(self, tool: Any) -> None:
        """
        Register a GISTool instance in the catalog.

        This method:
            1. Stores the tool by its canonical name in _tools
            2. Creates aliases for fuzzy/short matching in _alias_index
            3. Updates the _category_index for fast category filtering

        Args:
            tool: A GISTool instance (PortableTool or BackendTool)

        Complexity: O(A) where A = number of aliases generated (~5 per tool)
        """
        spec = tool.spec()
        name = spec.name

        # ── Store in primary hash table ────────────────────────────────
        self._tools[name] = tool

        # ── Build alias index for fuzzy matching ───────────────────────
        # "native_buffer" → aliases: "buffer", "native buffer", "Buffer"
        self._alias_index[name] = name  # self-reference
        self._alias_index[name.lower()] = name

        # Short alias: strip provider prefix ("native_buffer" → "buffer")
        if "_" in name:
            parts = name.split("_", 1)
            if len(parts) == 2 and parts[0] in ("native", "qgis", "gdal", "saga", "grass"):
                short = parts[1]
                # Only create alias if no collision with existing tool
                if short not in self._alias_index:
                    self._alias_index[short] = name
                    self._alias_index[short.lower()] = name

        # Display name alias
        if spec.display_name:
            dn_lower = spec.display_name.lower().replace(" ", "_")
            if dn_lower not in self._alias_index:
                self._alias_index[dn_lower] = name

        # ── Update category index ──────────────────────────────────────
        cat = spec.category or "general"
        if cat not in self._category_index:
            self._category_index[cat] = []
        self._category_index[cat].append(name)

    # ── Lookup ───────────────────────────────────────────────────────────

    def get_tool(self, name: str) -> Optional[Any]:
        """
        Find a tool by exact name or alias.

        Lookup strategy (stops at first hit):
            1. Exact match in _tools            → O(1)
            2. Lowercase match in _tools        → O(1)
            3. Alias resolution via _alias_index → O(1)
            4. Fuzzy alias with lowercase        → O(1)

        Args:
            name: Tool name or alias (e.g. "buffer", "native_buffer")

        Returns:
            GISTool instance or None
        """
        # 1. Exact match
        tool = self._tools.get(name)
        if tool is not None:
            return tool

        # 2. Lowercase match
        tool = self._tools.get(name.lower())
        if tool is not None:
            return tool

        # 3. Alias resolution
        canonical = self._alias_index.get(name)
        if canonical:
            return self._tools.get(canonical)

        # 4. Fuzzy alias with lowercase
        canonical = self._alias_index.get(name.lower())
        if canonical:
            return self._tools.get(canonical)

        return None

    def execute_tool(self, name: str, **kwargs) -> ToolResult:
        """
        Look up and execute a tool by name.

        Complexity: O(1) lookup + O(tool execution)
        """
        tool = self.get_tool(name)
        if tool is None:
            return ToolResult(
                success=False,
                error=f"Tool '{name}' not found in registry.",
                message=f"Unknown tool: {name}",
            )
        return tool.safe_execute(**kwargs)

    # ── Query ────────────────────────────────────────────────────────────

    def list_tools(self) -> List[ToolSpec]:
        """
        Return ToolSpec for every registered tool.
        Complexity: O(N) where N = total tools
        """
        return [t.spec() for t in self._tools.values()]

    def list_tool_names(self) -> List[str]:
        """Return sorted list of all tool names. O(N log N)."""
        return sorted(self._tools.keys())

    def get_tools_by_category(self, category: str) -> List[Any]:
        """
        Get all tools in a category using the pre-built index.
        Complexity: O(C) where C = tools in the category
        """
        names = self._category_index.get(category, [])
        return [self._tools[n] for n in names if n in self._tools]

    def tool_count(self) -> int:
        """Number of registered tools. O(1)."""
        return len(self._tools)

    def search_tools(self, query: str) -> List[ToolSpec]:
        """
        Search tools by name, description, or tags.

        Algorithm: Linear scan with substring matching.
        Complexity: O(N * K) where N = tools, K = query length

        For the typical case (~1000 tools, short query), this runs in <1ms.
        A trie or inverted index would be faster for very large registries,
        but the constant factor of Python dict iteration dominates at this scale.
        """
        query_lower = query.lower()
        results = []
        for tool in self._tools.values():
            spec = tool.spec()
            # Check name, display_name, description, and tags
            if (
                query_lower in spec.name.lower()
                or query_lower in spec.display_name.lower()
                or query_lower in spec.description.lower()
                or any(query_lower in tag.lower() for tag in spec.tags)
            ):
                results.append(spec)
        return results

    # ── Auto-discovery (portable tools only) ─────────────────────────────

    def discover_portable_tools(self) -> int:
        """
        Walk the geosi_engine.tools package and register PortableTool
        subclasses. This ONLY discovers portable tools — QGIS tools
        are discovered by auto_discover_qgis_tools() in qgis_bridge.py.

        Algorithm:
            1. pkgutil.iter_modules() to find tool modules → O(M) where M = modules
            2. For each module, inspect classes → O(C) where C = classes per module
            3. Register GISTool subclasses → O(1) per tool

        Returns:
            Number of portable tools discovered
        """
        from geosi_engine.base import GISTool
        import geosi_engine.tools as tools_pkg

        count = 0
        for finder, module_name, is_pkg in pkgutil.iter_modules(tools_pkg.__path__):
            try:
                module = importlib.import_module(
                    f"geosi_engine.tools.{module_name}"
                )
                for attr_name in dir(module):
                    obj = getattr(module, attr_name)
                    if (
                        isinstance(obj, type)
                        and issubclass(obj, GISTool)
                        and obj is not GISTool
                        and not getattr(obj, "__abstractmethods__", None)
                    ):
                        try:
                            instance = obj()
                            self.register_tool(instance)
                            count += 1
                        except Exception as e:
                            logger.debug(f"Skip {attr_name}: {e}")
            except Exception as e:
                logger.debug(f"Skip module {module_name}: {e}")

        logger.info(f"Discovered {count} portable tool(s)")
        return count

    def __len__(self) -> int:
        return len(self._tools)

    def __contains__(self, name: str) -> bool:
        return self.get_tool(name) is not None

    def __repr__(self) -> str:
        return f"ToolRegistry({len(self._tools)} tools)"
