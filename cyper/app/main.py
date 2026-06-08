"""FastAPI app: semantic search over the cyber ChromaDB + static frontend."""
from __future__ import annotations
import os
import re
from urllib.parse import quote
import bleach
import chromadb
import fitz  # PyMuPDF — render slide pages to images on demand
import markdown as md_lib
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from app.embedder import Embedder
from app.extract import discover_pdfs

CHROMA_DIR = os.environ.get("CHROMA_DIR", "/data/chroma_db")
PDF_ROOT = os.environ.get("PDF_ROOT", "/data/pdfs")
SLIDES_DIR = os.environ.get("SLIDES_DIR", "/data/slides")
SLIDE_ZOOM = 2.0  # ~144 DPI: readable diagrams/text without huge files
COLLECTION = "cyber"

# The study guide is a security course: its text contains live attack payloads
# (<script>, <img onerror=...>, SQLi, etc.). Render markdown, then sanitize so
# payloads are DISPLAYED as text, never executed in the browser.
_ALLOWED_TAGS = [
    "p", "br", "hr", "h1", "h2", "h3", "h4", "h5", "h6",
    "ul", "ol", "li", "strong", "em", "b", "i", "code", "pre",
    "blockquote", "span", "table", "thead", "tbody", "tr", "th", "td", "a",
]
_ALLOWED_ATTRS = {"a": ["href", "title"]}


def render_safe_markdown(text: str) -> str:
    html = md_lib.markdown(text, extensions=["fenced_code", "tables"])
    return bleach.clean(
        html, tags=_ALLOWED_TAGS, attributes=_ALLOWED_ATTRS,
        protocols=["http", "https"], strip=True,
    )

app = FastAPI(title="Cyber Exam Lookup")
_embedder: Embedder | None = None
_collection = None


@app.middleware("http")
async def revalidate_shell(request, call_next):
    """Make the HTML/JS/CSS shell always revalidate so a redeploy is picked up
    immediately (avoids a stale cached page served against new assets)."""
    response = await call_next(request)
    path = request.url.path
    if path == "/" or path.endswith((".html", ".js", ".css")):
        response.headers["Cache-Control"] = "no-cache"
    return response


def _lazy():
    global _embedder, _collection
    if _embedder is None:
        _embedder = Embedder()
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = client.get_collection(COLLECTION)
    return _embedder, _collection


def search(q: str, k: int = 5, where: dict | None = None) -> list[dict]:
    emb, col = _lazy()
    kwargs = {"query_embeddings": [emb.embed_query(q)], "n_results": k}
    if where:
        kwargs["where"] = where
    res = col.query(**kwargs)
    out: list[dict] = []
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        item = dict(meta)
        item["text"] = doc
        item["score"] = round(1 - dist, 3)  # cosine distance -> similarity
        item["html"] = render_safe_markdown(doc) if meta.get("type") in ("guide", "qna", "cmd") else None
        # source chunks map to a real PDF page -> offer a rendered slide image
        if meta.get("type") == "source" and meta.get("file") and meta.get("page"):
            item["img"] = f"/slide?file={quote(str(meta['file']))}&page={int(meta['page'])}"
        else:
            item["img"] = None
        out.append(item)
    return out


def build_where(ctype: str | None, difficulty: str | None) -> dict | None:
    """Translate the type/difficulty filters into a ChromaDB `where` clause."""
    if difficulty and not ctype:
        ctype = "qna"  # only Q&A chunks carry a difficulty
    conds = []
    if ctype in ("qna", "guide", "source", "cmd"):
        conds.append({"type": ctype})
    if difficulty:
        conds.append({"difficulty": difficulty})
    if not conds:
        return None
    return conds[0] if len(conds) == 1 else {"$and": conds}


@app.get("/search")
def search_endpoint(
    q: str = Query(..., min_length=2),
    k: int = 5,
    ctype: str | None = Query(None, alias="type"),
    difficulty: str | None = None,
) -> JSONResponse:
    where = build_where(ctype, difficulty)
    return JSONResponse({"query": q, "results": search(q, k, where)})


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


# --- slide page images (rendered lazily from the source PDFs, cached on disk) ---
def _build_pdf_index() -> dict[str, str]:
    """basename -> absolute path for every source PDF."""
    m: dict[str, str] = {}
    for p in discover_pdfs(PDF_ROOT):
        m.setdefault(os.path.basename(p), p)
    return m


# Built once at import (before the app serves a request) so /slide has no
# first-request race or latency. Tests monkeypatch this directly.
_pdf_map: dict[str, str] = _build_pdf_index()


def _slug(name: str) -> str:
    """Filename -> filesystem-safe cache dir name (no path separators)."""
    stem = name.rsplit(".", 1)[0]
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
    # only ever serve files that exist in our own discovered PDF set (no traversal)
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


app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
