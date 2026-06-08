# study-guide/

Source Markdown for the Cybersecurity F26 study guide, plus a self-contained
build script that compiles every Markdown file into one navigable PDF.

## Contents

| Path | What it is |
|------|------------|
| `00-overview.md` | Course overview & map (no commands/qna counterpart) |
| `01-*.md` … `12-*.md` | The 12 top-level chapter notes |
| `exam-prep.md` | Exam prep & revision (no commands/qna counterpart) |
| `commands/01-*.md` … `commands/12-*.md` | Per-chapter command & code reference |
| `qna/01-*.md` … `qna/12-*.md` | Per-chapter simulated open-book Q&A |
| `build_pdf.py` | Build script: Markdown → one combined PDF (see below) |
| `Cyber-Security-Study-Guide.pdf` | Generated output (build artifact) |

The `.md` files are clean GitHub-flavored Markdown: one `# H1` title per file,
pipe tables, fenced code blocks; no LaTeX, images, raw HTML, or front matter.

## build_pdf.py

Compiles the 38 source Markdown files into a single, paginated, bookmarked PDF.

### What it does

1. **Resolves the file order** by numeric `NN-` prefix (not brittle hardcoded
   names) and prints the resolved order for verification. Order is:
   1. `00-overview.md`
   2. for each chapter N = 01..12: `NN-*.md` (main), then `commands/NN-*.md`,
      then `qna/NN-*.md`
   3. `exam-prep.md` last
   If a numeric prefix is missing or ambiguous in any folder, the build aborts
   with a clear error rather than producing a silently-wrong document.
2. **Renders each file** Markdown → HTML with the Python-Markdown extensions
   `tables`, `fenced_code`, `codehilite`, `toc`, `sane_lists`. Before rendering,
   a small in-memory normalisation step (`fix_table_spacing`) inserts the blank
   line that the `tables` extension requires in front of any GFM pipe table that
   was authored glued directly to the paragraph above it. This hardens the build
   against a source quirk (e.g. an answer line `A.` immediately followed by a
   `| ... |` table header) without ever editing the source `.md` files. The step
   is conservative and idempotent: it only fires when a `|` line is followed by a
   `|---|---|`-style delimiter row and preceded by a non-blank, non-table line,
   and it skips anything inside ``` fenced code blocks ```.
3. **Composes one PDF** with PyMuPDF's Story API (`fitz.Story` +
   `fitz.DocumentWriter`), which handles automatic pagination. Custom
   `user_css` gives bordered/padded tables, monospace code blocks that
   **wrap** long command lines (`white-space: pre-wrap; word-wrap: break-word`)
   instead of clipping them, and styled headings/body (~10.5pt).
4. **Starts each source file on a fresh page** (one Story per file).
5. **Adds a PDF outline/bookmarks**: one top-level bookmark per source file,
   named after that file's `# H1` title — so all 38 sections are navigable. The
   H1 search strips ``` fenced code blocks ``` first, so a `#` shell comment in a
   code block can never be mistaken for the title.
6. **Prepends a title page** (page 1) with the document title and an embedded
   table of contents listing every section.

### How to run

```bash
python build_pdf.py
```

Run it from this directory (or any directory — it locates its sources relative
to its own file path). It prints the resolved file order, the final page count,
the bookmark count, and a title→page map.

### Output

`study-guide/Cyber-Security-Study-Guide.pdf`
(~357 pages, 38 bookmarks, ~2.4 MB — exact page count varies if sources change.)

### Dependencies (zero-install)

Relies only on libraries already present in the global Python 3.14 install — it
does **not** create a virtualenv and does **not** touch `app/requirements.txt`
or the FastAPI application:

- **`markdown`** (Python-Markdown 3.x) — Markdown → HTML; the listed extensions
  ship with the package, no extras needed.
- **`PyMuPDF`** (import name `fitz`, 1.27.x) — provides `Story` +
  `DocumentWriter` for HTML/CSS → PDF, plus outline (`set_toc`) and metadata.

`pandoc`, `wkhtmltopdf`, and `weasyprint` are **not** required and are not used.

### Notes / gotchas

- On this PyMuPDF version, `DocumentWriter` must target a path or a writable
  stream, **not** a `Document` object. The script renders into an in-memory
  `io.BytesIO` buffer and reopens it — this is intentional, not a workaround to
  "fix later."
- Pipe characters that remain in the PDF are inside fenced code blocks (shell
  pipelines and ASCII-art diagrams, e.g. the threat-modeling DFD legends, and
  the firewalls "Example ACL table (lecture format)" reproduced verbatim in a
  ` ```text ` block). They are *meant* to stay literal; only GitHub pipe
  **tables** are converted to bordered tables.
- A GFM table authored *glued* to the paragraph above it (no blank line between)
  is repaired at build time by `fix_table_spacing` (see step 2), so it still
  renders as a bordered table rather than literal `| ... |` pipe text. The fix
  lives in the build, not in the sources — the `.md` files are never edited.
- The script never modifies the source `.md` files.
- The output PDF is a build artifact; regenerate it any time the sources change
  by re-running `python build_pdf.py`.
