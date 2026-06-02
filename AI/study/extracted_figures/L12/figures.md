# L12 Clustering — Figure Catalogue

Source: `Lecture12-Clustering.pdf` (47 pages). Extracted with PyMuPDF 1.24.9.

Two extraction methods used:
- `fig_pNN_iM.png` — image objects embedded in the slide (PyMuPDF `get_images`).
- `slide_pNN.png` — full-page render of slide NN at 180 DPI (`Page.get_pixmap`), used when the informative content is a composite of native vector shapes + text + images that does not survive image-object extraction.

Verdict legend:
- **USE** = embedded in the chapter as-is.
- **REWORK** = embedded, but supplemented with prose / Mermaid / cropped slide-render because the raw image is unclear, partial, or decorative-looking on its own.
- **SKIP** = decorative stock photo, lecturer-portrait, or fragment with no pedagogical content.

---

## Page-by-page catalogue

### Page 1 — Title slide ("Cluster Analysis — Serkan Ayvaz")
| File | Verdict | Rationale |
|---|---|---|
| `fig_p01_i1.png` | SKIP | Tiny solid-black rectangle (slide-template ornament). No content. |

### Page 3 — "Notion of a Cluster can be Ambiguous"
| File | Verdict | Rationale |
|---|---|---|
| `slide_p03.png` | USE | Whole slide is a single composite showing one point cloud labelled with three different cluster counts (2, 4, 6). Key pedagogical figure for §3 on ambiguity. EXTRACTION_METHOD: page-render. |

### Page 4 — "Types of Clusterings"
| File | Verdict | Rationale |
|---|---|---|
| `fig_p04_i1.png` | SKIP | Decorative stock-art "network of multicoloured nodes" — purely illustrative slide-template imagery. |

### Page 5 — "Partitional Clustering" (Original Points → A Partitional Clustering)
| File | Verdict | Rationale |
|---|---|---|
| `slide_p05.png` | USE | Whole-slide composite: scatterplot of points before and after partitional clustering, with cluster boundaries. Anchors §3 partitional definition. EXTRACTION_METHOD: page-render. |

