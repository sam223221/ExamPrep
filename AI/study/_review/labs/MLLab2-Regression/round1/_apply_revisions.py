"""
Apply Round-1 reviewer revisions to lab2_regression_solution.ipynb.

Fixes applied:
  P0 (R1/R4): Cell 0 "OUTPUTS WHEN RUN" -- T4 forecast 7.7/grade 7 -> 9.70/grade 10.
  P0 (R3):    Cell 0 "MENTAL MODEL" -- delete fabricated L11 "elastic band/bendy"
              quotes; rewrite using L11 sec.2 real analogies (flight path,
              residuals, OLS-squaring). Also add SST/SSE/SSR + Adjusted R^2
              section.
  P1 (R2/R4): Add TOY_RANDOM_SEED, TOY_N_TRAIN, TOY_NOISE_STD KNOB blocks
              (referenced in variants.md), wire them through the toy dataset.
  P1 (R2):    Fix POLY_DEGREES_SWEEP KNOB contradiction. Make cell 32 verify
              cell adaptive to len(POLY_DEGREES_SWEEP).
  P0 (R4):    Address Variant 1's "6 R^2 rows" demand -- add POLY_DEGREES_SWEEP_2
              so a single notebook execution does both sweeps.
  P1 (R1):    Compute lazy baseline on the test set, not the full dataset.
"""
import json
from pathlib import Path

NB_PATH = Path(r"c:/Users/samgl/Documents/GitHub/ExamPrep/AI/lab2_regression_solution.ipynb")
nb = json.loads(NB_PATH.read_text(encoding="utf-8"))


def set_source(idx, text):
    """Replace cell idx's source with `text` (splitlines with newlines)."""
    lines = text.splitlines(keepends=True)
    nb["cells"][idx]["source"] = lines
    # Clear outputs so re-execution produces fresh ones; keep cell_type/metadata.
    if nb["cells"][idx]["cell_type"] == "code":
        nb["cells"][idx]["outputs"] = []
        nb["cells"][idx]["execution_count"] = None


