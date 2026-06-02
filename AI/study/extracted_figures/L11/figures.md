# L11 — Regression: Figure Catalogue

Source PDF: `Lecture11-Regression.pdf` (49 slides total).
Extraction method: PyMuPDF (`fitz`) embedded-image extraction. 36 raster images were lifted.

The "verdict" column is one of:
- **USE** — embedded in `study/lectures/L11-Regression.md` at the relevant section, as-is.
- **REWORK** — informative but cluttered / low-res / partially decorative; embedded **and** supplemented in prose or a clearer in-text recreation.
- **SKIP** — decorative or non-informational (stock photo, chalkboard wallpaper, book cover, slide-template ornament). Skipped figures are not embedded in the chapter, but every skip is justified below.

| # | File | Page | Caption / content | Verdict | Rationale |
|---|------|------|-------------------|---------|-----------|
| 01 | `fig01-page01-img1.png` | 1 | Tiny black rectangle (slide template ornament, ~527 bytes). | SKIP | Decorative title-slide template element with no information content. |
| 02 | `fig02-page02-img1.jpeg` | 2 | Stock photo: blackboard covered in unrelated physics/math scribbles ("What is a model?" slide background). | SKIP | Decorative stock photo; does not depict any regression concept. |
| 03 | `fig03-page03-img1.jpeg` | 3 | Stock photo: wooden mannequin with a question-mark speech bubble ("Why do we need a model?" slide background). | SKIP | Pure stage-dressing. |
| 04 | `fig04-page04-img1.png` | 4 | A tiny data table showing the first nine rows of the soft-drink advertising dataset (Sales / Advt columns). | USE | This is the actual sample data the running example uses; embedded in §5.1 to anchor the example. |
| 05 | `fig05-page05-img1.png` | 5 | Scatterplot of Sales vs Advertising (no fitted line). | USE | The "raw data" picture the lecture asks the reader to look at before fitting anything; embedded in §5.1. |
| 06 | `fig06-page06-img1.jpeg` | 6 | Stock photo: chalkboard covered with physics formulae (Newton, Einstein) — background for the "Model = mathematical equation" slide. | SKIP | Decorative. |
| 07 | `fig07-page07-img1.jpeg` | 7 | Stock photo: chalkboard with calculus secant-line scribbles — background for the "Model coefficients" slide. | SKIP | Decorative. |
| 08 | `fig08-page08-img1.png` | 8 | Four scatterplots showing the same Sales-vs-Advertising data with three different candidate lines (and one with no line). | USE | Directly motivates "which line is best?" — embedded in §3.2 where OLS is introduced. |
| 09 | `fig09-page09-img1.jpeg` | 9 | Generic scatter-plus-fitted-line cartoon (blue points, red line, axes from -20 to 60 and 0 to 16). | USE | Lecture uses it as a textbook visual for "linear-dependence assumption"; embedded in §3.1. |
| 10 | `fig10-page09-img2.png` | 9 | Wikipedia screenshot of "Regression analysis" article opening paragraph. | REWORK | Useful as visual confirmation of the textbook definition, but a screenshot of Wikipedia is a poor study artefact; embedded once in §1 with a paraphrased prose definition immediately afterwards. |
| 11 | `fig11-page09-img3.jpeg` | 9 | Book cover: *Inquiries into Human Faculty and its Development* — Francis Galton (1883), the historical origin of "regression". | SKIP | Lecture uses it as a one-frame historical aside (Galton coined "regression toward mediocrity"). Pure context decoration; no formula or data. |
| 12 | `fig12-page10-img1.png` | 10 | Scatterplot with regression line **and one labelled triple**: Observed point, Predicted point, vertical Residual segment. | USE | Canonical residual-visualisation diagram; embedded in §3.3 where the residual is defined. |
| 13 | `fig13-page11-img1.png` | 11 | Sales-vs-ADVT scatter with the fitted OLS line `Sales = 51.849 + 7.527 × Advertising` drawn through it. | USE | The chapter's worked-example "after fitting" picture; embedded in §5.1 to pair with the R output. |
| 14 | `fig14-page11-img2.jpeg` | 11 | Equation rendered as image: `Sales = 51.849 + 7.527 × Advertising`. | REWORK | Lecture slide had the equation as an image; we re-typeset the equation in LaTeX inline in §5.1 and do not embed the raster (image-only math is poor pedagogy). Listed here for completeness; SKIP in chapter. |
| 15 | `fig15-page12-img1.jpeg` | 12 | Two stacked scatterplots: top shows deviations from the mean $\bar y$ (SST decomposition); bottom shows the same data with the regression line, with black arrows for $y_i - \bar y$ and red arrows for $y_i - \hat y_i$. | USE | The single most important figure for grasping the SST/SSE/SSR decomposition; embedded in §3.5. |
| 16 | `fig16-page13-img1.jpeg` | 13 | Equation rendered as image: $\text{SST} = \sum_{i=1}^{n}(y_i - \bar y)^2$. | REWORK | Same reason as fig14 — we typeset the formula in LaTeX in §3.5 and do not embed the raster. |
| 17 | `fig17-page14-img1.png` | 14 | Equation rendered as image: $\text{SSE} = \sum_{i=1}^{n}(y_i - \hat y_i)^2$. | REWORK | Same reason — typeset in LaTeX in §3.5. |
| 18 | `fig18-page16-img1.jpeg` | 16 | R `lm(SALES ~ ADVT)` output: coefficients table (Intercept 51.849, ADVT 7.527, p-values) plus residual standard error, Multiple R-squared 0.2469, Adjusted R-squared 0.2142, F-statistic. Two callouts label "Part I" (coefficients) and "Part II" (fit statistics). | USE | The single R-output panel that anchors §3.6 ($R^2$ interpretation) and §3.8 (p-values). Embedded in §5.1. |
| 19 | `fig19-page17-img1.jpeg` | 17 | R `lm(SALES ~ ADVT + INCOME)` output: Intercept 36.8948, ADVT 5.0691, INCOME 0.8081, Multiple R-squared 0.452, Adjusted R-squared 0.4022. | USE | Direct comparison to fig18 — adding a predictor raises $R^2$ from 24.69% to 45.20%. Embedded in §5.2. |
| 20 | `fig20-page17-img2.jpeg` | 17 | Equation rendered as image: `Sales = a + b₁ × Advertising + b₂ × Income`. | REWORK | Typeset in LaTeX inline in §5.2; raster not embedded. |
| 21 | `fig21-page20-img1.jpeg` | 20 | R coefficient table for a house-price regression: SqFt, Bedrooms, **Bathrooms 7883.278** (SE 2117.035), Offers, BrickYes, NeighborhoodNorth, NeighborhoodWest. Multiple R-squared 0.8686. | USE | The "add a bathroom?" worked example uses this output to compute a 95% CI; embedded in §5.3. |
| 22 | `fig22-page22-img1.jpeg` | 22 | Decorative section-title slide: stylised silver-blue ribbon spiral on a pale-blue background ("Flexible regression models"). | SKIP | Pure section-divider art. |
| 23 | `fig23-page29-img1.jpeg` | 29 | Snippet of the salary-discrimination dataset (Gender / Experience / Salary, first nine rows). | USE | Reference data for the §5.4 worked example; embedded there. |
| 24 | `fig24-page30-img1.png` | 30 | Boxplots: Salary by Gender (Female vs Male). | USE | Shows the salary gap visually; embedded in §5.4 ("first look at the data"). |
| 25 | `fig25-page31-img1.png` | 31 | Boxplots: Experience by Gender. | USE | Rules out "women have less experience" as an explanation; embedded in §5.4 alongside fig24. |
| 26 | `fig26-page32-img1.jpeg` | 32 | Scatterplot of Salary vs Experience with triangles = male, circles = female — visualises a clear difference in slope. | USE | Motivates dummy variables and interaction terms; embedded in §5.4. |
| 27 | `fig27-page34-img1.jpeg` | 34 | Equation rendered as image: `Gender.Male = {1 if "male", 0 otherwise}`. | REWORK | Typeset in LaTeX in §3.10; raster not embedded. |
| 28 | `fig28-page35-img1.jpeg` | 35 | R `lm(Salary ~ Gender.Male)` output: Intercept 74420, Gender.Male **16591**, R-squared 0.1201. | USE | The "dummy alone" model; embedded in §5.4. |
| 29 | `fig29-page38-img1.jpeg` | 38 | R `lm(Salary ~ Experience + Gender.Male)` output: Intercept 53260, Experience 1744.6, Gender.Male 17020.6, R-squared 0.4413. | USE | The "dummy plus continuous" model — parallel lines case; embedded in §5.4. |
| 30 | `fig30-page40-img1.jpeg` | 40 | Salary-vs-Experience scatter with two **parallel** fitted lines (red = male, black = female) from the additive dummy model. | USE | Illustrates "same slope, different intercept"; embedded in §5.4. |
| 31 | `fig31-page42-img1.jpeg` | 42 | Equation rendered as image showing element-wise multiplication producing `Gender.Exp.Int`. | REWORK | Typeset inline in §3.11; raster not embedded. |
| 32 | `fig32-page43-img1.jpeg` | 43 | R `lm(Salary ~ Experience + Gender.Male + Gender.Exp.Int)` output: Experience 666.7, Gender.Male **−8034.3**, Gender.Exp.Int **2086.2**, R-squared 0.5561. | USE | The interaction-term model — non-parallel lines; embedded in §5.4. Important: dummy coefficient changes sign. |
| 33 | `fig33-page46-img1.jpeg` | 46 | Salary-vs-Experience scatter with two **non-parallel** fitted lines (red male steeper) from the interaction model. | USE | The visual payoff of interaction terms; embedded in §5.4. |
| 34 | `fig34-page47-img1.png` | 47 | Four-panel diagram of two predictors $X_1, X_2$ and response $Y$: Independent (separate arrows), Small Correlation (overlapping circles), Multicollinear (heavy overlap), Identical Information (one merged circle). | USE | Best concept-diagram for multicollinearity; embedded in §3.12. |
| 35 | `fig35-page48-img1.png` | 48 | Tiny 2×2 correlation table: Sales/Sales = 1, Sales/Assets = 0.9488, Assets/Sales = 0.9488, Assets/Assets = 1. | USE | Concrete example of a high-correlation pair flagged as multicollinear; embedded in §3.12. |
| 36 | `fig36-page48-img2.png` | 48 | Larger correlation-matrix visualisation (~26×26 financial-variables matrix) with coloured ellipses indicating correlation strength and sign. | USE | The "scatterplot/correlation matrix" diagnostic tool for multicollinearity; embedded in §3.12. |

---

## Coverage check

- **USE figures embedded in chapter:** 22 (fig04, 05, 08, 09, 10 [also REWORKed with prose], 12, 13, 15, 18, 19, 21, 23, 24, 25, 26, 28, 29, 30, 32, 33, 34, 35, 36).
- **REWORK figures handled in chapter:** 7 (fig10 prose paraphrase; fig14, 16, 17, 20, 27, 31 each re-typeset in LaTeX rather than embedded as rasters).
- **SKIP figures:** 7 (fig01 template ornament; fig02, 03, 06, 07 stock-photo backgrounds; fig11 book cover; fig22 section-divider art).
- **Total:** 36 (matches PDF inventory).

Every informative figure in the source PDF is accounted for. Decorative stock photos and slide-template ornaments are SKIP-rated with justification above; image-only equations are REWORKed by typesetting them in LaTeX in the chapter (more legible than embedded rasters and machine-searchable).
