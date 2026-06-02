/**
 * The Viterbi algorithm for Hidden Markov Models.
 *
 * Pure TypeScript — no React, no DOM. Computes the single most-likely hidden
 * state path and its probability, returning the δ (best-score) trellis and the
 * backpointer table so the UI can display the dynamic-programming steps and the
 * recovered path.
 *
 * Recurrences (max instead of sum versus Forward):
 *   Init      δ_0(s) = π[s] · b_s(o_0),                     bp_0(s) = -1
 *   Recurse   δ_t(s) = max_{s'} [ δ_{t-1}(s') · a_{s' s} ] · b_s(o_t)
 *             bp_t(s) = argmax_{s'} [ δ_{t-1}(s') · a_{s' s} ]
 *   Terminate best   = argmax_s δ_{T-1}(s) · end[s]   (end defaults to 1)
 *   Backtrack follow bp from the best terminal state to t = 0.
 *
 * Trellises are indexed `[stateIndex][t]`.
 */

import { type HMMModel, type ViterbiResult, terminationWeights } from './types';

/**
 * Run the Viterbi algorithm.
 *
 * @param model The HMM (assumed well-formed; validate via `validateModel`).
 * @param obs   Observation sequence as symbol indices into `model.symbols`.
 * @throws if an observation index is out of range or the sequence is empty.
 */
export function viterbi(model: HMMModel, obs: number[]): ViterbiResult {
  const n = model.states.length;
  const t = obs.length;

  if (t === 0) {
    throw new Error('Viterbi requires a non-empty observation sequence.');
  }
  for (const o of obs) {
    if (o < 0 || o >= model.symbols.length || !Number.isInteger(o)) {
      throw new Error(`Observation index ${o} is out of range.`);
    }
  }

  // delta[s][time] = best score of any path ending in state s at this time.
  const delta: number[][] = Array.from({ length: n }, () =>
    new Array<number>(t).fill(0),
  );
  // backpointers[s][time] = predecessor state index on the best path.
  const backpointers: number[][] = Array.from({ length: n }, () =>
    new Array<number>(t).fill(-1),
  );

  // Initialization at time 0.
  for (let s = 0; s < n; s++) {
    delta[s]![0] = model.start[s]! * model.B[s]![obs[0]!]!;
    backpointers[s]![0] = -1;
  }

  // Recursion for times 1 .. T-1.
  for (let time = 1; time < t; time++) {
    const symbol = obs[time]!;
    for (let s = 0; s < n; s++) {
      let bestScore = -Infinity;
      let bestPrev = 0;
      for (let prev = 0; prev < n; prev++) {
        const score = delta[prev]![time - 1]! * model.A[prev]![s]!;
        if (score > bestScore) {
          bestScore = score;
          bestPrev = prev;
        }
      }
      delta[s]![time] = bestScore * model.B[s]![symbol]!;
      backpointers[s]![time] = bestPrev;
    }
  }

  // Termination: pick the best final state, weighted by end probabilities.
  const end = terminationWeights(model);
  let bestFinalScore = -Infinity;
  let bestFinalState = 0;
  for (let s = 0; s < n; s++) {
    const score = delta[s]![t - 1]! * end[s]!;
    if (score > bestFinalScore) {
      bestFinalScore = score;
      bestFinalState = s;
    }
  }

  // Backtrack from the best terminal state to recover the path.
  const pathIndices = new Array<number>(t);
  pathIndices[t - 1] = bestFinalState;
  for (let time = t - 1; time > 0; time--) {
    pathIndices[time - 1] = backpointers[pathIndices[time]!]![time]!;
  }

  const path = pathIndices.map((stateIndex) => model.states[stateIndex]!);

  return { prob: bestFinalScore, path, delta, backpointers };
}
