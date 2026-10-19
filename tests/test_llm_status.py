"""LLM connection check: every failure mode maps to a specific, fixable message."""

import json
from types import SimpleNamespace

from geosi_engine.llm_status import check_llm

OLLAMA = "http://localhost:11434"
GROQ = "https://api.groq.com/openai/v1"


def agent(api_base="", api_model="", api_key="", ollama_model="llama3.2:3b"):
    return SimpleNamespace(
        _api_base=api_base, _api_model=api_model, _api_key=api_key, _ollama_endpoint=OLLAMA, _ollama_model=ollama_model
    )


def net(routes):
    """routes: url -> (status, payload) or an exception instance."""
    seen = []

    def fetch(url, headers, timeout):
        seen.append((url, headers))
        r = routes.get(url, OSError("connection refused"))
        if isinstance(r, Exception):
            raise r
        status, payload = r
        return status, json.dumps(payload).encode()

    fetch.seen = seen
    return fetch


def tags(*names):
    return 200, {"models": [{"name": n} for n in names]}


def test_ollama_connected_with_configured_model():
    s = check_llm(agent(), net({f"{OLLAMA}/api/tags": tags("llama3.2:3b")}))
    assert s.ok and s.provider == "ollama" and s.model == "llama3.2:3b"
    assert s.label == "llama3.2:3b · Ollama"


def test_ollama_latest_suffix_matches():
    s = check_llm(agent(ollama_model="llama3"), net({f"{OLLAMA}/api/tags": tags("llama3:latest")}))
    assert s.ok and s.model == "llama3:latest" and not s.note


def test_ollama_not_running():
    s = check_llm(agent(), net({}))
    assert not s.ok and s.problem == "ollama_unreachable"
    assert "ollama serve" in s.fix and "API key" in s.fix


def test_ollama_running_without_chat_model():
    s = check_llm(agent(), net({f"{OLLAMA}/api/tags": tags("nomic-embed-text:latest")}))
    assert not s.ok and s.problem == "ollama_no_models" and "ollama pull" in s.fix


def test_ollama_missing_model_falls_back_to_installed_one():
    s = check_llm(agent(ollama_model="mistral"), net({f"{OLLAMA}/api/tags": tags("qwen2.5:7b", "llama3:latest")}))
    assert s.ok and s.model == "llama3:latest"
    assert "ollama pull mistral" in s.note


def test_api_without_key_is_reported_before_any_request():
    fetch = net({f"{OLLAMA}/api/tags": tags("llama3:latest")})
    s = check_llm(agent(api_base=GROQ, api_model="llama-3.3-70b"), fetch)
    # Falls back to Ollama but tells the user why the hosted API isn't used
    assert s.ok and s.provider == "ollama" and "No API key" in s.note
    assert not any(u.startswith(GROQ) for u, _ in fetch.seen)


def test_api_rejected_key_with_no_ollama():
    s = check_llm(agent(api_base=GROQ, api_model="m", api_key="bad"), net({f"{GROQ}/models": (401, {})}))
    assert not s.ok and s.problem == "api_bad_key" and "valid API key" in s.fix
    assert "Ollama isn't available" in s.fix


def test_api_ok_sends_bearer_and_wins_over_ollama():
    fetch = net({f"{GROQ}/models": (200, {"data": [{"id": "m"}]}), f"{OLLAMA}/api/tags": tags("llama3")})
    s = check_llm(agent(api_base=GROQ, api_model="m", api_key="k"), fetch)
    assert s.ok and s.provider == "api" and s.label == "m · api.groq.com"
    assert fetch.seen[0] == (f"{GROQ}/models", {"Authorization": "Bearer k"})


def test_api_unknown_model_lists_alternatives():
    s = check_llm(
        agent(api_base=GROQ, api_model="nope", api_key="k"),
        net({f"{GROQ}/models": (200, {"data": [{"id": "a"}, {"id": "b"}]})}),
    )
    assert not s.ok and s.problem == "api_model_missing" and "a, b" in s.fix


def test_api_unreachable():
    s = check_llm(agent(api_base=GROQ, api_model="m", api_key="k"), net({}))
    assert not s.ok and s.problem == "api_unreachable" and "proxy" in s.fix


def test_local_openai_compatible_server_needs_no_key():
    base = "http://localhost:1234/v1"
    s = check_llm(agent(api_base=base, api_model="m"), net({f"{base}/models": (200, {"data": [{"id": "m"}]})}))
    assert s.ok and s.provider == "api"
