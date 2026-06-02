# L09a Round 1 — Revision Summary

**Reviser scope:** Apply P0 / P1 findings from the four round-1 reports to `study/lectures/L09a-Bayesian-Networks.md` and supporting files.

**Files modified:**

- `study/lectures/L09a-Bayesian-Networks.md` — large revision (chapter grew from 933 lines to ~1260; reading time bumped from ~75 min to ~90 min).
- `study/extracted_figures/L09a/figures.md` — fixed the P20 SKIP rationale and the inconsistent summary block.
- `study/lectures/DOCUMENT.md` — created (was missing per P1-6 in R1).
- `study/extracted_figures/L09a/DOCUMENT.md` — created (was missing per P1-6 in R1).

---

## P0 fixes applied

### From Reviewer 1 (Concept Completeness incl. Figures)

| Finding | Resolution |
|---|---|
| **P0-1** Four USE-marked figures not embedded (`page08-atomic-events.png`, `page33-anthrax-bn.png`, `page34-joint-table-2k.png`, `page55-compute-joint-entry-example.png`) | All four embedded. page08 → Figure 9.1 in §3.2 alongside the atomic-events bullet list. page34 → Figure 9.3 in §3.2 motivating the $2^k$-entries problem. page33 → Figure 9.9 in new §3.6a "Motivating example — diagnosing anthrax". page55 → Figure 9.26 in §5.7 setup. |
| **P0-2** Slides 31–33 (Anthrax / wide-mediastinum narrative) entirely missing from chapter prose | New §3.6a "Motivating example — diagnosing anthrax (slides 31–33)" added between §3.6 and §3.7. Walks the patient-presentation → uncertainty → wide-mediastinum-evidence → posterior-jumps story, with the slide-33 anthrax BN figure. |

### From Reviewer 3 (Pedagogical Clarity incl. Analogies)

| Finding | Resolution |
|---|---|
| **P0-1** §2 missing analogies for Bayes' rule, joint/atomic event, marginal, Markov condition (own analogy), CPT, chain rule, independence (unconditional), prior/posterior/evidence | §2 expanded from 4 to 14 analogies: thermometer (RV), master-spreadsheet (atomic event / joint), spreadsheet-projection (marginal), restrict-to-one-office (conditional probability), flip-the-causal-arrow (Bayes' rule), peel-off-variables (chain rule), behaviour-chart-on-fridge (CPT), two-questions-share-no-information (independence), gossip-graph (BN), parents-as-gatekeepers (Markov condition, with explaining-away caveat hint), once-I-know-the-rain (conditional independence — re-grounded in slide-41 *Traffic* version), weather-forecast-updating-after-lightning (prior/posterior/evidence), phone-book (inference by enumeration), gossip-graph-with-one-root (Naive Bayes). Each has a real "breakdown" caveat. |
| **P0-2** Only 1 of 12 §3 subsections back-links to §2; should be all | Back-link sentences added in §3.1, §3.2, §3.3, §3.5, §3.7, §3.8, §3.9, §3.10, §3.11, §3.13, §3.14 (§3.6 already had one). Each uses the "(Recall the *X* analogy from §2…)" template. |
| **P0-3** §3.13 has unjustified leaps (α dropped without intuition; lecture-late network referenced before defined; "4 joint computes" unexplained; phone-book analogy unused) | §3.13 rewrite: now (a) connects $\alpha$ to the §3.3 normalisation trick with a full paragraph; (b) explicitly explains "the number of joint entries is $2^{|Y|} = 2^2 = 4$"; (c) opens with the phone-book back-link; (d) flags the lecture-late network as a forward reference to §4.1. |
| **P0-4** Weak CI caveat (fashion-statement framing missed the actual statistical point) | Replaced with a real population-vs-instance breakdown: "conditional independence is a statement about the *whole population*, not a single day". |

### From Reviewer 4 (Exam Readiness)

| Finding | Resolution |
|---|---|
| **P0-1** §3.10 circular derivation (uses Markov condition to justify itself) | Rewritten as a four-step argument: (1) chain rule; (2) topological ordering; (3) prefix decomposition into parents + non-descendant non-parents; (4) Markov-condition substitution. Each step explicitly justified. |

---

## P1 fixes applied (key items)

### From Reviewer 4

