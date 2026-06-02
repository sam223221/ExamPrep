# L10 Reviewer #4 — Exam Readiness (Round 1)

**Reviewer role:** Lecture Reviewer #4 — Exam Readiness (Spec §7.1)
**Lecture under review:** L10 — Introduction to Machine Learning
**Source PDF:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture10-Introduction to Machine Learning.pdf` (61 slides)
**Chapter under review:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L10-Intro-to-ML.md`
**Stance:** HARSH. The chapter is generally strong (analogies, worked examples, formulas) but it has factual drift in several places that will lose marks on an exam if the student parrots it. The questions below are written to surface exactly those weak spots.

---

## 10 Exam Questions (with model answers + chapter audit)

For each question I give: (a) the question; (b) the model answer keyed to the slide; (c) whether the chapter, as written, would let a student answer this correctly; (d) any harsh findings on the chapter.

---

### Q1. (Definition) State the two-part definition of machine learning given in this lecture, and explain in one sentence how ML differs in stance from the agents you saw in earlier lectures (search, CSP, Bayes-net).

**Model answer (slide 2):**
ML is (i) getting a computer to do well on a task **without explicitly programming it**, and (ii) **improving performance on a task based on experience**. In earlier lectures the designer hand-codes the agent's rules (heuristics, propagators, network structure); in ML the agent is given data and infers its rules.

**Chapter status:** PASS. §1 paragraph 1 covers this almost verbatim and explicitly contrasts it with the earlier lectures.

**Finding:** None. Strong.

---

### Q2. (Three branches) For each of supervised, unsupervised, and reinforcement learning, give (a) what feedback the learner receives, (b) one example task, and (c) for RL only, the three structural difficulties named on slide 7.

**Model answer:**
- **Supervised:** training data is (input, output) pairs; learn the mapping. Example: predict house price from features. (Slides 8–9, 11.)
- **Unsupervised:** inputs only, no labels; discover structure such as clusters, outliers, generative distribution, missing-data fill-in. (Slide 4.)
- **Reinforcement:** no fixed dataset; agent has states, actions, rewards; goal is to maximise reward by acting and gathering its own data. Example: chess. (Slides 5–6.) Three difficulties (slide 7):
  1. **Stochasticity** — same action in same state can yield different next-state / reward.
  2. **Temporal credit assignment** — rewards arrive long after the action that earned them.
  3. **Exploration–exploitation trade-off** — keep using a known good strategy vs. try something potentially better.

**Chapter status:** PASS. §3.1 covers all three branches plus the three RL difficulties.

**Finding (P2):** §3.1 phrases stochasticity as "Identical actions in identical states may yield different next-states or different rewards (e.g. chess opponents)." That parenthetical is fine but the slide explicitly splits stochasticity into two bullets (state-stochasticity AND reward-stochasticity); the chapter compresses them into one. Student wouldn't lose marks but a careful examiner could mark this thin.

---

### Q3. (Terminology) Place each task in the right cell of a 2×2 table (regression vs classification, univariate vs multivariate). For full marks name the model family named on the slide for each task:
- (i) predict child's height from age
- (ii) spam vs ham email
- (iii) music genre out of 7 genres
- (iv) per-pixel cow / not-cow image segmentation

**Model answer (slides 11–15):**

| Task | Reg/Class | Uni/Multi | Architecture |
|---|---|---|---|
| (i) age → height | Regression | Univariate | Fully-connected network |
| (ii) spam vs ham | Classification (binary) | Univariate | Transformer |
| (iii) music genre (7-way) | Classification (multi-class) | Univariate | RNN |
| (iv) cow image segmentation | Classification (binary, per pixel) | **Multivariate** | Convolutional encoder–decoder |

**Chapter status:** PASS. §3.2 Table reproduces all of these.

**Finding (P2):** Chapter §3.2 calls image segmentation "Multivariate binary classification (per-pixel)" which matches slide 15 exactly. No issue. Translation row says "(slide gives no specific architecture)" which is accurate — slide 16 is just labelled "Translation" with the diagram and no arch name. Good catch by the writer.

---

### Q4. (Classification, formal) Give the four bullets of the formal definition of a classification task from slide 18, and state why the dataset is split into train and test.

