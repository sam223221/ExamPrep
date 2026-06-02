# L07 Round 1 — Reviewer #2 (Mathematical Rigor)

**Reviewer role:** Mathematical Rigor
**Chapter:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L07-CSP.md`
**Source PDF:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture7-Constraint Satisfaction Problem.pdf` (55 slides)

---

## VERDICT

**PASS WITH CONCERNS** — math is mostly right; the chapter is unusually careful (it computes the column-sum constraints in TWO+TWO=FOUR, verifies the 4-queens diagonal arithmetic, and explicitly disclaims the AC-3 naming). However, there is **one clear mathematical inaccuracy (scope of column-sum constraint, §3.4.3)**, **one mathematical claim that contradicts the slide for the n-queens slide-12 encoding**, and **several extrapolations beyond the slides that are presented without sufficient flagging** (AC-3 complexity bound, "Alternative formulation" pasted as if it were on slide 35–44, "implicit constant" hand-wave). Worth fixing before round 2 but not catastrophic.

---

## P0 FINDINGS

**None.** No outright false mathematics that would mislead a student on a graded exam. The TWO+TWO=FOUR worked example checks out, the 4-queens diagonal arithmetic checks out, the n!·m^n counting argument checks out, the arc-consistency x<y example checks out, and the n=7 Australian-map degree count for SA checks out.

---

## P1 FINDINGS

### P1-1. Wrong scope claim for the units-column cryptarithmetic constraint (§3.4.3)

**Location:** L07-CSP.md, lines 235–238 (chapter §3.4.3, the bullet list under "Cryptarithmetic showcases").

**Claim in chapter:**
> "**Mixed-arity constraints** (the column-sum constraints have scope 4: e.g. `O, R, X1` plus the implicit constant)."

**Problem:** Scope of a CSP constraint = the **set of variables** in its relation. The constant `10` is not a variable; it is a coefficient. So the units-column constraint `O + O = R + 10·X1` has scope **3** (`{O, R, X1}`), not 4. Calling a numerical coefficient an "implicit constant" *that adds to the scope* is a category error — it confuses arity of the relation with the number of distinct symbols.

Furthermore, the bullet picks the *one* column-sum constraint whose scope is 3 to illustrate "scope 4". The actual scope-4 column-sum constraints are `W + W + X1 = U + 10·X2` (scope `{W, X1, U, X2}`) and `T + T + X2 = O + 10·X3` (scope `{T, X2, O, X3}`). So the example is doubly wrong: wrong column AND wrong reasoning for why it's "scope 4".

**Suggested fix:** Rewrite as: "Mixed-arity constraints — the units-column constraint `O + O = R + 10·X1` has scope 3 (`{O, R, X1}`); the tens and hundreds columns have scope 4 (`{W, X1, U, X2}` and `{T, X2, O, X3}` respectively). The constant 10 is a coefficient, not a variable in the scope." Drop the "implicit constant" phrase.

### P1-2. Mathematical inaccuracy in the n-queens slide-12 binary "at most one" constraints (§3.4.2)

**Location:** L07-CSP.md, lines 197–201 (chapter §3.4.2, the slide-encoded formulation bullets).

**Claim in chapter:**
> "For each cell pair on the same **row** $i$: $(X_{ij}, X_{ik}) \in \{(0, 0), (0, 1), (1, 0)\}$ — at most one of them is 1."

**Problem:** This constraint, as written, must implicitly require $j \neq k$. The slide writes "$(X_{ij}, X_{ik})$" without that condition, and the chapter inherits the omission. Without $j \neq k$, the constraint applied to a single cell $X_{ij}$ paired with itself yields $(X_{ij}, X_{ij}) \in \{(0,0),(0,1),(1,0)\}$, which excludes $(1,1)$, i.e., forces $X_{ij} = 0$ — every queen-bearing cell is forbidden. Same issue for column / diagonal / anti-diagonal: the chapter's wording "indices step by $k$" (line 200) does not say $k \neq 0$.

This is a slide bug that the chapter faithfully reproduces. A rigorous review either flags the slide bug (best) or fixes it silently (acceptable). The chapter does neither: it transcribes the broken constraints and adds the gloss "at most one of them is 1" which only makes sense under the missing $j \neq k$ / $k \neq 0$ condition. A student answering an exam by quoting these constraints verbatim will be marked correct (matches slide) but is mathematically reproducing a malformed CSP.

