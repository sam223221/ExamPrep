/**
 * Probability & combinatorics utilities.
 *
 * Framework-free, pure functions — NO React. Combinatorics uses an exact BigInt
 * path internally so factorials / nPr / nCr never suffer floating-point drift,
 * then converts the (integer) result back to a Number for the UI. Probability
 * rules validate their inputs to the closed interval [0, 1] and throw a typed
 * {@link ProbabilityError} on bad input so callers can show inline messages.
 */

/** Error thrown for invalid combinatorics or probability inputs. */
export class ProbabilityError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ProbabilityError';
    Object.setPrototypeOf(this, ProbabilityError.prototype);
  }
}

/* ------------------------------------------------------------------ */
/* Validation helpers                                                  */
/* ------------------------------------------------------------------ */

/** Assert that `n` is a non-negative integer; throw {@link ProbabilityError} otherwise. */
function assertNonNegativeInteger(n: number, label: string): void {
  if (!Number.isFinite(n) || !Number.isInteger(n)) {
    throw new ProbabilityError(`${label} must be an integer`);
  }
  if (n < 0) {
    throw new ProbabilityError(`${label} must be ≥ 0`);
  }
}

/** Assert that `p` is a probability in [0, 1]; throw {@link ProbabilityError} otherwise. */
function assertProbability(p: number, label: string): void {
  if (!Number.isFinite(p)) {
    throw new ProbabilityError(`${label} must be a number`);
  }
  if (p < 0 || p > 1) {
    throw new ProbabilityError(`${label} must be between 0 and 1`);
  }
}

/* ------------------------------------------------------------------ */
/* Combinatorics (exact via BigInt)                                    */
/* ------------------------------------------------------------------ */

/** Exact n! as a BigInt. Caller guarantees `n` is a non-negative integer. */
function factorialBig(n: number): bigint {
  let acc = 1n;
  for (let k = 2; k <= n; k += 1) {
    acc *= BigInt(k);
  }
  return acc;
}

/**
 * Convert an exact BigInt count to a Number, guarding against silent precision
 * loss beyond `Number.MAX_SAFE_INTEGER`.
 */
function bigToSafeNumber(value: bigint, context: string): number {
  if (value > BigInt(Number.MAX_SAFE_INTEGER)) {
    throw new ProbabilityError(
      `${context} exceeds the safe integer range; result would be imprecise`,
    );
  }
  return Number(value);
}

/**
 * Exact factorial `n!`.
 *
 * Computed with BigInt to stay exact, then returned as a Number. Throws if `n`
 * is not a non-negative integer, or if `n!` exceeds the safe-integer range.
 *
 * @example factorial(6) // 720
 */
export function factorial(n: number): number {
  assertNonNegativeInteger(n, 'n');
  return bigToSafeNumber(factorialBig(n), `${n}!`);
}

/**
 * Permutations `nPr = n! / (n − r)!` — ordered selections of r from n.
 *
 * Computed as the exact falling factorial `n · (n−1) · … · (n−r+1)` in BigInt.
 * Throws if n or r are not non-negative integers, or if `r > n`.
 *
 * @example permutations(5, 2) // 20
 */
export function permutations(n: number, r: number): number {
  assertNonNegativeInteger(n, 'n');
  assertNonNegativeInteger(r, 'r');
  if (r > n) {
    throw new ProbabilityError('r must not exceed n');
  }
  let acc = 1n;
  for (let k = 0; k < r; k += 1) {
    acc *= BigInt(n - k);
  }
  return bigToSafeNumber(acc, 'nPr');
}

/**
 * Combinations `nCr = n! / (r!·(n−r)!)` — unordered selections of r from n.
 *
 * Uses the multiplicative formula with the smaller of `r`/`n−r` to keep the
 * intermediate BigInt small; every partial product divides exactly. Throws if
 * n or r are not non-negative integers, or if `r > n`.
 *
 * @example combinations(5, 2)  // 10
 * @example combinations(10, 3) // 120
 * @example combinations(7, 0)  // 1
 */
