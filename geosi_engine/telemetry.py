# -*- coding: utf-8 -*-
"""
GeoSI v2 — OpenTelemetry Instrumentation (Phase P1 gap, FR-7.3)
════════════════════════════════════════════════════════════════════
Every agent hand-off in the Core Workflow is wrapped with an OTel span:

    Supervisor → Planning → Validation → Permission & Safety
    → Execution Dispatcher → GIS / RS / ML / Geology
    → Verification → Report Generation

Design principles
─────────────────
* Gracefully degrades: if opentelemetry is not installed or
  ``GEOSI_OTEL_ENDPOINT`` is not set, a no-op tracer is used and
  all span calls become cheap pass-throughs.
* ``@span(name)`` decorator: the primary way to instrument a function.
* ``start_span(name)`` context manager: for inline block-level spans.
* Every span records:
    - ``agent.name``      — which agent owns this span
    - ``session.id``      — from the enclosing request context
    - ``llm.provider``    — set by PlanningAgent when known
    - ``error``           — automatically set on exception
* Propagator: W3C TraceContext (default for OTel), enabling end-to-end
  trace correlation from REST client → Supervisor → domain agent.

Usage
─────
::

    from geosi_engine.telemetry import span, start_span, set_span_attr

    class PlanningAgent:
        @span("planning.plan")
        def plan(self, query, ...):
            set_span_attr("llm.provider", provider_name)
            ...

    class SupervisorAgent:
        def _run_pipeline(self, request, engine):
            with start_span("supervisor.pipeline") as s:
                s.set_attribute("session.id", request.session_id)
                ...

Environment variables
─────────────────────
GEOSI_OTEL_ENDPOINT   — OTLP gRPC endpoint, e.g. http://localhost:4317
                        If absent, a no-op tracer is used.
GEOSI_SERVICE_NAME    — service name reported to the collector (default: geosi)
GEOSI_ENV             — injected as ``deployment.environment`` attribute
"""
from __future__ import annotations

import functools
import logging
import os
from contextlib import contextmanager
from typing import Any, Callable, Generator, Optional

logger = logging.getLogger("geosi_engine.telemetry")

# ---------------------------------------------------------------------------
# Tracer initialisation
# ---------------------------------------------------------------------------

_tracer = None
_NOOP = False


def _init_tracer():
    """
    Initialise the global OTel tracer.

    Called once on first use (lazy init so import never fails even
    if opentelemetry is absent).
    """
    global _tracer, _NOOP

    endpoint = os.environ.get("GEOSI_OTEL_ENDPOINT", "")
    service_name = os.environ.get("GEOSI_SERVICE_NAME", "geosi")

    if not endpoint:
        _NOOP = True
        logger.debug(
            "GEOSI_OTEL_ENDPOINT not set — OpenTelemetry disabled (no-op mode). "
            "Set GEOSI_OTEL_ENDPOINT to enable distributed tracing."
        )
        _tracer = _NoopTracer()
        return

    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

        resource = Resource.create({
            "service.name": service_name,
            "deployment.environment": os.environ.get("GEOSI_ENV", "development"),
        })
        provider = TracerProvider(resource=resource)
        exporter = OTLPSpanExporter(endpoint=endpoint, insecure=True)
        provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(provider)
        _tracer = trace.get_tracer("geosi_engine")
        logger.info(
            "OpenTelemetry tracing enabled: endpoint=%s service=%s",
            endpoint,
            service_name,
        )

    except ImportError:
        _NOOP = True
        logger.warning(
            "opentelemetry-sdk not installed — falling back to no-op tracer. "
            "Install opentelemetry-exporter-otlp to enable tracing."
        )
        _tracer = _NoopTracer()

    except Exception as exc:
        _NOOP = True
        logger.warning("Failed to initialise OpenTelemetry: %s — no-op mode.", exc)
        _tracer = _NoopTracer()


def get_tracer():
    """Return the singleton OTel tracer (initialising on first call)."""
    if _tracer is None:
        _init_tracer()
    return _tracer


# ---------------------------------------------------------------------------
# No-op tracer (fallback when OTel is absent / endpoint not configured)
# ---------------------------------------------------------------------------

class _NoopSpan:
    """Zero-overhead no-op span."""

    def set_attribute(self, key: str, value: Any) -> None:  # noqa: D401
        pass

    def record_exception(self, exc: Exception) -> None:
        pass

    def set_status(self, *args: Any, **kwargs: Any) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args: Any) -> None:
        pass


class _NoopTracer:
    """No-op tracer that makes all span calls cheap pass-throughs."""

    def start_as_current_span(self, name: str, **kwargs: Any):
        return _NoopSpan()

    def start_span(self, name: str, **kwargs: Any) -> _NoopSpan:
        return _NoopSpan()


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def span(name: str, agent: Optional[str] = None):
    """
    Decorator that wraps a function in an OTel span.

    Usage::

        @span("planning.plan", agent="planning")
        def plan(self, query, ...):
            ...

    Parameters
    ----------
    name:
        Span name (e.g. ``"supervisor.handle"``, ``"gis_agent.execute_step"``).
    agent:
        Optional agent name attached as ``agent.name`` attribute.
    """
    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            tracer = get_tracer()
            with tracer.start_as_current_span(name) as s:
                if agent:
                    s.set_attribute("agent.name", agent)
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:
                    s.record_exception(exc)
                    try:
                        from opentelemetry.trace import StatusCode
                        s.set_status(StatusCode.ERROR, str(exc))
                    except Exception:
                        logger.debug("suppressed exception", exc_info=True)
                    raise
        return wrapper
    return decorator


@contextmanager
def start_span(name: str, **attrs: Any) -> Generator[Any, None, None]:
    """
    Context manager for block-level spans.

    Usage::

        with start_span("supervisor.pipeline", session_id=sid) as s:
            s.set_attribute("query.length", len(query))
            ...

    Parameters
    ----------
    name:
        Span name.
    **attrs:
        Key/value attributes set immediately on the span.
    """
    tracer = get_tracer()
    with tracer.start_as_current_span(name) as s:
        for k, v in attrs.items():
            s.set_attribute(k, str(v))
        try:
            yield s
        except Exception as exc:
            s.record_exception(exc)
            try:
                from opentelemetry.trace import StatusCode
                s.set_status(StatusCode.ERROR, str(exc))
            except Exception:
                logger.debug("suppressed exception", exc_info=True)
            raise


def set_span_attr(key: str, value: Any) -> None:
    """
    Set an attribute on the **current** active span (if any).

    Silently does nothing when running in no-op mode or when there
    is no active span (e.g. in unit tests).
    """
    if _NOOP:
        return
    try:
        from opentelemetry import trace

        current = trace.get_current_span()
        if current:
            current.set_attribute(key, str(value))
    except Exception:
        logger.debug("suppressed exception", exc_info=True)