**Suggested fix:** After each line, add the explicit "for $j \neq k$" / "for $k \neq 0$" qualifier. Better: add a sentence noting that the slide omits the index-distinctness condition and the chapter is making it explicit.

### P1-3. AC-3 complexity bound $O(c \cdot d^3)$ is asserted as fact but is NOT in the slides (§4.8, §8)

**Location:** L07-CSP.md, line 521 (§4.8 Properties bullet "Cost") and line 731 (Cheat-Sheet "Cost of arc consistency").

**Claim in chapter:**
> "*Cost*: in the worst case $O(c \cdot d^3)$ where $c$ is the number of binary constraints and $d$ is the maximum domain size."

**Problem:** The slides do **not** state any complexity bound for arc consistency. Slide 52 only says "Arc consistency detects failure earlier than forward checking" and "Can be run before or after each assignment". The cited bound is textbook-correct AC-3 (AIMA, Russell & Norvig), but the chapter presents it without a citation marker like "[textbook reference, not in slides]". This is the chapter's own additional content masquerading as derived-from-slides.

Additionally, the chapter is otherwise *scrupulous* about flagging slide-vs-textbook divergences — see line 492 ("the slide does not use the name 'AC-3'"). The complexity bound deserves the same disclaimer.

**Suggested fix:** Add a parenthetical: "(this bound is the textbook AC-3 worst case; the slide does not state a complexity.)" Same fix at line 731.

### P1-4. "Alternative formulation" for n-queens is asserted as the formulation used on slides 35–44, but the slides never write the constraints (§3.4.2, §4.7)

**Location:** L07-CSP.md, lines 211 ("The 4-queens forward-checking trace on slides 35–44 (see §5.5) uses this compact formulation"), and §4.7 line 424 ("the compact $n$-variable n-queens formulation").

**Claim in chapter:** Slides 35–44 use the compact formulation $X_i \in \{1, \dots, n\}$ with constraints $X_i \neq X_j$ and $|X_i - X_j| \neq |i - j|$.

**Problem:** Slides 35–44 show domains $X_i \in \{1,2,3,4\}$ but never write the constraints in either form. The compact formulation is inferred (correctly) from the figure semantics, but the chapter presents this as fact ("uses this compact formulation"). A reviewer cannot verify from the slides alone that the compact formulation is what's intended; it's a *reasonable* reading because the slide-12 formulation would need 16 variables and would not fit on the figure. But the chapter should hedge.

**Suggested fix:** Replace "uses this compact formulation" with "is best read as the compact formulation; the slide does not write the constraint set explicitly, but the variable count $X_1, \ldots, X_4$ with domains $\{1,2,3,4\}$ is incompatible with the 16-variable slide-12 encoding."

### P1-5. Imprecise wording in the n!·m^n derivation (§3.5)

**Location:** L07-CSP.md, line 275.

**Claim:**
> "If at level 1 we could pick any of $n$ variables and assign any of $m$ values, level 1 has $n \cdot m$ children, level 2 has $(n-1) \cdot m$, …, totalling $n! \cdot m^n$ leaves."

**Problem:** The phrasing "level 2 has $(n-1) \cdot m$" reads as "level 2 has $(n-1) m$ nodes total", which is false. What is meant is: "each node at level 1 has $(n-1) m$ children" (branching factor at depth 2). The product of branching factors over depths 1 through $n$ gives the leaf count: $\prod_{k=1}^{n}(n-k+1)m = n! \cdot m^n$. The conclusion is correct; the intermediate claim is mis-stated.

**Suggested fix:** Rewrite as: "the branching factor at depth $k$ is $(n - k + 1) \cdot m$, so the leaf count is $\prod_{k=1}^{n} (n-k+1) \cdot m = n! \cdot m^n$."

---

## P2 FINDINGS

### P2-1. REVISE pseudocode iterates D_X while mutating D_X (§4.8)

**Location:** L07-CSP.md, lines 507–513.

