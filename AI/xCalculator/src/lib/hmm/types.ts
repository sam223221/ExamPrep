/**
 * Type definitions for a discrete Hidden Markov Model.
 *
 * Framework-free — no React, no DOM. Shared by the Forward (`forward.ts`) and
 * Viterbi (`viterbi.ts`) algorithms and the UI layer.
 *
 * Formulation (matching the course Lab 8 "ice-cream" model):
 *   - `states`  : hidden states, e.g. ["hot", "cold"].
 *   - `symbols` : observation alphabet, e.g. ["1", "2", "3"].
 *   - `start`   : π, the initial-state distribution (one entry per state).
 *   - `end`     : optional termination weight per state. When omitted it is
 *                 treated as 1 for every state (standard textbook Forward
 *                 without an explicit final state).
 *   - `A`       : transition matrix, states × states. Row i holds the
 *                 distribution P(next | current = state i): `A[i][j]` is the
 *                 probability of moving FROM state i TO state j.
 *   - `B`       : emission matrix, states × symbols. `B[i][k]` is the
 *                 probability of emitting symbol k while in state i.
 *
 * An observation sequence is an array of symbol indices into `symbols`.
 */
export interface HMMModel {
  states: string[];
  symbols: string[];
  start: number[];
  /** Optional per-state termination weight; defaults to all 1 when absent. */
  end?: number[];
  /** Transition matrix A[from][to], rows sum to 1. */
  A: number[][];
  /** Emission matrix B[state][symbol], rows sum to 1. */
  B: number[][];
}

/** Result of the Forward algorithm. */
export interface ForwardResult {
  /** P(O | model). */
  prob: number;
  /** α trellis: `trellis[stateIndex][t]` = α_t(state). */
  trellis: number[][];
}

/** Result of the Viterbi algorithm. */
export interface ViterbiResult {
  /** Probability of the single most-likely path. */
  prob: number;
  /** The most-likely hidden-state path, as state names. */
  path: string[];
  /** δ trellis: `delta[stateIndex][t]` = best score reaching `state` at t. */
  delta: number[][];
  /**
   * Backpointers: `backpointers[stateIndex][t]` = the previous state index that
   * maximised δ_t(state). At t = 0 the entries are -1 (no predecessor).
   */
  backpointers: number[][];
}

/**
 * Validate an HMM's shape and probability constraints.
 *
 * Returns a list of human-readable problems; an empty list means the model is
 * well-formed. Used by the UI to block a run with a clear message; the pure
 * algorithms assume a valid model and do not re-validate on the hot path.
 */
export function validateModel(model: HMMModel, tolerance = 1e-6): string[] {
  const problems: string[] = [];
  const n = model.states.length;
  const m = model.symbols.length;

  if (n < 1) problems.push('At least one hidden state is required.');
  if (m < 1) problems.push('At least one observation symbol is required.');

  if (model.start.length !== n) {
    problems.push(`Start vector has ${model.start.length} entries; expected ${n}.`);
  } else {
    const sum = model.start.reduce((acc, p) => acc + p, 0);
    if (Math.abs(sum - 1) > tolerance) {
      problems.push(`Start probabilities sum to ${sum.toFixed(4)} (must be 1).`);
    }
  }

  if (model.end && model.end.length !== n) {
    problems.push(`End vector has ${model.end.length} entries; expected ${n}.`);
  }

  // Whether the model uses explicit termination weights. When it does, each
  // transition row competes with its end weight, so row + end[i] = 1 (this is
  // the Lab 8 ice-cream formulation, where 0.2 of every row goes to "final").
  // Without an end vector, the transition row alone must sum to 1.
  const hasEnd = Boolean(model.end && model.end.length === n);

  if (model.A.length !== n) {
    problems.push(`Transition matrix has ${model.A.length} rows; expected ${n}.`);
  } else {
    model.A.forEach((row, i) => {
      if (row.length !== n) {
        problems.push(`Transition row "${model.states[i]}" has ${row.length} entries; expected ${n}.`);
        return;
      }
      const endWeight = hasEnd ? model.end![i]! : 0;
      const sum = row.reduce((acc, p) => acc + p, 0) + endWeight;
      if (Math.abs(sum - 1) > tolerance) {
        const detail = hasEnd
          ? `(transition row + end weight must be 1)`
          : `(must be 1)`;
        problems.push(`Transition row "${model.states[i]}" sums to ${sum.toFixed(4)} ${detail}.`);
      }
    });
  }

  if (model.B.length !== n) {
    problems.push(`Emission matrix has ${model.B.length} rows; expected ${n}.`);
  } else {
    model.B.forEach((row, i) => {
      if (row.length !== m) {
        problems.push(`Emission row "${model.states[i]}" has ${row.length} entries; expected ${m}.`);
        return;
      }
      const sum = row.reduce((acc, p) => acc + p, 0);
      if (Math.abs(sum - 1) > tolerance) {
        problems.push(`Emission row "${model.states[i]}" sums to ${sum.toFixed(4)} (must be 1).`);
      }
    });
  }

  return problems;
}

/**
 * Resolve the per-state termination weights, defaulting to all-ones when the
 * model has no explicit `end` vector.
 */
export function terminationWeights(model: HMMModel): number[] {
  if (model.end && model.end.length === model.states.length) {
    return model.end;
  }
  return model.states.map(() => 1);
}

/**
 * Map a sequence of observation symbols to their indices into `model.symbols`.
 * Throws on an unknown symbol so callers fail fast with a clear message.
 */
export function symbolsToIndices(model: HMMModel, sequence: readonly string[]): number[] {
  return sequence.map((symbol) => {
    const index = model.symbols.indexOf(symbol);
    if (index < 0) {
      throw new Error(`Observation "${symbol}" is not in the symbol alphabet.`);
    }
    return index;
  });
}
