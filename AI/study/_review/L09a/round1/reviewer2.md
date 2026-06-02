# L09a Round 1 — Reviewer 2 (Mathematical Rigor)

**Reviewer role:** Lecture Reviewer #2 — Mathematical Rigor. Verify every formula in
`study/lectures/L09a-Bayesian-Networks.md` against the source slides in
`Lecture9-Bayesian Networks.pdf` (slides 1–66). Be harsh.

**Scope (per spec §7.1):** conditional probability definition, product rule, chain
rule, BN factorisation, inference by enumeration, and all 8 worked examples.

---

## VERDICT

**Pass with one minor concern (P2).** Every formula matches the source; every
computation reproduces correctly; all 8 worked examples are numerically faithful
to the slides. The only mathematical defect is a small *displayed-arithmetic
inconsistency* in the Marie's-wedding worked example (chapter rounds the prior
to 0.014, but reports the slide's exact-fraction answer 0.111 — the rounded
intermediates actually give 0.113). Everything else is solid.

No P0, no P1, one P2.

---

## P0 — Showstoppers

*(none)*

---

## P1 — Important issues

*(none)*

---

## P2 — Polish / minor

### P2-1. Marie's wedding: displayed intermediates do not yield the reported final answer

**File / line:** `study/lectures/L09a-Bayesian-Networks.md` §3.4, lines 232–233.

**Issue.** The chapter writes
$$P(\text{Rain} \mid \text{Predict}) = \frac{0.9 \times 0.014}{0.9 \times 0.014 + 0.1 \times 0.986} = \frac{0.0126}{0.0126 + 0.0986} = \frac{0.0126}{0.1112} \approx 0.111.$$

`0.0126 / 0.1112` evaluates to **0.11331**, not 0.111. The slide-24 answer of
0.111 is recovered only if you keep the exact fraction `5/365`:
`(0.9 × 5/365) / (0.9 × 5/365 + 0.1 × 360/365) = (4.5/365) / (40.5/365) =
4.5 / 40.5 = 0.1111…`. The chapter writes the rounded intermediates (0.0126 /
0.1112) but reports the exact-fraction answer (0.111). A careful student
reproducing the chapter's arithmetic will land on 0.113 and conclude they have
made an error.

**Suggested fix.** Either (a) state the prior as `5/365 ≈ 0.0137` throughout and
compute consistently to 0.111, or (b) acknowledge the rounding: "Working with
the rounded `P(Rain) = 0.014` gives ≈ 0.113; the slide reports 0.111, obtained
by carrying 5/365 exactly." Option (a) is cleaner.

**Severity.** P2 — does not affect the final reported number (which matches the
slide), but the displayed chain of equalities is internally inconsistent and a
typical student will notice the 0.113 vs 0.111 gap.

---

## EVIDENCE — formula-by-formula verification

### Conditional-probability definition (§3.3, line 152)

> $P(A \mid B) = P(A \cap B)/P(B)$, $P(B) > 0$.

Verified against slide 14 (chapter cites it). Standard form, no errors.

### Product rule (§3.3, line 156, cheat-sheet line 880)

> $P(A,B) = P(A \mid B)\,P(B) = P(B \mid A)\,P(A)$.

Verified against slide 19. Correct.

### Chain rule (§3.3, line 158, cheat-sheet line 881)

> $P(A_1, \dots, A_n) = \prod_{i=1}^n P(A_i \mid A_1, \dots, A_{i-1})$.

Verified against slide 19 / 42 (slide 42 image rendered: chain-rule line
matches verbatim). Correct.

### Bayes' rule (§3.3, line 191)

> $P(A \mid B) = P(B \mid A)\,P(A) / P(B)$.

Standard; matches slides 19–24.

### Total-probability denominator (§3.4, line 229, cheat-sheet line 883)

> $P(B) = P(B \mid A)P(A) + P(B \mid \neg A)P(\neg A)$.

Standard; matches slide 24 derivation visible in `page24-marie-wedding-bayes-calculation.png`.

### Independence (§3.5, line 246)

> $P(A \cap B) = P(A)\,P(B) \iff P(A \mid B) = P(A) \iff P(B \mid A) = P(B)$.

