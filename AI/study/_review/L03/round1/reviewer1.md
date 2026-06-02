# L03 Round 1 — Reviewer #1: Concept Completeness (incl. Figures)

**Scope of this review:** Cross-check `study/lectures/L03-Uninformed-Search.md` against `Lecture3-Uninformed Search.pdf` (56 slides) for missing concepts, definitions, formulas, topic-bullets. Audit `study/extracted_figures/L03/figures.md` — every USE/REWORK embedded, every SKIP justified, no informative figure missed silently. The lecture deliberately defers A\*/heuristics; the chapter is checked for **honesty about that gap**, not for delivering it.

---

## VERDICT

**NEEDS_REVISION**

The chapter is structurally strong, generously analogised, and the figures catalogue is conscientiously assembled. However, three substantive concept omissions from the source deck (slide 5 examples, slide 6 motivation triad, slide 15's state-count + NP-hardness facts, slide 17's four-question checklist) plus a self-admitted broken sentence in the DFS trace (§5.5 Step 2) push this below an APPROVED bar. None of the findings are P0 — there are no factual errors and the A\*-gap disclosure is honest and clear. But the missing items are nominally "topic-bullets" on the slides, so under a strict §7.1 reading they need to be back-filled or explicitly justified-away.

---

## P0 — Blockers (broken functionality, wrong content)

**None.** No incorrect formulas, no wrong complexity bounds, no contradictions with the slides on completeness/optimality conditions. The UCS worked example arrives at the correct optimal path (A→D→F→G, cost 8). The slide-54 table is reproduced faithfully and the chapter's typeset version preserves the footnotes verbatim.

---

## P1 — Important (missing concepts, broken prose, gaps a student would lose marks for)

### P1-1 — Slide 15 dropped: state-count enumeration and NP-hardness of n-Puzzle

Slide 15 is a content-bearing slide, not decoration. It states:

- **8-puzzle:** 9!/2 = **181,440 states**
- **15-puzzle:** 16!/2 > **10 trillion** states
- **24-puzzle:** ~**10^25** states
- **"Optimal solution of n-Puzzle is NP-hard"** (bold, on-slide)

The chapter mentions the 8-puzzle in §3.3 ("8-puzzle tile arrangement") and §3.5 ("for the 8-puzzle, $b$ is at most 4") but **never quotes the state counts** and **never states the NP-hardness result**. The NP-hardness claim in particular is a non-trivial, examinable, stand-alone theoretical fact that the lecturer emphasised on the slide. Dropping it silently is a §7.1 violation.

**Fix:** Add a short paragraph to §3.3 or §3.5 enumerating the three state counts and the NP-hardness fact (cite slide 15).

**Note:** The figures.md catalogue justifies the SKIP of `fig08-8-puzzle.png` with *"the lecturer's point (state count is 9!/2 = 181,440) is captured better as a number than as a tile picture"* — but the chapter does not actually capture that number anywhere. The catalogue's justification is therefore aspirational rather than honest: the figure is skipped *and* its content is also dropped.

### P1-2 — Slide 6 dropped: the Motivation triad

Slide 6 ("Motivation") presents three explicit framing bullets, each with an icon:

1. **Search strategies** — important methods for many approaches to problem-solving
2. **To use search** — abstract formulation of the problem and the available steps
3. **Search algorithms** — **basis for many optimization and planning methods**

The chapter's §1 Overview never restates these three motivational pillars. The third point especially — "basis for many optimization and planning methods" — is the explicit hook into L05 (local search / optimisation) and beyond. The §7 Connections section sketches the link, but the chapter never tells the student that the lecturer explicitly *labelled* search algorithms as the foundation for optimisation and planning. That's a topic-bullet on the deck, so under the §7.1 lens it has to appear in the chapter.

**Fix:** Add a one-paragraph "Why this matters" or restructure §1 to enumerate slide 6's three motivational claims before the four-strategy summary.

### P1-3 — Slide 17 dropped: the four design questions for goal-based agents

Slide 17 ("Building goal-based agents") asks four explicit questions the student must be able to answer when formulating a search problem:

1. How do we represent the **state** of the world?
2. What is the **goal** and how can we recognise it?
3. What are the possible **actions**?
4. What **relevant** information do we encode to describe states, actions and their effects?

The chapter touches each of these implicitly via §3.2's five-component decomposition, but **does not quote the four questions as a teaching checklist**. This matters because the slide presents these as a *problem-formulation rubric* — the exam question "formulate problem X as a search task" maps directly to answering these four. A student reading the chapter loses the rubric framing.

**Fix:** Add a short subsection (or a callout box) in §3.2 listing the four questions verbatim and showing how each maps to the five components.

### P1-4 — Slide 5 dropped: three motivational worked examples

Slide 5 supplies three plain-English problem-formulation examples *before* the formal definition lands:

- Getting from home to SDU (start, goal, operators)
- Loading a moving truck (start, goal, operators)
- Getting settled (start, goal, operators)

These are gentle on-ramps to the formal "initial state / successor function / goal" triple. The chapter goes straight to Romania, vacuum, 8-puzzle, 8-queens, 3-puzzle — all are also on later slides, but the *pedagogical sequencing* of "here are three everyday-life examples first" is lost. Less severe than the above, but still a topic-bullet on a slide that the chapter does not address.

**Fix:** Either embed the three slide-5 examples as a short illustrative list in §3.2 (with a one-line each), or explicitly justify the omission ("the chapter goes directly to formal examples").

### P1-5 — Broken/unfinished sentence in DFS trace (§5.5 Step 2)

§5.5 contains this verbatim:

> | 2 | pop C (top), push F, G | `[B, F, G]` — wait. *Standard convention:* push children in *reverse* order so left child is on top. We follow the slide's left-first traversal, so we push children right-first: C then B → frontier becomes `[C, B]` with B on top. |

This reads like the author was thinking aloud mid-table-cell and forgot to clean up. The word "wait" inside a table row, followed by mid-sentence reasoning, followed by a corrected conclusion, is unprofessional and confusing for a study-prep chapter. The conclusion is correct (the subsequent rows use the corrected order), but the row itself is broken.

**Fix:** Rewrite the §5.5 trace so the first table either uses the LIFO push-order convention from the start, or replace the table with a single clean trace that does not retract itself.

### P1-6 — figures.md SKIP justification for `fig08` is inconsistent with chapter content

As noted in P1-1, `figures.md` justifies skipping the 8-puzzle figure by claiming the state count "is captured better as a number" — but the number is *not* captured in the chapter. Either:

- (a) Add the state count to the chapter (per P1-1), keeping the SKIP justified; or
- (b) Re-word the SKIP justification to admit the figure and its content were both dropped (less good).

Option (a) is the right fix; flagged separately here because it's a figures.md-level issue.

---

## P2 — Polish, suggestions, minor improvements

### P2-1 — §5.3 UCS trace narration of Step 3 is muddled

§5.3 Step 3 row reads:

> "pop D ($g=3$), expand to B ($g=3+2=5$ via D-E? no — D→E is 2, so $g$ would be 5; D→F is 2, so F has $g=5$; D's adjacencies on the slide give B (5), E (5), F (5))"

The parenthetical is a stream of self-corrections that survives into the published table. The mechanics (D adds E at 5 and F at 5; B was already on the fringe at 5 from A→B=5) are all correct, but the narration is confusing. A clean version:

> "Expand D. D's successors are E and F, each at $g=3+2=5$. B is already on the fringe at $g=5$ (from A→B=5). After this step the fringe holds B:5, E:5, F:5."

Same outcome, no retraction.

### P2-2 — §5.3 graph diagram in the code block is hard to read

The ASCII art under "Find the cheapest path from A to G in the directed graph below" is ambitious but the layout doesn't actually parse:

```
      ┌─ 5 ─┐
      ▼     │
  ┌── B ──1─► C
  ...
```

The follow-up "canonical edge list" sentence is what students will actually rely on. Consider deleting the ASCII art and keeping only the edge list — or replacing the ASCII with a cleaner enumeration. The slide-37 figure (Figure 8) already gives the visual; the ASCII duplicates it badly.

### P2-3 — UCS goal-test timing — slide vs. textbook convention

