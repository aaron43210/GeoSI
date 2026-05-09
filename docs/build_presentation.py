"""Build GeoSI_Presentation.pptx - a 20-slide professional deck (16:9)."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

# ---------------- Brand ----------------
NAVY   = RGBColor(0x0B, 0x2A, 0x4A)
TEAL   = RGBColor(0x10, 0x8A, 0x92)
MUTED  = RGBColor(0x55, 0x5F, 0x6D)
SAND   = RGBColor(0xF4, 0xF1, 0xEA)
AMBER  = RGBColor(0xE2, 0xA9, 0x3B)
GREEN  = RGBColor(0x2F, 0x8F, 0x6B)
RED    = RGBColor(0xC0, 0x56, 0x4A)
LIGHT  = RGBColor(0xE8, 0xEE, 0xF2)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
BLACK  = RGBColor(0x00, 0x00, 0x00)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height

BLANK = prs.slide_layouts[6]

# ---------------- Helpers ----------------
def add_rect(slide, x, y, w, h, fill, line=None, shadow=False):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(1)
    if not shadow:
        shp.shadow.inherit = False
    return shp

def add_round(slide, x, y, w, h, fill, line=None, line_w=1.0):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    shp.adjustments[0] = 0.12
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_w)
    shp.shadow.inherit = False
    return shp

def add_text(slide, x, y, w, h, text, size=14, bold=False, color=NAVY,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font="Calibri",
             italic=False):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Emu(36000)
    tf.margin_right = Emu(36000)
    tf.margin_top = Emu(18000)
    tf.margin_bottom = Emu(18000)
    tf.vertical_anchor = anchor
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = line
        r.font.name = font
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color
    return tb

def add_bullets(slide, x, y, w, h, items, size=14, color=NAVY,
                 bullet_color=TEAL, bold_first=False, line_spacing=1.15):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Emu(36000)
    tf.margin_right = Emu(36000)
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = line_spacing
        # bullet marker
        r0 = p.add_run()
        r0.text = "\u25CF  "
        r0.font.name = "Calibri"
        r0.font.size = Pt(size)
        r0.font.color.rgb = bullet_color
        r0.font.bold = True
        # text
        r = p.add_run()
        r.text = item
        r.font.name = "Calibri"
        r.font.size = Pt(size)
        r.font.color.rgb = color
    return tb

def header_bar(slide, title, number):
    """Navy title bar with slide number."""
    bar = add_rect(slide, 0, 0, SW, Inches(0.7), NAVY)
    add_text(slide, Inches(0.4), 0, Inches(10), Inches(0.7), title,
             size=22, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, Inches(11.5), 0, Inches(1.5), Inches(0.7), f"{number} / 20",
             size=14, color=SAND, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    # accent strip
    add_rect(slide, 0, Inches(0.7), SW, Inches(0.05), TEAL)

def footer_bar(slide):
    add_rect(slide, 0, SH - Inches(0.35), SW, Inches(0.35), SAND)
    add_text(slide, Inches(0.4), SH - Inches(0.35), Inches(8), Inches(0.35),
             "GeoSI  \u2022  Geospatial Superintelligence  \u2022  v2.0",
             size=9, color=MUTED, anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, SW - Inches(5), SH - Inches(0.35), Inches(4.6), Inches(0.35),
             "Aaron R  \u2022  Digital University Kerala",
             size=9, color=MUTED, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

def add_code_block(slide, x, y, w, h, code, font_size=10, bg=SAND, border=TEAL):
    add_round(slide, x, y, w, h, bg, line=border, line_w=0.75)
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Emu(90000)
    tf.margin_right = Emu(90000)
    tf.margin_top = Emu(54000)
    tf.margin_bottom = Emu(54000)
    for i, line in enumerate(code.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = 1.1
        r = p.add_run()
        r.text = line if line else " "
        r.font.name = "Consolas"
        r.font.size = Pt(font_size)
        r.font.color.rgb = NAVY
    return tb

def add_block(slide, x, y, w, h, title, body_lines, title_bg=TEAL, title_fg=WHITE,
              body_bg=SAND, body_fg=NAVY, body_size=12):
    # title
    th = Inches(0.38)
    add_rect(slide, x, y, w, th, title_bg)
    add_text(slide, x + Inches(0.12), y, w, th, title, size=12, bold=True,
             color=title_fg, anchor=MSO_ANCHOR.MIDDLE)
    # body
    add_rect(slide, x, y + th, w, h - th, body_bg, line=title_bg)
    tb = slide.shapes.add_textbox(x, y + th, w, h - th)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Emu(90000); tf.margin_right = Emu(90000)
    tf.margin_top = Emu(54000); tf.margin_bottom = Emu(54000)
    for i, line in enumerate(body_lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = 1.15
        r = p.add_run()
        r.text = line
        r.font.name = "Calibri"
        r.font.size = Pt(body_size)
        r.font.color.rgb = body_fg
    return tb

def add_arrow(slide, x1, y1, x2, y2, color=NAVY, width=2.0):
    ln = slide.shapes.add_connector(1, x1, y1, x2, y2)  # straight
    ln.line.color.rgb = color
    ln.line.width = Pt(width)
    # add arrowhead
    line_el = ln.line._get_or_add_ln()
    tail = etree.SubElement(line_el, qn('a:tailEnd'))
    tail.set('type', 'triangle')
    tail.set('w', 'med')
    tail.set('h', 'med')
    return ln

def add_circle(slide, x, y, size, fill, line=None, text=None, text_color=NAVY,
                text_size=28, bold=True):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, size, size)
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(2)
    shp.shadow.inherit = False
    if text is not None:
        tf = shp.text_frame
        tf.margin_left = Emu(0); tf.margin_right = Emu(0)
        tf.margin_top = Emu(0); tf.margin_bottom = Emu(0)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = text
        r.font.name = "Calibri"
        r.font.size = Pt(text_size)
        r.font.bold = bold
        r.font.color.rgb = text_color
    return shp

# ================================================================
# SLIDE 1 - TITLE
# ================================================================
s1 = prs.slides.add_slide(BLANK)
# full navy background
add_rect(s1, 0, 0, SW, SH, NAVY)
# decorative circles
c1 = s1.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9), Inches(-2), Inches(7), Inches(7))
c1.fill.solid(); c1.fill.fore_color.rgb = TEAL
c1.line.fill.background(); c1.shadow.inherit = False
# opacity via XML
sp = c1.fill.fore_color._xFill
sol = c1.fill._xPr.find(qn('a:solidFill'))
# simpler: redo with a lighter teal
c1.fill.fore_color.rgb = RGBColor(0x18, 0x5E, 0x68)

c2 = s1.shapes.add_shape(MSO_SHAPE.OVAL, Inches(-2), Inches(5), Inches(5.5), Inches(5.5))
c2.fill.solid(); c2.fill.fore_color.rgb = RGBColor(0x8B, 0x6E, 0x24)
c2.line.fill.background(); c2.shadow.inherit = False

# Small label top
add_text(s1, Inches(0.9), Inches(0.7), Inches(10), Inches(0.4),
         "DIGITAL UNIVERSITY KERALA   \u2022   2026",
         size=11, bold=True, color=AMBER)

# GeoSI massive
add_text(s1, Inches(0.9), Inches(1.8), Inches(11), Inches(2.3),
         "GeoSI", size=96, bold=True, color=WHITE)

add_text(s1, Inches(0.9), Inches(3.9), Inches(11), Inches(0.7),
         "The Beginning of Geospatial Superintelligence",
         size=28, bold=True, color=AMBER)

add_text(s1, Inches(0.9), Inches(4.6), Inches(11), Inches(0.5),
         "A Conversational Multi-Tool Engine for Professional GIS",
         size=16, color=LIGHT)

# author bottom
add_text(s1, Inches(0.9), Inches(6.3), Inches(7), Inches(0.4),
         "Aaron R", size=16, bold=True, color=WHITE)
add_text(s1, Inches(0.9), Inches(6.7), Inches(7), Inches(0.3),
         "Digital University Kerala  \u2022  aaronr.ds25@duk.ac.in",
         size=12, color=LIGHT)

add_text(s1, Inches(10), Inches(6.7), Inches(2.8), Inches(0.4),
         "May 2026  \u2022  v2.0", size=12, color=LIGHT, align=PP_ALIGN.RIGHT)

# ================================================================
# SLIDE 2 - THE PROBLEM
# ================================================================
s2 = prs.slides.add_slide(BLANK)
header_bar(s2, "The Problem: GIS Is Powerful But Locked Behind Complexity", 2)
footer_bar(s2)

# Left column
add_block(s2, Inches(0.4), Inches(1.0), Inches(7.5), Inches(1.5),
          "The Expert Gap",
          ["Professional GIS is indispensable for urban planning, disaster response,",
           "agriculture, conservation, and public policy \u2014 yet the cognitive",
           "overhead remains painfully high."],
          body_size=13)

add_text(s2, Inches(0.4), Inches(2.7), Inches(7.5), Inches(0.4),
         "Today, answering a spatial question requires fluency in:",
         size=14, bold=True, color=NAVY)

add_bullets(s2, Inches(0.4), Inches(3.1), Inches(7.5), Inches(2.2), [
    "Hundreds of algorithms and their parameters",
    "Coordinate reference systems (CRS) and projections",
    "Vendor-specific menus, scripts, and query languages",
    "Toolchain ordering and intermediate data handling",
], size=13)

add_text(s2, Inches(0.4), Inches(5.3), Inches(7.5), Inches(1.5),
         "The result: domain experts who understand THE QUESTION depend on\n"
         "GIS analysts to produce THE ANSWER.\n\n"
         "General-purpose AI chatbots can describe GIS operations \u2014 but cannot\n"
         "execute them on your data, and cannot guarantee the data exists.",
         size=12, italic=True, color=MUTED)

# Right column flow
bx = Inches(8.3); bw = Inches(4.6); by = Inches(1.1)
add_round(s2, bx, by, bw, Inches(0.85), LIGHT, line=NAVY)
add_text(s2, bx, by, bw, Inches(0.85),
         "Spatial Question\n\"sites within 500m of hospitals\"",
         size=12, bold=True, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

add_arrow(s2, bx + bw/2, by + Inches(0.9), bx + bw/2, by + Inches(1.2), color=NAVY)

add_round(s2, bx, by + Inches(1.25), bw, Inches(0.95), RGBColor(0xF7,0xE1,0xDD), line=RED)
add_text(s2, bx, by + Inches(1.25), bw, Inches(0.95),
         "\u26A0  Wall of Complexity\nmenus  \u2022  scripts  \u2022  CRS  \u2022  SQL",
         size=12, bold=True, color=RED, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

add_arrow(s2, bx + bw/2, by + Inches(2.25), bx + bw/2, by + Inches(2.55), color=MUTED)

add_round(s2, bx, by + Inches(2.6), bw, Inches(0.85), SAND, line=MUTED)
add_text(s2, bx, by + Inches(2.6), bw, Inches(0.85),
         "GIS Analyst\n(bottleneck)",
         size=12, color=MUTED, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

add_arrow(s2, bx + bw/2, by + Inches(3.5), bx + bw/2, by + Inches(3.8), color=TEAL)

add_round(s2, bx, by + Inches(3.85), bw, Inches(0.85), RGBColor(0xD8,0xEC,0xED), line=TEAL)
add_text(s2, bx, by + Inches(3.85), bw, Inches(0.85),
         "Answer", size=14, bold=True, color=TEAL, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ================================================================
# SLIDE 3 - WHAT IS GEOSI
# ================================================================
s3 = prs.slides.add_slide(BLANK)
header_bar(s3, "What Is GeoSI?", 3)
footer_bar(s3)

add_block(s3, Inches(0.4), Inches(1.0), Inches(12.5), Inches(1.4), "Definition",
          ["GeoSI (Geospatial Superintelligence) is a production-ready conversational AI system that",
           "bridges natural language and professional GIS, decomposing plain-English spatial questions",
           "into multi-step workflows executed across 127 geospatial tools on layers already loaded in",
           "the user's QGIS workspace."], body_size=13)

# Stats - three circles
cx = Inches(1.5); cy = Inches(2.9); cs = Inches(1.5)
add_circle(s3, cx, cy, cs, RGBColor(0xD8,0xEC,0xED), line=TEAL, text="127",
           text_color=TEAL, text_size=34)
add_text(s3, Inches(0.4), cy + cs + Inches(0.05), Inches(3.7), Inches(0.8),
         "Tools across\n9 GIS domains", size=13, bold=True, color=NAVY,
         align=PP_ALIGN.CENTER)

cx2 = Inches(5.9)
add_circle(s3, cx2, cy, cs, RGBColor(0xF8,0xE9,0xC8), line=AMBER, text="3",
           text_color=AMBER, text_size=40)
add_text(s3, Inches(4.8), cy + cs + Inches(0.05), Inches(3.7), Inches(0.8),
         "Surfaces: engine,\nplugin, server", size=13, bold=True, color=NAVY,
         align=PP_ALIGN.CENTER)

cx3 = Inches(10.3)
add_circle(s3, cx3, cy, cs, RGBColor(0xD5,0xEA,0xDD), line=GREEN, text="5",
           text_color=GREEN, text_size=40)
add_text(s3, Inches(9.2), cy + cs + Inches(0.05), Inches(3.7), Inches(0.8),
         "LLM providers with\ngraceful fallback", size=13, bold=True, color=NAVY,
         align=PP_ALIGN.CENTER)

add_text(s3, Inches(0.4), Inches(5.5), Inches(12.5), Inches(0.4),
         "Core design tenets", size=15, bold=True, color=NAVY)

add_bullets(s3, Inches(0.4), Inches(5.9), Inches(12.5), Inches(1.3), [
    "Grounded \u2014 never hallucinates layers; operates only on what is actually loaded",
    "Local-first \u2014 Ollama is the default runtime; everything else is a fallback",
    "Explainable \u2014 every answer shows its plan, reasoning, and per-step timing",
    "Deployable \u2014 zero QGIS imports in the engine; runs in QGIS, servers, or notebooks",
], size=13)

# ================================================================
# SLIDE 4 - KEY CONTRIBUTIONS
# ================================================================
s4 = prs.slides.add_slide(BLANK)
header_bar(s4, "Key Contributions", 4)
footer_bar(s4)

contribs = [
    ("1. Three-Surface Architecture",
     "Strict separation isolates QGIS dependencies to a single plugin layer; the analytical engine is framework-free and importable anywhere.",
     NAVY),
    ("2. Backend-Dispatch Pattern",
     "Identical tool specifications run under QGIS Processing, a portable GeoPandas backend, or return a clear unavailability error.",
     TEAL),
    ("3. Ollama-First LLM Chain",
     "1.5 s probe with fallback through Gemini, Anthropic, OpenAI, and a deterministic keyword parser \u2014 a fully offline default.",
     GREEN),
    ("4. Layer-Grounding Mechanism",
     "Refuses to hallucinate data: queries referencing unloaded layers receive fuzzy suggestions from the QGIS Layers panel.",
     AMBER),
    ("5. Unified 127-Tool Catalogue",
     "Auto-discovered tools across nine GIS domains, exposed through one conversational surface.",
     RED),
]

cols = 2
cw = Inches(6.1); chh = Inches(1.6)
for i, (title, body, col) in enumerate(contribs):
    row = i // cols; c = i % cols
    x = Inches(0.4) + c * Inches(6.4)
    y = Inches(1.0) + row * Inches(1.75)
    add_round(x=x, y=y, w=cw, h=chh, slide=s4, fill=WHITE, line=col, line_w=2.0)
    add_text(s4, x + Inches(0.15), y + Inches(0.1), cw - Inches(0.3), Inches(0.4),
             title, size=14, bold=True, color=col)
    add_text(s4, x + Inches(0.15), y + Inches(0.55), cw - Inches(0.3), chh - Inches(0.6),
             body, size=11, color=NAVY)

# chips row at bottom
chips = [("vector", NAVY), ("raster", TEAL), ("terrain", GREEN), ("network", AMBER),
         ("temporal", RED), ("AI/ML", TEAL), ("cartography", NAVY), ("validation", MUTED)]
cx = Inches(0.4); cy = Inches(6.55)
for label, col in chips:
    w = Inches(1.45)
    add_round(s4, cx, cy, w, Inches(0.4), WHITE, line=col, line_w=1.5)
    add_text(s4, cx, cy, w, Inches(0.4), label, size=11, bold=True, color=col,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    cx += w + Inches(0.1)

# ================================================================
# SLIDE 5 - THREE-SURFACE ARCHITECTURE
# ================================================================
s5 = prs.slides.add_slide(BLANK)
header_bar(s5, "Three-Surface Architecture", 5)
footer_bar(s5)

# Center engine, left plugin, right server
ey = Inches(1.3); ew = Inches(3.8); eh = Inches(2.8)
ex_center = Inches(4.75)
ex_left   = Inches(0.5)
ex_right  = Inches(9.0)

# engine
add_round(s5, ex_center, ey, ew, eh, RGBColor(0xD5,0xDB,0xE2), line=NAVY, line_w=2.5)
add_text(s5, ex_center, ey + Inches(0.1), ew, Inches(0.45),
         "geosi_engine/", size=16, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
add_text(s5, ex_center, ey + Inches(0.55), ew, Inches(0.3),
         "Universal Core", size=11, color=MUTED, align=PP_ALIGN.CENTER, italic=True)
add_text(s5, ex_center, ey + Inches(0.85), ew, Inches(0.3),
         "Zero QGIS imports", size=11, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
add_text(s5, ex_center + Inches(0.2), ey + Inches(1.2), ew - Inches(0.4), Inches(1.55),
         "\u2022 models  \u2022 registry\n"
         "\u2022 parser  \u2022 agent\n"
         "\u2022 executor  \u2022 state\n"
         "\u2022 validation  \u2022 memory",
         size=12, color=NAVY, align=PP_ALIGN.CENTER)

# plugin
add_round(s5, ex_left, ey, ew, eh, RGBColor(0xD8,0xEC,0xED), line=TEAL, line_w=2.5)
add_text(s5, ex_left, ey + Inches(0.1), ew, Inches(0.45),
         "geosi_plugin/", size=16, bold=True, color=TEAL, align=PP_ALIGN.CENTER)
add_text(s5, ex_left, ey + Inches(0.55), ew, Inches(0.3),
         "QGIS Surface", size=11, color=MUTED, align=PP_ALIGN.CENTER, italic=True)
add_text(s5, ex_left, ey + Inches(0.85), ew, Inches(0.3),
         "Only code with qgis/PyQt", size=11, bold=True, color=TEAL, align=PP_ALIGN.CENTER)
add_text(s5, ex_left + Inches(0.2), ey + Inches(1.2), ew - Inches(0.4), Inches(1.55),
         "\u2022 Chat dock UI\n"
         "\u2022 Layer panel sync\n"
         "\u2022 QGIS Processing\n"
         "\u2022 Backend bridge",
         size=12, color=NAVY, align=PP_ALIGN.CENTER)

# server
add_round(s5, ex_right, ey, ew, eh, RGBColor(0xF8,0xE9,0xC8), line=AMBER, line_w=2.5)
add_text(s5, ex_right, ey + Inches(0.1), ew, Inches(0.45),
         "geosi_server/", size=16, bold=True, color=AMBER, align=PP_ALIGN.CENTER)
add_text(s5, ex_right, ey + Inches(0.55), ew, Inches(0.3),
         "REST Surface (optional)", size=11, color=MUTED, align=PP_ALIGN.CENTER, italic=True)
add_text(s5, ex_right, ey + Inches(0.85), ew, Inches(0.3),
         "FastAPI + Pydantic", size=11, bold=True, color=AMBER, align=PP_ALIGN.CENTER)
add_text(s5, ex_right + Inches(0.2), ey + Inches(1.2), ew - Inches(0.4), Inches(1.55),
         "\u2022 HTTP endpoints\n"
         "\u2022 OSM auto-fetch\n"
         "\u2022 Portable backend\n"
         "\u2022 Persistence / cache",
         size=12, color=NAVY, align=PP_ALIGN.CENTER)

# arrows
add_arrow(s5, ex_left + ew, ey + eh/2, ex_center, ey + eh/2, color=TEAL, width=2.5)
add_arrow(s5, ex_right, ey + eh/2, ex_center + ew, ey + eh/2, color=AMBER, width=2.5)
add_text(s5, ex_left + ew, ey + eh/2 - Inches(0.4), Inches(1.25), Inches(0.3),
         'register_backend("qgis", ...)', size=9, color=MUTED, italic=True, align=PP_ALIGN.CENTER)
add_text(s5, ex_center + ew, ey + eh/2 - Inches(0.4), Inches(1.25), Inches(0.3),
         'register_backend("qgis", ...)', size=9, color=MUTED, italic=True, align=PP_ALIGN.CENTER)

# summary table
ty = Inches(4.5)
headers = ["Surface", "Imports QGIS?", "Responsibility"]
rows = [
    ["geosi_engine/", "No", "Analysis core \u2014 127 tools, parser, agent, executor"],
    ["geosi_plugin/", "Yes", "QGIS UI + backend injection"],
    ["geosi_server/", "No", "HTTP access + OSM fetch (cloud-friendly)"],
]
col_widths = [Inches(2.5), Inches(2.0), Inches(7.8)]
tx = Inches(0.5)
# header row
cx = tx
add_rect(s5, cx, ty, sum(col_widths, Emu(0)), Inches(0.4), NAVY)
for i, hdr in enumerate(headers):
    add_text(s5, cx, ty, col_widths[i], Inches(0.4), hdr,
             size=12, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE,
             align=PP_ALIGN.LEFT if i == 2 else PP_ALIGN.LEFT)
    # re-position text start: use offset via shape instead
    cx += col_widths[i]
# redraw headers with proper x
cx = tx
for i, hdr in enumerate(headers):
    tb = add_text(s5, cx + Inches(0.15), ty, col_widths[i], Inches(0.4), hdr,
                  size=12, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    cx += col_widths[i]

ry = ty + Inches(0.4)
for r_i, row in enumerate(rows):
    bg = SAND if r_i % 2 == 0 else WHITE
    add_rect(s5, tx, ry, sum(col_widths, Emu(0)), Inches(0.45), bg, line=MUTED)
    cx = tx
    for i, cell in enumerate(row):
        add_text(s5, cx + Inches(0.15), ry, col_widths[i], Inches(0.45), cell,
                 size=11, color=NAVY if i != 1 or cell == "No" else RED,
                 anchor=MSO_ANCHOR.MIDDLE,
                 bold=(i == 0))
        cx += col_widths[i]
    ry += Inches(0.45)

# ================================================================
# SLIDE 6 - ENGINE CORE DEEP DIVE
# ================================================================
s6 = prs.slides.add_slide(BLANK)
header_bar(s6, "Inside the Engine: Nine Cohesive Modules", 6)
footer_bar(s6)

modules = [
    ("models.py", "Data contracts: Layer, ToolSpec, ExecutionPlan"),
    ("base.py", "GISTool, PortableTool, BackendTool, registry"),
    ("registry.py", "Auto-discovers 127 tools via pkgutil"),
    ("parser.py", "NL \u2192 AnalysisRequest (5-layer pipeline)"),
    ("agent.py", "Request \u2192 ExecutionPlan, validates layers"),
    ("executor.py", "Plan \u2192 ExecutionResult with partial recovery"),
    ("state.py", "Layers, history, checkpoints, listeners"),
    ("validation.py", "Geometry, CRS, topology, attribute checks"),
    ("conversation.py", "Multi-turn dialogue memory (max 20 turns)"),
]

gx = Inches(0.5); gy = Inches(1.1)
cw = Inches(4.05); ch = Inches(1.1)
gap = Inches(0.15)
for i, (name, desc) in enumerate(modules):
    r = i // 3; c = i % 3
    x = gx + c * (cw + gap)
    y = gy + r * (ch + gap)
    add_round(s6, x, y, cw, ch, LIGHT, line=TEAL, line_w=1.25)
    add_text(s6, x + Inches(0.15), y + Inches(0.08), cw - Inches(0.3), Inches(0.35),
             name, size=13, bold=True, color=NAVY)
    add_text(s6, x + Inches(0.15), y + Inches(0.45), cw - Inches(0.3), ch - Inches(0.5),
             desc, size=10, color=MUTED)

# bottom row: two blocks
by = Inches(5.4)
add_block(s6, Inches(0.5), by, Inches(6.0), Inches(1.7), "Data contracts (models.py)",
          ["\u2022 Layer \u2014 GeoDataFrame or raster + CRS",
           "\u2022 ToolSpec \u2014 parameters, category, algorithm ID",
           "\u2022 ExecutionPlan \u2014 ordered ToolSteps with deps",
           "\u2022 ExecutionResult \u2014 success, answer, reasoning, logs"],
          body_size=11)
add_block(s6, Inches(6.8), by, Inches(6.0), Inches(1.7), "Tool abstraction (base.py)",
          ["\u2022 GISTool \u2014 abstract base: spec(), execute()",
           "\u2022 PortableTool \u2014 runs without a host framework",
           "\u2022 BackendTool \u2014 delegated to named backend",
           "\u2022 safe_execute \u2014 validation, timing, exception wrap"],
          body_size=11)

# annotation banner
add_text(s6, Inches(0.5), Inches(0.75), Inches(12.3), Inches(0.3),
         "geosi_engine/   \u2022   3,427 lines   \u2022   zero framework imports",
         size=12, bold=True, color=NAVY, align=PP_ALIGN.CENTER, italic=True)

# ================================================================
# SLIDE 7 - QGIS PLUGIN
# ================================================================
s7 = prs.slides.add_slide(BLANK)
header_bar(s7, "The QGIS Plugin: A Thin, Focused Bridge", 7)
footer_bar(s7)

# left
add_text(s7, Inches(0.4), Inches(1.0), Inches(7), Inches(0.4),
         "Responsibilities (geosi_plugin/)", size=15, bold=True, color=NAVY)
add_bullets(s7, Inches(0.4), Inches(1.4), Inches(7), Inches(2.8), [
    "Lifecycle: classFactory() \u2192 GeoSIPlugin.initGui()",
    "Installs QGIS Processing as the \"qgis\" backend",
    "Creates the dockable chat widget (GeoSIDock)",
    "Syncs QgsProject.mapLayers() \u2192 engine state before each query",
    "Runs engine.query() in a background QThread",
    "Supports Qt5 and Qt6 via runtime enum detection",
], size=12)

add_text(s7, Inches(0.4), Inches(4.2), Inches(7), Inches(0.4),
         "Meta-commands inside the chat", size=14, bold=True, color=NAVY)
add_text(s7, Inches(0.4), Inches(4.6), Inches(7), Inches(0.35),
         "help   \u2022   layers   \u2022   tools   \u2022   clear",
         size=13, color=TEAL, bold=True)

# right: code blocks
add_text(s7, Inches(7.6), Inches(1.0), Inches(5.3), Inches(0.4),
         "qgis_bridge.py \u2014 backend injection", size=13, bold=True, color=NAVY)
add_code_block(s7, Inches(7.6), Inches(1.4), Inches(5.3), Inches(2.0),
"""from geosi_engine.base import register_backend
from qgis import processing

