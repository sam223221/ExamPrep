# Figure Catalogue — L10 Introduction to Machine Learning

Source PDF: `Lecture10-Introduction to Machine Learning.pdf` (61 slides).
Extraction tool: `_extract.py` (PyMuPDF / fitz). Both embedded images and
per-page renders were produced; per-page renders are used wherever the slide's
informative content is a composite of text, arrows, and tables rather than a
single embedded image.

Conventions:

- **USE** — figure or page-render embedded in `study/lectures/L10-Intro-to-ML.md` as-is.
- **REWORK** — figure embedded, but supplemented with a Mermaid diagram or
  prose description because the original is unclear or composite.
- **SKIP** — figure deliberately not embedded (decorative photo, logo, slide
  template ornament, or empty/black image with no informative content).
- **EXTRACTION_METHOD: page-render** — image was produced by rasterising an
  entire PDF page via `fitz.Page.get_pixmap(dpi=160)` because the informative
  content is a composite of text, arrows, and shapes rather than a single
  embedded picture.

---

## Embedded images (PyMuPDF image extraction)

### fig01-page01-img1.png — title slide ornament
- Source page: 1 (title page, "Introduction to Machine Learning").
- Surrounding text: title only.
- Verdict: **SKIP**.
- Rationale: image is a small black rectangle / slide-template artefact. No information content.

### fig02-page02-img1.png — robot reading books (stock photo)
- Source page: 2 ("Machine learning — Definition").
- Surrounding text: "Getting a computer to do well on a task without explicitly programming it..."
- Verdict: **SKIP**.
- Rationale: decorative stock photo of a robot with books. Pure ornament.

### fig03-page04-img1.png — coloured graph / network art
- Source page: 4 ("Unsupervised Learning").
- Surrounding text: "Learning about a dataset without labels — Clustering, Finding outliers..."
- Verdict: **SKIP**.
- Rationale: decorative art piece (a multicoloured pinned-network sculpture); does not actually depict clustering output. The Venn diagram on page 3 (rendered separately, see `page03-render.png`) is the keeper here.

### fig04-page05-img1.png — RL stock photo
- Source page: 5 ("Reinforcement learning").
- Verdict: **SKIP**.
- Rationale: decorative stock illustration.

### fig05-page06-img1.png — chess photo
- Source page: 6 ("Example: chess").
- Verdict: **SKIP**.
- Rationale: decorative photo of a chessboard. The actual RL information is in the slide text.

### fig06-page07-img1.png — RL difficulty stock photo
- Source page: 7 ("Why is RL difficult?").
- Verdict: **SKIP**.
- Rationale: decorative.

### fig07-page08-img1.png — supervised learning stock photo
- Source page: 8 ("Supervised learning").
- Verdict: **SKIP**.
- Rationale: decorative.

### fig08-page10-img1.png — terms slide ornament
- Source page: 10 ("Terms — Regression / Classification").
- Verdict: **SKIP**.
- Rationale: decorative.

### fig09-page14-img1.png — bicycle photo (image classification example)
- Source page: 14 ("Image classification").
- Surrounding text: "Multiclass classification problem (discrete classes, >2 possible classes) — Convolutional network".
- Verdict: **SKIP**.
- Rationale: a single photo of a mountain bike used as an example input to an image-classifier on the slide. The Lecture chapter references image classification with prose; no information is lost.

### fig10-page15-img1.png — image segmentation example photo
- Source page: 15 ("Image segmentation").
- Verdict: **SKIP**.
- Rationale: decorative example photo. Concept is named and explained in §3 / §4 of the chapter.

### fig11-page18-img1.png — scantron answer sheet (decorative)
- Source page: 18 ("A Classification task" — title divider).
- Verdict: **SKIP**.
- Rationale: divider slide visual; no information.

### fig12-page21-img1.png — decision tree section title ornament
- Source page: 21 ("Decision Trees" — section title).
- Verdict: **SKIP**.
- Rationale: section divider visual.

### fig13-page32-img1.png — sapling/roots photo (decision tree section)
- Source page: 32 ("Decision Tree Induction").
- Verdict: **SKIP**.
- Rationale: decorative photo of a sapling with visible roots — visual pun on "tree induction" but adds no algorithmic content.

### fig14-page35-img1.png — tree induction icon
- Source page: 35 ("Tree Induction — Greedy strategy").
- Verdict: **SKIP**.
- Rationale: decorative icon.

