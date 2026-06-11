# DOCUMENT.md — `app/`

## What lives here

The FastAPI backend, the vanilla-JS frontend (`static/`), and the pytest suite
(`tests/`) for the Software Maintenance Exam Prep app.

## Current state (Backend implemented)

All backend modules below are implemented, Ruff-clean, and covered by the pytest
suite in `tests/`. They are **owned by the Backend Engineer**.

| File              | Purpose                                                                 | Key exports |
|-------------------|-------------------------------------------------------------------------|-------------|
| `__init__.py`     | Empty package marker.                                                    | — |
| `main.py`         | FastAPI app: `/health`, `/search`, `/slide`, `/api/lectures`, `/api/quiz`, `/api/quiz/check`, static mount last. `search()` over-fetches `max(24, 4·k)` candidates from Chroma, re-sorts by distance, and slices to `k` (P1 ANN-recall fix). | `app`, `search`, `build_where`, `render_slide`, `_pdf_map`, `_bank`, `OVERFETCH_MIN`, `OVERFETCH_FACTOR` |
| `lectures.py`     | Lecture-id helpers (`L01`..`L12`), **numeric** sort, curated deck-title map, lecture→topic/title maps, the closed 16-topic taxonomy + 4-level difficulty vocab. | `lecture_num_of`, `lecture_id_of`, `numeric_lecture_sort`, `deck_title_of`, `doc_kind_of`, `TOPICS`, `TOPIC_SET`, `DIFFICULTIES`, `LECTURE_TOPICS` |
| `extract.py`      | PyMuPDF extraction, `<!-- page:N -->` markers, whitespace/de-hyphen normalization, `doc_kind` classification, **numeric** discovery. | `extract_pdf`, `discover_pdfs`, `normalize_text`, `page_marker` |
| `chunker.py`      | `chunk_source` (~1000-char, page-flush, `source`) and `chunk_markdown` (`## ` H2 split, `guide`) carrying §2.4 metadata + a stable per-doc `chunk_index`. `chunk_markdown` is **size-bounded**: any H2 over `GUIDE_CHUNK_BUDGET_TOKENS` (~450 tok / ~1,800 chars) cascades to `### ` H3 split → paragraph windowing (~1-para overlap, never mid-sentence) so no chunk exceeds the bge-small window. H3-derived sub-chunks get a `"H2 › H3"` title. cyper's `qna`/`cmd` dropped. | `chunk_source`, `chunk_markdown`, `est_tokens`, `GUIDE_CHUNK_BUDGET_TOKENS`, `TITLE_SEPARATOR` |
| `embedder.py`     | `bge-small-en-v1.5` wrapper (cyper-identical: query prefix + `normalize_embeddings`). | `Embedder`, `MODEL_NAME`, `QUERY_PREFIX` |
| `ingest.py`       | Builds the single `software_maintenance` Chroma collection (`COLLECTION_METADATA`: `hnsw:space=cosine` + `hnsw:search_ef=200`, the P1 recall fix — chromadb 0.5.x defaults `search_ef` to 10, at which HNSW missed near neighbours on the ~2k-chunk corpus) from `data/guides/*.md` via `chunk_markdown`, numerically sorted, idempotent (delete-then-create), ids `c{i}` over the flattened chunk list (globally unique even though a guide now yields many chunks per H2). Persists `chunk_index` in metadata. Excludes `DOCUMENT.md`/`README.md`. MCQs NOT embedded. **Guide identity rule:** only `lecture-NN-*` guides with NN in the canonical `L01..L12` range carry a lecture id; bare-number course-level guides (`00-overview.md`, the `9x` exam-prep series `90-exam-*.md`…) get an empty `lecture_id` (no L-badge in Lookup), a slug-derived `deck_title`, and the course-spine topic. | `gather_chunks`, `guide_lecture_meta`, `main`, `COLLECTION`, `COLLECTION_METADATA` |
| `quiz.py`         | Loads/validates the MCQ bank into memory, pre-buckets by lecture/difficulty, seeded filter+sample, reshuffles options, strips `answer`/`explanation`/`source`, grades. Topic filter matches `topic` OR `tags`; `/api/lectures` topics are bank-derived. Never crashes on an empty/missing bank. | `QuizBank`, `_question_topics`, `_topic_matches` |
| `validate_mcqs.py`| Build-time gate (CI-usable, exits non-zero on any violation): schema, 4 options A–D, one answer, non-empty explanation, source.deck/page, closed topic/difficulty vocab, unique well-formed ids, no duplicate stems within/across lectures. | `validate_question`, `validate_file`, `validate_bank`, `main` |

