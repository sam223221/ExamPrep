# Reviewer 4 — Lab5-AlphaBeta — Round 1

Reviewer focus: **Variant Adaptability** (can a fresh exam agent solve
each variants.md item using ONLY KNOB blocks + docstrings + signatures
— without reading any function body?).

Files audited:
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout\handout\alpha_beta_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout\handout\tictactoe_template_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout\handout\Lab 5.pdf` (slides 4-12)
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab5-AlphaBeta\variants.md`
- Original templates `alpha_beta.py`, `tictactoe_template.py` (for diff context)

Mode: I executed each variant programmatically to verify the
KNOBs-only contract. Findings below cite empirical evidence.

---

## Report to PM

**Assignment recap:** Lab 5 — Alpha-Beta Pruning. Round-1 review #4 of
4. Charter: variant adaptability — verify every variant in
`variants.md` is solvable from KNOBs alone, and that the documented
expected outputs match reality.

**Status:** **Fail** — 2 P0 findings (one variant is empirically
degenerate; one expected-result assertion is false); plus multiple P1
docstring/KNOB-contract defects that will leave a fresh exam agent
either stuck or producing a misleading transcript.

---

### P0 findings

**P0-1. Variant 2 ("centre-weighted evaluator") is empirically a
no-op at the documented `MAX_DEPTH = 2` setting.**

- File: `study/_exam/Lab5-AlphaBeta/variants.md` lines 50-75.
- Empirical evidence (executed at `c:\...\handout\handout`):

  | EVALUATOR        | MAX_DEPTH | Move sequence                                          | Winner |
  |------------------|-----------|--------------------------------------------------------|--------|
  | `lines`          | 2         | X4, O0, X2, O6, X3, O5, X8, O1, X7                     | draw   |
  | `center-weighted`| 2         | X4, O0, X2, O6, X3, O5, X8, O1, X7 (BYTE-IDENTICAL)    | draw   |
  | `lines`          | 1         | X4, O0, X2, O6, X3, O5, X7, O1, X8                     | draw   |
  | `center-weighted`| 1         | X4, O0, X2, O6, X3, O5, X7, O1, X8 (BYTE-IDENTICAL)    | draw   |

- The variant explicitly asks the student to "Compare the final
  board, the per-ply moves, and the winner against the run with
  `EVALUATOR = 'lines'` and same `MAX_DEPTH`" — but they are
  identical. There is nothing to report.
- Root cause: `_score_lines` already counts presence-per-line, which
  scores the centre at +4 per ownership (centre participates in 4
  winning lines). The `center_weight=3` term in `_score_lines` only
  adds `(3-1)=+2` extra, which is **insufficient to change ordinal
  rankings** when the centre is already dominant under `lines`. The
  variant fails to demonstrate centre-weighting in a way the student
  can see.
- Suggested fix (variants.md and/or solution):
  - Either increase the contrast (e.g. instruct `MAX_DEPTH = 1` AND
    a `STARTING_BOARD` where centre is contested, e.g.
    `[U,U,U,U,U,U,U,U,U]` with `EVALUATOR='lines'` already picks
    centre — so you must START FROM a centre-occupied state and ask
    O to defend);
  - OR strengthen `_score_lines` so centre weighting changes the
    ordering;
  - OR rewrite the variant to compare `lines` vs
    `rows-cols-diags` (which DO differ at depth 2 — I have not
    verified, but `_score_open_lines` is structurally different).
- Severity: **P0** — a documented variant produces a degenerate
  result, so any exam agent solving Variant 2 will write
  `VERDICT: SOLVED` while reporting "no observable difference,"
  which is the OPPOSITE of the pedagogical point.

**P0-2. Variant 3's "expected qualitative observation" prose is
empirically false for `natural` ordering.**

- File: `study/_exam/Lab5-AlphaBeta/variants.md` lines 102-106:
  > "natural sits in between (it processes cell 0 first which is a
  > corner)."
- Empirical evidence (ply 1 from empty board, MAX_DEPTH=None,
  pruning on, COUNT_NODES on):

  | MOVE_ORDERING   | Nodes on ply 1 | First move |
  |-----------------|----------------|------------|
  | natural         | 30 709         | 0          |
  | center-first    | 15 705         | 4          |
  | corners-first   | 20 666         | 0          |

  `natural` is **the worst of the three**, not "in between." A
  student following the variants.md hint will conclude their own
  result is wrong and either tamper with knobs or write
  `VERDICT: STUCK`.