**Model answer (slide 18):**
1. You are given a collection of records (the **training set**); each record has attributes, one of which is the **class**.
2. We **find a model for the class attribute as a function of the other attributes**.
3. Goal: **previously unseen records** should be assigned a class **as accurately as possible**.
4. A **test set** is used to determine the model's accuracy. Usually the given dataset is divided into training and test, with the training set used to build and the test set used to validate.

The split exists because measuring accuracy on the training rows only tells us how well the model memorised them, not how well it generalises — that becomes the overfitting story (slide 56).

**Chapter status:** PASS. §3.3 reproduces all four bullets and the rationale.

**Finding:** None. Strong.

---

### Q5. (Hunt's algorithm) Write Hunt's algorithm in three bullets, exactly as on slide 33, with the variables $D_t$, $y_t$, $y_d$ used in the slide. Then apply it conceptually to the cheat-data example and explain why the slide-34 tree grows in the order **Refund → Marital Status → Taxable Income**.

**Model answer (slide 33):**
Let $D_t$ be the set of training records that reach node $t$.
1. If $D_t$ contains records that all belong to the **same class $y_t$**, then $t$ is a leaf labelled $y_t$.
2. If $D_t$ is the **empty set**, then $t$ is a leaf labelled by the **default class $y_d$**.
3. If $D_t$ contains records of **more than one class**, use an **attribute test** to split $D_t$ into smaller subsets and **recursively apply** the procedure to each subset.

On the cheat data (slide 34): start with the majority leaf "Don't Cheat". Split on Refund: Refund=Yes (Tids 1,4,7) are all "No" → pure leaf. Refund=No is mixed → recurse. Split on Marital Status: Married (Tids 2,6,9) all "No" → pure leaf. Single/Divorced still mixed → recurse. Split on Taxable Income at 80K: <80K (Tid 3) → "No", ≥80K (Tids 5,8,10) → "Yes". All leaves now pure → terminate.

**Chapter status:** PASS. §4.2 reproduces the three bullets, §5.3 walks through the slide-34 sequence step by step.

**Finding (P1 — POTENTIALLY WRONG INTUITION).**
§5.3 ends with "Each split was greedy: at each step the algorithm picked the attribute that most reduced impurity (in the slide, the order chosen is Refund → MarSt → TaxInc, which is what a Gini- or entropy-driven choice would also pick on these 10 rows)." This is an *unverified* claim — the lecturer never says Hunt's algorithm on this dataset must choose Refund first by Gini/entropy. Slide 34 simply *shows* one growth order without claiming it is the impurity-optimal one. If a student writes this and the examiner has actually computed the Gini at the root, the student may be marked down. RECOMMEND softening to "in the slide's chosen ordering" rather than implying it is provably optimal.

---

### Q6. (Gini computation) For a node with 6 records distributed as $(C_1=2, C_2=4)$:
(a) compute Gini.
(b) compute classification error.
(c) compute entropy.
(d) state the maximum value each measure can take for a two-class problem.

**Model answer (slides 42, 49, 51):**
- (a) $\operatorname{Gini} = 1 - (2/6)^2 - (4/6)^2 = 1 - 4/36 - 16/36 = 16/36 \approx 0.444$.
- (b) $\operatorname{Error} = 1 - \max(2/6, 4/6) = 1 - 4/6 = 1/3 \approx 0.333$.
- (c) $\operatorname{Entropy} = -(2/6)\log_2(2/6) - (4/6)\log_2(4/6) \approx 0.918$.
- (d) Max for 2-class: Gini $= 0.5$, Error $= 0.5$, Entropy $= 1$ (i.e. $\log_2 n_c$ with $n_c=2$).

**Chapter status:** PASS. §5.4, §5.7, §5.8 do all three. The cheat-sheet §8 table also lists the max values.

**Finding (P2 — slide-typo handling is correct but ambiguous).**
§5.7 says "the slide rounds to $0.65$; a printing typo in the slide repeats `log2(1/6)` twice — the second factor should be `log2(5/6)`". The chapter is RIGHT to flag this — slide 49 literally writes "Entropy = – (1/6) log2(1/6) – (5/6) log2(1/6) = 0.65" which is a typo because $-(1/6)\log_2(1/6) - (5/6)\log_2(1/6) \neq 0.65$. The correct expression uses $\log_2(5/6)$ for the second term. Good catch; this protects the student from carrying the typo into the exam. PASS.

---

