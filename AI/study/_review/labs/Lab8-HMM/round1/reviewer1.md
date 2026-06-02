# Lab 8 — HMM Solution — Reviewer #1 (Correctness) — Round 1

**Reviewer role:** Correctness — verify the solution actually produces the docstring's recorded outputs and that the Forward/Viterbi math is right.
**File under review:** `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 8\handout\hidden_markov_models_solution.py`
**Reference:** `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 8\handout\Lab 8.pdf`
**Stance:** HARSH. Anything ambiguous gets logged.

---

## 1. Reproduction result

Ran `py -3.12 "Lab 8\handout\hidden_markov_models_solution.py"` from the repo root. Captured stdout below verbatim:

```
Observations: 3 1 3
Probability: 0.016809200000000003
Path: [np.str_('hot'), np.str_('cold'), np.str_('hot')]

Observations: 3 3 1 1 2 2 3 1 3
Probability: 1.5724311879680006e-06
Path: [np.str_('hot'), np.str_('hot'), np.str_('cold'), np.str_('cold'), np.str_('hot'), np.str_('cold'), np.str_('hot'), np.str_('cold'), np.str_('hot')]

Observations: 3 3 1 1 2 3 3 1 2
Probability: 1.3007288729600007e-06
Path: [np.str_('hot'), np.str_('hot'), np.str_('cold'), np.str_('cold'), np.str_('cold'), np.str_('hot'), np.str_('hot'), np.str_('cold'), np.str_('cold')]
```

The script exits cleanly, no warnings, no exceptions.

---

## 2. Docstring vs. actual output — line-by-line diff

Docstring (lines 95–105) records:

| Sequence | Docstring Probability | Docstring Path |
|---|---|---|
| `3 1 3` | `0.016809200000000003` | `['hot', 'cold', 'hot']` |
| `3 3 1 1 2 2 3 1 3` | `1.5724311879680006e-06` | `['hot', 'hot', 'cold', 'cold', 'hot', 'cold', 'hot', 'cold', 'hot']` |
| `3 3 1 1 2 3 3 1 2` | `1.3007288729600007e-06` | `['hot', 'hot', 'cold', 'cold', 'cold', 'hot', 'hot', 'cold', 'cold']` |

Actual:

| Sequence | Actual Probability | Actual Path |
|---|---|---|
| `3 1 3` | `0.016809200000000003` | `[np.str_('hot'), np.str_('cold'), np.str_('hot')]` |
| `3 3 1 1 2 2 3 1 3` | `1.5724311879680006e-06` | `[np.str_('hot'), np.str_('hot'), np.str_('cold'), np.str_('cold'), np.str_('hot'), np.str_('cold'), np.str_('hot'), np.str_('cold'), np.str_('hot')]` |
| `3 3 1 1 2 3 3 1 2` | `1.3007288729600007e-06` | `[np.str_('hot'), np.str_('hot'), np.str_('cold'), np.str_('cold'), np.str_('cold'), np.str_('hot'), np.str_('hot'), np.str_('cold'), np.str_('cold')]` |

- **Probabilities:** identical to every decimal of the IEEE-754 representation. PASS.
- **Paths (semantic):** identical hidden-state sequences. PASS.
- **Paths (display):** the *printed repr* differs — actual output wraps each state name in `np.str_('...')` because `STATES` is `np.array([...])` so `states[p]` is an `np.str_` scalar, and `list.__repr__` falls back to each element's `repr`. Docstring shows clean `'hot'` strings, which is what you would get if `STATES` were a plain Python list. **This is a P2 cosmetic drift between docstring and reality.** It would matter if a grader scraped output with a regex like `\['hot', 'cold', 'hot'\]`.

---

## 3. Hand-verification of Forward on sequence `3 1 3`

Using the template emissions (P(3|H)=.75, P(3|C)=.1 — NOT the slide values):

- α₁(H) = a₀,H · b_H(3) = 0.8 · 0.75 = **0.600**
- α₁(C) = a₀,C · b_C(3) = 0.2 · 0.10 = **0.020**
- α₂(H) = (0.6·0.2 + 0.02·0.3) · b_H(1) = (0.120 + 0.006) · 0.1 = **0.0126**
- α₂(C) = (0.6·0.6 + 0.02·0.5) · b_C(1) = (0.360 + 0.010) · 0.8 = **0.2960**
- α₃(H) = (0.0126·0.2 + 0.2960·0.3) · b_H(3) = (0.00252 + 0.0888) · 0.75 = 0.09132 · 0.75 = **0.06849**
- α₃(C) = (0.0126·0.6 + 0.2960·0.5) · b_C(3) = (0.00756 + 0.148) · 0.1 = 0.15556 · 0.1 = **0.015556**
- α_F = (α₃(H) + α₃(C)) · 0.2 = (0.06849 + 0.015556) · 0.2 = 0.084046 · 0.2 = **0.0168092**