The `REVISE(X, Y)` pseudocode does `for each value x in D_X: ... remove x from D_X`. This is a code-correctness issue (iterator invalidation) rather than a math issue, but it would not run as written in most languages. The chapter is presenting pseudocode, so it's defensible; a one-line fix ("iterate over a snapshot of $D_X$") would harden it.

### P2-2. Carry-domain hand-wave for cryptarithmetic (§3.4.3)

**Location:** L07-CSP.md, line 222.

**Claim:** "Domains: $\{0, 1, 2, \dots, 9\}$ for letters; usually $\{0, 1\}$ for carries."

The slide says only "Domains: $\{0, 1, 2, \dots, 9\}$" — it does not narrow the carry domain. The chapter's narrowing to $\{0,1\}$ is *correct in fact* (carry between adjacent decimal columns can only be 0 or 1, since the maximum column sum is 9+9+1=19) but is a derivation, not a direct slide claim. A one-sentence justification would close the gap.

### P2-3. "Boolean satisfiability (SAT) is the canonical NP-complete CSP" claim (§6, pitfall 10)

**Location:** L07-CSP.md, line 665.

The claim is true (Cook–Levin), but it is asserted without proof or reference, and the slides do not mention SAT. Mild extrapolation. Either drop the SAT remark or cite "Cook–Levin, 1971".

### P2-4. Slide-source line for the FC table "step 3: V = blue" claim (§5.2)

**Location:** L07-CSP.md, lines 598–604.

The table is internally consistent with §4.6 and slides 30–34. Good. But the chapter writes "SA's domain after FC" — at step 1 it shows `{g, b}` (correct: SA loses red because WA=red is a neighbour); at step 2 (Q=g) it shows `{b}` (correct: SA loses green); at step 3 (V=b) `{}` (correct: SA loses blue). Internally clean. P2 only because slides 32–34 don't actually show SA's column reducing in this exact order; the slide animation shows full domain rows, and the order WA→Q→V matches slide 34's three-row state. Reader needs to be careful that the chapter's row order is WA, Q, V (skipping the assigned-but-unshown variables), not the same as the column-headed table on the slides. A one-line note would help.

### P2-5. Glossary lists "AC-3 (arc-consistency algorithm)" but slides don't (§ front matter, line 4)

The front-matter "Glossary terms introduced" line explicitly lists "AC-3 (arc-consistency algorithm)". The chapter later (§4.8, line 492) honestly disclaims that "the slide does not use the name 'AC-3'". These are mildly inconsistent: the glossary line implies AC-3 is introduced by this lecture. Rename the glossary term to "Arc-consistency algorithm (textbook name: AC-3)" or similar.

### P2-6. "Path cost is constant *and irrelevant*" (§6 pitfall 9)

**Location:** L07-CSP.md, line 663.

The chapter writes "Path cost is constant *and irrelevant* (slide 7) — every solution is at the same depth $n$". This is correct but the slide says only "constant cost per step". The "irrelevant" gloss is the chapter's own. Minor — accept as good pedagogy.

### P2-7. Optimisation claim about LCV's behaviour (§2.4, §4.5)

**Location:** L07-CSP.md, lines 64, 392–394.

The chapter says "LCV is greedy" and that "MRV picks *whether* a branch leads to a dead-end at all" (line 394). The second claim is upside-down: MRV picks the *variable*, not whether a branch is a dead end; LCV picks *which value*, and that's what affects whether a branch leads to a dead end vs. a quick success. Re-read line 394:

> "MRV picks *which* dead-end branches to encounter first; LCV picks *whether* a branch leads to a dead-end at all."

This is overstated. LCV does not *determine* whether a branch leads to a dead-end (the constraint structure does); it only affects the *order in which values are tried*. Reword to "MRV picks which dead-end branches we encounter first; LCV picks the value most likely to *avoid* a dead-end".

### P2-8. Arc consistency pseudocode missing "if D_X is empty: return failure" inside REVISE (§4.8)

