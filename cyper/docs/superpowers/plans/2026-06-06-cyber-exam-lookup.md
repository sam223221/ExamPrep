# Cyber Exam Lookup System — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local, offline, GPU-free searchbar website (Docker) that answers cybersecurity exam questions from a curated study guide + the original lecture PDFs, with source-page citations.

**Architecture:** PyMuPDF extracts the 24 PDFs to text inside the container. Parallel agents read the PDFs and write a deep markdown study guide per topic. An ingestion script chunks both the extracted source text and the guide, embeds them with a local `bge-small-en-v1.5` model, and stores them in a persistent ChromaDB. A FastAPI app serves a vanilla-JS searchbar that does semantic search over Chroma and returns rendered answers + citations. Everything runs offline after the image is built.

**Tech Stack:** Python 3.11, FastAPI, uvicorn, PyMuPDF, sentence-transformers (`BAAI/bge-small-en-v1.5`), ChromaDB, vanilla HTML/CSS/JS, Docker + docker-compose.

**Environment notes:**
- Host Python is 3.14 (too new for torch/chroma wheels) — **all ML runs in the Docker image (python:3.11-slim)**. Do not install ML deps on the host.
- Docker Desktop must be running before Tasks 7–8 (the daemon is currently down).
- Tests that need ML deps run **inside the container**: `docker compose run --rm app pytest`.

---

## File Structure

```
cyper/
├── 01..12 topic folders/          # source PDFs (input, unchanged)
├── SI5-CS_Cybersecurity_9 June (1).pdf
├── study-guide/                   # OUTPUT of Task 2 (agent-written markdown)
│   ├── 00-overview.md
│   ├── 01-introduction-setup.md
│   ├── ... (one per topic) ...
│   ├── 12-threat-modeling-2.md
│   └── exam-prep.md
├── app/
│   ├── extract.py                 # PDF -> text with page markers (Task 1)
│   ├── chunker.py                 # text -> chunks with metadata (Task 3)
│   ├── ingest.py                  # extract+chunk+embed -> Chroma (Task 3)
│   ├── main.py                    # FastAPI: /search + static (Task 4)
│   ├── embedder.py                # shared local embedding wrapper (Task 3)
│   ├── requirements.txt
│   ├── static/
│   │   ├── index.html             # searchbar UI (Task 5)
│   │   ├── app.js
│   │   └── style.css
│   └── tests/
│       ├── test_extract.py        # (Task 1)
│       ├── test_chunker.py        # (Task 3)
│       └── test_search.py         # (Task 4)
├── Dockerfile                     # (Task 6)
├── docker-compose.yml             # (Task 6)
├── .dockerignore                  # (Task 0)
└── README.md                      # (Task 7)
```

Data flow: `PDFs → extract.py → chunker.py → embedder.py → ChromaDB (volume) ← main.py ← browser`.

---

## Task 0: Scaffolding

**Files:**
- Create: `app/requirements.txt`, `.dockerignore`, `app/tests/__init__.py`

- [ ] **Step 1: requirements.txt** (pinned, CPU-only torch)

```
fastapi==0.115.6
uvicorn[standard]==0.34.0
pymupdf==1.25.1
chromadb==0.5.23
sentence-transformers==3.3.1
torch==2.5.1
markdown==3.7
pytest==8.3.4
httpx==0.28.1
```

- [ ] **Step 2: .dockerignore** (keep image lean; PDFs are mounted/needed at ingest only)

```
**/__pycache__
**/*.pyc
docs/
.git/
chroma_db/
*.zip
```

- [ ] **Step 3: empty `app/tests/__init__.py`**

- [ ] **Step 4: Commit** — `git add app/requirements.txt .dockerignore app/tests/__init__.py && git commit -m "chore: scaffold cyber lookup app"`

---

## Task 1: PDF extraction (`app/extract.py`)

**Responsibility:** Walk the topic folders, extract each PDF page-by-page to a markdown string with `<!-- page:N -->` markers, return structured records.

