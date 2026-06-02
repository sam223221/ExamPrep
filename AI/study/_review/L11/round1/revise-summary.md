# L11 Regression — Round 1 Revision Summary

**Revised by:** Reviser for L11, round 1
**File revised:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L11-Regression.md`
**Reports addressed:** `reviewer1.md`, `reviewer2.md`, `reviewer3.md`, `reviewer4.md`
**No P0 findings;** all targeted P1 fixes implemented. P2 polish addressed where it directly improves exam readiness or removes contradictions; remaining P2 polish deferred to round 2 unless it overlaps with a P1 fix.

---

## Fixes applied, mapped to reviewer findings

### Reviewer #1 P1 fixes

| Finding | Action |
|---|---|
| **R1-P1#1** R² range over-stated as `[0,1]` flatly | §3.6 rewritten to gate the bound to "OLS with intercept on training data," explicitly states $R^2$ can be negative on a held-out test set or no-intercept fit. Cheat-sheet §8 updated to match. Added a new pitfall (§6 #15). |
| **R1-P1#2** SSR identity asserted with no justification | §3.5 now boxes $\text{SSR} = \sum_i (\hat y_i - \bar y)^2$ as a numbered equation and adds a paragraph explaining the cross-term vanishes *because of OLS + intercept*. Flagged that the identity would fail for least-absolute-deviation regression or no-intercept fits. |
| **R1-P1#3** Adjusted R² formula provenance / sign convention on `p` ambiguous | §3.7 now (a) names "$p$ excludes the intercept; residual d.f. $= n - p - 1$"; (b) sanity-checks the formula on both Models 1 and 2 from the soft-drink example; (c) explicitly flags "EXTENSION — not on the slides"; (d) adds an intuition paragraph for *why* the $(n-1)/(n-p-1)$ multiplier is the right penalty. |
| **R1-P1#4** p-value definition: chapter quotes slide's classical inversion fallacy as authoritative | §3.8 now flags slide 19's phrasing as the **classical "inverse" misstatement** ($P(\text{data}\|H_0)$ vs $P(H_0\|\text{data})$) and demotes it to a quoted-but-incorrect example, then leads with the correct frequentist definition (with explicit formula $p_j = \Pr(\|T\| \ge \|t_j\| \mid H_0)$). New §6 pitfall (#14) reinforces. |
| **R1-P1#5** t-multiplier direction: chapter said "strictly closer to 1.96 for large samples" — was wrong on direction | §3.9 rewritten: shows the multiplier is *always at least 1.96, never smaller*, and explicitly tabulates 2.069 for n=25/p=1, 1.980 for n=128/p=7, 1.96 as the large-n limit. Cheat-sheet now writes the CI with the t-quantile explicitly. Pitfall reinforced via R-output cheat-sheet table. |
| **R1-P1#7** Galton "regression to the mean" etymology missing | §3.1 now contains a paragraph naming Galton, his 1889 *Natural Inheritance*, the biological "regression toward mediocrity," and that the modern OLS just inherited the word. Flagged as exam-style "etymology" answer. |
| **R1-P1#8** F-statistic prominent in figures but never defined | New §3.8.1 sub-section: defines $F = (\text{SSR}/p) / (\text{SSE}/(n-p-1))$, states null = "every slope is zero," contrasts with per-coefficient t-tests, shows the $F = t^2$ special case for one predictor (with arithmetic check $2.746^2 \approx 7.54$ for soft-drink). Cheat-sheet and R-output table also updated. |
| **R1-P1#9** "Linear in parameters" used but never defined | New blockquote in §3.13 defines linear-in-parameters formally, contrasts with non-linear-in-parameters (gives $y = \beta_0 \exp(\beta_1 x)$ as the contrast), explains why dummies/interactions/polynomials all still count as "linear regression." Cheat-sheet updated. |

R1-P1#6 (multicollinearity sign-flip demo) was flagged by R1 as defer-to-Round-2; left as-is for this round.

### Reviewer #2 P1 fixes

| Finding | Action |
|---|---|
| **R2-P1#1** Unit-of-Advertising contradiction (chapter declares \$ thousands, then interprets slope per \$1) | §5.1 setup rewritten to lock units explicitly: "Advertising in \$ thousands (so 9.5 = \$9,500); Sales in thousands of units (so 145.1 = 145,100 units)." §3.4 interpretation rewritten to say "one extra unit (= \$1,000) of Advertising → ~7,527 extra units of Sales on average" while preserving the slide-loose-equivalent "per \$1 of ad spend buys ~7.527 units." Interpret-table in §5.1 fully reconciled. New §6 pitfall (#16) on units. |
| **R2-P1#2** SSR = Σ(ŷ−ȳ)² noted "Equivalently" with no caveat | Same fix as R1-P1#2 above. |
| **R2-P1#3** Slide p-value definition left as if authoritative | Same fix as R1-P1#4 above. |
| **R2-P1#4** $R^2 \in [0,1]$ caveat is "slippery" | Same fix as R1-P1#1 above. |
| **R2-P1#5** Adjusted R² formula chapter-added — flag as extension | Same fix as R1-P1#3 above; explicit "EXTENSION — not on the slides" call-out added. |
| **R2-P1#6** Bathroom CI upper bound disagrees with slide by 0.002 | §3.9 now adds a clarifying sentence: "Slide 21 prints the upper bound as \$12,117.35; the precise arithmetic above gives \$12,117.348 — a rounding difference, not a discrepancy." |
| **R2-P1#7** Sample size n=25 inferred but not flagged | §5.1 setup now says: "(the slide displays only nine rows, but n=25 is inferred from the 23 residual degrees of freedom line of the lm output in figure 18: n−p−1=23 with p=1 gives n=25)." |

### Reviewer #3 P1 fixes (analogy quality)

| Finding | Action |
|---|---|
| **R3-P1#1** §2 bullet 4 "passengers' fuss" undefined | Bullet 4 rewritten to drop "fuss" entirely. New image: **shotgun blast on a target** (concrete spread image). SST = total spread; SSR = part the line absorbed; SSE = leftover. The §3.6 callback updated to "shotgun-spread analogy" to match. |
| **R3-P1#2** §2 bullet 5 "mirage" inverts p-value meaning | Bullet 5 rewritten: headline image is now **"random noise dressed up to look like a real signal"** (does not invert). Added explicit "Avoid the inverted reading: a small p-value does *not* mean the effect is an illusion." |
| **R3-P1#3** §2 bullet 2 sign collision: "well to the south = negative" contradicts $r_i = y_i - \hat y_i$ | Bullet 2 rewritten to drop geographic compass language entirely. Now: "above the line ($y_i > \hat y_i$) → positive residual; below the line → negative residual," with explicit reminder "Forget compass directions; the sign is determined by the chart's y-axis, not by geography." |
| **R3-P1#4** §2 bullets 6/7/8 (CI, dummy, interaction) contain no real analogies | All three rewritten with concrete imagery: CI = **dart-throw target ring** around the true slope; dummy = **light switch wired to a fixed bonus**; interaction = **throttle on the slope** (dummy decides if the throttle is engaged, interaction coefficient is the extra rise-per-year). The §3.9/§3.10/§3.11 callbacks updated to use the new names ("dart-throw," "light-switch," "throttle"). |

R3-P1 #4 (worked SST/SSE/SSR numbers), #5 (extrapolation callout), #6 (adjusted-R² why-the-penalty) — items #5 and #6 partially addressed via the new §3.7 intuition paragraph and the boxed extrapolation warning in §3.4. #4 (3-row toy SST/SSE/SSR calculation) deferred to Round 2 as a P2.

### Reviewer #4 P1 fixes

| Finding | Action |
|---|---|
| **R4-C-1** Adjusted R² formula provenance ambiguous | Same fix as R1-P1#3 / R2-P1#5; explicit "EXTENSION — not on the slides" call-out, plus per-model arithmetic check. |
| **R4-C-2** Model C "a touch lower" misrepresents 12% gap | §5.4 Important-read paragraph rewritten: explicitly quantifies "-\$8,034 / \$66,334 ≈ -12%" as "**not** a small 'touch,'" solves the crossover algebraically ($E \approx 3.85$ years), describes the trajectory honestly. |
| **R4-C-3** SSR = Σ(ŷ−ȳ)² buried in parenthetical | §3.5 now promotes the formula to a numbered boxed equation with a why-it's-true paragraph (same fix as R1-P1#2). |
| **R4-C-4** F-statistic missing | New §3.8.1 (same fix as R1-P1#8). |
| **R4-C-5** Degrees of freedom never defined | §4.1 now opens with a "Quick definition — degrees of freedom" blockquote: $n - p - 1$, why it matters, how it appears in R output (Residual std error, F-statistic). |
| **R4-M-1** p-value: slide-19 phrasing quoted without flag | Same fix as R1-P1#4. |
| **R4-M-2** CI conflates t-quantile and z-quantile | §3.9 rewritten (same as R1-P1#5): explicitly names 1.96 as the **standard-normal** quantile and 2.069 / 1.980 as exact **t-quantiles** for the two sample sizes used in the lecture. Cheat-sheet now writes CI with $t^*_{0.975, n-p-1}$ and the "≈ 2" approximation as the secondary form. |
| **R4-M-3** §8 cheat-sheet "$R^2 \in [0,1]$" contradicts §3.6 caveat | Cheat-sheet §8 R²-line rewritten to match §3.6: "Bounded $\in [0,1]$ for OLS with intercept on training data; **can be negative** on a held-out test set or for a no-intercept fit." Consistent across §3.6, §6 pitfall #15, and §8. |
| **R4-M-5** Units of Sales/Advertising never clarified | §5.1 setup and §3.4 interpret both rewritten (same fix as R2-P1#1). Pitfall #16 added. |
| **R4-M-4** Dummy trap "model cannot be estimated" not tied to $X^\top X$ singularity | §3.10 rewritten: "the sum of all k dummy columns equals the intercept column of 1s … design matrix rank deficient by 1 … $X^\top X$ singular and non-invertible." Plus a worked 3-level example (Neighborhood: East / North / West with East as baseline) using fig21. |
| **R4-M-6** House-price example response variable never named | §5.3 now says explicitly: "**Price (in US dollars)** as the response variable and seven predictors: SqFt … (East as baseline)." Also explicitly notes the 3-level Neighborhood encoding. |
| **R4-M-7** Intercept p-values flagged but never marked uninteresting | §3.8 now ends with a paragraph: "R prints a p-value for the intercept too, but it tests the unhelpful null 'is the intercept exactly zero?' … Don't use intercept p-values for variable selection." Soft-drink interpret-table updated to reflect this. New §6 pitfall #13. |

Additionally, the §3.11 throttle analogy now reproduces the **slide 28 plausible business examples** of interaction terms (Salary×Location, Price×Channel, Education×Gender), which R4 flagged as missed slide content.

---

## Cheat-sheet (§8) overhaul

The §8 cheat-sheet was substantially expanded to address:
- R1-P2#9: closed-form OLS slope formula added.
- R1-P2#10: `Residuals: Min 1Q Median 3Q Max` row added to the R-output table.
- R4-m-7/R4-m-8: $k - 1$ dummy rule added.
- F-statistic formula and a dedicated row in the R-output table.
- The "Adjusted R² (EXTENSION)" flag.
- The corrected CI formula with the t-quantile spelled out.

---

## Items deliberately deferred to Round 2 (not addressed this revision)

- R1-P1#6 (worked sign-flip example for multicollinearity — explicitly defer-by-R1)
- R1-P2#1 (glossary list completeness — design matrix, normal equations, baseline, etc.)
- R1-P2#3/#4 (figure-caption polish around colour codes — partially addressed for fig36)
- R1-P2#5 (Model 1/2 table missing $n = 25$ — addressed in §3.7 table)
- R3-P1#4 (3-row toy SST/SSE/SSR calculation)
- R3-P2#7 (§2's "read this section first" tension with §1 ordering)
- R3-P2#10 (Model C interpretation density — partially addressed via the explicit "12% lower" / crossover-at-E≈3.85 rewrite)
- R4-m-2 (consistency of "no matrix form" claim with §3.3 closed-form derivation — left as-is; the chapter explicitly flags the closed form as a chapter extension)

These are all polish-level and do not affect the chapter's correctness or exam-readiness.

---

## Verification spot-checks (post-revision)

- All numeric values from R2's audit table are unchanged.
- New arithmetic in §5.4 (`-8034 / 66334 ≈ -12%`, crossover $E \approx 3.85$ years from $8034.3 / 2086.2 = 3.852$) verified by hand.
- New §3.7 sanity-check on Adjusted R² ($n = 25$, $p = 1$, $R^2 = 0.2469 \Rightarrow R^2_{\text{adj}} = 0.2141$ rounding to slide-printed 0.2142) verified.
- New §3.8.1 $F = t^2$ for one predictor ($2.746^2 = 7.541 \approx 7.54$) verified.
- All analogy callbacks in §3 updated to match the renamed §2 analogies (shotgun-spread, dart-throw, light-switch, throttle).

## Status

**Ready for round 2 review.** No P0 introduced. All targeted P1 fixes implemented; P2 polish addressed where it overlaps with P1 fixes or removes contradictions. Chapter remains internally consistent across §2 (analogies), §3 (formal), §5 (worked examples), §6 (pitfalls), and §8 (cheat-sheet).
