# L03 — Uninformed Search — Round 2 — Reviewer #3 (Pedagogical Clarity incl. Analogies)

**Source:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture3-Uninformed Search.pdf` (56 slides)
**Draft under review:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L03-Uninformed-Search.md` (804 lines, ~60 min)
**Round 1 review:** `study/_review/L03/round1/reviewer3.md` (3 × P0, 8 × P1, 8 × P2)
**Revise summary:** `study/_review/L03/round1/revise-summary.md`
**Lens:** Pedagogical clarity. Read as a confused student. Every major concept must have a concrete everyday analogy in §2 with a "where it breaks down" caveat, cross-linked from §3.
**Disposition:** Harsh. False positives are cheap.

---

## VERDICT: **PASS WITH CONCERNS**

The three Round-1 P0 issues are now resolved cleanly. §5.3 has been rebuilt against slide 37 with a clean edge-list table and a step-by-step trace that matches the slide line-for-line; the chapter even reconciles the slide's step-7 `G:14` vs the algorithm's `G:8` with an honest pedagogical note. §5.5 DFS has been rewritten as a single clean 8-row table with a one-sentence convention header — no more "wait." leakage. §3.4 now teaches the tree-search vs graph-search distinction inside a proper callout box. Most Round-1 P1 items are addressed; §4.4.0 promotes depth-limited DFS to a named subroutine with the three return values; §5.2.2 commits to actual successor picks rather than conditional speculation; transition-model orphan is removed from §3.2; cheat-sheet analogies are added.

The reason this verdict is *Pass with concerns* and not *Pass* is one **new** P0 regression that was introduced by the round-1 revise (specifically the newly added §5.1.1 BFS trace contains the *exact same* "thinking-aloud mid-table" pattern that was the round-1 P0-2 defect — only this time in the BFS trace, not the DFS trace). The reviser fixed one instance of the defect class while introducing a fresh instance one section earlier. Two residual P1 cleanups (glossary-list inconsistency, §3.8 admissibility/consistency wording) round out the report.

I would mark this Approved if §5.1.1 step 1 were cleaned up in a follow-up touch-up edit.

---

## P0 — MUST FIX (blocks approval)

### P0-1. The newly added §5.1.1 BFS trace replays the exact "thinking-aloud" pattern that round-1 flagged in §5.5 DFS.

**Where:** `study/lectures/L03-Uninformed-Search.md` §5.1.1, Step 1 of the vacuum-world BFS trace (line 466).

**What's broken:** Step 1 of the trace reads, verbatim:

> *"pop `(A,1,1)`, not goal. Expand: $L$→`(A,1,1)`(no-op, skip — self-loop already in frontier? actually new, in explored after pop), $R$→`(B,1,1)`, $S$→`(A,0,1)` | `[(B,1,1), (A,0,1)]` | `{(A,1,1)}`"*

The parenthetical *"self-loop already in frontier? actually new, in explored after pop"* is the author hesitating in writing — asking themselves a question and then answering it mid-row. This is the textual equivalent of crossing out work on the board. It is *identical in flavour* to the round-1 P0-2 defect in §5.5 ("— wait. *Standard convention:* …"), which the reviser correctly removed in §5.5 but accidentally re-introduced in this new §5.1.1.

Worse, the parenthetical is not even self-consistent: it asks "already in frontier?", then answers "actually new", then settles on "in explored after pop" — three different reasons for skipping the $L$ child are floated in 14 words, only the last of which is the actual algorithmic reason. A confused student reading this *cannot tell which reason to write on the exam*.

**Why this matters pedagogically:** §5.1.1 is the *first* worked example in the chapter and the *first* trace a student will read. If the very first row of the very first trace exposes the author thinking in three competing voices, the student loses confidence in the chapter before they reach §5.3. The defect class is exactly what Reviewer #3 is supposed to catch.

**Suggested fix:** Rewrite step 1 as a clean single-voice row, identical in style to the now-clean §5.3 step 3:

> *"pop `(A,1,1)`, not goal. Expand: $L$→`(A,1,1)` (already in explored, skip), $R$→`(B,1,1)`, $S$→`(A,0,1)`. | `[(B,1,1), (A,0,1)]` | `{(A,1,1)}`"*

