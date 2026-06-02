# L05 Round 1 — Reviser Summary

**File revised:** `study/lectures/L05-Local-Search.md` (full rewrite, structure preserved)
**Reviewers addressed:** R1 (Concept Completeness), R2 (Mathematical Rigor), R3 (Pedagogical Clarity), R4 (Exam Readiness)
**Source ground-truth re-verified:** `Lecture5-Local Search.pdf` (slides 1–50), figures `fig01..fig18` (esp. fig04, fig07, fig18 visually inspected)

---

## P0 fixes applied

### P0-1. Hill-climbing `<` vs `≤` contradiction (R2, R3, R4)

- **Switched to `<` throughout** (§3.3 pseudocode, §4.1 pseudocode, §8.2 cheat sheet, §6 termination-condition pitfall) to match slide 13 verbatim.
- **Rewrote the plateau explanation correctly.** Slide-13's strict `<` rule **does not terminate on a plateau** — when `value(next) = value(current)`, the test `value(next) < value(current)` is FALSE so the algorithm sets `current ← next` and walks sideways indefinitely. Three-case breakdown (improvement / plateau / strict decrease) now in §3.3 spells this out.
- The prior version had this backwards: it claimed `<` "would happily traverse plateaux of equal value forever" but adopted `≤` while writing the prose as if `≤` were the safer plateau handler. R2 and R4 both flagged the inversion explicitly; both are now correct.
- The textbook `≤` variant is mentioned (§3.4 sideways-move variant + §6 plateau pitfall) but explicitly NOT the canonical rule.

### P0-2. Slide-12 8-queens trace fabricated (R1, R2, R3, R4)

- **Replaced the §5.4 caption and prose** with the actual slide-12 content (verified against `fig07-nqueens-example-solution.png`):
  - Left board: row scores `{2, 2, 1, 2, 3, 1, 2}` for the lower-right queen's seven alternative rows; minimum is $h = 1$ — *the local-minimum trap* the lecturer warns about in the slide caption.
  - Middle board: a different queen's column annotated; one row gives $h = 0$.
  - Right board: solved.
- Verbatim slide-12 caption ("Queen in lower right … Moving to a row with 1 conflict would be a local minima …") now quoted in §5.4.
- Removed the "happy accident of the tie-breaking rule" editorialising; the pedagogical point of slide 12 (local-minimum trap warning) is now front and centre.

### P0-3. §5.1 8-puzzle trace sideways-move under `≤` rule (R3, R4)

- The §5.1 trace table now explicitly labels each step as **strict improvement** / **plateau (equal value)** / **strict decrease**, and shows how slide-13's `<` rule permits the middle plateau step.
- Added a sentence anchoring the sign convention at the top of §5.1 (R3.P0.1 point 4).
- Added a note that the textbook `≤` rule would terminate at the first plateau and the trace would *not* reach the goal — so the slide-5 trace **depends on the slide-13 `<` rule**.
- Removed the ambiguous "$-3$ (tie) or back up to a $-4$ neighbour" wording.

### P0-4. Slide-9 4-queens misread (R4)

