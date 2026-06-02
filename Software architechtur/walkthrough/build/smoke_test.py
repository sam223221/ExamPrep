import fitz

doc = fitz.open(r"c:\Users\samgl\Documents\GitHub\ExamPrep\Software architechtur\lecture_2.pdf")
print("Pages:", doc.page_count)
print("Title:", doc.metadata.get("title", "(none)"))
print("First 200 chars of page 1:")
print(repr(doc[0].get_text()[:200]))
img_count = sum(len(doc[p].get_images(full=True)) for p in range(doc.page_count))
print("Total embedded images:", img_count)
doc.close()
