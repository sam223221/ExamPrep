# L09b (HMM) — Round 1 Revision Summary

**Artifact:** `study/lectures/L09b-HMM.md`
**Round:** 1
**Reviser brief:** Apply the P0/P1 fixes flagged by Reviewers 1–4.

---

## Fixes applied

### P0 from R3 — Missing §2 analogies + missing caveat

1. **Added §2.6 — first-order Markov assumption analogy** ("only checking the latest weather report"), with breakdown caveat about second-order chains and parameter explosion.
2. **Added §2.7 — initial distribution analogy** ("climatological prior on the day you arrived"), with breakdown caveat about priors being guessed / learned in practice and the "$\pi$ multiplies in exactly once at $t = 1$" reminder.
3. **Added §2.8 — filtering analogy** ("is it raining right now? versus how likely was the whole week?"), explicitly disambiguating textbook filtering from slide-Evaluation, plus a four-way taxonomy preview (filtering / smoothing / prediction / decoding).
4. **Added breakdown caveat to §2.5** (sum vs max): now flags back-pointers, magnitude differences, underflow, and Viterbi argmax tie ambiguity.
5. **Added umbrella analogy recalls** to §3.3 (formal HMM definition + the two assumptions), §4.1 (joint factorisation), §5.1, §5.2, §5.4, §5.5. The umbrella now appears as a recall in §3.1, §3.3, §4.1, and across all of §5 (previously only §3.1).

### P1 from R1 — Broken cross-references and figure

6. **Fixed L09a §3.7 → §3.13** (inference by enumeration) in §1.
7. **Fixed L09a §3.6 → §3.9** (Markov condition) — twice: once in the §3.2 glossary cross-link and once in §7 (Connections).
8. **Fixed L09a §3.1 → §3.3** (conditional probability / Bayes' rule) in §7. Consolidated with the Bayes' rule entry that previously sat under §3.3 (so §7 now has one entry pointing at the merged L09a §3.3 section).
9. **Fixed L02 §3.7 → §3.6** (environment taxonomy) in §7.
10. **§3.5 table header rewritten** for Problem 1: no longer equates "Evaluation" with "Filtering". New wording: "Likelihood evaluation (forward-algorithm output $P(O \mid \lambda)$); related to but *not identical to* filtering — see naming note below". Problem 2 row similarly tightened ("*Not* the same as smoothing").
11. **Slide 23 (Fair Bet Casino FSA) embedded** in §3.4 as Figure 3.6, with a caption that explicitly parallels Figure 3.4 (ice-cream HMM).
12. **State-numbering convention callout** added at the head of §5.3 — a prominent "⚠ Indexing convention" block flagging that slide 28 uses HOT = 1 / COLD = 2 but the trellis slides (38, 50) invert this, and stating that §5.3–§5.5 follow the trellis convention (COLD = 1, HOT = 2).
13. **$\lambda$ vs $\Phi$ notation caveat** added in §3.3 after the $\lambda = (A, B, \pi)$ definition: notes that slide 29 uses $\Phi = (A, B)$ and treats $\lambda$, $\Phi$, $(A, B, \pi)$, $(A, B)$ as the same model for exam purposes.

### P1 from R2 — Indexing convention

14. Covered by fix #12 (the §5.3 callout box).

### P1 from R3 — Analogy renaming, wrong cross-ref

15. **§2.3 lead rewritten** to use "totalling all the ways the story could have unfolded" throughout — the fight-then-makeup framing is dropped in favour of the section-title name, which is also the name used in §4.2 and §8. The §2.3 caveat now also covers the joint-vs-posterior distinction (was missing from R3's perspective).
16. **§2.1 cross-ref §3.4 → §3.3** (output-independence is defined in §3.3, not §3.4).

### P1 from R4 — Exam readiness gaps

17. **Added §4.6** — backward variable + smoothing. Defines $\beta_t(j) = P(o_{t+1}, \ldots, o_T \mid q_t = j, \lambda)$, the backward recursion, and the smoothing formula $P(q_t = j \mid O) = \alpha_t(j)\beta_t(j) / P(O \mid \lambda)$. Notes that forward + backward is the E-step of Baum–Welch.
18. **Added forward recursion derivation** in §4.2 — six-step derivation citing Markov (step 4) and output-independence (step 5) by name.
19. **Added "prediction" to the §3.5 naming-note** — now covers the full four-way standard taxonomy (filtering, smoothing, prediction, most-likely-explanation).

### Polish / secondary

20. Cheat-sheet (§8) "one-line analogy reminders" table expanded with new rows for *Markov assumption*, *initial distribution*, and *filtering*. The umbrella row now restores §2.1's filtering/Viterbi binding.
21. Pitfall #1 in §6 updated to point to §4.6 for smoothing and to include "prediction" as a fifth bullet.
22. Pitfall #1 reference list now includes §2.8.
23. Cross-link recalls added at §3.2 (both Markov assumption — to §2.2/§2.6 — and initial distribution — to §2.7) and at §3.5 (filtering — to §2.8).
24. Note added at §3.2 that the $q_0$/$a_{0j}$ slide-form and the $\pi_j$ textbook-form are equivalent (closes R4 polish #9).

---

## Items NOT addressed (intentionally, out of brief scope)

- P2 polish from R1, R2, R3, R4 (additional worked example, tabulated back-pointer matrix in §5.5, semiring framing, log-space promotion, etc.) — outside the brief's key-fix list.
- R3 P1-4 (move §4.4 sum-vs-max recall above the table) — not in brief.
- R4 P1-5 stationarity assumption promotion to §8 cheat sheet — not in brief.

These can be picked up in Round 2 if PM dispatches a follow-up pass.

---

## Verification

- All five broken cross-references re-anchored against the actual L09a and L02 table-of-contents (verified by `grep ^### 3` against both files).
- New §2 subsections (§2.6, §2.7, §2.8) each ship with a breakdown caveat per spec §7.1.
- §4.6 backward/smoothing math is the standard Rabiner-tutorial form; numerator $\alpha\beta$ at time $t$, denominator $P(O \mid \lambda)$.
- §3.5 table no longer asserts "Evaluation = Filtering".
- §5.3 indexing-flip is now a callout, not a parenthetical.
- Slide 23 figure file `page23-render.png` confirmed present in `study/extracted_figures/L09b/`.
- All section numbers (§2.6, §2.7, §2.8, §4.6) are unique and the chapter section list now reads: §1, §2.1–§2.8, §3.1–§3.5, §4.1–§4.6, §5.1–§5.5, §6, §7, §8.

---

## Diff scale

- ~14 net new analogies/sub-sections added (§2.6 / §2.7 / §2.8 / §4.6 + multiple recalls).
- ~5 cross-references corrected.
- ~3 tables/captions tightened.
- ~1 figure embedded.

Estimated round-trip exam-prep impact: **High.** The chapter now exposes the full standard HMM-task taxonomy, the backward/smoothing apparatus, the forward-recursion derivation, and a consistent state-indexing convention — all of which are likely exam-day catches.
