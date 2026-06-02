/**
 * The Forward algorithm for Hidden Markov Models.
 *
 * Pure TypeScript — no React, no DOM. Computes the likelihood `P(O | model)`
 * of an observation sequence and returns the full α trellis so the UI can show
 * the dynamic-programming table step by step.
 *
 * Recurrences (matching the course Lab 8 formulation):
 *   Init      α_0(s) = π[s] · b_s(o_0)
 *   Recurse   α_t(s) = ( Σ_{s'} α_{t-1}(s') · a_{s' s} ) · b_s(o_t)
 *   Terminate P(O)   = Σ_s α_{T-1}(s) · end[s]   (end defaults to 1)
 *
 * The returned trellis is indexed `[stateIndex][t]`.
 */

import { type HMMModel, type ForwardResult, terminationWeights } from './types';

/**
 * Run the Forward algorithm.
 *
 * @param model The HMM (assumed well-formed; validate via `validateModel`).
 * @param obs   Observation sequence as symbol indices into `model.symbols`.
 * @throws if an observation index is out of range or the sequence is empty.
 */
export function forward(model: HMMModel, obs: number[]): ForwardResult {
  const n = model.states.length;
  const t = obs.length;

  if (t === 0) {
    throw new Error('Forward requires a non-empty observation sequence.');
  }
  for (const o of obs) {
    if (o < 0 || o >= model.symbols.length || !Number.isInteger(o)) {
      throw new Error(`Observation index ${o} is out of range.`);
    }
  }

  // trellis[s][time] = α_time(s). Pre-fill with zeros.
  const trellis: number[][] = Array.from({ length: n }, () =>
    new Array<number>(t).fill(0),
  );

  // Initialization at time 0.
  for (let s = 0; s < n; s++) {
    trellis[s]![0] = model.start[s]! * model.B[s]![obs[0]!]!;
  }

  // Recursion for times 1 .. T-1.
  for (let time = 1; time < t; time++) {
    const symbol = obs[time]!;
    for (let s = 0; s < n; s++) {
      let incoming = 0;
      for (let prev = 0; prev < n; prev++) {
        incoming += trellis[prev]![time - 1]! * model.A[prev]![s]!;
      }
      trellis[s]![time] = incoming * model.B[s]![symbol]!;
    }
  }

  // Termination: weight the final column by the per-state end probabilities.
  const end = terminationWeights(model);
  let prob = 0;
  for (let s = 0; s < n; s++) {
    prob += trellis[s]![t - 1]! * end[s]!;
  }

  return { prob, trellis };
}
