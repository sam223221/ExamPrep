# L07 Round 2 — Reviewer #2 (Mathematical Rigor)

**Reviewer role:** Mathematical Rigor
**Chapter:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L07-CSP.md`
**Source PDF:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture7-Constraint Satisfaction Problem.pdf` (55 slides)
**Round 1 status:** Pass with concerns — 5 P1s, 8 P2s.

---

## VERDICT

**PASS WITH CONCERNS** — all five Round-1 P1s were addressed substantively and the math is now tighter than Round 1. The chapter has gained 150+ lines of legitimate content (worklist trace, K4 note, source-tagged complexity, qualifier-aware constraint statements). However, two new mathematical / pedagogical issues introduced by the revision **and** one Round-1 issue that the revision claims to have fixed but in fact only half-fixed are now visible. None are P0. The cumulative pattern — chapter is mostly excellent, with occasional figure-caption slippage and one residual scope claim — argues for one more focused pass rather than a wholesale rewrite.

---

## STATUS OF ROUND-1 P1 FINDINGS

| Round-1 P1 | Location | Round-2 verdict |
|---|---|---|
| **P1-1** Wrong scope for units-column cryptarithmetic | L07-CSP.md §3.4.3 line 282 | **Fixed.** Chapter now reads "the units-column constraint $O + O = R + 10 \cdot X_1$ has scope **3** (the variables $\{O, R, X_1\}$; the constants $1$, $2$ and $10$ are coefficients, not variables). The tens and hundreds columns have scope **4** (`{W, X1, U, X2}` and `{T, X2, O, X3}` respectively)." Math is now correct. (Note: "constants $1$, $2$" is a small new phrasing wart — see P2-R2-1 below.) |
| **P1-2** N-queens slide-12 missing $j \neq k$ / $k \neq 0$ qualifiers | §3.4.2 lines 237–244 | **Fixed.** Each constraint now carries an explicit qualifier (`j ≠ k`, `i ≠ k`, `k ≠ 0` such that $(i+k, j+k)$ on the board, `k ≠ 0` such that $(i+k, j-k)$ on the board). A dedicated "Note (beyond the slide)" paragraph (lines 244–245) explains the qualifiers and flags the slide bug honestly. This is the model fix. |
| **P1-3** AC-3 complexity unsourced | §4.8 line 593, §8 line 836 | **Fixed.** Both locations now read "Cost (beyond the slide): the textbook AC-3 worst case is $O(c \cdot d^3)$… **The slides do not state this bound**; cite it only as the textbook (Russell & Norvig) figure, not as a slide claim." The §8 line additionally adds the AC-3-is-preprocessing-not-solver clarification. Disclaimer is now consistent with the §4.8 "the slide does not use the name 'AC-3'" disclaimer at line 564. |
| **P1-4** Compact formulation claimed to be what slides 35–44 use | §3.4.2 line 254, §4.7 lines 477–479 | **Fixed.** §3.4.2 now reads "best read as this compact formulation — the slide does not write its constraint set explicitly, but the variable count $X_1, \ldots, X_4$ with domains $\{1,2,3,4\}$ is incompatible with the 16-variable slide-12 encoding." §4.7 line 477 strengthens this with the K4 derivation (every pair of rows interacts via both `≠` and diagonal constraints, so all $\binom{4}{2} = 6$ pairs are connected). |
| **P1-5** Imprecise $n! \cdot m^n$ derivation | §3.5 line 322 | **Fixed.** Now reads "the branching factor at depth $k$ is $(n - k + 1) \cdot m$, so the leaf count is the **product** $\prod_{k=1}^{n} (n - k + 1) \cdot m = n! \cdot m^n$". Product notation, sample values ($k=1 \Rightarrow n m$, $k=n \Rightarrow m$), and the conclusion all check. |

All five Round-1 P1s: **closed**.

---

## STATUS OF ROUND-1 P2 FINDINGS

