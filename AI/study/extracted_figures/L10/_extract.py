"""Extract text and embedded figures from the L10 Introduction to ML lecture PDF."""

import os
import sys
import fitz  # PyMuPDF


PDF_PATH = r"c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture10-Introduction to Machine Learning.pdf"
OUT_DIR = r"c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\extracted_figures\L10"
TEXT_DUMP = os.path.join(OUT_DIR, "_text_dump.txt")


def main():
    doc = fitz.open(PDF_PATH)
    print(f"PDF page count: {doc.page_count}")

    text_blocks = []
    figure_count = 0
    catalogue = []

    for pno in range(doc.page_count):
        page = doc.load_page(pno)
        page_label = f"=== Page {pno + 1} (PDF index {pno}) ==="
        text_blocks.append(page_label)
        text_blocks.append(page.get_text("text"))
        text_blocks.append("")

        # Enumerate embedded images on this page.
        images = page.get_images(full=True)
        for img_idx, img in enumerate(images):
            xref = img[0]
            try:
                pix = fitz.Pixmap(doc, xref)
                figure_count += 1
                slug = f"fig{figure_count:02d}-page{pno + 1:02d}-img{img_idx + 1}"
                target = os.path.join(OUT_DIR, slug + ".png")
                if pix.n - pix.alpha >= 4:  # CMYK or other -> convert to RGB
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                pix.save(target)
                catalogue.append((figure_count, pno + 1, img_idx + 1, target))
                pix = None
            except Exception as exc:
                print(f"  ! failed to extract image xref={xref} on page {pno + 1}: {exc}")

    with open(TEXT_DUMP, "w", encoding="utf-8") as fh:
        fh.write("\n".join(text_blocks))

    print(f"Wrote text dump: {TEXT_DUMP}")
    print(f"Extracted {figure_count} embedded images.")
    for row in catalogue:
        print(f"  fig{row[0]:02d} page={row[1]} idx={row[2]} -> {row[3]}")

    # Also render every page as a PNG so we have a fallback for slides with
    # composite visuals that don't extract as embedded images.
    for pno in range(doc.page_count):
        page = doc.load_page(pno)
        pix = page.get_pixmap(dpi=160)
        target = os.path.join(OUT_DIR, f"page{pno + 1:02d}-render.png")
        pix.save(target)


if __name__ == "__main__":
    main()
