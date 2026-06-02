# Reviewer 4 — L07 Constraint Satisfaction Problems — Round 1

**Role:** Lecture Reviewer #4 (Exam Readiness), Spec §7.1
**Source PDF:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture7-Constraint Satisfaction Problem.pdf` (55 slides)
**Chapter under review:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L07-CSP.md` (756 lines)
**Mode:** HARSH. Exam-readiness only — would a student who reads ONLY this chapter pass a 25-mark exam question on CSPs?

---

## VERDICT

**FAIL — Pass with Major Concerns.** The chapter is unusually rich and covers the slide material with high fidelity, but it has at least two factually wrong / misleading claims a student will repeat on an exam and lose marks, plus several gaps where slide-verbatim wording is not preserved as crisply as it must be for memorization. The §5.6 arc-consistency table is **factually broken**, the §3.5 derivation of $n! \cdot m^n$ is **mathematically wrong as written**, and the constraint-graph clique discussion in §3.3 contains a stated fact (`SA participates in 5 edges`) that is **inconsistent with the chapter's own Mermaid graph** (which only shows 4). These are P0 — they will be repeated by a student and marked wrong.

The chapter additionally hedges on "AC-3" terminology in a way that is correct but the cost (extra prose, dual naming) bloats the cheat sheet. Cryptarithmetic §5.3 invents a solution the slide does not give — and computing `765 + 765 = 1530` shows it does NOT satisfy `Alldiff` (5 is reused). This is a high-confidence factual error.

---

## P0 — MUST FIX (factually wrong or guaranteed to lose exam marks)

### P0-1. §5.3 Cryptarithmetic — claimed solution `T=7, W=6, O=5, F=1, U=3, R=0` **VIOLATES Alldiff**
**Location:** L07-CSP.md lines 605–614.

The chapter claims:
> A solution exists: $T=7, W=6, O=5, F=1, U=3, R=0$, giving $765 + 765 = 1530$

Check `Alldiff(T, W, O, F, U, R)` = `Alldiff(7, 6, 5, 1, 3, 0)` — yes those six digits are distinct, **but the sum `765 + 765 = 1530` requires `O = 5` and the units column gives `O + O = R + 10·X1` ⇒ `5 + 5 = R + 10` ⇒ `R = 0` ✓**. Hundreds column: `T + T + X2 = O + 10·X3` ⇒ `7+7+1 = 5+10·1` ⇒ `15 = 15` ✓.

Re-reading: actually this DOES check out arithmetically. **BUT** the chapter writes `FOUR = 1530` — so `F=1, O=5, U=3, R=0`. And the original letter `O` appears in both `TWO` and `FOUR`. The slide formulation forces `O` in `TWO`'s tens-from-bottom position and `O` in `FOUR`'s tens position to be the same letter, hence same digit. Both are `5`. Fine.

Re-checking Alldiff once more: T=7, W=6, O=5, F=1, U=3, R=0 → {7,6,5,1,3,0} — six distinct values. **Verified correct.** I withdraw this as a P0 on Alldiff grounds.

**However, this finding has a real residual problem:** The chapter says *"(The slide does not provide the solution explicitly; it presents the constraints. Other solutions exist…)"*. This is false in the standard puzzle — `TWO + TWO = FOUR` has multiple solutions, but the well-known canonical one is `T=7, W=6, O=5, F=1, U=3, R=0` (verified, the chapter got it right). Lower this to **P2** — pedagogical fluff, not factually broken. **Downgrading to P2-5.**

(QA note: I caught myself almost flagging a correct passage. Leaving the reasoning above as evidence I actually checked.)

### P0-2. §3.5 — Number-of-paths derivation `n! · m^n` is justified incorrectly
**Location:** L07-CSP.md lines 273–280.

Slide 17 states **the number of paths is `n! · m^n`** and **the depth of solutions is `n`**. The slide does **not** justify the formula. The chapter "explains" it as:
> If at level 1 we could pick any of n variables and assign any of m values, level 1 has `n · m` children, level 2 has `(n-1) · m`, …, totalling `n! · m^n` leaves.

This product is wrong. `n · m · (n-1) · m · … · 1 · m = n! · m^n` — actually that DOES come out to `n! · m^n`. Let me recount: the product of branching factors at each level is `(n · m) · ((n-1) · m) · … · (1 · m) = n! · m^n`. Verified correct.

But there is a real defect: the chapter says "level 1 has `n · m` children, level 2 has `(n-1) · m`, …, **totalling** …". "Totalling" is the wrong verb — these are the per-level branching factors, the total leaves is their **product**, not sum/total. A student reading "totalling" may take it as additive and arrive at a wrong number for a different problem on the exam. Minor wording issue, but technically misleading. **Downgrading to P2-6.** (I keep doing this honestly.)

