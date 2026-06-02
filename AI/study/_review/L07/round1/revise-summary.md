# L07 — Round 1 — Revise Summary

**Chapter:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L07-CSP.md`
**Reviews consumed:**
- Reviewer #2 (Mathematical Rigor) — Pass with concerns; 5 P1s, 8 P2s.
- Reviewer #3 (Pedagogical Clarity / Analogies) — Fail; 3 P0s, 7 P1s, 7 P2s.
- Reviewer #4 (Exam Readiness) — Fail; 5 P0s, 10 P1s, 10 P2s.
- Reviewer #1 — file not present; PM-supplied P0 list used as substitute.

---

## P0 Fixes Applied (per PM's "KEY P0 FIXES" list)

### 1. §4.7 K4 claim — clarified

The chapter previously asserted "The constraint graph is the complete graph K4" without acknowledging that the slide-35 picture appears to omit edges. A new "Note on the slide-35 picture" paragraph now states: the slide visually emphasises a subset of K4's six edges, but the true constraint graph is K4 because every row pair interacts via both column-equality (`X_i ≠ X_j`) and the diagonal constraint (`|X_i − X_j| ≠ |i − j|`). All six pairs are connected. This is why forward checking after assigning X1 must prune X2, X3, AND X4.

### 2. Figure-to-slide alignment in §4.7 (slides 40–43 skew)

The figure captions were re-anchored to their correct slide numbers (40, 41, 42, 43) and the post-`X2 = 4` domain reasoning (slides 41–43) is now spelled out explicitly:
- After `X2 = 4`: `X3 ∈ {2}` (4 same column as X2), `X4 ∈ {3}` (column 2 removed by diagonal: |2−4| = 2 = |4−2|).
- After `X3 = 2`: `X4 = 3` is removed by diagonal `|3 − 2| = 1 = |4 − 3|`, so `D_{X4} = ∅`.

### 3. Cryptarithmetic carry domains — match slide

§3.4.3 now states verbatim: "Domains (slide 13 verbatim): `{0, 1, 2, …, 9}` for *all* variables — slide 13 gives the same domain for letters and carries." The narrower `{0, 1}` for carries is now clearly tagged as **beyond the slide**, with a short justification (max column sum 9 + 9 + 1 = 19, so carry ∈ {0,1}).

### 4. Slide 18 block-quote fabrication — replaced with verbatim quotes

§3.5 no longer concatenates two distinct passages from slide 18 into one fake quote. The slide-18 content is now presented as **two separate verbatim block-quotes**:
1. The commutativity statement with example.
2. The "we fix the order of assignments / m^n leaves" statement.
A closing prose line cites slide 18's actual final sentence: "Depth-first search for CSPs with single-variable assignments is called backtracking search."

### 5. §3.2 goal-test attribution mixes slide 7 and slide 16

§3.2 now opens with an explicit dual-citation: slide 7 ("CSP Formulation") uses Initial state, **Successor function**, Goal test, Path cost; slide 16 ("Standard search formulation (incremental)") uses States, Initial state, **Action**, Goal test. Each bullet now cites the appropriate slide(s). The successor-function-vs-action confusion is resolved: the lecture uses both terms interchangeably; both are recognised on exam.

### 6. Concrete AC-3 worklist trace for §5.6

§5.6 was previously a single-row table. It is now:
- A "starting state" table (domains after `WA = red, Q = green`).
- An explicit worklist initialisation listing every directed arc between unassigned variables.
- A step-by-step trace table (arc popped → REVISE outcome → action → re-queue) showing failure detected on the *first* revision (`NT → SA` with both domains = `{blue}` ⇒ `D_NT = ∅`).
- A hypothetical-cascade table (with `D_SA = {r, b}`) illustrating how the cascade would propagate in the more general case.

### 7. §4.7 4-queens trace at slide 39 — why X3 = 2 is also pruned

A dedicated "Why X3's domain `{2, 4}` becomes `{}` after X2 = 3" paragraph now spells out **both** removals:
- X3 = 2: queen at (3, 2) vs X2 = (2, 3); col-diff 1, row-diff 1 → diagonal conflict.
- X3 = 4: queen at (3, 4) vs X2 = (2, 3); col-diff 1, row-diff 1 → diagonal conflict.

### 8. §3.4.2 4-queens diagonal constraint — k ≠ 0 / j ≠ k scoping

The slide-12 row/column/diagonal/anti-diagonal constraints now carry explicit qualifiers:
- Row: `j ≠ k`.
- Column: `i ≠ k`.
- Main diagonal: `k ≠ 0` such that `(i+k, j+k)` is on the board.
- Anti-diagonal: `k ≠ 0` such that `(i+k, j−k)` is on the board.

A "Note (beyond the slide)" paragraph explains the slide omits these qualifiers and why they are mathematically required.

### 9. Missing §2 analogies for Consistent assignment, Degree heuristic, Constraint propagation

Three new §2 subsections added:
- **§2.8 A consistent assignment is like a Tetris board mid-game** — partial-but-clean intuition.
- **§2.9 Degree heuristic is like seating the maiden aunt first** — the maiden-aunt sentence has been **extracted** out of §2.2 and given its own subsection with its own breakdown caveat. §2.2 is now cleanly about the constraint graph only.
- **§2.10 Constraint propagation is like Newton's cradle** — cascade intuition that subsumes both forward checking and arc consistency.

All three follow the new visual format: blockquote `> **Where it breaks down.** …` for caveats.

### 10. Cross-links from §3/§4 to §2

Added/restored italic `*Recall §2.x…*` lines:
- §3.1 → §2.1 (Sudoku) and §2.8 (Tetris / consistent assignment).
- §3.4.4 → §2.1 (Sudoku formal).
- §4.1 → §2.7 (outfit-trying) and §2.1 (Sudoku-pencil-marks loop) — placed directly after the pseudocode.
- §4.4 → §2.9 (maiden aunt, degree heuristic).
- §4.6 → §2.10 (Newton's cradle, first impulse).
- §4.8 → §2.10 (full cascade).

### 11. $O(c·d^3)$ AC-3 complexity not on slides — source-tagged

§4.8 "Cost" bullet now reads: "Cost (beyond the slide): the textbook AC-3 worst case is $O(c · d^3)$ … The slides do not state this bound; cite it only as the textbook (Russell & Norvig) figure, not as a slide claim."

§8 cheat-sheet's "Cost of arc consistency" entry rewritten with the same explicit "beyond the slide" tag and an added warning: "AC-3 is polynomial-time preprocessing — it prunes impossible values but does not solve the CSP; backtracking after AC-3 is still exponential." (This also addresses Reviewer #4 P1-8.)

---

## Reviewer #2 (Math Rigor) P1s — Status

| Finding | Status |
|---|---|
| P1-1 Wrong scope claim for units-column cryptarithmetic | **Fixed** — §3.4.3 now states "scope 3 for units column; scope 4 for tens / hundreds"; the "implicit constant" phrase removed. |
| P1-2 n-queens slide-12 missing `j ≠ k` / `k ≠ 0` qualifiers | **Fixed** — §3.4.2 §K0-8 above. |
| P1-3 AC-3 complexity unsourced | **Fixed** — §K0-11 above. |
| P1-4 Compact formulation assertion on slides 35–44 | **Fixed** — §3.4.2 rewritten to "best read as the compact formulation; the slide does not write its constraint set explicitly". |
| P1-5 Imprecise wording in n!·m^n derivation | **Fixed** — §3.5 derivation rewritten using "branching factor at depth k = (n − k + 1) · m" and "leaf count is the product". |

Reviewer #2 P2s — status: P2-1 (REVISE iterator) fixed (snapshot); P2-2 carry domain (already fixed via slide-match); P2-3 SAT citation (Cook–Levin added); P2-5 Glossary front-matter naming (fixed); P2-7 LCV claim (fixed); P2-4, P2-6, P2-8 deemed acceptable / minor and deferred to round 2 polish.

## Reviewer #3 (Pedagogy) P0s and P1s — Status

| Finding | Status |
|---|---|
| P0-1 Missing analogies for Consistent assignment / Degree heuristic / Constraint propagation | **Fixed** — §2.8, §2.9, §2.10 added. |
| P0-2 §2.1 never cross-linked from §3 / §4 | **Fixed** — §3.1, §3.4.4, §4.1 now all link back. |
| P0-3 §2.7 cross-linked from §4.2 but not from §4.1 | **Fixed** — §4.1 now has a §2.7 recall line. |
| P1-1 Maiden aunt in wrong section | **Fixed** — extracted to §2.9 with dedicated breakdown caveat. |
| P1-2 §2.5 "clipboard" typo | **Fixed** — rewritten as "crossing off attacked squares on a candidate list". |
| P1-3 §2.6 directionality | **Fixed** — caveat expanded with explicit "values are passport-pages, not the passport itself" and "Z's claims are re-tested, not modified by edict of X". |
| P1-4 §2.3 caveat self-contradicting §4.4 | **Fixed** — caveat now correctly says degree heuristic is a tie-breaker, not a fix for MRV's general failure mode. |
| P1-5 §3.4.4 → §2.1 missing recall | **Fixed** (also covered by P0-2). |
| P1-6 caveats not visually distinct | **Fixed** — all §2 caveats now use `> **Where it breaks down.** …` blockquote format. |
| P1-7 §8 cheat-sheet maiden-aunt mismatch | **Fixed** — §8 entry now points to §2.9. |

Reviewer #3 P2s — status: P2-1 mapping table added to §2 preamble; P2-2 LCV caveat tightened; P2-3 §2.5 → §4.8 pointer fixed (and §2.1 → §4.6–§4.8); P2-4 MRV quantitative contrast added (binary-vs-7-candidate); P2-5 §2.7 DFS-not-BFS clarification added; P2-6 customs queue deemed acceptable after caveat expansion; P2-7 §2.1 pointer fixed.

## Reviewer #4 (Exam Readiness) P0s — Status

| Finding | Status |
|---|---|
| P0-A §2.5 FC analogy mismatch with slide-12 | **Fixed** — §2.5 rewritten in candidate-list / domain language; explicit caveat notes that the picture maps cleanly only onto the compact formulation. |
| P0-B §3.4.2 k-quantifier scoping | **Fixed** — see #8 above. |
| P0-C AC-3 cascade hand-waved | **Fixed** — see #6 above (§5.6 trace). |
| P0-D §4.7 slide-39 explanation incomplete | **Fixed** — see #7 above. |
| P0-E AC-3 complexity unsourced | **Fixed** — see #11 above. |

Reviewer #4 P1s — status: P1-1 (cascade table) and P1-2 (pseudocode demarcation) fixed; P1-3 (Lab 4 confusion) fixed in §3.4.2; P1-4 (degree heuristic "weaker than MRV" editorial) fixed by removing the unsourced claim and quoting slide 27 instead; P1-5 (hypergraph description) fixed in §6 pitfall #11 with explicit drawing instructions; P1-6 (successor-function vs action) fixed; P1-7 (4-queens continuation) added; P1-8 (cheat-sheet AC-3 polynomial vs CSP NP-complete) clarified; P1-9 (consistent/complete/solution table) added as Pitfall #1; P1-10 (AC-3 naming consistency) — chapter now consistently uses "arc-consistency algorithm" in body and "AC-3" in glossary line + cheat-sheet, with explicit "the slides do not name it AC-3" disclaimer.

Reviewer #4 P2s — status: P2-1 8^8 "no redundancies" phrase added in §1; P2-3 register allocation removed from §1; P2-5 "other solutions exist" parenthetical retained but clarified; P2-6 "totalling" replaced with "product" / "leaf count is the product"; P2-7 reading time bumped to 60–75 min; P2-9 MRV "most-cornered" pairing with canonical term done. Remaining P2s deferred.

---

## Net change

Approximate net additions: ~150 lines across the chapter (§2 +3 subsections + caveats blockquoted; §3.2 expanded; §3.4.2 constraint qualifiers + alt-formulation rewrite; §3.4.3 hypergraph + carry-domain note; §3.5 rederivation; §4.7 K4 note + slide-39 reasoning + slide-41 reasoning + continuation; §4.8 pseudocode demarcation + source-tagged complexity; §5.6 worklist trace; §6 pitfall #1 table + pitfall #10 polynomial-vs-NP clarification + pitfall #11 hypergraph drawing).

No content removed beyond inaccurate claims (e.g. "register allocation in compilers", "weaker than MRV on its own", "implicit constant").

Chapter still cites slides verbatim where appropriate; new "beyond the slide" notes mark every textbook extrapolation.

---

## Open questions for next reviewer round

1. Whether Reviewer #1's file is intended to exist or whether the PM list above is the substitute. Currently no `reviewer1.md` is present in `study/_review/L07/round1/`.
2. The hypothetical-cascade table in §5.6 is illustrative — confirm whether reviewer wants it kept or trimmed.
3. Whether the §2.10 Newton's cradle analogy is acceptable as the constraint-propagation analogy or whether reviewers prefer a different image (e.g. "domino chain"). The Newton's cradle / cascade pairing is intentional because both forward checking and arc consistency share the cascade shape.