**Files:**
- Create: `app/extract.py`, `app/tests/test_extract.py`

- [ ] **Step 1: Write failing test** `app/tests/test_extract.py`

```python
import fitz  # PyMuPDF
from app.extract import extract_pdf, page_marker

def test_page_marker_format():
    assert page_marker(14) == "<!-- page:14 -->"

def test_extract_pdf_returns_pages(tmp_path):
    # build a 2-page PDF with known text
    doc = fitz.open()
    for txt in ("Alpha page one", "Bravo page two"):
        pg = doc.new_page()
        pg.insert_text((72, 72), txt)
    p = tmp_path / "sample.pdf"
    doc.save(p); doc.close()

    rec = extract_pdf(str(p))
    assert rec["n_pages"] == 2
    assert "Alpha page one" in rec["text"]
    assert "<!-- page:1 -->" in rec["text"]
    assert "<!-- page:2 -->" in rec["text"]
```

- [ ] **Step 2: Run test, expect FAIL** — `docker compose run --rm app pytest app/tests/test_extract.py -v` → ModuleNotFoundError/extract not defined. (Until Docker image exists in Task 6, run after Task 6; note this ordering.)

- [ ] **Step 3: Implement `app/extract.py`**

```python
"""Extract text from course PDFs, one record per file, page-delimited."""
from __future__ import annotations
import os
import glob
import fitz  # PyMuPDF


def page_marker(n: int) -> str:
    return f"<!-- page:{n} -->"


def extract_pdf(path: str) -> dict:
    doc = fitz.open(path)
    parts: list[str] = []
    for i, page in enumerate(doc, start=1):
        parts.append(page_marker(i))
        parts.append(page.get_text("text").strip())
    doc.close()
    return {
        "path": path,
        "file": os.path.basename(path),
        "n_pages": len(parts) // 2,
        "text": "\n".join(parts),
    }


def discover_pdfs(root: str) -> list[str]:
    pdfs = glob.glob(os.path.join(root, "**", "*.pdf"), recursive=True)
    return sorted(p for p in pdfs if "docs" not in p.replace("\\", "/").split("/"))


def topic_of(path: str) -> str:
    """Folder name like '06. Denial of Service' -> 'Denial of Service'."""
    parts = path.replace("\\", "/").split("/")
    for seg in parts:
        if seg[:2].isdigit() and "." in seg[:4]:
            return seg.split(".", 1)[1].strip()
    return "General"
```

- [ ] **Step 4: Run test, expect PASS**
- [ ] **Step 5: Commit** — `git commit -am "feat: PDF text extraction with page markers"`

---

## Task 2: Study guide generation (parallel agents) — AGENTIC, not code

**Responsibility:** Produce `study-guide/*.md` — the curated, exam-focused knowledge that makes search answers good. One agent per topic, dispatched in parallel.

**Output files:** `study-guide/00-overview.md`, `study-guide/01-...md` … `study-guide/12-...md`, `study-guide/exam-prep.md`.

- [ ] **Step 1:** Dispatch 12 parallel subagents. Each agent brief:
  > Read the lecture PDF `Lxx...` and exercise PDF `Exx...` in folder `<NN. Topic>` using the Read tool. Write `study-guide/<NN>-<slug>.md` with these sections, grounded ONLY in the PDFs (cite source pages as `(Lxx p.N)`): **## Overview**, **## Key Concepts** (each explained in plain language — what/why/how), **## Glossary**, **## How-To Cookbook** (concrete step-by-step procedures for the practical skills in this topic — commands, tools, worked examples), **## Exam-Style Q&A** (8–15 questions with full answers), **## Gotchas**. Aim for depth and exam usefulness. Do not invent facts not in the material; if unsure, say so.

- [ ] **Step 2:** After topic agents finish, dispatch one synthesis agent for `study-guide/00-overview.md` (how the 12 topics connect, the big picture of the course) and one for `study-guide/exam-prep.md` (read `SI5-CS_Cybersecurity_9 June (1).pdf` + all guides → exam format, likely question types, a study checklist, worked answers to the actual exam questions).

