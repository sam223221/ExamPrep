"""Extract text + image catalog from lecture_9.pdf."""
import json
from pathlib import Path
import fitz

ROOT = Path(r"c:/Users/samgl/Documents/GitHub/ExamPrep/Software architechtur")
SRC = ROOT / "lecture_9.pdf"
BUILD = ROOT / "walkthrough" / "build"
TXT_OUT = BUILD / "lecture_9_text.txt"
CAT_OUT = BUILD / "lecture_9_image_catalog.json"

doc = fitz.open(SRC)
lines = []
catalog = []
total_chars = 0

for pno in range(doc.page_count):
    page = doc[pno]
    text = page.get_text()
    total_chars += len(text)
    lines.append(f"===== PAGE {pno + 1} =====")
    lines.append(text.rstrip())
    lines.append("")
    for idx, img in enumerate(page.get_images(full=True), start=1):
        xref = img[0]
        try:
            base = doc.extract_image(xref)
            catalog.append({
                "page": pno + 1,
                "index": idx,
                "xref": xref,
                "ext": base.get("ext"),
                "width": base.get("width"),
                "height": base.get("height"),
                "colorspace": base.get("colorspace"),
                "size_bytes": len(base.get("image", b"")),
            })
        except Exception as e:
            catalog.append({"page": pno + 1, "index": idx, "xref": xref, "error": str(e)})

TXT_OUT.write_text("\n".join(lines), encoding="utf-8")
CAT_OUT.write_text(json.dumps(catalog, indent=2), encoding="utf-8")

print(f"Pages: {doc.page_count}")
print(f"Total chars: {total_chars}")
print(f"Text file: {TXT_OUT}")
print(f"Embedded images: {len(catalog)}")

# Quick distribution of embedded image sizes
small = sum(1 for c in catalog if c.get("width", 0) * c.get("height", 0) < 10000)
medium = sum(1 for c in catalog if 10000 <= c.get("width", 0) * c.get("height", 0) < 200000)
large = sum(1 for c in catalog if c.get("width", 0) * c.get("height", 0) >= 200000)
print(f"Small (<10k px): {small}")
print(f"Medium (10k-200k px): {medium}")
print(f"Large (>=200k px): {large}")
doc.close()
