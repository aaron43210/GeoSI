# -*- coding: utf-8 -*-
"""
GeoSI plugin settings — stored in QgsSettings under "geosi/".

    ollama_endpoint   http://localhost:11434
    planner_model     "" → auto-detect (prefers llama3 family)
    embed_model       nomic-embed-text
    max_attempts      3   (plan → verify → re-plan cycles per request)

apply(engine) pushes the values into a running engine; the dialog is
opened from the ⚙ button in the chat dock.
"""

from __future__ import annotations

import os

# Defaults; environment variables (OLLAMA_ENDPOINT, OLLAMA_MODEL,
# GEOSI_EMBED_MODEL) win over these until the user saves the dialog.
KEYS = {
    "ollama_endpoint": os.environ.get("OLLAMA_ENDPOINT", "http://localhost:11434"),
    "planner_model": os.environ.get("OLLAMA_MODEL", ""),
    "embed_model": os.environ.get("GEOSI_EMBED_MODEL", "nomic-embed-text"),
    "max_attempts": 3,
}


def load() -> dict:
    from qgis.core import QgsSettings

    s = QgsSettings()
    out = {}
    for key, default in KEYS.items():
        value = s.value(f"geosi/{key}", default)
        out[key] = int(value) if isinstance(default, int) else str(value or default)
    return out


def save(values: dict) -> None:
    from qgis.core import QgsSettings

    s = QgsSettings()
    for key in KEYS:
        if key in values:
            s.setValue(f"geosi/{key}", values[key])


def ollama_models(endpoint: str) -> list:
    try:
        import requests
        resp = requests.get(f"{endpoint}/api/tags", timeout=2)
        return [m.get("name") for m in resp.json().get("models", []) if m.get("name")]
    except Exception:
        return []


def apply(engine, values: dict = None) -> None:
    """Point a running engine at the configured models."""
    values = values or load()
    agent = engine.agent
    agent._ollama_endpoint = values["ollama_endpoint"].rstrip("/")
    if values["planner_model"]:
        agent._ollama_model = values["planner_model"]
    retriever = getattr(agent, "_tool_retriever", None)
    if retriever is not None and (retriever.model != values["embed_model"]
                                  or retriever.endpoint != agent._ollama_endpoint):
        agent._tool_retriever = None  # rebuilt lazily with the new model
        agent._example_selector = None
    os.environ["GEOSI_EMBED_MODEL"] = values["embed_model"]
    os.environ["OLLAMA_ENDPOINT"] = agent._ollama_endpoint
    if getattr(engine, "loop", None) is not None:
        engine.loop.max_attempts = max(1, int(values["max_attempts"]))


class SettingsDialog:
    """Small modal dialog; returns True from exec_() when saved."""

    def __init__(self, parent=None):
        from qgis.PyQt.QtWidgets import (
            QComboBox, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QSpinBox,
        )

        self.values = load()
        self.dialog = QDialog(parent)
        self.dialog.setWindowTitle("GeoSI settings")
        form = QFormLayout(self.dialog)

        self.endpoint = QLineEdit(self.values["ollama_endpoint"])
        form.addRow("Ollama URL", self.endpoint)

        models = ollama_models(self.values["ollama_endpoint"])
        self.planner = QComboBox()
        self.planner.setEditable(True)
        self.planner.addItem("")  # auto-detect
        self.planner.addItems([m for m in models if "embed" not in m])
        self.planner.setCurrentText(self.values["planner_model"])
        self.planner.setToolTip("Leave empty to auto-detect. Larger models plan more reliably.")
        form.addRow("Planning model", self.planner)

        self.embed = QComboBox()
        self.embed.setEditable(True)
        self.embed.addItems([m for m in models if "embed" in m] or ["nomic-embed-text"])
        self.embed.setCurrentText(self.values["embed_model"])
        form.addRow("Embedding model", self.embed)

        self.attempts = QSpinBox()
        self.attempts.setRange(1, 6)
        self.attempts.setValue(int(self.values["max_attempts"]))
        self.attempts.setToolTip("How many times GeoSI re-plans when a result fails its checks.")
        form.addRow("Max attempts", self.attempts)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.dialog.accept)
        buttons.rejected.connect(self.dialog.reject)
        form.addRow(buttons)

    def exec_(self) -> bool:
        run = getattr(self.dialog, "exec", None) or self.dialog.exec_
        if not run():
            return False
        self.values = {
            "ollama_endpoint": self.endpoint.text().strip() or KEYS["ollama_endpoint"],
            "planner_model": self.planner.currentText().strip(),
            "embed_model": self.embed.currentText().strip() or KEYS["embed_model"],
            "max_attempts": self.attempts.value(),
        }
        save(self.values)
        return True