- [ ] **Step 3:** Faithfulness review — dispatch a reviewer agent to spot-check 3 random claims per guide against the cited pages. Fix any hallucinations.

- [ ] **Step 4:** Commit — `git add study-guide && git commit -m "docs: comprehensive cyber study guide"`

---

## Task 3: Chunking + embedding + ingestion

**Files:**
- Create: `app/chunker.py`, `app/embedder.py`, `app/ingest.py`, `app/tests/test_chunker.py`

- [ ] **Step 1: Failing test** `app/tests/test_chunker.py`

```python
from app.chunker import chunk_markdown, chunk_source

def test_chunk_source_attaches_page():
    text = "<!-- page:1 -->\nIntro about firewalls.\n<!-- page:2 -->\nIDS detail here."
    chunks = chunk_source(text, file="L04.pdf", topic="Firewalls & IDS", max_chars=200)
    assert any(c["page"] == 1 for c in chunks)
    assert any(c["page"] == 2 for c in chunks)
    assert all(c["type"] == "source" for c in chunks)
    assert all(c["topic"] == "Firewalls & IDS" for c in chunks)

def test_chunk_markdown_splits_by_heading():
    md = "# T\n## Key Concepts\nA.\n## Glossary\nB."
    chunks = chunk_markdown(md, file="04-firewalls.md", topic="Firewalls & IDS")
    titles = {c["title"] for c in chunks}
    assert "Key Concepts" in titles and "Glossary" in titles
    assert all(c["type"] == "guide" for c in chunks)
```

- [ ] **Step 2: Run, expect FAIL**

- [ ] **Step 3: Implement `app/chunker.py`**

```python
"""Split source text and guide markdown into embeddable chunks with metadata."""
from __future__ import annotations
import re

PAGE_RE = re.compile(r"<!--\s*page:(\d+)\s*-->")


def chunk_source(text: str, file: str, topic: str, max_chars: int = 1000) -> list[dict]:
    """Split page-marked source text into ~max_chars chunks, tagging the page."""
    chunks: list[dict] = []
    cur_page = 1
    buf: list[str] = []

    def flush():
        body = " ".join(buf).strip()
        if body:
            chunks.append({
                "text": body, "file": file, "topic": topic,
                "page": cur_page, "type": "source", "title": topic,
            })

    for line in text.splitlines():
        m = PAGE_RE.search(line)
        if m:
            flush(); buf.clear()
            cur_page = int(m.group(1))
            continue
        buf.append(line)
        if sum(len(x) for x in buf) >= max_chars:
            flush(); buf.clear()
    flush()
    return chunks


def chunk_markdown(md: str, file: str, topic: str) -> list[dict]:
    """Split a study-guide markdown file by ## headings."""
    chunks: list[dict] = []
    title = "Overview"
    buf: list[str] = []

    def flush():
        body = "\n".join(buf).strip()
        if body:
            chunks.append({
                "text": body, "file": file, "topic": topic,
                "page": 0, "type": "guide", "title": title,
            })

    for line in md.splitlines():
        if line.startswith("## "):
            flush(); buf.clear()
            title = line[3:].strip()
        elif line.startswith("# "):
            continue
        else:
            buf.append(line)
    flush()
    return chunks
```

- [ ] **Step 4: Run, expect PASS**

- [ ] **Step 5: Implement `app/embedder.py`**

```python
"""Local sentence-transformers embedder (offline). bge models want a query prefix."""
from __future__ import annotations
from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-en-v1.5"
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


class Embedder:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def embed_docs(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.model.encode(
            QUERY_PREFIX + text, normalize_embeddings=True
        ).tolist()
```

- [ ] **Step 6: Implement `app/ingest.py`**

