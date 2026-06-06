import fitz  # PyMuPDF
from app.extract import extract_pdf, page_marker


def test_page_marker_format():
    assert page_marker(14) == "<!-- page:14 -->"


def test_extract_pdf_returns_pages(tmp_path):
    doc = fitz.open()
    for txt in ("Alpha page one", "Bravo page two"):
        pg = doc.new_page()
        pg.insert_text((72, 72), txt)
    p = tmp_path / "sample.pdf"
    doc.save(p)
    doc.close()

    rec = extract_pdf(str(p))
    assert rec["n_pages"] == 2
    assert "Alpha page one" in rec["text"]
    assert "<!-- page:1 -->" in rec["text"]
    assert "<!-- page:2 -->" in rec["text"]
