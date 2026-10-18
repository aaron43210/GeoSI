# -*- coding: utf-8 -*-
"""
GeoSI v2 — Validation Agent
════════════════════════════════════════════════════════════════════
Runs immediately after Planning, before Permission & Safety.

Responsibilities (PRD FR-1.2, G4, G12)
────────────────────────────────────────
1. Validates CRS, layer existence, parameter types/ranges using the
   existing ``ValidationEngine`` (KEEP — no rewrite).
2. SQL allow-list: any table/column identifier from an LLM-generated
   plan must pass the allow-list before reaching SQL (G4 fix).
3. Safe expression evaluation: replaces ``gdf.eval(expression)``
   with an AST-based evaluator that rejects arbitrary code (G12 fix).
"""
from __future__ import annotations

import ast
import logging
import re
from typing import Any, Optional

from geosi_engine.models import ExecutionPlan, ToolStep
from geosi_engine.validation import ValidationEngine, ValidationReport, ValidationIssue

logger = logging.getLogger("geosi_engine.agents.validation")


# ---------------------------------------------------------------------------
# SQL Identifier Allow-List
# ---------------------------------------------------------------------------

class TableAllowList:
    """
    Validates PostGIS table/column identifiers before they are used in SQL.

    The allow-list is populated at startup from ``PostGISManager.list_layers()``
    and can be extended via ``register(name)``.

    Any name that fails validation raises ``ValueError`` — the caller (Validation
    Agent or PostGISManager) must handle this before building SQL.
    """

    # Only allow names matching this pattern (prevents injection via
    # special characters even if somehow an attacker slips past the list).
    _SAFE_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]{0,127}$")

    def __init__(self) -> None:
        self._names: set[str] = set()
        # Always allow the fixed GeoSI system tables
        for name in (
            "geosi_layers",
            "geosi_projects",
            "geosi_workflow_history",
            "geosi_execution_results",
            "geosi_audit_log",
            "geosi_policy_overrides",
            "geosi_pending_approvals",
            "geosi_eval_runs",
            "geosi_query_history",
            "geosi_feedback_history",
        ):
            self._names.add(name)

    def register(self, name: str) -> None:
        """Register a known-safe table name."""
        if self._SAFE_RE.match(name):
            self._names.add(name)

    def register_many(self, names: list[str]) -> None:
        for n in names:
            self.register(n)

    def is_allowed(self, name: str) -> bool:
        return name in self._names and bool(self._SAFE_RE.match(name))

    def validate_and_quote(self, name: str) -> str:
        """
        Validate *name* is in the allow-list and safe to use as a SQL
        identifier.

        Returns a quoted identifier string (double-quoted, escaped).
        Raises ``ValueError`` on any failure.
        """
        if not name:
            raise ValueError("Table/column name must not be empty.")
        if not self._SAFE_RE.match(name):
            raise ValueError(
                f"Table/column name {name!r} contains invalid characters. "
                "Only alphanumeric characters and underscores are allowed."
            )
        if name not in self._names:
            raise ValueError(
                f"Table/column name {name!r} is not in the known-table allow-list. "
                "Register it via PostGISManager or the admin API before use."
            )
        # Double-quote and escape any internal double-quotes
        escaped = name.replace('"', '""')
        return f'"{escaped}"'


# Singleton — shared across the process lifetime
_TABLE_ALLOW_LIST = TableAllowList()


def get_allow_list() -> TableAllowList:
    """Return the process-level allow-list singleton."""
    return _TABLE_ALLOW_LIST


# ---------------------------------------------------------------------------
# Safe Expression Evaluator (G12 fix — replaces gdf.eval())
# ---------------------------------------------------------------------------

class _SafeNodeVisitor(ast.NodeVisitor):
    """
    AST visitor that rejects any node type not on the safe list.

    Safe nodes: arithmetic ``BinOp``, ``UnaryOp``, column ``Name``,
    numeric/string ``Constant``, and ``Expr`` wrappers.
    Everything else (``Call``, ``Attribute``, ``Import``, ``Subscript``,
    ``GeneratorExp``, etc.) raises ``ValueError``.
    """

    _ALLOWED = frozenset({
        ast.BinOp, ast.UnaryOp, ast.Name, ast.Constant,
        ast.Expr, ast.Expression,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
        ast.Pow, ast.FloorDiv,
        ast.UAdd, ast.USub, ast.Not,
        ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
        ast.BoolOp, ast.And, ast.Or,
        ast.Load,  # Variable access context
    })

    def generic_visit(self, node: ast.AST) -> None:
        if type(node) not in self._ALLOWED:
            raise ValueError(
                f"Disallowed expression node type: {type(node).__name__!r}. "
                "Only arithmetic / comparison / column-reference expressions "
                "are permitted. Imports, function calls, and attribute access "
                "are blocked."
            )
        super().generic_visit(node)