### Q7. (Best-split framework + continuous attribute) State the best-split rule from slide 41 (give the formula for $M_{1\dots k}$ and the definition of *gain*). Then explain the efficient continuous-attribute scan on slide 47 in four steps, and identify the best Gini and the threshold that achieves it for the Taxable-Income column.

**Model answer:**
Best-split (slide 41): given parent impurity $M_0$ and candidate split producing children with impurities $M_1,\dots,M_k$ and record counts $n_1,\dots,n_k$ (with $n = \sum n_i$),
$$M_{1\dots k} = \sum_i \tfrac{n_i}{n} M_i, \qquad \text{Gain} = M_0 - M_{1\dots k}.$$
Pick the candidate with the highest gain (equivalently the lowest $M_{1\dots k}$).

Continuous scan (slide 47):
1. Sort the records by the continuous attribute.
2. Linearly scan in order, incrementally updating the class-count matrix as each record moves from the ">" side to the "≤" side.
3. At each candidate split position compute the Gini in $O(1)$ from the running counts.
4. Choose the split with the **lowest** Gini.

Best for Taxable Income (slide 47): the minimum Gini reported is **0.300** at the split position **97** (between sorted values 95 and 100).

**Chapter status:** PARTIAL FAIL.

**Finding (P0 — FACTUAL ERROR).**
§4.5 says: "The minimum Gini in Figure 14 is **0.300** at the threshold between 85 and 90 (a `Yes / No` count of `1/3 vs 2/4` on the left / right). That is the best split point for `Taxable Income`."

This is **wrong**. Slide 47 puts the underlined Gini = 0.300 squarely in the column labelled **97**, which is the split position **between sorted values 95 and 100** (i.e. ≤95 vs ≥100). The chapter has identified the wrong column. The "85 / 90" boundary is the split position **87**, where Gini = 0.417 on the slide — not the minimum.

In §5.6 the chapter then *correctly* says "The minimum is **0.300** at the threshold around 97 (between the 95K-Yes-cheater and the 100K-No row)". So the chapter contradicts itself between §4.5 and §5.6.

**Impact:** A student copying §4.5 onto an exam will write the wrong threshold and lose every mark on this sub-question. MUST FIX.

**Recommended fix:** Change §4.5 to "The minimum Gini in Figure 14 is **0.300** at the threshold between 95 and 100 (split position 97 in the slide)." Drop the incorrect "1/3 vs 2/4" counts — at split position 97 the table on slide 47 shows Yes: 3|0, No: 3|4 (i.e. ≤97 gets 3 Yes + 3 No; >97 gets 0 Yes + 4 No), not the made-up `1/3 vs 2/4`.

---

### Q8. (Splitting on attribute types) The lecture distinguishes how to split (i) a nominal / ordinal attribute and (ii) a continuous attribute. Give both options for each, and explain why finding the optimal binary split of a $k$-valued categorical attribute is non-trivial.

**Model answer (slides 36–37):**
- **Nominal / ordinal:**
  - **Multi-way split** — one branch per distinct value (Size → {Small, Medium, Large} is three branches).
  - **Binary split** — partition the values into two subsets, e.g. {Small, Medium} vs {Large}. There are $2^{k-1}-1$ non-trivial ways to split $k$ values into two non-empty subsets, so finding the optimal partitioning is a search over exponentially many candidates.
- **Continuous:**
  - **Discretisation** — bucket the values once (static) or per node (dynamic — equal-interval, equal-frequency / percentiles, or clustering) and treat the result as ordinal.
  - **Binary decision $A < v$ vs $A \geq v$** — consider all possible splits, pick the best cut. More compute-intensive but exact.

**Chapter status:** PASS. §4.3 covers both attribute types and explicitly states the $2^{k-1}-1$ count.

**Finding (P2 — minor convention drift).**
The slide writes the binary continuous test as "$(A < v)$ or $(A \geq v)$" with the equality on the upper side. Slide 22's tree, however, draws the branches as `< 80K` and `> 80K` (no equality on either side) which is technically inconsistent with the lecture's own formal binary-decision notation. The chapter §4.3 follows the slide-37 convention $A < v$ vs $A \geq v$ and labels the slide-22 tree the same way — fine, but a student should be aware that the textbook convention is "≤ / >" or "< / ≥" depending on the lecturer's mood. Not a chapter error; flagging for the student.

---

### Q9. (Overfitting causes + remedies) The lecture identifies two distinct causes of overfitting (slides 57 and 58). State both, then list both remedies (pre-pruning and post-pruning) and name two pre-pruning hyperparameters and one post-pruning hyperparameter explicitly mentioned in the slides.