# ---------------------------------------------------------------------------
# Cell 0 -- rewrite mental-model and outputs-when-run sections.
# ---------------------------------------------------------------------------
cell0 = """# LAB ML-2: Regression (Linear + Polynomial on student grades) — SOLUTION

## PROBLEM STATEMENT (from `lab2_regression_handout.ipynb`)

> **Question.** Given a student's study habits, can we predict what grade
> they'll get on the final exam?
>
> In this lab you'll build a regression model that predicts a student's
> exam score on the **Danish 7-step scale** (`-3, 00, 02, 4, 7, 10, 12`).
> You'll start with one feature (study hours), then use all six. By the
> end you'll fill in your own habits and see the model's prediction for
> *you*.

The handout walks the student through five guided tasks (T1–T5) plus a
California-housing homework. Every "Concept → Intuition → Predict → Do →
Verify" rhythm and every markdown explainer below is preserved verbatim
from the handout. The TODO cells (T1, T2, T3, T4, T5) are the only cells
that change: each `raise NotImplementedError(...)` is replaced with a
working implementation, with `# KNOB:` blocks documenting every tunable
parameter the exam variants might want to flip.

The five tasks:

- **T1 — Simple linear regression** on `study_hours_per_week` only.
- **T2 — Multiple linear regression** on all six features.
- **T3 — Polynomial sweep + overfitting** on a toy 1-D dataset (default
  degrees `(1, 3, 12)` plus a second sweep `(2, 6, 18)` for variant 1).
- **T4 — Predict your own grade** by filling in `my_profile`.
- **T5 (bonus) — Gradient descent from scratch** on the T1 problem.

## MENTAL MODEL (L11 §2 analogies)

The lab uses the same picture L11 §2 (lecture lines 43–59) does — we are
**not** inventing new analogies, we are reusing the lecture's:

- **Linear regression = a single straight flight path on a 2-D chart of
  cities.** Each city sits at some longitude (x) and altitude (y); the
  flight path is the line. You can't pass over every city exactly, so
  you compromise on the route that *on average* misses by the least
  (L11 §2, lecture line 43).
- **A residual is how far each city sits above or below the flight
  path.** Positive = the city is above the line ($y_i > \\hat y_i$);
  negative = below. The sign matters — the "distance" picture is only
  correct after squaring (L11 §2, lecture line 45).
- **OLS = the flight path that minimises the sum of *squared*
  city-offsets.** Squaring matters: a city 10 km off counts not twice
  but **four times** as much as one 5 km off. OLS therefore weights
  large misses heavily and settles on the line that splits the
  difference between every pull the data exerts (L11 §2, lecture line
  47; L11 §3.3 "OLS-as-squared-penalty").
- **$R^2$ = the share of the data's spread that the flight path
  absorbs.** Total spread = SST; the leftover after fitting = SSE; what
  the line captured = SSR = SST − SSE. Then $R^2 = $ SSR / SST = 1 −
  SSE / SST (L11 §2 "shotgun-spread", §3.5–3.6).
- **Polynomial degree** is not an L11 §2 analogy — L11 forward-references
  polynomial regression as "a route to flexibility" in §3.13. The key
  insight is that even with `PolynomialFeatures(degree=d)`, the model
  is still **linear in its parameters**, so `LinearRegression` works
  unchanged. Higher degree = more flexibility = more risk of memorising
  noise (overfitting).
- **Gradient descent = rolling a marble down a bowl-shaped loss
  surface.** Each step nudges the parameters in the direction the bowl
  is steepest down. This analogy is the **lab's**, not L11's: L11 §1
  (lecture line 27) explicitly punts gradient descent to "ML Lab 2" —
  the iterative-optimisation perspective belongs *here*. L11 treats
  `lm()`/`LinearRegression()` as a closed-form black box only.

## SST / SSE / SSR — the single most important diagram in L11

L11 §3.5 calls the sum-of-squares decomposition "the single most
important diagram in the lecture" (lecture line 186). Three pieces:

- **SST = $\\sum_i (y_i - \\bar y)^2$** — Total Sum of Squares. The
  variability you face *before* any model, i.e. how badly the
  "predict-the-mean" baseline misses. Every model must beat SST.
- **SSE = $\\sum_i (y_i - \\hat y_i)^2$** — Error Sum of Squares. What's
  left *after* the model: the squared residuals OLS minimises.
- **SSR = SST − SSE = $\\sum_i (\\hat y_i - \\bar y)^2$** — Regression
  Sum of Squares. What the model managed to *explain*.

Then $\\boxed{R^2 = \\dfrac{\\text{SSR}}{\\text{SST}} = 1 - \\dfrac{\\text{SSE}}{\\text{SST}}}$.

The lab also writes $R^2$ as $1 - \\text{MSE}_\\text{model}/\\text{MSE}_\\text{lazy}$
in cell 13 — same quantity, since $\\text{MSE} = \\text{SSE}/n$ and
$\\text{MSE}_\\text{lazy} = \\text{SST}/n$ (the $n$'s cancel). Memorise the
L11 form; the lab's MSE form is just the sklearn-friendly renaming.

## Adjusted $R^2$ — the right metric for comparing models with different $p$

L11 §3.7 (lecture lines 220–241) warns: $R^2$ *never decreases* when you
add a predictor, even a useless one. Comparing raw $R^2$ across models
with different numbers of predictors is therefore naive. Use:

$$R^2_\\text{adj} = 1 - \\dfrac{n-1}{n-p-1}\\,(1 - R^2),$$

where $n$ is the sample size and $p$ is the number of predictors
(intercept not counted). The multiplier $(n-1)/(n-p-1)$ swells above 1
as $p$ grows, so a useless extra predictor barely moves $R^2$ but
*lowers* $R^2_\\text{adj}$. The lab compares T1 (p = 1) and T2 (p = 6) on
the held-out *test* set, which is a different (and equally valid)
defence against the same problem — a useless predictor will fail to
generalise and so will hurt test-set $R^2$ on its own. Both
approaches are exam-relevant. The lab's T2 sanity check prints the
adjusted-$R^2$ for both T1 and T2 alongside the raw values so you can
see the penalty in action.

## REFERENCES

- **L11 Regression** — `study/lectures/L11-Regression.md`
  (flight-path analogy §2; OLS / residual / SST-SSE-SSR §3.3–§3.6;
  adjusted $R^2$ §3.7; dummy / interaction / multicollinearity
  §3.10–§3.12 — **not** covered in this lab; polynomial regression
  forward-reference §3.13).
  Important: L11 itself does **not** cover gradient descent, MSE/RMSE
  by name, learning rate, or epochs. Those are this lab's contribution.
- **L10 Intro to ML** — `study/lectures/L10-Intro-to-ML.md`
  (train/test split, overfitting, MAE/MSE/R² as evaluation metrics).
- **Glossary** — `study/_shared/glossary.md`: *linear regression*,
  *polynomial regression*, *ordinary least squares*, *overfitting*,
  *train/test split*, *R²*, *MSE*, *MAE*, *gradient descent*,
  *learning rate*.

## HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS

See `study/_exam/MLLab2-Regression/variants.md` for the full curated
variant bank. Quick guide:

1. **Polynomial-degree sweep (variant 1):** the notebook ships with
   *two* sweeps so one execution covers the variant's "six rows"
   requirement: `POLY_DEGREES_SWEEP` (default `(1, 3, 12)`) and
   `POLY_DEGREES_SWEEP_2` (default `(2, 6, 18)`). Change either tuple
   to any length; the verify cell now resizes its subplot grid
   automatically. The toy dataset itself is governed by
   `TOY_RANDOM_SEED`, `TOY_N_TRAIN`, `TOY_NOISE_STD`.
2. **Drop a feature from the multiple regression (variant 2):** change
   the KNOB `T2_FEATURE_SUBSET` in the T2 cell. Allowed values:
   - `"all"` — default; uses every column in `FEATURE_COLS`.
   - `"drop_study_hours"` — drops `study_hours_per_week`.
   - any explicit Python list of column names (subset of `FEATURE_COLS`).
3. **Predict a new student row (variant 3):** rewrite the `my_profile`
   dict in the T4 cell with the variant's values. The dict's KNOB
   block documents the allowed range for each entry.
4. **Bonus — gradient descent tuning (variant 4):** change
   `GD_LEARNING_RATE` (small → slow convergence; large → instability)
   and/or `GD_N_EPOCHS` in the T5 prep cell.
5. **Bonus — split ratio (variant 5):** change `TEST_SPLIT_RATIO` at
   the top of T1; T2 reuses the same constant so the comparison stays
   apples-to-apples.

Every KNOB ships with its own `# KNOB:` block explaining default,
allowed range, the effect, and which variant the knob is for.

## OUTPUTS WHEN RUN

Running every cell top-to-bottom produces:

- T1 sanity check: `MAE ≈ 1.54, MSE ≈ 3.5, R² ≈ 0.32` (1-feature model
  beats the lazy baseline by ~0.3 grade points).
- T2 sanity check: `MAE ≈ 0.85, MSE ≈ 1.20, R² ≈ 0.77` (6-feature
  model adds ~0.45 R² over T1); adjusted-$R^2$ also printed.
- T3 sanity check: **two** sweeps printed. Default sweep `(1, 3, 12)`:
  degree 1 underfits (~0.3 R²), degree 3 fits well (~0.87 R²),
  degree 12 overfits dramatically (train R² ≈ 1.0, test R² collapses
  below 0.6). Second sweep `(2, 6, 18)`: degree 2 underfits, degree 6
  fits well, degree 18 overfits even more catastrophically. Six rows
  in the combined table — variant 1's requested output.
- T4 sample prediction for the default `my_profile`: `final_score ≈ 9.70`,
  snapped Danish grade `10`.
- T5 sanity check: `|Δw| < 0.05, |Δb| < 0.05` versus sklearn's
  closed-form answer; loss curve drops monotonically.
- Several matplotlib figures (line fits, residuals, coefficient bar
  charts, the polynomial-degree triptychs for both sweeps, the
  gradient-descent loss curve, and a feature-contribution chart for
  the student profile).

## ENTRY POINT: yes

A `.ipynb` is always an entry point. The Verifier executes the whole
notebook via `py -3.12 -m jupyter nbconvert --to notebook --execute
--inplace=false`; every cell must succeed without raising.
"""
set_source(0, cell0)


