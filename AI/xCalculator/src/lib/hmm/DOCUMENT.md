# `src/lib/hmm` — HMM math (framework-free)

Pure TypeScript implementation of the discrete Hidden Markov Model algorithms.
No React, no DOM — every function here is independently unit-testable and is
exercised by `src/lib/__tests__/hmm.test.ts`.

## Files

- **`types.ts`** — the `HMMModel` type and result types (`ForwardResult`,
  `ViterbiResult`), plus boundary helpers:
  - `validateModel(model)` → list of human-readable problems (empty = valid).
    Validates dimensions and probability sums. **Transition-row rule:** when the
    model has an explicit `end` vector, each transition row competes with its
    end weight, so `Σ_j A[i][j] + end[i] = 1`; without `end`, the row alone must
    sum to 1.
  - `terminationWeights(model)` → resolves `end`, defaulting to all-ones.
  - `symbolsToIndices(model, sequence)` → maps observation symbols to indices,
    throwing on an unknown symbol.
- **`forward.ts`** — `forward(model, obs)` → `{ prob, trellis }`. The Forward
  algorithm. `trellis[stateIndex][t] = α_t(state)`.
  - Init `α_0(s) = π[s]·b_s(o_0)`; recurse `α_t(s) = (Σ_{s'} α_{t-1}(s')·a_{s's})·b_s(o_t)`;
    terminate `P(O) = Σ_s α_{T-1}(s)·end[s]` (`end` defaults to 1).
- **`viterbi.ts`** — `viterbi(model, obs)` → `{ prob, path, delta, backpointers }`.
  Same recurrence as Forward but with `max`/`argmax`; records backpointers and
  backtracks from the best terminal state to recover the state-name path.

## Model conventions

- `states` (hidden), `symbols` (observation alphabet).
- `start` = π over states; optional `end` = per-state termination weight.
- `A[from][to]` transition matrix; `B[state][symbol]` emission matrix.
- An observation sequence is an array of **symbol indices** into `symbols`.

## Reference & verification

Matches the course Lab 8 "ice-cream" model. With states `hot/cold`, symbols
`1/2/3`, π `[0.8,0.2]`, end `[0.2,0.2]`, `A=[[0.2,0.6],[0.3,0.5]]`,
`B=[[0.1,0.15,0.75],[0.8,0.1,0.1]]`, observation `3 1 3` → `[2,0,2]`:

- Forward `P(O) ≈ 0.0168092`.
- Viterbi best path `["hot","cold","hot"]`, `P ≈ 0.01296`.

The original Lab 8 (`AI/Lab 8/handout/hidden_markov_models.py`) folds the start
and end into an explicit initial/final state. Here that is abstracted into the
`start` (π) and `end` vectors with `A`/`B` over the real states only; the 0.2
"to-final" mass of each Lab 8 transition row becomes `end[i] = 0.2`.

## Connections

Consumed only by `src/components/hmm/*` (the UI). The UI holds no probability
logic — it validates input via `validateModel`, then calls `forward`/`viterbi`.
