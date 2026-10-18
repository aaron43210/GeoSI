# -*- coding: utf-8 -*-
"""
GeoSI Knowledge — Query Memory
═══════════════════════════════════════════════════════════════════

Tracks user query patterns over time to:
    - Identify recurring query types
    - Infer user preferences (CRS, distance units, etc.)
    - Improve planning by recognizing patterns
    - Provide query suggestions

Storage: JSON file (~/.geosi/query_history.json) for persistence
across sessions + in-memory for fast lookup.
"""

import os
import json
import re
import logging
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

logger = logging.getLogger("geosi_knowledge.query_memory")

# Default storage path
_DEFAULT_HISTORY_DIR = os.path.expanduser("~/.geosi")
_DEFAULT_HISTORY_FILE = os.path.join(_DEFAULT_HISTORY_DIR, "query_history.json")


@dataclass
class QueryPattern:
    """
    A detected pattern in user queries.

    Attributes:
        pattern: The pattern description (e.g. "proximity_analysis")
        frequency: How many times this pattern has been seen
        last_seen: When this pattern was last matched
        avg_success_rate: Average success rate for this pattern
        example_queries: Example queries matching this pattern
    """
    pattern: str = ""
    frequency: int = 0
    last_seen: str = ""
    avg_success_rate: float = 1.0
    example_queries: List[str] = field(default_factory=list)

    def __repr__(self):
        return (
            f"QueryPattern({self.pattern}, freq={self.frequency}, "
            f"success={self.avg_success_rate:.0%})"
        )


