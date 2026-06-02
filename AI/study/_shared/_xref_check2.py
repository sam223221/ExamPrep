"""Cross-reference resolution check, v2 — using python-markdown's toc slugify.

The python-markdown library's toc extension provides the canonical slugify
used for in-page anchors. Use it directly so we match the rendering pipeline.
"""
import re
import sys
from pathlib import Path

from markdown.extensions.toc import slugify as md_slugify

ROOT = Path(r"c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study")

LINK_RE = re.compile(r"\[(?:[^\[\]]|\[[^\]]*\])*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


def collect_headings(md_path: Path) -> set[str]:
    text = md_path.read_text(encoding="utf-8", errors="replace")
    slugs = set()
    seen = {}
    for m in HEADING_RE.finditer(text):
        heading = m.group(2).strip()
        # Strip markdown inline formatting from heading
        h = re.sub(r"\*\*([^*]+)\*\*", r"\1", heading)
        h = re.sub(r"\*([^*]+)\*", r"\1", h)
        h = re.sub(r"`([^`]+)`", r"\1", h)
        # Use markdown-toc's slugify with default '-' separator
        slug = md_slugify(h, "-")
        if slug in seen:
            seen[slug] += 1
            slug = f"{slug}_{seen[slug]}"
        else:
            seen[slug] = 0
        slugs.add(slug)
    return slugs


def check_file(md_path: Path) -> list[tuple[str, str, str, str]]:
    results = []
    text = md_path.read_text(encoding="utf-8", errors="replace")
    for m in LINK_RE.finditer(text):
        url = m.group(1).strip()
        if url.startswith(("http://", "https://", "mailto:")):
            continue
        if url.startswith("#"):
            anchor = url[1:]
            file_slugs = collect_headings(md_path)
            if anchor in file_slugs:
                results.append(("PASS", str(md_path), url, "same-file"))
            else:
                results.append(("FAIL_ANCHOR", str(md_path), url, f"anchor not in own headings"))
            continue
        path_part, _, anchor = url.partition("#")
        if path_part.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf")):
            continue
        if not path_part.lower().endswith(".md"):
            continue
        target = (md_path.parent / path_part).resolve()
        if not target.exists():
            results.append(("FAIL_FILE", str(md_path), url, f"target file missing: {target}"))
            continue
        if anchor:
            target_slugs = collect_headings(target)
            if anchor not in target_slugs:
                results.append(("FAIL_ANCHOR", str(md_path), url, f"anchor '{anchor}' not in {target.name}"))
                continue
        results.append(("PASS", str(md_path), url, "ok"))
    return results


def main():
    files = list(ROOT.glob("lectures/*.md"))
    files.append(ROOT / "00-master-index.md")

    all_results = []
    for f in files:
        if f.name == "DOCUMENT.md":
            continue
        all_results.extend(check_file(f))

    passes = sum(1 for r in all_results if r[0] == "PASS")
    fails = [r for r in all_results if r[0] != "PASS"]

    print(f"Total links checked: {len(all_results)}")
    print(f"PASS: {passes}")
    print(f"FAIL: {len(fails)}")
    print()
    by_file = {}
    for status, src, url, detail in fails:
        short = Path(src).name
        by_file.setdefault(short, []).append((status, url, detail))
    for fname, items in sorted(by_file.items()):
        print(f"--- {fname} ({len(items)} fails) ---")
        for status, url, detail in items:
            print(f"  [{status}] {url}  =>  {detail}")
    sys.exit(0 if not fails else 1)


if __name__ == "__main__":
    main()
