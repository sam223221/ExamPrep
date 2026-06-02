"""Render selected lecture_10 pages as PNGs for the analysis doc."""
from pathlib import Path
import fitz

ROOT = Path(r"c:/Users/samgl/Documents/GitHub/ExamPrep/Software architechtur")
SRC = ROOT / "lecture_10.pdf"
OUT_DIR = ROOT / "walkthrough/images/lecture_10"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# (page_number_1indexed, filename, caption)
PAGES = [
    (6,  "fig01_computer_frustration_model.png",   "Computer Frustration Model (Hertzum & Hornaek 2023)"),
    (8,  "fig02_tam_model.png",                    "Technology Acceptance Model (Davis 1989)"),
    (10, "fig04_uz_ui_ux_layers.png",              "UZ / UI / UX vagueness layering"),
    (11, "fig05_usability_subqas.png",             "Usability sub-QAs breakdown"),
    (16, "fig07_mvc_recap.png",                    "MVC pattern (recap from lecture 3)"),
    (19, "fig10_usability_for_whom.png",           "Usability audience taxonomy"),
    (21, "fig12_reference_architecture_eval.png",  "Evaluating reference architectures via usability sub-QAs"),
    (26, "fig15_personas.png",                     "Two personas illustrating usability requirements"),
    (35, "fig21_usability_vs_power.png",           "Usability and power consumption trade-off"),
    (39, "fig23_per_package_p_states.png",         "Per-CPU-package P-states"),
    (40, "fig24_per_core_p_states.png",            "Per-CPU-core P-states"),
    (42, "fig26_c_states.png",                     "Per-CPU-package C-states"),
    (50, "fig30_power_redundancy.png",             "Power consumption with redundant machines"),
    (53, "fig31_graceful_degradation.png",         "Graceful degradation vs graceful shutdown"),
    (54, "fig32_mixing_tactics.png",               "Mixing graceful degradation with escalating restart"),
    (55, "fig33_preloading.png",                   "Preloading via escalating restart"),
    (58, "fig34_offloading_prefetching.png",       "Offloading and prefetching"),
]

doc = fitz.open(SRC)
mat = fitz.Matrix(2, 2)
for pno, fname, caption in PAGES:
    page = doc[pno - 1]
    pix = page.get_pixmap(matrix=mat)
    pix.save(OUT_DIR / fname)
    print(f"  page {pno:>3} -> {fname}  ({pix.width}x{pix.height})  [{caption}]")
doc.close()
print(f"\nWrote {len(PAGES)} PNGs to {OUT_DIR}")