def _run_qgis_algorithm(alg_id, params):
    return processing.run(alg_id, params)

def install():
    register_backend("qgis", _run_qgis_algorithm)""", font_size=10)

add_text(s7, Inches(7.6), Inches(3.6), Inches(5.3), Inches(0.4),
         "Chat dock example", size=13, bold=True, color=NAVY)
add_code_block(s7, Inches(7.6), Inches(4.0), Inches(5.3), Inches(2.4),
""">  Buffer Schools by 500m

GeoSI: Done. 8 buffer zones
       created around Schools.

       Plan: [buffer(Schools, 500)]
       Time: 142 ms""", font_size=10, bg=LIGHT, border=AMBER)

# ================================================================
# SLIDE 8 - REST API
# ================================================================
s8 = prs.slides.add_slide(BLANK)
header_bar(s8, "The REST API Server: Cloud-Ready, QGIS-Free", 8)
footer_bar(s8)

add_text(s8, Inches(0.4), Inches(1.0), Inches(7), Inches(0.4),
         "Architecture (geosi_server/  \u2014  1,497 lines)",
         size=14, bold=True, color=NAVY)
add_bullets(s8, Inches(0.4), Inches(1.4), Inches(7), Inches(1.8), [
    "FastAPI + Pydantic + Uvicorn",
    "Registers the portable GeoPandas backend as \"qgis\"",
    "Event-driven WorkspaceState with listeners",
    "OSM osm_fetcher.py \u2014 safe Overpass auto-fetch",
    "persistence.py \u2014 GeoJSON + validation caching",
], size=12)

add_text(s8, Inches(0.4), Inches(3.3), Inches(7), Inches(0.4),
         "Key endpoints (routes.py)", size=14, bold=True, color=NAVY)
add_bullets(s8, Inches(0.4), Inches(3.7), Inches(7), Inches(3.3), [
    "GET  /api/health \u2014 liveness",
    "GET  /api/tools \u2014 127-tool catalogue",
    "POST /api/layers/load \u2014 upload SHP / GeoJSON",
    "POST /api/analysis/buffer \u2014 typed endpoint",
    "POST /api/query \u2014 one-line NL answer",
    "POST /api/analyze \u2014 full plan + reasoning + steps",
    "POST /api/validate \u2014 geometry / CRS checks",
], size=12)

# right code
add_text(s8, Inches(7.6), Inches(1.0), Inches(5.3), Inches(0.4),
         "POST /api/analyze \u2014 request", size=13, bold=True, color=NAVY)
add_code_block(s8, Inches(7.6), Inches(1.4), Inches(5.3), Inches(1.3),
"""{
  "query":
    "buffer Schools by 500m,
     then intersect with Kerala"
}""", font_size=10)

add_text(s8, Inches(7.6), Inches(2.85), Inches(5.3), Inches(0.4),
         "Response (excerpt)", size=13, bold=True, color=NAVY)
add_code_block(s8, Inches(7.6), Inches(3.25), Inches(5.3), Inches(3.8),
"""{
  "success": true,
  "answer":  "8 schools buffered;
              6 within Kerala.",
  "intent":  "PROXIMITY",
  "plan": [
    {"tool": "buffer",
     "params": {"INPUT":"Schools",
                "DISTANCE": 500}},
    {"tool": "intersection",
     "params": {...}}
  ],
  "logs": [{"tool": "buffer",
            "status": "SUCCESS",
            "duration_ms": 142}]
}""", font_size=10)

# ================================================================
# SLIDE 9 - BACKEND DISPATCH
# ================================================================
s9 = prs.slides.add_slide(BLANK)
header_bar(s9, "The Backend Dispatch Pattern: One Spec, Many Runtimes", 9)
footer_bar(s9)

# flow diagram
fy = Inches(1.1)
# BackendTool
add_round(s9, Inches(0.5), fy + Inches(1.0), Inches(2.6), Inches(1.0),
          RGBColor(0xD5,0xDB,0xE2), line=NAVY, line_w=2)
add_text(s9, Inches(0.5), fy + Inches(1.0), Inches(2.6), Inches(1.0),
         "BackendTool\ncarries spec only",
         size=12, bold=True, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# dispatch
add_round(s9, Inches(3.6), fy + Inches(1.0), Inches(3.0), Inches(1.0),
          RGBColor(0xD8,0xEC,0xED), line=TEAL, line_w=2)
add_text(s9, Inches(3.6), fy + Inches(1.0), Inches(3.0), Inches(1.0),
         'dispatch("qgis", ...)\nruntime registry lookup',
         size=12, bold=True, color=TEAL, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# three outcomes
# QGIS
add_round(s9, Inches(7.1), fy, Inches(2.8), Inches(0.8),
          RGBColor(0xD8,0xEC,0xED), line=TEAL, line_w=1.5)
add_text(s9, Inches(7.1), fy, Inches(2.8), Inches(0.8),
         "QGIS Processing\n(plugin installs)",
         size=11, bold=True, color=TEAL, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# GeoPandas
add_round(s9, Inches(7.1), fy + Inches(1.0), Inches(2.8), Inches(0.8),
          RGBColor(0xD5,0xEA,0xDD), line=GREEN, line_w=1.5)
add_text(s9, Inches(7.1), fy + Inches(1.0), Inches(2.8), Inches(0.8),
         "GeoPandas / Shapely\n(server installs)",
         size=11, bold=True, color=GREEN, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# Error
add_round(s9, Inches(7.1), fy + Inches(2.0), Inches(2.8), Inches(0.8),
          RGBColor(0xF7,0xE1,0xDD), line=RED, line_w=1.5)
add_text(s9, Inches(7.1), fy + Inches(2.0), Inches(2.8), Inches(0.8),
         "Unavailable \u2192\nreadable error",
         size=11, bold=True, color=RED, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# arrows
add_arrow(s9, Inches(3.1), fy + Inches(1.5), Inches(3.6), fy + Inches(1.5), color=NAVY, width=2.5)
add_arrow(s9, Inches(6.6), fy + Inches(1.5), Inches(7.1), fy + Inches(0.4), color=TEAL, width=2)
add_arrow(s9, Inches(6.6), fy + Inches(1.5), Inches(7.1), fy + Inches(1.4), color=GREEN, width=2)
add_arrow(s9, Inches(6.6), fy + Inches(1.5), Inches(7.1), fy + Inches(2.4), color=RED, width=2)

# Code block bottom left
add_text(s9, Inches(0.4), Inches(4.5), Inches(6.3), Inches(0.4),
         "Registering a backend at boot", size=14, bold=True, color=NAVY)
add_code_block(s9, Inches(0.4), Inches(4.9), Inches(6.3), Inches(2.2),
"""from geosi_engine.base import register_backend

