# Reviewer 2 — Mathematical Rigor — L03 Round 1

**Reviewer:** Lecture Reviewer #2 (Mathematical Rigor)
**Artifact under review:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L03-Uninformed-Search.md`
**Source of truth:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture3-Uninformed Search.pdf` (56 slides)
**Spec section:** §7.1 — Formula correctness, derivation steps, indices, notation, assumptions, variable naming, LaTeX, slide-37 UCS trace cross-check.

---

## VERDICT

**FAIL.** The chapter contains a P0 contradiction between its own UCS trace prose and the resulting fringe (step 7), a P0 internal inconsistency in §5.3 about whether `E→G` exists (chapter declares the edge but its trace ignores it), and uncleaned stream-of-consciousness prose in §5.3 step 3 and §5.5 step 2 that has no place in a finished reference. A re-write of §5.3 and §5.5 is required before this lecture can move to App Tester.

---

## P0 — Blocking

### P0-1. §5.3 step 7 mismatches slide 37 exactly

**Spec requirement:** "the slide-37 UCS trace must be cross-checked step-by-step — the chapter has a full tabular trace that needs to match the slide exactly."

**Slide 37, Step 7 (source of truth):**
> Step 7
> Expand C
> Fringe:
>   **Node** G
>   **Cost** 14
> Explored: A D B E F C

**Chapter §5.3 step 7 (line 432):**
```
| 7 | pop C ($g=6$), expand to G via $C\!\to\!G=8$ ($g=6+8=14$) — but we
already have $G$ at cost 8, so do *not* replace | `{G:8}` | `{A, D, B, E, F, C}` |
```

The chapter's fringe after step 7 is `{G:8}`. The slide's fringe after step 7 is `{G:14}`. These are **different numbers**.

Either:
(a) the slide has an error (it replaced the cheaper G:8 with the more expensive G:14, violating UCS), and the chapter silently "corrected" it without flagging the discrepancy; or
(b) the chapter's mental model of UCS differs from the slide's mental model.

Whichever it is, the chapter MUST explicitly call this out. The current text passes off "the trace matches the slide" while in fact disagreeing with it on the step-7 fringe value. A student preparing from the chapter and then sitting an exam written from the slide will get caught.

**Fix:** Add an editor's note before the table along the lines of "Slide 37 prints G:14 in step 7, but this is a slide-side error — UCS must not replace an existing cheaper fringe node with a more expensive duplicate; we keep G:8 here. The final path A→D→F→G with cost 8 is unchanged."

**Evidence:**
- Slide 37, Step 7 panel: "Node G / Cost 14 / Explored: A D B E F C"
- Chapter line 432: "`{G:8}`"

---

### P0-2. §5.3 contradicts itself on whether `E → G` exists

**Chapter line 417 (canonical edge list):**
> $A\!\to\!B = 5$, $A\!\to\!D = 3$, $B\!\to\!C = 1$, $C\!\to\!E = 6$, $D\!\to\!E = 2$, $D\!\to\!F = 2$, **$E\!\to\!G = 4$**, $C\!\to\!G = 8$, $F\!\to\!G = 3$, and an arc back $E\!\to\!B = 4$.

**Chapter line 430 (step 5 of its own trace):**
> | 5 | pop E ($g=5$), no improvements | `{F:5, C:6}` | `{A, D, B, E}` |

If `E → G = 4` is in the edge list, then expanding E at $g=5$ MUST generate G with $g = 5+4 = 9$ and add it to the fringe (since G is not yet in explored or frontier). The chapter's row says "no improvements" and the fringe `{F:5, C:6}` does not contain G — this is **algorithmically wrong given the edge list the chapter just stated**.

Either:
- The slide's graph does NOT contain an outgoing arc `E → G` (in which case the chapter's edge list at line 417 is wrong and must be corrected — likely the arc is `G → E` directionally or there's no E↔G edge at all), or
- The slide's graph does contain `E → G = 4` and the slide's trace at step 5 missed it (in which case the chapter is reproducing a slide-side bug without flagging).

