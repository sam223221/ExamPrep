# L12 Clustering — Round 1 — Reviewer #4 (Exam Readiness)

## Report to PM

**Assignment recap:** L12 (Clustering) Round 1, Reviewer #4 lens = exam readiness. Source PDF = Lecture12-Clustering.pdf (47 slides). Chapter = study/lectures/L12-Clustering.md (545 lines, 8 sections).

**Status:** **Fail** — exam-readiness has several P0/P1 defects that would actively *mislead* a student walking into the exam. The chapter is rich, well-structured, and pedagogically generous, but on the items a student is most likely to be tested on (the K-means worked example, the agglomerative dendrogram, the DBSCAN core-point definition, and the "Which solutions to the initial-centroid problem" list) it contains factual drift from the slides, an internally inconsistent iteration table, and a worked SSE that is computed for the wrong centroids. Round 1 cannot ship to App Tester until P0s are fixed.

---

### P0 findings (exam-poisoning errors — must fix)

**P0-1 — Worked K-means iteration table (§5.1) is mis-numbered AND the table's "t=5 converged" row contradicts the slides.**
File: `study/lectures/L12-Clustering.md`, lines 350–358.

The chapter table reads:
| t | μ1 | μ2 |
|---|---|---|
| 0 | 2.00 | 4.00 |
| 1 | 2.5 | 16 |
| 2 | 3 | 18 |
| 3 | 4.75 | 19.60 |
| 4 | 7 | 25 |
| 5 | 7 | 25 (converged) |

But slide 9 explicitly labels:
- **t=1**: μ1=2, μ2=4 (the initial centroids, BEFORE the first assignment-and-update)
- **t=2**: μ1=2.5, μ2=16
- **t=3**: μ1=3, μ2=18

And slide 10:
- **t=4**: μ1=4.75, μ2=19.60
- **t=5 (converged)**: μ1=7, μ2=25

