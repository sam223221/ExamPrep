# Lab Reviewer #4 (Variant Adaptability) — Lab2-Search Round 1

**Reviewer role:** Variant adaptability auditor
**Inputs:**
- Solution: `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 2\Search_solution.py`
- Handout: `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 2\Lab 2.pdf`
- Variants: `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab2-Search\variants.md`

Verdict: **Fail** — the KNOB infrastructure itself is largely sound, but three of five variants ship incorrect "Expected answer" sections that an exam agent following the variant doc would parrot verbatim. The variant bank is unreliable as a study artefact.

All claims in this report were verified by running `Search_solution.py` under each variant's KNOB block.

---

## Report to PM

**Assignment recap:** Lab Reviewer #4 (Variant Adaptability) for Lab2-Search Round 1. Reviewing `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 2\Search_solution.py` against `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab2-Search\variants.md` and the handout `Lab 2.pdf`.

**Status:** Fail — three of the five variants ship incorrect "Expected answer" sections that an exam agent following the variant doc would parrot verbatim. The KNOB infrastructure itself is largely sound, but the variant bank is unreliable as a study artefact.

### P0 findings

1. **Variant 1 "Expected answer" is internally contradictory and numerically wrong** — `variants.md:41-43`.
   The variant claims "BFS finds a 7-step plan" in one clause and "total path length 6 actions / depth 6" in the next. Empirically (verified by running `Search_solution.py` with the variant's exact KNOB block), BFS finds a **5-action plan** of length 5 (`Suck-A, Right, Suck-B, Right, Suck-C` → `('C','Clean','Clean','Clean')`), producing a 6-state path. Both numbers in the doc are wrong.
   *Suggested fix:* change to "BFS finds a 5-action plan / depth 5; path has 6 states: `('A','D','D','D') → ('A','C','D','D') → ('B','C','D','D') → ('B','C','C','D') → ('C','C','C','D') → ('C','C','C','C')`."

2. **Variant 2 DFS expansion-order claim is wrong** — `variants.md:73-75`.
   The doc says "DFS expands A, B, D, E, C, F, G in fringe-traversal order before finding J inside G". Actual DFS expansion order is `A, B, D, E, C, F, G, H, I` and *then* J is goal-tested. H and I are popped and goal-tested before J because `Node.expand()` calls `insert(s, successors, insert_as_first=True)` internally, so `expand(G)` returns `[J, I, H]` and `insert_all(..., insert_as_first=True)` prepends each in turn, placing `H` at the head, then `I`, then `J`.
   *Suggested fix:* update expected expansion to `A, B, D, E, C, F, G, H, I, then J found`. Also clarify that under this implementation children are visited in *reverse* of the dict's listed order (because `expand` itself uses insert-as-first), which is why BFS expands `C` before `B` — that quirk is worth calling out explicitly so students don't get blindsided.

3. **Variant 3 "standard 7-step solution" claim is wrong** — `variants.md:115-116`.
   From `('W','E','W','W')` (farmer back with goat+cabbage, wolf already across), BFS finds a **3-step** solution: `→ ('E','E','W','E') → ('W','E','W','E') → ('E','E','E','E')` — i.e. ferry cabbage over, return alone, ferry goat over. The wolf is already on the east bank in this start state, so the classic 7-step doesn't apply. The KeyError analysis earlier in the variant is correct, but the punchline answer (`"BFS finds the standard 7-step solution"`) is wrong.

4. **Variant 4 (8-puzzle) misstates the optimal moves AND is not actually KNOB-adaptable** — `variants.md:144-145`.
   The doc says "BFS finds the 2-move solution Up-Right (blank moves) ending at `(1,2,3,4,5,6,7,8,0)`". For start `(1,2,3,4,5,6,0,7,8)` the blank is at index 6 (bottom-row, leftmost); the goal `(1,2,3,4,5,6,7,8,0)` puts the blank at index 8 (bottom-row, rightmost). The blank only needs to move **Right, Right** (two right moves) — there is no Up move. Separately, the variant violates the variant-bank charter (`variants.md:4-6`, "should be able to answer it by changing KNOB values, no function-body edits") because there is no KNOB that supplies a programmatic 8-puzzle generator — the doc admits this with "the exam agent can either hand-construct it for a small slice or import an external generator" (line 137-138), which is a function-body edit.
   *Suggested fix:* either drop this variant or add a `KNOB_BUILD_8PUZZLE_STATE_SPACE` flag with the generator function in the solution file.

### P1 findings

1. **Variant 5 expected-answer paragraph is incoherent** — `variants.md:171-180`.
   Opens with "**5-step** solution", then immediately re-counts to 7 ("…take goat = 7 with both rules"), then re-counts to 6 ("…take goat (6) — depth 6"), and concludes "depth 6, one shorter than the classic 7-step solution." The empirically verified answer is **depth 5**, which is two shorter than the classic 7 (path: `WWWW → EWEW → WWEW → EWEE → WWEE → EEEE`). The headline number happens to be right but the worked solution is internally contradictory and the comparison is off-by-one. Rewrite with a clean trace.

2. **Variant 1 KNOB table omits a relevant knob** — `variants.md:32-39`.
   The table never tells the agent that `KNOB_PRINT_FRINGE_TRACE` is currently silenced for Exercise 2 anyway (see `run_exercise_2()` which forces `KNOB_PRINT_FRINGE_TRACE = False` inside a try/finally). Students who want to "show the fringe" per the handout will be surprised that toggling the global KNOB has no effect during the vacuum-world demo. Variant should mention this gotcha or recommend running `searcher.run(...)` directly with the global re-enabled.

3. **Variant 2 max-fringe claim is right but the path claim is misleading** — `variants.md:73-78`.
   Both BFS and DFS converge on path `A→C→G→J` because of the reverse-children quirk in `Node.expand()`. The variant labels this as the path under both, which is *technically* correct but pedagogically dishonest — under a textbook BFS/DFS where children are added left-to-right, DFS goes `A→B→...` and never reaches J without backtracking from the left subtree. The variant should call out that `expand()` happens to invert child order, which is why the right subtree is explored first.

4. **Variant 4 has an internal contradiction between table and prose** — `variants.md:130-137`.
   Prose says "Use DFS with a depth limit sufficient to find a short solution" but the KNOB table sets `KNOB_DEFAULT_STRATEGY = "BFS"` with a parenthetical justification. These directly contradict each other inside the same variant. Pick one.

5. **No variant exercises `KNOB_TRACK_VISITED = False` on the cyclic problems.**
   Pedagogically this is the most interesting demonstration the KNOBs enable (showing exponential explosion / infinite recursion). Worth adding as a Variant 6.

6. **No variant exercises `KNOB_EX2_GOAL_STATE = None`.**
   The "any all-clean" hook exists in the `AllCleanSearcher` subclass and is documented in the KNOB block (line 261-265), but no variant tests it. Documented capability with no coverage.

7. **No variant exercises `KNOB_EX3_PASSENGERS_PER_TRIP`.**
   The KNOB doc (lines 308-316) explicitly invites a variant ("try 2 to model a larger boat") but the variant bank ignores it.

### P2 findings

1. Variant 2 says "Then RE-RUN with `KNOB_EX1_GOAL_STATE = "D"` to answer the 'had J been D' sub-question." This is fine but should be in the KNOB table not loose prose — currently a student following only the table will miss the re-run instruction.

2. The variant doc uses inconsistent quoting for tuples — e.g. `('W','W','W','W')` vs `('W', 'W', 'W', 'W')` vs `("A", "B")`. Minor, but consistency would help an exam agent copy-paste.

3. Variant 1's "What this tests" cleanly identifies three reasoning steps; the other variants would benefit from the same tri-pronged structure for grading clarity.

### QA Checklist (§7) status
N/A — this is a study-material variant-bank review, not a feature-plan QA. The relevant analogue is "do the variants actually solve correctly when KNOBs are applied as documented?" That fails on Variants 1, 2, 3, and 4 (P0).

### Acceptance criteria (§1) status
N/A.

### DOCUMENT.md audit
N/A — study materials, no DOCUMENT.md scope.

### Out-of-scope observations

1. `Node.expand()` reverses child order via `insert(s, successors, insert_as_first=True)` (`Search_solution.py:379-384`). This produces correct-looking results on the handout's A..J example (BFS path A→C→G→J is what the lecturer probably expects), but it means the code's "BFS" expands the rightmost child first, which is non-textbook. Worth flagging in the solution's docstring header so exam students don't assume left-to-right child order.

2. The variant bank doesn't reference `study/lectures/L03-Uninformed-Search.md` (which the solution docstring at line 55 says exists). If that lecture file isn't extracted yet, the cross-reference is dead.

3. `_track_visited` is a class-level attribute set on an instance (lines 461, 689). That's fine but slightly subtle — a code reader could think it's read-only.

### Concerns / risks

- An exam agent using this variant bank to *grade* itself will mark wrong answers as correct on Variants 1, 3, 4 and partially Variants 2 and 5. That defeats the purpose of having a variant bank.
- The "no function-body edits" charter is broken by Variant 4. Either retract the charter or drop the variant.
- The variant bank assumes BFS and DFS will explore children in their dict-order, but `expand()`'s implementation inverts this. None of the variants warn the reader about this subtlety, even though it changes every printed expansion order.

### What PM should do next

1. Dispatch the lab-author engineer (or whoever owns `variants.md`) to:
   - Fix Variant 1's depth/step counts (P0)
   - Fix Variant 2's DFS expansion-order list (P0)
   - Fix Variant 3's "7-step solution" → "3-step solution" (P0)
   - Either drop Variant 4 or add a KNOB-driven 8-puzzle generator to `Search_solution.py` so the variant honours the no-function-body-edits charter (P0)
   - Rewrite Variant 5's worked solution to be internally consistent and confirm depth=5 (P1)
   - Add a "child-ordering quirk" note pointing at `Node.expand()` (P1)
2. Then re-run QA on the variants to confirm every "Expected answer" is reproducible by running the variant's KNOB block.
3. Consider adding 3 new variants covering `KNOB_TRACK_VISITED=False`, `KNOB_EX2_GOAL_STATE=None`, and `KNOB_EX3_PASSENGERS_PER_TRIP=2` (P1 — fills documented-but-uncovered KNOB surface).

**DOCUMENT.md updated:** N/A for QA.

---

## Empirical evidence appendix

All verified by executing `Search_solution.py` under each variant's KNOB block.

| Variant | Doc claim | Actual (verified) |
|---|---|---|
| 1 | 7-step plan / depth 6 | 5-step plan / depth 5 |
| 2 DFS expansion | `A,B,D,E,C,F,G` then J | `A,B,D,E,C,F,G,H,I` then J |
| 2 BFS expansion | `A,C,B,G,F,E,D` then J | `A,C,B,G,F,E,D` then J (correct) |
| 2 max fringe (DFS / BFS) | 3 / 6 | 3 / 6 (correct) |
| 3 from `('E','E','W','W')` | KeyError + 7-step from `('W','E','W','W')` | KeyError (correct) + 3-step from `('W','E','W','W')` |
| 4 | 2-move "Up-Right" | 2-move "Right, Right"; also non-KNOB-adaptable |
| 5 | "5-step" / "depth 6" / "one shorter" | 5-step / depth 5 / two shorter |