- **P1-1 / P1-4 / P1-11 chain/fork/collider/explaining-away missing.** Added §3.9.1 "Three connection patterns — chain, fork, collider" with a comparison table and an explaining-away worked numerical example on the alarm network ($P(+b \mid +a) \approx 0.37$ vs $P(+b \mid +a, +e) \approx 0.003$).
- **P1-2 slide-48 verbatim query replaced.** §5.6 now has a "Slide 48 — the lecturer's worked sample joint" subsection computing $P(+b, \neg e, +a, \neg j, +m) = 6.57 \times 10^{-5}$, followed by the chapter's original "false-alarm" example $P(+j, +m, +a, \neg b, \neg e) = 6.28 \times 10^{-4}$ as a complementary case.
- **P1-3 Gaussian density formula missing.** §3.11 now includes the formula $f(x \mid \mu, \sigma^2) = (1/\sqrt{2\pi\sigma^2}) \exp(-(x-\mu)^2 / 2\sigma^2)$ with full numerical plug-ins for both class values in the slide-29 example (showing $\approx 0.0072$ and $\approx 1.2 \times 10^{-9}$).
- **P1-5 cost formula dropped $|D_X|$.** §3.13 and §4.4 cost formulas updated to $O(|D_X| \cdot n \cdot d^{|Y|})$.
- **P1-6 slide-30 NB-to-BN transition.** §3.11 now has a "Bridge to general BNs" subsection comparing the Naive Bayes factorisation to the extended-BN factorisation with $A_1 \to A_2$ added.
- **P1-7 slide 65 (expert vs data) missing.** Added §4.7 "Where does the Bayesian network come from?" with both options spelled out.
- **P1-8 slide 66 4-structure spectrum missing.** Added §4.6 "The BN trade-off spectrum" with a four-row comparison table (Strict / Naive Bayes / Sparse / Full).
- **P1-9 CPT-size two-number distinction.** §3.8 reorganised so the two numbers (cells $2^{k+1}$, independent parameters $2^k$) appear as bolded consecutive bullets, with the generic-domain formulas immediately after.
- **P1-10 alarm-network $P(+b \mid +j, +m)$ missing.** Added to §5.6 as a full inference-by-enumeration walkthrough — eight terms across two query values, with the final $\approx 0.284$ answer matching Russell & Norvig.
- **P1-12 dashed-line annotation caveat.** Added a paragraph after Figure 9.8 explaining that the slide-41 dashed line is a pedagogical annotation, not BN syntax.

### From Reviewer 3

- **P1-1 §3.7 cross-reference numbering.** §3.7 now correctly cites Markov (§3.9) and BN factorisation (§3.10) rather than the previous off-by-one (§3.8 / §3.9).
- **P1-1 "two things simultaneously" expanded.** §3.7 now has a paragraph spelling out that the Markov condition and the BN factorisation are two sides of the same coin.
- **P1-2 §3.9 heading.** Changed from "a.k.a. d-separation, informal version" to "special case of d-separation"; terminology note moved above the formal statement.
- **P1-3 "anti-correlated" intuition.** §3.5 now includes "knowing $A$ happened *rules out* $B$, so $P(B \mid A) = 0 < P(B)$".
- **P1-4 $X$ overloaded in §3.11.** Test record renamed from $X$ to $\mathbf{a}$ throughout the Naive Bayes section.
- **P1-5 Naive-Bayes leaves-don't-talk bridge.** §3.11 explicitly says the analogy half is the CI assumption.
- **P1-6 "non-parent ancestors are non-descendants" leap.** Eliminated by the four-step rewrite of §3.10.
- **P1-7 gossip-graph caveat split into two distinct breakdowns** (direction vs cycles).
- **P1-8 cheat-sheet analogies without §2 anchor.** All cheat-sheet one-liners now have a corresponding 2–4-sentence entry in §2.
- **P1-10 lecture-late narrative.** §4.1 now includes a paragraph telling the story of the two lecturers + sunny-traffic + robot-topic before the variable list.

### From Reviewer 1

- **P1-1 figures.md P20 SKIP rationale.** Rewritten to explicitly document that slide 48's factorisation formula and worked joint are reproduced inline (§3.10 and §5.6).
- **P1-2 "Cloud" analogy.** §2's conditional-independence analogy now uses the slide-41 Traffic version exclusively; "Cloud" mention removed.
- **P1-4 lecture-late parameter count.** §3.8 now states the explicit 10 vs 31 saving for the lecture-late network in addition to the alarm-network comparison.
- **P1-5 slide-50 textbook order vs slide-51 causal order.** §4.1 now has an "Ordering note" immediately after the variable list cross-referring to §6.7.
- **P1-6 DOCUMENT.md missing.** Created in both `study/lectures/` and `study/extracted_figures/L09a/`.

