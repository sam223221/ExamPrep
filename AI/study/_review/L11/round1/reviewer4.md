# L11 Regression — Round 1 — Reviewer #4 (Exam Readiness)

**Reviewer mandate:** Spec §7.1 — judge whether a student who studies *only* this chapter (no slides) can ace any reasonable exam question about Lecture 11. Be harsh. Compare line-by-line against the PDF.

**Verdict:** **PASS WITH MAJOR CONCERNS.** Conceptually rich, well-analogised, and structurally complete — but several exam-grade weaknesses remain that will cost marks on at least three predictable question types.

---

## 1. Source-fidelity audit (chapter vs PDF)

I read every PDF slide (1–49) and cross-checked against the chapter. Findings, in order of severity:

### CRITICAL (will lose marks on the exam)

**C-1. Adjusted R² formula is uncited and the slide value is misrepresented.**
- Chapter §3.7 presents the formula $R^2_{\text{adj}} = 1 - \frac{n-1}{n-p-1}(1-R^2)$ as "useful to know for variant questions" — but the slides do **not** contain that formula. If the exam writer is strict about "only what was in the lecture," a student reciting this formula could be marked wrong for over-claim. More importantly: the chapter says "The lecture states the property but does not give the formula" — true — but then says the formula is "useful to know." The student has no way to tell whether it is *examinable* or not. The flag is too soft. Mark it explicitly: **NOT IN THE SLIDES — KNOW THE BEHAVIOUR, NOT THE FORMULA.**
- Slide 38 Adjusted R² = **0.4359**, not 0.4413. Chapter §5.4 Model B summary table (line 587) reports "Adjusted R² 0.4359" correctly, but the running prose around line 546 says "$R^2 = 0.4413$ — up from 12%" without naming whether that is raw or adjusted. The reader has to infer. Same ambiguity in §5.4 Model C ("$R^2 = 0.5561$") — fine because raw, but adjusted-vs-raw is the entire point of §3.7 and the chapter blurs it in the very example meant to teach it.

**C-2. Model C interpretation is wrong about where the lines cross.**
- Chapter §5.4 line 572: *"the lines cross somewhere early in a career and then diverge."* Solve $66{,}333.6 + 666.7 E = 58{,}299.3 + 2{,}752.9 E$ → $8{,}034.3 = 2{,}086.2 E$ → $E \approx 3.85$ years. OK that is "early in a career." Fine.
- But then line 579 says: *"the male coefficient is **\$−8,034** (males start a touch lower!)"* and *"at zero experience men actually start a bit lower, but they accelerate faster."* "A touch lower" is misleading — \$8,034 on a \$66,334 base is **12% lower**. That is not a touch; it is a meaningful gap. The chapter's own figure 33 makes the lines clearly cross near $E \approx 4$. Tighten the language.

**C-3. The chapter never states the formula $\text{SSR} = \sum_i (\hat y_i - \bar y)^2$ except in passing.**
- §3.5 line 174 says "Equivalently, $\text{SSR} = \sum_i (\hat y_i - \bar y)^2$" — buried as a parenthetical. The slides give only $\text{SSR} = \text{SST} - \text{SSE}$ (slide 15). For an exam question "write SSR as a single sum," the chapter buries the answer. Promote it to a numbered formula block.

**C-4. F-statistic is mentioned three times but never explained.**
- Chapter line 426: "F-statistic p-value | 0.01151 | Overall the model is significantly better than predicting $\bar y$." Pitfall 11 (line 623) says: "the F-statistic tests the model as a whole." That is **all** the explanation. The slides do contain `F-statistic: 7.54 on 1 and 23 DF, p-value: 0.01151` (slide 16), so the F-statistic *is* lecture material. If the exam asks "what does the F-statistic test, and how is it different from the per-coefficient p-values?", the chapter gives the punchline but no scaffolding. Add a §3.8.1 micro-section (3–4 lines) covering: null = "all slopes are zero simultaneously", reject → at least one predictor matters, single test vs $p$ predictor-wise tests.

**C-5. Degrees of freedom appear in tables but are never defined.**
- "$n - p - 1$ degrees of freedom" shows up at line 700 in the R-output reading table, and "23 d.f." in §5.1 line 425. Nowhere does the chapter say what degrees of freedom mean in the regression context (number of observations minus number of estimated parameters). A student who has never seen R output before will not know whether 23 is meaningful. This is exam-cheap to fix — one sentence in §4.1.

