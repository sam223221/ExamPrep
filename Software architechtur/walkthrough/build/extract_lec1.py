import fitz
from pathlib import Path

src = Path(r"c:\Users\samgl\Documents\GitHub\ExamPrep\Software architechtur\lecture_1.pdf")
out_txt = Path(r"c:\Users\samgl\Documents\GitHub\ExamPrep\Software architechtur\walkthrough\build\lecture_1_text.txt")

doc = fitz.open(src)
lines = []
total_chars = 0
for pno in range(doc.page_count):
    page = doc[pno]
    text = page.get_text()
    total_chars += len(text)
    lines.append(f"===== PAGE {pno + 1} =====")
    lines.append(text)
    lines.append("")

out_txt.write_text("\n".join(lines), encoding="utf-8")
print(f"Pages: {doc.page_count}")
print(f"Total chars: {total_chars}")
doc.close()
