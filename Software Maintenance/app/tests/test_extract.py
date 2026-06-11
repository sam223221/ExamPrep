"""PDF extraction: page markers, record metadata, normalization, numeric discovery."""

import fitz  # PyMuPDF

from app.extract import discover_pdfs, extract_pdf, normalize_text, page_marker


def test_page_marker_format():
    assert page_marker(14) == "<!-- page:14 -->"


def test_normalize_dehyphenates_and_collapses_whitespace():
    raw = "refac-\ntoring   is    good\n\n\n\nend"
    out = normalize_text(raw)
    assert "refactoring is good" in out
    assert "\n\n\n" not in out  # 3+ newlines collapsed


def test_extract_pdf_record_shape(tmp_path):
    doc = fitz.open()
    for txt in ("Alpha page one", "Bravo page two"):
        doc.new_page().insert_text((72, 72), txt)
    p = tmp_path / "Lecture 4" / "Refactoring1.pdf"
    p.parent.mkdir(parents=True)
    doc.save(str(p))
    doc.close()

    rec = extract_pdf(str(p))
    assert rec["n_pages"] == 2
    assert rec["file"] == "Refactoring1.pdf"
    assert rec["lecture_id"] == "L04"
    assert rec["deck_title"] == "Refactoring"
    assert rec["doc_kind"] == "deck"
    assert "<!-- page:1 -->" in rec["text"]
    assert "<!-- page:2 -->" in rec["text"]
    assert "Alpha page one" in rec["text"]


def test_discover_pdfs_numeric_order(tmp_path):
    # Create lecture folders out of lexical order to prove numeric sort.
    for num in (2, 10, 1):
        d = tmp_path / f"Lecture {num}"
        d.mkdir()
        doc = fitz.open()
        doc.new_page().insert_text((72, 72), f"L{num}")
        doc.save(str(d / "deck.pdf"))
        doc.close()
    found = discover_pdfs(str(tmp_path))
    nums = [int(p.replace("\\", "/").split("/")[-2].split()[-1]) for p in found]
    assert nums == [1, 2, 10]
