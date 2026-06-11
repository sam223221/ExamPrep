"""Build the ``software_maintenance`` ChromaDB collection from the study guides.

Architecture §5.3/§5.4: the embedded corpus is the study guides ONLY. MCQs are not
embedded — they are validated by ``validate_mcqs.py`` and served from JSON by
``quiz.py``. Source PDF chunks are built (for slide-render page mapping) but not
embedded by default.

The build is idempotent (delete-then-create on every run, cyper-style) so re-ingest
after editing a guide is one command:

    podman compose --profile ingest run --rm ingest

Env vars: ``GUIDE_ROOT``, ``PDF_ROOT``, ``CHROMA_DIR``, ``MCQ_ROOT`` (the last is read
only to surface bank presence in the build log — it is not embedded here).
"""

from __future__ import annotations

import glob
import os
import re

import chromadb

from app.chunker import chunk_markdown
from app.embedder import Embedder
from app.lectures import (
    lecture_id_from_num,
    lecture_title_of,
    numeric_lecture_sort,
    topics_for_lecture,
)

GUIDE_ROOT = os.environ.get("GUIDE_ROOT", "/data/guides")
PDF_ROOT = os.environ.get("PDF_ROOT", "/data/pdfs")
CHROMA_DIR = os.environ.get("CHROMA_DIR", "/data/chroma_db")
MCQ_ROOT = os.environ.get("MCQ_ROOT", "/data/mcqs")
COLLECTION = "software_maintenance"

#: Collection-level HNSW config (P1 recall fix, 2026-06-10). ``hnsw:search_ef``
#: is the query-time exploration breadth; chromadb 0.5.x defaults it to 10, at
#: which HNSW deterministically missed higher-similarity chunks at the UI's
#: k=6 on the grown ~2k-chunk collection (App Tester P1 — the true #1 hit was
#: absent from the six returned). 200 on ~2k vectors is near-exhaustive and
#: still sub-millisecond; ``main.search`` additionally over-fetches + re-sorts.
COLLECTION_METADATA = {"hnsw:space": "cosine", "hnsw:search_ef": 200}

#: Metadata keys persisted to Chroma (all scalar — Chroma rejects lists/None).
_META_KEYS = (
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
)

# ``lecture-04-refactoring.md`` -> ('lecture-', '04', 'refactoring');
# ``00-overview.md`` / ``91-exam-model-answers.md`` -> (None, '00'/'91', slug).
_GUIDE_NAME_RE = re.compile(r"^(lecture-)?(\d{2})-(.+)$")

#: Canonical lecture-number range (``L01``..``L12``, conventions §"Lecture identity").
#: A numbered guide outside this range never mints a lecture id.
_LECTURE_NUM_MIN, _LECTURE_NUM_MAX = 1, 12


def guide_lecture_meta(path: str) -> tuple[str | None, int, str, str]:
    """Derive ``(lecture_id, lecture_num, deck_title, primary_topic)`` from a guide path.

    Only ``lecture-NN-*`` guides with ``NN`` in the canonical ``L01``..``L12`` range
    carry lecture identity. Bare-number course-level guides — the ``00`` overview/
    appendix and the ``9x`` exam-prep series (``90-exam-*.md`` …) — take the
    no-lecture path: empty ``lecture_id`` (so Lookup renders no L-badge), a
    slug-derived title, and the course-spine topic so they are still searchable.
    """
    stem = os.path.basename(path).rsplit(".", 1)[0]
    m = _GUIDE_NAME_RE.match(stem)
    if not m:
        # Unconventional filename: treat as a non-lecture guide.
        title = stem.replace("-", " ").title()
        return None, 0, title, "Software Change Process"
    is_lecture_file = m.group(1) is not None
    num = int(m.group(2))
    slug = m.group(3)
    title = slug.replace("-", " ").title()
    if not is_lecture_file or not (_LECTURE_NUM_MIN <= num <= _LECTURE_NUM_MAX):
        return None, 0, title or "Course Overview", "Software Change Process"
    lecture_id = lecture_id_from_num(num)
    topics = topics_for_lecture(lecture_id)
    primary_topic = topics[0] if topics else "Software Change Process"
    deck_title = lecture_title_of(lecture_id) or title
    return lecture_id, num, deck_title, primary_topic


# Engineering scaffolding that must never enter the searchable corpus.
_EXCLUDE_GUIDE_FILES = {"document.md", "readme.md"}


def gather_chunks() -> list[dict]:
    """Collect size-bounded guide chunks across ``data/guides/*.md`` in lecture order.

    ``chunk_markdown`` splits on ``##`` H2 headings and further sub-splits any section
    over the embedding budget (see ``chunker.py``), so a single guide may yield several
    chunks per H2; ``main`` assigns a globally unique ``c{i}`` id over the flattened
    list. ``DOCUMENT.md``/``README.md`` are excluded so engineering notes never pollute
    the index — only authored study guides (``00-overview.md``, ``lecture-NN-*.md``) embed.
    """
    md_paths = numeric_lecture_sort(
        [
            p
            for p in glob.glob(os.path.join(GUIDE_ROOT, "*.md"))
            if os.path.basename(p).lower() not in _EXCLUDE_GUIDE_FILES
        ]
    )
    chunks: list[dict] = []
    for md in md_paths:
        with open(md, encoding="utf-8") as fh:
            text = fh.read()
        lecture_id, num, deck_title, topic = guide_lecture_meta(md)
        chunks += chunk_markdown(
            text,
            lecture_id=lecture_id or "",
            lecture_num=num,
            deck_title=deck_title,
            topic=topic,
            source_pdf="",
            doc_kind="deck",
        )
    return [c for c in chunks if c["text"].strip()]


def _scalar_meta(chunk: dict) -> dict:
    """Project a chunk to Chroma-safe scalar metadata (Chroma forbids ``None``)."""
    meta: dict[str, str | int | float | bool] = {}
    for k in _META_KEYS:
        v = chunk.get(k)
        meta[k] = "" if v is None else v
    return meta


def main() -> None:
    chunks = gather_chunks()
    if not chunks:
        # No guides authored yet (Phase A not landed). Build an empty collection so
        # the app starts cleanly and re-ingest after authoring is one command.
        print(
            f"No guide chunks found under {GUIDE_ROOT!r}. "
            "Creating an empty collection (author guides, then re-run ingest)."
        )

    n_mcq_files = len(glob.glob(os.path.join(MCQ_ROOT, "*.json")))
    print(
        f"Gathered {len(chunks)} guide chunks. "
        f"MCQ bank: {n_mcq_files} file(s) under {MCQ_ROOT!r} (validated/served separately, not embedded)."
    )

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    col = client.create_collection(COLLECTION, metadata=COLLECTION_METADATA)

    if chunks:
        emb = Embedder()
        print(f"Embedding {len(chunks)} chunks with {emb.model.__class__.__name__}...")
        vectors = emb.embed_docs([c["text"] for c in chunks])
        col.add(
            ids=[f"c{i}" for i in range(len(chunks))],
            embeddings=vectors,
            documents=[c["text"] for c in chunks],
            metadatas=[_scalar_meta(c) for c in chunks],
        )

    print(f"Ingested {col.count()} chunks into '{COLLECTION}'.")


if __name__ == "__main__":
    main()
