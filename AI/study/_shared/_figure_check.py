"""Figure integrity check.

For each lecture .md, parse every ![...](../extracted_figures/...) reference,
confirm the file exists and is > 1 KB.
Also confirm study/extracted_figures/L*/figures.md exists for every lecture.
"""
import re
import sys
from pathlib import Path

ROOT = Path(r"c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study")

IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

MIN_FIG_BYTES = 1024


def main():
    lectures = sorted(p for p in (ROOT / "lectures").glob("*.md") if p.name != "DOCUMENT.md")
    fig_root = ROOT / "extracted_figures"

    fig_results = []
    cat_results = []

    for md_path in lectures:
        text = md_path.read_text(encoding="utf-8", errors="replace")
        for m in IMG_RE.finditer(text):
            path = m.group(1).strip()
            if path.startswith(("http://", "https://", "data:")):
                continue
            if "extracted_figures" not in path:
                continue
            target = (md_path.parent / path).resolve()
            if not target.exists():
                fig_results.append(("FAIL_MISSING", md_path.name, path, "file does not exist"))
                continue
            sz = target.stat().st_size
            if sz <= MIN_FIG_BYTES:
                fig_results.append(("FAIL_SIZE", md_path.name, path, f"{sz} bytes <= {MIN_FIG_BYTES}"))
                continue
            fig_results.append(("PASS", md_path.name, path, f"{sz} bytes"))

    # Check figures.md for each L*
    for lec_dir in sorted(fig_root.glob("L*")):
        if not lec_dir.is_dir():
            continue
        fig_md = lec_dir / "figures.md"
        if not fig_md.exists():
            cat_results.append(("FAIL", lec_dir.name, "figures.md missing"))
            continue
        text = fig_md.read_text(encoding="utf-8", errors="replace")
        # Look for at least one USE or REWORK verdict
        if re.search(r"\b(USE|REWORK)\b", text):
            cat_results.append(("PASS", lec_dir.name, "ok"))
        else:
            cat_results.append(("FAIL", lec_dir.name, "no USE or REWORK entries found"))

    fp = sum(1 for r in fig_results if r[0] == "PASS")
    ff = [r for r in fig_results if r[0] != "PASS"]

    cp = sum(1 for r in cat_results if r[0] == "PASS")
    cf = [r for r in cat_results if r[0] != "PASS"]

    print(f"=== Embedded figure references ===")
    print(f"Total references: {len(fig_results)}")
    print(f"PASS: {fp}, FAIL: {len(ff)}")
    for status, src, path, detail in ff:
        print(f"  [{status}] {src} -> {path}  ({detail})")
    print()
    print(f"=== figures.md per lecture dir ===")
    print(f"Total dirs: {len(cat_results)}, PASS: {cp}, FAIL: {len(cf)}")
    for status, lec, detail in cat_results:
        print(f"  [{status}] {lec}  ({detail})")

    sys.exit(0 if (not ff and not cf) else 1)


if __name__ == "__main__":
    main()