**Model answer (slides 57–60):**
- **Cause 1 — Noise (slide 57):** the decision boundary is distorted by a noise point — a mislabelled or anomalous training example pulls the boundary off the true class structure.
- **Cause 2 — Insufficient examples (slide 58):** in regions where there are too few training records, the classifier draws boundaries based on training records irrelevant to that region's true class structure, so test examples there get misclassified.
- **Pre-pruning (slide 59):** stop the algorithm before the tree is fully grown. Hyperparameters explicitly listed in the slides: `max_depth`, `min_samples_leaf`, `min_samples_split` (slide 53 and slide 59). Other stopping conditions: all instances same class; all attribute values same; instance count below threshold; chi-squared independence test; impurity gain below threshold.
- **Post-pruning (slide 60):** grow the tree fully, then trim subtrees bottom-up if doing so improves generalisation error; the new leaf gets the **majority class** of the subtree's records. Hyperparameter: `ccp_alpha` (Cost Complexity Pruning) and also MDL is named.

**Chapter status:** PASS. §6.2 and §6.3 cover causes and remedies; the cheat-sheet lists the hyperparameters; §4.8 also lists them.

**Finding (P2 — emphasis).**
§4.8 lists `max_depth`, `min_samples_leaf`, `min_samples_split` as bullets and §6.3 lists them as a single grouped bullet. The chapter is internally consistent. No issue.

**Finding (P1 — missing horizon-effect citation).**
§6.3 introduces "**horizon effect**" as a risk of pre-pruning ("one more split *would* have unlocked a hugely informative second-level split"). The horizon effect is a real concept but it is NOT named on any slide in this deck. A student writing "horizon effect" in an exam answer for *this course* may not get credit because the examiner is grading against the lecture content. Mark this as **chapter content beyond the deck** and warn the student to phrase it as their own gloss, not as "the lecturer said".

---

### Q10. (Ensembles + decision-tree limitations) (a) Explain bagging and random forest in one sentence each, including the key randomisation that distinguishes a random forest from plain bagging. (b) State three advantages of decision trees from slide 54. (c) State one limitation of the Student-ID split on slide 38 and explain in one sentence why decision trees built with information gain are biased toward such attributes.

**Model answer:**
- (a) **Bagging:** draw many bootstrap samples (sample-with-replacement) from the training set, fit one tree per bootstrap, predict by majority vote (classification) or average (regression). **Random forest:** bagging plus a second randomisation — at each split of each tree, only a random subset of the attributes is considered as candidates, decorrelating the trees and reducing variance more than bagging alone.
- (b) Slide 54 advantages: **inexpensive to construct**, **extremely fast at classifying unknown records**, **easy to interpret for small-sized trees**, **accuracy comparable to other techniques for many simple datasets** (any three).
- (c) Student ID has 20 distinct values and the slide-38 split puts one record per child, every child perfectly pure. Information gain rewards this because the children's entropy is 0 — but the split is useless on a new student because their ID has never been seen. Information-gain-based trees (ID3) are biased toward high-cardinality categorical attributes because the more children a split has, the easier it is for each child to be near-pure by accident; C4.5 partly fixes this with **information gain ratio**.

**Chapter status:** PARTIAL.

**Finding (P1 — chapter overshoots the lecture).**
§4.9 says of boosting: "Conceptually: train trees sequentially, each one focusing on examples the previous ones got wrong." That is correct AdaBoost intuition, but the slides only **name** AdaBoost/CatBoost/XGBoost (slide 20) — they do not describe how boosting works. A student answering an exam question on boosting using this gloss would be answering beyond what was taught; the examiner cannot mark them wrong but cannot mark them right either. Acceptable risk; flagging.

**Finding (P1 — Student-ID / information-gain bias is NOT explicit in the slides.)**
§6.4 says: "Bias toward attributes with **more values** (slide 38's `Student ID?` split has a perfectly pure child for every student, but the split is useless for new students — a classic ID3-style failure that information gain ratio in C4.5 partly fixes)." This is a real and well-known result, but the slide deck does not actually state it — slide 38 only asks "Which test condition is the best?" without resolving it on the Student-ID column or naming the high-cardinality bias. So if the exam restricts itself to *deck content*, the student should answer Q10(c) cautiously: the slide-38 image shows the failure visually but the formal "information gain is biased toward high-cardinality" claim is not in the lecture. The chapter should soften this to "this is an observation about slide 38 that the slides do not explicitly resolve" rather than asserting it as lecture content.

