# `study/` — AI Exam Prep Study Package

Root of the self-contained AI exam preparation package described in the spec at `docs/superpowers/specs/2026-05-22-ai-exam-prep-study-package-design.md` and built per the plan at `docs/superpowers/plans/2026-05-22-ai-exam-prep-study-package.md`.

## Layout

| Path | Purpose |
|---|---|
| `00-master-index.md` | Top-level study index (orientation, study order, full TOC, analogies index, glossary flattened, cross-reference graph, lab table, pitfalls compendium). |
| `00-master-index.pdf` | Print-ready rendering of the master index (produced by `render.py`). |
| `lectures/` | Ten lecture chapters in Markdown plus their rendered PDFs. See `lectures/DOCUMENT.md`. |
| `_shared/` | Cross-lecture resources (glossary, cross-reference map, HTML template + stylesheet for the renderer, toolchain notes). |
| `_exam/` | Variant prompts per lab (used by the Exam Agents). |
| `_review/` | Reviewer round outputs (one folder per artifact, per round). |
| `extracted_figures/` | Figures pulled out of the source lecture PDFs, one folder per lecture, with a `figures.md` catalogue per folder. |
| `requirements.txt` | Pinned Python dependencies for the entire package (renderer, figure extraction, notebook execution). |
| `render.py` | Markdown -> PDF renderer (see below). |

## `render.py` — the PDF renderer

Implements spec §10. Run via:

```powershell
py -3.12 study/render.py
```

The script:

1. Discovers every Markdown source: `study/00-master-index.md` and every `study/lectures/*.md` (excluding `DOCUMENT.md`).
2. Converts each Markdown to HTML with the pinned `markdown` extensions (`tables`, `fenced_code`, `footnotes`, `attr_list`, `def_list`, `codehilite`, `markdown_katex` for server-side KaTeX math rendering, and `toc` configured with `pymdownx.slugs.slugify(case="lower")` so heading IDs match GitHub's double-hyphen GFM slug rules — the master index links rely on this).
3. Wraps the body in `_shared/html-template.html`, substituting `{{ title }}` (first H1) and `{{ body }}`.
4. Renders the HTML to a PDF beside the source via the primary backend, WeasyPrint. The script prepends the MSYS2 GTK runtime directory (`C:\msys64\mingw64\bin`) to `PATH` before importing `weasyprint` — required on Windows; see `_shared/TOOLCHAIN.md`.

### Fallback chain (per spec §10)

If WeasyPrint cannot initialise (GTK runtime missing, library import error), `render.py` falls back to **pdfkit + wkhtmltopdf**. If that also fails, it emits styled `.html` files beside each `.md` (the verifier's PDF-presence check will flag this as a regression — visibility is the point). The selected backend is printed in the run summary.

### Idempotency

`render.py` is idempotent. Running it twice produces byte-equivalent PDFs (within the inherent variability of the font subsetter, but the on-page result is identical). It never deletes or rewrites a `.md` file, and it touches nothing outside `study/lectures/` and `study/` (the master index location).

### Logging

`fontTools` and `weasyprint` module loggers are set to `WARNING` to keep the per-glyph subsetter chatter out of the run summary.

## Recent changes

- **2026-05-23 (Phase 3.2):** Created `render.py` and `study/DOCUMENT.md`. Produced 11 PDFs (master index + 10 lectures), all >50 KB, total wall-clock ~53 s.
- **2026-05-23 (Phase 3.3 targeted fix):** Enabled the `toc` extension in `render.py` with `pymdownx.slugs.slugify(case="lower")` so heading IDs follow GFM double-hyphen conventions. Master-index anchors like `#1-overview--motivation` now resolve cleanly in every rendered PDF. Re-ran the renderer; `00-master-index.pdf` rebuilt at 384 KB.
