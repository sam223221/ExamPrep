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
4. Open <http://localhost:8000>

To stop: `podman compose down`. To stop but keep the embedded data: `podman compose stop app`.

## Re-ingest after editing the study guide
```
podman compose --profile ingest run --rm ingest
podman compose restart app
```

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