---

## QA Checklist (Spec §7.1 — Exam Readiness)

| Item | Status | Note |
|---|---|---|
| 10 exam questions provided | Pass | Q1–Q10 above. |
| Questions span the lecture | Pass | Coverage: definition (Q1), three branches (Q2), supervised taxonomy (Q3), classification formal (Q4), Hunt's (Q5), three impurity computations (Q6), best-split framework + continuous scan (Q7), splitting on attribute types (Q8), overfitting (Q9), ensembles + DT pros/cons + ID bias (Q10). No major topic untouched. |
| Each question has a model answer keyed to a slide | Pass | Every model answer cites the slide number. |
| Each question audited against the chapter | Pass | Each Q has a chapter-status verdict. |
| Severity-tagged findings | Pass | P0 in Q7, P1 in Q5/Q9/Q10, P2 in Q2/Q3/Q6/Q8. |

---

## Severity-Tagged Findings (across the chapter, not just per-question)

### P0 — Broken / will lose exam marks

**P0-1. §4.5 identifies the wrong threshold for the slide-47 best Gini.** (Q7 above.)
- File: `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L10-Intro-to-ML.md` line 314.
- Text: *"The minimum Gini in Figure 14 is **0.300** at the threshold between 85 and 90 (a `Yes / No` count of `1/3 vs 2/4` on the left / right). That is the best split point for `Taxable Income`."*
- Slide 47 puts Gini = 0.300 at split position **97** (between sorted values 95 and 100), not 87 (which is between 85 and 90 and where Gini = 0.417). The chapter contradicts itself: §5.6 line 484 then correctly says "the threshold around 97".
- Fix: change line 314 to "between 95 and 100 (split position 97 in slide 47)" and remove the fabricated `1/3 vs 2/4` count matrix — at split position 97 the slide actually shows Yes: 3|0, No: 3|4.
- Exam impact: a continuous-attribute Gini question is high-probability on this exam (slide 47 is the only worked numerical computation of a continuous split in the deck). The student following §4.5 will write the wrong answer. **Must fix before final draft.**

### P1 — Important, will hurt exam answer but not necessarily fail it

**P1-1. §5.3 claims the Hunt's-algorithm growth order on slide 34 is Gini/entropy-optimal.** (Q5.)
- File: line 436. *"the order chosen is Refund → MarSt → TaxInc, which is what a Gini- or entropy-driven choice would also pick on these 10 rows"*
- Slide 34 never proves the order is impurity-optimal; it just shows a growth sequence. Without doing the actual Gini computation on Refund vs MarSt at the root, this claim is unsupported.
- Fix: soften to "the slide's chosen growth order is Refund → MarSt → TaxInc; we are not told that this is the impurity-optimal order."

**P1-2. §6.3 invokes the "horizon effect" as if from the lecture.** (Q9.)
- File: line 566. *"The risk of pre-pruning is **horizon effect**…"*
- "Horizon effect" is a real concept but is not on any slide. Students who write it on an exam may not be credited.
- Fix: rephrase as the chapter author's observation, not the lecturer's term.

**P1-3. §4.9 derives boosting intuition the slides do not give.** (Q10.)
- File: line 363. *"Boosting … Conceptually: train trees sequentially, each one focusing on examples the previous ones got wrong."*
- The slides only name AdaBoost / CatBoost / XGBoost (slide 20). Any deeper claim is outside the lecture.
- Fix: explicitly tag as "background — not on slides".

**P1-4. §6.4 asserts information-gain bias toward high-cardinality attributes citing slide 38.** (Q10.)
- File: line 590. *"Bias toward attributes with more values … a classic ID3-style failure that information gain ratio in C4.5 partly fixes."*
- The bias is real, but slide 38 only shows the Student-ID partition picture without naming the bias. The C4.5/gain-ratio remedy is also not on the slides.
- Fix: tag as the chapter author's gloss; not lecture content.

### P2 — Polish

**P2-1. §3.1 collapses slide-7's two stochasticity bullets into one.** Slide 7 splits stochasticity into (a) state-stochasticity and (b) reward-stochasticity. Chapter merges them. Add a sub-bullet to mirror the slide.

