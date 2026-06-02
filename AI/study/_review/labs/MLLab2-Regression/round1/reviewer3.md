# Lab Reviewer #3 — Pedagogical Clarity — Round 1

**Reviewer hat:** Pedagogical Clarity / mental-model alignment with L11.
**Target:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab2_regression_solution.ipynb`
**Reference lecture:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L11-Regression.md`
**Tone (per brief):** HARSH.

## TL;DR

The lab is well-engineered as code, but as a teaching artefact it **drifts off the L11 mental model in several places that a careful examiner will notice**. The opening "mental model" line on cell 0 is *not* the L11 analogy (it says "best straight line through scatter points"; L11 §2 calls it a "flight path through cities" and explicitly leans on that phrase for residuals, OLS, $R^2$, dummies, interactions and multicollinearity). The lab then **fabricates a different L11 quote** ("best-fit elastic band") in cell 0 that does not appear anywhere in L11. Multiple L11 vocabulary items that the lecturer drills into students — *residual, SST/SSE/SSR decomposition, $R^2$ as SSR/SST, slope/intercept terminology, adjusted $R^2$, p-value, confidence interval, dummy variable, interaction term, multicollinearity* — are silently missing or replaced with sklearn-flavoured re-namings. The student finishes this lab thinking regression = `LinearRegression().fit()` + MAE/MSE/$R^2$ + polynomial degree; they do **not** finish it able to read an `lm()` summary, decompose SST = SSR + SSE on paper, or answer "is this coefficient practically significant?" — every one of which is exam-level L11 material. Pass with **significant concerns**.

---

## 1. Mental-model alignment with L11 §2 — three findings

### Finding 1.1 [P0-pedagogical] The headline mental-model analogy contradicts L11

**Where.** Cell 0 (the top-of-notebook synopsis) and cell 1 ("Predict Your Own Grade") opener.

**What the lab says (cell 0, lines 32–42):**
> "Regression is **fitting the best straight line through scatter points**; raising the polynomial degree lets the line *bend*... Gradient descent is **rolling a marble down a bowl-shaped loss surface**..."
> "This is consistent with the L11 §2 analogy in `study/lectures/L11-Regression.md` (regression line as a 'best-fit elastic band'; polynomial degree as 'how bendy you let the band be')."

**What L11 §2 actually says (lecture lines 43–60):**
- Regression = "drawing a single straight flight path on a 2-D chart of cities."
- OLS = "the flight path that minimises the sum of squared city-offsets."
- Residual = "how far each city sits above or below the flight path on the chart."
- $R^2$ = "the share of the data's spread that the flight path absorbs."

**The damage.** The lab's cell 0 explicitly claims its analogy is *consistent with L11 §2* and quotes the lecturer as saying "best-fit elastic band" and "how bendy you let the band be." **Those words do not exist in L11.** I grepped — the strings "elastic band" and "bendy" appear zero times in `L11-Regression.md`. This is a hallucinated cross-reference and is more damaging than just missing the analogy, because a student who reads the lab and then opens L11 looking for "elastic band" will conclude either (a) they have the wrong lecture, or (b) the lab is lying to them. Either outcome blows up trust in the entire study pack.

**Cost to the student.** The flight-path analogy is *not decorative* in L11 — it is reused as a load-bearing scaffold for residuals (§3.3), OLS (§3.3 verbatim "flight-path analogy"), $R^2$ (§3.6 "shotgun-spread analogy" sits inside the same picture), dummies (§3.10 "light-switch"), interactions (§3.11 "throttle"), and multicollinearity (§3.12 "two passports"). The lab never engages with *any* of those analogies, so when the exam asks "explain $R^2$ using the analogy from L11," the student has nothing to reach for.

**Suggested fix.** Replace cell 0's mental-model paragraph with a direct quote/paraphrase from L11 §2 — flight path through cities, residuals as vertical offsets above/below the path, OLS as the path that minimises squared offsets, $R^2$ as the share of the shotgun-spread the path absorbs. Then **delete** the false "consistent with L11 §2 ... elastic band ... bendy" sentence and replace it with a real cross-reference to L11 §2 line 43.

---

### Finding 1.2 [P1] No engagement at all with the L11 dummy/interaction/multicollinearity analogies

**Where.** Entire notebook.

**The deficit.** L11 §3.10–§3.12 spend slides 33–48 (about 1/3 of the lecture) on *dummy variables, interaction terms, multicollinearity*. L11 §2 wires three named analogies to those concepts: **light switch** (dummies), **throttle** (interactions), **two passports for one person** (multicollinearity). The Gender × Experience worked example in L11 §5.4 is the *longest worked example in the entire lecture* and produces the famous "sign flip" pedagogical moment that pitfall #6 in L11 §6 specifically calls out as an exam trap.

The lab covers **none** of these. The student dataset has six features, all numeric continuous (`study_hours_per_week`, `attendance_rate_pct`, `prior_math_grade`, `sleep_hours`, `exercises_completed`, `prior_programming_years`). No categorical → 0/1 recoding, no row-by-row product term, no correlation-table multicollinearity diagnosis. The closest the lab comes is the correlation heatmap in cell 9 — but it is used purely as "look, study hours correlates with score," **not** as the multicollinearity diagnostic L11 §3.12 explicitly teaches with the Sales/Assets 0.9488 example.

