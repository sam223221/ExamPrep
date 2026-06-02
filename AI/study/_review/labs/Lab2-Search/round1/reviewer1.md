# Lab 2 — Search: Reviewer #1 (Correctness) — Round 1

**Reviewer role:** Correctness inspector
**Solution under review:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 2\Search_solution.py`
**Original template:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 2\Search.py`
**Handout:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 2\Lab 2.pdf`
**Run command:** `py -3.12 "Lab 2\Search_solution.py"`
**Run result:** exits cleanly (exit code 0), all three demos print outputs.

---

## Report to PM

### Assignment recap
Verify Lab 2 solution: implement `insert/insert_all/remove_first` fringe primitives, run BFS/DFS on the A..J tree (Exercise 1), solve the vacuum world with BFS (Exercise 2), and solve the farmer/wolf/goat/cabbage river-crossing homework. Confirm correctness of outputs versus the lab handout and lecture-3 semantics.

### Status
**Pass with concerns** — every required exercise produces a correct, defensible answer. The fringe traces, the vacuum solution, and the river-crossing solution all match the canonical hand-traced answers. Concerns are about (a) one cosmetic deviation from the template's print order and (b) one minor bug in the original template that the solution silently inherits but never triggers.

### P0 findings
None.

### P1 findings

1. **`StateSpace.successor` swallows a missing-state-space without raising**
   File: `Lab 2\Search_solution.py:336-344`
   ```python
   def successor(self, state: Any):
       if self.state_space is None:
           print("No state space set")
       return self.state_space[state]   # TypeError-on-None one line later
   ```
   When `state_space is None` the function prints a warning, then immediately does `None[state]` which raises `TypeError: 'NoneType' object is not subscriptable`. The print is therefore noise — the error a user actually sees is the TypeError, not the helpful message. This is inherited verbatim from the original template and was flagged in the solution's docstring as deliberate ("Keep the original template's behaviour"), but for a study/exam reference it would be cleaner to either `raise ValueError("No state space set")` or simply remove the dead `print`. Suggested fix:
   ```python
   if self.state_space is None:
       raise ValueError("No state space set")
   return self.state_space[state]
   ```
   Severity P1 because the dead branch never fires on any of the three exercises, but the misleading control flow would confuse a student reading this as a worked example.

2. **BFS fringe ordering is the reverse of the textbook convention**
   File: `Lab 2\Search_solution.py:373-384` (`Node.expand`) + `403-415` (`insert`)
   `Node.expand` calls `insert(s, successors)` with the default `insert_as_first=True`, which means the child list returned by `expand` is **reversed** relative to the state-space dict. Then BFS appends them to the back of the fringe in that reversed order. Concrete consequence — after expanding A on the A..J tree, the BFS fringe is `[C, B]` instead of the textbook `[B, C]`. The shortest-path output (A → C → G → J) is still correct because both B and C are at depth 1, but a student grading this against the lecture slides' hand-trace will see the children appear in the "wrong" order. The solution's docstring acknowledges this is preserved from the template, but the trace is what the handout explicitly asks the student to produce ("give the fringe after expanding each node"). Suggested fix: change `Node.expand` to `successors.append(s)` (or `insert(s, successors, insert_as_first=False)`), then DFS will also need its insertion order checked — DFS currently prints `[B, C]` after expanding A and would become `[C, B]`. Either order is defensible, but the chosen one should match the lecture slide that students will be quoted against.
   Severity P1 because it doesn't break correctness but does change the artefact the handout literally asks for.

3. **`run()` output order silently diverged from the template**
   File: `Lab 2\Search_solution.py:515-525` vs original `Search.py:96-100`
   Original template prints `for node in path` (root-last order: J, G, C, A). Solution prints `for node in reversed(path)` (root-first order: A, C, G, J). The reversed order is much more readable, and the solution's comment explicitly explains and defends the change ("leaf-to-root; reversed() reads naturally for a human"), but a marker who diffs against the template will notice. Not a bug, but it is a behaviour change in code the lab handed out as scaffolding. Note this in the README or move it under a knob so the original output can be restored. Severity P1 only because the handout's wording ("solution path") doesn't pin the direction down — both orderings are correct.

### P2 findings

1. **`KNOB_PRINT_FRINGE_TRACE` is mutated with `global` inside `run_exercise_2/3`**
   File: `Lab 2\Search_solution.py:726-728, 760-762`
   The pattern works (and the `finally` block restores it) but mutating a module-level constant labelled "KNOB" is a smell. Cleaner: pass the trace flag explicitly to `tree_search`, or factor the trace decision into the `Searcher` instance. Cosmetic.

2. **`Self` typing import requires Python 3.11+**
   File: `Lab 2\Search_solution.py:133` `from typing import Any, Self`
   The lab's run command `py -3.12` makes this fine, but it is not the most portable choice for a study-archive reference. If anyone tries `py -3.10` the import will fail. Trivial.

3. **Unused/under-exercised KNOBs**
   File: `Lab 2\Search_solution.py:171, 254-265`
   `KNOB_MAX_FRINGE_NODES` and `KNOB_EX2_GOAL_STATE = None` paths are never exercised by the default run. They are documented as "exam variants" hooks and the code paths are sound, so this is a P2 nit at most; just flag that no smoke test exists for them.

4. **`AllCleanSearcher` defined inside `run_exercise_2()` is recreated every run**
   File: `Lab 2\Search_solution.py:709-720`
   Defining the class inside the function is fine but pointless given the function is only called once. Lifting it to module scope (next to `Searcher`) would be cleaner and let it be reused by an exam variant. Cosmetic.

5. **`Searcher.__init__` parameter `state_space: StateSpace = None`** declares the type as `StateSpace` but accepts `None`. The original template did the same; just flag for tidy typing (`StateSpace | None = None`). Trivial.

### Correctness checklist (the actual deliverable)

| Exercise | Required output | Solution output | Verdict |
|---|---|---|---|
| Ex1 DFS A→J | Path A → C → G → J at depth 3 (one valid DFS path; given the reversed-child quirk, A→B→D, A→B→E dead ends, then A→C→F, A→C→G→H, →I, →J) | A → C → G → J (depth 3). DFS fringe trace: `[B,C] → [D,E,C] → [E,C] → [C] → [F,G] → [G] → [H,I,J] → [I,J] → [J]` | **Pass** — every fringe step matches a hand trace (children built right-to-left because `expand` prepends, then DFS prepends again ⇒ left-to-right pop order). |
| Ex1 BFS A→J | Shortest path A → C → G → J at depth 3; fringe trace requested by the handout | A → C → G → J. Fringe trace: `[C,B] → [B,G,F] → [G,F,E,D] → [F,E,D,J,I,H] → [E,D,J,I,H] → [D,J,I,H] → [J,I,H]` | **Pass with concern (P1 #2)** — every state appears exactly once, all depths are monotonic non-decreasing (BFS invariant holds), the goal is found at the minimal depth. Sibling order is reversed from the textbook but mathematically the search is still BFS. |
| Ex2 BFS vacuum (`A, Dirty, Dirty`) → (`B, Clean, Clean`) | Shortest plan: Suck, Right, Suck (depth 3) | (A,D,D) → (A,C,D) → (B,C,D) → (B,C,C). Depth 3, three actions. | **Pass** — matches the optimal plan exactly. |
| Ex2 DFS vacuum (same start/goal) | Any valid path (not necessarily optimal) | Same as BFS — depth 3 | **Pass** — DFS happens to find the optimal path on this tiny graph because cycle-detection prunes Right/Left ping-pongs. |
| Homework BFS river crossing | Classic 7-step solution (depth 7) | `(W,W,W,W) → (E,W,E,W) → (W,W,E,W) → (E,W,E,E) → (W,W,W,E) → (E,E,W,E) → (W,E,W,E) → (E,E,E,E)` | **Pass** — verified each intermediate state is safe (no wolf+goat alone, no goat+cabbage alone) and each transition moves the farmer plus at-most-one item across. Matches the canonical "farmer-takes-goat / returns / takes-cabbage / brings-goat-back / takes-wolf / returns / takes-goat" sequence. |
| Homework DFS river crossing | Any valid path (with cycle detection) | 7-step solution, different middle: takes cabbage and wolf in opposite order. Depth 7. | **Pass** — alternative valid solution; safety verified state-by-state. |
| Unsafe state filter | Forbid wolf+goat alone, goat+cabbage alone | `is_safe` correctly rejects `(W,E,E,W)`, `(E,W,W,E)`, `(W,W,E,E)`, `(E,E,W,W)`, `(W,W,W,E)?` — checked: `(W,W,W,E)` has cabbage E alone with no predator → safe ✓. Final dict has exactly the 10 reachable safe states. | **Pass** |
| Boat-capacity constraint | Boat carries farmer + ≤ 1 other | `KNOB_EX3_PASSENGERS_PER_TRIP = 1` and `combinations(co_items_on_same_bank, k)` for `k in range(0, 2)` enumerates trips of 0 or 1 co-passenger. No 2+ trips generated. | **Pass** |
| `insert(node, queue, insert_as_first=True)` non-mutating | Spec: "returns a copy with the node inserted, does not modify input" | Implementation uses `[node] + queue` / `queue + [node]` — both produce fresh lists | **Pass** |
| `insert_all(nodes_to_add, queue, …)` non-mutating | Spec: "returns a copy with the nodes inserted, does not modify the original" | Builds `new_queue` by repeated `insert()` calls; the original `queue` arg is never appended-to | **Pass** |
| `remove_first(queue)` removes and returns head | Spec: "removes the first element… the removed element will be returned" | `queue.pop(0)` — does mutate the input list, which is consistent with the docstring ("Removes the first element from the input list"). | **Pass** |
| Tree-search loop termination | Original template's `while fringe is not None` is buggy (lists are never None) | Solution fixes it to `while fringe:` and documents the bug. | **Pass + improvement** |

### Out-of-scope observations
- The solution adds cycle detection (`KNOB_TRACK_VISITED`) which is **not** in the handout. Without it, BFS on the vacuum world and DFS on the river puzzle would explode/loop. This is a legitimate scope extension for a study reference and is documented as such; flagging it so the marker isn't surprised.
- The `AllCleanSearcher` subclass and the `KNOB_EX2_GOAL_STATE = None` "any-clean" goal-test are also extensions beyond the handout.
- `KNOB_DEFAULT_STRATEGY = None` runs **both** BFS and DFS for every exercise. The handout for Ex2 asks only for BFS; the extra DFS run is helpful pedagogically but adds noise. Consider documenting "the handout only asks for BFS here" in the printed banner.

### Concerns / risks
1. The reversed sibling order in BFS (P1 #2) is the single biggest risk for a marker who compares the fringe trace line-by-line against the lecture slides. If the slide for this exercise shows `[B, C]` after expanding A, the student needs to know why this solution shows `[C, B]` and be able to justify it (it's because of how `expand` is implemented in the template).
2. Cycle detection being on by default for Ex1 is correctly overridden (`searcher._track_visited = False` at line 689), but a student tweaking knobs might forget this and produce confusing output. Worth a one-line comment in `run_exercise_1` saying "do NOT remove this override."
3. The solution does not include any unit tests / asserts to lock in the expected outputs. For a study archive, a small `assert path[-1].state == "J"` etc. would catch regressions during last-minute exam-eve edits. Not required, just a safety-net suggestion.

### What PM should do next
Proceed to **Lab Reviewer #2 (Style/Pedagogy)** as planned. The correctness review is green-with-caveats. Before the exam, optionally:
1. Add a one-line note next to the BFS run explaining the `[C, B]` sibling order (P1 #2). No code change needed.
2. Replace the dead `print("No state space set")` with a `raise` (P1 #1).
3. Leave the `reversed(path)` print order as is — it is strictly more readable.

### DOCUMENT.md updated
N/A for QA / reviewer role.
