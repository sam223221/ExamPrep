# Lab Reviewer #3 — Pedagogical Clarity (MENTAL MODEL ↔ L12)

**Lab:** MLLab3-Clustering (Round 1)
**Notebook reviewed:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab3_clustering_solution.ipynb`
**Lecture anchor:** `study\lectures\L12-Clustering.md`
**Reviewer mandate:** Pedagogical clarity — does the lab's MENTAL MODEL match L12's MENTAL MODEL, do core concepts get the same names/definitions, are L12's pitfalls surfaced where they bite, do the analogies survive the transition from lecture to code?
**Tone:** Harsh. The student will see this exam in two weeks; sloppy framing here costs marks there.

---

## Verdict up front

**Status: Fail with significant pedagogical gaps.**

The notebook is *technically* correct and operationally well-built (KNOBs, sanity-checks, captioned plots). But as a pedagogical bridge between L12 and the exam it is **shallow on the lecture's mental model**, **silent on five of the six exam-classic pitfalls L12 §6 lists**, and **occasionally misrepresents L12's vocabulary**. A student who reads this notebook *instead* of L12 will pass the lab and fail the conceptual half of the exam.

The single-line analogy in the header is the *only* pedagogical bridge to L12. There is no breakdown of where it fails (L12 §2 always pairs an analogy with its breakdown — this lab does not), no mention of the three-family taxonomy (partitional / hierarchical / density-based), no reference to centroid as "gravitational centre", no contrast with hierarchical or DBSCAN, and the local-minimum trap (L12's §6.1 headline mistake) is only obliquely hinted at via a KNOB tooltip.

---

## P0 — Pedagogical gaps that will cost exam marks

### P0-1. The MENTAL MODEL section is one line. L12's mental model is a whole chapter.

**Location:** `sol-header` markdown cell, lines under `## MENTAL MODEL (one-line analogy):`.

**Evidence (from notebook):**
> **K party-hosts each claim the nearest guests, then re-arrange until nobody wants to switch.** Pick `K` host-spots. Every guest joins the closest host. Each host then moves to the geometric centre of their guests. Repeat. When no guest changes host, the party is settled — the hosts are the **centroids**, the guests around each host are a **cluster**. (This is consistent with the analogy used in the L12 — Clustering lecture chapter §2.)

**What L12 actually does** (lecture §2): pairs **six** analogies — sorting laundry (the *task*), party hosts (K-means), family tree (hierarchical), gravitational centre (centroid), dense-neighbourhood explorer (DBSCAN), upside-down family tree (dendrogram) — and for **every single one** it adds a "*Where it breaks down*" paragraph so the student does not over-extrapolate.

**Why this is P0:** The lab reduces L12's pedagogy to a single sentence about one algorithm. The student running this notebook never encounters the laundry analogy (the *task* framing), never sees the "where it breaks down" caveat that L12 §2 enforces on every analogy, and is given zero mental model for hierarchical or DBSCAN — which the lecture covers as equal-weight algorithms. The exam will not restrict itself to K-means.

**Suggested fix:** Replace the one-liner with a `## MENTAL MODEL` section that pulls in (a) the laundry analogy for the unsupervised *task*, (b) the party-host analogy for K-means *with its breakdown — "real-world clusters can be non-convex; K-means assumes spherical"*, (c) the gravitational-centre analogy for centroid, (d) at minimum a one-sentence acknowledgement that hierarchical / DBSCAN exist and have their own mental models in L12 §2. Cite L12 §2 by section, not just "consistent with §2".

---

### P0-2. Local-minimum trap (L12 §6.1, the headline exam mistake) is never named.

**Location:** absent. Closest mention is buried in the `N_INIT` KNOB tooltip ("With N_INIT=1 you can occasionally reproduce a textbook poor local optimum") and the T6 cell's text ("our scratch version does one run from Forgy random init").

**What L12 does:** §6 pitfall #1 — **"Forgetting that K-means converges to a local minimum."** Followed by: "*SSE is non-increasing at every step ... but the basin K-means settles in depends entirely on the initial centroids — slide 12. The exam-classic mistake is 'K-means finds the optimal clustering'; it does not.*" L12 marks this as the #1 exam trap.

**Why this is P0:** This is the lecture's number-one exam-trap. The lab never says the words "local minimum", never references slide 12, never asks the student to *demonstrate* the trap (the perfect demonstration would be: set `INIT_SCHEME='random'`, `N_INIT=1`, sweep `RANDOM_STATE`, watch inertia vary). The notebook's KNOBs make this demonstration *trivially* easy to author, yet no cell does so.

