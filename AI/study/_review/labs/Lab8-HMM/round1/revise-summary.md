# Lab 8 — HMM Round 1 Revise Summary

**Revised files:**
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 8\handout\hidden_markov_models_solution.py`
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab8-HMM\variants.md`

**Verification:** Ran `py -3.12 "Lab 8/handout/hidden_markov_models_solution.py"`
after every edit. All three default sequence outputs reproduce
bit-for-bit (`0.016809200000000003`, `1.5724311879680006e-06`,
`1.3007288729600007e-06`). Filter and smooth modes were exercised via
an in-process harness; values match Reviewer #4's hand-derived numbers
(filter t=2 hot=0.0408, smooth t=2 hot=0.0315). MODE typo raises
`ValueError`. Missing-`None` observation raises `AssertionError`.
Malformed row-sum TRANSITIONS/EMISSIONS edit raises `AssertionError` at
module import.

---

## Reviewer #2 — P0 fixes applied

**P0-1 (forward duplication).** Extracted `_forward_trellis(states,
observations, a_transitions, b_emissions) -> ndarray` as the single
source of truth for the forward recursion. `compute_forward`,
`compute_filtered`, and `compute_smoothed` all consume it. Termination
of `compute_forward` is now a one-line `sum_s alpha_T(s) * a_{s, qf}`
expression on the helper's output. The duplicated forward loops in
`compute_filtered` and `compute_smoothed` are gone.

**P0-2 (MODE validation).** Added module-import-time validation:
`MODE` is checked against `_VALID_MODES = {"viterbi", "filter",
"smooth"}` and a `ValueError` with an explicit "typos are NOT silently
ignored" message is raised on mismatch. The `main()` `if/elif` chain
now also has an explicit `else: raise ValueError(...)` so a runtime
mutation of `MODE` is caught too.

## Reviewer #3 — P0 fixes applied

**P0 (mental model umbrella+ice-cream blend).** Replaced the
Frankenstein paragraph with two clearly-separated blocks:
- "GENERAL HMM ANALOGY (L09b §2.1, the umbrella story)" — the umbrella
  story stated as the analogy.
- "THIS LAB'S CONCRETE INSTANCE (L09b §5.3, Jason's ice creams)" —
  the lab-specific instantiation, explicitly noting that ice-cream
  count plays the role of the umbrella.
Added a final sentence on the sum-vs-max structural insight (L09b
§2.5, §4.4) so the mental-model section now contains the exam-ready
one-liner.

**P0 (REFERENCES collapse of Evaluation vs Filtering).** Rewrote the
REFERENCES block. It now (a) corrects the misattribution — the lecture
uses the SLIDE naming, not the textbook naming; (b) defines Evaluation
as `P(O | lambda)` (returned by `compute_forward`) and Filtering as
`P(q_t | o_{1..t})` (returned by `compute_filtered`) as two DIFFERENT
outputs sharing one recursion; (c) cites L09b §3.5 and §6 Pitfall #1
explicitly. Adds references to §4.6 (Backward + smoothing) and §8
(cheat-sheet) for the variants that exercise those.

**P0 (Option B chosen for the emission policy).** I retained the
template emission values (P(3|H)=.75, P(3|C)=.1) as the default but
made the disagreement LOUD: the docstring now opens with a "!!!
IMPORTANT — HMM PARAMETER PROVENANCE !!!" banner that explicitly
states what disagrees, what the default reproduces, and points at
Variant 4 for the slide-values swap. Rationale: the existing OUTPUTS
WHEN RUN block (3 sequences) is referenced from `variants.md` V2 hints
as the baseline for the two-runs comparison, so changing the default
would have rippled into the variant bank and required re-capturing
three sets of reference outputs. The loud-disclosure path satisfies
R3 P0-3 without that ripple. (Option A — switching defaults — remains
available as a future revise round if the PM prefers slide values.)

**Convention note at §5.3 start about HOT=1 vs COLD=1.** The KNOB
block for MODE was rewritten to explicitly enumerate which entries get
printed: "print P(q_t = HOT | …) and P(q_t = COLD | …) — the two
real-state entries of the normalised forward column. The dummy
initial/final entries are zero and are not printed." The OBSERVATION
KNOB block already documents the leading-None convention; the MODE
KNOB now also documents that comparing filter vs smooth requires two
runs and that an invalid MODE raises `ValueError`.

