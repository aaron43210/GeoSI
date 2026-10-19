"""
Check whether GeoSI can reach a language model, and explain how to fix it if not.

``check_llm(agent)`` looks at the hosted OpenAI-compatible API first (when one
is configured), then local Ollama, and returns an ``LLMStatus`` saying which
model will answer, or which problem stops it and the exact fix.
"""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Tuple

logger = logging.getLogger("geosi_engine.llm_status")

# (url, headers, timeout) -> (http_status, body); raises OSError when unreachable
Fetch = Callable[[str, dict, float], Tuple[int, bytes]]

# Installed-model preference when the configured Ollama model is missing
PREFERRED_OLLAMA = ["llama3.2:3b", "llama3.2", "llama3:latest", "llama3", "qwen2.5-coder:14b", "qwen2.5", "mistral"]


@dataclass
class LLMStatus:
    ok: bool
    provider: str = "none"  # "api" | "ollama" | "none"
    model: str = ""
    problem: str = ""
    title: str = ""
    fix: str = ""
    note: str = ""

    @property
    def label(self) -> str:
        if not self.ok:
            return "Not connected"
        where = "Ollama" if self.provider == "ollama" else _host(self.model_source)
        return f"{self.model} · {where}"

    model_source: str = ""


def _reason(exc: Exception) -> str:
    """Short, human wording for a network failure."""
    text = str(getattr(exc, "reason", exc)).lower()
    if "refused" in text:
        return "nothing is answering at that address"
    if "timed out" in text or "timeout" in text:
        return "it did not answer in time"
    if "name or service" in text or "nodename" in text or "getaddrinfo" in text:
        return "that host name could not be found"
    if "certificate" in text or "ssl" in text:
        return "the secure connection failed (certificate or proxy problem)"
    return str(getattr(exc, "reason", exc))


def _host(url: str) -> str:
    return urllib.parse.urlparse(url).hostname or url or "API"


def _default_fetch(url: str, headers: dict, timeout: float) -> Tuple[int, bytes]:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec B310 — http(s) endpoints from settings
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, b""


def _is_local(url: str) -> bool:
    return _host(url) in ("localhost", "127.0.0.1", "::1", "0.0.0.0")  # noqa: S104  # nosec B104 — comparison only


def _same_model(a: str, b: str) -> bool:
    def norm(m: str) -> str:
        return m[:-7] if m.endswith(":latest") else m

    return norm(a) == norm(b)


def check_api(agent: Any, fetch: Fetch, timeout: float) -> LLMStatus:
    base = (getattr(agent, "_api_base", "") or "").rstrip("/")
    model = getattr(agent, "_api_model", "") or ""
    key = getattr(agent, "_api_key", "") or ""
    host = _host(base)
    if not model:
        return LLMStatus(
            False,
            "api",
            problem="api_no_model",
            title=f"No model chosen for {host}",
            fix="Open Settings and pick a model for the hosted API.",
            model_source=base,
        )
    if not key and not _is_local(base):
        return LLMStatus(
            False,
            "api",
            model,
            "api_no_key",
            f"No API key for {host}",
            "Open Settings and paste your API key. It is stored encrypted in the " "QGIS authentication database.",
            model_source=base,
        )
    headers = {"Authorization": f"Bearer {key}"} if key else {}
    try:
        status, body = fetch(f"{base}/models", headers, timeout)
    except Exception as exc:  # noqa: BLE001 — any network failure means unreachable
        return LLMStatus(
            False,
            "api",
            model,
            "api_unreachable",
            f"Can't reach {host}",
            f"Check your internet connection or proxy, and the API URL in Settings ({_reason(exc)}).",
            model_source=base,
        )
    if status in (401, 403):
        return LLMStatus(
            False,
            "api",
            model,
            "api_bad_key",
            f"{host} rejected the API key",
            "Open Settings and paste a valid API key.",
            model_source=base,
        )
    if status != 200:
        return LLMStatus(
            False,
            "api",
            model,
            "api_error",
            f"{host} answered HTTP {status}",
            "Check the API URL in Settings, or try again in a moment.",
            model_source=base,
        )
    try:
        ids = [m.get("id", "") for m in json.loads(body or b"{}").get("data", [])]
    except (ValueError, AttributeError):
        ids = []
    if ids and model not in ids:
        sample = ", ".join(sorted(ids)[:5])
        return LLMStatus(
            False,
            "api",
            model,
            "api_model_missing",
            f"Model '{model}' isn't available on {host}",
            f"Pick an available model in Settings, for example: {sample}.",
            model_source=base,
        )
    return LLMStatus(True, "api", model, title=f"Connected to {model}", model_source=base)


def _ollama_models(endpoint: str, fetch: Fetch, timeout: float) -> Tuple[Optional[List[str]], str]:
    try:
        status, body = fetch(f"{endpoint}/api/tags", {}, timeout)
    except Exception as exc:  # noqa: BLE001
        return None, _reason(exc)
    if status != 200:
        return None, f"HTTP {status}"
    try:
        names = [m.get("name", "") for m in json.loads(body or b"{}").get("models", [])]
    except (ValueError, AttributeError):
        return None, "unexpected response"
    # Embedding-only models cannot plan or chat
    return [n for n in names if n and "embed" not in n], ""


def check_ollama(agent: Any, fetch: Fetch, timeout: float) -> LLMStatus:
    endpoint = (getattr(agent, "_ollama_endpoint", "") or "http://localhost:11434").rstrip("/")
    wanted = getattr(agent, "_ollama_model", "") or ""
    models, err = _ollama_models(endpoint, fetch, timeout)
    if models is None:
        return LLMStatus(
            False,
            "ollama",
            wanted,
            "ollama_unreachable",
            f"Ollama isn't reachable at {endpoint}",
            (f"Checked {endpoint}: {err}. " if err else "")
            + "Start Ollama (run `ollama serve`, or open the Ollama app; install it from "
            "https://ollama.com), or add a hosted API key in Settings.",
            model_source=endpoint,
        )
    if not models:
        return LLMStatus(
            False,
            "ollama",
            wanted,
            "ollama_no_models",
            "Ollama is running but has no chat model",
            "Download one with `ollama pull llama3.2`, then press Check again.",
            model_source=endpoint,
        )
    match = next((m for m in models if wanted and _same_model(m, wanted)), None)
    if match:
        return LLMStatus(True, "ollama", match, title=f"Connected to {match}", model_source=endpoint)
    chosen = next((m for p in PREFERRED_OLLAMA for m in models if _same_model(m, p)), models[0])
    note = (
        f"'{wanted}' isn't installed, so GeoSI uses '{chosen}'. Run `ollama pull {wanted}` to use it." if wanted else ""
    )
    return LLMStatus(True, "ollama", chosen, title=f"Connected to {chosen}", note=note, model_source=endpoint)


def check_llm(agent: Any, fetch: Optional[Fetch] = None, timeout: float = 3.0) -> LLMStatus:
    """Hosted API first when configured, then local Ollama (same order the planner uses)."""
    fetch = fetch or _default_fetch
    api = None
    if getattr(agent, "_api_base", ""):
        api = check_api(agent, fetch, timeout)
        if api.ok:
            return api
    ollama = check_ollama(agent, fetch, timeout)
    if ollama.ok:
        if api is not None:
            ollama.note = f"{api.title}. Using local Ollama instead. " + ollama.note
        return ollama
    if api is not None:
        api.fix += f" (Local Ollama isn't available either: {ollama.title.lower()}.)"
        return api
    return ollama
