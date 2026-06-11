"""FastAPI app — semantic Lookup over guides + interactive Quiz over the MCQ bank.

Implements the FROZEN architecture §5.5 contract exactly:

    GET  /health                liveness
    GET  /search                semantic lookup over guide chunks
    GET  /slide                 render a source slide page to PNG (cached, traversal-guarded)
    GET  /api/lectures          quiz/lookup filter metadata (computed from the loaded bank)
    GET  /api/quiz              fetch a quiz set (answers stripped, options reshuffled)
    POST /api/quiz/check        grade answers + reveal explanations

Structural choices mirror cyper: a lazily-loaded embedder/collection (so Quiz mode
and ``/health`` are instant before the model warms), a ``no-cache`` shell middleware,
bleach-sanitized rendered markdown, and the static mount LAST so API routes win.
"""

from __future__ import annotations

import os
import re
from urllib.parse import quote

import bleach
import chromadb
import fitz  # PyMuPDF — render slide pages to PNG on demand
import markdown as md_lib
from fastapi import Body, FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from app.embedder import Embedder
from app.extract import discover_pdfs
from app.lectures import DIFFICULTY_SET, TOPIC_SET
from app.quiz import QuizBank

CHROMA_DIR = os.environ.get("CHROMA_DIR", "/data/chroma_db")
PDF_ROOT = os.environ.get("PDF_ROOT", "/data/pdfs")
SLIDES_DIR = os.environ.get("SLIDES_DIR", "/data/slides")
MCQ_ROOT = os.environ.get("MCQ_ROOT", "/data/mcqs")
STATIC_DIR = os.environ.get("STATIC_DIR", "app/static")
SLIDE_ZOOM = 2.0  # ~144 DPI: readable diagrams/text without huge files
COLLECTION = "software_maintenance"

# Validation bounds (architecture §9).
LECTURE_RE = re.compile(r"^L\d{2}$|^all$")
MAX_K = 20
MAX_N = 100

# ANN recall guard (P1 fix, 2026-06-10): at small ``n_results`` Chroma's HNSW
# search under-explores the grown collection (1,956 chunks) and deterministically
# drops higher-similarity chunks — reproduced at the UI's k=6, where the true #1
# hit was absent from the six returned. Over-fetch a wider candidate set (which
# raises the effective HNSW ``ef`` to the requested size), then re-sort by
# distance and slice back to the caller's k. The API contract is unchanged:
# ``/search`` still returns exactly k results, best first.
OVERFETCH_MIN = 24
OVERFETCH_FACTOR = 4

# Course content is author-trusted, but render markdown through bleach anyway
# (defense in depth): payloads are DISPLAYED as text, never executed.
_ALLOWED_TAGS = [
    "p",
    "br",
    "hr",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "ul",
    "ol",
    "li",
    "strong",
    "em",
    "b",
    "i",
    "code",
    "pre",
    "blockquote",
    "span",
    "table",
    "thead",
    "tbody",
    "tr",
    "th",
    "td",
    "a",
]
_ALLOWED_ATTRS = {"a": ["href", "title"]}


def render_safe_markdown(text: str) -> str:
    html = md_lib.markdown(text, extensions=["fenced_code", "tables"])
    return bleach.clean(
        html,
        tags=_ALLOWED_TAGS,
        attributes=_ALLOWED_ATTRS,
        protocols=["http", "https"],
        strip=True,
    )


app = FastAPI(title="Software Maintenance Exam Prep")

_embedder: Embedder | None = None
_collection = None

# The MCQ bank is loaded ONCE at import into memory (no per-request disk reads).
# Loading is defensive: a missing/empty data/mcqs never crashes the app.
_bank: QuizBank = QuizBank.load(MCQ_ROOT)


@app.middleware("http")
async def revalidate_shell(request, call_next):
    """Force the HTML/JS/CSS shell to always revalidate so a redeploy is picked up
    immediately (avoids a stale cached page served against new assets)."""
    response = await call_next(request)
    path = request.url.path
    if path == "/" or path.endswith((".html", ".js", ".css")):
        response.headers["Cache-Control"] = "no-cache"
    return response


def _lazy():
    """Lazily construct the embedder + open the Chroma collection on first search."""
    global _embedder, _collection
    if _embedder is None:
        _embedder = Embedder()
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = client.get_collection(COLLECTION)
    return _embedder, _collection


# --- search -----------------------------------------------------------------


def build_where(lecture: str | None, topic: str | None) -> dict | None:
    """Translate the lecture/topic filters into a ChromaDB ``where`` clause.

    ``lecture='all'`` (or ``None``) means no lecture constraint. Combines via
    ``$and`` when both filters are present (cyper pattern).
    """
    conds: list[dict] = []
    if lecture and lecture != "all":
        conds.append({"lecture_id": lecture})
    if topic:
        conds.append({"topic": topic})
    if not conds:
        return None
    return conds[0] if len(conds) == 1 else {"$and": conds}