## Files

- `static/` — frontend assets (Frontend Engineer; see `static/DOCUMENT.md`).
- `tests/` — pytest suite, 73 tests, all passing (see `tests/DOCUMENT.md`).

## Key decisions

- **Module shape mirrors `cyper`.** `main.py` uses a lazy embedder/collection, a
  `no-cache` shell middleware, and mounts `app/static` last — the proven cyper
  structure. `embedder.py` is cyper-identical.
- **Numeric lecture sort is enforced.** Folder names (`Lecture 1`, `Lecture 10`, …)
  mis-sort lexically; `lectures.numeric_lecture_sort` orders by the parsed integer
  and threads the canonical `L01…L12` id everywhere (verified live: discovery yields
  1,2,3,…7,9,10,11 with the empty Lecture 8 skipped). Architecture §2.1 — highest
  correctness item.
- **Search corpus = guides only.** `ingest.py` embeds guide chunks
  (`chunk_type=guide`, page 0); MCQs are served from JSON by `quiz.py`, not embedded.
  `DOCUMENT.md`/`README.md` are excluded so engineering notes never pollute the index.
- **Course-level guides carry no lecture identity (2026-06-10).** `guide_lecture_meta`
  grants a lecture id only to `lecture-NN-*` guides with NN in the canonical
  `L01..L12` range. Bare-number guides — `00-overview.md` and the `9x` exam-prep
  series (`90-exam-what-to-expect.md`, `91-exam-model-answers.md`,
  `92-exam-copy-paste-library.md`) — take the no-lecture path: empty `lecture_id`
  (so Lookup renders no L-badge), a slug-derived `deck_title` ("Exam Model Answers" …),
  and the `Software Change Process` topic so they stay searchable. Before this rule the
  `9x` files minted bogus `L90/L91/L92` ids with "Lecture 90" titles.
- **Size-bounded guide chunking (embedding-recall fix).** After the guides were
  deepened (~doubled), the old "one chunk per `## ` H2" rule produced sections up to
  ~24,700 est-tokens — far past the bge-small ~512-token window, so the embedder
  silently truncated each section to its first concept and deep-content recall
  collapsed. `chunk_markdown` now caps every chunk at `GUIDE_CHUNK_BUDGET_TOKENS`
  (~450 tok / ~1,800 chars, `len/4` token estimate, dependency-free) via the cascade
  H2 → `### ` H3 → paragraph windowing (~1-para overlap at seams, never mid-sentence;
  an over-budget paragraph splits on sentence ends). Stored markdown and H2 headers
  are untouched — this only changes how text is split **for the index**. Small
  sections still emit as one chunk (no regression). Over the real guides this took the
  corpus from **107 chunks (max ~24,700 tok)** to **771 chunks (max 450 est-tok, 0 over
  budget)**. **A re-ingest is required** for the live app to pick up the new chunks:
  `podman compose --profile ingest run --rm ingest`.
- **ANN-recall fix at small k (P1, 2026-06-10).** The App Tester reproduced
  deterministic recall loss at the UI's `k=6`: the true #1 hit (sim 0.794) was
  absent from the six results while `k=20` returned it at rank 1. Root cause:
  chromadb 0.5.x defaults the HNSW query-time exploration breadth
  (`hnsw:search_ef`) to **10**, and the effective `ef` is `max(search_ef,
  n_results)` — so `n_results=6` under-explored the grown 1,956-chunk graph.
  Two-layer fix, API contract unchanged (`/search` still returns exactly `k`
  results, best first): (1) `ingest.py` builds the collection with
  `hnsw:search_ef=200` (near-exhaustive on ~2k vectors, still sub-millisecond) —
  **requires a re-ingest** to take effect; (2) `main.search()` over-fetches
  `max(OVERFETCH_MIN=24, OVERFETCH_FACTOR=4 · k)` candidates, re-sorts by raw
  distance, and slices to `k` (defense in depth — also protects an older index
  mounted without the metadata). Verified live post-fix: the 0.794 chunk ranks
  #1 at `k=6`.
