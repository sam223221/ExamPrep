# L11 Regression — Reviewer #2 (Mathematical Rigor) — Round 1

**Reviewer role:** Lecture Reviewer #2 (Mathematical Rigor)
**Artifact reviewed:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L11-Regression.md`
**Source of truth:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture11-Regression.pdf` (slides 1–48, "Linear Regression", Serkan Ayvaz)
**Spec section:** §7.1 — verify regression formulas (residuals, R², p-values, dummy/interaction terms).
**Stance:** Harsh.

---

## Report to PM

**Assignment recap:** Verify mathematical/statistical rigor of every formula and numeric claim in the L11 Regression chapter against the slide deck. I walked every formula (residual, SSE/SST/SSR, R², adjusted R², CI, OLS closed-form, matrix normal equation, dummy/interaction algebra) and every numeric example (soft-drink simple, soft-drink + income, bathroom CI, salary models A/B/C, multicollinearity table) line-by-line. The chapter is mostly correct, often **more** rigorous than the slides themselves, but it carries several genuinely sloppy statements and at least two arithmetic/units issues that an exam-graded student would lose marks for.

**Status:** Pass with concerns (no P0, several P1, several P2).

---

### P0 findings

None. No formula is mathematically wrong in a way that would mislead the student about the underlying statistics. The headline expressions (residual, SSE, SST, SSR, R², adjusted R², CI, OLS closed-form, normal equation, dummy recoding, interaction product) are all algebraically correct as written.

---

### P1 findings (must fix before shipping)

1. **L11-Regression.md §3.4 (line 150) and §5.1 (lines 420, 423, 429, 419) — unit-of-Advertising contradiction (numerical).**
   The chapter declares in §5.1 line 394 that "Advertising (\$ thousands)" and "Sales (units sold, in thousands)." It then claims:
   - line 150: "For every **one-dollar** increase in advertising, sales increase by **\$7.527** on average."
   - line 420: "Every additional **\$1** of advertising buys **7.527** additional units of sales on average."
   - line 419: "With zero advertising, predicted sales ≈ **51,849 units**."
   - line 429: "For Advertising = 10 (i.e. **\$10,000**), … ≈ **127,119 sales units** predicted."

   If Advertising is in \$k as the chapter explicitly states, then per **\$1** of ad spend the increment is \$0.007527, not \$7.527. The slope of 7.527 is per **\$1,000** of ad spend. The chapter cannot have it both ways — either Advertising is in raw dollars (in which case the data table values 9.5, 10.1, 9.4 etc. are absurd) or it is in \$k (in which case the per-\$1 phrasing is wrong by a factor of 1,000).
   Worse, the slide itself (slide 11) is loose ("for every \$1 increase in advertising sales increase by \$7.527"), but the chapter introduces the "\$ thousands" unit convention that the slide does not commit to and then ignores its own convention.
   **Fix:** Pick one convention. Recommended: state explicitly that the data are stored in whatever units the slide uses (the slide simply shows raw numbers 9.5, 10.1 … and 145.1, 128.3 …; the simplest honest reading is "Sales in **some** units, Advertising in **some** units, and the slope is 7.527 of-those-Sales-units per of-those-Advertising-units"). If you keep the "\$ thousands" reading, rewrite line 150 and 420 to say "per \$1,000 of ad spend" or "per unit (= \$1,000) of advertising," and rewrite line 419 to say "≈ \$51,849 of sales (51.849 thousand units)" — pick consistent units everywhere.

2. **L11-Regression.md §3.5 line 174 — SSR identity asserted without justification.**
   Chapter writes:
   > "Equivalently, $\text{SSR} = \sum_i (\hat y_i - \bar y)^2$ — how far the fitted predictions stray from the mean."
   This identity is **only** true because the cross-term $\sum_i (\hat y_i - \bar y)(y_i - \hat y_i)$ vanishes, and that vanishing requires (i) OLS estimation and (ii) an intercept in the model. The chapter just says "Equivalently" with no flag. This is exactly the kind of "obvious" identity that the lecturer is likely to drill on the exam — the student should know it depends on the OLS+intercept setup. The slide (15) writes only SSR = SST − SSE and never asserts the Σ(ŷ − ȳ)² form, so the chapter is *adding* a result without justifying it.
   **Fix:** Either drop the second form, or add one sentence: "This second equality requires the OLS normal-equation property that residuals are orthogonal to fitted values, which holds whenever the model includes an intercept."

