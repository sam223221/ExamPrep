"""Guide identity derivation + corpus gathering (``app.ingest``).

Covers the two identity paths of ``guide_lecture_meta``:

* ``lecture-NN-*`` guides (NN in the canonical L01..L12 range) carry full lecture
  identity — id, number, curated lecture title, primary taxonomy topic.
* Course-level guides — ``00-overview.md`` and the ``9x`` exam-prep series
  (``90-exam-*.md`` …) — carry NO lecture id (Lookup renders no L-badge), a
  slug-derived title, and the course-spine topic so they stay searchable.

Plus a ``gather_chunks`` integration check that the metadata actually lands on
the chunks and that engineering files (``DOCUMENT.md``) never enter the corpus.
"""

from app import ingest


def test_lecture_guide_carries_full_identity():
    lid, num, deck_title, topic = ingest.guide_lecture_meta(
        "/data/guides/lecture-04-refactoring-maintainable-code.md"
    )
    assert lid == "L04"
    assert num == 4
    assert deck_title == "Refactoring & Maintainable Code"  # curated LECTURE_TITLES row
    assert topic == "Refactoring"  # first LECTURE_TOPICS entry


def test_overview_guide_has_no_lecture_identity():
    lid, num, deck_title, topic = ingest.guide_lecture_meta("/data/guides/00-overview.md")
    assert lid is None
    assert num == 0
    assert deck_title == "Overview"
    assert topic == "Software Change Process"


def test_exam_series_guides_have_no_lecture_identity():
    # The 9x exam-prep guides must NOT mint bogus L90/L91/L92 ids — they take the
    # same no-lecture path as 00-overview.md, with sensible slug-derived titles.
    cases = {
        "90-exam-what-to-expect.md": "Exam What To Expect",
        "91-exam-model-answers.md": "Exam Model Answers",
        "92-exam-copy-paste-library.md": "Exam Copy Paste Library",
    }
    for fname, expected_title in cases.items():
        lid, num, deck_title, topic = ingest.guide_lecture_meta(f"/data/guides/{fname}")
        assert lid is None, fname
        assert num == 0, fname
        assert deck_title == expected_title
        assert topic == "Software Change Process"


def test_lecture_prefixed_guide_outside_canonical_range_gets_no_id():
    # Defensive: even an explicit ``lecture-`` prefix never mints an id beyond L12.
    lid, num, deck_title, topic = ingest.guide_lecture_meta("/data/guides/lecture-90-bogus.md")
    assert lid is None
    assert num == 0
    assert deck_title == "Bogus"
    assert topic == "Software Change Process"


def test_unconventional_filename_falls_back_gracefully():
    lid, num, deck_title, topic = ingest.guide_lecture_meta("/data/guides/cheat-sheet.md")
    assert lid is None
    assert num == 0
    assert deck_title == "Cheat Sheet"
    assert topic == "Software Change Process"


def test_gather_chunks_metadata_and_exclusions(tmp_path, monkeypatch):
    (tmp_path / "00-overview.md").write_text(
        "## Course Map\n\nThe change spine in brief.\n", encoding="utf-8"
    )
    (tmp_path / "lecture-04-refactoring.md").write_text(
        "## Key Concepts\n\nExtract Method shortens long methods.\n", encoding="utf-8"
    )
    (tmp_path / "91-exam-model-answers.md").write_text(
        "## What is meant by a refactoring pattern?\n\nA reusable transformation.\n",
        encoding="utf-8",
    )
    # Engineering scaffolding: must never enter the searchable corpus.
    (tmp_path / "DOCUMENT.md").write_text("## Internal\n\nNot study content.\n", encoding="utf-8")
    monkeypatch.setattr(ingest, "GUIDE_ROOT", str(tmp_path))

    chunks = ingest.gather_chunks()

    assert all("Not study content" not in c["text"] for c in chunks)
    by_title = {c["title"]: c for c in chunks}
    lecture_chunk = by_title["Key Concepts"]
    assert lecture_chunk["lecture_id"] == "L04"
    assert lecture_chunk["lecture_num"] == 4
    exam_chunk = by_title["What is meant by a refactoring pattern?"]
    assert exam_chunk["lecture_id"] == ""  # empty string -> no L-badge in Lookup
    assert exam_chunk["lecture_num"] == 0
    assert exam_chunk["deck_title"] == "Exam Model Answers"
    assert exam_chunk["topic"] == "Software Change Process"
    overview_chunk = by_title["Course Map"]
    assert overview_chunk["lecture_id"] == ""
    assert overview_chunk["deck_title"] == "Overview"