That is the same algorithmic statement with one chosen reason ("already in explored") and no in-line hesitation. The fix is a 1-line edit; no other rows of §5.1.1 are affected.

---

## P1 — SHOULD FIX (requested, not blocking)

### P1-1. The "Glossary terms introduced" line in the chapter header still lists `transition model (search)` even though §3.2 no longer introduces or uses the term.

**Where:** Line 4 of `study/lectures/L03-Uninformed-Search.md`.

**What's broken:** The Round-1 revise correctly removed the orphan `transition model` / `Result(s, a)` parenthetical from §3.2 (per Round-1 P1-4). But the glossary-terms-introduced list at the top of the chapter still advertises `transition model (search)` as a term this chapter introduces. A student who jumps to the glossary expecting to find an L03 entry on transition model will be confused — and a reader who reads top-to-bottom now sees a header promise that the body does not deliver. Either re-introduce the term meaningfully in §3.2 (the reviser deliberately chose *not* to do this, correctly, since the slides don't use it), or remove the term from the header list.

**Suggested fix:** Delete `transition model (search), ` from line 4. One token deletion.

### P1-2. §3.8 still names "admissibility" and "consistency" — round-1 P1-3 asked for them to live only in the glossary.

**Where:** §3.8 line 254, and §7 forward-reference list line 735.

**What's broken:** Round-1 P1-3 asked that admissibility and consistency be moved to the glossary's A\* entry and removed from L03's running text. The reviser trimmed §3.8 to a single paragraph but the paragraph still contains the parenthetical *"the conditions on $h$ that make those guarantees hold (admissibility, consistency)"*. §7 similarly mentions both terms in its forward-reference bullet. A student reading §3.8 sees two new bolded-by-context concept names and now believes (a) these were introduced in L03 and (b) they're testable here.

Mitigation: the §3.8 paragraph does explicitly say *"You do not need these conditions for an L03-only exam"*, so the damage is bounded. But the round-1 fix was specifically *delete the names*, not *include them with a disclaimer*. The right move is to push the term list entirely into the glossary entry.

**Suggested fix:** Replace the §3.8 parenthetical with *"plus conditions on $h$ (covered in L05)"*. Drop the explicit terms here. Keep the §7 mention but reword to *"properties of $h$ that condition A\*'s optimality"* without naming admissibility/consistency.

### P1-3. §4.2.1 (goal-test-on-pop counter-example) under-specifies the PUSH-test order.

**Where:** §4.2.1, the "Goal-test on PUSH (wrong)" case.

**What's broken:** The counter-example asserts that goal-test-on-push *returns the 6-cost path immediately* in the second weight assignment. This is only true if the successor function returns $G_1$ in S's expansion *before* (or co-equal to) testing on $A$. If the implementation generates $A$ first and tests it (not a goal, push), then generates $G_1$ and tests it (goal, return), the PUSH-test version returns cost-6 — fine. But if a student writes their pseudocode such that successors are batched and the algorithm proceeds to pop after pushing all successors, then PUSH-test fires on whichever goal is *generated* first regardless of cost — which may or may not be $G_1$ depending on iteration order. The chapter doesn't surface this.

The example is *correct enough* for the pedagogical point — if the lower-cost path goes through a non-goal intermediate node, PUSH-test cannot defer to expansion ordering and will return whichever goal is generated first. But making this premise explicit ("assume children are generated in declaration order") would lock the example down.

**Suggested fix:** Add one sentence at the top of §4.2.1: *"Assume the successor function returns children in declaration order: $G_1$ then $A$."* Then the trace is unambiguous.

### P1-4. §5.3 step-7 pedagogical note is good but the "what to write on the exam" ladder is buried under the slide-vs-algorithm reconciliation.

**Where:** §5.3, the blockquote after the step-7 trace row (lines 566–568).

**What's broken:** The reconciliation paragraph is correct and honest, but the *student-facing* takeaway ("If asked to reproduce the slide, write `G:14` for step 7 (matches the slide). If asked to explain UCS, write `G:8` is retained (matches the algorithm). If asked which path is optimal, the answer is $A \to D \to F \to G$, cost 8") is at the end of a long paragraph. A student skimming under exam pressure would benefit from this ladder being the *first* sentence of the note, not the last.

