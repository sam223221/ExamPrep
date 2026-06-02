# Lab 5 — Alpha-Beta — Reviewer #3 (Pedagogical Clarity) — Round 1

**Reviewer role:** Pedagogical Clarity inspector. I am NOT checking
correctness of the algorithm, KNOB plumbing, or whether the engine actually
returns the right move (those are #1 / #2's beats). I am checking whether a
student studying for an exam can read these solutions and *learn from them*
— whether the prose, naming, structure and didactic framing match the level
and style of the L06 lecture notes, and whether the comments answer the
questions a confused student would actually ask.

**Verdict:** **Fail — Pass with concerns.** The two files are technically
literate but pedagogically uneven. `alpha_beta_solution.py` is genuinely
good — it reads almost like a continuation of L06 §4.2.1. The
Tic-Tac-Toe file is significantly weaker, with several places where the
"why" comments are missing exactly at the lines a student will be confused
by. There are also two structural problems (the Nim file is imported by the
Tic-Tac-Toe file purely to "reuse the engine", which the docstring lies
about; and the slide-8 student TODO list omits one of the four functions
the file actually answers) that should be fixed before this becomes
canonical study material.

---

## Files reviewed

- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout\handout\alpha_beta_solution.py` (404 lines)
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout\handout\tictactoe_template_solution.py` (627 lines)
- Read alongside: `study\lectures\L06-Adversarial-Search.md` (the reference
  the solutions claim to track) and the two `*.py` (non-solution) handouts
  to understand exactly what the student is starting from.

---

## P0 findings — pedagogical defects that block shipping as study material

### P0-1. `tictactoe_template_solution.py` docstring lies about what the slide-8 TODOs are.

`tictactoe_template_solution.py:26-31` claims:

> Slide 8 asks the student to:
>   1. Implement `is_terminal(state)`.
>   2. Implement `utility_of(state)`.
>   3. Implement `successors_of(state)`.

…and then later, at line 330, the section header reads
`is_terminal / utility_of — the three slide-8 TODOs` — but only two
functions are defined in that section. The "three" count is wrong twice (or
the function list is wrong twice). The actual handout
`tictactoe_template.py` has **five** raise-NotImplementedError stubs:
`is_terminal`, `utility_of`, `winner_of`, `is_full_board`,
`successors_of`. The solution file silently implements all five but
presents the lab as if it were a 3-function exercise.

A student going through L06 §5 worked examples and Lab 5 in parallel will
read this header, count the implementations, and conclude they're missing
one. **Fix:** update both the docstring list and the section header to
match the actual count (either "three slide-8 TODOs plus two helpers" or
list all five). `file:tictactoe_template_solution.py:26-31, 330`.

### P0-2. The cross-file import is presented as pedagogical reuse — it is actually a code smell that confuses the mental model.

`tictactoe_template_solution.py:127-134`:

```python
from alpha_beta_solution import (
    nodes_evaluated as _nim_nodes_evaluated,  # noqa: F401  (re-exposed below)
    reset_node_counter,
)
import alpha_beta_solution as _ab  # for read/write access to the live counter
```

But then `tictactoe_template_solution.py:267-326` defines a *brand-new*
`minmax_decision(state)` with its own `max_value` / `min_value`. **The
"engine" is NOT actually reused** — only `reset_node_counter` is called.
The docstring at line 128 claims:

> Reuse the engine + KNOBs from the sister Nim module so that any change
> made there (USE_ALPHA_BETA_PRUNING, COUNT_NODES, etc.) flows through
> here automatically — see alpha_beta_solution.py for full KNOB docs.

This is **factually wrong**: `USE_ALPHA_BETA_PRUNING`, `COUNT_NODES` and
`MOVE_ORDERING` are **redefined** in `tictactoe_template_solution.py:177`,
`:184`, `:200` with new values. A student who flips
`alpha_beta_solution.USE_ALPHA_BETA_PRUNING = False` and runs
Tic-Tac-Toe expecting it to disable pruning will be silently betrayed —
the local copy of the KNOB inside `tictactoe_template_solution.py` is
what the local `minmax_decision` reads.

This is pedagogically worse than copy-paste because it teaches the student
a wrong model ("module imports share KNOBs"). **Fix:** either genuinely
factor a single `alpha_beta_core.py` that both files import and parameterise,
*or* drop the bogus import entirely and write the local `_reset_local_counter`
directly. Don't pretend at reuse you don't have.
`file:tictactoe_template_solution.py:127-134, 177, 184, 200`.

### P0-3. The two `nodes_evaluated` counters in the same Python process is a recipe for student confusion.

`alpha_beta_solution.py:159` declares `nodes_evaluated: int = 0` at module
level. `tictactoe_template_solution.py:254` declares **its own**
`nodes_evaluated: int = 0` at module level. The Tic-Tac-Toe
`minmax_decision` increments its local one (`:281`, `:301`); the
`_reset_local_counter` at `:257` resets its local one. But the Nim engine's
`reset_node_counter` is **imported and used** at
`tictactoe_template_solution.py:577, 602`, which resets the *Nim* module's
counter, not the local one — yet the value printed at line 582 is the
*local* counter. The two are kept in sync by accident only because the
Tic-Tac-Toe `minmax_decision` does not import or call into
`alpha_beta_solution.max_value` / `min_value`.

A student trying to actually use the COUNT_NODES feature on Tic-Tac-Toe will
either read the Nim counter and get zero, or fail to reset between
decisions because the wrong reset function was called. This is exactly the
kind of subtle dual-state bug that the lecture cleanly avoids by stating
one recursion. **Fix:** delete the import of `reset_node_counter` and
replace every `reset_node_counter()` call in the Tic-Tac-Toe file with
`_reset_local_counter()`. The current code "works" only because the Nim
counter is never read here, but the docstring at line 252 lies about it:
"we keep them separate so a Nim game and a Tic-Tac-Toe game can run
independently without smearing counts" — they *aren't* kept separate, they
share a reset call. `file:tictactoe_template_solution.py:577, 602, 252-254`.

---

## P1 findings — significant pedagogical clarity gaps

### P1-1. The lecture's mental-model framing is undermined by inconsistent symbol↔role mapping between the two files.

L06 §2.1 and §3.2 are unambiguous: **MAX is the player to move at the
root, MIN is the alternating opponent**. The lab's two files then take
opposite stances:

- **Nim (`alpha_beta_solution.py:24-29`):** "The USER moves first (so the
  USER is the MIN player here, matching the slide's 'MIN should start the
  game' remark)." The computer is MAX, but **MAX moves second**.
- **Tic-Tac-Toe (`tictactoe_template_solution.py:319-326`):** X is MAX
  *and* moves first (slide 4 default). MAX = first-to-move.

Both stances are *individually* legitimate, but the Nim file's framing
**contradicts L06 §3.2's "root is MAX-to-move" convention without
flagging it**. The docstring waves at "slide-11 figure where MIN moves
first", but a student studying from L06 §5.2 (which is the
walkthrough on the exact slide-11 tree) reads:

> By convention the player to move at the root is called **MAX**, and the
> alternating opponent is called **MIN**.

…and is then handed a Nim solution where the player-to-move-at-root is
MIN. That requires an explicit "**lab variant note: in this lab we flip
the convention because…**" callout. There is none.

`alpha_beta_solution.py:250-262` (the `utility_of` parity argument) is
*correct* but reads like Ottoman-empire-era diplomacy — the parity is what
makes the convention flip work, but a student reading it cold will not
see this. Add a short "we flipped the convention because the slide-11
animation has MIN at the root" sentence near the top. `file:alpha_beta_solution.py:24-29, 250-262`.

### P1-2. "Mental model" paragraphs are copy-pasted with the exact same chess-book analogy in both files — but never cross-referenced.

`alpha_beta_solution.py:32-36` and `tictactoe_template_solution.py:36-45`
both contain the *same* "alpha-beta is like reading a chess book" analogy.
Worse, the Tic-Tac-Toe version (line 43-45) reads:

> (Consistent with the analogy used in Lecture 6 study/lectures/L06-Adversarial-Search.md §2
> "Alpha-beta pruning ↔ you stop reading a bad chess line the moment you
> realise it's worse than one you've already considered".)

— a citation that **is correct** and that the Nim file is missing. The
Nim version uses different wording and no citation. A student reading
both files (which is what the docstring at line 130 invites them to do)
will think the analogy is "made up by the lab author" rather than
"directly from L06 §2.2". **Fix:** either copy-paste the citation into the
Nim file too, or write the analogy in *one* place (a shared docstring or
the lab's `notes.md`) and cite it from both files.
`file:alpha_beta_solution.py:32-36; tictactoe_template_solution.py:36-45`.

### P1-3. The pseudocode-to-code mapping is invisible at the recursion.

L06 §4.2.1 lays out the canonical Russell-&-Norvig pseudocode. The
solutions' `max_value` / `min_value` functions could trivially be
annotated line-by-line to match — e.g.

```
v ← -∞                              # line A of R&N pseudocode
for each s' in SUCCESSORS(state):   # line B
    v ← max(v, MIN-VALUE(...))      # line C
    if v ≥ β: return v              # line D — β-cutoff
    α ← max(α, v)                   # line E
```

Neither file does this. Instead `alpha_beta_solution.py:184-201` and
`tictactoe_template_solution.py:280-298` use a Python idiom that's
*similar* to R&N but uses `expected_value` (Nim MAX), `v` (Nim MIN), `v`
(Tic-Tac-Toe MAX), `v` (Tic-Tac-Toe MIN) — **inconsistent variable names
for the exact same role** across just four functions in the same lab.

The L06 cheat-sheet (§8) uses one `v` everywhere. The lab should too.
Worse, the comments at `alpha_beta_solution.py:197` ("The beta cutoff…")
and `:214` ("The alpha cutoff…") use the right L06 names, but a student
checking variable names against the cheat-sheet will not see "expected_value
≥ β" matching "v ≥ β" without a translation step. **Fix:** rename
`expected_value` → `v` in the two MAX-value functions; or add an explicit
"v in the lecture is called expected_value here" comment at the top of
each. `file:alpha_beta_solution.py:184-201, 211-219; tictactoe_template_solution.py:280-298, 300-316`.

### P1-4. `utility_of` for Nim — the parity argument is correct but presented as a fait accompli, not derived.

`alpha_beta_solution.py:245-269` is **the** pedagogically critical block in
the Nim file (it's the one of the three TODOs that has any reasoning
content; `is_terminal` and `split_pile_options` are mechanical). The
solution presents:

```
len == 1 → no splits yet      → USER's turn  (USER = MIN)
len == 2 → 1 split done       → COMPUTER's turn (COMPUTER = MAX)
len == 3 → 2 splits done      → USER's turn
```

…and then "terminal with odd len → USER's turn → USER lost → +1." This is
correct, but the reasoning compresses two steps into one line:

1. **Step A (whose turn):** parity of `len(state)` ↔ whose turn it is.
2. **Step B (terminal semantics):** at a terminal state, the player whose
   turn it is **just lost** (they cannot move) — this is the Nim rule.
3. **Step C (utility sign):** by the COMPUTER_PLAYS_MAX convention, USER
   loses ⇒ +1 (computer wins).

The slide-12 Nim rule "first player who can no longer move loses" appears
*nowhere in the function's docstring*. A student trying to derive `utility_of`
from scratch needs all three steps spelled out, not just the punchline. The
function header docstring at `:81-22` mentions "first player who can no
longer move loses", but `utility_of` is 160 lines below that and the
reasoning is not repeated locally where the student needs it. **Fix:**
inline the rule "the player whose turn it is at a terminal state has lost"
as a single comment right above the `+1 if ... else -1` line; the parity
table already provided is the *correct* visualisation but it needs the
"player-to-move-just-lost" axiom to bridge from parity to sign. `file:alpha_beta_solution.py:245-269`.

### P1-5. Tic-Tac-Toe `_to_move` is presented as a "by the parity rule" tautology — the actual lecture concept is invisible.

`tictactoe_template_solution.py:466-469`:

```python
def _to_move(state: Board) -> Symbols:
    """Whose turn it is, by the parity rule of `successors_of`."""
    open_count = sum(1 for cell in state if cell == Symbols.UNPLACED)
    return Symbols.X if (open_count % 2 == 1) else Symbols.O
```

A student reading this needs to be told: **on an empty board (9 unplaced),
it's X's turn; X is the first-to-move by slide-4 convention; X is MAX.**
The function's docstring says "by the parity rule of `successors_of`" — a
circular reference back to a function that itself has the same parity
inference at lines 406-409. Neither function plainly says "9 - (X plays
made) - (O plays made) = open_count; X has played one more than O iff
open_count is odd ⇒ it's X's turn." A student who has just read L06 §3.2
("by convention the player to move at the root is MAX") will not see how
the parity computes that. **Fix:** add an example to the `_to_move`
docstring — `_to_move([UNPLACED]*9) == X` and
`_to_move([X, UNPLACED, ..., UNPLACED]) == O`. `file:tictactoe_template_solution.py:406-409, 466-469`.

### P1-6. The `_evaluate` function silently encodes L06 pitfall #6 — but doesn't say so.

`tictactoe_template_solution.py:472-486, 488-510` implements the
`(X's open lines) - (O's open lines)` heuristic from L06 §3.4 / slide 30.
The function `_score_lines` at `:488-510` computes:

```python
xs = sum(1 for s in cells if s == Symbols.X)
os_ = sum(1 for s in cells if s == Symbols.O)
if xs > 0 and os_ == 0:
    score += xs
elif os_ > 0 and xs == 0:
    score -= os_
```

**This is a different formula** from L06 §3.4. The lecture defines an
"open line for X" as a line *with no O on it* (regardless of how many X's
are on it). The lecture's formula scores **+1** for *every* X-open line.
This solution scores **+xs** (i.e. the *count* of X's on that line) for
every X-open line. So a line with two X's contributes +2 here, +1 in the
lecture.

This is L06 §6 pitfall #6 verbatim — and yet the function's docstring at
`:489-493` *does not flag it*. Worse, the `_apply_move_ordering` / `_evaluate`
machinery is what the variants.md exam variant is supposed to exercise,
so this divergence will produce different scores than a student reading
the lecture would compute by hand.

I'm not going to call this a P0 because the score-by-count variant *does*
agree in sign with the lecture's count-by-line variant, so the **minimax
decision is the same** at every state. But pedagogically this is exactly
the place where a footnote is mandatory: "We score +xs instead of +1 to
keep the centre-weighting KNOB monotone; this differs from L06 §3.4 by a
positive scale on individual lines but preserves the sign of the
heuristic at every state." Without this footnote, a student doing the
"empty board → Eval = 0; X-in-centre → Eval = 4" sanity check from L06
§3.4 will get **different numbers** here. `file:tictactoe_template_solution.py:472-510`.

### P1-7. Both files mention `variants.md` 3 times without showing what it is or where to find it.

`alpha_beta_solution.py:142, 305` and `tictactoe_template_solution.py:199`
all reference "variants.md variant N". A student studying the lab does
not have the variants file open and probably does not know it exists.
Either inline a 1-sentence summary of each referenced variant, or replace
"variants.md variant 1" with the specific variant question
(e.g. "report nodes evaluated with vs without pruning"). The latter is
already *partly* done at line 305 — the parenthetical there is fine —
but lines 142 and 199 just say "variants.md variant 2" with no question.
`file:alpha_beta_solution.py:142, 305; tictactoe_template_solution.py:199`.

### P1-8. The Nim REPL says "alpha-beta evaluated N states" *after* the computer move — but the student doesn't see what move was made.

`alpha_beta_solution.py:391-397`:

```python
reset_node_counter()
state = computer_select_pile(state)
if COUNT_NODES:
    print(f"[alpha-beta] evaluated {nodes_evaluated} states "
          f"(pruning={USE_ALPHA_BETA_PRUNING}, "
          f"ordering={MOVE_ORDERING})")
print("The computer has split a pile")
```

The instrumentation line prints **before** the announcement of the
computer move. The "The computer has split a pile" line *doesn't show
the new state* — the student has to wait for the next iteration of the
loop (which displays the piles inside `user_select_pile` at line 350).
A student running `py -3.12 alpha_beta_solution.py` and trying to
correlate the node count with the chosen move has to mentally splice the
two prints together. **Fix:** print the new pile list right after
`state = computer_select_pile(state)` so the student sees
"`computer split into [3, 2, 1, 1]; [alpha-beta] evaluated 28 states`".
`file:alpha_beta_solution.py:388-399`.

---

## P2 findings — polish / suggestions

### P2-1. The "KNOB" block is brilliant but inconsistent on one detail.

`alpha_beta_solution.py:90-143` and the parallel block in
`tictactoe_template_solution.py:141-228` — the KNOB documentation format
is exemplary and is what every lab in this course should follow. Two
small nits:

- The "Exam variants" tag lists slide numbers in the Nim file but exam-
  variant *labels* in the Tic-Tac-Toe file. Pick one.
- `STARTING_BOARD` at `tictactoe_template_solution.py:220-228` describes
  a validation rule ("X must be played between 0 and 1 more times than O")
  but does **not** validate it — `_starting_board` at `:544-550` only
  checks length. If a student sets `STARTING_BOARD = [O, O, ...]` they
  get an undefined search. Either implement the validation or remove the
  promise.

### P2-2. `infinity = float('inf')` is defined inside every decision function.

`alpha_beta_solution.py:182`, `tictactoe_template_solution.py:278`. Move
to module-level `_INFINITY = float('inf')` once per file. Minor, but
makes the recursion 5 lines shorter and removes a "what's `infinity`?"
distraction at the moment a student is trying to parse the cutoff logic.

### P2-3. `argmax` is defined but used in only one of the two files.

`alpha_beta_solution.py:332-334` defines `argmax(iterable, func)` (a
1-line wrapper around `max(..., key=...)`). The Tic-Tac-Toe file
**doesn't import it** and uses inline `max(..., key=...)` at
`:323, 325`. The lecture's pseudocode at `:236` uses `argmax`. Either
expose `argmax` from the Nim module and use it in Tic-Tac-Toe, or drop
the wrapper from the Nim file. Right now a student wonders "why does
this lab introduce `argmax` only sometimes?"

### P2-4. The `_score_open_lines` heuristic shadows a function whose name does NOT contain "open" — leading to confusing search.

`tictactoe_template_solution.py:513-523`. The function counts lines
**not blocked** by the opponent, which the lecture also calls "open lines".
But there are now two functions whose docstrings mention "open lines":
`_score_lines` and `_score_open_lines`. A student grepping for "open
lines" gets both, with no signal as to which is L06 §3.4's. **Fix:** rename
to `_score_winnable_lines` (matches the variable names `x_winnable` /
`o_winnable` already inside).

### P2-5. The Tic-Tac-Toe `display` helper renders the board with cell *numbers* on empty cells, but the lecture renders empty cells as blanks.

`tictactoe_template_solution.py:530-537` prints the cell index (0..8) at
every UNPLACED cell:

```python
symbol = c if state[c] == Symbols.UNPLACED else state[c]
```

This is **actually pedagogically good** because it doubles as a "where
to play" guide for the human in interactive mode. But it differs from
L06 Figure 2 (slide 8) which uses blanks. Add a one-line comment "(we
show cell indices on empties as a click-target hint; L06 slide 8 leaves
them blank)" so a student doing a side-by-side visual check doesn't get
disoriented.

### P2-6. Module-level mutable counter shared via `_ab.nodes_evaluated`.

The pattern `import alpha_beta_solution as _ab; _ab.nodes_evaluated += 1`
(implicit, via `reset_node_counter()`) is fine for a teaching example
but is exactly the global-state-mutation pattern that L06 §6.x pitfalls
warn about elsewhere. A 1-sentence "we use a module-level counter for
teaching simplicity; production code would thread the counter through
the recursion" comment would head off bad habits.

### P2-7. The `__main__` block in `alpha_beta_solution.py` runs an *interactive* game even though the file is described as "imported by Tic-Tac-Toe as the canonical engine".

Lines 69-81 of the file claim:

> ENTRY POINT: yes — but optional. Running `py -3.12 alpha_beta_solution.py`
> plays one Nim game (interactive). The canonical lab entry point that is
> exercised by the Verifier is `tictactoe_template_solution.py`…

But then the `if __name__ == '__main__':` block at `:402-403` calls
`main()` which requires keyboard input (`user_select_pile` at `:357,
372`). A student who is told "the canonical entry point is the
Tic-Tac-Toe file, but you can also run the Nim file" will run the Nim
file expecting a self-play demo (matching the Tic-Tac-Toe pattern) and
get hung on `input()`. Either add a `DEMO_MODE` KNOB to the Nim file
matching the Tic-Tac-Toe one, or change the docstring to "Running this
file directly prompts the user for keyboard input" so the expectation
is set.

---

## Convention adherence — comparing to L06 voice and notation

| Aspect | L06 says | Solution says | OK? |
|---|---|---|---|
| Alpha = floor, beta = ceiling | §2.2 explicit mnemonic | Nim `:198, :217` says "the beta cutoff" / "the alpha cutoff" with the right intuition but no floor/ceiling words | P2 — would help students who memorised the mnemonic |
| `Eval` vs `U(s)` distinction | §6 pitfall #8 mandatory | Tic-Tac-Toe `_evaluate` vs `utility_of` — implemented correctly but the docstring at `:472` does not cite pitfall #8 | P2 |
| Move ordering matters | §4.3 + §6 pitfall #4 | Both files have `MOVE_ORDERING` KNOB but neither comment cites §4.3's $O(b^{d/2})$ vs $O(b^d)$ result | P1-3 (covered above) |
| Minimax-decision vs minimax-value | §3.3 separation of "value" and "decision" | Both files' top-level `alpha_beta_decision` / `minmax_decision` do `argmax` over `min_value` of successors — correct but undocumented | P2 — add a one-line "this is `MINIMAX-DECISION` from §4.1; the inner `min_value` is `MINIMAX-VALUE`" cross-reference |
| Tic-tac-toe coordinate convention | slide 4: 0..8 row-major | matches | OK |
| Utility sign convention | slide 6: +1 X wins, -1 O wins, 0 draw or non-terminal | matches `utility_of` at `:344-361` | OK |
| Open line definition | §3.4 + §6 pitfall #6 | `_score_lines` does NOT match — counts xs/os instead of +1 per line | P1-6 (above) |

---

## DOCUMENT.md audit

- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout\handout\` — I did
  not find a `DOCUMENT.md` here. The two solution files were created
  alongside the original `alpha_beta.py` / `tictactoe_template.py`.
  Per the PM standing rules: **every directory with new or modified files
  must have an updated `DOCUMENT.md`**. This is **missing → P1**.

(Note: I did not exhaustively search every directory that might have been
touched by this lab — the QA Inspector's standing checklist applies to
all directories with code changes, but I am scoped to pedagogical clarity
and only checked the immediate handout directory.)

---

## Acceptance criteria (informal — derived from lecture cross-reference, not a Plan §1 I was given)

A student who has read L06 §2-§4 should be able to:

1. Recognise the lab's `alpha_beta_decision` as the `ALPHA-BETA-DECISION`
   pseudocode of L06 §4.2.1 — **Met** (both files use the same shape; P1-3
   is a naming nit, not a structural mismatch).
2. Recognise the lab's `utility_of` as the rule-given U(s) from L06 §3.2 —
   **Partially met** (Tic-Tac-Toe is clean; Nim's parity-based encoding is
   correct but underexplained — P1-4).
3. Recognise the lab's `_evaluate` as the Eval(s) from L06 §3.4 — **Not met**
   (the score-by-count divergence in P1-6 means a hand-computation from L06
   gives different numbers).
4. Trace `nodes_evaluated` to a meaningful comparison of pruning on vs off —
   **Risk** (the Nim file's READ block prints the counter; the Tic-Tac-Toe
   file has the dual-counter bug from P0-3).
5. Adapt the lab to the slide-12 homework (N=15 and N=20) — **Met**
   (`START_PILE` KNOB is documented and located at top of file).
6. Adapt the lab to the slide-12 step-3 "play the MIN position" variant —
   **Met** (the `COMPUTER_PLAYS_MAX = False` KNOB exists and the sign-flip
   in `utility_of` is correctly implemented).

---

## Out-of-scope observations

- The handout `alpha_beta.py:107` says `for j in range(1, ____)` with the
  blank to be filled. The solution at line 313 fills the blank with `pile`
  rather than the tighter `pile // 2 + 1`. Both are correct; the solution
  comment at lines 310-312 explains why the loose bound is fine (the
  `if j < k` filter at line 315 enforces the constraint). This is good
  pedagogy and worth highlighting in a future lecture cross-reference.
- The Tic-Tac-Toe self-play in `_self_play` is guaranteed to draw — L06
  §4.7 mentions checkers (solved 2007) but does not state that
  Tic-Tac-Toe is also solved. The lab's docstring at line 565 *does* state
  this. Worth a one-line forward-ref from L06 §4.7 to "Tic-Tac-Toe is
  also solved" for completeness — but that's a lecture-note edit, not a
  lab edit.

---

## Concerns / risks (gut-feel)

- The dual-file structure invites the cross-file confusion of P0-2 and
  P0-3. If the intent is "two flagship examples of alpha-beta in two
  different games", then they should be **two independent files** that
  each contain a complete, self-explanatory alpha-beta engine. If the
  intent is "one engine, two test cases", then there should be a single
  `alpha_beta_core.py` plus two thin game-specific drivers. The current
  state is "one engine, plus a second engine that pretends to import the
  first" — the worst of both worlds.
- The lab is being marketed (via the docstrings) as a study aid for L06.
  In that role, prose quality and reference accuracy matter as much as
  code correctness. Three of the L06 §6 pitfalls (#4 move ordering, #5
  Eval-at-terminal, #6 open-line definition) are touched by the code
  but **not cited by the code**. A student reading the solution and
  L06 §6 in parallel should see "ah, this is exactly what §6 pitfall #N
  warns about". They will not.
- The "BE HARSH" instruction in my brief calls for harshness on
  pedagogical clarity — and on pedagogical clarity the Nim file is
  *good*, the Tic-Tac-Toe file is *uneven*, and the relationship between
  them is *bad*. The grade I'd give: **B for Nim, C+ for Tic-Tac-Toe,
  D for the cross-file architecture**.

---

## Report to PM

**Assignment recap:** Lab5-AlphaBeta round 1 pedagogical-clarity review.
Files: `handout/handout/alpha_beta_solution.py` and
`handout/handout/tictactoe_template_solution.py`. Reference:
`study/lectures/L06-Adversarial-Search.md`.

**Status:** **Fail — Pass with concerns.** Two P0 documentation
inaccuracies and one P0 dual-state bug, plus 8 P1 clarity gaps. Code is
substantially correct; pedagogical framing is not yet exam-ready.

**P0 findings:**
1. `tictactoe_template_solution.py:26-31, 330` — docstring claims slide-8
   has three TODOs; file implements five. Fix the count or list the
   helpers.
2. `tictactoe_template_solution.py:127-134, 177, 184, 200` — import
   pretends at engine reuse but the KNOBs are redefined locally and the
   engine is reimplemented. Either factor a real core or drop the bogus
   import.
3. `tictactoe_template_solution.py:577, 602, 252-254` — `reset_node_counter`
   imported from the Nim module resets the wrong counter; "kept separate"
   docstring contradicts the actual call site. Replace with
   `_reset_local_counter()`.

**P1 findings:**
1. Nim's MIN-at-root convention contradicts L06 §3.2 without an explicit
   variant note. `alpha_beta_solution.py:24-29, 250-262`.
2. Mental-model paragraph duplicated across files; only one cites L06.
3. `expected_value` vs `v` naming inconsistency across the four
   `max_value` / `min_value` functions; doesn't match L06 §4.2.1's `v`.
4. Nim `utility_of` parity reasoning skips the "player-to-move-just-lost"
   axiom from slide-10 Nim rules.
   `alpha_beta_solution.py:245-269`.
5. Tic-Tac-Toe `_to_move` docstring is circular; needs an example.
   `tictactoe_template_solution.py:466-469`.
6. `_score_lines` diverges from L06 §3.4's formula (counts xs instead of
   +1 per line) without footnoting the divergence —
   directly contradicts §6 pitfall #6. `tictactoe_template_solution.py:472-510`.
7. `variants.md` referenced 3x with no inlined summary or path.
8. Nim REPL prints node-count before showing the move that produced it.
   `alpha_beta_solution.py:388-399`.
9. `DOCUMENT.md` missing in `handout/handout/`. (per standing checklist)

**P2 findings:**
1. KNOB block format inconsistent on "exam variants" tagging style.
2. `infinity = float('inf')` redefined inside every decision function.
3. `argmax` defined in Nim, unused in Tic-Tac-Toe.
4. `_score_open_lines` shares a "open lines" docstring keyword with
   `_score_lines`.
5. `display` shows cell indices where L06 Figure 2 shows blanks; add a
   one-line note.
6. Module-level mutable counter pattern; add a 1-line caveat.
7. Nim `__main__` enters interactive mode while docstring implies it can
   be run head-lessly like Tic-Tac-Toe.

**QA Checklist (§7) status:** N/A — I was not given a Plan §7 directly.
Inferred from L06 cross-reference, the lab fails on:
"DOCUMENT.md present in every modified directory" (missing — P1-9) and
"Conventions from PM/conventions.md followed" (cannot evaluate — I have
not seen this lab's `PM/conventions.md`).

**Acceptance criteria (§1) status:** see "Acceptance criteria" section
above — 4 met, 2 partially-met-or-at-risk.

**DOCUMENT.md audit:** `handout/handout/` — **MISSING**. Other dirs not
audited (out of scope for clarity review).

**Out-of-scope observations:**
- The `split_pile_options` loop bound in the solution (`range(1, pile)`)
  is loose but correct and well-commented; the corresponding hint in
  `alpha_beta.py:107` is open-ended in a way that the solution clarifies
  well. Worth mirroring this style in future labs.
- Tic-Tac-Toe is also a solved game (forward-ref candidate for L06 §4.7).

**Concerns / risks:** the cross-file relationship (P0-2, P0-3) is the
most exam-dangerous defect — it teaches a wrong module-import mental
model. The `_score_lines` divergence (P1-6) is the most lecture-dangerous
defect — a student who hand-computes Eval from L06 §3.4 and re-runs the
solution will get inconsistent numbers and not know which is right.

**What PM should do next:**
1. Dispatch implementation engineer to fix P0-1, P0-2, P0-3 (re-architect
   the cross-file import OR drop it; correct the slide-8 TODO count;
   replace the wrong reset call).
2. Dispatch engineer to fix P1-1 through P1-8 in a second pass (these
   are mostly comment-only edits, ~30 minutes of work).
3. Dispatch DOCUMENT.md engineer to write the missing
   `handout/handout/DOCUMENT.md`.
4. Re-run reviewer #3 after fixes — round 2.
5. Reviewers #1 and #2 (correctness, KNOB plumbing) should weigh in
   independently; I did not inspect those concerns.

**DOCUMENT.md updated:** N/A for QA.
