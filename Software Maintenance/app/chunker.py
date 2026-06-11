"""Split source text and guide markdown into chunks carrying §2.4 metadata.

Two producers (matching cyper, minus its ``qna``/``cmd`` types — this app embeds
GUIDES only and serves MCQs from JSON):

  * ``chunk_source``   — page-marked deck/lab text -> ~1000-char ``source`` chunks,
                         flushed on page-marker boundaries, each tagged with the
                         real PDF page. Built for slide-render page mapping and as
                         a fallback corpus; not embedded by default (architecture §2.3).
  * ``chunk_markdown`` — generated study-guide ``.md`` -> ``guide`` chunks split on
                         ``## `` H2 headings, page 0 (synthesized content).

After the guides were deepened (~doubled in size) the H2-per-chunk rule produced
chunks far larger than the bge-small embedding window (~512 tokens), so the
embedder silently truncated each section to its first concept and lookup recall
for deep content collapsed. ``chunk_markdown`` therefore applies a size-bounded
cascade so **no emitted chunk exceeds ~``GUIDE_CHUNK_BUDGET_TOKENS``** while the
stored markdown and its H2 headers are left untouched (this only changes how text
is split for the index):

  1. Split the guide on ``## `` H2 sections (as before).
  2. An H2 section within budget is emitted as one chunk (no regression for small
     sections — current behaviour).
  3. An over-budget H2 section is sub-split on ``### `` H3 subsections.
  4. An H3 subsection (or an H2 that has no H3s) still over budget is windowed
     into <=budget pieces on blank-line / paragraph boundaries (never mid-sentence)
     with a ~1-paragraph overlap so context is not lost at the seams. A single
     paragraph above budget is split on sentence boundaries; a single sentence
     above budget is hard-split as a last resort so the invariant always holds.

Tokens are estimated as ``len(text) / 4`` (dependency-free, consistent with how
the index was measured). Every chunk still carries the full architecture §2.4
metadata block (scalar values only) and renders uniformly in the UI; sub-chunks
inherit their H2 section ``title`` (a sub-chunk from an H3 is labelled
``"<H2 section> › <H3 subsection>"``) and a stable ``chunk_index`` so ``ingest.py``
ids stay unique.
"""

from __future__ import annotations

import re

PAGE_RE = re.compile(r"<!--\s*page:(\d+)\s*-->")

#: Per-chunk embedding budget. ~450 tokens keeps every chunk inside the bge-small
#: window (~512) with headroom for the bge query prefix; ~1,800 chars at 4 chars/token.
GUIDE_CHUNK_BUDGET_TOKENS = 450
_CHARS_PER_TOKEN = 4
#: Overlap carried between windowed pieces so context is not lost at a seam.
_WINDOW_OVERLAP_TOKENS = 40

#: H2 ``title`` and H3 subsection ``title`` are joined with this separator so a
#: result card from an H3-derived sub-chunk shows ``"<H2> › <H3>"``.
TITLE_SEPARATOR = " › "

# Sentence boundary: end punctuation followed by whitespace. Used only to split a
# single paragraph that is itself over budget — never to split inside a sentence.
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def est_tokens(text: str) -> int:
    """Estimate token count as ``len(text) / 4`` (matches how the index was sized)."""
    return len(text) // _CHARS_PER_TOKEN


def _budget_chars(budget_tokens: int) -> int:
    return budget_tokens * _CHARS_PER_TOKEN


def _meta(
    *,
    text: str,
    lecture_id: str,
    lecture_num: int,
    deck_title: str,
    source_pdf: str,
    page: int,
    topic: str,
    chunk_type: str,
    title: str,
    doc_kind: str,
    chunk_index: int,
) -> dict:
    """Assemble one chunk dict with the exact §2.4 field set (all scalar)."""
    return {
        "text": text,
        "lecture_id": lecture_id,
        "lecture_num": lecture_num,
        "deck_title": deck_title,
        "source_pdf": source_pdf,
        "page": page,
        "topic": topic,
        "chunk_type": chunk_type,
        "title": title,
        "doc_kind": doc_kind,
        "chunk_index": chunk_index,
    }


