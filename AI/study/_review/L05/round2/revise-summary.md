# L05 Round 2 → Round 3 Revise Summary

**Scope:** P1-only cleanup pass over the Round 2 reviewer reports. No
P0s were raised in Round 2 — all four reviewers issued APPROVED or PASS
verdicts modulo the P1s addressed here. P2s are deferred to backlog.

**Source reports consulted:**
- `study/_review/L05/round2/reviewer1.md` (Concept Completeness incl. Figures)
- `study/_review/L05/round2/reviewer2.md` (read for context — not the source of any fix in this pass)
- `study/_review/L05/round2/reviewer3.md` (Pedagogical Clarity incl. Analogies)
- `study/_review/L05/round2/reviewer4.md` (Exam Readiness)

**Files touched:**
- `study/lectures/L05-Local-Search.md`
- `study/extracted_figures/L05/figures.md`

---

## P1 fixes applied

### Fix 1 — figures.md falsely claims chapter has Mermaid diagrams (R1-P1-1, carryover from Round 1)

**File:** `study/extracted_figures/L05/figures.md` (lines 82–85).

**Before:** "...the chapter additionally backs each up with a Mermaid
diagram or in-text prose where extra clarity helps."

**After:** "...the chapter additionally backs each up with in-text prose
where extra clarity helps."

**Rationale:** The chapter contains zero Mermaid blocks (verified). The
catalogue must accurately describe what the chapter does.

**Edit size:** dropped "a Mermaid diagram or" — one phrase.

---

### Fix 2 — §5.4 slide-12 left-board caption was internally inconsistent ("8 values one per row, queen's row marked separately") AND left/middle 8-vs-7 asymmetry was unexplained (R1-P1-2 + R4-P1-2)

**File:** `study/lectures/L05-Local-Search.md` (slide-12 figure caption).

**Before:** "**Left:** ...the labels (top to bottom) are $\{2, 2, 1, 2,
3, 1, 2, 2\}$ (one per row of the column; the queen's current row is
marked separately). The minimum among these is $h = 1$... **Middle:**
...row-scores $\{3, 3, 2, 3, 2, 3, 0\}$..."

The two clauses contradicted (8 values cannot be both "one per row" and
"with the queen's row marked separately"); R4 separately raised the
asymmetry between the left board's 8 labels and the middle board's 7
labels.

**After (single edit closes both findings):** "**Left:** ...eight values
in total. Seven of these are alternative-row successor scores; the
eighth — the label in the queen's *current* row — annotates the queen's
current contribution to the conflict count (also 2), not a successor.
The minimum *successor* score is $h = 1$... **Middle:** ...only its
seven alternative-row successor scores $\{3, 3, 2, 3, 2, 3, 0\}$ (the
slide omits an annotation for the current row on this board)... The
left/middle asymmetry — 8 labels vs 7 — is purely an annotation
choice; under the per-column formulation each column has exactly 7
successors (current row excluded; §5.4)."

**Rationale:** Option B from R1-P1-2 (chapter keeps the 8-value list,
which matches the slide visually) with explicit disambiguation; R4-P1-2
asymmetry resolved by the new "purely an annotation choice" sentence.
Pedagogical point (the $h = 1$ trap) is unchanged — the fix is purely
clarification.

---

### Fix 3 — §2.E "Temperature schedule" caveat said "GA schedulers" instead of "SA schedulers" (R3-P1)

**File:** `study/lectures/L05-Local-Search.md` (§2.E temperature schedule
sub-section, line ~184).

**Before:** "...GA schedulers can use any monotone-decreasing function,
including ones with no physical analogue."

**After:** "...SA schedulers can use any monotone-decreasing function,
including ones with no physical analogue."

**Rationale:** Temperature schedules are a feature of simulated
annealing, not genetic algorithms. One-word fix; R3 flagged it as
exactly the kind of error a careful student notices because the marble
analogy was just introduced in §2.C (SA).

---