### fig15-page45-img1.png — splitting based on Gini icon
- Source page: 45 ("Splitting Based on GINI").
- Verdict: **SKIP**.
- Rationale: decorative ornament; the formula text is the informative content (kept verbatim in the chapter §4).

### fig16-page52-img1.png — impurity curves for 2-class problem
- Source page: 52 ("Comparison among Splitting Criteria").
- Surrounding text: "For a 2-class problem:" — slide shows three curves (Entropy normalised to [0,1], Gini, Misclassification error) as $p$ ranges from 0 to 1.
- Verdict: **USE**.
- Rationale: the canonical "all three impurity measures agree on which split is best, but disagree on magnitude" figure. Critical for understanding why classifiers usually behave similarly under Gini vs entropy.

### fig17-page54-img1.png — classification advantages ornament
- Source page: 54 ("Decision Tree Based Classification — Advantages").
- Verdict: **SKIP**.
- Rationale: decorative icon.

### fig18-page55-img1.png — looking-up-at-tree-canopy photo
- Source page: 55 ("Practical Issues of Classification").
- Verdict: **SKIP**.
- Rationale: decorative tree-canopy photo (visual continuity with the "decision tree" theme).

### fig19-page56-img1.png — overfitting curve (training vs test error)
- Source page: 56 ("Underfitting and Overfitting").
- Surrounding text: "Underfitting: when model is too simple... Overfitting: when model is more complex than necessary..."
- Verdict: **USE**.
- Rationale: the classic U-shaped test error vs monotonically-falling training error figure. This is THE diagram a student must internalise about overfitting.

### fig20-page57-img1.png — overfitting due to noise (2D scatter with distorted decision boundary)
- Source page: 57 ("Overfitting due to Noise").
- Verdict: **USE**.
- Rationale: shows a single labelled noise point distorting the decision boundary — concrete illustration of how a deep tree memorises noise.

### fig21-page58-img1.png — overfitting due to insufficient examples (sparse 2D region)
- Source page: 58 ("Overfitting due to Insufficient Examples").
- Verdict: **USE**.
- Rationale: shows misclassified points in a region with few training examples; pedagogically distinct from the noise case.

### fig22-page59-img1.png — pre-pruning ornament
- Source page: 59 ("How to Address Overfitting" — Pre-Pruning).
- Verdict: **SKIP**.
- Rationale: decorative icon.

### fig23-page60-img1.png — post-pruning ornament
- Source page: 60 ("How to Address Overfitting" — Post-pruning).
- Verdict: **SKIP**.
- Rationale: decorative icon.

---

## Per-page renders (EXTRACTION_METHOD: page-render)

Several slides are composite diagrams (tree drawings, attribute tables with
flowcharts, splitting visualisations). Image-level extraction would only
recover one component. For those slides we use the full-page render. Files
are named `pageNN-render.png`.

