import { describe, it, expect } from 'vitest';
import { forward } from '../hmm/forward';
import { viterbi } from '../hmm/viterbi';
import { type HMMModel, validateModel, symbolsToIndices } from '../hmm/types';

/**
 * The course Lab 8 "ice-cream" HMM.
 *
 *   states  = hot, cold        symbols = 1, 2, 3
 *   π       = [0.8, 0.2]       end     = [0.2, 0.2]
 *   A (from→to): hot→[0.2, 0.6], cold→[0.3, 0.5]
 *   B (state→symbol): hot→[0.1, 0.15, 0.75], cold→[0.8, 0.1, 0.1]
 *
 * Observation sequence "3 1 3" → symbol indices [2, 0, 2].
 */
function iceCreamModel(): HMMModel {
  return {
    states: ['hot', 'cold'],
    symbols: ['1', '2', '3'],
    start: [0.8, 0.2],
    end: [0.2, 0.2],
    A: [
      [0.2, 0.6],
      [0.3, 0.5],
    ],
    B: [
      [0.1, 0.15, 0.75],
      [0.8, 0.1, 0.1],
    ],
  };
}

const OBS = [2, 0, 2]; // "3 1 3"

describe('HMM — Forward algorithm (Lab 8 ice-cream)', () => {
  it('computes P(O) ≈ 0.0168092 for the observation "3 1 3"', () => {
    const result = forward(iceCreamModel(), OBS);
    expect(result.prob).toBeCloseTo(0.01681, 5);
  });

  it('returns an α trellis sized states × timesteps', () => {
    const result = forward(iceCreamModel(), OBS);
    expect(result.trellis.length).toBe(2);
    expect(result.trellis[0]!.length).toBe(3);
    // α_0(hot) = π_hot · B_hot(3) = 0.8 · 0.75 = 0.6
    expect(result.trellis[0]![0]).toBeCloseTo(0.6, 10);
    // α_0(cold) = π_cold · B_cold(3) = 0.2 · 0.1 = 0.02
    expect(result.trellis[1]![0]).toBeCloseTo(0.02, 10);
  });

  it('maps observation symbols to indices', () => {
    const model = iceCreamModel();
    expect(symbolsToIndices(model, ['3', '1', '3'])).toEqual([2, 0, 2]);
  });

  it('reports the ice-cream model as well-formed', () => {
    expect(validateModel(iceCreamModel())).toEqual([]);
  });
});

describe('HMM — Viterbi algorithm (Lab 8 ice-cream)', () => {
  it('recovers the most-likely path ["hot", "cold", "hot"]', () => {
    const result = viterbi(iceCreamModel(), OBS);
    expect(result.path).toEqual(['hot', 'cold', 'hot']);
  });

  it('computes the best-path probability ≈ 0.01296', () => {
    const result = viterbi(iceCreamModel(), OBS);
    expect(result.prob).toBeCloseTo(0.01296, 5);
  });

  it('returns δ and backpointer trellises sized states × timesteps', () => {
    const result = viterbi(iceCreamModel(), OBS);
    expect(result.delta.length).toBe(2);
    expect(result.delta[0]!.length).toBe(3);
    expect(result.backpointers.length).toBe(2);
    expect(result.backpointers[0]!.length).toBe(3);
    // t = 0 has no predecessor.
    expect(result.backpointers[0]![0]).toBe(-1);
    expect(result.backpointers[1]![0]).toBe(-1);
  });
});

describe('HMM — input guards', () => {
  it('throws on an empty observation sequence', () => {
    expect(() => forward(iceCreamModel(), [])).toThrow(/non-empty/i);
    expect(() => viterbi(iceCreamModel(), [])).toThrow(/non-empty/i);
  });

  it('throws on an out-of-range observation index', () => {
    expect(() => forward(iceCreamModel(), [9])).toThrow(/out of range/i);
    expect(() => viterbi(iceCreamModel(), [9])).toThrow(/out of range/i);
  });

  it('throws on an unknown observation symbol', () => {
    expect(() => symbolsToIndices(iceCreamModel(), ['4'])).toThrow(/not in the symbol/i);
  });
});
