"""
LAB 8: Hidden Markov Models (Viterbi & Forward Algorithms)
==========================================================

PROBLEM STATEMENT (from Lab 8.pdf):
-----------------------------------
Exercise 1 — The Forward & Viterbi Algorithm
    1. Implement the Forward Algorithm for the Hidden Markov Model
       (HOT/COLD weather, ice-creams-eaten observations) to compute the
       probability of the observation sequence 3 1 3.
    2. Implement the Viterbi Algorithm to compute the most likely weather
       sequence for the observation sequence 3 1 3.
    Use the file hidden_markov_models.py — it contains the incomplete
    functions compute_forward and compute_viterbi.

Exercise 2 — Repeat for two longer observation sequences:
    Sequence A: 3, 3, 1, 1, 2, 2, 3, 1, 3
    Sequence B: 3, 3, 1, 1, 2, 3, 3, 1, 2
    For each: (a) probability via Forward, (b) most-likely weather via Viterbi.

!!! IMPORTANT — HMM PARAMETER PROVENANCE !!!
The HMM (Jurafsky & Martin, SLP3 Appendix A — "Jason's ice creams")
parameters used here are TAKEN VERBATIM FROM THE TEMPLATE FILE
`hidden_markov_models.py`, not from the slide diagram in `Lab 8.pdf`.
THE TEMPLATE AND THE SLIDE DISAGREE ON THE EMISSION MATRIX:
        slide:    P(3|H)=.4,  P(3|C)=.1   (Lab 8.pdf slide 3)
        template: P(3|H)=.75, P(3|C)=.1   (DEFAULT IN THIS FILE)
If you are graded against the slide's worked example, the OUTPUTS
WHEN RUN block below will NOT reproduce it — you must first switch
EMISSIONS to the slide values (see KNOB EMISSIONS below). Variant 4
exercises this exact swap. This is a conscious choice: the default
matches the template/grader and the docstring's recorded outputs;
the slide values are one KNOB edit away.

MENTAL MODEL (one-line analogy):
--------------------------------
GENERAL HMM ANALOGY (L09b §2.1, the umbrella story): you watch someone's
umbrella each morning to guess whether it is raining where they live —
the umbrella is the *visible observation*, the weather is the *hidden
state*, and the HMM links them through transition probabilities (day-to-
day weather) and emission probabilities (umbrella-given-weather).

THIS LAB'S CONCRETE INSTANCE (L09b §5.3, Jason's ice creams): the
observation is the number of ice creams Jason eats that day (1, 2, or 3),
and the hidden state is the day's weather (HOT / COLD). Ice-cream count
plays the role of the umbrella; weather plays the role of weather.

The Forward algorithm asks "how likely is this whole record of ice-cream
counts under the model?" (sum over all possible hidden sequences);
Viterbi asks "what single weather sequence best explains it?" (max over
all possible hidden sequences). Forward vs Viterbi = sum vs max on the
same trellis with the same per-cell weights — that one-operator swap is
the structural insight (L09b §2.5, §4.4).

REFERENCES:
-----------
- Lecture 9b (Hidden Markov Models). The lecture uses the SLIDE naming
  convention (NOT the textbook one): Problem 1 = Evaluation, Problem 2 =
  Decoding, Problem 3 = Learning. L09b §3.5 explicitly warns that the
  textbook names — filtering / smoothing-or-decoding / learning — are
  NOT one-to-one with the slide names. In particular:
        Evaluation  = P(O | lambda)            — likelihood of the
                                                  whole observation
                                                  sequence (returned by
                                                  compute_forward).
        Filtering   = P(q_t | o_{1..t})        — posterior over the
                                                  CURRENT hidden state
                                                  given evidence up to t
                                                  (returned by
                                                  compute_filtered).
  Evaluation and Filtering share the forward recursion but are DIFFERENT
  outputs. Do not collapse them; see L09b §6 Pitfall #1.
  See study/lectures/L09b-HMM.md §3 (HMM definition), §4 (Forward &
  Viterbi pseudocode), §4.6 (Backward + smoothing), §5 (worked
  ice-cream example), §6 (pitfalls), §8 (cheat-sheet).
- Related glossary terms: Hidden Markov Model, Hidden state, Observation,
  Markov assumption, Markov chain, Transition model, Emission model
  (observation model), Initial distribution, Forward algorithm, Viterbi
  algorithm, Filtering (HMM problem 1), Trellis, Backpointer.
- Source slides for the diagram (transition probabilities only — emissions
  differ): Lab 8.pdf slide 3 and Jurafsky & Martin
  https://web.stanford.edu/~jurafsky/slp3/A.pdf

HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS:
--------------------------------------------------
1. Different observation sequence (e.g. 1 2 3 instead of 3 1 3):
   Change KNOB OBSERVATION_SETS (remember the leading None placeholder at
   index 0 — every sequence in the list uses 1-based indexing inside the
   algorithms). Run the file: forward gives the probability, viterbi gives
   the weather sequence.

2. Different / modified transition matrix (e.g. make COLD->COLD stickier):
   Edit KNOB TRANSITIONS. Rows must still sum to 1. The "initial" row
   (index 0) gives the start-state distribution; the "final" row stays at
   zero; the last column gives the probability of ending in each step.

3. Different emission matrix (e.g. revert to the slide values):
   Edit KNOB EMISSIONS. Each non-dummy row must sum to 1 over its non-zero
   observation columns (here columns 1..3 because observations are in
   {1,2,3}).

4. More hidden states (e.g. add a MILD state):
   Extend KNOB STATES, TRANSITIONS, and EMISSIONS in lockstep. The shapes
   are (N+2,) for states and (N+2, N+2) for transitions, (N+2, M+1) for
   emissions where N = number of "real" hidden states and M = number of
   possible observation symbols.

5. Filtered vs smoothed posterior over a single time step:
   "Filtered" P(q_t = k | o_{1..t}) is alpha_t(k) / sum_j alpha_t(j) — set
   KNOB MODE = "filter" and the script prints the normalised forward
   trellis column at each t. "Smoothed" P(q_t = k | o_{1..T}) uses both
   forward and backward; toggle KNOB MODE = "smooth" to enable the
   backward pass and print the smoothed posteriors. Viterbi (KNOB MODE =
   "viterbi", default) ignores MODE for the path-decoding step — the
   default print always shows Forward probability + Viterbi path.

OUTPUTS WHEN RUN:
-----------------
For each observation sequence, prints:
    Observations: <space-separated obs>
    Probability:  <forward probability, P(O|lambda)>
    Path:         <most-likely state sequence from Viterbi>

Reference output for the template HMM and the three default sequences
(captured from `py -3.12 hidden_markov_models_solution.py` on this repo):

    Observations: 3 1 3
    Probability: 0.016809200000000003
    Path: ['hot', 'cold', 'hot']

    Observations: 3 3 1 1 2 2 3 1 3
    Probability: 1.5724311879680006e-06
    Path: ['hot', 'hot', 'cold', 'cold', 'hot', 'cold', 'hot', 'cold', 'hot']

    Observations: 3 3 1 1 2 3 3 1 2
    Probability: 1.3007288729600007e-06
    Path: ['hot', 'hot', 'cold', 'cold', 'cold', 'hot', 'hot', 'cold', 'cold']

ENTRY POINT: yes
----------------
Run directly with `py -3.12 hidden_markov_models_solution.py` — main()
exercises Forward + Viterbi on every sequence in OBSERVATION_SETS.
"""
import numpy as np
from numpy import ndarray