Matches `0.016809200000000003` to the floating-point bit (the trailing `...3` is the usual binary repr of the decimal `0.0168092`). **Forward math: CORRECT.**

Viterbi for `3 1 3` should obviously want HOT at t=1 (P(3|H)=.75 is huge), then any state at t=2 (obs `1` favours COLD strongly), then HOT at t=3. Output `H C H` is the right argmax path — confirmed by the slide's worked example (slide 6) which also recovers H-C-H structure, even though its numerical α values differ because the slide uses different emissions. **Viterbi qualitatively: CORRECT.**

---

## 4. Code-level correctness audit

Reading `hidden_markov_models_solution.py` end-to-end:

### compute_forward (lines 249–287)
- Initialisation (line 272): `forward[s, 1] = a_transitions[0, s] * b_emissions[s, observations[1]]` — matches Jurafsky `α₁(s) = a_{0,s} · b_s(o_1)`. ✓
- Recursion (lines 275–280): summation index `s_prev` over `1..big_n`, exactly the textbook recurrence. ✓
- Termination (lines 283–285): `α_F = Σ α_T(s) · a_{s,qf}`. ✓
- Returns `float(forward[qf, big_t])`. The `[qf, big_t]` cell is set; the rest of the `qf` row stays at the sentinel `5`, but that's never read. ✓
- **No bugs found.**

### compute_viterbi (lines 290–341)
- Initialisation (lines 311–313): viterbi[s,1] same as forward; backpointers[s,1] = 0 (start). ✓
- Recursion (lines 317–325): builds `scored_predecessors = [(s_prev, score)]`; takes `max` for the cell, `argmax(...)` for the backpointer. `argmax` is the local helper that returns the *first* element of the max tuple, i.e. the `s_prev` index — correct. ✓
- Note (subtle, but legit): the score the helper picks `argmax` over includes `b_s(o_t)`, which is a constant multiplier across all `s_prev`. The textbook argmax in the slide only uses `viterbi[s', t-1] * a_{s', s}` (no emission). Multiplying every candidate by the same positive constant does not change the argmax, so this is **mathematically equivalent**. Not a bug, but worth flagging because a strict pseudocode-compare reviewer might frown. P2.
- Termination (lines 328–332): `max` and `argmax` over `viterbi[s,T] * a_{s,qf}`. Matches pseudocode. ✓
- Backtrace (lines 337–340): starts from `backpointers[qf, big_t]` (which is the best last real state), then walks back via `backpointers[path[-1], t]` for `t = T..2`, reverses. Produces length-T list of real-state indices. The slide pseudocode says "return the backtrace path by following backpointers to states back in time from backpointer[qF, T]" — this is the standard implementation. ✓
- **No correctness bugs.** Path returned is `[1, 2, 1]` for `3 1 3`, mapped to `['hot', 'cold', 'hot']` via `convert_path_states_to_observations`. ✓

### compute_backward, compute_filtered, compute_smoothed (lines 344–428)
- Not exercised by the default `MODE = "viterbi"`. Reviewed by inspection:
  - `compute_backward`: termination at `β_T(s) = a_{s,qf}`, recursion `β_t(s) = Σ a_{s,s'} · b_{s'}(o_{t+1}) · β_{t+1}(s')`. Standard. ✓
  - `compute_filtered`: re-runs forward locally, normalises each column. The "real-state" entries normalise correctly because the dummy rows are zero. ✓
  - `compute_smoothed`: γ_t ∝ α_t · β_t, normalise. ✓
- These are not required by Lab 8.pdf; they are the docstring's "Variant 3" extension. **Not a correctness issue, but bloats the file beyond the lab's literal ask.** P2.

### Auxiliary
- `argmax` helper (lines 431–438): takes `[(key, value)]` and returns the key of the max-value tuple. Correct for the way it is called. Docstring says `tuple(key, value)` not `(key, value)` — that's a docstring typo (tuple is the constructor, not the literal form) but harmless. P2.
- `inclusive_range(a, b)` (line 245): returns `range(a, b+1)`. Trivially correct.
- `convert_path_states_to_observations` (line 241): list comprehension `states[p]` — relies on `states` being numpy-indexable. Returns a list of `np.str_` scalars (cause of the §2 cosmetic mismatch).

