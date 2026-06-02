# L07 — Round 1 — Reviewer 3 (Pedagogical Clarity incl. Analogies)

**Scope:** Spec §7.1. Enforce §2 analogies (every concept needs an everyday analogy + breakdown caveat, cross-linked from §3). Be harsh.

**Source:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture7-Constraint Satisfaction Problem.pdf`
**Chapter:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L07-CSP.md`

---

## VERDICT

**FAIL (Revise & Resubmit).**

The chapter ships seven well-written analogies in §2, each with a breakdown caveat — that part of the deliverable is genuinely strong. But the spec demands **every concept** declared in the front-matter glossary line gets an analogy *and* a cross-link from the formal section. The chapter misses this on three named concepts (Consistent assignment, Degree heuristic, Constraint propagation) and silently drops the cross-link on three more (CSP/§2.1 never recalled from §3 or §4.1; Backtracking/§2.7 never recalled from §4.1; Sudoku/§2.1 never recalled from §3.4.4 — i.e. the section that *is* Sudoku). One analogy (§2.2's "maiden aunt") secretly does double duty as the degree-heuristic analogy, which the cheat-sheet (§8) confirms, but it does not get its own subsection, its breakdown caveat covers the wrong concept, and the cross-link from §4.4 to it is missing. Plus one accuracy bug in §2.5 ("clipboard" should be "board"). This is sloppy enforcement, not a missing-everything situation — but the spec is unambiguous and the gaps are real, so it cannot pass as-is.

---

## P0 — Blocking

### P0-1. §2 fails the "every concept gets an analogy" mandate — three concepts have no analogy at all

The chapter's own front-matter line (L4) enumerates the lecture's glossary terms: *CSP, Variable (CSP), Variable domain, Constraint, Constraint graph, **Consistent assignment**, Backtracking search (CSP), Minimum Remaining Values (MRV), **Degree heuristic**, Least Constraining Value (LCV), Forward checking, Arc consistency, **Constraint propagation**, AC-3.*

§2 ships analogies for: CSP (§2.1), constraint graph (§2.2), MRV (§2.3), LCV (§2.4), forward checking (§2.5), arc consistency (§2.6), backtracking (§2.7). The three terms bolded above are introduced as their own glossary entries but receive **no §2 analogy section, no breakdown caveat, no cross-link from §3/§4 to an analogy**:

1. **Consistent assignment** (L103, §3.1) — defined formally but never analogised. This is exam-trap #1 in §6 ("Confusing *consistent* with *complete*"), so its lack of intuition is the most embarrassing miss.
2. **Degree heuristic** (L368, §4.4) — has no dedicated §2.x subsection. The "maiden aunt who feuds with half the family" line is buried inside §2.2 (seating chart for constraint graph) and reused informally; the cheat-sheet at L723 literally writes "*Seat the maiden aunt first.*" as the degree-heuristic one-liner, proving the chapter knows the analogy exists — yet refuses to give it a numbered subsection with its own breakdown caveat.
3. **Constraint propagation** (L4, §4.6 paragraph at L465) — collapsed into §2.6 (arc consistency). But §4.6 introduces "constraint propagation" as a distinct concept superordinate to arc consistency ("the simplest form is arc consistency"), and the slide deck (slide 45) phrases it as a standalone idea. It deserves its own analogy or an explicit "we treat constraint propagation and arc consistency together because the slides present them as one mechanism — see §2.6".

**Suggested fix:** add §2.8 *Consistent assignment is like a Tetris board mid-game* (the partial state is fine so long as no current piece is overlapping; you can still lose later), §2.9 *Degree heuristic is like seating the maiden aunt first* (most-feared guest first; breakdown: she may also be irrelevant to most tables). Move the maiden-aunt sentence **out** of §2.2 so the seating-chart analogy belongs cleanly to the constraint graph. For constraint propagation, either add a §2.x for it or explicitly note in §2.6's prose that "this analogy also stands in for *constraint propagation* in general (§4.6) — arc consistency is its archetypal instance."

### P0-2. §2.1 (Sudoku) is never cross-linked back from §3 or §4 — orphan analogy

§2.1 sets up Sudoku as the introductory analogy for CSP as a whole and for backtracking specifically (it walks through "pick a square, try a value, erase, backtrack" — the literal backtracking algorithm verbatim, per L44). But:

- **§3.1** (Variable/Domain/Constraint) has a `*Recall the "seating chart" analogy from §2.2*` line at L105, but **no recall to §2.1**, even though §2.1 is the canonical analogy for the CSP-as-a-whole concept §3.1 is introducing.
- **§3.4.4** (Sudoku) at L244–256 talks about Sudoku formally without **once** referring the reader back to §2.1's Sudoku analogy. The same example appears twice with no thread connecting them; the reader who only reads §3 will not know §2.1 also opened with Sudoku.
- **§4.1** (backtracking search formal algorithm, L291–322) has **no recall** to §2.1's "erase and try the next value" framing — even though §2.1 *is* a verbal description of the pseudocode at L296–309.

The spec line "cross-linked from §3" is being violated here. The reader who skips §2 (because it's "the intuition section, I already know CSPs") will never encounter the Sudoku analogy at all.

**Suggested fix:** add an italic recall at the end of §3.1 (`*Recall §2.1: the Sudoku grid is the canonical CSP — variable = cell, domain = {1..9}, constraint = no duplicate in row/column/box.*`), at the end of §3.4.4 (`*Recall §2.1: the algorithm you intuited there — try a value, erase on conflict, backtrack — is exactly what §4.1 formalises.*`), and at the top of §4.1 (`*This is the Sudoku-pencil-marks loop of §2.1 written as pseudocode.*`).

### P0-3. §2.7 (outfit-trying for backtracking) is cross-linked from §4.2 (the *trace*) but **not** from §4.1 (the *definition*)

L344 has the recall: `*Recall §2.7: the wedding-outfit analogy. Plain backtracking only discovers the dead-end when it tries SA — it does not anticipate it.*` — good, but this sits in §4.2 (the map-coloring walk-through). The formal algorithm definition in §4.1 (L291–322) has no recall at all. Yet §2.7's whole breakdown caveat ("pure backtracking, by itself, is much weaker than the best CSP algorithms — it is the *baseline* on top of which all the §4 improvements stack") is **precisely the framing §4.1 needs** to set up §4.3–§4.8.

**Suggested fix:** add `*Recall §2.7: backtracking is shirt → trousers → shoes with backtrack-on-stuck. The pseudocode below is exactly that, recursively.*` after L309 (between the pseudocode block and the "It is depth-first search…" paragraph).

---

## P1 — Important

### P1-1. The "maiden aunt" analogy is in the wrong section and has no breakdown caveat

§2.2 (L48–52) is titled "The constraint graph is like a seating chart at a wedding" and is supposed to be the analogy for the **constraint graph** concept. It then says "the most-connected guest — the maiden aunt who feuds with half the family — is the one to seat first, because every later choice has to respect her constraints" — this sentence is **not about the constraint graph**. It is about the **degree heuristic** (variable selection by max constraints on unassigned neighbours). And §8 (cheat-sheet, L723) explicitly attaches "*Seat the maiden aunt first.*" to the degree-heuristic row, confirming the author intended this as the degree-heuristic analogy.

This creates three problems:

1. The §2.2 breakdown caveat (L52) talks about unary constraints and the binary-graph distinction — it does **not** caveat the degree-heuristic intuition. So the degree heuristic effectively ships **without** the mandatory "where it breaks down" caveat.
2. The cross-link rule is violated: §4.4 (degree heuristic at L368–376) does not contain a `*Recall §2.X…*` line because there is no §2.x for it to recall.
3. A future reviewer or editor will read §2.2 and assume the maiden-aunt clause is part of the constraint-graph analogy, not realising it is the degree-heuristic analogy in disguise.

**Suggested fix:** extract the maiden-aunt sentence into its own subsection (e.g. §2.9 or insert as new §2.3, renumbering the rest). Write a dedicated breakdown caveat for the degree heuristic: e.g. "*Where it breaks down:* the maiden aunt may have many feuds but also be irrelevant to the actual seating problem if those feuds are with guests who didn't come — degree counts edges, not their tightness. MRV (§2.3 / §4.4) breaks this tie correctly when domain sizes already differ."

### P1-2. §2.5 (forward checking analogy) contains an accuracy bug — "clipboard" should be "board"

L68: "If some other queen still on her clipboard has *no square left*, you know without proceeding that this branch is doomed."

A queen is not on a clipboard. The intended image is the chessboard — "if some other queen [still to be placed] on the board has no legal square left". As written, this is either (a) a typo for "board" or (b) a stretched metaphor where the queens are imagined as candidates on a clipboard being placed onto a board, which would be a fresh and unsignalled extension of the analogy. Either way the reader is confused at the exact moment the analogy is supposed to deliver clarity.

**Suggested fix:** change "her clipboard" to "the board" (or rephrase: "if some other queen still waiting to be placed has no legal square left on the board").

### P1-3. §2.6 (arc consistency = customs queue) abuses the analogy in a way that may mis-train intuition

L74: "If your X-passport claims value `5`, there must be at least one value in Y's domain that pairs legally with `5`. If not, you scratch `5` off X's domain — and now everyone who pointed at X must restamp their passports too…"

The customs / passport metaphor is creative but breaks down faster than the chapter admits:

1. A real customs queue stamps **the document**, not the **value claimed by the document**. The analogy mixes "a passenger has a passport" (variable has a domain) with "a passport claims a value" (value is being checked). The reader has to mentally do "values are passport-pages, not the passport itself".
2. "everyone who pointed at X must restamp their passports" — in arc consistency the rule is that arcs *into* X (i.e. `Z → X` for every neighbour Z) get re-queued, but the analogy says "everyone who pointed at X must restamp **their** passports", implying Z's domain is modified, not Z's relationship to X. This is precisely the directionality confusion §6 pitfall #7 (L658–659) is trying to prevent.

The breakdown caveat at L76 is about $k$-consistency, not about either of these confusions.

**Suggested fix:** expand the breakdown caveat to: "*Where it breaks down (analogy-level):* values are the 'claims' on a passport, not the passport itself; and a cascade re-stamp does not change Z's claim, only re-tests it — Z may lose values, but only via its own consistency check, not by edict of X."

### P1-4. §2.3 (MRV) breakdown caveat conflates "irrelevant variable" with the degree-heuristic fix in a misleading way

L58: "*Where it breaks down:* MRV ignores how *important* a variable is — it might pick a tightly constrained but irrelevant variable when assigning a 'central' variable would have helped more. The **degree heuristic** (§4.4) is the tie-breaker that fixes this."

Two problems:

1. The degree heuristic is **a tie-breaker** for MRV ties (i.e. when several variables have the same fewest-remaining-values count). It does **not** fix MRV's general "picked an irrelevant tightly-constrained variable" failure mode — when MRV unambiguously points to a tight-but-irrelevant variable, degree heuristic is not consulted. The chapter itself confirms this at §4.4 L372 ("It exists to break MRV ties; on its own (as the primary variable selector) it is weaker than MRV"), so the §2.3 caveat is internally inconsistent.
2. "Tightly constrained but irrelevant" is also not a real failure mode of MRV in practice — MRV is provably good on most CSPs. The caveat is overstating the problem to justify mentioning degree heuristic.

**Suggested fix:** replace with: "*Where it breaks down:* MRV is silent at the very start of the search when every domain is full — at that point all variables tie. The **degree heuristic** (§4.4) breaks this tie by picking the variable with the most unassigned neighbours, but it is *only* a tie-breaker, not a correction to MRV's selection logic."

### P1-5. §3.4.4 (Sudoku) does not invoke §2.1, despite §2.1 being a Sudoku analogy

(Already flagged under P0-2 as the most acute cross-link gap; restating here as a P1 because the fix is independent and small.) The section on Sudoku as a formal CSP at L244–256 mentions Sudoku in detail but has no italic recall to the §2.1 Sudoku analogy. A reader who jumped straight to §3 to find "the Sudoku CSP" will never know there is a perfectly-tuned analogy three sections earlier.

**Suggested fix:** add at L256 (or just below the figure caption at L248): `*Recall §2.1: the pencil-marks-and-erase loop you intuited there — pick a cell, try a value, erase on conflict, backtrack — is the §4.1 backtracking algorithm. Sudoku is the textbook CSP precisely because pure backtracking gives a surprisingly usable solver, even before any of the §4.4–§4.8 improvements.*`

### P1-6. The "Where the analogy breaks down" caveats are not visually distinct enough

Every §2.x analogy uses the convention `- *Where it breaks down:* …` as a bulleted line in italics. This works on close reading but blends into the body text on a skim. Given the chapter explicitly says (L40) "these limits matter, because a wrong analogy mis-trains intuition for the exam", the caveats deserve more visual weight — e.g. a `> **Caveat.** …` blockquote or a bolded "**Limit:**" lead-in. As-is, an exam-prepping student scanning §2 will absorb the analogy and skip the caveat in 4 of 7 cases.

**Suggested fix:** swap the bulleted-italic format for a blockquote: `> **Where it breaks down.** …`. Apply consistently to all seven existing §2 analogies plus any added under P0-1.

### P1-7. §8 (Cheat-Sheet) one-line analogies are inconsistent with §2 subheading titles

Cheat-sheet entries (L709–729) use these one-liners:

| §8 one-liner | §2 subheading |
|---|---|
| "Sudoku grid: cells, candidates, no-duplicate rules." | "CSP is like filling a Sudoku grid" |
| "Wedding seating chart with 'can't sit together' edges." | "The constraint graph is like a seating chart at a wedding" |
| "Outfit-trying: shirt, trousers, shoes, swap when stuck." | "Backtracking is like trying outfits before a wedding" |
| "Tackle the most-cornered Sudoku square." | "MRV is like tackling the most-cornered square first" |
| "Seat the maiden aunt first." | (no §2 subheading — see P1-1) |
| "Leave doors open." | "LCV is like leaving doors open" |
| "Mark off attacked squares; if a queen has nowhere to land, abandon ship." | "Forward checking is like marking off attacked squares as you place a queen" |
| "Customs queue with reciprocal stamps." | "Arc consistency is like a customs queue with reciprocal stamps" |

The mismatches are mostly cosmetic — but the cheat-sheet item for **degree heuristic** ("Seat the maiden aunt first") has no §2 home, confirming P1-1 from a second angle. The cheat-sheet is implicitly accusing §2 of having a missing subsection.

**Suggested fix:** once P1-1 is addressed (maiden aunt promoted to its own §2.x), update §8's row to point to it. Otherwise leave §8 unchanged — the one-liner format does not need to be verbatim from the §2 headings.

---

## P2 — Polish

### P2-1. §2 lacks a one-paragraph "how to read this section" preamble

L40 ("Before any formalism, build a mental model for each new idea. Each analogy below carries a 'where the analogy breaks down' caveat — these limits matter, because a wrong analogy mis-trains intuition for the exam.") is a good opening, but it does not tell the reader **which §3/§4 sections to revisit for each analogy**. A small table mapping `§2.x → §3.y / §4.z` would make the recall cross-links discoverable from the analogy side, not just from the formal side.

**Suggested fix:** add a small table at L41 mapping each §2.x to its §3/§4 home.

### P2-2. §2.4 (LCV) breakdown caveat ends inconclusively

L64: "For very tight problems (where every choice eventually fails), LCV may be wasted effort — you'll backtrack regardless of order."

This is correct, but "wasted effort" is vague. A more specific phrasing — e.g. "For over-constrained CSPs with no solution, LCV's overhead (per-value support counting) is paid on every node and yields nothing, since *every* branch is doomed and reordering them only changes which doomed branch is explored first." — would be sharper.

**Suggested fix:** tighten phrasing as above.

### P2-3. §2.5 (forward checking) breakdown caveat references §4.6 but the section is §4.7 by section numbering

L70 says "**Arc consistency** (§4.6) closes this gap." — but in the chapter as written, §4.6 is titled "Forward checking" (L396) and arc consistency is §4.8 (L457). The cross-reference is one section off (forward, in fact). Note: §4.7 is "Forward checking on 4-queens" so the cross-link off-by-one is real, not a typo for §4.7. Either re-number arc consistency to §4.6 (would conflict with FC) or fix the in-text reference to "§4.8".

**Suggested fix:** s/`(§4.6) closes this gap`/`(§4.8) closes this gap`/ in L70.

### P2-4. §2.3 (MRV) example is non-quantitative — gives a feel but no comparison

L56 describes the most-cornered Sudoku cell ("only `{3, 7}` are still legal"). It would be marginally more pedagogical to contrast with a non-cornered cell ("vs. a cell whose row/column/box have left `{1,2,4,5,6,8,9}` candidates — choosing the {3,7} cell yields a binary branch with ~50% failure rate, while choosing the 7-candidate cell yields a 7-ary branch with ~14% per-branch failure rate"). This is what makes MRV's "fail fast" pay off.

**Suggested fix:** add the contrast above.

### P2-5. §2.7 (outfit-trying) does not say *why* it is the analogy for backtracking *specifically* and not for, say, brute-force search

L78–80 describes outfit-trying, but the framing "swap the trousers for a different pair (backtrack one level). Only if no trousers work do you swap the shirt." is true of any DFS. What makes it backtracking specifically (vs. iterative deepening, vs. BFS) is the *recursion-stack* nature — you keep the chosen shirt while exploring trouser options. The analogy implies this but does not name it.

**Suggested fix:** add a sentence: "Notice that the *shirt* stays on while you cycle through trousers — backtracking holds onto the prefix of decisions, only undoing the most recent one when it fails. That last-in-first-out undo is what makes this DFS, not BFS."

### P2-6. §2.6 (customs queue) is the longest and most strained analogy — consider simplification

The customs/passport metaphor at L74 carries a lot of weight ("X-passport", "claims value 5", "scratch 5 off X's domain", "everyone who pointed at X must restamp their passports", "every arc certifies or some passport is fully blank"). It works, but it is harder to hold in working memory than the others. A more direct analogy — e.g. "arc consistency is like checking that every dance-partner pair can still find a song they both like; remove any partner who has run out of compatible songs, and re-check everyone they were previously paired with" — might land faster. This is a taste call; flagging for consideration.

**Suggested fix:** consider a tighter analogy, or split the passport explanation into two shorter sentences with an explicit "Now back to the formal definition" pivot.

### P2-7. §2.1 closes with "we cover it in §4.5" but §4.5 is LCV, not constraint propagation

L46: "That is **constraint propagation**, not backtracking; we cover it in §4.5. Real CSP solvers combine the two."

In the chapter as written, §4.5 is "Value ordering — Least Constraining Value (LCV)" (L378). Constraint propagation as a generalisation of FC is introduced at §4.6 (forward checking, L396) and §4.8 (arc consistency, L457). The §4.5 pointer is wrong.

**Suggested fix:** s/`we cover it in §4.5`/`we cover it in §4.6–§4.8`/ in L46.

---

## EVIDENCE

Direct quotations from the chapter and the corresponding spec violations.

**E1. Front-matter glossary line (L4):** the chapter declares these terms as the ones it introduces — they form the canonical concept list against which §2 must be audited.

> Glossary terms introduced: CSP, Variable (CSP), Variable domain, Constraint, Constraint graph, Consistent assignment, Backtracking search (CSP), Minimum Remaining Values (MRV), Degree heuristic, Least Constraining Value (LCV), Forward checking, Arc consistency, Constraint propagation, AC-3 (arc-consistency algorithm).

Of these, **Consistent assignment**, **Degree heuristic**, and **Constraint propagation** have no dedicated §2.x analogy section. (See P0-1.)

**E2. §2 contains exactly seven analogies** (L42–84): §2.1 Sudoku, §2.2 seating chart, §2.3 most-cornered square, §2.4 leaving doors open, §2.5 marking attacked squares, §2.6 customs queue, §2.7 trying outfits. Each has a `- *Where it breaks down:* …` bullet. None of the three concepts in E1 is among them. (P0-1.)

**E3. Cross-link audit** — `grep §2` over the chapter returns these recall lines:

- L105 (in §3.1): `Recall the "seating chart" analogy from §2.2` ✓
- L152 (in §3.3): `Recall the "seating chart" analogy in §2.2` ✓
- L344 (in §4.2): `Recall §2.7: the wedding-outfit analogy` ✓
- L364 (in §4.4): `Intuition (§2.3): pick the most-cornered square` ✓
- L386 (in §4.5): `Intuition (§2.4): leave doors open` ✓
- L420 (in §4.6): `Recall §2.5: place a queen, cross out attacked squares` ✓
- L523 (in §4.8): `Recall §2.6: arc consistency = customs queue` ✓

**Zero cross-links to §2.1** (Sudoku) from anywhere in §3 or §4 — including from §3.4.4 (the Sudoku formal example) and §4.1 (the backtracking algorithm definition). (P0-2, P0-3.)

**E4. The "maiden aunt" misplacement.** §2.2 body text (L50):

> Isolated guests (no edges) can be placed anywhere; the most-connected guest — the maiden aunt who feuds with half the family — is the one to seat first, because every later choice has to respect her constraints.

vs. §8 cheat-sheet (L723):

> **Degree heuristic.** Tie-breaker for MRV: among ties, pick the variable in the **most constraints on yet-unassigned neighbours**. [Slide 27.] *Seat the maiden aunt first.*

Same metaphor, two different conceptual homes, neither with a dedicated breakdown caveat for the degree heuristic. (P1-1.)

**E5. §2.5 typo** (L68):

> If some other queen still on her clipboard has *no square left*, you know without proceeding that this branch is doomed.

"Clipboard" should be "board" (or the metaphor needs an explicit setup that there is a clipboard of pending queens). (P1-2.)

**E6. Stale section pointers in §2.1 and §2.5:**

- L46: "*we cover it in §4.5*" — §4.5 is LCV in the actual chapter; constraint propagation is §4.6–§4.8. (P2-7.)
- L70: "**Arc consistency** (§4.6) closes this gap." — §4.6 is FC; AC is §4.8. (P2-3.)

**E7. §2.3 caveat self-contradiction.** §2.3 caveat (L58): "The **degree heuristic** (§4.4) is the tie-breaker that fixes this." vs. §4.4 body (L372): "It exists to break MRV ties; on its own (as the primary variable selector) it is weaker than MRV." The degree heuristic does not fix MRV's "irrelevant variable" failure mode — it is only consulted on ties. (P1-4.)

---

## PM REPORT

```
## Report to PM

**Assignment recap:** L07 (Constraint Satisfaction Problems) Round 1 — Reviewer 3 (Pedagogical Clarity incl. Analogies). Spec §7.1: enforce §2 analogies — every concept needs everyday analogy + breakdown caveat, cross-linked from §3.

**Status:** Fail — Revise & Resubmit. The seven analogies in §2 are well-written and each has a breakdown caveat, but the spec is violated on three concepts (Consistent assignment, Degree heuristic, Constraint propagation) that have no §2 section at all; on three cross-links (CSP→§2.1, Backtracking-def→§2.7, Sudoku-formal→§2.1) that are missing from §3/§4; and on the §2.2 "maiden aunt" line which is the degree-heuristic analogy in the wrong section with the wrong caveat. Plus accuracy fixes in §2.5 ("clipboard"), §2.1 ("§4.5"), §2.5 ("§4.6").

**P0 findings:**
1. §2 missing analogies for three named glossary concepts: **Consistent assignment**, **Degree heuristic**, **Constraint propagation** (lines 4 vs. 42–84). Add §2.8 / §2.9 with breakdown caveats; promote "maiden aunt" out of §2.2 into its own subsection.
2. §2.1 (Sudoku) is never cross-linked back from §3.1, §3.4.4, or §4.1 (lines 88–322). Add italic `*Recall §2.1…*` lines at L105, L256, and L309.
3. §2.7 (backtracking analogy) recalled at §4.2 (L344) but not at §4.1 — the formal-definition section (L291–322). Add recall at L309 between the pseudocode and the properties paragraph.

**P1 findings:**
1. "Maiden aunt" in §2.2 (L50) is the degree-heuristic analogy disguised inside the constraint-graph analogy — §8 cheat-sheet (L723) confirms it. Extract to its own §2.x with a degree-heuristic-specific breakdown caveat.
2. §2.5 accuracy bug (L68): "on her clipboard" should be "on the board".
3. §2.6 customs-queue analogy (L74) has directional-confusion potential that §6 pitfall #7 (L658) explicitly warns against. Expand the breakdown caveat at L76 accordingly.
4. §2.3 MRV breakdown caveat (L58) self-contradicts §4.4 body (L372) — degree heuristic is a tie-breaker, not a fix for MRV's general failure modes. Rewrite caveat.
5. §3.4.4 (Sudoku formal) does not recall §2.1 — see P0-2; flagged here independently because the §3.4.4 fix is small and isolated.
6. §2 breakdown caveats use bulleted-italic format that blends into body text. Promote to `> **Where it breaks down.** …` blockquote for visual weight.
7. §8 cheat-sheet (L723) attaches "Seat the maiden aunt first" to degree heuristic, exposing the §2 missing-subsection from a second angle. Will resolve automatically once P1-1 is fixed.

**P2 findings:**
1. §2 lacks an opening "§2.x → §3/§4 mapping" table for analogy-side discoverability of cross-links (L40).
2. §2.4 (LCV) breakdown caveat (L64) is vague; tighten to specify that LCV's overhead is paid even on doomed branches.
3. §2.5 caveat (L70) wrong pointer: "§4.6" should be "§4.8" — §4.6 is FC, AC is §4.8.
4. §2.3 (MRV) example (L56) is non-quantitative; consider adding a 2-candidate-vs-7-candidate contrast to make "fail fast" visible.
5. §2.7 (outfit-trying) does not flag that it's specifically DFS-with-stack (vs. BFS / iterative deepening) — add one sentence.
6. §2.6 (customs queue) is the longest and most strained analogy — consider a dance-partner alternative or split into shorter sentences with a pivot.
7. §2.1 caveat (L46) wrong pointer: "§4.5" (LCV) should be "§4.6–§4.8" (FC + AC are the constraint-propagation sections).

**QA Checklist (§7) status:** N/A — this review covers Spec §7.1 (pedagogical clarity / analogies), not the chapter-internal §7. The chapter's §7 (Connections to Other Lectures) was not in scope for this reviewer pass.

**Acceptance criteria (§1) status:** N/A — Reviewer 3 evaluates §2-analogy compliance, not the chapter's own §1 acceptance criteria.

**DOCUMENT.md audit:** N/A — this review changes no project files; no DOCUMENT.md update needed.

**Out-of-scope observations (worth a follow-up):**
- The chapter's §6 Common Pitfalls (L640–671) is excellent and pedagogically tight — its exam-trap framing is the right model for the missing breakdown caveats in §2 (see P0-1, P1-3).
- The §4.9 "Tiny worked example — arc consistency from scratch" (L525–555) is the clearest piece of pedagogy in the chapter; consider promoting a similar tiny worked example into §3.5 (where naive search size is discussed but never numerically illustrated for the Australia map).
- The mermaid graph at L130–142 is correct but does not reproduce the Australia outline that the embedded slide figure at L124 does — the chapter already has both, but a reader might wonder why. A short caption clarifying "the mermaid graph is a topological re-rendering of the slide figure above; T's isolation is visible in both" would help.

**Concerns / risks:**
- The chapter is *very long* (756 lines). The §2 analogy compliance issues are pedagogically real but localised — fixing them is ~30 lines of edits. Don't let the size of the chapter intimidate the fix list; the §3–§8 content is solid and should not be touched.
- The cheat-sheet (§8) is internally consistent with §2 *except* for the degree-heuristic row (L723). This is the single best diagnostic that §2 is missing a subsection — the fix has a built-in correctness check.
- "Spec §7.1" was referenced in the brief but no `spec*.md` file exists in the repo (verified by Glob over the project). I treated the spec as: (a) every concept in the chapter's front-matter glossary line (L4) needs a §2 analogy with breakdown caveat; (b) every analogy needs a cross-link from §3 (and ideally §4) back to it. If the actual Spec §7.1 is more lenient (e.g. only major concepts, not every glossary entry), some P0/P1 items may downgrade.

**What PM should do next:** dispatch the chapter author (or pm-frontend for lecture content) to apply the three P0 fixes — add the missing §2 subsections for Consistent assignment, Degree heuristic, and Constraint propagation; restore the §2.1 cross-links into §3.1 / §3.4.4 / §4.1; add the §2.7 recall at §4.1. Then apply the P1 typo / directional fixes (clipboard, customs caveat, MRV caveat). Then re-run Reviewer 3.

**DOCUMENT.md updated:** N/A for QA / Reviewer.
```