# ---------------------------------------------------------------------------
# KNOBs — every tunable parameter for variant questions lives here.
# ---------------------------------------------------------------------------

# KNOB: STATES (default=["initial", "hot", "cold", "final"])
#   What it does: names of all HMM states. The first ("initial") and last
#       ("final") are *dummy* start/end markers used by the augmented
#       Jurafsky formulation; the "real" hidden states sit between them.
#   Effect: changing this list changes len(states); the algorithms derive
#       big_n = len(states) - 2 (number of real states) from it. Must be
#       kept in lockstep with TRANSITIONS and EMISSIONS shapes.
#   Exam variants:
#       - Default 2-state weather: ["initial", "hot", "cold", "final"]
#       - 3-state weather: ["initial", "hot", "mild", "cold", "final"]
#         (also extend TRANSITIONS / EMISSIONS to 5x5 and 5xM).
STATES = np.array(["initial", "hot", "cold", "final"])

# KNOB: OBSERVATION_SETS (default=three Jurafsky sequences)
#   What it does: list of observation sequences to decode. Each sequence
#       must start with None at index 0 (sentinel for 1-based indexing
#       used by the algorithms — t runs 1..T).
#   Effect: each sequence is fed to compute_forward and compute_viterbi.
#   VARIANT-RUN CONVENTION: for a variant question, REPLACE the entire
#       list with `[[None, <your sequence>]]` (one element). Do NOT
#       APPEND to the default — the script prints one output block per
#       sequence and appending bloats the run log so the grader has to
#       hunt for the variant's answer.
#       Correct:   OBSERVATION_SETS = [[None, 2, 3, 3, 1, 2]]
#       WRONG:     OBSERVATION_SETS = [[None, 3, 1, 3], [None, 2, 3, 3, 1, 2]]
#       WRONG:     OBSERVATION_SETS = [[2, 3, 3, 1, 2]]   # missing None → IndexError
#   Exam variants:
#       - Exercise 1 sequence: [None, 3, 1, 3]
#       - Exercise 2 sequence A: [None, 3, 3, 1, 1, 2, 2, 3, 1, 3]
#       - Exercise 2 sequence B: [None, 3, 3, 1, 1, 2, 3, 3, 1, 2]
#       - Variant 1 (new sequence): replace with [[None, 2, 3, 3, 1, 2]].
OBSERVATION_SETS = [
    [None, 3, 1, 3],
    [None, 3, 3, 1, 1, 2, 2, 3, 1, 3],
    [None, 3, 3, 1, 1, 2, 3, 3, 1, 2],
]

