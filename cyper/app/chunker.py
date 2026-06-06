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
