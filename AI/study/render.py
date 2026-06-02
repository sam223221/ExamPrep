"""Markdown -> PDF renderer for the AI Exam Prep study package.

Implements spec section 10 (Rendering Pipeline) from:
    docs/superpowers/specs/2026-05-22-ai-exam-prep-study-package-design.md

Pipeline (primary path):
    1. Walk ``study/lectures/`` for every ``*.md`` (10 lecture chapters)
       and ``study/00-master-index.md``.
    2. For each, convert Markdown -> HTML via the ``markdown`` library with
       the pinned extensions (tables, fenced_code, footnotes, attr_list,
       def_list, codehilite, pymdownx.arithmatex passthrough, and the
       ``markdown-katex`` extension which server-side-renders ``$...$`` and
       ``$$...$$`` to KaTeX HTML).
    3. Wrap the HTML body in ``study/_shared/html-template.html`` after
       substituting ``{{ title }}`` (the first H1 of the source) and
       ``{{ body }}`` (the converted markdown).
    4. Hand the HTML to WeasyPrint to produce ``<basename>.pdf`` next to
       the source ``.md``.

Fallback chain (per spec sec.10):
    - If WeasyPrint cannot be imported (or its native runtime fails to load):
      try ``pdfkit`` + ``wkhtmltopdf``.
    - If ``pdfkit`` is also unavailable: emit styled ``.html`` files next to
      each source ``.md`` and surface the degraded path in the run summary.

Hard constraints (Appendix A.9 of the plan):
    - Idempotent. Running the script twice produces identical output.
    - Never deletes or rewrites any ``.md`` file.
    - Never touches any ``*_solution.*`` file or anything outside the
      ``study/lectures/`` and ``study/`` (master index) targets.

Usage:
    py -3.12 study/render.py
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# WeasyPrint native runtime (GTK3) MUST be on PATH before ``import weasyprint``
# on Windows. See study/_shared/TOOLCHAIN.md. We do this unconditionally; if
# the directory does not exist (non-Windows host, or different MSYS2 install
# location), nothing happens.
# ---------------------------------------------------------------------------

import os
import sys

_GTK_RUNTIME_DIR = r"C:\msys64\mingw64\bin"
if os.path.isdir(_GTK_RUNTIME_DIR):
    if _GTK_RUNTIME_DIR not in os.environ.get("PATH", ""):
        os.environ["PATH"] = _GTK_RUNTIME_DIR + os.pathsep + os.environ.get("PATH", "")

import html as html_lib
import logging
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("render")

# fontTools (used by WeasyPrint for PDF font subsetting) emits very chatty
# INFO logs — one line per glyph table per font per page. Mute it.
for _noisy in ("fontTools", "fontTools.subset", "fontTools.ttLib", "weasyprint"):
    logging.getLogger(_noisy).setLevel(logging.WARNING)

# ---------------------------------------------------------------------------
# Paths (all derived from this file's location so the script is portable).
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent          # .../study
STUDY_ROOT = SCRIPT_DIR
LECTURES_DIR = STUDY_ROOT / "lectures"
SHARED_DIR = STUDY_ROOT / "_shared"
TEMPLATE_PATH = SHARED_DIR / "html-template.html"
STYLESHEET_PATH = SHARED_DIR / "style.css"
MASTER_INDEX_MD = STUDY_ROOT / "00-master-index.md"

# Files inside lectures/ that are NOT chapter PDFs to render (housekeeping
# markdown that the lecture extractors or PM dropped in place).
LECTURE_EXCLUDE_NAMES = {"DOCUMENT.md"}

# Min PDF size we consider "rendered, not a stub". The verifier enforces 50 KB;
# we report against the same threshold so failures are visible immediately.
MIN_PDF_BYTES = 50 * 1024


# ---------------------------------------------------------------------------
# Lazy markdown / weasyprint / pdfkit imports
# ---------------------------------------------------------------------------
# We import ``markdown`` eagerly because it has no native dependencies, but
# defer ``weasyprint`` / ``pdfkit`` until we know which path we are taking.
# This lets us produce a useful diagnostic if the GTK runtime is missing
# without aborting the script outright.

import markdown as md_mod  # noqa: E402  (post-PATH-mutation, intentional)


# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------


@dataclass
class RenderResult:
    """One row of the final summary table."""

    source_md: Path
    output_path: Path           # the *.pdf (or *.html if degraded)
    success: bool
    size_bytes: int = 0
    path_taken: str = ""        # "weasyprint" | "pdfkit" | "html-only" | "skipped"
    error: Optional[str] = None
    duration_s: float = 0.0
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Markdown -> HTML conversion
# ---------------------------------------------------------------------------


def _build_markdown_converter() -> md_mod.Markdown:
    """Construct the configured ``markdown.Markdown`` instance.

    Extensions (matched against spec sec.10):
      - ``tables``                — pipe-style tables.
      - ``fenced_code``           — ```lang ... ``` fences.
      - ``footnotes``             — `[^1]` references.
      - ``attr_list``             — `{#id .class}` attributes on blocks/inlines.
      - ``def_list``              — definition lists.
      - ``codehilite``            — Pygments classes on fenced code (CSS in style.css).
      - ``markdown_katex``        — server-side KaTeX renderer. Owns the
                                    ``$...$`` and ``$$...$$`` math delimiters
                                    end-to-end and emits real HTML (no client
                                    JS required), which is what WeasyPrint
                                    needs to paginate math gracefully.
      - ``toc``                   — generates ``id`` attributes on every
                                    heading. Configured with the
                                    ``pymdownx.slugs.slugify(case="lower")``
                                    slugifier so anchor IDs match GitHub's
                                    GFM-style double-hyphen output (e.g.
                                    ``"1. Overview & Motivation"`` becomes
                                    ``#1-overview--motivation``). The
                                    master index (``00-master-index.md``)
                                    was authored against GFM slugs, so
                                    Python-Markdown's default single-hyphen
                                    slugifier would leave its anchors
                                    broken in the rendered PDF.

    Note on ``pymdownx.arithmatex``: spec sec.10 lists arithmatex as a math
    passthrough option, but arithmatex and markdown_katex compete for the
    same delimiters — whichever runs first wins. Because we have committed to
    server-side KaTeX rendering (so the PDF carries no JS), we let
    markdown_katex own the math pass exclusively. Arithmatex would only be
    needed if we were emitting MathJax script tags for a web target.
    """
    # ``codehilite`` adds Pygments class hooks; the stylesheet already paints
    # ``pre`` and ``code`` so we don't ship a Pygments stylesheet too.
    from pymdownx.slugs import slugify as gfm_slugify  # noqa: WPS433 — local import

    extensions = [
        "tables",
        "fenced_code",
        "footnotes",
        "attr_list",
        "def_list",
        "codehilite",
        "markdown_katex",
        "toc",
    ]

    extension_configs = {
        "markdown_katex": {
            # markdown_katex shells out to a bundled KaTeX binary and embeds
            # its output as raw HTML in the document. We let it inject its
            # own font CSS only if no stylesheet handles math — our stylesheet
            # already styles ``.katex`` / ``.katex-display``.
            "no_inline_svg": False,
            "insert_fonts_css": False,
        },
        "codehilite": {
            # ``css_class`` matches the default; we keep it explicit so that
            # if anyone customises style.css later they know the selector.
            "css_class": "codehilite",
            "guess_lang": False,
        },
        "toc": {
            # GFM-compatible slug rules: ``pymdownx.slugs.slugify(case="lower")``
            # preserves consecutive hyphens (so "A & B" -> "a--b"), matching
            # GitHub. Python-Markdown's default ``markdown.extensions.toc.slugify``
            # collapses them to single hyphens, which is what produced the
            # broken anchors flagged by the verifier.
            "slugify": gfm_slugify(case="lower"),
            # Don't inject a <div class="toc"> into the document — we just
            # want heading IDs. Anchor markup itself is suppressed; the
            # browser's `:target` works either way.
            "toc_depth": "1-6",
            "permalink": False,
        },
    }

    return md_mod.Markdown(
        extensions=extensions,
        extension_configs=extension_configs,
        output_format="html5",
        tab_length=4,
    )


_H1_RE = re.compile(r"^\s{0,3}#\s+(.+?)\s*#*\s*$", re.MULTILINE)


def _extract_title(markdown_source: str, fallback: str) -> str:
    """Return the first H1 in the markdown source, or ``fallback``."""
    m = _H1_RE.search(markdown_source)
    if not m:
        return fallback
    # H1 lines occasionally contain inline markdown (e.g. *emphasis*); we
    # strip the most common markup so the <title> stays clean.
    title = m.group(1).strip()
    title = re.sub(r"[`*_]", "", title)
    return title or fallback


def _convert_markdown_to_html(md_path: Path, converter: md_mod.Markdown) -> tuple[str, str]:
    """Read ``md_path``, return (title, html_body)."""
    text = md_path.read_text(encoding="utf-8")
    title = _extract_title(text, fallback=md_path.stem)

    # ``markdown.Markdown`` instances are stateful across .convert() calls
    # (footnote counters etc.); reset before every document to keep output
    # deterministic and idempotent.
    converter.reset()
    body_html = converter.convert(text)
    return title, body_html


# ---------------------------------------------------------------------------
# HTML template wrapping
# ---------------------------------------------------------------------------


def _load_template() -> str:
    if not TEMPLATE_PATH.is_file():
        raise FileNotFoundError(f"HTML template missing: {TEMPLATE_PATH}")
    return TEMPLATE_PATH.read_text(encoding="utf-8")


def _wrap_in_template(template: str, title: str, body_html: str) -> str:
    """Substitute ``{{ title }}`` and ``{{ body }}`` into the template.

    We do not use ``str.format`` because the template contains CSS braces
    and percent-signs from KaTeX output. Plain ``str.replace`` is safest.
    """
    out = template
    out = out.replace("{{ title }}", html_lib.escape(title))
    out = out.replace("{{ body }}", body_html)
    return out


# ---------------------------------------------------------------------------
# Renderer backends
# ---------------------------------------------------------------------------


class RendererBackend:
    """Common protocol for the three rendering paths."""

    name: str = "abstract"

    def render(self, html: str, base_url: Path, out_path: Path) -> None:  # pragma: no cover - interface
        raise NotImplementedError


class WeasyPrintBackend(RendererBackend):
    name = "weasyprint"

    def __init__(self) -> None:
        # Import lazily so an early failure becomes a backend-selection
        # event, not a script-load crash.
        import weasyprint  # noqa: WPS433 — local import is intentional
        self._weasy = weasyprint

    def render(self, html: str, base_url: Path, out_path: Path) -> None:
        # ``base_url`` tells WeasyPrint where to resolve relative links
        # (the <link rel="stylesheet" href="style.css"> in the template,
        # and any <img src="../extracted_figures/..."> in the body).
        doc = self._weasy.HTML(string=html, base_url=str(base_url))
        doc.write_pdf(target=str(out_path))


class PdfKitBackend(RendererBackend):
    name = "pdfkit"

    def __init__(self) -> None:
        import pdfkit  # noqa: WPS433
        self._pdfkit = pdfkit
        # Probe for wkhtmltopdf. pdfkit raises OSError at render() time when
        # the binary is missing; we fail fast here so the PM report reflects
        # the actual cause.
        from shutil import which
        wk = which("wkhtmltopdf") or which("wkhtmltopdf.exe")
        if not wk:
            raise RuntimeError(
                "pdfkit installed but wkhtmltopdf binary not on PATH; cannot use pdfkit backend"
            )
        self._wk_path = wk
        self._config = pdfkit.configuration(wkhtmltopdf=wk)

    def render(self, html: str, base_url: Path, out_path: Path) -> None:
        # pdfkit resolves relative URLs against the *file location*; to keep
        # ``<link href="style.css">`` working we write a temporary HTML next
        # to the template, then convert. Idempotency is preserved because
        # the temporary file is removed in ``finally``.
        import tempfile
        tmp_html = base_url / f".__render_tmp__{out_path.stem}.html"
        try:
            tmp_html.write_text(html, encoding="utf-8")
            options = {
                "encoding": "UTF-8",
                "enable-local-file-access": "",
                "quiet": "",
                "print-media-type": "",
            }
            self._pdfkit.from_file(
                str(tmp_html),
                str(out_path),
                configuration=self._config,
                options=options,
            )
        finally:
            try:
                tmp_html.unlink()
            except FileNotFoundError:
                pass


class HtmlOnlyBackend(RendererBackend):
    """Final fallback: emit a styled ``.html`` next to each ``.md``.

    No PDF is produced; the user is expected to open the file in a browser
    and print to PDF themselves. The verifier's PDF presence check will
    flag this as a regression — that visibility is the point.
    """

    name = "html-only"

    def render(self, html: str, base_url: Path, out_path: Path) -> None:
        # If the caller passed an out_path ending in .pdf we replace the
        # extension; the PM report makes this swap explicit.
        target = out_path.with_suffix(".html")
        target.write_text(html, encoding="utf-8")


def _select_backend() -> RendererBackend:
    """Try the configured backends in priority order, return the first that
    initialises cleanly. Raises only if every backend fails (in which case
    the caller falls back to HtmlOnly explicitly)."""
    candidates: list[tuple[str, type[RendererBackend]]] = [
        ("weasyprint", WeasyPrintBackend),
        ("pdfkit", PdfKitBackend),
    ]
    last_exc: Optional[Exception] = None
    for name, cls in candidates:
        try:
            backend = cls()
            log.info("Selected renderer backend: %s", name)
            return backend
        except Exception as exc:  # noqa: BLE001 — we want every failure mode
            last_exc = exc
            log.warning("Backend %s unavailable: %s", name, exc)
    log.warning("All PDF backends failed; falling back to HTML-only output. Last error: %s", last_exc)
    return HtmlOnlyBackend()


# ---------------------------------------------------------------------------
# Source discovery
# ---------------------------------------------------------------------------


def _discover_sources() -> list[Path]:
    """Return the ordered list of markdown files to render.

    Order: master index first (so it's first in the run summary), then
    every lecture in lexical filename order (L02-... before L11-...).
    """
    sources: list[Path] = []
    if MASTER_INDEX_MD.is_file():
        sources.append(MASTER_INDEX_MD)
    else:
        log.warning("Master index not found at %s — skipping.", MASTER_INDEX_MD)

    if not LECTURES_DIR.is_dir():
        log.error("Lectures directory missing: %s", LECTURES_DIR)
        return sources

    lecture_files = sorted(
        p
        for p in LECTURES_DIR.glob("*.md")
        if p.name not in LECTURE_EXCLUDE_NAMES
    )
    sources.extend(lecture_files)
    return sources


# ---------------------------------------------------------------------------
# Per-document rendering
# ---------------------------------------------------------------------------


def _render_one(
    md_path: Path,
    *,
    converter: md_mod.Markdown,
    template: str,
    backend: RendererBackend,
) -> RenderResult:
    started = time.perf_counter()
    warnings_: list[str] = []
    try:
        title, body_html = _convert_markdown_to_html(md_path, converter)

        # Surface a soft warning if the converted body is implausibly small —
        # this is how silent katex / extension breakage normally appears.
        if len(body_html) < 1024:
            warnings_.append(
                f"Converted HTML for {md_path.name} is only {len(body_html)} chars — "
                "extensions may have failed silently."
            )

        full_html = _wrap_in_template(template, title=title, body_html=body_html)

        # PDF lives next to its source so cross-references (relative ../foo.pdf)
        # work without remapping. base_url is the directory of the source so
        # the template's <link href="style.css"> resolves against _shared/.
        # We solve this by giving WeasyPrint a base_url that points to the
        # template directory — the stylesheet sits there.
        if isinstance(backend, HtmlOnlyBackend):
            out_path = md_path.with_suffix(".html")
        else:
            out_path = md_path.with_suffix(".pdf")

        backend.render(html=full_html, base_url=SHARED_DIR, out_path=out_path)

        size = out_path.stat().st_size if out_path.exists() else 0
        success = size > 0
        result = RenderResult(
            source_md=md_path,
            output_path=out_path,
            success=success,
            size_bytes=size,
            path_taken=backend.name,
            duration_s=time.perf_counter() - started,
            warnings=warnings_,
        )
        if backend.name != "html-only" and size < MIN_PDF_BYTES:
            result.warnings.append(
                f"Output {out_path.name} is {size} B (< {MIN_PDF_BYTES} B threshold)."
            )
        return result
    except Exception as exc:  # noqa: BLE001
        log.exception("Failed to render %s", md_path)
        return RenderResult(
            source_md=md_path,
            output_path=md_path.with_suffix(".pdf"),
            success=False,
            path_taken=backend.name,
            error=f"{type(exc).__name__}: {exc}",
            duration_s=time.perf_counter() - started,
            warnings=warnings_,
        )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def _kb(n: int) -> str:
    return f"{n / 1024:.1f} KB"


def _print_summary(results: list[RenderResult], total_elapsed: float, backend_name: str) -> int:
    """Pretty-print the run summary and return the process exit code."""
    sep = "-" * 78
    print()
    print(sep)
    print(" AI Exam Prep — PDF Render Summary")
    print(sep)
    print(f" Pipeline path: {backend_name}")
    print(f" Sources discovered: {len(results)}")
    print(f" Total wall-clock time: {total_elapsed:.2f}s")
    print(sep)

    ok = [r for r in results if r.success]
    bad = [r for r in results if not r.success]
    too_small = [r for r in ok if r.path_taken != "html-only" and r.size_bytes < MIN_PDF_BYTES]

    if ok:
        print(" Rendered:")
        for r in ok:
            rel = r.output_path.relative_to(STUDY_ROOT)
            marker = "OK" if r.path_taken != "html-only" else "HTML"
            print(f"   [{marker}] {rel}   {_kb(r.size_bytes):>10}   ({r.duration_s:.2f}s)")
    if too_small:
        print()
        print(" PDFs under 50 KB threshold:")
        for r in too_small:
            print(f"   [SMALL] {r.output_path.name}   {_kb(r.size_bytes)}")
    if bad:
        print()
        print(" Failures:")
        for r in bad:
            print(f"   [FAIL] {r.source_md.name}: {r.error}")

    # Warnings (non-fatal).
    all_warnings = [(r, w) for r in results for w in r.warnings]
    if all_warnings:
        print()
        print(" Warnings:")
        for r, w in all_warnings:
            print(f"   [WARN] {r.source_md.name}: {w}")

    print(sep)
    # Plain-ASCII status line so it renders on Windows cp1252 consoles.
    if not bad and not too_small:
        print(f" [SUCCESS] rendered {len(ok)} PDFs cleanly.")
    else:
        print(f" [PARTIAL] rendered {len(ok)} / {len(results)} sources; "
              f"{len(bad)} failed, {len(too_small)} undersize.")
    print(sep)

    # Exit code: non-zero if anything failed or any PDF is below threshold.
    return 0 if not bad and not too_small else 1


def main() -> int:
    overall_start = time.perf_counter()

    if not STYLESHEET_PATH.is_file():
        log.error("Stylesheet missing: %s — the rendered output will be unstyled.", STYLESHEET_PATH)

    sources = _discover_sources()
    if not sources:
        log.error("No source markdown files found; nothing to render.")
        return 2

    log.info("Discovered %d markdown source(s).", len(sources))

    template = _load_template()
    converter = _build_markdown_converter()
    backend = _select_backend()

    results: list[RenderResult] = []
    for src in sources:
        log.info("Rendering %s ...", src.relative_to(STUDY_ROOT))
        results.append(
            _render_one(src, converter=converter, template=template, backend=backend)
        )

    elapsed = time.perf_counter() - overall_start
    return _print_summary(results, elapsed, backend.name)


if __name__ == "__main__":
    sys.exit(main())
