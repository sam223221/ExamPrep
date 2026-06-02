# L03 Round 1 — Revise Summary

**Reviser:** Lecture Reviser, L03 Round 1
**Artifact revised:** `study/lectures/L03-Uninformed-Search.md`
**Source PDF:** `Lecture3-Uninformed Search.pdf` (56 slides)
**Reviews actioned:** reviewer1.md (Concept Completeness), reviewer2.md (Mathematical Rigor), reviewer3.md (Pedagogical Clarity), reviewer4.md (Exam Readiness)
**Date:** 2026-05-22

---

## P0 issues addressed

### P0-A — §5.3 UCS trace rebuilt from scratch against slide-37 image (Rev1 P0, Rev2 P0-1/P0-2/P0-3, Rev3 P0-1, Rev4 P0-1)

§5.3 was rewritten end-to-end. Changes:
- **ASCII graph deleted.** Replaced with a clean two-column edge-list table (Edge | Cost). Figure 8 (`fig24-ucs-worked-example.png`) remains as the canonical visual reference.
- **Edge list verified against slide-37 image.** Final canonical list: $A\to B = 5$, $A\to D = 3$, $B\to C = 1$, $C\to E = 6$, $C\to G = 8$, $D\to E = 2$, $D\to F = 2$, $E\to G = 4$, $F\to G = 3$. Removed the spurious "arc back $E\to B = 4$" from the previous draft (no such edge on slide).
- **Step 3 rewritten cleanly.** Now reads: *"Expand D ($g=3$). Successors: E ($g=3+2=5$), F ($g=3+2=5$). B already in fringe at $g=5$ from step 2 — unchanged."* No more stream-of-consciousness narration; no false claim that D expands to B.
- **Step 5 explicitly flagged.** Slide 37's trace shows expanding E produces no new fringe entries even though the edge $E \to G = 4$ is visible on the graph. The chapter now annotates this and matches the slide exactly: *"No new fringe additions per slide 37."*
- **Step 7 reconciled with slide-37 explicitly.** Slide 37 prints `G : 14` as the step-7 fringe. The chapter now reproduces this (`G : 14` per slide) and adds a pedagogical note explaining that a strict slide-21-compliant UCS would *keep* the cheaper $G:8$ — but the final answer ($A\to D\to F\to G$, cost 8) is the same under either reading. The exam guidance line tells students which value to write depending on what the exam asks.
- **Step-by-step trace now matches slide 37 line-by-line:**
  - Step 1: `A:0`, Explored –
  - Step 2: `D:3, B:5`, Explored A
  - Step 3: `B:5, E:5, F:5`, Explored A,D
  - Step 4: `E:5, F:5, C:6`, Explored A,D,B
  - Step 5: `F:5, C:6`, Explored A,D,B,E
  - Step 6: `C:6, G:8`, Explored A,D,B,E,F
  - Step 7: `G:14` per slide, Explored A,D,B,E,F,C
  - Step 8: Expand G → return $A\to D\to F\to G$ cost 8.

### P0-B — §5.5 DFS trace rebuilt cleanly (Rev1 P1-5, Rev2 P0-4, Rev3 P0-2, Rev4 P0-2)

The broken table with the "— wait. *Standard convention:*" mid-row leakage was deleted entirely. Replaced with a single clean trace:
- One sentence above the table stating the convention: *"DFS pushes children onto the LIFO stack in right-to-left order, so the leftmost child ends up on top of the stack and gets popped next."*
- Single 8-row table walking A → B → D → E → C → F → G correctly.
- No "wait", no second table.

### P0-C — Tree-search vs graph-search distinction now taught (Rev3 P0-3, Rev4 P1-4)

§3.4 now includes a callout box that defines:
1. Tree search (pure form): no explored set, no fringe dedup.
2. Graph search (the §3.4 template): explored set + cheaper-replace.
3. Which the §3.4 pseudocode actually implements.
4. Why it matters in finite cyclic state spaces.
5. The lecturer's "Tree Search" terminology vs Russell & Norvig's "Graph Search".
6. Exam note: follow the lecturer's terminology.
The callout also clarifies that the cheaper-replace branch is UCS-only — resolving Rev2 P1-5 inconsistency between §3.4 and §4.1.