Standard. Slide 25 cited. Correct.

### Conditional independence (§3.6, line 258)

> $P(X, Y \mid Z) = P(X \mid Z)\,P(Y \mid Z) \iff P(X \mid Y, Z) = P(X \mid Z)$.

Verified against slide 41 (`page41-rain-umbrella-traffic-cond-indep.png`)
which writes both forms verbatim:
- `P(U, T | R) = P(U | R) P(T | R)`
- `P(U | T, R) = P(U | R)`

Correct.

### Markov condition (§3.9, line 338)

> $X \perp \text{NonDescendants}(X) \mid \text{Parents}(X)$.

Verified against slide 39 (`page39-markov-condition-diagram.png`). Correct
re-statement of the slide's English version.

### BN joint factorisation (§3.10, line 356, cheat-sheet line 898)

> $P(X_1=x_1, \dots, X_n=x_n) = \prod_{i=1}^n P(X_i=x_i \mid \text{Parents}(X_i)=\text{parents}_i)$.

Verified against slide 42 (`page42-joint-from-chain-rule.png`) — three-line
derivation (chain rule → Markov → BN factorisation) matches the slide exactly.

### Naive Bayes assumption (§3.11, line 391)

> $P(A_1, A_2, \dots, A_n \mid C) = \prod_{i=1}^n P(A_i \mid C)$.

Standard. Slide 28 cited. Correct.

### Inference by enumeration (§3.13, line 452)

> $P(X=x \mid e) = \alpha \sum_y P(X=x, e, y) = \alpha \sum_y \prod_{i=1}^n P(V_i=v_i \mid \text{Parents}(V_i))$.

Verified against slides 58–60 (`page58-…` and `page60-…`) — the "Step 1 /
Step 2 / Step 3" reduction matches.

### Parameter-count formula (§3.8, line 322)

> $\sum_i (|D(X_i)| - 1) \cdot \prod_{X_j \in \text{Pa}(X_i)} |D(X_j)|$.

For the alarm network (5 Boolean nodes, parent sets ∅, ∅, {B,E}, {A}, {A}) this
gives $1 + 1 + 4 + 2 + 2 = 10$, which is what the chapter and slide 47 state.
Standard parameter-count identity; correct.

### CPT-size identity (§3.8, line 314)

> "Boolean variable with $k$ Boolean parents has $2^{k+1}$ probability entries
> in total — though only $2^k$ of them are *independent* numbers."

Verified against slide 38 (`page38-cpt-detail.png`): the slide writes "$2^{k+1}$
probabilities" — the chapter correctly distinguishes that this is the count of
*table cells*, with half determined by row-sum-to-1. The clarification is more
precise than the slide and is the right pedagogical move (also flagged as
Pitfall 6.9 in §6).

---

## EVIDENCE — worked-example numerical verification

### Worked example 1: Meningitis (§3.4 / §5.1, slide 21)

Givens: $P(\text{stiff} \mid \text{men}) = 0.5$, $P(\text{men}) = 2 \times 10^{-5}$, $P(\text{stiff}) = 0.05$.

Computation: $\frac{0.5 \times 2 \times 10^{-5}}{0.05} = \frac{10^{-5}}{0.05} = 2 \times 10^{-4}$.

Chapter: $2 \times 10^{-4}$. **Match.**

### Worked example 2: Marie's wedding (§3.4 / §5.2, slides 22–24)

Givens: $P(R) = 5/365 \approx 0.014$, $P(\text{Pr} \mid R) = 0.9$, $P(\text{Pr} \mid \neg R) = 0.1$.

Slide answer: 0.111 (using exact 5/365).
Chapter displayed arithmetic: $0.0126 / 0.1112 \approx 0.111$ — but the literal
division $0.0126 / 0.1112 = 0.1133$, not 0.111. **Match in final number but
displayed-arithmetic mismatch — see P2-1 above.**

### Worked example 3: Cavity / Toothache marginals and conditionals (§3.2 / §3.3 / §5.3, slides 9–18)

Joint: 0.8 / 0.1 / 0.05 / 0.05 (verified against `page09-joint-distribution-table.png`).