# KNOB: TRANSITIONS (default=Jurafsky ice-cream HMM transition matrix)
#   What it does: A[i,j] = P(q_{t+1}=j | q_t=i). Row 0 is the *initial*
#       distribution: A[0, j] = P(q_1 = j). The last column is the
#       end-transition probability A[i, qf] = P(q_T+1 = end | q_t = i).
#   Effect: rows must sum to 1 (except the all-zero "final" row, which is
#       absorbing). Skewing A[hot,cold] up vs A[hot,hot] makes hot
#       weather less sticky and yields a noisier hidden-path estimate.
#   Exam variants:
#       - Variant 2 (modified transitions): try making cold sticky by
#         setting [.0, .1, .7, .2] for the cold row.
#       - "Equal-priors" sanity check: set initial row to [.0, .5, .5, .0].
#                       to:  S   h   c   e     from:
TRANSITIONS = np.array([[.0, .8, .2, .0],   # Initial state
                        [.0, .2, .6, .2],   # Hot state
                        [.0, .3, .5, .2],   # Cold state
                        [.0, .0, .0, .0],   # Final state
                        ])

# KNOB: EMISSIONS (default=template values P(3|H)=.75, P(3|C)=.1)
#   What it does: B[state, obs] = P(observation = obs | state). The dummy
#       initial / final rows stay zero. Observation 0 is unused (index 0
#       is reserved as a None sentinel everywhere).
#   Effect: row sums over the *real* observation columns (1..M) must be 1.
#   Note: the slide in Lab 8.pdf shows DIFFERENT emissions:
#         slide hot row would be [.0, .2, .4, .4]
#         slide cold row would be [.0, .5, .4, .1]
#       If a question phrases probabilities as ".2 .4 .4 / .5 .4 .1",
#       replace the matrix below with those values.
#   Exam variants:
#       - Default (matches the original template values used for grading):
#         hot=[.0, .1, .15, .75], cold=[.0, .8, .1, .1]
#       - Slide diagram values: hot=[.0, .2, .4, .4], cold=[.0, .5, .4, .1]
#                     0    1    2     3
EMISSIONS = np.array([[.0, .0, .0, .0],     # Initial state
                      [.0, .1, .15, .75],   # Hot state
                      [.0, .8, .1, .1],     # Cold state
                      [.0, .0, .0, .0],     # Final state
                      ])