def search(q: str, k: int, where: dict | None) -> list[dict]:
    emb, col = _lazy()
    # Over-fetch to defeat HNSW recall loss at small n_results, then slice to k.
    n_fetch = max(OVERFETCH_MIN, OVERFETCH_FACTOR * k)
    kwargs: dict = {"query_embeddings": [emb.embed_query(q)], "n_results": n_fetch}
    if where:
        kwargs["where"] = where
    res = col.query(**kwargs)
    out: list[dict] = []
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]
    # Defensive re-sort on raw distance (best first) before slicing to the
    # requested k — the top-k of the wider candidate set is what the UI gets.
    rows = sorted(zip(docs, metas, dists, strict=False), key=lambda row: row[2])[:k]
    for doc, meta, dist in rows:
        item = dict(meta)
        item["text"] = doc
        item["score"] = round(1 - dist, 3)  # cosine distance -> similarity
        item["html"] = render_safe_markdown(doc)
        # A guide chunk citing a real source page can offer a rendered slide image.
        src = meta.get("source_pdf")
        page = meta.get("page")
        if src and isinstance(page, int) and page >= 1:
            item["img"] = f"/slide?file={quote(str(src))}&page={int(page)}"
        else:
            item["img"] = None
        out.append(item)
    return out


@app.get("/search")
def search_endpoint(
    q: str = Query(..., min_length=2),
    k: int = Query(6, ge=1, le=MAX_K),
    lecture: str | None = Query(None),
    topic: str | None = Query(None),
) -> JSONResponse:
    if lecture is not None and not LECTURE_RE.match(lecture):
        raise HTTPException(status_code=422, detail="lecture must match ^L\\d{2}$ or 'all'")
    if topic is not None and topic not in TOPIC_SET:
        raise HTTPException(status_code=422, detail="topic not in the closed taxonomy")
    where = build_where(lecture, topic)
    return JSONResponse({"query": q, "results": search(q, k, where)})


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


# --- slide page images (rendered lazily from source PDFs, cached on disk) ----


def _build_pdf_index() -> dict[str, str]:
    """basename -> absolute path for every discovered source PDF."""
    m: dict[str, str] = {}
    for p in discover_pdfs(PDF_ROOT):
        m.setdefault(os.path.basename(p), p)
    return m


# Built once at import so /slide has no first-request race. Tests monkeypatch this.
_pdf_map: dict[str, str] = _build_pdf_index()


def _slug(name: str) -> str:
    """Filename -> filesystem-safe cache dir name (no path separators)."""
    stem = os.path.basename(name).rsplit(".", 1)[0]
    return re.sub(r"[^A-Za-z0-9._-]", "_", stem)


def render_slide(path: str, page: int) -> bytes:
    doc = fitz.open(path)
    try:
        if page < 1 or page > len(doc):
            raise HTTPException(status_code=404, detail="page out of range")
        pix = doc[page - 1].get_pixmap(matrix=fitz.Matrix(SLIDE_ZOOM, SLIDE_ZOOM))
        return pix.tobytes("png")
    finally:
        doc.close()


@app.get("/slide")
def slide(file: str = Query(...), page: int = Query(..., ge=1)) -> Response:
    # Only ever serve a basename present in our own discovered PDF set (no traversal).
    path = _pdf_map.get(os.path.basename(file))
    if not path:
        raise HTTPException(status_code=404, detail="unknown source file")
    cache = os.path.join(SLIDES_DIR, _slug(file), f"p{page}.png")
    if os.path.exists(cache):
        with open(cache, "rb") as fh:
            return Response(content=fh.read(), media_type="image/png")
    data = render_slide(path, page)
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    with open(cache, "wb") as fh:
        fh.write(data)
    return Response(content=data, media_type="image/png")


# --- quiz / lookup metadata -------------------------------------------------


@app.get("/api/lectures")
def lectures() -> JSONResponse:
    return JSONResponse(_bank.lectures_metadata())


@app.get("/api/quiz")
def quiz(
    lecture: str | None = Query(None),
    topic: str | None = Query(None),
    difficulty: str | None = Query(None),
    n: int = Query(20, ge=1, le=MAX_N),
    seed: int | None = Query(None),
) -> JSONResponse:
    if lecture is not None and not LECTURE_RE.match(lecture):
        raise HTTPException(status_code=422, detail="lecture must match ^L\\d{2}$ or 'all'")
    if topic is not None and topic not in TOPIC_SET:
        raise HTTPException(status_code=422, detail="topic not in the closed taxonomy")
    if difficulty is not None and difficulty not in DIFFICULTY_SET:
        raise HTTPException(status_code=422, detail="difficulty not in the closed vocabulary")

    questions = _bank.sample(lecture=lecture, topic=topic, difficulty=difficulty, n=n, seed=seed)
    if not questions:
        raise HTTPException(status_code=404, detail="no questions match the given filters")
    return JSONResponse({"count": len(questions), "questions": questions})


@app.post("/api/quiz/check")
def quiz_check(payload: dict = Body(...)) -> JSONResponse:
    answers = payload.get("answers") if isinstance(payload, dict) else None
    if not isinstance(answers, list):
        raise HTTPException(status_code=422, detail="body must be {answers: [{id, chosen}]}")
    return JSONResponse(_bank.grade(answers))


# Static frontend mounted LAST so the API routes above take precedence.
if os.path.isdir(STATIC_DIR):
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
