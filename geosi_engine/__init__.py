# -*- coding: utf-8 -*-
"""
GeoSI Engine — Facade Class (v2: Dynamic Tool Discovery + Knowledge Layer)
═════════════════════════════════════════════════════════════════

This is the single entry point for all GeoSI interactions:

    from geosi_engine import GeoSI
    engine = GeoSI(enable_knowledge=True)
    result = engine.run("Buffer hospitals by 500m")

The GeoSI class wires together:
    - ToolRegistry    → catalog of all available tools
    - GeoSIAgent      → LLM-powered planner
    - ExecutionEngine  → step-by-step executor
    - StateManager     → workspace layer tracking
    - ConversationManager → multi-turn dialogue memory
    - KnowledgeManager → RAG + memory layer (Phase 2)
    - Database/Repos   → PostGIS persistence (Phase 2)

v2 Key Difference:
    The registry starts EMPTY. Tools are injected externally by the
    QGIS plugin via auto_discover_qgis_tools(). The only tools
    registered at init are portable tools (GeoPandas loaders).
"""

import logging

from geosi_engine.registry import ToolRegistry
from geosi_engine.state import StateManager
from geosi_engine.agent import GeoSIAgent
from geosi_engine.executor import ExecutionEngine
from geosi_engine.conversation import ConversationManager
from geosi_engine.models import (
    AnalysisRequest,
    ExecutionPlan,
    ExecutionResult,
    ExecutionStatus,
    IntentType,
    Layer,
    ToolSpec,
    ToolParameter,
    ToolResult,
    ToolStep,
    StepLog,
)

logger = logging.getLogger("geosi_engine")

# ── Public API ─────────────────────────────────────────────────────────
__all__ = [
    "GeoSI",
    "ToolRegistry",
    "StateManager",
    "GeoSIAgent",
    "ExecutionEngine",
    "ConversationManager",
    # Data models
    "AnalysisRequest",
    "ExecutionPlan",
    "ExecutionResult",
    "ExecutionStatus",
    "IntentType",
    "Layer",
    "ToolSpec",
    "ToolParameter",
    "ToolResult",
    "ToolStep",
    "StepLog",
]