### Sentinel value `5` (lines 268, 302, 307)
The forward / viterbi matrices are filled with `5.0` (and backpointers with `int` 5) as a sentinel. Every "real" cell (rows 1..N for t=1..T, plus row qf at t=T) is written before being read. The dummy "initial" row (index 0) and unused cells in the `qf` row stay at 5, but those are never indexed. **Not a bug.** Slightly clever; a stricter reviewer would prefer `np.full(..., np.nan)` so a mis-indexed read would propagate visibly rather than silently inflate a probability.

---

## 5. Cross-check against the lab handout

- **Exercise 1** (slide 2): "compute the probability of observation sequence 3 1 3" + "most likely weather sequence". Solution outputs both. ✓
- **Exercise 2** (slide 8): same for `3,3,1,1,2,2,3,1,3` and `3,3,1,1,2,3,3,1,2`. Both present in `OBSERVATION_SETS`, both produce output. ✓
- **Important caveat (already flagged by the docstring):** the slide diagram on slide 3 of `Lab 8.pdf` shows emissions P(3|H)=0.4, P(3|C)=0.1 (you can read it off the B₁/B₂ boxes: H = [.2,.4,.4], C = [.5,.4,.1]). The solution uses P(3|H)=0.75, P(3|C)=0.1 — inherited from the template `hidden_markov_models.py`. The lab text says "the Hidden Markov Model **shown on the next slide**" → strict reading is the *slide's* values. The template hardcodes different values. **The solution matches the template, NOT the slide.** The docstring (lines 22–25, 172–180) explicitly documents this and tells the student how to switch. This is the lab author's call, not a solution bug — the original handout file shipped with these numbers. P1 *informational* — flag for the grader, not for the engineer.

If the question on the exam phrases probabilities as `.2 .4 .4 / .5 .4 .1`, running this solution as-is would produce **wrong** numbers. The exam-prep mitigation is the KNOB section, so this is acceptable for a study repo, but the docstring's "Reference output ... captured from ... on this repo" is only valid for the template emissions, not the slide emissions.

---

## 6. Findings (severity-tagged)

### P0 — Broken / blocks correctness verification
None. Forward + Viterbi produce numerically and semantically correct outputs that match the docstring.

### P1 — Important issues
1. **Slide-vs-template emission mismatch is silently divergent from the lab handout.** `Lab 8.pdf` slide 3 shows P(3|H)=.4, but `EMISSIONS` hard-codes P(3|H)=.75. The docstring discloses this on lines 22–25 and 172–180, so a careful student is warned, but a less-careful student running the file and reading off `0.016809200000000003` would submit a number that disagrees with the slide's worked example (slide 4 shows α₁(H)=.32, which only happens with slide emissions; this solution computes α₁(H)=.60). **Recommendation:** add a banner-level comment at the top of `main()` printing "Using TEMPLATE emissions (P(3|H)=.75); switch EMISSIONS to slide values [.0,.2,.4,.4]/[.0,.5,.4,.1] to reproduce the slide's α values." Or, better, default to the slide values and put template values in the variants section, since the lab problem statement points at the slide.