export function combinations(n: number, r: number): number {
  assertNonNegativeInteger(n, 'n');
  assertNonNegativeInteger(r, 'r');
  if (r > n) {
    throw new ProbabilityError('r must not exceed n');
  }
  // Symmetry: C(n, r) === C(n, n − r); pick the smaller k for fewer iterations.
  const k = Math.min(r, n - r);
  let acc = 1n;
  for (let i = 0; i < k; i += 1) {
    // acc = acc * (n − i) / (i + 1); exact at each step for binomial coefficients.
    acc = (acc * BigInt(n - i)) / BigInt(i + 1);
  }
  return bigToSafeNumber(acc, 'nCr');
}

/* ------------------------------------------------------------------ */
/* Probability rules                                                   */
/* ------------------------------------------------------------------ */

/** Complement: `P(¬A) = 1 − P(A)`. */
export function complement(p: number): number {
  assertProbability(p, 'P(A)');
  return 1 - p;
}

/**
 * Inclusion–exclusion union: `P(A∪B) = P(A) + P(B) − P(A∩B)`.
 * Validates each input to [0, 1].
 */
export function unionProb(pA: number, pB: number, pAB: number): number {
  assertProbability(pA, 'P(A)');
  assertProbability(pB, 'P(B)');
  assertProbability(pAB, 'P(A∩B)');
  return pA + pB - pAB;
}

/** Intersection of independent events: `P(A∩B) = P(A)·P(B)`. */
export function intersectionIndependent(pA: number, pB: number): number {
  assertProbability(pA, 'P(A)');
  assertProbability(pB, 'P(B)');
  return pA * pB;
}

/**
 * Conditional probability: `P(A|B) = P(A∩B) / P(B)`.
 * Validates inputs to [0, 1] and guards against `P(B) = 0`.
 */
export function conditional(pAB: number, pB: number): number {
  assertProbability(pAB, 'P(A∩B)');
  assertProbability(pB, 'P(B)');
  if (pB === 0) {
    throw new ProbabilityError('P(B) must be greater than 0 to condition on B');
  }
  return pAB / pB;
}

/* ------------------------------------------------------------------ */
/* Bayes' theorem                                                      */
/* ------------------------------------------------------------------ */

/** Result of {@link bayes}: the posterior plus the intermediate terms for display. */
export interface BayesResult {
  /** Posterior P(A|B). */
  posterior: number;
  /** Numerator: P(B|A)·P(A). */
  numerator: number;
  /** Denominator: P(B|A)·P(A) + P(B|¬A)·P(¬A) = P(B). */
  denominator: number;
  /** Prior complement P(¬A) = 1 − P(A). */
  priorComplement: number;
}

/**
 * Bayes' theorem in total-probability form:
 *
 *   P(A|B) = P(B|A)·P(A) / [ P(B|A)·P(A) + P(B|¬A)·P(¬A) ]
 *
 * Returns the posterior together with the numerator, denominator and P(¬A) so
 * the UI can show the worked steps. Validates all three inputs to [0, 1] and
 * guards against a zero denominator (B impossible under the model).
 *
 * @example bayes(0.01, 0.99, 0.05).posterior // ≈ 0.16667
 */
export function bayes(pA: number, pBgivenA: number, pBgivenNotA: number): BayesResult {
  assertProbability(pA, 'P(A)');
  assertProbability(pBgivenA, 'P(B|A)');
  assertProbability(pBgivenNotA, 'P(B|¬A)');

  const priorComplement = 1 - pA;
  const numerator = pBgivenA * pA;
  const denominator = numerator + pBgivenNotA * priorComplement;

  if (denominator === 0) {
    throw new ProbabilityError(
      'P(B) is 0 under these inputs; the posterior P(A|B) is undefined',
    );
  }

  return {
    posterior: numerator / denominator,
    numerator,
    denominator,
    priorComplement,
  };
}
