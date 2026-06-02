"""
Build the final Software Architecture exam-prep walkthrough PDF.

Run from the project root (the one containing the `walkthrough/` directory):

    python walkthrough/build/build_pdf.py

Output:
    walkthrough/Software_Architecture_Walkthrough.pdf

The script parses every chapter markdown under walkthrough/chapters/ (skipping
the 00_outline.md scaffolding doc), assembles a cover, intro, course map,
TOC, all 17 chapters in order, then a glossary, acronym index, bibliography,
and a one-page cheat-sheet.

Dependencies (all already installed): reportlab, Pillow, PyMuPDF, markdown.
"""

from __future__ import annotations

import os
import re
import sys
import time
import html
import json
from collections import OrderedDict
from pathlib import Path

from PIL import Image as PILImage

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, inch, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SCRIPT_PATH = Path(__file__).resolve()
BUILD_DIR = SCRIPT_PATH.parent
WALKTHROUGH_DIR = BUILD_DIR.parent
CHAPTERS_DIR = WALKTHROUGH_DIR / "chapters"
IMAGES_DIR = WALKTHROUGH_DIR / "images"
ANALYSIS_DIR = WALKTHROUGH_DIR / "analysis"
OUT_PDF = WALKTHROUGH_DIR / "Software_Architecture_Walkthrough.pdf"

# Page geometry
PAGE_W, PAGE_H = A4
MARGIN = 1.8 * cm
CONTENT_W = PAGE_W - 2 * MARGIN
CONTENT_H = PAGE_H - 2 * MARGIN

MAX_IMG_W = CONTENT_W
# Cap image height at 13 cm: many slide diagrams are landscape, this keeps
# them out of the "full page each" trap that bloats the page count.
MAX_IMG_H = 13 * cm

# ---------------------------------------------------------------------------
# Stats trackers (populated during build, reported at end)
# ---------------------------------------------------------------------------

stats = {
    "chapters_rendered": 0,
    "images_embedded": 0,
    "images_missing": 0,
    "tables_rendered": 0,
    "code_blocks": 0,
    "issues": [],
}

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

base_styles = getSampleStyleSheet()


def _style(
    name,
    parent=None,
    fontName="Helvetica",
    fontSize=10.5,
    leading=14,
    spaceBefore=0,
    spaceAfter=4,
    textColor=colors.black,
    alignment=TA_LEFT,
    leftIndent=0,
    rightIndent=0,
    firstLineIndent=0,
    backColor=None,
    borderColor=None,
    borderWidth=0,
    borderPadding=0,
    bulletIndent=0,
):
    return ParagraphStyle(
        name=name,
        parent=parent,
        fontName=fontName,
        fontSize=fontSize,
        leading=leading,
        spaceBefore=spaceBefore,
        spaceAfter=spaceAfter,
        textColor=textColor,
        alignment=alignment,
        leftIndent=leftIndent,
        rightIndent=rightIndent,
        firstLineIndent=firstLineIndent,
        backColor=backColor,
        borderColor=borderColor,
        borderWidth=borderWidth,
        borderPadding=borderPadding,
        bulletIndent=bulletIndent,
    )


STYLES = {
    "Body": _style("Body", fontSize=9.5, leading=12.5, spaceAfter=3,
                   alignment=TA_JUSTIFY),
    "BodyNoJust": _style("BodyNoJust", fontSize=9.5, leading=12.5, spaceAfter=3),
    "ChapterTitle": _style("ChapterTitle", fontName="Helvetica-Bold",
                           fontSize=20, leading=24, spaceBefore=2,
                           spaceAfter=10, textColor=colors.HexColor("#1a3a6b")),
    "Heading1": _style("Heading1", fontName="Helvetica-Bold",
                       fontSize=14, leading=17, spaceBefore=10,
                       spaceAfter=5, textColor=colors.HexColor("#1a3a6b")),
    "Heading2": _style("Heading2", fontName="Helvetica-Bold",
                       fontSize=12, leading=15, spaceBefore=7,
                       spaceAfter=3, textColor=colors.HexColor("#2a4a7b")),
    "Heading3": _style("Heading3", fontName="Helvetica-Bold",
                       fontSize=11, leading=14, spaceBefore=5,
                       spaceAfter=2, textColor=colors.HexColor("#3a5a8b")),
    "Heading4": _style("Heading4", fontName="Helvetica-BoldOblique",
                       fontSize=10, leading=13, spaceBefore=4,
                       spaceAfter=2, textColor=colors.HexColor("#444444")),
    "Caption": _style("Caption", fontName="Helvetica-Oblique",
                      fontSize=8.5, leading=11, spaceAfter=5,
                      alignment=TA_CENTER, textColor=colors.HexColor("#555555")),
    "Blockquote": _style(
        "Blockquote",
        fontSize=9.5,
        leading=12.5,
        leftIndent=10,
        rightIndent=10,
        spaceBefore=3,
        spaceAfter=4,
        textColor=colors.HexColor("#333333"),
        borderColor=colors.HexColor("#bbbbbb"),
        borderWidth=0,
        borderPadding=5,
        backColor=colors.HexColor("#f3f3f8"),
    ),
    "Code": _style("Code", fontName="Courier", fontSize=8,
                   leading=10, leftIndent=6, rightIndent=6,
                   spaceBefore=2, spaceAfter=4, backColor=colors.HexColor("#f0f0f0"),
                   borderColor=colors.HexColor("#cccccc"), borderWidth=0.5,
                   borderPadding=3),
    "Bullet": _style("Bullet", fontSize=9.5, leading=12.5,
                     leftIndent=14, bulletIndent=2, spaceAfter=1,
                     alignment=TA_LEFT),
    "Cover": _style("Cover", fontName="Helvetica-Bold",
                    fontSize=30, leading=36, alignment=TA_CENTER,
                    spaceAfter=20, textColor=colors.HexColor("#1a3a6b")),
    "CoverSub": _style("CoverSub", fontName="Helvetica",
                       fontSize=14, leading=20, alignment=TA_CENTER,
                       spaceAfter=8, textColor=colors.HexColor("#555555")),
    "CoverMeta": _style("CoverMeta", fontName="Helvetica",
                        fontSize=11, leading=16, alignment=TA_CENTER,
                        spaceAfter=4, textColor=colors.HexColor("#333333")),
    "TOC1": _style("TOC1", fontName="Helvetica-Bold", fontSize=10.5,
                   leading=13, spaceBefore=3, spaceAfter=0,
                   textColor=colors.HexColor("#1a3a6b")),
    "TOC2": _style("TOC2", fontName="Helvetica", fontSize=8.5,
                   leading=10.5, leftIndent=14, spaceAfter=0,
                   textColor=colors.HexColor("#444444")),
}

# ---------------------------------------------------------------------------
# Page template with header + footer
# ---------------------------------------------------------------------------

current_chapter_title = {"text": ""}


class ChapterMarker(Flowable):
    """A zero-height flowable that updates the running chapter title.

    When this flowable is drawn (i.e. flows into the document), it sets
    the title for headers on the *following* pages. We attach it just
    before each new chapter title.
    """

    def __init__(self, title):
        super().__init__()
        self.title = title
        self.width = 0
        self.height = 0

    def wrap(self, availWidth, availHeight):
        return (0, 0)

    def draw(self):
        # When this flowable renders, update the running header title.
        current_chapter_title["text"] = self.title