### MAJOR (likely to lose marks under unfavourable phrasing)

**M-1. The "p-value definition" is the lecture's own loose phrasing — and the chapter inherits the looseness.**
- Slide 19: *"p-value measures the probability that, given the current information, a particular predictor has no relationship with the response."* This is, strictly, **wrong** (the correct definition is the probability of observing data at least as extreme as the data given the null), and the chapter quotes it verbatim at line 231 before silently correcting it at line 232. A careful exam grader who has Bayesian instincts will mark a student down for reciting slide 19 as truth. The chapter does correct the definition, but the **block quote** of the wrong version stays prominent. Recommend: keep the quote, but immediately label it as "the lecture's informal phrasing" rather than presenting it as a definition.

**M-2. "Confidence interval = $\hat b \pm 2 \cdot \text{SE}(\hat b)$" is presented as the formula, with the t-distribution buried.**
- §3.9 line 256: "The '2' is a rule-of-thumb approximation to the 97.5% quantile of the t-distribution — strictly closer to 1.96 for large samples."
- 1.96 is the **normal** quantile, not the t-quantile. For 23 d.f. the 97.5% t-quantile is 2.069; for 120 d.f. it is 1.98. The chapter conflates t and z. Exam-pedant graders will catch this. Either say "1.96 for the normal approximation; the exact t-quantile depends on d.f." or drop the parenthetical.

**M-3. R² interpretation lower bound is misstated.**
- §3.6 line 186: *"$R^2 = 0$: the model explains nothing — the regression line is no better than predicting $\bar y$ for every point."* For an OLS fit on training data this is fine, but for *test-set* or non-OLS $R^2$ (which the chapter explicitly says ML Lab 2 covers) $R^2$ can be **negative**. The chapter says "always lies in $[0,1]$ for OLS on training data" — good — but the §8 cheat-sheet at line 668 says *"$R^2 \in [0,1]$"* without the caveat. Exam Q: "Can $R^2$ be negative?" expects "Yes, on test data" — the chapter only really commits in §3.6 and forgets it in §8.

**M-4. The dummy-variable trap is asserted but not justified.**
- §3.10 line 277 says "the second column would be a perfect linear combination of the first — perfect multicollinearity (§3.12) and the model cannot be estimated." Good. But the slides (slide 34) merely state that the two columns "carry the identical information" with `Gender.Male = 1 − Gender.Female`. The chapter elevates this to "the model cannot be estimated" — true mathematically, but never tied to **why** ($X^\top X$ becomes singular and non-invertible). Since §1 line 31 explicitly says the chapter does NOT derive matrix form, the "cannot be estimated" claim is hanging. Either give one sentence on rank-deficiency or soften to "the software will drop one of the columns."

**M-5. Slide 6 hypothetical "Sales = $10,000 + 5 × Advertising" — chapter never resolves the unit mystery.**
- The hypothetical model on slide 6 has intercept \$10,000 and slope 5, while the fitted model on slide 11 has intercept 51.849 and slope 7.527 with **no dollar sign**. Slide 11 says "for every \$1 increase in advertising sales increase by \$7.527" — but the scatter axis shows Advertising in single digits (8.5–12). Either Sales is in thousands and Advertising is in thousands (then \$7.527 means \$7,527 of sales per \$1,000 ad spend) or units are inconsistent. The chapter inherits this confusion uncritically at line 142 and §5.1. Exam Q: "Predict sales when advertising = \$10,000" — student plugs in 10000, gets nonsense. Add an explicit unit footnote: "Advertising in \$1,000s, Sales in unit-thousands (per slide 5 axis labels)."

**M-6. House-price example: §6 of the Plan template demands acceptance criteria — the chapter does not say what other predictors are in the house regression and just throws the coefficient table at the reader.**
- §5.3 line 467 lists predictors as "SqFt, Bedrooms, Bathrooms, Offers, BrickYes, NeighborhoodNorth, NeighborhoodWest" but never tells the reader **what the response is** (price in dollars). Slide 20 also leaves this implicit. Exam Q: "What is the dependent variable in the house-price regression?" — answer "house price" — chapter never names it.