**Suggested fix:** Swap the paragraph order: lead with the three-line exam ladder, then explain *why* there's a discrepancy. Same content; better signal-to-noise for the reader who's reading at 200 wpm because the exam is tomorrow.

### P1-5. §5.7 BFS-vs-UCS contrast tie-breaks on "left-to-right child ordering matching the edge list" but the edge list isn't ordered left-to-right.

**Where:** §5.7, the BFS analysis.

**What's broken:** The chapter says *"With left-to-right child ordering matching the edge list (B before D from A, so $A \to B \to C \to G$ is generated first)"*. The edge list in §5.3 puts $A \to B = 5$ before $A \to D = 3$, so "B before D from A" matches the edge list — fine. But the slide-37 graph picture itself has D *below* B (i.e. B is the top-right child of A, D is the lower-left). A student looking at Figure 8 and trying to apply "left-to-right child ordering" can't see a left-to-right ordering visually; they need to be told *which* ordering convention generates the cited result.

The point of §5.7 is to nail the BFS-vs-UCS difference, not to wade through FIFO tie-breaking. The current text gets the *right answer* (BFS returns cost 14 because $A \to B \to C \to G$ is generated first in row-order), but it gets there via a vague convention reference.

**Suggested fix:** Replace *"With left-to-right child ordering matching the edge list"* with *"with children pushed in edge-list order (B before D when expanding A; C is the only child of B; G the only child of C)"*. Same information, but anchored on the edge-list table the student can actually re-read.

### P1-6. §3.4 tree-vs-graph callout is correct but doesn't actually answer the "why does it matter for exams" question that Round-1 P0-3 asked for.

**Where:** §3.4 callout box (lines 213–219).

**What's broken:** The callout defines tree search, graph search, identifies which the pseudocode implements, and notes the lecturer's terminology. Good. But the "why the difference matters" sentence — *"the explored set blocks re-expansion of finished states; the frontier-dedup check keeps only the cheapest known path to each state still on the frontier"* — is the *mechanism*, not the *consequence*. The consequence the student needs is: *"pure tree search in a cyclic state space can re-generate the same state many times, blowing time complexity from $b^d$ to something potentially unbounded."* That is what makes graph search exam-critical.

The current callout gets the mechanism right but leaves the student wondering *why I'd ever care*. The round-1 P0-3 suggested fix asked for "why the difference matters in finite cyclic state spaces" — the current callout has the *promise* of this but answers it as "this is what every reasonable implementation does", which is the opposite of motivation.

**Suggested fix:** Append one sentence: *"Without the explored set, pure tree search in a graph with cycles can re-expand the same state from every distinct path leading to it — exponentially many in the worst case — turning a finite state-space search into an infinite tree-search."*

---

## P2 — NICE TO HAVE

### P2-1. §5.6.1 IDS arithmetic table is correct; one cosmetic suggestion.

