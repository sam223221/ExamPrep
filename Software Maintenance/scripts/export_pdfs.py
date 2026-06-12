"""Export all study guides in data/guides/ to PDF for exam-day offline use.

Pipeline (fully local, zero network):
    1. Render each guide's Markdown to styled HTML (python-markdown, "extra" +
       "sane_lists" extensions: GFM-ish tables, fenced code, bold/italics).
    2. Print each HTML file to PDF with a locally installed Chromium browser
       (Microsoft Edge preferred, Google Chrome fallback) in headless mode.
       Output is a real text layer - selectable and searchable, never rasterized.
    3. Post-process with PyMuPDF (fitz): inject a bookmark outline into every
       per-guide PDF (H1 + all H2 sections) and build the combined
       SB5-MAI-complete-notes.pdf with a two-level outline
       (level 1 = guide, level 2 = H2 section).

Heading detection: H1/H2 elements are given unique CSS font sizes (26px/19px),
so their rendered spans are identified in the PDF by exact font size. This is
how bookmark target pages are found without guessing from text matches.

Outputs (all under notes-pdf/):
    <guide-stem>.pdf            one per guide, deterministic course order
    SB5-MAI-complete-notes.pdf  all guides concatenated, with bookmarks

Usage:
    python scripts/export_pdfs.py                 # build everything + merge
    python scripts/export_pdfs.py --only 00-overview,lecture-01
    python scripts/export_pdfs.py --skip-existing # resume an interrupted run
    python scripts/export_pdfs.py --merge-only    # rebuild only the combined PDF

Deterministic guide order: 00-overview, lecture-01..lecture-11, 90, 91, 92,
93, 94. Paths are project-root-relative (derived from this file's location).
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import fitz  # PyMuPDF
import markdown

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GUIDES_DIR = PROJECT_ROOT / "data" / "guides"
OUT_DIR = PROJECT_ROOT / "notes-pdf"
COMBINED_NAME = "SB5-MAI-complete-notes.pdf"
COMBINED_TITLE = "SB5-MAI Software Maintenance - Complete Study Notes"

# Browser candidates, in order of preference. Only local executables; the
# rendered HTML references no remote resources, so no network is touched.
BROWSER_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]
BROWSER_NAMES = ["msedge", "chrome"]  # PATH fallbacks

PER_GUIDE_TIMEOUT_S = 600  # largest guide is ~46k words; minutes of headroom

# Heading font sizes. Chosen to be UNIQUE in the stylesheet so headings can be
# recovered from the PDF by font size alone (1 px = 0.75 pt in print).
H1_PX = 26
H2_PX = 19
PX_TO_PT = 0.75
H1_PT = H1_PX * PX_TO_PT  # 19.5
H2_PT = H2_PX * PX_TO_PT  # 14.25
SIZE_TOL = 0.35

MD_EXTENSIONS = ["extra", "sane_lists"]

CSS = f"""
@page {{ size: A4; margin: 16mm 15mm 18mm 15mm; }}
* {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 10.5pt; line-height: 1.45; color: #1c2733; margin: 0;
}}
h1, h2, h3, h4 {{
  font-family: 'Segoe UI', Arial, sans-serif;
  line-height: 1.25; page-break-after: avoid; page-break-inside: avoid;
}}
h1 {{
  font-size: {H1_PX}px; color: #102a43;
  border-bottom: 3px solid #1a3a5c; padding-bottom: 6px; margin: 0 0 18px 0;
}}
h2 {{
  font-size: {H2_PX}px; color: #14365c;
  border-bottom: 1.5px solid #b8c7d9; padding-bottom: 4px; margin-top: 26px;
}}
h3 {{ font-size: 14.5px; color: #1f4e79; margin-top: 18px; }}
h4 {{ font-size: 12px; color: #333; }}
/* Inline code inside headings must inherit the heading size so font-size
   based heading detection (and visual hierarchy) stays intact. */
h1 code, h2 code, h3 code, h4 code {{ font-size: inherit; background: none; }}
code, pre {{ font-family: 'Cascadia Mono', Consolas, 'Courier New', monospace; }}
code {{ font-size: 9pt; background: #eef1f5; padding: 0.5px 3px; border-radius: 3px; }}
pre {{
  font-size: 8.5pt; line-height: 1.35;
  background: #f6f8fa; border: 0.5pt solid #d6dde6; border-radius: 4px;
  padding: 8px 10px; margin: 10px 0;
  white-space: pre-wrap; overflow-wrap: anywhere;  /* never clip off-page */
}}
pre code {{ background: none; padding: 0; font-size: inherit; }}
table {{
  border-collapse: collapse; width: 100%; margin: 10px 0;
  font-family: 'Segoe UI', Arial, sans-serif; font-size: 9pt;
}}
th, td {{
  border: 0.5pt solid #9fb0c1; padding: 4px 6px;
  text-align: left; vertical-align: top; overflow-wrap: anywhere;
}}
th {{ background: #e8eef5; }}
tr:nth-child(even) td {{ background: #f7f9fb; }}
tr {{ page-break-inside: avoid; }}
blockquote {{
  border-left: 3px solid #8899bb; background: #f4f6fa; color: #2a3540;
  margin: 10px 0 10px 4px; padding: 2px 12px;
}}
ul, ol {{ padding-left: 22px; }}
li {{ margin: 2px 0; }}
hr {{ border: none; border-top: 1px solid #c5ccd4; margin: 16px 0; }}
a {{ color: inherit; text-decoration: none; }}
img {{ max-width: 100%; }}
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
{body}
</body>
</html>
"""


def discover_guides() -> list[Path]:
    """Return the 16 content guides in deterministic course order.

    Order: 00-overview, lecture-01..lecture-11 (numeric), then the 9x exam /
    lab series (90, 91, 92, 93, 94). DOCUMENT.md and any non-conforming file
    names are excluded.
    """
    overview: list[tuple[int, Path]] = []
    lectures: list[tuple[int, Path]] = []
    exam_series: list[tuple[int, Path]] = []
    for path in sorted(GUIDES_DIR.glob("*.md")):
        lecture_match = re.match(r"^lecture-(\d{2})-", path.name)
        prefix_match = re.match(r"^(\d{2})-", path.name)
        if lecture_match:
            lectures.append((int(lecture_match.group(1)), path))
        elif prefix_match:
            num = int(prefix_match.group(1))
            (overview if num < 10 else exam_series).append((num, path))
        # anything else (e.g. DOCUMENT.md) is not a content guide
    ordered = (
        [p for _, p in sorted(overview)]
        + [p for _, p in sorted(lectures)]
        + [p for _, p in sorted(exam_series)]
    )
    return ordered


def find_browser() -> str:
    for candidate in BROWSER_CANDIDATES:
        if Path(candidate).is_file():
            return candidate
    for name in BROWSER_NAMES:
        found = shutil.which(name)
        if found:
            return found
    raise RuntimeError(
        "No Chromium-based browser found (tried Edge and Chrome). Install one or add it to PATH."
    )


def normalize(text: str) -> str:
    """Collapse all whitespace runs to single spaces and strip."""
    return " ".join(text.split())


def strip_inline_markup(heading: str) -> str:
    """Reduce a Markdown heading to its rendered plain text."""
    return normalize(heading.replace("**", "").replace("`", "").replace("*", ""))


def md_heading_inventory(md_text: str) -> tuple[str, list[str]]:
    """Return (H1 title, list of H2 titles) from Markdown, skipping code fences."""
    h1 = ""
    h2s: list[str] = []
    in_fence = False
    for line in md_text.splitlines():
        stripped = line.rstrip()
        if re.match(r"^(```|~~~)", stripped):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if stripped.startswith("## ") and not stripped.startswith("###"):
            h2s.append(strip_inline_markup(stripped[3:]))
        elif stripped.startswith("# ") and not h1:
            h1 = strip_inline_markup(stripped[2:])
    return h1, h2s


def render_html(md_path: Path, html_path: Path) -> None:
    md_text = md_path.read_text(encoding="utf-8")
    body = markdown.markdown(md_text, extensions=MD_EXTENSIONS)
    title, _ = md_heading_inventory(md_text)
    page = HTML_TEMPLATE.format(title=title or md_path.stem, css=CSS, body=body)
    html_path.write_text(page, encoding="utf-8")


def html_to_pdf(browser: str, html_path: Path, pdf_path: Path, profile_dir: Path) -> None:
    """Print an HTML file to PDF via headless Chromium. Atomic on success."""
    tmp_pdf = pdf_path.with_suffix(".pdf.tmp")
    tmp_pdf.unlink(missing_ok=True)
    cmd = [
        browser,
        "--headless",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-extensions",
        "--disable-sync",
        "--disable-background-networking",
        "--disable-component-update",
        f"--user-data-dir={profile_dir}",
        "--no-pdf-header-footer",
        f"--print-to-pdf={tmp_pdf}",
        html_path.resolve().as_uri(),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=PER_GUIDE_TIMEOUT_S)
    if not tmp_pdf.is_file() or tmp_pdf.stat().st_size == 0:
        raise RuntimeError(
            f"Browser failed to produce {pdf_path.name} "
            f"(exit {result.returncode}): {result.stderr[-500:]}"
        )
    tmp_pdf.replace(pdf_path)


def detect_headings(
    doc: fitz.Document,
) -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    """Find rendered H1/H2 headings by their unique font sizes.

    Returns two lists of (0-based page index, heading text), in reading order.
    Wrapped headings (multiple lines in one text block) are joined back into a
    single title.
    """
    h1s: list[tuple[int, str]] = []
    h2s: list[tuple[int, str]] = []
    for page_index in range(doc.page_count):
        page_dict = doc[page_index].get_text("dict")
        for block in page_dict["blocks"]:
            if block.get("type") != 0:
                continue
            h1_parts: list[str] = []
            h2_parts: list[str] = []
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    size = span.get("size", 0.0)
                    if abs(size - H1_PT) < SIZE_TOL:
                        h1_parts.append(span["text"])
                    elif abs(size - H2_PT) < SIZE_TOL:
                        h2_parts.append(span["text"])
            if h1_parts:
                h1s.append((page_index, normalize(" ".join(h1_parts))))
            if h2_parts:
                h2s.append((page_index, normalize(" ".join(h2_parts))))
    return h1s, h2s


def export_guide(browser: str, md_path: Path, build_dir: Path, profile_dir: Path) -> Path:
    """Render one guide to notes-pdf/<stem>.pdf with its own bookmark outline."""
    pdf_path = OUT_DIR / f"{md_path.stem}.pdf"
    html_path = build_dir / f"{md_path.stem}.html"
    render_html(md_path, html_path)
    html_to_pdf(browser, html_path, pdf_path, profile_dir)

    md_title, md_h2s = md_heading_inventory(md_path.read_text(encoding="utf-8"))
    with fitz.open(pdf_path) as doc:
        h1s, h2s = detect_headings(doc)
        title = h1s[0][1] if h1s else (md_title or md_path.stem)
        toc = [[1, title, 1]]
        toc += [[2, text, page + 1] for page, text in h2s]
        doc.set_toc(toc)
        doc.saveIncr()
        pages = doc.page_count
        if len(h2s) != len(md_h2s):
            print(
                f"  WARNING {md_path.stem}: markdown has {len(md_h2s)} H2s "
                f"but {len(h2s)} were detected in the PDF"
            )
        print(f"  {md_path.stem}.pdf: {pages} pages, {len(h2s)}/{len(md_h2s)} H2 bookmarks")
    return pdf_path


def merge_guides(guides: list[Path]) -> None:
    """Concatenate per-guide PDFs into the combined volume with bookmarks."""
    combined_path = OUT_DIR / COMBINED_NAME
    combined = fitz.open()
    toc: list[list] = []
    for md_path in guides:
        pdf_path = OUT_DIR / f"{md_path.stem}.pdf"
        if not pdf_path.is_file():
            raise RuntimeError(f"Missing {pdf_path.name}; run without --merge-only first.")
        with fitz.open(pdf_path) as part:
            offset = combined.page_count
            combined.insert_pdf(part)
            part_toc = part.get_toc(simple=True)
        if part_toc:
            for level, title, page in part_toc:
                toc.append([level, title, page + offset])
        else:
            md_title, _ = md_heading_inventory(md_path.read_text(encoding="utf-8"))
            toc.append([1, md_title or md_path.stem, offset + 1])
    combined.set_toc(toc)
    combined.set_metadata(
        {
            "title": COMBINED_TITLE,
            "author": "SB5-MAI exam prep",
            "creator": "scripts/export_pdfs.py",
        }
    )
    combined.save(combined_path, garbage=4, deflate=True)
    pages = combined.page_count
    bookmarks = len(toc)
    combined.close()
    size_mb = combined_path.stat().st_size / (1024 * 1024)
    print(f"  {COMBINED_NAME}: {pages} pages, {bookmarks} bookmarks, {size_mb:.1f} MB")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export data/guides/*.md to notes-pdf/*.pdf (+ combined)."
    )
    parser.add_argument(
        "--only",
        help="Comma-separated guide-stem prefixes to (re)build; skips merge.",
    )
    parser.add_argument(
        "--merge-only",
        action="store_true",
        help="Skip per-guide conversion; rebuild the combined PDF only.",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip guides whose PDF already exists and is newer than the .md.",
    )
    args = parser.parse_args()

    guides = discover_guides()
    if not guides:
        print(f"No guides found in {GUIDES_DIR}", file=sys.stderr)
        return 1
    print(f"{len(guides)} guides in {GUIDES_DIR}")
    OUT_DIR.mkdir(exist_ok=True)

    if not args.merge_only:
        selected = guides
        if args.only:
            prefixes = [p.strip() for p in args.only.split(",") if p.strip()]
            selected = [g for g in guides if any(g.stem.startswith(p) for p in prefixes)]
            if not selected:
                print(f"--only matched no guides: {args.only}", file=sys.stderr)
                return 1
        browser = find_browser()
        print(f"Browser: {browser}")
        with tempfile.TemporaryDirectory(prefix="export_pdfs_") as tmp:
            build_dir = Path(tmp) / "html"
            profile_dir = Path(tmp) / "profile"
            build_dir.mkdir()
            profile_dir.mkdir()
            for md_path in selected:
                pdf_path = OUT_DIR / f"{md_path.stem}.pdf"
                if (
                    args.skip_existing
                    and pdf_path.is_file()
                    and pdf_path.stat().st_mtime > md_path.stat().st_mtime
                ):
                    print(f"  {pdf_path.name}: up to date, skipped")
                    continue
                export_guide(browser, md_path, build_dir, profile_dir)

    if args.merge_only or not args.only:
        merge_guides(guides)
    return 0


if __name__ == "__main__":
    sys.exit(main())
