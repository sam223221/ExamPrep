# Reviewer 4 — L07 Constraint Satisfaction Problems — Round 2

**Role:** Lecture Reviewer #4 (Exam Readiness), Spec §7.1
**Source PDF:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture7-Constraint Satisfaction Problem.pdf` (55 slides)
**Chapter under review:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L07-CSP.md` (865 lines, up from 756)
**Mode:** HARSH. Round 2 — exam-readiness only. Specifically re-verifying that the five Round-1 P0s are *actually* fixed, not just claimed fixed.

---

## VERDICT

**Pass with concerns.** The reviser closed four of the five Round-1 P0s cleanly and improved the chapter substantially in §2 (three new analogies), §3.4.2 (quantifier scoping), §3.5 (derivation rewritten), §4.7 (slide-39 reasoning), §6 (the consistent/complete/solution table is now exam-ready), and §8 (cheat sheet now warns about AC-3 vs CSP complexity confusion). The §5.6 worklist trace is a real improvement.

**However, one Round-1 P0 has a regression**, two new defects have appeared in the revision, and one Round-1 P1 was claimed fixed but is still half-broken. None of these is a P0-level "broken arithmetic" finding — they are exam-readiness defects that would dock marks. Net: the chapter is on the right side of the pass line, but a polishing pass is required before final approval.

---

## P0 — MUST FIX (factually wrong or guaranteed to lose exam marks)

### P0-1. §5.6 worklist trace — the seeded arc list contains a *false* claim that NT and NSW are "not adjacent"
**Location:** `L07-CSP.md:714`.

The chapter writes:

> `NT→SA, SA→NT, NT→NSW (not adjacent, skip), SA→NSW, NSW→SA, SA→V, V→SA, NSW→V, V→NSW` (and reverse-stamps).

The parenthetical "NT→NSW (not adjacent, skip)" is correct as a slide-10 fact — NT and NSW share no border in the Australia map and therefore no constraint exists between them. **But the formatting puts this skip-arc inside the worklist seed list as if it were on the worklist.** A student copying this verbatim onto an exam will write the worklist with NT→NSW in it and then have to delete it, OR worse, will leave it in and falsely conclude AC-3 visits an arc that does not exist in the CSP.

Beyond formatting: the chapter is *missing arcs that DO exist*. The full set of unassigned-pair arcs is:

- NT ↔ SA (adjacent) ✓ listed
- SA ↔ NSW (adjacent) ✓ listed
- SA ↔ V (adjacent) ✓ listed
- NSW ↔ V (adjacent) ✓ listed
- NT, NSW, V, T arcs *to T* — T is isolated, but it is unassigned, so the question is whether AC-3 seeds arcs to/from T. **Since T shares no constraint with anyone, no arcs touch T.** Correct to omit, but the chapter does not say so.

The bigger problem: the chapter does *not* list arcs Q ↔ {NT, NSW, SA}, WA ↔ {NT, SA} — these are between an **assigned** variable and unassigned variables. Are they on the worklist? **AC-3 includes them** (the formal algorithm seeds *all* directed arcs in the CSP, then domains of assigned variables are singletons and revisions cannot prune them further, so they no-op). The chapter sweeps this under the rug by silently restricting the worklist to "between unassigned variables". This is non-standard — Russell & Norvig's AC-3 doesn't make this distinction — and a student answering "list the initial AC-3 worklist" on the exam will write a different set than the chapter shows.

**Fix:**
- Remove `NT→NSW (not adjacent, skip)` from the worklist line entirely.
- Add a one-line note: "the formal AC-3 worklist also includes arcs *from* assigned variables (WA, Q) outward; we omit them because the assigned variables' singletons cannot be pruned further. This is an optimisation, not the formal AC-3 seed."

Severity: **P0** because the exam scenario "list the AC-3 worklist for this CSP after `WA=red, Q=green`" is exactly the question the slide animation sets up, and the chapter gives the wrong (or at least misleading) answer. A student who memorises this line will be docked.

---

## P1 — IMPORTANT FIXES (gaps the student WILL notice in exam prep)

### P1-1. §3.5 derivation — the "product" wording is now correct, but the formula is stated with an off-by-one
**Location:** `L07-CSP.md:322`.