### Fix 4 — §5.8 lacked a worked accept/reject decision against a uniform-random draw $u$ (R4-P1-1)

**File:** `study/lectures/L05-Local-Search.md` (§5.8, end of section).

**Before:** §5.8 ended with the three-temperature snapshot table
(holding $\Delta = -5$ fixed and varying $T \in \{100, 10, 1\}$) and
the one-line moral "By the time $T$ has dropped to 1...the algorithm
has become greedy hill climbing."

**After:** Added a substantial new sub-section "Accept/reject with a
uniform draw — the operational step" containing:

1. The accept-rule restatement $u < \exp(\Delta / T) \Rightarrow$ accept.
2. A 3-row worked trace under geometric cooling ($T_0 = 100$,
   $\alpha = 0.9$) for proposed moves $\Delta = +2, -3, -10$ with
   uniform draws $u = 0.4, 0.8, 0.6$ — full arithmetic (cumulative $T_t$,
   exponential, comparison, decision).
3. A contrast 3-row trace at $t = 50$ (so $T_{50} \approx 0.515$) with
   the *same three draws* showing that the same two downhill moves
   accepted early are *rejected* late — making the
   exploration-then-exploitation behaviour explicit.
4. Exam tip: state $u$, compute $\exp(\Delta/T)$, write the comparison.

**Rationale:** R4-P1-1 (carryover from Round 1 P1-9). The Round 1 P1-9
was demoted to P1 in Round 2 because the temperature-comparison table
was partial coverage; R4 said one $u$-draw worked example would close
the gap entirely. This edit goes further with a two-phase contrast
(early-T vs late-T with same $u$s) for pedagogical sting.

**Side-effect on reading time:** §5.8 grows by ~30 lines. R4-P2-2 had
already noted the chapter likely exceeds the "~55 min" front-matter
estimate; this addition pushes it further. Reading-time recalibration
remains deferred per Round 1 P2-10.

---

### Fix 5 — §6 plateau pitfall said hill climbing "walks indefinitely" without finite-state-space caveat (R4-P1-3)