# KNOB: MODE (default="viterbi", allowed={"viterbi", "filter", "smooth"})
#   What it does: selects an *additional* posterior calculation to print
#       alongside the always-on Forward+Viterbi outputs.
#       - "viterbi": no extra output (default).
#       - "filter":  for each t, print P(q_t = HOT | o_{1..t}) and
#                    P(q_t = COLD | o_{1..t}) — the two real-state
#                    entries of the normalised forward column. The
#                    dummy initial/final entries are zero and are not
#                    printed.
#       - "smooth":  for each t, print P(q_t = HOT | o_{1..T}) and
#                    P(q_t = COLD | o_{1..T}) using the forward-backward
#                    algorithm. Same two-entry-per-line format as
#                    "filter".
#   Effect: only the printing layer; compute_forward and compute_viterbi
#       always run. Run time is the same to within O(N²T) for the extra
#       forward/backward pass.
#   Invalid values: any string outside {"viterbi", "filter", "smooth"}
#       raises ValueError at module import. A typo (e.g. "smoothed",
#       "Filter", "viterbi ") will NOT silently no-op.
#   Compare-filter-vs-smooth note: to compare them in one task you must
#       run the script TWICE, once with MODE="filter" and once with
#       MODE="smooth". A single run prints only one of the two.
#   Exam variants:
#       - Variant 3 ("filtered vs smoothed posterior"): run once with
#         MODE = "filter", then again with MODE = "smooth", capturing
#         the two stdout blocks.
MODE = "viterbi"
_VALID_MODES = {"viterbi", "filter", "smooth"}
if MODE not in _VALID_MODES:
    raise ValueError(
        f"MODE must be one of {sorted(_VALID_MODES)}; got {MODE!r}. "
        "Typos like 'smoothed' or 'Filter' are NOT silently ignored."
    )

# ---------------------------------------------------------------------------
# Invariant assertions on the KNOB matrices. These run at module import so
# a malformed TRANSITIONS / EMISSIONS edit fails LOUDLY instead of yielding
# a plausible-but-wrong probability.
# ---------------------------------------------------------------------------

# TRANSITIONS: every row except the absorbing "final" row (last index)
# must sum to 1 across all columns (real states + end column).
_trans_real = TRANSITIONS[:-1]
_trans_row_sums = _trans_real.sum(axis=1)
assert np.allclose(_trans_row_sums, 1.0), (
    f"TRANSITIONS rows (excluding the final/absorbing row) must each sum to 1.0; "
    f"got row sums = {_trans_row_sums.tolist()}"
)

# EMISSIONS: the dummy initial (row 0) and final (last row) rows are zero
# by construction; every *real* state row must sum to 1 across the real
# observation columns (1..M). Column 0 is reserved for the None sentinel
# and must be zero.
_emit_real = EMISSIONS[1:-1, 1:]
_emit_row_sums = _emit_real.sum(axis=1)
assert np.allclose(_emit_row_sums, 1.0), (
    f"EMISSIONS real-state rows must sum to 1.0 across columns 1..M; "
    f"got row sums = {_emit_row_sums.tolist()}"
)
assert np.allclose(EMISSIONS[:, 0], 0.0), (
    "EMISSIONS column 0 is reserved for the None observation sentinel and must be 0."
)