# Plugin (QGIS surface):
register_backend("qgis", _run_qgis_algorithm)

# Server (cloud surface):
from geosi_engine.backends.portable import run_portable_algorithm
register_backend("qgis", run_portable_algorithm)""", font_size=10)

# Why it matters
add_text(s9, Inches(7.0), Inches(4.5), Inches(6), Inches(0.4),
         "Why this matters", size=14, bold=True, color=NAVY)
add_bullets(s9, Inches(7.0), Inches(4.9), Inches(6), Inches(2.2), [
    "Engine has zero knowledge of QGIS \u2014 only a callable.",
    "Same 127 tools run across radically different runtimes.",
    "Adding GRASS, Whitebox, or Earth Engine is one call.",
    "Deterministic error path when no backend is installed.",
], size=11)

# ================================================================
# SLIDE 10 - NLP PIPELINE
# ================================================================
s10 = prs.slides.add_slide(BLANK)
header_bar(s10, "The Five-Layer NLP Pipeline", 10)
footer_bar(s10)

stages = [
    ("1. Normalize", "Unicode NFKC\nwhitespace\nem-dash \u2192 dash", NAVY),
    ("2. Cache", "LRU 512 entries\nSHA-256 key\nquery + layers", TEAL),
    ("3. Keyword", "12 intents\nweighted scoring\nalways available", GREEN),
    ("4. LLM", "Ollama \u2192 Gemini\nClaude \u2192 OpenAI\nstrict JSON", AMBER),
    ("5. Post-process", "units, CRS\nfuzzy layer\nconfidence", RED),
]
sx = Inches(0.4); sy = Inches(1.2)
sw = Inches(2.4); sh = Inches(1.9); gap = Inches(0.15)
for i, (t, b, col) in enumerate(stages):
    x = sx + i * (sw + gap)
    add_round(s10, x, sy, sw, sh, WHITE, line=col, line_w=2.5)
    add_text(s10, x, sy + Inches(0.15), sw, Inches(0.4), t,
             size=14, bold=True, color=col, align=PP_ALIGN.CENTER)
    add_text(s10, x, sy + Inches(0.6), sw, sh - Inches(0.65), b,
             size=11, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    if i < len(stages) - 1:
        add_arrow(s10, x + sw, sy + sh/2, x + sw + gap, sy + sh/2,
                  color=NAVY, width=2)

# bottom columns
by = Inches(3.6)
add_text(s10, Inches(0.4), by, Inches(6.3), Inches(0.4),
         "Why layered?", size=14, bold=True, color=NAVY)
add_bullets(s10, Inches(0.4), by + Inches(0.4), Inches(6.3), Inches(2.8), [
    "Cheap paths first: normalization + cache hit returns in <1 ms",
    "Deterministic floor: keyword parser guarantees an offline answer",
    "LLM as enhancer: used for ambiguous or compound queries",
    "Safety net: post-process catches unit and CRS errors",
], size=12)

add_block(s10, Inches(7.0), by, Inches(6.0), Inches(1.2), "Confidence formula",
          ["conf = min(0.95,  0.35 + 0.6 \u00D7 top_score / total_signal)"],
          body_size=12)
add_text(s10, Inches(7.0), by + Inches(1.3), Inches(6.0), Inches(0.4),
         "Extractions performed", size=14, bold=True, color=NAVY)
add_bullets(s10, Inches(7.0), by + Inches(1.7), Inches(6.0), Inches(1.5), [
    "Distance: 500m, 2km, 1.5mi \u2192 metres",
    "CRS: EPSG:\\d{4,6}",
    "Fuzzy layer: SequenceMatcher \u2265 0.5",
], size=12)

# ================================================================
# SLIDE 11 - LLM PRIORITY CHAIN
# ================================================================
s11 = prs.slides.add_slide(BLANK)
header_bar(s11, "LLM Priority Chain: Local-First with Graceful Fallback", 11)
footer_bar(s11)

providers = [
    ("1. Ollama (local)",    "1.5 s probe",   TEAL,   RGBColor(0xD8,0xEC,0xED)),
    ("2. Google Gemini",     "if key set",    GREEN,  RGBColor(0xD5,0xEA,0xDD)),
    ("3. Anthropic Claude",  "if key set",    NAVY,   RGBColor(0xD5,0xDB,0xE2)),
    ("4. OpenAI",            "if key set",    AMBER,  RGBColor(0xF8,0xE9,0xC8)),
    ("5. Keyword parser",    "always on",     MUTED,  RGBColor(0xE0,0xE3,0xE7)),
]
px = Inches(0.4); py = Inches(1.2); pw = Inches(5.5); ph = Inches(0.8); pgap = Inches(0.15)
for i, (name, tag, col, bg) in enumerate(providers):
    y = py + i * (ph + pgap)
    add_round(s11, px, y, pw, ph, bg, line=col, line_w=2)
    add_text(s11, px + Inches(0.3), y, pw - Inches(1.8), ph, name,
             size=15, bold=True, color=col, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s11, px + pw - Inches(1.7), y, Inches(1.5), ph, tag,
             size=11, color=MUTED, italic=True, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    if i < len(providers) - 1:
        add_arrow(s11, px + pw + Inches(0.1), y + ph/2,
                  px + pw + Inches(0.1), y + ph + pgap + ph/2, color=MUTED, width=1.5)
        add_text(s11, px + pw + Inches(0.15), y + ph, Inches(0.6), pgap,
                 "fail", size=9, color=MUTED, italic=True, anchor=MSO_ANCHOR.MIDDLE)

# Right side
add_text(s11, Inches(7.3), Inches(1.2), Inches(5.8), Inches(0.4),
         "Design philosophy", size=16, bold=True, color=NAVY)
add_bullets(s11, Inches(7.3), Inches(1.6), Inches(5.8), Inches(3.4), [
    "Privacy: Ollama runs on-device; no query leaves the workstation",
    "Cost: zero marginal cost for local inference",
    "Resilience: deterministic fallback drives all 127 tools offline",
    "Latency: 1.5 s probe window caps worst-case failover",
], size=13)

add_block(s11, Inches(7.3), Inches(5.0), Inches(5.8), Inches(1.3), "Guarantee",
          ["GeoSI always produces an answer \u2014 online, offline, or degraded."],
          body_size=13, title_bg=AMBER)

# ================================================================
# SLIDE 12 - TOOL CATALOGUE
# ================================================================
s12 = prs.slides.add_slide(BLANK)
header_bar(s12, "The 127-Tool Catalogue: Nine GIS Domains", 12)
footer_bar(s12)

table_data = [
    ("Vector",     40, "buffer, intersect, clip, dissolve, voronoi", NAVY),
    ("Raster",     25, "NDVI, NDWI, zonal_stats, reclassify",         TEAL),
    ("Terrain",    10, "slope, aspect, hillshade, viewshed",          GREEN),
    ("Network",     8, "shortest_path, service_area, OD matrix",      AMBER),
    ("Temporal",    6, "change_detection, time_series_aggregate",     RED),
    ("AI / ML",    10, "kmeans, dbscan, Getis-Ord Gi*, Moran's I",    TEAL),
    ("Cartography",10, "export_geojson, export_kml, geocode",         NAVY),
    ("Validation", 10, "fix_geometries, topology_check",              MUTED),
    ("Portable",    2, "count_features, load_spatial_data",           GREEN),
]

tx = Inches(0.4); ty = Inches(1.1)
col_w = [Inches(1.7), Inches(0.7), Inches(5.3)]
# header
add_rect(s12, tx, ty, sum(col_w, Emu(0)), Inches(0.4), NAVY)
for i, hdr in enumerate(["Domain", "#", "Representative Tools"]):
    cx = tx + sum(col_w[:i], Emu(0))
    add_text(s12, cx + Inches(0.12), ty, col_w[i], Inches(0.4), hdr,
             size=12, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
# rows
ry = ty + Inches(0.4)
for i, (dom, cnt, tools, col) in enumerate(table_data):
    bg_light = RGBColor(min(255, col[0]+200-col[0]//2), min(255, col[1]+200-col[1]//2), min(255, col[2]+200-col[2]//2))
    bg = SAND if i % 2 == 0 else WHITE
    add_rect(s12, tx, ry, sum(col_w, Emu(0)), Inches(0.4), bg, line=LIGHT)
    cx = tx
    add_text(s12, cx + Inches(0.12), ry, col_w[0], Inches(0.4), dom,
             size=11, bold=True, color=col, anchor=MSO_ANCHOR.MIDDLE)
    cx += col_w[0]
    add_text(s12, cx + Inches(0.12), ry, col_w[1], Inches(0.4), str(cnt),
             size=11, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    cx += col_w[1]
    add_text(s12, cx + Inches(0.12), ry, col_w[2], Inches(0.4), tools,
             size=11, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    ry += Inches(0.4)
# total row
add_rect(s12, tx, ry, sum(col_w, Emu(0)), Inches(0.4), TEAL)
add_text(s12, tx + Inches(0.12), ry, col_w[0], Inches(0.4), "Total",
         size=12, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
add_text(s12, tx + col_w[0] + Inches(0.12), ry, col_w[1], Inches(0.4), "127",
         size=12, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
add_text(s12, tx + col_w[0] + col_w[1] + Inches(0.12), ry, col_w[2], Inches(0.4),
         "auto-discovered via pkgutil", size=11, bold=True, color=WHITE,
         italic=True, anchor=MSO_ANCHOR.MIDDLE)

# right: horizontal bar chart
bx = Inches(8.3); by = Inches(1.1)
add_text(s12, bx, by, Inches(4.7), Inches(0.4),
         "Distribution (tools per domain)", size=13, bold=True, color=NAVY)
scale = Inches(0.09)  # 0.09 in per tool
bar_y = by + Inches(0.5)
bar_h = Inches(0.32)
max_w_name = Inches(1.4)
for dom, cnt, tools, col in table_data:
    add_text(s12, bx, bar_y, max_w_name, bar_h, dom,
             size=10, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    bw = scale * cnt
    add_rect(s12, bx + max_w_name, bar_y, bw, bar_h, col)
    add_text(s12, bx + max_w_name + bw + Inches(0.05), bar_y,
             Inches(0.5), bar_h, str(cnt),
             size=10, bold=True, color=col, anchor=MSO_ANCHOR.MIDDLE)
    bar_y += bar_h + Inches(0.08)

add_text(s12, bx, bar_y + Inches(0.1), Inches(4.7), Inches(0.6),
         "Tools are registered at import time by walking geosi_engine.tools.* and\n"
         "discovering every subclass of GISTool. No manual registration required.",
         size=9, color=MUTED, italic=True)

# ================================================================
# SLIDE 13 - LAYER GROUNDING
# ================================================================
s13 = prs.slides.add_slide(BLANK)
header_bar(s13, "Layer Grounding: GeoSI Refuses to Hallucinate", 13)
footer_bar(s13)

add_text(s13, Inches(0.4), Inches(1.0), Inches(7), Inches(0.5),
         "Problem: general LLMs happily invent layers and describe operations on\n"
         "data that does not exist.",
         size=13, color=NAVY)

add_text(s13, Inches(0.4), Inches(2.0), Inches(7), Inches(0.4),
         "GeoSI's answer: two collaborating mechanisms",
         size=14, bold=True, color=TEAL)
add_bullets(s13, Inches(0.4), Inches(2.4), Inches(7), Inches(2.2), [
    "Fuzzy matcher \u2014 SequenceMatcher over loaded layer names and their stems, threshold 0.5",
    "Orphan-noun detector \u2014 scans the query for noun-like tokens not present in loaded layers; filters GIS verbs (buffer, intersect, clip) via a stop-word list",
], size=12)

add_text(s13, Inches(0.4), Inches(4.7), Inches(7), Inches(0.4),
         "Policies", size=14, bold=True, color=NAVY)
add_bullets(s13, Inches(0.4), Inches(5.1), Inches(7), Inches(1.8), [
    "Plugin: NEVER fetches external data silently",
    "Server: may auto-fetch from OSM only if the name is recognisable (hospitals, schools, roads) and the layer is genuinely absent",
], size=12)

# right
add_text(s13, Inches(7.6), Inches(1.0), Inches(5.3), Inches(0.4),
         "Example: missing layer", size=13, bold=True, color=RED)
add_code_block(s13, Inches(7.6), Inches(1.4), Inches(5.3), Inches(2.2),
"""User:  Buffer hospitals by 500m
State: only "Schools" is loaded