- §5.3 rewritten to acknowledge that slide 9 shows fewer queens than columns (it's illustrative, not committed to a per-column formulation at the *start*; the strategy it advocates *is* per-column).
- The §5.3 ↔ §5.4 transition now explicitly says the per-column convention used by slides 10–12 (and §5.4 onward) differs from the picture in slide 9.
- The §5.4 opener now states the per-column convention explicitly and reconciles it with the $8^8$ state-space size in §2.A.

### P0-5. GA mutation `0→0` self-contradiction (R1 implicitly, R2-P2.9, R3-P1.5, R4-P0.4)

- Re-verified by visual inspection of `fig18-mutation.png`:
  - Offspring 1: `1011011111` → `1011001111`. **Bit 6** (1-indexed, left-to-right) flips $1 \to 0$. (Not bit 5; not 0→0.)
  - Offspring 2: `1000000000` → `1010000000`. **Bit 3** flips $0 \to 1$. (This was already correct.)
- §5.7 now states "Throughout this section bits are 1-indexed left-to-right" explicitly at the top.
- Step 4 caption rewritten with corrected bit numbers and clear `1 → 0` / `0 → 1` notation.

### P0-6. Completeness story contradicts itself (R2-P1.10, R4-P0-5)

- §4.4 comparison table and §8.1 cheat-sheet table **now agree**: HC = No; RR-HC = Yes-in-limit (with two named assumptions); SA = "No in practice"; GA = "No (no formal claim)".
- §6 "Hill climbing is complete" pitfall updated to reflect the same story.
- Removed the §4.4 "Yes in the limit of infinite generations + mutation" GA claim, which had no slide basis (per R4).

### P0-7. Missing §2 analogies + caveats (R3-P1.1, R3-P1.2, R3-P1.13)

- Added new §2.E "Mini-analogies for the algorithm-internal operators" subsection with eight full analogies + breakdown caveats:
  1. Random-restart hill climbing — "helicopter ride after every foothill"
  2. First-choice hill climbing — "pick the first step that goes up"
  3. Stochastic hill climbing — "roll a die among the improving directions"
  4. Temperature schedule — "the dimmer-switch on the shaker"
  5. Roulette-wheel selection — "casino roulette with rigged slot widths"
  6. Crossover — "swap engine and body of two prototype cars"
  7. Mutation — "a one-letter typo when copying a long word"
  8. Fitness landscape — "topography of all candidate solutions"
- §2.B caveat for hill climbing rewritten to identify a real metaphor breakdown (sniff-every-direction vs feet-only; step-size mismatch) — previously it praised the algorithm instead of identifying breakdown points (R3-P1.2).
- §2.A caveat split into two clearly-labelled sub-caveats (geometry vs terminology) per R3-P1.8.
- §2.F (renamed from §2.E) cheat-sheet table expanded to include first-choice HC, stochastic HC, elitism, tournament selection, population, generation, plateau, shoulder, ridge, genotype/phenotype, tournament selection (R3-P1.14).

---

## P1 fixes applied

- **R1-P1.1 MCMC gloss:** Added one-sentence definition of MCMC in §3.5 ("MCMC algorithms generate samples from a target probability distribution by constructing a Markov chain whose stationary distribution is the target; SA is the special case where the target is $\propto \exp(f(s)/T)$ with $T \to 0$").
- **R1-P1.2 / R2-P1.7 Continuous-space vs Ridge:** Disentangled in §3.2. Slide-14 footnote now correctly attributed to "continuous-space step-size sensitivity" (a separate, fifth bullet). Ridge moved out of slide-15 list and labelled "not on slide 15; standard reference".
- **R1-P1.4 §5.1 trace clarity:** Trace table re-written (see P0-3 above).
- **R1-P1.5 / R2-slide-18 framing:** Added sentence in §3.5 stating SA's second fundamental departure from HC — "picks one random neighbour per step" with $O(1)$ vs $O(b)$ per-step cost.
- **R2-P1.1 slide-19 caption:** Expanded to cover all four temperatures from the slide ($T \in \{100, 50, 10, 1\}$) with numerical intercepts.
- **R2-P1.2 Geman & Geman attribution:** Changed schedule form to canonical $c / \log(1+t)$ (was $c / \log(t+2)$). Added clarifying note that constant $c$ must exceed deepest-local-optimum depth. **Tagged "Not on the slides; included for context"** per R4-P1.1.
- **R2-P1.3 random-restart completeness:** Added the two missing assumptions in §3.4 ("restart distribution puts positive probability on every basin … AND hill climbing from any state in that basin reaches the global maximum").
- **R2-P1.4 `8^8` arithmetic:** Fixed to $\approx 1.68 \times 10^{7}$ (with exact value $16{,}777{,}216$). Per-column parameterisation now stated explicitly in §2.A and §5.4.
- **R2-P1.5 R&N 7-restarts anecdote:** Tagged "(not on slides; Russell & Norvig AIMA 3e §4.1.1)" and reworded to match R&N's "iterations" not "restarts" (one iteration = one HC run).
- **R2-P1.6 / R4-P1-5 $\Delta = 0$ boundary:** Added explicit note that $\exp(0/T) = 1$ so lateral moves are always accepted; case split is a free choice. §4.2 pseudocode comment changed from "downhill: maybe accept" to "lateral (Δ=0) or downhill: maybe accept".
- **R2-P1.8 §5.1 trace ambiguity:** Resolved by P0-3.
- **R2-P1.9 $h$ vs $f$ notation:** Added explicit "notational warning" in §3.1 and an anchoring sentence at the top of §5.1.
- **R2-P1.11 iteration bound:** Replaced "typically small" with "bounded by the diameter of the objective's image (each step strictly improves or walks a plateau)".
- **R3-P1.3 selection: spin wheel TWICE:** Added bold sentence in §3.6 Selection subsubsection.
- **R3-P1.4 Replacement procedural glue:** Rewrote §3.6 Replacement subsubsection with the explicit "Repeat selection + crossover + mutation until you have $N$ offspring; this set of $N$ offspring is the new generation" connective.
- **R3-P1.7 §3 → §2 cross-links:** Added "Recall the … analogy" sentences in §3.2 (newly added), §3.4 (newly added), §3.6 (rewritten to redeploy the analogy in full per R3 suggestion), §3.7 (newly added).
- **R3-P1.9 §6 sign-convention rewrite:** §6 first pitfall rewritten to commit to one naming convention ($f$ for the maximised objective; $h$ in the L03 non-negative sense) and footnote slide-5's labelling collision.
- **R3-P1.10 Δ definition promoted:** $\Delta > 0$ vs $\Delta < 0$ vs $\Delta = 0$ now its own bulleted block in §3.5, not a parenthetical.
- **R4-P1-2 TSP $\binom{n}{2}$ neighbour count:** Corrected to $\binom{n}{2} - n$ approximately and flagged as not on slides.
- **R4-P1-4 "ridge" not on slide 15:** Moved to "not on slide 15" bullet in §3.2.
- **R4-P1-6 roulette-wheel boundary:** Changed §3.6.1 interval convention to $(F_{i-1}, F_i]$ (left-open, right-closed); §5.7 step 2 now shows the cumulative table and the slice column matches this convention; $R = 7$ now correctly selects chromosome 4 (matches slide 42).
- **R4-P1-7 problem-specific $b$ values:** Added "8-queens: $b = 56$; 8-puzzle: $b \le 4$" to §3.3 Properties table and §4.1.
- **R4-P1-9 multi-step SA example:** §5.8 now includes a 3-row temperature comparison ($T \in \{100, 10, 1\}$, same $\Delta = -5$).
- **R4-P1-10 why 56 not 64:** Added one sentence in §5.4: "the current row is not a successor — that would leave the board unchanged".

---

## P2 fixes applied (selective)

- **R1-P2.1** fig01 caption notes "page-render includes the text overlay".
- **R3-P2.2 / R4-P2-3** $8^8$ motivation: §2.A now ties the state-space size to the per-column convention used in §5.4 (R4-P2-3 closed; R3-P2.2 partial — the explicit "BFS would need 16.7M frontier nodes" sentence not added since the spec's reading-time budget is already at ~55 min).
- **R3-P2.3** §5.8 now has the requested 3-row temperature comparison table.
- **R3-P2.4** §5.6 now states "we pick the smallest power of 2 that exceeds the maximum integer position".
- **R3-P2.6** §8.5 now has the "Expanded from §3.6 line 'biological dictionary'" cross-reference.

---

## P2 items intentionally deferred

- **R1-P2.2, R1-P2.3, R1-P2.4** (catalogue prose tweaks) — `figures.md` is a separate catalogue file; out of scope for this revision pass.
- **R2-P2.1, R2-P2.2** (LaTeX cosmetic `\!` and `\operatorname*`) — replaced `\operatorname*` with the more portable `\mathop{\mathrm{...}}\limits` form; left `\exp(...)` plain (no `\!`) in the formula box, but the existing math is otherwise unchanged.
- **R2-P2.5** (GA pseudocode off-by-one when $N$ odd) — added "assume $N$ even" comment in §4.3 pseudocode.
- **R2-P2.6** (more precise GA per-generation complexity) — §4.3 now states $O(N^{2} + N(F+L))$ with $F$ dominating in practice; §4.4 table shows "$O(NF)$ per generation (dominant)".
- **R2-P2.7** (quantitative $T=1$ sliver) — §3.5 figure caption now shows $\exp(-3) \approx 0.05$ as the sliver boundary.
- **R2-P2.10** ("$\infty$ neighbours" imprecise) — §3.4 reworded to "effectively unbounded neighbours".
- **R3-P2.5** (Mermaid diagrams) — deferred; the figure catalogue's "Mermaid or in-text prose" claim is best fixed by editing `figures.md` itself, which is out of scope for this revision.
- **R3-P2.7** (§2.D blockquote duplication) — kept the §2.D blockquote and turned §3.6's biological dictionary into a "recall §2.D" deployment of the analogy (R3-P1.7).
- **R3-P2.8** (cheat-sheet capitalisation) — pass complete, all rows use sentence case consistently.
- **R3-P2.9** (when-to-use-local-search forward in §2) — added a callout box at the end of §1.
- **R3-P2.10** (reading-time front-matter) — left as-is; not in scope for content revision.
- **R4-P2-1, R4-P2-2** (bibliography, forward-link gating) — leave as outstanding for a later pass; the chapter's "Not on slides; standard reference" tags now flag the editorial-addition issue R4 raised.
- **R4-P2-5** (figure-dependent prose) — partial: §5.1, §5.4, §5.7 all now have explicit numerical content in prose so the figures are corroborative rather than load-bearing.
- **R4-P2-6** (§8.7 GA recommendation editorial) — kept but it's labelled "decision rule", clearly not a slide claim.

---

## Files modified

- `study/lectures/L05-Local-Search.md` — full rewrite of §2 (added §2.E mini-analogies, restructured §2.F cheat-sheet), §3.2 (ridge/continuous-space disentangle, slide-15 four-features), §3.3 (`<` rule + plateau semantics), §3.4 (random-restart assumptions, sideways variant), §3.5 (Δ split, $\Delta=0$ boundary, multi-temp curve description, MCMC gloss, Geman & Geman canonical form), §3.6 (selection spin-twice, Replacement glue), §3.6.1 (interval convention $(F_{i-1}, F_i]$), §4.1 (`<` verbatim, problem-specific $b$), §4.2 (lateral/downhill comment), §4.3 ($N$-even, complexity), §4.4 (completeness column rewritten), §5.1 (trace under `<` rule, sign anchor), §5.3 (slide-9 honest reading), §5.4 (slide-12 trap warning, per-column convention, $b=56$ explanation, R&N aside tagged), §5.6 (10-bits justification), §5.7 (1-indexed convention, cumulative-fitness table, bit-6 fix), §5.8 (3-row temp table), §6 (sign convention rewrite, plateau pitfall rewrite, completeness rewrite, mutation-rate nuance), §7 (GA completeness language softened), §8 (cheat sheet aligned with main text — `<` rule, GA completeness "No", expanded landscape vocab, expanded GA dictionary, §8.8 advice updated).

## Files NOT modified (out of scope for this revision)

- `study/extracted_figures/L05/figures.md` (catalogue prose claims; flagged by R1-P1.3 but is a separate file)
- Image files `fig01.png..fig18.png` (unchanged)
- Cross-reference files `study/_shared/glossary.md`, `study/_shared/cross-references.md`
