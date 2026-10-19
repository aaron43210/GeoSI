"""
GeoSI v2 — Phase P5–P8 Agent Tests
Tests for all 8 newly implemented agents:
  7.  Remote Sensing Agent
  8.  Machine Learning Agent
  9.  Geology Agent
  10. Verification Agent
  11. Report Generation Agent
  12. Research Agent
  13. Workflow Optimization Agent
  14. Code Generation Agent
  +   Reflection Agent (Agent #4)
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

# ── Reflection Agent (Agent #4) ───────────────────────────────────────────


def test_reflection_critic_passes_clean_plan():
    """Critic should pass a plan with no known-bad tools."""
    from geosi_engine.agents.reflection import ReflectionAgent
    from geosi_engine.models import ExecutionPlan, ToolStep

    engine = MagicMock()
    engine.knowledge = None
    engine.registry = None

    agent = ReflectionAgent(engine=engine)
    plan = ExecutionPlan(
        steps=[
            ToolStep(tool_name="native:buffer", risk_level="mutating"),
            ToolStep(tool_name="native:clip", risk_level="mutating"),
        ]
    )
    report = agent.critic(plan)
    assert report is not None
    assert len(report.errors()) == 0  # No hard errors for unknown tools


def test_reflection_retry_exhausts_raises():
    """reflect_and_retry must raise RuntimeError after N=2 retries."""
    from geosi_engine.agents.reflection import ReflectionAgent

    engine = MagicMock()
    engine.knowledge = None
    agent = ReflectionAgent(engine=engine)

    from geosi_engine.models import ExecutionPlan

    plan = ExecutionPlan(steps=[])

    call_count = 0

    def always_fails(p):
        nonlocal call_count
        call_count += 1
        raise RuntimeError("simulated failure")

    with pytest.raises(RuntimeError, match="exhausted"):
        agent.reflect_and_retry(plan, error="test error", executor_fn=always_fails)

    assert call_count == 2  # N=2 retries


# ── Verification Agent (Agent #10) ───────────────────────────────────────


def test_verification_nonexistent_vector():
    """verify_vector on a missing file should produce an error finding."""
    from geosi_engine.agents.verification import VerificationAgent

    agent = VerificationAgent(engine=MagicMock())
    report = agent.verify_vector("/nonexistent/path/layer.gpkg")
    assert not report.passed
    assert len(report.errors()) > 0


def test_verification_nonexistent_raster():
    """verify_raster on a missing file should produce an error finding."""
    from geosi_engine.agents.verification import VerificationAgent

    agent = VerificationAgent(engine=MagicMock())
    report = agent.verify_raster("/nonexistent/path/dem.tif")
    assert not report.passed
    assert len(report.findings) > 0


def test_verification_crs_match_no_files():
    """verify_crs_match with no files should pass trivially."""
    from geosi_engine.agents.verification import VerificationAgent

    agent = VerificationAgent(engine=MagicMock())
    report = agent.verify_crs_match([])
    assert report.passed  # Nothing to mismatch


def test_verification_execution_result_no_output():
    """verify_execution_result with no output path should pass (in-memory result)."""
    from geosi_engine.agents.verification import VerificationAgent

    agent = VerificationAgent(engine=MagicMock())
    result = MagicMock(spec=[])  # No output_layer / output_path attrs
    result.success = True
    report = agent.verify_execution_result(result)
    assert report.passed


# ── Report Generation Agent (Agent #11) ──────────────────────────────────


def test_report_execution_summary(tmp_path):
    """Generate an execution summary and confirm file is written."""
    from geosi_engine.agents.report_generation import ReportGenerationAgent, ReportRequest

    agent = ReportGenerationAgent(engine=MagicMock())
    out = tmp_path / "summary.md"
    req = ReportRequest(
        report_type="execution_summary",
        audit_log_id="test-audit-001",
        session_id="test-session",
        output_path=str(out),
    )
    result = agent.generate(req)
    assert result.success
    assert result.audit_log_id == "test-audit-001"
    assert out.exists()
    assert "GeoSI Execution Summary" in out.read_text()


def test_report_workflow_graph_mermaid(tmp_path):
    """Generate a Mermaid workflow graph from a plan."""
    from geosi_engine.agents.report_generation import ReportGenerationAgent, ReportRequest
    from geosi_engine.models import ExecutionPlan, ToolStep

    agent = ReportGenerationAgent(engine=MagicMock())
    plan = ExecutionPlan(
        steps=[
            ToolStep(tool_name="native:buffer", risk_level="mutating"),
            ToolStep(tool_name="native:clip", risk_level="mutating"),
        ]
    )
    out = tmp_path / "workflow.md"
    req = ReportRequest(
        report_type="workflow_graph",
        plan=plan,
        output_path=str(out),
        parameters={"format": "mermaid"},
    )
    result = agent.generate(req)
    assert result.success
    assert "mermaid" in result.content


def test_report_unknown_type():
    """Requesting an unknown report type should return success=False."""
    from geosi_engine.agents.report_generation import ReportGenerationAgent, ReportRequest

    agent = ReportGenerationAgent(engine=MagicMock())
    req = ReportRequest(report_type="unknown_type")
    result = agent.generate(req)
    assert not result.success
    assert "unknown" in result.error.lower()


# ── Code Generation Agent (Agent #14) ────────────────────────────────────


def test_codegen_requires_human_review():
    """GeneratedCode.requires_human_review must ALWAYS be True."""
    from geosi_engine.agents.code_generation import GeneratedCode

    # Normal construction
    code = GeneratedCode(success=True, target_language="pyqgis", code="print('hello')")
    assert code.requires_human_review is True

    # Attempting to pass False must still result in True
    code2 = GeneratedCode(success=True, target_language="pyqgis", requires_human_review=False)
    assert code2.requires_human_review is True  # enforced by __post_init__


def test_codegen_pyqgis_from_plan():
    """Generate PyQGIS code from a simple plan."""
    from geosi_engine.agents.code_generation import CodeGenerationAgent, CodeRequest
    from geosi_engine.models import ExecutionPlan, ToolStep

    agent = CodeGenerationAgent(engine=MagicMock())
    plan = ExecutionPlan(
        steps=[
            ToolStep(tool_name="native:buffer", risk_level="mutating", parameters={"DISTANCE": 500}),
        ]
    )
    req = CodeRequest(target_language="pyqgis", plan=plan)
    result = agent.generate(req)

    assert result.success
    assert result.requires_human_review is True
    assert "processing.run" in result.code
    assert "native:buffer" in result.code
    assert len(result.warnings) > 0  # Must always warn about review


def test_codegen_geopandas_from_plan():
    """Generate GeoPandas code from a plan."""
    from geosi_engine.agents.code_generation import CodeGenerationAgent, CodeRequest
    from geosi_engine.models import ExecutionPlan, ToolStep

    agent = CodeGenerationAgent(engine=MagicMock())
    plan = ExecutionPlan(
        steps=[
            ToolStep(tool_name="native:clip", risk_level="mutating"),
        ]
    )
    req = CodeRequest(target_language="geopandas", plan=plan)
    result = agent.generate(req)

    assert result.success
    assert "import geopandas" in result.code
    assert result.requires_human_review is True


def test_codegen_auto_language_detection():
    """Auto-detect pyqgis when native: tools are present."""
    from geosi_engine.agents.code_generation import CodeGenerationAgent, CodeRequest
    from geosi_engine.models import ExecutionPlan, ToolStep

    agent = CodeGenerationAgent(engine=MagicMock())
    plan = ExecutionPlan(steps=[ToolStep(tool_name="native:buffer")])
    req = CodeRequest(target_language="auto", plan=plan)
    result = agent.generate(req)

    assert result.target_language == "pyqgis"


# ── Research Agent (Agent #12) ────────────────────────────────────────────


def test_research_search_no_knowledge():
    """Research search should succeed gracefully when knowledge is unavailable."""
    from geosi_engine.agents.research import ResearchAgent, ResearchQuery

    engine = MagicMock()
    engine.knowledge = None
    permission = MagicMock()
    agent = ResearchAgent(engine=engine, permission_agent=permission)

    req = ResearchQuery(query="NDVI vegetation analysis", max_results=5)
    result = agent.search(req)

    assert result.success
    assert result.query == "NDVI vegetation analysis"
    assert result.total_sources == 0  # No sources without knowledge
    assert isinstance(result.citations, list)


# ── Workflow Optimization Agent (Agent #13) ───────────────────────────────


def test_workflow_opt_detects_redundant_steps():
    """WFO should flag back-to-back identical tool steps."""
    from geosi_engine.agents.workflow_optimization import WorkflowOptimizationAgent
    from geosi_engine.models import ExecutionPlan, ToolStep

    agent = WorkflowOptimizationAgent(engine=MagicMock())
    plan = ExecutionPlan(
        steps=[
            ToolStep(tool_name="native:buffer", parameters={"DISTANCE": 500}),
            ToolStep(tool_name="native:buffer", parameters={"DISTANCE": 500}),  # identical
            ToolStep(tool_name="native:clip"),
        ]
    )
    report = agent.analyze(plan)

    assert report.success
    redundant = [s for s in report.suggestions if s.type == "remove_step"]
    assert len(redundant) >= 1


def test_workflow_opt_compare():
    """compare_workflows should show tool differences."""
    from geosi_engine.agents.workflow_optimization import WorkflowOptimizationAgent
    from geosi_engine.models import ExecutionPlan, ToolStep

    agent = WorkflowOptimizationAgent(engine=MagicMock())
    plan_a = ExecutionPlan(steps=[ToolStep(tool_name="native:buffer"), ToolStep(tool_name="native:clip")])
    plan_b = ExecutionPlan(steps=[ToolStep(tool_name="native:buffer"), ToolStep(tool_name="native:dissolve")])

    diff = agent.compare_workflows(plan_a, plan_b)
    assert "native:clip" in diff["tools_only_in_a"]
    assert "native:dissolve" in diff["tools_only_in_b"]


# ── Remote Sensing Agent (Agent #7) ───────────────────────────────────────


def test_rs_supported_indices():
    """All expected spectral indices must be registered."""
    from geosi_engine.agents.remote_sensing import RemoteSensingAgent

    agent = RemoteSensingAgent(engine=MagicMock(), permission_agent=MagicMock())
    indices = agent.supported_indices()

    for idx in ("NDVI", "NDWI", "SAVI", "EVI", "NDBI"):
        assert idx in indices


def test_rs_unknown_index():
    """Unknown spectral index should return error result."""
    from geosi_engine.agents.remote_sensing import RemoteSensingAgent

    agent = RemoteSensingAgent(engine=MagicMock(), permission_agent=MagicMock())
    result = agent.compute_spectral_index("INVALID_IDX", "/fake/layer.tif", {})

    assert not result.success
    assert "Unknown spectral index" in result.error


# ── Machine Learning Agent (Agent #8) ────────────────────────────────────


def test_ml_unknown_job_type():
    """Unknown ML job type should return error."""
    from geosi_engine.agents.machine_learning import MachineLearningAgent, MLJobRequest

    engine = MagicMock()
    permission = MagicMock()
    permission.check_permission.return_value = MagicMock(decision="allow")
    permission.audit_log_before_execution.return_value = "audit-001"
    permission.update_audit_log.return_value = None

    agent = MachineLearningAgent(engine=engine, permission_agent=permission)
    job = MLJobRequest(job_type="unknown_type", algorithm="rf", session_id="test")

    result = agent._dispatch(job)
    assert not result.success
    assert "Unknown ML job type" in result.error


# ── Geology Agent (Agent #9) ──────────────────────────────────────────────


def test_geology_unknown_operation():
    """Unknown geology operation should return error."""
    from geosi_engine.agents.geology import GeologyAgent, GeologyJobRequest

    engine = MagicMock()
    engine.knowledge = None
    permission = MagicMock()
    permission.check_permission.return_value = MagicMock(decision="allow")
    permission.audit_log_before_execution.return_value = "audit-002"
    permission.update_audit_log.return_value = None

    agent = GeologyAgent(engine=engine, permission_agent=permission)
    job = GeologyJobRequest(operation="unknown_op", session_id="test")

    result = agent.execute(job)
    assert not result.success
    assert "Unknown geology operation" in result.error


def test_geology_supported_operations():
    """All PRD-listed geology operations must be in the registry."""
    from geosi_engine.agents.geology import GEOLOGY_OPERATIONS

    required = [
        "geological_mapping",
        "structural_analysis",
        "stratigraphic_modeling",
        "cross_section",
        "fault_visualization",
        "fold_analysis",
        "borehole_correlation",
        "mineral_prospectivity",
        "landslide_susceptibility",
        "ai_interpretation",
    ]
    for op in required:
        assert op in GEOLOGY_OPERATIONS, f"Missing geology op: {op}"
