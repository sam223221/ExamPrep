"""Quiz bank: load, filter, seeded sample, grade, and answer-hygiene."""

import json

from app.quiz import QuizBank


def _q(qid, lecture, topic, difficulty, answer="A", stem=None, tags=None):
    q = {
        "id": qid,
        "lecture_id": lecture,
        "topic": topic,
        "difficulty": difficulty,
        "stem": stem or f"Question {qid}?",
        "options": [
            {"key": "A", "text": "alpha"},
            {"key": "B", "text": "bravo"},
            {"key": "C", "text": "charlie"},
            {"key": "D", "text": "delta"},
        ],
        "answer": answer,
        "explanation": f"Because {answer} (Deck p.1).",
        "source": {"deck": "Refactoring1.pdf", "page": 1},
    }
    if tags is not None:
        q["tags"] = tags
    return q


def _write_bank(tmp_path):
    l4 = {
        "lecture_id": "L04",
        "questions": [
            _q("L04-Q001", "L04", "Refactoring", "easy"),
            _q("L04-Q002", "L04", "Refactoring", "hard", answer="C"),
            _q("L04-Q003", "L04", "Prefactoring", "easy", answer="B"),
            # Cross-cutting: primary topic Refactoring, but its taxonomy topic
            # "JHotDraw Case Study" lives only in `tags` (alongside granular,
            # non-taxonomy tags that must NOT become offered chips).
            _q(
                "L04-Q004",
                "L04",
                "Refactoring",
                "medium",
                answer="D",
                tags=["JHotDraw Case Study", "extract-method", "gof"],
            ),
        ],
    }
    l7 = {
        "lecture_id": "L07",
        "questions": [
            _q("L07-Q001", "L07", "Software Testing", "medium", answer="D"),
        ],
    }
    (tmp_path / "lecture-04-refactoring.json").write_text(json.dumps(l4), encoding="utf-8")
    (tmp_path / "lecture-07-testing.json").write_text(json.dumps(l7), encoding="utf-8")
    return QuizBank.load(str(tmp_path))


def test_load_empty_dir_does_not_crash(tmp_path):
    bank = QuizBank.load(str(tmp_path / "nope"))
    assert bank.questions == []
    assert bank.sample(n=5) == []  # no questions -> empty, no exception


def test_buckets_and_metadata(tmp_path):
    bank = _write_bank(tmp_path)
    assert len(bank.questions) == 5
    rows = bank.lectures_metadata()
    ids = [r["lecture_id"] for r in rows]
    assert ids == ["L04", "L07"]  # numeric order
    l4 = rows[0]
    assert l4["counts"]["total"] == 4
    assert l4["counts"]["by_difficulty"]["easy"] == 2
    assert l4["counts"]["by_difficulty"]["hard"] == 1
    assert l4["counts"]["by_difficulty"]["medium"] == 1


def test_filter_by_lecture_difficulty_topic(tmp_path):
    bank = _write_bank(tmp_path)
    easy_l4 = bank.sample(lecture="L04", difficulty="easy", n=10)
    assert {q["id"] for q in easy_l4} == {"L04-Q001", "L04-Q003"}
    pref = bank.sample(lecture="L04", topic="Prefactoring", n=10)
    assert {q["id"] for q in pref} == {"L04-Q003"}
    all_q = bank.sample(lecture="all", n=10)
    assert len(all_q) == 5


def test_served_payload_strips_answer_explanation_and_source(tmp_path):
    bank = _write_bank(tmp_path)
    for q in bank.sample(n=10):
        # FIX 2: source (deck + page) is withheld pre-grade — it points at the slide.
        assert "answer" not in q
        assert "explanation" not in q
        assert "source" not in q
        # Public fields the UI needs DO survive.
        assert set(q) <= {"id", "lecture_id", "topic", "difficulty", "stem", "options", "tags"}
        assert {"id", "lecture_id", "topic", "difficulty", "stem", "options"} <= set(q)
        assert len(q["options"]) == 4
        assert {o["key"] for o in q["options"]} == {"A", "B", "C", "D"}


def test_served_payload_keeps_tags(tmp_path):
    # `tags` is a public field (FIX 2 keeps it); the cross-cutting question carries it.
    bank = _write_bank(tmp_path)
    served = {q["id"]: q for q in bank.sample(lecture="L04", n=10)}
    assert served["L04-Q004"]["tags"] == ["JHotDraw Case Study", "extract-method", "gof"]


def test_filter_matches_topic_only_in_tags(tmp_path):
    # FIX 1b: a question whose taxonomy topic lives ONLY in `tags` is reachable.
    bank = _write_bank(tmp_path)
    jhd = bank.sample(lecture="L04", topic="JHotDraw Case Study", n=10)
    assert {q["id"] for q in jhd} == {"L04-Q004"}
    # The same question is also still reachable by its primary topic.
    refac = bank.sample(lecture="L04", topic="Refactoring", n=10)
    assert "L04-Q004" in {q["id"] for q in refac}


def test_metadata_topics_are_bank_derived_distinct_set(tmp_path):
    # FIX 1a: offered topics == sorted, distinct taxonomy topics actually present in
    # the lecture's questions (primary topic + taxonomy topics from `tags`). Granular
    # non-taxonomy tags ("extract-method", "gof") must NOT appear as chips.
    bank = _write_bank(tmp_path)
    rows = {r["lecture_id"]: r for r in bank.lectures_metadata()}
    assert rows["L04"]["topics"] == ["JHotDraw Case Study", "Prefactoring", "Refactoring"]
    assert rows["L07"]["topics"] == ["Software Testing"]
    # Every offered chip has >= 1 matching question (the coherence guarantee).
    for lec, row in rows.items():
        for topic in row["topics"]:
            assert bank.sample(lecture=lec, topic=topic, n=50), (lec, topic)


def test_seeded_sample_is_deterministic(tmp_path):
    bank = _write_bank(tmp_path)
    a = bank.sample(lecture="all", n=3, seed=42)
    b = bank.sample(lecture="all", n=3, seed=42)
    assert [q["id"] for q in a] == [q["id"] for q in b]
    # option order is also deterministic under the same seed
    assert [o["key"] for o in a[0]["options"]] == [o["key"] for o in b[0]["options"]]


def test_grade_scores_against_bank(tmp_path):
    bank = _write_bank(tmp_path)
    result = bank.grade(
        [
            {"id": "L04-Q001", "chosen": "A"},  # correct
            {"id": "L04-Q002", "chosen": "A"},  # wrong (answer C)
            {"id": "L07-Q001", "chosen": "D"},  # correct
        ]
    )
    assert result["score"] == 2
    assert result["total"] == 3
    by_id = {r["id"]: r for r in result["results"]}
    assert by_id["L04-Q001"]["correct"] is True
    assert by_id["L04-Q002"]["correct"] is False
    assert by_id["L04-Q002"]["answer"] == "C"
    assert "Deck p.1" in by_id["L04-Q002"]["explanation"]
    assert by_id["L04-Q001"]["source"]["deck"] == "Refactoring1.pdf"


def test_grade_unknown_id_flagged_not_crash(tmp_path):
    bank = _write_bank(tmp_path)
    result = bank.grade([{"id": "L99-Q999", "chosen": "A"}, {"bad": "entry"}])
    assert result["score"] == 0
    assert all(r["correct"] is False for r in result["results"])
    assert result["results"][0]["unknown"] is True