3. **L11-Regression.md §3.8 line 230–232 — p-value definition is doubled and the slide's wrong version is left standing.**
   The chapter first **quotes the slide's definition** as if authoritative:
   > "The **p-value** measures the probability that, given the current information, a particular predictor has no relationship with the response."
   This statement, taken literally, is wrong: it conflates $P(\text{data} \mid H_0)$ with $P(H_0 \mid \text{data})$. The chapter then immediately gives the correct definition ("probability of observing a coefficient at least as extreme as the one estimated, assuming the true coefficient were zero"). Leaving both side-by-side without flagging the conflict makes the slide look authoritative when it is in fact mathematically loose. A student reading quickly may memorise the wrong (slide) definition.
   **Fix:** Add a clear caveat: "The slide phrasing collapses the conditional — strictly, the p-value is *not* the probability that the predictor has no relationship, it is the probability of seeing a coefficient this extreme **assuming** the null is true. The two are not equal (this is the prosecutor's fallacy / base-rate fallacy)." Or just demote the slide quote to a footnote and lead with the rigorous definition.

4. **L11-Regression.md §3.6 line 185–187 — claim "$R^2 \in [0,1]$" is gated correctly but the gating wording is slippery.**
   Chapter says: "It always lies in $[0, 1]$ for OLS on training data." Mathematically this is *only* true when the OLS model includes an intercept (otherwise SST need not bound SSE). Without an intercept, R² can be negative even on training data, and many texts therefore avoid quoting R² at all for no-intercept regressions. Since the entire lecture assumes models of the form $y = a + b_1 x_1 + \dots$ (intercept always present), the chapter is *de facto* fine, but the rigor reviewer flags it.
   **Fix:** Either add the parenthetical "(provided the model contains an intercept, which the lecture always assumes)" or live with the slight slop. P1 because the lecture's whole framing assumes intercepts, so a careful exam question could exploit this.

5. **L11-Regression.md §3.7 line 212 — adjusted R² formula is given, but the slide never gives it.**
   The chapter prints
   $$R^2_{\text{adj}} = 1 - \frac{n-1}{n-p-1}(1 - R^2)$$
   as "the standard expression — useful to know for variant questions." That formula **is** the standard one used by R's `lm()` summary output and is consistent with the numerical Adjusted R² values quoted (e.g., 0.2142, 0.4022, 0.1158, 0.4359, 0.5495). I sanity-checked numerically:
   - Model 1: n = 25, p = 1, R² = 0.2469. R²_adj = 1 − (24/23)(1 − 0.2469) = 1 − 1.04348 × 0.7531 = 1 − 0.78588 = **0.21412**. Slide rounds to **0.2142**. ✓
   - Model 2: n = 25, p = 2, R² = 0.4520. R²_adj = 1 − (24/22)(0.548) = 1 − 1.09091 × 0.548 = 1 − 0.59782 = **0.40218**. Slide rounds to **0.4022**. ✓
   - Model A (salary, dummy only): n = 208, p = 1, R² = 0.1201. R²_adj = 1 − (207/206)(0.8799) = 1 − 1.004854 × 0.8799 = 1 − 0.88418 = **0.11582**. Slide rounds to **0.1158**. ✓
   - Model B: n = 208, p = 2, R² = 0.4413. R²_adj = 1 − (207/205)(0.5587) = 1 − 1.009756 × 0.5587 = 1 − 0.56415 = **0.43585**. Slide rounds to **0.4359**. ✓
   - Model C: n = 208, p = 3, R² = 0.5561. R²_adj = 1 − (207/204)(0.4439) = 1 − 1.014706 × 0.4439 = 1 − 0.45042 = **0.54958**. Slide rounds to **0.5495** (slight off-by-one in last digit from rounding of R² to 4 sf, not a chapter error). ✓
   The formula is correct and arithmetic checks. But it is presented as "the lecture states the property but does not give the formula" — that is true, the slide really does not. The chapter is **adding content the slide does not contain**, which is fine for a study guide but should be more clearly flagged as a chapter extension rather than slide material.
   **Fix:** Flag this paragraph more visibly as "(EXTENSION — not on the slides, but the formula behind every Adjusted R² value R prints; expect a variant exam question to either give you this or have you derive it.)"