**P2-2. §5.6 table has the threshold labelled as "≤ 55" through "≤ 230" but slide 47 labels the split *positions* as 55, 65, 72, ..., 230 (midpoints between adjacent sorted values).** The chapter's "≤" notation is *correct in meaning* but the slide uses "≤ / >" headings on the count matrix and never writes "≤ 55". A reader cross-referencing slide 47 will be momentarily confused. Suggest changing "≤ 55" → "split @ 55", etc.

**P2-3. §4.6 writes information gain as `IG = Entropy(parent) − Σ (n_i/n) Entropy(child_i)`** which is correct, but the slides themselves never write down the information-gain formula explicitly — slide 48 only defines entropy and asserts "Entropy based computations are similar to GINI". So the chapter is helpfully adding the formula but should flag that the slide does not. Minor.

**P2-4. §4.8 says `max_depth`, `min_samples_leaf`, `min_samples_split` are "pre-set numbers the tree-builder respects".** This is fine but slides 53 and 59 are the source — only slide 59 frames them under "How to Address Overfitting". The chapter places them in §4.8 (Stopping criteria) AND in §6.3 (Addressing overfitting). Mild duplication; not wrong.

**P2-5. §5.7 entropy column reports 0.650 for node B, but the corrected value of $-(1/6)\log_2(1/6) - (5/6)\log_2(5/6) \approx 0.650$** — chapter rounds to 0.65 and reports it correctly. The pedantic version is $\approx 0.6500$. No fix needed; flagging for completeness.

**P2-6. Q3-relevant: translation example architecture.** Chapter says "(slide gives no specific architecture)" which is accurate. PASS, no fix.

**P2-7. §4.5 has Figure 12 captioned "Gini values for four 6-record nodes. The 50/50 node has the maximum Gini."** This is consistent with slide 42 except the figure shows nodes (0,6), (1,5), (2,4), (3,3) — only the (3,3) one is 50/50 and yields Gini = 0.500. The chapter is correct; no fix.

### N/A items
- Performance / security / accessibility / DOCUMENT.md — N/A for a study chapter.

---

## Coverage gaps (topics in the deck that the chapter could quiz harder on)

- The chapter mentions slide 17 (the schematic stars-and-discs classification picture) only obliquely. An exam question asking the student to identify what is being shown on slide 17 would be a valid factual recall and the chapter does not prepare them for it. **Suggest:** add a one-line note in §3.3 pointing to slide 17 as the visual intuition before slide 18's definition.
- The chapter never quizzes the **count-matrix mechanics** of the efficient continuous-attribute scan. The student should be able to compute the Yes/No tallies at one specific split position from scratch. None of the 10 questions above forces this either — but slide 47 invites such a question and it is high-probability for an exam. **Recommended additional question:** *"For split position 97 on the Taxable Income column, write down the count matrix (Yes/No on each side) and verify the Gini = 0.300."*
- No question covers the relationship between **Naive Bayes / Bayesian Belief Networks** (slide 20) and decision trees. The lecture lists them as alternative techniques; an exam could ask the student to name three classification-technique families beyond decision trees. The chapter's §3.4 lists all eight techniques; consider a recall question.

---

## Acceptance Criteria (Spec §7.1)