# ---------------------------------------------------------------------------
# Cell 8 -- dataset + global KNOBs. Add TOY_* knobs; clean up POLY_DEGREES_SWEEP
# language (resolve "more degrees still works" vs "panel resizes" contradiction);
# add POLY_DEGREES_SWEEP_2.
# ---------------------------------------------------------------------------
cell8 = """# --- Build the dataset. Just run this cell. ---

DANISH_SCALE = np.array([-3, 0, 2, 4, 7, 10, 12], dtype=float)

def snap_to_danish(score):
    \"\"\"Round each score to the nearest Danish grade in {-3, 0, 2, 4, 7, 10, 12}.\"\"\"
    score = np.asarray(score, dtype=float)
    return DANISH_SCALE[np.argmin(np.abs(score[..., None] - DANISH_SCALE), axis=-1)]

def make_student_grade_data(n_students=360, random_state=42):
    rng = np.random.default_rng(random_state)
    study        = np.clip(rng.normal(8.0,  3.5, n_students), 0.5, 20.0)
    attendance   = np.clip(rng.normal(82.0, 12.0, n_students), 40.0, 100.0)
    prior_math   = rng.choice(DANISH_SCALE, size=n_students,
                              p=[0.05, 0.10, 0.18, 0.25, 0.22, 0.15, 0.05])
    sleep        = np.clip(rng.normal(7.0, 1.2, n_students), 3.0, 10.0)
    exercises    = rng.integers(0, 11, size=n_students).astype(int)
    prog_years   = np.clip(rng.exponential(1.2, n_students), 0.0, 6.0)

    # Hidden generative formula — don't peek if you want the exercise to be honest!
    score = (
        -3.0
        + 0.45 * study
        + 0.025 * attendance
        + 0.35 * prior_math
        - 0.30 * (sleep - 7.2) ** 2
        + 0.18 * exercises
        + 0.30 * prog_years
        + rng.normal(0.0, 1.0, n_students)
    )
    score = np.clip(score, -3.0, 12.0)

    df = pd.DataFrame({
        'study_hours_per_week':     np.round(study, 1),
        'attendance_rate_pct':      np.round(attendance, 1),
        'prior_math_grade':         prior_math.astype(int),
        'sleep_hours':              np.round(sleep, 1),
        'exercises_completed':      exercises,
        'prior_programming_years':  np.round(prog_years, 1),
        'final_score':              np.round(score, 2),
        'final_grade':              snap_to_danish(score).astype(int),
    })
    return df

FEATURE_COLS = [
    'study_hours_per_week',
    'attendance_rate_pct',
    'prior_math_grade',
    'sleep_hours',
    'exercises_completed',
    'prior_programming_years',
]

df = make_student_grade_data()
print(f'Dataset shape: {df.shape}')
df.head()


# ---------------------------------------------------------------------------
# Global KNOBs read by the rest of the notebook.
# ---------------------------------------------------------------------------

# KNOB: TEST_SPLIT_RATIO (default=0.2, range=(0.1, 0.5))
#   What it does: fraction of the 360-student dataset reserved for the
#     test split in T1, T2, and the T2 feature-drop variant.
#   Effect: smaller test fraction = more training data = lower variance
#     in coefficients but a noisier test-R^2 estimate. The sanity-check
#     tolerances assume 0.2.
#   Exam variants: variant 5 sets this to 0.5 to halve the training set
#     and watch R^2 degrade. Keep at 0.2 for variants 1-3.
TEST_SPLIT_RATIO = 0.2

# KNOB: SPLIT_RANDOM_STATE (default=42, allowed=any int)
#   What it does: seed handed to sklearn's train_test_split so the same
#     students go into train and test across re-runs.
#   Effect: changing the seed reshuffles the split — useful as a quick
#     sanity check that results are not seed-cherry-picked.
#   Exam variants: keep at 42 for every variant unless the variant text
#     explicitly says "with a different seed".
SPLIT_RANDOM_STATE = 42

# KNOB: POLY_DEGREES_SWEEP (default=(1, 3, 12), allowed=tuple of positive ints,
#                           any length >= 1)
#   What it does: the polynomial degrees evaluated in T3's *first* toy
#     overfitting sweep.
#   Effect: low degrees underfit, mid degrees fit well, high degrees
#     overfit. The verify cell (cell 32) reads len(POLY_DEGREES_SWEEP)
#     at runtime and draws a 1 x len() subplot grid — no manual
#     bookkeeping needed when you change the tuple length.
#   Exam variants: variant 1 keeps this at (1, 3, 12) for the
#     underfit -> goodfit -> overfit baseline; the second sweep
#     (POLY_DEGREES_SWEEP_2 below) does the (2, 6, 18) replay, so
#     a single notebook execution prints all six (degree, train, test)
#     rows.
POLY_DEGREES_SWEEP = (1, 3, 12)

# KNOB: POLY_DEGREES_SWEEP_2 (default=(2, 6, 18), allowed=tuple of positive ints,
#                              any length >= 1)
#   What it does: a *second* polynomial sweep run on the same toy
#     dataset right after the first one. Lets variant 1's "report six
#     (degree, train_R^2, test_R^2) rows" answer come out of a single
#     notebook execution.
#   Effect: identical role to POLY_DEGREES_SWEEP — same fit/score
#     loop, same verify plot, just at different degrees. Set to an
#     empty tuple () if you want to skip the second sweep.
#   Exam variants: variant 1 reads this as (2, 6, 18) to confirm the
#     underfit -> goodfit -> overfit progression at a different scale.
POLY_DEGREES_SWEEP_2 = (2, 6, 18)

# KNOB: TOY_RANDOM_SEED (default=7, allowed=any int)
#   What it does: seed for the toy 1-D dataset used by T3. Controls
#     both training-point noise and test-point noise.
#   Effect: different seeds reshuffle the noise sprinkled around the
#     true wiggle curve. R^2 numbers will shift slightly but the
#     underfit -> goodfit -> overfit *pattern* across degrees is robust
#     to the seed.
#   Exam variants: variant 1 typically keeps this at 7 so the
#     comparison between the two sweeps is apples-to-apples.
TOY_RANDOM_SEED = 7

# KNOB: TOY_N_TRAIN (default=14, allowed=int in roughly 8..200)
#   What it does: number of training points in T3's toy dataset.
#     Few training points + a flexible model is the recipe that makes
#     overfitting dramatic.
#   Effect: more train points -> harder to overfit at high degree, so
#     the train/test gap at degree 12 shrinks. With ~50 points even
#     degree 18 fits okay.
#   Exam variants: variant 1 keeps this at 14 — raising it would
#     suppress the overfitting payoff. The test set is fixed at 40
#     points regardless.
TOY_N_TRAIN = 14

# KNOB: TOY_NOISE_STD (default=0.45, allowed=float in 0.0..2.0)
#   What it does: standard deviation of the Gaussian noise added to
#     both the toy training and toy test points.
#   Effect: low noise -> the true wiggle is easy to see and even
#     simple polynomials do well; high noise -> all degrees do worse
#     on test, and overfit-versus-fit signals get harder to separate.
#   Exam variants: variant 1 keeps this at 0.45 so the pattern is
#     dramatic but not pathological.
TOY_NOISE_STD = 0.45

# KNOB: T2_FEATURE_SUBSET (default="all",
#                          allowed={"all", "drop_study_hours",
#                                   list of column names from FEATURE_COLS})
#   What it does: chooses which columns of the dataset feed the T2
#     multiple regression.
#   Effect:
#     - "all" -> all six features (the default; matches the handout
#       sanity check).
#     - "drop_study_hours" -> the five features other than
#       study_hours_per_week. R^2 drops by ~0.2-0.3 because the strongest
#       single signal is removed.
#     - explicit list -> any subset of FEATURE_COLS; T2 still runs but
#       the sanity check's expected values will not match.
#   Exam variants: variant 2 uses "drop_study_hours".
T2_FEATURE_SUBSET = \"all\"
"""
set_source(8, cell8)