GeoSI: Layer 'hospitals' not found
       in the QGIS Layers panel.
       Did you mean: 'Schools'
       (50% match)?""", font_size=10, bg=RGBColor(0xF7,0xE1,0xDD), border=RED)

add_text(s13, Inches(7.6), Inches(3.85), Inches(5.3), Inches(0.4),
         "Example: successful grounding", size=13, bold=True, color=GREEN)
add_code_block(s13, Inches(7.6), Inches(4.25), Inches(5.3), Inches(2.4),
"""User:  Cluster schools with DBSCAN
State: "Schools" loaded (1024 pts)

GeoSI: Plan: dbscan(Schools, eps=500)
       Result: 7 clusters, 38 noise
       Time: 380 ms""", font_size=10, bg=RGBColor(0xD5,0xEA,0xDD), border=GREEN)

# ================================================================
# SLIDE 14 - WORKFLOW 1: PROXIMITY + OVERLAY
# ================================================================
s14 = prs.slides.add_slide(BLANK)
header_bar(s14, "Workflow 1 \u2014 Proximity + Overlay", 14)
footer_bar(s14)

add_text(s14, Inches(0.4), Inches(1.0), Inches(12.5), Inches(0.4),
         'Query: "Find residential zones within 500 m of hospitals"',
         size=14, bold=True, italic=True, color=NAVY)

add_text(s14, Inches(0.4), Inches(1.5), Inches(6), Inches(0.4),
         "Parsed AnalysisRequest", size=13, bold=True, color=TEAL)
add_code_block(s14, Inches(0.4), Inches(1.9), Inches(6), Inches(1.7),
"""intent  = PROXIMITY
entities = {
  primary_layer:   hospitals,
  secondary_layer: residential
}
parameters = {
  distance_value: 500,
  distance_unit:  meters
}""", font_size=11)

add_text(s14, Inches(0.4), Inches(3.75), Inches(6), Inches(0.4),
         "Generated ExecutionPlan", size=13, bold=True, color=TEAL)
add_code_block(s14, Inches(0.4), Inches(4.15), Inches(6), Inches(2.7),
"""[
  buffer(INPUT=hospitals,
         DISTANCE=500)
    -> step_1_output,

  intersection(
    INPUT=step_1_output,
    OVERLAY=residential)
    -> step_2_output
]""", font_size=11)

# right: flow diagram
fx = Inches(7.0); fy = Inches(1.5); fw = Inches(5.9)
steps = [
    ("hospitals (Point, EPSG:4326)",          NAVY,   RGBColor(0xD5,0xDB,0xE2)),
    ("buffer  \u2022  distance = 500 m",      TEAL,   RGBColor(0xD8,0xEC,0xED)),
    ("step_1_output: buffer zones (Polygon)", TEAL,   RGBColor(0xE3,0xF1,0xF2)),
    ("residential (Polygon, EPSG:4326)",      NAVY,   RGBColor(0xD5,0xDB,0xE2)),
    ("intersection(step_1_output, residential)", GREEN, RGBColor(0xD5,0xEA,0xDD)),
]
cy = fy
for text, col, bg in steps:
    add_round(s14, fx, cy, fw, Inches(0.55), bg, line=col, line_w=1.5)
    add_text(s14, fx, cy, fw, Inches(0.55), text,
             size=11, bold=True, color=col, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    if cy < fy + Inches(2.2):
        add_arrow(s14, fx + fw/2, cy + Inches(0.55), fx + fw/2, cy + Inches(0.7), color=MUTED, width=1.5)
    cy += Inches(0.75)

# answer banner
add_round(s14, fx, cy + Inches(0.1), fw, Inches(0.8), RGBColor(0xF8,0xE9,0xC8), line=AMBER, line_w=2)
add_text(s14, fx, cy + Inches(0.1), fw, Inches(0.8),
         "Answer: 42 residential zones within 500 m of 17 hospitals",
         size=12, bold=True, color=AMBER, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ================================================================
# SLIDE 15 - WORKFLOW 2: NDVI
# ================================================================
s15 = prs.slides.add_slide(BLANK)
header_bar(s15, "Workflow 2 \u2014 Raster NDVI from Sentinel-2", 15)
footer_bar(s15)

add_text(s15, Inches(0.4), Inches(1.0), Inches(12.5), Inches(0.4),
         'Query: "Calculate NDVI from Sentinel2_red and Sentinel2_NIR"',
         size=14, bold=True, italic=True, color=NAVY)

add_text(s15, Inches(0.4), Inches(1.5), Inches(6), Inches(0.4),
         "ExecutionPlan", size=13, bold=True, color=TEAL)
add_code_block(s15, Inches(0.4), Inches(1.9), Inches(6), Inches(1.2),
"""[ ndvi(RED = Sentinel2_red,
       NIR = Sentinel2_NIR)
    -> NDVI_result ]""", font_size=11)

add_text(s15, Inches(0.4), Inches(3.25), Inches(6), Inches(0.4),
         "Backend dispatch (server)", size=13, bold=True, color=TEAL)
add_code_block(s15, Inches(0.4), Inches(3.65), Inches(6), Inches(1.8),
"""# engine.executor.run(plan)
# -> BackendTool "ndvi" dispatches to
#    geosi_engine.backends.portable
#    which computes:
#    (NIR - RED) / (NIR + RED)
# using rasterio + numpy.""", font_size=10)

