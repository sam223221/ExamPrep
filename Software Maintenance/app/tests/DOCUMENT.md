# DOCUMENT.md — `app/tests/`

## What lives here

The pytest suite for the backend. Discovered via `pyproject.toml`
(`testpaths = ["app/tests"]`, `test_*.py`).

## Current state (implemented)

73 tests across 7 modules, all passing, Ruff-clean. Fixtures are small and
self-contained — no test depends on the real guides/MCQs/PDFs existing.

| File              | Covers                                                                                   | Tests |
|-------------------|------------------------------------------------------------------------------------------|-------|
| `test_lectures.py`| Numeric lecture sort (beats lexical), `L01..L12` ids, deck-title map + fallback, `doc_kind`, closed taxonomy/difficulty, lecture→topic map, empty-lecture handling. | 8 |
| `test_extract.py` | Page markers, de-hyphenation/whitespace normalization, record shape (lecture_id/deck_title/doc_kind), numeric `discover_pdfs` order. | 4 |
| `test_chunker.py` | `chunk_source` page-flush + max_chars split, `chunk_markdown` H2 split + Overview capture, full §2.4 metadata (+`chunk_index`) on every chunk. **Size-bounded cascade:** small section → 1 chunk (no regression); no chunk over the ~450-tok / ~1,800-char budget; H3 sub-chunks carry `"H2 › H3"` title + correct `lecture_id`/`chunk_type`/`page`/`topic`; H2-direct lead-in keeps the bare H2 title; monotonic gap-free `chunk_index`; windowing is lossless (every paragraph survives) and overlaps at seams; an H2 with no H3s windows directly; an over-budget paragraph splits on sentence ends. | 13 |
| `test_ingest.py`  | `guide_lecture_meta` identity paths — `lecture-NN-*` in `L01..L12` carries full lecture identity (id/num/curated title/primary topic); course-level bare-number guides (`00-overview.md`, the `9x` exam series) get NO lecture id + slug title + course-spine topic; out-of-range `lecture-90-*` never mints an id; unconventional filename fallback. Plus a `gather_chunks` tmpdir integration test: metadata lands on chunks (`lecture_id=""` for exam guides → no L-badge) and `DOCUMENT.md` is excluded from the corpus. | 6 |
| `test_validate.py`| `validate_mcqs` gate — one test per violation (bad id, id/lecture mismatch, wrong option count/keys/dupes, bad answer, empty explanation, missing source, out-of-vocab topic/difficulty), cross-file duplicate id + stem, CLI exit codes, empty-dir OK. | 16 |
| `test_quiz.py`    | Empty-dir no-crash, buckets + bank-derived `/api/lectures` topics metadata, lecture/topic/difficulty filtering, **topic-in-`tags` reachability** (FIX 1b), **answer-hygiene** (served payload has no answer/explanation/`source` — FIX 2 — and keeps `tags`), seeded determinism, grading, unknown-id flagged not-crash. | 11 |
| `test_search.py`  | `build_where` (lecture/topic/`$and`), `/search` params + 422 validation, **P1 ANN-recall fix:** `search()` over-fetches `max(24, 4·k)` from Chroma (fake collection records `n_results`), re-sorts by distance, slices to exactly `k`, handles fewer-than-k candidates; `ingest.COLLECTION_METADATA` carries `hnsw:search_ef ≥ 100` + cosine space. `/health`, `/slide` `_slug` + traversal guard + real PNG render + out-of-range 404, `/api/lectures` bank-derived topics, `/api/quiz` topic-only-in-`tags` filter, full quiz flow with no pre-grade `source` + `/api/quiz/check` returning `answer`/`explanation`/`source`, quiz 422/404, malformed-body 422. | 15 |

## Conventions

- Run: `podman compose run --rm app pytest -v` (or `pytest` from the repo root).
- Config lives in `pyproject.toml` under `[tool.pytest.ini_options]`.
- Tests must be offline and deterministic; monkeypatch external resources (the PDF
  map `main._pdf_map`, the in-memory bank `main._bank`, and `main.search`) rather
  than hitting real files/models — mirrors cyper's `test_search.py` approach. The
  embedder and Chroma client are never constructed by the suite.
- `chunk_source`/`chunk_markdown` and the validate helpers take **keyword-only**
  metadata args; fixture dicts (`_SRC_KW`, `_GUIDE_KW`, `_q(...)`) are spread in.

## How it connects

Tests import from the `app` package (first-party). The same image that serves the
app runs the suite, so test deps (`pytest`, `httpx`) are already pinned in
`requirements.txt`.
