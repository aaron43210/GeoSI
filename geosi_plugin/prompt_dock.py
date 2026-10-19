"""
GeoSI Plugin — chat dock.

    ┌ header ─ GeoSI · tools ─────────── [● model chip] ↶ ＋ ⚙ ┐
    │ notice bar (shown while no model is connected / offline)  │
    │ chat (QTextBrowser: bubbles, cards with action links)     │
    │ run bar (progress while a request runs)                   │
    │ composer: multi-line prompt + [@ Layer][Map view][Sel] ➤  │
    └───────────────────────────────────────────────────────────┘

Requests need a reachable model (hosted API or Ollama) unless the user
chooses "Continue offline". A request sent before that is kept and runs
as soon as the connection works.

Queries run as a QgsTask so QGIS never freezes; the task's finished
callback runs on the main thread, where result layers are added.
"""

import html
import logging
import os
import re
import traceback
from urllib.parse import parse_qs, quote, urlparse

from qgis.PyQt.QtCore import QStringListModel, Qt, QUrl, pyqtSignal
from qgis.PyQt.QtWidgets import QCompleter, QPlainTextEdit

from .ui_theme import stylesheet, tokens_for

logger = logging.getLogger("geosi_plugin.prompt_dock")

# The desktop plugin is one user with one workspace: a single session
SESSION_ID = "qgis-desktop"

_CONNECTION_ERROR_RE = re.compile(
    r"not reachable|unreachable|connection refused|timed out|max retries|api key|401|403", re.IGNORECASE
)

_GIS_EXTS = frozenset({".gpkg", ".shp", ".geojson", ".json", ".tif", ".tiff", ".fgb", ".kml", ".kmz", ".csv", ".zip"})


class PromptEdit(QPlainTextEdit):
    """Multi-line prompt: Enter sends, Shift+Enter adds a line, grows to 6 lines."""

    submitted = pyqtSignal()
    focusChanged = pyqtSignal(bool)
    MAX_LINES = 6

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("prompt")
        self.setTabChangesFocus(True)
        self.completer = None
        self.textChanged.connect(self._fit_height)
        self._fit_height()

    # QLineEdit-compatible API (the benchmark and older code use it)
    def text(self):
        return self.toPlainText()

    def setText(self, text):
        self.setPlainText(text)
        self.setCursorPosition(len(text))

    def cursorPosition(self):
        return self.textCursor().position()

    def setCursorPosition(self, pos):
        cursor = self.textCursor()
        cursor.setPosition(max(0, min(pos, len(self.toPlainText()))))
        self.setTextCursor(cursor)

    def keyPressEvent(self, event):
        popup = self.completer.popup() if self.completer else None
        enter = event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter)
        if (
            popup is not None
            and popup.isVisible()
            and (enter or event.key() in (Qt.Key.Key_Escape, Qt.Key.Key_Tab, Qt.Key.Key_Backtab))
        ):
            event.ignore()  # let the completer take it
            return
        if enter and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            self.submitted.emit()
            return
        super().keyPressEvent(event)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focusChanged.emit(True)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.focusChanged.emit(False)

    def _fit_height(self):
        lines = max(1, min(self.MAX_LINES, int(self.document().size().height()) or 1))
        line_h = self.fontMetrics().lineSpacing()
        self.setFixedHeight(lines * line_h + 14)