§4.2 says: *"the goal test is performed when a node is popped from the queue (i.e. when chosen for expansion), not when generated... The lecture doesn't state this explicitly on the slide, but the worked example on slide 37 follows this convention."*

Good catch on the implicit convention. But check slide 37: the trace pops G with cost 8 in Step 8 and *then* reports "Found the path". Yes, this matches goal-test-on-pop. The chapter handles this correctly; just consider adding a sentence noting that the slide's *Step 6* generates G at cost 8 but does not return — confirming goal-test-on-pop in the slide itself. Strengthens an already-good footnote.

### P2-4 — Step costs assumption — slide 10 says $c \ge 0$, UCS slide 36 tightens to $c \ge \epsilon > 0$

The chapter handles this correctly in §3.2 ("The slides assume $c \ge 0$ throughout (and UCS additionally requires $c \ge \epsilon > 0$ for completeness)") and again in §4.2. The slide-54 footnote (2) is also preserved. No fix needed — this is a *commendation*, not a defect. Listed in P2 only as confirmation that the harshest version of this completeness condition is correctly stated.

### P2-5 — §5.2 "next strategies pick differently" paragraph speculates incorrectly

§5.2 ends with:

> "BFS picks `Timisoara` next (next in FIFO order after `Sibiu`'s siblings), UCS picks the city with the lowest $g$-value (probably `Zerind` at 75 if Arad→Sibiu were 140), DFS picks the most recently added (`Rimnicu Vilcea`)."

The "probably Zerind at 75 if Arad→Sibiu were 140" hedging is awkward — Arad→Sibiu *is* 140 on the slide-18 map, and Arad→Zerind is 75, so UCS would in fact pick Zerind next (75 < 118 Timisoara < 140 Sibiu). Drop the "probably... if" hedge.

### P2-6 — Glossary line on slide 7 vs. chapter terminology

Slide 7 lists "states, initial state, goal state, successor functions (operators), cost" — the chapter's §3.2 mirrors this but uses "step cost" for the per-action cost and "path cost" for the sum. Both are correct and consistent with the deck, but consider explicitly noting in §3.2 that slide 7's "cost" splits into the slide-10 distinction of "step cost" vs "path cost".

### P2-7 — Slide 16 (3-puzzle) handling

The figure SKIP is justified by the catalogue, but the slide as a *pedagogical example* — "Simpler: 3-Puzzle" — is not narrated in the chapter at all. The slide shows a 7-step trace from `[3,_;2,1]` to `[1,2;_,3]`. The chapter could mention that the lecturer offered a simpler 3-puzzle illustration before the 8-puzzle (one sentence). Minor.

### P2-8 — Slide 19 (8-queens) handling

The chapter mentions 8-queens *in passing* in §3.4 and forwards it to L05. The slide poses the explicit question "What are the states, successor function, goal state?" which is a *student exercise*. Consider adding the 8-queens question as a "Try yourself" callout box — it's a useful self-test against the formulation framework introduced in §3.2.

### P2-9 — Slide 11 vs. slide 18 Romania figures

The catalogue correctly SKIPs `fig05` (slide 11 combined map+graph) in favour of `fig11` (slide 18 standalone graph). Good call; the slide-18 version is cleaner. No issue.

### P2-10 — Chapter mentions $g(n)$, $C^*$, $\epsilon$ — should add definition of $h(n)$ symbolically even though deferred

§3.8 "A\* and admissibility (forward reference)" introduces $f(n) = g(n) + h(n)$ but does not separately define $h(n)$ in symbols (only verbally as "heuristic function, estimate of cost-to-go"). For a cheat-sheet to be useful, an explicit `h(n) — heuristic estimate of remaining cost from n to nearest goal` definition would help. Add to §8 "Notation reminders".

---

## EVIDENCE

### Slide-by-slide coverage matrix

