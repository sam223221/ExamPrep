"""Extract text + image catalog for lecture_10.pdf."""
import json
import sys
from pathlib import Path

import fitz

ROOT = Path(r"c:/Users/samgl/Documents/GitHub/ExamPrep/Software architechtur")
SRC = ROOT / "lecture_10.pdf"
OUT_TXT = ROOT / "walkthrough/build/lecture_10_text.txt"
OUT_CATALOG = ROOT / "walkthrough/build/lecture_10_image_catalog.json"

doc = fitz.open(SRC)
print(f"Pages: {doc.page_count}")

lines = []
catalog = []
total_imgs = 0
for pno in range(doc.page_count):
    page = doc[pno]
    lines.append(f"===== PAGE {pno + 1} =====")
    lines.append(page.get_text().strip())
    lines.append("")
    for idx, img in enumerate(page.get_images(full=True), start=1):
        xref = img[0]
        try:
            pix = fitz.Pixmap(doc, xref)
            w, h = pix.width, pix.height
            colorspace = "CMYK" if pix.n - pix.alpha >= 4 else ("RGB" if pix.n - pix.alpha == 3 else "Gray")
            pix = None
        except Exception as e:
            w = h = 0
            colorspace = f"ERR:{e}"
        catalog.append({
            "page": pno + 1,
            "index": idx,
            "xref": xref,
            "width": w,
            "height": h,
            "colorspace": colorspace,
        })
        total_imgs += 1

OUT_TXT.write_text("\n".join(lines), encoding="utf-8")
OUT_CATALOG.write_text(json.dumps(catalog, indent=2), encoding="utf-8")
print(f"Wrote text -> {OUT_TXT}")
print(f"Wrote catalog -> {OUT_CATALOG}")
print(f"Total embedded images: {total_imgs}")
print(f"Text file size: {OUT_TXT.stat().st_size} bytes")

# Count lines
nlines = sum(1 for _ in open(OUT_TXT, encoding='utf-8'))
print(f"Text file lines: {nlines}")

doc.close()