# ---------------------------------------------------------------------------
# Cell 12 -- compute lazy baseline on full dataset (kept for the
# "predict-the-mean" picture) but also stash test-set lazy baseline for
# honest comparison. Cells 17/18/25 use the test-set version.
# ---------------------------------------------------------------------------
cell12 = """# --- The lazy predictor and its error. ---

# The classroom-friendly picture: predict the overall mean for every
# row. This is the *full-dataset* lazy baseline, which doubles as L11's
# SST/n proxy (predict-the-mean is the SST baseline; lecture lines
# 163–167).
lazy_prediction = df['final_score'].mean()
lazy_mae = mean_absolute_error(df['final_score'], [lazy_prediction] * len(df))

print(f'Lazy predictor always guesses: {lazy_prediction:.2f}')
print(f'Lazy predictor MAE (whole dataset): {lazy_mae:.2f}  <- the bar to beat')

# For the honest T1/T2 comparisons we need a lazy baseline computed on
# the **test** split (predicting y_train.mean() for every y_test student).
# The split happens in cell 17; we store the test-set lazy MAE there.

fig, ax = plt.subplots(figsize=(8, 4.2))
ax.scatter(df['study_hours_per_week'], df['final_score'],
           s=22, alpha=0.45, color=COLORS['slate'], label='actual scores')
ax.axhline(lazy_prediction, color=COLORS['red'], ls='--', lw=2,
           label=f'lazy prediction = {lazy_prediction:.2f}')
ax.set_xlabel('study_hours_per_week'); ax.set_ylabel('final_score')
ax.set_title('The lazy predictor: one flat line, ignores all features')
ax.legend()
plt.show()
"""
set_source(12, cell12)