Reading slide 37 carefully, the trace at step 6 ("Expand F → Fringe: Node C G, Cost 6 8") is the FIRST time G appears in the fringe, which is consistent only with G having NO predecessor among {A, D, B, E} other than F. So the canonical edge list at line 417 is almost certainly wrong about `E → G = 4`.

**Fix:** Remove `E → G = 4` from the edge list (or replace with the actual edge direction shown on the slide), and verify every other entry in the edge list against the slide image. If `E → G` is genuinely on the slide, then either the slide is buggy or the chapter trace is wrong; either way the chapter must flag it.

**Evidence:**
- Chapter line 417 declares `E → G = 4`.
- Chapter line 430 says expanding E yields "no improvements" with no G in the resulting fringe — incompatible with `E → G = 4`.
- Slide 37 trace's first appearance of G is at step 6 (after expanding F), confirming G has no predecessor in {A, D, B, E}.

---

### P0-3. §5.3 step 3 prose is stream-of-consciousness, not a finished trace

**Chapter line 428 verbatim:**
> | 3 | pop D ($g=3$), expand to B ($g=3+2=5$ via D-E? no — D→E is 2, so $g$ would be 5; D→F is 2, so F has $g=5$; D's adjacencies on the slide give B (5), E (5), F (5)) | `{B:5, E:5, F:5}` | `{A, D}` |

This is the author thinking aloud inside a published table cell. It is **incoherent** as a step description:
- It claims D expands to B with cost 5, but the canonical edge list at line 417 has NO edge `D → B`. The B:5 in the fringe at step 3 is the **original** B added from A's expansion at step 2 (via A→B=5), not a new B via D.
- It then second-guesses itself ("via D-E? no — D→E is 2…") in published prose.
- It conflates which node B at cost 5 means.

The resulting fringe `{B:5, E:5, F:5}` is correct (B is left over from step 2; E and F are new from D), but the prose says the opposite ("expand to B").

**Fix:** Re-write the step 3 cell cleanly, e.g.:
> | 3 | pop D ($g=3$); D's successors are E ($g=3+2=5$) and F ($g=3+2=5$). B already in frontier at $g=5$ from step 2. | `{B:5, E:5, F:5}` | `{A, D}` |

**Evidence:** Chapter line 428.

---

### P0-4. §5.5 DFS trace step 2 contains an editorial "wait." in the published table

**Chapter lines 466–467 verbatim:**
> | 2 | pop C (top), push F, G | `[B, F, G]` — wait. *Standard convention:* push children in *reverse* order so left child is on top. We follow the slide's left-first traversal, so we push children right-first: C then B → frontier becomes `[C, B]` with B on top. |

This is stream-of-consciousness mid-table editing left in the document. A published trace cannot say "wait." in the middle of a row. The author is mid-correction inside the artifact.

**Fix:** Delete this row. Rebuild the DFS trace as a single clean table that matches the slide's left-first traversal from the start.

**Evidence:** Chapter lines 466–467.

---

## P1 — Important

### P1-1. §3.5 definition of $d$ deviates from slide 28

**Slide 28 verbatim:**
> *d:* depth of the least-cost (cheapest) solution

**Chapter §3.5 line 175:**
> $d$ — **depth of the shallowest goal**: the length (in actions) of the shortest path from $s_0$ to any goal state.

"Shallowest goal" and "least-cost solution" are **not the same thing** when step costs vary. The slide 28 definition (least-cost) and the slide 54 footnote ("d is the depth of the shallowest solution, or is m when there is no solution") **disagree with each other**, and the chapter sided with slide 54 silently. This is a real mathematical ambiguity — the canonical Russell & Norvig definition is "shallowest" (matching slide 54 and the chapter), but the chapter MUST flag that slide 28 says something different, because a student answering "what is d?" on the exam may be marked against slide 28.

**Fix:** Add a footnote at chapter line 175: "Slide 28 of the deck phrases this as 'depth of the least-cost (cheapest) solution', which is technically a different notion. Slide 54's footnote and the standard textbook convention is 'shallowest solution', which we follow here. For the BFS/IDS optimality bound (uniform step costs) the two coincide."

**Evidence:** Slide 28 vs slide 54 footnote; chapter §3.5 line 175.

---

### P1-2. §4.1 BFS optimality phrasing generalises slide 35 silently

**Slide 35 verbatim:**
> Optimal?
> Yes – if cost = 1 per step

**Chapter §4.1 line 233:**
> **Optimal?** Yes — *but only when every step costs the same*.

The chapter's "every step costs the same" is mathematically a stronger claim than "cost = 1 per step" — they happen to be equivalent (rescaling), but the slide literally says "= 1". Slide 53 IDS says the same ("Yes, if step cost = 1"). Only slide 54 footnote 3 ("cost-optimal if action costs are all identical") justifies the chapter's generalisation.

**Fix:** Either restate exactly as the slide ("if cost = 1 per step") or add a one-line footnote that says "Slides 35 and 53 say 'cost = 1'; slide 54 footnote 3 generalises this to 'all identical', which is what we use."

**Evidence:** Slide 35, slide 53, slide 54 footnote 3; chapter line 233 and line 315.

---

### P1-3. §5.2 line 397 conditional is non-sensical

**Chapter line 397:**
> UCS picks the city with the lowest $g$-value (probably `Zerind` at 75 if Arad→Sibiu were 140), DFS picks the most recently added (`Rimnicu Vilcea`).

"if Arad→Sibiu were 140" — but Arad→Sibiu **is** 140 per slide 18 (the very figure cited in the chapter). The conditional is mis-typed. The actual point is: UCS picks the cheapest, and at the fringe `{Sibiu:140, Timisoara:118, Zerind:75}` the cheapest is Zerind, full stop. No conditional needed.

**Fix:** "UCS picks `Zerind` (cheapest at $g=75$); DFS picks the most recently added child (`Rimnicu Vilcea` if Sibiu was just expanded with that as the last child pushed)."

**Evidence:** Chapter line 397, slide 18, slide 11.

---

### P1-4. §5.5 Figure 10 caption attributes content that is not on slide 46

**Chapter line 484 (Figure 10 caption):**
> *Figure 10: DFS step 9 (slide 46). Compared with BFS on the same tree, DFS dives left-deep (A → B → D, back up to E, back up to C, then F, then G).*

Slide 46 is the last DFS slide and the red arrow is on **C**. The slide animation (slides 38–46) shows A → B → D → E → C only. The chapter's caption claims slide 46 shows "then F, then G" — those steps are **not on any L03 slide**. The chapter is extrapolating and attributing the extrapolation to slide 46.

**Fix:** Either change the caption to "Slide 46 ends at C; we extend the trace to F and G in the table above" or remove the F/G claim from the caption.

**Evidence:** Slide 46 image shows red arrow on C; no F or G expansion is animated in L03.

---

### P1-5. §3.4 algorithm template asserts the "replace if cheaper" rule for general TREE-SEARCH

**Chapter §3.4 lines 163–164:**
> else if s' is in frontier with higher path_cost:
>     replace the existing frontier node with `child`

Slide 21 only states this rule once, generically, under "To handle repeated states". The chapter promotes it to part of the generic algorithm. This is fine for UCS (it's required for correctness) but it is **NOT meaningful for BFS or DFS**, because BFS expands in FIFO order (the existing copy was added first and will be popped first regardless of cost) and DFS doesn't care about cost at all. Including this branch in the generic template at §3.4 then **also** in BFS (§4.1) and UCS (§4.2) suggests it always matters. For BFS it doesn't.

**Fix:** Note at §3.4 that the "replace if cheaper" branch is **only meaningful for UCS** (and for any cost-aware strategy); for BFS/DFS it can be dropped. Or move that branch out of the generic template and into UCS-only.

**Evidence:** Slide 21 (lists the rule generically); chapter §3.4 line 163, §4.1 line 226 (omits it correctly for BFS), §4.2 line 257 (includes it for UCS — correct).

The chapter's §4.1 BFS pseudocode (line 226) does NOT include the replace rule — which is actually consistent and correct, but contradicts the generic template at §3.4 line 163. So the inconsistency is between the chapter's own §3.4 and §4.1.

---

### P1-6. §1 line 38 defines $m$ in the search tree, slide 28 defines it in the state space

**Slide 28 verbatim:**
> *m*: maximum length of any path in the **state space** (may be infinite)

**Chapter §1 line 38:**
> $m$ — the **maximum depth** of any branch (possibly $\infty$).

"Maximum depth of any branch" of the **search tree** is finite once the tree is finite; "maximum length of any path in the **state space**" can be infinite if the state space has cycles even when the tree under graph search is finite. The chapter's §3.5 line 176 gets it right ("maximum length of any path in the state space"), so this is just a sloppy phrasing in §1.

**Fix:** §1 line 38 → "$m$ — the **maximum length of any path in the state space** (possibly $\infty$)."

**Evidence:** Slide 28 vs chapter §1 line 38.

---

### P1-7. §5.3 graph diagram (lines 403–415) does not match the prose edge list

The ASCII art at lines 403–415 is stylized and the prose at line 417 says it is "a little stylised" and provides a "canonical edge list". But the two disagree:
- ASCII art shows "B ──1─► C" and "C → G also cost 4 not shown directly above" in a parenthetical, but the canonical edge list says `C → G = 8`. The parenthetical "(E → G also cost 4 not shown directly above)" further contradicts itself ("not shown" but the art does show `E ─4─► G`).
- The art shows `D → F cost 2` and `F → G cost 3` in a parenthetical that says "(D → F cost 2, F → G cost 3)" — these match the edge list, fine.

The whole ASCII block is confusing enough that a student trying to verify the trace from it cannot. Either replace with a properly rendered diagram (the figure `fig24-ucs-worked-example.png` already exists for this purpose — Figure 8) and DELETE the ASCII attempt, or fix the ASCII so it matches the canonical edge list exactly.

**Fix:** Delete the ASCII block at lines 403–415 entirely; rely on Figure 8 plus the edge list at line 417 (which itself needs the P0-2 fix).

**Evidence:** Chapter lines 403–417.

---

### P1-8. Slide 36 uses $[\,]$ but chapter renders as $\lfloor\,\rfloor$ without note

**Slide 36 verbatim:** $O(b^{1+[C^*/\epsilon]})$
**Slide 54 verbatim:** $O(b^{1+\lfloor C^*/\epsilon \rfloor})$
**Chapter renders as:** $O\!\bigl(b^{\,1 + \lfloor C^*/\epsilon \rfloor}\bigr)$ everywhere.

This is the **correct** rendering — slide 36 just uses generic brackets `[ ]` that on slide 54 are confirmed as floor brackets `⌊ ⌋`. The chapter is right but should drop a footnote: "Slide 36 prints $[\cdot]$; slide 54 confirms this is the floor function." Without that footnote a careful student is left wondering whether `[·]` means ceiling, floor, or rounding.

**Fix:** Add a one-line footnote on first use of the bound at §4.2 line 265.

**Evidence:** Slide 36, slide 54 (footnote definition), chapter §4.2.

---

## P2 — Polish

### P2-1. §3.5 line 174 unsourced "$b \approx 35$ for chess" claim

Slide 28 does not give the chess branching factor. The chapter cites it without a source. It is a textbook standard value (Russell & Norvig give 35 for chess), but if this chapter aims to be a faithful summary of L03 slides, unsourced extra data belongs in a "background" callout, not embedded in a definition.

**Fix:** Either drop the chess example or footnote "Standard textbook value (Russell & Norvig); not in the L03 slides."

---

### P2-2. §4.2 line 243 "the lecture doesn't state this explicitly on the slide" — unverifiable claim about UCS goal-test-on-pop

The chapter asserts UCS tests goals on pop (expansion), not on generation, and adds: "The lecture doesn't state this explicitly on the slide, but the worked example on slide 37 follows this convention." Verifying from slide 37: at step 6, G is generated with $g=8$ but is NOT returned; the algorithm continues to step 7 (expand C) and step 8 (expand G). So yes, slide 37 tests on pop. The chapter's note is accurate but the phrasing "the lecture doesn't state this explicitly" makes a strong claim about the absence of a statement — confirmed by reading slides 36–37 — that should be tightened to "Slide 36's properties list does not flag this; slide 37's trace makes it implicit."

---

### P2-3. §6 pitfall #11 references slide 21, no clarity about UCS-specific application

Pitfall #11 (chapter line 545) refers to the slide-21 "replace if cheaper" rule. This is correct, but as noted under P1-5, the rule is only meaningful for cost-aware strategies. Add a parenthetical: "(matters for UCS; harmless to omit for BFS/DFS)."

---

### P2-4. §5.6 line 511 arithmetic-by-hand is fine; consider showing the per-level table

The IDS overhead example (b=10, d=5 → 123456) is correct but presented as a sum without a per-level breakdown. For pedagogical clarity, show the table:

| level $k$ | coefficient $(d+1-k)$ | $b^k$ | contribution |
|-----------|------------------------|--------|---------------|
| 0 | 6 | 1 | 6 |
| 1 | 5 | 10 | 50 |
| 2 | 4 | 100 | 400 |
| 3 | 3 | 1000 | 3000 |
| 4 | 2 | 10000 | 20000 |
| 5 | 1 | 100000 | 100000 |
| **sum** |  |  | **123,456** |

Optional improvement, not required.

---

### P2-5. §2.4 line 75 carts analogy is fine but mixes "advance the cart" with "step"

Minor: "advance the cart that has accumulated the least cost so far — that is, advance the cheapest cart by one step". This conflates "current cart cost" with "step". The accurate analogy is "extend the cheapest partial path by one edge". Cosmetic.

---

### P2-6. LaTeX formatting

Chapter consistently uses `O(b^d)`, `O(b\,m)`, `O(b\,d)` — clean. No malformed LaTeX. The only minor nit: line 597 uses `O(b^{1+\lfloor C^*/\epsilon\rfloor})` in the cheat-sheet table without the `\!\bigl( ... \bigr)` spacing used elsewhere — purely cosmetic.

---

## EVIDENCE TABLE — Slide-by-slide formula verification

| Topic | Slide | Chapter location | Match? |
|---|---|---|---|
| Search problem 5 components | 10 | §3.2 lines 111–115 | Yes |
| State space defn | 12 | §3.3 line 128 | Yes |
| Vacuum 8 states | 13–14 | §3.3 line 131, §5.1 line 361 | Yes |
| Eval dimensions (4) | 27 | §1 lines 29–32, §3.6 lines 186–189 | Yes |
| b, d, m defns | 28 | §3.5 lines 174–176 | **d phrasing P1-1; m phrasing P1-6** |
| BFS Complete | 35 | §4.1 line 232 | Yes |
| BFS Optimal "if cost = 1" | 35 | §4.1 line 233 | **P1-2 (generalisation)** |
| BFS Time $O(b^d)$ | 35 | §4.1 line 234 | Yes |
| BFS Space $O(b^d)$ | 35 | §4.1 line 235 | Yes |
| UCS Complete | 36 | §4.2 line 263 | Yes (with ε caveat in chapter) |
| UCS Optimal | 36 | §4.2 line 264 | Yes |
| UCS Time $O(b^{1+\lfloor C^*/\epsilon\rfloor})$ | 36 | §4.2 line 265 | Yes (rendering note P1-8) |
| UCS Space same | 36 | §4.2 line 266 | Yes |
| UCS = BFS when costs equal | 36 | §4.2 line 267 | Yes |
| UCS trace step 1 | 37 | §5.3 line 425 | Yes |
| UCS trace step 2 | 37 | §5.3 line 426 | Yes |
| UCS trace step 3 | 37 | §5.3 line 427 | **P0-3 (garbled prose)** |
| UCS trace step 4 | 37 | §5.3 line 429 | Yes |
| UCS trace step 5 | 37 | §5.3 line 430 | Yes — but **P0-2** (edge list inconsistency) |
| UCS trace step 6 | 37 | §5.3 line 431 | Yes |
| UCS trace step 7 | 37 | §5.3 line 432 | **P0-1 (G:8 vs slide G:14)** |
| UCS trace step 8 (final path) | 37 | §5.3 line 433, 435 | Yes |
| DFS Complete | 47 | §4.3 line 292 | Yes |
| DFS Optimal | 47 | §4.3 line 293 | Yes |
| DFS Time $O(b^m)$ | 47 | §4.3 line 294 | Yes |
| DFS Space $O(b\,m)$ | 47 | §4.3 line 295 | Yes |
| DFS animation order | 38–46 | §5.5 lines 472–482 | **P1-4 (caption extrapolation)** |
| IDS Complete | 53 | §4.4 line 314 | Yes |
| IDS Optimal "if step cost = 1" | 53 | §4.4 line 315 | **P1-2 (same generalisation)** |
| IDS Time sum & $O(b^d)$ | 53 | §4.4 line 317 | Yes |
| IDS Space $O(b\,d)$ | 53 | §4.4 line 319 | Yes |
| IDS arithmetic example | (chapter only) | §5.6 line 511 | Yes (verified $6+50+400+3000+20000+100000 = 123456$) |
| Comparison table | 54 | §4.5 lines 332–337 | Yes (covered four only, matches slide) |
| Footnote 1 (b finite) | 54 | §4.5 line 341 | Yes |
| Footnote 2 (ε > 0) | 54 | §4.5 line 343 | Yes |
| Footnote 3 (costs identical) | 54 | §4.5 line 345 | Yes |
| A\* / informed deferred | 54, 55 | §1 line 25, §3.7 line 197 | Yes |

---

## Report to PM

**Assignment recap:** Reviewer #2 (Mathematical Rigor) for L03 Round 1 chapter against the L03 PDF source.

**Status:** Fail. P0 issues in the UCS worked example block (§5.3) and editorial leftovers in DFS trace (§5.5).

**P0 findings:**
1. **§5.3 step 7 (chapter line 432) prints fringe `{G:8}` while slide 37 step 7 prints fringe `{G:14}`.** The chapter silently corrected what looks like a slide-side bug without flagging the discrepancy. Either flag the slide as wrong with an editor's note, or match the slide and explain the resulting algorithmic inconsistency.
2. **§5.3 edge list (chapter line 417) declares `E → G = 4` but the chapter's own trace (line 430) treats E as having no successor G.** Either the edge list is wrong or the trace is wrong. Reading slide 37's step 6 (G first appears via F) suggests the edge list is wrong and `E → G = 4` should be removed.
3. **§5.3 step 3 (chapter line 428) is stream-of-consciousness prose** ("expand to B ($g=3+2=5$ via D-E? no — D→E is 2…") that wrongly says D expands to B (there is no D→B edge per the chapter's own edge list). Rewrite cleanly.
4. **§5.5 step 2 (chapter lines 466–467) contains a literal "wait." mid-table** as the author corrects themselves inside the published artifact. Delete and re-do the DFS table.

**P1 findings:**
1. §3.5 line 175 — definition of $d$ as "shallowest goal" deviates from slide 28's "least-cost (cheapest) solution" without flagging the slide-internal contradiction (slide 54 also says "shallowest").
2. §4.1 line 233 and §4.4 line 315 — chapter generalises "cost = 1 per step" (slides 35, 53) to "every step costs the same" without footnote; only slide 54 footnote 3 justifies the generalisation.
3. §5.2 line 397 — nonsensical conditional "if Arad→Sibiu were 140" (it is 140 per slide 18).
4. §5.5 Figure 10 caption (line 484) — attributes "F, then G" exploration to slide 46, which only shows up to C.
5. §3.4 lines 163–164 vs §4.1 line 226 — generic algorithm template includes "replace if cheaper" branch but BFS pseudocode correctly omits it; flag that the branch is UCS-only.
6. §1 line 38 — $m$ defined as "max depth of any branch" (search tree) rather than slide 28's "max length of any path in the state space"; §3.5 line 176 gets it right, §1 needs to match.
7. §5.3 ASCII graph (lines 403–415) is stylised, partially contradicts the canonical edge list, and contains self-contradictory parentheticals ("not shown directly above" then shown directly above). Delete in favour of Figure 8.
8. §4.2 line 265 — `[ ]` vs `⌊ ⌋` in slide 36 vs slide 54 should be flagged with a one-line footnote.

**P2 findings:**
1. §3.5 line 174 — unsourced "$b \approx 35$ for chess" not on any L03 slide.
2. §4.2 line 243 — UCS goal-test-on-pop claim about slide absence; tighten phrasing.
3. §6 pitfall #11 — clarify that the "replace if cheaper" rule is UCS-only.
4. §5.6 line 511 — add per-level table to make the IDS arithmetic auditable.
5. §2.4 line 75 — minor analogy phrasing.
6. §5.3 line 597 — cosmetic LaTeX spacing inconsistency in cheat-sheet table.

**QA Checklist (§7) status (interpreted for a lecture-summary deliverable):**
- Formulas match source: **FAIL** (P0-1, P0-2).
- Derivation steps complete: **FAIL** (P0-3 step 3 incoherent).
- Indices and notation correct: **PASS with caveats** (P1-1 d, P1-6 m).
- Assumptions stated: **PASS** (ε > 0, c ≥ 0 both noted).
- Variable names consistent: **PASS** (g, C*, ε, b, d, m used consistently).
- LaTeX clean: **PASS** (minor P1-8 floor notation footnote needed).
- Slide-37 UCS trace step-by-step match: **FAIL** (P0-1, P0-2).
- Worked-example prose finished: **FAIL** (P0-3, P0-4 stream-of-consciousness leftovers).

**Acceptance criteria (§1) status:** N/A — this is a lecture-summary review, not a feature.

**DOCUMENT.md audit:** N/A for lecture chapter review (no code directories modified).

**Out-of-scope observations:**
- The chapter's §5.5 DFS table is technically a hybrid of the slide's actual animation (which stops at C) plus author extrapolation (F, G). This is pedagogically fine if labelled, but Figure 10's caption (P1-4) mis-attributes the extrapolation to slide 46. Worth a broader audit for "claims attributed to slides" across the chapter.
- §3.8 (A* forward reference) is responsibly flagged but the cheat-sheet at §8 line 613 leaves `f(n) = g(n) + h(n)` in plain text without re-flagging it as forward-reference there. Minor.
- Cross-references in §7 (lines 557–571) name future lectures (L05, L06, L07, L09b) — these are NOT my review scope but worth a sanity pass when those lectures land, to make sure the forward links are honored.

**Concerns / risks:**
1. The UCS worked example is the most exam-relevant figure in the entire lecture (chapter line 420 says so itself). Two P0 issues in this single block (P0-1 step-7 disagreement, P0-2 edge-list inconsistency) is a serious risk for student learning. This is THE block to get right.
2. The chapter has two separate "author thinking aloud in a published table" leakages (P0-3, P0-4). This suggests the worked-examples section was not given a final editing pass. Recommend a full re-read of §5 before re-QA.

**What PM should do next:**
1. Dispatch the lecture-author engineer to fix P0-1, P0-2, P0-3, P0-4 (priority order). Specifically:
   - Verify slide 37 graph directionality (especially `E → G` vs `G → E`) by re-examining the image; correct the edge list at line 417.
   - Re-write §5.3 step 3 and step 7 cleanly.
   - Re-write §5.5 step 2 cleanly.
   - Decide on the slide-37 step-7 G:14 vs G:8 question: either match the slide exactly (with editor's note flagging the slide-side bug) or correct silently with explicit comment.
2. Then address P1-1 through P1-8 (P1-3 line 397 is a trivial typo fix, do at the same time).
3. Re-dispatch Reviewer #2 for verification of P0 fixes.
4. Only after P0 cleared should this lecture move to App Tester or final Code Reviewer.

**DOCUMENT.md updated:** N/A for QA.
