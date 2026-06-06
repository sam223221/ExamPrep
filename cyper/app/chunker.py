"""Split source text and guide markdown into embeddable chunks with metadata."""
from __future__ import annotations
import re

PAGE_RE = re.compile(r"<!--\s*page:(\d+)\s*-->")
QNA_RE = re.compile(r"^###\s*\[([^\]]+)\]\s*(.*)$")
ANSWER_LABEL_RE = re.compile(r"^\*\*answer:\*\*\s*", re.IGNORECASE)


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
                "difficulty": "",
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
                "difficulty": "",
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


def normalize_difficulty(raw: str) -> str:
    """'VERY HARD' -> 'very-hard', 'EASY' -> 'easy'."""
    return raw.strip().lower().replace(" ", "-")


def chunk_qna(md: str, file: str, topic: str) -> list[dict]:
    """Parse a simulated-Q&A file into one chunk per question.

    Each question block looks like:
        ### [VERY HARD] <question text>
        **Answer:** <answer markdown...>
    Produces a `type=qna` chunk carrying the question's `difficulty` so the
    search API can filter by it.
    """
    chunks: list[dict] = []
    difficulty = ""
    question = ""
    buf: list[str] = []

    def flush():
        if not question:
            return
        answer = ANSWER_LABEL_RE.sub("", "\n".join(buf).strip())
        body = f"**Q:** {question}\n\n{answer}".strip()
        title = question if len(question) <= 90 else question[:87] + "..."
        chunks.append({
            "text": body, "file": file, "topic": topic,
            "page": 0, "type": "qna", "title": title,
            "difficulty": difficulty,
        })

    for line in md.splitlines():
        m = QNA_RE.match(line)
        if m:
            flush(); buf.clear()
            difficulty = normalize_difficulty(m.group(1))
            question = m.group(2).strip()
        elif line.startswith("# "):
            continue
        else:
            buf.append(line)
    flush()
    return chunks