def _draw_header_footer(canv: canvas.Canvas, doc):
    canv.saveState()
    # Footer page number
    page_num = canv.getPageNumber()
    canv.setFont("Helvetica", 8.5)
    canv.setFillColor(colors.HexColor("#666666"))
    canv.drawCentredString(PAGE_W / 2, 1.0 * cm, f"Page {page_num}")
    # Header (chapter title)
    title = current_chapter_title["text"]
    if title:
        canv.setFont("Helvetica-Oblique", 8.5)
        canv.setFillColor(colors.HexColor("#888888"))
        canv.drawString(MARGIN, PAGE_H - 1.0 * cm, title)
        canv.setStrokeColor(colors.HexColor("#cccccc"))
        canv.setLineWidth(0.4)
        canv.line(MARGIN, PAGE_H - 1.15 * cm,
                  PAGE_W - MARGIN, PAGE_H - 1.15 * cm)
    canv.restoreState()


def _draw_cover_blank(canv: canvas.Canvas, doc):
    """Cover page: no header, no footer."""
    pass


# ---------------------------------------------------------------------------
# TOC support
# ---------------------------------------------------------------------------


class TOCDocTemplate(BaseDocTemplate):
    """Doc template that exposes afterFlowable for TOC entries."""

    def afterFlowable(self, flowable):
        if not isinstance(flowable, Paragraph):
            return
        style_name = flowable.style.name
        text = flowable.getPlainText()
        if style_name == "ChapterTitle":
            self.notify("TOCEntry", (0, text, self.page))
        elif style_name == "Heading1":
            self.notify("TOCEntry", (1, text, self.page))
        elif style_name == "Heading2":
            self.notify("TOCEntry", (2, text, self.page))


# ---------------------------------------------------------------------------
# Markdown -> flowables
# ---------------------------------------------------------------------------


_INLINE_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_INLINE_IMG_RE = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$")
_INLINE_CODE_RE = re.compile(r"`([^`]+)`")
_INLINE_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
_INLINE_ITALIC_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
_HRULE_RE = re.compile(r"^\s*---+\s*$")
_BULLET_RE = re.compile(r"^(\s*)([-*])\s+(.*)$")
_NUMBERED_RE = re.compile(r"^(\s*)(\d+)\.\s+(.*)$")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-+:?(\s*\|\s*:?-+:?)+\s*\|?\s*$")


def render_inline(text: str) -> str:
    """Convert inline markdown to reportlab-Paragraph-friendly markup.

    Output uses <b>, <i>, <font name="Courier">, and HTML-escaped characters.
    """
    if not text:
        return ""
    # First, protect inline code by extracting it.
    code_segments = []

    def _grab_code(m):
        idx = len(code_segments)
        code_segments.append(m.group(1))
        return f"\x00CODE{idx}\x00"

    work = _INLINE_CODE_RE.sub(_grab_code, text)

    # Protect images and links from being mangled (we strip them inline).
    def _grab_link(m):
        label, _url = m.group(1), m.group(2)
        return label  # render as plain text (no real hyperlink)

    work = _INLINE_LINK_RE.sub(_grab_link, work)

    # Bold then italic. Use sentinel tokens so we can HTML-escape later.
    work = _INLINE_BOLD_RE.sub(
        lambda m: "\x01B\x02" + m.group(1) + "\x01/B\x02", work)
    work = _INLINE_ITALIC_RE.sub(
        lambda m: "\x01I\x02" + m.group(1) + "\x01/I\x02", work)

    # HTML-escape what remains.
    work = html.escape(work, quote=False)

    # Restore protected tokens as XML tags.
    work = work.replace("\x01B\x02", "<b>").replace("\x01/B\x02", "</b>")
    work = work.replace("\x01I\x02", "<i>").replace("\x01/I\x02", "</i>")

    # Restore inline code.
    def _restore_code(m):
        idx = int(m.group(1))
        c = html.escape(code_segments[idx], quote=False)
        return f'<font name="Courier" size="9" backColor="#eeeeee">{c}</font>'

    work = re.sub(r"\x00CODE(\d+)\x00", _restore_code, work)
    return work


def _img_dimensions(path: Path):
    """Return (width, height) clamped to MAX_IMG_W/H, preserving aspect."""
    with PILImage.open(path) as im:
        iw, ih = im.size
    # Convert pixels to points: assume 96 DPI for screenshots
    px_to_pt = 72.0 / 96.0
    w_pt = iw * px_to_pt
    h_pt = ih * px_to_pt
    # Scale to fit width
    if w_pt > MAX_IMG_W:
        ratio = MAX_IMG_W / w_pt
        w_pt *= ratio
        h_pt *= ratio
    # Scale to fit height
    if h_pt > MAX_IMG_H:
        ratio = MAX_IMG_H / h_pt
        w_pt *= ratio
        h_pt *= ratio
    return w_pt, h_pt


def _build_image_flowable(alt: str, img_path: str, base_dir: Path):
    """Return a list of flowables for an image (image + caption)."""
    # Resolve relative path; chapters reference ../images/...
    resolved = (base_dir / img_path).resolve()
    if not resolved.exists():
        stats["images_missing"] += 1
        stats["issues"].append(f"MISSING IMAGE: {img_path}")
        return [Paragraph(
            f"<b>[MISSING IMAGE]</b> <font color='#aa0000'>{html.escape(img_path)}</font>",
            STYLES["Body"])]
    try:
        w, h = _img_dimensions(resolved)
        img = Image(str(resolved), width=w, height=h)
        flowables = [img]
        if alt:
            flowables.append(Spacer(1, 2))
            flowables.append(Paragraph(html.escape(alt), STYLES["Caption"]))
        stats["images_embedded"] += 1
        return [KeepTogether(flowables)]
    except Exception as exc:
        stats["images_missing"] += 1
        stats["issues"].append(f"IMAGE ERROR {img_path}: {exc}")
        return [Paragraph(
            f"<b>[IMAGE ERROR]</b> {html.escape(img_path)}: {html.escape(str(exc))}",
            STYLES["Body"])]


def _parse_table(rows):
    """Build a reportlab Table from a list of '|...|' lines."""
    cells = []
    for line in rows:
        parts = [c.strip() for c in line.strip().strip("|").split("|")]
        cells.append(parts)
    if not cells:
        return None
    # Normalise column count
    ncols = max(len(r) for r in cells)
    for r in cells:
        while len(r) < ncols:
            r.append("")
    # Render each cell as Paragraph for wrapping
    # Pick font size based on column count
    if ncols >= 9:
        fs = 6.5
        lead = 8.5
    elif ncols >= 7:
        fs = 7.5
        lead = 10
    elif ncols >= 5:
        fs = 8.5
        lead = 11
    else:
        fs = 9.5
        lead = 12
    cell_style = ParagraphStyle("cell", parent=STYLES["Body"],
                                fontSize=fs, leading=lead, alignment=TA_LEFT,
                                spaceAfter=0, spaceBefore=0)
    header_style = ParagraphStyle("cellh", parent=cell_style,
                                  fontName="Helvetica-Bold",
                                  textColor=colors.white)
    rendered = []
    for ri, row in enumerate(cells):
        out = []
        for c in row:
            txt = render_inline(c)
            out.append(Paragraph(txt or "&nbsp;",
                                 header_style if ri == 0 else cell_style))
        rendered.append(out)
    col_w = CONTENT_W / ncols
    tbl = Table(rendered, colWidths=[col_w] * ncols, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3a6b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f5f5fa")]),
    ]))
    stats["tables_rendered"] += 1
    return tbl


