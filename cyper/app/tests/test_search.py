from fastapi.testclient import TestClient
from app import main


def test_search_endpoint_returns_results(monkeypatch):
    def fake_search(q, k=5, where=None):
        return [{"text": "A SYN flood exhausts the TCP backlog.",
                 "file": "L06_DoS.pdf", "page": 14, "topic": "Denial of Service",
                 "type": "source", "title": "Denial of Service", "score": 0.91}]
    monkeypatch.setattr(main, "search", fake_search)
    client = TestClient(main.app)
    r = client.get("/search", params={"q": "syn flood"})
    assert r.status_code == 200
    body = r.json()
    assert body["results"][0]["page"] == 14
    assert "SYN flood" in body["results"][0]["text"]


def test_build_where_filters():
    from app.main import build_where
    assert build_where(None, None) is None
    assert build_where("qna", None) == {"type": "qna"}
    assert build_where("source", None) == {"type": "source"}
    # difficulty implies qna, and combines via $and
    assert build_where(None, "hard") == {"$and": [{"type": "qna"}, {"difficulty": "hard"}]}
    assert build_where("qna", "easy") == {"$and": [{"type": "qna"}, {"difficulty": "easy"}]}


def test_slug_sanitizes():
    from app.main import _slug
    assert _slug("L08_Threat Modeling 1.pdf") == "L08_Threat_Modeling_1"
    s = _slug("a/b\\c.pdf")
    assert "/" not in s and "\\" not in s


def test_slide_rejects_unknown_file(monkeypatch):
    from app import main
    monkeypatch.setattr(main, "_pdf_map", {"known.pdf": "/x/known.pdf"})
    client = TestClient(main.app)
    # path traversal collapses to basename "passwd", not in the map -> 404
    r = client.get("/slide", params={"file": "../../etc/passwd", "page": 1})
    assert r.status_code == 404


def test_slide_renders_known_pdf(tmp_path, monkeypatch):
    import fitz
    from app import main
    doc = fitz.open()
    doc.new_page().insert_text((72, 72), "Slide content")
    pdf = tmp_path / "deck.pdf"
    doc.save(pdf)
    doc.close()
    monkeypatch.setattr(main, "_pdf_map", {"deck.pdf": str(pdf)})
    monkeypatch.setattr(main, "SLIDES_DIR", str(tmp_path / "cache"))
    client = TestClient(main.app)
    r = client.get("/slide", params={"file": "deck.pdf", "page": 1})
    assert r.status_code == 200
    assert r.headers["content-type"] == "image/png"
    assert r.content[:8] == b"\x89PNG\r\n\x1a\n"  # PNG magic bytes
    # out-of-range page -> 404
    assert client.get("/slide", params={"file": "deck.pdf", "page": 99}).status_code == 404
