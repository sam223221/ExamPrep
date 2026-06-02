# L09a Round 1 — Reviewer #1 (Concept Completeness incl. Figures)

**Reviewer scope:** Spec §7.1 — cross-check every slide vs chapter; audit figures.md (every USE/REWORK embedded, every SKIP justified).

**Artifacts inspected:**
- Source PDF: `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture9-Bayesian Networks.pdf` (67 slides)
- Chapter: `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L09a-Bayesian-Networks.md` (933 lines)
- Figure catalogue: `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\extracted_figures\L09a\figures.md`
- Figure files: 44 files in `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\extracted_figures\L09a\`

---

## VERDICT

**FAIL.** Four figures classified as **USE** in `figures.md` are missing from the chapter, including the slide-33 Anthrax BN diagram (the first intuitive Bayes-net picture in the lecture), the slide-34 "$2^k$ joint table" motivation, the slide-08 atomic-events panel, and slide-55's joint-entry computation setup. The catalogue advertises 27 USE figures embedded; only 23 are. This is a hard P0 against §7.1 because the catalogue's own promise — "every informative figure embedded" — is broken, and at least one of the missing figures (Anthrax BN, page-33) is genuinely pedagogically valuable. Otherwise the chapter is exceptionally thorough and the prose covers every slide's concept.

---

## P0 — Blocking

### P0-1. Four USE-marked figures are not embedded in the chapter

The catalogue (`figures.md`, lines 53, 60, 61, 76) marks the following as **USE** (i.e., must be embedded). The chapter does not `![…](…)` any of them:

| Catalogue ID | File | Slide | Catalogue rationale | Embedded in chapter? |
|---|---|---|---|---|
| P1 | `page08-atomic-events.png` | 8 | "Foundation example for §3.1." | **No** |
| P8 | `page33-anthrax-bn.png` | 33 | "First *intuitive* Bayes-net diagram of the lecture. Motivates the BN section." | **No** |
| P9 | `page34-joint-table-2k.png` | 34 | "The '$2^k$ entries' pain-point table (A, B, C). Motivates the BN factorisation." | **No** |
| P24 | `page55-compute-joint-entry-example.png` | 55 | "Computing the joint entry $P(S, \neg M, L, \neg R, T)$. §5 worked example." | **No** |

Evidence (grep over chapter for `extracted_figures/L09a/` returns 23 hits; none match `page08`, `page33`, `page34`, or `page55`):

```
$ rg "page(08|33|34|55)" lectures/L09a-Bayesian-Networks.md
No matches found
```

Why each is harmful:
- **Slide 33 (Anthrax BN)** is the **first BN diagram in the lecture** — the entire setup ("now suppose you order an x-ray and observe wide mediastinum, your belief jumps") motivates why we need BNs. The chapter walks through this story in prose nowhere — slide 33 content is essentially skipped. The Anthrax DAG is genuinely informative (one cause node with four effect nodes) and is the only intuitive picture before the abstract A→B→{C,D} reference network.
- **Slide 34 ($2^k$ table)** sets up the central motivation for §3.7 ("How do we use fewer numbers?"). The chapter text mentions this in passing ("write out the table for $n = 30$ and you already need a billion cells" in §3.2) but never embeds the slide's three-variable counterexample table.
- **Slide 55 setup** — chapter §5.7 jumps straight into the derivation on slide 56 without showing the slide-55 question framing ("What is $P(S, \neg M, L, \neg R, T)$?").
- **Slide 8 atomic events** — chapter §3.2 uses a markdown blockquote of the four events but doesn't embed the slide image.

**Fix:** Either embed all four images (preferred, since the catalogue made the commitment), or change their verdicts in `figures.md` from USE to SKIP with justification. If keeping as USE, add inline content for slide 33 ("Anthrax motivating example") which is currently a slide-content gap, not just a figure gap.

### P0-2. Slide 33 — Anthrax motivating example is conceptually missing from chapter prose

Independent of the figure embed, the **Anthrax / wide-mediastinum belief-update narrative** (slides 31–33) is the lecture's intuitive motivation for Bayes nets and inference. The chapter's §3.7 jumps straight to the formal "DAG + CPTs" definition citing slide 35 alone. The progression of slides 31 → 32 → 33 ("you observe symptoms" → "you're uncertain" → "now you observe wide mediastinum, your belief jumps; here is the BN that organises this reasoning") is not reproduced anywhere in the chapter. §1 mentions "diagnostic systems" but not this specific worked story. §3.7 cites "[Slide 35]" but the conceptual lead-in from slides 31–33 is dropped.

**Fix:** Add a short paragraph between §3.5 (Independence) and §3.7 (BN definition) — or fold into §3.7 — narrating the Anthrax example and embedding `page33-anthrax-bn.png`. This is exactly the "concept completeness against the source" issue §7.1 asks for.

---

## P1 — Important

### P1-1. Slide 48 content (joint-factorisation formula + sample joint computation) is incompletely surfaced

Slide 48 is marked **SKIP** in `figures.md` (P20) with the justification "Same alarm-network DAG as P18 but without the CPTs — fully redundant." This is **wrong**. Slide 48 actually contains two pieces of unique content the earlier alarm-network slides do NOT have:

1. The general factorisation formula written out in the alarm-network's variables:
   $\prod_i P(X_i | \text{Parents}(X_i)) = P(B) \cdot P(E) \cdot P(A|B,E) \cdot P(J|A) \cdot P(M|A)$.
2. A sample joint computation $P(+b, -e, +a, -j, +m) = P(+b)P(-e)P(+a|+b,-e)P(-j|+a)P(+m|+a)$.

The chapter does cover (1) in §3.10 and (2) in §5.6 with a different assignment ($+j, +m, +a, \neg b, \neg e$). So the *content* is present, but the SKIP rationale is misleading. Either:
- Update `figures.md` P20 justification to read "Content covered in chapter §3.10 (factorisation) and §5.6 (sample joint)" instead of "fully redundant with P18", or
- Embed `page48-alarm-network-clean.png` near §5.6 to show how the slide writes out the factorisation explicitly.

### P1-2. Slide 41 alternate variable letters not flagged

Slide 41's drawing labels the nodes **R**ain, **U**mbrella, **T**raffic. The chapter uses lowercase letter shorthand $U \perp T \mid R$ correctly, but earlier in §2 the analogy is written as "$\text{Umbrella} \perp \text{Cloud} \mid \text{Rain}$" — the "cloud" version is **not** on the slides at all (slide 41 uses traffic, not cloud). This is a chapter authoring choice that may confuse a student comparing chapter text to slides. The chapter then introduces traffic correctly in the second paragraph of §2 and again in §3.6. Recommend either dropping the cloud-version analogy or labelling it explicitly as "(textbook-style example, not on slide)."

### P1-3. Slide 7 D notation discrepancy

Slide 7 writes the dice-sum event as "$D \in \{(5,6), (6,5)\}$" (set membership, italicized). Chapter §3.1 has "$D \in \{(5,6), (6,5)\}$" ✓ — but earlier in §3.1 the variable definition says "$D \in \{(1,1), (1,2), \dots, (6,6)\}$ — **pair-valued**." That phrasing is fine, but the slide also reuses $D$ on slide 7 with **proposition** "Sum of the two dice rolls is 11" ⇔ "$D \in \{(5,6), (6,5)\}$" — the chapter could be clearer that $D$ here is the *outcome of two dice*, not the *sum*. Low-impact polish, but worth a note since it's a glossary term.

### P1-4. Slide 53/54 CPT count not stated as parameter savings comparison

The lecture-late example has 5 Boolean variables; chapter quotes 10 parameters for the alarm network but does not perform the analogous count for the lecture-late network (1 + 1 + 2 + 4 + 2 = 10 vs $2^5 - 1 = 31$). This would reinforce the "compactness" point of §3.10 and §3.8. Minor concept-completeness gap.

### P1-5. Slide 50 ordering vs slide 51 drawing — chapter explanation is buried

Slide 50 lists variables in order $T, L, R, M, S$ but the slide-51 drawing introduces them in causal-topological order ($S, M$ as roots; $L, R$ as middle; $T$ as leaf). The chapter mentions this asymmetry only in §6.7's "Common Pitfalls" section as "the natural causal ordering used in the figure is $S, M, R, L, T$" — but a student reading §4.1 might be confused by §4.1 listing variables in textbook order while the diagram uses a different one. Cross-link recommendation: in §4.1 immediately after the bullet list, add a one-liner: "Note the variable list is in textbook order; the diagram in Step 1 reorders to causal-topological order — see §6.7 on variable ordering."

### P1-6. DOCUMENT.md missing in `study/lectures/` and `study/extracted_figures/L09a/`

Per the spec: "Every directory with new/modified files must have an updated `DOCUMENT.md`. Missing = P1." Neither directory contains a `DOCUMENT.md` (verified by directory listing). Both directories have new/modified files for this lecture chapter.

---

## P2 — Polish / Minor

### P2-1. Chapter §3.13 quotation of slide 64 slightly paraphrased

Chapter §3.13 quotes slide 64 as:
> Exact inference is feasible in small to medium-sized networks. Exact inference in large networks takes a very long time. We resort to approximate inference techniques which are much faster and give pretty good results. General querying of Bayes nets is NP-complete.

The slide actually says:
> Exact inference is feasible in small to medium-sized networks. Exact inference in large networks takes a very long time. We resort to approximate inference techniques which are much faster and give pretty good results. **If ever asked to manually do a Bayes Net inference -> many tricks to save you time -> not topic of this class though :(**
>
> **Sadder and worse news:** General querying of Bayes nets is NP-complete.

The chapter elides the parenthetical aside, which is fine, but the elision is silent. Minor: add an ellipsis or note "[paraphrased]" for fidelity.

### P2-2. §3.4 Marie's wedding — chapter notes 0.111 but slide rounds to 0.111 explicitly

Chapter writes "$\approx 0.111$" ✓ matches slide. No issue. (Logging here only because §5.2 reduces the answer to "about $11\%$" which is fine but slightly looser than the slide's three-decimal value.)

### P2-3. Caption numbering Figure 9.1 through 9.23 — verify monotone

Spot-checked: figures embedded in chapter are numbered 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 9.10, 9.11, 9.12, 9.13, 9.14, 9.15, 9.16, 9.17, 9.18, 9.19, 9.20, 9.21, 9.22, 9.23 — monotone and consecutive. Good. (If P0-1 is fixed, new figures will need renumbering and downstream references checked.)

### P2-4. §3.1 worked coin example uses notation $X(t)$ but the slide uses $X(t)$ everywhere with capitalized $X$

Chapter is consistent. No issue. Logging because the slide capitalisation is sometimes used as a "you got the slide?" sanity check.

### P2-5. §2 cloud analogy could be replaced by slide-41 traffic analogy for unity

See P1-2. Lower urgency than the P1, but consolidating to the slide's traffic version would make the §2 and §3.6 examples literally identical.

### P2-6. The catalogue claims "REWORK: 0" but lists fig09 as REWORK

`figures.md` summary section line 87 says "Page renders: 28 — of which **26 USE**, 0 REWORK, 2 SKIP". The raster image fig09 (line 37) is marked REWORK in the table. Summary is inconsistent with the per-row verdicts. Suggest restating as "1 REWORK (absorbed by page render P7), 15 SKIP" to keep the per-row verdicts consistent with the totals.

---

## EVIDENCE

### Slide-by-slide concept coverage matrix

| Slide | Topic | Chapter location | Status |
|---|---|---|---|
| 1 | Cover | n/a | n/a |
| 2 | Uncertainty motivation | §1 | Pass |
| 3 | Expected utility / decision theory | §1 | Pass |
| 4 | Frequentism vs Subjectivism | §3.1 | Pass |
| 5 | Random variables (CSP analogy) | §3.1 | Pass |
| 6 | RV formal definition + coin example | §3.1 | Pass |
| 7 | Events / propositions | §3.1 | Pass |
| 8 | Atomic events | §3.2 | **Concept text yes; figure embed missing (P0-1)** |
| 9 | Joint distribution example | §3.2 (Fig 9.1) | Pass |
| 10 | Joint dist size + notation | §3.2 | Pass |
| 11 | Marginal — setup | §3.2 (Fig 9.2) | Pass |
| 12 | Marginal — solved | §3.2 | Pass |
| 13 | Marginal — general formula | §3.2 | Pass |
| 14 | Conditional probability + Venn | §3.3 | Pass |
| 15 | Conditional probability — questions | §3.3 | Pass |
| 16 | Conditional probability — solved | §3.3 | Pass |
| 17 | All four conditional distributions | §3.3 (Fig 9.3) | Pass |
| 18 | Normalisation trick | §3.3 (Fig 9.4) | Pass |
| 19 | Product rule + chain rule | §3.3 | Pass |
| 20 | Bayes' rule (definition + why useful) | §3.3 | Pass |
| 21 | Meningitis example | §3.4 / §5.1 | Pass |
| 22 | Marie wedding setup | §3.4 / §5.2 | Pass |
| 23 | Marie wedding — given quantities | §3.4 | Pass |
| 24 | Marie wedding — calculation | §3.4 (Fig 9.5) | Pass |
| 25 | Independence + mutually-exclusive trap | §3.5 / §6.1 | Pass |
| 26 | Probabilistic inference motivation | §3.12 | Pass |
| 27 | Bayesian inference as classifier | §3.11 | Pass |
| 28 | Naive Bayes formula | §3.11 | Pass |
| 29 | Naive Bayes worked example | §3.11 / §5.4 (Fig 9.13) | Pass |
| 30 | What if not independent? | §3.11 | Pass |
| 31 | Anthrax setup | — | **Missing (P0-2)** |
| 32 | Reasoning with uncertainty | — | **Missing (P0-2)** |
| 33 | Anthrax BN | — | **Missing — figure AND prose (P0-1, P0-2)** |
| 34 | $2^k$ joint table problem | — (mentioned in §3.2 only by number) | **Figure missing (P0-1)** |
| 35 | BN definition (DAG + CPTs) | §3.7 (Fig 9.7) | Pass |
| 36 | BN structure annotations | §3.7 (Fig 9.8) | Pass |
| 37 | CPT set | §3.8 (Fig 9.10) | Pass |
| 38 | CPT detail / 2^(k+1) rule | §3.8 (Fig 9.9) | Pass |
| 39 | Markov condition diagram | §3.9 (Fig 9.11) | Pass |
| 40 | Height/vocabulary/age example | §3.6 | Pass |
| 41 | Rain/Umbrella/Traffic example | §3.6 (Fig 9.6) | Pass |
| 42 | Joint from chain rule + Markov | §3.10 (Fig 9.12) | Pass |
| 43 | Inference queries P(X\|E) | §3.12 | Pass |
| 44 | A→B→{C,D} joint setup | §4.2 / §5.5 | Pass |
| 45 | A→B→{C,D} joint with numbers | §4.2 / §5.5 (Fig 9.19) | Pass |
| 46 | Alarm network DAG | §5.6 (Fig 9.21) | Pass |
| 47 | Alarm network CPTs | §5.6 (Fig 9.22) | Pass |
| 48 | Alarm joint formula + sample | §3.10 / §5.6 (no figure) | **Coverage OK but figures.md SKIP rationale wrong (P1-1)** |
| 49 | Building a BN (recipe) | §4.1 | Pass |
| 50 | Lecture-late variables + assumptions | §4.1 | Pass |
| 51 | Step 1: add variables | §4.1 (Fig 9.16) | Pass |
| 52 | Step 2: add edges | §4.1 (Fig 9.17) | Pass |
| 53 | Step 3: CPTs | §4.1 (Fig 9.18) | Pass |
| 54 | BN observations | §4.1 | Pass |
| 55 | Compute joint entry setup | §5.7 (no figure) | **Figure missing (P0-1)** |
| 56 | Compute joint derivation | §4.3 / §5.7 (Fig 9.20) | Pass |
| 57 | Where we are summary | §3.10 / §3.13 (paraphrased) | Pass |
| 58 | P(R\|T,~S) — Step 1/2/3 | §3.13 / §5.8 (Fig 9.14) | Pass |
| 59 | Step 1/2/3 with annotations | §5.8 | Pass |
| 60 | 4 joint computes | §3.13 / §5.8 (Fig 9.15) | Pass |
| 61 | The good news — inference formula | §3.13 / §4.4 | Pass |
| 62 | Cost of inference | §4.4 | Pass |
| 63 | Real-world BN diagram | §8 cheat-sheet end (Fig 9.23) | Pass |
| 64 | NP-completeness | §3.13 / §4.4 | Pass (with P2-1) |
| 65 | Expert vs learning | — | Not covered — see "Out-of-scope observations" |
| 66 | Summary | §8 | Pass |
| 67 | Thank you | n/a | n/a |

### Figure audit summary

- Catalogue total: 16 raster + 28 page renders = 44 files.
- USE-marked in catalogue: 1 raster (fig15) + 26 page renders = **27 total claimed**.
- Actually embedded in chapter: **23 figures** (counted by `rg "extracted_figures/L09a/"`).
- **Missing embeds (USE in catalogue, not in chapter):** P1 (page08), P8 (page33), P9 (page34), P24 (page55). All 4 files exist on disk — they were extracted but not embedded.
- SKIP justifications: spot-checked all 15 SKIP raster decisions — all reasonable (decorative stock photos, ornaments, the small Bayes portrait, redundant raster of slide-29 table).
- SKIP page-render rationale for P20 (page48) is **incorrect** — see P1-1.
- REWORK: 1 file (fig09 — page-29 training table); catalogue says it was absorbed into the higher-fidelity page-render P7, which IS embedded. OK in practice but summary line is inconsistent (P2-6).

### Out-of-scope observations

- **Slide 65** ("Where do we get the Bayesian network from? — expert design or learning") is not covered in the chapter. Mild omission — it is one slide and lightweight, but it sets up topic continuity into structure learning / parameter estimation (mentioned in passing in L11/L12 by the topic but not pointed back to here). Worth one sentence in §3.10 or §7 forward-references.
- The chapter does compute its own numerical answer to $P(R | T, \neg S) \approx 0.415$ in §5.8 — this exceeds the slide content (slides 58–60 only sketch the structure). I verified the arithmetic by hand: numerator 0.21210, denominator 0.51100, ratio 0.41507. Correct.
- The chapter's §5.6 sample joint computation $P(+j, +m, +a, \neg b, \neg e) = 0.000628$ differs from slide 48's worked example $P(+b, -e, +a, -j, +m)$ — chapter computes a different joint entry. Both are valid; just flagging.

### Concerns / risks

- The four missing USE figures aren't just inventory drift — slide 33 (Anthrax BN) is a real conceptual gap (P0-2). Re-QA should verify both the figure embed and the surrounding narrative.
- `figures.md` has at least two metadata bugs (P1-1 and P2-6). The catalogue is meant to be a contract between extractor and author; if it ships with wrong SKIP rationales, future authors / reviewers will trust it incorrectly.

---

## Report to PM

**Assignment recap:** Reviewer #1 (Concept Completeness incl. Figures) for L09a (Bayesian Networks) Round 1. Spec §7.1 — every slide cross-checked vs chapter; `figures.md` USE/REWORK embedded, SKIP justified.

**Status:** Fail

**P0 findings:**
1. `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L09a-Bayesian-Networks.md` — Four figures marked USE in `figures.md` (P1=`page08-atomic-events.png`, P8=`page33-anthrax-bn.png`, P9=`page34-joint-table-2k.png`, P24=`page55-compute-joint-entry-example.png`) are not embedded. Fix: embed them in the relevant chapter sections (§3.2 atomic events, new sub-section before §3.7 for Anthrax, §3.2 or §3.7 motivation for 2^k table, §5.7 setup). Files already exist in `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\extracted_figures\L09a\`.
2. `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L09a-Bayesian-Networks.md` §3.5–§3.7 — Slides 31–33 Anthrax / wide-mediastinum motivating narrative is entirely missing from chapter prose, not just the figure. Fix: add a 2-paragraph motivation block before §3.7 introducing the slide-33 anthrax network as the lead-in to the formal BN definition.

**P1 findings:**
1. `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\extracted_figures\L09a\figures.md` line 72 — P20 SKIP justification "fully redundant with P18" is wrong; slide 48 contains the explicit factorisation formula and a sample joint computation. Fix: update justification, or embed `page48-alarm-network-clean.png` near §5.6.
2. `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L09a-Bayesian-Networks.md` §2 — "Cloud" analogy for conditional independence does not match the slide-41 "Traffic" analogy. Recommend consolidating to traffic version.
3. `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L09a-Bayesian-Networks.md` §3.1 — Variable $D$ is "outcome of rolling two dice" but slide 7 also uses $D$ inside a sum-related event; chapter could disambiguate.
4. `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L09a-Bayesian-Networks.md` §4.1 — Lecture-late parameter-count comparison (10 vs 31) not stated explicitly the way the alarm-network one is.
5. `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L09a-Bayesian-Networks.md` §4.1 — Slide-50 textbook-order vs slide-51 causal-order asymmetry only addressed in §6.7; add cross-reference in §4.1.
6. DOCUMENT.md missing in `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\` and `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\extracted_figures\L09a\`.

**P2 findings:**
1. §3.13 silent paraphrase of slide 64 quote (drops the "tricks to save you time" parenthetical).
2. §5.2 looser rounding ("about 11%") than slide.
3. Figure caption monotonicity verified 9.1–9.23. (Will need re-checking if P0-1 fixed.)
4. RV $X(t)$ notation consistent with slide.
5. (See P1-2.)
6. `figures.md` summary line "0 REWORK" inconsistent with per-row REWORK on fig09.

**QA Checklist (§7) status:** This is a lecture-chapter review, not a code review. Mapped to spec §7.1 (Concept Completeness):
- Every slide cross-referenced: **Fail** — slides 31, 32, 33 narrative gap; slide 65 not covered.
- figures.md USE/REWORK embedded: **Fail** — 4 USE figures missing.
- figures.md SKIP justified: **Pass with concerns** — P20 (slide 48) justification incorrect (P1-1); summary line miscount (P2-6).
- Concept correctness against source: **Pass** — verified arithmetic in §5.6 ($0.000628$), §5.8 ($0.415$), §3.4 ($0.0002$, $0.111$); all match slide numbers or are correct extensions.

**Acceptance criteria (§1) status:** N/A — lecture chapter has no §1 Scope. Mapped to concept-coverage: 64/67 slides covered (slide 31, 32, 33 narrative gap; slide 65 not covered). Atomic events, anthrax motivation, $2^k$ table figure, slide 55 setup figure all need to be added.

**DOCUMENT.md audit:**
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\` — **missing**
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\extracted_figures\L09a\` — **missing** (only `figures.md` present, which is a different artifact)
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_review\L09a\round1\` — N/A (review directory; this report)

**Out-of-scope observations:**
- Slide 65 ("expert design vs learning") not covered — worth a sentence in §7 forward-references.
- Chapter §5.8 computes numerical $P(R|T,\neg S)$ that the slides only sketch — verified correct; this is bonus value, not a defect.
- The chapter's §2 "gossip graph" analogy is excellent and the §6 Common Pitfalls list is thorough — well above the typical lecture-chapter bar.

**Concerns / risks:**
- Four missing figure embeds against an explicit catalogue commitment suggests the embed step was incomplete. If other lectures share this catalogue, they may have the same drift — worth a spot check.
- `figures.md` for L09a has two metadata bugs (incorrect SKIP rationale for P20; inconsistent summary count). Pattern check the other lectures' figures.md files for similar issues.

**What PM should do next:**
1. Dispatch a writer (or `pm-investigator` for narrow fix) to:
   - Embed the four missing figures in the chapter at the locations called out in P0-1.
   - Author the Anthrax motivating narrative (slides 31–33) before §3.7 — P0-2.
   - Fix `figures.md` P20 SKIP rationale and the summary line — P1-1, P2-6.
   - Address P1-2 through P1-6 as time allows; P1-6 (DOCUMENT.md) requires a separate setup task.
2. Re-dispatch this Reviewer #1 (or run Round 2) to verify all P0 and P1 items closed.
3. After Reviewer #1 re-approves, proceed to the remaining L09a Round 1 reviewers and downstream pipeline.

**DOCUMENT.md updated:** N/A for QA.