The level-by-level table is exactly the kind of pedagogical scaffolding Round 1 P1-11 (Reviewer #4) asked for and the chapter's revise summary reported as deferred — actually it's been delivered. Bonus. The only nit: the column heading "coefficient $(d+1-k)$" could be re-labelled "level multiplier" to make it more obviously a real-world quantity (how many times level $k$ is visited across all IDS passes) rather than an abstract algebra term.

### P2-2. §2.5 IDS analogy is still the weakest of the six.

The IDS analogy *"do a depth-first search but only let yourself go to depth 1. Find nothing? Throw away everything you've remembered and do a depth-first search to depth 2"* is correct but it's a paraphrase of the algorithm rather than an everyday picture. The round-1 P2-1 suggested a "rehearsal" image (each pass is a rehearsal that goes one beat deeper); the reviser opted to keep the algorithm-paraphrase form. Not a blocker; consider for a future polish round.

### P2-3. §5.3.1 counterfactual is good but the new edge $E \to F$ feels invented.

The counterfactual "*suppose later we discovered a cheaper alternative: an edge $E \to F$ with cost $1$*" introduces an edge that doesn't exist in the slide-37 graph. The point of the counterfactual — to show the replace-if-cheaper rule firing — would be clearer if the chapter built a tiny standalone 4-node graph specifically for this purpose, rather than perturbing the canonical example. Cosmetic.

### P2-4. §5.2.2 Romania UCS trace says "Pop Zerind(75)" then "Generate Oradea(146 via Zerind=75+71)" — but Zerind's other neighbour is Arad', which the trace says "(skip, in explored)". This is correct, but a footnote noting that Zerind's only non-skipped neighbour is Oradea would tighten the row.

Optional; the trace is internally correct.

### P2-5. The cheat-sheet "When to pick which" bullets now include the "Non-uniform step costs + memory tight" case pointing at IDA\* — good. One small unevenness: the four bullets vary between "→ X" (terse) and "→ X. (sentence with explanation.)" — the IDA\* row is the only one with two sentences. Tighten for parallelism.

### P2-6. §5.8 (8-queens formulation) is a strong addition and earns its keep. No defect from this lens; flagging positively.

### P2-7. §3.3.1 n-Puzzle state counts (8-puzzle = 181,440, 15-puzzle > 10¹³, 24-puzzle ≈ 10²⁵, NP-hardness) is a clean addition. The factor-of-2 explanation ("exactly half of the $9!$ tile arrangements are reachable from any given starting configuration") is a nice touch — slide 15 doesn't actually explain this; the chapter does. Good pedagogical decision.

### P2-8. The chapter is now 804 lines / ~60 min. At the long end. The cheat sheet in §8 substantially mitigates this. Verify with App Tester that §8 alone is exam-sufficient.

---

## VERIFICATION: each Round 1 finding checked against round-2 draft

### Round 1 P0s — verification

| Finding | Round 1 defect | Round 2 status | Notes |
|---------|----------------|----------------|-------|
| **P0-1** | §5.3 UCS trace corrupt (ASCII graph, step-3 thinking-aloud, step-7 mismatch with slide) | **FIXED** | Edge-list table replaces ASCII; step 3 rewritten as one declarative sentence; step 7 reconciled with slide via honest pedagogical note. Trace matches slide 37 line-by-line. |
| **P0-2** | §5.5 DFS table has "wait. *Standard convention:*" mid-row, then a second table below | **FIXED** | First broken table deleted; single clean 8-row trace; one-sentence convention header above the table. |
| **P0-3** | §3.4 tree-vs-graph distinction named but not taught | **MOSTLY FIXED** | Callout box added defining tree search vs graph search, identifying which the pseudocode implements, and noting the lecturer's terminology. The "why it matters" motivation is implicit (see P1-6 above for a small polish). |

### Round 1 P1s — verification

| Finding | Round 2 status |
|---------|----------------|
| **P1-1** depth-limited DFS undefined | **FIXED.** §4.4.0 defines DL-DFS as a named subroutine with three return values (solution / failure / cutoff) and complexity. |
| **P1-2** Romania step-2 conditional speculation | **FIXED.** §5.2.1 commits to BFS=Timisoara, UCS=Zerind(g=75), DFS=Rimnicu Vilcea with explicit anchoring to the data structure. |
| **P1-3** §3.8 leaks admissibility/consistency | **PARTIALLY FIXED.** §3.8 trimmed to one paragraph with the L05 disclaimer, but admissibility/consistency are still named in line 254. See round-2 P1-2 above. |
| **P1-4** transition model orphan | **PARTIALLY FIXED.** Body removed; header glossary-terms-introduced list still lists it. See round-2 P1-1 above. |
| **P1-5** maze "where it breaks down" undersells "agent doesn't move" | **FIXED.** §2.1 caveat now reads *"This is the same point slide 9 captures with 'close his/her eyes!' — once the plan is committed, the agent executes blind"* and cross-links forward. |
| **P1-6** cheat-sheet drops analogies on Setup/Search-tree rows | **FIXED.** §8 now has italic analogies for frontier (to-do list), explored set (already done list), branching factor (corridors per junction), problem-solving agent (closes eyes once plan fixed). |
| **P1-7** UCS pseudocode doesn't surface goal-test-on-pop | **FIXED.** §4.2 pseudocode has the inline `# UCS-SPECIFIC: test on POP, not on push` comment, *and* §4.2.1 adds a full 4-node counter-example. The latter exceeds what was asked. |
| **P1-8** replace-if-cheaper rule never illustrated firing | **FIXED.** §5.3.1 counterfactual shows the rule firing with explicit $D\to F = 4$ and $E \to F = 1$. (See round-2 P2-3 above for a cosmetic suggestion.) |

### Round 1 P2s — verification

| Finding | Round 2 status |
|---------|----------------|
| **P2-1** Grocery-cart and IDS analogies weak | **PARTIALLY FIXED.** UCS analogy replaced with Dijkstra wavefront — clean improvement. IDS analogy still in algorithm-paraphrase form (see round-2 P2-2). |
| **P2-2** Add slide refs on "Idea." lines | Not addressed; chapter editor's discretion. |
| **P2-3** Cheat-sheet decision tree as flowchart | Not addressed; bullets remain. |
| **P2-4** §6 pitfall #7 graph drawing | **PARTIALLY FIXED.** Pitfall #7 now has explicit numerics ($C^*=9.99, \epsilon=0.01, C^*/\epsilon=999$) but still no drawing. Numbers are vivid enough. |
| **P2-5** HMM-Viterbi forward link | Not addressed; remains in §7. |
| **P2-6** §1 honest-scope note | Preserved. Good. |
| **P2-7** Figure 7c duplicate-Arad as inline | **FIXED.** §5.2.1 step 1 now mentions *"Notice the duplicate 'Arad' in the tree — that's why we need the repeated-state check"* inline above the figure. |
| **P2-8** Reading-time / cheat-sheet sufficiency | Reading time now ~60 min; verify with App Tester. |

---

## EVIDENCE — what I read

**Files inspected:**
- `study/_review/L03/round1/reviewer3.md` (Round 1 report, 267 lines)
- `study/_review/L03/round1/revise-summary.md` (revise summary, 211 lines)
- `study/lectures/L03-Uninformed-Search.md` (revised chapter, 804 lines)
- `study/extracted_figures/L03/fig24-ucs-worked-example.png` (slide 37 image — line-by-line verification of §5.3 trace)

**Slide-37 verification (re-done from scratch against `fig24-ucs-worked-example.png`):**

| Slide step | Chapter row | Match? |
|------------|-------------|--------|
| Step 1: Fringe A:0, Explored – | Step 1: `A : 0`, Explored – | ✓ |
| Step 2: Expand A, Fringe D B = 3 5, Explored A | Step 2: `D:3, B:5`, Explored A | ✓ |
| Step 3: Expand D, Fringe B E F = 5 5 5, Explored A D | Step 3: `B:5, E:5, F:5`, Explored A,D | ✓ |
| Step 4: Expand B, Fringe E F C = 5 5 6, Explored A D B | Step 4: `E:5, F:5, C:6`, Explored A,D,B | ✓ |
| Step 5: Expand E, Fringe F C = 5 6, Explored A D B E | Step 5: `F:5, C:6`, Explored A,D,B,E | ✓ |
| Step 6: Expand F, Fringe C G = 6 8, Explored A D B E F | Step 6: `C:6, G:8`, Explored A,D,B,E,F | ✓ |
| Step 7: Expand C, Fringe G = 14, Explored A D B E F C | Step 7: `G:14` per slide, Explored A,D,B,E,F,C | ✓ |
| Step 8: Expand G, "Found the path: A to D to F to G" | Step 8: Return $A\to D\to F\to G$, cost 8 | ✓ |

The chapter matches slide 37 exactly, and reconciles the slide-7-vs-algorithm tension with an honest pedagogical note. The reviser's judgement call — "match the slide for exam recall; explain the algorithm separately" — is correct and student-friendly.

**§5.5 DFS verification (against slides 38–46):**
- The 8-row trace walks A → B → D → E → C → F → G in left-first DFS order.
- Step 1 pushes C then B; B ends up on top of `[C, B]`. ✓
- Step 2 pops B, pushes E then D; D ends up on top of `[C, E, D]`. ✓
- Trace terminates at step 7 with G as goal. ✓
- No "wait" leakage. Single table. Single voice. ✓

**§3.4 tree-vs-graph callout verification:**
- Defines tree search (pure form, no dedup): ✓
- Defines graph search (this template, with dedup): ✓
- States which the pseudocode implements: ✓
- Notes "replace if cheaper" is UCS-only (resolves the Round-1 Rev2 P1-5 inconsistency): ✓
- "Why it matters" is implicit; see round-2 P1-6.

**Slide-cross-reference audit:** every `[Lecture 3, slides N–M]` block at section ends matches the slide content. No fabricated slide references.

**New worked-example additions audit:**
- §1.1 motivation triad (slide 6) — content matches slide. ✓
- §3.1.1 three warm-up examples (slide 5) — match slide. ✓
- §3.2.1 four design questions (slide 17) — match slide. ✓
- §3.3.1 n-Puzzle state counts (slide 15) — match slide. ✓ Bonus: the factor-of-2 reachability explanation is correct.
- §4.2.1 goal-test-on-pop counter-example — algorithmically correct; under-specifies generation order (see round-2 P1-3).
- §4.4.0 depth-limited DFS — correct.
- §4.5.1 bidirectional + depth-limited — correct.
- §5.1.1 vacuum-world BFS — **CONTAINS NEW P0-1 DEFECT** (see above).
- §5.2.2 Romania UCS to completion — arithmetic verified (220+97=317 Pitesti, 317+101=418 Bucharest, etc.).
- §5.3.1 replace-if-cheaper counterfactual — correct.
- §5.6.1 IDS overhead arithmetic — $6+50+400+3000+20000+100000 = 123{,}456$ ✓.
- §5.7 BFS-vs-UCS contrast — correct (BFS returns 14-cost via FIFO tie-breaking; UCS returns 8-cost).
- §5.8 8-queens formulation — correct.

**External corroboration:**
- Slide 37 PNG re-checked line-by-line; chapter trace matches.
- Slide 54 comparison table data matches chapter §4.5 table.
- IDS arithmetic for $b=10, d=5 \Rightarrow 123{,}456$ verified by hand.
- BFS-vs-UCS slide-37 contrast (cost 14 vs cost 8) verified by hand.

---

## Report to PM

**Assignment recap:** Round-2 pedagogical-clarity review of `L03-Uninformed-Search.md`. Verify the three Round-1 P0 defects (§5.3 UCS corrupt, §5.5 DFS mid-table correction, §3.4 graph vs tree search abdicated) are fixed; flag any new defects introduced by the revise.

**Status:** **Pass with concerns.** 1 × new P0 (regression of round-1 P0-2 defect class in a newly added section), 6 × P1, 8 × P2 (most carry-overs).

**P0 findings:**

1. **`study/lectures/L03-Uninformed-Search.md` §5.1.1 step 1 (line 466).** The newly added vacuum-world BFS trace has the same "thinking-aloud" defect as the round-1 P0-2 (which the reviser correctly fixed in §5.5). Specifically the parenthetical "*(no-op, skip — self-loop already in frontier? actually new, in explored after pop)*" floats three competing reasons for skipping the $L$ child in 14 words. Fix: rewrite as one clean reason — *"$L$→`(A,1,1)` (already in explored, skip)"*. One-line edit.

**P1 findings:**

1. `study/lectures/L03-Uninformed-Search.md` line 4 — glossary-terms-introduced header still lists `transition model (search)` despite the body removing the term. Delete the token.
2. `study/lectures/L03-Uninformed-Search.md` §3.8 line 254 and §7 line 735 — "admissibility" and "consistency" are still named, contrary to round-1 P1-3 which asked them to live only in the glossary. Reword to "conditions on $h$ (see L05)" without naming.
3. `study/lectures/L03-Uninformed-Search.md` §4.2.1 — goal-test-on-PUSH counter-example under-specifies the order of successor generation. Add one sentence: *"Assume the successor function returns $G_1$ then $A$"*.
4. `study/lectures/L03-Uninformed-Search.md` §5.3 step-7 pedagogical note (lines 566–568) — the student-facing "what to write on the exam" ladder is at the end; move it to the front for higher signal-to-noise.
5. `study/lectures/L03-Uninformed-Search.md` §5.7 — "left-to-right child ordering matching the edge list" is vague; anchor it on the edge-list table instead.
6. `study/lectures/L03-Uninformed-Search.md` §3.4 tree-vs-graph callout — defines the mechanism but doesn't make the *consequence* vivid. Append one sentence on "without an explored set, pure tree search re-expands the same state from every path".

**P2 findings:**

1. §5.6.1 IDS arithmetic — rename column header "coefficient $(d+1-k)$" to "level multiplier".
2. §2.5 IDS analogy is still the algorithm paraphrased rather than an everyday image (round-1 P2-1 carry-over).
3. §5.3.1 counterfactual introduces an invented $E \to F$ edge; consider building a standalone 4-node example instead.
4. §5.2.2 Romania trace — add footnote noting Zerind's only non-skipped neighbour is Oradea.
5. §8 cheat-sheet "When to pick which" bullets — tighten for parallelism (IDA\* bullet is the only one with two sentences).
6. §5.8 8-queens formulation is a strong addition; flagged positively.
7. §3.3.1 n-Puzzle counts + NP-hardness + factor-of-2 explanation; flagged positively.
8. Reading time ~60 min at the long end; verify §8 cheat-sheet is exam-sufficient with App Tester.

**QA Checklist status (versus Reviewer #3's §7.1 lens):**

- **"flag hand-waving"** — round-1 §3.4 graph-vs-tree fixed; round-2 §3.4 still slightly hand-waves the "why it matters" consequence (P1-6). **Mostly Pass.**
- **"flag unjustified leaps"** — round-1 §5.3 step-3 thinking-aloud fixed; round-1 §5.5 wait-redo fixed; **new** §5.1.1 step-1 thinking-aloud introduced (P0-1). **Regression.**
- **"flag undefined terms"** — transition model body-removed (P1-1 cleans header); admissibility/consistency still named in §3.8 (P1-2). **Mostly Pass.**
- **"flag missing intuition"** — §2.1 maze breakdown reinforced; §8 cheat-sheet analogies added. **Pass.**
- **"enforce analogies"** — §2 still delivers six analogies + six caveats; cheat-sheet analogies present. **Pass.**

**Acceptance criteria (§7.1) status:**

- Every major concept has an analogy in §2 with "where it breaks down" caveat: **Met.**
- Analogies are cross-linked from §3: **Met.**
- Pseudocode is free of in-line author confusion / hand-waving: **Not met** (§5.1.1 step 1 regression — see P0-1).
- Traces match the slides line-by-line: **Met for §5.3, §5.5, §5.6** (verified above).
- Tree search vs graph search is taught, not deferred: **Met** (callout box added; cosmetic motivation polish suggested in P1-6).

**DOCUMENT.md audit:** N/A — this is a textbook chapter, not an engineering directory.

**Out-of-scope observations:**
- The reviser's judgement call in §5.3 (match slide for exam recall; explain algorithm separately) is the right call and I would not unwind it. The "What to write on the exam" ladder is a textbook-quality piece of meta-pedagogy.
- §5.7 BFS-vs-UCS contrast is the kind of decisive worked example that round 1 didn't even request; it earns its keep.
- §5.2.2 Romania UCS to completion fills a real gap (slides only go through step 1–2 of the search) without exceeding L03's scope.

**Concerns / risks:**

- The §5.1.1 P0-1 defect is *one line* and *in a newly added section* — easy to fix. If it lingers, however, it'll be the first thing a student trips on in the chapter (BFS is §5.1, the first worked example).
- §3.8's "admissibility, consistency" naming-with-disclaimer is a judgement call. I'm flagging it as P1 because the round-1 reviewer-3 spec was explicit (move to glossary), and the round-1 revise didn't fully execute. Reviewer #2 (mathematical rigour) and Reviewer #4 (exam readiness) might want these terms named here — defer to PM on the round-2 cross-review aggregation.
- Reading time is now ~60 min for a 56-slide deck; check whether App Tester / examiners think §8 is sufficient as a standalone revision tool.

**What PM should do next:**

1. **Dispatch a focused touch-up edit** to fix the one P0-1 (one-line rewrite of §5.1.1 step 1) plus the six P1 items above. These can be batched in a single short edit pass; no architectural changes required.
2. **Optional:** sweep the eight P2 items in the same pass if scope permits (mostly cosmetic).
3. **Do not re-dispatch the full Reviewer #3 cycle after the touch-up** — a quick sanity-check that §5.1.1 step 1 reads cleanly and the header glossary list no longer says "transition model" is sufficient.
4. Proceed to App Tester once the touch-up lands (no need to wait for round 3 of reviewers — this is a polish round, not a defect round).

**DOCUMENT.md updated:** N/A for QA.