def chunk_source(
    text: str,
    *,
    lecture_id: str,
    lecture_num: int,
    deck_title: str,
    source_pdf: str,
    topic: str,
    doc_kind: str = "deck",
    max_chars: int = 1000,
) -> list[dict]:
    """Split page-marked source text into ~``max_chars`` chunks, tagging each page.

    Accumulates lines until ~``max_chars`` characters, flushing the buffer on every
    page-marker boundary so a chunk never straddles two PDF pages and always carries
    one true ``page``. ``chunk_type='source'``.
    """
    chunks: list[dict] = []
    cur_page = 1
    buf: list[str] = []

    def flush() -> None:
        body = " ".join(part for part in buf if part).strip()
        if body:
            chunks.append(
                _meta(
                    text=body,
                    lecture_id=lecture_id,
                    lecture_num=lecture_num,
                    deck_title=deck_title,
                    source_pdf=source_pdf,
                    page=cur_page,
                    topic=topic,
                    chunk_type="source",
                    title=deck_title,
                    doc_kind=doc_kind,
                    chunk_index=len(chunks),
                )
            )

    for line in text.splitlines():
        m = PAGE_RE.search(line)
        if m:
            flush()
            buf.clear()
            cur_page = int(m.group(1))
            continue
        buf.append(line)
        if sum(len(x) for x in buf) >= max_chars:
            flush()
            buf.clear()
    flush()
    return chunks


def _split_oversized_paragraph(paragraph: str, budget_chars: int) -> list[str]:
    """Break a single over-budget paragraph into <=budget pieces on sentence ends.

    Sentences are greedily packed up to ``budget_chars``. A lone sentence that is
    itself over budget is hard-split into ``budget_chars`` slices (last-resort
    guarantee that no piece ever exceeds budget); this is rare in authored guides.
    """
    pieces: list[str] = []
    cur = ""
    for sentence in _SENTENCE_SPLIT_RE.split(paragraph.strip()):
        sentence = sentence.strip()
        if not sentence:
            continue
        if len(sentence) > budget_chars:
            if cur:
                pieces.append(cur)
                cur = ""
            for i in range(0, len(sentence), budget_chars):
                pieces.append(sentence[i : i + budget_chars])
            continue
        candidate = f"{cur} {sentence}".strip() if cur else sentence
        if len(candidate) > budget_chars:
            if cur:
                pieces.append(cur)
            cur = sentence
        else:
            cur = candidate
    if cur:
        pieces.append(cur)
    return pieces


def _window_paragraphs(text: str, budget_tokens: int) -> list[str]:
    """Window ``text`` into <=budget pieces on blank-line / paragraph boundaries.

    Packs whole paragraphs up to the budget, carrying ~``_WINDOW_OVERLAP_TOKENS``
    of the previous piece's tail paragraph(s) into the next so context is not lost
    at a seam. Any single paragraph over budget is first split on sentence
    boundaries (never mid-sentence) by :func:`_split_oversized_paragraph`.
    """
    budget_chars = _budget_chars(budget_tokens)
    overlap_chars = _budget_chars(_WINDOW_OVERLAP_TOKENS)

    # Normalise into atomic, within-budget paragraph units.
    units: list[str] = []
    for para in re.split(r"\n\s*\n", text):
        para = para.strip()
        if not para:
            continue
        if len(para) > budget_chars:
            units.extend(_split_oversized_paragraph(para, budget_chars))
        else:
            units.append(para)
    if not units:
        return []

    def joined_len(parts: list[str]) -> int:
        # Length of "\n\n".join(parts) without building the string.
        return sum(len(p) for p in parts) + 2 * max(0, len(parts) - 1)

    def overlap_tail(parts: list[str], headroom: int) -> list[str]:
        """Trailing paragraph(s) of ``parts`` to seed the next window as overlap.

        Targets ~``overlap_chars`` but always keeps **at least the last whole
        paragraph** (the "~1 paragraph" overlap from the spec) so context survives a
        seam even when paragraphs are larger than ~40 tokens. ``headroom`` (the room
        the next unit leaves in a fresh window) is a hard cap so the seeded overlap
        can never push that window over budget; if even the last paragraph will not
        fit the headroom, the tail is empty. Whole paragraphs only — never
        mid-sentence.
        """
        tail: list[str] = []
        for i, prev in enumerate(reversed(parts)):
            candidate = [prev, *tail]
            if joined_len(candidate) > headroom:
                break
            # Keep the first (last-in-section) paragraph unconditionally; keep
            # further ones only while under the soft overlap target.
            if i > 0 and joined_len(candidate) > overlap_chars:
                break
            tail.insert(0, prev)
        return tail

    pieces: list[str] = []
    cur: list[str] = []

    for unit in units:
        if cur and joined_len([*cur, unit]) > budget_chars:
            pieces.append("\n\n".join(cur))
            # Seed the next window with a bounded overlap that still leaves room
            # for ``unit`` (every unit is guaranteed <= budget_chars).
            cur = overlap_tail(cur, budget_chars - len(unit))
        cur.append(unit)
    if cur:
        pieces.append("\n\n".join(cur))
    return pieces