6. **L11-Regression.md §3.9 line 259 — CI upper bound disagrees with the slide by 0.002.**
   Chapter writes the bathroom CI as $[\$3{,}649.208,\ \$12{,}117.348]$. The slide (21) writes the upper bound as **\$12,117.35** (two decimals). The arithmetic 7883.278 + 2 × 2117.035 = 7883.278 + 4234.07 = **12117.348** is mathematically what the chapter has; the slide just rounded to 12117.35. So the chapter is internally more accurate than the slide, but it disagrees with the source as printed. Since elsewhere the chapter is religiously faithful to slide numerics, the inconsistency is jarring.
   **Fix:** Add a short footnote: "Slide 21 prints the upper bound as \$12,117.35; the precise arithmetic 7,883.278 + 2 × 2,117.035 gives \$12,117.348." Then the student knows both numbers and which is the true source.

7. **L11-Regression.md §5.1 line 394 — sample size n = 25 is invented from the slide.**
   Chapter says "For 25 sales regions it records Advertising and Sales." The slide (4) shows only nine rows; the n = 25 figure comes from reading "23 degrees of freedom" off the lm output on slide 16 and inferring n = 23 + 2 = 25 (residual df = n − p − 1 for a 1-predictor model with intercept). The inference is correct but the chapter should state it as an inference, not as primary data.
   **Fix:** Add "(n = 25, inferred from the 23 residual degrees of freedom reported in figure 18)."

---

### P2 findings (polish / suggestions)

1. **Line 134 closed-form OLS** — formula correct, but the chapter says "For one predictor it is …" without mentioning that the same formula equals $\text{Cov}(x,y) / \text{Var}(x)$, which is the form most students will see in stats coursework. Minor missed connection.

2. **Line 256 — "rule-of-thumb approximation to the 97.5% quantile of the t-distribution"** — better to say "the 97.5% percentile of the standard normal (or t with large df)." The chapter is *roughly* right but the precise statement is that 1.96 is the standard-normal critical value; the t-quantile depends on df, so calling 1.96 a t-quantile is sloppy.

3. **§4.1 pseudocode line 363** — "Compute the standard errors SE(b_j) for each coefficient (formula uses the residual standard error and the diagonal of (X^T X)^{-1})." Correct in spirit. For a rigorous study guide, the full formula $\widehat{\text{SE}}(\hat\beta_j) = \hat\sigma \sqrt{[(X^\top X)^{-1}]_{jj}}$ with $\hat\sigma^2 = \text{SSE}/(n-p-1)$ would be worth half a line in §4.1, since the slide does indirectly use it via the printed Std. Error column. This is a P2 because the slide doesn't derive it either.

4. **Line 426 — F-statistic p-value listed without any mention of what the F-statistic actually is.** §6 pitfall #11 alludes to it ("tests does any predictor matter") but the chapter never writes $F = (\text{SSR}/p) / (\text{SSE}/(n-p-1))$ or even names the numerator/denominator df. The slide also omits this, so it is in-scope to skip, but for a "Mathematical Rigor" review I have to flag it — the chapter prints F-statistic numbers (7.54, 9.074, 28.12, 80.98, 85.18, 113.3) in tables without saying what the test ratio actually is.

5. **§3.10 line 277 — "dummy-variable trap" framing.** Chapter says "the second column would be a perfect linear combination of the first — perfect multicollinearity (§3.12) and the model cannot be estimated." Strictly, with $k$ dummies for $k$ levels plus an intercept column, the design matrix is rank-deficient by 1 (the sum of all $k$ dummies equals the intercept column), so $(X^\top X)$ is singular. The chapter says "the second column would be a perfect linear combination of the first" — for $k = 2$ that is correct (Female = 1 − Male, and 1 is the intercept), but the phrasing obscures that the relation is *with the intercept column*, not just the other dummy. A student trying to extend the rule to $k = 3$ levels (e.g., Neighborhood: North/South/West) needs to understand that the rank deficiency is between the dummies *and the intercept*.
   **Suggested fix:** "If you include all k dummy columns together with the intercept column, the sum of the dummy columns equals the intercept column, making the design matrix rank-deficient."

6. **§5.4 line 587 table — Adjusted R² column for Model C is 0.5495.** Slide 43 says 0.5495. My recomputation above gives 0.54958, which rounds to 0.5496 if you use R² = 0.5561 exactly. The discrepancy is a rounding cascade, not an error, but a careful student rechecking the math will be momentarily confused. Worth a one-line footnote.

7. **§3.13 line 332 — "advertising shows diminishing returns ('saturation point') and may even backfire if overdone (inverse-U)."** The slide (24) does mention "saturation point" and "negative effect" but the chapter promotes the qualitative observation to a stronger claim ("inverse-U"). The lecture content is only suggestive, not committal. Minor.

