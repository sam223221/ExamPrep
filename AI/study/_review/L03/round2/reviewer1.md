# L03 Round 2 — Reviewer #1: Concept Completeness (incl. Figures)

**Scope of this review:** Verify every Round 1 P1 (six findings) is correctly addressed in the revised `study/lectures/L03-Uninformed-Search.md`. Re-audit `study/extracted_figures/L03/figures.md` for residual inconsistency. Spot-check for new regressions introduced by the substantial rewrite (chapter grew from ~633 lines to ~805 lines; many new subsections). Lens unchanged: missing concepts, broken prose, dropped slide-bullets.

---

## VERDICT

**APPROVED**

Every Round 1 P1 is fixed cleanly. The six previously-dropped slide concepts now appear at the right locations, with the right phrasings, and are also reinforced in the cheat sheet. The broken §5.5 DFS table cell is gone, replaced by a single clean 8-row table with the LIFO push-convention stated above it. The figures.md SKIP justification for `fig08` is now factually accurate because the state count is captured in §3.3.1. No new P0 issues introduced. Two minor P2 observations on the new content are listed below — both are polish items, not blockers.

---

## Round 1 P1 verification

### P1-1 — Slide 15 (state counts + NP-hardness) — FIXED

New §3.3.1 "How big can state spaces get? — the n-Puzzle (slide 15)" at chapter lines 163–173 contains:
- 8-puzzle: $9!/2 = 181{,}440$ states ✓
- 15-puzzle: $> 10^{13}$ ("more than ten *trillion* states") ✓
- 24-puzzle: $\approx 10^{25}$ states ✓
- **Bold n-Puzzle NP-hardness claim** ("finding an optimal solution to the n-Puzzle is NP-hard") ✓
- Bonus parity explanation for the $9!/2$ factor (lines 173) — a nice addition that students will find clarifying.

The cheat sheet (§8) also reproduces all four facts in one line: *"8-puzzle = 181,440; 15-puzzle > 10¹³; 24-puzzle ≈ 10²⁵. Optimal n-Puzzle is NP-hard."* Verified at chapter line 759.

Grep for "181,440" returns 2 matches (§3.3.1 and §8) — both correct locations. Grep for "NP-hard" returns 2 matches in the same locations.

### P1-2 — Slide 6 motivation triad — FIXED

New §1.1 "Why search? (slide 6)" at chapter lines 18–26 enumerates all three motivational bullets:
1. "Search strategies are important methods for many approaches to problem-solving" ✓
2. "To use search, you must first abstract the problem into states and the available steps" ✓
3. **"Search algorithms are the basis for many optimisation and planning methods"** (the critical forward-link bullet that was the reason this P1 was raised) ✓

The closing paragraph at line 26 ties the third bullet forward to L05 hill-climbing and L07 CSP — exactly the framing that was missing in Round 1.

### P1-3 — Slide 17 four design questions — FIXED

New §3.2.1 "The four design questions (slide 17)" at chapter lines 141–150 lists all four questions verbatim:
1. State representation ✓
2. Goal recognition ✓
3. Possible actions ✓
4. Relevant information encoding ✓

The mapping back to the five components of §3.2 (Q1 → initial state + state representation, Q2 → goal test, Q3 → successor function, Q4 → step-cost + auxiliary) is also given. Cheat sheet line 751 reinforces this as "Four design questions (slide 17): How to represent state? How to recognise the goal? What are the actions? What relevant info to encode?". The rubric framing the Round 1 review asked for is explicit ("when an exam question says 'formulate problem X as a search task', these are the four questions you answer").

### P1-4 — Slide 5 three warm-up examples — FIXED

New §3.1.1 "Slide-5 warm-up: three everyday problem-formulation examples" at chapter lines 119–127 contains all three slide-5 examples with the initial/goal/operators triple for each:
- Home → SDU (walk, bus, cycle, drive, train) ✓
- Loading a moving truck ✓
- Getting settled in a new flat ✓

The pedagogical framing ("see the *same triple* — initial state, goal, available operators — recur") explicitly states why these warm-ups matter, which is what was missing in Round 1.

### P1-5 — DFS §5.5 broken table cell — FIXED

The Round 1 problematic cell

> | 2 | pop C (top), push F, G | `[B, F, G]` — wait. *Standard convention:* push children in *reverse* order...

is gone. Grep for "wait" against the chapter returns 0 matches. The replacement at chapter lines 601–616 is a single clean trace:

- One sentence above the table at line 603 states the convention: *"DFS pushes children onto the LIFO stack in right-to-left order, so the leftmost child ends up on top of the stack and gets popped next."*
- Single 8-row table walks A → B → D → E → C → F → G → goal correctly. Every row's frontier state is consistent with LIFO + right-to-left push convention.
- No mid-cell retraction, no "— wait", no second table.

Step-by-step verification of the new trace against slide-46 traversal A → B → D → E → C → F → G:

| Step | Pop | Frontier after | Matches slide? |
|------|-----|----------------|-----------------|
| 0 | – | `[A]` | ✓ |
| 1 | A | `[C, B]` (B on top, push C then B) | ✓ |
| 2 | B | `[C, E, D]` (D on top) | ✓ |
| 3 | D | `[C, E]` (no children) | ✓ |
| 4 | E | `[C]` (no children) | ✓ |
| 5 | C | `[G, F]` (F on top, push G then F) | ✓ |
| 6 | F | `[G]` | ✓ |
| 7 | G | goal | ✓ |

Trace is correct and clean.

### P1-6 — figures.md fig08 SKIP justification — FIXED

The fig08 SKIP justification at `figures.md` line 29 still reads:

> "...the lecturer's point (state count is 9!/2 = 181,440) is captured better as a number than as a tile picture."

This claim is now **factually accurate** because the chapter does capture the state count (verified above under P1-1). The reviser's choice not to edit `figures.md` is therefore correct — the catalogue's justification became true by virtue of the chapter being fixed. No further edit needed.

---

## P0 — Blockers

**None.** No factual errors, no broken prose, no new slide content silently dropped. Spot-check of all six fixes confirms they land in the right places with the right phrasings.

---

## P1 — Important (new issues introduced by the rewrite)

**None.** The revision is internally consistent. Six new subsections added in this round (§1.1, §3.1.1, §3.2.1, §3.3.1, §4.2.1, §4.4.0, §4.5.1, §5.1.1, §5.2.2, §5.3.1, §5.6.1, §5.7, §5.8) all read cleanly. The expanded §5.5 DFS trace is sound. The new §5.7 BFS-vs-UCS contrast on the slide-37 graph is a strong pedagogical addition.

---

## P2 — Polish, suggestions

### P2-1 — §5.3 Step 7 fringe "`G : 14`" tabular row is honest but visually confusing

Chapter line 563 prints `G : 14` *(per slide)* in the fringe column for step 7. The pedagogical note immediately below (line 566) correctly explains that this reflects the slide's display rather than the algorithm's actual behaviour, and the exam-answer guidance (line 568) tells the student which to write under different exam framings. This is the *correct* handling of the slide-vs-algorithm tension. However the table-row content `G : 14` is itself a tiny bug in the slide that has now propagated into the chapter table. A future polish pass could add a parenthetical right inside the cell (e.g. `G : 14 (slide-display) — algorithm retains G : 8`) so the asterisked "per slide" annotation is not the only signal that something unusual is happening. Not a blocker; the existing prose note already covers it.

### P2-2 — §5.1.1 Step 1 cell has a stream-of-consciousness aside

Chapter line 466 contains:

> | 1 | pop `(A,1,1)`, not goal. Expand: $L$→`(A,1,1)`(no-op, skip — self-loop already in frontier? actually new, in explored after pop), $R$→`(B,1,1)`, $S$→`(A,0,1)` | ...

The phrase *"already in frontier? actually new, in explored after pop"* is the exact failure mode that bit §5.5 in Round 1 — a mid-cell self-correction surviving into the published table. The conclusion is correct (the $L$-self-loop is suppressed because $(A,1,1)$ is in `explored` after the pop) but the narration is muddled. A clean rewrite:

> "pop `(A,1,1)`, not goal. Expand. $L$ → `(A,1,1)` self-loop, already in explored after the pop, skip. $R$ → `(B,1,1)`. $S$ → `(A,0,1)`."

Same outcome, no internal question-marks. This is the same polish category as Round 1 P2-1 — flagged here because it is the only remaining instance of the pattern Round 1 specifically criticised.

### P2-3 — §3.3.1 parity sentence under-specifies the partition

Chapter line 173:

> "The factor $1/2$ in $9!/2$ comes from the fact that exactly half of the $9!$ tile arrangements are reachable from any given starting configuration..."

The factor $1/2$ is correct. A pedantic reader might want to see the term "permutation parity" or "even permutations" used explicitly, but the parenthetical *"(the other half live in a disconnected component, distinguishable by tile-permutation parity)"* arguably suffices. Optional sharpening only.

---

## EVIDENCE — Slide-by-slide coverage matrix (Round-2 delta)

Every Round 1 OK row remains OK. Below is the delta only — slides whose verdict changed between Round 1 and Round 2:

| Slide | Topic | Round 1 verdict | Round 2 verdict | Where |
|---|---|---|---|---|
| 5 | Three real-life examples (home→SDU, moving truck, getting settled) | **P1-4 DROPPED** | **OK** | §3.1.1 (chapter L119–127) |
| 6 | Motivation triad (strategies / abstract formulation / basis for opt+planning) | **P1-2 DROPPED** | **OK** | §1.1 (chapter L18–26) |
| 15 | 8-puzzle state counts + NP-hard | **P1-1 DROPPED** | **OK** | §3.3.1 (chapter L163–173) + §8 cheat-sheet L759 |
| 17 | Four design questions | **P1-3 DROPPED** | **OK** | §3.2.1 (chapter L141–150) + §8 cheat-sheet L751 |
| 38–46 | DFS animation | **P1-5 broken Step 2 cell** | **OK** | §5.5 (chapter L601–616), single clean trace |
| (figures.md) | fig08 SKIP justification | **P1-6 inconsistent** | **OK** | resolved by chapter side (P1-1 fixed makes justification true) |