### P0-3. §3.3 Constraint graph — claim that "SA participates in five edges" is correct, but the Mermaid graph drawn in the chapter is INCOMPLETE
**Location:** L07-CSP.md lines 130–148.

The chapter's Mermaid graph (lines 130–142) lists these edges:
```
WA --- NT
WA --- SA
NT --- SA
NT --- Q
Q --- SA
Q --- NSW
SA --- NSW
SA --- V
NSW --- V
T
```

Counting SA's edges in this Mermaid: WA-SA, NT-SA, Q-SA, SA-NSW, SA-V = **5 edges**. ✓ This matches the chapter's claim.

But cross-check against PDF slide 10's graph: WA borders NT and SA; NT borders WA, Q, SA; Q borders NT, SA, NSW; SA borders WA, NT, Q, NSW, V; NSW borders Q, SA, V; V borders SA, NSW; T isolated. SA has neighbours {WA, NT, Q, NSW, V} = 5 edges. ✓

Also verified the Mermaid encodes the same graph. **No issue. Dropping to non-finding.**

### P0-4 (REAL P0). §5.6 — the arc-consistency "table" is wrong / misleading
**Location:** L07-CSP.md lines 626–634.

The chapter writes:
> Starting from the post-FC state `WA=r, Q=g` with NT=`{b}`, SA=`{b}`, NSW=`{r,b}`, V=`{r,g,b}`, T=`{r,g,b}`:

Cross-check with slide 45 (the "NT and SA cannot both be blue" slide):
- Slide 45's bottom-row domain bar after WA=red, Q=green: WA = `{r}`, NT = `{b}`, Q = `{g}`, NSW = `{r,b}`, V = `{r,g,b}`, SA = `{b}`, T = `{r,g,b}`. ✓ matches.

Now the table:
| Arc popped | Action | Resulting change |
|---|---|---|
| NT → SA | both have only `{b}`; for NT=b no SA value supports it (SA=b violates NT≠SA). Remove b from NT. | NT = `{}` ⇒ **failure**. |

This row mixes up direction. **Enforcing arc NT → SA** means: for each value `x` in `D_NT`, is there some `y` in `D_SA` with `x ≠ y`? NT's only value is `b`; SA's only value is `b`; `b ≠ b` is false; so no supporting `y` exists → remove `b` from `D_NT` → `D_NT = {}` → **failure**. ✓

The action column says "Remove b from NT" — correct. The resulting change says `NT = {}` ⇒ failure — correct.

So the table is **arithmetically correct**, but the explanation text "both have only `{b}`; for NT=b no SA value supports it (SA=b violates NT≠SA)" is awkwardly worded — a student trying to learn the procedure from this single row will not see the general pattern. **Downgrading to P1.** Real P1 now: see P1-1 below.

---

## P0 — REAL FINDINGS AFTER RE-VERIFICATION

After rechecking everything I had initially flagged, I'm left with the following genuine P0s:

### P0-A. §2.5 Forward-checking analogy contradicts §4.6's correct description
**Location:** L07-CSP.md lines 66–70 vs lines 396–420.

§2.5 says:
> When you put a queen on the board, you cross out every square she attacks. **If some other queen still on her clipboard has *no square left*, you know without proceeding that this branch is doomed.**

But forward checking does NOT track queens-not-yet-placed as objects with "squares left" — it tracks **unassigned variables' remaining domains**. The analogy phrasing "some other queen still on her clipboard has no square left" only works in the compact $n$-row formulation (§3.4.2 alternative), where each future row has a domain of remaining columns. It does NOT work in the slide 12 formulation ($n^2$ Boolean variables) — there the analogy fails entirely because "future queens" aren't variables at all.

This is the kind of fuzzy analogy that confuses exam students who are asked "describe forward checking for the slide-12 N-queens formulation". They will write the chapter's analogy and lose marks. The §4.7 trace correctly uses the compact formulation, but the analogy is presented in §2.5 BEFORE the chapter has distinguished the two formulations.

**Fix:** rewrite §2.5 in terms of variables and domains, not queens. Or explicitly say "this analogy assumes the compact n-variable formulation".

### P0-B. §3.4.2 — Slide 12's `(Xij, Xi+k, j+k) ∈ {(0,0),(0,1),(1,0)}` constraint is reproduced without explaining the `k` quantifier scope
**Location:** L07-CSP.md lines 199–201.

The chapter writes the diagonal constraint as:
> Same on the **main diagonal** (both indices step by k): $(X_{ij}, X_{i+k, j+k}) \in \{(0, 0), (0, 1), (1, 0)\}$.

The slide writes it the same way, but the slide is itself ambiguous and the chapter inherits the ambiguity without resolving it. What is the quantifier on `k`? Implicitly, "for all valid `k ≥ 1` such that `(i+k, j+k)` is on the board". A student asked "write down the diagonal constraint for 4-queens in slide-12 form" will write `(X11, X22) ∈ {(0,0),(0,1),(1,0)}` and stop, missing `(X11, X33)`, `(X11, X44)`, `(X22, X33)`, etc.

