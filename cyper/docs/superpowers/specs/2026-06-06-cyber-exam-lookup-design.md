# Design: Cyber Exam Lookup System

**Date:** 2026-06-06
**Status:** Approved (pending spec review)
**Location:** `ExamPrep/cyper/`

## 1. Purpose

Turn a full semester of cybersecurity lecture material (24 PDFs across 12 topics + the
exam paper) into a **local, offline, queryable study tool**. The user types a question in a
searchbar and instantly gets a well-written answer drawn from a curated study guide, plus the
exact source PDF and page. Built for use during an open-book exam: **no internet, no GPU, no
external API**.

### Acceptance criteria
- `docker compose up` serves a working searchbar website at `http://localhost:8000`.
- A natural-language query returns: (a) the best-matching study-guide section rendered as
  readable text, (b) the source PDF + page citation, (c) related chunks ranked by similarity.
- Works fully offline after the image is built (embedding model baked in, no CDN assets).
- The study guide covers all 12 topics at depth: concepts, glossary, how-to cookbook, exam Q&A.

### Out of scope
- No generative LLM at query time (retrieval-only — decided with user).
- No cloud services, no API keys, no authentication, no multi-user support.
- No mobile app; a responsive web page is sufficient.

## 2. Source material

`cyper/` contains 12 numbered topic folders, each with a lecture (`Lxx`) and exercise (`Exx`) PDF:

| # | Topic | # | Topic |
|---|---|---|---|
| 01 | Introduction & Set-up | 07 | Social Engineering |
| 02 | Vulnerability Assessment | 08 | Threat Modeling I |
| 03 | Penetration Testing | 09 | Cryptography |
| 04 | Firewalls & IDS | 10 | Multi-Party Computation |
| 05 | Malware & SQL Injection | 11 | Privacy, Data Protection & GDPR |
| 06 | Denial of Service | 12 | Threat Modeling II + Exam Prep |

Plus `SI5-CS_Cybersecurity_9 June (1).pdf` (exam paper) and `08.../Resources.zip`.

## 3. Architecture

```
24 PDFs ──▶ [1] Extract text ──▶ extracted/*.md  (page numbers kept for citations)
                  │
                  ▼
        [2] 12 parallel agents (one per topic) read lecture+exercise
                  │
                  ▼
        study-guide/*.md  (per-topic guide + how-to cookbook + exam Q&A)
        + overview.md + exam-prep.md (from the real exam paper)
                  │
                  ▼
        [3] Ingest: chunk (source text + guide) ──▶ embed locally ──▶ ChromaDB (persisted)
                  │
                  ▼
        [4] FastAPI + vanilla-JS searchbar ──▶ docker compose up ──▶ localhost:8000
```

### [1] Extraction
- **PyMuPDF (fitz)** extracts text page-by-page from each PDF into `extracted/<topic>/<file>.md`.
- Each page is delimited so chunking can attach a `source_file` + `page` citation.
- Image-only slides extract poorly; any file that yields suspiciously little text is flagged
  and re-run through OCR (Tesseract) as a fallback.

### [2] Study guide (parallel agents)
- One agent per topic (12 total), each reads its extracted lecture + exercise text and writes
  `study-guide/<NN>-<topic>.md` containing:
  - **Concepts explained** — what it is, why it matters, how it works.
  - **Glossary** — key terms and definitions.
  - **How-to cookbook** — practical procedures (e.g. nmap scan, SQLi exploitation, Metasploit
    usage, STRIDE threat model, RSA by hand, configuring a firewall rule).
  - **Exam-style Q&A** — likely questions with worked answers.
  - **Gotchas** — common mistakes and edge cases.
- Two synthesis docs: `overview.md` (how the 12 topics connect) and `exam-prep.md` (derived
  from the actual exam paper).
- Depth target: **maximum useful depth** — full explanations + hands-on cookbook + Q&A, not
  short summaries.

### [3] Vector database
- **Both** the original extracted text **and** the new study guide are chunked and embedded,
  so a search returns curated answers *and* the underlying source.
- Chunking: by section for the guide; by page/paragraph window for source text.
- **Embeddings:** `BAAI/bge-small-en-v1.5` (~130 MB), downloaded at image build time → offline.
- **Store:** **ChromaDB**, embedded + persistent (no separate server), persisted to a volume.
- Each chunk's metadata: `source_file`, `page`, `topic`, `type` (`guide` | `source`), `title`.

### [4] Website
- **Backend:** FastAPI + uvicorn. Endpoint `GET /search?q=...&k=...` embeds the query, queries
  Chroma, returns ranked results with metadata, snippet, rendered markdown, and similarity score.
- **Frontend:** single vanilla HTML/CSS/JS page, keyboard-first searchbar, results list showing
  the best guide answer (markdown → HTML), source citation, and related links. No build step,
  no CDN.
- Served by the same FastAPI app (static files).

## 4. Stack
- Python 3.11, FastAPI, uvicorn
- PyMuPDF (extraction), Tesseract/pytesseract (OCR fallback)
- sentence-transformers + `bge-small-en-v1.5` (embeddings)
- ChromaDB (vector store)
- Vanilla HTML/CSS/JS (frontend)
- Docker + docker-compose

## 5. Offline guarantee
- Embedding model downloaded into the image during build; `HF_HUB_OFFLINE=1` at runtime.
- All frontend assets local (no CDN/Google Fonts).
- ChromaDB persisted to a named volume so ingestion runs once.

## 6. Deliverables (in `cyper/`)
- `extracted/` — extracted text per PDF.
- `study-guide/` — markdown guides (12 topic + overview + exam-prep).
- `app/` — FastAPI backend, frontend, ingestion script.
- `Dockerfile`, `docker-compose.yml`, `README.md`.

## 7. Risks
- **PDF extraction quality** for image-heavy slide decks → OCR fallback mitigates.
- **Study-guide accuracy** — agents must stay grounded in the source, not invent. Each guide
  cites the source pages it draws from; a review pass checks faithfulness.
- **Image size** — embedding model + deps. Acceptable for local use (~1–2 GB).

## 8. Build order
1. Extraction script + run it over all PDFs.
2. Parallel topic agents → study guide + synthesis docs.
3. Ingestion script → ChromaDB.
4. FastAPI backend + frontend.
5. Dockerfile + compose + README.
6. End-to-end test: `docker compose up`, run sample exam queries, verify citations.