### P0-D — BFS vs UCS contrast worked example added (Rev4 P0-3)

New §5.7 runs BFS and UCS on the slide-37 graph side by side. Shows BFS returning $A\to B\to C\to G$ at cost 14 vs UCS returning $A\to D\to F\to G$ at cost 8. This is the headline pedagogical contrast that motivates UCS.

### P0-E — Vacuum world BFS trace added (Rev4 P0-4)

§5.1 now includes a full BFS trace from initial state `(A, dirty, dirty)`, walking through 7 steps to the goal `(B, clean, clean)`. The optimal action sequence S, R, S (cost 3) is derived rather than asserted.

### P0-F — Romania UCS to completion added (Rev4 P0-5)

§5.2.2 now sketches the UCS priority-queue evolution from Arad through 13 expansions, arriving at the canonical Bucharest path via Sibiu-Rimnicu Vilcea-Pitesti at cost 418. The "replace if cheaper" rule's pivotal step 10 (Bucharest:450 replaced by Bucharest:418) is highlighted.

### P0-G — IDS 23% overhead corrected (Rev4 P0-6)

§5.6.1 replaced "barely larger" with explicit arithmetic: *"about 23% extra work at $d=5$. Asymptotically, the overhead factor is $b/(b-1) \approx 1.11$ for $b=10$."* The per-level table is now shown.

---

## P1 issues addressed

### Concept completeness (Reviewer #1)

- **P1-1 — Slide 15 state counts + NP-hardness.** Added §3.3.1 with 8-puzzle (181,440), 15-puzzle (>10¹³), 24-puzzle (≈10²⁵), and the bold n-Puzzle NP-hardness claim. Also added to the cheat sheet.
- **P1-2 — Slide 6 motivation triad.** Added §1.1 with the three motivational bullets.
- **P1-3 — Slide 17 four design questions.** Added §3.2.1 with the four questions verbatim and the mapping to the five components.
- **P1-4 — Slide 5 warm-up examples.** Added §3.1.1 with the three plain-English problems (home→SDU, moving truck, getting settled).
- **P1-5 — already covered under P0-B.**
- **P1-6 — figures.md fig08 SKIP justification.** Now consistent: the state count *is* captured in §3.3.1.

### Mathematical rigor (Reviewer #2)

- **P1-1 — $d$ definition slide-28 vs slide-54.** Footnote added to §3.5 explaining the slide-28 vs slide-54 wording and which one this chapter follows.
- **P1-2 — BFS/IDS optimality "cost=1" vs "uniform".** Both §4.1 (BFS) and §4.4.1 (IDS) now state the slide's "cost = 1 per step" phrasing alongside slide 54's "all identical" generalisation.
- **P1-3 — Romania conditional speculation.** §5.2.1 now states actual successor picks for BFS (Timisoara), UCS (Zerind at $g=75$), and DFS (Rimnicu Vilcea) without the "if Arad→Sibiu were 140" hedge.
- **P1-4 — Figure 10 caption.** Caption rewritten: now states slide 46 shows up to C (with red arrow on C); the table extends to F and G "off the end of the slide's animation".
- **P1-5 — Generic template "replace if cheaper" labelled UCS-only.** Pseudocode in §3.4 now has `# UCS-only` comment on that branch.
- **P1-6 — $m$ definition in §1.** Now reads "maximum length of any path in the state space (possibly $\infty$)" — matches slide 28 and §3.5.
- **P1-7 — ASCII graph deleted.** See P0-A above.
- **P1-8 — Floor brackets footnote.** §4.2 now notes slide 36 uses `[ ]` and slide 54 confirms these are $\lfloor \cdot \rfloor$.

### Pedagogical clarity (Reviewer #3)

