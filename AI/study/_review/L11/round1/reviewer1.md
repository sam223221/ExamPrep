# L11 Regression — Round 1 Review (Reviewer #1, Concept Completeness incl. Figures)

## Report to PM

**Assignment recap:** Concept-completeness review (Reviewer #1) of `study/lectures/L11-Regression.md` against `Lecture11-Regression.pdf` (49 slides) and `study/extracted_figures/L11/figures.md`. Brief acknowledged that L11 is slim on classical diagnostics — I checked that the chapter honestly flags what is missing from slides and points to ML Lab 2.

**Status:** Pass with concerns

Overall the chapter is unusually thorough: every numeric example from the slides is reproduced and arithmetically expanded, every USE-rated figure is embedded at the right pedagogical moment, every REWORK/SKIP rating in `figures.md` is honoured, and the things slides do not cover (gradient descent, MSE/RMSE, polynomial regression, regularisation, train/test) are flagged in §1, §3.13, §4.2 and §7 with explicit forward-references to ML Lab 2. The skeleton (Overview → Analogies → Core Concepts → Algorithms → Worked Examples → Pitfalls → Connections → Cheat-Sheet) is the right one and is fully populated.

That said, there are real conceptual gaps and a few outright errors that need fixing before this becomes a publishable exam study guide. Most are P2, but two are P1 inaccuracies that risk teaching the student something wrong about R-squared and about the variability decomposition.

---

### P0 findings

None. No factual error rises to "broken material" — the chapter is safe to study from for the bulk of the exam questions a student will actually face.

---

### P1 findings

1. **`L11-Regression.md:185-188` — claim that "R² always lies in [0,1] for OLS on training data" is overconfident and slightly wrong.**
   The chapter says `R^2 \in [0,1]` flatly. This is only guaranteed when the model contains an intercept and is fit by OLS on the training set. Strictly, on a held-out test set (or for a model without intercept) R² *can* go negative — the model can do worse than predicting `ȳ`. Since §4.2 and §7 themselves point the student at ML Lab 2 (which evaluates R² on a **test** set), the student will hit a negative R² in the lab and the chapter will have under-prepared them. Suggested fix: add a one-sentence footnote — "On a held-out test set or for an intercept-free fit, R² can drop below 0; the [0, 1] guarantee is a training-set-plus-intercept fact."

2. **`L11-Regression.md:171-178` — SSR identity `SSR = Σ(ŷ_i − ȳ)²` is asserted but the equality `SST = SSR + SSE` is not proved or even motivated.**
   The chapter states SST = SSR + SSE as fact and then immediately uses it. The slides do the same (slide 15 just declares `SSR = SST − SSE`), but a study guide is supposed to repair gaps the slides leave. The identity only holds because the OLS residuals are orthogonal to the centered fitted values (`Σ r_i (ŷ_i − ȳ) = 0`). Without at least one line of motivation, the reader is left thinking SSR is *defined* as `SST − SSE` (which §3.5 does) **and** as `Σ(ŷ_i − ȳ)²` (which §3.5 also does), with no explanation of why these two definitions coincide. Suggested fix: add one sentence pointing out that this is a consequence of OLS's first-order conditions, and that the identity would fail for, e.g., least-absolute-deviation regression.

3. **`L11-Regression.md:188-189` — Adjusted-R² formula not derived; sign convention on `p` is buried and ambiguous.**
   The chapter gives `R²_adj = 1 − (n−1)/(n−p−1) · (1 − R²)` and says `p` is "the number of predictors." It does *not* say whether the intercept counts. Convention: in this formula `p` excludes the intercept; `n − p − 1` is the residual degrees of freedom. The slides do not state the formula at all, so a student who only reads the chapter will not be able to reproduce R²_adj = 0.2142 from the table. Suggested fix: add the explicit residual-d.f. convention and verify on Model 1 (`n = 25, p = 1` → `R²_adj = 1 − 24/23 · 0.7531 = 0.2138 ≈ 0.2142` ✓).

4. **`L11-Regression.md:226-242` — p-value definition is technically wrong as stated.**
   Section 3.8 quotes the slide ("the probability that, given the current information, a particular predictor has no relationship with the response") and then attempts to correct it ("the probability of observing a coefficient at least as extreme as the one estimated, assuming the true coefficient were zero"). The second statement is the *correct* frequentist definition; the first is the classical inversion fallacy and should be explicitly called out as **wrong**. The chapter currently reads as if both statements are interchangeable. A student parroting the first statement on the exam would be marked down by a strict examiner. Suggested fix: insert an explicit "the slide phrasing is technically the inverse and is a known textbook misstatement; here is what p-value really means."

5. **`L11-Regression.md:252-261` — "approximately ±2·SE" rule of thumb glosses degrees of freedom.**
   For the soft-drink regression `n = 25, p = 1`, residual d.f. = 23, and the 97.5% t-quantile is 2.069, not 1.96. The chapter's parenthetical "strictly closer to 1.96 for large samples" goes the wrong direction — for *small* samples the multiplier is *bigger*, not smaller, than 2. The bathroom example has `n = 128, p = 7` (residual d.f. = 120) so 1.98 is fine there, but the housekeeping note in §3.9 misleads students about which direction the correction goes. Suggested fix: rewrite as "1.96 in the large-sample limit; >2 for small samples; for n = 25 with one predictor, the actual multiplier is 2.069."

6. **`L11-Regression.md:296-297` — slope flipping with collinearity is asserted but the §5.5 example never demonstrates it.**
   The chapter promises that multicollinearity makes coefficients "flip sign or balloon in magnitude" (analogy, §2; pitfall #8, §6; §5.5 intro). But §5.5 is one paragraph long: it says "individual coefficients can flip sign, balloon, or become statistically insignificant" without showing a single before/after coefficient. The slides do not show this either (slide 48 just shows the correlation table), so this is a slide-gap the chapter should fill but does not. Suggested fix: add a worked one-paragraph synthetic example or explicitly mark §5.5 as "no worked numbers in slides — see ML Lab 2 if available."

7. **Missing concept: Galton's "regression to the mean".**
   Figure 11 (Galton book cover, page 9 of the PDF) is correctly SKIP-rated in `figures.md`, but `figures.md`'s rationale ("Lecture uses it as a one-frame historical aside (Galton coined 'regression toward mediocrity'). Pure context decoration; no formula or data.") implies the lecturer at least name-drops the historical origin. The chapter mentions Galton zero times. This is the etymology of the word "regression" and frequently appears in exam-style "what does the name mean?" questions. Suggested fix: one sentence in §3.1 or §1 — "The word 'regression' itself comes from Galton's 1886 observation that tall fathers' sons regress toward the mean height, even though Galton's biological claim has nothing to do with the modern OLS we are about to derive."

8. **Missing concept: F-statistic / overall-model test.**
   §5.1's table reports the F-statistic p-value = 0.01151 as "Overall the model is significantly better than predicting `ȳ`," and pitfall #11 (§6) mentions the F-statistic, but there is no §3 sub-section explaining what F actually is. The slides do not explain F either — but figure 18 displays it prominently and any student reading R output for the first time will ask "what is `F-statistic: 7.54 on 1 and 23 DF`?". Suggested fix: a short §3.8.1 or footnote: "F is the ratio of explained variance to unexplained variance scaled by degrees of freedom; it tests the null that *all* slopes are zero simultaneously. For one predictor, the F-test is equivalent to the t-test on that single slope (F = t²)."

9. **Missing concept: linearity-in-parameters vs linearity-in-inputs.**
   §3.13 and pitfall #9 (§6) both wave at the distinction ("interaction terms keep the model linear in parameters", "polynomial features keep linearity-in-parameters while breaking linearity in the inputs"), but neither formally defines what "linear in parameters" means. A student who has not seen this phrase before will not understand why `y = a + b·x²` is still a "linear regression". Suggested fix: a one-paragraph definition the first time the phrase appears, stating that "linear in parameters" means the model is a linear combination of fixed feature functions of the inputs, and that this is the technical reason OLS still works for polynomial / interaction / dummy expansions.

---

### P2 findings

1. **`L11-Regression.md:5` — glossary list is incomplete vs the body.** Body uses "design matrix" (§4.1), "normal equations" (§4.1), "baseline" (§3.10, §6 pitfall #5), "F-statistic" (§5.1 table, §6 pitfall #11), and "extrapolation" (§3.4, §6 pitfall #7), but the §1 glossary line does not list any of these. Either add them or drop the glossary header's claim of completeness.

2. **`L11-Regression.md:75` — figure 9 caption.** The caption ("A scatter of (x, y) pairs and a fitted line. Regression is the procedure that turns the scatter into the line.") describes what the figure *contains* but does not say why the lecture chose this particular cartoon (axis range −20 to 60, large noise). It is fine, just generic.

3. **`L11-Regression.md:122-123` — figure 12 caption.** The caption describes the figure but does not state that the dashed segment in fig12 is the *signed* residual (the slide labels just say "Residual"). Since §3.3 immediately states residuals are signed (line 120), the caption could reinforce this.

4. **`L11-Regression.md:176-177` — figure 15 caption is good but could explicitly state the colour code.** The top panel arrows are deviations from `ȳ`; the bottom panel has black arrows (y − ȳ) and red arrows (y − ŷ). The caption mentions arrows but not which colour corresponds to which decomposition; a colour-blind reader is left guessing.

5. **`L11-Regression.md:215-219` — small table comparing Model 1 / Model 2 has no n.** The table reports R² and Adjusted R² but not n (= 25 for both). A student trying to verify adjusted-R² by hand needs n.

6. **`L11-Regression.md:419-426` — soft-drink "Step 3 — Interpret" table reads `Intercept p-value | 0.0768 | Not quite significant at the 5% level.`** This is correct, but the slide marks the intercept p-value with a `.` (which means `p < 0.1`). The chapter doesn't mention that the intercept *is* flagged in the R output. A pedantic exam answer would say "borderline significant at the 10% level."

7. **`L11-Regression.md:587-588` — Model B Adjusted R² = 0.4359.** This is reported in §5.4's summary table but does not match the body, which in line 532-534 quotes only `R^2 = 0.4413` and does not give Adjusted R². The figure 29 OCR shows Adjusted R² = 0.4359; the chapter is internally consistent because the summary table on line 587 captures it. Just worth double-checking that the in-section text matches the summary table everywhere.

8. **`L11-Regression.md:631-645` — Connections § cross-refs L05, L09a, L10, ML-Lab-2 but not L12 (clustering) despite "Compare against L12's unsupervised clustering, which has no target y" being asserted in line 635.** If L12 exists in the course, link it; if it doesn't, drop the reference.

9. **`L11-Regression.md:686-689` — exam-day formula sheet does not include the closed-form OLS solution `b̂ = Σ(x−x̄)(y−ȳ)/Σ(x−x̄)²`.** The chapter explicitly states (§3.3, line 133–134) that the slides do not show this but provides it in the body. If a student is reading only the cheat-sheet on exam day, they cannot reproduce the slope from raw data.

10. **`L11-Regression.md:692-702` — "Reading R output" table is excellent but doesn't say what `Residuals: Min 1Q Median 3Q Max` is for.** Every R `lm()` output displays a residual five-number summary above the coefficient table (visible in figures 18, 19, 21, 28, 29, 32). Since the chapter teaches reading R output, the five-number summary deserves a row in the cheat-sheet table.

11. **Figure 14, 16, 17, 20, 27, 31 are listed as REWORK with LaTeX re-typesetting.** The chapter does typeset these in LaTeX, but `figures.md` line 26 says fig14 is "Listed here for completeness; SKIP in chapter," while in fact the equation `Sales = 51.849 + 7.527 × Advertising` *is* rendered in §3.4 (line 142) and §5.1 (line 410) inline, plus it is shown via the embedded fig13 caption. That is technically consistent with "REWORK / re-typeset" but the wording in figures.md is muddled. Cosmetic, not chapter-content.

12. **§3.10 doesn't explain how R encodes multi-level categoricals by default.** The lecture only uses binary Gender, but the dummy-variable trap discussion (line 277) says "for a categorical with k levels, add k−1 dummies." A student wondering "what does R do with Neighborhood {East, North, West}?" (visible in figure 21 as `NeighborhoodNorth` and `NeighborhoodWest`, with East as the absorbed baseline) gets no explanation — yet the worked figure in front of them shows exactly this. One sentence in §3.10 pointing at fig21 as a 3-level example would close the loop.

13. **No mention of residual plots / regression-assumption diagnostics.** The slides explicitly do *not* cover residual-vs-fitted plots, Q-Q plots, heteroscedasticity, autocorrelation, or normality of residuals — which is fair, the slides are slim. The chapter mirrors that omission. Since the brief says "L11 is slim on classical regression diagnostics — chapter should honestly flag what's missing from slides and point to ML Lab 2," this is partially handled in §1 ("What L11 does not cover") **but residual diagnostics are not on the list there.** Add a bullet to §1's "does not cover" list: "No residual-plot diagnostics (residual-vs-fitted, Q-Q, leverage, Cook's distance); the Gauss-Markov assumptions (linearity, independence, homoscedasticity, normality of residuals) are not stated. ML Lab 2 may or may not introduce them depending on variant."

14. **No mention of standardised/beta coefficients.** The slides do not cover this; the chapter follows. Worth a single sentence in §3.4 — "raw slope is in *units of y per unit of x*; if x and y are on incomparable scales (advertising in $1000s vs income in $10,000s), some textbooks report standardised coefficients (z-scored beta) to make magnitudes comparable. Not covered in L11."

15. **The "passengers' fuss" analogy (§2 line 49) is cute but never returns in §3.6.** The analogy is recalled at line 197, but a student reading §3.6 in isolation hits R² with no analogy in arm's reach. Already a wash — fine as is.

16. **`L11-Regression.md:705-707` — closing citation reads "Lecture 11 slides 1–48"** but the PDF has 49 slides (slide 49 is the "Thanks for your attention" card). Pedantic but the figures.md inventory says 49 slides total.

---

### QA Checklist (§7) status

The brief did not provide an explicit §7 QA checklist for a study-guide chapter, so I reused the implicit checklist for chapter completeness:

| Item | Status | Note |
|---|---|---|
| All §1 scope items (every concept that L11 explicitly teaches) covered in §3? | Pass | Linear regression simple + multiple ✓, OLS ✓, intercept/slope interpretation ✓, SST/SSE/SSR decomposition ✓, R² ✓, Adjusted R² ✓, p-value ✓, CI ✓, dummies ✓, interactions ✓, multicollinearity ✓, linearity-as-approximation ✓. |
| Every USE-rated figure embedded? | Pass | All 22 USE figures (fig04, 05, 08, 09, 10, 12, 13, 15, 18, 19, 21, 23, 24, 25, 26, 28, 29, 30, 32, 33, 34, 35, 36) appear in chapter at the right section. |
| Every REWORK figure handled (paraphrased or re-typeset)? | Pass | fig10 has prose paraphrase + embedded raster; fig14, 16, 17, 20, 27, 31 re-typeset in LaTeX. |
| Every SKIP figure justified? | Pass | All 7 SKIPs justified in `figures.md`; no decorative junk leaks into the chapter. |
| Honestly flags what slides do NOT cover? | Pass | §1, §3.13, §4.2 and §7 all forward-reference ML Lab 2 for gradient descent, MSE/RMSE, polynomial features, regularisation, train/test. **Concern: residual-plot diagnostics not in the "does not cover" list — see P2 #13.** |
| Every numeric example from slides reproduced with arithmetic? | Pass | Soft-drink simple (§5.1), soft-drink + income (§5.2), bathroom CI (§5.3), salary Models A/B/C (§5.4), sales-vs-assets (§5.5). Arithmetic for CI ($3,649 ↔ $12,117), male-specific equation $58,299 + $2,752.9×Exp, prediction $127,119 — all checked. |
| Analogies in §2 referenced again in §3? | Pass | Flight-path (§3.2 line 110, §3.3 line 129), passengers' fuss (§3.6 line 197), fake universe (§3.8 line 240), repeated sampling (§3.9 line 263), yes/no flag (§3.10 line 279), slope-depends-on-group (§3.11 line 295), two passports (§3.12 line 322) — all recalled. |
| §6 pitfalls list covers exam traps? | Pass | 12 pitfalls; the practical-vs-statistical-significance trap is repeated three times across the chapter which is the right amount for an exam guide. |
| Cross-references to other lectures (L10, L05, L09a, ML-Lab-2) present? | Pass | §7 lists them; format matches sibling chapters (I did not cross-check against e.g. L10-Intro-to-ML.md). |
| Cheat-sheet (§8) is self-contained? | Mostly | Missing closed-form OLS slope formula (P2 #9) and residual-summary row in the R-output table (P2 #10). |

### Acceptance criteria (§1) status

The chapter's own §1 is the implicit acceptance criterion. The "What L11 does cover" list (lines 18–24) and "What L11 does not cover" list (lines 27–31) are the checklist. Every "does cover" bullet is met. Every "does not cover" bullet is correctly flagged with a forward-reference. **One gap:** residual-plot diagnostics / Gauss-Markov assumptions are neither covered nor listed in "does not cover" — see P2 #13.

### DOCUMENT.md audit

N/A for a Markdown study chapter — no DOCUMENT.md was expected and none is required in the `study/lectures/` directory per the workflow.

### Out-of-scope observations

1. **`figures.md` line 26** ("Listed here for completeness; SKIP in chapter") contradicts itself for fig14: the equation IS rendered (just as LaTeX, not as a raster). REWORK is the right verdict; the rationale text should say "embedded as LaTeX, not as raster," not "SKIP." See P2 #11.
2. **`figures.md` does not list a verdict for the "Thanks for your attention" slide 49** because PyMuPDF presumably extracted no embedded image from it (slide 49 is just text). The PDF has 49 pages but figures.md says "49 slides total" and "Total: 36 (matches PDF inventory)" — these two numbers refer to different things (slides vs extracted images). Cosmetic.
3. **The chapter cites Serkan Ayvaz** (line 707) as the lecturer; the PDF title slide confirms this. Good.
4. **The L09a cross-reference (line 639)** to "Bayesian Networks (probabilistic framing of regression)" is technically correct but a stretch — L09a may not actually frame regression Bayesianly. Worth a sanity-check by Reviewer #2.
5. **Two parallel analogies in §2 use airline imagery** (flight-path × 4) — this is the chapter's strongest pedagogical move and should be preserved through any rewrite.

### Concerns / risks

- The chapter is **long** (~50 min reading time per its own §1) for what the slides actually cover. The brief said "lecture is slim on classical diagnostics" — the chapter compensates by going deep on analogies and worked arithmetic, which is correct. But the §3 → §5 sequence repeats the same R-output reading three times (figs 18, 19, 21, 28, 29, 32). Not a defect, just dense.
- The "OLS deliberately bends toward outliers to keep their big squared distances down" (line 47) is good intuition but a careful reader may object: OLS bends *less* than the outlier wants — it splits the difference. The current wording is defensible but could be tightened.
- §3.7 says "Adjusted R² can decrease when a useless predictor is added, which is exactly the safety property we want." This is correct but doesn't note that adjusted R² *can also increase* when a useful predictor is added — i.e., the direction of change is informative about whether the new variable carries real signal. Minor.

### What PM should do next

Have `pm-frontend` (or whoever wrote the chapter) fix the **P1 list** before the Round-2 review. In particular:
- P1 #1 (R² range correctness)
- P1 #4 (p-value definition)
- P1 #5 (t-multiplier direction)
- P1 #7 (Galton)
- P1 #8 (F-statistic)
- P1 #9 (linear-in-parameters definition)

The remaining P1s (#2 SSR identity, #3 R²_adj derivation, #6 multicollinearity demo) are improvements rather than corrections — defer to Round 2 if time-boxed.

P2 fixes are quality polish; queue for a final pass, do not block reviewer #2 / #3.

After fixes, dispatch Reviewer #2 (typically Voice / Pedagogy) for Round 1, then re-QA on the corrected chapter.

**DOCUMENT.md updated:** N/A for QA
