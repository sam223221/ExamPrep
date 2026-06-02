# L05 Round 1 — Reviewer #1 (Concept Completeness incl. Figures)

**Source:** `Lecture5-Local Search.pdf` (50 slides)
**Chapter:** `study/lectures/L05-Local-Search.md` (917 lines)
**Figure catalogue:** `study/extracted_figures/L05/figures.md` (18 USE entries, 0 REWORK, well-justified SKIPs)

---

## VERDICT: **NEEDS_REVISION**

Coverage is generally strong — every slide section, every named concept, and every formula from slides 1–50 has a home somewhere in the chapter; every USE figure in the catalogue is embedded; every SKIP is reasonably justified. However, the chapter contains **one material factual error in a figure caption** (slide-12 description, P0), **silently drops at least one slide-stated concept** (Markov Chain Monte Carlo is mentioned but not glossed; the chapter's "out of scope" framing contradicts the lecturer presenting it as the bridge to "more modern techniques"), and the figure-catalogue ↔ chapter ↔ slide accounting is asymmetric in two small but verifiable ways (P1). Bring those to ground and this is approvable.

---

## P0 — MUST FIX (blocks approval)

### P0-1. Slide-12 figure caption misrepresents what the leftmost board shows

**Chapter line 603:**

> "Three boards: the first showing per-row $h$ scores if the lower-right queen is moved (best row gives $h = 0$); the middle shows the result after that move ($h = 0$, the global minimum); the right shows the final solved 8-queens board."

**Slide 12 actually shows** (in the leftmost board) the row-by-row $h$ values **2, 2, 1, 2, 3, 1, 2** for the seven alternative rows of the lower-right column queen. The minimum on the *left* board is **$h = 1$**, not $h = 0$. The point of the slide is exactly the **local-minimum trap**: the lecturer's caption is "Moving to a row with 1 conflict would be a local minima." The $h = 0$ value the chapter mentions appears on the **middle** board (which shows row-options for a *different* queen, with values 3, 3, 2, 3, 2, 3, **0**), not the first.

The chapter currently:
- Tells the reader the leftmost board has a row giving $h = 0$ (false — its best row is $h = 1$, which is the local-minimum trap).
- Loses the pedagogical sting of slide 12 (the explicit local-minimum warning the lecturer puts in the caption).

**Fix:** rewrite the caption to match the slide. Suggested wording:

> "Three boards. **Left:** the original $h = 17$ board annotated with the seven row-scores that would result from moving the lower-right column's queen (best is $h = 1$, marked — a *local-minimum trap*). **Middle:** after the move-up-one-row choice, a different queen's column is annotated with its row-scores; one row gives $h = 0$. **Right:** the resulting solved 8-queens board after taking the $h = 0$ move. The lecturer's caption flags the trap: *'Moving to a row with 1 conflict would be a local minima.'*"

The §5.4 prose narrative below the figure (lines 605–610) *does* mention the trap correctly, but it now contradicts the caption above it — making the section internally inconsistent.

**Severity:** P0 because (a) the caption asserts a verifiable factual claim that is false against the slide, (b) the misstatement undermines the very pedagogical point the slide exists to make (local minima trap), and (c) any student studying from this chapter and the slide side-by-side will be confused about which figure shows what.

**Evidence:** PDF slide 12 (image inspected); chapter line 603; chapter lines 605–610.

---

## P1 — SHOULD FIX (requested, not blocking)

### P1-1. Slide 20 introduces **Markov Chain Monte Carlo (MCMC)** as a named "more modern technique"; the chapter calls it out of scope without giving a one-sentence gloss

**Slide 20** says:

> "More modern techniques: general family of **Markov Chain Monte Carlo (MCMC)** algorithms for exploring complicated state spaces"

The chapter (line 305–307) says:

> "The slides also note (slide 20) that simulated annealing is a special case of a broader family of stochastic-sampling algorithms — **Markov Chain Monte Carlo (MCMC)** — but that family is out of scope."

The §4 spec from this reviewer's brief is **concept completeness**: every *named concept* on a slide must be present. MCMC is named, but the chapter dismisses it. A one-sentence gloss is owed — *"MCMC generates samples from a target probability distribution by constructing a Markov chain whose stationary distribution is that target; SA is the special case where the target is $\propto \exp(f(s) / T)$ with $T \to 0$"* — without expanding into a full subsection. As written the chapter teaches the reader to skip the concept, which is not what concept-completeness requires.

**Fix:** add one sentence (and ideally a single bullet) explaining what MCMC *is*, even if the lecture doesn't go deeper. Concept-completeness ≠ depth; it = presence.

**Evidence:** PDF slide 20; chapter lines 305–307.

### P1-2. Slide 14 mentions "**In continuous spaces, problems w/ choosing step size, slow convergence**" — the chapter glosses this as "Ridge" only

**Slide 14** has a footnote-style line beneath the 1-D landscape sketch:

> "In continuous spaces, problems w/ choosing step size, slow convergence"

The chapter (line 189) folds this into the **Ridge** description: *"(slide 14's 'problems w/ choosing step size, slow convergence' footnote)"*. But the slide-14 footnote is not *about* ridges — it is a separate, distinct slide-14 observation about **continuous-space hill climbing**. The two concerns are conceptually different:

- **Ridge** is a *combinatorial* / *discrete* pathology — neighbours don't align with the ridge direction.
- **Step-size / slow convergence in continuous spaces** is a *continuous-optimisation* pathology — line-search problems, oscillation across narrow valleys, slowdown near the optimum.

Conflating them buries the continuous-space concern. The chapter does mention continuous spaces in §1 ("crucially — applicable to **continuous** state spaces") but never returns to the *cost* of doing so. Slide 14's footnote is precisely that cost.

**Fix:** add a sentence either to §3.2 or §3.3 explicitly capturing the continuous-space concern from slide 14: *"On continuous landscapes, hill climbing additionally suffers from step-size sensitivity (too small → slow convergence; too large → overshoot) and slow asymptotic convergence near the optimum."* Keep the ridge text where it is, but disentangle it from this footnote.

**Evidence:** PDF slide 14 (footnote at the bottom of the slide); chapter line 189.

### P1-3. Catalogue says "All embedded figures are USE", but only **17** of the 18 USE figures are embedded in the chapter

Counted independently from the chapter source: `fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14, fig15, fig17, fig18` = **17 figures embedded** in the chapter body.

**`fig16-roulette-wheel-selection.png` is missing from the chapter body.**

Grep result (line 656 of chapter) shows only "[Omitted long matching line]" — checking the actual chapter contents around §5.7 step 2 (line 654–657):

```markdown
**Step 2 — roulette-wheel selection** (slide 42).

![Roulette wheel laid out as a 1-D bar from 0 to 18 ... ](../extracted_figures/L05/fig16-roulette-wheel-selection.png)
```

— **OK, fig16 IS embedded.** Re-counting: the grep output truncated a line, but reading the actual chapter at line 656 confirms `fig16` is present. Withdrawing the missing-figure claim.

**However**, the *figure-catalogue accounting* still has a separate issue: the catalogue (`figures.md`, line 81–84) says

> "All embedded figures are USE. No REWORK entries were necessary because the page-rendered slides preserve the lecturer's own annotation and labelling; the chapter additionally backs each up with a Mermaid diagram or in-text prose where extra clarity helps."

The chapter does **not** contain a single Mermaid diagram. The figure-catalogue's claim "the chapter additionally backs each up with a Mermaid diagram or in-text prose where extra clarity helps" is half-true (the in-text prose part) and half-false (no Mermaid). Minor, but the catalogue should not claim infrastructure it didn't deliver.

**Fix:** in `figures.md`, drop the "Mermaid diagram or" clause, or add Mermaid diagrams where useful (e.g. a flowchart for the GA loop, a state-machine for SA temperature transitions). I would not require Mermaid additions; just fix the catalogue's prose.

**Evidence:** `figures.md` lines 81–84; chapter (no Mermaid blocks present — search for ``` ```mermaid``` ``` returns zero hits).

### P1-4. Slide 5's neighbour-evaluation in the chapter §5.1 trace table is partially under-specified

**Chapter table (lines 539–545):**

| Step | Current $h$ | Successors evaluated | Best successor $h$ | Chosen? |
|---|---|---|---|---|
| 1 | $-3$ | $-3$, $-4$ | $-3$ (tie) or back up to a $-4$ neighbour | the slide takes a side-step to a different $-3$ |

Looking at slide 5 directly: from the $h = -3$ state (second-row middle of the figure), the two arrows shown are labelled **$-3$** (right) and **$-4$** (down). The chapter's description ("$-3$ (tie) or back up to a $-4$ neighbour") confusingly suggests the algorithm might "back up" — but $-4$ is *worse* than $-3$, not "backing up" to a previously visited value. And "a different $-3$" implies a sideways move (which most hill-climbing variants would *not* take if using strict `<` termination per slide 13).

This is a pedagogical / accuracy gap rather than a missing concept, but it bears on whether the chapter accurately reports what slide 5 shows. The chapter elsewhere (line 547–551) correctly notes the trace shows a "friendly" start; it would be cleaner to say outright: *"the slide allows side-step moves between equal-valued neighbours; this is a stochastic / first-choice hill-climbing variant (slide 13's 'variants' bullet), not strict hill climbing."*

**Fix:** clarify the table row 1 to flag that the trace assumes a side-stepping variant and cross-reference §3.4.

**Evidence:** PDF slide 5; chapter lines 539–545.

### P1-5. Slide 18 (text-only SA prose) — one concept-line not represented in the chapter

**Slide 18** has five bullet points; the chapter §3.5 covers four of them. The one it does **not** explicitly carry over is the framing line:

> "**Picks random** rather than best state move as in hill-climbing."

The chapter §3.5 jumps into the acceptance rule (lines 270–286) without first stating that — unlike hill climbing, which evaluates **all** neighbours and picks the best — simulated annealing **picks one random neighbour** per step. This is the structural difference between the two algorithms, and slide 18 calls it out explicitly. The chapter's §4.2 pseudocode (line 459) does encode it (`next ← a random neighbour of current`), and §4.4 table mentions "$O(1)$ — evaluate one neighbour", but no §3 prose says "SA picks one random neighbour rather than the best — a fundamental departure from hill climbing's all-neighbours-then-argmax".

**Fix:** add a sentence in §3.5 (right after the "defect we are fixing" paragraph): *"A second fundamental departure: where hill climbing evaluates all neighbours and moves to the best, simulated annealing samples a single random neighbour per step and decides whether to accept it. This makes per-step cost $O(1)$ rather than $O(b)$."* This brings slide 18 into compliance and pre-positions the §4 complexity table.

**Evidence:** PDF slide 18 (bullet 3); chapter §3.5 lines 261–309.

---

## P2 — NICE TO HAVE

### P2-1. The figure catalogue's SKIP list omits slide 2's 3-D paraboloid as a "USE" only with caveats

`fig01-objective-landscape.png` is extracted from slide 2; the slide also has a substantial text overlay ("Local search algorithms — Some types of search problems…"). The catalogue's entry says "(3-D bumpy paraboloid graphic)" but the page-rendered image *includes the text*. That's fine for embedding, but a sharper note would say "page-render includes the lecturer's text overlay; the graphic itself is a 3-D bumpy paraboloid". Cosmetic.

### P2-2. Slides 23 ("?" mannequin) and 21 (DNA-helix decoration) are correctly SKIPped, but the catalogue could be marginally tightened to note that slide 21's *content* (Genetic Algorithms — History: Holland 1970s, popular late 1980s, Darwin, etc.) **is** carried into the chapter even though the *image* is decorative. The current catalogue line 65 just says "Slide 21 (stock DNA-helix illustration introducing GA history — purely decorative)" — true of the image, but a reader auditing concept completeness might worry the *bullets* on that slide were dropped. They weren't (chapter §3.6 picks them up), but the catalogue could say so.

### P2-3. Catalogue's "Coverage check" at the bottom (line 71–80) is excellent — every "Approaches" topic from slide 3 has at least one embedded figure. Could be made tighter by adding a one-line note on which sections of the chapter each figure embeds at (the table column already does this per-row, but a roll-up across sections would help). Cosmetic.

### P2-4. Slide 47 mentions "no general theory to deduce good values" for GA parameters. The chapter §6 "Bigger population = better — half-true" captures this exactly (line 745). Excellent. Could also be referenced from §3.6 / §4.3. Cosmetic.

### P2-5. The chapter (line 218) says: *"The slide-13 pseudocode uses `<`, which terminates only on a *strict* decrease and would happily traverse plateaux of equal value forever — a known weakness."* This is a worthwhile clarification, but it would benefit from cross-referencing the **shoulder vs plateau vs flat local maximum** distinction in §3.2 (the chapter does name these — line 187 — but doesn't link the `<` vs `≤` discussion to them). Adds clarity, not concept-completeness.

---

## EVIDENCE

**Slides inspected (all 50):**
- Slide 1 (title) — correctly SKIPped in catalogue; not expected in chapter.
- Slide 2 (objective function) — fig01 ✓ embedded line 26.
- Slide 3 (approaches list) — covered chapter §1 lines 39–43; SKIP justified.
- Slide 4 (hill-climbing motivation, "Everest in fog with amnesia") — covered §2.B (line 72) and §3.3 (line 234); SKIP justified.
- Slide 5 (8-puzzle hill climbing) — fig02 ✓ embedded line 535; §5.1.
- Slide 6 (US-map TSP screenshot) — correctly SKIPped (decorative).
- Slide 7 (TSP pairwise exchange) — fig03 ✓ embedded line 562; §5.2.
- Slide 8 (n-queens problem statement) — SKIPped (subsumed by slide 9 per catalogue).
- Slide 9 (4-queens local improvement) — fig04 ✓ embedded line 576; §5.3.
- Slide 10 (8-queens h=17 board) — fig05 ✓ embedded line 586; §5.4.
- Slide 11 (h=17 successors) — fig06 ✓ embedded line 593; §5.4; "8*7=56" successors verified.
- Slide 12 (Example Solution) — fig07 ✓ embedded line 603 — **P0-1: caption misrepresents leftmost board's $h$ values**.
- Slide 13 (Hill-climbing pseudocode) — text-only; SKIP justified; covered §3.3 lines 198–219 and §4.1 lines 422–448 — note the `<` vs `≤` discrepancy is correctly flagged.
- Slide 14 (Hill-climbing complete/optimal?) — fig08 ✓ embedded line 619; §5.5 — **P1-2: continuous-space footnote conflated with Ridge**.
- Slide 15 (state-space landscape) — fig09 ✓ embedded line 180; §3.2.
- Slide 16 (Simulated annealing motivation) — text-only; SKIP justified; §3.5 lines 261–268.
- Slide 17 (SA pseudocode) — text-only; SKIP justified; §4.2 lines 451–470.
- Slide 18 (SA prose) — text-only; SKIP justified — **P1-5: "picks random rather than best" framing missing from §3.5**.
- Slide 19 (Temperature curves) — fig10 ✓ embedded line 287; §3.5.
- Slide 20 (SA convergence + MCMC) — text-only; SKIP justified — **P1-1: MCMC named concept dismissed without gloss**.
- Slide 21 (GA history) — SKIPped (decoration); content carried in §3.6.
- Slide 22 (Evolution in real world) — text-only; SKIP justified; §3.6 lines 318–326 and §8.5 dictionary lines 873–886.
- Slide 23 ("?" mannequin) — SKIP justified.
- Slide 24 (blind generate-and-test) — text-only; SKIP justified; §3.6 implicit motivation.
- Slide 25 (can we use this dumb idea) — text-only; SKIP justified.
- Slide 26 (less-dumb GA idea) — text-only; SKIP justified; §3.6.
- Slide 27 (How to encode a solution) — text-only; SKIP justified; §3.6 / §5.6.
- Slide 28 (silly example setup) — text-only; SKIP justified; §5.6 lines 626–633.
- Slide 29 (oil-road positions) — fig11 ✓ embedded line 634; §5.6.
- Slide 30 (search space text) — text-only; SKIP justified; §3.6 / §3.7.
- Slide 31 (binary string encoding) — fig12 ✓ embedded line 638; §5.6.
- Slide 32 (oil fitness curve) — fig13 ✓ embedded line 642; §5.6.
- Slide 33 (summary so far) — text-only; SKIP justified.
- Slide 34 (search space dimensions) — text-only; SKIP justified; §3.7.
- Slide 35 (fitness landscapes) — fig14 ✓ embedded line 402; §3.7.
- Slide 36 (search space small-improvements) — text-only; SKIP justified; chapter §3.7 line 404–409 quotes verbatim.
- Slide 37 (back to GA algorithm) — text-only; SKIP justified.
- Slide 38 (adding reproduction) — text-only; SKIP justified.
- Slide 39 (crossover overview) — text-only; SKIP justified; §3.6.
- Slide 40 (selecting parents — roulette) — text-only; SKIP justified; §3.6.1.
- Slide 41 (example population table) — fig15 ✓ embedded line 652; §5.7.
- Slide 42 (roulette wheel selection) — fig16 ✓ embedded line 656; §5.7.
- Slide 43 (crossover recombination) — fig17 ✓ embedded line 660; §5.7.
- Slide 44 (mutation) — fig18 ✓ embedded line 664; §5.7.
- Slide 45 (GA algorithm full) — text-only; SKIP justified; §4.3.
- Slide 46 (variants of GA) — text-only; SKIP justified; covered §3.6 (lines 334–337, 345–346).
- Slide 47 (parameters to tune) — text-only; SKIP justified; §6 lines 741–746 and §8.6.
- Slide 48 (GA summarised) — text-only; SKIP justified; §4.3 lines 478–504.
- Slide 49 (Summary: Local Search) — text-only; SKIP justified; chapter §8 cheat-sheet.
- Slide 50 (Thank you) — SKIPped, no content.

**Chapter sections cross-checked:** §1 motivation, §2 analogies, §3.1–§3.7 core concepts, §4.1–§4.4 algorithms + comparison table, §5.1–§5.8 worked examples, §6 pitfalls, §7 connections, §8 cheat-sheet.

**Catalogue cross-checked:** all 18 entries against the chapter; all SKIP justifications against the source PDF.

**Files verified to exist on disk:** all 18 `fig01..fig18` PNGs in `study/extracted_figures/L05/` (sizes 70k–1.6 MB; all > 1 KB threshold).

---

## Report to PM

**Assignment recap:** L05 Round 1 — Lecture Reviewer #1 (Concept Completeness incl. Figures) per spec §7.1.

**Status:** Fail (NEEDS_REVISION) — one P0 caption error, five P1 concept/coverage gaps, five P2 polish items.

**P0 findings:**

1. **`L05-Local-Search.md` line 603** — Slide-12 figure caption claims the leftmost board's best row gives $h = 0$. Slide 12 actually shows the leftmost board's best row giving $h = 1$ (the local-minimum trap the lecturer flags). Rewrite the caption per the suggested wording in P0-1 to correctly describe each of the three boards in slide 12.

**P1 findings:**

1. **`L05-Local-Search.md` lines 305–307** — MCMC is mentioned but dismissed; concept-completeness requires a one-sentence gloss even if depth is out of scope.
2. **`L05-Local-Search.md` line 189** — Slide-14's continuous-space footnote (step-size sensitivity, slow convergence) is conflated with the Ridge concept. Disentangle and add a continuous-space sentence in §3.2 or §3.3.
3. **`study/extracted_figures/L05/figures.md` lines 81–84** — Catalogue claims chapter has "Mermaid diagram or in-text prose"; chapter has zero Mermaid blocks. Drop the Mermaid clause from the catalogue or add Mermaid diagrams.
4. **`L05-Local-Search.md` line 542** — §5.1 trace table row 1 has confusing wording ("back up to a $-4$ neighbour"). Clarify that the trace assumes a side-stepping / stochastic hill-climbing variant from §3.4.
5. **`L05-Local-Search.md` §3.5** — Slide 18's "picks random rather than best state move as in hill-climbing" framing is missing from the prose. Add one sentence positioning SA's $O(1)$ per-step cost vs hill climbing's $O(b)$.

**P2 findings:**

1. Catalogue entry for fig01 could note the page-render includes text overlay.
2. Catalogue's SKIP entry for slide 21 could note the *content* (Holland 1970s, late-1980s, Darwin) is preserved even though the image isn't.
3. Catalogue's coverage roll-up could include chapter section anchors per topic.
4. Slide-47 parameter-tuning advice could be cross-referenced from §3.6 / §4.3 in addition to §6.
5. The chapter's `<` vs `≤` discussion (line 218) could explicitly cross-reference the plateau/shoulder/flat-local-max distinction in §3.2.

**QA Checklist (§7) status:** N/A (this is a study-document review, not an engineering feature).

**Acceptance criteria (§1) status:** N/A.

**DOCUMENT.md audit:** N/A.

**Out-of-scope observations:** none flagged outside Reviewer #1 lens (mathematical rigor, pedagogical clarity, exam-readiness are other reviewers' lenses).

**Concerns / risks:**
- P0-1 is the highest-impact item — it would actively mislead a student studying from chapter + slides side-by-side, *especially* given that the chapter prose immediately below (lines 605–610) correctly describes the local-minimum trap, creating internal contradiction.
- The figure catalogue is otherwise excellent (every SKIP justified, every USE embedded, page-render rationale documented per spec §6.1.1). No figures were missed from the source PDF.

**What PM should do next:** Dispatch a reviser to fix P0-1 and all five P1s, then re-QA. P2s can be deferred to a later round or accepted as caveats.

**DOCUMENT.md updated:** N/A for QA.
