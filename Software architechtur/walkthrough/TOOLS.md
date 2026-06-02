# Toolchain for the Exam-Prep Walkthrough

This document is the single source of truth for which tools to use when extracting source PDFs and assembling the final study guide. All future agents should consult this before writing extraction or build scripts.

## Environment

- **OS:** Windows 11 (PowerShell). Working dir: `c:\Users\samgl\Documents\GitHub\ExamPrep\Software architechtur\` (note the typo `architechtur` — preserve it, do not rename).
- **Python interpreter to use:** `python` (resolves to Python 3.14.0). The launcher `py` also works and points to the same install. `python3` is available too (3.13.13) but stick to `python` for consistency.

## Installed Python packages (verified)

| Package | Version | Use |
|---|---|---|
| PyMuPDF (`import fitz`) | 1.27.2.2 | PDF text + image extraction (primary) |
| Pillow (`PIL`) | 12.1.0 | Image post-processing |
| reportlab | 4.4.10 | Final PDF assembly (primary path) |
| markdown | 3.10.2 | Markdown -> HTML for the build step |

## Missing (do NOT install without user approval)

- pdfplumber, pypdf, pdf2image, weasyprint, markdown-pdf — none required; PyMuPDF handles everything we need.
- System tools: pandoc, wkhtmltopdf, pdftoppm, pdfimages — all absent.
- LaTeX (pdflatex, xelatex) — absent. Do not rely on a pandoc+LaTeX pipeline.

## Recommended pipeline

1. **Text + image extraction:** PyMuPDF (`fitz`). It is the lightest reliable option and is already installed. Do not import `pdfplumber` or `pypdf`.
2. **Per-lecture notes:** write Markdown into `walkthrough/analysis/lecture_N.md`. Save extracted images under `walkthrough/images/lecture_N/`.
3. **Topic chapters:** consolidate notes into Markdown chapters under `walkthrough/chapters/`.
4. **Final PDF assembly:** convert Markdown -> HTML with the `markdown` package, then render to PDF with `reportlab` (or, simpler, build the PDF directly with `reportlab.platypus` from structured chapter content). Avoid weasyprint/pandoc/LaTeX paths — none of those are installed.

## Smoke test result (lecture_2.pdf, 1.27 MB)

- 76 pages, title `Software Architecture (T630019402) 10pt Lecture #2, February 17, 2026`, 2 embedded images. Text extraction is clean. Script lives at `walkthrough/build/smoke_test.py`.

## Copy-paste template: extract one PDF

```python
# Usage: python extract_one.py <source.pdf> <out_dir>
# Writes <out_dir>/text.md and <out_dir>/images/page<N>_img<K>.<ext>

import sys, os, fitz
from pathlib import Path

src = Path(sys.argv[1])
out = Path(sys.argv[2])
img_dir = out / "images"
img_dir.mkdir(parents=True, exist_ok=True)

doc = fitz.open(src)
md_lines = [f"# {src.stem}", "", f"_Pages: {doc.page_count}_", ""]

for pno in range(doc.page_count):
    page = doc[pno]
    md_lines.append(f"## Page {pno + 1}")
    md_lines.append("")
    md_lines.append(page.get_text().strip())
    md_lines.append("")

    for idx, img in enumerate(page.get_images(full=True), start=1):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        ext = "png"
        if pix.n - pix.alpha >= 4:  # CMYK -> convert to RGB
            pix = fitz.Pixmap(fitz.csRGB, pix)
        fname = f"page{pno + 1:03d}_img{idx}.{ext}"
        pix.save(img_dir / fname)
        pix = None
        md_lines.append(f"![{fname}](images/{fname})")
        md_lines.append("")

doc.close()
(out / "text.md").write_text("\n".join(md_lines), encoding="utf-8")
print(f"Wrote {out / 'text.md'} and images to {img_dir}")
```

## Copy-paste template: assemble final PDF (reportlab)

```python
# Build a PDF from chapter Markdown files using reportlab's SimpleDocTemplate.
# Markdown is converted to a stripped-down HTML subset that reportlab's Paragraph
# understands (<b>, <i>, <br/>, <para>). For richer rendering, pre-render code
# blocks and tables manually.

import markdown
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak

chapters_dir = Path("walkthrough/chapters")
out_pdf = Path("walkthrough/build/study_guide.pdf")
styles = getSampleStyleSheet()
story = []

for md_path in sorted(chapters_dir.glob("*.md")):
    html = markdown.markdown(md_path.read_text(encoding="utf-8"))
    # naive: one Paragraph per top-level block; refine per chapter as needed
    for block in html.split("\n\n"):
        story.append(Paragraph(block, styles["BodyText"]))
        story.append(Spacer(1, 6))
    story.append(PageBreak())

SimpleDocTemplate(str(out_pdf), pagesize=A4).build(story)
```

## House rules for extraction agents

- Never read a lecture PDF end-to-end in one go via the Read tool — they are too large. Always extract via the script above.
- Save extracted text as UTF-8 Markdown.
- Image filenames must be zero-padded by page (`page003_img1.png`) so they sort naturally.
- If an embedded image is CMYK, convert to RGB before saving (the template handles this).
- Keep `walkthrough/build/` for throwaway artifacts; commit only the final assembled PDF if requested.
