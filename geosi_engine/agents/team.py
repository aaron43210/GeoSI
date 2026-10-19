# -*- coding: utf-8 -*-
"""
GeoSI v2 — Agent Team
════════════════════════════════════════════════════════════════════
The agents one session's pipeline works with, created once per engine.

    permission     PermissionSafetyAgent   screens requests, gates steps, audit log
    planning       PlanningAgent           plans (rules → deterministic → templates → LLM)
    reflection     ReflectionAgent         critic before execution, feedback after failures
    validation     ValidationAgent         static plan checks (tools, layers, fields, expressions)
    optimizer      WorkflowOptimizationAgent  advisory suggestions on the plan
    gis            GISAgent                executes steps through the permission gate
    verification   VerificationAgent       checks results against the request + file QA
    reporter       ReportGenerationAgent   answers questions, writes the execution report
    research       ResearchAgent           GraphRAG retrieval (only with the knowledge layer)

Domain agents (remote sensing, machine learning, geology, code generation)
are reached as registered tools that the GIS Agent dispatches, so they go
through the same pipeline and permission gate as every other tool. The
SupervisorAgent owns sessions, circuit breakers and approvals, and drives
this team through ``AgentLoop``.
"""
from __future__ import annotations

from typing import Any, Optional


class AgentTeam:
    """Lazily-built set of agents bound to one engine (session)."""

    def __init__(self, engine: Any, supervisor: Any = None) -> None:
        from geosi_engine.agents.gis_agent import GISAgent
        from geosi_engine.agents.permission_safety import PermissionSafetyAgent
        from geosi_engine.agents.planning import PlanningAgent
        from geosi_engine.agents.reflection import ReflectionAgent
        from geosi_engine.agents.report_generation import ReportGenerationAgent
        from geosi_engine.agents.validation import ValidationAgent
        from geosi_engine.agents.verification import VerificationAgent
        from geosi_engine.agents.workflow_optimization import WorkflowOptimizationAgent

        self.engine = engine
        self.permission = PermissionSafetyAgent(engine)
        self.planning = PlanningAgent(engine, supervisor=supervisor)
        self.reflection = ReflectionAgent(engine)
        self.validation = ValidationAgent(engine)
        self.optimizer = WorkflowOptimizationAgent(engine)
        self.gis = GISAgent(engine, permission_agent=self.permission)
        self.verification = VerificationAgent(engine)
        self.reporter = ReportGenerationAgent(engine)
        self._research: Optional[Any] = None

    def attach_supervisor(self, supervisor: Any) -> None:
        self.planning._supervisor = supervisor

    @property
    def research(self) -> Optional[Any]:
        """ResearchAgent, created on first use and only with the knowledge layer."""
        if self._research is None and getattr(self.engine, "knowledge", None) is not None:
            from geosi_engine.agents.research import ResearchAgent

            self._research = ResearchAgent(self.engine, self.permission)
        return self._research
