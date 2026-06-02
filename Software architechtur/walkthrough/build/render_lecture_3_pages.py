"""Render selected lecture_3 pages as PNG images (since diagrams are vector, not embedded).

We pick pages whose primary content is an architecture/UML/sequence/tree/taxonomy diagram.
"""
import fitz
from pathlib import Path

src = Path(r"c:\Users\samgl\Documents\GitHub\ExamPrep\Software architechtur\lecture_3.pdf")
img_dir = Path(r"c:\Users\samgl\Documents\GitHub\ExamPrep\Software architechtur\walkthrough\images\lecture_3")
img_dir.mkdir(parents=True, exist_ok=True)

# (page_num_1based, slug)
selections = [
    (8,  "refining_basic_concepts"),                     # Fig 3: in-house vs external components
    (13, "processes_threads_coupling"),                  # Fig 5: machine/process/thread resources
    (16, "integrability_scenario_template"),             # Fig 6: integrability scenario template
    (18, "integrability_tactics_tree"),                  # Fig 8: integrability tactics taxonomy
    (26, "publish_subscribe_pattern"),                   # Fig 14: pub-sub broker
    (29, "observer_vs_pubsub_table"),                    # Table 1: observer vs publish-subscribe
    (31, "logging_microservices_design"),                # Fig 16: logging design for microservices
    (35, "dhcp_discovery_sequence"),                     # Fig 17: DHCP discovery sequence
    (38, "orchestrator_service_discovery"),              # Fig 19: orchestrator with meta-data
    (40, "wrapper_pattern"),                             # Fig 20: wrapper
    (42, "pci_bridge_pattern"),                          # Fig 21: PCI bridges and buses
    (44, "mediator_pattern"),                            # Fig 23: mediator
    (53, "incompatible_change_alternatives"),            # Fig 26: incompatible changes alternatives
    (54, "semantic_versioning"),                         # Fig 27: semantic versioning numbers
    (58, "modifiability_tactics_tree"),                  # Fig 29: modifiability tactics
    (61, "five_modifiability_tactics"),                  # Fig 31: 5 modifiability tactics (split, combine, etc.)
    (65, "binding_stages"),                              # Fig 32: compile/start-up/runtime binding
    (66, "interface_evolution_tactics"),                 # Fig 33: graceful extension
    (67, "graceful_deprecation"),                        # Fig 34: deprecation period
    (75, "plugin_micro_kernel_pattern"),                 # Fig 37: plugin/micro-kernel
    (77, "pipe_and_filter_pattern"),                     # Fig 39: pipe-and-filter
    (78, "batch_sequential_pattern"),                    # Fig 40: batch-sequential
]

doc = fitz.open(src)
saved = []
for pno, slug in selections:
    page = doc[pno - 1]
    pix = page.get_pixmap(dpi=170)
    fname = f"lecture_3_p{pno:02d}_img1_{slug}.png"
    out = img_dir / fname
    pix.save(out)
    saved.append((fname, out.stat().st_size))
doc.close()

for f, b in saved:
    print(f"{f}\t{b}")
print(f"Total: {len(saved)} files")