**M-7. F-statistic intercept p-value mention in §5.1 is wrong.**
- §5.1 line 421 says "Intercept p-value | 0.0768 | Not quite significant at the 5% level." OK — but the table presents this with the same status as the slope p-value. The intercept's p-value tests whether the intercept differs from zero — an **uninteresting** test for a sales model. The chapter does not flag this. Pitfall worth adding: "intercept p-values are almost never interesting and never used for variable selection."

### MINOR (cosmetic / would not flip a mark on its own)

**m-1.** §2 line 51 — "fake universe" analogy for p-value is good, but the formal "data at least as extreme" phrasing is buried until §3.8. Tighten the chain.

**m-2.** §3.3 line 134: closed-form $\hat b$ formula is given, but the chapter just *introduced* it after saying in §1 line 31 that matrix form is not covered. The scalar closed form is on the boundary — fine to include but inconsistent with the "stay scalar" framing. Either commit to scalar derivation or drop it.

**m-3.** Glossary at top (line 5) lists "polynomial regression (forward-reference only)" — good. But the same line lists "$R^2$" and "adjusted $R^2$" without distinguishing whether adjusted-$R^2$ formula is examinable. See C-1.

**m-4.** §3.11 line 291 — interaction-term example uses 7, 11, 6 — three rows — but does not match the example dataset shown on slide 42 (which uses Male=7, Female=11, Female=6). Minor — but worth a "see slide 42 for the source rows" to avoid the impression the numbers are arbitrary.

**m-5.** §3.12 line 304 figure caption says "thinner the ellipse, the stronger the correlation" — this is correct for the standard ellipse correlation plot, but the chapter never tells the student how to **read** the colour (blue = positive, red = negative). Caption needs a half-sentence.

**m-6.** §4.1 algorithm step 5 mentions "the diagonal of $(X^\top X)^{-1}$" — but §1 said matrix form is not in scope. Inconsistent. Either keep step 5 high-level ("software computes SE from the design matrix") or accept that you've introduced matrix form.

**m-7.** §6 Pitfall 12 line 625 — lumps "MSE, RMSE, gradient descent, learning rate, epoch, polynomial regression" as "covered in ML Lab 2" — but if the exam covers only L11 these are not examinable. The framing should be "if an exam question uses these names, that's a Lab 2 carryover; don't worry."

**m-8.** §8 cheat-sheet line 685 — "Dummy variable: 0/1 recoding..." does not remind the reader about the $k-1$ rule. Inconsistent — the rule appears in §3.10 and Pitfall 4 but is the single most testable factoid and should be in the cheat-sheet.

**m-9.** Line 314 — "A correlation of exactly 1 is the extreme case where the two variables encode the same information twice (units in kg vs grams)" — kg vs g have correlation 1 because they are **linear** rescalings; this is true. But the slide-48 example "Sales vs Assets at 0.9488" is **not** that case; they are conceptually related but not identical. Chapter handles this OK but the wording on line 313-314 risks confusing students between "perfectly multicollinear" and "near-multicollinear."

**m-10.** Figure 10 caption (line 79) mentions "See `figures.md` REWORK note" — this is internal scaffolding leaking into the study chapter. Strip.

---

## 2. Coverage check against PDF slide-by-slide