| Slide | Topic | Chapter coverage | Verdict |
|---|---|---|---|
| 1 | Cover | §1 | OK |
| 2 | Maze opener | §2.1 | OK |
| 3 | Joke flowchart | (decorative) | OK |
| 4 | Problem-solving agent definition | §3.1, §1 | OK |
| 5 | Three real-life examples (home→SDU, moving truck, getting settled) | **DROPPED** | **P1-4** |
| 6 | Motivation triad (strategies / abstract formulation / basis for opt+planning) | **DROPPED** | **P1-2** |
| 7 | Objectives + A\* listed but not derived | §1 "Honest note on scope" | OK |
| 8 | Setting: observable/deterministic/discrete/known + maze | §1, Fig 1 | OK |
| 9 | Solution/Search/Close-eyes | §1, §3.1 | OK |
| 10 | Search problem 5 components | §3.2, Fig 2 | OK |
| 11 | Romania intro | §5.2 | OK |
| 12 | State Space definition | §3.3 | OK |
| 13 | Vacuum world intro | §5.1 | OK |
| 14 | Vacuum world state-space graph | §3.3, Fig 3 | OK |
| 15 | **8-puzzle: state counts + NP-hard** | §3.3/§3.5 mention 8-puzzle but DROP state counts and NP-hardness | **P1-1** |
| 16 | 3-puzzle simpler example | not narrated | P2-7 |
| 17 | **Four design questions** for goal-based agents | DROPPED | **P1-3** |
| 18 | Romania route planning graph | §5.2, Fig 6 | OK |
| 19 | 8-queens puzzle | passing mention only, no exercise | P2-8 |
| 20 | Tree Search description + Nodes-vs-states | §3.4, Fig 4 | OK |
| 21 | Tree-search algorithm outline + repeated-state handling | §3.4 pseudocode | OK |
| 22–26 | Tree-search Romania animation | §5.2 + Figs 7a, 7b, 7c | OK |
| 27 | 4 evaluation dimensions | §1, §3.6 | OK |
| 28 | b, d, m parameters | §3.5 | OK |
| 29 | Uninformed search list (4 strategies) | §3.7 | OK |
| 30–34 | BFS animation | §5.4, Fig 9 (final frame) | OK |
| 35 | BFS properties | §4.1 | OK |
| 36 | UCS + ε > 0 condition | §4.2 | OK |
| 37 | UCS worked example | §5.3, Fig 8 | OK (P2-1, P2-2 style issues) |
| 38–46 | DFS animation | §5.5, Fig 10 (final frame) | **P1-5** (broken Step 2 cell) |
| 47 | DFS properties | §4.3 | OK |
| 48 | IDS intro | §4.4 | OK |
| 49 | IDS limit 0 | §5.6 prose | OK |
| 50 | IDS limit 1 | §5.6, Fig 11 | OK |
| 51 | IDS limit 2 | §5.6, Fig 12 | OK |
| 52 | IDS limit 3 | §5.6, Fig 13 | OK |
| 53 | IDS properties + time accounting | §4.4 | OK |
| 54 | Comparison table | §4.5, Fig 5, typeset table | OK |
| 55 | Next class: Informed Search | §1, §7 | OK |
| 56 | Thank you | N/A | OK |

### Figures catalogue audit

Catalogue claims 15 USE/REWORK embedded; verified by grep against chapter — all 15 appear:

- `fig03-search-maze-labelled.png` → Figure 1 (§2.1)
- `fig04-search-problem-components.png` → Figure 2 (§3.2)
- `fig07-vacuum-world-state-space.png` → Figure 3 (§3.3)
- `fig13-tree-search-diagram.png` → Figure 4 (§3.4)
- `fig38-comparison-table.png` → Figure 5 (§4.5)
- `fig11-romania-route-graph.png` → Figure 6 (§5.2)
- `fig14-tree-search-step1.png` → Figure 7a (§5.2)
- `fig17-tree-search-step4.png` → Figure 7b (§5.2)
- `fig18-tree-search-step5-fringe.png` → Figure 7c (§5.2) [REWORK]
- `fig24-ucs-worked-example.png` → Figure 8 (§5.3)
- `fig23-bfs-step5.png` → Figure 9 (§5.4)
- `fig33-dfs-step9.png` → Figure 10 (§5.5)
- `fig35-ids-limit-1.png` → Figure 11 (§5.6)
- `fig36-ids-limit-2.png` → Figure 12 (§5.6)
- `fig37-ids-limit-3.png` → Figure 13 (§5.6)