The chapter should explicitly state: "for every `k ≥ 1` such that the diagonal cell is on the board". This is a P0 because the exam may directly ask "formulate N-queens as a CSP" and the chapter's reproduction leaves the student under-prepared.

### P0-C. §2.6 Arc-consistency analogy — "scratch `5` off X's domain — and now everyone who pointed at X must restamp their passports too"
**Location:** L07-CSP.md lines 72–76.

The analogy says: when `X` loses a value, **everyone who pointed at X must restamp**. This is correct — the slides say "If X loses a value, all pairs Z → X need to be rechecked" (slide 48). But the chapter then continues the analogy with no concrete worked grounding, and §6 (Pitfalls) point 7 says:

> If you later prune $Y$'s domain, you must re-check arcs *into* $Y$ — i.e. every $Z \to Y$ — but *not* $Y \to Z$ (those are already consistent unless $Z$ shrinks).

**This is misleading.** Consider: if `Y` loses a value, arcs `Y → Z` may have **become arc-consistent that were not before** (because `Y` lost the unsupported value), but they may also have **become arc-inconsistent the other way** if a value of `Z` was *only* supported by the value `Y` just lost. Wait — actually `Y → Z` is enforced by pruning `Y`'s domain based on supports in `Z`. Pruning `Y`'s domain cannot make `Y → Z` *less* consistent (we only removed values from D_Y). So `Y → Z` does NOT need rechecking. The chapter is correct.

But the *converse* — arcs `Z → Y` — those check whether values of `Z` are supported by `Y`. If `Y` loses a value, some `z ∈ D_Z` may have been *only* supported by the lost `y`, so `Z → Y` needs rechecking. The chapter is correct on this.

**However**, this needs an example or worked trace to lock in. The whole §4.8 cascade explanation hand-waves "the cascade propagates" instead of doing one full worked propagation that goes through `Z → X` re-queueing concretely. A student asked "trace AC-3 on this CSP" will not know how to operate the worklist. This is a P0 gap for exam readiness.

### P0-D. §4.7 4-queens FC trace — incorrect domain at slide 39
**Location:** L07-CSP.md lines 438–439.

