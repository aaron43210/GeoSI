# -*- coding: utf-8 -*-
"""
GeoSI — AST Code Sandbox & Security Guard
══════════════════════════════════════════════════════════════════════
Statically analyses Python code before execution to block dangerous
calls that an LLM might generate accidentally or maliciously.

Usage:
    from geosi_engine.security import ASTGuard

    ok, violations = ASTGuard.check(code_string)
    if not ok:
        raise PermissionError(f"Blocked: {violations}")

The guard is conservative by default — better to block a safe snippet
than to execute a harmful one. It does NOT execute the code.
"""
from __future__ import annotations

import ast
import logging
import re
from typing import List, Tuple

logger = logging.getLogger("geosi_engine.security")

# ── Blocked module names ───────────────────────────────────────────────
BLOCKED_MODULES = frozenset({
    "os", "subprocess", "sys", "ctypes", "socket",
    "threading", "multiprocessing", "signal",
    "importlib", "importlib.util",
    "builtins", "gc", "inspect",
    "pty", "popen2", "commands",
    "winreg", "winreg", "msvcrt",
})

# Specific attribute accesses to block (module.attr)
BLOCKED_ATTRS = frozenset({
    "os.system", "os.popen", "os.execv", "os.execve", "os.fork",
    "os.kill", "os.remove", "os.unlink", "os.rmdir", "os.removedirs",
    "os.rename", "os.replace",
    "subprocess.run", "subprocess.Popen", "subprocess.call",
    "subprocess.check_output",
    "ctypes.cdll", "ctypes.windll",
    "socket.socket",
})

# Blocked built-in function calls
BLOCKED_BUILTINS = frozenset({
    "eval", "exec", "compile", "__import__",
    "open",    # allow only explicit allowlisted paths — blocked by default
    "input",
})

# Blocked dunder names
BLOCKED_DUNDERS = frozenset({
    "__subclasses__", "__bases__", "__mro__",
    "__class__", "__globals__", "__builtins__",
    "__code__", "__func__",
})

# Regex for dangerous string patterns even in comments/strings
_DANGEROUS_PATTERNS = [
    re.compile(r"rm\s+-rf\s+/"),
    re.compile(r"shutil\.rmtree\(.*[/\\]"),
    re.compile(r"DROP\s+TABLE", re.IGNORECASE),
    re.compile(r"DELETE\s+FROM", re.IGNORECASE),
    re.compile(r"authManager\(\)"),
]


class _Visitor(ast.NodeVisitor):
    """AST visitor that collects security violations."""

    def __init__(self, allow_open: bool = False) -> None:
        self.violations: List[str] = []
        self._allow_open = allow_open

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            root = alias.name.split(".")[0]
            if root in BLOCKED_MODULES:
                self.violations.append(
                    f"line {node.lineno}: blocked import '{alias.name}'"
                )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        mod = (node.module or "").split(".")[0]
        if mod in BLOCKED_MODULES:
            self.violations.append(
                f"line {node.lineno}: blocked import from '{node.module}'"
            )
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        name = self._call_name(node.func)
        if name:
            if name in BLOCKED_BUILTINS:
                if name == "open" and self._allow_open:
                    pass
                else:
                    self.violations.append(
                        f"line {node.lineno}: blocked call to '{name}()'"
                    )
            if name in BLOCKED_ATTRS:
                self.violations.append(
                    f"line {node.lineno}: blocked call to '{name}()'"
                )
            for dunder in BLOCKED_DUNDERS:
                if dunder in name:
                    self.violations.append(
                        f"line {node.lineno}: blocked dunder '{name}'"
                    )
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if node.attr in BLOCKED_DUNDERS:
            self.violations.append(
                f"line {node.lineno}: blocked attribute '{node.attr}'"
            )
        self.generic_visit(node)

    @staticmethod
    def _call_name(func: ast.expr) -> str:
        if isinstance(func, ast.Name):
            return func.id
        if isinstance(func, ast.Attribute):
            parent = _Visitor._call_name(func.value)
            return f"{parent}.{func.attr}" if parent else func.attr
        return ""


class ASTGuard:
    """
    Static security analyser for LLM-generated Python code.

    Call ``ASTGuard.check(code)`` before executing any generated script.
    """

    @staticmethod
    def check(code: str, allow_open: bool = False) -> Tuple[bool, List[str]]:
        """
        Parse and inspect *code*.

        Returns (is_safe, violations).
        ``is_safe`` is True when no violations were found.
        ``violations`` is a list of human-readable problem descriptions.
        """
        violations: List[str] = []

        # 1. Syntax check
        try:
            tree = ast.parse(code, filename="<generated>")
        except SyntaxError as exc:
            return False, [f"Syntax error: {exc}"]

        # 2. AST walk
        visitor = _Visitor(allow_open=allow_open)
        visitor.visit(tree)
        violations.extend(visitor.violations)

        # 3. Regex patterns on raw source
        for pat in _DANGEROUS_PATTERNS:
            if pat.search(code):
                violations.append(f"Blocked pattern: {pat.pattern!r}")

        is_safe = len(violations) == 0
        if not is_safe:
            logger.warning("ASTGuard blocked %d violation(s):\n%s",
                           len(violations), "\n".join(f"  • {v}" for v in violations))
        return is_safe, violations

    @staticmethod
    def safe_exec(code: str, globals_: dict, locals_: dict, allow_open: bool = False) -> Tuple[bool, str]:
        """
        Check *code* with ASTGuard then execute it.

        Returns (success, error_message).
        """
        ok, violations = ASTGuard.check(code, allow_open=allow_open)
        if not ok:
            msg = "Code blocked by ASTGuard:\n" + "\n".join(f"  • {v}" for v in violations)
            return False, msg
        try:
            exec(compile(code, "<generated>", "exec"), globals_, locals_)  # noqa: S102
            return True, ""
        except Exception as exc:
            return False, str(exc)
