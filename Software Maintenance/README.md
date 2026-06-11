# Software Maintenance Exam Prep (SB5-MAI)

Offline study-prep web app for the **Software Maintenance** course. It turns the
course slide PDFs into per-lecture study guides and a quality-first MCQ bank, then
serves them through a single local website with **two modes**:

- **Lookup** — semantic search over the study guides (type a question, get the
  best-matching guide section plus the exact source deck and page).
- **Quiz** — interactive practice: filter MCQs by lecture / topic / difficulty,
  answer, then grade with explanations and citations.

Runs fully local under Podman (or Docker) — no internet, no GPU, no API keys.
The embedding model (`BAAI/bge-small-en-v1.5`) is baked into the image and the
container runs with Hugging Face offline flags set.

> Reuses the proven `ExamPrep/cyper` pattern (FastAPI + ChromaDB + bge-small).

---

## Prerequisites

- **Podman** (this machine's engine) or Docker — commands are identical, just swap
  `podman` for `docker`.
- The compose file uses standard schema only, so `podman compose` works directly.
- No other tooling required on the host; everything runs in the container.

Check the engine is up:

```
podman ps
```

---

## Two modes, two data sources

| Mode   | Endpoint(s)                              | Backed by                          |
|--------|------------------------------------------|------------------------------------|
| Lookup | `GET /search`                            | ChromaDB index over `data/guides/` |
| Quiz   | `GET /api/quiz`, `POST /api/quiz/check`  | MCQ JSON bank in `data/mcqs/`      |

The study guides are embedded into ChromaDB by the `ingest` step. The MCQ bank is
**not** embedded — it is loaded into memory at app startup and filtered exactly by
lecture / topic / difficulty.

---

## Setup & run

### 1. (Optional) local env file

```
cp .env.example .env
```

The app needs no secrets. `.env` only documents paths/ports and is gitignored.
Inside containers the paths are already set by the image/compose file, so this
step matters mainly when running outside a container.

### 2. Build the image + ingest (one-time, and after editing guides)

This builds the ChromaDB collection from the study guides into the `chroma` volume:

```
podman compose --profile ingest run --rm ingest
```

### 3. Start the website

```
podman compose up -d app
```

Open **<http://127.0.0.1:8000>**.

> Prefer `127.0.0.1` over `localhost` — on Windows `localhost` resolves to IPv6
> `::1` first and can stall ~2s per request before falling back to IPv4, since the
> app publishes on IPv4 only.

To stop: `podman compose down`. To stop but keep the embedded data:
`podman compose stop app`.

### Re-ingest after editing a study guide / adding a lecture

```
podman compose --profile ingest run --rm ingest
podman compose restart app
```

`restart` is enough for **data** changes — the new embeddings live in the `chroma`
volume and the app reconnects on restart. (Editing the MCQ bank only needs a
`restart`, since the bank is loaded at startup.)

### After changing app CODE (Python / JS / CSS)

Rebuild the image and **recreate** the container (a plain `restart` keeps the old
image):

```
podman compose build app
podman compose up -d --force-recreate app
```

> **If the code change affects ingest output** (e.g. editing the chunker, the
> guide loader, or `embedder.py`), a rebuilt `app` image is **not** enough — you
> must also force-rebuild the `ingest` image and re-ingest. Both services share
> one Dockerfile that bakes `app/` into the image, and `podman compose build` can
> reuse a **cached** `app/` layer, so a plain rebuild may silently re-ingest with
> stale code. Force the layer to bust and re-ingest:
>
> ```
> podman compose build --no-cache ingest    # or `--no-cache` (no service) to refresh app + ingest
> podman compose --profile ingest run --rm ingest
> podman compose up -d --force-recreate app
> ```
>
> After a `--no-cache` build both images dedupe to the current code.

### Tests

```
podman compose run --rm app pytest -v
```

Lint / format (Ruff, config in `pyproject.toml`):

```
podman compose run --rm app ruff check app
podman compose run --rm app ruff format --check app
```

### Troubleshooting

- **Ingest reports an unexpected / old chunk count** (expected is **~771** guide
  chunks): the `ingest` image layer is stale — `app/` is baked in at build time and
  a cached layer re-ingested with old code. Rebuild with `--no-cache` and re-ingest:

  ```
  podman compose build --no-cache ingest
  podman compose --profile ingest run --rm ingest
  podman compose up -d --force-recreate app
  ```

---

## Environment variables

All paths default to in-container locations; override only when running on the host.

| Variable     | Default (host `.env`) | In container     | Purpose                                                        |
|--------------|-----------------------|------------------|----------------------------------------------------------------|
| `PDF_ROOT`   | `./`                  | `/data/pdfs`     | Root holding the source `Lecture N/` slide PDFs (read-only).   |
| `GUIDE_ROOT` | `./data/guides`       | `/data/guides`   | Per-lecture study-guide markdown — the embedded search corpus. |
| `MCQ_ROOT`   | `./data/mcqs`         | `/data/mcqs`     | Per-lecture MCQ JSON files — the quiz bank.                    |
| `CHROMA_DIR` | `./data/chroma_db`    | `/data/chroma_db`| Persisted ChromaDB vector store (built by `ingest`).           |
| `SLIDES_DIR` | (n/a on host)         | `/data/slides`   | Disk cache for rendered slide PNGs.                            |
| `PORT`       | `8000`                | `8000`           | HTTP port the app listens on.                                 |

The Hugging Face offline flags (`HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`) and
the model cache (`HF_HOME=/models`) are set in the image, not in `.env`.

---

## Architecture overview

```
Source PDFs (Lecture N/)                data/guides/*.md          data/mcqs/*.json
        │                                      │                         │
        │  extract.py (PyMuPDF, page-tagged)   │  chunk_markdown (## H2)  │  load + validate
        ▼                                      ▼                         ▼
  /slide  (render a page → PNG, cached)   ingest.py → embedder.py    quiz bank (in memory)
                                          (bge-small-en-v1.5)
                                               │                         │
                                               ▼                         │
                                          ChromaDB  ───────► /search ◄────┤
                                          (cosine, persisted)            │
                                                                         ▼
   Browser  ◄──  app/static (index.html · style.css · common.js · lookup.js · quiz.js)
            └─ Lookup: /search          └─ Quiz: /api/lectures, /api/quiz, /api/quiz/check
```

- **Lecture ids** are canonical zero-padded `L01…L12`. Lectures are sorted
  **numerically** everywhere (the folder names are non-padded — `Lecture 1`,
  `Lecture 10`, … — so a lexical sort mis-orders them). This is the single join
  key across guides, MCQs, and Chroma metadata.
- **Single ChromaDB collection** `software_maintenance` with cosine space; filters
  are `where` clauses on metadata (lecture / topic), not separate collections.
- **Answer hygiene:** the quiz endpoints withhold the correct answer and
  explanation until grading at `POST /api/quiz/check`, so answers never ship to the
  browser early.
- **Offline + security:** local-only, no auth, no secrets; markdown is rendered
  then sanitized with a `bleach` allowlist; `/slide` only serves PDFs in the
  discovered set (no path traversal); all dependency versions are pinned and the
  model is baked in.

See `PM/architecture.md` for the full design (ingest pipeline, guide template, MCQ
schema, API contract, edge cases, security, performance, trade-offs).

---

## Project layout

```
Software Maintenance/
├── Lecture 1/ … Lecture 12/   # SOURCE slide PDFs — read-only, never modified
├── app/                       # FastAPI backend + vanilla-JS frontend + tests
│   ├── static/                # index.html, style.css, common.js, lookup.js, quiz.js
│   └── tests/                 # pytest suite
├── data/
│   ├── guides/                # per-lecture study-guide markdown (embedded corpus)
│   └── mcqs/                  # per-lecture MCQ JSON (quiz bank)
├── Dockerfile                 # python:3.11-slim, CPU torch, bge baked in, non-root
├── docker-compose.yml         # `ingest` profile + `app` service (Podman-compatible)
├── requirements.txt           # pinned deps (mirrors cyper)
├── pyproject.toml             # Ruff + pytest config (Python 3.11)
├── .env.example               # paths/ports (no secrets)
└── README.md
```

> **Lectures 8 and 12** currently have no materials. Numeric discovery simply skips
> absent ids — no guide/MCQ is produced and the UI shows no chip for them. They slot
> in later by adding the files and re-ingesting, with zero code changes.