- Root cause: in `_apply_move_ordering`, `corners-first` ranks
  corners (0,2,6,8) before the centre (rank 1) before edges (rank
  2). In Python's stable sort, the corners come first in the
  resulting list, but the **CENTRE LANDS AT INDEX 4** (5th item) —
  the same position the centre occupies in `natural` ordering
  (cell 4 of a 0..8 walk). The number-of-nodes difference comes
  from alpha-beta's bookkeeping on the corners (because corners
  with extreme indices participate in different sets of winning
  lines), not from a clean "centre-position" intuition.
- Suggested fix: replace the variants.md prose with the verified
  table and a one-line explanation tied to empirical numbers, NOT
  a hand-wavy "in between."
- Severity: **P0** — examiner #4's own measurement contradicts the
  variant; any other examiner will hit the same contradiction.

---

### P1 findings

**P1-1. Duplicate `USE_ALPHA_BETA_PRUNING` and `COUNT_NODES` KNOBs
across the two modules are a foot-gun.**

- Files:
  - `alpha_beta_solution.py:119` defines `USE_ALPHA_BETA_PRUNING`
  - `tictactoe_template_solution.py:177` re-defines the SAME-NAMED
    constant.
- Both Python identifiers exist; Python scoping makes the bare
  `USE_ALPHA_BETA_PRUNING` inside
  `tictactoe_template_solution.minmax_decision` resolve to the
  **tictactoe** module's copy. The bare `USE_ALPHA_BETA_PRUNING`
  inside `alpha_beta_solution.alpha_beta_decision` resolves to the
  **alpha_beta_solution** copy.
- The Tic-Tac-Toe docstring (lines 127-129) explicitly claims:
  > "any change made there (USE_ALPHA_BETA_PRUNING, COUNT_NODES,
  > etc.) flows through here automatically".
- This is **FALSE**. A student who follows that promise — sets
  `USE_ALPHA_BETA_PRUNING = False` in `alpha_beta_solution.py` and
  runs `py tictactoe_template_solution.py` — will get a transcript
  showing PRUNING-ON behaviour (15 705 nodes on ply 1, not the
  221 625 they were trying to elicit at depth 7). Their Variant 1
  table will be wrong by an order of magnitude and they will not
  know why.
- Empirical confirmation: `id(ab.USE_ALPHA_BETA_PRUNING) ==
  id(ttt.USE_ALPHA_BETA_PRUNING)` only because both happen to be the
  same singleton `True`; mutating one does not propagate.
- Suggested fix: either (a) delete the duplicates from
  `tictactoe_template_solution.py` and import the originals as
  module variables (with the caveat that imported globals are
  copies, so you'd need `_ab.USE_ALPHA_BETA_PRUNING` accessors
  throughout `minmax_decision`), or (b) state explicitly that the
  KNOBs must be edited in the SAME FILE you intend to run, and
  delete the misleading "flows through here automatically" claim.
- Severity: **P1** — every exam agent who reads the docstring
  literally will be misled.

**P1-2. Variant 1 prose "increase the minimax tree-depth limit from
3 to 7" implies a baseline of 3 that does not exist.**

- File: `variants.md` line 19.
- Default `MAX_DEPTH = None` (full-depth, slide-4 semantics). There
  is no MAX_DEPTH=3 anywhere in the solution.
- The variant's instruction block (line 28) correctly tells the
  student to "Set `MAX_DEPTH = 3`, run" — but the **question
  prose** (line 19) frames it as a baseline-vs-deeper experiment.
  The student will reasonably ask "is `3` the baseline I should
  contrast against, or is `None` the baseline?" and there is no
  answer.
- Suggested fix: change line 19 to "Set the minimax tree-depth
  limit to 3, then 7. For each, report the nodes evaluated with and
  without alpha-beta pruning."
- Severity: **P1** — ambiguity, students may produce an extra
  unnecessary `MAX_DEPTH=None` row.

**P1-3. Variant 1 instructs holding `MOVE_ORDERING` constant only
implicitly — and the default `center-first` skews the result.**

- File: `variants.md` lines 28-45.
- Default `MOVE_ORDERING = "center-first"` (line 200 of
  `tictactoe_template_solution.py`). This is NOT `natural`. A
  student who reproduces the experiment after touching Variant 3
  will see different numbers and have no docstring guidance on
  which baseline to report.
