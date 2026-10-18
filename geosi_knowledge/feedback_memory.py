# -*- coding: utf-8 -*-
"""
GeoSI Knowledge — Feedback Memory
═══════════════════════════════════════════════════════════════════

Learns from execution success/failure to:
    - Track per-tool reliability (success rate)
    - Identify common failure patterns
    - Suggest workarounds for known issues
    - Guide the planning agent away from unreliable paths
"""

import os
import json
import logging
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

logger = logging.getLogger("geosi_knowledge.feedback_memory")

_DEFAULT_FEEDBACK_DIR = os.path.expanduser("~/.geosi")
_DEFAULT_FEEDBACK_FILE = os.path.join(_DEFAULT_FEEDBACK_DIR, "feedback_history.json")


@dataclass
class FeedbackSignal:
    """
    A feedback signal from a past execution.

    Attributes:
        query: Original query
        tool_sequence: Tools used
        success: Whether execution succeeded
        error_type: Classification of error (if failed)
        suggestion: Workaround or suggestion
        timestamp: When this feedback was recorded
    """
    query: str = ""
    tool_sequence: List[str] = field(default_factory=list)
    success: bool = True
    error_type: Optional[str] = None
    suggestion: Optional[str] = None
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def __repr__(self):
        status = "✅" if self.success else f"❌ {self.error_type}"
        tools = " → ".join(self.tool_sequence) if self.tool_sequence else "N/A"
        return f"FeedbackSignal({status}, tools=[{tools}])"


@dataclass
class FailurePattern:
    """
    A recurring failure pattern.

    Attributes:
        tool_name: Tool that fails
        error_type: Type of error
        frequency: How many times this has occurred
        workaround: Known workaround (if any)
        example_queries: Queries that triggered this failure
    """
    tool_name: str = ""
    error_type: str = ""
    frequency: int = 0
    workaround: Optional[str] = None
    example_queries: List[str] = field(default_factory=list)

    def __repr__(self):
        return (
            f"FailurePattern(tool={self.tool_name}, "
            f"error={self.error_type}, freq={self.frequency})"
        )


