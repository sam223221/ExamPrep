"""Chunkers: source page-flush and guide H2/size-bounded split, with §2.4 metadata."""

from app.chunker import (
    GUIDE_CHUNK_BUDGET_TOKENS,
    TITLE_SEPARATOR,
    chunk_markdown,
    chunk_source,
    est_tokens,
)

_SRC_KW = {
    "lecture_id": "L04",
    "lecture_num": 4,
    "deck_title": "Refactoring",
    "source_pdf": "Refactoring1.pdf",
    "topic": "Refactoring",
}
_GUIDE_KW = {
    "lecture_id": "L04",
    "lecture_num": 4,
    "deck_title": "Refactoring & Maintainable Code",
    "topic": "Refactoring",
}


def test_chunk_source_flushes_on_page_boundary():
    text = "<!-- page:1 -->\nExtract method intro.\n<!-- page:2 -->\nRename variable detail."
    chunks = chunk_source(text, max_chars=200, **_SRC_KW)
    pages = {c["page"] for c in chunks}
    assert 1 in pages and 2 in pages
    assert all(c["chunk_type"] == "source" for c in chunks)
    assert all(c["lecture_id"] == "L04" and c["lecture_num"] == 4 for c in chunks)
    assert all(c["source_pdf"] == "Refactoring1.pdf" for c in chunks)
    # no chunk straddles a page marker
    p1 = next(c for c in chunks if c["page"] == 1)
    assert "Rename variable" not in p1["text"]


def test_chunk_source_respects_max_chars():
    # Real extracted page text is many short lines; the chunker flushes once the
    # accumulated line buffer crosses max_chars (it splits between lines, not mid-line).
    lines = "\n".join(["word " * 10 for _ in range(50)])  # ~50 lines, ~2500 chars
    text = f"<!-- page:1 -->\n{lines}"
    chunks = chunk_source(text, max_chars=300, **_SRC_KW)
    assert len(chunks) >= 2  # one page split into multiple ~300-char chunks
    assert all(c["page"] == 1 for c in chunks)


def test_chunk_markdown_splits_by_h2():
    md = "# Lecture 4 — Refactoring\nintro line\n## Key Concepts\nExtract Method.\n## Glossary\nTerm: x."
    chunks = chunk_markdown(md, **_GUIDE_KW)
    titles = {c["title"] for c in chunks}
    assert "Key Concepts" in titles and "Glossary" in titles
    assert all(c["chunk_type"] == "guide" for c in chunks)
    assert all(c["page"] == 0 for c in chunks)
    # content before the first H2 is captured under Overview
    assert any(c["title"] == "Overview" and "intro line" in c["text"] for c in chunks)


def test_chunk_markdown_carries_metadata():
    md = "## Section A\nbody"
    chunks = chunk_markdown(md, **_GUIDE_KW)
    c = chunks[0]
    for key in (
        "lecture_id",
        "lecture_num",
        "deck_title",
        "source_pdf",
        "page",
        "topic",
        "chunk_type",
        "title",
        "doc_kind",
        "chunk_index",
    ):
        assert key in c


# --- size-bounded sub-chunking (deepened-guide fix) -------------------------

#: ~1,800 chars at the default budget; one paragraph is a little under budget so a
#: handful of them per H3 forces the cascade to window on paragraph boundaries.
_BUDGET_CHARS = GUIDE_CHUNK_BUDGET_TOKENS * 4


def _para(token: str) -> str:
    """A ~360-char paragraph (well under budget) embedding a unique ``token``."""
    return f"{token} " + ("alpha beta gamma delta epsilon zeta eta theta. " * 8)


def _h3(title: str, lo: int, hi: int) -> str:
    """An ``### title`` subsection of unique ``P##``-tokened paragraphs ``[lo, hi)``."""
    body = "\n\n".join(_para(f"P{i:02d}") for i in range(lo, hi))
    return f"### {title}\n{body}"


def _big_guide() -> str:
    """A guide with one small H2 and one huge multi-``###`` H2 section.

    The large H2 has two H3 subsections each containing several paragraphs that, in
    aggregate, exceed budget — so every level of the cascade (H3 split + paragraph
    windowing) is exercised. Each paragraph carries a unique ``P##`` token so the
    lossless-coverage assertion can verify nothing is dropped.
    """
    small = "## Quick Note\n" + _para("SMALL")
    h3a = _h3("Catalog Part One", 0, 8)
    h3b = _h3("Catalog Part Two", 8, 16)
    lead = "## Key Concepts\nlead-in before the first subsection."
    big = f"{lead}\n\n{h3a}\n\n{h3b}"
    return f"# Lecture 4 — Refactoring\nintro\n\n{small}\n\n{big}\n"


