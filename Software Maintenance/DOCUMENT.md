# DOCUMENT.md — Project root

## What lives here

Infrastructure and scaffolding for the **Software Maintenance Exam Prep** app — an
offline FastAPI + ChromaDB + bge-small study tool with a Lookup (semantic search)
mode and a Quiz (MCQ) mode. This root holds the Docker/Podman setup, dependency
pins, tooling config, and the top-level docs. Application logic lives in `app/`;
generated content lives in `data/`.

## Files created by Setup (Phase 0)

| File                 | Purpose                                                                 |
|----------------------|-------------------------------------------------------------------------|
| `requirements.txt`   | Pinned runtime/build/test deps. Versions mirror `cyper` for consistency. |
| `Dockerfile`         | Multi-stage `python:3.11-slim`; CPU torch; bge-small baked in; non-root; HF offline env; `/health` HEALTHCHECK. |
| `docker-compose.yml` | `ingest` one-shot profile + long-running `app` service. Standard schema → Podman-compatible. Named `chroma` + `slides` volumes. |
| `.dockerignore`      | Keeps the build context/image lean (excludes caches, PM/, chroma_db, docs). |
| `.env.example`       | Committed template — paths/ports only, no secrets.                       |
| `pyproject.toml`     | Ruff (lint + format) and pytest config. Python 3.11.                    |
| `README.md`          | What the app is, prerequisites, ingest + run with `podman compose`, the two modes, env reference, architecture overview. |
| `.gitignore`         | Pre-existing `PM/`; appended Python + tooling caches + `chroma_db/` + `slides/` + `.env` + OS cruft. |
| `DOCUMENT.md`        | This file.                                                              |

## Directory skeleton (created here, documented in each subdir)

- `app/`, `app/static/`, `app/tests/` — backend, frontend, tests. Contains empty
  `app/__init__.py` and `app/tests/__init__.py` package markers.
- `data/`, `data/guides/`, `data/mcqs/` — generated study guides and MCQ bank.

`Lecture 1/ … Lecture 12/` and `PM/` are **not** owned by Setup and are never
modified.

## Key decisions

- **Mirror `cyper`.** Pinned versions, the bge-small bake-in, the `ingest`-profile
  compose shape, and the lazy-embedder/`no-cache`-middleware app structure all come
  from the proven `ExamPrep/cyper` project so the two offline apps stay consistent.
- **Podman-first.** The compose file uses only standard schema (no Docker-Desktop
  features); the app binds `127.0.0.1:8000` for a single-user, no-auth local tool.
  README documents `podman compose` throughout.
- **Non-root container + HEALTHCHECK.** Improvements over `cyper` (which runs as
  root): a dedicated `appuser`, owned `/data` + `/models`, and a `/health`-based
  healthcheck — per the global project standards.
- **Two data planes.** Guides are embedded into ChromaDB (Lookup); the MCQ bank is
  served from JSON in memory (Quiz). The compose mounts reflect this split.
- **Slot-in safety.** Lectures 8 and 12 (no materials) need no config changes; this
  scaffold makes no assumption about which lecture ids exist.

## How it connects

`Dockerfile` builds one image used by both compose services. `ingest` reads
`data/guides/` (and discovers source PDFs under the read-only repo root) and writes
the `chroma` volume; `app` reads that volume plus `data/mcqs/` and serves the site.
The Backend Engineer fills `app/*.py`; the Frontend Engineer fills `app/static/`;
the content phases fill `data/guides/` and `data/mcqs/`.
