"""Extract lecture_5.pdf text per page and catalog images.

Outputs:
- walkthrough/build/lecture_5_text.txt with ===== PAGE N ===== markers
- walkthrough/build/lecture_5_image_catalog.json
"""
import json
import fitz
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "lecture_5.pdf"
TXT_OUT = ROOT / "walkthrough" / "build" / "lecture_5_text.txt"
CATALOG_OUT = ROOT / "walkthrough" / "build" / "lecture_5_image_catalog.json"

doc = fitz.open(PDF)
n_pages = doc.page_count

text_chunks = []
catalog = []
total_images = 0

for pno in range(n_pages):
    page = doc[pno]
    text = page.get_text()
    text_chunks.append(f"===== PAGE {pno + 1} =====\n{text}")

    snippet = " ".join(text.split())[:120]
    for idx, img in enumerate(page.get_images(full=True), start=1):
        xref = img[0]
        try:
            pix = fitz.Pixmap(doc, xref)
            w, h = pix.width, pix.height
            n_bytes = len(pix.tobytes("png"))
            pix = None
        except Exception as e:
            w = h = n_bytes = -1
        catalog.append({
            "page": pno + 1,
            "index": idx,
            "xref": xref,
            "w": w,
            "h": h,
            "bytes": n_bytes,
            "page_snippet": snippet,
        })
        total_images += 1

TXT_OUT.write_text("\n".join(text_chunks), encoding="utf-8")
CATALOG_OUT.write_text(json.dumps(catalog, indent=2), encoding="utf-8")

print(f"pages={n_pages}")
print(f"images={total_images}")
print(f"text_chars={sum(len(c) for c in text_chunks)}")
print(f"text_path={TXT_OUT}")
print(f"catalog_path={CATALOG_OUT}")
doc.close()