| Round-1 P2 | Status |
|---|---|
| P2-1 REVISE iterator invalidation | **Fixed** — line 581 now reads "for each value x in **a snapshot of $D_X$**: # iterate snapshot to avoid invalidation". |
| P2-2 Carry domain narrowing without justification | **Fixed** — §3.4.3 lines 265 + 274 now state slide-13 verbatim ("$\{0, 1, 2, \dots, 9\}$ for *all* variables"), and the $\{0,1\}$ tightening appears as a separate "Note (beyond the slide)" with the column-sum justification ($9+9+1=19$). |
| P2-3 SAT cited without source | **Fixed** — §6 pitfall 10 (line 770) now cites "Cook–Levin theorem, 1971; not on the slides". |
| P2-4 FC table row-ordering note | **Not directly addressed.** §5.2 table still shows the WA/Q/V abridged sequence without a one-line note that the slides display all variables as a 7-row vertical state. **Acceptable as P2 carry-over.** |
| P2-5 Glossary "AC-3" naming consistency | **Fixed** — front-matter (line 4) now reads "Arc-consistency algorithm (textbook name: AC-3)", which is consistent with §4.8 line 564's disclaimer. |
| P2-6 "Path cost is constant *and irrelevant*" gloss | **Not directly addressed.** §6 pitfall 9 (line 768) retains the "constant *and irrelevant*" gloss. Acceptable as the chapter justifies it with "every solution is at the same depth $n$ and we just want any one". P2 carry-over. |
| P2-7 LCV-determines-dead-end overstatement | **Fixed** — line 447 now reads "MRV picks *which* variable's dead-end branches we encounter first; LCV picks the value most likely to *avoid* a dead-end" — closes the prior "whether a branch leads to a dead-end" overclaim. |
| P2-8 REVISE missing empty-domain check | **Acceptable as-is** per Round 1; the outer `ARC-CONSISTENCY` caller still checks `if D_X is empty: return failure` (line 574). No change needed. |

Round-1 P2s: 5 fixed, 3 carry-over (all benign).

---

## P0 FINDINGS — Round 2

**None.** No outright false mathematics. The new content (worklist trace §5.6, K4 note §4.7, source-tagged complexity §4.8/§8) is mathematically sound.

---

## P1 FINDINGS — Round 2

### P1-R2-1. Figure caption for 4-queens "Stage 6 (slide 41)" mis-anchored — describes slide 42's post-FC state

**Location:** L07-CSP.md, line 505, the caption `Stage 6 (slide 41): after X_2 = 4, X_3 ∈ {2}, X_4 ∈ {3}.`

**Claim in chapter:** Slide 41 shows X3 = {2}, X4 = {3} after FC for X2 = 4.

**Problem:** Verified against `Lecture7-Constraint Satisfaction Problem.pdf` slides 40–43:

- **Slide 40:** X1 = {1..4}, X2 = `{ , , ,4}` (i.e. X2 chose 4), X3 = `{ ,2, ,4}` = `{2,4}`, X4 = `{ ,2,3, }` = `{2,3}`. (Backtrack from X2=3, now trying X2=4.)
- **Slide 41:** **identical to slide 40** in the table content — X3 = `{2,4}`, X4 = `{2,3}`. The slide depicts X2=4 chosen but FC for X2=4 not yet propagated to X3 / X4.
- **Slide 42:** X3 = `{ ,2, , }` = `{2}`, X4 = `{ , ,3, }` = `{3}`. *This* is the post-FC-for-X2=4 state — i.e. the state the chapter's caption ascribes to slide 41.
- **Slide 43:** Same as slide 42 (X3 = `{2}`, X4 = `{3}`). The next assignment X3=2 has not yet been made.

The chapter's slide numbering is off by one. The Round-1 revise-summary explicitly claimed this was fixed (item #2: "The figure captions were re-anchored to their correct slide numbers (40, 41, 42, 43)"), but the actual slide content does not support the new mapping. Slides 41–43 evidently encode the FC reduction in two animation steps (slide 41 = "X2=4 just placed, FC pending"; slide 42 = "FC applied"; slide 43 = "ready to assign X3"), so the correct caption for slide 41 is "Stage 5: try X_2 = 4 (queen drawn, FC for X2=4 not yet shown)", and the post-FC state X3={2}, X4={3} belongs on slides 42 (and continues on 43).

**Why this matters for math rigor:** The chapter's claim that FC reduces X3 and X4 *immediately* on slide 41 is the entire reason the §4.7 trace makes sense as a one-step-at-a-time animation. If a student looks up slide 41 in the deck and sees a different state than the chapter claims, the chapter's worked example loses its slide-traceability — which is exactly the kind of integrity the chapter has been careful to maintain everywhere else.