# ---------------------------------------------------------------------------
# Algorithms
# ---------------------------------------------------------------------------


def main() -> None:
    np.set_printoptions(suppress=True)

    for observations in OBSERVATION_SETS:
        print("Observations: {}".format(" ".join(map(str, observations[1:]))))

        probability = compute_forward(STATES, observations, TRANSITIONS, EMISSIONS)
        print("Probability: {}".format(probability))

        path = compute_viterbi(STATES, observations, TRANSITIONS, EMISSIONS)
        print(f"Path: {convert_path_states_to_observations(path, STATES)}")

        if MODE == "viterbi":
            pass  # default: no extra output
        elif MODE == "filter":
            posteriors = compute_filtered(STATES, observations, TRANSITIONS, EMISSIONS)
            print("Filtered P(q_t | o_{1..t}):")
            for t, dist in enumerate(posteriors, start=1):
                print(f"  t={t}: " + ", ".join(
                    f"{name}={dist[i]:.4f}"
                    for i, name in enumerate(STATES[1:-1], start=1)
                ))
        elif MODE == "smooth":
            posteriors = compute_smoothed(STATES, observations, TRANSITIONS, EMISSIONS)
            print("Smoothed P(q_t | o_{1..T}):")
            for t, dist in enumerate(posteriors, start=1):
                print(f"  t={t}: " + ", ".join(
                    f"{name}={dist[i]:.4f}"
                    for i, name in enumerate(STATES[1:-1], start=1)
                ))
        else:
            raise ValueError(
                f"MODE must be one of {sorted(_VALID_MODES)}; got {MODE!r}. "
                "Typos like 'smoothed' or 'Filter' are NOT silently ignored."
            )

        print("")


def convert_path_states_to_observations(path: list[int], states: ndarray) -> list[str]:
    return [states[p] for p in path]


def inclusive_range(a: int, b: int) -> range:
    return range(a, b + 1)


def _forward_trellis(states: ndarray, observations: list[int | None], a_transitions: ndarray,
                     b_emissions: ndarray) -> ndarray:
    """Build the full forward trellis alpha[s, t] for s in 0..N+1, t in 0..T.

    Shared by compute_forward, compute_filtered, and compute_smoothed so
    that there is ONE source of truth for the forward recursion. Returns
    the alpha matrix with the dummy initial / final rows kept at zero
    (only the real-state rows 1..N and time columns 1..T are written).

    Indexing convention (matches L09b §4.2 modulo the augmented start /
    end states): t runs 1..T, s runs 1..N for real states.

    Initialisation:  alpha_1(s) = a_{0,s} * b_s(o_1).
    Recursion:       alpha_t(s) = sum_{s'} alpha_{t-1}(s') * a_{s',s} * b_s(o_t).
    """
    assert observations[0] is None, (
        "observations[0] must be None — the algorithms are 1-indexed and "
        f"use observations[0] as a sentinel. Got observations[0] = {observations[0]!r}."
    )

    big_n = len(states) - 2
    big_t = len(observations) - 1

    forward = np.zeros((big_n + 2, big_t + 1))

    # Initialisation step: alpha_1(s) = a_{0,s} * b_s(o_1) for each real state s.
    for s in inclusive_range(1, big_n):
        forward[s, 1] = a_transitions[0, s] * b_emissions[s, observations[1]]

    # Recursion step: alpha_t(s) = sum_{s'} alpha_{t-1}(s') * a_{s', s} * b_s(o_t).
    for t in inclusive_range(2, big_t):
        for s in inclusive_range(1, big_n):
            forward[s, t] = sum(
                forward[s_prev, t - 1] * a_transitions[s_prev, s] * b_emissions[s, observations[t]]
                for s_prev in inclusive_range(1, big_n)
            )

    return forward