Marginals (chapter lines 141):
- $P(\text{Cavity} = F) = 0.8 + 0.1 = 0.9$ — **correct**.
- $P(\text{Cavity} = T) = 0.05 + 0.05 = 0.1$ — **correct**.
- $P(\text{Toothache} = F) = 0.8 + 0.05 = 0.85$ — **correct**.
- $P(\text{Toothache} = T) = 0.1 + 0.05 = 0.15$ — **correct**.

Conditionals (chapter lines 165, 167):
- $P(\text{Cav}{=}T \mid \text{Toot}{=}F) = 0.05 / 0.85 = 0.0588 \approx 0.059$ — matches slide 17 (0.059). **Correct.**
- $P(\text{Cav}{=}F \mid \text{Toot}{=}T) = 0.1 / 0.15 = 0.6667 \approx 0.667$ — matches slide 17 (0.667). **Correct.**

Normalisation trick (chapter line 182):
- $P(\text{Toot}{=}F \mid \text{Cav}{=}F) = 0.8 / 0.9 = 0.8889 \approx 0.889$ — matches slide 18. **Correct.**
- $P(\text{Toot}{=}T \mid \text{Cav}{=}F) = 0.1 / 0.9 = 0.1111 \approx 0.111$ — matches slide 18. **Correct.**

### Worked example 4: Naive Bayes (§3.11 / §5.4, slide 29)

Test record: Refund=No, Married, Income=120K.

Chapter line 412: $P(X \mid \text{No}) = (4/7) \cdot (4/7) \cdot 0.0072 \approx 0.0024$.

Verification:
- $P(\text{Refund}{=}\text{No} \mid \text{No}) = 4/7$ — matches slide 29 (`P(Refund=No|No) = 4/7`). **Correct.**
- $P(\text{Married} \mid \text{No}) = 4/7$ — matches slide 29 (`P(Marital Status=Married|No) = 4/7`). **Correct.**
- Gaussian density at $x = 120$, $\mu = 110$, $\sigma^2 = 2975$:
  $(1/\sqrt{2\pi \cdot 2975}) \exp(-100/5950) = (1/\sqrt{18691.5}) \cdot 0.9833
  = 0.00731 \cdot 0.9833 = 0.00719 \approx 0.0072$. **Match.**
- Product: $16/49 \cdot 0.0072 = 0.3265 \cdot 0.0072 = 0.00235 \approx 0.0024$. **Match.**

Chapter line 415: $P(X \mid \text{Yes}) = 1 \cdot 0 \cdot 1.2 \times 10^{-9} = 0$.

- $P(\text{Refund}{=}\text{No} \mid \text{Yes}) = 1$ — matches slide. **Correct.**
- $P(\text{Married} \mid \text{Yes}) = 0$ — matches slide. **Correct.**
- Gaussian at $x = 120$, $\mu = 90$, $\sigma^2 = 25$:
  $(1/\sqrt{50\pi}) \exp(-900/50) = 0.0798 \cdot e^{-18} = 0.0798 \cdot 1.523 \times 10^{-8} \approx 1.215 \times 10^{-9} \approx 1.2 \times 10^{-9}$. **Match.**

Conclusion Class = No. **Matches slide.**

### Worked example 5: A → B → {C, D} joint entry (§4.2 / §5.5, slides 44–45)

Chapter line 589–590: $P(A{=}T, B{=}T, C{=}T, D{=}T) = 0.4 \times 0.3 \times 0.1 \times 0.95 = 0.0114$.

CPT values verified against `page35-abcd-bayesnet-cpts.png` and `page45-abcd-joint-calculation.png`:
- $P(A{=}T) = 0.4$ ✓
- $P(B{=}T \mid A{=}T) = 0.3$ ✓
- $P(C{=}T \mid B{=}T) = 0.1$ ✓
- $P(D{=}T \mid B{=}T) = 0.95$ ✓

$0.4 \cdot 0.3 = 0.12; \; 0.12 \cdot 0.1 = 0.012; \; 0.012 \cdot 0.95 = 0.0114$. **Match.**

### Worked example 6: Alarm network (§5.6, slides 46–48)