| Slide | Topic | Chapter coverage | Verdict |
|---|---|---|---|
| 1 | Title | — | N/A |
| 2 | What is a model | §3.1 | OK |
| 3 | Why models | §3.1 | OK |
| 4 | Soft-drink data | §3.2, §5.1 | OK |
| 5 | Scatter | §3.2, §5.1 | OK |
| 6 | Hypothetical model | §3.2 | OK but units (M-5) |
| 7 | Intercept/slope definitions | §3.2 | OK |
| 8 | Three candidate lines | §3.2 | OK |
| 9 | Wikipedia / Galton | §3.1 | OK |
| 10 | Residual, OLS, "or absolute residuals" | §3.3 | OK |
| 11 | Sales = 51.849 + 7.527 × Advt | §3.4 | OK |
| 12 | SST visual | §3.5 | OK |
| 13 | SST formula | §3.5 | OK |
| 14 | SSE formula | §3.5 | OK |
| 15 | SSR formula, R² | §3.5, §3.6 | OK |
| 16 | R-squared interpretation, R output (Part I/II) | §3.6, §5.1 | OK |
| 17 | Add INCOME | §3.7, §5.2 | OK |
| 18 | Adjusted R² | §3.7 | **Weak** — see C-1 |
| 19 | p-value | §3.8 | **Weak** — see M-1 |
| 20 | Bathroom slope | §3.9, §5.3 | OK |
| 21 | Confidence interval | §3.9, §5.3 | OK but M-2 |
| 22 | Section header | — | N/A |
| 23 | Linearity limit | §3.13 | OK |
| 24 | Saturation example | §3.13 | OK |
| 25 | Need for flexibility | §3.13 | OK |
| 26 | Interaction + dummy headline | §3.10, §3.11 | OK |
| 27 | Interaction = product | §3.11 | OK |
| 28 | Spending/salary examples | §3.11 | **Missing** — chapter cites slides 26–28 but never reproduces the spending/salary or price-sensitivity *worked* examples. They are exam-easy "give an example of a plausible interaction term" questions. |
| 29 | Salary dataset | §5.4 | OK |
| 30 | Boxplot salary | §5.4 | OK |
| 31 | Boxplot experience | §5.4 | OK |
| 32 | Salary–Experience scatter by gender | §5.4 | OK |
| 33 | Dummy explained | §3.10 | OK |
| 34 | Gender.Male formula + trap warning | §3.10 | OK |
| 35 | R output Model A | §5.4 | OK |
| 36 | Interpret Model A | §5.4 | OK |
| 37 | Baseline = intercept | §3.10 | OK |
| 38 | R output Model B | §5.4 | OK |
| 39 | Model B male/female equations | §5.4 | OK |
| 40 | Model B parallel lines plot | §5.4 | OK |
| 41 | Need varying slopes | §3.11 | OK |
| 42 | Creating Gender.Exp.Int (row-by-row) | §3.11 | OK |
| 43 | R output Model C | §5.4 | OK |
| 44 | Interpret Model C — **sign flip** | §6 Pitfall 6 | OK |
| 45 | Model C male/female equations | §5.4 | OK |
| 46 | Model C non-parallel lines plot | §5.4 | OK |
| 47 | Multicollinearity four panels | §3.12 | OK |
| 48 | Diagnosing multicollinearity | §3.12 | OK |
| 49 | Thanks | — | N/A |

**Missed slide-level content:** slide 28 (the *examples* of plausible interaction terms in retail: salary×location, price×channel) is cited but not reproduced. These are exactly the kind of "give your own example of an interaction term" prompts the exam loves. Add a 4-line subsection or bullet list.

---

## 3. Exam-readiness probes (what could the exam ask, and would the chapter get you full marks?)

| Likely exam question | Chapter answer? | Mark expectation |
|---|---|---|
| "Write the OLS objective function." | §3.3 — yes, SSE formula given. | Full marks. |
| "Interpret the slope 7.527 in the soft-drink model." | §3.4 line 150 — yes. | Full marks. |
| "Define SST, SSE, SSR and state their relationship." | §3.5 — yes. | Full marks. |
| "Define R² and give its range." | §3.6 — yes, [0,1] caveated for OLS training. | Full marks. |
| "Why use adjusted R² instead of R²?" | §3.7 — yes. | Full marks. |
| "Give the adjusted R² formula." | §3.7 — gives formula but flags as "not in slides." | **Risk** — see C-1. |
| "What does a p-value of 0.0115 mean for the ADVT slope?" | §3.8 — yes, but with the imprecise slide-19 phrasing. | **Risk** — see M-1. |
| "Compute a 95% CI for slope 7.527 with SE 2.741." | §3.9 — yes, formula and worked example. | Full marks. |
| "Why might statistically significant ≠ practically important?" | §3.9, §5.3 — yes, bathroom example. | Full marks. |
| "Why use $k-1$ dummies for $k$ categories, not $k$?" | §3.10 — yes. | Full marks. |
| "Write the male-specific line from Model B coefficients." | §5.4 — yes, line 539. | Full marks. |
| "What does the interaction coefficient 2,086.2 mean?" | §5.4 — yes, line 579 explains. | Full marks. |
| "When R² = 0.25, is the model good?" | §3.6 — yes, "depends on discipline." | Full marks. |
| "Why might a coefficient flip sign when you add an interaction?" | §6 Pitfall 6 line 612 — yes. | Full marks. |
| "What does the F-statistic test?" | §6 Pitfall 11 — one line. | **Risk** — see C-4. Sufficient for "tests the whole model" answer, insufficient for "what is the null hypothesis of the F-test." |
| "What is multicollinearity and how do you diagnose it?" | §3.12 — yes. | Full marks. |
| "Two predictors have correlation 0.95 — what is the risk?" | §3.12 + Pitfall 8 — yes. | Full marks. |
| "Define degrees of freedom in regression." | — | **Fail** — see C-5. |
| "Can R² be negative?" | §3.6 yes, §8 cheat sheet no. | **Risk** — see M-3. |
| "Give an example of a plausible interaction term in business." | — | **Fail** — chapter cites slide 28 but doesn't reproduce. |
| "What does the intercept p-value 0.0768 mean?" | §5.1 table mentions it. | Partial — chapter doesn't say why this is usually uninteresting. |

