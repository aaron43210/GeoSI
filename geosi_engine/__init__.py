# -*- coding: utf-8 -*-
"""
GeoSI Engine — The Shared Core of Geospatial Superintelligence

This package is the shared brain used by BOTH:
    1. geosi_plugin/  (QGIS desktop plugin)
    2. geosi_server/  (FastAPI REST API)

It provides:
    - models.py   — Data structures (Layer, ToolResult, AnalysisRequest)
    - base.py     — Abstract base class for all GIS tools
    - registry.py — Central registry that discovers and executes tools
    - parser.py   — Natural language to structured analysis request
    - agent.py    — LLM-powered multi-step planning
    - executor.py — Execute plans step-by-step
    - state.py    — Track layers, history, and intermediate results
    - tools/      — 130+ GIS tool implementations

Usage:
    from geosi_engine import GeoSI

    # Create the engine
    engine = GeoSI()

    # Run a natural language query
    result = engine.query("Buffer hospitals by 500 meters")

    # Or use tools directly
    result = engine.registry.execute_tool("buffer", layer="hospitals", distance=500)

Architecture:
    See FILE_CONNECTIONS.md in the project root for the full architecture map.

Author: Aaron R — Digital University Kerala (DUK)
Version: 1.0.0
"""

# ===========================================================================
# VERSION
# ===========================================================================

__version__ = "1.0.0"
__author__ = "Aaron R"
__project__ = "GeoSI — Geospatial Superintelligence"


# ===========================================================================
# PUBLIC API
# ===========================================================================

# Import the core classes that users need
# These are the main entry points for both the plugin and server

from geosi_engine.models import (
    Layer,
    ToolResult,
    ToolParameter,
    ToolSpec,
    AnalysisRequest,
    ExecutionPlan,
    ExecutionResult,
    ExecutionStatus,
    IntentType,
    GeometryType,
)

from geosi_engine.base import GISTool
from geosi_engine.registry import ToolRegistry
from geosi_engine.state import StateManager


# ===========================================================================
# CONVENIENCE CLASS — The main GeoSI engine
# ===========================================================================

class GeoSI:
    """
    Main entry point for the Geospatial Superintelligence engine.

    This class ties together:
        - ToolRegistry: knows what tools are available
        - StateManager: tracks loaded layers and execution history
        - Agent: plans multi-step workflows from natural language
        - Executor: runs each step and collects results

    Both the QGIS Plugin and FastAPI Server create ONE instance of this
    class and use it to handle all user requests.

    Usage:
        engine = GeoSI()
        result = engine.query("Find parks within 1km of schools")
        print(result["answer"])     # "Found 42 parks within 1km of schools"
        print(result["reasoning"])  # "Step 1: Buffer schools... Step 2: Intersect..."

    Attributes:
        registry: ToolRegistry with all registered GIS tools
        state: StateManager tracking loaded layers and execution history
        version: Current engine version string
    """

    def __init__(self):
        """
        Initialize the GeoSI engine.

        Creates the tool registry (which auto-registers all built-in tools)
        and a fresh state manager. The agent and executor are created lazily
        when the first query arrives.
        """
        # Create the tool registry — this auto-registers all built-in tools
        # Each tool knows its name, parameters, QGIS algorithm ID, and category
        self.registry = ToolRegistry()

        # Create a fresh state manager to track layers and history
        # This is shared across all operations in this session
        self.state = StateManager()

        # Version for API responses
        self.version = __version__

        # Import here to avoid circular imports during init
        from geosi_engine.agent import GeoSIAgent
        from geosi_engine.executor import ExecutionEngine

        # Create the core engine components
        self.agent = GeoSIAgent(self.registry)
        self.executor = ExecutionEngine(self.registry, self.state)

        # Print startup confirmation
        tool_count = len(self.registry.list_tools())
        print(f"GeoSI Engine v{self.version} initialized with {tool_count} tools")

    def query(self, question: str) -> dict:
        """
        Process a natural language GIS query.

        This is the main method that both the plugin and server call.
        It goes through the full pipeline:
            1. Parse the question to extract intent and entities
            2. Auto-load any .shp / .geojson / .gpkg file referenced by name
            3. Plan a sequence of tool steps (validating layers exist)
            4. Execute each step using the tool registry
            5. Return a human-readable answer

        Args:
            question: Natural language GIS query
                      Example: "Count all schools from Schools.shp"

        Returns:
            Dictionary with keys:
                - success (bool): Did the query complete without errors?
                - answer (str): Human-readable answer
                - reasoning (str): Step-by-step explanation
                - error (str or None): Error message if failed
                - results (dict): Raw output data (Layer objects, counts, etc.)
        """
        import re
        import os

        try:
            # ── Auto-load any file reference found in the query ───────────────
            # Handles queries like "Count all schools from Schools.shp"
            file_pattern = r'\b[\w\-]+\.(?:shp|geojson|gpkg|kml|tif|tiff)\b'
            for fname in re.findall(file_pattern, question, flags=re.IGNORECASE):
                layer_stem = os.path.splitext(fname)[0]
                # Skip if already in state (by stem or full name)
                if self.state.get_layer(layer_stem) or self.state.get_layer(fname):
                    continue
                # Search common project data directories
                base = os.path.dirname(os.path.abspath(__file__))
                search_dirs = [
                    os.getcwd(),
                    os.path.normpath(os.path.join(base, "..", "Data_06_2_2026")),
                    os.path.normpath(os.path.join(base, "..")),
                    os.path.expanduser(
                        "~/Downloads/GEO_SUPER_INTELLIGENCE-DEMO/Data_06_2_2026"
                    ),
                    os.path.expanduser("~/Downloads/GEO_SUPER_INTELLIGENCE-DEMO"),
                ]
                for search_dir in search_dirs:
                    candidate = os.path.normpath(os.path.join(search_dir, fname))
                    if os.path.exists(candidate):
                        from geosi_engine.tools.portable import LoadLayerTool
                        load_result = LoadLayerTool().execute(filepath=candidate)
                        if load_result.success and load_result.output:
                            self.state.add_layer(load_result.output)
                            print(f"GeoSI: auto-loaded '{fname}' from {candidate}")
                        break

            # Step 1: Parse the question into a structured request
            request = self.agent.parse(question, self.state)

            # Step 2: Create an execution plan (with layer validation)
            plan = self.agent.plan(request, self.state)

            # Step 3: Execute the plan step by step
            result = self.executor.run(plan)

            return {
                "success": result.success,
                "answer": result.answer,
                "reasoning": result.reasoning,
                "error": result.error,
                "results": result.results,
            }

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            return {
                "success": False,
                "answer": f"Error processing query: {str(e)}",
                "reasoning": f"The engine encountered an error during processing.\n{tb}",
                "error": str(e),
                "results": {},
            }
