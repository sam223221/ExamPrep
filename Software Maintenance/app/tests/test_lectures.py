"""Lecture identity, numeric sort, deck-title map, taxonomy."""

from app import lectures as L


def test_lecture_num_of_parses_integer():
    assert L.lecture_num_of("/data/pdfs/Lecture 4/Refactoring1.pdf") == 4
    assert L.lecture_num_of("Lecture 10/CleanCode.pdf") == 10
    assert L.lecture_num_of(r"C:\x\Lecture 12\foo.pdf") == 12
    assert L.lecture_num_of("no-lecture-here.pdf") is None


def test_lecture_id_zero_padded():
    assert L.lecture_id_from_num(4) == "L04"
    assert L.lecture_id_from_num(11) == "L11"
    assert L.lecture_id_of("Lecture 2/JHotDraw.pdf") == "L02"
    assert L.num_from_lecture_id("L09") == 9
    assert L.num_from_lecture_id("nope") is None


def test_numeric_sort_beats_lexical():
    # Lexical sort would put Lecture 10/11/12 before Lecture 2 — the core hazard.
    paths = [
        "Lecture 2/a.pdf",
        "Lecture 12/a.pdf",
        "Lecture 1/a.pdf",
        "Lecture 10/a.pdf",
        "Lecture 11/a.pdf",
    ]
    out = L.numeric_lecture_sort(paths)
    nums = [L.lecture_num_of(p) for p in out]
    assert nums == [1, 2, 10, 11, 12]


def test_numeric_sort_places_unlectured_last():
    paths = ["zzz.pdf", "Lecture 3/x.pdf", "aaa.pdf"]
    out = L.numeric_lecture_sort(paths)
    assert out[0] == "Lecture 3/x.pdf"
    assert set(out[1:]) == {"aaa.pdf", "zzz.pdf"}


def test_deck_title_curated_and_fallback():
    assert L.deck_title_of("ConceptLocation.pdf") == "Concept Location"
    assert L.deck_title_of("BetterCode.pdf") == "Building Maintainable Software"
    # Unmapped file: camelCase split fallback, never crashes.
    assert L.deck_title_of("SomeNewDeck.pdf") == "Some New Deck"


def test_doc_kind_classification():
    assert L.doc_kind_of("Refactoring1.pdf") == "deck"
    assert L.doc_kind_of("RefactoringLab1.pdf") == "lab"
    assert L.doc_kind_of("Lab - GIT.pdf") == "lab"
    assert L.doc_kind_of("[Litt] Literature List.pdf") == "meta"


def test_taxonomy_is_closed_and_sized():
    assert len(L.TOPICS) == 16
    assert "Refactoring" in L.TOPIC_SET
    assert L.DIFFICULTIES == ("easy", "medium", "hard", "very-hard")


def test_topics_for_lecture_and_titles():
    assert "Refactoring" in L.topics_for_lecture("L04")
    assert L.topics_for_lecture("L08") == []  # empty lecture: no topics, no crash
    assert L.lecture_title_of("L07") == "Software Testing"
    assert L.lecture_title_of("L08") == "Lecture 8"  # generic fallback