def _flush_list(buf, ordered):
    if not buf:
        return None
    items = []
    for item_text in buf:
        items.append(ListItem(
            Paragraph(render_inline(item_text), STYLES["Body"]),
            leftIndent=10, value=None,
        ))
    if ordered:
        lf = ListFlowable(items, bulletType="1",
                          leftIndent=18, bulletFontSize=10,
                          bulletColor=colors.HexColor("#1a3a6b"))
    else:
        lf = ListFlowable(items, bulletType="bullet",
                          start="•", leftIndent=18,
                          bulletFontSize=10,
                          bulletColor=colors.HexColor("#1a3a6b"))
    return lf


def parse_markdown_to_flowables(md_text: str, base_dir: Path,
                                first_heading_as_chapter=True):
    """Convert markdown text into a list of reportlab flowables.

    `first_heading_as_chapter=True` means the first `# Heading` becomes a
    ChapterTitle. Subsequent `#` headings (rare in chapters) are demoted.
    """
    lines = md_text.split("\n")
    flowables = []
    i = 0

    # State
    in_code = False
    code_lang = ""
    code_buf = []

    list_buf = []  # for collecting bullet items
    list_ordered = False

    table_buf = []  # collecting consecutive table lines
    in_table = False

    para_buf = []

    blockquote_buf = []

    seen_chapter_title = False

    def flush_para():
        nonlocal para_buf
        if para_buf:
            txt = " ".join(s.strip() for s in para_buf if s.strip())
            if txt:
                flowables.append(Paragraph(render_inline(txt), STYLES["Body"]))
            para_buf = []

    def flush_list():
        nonlocal list_buf, list_ordered
        lf = _flush_list(list_buf, list_ordered)
        if lf is not None:
            flowables.append(lf)
            flowables.append(Spacer(1, 2))
        list_buf = []

    def flush_table():
        nonlocal table_buf, in_table
        if table_buf:
            tbl = _parse_table(table_buf)
            if tbl:
                flowables.append(Spacer(1, 2))
                flowables.append(tbl)
                flowables.append(Spacer(1, 2))
        table_buf = []
        in_table = False

    def flush_blockquote():
        nonlocal blockquote_buf
        if blockquote_buf:
            txt = " ".join(s.strip() for s in blockquote_buf if s.strip())
            if txt:
                flowables.append(Paragraph(render_inline(txt),
                                           STYLES["Blockquote"]))
            blockquote_buf = []

    while i < len(lines):
        line = lines[i]
        rstripped = line.rstrip()

        # Code block fences
        if rstripped.startswith("```"):
            if not in_code:
                flush_para()
                flush_list()
                flush_table()
                flush_blockquote()
                in_code = True
                code_lang = rstripped[3:].strip()
                code_buf = []
            else:
                # close
                code_text = "\n".join(code_buf)
                # escape and render
                pf = Preformatted(code_text, STYLES["Code"])
                flowables.append(pf)
                flowables.append(Spacer(1, 2))
                stats["code_blocks"] += 1
                in_code = False
                code_buf = []
                code_lang = ""
            i += 1
            continue

        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # Image (must be on its own line)
        m_img = _INLINE_IMG_RE.match(rstripped)
        if m_img:
            flush_para()
            flush_list()
            flush_table()
            flush_blockquote()
            alt, path = m_img.group(1), m_img.group(2)
            flowables.extend(_build_image_flowable(alt, path, base_dir))
            flowables.append(Spacer(1, 2))
            i += 1
            continue

        # Horizontal rule
        if _HRULE_RE.match(rstripped):
            flush_para()
            flush_list()
            flush_table()
            flush_blockquote()
            # Use a spacer + thin rule via small table
            sep = Table([[" "]], colWidths=[CONTENT_W], rowHeights=[1])
            sep.setStyle(TableStyle([
                ("LINEABOVE", (0, 0), (-1, 0), 0.5,
                 colors.HexColor("#bbbbbb")),
            ]))
            flowables.append(Spacer(1, 3))
            flowables.append(sep)
            flowables.append(Spacer(1, 6))
            i += 1
            continue

        # Headings
        m_h = _HEADING_RE.match(rstripped)
        if m_h:
            flush_para()
            flush_list()
            flush_table()
            flush_blockquote()
            hashes, text = m_h.group(1), m_h.group(2).strip()
            level = len(hashes)
            if level == 1:
                if first_heading_as_chapter and not seen_chapter_title:
                    seen_chapter_title = True
                    # Page break before chapter title (handled by caller via PageBreak before)
                    flowables.append(Paragraph(render_inline(text),
                                               STYLES["ChapterTitle"]))
                else:
                    flowables.append(Paragraph(render_inline(text),
                                               STYLES["Heading1"]))
            elif level == 2:
                flowables.append(Paragraph(render_inline(text),
                                           STYLES["Heading1"]))
            elif level == 3:
                flowables.append(Paragraph(render_inline(text),
                                           STYLES["Heading2"]))
            elif level == 4:
                flowables.append(Paragraph(render_inline(text),
                                           STYLES["Heading3"]))
            else:
                flowables.append(Paragraph(render_inline(text),
                                           STYLES["Heading4"]))
            i += 1
            continue

        # Table
        if "|" in rstripped and rstripped.strip().startswith("|"):
            # Check if next line is a separator -> table
            if not in_table:
                if i + 1 < len(lines) and _TABLE_SEP_RE.match(lines[i + 1]):
                    flush_para()
                    flush_list()
                    flush_blockquote()
                    in_table = True
                    table_buf = [rstripped]
                    i += 2  # skip separator
                    continue
            else:
                table_buf.append(rstripped)
                i += 1
                continue

        # If we were in a table and this line is not a table line, flush
        if in_table:
            flush_table()

        # Blockquote
        if rstripped.startswith(">"):
            flush_para()
            flush_list()
            blockquote_buf.append(rstripped.lstrip(">").lstrip())
            i += 1
            continue
        else:
            flush_blockquote()

        # Bullet
        m_b = _BULLET_RE.match(line)
        if m_b:
            if list_ordered:
                flush_list()
            flush_para()
            list_ordered = False
            list_buf.append(m_b.group(3))
            i += 1
            continue

        # Numbered
        m_n = _NUMBERED_RE.match(line)
        if m_n:
            if not list_ordered:
                flush_list()
            flush_para()
            list_ordered = True
            list_buf.append(m_n.group(3))
            i += 1
            continue

        # Blank line
        if not rstripped.strip():
            flush_para()
            flush_list()
            flush_blockquote()
            i += 1
            continue

        # Plain text -> accumulate
        flush_list()
        # If line is an italic caption immediately after an image (starts with *...*)
        # treat as a small caption-ish paragraph? Easiest: just normal paragraph.
        para_buf.append(rstripped)
        i += 1

    # End
    flush_para()
    flush_list()
    flush_table()
    flush_blockquote()
    if in_code:
        # unterminated
        code_text = "\n".join(code_buf)
        flowables.append(Preformatted(code_text, STYLES["Code"]))

    return flowables


