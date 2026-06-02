"""Extract text and catalog images for lecture_4.pdf."""
import json, sys
from pathlib import Path
import fitz

ROOT = Path(r"c:/Users/samgl/Documents/GitHub/ExamPrep/Software architechtur")
SRC = ROOT / "lecture_4.pdf"
BUILD = ROOT / "walkthrough" / "build"
TXT = BUILD / "lecture_4_text.txt"
CAT = BUILD / "lecture_4_image_catalog.json"

doc = fitz.open(SRC)
text_chunks = []
catalog = []

for pno in range(doc.page_count):
    page = doc[pno]
    text = page.get_text().strip()
    text_chunks.append(f"===== PAGE {pno + 1} =====\n{text}\n")

    for idx, img in enumerate(page.get_images(full=True), start=1):
        xref = img[0]
        try:
            pix = fitz.Pixmap(doc, xref)
            w, h = pix.width, pix.height
            n = pix.n
            cs_n = pix.n - pix.alpha
            data_len = len(pix.tobytes("png"))
            pix = None
        except Exception as e:
            w = h = n = data_len = -1
            cs_n = -1

        snippet = text[:160].replace("\n", " ") if text else ""
        catalog.append({
            "page": pno + 1,
            "index": idx,
            "xref": xref,
            "width": w,
            "height": h,
            "channels": n,
            "cs_channels": cs_n,
            "png_bytes": data_len,
            "page_text_snippet": snippet,
        })

TXT.write_text("\n".join(text_chunks), encoding="utf-8")
CAT.write_text(json.dumps(catalog, indent=2), encoding="utf-8")

print(f"pages={doc.page_count}")
print(f"text_chars={sum(len(c) for c in text_chunks)}")
print(f"images_total={len(catalog)}")
# Image stats: distinct sizes, largest few
sizes = sorted({(c['width'], c['height']) for c in catalog})
print(f"distinct_sizes={len(sizes)}")
big = sorted(catalog, key=lambda c: c['png_bytes'], reverse=True)[:10]
for b in big:
    print(f"p{b['page']:>3} img{b['index']} {b['width']}x{b['height']} {b['png_bytes']}B")

doc.close()
