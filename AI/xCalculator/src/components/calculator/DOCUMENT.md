# DOCUMENT — src/components/calculator/

The arithmetic calculator tab (spec §3).

## Files in this directory

| File             | Purpose                                                                                          |
| ---------------- | ------------------------------------------------------------------------------------------------ |
| `Calculator.tsx` | Button-grid + keyboard calculator. Default export, no props (matches the `App.tsx` panel contract). |
| `DOCUMENT.md`    | This file.                                                                                       |

## What it does

- Maintains a live expression string and a result display. `=` / `Enter` evaluate the
  expression via `lib/calc.ts` (`evaluate`). `CalcError` (malformed input, division by zero)
  is caught and shown as a friendly inline message inside an `aria-live` / `role="alert"`
  region — never a crash.
- Button grid: digits `0–9`, `.`, operators `+ − × ÷ ^`, parentheses, `%` (÷100), `±`
  (wrap/unwrap unary minus), `=`, `C` (clear), `⌫` (backspace).
- Full keyboard support, scoped to the focusable panel root (`role="application"`): digits and
  `+ - * / ^ ( ) .` append; `Enter`/`=` evaluate; `Esc` clears; `Backspace` deletes; `%`
  applies percent. The panel autofocuses on mount.
- Session history (component state only, no persistence): each `=` records `expression = result`;
  clicking an entry reloads its expression; a Clear button empties the list.

## Key decisions

- **Display tokens vs. raw operators.** Buttons show `× ÷ −` but insert `* / -` so the string
  fed to `evaluate` is plain ASCII the parser understands.
- **`±` semantics.** Wraps the whole current expression as `-( … )`. It only *unwraps* when the
  expression is a single balanced `-( … )` group — i.e. the leading `(` matches the final `)`
  (checked by the module-scope `isFullyNegatedGroup` helper, which scans paren depth). For a
  compound expression like `-(1)+(2)`, where the leading `(` closes early, it re-wraps to
  `-(-(1)+(2))` rather than mis-stripping to `1)+(2`. Button-produced `-(expr)` still round-trips.
- **`%` semantics.** Treated as "divide the current expression by 100" (`( … )/100`), the
  common study-calculator meaning.
- **No probability/parse logic here.** All evaluation lives in `lib/calc.ts`; this component is
  purely presentation + input handling.
- **`text-base` on the `=` key** intentionally uses the dark `base` color token as the text
  color (dark text on the green `accent` button) for contrast — it is a color, not a font size.

## Accessibility

Real `<button>` elements; `aria-label`s on symbol-only keys (`÷`, `×`, `±`, `⌫`, `(`, `)`,
`%`, `=`); visible `focus-visible` rings; results announced via `aria-live="polite"`; errors
via `role="alert"`. Press-scale animation respects `prefers-reduced-motion`.