**Suggested fix:** Add a short markdown cell after T2 titled "Pitfall — K-means is local search" that (a) names the local-minimum trap, (b) cites L12 §6.1 and the L05 Local Search connection L12 explicitly draws, (c) instructs the student to set `INIT_SCHEME='random', N_INIT=1` and run the elbow cell with three different `RANDOM_STATE` values to *observe* the variability. The whole point of the lab is to make abstract claims concrete; the most important abstract claim is missing.

---

### P0-3. L12's three-family taxonomy (partitional / hierarchical / density-based) is invisible.

**Location:** absent. The notebook mentions "partitional vs hierarchical" only as a REFERENCES bullet ("L12 — Clustering: §3 Core Concepts — cluster, centroid, intra/inter-cluster distance, partitional vs hierarchical, K-means objective...").

**What L12 does:** §3.2 + cheat sheet §8 organise the entire lecture around three families. The exam table on L12 §4.7 contrasts K-means / Agglomerative / DBSCAN on six axes (need K?, shape, noise?, sensitive to outliers?, deterministic?, complexity).

**Why this is P0:** A student who works through this lab learns "K-means and how to pick K". A student who reads L12 learns "there are three families of clustering algorithms; K-means is one; here is when to use which". The exam will ask the second-flavour question ("the data has noise — which algorithm?"); the lab will not have prepared the student for it.

**Suggested fix:** Add a markdown cell near the top — *before* the warm-up — titled "Where K-means sits" that reproduces L12's three-family taxonomy (one sentence each) and explicitly says "this lab exercises only the partitional family; hierarchical clustering and DBSCAN are L12 §3.5–§3.7 and §4.4–§4.6". Add a closing markdown cell pointing back to L12's §4.7 comparison table.

---

## P1 — Significant clarity / vocabulary issues

### P1-1. "Centroid" is never tied to L12's gravitational-centre analogy or to the SSE-minimisation justification.

**Location:** the word "centroid" first appears in the warm-up cell (`cell-warmup`) without definition, then in the T1 fit cell with `centers_raw_t1 = scaler2.inverse_transform(kmeans2.cluster_centers_)` — no markdown explains *why* this is the mean.

**What L12 does:** §3.3 gives the formula $\mu_k = \frac{1}{|C_k|} \sum_{x \in C_k} x$ and ties it to the *gravitational-centre* analogy, and crucially says: "*the centroid is the position that minimises the sum of squared distances to the members of the cluster, which is why K-means updates centroids to means rather than to (say) medians.*"

**Why this matters:** The lab uses the word "centroid" 30+ times without ever explaining why "mean" is the right choice. Exam variant *"why does K-means use the mean and not the median?"* — the L12 answer is "because the mean minimises SSE, and K-means is coordinate descent on SSE". The lab does not equip the student with this answer.

**Suggested fix:** Add a one-paragraph markdown cell before T1 titled "What is a centroid?" — define the formula, name the SSE-minimisation property, refer to L12 §3.3, and link "centroid" to "geometric centre of the guests in the party-host analogy".

---

### P1-2. "Inertia" is used heavily; "SSE" / "within-cluster sum of squares" is never spoken.

**Location:** every fit cell prints `inertia`. The header says "K-means objective (within-cluster sum-of-squares = inertia)" in passing.

**What L12 does:** §4.1 defines the objective as **SSE**, gives the formula $\text{SSE} = \sum_{k=1}^{K} \sum_{x \in C_k} \|x - \mu_k\|_2^{2}$, and notes parenthetically "(also called *inertia* or SSE in the labs)".

**Why this matters:** The exam will use the word **SSE** (it is on the slides; "inertia" is not — it is sklearn vocabulary). A student who has only ever seen `inertia` in code may freeze when the exam asks "compute the SSE of the converged clustering". L12 §5.1 worked example computes SSE by hand and gets 150 — the lab never asks the student to recompute it from the centroids and verify it matches sklearn's `.inertia_`. That would be a *perfect* one-line cell.

**Suggested fix:** (a) In the T1 verify cell, change the print to `Inertia (sklearn) = SSE (L12 §4.1): {kmeans2.inertia_:.1f}`. (b) Add a tiny verification cell that recomputes SSE manually with `np.sum((X2_scaled - kmeans2.cluster_centers_[kmeans2.labels_]) ** 2)` and confirms it equals `.inertia_`. This is the single best way to anchor sklearn vocabulary to lecture vocabulary.

