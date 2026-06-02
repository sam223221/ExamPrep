# Lab 2 — Search: Reviewer #3 (Pedagogical Clarity)

**Reviewer scope:** docstrings, comments, MENTAL MODEL, and consistency with `study/lectures/L03-Uninformed-Search.md`.
**File under review:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 2\Search_solution.py`
**Lecture of record:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L03-Uninformed-Search.md`

This review is HARSH on purpose. I focus on whether a student reading the comments learns the *same* mental model that L03 teaches, with the *same vocabulary*, the *same trace conventions*, and the *same edge-cases flagged*. Code correctness is only critiqued where it leaks into pedagogy.

---

## Report to PM

**Assignment recap:** Lab 2 Search solution — Round 1 pedagogical-clarity audit against L03.
**Status:** Fail.
**Headline reason:** The MENTAL MODEL is solid and the KNOB documentation is unusually careful, but (1) the vacuum-world Left/Right semantics in the comments contradict L03 §5.1 and the lab handout's hint, (2) the file silently uses a *different* DFS-child-order convention from L03 §5.5 with no docstring reconciliation, (3) the algorithm comments suppress the L03 "graph search vs tree search" terminological move that the KNOB itself exposes, and (4) several public methods lack docstrings entirely while non-public hooks have lavish ones — the prioritisation is upside down.

---

### P0 findings (pedagogy that will actively mis-train the student)

**P0-1. `build_vacuum_state_space` LEFT/RIGHT comment contradicts L03 §5.1 and the lab handout's hint.**
File: `Search_solution.py:566-574`.
```python
# Action 2: LEFT — move to the previous room in the tuple
# (wraps around).  In the 2-room world this is just "go to the
# other room"; in 3+ rooms it cycles.
left_idx = (rooms.index(location) - 1) % len(rooms)
```
L03 §5.1 (slide 13) defines the actions as *anchored*, not cyclic:
> `L`: agent moves to $A$ (no-op if already in $A$).
> `R`: agent moves to $B$ (no-op if already in $B$).

The lab handout's worked successor hint reflects this:
```
('A','Dirty','Dirty'): [('A','Clean','Dirty'),     # Suck
                        ('A','Dirty','Dirty'),     # Left → A (SELF-LOOP)
                        ('B','Dirty','Dirty')]     # Right → B
```
The solution's cyclic interpretation makes Left from `A` produce `B` (because `(0-1) % 2 == 1`), eliminating the self-loop the handout explicitly shows. A student who memorises this code as "the canonical vacuum-world model" will, on an exam asked to reproduce slide 13's successor table, write the wrong table. The comment is internally consistent with the (wrong) code, which is worse — there is no inline cue that anything is off.
*Fix:* anchor L to `rooms[0]` and R to `rooms[-1]` (or to the last room) and rewrite the comment to quote L03 §5.1 verbatim: *"L moves to A (no-op if already in A); R moves to B (no-op if already in B)."*

**P0-2. MENTAL MODEL omits the "graph search vs tree search" distinction even though the file's `KNOB_TRACK_VISITED` toggles exactly this.**
File: `Search_solution.py:41-51` (MENTAL MODEL) vs `173-187` (KNOB_TRACK_VISITED).
L03 §3.4 spends an entire pull-quote on the difference and §6 pitfall #5 expands it into three sub-modes:
- pure DFS with no check → loops forever
- DFS with current-path check → terminates but incomplete
- DFS with explored set → terminates, incomplete on disconnected components

