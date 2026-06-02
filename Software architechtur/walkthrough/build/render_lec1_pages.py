"""Render selected pages of lecture 1 as PNG (most diagrams are vector, not embedded raster)."""
import fitz
from pathlib import Path

src = Path(r"c:\Users\samgl\Documents\GitHub\ExamPrep\Software architechtur\lecture_1.pdf")
out_dir = Path(r"c:\Users\samgl\Documents\GitHub\ExamPrep\Software architechtur\walkthrough\images\lecture_1")
out_dir.mkdir(parents=True, exist_ok=True)

# (page_number_in_pdf_1_indexed, slug)
pages_to_render = [
    (6,  "sequential_lecture_structure"),
    (26, "user_interface_not_architecture"),
    (28, "design_arch_implementation_pyramid"),
    (33, "two_types_of_constraints"),
    (34, "twin_peaks_basic"),
    (36, "twin_peaks_mountain_range"),
    (40, "concepts_components_modules_connectors"),
    (42, "machine_cpu_memory_view"),
    (43, "system_cpu_memory_view"),
    (46, "client_server_component_diagram"),
    (49, "cloud_internet_view"),
    (52, "decomposition_vs_clientserver_view"),
    (53, "sync_async_notations"),
    (54, "kruchten_4plus1_views"),
    (56, "substitution_principle_example"),
    (60, "liskov_component_substitution"),
    (61, "cohesion_noncohesion"),
    (64, "segregation_principle"),
    (68, "ill_designed_decomposition"),
    (69, "ensemble_learning_architecture"),
    (72, "layered_operating_system"),
    (74, "layered_manufacturing_automation"),
    (77, "healthcare_emergency_system_sketch"),
]

doc = fitz.open(src)
zoom = 2.0  # 144 DPI equivalent
mat = fitz.Matrix(zoom, zoom)

for pno, slug in pages_to_render:
    page = doc[pno - 1]
    pix = page.get_pixmap(matrix=mat)
    fname = f"lecture_1_p{pno:02d}_img1_{slug}.png"
    pix.save(out_dir / fname)
    print(f"Saved {fname} ({pix.width}x{pix.height})")
doc.close()
print(f"\nTotal: {len(pages_to_render)} pages rendered to {out_dir}")