---

### P1-3. The L05 "K-means is local search in disguise" connection is dropped entirely.

**Location:** absent.

**What L12 does:** §4.1 has a blockquote that begins "**K-means is local search in disguise.** Compare with [L05 Local Search] hill climbing: SSE is the objective surface, the assign/recompute loop is coordinate descent on it, every initialisation is a different starting point in the energy landscape, and slide-17's 'multiple runs' remedy is literally L05's *random-restart hill climbing*." §7 reinforces the link.

**Why this matters:** This is a cross-lecture insight the exam writer can lean on. The lab has a perfect place to land it — the T6 from-scratch cell that *literally implements coordinate descent* — and it does not.

**Suggested fix:** In the T6 explainer markdown, add: "*Step 1 (assign) minimises SSE over assignments holding centroids fixed; step 3 (update) minimises SSE over centroids holding assignments fixed. This is coordinate descent on SSE — L12 §4.1 calls K-means 'local search in disguise' and cites L05 Local Search; the `N_INIT > 1` mechanic is L05's random-restart hill climbing.*"

---

### P1-4. Elbow + silhouette: the lab implements them but does not name them as L12-omitted material.

**Location:** T4 explainer cell.

**What the lab says:**
> K-means can't tell you `K`. There are two standard *suggestions* used in practice:
> - **Elbow method.** [...]
> - **Silhouette score.** [...]

