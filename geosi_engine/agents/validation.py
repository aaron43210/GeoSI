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

_NAMED_LAYER_RE = re.compile(r"\b(?:the\s+)?([a-z_][a-z0-9_]*)\s+layer\b", re.IGNORECASE)
_NOT_LAYER_WORDS = frozenset({
    "the", "a", "an", "this", "that", "new", "result", "output", "input", "each",
    "every", "same", "previous", "vector", "raster", "point", "line", "polygon",
    "one", "single", "another", "separate", "combined", "merged", "final", "temporary",
    "my", "your", "base", "current", "active", "selected", "any", "all", "other", "first",
    "second", "last", "target", "source", "reference", "mask", "empty", "two", "three",
})
# Tools that build SQL from their parameters (identifiers must pass the allow-list)
_SQL_TOOL_RE = re.compile(r"sql|postgis|spatialite|database", re.IGNORECASE)


class ValidationAgent:
    """
    Validates an ``ExecutionPlan`` before any step runs.

    Checks, per step:
    * the tool exists in the registry;
    * input layers exist (named layers or earlier step outputs);
    * field parameters name real fields of their input layer — a wrong
      name comes back with the layer's actual fields so the planner can
      correct it;
    * QGIS expressions parse (``QgsExpression``, registered by the QGIS
      bridge); other tools' expressions pass the safe AST evaluator (G12);
    * identifiers sent to SQL-building tools pass the allow-list (G4);
    * CRS of input layers (``ValidationEngine``).

    ``check_request`` catches requests that name a layer that isn't loaded.
    """

    def __init__(self, engine: Any) -> None:
        self._engine = engine
        self._validator = ValidationEngine()

    # Patterns that bypass the named-layer check (conversational / educational / code-gen)
    _LAYER_FREE_RE = re.compile(
        r"^(?:hi|hello|hey|howdy|greetings?|help|what\s+can\s+you|who\s+are\s+you)"
        r"|\b(?:what\s+is|what\s+are|how\s+(?:do\s+I|to|does)|explain|describe|define"
        r"|tell\s+me\s+about|difference\s+between)\b"
        r"|\b(?:generate|write|create|show|give\s+me|make)\b.{0,50}"
        r"\b(?:code|script|snippet|example|template|function)\b",
        re.IGNORECASE,
    )

    def check_request(self, query: str, state: Optional[Any] = None) -> Optional[str]:
        """
        Return a message when the request names a layer that isn't loaded.

        Conversational, educational, and code-gen queries are exempt so the
        engine responds helpfully even when no project is open.
        """
        # Don't gate on layers for non-spatial queries
        if self._LAYER_FREE_RE.search(query or ""):
            return None

        state = state if state is not None else getattr(self._engine, "state", None)
        if state is None:
            return None
        names = {n.lower() for n in state.list_layers()}
        for m in _NAMED_LAYER_RE.finditer(query or ""):
            word = m.group(1).lower()
            if word in _NOT_LAYER_WORDS:
                continue
            if word not in names and word.rstrip("s") not in names and word + "s" not in names:
                loaded = ", ".join(state.list_layers()) or "none"
                return f"There is no layer named '{word}' in the project. Loaded layers: {loaded}."
        return None

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
        produced: set[str] = set()
        for step in plan.steps:
            self._validate_step(step, state, report, produced)
            if step.output_name:
                produced.add(step.output_name)
        return report

    # ------------------------------------------------------------------

    def _validate_step(
        self,
        step: ToolStep,
        state: Optional[Any],
        report: ValidationReport,
        produced: set[str],
    ) -> None:
        registry = getattr(self._engine, "registry", None)
        tool = registry.get_tool(step.tool_name) if registry is not None else None
        if registry is not None and tool is None:
            report.add(ValidationIssue(
                "error", "unknown_tool",
                f"Step {step.step_id}: tool '{step.tool_name}' not found in registry.",
            ))
            return
        spec = tool.spec() if tool is not None else None
        is_qgis = bool(getattr(spec, "qgis_algorithm", None))
        specs = {p.name: p for p in (getattr(spec, "parameters", None) or [])}

        # Layers named in input_layers or in layer-typed parameters
        layer_names = list(step.input_layers)
        for key, value in step.parameters.items():
            if getattr(specs.get(key), "param_type", "") == "layer":
                layer_names.extend(v for v in (value if isinstance(value, list) else [value])
                                   if isinstance(v, str))
        if state is not None:
            for name in layer_names:
                if name in produced or name.startswith("step_"):
                    continue
                layer = state.get_layer(name)
                if layer is None:
                    if self._looks_like_path(name):
                        continue
                    report.add(ValidationIssue(
                        "error", "unknown_layer",
                        f"Step {step.step_id}: input layer '{name}' is not loaded.", name,
                    ))
                    continue
                crs_report = self._validator.validate_crs(layer)
                report.issues.extend(i for i in crs_report.issues if i.severity != "error")

        if state is not None and specs:
            self._check_fields(step, specs, state, report)
        self._check_expressions(step, specs, is_qgis, report)
        if _SQL_TOOL_RE.search(step.tool_name):
            self._check_sql_identifiers(step, report)

    @staticmethod
    def _looks_like_path(name: str) -> bool:
        return bool(re.search(r"[\\/]|\.(gpkg|shp|tif|tiff|geojson|json|csv|fgb|gml|kml)$", name, re.I))

    def _check_fields(self, step: ToolStep, specs: dict, state: Any, report: ValidationReport) -> None:
        """Field parameters must name fields of the layer they refer to."""
        for key, value in step.parameters.items():
            pspec = specs.get(key)
            if getattr(pspec, "param_type", "") != "field" or not pspec.parent_layer:
                continue
            layer_name = step.parameters.get(pspec.parent_layer)
            layer = state.get_layer(layer_name) if isinstance(layer_name, str) else None
            fields = [f for f in (getattr(layer, "fields", None) or []) if f != "fid"]
            if not fields:
                continue  # unknown (e.g. an earlier step's output)
            wanted = value if isinstance(value, list) else (
                [v.strip() for v in value.split(",")] if isinstance(value, str) else [])
            by_lower = {f.lower(): f for f in fields}
            for name in wanted:
                if not name or name in fields:
                    continue
                if name.lower() in by_lower:
                    # Same field, wrong case: fix it rather than fail
                    fixed = by_lower[name.lower()]
                    if isinstance(value, list):
                        step.parameters[key] = [fixed if v == name else v for v in step.parameters[key]]
                    else:
                        step.parameters[key] = str(step.parameters[key]).replace(name, fixed)
                    continue
                report.add(ValidationIssue(
                    "error", "unknown_field",
                    f"Step {step.step_id}: field '{name}' ({key}) does not exist in layer "
                    f"'{layer_name}'. Its fields are: {', '.join(fields)}.",
                    layer_name,
                ))

    def _check_sql_identifiers(self, step: ToolStep, report: ValidationReport) -> None:
        """Reject any SQL-injectable identifier in parameters (G4)."""
        allow_list = get_allow_list()
        for key, value in step.parameters.items():
            if not isinstance(value, str):
                continue
            if key.lower() in ("table", "table_name", "layer_table", "column", "field"):
                try:
                    allow_list.validate_and_quote(value)
                except ValueError as exc:
                    report.add(ValidationIssue(
                        "error", "sql_injection_risk",
                        f"Step {step.step_id}, param '{key}': {exc}",
                    ))

    def _check_expressions(self, step: ToolStep, specs: dict, is_qgis: bool,
                           report: ValidationReport) -> None:
        """QGIS expressions must parse; other expressions must be AST-safe (G12)."""
        from geosi_engine.base import get_expression_validator

        qgis_validator = get_expression_validator()
        for key, value in step.parameters.items():
            if not isinstance(value, str):
                continue
            ptype = getattr(specs.get(key), "param_type", "")
            if is_qgis and ptype:
                # Trust the algorithm's declared type: gdal:rastercalculator's
                # FORMULA is a numpy formula, not a QGIS expression
                is_expression = ptype == "expression"
            else:
                is_expression = ptype == "expression" or key.lower() in ("expression", "formula", "calc_expression")
            if not is_expression:
                continue
            if is_qgis:
                error = qgis_validator(value) if qgis_validator is not None else None
            else:
                try:
                    safe_evaluator.validate(value)
                    error = None
                except ValueError as exc:
                    error = str(exc)
            if error:
                report.add(ValidationIssue(
                    "error", "invalid_expression",
                    f"Step {step.step_id}, param '{key}': expression {value!r} is invalid: {error}",
                ))