```python
"""Build the ChromaDB collection from source PDFs + study guide."""
from __future__ import annotations
import glob
import os
import chromadb
from app.extract import extract_pdf, discover_pdfs, topic_of
from app.chunker import chunk_source, chunk_markdown
from app.embedder import Embedder

PDF_ROOT = os.environ.get("PDF_ROOT", "/data/pdfs")
GUIDE_ROOT = os.environ.get("GUIDE_ROOT", "/data/study-guide")
CHROMA_DIR = os.environ.get("CHROMA_DIR", "/data/chroma_db")
COLLECTION = "cyber"


def gather_chunks() -> list[dict]:
    chunks: list[dict] = []
    for pdf in discover_pdfs(PDF_ROOT):
        rec = extract_pdf(pdf)
        chunks += chunk_source(rec["text"], file=rec["file"], topic=topic_of(pdf))
    for md in sorted(glob.glob(os.path.join(GUIDE_ROOT, "*.md"))):
        with open(md, encoding="utf-8") as fh:
            text = fh.read()
        chunks += chunk_markdown(text, file=os.path.basename(md), topic="Study Guide")
    return [c for c in chunks if c["text"].strip()]


def main() -> None:
    chunks = gather_chunks()
    print(f"Embedding {len(chunks)} chunks...")
    emb = Embedder()
    vectors = emb.embed_docs([c["text"] for c in chunks])

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    col = client.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})
    col.add(
        ids=[f"c{i}" for i in range(len(chunks))],
        embeddings=vectors,
        documents=[c["text"] for c in chunks],
        metadatas=[{k: c[k] for k in ("file", "topic", "page", "type", "title")}
                   for c in chunks],
    )
    print(f"Ingested {col.count()} chunks into '{COLLECTION}'.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 7: Commit** — `git commit -am "feat: chunking, local embedder, Chroma ingestion"`

---

## Task 4: FastAPI backend (`app/main.py`)

**Files:**
- Create: `app/main.py`, `app/tests/test_search.py`

- [ ] **Step 1: Failing test** `app/tests/test_search.py` (uses a tiny in-memory collection via monkeypatch-free fixture)

```python
from fastapi.testclient import TestClient
from app import main

def test_search_endpoint_returns_results(monkeypatch):
    # stub the searcher so the test needs no real Chroma/model
    def fake_search(q, k=5):
        return [{"text": "A SYN flood exhausts the TCP backlog.",
                 "file": "L06_DoS.pdf", "page": 14, "topic": "Denial of Service",
                 "type": "source", "title": "Denial of Service", "score": 0.91}]
    monkeypatch.setattr(main, "search", fake_search)
    client = TestClient(main.app)
    r = client.get("/search", params={"q": "syn flood"})
    assert r.status_code == 200
    body = r.json()
    assert body["results"][0]["page"] == 14
    assert "SYN flood" in body["results"][0]["text"]
```

- [ ] **Step 2: Run, expect FAIL**

- [ ] **Step 3: Implement `app/main.py`**

```python
"""FastAPI app: semantic search over the cyber ChromaDB + static frontend."""
from __future__ import annotations
import os
import chromadb
import markdown as md_lib
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.embedder import Embedder

CHROMA_DIR = os.environ.get("CHROMA_DIR", "/data/chroma_db")
COLLECTION = "cyber"

app = FastAPI(title="Cyber Exam Lookup")
_embedder: Embedder | None = None
_collection = None


def _lazy():
    global _embedder, _collection
    if _embedder is None:
        _embedder = Embedder()
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = client.get_collection(COLLECTION)
    return _embedder, _collection


def search(q: str, k: int = 5) -> list[dict]:
    emb, col = _lazy()
    res = col.query(query_embeddings=[emb.embed_query(q)], n_results=k)
    out: list[dict] = []
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        item = dict(meta)
        item["text"] = doc
        item["score"] = round(1 - dist, 3)  # cosine distance -> similarity
        item["html"] = md_lib.markdown(doc) if meta.get("type") == "guide" else None
        out.append(item)
    return out


