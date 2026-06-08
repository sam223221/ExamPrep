#!/usr/bin/env python3
"""build_pdf.py - Combine the Cybersecurity study-guide Markdown files into one PDF.

This is a self-contained, zero-install build script. It reads the 37 clean
Markdown files under ``study-guide/`` (13 top-level chapters + 12 ``commands/``
+ 12 ``qna/``), renders each to HTML, and composes a single paginated,
bookmarked PDF using PyMuPDF's Story API.

Output
------
``study-guide/Cyber-Security-Study-Guide.pdf``

File order inside the PDF
-------------------------
1. ``00-overview.md``
2. For each chapter N (01..12):
     a. top-level ``NN-*.md`` (main chapter)
     b. ``commands/NN-*.md``
     c. ``qna/NN-*.md``
3. ``exam-prep.md`` last

Each source file starts on a fresh page and gets a top-level PDF bookmark
named after its ``# H1`` title, so all 37 sections are navigable. Page 1 is a
generated title page with an embedded table of contents.

Dependencies (all expected to be globally installed already -- no venv, no
pip install required):
    * markdown   (Python-Markdown, with the tables/fenced_code/codehilite/
                  toc/sane_lists extensions, all bundled)
    * PyMuPDF    (import name ``fitz``; provides Story + DocumentWriter)

Run
---
    python build_pdf.py

The script does NOT modify any of the source ``.md`` files and does NOT touch
the FastAPI app or its environment.
"""

from __future__ import annotations

import html as _html
import io
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

try:
    import fitz  # PyMuPDF
except ImportError as exc:  # pragma: no cover - environment guard
    sys.exit(
        "ERROR: PyMuPDF (import name 'fitz') is not available. "
        "Install it or run with the interpreter that has it.\n"
        f"Underlying import error: {exc}"
    )

try:
    import markdown
except ImportError as exc:  # pragma: no cover - environment guard
    sys.exit(
        "ERROR: the 'markdown' package is not available. "
        "Install it or run with the interpreter that has it.\n"
        f"Underlying import error: {exc}"
    )


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_PDF = SCRIPT_DIR / "Cyber-Security-Study-Guide.pdf"

DOCUMENT_TITLE = "Cybersecurity — Combined Study Guide"
DOCUMENT_SUBTITLE = "Cybersecurity F26 · SDU Centre for Industrial Software"

# Page geometry (A4 with a comfortable margin).
PAGE_RECT = fitz.paper_rect("a4")
MARGIN = 40  # points
CONTENT_RECT = PAGE_RECT + (MARGIN, MARGIN, -MARGIN, -MARGIN)

# Markdown extensions. ``codehilite`` emits <span> classes for syntax colour
# (nice-to-have); the others are required for correct rendering of the source.
MD_EXTENSIONS = ["tables", "fenced_code", "codehilite", "toc", "sane_lists"]
MD_EXTENSION_CONFIGS = {
    # Inline the highlight spans without needing an external stylesheet, and
    # never crash on a code block whose "language" pygments doesn't know.
    "codehilite": {"guess_lang": False, "noclasses": False},
}