### P2 — Polish / suggestions
1. **Path printout displays `np.str_('hot')` instead of `'hot'`.** Docstring's "Reference output" shows clean `['hot', 'cold', 'hot']`; actual prints the numpy scalar repr. Fix: cast in `convert_path_states_to_observations` — `return [str(states[p]) for p in path]` — and the printed list will then match the docstring exactly. Pure cosmetic, but the docstring claims byte-perfect reproducibility.
2. **Viterbi recursion folds `b_s(o_t)` into the argmax expression.** Mathematically equivalent because the emission is a positive constant across all `s_prev`, but the slide's pseudocode shows `argmax_s' viterbi[s', t-1] * a_{s', s}` without the emission. A pseudocode-strict grader might want the emission factored out of the argmax. Suggest a one-line comment in `compute_viterbi` near line 319 explaining "the b_s(o_t) factor is a positive constant across s_prev so it does not affect the argmax — kept in for symmetry with the `max` score above".
3. **`argmax` helper docstring** (line 433) says "sequence[i] = tuple(key, value)". `tuple(key, value)` is a TypeError (the constructor takes one iterable). Should read `sequence[i] = (key, value)` or "sequence[i] is a 2-tuple (key, value)".
4. **Sentinel `5.0` in `forward`/`viterbi` matrices.** Works because every read-site touches only written cells. A `np.nan` sentinel would crash loudly on any future indexing bug; `5` would silently mis-add. Suggest `np.nan` (or at least a comment "ANY non-zero sentinel works; `5` is arbitrary").
5. **Backward / filtered / smoothed code is unreachable in default mode.** With `MODE = "viterbi"`, lines 344–428 are dead code (≈85 LOC of ~190 non-blank LOC ≈ 45% of the file). Acceptable for an exam-prep file because the KNOB documents Variant 3, but a strict reviewer would prefer those moved to a separate module imported on demand.
6. **`OBSERVATION_SETS` requires a `None` sentinel at index 0** and this is explained in the KNOB comment, but the constraint is purely a convenience for the 1-based pseudocode mapping. If a student dropped the `None`, `observations[1]` would skip the first observation and silently produce wrong probabilities (no IndexError, no warning). A defensive `assert observations[0] is None` at the start of `compute_forward` / `compute_viterbi` would catch this in 0.001 s. Recommend adding it.
7. **`np.set_printoptions(suppress=True)`** is called but the script never prints any numpy arrays in default mode — it only prints scalars and lists. The call is harmless but misleading; remove or move into the `MODE in {"filter", "smooth"}` branches where numpy arrays actually get formatted.
8. **No README / DOCUMENT.md in `Lab 8/handout/`.** Out of scope for "Correctness Reviewer #1" — flag for the PM workflow's Reviewer #2.

---

## 7. Conclusion

The Forward algorithm and Viterbi algorithm in `hidden_markov_models_solution.py` are **mathematically correct** for the parameter set encoded in the file. The hand-derived value for the `3 1 3` Forward probability (0.0168092) matches the program's output to floating-point precision. All three docstring-recorded outputs are reproduced bit-for-bit in the numerical fields. The only diff against the docstring's recorded output is the `np.str_('...')` repr wrapping the path elements — a cosmetic numpy-vs-Python display quirk, not a correctness bug.

The one substantive correctness *risk* is the slide-vs-template emission mismatch, which is a known and documented choice by the lab author, not a fault of the solution implementation. The docstring discloses this prominently.

**Overall verdict: CORRECT.** The solution is suitable as a reference answer for the lab as shipped. Recommend the P1 fix (banner about emission set) and the trivial P2 fixes (cast to `str`, `assert observations[0] is None`, fix `argmax` docstring) before declaring it exam-ready.

---

## Report to PM

**Assignment recap:** Lab 8 HMM solution (`hidden_markov_models_solution.py`) — Reviewer #1 (Correctness), Round 1. Verify Forward + Viterbi outputs match the docstring's recorded outputs for all three sequences from `Lab 8.pdf`.

**Status:** Pass with concerns

**P0 findings:** None.

**P1 findings:**
1. `hidden_markov_models_solution.py:182-186` — Solution uses **template** emissions (P(3|H)=.75, P(3|C)=.1) but `Lab 8.pdf` slide 3 shows **slide** emissions (P(3|H)=.4). Docstring lines 22-25, 172-180 disclose this, but a student running the solution will get numbers that disagree with the slide's worked example (the slide shows α₁(H)=.32; this solution computes α₁(H)=.60). Suggested fix: add a one-line banner print in `main()` clarifying which emission set is in effect, OR switch default to slide values and move template values to the variants comment block.

**P2 findings:**
1. `hidden_markov_models_solution.py:241-242` — `convert_path_states_to_observations` returns `np.str_` scalars, so the printed path reads `[np.str_('hot'), ...]` instead of the clean `['hot', ...]` shown in the docstring's "Reference output" block (lines 95-105). Cast with `str(states[p])` to match the docstring byte-for-byte.
2. `hidden_markov_models_solution.py:319-325` — Viterbi recursion folds `b_s(o_t)` into the argmax expression; mathematically equivalent to the slide pseudocode (positive constant across `s_prev`) but a strict pseudocode-compare reviewer might object. Add a one-line clarifying comment.
3. `hidden_markov_models_solution.py:433-437` — `argmax` docstring writes "sequence[i] = tuple(key, value)"; the literal `tuple(key, value)` is a TypeError. Reword to "sequence[i] is a 2-tuple `(key, value)`".
4. `hidden_markov_models_solution.py:268, 302, 307` — Sentinel value `5` works because every cell read is a cell written, but `np.nan` would loudly crash on any future indexing bug. Defensive suggestion.
5. `hidden_markov_models_solution.py:249-287, 290-341` — Add `assert observations[0] is None` at the top of `compute_forward` and `compute_viterbi`. Dropping the `None` sentinel currently silently skips the first observation and yields wrong probabilities with no error.
6. `hidden_markov_models_solution.py:344-428` — `compute_backward`, `compute_filtered`, `compute_smoothed` (~85 LOC, ~45% of the file) are dead code in default `MODE = "viterbi"`. Acceptable for an exam-prep KNOB but bloats the correctness surface.
7. `hidden_markov_models_solution.py:210` — `np.set_printoptions(suppress=True)` is dead in default mode (no numpy arrays printed). Move into the `MODE in {"filter", "smooth"}` branches.
8. `Lab 8/handout/` — no `DOCUMENT.md`. Out of scope for Correctness Reviewer #1; flag for the PM's documentation reviewer.

**QA Checklist (§7) status:**
- Bug-free against scope: **Pass** — Forward 0.0168092 matches hand-derivation; all three sequence outputs match the docstring numerically.
- Security items from §6: **N/A** — pure offline numerical script, no inputs, no I/O, no secrets.
- Performance acceptable: **Pass** — O(N²·T) per call, T≤9, N=2; runs in well under a second.
- Accessibility: **N/A** — console output only.
- DOCUMENT.md present in every modified directory: **Fail** — no DOCUMENT.md in `Lab 8/handout/`. (Flag, not blocker for correctness round.)
- Conventions from PM/conventions.md followed: **N/A for this scope** — code-style review is Reviewer #2's lane; this round is correctness only.

**Acceptance criteria (§1) status:**
- Forward algorithm produces P(O|λ) for sequence `3 1 3`: **Met** (0.016809200000000003).
- Viterbi algorithm produces best path for sequence `3 1 3`: **Met** (`['hot', 'cold', 'hot']`).
- Forward + Viterbi for `3 3 1 1 2 2 3 1 3`: **Met** (`1.5724311879680006e-06`, `H H C C H C H C H`).
- Forward + Viterbi for `3 3 1 1 2 3 3 1 2`: **Met** (`1.3007288729600007e-06`, `H H C C C H H C C`).
- All three sequences' results match the docstring's "Reference output" block: **Met** (numerical) / **Cosmetic drift** (path repr — see P2 #1).

**DOCUMENT.md audit:**
- `Lab 8/handout/` — Missing. (Out of scope for correctness reviewer; flag only.)
- `study/_review/labs/Lab8-HMM/round1/` — Reviewer output dir; `reviewer1.md` is this file. N/A.

**Out-of-scope observations:**
- The reference template `hidden_markov_models.py` still ships with `raise NotImplementedError` in both `compute_forward` and `compute_viterbi` — this is correct for a "student starting point", but the PM should be aware that the *_solution.py* file is the only runnable artifact.
- The lab handout's slide pseudocode for Viterbi writes the argmax without the emission factor; the solution includes it. Mathematically equivalent, but worth a one-line comment to forestall reviewer confusion.

**Concerns / risks:**
- **Emission-set ambiguity is the biggest gotcha.** A student preparing for the exam will see two different "right answers" depending on whether the question quotes the slide's B₁/B₂ matrices or the template's. The KNOB section documents both, but the *default* should arguably match the slide because the lab problem statement points at the slide. If the exam uses slide values, running this solution unchanged gives a wrong number.
- The `np.str_` repr in the path printout is harmless functionally but means the docstring's "Reference output" is *not* a byte-perfect match. Anyone using `diff` to grade would flag it.

**What PM should do next:**
- Decide whether to default to slide emissions (recommended — matches the lab problem statement literally) or keep template emissions (matches the original starter file and the docstring's recorded outputs). If switching defaults: re-capture the "Reference output" block and re-run any dependent study notes.
- Dispatch the engineer to apply P2 #1 (cast to `str` in `convert_path_states_to_observations`) and P2 #5 (`assert observations[0] is None`) — both are one-line, zero-risk improvements.
- After fixes, run Reviewer #2 (style/conventions/documentation) and add DOCUMENT.md to `Lab 8/handout/`.
- No re-QA needed for correctness — the math is sound.

**DOCUMENT.md updated:** N/A for QA