@app.get("/search")
def search_endpoint(q: str = Query(..., min_length=2), k: int = 5) -> JSONResponse:
    return JSONResponse({"query": q, "results": search(q, k)})


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
```

- [ ] **Step 4: Run, expect PASS**
- [ ] **Step 5: Commit** — `git commit -am "feat: FastAPI search endpoint + static mount"`

---

## Task 5: Frontend (`app/static/`)

**Files:** Create `app/static/index.html`, `app/static/style.css`, `app/static/app.js`

- [ ] **Step 1: `index.html`** — searchbar, results container, no external assets.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Cyber Exam Lookup</title>
  <link rel="stylesheet" href="/style.css" />
</head>
<body>
  <header><h1>🔐 Cyber Exam Lookup</h1>
    <p>Search the course. Offline. Cited.</p></header>
  <main>
    <input id="q" type="search" autofocus placeholder="Ask anything… e.g. how does a SYN flood work?" />
    <div id="status"></div>
    <div id="results"></div>
  </main>
  <script src="/app.js"></script>
</body>
</html>
```

- [ ] **Step 2: `style.css`** — clean dark, readable, system font stack (offline).

```css
:root { --bg:#0f1419; --card:#1a2027; --fg:#e6edf3; --muted:#8b98a5; --accent:#3fb950; }
* { box-sizing: border-box; }
body { margin:0; font-family: ui-sans-serif, system-ui, "Segoe UI", Roboto, sans-serif;
  background:var(--bg); color:var(--fg); }
header { padding:24px; text-align:center; }
header h1 { margin:0 0 4px; } header p { margin:0; color:var(--muted); }
main { max-width:820px; margin:0 auto; padding:0 16px 64px; }
#q { width:100%; padding:14px 16px; font-size:18px; border-radius:10px;
  border:1px solid #2a323c; background:var(--card); color:var(--fg); }
#q:focus { outline:2px solid var(--accent); }
#status { color:var(--muted); margin:10px 2px; min-height:18px; }
.result { background:var(--card); border:1px solid #2a323c; border-radius:12px;
  padding:16px 18px; margin:12px 0; }
.result .meta { font-size:13px; color:var(--muted); margin-bottom:8px;
  display:flex; gap:10px; flex-wrap:wrap; }
.badge { background:#21262d; padding:2px 8px; border-radius:999px; }
.badge.guide { color:var(--accent); } .badge.source { color:#58a6ff; }
.result .body { line-height:1.55; } .result .body p:first-child { margin-top:0; }
.score { margin-left:auto; }
mark { background:#3fb95033; color:inherit; }
```

- [ ] **Step 3: `app.js`** — debounce, fetch `/search`, render results with citation + score.

```javascript
const q = document.getElementById("q");
const results = document.getElementById("results");
const statusEl = document.getElementById("status");
let timer = null;

function escapeHtml(s) {
  return s.replace(/[&<>]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}

function render(data) {
  if (!data.results.length) { results.innerHTML = "<p>No matches.</p>"; return; }
  results.innerHTML = data.results.map(r => {
    const cite = r.type === "guide"
      ? `Study guide · ${escapeHtml(r.title)}`
      : `${escapeHtml(r.file)} · p.${r.page}`;
    const body = r.html ? r.html : `<p>${escapeHtml(r.text)}</p>`;
    return `<div class="result">
      <div class="meta">
        <span class="badge ${r.type}">${r.type}</span>
        <span>${escapeHtml(r.topic)}</span>
        <span>${cite}</span>
        <span class="score">sim ${r.score}</span>
      </div>
      <div class="body">${body}</div>
    </div>`;
  }).join("");
}

async function run() {
  const term = q.value.trim();
  if (term.length < 2) { results.innerHTML = ""; statusEl.textContent = ""; return; }
  statusEl.textContent = "Searching…";
  try {
    const res = await fetch(`/search?q=${encodeURIComponent(term)}&k=6`);
    const data = await res.json();
    statusEl.textContent = `${data.results.length} results for "${term}"`;
    render(data);
  } catch (e) { statusEl.textContent = "Error: " + e.message; }
}

q.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(run, 220); });
q.addEventListener("keydown", e => { if (e.key === "Enter") { clearTimeout(timer); run(); } });
```