8. **Cheat sheet line 689 — CI formula uses literal "2" with no asterisk back to the 1.96 note in §3.9.** Easy to misremember as the exact critical value. Tiny.

9. **§3.3 line 131 — "produces statistical properties that line up with the Gaussian-noise assumption."** Correct but a bit vague. The precise statement is that OLS = MLE under Gaussian errors. The chapter could win a half-mark by saying so explicitly.

10. **Glossary forward-reference for polynomial regression (line 5, §3.13 line 336)** — fine, just confirming this is properly flagged FWD-REF; chapter does so.

---

### Verification of every numeric claim (slide vs chapter)

| Chapter quantity | Chapter value | Slide value | Verdict |
|---|---|---|---|
| Soft-drink intercept | 51.849 | 51.849 (slide 11) | ✓ |
| Soft-drink slope | 7.527 | 7.527 | ✓ |
| R² (ADVT only) | 0.2469 | 0.2469 | ✓ |
| Adj R² (ADVT only) | 0.2142 | 0.2142 | ✓ |
| Intercept p-value (ADVT only) | 0.0768 | 0.0768 | ✓ |
| ADVT p-value (ADVT only) | 0.0115 | 0.0115 | ✓ |
| Residual SE (ADVT only) | 14.51 on 23 df | 14.51 on 23 df | ✓ |
| F-statistic p-value | 0.01151 | 0.01151 | ✓ |
| Intercept (ADVT + INCOME) | 36.8948 | 36.8948 | ✓ |
| ADVT slope (with INCOME) | 5.0691 | 5.0691 | ✓ |
| INCOME slope | 0.8081 | 0.8081 | ✓ |
| R² (ADVT + INCOME) | 0.4520 | 0.452 | ✓ |
| Adj R² (ADVT + INCOME) | 0.4022 | 0.4022 | ✓ |
| Bathrooms estimate | 7,883.278 | 7,883.278 | ✓ |
| Bathrooms SE | 2,117.035 | 2,117.035 | ✓ |
| Bathrooms t-value | 3.724 | 3.724 | ✓ |
| Bathrooms p-value | 0.000300 | 0.000300 | ✓ |
| 95% CI lower | 3,649.208 | 3,649.208 | ✓ |
| 95% CI upper | 12,117.348 | 12,117.35 | P1 #6 (rounding mismatch with slide) |
| Salary Model A intercept | 74,420 | 74420 | ✓ |
| Salary Model A Gender.Male | 16,591 | 16591 | ✓ |
| Salary Model A p-value | 2.94 × 10⁻⁷ | 2.94e-07 | ✓ |
| Salary Model A R² | 0.1201 | 0.1201 | ✓ |
| Salary Model A Adj R² | 0.1158 | 0.1158 | ✓ |
| Salary Model B intercept | 53,260 | 53260.0 | ✓ |
| Salary Model B Experience | 1,744.6 | 1744.6 | ✓ |
| Salary Model B Gender.Male | 17,020.6 | 17020.6 | ✓ |
| Salary Model B male intercept | 70,280.6 (= 53260 + 17020.6) | 70,280.6 | ✓ |
| Salary Model B R² | 0.4413 | 0.4413 | ✓ |
| Salary Model B Adj R² | 0.4359 | 0.4359 | ✓ |
| Salary Model C intercept | 66,333.6 | 66333.6 | ✓ |
| Salary Model C Experience | 666.7 | 666.7 | ✓ |
| Salary Model C Gender.Male | −8,034.3 | -8034.3 | ✓ |
| Salary Model C Gender.Exp.Int | 2,086.2 | 2086.2 | ✓ |
| Interaction p-value | 7.95 × 10⁻¹² | 7.95e-12 | ✓ |
| Salary Model C R² | 0.5561 | 0.5561 | ✓ |
| Salary Model C Adj R² | 0.5495 | 0.5495 | ✓ |
| Male-specific intercept (Model C) | 58,299.3 (= 66333.6 − 8034.3) | 58,299.3 | ✓ |
| Male-specific slope (Model C) | 2,752.9 (= 666.7 + 2086.2) | 2,752.9 | ✓ |
| Soft-drink prediction at Advt=10 | 127.119 | (not stated on slide; chapter extension) | ✓ arithmetic, P2 unit issue |
| Sales/Assets correlation | 0.9488 | 0.9488454 | ✓ (chapter rounds, fine) |
| Multicollinearity correlation threshold | 0.8 or 0.9 | 0.8 or 0.9 | ✓ |