class FeedbackMemory:
    """
    Learns from execution success/failure.

    Tracks per-tool reliability and identifies failure patterns
    to help the planning agent make better decisions.

    Usage:
        memory = FeedbackMemory()
        memory.record_feedback(query, plan, result, success=False, error_type="missing_layer")
        reliability = memory.get_tool_reliability()
        failures = memory.get_failure_patterns()
    """

    def __init__(self, feedback_file: Optional[str] = None):
        """
        Args:
            feedback_file: Path to JSON feedback file.
                           Default: ~/.geosi/feedback_history.json
        """
        self.feedback_file = feedback_file or _DEFAULT_FEEDBACK_FILE
        self._signals: List[FeedbackSignal] = []
        self._max_signals = 500

        # Per-tool statistics (tool_name → {success: int, fail: int})
        self._tool_stats: Dict[str, Dict[str, int]] = defaultdict(
            lambda: {"success": 0, "fail": 0}
        )

        # Error pattern tracking (error_type → count)
        self._error_patterns: Dict[str, List[Dict]] = defaultdict(list)

        # Load existing feedback
        self._load_feedback()

    def record_feedback(
        self,
        query: str,
        plan: Any,
        result: Any,
        success: bool,
        error_type: Optional[str] = None,
    ) -> FeedbackSignal:
        """
        Record feedback from an execution.

        Args:
            query: Original user query
            plan: ExecutionPlan object
            result: ExecutionResult object
            success: Whether execution succeeded
            error_type: Classification of error (auto-detected if not provided)

        Returns:
            The recorded FeedbackSignal.
        """
        # Extract tool sequence
        tool_sequence = []
        if plan and hasattr(plan, "steps"):
            tool_sequence = [s.tool_name for s in plan.steps]

        # Auto-detect error type if not provided
        if not success and not error_type:
            error_type = self._classify_error(result)

        # Build suggestion based on error type
        suggestion = self._generate_suggestion(error_type, tool_sequence)

        signal = FeedbackSignal(
            query=query,
            tool_sequence=tool_sequence,
            success=success,
            error_type=error_type,
            suggestion=suggestion,
        )

        # Store signal
        self._signals.append(signal)
        if len(self._signals) > self._max_signals:
            self._signals = self._signals[-self._max_signals:]

        # Update per-tool statistics
        for tool in tool_sequence:
            if success:
                self._tool_stats[tool]["success"] += 1
            else:
                self._tool_stats[tool]["fail"] += 1

        # Track error pattern
        if error_type:
            self._error_patterns[error_type].append({
                "query": query,
                "tools": tool_sequence,
                "timestamp": signal.timestamp,
            })

        # Persist
        self._save_feedback()

        logger.debug(
            f"Feedback recorded: {'✅' if success else '❌'} "
            f"query='{query[:50]}...', error={error_type}"
        )
        return signal

    def get_relevant_feedback(
        self,
        query: str,
        limit: int = 5,
    ) -> List[FeedbackSignal]:
        """
        Retrieve feedback signals relevant to a query.

        Searches for past feedback with similar queries or tool sequences.

        Args:
            query: Current query
            limit: Maximum results

        Returns:
            List of relevant FeedbackSignal objects.
        """
        if not self._signals:
            return []

        import re
        query_terms = set(re.findall(r"\b\w{3,}\b", query.lower()))
        stop_words = {
            "the", "and", "for", "from", "with", "this", "that",
            "are", "was", "will", "can", "how", "what",
        }
        query_terms -= stop_words

        scored = []
        for signal in self._signals:
            signal_terms = set(re.findall(r"\b\w{3,}\b", signal.query.lower()))
            signal_terms -= stop_words
            overlap = query_terms & signal_terms
            if overlap:
                score = len(overlap) / max(len(query_terms), 1)
                scored.append((score, signal))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [signal for _, signal in scored[:limit]]

    def get_tool_reliability(
        self, tool_name: Optional[str] = None
    ) -> Any:
        """
        Get success rate per tool.

        Args:
            tool_name: If given, return that single tool's success rate as a
                       float (or ``None`` when the tool has no history).
                       If omitted, return the full ``{tool_name: rate}`` dict.

        Returns:
            ``float | None`` when *tool_name* is supplied, otherwise a
            ``Dict[str, float]`` mapping tool_name → success_rate (0.0–1.0),
            sorted ascending by rate.
        """
        reliability = {}
        for tool, stats in self._tool_stats.items():
            total = stats["success"] + stats["fail"]
            if total > 0:
                reliability[tool] = stats["success"] / total

        if tool_name is not None:
            return reliability.get(tool_name)

        return dict(sorted(reliability.items(), key=lambda x: x[1]))

    def get_failure_patterns(self) -> List[FailurePattern]:
        """
        Get common failure patterns.

        Returns:
            List of FailurePattern objects, sorted by frequency.
        """
        patterns = []

        # Analyze per-error-type patterns
        for error_type, occurrences in self._error_patterns.items():
            # Find most common tool in this error type
            tool_counter = Counter()
            for occ in occurrences:
                for tool in occ.get("tools", []):
                    tool_counter[tool] += 1

            most_common_tool = tool_counter.most_common(1)
            tool_name = most_common_tool[0][0] if most_common_tool else "unknown"

            pattern = FailurePattern(
                tool_name=tool_name,
                error_type=error_type,
                frequency=len(occurrences),
                workaround=self._generate_suggestion(error_type, [tool_name]),
                example_queries=[
                    occ["query"] for occ in occurrences[-3:]
                ],
            )
            patterns.append(pattern)

        patterns.sort(key=lambda p: p.frequency, reverse=True)
        return patterns

    def get_tool_warnings(self, tool_names: List[str]) -> List[str]:
        """
        Get warnings for specific tools based on past failures.

        Used by the planning agent to check if proposed tools
        have known issues.
        """
        warnings = []
        reliability = self.get_tool_reliability()

        for tool in tool_names:
            rate = reliability.get(tool)
            if rate is not None and rate < 0.5:
                warnings.append(
                    f"⚠ Tool '{tool}' has a {rate:.0%} success rate "
                    f"based on {self._tool_stats[tool]['success'] + self._tool_stats[tool]['fail']} executions"
                )

        return warnings

    # ── Private helpers ────────────────────────────────────────────────

    @staticmethod
    def _classify_error(result: Any) -> str:
        """Auto-classify an error from an ExecutionResult."""
        if result is None:
            return "null_result"

        error = getattr(result, "error", "") or ""
        error_lower = error.lower()

        if "not found" in error_lower or "no such" in error_lower:
            return "missing_layer"
        elif "parameter" in error_lower or "missing" in error_lower:
            return "missing_parameter"
        elif "crs" in error_lower or "projection" in error_lower:
            return "crs_mismatch"
        elif "memory" in error_lower or "oom" in error_lower:
            return "out_of_memory"
        elif "timeout" in error_lower:
            return "timeout"
        elif "permission" in error_lower:
            return "permission_denied"
        elif "tool" in error_lower and "not found" in error_lower:
            return "unknown_tool"
        else:
            return "unknown_error"

    @staticmethod
    def _generate_suggestion(
        error_type: Optional[str],
        tools: List[str],
    ) -> Optional[str]:
        """Generate a suggestion based on error type."""
        suggestions = {
            "missing_layer": "Ensure the layer is loaded in the workspace before running the workflow.",
            "missing_parameter": "Check that all required parameters are provided in the query.",
            "crs_mismatch": "Reproject layers to the same CRS before overlay operations.",
            "out_of_memory": "Try processing a smaller extent or lower resolution.",
            "timeout": "The operation timed out. Try with a smaller dataset.",
            "permission_denied": "Check file permissions on input/output paths.",
            "unknown_tool": "The requested tool is not available. Check tool registration.",
        }
        return suggestions.get(error_type)

    # ── Persistence ────────────────────────────────────────────────────

    def _save_feedback(self) -> None:
        """Save feedback history to JSON file."""
        try:
            os.makedirs(os.path.dirname(self.feedback_file), exist_ok=True)

            data = {
                "signals": [
                    {
                        "query": s.query,
                        "tool_sequence": s.tool_sequence,
                        "success": s.success,
                        "error_type": s.error_type,
                        "suggestion": s.suggestion,
                        "timestamp": s.timestamp,
                    }
                    for s in self._signals
                ],
                "tool_stats": dict(self._tool_stats),
            }

            with open(self.feedback_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)

        except Exception as e:
            logger.debug(f"Failed to save feedback: {e}")

    def _load_feedback(self) -> None:
        """Load feedback history from JSON file."""
        if not os.path.exists(self.feedback_file):
            return

        try:
            with open(self.feedback_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Load signals
            for s in data.get("signals", []):
                signal = FeedbackSignal(
                    query=s.get("query", ""),
                    tool_sequence=s.get("tool_sequence", []),
                    success=s.get("success", True),
                    error_type=s.get("error_type"),
                    suggestion=s.get("suggestion"),
                    timestamp=s.get("timestamp", ""),
                )
                self._signals.append(signal)

                # Rebuild error patterns
                if signal.error_type:
                    self._error_patterns[signal.error_type].append({
                        "query": signal.query,
                        "tools": signal.tool_sequence,
                        "timestamp": signal.timestamp,
                    })

            # Load tool stats
            for tool, stats in data.get("tool_stats", {}).items():
                self._tool_stats[tool] = stats

            logger.info(f"Loaded {len(self._signals)} feedback records")

        except Exception as e:
            logger.debug(f"Failed to load feedback: {e}")

    def __len__(self):
        return len(self._signals)

    def __repr__(self):
        return f"FeedbackMemory(signals={len(self._signals)}, tools={len(self._tool_stats)})"