CPT values verified against `page47-alarm-network-cpts.png`:
- $P(+b) = 0.001$, $P(+e) = 0.002$ ✓
- $P(+a \mid +b, +e) = 0.95$, $P(+a \mid +b, \neg e) = 0.94$ ✓
- $P(+a \mid \neg b, +e) = 0.29$, $P(+a \mid \neg b, \neg e) = 0.001$ ✓
- $P(+j \mid +a) = 0.9$, $P(+j \mid \neg a) = 0.05$ ✓
- $P(+m \mid +a) = 0.7$, $P(+m \mid \neg a) = 0.01$ ✓

Parameter count: $1 + 1 + 4 + 2 + 2 = 10$ vs. $2^5 - 1 = 31$. **Match.**

Sample joint computation, chapter lines 722–725:
$P(+j, +m, +a, \neg b, \neg e) = 0.9 \cdot 0.7 \cdot 0.001 \cdot 0.999 \cdot 0.998$
$= 0.63 \cdot 0.001 \cdot 0.999 \cdot 0.998$
$= 0.00063 \cdot 0.999 \cdot 0.998$
$= 0.00062937 \cdot 0.998$
$= 0.000628 \dots$

Chapter writes "0.000\,628\ldots". **Match.**

### Worked example 7: Lecture-late joint entry $P(T, \neg R, L, \neg M, S)$ (§4.3 / §5.7, slide 56)

Derivation verified against `page56-compute-joint-derivation.png` — each step
(chain rule, Markov, $M \perp S$) reproduced verbatim from the slide.

Numerical (chapter line 623): $0.3 \cdot 0.4 \cdot 0.1 \cdot 0.4 \cdot 0.3 = 0.00144$.

Factor verification using slide-53 CPTs (`page53-lecture-bn-step-add-tables.png`):
- $P(T \mid L) = 0.3$ ✓
- $P(\neg R \mid \neg M) = 1 - 0.6 = 0.4$ ✓ (slide gives $P(R \mid \neg M) = 0.6$)
- $P(L \mid \neg M, S) = 0.1$ ✓
- $P(\neg M) = 1 - 0.6 = 0.4$ ✓ (slide gives $P(M) = 0.6$)
- $P(S) = 0.3$ ✓

Product: $0.3 \cdot 0.4 = 0.12; \; 0.12 \cdot 0.1 = 0.012; \; 0.012 \cdot 0.4 = 0.0048; \; 0.0048 \cdot 0.3 = 0.00144$. **Match.**

### Worked example 8: Lecture-late inference $P(R \mid T, \neg S)$ (§5.8, slides 58–60)

