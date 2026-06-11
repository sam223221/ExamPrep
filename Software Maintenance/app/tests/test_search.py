"""API: /search where-builder + params, /slide traversal/render, /health, quiz routes."""

import json

from fastapi.testclient import TestClient

from app import main

# --- where builder ----------------------------------------------------------


def test_build_where_filters():
    from app.main import build_where

    assert build_where(None, None) is None
    assert build_where("all", None) is None
    assert build_where("L04", None) == {"lecture_id": "L04"}
    assert build_where(None, "Refactoring") == {"topic": "Refactoring"}
    assert build_where("L04", "Refactoring") == {
        "$and": [{"lecture_id": "L04"}, {"topic": "Refactoring"}]
    }


# --- /search ----------------------------------------------------------------


def test_search_endpoint_returns_results(monkeypatch):
    def fake_search(q, k, where):
        return [
            {
                "text": "Extract Method names a block.",
                "lecture_id": "L04",
                "topic": "Refactoring",
                "title": "Key Concepts",
                "source_pdf": "",
                "page": 0,
                "score": 0.91,
                "html": "<p>x</p>",
                "img": None,
            }
        ]

    monkeypatch.setattr(main, "search", fake_search)
    client = TestClient(main.app)
    r = client.get("/search", params={"q": "extract method", "lecture": "L04"})
    assert r.status_code == 200
    body = r.json()
    assert body["results"][0]["topic"] == "Refactoring"


def test_search_rejects_bad_lecture(monkeypatch):
    monkeypatch.setattr(main, "search", lambda *a, **k: [])
    client = TestClient(main.app)
    assert client.get("/search", params={"q": "x", "lecture": "L4"}).status_code == 422


def test_search_rejects_out_of_vocab_topic(monkeypatch):
    monkeypatch.setattr(main, "search", lambda *a, **k: [])
    client = TestClient(main.app)
    assert client.get("/search", params={"q": "x", "topic": "Nope"}).status_code == 422


def test_search_rejects_short_query():
    client = TestClient(main.app)
    assert client.get("/search", params={"q": "a"}).status_code == 422


# --- /search over-fetch (P1 ANN-recall fix, 2026-06-10) ----------------------


class _FakeEmbedder:
    def embed_query(self, q):
        return [0.0, 0.0]


class _FakeCollection:
    """Stands in for the Chroma collection; records the n_results actually requested."""

    def __init__(self, distances):
        self._distances = distances
        self.requested_n = None

    def query(self, **kwargs):
        self.requested_n = kwargs["n_results"]
        n = min(kwargs["n_results"], len(self._distances))
        return {
            "documents": [[f"doc {i}" for i in range(n)]],
            "metadatas": [
                [
                    {"lecture_id": "L03", "title": f"t{i}", "source_pdf": "", "page": 0}
                    for i in range(n)
                ]
            ],
            "distances": [self._distances[:n]],
        }


def test_search_overfetches_then_slices_to_k(monkeypatch):
    # HNSW recall at small n_results deterministically missed higher-similarity
    # chunks on the grown collection (App Tester P1). search() must therefore
    # ask Chroma for max(OVERFETCH_MIN, OVERFETCH_FACTOR*k) candidates, re-sort
    # by distance, and return exactly k — the API contract is unchanged.
    distances = [0.40, 0.10, 0.30, 0.20] + [0.50 + i / 100 for i in range(40)]
    col = _FakeCollection(distances)
    monkeypatch.setattr(main, "_lazy", lambda: (_FakeEmbedder(), col))
    out = main.search("ci pipeline structure", 6, None)
    assert col.requested_n == 24  # max(24, 4*6) — over-fetched, not the raw k=6
    assert len(out) == 6  # sliced back to the requested k
    scores = [r["score"] for r in out]
    assert scores == sorted(scores, reverse=True)  # best-first after the re-sort
    assert out[0]["score"] == 0.9  # 1 - 0.10: the true best candidate leads


def test_search_overfetch_scales_with_k_and_caps_at_available(monkeypatch):
    col = _FakeCollection([i / 100 for i in range(100)])
    monkeypatch.setattr(main, "_lazy", lambda: (_FakeEmbedder(), col))
    out = main.search("ci pipeline structure", 20, None)
    assert col.requested_n == 80  # max(24, 4*20)
    assert len(out) == 20

    # Fewer candidates than k (e.g. a narrow `where` filter) still returns them all.
    small = _FakeCollection([0.1, 0.2, 0.3])
    monkeypatch.setattr(main, "_lazy", lambda: (_FakeEmbedder(), small))
    assert len(main.search("ci pipeline structure", 6, None)) == 3


def test_ingest_collection_raises_hnsw_search_ef():
    # The other half of the P1 recall fix: the collection itself is built with a
    # query-time exploration breadth (hnsw:search_ef) far above chromadb 0.5.x's
    # default of 10 — at the default, HNSW missed near neighbours on the ~2k-chunk
    # collection regardless of over-fetching.
    from app.ingest import COLLECTION_METADATA

    assert COLLECTION_METADATA["hnsw:space"] == "cosine"
    assert COLLECTION_METADATA["hnsw:search_ef"] >= 100


# --- /health ----------------------------------------------------------------


def test_health():
    client = TestClient(main.app)
    r = client.get("/health")
    assert r.status_code == 200 and r.json() == {"status": "ok"}


# --- /slide -----------------------------------------------------------------