# CSS applied to every rendered file. Tables get visible borders + padding;
# code/pre use a monospace font and wrap long lines instead of clipping them.
USER_CSS = """
* { box-sizing: border-box; }

body {
    font-family: serif;
    font-size: 10.5pt;
    line-height: 1.42;
    color: #1a1a1a;
}

h1 {
    font-family: sans-serif;
    font-size: 19pt;
    color: #0d2b45;
    border-bottom: 2px solid #0d2b45;
    padding-bottom: 4px;
    margin: 0 0 12px 0;
}

h2 {
    font-family: sans-serif;
    font-size: 14.5pt;
    color: #14507a;
    border-bottom: 1px solid #c5d4e0;
    padding-bottom: 2px;
    margin: 18px 0 8px 0;
}

h3 {
    font-family: sans-serif;
    font-size: 12.5pt;
    color: #1b5e20;
    margin: 14px 0 6px 0;
}

h4, h5, h6 {
    font-family: sans-serif;
    font-size: 11pt;
    color: #333333;
    margin: 12px 0 5px 0;
}

p { margin: 0 0 8px 0; }

ul, ol { margin: 0 0 8px 0; padding-left: 22px; }
li { margin: 0 0 3px 0; }

a { color: #14507a; text-decoration: none; }

blockquote {
    margin: 0 0 10px 0;
    padding: 4px 10px;
    border-left: 3px solid #b0c4d4;
    background-color: #f3f7fa;
    color: #444444;
    font-size: 10pt;
}

/* Tables: visible grid with padding so columns are readable. */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 8px 0 12px 0;
    font-size: 9.5pt;
}
th, td {
    border: 1px solid #8a9bab;
    padding: 4px 6px;
    text-align: left;
    vertical-align: top;
}
th {
    background-color: #e8eef3;
    font-family: sans-serif;
    color: #0d2b45;
}

/* Inline code and fenced code blocks: monospace + wrap long command lines. */
code {
    font-family: monospace;
    font-size: 9pt;
    background-color: #f0f2f4;
    padding: 0 2px;
}
pre {
    font-family: monospace;
    font-size: 8.5pt;
    background-color: #f5f6f7;
    border: 1px solid #d8dde2;
    padding: 6px 8px;
    margin: 6px 0 12px 0;
    white-space: pre-wrap;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
pre code {
    background-color: transparent;
    padding: 0;
    font-size: 8.5pt;
}

hr { border: none; border-top: 1px solid #cccccc; margin: 14px 0; }
"""

# CSS for the generated title page / table-of-contents page.
TITLE_CSS = """
body { font-family: serif; color: #1a1a1a; }
.title {
    font-family: sans-serif;
    font-size: 30pt;
    color: #0d2b45;
    text-align: center;
    margin: 120px 0 10px 0;
    line-height: 1.2;
}
.subtitle {
    font-family: sans-serif;
    font-size: 13pt;
    color: #14507a;
    text-align: center;
    margin: 0 0 6px 0;
}
.meta {
    font-family: sans-serif;
    font-size: 10pt;
    color: #666666;
    text-align: center;
    margin: 0 0 40px 0;
}
.toc-head {
    font-family: sans-serif;
    font-size: 15pt;
    color: #0d2b45;
    border-bottom: 1px solid #c5d4e0;
    padding-bottom: 3px;
    margin: 30px 0 10px 0;
}
.toc-item {
    font-size: 10pt;
    margin: 0 0 3px 0;
}
.toc-num { color: #888888; }
"""


# --------------------------------------------------------------------------- #
# File ordering
# --------------------------------------------------------------------------- #

# Regex to pull the leading "NN" numeric prefix off a filename like
# "03-penetration-testing.md".
_PREFIX_RE = re.compile(r"^(\d{2})-")


@dataclass
class Section:
    """One source file destined for one PDF section."""

    path: Path
    label: str  # short human label used only for the build log


def _glob_by_prefix(folder: Path, prefix: str) -> Path:
    """Return the single ``NN-*.md`` file in *folder* whose name starts with
    *prefix* (e.g. ``"03"``). Raises if zero or more than one match -- we want
    the order to be unambiguous, not silently wrong."""
    matches = sorted(folder.glob(f"{prefix}-*.md"))
    if not matches:
        raise FileNotFoundError(
            f"No file matching '{prefix}-*.md' found in {folder}"
        )
    if len(matches) > 1:
        names = ", ".join(m.name for m in matches)
        raise RuntimeError(
            f"Ambiguous match for '{prefix}-*.md' in {folder}: {names}"
        )
    return matches[0]


def resolve_order() -> list[Section]:
    """Resolve the exact ordered list of source files per the chosen layout.

    Order:
        00-overview.md
        for N in 01..12: main NN-*.md, commands/NN-*.md, qna/NN-*.md
        exam-prep.md
    """
    base = SCRIPT_DIR
    commands_dir = base / "commands"
    qna_dir = base / "qna"

    for folder in (base, commands_dir, qna_dir):
        if not folder.is_dir():
            raise FileNotFoundError(f"Expected source folder is missing: {folder}")

    sections: list[Section] = []

    # 1) Overview.
    overview = base / "00-overview.md"
    if not overview.is_file():
        raise FileNotFoundError(f"Missing required file: {overview}")
    sections.append(Section(overview, "00-overview"))

    # 2) Per-chapter grouping 01..12.
    for n in range(1, 13):
        prefix = f"{n:02d}"
        main = _glob_by_prefix(base, prefix)
        cmd = _glob_by_prefix(commands_dir, prefix)
        qna = _glob_by_prefix(qna_dir, prefix)
        sections.append(Section(main, f"{prefix} main"))
        sections.append(Section(cmd, f"{prefix} commands"))
        sections.append(Section(qna, f"{prefix} qna"))

    # 3) Exam prep last.
    exam = base / "exam-prep.md"
    if not exam.is_file():
        raise FileNotFoundError(f"Missing required file: {exam}")
    sections.append(Section(exam, "exam-prep"))

    return sections