# ---------------------------------------------------------------------------
# Front matter
# ---------------------------------------------------------------------------


def build_cover():
    fl = []
    fl.append(Spacer(1, 5 * cm))
    fl.append(Paragraph("Software Architecture", STYLES["Cover"]))
    fl.append(Paragraph("Exam Walkthrough", STYLES["Cover"]))
    fl.append(Spacer(1, 1.0 * cm))
    fl.append(Paragraph("A topic-organised deep study guide",
                        STYLES["CoverSub"]))
    fl.append(Spacer(1, 2.4 * cm))
    fl.append(Paragraph("Course <b>T630019402</b>", STYLES["CoverMeta"]))
    fl.append(Paragraph("University of Southern Denmark (SDU)",
                        STYLES["CoverMeta"]))
    fl.append(Paragraph("Lecturer: Jukka Ruohonen", STYLES["CoverMeta"]))
    fl.append(Paragraph("Spring 2026", STYLES["CoverMeta"]))
    fl.append(Spacer(1, 1.2 * cm))
    fl.append(Paragraph(
        "Prepared from 10 lectures and 2 case studies",
        STYLES["CoverMeta"]))
    fl.append(Paragraph("Compiled 2026-05-26", STYLES["CoverMeta"]))
    return fl  # caller adds the trailing PageBreak


def build_intro():
    fl = []
    fl.append(Paragraph("How to use this guide", STYLES["ChapterTitle"]))
    fl.append(Paragraph(
        "This walkthrough was built directly from the lecturer's slides "
        "(Lectures 1-10 plus the two assigned case studies) and the analysis "
        "notes the writers produced for each lecture. It is organised "
        "<i>by topic</i>, not by lecture &mdash; each quality attribute has "
        "its own chapter, and the cross-cutting material lives in dedicated "
        "reference chapters at the end.",
        STYLES["Body"]))
    fl.append(Paragraph("Structure at a glance", STYLES["Heading2"]))
    fl.append(Paragraph(
        "Chapters 1 and 2 lay the foundation: the vocabulary, views, the "
        "SOLID-at-component-scope rules, and the quality-attribute (QA) "
        "framework with its six-slot scenario template and ISO/IEC 25010 "
        "taxonomy. Chapters 3 through 12 walk each individual QA in turn, "
        "using the same definition &rarr; 6-slot scenario &rarr; tactics tree "
        "&rarr; patterns rhythm. Chapter 13 is a cross-QA reference; "
        "Chapter 14 covers architecture evaluation. Chapters 15 and 16 are "
        "the two case-study walkthroughs (Linux network stack; MLOps "
        "reference architecture). Chapter 17 is exam-tactical preparation.",
        STYLES["Body"]))
    fl.append(Paragraph("Exam intel", STYLES["Heading2"]))
    fl.append(Paragraph(
        "From Lecture 10 page 2 (the lecturer's own briefing): "
        "<b>16 questions, 34 points total, passing at 17 points</b> "
        "(approximately 50%). Per-question worth ranges from 1 to 5 points. "
        "Smartphones are permitted, but only for digitising hand-drawn "
        "diagrams (photograph the paper, upload the image). The re-exam "
        "uses the same format.",
        STYLES["Body"]))
    fl.append(Paragraph(
        "Two warnings appear repeatedly in the slides. First: "
        "<b>anything that appeared in the lectures may appear in the exam</b>, "
        "including the lecturer's own publications and side remarks. "
        "Second: <b>slides alone are not sufficient</b> &mdash; you must be "
        "able to <i>apply</i> the material to fresh scenarios you have never "
        "seen. The lecturer states this explicitly twice in the briefing.",
        STYLES["Body"]))
    fl.append(Paragraph("Soft-skill emphasis", STYLES["Heading2"]))
    fl.append(Paragraph(
        "Lecture 1 boldfaces the claim that the <b>top three job qualities "
        "of a software architect are communication-related</b>: "
        "articulation and transferability of knowledge, stakeholder "
        "management, and communication / presentation / negotiation. This "
        "is exam-counted. At least one written-discussion question on the "
        "non-technical side of the architect's role is expected.",
        STYLES["Body"]))
    fl.append(Paragraph("How to read this guide", STYLES["Heading2"]))
    fl.append(Paragraph(
        "On a first pass, read Chapters 1, 2, and 17 to get the framework, "
        "the QA machinery, and the exam map. Then read the QA chapters in "
        "any order you like &mdash; they were written to stand alone but "
        "with explicit cross-references. Use Chapter 13 (Pattern + Tactic "
        "Reference) during revision: it is a flippable index, not a "
        "linear read. The case-study chapters (15, 16) are best read "
        "after the QA chapters they exemplify (Ch 15 after Ch 7, 8, 9; "
        "Ch 16 after Ch 6 and 9). The final cheat-sheet in the back "
        "matter is the 48-hours-before-exam document.",
        STYLES["Body"]))
    return fl


def build_course_map():
    fl = []
    fl.append(Paragraph("Course map", STYLES["ChapterTitle"]))
    fl.append(Paragraph(
        "Software Architecture as taught here builds on "
        "<b>Bass, Clements and Kazman (2021)</b> &mdash; <i>Software "
        "Architecture in Practice</i> &mdash; and <b>Fairbanks (2010)</b> "
        "&mdash; <i>Just Enough Software Architecture</i> &mdash; "
        "supplemented with Ruohonen's own publications (NetBSD test "
        "evolution, Linux kernel regression patterns, EU CRA mapping, "
        "secure defaults, agentic AI). Ten lectures progress from "
        "<b>foundations</b> (Lecture 1: vocabulary, views, SOLID at "
        "component scope, layering) through the <b>Quality-Attribute "
        "framework</b> (Lecture 2: ASRs, scenarios, ISO/IEC 25010, risk, "
        "SBOM), and then march through individual QAs lecture by "
        "lecture using a consistent rhythm: definition &rarr; six-slot "
        "scenario &rarr; tactics tree &rarr; patterns.",
        STYLES["Body"]))
    fl.append(Paragraph(
        "The lecture sequence is: Integrability + Modifiability (L3), "
        "Testability + Deployability (L4), Availability (L5), "
        "Performance (L6), Scalability (L7), Safety + Security part 1 "
        "(L8), Security part 2 (L9), Usability + Power Consumption + "
        "Architecture Evaluation (L10). Two case studies anchor "
        "everything: <b>Case 1</b> &mdash; the <i>Linux network stack</i> "
        "(Horvat poster) as a &ldquo;find every pattern and tactic in one "
        "real system&rdquo; exercise; and <b>Case 3</b> &mdash; the "
        "<i>MLOps reference architecture</i> (Kreuzberger et al.) as a "
        "&ldquo;design an end-to-end reference architecture&rdquo; "
        "exercise.",
        STYLES["Body"]))
    fl.append(Paragraph(
        "The exam style favours <b>scenario-based answers</b>, "
        "<b>drawn diagrams</b> (often photographed via smartphone), and "
        "concise <b>prioritised discussion of trade-offs</b>. Articulating "
        "the QA you are trading away matters as much as articulating the "
        "one you are buying.",
        STYLES["Body"]))
    return fl