def test_slug_sanitizes():
    from app.main import _slug

    assert _slug("OOPrinciples.pdf") == "OOPrinciples"
    s = _slug("a/b\\c.pdf")
    assert "/" not in s and "\\" not in s


def test_slide_rejects_unknown_and_traversal(monkeypatch):
    monkeypatch.setattr(main, "_pdf_map", {"known.pdf": "/x/known.pdf"})
    client = TestClient(main.app)
    # traversal collapses to basename "passwd", not in the map -> 404
    r = client.get("/slide", params={"file": "../../etc/passwd", "page": 1})
    assert r.status_code == 404


def test_slide_renders_known_pdf(tmp_path, monkeypatch):
    import fitz

    doc = fitz.open()
    doc.new_page().insert_text((72, 72), "Slide content")
    pdf = tmp_path / "deck.pdf"
    doc.save(str(pdf))
    doc.close()
    monkeypatch.setattr(main, "_pdf_map", {"deck.pdf": str(pdf)})
    monkeypatch.setattr(main, "SLIDES_DIR", str(tmp_path / "cache"))
    client = TestClient(main.app)
    r = client.get("/slide", params={"file": "deck.pdf", "page": 1})
    assert r.status_code == 200
    assert r.headers["content-type"] == "image/png"
    assert r.content[:8] == b"\x89PNG\r\n\x1a\n"
    assert client.get("/slide", params={"file": "deck.pdf", "page": 99}).status_code == 404


# --- quiz routes (against an in-memory bank monkeypatched into main) ---------


def _mcq(qid, topic, *, stem, tags=None):
    q = {
        "id": qid,
        "lecture_id": "L04",
        "topic": topic,
        "difficulty": "easy",
        "stem": stem,
        "answer": "A",
        "explanation": "because (Deck p.1).",
        "source": {"deck": "d.pdf", "page": 1},
        "options": [{"key": k, "text": k} for k in ("A", "B", "C", "D")],
    }
    if tags is not None:
        q["tags"] = tags
    return q


def _bank_with_questions(tmp_path):
    from app.quiz import QuizBank

    questions = [
        _mcq("L04-Q001", "Refactoring", stem="Q1?"),
        # Cross-cutting: its taxonomy topic lives only in `tags` (FIX 1b reachability).
        _mcq(
            "L04-Q002",
            "Refactoring",
            stem="Q2?",
            tags=["JHotDraw Case Study", "extract-method"],
        ),
    ]
    (tmp_path / "lecture-04.json").write_text(
        json.dumps({"lecture_id": "L04", "questions": questions}), encoding="utf-8"
    )
    return QuizBank.load(str(tmp_path))


def test_api_lectures_and_quiz_flow(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "_bank", _bank_with_questions(tmp_path))
    client = TestClient(main.app)

    lec = client.get("/api/lectures")
    assert lec.status_code == 200
    assert lec.json()[0]["lecture_id"] == "L04"

    quiz = client.get("/api/quiz", params={"lecture": "L04", "n": 5})
    assert quiz.status_code == 200
    body = quiz.json()
    assert body["count"] == 2
    served = body["questions"][0]
    # FIX 2: pre-grade payload must not leak answer, explanation, or source.
    assert "answer" not in served
    assert "explanation" not in served
    assert "source" not in served

    check = client.post("/api/quiz/check", json={"answers": [{"id": "L04-Q001", "chosen": "A"}]})
    assert check.status_code == 200
    check_body = check.json()
    assert check_body["score"] == 1
    # FIX 2: source (and answer/explanation) DO come back after grading, for citations.
    result = check_body["results"][0]
    assert result["answer"] == "A"
    assert result["explanation"] == "because (Deck p.1)."
    assert result["source"] == {"deck": "d.pdf", "page": 1}


def test_api_lectures_topics_are_bank_derived(tmp_path, monkeypatch):
    # FIX 1a: /api/lectures topics == the distinct taxonomy topics present in the
    # lecture's fixture questions (no extra granular tags, no missing tag-topics).
    monkeypatch.setattr(main, "_bank", _bank_with_questions(tmp_path))
    client = TestClient(main.app)
    row = client.get("/api/lectures").json()[0]
    assert row["topics"] == ["JHotDraw Case Study", "Refactoring"]


def test_api_quiz_filter_matches_topic_only_in_tags(tmp_path, monkeypatch):
    # FIX 1b: requesting a topic that only appears in a question's `tags` returns it.
    monkeypatch.setattr(main, "_bank", _bank_with_questions(tmp_path))
    client = TestClient(main.app)
    r = client.get("/api/quiz", params={"lecture": "L04", "topic": "JHotDraw Case Study", "n": 5})
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 1
    assert body["questions"][0]["id"] == "L04-Q002"


def test_api_quiz_validation_and_404(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "_bank", _bank_with_questions(tmp_path))
    client = TestClient(main.app)
    assert client.get("/api/quiz", params={"lecture": "bad"}).status_code == 422
    assert client.get("/api/quiz", params={"difficulty": "trivial"}).status_code == 422
    # valid filter that matches nothing -> 404
    assert client.get("/api/quiz", params={"lecture": "L11"}).status_code == 404


def test_api_quiz_check_malformed_body(monkeypatch, tmp_path):
    monkeypatch.setattr(main, "_bank", _bank_with_questions(tmp_path))
    client = TestClient(main.app)
    assert client.post("/api/quiz/check", json={"nope": 1}).status_code == 422