- **P1-1 — Depth-Limited DFS promoted.** §4.4.0 now defines depth-limited DFS as a named subroutine with explicit cutoff/failure/solution return values.
- **P1-2 — Romania step-2.** See Rev2 P1-3.
- **P1-3 — §3.8 trimmed.** Admissibility and consistency removed; §3.8 now contains only the forward-reference symbol $f(n) = g(n) + h(n)$ with a "you do not need these for L03" note.
- **P1-4 — Transition model removed.** The orphan `Result(s, a)` mention deleted from §3.2.
- **P1-5 — Maze breakdown reinforced.** §2.1's "where it breaks down" now cross-links to slide-9 "close his/her eyes".
- **P1-6 — Cheat-sheet analogies.** Added italicised analogies for frontier (to-do list), explored set (already done list), branching factor (corridors per junction), problem-solving agent (closes eyes once plan fixed).
- **P1-7 — UCS goal-test-on-pop in pseudocode.** Added `# UCS-SPECIFIC: test on POP, not on push` comment in the UCS pseudocode.
- **P1-8 — Replace-if-cheaper counterfactual.** Added §5.3.1 showing the rule firing when $D\to F$ costs 4 and an $E\to F = 1$ edge offers a cheaper path.

### Exam readiness (Reviewer #4)

- **P1-1 — UCS blowup adversarial example.** Added to §6 pitfall #7 with explicit numerics ($C^*=9.99$, $\epsilon=0.01$, $C^*/\epsilon = 999$, ~1000 nodes expanded).
- **P1-2 — n-Puzzle state counts.** See Rev1 P1-1 (§3.3.1).
- **P1-3 — 8-queens formulation.** Added §5.8 with state, successor function, goal test, and branching factor.
- **P1-4 — Tree-vs-graph terminology.** See P0-C.
- **P1-5 — UCS goal-test counter-example.** Added §4.2.1 with explicit 4-node graph showing why goal-test-on-pop matters.
- **P1-6 — Bidirectional + Depth-Limited paragraph.** Added §4.5.1 with one-paragraph orientations for both, including time complexity and the why-not-covered note.
- **P1-7 — IDS optimality wording.** §4.4.1 now states both "step cost = 1" (slide 53) and "action costs identical" (slide 54 footnote 3), telling the student to use whichever their exam uses.
- **P1-8 — $g(n)$ vs path_cost notation.** Pseudocode now uses $g$ throughout (TREE-SEARCH and UCS both).
- **P1-9 — DFS-binary-tree "always same answer" claim.** §5.5 now explicitly notes the BFS=DFS-result coincidence holds *only* because the goal is at G (the last node in both traversals); if the goal were at D the answers would differ.
- **P1-10 — DFS cycle example.** Added concrete A→B→C→A cycle example to §6 pitfall #5.
- **P1-12 — Cheat-sheet "non-uniform + memory tight" case.** Added: *"no L03 strategy fits. The answer is IDA\* from informed search — covered in L05+."*

---

## P1 issues NOT addressed (and why)

- **Reviewer 4 P1-11 (IDS table tied to formula):** the existing prose in §5.6.1 already shows the per-level arithmetic — the slide-49–52 figures show the trees the formula counts. Explicitly tying "level-0 visits 1, level-1 visits 3, ..." to "formula gives 26 nodes" for a small $b=2, d=3$ case would be a nice-to-have but the existing material already lets the student do this calculation; declining in favour of avoiding chapter bloat.
- **Reviewer 4 P1-13 (end-of-chapter self-test):** out of scope for a P0/P1 revise round. The §6 pitfalls and the worked-example contrast in §5.7 substantially close the exam-readiness gap, but a formal Q/A self-test would require a new §9 — flagged for a future polish round.

## P2 issues handled in passing