class SafeExpressionEvaluator:
    """
    Validates a field-calculator expression before passing it to pandas.

    Replaces ``gdf.eval(expression)`` with a two-step approach:
      1. Parse the expression string with the Python AST.
      2. Walk the AST with ``_SafeNodeVisitor``; reject anything unsafe.
      3. If valid, execute via ``gdf.eval(expression, engine='numexpr')``
         (numexpr engine, *not* the Python engine, which can execute
         arbitrary code).
    """

    def validate(self, expression: str) -> None:
        """
        Raise ``ValueError`` if *expression* contains unsafe constructs.

        Parameters
        ----------
        expression:
            A field-calculator expression string (e.g. ``"area * 2.5"``).
        """
        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            raise ValueError(f"Invalid expression syntax: {exc}") from exc

        _SafeNodeVisitor().visit(tree)

    def evaluate(self, gdf: Any, expression: str) -> Any:
        """
        Validate and evaluate *expression* against *gdf*.

        Parameters
        ----------
        gdf:
            A ``geopandas.GeoDataFrame`` or ``pandas.DataFrame``.
        expression:
            Field calculator expression (column arithmetic only).

        Returns
        -------
        Series
            Result of the evaluated expression.
        """
        self.validate(expression)
        # Use 'python' engine only as fallback; prefer numexpr (safer sandbox)
        try:
            return gdf.eval(expression, engine="numexpr")
        except Exception:
            # numexpr not available → use python engine but expression is
            # already AST-validated above so arbitrary code is blocked
            return gdf.eval(expression, engine="python")


# Module-level singleton
safe_evaluator = SafeExpressionEvaluator()


# ---------------------------------------------------------------------------
# Validation Agent
# ---------------------------------------------------------------------------

class ValidationAgent:
    """
    Validates an ``ExecutionPlan`` before it reaches Permission & Safety.

    Wraps the existing ``ValidationEngine`` (KEEP — no rewrite) and adds:
    * SQL allow-list checks (G4 fix)
    * gdf.eval safety checks (G12 fix)
    * CRS mismatch detection
    * Layer existence checks
    """

    def __init__(self, engine: Any) -> None:
        self._engine = engine
        self._validator = ValidationEngine()

    def validate(
        self,
        plan: ExecutionPlan,
        state: Optional[Any] = None,
    ) -> ValidationReport:
        """
        Validate *plan* against the current workspace state.

        Returns a ``ValidationReport``; check ``report.ok`` before proceeding.
        """
        report = ValidationReport()

        for step in plan.steps:
            self._validate_step(step, state, report)

        return report

    def _validate_step(
        self,
        step: ToolStep,
        state: Optional[Any],
        report: ValidationReport,
    ) -> None:
        """Validate one step: tool existence, CRS, layers, SQL safety, eval safety."""

        # Tool existence
        if hasattr(self._engine, "registry"):
            tool = self._engine.registry.get_tool(step.tool_name)
            if tool is None:
                report.add(ValidationIssue(
                    "error", "unknown_tool",
                    f"Step {step.step_id}: tool '{step.tool_name}' not found in registry.",
                ))
                return

        # Layer existence + CRS check
        if state is not None:
            for layer_name in step.input_layers:
                layer = state.get_layer(layer_name)
                if layer is None:
                    report.add(ValidationIssue(
                        "error", "unknown_layer",
                        f"Step {step.step_id}: input layer '{layer_name}' is not loaded.",
                        layer_name,
                    ))
                else:
                    crs_report = self._validator.validate_crs(layer)
                    report.issues.extend(crs_report.issues)
                    if not crs_report.ok:
                        report.ok = False

        # SQL identifier safety (G4 fix)
        self._check_sql_identifiers(step, report)

        # Expression safety (G12 fix)
        self._check_expressions(step, report)

    def _check_sql_identifiers(
        self, step: ToolStep, report: ValidationReport
    ) -> None:
        """Reject any SQL-injectable identifier in parameters."""
        allow_list = get_allow_list()
        for key, value in step.parameters.items():
            if not isinstance(value, str):
                continue
            # Only check values that look like table/column names
            if key.lower() in ("table", "table_name", "layer_table", "column", "field"):
                try:
                    allow_list.validate_and_quote(value)
                except ValueError as exc:
                    report.add(ValidationIssue(
                        "error", "sql_injection_risk",
                        f"Step {step.step_id}, param '{key}': {exc}",
                    ))

    def _check_expressions(
        self, step: ToolStep, report: ValidationReport
    ) -> None:
        """Reject unsafe field-calculator expressions (G12 fix)."""
        for key, value in step.parameters.items():
            if key.lower() in ("expression", "formula", "calc_expression"):
                if isinstance(value, str):
                    try:
                        safe_evaluator.validate(value)
                    except ValueError as exc:
                        report.add(ValidationIssue(
                            "error", "unsafe_expression",
                            f"Step {step.step_id}, param '{key}': {exc}",
                        ))