# --------------------------------------------------------------------------- #
# Markdown -> HTML
# --------------------------------------------------------------------------- #

_H1_RE = re.compile(r"^\s*#\s+(.*?)\s*#*\s*$", re.MULTILINE)


def _strip_fenced_code(md_text: str) -> str:
    """Return *md_text* with the contents of ``` fenced code blocks ``` removed,
    so a ``#`` *comment* inside a code block cannot be mistaken for an H1.

    The fence lines themselves are kept (as blanks) only insofar as we drop the
    block body; surrounding prose and any real ``# H1`` heading are preserved.
    """
    lines = md_text.split("\n")
    kept: list[str] = []
    in_fence = False
    for line in lines:
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            continue  # drop the fence marker line itself
        if not in_fence:
            kept.append(line)
    return "\n".join(kept)


def extract_h1_title(md_text: str, fallback: str) -> str:
    """Return the first ``# H1`` title from *md_text*, or *fallback* if none.

    Fenced code blocks are stripped before the search so a ``#`` line inside a
    code block (e.g. a shell comment) can never be misread as the title.
    """
    match = _H1_RE.search(_strip_fenced_code(md_text))
    if match:
        title = match.group(1).strip()
        if title:
            return title
    return fallback


# A GFM table *delimiter* row: pipe-separated cells made only of dashes and
# optional alignment colons, e.g. ``|---|---|`` or ``| :--- | ---: |``. The
# leading pipe is optional. We require at least one pipe and at least one run of
# two-or-more dashes so a lone ``---`` horizontal rule never matches.
_TABLE_DELIM_RE = re.compile(r"^\s*\|?\s*:?-{2,}.*\|.*$")

# Opening/closing of a ``` fenced code block (optional indent + optional info
# string). Pipes inside such blocks (shell pipelines, ASCII-art DFD legends) are
# literal content and must never be treated as table markup.
_FENCE_RE = re.compile(r"^\s*```")


def fix_table_spacing(md_text: str) -> str:
    """Insert a blank line before any GFM pipe table that is glued directly to
    the line above it.

    Why this exists
    ---------------
    Python-Markdown's ``tables`` extension only recognises a table when a blank
    line separates it from the preceding paragraph. If a source file writes a
    table header immediately under a non-blank line (e.g. an answer that starts
    ``A.`` on its own line, with the ``| ... |`` header on the very next line),
    the whole block is swallowed into one paragraph and the table renders as
    literal ``| ... |`` pipe text in the PDF. We harden the *build* against this
    class of authoring quirk instead of editing the user's source ``.md`` files.

    Heuristic (deliberately conservative)
    -------------------------------------
    For each line, insert a blank line *before* it when ALL of:
      * the line itself contains ``|`` (it looks like a table header row), AND
      * the next line is a table delimiter row (``|---|---|`` style), AND
      * the previous line is non-blank and is NOT itself a table line
        (contains no ``|``) -- i.e. the table is glued to a paragraph.

    Lines inside ``` fenced code blocks ``` are skipped entirely, so shell
    pipelines and ASCII-art diagrams are never disturbed. Tables that are
    already correctly separated (blank line above the header) do not match, so
    this transform is idempotent and leaves the 16 well-formed tables untouched.
    """
    lines = md_text.split("\n")
    out: list[str] = []
    in_fence = False

    for i, line in enumerate(lines):
        # Track fenced-code-block boundaries so we never touch their contents.
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue

        if not in_fence and "|" in line and i + 1 < len(lines):
            next_line = lines[i + 1]
            prev_line = lines[i - 1] if i > 0 else ""
            looks_like_header = _TABLE_DELIM_RE.match(next_line) is not None
            glued_to_paragraph = bool(prev_line.strip()) and "|" not in prev_line
            if looks_like_header and glued_to_paragraph:
                out.append("")  # the missing blank line the table needs

        out.append(line)

    return "\n".join(out)