**Probe summary:** of ~20 plausible exam Qs, the chapter is *full-marks-ready* on ~14, *partial-credit-risky* on ~5, and *fails* on 2. That is a **B+ chapter for an A grade exam**. Not yet at the "open the chapter the night before, ace the exam" bar this project is aiming at.

---

## 4. Pedagogical hazards (will a student misinterpret?)

1. **The "two passports" analogy for multicollinearity** (§2 line 59 / §3.12 line 322) is good, but the chapter never makes the student manually compute a correlation. Slide 48 shows a 0.9488. The chapter could insert a tiny "compute the correlation between these 5 (X1, X2) pairs by hand" exercise. Exam Q: "Given a correlation matrix, identify which pair triggers concern." The chapter has the rule but not the exercise.

2. **Adjusted R²** is introduced via a *table* (§3.7 line 215) where the student is supposed to absorb "raw vs adjusted." The table is fine but there is no "if I add a noise variable, what happens to each?" worked example. The slide-deck has the conceptual claim; the chapter could add a 3-line illustrative micro-example. Otherwise the student has to take it on faith.

3. **The bathroom example** assumes the student knows that "break-even" means the lower CI bound must clear the threshold. Some students will write "the point estimate 7,883 > 6,000 → add the bathroom" and lose marks. Pitfall 2 covers this — but maybe make it the *first* pitfall, or in §5.3 add a "Wrong answer: …" panel showing the trap.

4. **Sign-flip pitfall** (Pitfall 6, line 612) is great but easy to skim. Worth a callout box. Slide 44 itself flags it; the chapter could elevate.

5. **The chapter never derives the formula $\hat b = \frac{\text{cov}(x,y)}{\text{var}(x)}$ even though it gives the equivalent sum-form.** This costs nothing to add and clarifies the closed-form OLS.

---

## 5. Glossary check

Glossary terms claimed at line 5: linear regression, OLS, residual, intercept, slope, sum of squares (SST/SSE/SSR), R², adjusted R², p-value, confidence interval, dummy variable, interaction term, multicollinearity, polynomial regression (forward-ref).

Cross-checked against text definitions:
- All 14 terms are defined inline at first use. **Pass.**
- **Missing from glossary list:** baseline, design matrix, normal equations, F-statistic, t-statistic, standard error, degrees of freedom — all of which the chapter uses without listing as glossary terms. At least baseline, F-statistic, t-statistic, and standard error should be on the list since they appear in R output.

---

## 6. Forward-reference discipline

§1 line 26–32 commits to NOT covering MSE/RMSE/gradient descent/learning rate/regularisation/polynomial features/train-test split. Audit:

- MSE/RMSE — mentioned at §1 line 28 and §4.2 table. Forward-ref clean.
- Gradient descent — §1, §3.3 line 135, §4.2. Forward-ref clean.
- Polynomial — §1, §3.13 line 336, §8. Forward-ref clean.
- Train/test — §4.2 table, §7. Forward-ref clean.
- Matrix form $X^\top X$ — §1 line 31 says "not covered," but §3.3 line 135, §4.1 step 5, and §6 implicitly use it. **Inconsistent** — see m-2, m-6.

---

## Report to PM

**Assignment recap:** L11 Regression, Round 1, exam-readiness review (Spec §7.1). Compared chapter `study/lectures/L11-Regression.md` against PDF `Lecture11-Regression.pdf` (49 slides).