# ---------------------------------------------------------------------------
# Cell 17 -- T1 solution. Add test-set lazy baseline computation right after
# the split (used by cell 18 sanity check).
# ---------------------------------------------------------------------------
cell17 = """##############################################################
###          T1 -- Simple linear regression (SOLUTION)     ###
##############################################################
# Required variables:
#   X1, y, X1_train, X1_test, y_train, y_test,
#   model_t1, y_pred_t1, mae_t1, mse_t1, r2_t1
#
# Strategy: the five-step recipe from the markdown above. The only
# subtleties are (a) X must be 2-D for sklearn even with one feature
# (we use the double-bracket DataFrame idiom), and (b) reading the
# TEST_SPLIT_RATIO / SPLIT_RANDOM_STATE KNOBs declared in the dataset
# cell so a variant that flips the split ratio still works without
# editing this cell.

# KNOB: T1_FEATURE (default='study_hours_per_week', allowed=any column of FEATURE_COLS)
#   What it does: the single feature used by the one-feature regression.
#   Effect: study_hours_per_week is the strongest single predictor and
#     hits the sanity-check window (R^2 ~ 0.32). Changing to a weaker
#     feature (e.g. sleep_hours) will produce a much lower R^2 -- which
#     is itself an instructive variant if the exam asks "which single
#     feature carries the most signal?".
#   Exam variants: variant 2 inspects which feature dominates AFTER
#     dropping study_hours from T2; if you want to repeat the analysis
#     for T1 you can swap this KNOB to the runner-up.
T1_FEATURE = 'study_hours_per_week'

X1 = df[[T1_FEATURE]].values  # shape (n, 1) -- sklearn wants 2-D inputs
y = df['final_score'].values  # shape (n,)   -- the regression target

# Single split shared across T1 / T2 / T2-dropped so R^2 comparisons are
# apples to apples (same students in test set for every model).
X1_train, X1_test, y_train, y_test = train_test_split(
    X1, y,
    test_size=TEST_SPLIT_RATIO,
    random_state=SPLIT_RANDOM_STATE,
)

# Honest lazy baseline: predict y_train.mean() for every test student.
# This is what cell 18's "your model beats baseline by X" line compares to.
lazy_pred_test = float(np.mean(y_train))
lazy_mae_test = mean_absolute_error(y_test, [lazy_pred_test] * len(y_test))

model_t1 = LinearRegression()
model_t1.fit(X1_train, y_train)

# Honest grading: predict on the held-out test split only.
y_pred_t1 = model_t1.predict(X1_test)
mae_t1 = mean_absolute_error(y_test, y_pred_t1)
mse_t1 = mean_squared_error(y_test, y_pred_t1)
r2_t1 = r2_score(y_test, y_pred_t1)

print(f'Learned line:  final_score = {model_t1.coef_[0]:.3f} * {T1_FEATURE}'
      f' + {model_t1.intercept_:.3f}')
print(f'T1 metrics:  MAE = {mae_t1:.3f}   MSE = {mse_t1:.3f}   R^2 = {r2_t1:.3f}')
print(f'Test-set lazy baseline (predict y_train.mean): MAE = {lazy_mae_test:.3f}')
"""
set_source(17, cell17)


