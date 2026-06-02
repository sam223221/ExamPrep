"""Cross-reference resolution check.

For each study/lectures/*.md and study/00-master-index.md:
- Parse every [...](...)  link to other .md files.
- Confirm target file exists.
- If anchor present (after #), confirm a matching heading exists in target.
"""
import re
import sys
from pathlib import Path

ROOT = Path(r"c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study")

LINK_RE = re.compile(r"\[(?:[^\[\]]|\[[^\]]*\])*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


def slugify(text: str) -> str:
    # GitHub-flavored slugify approximation
    s = text.lower()
    # Remove characters that are not alphanumeric, hyphen, underscore, or space
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return s


def collect_headings(md_path: Path) -> set[str]:
    text = md_path.read_text(encoding="utf-8", errors="replace")
    slugs = set()
    seen = {}
    for m in HEADING_RE.finditer(text):
        heading = m.group(2).strip()
        # strip trailing markdown links / formatting
        heading = re.sub(r"`([^`]*)`", r"\1", heading)
        slug = slugify(heading)
        # github-style: duplicate headings get -1, -2 suffix
        if slug in seen:
            seen[slug] += 1
            slug = f"{slug}-{seen[slug]}"
        else:
            seen[slug] = 0
        slugs.add(slug)
    return slugs


def check_file(md_path: Path) -> list[tuple[str, str, str, str]]:
    """Return list of (status, src_file, link_target, detail)."""
    results = []
    text = md_path.read_text(encoding="utf-8", errors="replace")
    for m in LINK_RE.finditer(text):
        url = m.group(1).strip()
        # Skip external URLs
        if url.startswith(("http://", "https://", "mailto:")):
            continue
        # Skip pure anchors (same file)
        if url.startswith("#"):
            anchor = url[1:]
            file_slugs = collect_headings(md_path)
            if anchor in file_slugs:
                results.append(("PASS", str(md_path), url, "same-file anchor"))
            else:
                results.append(("FAIL_ANCHOR", str(md_path), url, f"anchor '{anchor}' not in own headings"))
            continue
        # split anchor
        path_part, _, anchor = url.partition("#")
        # Skip image files
        if path_part.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf")):
            continue
        # only check .md links per spec
        if not path_part.lower().endswith(".md"):
            continue
        # Resolve relative to md_path's dir
        target = (md_path.parent / path_part).resolve()
        if not target.exists():
            results.append(("FAIL_FILE", str(md_path), url, f"target file missing: {target}"))
            continue
        if anchor:
            target_slugs = collect_headings(target)
            if anchor not in target_slugs:
                results.append(("FAIL_ANCHOR", str(md_path), url, f"anchor '{anchor}' not found in {target.name} (slugs available e.g.: {list(target_slugs)[:5]})"))
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
    for status, src, url, detail in fails:
        short = Path(src).name
        print(f"[{status}] {short}  ->  {url}")
        print(f"           {detail}")
    sys.exit(0 if not fails else 1)


if __name__ == "__main__":
    main()