- The variant should explicitly pin
  `MOVE_ORDERING = "natural"` to make the result depend only on
  `MAX_DEPTH` and `USE_ALPHA_BETA_PRUNING`, OR state which ordering
  the expected ratio observation assumes.
- Severity: **P1** — reproducibility hazard. Two correct examiners
  will produce different numbers.

**P1-4. Variant 4 (Nim) main() loop hardcodes USER-first, breaking
slide-12 step 3 semantics.**

- File: `alpha_beta_solution.py:383-399` (`main`).
- Slide 10: "MIN should start the game."
- Slide 12 step 3: "play the MIN position" → COMPUTER plays MIN.
- Therefore when `COMPUTER_PLAYS_MAX = False` the COMPUTER (= MIN)
  must move FIRST. The current `main()` always calls
  `user_select_pile(state)` first (line 389), regardless of the
  flag.
- The docstring at lines 384-385 reinforces the bug:
  ```
  """Run one interactive Nim game starting from a single pile of START_PILE
  tokens. The user (MIN) moves first."""
  ```
  — this is only true when `COMPUTER_PLAYS_MAX=True`.
- Suggested fix:
  - Branch on `COMPUTER_PLAYS_MAX` in `main()`: if False, call
    `computer_select_pile` first.
  - Update the docstring to mention the conditional.
- Severity: **P1** — Variant 4 part 2 ("flip the roles and rerun")
  will produce a transcript where the game still has the human
  open, which is the WRONG configuration for slide-12 step 3.

**P1-5. KNOB-allowed-values are silently ignored when wrong.**

- Files:
  - `alpha_beta_solution.py:_imbalance_score`-driven branch of
    `successors_of` (lines 291-295) — unknown `MOVE_ORDERING` falls
    silently through to natural.
  - `tictactoe_template_solution.py:_apply_move_ordering` (line
    463) and `_evaluate` (line 485) — same silent fallback.
- A student who copies a Nim-only ordering value
  (`balanced-first`, `skewed-first`) into the tictactoe KNOB will
  see "natural" behaviour without any warning. Empirical
  confirmation: setting
  `tictactoe_template_solution.MOVE_ORDERING = "balanced-first"`
  returns move=0 (natural-ordering result) with no warning.
- Suggested fix: raise `ValueError(f"unknown MOVE_ORDERING:
  {MOVE_ORDERING!r}, allowed values are {{...}}")` from each
  dispatcher.
- Severity: **P1** — silent failure violates the
  KNOB-contract-by-docstring promise.

**P1-6. `MAX_DEPTH` KNOB doc says "any int >= 1" but the depth=0
case is silently accepted.**

- File: `tictactoe_template_solution.py:141-151`.
- Empirical: with `MAX_DEPTH = 0`, the top-level call passes
  `depth=1` so the very first recursion already meets the cutoff,
  but every node is still counted. The result is identical to
  `MAX_DEPTH = 1`. The docstring promises a tighter contract.
- Suggested fix: validate `MAX_DEPTH is None or MAX_DEPTH >= 1` at
  the top of `minmax_decision`, raise on violation.
- Severity: **P1** — non-binding spec; small but a tell that the
  KNOB block was not pressure-tested.

**P1-7. `STARTING_BOARD` KNOB documented but not exercised by any
variant.**

- Files: `tictactoe_template_solution.py:220-228` defines the KNOB.
- variants.md mentions "show alpha-beta from this mid-game
  position" (line 96) in passing but no concrete variant uses it.
  A student reading variants.md will not know how to populate
  `STARTING_BOARD` (what's the syntax for `Symbols.X`? Is it
  imported by name? The docstring says "list of 9 cells" but not
  HOW to construct one).
- Suggested fix: add Variant 5 (or extend Variant 2) that uses
  `STARTING_BOARD = [Symbols.X, Symbols.UNPLACED, ..., Symbols.UNPLACED]`
  with concrete import instructions. Or remove the KNOB if not
  used.
- Severity: **P1** — dead KNOB. The docstring contract is not
  tested by any variant, so the exam-time correctness of the KNOB
  is unverifiable from the agent's allowed inputs.

---

### P2 findings

**P2-1. Two module-level `nodes_evaluated` counters with the same
name across the two files.**

