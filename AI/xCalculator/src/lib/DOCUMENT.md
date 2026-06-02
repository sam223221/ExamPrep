# DOCUMENT — src/lib/

Framework-free TypeScript modules. All algorithms live here so they stay independently
testable; UI components import these and contain no math logic. Vitest specs live in
`src/lib/__tests__/` (the project's vitest `include` glob is `src/**/__tests__/**`).

## Files in this directory

| File                       | Purpose                                                                                                                  |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `calc.ts`                  | Safe arithmetic evaluator (no `eval`): `tokenize` → `toRpn` (shunting-yard) → `evalRpn`. `evaluate(expr)` is the public entry; throws `CalcError` on malformed input or division by zero. Supports `+ - * / ^`, unary minus, parentheses, decimals; `^` right-associative. |
| `probability.ts`           | Combinatorics (`factorial`, `permutations`, `combinations` — exact via BigInt) and probability rules (`complement`, `unionProb`, `intersectionIndependent`, `conditional`) plus `bayes` (returns posterior + numerator/denominator/P(¬A)). Validates inputs and throws `ProbabilityError`. |
| `__tests__/calc.test.ts`        | Vitest suite for `calc.ts`: precedence, right-associative `^`, unary minus, divide-by-zero and malformed-input errors. |
| `__tests__/probability.test.ts` | Vitest suite for `probability.ts`: `factorial(6)=720`, `nPr(5,2)=20`, `nCr(5,2)=10`, `nCr(10,3)=120`, a worked Bayes case (`≈0.16667`), and `r>n` / out-of-range throws. |

## Subdirectories

- `bayes/` (`types.ts`, `inference.ts`) and `hmm/` (`types.ts`, `forward.ts`, `viterbi.ts`)
  are owned by a separate engineer and **documented in their own `DOCUMENT.md`** files.

## Key decisions

- **No `eval` / `Function`.** `calc.ts` is a hand-written shunting-yard parser per the spec
  (§3) and security plan (§6).
- **BigInt for combinatorics.** `factorial`/`nPr`/`nCr` compute exactly in BigInt and convert
  to Number only for the final (integer) result, guarding against silent precision loss past
  `Number.MAX_SAFE_INTEGER`.
- **Unary-minus precedence.** Unary minus binds tighter than `^`, so `-2^2` evaluates to
  `(-2)^2 = 4` — a deliberate, documented choice for a study calculator where the typed text
  reflects exactly what the user sees.
- **Typed errors.** `CalcError` and `ProbabilityError` let UI layers catch and show friendly
  inline messages instead of crashing.
