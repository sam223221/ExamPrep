"""Render selected lecture_8 pages as PNG for vector diagrams."""
from pathlib import Path
import fitz

ROOT = Path(r"c:\Users\samgl\Documents\GitHub\ExamPrep\Software architechtur")
SRC = ROOT / "lecture_8.pdf"
OUT_DIR = ROOT / "walkthrough" / "images" / "lecture_8"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# (page_number_1based, filename_stem)
PAGES = [
    (17, "page017_safety_scenarios"),
    (18, "page018_safety_tactics_tree"),
    (21, "page021_monitor_actuator_pattern"),
    (22, "page022_security_scenarios"),
    (25, "page025_security_tactics_tree"),
    (28, "page028_siem_architecture"),
    (34, "page034_llm_gateway"),
    (40, "page040_input_channel_validators"),
    (43, "page043_input_validation_three_components"),
    (47, "page047_pipe_filter_validation"),
    (48, "page048_data_vs_control"),
    (50, "page050_trust_boundaries"),
    (58, "page058_revoke_access_tactic"),
    (71, "page071_securing_ai_agents"),
    (73, "page073_cb4a_agent_security"),
    (76, "page076_privilege_drop_separation"),
    (77, "page077_postfix_privilege"),
    (79, "page079_k8s_privilege_drop"),
]

doc = fitz.open(SRC)
matrix = fitz.Matrix(2, 2)  # 2x zoom for crisp diagrams

for pno, stem in PAGES:
    page = doc[pno - 1]
    pix = page.get_pixmap(matrix=matrix)
    out_path = OUT_DIR / f"{stem}.png"
    pix.save(out_path)
    print(f"Wrote {out_path.name} ({pix.width}x{pix.height}, {len(pix.tobytes('png'))} bytes)")
    pix = None

doc.close()
print(f"\nRendered {len(PAGES)} pages to {OUT_DIR}")