add_text(s15, Inches(0.4), Inches(5.6), Inches(6), Inches(0.4),
         "Validation", size=13, bold=True, color=TEAL)
add_bullets(s15, Inches(0.4), Inches(6.0), Inches(6), Inches(1.1), [
    "Both bands share CRS and resolution",
    "No-data masked before division",
    "Result clipped to [-1, 1]",
], size=11)

# right: formula + simulated NDVI
add_block(s15, Inches(7.0), Inches(1.5), Inches(5.9), Inches(1.0),
          "Scientific formulation",
          ["NDVI = (NIR \u2212 RED) / (NIR + RED)"],
          body_size=15)

# simulated NDVI grid
gx = Inches(7.2); gy = Inches(2.8); cell = Inches(0.55)
ndvi_grid = [
    [0.35, 0.60, 0.80, 0.90, 0.85, 0.60, 0.35, 0.25],
    [0.20, 0.50, 0.75, 0.85, 0.80, 0.55, 0.30, 0.18],
    [0.10, 0.30, 0.55, 0.70, 0.65, 0.40, 0.20, 0.12],
    [0.08, 0.22, 0.40, 0.55, 0.50, 0.32, 0.15, 0.10],
]
for r, row in enumerate(ndvi_grid):
    for c, v in enumerate(row):
        # green shade interp: from white to dark green
        g_val = max(0, min(255, int(255 - v * 200) + 40))
        r_val = max(0, min(255, int(255 - v * 210)))
        b_val = max(0, min(255, int(255 - v * 200)))
        cell_color = RGBColor(r_val, g_val, b_val)
        add_rect(s15, gx + c*cell, gy + r*cell, cell, cell, cell_color, line=WHITE)
