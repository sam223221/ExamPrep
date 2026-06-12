# scripts/

Standalone maintenance/utility scripts for the SB5-MAI exam-prep package.
These are NOT part of the FastAPI app in `app/` — they run directly on the
host with the system Python and are invoked manually.

## Files

| File | Purpose |
|---|---|
| `export_pdfs.py` | Exports all 16 study guides in `data/guides/` to PDF (`notes-pdf/`) for exam-day offline use: one PDF per guide plus the combined `SB5-MAI-complete-notes.pdf` with a two-level bookmark outline (guide → H2 section). |

## export_pdfs.py

### Toolchain (fully local, zero network)

1. **python-markdown** (`extra` + `sane_lists` extensions) renders each guide
   to styled HTML — GFM-style tables, fenced code blocks, bold/italics.
2. **Headless Chromium** (Microsoft Edge preferred, Chrome fallback; located
   at the standard Windows install paths or on PATH) prints the HTML to PDF
   via `--print-to-pdf`. This produces a real, selectable/searchable text
   layer — nothing is rasterized. A throwaway `--user-data-dir` profile in
   `%TEMP%` avoids clashing with a running browser, and
   `--no-pdf-header-footer` suppresses URL/date headers.
3. **PyMuPDF (fitz)** injects bookmark outlines into every per-guide PDF and
   concatenates all 16 into the combined volume (with `garbage=4, deflate`).

### Layout contract

- A4, margins 16/15/18/15 mm (`@page` CSS), no headers/footers.
- Body: Georgia 10.5 pt; headings: Segoe UI; code: Cascadia Mono/Consolas.
- Fenced code blocks use `white-space: pre-wrap` + `overflow-wrap: anywhere`
  so long lines wrap instead of clipping off-page.
- Markdown tables render as real bordered tables (zebra rows, wrap-anywhere
  cells, no row split across pages).
- Headings carry `page-break-inside: avoid` — a heading must never split
  across a page boundary (this also keeps heading detection exact, see below).

### Heading detection (how bookmarks find their pages)

H1 and H2 are given **unique font sizes in the stylesheet** (26 px / 19 px →
19.5 pt / 14.25 pt in print). After conversion the script re-opens the PDF
with fitz and identifies heading spans by exact font size, which yields the
precise target page for every bookmark without fragile text matching. If the
detected H2 count differs from the markdown's H2 count, a WARNING is printed.

### Guide order (deterministic)

`00-overview`, `lecture-01` … `lecture-11` (numeric sort, per
`PM/conventions.md`), then the `9x` series: `90, 91, 92, 93, 94`.
`DOCUMENT.md` and any non-conforming filenames in `data/guides/` are ignored.

### Usage

```
python scripts/export_pdfs.py                  # build all 16 + combined
python scripts/export_pdfs.py --only 91-exam   # rebuild matching guides only
python scripts/export_pdfs.py --skip-existing  # resume an interrupted run
python scripts/export_pdfs.py --merge-only     # rebuild only the combined PDF
```

All paths are derived from the script's own location (project-root-relative);
the script makes no network calls and never modifies `data/guides/`.

### Dependencies

Host Python with `markdown` and `pymupdf` installed, plus a local
Chromium-based browser (Edge ships with Windows 11). No pip installs were
needed on this machine.