def build_toc(toc_flowable):
    fl = []
    fl.append(Paragraph("Table of contents", STYLES["ChapterTitle"]))
    fl.append(Spacer(1, 0.4 * cm))
    toc_flowable.levelStyles = [
        STYLES["TOC1"],
        STYLES["TOC2"],
    ]
    fl.append(toc_flowable)
    return fl


# ---------------------------------------------------------------------------
# Back matter generation
# ---------------------------------------------------------------------------


_GLOSSARY_HEADING_RE = re.compile(r"^###\s+(?:\d+\.\s+)?(.+?)\s*$")


def gather_glossary():
    """Scan chapters for `### ` headings; treat each as a glossary term.

    Term = heading text (stripped of leading numbers like '5.').
    Definition = the first paragraph after the heading (skip Definition: marker).
    """
    entries = {}  # term -> (chapter_label, definition)
    for md_path in sorted(CHAPTERS_DIR.glob("[0-1][0-9]_*.md")):
        chap_num = md_path.stem.split("_")[0]
        try:
            chap_label = f"Ch {int(chap_num)}"
        except ValueError:
            chap_label = ""
        lines = md_path.read_text(encoding="utf-8").split("\n")
        i = 0
        while i < len(lines):
            line = lines[i]
            m = re.match(r"^###\s+(.+?)\s*$", line)
            if m:
                term = m.group(1).strip()
                # Strip "N." prefix
                term = re.sub(r"^\d+(?:\.\d+)*\.\s+", "", term)
                # Skip non-term style headings (very long ones)
                if len(term) > 90:
                    i += 1
                    continue
                # Skip obvious section headers (those with no real concept)
                if term.lower().startswith(("opening", "appendix",
                                            "summary cards", "what to memorise",
                                            "what to memorize", "checklist",
                                            "exam logistics", "the soft-skills",
                                            "question archetype")):
                    i += 1
                    continue
                # Collect definition
                # Look for "**Definition.**" or first non-empty paragraph
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                def_text = ""
                if j < len(lines):
                    block = []
                    while j < len(lines) and lines[j].strip() and \
                            not lines[j].startswith("#") and \
                            not lines[j].startswith("![") and \
                            not lines[j].startswith("|") and \
                            not lines[j].startswith("```"):
                        block.append(lines[j].strip())
                        j += 1
                    def_text = " ".join(block).strip()
                # Clean: strip leading "**Definition.**"
                def_text = re.sub(r"^\*\*Definition\.\*\*\s*", "", def_text)
                def_text = re.sub(r"^\*\*[^*]+\*\*\s*", "", def_text,
                                  count=0)  # only leading bold
                # Truncate to first 2 sentences
                sentences = re.split(r"(?<=[.!?])\s+", def_text)
                if sentences:
                    def_text = " ".join(sentences[:2]).strip()
                if len(def_text) > 350:
                    def_text = def_text[:347] + "..."
                if def_text and term not in entries:
                    entries[term] = (chap_label, def_text)
            i += 1
    return entries


def build_glossary():
    fl = []
    fl.append(Paragraph("Glossary", STYLES["ChapterTitle"]))
    fl.append(Paragraph(
        "Alphabetical reference for the key concepts introduced "
        "throughout the book. The chapter tag points to the canonical home "
        "where the concept is developed in depth.",
        STYLES["Body"]))
    fl.append(Spacer(1, 0.3 * cm))
    entries = gather_glossary()
    # Sort case-insensitively
    keys = sorted(entries.keys(), key=lambda s: s.lower())
    # Group by first letter
    current_letter = None
    for term in keys:
        chap, definition = entries[term]
        first = term[0].upper()
        if first != current_letter:
            current_letter = first
            fl.append(Spacer(1, 0.2 * cm))
            fl.append(Paragraph(first, STYLES["Heading2"]))
        line = (f"<b>{html.escape(term)}</b> "
                f"<font color='#888888'>[{chap}]</font> &mdash; "
                f"{render_inline(definition)}")
        fl.append(Paragraph(line, STYLES["Body"]))
    return fl


