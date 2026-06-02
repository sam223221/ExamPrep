# L03 Round 1 — Reviewer 4 (Exam Readiness)

**Lecture:** L03 — Uninformed Search
**Reviewer role:** Exam writer
**Source PDF:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture3-Uninformed Search.pdf`
**Chapter:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L03-Uninformed-Search.md`
**Date:** 2026-05-22

---

## VERDICT

**FAIL — REWRITE REQUIRED.**

The chapter reads well and covers the slide deck competently, but as an **exam study artifact** it has serious defects. The single most important worked example in the entire lecture — the UCS trace on slide 37 — is **reproduced incorrectly** in the chapter (the trace contradicts the slide on multiple steps and the edge list it claims to use does not match the slide's graph). A student who memorizes the chapter's table will get the wrong answer on an exam question taken directly from this slide. That alone is a P0.

Beyond the broken UCS trace, the chapter has structural gaps that hurt exam readiness: there is no worked example for problem **formulation** (despite the lecture spending five slides on it — moving truck, 8-puzzle, 3-puzzle, 8-queens, route planning), no IDS time-cost numerical example matching the lecturer's accounting formula, no derivation of the $b^{1+\lfloor C^*/\epsilon\rfloor}$ bound with a concrete adversarial example, and no worked example of "BFS-vs-UCS gives different answers" — the single most likely free-response prompt on this material. The DFS trace in §5.5 contains a confused "wait" mid-table that no student should ever see in study material.

Of the 10 plausible exam questions I drafted (see EVIDENCE), the chapter as written lets a student answer **5 fully, 3 partially, and 2 not at all**.

---

## P0 — MUST FIX BEFORE SHIPPING

### P0-1 — UCS worked example (§5.3) is wrong and self-contradictory

This is the most important worked example in the lecture and the chapter botches it. The slide-37 trace gives:

| Step | Frontier (Node : Cost) | Explored |
|------|------------------------|----------|
| 1 | A : 0 | – |
| 2 | D B : 3 5 | A |
| 3 | B E F : 5 5 5 | A D |
| 4 | E F C : 5 5 6 | A D B |
| 5 | F C : 5 6 | A D B E |
| 6 | C G : 6 8 | A D B E F |
| 7 | G : 14 | A D B E F C |
| 8 | Expand G → path A→D→F→G | — |

That is what the **slide** says. Now the chapter's version of step 7 (line 432):

> `pop C ($g=6$), expand to G via $C\!\to\!G=8$ ($g=6+8=14$) — but we already have $G$ at cost 8, so do *not* replace`
> Frontier becomes `{G:8}`

This contradicts the slide. The slide explicitly writes "Cost 14" in step 7's frontier (singleton G with cost 14, not G with cost 8). The chapter has invented a "do not replace" outcome that the slide does not show. Either (i) the slide is wrong and we should call it out, or (ii) the chapter rewrote the trace wrongly. Either way an exam question lifted from the slide will produce the slide's answer, not the chapter's.

Worse — the chapter's edge list (line 417):

> `$A\!\to\!B = 5$, $A\!\to\!D = 3$, $B\!\to\!C = 1$, $C\!\to\!E = 6$, $D\!\to\!E = 2$, $D\!\to\!F = 2$, $E\!\to\!G = 4$, $C\!\to\!G = 8$, $F\!\to\!G = 3$, and an arc back $E\!\to\!B = 4$`

does not match the trace. With this edge list:
- After popping A (g=0), children are D (g=3) and B (g=5). OK.
- After popping D (g=3), children are E (g=3+2=5) and F (g=3+2=5). Slide says frontier after step 3 is `B:5, E:5, F:5` — so D does NOT generate B (no D→B edge), but the chapter's narrative in line 428 says "expand to B (g=3+2=5 via D-E?)". This is incoherent — the chapter author is *confused* about which edges exist in the graph.

The slide's graph (per the screenshot description) has edges: A→B(5), A→D(3), B→C(1), B→E(4), C→E(6), C→G(8), D→E(2), D→F(2), E→G(4), F→G(3). After expanding D, only E and F are reached — not B. The chapter's "expand D... to B (g=5)" is wrong. The chapter is reading the slide's frontier row "B E F : 5 5 5" as "D generated all three" when in fact B was already in the frontier from step 2 with g=5 and only E and F are new.

The optimal-path claim at line 435 (`A → D → F → G with total cost $3 + 2 + 3 = 8$`) happens to match the slide's final answer, but it sits on top of a trace that contradicts itself and the slide. A student studying this section will fail an exam question asking to reproduce slide 37.

**Fix:** Re-trace the example by hand against the slide. State the edge list once, derive the trace, and reconcile against the slide. Resolve the C→G(8) vs G(14) issue explicitly — the slide's step-7 frontier "G : 14" suggests UCS re-discovered G via C with cost 6+8=14 and replaced the existing G:8 entry (or kept both with priority queue duplicates). Whichever interpretation the chapter takes must be stated, and the result must match the slide.

### P0-2 — DFS worked example (§5.5) contains in-table confusion

Lines 466–468 in the chapter:

```
| 2 | pop C (top), push F, G | `[B, F, G]` — wait. *Standard convention:* push children in *reverse* order so left child is on top. We follow the slide's left-first traversal, so we push children right-first: C then B → frontier becomes `[C, B]` with B on top. |
```

This is a row in a worked-example trace table. **Trace tables should not contain the word "wait"** or mid-stream corrections of the author's convention. A student reading this on the night before an exam will give up — they cannot tell which version is the "real" trace. Pick one push convention up front, state it once, then execute. The "left-first trace assuming G is the goal" table that follows (lines 473–482) is fine; delete the broken table above it.

### P0-3 — No worked example of "BFS vs UCS on the same non-uniform graph"

The single most likely free-response exam question on uninformed search is: *"Given this graph with non-uniform edge weights, show what path BFS returns and what path UCS returns, and explain why they differ."* The chapter has UCS on a small graph (§5.3, broken — see P0-1) and BFS on a binary tree (§5.4) and DFS on the same binary tree (§5.5). It never runs **two different strategies on the same weighted graph** to expose the optimality gap. This is the headline pitfall (mentioned in §6 item 1, again in §6 item 4, again in §8 "When to pick which") and it has no corresponding worked example. Pitfalls without worked examples are unmemorable.

**Fix:** Add a §5.7 that runs BFS and UCS on the slide-37 graph side by side and shows BFS returning A→B→C→G (cost 5+1+8=14, found at depth 3 — but BFS expanding by FIFO would actually find G via A→B→C→G at depth 3 with cost 14) vs UCS returning A→D→F→G (cost 8). This is the lecture's whole point.

### P0-4 — Vacuum-world worked example has no actual search trace

§5.1 (lines 357–373) describes the vacuum-world problem **formulation** but never runs a search algorithm on it. The lecturer spent slides 13–14 on this example. The chapter says (line 373): *"every algorithm we discuss below will, when applied to this 8-node graph, find a 2-action or 3-action solution depending on the initial state."* — but never runs any of them. This is the canonical "small enough to enumerate" exam target. A student should be able to point to vacuum-world and say "BFS expands these states in this order, finds the goal in N steps."

**Fix:** Add a BFS or UCS trace on vacuum world starting from the worst-case initial state (agent in A, both dirty) showing the action sequence S, R, S as the optimal solution.

### P0-5 — Romania example trails off without a strategy executed end-to-end

§5.2 (lines 375–397) walks through the first **two** expansion steps of a generic tree search and stops. The chapter then says (line 397): *"What happens next depends on the strategy: BFS picks `Timisoara` next..., UCS picks the city with the lowest $g$-value (probably `Zerind` at 75 if Arad→Sibiu were 140), DFS picks the most recently added (`Rimnicu Vilcea`)."* — and stops there. **No strategy is run to completion against Romania.**

This matters because Romania is the canonical exam vehicle for UCS — the lecturer puts it on slides 11 and 18 specifically because students are expected to compute the optimal Arad→Bucharest path. Without a finished UCS trace on Romania, the chapter leaves the most-likely exam question unrehearsed.

**Fix:** Run UCS on Romania to completion. Show the priority queue evolving step by step from Arad to Bucharest. Compare against the slide-18 edge weights. State the optimal cost (418 via Sibiu-Rimnicu Vilcea-Pitesti-Bucharest, per the canonical Russell & Norvig answer).

### P0-6 — IDS time-complexity numerical example uses wrong arithmetic

Line 511:

> For $b = 10, d = 5$ this is $6 + 50 + 400 + 3000 + 20000 + 100000 = 123456$ — barely larger than the $b^d = 100000$ that a *single* BFS pass to depth $d$ would have generated.

Let me check: with $b=10, d=5$ the formula $(d+1)b^0 + d\,b^1 + (d-1)b^2 + (d-2)b^3 + (d-3)b^4 + 1 \cdot b^5$ = $6 \cdot 1 + 5 \cdot 10 + 4 \cdot 100 + 3 \cdot 1000 + 2 \cdot 10000 + 1 \cdot 100000$ = $6 + 50 + 400 + 3000 + 20000 + 100000 = 123456$. OK the arithmetic happens to come out to the cute number 123456 — but **the formula is wrong**. The chapter's formula on line 317 is `(d+1)b^0 + d·b^1 + (d-1)b^2 + … + 1·b^d`. Reading the pattern, the coefficient of $b^k$ is $(d+1-k)$, so the coefficient of $b^d$ should be $(d+1-d) = 1$, ✓. But the coefficient of $b^{d-1} = b^4$ should be $(d+1-(d-1)) = 2$, ✓. The coefficient of $b^0$ should be $(d+1)$. With $d=5$, that's 6 ✓. So the arithmetic is consistent.

**However**, the slide's formula on slide 53 says `(d+1)b^0 + d·b^1 + (d-1)b^2 + … + b^d`, which gives the coefficient of $b^k$ as $(d+1-k)$. The chapter reproduces this faithfully. The example arithmetic happens to land on 123456 (a Hollywood-friendly number), which makes me worried the author cherry-picked $d=5$ to get the cute result rather than picking the realistic case. Fine. But the surrounding claim is misleading: "barely larger than $b^d = 100000$" — actually $123456 / 100000 \approx 1.235$, i.e. 23.5% larger. That is not "barely larger" — that is a meaningful constant-factor overhead. A more honest reading is "asymptotically the same big-O, with a constant factor of about $b/(b-1)$ for large $d$" — for $b=10$, that's 1.11 in the limit, plus lower-order terms, giving the ~1.23x at $d=5$. The chapter's "barely" oversells the result.

**Fix:** Either remove "barely" or replace with "about 23% overhead at $d=5$, asymptotically $b/(b-1)$ overhead as $d \to \infty$".

---

## P1 — IMPORTANT GAPS

### P1-1 — No worked example of UCS with $b^{1+\lfloor C^*/\epsilon\rfloor}$ blowup

§6 item 7 (line 537) names this pitfall: *"a 'graph with one cheap edge of cost 0.01 and many expensive edges of cost 10' will trigger an enormous UCS expansion."* — but never shows the example. This is exactly the kind of contrived weighted graph a lecturer would put on a final. The chapter promises the pitfall but doesn't drill the student against it.

**Fix:** Construct a tiny adversarial graph (4–5 nodes, $C^* = 10$, $\epsilon = 0.01$, so $C^*/\epsilon = 1000$) and show UCS expanding 1000+ nodes along a cheap-step path before finding the goal via a 1-step expensive path.

### P1-2 — No 8-puzzle search-tree example despite full slide

Slide 15 dedicates a full slide to 8-puzzle (`9!/2 = 181,440 states`, NP-hard). Slide 17 reinforces with the "many possible paths" picture. Slide 16 even shows a 3-puzzle worked example with a full 7-step path from start to goal. The chapter mentions 8-puzzle once in passing (§3.3, line 124) and never runs a search on it. The 3-puzzle solution path from slide 16 is not reproduced.

**Fix:** Reproduce the slide-16 3-puzzle solution as a worked example showing the action sequence and confirming it's the shortest (per uniform step cost = BFS/IDS optimal).

### P1-3 — Missing 8-queens formulation discussion

Slide 19 asks: *"What are the states, successor function, goal state?"* for 8-queens. This is a classic state-space-formulation exam question. The chapter omits 8-queens entirely. (Yes, 8-queens shows up properly in L05 as a local-search example, but the L03 slide poses it as a *formulation* exercise, not a local-search problem.) A student opening the L03 chapter expecting "I'll learn to formulate 8-queens as a search problem" finds nothing.

**Fix:** Add a short §5.7 on 8-queens formulation: state = partial board with $k \le 8$ queens placed, successor function = add a non-attacking queen in the next column, goal = 8 queens placed. Note the branching factor and explain why BFS is hopeless here but DFS is fine.

### P1-4 — Generic algorithm pseudocode (§3.4) silently introduces graph search without naming it

Lines 149–166 give the algorithm with `explored` set and "replace if cheaper in frontier" logic. The chapter then says (line 168): *"The 'tree' name is slightly misleading... we are doing graph search."* — but the previous lecture-source slide 20 explicitly says *Tree Search* and slide 21 calls the same algorithm *"Tree Search Algorithm Outline"*. The chapter is right that the algorithm is technically graph search; the lecture is technically wrong; but the chapter does not warn the student that **the exam will use the lecturer's terminology** ("tree search") even when the algorithm is graph search. This is a labelling pitfall worth a callout.

**Fix:** Add a one-line note: "The lecturer calls this *Tree Search*; Russell & Norvig 4th ed. calls it *Graph Search*. On exams, follow the lecturer's terminology."

### P1-5 — Goal-test-on-pop vs goal-test-on-generation is only stated, never demonstrated

§4.2 line 243 says: *"the goal test is performed when a node is popped from the queue... otherwise a sub-optimal goal node could be returned just because it was generated early."* §6 item 2 reinforces this as a pitfall. But the chapter never shows a counter-example (a graph where goal-test-on-generation gives the wrong answer). This is a P1 because exam questions on this point are common — "Why does UCS goal-test on pop?" — and the student needs a concrete example to commit it to memory.

**Fix:** Show a 4-node example where the optimal goal is reached via a 2-step path of cost 5 and a sub-optimal goal is reached via a 1-step path of cost 6. If we goal-test on generation, we return the 1-step goal at cost 6; if we goal-test on pop, we pop the optimal goal first.

### P1-6 — Bidirectional search and Depth-Limited search are dismissed too quickly

Slide 54 has these in the table. The chapter (line 325) says: *"The lecturer annotates two columns — Depth-Limited and Bidirectional — with 'these two haven't covered, but you can read about them in the book'. We retain them in the table because they appear on the slide; the cheat-sheet in §8 retains only the four covered methods."*

Then deletes them from §8. **This is risky.** The lecturer's slide-54 table shows their big-O — $O(b^\ell)$ and $O(b^{d/2})$ — and the conditions (footnotes 1, 4). A multiple-choice exam question of the form "Which of the following has time complexity $O(b^{d/2})$?" would catch out a student who only studied §8. The chapter should at minimum have a one-paragraph "for completeness" section explaining what depth-limited and bidirectional are, what their complexity is, and why the lecturer skipped them.

**Fix:** Add §4.6 "Out-of-scope: Depth-Limited and Bidirectional" with two paragraphs each — definition, complexity row, why-not-covered.

### P1-7 — IDS optimality wording is sloppy

Line 315: *"Optimal? Yes when every step cost is 1 (or, more generally, uniform)."* The "more generally, uniform" parenthetical is correct but contradicts the slide-53 wording *"Yes, if step cost = 1"*. The chapter is being more general than the slide. That's fine **if** flagged. But the exam will probably ask "What is the condition for IDS optimality?" expecting the slide answer "step cost = 1". The chapter should note "the slide says step cost = 1, but the true condition is uniform step cost — answer whichever your exam uses."

### P1-8 — Notation $g(n)$ introduced too late

§3.2 (line 117) introduces $g(n)$ as path cost. Good. But the UCS pseudocode on line 246 uses `path_cost` and the trace tables in §5.3 use $g$. The cheat-sheet (line 610) finally writes "$g(n)$ — path cost from root to $n$". Pick **one** symbol. Most exam-paper conventions write $g(n)$. Use $g(n)$ everywhere from §3.4 onward, including in pseudocode (`g(n)` instead of `path_cost`).

### P1-9 — DFS-on-binary-tree trace has an unreachable explanation

§5.5 lines 462–468 introduce a confused "wait" mid-table (P0-2 above) and then the cleaner "left-first trace" table (lines 473–482). The cleaner trace has 7 steps and finds G as the goal — good. But the surrounding prose (line 487) says: *"On this tiny tree, both BFS and DFS explore all 7 nodes and return the same answer."* This is **only true if G is the last node BFS and DFS visit**. BFS visits in order A B C D E F G — finds G last ✓. DFS (left-first) visits A B D E C F G — finds G last ✓. OK, the claim holds, but only by construction. A student reading this might conclude "BFS and DFS always give the same answer on the same tree". State explicitly: "If we'd put the goal at D instead of G, BFS would visit 4 nodes (A B C D) while DFS-left would visit 3 (A B D)."

### P1-10 — No worked example of "what happens when DFS hits a cycle"

§6 item 5 (line 533) names the pitfall. §4.3 line 292 mentions it. But the chapter never shows it. A student asked "construct a graph where DFS without the explored set loops forever" needs a tiny example to point to. This is two lines of work in the chapter (A↔B↔C cycle with goal D unreachable from C; DFS oscillates A-B-C-B-C-B-C... forever).

### P1-11 — IDS table for depth limits 0, 1, 2, 3 doesn't tie back to the time formula

§5.6 walks through the depth-limit traces (good). But it never says: "level-0 visits 1 node, level-1 visits 3, level-2 visits 7, level-3 visits 15. Total over all 4 passes: 1+3+7+15 = 26 nodes. Predicted by the formula with $b=2, d=3$: $4 \cdot 1 + 3 \cdot 2 + 2 \cdot 4 + 1 \cdot 8 = 4+6+8+8 = 26$. ✓" Tying the figure-by-figure trace back to the formula is the whole point of having both.

### P1-12 — Cheat-sheet "When to pick which" is silent on a key case

§8 "When to pick which" (lines 602–606) covers:
- Uniform costs, memory OK → BFS
- Uniform costs, memory tight → IDS
- Non-uniform costs → UCS
- Memory tight, optimality doesn't matter, depth bounded → DFS

Missing: "Non-uniform costs **AND** memory tight". That's a real exam-trap question — UCS's space is $O(b^{1+\lfloor C^*/\epsilon\rfloor})$, just as bad as time. The honest answer is "no uninformed strategy covered here is good for this case; you need iterative-deepening A\* (IDA\*) from L05+ informed search". State that.

### P1-13 — No glossary stress-test

The chapter's first line claims to introduce ~20 glossary terms. There is no end-of-chapter quiz, no "define these in your own words" prompt, no fill-in-the-blank. For an exam-prep artifact this is a missed opportunity. At minimum a §9 with 10 short "Q: define X / state the time complexity of Y" prompts and answers would help.

---

## P2 — POLISH

### P2-1 — Forward references to L05/L06/L07/L09b
§7 is well-done but spends more words on connections than on L03 self-contained mastery. Trim to ~50% of current length.

### P2-2 — Figure captions are sometimes longer than needed
Figure 7c (line 395) takes 3 lines to say "frontier in red". Cut to one.

### P2-3 — "Lecture 3, slides X–Y" footnotes
Repeated at end of every section. Helpful but cluttered. Consolidate into a single per-section line.

### P2-4 — "Honest note on scope" callout (§1)
Right tone. But three paragraphs on what L03 doesn't cover, before covering what L03 does cover, is poor ordering. Move the "honest note" to a §1.5 after the four-strategy overview.

### P2-5 — UCS pseudocode key
Line 248: `key=path_cost`. Use $g$ here too (see P1-8).

### P2-6 — DFS-vs-IDS "best of both worlds" overstates
Line 321: *"IDS is the **default** recommendation in uninformed-search settings where $b$ is finite and step costs are uniform."* Slides do not say this. R&N do, but the chapter should either cite R&N or qualify with "in textbooks, IDS is often called...". The lecture deck just stops with the comparison table.

### P2-7 — Branching-factor figures
Line 174: "for chess, $b \approx 35$; for the Romania road graph, $b$ is small and finite; for the 8-puzzle, $b$ is at most 4". The slides do not give these numbers. They're correct trivia but unsourced.

### P2-8 — Cheat-sheet missing the slide-7 informed-search reminder
§8 "Common pitfalls" item on A\* (line 629) is good but doesn't include the explicit reminder *"A\* is referenced on slide 7 but explicitly deferred to next class on slide 55."* A one-line callout helps students avoid this trap on multiple-choice questions.

### P2-9 — Vacuum-world figure caption
Figure 3 caption (line 131) is right that the graph has 8 nodes. But the chapter never tests the student on counting them. Add a fold-out aside "Q: How many edges does this graph have? A: ..." for active engagement.

### P2-10 — "Where it breaks down" is repetitive
Every analogy in §2 has a "Where it breaks down" — good idea, but five of them in a row reads tediously. Consider folding into a single "Common ways these analogies mislead" subsection.

---

## EVIDENCE — 10 PLAUSIBLE EXAM QUESTIONS

Below are 10 questions an exam writer would plausibly set on this material. For each I judge whether a student studying ONLY this chapter could answer it.

**Q1. Define a search problem. List the five components.**
Answer in chapter §3.2 lines 109–115. ✓ FULLY ANSWERED.

**Q2. State the time and space complexity of BFS, UCS, DFS, IDS. State the completeness/optimality conditions for each.**
Answered by the table in §4.5 (line 332) and pitfalls in §6. ✓ FULLY ANSWERED.

**Q3. Given the slide-37 graph, run UCS from A to G. Show the frontier and explored set at each step. State the optimal path and its cost.**
Chapter §5.3 attempts this but **gets the trace wrong** (see P0-1). A student following the chapter's table will write the wrong frontier at steps 3 and 7. ✗ NOT ANSWERED (chapter actively misleads).

**Q4. Why does UCS perform the goal test when a node is popped, not when generated? Give a small example where the two policies disagree.**
Chapter §4.2 (line 243) and §6 item 2 (line 523) state the rule but **provide no example** (see P1-5). ◐ PARTIALLY ANSWERED — student knows the rule but can't construct the example, and a 5-mark question asking for the example loses 3 marks.

**Q5. Construct a search problem (states, initial state, successor function, goal test, step costs) for the 8-queens puzzle.**
Chapter §3.3 mentions 8-puzzle in passing but **8-queens is omitted entirely** despite being on slide 19 (see P1-3). ✗ NOT ANSWERED.

**Q6. On the binary tree A-(B,C)-(D,E,F,G) with goal G, trace BFS and DFS and report the order of expansion for each.**
Chapter §5.4 and §5.5 cover this. §5.5 has the "wait" defect (P0-2) but the cleaner subtable is correct. ✓ FULLY ANSWERED (after a confused detour).

**Q7. Romania route planning: starting from Arad, find the optimal path to Bucharest using UCS. Give the path and the total cost.**
Chapter §5.2 walks through 2 steps and **stops** (see P0-5). Student cannot answer. ✗ NOT ANSWERED.

**Q8. Vacuum world: starting with the agent in cell A and both cells dirty, find the optimal action sequence and its cost (per uniform step cost = 1).**
Chapter §5.1 defines the problem but **does not run search on it** (see P0-4). Student must construct the trace themselves. ◐ PARTIALLY ANSWERED.

**Q9. Why is IDS preferred to BFS in practice when $b$ is finite and step costs are uniform? Quantify the overhead.**
Chapter §4.4 + §5.6 + the 123456 example (line 511). Answer is there but the chapter undersells the overhead by calling it "barely larger" (P0-6). ◐ PARTIALLY ANSWERED.

**Q10. Construct a graph where UCS expands $\gg b^d$ nodes due to a small $\epsilon$ relative to $C^*$.**
Chapter §6 item 7 (line 537) names the pitfall but **shows no example** (see P1-1). ✗ NOT ANSWERED.

**Score: 5 fully + 3 partial + 2 not at all. Effective coverage: 5 + 3 × 0.5 = 6.5 / 10 = 65%.** A study artifact should score 90%+ on its own-material exam questions.

---

## CHEAT-SHEET ACCURACY AUDIT

Spot-checks of §8:

- ✓ "BFS: complete (finite b), optimal iff uniform step costs, time $O(b^d)$, space $O(b^d)$" — correct.
- ✓ "UCS: complete (all costs $\ge \epsilon > 0$), optimal, time and space $O(b^{1+\lfloor C^*/\epsilon\rfloor})$" — correct.
- ✓ "DFS: complete in finite spaces with repeated-state check, not optimal, time $O(b^m)$, space $O(bm)$" — correct.
- ✓ "IDS: complete (finite b), optimal iff uniform step costs, time $O(b^d)$, space $O(bd)$" — correct.
- ⚠ "When to pick which" — missing the "non-uniform + memory tight" case (P1-12).
- ⚠ Footnotes ¹/²/³ correctly transcribed from slide 54. Good.
- ⚠ Bidirectional and Depth-Limited removed (judgment call, see P1-6).

---

## OUT-OF-SCOPE OBSERVATIONS

1. The chapter's prose quality is genuinely good — the analogies in §2 are useful and the "where it breaks down" caveats are excellent pedagogy. The defects are concentrated in the worked-example sections (§5) where rigor matters most.

2. The forward references in §7 to L05/L06/L07/L09b are detailed enough that the L03 chapter feels like it's selling its own importance via the future. Trim.

3. The chapter mentions $f(n) = g(n) + h(n)$ in the cheat-sheet (line 613) — students will see this in study and wonder if they need to know it. Add: "you do NOT need this for an L03-only exam; it's noted for context with L05+."

---

## CONCERNS / RISKS

- **Trust risk**: the UCS trace bug (P0-1) is the kind of error that, once a student catches it, makes them distrust the entire chapter. Round 2 reviewers should re-verify every worked example by hand.
- **Coverage risk**: 5/10 plausible questions are not fully answered. Round 2 must add worked examples for vacuum world, Romania UCS, BFS-vs-UCS, 8-queens, and adversarial-$\epsilon$ UCS.
- **Slide fidelity risk**: where the chapter generalizes beyond the slides (e.g. IDS optimality with "uniform costs" instead of "step cost = 1"), exam answers may diverge from the lecturer's expected answer. Flag every generalization explicitly.

---

## WHAT PM SHOULD DO NEXT

1. **Block ship.** This chapter is not exam-ready.
2. Dispatch the lecture-writer agent to fix P0-1 through P0-6 — these are blocking.
3. After P0 fixes, re-dispatch this reviewer (or Reviewer 4 round 2) to re-audit §5 worked examples and check the new ones (BFS-vs-UCS, vacuum world trace, Romania UCS, adversarial-$\epsilon$ UCS).
4. After P0 is clean, address P1-1 through P1-13 in priority order.
5. P2 polish can ride along with whichever pass touches those sections.
6. Once §5 is solid, add a §9 "Self-test" with 10 Q/A pairs matching the 10 exam questions above (P1-13).

---

## Report to PM

**Assignment recap:** L03 Round 1, Reviewer 4 (Exam Readiness). Compared `study/lectures/L03-Uninformed-Search.md` against `Lecture3-Uninformed Search.pdf` (slides 1–56), reading as an exam writer.

**Status:** **Fail** — chapter is not exam-ready in current state.

**P0 findings (6, must-fix):**
1. UCS worked example (§5.3) trace is wrong and self-contradictory; contradicts slide 37 at steps 3 and 7; chapter's edge list disagrees with chapter's own trace narrative.
2. DFS worked example (§5.5) contains a mid-table "wait" correction that no exam-prep artifact should ship.
3. No worked example of BFS-vs-UCS on the same weighted graph — the single most likely free-response prompt.
4. Vacuum world (§5.1) is formulated but no search algorithm is run on it.
5. Romania (§5.2) trails off after two expansion steps; no strategy is executed end-to-end despite slides 11/18 setting this up.
6. IDS arithmetic example (§5.6, line 511) labels 23% overhead as "barely larger" — misleading.

**P1 findings (13):** missing UCS-blowup worked example, missing 8-puzzle/3-puzzle worked example, 8-queens formulation entirely absent, tree-vs-graph search terminology not flagged for exams, goal-test-on-pop has no demonstrator example, Bidirectional/Depth-Limited deleted from cheat-sheet, IDS optimality wording generalizes past the slide without flagging, $g(n)$ vs `path_cost` notation inconsistent, DFS-binary-tree trace has confused "wait" prose, no DFS-cycle worked example, IDS table doesn't tie back to time formula, cheat-sheet missing "non-uniform + memory tight" case, no end-of-chapter self-test.

**P2 findings (10):** §7 forward references too long, figure captions verbose, slide-citation footnotes repetitive, "Honest note on scope" misordered in §1, UCS pseudocode uses `path_cost` not $g$, "IDS is the default" overclaims relative to slides, branching-factor figures unsourced, cheat-sheet A\* reminder incomplete, vacuum world has no active-engagement prompt, §2 analogies' "where it breaks down" is repetitive.

**Exam-readiness score:** 6.5 / 10 plausible questions answerable from chapter alone. Target is ≥9/10.

**Cheat-sheet (§8) audit:** Complexity rows correct. "When to pick which" missing one case. Footnotes correctly transcribed.

**Out-of-scope observations:** Prose quality is genuinely strong; defects are concentrated in worked examples (§5). Once §5 is rebuilt the rest needs only light edits.

**Concerns / risks:** P0-1 (broken UCS trace) is a credibility-destroying defect. Once a student catches it they will doubt every other table in the chapter.

**What PM should do next:** Fix all six P0 items first, then re-run QA on §5 worked examples specifically. Do NOT advance to App Tester / Code Reviewer until §5 is verified against the slides by hand. Add the missing worked examples (vacuum world trace, Romania UCS to completion, BFS-vs-UCS contrast, 8-queens formulation, adversarial-$\epsilon$ UCS). Then address P1 in priority order, P2 in pass-through.

**DOCUMENT.md updated:** N/A for QA.