- [ ] **Step 4: Commit** — `git commit -am "feat: searchbar frontend"`

---

## Task 6: Docker (model baked in for offline)

**Files:** Create `Dockerfile`, `docker-compose.yml`

- [ ] **Step 1: `Dockerfile`** — install deps, pre-download the embedding model into the image.

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    HF_HOME=/models \
    PDF_ROOT=/data/pdfs \
    GUIDE_ROOT=/data/study-guide \
    CHROMA_DIR=/data/chroma_db

WORKDIR /srv
COPY app/requirements.txt .
RUN pip install --no-cache-dir torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir -r requirements.txt

# Bake the embedding model into the image so runtime is fully offline.
RUN python -c "from sentence_transformers import SentenceTransformer; \
SentenceTransformer('BAAI/bge-small-en-v1.5')"

ENV HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
COPY app ./app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- [ ] **Step 2: `docker-compose.yml`** — mount PDFs + guide read-only, persist Chroma in a volume. `ingest` is a one-shot profile service; `app` serves.

```yaml
services:
  ingest:
    build: .
    profiles: ["ingest"]
    volumes:
      - ./:/data/pdfs:ro
      - ./study-guide:/data/study-guide:ro
      - chroma:/data/chroma_db
    command: ["python", "-m", "app.ingest"]

  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - chroma:/data/chroma_db
    restart: unless-stopped

volumes:
  chroma:
```

- [ ] **Step 3: Commit** — `git commit -am "feat: Dockerfile + compose, offline model baked in"`

---

## Task 7: README

**Files:** Create `README.md`

- [ ] **Step 1:** Write run instructions:

```markdown
# Cyber Exam Lookup

Offline semantic search over the cybersecurity course (lectures + curated study guide).

## Run
1. Start Docker Desktop.
2. Build + ingest (one-time, embeds all material):
   `docker compose --profile ingest run --rm ingest`
3. Start the site:
   `docker compose up -d app`
4. Open http://localhost:8000

## Re-ingest after editing the study guide
`docker compose --profile ingest run --rm ingest && docker compose restart app`

## Tests
`docker compose run --rm app pytest`
```

- [ ] **Step 2: Commit** — `git commit -am "docs: README run instructions"`

---

## Task 8: End-to-end verification

- [ ] **Step 1:** Start Docker Desktop; confirm `docker ps` works.
- [ ] **Step 2:** Build + run tests: `docker compose run --rm app pytest -v` → all pass.
- [ ] **Step 3:** Ingest: `docker compose --profile ingest run --rm ingest` → prints "Ingested N chunks" with N in the thousands.
- [ ] **Step 4:** `docker compose up -d app`; `curl "http://localhost:8000/health"` → `{"status":"ok"}`.
- [ ] **Step 5:** Run 5 real exam-style queries against `/search` (e.g. "STRIDE", "SQL injection union", "RSA key generation", "SYN flood mitigation", "GDPR lawful basis"). Verify each returns a relevant guide answer AND a source citation with a plausible page.
- [ ] **Step 6:** Open the site in a browser, confirm searchbar renders results live.
- [ ] **Step 7:** Commit any fixes.

---

## Self-Review (completed)

- **Spec coverage:** Extraction (T1), parallel-agent guide (T2), Chroma ingest w/ local bge embeddings over source+guide (T3), FastAPI+JS searchbar (T4/T5), offline Docker (T6), README (T7), E2E test incl. citations (T8). ✓
- **Placeholders:** none — all code shown inline.
- **Type consistency:** chunk dicts use the same keys (`text/file/topic/page/type/title`) across chunker → ingest → main → frontend; `search()` adds `score`/`html`. `Embedder.embed_docs/embed_query` names match across ingest and main. ✓
- **Ordering caveat:** Task 1/3 tests depend on the Docker image (Task 6) since ML deps aren't on the host — run those tests after the image builds (noted in T1 Step 2 and T8).
```
