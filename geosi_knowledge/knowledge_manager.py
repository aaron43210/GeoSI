# -*- coding: utf-8 -*-
"""
GeoSI Knowledge — Knowledge Manager
═══════════════════════════════════════════════════════════════════

Central orchestrator for all GIS knowledge retrieval.
Sits between the Parser and the Planning Agent in the pipeline:

    User Query → Parser → KnowledgeManager → Planning Agent

Composes:
    - RAGService (Qdrant document retrieval)
    - WorkflowMemory (past workflow examples)
    - QueryMemory (user query patterns)
    - FeedbackMemory (execution success/failure learning)

Main method:
    retrieve_context(query) → KnowledgeContext
        Returns assembled knowledge for the planning agent.
"""

import logging
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

from geosi_knowledge.workflow_memory import WorkflowMemory, WorkflowExample
from geosi_knowledge.query_memory import QueryMemory, QueryPattern
from geosi_knowledge.feedback_memory import FeedbackMemory, FeedbackSignal

logger = logging.getLogger("geosi_knowledge.knowledge_manager")


@dataclass
class KnowledgeContext:
    """
    Assembled knowledge context for the planning agent.

    This is what KnowledgeManager returns to the agent before
    workflow generation — giving it contextual GIS knowledge.

    Attributes:
        relevant_docs: Matching GIS documentation snippets
        similar_workflows: Past workflow templates
        query_patterns: Recurring user patterns
        feedback_signals: What worked/failed before
        context_prompt: Assembled prompt section for the LLM
        tool_warnings: Warnings about unreliable tools
        user_preferences: Inferred user preferences
    """
    relevant_docs: List[Any] = field(default_factory=list)
    similar_workflows: List[WorkflowExample] = field(default_factory=list)
    query_patterns: List[QueryPattern] = field(default_factory=list)
    feedback_signals: List[FeedbackSignal] = field(default_factory=list)
    context_prompt: str = ""
    tool_warnings: List[str] = field(default_factory=list)
    user_preferences: Dict[str, Any] = field(default_factory=dict)

    def has_knowledge(self) -> bool:
        """Check if any knowledge was retrieved."""
        return bool(
            self.relevant_docs
            or self.similar_workflows
            or self.query_patterns
            or self.feedback_signals
        )

    def __repr__(self):
        return (
            f"KnowledgeContext("
            f"docs={len(self.relevant_docs)}, "
            f"workflows={len(self.similar_workflows)}, "
            f"patterns={len(self.query_patterns)}, "
            f"feedback={len(self.feedback_signals)}, "
            f"prompt_len={len(self.context_prompt)})"
        )


