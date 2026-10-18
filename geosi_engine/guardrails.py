# -*- coding: utf-8 -*-
"""
GeoSI v2 — Guardrails
══════════════════════════════════════════════════════════════════════
Scans text for prompt-injection patterns before it enters any agent's
planning prompt.

Design (PRD FR-3.1)
--------------------
* Content retrieved from Qdrant is **annotated**, not silently stripped.
  The calling agent receives a ``GuardrailResult`` and decides how to
  react — this makes the guardrail transparent and auditable.
* Pattern matching uses both exact-string containment and compiled
  regex for flexibility.  The corpus covers ≥ 20 known injection
  phrases sourced from OWASP Agentic Top-10 2026 guidance.

Usage
-----
::

    from geosi_engine.guardrails import scan_text

    result = scan_text(retrieved_chunk)
    if not result.is_clean:
        logger.warning("Guardrail flags: %s", result.flags)
        # attach flags to context object; do not silently trust
"""
from __future__ import annotations

import re
import logging
from dataclasses import dataclass, field

logger = logging.getLogger("geosi_engine.guardrails")


# ---------------------------------------------------------------------------
# Pattern corpus — extend here; keep lowercase for case-insensitive matching
# ---------------------------------------------------------------------------

# Literal substring patterns (fast path, case-insensitive)
_LITERAL_PATTERNS: list[str] = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "ignore the above",
    "disregard previous instructions",
    "disregard all instructions",
    "forget previous instructions",
    "override your instructions",
    "you are now",
    "act as if",
    "pretend you are",
    "pretend to be",
    "your new role is",
    "from now on you are",
    "new persona",
    "new system prompt",
    "system prompt:",
    "### system",
    "[system]",
    "<system>",
    "jailbreak",
    "you have no restrictions",
    "you have no limitations",
    "do anything now",
    "dan mode",
    "developer mode enabled",
    "sudo mode",
    "god mode",
]

# Regex patterns for more nuanced detection
_REGEX_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"(?i)ignore\s+(all\s+)?(?:previous|prior|above|earlier)\s+\w+"),
    re.compile(r"(?i)you\s+are\s+(now\s+)?(?:a|an|the)\s+\w+\s+(assistant|agent|bot|ai)"),
    re.compile(r"(?i)role\s*[:=]\s*(?:system|admin|root|developer|owner)"),
    re.compile(r"(?i)\[\s*(?:system|admin|root)\s*\]"),
    re.compile(r"(?i)<\s*(?:system|prompt|instruction)\s*>"),
    re.compile(r"(?i)###\s*(?:system|instruction|prompt|override)"),
]


@dataclass
class GuardrailResult:
    """
    Result of a guardrail scan.

    Attributes
    ----------
    flags:
        List of triggered pattern descriptions (empty means clean).
    is_clean:
        ``True`` when no injection patterns were detected.
    """

    flags: list[str] = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        return len(self.flags) == 0

    def __repr__(self) -> str:
        if self.is_clean:
            return "GuardrailResult(clean)"
        return f"GuardrailResult(flags={self.flags!r})"


# ---------------------------------------------------------------------------
# Aho-Corasick automaton — O(T) multi-pattern scan (vs O(P×T) naive loop)
# Built once at module load from _LITERAL_PATTERNS. Falls back to linear scan
# if pyahocorasick is not installed.
# ---------------------------------------------------------------------------
_AHO_AUTOMATON = None
try:
    import ahocorasick
    _AHO_AUTOMATON = ahocorasick.Automaton()
    for _idx, _pat in enumerate(_LITERAL_PATTERNS):
        _AHO_AUTOMATON.add_word(_pat, (_idx, _pat))
    _AHO_AUTOMATON.make_automaton()
except ImportError:
    pass  # Falls back to O(P×T) loop below


def scan_text(text: str) -> GuardrailResult:
    """
    Scan *text* for known prompt-injection patterns.

    Time complexity:
        O(T + M) with Aho-Corasick (T = text length, M = match count)
        O(P × T) fallback when pyahocorasick is not installed

    Parameters
    ----------
    text:
        Any string — typically a RAG-retrieved document chunk, tool
        description, or user query fragment.

    Returns
    -------
    GuardrailResult
        Contains a list of triggered pattern descriptions.
        ``result.is_clean`` is ``True`` when no patterns fire.
    """
    if not text:
        return GuardrailResult()

    flags: list[str] = []
    lowered = text.lower()

    # Fast path: Aho-Corasick O(T) single-pass scan over all literal patterns
    if _AHO_AUTOMATON is not None:
        for _, (_idx, pattern) in _AHO_AUTOMATON.iter(lowered):
            flags.append(f"literal:{pattern!r}")
    else:
        # Fallback: O(P × T) linear scan
        for pattern in _LITERAL_PATTERNS:
            if pattern in lowered:
                flags.append(f"literal:{pattern!r}")

    # Regex patterns — always O(T) per pattern (compiled at module load)
    for rx in _REGEX_PATTERNS:
        match = rx.search(text)
        if match:
            flags.append(f"regex:{rx.pattern!r} matched {match.group()!r}")

    if flags:
        logger.warning(
            "Guardrail triggered (%d flag(s)): %s",
            len(flags),
            "; ".join(flags[:3]) + ("…" if len(flags) > 3 else ""),
        )

    return GuardrailResult(flags=flags)


def scan_chunks(chunks: list[str]) -> list[GuardrailResult]:
    """
    Scan a list of text chunks (e.g. RAG-retrieved snippets) and return
    one ``GuardrailResult`` per chunk.
    """
    return [scan_text(chunk) for chunk in chunks]