def _split_h3_sections(body: str) -> list[tuple[str | None, str]]:
    """Split an H2 body into ``[(h3_title | None, h3_body), ...]`` on ``### `` heads.

    Content before the first ``### `` is returned with an ``h3_title`` of ``None``
    (it belongs to the H2 section directly). Sections with no H3s yield a single
    ``(None, body)`` pair.
    """
    sections: list[tuple[str | None, str]] = []
    cur_title: str | None = None
    buf: list[str] = []

    def flush() -> None:
        chunk_body = "\n".join(buf).strip()
        if chunk_body:
            sections.append((cur_title, chunk_body))

    for line in body.splitlines():
        if line.startswith("### "):
            flush()
            buf = []
            cur_title = line[4:].strip()
        else:
            buf.append(line)
    flush()
    return sections


def chunk_markdown(
    md: str,
    *,
    lecture_id: str,
    lecture_num: int,
    deck_title: str,
    topic: str,
    source_pdf: str = "",
    doc_kind: str = "deck",
    budget_tokens: int = GUIDE_CHUNK_BUDGET_TOKENS,
) -> list[dict]:
    """Split a study-guide markdown file into size-bounded ``guide`` chunks.

    Splits on ``## `` H2 headings (the H1 title line is skipped; content before the
    first H2 accumulates under an "Overview" section). An H2 section within
    ``budget_tokens`` is emitted as one chunk; an over-budget section is sub-split
    on ``### `` H3s and, if still over budget, windowed on paragraph boundaries with
    a small overlap. ``page=0`` (synthesized content), ``chunk_type='guide'``.

    The H2 heading text is each chunk's ``title``; a sub-chunk derived from an H3 is
    labelled ``"<H2 section> › <H3 subsection>"``. A monotonic ``chunk_index`` keeps
    ids unique in ``ingest.py``. No emitted chunk exceeds ``budget_tokens``.
    """
    chunks: list[dict] = []

    def emit(text: str, title: str) -> None:
        body = text.strip()
        if body:
            chunks.append(
                _meta(
                    text=body,
                    lecture_id=lecture_id,
                    lecture_num=lecture_num,
                    deck_title=deck_title,
                    source_pdf=source_pdf,
                    page=0,
                    topic=topic,
                    chunk_type="guide",
                    title=title,
                    doc_kind=doc_kind,
                    chunk_index=len(chunks),
                )
            )

    def emit_bounded(text: str, title: str) -> None:
        """Emit ``text`` as one chunk if within budget, else windowed sub-chunks."""
        if est_tokens(text) <= budget_tokens:
            emit(text, title)
            return
        for window in _window_paragraphs(text, budget_tokens):
            emit(window, title)

    # --- split into H2 sections (preserving the legacy "Overview" pre-section) ---
    h2_title = "Overview"
    buf: list[str] = []

    def flush_h2() -> None:
        section = "\n".join(buf).strip()
        if not section:
            return
        if est_tokens(section) <= budget_tokens:
            emit(section, h2_title)
            return
        # Over budget: cascade to H3 subsections, then paragraph windowing.
        for h3_title, h3_body in _split_h3_sections(section):
            if h3_title is None:
                # H2-direct content (or an H2 with no H3s at all).
                emit_bounded(h3_body, h2_title)
            else:
                emit_bounded(h3_body, f"{h2_title}{TITLE_SEPARATOR}{h3_title}")

    for line in md.splitlines():
        if line.startswith("## "):
            flush_h2()
            buf = []
            h2_title = line[3:].strip()
        elif line.startswith("# "):
            continue
        else:
            buf.append(line)
    flush_h2()
    return chunks
