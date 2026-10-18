# -*- coding: utf-8 -*-
"""
GeoSI Knowledge — Workflow Memory
═══════════════════════════════════════════════════════════════════

Remembers past workflows and their outcomes. Stores workflow
examples in Qdrant for semantic retrieval and provides the
planning agent with similar past workflows.

Data flow:
    Execution completes → store_workflow() → Qdrant (gis_workflows)
    New query arrives → find_similar() → matching past workflows
"""

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

logger = logging.getLogger("geosi_knowledge.workflow_memory")


@dataclass
class WorkflowExample:
    """
    A recorded or built-in workflow example.

    Attributes:
        name: Workflow identifier (e.g. "ndvi_calculation")
        description: Human-readable description
        user_query: Example query that triggers this workflow
        tool_sequence: Ordered list of tool names used
        plan_json: Serialized execution plan (optional)
        success: Whether this workflow succeeded
        execution_time_ms: How long the workflow took
        tags: Search tags
        output_description: What the workflow produces
        created_at: When this workflow was recorded
    """
    name: str = ""
    description: str = ""
    user_query: str = ""
    tool_sequence: List[str] = field(default_factory=list)
    plan_json: Optional[Dict] = None
    success: bool = True
    execution_time_ms: float = 0.0
    tags: List[str] = field(default_factory=list)
    output_description: str = ""
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def __repr__(self):
        tools = " → ".join(self.tool_sequence) if self.tool_sequence else "N/A"
        status = "✅" if self.success else "❌"
        return f"WorkflowExample({status} {self.name}: {tools})"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict for Qdrant payload."""
        return {
            "name": self.name,
            "description": self.description,
            "user_query": self.user_query,
            "tool_sequence": self.tool_sequence,
            "success": self.success,
            "execution_time_ms": self.execution_time_ms,
            "tags": self.tags,
            "output_description": self.output_description,
            "created_at": self.created_at,
        }

    def to_searchable_text(self) -> str:
        """Build a text representation for embedding."""
        parts = [
            self.name.replace("_", " "),
            self.description,
            self.user_query,
            " ".join(self.tool_sequence),
            " ".join(self.tags),
            self.output_description,
        ]
        return " | ".join(part for part in parts if part)


class WorkflowMemory:
    """
    Remembers past workflows and their outcomes.

    Uses Qdrant's 'gis_workflows' collection for semantic retrieval
    and maintains an in-memory cache of recent workflows.

    Usage:
        memory = WorkflowMemory(rag_service)
        memory.store_workflow(query, plan, result, success=True)
        similar = memory.find_similar("Calculate NDVI", limit=3)
    """

    def __init__(self, rag_service=None):
        """
        Args:
            rag_service: RAGService for Qdrant access.
                         If None, operates in memory-only mode.
        """
        self.rag = rag_service
        self._cache: List[WorkflowExample] = []
        self._max_cache = 100

        # Load built-in workflows on first init
        self._load_builtins()

    def store_workflow(
        self,
        query: str,
        plan: Any,
        result: Any,
        success: bool = True,
    ) -> Optional[WorkflowExample]:
        """
        Record a completed workflow execution.

        Args:
            query: Original user query
            plan: ExecutionPlan object
            result: ExecutionResult object
            success: Whether execution succeeded

        Returns:
            WorkflowExample that was stored, or None on failure.
        """
        # Extract tool sequence from plan
        tool_sequence = []
        plan_data = None
        if plan and hasattr(plan, "steps"):
            tool_sequence = [s.tool_name for s in plan.steps]
            plan_data = {
                "plan_id": getattr(plan, "plan_id", ""),
                "reasoning": getattr(plan, "reasoning", ""),
                "steps": [
                    {
                        "step_id": s.step_id,
                        "tool_name": s.tool_name,
                        "description": s.description,
                    }
                    for s in plan.steps
                ],
            }

        # Extract execution time
        exec_time = getattr(result, "total_duration_ms", 0.0) if result else 0.0

        # Derive workflow name from query
        name = self._derive_name(query, tool_sequence)

        workflow = WorkflowExample(
            name=name,
            description=f"Auto-recorded: {query[:100]}",
            user_query=query,
            tool_sequence=tool_sequence,
            plan_json=plan_data,
            success=success,
            execution_time_ms=exec_time,
            tags=self._extract_tags(query, tool_sequence),
        )

        # Store in cache
        self._cache.append(workflow)
        if len(self._cache) > self._max_cache:
            self._cache = self._cache[-self._max_cache:]

        # Store in Qdrant if RAG service available
        if self.rag and self.rag.available:
            try:
                self.rag.ingest_workflow(workflow.to_dict())
                logger.info(f"Stored workflow: {workflow.name}")
            except Exception as e:
                logger.warning(f"Failed to store workflow in Qdrant: {e}")

        return workflow

    def find_similar(
        self,
        query: str,
        limit: int = 5,
    ) -> List[WorkflowExample]:
        """
        Find similar past workflows using semantic search.

        Strategy:
            1. Search Qdrant gis_workflows collection
            2. Also check in-memory cache for recent workflows
            3. Merge and deduplicate results

        Args:
            query: User's current query
            limit: Maximum results

        Returns:
            List of similar WorkflowExample objects.
        """
        results = []

        # 1. Search Qdrant
        if self.rag and self.rag.available:
            try:
                rag_results = self.rag.retriever.hybrid_search(
                    query=query,
                    collection="gis_workflows",
                    limit=limit,
                )
                for r in rag_results:
                    wf = WorkflowExample(
                        name=r.metadata.get("name", ""),
                        description=r.metadata.get("description", ""),
                        user_query=r.metadata.get("user_query", ""),
                        tool_sequence=r.metadata.get("tool_sequence", []),
                        success=r.metadata.get("success", True),
                        tags=r.metadata.get("tags", []),
                    )
                    results.append(wf)
            except Exception as e:
                logger.debug(f"Qdrant workflow search failed: {e}")

        # 2. Search in-memory cache
        cache_matches = self._search_cache(query, limit)
        results.extend(cache_matches)

        # 3. Deduplicate by name
        seen = set()
        unique = []
        for wf in results:
            if wf.name not in seen:
                seen.add(wf.name)
                unique.append(wf)

        return unique[:limit]

    def get_successful_workflows(
        self,
        operation: str,
        limit: int = 3,
    ) -> List[WorkflowExample]:
        """
        Get workflows that succeeded for a given operation type.

        Searches both cache and Qdrant for successful workflows
        matching the operation.
        """
        matching = [
            wf for wf in self._cache
            if wf.success and (
                operation in wf.tool_sequence
                or operation.lower() in wf.name.lower()
                or operation.lower() in wf.user_query.lower()
            )
        ]
        matching.sort(key=lambda w: w.execution_time_ms)
        return matching[:limit]

    def list_workflows(self) -> List[str]:
        """List all workflow names in cache."""
        return [wf.name for wf in self._cache]

    def get_workflow(self, name: str) -> Optional[WorkflowExample]:
        """Get a specific workflow by name."""
        for wf in self._cache:
            if wf.name == name:
                return wf
        return None

    # ── Private helpers ────────────────────────────────────────────────

    def _search_cache(self, query: str, limit: int) -> List[WorkflowExample]:
        """Simple keyword search over cached workflows."""
        query_lower = query.lower()
        scored = []
        for wf in self._cache:
            score = 0
            searchable = wf.to_searchable_text().lower()
            # Count keyword matches
            for word in query_lower.split():
                if len(word) > 2 and word in searchable:
                    score += 1
            if score > 0:
                scored.append((score, wf))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [wf for _, wf in scored[:limit]]

    @staticmethod
    def _derive_name(query: str, tools: List[str]) -> str:
        """Generate a workflow name from query and tools."""
        import re
        # Use first tool and key words from query
        key_words = re.findall(r"\b[a-z]{3,}\b", query.lower())
        # Filter out common words
        stops = {"the", "from", "with", "for", "and", "this", "that", "using"}
        key_words = [w for w in key_words if w not in stops][:3]
        tool_part = tools[0].replace("native_", "") if tools else "unknown"
        name_parts = key_words + [tool_part]
        return "_".join(name_parts)

    @staticmethod
    def _extract_tags(query: str, tools: List[str]) -> List[str]:
        """Extract search tags from query and tool list."""
        import re
        tags = set()
        # Add tool names (without prefixes)
        for tool in tools:
            tags.add(tool.replace("native_", "").replace("gdal_", ""))
        # Add key GIS terms from query
        gis_terms = {
            "ndvi", "ndwi", "ndbi", "slope", "aspect", "hillshade",
            "buffer", "intersect", "clip", "dissolve", "contour",
            "dem", "sentinel", "landsat", "watershed", "classification",
            "raster", "vector", "reproject", "merge", "mosaic",
        }
        for word in re.findall(r"\b\w+\b", query.lower()):
            if word in gis_terms:
                tags.add(word)
        return list(tags)

    def _load_builtins(self):
        """Load built-in workflow templates."""
        try:
            from geosi_knowledge.builtin_workflows import get_builtin_workflows
            builtins = get_builtin_workflows()
            self._cache.extend(builtins)
            logger.info(f"Loaded {len(builtins)} built-in workflow templates")
        except Exception as e:
            logger.debug(f"Could not load built-in workflows: {e}")