# ---------------------------------------------------------------------------
# Cell 18 -- update sanity check to use test-set lazy MAE.
# ---------------------------------------------------------------------------
cell18 = """# --- Sanity check for T1. Do NOT edit this cell. ---

print(f'MAE = {mae_t1:.2f}   (expected ~1.54, anything in 1.35–1.70 is fine)')
print(f'MSE = {mse_t1:.2f}   (expected ~3.5,  anything in 3.0–4.3 is fine)')
print(f'R^2 = {r2_t1:.3f}  (expected ~0.319, anything in 0.25–0.40 is fine)')
print()
# Use the honest test-set lazy baseline (predict y_train.mean for every
# y_test student) — not the full-dataset lazy_mae from cell 12. That one
# was the picture-friendly version; for an apples-to-apples comparison
# the baseline must be evaluated on the same students the model is.
print(f'Lazy baseline MAE on test set: {lazy_mae_test:.2f}.')
improvement = lazy_mae_test - mae_t1
print(f'Your model beats the test-set baseline by {improvement:+.2f} grade points.')
print(f'(For reference, cell 12 reported {lazy_mae:.2f} on the full dataset —'
      f' that figure is the SST/n proxy from L11 §3.5, not a fair model comparison.)')

# If your numbers are far off, check:
#   * Did you pass `random_state=42` to train_test_split? (You must.)
#   * Did you fit on *train* and predict on *test*, not the other way?
#   * Did you call .values on the DataFrame columns so X1 is a NumPy array
#     of shape (n, 1) — not a 1-D array?
"""
set_source(18, cell18)


# ---------------------------------------------------------------------------
# Cell 25 -- T2 sanity check. Add adjusted-R^2 alongside raw R^2.
# ---------------------------------------------------------------------------
cell25 = """# --- Sanity check for T2. Do NOT edit. ---

print(f'MAE = {mae_t2:.2f}   (expected ~0.85, anything in 0.70–1.05 is fine)')
print(f'MSE = {mse_t2:.2f}   (expected ~1.20, anything in 0.90–1.60 is fine)')
print(f'R^2 = {r2_t2:.3f}  (expected ~0.767, anything in 0.70–0.82 is fine)')
print()

# Adjusted R^2 (L11 §3.7, lecture lines 220–241):
#   R^2_adj = 1 - (n - 1) / (n - p - 1) * (1 - R^2)
# n is the test-set size; p is the number of predictors (intercept
# excluded). This is the right metric for comparing models with
# different p — raw R^2 never decreases when you add a predictor,
# adjusted R^2 *can*.
n_test = len(y_test)
p_t1 = 1                          # T1 used only T1_FEATURE
p_t2 = len(T2_COLS_IN_USE)        # T2 used however many columns the KNOB resolved to
adj_r2_t1 = 1.0 - (n_test - 1) / (n_test - p_t1 - 1) * (1.0 - r2_t1)
adj_r2_t2 = 1.0 - (n_test - 1) / (n_test - p_t2 - 1) * (1.0 - r2_t2)

print(f'T1 (p={p_t1}) raw R^2 = {r2_t1:.3f}   adjusted R^2 = {adj_r2_t1:.3f}')
print(f'T2 (p={p_t2}) raw R^2 = {r2_t2:.3f}   adjusted R^2 = {adj_r2_t2:.3f}')
print(f'Raw R^2 jump:      {r2_t2 - r2_t1:+.3f}')
print(f'Adjusted R^2 jump: {adj_r2_t2 - adj_r2_t1:+.3f}  '
      f'(the honest comparison — more features pay off only if this is positive too)')

# If your numbers are far off, check:
#   * Did you use `FEATURE_COLS` (all six), not a subset?
#   * Did you pass `random_state=42` again?
#   * Are you fitting on X6_train and predicting on X6_test (not X1_*)?
"""
set_source(25, cell25)