ACRONYMS = OrderedDict([
    ("ASR", "Architecturally Significant Requirement &mdash; a requirement "
            "whose satisfaction is materially affected by architecture."),
    ("ATAM", "Architecture Tradeoff Analysis Method &mdash; SEI scenario-"
             "based architecture evaluation method."),
    ("CAP", "Consistency, Availability, Partition tolerance &mdash; "
            "Brewer's theorem; under a network partition you can only have "
            "two of the three."),
    ("PACELC", "Partition-CAP-Else-Consistency-Latency &mdash; Abadi's "
               "extension: even without partition you still trade "
               "consistency against latency."),
    ("CDN", "Content Delivery Network &mdash; tiered edge cache topology "
            "for static assets, with DDoS / DNS / WAF bundled in."),
    ("CIA", "Confidentiality, Integrity, Availability &mdash; the "
            "foundational security triad; sometimes extended to CIAA "
            "with Authenticity."),
    ("CRA", "Cyber Resilience Act &mdash; EU regulation mandating "
            "secure-by-default products and automatic, separated security "
            "updates by 2027."),
    ("CRC", "Cyclic Redundancy Check &mdash; integrity checksum used for "
            "sanity-checking, not for security."),
    ("CSP", "Content Security Policy &mdash; HTTP-header policy that "
            "restricts which sources scripts and assets can be loaded "
            "from."),
    ("CVE", "Common Vulnerabilities and Exposures &mdash; the public "
            "registry of disclosed vulnerabilities."),
    ("DHCP", "Dynamic Host Configuration Protocol &mdash; the canonical "
             "service-discovery / address-assignment example."),
    ("DNS", "Domain Name System &mdash; the canonical name-to-address "
            "service discovery; A and MX records are exam-relevant."),
    ("EDF", "Earliest Deadline First &mdash; deadline-driven scheduling "
            "algorithm."),
    ("GDPR", "General Data Protection Regulation &mdash; EU personal-data "
             "regulation that shapes data-classification decisions."),
    ("HTTP", "Hypertext Transfer Protocol &mdash; the dominant web "
             "protocol; OWASP guidance applies."),
    ("IDS", "Intrusion Detection System &mdash; passive monitoring; "
            "compare IPS (preventive)."),
    ("IPC", "Inter-Process Communication &mdash; mechanisms (pipes, "
            "sockets, shared memory) used by container-to-container "
            "communication inside a pod."),
    ("IP", "Internet Protocol &mdash; the L3 network protocol used by "
           "pod-to-pod communication in Kubernetes."),
    ("ISO/IEC 25010", "International quality-attribute taxonomy with 8 "
                      "top-level categories (functional suitability, "
                      "performance efficiency, compatibility, usability, "
                      "reliability, security, maintainability, "
                      "portability)."),
    ("K8s", "Kubernetes &mdash; the de facto container-orchestration "
            "platform; cluster &rarr; node &rarr; pod &rarr; container."),
    ("LACP", "Link Aggregation Control Protocol &mdash; bonds multiple "
             "NICs into one logical link for capacity and redundancy."),
    ("LLM", "Large Language Model &mdash; new attack surface and "
            "verification-debt vector; see OWASP LLM Top-10."),
    ("MitM", "Man-in-the-Middle attack &mdash; Conti and Dragoni's 2016 "
             "taxonomy lists 7 countermeasures; encryption alone is "
             "ineffective without authentication and secure key "
             "exchange."),
    ("MLOps", "Machine Learning Operations &mdash; reference architecture "
              "of Kreuzberger et al., the Case 3 subject."),
    ("MTBF", "Mean Time Between Failures &mdash; availability metric."),
    ("MTTF", "Mean Time To Failure &mdash; availability metric."),
    ("MTTR", "Mean Time To Repair &mdash; the lower this is, the higher "
             "availability."),
    ("MX", "DNS Mail Exchange record &mdash; the lecturer's running DNS "
           "load-balancing example."),
    ("NAPI", "New API &mdash; Linux kernel network polling extension that "
             "blends interrupts with polling under high load."),
    ("NIST", "(US) National Institute of Standards and Technology &mdash; "
             "publishes the canonical security frameworks."),
    ("OWASP", "Open Web Application Security Project &mdash; publishes "
              "the Top-10 lists for Web, LLM, and CI/CD."),
    ("OVS", "Open vSwitch &mdash; the SDN dataplane in OpenStack."),
    ("RFC", "Request For Comments &mdash; IETF document series; RFC 1958 "
            "(architectural principles incl. Postel's law) is "
            "exam-relevant."),
    ("SBOM", "Software Bill of Materials &mdash; structured inventory of "
             "components and dependencies; CycloneDX is the reference "
             "schema; mandated by the EU CRA from 2027."),
    ("SDL", "(Microsoft) Security Development Lifecycle &mdash; 5 stages "
            "(Design / Implementation / Build / Deploy / Run) with 3 "
            "gates, on a zero-trust baseline."),
    ("SDN", "Software-Defined Networking &mdash; programmable network "
            "control plane; OpenStack Neutron is the lecturer's example."),
    ("SIEM", "Security Information and Event Management &mdash; the "
             "broker + pipe-and-filter system in a SOC."),
    ("SOC", "Security Operations Centre &mdash; the team that runs SIEM "
            "and handles incidents."),
    ("SOLID", "Single-responsibility, Open-closed, Liskov-substitution, "
              "Interface-segregation, Dependency-inversion &mdash; "
              "object-oriented principles lifted to component scope by "
              "Lano and Tehrani."),
    ("SRI", "Subresource Integrity &mdash; HTML attribute "
            "(<i>integrity=\"sha384-...\"</i>) that pins an external "
            "script to a known hash."),
    ("SSRF", "Server-Side Request Forgery &mdash; classic example of "
             "the confused-deputy anti-pattern."),
    ("STAR", "Situation, Task, Action, Result &mdash; soft-skill answer "
             "structure recommended for exam discussion questions."),
    ("TAM", "Technology Acceptance Model &mdash; Davis 1989; perceived "
            "usefulness + perceived ease of use &rarr; attitude &rarr; "
            "intention &rarr; use."),
    ("TCP", "Transmission Control Protocol &mdash; reliable byte-stream "
            "transport used by pod-to-pod communication and most "
            "application protocols."),
    ("TMR", "Triple Modular Redundancy &mdash; majority-gate voting "
            "across three independent replicas."),
    ("UML", "Unified Modeling Language &mdash; the diagrammatic notation "
            "used in the slides for components and deployments."),
    ("WAF", "Web Application Firewall &mdash; HTTP-layer reverse-proxy "
            "filter; bundled into CDN tiers."),
    ("XDP", "eXpress Data Path &mdash; Linux NIC-driver-level packet "
            "filter (Netfilter at the earliest hook); used for DDoS "
            "mitigation."),
])


def build_acronym_index():
    fl = []
    fl.append(Paragraph("Acronym index", STYLES["ChapterTitle"]))
    fl.append(Paragraph(
        "Acronyms used recurrently throughout the lectures, with a "
        "short gloss. Where an acronym has a dedicated discussion in a "
        "chapter, the body of that chapter should be consulted for the "
        "full treatment.",
        STYLES["Body"]))
    fl.append(Spacer(1, 0.3 * cm))
    rows = [["Acronym", "Expansion / meaning"]]
    for acro, gloss in ACRONYMS.items():
        rows.append([acro, gloss])
    cell = ParagraphStyle("acro_cell", parent=STYLES["Body"],
                          fontSize=9, leading=12, alignment=TA_LEFT,
                          spaceAfter=0, spaceBefore=0)
    header = ParagraphStyle("acro_h", parent=cell,
                            fontName="Helvetica-Bold",
                            textColor=colors.white)
    rendered = []
    for ri, row in enumerate(rows):
        if ri == 0:
            rendered.append([Paragraph(c, header) for c in row])
        else:
            acro, defn = row
            rendered.append([
                Paragraph(f"<b>{html.escape(acro)}</b>", cell),
                Paragraph(defn, cell),  # already contains HTML entities
            ])
    tbl = Table(rendered, colWidths=[3.0 * cm, CONTENT_W - 3.0 * cm],
                repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3a6b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f5f5fa")]),
    ]))
    fl.append(tbl)
    return fl


def gather_bibliography():
    """Scan analysis files (and the chapters) for citations like
    (Author Year) or (Author et al. Year)."""
    cites = set()
    cite_re = re.compile(
        r"\(([A-Z][A-Za-z\-]+(?:\s+(?:&|and|et al\.?))?(?:\s+[A-Z][A-Za-z\-]+)?)"
        r"(?:\s+et al\.)?,?\s*(\d{4}[a-z]?)\)")
    files = []
    if ANALYSIS_DIR.exists():
        files.extend(sorted(ANALYSIS_DIR.glob("*.md")))
    files.extend(sorted(CHAPTERS_DIR.glob("[0-1][0-9]_*.md")))
    for p in files:
        text = p.read_text(encoding="utf-8")
        for m in cite_re.finditer(text):
            name = m.group(1).strip()
            year = m.group(2)
            # Skip obvious false positives
            if name.lower() in ("see", "fig", "figure", "p", "pp", "ch", "chapter"):
                continue
            if " " in name and " et al" in name.lower():
                pass
            # Normalize "et al."
            cites.add((name, year))
    return sorted(cites, key=lambda x: (x[0].lower(), x[1]))