def compute_forward(states: ndarray, observations: list[int | None], a_transitions: ndarray,
                    b_emissions: ndarray) -> float:
    # Why the index gymnastics: this implementation mirrors the
    # Jurafsky & Martin augmented formulation (start state q_0 in row 0
    # of TRANSITIONS, end state q_F in the last column). It is
    # equivalent to L09b §4.2's slide pseudocode under the encoding
    # `pi_s = a_{0,s}` and termination `sum_s alpha_T(s) * a_{s, qf}`
    # (which reduces to L09b's `sum_s alpha_T(s)` exactly when all real
    # states share the same end-transition probability, as in the
    # default HMM where a[hot,end] = a[cold,end] = 0.2).
    assert observations[0] is None, (
        "observations[0] must be None (sentinel for 1-based indexing)."
    )

    big_n = len(states) - 2
    big_t = len(observations) - 1
    qf: int = big_n + 1

    forward = _forward_trellis(states, observations, a_transitions, b_emissions)

    # Termination: alpha_F = sum_s alpha_T(s) * a_{s, qf}.
    alpha_final = sum(
        forward[s, big_t] * a_transitions[s, qf] for s in inclusive_range(1, big_n)
    )

    return float(alpha_final)


def compute_viterbi(states: ndarray, observations: list[int | None], a_transitions: ndarray,
                    b_emissions: ndarray) -> list[int]:
    # compute_viterbi differs from compute_forward in exactly two
    # places: (a) every `sum(...)` becomes `max(...)` and (b) we record
    # a backpointer for each cell. See L09b §4.4 and §6 Pitfall #2
    # ("Confusing forward alpha with Viterbi v").
    assert observations[0] is None, (
        "observations[0] must be None (sentinel for 1-based indexing)."
    )

    # number of states - subtract two because "initial" and "final" doesn't count.
    big_n = len(states) - 2

    # number of observations - subtract one, because a dummy "None" is added on index 0.
    big_t = len(observations) - 1

    # final state
    qf = big_n + 1

    # probability matrix - all values initialized to 5, as 0 is valid value in matrix
    viterbi = np.ones((big_n + 2, big_t + 1)) * 5

    # Must be of type int, otherwise it is tricky to use its elements to index
    # the states
    # all values initialized to 5, as 0 is valid value in matrix
    backpointers = np.ones((big_n + 2, big_t + 1), dtype=int) * 5

    # Initialization: same as Forward but we *also* set a backpointer of 0
    # (the start state) so the eventual back-trace terminates cleanly.
    for s in inclusive_range(1, big_n):
        viterbi[s, 1] = a_transitions[0, s] * b_emissions[s, observations[1]]
        backpointers[s, 1] = 0

    # Recursion: instead of summing over the previous column we take the
    # argmax — Viterbi keeps the *single best* path, not the marginal.
    for t in inclusive_range(2, big_t):
        for s in inclusive_range(1, big_n):
            scored_predecessors = [
                (s_prev,
                 viterbi[s_prev, t - 1] * a_transitions[s_prev, s] * b_emissions[s, observations[t]])
                for s_prev in inclusive_range(1, big_n)
            ]
            viterbi[s, t] = max(score for _, score in scored_predecessors)
            backpointers[s, t] = argmax(scored_predecessors)

    # Termination at the final dummy state.
    final_scored = [
        (s, viterbi[s, big_t] * a_transitions[s, qf]) for s in inclusive_range(1, big_n)
    ]
    viterbi[qf, big_t] = max(score for _, score in final_scored)
    backpointers[qf, big_t] = argmax(final_scored)

    # Backtrace: walk the backpointer chain from the final state back to t=1.
    # The returned list excludes the dummy start/end markers so the caller
    # sees a clean sequence of real hidden states ordered t=1..T.
    path: list[int] = [int(backpointers[qf, big_t])]
    for t in range(big_t, 1, -1):
        path.append(int(backpointers[path[-1], t]))
    path.reverse()
    return path