class KnowledgeManager:
    """
    Central orchestrator for all GIS knowledge retrieval.

    Usage:
        km = KnowledgeManager()
        context = km.retrieve_context("Calculate NDVI from Sentinel imagery")
        # context.context_prompt → inject into LLM prompt
        # context.similar_workflows → use for rule-based planning
    """

    def __init__(
        self,
        rag_service=None,
        workflow_memory: Optional[WorkflowMemory] = None,
        query_memory: Optional[QueryMemory] = None,
        feedback_memory: Optional[FeedbackMemory] = None,
    ):
        """
        Initialize the knowledge manager.

        If components are not provided, creates them with defaults.

        Args:
            rag_service: RAGService for document retrieval (optional)
            workflow_memory: WorkflowMemory instance (optional)
            query_memory: QueryMemory instance (optional)
            feedback_memory: FeedbackMemory instance (optional)
        """
        # Initialize RAG service (lazy — only if available)
        self.rag = rag_service
        self._rag_initialized = rag_service is not None

        # Initialize memory components
        self.workflow_memory = workflow_memory or WorkflowMemory(
            rag_service=rag_service
        )
        self.query_memory = query_memory or QueryMemory()
        self.feedback_memory = feedback_memory or FeedbackMemory()

        logger.info(
            f"KnowledgeManager initialized: "
            f"RAG={'ready' if self.rag and self.rag.available else 'unavailable'}, "
            f"workflows={len(self.workflow_memory._cache)}, "
            f"queries={len(self.query_memory)}, "
            f"feedback={len(self.feedback_memory)}"
        )

    def _ensure_rag(self):
        """Lazy-initialize RAG service if not done yet."""
        if not self._rag_initialized:
            try:
                from geosi_rag.rag_service import RAGService
                self.rag = RAGService()
                self.workflow_memory.rag = self.rag
                self._rag_initialized = True
                logger.info("RAG service lazy-initialized")
            except Exception as e:
                logger.debug(f"RAG service unavailable: {e}")
                self._rag_initialized = True  # Don't retry

    def ensure_rag(self):
        """
        Public entrypoint to force lazy RAG initialization.

        Callers that touch ``self.rag`` directly (e.g. the /rag/* routes)
        must call this first, otherwise a cold session reports the RAG
        service as unavailable until some other method triggers lazy init.
        """
        self._ensure_rag()
        return self.rag

    def retrieve_context(
        self,
        query: str,
        doc_limit: int = 5,
        workflow_limit: int = 5,
        feedback_limit: int = 3,
    ) -> KnowledgeContext:
        """
        Retrieve all relevant knowledge for a query.

        This is the main method — called by the planning agent
        before workflow generation.

        Pipeline:
            1. Search GIS documentation via RAG (Qdrant)
            2. Find similar past workflows
            3. Check query patterns
            4. Get feedback signals
            5. Assemble context prompt

        Args:
            query: User's natural language query
            doc_limit: Max documentation results
            workflow_limit: Max workflow results
            feedback_limit: Max feedback signals

        Returns:
            KnowledgeContext with all retrieved knowledge
        """
        context = KnowledgeContext()

        # 1. Search GIS documentation via RAG
        self._ensure_rag()
        if self.rag and self.rag.available:
            try:
                rag_result = self.rag.query(
                    query, doc_limit=doc_limit, workflow_limit=0
                )
                context.relevant_docs = rag_result.documents
            except Exception as e:
                logger.debug(f"RAG retrieval failed: {e}")

        # 2. Find similar past workflows
        try:
            context.similar_workflows = self.workflow_memory.find_similar(
                query, limit=workflow_limit
            )
        except Exception as e:
            logger.debug(f"Workflow search failed: {e}")

        # 3. Check query patterns
        try:
            context.query_patterns = self.query_memory.get_patterns(query)
        except Exception as e:
            logger.debug(f"Pattern search failed: {e}")

        # 4. Get feedback signals
        try:
            context.feedback_signals = self.feedback_memory.get_relevant_feedback(
                query, limit=feedback_limit
            )
        except Exception as e:
            logger.debug(f"Feedback search failed: {e}")

        # 5. Get user preferences
        try:
            context.user_preferences = self.query_memory.get_user_preferences()
        except Exception as e:
            logger.debug(f"Preferences retrieval failed: {e}")

        # 6. Check tool warnings from proposed workflows
        if context.similar_workflows:
            all_tools = set()
            for wf in context.similar_workflows:
                all_tools.update(wf.tool_sequence)
            context.tool_warnings = self.feedback_memory.get_tool_warnings(
                list(all_tools)
            )

        # 7. Assemble context prompt for the LLM
        context.context_prompt = self._build_context_prompt(context)

        logger.info(
            f"Knowledge retrieved for '{query[:50]}...': {context}"
        )
        return context

    def learn_from_execution(
        self,
        query: str,
        plan: Any,
        result: Any,
    ) -> None:
        """
        Learn from a completed execution.

        Called after every execution to update all memory stores.

        Args:
            query: Original user query
            plan: ExecutionPlan object
            result: ExecutionResult object
        """
        success = getattr(result, "success", False)

        # Extract intent
        intent = ""
        tool_sequence = []
        if plan and hasattr(plan, "request") and plan.request:
            intent_obj = getattr(plan.request, "intent", None)
            intent = intent_obj.value if hasattr(intent_obj, "value") else str(intent_obj or "")
        if plan and hasattr(plan, "steps"):
            tool_sequence = [s.tool_name for s in plan.steps]

        # 1. Store in workflow memory
        try:
            self.workflow_memory.store_workflow(query, plan, result, success)
        except Exception as e:
            logger.debug(f"Workflow memory update failed: {e}")

        # 2. Record in query memory
        try:
            entities = {}
            if plan and hasattr(plan, "request") and plan.request:
                entities = getattr(plan.request, "entities", {})
            status = "success" if success else "failed"
            self.query_memory.record_query(
                query=query,
                intent=intent,
                entities=entities,
                status=status,
                tool_sequence=tool_sequence,
            )
        except Exception as e:
            logger.debug(f"Query memory update failed: {e}")

        # 3. Record in feedback memory
        try:
            self.feedback_memory.record_feedback(
                query=query,
                plan=plan,
                result=result,
                success=success,
            )
        except Exception as e:
            logger.debug(f"Feedback memory update failed: {e}")

        logger.info(
            f"Learned from execution: "
            f"{'✅' if success else '❌'} '{query[:50]}...'"
        )

    def search_gis_docs(
        self,
        query: str,
        collection: str = "gis_docs",
        limit: int = 5,
    ) -> List[Any]:
        """
        Direct document search against a Qdrant collection.

        Used by the MCP ``search_gis_docs`` tool. Returns a list of
        ``SearchResult`` objects (``.text`` / ``.score`` / ``.source`` /
        ``.metadata``). Returns ``[]`` when the RAG service is unavailable.
        """
        self._ensure_rag()
        if not self.rag or not self.rag.available:
            return []
        try:
            return self.rag.retriever.hybrid_search(query, collection=collection, limit=limit)
        except Exception as e:
            logger.debug(f"search_gis_docs failed: {e}")
            return []

    def ingest_documents(self, directory: str, collection: str = "gis_docs") -> int:
        """
        Ingest documents from a directory into the knowledge base.

        Convenience wrapper around RAGService.ingest_documents().

        Args:
            directory: Path to directory with documents
            collection: Target Qdrant collection

        Returns:
            Number of chunks ingested
        """
        self._ensure_rag()
        if not self.rag or not self.rag.available:
            logger.warning("Cannot ingest — RAG service unavailable")
            return 0

        return self.rag.ingest_documents(directory, collection)

    def get_workflow_history(self) -> List[str]:
        """Get list of all known workflow names."""
        return self.workflow_memory.list_workflows()

    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        stats = {
            "workflow_count": len(self.workflow_memory._cache),
            "query_count": len(self.query_memory),
            "feedback_count": len(self.feedback_memory),
            "tool_reliability": self.feedback_memory.get_tool_reliability(),
            "frequent_operations": self.query_memory.get_frequent_operations(),
        }

        if self.rag and self.rag.available:
            for collection in ["gis_docs", "gis_workflows", "geosi_history"]:
                info = self.rag.store.collection_info(collection)
                if info:
                    stats[f"qdrant_{collection}"] = info.get("points_count", 0)

        return stats

    # ── Context prompt assembly ────────────────────────────────────────

    def _build_context_prompt(self, context: KnowledgeContext) -> str:
        """
        Build a context prompt section from all retrieved knowledge.

        This is injected into the LLM prompt before the planning instruction.
        """
        if not context.has_knowledge():
            return ""

        sections = ["─── GIS Knowledge Context ───\n"]

        # Documentation
        if context.relevant_docs:
            sections.append("## Relevant GIS Documentation\n")
            for i, doc in enumerate(context.relevant_docs[:5], 1):
                source_label = (
                    doc.source.split("/")[-1] if hasattr(doc, "source") and doc.source
                    else "docs"
                )
                text = doc.text if hasattr(doc, "text") else str(doc)
                score = doc.score if hasattr(doc, "score") else 0
                sections.append(
                    f"[{i}] {source_label} (relevance: {score:.2f})\n"
                    f"{text[:400]}\n"
                )

        # Similar workflows
        if context.similar_workflows:
            sections.append("\n## Similar Past Workflows\n")
            for i, wf in enumerate(context.similar_workflows[:5], 1):
                tools = " → ".join(wf.tool_sequence) if wf.tool_sequence else "N/A"
                status = "✅ succeeded" if wf.success else "❌ failed"
                sections.append(
                    f"[{i}] {wf.name} ({status})\n"
                    f"  Query: \"{wf.user_query}\"\n"
                    f"  Tools: {tools}\n"
                    f"  {wf.description[:200]}\n"
                )

        # Query patterns
        if context.query_patterns:
            sections.append("\n## User Patterns\n")
            for pattern in context.query_patterns[:3]:
                sections.append(
                    f"- {pattern.pattern}: seen {pattern.frequency}x, "
                    f"success rate {pattern.avg_success_rate:.0%}\n"
                )

        # Feedback warnings
        if context.feedback_signals:
            failure_signals = [s for s in context.feedback_signals if not s.success]
            if failure_signals:
                sections.append("\n## Known Issues\n")
                for signal in failure_signals[:3]:
                    if signal.suggestion:
                        sections.append(
                            f"⚠ Similar query failed ({signal.error_type}): "
                            f"{signal.suggestion}\n"
                        )

        # Tool warnings
        if context.tool_warnings:
            sections.append("\n## Tool Warnings\n")
            for warning in context.tool_warnings:
                sections.append(f"{warning}\n")

        sections.append("\n─── End Knowledge Context ───\n")
        return "\n".join(sections)

    def __repr__(self):
        return (
            f"KnowledgeManager("
            f"rag={'ready' if self.rag and getattr(self.rag, 'available', False) else 'off'}, "
            f"workflows={len(self.workflow_memory._cache)}, "
            f"queries={len(self.query_memory)}, "
            f"feedback={len(self.feedback_memory)})"
        )