The MENTAL MODEL block sells the file as *just* "FRONT vs BACK insertion" without flagging that a switch elsewhere in the file silently promotes the algorithm from "tree search" to "graph search". A student reading the MENTAL MODEL and then watching `KNOB_TRACK_VISITED = True` solve the cyclic vacuum world will not know which textbook claim they have just witnessed (it's the third sub-mode). The KNOB's own docstring does name the distinction but the *top-of-file* pedagogical anchor does not.
*Fix:* in the MENTAL MODEL paragraph, add one sentence: *"This file actually runs **graph search** (L03 §3.4) — i.e. tree search plus an explored set — whenever `KNOB_TRACK_VISITED` is True; `run_exercise_1()` flips it off to demonstrate the pure tree-search behaviour the slides describe."*

**P0-3. `Node.expand` comment hand-waves a non-trivial double-reversal that determines whether DFS matches L03 §5.5's left-first convention.**
File: `Search_solution.py:373-384`.
```python
# We deliberately use the module-level insert() helper rather than
# list.append so that the original template's behaviour ("expansion
# order = insertion order at the FRONT of a working list") is preserved.
```
What actually happens: `expand` calls `insert(s, successors, insert_as_first=True)` *for every child*, so a child list `[B, C]` ends up as `[C, B]` in `successors`. Then `insert_all` is called on the *fringe*. For DFS (`insert_as_first=True`) we end up with `[B, C, …old fringe…]` — i.e. B on top, popped first, which is **left-first DFS, matching L03 §5.5**. For BFS we end up with `[…old fringe…, B, C]` — also left-first FIFO. The double-reversal is *the* reason the file's traces match L03's traces.

The current comment ("expansion order = insertion order at the FRONT of a working list") does not say any of this and would not help a student who is trying to *reproduce* the L03 §5.5 DFS-on-A..G trace by hand and is confused about why the algorithm seems to push right-to-left but pop left-to-right. L03 §5.5 explicitly highlights the convention: *"DFS pushes children onto the LIFO stack in right-to-left order, so the leftmost child ends up on top of the stack and gets popped next."* The solution does the same thing, but spends its comment defending a coding choice ("we use insert() not append") instead of teaching the convention.
*Fix:* rewrite the comment to be student-facing: *"Each child is prepended to `successors`, so after the loop `successors` holds them in **reverse** order. `insert_all` then pushes that reversed list onto the fringe — for DFS this yields L03 §5.5's left-first convention (leftmost child on top of the stack, popped next); for BFS it yields edge-list FIFO order."*

---

### P1 findings (important pedagogy that will leave gaps)

**P1-1. The MENTAL MODEL's L03 paraphrase is not a real quote.**
File: `Search_solution.py:50-51`.
```python
# (Consistent with L03's "the search is what you do; the strategy is just how
# you order the fringe.")
```
L03 does not contain that string. L03 §2.6 says *"The order in which you pick items from the to-do list is the search strategy: FIFO ↦ BFS, LIFO ↦ DFS, priority by cost ↦ UCS."* L03 §3.4 says *"the order in which you pick is the search strategy"*. The paraphrase is *defensible* as a summary but a student who Ctrl-Fs L03 will not find it, and that is a credibility leak in a pedagogical artefact that otherwise insists on being citable. Either quote a real sentence or drop the quotation marks.

**P1-2. `tree_search` algorithm comment omits the "frontier dedup" half of L03's pseudocode.**
File: `Search_solution.py:494-499`.
The solution implements graph search using `visited: set` only — it never checks "is this state already in the fringe?" before pushing. L03 §3.4 pseudocode and §4.1 BFS pseudocode both include the `s' ∉ frontier` test:
```
if s' ∉ explored and child.state not already in frontier:
    push(frontier, child)
```
The L03 §5.7 BFS-vs-UCS contrast is *built* on this dedup rule firing. The solution skips it (correctness-wise harmless here because the goal test happens on pop, but it changes the fringe trace the student sees — duplicates of the same state appear, then get popped and dropped). The comment at 494-499 says only *"Cycle detection: only skip AFTER the goal test … and BEFORE expansion (so we don't generate the same children twice)"*, which is half the story. A student who later reads L03 §5.7 will be confused that the solution's BFS fringe carries duplicates that L03's BFS does not.
*Fix:* add one line: *"Note: L03 §3.4 also checks `s' ∉ frontier` before pushing. We don't — duplicates may sit in the fringe but are dropped harmlessly when popped (the `visited` guard fires), so the **solution path** matches L03's, but the **fringe trace** will show transient duplicates."*

**P1-3. `path()` docstring does not state the leaf-to-root ordering contract.**
File: `Search_solution.py:361-371`.
```python
def path(self) -> list[Self]:
    # Walk parent pointers from this node up to the root, …
```
Comment exists, but it is buried *inside* the body, not in a docstring. The function has no docstring at all. L03 §3.4 returns "the path" as root-to-leaf (the standard convention) — the solution returns leaf-to-root and relies on the caller in `Searcher.run` to `reversed()` it. The opposite convention is fine but **must be in the docstring** because every consumer of the function has to remember to reverse. Currently `Searcher.run` (line 522-524) does reverse it, but the comment there says only *"The path list is leaf-to-root; reversed() reads naturally for a human"* — the *function that produces* the leaf-to-root list does not document the contract.

**P1-4. `StateSpace.successor` has no docstring; the `print("No state space set")` is undocumented behaviour.**
File: `Search_solution.py:336-344`.
This is the single most-called function in the whole search. It deserves a docstring. The inline comment at 339-343 defends *why* a missing state space prints rather than crashes, but the *contract* — "returns the list of successor states for `state`" — is implicit. L03 §3.2 makes the successor-function definition explicit; the solution's class should mirror it.

**P1-5. The `Searcher` class docstring promises generality but the `__init__` and `tree_search` parameters are not individually documented.**
File: `Search_solution.py:449-526`.
The class docstring (`"Generic tree searcher parameterised by initial state, goal, and graph."`) is one line. `tree_search` has a docstring but `__init__`, `_is_goal`, and `run` do not. `_is_goal` is *the* hook L03 students should be told about — slides 4.2.1 emphasise that "goal test" is a *function*, not equality, and the solution implements it as a function but never says *"override `_is_goal` if your goal is set-membership instead of equality"* in a docstring. The override mechanism is exercised by `AllCleanSearcher` at line 709 with only a one-line inline comment.

**P1-6. The MENTAL MODEL block does not mention UCS / IDS even to disclaim them.**
File: `Search_solution.py:41-51`.
L03 §1.2 names *four* uninformed strategies (BFS, UCS, DFS, IDS). The lab does only two. A pedagogically responsible MENTAL MODEL would say so: *"This lab covers BFS and DFS only — L03 also defines UCS (priority queue keyed by $g(n)$, see L03 §4.2) and IDS (DFS with iteratively-deepening depth limit, L03 §4.4), both out of scope for Lab 2."* Without that, a student studying for an L03 exam from this file will think BFS/DFS are the whole story.

**P1-7. Glossary block (lines 57-63) is inconsistent with the L03 glossary header.**
The file's glossary says *"Breadth-first search (BFS) — FIFO frontier, expands shallowest node."* L03's glossary header (top of file) instead uses *"frontier (fringe)"* and lists both names because the slides use `fringe` and the textbook uses `frontier`. The solution's glossary uses both terms (`Frontier (fringe)`) so this is actually OK — keeping for the record. **However**, the solution everywhere in code uses the variable name `fringe` and the print label `"Fringe: …"`. L03 §6 pitfall #8 explicitly flags *"Treating 'fringe' and 'frontier' as different things. They are not."* The solution could include one line acknowledging this — currently a student might read "Frontier (fringe)" in the glossary and not realise the variable below is using the alt-name.

**P1-8. `insert`'s slicing comment claims an enforcement that the slicing does not actually enforce.**
File: `Search_solution.py:411-415`.
```python
# Slicing creates a shallow copy; this enforces the "do not mutate the
# input" contract spelled out in the original template's docstring.
if insert_as_first:
    return [node] + queue
return queue + [node]
```
There is no slicing here. `[node] + queue` and `queue + [node]` both build *new* lists via `list.__add__`, which does copy the right-hand operand — so the no-mutate contract IS upheld — but it is upheld by `+`, not by "slicing". The comment is technically wrong about the mechanism. A first-year Python student reading this will look for a `[:]` and not find one.
*Fix:* *"List concatenation (`+`) returns a new list, so the input `queue` is never mutated — this is the contract spelled out in the original template's docstring."*

**P1-9. The "original template's `while fringe is not None` was a subtle bug" remark is good but undersells the consequence.**
File: `Search_solution.py:469-471, 482-484`.
The comment correctly diagnoses the bug. But L03 §6 pitfall #5 — DFS in cyclic spaces — would *also* make this loop infinite even with the fix, unless `KNOB_TRACK_VISITED=True`. The comment should connect the two: *"With `is not None` the loop runs while the fringe is non-empty; in a cyclic state space (vacuum world; river-crossing) this would still loop forever without `KNOB_TRACK_VISITED=True`, which is why that KNOB exists."* Without this connection a student misreads the bug fix as "this loop now terminates" — which is only true for acyclic graphs.

---

### P2 findings (polish)

**P2-1.** The decorative banners (`# ===== K N O B S =====`, etc.) use spaced-letter formatting that screen readers and grep both hate. This is purely cosmetic but a student copy-pasting to study notes loses the section headers.

**P2-2.** `_swap_bank` (line 586-588) uses `banks[0] if bank == banks[1] else banks[1]`. Clear enough, but the docstring is one line and does not flag that the function assumes a two-element `banks` tuple — passing three banks silently degrades to "swap with bank 0 or bank 1". For a knob-driven file that takes its banks tuple from `KNOB_EX3_BANKS`, this is a brittleness the docstring should mention.

**P2-3.** `KNOB_EX1_GOAL_STATE` exam-variant suggestion (line 232-233): *"`('B', 'J')` to start the search part-way down (DFS will then fail to find J at all because J is in C's subtree, which is unreachable from B"*. This is a great pedagogical hook for L03 §6 pitfall #5 (DFS incompleteness in disconnected components). But it is buried in a KNOB docstring; consider promoting it to the MENTAL MODEL or to a `# Try this at home:` block.

**P2-4.** `KNOB_DEFAULT_STRATEGY` (line 151) is typed `str | None` but accepts only `{None, "BFS", "DFS"}`. Use `typing.Literal["BFS", "DFS"] | None` to make the contract self-documenting and IDE-checkable.

**P2-5.** `KNOB_PRINT_FRINGE_TRACE` is mutated as a *global* in `run_exercise_2` and `run_exercise_3` (lines 726-728, 760-762). The `try/finally` correctly restores it, but a comment explaining *why* this is acceptable (the file is single-threaded; the alternative would be to plumb the flag through the searcher) would head off a "globals are evil" knee-jerk from a reader.

**P2-6.** `Node.__repr__` returns `f"State: {self.state} - Depth: {self.depth}"`. L03 §5.5's traces show fringes as bare states (`[B, C]`, `[C, E, D]`). The solution's fringe prints will look like `[State: B - Depth: 1, State: C - Depth: 1, …]`. A side-by-side comparison with the lecture trace would benefit from a `--terse` repr (state-only). Not a bug; a missed pedagogical opportunity.

**P2-7.** No reference anywhere to L03 §5.5's *"left-first DFS"* convention. The DFS run on the A..J tree in this file will produce traces that students will compare letter-by-letter with L03 §5.5's binary-tree trace. A one-line comment in `run_exercise_1` saying *"DFS here follows L03 §5.5's left-first convention — leftmost child popped first"* would close the loop.

**P2-8.** Lines 53-56 say *"See study/lectures/L03-Uninformed-Search.md once extracted."* The lecture *has* been extracted (we read it). The "once extracted" phrasing is stale and signals to the student that the lecture file might not be there yet, when in fact it is the canonical reference.

---

### QA Checklist (§7) status

QA Checklist §7 is from the Feature Plan template — there is no `PM/` folder in this repository and no Feature Plan was provided for this review. The standing checklist items I can evaluate from the pedagogical-clarity vantage point:

- **Bug-free against scope:** Fail — see P0-1 (vacuum Left/Right semantics).
- **Security:** N/A (offline algorithm code; no I/O surface).
- **Performance:** N/A for this review (Reviewer #1's territory).
- **Accessibility:** N/A (no UI).
- **DOCUMENT.md present in every modified directory:** Not evaluated (no project-wide doc system in this repo as far as I can see; lab files are standalone).
- **Conventions from PM/conventions.md followed:** N/A (no PM/ folder).
- **Docstring + comment quality:** Mixed. KNOB block is exemplary; class/method docstrings are uneven (P1-3, P1-4, P1-5 above).
- **MENTAL MODEL consistent with L03:** Mostly yes for BFS/DFS framing, but with the gaps P0-2, P1-1, P1-6 above.

### Acceptance criteria status

I have no Feature Plan §1 to score against. The lab handout's acceptance criteria (paraphrased from the file's PROBLEM STATEMENT block):

- Ex 1 `insert/insert_all/remove_first` implemented and demonstrated → **Met.**
- Ex 1 fringe trace printed after each expansion → **Met** (line 502-505).
- Ex 2 vacuum world BFS produces a clean state → **Met by output, but P0-1 means the underlying transition table does not match the handout's hint.**
- Homework river-crossing BFS finds the 7-step solution → **Met.**

### DOCUMENT.md audit

Not applicable in this repository at this path.

### Out-of-scope observations

- The `Self` type from `typing` in the original Search.py (Python 3.11+) is preserved in the solution. Acceptable, but a brief comment "requires Python ≥3.11 for `typing.Self`" would help a student on an older runtime.
- The solution preserves the original template's print-on-missing-state-space behaviour (line 342). Reviewer #1 may want to escalate that to a `ValueError`; from a pedagogical standpoint the preserved behaviour matches the lab template, so I do not file it here.
- No tests of any kind. A `pytest`-style block exercising the three demos against expected outputs would let students experiment with the KNOBs without breaking the lab's expected outputs. Out of pedagogical-clarity scope but worth flagging.

### Concerns / risks

- **The single biggest risk** is P0-1 (vacuum Left/Right semantics). A student who studies this file as the canonical L03 vacuum-world implementation and then sees an exam question asking "give the successor states of `('A','Dirty','Dirty')`" will write the wrong table. This is a pedagogically *dangerous* divergence dressed up in a confident-sounding comment.
- **The second-biggest risk** is the MENTAL MODEL's silence on graph-vs-tree search (P0-2). The KNOB does the right thing, but the top-of-file mental model that the student will actually *read first* does not flag what is being toggled.
- **The third** is the unstated DFS-left-first convention (P0-3 / P2-7). A student trying to reproduce a DFS hand-trace from this file against L03 §5.5 will hit a moment of "why does this work?" with no comment to anchor them.

### What PM should do next

1. **Send back to `pm-frontend` (or the engineer who wrote this file)** to fix all three P0s before App Tester sees it.
2. **Specifically demand:**
   - Vacuum Left/Right semantics anchored to L03 §5.1's definitions, with a side-by-side comparison of the successor table for `('A','Dirty','Dirty')` against the handout's hint as a comment.
   - One sentence in the MENTAL MODEL naming the graph-search-vs-tree-search switch.
   - A docstring on `Node.expand` and on `Searcher.tree_search` connecting the double-reversal to L03 §5.5's left-first convention.
3. **After P0s are closed,** sweep P1-1 (fake quote), P1-3/4/5 (missing docstrings on `path`, `successor`, `_is_goal`, `Searcher.__init__`, `Searcher.run`), and P1-8 (slicing comment is wrong about the mechanism).
4. **Re-run Reviewer #3 once the above lands**; do not proceed to Reviewer #4 / App Tester with the vacuum bug live.

**DOCUMENT.md updated:** N/A for QA.