def test_small_section_stays_one_chunk():
    chunks = chunk_markdown(_big_guide(), **_GUIDE_KW)
    small = [c for c in chunks if c["title"] == "Quick Note"]
    assert len(small) == 1
    assert "SMALL" in small[0]["text"]


def test_no_chunk_exceeds_budget():
    chunks = chunk_markdown(_big_guide(), **_GUIDE_KW)
    assert chunks, "expected chunks to be produced"
    for c in chunks:
        assert len(c["text"]) <= _BUDGET_CHARS, f"{c['title']} over char budget"
        toks = est_tokens(c["text"])
        assert toks <= GUIDE_CHUNK_BUDGET_TOKENS, f"{c['title']} over token budget"


def test_h3_subchunks_carry_h2_h3_title_and_metadata():
    chunks = chunk_markdown(_big_guide(), **_GUIDE_KW)
    sub = [c for c in chunks if TITLE_SEPARATOR in c["title"]]
    assert sub, "expected H3-derived sub-chunks with 'H2 › H3' titles"
    expected = {
        f"Key Concepts{TITLE_SEPARATOR}Catalog Part One",
        f"Key Concepts{TITLE_SEPARATOR}Catalog Part Two",
    }
    assert {c["title"] for c in sub} == expected
    for c in sub:
        assert c["lecture_id"] == "L04"
        assert c["chunk_type"] == "guide"
        assert c["page"] == 0
        assert c["topic"] == "Refactoring"


def test_chunk_indices_are_unique_and_stable():
    chunks = chunk_markdown(_big_guide(), **_GUIDE_KW)
    idxs = [c["chunk_index"] for c in chunks]
    assert idxs == list(range(len(chunks)))  # monotonic, gap-free, unique


def test_h2_direct_content_keeps_plain_h2_title():
    # The "lead-in before the first subsection" sits under the H2 but before any H3,
    # so it must keep the bare H2 title (no separator).
    chunks = chunk_markdown(_big_guide(), **_GUIDE_KW)
    lead = [c for c in chunks if c["title"] == "Key Concepts"]
    assert lead, "H2-direct lead-in should be emitted under the plain H2 title"
    assert any("lead-in" in c["text"] for c in lead)


def test_windowing_is_lossless_across_subchunks():
    # Every authored paragraph token (P00..P15) must survive somewhere in the
    # sub-chunks for its H3 — windowing splits but never drops content.
    chunks = chunk_markdown(_big_guide(), **_GUIDE_KW)
    joined = "\n".join(c["text"] for c in chunks)
    for i in range(16):
        assert f"P{i:02d}" in joined, f"paragraph P{i:02d} was lost"


def test_windows_overlap_at_seams():
    # A long H3 (no sub-headings) split into multiple windows must share a paragraph
    # at the seam so context is not lost — consecutive windows overlap.
    paras = "\n\n".join(_para(f"Q{i:02d}") for i in range(12))
    md = f"## Deep Dive\n{paras}"
    chunks = chunk_markdown(md, **_GUIDE_KW)
    assert len(chunks) >= 2, "expected the oversized section to window into pieces"
    overlapped = False
    for a, b in zip(chunks, chunks[1:], strict=False):
        a_tokens = {t for t in a["text"].split() if t.startswith("Q")}
        b_tokens = {t for t in b["text"].split() if t.startswith("Q")}
        if a_tokens & b_tokens:
            overlapped = True
    assert overlapped, "consecutive windows should share an overlap paragraph"


def test_section_without_h3_windows_directly():
    # A huge H2 with NO H3s must skip the H3 step and window on paragraphs directly.
    paras = "\n\n".join(_para(f"R{i:02d}") for i in range(12))
    md = f"## Definitions & Terminology\n{paras}"
    chunks = chunk_markdown(md, **_GUIDE_KW)
    assert len(chunks) >= 2
    assert all(c["title"] == "Definitions & Terminology" for c in chunks)
    assert all(len(c["text"]) <= _BUDGET_CHARS for c in chunks)


def test_oversized_paragraph_split_on_sentences():
    # A single paragraph larger than budget must be split (on sentence ends) so no
    # chunk exceeds budget, and must not be dropped.
    sentence = "This is a self contained sentence about refactoring. "
    huge_para = sentence * 60  # ~3,180 chars, well over the ~1,800 budget
    md = f"## Big Para\n{huge_para}"
    chunks = chunk_markdown(md, **_GUIDE_KW)
    assert len(chunks) >= 2
    assert all(len(c["text"]) <= _BUDGET_CHARS for c in chunks)
    assert all(c["title"] == "Big Para" for c in chunks)
