"""Render specific PDF pages from lecture_4 to PNG (cropped to figure region)."""
import fitz
from pathlib import Path

ROOT = Path(r"c:/Users/samgl/Documents/GitHub/ExamPrep/Software architechtur")
SRC = ROOT / "lecture_4.pdf"
OUT = ROOT / "walkthrough" / "images" / "lecture_4"
OUT.mkdir(parents=True, exist_ok=True)

# (page_number_1based, output_slug, optional clip rect-relative-to-page or None for full)
# We'll render whole page at high DPI then save.
TARGETS = [
    (8,  "p08_testability_scenarios"),
    (12, "p12_oracle_diagram"),
    (15, "p15_fuzzing_skeleton"),
    (16, "p16_fuzzer_perf_checks"),
    (19, "p19_testability_tactics_tree"),
    (36, "p36_llm_generate_verify_loop"),
    (41, "p41_llm_with_independent_validation"),
    (48, "p48_ci_cd_pipeline"),
    (52, "p52_deployability_scenarios"),
    (53, "p53_deployability_tactics_tree"),
    (54, "p54_separate_builds"),
    (58, "p58_multi_server_versions"),
    (64, "p64_rolling_upgrade_start"),
    (65, "p65_rolling_upgrade_50pct"),
    (67, "p67_rolling_upgrade_complete"),
    (72, "p72_ab_testing_split"),
    (75, "p75_cra_security_updates"),
    (77, "p77_semantic_versioning"),
    (80, "p80_chaos_engineering_setup"),
]

doc = fitz.open(SRC)
zoom = 2.5  # ~180 dpi
mat = fitz.Matrix(zoom, zoom)

for pno, slug in TARGETS:
    page = doc[pno - 1]
    pix = page.get_pixmap(matrix=mat, alpha=False)
    fname = OUT / f"lecture_4_p{pno:02d}_{slug}.png"
    pix.save(fname)
    print(f"saved {fname.name} {pix.width}x{pix.height}")
    pix = None

doc.close()
print("DONE")