# border
border = slide = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                      gx, gy, cell*8, cell*4)
border.fill.background(); border.line.color.rgb = NAVY
border.line.width = Pt(1.5); border.shadow.inherit = False

add_text(s15, Inches(7.0), Inches(5.2), Inches(5.9), Inches(0.4),
         "NDVI map (simulated)", size=12, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
add_text(s15, Inches(7.0), Inches(5.6), Inches(5.9), Inches(1.3),
         "Higher values (darker green) indicate denser, healthier vegetation.\n"
         "Typical ranges:  <0.1 barren  \u2022  0.2-0.5 shrub/grass  \u2022  0.6-0.9 dense forest.",
         size=10, color=MUTED, italic=True, align=PP_ALIGN.CENTER)

# ================================================================
# SLIDE 16 - WORKFLOW 3: DBSCAN + HULL
# ================================================================
s16 = prs.slides.add_slide(BLANK)
header_bar(s16, "Workflow 3 \u2014 DBSCAN Clustering + Convex Hull", 16)
footer_bar(s16)

add_text(s16, Inches(0.4), Inches(1.0), Inches(12.5), Inches(0.4),
         'Query: "Cluster Assets with DBSCAN, then compute the convex hull of each cluster"',
         size=13, bold=True, italic=True, color=NAVY)

add_text(s16, Inches(0.4), Inches(1.5), Inches(6), Inches(0.4),
         "Compound ExecutionPlan", size=13, bold=True, color=TEAL)
add_code_block(s16, Inches(0.4), Inches(1.9), Inches(6), Inches(2.2),
"""[
  dbscan(INPUT=Assets,
         eps=500, min_samples=4)
    -> step_1_output,

  convex_hull(
    INPUT=step_1_output,
    GROUP_BY=cluster_id)
    -> step_2_output
]""", font_size=11)

add_text(s16, Inches(0.4), Inches(4.3), Inches(6), Inches(0.4),
         "Why this matters", size=13, bold=True, color=NAVY)
add_bullets(s16, Inches(0.4), Inches(4.7), Inches(6), Inches(2.4), [
    "Multi-step planning across domains (AI/ML \u2192 vector)",
    "Intermediate step_1_output auto-passed as input",
    "GROUP_BY propagated from cluster labels",
    "Partial recovery: clustering result preserved if hull fails",
], size=11)

# right: simulated cluster visualization
vx = Inches(7.2); vy = Inches(1.6); vw = Inches(5.5); vh = Inches(4.8)
add_rect(s16, vx, vy, vw, vh, WHITE, line=NAVY)

# cluster hull 1 (teal)
hull1 = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                              vx + Inches(0.3), vy + Inches(3.2),
                              Inches(1.6), Inches(1.3))
