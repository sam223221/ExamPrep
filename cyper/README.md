# Cyber Exam Lookup

Offline semantic search over the cybersecurity course (lecture PDFs + a curated study guide).
Type a question, get the best-matching guide answer plus the exact source PDF and page.
Runs fully local in Docker — no internet, no GPU, no API keys.

## What's inside
- `study-guide/` — curated, exam-focused markdown (12 topics + overview + exam-prep), written
  from the lecture PDFs with inline page citations.
- `app/` — FastAPI backend, vanilla-JS searchbar, PDF extraction + Chroma ingestion.
- `Dockerfile` / `docker-compose.yml` — one image; the embedding model is baked in for offline use.

## Run

Works with **Docker** or **Podman** — the commands are identical, just swap `docker` for
`podman`. (This machine runs Podman; Docker Desktop is installed but its engine is usually
stopped, so the examples below use `podman`.)

1. Make sure the engine is up: `podman ps` (or start Docker Desktop for `docker`).
2. Build the image + ingest all material (one-time; embeds PDFs + study guide into ChromaDB):
   ```
   podman compose --profile ingest run --rm ingest
   ```
3. Start the website:
   ```
   podman compose up -d app
   ```
4. Open **<http://127.0.0.1:8000>** (prefer `127.0.0.1` over `localhost` — on Windows
   `localhost` resolves to IPv6 `::1` first and can stall ~2s per request before falling back
   to IPv4, since the app/podman publish on IPv4 only).

To stop: `podman compose down`. To stop but keep the embedded data: `podman compose stop app`.

## Re-ingest after editing the study guide / adding PDFs
```
podman compose --profile ingest run --rm ingest
podman compose restart app
```
`restart` is enough for **data** changes (the new embeddings live in the `chroma` volume and
the app reconnects on restart).

## After changing app CODE (Python/JS/CSS)
Rebuild the image and **recreate** the container (a plain `restart` keeps the old image):
```
podman compose build app
podman compose up -d --force-recreate app
```

## Slide images
Every **source** (slide/PDF) result shows a "📄 view slide" thumbnail of the actual page —
so diagrams, charts, DFDs, and attack trees that don't survive text extraction are still
visible. Pages are rendered on demand (`GET /slide?file=...&page=...`, PyMuPDF → PNG) and
cached on the `slides` volume, so the first view of a page takes ~1–2s and every later view is
instant. The endpoint only serves files in the indexed PDF set (no path traversal).

## Search filters
The searchbar has filter chips: **All / Q&A / Guide / Slides**. Selecting **Q&A** reveals a
difficulty row (**Any / Easy / Medium / Hard / Very hard**) backed by a bank of ~240 simulated
open-book questions (20 per topic, grounded in the material). Filters map to the API as
`/search?q=...&type=qna&difficulty=hard`.

## Tests
```
podman compose run --rm app pytest -v
```

## How it works
`PDFs → extract.py (PyMuPDF, page-tagged) → chunker.py → embedder.py (bge-small-en-v1.5)
→ ChromaDB (persisted in a volume) ← main.py /search ← browser`

Each search embeds your query locally, runs a cosine-similarity lookup in Chroma, and returns
ranked results: curated **guide** answers (rendered markdown) and **source** chunks with
`file · page` citations.