# ---------------------------------------------------------------------------
# Cell 29 -- toy dataset construction. Wire TOY_* KNOBs through.
# ---------------------------------------------------------------------------
cell29 = """# --- Build a small 1-D toy dataset so overfitting is visually obvious. ---

# The TOY_RANDOM_SEED / TOY_N_TRAIN / TOY_NOISE_STD KNOBs are declared
# in cell 8 alongside the polynomial-sweep knobs. Variant 1 may keep
# them at their defaults; advanced variants can perturb them to study
# the seed/size/noise sensitivity of the overfitting collapse.
toy_rng = np.random.default_rng(TOY_RANDOM_SEED)
true_curve = lambda x: 2.5 + 1.2 * np.sin(1.7 * x) + 0.35 * x

# Training points: TOY_N_TRAIN evenly spaced on [-2.5, 2.5], noise std =
# TOY_NOISE_STD. Few training points + a flexible model is the recipe
# that makes overfitting dramatic.
x_train_toy = np.linspace(-2.5, 2.5, TOY_N_TRAIN)
y_train_toy = true_curve(x_train_toy) + toy_rng.normal(0, TOY_NOISE_STD, TOY_N_TRAIN)

# 40 interior test points, offset so they fall between the training points.
# The test set size is kept fixed (40) regardless of TOY_N_TRAIN so the
# test-R^2 estimate variance stays comparable across variants.
offset = (5.0 / max(TOY_N_TRAIN, 2)) * 0.5
x_test_toy = np.linspace(-2.5 + offset, 2.5 - offset, 40)
y_test_toy = true_curve(x_test_toy) + toy_rng.normal(0, TOY_NOISE_STD, 40)

# Dense grid for drawing fitted curves smoothly. Slightly wider than the
# data range so the polynomial wings are visible at the edges.
x_grid = np.linspace(-2.6, 2.6, 300)

fig, ax = plt.subplots(figsize=(8.5, 4.2))
ax.scatter(x_train_toy, y_train_toy, s=58, color=COLORS['teal'],
           label=f'train ({TOY_N_TRAIN} points)')
ax.scatter(x_test_toy, y_test_toy, s=26, marker='s', alpha=0.55,
           color=COLORS['orange'], label='test (40 points)')
ax.plot(x_grid, true_curve(x_grid), color=COLORS['slate'], ls='--', lw=1.2,
        label='true curve (hidden from models)')
ax.set_xlabel('x'); ax.set_ylabel('y')
ax.set_title(f'Toy dataset — seed={TOY_RANDOM_SEED}, noise std={TOY_NOISE_STD}')
ax.legend()
plt.show()
"""
set_source(29, cell29)


# ---------------------------------------------------------------------------
# Cell 31 -- T3 solution. Helper function so we can run two sweeps cleanly.
# ---------------------------------------------------------------------------
cell31 = """##############################################################
###            T3 -- Overfitting sweep (SOLUTION)          ###
##############################################################
# Required variables:
#   toy_records  -- list of (degree, train_r2, test_r2) tuples for the
#                   default sweep (POLY_DEGREES_SWEEP)
#   toy_fits     -- dict mapping degree to (poly_object, fitted_model)
#                   for the default sweep
#   toy_records2 -- same shape as toy_records but for POLY_DEGREES_SWEEP_2
#   toy_fits2    -- same shape as toy_fits but for POLY_DEGREES_SWEEP_2
#
# Loop over POLY_DEGREES_SWEEP, then over POLY_DEGREES_SWEEP_2. For
# each degree we: expand the 1-D toy x into polynomial columns x, x^2,
# ... x^d; fit a LinearRegression on those columns; score R^2 on the
# same train split and on the held-out test split. The gap
# (train_r2 - test_r2) is the overfitting signal -- nearly zero for
# the right degree, large for the over-flexible model.

def _run_poly_sweep(degrees):
    \"\"\"Run one full polynomial-degree sweep on the toy dataset.

    Returns (records, fits) where records is a list of
    (degree, train_r2, test_r2) tuples and fits is a dict
    mapping degree to (PolynomialFeatures, fitted LinearRegression).
    \"\"\"
    records = []
    fits = {}
    for d in degrees:
        # PolynomialFeatures(degree=d) expands one column x into x, x^2, ..., x^d.
        # include_bias=False because LinearRegression already learns its
        # own intercept; including a bias column would be redundant.
        poly_d = PolynomialFeatures(degree=d, include_bias=False)

        # fit_transform learns the expansion (which power columns to
        # emit) AND applies it; transform applies the SAME expansion
        # to test data.
        Xtr = poly_d.fit_transform(x_train_toy.reshape(-1, 1))
        Xte = poly_d.transform(x_test_toy.reshape(-1, 1))

        m = LinearRegression().fit(Xtr, y_train_toy)

        # Two R^2 scores: train (how well it fits points it saw) and test
        # (how well it generalises). The gap is the diagnostic.
        train_r2 = r2_score(y_train_toy, m.predict(Xtr))
        test_r2 = r2_score(y_test_toy, m.predict(Xte))

        records.append((d, train_r2, test_r2))
        fits[d] = (poly_d, m)
    return records, fits


toy_records, toy_fits = _run_poly_sweep(POLY_DEGREES_SWEEP)

# Second sweep, possibly empty if the variant disabled it.
toy_records2, toy_fits2 = _run_poly_sweep(POLY_DEGREES_SWEEP_2)

# Quick text summary so the printout is intelligible even if the
# verify cell's plotting fails. Variant 1 asks for "six rows" — we
# print both sweeps in one table.
print('Polynomial degree sweep #1 (POLY_DEGREES_SWEEP):')
for d, tr, te in toy_records:
    print(f'  degree {d:>2d}:  train R^2 = {tr:6.3f}   test R^2 = {te:6.3f}'
          f'   gap = {tr - te:+6.3f}')
if toy_records2:
    print('Polynomial degree sweep #2 (POLY_DEGREES_SWEEP_2):')
    for d, tr, te in toy_records2:
        print(f'  degree {d:>2d}:  train R^2 = {tr:6.3f}   test R^2 = {te:6.3f}'
              f'   gap = {tr - te:+6.3f}')
"""
set_source(31, cell31)