## Reviewer #4 — P1 fixes applied (variants.md)

**P1-1 (V3 wrong universal claim).** Replaced the "filtered and
smoothed must agree at the last step" sentence with the correct
conditional: agreement at `t = T` holds whenever all real states
share the same end-transition probability `a[s, qf]`, which is true
for the default HMM (and Variant 2) but is NOT a universal property
of forward-backward. Added explicit note that a future variant
changing one row's end-transition would break this.

**P1-2 (V1 replace vs append ambiguity).** Added bolded instruction:
"REPLACE the entire list (do not append to the default three
sequences) so the script prints exactly one output block matching the
expected answer". Concrete line shown:
`OBSERVATION_SETS = [[None, 2, 3, 3, 1, 2]]`.

**P1-3 (V2 acceptance requires two runs).** Added bolded "TWO RUNS
ARE REQUIRED" bullet that walks through both ways to satisfy the
comparison: (a) run twice (default first, then modified), or
(b) read the original-default values from the OUTPUTS WHEN RUN
docstring block and only run once with modified TRANSITIONS. Both
paths produce the same comparison sentence.

**P1-4/P1-5 (V3 expected-output format).** Replaced the "two tables"
phrasing with "two stdout blocks" and pasted the actual stdout
format verbatim (the captured filter and smooth output for
`OBSERVATION_SETS = [[None, 3, 1, 3]]`). Also adds an "expected shift
magnitude is ~1 percentage point on a T=3 chain" note so an agent
does not panic on small numbers.

## Reviewer #2 — P1 fixes applied (assertions)

**P1-2 (assert observations[0] is None).** Added to `_forward_trellis`,
`compute_forward`, `compute_viterbi`, and `compute_backward`. The
assert message says "observations[0] must be None (sentinel for
1-based indexing)" so a panicking student sees the fix immediately.

**P1-3 (TRANSITIONS row-sum invariant).** Added at module import:
`assert np.allclose(TRANSITIONS[:-1].sum(axis=1), 1.0, ...)` with an
explicit message listing the offending row sums. The final (absorbing)
row is excluded.

**P1-4 (EMISSIONS row-sum invariant).** Added at module import:
checks (a) the real-state rows sum to 1.0 over columns 1..M, and
(b) column 0 is zero everywhere (the None-sentinel reservation).

---

## Items consciously deferred

- **R1 P2-1 (cast np.str_ to str in `convert_path_states_to_observations`).**
  Not part of the keyed fix list; documented in the V1 hint as a
  cosmetic artefact the agent should expect.
- **R2 P1-1 (Variant 5 for STATES).** Out of scope for this revise pass.
- **R3 P0-4/P0-5/P0-6 (augmented-vs-textbook pseudocode form).**
  Documented in the `compute_forward` body comment ("equivalent to
  L09b §4.2's slide pseudocode under the encoding pi_s = a_{0,s}…")
  and in `compute_backward`'s docstring, but did not re-implement in
  the L09b non-augmented form. Out of scope for the keyed fix list.
- **R3 P1-3 ("better sense in my head" argmax comment).** Untouched
  this round; flagged for a polish pass.
- **R4 P2-7 (per-function docstrings outside §8.2 strict surface).**
  Spec coordination question, not a Lab 8 file change.

---

## Files changed

- `Lab 8\handout\hidden_markov_models_solution.py` (substantive edits
  to docstring header, MENTAL MODEL, REFERENCES, OBSERVATION_SETS
  KNOB doc, MODE KNOB doc + validation, added invariant assertions,
  added `_forward_trellis` helper, refactored `compute_forward`,
  `compute_filtered`, `compute_smoothed`, added `observations[0] is
  None` asserts, added `else: raise ValueError` in `main`).
- `study\_exam\Lab8-HMM\variants.md` (V1 replace/append, V2 two-runs,
  V3 universal-claim correction + actual-stdout format).