**File:** `study/lectures/L05-Local-Search.md` (§6 "Plateaux vs ridges
vs local maxima" sub-section, plateau bullet).

**Before:** "Plateau / flat local maximum: all immediate neighbours
have *equal* value, and there's no way out by neighbour evaluation
alone. Hill-climbing test is *false* (no strict decrease) → algorithm
**walks indefinitely** across the plateau. This is the slide-13 rule's
well-known pathology."

**After:** "Plateau / flat local maximum: all immediate neighbours have
*equal* value, and there's no way out by neighbour evaluation alone.
Hill-climbing test is *false* (no strict decrease) → algorithm **walks
indefinitely** across the plateau (more precisely: on an *unbounded or
cyclic* plateau the walk is infinite; in a **finite state space** the
algorithm walks until it either falls off — a strict-decrease boundary
terminates it — or revisits states in a cycle, in which case
implementations typically cap it with a step budget). This is the
slide-13 rule's well-known pathology."

**Rationale:** R4 noted the strong claim "walks indefinitely" is true
on an unbounded plateau but not in a finite state space (which is
every state space we care about). The parenthetical preserves the
slide-13 rule semantics while adding the practical caveat.

---

### Fix 6 — §3.3 pseudocode `next ← argmax` was silent on tie-breaking (R4-P1-4)

**File:** `study/lectures/L05-Local-Search.md` (§3.3 pseudocode + new
prose paragraph).

**Before:** Pseudocode line read `next ← argmax over neighbours(current)
of value(s)      # successor` with no mention of ties; the §5.4 board
explicitly demonstrates tie-breaking is exam-relevant but §3.3 said
nothing about it.

**After:**
1. Pseudocode comment changed to `# ties broken arbitrarily — see §3.4
   for variants`.
2. Added a new prose paragraph "Tie-breaking" after the
   improvement/plateau/strict-decrease case analysis. It points out
   that the baseline policy is implementation-defined (first-found,
   uniform-random, lexicographic), cites the §5.4 8-queens example as
   evidence that tie-breaking can decide global-vs-local-optimum, and
   notes how §3.4's first-choice and stochastic variants make the
   policy explicit.

**Rationale:** R4-P1-4. Closes the loop between §3.3 (baseline
pseudocode) and §5.4 (tie-break-dependent example). §4.1's pseudocode
is left unmodified because it is tagged "slide 13 verbatim"; the
explanation lives in §3.3.

---

## Items NOT addressed in this pass

### R1 P2s — figure-catalogue polish (lines fig01 page-render note, slide-21 SKIP carryover, coverage roll-up)

Out of scope for a P1-only revision pass. Backlog.

### R1 P2-2 (post-figure prose "two rows give $h = 1$"), P2-3 (slide-43 parents explicit), P2-4 (1-indexed forward-ref from §4.3 to §5.7), P2-5 (catalogue figure-free section list)

Out of scope. Backlog.

### R3 P2-1 through P2-7 (§3.4 cross-link redeployment, §2.E ordering, §3.6.x sub-cross-links, §5.7 mutation rate intuition, §6 cross-ref, off-by-one for power-of-2, reading-time recalibration)

Out of scope. Backlog. R3 explicitly recommended deferring these to
backlog after the one-word fix.

### R4 P2-1 through P2-7 (R&N "iterations" wording, reading-time recalibration, 1-vs-0-indexing cross-lecture warning, exact 2-opt count $n(n-3)/2$, §4.4 "Best for" editorial flagging, §5.5 slide-14 attacking-pair claim)

Out of scope. Backlog. R4 explicitly recommended advancing to the next
gate after the four P1s were closed.

---

## Self-verification

- **R1 P1-1** (figures.md Mermaid claim): Edit applied. Verified the
  phrase "Mermaid diagram" no longer appears in
  `study/extracted_figures/L05/figures.md`.
- **R1 P1-2** (§5.4 left-board count inconsistency): Edit applied. New
  caption is internally consistent (eight values are listed, seven are
  successors, the eighth is annotated as the queen's current contribution
  — no contradictory clauses).
- **R3 P1** (GA → SA): Edit applied. Verified "GA schedulers" no longer
  appears in §2.E.
- **R4 P1-1** (u-draw worked example): Edit applied. §5.8 now contains
  two 3-row worked traces (one at $t = 1, 2, 3$ accepting all moves;
  one at $t = 50$ rejecting both downhill moves with the same $u$
  draws) — the exact shape of exam-question Q5 from R4's question set.
- **R4 P1-2** (§5.4 figure asymmetry): Closed jointly with R1 P1-2
  by the same edit. New caption explicitly says "purely an annotation
  choice...each column has exactly 7 successors."
- **R4 P1-3** (finite-state-space / step-budget caveat): Edit applied.
  §6 plateau bullet now contains "(more precisely: on an *unbounded or
  cyclic* plateau the walk is infinite; in a **finite state space**
  the algorithm walks until it either falls off — a strict-decrease
  boundary terminates it — or revisits states in a cycle, in which
  case implementations typically cap it with a step budget)".
- **R4 P1-4** (tie-breaking): Edit applied. §3.3 pseudocode comment
  updated; new "Tie-breaking" prose paragraph added cross-referencing
  §5.4 and §3.4.

---

## What round-3 reviewers should look at

- **R1:** verify Fix 1 (figures.md) and Fix 2 (§5.4 left-board prose) —
  the two P1s in R1's report.
- **R3:** verify Fix 3 (one-word edit). Should be approve-and-move-on.
- **R4:** verify Fixes 4, 5, 6 (§5.8 u-draw example, §6 plateau caveat,
  §3.3 tie-breaking). R4-P1-2 was closed jointly with R1-P1-2 — see
  Fix 2.
- **R2:** no R2 P1s addressed in this pass (R2's Round 2 report not the
  source of any P1 in the brief); spot-check the §5.8 worked example
  for mathematical rigor.