# ---------------------------------------------------------------------------
# Cell 32 -- T3 verify. Make subplot grid adaptive; draw both sweeps.
# ---------------------------------------------------------------------------
cell32 = """# --- Sanity check for T3 + side-by-side picture(s) of all fits. ---

print(f\"{'sweep':>8s}  {'degree':>8s}  {'train R^2':>10s}  {'test R^2':>10s}  {'gap':>8s}\")
for d, tr, te in toy_records:
    print(f'{\"#1\":>8s}  {d:>8d}  {tr:>10.3f}  {te:>10.3f}  {tr - te:>+8.3f}')
for d, tr, te in toy_records2:
    print(f'{\"#2\":>8s}  {d:>8d}  {tr:>10.3f}  {te:>10.3f}  {tr - te:>+8.3f}')

print()
print('Expected patterns (default knobs):')
print('  Sweep #1 (1, 3, 12): degree 1 R^2 ~ 0.2–0.4 (underfit), degree 3 ~ 0.85–0.90')
print('                       (good fit), degree 12 train near 1.0 / test much lower (overfit).')
print('  Sweep #2 (2, 6, 18): same underfit -> goodfit -> overfit pattern at higher scale.')


def _plot_sweep(records, fits, sweep_label):
    \"\"\"Draw one 1 x N panel for a single sweep, N = len(records).

    Adapts to any sweep length — no hard-coded 3.
    \"\"\"
    if not records:
        return
    n_panels = len(records)
    fig, axes = plt.subplots(1, n_panels,
                             figsize=(5.0 * n_panels, 4.4),
                             sharey=True, squeeze=False)
    axes = axes[0]
    x_plot_grid = np.linspace(-2.6, 2.6, 300)
    for ax, (d, tr, te) in zip(axes, records):
        poly_d, m = fits[d]
        y_fit = m.predict(poly_d.transform(x_plot_grid.reshape(-1, 1)))
        ax.scatter(x_train_toy, y_train_toy, s=30, color=COLORS['teal'], label='train')
        ax.scatter(x_test_toy, y_test_toy, s=55, marker='s',
                   color=COLORS['orange'], label='test')
        ax.plot(x_plot_grid, y_fit, color=COLORS['red'], lw=2,
                label=f'degree {d} fit')
        ax.plot(x_plot_grid, true_curve(x_plot_grid), color=COLORS['slate'],
                ls='--', lw=1, label='truth')
        ax.set_title(f'degree {d}  |  train R^2={tr:.2f}, test R^2={te:.2f}')
        ax.set_xlabel('x')
        if ax is axes[0]:
            ax.set_ylabel('y')
        # ylim chosen from the **data** with a small buffer, then loosened
        # slightly toward the fit if it stays civil. A divergent very-high-
        # degree fit (e.g. degree 18 on 14 train points) will blow up far
        # outside the data range — clamping to a sensible window keeps the
        # picture readable while the printed table still tells the true
        # numerical story (test R^2 in the thousands of negative).
        y_data_lo = float(min(y_train_toy.min(), y_test_toy.min())) - 0.5
        y_data_hi = float(max(y_train_toy.max(), y_test_toy.max())) + 0.5
        # Compute the fit's range only on x within the data envelope (not
        # the wide x_plot_grid edges where high-degree wings explode).
        in_envelope = (x_plot_grid >= -2.5) & (x_plot_grid <= 2.5)
        if in_envelope.any():
            y_fit_lo = float(y_fit[in_envelope].min())
            y_fit_hi = float(y_fit[in_envelope].max())
            y_lo = min(y_data_lo, max(y_fit_lo, y_data_lo - 3.0))
            y_hi = max(y_data_hi, min(y_fit_hi, y_data_hi + 3.0))
        else:
            y_lo, y_hi = y_data_lo, y_data_hi
        ax.set_ylim(y_lo, y_hi)
    axes[0].legend(loc='lower right', fontsize=9)
    fig.suptitle(f'Polynomial sweep {sweep_label}', y=1.02)
    plt.tight_layout(); plt.show()


_plot_sweep(toy_records, toy_fits, '#1 (POLY_DEGREES_SWEEP)')
_plot_sweep(toy_records2, toy_fits2, '#2 (POLY_DEGREES_SWEEP_2)')
"""
set_source(32, cell32)


NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
print("Notebook revised successfully.")
print(f"Wrote {NB_PATH}")