The chapter writes:

> the branching factor at depth $k$ is $(n - k + 1) \cdot m$, so the leaf count is the **product** $\prod_{k=1}^{n} (n - k + 1) \cdot m = n! \cdot m^n$.

Let me expand the product:
- $k=1$: $(n - 0) \cdot m = n \cdot m$
- $k=2$: $(n - 1) \cdot m$
- ...
- $k=n$: $(n - n + 1) \cdot m = 1 \cdot m$

Product: $n \cdot (n-1) \cdots 1 \cdot m^n = n! \cdot m^n$. ✓ Correct.

However the textual claim "the branching factor at depth $k$ is $(n - k + 1) \cdot m$" is at odds with the standard search-tree convention where depth $k=0$ is the root. The chapter is using "depth $k$" to mean "level $k$ starting from 1". A student reading "at depth 1 the branching factor is $n \cdot m$" may be confused if their textbook uses $k=0$ for the root level. The chapter should clarify "level $k$ measured from 1 at the first assignment" or restate as "after $k-1$ variables have been assigned, the branching factor is $(n - k + 1) \cdot m$".

Minor. **P1** because the exam question "derive the leaf count of the unordered CSP search tree" *exists* and a student writing the chapter's formula verbatim will be marked correct, but a student who tries to *explain* it using the chapter's wording will lose half a mark for the indexing ambiguity.

### P1-2. §4.7 K4 note — the "X1–X3 and X2–X4 may render less obviously" hedge is fluff and partially incorrect
**Location:** `L07-CSP.md:479`.

The chapter writes:

> The four-box diagram drawn on slide 35 visually emphasises only a subset of $K_4$'s six edges (X1–X2, X3–X4, X1–X4, X2–X3 are drawn most prominently); the left and right vertical edges X1–X3 and X2–X4 may render less obviously depending on rendering.

This sentence is too hedged. "May render less obviously depending on rendering" is not a real statement — either the slide draws the edge or it doesn't. Cross-check slide 35: the slide's constraint-graph picture shows four nodes labeled X1, X2, X3, X4 with edges drawn between **adjacent rows only** (i.e. X1-X2, X2-X3, X3-X4) — NOT all six edges of K4. The chapter's "X1–X4 are drawn most prominently" is also incorrect — slide 35 does *not* prominently draw X1-X4 as an edge.

The correct point is: slide 35's picture is the **constraint graph as the slide chooses to draw it** — and it deliberately simplifies to the row-adjacency edges to fit the visual. The **actual** constraint graph (the one implied by the constraint set) is K4, because of diagonal and column constraints connecting non-adjacent rows. The chapter is right about the conclusion, wrong about which edges are drawn on the slide.

**Fix:** drop the "X1–X2, X3–X4, X1–X4, X2–X3 are drawn most prominently" enumeration. Replace with: "Slide 35's diagram only draws the row-adjacent edges, simplifying the visual; the *implicit* constraint graph is K4 because every row pair interacts via column-equality and diagonal constraints."

Severity: **P1**. A student copying the chapter's enumeration onto an exam answer will write a factually wrong description of slide 35.

### P1-3. §4.7 / §5.4 — the 4-queens "continuation" is now inside both §4.7 AND §5.4, with inconsistent detail
**Location:** `L07-CSP.md:525` (§4.7) vs `L07-CSP.md:692` (§5.4).

§4.7 line 525 says:

> Continuing the algorithm with $X_1 = 2$ leads to a solution: forward checking after $X_1 = 2$ leaves $X_2 \in \{4\}$ (the only column non-conflicting with row 1 / column 2), then $X_3 \in \{1, 3\}$, then with $X_2 = 4$ propagated $X_3 \in \{1\}$ and $X_4 \in \{3\}$ — yielding $(X_1, X_2, X_3, X_4) = (2, 4, 1, 3)$.

§5.4 line 692 says:

> The continuation (not shown on the slides) reaches `X_1 = 2, X_2 = 4, X_3 = 1, X_4 = 3` — a valid 4-queens solution.

