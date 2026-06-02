import { describe, it, expect } from 'vitest';
import {
  factorial,
  permutations,
  combinations,
  complement,
  unionProb,
  intersectionIndependent,
  conditional,
  bayes,
  ProbabilityError,
} from '../probability';

describe('factorial', () => {
  it('factorial(0) = 1', () => {
    expect(factorial(0)).toBe(1);
  });

  it('factorial(1) = 1', () => {
    expect(factorial(1)).toBe(1);
  });

  it('factorial(6) = 720', () => {
    expect(factorial(6)).toBe(720);
  });

  it('factorial(10) = 3628800 (exact, no float drift)', () => {
    expect(factorial(10)).toBe(3628800);
  });

  it('throws on negative input', () => {
    expect(() => factorial(-1)).toThrow(ProbabilityError);
  });

  it('throws on non-integer input', () => {
    expect(() => factorial(2.5)).toThrow(ProbabilityError);
  });
});

describe('permutations (nPr)', () => {
  it('permutations(5, 2) = 20', () => {
    expect(permutations(5, 2)).toBe(20);
  });

  it('permutations(n, 0) = 1', () => {
    expect(permutations(8, 0)).toBe(1);
  });

  it('permutations(n, n) = n!', () => {
    expect(permutations(5, 5)).toBe(120);
  });

  it('throws when r > n', () => {
    expect(() => permutations(3, 5)).toThrow(ProbabilityError);
  });

  it('throws on negative r', () => {
    expect(() => permutations(5, -1)).toThrow(ProbabilityError);
  });
});

describe('combinations (nCr)', () => {
  it('combinations(5, 2) = 10', () => {
    expect(combinations(5, 2)).toBe(10);
  });

  it('combinations(10, 3) = 120', () => {
    expect(combinations(10, 3)).toBe(120);
  });

  it('combinations(n, 0) = 1', () => {
    expect(combinations(7, 0)).toBe(1);
  });

  it('combinations(n, n) = 1', () => {
    expect(combinations(7, 7)).toBe(1);
  });

  it('is symmetric: combinations(10, 7) = combinations(10, 3)', () => {
    expect(combinations(10, 7)).toBe(combinations(10, 3));
  });

  it('stays exact for a large value (combinations(52, 5) = 2598960)', () => {
    expect(combinations(52, 5)).toBe(2598960);
  });

  it('throws when r > n', () => {
    expect(() => combinations(3, 5)).toThrow(ProbabilityError);
  });

  it('throws on negative n', () => {
    expect(() => combinations(-3, 1)).toThrow(ProbabilityError);
  });
});

describe('probability rules', () => {
  it('complement(0.3) = 0.7', () => {
    expect(complement(0.3)).toBeCloseTo(0.7, 12);
  });

  it('unionProb: P(A∪B) = P(A) + P(B) − P(A∩B)', () => {
    expect(unionProb(0.5, 0.4, 0.2)).toBeCloseTo(0.7, 12);
  });

  it('intersectionIndependent: P(A∩B) = P(A)·P(B)', () => {
    expect(intersectionIndependent(0.5, 0.4)).toBeCloseTo(0.2, 12);
  });

  it('conditional: P(A|B) = P(A∩B) / P(B)', () => {
    expect(conditional(0.2, 0.5)).toBeCloseTo(0.4, 12);
  });

  it('conditional throws when P(B) = 0', () => {
    expect(() => conditional(0.2, 0)).toThrow(ProbabilityError);
  });

  it('rules throw on out-of-range probabilities', () => {
    expect(() => complement(1.5)).toThrow(ProbabilityError);
    expect(() => complement(-0.1)).toThrow(ProbabilityError);
    expect(() => unionProb(0.5, 1.2, 0.1)).toThrow(ProbabilityError);
    expect(() => intersectionIndependent(0.5, -0.2)).toThrow(ProbabilityError);
  });
});

describe('bayes', () => {
  it('worked case: bayes(0.01, 0.99, 0.05).posterior ≈ 0.16667', () => {
    const result = bayes(0.01, 0.99, 0.05);
    expect(result.posterior).toBeCloseTo(0.16667, 5);
  });

  it('exposes intermediate numerator / denominator / P(¬A)', () => {
    const result = bayes(0.01, 0.99, 0.05);
    expect(result.numerator).toBeCloseTo(0.0099, 12);
    expect(result.priorComplement).toBeCloseTo(0.99, 12);
    expect(result.denominator).toBeCloseTo(0.0099 + 0.05 * 0.99, 12);
    expect(result.posterior).toBeCloseTo(result.numerator / result.denominator, 12);
  });

  it('a certain prior collapses the posterior to 1', () => {
    expect(bayes(1, 0.5, 0.5).posterior).toBeCloseTo(1, 12);
  });

  it('throws when an input is out of [0, 1]', () => {
    expect(() => bayes(1.1, 0.5, 0.5)).toThrow(ProbabilityError);
    expect(() => bayes(0.5, -0.1, 0.5)).toThrow(ProbabilityError);
  });

  it('throws when the denominator is 0 (B impossible)', () => {
    expect(() => bayes(0.5, 0, 0)).toThrow(ProbabilityError);
  });
});
