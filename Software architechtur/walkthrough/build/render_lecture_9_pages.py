"""Render selected lecture 9 pages as PNG into walkthrough/images/lecture_9/.

Pages were selected because they contain vector architecture diagrams
that are not extractable as embedded images.
"""
from pathlib import Path
import fitz

ROOT = Path(r"c:/Users/samgl/Documents/GitHub/ExamPrep/Software architechtur")
SRC = ROOT / "lecture_9.pdf"
OUT = ROOT / "walkthrough" / "images" / "lecture_9"
OUT.mkdir(parents=True, exist_ok=True)

# (page_number_1based, descriptive_name)
PAGES = [
    (13, "page013_security_tradeoffs.png"),
    (19, "page019_security_as_constraint.png"),
    (20, "page020_microsoft_sdl_model.png"),
    (23, "page023_owasp_cicd_top10.png"),
    (27, "page027_k8s_scanning_pull_model.png"),
    (32, "page032_threat_modeling_tasks.png"),
    (34, "page034_protection_rings.png"),
    (36, "page036_trust_boundaries.png"),
    (38, "page038_killchain_privesc.png"),
    (41, "page041_killchain_exfiltration.png"),
    (44, "page044_dmz_firewall_ids.png"),
    (47, "page047_validation_egress_filter.png"),
    (48, "page048_zero_trust_architecture.png"),
    (49, "page049_sidecar_zero_trust.png"),
    (51, "page051_sidecar_ingress_egress.png"),
    (52, "page052_sidecar_honeypot.png"),
    (58, "page058_personal_data_classification.png"),
    (59, "page059_side_channels_cloud.png"),
    (62, "page062_mitm_protocol_table.png"),
    (67, "page067_cicd_ssh_https.png"),
    (68, "page068_encryption_lifecycle.png"),
]

doc = fitz.open(SRC)
mat = fitz.Matrix(2, 2)
for page_num, name in PAGES:
    page = doc[page_num - 1]
    pix = page.get_pixmap(matrix=mat)
    pix.save(OUT / name)
    print(f"Rendered page {page_num} -> {name} ({pix.width}x{pix.height})")
doc.close()
print(f"Done. Total: {len(PAGES)} pages rendered.")
