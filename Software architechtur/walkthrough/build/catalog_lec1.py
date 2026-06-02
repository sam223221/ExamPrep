import fitz
import json
from pathlib import Path

src = Path(r"c:\Users\samgl\Documents\GitHub\ExamPrep\Software architechtur\lecture_1.pdf")
out_json = Path(r"c:\Users\samgl\Documents\GitHub\ExamPrep\Software architechtur\walkthrough\build\lecture_1_image_catalog.json")

doc = fitz.open(src)
catalog = []
total = 0
diagrams = 0
deco = 0
for pno in range(doc.page_count):
    page = doc[pno]
    text = page.get_text()
    snippet = " ".join(text.split())[:60]
    for idx, img in enumerate(page.get_images(full=True), start=1):
        xref = img[0]
        try:
            info = doc.extract_image(xref)
            w = info.get("width", 0)
            h = info.get("height", 0)
            size = len(info.get("image", b""))
            ext = info.get("ext", "png")
        except Exception as e:
            w = h = size = 0
            ext = "?"
        is_diagram = (w >= 150 and h >= 150 and size >= 5000)
        if is_diagram:
            diagrams += 1
        else:
            deco += 1
        total += 1
        catalog.append({
            "page": pno + 1,
            "index": idx,
            "xref": xref,
            "width": w,
            "height": h,
            "bytes": size,
            "ext": ext,
            "likely_diagram": is_diagram,
            "snippet": snippet,
        })

out_json.write_text(json.dumps(catalog, indent=2), encoding="utf-8")
print(f"Total images: {total}")
print(f"Likely diagrams (>=150x150 & >=5KB): {diagrams}")
print(f"Likely decorative: {deco}")
doc.close()
