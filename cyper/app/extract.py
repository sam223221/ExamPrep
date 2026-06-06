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
