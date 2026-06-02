"""Render selected pages of lecture_5.pdf as PNG at 144 DPI (matrix=2,2)."""
import fitz
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "lecture_5.pdf"
OUT = ROOT / "walkthrough" / "images" / "lecture_5"
OUT.mkdir(parents=True, exist_ok=True)

# (page number 1-indexed, slug)
PAGES = [
    (11, "fault_to_failure_flow"),
    (13, "availability_scenario_template"),
    (16, "availability_tactics_tree"),
    (18, "watchdog_heartbeat"),
    (20, "ping_echo"),
    (28, "load_balancing_active_active_vs_passive"),
    (38, "consistency_vs_availability_tradeoff"),
    (44, "circuit_breaker_state_diagram"),
    (50, "escalating_restart"),
    (53, "isolation_gradient"),
    (55, "blast_radius_failure_domains"),
    (62, "active_redundancy_hot_spare"),
    (67, "spare_redundancy_cold_spare"),
    (69, "bulkheads_equitable_allocation"),
    (73, "saga_pattern"),
    (74, "saga_rollback_flight_hotel"),
    (75, "patterns_summary_table"),
]

doc = fitz.open(PDF)
mat = fitz.Matrix(2, 2)
for pno, slug in PAGES:
    page = doc[pno - 1]
    pix = page.get_pixmap(matrix=mat)
    fname = f"lecture_5_p{pno:02d}_page_{slug}.png"
    pix.save(OUT / fname)
    print(f"wrote {fname} ({pix.width}x{pix.height})")
doc.close()
print(f"total={len(PAGES)}")