- **Answer hygiene (the one app-specific security item, §9).** `/api/quiz` strips
  `answer`+`explanation`+`source` and reshuffles options server-side; `/api/quiz/check`
  is the sole grading authority. `source` (deck + page) is withheld pre-grade because
  it points at the exact slide — leaking it would let a user open `/slide` and read the
  answer before submitting. Verified end-to-end (incl. the real 2,337-question bank):
  the served quiz payload contains no `answer`/`explanation`/`source`; `/api/quiz/check`
  returns all three for post-grade citations.
- **Topic-filter coherence (MCQ bank was tagged inconsistently by parallel authors).**
  `/api/lectures` reports each lecture's `topics` as the **sorted, distinct set of
  closed-taxonomy topics actually present** among its questions — each question's
  `topic` plus any taxonomy topics in its `tags` (granular non-taxonomy tags like
  `grep`/`gof` are excluded). The `/api/quiz` topic filter matches a question when
  `topic == q.topic` **OR** `topic in q.tags`. Together these guarantee every offered
  chip has ≥1 matching question (no spurious 404s) and cross-cutting tagged questions
  are reachable. The closed taxonomy constant and the MCQ JSON are unchanged.
- **`L01..L12` is the single join key.** Derived once in `lectures.py` and shared by
  guides, MCQs, and Chroma metadata. The closed 16-topic taxonomy + 4-level difficulty
  vocab live there too and are enforced at the API boundary and by `validate_mcqs.py`.
- **Defensive boot.** The MCQ bank loads once at import; a missing/empty `data/mcqs/`
  or a malformed file never crashes startup (invalid questions are skipped, surfaced
  in `QuizBank.load_errors`). Quiz mode is instant — the embedder is lazy, so only the
  first `/search` pays model-load cost.

## How it connects

The image's `CMD` runs `uvicorn app.main:app`; the `ingest` service runs
`python -m app.ingest`. `main.py` imports `embedder`, `extract`, `lectures`, `quiz`
and serves `static/`. `quiz.py` and `validate_mcqs.py` share the schema rules.
Run paths and env vars (`GUIDE_ROOT`, `PDF_ROOT`, `MCQ_ROOT`, `CHROMA_DIR`,
`SLIDES_DIR`, optional `STATIC_DIR`) are wired in `docker-compose.yml`.

## API contract (frozen — architecture §5.5)

| Method | Path | Notes |
|---|---|---|
| GET  | `/health` | `{status:"ok"}` |
| GET  | `/search` | `q`(≥2), `k`(default 6, ≤20), `lecture`(`^L\d{2}$\|^all$`), `topic`(closed vocab). 422 on bad params. |
| GET  | `/slide`  | `file`(basename), `page`(≥1). Renders PNG, disk-cached, traversal-guarded. 404 unknown file/out-of-range. |
| GET  | `/api/lectures` | `[{lecture_id,lecture_num,title,topics,counts.by_difficulty}]` from the loaded bank. `topics` = sorted distinct taxonomy topics actually present in the lecture's questions (from `topic` + `tags`). |
| GET  | `/api/quiz` | `lecture?`,`topic?`,`difficulty?`,`n`(default 20, ≤100),`seed?`. Topic matches `q.topic` OR `topic in q.tags`. `answer`/`explanation`/`source` stripped, options reshuffled. 422 bad filter, 404 no match. |
| POST | `/api/quiz/check` | body `{answers:[{id,chosen}]}` → `{score,total,results:[{id,correct,answer,explanation,source}]}`. Unknown ids flagged, never 500. |

## Testing

Run `pytest` from the project root (or `podman compose run --rm app pytest`).
Tests are offline/deterministic and monkeypatch heavy resources (Chroma, the
embedder, the PDF map, the in-memory bank) — they never load the model or hit the
real vector store.
