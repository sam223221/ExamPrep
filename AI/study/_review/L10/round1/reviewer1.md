# L10 Round 1 — Reviewer #1 (Concept Completeness incl. Figures)

**Lecture:** L10 — Introduction to Machine Learning
**Source PDF:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture10-Introduction to Machine Learning.pdf` (61 slides)
**Chapter:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L10-Intro-to-ML.md`
**Figures catalogue:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\extracted_figures\L10\figures.md`
**Spec:** §7.1 — verify every slide covered, every figure embedded properly. BE HARSH.

---

## VERDICT: **Fail — must revise**

Two material P0 problems (a wrong numerical worked-example claim that contradicts the chapter's own §5.6, and a numerically wrong Yes/No count) plus seven figures that the figures catalogue marks **USE** but the chapter never embeds. The chapter is well-written and covers most slides, but a student studying §4.5 will memorise a wrong fact, and the figure inventory is inconsistent. Round 1 must fix these before the chapter is exam-ready.

---

## P0 — Blockers (must fix)

### P0-1. Wrong best-split location AND wrong Yes/No counts in §4.5 (continuous-attribute Gini scan)
- **Location:** `study/lectures/L10-Intro-to-ML.md` line 314 (end of §4.5).
- **Text in chapter:** *"The minimum Gini in Figure 14 is **0.300** at the threshold between 85 and 90 (a `Yes / No` count of `1/3 vs 2/4` on the left / right). That is the best split point for `Taxable Income`."*
- **Reality on slide 47:** The threshold yielding Gini = 0.300 is position **97** (i.e. between sorted values **95K and 100K**), not "between 85 and 90". The cumulative class counts at that split position are left = (Yes=3, No=3), right = (Yes=0, No=4) — i.e. **`3/3 vs 0/4`**, not `1/3 vs 2/4`.
- **Verification:** From the slide-47 text dump (lines 1497–1580 of `_text_dump.txt`), split positions are 55/65/72/80/87/92/**97**/110/122/172/230 with Gini 0.420/0.400/0.375/0.343/0.417/0.400/**0.300**/0.343/0.375/0.400/0.420. The 7th position (97) is the minimum, and lies between sorted record values 95 and 100. Re-deriving: Gini(left) = 1 − (3/6)² − (3/6)² = 0.5; Gini(right) = 1 − 0² − 1² = 0; weighted = (6/10)(0.5) + (4/10)(0) = **0.300**.
- **Why P0:** This is the headline number in a worked example that the same chapter also recites correctly in §5.6 (lines 469–484), where the threshold table and the surrounding prose state the threshold is "around 97 (between the 95K-Yes-cheater and the 100K-No row)". §4.5 directly contradicts §5.6 and gets two facts wrong (which threshold, which counts). An exam-bound student will remember whichever they read first; one of the two is unambiguously wrong.
- **Suggested fix:** Replace line 314 with: *"The minimum Gini in Figure 14 is **0.300** at the threshold between 95K and 100K (sorted-value split position 97), where the left/right class counts are (Yes=3, No=3) vs (Yes=0, No=4). That is the best split point for `Taxable Income`."*

---

## P1 — Important issues (should fix)

### P1-1. Seven slides catalogued as USE are never embedded
The figures.md catalogue (`extracted_figures/L10/figures.md`) explicitly marks the following per-page renders as **USE** with intended chapter section, but the chapter does not embed any of them:

| Slide | File | Catalogue intent | Chapter status |
|---|---|---|---|
| 43 | `page43-render.png` | §5.4 (three worked Gini examples — formula + numerical) | Not embedded; §5.4 only has prose |
| 44 | `page44-render.png` | §4.5 (weighted-sum split formula) | Not embedded; §4.5 has the formula in LaTeX but no figure |
| 48 | `page48-render.png` | §4.6 (Entropy formula + properties) | Not embedded; §4.6 prose-only |
| 49 | `page49-render.png` | §5.7 (three worked entropy examples) | Not embedded; §5.7 prose-only |
| 50 | `page50-render.png` | §4.7 (Classification error formula) | Not embedded; §4.7 prose-only |
| 51 | `page51-render.png` | §5.8 (three worked classification-error examples) | Not embedded; §5.8 prose-only |
| 53 | `page53-render.png` | §4.8 (stopping criteria + hyperparameters) | Not embedded; §4.8 prose-only |

- **Why P1:** Either the figures catalogue is wrong (should say SKIP for these) or the chapter is missing seven figure embeds. Visual symmetry matters here — every other impurity formula slide is shown as a figure (Gini at §4.5, Gini examples at line 290, comparison curves at §5.9 line 508). It is jarring that Gini gets figures but entropy and classification error do not, and that worked Gini at §5.4 has no figure while the analogous worked Gini at §5.5 (slide 45) is described in prose only because slide 45 itself is unembedded.
- **Suggested fix:** Either (a) embed the seven page-renders into the listed sections, or (b) downgrade them to SKIP in `figures.md` with a stated rationale (e.g. "formula already given in LaTeX; render redundant"). Pick one and make the chapter + catalogue agree.

### P1-2. Slide 35 (Tree induction — greedy strategy / issues) lacks an explicit section header
- **Location:** chapter §4.4 (line 254) handles "How to find the best split" but the "Tree Induction — Greedy strategy + Issues (how to split? how to determine the best? when to stop?)" framing of slide 35 is folded silently into §4.2/§4.4 without being called out.
- **Why P1:** Slide 35 is the meta-overview that names the three issues (split-how, best-split, stop) the rest of the lecture answers. Students reading the chapter never see this three-bullet framing explicitly, which makes §4.3–§4.8 feel ad-hoc rather than an answer to a stated structure. This is the kind of organising frame that helps exam recall.
- **Suggested fix:** Add a one-paragraph "§4.2.1 The three issues" callout (or fold into a clearly-labelled intro of §4.3) listing: (1) how to specify the attribute test, (2) how to determine the best split, (3) when to stop. Then say "the next three subsections answer each".

### P1-3. Slide 40 (Measures of Node Impurity — the three options list) not explicitly catalogued
- **Location:** chapter §4.4 line 277 says "We now need a concrete impurity measure. The slides cover **three** (slide 40): Gini index, entropy, and misclassification (classification) error."
- **Why P1:** Coverage is technically present, but the slide 40 itself (the three-bullet list of impurity measures) is neither rendered as a figure nor cited in figures.md (page40-render exists in the directory but is not catalogued at all — neither USE nor SKIP). Minor catalogue gap, not a content gap. Document the decision in figures.md.

### P1-4. Slides 28–29 (Apply Model — intermediate frames) referenced but not embedded
- **Location:** chapter §5.2 line 415: *"(Slides 28–29 continue to emphasise the same step pictorially.)"*
- **Why P1:** The chapter explicitly tells the student "slides 28–29 exist and emphasise the same step", but the figures.md catalogue lists `page28-render.png` and `page29-render.png` as **USE** with intent §5.2. Same inconsistency category as P1-1: catalogue says USE, chapter doesn't embed. Decide: embed (slides 28 and 29 do show progressive arrows along the tree path) or downgrade catalogue to SKIP with a one-line rationale ("pictorially redundant with slides 25–27 and 30").

### P1-5. Slide 16 (Translation) — inference goes beyond what the slide says
- **Location:** chapter §3.2 table (line 144): row "Machine translation | Sequence-to-sequence (one continuous output sequence) | (slide gives no specific architecture)".
- **Reality:** slide 16 is literally just the word "Translation" with no architecture, no input/output framing, no "seq2seq" label.
- **Why P1:** Calling translation "sequence-to-sequence (one continuous output sequence)" is the chapter's own inference. The "continuous output sequence" phrasing is also misleading because translation has *discrete* token outputs, not continuous values. If the chapter wants to keep the row, it must either drop the architecture claim or label it as the chapter author's gloss, not the slide's statement.
- **Suggested fix:** Replace the table row's "Output type" cell with "Sequence output (not directly fitting the regression/classification dichotomy on slide 10)" and remove the seq2seq/continuous claim, OR drop the row entirely and note in prose that slide 16 names translation without an architecture.

### P1-6. Chapter §4.9 (Ensembles) — develops Bagging and Random Forest beyond the slide deck
- **Location:** chapter §4.9 (lines 357–365).
- **Reality:** the slides only NAME these on slide 20 ("Ensemble Methods (Bagging - Boosting), Random Forest, AdaBoost, CatBoost, XGBoost"). They are not developed anywhere in the deck.
- **Why P1:** The chapter develops them in some detail (bootstrap sampling, decorrelation, majority vote / average) — accurate, but it is *adding* content the lecture did not cover, which violates §7.1's "every slide covered" implies "and not much else". For an exam-prep chapter the addition is borderline acceptable (it is needed for ML Lab 1), but it should be explicitly flagged as such, not presented as if it were lecture content.
- **Suggested fix:** Add a leading sentence to §4.9 along the lines of "Slide 20 only names these methods; the descriptions below are added for the chapter because ML Lab 1 uses them." This is a transparency issue.

### P1-7. Misclassification error caption in §5.8 — "linearly … then mirrors" claim under-justified
- **Location:** chapter line 504: *"Note classification error grows *linearly* with the minority class probability $p$ up to $p = 0.5$, then mirrors — that is why it is a 'kinked' line in the comparison plot below, while Gini is a parabola and entropy a smooth-arched curve."*
- **Issue:** The slide 50 formula is $\operatorname{Error}(t) = 1 - \max_i P(i \mid t)$, which for two classes is $\min(p, 1-p)$ — yes, a piecewise-linear V (kink at $p=0.5$). The chapter's "grows linearly … then mirrors" is correct but obscured by sloppy phrasing. Not numerically wrong, but exam students may misread it.
- **Suggested fix:** Replace with: "For two classes, Error$(t) = \min(p, 1-p)$ — a piecewise-linear function of $p$ that grows linearly from 0 to 0.5 as $p$ moves from 0 to 0.5, then linearly decreases back to 0 as $p$ moves from 0.5 to 1. This is the kink visible in Figure 16."

---

## P2 — Polish / suggestions

### P2-1. Slide 23 tree branch label inconsistency
- Slide 22 caption shows `< 80K` and `> 80K`; slide 34 (Hunt) shows `< 80K` and `>= 80K`. The chapter quotes both forms. Worth noting once in §5.1 that the slide deck itself is inconsistent on the boundary case (does 80K go left or right?).

### P2-2. Glossary additions noted but never queued
- The figures.md document admits five concepts are introduced inline that are not yet in the global glossary (Hunt's algorithm, CART, ID3, C4.5, SLIQ, SPRINT, classification error as impurity measure, underfitting, pre-/post-pruning, hyperparameters). The chapter introduces all of them — but they should be queued for the glossary in a `glossary-additions.md` file. Not a chapter defect, but a follow-up the PM should track.

### P2-3. §5.7 entropy values cite slide rounding but use more precise figures
- Line 491: *"$\operatorname{Entropy} \approx 0.650$ (the slide rounds to $0.65$..."*. Fine, but earlier (line 492) you write 0.918 then say "slide rounds to 0.92". Both are correct; just make the formatting symmetric (e.g. always quote the slide value first, then the more-precise value, or vice versa).

### P2-4. Figure 16 — entropy curve caption claim
- Chapter line 508: *"Entropy peaks at 1.0 at p=0.5"*. The entropy curve on slide 52 is normalised to [0, 1]. The plain $-\sum p \log_2 p$ formula already gives 1 at $p=0.5$ for two classes, but other deck conventions normalise differently. The wording is correct here, but a one-line "log base 2, two-class case" qualifier would help.

### P2-5. §5.3 ordering claim
- Line 436: *"the order chosen is Refund → MarSt → TaxInc, which is what a Gini- or entropy-driven choice would also pick on these 10 rows"*. Asserted without computation. Either back this with a quick Gini-of-Refund vs Gini-of-MarSt calculation, or hedge ("the slide implies this would also be the impurity-driven choice").

### P2-6. Figure number drift in §2 analogy paragraph
- Line 83: *"see Figure 11 in §5"*. Figure 11 in the chapter is the best-split framework, not the impurity-curves figure (which is Figure 16). The analogy text should point to Figure 16.

---

## EVIDENCE — slide-by-slide coverage matrix

Format: `Slide | Title | Coverage section | Figure embedded?`. **bold** = problem.

| Slide | Title | Chapter coverage | Figure |
|---|---|---|---|
| 1 | Title | N/A (skip) | N/A |
| 2 | ML Definition | §1 | text only ✓ |
| 3 | ML categories Venn | §1 | Figure 1 (page03-render) ✓ |
| 4 | Unsupervised Learning | §3.1 | text only ✓ |
| 5 | Reinforcement Learning | §3.1 | text only ✓ |
| 6 | RL example: chess | §3.1 + §2 analogy | text only ✓ |
| 7 | Why is RL difficult? | §3.1 (three difficulties) | text only ✓ |
| 8 | Supervised Learning | §3.1 / §3.2 | text only ✓ |
| 9 | Supervised model = equation | §3.2 | Figure 2 (page09-render) ✓ |
| 10 | Terms (regression/classification, uni/multivariate) | §3.2 | text only ✓ |
| 11 | Regression — height | §3.2 table | text only ✓ |
| 12 | Text classification | §3.2 table | text only ✓ |
| 13 | Music genre classification | §3.2 table | text only ✓ |
| 14 | Image classification | §3.2 table | text only ✓ |
| 15 | Image segmentation | §3.2 table | text only ✓ |
| 16 | Translation | §3.2 table (**P1-5: chapter over-claims**) | text only |
| 17 | "A Classification task" title | §3.3 preamble | divider — skip ✓ |
| 18 | Classification — Definition | §3.3 | text only ✓ |
| 19 | Illustrating Classification Task | §3.3 | Figure 3 (page19-render) ✓ |
| 20 | Classification Techniques | §3.4 + §4.9 | text only ✓ |
| 21 | "Decision Trees" title | §3.5 preamble | divider — skip ✓ |
| 22 | Example of a Decision Tree | §3.5 / §5.1 | Figure 4 (page22-render) ✓ |
| 23 | Another Example of Decision Tree | §3.5 / §5.10 | Figure 5 (page23-render) ✓ |
| 24 | DT Classification Task (duplicate of 19) | (not covered — figures.md SKIP) | acceptable ✓ |
| 25 | Apply Model — start at root | §5.2 step 1 | page25-render ✓ |
| 26 | Apply Model — Refund=No branch | §5.2 step 2 | page26-render ✓ |
| 27 | Apply Model — MarSt branch | §5.2 step 3 | page27-render ✓ |
| 28 | Apply Model — intermediate | §5.2 line 415 mentions | **P1-4: catalogued USE, NOT embedded** |
| 29 | Apply Model — intermediate | §5.2 line 415 mentions | **P1-4: catalogued USE, NOT embedded** |
| 30 | Apply Model — assign "No" | §5.2 final step | page30-render ✓ |
| 31 | DT Classification Task (duplicate of 19/24) | not covered | duplicate; acceptable |
| 32 | DT Induction algorithms list | §4.2 | text only ✓ |
| 33 | Hunt's general structure | §4.2 | Figure 6 (page33-render) ✓ |
| 34 | Hunt's algorithm walked through | §5.3 | Figure 15 (page34-render) ✓ |
| 35 | Tree Induction — greedy + issues | folded into §4.2/§4.4 (**P1-2: framing lost**) | not embedded |
| 36 | Splitting on Nominal/Ordinal | §4.3 | Figure 7 (page36-render) ✓ |
| 37 | Splitting on Continuous | §4.3 | Figure 8 (page37-render) ✓ |
| 38 | Best Split — three candidates | §4.4 | Figure 9 (page38-render) ✓ |
| 39 | Greedy + homogeneity | §4.4 | Figure 10 (page39-render) ✓ |
| 40 | Measures of Node Impurity | §4.4 line 277 | **P1-3: page40-render uncatalogued** |
| 41 | How to find the best split — M_0 framework | §4.4 | Figure 11 (page41-render) ✓ |
| 42 | Gini Index measure + 4 examples | §4.5 | Figure 12 (page42-render) ✓ |
| 43 | Worked Gini examples | §5.4 | **P1-1: catalogued USE, NOT embedded** |
| 44 | Splitting Based on GINI (weighted) | §4.5 (formula in LaTeX) | **P1-1: catalogued USE, NOT embedded** |
| 45 | Binary attributes — worked GINI | §5.5 | not embedded; figures.md silent on page45-render existence |
| 46 | Continuous attributes — slow method | §4.5 | Figure 13 (page46-render) ✓ |
| 47 | Continuous attributes — efficient sort+scan | §4.5 / §5.6 (**P0-1: §4.5 mis-states the result**) | Figure 14 (page47-render) ✓ |
| 48 | Entropy formula + properties | §4.6 | **P1-1: catalogued USE, NOT embedded** |
| 49 | Worked Entropy examples | §5.7 | **P1-1: catalogued USE, NOT embedded** |
| 50 | Classification Error formula | §4.7 | **P1-1: catalogued USE, NOT embedded** |
| 51 | Worked Classification Error examples | §5.8 | **P1-1: catalogued USE, NOT embedded** |
| 52 | Comparison among impurity criteria | §5.9 | Figure 16 (fig16-page52-img1) ✓ |
| 53 | Stopping Criteria | §4.8 | **P1-1: catalogued USE, NOT embedded** |
| 54 | DT Advantages | §6.4 | text only ✓ |
| 55 | Practical Issues (Underfitting/Overfitting/Missing/Cost) | §6 preamble | divider — skip ✓ |
| 56 | Underfitting and Overfitting | §6.1 | Figure 17 (fig19-page56-img1) ✓ |
| 57 | Overfitting due to Noise | §6.2 | Figure 18 (fig20-page57-img1) ✓ |
| 58 | Overfitting due to Insufficient Examples | §6.2 | Figure 19 (fig21-page58-img1) ✓ |
| 59 | Pre-pruning | §6.3 | text only ✓ |
| 60 | Post-pruning | §6.3 | text only ✓ |
| 61 | Thanks for your attention | N/A | skip ✓ |

**Summary:** 61/61 slide titles are addressed (or correctly skipped as dividers/duplicates). 23 figures embedded; 7 catalogued as USE are missing; 1 page-render exists but is uncatalogued; 1 worked-example claim (§4.5 line 314) is numerically wrong.

---

## Figures audit

- **Total slides:** 61.
- **Figures embedded in chapter:** 23.
- **Catalogued USE — embedded:** 16 (matches catalogue intent).
- **Catalogued USE — missing:** 7 (pages 28, 29, 43, 44, 48, 49, 50, 51, 53 — note page 45 also exists but is not catalogued USE, only described in prose).
- **Catalogued SKIP — correctly absent:** 23 decorative ornaments / dividers.
- **Uncatalogued page-renders:** at minimum `page40-render.png` (silently exists).

The catalogue is internally consistent for USE-vs-SKIP intent, but the chapter does not honour the USE intent on seven entries. This is the single biggest mechanical problem to fix.

---

## Concerns / risks

1. **§4.5 ↔ §5.6 internal contradiction** is the kind of error a copy-editor catches and a tired student does not. Top priority.
2. **Asymmetric figure embedding** between Gini (heavily illustrated) and Entropy / Classification Error / Stopping (no figures) makes the chapter feel like it loses interest after slide 47. Fix by either embedding the missing renders or downgrading the catalogue.
3. **Scope creep risk in §4.9:** Bagging/Random Forest discussion is *useful for ML Lab 1* but goes beyond the slides. Acceptable if flagged; not acceptable if presented as lecture content.
4. **The chapter is otherwise excellent** — well-structured, the analogies in §2 are pedagogically strong, the cheat-sheet in §8 is exam-ready. After P0-1 and P1-1 are fixed this should pass Round 2 without difficulty.

---

## Report to PM

**Assignment recap:** L10 "Introduction to Machine Learning" — Round 1, Reviewer #1 (Concept Completeness incl. Figures) per Spec §7.1. 61 slides, two artefacts (chapter + figures catalogue). Reviewed the chapter against the slide deck (text dump + slide titles), and the chapter's image embeds against the figures catalogue.

**Status:** **Fail** — one P0 numerical error (worked-example claim that contradicts the chapter's own later section) and one large P1 cluster (seven catalogued USE figures never embedded). 23 slides covered with figures; all 61 slide titles are addressed in the prose; coverage is otherwise strong.

**P0 findings:**
1. `L10-Intro-to-ML.md:314` — §4.5 states minimum Gini = 0.300 is *"between 85 and 90 (a Yes/No count of 1/3 vs 2/4)"*. **Both claims are wrong.** The minimum is at split position 97 (between sorted values 95 and 100), with counts 3/3 on the left vs 0/4 on the right. §5.6 of the same chapter has the right number. Fix: replace the sentence with the corrected threshold (95K–100K) and counts (3/3 vs 0/4).

**P1 findings:**
1. Seven slides catalogued as **USE** in `extracted_figures/L10/figures.md` are not embedded in the chapter: slides 28, 29, 43, 44, 48, 49, 50, 51, 53. Either embed them or downgrade the catalogue.
2. Slide 35 (greedy strategy + three issues framing) is folded silently into §4.2/§4.4; lose the organising frame that helps exam recall.
3. `page40-render.png` exists on disk but is uncatalogued (not USE, not SKIP). Document the decision.
4. Slides 28–29 are explicitly referenced in §5.2 line 415 ("Slides 28–29 continue to emphasise...") yet not embedded — same as P1-1 but called out separately because of the explicit textual reference.
5. Slide 16 (Translation): chapter table calls it "sequence-to-sequence (one continuous output sequence)" — both labels are chapter inferences beyond the slide content, and "continuous output sequence" is misleading for token outputs.
6. §4.9 (Ensemble methods) develops Bagging/Random Forest beyond what the slides cover; add an explicit "added for the chapter because ML Lab 1 needs it" disclaimer.
7. §5.8 line 504 explains the classification-error curve in an under-justified way; rewrite as `Error = min(p, 1-p)` for the two-class case.

**P2 findings:**
1. §5.1/§5.3 expose slide-deck's own `> 80K` vs `>= 80K` boundary inconsistency without commenting.
2. Glossary additions (Hunt's, CART, ID3, C4.5, SLIQ, SPRINT, classification error, underfitting, pre-/post-pruning, hyperparameters) noted in figures.md but no `glossary-additions.md` queued.
3. §5.7 entropy values: slide-rounded vs chapter-precise reporting is inconsistent across the three sub-bullets.
4. Figure 16 caption: would benefit from a "log base 2, two-class" qualifier.
5. §5.3 line 436: claim "Refund → MarSt → TaxInc is what a Gini-driven choice would also pick" is asserted without a Gini calculation backing it.
6. §2 line 83 cross-references "Figure 11 in §5" but the impurity-curves figure is Figure 16, not 11.

**QA Checklist (§7) status:** N/A — this is a lecture-chapter review, not an engineering deliverable. Spec §7.1 checklist applied above instead.

**Acceptance criteria (§1) status:** Spec §7.1 is "every slide covered, every figure embedded properly". Result: slide coverage 61/61 (Met); figure embedding 23/30 catalogued-USE (Not met — 7 missing).

**DOCUMENT.md audit:** N/A for chapter review.

**Out-of-scope observations:** The chapter's connections to L02 (learning agent), L09a (Naive Bayes), L11 (Regression) and L12 (Clustering) in §7 are well-handled. The cross-references in `study/_shared/cross-references.md` were not opened for this review; flagging in case Reviewer #2 or the lab-handoff reviewer wants to verify them.

**Concerns / risks:**
- §4.5/§5.6 contradiction is the kind of bug a tired exam-taker will memorise wrong.
- Figure embedding becomes sparse after slide 47 (no figures for entropy, error, stopping). The chapter loses its visual scaffolding right when the impurity-measure comparison would benefit from one.
- §4.9 walks beyond the lecture — fine if disclaimed, problematic if presented as canonical.

**What PM should do next:**
1. Dispatch the chapter author / lecture-writer to fix **P0-1** immediately (one sentence).
2. Decide the figure policy for the seven P1-1 entries: embed or downgrade-catalogue. Then dispatch the writer to execute.
3. Address P1-2 through P1-7 in the same revision pass.
4. P2 items can wait for Round 2 or be batched into a final polish pass.
5. Re-run Reviewer #1 (concept completeness) after the revision; then proceed to Reviewer #2 (anything else in spec §7).

**DOCUMENT.md updated:** N/A for QA.