**Numerical audit verdict:** every single value in the chapter ties out to the slide, modulo the one slide-rounding mismatch already flagged in P1 #6.

---

### Formula audit

| Formula | Chapter form | Mathematically correct? | Slide-supported? |
|---|---|---|---|
| Residual | $r_i = y_i - \hat y_i$ | ✓ | ✓ (slide 10) |
| OLS objective | $\text{SSE} = \sum (y_i - \hat y_i)^2$ | ✓ | ✓ (slide 14) |
| SST | $\sum (y_i - \bar y)^2$ | ✓ | ✓ (slide 13) |
| SSE | $\sum (y_i - \hat y_i)^2$ | ✓ | ✓ (slide 14) |
| SSR = SST − SSE | ✓ | ✓ | ✓ (slide 15) |
| SSR = Σ(ŷ − ȳ)² (second form) | ✓ but unjustified | ✓ (under OLS+intercept) | ✗ slide does not give it — P1 #2 |
| R² = SSR/SST = 1 − SSE/SST | ✓ | ✓ | ✓ (slide 15) |
| Adjusted R² | $1 - \frac{n-1}{n-p-1}(1-R^2)$ | ✓ | ✗ slide does not give it — P1 #5 |
| OLS 1-predictor closed-form | $\hat b = \frac{\sum (x_i-\bar x)(y_i-\bar y)}{\sum(x_i-\bar x)^2}$, $\hat a = \bar y - \hat b \bar x$ | ✓ | ✗ slide does not derive — chapter extension, OK |
| Matrix normal-equation | $\hat\beta = (X^\top X)^{-1} X^\top y$ | ✓ | ✗ slide does not give — chapter extension, OK |
| 95% CI | $\hat b \pm 2 \text{SE}(\hat b)$ | ✓ (with 1.96 footnote) | ✓ (slide 21) |
| Dummy recoding | Gender.Male = 1 if male, 0 otherwise | ✓ | ✓ (slide 34) |
| Interaction product | row-by-row, Gender.Male × Experience | ✓ | ✓ (slide 42) |
| t-statistic | $t_j = \hat b_j / \text{SE}(\hat b_j)$ | ✓ (in §4.1 pseudocode) | implicit on slide via R output |

All formulas pass; only flags are P1 #2 (justification missing) and P1 #5 (slide does not supply the formula, chapter does — fine, but flag as extension).

---

### QA Checklist (§7) status

The Feature Plan / spec §7.1 directive was "Verify regression formulas: residuals, R², p-values, dummy/interaction terms." Walking each:

- **Residuals** — Pass. Definition correct, sign convention noted, OLS objective correct.
- **R²** — Pass with concern. Numerical R² values all match slide. The decomposition identity is correct but SSR = Σ(ŷ − ȳ)² is asserted without justification (P1 #2). The [0,1] range is gated correctly but not perfectly (P1 #4).
- **p-values** — Pass with concern. Numerical p-values all match slide. The slide's loose definition is quoted alongside the correct one without flagging the conflict (P1 #3).
- **Dummy variables** — Pass. Recoding correct, baseline interpretation correct, k−1 rule given. P2 #5 only.
- **Interaction terms** — Pass. Row-by-row product correct, group-specific line derivations all arithmetic-check (58,299.3 = 66,333.6 − 8,034.3; 2,752.9 = 666.7 + 2,086.2). Sign-flip pitfall (chapter §6 pitfall #6) correctly identified.

**Adjusted R²** (not explicitly named in spec §7.1 but covered by the chapter): Pass. Formula correct, numerical audit confirms all four printed values to within slide rounding.

**Confidence intervals** (chapter §3.9): Pass with concern. Formula correct. Numerical CI = [3,649.208, 12,117.348] vs slide [3,649.208, 12,117.35] flagged P1 #6.

**Multicollinearity** (chapter §3.12): Pass. No formulas to verify beyond the correlation threshold 0.8/0.9; that ties to the slide.

---

### Acceptance criteria (§1) status

The spec §7.1 has one acceptance criterion: every formula must match the slides or be derivable from them, and every numeric value must match. **Met**, with the noted unit-confusion in §3.4/§5.1 (P1 #1) which is a *consistency* failure, not a formula error.

---

### DOCUMENT.md audit

Not applicable to this review — `study/lectures/` is a documentation tree, and I was not asked to evaluate file scaffolding for this round. The PM should confirm whether `study/lectures/DOCUMENT.md` exists and lists L11-Regression.md.

---

### Out-of-scope observations

1. **§7 Connections to Other Lectures (line 637)** — Chapter says: "L11's whole topic falls under [supervised learning](L10-Intro-to-ML.md): given input/output pairs, learn the input-to-output mapping. Compare against L12's unsupervised clustering, which has no target y." This references L12 which I have not been asked to verify. The directional link is fine but Reviewer #1 (Pedagogy) or a cross-lecture reviewer should check the L12 reference exists.

2. **§4.2 Lecture-vs-Lab comparison table** — Chapter contrasts L11 lecture with "ML Lab 2." I have not been asked to verify ML Lab 2 exists or contains the claimed material (gradient descent, MSE/RMSE, polynomial features, train/test split, learning rate, epochs). Recommend PM dispatch a separate reviewer to confirm ML Lab 2 actually contains what the chapter promises, since the chapter repeatedly defers to it.

3. **Figure paths** (e.g., line 75 `../extracted_figures/L11/fig09-page09-img1.jpeg`) — Not in my scope (Reviewer #1 / image reviewer territory), but I note that the chapter relies on these figures being present in the expected location. If they are missing the chapter will render with broken images.

4. **Chapter glossary list at line 5** — Lists "polynomial regression (forward-reference only)" but also lists `multicollinearity` without a forward-reference flag, even though slide-level coverage is one slide (47) plus one example (48). The chapter §3.12 treatment is much fuller than the slide. Fine, but the glossary's signalling that everything except polynomial regression is "fully covered" is mildly overclaiming.

---

### Concerns / risks

1. **The chapter is more rigorous than the slides on multiple points.** This is generally good for a study guide, but in two places (adjusted R² formula §3.7, second form of SSR §3.5) the chapter adds mathematical content the slide does not contain. Exam students cramming from the slides alone will not have seen the closed-form OLS expression or the adjusted R² formula. Either the chapter should warn that these are extensions ("not on the slides — but you'll need them for variant questions"), or the PM should confirm with the course materials whether the exam can fairly assess them. Right now the chapter quietly promotes extension material into the main flow.

2. **The unit confusion in §3.4/§5.1 (P1 #1) is the kind of slip that becomes a habit.** If the chapter teaches the student to confuse "per \$1" with "per \$1,000," the student will carry that error into every regression interpretation question on the exam. This is the single highest-impact P1 to fix.

3. **The slide's mis-stated p-value definition (P1 #3) is dangerous because Serkan Ayvaz wrote it and so a student may assume it is the authoritative form.** The chapter's correction is too gentle — it sits side-by-side with the wrong version without flagging the conflict. Suggest stronger wording.

4. **Forward-reference discipline is uneven.** Polynomial regression is correctly flagged FWD-REF; MSE/RMSE, gradient descent, learning rate, epoch are mentioned as "covered in ML Lab 2" but not glossary-flagged. That is consistent with the chapter's own §1 "What L11 does not cover" list, so it is a minor signaling issue rather than a rigor failure.

5. **No matrix derivation of the slope expression.** The chapter prints both $\hat b = \Sigma(x_i-\bar x)(y_i-\bar y)/\Sigma(x_i-\bar x)^2$ and $\hat\beta = (X^\top X)^{-1} X^\top y$ but never shows how the second reduces to the first when $X$ has one predictor column and a constant column. For "Mathematical Rigor" review that is a P2-level gap, but for a student trying to connect the two forms it is a real missed teaching opportunity.

---

### What PM should do next

1. **Dispatch the chapter author / engineer back to fix P1 #1 through P1 #6.** None require new research; all are clarification/consistency fixes inside the existing prose. Estimated effort: 30 minutes.
2. After those fixes, **proceed to App Tester / Code Reviewer / pedagogy reviewer.** I do not need to re-QA the math unless the engineer changes a numeric value (they shouldn't — the audit is clean).
3. Consider whether to dispatch a **scope reviewer** to assess whether the closed-form OLS, normal equation, and adjusted R² formula belong in a "study guide for the slides" or whether they should be moved to ML Lab 2. (My recommendation: keep them in L11 but label them more clearly as extensions.)
4. **No P0s, no need to block ship.** The chapter is solid math overall.

**DOCUMENT.md updated:** N/A for QA.

---

_Reviewer #2 sign-off: the math is clean enough that I can certify the chapter does not teach false statistics. The P1s are real and worth fixing, but none of them would cause a student to learn an actually-wrong formula. The unit confusion (P1 #1) is the one I would prioritise — it is the only finding that could directly cost the student exam marks._