All 58 SKIPs are justified in figures.md. None of the 73 figures on disk is *informative-but-dropped-silently* under my review — except indirectly via P1-1 (fig08's information content was claimed-captured but actually wasn't).

### Honesty about the A\* gap (per review brief)

The chapter discloses the A\*/heuristics gap **explicitly and repeatedly**:

- §1 paragraph 5: "Honest note on scope. Slide 7 also lists *informed search — best-first (greedy, A\*), heuristics* as an objective. Despite that, the deck does not derive any informed-search method..."
- §3.8 forward reference: "The L03 deck does not introduce these terms; they will arrive when needed in subsequent lectures."
- §4.5 caption of Figure 5 keeps the slide-54 "haven't covered" callout
- §6 Pitfall #10: "Claiming the lecture covers A\*. It does not."
- §8 cheat-sheet bullet: "A\*, greedy best-first, and heuristics are *not* covered in this lecture"

This is **commendable** — no penalty for the absent A\* material.

### Slide-15 specific evidence (P1-1)

Slide 15 verbatim:
> "Initial State: Any locations of tiles, number of states: 8-puzzle: 9!/2 = 181,440 states; 15-puzzle: 16!/2 > 10 trillion states; 24-puzzle: 10^25 states.
> Successor Function: Actions: Move blank left, right, up, down, and consequent states.
> Path cost: 1 per move.
> **Optimal solution of n-Puzzle is NP-hard**"

Grep of chapter for "181,440", "9!/2", "NP-hard", "10 trillion", "10^25", "24-puzzle", "15-puzzle" returns **no matches**. Confirmed P1-1.

### DFS §5.5 evidence (P1-5)

Direct quote from chapter line 467:

> | 2 | pop C (top), push F, G | `[B, F, G]` — wait. *Standard convention:* push children in *reverse* order so left child is on top. We follow the slide's left-first traversal, so we push children right-first: C then B → frontier becomes `[C, B]` with B on top. |

Confirmed P1-5 — broken/self-correcting table cell.

---

## PM Report

**Assignment recap:** L03 Round 1 Reviewer #1 — Concept Completeness (incl. Figures), lens §7.1.

**Status:** NEEDS_REVISION.

**P0 findings:** 0.

**P1 findings:** 6.
1. Slide 15 dropped: 8-puzzle/15-puzzle/24-puzzle state counts and **n-Puzzle NP-hardness** are missing from the chapter despite being on a content slide.
2. Slide 6 dropped: the **Motivation triad** (search strategies / abstract formulation / **basis for optimisation+planning**) is not enumerated in §1.
3. Slide 17 dropped: the **four design questions** (state representation / goal recognition / actions / relevant information encoding) are missing as a rubric.
4. Slide 5 dropped: three plain-English problem-formulation examples (home→SDU, moving truck, getting settled) absent.
5. §5.5 DFS trace Step 2 contains a broken, self-correcting table cell ("...`[B, F, G]` — wait. *Standard convention:*..."). Cleanup required.
6. figures.md justifies SKIP of `fig08-8-puzzle.png` by claiming the state count "is captured better as a number than as a tile picture" — but the number is not captured in the chapter (couples to P1-1).

**P2 findings:** 10 (style, narration cleanups, optional additions). Most important: §5.3 Step 3 narration is muddled; §5.3 ASCII graph is hard to parse; §5.2 has an incorrect "probably... if" hedge about Arad→Sibiu cost when the slide gives a definite 140.

**Honesty about A\* gap:** Excellent. Chapter discloses the absence in five separate places. No penalty.

**What PM should do next:**
1. Dispatch the lecture-author employee to back-fill the four slide-content gaps (P1-1 through P1-4): a short paragraph each, citing slides 5, 6, 15, 17.
2. Same employee: rewrite §5.5 DFS Step 2 cell so it does not retract itself (P1-5).
3. Same employee: clean §5.3 narration and ASCII graph (P2-1, P2-2).
4. Re-dispatch Reviewer #1 for a round-2 verify against this exact list before accepting.

**DOCUMENT.md updated:** N/A for QA (no source files modified).