**Suggested fix:** Re-anchor the figures:
- "Stage 5 (slide 40 / 41): try X_2 = 4; FC for X2=4 not yet applied (X_3 still = {2,4}, X_4 still = {2,3})."
- "Stage 6 (slide 42): after FC for X_2 = 4 propagates, X_3 = {2}, X_4 = {3}."
- "Stage 7 (slide 43): about to try X_3 = 2 (still X_3 = {2}, X_4 = {3})."
- "Stage 8 (slide 44): after X_3 = 2, X_4 = {} — backtrack."

Also: slide 44 actually shows the *backtrack to X_1* re-exposing X2={3,4} with X3 empty (`{,,,}` for X3) and X4 = `{3}` — see pdftotext below — so the "Stage 9" claim that slide 44 is the *retry of X_1 = 2* is itself a slight mis-anchor (slide 44 is "X1=1 has now fully failed; the trace stops here"). The chapter's own narrative at line 525 ("The slide trace stops here. Continuing the algorithm with $X_1 = 2$ leads to a solution: …") is correct; the figure caption for fig33 (line 523) should be re-phrased to match.

### P1-R2-2. Slide 39 internal inconsistency unflagged — X4 = {3} on the slide is itself wrong by proper FC

**Location:** L07-CSP.md, line 494, the caption `Stage 4: after X_2 = 3, X_3's domain wipes out — both remaining values conflict. Backtrack.` and the discussion lines 496–499.

**Problem:** Slide 39's depicted state is `X3 = empty, X4 = {3}`. The chapter discusses only the X3 wipeout (correctly: X3=2 and X3=4 both diagonal-conflict with X2 at (2,3)). But the **X4 = {3}** state shown on slide 39 is itself **inconsistent with proper forward checking**:

- X4 started from {2,3} after X1=1 (per slide 37).
- After X2=3 (queen at (2,3)), proper FC for X4 against X2=3:
  - X4 = 2: queen at (4,2). vs X2 = (2,3): column diff $|2-3| = 1$, row diff $|4-2| = 2$. Not equal ⇒ **no diagonal conflict**. Not same column. **Keep**.
  - X4 = 3: queen at (4,3). **Same column as X2 = 3** ⇒ column conflict. **Remove**.
- Correct post-FC: D_{X4} = {2}.
- Slide shows: D_{X4} = {3}.

So the slide is internally inconsistent (it removes the non-conflicting value 2 and keeps the column-conflicting value 3). This is a **slide bug**, not a chapter bug per se — but the chapter is otherwise scrupulous about flagging slide bugs (it does so for slide 12, see the §3.4.2 "Note (beyond the slide)") and this one slips through.

**Why this matters for math rigor:** A student stepping through the 4-queens trace by hand will compute D_{X4} = {2} after X2=3 and then look at the slide, see X4 = {3}, and conclude their FC reasoning is wrong (or worse, transcribe the slide's incorrect state on the exam). The chapter's careful disclaimer culture means students will trust the slide on points the chapter does not flag.

**Suggested fix:** Add a footnote or parenthetical after line 499: "*Note: slide 39 depicts $D_{X_4} = \{3\}$, but proper FC after $X_2 = 3$ should give $D_{X_4} = \{2\}$ ($X_4 = 3$ has the same column as $X_2$; $X_4 = 2$ is non-conflicting). The slide's depiction may be an artifact of the animation: once the failure on $X_3$ was detected, FC may have been halted before fully updating $X_4$. Either way, the failure is correctly detected via $X_3$'s wipeout.*"

This is a P1 because it is a *mathematical* inaccuracy that the chapter implicitly endorses by not flagging.

### P1-R2-3. §5.6 worklist initialisation lists a non-edge inside the worklist string

**Location:** L07-CSP.md, line 714, the worklist seed string `NT→SA, SA→NT, NT→NSW (not adjacent, skip), SA→NSW, NSW→SA, SA→V, V→SA, NSW→V, V→NSW`.

**Problem:** The string lists `NT→NSW` and *then* annotates "(not adjacent, skip)". This is mathematically inconsistent with the line's own framing as "every directed arc between unassigned variables" — an arc only exists between variables that share a constraint, so by definition a non-adjacent pair does not produce an arc to seed. Either:

- Drop `NT→NSW` from the list (since it does not contribute an arc); the sentence is intended to enumerate arcs that *are* seeded.
- Or rewrite to make the framing match: "Candidate directed pairs between unassigned variables, only some of which are arcs because only adjacent pairs share a constraint: …" — but this is a confusing pedagogical choice.

Additionally, **`NT→V` is missing**: NT and V are not adjacent in the Australia graph, so this is correctly omitted by default; the chapter mentions only NT→NSW as the explicit "skip" — which raises the question why one non-edge is called out and the others aren't. (NT–V, NT–T, SA–T, NSW–T, V–T, T–anything are all non-edges and would also need "skip" annotations under the chapter's logic.)

