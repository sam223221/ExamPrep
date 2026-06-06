"""FastAPI app: semantic search over the cyber ChromaDB + static frontend."""
from __future__ import annotations
import os
import bleach
import chromadb
import markdown as md_lib
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.embedder import Embedder

CHROMA_DIR = os.environ.get("CHROMA_DIR", "/data/chroma_db")
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
        item["html"] = render_safe_markdown(doc) if meta.get("type") in ("guide", "qna") else None
        out.append(item)
    return out


def build_where(ctype: str | None, difficulty: str | None) -> dict | None:
    """Translate the type/difficulty filters into a ChromaDB `where` clause."""
    if difficulty and not ctype:
        ctype = "qna"  # only Q&A chunks carry a difficulty
    conds = []
    if ctype in ("qna", "guide", "source"):
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


app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