class GeoSIDock:
    """Dockable chat widget for GeoSI inside QGIS."""

    def __init__(self, iface, engine, supervisor=None, run_in_background=True):
        from qgis.PyQt.QtWidgets import QDockWidget, QTextBrowser, QVBoxLayout, QWidget

        self.iface = iface
        self.engine = engine
        if supervisor is None:
            from geosi_engine.agents.supervisor import SupervisorAgent
            from geosi_engine.session_pool import SessionPool

            supervisor = SupervisorAgent(SessionPool(max_size=1, ttl_seconds=float("inf"), factory=lambda sid: engine))
        self.supervisor = supervisor
        self._task = None
        self._status_task = None
        self._pending_query = None
        self._pending_approval = None
        self._synced = {}  # engine layer name -> QGIS layer id
        self._closed = False
        # Run work as QgsTasks so QGIS stays responsive. Tests that need the
        # result synchronously pass False.
        self.run_in_background = run_in_background
        # True once the user chooses to work without a model
        self.offline_ok = False
        self.llm_status = None

        self.dock = QDockWidget("GeoSI", iface.mainWindow())
        self.dock.setObjectName("GeoSIDock")
        self.dock.destroyed.connect(self._mark_closed)
        self.dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)

        root = QWidget()
        root.setObjectName("geosiRoot")
        self.t = tokens_for(self.dock)
        root.setStyleSheet(stylesheet(self.t))
        layout = QVBoxLayout(root)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        layout.addLayout(self._build_header())
        self.notice = self._build_notice()
        layout.addWidget(self.notice)

        self.chat_display = QTextBrowser()
        self.chat_display.setObjectName("chat")
        self.chat_display.setOpenLinks(False)
        self.chat_display.setOpenExternalLinks(False)
        self.chat_display.anchorClicked.connect(self._on_anchor)
        layout.addWidget(self.chat_display, 1)

        layout.addWidget(self._build_run_bar())
        layout.addWidget(self._build_composer())

        root.setAcceptDrops(True)
        root.dragEnterEvent = self._drag_enter
        root.dropEvent = self._drop_event
        self.dock.setWidget(root)

        from geosi_engine.base import attach_ui

        attach_ui(True, iface)
        self._welcome()
        self._check_connection(announce=True)

    # ── Layout ─────────────────────────────────────────────────────────

    def _build_header(self):
        from qgis.PyQt.QtWidgets import QHBoxLayout, QLabel, QPushButton, QToolButton, QVBoxLayout

        row = QHBoxLayout()
        titles = QVBoxLayout()
        titles.setSpacing(0)
        title = QLabel("GeoSI")
        title.setObjectName("title")
        self.subtitle = QLabel(f"{self.engine.registry.tool_count()} GIS tools ready")
        self.subtitle.setObjectName("subtitle")
        titles.addWidget(title)
        titles.addWidget(self.subtitle)
        row.addLayout(titles)
        row.addStretch()

        self.status_chip = QPushButton("● Checking…")
        self.status_chip.setObjectName("statusChip")
        self.status_chip.setCursor(Qt.CursorShape.PointingHandCursor)
        self.status_chip.setToolTip("Model connection. Click to check again.")
        self.status_chip.clicked.connect(lambda: self._check_connection(announce=True))
        row.addWidget(self.status_chip)

        for glyph, tip, handler in (
            ("↶", "Undo the last GeoSI change to the project", self._on_undo),
            ("＋", "New chat", self._on_clear),
            ("⚙", "Settings: model, Ollama URL, API key", self._on_settings),
        ):
            btn = QToolButton()
            btn.setObjectName("iconBtn")
            btn.setText(glyph)
            btn.setToolTip(tip)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(handler)
            row.addWidget(btn)
        return row

    def _build_notice(self):
        from qgis.PyQt.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

        frame = QFrame()
        frame.setObjectName("notice")
        frame.setProperty("level", "warning")
        box = QVBoxLayout(frame)
        box.setContentsMargins(10, 6, 10, 6)
        box.setSpacing(4)
        # One line of status; the full explanation and fix go into the chat card
        self.notice_title = QLabel()
        self.notice_title.setObjectName("noticeTitle")
        self.notice_title.setWordWrap(True)
        box.addWidget(self.notice_title)

        buttons = QHBoxLayout()
        buttons.setSpacing(6)
        self.notice_settings = QPushButton("Settings")
        self.notice_settings.setObjectName("primary")
        self.notice_settings.clicked.connect(self._on_settings)
        self.notice_retry = QPushButton("Check again")
        self.notice_retry.setObjectName("secondary")
        self.notice_retry.clicked.connect(lambda: self._check_connection(announce=True))
        self.notice_offline = QPushButton("Continue offline")
        self.notice_offline.setObjectName("secondary")
        self.notice_offline.clicked.connect(self._on_continue_offline)
        for b in (self.notice_settings, self.notice_retry, self.notice_offline):
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            buttons.addWidget(b)
        buttons.addStretch()
        box.addLayout(buttons)
        frame.hide()
        return frame

    def _build_run_bar(self):
        from qgis.PyQt.QtWidgets import QLabel, QProgressBar, QVBoxLayout, QWidget

        wrap = QWidget()
        box = QVBoxLayout(wrap)
        box.setContentsMargins(2, 0, 2, 0)
        box.setSpacing(2)
        self.run_bar = QProgressBar()
        self.run_bar.setObjectName("runBar")
        self.run_bar.setTextVisible(False)
        self.run_bar.setFixedHeight(3)
        self.run_bar.setRange(0, 0)
        self.status_label = QLabel("")
        self.status_label.setObjectName("runText")
        box.addWidget(self.run_bar)
        box.addWidget(self.status_label)
        wrap.hide()
        self.run_wrap = wrap
        return wrap

    def _build_composer(self):
        from qgis.PyQt.QtWidgets import QFrame, QHBoxLayout, QPushButton, QVBoxLayout

        frame = QFrame()
        frame.setObjectName("composer")
        box = QVBoxLayout(frame)
        box.setContentsMargins(8, 6, 8, 6)
        box.setSpacing(4)

        self.input_box = PromptEdit()
        self.input_box.setPlaceholderText("Ask GeoSI to analyse, map or explain…")
        self.input_box.setToolTip("Enter sends, Shift+Enter adds a line, @ names a layer")
        self.input_box.submitted.connect(self._on_submit)
        self.input_box.textChanged.connect(self._on_input_changed)
        self.input_box.focusChanged.connect(lambda on: self._set_prop(frame, "focused", "true" if on else "false"))
        box.addWidget(self.input_box)

        self._completer_model = QStringListModel()
        self._completer = QCompleter(self._completer_model, self.input_box)
        self._completer.setWidget(self.input_box)
        self._completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self._completer.activated.connect(self._on_completer_activated)
        self.input_box.completer = self._completer

        row = QHBoxLayout()
        row.setSpacing(4)
        for label, tip, handler in (
            ("@ Layer", "Name a loaded layer in your request", self._on_insert_layer_ref),
            ("Map view", "Limit the request to the current map extent", self._on_append_extent),
            ("Selection", "Use the selected features of the active layer", self._on_append_selected),
        ):
            chip = QPushButton(label)
            chip.setObjectName("chip")
            chip.setToolTip(tip)
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.clicked.connect(handler)
            row.addWidget(chip)
        row.addStretch()
        self.send_btn = QPushButton("Send")
        self.send_btn.setObjectName("primary")
        self.send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_btn.clicked.connect(self._on_send_or_stop)
        row.addWidget(self.send_btn)
        box.addLayout(row)
        return frame

    @staticmethod
    def _set_prop(widget, name, value):
        widget.setProperty(name, value)
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    def _mark_closed(self, *_):
        from geosi_engine.base import attach_ui

        self._closed = True
        attach_ui(False)

    # ── Qt delegation (so iface.addDockWidget works) ───────────────────

    def show(self):
        self.dock.show()

    def hide(self):
        self.dock.hide()

    def __getattr__(self, name):
        if name == "dock":  # not set yet: avoid infinite recursion
            raise AttributeError(name)
        return getattr(self.dock, name)

    # ── Model connection ───────────────────────────────────────────────

    def _connection_ready(self):
        return self.offline_ok or (self.llm_status is not None and self.llm_status.ok)

    def _check_connection(self, announce=False):
        """Probe the hosted API / Ollama off the main thread."""
        from geosi_engine.llm_status import check_llm

        self.status_chip.setText("● Checking…")
        self._chip_colour("faint")
        if not self.run_in_background:
            self._on_status(check_llm(self.engine.agent), announce)
            return
        from qgis.core import QgsApplication, QgsTask

        def body(task):
            return check_llm(self.engine.agent)

        def done(exception, status=None):
            self._status_task = None
            if self._closed:
                return
            if exception is not None or status is None:
                from geosi_engine.llm_status import LLMStatus

                status = LLMStatus(
                    False,
                    problem="check_failed",
                    title="Couldn't check the model connection",
                    fix=str(exception or "Unknown error"),
                )
            self._on_status(status, announce)

        self._status_task = QgsTask.fromFunction("GeoSI: checking model connection", body, on_finished=done)
        QgsApplication.taskManager().addTask(self._status_task)

    def _on_status(self, status, announce):
        previous = self.llm_status
        self.llm_status = status
        agent = self.engine.agent
        agent.model_available = status.ok  # model-first planning while connected
        if status.ok and status.provider == "ollama" and status.model:
            agent._ollama_model = status.model  # an installed model, not a stale guess
        self._refresh_connection_ui()

        if status.ok:
            if announce or (previous is not None and not previous.ok):
                note = f" {html.escape(status.note)}" if status.note else ""
                self._append_meta(f"● Connected to <b>{html.escape(status.label)}</b>.{note}", "ok")
            if self._pending_query:
                query, self._pending_query = self._pending_query, None
                self._append_meta("Running your request now.")
                self._run(query)
        elif announce:
            self._append_connection_card()

    def _refresh_connection_ui(self):
        s = self.llm_status
        if s is not None and s.ok:
            self.status_chip.setText(f"● {s.label}")
            self.status_chip.setToolTip(f"{s.title}. {s.note}".strip() + " Click to check again.")
            self._chip_colour("ok")
            self.notice.hide()
            return
        if self.offline_ok:
            self.status_chip.setText("● Offline")
            self._chip_colour("warn")
            self._show_notice("info", "Offline: built-in planning only. Connect a model for open questions.")
            return
        self.status_chip.setText("● Not connected")
        self._chip_colour("danger")
        if s is not None:
            self._show_notice("warning", f"No model connected. {s.title}.")

    def _chip_colour(self, token):
        self.status_chip.setStyleSheet(f"QPushButton#statusChip {{ color: {self.t[token]}; }}")

    def _show_notice(self, level, title):
        self._set_prop(self.notice, "level", level)
        self.notice_title.setText(title)
        # Offline: "Settings" is the way back to a model; no need for the other two
        self.notice_retry.setVisible(level == "warning")
        self.notice_offline.setVisible(level == "warning")
        self.notice.show()

    def _fix_html(self, fix):
        """Escape a fix hint, then render `code` and bare https links."""
        text = html.escape(fix)
        text = re.sub(r"`([^`]+)`", rf"<code style='background:{self.t['sunk']};'>\1</code>", text)
        return re.sub(r"(https://[\w./-]+)", rf"<a href='\1' style='color:{self.t['accent']};'>\1</a>", text)

    def _on_continue_offline(self):
        self.offline_ok = True
        self._refresh_connection_ui()
        self._append_meta("Continuing offline with built-in planning.")
        if self._pending_query:
            query, self._pending_query = self._pending_query, None
            self._run(query)

    # ── Requests ───────────────────────────────────────────────────────

    def _on_send_or_stop(self):
        if self._task is not None:
            self._on_stop()
        else:
            self._on_submit()

    def _on_submit(self):
        query = self.input_box.text().strip()
        if not query:
            return
        self.input_box.clear()
        self._append_user(query)

        command = query.lower()
        if command in ("help", "/help"):
            self._show_help()
            return
        if command in ("tools", "/tools"):
            self._show_tools()
            return
        if command in ("layers", "/layers"):
            self._show_layers()
            return
        if command in ("status", "/status", "connection"):
            self._check_connection(announce=True)
            return
        if command.startswith(("search ", "/search ")):
            self._search_tools(query.split(" ", 1)[1].strip())
            return

        if self._task is not None:
            self._append_meta("Still working on the previous request. Press Stop to cancel it.")
            return
        if self.llm_status is None and not self.offline_ok:
            self._pending_query = query
            self._append_meta("Checking the model connection first…")
            return
        if not self._connection_ready():
            self._pending_query = query
            self._append_connection_card(waiting=True)
            return
        self._run(query)

    def _run(self, query):
        self._sync_layers()
        self._start(query)

    def _start(self, query, resume=None):
        """Run a request (or resume a paused one) without blocking QGIS."""
        if not self.run_in_background:
            self._show_result(*self._run_query(query, resume=resume))
            return
        from qgis.core import QgsApplication, QgsTask

        label = "resuming approved step" if resume else query[:50]
        task = QgsTask.fromFunction(f"GeoSI: {label}", self._task_body, query, resume, on_finished=self._on_task_done)
        self._task = task
        task.progressChanged.connect(self._on_progress)
        self._set_busy(True)
        QgsApplication.taskManager().addTask(task)

    def _run_query(self, query, task=None, resume=None):
        """Run through the Supervisor; returns (ExecutionResult, error_text). Safe off the main thread."""
        loop = getattr(self.engine, "loop", None)
        if loop is not None:
            loop.should_stop = task.isCanceled if task is not None else (lambda: False)
            loop.on_progress = task.setProgress if task is not None else None
        try:
            from geosi_engine.agents.supervisor import SupervisorRequest

            if resume is not None:
                response = self.supervisor.resume(resume[0], resume[1], session_id=SESSION_ID)
            else:
                response = self.supervisor.handle(SupervisorRequest(query=query, session_id=SESSION_ID, surface="qgis"))
            if response.execution_result is None:
                return None, response.error or "No result"
            return response.execution_result, None
        except Exception as e:
            logger.error("GeoSI request failed:\n%s", traceback.format_exc())
            return None, f"{type(e).__name__}: {e}"

    def _task_body(self, task, query, resume=None):
        return self._run_query(query, task, resume=resume)

    def _on_task_done(self, exception, value=None):
        self._task = None
        self._set_busy(False)
        if exception is not None:
            self._append_error(str(exception))
            return
        if value is None:
            self._append_meta("Stopped.")
            return
        self._show_result(*value)

    def _on_progress(self, pct):
        self.run_bar.setRange(0, 100)
        self.run_bar.setValue(int(pct))
        self.status_label.setText(f"Working… {pct:.0f}%")

    def _on_stop(self):
        if self._task is not None:
            self._task.cancel()
            self.status_label.setText("Stopping after the current step…")

    def _set_busy(self, busy):
        self.send_btn.setText("Stop" if busy else "Send")
        self.send_btn.setObjectName("danger" if busy else "primary")
        self._set_prop(self.send_btn, "busy", busy)
        self.run_bar.setRange(0, 0)
        self.status_label.setText("Planning and running…" if busy else "")
        self.run_wrap.setVisible(busy)

    def _on_settings(self):
        from .settings import SettingsDialog, apply

        dlg = SettingsDialog(self.dock)
        if dlg.exec_():
            apply(self.engine, dlg.values)
            self._append_meta("Settings saved. Checking the connection…")
            self._check_connection(announce=True)

    def _apply_ui_actions(self):
        """Run map changes the tools queued (basemap, zoom, style, export) on the main thread."""
        from geosi_engine.base import drain_ui_actions

        for description, fn in drain_ui_actions():
            try:
                outcome = fn()
            except Exception as exc:  # noqa: BLE001
                logger.warning("UI action failed: %s", description, exc_info=True)
                self._append_error(f"{description.rstrip('.')} failed: {exc}")
                continue
            if outcome is None or outcome is False:
                self._append_error(f"Couldn't complete: {description}")
            else:
                self._append_meta(html.escape(description), "ok")

    def _show_result(self, result, error):
        self._render_result(result, error)
        self._apply_ui_actions()

    def _render_result(self, result, error):
        if error:
            self._append_error(error)
            if _CONNECTION_ERROR_RE.search(error):
                self._check_connection(announce=True)
            return
        if result.approval_pending:
            self._ask_approval(result)
            return
        if result.success:
            self._append_assistant(result.answer)
            src = getattr(result, "plan_source", "")
            if src and src.startswith(("ollama:", "api:", "gemini", "anthropic")):
                self._append_meta(f"answered by {html.escape(str(src))}")
            for w in getattr(result, "warnings", None) or []:
                self._append_meta(f"⚠ {html.escape(str(w))}", "warn")
            if result.reasoning:
                self._append_details("How I did it", result.reasoning)
            self._load_result_layers(result)
        else:
            message = result.answer or result.error or "Unknown error"
            self._append_error(message)
            if result.reasoning and result.reasoning != message:
                self._append_details("What was tried", result.reasoning)
            if _CONNECTION_ERROR_RE.search(f"{message} {result.error or ''}"):
                self._check_connection(announce=True)

    def _ask_approval(self, result):
        """A step needs approval: show an in-chat card; the links resume or stop it."""
        from geosi_engine.agents.permission_safety import PermissionSafetyAgent

        action_id = result.approval_pending
        pending = PermissionSafetyAgent._APPROVALS.get(action_id)
        data = pending.step_data if pending else {}
        self._pending_approval = action_id
        body = (
            f"<b>{html.escape(str(data.get('tool_name', 'A step')))}</b> changes data outside the current "
            f"analysis (risk: {html.escape(str(data.get('risk_level', '?')))}).<br>"
            f"<span style='color:{self.t['muted']};'>Parameters: "
            f"{html.escape(str(data.get('parameters', {})))[:400]}</span>"
        )
        self._append_card(
            "warning",
            "Approve this step?",
            body,
            [("Approve", f"geosi:approve?id={quote(action_id)}"), ("Reject", f"geosi:reject?id={quote(action_id)}")],
        )

    def _resolve_approval(self, action_id, approved):
        if action_id != self._pending_approval:
            self._append_meta("That approval is no longer pending.")
            return
        self._pending_approval = None
        self._append_meta("Approved, continuing." if approved else "Rejected. Nothing was changed.")
        self._start("", resume=(action_id, approved))

    def _on_anchor(self, url: QUrl):
        target = url.toString()
        if target.startswith(("http://", "https://")):
            from qgis.PyQt.QtGui import QDesktopServices

            QDesktopServices.openUrl(url)
            return
        parsed = urlparse(target)
        if parsed.scheme != "geosi":
            return
        args = parse_qs(parsed.query)
        action = parsed.path
        if action == "settings":
            self._on_settings()
        elif action == "recheck":
            self._check_connection(announce=True)
        elif action == "offline":
            self._on_continue_offline()
        elif action == "prompt":
            self.input_box.setText(args.get("q", [""])[0])
            self.input_box.setFocus()
        elif action in ("approve", "reject"):
            self._resolve_approval(args.get("id", [""])[0], action == "approve")

    # ── @-layer autocomplete ───────────────────────────────────────────

    def _on_input_changed(self):
        text = self.input_box.text()
        fragment = text[: self.input_box.cursorPosition()]
        at_pos = fragment.rfind("@")
        popup = self._completer.popup()
        if at_pos == -1 or " " in fragment[at_pos:]:
            popup.hide()
            return
        partial = fragment[at_pos + 1 :]
        matches = [f"@{n}" for n in self.engine.state.list_layers() if n.lower().startswith(partial.lower())]
        if not matches:
            popup.hide()
            return
        self._completer_model.setStringList(matches)
        self._completer.setCompletionPrefix(f"@{partial}")
        rect = self.input_box.cursorRect()
        rect.setWidth(max(160, popup.sizeHintForColumn(0) + 24))
        self._completer.complete(rect)

    def _on_completer_activated(self, completion: str):
        text = self.input_box.text()
        cursor = self.input_box.cursorPosition()
        at_pos = text.rfind("@", 0, cursor)
        if at_pos == -1:
            return
        self.input_box.setText(text[:at_pos] + completion + " " + text[cursor:])
        self.input_box.setCursorPosition(at_pos + len(completion) + 1)

    # ── Context chips ──────────────────────────────────────────────────

    def _on_insert_layer_ref(self):
        self._sync_layers()
        pos = self.input_box.cursorPosition()
        text = self.input_box.text()
        self.input_box.setText(text[:pos] + "@" + text[pos:])
        self.input_box.setCursorPosition(pos + 1)
        self.input_box.setFocus()
        self._on_input_changed()

    def _append_to_prompt(self, snippet):
        current = self.input_box.text().rstrip()
        self.input_box.setText(f"{current} {snippet}".strip())
        self.input_box.setFocus()

    def _on_append_extent(self):
        try:
            ext = self.iface.mapCanvas().extent()
            crs = self.iface.mapCanvas().mapSettings().destinationCrs().authid()
            self._append_to_prompt(
                f"within the map extent ({ext.xMinimum():.4f}, {ext.yMinimum():.4f}, "
                f"{ext.xMaximum():.4f}, {ext.yMaximum():.4f} {crs})"
            )
        except Exception:  # noqa: BLE001
            self._append_to_prompt("within the current map extent")

    def _on_append_selected(self):
        layer = self.iface.activeLayer()
        if layer is None:
            self._append_meta("Select a layer in the Layers panel first.")
            return
        count = layer.selectedFeatureCount() if hasattr(layer, "selectedFeatureCount") else 0
        what = f"the {count} selected features of" if count else "all features of"
        self._append_to_prompt(f"using {what} @{layer.name()}")

    def _on_undo(self):
        loop = getattr(self.engine, "loop", None)
        undo = getattr(loop, "undo_last", None)
        if undo is None:
            self._append_meta("Undo isn't available.")
            return
        try:
            undone = undo()
        except Exception as exc:  # noqa: BLE001
            self._append_error(f"Undo failed: {exc}")
            return
        if undone:
            self._synced.clear()
            self.engine.state.layers.clear()
            self._sync_layers()
            self._append_meta("↶ Undone. The project is back to how it was before the last request.", "ok")
        else:
            self._append_meta("Nothing to undo yet.")

    # ── Drag-and-drop ──────────────────────────────────────────────────

    def _drag_enter(self, event):
        if event.mimeData().hasUrls() and any(
            os.path.splitext(u.toLocalFile())[1].lower() in _GIS_EXTS for u in event.mimeData().urls()
        ):
            event.acceptProposedAction()
            return
        event.ignore()

    def _drop_event(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if os.path.splitext(path)[1].lower() in _GIS_EXTS:
                self._load_dropped_file(path)
        event.acceptProposedAction()

    def _load_dropped_file(self, path: str):
        from qgis.core import QgsProject, QgsRasterLayer, QgsVectorLayer

        name, ext = os.path.splitext(os.path.basename(path))
        ext = ext.lower()
        source = f"/vsizip/{path}" if ext == ".zip" else path  # zipped shapefile
        layer = QgsRasterLayer(source, name) if ext in (".tif", ".tiff") else QgsVectorLayer(source, name, "ogr")
        if not layer.isValid():
            self._append_error(f"Couldn't open {os.path.basename(path)} as a GIS layer.")
            return
        QgsProject.instance().addMapLayer(layer)
        self._sync_layers()
        self._append_meta(f"Added layer <b>{html.escape(name)}</b> from {html.escape(os.path.basename(path))}.", "ok")

    def _on_clear(self):
        self.chat_display.clear()
        conversation = getattr(self.engine, "conversation", None)
        if conversation is not None:
            conversation.clear()
        self._welcome()
        if not self._connection_ready() and self.llm_status is not None:
            self._append_connection_card()

    # ── Layer sync ─────────────────────────────────────────────────────

    def _sync_layers(self):
        """Mirror the QGIS project's layers into the engine (adds, renames, removals)."""
        try:
            from qgis.core import QgsProject, QgsWkbTypes

            from geosi_engine.models import Layer

            current = QgsProject.instance().mapLayers()
            state = self.engine.state
            for name, layer_id in list(self._synced.items()):
                qgs = current.get(layer_id)
                if qgs is None or qgs.name() != name:
                    state.remove_layer(name)
                    del self._synced[name]

            known = set(state.list_layers())
            for layer_id, qgs in current.items():
                name = qgs.name()
                if name in known:
                    if name in self._synced and hasattr(qgs, "featureCount"):
                        state.get_layer(name).feature_count = qgs.featureCount()
                    continue
                is_vector = hasattr(qgs, "featureCount")
                fields, field_types, field_values = [], {}, {}
                geom_type = "Raster"
                if is_vector:
                    try:
                        from .qgis_bridge import field_metadata

                        fields = [f.name() for f in qgs.fields()]
                        field_types, field_values = field_metadata(qgs)
                        geom_type = QgsWkbTypes.displayString(qgs.wkbType())
                    except Exception:  # noqa: BLE001
                        logger.debug("field metadata unavailable for %s", name, exc_info=True)
                engine_layer = Layer(
                    name=name,
                    geometry_type=geom_type,
                    feature_count=qgs.featureCount() if is_vector else 1,
                    crs=qgs.crs().authid(),
                    filepath=qgs.source().split("|")[0],
                    layer_type="vector" if is_vector else "raster",
                    fields=fields,
                    field_types=field_types,
                    field_values=field_values,
                )
                engine_layer.features = qgs  # QgsMapLayer reference for fast paths
                state.add_layer(engine_layer)
                self._synced[name] = layer_id
        except Exception:  # noqa: BLE001
            logger.warning("Layer sync failed", exc_info=True)

    def _load_result_layers(self, result):
        from qgis.core import QgsProject, QgsRasterLayer, QgsVectorLayer

        for name, output in (result.results or {}).items():
            layer_obj = getattr(output, "output", output)
            filepath = getattr(layer_obj, "filepath", "") if layer_obj is not None else ""
            if not filepath or not os.path.isfile(filepath):
                continue
            layer_name = getattr(layer_obj, "name", name)
            if getattr(layer_obj, "layer_type", "vector") == "raster":
                qgs = QgsRasterLayer(filepath, layer_name)
            else:
                qgs = QgsVectorLayer(filepath, layer_name, "ogr")
            if qgs.isValid():
                QgsProject.instance().addMapLayer(qgs)
                self._append_meta(f"Added result layer <b>{html.escape(layer_name)}</b>.", "ok")
            else:
                logger.warning("Result layer is not valid: %s", filepath)

    # ── Built-in commands ──────────────────────────────────────────────

    def _show_help(self):
        self._append_assistant(
            "**Things you can ask**\n"
            "- Analysis: *buffer hospitals by 500 m*, *clip roads to the study area*, *slope from dem*\n"
            "- Questions about your data: *how many parcels does owner A have?*\n"
            "- Open data: *add an OpenStreetMap basemap*, *fetch schools in Leeds from OpenStreetMap*\n"
            "- Code: *write PyQGIS code to reproject a layer*\n"
            "- Concepts: *what is NDVI?*\n\n"
            "**Commands**: `tools`, `search <word>`, `layers`, `status`, `help`"
        )

    def _show_tools(self):
        categories = {}
        for spec in self.engine.registry.list_tools():
            categories.setdefault(spec.category or "general", []).append(spec.name)
        total = sum(len(v) for v in categories.values())
        lines = [f"**{total} tools** by category (type `search <word>` to find one):"]
        for cat in sorted(categories):
            names = sorted(categories[cat])
            more = f" … and {len(names) - 12} more" if len(names) > 12 else ""
            lines.append(f"- **{cat}** ({len(names)}): {', '.join(names[:12])}{more}")
        self._append_assistant("\n".join(lines))

    def _show_layers(self):
        self._sync_layers()
        state = self.engine.state
        names = state.list_layers()
        if not names:
            self._append_assistant("No layers are loaded. Add data in QGIS, or drop a file onto this panel.")
            return
        lines = [f"**{len(names)} layer(s) loaded:**"]
        for n in names:
            lyr = state.get_layer(n)
            detail = f"{lyr.geometry_type}, {lyr.feature_count} features, {lyr.crs}" if lyr else ""
            lines.append(f"- **{n}** — {detail}")
        self._append_assistant("\n".join(lines))

    def _search_tools(self, query: str):
        results = self.engine.registry.search_tools(query)
        if not results:
            self._append_assistant(f"No tools match '{query}'.")
            return
        lines = [f"**{len(results)} tool(s) match '{query}':**"]
        lines += [f"- **{s.name}**: {s.description[:90]}" for s in results[:15]]
        self._append_assistant("\n".join(lines))

    # ── Chat rendering ─────────────────────────────────────────────────

    def _welcome(self):
        t = self.t
        self._sync_layers()
        layers = self.engine.state.list_layers()
        vector = next((n for n in layers if self.engine.state.get_layer(n).layer_type == "vector"), None)
        raster = next((n for n in layers if self.engine.state.get_layer(n).layer_type == "raster"), None)
        prompts = []
        if vector:
            prompts += [f"Buffer {vector} by 500 m", f"How many features are in {vector}?"]
        if raster:
            prompts.append(f"Calculate slope from {raster}")
        prompts += ["Add an OpenStreetMap basemap", "What is NDVI?", "Write PyQGIS code to buffer a layer"]
        links = " ".join(
            f"<a href='geosi:prompt?q={quote(p)}' style='color:{t['accent']}; text-decoration:none;'>"
            f"&nbsp;{html.escape(p)}&nbsp;</a>&nbsp;·"
            for p in prompts[:5]
        ).rstrip("·")
        data_line = (
            f"{len(layers)} layer(s) in this project." if layers else "No layers loaded yet. Drop a file here or ask."
        )
        self._insert(
            f"<p style='font-size:15px; font-weight:600; color:{t['text']};'>What would you like to do?</p>"
            f"<p style='color:{t['muted']};'>Describe a GIS task in plain words. GeoSI picks the QGIS "
            f"tools, runs them and adds the results to your map. {data_line}</p>"
            f"<p style='color:{t['muted']};'>Try: {links}</p>"
        )

    def _append_connection_card(self, waiting=False):
        s = self.llm_status
        if s is None or s.ok:
            return
        actions = [
            ("Open settings", "geosi:settings"),
            ("Check again", "geosi:recheck"),
            ("Continue offline", "geosi:offline"),
        ]
        if waiting:
            self._append_card(
                "warning",
                "Waiting for a model",
                f"I'll run <i>{html.escape(self._pending_query or '')}</i> as soon as a model is connected "
                "(see above), or choose <b>Continue offline</b> to use built-in planning now.",
                actions,
            )
            return
        self._append_card("warning", s.title, self._fix_html(s.fix), actions)

    def _insert(self, fragment_html):
        self.chat_display.append(fragment_html)
        bar = self.chat_display.verticalScrollBar()
        bar.setValue(bar.maximum())

    def _append_user(self, text: str):
        t = self.t
        self._insert(
            "<table width='100%' cellspacing='0' cellpadding='0'><tr><td width='18%'></td>"
            f"<td bgcolor='{t['user_bubble']}' style='padding:8px 10px; color:{t['text']};'>"
            f"{html.escape(text).replace(chr(10), '<br>')}</td></tr></table>"
        )

    def _append_assistant(self, text: str):
        t = self.t
        self._insert(
            "<table width='100%' cellspacing='0' cellpadding='0'><tr>"
            f"<td style='padding:4px 2px; color:{t['text']};'>"
            f"<span style='color:{t['accent']}; font-weight:600;'>GeoSI</span><br>"
            f"{self._markdown_to_html(text, t)}</td><td width='8%'></td></tr></table>"
        )

    def _append_meta(self, html_text: str, tone="muted"):
        colour = {"ok": self.t["ok"], "warn": self.t["warn"]}.get(tone, self.t["faint"])
        self._insert(f"<p style='color:{colour}; font-size:11px;'>{html_text}</p>")

    def _append_error(self, text: str):
        self._append_card("danger", "Something went wrong", html.escape(str(text)).replace("\n", "<br>"), [])

    def _append_details(self, label: str, text: str):
        t = self.t
        self._insert(
            f"<p style='color:{t['faint']}; font-size:11px;'><b>{html.escape(label)}</b><br>"
            f"{html.escape(text).replace(chr(10), '<br>')}</p>"
        )

    def _append_card(self, level, title, body_html, actions):
        t = self.t
        bar, bg = {"danger": (t["danger"], t["danger_bg"]), "info": (t["accent"], t["sunk"])}.get(
            level, (t["warn"], t["warn_bg"])
        )
        buttons = "&nbsp;&nbsp;".join(
            f"<a href='{href}' style='color:{t['accent']}; font-weight:600; text-decoration:none;'>"
            f"{html.escape(label)}</a>"
            for label, href in actions
        )
        self._insert(
            "<table width='100%' cellspacing='0' cellpadding='0'><tr>"
            f"<td width='3' bgcolor='{bar}'></td>"
            f"<td bgcolor='{bg}' style='padding:8px 10px; color:{t['text']};'>"
            f"<b>{html.escape(title)}</b><br>{body_html}"
            + (f"<br><br>{buttons}" if buttons else "")
            + "</td></tr></table>"
        )

    @staticmethod
    def _markdown_to_html(text: str, t=None) -> str:
        """Render the markdown subset the agents produce (code, bold, italics, lists, headings)."""
        from .ui_theme import LIGHT

        t = t or LIGHT
        if not text:
            return ""
        code_blocks = []

        def keep_block(m):
            code = html.escape(m.group(2).strip("\r\n"))
            lang = html.escape((m.group(1) or "python").upper())
            code_blocks.append(
                "<table width='100%' cellspacing='0' cellpadding='0'><tr>"
                f"<td bgcolor='{t['code_bg']}' style='padding:8px;'>"
                f"<span style='color:{t['faint']}; font-size:10px;'>{lang}</span>"
                f"<pre style='color:{t['code_text']}; font-family:monospace; font-size:12px; margin:0; "
                "white-space:pre-wrap;'>"
                f"{code}</pre></td></tr></table>"
            )
            return f"\x00{len(code_blocks) - 1}\x00"

        out = re.sub(r"```([\w+-]*)\r?\n?(.*?)```", keep_block, text, flags=re.DOTALL)
        out = html.escape(out)
        out = re.sub(
            r"`([^`]+)`",
            rf"<code style='background:{t['code_bg']}; color:{t['code_text']}; font-family:monospace;'>\1</code>",
            out,
        )
        out = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", out)
        out = re.sub(r"(?<![\*\w])\*([^*\n]+)\*(?!\*)", r"<i>\1</i>", out)
        lines = []
        for line in out.split("\n"):
            heading = re.match(r"#{1,4}\s+(.*)", line)
            bullet = re.match(r"\s*[-•*]\s+(.*)", line)
            if heading:
                lines.append(f"<b>{heading.group(1)}</b>")
            elif bullet:
                lines.append(f"&nbsp;&nbsp;•&nbsp;{bullet.group(1)}")
            else:
                lines.append(line)
        out = "<br>".join(lines)
        for i, block in enumerate(code_blocks):
            out = out.replace(f"\x00{i}\x00", block)
        return out
