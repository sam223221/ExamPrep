# DOCUMENT — src/components/probability/

The probability tab (spec §4).

## Files in this directory

| File              | Purpose                                                                                            |
| ----------------- | -------------------------------------------------------------------------------------------------- |
| `Probability.tsx` | Three-section probability tool. Default export, no props (matches the `App.tsx` panel contract).   |
| `DOCUMENT.md`     | This file.                                                                                         |

## What it does

Three labelled-form sections, each showing its formula (monospace) and a live result:

1. **Combinatorics** — `n!`, `nPr = n!/(n−r)!`, `nCr = n!/(r!(n−r)!)`. Integer inputs.
2. **Probability rules** — complement `1−P(A)`, union `P(A)+P(B)−P(A∩B)`, independent
   intersection `P(A)·P(B)`, conditional `P(A∩B)/P(B)`. Probability inputs in [0, 1].
3. **Bayes' theorem** — total-probability form; shows the posterior plus the worked terms
   (P(¬A), numerator, denominator = P(B)).

All math is delegated to `lib/probability.ts`. Results recompute live via `useMemo` on input
change. Blank inputs render a neutral `—`; invalid or out-of-range inputs (caught
`ProbabilityError`, e.g. `r > n`, probability outside [0, 1], `P(B)=0`) render an inline
`role="alert"` message in a red-tinted result box. The component never crashes on bad input.

## Key decisions

- **Stateless math.** This component holds only the input strings and renders results; every
  computation is a pure call into `lib/probability.ts`. No probability logic lives here.
- **String-state inputs.** Inputs are kept as strings so partially-typed/blank values are
  representable; `parseNum` converts and a section computes only when all its inputs parse.
- **`safeCompute` wrapper.** Centralizes the try/catch → inline-error mapping so each result
  line shows either a value or a friendly message.
- **Reusable subcomponents.** `Section`, `Formula`, `NumberField` (label tied to input via
  `useId`), and `ResultLine` keep the three sections consistent and accessible.

## Accessibility

Every input has a `<label htmlFor>` bound by `useId`; probability fields advertise
`min=0 max=1 step=0.01`; integer fields `step=1 min=0`. Error messages use `role="alert"`;
inputs show a visible `focus-visible` ring. Layout is responsive (single column on mobile,
multi-column grids from the `sm` breakpoint).
