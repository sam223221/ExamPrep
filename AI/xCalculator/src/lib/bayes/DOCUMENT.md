# `src/lib/bayes` — Bayesian-network math (framework-free)

Pure TypeScript model and exact-inference engine for discrete Bayesian
networks. No React, no DOM. Exercised by `src/lib/__tests__/bayes.test.ts`.

## Files

- **`types.ts`** — the network model:
  - `BNNode` = `{ id, name, states[], parents[], cpt }`. `parents` is the
    ordered list of parent ids; that order defines the order of values in CPT
    keys.
  - `Cpt` = `Record<string, number[]>`. The key encodes the parent-state tuple
    (parent order) via `cptKey([...])`; the value is a distribution aligned to
    the node's `states`. Roots use the empty-tuple key `""`.
  - `cptKey` / `parseCptKey` use the unit-separator char (U+001F) so state names
    can contain any printable text without colliding with the delimiter.
- **`inference.ts`** — exact inference by enumeration (AIMA ENUMERATION-ASK /
  ENUMERATE-ALL):
  - `enumerationAsk(queryVar, evidence, network)` → normalized
    `Record<state, number>` posterior over the query variable.
  - `marginal(queryVar, network)` → `enumerationAsk` with empty evidence.
  - `jointProbability(fullAssignment, network)` = `Π P(xi | parents(xi))`.
  - `topologicalOrder(network)` (Kahn's algorithm) — **throws on a cycle** or a
    missing parent reference; the network must be a DAG.
  - `conditionalProbability(node, value, assignment)` — CPT lookup helper.
  - `validateCpts(network)` / `isDag(network)` — non-throwing checks the UI uses
    to display a clear "network invalid" message.

## Design notes

- Enumeration is exponential in the number of hidden variables — acceptable for
  exam-sized networks (the documented scope).
- The formulation mirrors the course `Lab7/handout/Variable.py`: a per-node CPT
  keyed by ordered parent assignments, distributions aligned to the node's
  ordered states.
- Multi-valued variables and arbitrary evidence subsets are supported.

## Verification

The AIMA Alarm network (built in the test) gives
`P(Burglary=true | JohnCalls=true, MaryCalls=true) ≈ 0.2842`, the posterior sums
to 1, `P(Alarm=true) ≈ 0.00252`, and a 2-node cycle throws.

## Connections

Consumed by `src/components/bayes/*` (the UI). The UI builds the model from the
React Flow graph and calls these functions; it holds no inference logic.