The slides only sketch the structure ("Step 1 / Step 2 / Step 3", "4 joint
computes / 4 joint computes" — `page60-compute-conditional-numbers.png`); the
numerical solve is contributed by the chapter, so I check every cell.

Chapter formula (line 739):
$P(R, T, \neg S) = \sum_{m,l} P(M{=}m) P(\neg S) P(R \mid M{=}m) P(L{=}l \mid M{=}m, \neg S) P(T \mid L{=}l)$.

This is the BN factorisation $P(M) P(S) P(R \mid M) P(L \mid M, S) P(T \mid L)$
evaluated at $S = \text{false}$, with $R$ and $T$ pinned to true and the hidden
variables $M, L$ summed out. **Correct setup.**

Numerator rows (chapter table line 744–748):
- $(m{=}T, l{=}T)$: $0.6 \cdot 0.3 \cdot 0.1 \cdot 0.3 \cdot 0.7 = 0.18 \cdot 0.1 \cdot 0.3 \cdot 0.7 = 0.018 \cdot 0.21 = 0.00378$ ✓
- $(m{=}T, l{=}F)$: $0.6 \cdot 0.3 \cdot 0.9 \cdot 0.8 \cdot 0.7 = 0.18 \cdot 0.9 \cdot 0.56 = 0.162 \cdot 0.56 = 0.09072$ ✓
- $(m{=}F, l{=}T)$: $0.4 \cdot 0.6 \cdot 0.2 \cdot 0.3 \cdot 0.7 = 0.24 \cdot 0.2 \cdot 0.21 = 0.048 \cdot 0.21 = 0.01008$ ✓
- $(m{=}F, l{=}F)$: $0.4 \cdot 0.6 \cdot 0.8 \cdot 0.8 \cdot 0.7 = 0.24 \cdot 0.8 \cdot 0.56 = 0.192 \cdot 0.56 = 0.10752$ ✓

Sum: $0.00378 + 0.09072 + 0.01008 + 0.10752 = 0.21210$. **Match.**

Denominator rows (chapter table line 755–759):
- $(m{=}T, l{=}T)$: $0.6 \cdot 0.7 \cdot 0.1 \cdot 0.3 \cdot 0.7 = 0.42 \cdot 0.021 = 0.00882$ ✓
- $(m{=}T, l{=}F)$: $0.6 \cdot 0.7 \cdot 0.9 \cdot 0.8 \cdot 0.7 = 0.42 \cdot 0.504 = 0.21168$ ✓
- $(m{=}F, l{=}T)$: $0.4 \cdot 0.4 \cdot 0.2 \cdot 0.3 \cdot 0.7 = 0.16 \cdot 0.042 = 0.00672$ ✓
- $(m{=}F, l{=}F)$: $0.4 \cdot 0.4 \cdot 0.8 \cdot 0.8 \cdot 0.7 = 0.16 \cdot 0.448 = 0.07168$ ✓

Sum: $0.00882 + 0.21168 + 0.00672 + 0.07168 = 0.29890$. **Match.**

Normalisation (chapter line 765):
$P(R \mid T, \neg S) = 0.2121 / (0.2121 + 0.2989) = 0.2121 / 0.5110 = 0.4150 \approx 0.415$. **Match.**

All cells, all sums, the normalisation, and the final answer reproduce exactly.

### EU formula (§1, line 24)

> $\text{EU}(a) = \sum_o P(o \mid a)\,U(o)$.

Standard decision-theory formula. Slide 3 attests its use. Correct.

### Coin-flip RV example (§3.1, line 99)

> $X(\text{HHH}) = 3$; $X(\text{HHT}) = X(\text{HTH}) = X(\text{THH}) = 2$;
> $X(\text{TTH}) = X(\text{THT}) = X(\text{HTT}) = 1$; $X(\text{TTT}) = 0$.

Count check: TTH has 1 H, THT has 1 H, HTT has 1 H — all = 1 ✓. HHT/HTH/THH
each have 2 H ✓. Distribution: $P(X{=}3) = 1/8, P(X{=}2) = 3/8, P(X{=}1) = 3/8,
P(X{=}0) = 1/8$. Sum to 1 ✓. **Correct.**

---

## OUT-OF-SCOPE OBSERVATIONS (not mathematical-rigor issues, flagged for PM)

These are notes the PM may pass to other reviewers; none are mine to fix.

1. **"Random variable" definition slightly looser than measure-theoretic
   standard.** Chapter line 90 says an RV is "a function from the sample space
   … to the real numbers", but immediately gives categorical RVs (Weather =
   Sunny / Cloudy / Rainy / Snow) and pair-valued RVs (Dice = (i,j)) which are
   not real-valued. This follows the lecture slides verbatim (the slides also
   use this loose definition à la Russell & Norvig) so it's not a defect
   relative to the source — but a stickler reviewer might want a footnote
   saying "AI textbooks routinely call non-numeric-valued functions 'random
   variables' for convenience". Out of scope for math rigor.

2. **Joint factorisation chain-rule expansion repeated.** §3.10 and §4.3 both
   walk through chain rule + Markov, with the same algebra. Not a math
   problem — possibly an editorial one for Reviewer 1.

3. **Slide-numbering sanity.** The chapter consistently cites slide numbers
   1–66. The PDF is 67 slides per the figures.md catalogue; checked that
   every cited slide number in the chapter (3, 4, 5–7, 8, 9–13, 14, 17, 18,
   19–24, 25, 27–30, 33, 35–42, 43, 44–48, 49, 50–60, 63, 64, 66) maps to a
   real slide. No misnumbering detected.

---

## CONCERNS / RISKS