def render_html(md_text: str) -> str:
    """Render Markdown *md_text* to a full standalone HTML document string."""
    # A fresh converter per file avoids state bleeding between documents
    # (notably the ``toc`` and ``codehilite`` extensions keep per-run state).
    md = markdown.Markdown(
        extensions=MD_EXTENSIONS,
        extension_configs=MD_EXTENSION_CONFIGS,
        output_format="html5",
    )
    # Normalise table spacing first so a table glued to the paragraph above it
    # still renders as a real bordered table (see fix_table_spacing).
    body = md.convert(fix_table_spacing(md_text))
    return f"<html><head></head><body>{body}</body></html>"


# --------------------------------------------------------------------------- #
# PDF composition
# --------------------------------------------------------------------------- #

@dataclass
class Bookmark:
    title: str
    page: int  # 1-based page number where the section starts


def _write_story_pages(
    writer: fitz.DocumentWriter, html: str, user_css: str
) -> int:
    """Render one HTML document through a Story onto *writer*, one or more
    pages. Returns the number of pages written for this document.

    Each call begins on a fresh page, which is exactly the "each source file
    starts on a new page" requirement.
    """
    story = fitz.Story(html=html, user_css=user_css, em=11)
    pages_written = 0
    more = True
    while more:
        device = writer.begin_page(PAGE_RECT)
        more, _ = story.place(CONTENT_RECT)
        story.draw(device)
        writer.end_page()
        pages_written += 1
        # Safety valve: a single source file producing an absurd number of
        # pages almost certainly means a layout loop. Fail loudly.
        if pages_written > 2000:
            raise RuntimeError(
                "A single section exceeded 2000 pages - aborting to avoid "
                "an infinite layout loop."
            )
    return pages_written


def _build_title_html(sections: list[Section], titles: list[str]) -> str:
    """Build the HTML for the title + table-of-contents page."""
    items: list[str] = []
    for idx, title in enumerate(titles, start=1):
        safe = _html.escape(title)
        items.append(
            f'<div class="toc-item"><span class="toc-num">{idx:02d}.</span> {safe}</div>'
        )
    toc_block = "\n".join(items)
    return (
        "<html><head></head><body>"
        f'<div class="title">{_html.escape(DOCUMENT_TITLE)}</div>'
        f'<div class="subtitle">{_html.escape(DOCUMENT_SUBTITLE)}</div>'
        f'<div class="meta">{len(titles)} sections · generated by build_pdf.py</div>'
        f'<div class="toc-head">Contents</div>'
        f"{toc_block}"
        "</body></html>"
    )


def _iter_title_pages(html: str) -> Iterator[fitz.Story]:
    """Yield a Story for the title page (kept tiny; usually one page)."""
    yield fitz.Story(html=html, user_css=TITLE_CSS, em=11)


