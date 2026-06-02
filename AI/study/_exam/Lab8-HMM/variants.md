# Lab 8 — HMM Variant Bank

Each variant is a self-contained exam-style question solvable by tweaking
KNOBs in `Lab 8/handout/hidden_markov_models_solution.py`. Exam agents are
limited to reading the docstring header + KNOB blocks + function
signatures — nothing else from the solution file.

Spec reference: §8.2 (3-exam-agent gate) and §8.3 (initial variant bank
for Lab 8: "Different observation sequence / Different transition matrix
/ Compute filtered vs smoothed posterior").

---

## Variant 1 — Different observation sequence

**Question.** Using the same HMM as the lab (states HOT / COLD, the
transition matrix and emission matrix that ship with `hidden_markov_models.py`),
compute (a) the probability under the model of the observation sequence
**2, 3, 3, 1, 2** of ice creams, and (b) the most likely weather sequence
that produced those observations.

Hints for the exam agent:
- Touch ONE knob only: `OBSERVATION_SETS`.
- **REPLACE the entire list** (do not append to the default three
  sequences) so the script prints exactly one output block matching
  the expected answer:
  `OBSERVATION_SETS = [[None, 2, 3, 3, 1, 2]]`
- Remember the leading `None` sentinel — every sequence must look like
  `[None, 2, 3, 3, 1, 2]`. The module raises `AssertionError` if the
  sentinel is missing.
- The script will print both the Forward probability and the Viterbi
  path.

Expected answer shape:
- Probability is a single positive float (much less than 1).
- Path is a length-5 list of state-name strings (each is "hot" or
  "cold"). Note: the printed path may render each element wrapped as
  `np.str_('hot')` — that is a cosmetic numpy-scalar repr; the
  semantic value is the plain string "hot".

---

## Variant 2 — Modified transition matrix (sticky COLD)

**Question.** The course wants to model a climate where cold spells are
much more persistent: change the transition matrix so that
`P(cold | cold) = 0.7`, `P(hot | cold) = 0.1`, and the end-transition
from cold stays at 0.2. Keep the hot row, the initial row, and the
emission matrix unchanged. Under this modified HMM, compute the Forward
probability and the most likely weather sequence for the original
**3 1 3** observation sequence. Does the predicted weather sequence
change compared to the original transition matrix?

Hints for the exam agent:
- Touch the `TRANSITIONS` KNOB only. The cold row (index 2) becomes
  `[.0, .1, .7, .2]`. The module asserts non-final rows sum to 1.0 at
  import time; a malformed edit will raise `AssertionError` loudly.
- Keep `OBSERVATION_SETS = [[None, 3, 1, 3]]` to isolate this comparison
  from the longer sequences.
- **TWO RUNS ARE REQUIRED.** This variant compares two HMMs against the
  same observation sequence, so the answer needs two probabilities and
  two paths. EITHER (a) run once with the default TRANSITIONS, save
  output; then modify TRANSITIONS as above and run a second time, OR
  (b) read the original-default `Probability: 0.016809200000000003`
  and `Path: ['hot', 'cold', 'hot']` from the OUTPUTS WHEN RUN block
  in the solution docstring (the docstring is part of the allowed
  surface) and only run once with the modified TRANSITIONS.
- Report: original Viterbi path vs new Viterbi path; original probability
  vs new probability.

Expected answer shape:
- Two probabilities, two 3-element paths, and one sentence comparing them.

---

## Variant 3 — Filtered vs smoothed posterior

**Question.** For the original observation sequence **3 1 3** and the
default HMM (no parameter changes), produce the per-step posterior
distribution over the hidden state HOT / COLD in two ways:
(a) **Filtered**: $P(q_t \mid o_{1..t})$ — the best estimate using only
    evidence seen *up to* time $t$.
(b) **Smoothed**: $P(q_t \mid o_{1..T})$ — using *all* the evidence,
    including future observations.
Which time step shows the biggest difference between filtered and
smoothed estimates, and intuitively why?

Hints for the exam agent:
- Set `OBSERVATION_SETS = [[None, 3, 1, 3]]` so only the variant
  sequence is exercised (the script prints one block per sequence).
- TWO RUNS of the script: first with `MODE = "filter"`, then with
  `MODE = "smooth"`. No other KNOB needs to change. A typo like
  `MODE = "smoothed"` now raises `ValueError` at module import (the
  module validates MODE against `{"viterbi", "filter", "smooth"}`).
- Both modes also print the Forward probability and Viterbi path; you
  can ignore those for this question (they're identical across runs).
- Expect a small shift on a T=3 chain — on the order of ~1 percentage
  point between filter and smooth at the most-affected step. Do not
  expect dramatic divergence.
- For the discussion: filtered and smoothed agree at the LAST time
  step `t = T` whenever all real states share the same end-transition
  probability `a[s, qf]` (true for the default HMM, where
  `a[hot, qf] = a[cold, qf] = 0.2`, and true under Variant 2 as well).
  This is NOT a universal property of forward-backward; if a future
  variant changed only one row's end-transition, the last-step
  agreement would break. Earlier-step divergence is the contribution
  of future observations.

Expected answer shape:
- Two stdout blocks (one for filter, one for smooth) — paste the
  script's `t=…: hot=…, cold=…` lines verbatim. The actual stdout
  format for each run is:
        Filtered P(q_t | o_{1..t}):
          t=1: hot=0.9677, cold=0.0323
          t=2: hot=0.0408, cold=0.9592
          t=3: hot=0.8149, cold=0.1851
        Smoothed P(q_t | o_{1..T}):
          t=1: hot=0.9723, cold=0.0277
          t=2: hot=0.0315, cold=0.9685
          t=3: hot=0.8149, cold=0.1851
  (one row per t, two `name=prob` fields per row — NOT a Markdown
  table; the rubric accepts the raw stdout).
- One sentence identifying the time step with the largest filtered →
  smoothed shift and naming the future evidence that drove it.

---

## Optional Variant 4 — Slide-vs-template emission discrepancy

**Question.** The slide diagram in `Lab 8.pdf` shows emission
probabilities of `P(3|HOT) = .4` and `P(3|COLD) = .1`, but the code
template ships with `P(3|HOT) = .75` and `P(3|COLD) = .1`. Re-compute
the Forward probability and Viterbi path for **3 1 3** under the
*slide* values:
$B_1 = [.0, .2, .4, .4]$, $B_2 = [.0, .5, .4, .1]$. Does the most-likely
weather sequence change?

Hints for the exam agent:
- Touch `EMISSIONS` only. Hot row becomes `[.0, .2, .4, .4]`; cold row
  becomes `[.0, .5, .4, .1]`.
- Confirm each non-dummy row sums to 1.
- Report both numbers and the path; compare to the template-default
  output (which is included in the docstring under OUTPUTS WHEN RUN).

Expected answer shape:
- One probability, one 3-element path, one sentence comparing to the
  template default.