- Files: `alpha_beta_solution.py:159`,
  `tictactoe_template_solution.py:254`.
- The TicTacToe module imports `nodes_evaluated as
  _nim_nodes_evaluated` and then SHADOWS it with its own local. A
  reader walking the docstring will assume there's one global; in
  fact each entry point uses its own. The print line on
  `tictactoe_template_solution.py:582` reads the local; the
  `alpha_beta_solution.py` print on line 394 reads the Nim one. Not
  a bug, but confusing.
- Severity: **P2** — name collision; rename one (e.g.
  `ttt_nodes_evaluated`) to make introspection obvious.

**P2-2. `Variant 1` table has empty `?` cells where the expected
order-of-magnitude ratio should be hinted.**

- File: `variants.md` lines 33-39.
- Lab examiners benefit from a "ratio sanity check" so they catch
  obvious miscounts. The empirical numbers are: depth-3 prune-on
  208 / prune-off 585 = 2.8x; depth-7 prune-on 9 747 / prune-off
  221 625 = 22.7x. Putting an approximate ratio in the variant
  prose ("expect 2-3x at depth 3; 20-30x at depth 7") would let an
  agent catch transcription errors.
- Severity: **P2** — quality-of-life for examiners.

**P2-3. The "MIN should start" remark on slide 10 is paraphrased
into a docstring claim that "USER (MIN) moves first" (line 26 of
alpha_beta_solution.py) — but the slide-11 figure shows USER
opening only INDIRECTLY (MIN labels the topmost row).**

- File: `alpha_beta_solution.py:25-29`.
- Minor pedagogical wording — the docstring is correct for the
  default flag but elides nuance about who is MAX vs who is the
  "computer."
- Severity: **P2** — wording.

**P2-4. The handout PDF mentions a "Challenge: Solve Breakthrough"
slide (slide 13) which is not addressed by any variant.**

- Files: `Lab 5.pdf` slide 13, `variants.md` (no Breakthrough
  variant).
- Slide 13 is explicitly optional but worth noting as a possible
  extension variant.
- Severity: **P2** — scope decision; flag for PM.

**P2-5. `_score_open_lines` ("rows-cols-diags" evaluator) is
documented but never picked by any variant.**

- File: `tictactoe_template_solution.py:153-168` (KNOB) and
  `513-523` (impl).
- Like `STARTING_BOARD`, this evaluator is defined but unused.
- Severity: **P2** — dead KNOB; either exercise or remove.

**P2-6. Random seed knob `RANDOM_SEED` exists but the docstring
example does not actually demonstrate how the seed reproducibility
relates to a variant.**

- File: `tictactoe_template_solution.py:202-206`.
- Severity: **P2** — minor.

---

### QA Checklist (Plan §7) status

This is a lab review, not a feature; mapping the standing checks:

- **Scope compliance** — Solutions stay within slides 4-12 of Lab 5
  PDF. The Breakthrough challenge (slide 13) is intentionally out of
  scope. **Pass.**
- **Bugs** — `main()` USER-first hardcode under `COMPUTER_PLAYS_MAX=False`
  (P1-4); silent KNOB fallback (P1-5); duplicate KNOBs (P1-1). **Fail.**
- **Security** — N/A (no inputs from untrusted sources; only stdin
  for interactive mode which validates pile indices).
  **Pass (N/A).**
- **Performance** — Full-depth tic-tac-toe with pruning OFF at
  depth 7 evaluates 221 625 nodes (~1.5 s on my box). Acceptable
  for a lab. No N+1 or unbounded queries. **Pass.**
- **Accessibility** — N/A (CLI only). **N/A.**
- **Convention adherence** — Solution files follow the
  docstring/KNOB convention established by the project's other
  labs (verified by structural similarity, since I am forbidden
  from reading PM/conventions.md as a reviewer). **Pass.**
- **DOCUMENT.md presence** — Out of my reviewer scope to check
  every directory; flag for QA Inspector. **N/A for this charter.**
- **Tests** — No unit tests exist; variants.md substitutes. Two
  variants (2 and 3) have wrong/degenerate expected outputs
  (P0-1, P0-2). **Fail.**
- **Quality** — No TODOs/placeholders in solution files. Engineer
  did clean work modulo the contract bugs. **Pass.**

### Acceptance criteria (variant adaptability) status

Mapping each variant to "fresh agent can solve it from KNOBs alone":