**Status:** PASS WITH MAJOR CONCERNS — chapter is conceptually strong but has 5 critical and 7 major exam-relevance gaps. Not yet at the "study only this chapter and ace the exam" bar.

**P0 findings:** None — no factual contradictions of the slide deck severe enough to teach the student something *wrong*.

**P1 findings (critical / major, must address before exam):**
1. **C-1** Adjusted R² formula provenance ambiguous; Model B adjusted-vs-raw R² blurred in prose (§3.7, §5.4).
2. **C-2** Model C "males start a touch lower" — \$8,034 on \$66,334 is 12%, not "a touch." Tighten §5.4 line 579.
3. **C-3** $\text{SSR} = \sum (\hat y_i - \bar y)^2$ buried in parenthetical (§3.5 line 174). Promote.
4. **C-4** F-statistic never explained beyond one pitfall line; no statement of null hypothesis or contrast with per-coefficient p-values. Add §3.8.1.
5. **C-5** Degrees of freedom never defined. Add one sentence in §4.1.
6. **M-1** p-value: slide-19 informal definition quoted at line 231 without flagging as imprecise.
7. **M-2** Confidence interval — conflates t-quantile (2.069 for 23 d.f.) with z-quantile (1.96). §3.9 line 256.
8. **M-3** "$R^2 \in [0,1]$" in §8 cheat-sheet contradicts §3.6 caveat about test-set $R^2$ possibly being negative.
9. **M-4** Dummy-variable trap asserted as "model cannot be estimated" without tying to $X^\top X$ singularity. §3.10.
10. **M-5** Units mystery: Sales/Advertising scale never clarified. §3.2, §5.1.
11. **M-6** House-price regression: response variable (price) never named in §5.3.
12. **M-7** Intercept p-values flagged in tables but never marked as "usually uninteresting."

**P2 findings (polish):**
- m-1 through m-10 (see §1 above): minor wording, missing slide-28 worked examples, glossary gaps (baseline, F-stat, t-stat, SE, d.f.), internal scaffolding leak ("See figures.md REWORK note"), inconsistent matrix-form scope.
- Missed slide content: slide 28 interaction-term *examples* (salary×location, price×channel) are exam-bait and absent from prose.
- Cheat-sheet missing the $k-1$ dummy rule (Pitfall 4 has it; §8 does not).

**QA Checklist (§7) status:**
- Source fidelity: **Pass with concerns** — see C-1, C-2, M-1, M-2.
- Coverage of all 49 slides: **Pass** — every slide accounted for except slide 28 examples missing.
- Glossary: **Pass with concerns** — 4 terms used but unlisted (baseline, F-statistic, t-statistic, standard error, degrees of freedom).
- Pedagogical traps marked: **Pass** — Pitfalls section is strong (12 entries).
- Forward references disciplined: **Pass with concerns** — matrix form leaks into §3.3, §4.1.
- Worked examples reproducible: **Pass** — soft-drink, INCOME, bathroom, salary all walkable.
- Cheat-sheet self-contained: **Fail** — missing $k-1$ rule, mis-states $R^2$ range, no F-stat row.

**Acceptance criteria (§1) status:**
- "Study only this chapter and ace the exam" → **Not met.** B+ chapter for an A-grade exam.

**DOCUMENT.md audit:** N/A for study-chapter review.

**Out-of-scope observations:**
- The chapter cross-references L05 (Local Search) and L09a (Bayesian Networks) — these connections are good but unverified. If those chapters have not yet been written / reviewed, the hyperlinks will dangle.
- ML Lab 2 cross-refs assume that document exists; verify before publication.

**Concerns / risks:**
- The chapter consistently leans toward "more is more" — three or four passes over the same concept (analogy, formal, worked, cheat-sheet). Good for retention but creates the inconsistencies flagged above (e.g. $R^2$ range, dummy $k-1$ rule). Tighten consistency across the four passes.
- The F-statistic gap is the single most-likely exam landmine. Address before any other change.

**What PM should do next:**
1. Dispatch chapter author to fix all P1 items (C-1 through C-5, M-1 through M-7).
2. Re-run reviewers #1–3 if they have not already raised the F-stat / d.f. gap.
3. Re-QA after fixes.
4. Then publish for student use.

**DOCUMENT.md updated:** N/A for QA.