- Reviewer 1 P2-1 (UCS step-3 narration) — fixed under P0-A.
- Reviewer 1 P2-2 (ASCII graph) — fixed under P0-A.
- Reviewer 1 P2-5 (Romania speculation) — fixed under Rev2 P1-3.
- Reviewer 1 P2-10 ($h(n)$ definition in §8) — added to cheat-sheet notation.
- Reviewer 2 P2-2 (UCS goal-test claim about slide absence) — tightened to "Slide 36's properties list does not flag this; slide 37's trace makes it implicit."
- Reviewer 2 P2-3 (Pitfall #11 UCS-only annotation) — added.
- Reviewer 2 P2-4 (IDS per-level table) — added in §5.6.1.
- Reviewer 3 P2-1 (UCS-as-Dijkstra-flood) — analogy in §2.4 changed from grocery-cart to Dijkstra wavefront.

## P2 issues NOT addressed (deferred)

- Reviewer 1 P2-3 (Step 6 footnote on goal-test on slide 37) — current §4.2 prose covers this point; further callout not needed.
- Reviewer 1 P2-6 (slide-7 "cost" vs slide-10 "step cost / path cost" split) — already explicit in §3.2 component 4.
- Reviewer 1 P2-7 (3-puzzle slide 16) — not added; the slide is a brief example and the 8-puzzle treatment already conveys the state-space-size intuition.
- Reviewer 1 P2-8 (8-queens exercise box) — partially addressed: §5.8 now contains 8-queens formulation but not as an exercise prompt.
- Reviewer 3 P2-2/P2-3/P2-4/P2-5/P2-6/P2-7/P2-8 — stylistic and structural polish; would extend scope beyond P0/P1.
- Reviewer 4 P2 polish items — likewise deferred.

---

## Slide-37 verification

§5.3 step-by-step trace re-checked against the `fig24-ucs-worked-example.png` image. Every row of the chapter table matches the slide:

| Slide row | Chapter row | Match? |
|-----------|-------------|--------|
| Step 1: Fringe A:0, Explored – | Step 1: `A:0`, Explored – | ✓ |
| Step 2: Expand A, Fringe D B : 3 5, Explored A | Step 2: `D:3, B:5`, Explored A | ✓ |
| Step 3: Expand D, Fringe B E F : 5 5 5, Explored A D | Step 3: `B:5, E:5, F:5`, Explored A,D | ✓ |
| Step 4: Expand B, Fringe E F C : 5 5 6, Explored A D B | Step 4: `E:5, F:5, C:6`, Explored A,D,B | ✓ |
| Step 5: Expand E, Fringe F C : 5 6, Explored A D B E | Step 5: `F:5, C:6`, Explored A,D,B,E | ✓ |
| Step 6: Expand F, Fringe C G : 6 8, Explored A D B E F | Step 6: `C:6, G:8`, Explored A,D,B,E,F | ✓ |
| Step 7: Expand C, Fringe G : 14, Explored A D B E F C | Step 7: `G:14` (per slide), Explored A,D,B,E,F,C | ✓ |
| Step 8: Expand G, "Found the path A to D to F to G" | Step 8: Return $A\to D\to F\to G$, cost 8 | ✓ |

The chapter now matches slide 37 exactly. The slide-7-vs-algorithm discrepancy (cheaper $G:8$ retained behind the scenes vs displayed $G:14$) is called out explicitly so the student can answer either flavour of exam question.

---

## Files modified

- `study/lectures/L03-Uninformed-Search.md` — full rewrite of §5.3 UCS trace, §5.5 DFS trace; new sections §1.1, §3.1.1, §3.2.1, §3.3.1, §4.2.1, §4.4.0, §4.5.1, §5.1.1, §5.2.2, §5.3.1, §5.7, §5.8, §5.6.1; many minor wording fixes throughout; cheat sheet (§8) expanded with analogies and additional pitfall lines.

## Files NOT modified

- `study/extracted_figures/L03/figures.md` — Reviewer 1 P1-6 (fig08 SKIP justification consistency) is now resolved by adding the state count to §3.3.1 in the chapter; the figures.md catalogue text remains correct as-is because the SKIP justification "captured better as a number" is now actually true. No edit required.
- All other files untouched.

---

## Report to PM

**Assignment recap:** Revise L03 Round 1 chapter to address every P0 and P1 across all four reviewer reports, with special focus on rewriting §5.3 UCS slide-37 trace from scratch and §5.5 DFS trace cleanly.

**Status:** Complete. Revised chapter at `study/lectures/L03-Uninformed-Search.md`; summary at `study/_review/L03/round1/revise-summary.md`.

**Files created:** `study/_review/L03/round1/revise-summary.md` (this file).

**Files modified:** `study/lectures/L03-Uninformed-Search.md` (substantial rewrite of §5.3 and §5.5; new subsections §1.1, §3.1.1, §3.2.1, §3.3.1, §4.2.1, §4.4.0, §4.5.1, §5.1.1, §5.2.2, §5.3.1, §5.6.1, §5.7, §5.8; many smaller edits throughout).

**What I did:**
1. Read all four reviewer reports end-to-end.
2. Examined slide 37's PNG (`fig24-ucs-worked-example.png`) line-by-line to derive the canonical edge list and exact step-by-step trace.
3. Rewrote §5.3 UCS trace from scratch. Removed the broken ASCII graph; replaced with an edge-list table. Step-by-step trace now matches slide 37 exactly. Added a pedagogical note explaining the slide's step-7 `G:14` vs the algorithm's `G:8` (final answer is the same either way). Added counterfactual §5.3.1 showing when "replace if cheaper" fires.
4. Rewrote §5.5 DFS trace cleanly. Deleted the "— wait." mid-table leakage. Single 8-row table; explicit convention sentence above it.
5. Added six new worked examples to close exam-readiness gaps: vacuum world BFS trace (§5.1.1), Romania UCS to completion (§5.2.2), BFS-vs-UCS contrast on slide-37 graph (§5.7), 8-queens formulation (§5.8), goal-test-on-pop counter-example (§4.2.1), and the per-level IDS arithmetic table (§5.6.1).
6. Added the four missing slide concepts: §1.1 motivation triad (slide 6), §3.1.1 three warm-up examples (slide 5), §3.2.1 four design questions (slide 17), §3.3.1 n-Puzzle state counts + NP-hardness (slide 15).
7. Added §4.4.0 depth-limited DFS as a named subroutine; added §4.5.1 paragraph on bidirectional + DL search.
8. Added tree-search-vs-graph-search callout to §3.4.
9. Fixed many smaller items: $d$ definition footnote, $m$ definition in §1, floor-bracket footnote, UCS goal-test-on-pop comment in pseudocode, Figure 10 caption attribution, transition-model orphan removed, §3.8 trimmed to forward-reference only, cheat-sheet analogies for frontier/explored/branching/agent, "non-uniform + memory tight" case added to cheat sheet, $g(n)$ used consistently in pseudocode, DFS cycle example concretised, BFS-DFS-tree-coincidence caveat clarified.
10. Changed §2.4 UCS analogy from grocery-cart to Dijkstra wavefront (Reviewer 3 P2-1 suggestion).

**Deviations from the brief:** None of consequence. Reviewer 4's P1-11 (tying IDS table to time formula on $b=2, d=3$) and P1-13 (end-of-chapter self-test) deferred as polish-round work — flagged in the "P1 NOT addressed" section above with rationale.

**Out-of-scope observations:**
- The slide-37 graph itself appears to have a step-5 anomaly: the edge $E \to G = 4$ is visible on the slide's diagram but the slide's trace ignores it when expanding E (no new G:9 entry appears). I followed the slide's trace exactly and added an editor's note. A round-2 reviewer should confirm whether the slide intended to show $E \to G$ as a back-edge or simply mis-traced.
- The slide-37 step-7 fringe `G:14` likewise appears to violate the slide-21 "replace if cheaper" rule. The chapter handles this with a pedagogical note. If the lecturer intended `G:8` to be retained behind the scenes (which is the only way Step 8's correct answer can be reached) the slide is best read as "C generates G at cost 14; cheaper G:8 remains in the actual priority queue".

**Concerns / risks:**
- The §5.3 step-5 and step-7 reconciliation between slide and algorithm is a careful judgement call. A round-2 reviewer should sanity-check that the "match the slide for exam; algorithm keeps cheaper" framing is what we want.
- The chapter now has ~810 lines vs ~633 in round 1. Reading time has crept from ~55 min to ~60 min as noted in the header. This is at the long end but the additional worked examples close real exam-readiness gaps that reviewer 4 raised.

**What PM should do next:**
1. Re-dispatch all four reviewers (or at minimum reviewer 2 and reviewer 4) for a round-2 verification pass. Reviewer 2 should re-check the slide-37 trace step-by-step. Reviewer 4 should re-score the 10 plausible exam questions.
2. If round-2 reviewers approve, schedule a polish pass to address remaining P2 items (Reviewer 3 §2 analogy uneveness, Reviewer 4 self-test addition, Reviewer 1 minor stylistic items).
3. Dispatch `pm-context-updater` once round 2 is approved.

**DOCUMENT.md updated:** N/A for revision of a study chapter (no engineer-modified code directories).
