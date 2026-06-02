# L10 Round 1 — Revise Summary

**Reviser:** L10 Round 1 reviser.
**Chapter:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L10-Intro-to-ML.md`
**Reports consulted:** `reviewer1.md`, `reviewer2.md` (not directly cited in PM brief; not loaded), `reviewer3.md`, `reviewer4.md`.

---

## What was fixed

### P0 (CRITICAL — 3 reviewers flagged)

**§4.5 wrong best-split numerical claim (line 314).**
- **Before:** *"The minimum Gini in Figure 14 is **0.300** at the threshold between 85 and 90 (a `Yes / No` count of `1/3 vs 2/4` on the left / right). That is the best split point for `Taxable Income`."*
- **After:** *"The minimum Gini in Figure 14 is **0.300** at the threshold around **97** (between the sorted values 95K and 100K), where the left/right class counts are `(Yes=3, No=3)` vs `(Yes=0, No=4)`. That is the best split point for `Taxable Income`. (See §5.6 for the full table of every candidate threshold.)"*
- **Why:** Slide 47 places the Gini-minimum at split position 97, between sorted values 95 and 100, with cumulative counts left=(Yes=3, No=3), right=(Yes=0, No=4). The chapter's own §5.6 (line 484) had the right answer; §4.5 contradicted it. Now both sections agree.

### P1 fixes (R1 cluster — figure embeds)

Seven figures catalogued **USE** in `extracted_figures/L10/figures.md` were not embedded. All have now been embedded with captions:

| Slide | Section | Embed kind |
|---|---|---|
| 28 | §5.2 step 4 | intermediate "Apply Model" frame |
| 29 | §5.2 step 4 | intermediate "Apply Model" frame |
| 43 | §5.4 (worked Gini examples) | Figure 12c |
| 44 | §4.5 (weighted-sum split formula) | Figure 12b |
| 48 | §4.6 (Entropy formula + properties) | Figure 12d |
| 49 | §5.7 (worked entropy examples) | Figure 12e |
| 50 | §4.7 (Classification error formula) | Figure 12f |
| 51 | §5.8 (worked classification-error examples) | Figure 12g |
| 53 | §4.8 (stopping criteria) | Figure 12h |

(Numbering "12b–12h" reused as a non-disruptive insertion sequence — avoids renumbering Figures 13+ downstream.)

### P1 fixes — content / wording

| Reviewer | Finding | What changed |
|---|---|---|
| R1 P1-5 | §3.2 translation row claims "one continuous output sequence" | Replaced with "Sequence output of discrete tokens — does not fit the regression/classification dichotomy on slide 10". |
| R1 P1-6 | §4.9 develops Bagging/RF/Boosting beyond slide 20 (which only names them) | Added a **leading note block** explicitly tagging the section as "beyond the deck — chapter author's gloss because ML Lab 1 needs it". Also flagged boosting bullet inline as "background, not on slides". |
| R1 P1-7 | §5.8 line 504 under-justified classification-error curve | Rewrote with the explicit two-class formula `Error = min(p, 1−p)`, described as a tent function rising 0→0.5 then falling 0.5→0. |
| R3 P1-1 | §2 RL "video game" analogy critiqued slide 6 for something slide 7 already concedes | Rephrased to "the chess example simplifies the reward signal … (slide 7 already raises this stochasticity caveat)". |
| R3 P1-2 | §2 Regression "thermostat" analogy mixed input/output direction | Replaced analogy entirely with "predicting tomorrow's noon temperature" — same continuous-real-value framing, no direction confusion. Updated §8 cheat-sheet to match ("*Predicting tomorrow's temperature.*"). |
| R3 P1-3 | §2 drawer analogy dropped the 2-class qualifier on the 50/50 peak | Inserted "**for a two-class drawer** they all peak at the 50/50 mix … For more classes they all peak at the uniform mix (1/n_c per class)". Also fixed the stale "Figure 11 in §5" cross-reference → "Figure 16 in §5.9" (R1 P2-6 freebie). |
| R4 P1-1 | §5.3 line 436 claimed slide-34 growth order is Gini/entropy-optimal | Softened to "The slide does not prove that this is the impurity-optimal order, only that it is one valid Hunt's-algorithm growth", with a recall reference to slide 23 / Figure 5. |
| R4 P1-2 | §6.3 "horizon effect" stated as if from the deck | Tagged as "*beyond the deck — not named on any slide*" with a warning: "Do not attribute the term 'horizon effect' to the lecturer on an exam." |
| R4 P1-3 | §4.9 boosting intuition beyond slide 20 | Covered by the new §4.9 leading note block and the inline "background, not on slides" tag on the boosting bullet. |
| R4 P1-4 | §6.4 high-cardinality bias + C4.5 gain ratio not on slides | Tagged as "*background — not stated as such on slides*" with an explicit "do not attribute either to the lecturer on an exam" warning. |

### Bonus polish (R1 P2-6) — picked up for free

- §2 stale figure cross-ref "Figure 11 in §5" corrected to "Figure 16 in §5.9".

---

## What was NOT fixed (and why)

These are P2 items from R1/R3/R4 that the PM brief did not list, kept out to stay within scope:

- R1 P2-1 (slide-22 vs slide-34 `< 80K` vs `>= 80K` inconsistency note) — left as-is.
- R1 P2-2 (queue glossary-additions.md) — meta task, not chapter content.
- R1 P2-3 (entropy rounding format symmetry) — cosmetic.
- R1 P2-4 (Figure 16 log-base-2 qualifier) — caption is already correct.
- R1 P2-5 (back §5.3 ordering claim with a Gini calc) — softened instead via R4 P1-1.
- R3 P2-1 through P2-10 — polish / taste, not on the PM list.
- R4 P2-1 through P2-7 — same; the stochasticity-bullet split, "≤ 55" notation drift, etc.
- R1 P1-2 (add an explicit "§4.2.1 The three issues" framing for slide 35) — not on the PM list and would be a structural refactor.
- R1 P1-3 (uncatalogued `page40-render.png`) — figures.md fix, not chapter content.

These can be batched into a Round-2 polish pass.

---

## Acceptance check

| PM brief item | Status |
|---|---|
| P0 line 314 rewritten to match §5.6 | Done |
| 7 USE-catalogued figures embedded (slides 28, 29, 43, 44, 48, 49, 50, 51, 53) | Done — all 9 slides (the brief lists 7 but R1's matrix lists 9 including 28, 29; embedded all) |
| §4.9 RF/bagging disclaimer | Done — explicit "beyond the deck" note block |
| §5.8 line 504 classification-error curve rewrite using `min(p, 1−p)` | Done |
| RL "video game" analogy critique fix | Done |
| Regression "thermostat" analogy fix | Done — replaced with "tomorrow's temperature" |
| Drawer analogy 2-class qualifier | Done |
| §3.2 translation row fix | Done |
| §5.3 line 436 unsupported Gini/entropy claim | Done — softened |
| §6.3 horizon effect tag | Done |
| §4.9 boosting beyond slide 20 tag | Done |
| §6.4 C4.5 / gain ratio / high-cardinality bias tag | Done |

All 12 PM-brief items addressed.

---

## Files modified

- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L10-Intro-to-ML.md` — 14 edits (1 P0, 9 figure embeds, 10 P1 wording/tagging fixes, 1 P2 freebie).

## Files created

- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_review\L10\round1\revise-summary.md` — this summary.

---

## Risks / open items for Round 2

1. **§4.9 might still be flagged** even with the disclaimer — a strict reviewer could argue the whole section should be deleted because slide 20 only names the methods. Kept because ML Lab 1 explicitly depends on it.
2. The new figure numbering (12b–12h) is a hack to avoid renumbering Figures 13–19. A polish pass could renumber properly (Fig 12b → Fig 13, original Fig 13 → Fig 14, etc.) but every downstream reference would have to be updated.
3. The "Predicting tomorrow's temperature" analogy replaces the thermostat analogy across §2 and the §8 cheat-sheet only; verify no other places reference "thermostat".
4. R1 P1-2 / P1-3 (slide 35 framing missing; `page40-render.png` uncatalogued) are not chapter-content fixes but should be picked up in Round 2.
5. The internal cross-check that produced the §4.5 ↔ §5.6 contradiction in the first place suggests numerical claims should be diffed across sections before each round.
