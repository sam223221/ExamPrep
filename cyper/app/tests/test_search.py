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