class GeoSI:
    """
    GeoSI v2 — Geospatial Superintelligence Engine.

    Facade that orchestrates the full pipeline:
        User Query → Knowledge → Parse → Plan → Execute → Learn → Result

    Usage (inside QGIS plugin):
        engine = GeoSI(enable_knowledge=True)
        # Plugin bridge injects QGIS tools:
        from geosi_plugin.qgis_bridge import install
        install(engine.registry)
        # Now run queries:
        result = engine.run("Buffer hospitals by 500m")

    Usage (standalone, portable tools only):
        engine = GeoSI()
        result = engine.run("Count features in schools.shp")
    """

    def __init__(self, use_llm: bool = True, enable_knowledge: bool = False):
        # ── Initialize conversation memory ─────────────────────────────
        self.conversation = ConversationManager(
            system_prompt=(
                "You are GeoSI, an advanced geospatial AI assistant. "
                "Help users analyze spatial data by planning and executing "
                "GIS workflows."
            )
        )

        # ── Initialize the tool registry (starts empty in v2) ──────────
        self.registry = ToolRegistry()

        # ── Discover portable tools (GeoPandas/Rasterio loaders) ───────
        # These work without QGIS and are always available
        try:
            self.registry.discover_portable_tools()
        except Exception:
            logger.debug("suppressed exception", exc_info=True)

        # ── Register domain agents as tools (PRD "any GIS task") ───────
        # Exposes Code Generation / Report / Research / Remote Sensing /
        # Machine Learning / Geology as first-class registry entries so the
        # single Supervisor pipeline can plan→validate→permission→execute
        # them like any other tool. Non-fatal if unavailable.
        try:
            from geosi_engine.tools.domain_tools import discover_domain_tools
            discover_domain_tools(self, self.registry)
        except Exception as exc:
            logger.debug("Domain tool registration skipped: %s", exc)

        # ── Initialize workspace state ─────────────────────────────────
        self.state = StateManager()

        # ── Phase 2: Knowledge Layer (optional) ───────────────────────
        self.knowledge = None
        self.data = None
        self.rag = None

        if enable_knowledge:
            self._init_knowledge_layer()

        # ── Initialize the LLM-powered planner ─────────────────────────
        self.agent = GeoSIAgent(
            registry=self.registry,
            use_llm=use_llm,
            conversation=self.conversation,
            knowledge=self.knowledge,
        )

        # ── Initialize the step-by-step executor ───────────────────────
        self.executor = ExecutionEngine(
            registry=self.registry,
            state=self.state,
        )
        from geosi_engine.agent_loop import AgentLoop
        self.loop = AgentLoop(self)

    def _init_knowledge_layer(self):
        """
        Initialize the Phase 2 knowledge and data layers.

        Components initialized:
            - KnowledgeManager (RAG + memory)
            - Database + repositories (PostGIS)

        Failures are non-fatal — the engine works without them.
        """
        # ── Initialize Knowledge Manager ──────────────────────────────
        try:
            from geosi_knowledge import KnowledgeManager
            self.knowledge = KnowledgeManager()
            logger.info(f"Knowledge layer initialized: {self.knowledge}")
        except Exception as e:
            logger.warning(f"Knowledge layer unavailable: {e}")

        # ── Initialize PostGIS Data Layer ──────────────────────────────
        try:
            from geosi_data import (
                Database,
                PostGISManager,
                LayerRepository,
                ProjectRepository,
                MetadataRepository,
            )

            db = Database()
            if db.available:
                db.init_db()
                self.data = {
                    "database": db,
                    "postgis": PostGISManager(db),
                    "layers": LayerRepository(db),
                    "projects": ProjectRepository(db),
                    "metadata": MetadataRepository(db),
                }
                logger.info("PostGIS data layer initialized")
            else:
                logger.info("PostGIS unavailable — running without persistence")
        except Exception as e:
            logger.warning(f"Data layer unavailable: {e}")

    def run(self, query: str) -> ExecutionResult:
        """
        Run a complete GIS query from natural language.

        Pipeline:
            1. Parse: NL → AnalysisRequest (extract intent + entities)
            2. Plan:  AnalysisRequest → ExecutionPlan (select tools)
            3. Execute: ExecutionPlan → ExecutionResult (run tools)
            4. Learn: Record execution in knowledge layer
            5. Persist: Store results in PostGIS

        Args:
            query: Natural language GIS query

        Returns:
            ExecutionResult with answer, reasoning, and output layers
        """
        # 1-3. Parse → plan → execute → verify, re-planning on problems
        result = self.loop.run(query)
        plan = self.loop.last_plan

        # 4. Track in conversation memory
        self.conversation.add_user_message(query)
        self.conversation.add_assistant_message(result.answer)

        # 5. Phase 2: Learn from execution
        if self.knowledge:
            try:
                self.knowledge.learn_from_execution(query, plan, result)
            except Exception as e:
                logger.debug(f"Knowledge learning failed: {e}")

        # 6. Phase 2: Persist to PostGIS
        if self.data:
            try:
                self.data["metadata"].store_execution_result(query, plan, result)
            except Exception as e:
                logger.debug(f"PostGIS persistence failed: {e}")

        return result

    def resume(self, action_id: str, approved: bool) -> ExecutionResult:
        """Continue a run that paused for approval (see SupervisorAgent.resume)."""
        result = self.loop.resume(action_id, approved)
        if self.knowledge and result.success:
            try:
                self.knowledge.learn_from_execution("(resumed)", self.loop.last_plan, result)
            except Exception as e:
                logger.debug(f"Knowledge learning failed: {e}")
        return result

    def shutdown(self) -> None:
        """Release session resources (called when the session is evicted)."""
        self.loop.paused.clear()
        self.state.clear()

    # ── Phase 2: Convenience methods ───────────────────────────────

    def ingest_documents(self, directory: str, collection: str = "gis_docs") -> int:
        """
        Ingest documentation into the knowledge base.

        Args:
            directory: Path to directory with documents
            collection: Target Qdrant collection

        Returns:
            Number of chunks ingested
        """
        if self.knowledge:
            return self.knowledge.ingest_documents(directory, collection)
        logger.warning("Knowledge layer not enabled")
        return 0

    def get_workflow_history(self):
        """Get past workflow history from PostGIS."""
        if self.data:
            return self.data["metadata"].get_workflow_history()
        return []

    def get_knowledge_stats(self):
        """Get knowledge base statistics."""
        if self.knowledge:
            return self.knowledge.get_statistics()
        return {}