So the *slide labelling convention* is that iteration t is the *state after t-1 updates*, i.e. iteration t=1 is the **starting** state. The chapter shifts every label by one (its "t=1" is the slides' "t=2"). On an exam where the lecturer asks "what is μ1 at iteration t=3?", a student who memorised the chapter will answer 4.75; the slide-correct answer is 3. **This is a guaranteed wrong-answer pipeline.** Either re-align the table to slide labelling OR add an explicit note "convention here differs from the slides — slide t=k corresponds to chapter t=k-1." Currently nothing of the sort is said.

Additionally the chapter adds a sixth row "5 (no change)" which does not exist on the slides. Slide 10 declares t=5 itself "converged". Either drop the duplicate row or be explicit that this is just a re-check.

**P0-2 — SSE computation (§5.1, lines 363–366) is correct for the FINAL converged state, but the chapter never tells the student that the converged centroids are μ1=7, μ2=25. The reader has to back-derive that from the table. Worse — the formula plugs in `(25-25)^2 = 0` for the point at x=25, implying the student must know that 25 is the centroid of {20,25,30}.**

Verification: mean{20,25,30} = 25 ✓ and mean{2,3,4,10,11,12} = 42/6 = 7 ✓ so SSE = 25+16+9+9+16+25 + 25+0+25 = 150 is arithmetically correct. **But** the chapter never writes the converged partition C1={2,3,4,10,11,12}, C2={20,25,30} *as a labelled result*, only inside a "Final SSE" formula. For an exam where the question is "what are the final clusters?" the student has to dig. **Add the converged partition explicitly as a clean stated result before the SSE.**

**P0-3 — DBSCAN core-point definition contradicts itself between the table (§3.7 line 176) and Figure 4 caption (line 181).**

- Line 176 table: "Has more than **MinPts** points within distance Eps (counts the point itself in some textbooks; the slides phrase it as 'more than')."
- Line 181 caption: "the core point's Eps-circle contains **≥ MinPts** neighbours".

These are different: "more than MinPts" means strictly > MinPts; "≥ MinPts" means at least MinPts. The slide-37 figure shows MinPts=4 with a core-point's circle containing exactly 4 points (so "≥ 4" works but "> 4" does not). The slide-36 *text* says "more than" though. This contradiction will cost a student a true/false exam point. **Resolve to one convention with an explicit sentence: "The slides write 'more than MinPts' but the figure on slide 37 illustrates ≥ MinPts; the standard textbook convention is ≥ MinPts (counting the point itself). Use ≥ MinPts unless the question literally quotes 'more than'."**

**P0-4 — Agglomerative trace (§5.2, lines 384–391) merges in the wrong order vs the dendrogram on slide 23.**

The chapter says:
- Step 1: merge {3,4} at 1.48
- Step 2: merge {1,2} at 1.49
- Step 3: merge {1,2} ∪ {3,4} at 1.81
- Step 4: merge with {5} at 4.82

But slide 23 shows d(2,3)=2.29 not 2.99 — verified correct. **However** the slide-23 dendrogram visually shows 5 merging in at distance ≈4.8 against the entire 1-2-3-4 supercluster. With MIN linkage, d({1,2,3,4}, {5}) = min(5.05, 4.82, 4.94, 4.83) = **4.82** ✓ Chapter's value matches.

So the trace itself is correct, but the chapter never states *which linkage the slide uses*. The dendrogram on slide 23 was drawn by the lecturer without specifying the linkage. A student who applies *complete-link* MAX would get d({1,2,3,4}, {5}) = max(5.05, 4.82, 4.94, 4.83) = 5.05, not 4.82. **State explicitly: "The slide-23 dendrogram is the MIN-linkage outcome (verified by reconstruction)."** Currently the chapter says "Trace agglomerative clustering with MIN" but does not justify why MIN is the right reading of the slide.

**Also a P0 sub-issue:** in step 3 of the trace (line 390) the chapter writes
> $d(\{1,2\}, \{3,4\}) = \min(1.81, 1.99, 3.42, 2.29) = 1.81$

That min is over d(1,3)=3.42, d(1,4)=1.81, d(2,3)=2.29, d(2,4)=1.99. Min = 1.81 ✓. **Verified correct.**

**P0-5 — §4.3 "Solutions to initial-centroid problem" lists FIVE remedies but slide 17 lists FIVE bullets including bisecting K-means, AND the chapter then adds K-means++ as a sixth (parenthetical). Fine — but item 3 in the chapter list is mis-quoted.**

Slide 17 reads: "Select more than k initial centroids and then select among these initial centroids — Select most widely separated."

Chapter line 240 paraphrases this as: "**Over-select and prune.** Pick > K candidate centres, then choose K of them that are most widely separated."

This is correct but the chapter has reordered the slide bullets. Slide order is:
1. Multiple runs
2. Sample + hierarchical for init
3. Select more than k initial centroids
4. Postprocessing
5. Bisecting K-means

Chapter order matches (lines 237–241). ✓ — but the chapter's "selected most widely separated" phrasing implies you select the k most-mutually-separated from a candidate pool. The slide is mute on *how* you select; literal reading = "select most widely separated" = select centres that are most separated. Minor but if exam asks "what does the lecturer recommend?" the literal slide answer is the sparse 5-bullet list. **Quote the slide verbatim for these five.**

---

### P1 findings (important — should fix before final)

**P1-1 — Convergence claim is too strong (§4.1, lines 211).**
> "Convergence is guaranteed (SSE decreases at every step and the set of possible assignments is finite), but only to a local minimum"

K-means SSE is **non-increasing**, not "decreases at every step". On a non-improving iteration centroids can stop moving (zero update). Fix wording to "SSE is non-increasing and bounded below, so the algorithm terminates."

**P1-2 — Complexity row in §4.7 (line 329) gives agglomerative complexity as O(n² log n) time and O(n²) space, with no source.**
The slides do not give complexity. The textbook value most commonly cited is O(n³) for naive agglomerative or O(n² log n) with priority-queue update. The chapter picks the latter without justification. If the exam asks "what is the time complexity?" the slide-grounded answer is "not on the slides". **Add a footnote: "Complexity figures are textbook standard, not on the slides."**

**P1-3 — DBSCAN complexity row (§4.7 line 329) also not on the slides.** Same fix: footnote.

**P1-4 — §6.4 (line 446) says "When the exam says 'draw the dendrogram', state the linkage rule first." Good advice, but the slide-23 example in the chapter itself does NOT state its linkage rule until well into §5.2. Self-inconsistent — see P0-4.**

**P1-5 — §3.4 (line 139) flags "dendogram" as a typo in the slides — correct, slides 20, 23 do spell it "dendogram". Good catch. But §5.2 figure 11 caption (line 396) and §5.2 figure 12 caption (line 401) silently use "dendrogram" without re-flagging. Just consistency — one explicit "the slides spell it 'dendogram' throughout" note is enough.**

**P1-6 — §4.5 Bisecting K-means algorithm (lines 282–288) is explicitly labelled "reconstructed from the literature" — fine, but the chapter then describes it as if it were authoritative. An exam grounded on this lecture cannot test bisecting K-means in detail because slides 17–18 give only the *name* and one picture. The chapter should make clear: "Slide-grounded knowledge of bisecting K-means is: name + reduced-init-sensitivity + the slide-18 picture. The 5-step algorithm below is for understanding, not for quoting on the exam."**

**P1-7 — §5.2 (line 398) "Slides 24–27 generalise the same trace with abstract clusters C1, … C5 and explicitly visualise the merger of the two closest clusters C2 ∪ C5". Slide 24 starts with p1–p12 (twelve points), not C1–C5; the abstract C-clusters appear only on slides 25–27. Minor factual drift — fix wording.**

**P1-8 — DBSCAN k-distance plot (Figure 9, line 316) caption reads "elbow at distance 7–10 gives Eps ≈ 7–10". The slide-41 annotation says "Eps ~ 7-10, MinPts = 4". The chapter's claim that the elbow is in the 7-10 *range* is consistent with the slide, but a student reading "elbow at distance 7-10" might think the elbow has width. Tighten: "knee around d ≈ 7-10, slide annotates Eps ≈ 7-10".**

**P1-9 — §6 Pitfalls #11 (lines 453–464) claims "Five aspects to evaluate" from slide 45 and lists them — verified against slide 45 ✓. But the chapter then says "The slides do not name specific validity indices; silhouette, Calinski–Harabasz, Davies–Bouldin, and (with labels) ARI / NMI are the textbook answers." This is *helpful*, but for an exam graded strictly on slide content, naming these on a question that asks "what does the lecture cover for cluster validity?" would be wrong. **Add: "If asked what *this lecture* says, name only: tendency, external comparison, internal comparison, two-clustering comparison, choosing K. Do NOT volunteer silhouette/CH/DB unless the question asks for textbook indices."**

**P1-10 — §6 Pitfall #9 (line 451) "All three algorithms degrade — K-means worst, DBSCAN slightly less, hierarchical least but still." This ranking is *not on the slides*. Slide 19 only shows a network picture and the title "What do to in high-dimensional data?" with no ranking and no resolution. The chapter is volunteering a relative ranking the lecturer did not give. **Flag as exam-trap: "Lecture does not rank the algorithms by dimensional robustness; do not write a ranking on the exam."**

**P1-11 — Glossary block (line 5) lists "centroid linkage" as inline glossary. But §4.4 calls it "Distance between centroids" in the table (line 256) — matches slide 28 phrasing. Two names for the same thing should be cross-referenced in the text once.**

**P1-12 — §2 (line 90) claims "centroid distance can decrease as you merge — the merged centroid is closer to a third cluster's centroid than either parent was. That creates inversions in the dendrogram". True statement, NOT on the slides. The slide-28-32 deck simply lists centroid linkage as one of four options without flagging the inversion property. Mark this as "off-slide enrichment, exam-irrelevant".**

---

### P2 findings (polish)

**P2-1** — §1 line 14 "[Figure 1] The same point cloud admits two-, four-, or six-cluster interpretations". Slide 3 also shows the panel labeled "How many clusters?" (the implicit baseline). Mention all four panels: how-many, 2, 4, 6.

**P2-2** — §2 (line 92) "[Lecture 12, slides 1-34, used throughout the rest of this chapter.]" — citation block looks pasted; slide range is too generous. Trim.

**P2-3** — Algorithm comparison table (§4.7, line 322) is excellent for exam cheat-sheet usage. Consider also adding a "Deterministic?" row that explicitly says "K-means: No; agglomerative: Yes given linkage; DBSCAN: Yes". Wait — that row exists at line 328 ✓. Good.

**P2-4** — §8 Cheat-sheet (lines 484–541) duplicates a *lot* of §4–§6 material. For exam cramming this is excellent. No fix needed but flag that any future edit must keep the two in sync.

**P2-5** — Line 5 inline-glossary list contains "MIN / single-link, MAX / complete-link". These are stylistically inconsistent with "group-average linkage" (no slash). Pick one style.

**P2-6** — Figure 8 caption (line 291) refers to "Voronoi-style cuts" — slide 18 doesn't use the term Voronoi. Minor enrichment beyond the slide; either keep with a note or replace with "radial decomposition".

---

### Standing checks

**Coverage of every slide.** Verified:
| Slide | In chapter? | Where |
|---|---|---|
| 1 (title) | implicit | §1 line 11 cites slide 1 |
| 2 (intra/inter) | ✓ | §1, §3.1 |
| 3 (ambiguous) | ✓ | §1 Fig 1, §6 pitfall 3 |
| 4 (types) | ✓ | §3.2 |
| 5 (partitional) | ✓ | §3.2 Fig 2 |
| 6 (hierarchical) | ✓ | §3.4 |
| 7 (algorithms) | ✓ | §3.2 |
| 8 (K-means pseudocode) | ✓ | §4.1 Fig 5 |
| 9–10 (1-D example) | ✓ but P0 mis-numbered | §5.1 |
| 11 (issues) | ✓ | §4.2 |
| 12 (sub-opt vs opt) | ✓ | §4.2 Fig 6 |
| 13–16 (init importance) | ✓ collapsed into §4.2 | §4.2 |
| 17 (solutions) | ✓ | §4.3 |
| 18 (bisecting picture) | ✓ | §4.5 Fig 8 |
| 19 (high-dim) | mentioned | §6 pitfall 9, §1 (omitted figure) |
| 20 (dendrogram) | ✓ | §3.4 Fig 3 |
| 21 (two main types) | ✓ | §3.5 |
| 22 (algorithm) | ✓ | §3.6 |
| 23 (5-company example) | ✓ but P0 | §5.2 |
| 24–27 (intermediate situation) | ✓ | §5.2 Fig 12 |
| 28–32 (inter-cluster similarity) | ✓ | §4.4 Fig 7a–7e |
| 33 (Ward) | ✓ | §4.4 table |
| 34 (problems & limits) | ✓ | §6 pitfall 5 + §4.7 |
| 35 (DBSCAN intro) | ✓ | §3.7 |
| 36 (core/border/noise) | ✓ but P0-3 | §3.7 table |
| 37 (core/border/noise figure) | ✓ | §3.7 Fig 4 |
| 38 (GTA core/border/noise) | ✓ | §5.3 Fig 13a, 13b |
| 39 (density-connected) | ✓ | §3.7 |
| 40 (algorithm) | ✓ | §4.6 |
| 41 (knee plot) | ✓ | §4.6 Fig 9 |
| 42 (works well) | ✓ | §5.3 Fig 14 |
| 43 (does NOT work) | ✓ | §5.4 |
| 44 (validity intro) | ✓ | §6 pitfall 11 |
| 45 (five aspects) | ✓ | §6 pitfall 11 |
| 46 (final quote) | ✓ | §6 pitfall 11 |
| 47 (thanks) | n/a | n/a |

**No slide is silently skipped.** Slide 19's content (the high-dimensional picture) is only obliquely referenced in §6 — slide 19 deserves at least one explicit "Slide 19 raises the question of what to do in high-dimensional data and does not answer it" line so the student knows there is no examinable content there. Currently the line 451 mention is good but does not cite slide 19 as "open question".

**Cross-references to other lectures.** §7 is well done. Minor: line 478 "L05 Local Search §3" — verify L05 actually has a §3 on local search before final.

**Glossary alignment.** Inline-glossary list at line 5 declares 19 inline terms. I did not verify each against `_shared/glossary.md` (cross-file). Reviewer 5 should.

**Figures.** All 15 figures referenced are present in the extracted_figures path naming convention (slide_pNN.png and fig_pNN_iN.png). I did not file-verify the binaries — flagged for reviewer responsible for asset audit.

**Production-readiness.** No TODO, no // ...rest, no placeholder text found in the chapter. ✓

---

### Acceptance criteria status (§1 Plan implicit)

- Cover every slide of L12: **Met with caveats** (slide 19 underweighted; see standing checks).
- Slide-grounded definitions for clustering, K-means, centroid, hierarchical, agglomerative, dendrogram, DBSCAN: **Met**.
- Worked examples for K-means and agglomerative: **Met, but P0-1 mis-labels K-means iterations**.
- Cluster validity covered: **Met** (slides 44–46 quoted).
- "What this lecture omits" honesty: **Met and good** — §1 lines 22–26 and §6 pitfall 12 explicitly call out K-means++, elbow, silhouette as off-slide.

---

### DOCUMENT.md audit

N/A — this is a study chapter, not a code directory. No DOCUMENT.md expected.

---

### Out-of-scope observations

- The chapter introduces "K-medoids" in §6 pitfall 8 (line 450) as an alternative to K-means for noisy data. K-medoids is *not on the slides*. Flag it explicitly as off-slide, or drop it.
- §6 pitfall 7 (line 449) names "OPTICS" as the standard follow-up to DBSCAN-on-varying-density. OPTICS not on the slides. Same flag.
- The chapter speaks of "z-score (or min-max) features first" (§6 pitfall 10, line 452) — feature scaling is not on the slides; flagged correctly as "Not on the slides but exam-relevant".

---

### Concerns / risks

1. **Exam-readiness risk: the K-means iteration mis-labelling (P0-1) is the single most likely exam-failure trigger in this chapter.** The lecturer's table on slide 9–10 uses t=1 as the *initial* state. A student who memorises this chapter and is asked "What is μ2 at t=2?" will write "16" when the slide answer is "4". That is a guaranteed point loss.

2. **The DBSCAN definition ambiguity (P0-3) is a coin-flip on every exam true/false question about core points.** Resolve to one convention with an explicit "Slide says X but figure says Y; here is what I would write".

3. **Bisecting K-means over-explained.** The slides give it half a sentence + a Wikipedia picture. The chapter gives it five paragraphs and a 5-step algorithm. A student who memorises the chapter's bisecting K-means algorithm and quotes it in an exam might *lose* points for putting in non-slide content. P1-6 should fix.

4. **Linkage of the 5-company dendrogram is never declared by the lecturer.** P0-4. Even if it's MIN, that should be stated as a *reconstruction*.

5. **The chapter is 545 lines with extensive analogies, omission-flagging, cheat-sheet, and cross-references. For a 47-slide deck this is generous — possibly *too* generous for exam revision. A student short on time will struggle to extract the slide-grounded core from the surrounding enrichment.** Consider a future "tight" version that strips analogies and off-slide content to ~150 lines.

---

### What PM should do next

1. **Dispatch the engineer who owns this chapter to fix P0-1 through P0-5.** Re-align the K-means iteration table to slide labelling (or add an explicit conversion note). State the converged partition before the SSE computation. Resolve the core-point ≥ vs > MinPts contradiction. Declare the slide-23 dendrogram as MIN-linkage. Quote slide 17's five remedies verbatim.
2. After P0 fixes, **dispatch Reviewer #4 (me) for a Round 2 re-pass on the §5.1 and §5.2 traces specifically** — these are the highest-yield exam targets.
3. P1 items can be batched in the same fix cycle if convenient, but P0 is the blocker.
4. **Do NOT proceed to App Tester** until P0-1, P0-3, P0-4 are resolved — those three will mislead the student even on a perfectly-graded test.

**DOCUMENT.md updated:** N/A for QA.