def build_pdf(sections: list[Section]) -> tuple[int, list[Bookmark]]:
    """Render every section into ``OUTPUT_PDF`` and return
    ``(page_count, bookmarks)``.

    Strategy:
      1. Write the content body (all 37 sections) to a temporary writer,
         capturing each file's H1 title and start page.
      2. Render the title page separately.
      3. Stitch title page + body into the final document, then apply the
         outline (TOC) offset by the title page count.
    """
    titles: list[str] = []
    md_texts: list[str] = []

    # Read + render every file up front so a read/parse failure aborts before
    # we start writing any PDF bytes.
    for section in sections:
        try:
            text = section.path.read_text(encoding="utf-8")
        except OSError as exc:
            raise RuntimeError(f"Could not read {section.path}: {exc}") from exc
        title = extract_h1_title(text, fallback=section.path.stem)
        titles.append(title)
        md_texts.append(text)

    # ----- Pass 1: render the content body to an in-memory PDF. ----------- #
    # PyMuPDF's DocumentWriter needs a path or a writable stream (not a
    # Document object), so we render into a BytesIO buffer and reopen it.
    body_buffer = io.BytesIO()
    body_writer = fitz.DocumentWriter(body_buffer)

    content_bookmarks: list[Bookmark] = []
    body_page_cursor = 0  # 0-based count of body pages written so far

    for section, text, title in zip(sections, md_texts, titles):
        try:
            html = render_html(text)
        except Exception as exc:  # markdown conversion failure
            raise RuntimeError(
                f"Markdown rendering failed for {section.path}: {exc}"
            ) from exc

        start_page_in_body = body_page_cursor  # 0-based
        try:
            written = _write_story_pages(body_writer, html, USER_CSS)
        except Exception as exc:
            raise RuntimeError(
                f"PDF layout failed for {section.path}: {exc}"
            ) from exc
        body_page_cursor += written
        # Bookmark page is 1-based within the body; the title-page offset is
        # added when we know it.
        content_bookmarks.append(Bookmark(title, start_page_in_body + 1))

    body_writer.close()
    body_doc = fitz.open(stream=body_buffer.getvalue(), filetype="pdf")

    # ----- Render the title page into its own PDF. ------------------------ #
    title_html = _build_title_html(sections, titles)
    title_buffer = io.BytesIO()
    title_writer = fitz.DocumentWriter(title_buffer)
    title_pages = 0
    for story in _iter_title_pages(title_html):
        more = True
        while more:
            device = title_writer.begin_page(PAGE_RECT)
            more, _ = story.place(CONTENT_RECT)
            story.draw(device)
            title_writer.end_page()
            title_pages += 1
            if title_pages > 50:
                raise RuntimeError("Title page overflowed 50 pages - aborting.")
    title_writer.close()
    title_doc = fitz.open(stream=title_buffer.getvalue(), filetype="pdf")

    # ----- Stitch: title page(s) first, then the body. ------------------- #
    final_doc = fitz.open()
    final_doc.insert_pdf(title_doc)
    final_doc.insert_pdf(body_doc)
    title_doc.close()
    body_doc.close()

    # Outline: one top-level entry per source file, page offset by the title
    # page count. set_toc expects 1-based page numbers.
    toc = [
        [1, bm.title, bm.page + title_pages] for bm in content_bookmarks
    ]
    final_doc.set_toc(toc)

    # Document metadata.
    final_doc.set_metadata(
        {
            "title": DOCUMENT_TITLE,
            "subject": "Cybersecurity F26 combined study guide",
            "creator": "build_pdf.py (PyMuPDF Story API)",
            "producer": "PyMuPDF",
        }
    )

    page_count = final_doc.page_count
    final_doc.save(str(OUTPUT_PDF), garbage=4, deflate=True)
    final_doc.close()

    bookmarks = [Bookmark(bm.title, bm.page + title_pages) for bm in content_bookmarks]
    return page_count, bookmarks


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

def main() -> int:
    print("=" * 70)
    print("Building combined Cybersecurity study-guide PDF")
    print("=" * 70)

    try:
        sections = resolve_order()
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"\nERROR resolving source file order: {exc}", file=sys.stderr)
        return 1

    print(f"\nResolved {len(sections)} source files in this order:\n")
    for idx, section in enumerate(sections, start=1):
        rel = section.path.relative_to(SCRIPT_DIR)
        print(f"  {idx:2d}. [{section.label:>13}]  {rel}")

    if len(sections) != 37:
        print(
            f"\nWARNING: expected 37 source files but resolved {len(sections)}.",
            file=sys.stderr,
        )

    print(f"\nRendering -> {OUTPUT_PDF}")
    try:
        page_count, bookmarks = build_pdf(sections)
    except RuntimeError as exc:
        print(f"\nERROR building PDF: {exc}", file=sys.stderr)
        return 1

    print("\nDone.")
    print(f"  Output file : {OUTPUT_PDF}")
    print(f"  Pages       : {page_count}")
    print(f"  Bookmarks   : {len(bookmarks)}")
    print("\nBookmark map (title -> 1-based start page):")
    for bm in bookmarks:
        print(f"    p.{bm.page:>4}  {bm.title}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