### Page 8 — K-means basic algorithm (pseudocode)
| File | Verdict | Rationale |
|---|---|---|
| `fig_p08_i1.png` | USE | High-resolution image of the 5-line K-means pseudocode (Select K centroids → repeat assign/recompute → until centroids don't change). Embedded verbatim in §4. |

### Page 9 — K-means worked example (initial → iter 3, 1-D ice-cream-style example)
| File | Verdict | Rationale |
|---|---|---|
| `fig_p09_i1.png` | USE | Iteration trace (a)–(d) of K-means on a 1-D dataset {2,3,4,10,11,12,20,25,30} with K=2, showing centroids $\mu_1, \mu_2$ moving from {2,4} → {2.5,16} → {3,18}. Central worked example for §5. |
| `slide_p09.png` | SKIP | Whole-slide render of page 9 — redundant with `fig_p09_i1.png` which is the only content on that slide. EXTRACTION_METHOD: page-render. |

### Page 10 — K-means worked example, continuation (iter 4, iter 5 converged)
| File | Verdict | Rationale |
|---|---|---|
| `fig_p10_i1.png` | USE | Iteration trace (e)–(f) completing the page-9 example: $\mu_1=4.75, \mu_2=19.60$ → $\mu_1=7, \mu_2=25$ (converged). Continues §5 worked example. |
| `slide_p10.png` | SKIP | Whole-slide render of page 10 — redundant with `fig_p10_i1.png`. EXTRACTION_METHOD: page-render. |

### Page 11 — "Issues and Limitations for K-means"
| File | Verdict | Rationale |
|---|---|---|
| `fig_p11_i1.png` | SKIP | Stock photo of a hand filling in a multiple-choice answer sheet (decorative illustration of "issues"). No conceptual content. |

### Page 12 — "Two different K-means Clusterings" (Sub-optimal vs Optimal)
| File | Verdict | Rationale |
|---|---|---|
| `slide_p12.png` | USE | Three-panel scatterplot comparing original points, sub-optimal local-minimum clustering, and optimal global-minimum clustering. Anchors §6 pitfall on initialisation. EXTRACTION_METHOD: page-render. |

### Pages 13–16 — "Importance of Choosing Initial Centroids" (multi-page trace of two different inits)
| File | Verdict | Rationale |
|---|---|---|
| `slide_p13.png` | SKIP | 6-panel K-means iteration trace from a good initialisation. The point this trace makes — "different initial centroids → different convergence path" — is captured more compactly by Figure 6 (`slide_p12`) in the chapter, which compares the sub-optimal and optimal outcomes directly. Embedding all 22 sub-panels of slides 13–16 would add length without new pedagogical content. EXTRACTION_METHOD: page-render. |
| `slide_p14.png` | SKIP | Same justification as `slide_p13.png` — alternate good-initialisation trace, redundant with Figure 6. EXTRACTION_METHOD: page-render. |
| `slide_p15.png` | SKIP | Same justification — bad-initialisation trace, redundant with Figure 6's sub-optimal panel. EXTRACTION_METHOD: page-render. |
| `slide_p16.png` | SKIP | Same justification — alternate bad-initialisation trace. EXTRACTION_METHOD: page-render. |

### Page 17 — "Solutions to Initial Centroids Problem"
| File | Verdict | Rationale |
|---|---|---|
| `fig_p17_i1.png` | SKIP | Stock photo: chalkboard with calculus formulas (decorative). |

### Page 18 — Bisecting K-means
| File | Verdict | Rationale |
|---|---|---|
| `fig_p18_i1.png` | USE | Wikipedia-sourced figure illustrating bisecting K-means as the dataset is recursively split. Embedded in §4 bisecting K-means subsection. |
| `slide_p18.png` | REWORK | Full slide render kept as backup since `fig_p18_i1` is a stylised radial pattern that does not on its own communicate "split largest cluster into two with K=2, recurse"; chapter adds a prose explanation. EXTRACTION_METHOD: page-render. |

### Page 19 — "What do to in high-dimensional data?"
| File | Verdict | Rationale |
|---|---|---|
| `fig_p19_i1.png` | SKIP | Tiny low-res screenshot of a network graph blog post (https://bigsnarf.wordpress.com/2012/12/) — illustrative only, not a concept figure. The slide text is the entire content; mentioned in §6 pitfall on high-D data. |

### Page 20 — Hierarchical Clustering / Dendrogram
| File | Verdict | Rationale |
|---|---|---|
| `slide_p20.png` | USE | Whole slide containing the canonical dendrogram example (6 points, nested merges, "cut at height" visual). Anchors §3 hierarchical-clustering and §3 dendrogram. EXTRACTION_METHOD: page-render. |

### Page 21 — "Hierarchical Clustering" types (agglomerative vs divisive)
| File | Verdict | Rationale |
|---|---|---|
| `fig_p21_i1.png` | SKIP | Stock photo of wooden-figurine "people connected by string" (decorative). |

### Page 23 — "Cluster Example" (distance matrix + dendrogram)
| File | Verdict | Rationale |
|---|---|---|
| `slide_p23.png` | USE | The 5-company distance matrix worked example with its resulting dendrogram. Central §5 hierarchical worked example. EXTRACTION_METHOD: page-render. |

### Page 26 — "Intermediate Situation" (proximity matrix as we merge C2 and C5)
| File | Verdict | Rationale |
|---|---|---|
| `fig_p26_i1.png` | SKIP | A 2x2 pixel beige fragment — extraction artefact, no content. |
| `slide_p23.png` (already listed) | (used for the worked example) | — |

(Slides 24–27 — "Starting Situation / Intermediate / After Merging" — full slides are not separately rendered because the worked example on slide 23 already captures the conceptual flow; the merge sequence is described in prose in §5.)

### Page 27 — "After Merging" (how to update the proximity matrix question)
| File | Verdict | Rationale |
|---|---|---|
| `slide_p27.png` | USE | Captures the "?" question marks in the merged-cluster proximity matrix, which motivates the linkage methods on the next four slides. EXTRACTION_METHOD: page-render. |

### Pages 28–32 — "How to Define Inter-Cluster Similarity" (MIN, MAX, Group Average, Distance Between Centroids)
| File | Verdict | Rationale |
|---|---|---|
| `slide_p28.png` | USE | Master slide listing the four linkage options. Title figure for §4 linkage table. EXTRACTION_METHOD: page-render. |
| `slide_p29.png` | USE | MIN linkage (single-link): yellow arrow from one cluster's nearest border point to the other's. EXTRACTION_METHOD: page-render. |
| `slide_p30.png` | REWORK | MAX linkage (complete-link): yellow arrow between two farthest points. Embedded together with `slide_p29` and `slide_p32` as a side-by-side comparison. EXTRACTION_METHOD: page-render. |
| `slide_p31.png` | REWORK | Group-average linkage: all pairwise yellow lines drawn between two clusters. Small render; embedded with prose explanation. EXTRACTION_METHOD: page-render. |
| `slide_p32.png` | USE | Centroid-distance linkage: yellow arrow between cluster centroids (marked with red x). EXTRACTION_METHOD: page-render. |

### Page 34 — "Hierarchical Clustering: Problems and Limitations"
| File | Verdict | Rationale |
|---|---|---|
| `fig_p34_i1.png` | SKIP | Decorative marble-texture stock image. No content. |

### Page 37 — "DBSCAN: Core, Border, and Noise Points" (illustrative figure)
| File | Verdict | Rationale |
|---|---|---|
| `fig_p37_i1.png` | USE | Scatterplot with three labelled $\epsilon$-neighbourhoods showing one Core Point (≥ MinPts neighbours inside), one Border Point, and one Noise Point. Eps = 1, MinPts = 4. Central §3 DBSCAN definition figure. |

### Page 38 — "DBSCAN: Core, Border and Noise Points" (Eps=10, MinPts=4 dataset)
| File | Verdict | Rationale |
|---|---|---|
| `fig_p38_i1.png` | USE | "Original Points" scatter — 'GTA' point pattern with surrounding noise. Used as before-image in §5 DBSCAN example. |
| `fig_p38_i2.png` | USE | Same scatter after DBSCAN classification: green = core, blue = border, red = noise. After-image in §5 DBSCAN example. |
| `slide_p38.png` | SKIP | Whole-slide render — the two component figures `fig_p38_i1` and `fig_p38_i2` are already embedded and capture the entire informative content. EXTRACTION_METHOD: page-render. |

### Page 39 — "Density-Connected points"
| File | Verdict | Rationale |
|---|---|---|
| `slide_p39.png` | SKIP | Whole-slide render. The two small density-edge / density-connected diagrams on slide 39 are conceptually clear from the prose definitions in §3.7; the embedded core/border/noise figure (Figure 4) anchors the visual intuition. Embedding slide 39 in raster form would add a low-resolution duplicate of content already covered in text. EXTRACTION_METHOD: page-render. |

### Page 41 — "DBSCAN: Determining Eps and MinPts" (k-distance knee plot)
| File | Verdict | Rationale |
|---|---|---|
| `fig_p41_i1.png` | USE | The signature DBSCAN k-distance plot: sorted distance to 4th nearest neighbour for ~3000 points, with the elbow/knee at ~7–10 marking Eps. Central §4 DBSCAN-parameter selection figure. |
| `slide_p41.png` | SKIP | Whole-slide render — same content as `fig_p41_i1.png` with just the slide title and a couple of annotations. EXTRACTION_METHOD: page-render. |

### Page 42 — "When DBSCAN Works Well"
| File | Verdict | Rationale |
|---|---|---|
| `fig_p42_i1.png` | SKIP | Duplicate of `fig_p38_i1.png` (same GTA original-points scatter); the chapter embeds the page-38 copy as Figure 13a. |
| `fig_p42_i2.png` | USE | DBSCAN clusters in colour: 6 well-separated clusters recovered despite irregular shapes. Embedded as Figure 14. |
| `slide_p42.png` | SKIP | Whole-slide render — `fig_p42_i1` (= duplicate of `fig_p38_i1`) and `fig_p42_i2` together cover the slide's content. EXTRACTION_METHOD: page-render. |

### Page 43 — "When DBSCAN Does NOT Work Well" (varying density)
| File | Verdict | Rationale |
|---|---|---|
| `fig_p43_i1.png` | USE | Ground-truth: three blob clusters of very different densities (sparse green ellipse, medium red, dense yellow with embedded denser sub-clusters). Original points. |
| `fig_p43_i2.png` | USE | DBSCAN with `MinPts=4, Eps=9.75`: the sparse green and medium-density red are mostly recovered, but the dense yellow region is over-merged into noise. |
| `fig_p43_i3.png` | USE | DBSCAN with `MinPts=4, Eps=9.92`: now most of the sparse and medium clusters are marked noise (small blue dots) while only the densest sub-clusters survive as clusters. Demonstrates parameter sensitivity. |
| `slide_p43.png` | SKIP | Whole-slide render — the three component figures already capture every panel of the slide. EXTRACTION_METHOD: page-render. |

### Page 45 — "Different Aspects of Cluster Validation"
| File | Verdict | Rationale |
|---|---|---|
| `fig_p45_i1.png` | SKIP | Decorative stock image of glowing dotted network — slide-template ornament. |

---

## Summary

| Verdict | Count |
|---|---|
| USE | 21 |
| REWORK | 3 (`slide_p18`, `slide_p30`, `slide_p31`) |
| SKIP | 21 |
| **Total** | **45** |

The 45 entries above account for all PNG files in `study/extracted_figures/L12/`. The chapter L12-Clustering.md embeds 23 figures inline (the 21 USE plus the two of three REWORK that contribute unique information — `slide_p30` and `slide_p31` are inline alongside their MIN/centroid companions as the linkage-method comparison strip). `slide_p18.png` is the third REWORK: it is referenced in the catalogue as a backup for `fig_p18_i1.png` but the chapter uses the embedded image plus prose explanation (per spec §6.1.1 point 5) rather than embedding both rasters — embedding `slide_p18` would be a low-resolution duplicate of the same content. Verifier should treat the prose subsection on Bisecting K-means (§4.5) as the "alongside" clarification of `fig_p18_i1`.

All `USE` and `REWORK` figures are embedded in `study/lectures/L12-Clustering.md` with markdown image syntax and captions. All `SKIP` rationales above explain why the figure is decorative or content-free.

Concepts not covered by any figure in the source PDF but discussed in the chapter (with rationale documented in §1 / §6 of the chapter):
- K-means++ — not in the source slides; mentioned briefly in §6 / §7 with pointer to ML Lab 3.
- Elbow / silhouette method for choosing K — not in the source slides; pointer to ML Lab 3.
- Single-link / complete-link / average-link example dendrograms — slides only describe the four linkage measures; full worked dendrograms per linkage are not in the deck.
