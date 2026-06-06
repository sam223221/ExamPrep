"""Build the ChromaDB collection from source PDFs + study guide."""
from __future__ import annotations
import glob
import os
import chromadb
from app.extract import extract_pdf, discover_pdfs, topic_of
from app.chunker import chunk_source, chunk_markdown, chunk_qna
from app.embedder import Embedder

PDF_ROOT = os.environ.get("PDF_ROOT", "/data/pdfs")
GUIDE_ROOT = os.environ.get("GUIDE_ROOT", "/data/study-guide")
CHROMA_DIR = os.environ.get("CHROMA_DIR", "/data/chroma_db")
COLLECTION = "cyber"


def _qna_topic(path: str) -> str:
    """'08-threat-modeling-1.md' -> 'Threat Modeling 1'."""
    stem = os.path.basename(path).rsplit(".", 1)[0]
    head, _, tail = stem.partition("-")
    name = tail if head.isdigit() and tail else stem
    return name.replace("-", " ").title()


def gather_chunks() -> list[dict]:
    chunks: list[dict] = []
    for pdf in discover_pdfs(PDF_ROOT):
        rec = extract_pdf(pdf)
        chunks += chunk_source(rec["text"], file=rec["file"], topic=topic_of(pdf))
    # top-level study-guide chapters (non-recursive: excludes the qna/ subfolder)
    for md in sorted(glob.glob(os.path.join(GUIDE_ROOT, "*.md"))):
        with open(md, encoding="utf-8") as fh:
            text = fh.read()
        chunks += chunk_markdown(text, file=os.path.basename(md), topic="Study Guide")
    # simulated open-book Q&A: one chunk per question, tagged with difficulty
    for md in sorted(glob.glob(os.path.join(GUIDE_ROOT, "qna", "*.md"))):
        with open(md, encoding="utf-8") as fh:
            text = fh.read()
        chunks += chunk_qna(text, file=os.path.basename(md), topic=_qna_topic(md))
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
        metadatas=[{k: c[k] for k in ("file", "topic", "page", "type", "title", "difficulty")}
                   for c in chunks],
    )
    print(f"Ingested {col.count()} chunks into '{COLLECTION}'.")


if __name__ == "__main__":
    main()