- **Variant 1 (depth-limit comparison)** — **Met with caveats.**
  Functionally produces useful numbers; ambiguous baseline (P1-2)
  and unpinned MOVE_ORDERING (P1-3) hurt reproducibility.
- **Variant 2 (centre-weighted evaluator)** — **NOT MET.** Output
  is empirically degenerate (P0-1). Agent will report
  `VERDICT: SOLVED — no difference` which contradicts the
  pedagogical claim of the variant.
- **Variant 3 (move-ordering ablation)** — **Met as numbers; NOT
  MET as written observation.** Numerical tabulation is reproducible
  but the variants.md "expected qualitative observation"
  contradicts reality (P0-2). Agent will be confused.
- **Variant 4 (Nim, START_PILE 15/20)** — **Partially met.** Part 1
  is solvable. Part 2 (flip `COMPUTER_PLAYS_MAX`) is broken by P1-4
  — the game continues with the wrong opener.

### DOCUMENT.md audit

Out of variant-adaptability charter. **N/A** — defer to a sibling
reviewer.

### Out-of-scope observations

- `argmax(...)` in `alpha_beta_solution.py:332-334` is a 2-line
  wrapper around `max(..., key=...)`. Kept for fidelity to the
  handout's variable name; harmless but indirection-for-indirection's
  sake.
- The two `__pycache__` entries in `handout/handout` indicate
  someone ran the file — verify the cache is gitignored elsewhere
  (not my charter, but flagging because cache files are visible
  in `Glob` output).
- `tictactoe_template_solution.py` imports
  `nodes_evaluated as _nim_nodes_evaluated` with `# noqa: F401
  (re-exposed below)` but **never re-exposes it**. The comment is
  a lie. Dead import.
- The `Symbols.placed()` classmethod (lines 244-246) is defined
  but never called by the solution or the variants. Either expose
  it in a variant or delete it.

### Concerns / risks

1. **The "variant adaptability" promise of the lab is broken.**
   Two of four variants (Variant 2 fully, Variant 3 in its prose)
   will produce confusing or wrong outputs for any examiner who
   follows the instructions faithfully. The pedagogical purpose
   of pre-written variants — let a fresh agent succeed without
   reading bodies — fails. P0-1 and P0-2 must be fixed before any
   examiner round can be considered valid.

2. **The "KNOB changes flow across files" promise is false** (P1-1).
   This is the single most likely failure mode for an examiner:
   they read the centralised docstring at the top of
   `tictactoe_template_solution.py`, edit the wrong file, run, get
   the wrong number. They cannot debug it without reading
   function bodies — exactly the thing the spec forbids.

3. **Variant 4 has a wrong-opener bug** when
   `COMPUTER_PLAYS_MAX=False`. The slide-12 step 3 intent is not
   reproduced. Less severe than P0 only because Variant 4 is
   declared "optional bonus" in variants.md.

4. **No automated examiner-check script.** All four variants would
   benefit from a `verify_variants.py` that runs each variant
   non-interactively and prints expected/actual deltas. I can
   write this once the P0s are fixed.

### What PM should do next

1. **Fix P0-1 (Variant 2 degeneracy):** either rewrite the variant
   to use `MAX_DEPTH=1` + a non-trivial `STARTING_BOARD`, or
   change the evaluator contrast to `lines` vs `rows-cols-diags`,
   or strengthen `_score_lines` so `center_weight=3` actually
   changes rankings.
2. **Fix P0-2 (Variant 3 prose):** replace the "natural sits in
   between" sentence with the verified table values I produced
   (natural 30 709, center-first 15 705, corners-first 20 666).
3. **Fix P1-1 (duplicate KNOB foot-gun):** either delete the
   `tictactoe_template_solution.py` re-declarations and route
   through `_ab.<knob>`, or rewrite the docstring claim. Pick one.
4. **Fix P1-4 (Nim opener):** branch on `COMPUTER_PLAYS_MAX` in
   `main()`.
5. **Fix P1-5 (silent KNOB fallback):** raise on unknown
   `MOVE_ORDERING` / `EVALUATOR` values.
6. **Re-run all four variants** and confirm transcripts match the
   updated variants.md.
7. **Then proceed to App Tester / next reviewer.** Do NOT mark
   Lab 5 as variant-ready until at minimum P0-1 and P0-2 are
   resolved.

**DOCUMENT.md updated:** N/A for QA.