- The Marie's-wedding intermediate-arithmetic mismatch (P2-1) is the only
  thing that will trip a careful student. Easy fix.
- The numerical solve in §5.8 is the chapter's own contribution (slides 58–60
  only sketch the structure). It is **correct in every cell** — I am confident
  in stamping this as exam-quality.
- All 8 worked examples reproduce, every formula in the cheat-sheet survives
  scrutiny, the parameter-count identity is exact, and the BN factorisation
  derivation in §3.10 mirrors slide 42 verbatim.

The mathematical content is in good shape.

---

## Report to PM

**Assignment recap:** L09a — Bayesian Networks, Round 1 mathematical-rigor
review. Source: `Lecture9-Bayesian Networks.pdf` (slides 1–66, Serkan Ayvaz).
Chapter under review: `study/lectures/L09a-Bayesian-Networks.md`.

**Status:** Pass with concerns (one P2; no P0/P1).

**P0 findings:** None.

**P1 findings:** None.

**P2 findings:**

1. `study/lectures/L09a-Bayesian-Networks.md` §3.4, lines 232–233 — Marie's
   wedding worked example shows intermediate arithmetic `0.0126 / 0.1112` and
   reports `≈ 0.111`. The literal division gives `0.113`. The reported `0.111`
   is the slide's exact-fraction answer (`(4.5/365) / (40.5/365) = 1/9`).
   **Suggested fix:** either compute with the exact fraction $5/365$
   throughout, or add a one-line "(carrying $5/365$ exactly rather than the
   rounded 0.014)" caveat. Cosmetic, but a sharp student will notice and lose
   trust.

**QA Checklist (§7) status:** N/A — this is a content review of a study chapter,
not a feature with an attached Plan. The spec for this review is the section-7.1
instruction (verify all formulas + 8 worked examples). Per that spec:
- Conditional probability — Pass.
- Product rule — Pass.
- Chain rule — Pass.
- Bayes' rule — Pass.
- Total-probability denominator — Pass.
- Conditional independence — Pass.
- Markov condition — Pass.
- BN factorisation — Pass.
- Naive Bayes assumption — Pass.
- Inference by enumeration formula — Pass.
- CPT-size / parameter-count identities — Pass.
- Worked example 1 (Meningitis) — Pass.
- Worked example 2 (Marie's wedding) — Pass-with-P2 (final answer matches slide; intermediate arithmetic doesn't).
- Worked example 3 (Cavity / Toothache marginal + conditional) — Pass.
- Worked example 4 (Naive Bayes) — Pass.
- Worked example 5 (A→B→{C,D} joint) — Pass.
- Worked example 6 (Alarm network) — Pass.
- Worked example 7 (Lecture-late joint entry $P(T,\neg R,L,\neg M,S)$) — Pass.
- Worked example 8 (Lecture-late inference $P(R \mid T, \neg S)$) — Pass.

**Acceptance criteria (§1) status:** N/A — content review.

**DOCUMENT.md audit:** N/A — content review; no code directories were touched.

**Out-of-scope observations:**

- §3.1 RV definition is the loose "function to reals" version followed by
  categorical and pair-valued examples — follows the source slides, but a
  Reviewer 1 (clarity / pedagogy) might want a footnote.
- §3.10 chain-rule-plus-Markov derivation is repeated in §4.3 — possible
  editorial trim for Reviewer 1.
- All slide-number citations resolve to real slides (1–66); no misnumbering.

**Concerns / risks:** None beyond the one P2 above. The chapter's mathematical
content is publishable as-is once the Marie's-wedding intermediate arithmetic
is reconciled (≈ 2-minute fix).

**What PM should do next:**

1. Pass the P2 finding to whichever agent owns chapter edits (likely the
   lecture-writer engineer) — single-line cosmetic fix.
2. Do **not** block the L09a workflow on this; the final answers and every
   non-cosmetic formula are correct. App Tester (if any visual checks remain)
   can proceed; final code review can proceed; this P2 can be folded into the
   reviewer-aggregated edit pass.
3. After the fix, no re-QA is needed for mathematical rigor — I've verified
   every other number.

**DOCUMENT.md updated:** N/A for QA / Reviewer roles.
