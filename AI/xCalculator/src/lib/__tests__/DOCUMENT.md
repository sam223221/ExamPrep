# DOCUMENT — src/lib/\_\_tests\_\_/

Vitest specs for the framework-free algorithm modules in `src/lib`. The project's
vitest `include` glob is `src/**/__tests__/**`, so every `*.test.ts` here is picked up
automatically. Each suite imports the pure functions directly (no DOM, no React) and
asserts both correctness on known cases and the typed-error behaviour at the boundaries.

## Files in this directory

| File                   | Purpose                                                                                                  |
| ---------------------- | -------------------------------------------------------------------------------------------------------- |
| `calc.test.ts`         | Specs for `lib/calc.ts` — the safe arithmetic evaluator (precedence, associativity, errors, internals). |
| `probability.test.ts`  | Specs for `lib/probability.ts` — combinatorics, probability rules, and Bayes' theorem.                   |
| `bayes.test.ts`        | Specs for `lib/bayes/inference.ts` — exact Bayesian-network inference by enumeration over the AIMA Alarm network. |
| `hmm.test.ts`          | Specs for `lib/hmm/forward.ts` + `lib/hmm/viterbi.ts` — Forward and Viterbi over the Lab 8 ice-cream HMM. |
| `DOCUMENT.md`          | This file.                                                                                               |

## Headline asserted values

These are the load-bearing numeric anchors each suite locks in; if a refactor changes
any of them, a test fails.

### `calc.test.ts`

- Precedence / associativity: `2+3*4 = 14`, `(2+3)*4 = 20`, `2^10 = 1024`,
  `2^3^2 = 512` (right-associative `^`), `(1+2)*(3+4)^2 = 147`.
- Unary minus: `-3+5 = 2`, `2 * -3 = -6`, `10 - (-4) = 14`, and the documented
  `-2^2 = 4` (unary binds tighter than `^`).
- Errors throw `CalcError`: division by zero, malformed operator runs (`2+*3`), trailing
  operator (`2+`), unmatched parens, empty input, illegal characters, malformed number
  (`1.2.3`).
- Internals: `tokenize` classifies a leading `-` as `unary: true` and the `-` in `5-3` as
  binary; `toRpn(tokenize('2+3*4'))` yields RPN `[2, 3, 4, *, +]`.

### `probability.test.ts`

- Combinatorics (exact, no float drift): `factorial(6) = 720`, `factorial(10) = 3628800`;
  `permutations(5,2) = 20`, `permutations(5,5) = 120`; `combinations(5,2) = 10`,
  `combinations(10,3) = 120`, symmetry `combinations(10,7) = combinations(10,3)`, and the
  large exact case `combinations(52,5) = 2598960`.
- Probability rules: `complement(0.3) = 0.7`, `unionProb(0.5,0.4,0.2) = 0.7`,
  `intersectionIndependent(0.5,0.4) = 0.2`, `conditional(0.2,0.5) = 0.4`.
- Bayes: worked case `bayes(0.01, 0.99, 0.05).posterior ≈ 0.16667`, with intermediate
  `numerator ≈ 0.0099` and `denominator` verified against `numerator/denominator`; a certain
  prior collapses the posterior to `1`.
- Guards throw `ProbabilityError`: negative / non-integer factorial input, `r > n`, negative
  `r`/`n`, out-of-range probabilities, `conditional` with `P(B) = 0`, and Bayes with an
  impossible `B`.

### `bayes.test.ts`

- Fixture: the canonical AIMA Alarm/Burglary network (Russell & Norvig, Fig. 14.2), states
  ordered `["true", "false"]`.
- **`P(Burglary=true | JohnCalls=true, MaryCalls=true) ≈ 0.284`** (`enumerationAsk`), with the
  returned distribution normalized to sum 1 (`false ≈ 1 − 0.2841718`).
- Marginals: `P(Alarm=true) ≈ 0.002516`, `P(Burglary=true) = 0.001` (empty evidence).
- Full-joint chain rule: `P(j, m, a, ¬b, ¬e) = 0.9·0.7·0.001·0.999·0.998 ≈ 0.00062811`.
- Structure: `topologicalOrder` puts parents before children; `validateCpts` reports the
  well-formed network as valid (`[]`); a 2-node cycle `A→B→A` throws (`/cycle/i`); a 3-state
  `Weather` query confirms multi-valued support.

### `hmm.test.ts`

- Fixture: the course Lab 8 "ice-cream" HMM — states `hot, cold`; symbols `1, 2, 3`;
  `π = [0.8, 0.2]`, `end = [0.2, 0.2]`; observation `"3 1 3"` → symbol indices `[2, 0, 2]`.
- **Forward: `P(O) ≈ 0.0168092` for `"3 1 3"`**; α trellis is `states × timesteps` (2 × 3) with
  `α₀(hot) = 0.8·0.75 = 0.6` and `α₀(cold) = 0.2·0.1 = 0.02`; `symbolsToIndices(["3","1","3"]) = [2,0,2]`.
- **Viterbi: best path `["hot", "cold", "hot"]` with probability ≈ `0.01296`**; δ and backpointer
  trellises are `states × timesteps`, and the `t = 0` backpointers are `-1` (no predecessor).
- Guards: empty observation sequence throws (`/non-empty/i`), out-of-range index throws
  (`/out of range/i`), and an unknown symbol throws from `symbolsToIndices` (`/not in the symbol/i`).