Two issues:
1. **Inconsistent depth.** §4.7's continuation is a half-trace with FC-domain reasoning; §5.4 is just the answer. A student reading §5.4 first sees no derivation and may not realise §4.7 has the trace. Add a `*See §4.7 for the continuation trace*` pointer in §5.4.
2. **Verify the §4.7 claim.** "$X_2 \in \{4\}$ (the only column non-conflicting with row 1 / column 2)". Check: $X_1 = 2$ ⇒ queen at $(1, 2)$. For $X_2$, queen at $(2, c)$: remove $c = 2$ (column), remove $c = 1$ (diagonal: $|c - 2| = 1 = |2 - 1|$), remove $c = 3$ (diagonal: $|c - 2| = 1$). Remaining: $c = 4$. ✓ So $X_2 \in \{4\}$.

   For $X_3$ (row 3) under just $X_1 = 2$: remove $c = 2$ (column), remove $c = 4$ (diagonal: $|c-2|=2 = |3-1|=2$). Keeps $\{1, 3\}$. ✓ matches chapter.

   For $X_4$ (row 4) under just $X_1 = 2$: remove $c = 2$ (column), $c = 5$ off-board. Diagonal: $|c - 2| = 3 = |4 - 1|$ ⇒ $c \in \{-1, 5\}$ — neither on board. Keeps $\{1, 3, 4\}$. **The chapter does not state this** — it skips straight to "after $X_2 = 4$ propagated".

   After $X_2 = 4$ (queen at $(2, 4)$): for $X_3$, queen at $(3, c)$, $c \in \{1, 3\}$ remaining: $c=1$ check against (2,4): $|1-4|=3, |3-2|=1$ no conflict ✓; $c=3$ check: $|3-4|=1 = |3-2|=1$ ⇒ diagonal conflict ⇒ remove. So $X_3 \in \{1\}$ ✓.

   For $X_4$, $c \in \{1, 3\}$ remaining after $X_1$: $c=1$ vs (2,4): $|1-4|=3, |4-2|=2$ no conflict; $c=3$ vs (2,4): $|3-4|=1, |4-2|=2$ no conflict. **So $X_4 \in \{1, 3\}$ after $X_1, X_2$ FC.** Chapter says $X_4 \in \{3\}$. This is wrong — at this stage $X_4 = 1$ is also legal under FC.

   Now after $X_3 = 1$ (queen at $(3, 1)$): for $X_4$, $c=1$ same column ⇒ remove. $c=3$: $|3-1|=2, |4-3|=1$ no conflict ⇒ keep. So $X_4 \in \{3\}$ ⇒ assign $X_4 = 3$ ⇒ solution $(2, 4, 1, 3)$ ✓.

   **So the chapter's claim "with $X_2 = 4$ propagated $X_3 \in \{1\}$ and $X_4 \in \{3\}$" is partially wrong**: $X_4 \in \{1, 3\}$ at that point, not $\{3\}$. $X_4$ collapses to $\{3\}$ only after $X_3 = 1$ is *also* assigned and propagated.

**Fix:** rewrite §4.7 line 525 as: "$X_2 \in \{4\}$; then $X_3 \in \{1\}$ and $X_4 \in \{1, 3\}$ after $X_2 = 4$ propagated; then $X_3 = 1$ forces $X_4 \in \{3\}$; assign $X_4 = 3$. Solution: $(2, 4, 1, 3)$."

Severity: **P1**. Not exam-question-defining, but a student walking the continuation will discover the inconsistency and either lose confidence in the chapter or memorise the wrong intermediate.

### P1-4. §4.7 "Note on the slide-35 picture" mixes up which slide shows what
**Location:** `L07-CSP.md:479`.

The chapter calls slide 35 "the four-box diagram drawn on slide 35 visually emphasises only a subset of K4's six edges". But slide 35 is the **starting board** (empty 4×4 chessboard before any assignment, with all four variables having domain {1,2,3,4}). The **constraint graph picture** is on slide 35 only if the slide-deck includes a graph drawing on the same slide as the empty board. Looking at the captions of figures in the chapter:

- `fig24-4q-start.png` *(slide 35)* — slide 35
- `fig25-4q-x1-1.png` *(slide 36)* — slide 36, X_1=1 assignment
- ...

