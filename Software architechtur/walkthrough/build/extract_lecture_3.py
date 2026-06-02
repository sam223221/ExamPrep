"""Extract text + catalog images for lecture_3.pdf."""
import fitz, json, sys
from pathlib import Path

src = Path(r"c:\Users\samgl\Documents\GitHub\ExamPrep\Software architechtur\lecture_3.pdf")
build = Path(r"c:\Users\samgl\Documents\GitHub\ExamPrep\Software architechtur\walkthrough\build")
build.mkdir(parents=True, exist_ok=True)

text_path = build / "lecture_3_text.txt"
catalog_path = build / "lecture_3_image_catalog.json"

doc = fitz.open(src)
lines = []
catalog = []

likely_diagram = 0
likely_decorative = 0
total_images = 0

for pno in range(doc.page_count):
    page = doc[pno]
    lines.append(f"===== PAGE {pno + 1} =====")
    page_text = page.get_text().strip()
    lines.append(page_text)
    lines.append("")

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
            w, h, n_bytes = 0, 0, 0

        # crude classification
        area = w * h
        classification = "decorative"
        if area >= 80000 and min(w, h) >= 200:
            classification = "likely_diagram"
            likely_diagram += 1
        else:
            likely_decorative += 1
        total_images += 1

        snippet = page_text[:160].replace("\n", " ")
        catalog.append({
            "page": pno + 1,
            "index": idx,
            "xref": xref,
            "width": w,
            "height": h,
            "bytes": n_bytes,
            "classification": classification,
            "snippet": snippet,
        })

doc.close()

text_path.write_text("\n".join(lines), encoding="utf-8")
catalog_path.write_text(json.dumps(catalog, indent=2), encoding="utf-8")

print(f"Pages: {len(lines and [l for l in lines if l.startswith('===== PAGE')])}")
print(f"Total images: {total_images}")
print(f"Likely diagrams: {likely_diagram}")
print(f"Likely decorative: {likely_decorative}")
print(f"Text bytes: {text_path.stat().st_size}")
print(f"Catalog bytes: {catalog_path.stat().st_size}")