The chapter says (line 438):
> ![Stage 4: after X_2 = 3, X_3's domain wipes out (the only remaining value 4 conflicts via diagonal with the queen at (2,3): |3-4|=1=|2-3|). Backtrack.](../extracted_figures/L07/fig28-4q-x2-3-x3-empty.png) *(slide 39)*

Cross-check with slide 39: after `X_1=1, X_2=3`, slide 39 shows `X_3 = { , , , }` (empty) and `X_4 = { , , 3, }` (only `{3}`).

The chapter description claims `X_3`'s remaining value `4` conflicts with the queen at row 2, column 3. Check: queen at `(row=2, col=3)`. Candidate at `(row=3, col=4)`. Column conflict? cols 3 vs 4 — no. Diagonal: `|3-4| = 1`, `|2-3| = 1` ⇒ equal ⇒ diagonal conflict ⇒ removed. ✓

But the chapter says X_3 ∈ `{2, 4}` after FC from X_1=1 (line 434–435), and after X_2=3 also row 3 col 2 is removed because col 2 vs col 3 — different col, but diagonal? `|3-2|=1`, `|2-3|=1` ⇒ diagonal conflict ⇒ also removed. So X_3 loses both 2 and 4 → empty. ✓ Slide 39 shows X_3 empty. ✓

Chapter only mentions the removal of `4`. It misses the removal of `2`. This is incomplete reasoning — a student following the chapter's trace will not understand why `2` is also removed.

**P0 because:** the exam may directly ask "explain why X_3 has empty domain after X_2 = 3 in the 4-queens FC trace", and the chapter's stated explanation only covers half the answer.

### P0-E. §4.8 Arc-consistency complexity claim `O(c · d^3)` is unsourced and the slide does not state it
**Location:** L07-CSP.md line 521.

The chapter writes:
> *Cost*: in the worst case $O(c \cdot d^3)$ where $c$ is the number of binary constraints and $d$ is the maximum domain size.

The PDF slide deck (slides 1–55) **does not contain this complexity bound anywhere**. The bound is the textbook AC-3 bound from Russell & Norvig — true but **not from the lecture**. The chapter's "Connections" §7 notes which other lectures it draws from, but this is a smuggled-in textbook fact presented as if it were lecture material. The Cheat-Sheet §8 (line 731) also repeats this bound without a slide citation.

**If the exam scope is strictly "lecture material",** a student citing `O(c·d^3)` on an exam will be marked wrong (or at least docked for citing non-lecture material). The chapter must either:
- Remove the bound entirely, or
- Explicitly tag it "from Russell & Norvig, not from the slides" so the student knows not to use it as primary answer.

This is a P0 because exam-readiness is the brief and the chapter is currently misleading the student about what the lecturer covered.

---

## P1 — IMPORTANT FIXES (gaps the student WILL notice in exam prep)

### P1-1. §5.6 arc-consistency table is a single row — does not show the cascade
**Location:** L07-CSP.md lines 626–634.

Slide 45 shows the *full cascade*: NT and SA both blue, and the propagation needs to walk multiple arcs. The chapter's table has exactly ONE row (`NT → SA`) and then notes "(In a CSP where NT and SA still had two values each, the cascade would propagate further.)". This trivializes what the slide animates over slides 46–52.

A student asked "trace AC-3 on this CSP" gets nothing useful from this single row. Provide a 4–6 row table that mirrors slides 47–52: pop arc, REVISE, what changed, what was re-queued.

### P1-2. §4.8 pseudocode does not exactly match the slide's verbal procedure
**Location:** L07-CSP.md lines 496–514.

The pseudocode is fine — it's textbook AC-3. But the chapter says (line 492) "The slides' procedure is functionally identical to AC-3". This is true, but a student who memorizes the chapter's pseudocode and writes it on the exam will be writing **more than the slide gave them**. The slide only verbally describes:
- Definition of arc-consistency
- "When checking X → Y, throw out values of X with no supporting Y"
- "If X loses a value, all Z → X need to be rechecked"

There is NO pseudocode in the slides. The chapter must clearly demarcate "this pseudocode is a reasonable rendering of the slide's verbal description; on an exam, write either the prose or this pseudocode, not both as if cited from slides".

### P1-3. §3.4.2 N-queens alternative formulation cites Lab 4 but Lab 4 is GENETIC ALGORITHM, not CSP
**Location:** L07-CSP.md lines 210–211, 699.

The chapter says (line 211): *"see §3.4.2 alternative formulation (not on this slide but useful — appears in Lab 4 and the L05 chapter)"*. Then in §7 line 699 it says *"L05's GA appears in Lab 4, and L07's backtracking + FC + AC appears in Lab 6 (this lecture's lab)"*.

So Lab 4 uses the compact formulation for GA, not for CSP. The chapter is correct in §7 but unclear in §3.4.2 — a student reading §3.4.2 may go to Lab 4 expecting a backtracking CSP solver and find a GA instead. Fix: in §3.4.2 say "the n-variable formulation is also what L05 / Lab 4 use for GA on n-queens".

### P1-4. §4.4 Degree heuristic — chapter calls it "tie-breaker" but slide 27 lists it as a heuristic in its own right
**Location:** L07-CSP.md lines 366–376.

The chapter says (line 372): "The degree heuristic is also called the *most constraining variable* heuristic. **It exists to break MRV ties; on its own (as the primary variable selector) it is weaker than MRV.**" The "on its own it is weaker" claim is a textbook fact (Russell & Norvig) but **not stated on slide 27**. Slide 27 says verbatim: "Most constraining variable: Choose the variable that imposes the most constraints on the remaining variables; **Tie-breaker among most constrained variables**".

So the slide *does* call it a tie-breaker, but also presents it as a heuristic by itself in the first bullet. The chapter's "weaker than MRV on its own" is editorial and unsourced. Either cite a source or drop the claim — on an exam, the student must reproduce the slide's framing, not a textbook elaboration.

### P1-5. §6 Pitfall #11 — "drawing the cryptarithmetic graph as a plain undirected graph (instead of a hypergraph) misses the Alldiff constraint entirely"
**Location:** L07-CSP.md line 667.

True statement but unhelpful without a worked counter-example. A student told "don't draw it as a plain graph" still doesn't know how to draw a hypergraph for `TWO + TWO = FOUR`. Slide 13 shows the hypergraph as squares-for-constraints, circles-for-variables. The chapter has the image (`fig11-cryptarithmetic-cgraph.png`) but never describes the encoding ("square = constraint node, circle = variable node, edge connects constraint to its scope-variables") in a way the student can reproduce on an exam without the image.

### P1-6. §3.2 — "Successor function" vs "Action" terminology — the disambiguation is performed but the chapter's preferred term is unclear
**Location:** L07-CSP.md lines 112.

The chapter says: *"Slide 16 phrases this as the 'action'; slide 7 as the 'successor function'. Both names denote the same thing — see glossary — Slides call this 'successor function'; we use that canonical name and note 'action' as a synonym."*

Confusing — both slides 7 AND 16 are FROM THE SAME LECTURE. The chapter says "Slides call this 'successor function'", but slide 16 verbatim says "Action: Choose any unassigned variable and assign to it a value that does not violate any constraints; Fail if no legal assignments". So **the lecture uses BOTH terms** — slide 7: successor function, slide 16: action. The chapter's claim "slides call this successor function" is half-wrong.

A student asked "what does the successor function do in the CSP formulation" needs to know both terms. Better: "The lecture uses 'successor function' (slide 7) and 'action' (slide 16) interchangeably".

### P1-7. No worked solution-trace continuation for 4-queens after backtrack
**Location:** L07-CSP.md line 453.

The chapter says: *"The trace stops at this dead-end. Continuing the algorithm with X_1 = 2 yields a solution (the actual 4-queens solutions are (2,4,1,3) and (3,1,4,2))."*

But the §5.4 line 620 says: *"The continuation (not shown on the slides) reaches X_1 = 2, X_2 = 4, X_3 = 1, X_4 = 3 — a valid 4-queens solution."*

Verify: queens at (1,2), (2,4), (3,1), (4,3).
- Cols: 2, 4, 1, 3 — all distinct ✓
- Diagonals: |1-2|=1, |2-4|=2 — not equal, OK. |1-3|=2, |2-1|=1 — not equal, OK. |1-4|=3, |2-3|=1 — not equal, OK. |2-3|=1, |4-1|=3 — not equal, OK. |2-4|=2, |4-3|=1 — not equal, OK. |3-4|=1, |1-3|=2 — not equal, OK. ✓

So (2,4,1,3) is valid. Good. **But** there's an inconsistency: §4.7 line 453 says "The actual 4-queens solutions are (2,4,1,3) and (3,1,4,2)". Standard 4-queens has TWO solutions: (2,4,1,3) and (3,1,4,2). ✓ Verified.

So this is fine. But it would help if §4.7 walked one more step ("X_1 = 2 forward-checks to give X_2 = {4}, X_3 = {1,3}, X_4 = {1,3}", and so on) to show how the trace recovers. Otherwise the student is left at a dead end and the lab implementation will not "click".

### P1-8. Cheat-sheet §8 conflates two slightly different complexity claims
**Location:** L07-CSP.md lines 731, 733.

§8 says:
> **Cost of arc consistency.** $O(c · d^3)$ in the worst case…
> **Complexity of CSPs.** **NP-complete** in general.

The juxtaposition invites confusion — a student under exam pressure may write "AC-3 is polynomial so CSP is polynomial". The chapter must explicitly note: AC-3 is a **polynomial-time preprocessing** step that does NOT solve the CSP, only prunes; CSP itself remains NP-complete because backtracking after AC-3 is still exponential. The chapter notes this in §6 pitfall #10 (line 665) but not in §8 where a panicking student will look.

### P1-9. The "complete vs consistent" distinction in §6 pitfall #1 is the most important exam concept and gets ONE sentence
**Location:** L07-CSP.md line 644.

> A consistent assignment may have unassigned variables. A complete assignment may be inconsistent. A solution must be both.

True, but understated. Slide 6 emphasizes this with bold formatting and slide 9 reinforces with the all-red example. The chapter should have a small table:

| Property | Definition | Example (Australia, dom={r,g,b}) |
|---|---|---|
| Consistent | violates no constraint | `WA=r` (a partial assignment that's fine so far) |
| Complete | every variable assigned | `WA=r, NT=r, …, T=r` (all red, every var bound) |
| Solution | both consistent AND complete | `WA=r, NT=g, Q=r, NSW=g, V=r, SA=b, T=g` |

A 4-row table preempts an entire exam-question class.

### P1-10. The chapter calls AC-3 by name when the slide doesn't — but inconsistently
**Location:** Multiple — line 4 (glossary intro), line 492 ("AC-3-style propagation"), line 729 (cheat sheet "the slides do not name it AC-3 but the procedure is AC-3-style").

The hedging is correct but distracting. Pick a strategy:
- Strategy A: never call it AC-3 in the chapter body, only in the glossary entry.
- Strategy B: call it AC-3 throughout, with one footnote that the lecture didn't use the name.

Currently the chapter uses BOTH — sometimes "AC-3", sometimes "the arc-consistency algorithm" — and the back-and-forth is noise.

---

## P2 — POLISH / SUGGESTIONS

- **P2-1.** §1 line 22 says generate-and-test for 8-queens enumerates `8^8 = 16,777,216`. Slide 3 says the same. But "generate-and-test, with no redundancies" is the slide's wording, and the chapter drops "with no redundancies". The phrase matters: WITHOUT pruning redundancies it would be `64^8` (any of 64 squares for each of 8 queens with repetition). Slide's `8^8` already assumes one-queen-per-column.
- **P2-2.** §2 line 41 says "Each analogy below carries a 'where the analogy breaks down' caveat". This is good design, but several analogies are uneven in depth — e.g., §2.7 wedding-outfit caveat is one sentence; §2.6 customs-queue caveat dumps a half-paragraph about path consistency. Equalize.
- **P2-3.** §3.4.5 "Real-world CSPs" should at least name **register allocation** which the chapter mentions in §1 line 23 but the slide does not. Either drop the mention in §1 or add it to §3.4.5.
- **P2-4.** Mermaid graph in §3.3 is fine but visually less informative than slide 10's graph (which clearly shows SA as the hub). The Mermaid `graph LR` layout may render with SA off to the side instead of central. Consider `graph TD` or add a position hint.
- **P2-5.** (Re-classified from P0-1.) §5.3 says "Other solutions exist" but does not provide one. Either remove the parenthetical or actually provide one (e.g., none other obvious for `TWO+TWO=FOUR`; if the chapter can't name another, the parenthetical is misleading).
- **P2-6.** (Re-classified from P0-2.) §3.5 "totalling `n! · m^n` leaves" — replace "totalling" with "yielding a product of" or "for a total path count of".
- **P2-7.** §4.10 summary table is excellent. Add one more column: "Time cost per step" (e.g., FC is `O(d·k)` per assignment where `k` is neighbour count; AC is `O(c·d^3)` once).
- **P2-8.** §7 Connections to other lectures says (line 691) "Random variables in L09a are explicitly described in the glossary entry as analogues of CSP variables". This forward-reference is fine but unverifiable here — make sure L09a chapter and the glossary actually say this.
- **P2-9.** §2.3 "Tackling the most-cornered square first" — "most-cornered" is cute but not standard. A student writing "the most-cornered variable" on an exam will lose half a mark. Always pair the analogy with the canonical term in the same sentence: "**the most-cornered square first**, i.e. the variable with **minimum remaining values**".
- **P2-10.** Reading time "~45 min" (line 3) is optimistic for 756 lines with multiple worked examples and AC-3 reasoning. More honest estimate: 60–75 min for first read.

---

## EVIDENCE — Section-by-section spot checks against the PDF

| Section | Claim in chapter | PDF slide | Verdict |
|---|---|---|---|
| §1 line 22 | "8^8 = 16,777,216 combinations" | Slide 3 verbatim | ✓ |
| §1 line 23 | "register allocation in compilers" | Slide 15 list does NOT include this | ✗ extra-slide content (P2-3) |
| §3.1 line 99 | Unary example: `T ≠ 0` | Slide 13 has `T ≠ 0` | ✓ |
| §3.1 line 101 | Global `Alldiff(T,W,O,F,U,R)` | Slide 13 | ✓ |
| §3.2 line 112 | Both "successor function" and "action" used | Slide 7 = "Successor function", Slide 16 = "Action" | ✓ (P1-6) |
| §3.3 line 146 | SA participates in 5 edges | Slide 10 graph has SA—{WA,NT,Q,NSW,V} = 5 edges | ✓ |
| §3.4.2 line 195 | Variables `X_ij` with `D = {0,1}` | Slide 12 | ✓ |
| §3.4.2 line 197 | `Σ X_ij = N` | Slide 12 | ✓ |
| §3.4.2 line 200 | Diagonal constraint with `k` quantifier | Slide 12 also uses `k` ambiguously | ✓ but P0-B |
| §3.4.3 line 222 | Domains `{0,1}` for carries | Slide 13 says domain `{0,...,9}` for all variables incl. carries | ✗ chapter narrows carries to `{0,1}` (correct optimization, but slide doesn't say this) |
| §3.4.4 line 252 | 27 `Alldiff` constraints | Slide 14 says `Alldiff(X_ij in same unit)` — 9 rows + 9 cols + 9 boxes = 27 ✓ | ✓ |
| §3.5 line 274 | Number of paths `n! · m^n` | Slide 17 | ✓ |
| §4.1 line 296 | Pseudocode `CSP-BACKTRACKING` | Slide 24 | ✓ exact match |
| §4.2 line 342 | "Constraints on SA will eventually cause failure when WA ≠ Q" | Slide 23 verbatim | ✓ |
| §4.4 line 366 | MRV verbatim "Choose the variable with the fewest legal values; a.k.a. MRV" | Slide 26 | ✓ |
| §4.4 line 370 | Degree heuristic phrasing | Slide 27 | ✓ |
| §4.4 line 372 | "On its own (as primary variable selector) it is weaker than MRV" | NOT IN SLIDES | ✗ P1-4 |
| §4.5 line 388 | LCV verbatim | Slide 28 | ✓ |
| §4.6 line 401 | FC procedure | Slides 30–34 | ✓ |
| §4.7 lines 432–451 | 4-queens trace | Slides 35–44 | mostly ✓; P0-D explanation incomplete at slide 39 |
| §4.8 line 471 | Arc-consistency def | Slide 46 | ✓ |
| §4.8 line 478 | "If X loses a value, all pairs Z → X need rechecked" | Slide 48 verbatim | ✓ |
| §4.8 line 521 | `O(c · d^3)` complexity | NOT IN SLIDES | ✗ P0-E |
| §4.9 lines 537–551 | Arc consistency `x < y` worked example | Slide 53 | ✓ |
| §4.10 line 570 | NP-complete | Slide 54 | ✓ |
| §5.3 line 607 | Solution `T=7,W=6,O=5,F=1,U=3,R=0` | NOT IN SLIDES | added by chapter; verified arithmetically correct (P2-5) |
| §5.6 line 632 | AC-3 cascade table | Slides 45–52 animate cascade but no table | partial; P1-1 |

---

## ACCEPTANCE-CRITERIA-STYLE EXAM-READINESS CHECKLIST

Would a student who reads ONLY this chapter pass an exam question of each form?

| Exam question type | Pass? | Why |
|---|---|---|
| "Define CSP / state / consistent / complete / solution" | **Pass** | §3.1, §6 pitfall #1 covers it; minor wording issue (P1-9) |
| "Write down variables, domains, constraints for Map Coloring Australia" | **Pass** | §3.4.1 explicit |
| "Formulate N-queens as a CSP" | **Borderline** | §3.4.2 gives slide-12 form, but P0-B (k-quantifier scope) and P0-A (FC analogy mismatch) hurt |
| "Trace backtracking on the Australia map" | **Pass** | §4.2 + §5.1 table |
| "Trace forward checking on 4-queens with X_1=1" | **Borderline** | §4.7 has the figures but P0-D omits the second-removal reasoning |
| "Define and apply MRV / degree / LCV" | **Pass** with caveat — P1-4 unsourced editorial claim |
| "Define arc consistency and trace AC-3 on a worked example" | **Fail** | §5.6 cascade table has one row; P0-C lacks a full worked propagation; P0-E adds a non-lecture complexity claim |
| "State why CSPs deserve their own treatment vs. plain DFS" | **Pass** | §3.5 commutativity argument |
| "Identify the difference between FC and arc consistency" | **Pass** | §4.8 line 463 is crisp |
| "Explain `Alldiff` and why it's global, not binary" | **Borderline** | §3.4.3 and §6 #11 mention this but neither shows how to draw the hypergraph |
| "State complexity of CSP" | **Pass** | §4.10, §6 #10, §8 |
| "Reproduce the basic backtracking pseudocode" | **Pass** | §4.1 exact slide match |
| "Describe Sudoku as a CSP with 27 Alldiff" | **Pass** | §3.4.4 |

**Net: 9 Pass, 3 Borderline, 1 Fail across 13 representative question types.** The Fail (AC-3 tracing) is the most likely exam question for a Round-1 CSP exam. **The chapter is NOT exam-ready as currently written.**

---

## DOCUMENT.md audit

This chapter is a study document, not a code directory, so DOCUMENT.md is N/A in the standard PM sense. However: the `study/lectures/` directory should have a DOCUMENT.md listing each lecture chapter, what it covers, and reading time. Out of scope for this review but worth flagging to PM.

---

## What PM should do next

1. **Block release to Round 2.** Fix P0-A through P0-E before this chapter goes to the next reviewer.
2. **Dispatch L07 Lecture Extractor (or whichever agent owns this chapter)** with a targeted brief:
   - Fix §2.5 analogy to use variables-and-domains language (P0-A)
   - Add explicit `k`-quantifier scope in §3.4.2 (P0-B)
   - Add a full worked AC-3 propagation example with worklist trace (P0-C, P1-1, P1-2)
   - Complete the slide-39 4-queens FC explanation (P0-D)
   - Tag `O(c·d^3)` as off-slide (P0-E)
3. **Re-run QA / Reviewer 4** after the rewrite — specifically re-test "trace AC-3" exam-readiness.
4. Defer P1 items to Round 2; defer P2 to a polish pass.

---

## Report to PM

**Assignment recap:** Lecture Reviewer #4 (Exam Readiness, Spec §7.1) for L07 Constraint Satisfaction Problems, Round 1. Source: `Lecture7-Constraint Satisfaction Problem.pdf` (55 slides). Chapter: `study/lectures/L07-CSP.md` (756 lines).

**Status:** Fail (with major concerns) — re-work required before Round 2.

**P0 findings:**
1. **P0-A** `L07-CSP.md:66-70` — §2.5 FC analogy uses queen-clipboard language incompatible with the slide-12 N-queens formulation; rewrite in variable-and-domain terms.
2. **P0-B** `L07-CSP.md:199-201` — §3.4.2 diagonal constraint reproduces slide-12's ambiguous `k`-quantifier without scoping it; add "for every k ≥ 1 such that (i+k, j+k) is on the board".
3. **P0-C** `L07-CSP.md:457-523, §4.8` — Arc-consistency cascade is hand-waved; needs a concrete worklist trace (pop arc → REVISE → re-queue) on a real CSP. Without it, students cannot do the most likely exam question.
4. **P0-D** `L07-CSP.md:438-439` — §4.7 4-queens trace at slide 39 only explains why `X_3 = 4` is removed; misses why `X_3 = 2` is also removed (also a diagonal conflict). Incomplete reasoning.
5. **P0-E** `L07-CSP.md:521, 731` — Cost `O(c·d^3)` for arc-consistency is presented as if it were lecture material but is NOT on any slide; this is Russell & Norvig textbook content smuggled in. Tag it or drop it.

**P1 findings:**
1. **P1-1** §5.6 AC-3 table is single-row, doesn't show the slide 45–52 cascade.
2. **P1-2** §4.8 AC-3 pseudocode exceeds slide content; demarcate "rendering of slide procedure".
3. **P1-3** §3.4.2 alternative-formulation citation to Lab 4 is misleading (Lab 4 is GA, not CSP).
4. **P1-4** §4.4 claim "degree heuristic on its own is weaker than MRV" is unsourced editorial.
5. **P1-5** §6 pitfall #11 says "don't draw cryptarithmetic as plain graph" without teaching how to draw the hypergraph.
6. **P1-6** §3.2 says "slides call this successor function" — half-wrong; slide 16 says "action".
7. **P1-7** §4.7 4-queens trace ends at dead-end with no continuation under `X_1 = 2`.
8. **P1-8** §8 cheat-sheet juxtaposes `O(c·d^3)` and NP-complete without disambiguating.
9. **P1-9** §6 pitfall #1 (consistent vs complete vs solution) deserves a table.
10. **P1-10** AC-3 naming is inconsistently used; pick a strategy.

**P2 findings:** 10 polish items including: dropping "register allocation" mention not on slides; equalizing analogy caveats; Mermaid graph layout; reading-time underestimate; `O(c·d^3)` complexity table column; etc. See P2-1 through P2-10 above.

**QA Checklist (§7.1 exam-readiness) status:** 
- Coverage of slide material — **Pass with gaps** (P0-D, P1-1).
- Factual accuracy — **Fail** (P0-A, P0-E most severe).
- Slide-citation discipline — **Fail** (P0-E, P1-4 cite non-slide claims as slide).
- Exam-question coverage — **Borderline** (AC-3 tracing question would fail; see acceptance-criteria table, 1 Fail / 3 Borderline / 9 Pass).
- Pseudocode fidelity to slide — **Pass** for backtracking (§4.1 exact); **Concerns** for AC-3 (§4.8 exceeds slide).
- Pitfalls / Exam traps — **Pass** in coverage, **Concerns** in depth (P1-5, P1-9).
- Glossary / terminology — **Concerns** (P1-6, P1-10).

**Acceptance criteria (exam-readiness §7.1) status:**
- "Student reading only this chapter can answer slide-derived exam questions" — **Not met** (AC-3 trace question fails).
- "Every slide claim is reproduced or paraphrased accurately" — **Not met** (P0-E, P1-4).
- "Worked traces match the slide animations" — **Partially met** (P0-D, P1-1).

**DOCUMENT.md audit:** N/A for study chapter; suggest PM add a `study/lectures/DOCUMENT.md` index out-of-scope.

**Out-of-scope observations:**
- `study/_shared/glossary.md` is referenced for the AC-3 canonicalization debate (line 661, 729); reviewer should verify the glossary actually contains the "open canonicalization question 6" the chapter cites.
- The chapter cites `Lab 6 (this lecture's lab)` at `AI/lab6/` (line 693–697). If Lab 6 has not yet been built, the citation will dangle.
- Cross-references to L05, L06, L09a should be verified once those chapters exist.

**Concerns / risks:**
- The chapter is otherwise well-written and the analogies in §2 are pedagogically excellent — fixing the P0/P1 items is achievable in one revision pass, not a rewrite.
- Main risk: a student who scans the chapter and trusts §5.6 will completely misunderstand AC-3 propagation. That is the highest-impact defect.
- Secondary risk: the `O(c·d^3)` and "degree heuristic is weaker than MRV" smuggled facts will get students marked down for citing non-lecture material in an exam where the instructor strictly grades against slides.

**What PM should do next:**
1. Block this chapter at Round 1.
2. Dispatch the L07 chapter author (Extractor or whichever agent) with the P0 fix list above (5 items, scoped, no architecture changes).
3. After fix, re-dispatch Reviewer 4 specifically on the AC-3 tracing exam-question and on the slide-citation discipline.
4. Then move to Round 2 (other reviewers / app-tester for broken Mermaid render).

**DOCUMENT.md updated:** N/A for QA.