**Cost to the student.** The student walks out unable to:
- Encode a 3-level Neighborhood variable as $k-1 = 2$ dummies and identify the baseline (L11 §3.10, §5.3 worked example).
- Read a Gender × Experience interaction coefficient and predict the slope of the male regression line vs the female regression line (L11 §5.4, slides 41–46).
- Look at a correlation matrix and flag pairs with $|r| \ge 0.8$ as multicollinearity candidates (L11 §3.12 slide 48 rule of thumb).

**Suggested fix.** This is genuinely awkward because the lab's dataset doesn't have a natural categorical. But the lab *could*, with minimal cost:
- Add a "section 4.5 — what if a feature were categorical?" markdown that takes `prior_math_grade` (currently treated as numeric — a defensible but exam-incorrect choice; see Finding 4.1 below) and demonstrates dummy encoding.
- Add a brief "look at the correlation heatmap with multicollinearity glasses on" callout next to cell 9, linking to L11 §3.12.
- Either include a real interaction-term mini-example, or *explicitly flag* in cell 0 that interactions are L11 territory not covered in this lab and direct the student to L11 §5.4.

If the lab cannot accommodate dummies/interactions, **the cell-0 REFERENCES block must say so out loud**: "This lab does NOT cover dummies, interactions, or multicollinearity — see L11 §3.10–§3.12 for those." Right now the lab implicitly claims to cover L11 by calling itself "Lab 2 — Regression" and citing L11 in the references, while silently dropping a third of the lecture.

---

### Finding 1.3 [P1] The "marble in a bowl" analogy for gradient descent is fine but is presented as if from L11 — L11 doesn't cover gradient descent at all

**Where.** Cell 0 lines 32–38, and cell 39 (T5 markdown).

**The issue.** Cell 0 says "Gradient descent is rolling a marble down a bowl-shaped loss surface" with no caveat that L11 doesn't teach this. Cell 39 (the T5 markdown) correctly says "Everything above used sklearn's `.fit()` as a black box. Under the hood, `LinearRegression` solves the best `w, b` with a closed-form matrix equation. But for big models ... we have to search for the answer iteratively with gradient descent." That cell 39 framing is good. But the cell-0 "mental model" paragraph that opens the lab gives gradient descent equal billing with linear regression, without flagging that **L11 explicitly punts gradient descent to "ML Lab 2"** (L11 §1 line 27: "No gradient descent. The slides treat OLS as a black-box closed-form solve; the iterative-optimisation perspective belongs to ML Lab 2 — Regression").

**Cost to the student.** Mild. The L10 chapter and L11 §7 already establish that gradient descent is lab territory. The risk is that a student who only skims cell 0 walks away thinking gradient descent is part of L11.

**Suggested fix.** In cell 0 and again in cell 39's intro, add: "L11 does *not* derive gradient descent — it treats `lm()`/`LinearRegression()` as a closed-form black box. This lab is where gradient descent enters the curriculum. The marble-bowl analogy is the lab's, not L11's."

---

## 2. L11 vocabulary the lab silently drops

L11 introduces 17 glossary terms in line 5 of its preface. I checked each one against the lab. The pattern is alarming: **the lab covers the sklearn-flavoured subset (MAE, MSE, $R^2$, train/test split, overfitting) but drops most of the statistical-inference vocabulary that L11 spends slides 17–21 hammering**.

### Finding 2.1 [P0-pedagogical] Missing: SST / SSE / SSR decomposition

**Where.** Entire notebook.

**The miss.** L11 §3.5 (lecture lines 159–186) builds the SST = SSR + SSE decomposition over three steps, with the side-by-side diagram (figure 15) that L11 explicitly calls "the single most important diagram in the lecture" (lecture line 186). L11 §3.6 (line 190) then *defines* $R^2 = $ SSR / SST = 1 − SSE/SST. The lab uses $R^2$ ten times but **never once writes out SSR or SST or SSE**. The student gets $R^2$ as "a magic number sklearn computes."

**Concretely**, in cell 13 the lab says:
> "**R²** (coefficient of determination): a rescaled score where `0` means 'no better than the lazy predictor' and `1` means 'perfect.' Formally `R² = 1 − MSE_model / MSE_lazy`."