def compute_backward(states: ndarray, observations: list[int | None], a_transitions: ndarray,
                     b_emissions: ndarray) -> ndarray:
    """Backward trellis beta_t(s) = P(o_{t+1..T} | q_t = s, lambda).

    Used only by compute_smoothed (Variant 3). Mirrors the Forward
    pseudocode in reverse: initialise from the end-of-sequence transitions,
    recurse from t=T-1 down to t=1.

    NOTE: This is the *augmented* Jurafsky termination
    beta_T(s) = a_{s, qf}; L09b §4.6's non-augmented form uses
    beta_T(s) = 1. The two are equivalent when paired with the matching
    forward termination (`sum_s alpha_T(s) * a_{s, qf}` here vs
    `sum_s alpha_T(s)` in L09b).
    """
    assert observations[0] is None, (
        "observations[0] must be None (sentinel for 1-based indexing)."
    )

    big_n = len(states) - 2
    big_t = len(observations) - 1
    qf = big_n + 1

    backward = np.zeros((big_n + 2, big_t + 1))

    # Termination of the backward pass: probability of "reaching end" from each state.
    for s in inclusive_range(1, big_n):
        backward[s, big_t] = a_transitions[s, qf]

    for t in range(big_t - 1, 0, -1):
        for s in inclusive_range(1, big_n):
            backward[s, t] = sum(
                a_transitions[s, s_next] * b_emissions[s_next, observations[t + 1]] * backward[s_next, t + 1]
                for s_next in inclusive_range(1, big_n)
            )

    return backward


def compute_filtered(states: ndarray, observations: list[int | None], a_transitions: ndarray,
                     b_emissions: ndarray) -> list[ndarray]:
    """Per-step filtered distribution P(q_t = s | o_{1..t}) for t = 1..T.

    Builds the forward trellis via the shared `_forward_trellis()`
    helper and normalises each column. Returns a list of length T whose
    elements are length-(N+2) arrays (the initial / final entries are
    zero by construction).
    """
    big_t = len(observations) - 1

    forward = _forward_trellis(states, observations, a_transitions, b_emissions)

    distributions: list[ndarray] = []
    for t in inclusive_range(1, big_t):
        column = forward[:, t].copy()
        z = column.sum()
        distributions.append(column / z if z > 0 else column)
    return distributions


def compute_smoothed(states: ndarray, observations: list[int | None], a_transitions: ndarray,
                     b_emissions: ndarray) -> list[ndarray]:
    """Per-step smoothed distribution P(q_t = s | o_{1..T}) for t = 1..T.

    Standard forward-backward: posterior is proportional to alpha_t(s) *
    beta_t(s), then normalise across states for each t. Both alpha and
    beta come from the shared `_forward_trellis()` / `compute_backward`
    helpers — there is exactly one forward implementation in this file
    (L09b §4.6).
    """
    big_t = len(observations) - 1

    forward = _forward_trellis(states, observations, a_transitions, b_emissions)
    backward = compute_backward(states, observations, a_transitions, b_emissions)

    distributions: list[ndarray] = []
    for t in inclusive_range(1, big_t):
        unnormalised = forward[:, t] * backward[:, t]
        z = unnormalised.sum()
        distributions.append(unnormalised / z if z > 0 else unnormalised)
    return distributions


def argmax(sequence: list[tuple[float, float]]):
    '''
    This takes in a list, that provides its own keys as tuples.
    As such the following must hold true:
    sequence[i] = tuple(key, value)
    '''
    # I have rewritten this function slightly, to make it make better sense in my head
    return max(sequence, key=lambda x: x[1])[0]


if __name__ == '__main__':
    main()