### From Reviewer 2

- **P2-1 Marie's wedding intermediate arithmetic.** §3.4 now computes with the exact fraction $5/365$ to recover the slide's $1/9 \approx 0.111$, and explicitly notes that rounding $P(R)$ to $0.014$ yields the alternative $\approx 0.1133$.

---

## P2 items addressed

- §3.5 "Conversely" → "For mutually exclusive events," (R4 P2-5).
- §3.7 "Ancestors" vocab added (R4 P2-7).
- §3.10 storage formula now consistently $O(n \cdot d^k)$ with $d^k$ instead of mixing $2^k$ and $d^k$ (R4 P2-8).
- §3.11 Naive Bayes graph noted as "star graph / root-and-leaves" (R4 P2-9).
- §8 cheat-sheet now opens with a flight-to-the-airport callback (R3 P2-2).
- §6.3 already mentions the base-rate fallacy — no change needed; the 11% Marie's-wedding callback already lands.
- §6 now includes §6.11 (collider trap) and §6.12 (normalisation forget).
- Figure caption monotonicity verified: 9.1 through 9.27, monotone and consecutive.

## P2 items deferred

- R4 P2-13 (deleting redundant §5.1–§5.5 restatements). The redundancy is intentional — §5 is a worked-examples index that exists to be a quick reference, and removing the section headings would make examples harder to find. Left as-is.
- R4 P2-6 (cutting the height/vocabulary example in §3.6). Kept both examples because the height/vocabulary one is the slide-40 source and Rain/Umbrella/Traffic is the slide-41 source; deleting either loses a slide citation.
- R3 P2-1 (§2 heading style consistency). The §2 rewrite uses a uniform "### {Concept} is like *{analogy}*." template throughout.
- R3 P2-7 (glossary back-linking from header bullets). The header glossary list is intentionally not link-decorated to keep the chapter readable on plain Markdown viewers; the `_shared/glossary.md` cross-reference exists in §3.9.
- R3 P2-4 (one canonical example). Multiple canonical examples are intentional — the Cavity/Toothache joint is the bedrock for §3.2–§3.3; A→B→{C,D} is the simplest BN for §3.7; alarm is the canonical full-CPT BN for §5.6; lecture-late is the build-from-scratch + inference walk-through for §4.1 + §5.8.

---

## Verification

- **All 4 missing USE figures embedded:** verified by `grep "page(08|33|34|55)"` returning 4 hits in `L09a-Bayesian-Networks.md`.
- **Figure numbering monotone:** verified 9.1–9.27 consecutive (one image each).
- **§2 analogy count:** 14 (up from 4); each has a "where the analogy breaks down" sentence.
- **§3 back-links:** every §3.X subsection (3.1, 3.2, 3.3, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.13, 3.14) has either a "Recall the X analogy from §2" sentence or a contextual back-reference. §3.4 (worked examples) and §3.12 (queries flavours) re-use §3.3's setup so back-links would be redundant.
- **§3.10 derivation no longer circular:** rewritten in four explicit steps.
- **Alarm network $P(+b \mid +j, +m) \approx 0.284$:** verified numerically — denominator $0.000592 + 0.001492 \approx 0.002084$, ratio $0.284$.
- **Gaussian density spot check:** $f(120 \mid 110, 2975) \approx 0.0072$ and $f(120 \mid 90, 25) \approx 1.2 \times 10^{-9}$ both reproduce the slide-29 values.
- **DOCUMENT.md present** in both `study/lectures/` and `study/extracted_figures/L09a/`.

---

## What round 2 should focus on

1. Spot-check the new §2 entries — do the analogies land for a first reader?
2. Re-read §3.9.1 (chain/fork/collider) — is the trichotomy clear? Is the explaining-away example accessible?
3. Re-verify the new arithmetic in §5.6 ($P(+b \mid +j, +m) \approx 0.284$) end-to-end.
4. Confirm that the §3.10 four-step derivation reads cleanly under exam pressure.
5. Cross-check the new §4.6 trade-off spectrum table — the parameter counts and edges should be correct for $n = 5$ Boolean variables.