| Criterion | Status |
|---|---|
| 10 exam questions, each tied to a slide range | Met |
| Questions cover the lecture broadly (def, branches, classification, Hunt's, impurity, best-split, continuous, overfit, ensembles) | Met |
| Each question has a model answer | Met |
| Chapter audited against PDF source for each Q | Met |
| Severity-tagged findings | Met |

---

## Out-of-scope observations
- The chapter cross-references L11 (Regression), L12 (Clustering), L02 (Agents), L09a (Bayesian Networks). I did not verify those cross-references against their source PDFs — that is reviewers #1–#3's territory. The internal claims about what L09a / L02 contain look plausible but I cannot vouch for them.
- The chapter says ML Lab 1 uses `RandomForestClassifier(n_estimators=...)` and `DecisionTreeClassifier(max_depth=...)`. I have not opened the lab notebook to verify; not in scope.

---

## Concerns / Risks

1. **P0-1 (wrong threshold in §4.5)** is the single highest-risk error in this chapter. It will mislead a student on a likely exam question.
2. The chapter occasionally generalises beyond the slides (horizon effect, boosting intuition, information-gain bias). These are not wrong but they are **outside the lecturer's tested content**. A student who treats them as quotable from the lecture may lose marks. Recommend tagging such passages as "background, not in deck".
3. The chapter's internal cross-check is weak: §4.5 and §5.6 give different thresholds for the same numerical answer. A round-2 pass should explicitly diff numerical answers across sections.

---

## What PM should do next

1. Dispatch `pm-frontend` or whichever employee owns chapter authorship to fix **P0-1** immediately (line 314 of `L10-Intro-to-ML.md`).
2. Address the four P1 findings in the same revision pass — they are all single-paragraph rewrites.
3. P2 items can be batched into a polish pass after round-1 reviewers all report in.
4. After fixes, re-run a quick numerical sanity check: every "0.300", "0.343", "0.420" in the chapter should be cross-referenced against slide 47's column headers.
5. Once fixes are made, re-QA this lecture before App Tester / Code Reviewer steps.

**DOCUMENT.md updated:** N/A for QA.

---

## Report to PM

**Assignment recap:** Lecture Reviewer #4 (Exam Readiness, Spec §7.1) — L10 Round 1. Produced 10 exam questions with model answers, audited each against the chapter and the source PDF.

**Status:** **Fail** — one P0 factual error in §4.5 will mislead students on a high-probability exam question. Otherwise the chapter is strong.

**P0 findings:**
1. **`L10-Intro-to-ML.md` line 314 (§4.5)** — claims slide-47 best Gini = 0.300 is at threshold "between 85 and 90 (1/3 vs 2/4 count)". Correct threshold is between 95 and 100 (split position 97); count matrix is Yes 3|0, No 3|4. Chapter contradicts itself in §5.6 line 484. **Fix:** rewrite line 314 to match §5.6.

**P1 findings:**
1. `L10-Intro-to-ML.md` line 436 (§5.3) — unsupported claim that slide-34 growth order is impurity-optimal. Soften.
2. `L10-Intro-to-ML.md` line 566 (§6.3) — "horizon effect" not on any slide; tag as chapter gloss.
3. `L10-Intro-to-ML.md` line 363 (§4.9) — boosting intuition beyond the slide; tag as background.
4. `L10-Intro-to-ML.md` line 590 (§6.4) — high-cardinality bias / C4.5 gain ratio not on slides; tag.

**P2 findings:**
1. §3.1 collapses slide-7's two stochasticity bullets into one — split them.
2. §5.6 uses "≤ 55" notation; slide 47 uses split-position headers. Notation drift.
3. §4.6 writes the information-gain formula; slide 48 does not. Helpful but flag.
4. §4.8 and §6.3 duplicate the `max_depth` / `min_samples_*` hyperparameter list. Mild redundancy.
5. §5.7 entropy 0.65 is correctly noted as a slide rounding; no fix.
6. (Coverage gap) Chapter doesn't drill the count-matrix mechanics of slide 47 explicitly — recommend an extra exam question.
7. (Coverage gap) Slide 17 visualisation is never quizzed.

**QA Checklist (§7) status:** N/A — this lecture chapter is a study artifact, not a software change. Reviewer #4's own §7.1 checklist (10 exam questions, slide-keyed, audited): all Pass.

**Acceptance criteria (§1) status:** 10 exam questions delivered with model answers and chapter audit — **Met**, contingent on P0 fix.

**DOCUMENT.md audit:** N/A — chapter review, not a code-directory deliverable.

**Out-of-scope observations:** Did not verify L02 / L09a / L11 / L12 cross-references (reviewers #1–#3's territory). Did not open ML Lab 1 notebook to verify the API calls cited in §7.

**Concerns / risks:**
- §4.5 numerical error is the worst kind: a numeric answer the student would copy verbatim onto an exam.
- Multiple passages slide silently from "lecture content" to "chapter author's background knowledge" without flagging the boundary. Students under exam pressure will not draw the distinction; the chapter should.
- §4.5 vs §5.6 contradiction shows the chapter was not internally diffed before being marked round-1-ready.

**What PM should do next:**
1. Dispatch chapter author to fix **P0-1** on line 314 immediately.
2. In the same pass, address P1-1 through P1-4 (line 436, 566, 363, 590).
3. Batch P2s for the polish pass.
4. Re-QA on the corrected chapter before sending to App Tester / Code Reviewer steps.

**DOCUMENT.md updated:** N/A for QA.