| File | Slide | Verdict | Use in chapter | Notes |
|---|---|---|---|---|
| `page03-render.png` | 3 — ML categories Venn | **USE** | §1 / §2 | AI ⊃ ML ⊃ {Supervised, Unsupervised, RL}; Deep Learning overlay. Key "where ML sits" diagram. |
| `page09-render.png` | 9 — model = equation relating input to output | **REWORK** | §3.2 | Slide shows scatter age vs height with several candidate curves. Embedded as page-render plus prose description. |
| `page19-render.png` | 19 — Illustrating Classification Task | **USE** | §3.1 / §4.1 | The induction/deduction loop with train/test tables. |
| `page22-render.png` | 22 — Example of a Decision Tree | **USE** | §3.3 / §5.1 | Refund / MarSt / TaxInc tree with training table. |
| `page23-render.png` | 23 — Another Example of Decision Tree | **USE** | §3.3 / §6 | Same data, different tree — "there could be more than one tree". |
| `page24-render.png` | 24 — Decision Tree Classification Task | **SKIP** | — | Duplicate of slide 19 with "Decision Tree" boxed; redundant if §3.1 already shows slide 19. |
| `page25-render.png` | 25 — Apply Model: start from root | **USE** | §5.2 | First step of the apply-to-test walkthrough. |
| `page26-render.png` | 26 — Apply Model: Refund=No branch | **USE** | §5.2 | Step 2. |
| `page27-render.png` | 27 — Apply Model: MarSt branch | **USE** | §5.2 | Step 3. |
| `page28-render.png` | 28 — Apply Model: at MarSt=Married | **USE** | §5.2 | Step 4. |
| `page29-render.png` | 29 — Apply Model: traverse to leaf | **USE** | §5.2 | Step 5. |
| `page30-render.png` | 30 — Apply Model: leaf → "No" | **USE** | §5.2 | Final step. |
| `page33-render.png` | 33 — Hunt's Algorithm structure | **USE** | §4.2 | Recursive split structure described verbatim. |
| `page34-render.png` | 34 — Hunt's Algorithm walked through | **USE** | §5.3 | The four-step expansion of the cheat data. |
| `page36-render.png` | 36 — Splitting on Nominal/Ordinal | **USE** | §4.3 | Multi-way vs binary split visualisations. |
| `page37-render.png` | 37 — Splitting on Continuous | **USE** | §4.3 | Binary vs multi-way numeric splits. |
| `page38-render.png` | 38 — Determine the Best Split (Own car/CarType/Student ID) | **USE** | §4.4 | Motivates impurity by showing three candidate tests. |
| `page39-render.png` | 39 — Greedy approach: prefer homogeneous nodes | **USE** | §4.4 | The "high vs low impurity" contrast pair. |
| `page41-render.png` | 41 — How to Find the Best Split — $M_0 - M_{12}$ vs $M_0 - M_{34}$ | **USE** | §4.4 | The framework formula for impurity gain. |
| `page42-render.png` | 42 — Gini Index measure (with 4 example nodes) | **USE** | §4.5 | Formula + 4 numerical examples in one frame. |
| `page43-render.png` | 43 — Examples for computing GINI | **USE** | §5.4 | Three worked Gini examples. |
| `page44-render.png` | 44 — Splitting Based on GINI (weighted gain) | **USE** | §4.5 | Weighted-sum formula. |
| `page45-render.png` | 45 — Binary Attributes: Computing GINI Index | **USE** | §5.5 | Concrete worked split with N1 / N2. |
| `page46-render.png` | 46 — Continuous Attributes: Computing Gini Index (slow method) | **USE** | §4.5 | Slow O(N²) approach. |
| `page47-render.png` | 47 — Continuous Attributes: Computing Gini Index (efficient sort+scan) | **USE** | §4.5 / §5.6 | Sorted-scan with the Taxable-Income walk-through. |
| `page48-render.png` | 48 — Entropy formula and properties | **USE** | §4.6 | Definition of entropy as splitting criterion. |
| `page49-render.png` | 49 — Examples for computing Entropy | **USE** | §5.7 | Three worked entropy examples. |
| `page50-render.png` | 50 — Splitting Criteria: Classification Error | **USE** | §4.7 | Formula and properties. |
| `page51-render.png` | 51 — Examples for Computing Error | **USE** | §5.8 | Three worked classification-error examples. |
| `page53-render.png` | 53 — Stopping Criteria for Tree Induction | **USE** | §4.8 | Stop conditions + hyperparameters. |

All files listed above exist as `.png` in this directory and are referenced by
`../extracted_figures/L10/...` from the chapter markdown.

---

## Concepts I could not find in the global glossary

None. All slide-introduced concepts (supervised learning, unsupervised
learning, reinforcement learning, classification, regression, decision tree,
Gini impurity, entropy, information gain, overfitting, ensemble method,
bagging, random forest, training set, test set) match entries in
`study/_shared/glossary.md` under canonical names. Concepts introduced in
this lecture but not yet in the glossary main entries:

- **Hunt's algorithm**, **CART**, **ID3**, **C4.5**, **SLIQ**, **SPRINT** —
  named algorithms used to construct decision trees. Treated as decision-tree
  induction algorithms in §4 of the chapter and named explicitly without
  promoting each to its own glossary entry (consistent with how the slides
  treat them — list of names rather than independent derivations).
- **Misclassification error / Classification error (impurity measure)** —
  third impurity criterion alongside Gini and entropy. Added inline in §4.7;
  the glossary has Gini and Entropy entries but not this one. Flagging in the
  `glossary-additions.md` file is optional given Reviewer #1 will catch it.
- **Underfitting** — counterpart to overfitting. Defined inline in §6 with a
  cross-reference to the glossary's "Overfitting" entry.
- **Pre-pruning / Early stopping**, **Post-pruning** — overfitting-mitigation
  techniques. Defined inline in §6.
- **Hyperparameters of a decision tree** (`max_depth`, `min_samples_leaf`,
  `min_samples_split`, `ccp_alpha`) — named on slides 53 and 60; defined
  inline in §4.8 and §6.