All other slide-coverage rows (slides 1–4, 7–14, 16, 18–37, 47–56) remain at the Round 1 verdict (OK except slide 16 / 19 / 11 which were P2-only and noted in Round 1).

---

## EVIDENCE — Slide-15 specific re-verification

Round 1 grep for "181,440 / 9!/2 / NP-hard / 10 trillion / 10^25 / 24-puzzle / 15-puzzle" returned zero matches. Round 2 grep:

- `9!/2` → 2 matches (lines 167, 173).
- `181,440` → 1 match (line 167, with the proper TeX `{,}` typesetting).
- `NP-hard` → 2 matches (lines 171, 759).
- `10^{13}` / `10¹³` → 2 matches (lines 168, 759).
- `10^{25}` / `10²⁵` → 2 matches (lines 169, 759).
- `15-puzzle` → 2 matches.
- `24-puzzle` → 2 matches.
- `10 trillion` → 1 match (line 168 — "more than ten *trillion* states").

All slide-15 content now lives in the chapter at both the main section (§3.3.1) and the cheat sheet (§8).

---

## EVIDENCE — DFS Step-2 specific re-verification

Round 1: chapter line 467 contained the broken `| 2 | pop C (top), push F, G | [B, F, G] — wait. Standard convention: ... |` cell.

Round 2 grep for "wait" against the chapter file: **0 matches.** The whole second-thoughts pattern is eradicated. The replacement table at lines 605–616 is a single clean walk through the binary tree with explicit "right-to-left push" convention stated above the table (line 603).

---

## EVIDENCE — figures.md re-audit

- All 15 USE/REWORK figures from Round 1 remain embedded in the chapter (grep-verified).
- No new figures embedded since Round 1.
- The fig08 SKIP justification text is unchanged but now accurate (because §3.3.1 captures the state count).
- All other 57 SKIP justifications unchanged from Round 1; all remain valid.

---

## EVIDENCE — A\* honesty preserved

The chapter still discloses the A\*/heuristics gap in five separate places (§1.2 "Honest note on scope", §3.7 closing line, §3.8 forward reference, §4.5 Figure 5 caption, §6 Pitfall #10, §8 cheat-sheet last bullet). Round 1 commendation stands.

---

## Concerns / risks

- **Chapter length.** Now ~805 lines / ~60 min reading time (per the chapter's own header). At the long end of "study cheat sheet" but the new worked examples (§5.1.1, §5.2.2, §5.7, §5.8, §4.2.1) close real exam-readiness gaps. Acceptable.
- **§5.3 Step 7 slide-vs-algorithm reconciliation.** The chapter's framing ("write `G:14` if reproducing the slide; write `G:8` if explaining UCS; the optimal path is the same either way") is the correct pedagogical move given the slide's own inconsistency. Noted as P2-1 above.

---

## PM Report

**Assignment recap:** L03 Round 2 Reviewer #1 — Concept Completeness (incl. Figures). Verify all six Round 1 P1 findings are resolved without introducing new P0 / P1 issues.

**Status:** APPROVED.

**P0 findings:** 0.

**P1 findings:** 0.

**P2 findings:** 3.
1. §5.3 Step 7 `G:14` cell could be made self-explanatory inside the cell (currently relies on the prose note immediately below — works, but slightly inelegant).
2. §5.1.1 Step 1 cell contains a Round-1-style self-correcting aside ("self-loop already in frontier? actually new, in explored after pop"). Conclusion is correct; the narration is muddled. Quick rewrite suggested.
3. §3.3.1 parity sentence could use the words "permutation parity" / "even permutations" explicitly. Optional.

**Round 1 P1 status (each):**
- P1-1 (slide 15 state counts + NP-hard) — **FIXED** (§3.3.1 + §8 cheat-sheet).
- P1-2 (slide 6 motivation triad) — **FIXED** (§1.1).
- P1-3 (slide 17 four design questions) — **FIXED** (§3.2.1 + §8 cheat-sheet).
- P1-4 (slide 5 three warm-up examples) — **FIXED** (§3.1.1).
- P1-5 (broken DFS §5.5 Step 2 cell) — **FIXED** (clean §5.5 rebuild; "wait" gone; trace correct).
- P1-6 (figures.md fig08 SKIP justification inconsistent) — **FIXED** (the chapter side change makes the justification text factually accurate; no edit to figures.md needed).

**Honesty about A\* gap:** Excellent — preserved across five chapter locations. No penalty.

**What PM should do next:**
1. Accept this round-2 review as a pass for Reviewer #1 lens.
2. Cross-reference against Reviewer #2 (Mathematical Rigor) and Reviewer #4 (Exam Readiness) round-2 verdicts before declaring L03 done — the substantial §5.3 rewrite and the new worked examples affect those lenses more than mine.
3. Optionally schedule a polish pass to handle the 3 P2 items above (very minor; can be folded into a global L03–L13 stylistic sweep).
4. Once all four round-2 lenses approve, dispatch `pm-context-updater` to refresh `PM/history.md` with the L03 outcome.

**DOCUMENT.md updated:** N/A for a study-chapter review.