That formula is mathematically equivalent to $R^2 = 1 - $ SSE/SST (since MSE = SSE/n and MSE_lazy = SST/n, the n's cancel). But it is **not** the L11 formula and it does not name SST/SSE/SSR. A student who learns regression from this lab can't decode an exam question that says "given SST = 1200 and SSE = 300, compute $R^2$" (that's exam-style L11 material). They also can't answer the L11 §6 pitfall #10 mnemonic question ("**T**otal, **E**rror, **R**egression").

**Suggested fix.** In cell 13 (T1's "the concept" block), add a paragraph: "$R^2$ has a more natural form in terms of sums of squares — see L11 §3.5. Total variability = SST = $\sum (y_i - \bar y)^2$; the part the model fails to explain = SSE = $\sum (y_i - \hat y_i)^2$; the part it captures = SSR = SST − SSE. Then $R^2 = $ SSR / SST = 1 − SSE/SST. The MAE_model / MAE_lazy form below is the same thing scaled by $n$." Then later, in the residual plot of cell 19, label one residual as "$y_i - \hat y_i$" and mention that summing the squares of these segments is SSE.

### Finding 2.2 [P0-pedagogical] Missing: adjusted $R^2$

**Where.** Entire notebook.

**The miss.** Adjusted $R^2$ is the named subject of L11 §3.7 (~30 lines of lecture text including the formula $R^2_\text{adj} = 1 - \frac{n-1}{n-p-1}(1 - R^2)$ and a numerical sanity check on the soft-drink data). L11 §6 pitfall #3 specifically warns against "naively comparing $R^2$ across models with different numbers of predictors." T1 has 1 feature, T2 has 6 features — this lab is **the** natural place to introduce adjusted $R^2$ and the student walks out without seeing the term.

The closest the lab gets is cell 25:
> "T1 (1 feature) R^2 was {r2_t1:.3f}. T2 (6 features) R^2 is {r2_t2:.3f}. That is a jump of {r2_t2 - r2_t1:+.3f} — using more features pays off."

Which is *the exact comparison L11 §3.7 warns is naive* — comparing raw $R^2$ across models with different $p$. The lab's defence is that we're comparing test-set $R^2$, not training-set $R^2$, which does address the naive-comparison concern by a different route (held-out test data automatically penalises useless predictors). But (a) the lab never says this is *why* the comparison is fair, and (b) the student has no clue what adjusted $R^2$ is when the exam asks them to compute it.

**Suggested fix.** In cell 25 (after the T1-vs-T2 comparison), add a paragraph: "L11 introduces a related metric, **adjusted $R^2$**, that compares models *on training data* even when they have different numbers of predictors. Formula: $R^2_\text{adj} = 1 - \frac{n-1}{n-p-1}(1 - R^2)$ — the multiplier $(n-1)/(n-p-1)$ taxes you for every extra predictor. We get away with raw $R^2$ here because we're scoring on a held-out test set, which is sklearn's go-to defence against the same problem. Both approaches show up in the exam."

### Finding 2.3 [P1] Missing: p-value, confidence interval, statistical significance

**Where.** Entire notebook.

**The miss.** L11 §3.8 (p-value), §3.8.1 (F-statistic), and §3.9 (confidence intervals) are the inferential core of the lecture — slides 19–21. The bathroom-renovation example in L11 §5.3 (slides 20–21) is one of L11's most exam-quotable moments: "the coefficient is significant ($p = 0.0003$) but the 95% CI lower bound is $3,649 < break-even \$6,000, so don't add the bathroom — statistical significance ≠ practical importance."

The lab has **none of this**. No `statsmodels.OLS()` (which would give a real `lm()`-style summary including SE / t / p / CI / F). No discussion of `model_t2.coef_` confidence intervals. The student gets coefficients in cell 26 ("Raw coefficients" display) and a "standardised coefficient" bar chart — but never sees a standard error, never sees a p-value, never sees "this slope is significant but practically irrelevant."

**Counter-argument.** This is fair-game lab territory: ML Lab 2's curriculum focus is "predictive accuracy, not inferential statistics" (the lab's own L11 §4.2 comparison table on lecture line 459 says so — "Significance: ... Not emphasised — focus is on predictive accuracy, not inferential statistics"). So the lab is *consistent with its own scoping* in not covering p-values.

**The pedagogical concern.** That scoping comment is in *L11*, not in the lab. The student reading the lab in isolation has no idea this is an intentional gap. The cell-0 REFERENCES block doesn't say "we don't cover p-values/CIs/F — go to L11 §3.8–§3.9 for those." Without that signpost, a student studying for the exam from the lab alone will not know they're missing 30% of the inferential vocabulary.

**Suggested fix.** Add to cell 0's REFERENCES block (or to cell 26's coefficient-chart commentary): "This lab focuses on predictive metrics (MAE/MSE/$R^2$). L11 introduces three more concepts on the **inference** side — p-values, 95% confidence intervals, and the F-statistic — which let you decide whether a coefficient is statistically significant and whether it's practically important. Those live in L11 §3.8–§3.9 and ML Lab 2 does *not* repeat them. The bathroom-renovation example in L11 §5.3 is the canonical worked example."

### Finding 2.4 [P1] Missing: explicit naming of `slope` and `intercept` as "$b$" and "$a$"

**Where.** Cells 4, 13, 21, 39 (everywhere the equation appears).

**The miss.** L11 uses two notations consistently: in slide 6 the simple regression is `Sales = a + b × Advertising`; in the closed-form box (§3.3 line 136) it's `b_hat`, `a_hat`. L11 §3.2 line 93 calls $a$ "intercept" and $b$ "slope" verbatim.

The lab uses **different letters and different names**:
- Cell 4 (warm-up): `\hat{y} = w \cdot x + b`; calls $w$ "weight, a.k.a. slope" and $b$ "bias, a.k.a. intercept."
- Cell 13 (T1): same `\hat{y} = w \cdot x + b`.
- Cell 21 (T2): same, generalised to $w_1, \dots, w_6$.

This is the sklearn convention (`coef_` returns the $w_j$, `intercept_` returns $b$), but it is **not** the L11 convention. The student now has to mentally translate every L11 formula on the exam to the lab's notation and back. L11's formula sheet (§8 lines 786–792) is entirely in $a$/$b_j$ notation.

**Cost to the student.** Low-grade chronic friction. Every L11 formula in §3.3, §3.5, §3.6, §3.7, §3.8.1, §8 has to be re-keyed mentally during exam revision. The lab does say "weight, a.k.a. slope" once in cell 4, but never circles back to align the two conventions.

**Suggested fix.** In cell 4 (the warm-up), keep the sklearn `w/b` convention but add: "L11 uses different letters for the same things. The lecture writes the line as `y = a + b·x` where `a` is the intercept and `b` is the slope. Same equation, same two knobs, different letter labels. sklearn returns the slope as `.coef_` (the L11 `b`) and the intercept as `.intercept_` (the L11 `a`). Don't let the notation fool you on the exam."

### Finding 2.5 [P2] Inconsistent "residual" terminology

**Where.** Cell 13 vs cell 19 vs cell 39.

**The issue.**
- Cell 13 (T1 "the concept") defines: $\text{residual}_i = y_i - \hat{y}_i$ ✓ (matches L11 §3.3 line 120).
- Cell 19 (T1 visualisation): "residual (actual − predicted)" ✓ (consistent).
- Cell 39 (T5 gradient descent): defines `error = y_hat - y_gd` — i.e. $\hat y - y$, the **opposite sign** of cell 13's residual. The code comment says "Error of each prediction" with no flag that this is the negated residual.

That sign flip will trip up a student trying to match the gradient-descent error term to the L11 residual. The gradient formula `dw = (2/n) * sum(error * x)` happens to give the right answer because the sign cancels with the minus sign in the update rule, but the conceptual link is broken.

**Suggested fix.** In cell 41 (T5 hint markdown) and cell 42 (T5 solution code), explicitly note: "We use `error = y_hat - y` here rather than the L11 residual $r = y - \hat y$ because it makes the gradient sign work out cleanly. The two differ by a minus sign."

---

## 3. KNOB documentation — pedagogical value

This is the one area where the lab over-delivers, and it's worth saying so before going back to harsh.

**What's right.** Every KNOB block (TEST_SPLIT_RATIO, SPLIT_RANDOM_STATE, POLY_DEGREES_SWEEP, T2_FEATURE_SUBSET, T1_FEATURE, my_profile, GD_LEARNING_RATE, GD_N_EPOCHS) follows the same three-field schema (What it does / Effect / Exam variants). This is *better* than L11 itself in some places — e.g. L11 nowhere quantifies the bowl-vs-cliff failure modes of learning-rate selection, but the GD_LEARNING_RATE KNOB does (cell 40 lines 1275–1283).

**What's missing.** The KNOB blocks aren't tied back to L11 vocabulary. GD_LEARNING_RATE / GD_N_EPOCHS could note "L11 §1 line 27 lists 'learning rate, epoch' as L11-omitted vocabulary — these are the lab's contribution." TEST_SPLIT_RATIO could cite "L11 §6 pitfall #15 — $R^2$ can be **negative on test data**." This is a P2 because the KNOB blocks are excellent in their own right; they just don't bridge to L11.

### Finding 3.1 [P2] KNOB blocks should mention which L11 pitfall / vocabulary item each knob illustrates

**Suggested fix.** Add a fourth field to each KNOB schema: "L11 link" with a §-pointer to the relevant lecture section. Example for GD_LEARNING_RATE: "L11 link: L11 §1 line 27 — gradient descent is L11-omitted, lab-introduced."

---

## 4. Lecture-specific pedagogical traps

### Finding 4.1 [P1] `prior_math_grade` is treated as numeric — but it's the Danish 7-step scale, which is *ordinal categorical*

**Where.** Cell 8 (`make_student_grade_data`) and cell 24 (T2 fit).

**The issue.** `prior_math_grade` is drawn from `DANISH_SCALE = [-3, 0, 2, 4, 7, 10, 12]` and stored as `prior_math.astype(int)`. The T2 multiple regression then treats it as a continuous numeric feature.

That's defensible — Danish grades have a meaningful ordering and are not too far from equally spaced (modulo the -3 ↔ 0 ↔ 2 cluster). But it is also a *teachable moment* for L11 §3.10 (dummy variables for categoricals). The grade scale is genuinely ordinal and the L11 §6 pitfall #4 "dummy-variable trap" is exactly the trap to surface here. The lab does not flag this, does not contrast "what would happen if we one-hot encoded prior_math_grade into 6 dummies?", does not explain why a regression that uses prior_math_grade as a numeric column is making an *equal-spacing assumption* on the grade scale.

**Suggested fix.** In cell 7 (the dataset table) or cell 27 (post-T2 commentary), add a callout: "`prior_math_grade` is technically *ordinal categorical* — its values come from a fixed set (the Danish 7-step scale) and we are assuming the grade differences are equally spaced (i.e. that 4 → 7 is the same jump as 7 → 10). L11 §3.10 discusses an alternative encoding via dummy variables. We go with numeric here for simplicity; on the exam, be ready for the dummy-encoded version."

### Finding 4.2 [P1] T3 overfitting demo uses 1-D synthetic curve, not the student dataset — pedagogically defensible but breaks the lab's narrative

**Where.** Cells 28–32.

**The issue.** T1 and T2 are on the student-grades dataset; T4 returns to the student-grades dataset; **T3 silently switches to a 1-D toy dataset with a sinusoidal true curve**. The lab justifies this in cell 28 ("To make overfitting visible we use a tiny toy dataset...") — and the justification is correct: 360 students × 6 features won't overfit to degree 12 dramatically. But the pedagogical cost is real: the student loses the narrative thread (predict the student grade) for one section and re-acquires it for T4.

More importantly: L11 §3.13 explicitly flags polynomial regression as a *forward-reference to ML Lab 2* (lecture line 416). T3 is *the* moment to land that connection. The lab cell 28 doesn't cite L11 §3.13. It also doesn't make explicit that "polynomial regression is still linear-in-parameters" — L11 §3.13 spends a whole `> EXTENSION` block on that distinction (lecture lines 408–414).

**Suggested fix.** In cell 28, add: "L11 §3.13 forward-references polynomial regression as a 'route to flexibility' from L11; this is the lab where it lands. The key insight is that even with `PolynomialFeatures(degree=d)`, the model is still **linear in its parameters** (each `w_j` enters as a multiplier) — sklearn's `LinearRegression` works unchanged. We switch to a 1-D toy dataset only because the student-grades dataset is too large and too multi-feature for the overfitting collapse to be visually obvious."

### Finding 4.3 [P2] No mention of L11 §3.4 "extrapolation warning" when the lab predicts on `my_profile` in T4

**Where.** Cell 36 (T4 solution).

**The issue.** L11 §3.4 (lecture line 154) hammers on extrapolation: "The intercept is only meaningful if $x = 0$ is inside (or near) the observed data range." Pitfall #7 in L11 §6 generalises this to "any prediction $\hat y$ for an $x$ outside the training range." T4 lets the student type in arbitrary numbers within the documented allowed ranges — but those allowed ranges are the dataset's hard clipping bounds (`study_hours_per_week: 0.5–20.0`), **not** the typical training range. A student plugging in `study_hours_per_week = 20` is at the edge of the training distribution; the prediction will be an extrapolation even though it's within the "allowed range."

L11 §3.4's extrapolation warning is one of the lecture's most repeated cautions, and T4 is exactly the place where a careful exam answer would mention it.

**Suggested fix.** In cell 36's KNOB block for `my_profile`, append a paragraph: "Heads-up: the 'allowed ranges' above are the dataset's *hard* clipping bounds, not the dense training range. A `study_hours_per_week` of `20.0` or a `prior_programming_years` of `6.0` is at the edge of the training distribution, so the prediction there is an *extrapolation* in the L11 §3.4 sense — treat with caution. The model has seen plenty of students at, say, `study_hours_per_week ≈ 8`, but very few at `20`."

### Finding 4.4 [P2] "Class average" in cell 37's feature-contribution chart is *training-set* mean, not full dataset mean — a subtle bias

**Where.** Cell 37 (`avg_profile = X6_train.mean(axis=0)`).

**The issue.** The contribution decomposition `contribs = model_t2.coef_ * (my_x.flatten() - avg_profile)` is mathematically a centered-feature reparametrisation: the prediction equals `(intercept + coef · avg_profile) + sum(contribs)`, where the parenthesised term is the prediction at the average student. This is a clever and useful visualisation. But:
- The label says "grade-point contribution vs the **average** student" (cell 37 line 1208), which to a student reads as "the average student in the dataset" — but the code uses `X6_train.mean(axis=0)`, i.e. the average student *in the training set*.
- The difference is small (80% of the dataset is in training), but it is a difference, and a careful examiner who pulls up the lab will spot the inconsistency.

**Suggested fix.** Either change the label to "grade-point contribution vs the average training student," or change the code to `df[T2_COLS_IN_USE].mean(axis=0)`. The former is the more honest fix — the model was fit on training data, so its centering should reference training-data means.

---

## 5. L11 cross-references that are missing where they should be present

The lab's cell 0 REFERENCES block names L11 once and L10 once. Inside the body of the notebook, L11 is cited zero times. Concrete missed opportunities:

- Cell 11 ("lazy baseline"): could cite L11 §3.5 — "predicting the mean is the SST baseline; every model must beat SST."
- Cell 12 (`lazy_mae`): could cite L11 §3.6 — "the lazy MSE is SST/n; $R^2$ = 1 − model MSE / lazy MSE."
- Cell 13 (T1 concept): should cite L11 §3.2 (slope/intercept names) and §3.3 (residuals).
- Cell 19 (T1 residual plot): should cite L11 §3.3 figure 12 (the canonical residual diagram).
- Cell 21 (T2 concept): should cite L11 §3.7 (adjusted $R^2$).
- Cell 26 (T2 coefficient chart): should cite L11 §3.8–§3.9 (p-values, CIs — which the lab doesn't compute).
- Cell 28 (T3 polynomial): should cite L11 §3.13 (forward-reference) — see Finding 4.2 above.
- Cell 39 (T5 gradient descent): should cite L11 §1 line 27 (the explicit L11-omits-this statement).

### Finding 5.1 [P1] Inline L11 cross-references are absent across the whole notebook

**Suggested fix.** Add one-line `> L11 §X.Y` callouts to each of the cells listed above. Costs minutes; pays back every time the student revises with both files open.

---

## 6. Specific factual / phrasing issues against L11

### Finding 6.1 [P2] Cell 4's "When `x = 0`" intercept description risks the extrapolation trap

**Where.** Cell 4 lines 215–217:
> "`b` (*bias*, a.k.a. *intercept*) is where the line crosses the y-axis — the prediction when `x = 0`."

That's true geometrically but is *exactly* the framing L11 §3.4 (lecture lines 150–154) warns against: "The intercept is only meaningful if $x = 0$ is inside (or near) the observed data range." For the warm-up data (`x = np.linspace(0, 10, 80)`), $x = 0$ is at the boundary, so the intercept *is* defensibly interpolatable here — but the student will then carry the "prediction when x = 0" reading into T1 where Advertising-style features (study_hours, attendance) all have $x = 0$ outside the typical training range.

**Suggested fix.** Append to the bullet: "...the prediction when `x = 0`. Be careful: if `x = 0` is outside the range of your training data, that prediction is an *extrapolation* — see L11 §3.4."

### Finding 6.2 [P2] Cell 13's R² definition uses `MSE_lazy` notation found nowhere in L11

**Where.** Cell 13 lines 505–508 (already quoted in Finding 2.1).

**The issue.** The phrase `MSE_lazy` is the lab's invention. L11 uses SST (sum of squares total) for the same quantity. Internal to the lab this is fine; against L11 it's an extra mental hop.

**Suggested fix.** See Finding 2.1.

### Finding 6.3 [P2] The "snapping" step at the end of T4 has no L11 counterpart and could confuse exam-style "what is the regression prediction?" questions

**Where.** Cell 36 lines 1180–1184.

**The issue.** `my_score = float(model_t2.predict(my_x)[0])` is the regression prediction; `my_grade = int(snap_to_danish(np.array([my_score]))[0])` then snaps to the nearest Danish grade. The lab labels the second as "Danish grade" and presents both. That's fine, but the lab never makes explicit that **the model's actual output is `my_score`**, the continuous score — `my_grade` is a post-hoc classification on top of the regression output. A confused student could think "regression returns a Danish grade" — that's wrong: regression returns a real number; snapping is an extra classification step the lab adds for narrative payoff.

**Suggested fix.** Add a sentence above the print statement: "Note that the model's *actual* prediction is `my_score` — a continuous real number. Snapping to the Danish scale (`my_grade`) is a post-hoc rounding step the lab adds for narrative payoff; it is **not** part of regression. The exam asks for the continuous regression output."

---

## 7. Comparison to L11's own pedagogical scaffolding

L11 has a five-part pedagogical scaffold:
1. **Big-picture analogies** (§2) — 8 named analogies.
2. **Core formal concepts** (§3) — definitions + worked equations.
3. **Algorithms / methods** (§4) — OLS pseudocode + L11-vs-Lab comparison table.
4. **Worked examples** (§5) — 4 fully-expanded numerical examples.
5. **Common pitfalls** (§6) — 16 named exam traps.
6. **Cheat-sheet** (§8) — one-page recap with every analogy callback.

The lab covers (roughly):
- (1) — partially, with the wrong analogy (Finding 1.1).
- (2) — partially, with sklearn-flavoured re-namings (§2 Findings throughout).
- (3) — yes, replaced with sklearn API call sequence.
- (4) — yes, but the student-grades / California-housing examples don't map to L11 §5's soft-drink/bathroom/gender-salary examples.
- (5) — **not at all**. None of L11's 16 pitfalls are flagged in the lab. Pitfalls 1, 2, 3, 7, 12, 13, 14, 15 are *directly applicable* to the lab's content.
- (6) — N/A (the lab has its own summary in cell 45).

### Finding 7.1 [P1] No pitfall-style "common mistakes" section anywhere in the lab

**Suggested fix.** Add a markdown cell after cell 44 (the T5 closing block) titled "Common mistakes to watch for on the exam (cross-references to L11 §6)." Bullet at least:
- "$R^2$ can be negative on a test set" — L11 §6 pitfall #15. The lab's T3 degree-12 overfit comes close to this; flag it.
- "Comparing raw $R^2$ across models with different $p$ is naive — use adjusted $R^2$" — pitfall #3. T1-vs-T2 comparison is exactly the trap.
- "Statistical significance ≠ practical importance" — pitfall #2. Lab doesn't cover p-values but should at least name this trap.
- "Extrapolating beyond the data range" — pitfall #7. T4 my_profile is the trap.
- "L11 does *not* name MSE, RMSE, gradient descent, learning rate, epoch, or polynomial regression. If the exam asks for them by name, the answer is 'covered in ML Lab 2'" — pitfall #12. This is the lab's *raison d'être* and should be stated up front.
- "Misstating the p-value's meaning" — pitfall #14. Lab doesn't compute p-values but the student needs to know this is on the exam.

This is the most cost-effective single pedagogical fix in this review.

---

## 8. Things the lab does well (in fairness)

For balance — the lab is not bad. It is **well-engineered but L11-disconnected**.

- **The Concept → Intuition → Predict → Do → Verify rhythm is excellent** and is closely L11-aligned in spirit (L11 §2 also says "read this first; the formalism is much easier to absorb once you have a picture in your head").
- **The KNOB documentation is exceptionally thorough** — better than most professional codebases I've reviewed in this role. See §3 above.
- **The hints structure (Hint 1 → Hint 2 → Hint 3) is well-thought-through** and matches the lab's stated "try first, then peek" philosophy.
- **T5 (gradient descent from scratch)** is genuinely well-pedagogised — the five-step recipe, the gradient formulas spelled out, the comparison with sklearn's closed-form answer. This is the cell where the lab most clearly fills an L11 gap (L11 §1 line 27 explicitly cedes gradient descent to "ML Lab 2").
- **The synthetic-dataset design** with a known generative formula (cell 8 lines 304–313) is pedagogically excellent — the student can in principle recover the underlying coefficients from the multiple regression, which gives the model a "ground truth" to be measured against.
- **The cell-37 feature-contribution bar chart** is a genuinely insightful visualisation — "why the model predicted X for you" decomposed into per-feature contributions. L11 doesn't have anything like it; it's the lab's own contribution and a good one. (Cf. Finding 4.4 for the training-vs-full-dataset average nit.)
- **The cell-32 polynomial-degree triptych** is *the* visual for L11 §3.13's "more flexibility = more overfit" warning, and is well-executed.

---

## Report to PM

**Assignment recap:** Lab Reviewer #3 (Pedagogical Clarity) for MLLab2-Regression Round 1. Lab notebook `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab2_regression_solution.ipynb` reviewed against lecture `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L11-Regression.md`. Mental model ↔ L11 alignment was the primary lens.

**Status:** **Pass with significant concerns.** The lab is technically correct and well-engineered (KNOBs, hints, narrative structure all good). But it drifts off L11's mental model in load-bearing ways and silently drops about a third of L11's vocabulary. A student who studies for the exam from this lab without re-reading L11 will be missing SST/SSR/SSE, adjusted $R^2$, p-values, confidence intervals, F-statistic, dummy variables, interaction terms, multicollinearity, and the flight-path / light-switch / throttle / two-passports analogies — every one of which is L11 examination material.

**P0 findings (pedagogical):**
1. **Finding 1.1** — Cell 0 cites a *fabricated* L11 analogy ("elastic band", "bendy") that does not exist in L11. Active misinformation that breaks student trust. **Fix:** rewrite cell 0's mental-model paragraph using L11 §2's actual flight-path analogy.
2. **Finding 2.1** — SST / SSE / SSR decomposition (L11's "single most important diagram") is nowhere in the lab. $R^2$ is given as `1 − MSE_model / MSE_lazy` instead of the L11 form `SSR / SST`. **Fix:** in cell 13, add the L11 §3.5 decomposition.
3. **Finding 2.2** — Adjusted $R^2$ is never mentioned, even though T1-vs-T2 is *the* canonical use case. The lab makes the exact "naive $R^2$ comparison" L11 §6 pitfall #3 warns against. **Fix:** in cell 25, name adjusted $R^2$ and contrast it with the held-out-test-set defence the lab implicitly uses.

**P1 findings:**
1. **Finding 1.2** — No dummies, interactions, or multicollinearity anywhere. L11 spends ~30% of slides on these. **Fix:** at minimum, add a "this lab does not cover X, see L11 §3.10–§3.12" signpost. Ideally add a mini-example on `prior_math_grade` as a categorical and a multicollinearity callout on the cell-9 correlation heatmap.
2. **Finding 1.3** — Gradient descent "marble in a bowl" analogy presented without flagging that L11 doesn't cover gradient descent at all. **Fix:** cell 0 and cell 39 should explicitly say "L11 punts gradient descent to this lab."
3. **Finding 2.3** — No p-values, no confidence intervals, no F-statistic. ML Lab 2's scoping note (in L11 §4.2) explains why, but the lab itself doesn't say so. **Fix:** add a signpost in cell 0 and cell 26.
4. **Finding 2.4** — Notation collision (`w/b` vs L11's `a/b`/`b_j`). **Fix:** in cell 4, bridge the two notations once.
5. **Finding 4.1** — `prior_math_grade` is ordinal categorical but treated as numeric without comment. **Fix:** flag it in cell 7 or cell 27.
6. **Finding 4.2** — T3 switch to a 1-D toy dataset breaks the lab's narrative and doesn't connect to L11 §3.13's forward-reference. **Fix:** add the "linear-in-parameters" explanation from L11 §3.13 to cell 28.
7. **Finding 5.1** — Inline L11 cross-references are absent across the entire body of the notebook. **Fix:** add one-line §-pointer callouts to the 8 cells listed in §5 above.
8. **Finding 7.1** — No "common mistakes / pitfalls" section anywhere. Most cost-effective single fix. **Fix:** add a pitfall-cross-reference cell after cell 44 covering L11 §6 pitfalls 2, 3, 7, 12, 14, 15.

**P2 findings:**
1. **Finding 2.5** — Sign convention for residual vs error differs between cells 13/19 (residual = `y − y_hat`) and cells 39/42 (error = `y_hat − y`). Flag explicitly in T5.
2. **Finding 3.1** — KNOB blocks should add an "L11 link" field tying each knob back to a lecture section.
3. **Finding 4.3** — T4 should warn about extrapolation when `my_profile` is at the edge of the "allowed range."
4. **Finding 4.4** — Cell 37 "average student" baseline uses training-set mean but labels it as "the average student" (full dataset implied). Either re-label or re-compute.
5. **Finding 6.1** — Cell 4's "When `x = 0`" intercept description should carry the L11 §3.4 extrapolation warning inline.
6. **Finding 6.2** — `MSE_lazy` notation in cell 13 is the lab's invention; tie back to L11's SST.
7. **Finding 6.3** — T4's `snap_to_danish` step should be flagged as a post-hoc classification on top of regression, not part of regression itself.

**Pedagogical-clarity checklist status (against L11 §2 analogies + §3 vocabulary + §6 pitfalls):**

| L11 element | Lab coverage | Note |
|---|---|---|
| L11 §2 flight-path analogy | **Missing / contradicted** | See Finding 1.1 (P0). |
| L11 §2 shotgun-spread $R^2$ analogy | Missing | Not flagged. |
| L11 §2 dart-throw CI analogy | Missing | Lab doesn't cover CIs. |
| L11 §2 light-switch dummy analogy | Missing | Lab doesn't cover dummies. |
| L11 §2 throttle interaction analogy | Missing | Lab doesn't cover interactions. |
| L11 §2 two-passports multicollinearity | Missing | Lab doesn't cover multicollinearity. |
| L11 §3.2 slope/intercept names ($a, b$) | Renamed to `w, b` without bridge | Finding 2.4. |
| L11 §3.3 residual definition | Present (cell 13) | Sign convention flipped in T5 (Finding 2.5). |
| L11 §3.3 OLS objective | Implicit via sklearn | Closed-form math not named. |
| L11 §3.5 SST/SSE/SSR | **Missing** | Finding 2.1 (P0). |
| L11 §3.6 $R^2$ formula | Re-stated as MSE-ratio | Finding 2.1 (P0). |
| L11 §3.7 adjusted $R^2$ | **Missing** | Finding 2.2 (P0). |
| L11 §3.8 p-value | Missing | Finding 2.3 (P1). |
| L11 §3.8.1 F-statistic | Missing | Finding 2.3 (P1). |
| L11 §3.9 95% CI | Missing | Finding 2.3 (P1). |
| L11 §3.10 dummy variable | Missing | Finding 1.2 (P1). |
| L11 §3.11 interaction term | Missing | Finding 1.2 (P1). |
| L11 §3.12 multicollinearity | Missing | Finding 1.2 (P1). |
| L11 §3.13 linear-in-parameters | Implicit in T3 | Should be named (Finding 4.2). |
| L11 §6 pitfalls list | **Missing entirely** | Finding 7.1 (P1). |

**Acceptance criteria status (re-cast as pedagogical):** None formally defined; this reviewer's working pedagogical acceptance criterion was "after this lab, a student can answer L11-style exam questions on the vocabulary the lab claims to cover." On that criterion: **not met for adjusted $R^2$, SST/SSE/SSR, intercept-as-extrapolation, model-comparison subtleties; met for `LinearRegression.fit()`, MAE/MSE/$R^2$ as test-set metrics, train/test split, polynomial-feature overfitting, gradient descent.**

**DOCUMENT.md audit:** N/A — this is a single-notebook lab review, not a multi-directory feature ship.

**Out-of-scope observations:**
1. L11 itself contains the soft-drink (`SALES ~ ADVT`), house-price-bathroom, and Gender × Experience examples; the lab uses **none** of them. If the lab were re-written to lift even one (say, dummy-encoding `prior_math_grade` mirroring the L11 §5.3 Neighborhood encoding), the L11 ↔ Lab tie would be much tighter. Out-of-scope for this round but worth scheduling.
2. The `variants.md` at `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\MLLab2-Regression\variants.md` was not directly read by this reviewer (out of pedagogical-clarity scope, into "variant coverage" scope); a separate reviewer focused on exam-variant coverage should check that the KNOB blocks actually unlock the variant bank as the lab claims.

**Concerns / risks:**
- **High risk:** the cell-0 fabricated quotes ("elastic band", "bendy") will be discovered by any student who cross-checks with L11. Once they catch one fabrication, trust in the rest of the study pack collapses. Fix this in Round 2 *before* anything else.
- **Medium risk:** a student who studies for the exam from the lab alone (i.e. skips L11) will fail any question on adjusted $R^2$, p-values, CIs, F-statistic, dummies, interactions, or multicollinearity. The lab does not signal that it is intentionally L11-incomplete.
- **Low risk:** the notation mismatch (`w/b` vs L11's `a/b`) is annoying but not load-bearing; a one-sentence bridge in cell 4 fixes it for the rest of the lab.

**What PM should do next:**
1. **Dispatch a fix-cycle engineer** to address the three P0 findings (1.1, 2.1, 2.2) — they are cheap textual fixes that disproportionately raise quality.
2. **Decide policy on Findings 1.2 and 2.3** — does ML Lab 2 cover dummies/interactions/multicollinearity/p-values/CIs at all? If not, the fix is just a signpost; if yes, the fix is content additions. This is a scoping call only PM/owner can make.
3. **Then re-QA** focused on the three P0 fixes and the L11-cross-reference additions (Finding 5.1, Finding 7.1).
4. After Round 2, the lab is plausibly ready for App Tester / Code Reviewer.

**DOCUMENT.md updated:** N/A for QA / Lab Reviewer.