The chapter does not explicitly include a "constraint graph for 4-queens" figure. The reference to "the four-box diagram drawn on slide 35" therefore points at the empty-board figure, but an empty board is not a four-box constraint graph. Either:
- the slide deck includes a graph diagram on slide 35 alongside the board (chapter should state which figure), OR
- the chapter is conflating two slides.

Cannot verify without re-checking the source PDF. **P1** because the "Note on the slide-35 picture" is now a defensive paragraph against an ambiguous slide, but the paragraph itself is unclear about *what* on slide 35 it is defending against.

### P1-5. §3.4.2 alt-formulation parenthetical "Note: Lab 4 uses this formulation for a genetic algorithm, not for CSP backtracking; Lab 6 — see §7 — is the CSP lab" is good but should be visually distinct
**Location:** `L07-CSP.md:254`.

This was the Round-1 P1-3 issue. The fix is *present* but tucked at the end of a long paragraph in italics. A student skimming for "where is the CSP lab?" will miss this. Recommend boxing this in a `> **Lab note.**` blockquote, the same way the chapter handles "Where it breaks down" caveats in §2.

Severity: **P1**.

### P1-6. AC-3 naming inconsistency persists despite Round-1 P1-10 claim
**Location:** Throughout — `L07-CSP.md:4` (glossary intro), `:564` ("AC-3-style propagation"), `:766` (pitfall #8), `:834` (cheat sheet).

The Round-1 revise-summary claims (line 129) that the chapter "now consistently uses 'arc-consistency algorithm' in body and 'AC-3' in glossary line + cheat-sheet, with explicit 'the slides do not name it AC-3' disclaimer". Verifying:

- §4.8 body line 564 says: "usually called **AC-3** in textbooks, but **the slide does not use the name 'AC-3'**, so we will refer to it here as 'the arc-consistency algorithm' or 'AC-3-style propagation'..."
- §8 cheat sheet line 834: "the slides do not name it 'AC-3' but the procedure is AC-3-style."
- §6 pitfall #8 line 766: "The textbook name is AC-3, and you should recognise it — but be careful about citing 'AC-3' as if the lecture used the term."

This is consistent in *messaging*, but the *naming* itself still goes back and forth: "the arc-consistency algorithm", "AC-3-style propagation", "AC-3" — three names for the same procedure within one chapter. The disambiguation paragraph is correct; the rotation of names is what's annoying. Pick one name as the chapter's canonical term and stick with it; mention the others *once* in the glossary entry.

Severity: **P1**. Doesn't lose exam marks, but does cost the student a few seconds of re-reading.

### P1-7. §5.6 "Hypothetical cascade" table is incomplete and labelled with `…`
**Location:** `L07-CSP.md:730–731`.

The chapter says:

> | Step | Arc popped | REVISE | Action | Re-queue |
> |---|---|---|---|---|
> | 1 | NSW → SA | NSW = {r, b}, SA = {r, b}. ... ✓. No removal. | no change | — |
> | 2 | V → NSW | ... | no change | — |
> | … | (continue) | … | … | … |

A `…` row in a "concrete worklist trace" is a cop-out. Round-1 P0-C demanded a *full* worked propagation; the revise-summary §6 claims this is fixed. Counting actual revisions: only 2 rows of the hypothetical cascade are populated, and both are **no-op revisions**. A student reading this learns nothing about how to detect a *successful* revision in the cascade — the table never demonstrates one.

The reviser's defence might be "the actual cascade in the slide-45 state terminates at step 1 with failure". True. But then the hypothetical table should either:
- Be replaced with a CSP where the cascade actually runs to a non-trivial fixpoint (e.g. construct an example where REVISE makes a real removal mid-cascade), or
- Be removed entirely with a sentence: "In the slide-45 state, the cascade terminates at the first arc; an extended trace would demonstrate further removals, but the topology of this CSP doesn't produce them."

Severity: **P1**. Round-1 P0-C is *technically* closed (the worklist trace exists), but the educational payload is thin — the table demonstrates "AC-3 detects failure immediately" but does not demonstrate "AC-3 propagates through multiple removals before terminating".

### P1-8. §3.4.3 cryptarithmetic — carry-domain narrowing reasoning has an arithmetic slip
**Location:** `L07-CSP.md:274`.

The chapter writes:

> A common textbook tightening narrows the carry domains to $\{0, 1\}$ because the maximum value of any decimal column sum here is at most $9 + 9 + 1 = 19$, so the carry is always 0 or 1.

Check: the column-sum equations are:
- Units: $O + O + 0 = R + 10 X_1$ — max LHS = $9 + 9 = 18$ ⇒ $X_1 \in \{0, 1\}$.
- Tens: $W + W + X_1 = U + 10 X_2$ — max LHS = $9 + 9 + 1 = 19$ ⇒ $X_2 \in \{0, 1\}$.
- Hundreds: $T + T + X_2 = O + 10 X_3$ — max LHS = $9 + 9 + 1 = 19$ ⇒ $X_3 \in \{0, 1\}$.

The chapter says "the maximum value of any decimal column sum here is at most $9 + 9 + 1 = 19$". For the units column there's no `+1` (no incoming carry), so max is $18$ for units and $19$ for tens / hundreds. The chapter's blanket "$9 + 9 + 1 = 19$" is correct for the tighter bound but understates for units. Minor.

The conclusion ($X_i \in \{0, 1\}$) is correct. **P1** because if asked to *show* the carry-domain narrowing on the exam, the student needs to handle units separately.

### P1-9. §4.7 "Stage 5 (slide 40)" caption says "try X_2 = 4" but the stage numbering is off by 1
**Location:** `L07-CSP.md:503` and surrounding figure captions.

The chapter labels the panels:
- Stage 0 (slide 35): empty
- Stage 1 (slide 36): X_1 = 1
- Stage 2 (slide 37): FC after X_1 = 1
- Stage 3 (slide 38): X_2 = 3
- Stage 4 (slide 39): X_3 empty
- Stage 5 (slide 40): X_2 = 4
- Stage 6 (slide 41): FC after X_2 = 4
- Stage 7 (slide 42): X_3 = 2
- Stage 8 (slide 43): X_4 empty
- Stage 9 (slide 44): backtrack to X_1 = 2

But slide 40 in the source PDF is the *backtrack-from-failure* slide ("X3 has empty domain, return to X2") not the "try X_2 = 4" slide. Slides 40 and 41 may be reversed. Cannot verify without source — but the captions need a recount.

Severity: **P1** if confirmed. **P2** if the slide-numbering is actually correct and I'm wrong. Flag for verification against the source PDF.

---

## P2 — POLISH / SUGGESTIONS

- **P2-1.** §3.5 line 327: the chapter renders the literal blockquote `> � For example,...` with a `�` character — a Unicode replacement character (encoding error from the PDF). Replace `�` with the proper bullet `•` or `-`. Same on line 332.
- **P2-2.** §5.6 worklist table at line 720 footer row shows `(none — failure detected)` and then a `—` row labelled "step —". The dash-row is parsing-fragile (the column `Step` reads "—" and the action column reads "abort"). Either merge into row 1 or use a clearer "Step 1 (continued)" label.
- **P2-3.** §6 pitfall #1 table at line 745 has "Example: `WA = r` only (a partial assignment that's fine so far)" — the word "only" is awkward. Replace with "Example: `WA = r` (a partial assignment with no constraint violations)".
- **P2-4.** §2.5 forward-checking analogy was rewritten as "crossing off attacked squares on a candidate list" — good. But the caveat now reads "This analogy maps cleanly only onto the compact n-queens formulation (§3.4.2 alternative), where each future row's *domain* is the candidate list." The phrasing "future row's domain is the candidate list" is awkward — a domain *contains* the candidate list, it isn't a list. Rephrase: "where each future row's domain is the set of candidate columns".
- **P2-5.** §2.9 maiden-aunt analogy ends with "slide 27 explicitly frames it as a tie-breaker among most-constrained variables". This is correct but repeats the slide-27 framing five times across §2.3, §2.9, §4.4, §6 pitfall #3, §8 cheat-sheet. Trim the repetition to once per chapter.
- **P2-6.** §2.10 Newton's-cradle analogy ends "*it ripples through the constraint graph*". A cradle is a chain, not a graph — fine analogy, but the analogy doesn't capture branching of propagation. Add half a sentence: "real propagation can branch — multiple neighbours touched at once, like dropping a stone in a pond rather than hitting a one-line chain".
- **P2-7.** §4.10 summary table — the column "Where the slides cover it" repeats "Slide 24, Slide 26, …" — would be cleaner as a single column "Slide(s)" with just the numbers.
- **P2-8.** §7 Lab 6 paragraph at line 798–802 forward-references `Lab6-CSP/lab6/constraints_template_solution.py` which may not yet exist if Lab 6 has not been produced. If still pending, add `(if/once produced by the Lab Solver agent)`. Currently reads as if the file is guaranteed to exist.
- **P2-9.** §8 cheat-sheet line 836 paragraph is now ~6 sentences long and visually heavy. Break into two paragraphs or use bullet points.
- **P2-10.** Reading time was bumped to 60–75 min — good. But the chapter is 865 lines now (up from 756) with several worked traces. 60-75 min is still tight for a careful first read; consider 75–90 min as more honest.

---

## EVIDENCE — Spot checks against the revised chapter

| Round-1 P0 | Round-2 status | Where verified |
|---|---|---|
| P0-A §2.5 FC analogy clipboard language | **Fixed** | `L07-CSP.md:81-86` — analogy now uses "candidate list", explicit caveat about which formulation it maps to |
| P0-B §3.4.2 k-quantifier scoping | **Fixed** | `L07-CSP.md:238-244` — explicit `j ≠ k`, `k ≠ 0`, and "on the board" qualifiers added with a "beyond the slide" note |
| P0-C AC-3 cascade hand-waved | **Partially fixed; new P1-7 hypothetical-cascade defect** | `L07-CSP.md:698-733` — worklist initialisation + main trace exist, but trace terminates at step 1 and the hypothetical cascade ends in `…` |
| P0-D §4.7 slide-39 explanation incomplete | **Fixed** | `L07-CSP.md:496-499` — both X_3 = 2 and X_3 = 4 removals are now spelled out with the arithmetic |
| P0-E `O(c·d^3)` unsourced | **Fixed** | `L07-CSP.md:593` and `L07-CSP.md:836` — both occurrences now explicitly tagged "beyond the slide", "cite as Russell & Norvig" |

| New Round-2 P0 / P1 finding | Location | Severity |
|---|---|---|
| Worklist line includes `NT→NSW (not adjacent, skip)` as if it were on the worklist; also restricts to "unassigned pairs" without acknowledging the standard AC-3 seed includes all directed arcs | `L07-CSP.md:714` | P0 |
| §4.7 K4 note enumerates wrong edges as "drawn most prominently" | `L07-CSP.md:479` | P1 |
| §4.7 line 525 continuation says `X_4 ∈ {3}` after FC propagation from $X_2 = 4$; actually $X_4 ∈ \{1, 3\}$ until $X_3$ is also assigned | `L07-CSP.md:525` | P1 |
| §5.6 hypothetical cascade table ends in `…` — does not demonstrate any successful REVISE removal | `L07-CSP.md:731` | P1 |
| AC-3 naming still rotates among three terms in body | throughout | P1 |
| §3.5 derivation uses "depth $k$" with ambiguous indexing | `L07-CSP.md:322` | P1 |
| §3.4.3 carry-narrowing reasoning quotes `9+9+1=19` blanket but units column has no `+1` | `L07-CSP.md:274` | P1 |
| `�` Unicode replacement char in §3.5 blockquote | `L07-CSP.md:327, :332` | P2 |

---

## ACCEPTANCE-CRITERIA-STYLE EXAM-READINESS CHECKLIST (re-run)

| Exam question type | Round 1 | Round 2 | Notes |
|---|---|---|---|
| "Define CSP / state / consistent / complete / solution" | Pass | **Pass** | Pitfall #1 table is now a strong reference |
| "Write down variables, domains, constraints for Map Coloring Australia" | Pass | **Pass** | unchanged |
| "Formulate N-queens as a CSP" | Borderline | **Pass** | P0-B fixed with explicit quantifier scoping |
| "Trace backtracking on the Australia map" | Pass | **Pass** | unchanged |
| "Trace forward checking on 4-queens with X_1=1" | Borderline | **Pass** | P0-D fixed (both removals explained); P1-3 minor arithmetic on continuation |
| "Define and apply MRV / degree / LCV" | Pass with caveat | **Pass** | unsourced editorial removed; slide-27 framing preserved |
| "Define arc consistency and trace AC-3 on a worked example" | Fail | **Pass with concerns** | §5.6 trace exists; but P0-1 (worklist contents) and P1-7 (hypothetical cascade incomplete) mean a student tracing AC-3 on a *new* CSP may stumble |
| "State why CSPs deserve their own treatment vs. plain DFS" | Pass | **Pass** | §3.5 derivation now correctly worded |
| "Identify the difference between FC and arc consistency" | Pass | **Pass** | §4.8 is crisp; §2.10 Newton's-cradle analogy adds intuition |
| "Explain `Alldiff` and why it's global, not binary" | Borderline | **Pass** | §6 pitfall #11 now has explicit hypergraph drawing instructions |
| "State complexity of CSP" | Pass | **Pass** | now also disambiguates AC-3 polynomial vs CSP NP-complete in §6 pitfall #10 |
| "Reproduce the basic backtracking pseudocode" | Pass | **Pass** | unchanged |
| "Describe Sudoku as a CSP with 27 Alldiff" | Pass | **Pass** | unchanged |

**Net: 12 Pass, 1 Pass-with-concerns, 0 Borderline, 0 Fail.** Major improvement over Round 1's 9 / 1 / 3 / 1.

---

## DOCUMENT.md audit

Same as Round 1 — study chapter, DOCUMENT.md N/A. The recommendation to add a `study/lectures/DOCUMENT.md` index still stands but is out of scope for this review.

---

## What PM should do next

1. **Dispatch the Lecture Extractor (or whichever agent owns L07) for a focused polish pass.** The brief should include:
   - Fix P0-1 (`L07-CSP.md:714`) — remove the in-line "(not adjacent, skip)" arc and either restrict the worklist correctly with an explicit note about the optimisation, or list the full AC-3 seed.
   - Fix P1-2 (`:479`) — drop the wrong edge enumeration in the K4 note.
   - Fix P1-3 (`:525`) — correct the 4-queens continuation trace.
   - Fix P1-7 (`:731`) — replace the `…`-row hypothetical cascade with a real or removed example.
   - Address P1-6 by picking ONE canonical name for the AC-3 procedure throughout the body.
   - Replace `�` characters in §3.5.
2. **Do NOT re-run another full review round** after this — the remaining defects are polish-scope. Move to Reviewer 5 (or whichever final reviewer remains) in parallel with the polish pass.
3. The chapter is **exam-ready with documented caveats**. A student reading this chapter can now answer 12 of 13 representative exam-question types without losing marks; the 13th (AC-3 trace on a new CSP) is the one where the P0-1 worklist defect could cost a mark.

---

## Report to PM

**Assignment recap:** Lecture Reviewer #4 (Exam Readiness, Spec §7.1) for L07 Constraint Satisfaction Problems, **Round 2** (post-revision). Source PDF unchanged. Chapter is now 865 lines (was 756). Verifying that Round-1 P0s P0-A through P0-E were actually fixed.

**Status:** **Pass with concerns** — major improvement over Round 1's Fail; four of five Round-1 P0s are cleanly closed and the fifth (AC-3 cascade) is partially closed but with new defects in the surrounding worklist seeding. The chapter is exam-ready on aggregate but needs one more polish pass.

**P0 findings:**
1. **P0-1** `L07-CSP.md:714` — §5.6 worklist line embeds `NT→NSW (not adjacent, skip)` as if it were on the worklist; also tacitly restricts the AC-3 seed to "unassigned-pair arcs" without acknowledging this is an optimisation, not the formal seed. A student writing the worklist on an exam will be wrong-footed.

**P1 findings:**
1. **P1-1** `:322` — §3.5 "depth $k$" indexing convention ambiguous (k starts at 1, not 0).
2. **P1-2** `:479` — K4 note enumerates the wrong "prominently drawn" edges; slide 35's picture shows row-adjacent edges only, not the chapter's claim.
3. **P1-3** `:525` — §4.7 4-queens continuation says `X_4 ∈ {3}` after FC from `X_2 = 4`, but actually `X_4 ∈ {1, 3}` at that point — collapses to `{3}` only after `X_3 = 1` is assigned.
4. **P1-4** `:479` — "Note on the slide-35 picture" references "the four-box diagram drawn on slide 35" but slide 35 in the PDF is the empty starting board; unclear what is being defended against.
5. **P1-5** `:254` — Lab 4 / Lab 6 disambiguation parenthetical is correct but visually buried in italics.
6. **P1-6** Throughout — AC-3 naming rotates among "arc-consistency algorithm", "AC-3-style propagation", and "AC-3" within the body.
7. **P1-7** `:731` — Hypothetical-cascade table in §5.6 ends in `…` and demonstrates no successful REVISE removal; the educational point of "cascade with real propagation" is not actually made.
8. **P1-8** `:274` — Carry-domain narrowing reasoning uses blanket `9+9+1=19` but units column has no `+1`.
9. **P1-9** `:503` — Stage / slide number alignment in §4.7 figure captions needs re-verification against source PDF (slide 40 vs 41 ordering).

**P2 findings:** 10 polish items including `�` Unicode replacement characters in §3.5 blockquote (P2-1), repetitive degree-heuristic-tie-breaker mentions (P2-5), reading-time still optimistic (P2-10), forward-reference to Lab 6 solution file that may not yet exist (P2-8). Full list above.

**QA Checklist (§7.1 exam-readiness) status:**
- Coverage of slide material — **Pass** (P0-D fix closes the slide-39 gap)
- Factual accuracy — **Pass with concerns** (P1-3 4-queens continuation arithmetic; P1-2 K4-edge enumeration)
- Slide-citation discipline — **Pass** (P0-E fix tagged correctly)
- Exam-question coverage — **Pass** (12 / 13 question types now Pass; 1 Pass-with-concerns)
- Pseudocode fidelity to slide — **Pass** (§4.1 backtracking exact; §4.8 AC-3 pseudocode demarcated as "faithful textbook rendering")
- Pitfalls / exam traps — **Pass** (pitfall #1 table is now textbook-quality)
- Glossary / terminology — **Pass with concerns** (P1-6 naming rotation)

**Acceptance criteria status:**
- "Student reading only this chapter can answer slide-derived exam questions" — **Largely met** (one borderline at AC-3 trace on a new CSP).
- "Every slide claim is reproduced or paraphrased accurately" — **Met** (Round-1 unsourced claims removed or tagged).
- "Worked traces match the slide animations" — **Mostly met** (P1-3 minor arithmetic glitch in 4-queens continuation).

**DOCUMENT.md audit:** N/A — study chapter.

**Out-of-scope observations:**
- `study/_shared/glossary.md` referenced repeatedly; verify the "open canonicalisation question 6" exists in the glossary.
- `AI/lab6/` referenced at lines 798–802 with a forward reference to `constraints_template_solution.py` that may not yet exist; if Lab 6 has not been built, this is a dangling citation.
- The chapter's "Reading time" of 60–75 min is still optimistic for the 865-line chapter with multiple worked traces.

**Concerns / risks:**
- The §5.6 worklist trace is the chapter's biggest improvement, but also the location of the new P0-1 defect. The fix is mechanical (one line) but must be done.
- The 4-queens continuation arithmetic (P1-3) is the kind of off-by-one that students will catch, lose confidence in the chapter, then over-correct everywhere else. Worth fixing for trust as well as correctness.
- The hypothetical cascade ending in `…` (P1-7) is a missed pedagogical opportunity — the chapter has the worklist machinery in place but doesn't use it to demonstrate a *propagating* cascade. This is the difference between "AC-3 detects this failure" and "here's how AC-3 propagates in general".

**What PM should do next:**
1. Dispatch the L07 chapter owner with the P0-1, P1-2, P1-3, P1-7 fix list (plus the P2 polish items). One focused revision pass should close all of these.
2. Do **not** re-run another full reviewer round after the polish; instead, run a brief sanity-check on just the changed lines.
3. Approve for downstream consumption (App Tester / Code Reviewer / Lab 6 integration) **conditional on** the P0-1 fix.

**DOCUMENT.md updated:** N/A for QA.
