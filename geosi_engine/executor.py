"""
GeoSI Engine — Execution Engine

Runs an ExecutionPlan step by step, wiring the output of each step
to the input of the next. Records logs, handles errors, and produces
a final ExecutionResult.

See FILE_CONNECTIONS.md:
    - IMPORTS FROM: models.py, registry.py, state.py
    - USED BY: geosi_plugin/, geosi_server/
"""

import logging
import time
from typing import Any, Dict

from geosi_engine.models import (
    ExecutionPlan,
    ExecutionResult,
    ExecutionStatus,
    Layer,
    StepLog,
    ToolResult,
)
from geosi_engine.registry import ToolRegistry
from geosi_engine.state import StateManager

logger = logging.getLogger("geosi_engine.executor")


class ExecutionEngine:
    """
    Executes an ExecutionPlan step by step.

    The engine:
        1. Iterates through each ToolStep in the plan
        2. Resolves input layers from the state manager
        3. Calls the tool via the registry
        4. Stores the result in state for downstream steps
        5. Logs execution time and status

    Usage:
        engine = ExecutionEngine(registry, state)
        result = engine.execute(plan)
        print(result.answer)
    """

    def __init__(self, registry: ToolRegistry, state: StateManager):
        self.registry = registry
        self.state = state

    def execute_step(self, step, state: StateManager = None) -> ToolResult:
        """
        Execute a single ``ToolStep`` and persist its output.

        Factored out of :meth:`run` so callers that enforce their own control
        flow (the GIS Agent's permission gate) can drive the plan step-by-step.
        Resolves prior-step outputs and layer-name references the same way
        :meth:`run` does, calls the tool via the registry, and saves the result
        under ``step.output_name`` so downstream steps can reference it.

        Parameters
        ----------
        step:
            The ``ToolStep`` to execute.
        state:
            Session ``StateManager``. Defaults to the engine's own state.

        Returns
        -------
        ToolResult
        """
        st = state or self.state

        # Build parameters, resolving references the same way run() does
        resolved_params = dict(step.parameters)

        # Link previous step outputs by output_name
        for key, value in list(resolved_params.items()):
            if isinstance(value, str):
                prev_result = st.get_result(value) if hasattr(st, "get_result") else None
                if prev_result is not None:
                    if isinstance(prev_result, ToolResult) and prev_result.output:
                        resolved_params[key] = prev_result.output
                    else:
                        resolved_params[key] = prev_result

        # Resolve layer-name references from state
        for key, value in list(resolved_params.items()):
            if isinstance(value, str):
                layer = st.get_layer(value)
                if layer is not None:
                    resolved_params[key] = layer
            elif isinstance(value, list):
                new_list = []
                for item in value:
                    if isinstance(item, str):
                        layer = st.get_layer(item)
                        new_list.append(layer if layer is not None else item)
                    else:
                        new_list.append(item)
                resolved_params[key] = new_list

        tool_result = self.registry.execute_tool(step.tool_name, **resolved_params)

        if step.output_name:
            try:
                st.save_result(step.output_name, tool_result)
            except Exception as exc:  # pragma: no cover - defensive
                logger.debug("save_result failed for '%s': %s", step.output_name, exc)
        return tool_result

    def run(self, plan: ExecutionPlan, step_runner=None) -> ExecutionResult:
        """
        Execute all steps in the plan and return the final result.

        Args:
            plan: The ExecutionPlan with ordered ToolSteps.
            step_runner: Optional ``(step, state) -> ToolResult`` used instead
                of calling the registry directly — the agent pipeline passes
                ``GISAgent.execute_step`` so every step goes through the
                permission gate. It may raise an approval-pending error
                (has ``action_id``) to pause, or ``PermissionDeniedError``.

        Returns:
            ExecutionResult with answer, reasoning, logs, and outputs.
        """
        approval_pending = None
        denied = False
        # Mark start time for total execution duration
        total_start = time.time()
        # Track execution logs for each step
        logs = []
        # Store outputs keyed by output_name so downstream steps can reference them
        step_outputs: Dict[str, Any] = {}
        # Keep last result to generate final answer
        last_result = None
        # Track if all steps succeeded (vs. partial failure)
        all_success = True

        # Check if plan has no steps (validation error)
        if not plan.steps:
            total_elapsed = (time.time() - total_start) * 1000
            return ExecutionResult(
                success=False,
                answer=plan.reasoning or "No steps to execute",
                reasoning=plan.reasoning or "Execution plan is empty",
                error=plan.reasoning or "Execution plan produced no steps",
                results={},
                logs=[],
                total_duration_ms=total_elapsed,
            )

        logger.info(f"▶ Executing plan {plan.plan_id} ({len(plan.steps)} steps)")

        for step in plan.steps:
            # Track step timing
            step_start = time.time()
            logger.info(f"  Step {step.step_id}: {step.description}")

            # Build the parameters for this step, resolving references as needed
            resolved_params = dict(step.parameters)

            # Link previous step outputs: if a param value matches a prior step's
            # output_name, substitute the actual result
            for key, value in resolved_params.items():
                if isinstance(value, str) and value in step_outputs:
                    prev_result = step_outputs[value]
                    if isinstance(prev_result, ToolResult) and prev_result.output:
                        resolved_params[key] = prev_result.output
                    else:
                        resolved_params[key] = prev_result

            # Resolve layer references: if a string matches a loaded layer name,
            # fetch the Layer object from state
            for key, value in resolved_params.items():
                if isinstance(value, str):
                    layer = self.state.get_layer(value)
                    if layer is not None:
                        resolved_params[key] = layer
                elif isinstance(value, list):
                    # Resolve a list of layer names
                    new_list = []
                    for item in value:
                        if isinstance(item, str):
                            layer = self.state.get_layer(item)
                            new_list.append(layer if layer is not None else item)
                        else:
                            new_list.append(item)
                    resolved_params[key] = new_list

            # Call the tool (through the permission gate when a runner is set)
            try:
                if step_runner is not None:
                    tool_result = step_runner(step, self.state)
                else:
                    tool_result = self.registry.execute_tool(step.tool_name, **resolved_params)
            except Exception as exc:
                if getattr(exc, "action_id", None):
                    # Paused: a human must approve this step first
                    approval_pending = exc.action_id
                    logs.append(
                        StepLog(
                            step_id=step.step_id,
                            tool_name=step.tool_name,
                            status=ExecutionStatus.PENDING_APPROVAL,
                            duration_ms=(time.time() - step_start) * 1000,
                            error_message=str(exc),
                        )
                    )
                    all_success = False
                    break
                denied = type(exc).__name__ == "PermissionDeniedError"
                tool_result = ToolResult(
                    success=False, error=str(exc), message="Refused by policy" if denied else "Step raised an error"
                )

            # Compute execution time in milliseconds
            elapsed = (time.time() - step_start) * 1000

            # Store the result keyed by output_name for downstream steps to reference
            step_outputs[step.output_name] = tool_result
            self.state.save_result(step.output_name, tool_result)
            last_result = tool_result

            # Extract feature count if output is a Layer
            feature_count = 0
            if tool_result.output and isinstance(tool_result.output, Layer):
                feature_count = tool_result.output.feature_count

            # Create log entry with execution details
            log = StepLog(
                step_id=step.step_id,
                tool_name=step.tool_name,
                status=(ExecutionStatus.SUCCESS if tool_result.success else ExecutionStatus.FAILED),
                duration_ms=elapsed,
                output_features=feature_count,
                error_message=tool_result.error,
            )
            logs.append(log)
            self.state.log_step(log)

            # Mark success as false if any step fails, but continue execution
            # (partial results are better than aborting the plan)
            if not tool_result.success:
                all_success = False
                logger.warning(f"  ⚠ Step {step.step_id} failed: {tool_result.error}")
                if denied:
                    break  # a policy refusal ends the plan
                # Continue with remaining steps (partial execution)

        # Compute total execution time
        total_elapsed = (time.time() - total_start) * 1000

        # Generate human-readable answer and step-by-step reasoning
        answer = self._build_answer(plan, logs, last_result)
        reasoning = self._build_reasoning(plan, logs)
        if approval_pending:
            answer = (
                f"⏸ Approval required before continuing: approve or reject action " f"`{approval_pending}` to proceed."
            )
        elif denied:
            answer = f"⛔ Stopped by policy: {last_result.error if last_result else 'denied'}"

        # Extract final output layers that are ready to be returned to the user
        result_layers = {}
        for name, result in step_outputs.items():
            if isinstance(result, ToolResult):
                result_layers[name] = result.output

        # Set final status: SUCCESS if all steps passed, PARTIAL if some failed
        success = all_success
        status = ExecutionStatus.SUCCESS if all_success else ExecutionStatus.PARTIAL
        error = None
        # Collect error messages from all failed steps
        if not all_success:
            failed = [log for log in logs if log.status == ExecutionStatus.FAILED]
            error = "; ".join(f"{log.step_id}: {log.error_message}" for log in failed if log.error_message)

        logger.info(f"◼ Plan {plan.plan_id} {status.value} in {total_elapsed:.0f}ms")

        return ExecutionResult(
            success=success,
            answer=answer,
            reasoning=reasoning,
            error=error,
            results=result_layers,
            logs=logs,
            total_duration_ms=total_elapsed,
            approval_pending=approval_pending,
            denied=denied,
            plan_source=getattr(plan, "plan_source", ""),
        )

    # ── Answer generation ─────────────────────────────────────────────

    def _build_answer(self, plan: ExecutionPlan, logs: list, last_result: Any) -> str:
        """Generate a human-readable answer from execution results."""
        succeeded = sum(1 for log in logs if log.status == ExecutionStatus.SUCCESS)
        total = len(logs)

        if succeeded == total and last_result and last_result.success:
            msg = last_result.message or "Analysis completed successfully."
            return f"✅ {msg}"
        elif succeeded > 0:
            return f"⚠ Partial success: {succeeded}/{total} steps completed. " f"Check logs for details."
        else:
            return "❌ Analysis failed. Check error logs for details."

    def _build_reasoning(self, plan: ExecutionPlan, logs: list) -> str:
        """Build step-by-step reasoning from execution logs."""
        lines = [plan.reasoning, "", "Execution log:"]
        for log in logs:
            icon = "✅" if log.status == ExecutionStatus.SUCCESS else "❌"
            line = f"  {icon} {log.step_id} ({log.tool_name}): {log.duration_ms:.0f}ms"
            if log.output_features:
                line += f" → {log.output_features} features"
            if log.error_message:
                line += f" [ERROR: {log.error_message}]"
            lines.append(line)
        return "\n".join(lines)