**Why this matters for math rigor:** The §5.6 trace is a flagship pedagogical artefact (the entire reason it was added in Round 1 was Reviewer #4's P0-C "AC-3 cascade hand-waved"). A student transcribing the worklist initialisation will either be confused by the inconsistent treatment of non-edges or seed the worklist with a phantom arc.

**Suggested fix:** Replace line 714 with a clean enumeration. The actual arcs between unassigned variables in the post-FC state (unassigned = NT, SA, NSW, V, T) — using the Australia adjacency from §3.3 (edges: WA-NT, WA-SA, NT-SA, NT-Q, Q-SA, Q-NSW, SA-NSW, SA-V, NSW-V) — and excluding edges that touch assigned variables (WA, Q) or T (isolated):

- NT–SA → 2 directed arcs: NT→SA, SA→NT.
- SA–NSW → SA→NSW, NSW→SA.
- SA–V → SA→V, V→SA.
- NSW–V → NSW→V, V→NSW.

Eight directed arcs. T contributes none (isolated). The chapter's list includes a parenthetical skip for NT→NSW but not for the (also non-existent) NT→V, NT→T, SA→T, NSW→T, V→T; this is asymmetric.

The corrected line should read: `NT→SA, SA→NT, SA→NSW, NSW→SA, SA→V, V→SA, NSW→V, V→NSW` — eight arcs, no "skip" parenthetical, with a separate sentence noting "T is isolated and so contributes no arcs; NT shares no edge with NSW or V and so contributes no arcs to them."

---

## P2 FINDINGS — Round 2

### P2-R2-1. "Constants $1$, $2$ and $10$ are coefficients" wart

**Location:** §3.4.3 line 282.

The chapter's revision now reads: "the units-column constraint $O + O = R + 10 \cdot X_1$ has scope **3** (the variables $\{O, R, X_1\}$; the constants $1$, $2$ and $10$ are coefficients, not variables)." The "$1$, $2$" annotations are over-eager: there is no literal $1$ or $2$ in the equation $O + O = R + 10 \cdot X_1$. (Presumably the writer meant "the implicit coefficients of $O$ and $R$ are $1$, and the coefficient of $X_1$ is $10$"; but the equation does not contain a literal $2$ anywhere.) Drop "$1$, $2$ and" — leave only "the constant $10$ is a coefficient, not a variable".

### P2-R2-2. "Constants $1$, $2$ and $10$" carries through to "the constant 10 is a coefficient" framing

Same line. After the suggested fix in P2-R2-1, the sentence reads cleanly. Mild stylistic — not a math issue.

### P2-R2-3. §4.7 "Stage 9 (slide 44)" caption claims trace continues with $X_1 = 2$

**Location:** L07-CSP.md, line 523, the figure caption for fig33: `Stage 9 (slide 44): every branch under X_1 = 1 fails; backtrack to X_1 and try X_1 = 2.`

Slide 44 itself shows X2={3,4}, X3=`{,,,}` (empty), X4=`{ , ,3, }` = `{3}`. This is the *failure-of-X1=1* state — the trace has not yet tried X1=2; the slide is the terminal state of the X1=1 branch. The chapter's prose at line 525 correctly states "*Continuing* the algorithm with $X_1 = 2$ leads to a solution…", which is a forward-looking statement. The figure caption should match the prose: "Stage 9 (slide 44): under X_1 = 1 the algorithm has now exhausted X_2 ∈ {3, 4}; both fail. Algorithm backtracks to X_1 (trace stops on this slide; continuation discussed below)."

P2 because the prose immediately corrects the caption.

### P2-R2-4. §5.6 hypothetical-cascade table truncated

**Location:** L07-CSP.md, lines 727–731.

The hypothetical-cascade table shows steps 1 and 2 then "…(continue)" — the cascade is not played out. This is acceptable as an illustration but it's a missed pedagogical opportunity: the original purpose (Reviewer #4 P0-C) was to demonstrate the cascade *in motion*. A two-step trace with "..." does not exercise the propagation. **Acceptable as P2** because the failure-at-step-1 trace already in the chapter is the load-bearing example.

### P2-R2-5. §4.8 ARC-CONSISTENCY pseudocode missing return-type comment

**Location:** L07-CSP.md, lines 569–586.

`ARC-CONSISTENCY` returns "success" or "failure"; `REVISE` returns a Boolean ("True" / "removed"). The two are not compatible types, which is a minor pseudocode style issue but unambiguous to a careful reader. No fix needed; flag as P2 stylistic.

### P2-R2-6. §2.5 caveat duplicates §4.6 / §4.8 contrast

**Location:** L07-CSP.md, lines 84–86.

The §2.5 caveat covers BOTH "FC vs slide-12 formulation" AND "FC vs arc consistency". The two are distinct points; pedagogically, splitting them into two separate caveats (or a `>` block followed by `>` block) would be cleaner. P2 — current text is correct, just dense.

### P2-R2-7. §2.9 maiden-aunt caveat over-hedges

**Location:** L07-CSP.md, line 112.

The maiden-aunt caveat says "may have many feuds but also be irrelevant to the actual seating problem if those feuds are with guests who already have their tables decided — degree counts *edges to unassigned neighbours*, not their tightness". The "not their tightness" is a separate point (degree counts edges, not their constraint-tightness; this is true but is a different observation than the "edges-to-unassigned" point). Two unrelated caveats fused into one. P2.

### P2-R2-8. Footnote for "Lab 4 / GA n-queens" cross-reference

**Location:** L07-CSP.md, line 254, parenthetical `*(Note: Lab 4 uses this formulation for a genetic algorithm, not for CSP backtracking; Lab 6 — see §7 — is the CSP lab.)*`

This parenthetical is now mid-paragraph and breaks the flow of the "Alternative formulation" pedagogy. Move it to a footnote or to the §7 cross-references table. P2 stylistic.

---

## EVIDENCE — verified by direct computation / PDF cross-check

| Claim | Location | Verified |
|---|---|---|
| $8^8 = 16{,}777{,}216$ | §3.4.2 / slide 3 | ✓ |
| $n! \cdot m^n$ leaves count derivation (new wording) | §3.5 / slide 17–18 | ✓ — product form is right |
| Cryptarithmetic scope claim: units = 3, tens = 4, hundreds = 4 | §3.4.3 | ✓ |
| Slide-12 n-queens constraints with explicit $j \neq k$ / $k \neq 0$ qualifiers | §3.4.2 | ✓ |
| 4-queens FC after X1=1: X2 ∈ {3,4}, X3 ∈ {2,4}, X4 ∈ {2,3} | §4.7 / slide 37 | ✓ — verified by hand and matches slide |
| 4-queens FC after X1=1, X2=4: X3 = {2}, X4 = {3} | §4.7 lines 507–515 | ✓ — verified by hand; this is the post-FC state shown on slide 42, NOT slide 41 as the chapter caption claims (P1-R2-1) |
| 4-queens FC after X1=1, X2=3: X3 = ∅ | §4.7 line 494 | ✓ — slide depicts this; chapter is right |
| 4-queens FC after X1=1, X2=3: X4 SHOULD be {2}, but slide shows {3} | slide 39 | ✗ on slide — chapter does not flag (P1-R2-2) |
| 4-queens solution $(2, 4, 1, 3)$ | §4.7 line 525, §5.4 | ✓ |
| Other 4-queens solution $(3, 1, 4, 2)$ | §4.7 line 525 | ✓ |
| TWO+TWO=FOUR with $T=7, W=6, O=5, F=1, U=3, R=0$ | §5.3 | ✓ all column equations + Alldiff + leading-zero |
| Carry-domain narrowing $\{0,1\}$ justification: max column sum $9+9+1=19$ | §3.4.3 line 274 | ✓ |
| AC-3 complexity $O(c \cdot d^3)$ explicitly tagged "beyond the slide" | §4.8 line 593, §8 line 836 | ✓ disclaimers consistent |
| AC-3 is polynomial preprocessing, not a solver | §8 line 836 | ✓ |
| Constraint graph for 4-queens compact formulation = K_4 | §4.7 line 477 | ✓ — both `X_i ≠ X_j` (column) and $|X_i - X_j| \neq |i - j|$ (diagonal) apply to every pair, all $\binom{4}{2} = 6$ edges present |
| §4.9 x<y AC reduces to $D_x = \{1,2\}$, $D_y = \{2,3\}$ | §4.9 / slide 53 | ✓ — verified against slide 53 |
| SA has degree 5 in Australia graph (WA, NT, Q, NSW, V) | §3.3 line 187, §4.4 line 427 | ✓ |
| §5.6 NT→SA failure at step 1 (D_NT = ∅) | §5.6 lines 720–722 | ✓ — both NT and SA = {b}; only candidate fails the `≠` constraint |

PDF slides re-read with attention to mathematical content: 3, 6, 7, 12, 13, 14, 17, 18, 26, 27, 35–44, 45–53, 54. All chapter quotations remain faithful to slide wording. The mathematical edits introduced in Round 1 are all sound; the only new issues are figure-caption slippage in §4.7 (P1-R2-1) and an unflagged slide-39 internal inconsistency (P1-R2-2).

---

## Report to PM

**Assignment recap:** L07 (Constraint Satisfaction Problems) **Round 2**, Reviewer #2 — Mathematical Rigor focus. Verifying that the five Round-1 P1s were correctly fixed and that the revisions did not introduce new math errors. Source `Lecture7-Constraint Satisfaction Problem.pdf` (55 slides). Chapter `study/lectures/L07-CSP.md`.

**Status:** Pass with concerns.

**P0 findings:** None.

**P1 findings:**
1. **`L07-CSP.md:505`** — Figure caption "Stage 6 (slide 41): after X_2 = 4, X_3 ∈ {2}, X_4 ∈ {3}" mis-anchored. Slide 41 actually shows X3 = {2,4}, X4 = {2,3}; the post-FC reduction X3={2}, X4={3} appears on slide 42. The Round-1 revise-summary claimed this was fixed but the re-anchoring is wrong. Suggested fix: re-anchor as (40/41) = "X2=4 placed, FC pending", (42) = "FC reduces X3, X4", (43) = "about to assign X3", (44) = "X1=1 fully fails".
2. **`L07-CSP.md:494, around 499`** — Slide 39 itself contains an internal FC inconsistency (X4 should be {2} after X2=3 but slide shows {3}). The chapter's narrative correctly identifies the X3 wipeout but does not flag the X4 anomaly. Add a footnote noting the slide artifact and giving the correct FC computation, otherwise students will copy the slide's incorrect X4 state.
3. **`L07-CSP.md:714`** — §5.6 worklist initialisation lists `NT→NSW (not adjacent, skip)` inside an enumeration of "every directed arc between unassigned variables", which is logically inconsistent (a non-adjacent pair is not an arc). Either drop `NT→NSW` from the list or recast the framing. Also asymmetric: other non-edges (NT–V, NT–T, SA–T, NSW–T, V–T) are not enumerated-and-skipped. Recommend a clean eight-arc enumeration.

**P2 findings:**
1. **`§3.4.3:282`** — "the constants $1$, $2$ and $10$ are coefficients" — there is no literal `2` in the equation; drop "$1$, $2$ and".
2. (Subsumed by P2-R2-1.)
3. **`§4.7:523`** — Figure caption fig33 / "Stage 9 (slide 44)" claims trace continues with $X_1 = 2$; slide 44 is actually the terminal failure of $X_1 = 1$. Re-phrase to match the prose at line 525.
4. **`§5.6:727–731`** — Hypothetical-cascade table truncated with "…(continue)". Acceptable but a missed pedagogical opportunity to actually trace the cascade.
5. **`§4.8:569–586`** — `ARC-CONSISTENCY` returns "success/failure", `REVISE` returns Boolean. Type mismatch is unambiguous to a careful reader; minor pseudocode style nit.
6. **`§2.5:84–86`** — Caveat fuses two distinct points (FC vs slide-12 formulation, FC vs AC).
7. **`§2.9:112`** — Maiden-aunt caveat fuses "edges to unassigned" + "not tightness" — two unrelated points in one sentence.
8. **`§3.4.2:254`** — Lab 4 parenthetical breaks paragraph flow; move to footnote or §7 table.

Plus three Round-1 P2 carry-overs (P2-4 FC table row-ordering, P2-6 "irrelevant" gloss, P2-8 REVISE-empty-check style) deferred as acceptable.

**QA Checklist (§7) status:** N/A — this is a lecture-chapter review, not a feature-shipping QA. Per the per-review mathematical-rigor checklist:
- Per-slide claims traced to source: **Pass** with figure-caption slippage at slides 41 / 44 (P1-R2-1, P2-R2-3).
- Equations and arithmetic correct: **Pass**.
- Pseudocode mathematically sound: **Pass** (REVISE snapshot fix applied; minor return-type style noted).
- Worked examples (TWO+TWO=FOUR, 4-queens FC trace, x<y AC): **Pass** *except* the slide-41 figure-caption mismatch.
- Complexity claims sourced: **Pass** — both AC-3 cost statements now carry "beyond the slide" tags.
- Definitions match slides (scope, arc consistency, etc.): **Pass** — Round-1 scope error corrected.

**Acceptance criteria (§1) status:** N/A — same reason. As mathematical-rigor acceptance criteria:
- Every mathematical statement matches the slides or is explicitly marked as extrapolation: **Mostly Met** — extrapolations are now tagged, but slide 39 carries a slide-side error the chapter does not flag (P1-R2-2).
- Arithmetic in worked examples checks: **Met**.
- Constraint scopes / arities are correct: **Met** — scope-3 / scope-4 cryptarithmetic columns now correct.

**DOCUMENT.md audit:** N/A for this review type.

**Out-of-scope observations:**
- The K4 derivation added in §4.7 (line 477) is genuinely good pedagogy — explicitly tying "every pair of rows interacts via both `≠` and the diagonal" to "constraint graph is the complete graph K_4" is a notable improvement over Round 1.
- The §5.6 worklist trace, even with the minor P1-R2-3 wart, is a substantial pedagogical upgrade and worth keeping (don't trim).
- The chapter is now ~150 lines longer than Round 1; reading time estimate (60–75 min) is still plausible but starts to creak. If a future round trims, the hypothetical-cascade table in §5.6 (lines 725–731) is the lowest-load-bearing candidate.

**Concerns / risks:**
- The figure-caption slippage in §4.7 (P1-R2-1) is the kind of error a sharp examiner will catch when students cite specific slide numbers in their answer. The Round-1 fix moved the captions to "the correct slide numbers (40, 41, 42, 43)" but the new mapping is still off by one for the post-FC state. Students writing "as shown on slide 41" will be cross-checked against the actual slide 41 and marked down.
- The unflagged slide-39 X4 inconsistency (P1-R2-2) creates a trap: students who compute FC correctly will get the right *answer* (failure on X3) but a different *X4 state* than the slide shows, and may then doubt their own (correct) reasoning. A footnote closes this gap cheaply.
- No P0s. Math is fundamentally sound. The three P1s are all small (single-line edits, except P1-R2-1 which is four caption rewrites).

**What PM should do next:** Send the three P1s to the Lecture Extractor for Round-3 fixes:
- P1-R2-1: re-anchor four figure captions in §4.7 (slides 40, 41, 42, 43, 44).
- P1-R2-2: add a footnote in §4.7 noting the slide-39 X4 artifact.
- P1-R2-3: clean up the §5.6 worklist initialisation enumeration.

P2-R2-1 (the "1, 2 and 10" wart) is a one-word edit and can be batched. Other P2s can be deferred. After these fixes, no re-review needed from Reviewer #2 — the chapter will be in a solid mathematical state.

**DOCUMENT.md updated:** N/A for QA.