**What L12 actually says** (§6 pitfall #3, §1, §6 pitfall #12):
> **Choosing $K$ by eyeballing.** [...] The lecture does **not** prescribe a method for $K$; if the exam asks "how would you choose $K$?", the slide-deck answer is "you have to pick it — it is an input"; the lab-3 answer is "elbow on inertia vs $K$, or silhouette score".

And §1 explicitly flags:
> Elbow method and silhouette score for choosing $K$ or evaluating clusters are **not derived on the slides** [...] ML Lab 3 fills the gap.

**Why this matters:** L12 *explicitly tells the student* that elbow and silhouette are NOT on the slides — i.e. they are exam-relevant only insofar as the lab teaches them. The lab teaches them but does not echo the "not on the slides" warning. A student who treats elbow / silhouette as slide-grounded answers on an exam question phrased *"what does the lecture say about choosing K?"* will lose marks for citing material that was not lectured.

**Suggested fix:** Add a callout to the T4 explainer: "*Important — L12 §1 and §6 pitfall #3 explicitly flag elbow and silhouette as NOT on the slides. If an exam question asks 'what does the lecture say about choosing K?' the slide-grounded answer is 'K is an input — pick it'. Use elbow / silhouette only when the question asks 'how would you choose K in practice?' or names ML Lab 3.*"

---

### P1-5. K-means++ is used by default with no L12 callout that it is not slide material.

**Location:** `INIT_SCHEME = 'k-means++'` (KNOB cell). The header REFERENCES section says "L12 does not formally introduce K-means++ initialisation" — buried, easy to miss.

**What L12 does:** §1 explicitly flags K-means++ as not on the slides; §4.3 lists the *five* mitigations the slide actually gives (multiple runs, sample+hierarchical, over-select-then-prune, post-processing, bisecting K-means) and only parenthetically mentions K-means++ as the "modern default".

**Why this matters:** The default `INIT_SCHEME='k-means++'` silently uses a method the lecture does not name. An exam-variant question *"list the initialisation remedies on slide 17"* will expect the **five slide-grounded** answers, not "k-means++". The lab teaches the modern answer by default and never names the slide-grounded list.

**Suggested fix:** Add the slide-17 verbatim five-mitigation list (multiple runs / sample+hierarchical / over-select / post-process / bisecting) into the T1 explainer markdown, with a sentence: "*these are the five remedies L12 §4.3 lists from slide 17. K-means++ — which sklearn uses by default and which we set via `INIT_SCHEME='k-means++'` — is the modern textbook follow-up but is NOT on the slides.*"

---

### P1-6. No mention of hierarchical clustering or DBSCAN at all.

**Location:** absent (the references section names "partitional vs hierarchical" but no body cell discusses either).

**What L12 does:** Three full sections (§3.5, §3.6, §3.7) on hierarchical and DBSCAN; comparison table §4.7; a full worked agglomerative example (§5.2) and two DBSCAN worked examples (§5.3, §5.4).

**Why this matters:** A student running the lab top-to-bottom encounters zero hierarchical content and zero DBSCAN content. The exam will ask comparative questions ("the data has noise — choose an algorithm"; "draw the dendrogram for these distances"). The lab does not need to *implement* hierarchical or DBSCAN, but it should at minimum end with a comparison-table markdown cell pointing the student at L12's §4.7 and noting which algorithm answers which exam-question shape.

**Suggested fix:** Add a closing "Where K-means fits in the L12 family" markdown cell after T6 with (a) a tiny L12 §4.7 comparison table, (b) one-line summaries of when hierarchical wins (no need to choose K upfront, want a tree) and when DBSCAN wins (noise in data, non-spherical shapes), (c) explicit pointers to L12 §3.5 and §3.7 for the algorithms the lab does not exercise.

---

### P1-7. Feature scaling is justified by the right reason but not connected to L12 §6 pitfall #10.

**Location:** T1 explainer cell:
> **Scale** with `StandardScaler` so that the larger numeric range of `study_hours_per_week` (0–20) doesn't drown out `prior_math_grade` (−3–12) in the Euclidean distance.

**What L12 §6 pitfall #10 says:**
> **Forgetting feature scaling.** Not on the slides, but exam-relevant: K-means and DBSCAN both compute Euclidean distance, which is dominated by the largest-range feature. Always z-score (or min-max) features first when they have heterogeneous units.

**Why this matters:** The lab gives the correct reason but does not cite the lecture's exam-trap framing or the "not on the slides" disclaimer. A two-line cross-reference would close the loop.

**Suggested fix:** Append to the T1 explainer: "*This is L12 §6 pitfall #10 — 'Forgetting feature scaling'. The lecture flags it as exam-relevant but not slide-grounded.*"

---

## P2 — Polish & convention nits

### P2-1. Header reference list does not cite L12 sections precisely.

**Location:** REFERENCES bullet `§3 Core Concepts — cluster, centroid, intra/inter-cluster distance, partitional vs hierarchical, K-means objective (within-cluster sum-of-squares = inertia)`.

§3 contains the *concept* of K-means but the objective and the iteration are in **§4.1**. Mis-citing §3 sends a student looking for the SSE formula to the wrong place.

**Fix:** Change to `§3 Core Concepts (centroid, intra/inter-cluster distance, taxonomy); §4.1 K-means objective and iteration (SSE formula); §4.2 K-means limitations; §4.3 initialisation remedies.`

---

### P2-2. T1 "two_feats = list(FEATURE_PAIR_T1)" is the source of truth, but other cells read from `FEATURE_PAIR_T1` directly.

**Location:** T1 intuition cell uses `demo_feats = list(FEATURE_PAIR_T1)`; T1 fit uses `two_feats = list(FEATURE_PAIR_T1)`; T3 verify reads `two_feats` (the T1 binding). Cross-cell dependency is implicit. Not a bug but a clarity nit.

**Fix:** A short note in the KNOBs cell: "*`two_feats` is defined inside the T1 cell from `FEATURE_PAIR_T1`; T3 and T6 inherit it. Re-run the T1 cell after editing `FEATURE_PAIR_T1`.*"

---

### P2-3. "Dendrogram" never mentioned, so the L12 §3.4 spelling-typo callout cannot be reinforced.

**Location:** absent.

L12 §3.4 has a useful exam-aware nugget: "*the slides spell it 'dendogram' (visible in Figure 11 ... and on the slide-20 / slide-23 rendered images) — that is a typo for dendrogram.*" The lab does not surface this because the lab does not touch hierarchical clustering — but if P1-6 above gets fixed with a comparison cell, the spelling note costs one extra sentence and saves a confused student during the exam.

---

### P2-4. "How to adapt this for different question variants" sidesteps L12's exam pitfalls.

**Location:** sol-header markdown cell.

The adaptation list is excellent at the *operational* level (which KNOB to flip) but never says "here's the L12 exam-trap you should be ready for". A list bullet like "*if the exam emphasises noise / outliers, flag that K-means is the wrong algorithm — L12 §6 pitfall #8 — and recommend DBSCAN*" would do real pedagogical work.

---

### P2-5. T2 cluster naming ("Light effort" / "Moderate middle" / "Dedicated achievers") is hard-coded by study-hours rank.

**Location:** `cell-t5-reveal`. The mapping `study_ranks = centers_df_t2['study_hours_per_week'].rank(...)` assumes the discovered clusters separate primarily on study hours. With the default seed this holds; with `INIT_SCHEME='random'`, `N_INIT=1`, and a hostile `RANDOM_STATE`, K-means could converge to a partition where study hours are *not* the dominant axis. The "Light effort" / "Dedicated achievers" labels would then mislabel clusters. Pedagogically this is the perfect place to surface the local-minimum lesson (P0-2), but the cell is silent on the assumption.

**Fix:** Add a one-line caveat: "*Names are assigned by study-hours rank, assuming K-means recovered the three baked archetypes. If you set `INIT_SCHEME='random', N_INIT=1` and hit a bad local optimum, the labels may not match — L12 §6 pitfall #1.*"

---

## What L12 §6 lists vs what the lab surfaces

L12 enumerates 12 pitfalls in §6. Lab coverage:

| L12 §6 pitfall | Lab coverage |
|---|---|
| 1. K-means converges to local minimum | **MISSING** (KNOB tooltip only) — P0-2 |
| 2. "Converged ≠ correct" | **MISSING** — never said |
| 3. Choosing K by eyeballing | Partial — T4 implements elbow/silhouette but does not give the L12 slide-grounded "K is an input" answer — P1-4 |
| 4. Dendrogram is not canonical | N/A (no hierarchical content) — P1-6 |
| 5. Once-merged-never-undone | N/A (no hierarchical content) — P1-6 |
| 6. Single-link chaining | N/A (no hierarchical content) — P1-6 |
| 7. DBSCAN parameter sensitivity | N/A (no DBSCAN content) — P1-6 |
| 8. "Noise" vs "outlier" in K-means | **MISSING** — never said. Exam-classic question. |
| 9. High-dim curse | **MISSING** — never said |
| 10. Feature scaling | Covered correctly, not cross-referenced — P1-7 |
| 11. Cluster validity is hard | **MISSING** — silhouette is treated as the answer, not as one *index* among many; L12 §6 #11 explicitly warns against "volunteering silhouette/CH/DB/ARI/NMI" |
| 12. Topics this lecture omits | Partially covered (header mentions K-means++, silhouette) — P1-4, P1-5 |

**Eight of twelve L12 pitfalls are absent or weakly present.** The lab is operationally complete; pedagogically it covers roughly a third of L12's exam-trap surface area.

---

## What the lab gets right (give credit where due)

- **Party-host analogy is reproduced verbatim** from L12 §2 and used consistently in the warm-up.
- **The T2 "reveal" is a genuine pedagogical win** — showing that K-means recovers grade-correlated clusters without seeing grades is exactly the L10 "unsupervised learning has structure" payoff.
- **T6 from-scratch implementation** is the right call pedagogically — implementing Lloyd's algorithm in ten lines is the best way to make "K-means is just assign + update" concrete.
- **KNOBs convention is excellent.** Every variant-flip surface is named, defaulted, and documented. This is what a "study notebook" should look like.
- **`StandardScaler` is fit twice (`scaler2`, `scaler6`)** with explicit explanation of why — that's the right level of detail for a student.
- **T3's side-by-side k=2/3/5 panel** is exactly L12's "what does under- vs over-clustering look like" intuition.

---

## Recommended fix order

1. **P0-2 first** (local-minimum trap). Cheapest, highest pedagogical value: one markdown cell + one demonstration cell with `INIT_SCHEME='random', N_INIT=1` and a `RANDOM_STATE` sweep. This single change closes L12 §6 #1, #2, partially #8, partially #11.
2. **P0-1** (expand MENTAL MODEL to multi-analogy with breakdowns). Pure markdown.
3. **P0-3 + P1-6** as a single change: add a top "Where K-means sits" cell and a bottom "Where K-means fits in the L12 family" cell. Brings the three-family taxonomy into the lab without implementing hierarchical/DBSCAN.
4. **P1-1, P1-2, P1-3, P1-4, P1-5, P1-7** can all be addressed as cross-reference annotations in existing markdown explainers — one or two sentences each, no new cells needed.
5. **P2 polish** last.

---

## Report to PM

**Assignment recap:** Lab Reviewer #3 (Pedagogical Clarity) for MLLab3-Clustering, Round 1. Mandate: cross-check MENTAL MODEL ↔ L12-Clustering. Notebook: `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab3_clustering_solution.ipynb`; lecture: `study\lectures\L12-Clustering.md`.

**Status:** Fail with significant pedagogical gaps. Notebook is technically correct and operationally well-built but covers ~1/3 of L12's pedagogical surface area and misses the lecture's #1 exam-trap.

**P0 findings:**
1. `sol-header` MENTAL MODEL cell — single-line K-means analogy with no breakdown; L12 §2 has six analogies each with a breakdown clause. Fix: expand to a multi-analogy section.
2. **No cell anywhere** — local-minimum trap (L12 §6 pitfall #1, the headline exam mistake) is never named. Fix: add a "K-means is local search" markdown cell + a `RANDOM_STATE` sweep cell with `INIT_SCHEME='random', N_INIT=1`.
3. **No cell anywhere** — L12's three-family taxonomy (partitional / hierarchical / density-based) is invisible. Fix: add a top "Where K-means sits" cell.

**P1 findings:**
1. T1 / warm-up — "centroid" used 30+ times; never tied to L12 §3.3 gravitational-centre analogy or to the "mean minimises SSE" justification.
2. All fit cells — uses "inertia" exclusively; L12 §4.1 uses "SSE". Fix: print both labels; add a one-line verification cell that recomputes SSE manually.
3. T6 explainer — drops L12 §4.1's "K-means is local search in disguise" cross-reference to L05.
4. T4 explainer — implements elbow + silhouette but does not echo L12 §1 / §6 #3's "not on the slides" disclaimer; risks the student citing non-lecture material on a "what does the lecture say about K?" question.
5. KNOB `INIT_SCHEME='k-means++'` default — uses a method L12 explicitly flags as not on the slides; the five slide-grounded mitigations from L12 §4.3 / slide 17 are never enumerated in the lab.
6. **No cells for hierarchical or DBSCAN** even as a comparison-table footnote; L12's §4.7 comparison table is the obvious exam scaffold and is absent.
7. T1 feature-scaling rationale — correct, but not cross-referenced to L12 §6 pitfall #10.

**P2 findings:**
1. Header REFERENCES bullets cite §3 for material that is actually in §4.1.
2. `FEATURE_PAIR_T1 → two_feats` cross-cell dependency is implicit.
3. L12 §3.4 "dendogram" spelling-typo callout cannot be reinforced because no dendrogram cell exists.
4. "How to adapt this for different question variants" lists KNOB flips but never lists L12 exam-traps the student should be ready to invoke.
5. T5 cluster naming hard-codes `study_hours_per_week` ranking — silently assumes the local optimum K-means hit. Perfect place to surface P0-2's lesson.

**QA Checklist (§7) status:** N/A — this is a pedagogical-clarity review, not a code-correctness review. The notebook executes cleanly per its own self-report; correctness is for Reviewer #1 / #2.

**Acceptance criteria (§1) status:** N/A — same reason.

**DOCUMENT.md audit:** N/A — pedagogical review.

**Out-of-scope observations:**
- The cluster-naming assumption in `cell-t5-reveal` (P2-5) is the closest the lab comes to a *latent bug*: if a student flips `INIT_SCHEME='random', N_INIT=1` and seeds badly, the printed cluster names ("Dedicated achievers" etc.) may mismatch the actual archetypes. This is mostly cosmetic but could confuse a panicked exam-prepper. Flagging for Reviewer #2 (correctness) to confirm.
- The lab claims "T4 (implicit) — the handout's summary promises" but I cannot see the handout from my brief; if the handout never named T4, the lab is over-delivering, which is fine pedagogically but worth a PM sanity-check against the handout.

**Concerns / risks:**
- The notebook is *so* well-built operationally that a student may treat it as a complete substitute for L12. It is not. The PM should consider adding a banner cell at the top: "*This notebook is the hands-on companion to L12-Clustering, not a replacement. Read L12 §1–§7 first.*"
- The exam writer (per L12's framing) will lean heavily on the L05 cross-reference and on the three-family taxonomy. The lab does not prepare the student for either.

**What PM should do next:**
1. Send fix instructions for P0-1, P0-2, P0-3 to the lab author (these are pure markdown additions; no code changes needed). Re-QA from Reviewer #3 after.
2. Then send the P1 cross-reference patches as a single batch — they are all one-to-two-sentence markdown annotations.
3. P2 nits can roll into the same patch or wait.
4. Do NOT ship Round 1 of this lab to the student as their *only* clustering revision artefact. It must be paired with a re-read of L12.

**DOCUMENT.md updated:** N/A for QA.
