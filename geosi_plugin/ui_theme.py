"""
GeoSI dock theme: light/dark palettes that follow the active QGIS theme.

Colours are plain hex so they also work inside QTextBrowser rich text,
which ignores rgba().
"""

from __future__ import annotations

from typing import Dict

LIGHT: Dict[str, str] = {
    "page": "#f6f7f9",
    "raised": "#ffffff",
    "sunk": "#eef1f4",
    "border": "#dde2e8",
    "text": "#1d2127",
    "muted": "#5d6570",
    "faint": "#8a929c",
    "accent": "#2e8b57",
    "accent_hover": "#25744a",
    "on_accent": "#ffffff",
    "user_bubble": "#e3f1e9",
    "warn": "#b85c00",
    "warn_bg": "#fdf2e6",
    "danger": "#c62f35",
    "danger_bg": "#fcebec",
    "ok": "#1f8a4c",
    "code_bg": "#f1f3f6",
    "code_text": "#24292f",
}

DARK: Dict[str, str] = {
    "page": "#1b1d20",
    "raised": "#25282c",
    "sunk": "#202326",
    "border": "#363a40",
    "text": "#eceef1",
    "muted": "#a6adb6",
    "faint": "#737b85",
    "accent": "#4caf78",
    "accent_hover": "#5fc189",
    "on_accent": "#0d1f15",
    "user_bubble": "#1f3a2b",
    "warn": "#f0a050",
    "warn_bg": "#3a2c1d",
    "danger": "#f0686d",
    "danger_bg": "#3b2224",
    "ok": "#56c487",
    "code_bg": "#16181b",
    "code_text": "#d7dce2",
}


def tokens_for(widget) -> Dict[str, str]:
    """Pick the palette matching the window colour QGIS is using."""
    try:
        from qgis.PyQt.QtGui import QPalette

        window = widget.palette().color(QPalette.ColorRole.Window)
        return DARK if window.lightness() < 128 else LIGHT
    except Exception:  # noqa: BLE001 — no Qt palette available: default to light
        return LIGHT


def stylesheet(t: Dict[str, str]) -> str:
    return f"""
QWidget#geosiRoot {{ background: {t['page']}; }}
QLabel {{ color: {t['text']}; background: transparent; }}
QLabel#title {{ font-size: 15px; font-weight: 600; }}
QLabel#subtitle, QLabel#runText {{ color: {t['muted']}; font-size: 11px; }}

QPushButton#statusChip {{
    background: {t['raised']}; color: {t['text']}; border: 1px solid {t['border']};
    border-radius: 11px; padding: 2px 10px; font-size: 11px;
}}
QPushButton#statusChip:hover {{ border-color: {t['accent']}; }}

QToolButton#iconBtn {{
    background: transparent; color: {t['muted']}; border: none; border-radius: 6px;
    padding: 4px 6px; font-size: 14px;
}}
QToolButton#iconBtn:hover {{ background: {t['sunk']}; color: {t['text']}; }}

QFrame#notice {{ border-radius: 8px; }}
QFrame#notice[level="warning"] {{ background: {t['warn_bg']}; border: 1px solid {t['warn']}; }}
QFrame#notice[level="info"] {{ background: {t['sunk']}; border: 1px solid {t['border']}; }}
QLabel#noticeTitle {{ font-weight: 600; }}

QPushButton#primary {{
    background: {t['accent']}; color: {t['on_accent']}; border: none; border-radius: 6px;
    padding: 5px 12px; font-weight: 600;
}}
QPushButton#primary:hover {{ background: {t['accent_hover']}; }}
QPushButton#primary:disabled {{ background: {t['border']}; color: {t['faint']}; }}
QPushButton#secondary {{
    background: {t['raised']}; color: {t['text']}; border: 1px solid {t['border']};
    border-radius: 6px; padding: 5px 12px;
}}
QPushButton#secondary:hover {{ border-color: {t['accent']}; }}
QPushButton#danger {{
    background: {t['danger']}; color: #ffffff; border: none; border-radius: 6px;
    padding: 5px 12px; font-weight: 600;
}}

QTextBrowser#chat {{
    background: {t['page']}; color: {t['text']}; border: none; padding: 4px;
    selection-background-color: {t['accent']};
}}

QFrame#composer {{
    background: {t['raised']}; border: 1px solid {t['border']}; border-radius: 10px;
}}
QFrame#composer[focused="true"] {{ border-color: {t['accent']}; }}
QPlainTextEdit#prompt {{
    background: transparent; color: {t['text']}; border: none; font-size: 13px;
    selection-background-color: {t['accent']};
}}
QPushButton#chip {{
    background: {t['sunk']}; color: {t['muted']}; border: 1px solid {t['border']};
    border-radius: 10px; padding: 2px 8px; font-size: 11px;
}}
QPushButton#chip:hover {{ color: {t['text']}; border-color: {t['accent']}; }}

QProgressBar#runBar {{ background: {t['sunk']}; border: none; border-radius: 1px; }}
QProgressBar#runBar::chunk {{ background: {t['accent']}; border-radius: 1px; }}
"""