@dataclass
class QueryRecord:
    """Internal record of a single query execution."""
    query: str
    intent: str = ""
    entities: Dict[str, Any] = field(default_factory=dict)
    status: str = "unknown"  # success, failed, partial
    tool_sequence: List[str] = field(default_factory=list)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class QueryMemory:
    """
    Tracks user query patterns over time.

    Usage:
        memory = QueryMemory()
        memory.record_query("Buffer hospitals by 500m", "proximity", {...}, "success")
        patterns = memory.get_patterns("Buffer schools by 1km")
        prefs = memory.get_user_preferences()
    """

    def __init__(self, history_file: Optional[str] = None):
        """
        Args:
            history_file: Path to JSON history file.
                          Default: ~/.geosi/query_history.json
        """
        self.history_file = history_file or _DEFAULT_HISTORY_FILE
        self._records: List[QueryRecord] = []
        self._max_records = 1000

        # Load existing history
        self._load_history()

    def record_query(
        self,
        query: str,
        intent: str = "",
        entities: Optional[Dict] = None,
        status: str = "unknown",
        tool_sequence: Optional[List[str]] = None,
    ) -> None:
        """
        Record a query execution.

        Args:
            query: The user's query text
            intent: Classified intent type
            entities: Extracted entities
            status: Execution status (success/failed/partial)
            tool_sequence: Tools used in execution
        """
        record = QueryRecord(
            query=query,
            intent=intent,
            entities=entities or {},
            status=status,
            tool_sequence=tool_sequence or [],
        )
        self._records.append(record)

        # Trim if over limit
        if len(self._records) > self._max_records:
            self._records = self._records[-self._max_records:]

        # Persist to disk
        self._save_history()

        logger.debug(f"Recorded query: '{query[:50]}...' ({intent}, {status})")

    def get_patterns(self, query: str) -> List[QueryPattern]:
        """
        Find patterns matching the current query.

        Analyzes query history to find similar past queries and
        their success rates.

        Args:
            query: Current query to match against.

        Returns:
            List of matching QueryPattern objects.
        """
        if not self._records:
            return []

        # Extract key terms from current query
        query_terms = set(self._extract_terms(query))
        if not query_terms:
            return []

        # Group records by intent and find matching patterns
        intent_groups: Dict[str, List[QueryRecord]] = {}
        for record in self._records:
            key = record.intent or "unknown"
            if key not in intent_groups:
                intent_groups[key] = []
            intent_groups[key].append(record)

        patterns = []
        for intent, records in intent_groups.items():
            # Check if any records share terms with current query
            matching = []
            for r in records:
                r_terms = set(self._extract_terms(r.query))
                overlap = query_terms & r_terms
                if len(overlap) >= 1:
                    matching.append(r)

            if matching:
                success_count = sum(1 for r in matching if r.status == "success")
                total = len(matching)
                success_rate = success_count / total if total > 0 else 0.0

                pattern = QueryPattern(
                    pattern=intent,
                    frequency=total,
                    last_seen=matching[-1].timestamp,
                    avg_success_rate=success_rate,
                    example_queries=[r.query for r in matching[-3:]],
                )
                patterns.append(pattern)

        # Sort by frequency descending
        patterns.sort(key=lambda p: p.frequency, reverse=True)
        return patterns

    def get_frequent_operations(self) -> Dict[str, int]:
        """
        Get most common operations/intents from query history.

        Returns:
            Dict mapping operation → count, sorted by frequency.
        """
        counter = Counter()
        for record in self._records:
            if record.intent:
                counter[record.intent] += 1
            for tool in record.tool_sequence:
                clean_tool = tool.replace("native_", "").replace("gdal_", "")
                counter[clean_tool] += 1

        return dict(counter.most_common(20))

    def get_user_preferences(self) -> Dict[str, Any]:
        """
        Infer user preferences from query history.

        Analyzes patterns like:
            - Preferred CRS (most commonly used)
            - Default distance units
            - Most used layer types
            - Common operation patterns

        Returns:
            Dict of inferred preferences.
        """
        preferences: Dict[str, Any] = {}

        if not self._records:
            return preferences

        # Analyze CRS preferences
        crs_counter = Counter()
        for record in self._records:
            entities = record.entities or {}
            if "crs" in entities:
                crs_counter[entities["crs"]] += 1
            # Check query for EPSG codes
            epsg_matches = re.findall(r"EPSG:\d+", record.query, re.IGNORECASE)
            for epsg in epsg_matches:
                crs_counter[epsg.upper()] += 1

        if crs_counter:
            preferences["preferred_crs"] = crs_counter.most_common(1)[0][0]

        # Analyze distance unit preferences
        distance_units = Counter()
        for record in self._records:
            query_lower = record.query.lower()
            if "km" in query_lower or "kilometer" in query_lower:
                distance_units["km"] += 1
            elif "meter" in query_lower or " m " in query_lower:
                distance_units["m"] += 1
            elif "mile" in query_lower:
                distance_units["miles"] += 1
            elif "feet" in query_lower or " ft " in query_lower:
                distance_units["feet"] += 1

        if distance_units:
            preferences["preferred_distance_unit"] = distance_units.most_common(1)[0][0]

        # Most common operations
        preferences["frequent_operations"] = self.get_frequent_operations()

        # Total queries
        preferences["total_queries"] = len(self._records)
        success = sum(1 for r in self._records if r.status == "success")
        preferences["overall_success_rate"] = success / len(self._records)

        return preferences

    def get_recent_queries(self, limit: int = 10) -> List[str]:
        """Get the most recent queries."""
        return [r.query for r in self._records[-limit:]]

    # ── Persistence ────────────────────────────────────────────────────

    def _save_history(self) -> None:
        """Save query history to JSON file."""
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)

            data = [
                {
                    "query": r.query,
                    "intent": r.intent,
                    "entities": r.entities,
                    "status": r.status,
                    "tool_sequence": r.tool_sequence,
                    "timestamp": r.timestamp,
                }
                for r in self._records
            ]

            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)

        except Exception as e:
            logger.debug(f"Failed to save query history: {e}")

    def _load_history(self) -> None:
        """Load query history from JSON file."""
        if not os.path.exists(self.history_file):
            return

        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            self._records = [
                QueryRecord(
                    query=r.get("query", ""),
                    intent=r.get("intent", ""),
                    entities=r.get("entities", {}),
                    status=r.get("status", "unknown"),
                    tool_sequence=r.get("tool_sequence", []),
                    timestamp=r.get("timestamp", ""),
                )
                for r in data
            ]
            logger.info(f"Loaded {len(self._records)} query records from history")

        except Exception as e:
            logger.debug(f"Failed to load query history: {e}")

    @staticmethod
    def _extract_terms(text: str) -> List[str]:
        """Extract meaningful terms from text for pattern matching."""
        stop_words = {
            "the", "a", "an", "is", "are", "was", "to", "of", "in",
            "for", "on", "with", "at", "by", "from", "and", "or",
            "not", "this", "that", "it", "as", "do", "how", "what",
            "can", "will", "all", "my", "me", "we", "you",
        }
        tokens = re.findall(r"\b[a-zA-Z0-9_]+\b", text.lower())
        return [t for t in tokens if t not in stop_words and len(t) > 2]

    def __len__(self):
        return len(self._records)

    def __repr__(self):
        return f"QueryMemory(records={len(self._records)})"
