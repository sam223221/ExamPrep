"""Extract text from course PDFs, one record per file, page-delimited.

Adapted from cyper's ``extract.py``. Two project-specific changes:
  1. Discovery sorts lectures **numerically** (cyper used a lexical ``sorted()``
     which mis-orders the non-zero-padded ``Lecture 1``..``Lecture 12`` folders).
  2. Each record carries the canonical ``lecture_id``, curated ``deck_title``, and
     ``doc_kind`` so guides can weight decks over labs and citations read correctly.

Text is normalized (whitespace collapsed, line-break hyphenation rejoined, stray
control characters stripped) to improve embedding quality and guide readability.
"""

from __future__ import annotations

import glob
import os
import re

import fitz  # PyMuPDF

from app.lectures import deck_title_of, doc_kind_of, lecture_id_of, numeric_lecture_sort

# Hyphenated word split across a line break: ``foo-\nbar`` -> ``foobar``.
_DEHYPHEN_RE = re.compile(r"(\w)-\n(\w)")
# Runs of horizontal whitespace (not newlines) collapse to a single space.
_HSPACE_RE = re.compile(r"[ \t ]+")
# Three or more newlines collapse to two (preserve paragraph breaks).
_VSPACE_RE = re.compile(r"\n{3,}")
# Control characters except tab/newline/carriage-return.
_CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def page_marker(n: int) -> str:
    """The inline marker the chunker uses to attach a page number to a chunk."""
    return f"<!-- page:{n} -->"


def normalize_text(text: str) -> str:
    """Clean extracted page text without disturbing meaningful structure.

    Danish characters in the PDF text layer are valid UTF-8 and left untouched
    (the mojibake noted in overview.md is a console artifact only). We only strip
    stray control characters, rejoin hyphenated line breaks, and collapse runs of
    whitespace.
    """
    text = _CTRL_RE.sub("", text)
    text = _DEHYPHEN_RE.sub(r"\1\2", text)
    text = _HSPACE_RE.sub(" ", text)
    text = _VSPACE_RE.sub("\n\n", text)
    return text.strip()


def extract_pdf(path: str) -> dict:
    """Extract one PDF into a single page-delimited record.

    Returns ``{path, file, lecture_id, deck_title, doc_kind, n_pages, text}``.
    A ``<!-- page:N -->`` marker precedes each page's text so the chunker can map
    every chunk back to a real PDF page (and the ``/slide`` endpoint can render it).
    """
    file = os.path.basename(path)
    doc = fitz.open(path)
    parts: list[str] = []
    n_pages = 0
    try:
        for i, page in enumerate(doc, start=1):
            n_pages = i
            parts.append(page_marker(i))
            parts.append(normalize_text(page.get_text("text")))
    finally:
        doc.close()
    return {
        "path": path,
        "file": file,
        "lecture_id": lecture_id_of(path),
        "deck_title": deck_title_of(file),
        "doc_kind": doc_kind_of(file),
        "n_pages": n_pages,
        "text": "\n".join(parts),
    }


def discover_pdfs(root: str) -> list[str]:
    """Find every source PDF under ``root`` and return them in numeric lecture order.

    Mirrors cyper's recursive glob but **overrides the sort**: paths are ordered by
    integer lecture number (then basename) via ``numeric_lecture_sort`` rather than
    lexically. Skips VCS/build noise directories.
    """
    pdfs = glob.glob(os.path.join(root, "**", "*.pdf"), recursive=True)
    skip = {".git", "__pycache__", "chroma_db", "slides", "node_modules"}
    kept = [p for p in pdfs if not (skip & set(p.replace("\\", "/").split("/")))]
    return numeric_lecture_sort(kept)
