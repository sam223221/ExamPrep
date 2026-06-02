"""Extract text and image catalog from lecture_8.pdf."""
import json
from pathlib import Path
import fitz

ROOT = Path(r"c:\Users\samgl\Documents\GitHub\ExamPrep\Software architechtur")
SRC = ROOT / "lecture_8.pdf"
TEXT_OUT = ROOT / "walkthrough" / "build" / "lecture_8_text.txt"
CATALOG_OUT = ROOT / "walkthrough" / "build" / "lecture_8_image_catalog.json"

doc = fitz.open(SRC)
text_chunks = []
catalog = []

for pno in range(doc.page_count):
    page = doc[pno]
    text = page.get_text()
    text_chunks.append(f"===== PAGE {pno+1} =====\n{text}")
    for idx, img in enumerate(page.get_images(full=True), start=1):
        xref = img[0]
        try:
            pix = fitz.Pixmap(doc, xref)
            if pix.n - pix.alpha >= 4:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            w, h = pix.width, pix.height
            n_bytes = len(pix.tobytes("png"))
            pix = None
        except Exception as e:
            w = h = n_bytes = -1
        snippet = text.strip().replace("\n", " ")[:160]
        catalog.append({
            "page": pno+1,
            "index": idx,
            "xref": xref,
            "w": w,
            "h": h,
            "bytes": n_bytes,
            "snippet": snippet,
        })

TEXT_OUT.write_text("\n".join(text_chunks), encoding="utf-8")
CATALOG_OUT.write_text(json.dumps(catalog, indent=2), encoding="utf-8")

# Stats
total_chars = sum(len(t) for t in text_chunks)
print(f"Pages: {doc.page_count}")
print(f"Total text chars: {total_chars}")
print(f"Total embedded images: {len(catalog)}")
# Image size histogram
by_page = {}
for c in catalog:
    by_page.setdefault(c["page"], 0)
    by_page[c["page"]] += 1
print(f"Pages with embedded images: {len(by_page)}")
print(f"Text -> {TEXT_OUT}")
print(f"Catalog -> {CATALOG_OUT}")
doc.close()
