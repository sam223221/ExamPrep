"""Extract images and page renders from the L03 source PDF."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import fitz  # PyMuPDF

SRC = Path(r"c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture3-Uninformed Search.pdf")
OUT = Path(r"c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\extracted_figures\L03")
OUT.mkdir(parents=True, exist_ok=True)


def slug(s: str) -> str:
    keep = []
    for c in s.lower():
        if c.isalnum():
            keep.append(c)
        elif c in " -_":
            keep.append("-")
    out = "".join(keep)
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")[:40] or "img"


def main() -> None:
    doc = fitz.open(SRC)
    print(f"Opened {SRC.name}: {len(doc)} pages")

    # Pages we want full-slide renders for (composite slides where image-level
    # extraction often misses arrows/labels/overlays). 1-indexed page numbers.
    page_renders = {
        2: "maze-cover",
        3: "problem-solving-flowchart",
        8: "search-maze-labelled",
        10: "search-problem-components",
        11: "romania-map-and-graph",
        13: "vacuum-world-initial",
        14: "vacuum-world-state-space",
        15: "8-puzzle",
        16: "3-puzzle-trace",
        17: "building-goal-based-agents",
        18: "romania-route-graph",
        19: "8-queens",
        20: "tree-search-diagram",
        22: "tree-search-step1",
        23: "tree-search-step2",
        24: "tree-search-step3-fringe",
        25: "tree-search-step4",
        26: "tree-search-step5-fringe",
        30: "bfs-step1",
        31: "bfs-step2",
        32: "bfs-step3",
        33: "bfs-step4",
        34: "bfs-step5",
        37: "ucs-worked-example",
        38: "dfs-step1",
        39: "dfs-step2",
        40: "dfs-step3",
        41: "dfs-step4",
        42: "dfs-step5",
        43: "dfs-step6",
        44: "dfs-step7",
        45: "dfs-step8",
        46: "dfs-step9",
        49: "ids-limit-0",
        50: "ids-limit-1",
        51: "ids-limit-2",
        52: "ids-limit-3",
        54: "comparison-table",
    }

    seq = 1
    catalogue: list[dict] = []

    # 1) page-render fallbacks for slides we care about
    for page_idx in range(len(doc)):
        page_no = page_idx + 1
        if page_no not in page_renders:
            continue
        page = doc.load_page(page_idx)
        pix = page.get_pixmap(dpi=180, alpha=False)
        name = f"fig{seq:02d}-{page_renders[page_no]}.png"
        path = OUT / name
        pix.save(path)
        catalogue.append(
            {
                "seq": seq,
                "name": name,
                "page": page_no,
                "method": "page-render",
                "size": path.stat().st_size,
            }
        )
        print(f"  rendered page {page_no:>2} -> {name} ({path.stat().st_size} B)")
        seq += 1

    # 2) Also enumerate image-level extracts as a record (smaller, sharper)
    for page_idx in range(len(doc)):
        page_no = page_idx + 1
        info = doc.get_page_images(page_idx, full=True)
        for ix, item in enumerate(info, 1):
            xref = item[0]
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.n - pix.alpha >= 4:  # CMYK -> RGB
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                # skip tiny logos & decorative bits
                if pix.width < 80 or pix.height < 80:
                    pix = None
                    continue
                name = f"fig{seq:02d}-page{page_no:02d}-img{ix}.png"
                path = OUT / name
                pix.save(path)
                catalogue.append(
                    {
                        "seq": seq,
                        "name": name,
                        "page": page_no,
                        "method": "image-extract",
                        "size": path.stat().st_size,
                    }
                )
                print(f"  extracted img p{page_no:>2}#{ix} -> {name} ({path.stat().st_size} B)")
                seq += 1
                pix = None
            except Exception as e:
                print(f"  WARN extracting p{page_no}#{ix}: {e}")

    # write a tiny inventory for the human-readable figures.md to consume
    inv = OUT / "_inventory.txt"
    inv.write_text(
        "\n".join(
            f"{c['seq']:02d}\t{c['name']}\tpage={c['page']}\tmethod={c['method']}\tbytes={c['size']}"
            for c in catalogue
        ),
        encoding="utf-8",
    )
    print(f"Wrote {inv} ({len(catalogue)} entries)")


if __name__ == "__main__":
    main()