The outer ARC-CONSISTENCY function checks `if D_X is empty: return failure` after REVISE returns true (line 502). This is correct — REVISE itself does not need to check. P2 only as a clarity nit: some textbook presentations make REVISE return a failure flag directly, others (like the chapter's) lift the check to the caller. Acceptable as-is.

---

## EVIDENCE

I cross-verified the following load-bearing mathematical claims by direct computation:

| Claim | Location | Verified |
|---|---|---|
| $8^8 = 16{,}777{,}216$ | chapter §3.4.2 / slide 3 | ✓ |
| $n! \cdot m^n$ leaves count formula | chapter §3.5 / slide 17–18 | ✓ (derivation, despite imprecise wording — P1-5) |
| TWO+TWO=FOUR with $T=7,W=6,O=5,F=1,U=3,R=0 \Rightarrow 765+765=1530$ | chapter §5.3 | ✓ all four column equations, Alldiff, and leading-zero constraints hold |
| 4-queens FC pruning after $X_1=1$: $X_2 \in \{3,4\}, X_3 \in \{2,4\}, X_4 \in \{2,3\}$ | chapter §4.7 / slide 37 | ✓ (column + diagonal arithmetic) |
| 4-queens FC stage 4: after $X_1=1, X_2=3$, $X_3 = \emptyset$ | chapter §4.7 / slide 39 | ✓ ($X_3=2$ diagonal with $(2,3)$; $X_3=4$ diagonal with $(2,3)$) |
| 4-queens FC stage 8: after $X_1=1, X_2=4, X_3=2$, $X_4 = \emptyset$ | chapter §4.7 / slide 43 | ✓ ($X_4=2$ same column as $X_3$; $X_4=3$ diagonal with $(3,2)$) |
| 4-queens solution $(2,4,1,3)$ valid | chapter §4.7, §5.4 | ✓ (all pairwise row-/column-/diagonal-distinct checks pass) |
| SA has degree 5 in Australia constraint graph | chapter §3.3, §4.4 | ✓ (neighbours: WA, NT, Q, NSW, V) |
| Tiny x<y AC example reduces to $D_x = \{1,2\}, D_y = \{2,3\}$ | chapter §4.9 / slide 53 | ✓ (both directions, plus the re-check of $x \to y$ after $y$ shrinks) |
| Arc consistency on §5.6 table: NT→SA with both = {b} wipes NT | chapter §5.6 | ✓ |
| Compact n-queens diagonal constraint $|X_i - X_j| \neq |i - j|$ | chapter §3.4.2 | ✓ (queens at $(i, X_i), (j, X_j)$ are on same diagonal iff row-diff = col-diff) |

Mis-verified or under-supported claims:

| Claim | Location | Issue |
|---|---|---|
| "the column-sum constraints have scope 4: e.g. O, R, X1 plus the implicit constant" | §3.4.3 line 237 | Wrong — scope of $O+O=R+10\cdot X_1$ is 3 (P1-1) |
| Slide-12 row constraint $(X_{ij}, X_{ik})$ "at most one of them is 1" | §3.4.2 lines 198–201 | Requires implicit $j \neq k$ / $k \neq 0$ qualifiers (P1-2) |
| AC-3 complexity $O(c \cdot d^3)$ | §4.8 line 521 / §8 line 731 | Not in slides (P1-3) |
| Compact formulation is "the formulation used on slides 35–44" | §3.4.2 line 211 | Inferred from figures; not explicitly stated on slides (P1-4) |
| "level 2 has $(n-1) \cdot m$" | §3.5 line 275 | Reads as count, not branching factor (P1-5) |

Slides re-read with attention to mathematical content: 3, 6, 7, 12, 13, 14, 17, 18, 24, 26–29, 35–44, 46–53, 54. All of the chapter's per-slide quotations are faithful.

---

## Report to PM

**Assignment recap:** L07 (Constraint Satisfaction Problems) Round 1, Reviewer #2 — Mathematical Rigor focus. Source `Lecture7-Constraint Satisfaction Problem.pdf` (55 slides). Chapter `study/lectures/L07-CSP.md`.

**Status:** Pass with concerns.

**P0 findings:** None.

**P1 findings:**
1. **`L07-CSP.md:235-238`** — Scope claim for units-column cryptarithmetic constraint is wrong (scope is 3, not 4; "implicit constant" is a category error).
2. **`L07-CSP.md:197-201`** — n-queens slide-12 binary constraints inherit a slide bug (missing $j \neq k$ / $k \neq 0$ qualifiers) without flagging.
3. **`L07-CSP.md:521, 731`** — AC-3 complexity bound $O(c \cdot d^3)$ presented as derived, but is not in the slides; needs a "textbook, not in slides" disclaimer consistent with §4.8 line 492 disclaimer about the name "AC-3".
4. **`L07-CSP.md:211, 424`** — "Compact formulation" claimed to be what slides 35–44 use; the slides only show domains, not constraints. Should hedge.
5. **`L07-CSP.md:275`** — Imprecise wording in the $n! \cdot m^n$ derivation conflates "nodes at level k" with "branching factor at depth k". Conclusion is right; derivation reads wrong.

**P2 findings:**
1. REVISE pseudocode iterates D_X while mutating it (§4.8).
2. Carry domain $\{0,1\}$ for cryptarithmetic added without justification (§3.4.3).
3. SAT NP-completeness cited without source (§6 pitfall 10).
4. FC table row ordering (§5.2) needs a note that columns are abbreviated relative to slide animation.
5. Glossary front-matter lists "AC-3" but §4.8 disclaims the name (line 4 vs. line 492 inconsistency).
6. "Path cost is constant *and irrelevant*" — the "irrelevant" gloss is the chapter's, not the slide's (§6 pitfall 9).
7. "LCV picks whether a branch leads to a dead-end at all" overstated (§4.5 line 394).
8. REVISE missing in-function empty-domain check (minor style; outer caller handles it).

**QA Checklist (§7) status:** N/A — this is a lecture-chapter review, not a feature-shipping QA. The "§7 QA Checklist" in the role brief refers to the standard PM Feature-Plan template, which does not apply to lecture-chapter reviews. Treating this section as the per-review math-rigor checklist:

- Per-slide claims traced to source: **Pass** (chapter cites slide numbers consistently)
- Equations and arithmetic correct: **Pass** with one wrong scope claim (P1-1)
- Pseudocode mathematically sound: **Pass** (REVISE has a minor style issue, P2-1, not a math issue)
- Worked examples (TWO+TWO=FOUR, 4-queens FC trace, x<y AC): **Pass** (all verified)
- Complexity claims sourced: **Fail** — AC-3 bound is added without disclaimer (P1-3)
- Definitions match slides (arc consistency, constraint, scope, etc.): **Pass** except scope-arity confusion in §3.4.3 (P1-1)

**Acceptance criteria (§1) status:** N/A — same reason. As mathematical-rigor acceptance criteria:
- Every mathematical statement matches the slides or is explicitly marked as extrapolation: **Not met** (P1-3, P1-4 are unmarked extrapolations)
- Arithmetic in worked examples checks: **Met**
- Constraint scopes / arities are correct: **Not met** (P1-1)

**DOCUMENT.md audit:** N/A for this review type.

**Out-of-scope observations:**
- The chapter is unusually pedagogically strong on analogies (§2) and exam pitfalls (§6). The pitfall list is the kind of section that genuinely helps students — keep this structure for L08+ chapters.
- The "Connections to Other Lectures" section (§7) is useful but cites lecture slide numbers from L03, L05, L06 — those references should be verified by Reviewer #3 (or whoever owns cross-lecture consistency), not by me.
- The DOCUMENT.md/glossary/Lab 6 cross-references are file paths I did not verify exist; that's outside math rigor.

**Concerns / risks:**
- The scope-arity confusion (P1-1) is the kind of mistake that a sharp examiner would catch in a hand-graded answer. Students copying from the chapter will get marked down. Fix before the chapter is published to students.
- The unmarked AC-3 complexity bound (P1-3) is harmless in isolation, but it sets a precedent: if later chapters import textbook material as "from the slides", students will overgeneralise and cite textbook facts on the exam expecting partial credit.
- No P0 — the chapter is broadly sound and I would not block on these issues, but I would expect a re-review after fixes.

**What PM should do next:** Send P1 findings to the Lecture Extractor (or whatever agent produced this chapter) for revision. The five P1s are small text edits, each <5 lines. After fix, dispatch Reviewer #2 again for spot-check on P1-1 and P1-3 specifically (those have the most exam impact). P2s can be batched with the next round; they don't need a re-review.

**DOCUMENT.md updated:** N/A for QA.