# Curated bibliography of the works the lecturer explicitly cites
CURATED_BIBLIOGRAPHY = [
    ("Abadi, D. J. (2010). Consistency tradeoffs in modern distributed "
     "database system design. <i>IEEE Computer</i>. <b>[PACELC theorem.]</b>"),
    ("Adkins, H. et al. (2020). <i>Building Secure and Reliable Systems</i>. "
     "O'Reilly / Google SRE. <b>[Least privilege; blast radius; sharding.]</b>"),
    ("Arce, I., Clark-Fisher, K., Daswani, N. et al. (2014). Avoiding the "
     "Top 10 Software Security Design Flaws. IEEE Computer Society Center "
     "for Secure Design."),
    ("Bansal, C. et al. (2020). Decaf: Diagnosing and triaging performance "
     "issues in large-scale cloud services. <i>ICSE</i>."),
    ("Bass, L., Clements, P. &amp; Kazman, R. (2021). <i>Software "
     "Architecture in Practice</i> (4th ed.). Addison-Wesley. "
     "<b>[Primary textbook.]</b>"),
    ("Boehm, B. W. (1984). Verifying and validating software requirements "
     "and design specifications. <i>IEEE Software</i>, 1(1), 75-88."),
    ("Bondi, A. B. (2000). Characteristics of scalability and their "
     "impact on performance. <i>WOSP</i>."),
    ("Bouzoukas, A. (2026). LLMs and software verification debt "
     "[forthcoming]. Cited in Lecture 4."),
    ("Brewer, E. A. (2000). Towards robust distributed systems. "
     "<i>PODC keynote</i>. <b>[CAP theorem.]</b>"),
    ("Brooker, M. (2019). Exponential backoff and jitter. AWS "
     "Architecture Blog."),
    ("Chou, P. et al. (2025). The vibe coder vignette. Cited in Lecture 4."),
    ("Cleland-Huang, J., Hanmer, R., Supakkul, S. &amp; Mirakhorli, M. "
     "(2013). The Twin Peaks of requirements and architecture. <i>IEEE "
     "Software</i>, 30(2)."),
    ("Conti, M., Dragoni, N. &amp; Lesyk, V. (2016). A survey of "
     "Man-in-the-Middle attacks. <i>IEEE Communications Surveys &amp; "
     "Tutorials</i>."),
    ("Davis, F. D. (1989). Perceived usefulness, perceived ease of use, "
     "and user acceptance of information technology. <i>MIS Quarterly</i>, "
     "13(3). <b>[TAM model.]</b>"),
    ("Dean, J. &amp; Ghemawat, S. (2008). MapReduce: simplified data "
     "processing on large clusters. <i>CACM</i>, 51(1), 107-113."),
    ("Deutsch, P. &amp; Wilson, J. (1994). The eight fallacies of "
     "distributed computing. Sun Microsystems."),
    ("Didi, A. &amp; Zavodchik, M. (2026). Agent Task/Skill trust "
     "boundaries [cited in Lecture 8]."),
    ("Fairbanks, G. (2010). <i>Just Enough Software Architecture: A "
     "Risk-Driven Approach</i>. Marshall &amp; Brainerd. <b>[Primary "
     "textbook.]</b>"),
    ("Falessi, D., Babar, M. A., Cantone, G. &amp; Kruchten, P. (2010). "
     "Applying empirical software engineering to software architecture: "
     "challenges and lessons learned. <i>Empirical Software Engineering</i>."),
    ("Gustafson, J. L. (1988). Reevaluating Amdahl's law. <i>CACM</i>."),
    ("Hardy, N. (1988). The Confused Deputy. <i>ACM Operating Systems "
     "Review</i>, 22(4)."),
    ("Hertzum, M. &amp; Hornaek, K. (2023). The Computer Frustration "
     "Model. Cited in Lecture 10."),
    ("Hjerppe, K. (2019). GDPR personal-data modules. Cited in Lecture 9."),
    ("Horvat, M. (2016). The Linux network stack poster. <b>[Case 1.]</b>"),
    ("ISO/IEC 25010:2011 (2011). Systems and software Quality Requirements "
     "and Evaluation (SQuaRE) &mdash; System and software quality models."),
    ("Kreuzberger, D., Kuehl, N. &amp; Hirschl, S. (2023). Machine Learning "
     "Operations (MLOps): Overview, definition, and architecture. "
     "<i>IEEE Access</i>. <b>[Case 3.]</b>"),
    ("Kruchten, P. (1995). The 4+1 view model of architecture. <i>IEEE "
     "Software</i>, 12(6), 42-50."),
    ("Lano, K. &amp; Tehrani, S. K. (2025). SOLID principles at component "
     "scope [cited in Lecture 1]."),
    ("Lübke, D., Zimmermann, O. et al. (2019). Five alternatives to "
     "incompatible API changes."),
    ("Montesi, F. &amp; Weber, J. (2016). Circuit breakers, discovery, "
     "and API gateways in microservices. <i>arXiv</i>."),
    ("NCSC (2025). Zero-trust architectural design principles. UK National "
     "Cyber Security Centre."),
    ("OWASP (2024). Top 10 for LLM Applications."),
    ("OWASP (2024). Top 10 CI/CD Security Risks."),
    ("Postel, J. (1996). RFC 1958 &mdash; Architectural principles of the "
     "Internet. (Postel's Robustness Principle.)"),
    ("Rams, D. (1980s). Ten principles for good design. (Subset "
     "reproduced in Lecture 10.)"),
    ("Richards, M. (2015). <i>Software Architecture Patterns</i>. O'Reilly. "
     "(Sync / async notations.)"),
    ("Ruohonen, J. &amp; Alami, A. (2024). Linux kernel regression "
     "patterns. <b>[Cited in Lecture 4.]</b>"),
    ("Ruohonen, J. (2025). Safe and secure defaults. <b>[Cited in Lecture "
     "4.]</b>"),
    ("Ruohonen, J. et al. (2025). Mapping the EU Cyber Resilience Act."),
    ("Sierra, R. (2026). Securing AI agents: identity binding and "
     "non-repudiation. Cited in Lecture 8."),
    ("Silva, P. F. et al. (2022). Suitability metric for reference "
     "architectures. Cited in Lecture 10."),
    ("Vakulov, V. (2026). AI assistance in SOC analysis. Cited in "
     "Lecture 8."),
    ("Williams, R. (2026). Over-engineering as the new technical debt. "
     "Cited in Lecture 5."),
    ("Yang, J., Wang, H. &amp; Liang, P. (2016). Empirical study on "
     "architecture design upfront vs. emergent. <i>JSS</i>."),
    ("Zimmermann, M., Staicu, C.-A., Tenny, C. &amp; Pradel, M. (2019). "
     "Small world with high risks: a study of security threats in the npm "
     "ecosystem. <i>USENIX Security</i>."),
]


def build_bibliography():
    fl = []
    fl.append(Paragraph("Bibliography", STYLES["ChapterTitle"]))
    fl.append(Paragraph(
        "Sources cited in the lectures, the analysis notes and the "
        "chapters. Citations follow the style used by the lecturer "
        "(author-year). Primary textbooks and the lecturer's own "
        "publications are marked in bold.",
        STYLES["Body"]))
    fl.append(Spacer(1, 0.3 * cm))
    bib_style = ParagraphStyle("bib", parent=STYLES["Body"],
                               fontSize=9.5, leading=12.5,
                               leftIndent=12, firstLineIndent=-12,
                               spaceAfter=4)
    for entry in CURATED_BIBLIOGRAPHY:
        fl.append(Paragraph(entry, bib_style))
    return fl