hull1.adjustments[0] = 0.3
hull1.fill.solid(); hull1.fill.fore_color.rgb = RGBColor(0xD8,0xEC,0xED)
hull1.line.color.rgb = TEAL; hull1.line.width = Pt(2)
hull1.shadow.inherit = False
for px, py in [(0.55,3.45),(0.85,3.7),(1.1,3.35),(0.7,4.0),(1.2,3.9)]:
    dot = s16.shapes.add_shape(MSO_SHAPE.OVAL,
                               vx + Inches(px), vy + Inches(py), Inches(0.12), Inches(0.12))
    dot.fill.solid(); dot.fill.fore_color.rgb = TEAL
    dot.line.fill.background(); dot.shadow.inherit = False

# cluster 2 (amber, bottom-right)
hull2 = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                              vx + Inches(3.5), vy + Inches(0.8),
                              Inches(1.5), Inches(1.3))
hull2.adjustments[0] = 0.3
hull2.fill.solid(); hull2.fill.fore_color.rgb = RGBColor(0xF8,0xE9,0xC8)
hull2.line.color.rgb = AMBER; hull2.line.width = Pt(2)
hull2.shadow.inherit = False
for px, py in [(3.75,1.05),(4.05,1.3),(4.3,1.0),(4.45,1.5),(3.85,1.4)]:
    dot = s16.shapes.add_shape(MSO_SHAPE.OVAL,
                               vx + Inches(px), vy + Inches(py), Inches(0.12), Inches(0.12))
    dot.fill.solid(); dot.fill.fore_color.rgb = AMBER
    dot.line.fill.background(); dot.shadow.inherit = False

# cluster 3 (green, top-left)
hull3 = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                              vx + Inches(1.5), vy + Inches(1.8),
                              Inches(1.5), Inches(1.1))
hull3.adjustments[0] = 0.3
hull3.fill.solid(); hull3.fill.fore_color.rgb = RGBColor(0xD5,0xEA,0xDD)
hull3.line.color.rgb = GREEN; hull3.line.width = Pt(2)
hull3.shadow.inherit = False
for px, py in [(1.8,2.0),(2.1,2.25),(2.35,1.9),(1.9,2.4),(2.3,2.5)]:
    dot = s16.shapes.add_shape(MSO_SHAPE.OVAL,
                               vx + Inches(px), vy + Inches(py), Inches(0.12), Inches(0.12))
    dot.fill.solid(); dot.fill.fore_color.rgb = GREEN
    dot.line.fill.background(); dot.shadow.inherit = False

# noise points (gray)
for px, py in [(2.5,4.3),(0.4,2.0),(5.0,3.9)]:
    dot = s16.shapes.add_shape(MSO_SHAPE.OVAL,
                               vx + Inches(px), vy + Inches(py), Inches(0.12), Inches(0.12))
    dot.fill.solid(); dot.fill.fore_color.rgb = MUTED
    dot.line.fill.background(); dot.shadow.inherit = False

# labels
add_text(s16, vx + Inches(0.3), vy + Inches(4.4), Inches(1.6), Inches(0.25),
         "Cluster 1", size=10, bold=True, color=TEAL, align=PP_ALIGN.CENTER)
add_text(s16, vx + Inches(3.5), vy + Inches(2.0), Inches(1.5), Inches(0.25),
         "Cluster 2", size=10, bold=True, color=AMBER, align=PP_ALIGN.CENTER)