def build_cheat_sheet():
    fl = []
    fl.append(Paragraph("Final cheat sheet (1 page)",
                        STYLES["ChapterTitle"]))
    cs = ParagraphStyle("cs", parent=STYLES["Body"], fontSize=9,
                        leading=11.5, spaceAfter=4)
    h2 = ParagraphStyle("csh", parent=STYLES["Heading3"], fontSize=10.5,
                        leading=13, spaceBefore=4, spaceAfter=2)
    items = [
        ("Bass-Clements-Kazman definition",
         "<i>A software architecture is the set of structures needed to "
         "reason about a computing system; these structures comprise "
         "software elements, relations among them, and properties of "
         "both.</i> Three atoms: <b>elements + relations + properties</b>."),
        ("Ten-term vocabulary",
         "<b>module, interface, component, process, machine, system, "
         "deployment, environment, element, connector</b>."),
        ("6-slot QA scenario template",
         "<b>Source &rarr; Stimulus &rarr; Environment &rarr; Artifact "
         "&rarr; Response &rarr; Response measure.</b> Fill all six for "
         "any QA question."),
        ("ISO/IEC 25010 (eight categories)",
         "Functional suitability, Performance efficiency, Compatibility, "
         "Usability, Reliability, Security, Maintainability, Portability."),
        ("Eight fallacies of distributed computing",
         "Network is reliable; latency is zero; bandwidth is infinite; "
         "network is secure; topology doesn't change; there is one admin; "
         "transport cost is zero; network is homogeneous."),
        ("Nines table",
         "90% = 36.5d/yr; 99% = 3.65d/yr; 99.9% = 8.76h/yr; 99.99% = "
         "52.6m/yr; 99.999% = 5.26m/yr; 99.9999% = 31.5s/yr."),
        ("Postel's robustness principle (RFC 1958)",
         "<i>Be conservative in what you send, be liberal in what you "
         "accept.</i>"),
        ("CAP / PACELC",
         "Under a partition, choose Consistency or Availability. Else "
         "(no partition) you still trade Consistency against Latency. "
         "Cassandra = PA/EL, Spanner-like = PC/EC."),
        ("Cyber kill chain (8 stages)",
         "Initial exploit &rarr; Privilege escalation &rarr; Escape "
         "&rarr; Recon &rarr; Lateral movement &rarr; Exfiltration "
         "&rarr; Tampering &rarr; Persist (RAT)."),
        ("Lecturer's running examples",
         "Flight + hotel reservation (saga); healthcare ER (24/7); "
         "Linux network stack (Case 1, layering); MLOps reference "
         "architecture (Case 3); Postfix (privilege separation); qmail "
         "(privilege drop)."),
        ("Top-three architect job qualities",
         "<b>All three are communication-related</b>: articulation / "
         "transferability, stakeholder management, communication / "
         "negotiation. This is exam-counted."),
        ("Five canonical modifiability moves",
         "<b>Split &middot; Combine &middot; Encapsulate &middot; "
         "Intermediary &middot; Restrict.</b>"),
        ("Availability tactics tree (don't forget Reintroduce)",
         "<b>Detect &middot; Repair &middot; Reintroduce &middot; "
         "Prevent.</b> Reintroduce is the branch students forget."),
        ("Saga (flight + hotel)",
         "Local transactions per service; on success, notify next; on "
         "failure, run compensating transactions backwards."),
    ]
    for h, body in items:
        fl.append(Paragraph(h, h2))
        fl.append(Paragraph(body, cs))
    return fl


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------


def build():
    t0 = time.time()
    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)

    # The story
    story = []

    # --- Cover (no header / footer) ---
    story.append(NextPageTemplate("cover"))
    story.extend(build_cover())
    # Emit chapter marker BEFORE leaving the cover so when the next page
    # (intro) starts, its onPage callback reads the new title.
    story.append(ChapterMarker("How to use this guide"))
    story.append(NextPageTemplate("normal"))
    story.append(PageBreak())

    # --- Intro / course map ---
    story.extend(build_intro())
    story.append(ChapterMarker("Course map"))
    story.append(PageBreak())
    story.extend(build_course_map())

    # --- TOC ---
    toc = TableOfContents()
    toc.levelStyles = [STYLES["TOC1"], STYLES["TOC2"]]
    story.append(ChapterMarker("Table of contents"))
    story.append(PageBreak())
    story.extend(build_toc(toc))

    # --- Chapters ---
    chapter_files = sorted(
        p for p in CHAPTERS_DIR.glob("[0-1][0-9]_*.md")
        if p.stem != "00_outline"
    )
    print(f"Found {len(chapter_files)} chapter files")

    for md_path in chapter_files:
        print(f"  parsing {md_path.name}")
        text = md_path.read_text(encoding="utf-8")
        # Extract chapter title (first '# ' heading) and emit ChapterMarker
        first_h1 = ""
        for ln in text.split("\n"):
            m = re.match(r"^#\s+(.+?)\s*$", ln)
            if m:
                first_h1 = m.group(1).strip()
                break
        # Emit marker BEFORE PageBreak so it updates state before next page starts
        if first_h1:
            story.append(ChapterMarker(first_h1))
        story.append(PageBreak())
        flows = parse_markdown_to_flowables(text, base_dir=md_path.parent)
        story.extend(flows)
        stats["chapters_rendered"] += 1

    # --- Back matter ---
    story.append(ChapterMarker("Glossary"))
    story.append(PageBreak())
    story.extend(build_glossary())
    story.append(ChapterMarker("Acronym index"))
    story.append(PageBreak())
    story.extend(build_acronym_index())
    story.append(ChapterMarker("Bibliography"))
    story.append(PageBreak())
    story.extend(build_bibliography())
    story.append(ChapterMarker("Cheat sheet"))
    story.append(PageBreak())
    story.extend(build_cheat_sheet())

    # --- Build doc ---
    doc = TOCDocTemplate(
        str(OUT_PDF),
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title="Software Architecture - Exam Walkthrough",
        author="ExamPrep build pipeline",
        subject="T630019402 SDU Spring 2026",
    )

    cover_frame = Frame(MARGIN, MARGIN, CONTENT_W, CONTENT_H,
                        id="cover_frame", showBoundary=0)
    normal_frame = Frame(MARGIN, MARGIN, CONTENT_W, CONTENT_H,
                         id="normal_frame", showBoundary=0)
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame],
                     onPage=_draw_cover_blank),
        PageTemplate(id="normal", frames=[normal_frame],
                     onPage=_draw_header_footer),
    ])

    # Build twice for TOC accuracy
    print("Building PDF (multiBuild for TOC)...")
    doc.multiBuild(story)

    elapsed = time.time() - t0

    # --- Verify with PyMuPDF ---
    try:
        import fitz
        d = fitz.open(str(OUT_PDF))
        page_count = len(d)
        mb = os.path.getsize(OUT_PDF) / 1e6
        # Spot-check pages
        print(f"\n=== BUILD COMPLETE ===")
        print(f"PDF:           {OUT_PDF}")
        print(f"Pages:         {page_count}")
        print(f"Size:          {mb:.2f} MB")
        print(f"Time:          {elapsed:.1f}s")
        print(f"Chapters:      {stats['chapters_rendered']}")
        print(f"Images OK:     {stats['images_embedded']}")
        print(f"Images miss:   {stats['images_missing']}")
        print(f"Tables:        {stats['tables_rendered']}")
        print(f"Code blocks:   {stats['code_blocks']}")
        if stats["issues"]:
            print(f"\nIssues ({len(stats['issues'])}):")
            for issue in stats["issues"][:30]:
                print(f"  - {issue}")
            if len(stats["issues"]) > 30:
                print(f"  ... and {len(stats['issues']) - 30} more")
        for pn in (0, min(49, page_count - 1), min(99, page_count - 1),
                   page_count - 1):
            try:
                p = d[pn]
                snippet = (p.get_text() or "")[:120].replace("\n", " | ")
                print(f"\n--- p.{pn + 1} snippet ---\n{snippet}")
            except Exception as exc:
                print(f"  could not read page {pn}: {exc}")
        d.close()
    except Exception as exc:
        print(f"PyMuPDF verify failed: {exc}")

    return OUT_PDF


if __name__ == "__main__":
    build()