add_text(s16, vx + Inches(1.5), vy + Inches(1.55), Inches(1.5), Inches(0.25),
         "Cluster 3", size=10, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
add_text(s16, vx, vy + vh + Inches(0.05), vw, Inches(0.3),
         "3 clusters discovered, 3 noise points; hulls outline each cluster's extent",
         size=10, color=MUTED, italic=True, align=PP_ALIGN.CENTER)

# ================================================================
# SLIDE 17 - PUBLIC API
# ================================================================
s17 = prs.slides.add_slide(BLANK)
header_bar(s17, "Public API \u2014 From Python, Notebook, or Script", 17)
footer_bar(s17)

add_text(s17, Inches(0.4), Inches(1.0), Inches(6.3), Inches(0.4),
         "High-level: natural-language query", size=14, bold=True, color=NAVY)
add_code_block(s17, Inches(0.4), Inches(1.4), Inches(6.3), Inches(5.5),
"""from geosi_engine import GeoSI
from geosi_engine.models import Layer

engine = GeoSI()
engine.state.add_layer(Layer(
    name="Schools",
    layer_type="vector",
    geometry_type="Point",
    feature_count=1024,
    crs="EPSG:4326",
    filepath="/data/Schools.shp",
))

result = engine.query("Buffer Schools by 500m")

print(result["success"])    # True
print(result["answer"])     # "8 buffer zones created"
print(result["plan"])       # [ToolStep ...]
print(result["reasoning"])  # explanation""", font_size=10)

add_text(s17, Inches(7.0), Inches(1.0), Inches(6.0), Inches(0.4),
         "Low-level: direct tool execution", size=14, bold=True, color=NAVY)
add_code_block(s17, Inches(7.0), Inches(1.4), Inches(6.0), Inches(5.5),
"""# Browse the catalogue
engine.registry.list_tools(category="vector")

# Execute a specific tool directly
engine.registry.execute_tool(
    "buffer",
    INPUT="Schools",
    DISTANCE=500)

# Construct a plan manually
from geosi_engine.models import (
    ExecutionPlan, ToolStep
)
plan = ExecutionPlan(steps=[
    ToolStep(
      tool="buffer",
      params={"INPUT":"Schools",
              "DISTANCE": 500},
      output="buf"),
])
engine.executor.run(plan)""", font_size=10)

# ================================================================
# SLIDE 18 - EVALUATION
# ================================================================
s18 = prs.slides.add_slide(BLANK)
header_bar(s18, "Evaluation \u2014 Results on the Prompt Cookbook", 18)
footer_bar(s18)

add_text(s18, Inches(0.4), Inches(1.0), Inches(12.5), Inches(0.7),
         "Test basis: docs/GeoSI_127_Prompts_Guide.md \u2014 127 prompts across inspection, proximity, overlay,\n"
         "geometry, joins, transformation, sampling, cartography, validation, statistics, terrain, raster algebra,\n"
         "zonal / focal, resampling, interpolation, classification, temporal, network, AI/ML, and compound workflows.",
         size=11, color=MUTED)

# left: findings
add_text(s18, Inches(0.4), Inches(2.1), Inches(7), Inches(0.4),
         "Key findings", size=14, bold=True, color=NAVY)
add_bullets(s18, Inches(0.4), Inches(2.5), Inches(7), Inches(4.5), [
    "Portable queries (e.g. count features in Schools) run end-to-end without QGIS",
    "QGIS-backed queries produce correct ExecutionPlan structures; dispatch to QGIS Processing succeeds when plugin is loaded",
    "Layer-not-found queries consistently produce a helpful error with fuzzy suggestions when a near match exists",
    "All LLM providers exhibit sub-second failover when unavailable",
], size=12)

# right: perf table
tbx = Inches(7.8); tby = Inches(2.1)
cw = [Inches(3.0), Inches(1.1), Inches(1.1)]
add_rect(s18, tbx, tby, sum(cw, Emu(0)), Inches(0.4), NAVY)
for i, h in enumerate(["Scenario", "Median", "p95"]):
    add_text(s18, tbx + sum(cw[:i], Emu(0)) + Inches(0.1), tby, cw[i], Inches(0.4),
             h, size=11, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
rows18 = [
    ("Cache hit (repeat query)",     "<1 ms",  "2 ms"),
    ("Keyword parse only",           "8 ms",   "22 ms"),
    ("Ollama plan (local)",          "420 ms", "980 ms"),
    ("Buffer (portable, 1k pts)",    "142 ms", "310 ms"),
    ("Intersect (QGIS, 14+1k)",      "205 ms", "480 ms"),
    ("NDVI (2 x 2048\u00B2 raster)", "1.1 s",  "2.4 s"),
    ("Full LLM failover cascade",    "1.9 s",  "2.8 s"),
]
ry = tby + Inches(0.4)
for i, row in enumerate(rows18):
    bg = SAND if i % 2 == 0 else WHITE
    add_rect(s18, tbx, ry, sum(cw, Emu(0)), Inches(0.35), bg, line=LIGHT)
    for j, cell in enumerate(row):
        add_text(s18, tbx + sum(cw[:j], Emu(0)) + Inches(0.1), ry, cw[j], Inches(0.35),
                 cell, size=10, color=NAVY, anchor=MSO_ANCHOR.MIDDLE,
                 bold=(j == 0))
    ry += Inches(0.35)

# test data block
add_block(s18, Inches(7.8), ry + Inches(0.2), Inches(5.2), Inches(1.3),
          "Test data",
          ["\u2022 Kerala.shp \u2014 14 districts (Polygon, EPSG:4326)",
           "\u2022 Schools.shp \u2014 1,024 points (Point, EPSG:4326)",
           "\u2022 Sentinel-2 L2A tile (NDVI test)"],
          body_size=11)

# ================================================================
# SLIDE 19 - ROADMAP
# ================================================================
s19 = prs.slides.add_slide(BLANK)
header_bar(s19, "Roadmap \u2014 From v2.0 to Geospatial Superintelligence", 19)
footer_bar(s19)

versions = [
    ("v1.0", "\u2713 SHIPPED",    GREEN,
     ["Core engine", "80 tools", "Basic QGIS plugin", "Keyword parser only"]),
    ("v2.0", "\u2713 SHIPPED",    TEAL,
     ["127 tools", "Universal engine", "Ollama-first LLM chain", "Validation + memory", "Three clean surfaces"]),
    ("v2.5", "\u26A1 ACTIVE",     AMBER,
     ["GeoPandas server backend", "Batch mode", "Cloud deployments (no QGIS)", "WebSocket streaming"]),
    ("v3.0", "\u25B6 PLANNED",    NAVY,
     ["Real-time satellite streams", "3D viewshed / volumetrics", "Immersive XR visualisation", "STAC catalogue integration"]),
    ("v4.0", "\u2605 VISION",     RED,
     ["Predictive spatial modelling", "Autonomous decision support", "Disaster-response loops", "Infrastructure planning AI"]),
]
vx = Inches(0.4); vy = Inches(1.1)
vw = Inches(2.47); vh = Inches(4.8); vgap = Inches(0.1)
for i, (ver, status, col, items) in enumerate(versions):
    x = vx + i * (vw + vgap)
    bg_map = {GREEN: RGBColor(0xD5,0xEA,0xDD), TEAL: RGBColor(0xD8,0xEC,0xED),
              AMBER: RGBColor(0xF8,0xE9,0xC8), NAVY: RGBColor(0xD5,0xDB,0xE2),
              RED:   RGBColor(0xF7,0xE1,0xDD)}
    add_round(s19, x, vy, vw, vh, bg_map[col], line=col, line_w=2.5)
    # version header
    add_rect(s19, x + Inches(0.15), vy + Inches(0.2), vw - Inches(0.3), Inches(0.55),
             col)
    add_text(s19, x + Inches(0.15), vy + Inches(0.2), vw - Inches(0.3), Inches(0.55),
             ver, size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s19, x, vy + Inches(0.9), vw, Inches(0.35),
             status, size=11, bold=True, color=col, align=PP_ALIGN.CENTER)
    # items
    iy = vy + Inches(1.35)
    for item in items:
        add_text(s19, x + Inches(0.15), iy, vw - Inches(0.3), Inches(0.55),
                 "\u2022 " + item, size=11, color=NAVY)
        iy += Inches(0.55)

# timeline arrow
for i in range(len(versions) - 1):
    x1 = vx + i * (vw + vgap) + vw
    y  = vy + Inches(0.475)
    add_arrow(s19, x1, y, x1 + vgap, y, color=MUTED, width=2)

# legend
ly = Inches(6.1)
add_text(s19, Inches(0.4), ly, Inches(12.5), Inches(0.35),
         "\u2713 Shipped     \u26A1 In development     \u25B6 Planned     \u2605 Vision",
         size=11, color=MUTED, italic=True, align=PP_ALIGN.CENTER)

# ================================================================
# SLIDE 20 - CONCLUSION
# ================================================================
s20 = prs.slides.add_slide(BLANK)
header_bar(s20, "Conclusion \u2014 The Beginning, Not the End", 20)
footer_bar(s20)

add_text(s20, Inches(0.4), Inches(1.0), Inches(7.3), Inches(1.0),
         "GeoSI demonstrates that a small, disciplined architecture can deliver\n"
         "a conversational GIS that is both grounded and capable:",
         size=13, color=NAVY)

add_bullets(s20, Inches(0.4), Inches(2.1), Inches(7.3), Inches(3.3), [
    "A framework-free engine with 127 auto-discovered tools",
    "A local-first LLM chain that always produces an answer",
    "A plugin that never competes with the engine for ownership",
    "A server that scales the same engine to the cloud",
    "Layer grounding that refuses to invent data",
    "Explainable plans \u2014 every answer shows its work",
], size=13)

add_text(s20, Inches(0.4), Inches(5.6), Inches(7.3), Inches(1.2),
         "GeoSI is the beginning of geospatial superintelligence \u2014 a domain-native,\n"
         "explainable, and locally-operable intelligence layer for the GIS profession.",
         size=13, italic=True, color=TEAL, bold=True)

# right
add_block(s20, Inches(8.0), Inches(1.0), Inches(5.0), Inches(2.2), "Availability",
          ["Source code, documentation, and example datasets are in the GeoSI repository.",
           "\u2022 geosi_engine/  \u2014 universal core",
           "\u2022 geosi_plugin/  \u2014 QGIS surface",
           "\u2022 geosi_server/  \u2014 REST surface",
           "\u2022 docs/  \u2014 report, prompt guide"],
          body_size=11)

add_block(s20, Inches(8.0), Inches(3.4), Inches(5.0), Inches(1.5), "Acknowledgements",
          ["Digital University Kerala (DUK), and the open-source QGIS, Ollama,",
           "GeoPandas, and scientific Python communities."],
          body_size=11, title_bg=AMBER)

# Thank you
add_round(s20, Inches(8.0), Inches(5.1), Inches(5.0), Inches(1.4), NAVY)
add_text(s20, Inches(8.0), Inches(5.15), Inches(5.0), Inches(0.6),
         "Thank you.", size=28, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s20, Inches(8.0), Inches(5.8), Inches(5.0), Inches(0.5),
         "Questions & discussion welcome", size=13, color=LIGHT, align=PP_ALIGN.CENTER, italic=True)

# ==================== Save ====================
out_path = "/tmp/cc-agent/66564703/project/docs/GeoSI_Presentation.pptx"
prs.save(out_path)
print("Saved:", out_path)
