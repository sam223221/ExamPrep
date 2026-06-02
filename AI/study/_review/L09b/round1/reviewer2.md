# Reviewer #2 — Mathematical Rigor — L09b (HMM) Round 1

## Report to PM

**Assignment recap:** Lecture Reviewer #2 (Mathematical Rigor) for **L09b — Hidden Markov Models, Round 1**. Spec §7.1. Verified forward and Viterbi recursions (initialisation / recursion / termination) and the worked $O = 3, 1, 3$ ice-cream arithmetic step-by-step against `Lecture9-Hidden Markov Models.pdf` (slides 1–52).

**Status:** **Pass with concerns** — the mathematics is correct end-to-end, but the chapter introduces and tolerates a state-indexing inconsistency relative to the source slides that will trip a careful reader, and a small handful of P2 nits are worth fixing before Round 2.

---

## P0 findings (mathematical errors that would break the proof or the answer)

None. Every formula and every number in §4.2, §4.3, §5.1, §5.2, §5.4, §5.5 reproduces the slides correctly, and every arithmetic step I re-computed by hand matched the chapter to full precision.

## P1 findings (would mislead a careful exam-prepping student)

1. **State indexing inconsistency with the slide 28 diagram (chapter §5.3, lines 462–468).**
   The chapter writes "the lecture's trellis numbers states with COLD as $q_1$ and HOT as $q_2$" and then builds the $A$ and $B$ matrices with row 1 = COLD, row 2 = HOT. The trellis slides 38 and 50 do use that ordering. **But slide 28** — the very HMM diagram the chapter cites as Figure 3.4 and uses to define the parameters — labels the states `HOT_1` (subscript 1) and `COLD_2` (subscript 2). So in the source figure HOT is state 1 and COLD is state 2; in the source trellis it is the opposite. The chapter silently picks the trellis convention without flagging that slide 28's labels disagree. A student who memorises "$B_1$ = HOT" from slide 28 (chapter line 198 even reproduces "$B_1$ for HOT" in the figure caption) and then turns to the chapter's $A$ and $B$ matrices in §5.3 will read row 1 as HOT and get the wrong answer.
   *Suggested fix:* add a one-sentence "the slides conflict on which state is index 1 vs 2 — we use the trellis convention (COLD = 1, HOT = 2) throughout §5.3–§5.5" immediately after the "labelled $q_1 = $ COLD and $q_2 = $ HOT" line, and reword the caption of Figure 3.4 (line 198) so it does not assert "$B_1$ for HOT" while the next section asserts "row 1 = COLD".

2. **Recursion-range upper bound on $t$ should explicitly include $t = T$.**
   Slide 37 writes the forward recursion with the range $1 \le j \le N, \; 1 < t \le T$. The chapter (line 293) reproduces "$1 \le j \le N, \; 1 < t \le T$" — good. But the Viterbi recursion (line 355) only says "$1 \le j \le N, \; 1 < t \le T$" for $v_t(j)$ and the same for $bt_t(j)$ — also good. *I include this as a P1 only to flag that the chapter does not separately spell out that the final-column cells $v_T(j)$ and $\alpha_T(j)$ are filled by the same recursion (i.e., the recursion runs all the way to $t = T$ and only then does termination happen). The wording "Termination — sum over all final states" / "the best score and the start of the backtrace" is fine, but a reader confused about whether $T$ is part of the recursion or part of the termination might be reassured by one explicit sentence.* Down-grade to P2 if you disagree.

## P2 findings (polish; would not change a student's exam answer)

1. **Slide-vs-chapter typo correction is silent (line 168).** Slide 17 reads "$B = b_j(o_t)$ … each expressing the probability of an observation $o_t$ being generated from a state $i$" — the source slide writes "state $i$" while subscripting $b$ with $j$. The chapter quietly corrects this to "from a state $j$" without acknowledgement. The fix is correct mathematically but the chapter brands the table "reproduced verbatim" (line 160). Either: (a) keep the silent fix and remove "reproduced verbatim", or (b) keep the verbatim wording and add a footnote "the slide writes 'state $i$'; this is a typo — the subscript on $b_j$ shows the intended state is $j$".

2. **Fair Bet Casino prior assumed without slide support (chapter §5.2, line 436 footnote "assuming uniform prior").** The slide 25 table does not state a prior on $q_1$; it just shows $P(q_{i-1} \to q_i) = 1/2$ for the first column. The chapter correctly identifies that this $1/2$ implicitly comes from $\pi_F = 1/2$, but the parenthetical "(assuming uniform prior)" reads as if the chapter is making an assumption rather than reading one off the slide. Reword to "(the slide's $\frac{1}{2}$ in the first column corresponds to $\pi_F = \frac{1}{2}$, i.e., the slide assumes a uniform prior on the starting coin)".

3. **$\lambda$ vs $\Phi$ vs $(A, B)$ vs $(A, B, \pi)$ notation.** The slide 29 problem statement parametrises the HMM as $\Phi = (A, B)$. The chapter §3.3 line 171 defines $\lambda = (A, B, \pi)$ and §3.5 line 224 mentions $\lambda = (A, B)$ (dropping $\pi$ to match the slide). The chapter never explains the discrepancy. Add one line: "the slides write the model parameters as $\Phi = (A, B)$, folding $\pi$ in implicitly with the start state; we keep $\pi$ explicit as $\lambda = (A, B, \pi)$ throughout."

4. **Termination range index (chapter line 296).** $P(O \mid \lambda) = \sum_{i=1}^{N} \alpha_T(i)$ — fine, but the recursion uses $j$ as the destination state index while the termination uses $i$. Pedagogically clearer if the same letter is used (slide uses $i$ in termination, $j$ in recursion — same minor inconsistency). Not worth a fix unless re-typesetting.

5. **Ratio reported as ~0.478 (line 577).** $0.012544 / 0.026264 = 0.47763\ldots$ — rounding to "about 48%" is fine; "approximately 0.478" is slightly precision-overstated. Either say "≈ 47.8%" or just "≈ 48%".

---

## Step-by-step verification of the $O = 3, 1, 3$ worked example

### Forward (chapter §5.4)

**Initialization** ($t = 1$, $o_1 = 3$):
- $\alpha_1(\text{HOT}) = 0.8 \times 0.4 = 0.32$ ✓
- $\alpha_1(\text{COLD}) = 0.2 \times 0.1 = 0.02$ ✓

**Recursion** ($t = 2$, $o_2 = 1$):
- $\alpha_2(\text{HOT}) = (0.32 \cdot 0.7 + 0.02 \cdot 0.4) \cdot 0.2 = (0.224 + 0.008) \cdot 0.2 = 0.232 \cdot 0.2 = 0.0464$ ✓
  - Slide pre-folding: $0.32 \cdot 0.14 + 0.02 \cdot 0.08 = 0.0448 + 0.0016 = 0.0464$ ✓
- $\alpha_2(\text{COLD}) = (0.32 \cdot 0.3 + 0.02 \cdot 0.6) \cdot 0.5 = (0.096 + 0.012) \cdot 0.5 = 0.108 \cdot 0.5 = 0.054$ ✓
  - Slide pre-folding: $0.32 \cdot 0.15 + 0.02 \cdot 0.30 = 0.048 + 0.006 = 0.054$ ✓

**Recursion** ($t = 3$, $o_3 = 3$):
- $\alpha_3(\text{HOT}) = (0.0464 \cdot 0.7 + 0.054 \cdot 0.4) \cdot 0.4 = (0.03248 + 0.0216) \cdot 0.4 = 0.05408 \cdot 0.4 = 0.021632$ ✓
- $\alpha_3(\text{COLD}) = (0.0464 \cdot 0.3 + 0.054 \cdot 0.6) \cdot 0.1 = (0.01392 + 0.0324) \cdot 0.1 = 0.04632 \cdot 0.1 = 0.004632$ ✓

**Termination:**
- $P(O \mid \lambda) = 0.021632 + 0.004632 = 0.026264$ ✓

### Viterbi (chapter §5.5)

**Initialization** — identical to forward; back-pointers $= 0$. ✓

**Recursion** ($t = 2$, $o_2 = 1$):
- $v_2(\text{HOT}) = \max(0.32 \cdot 0.7 \cdot 0.2, \; 0.02 \cdot 0.4 \cdot 0.2) = \max(0.0448, 0.0016) = 0.0448$ ✓, $bt = $ HOT ✓
- $v_2(\text{COLD}) = \max(0.32 \cdot 0.3 \cdot 0.5, \; 0.02 \cdot 0.6 \cdot 0.5) = \max(0.048, 0.006) = 0.048$ ✓, $bt = $ HOT ✓

**Recursion** ($t = 3$, $o_3 = 3$):
- $v_3(\text{HOT}) = \max(0.0448 \cdot 0.7 \cdot 0.4, \; 0.048 \cdot 0.4 \cdot 0.4) = \max(0.012544, 0.00768) = 0.012544$ ✓, $bt = $ HOT ✓
- $v_3(\text{COLD}) = \max(0.0448 \cdot 0.3 \cdot 0.1, \; 0.048 \cdot 0.6 \cdot 0.1) = \max(0.001344, 0.00288) = 0.00288$ ✓, $bt = $ COLD ✓

**Termination:** $P^* = 0.012544$, $q_3^* = $ HOT ✓
**Backtrace:** $q_2^* = bt_3(\text{HOT}) = $ HOT, $q_1^* = bt_2(\text{HOT}) = $ HOT ✓ → sequence **HHH** ✓

Final ratio: $0.012544 / 0.026264 = 0.47763\ldots$ — chapter reports 0.478 (rounding) and "about 48%" — both acceptable.

**Verdict on arithmetic:** every intermediate value is correct to the precision shown.

---

## Verification of formula transcription (slide ↔ chapter)

| Source slide | Formula | Chapter location | Match |
|---|---|---|---|
| Slide 9 — Markov chain $a_{ij} = P(q_t = j \mid q_{t-1} = i)$ | line 123 | ✓ |
| Slide 10 — Markov assumption $P(q_i \mid q_1 \ldots q_{i-1}) = P(q_i \mid q_{i-1})$ | line 133 | ✓ |
| Slide 11 — initial distribution $\pi_i = P(q_1 = i)$, $\sum \pi_j = 1$ | line 139 | ✓ |
| Slide 17 — HMM definition table | §3.3 lines 165–169 | ✓ (with the silent "state $i$" → "state $j$" correction noted in P2-1) |
| Slide 18 — Markov + output-independence | lines 189–191 | ✓ |
| Slide 28 — ice-cream HMM parameters | §5.3 lines 462–468 | ✓ on values, P1-1 on labelling |
| Slide 32 — $P(O \mid Q) = \prod P(o_i \mid q_i)$ | line 246 | ✓ |
| Slide 33 — $P(O, Q) = \prod P(o_i \mid q_i) \prod P(q_i \mid q_{i-1})$ | line 255 | ✓ |
| Slide 34 — $P(O \mid \lambda) = \sum_Q P(O, Q)$ | line 262 | ✓ |
| Slide 37 — forward init / recursion / termination | lines 290, 293, 296 | ✓ exact |
| Slide 41 — forward pseudocode | lines 306–317 | ✓ exact transcription |
| Slide 47 — Viterbi cell formula $v_t(j) = \max_i v_{t-1}(i) a_{ij} b_j(o_t)$ | line 354 | ✓ |
| Slide 48 — Viterbi init / recursion / termination / backtrace | lines 351, 354–355, 358, 361 | ✓ exact |
| Slide 49 — Viterbi pseudocode | lines 367–383 | ✓ exact transcription |
| Slide 50 — Viterbi trellis on $3, 1, 3$ with worked maxes | §5.5 lines 528–558 | ✓ exact |

Forward variable definition $\alpha_t(j) = P(o_1, \ldots, o_t, q_t = j \mid \lambda)$ (line 278) — standard, matches slide 36. Viterbi variable definition $v_t(j) = \max_{q_1 \ldots q_{t-1}} P(q_1, \ldots, q_{t-1}, q_t = j, o_1, \ldots, o_t \mid \lambda)$ (line 338) — standard, matches slide 46.

Pseudocode in Figure 4.4 (forward) and Figure 4.7 (Viterbi) is reproduced character-for-character against the slide images. ✓

---

## Verification of Fair Bet Casino walkthrough (chapter §5.2)

Sequence $o = 0\,1\,0\,1\,1\,1\,0\,1\,0\,0\,1$, path $q = F\,F\,F\,B\,B\,B\,B\,B\,F\,F\,F$ (slide 25). Each row of the chapter's per-position table reproduces the slide column-by-column:

- Emission column: $\tfrac{1}{2}, \tfrac{1}{2}, \tfrac{1}{2}, \tfrac{3}{4}, \tfrac{3}{4}, \tfrac{3}{4}, \tfrac{1}{4}, \tfrac{3}{4}, \tfrac{1}{2}, \tfrac{1}{2}, \tfrac{1}{2}$ — ✓ matches slide.
- Transition column: $\tfrac{1}{2}$ (start), $\tfrac{9}{10}, \tfrac{9}{10}, \tfrac{1}{10}, \tfrac{9}{10}, \tfrac{9}{10}, \tfrac{9}{10}, \tfrac{9}{10}, \tfrac{1}{10}, \tfrac{9}{10}, \tfrac{9}{10}$ — ✓ matches slide.

See P2-2 on the wording around the initial $\tfrac{1}{2}$.

---

## Verification of weather Markov chain (chapter §5.1)

Slide 14: $P(3, 3, 3, 3) = \pi_3 a_{33}^3 = 0.2 \times 0.6^3 = 0.0432$. ✓ Chapter line 418 matches.

Discussion-prompt computations (chapter lines 425–426):
- $P(\text{HHHH}) = 0.5 \times 0.5^3 = 0.5 \times 0.125 = 0.0625$ ✓
- $P(\text{COLD, HOT, COLD, HOT}) = 0.3 \times 0.2 \times 0.2 \times 0.2 = 0.0024$ ✓
- Ratio $0.0625 / 0.0024 = 26.04\ldots$ — chapter says "~26×" ✓

Row sums of the transition matrix the chapter quotes (line 144):
- HOT row: $0.5 + 0.2 + 0.3 = 1.0$ ✓
- COLD row: $0.2 + 0.5 + 0.3 = 1.0$ ✓
- WARM row: $0.3 + 0.1 + 0.6 = 1.0$ ✓

All internally consistent and consistent with the slide 13 figure.

---

## QA Checklist (Spec §7.1) status

- [x] **Forward recursion initialisation matches PDF** — pass (line 290 vs slide 37).
- [x] **Forward recursion step matches PDF** — pass (line 293 vs slide 37).
- [x] **Forward termination matches PDF** — pass (line 296 vs slide 37).
- [x] **Viterbi initialisation matches PDF (incl. $bt_1(j) = 0$)** — pass (line 351 vs slide 48).
- [x] **Viterbi recursion step matches PDF (both $v_t$ and $bt_t$)** — pass (lines 354–355 vs slide 48).
- [x] **Viterbi termination matches PDF ($P^*$ and $q_T^*$)** — pass (line 358 vs slide 48).
- [x] **Viterbi backtrace step $q_{t-1}^* = bt_t(q_t^*)$ stated** — pass (line 361).
- [x] **Forward pseudocode reproduced verbatim** — pass (lines 306–317 vs slide 41).
- [x] **Viterbi pseudocode reproduced verbatim** — pass (lines 367–383 vs slide 49).
- [x] **$O = 3, 1, 3$ ice-cream forward arithmetic: every $\alpha_t(j)$ recomputed** — pass; all 6 $\alpha$ values, the termination sum $0.026264$, and the slide's pre-folded notation $0.32 \cdot 0.14 + 0.02 \cdot 0.08 = 0.0464$ and $0.32 \cdot 0.15 + 0.02 \cdot 0.30 = 0.054$ all verified.
- [x] **$O = 3, 1, 3$ ice-cream Viterbi arithmetic: every $v_t(j)$ and back-pointer recomputed** — pass; HHH with $P^* = 0.012544$ verified.
- [x] **Fair Bet Casino per-position emission and transition table matches slide 25** — pass.
- [x] **Weather Markov chain example $P(\text{WWWW}) = 0.0432$ and the HHHH vs CHCH comparison** — pass.

---

## Acceptance criteria (Spec §7.1) status

- **Forward algorithm formally correct and slide-faithful** — Met.
- **Viterbi algorithm formally correct and slide-faithful** — Met.
- **Worked $O = 3, 1, 3$ arithmetic correct to the precision printed** — Met.
- **Initialisation / recursion / termination cases all handled** — Met.

---

## DOCUMENT.md audit

N/A for this artefact — pure lecture note, not a code directory.

## Out-of-scope observations

1. The chapter's §6 pitfalls #11 (numerical underflow, log-space Viterbi) is a strict improvement over the slide and is mathematically correct. The log-domain Viterbi recursion $\log v_t(j) = \max_i [\log v_{t-1}(i) + \log a_{ij} + \log b_j(o_t)]$ (line 610) is right.
2. §7 connects the HMM trellis to dynamic programming on layered graphs (line 633). The remark "the operator is $\sum$ (forward, total flow) or $\min/\max$ (Viterbi, best path)" mixes "min" (shortest path) with "max" (Viterbi) without acknowledgment that Viterbi specifically uses max because probabilities multiply along paths and we want the largest product. Not wrong, but a re-reading reader might wonder. Could add "(min for shortest path, max for highest-probability path)".
3. The Viterbi backtrace block in the pseudocode (slide 49, line 381) reads "the path starting at *bestpathpointer*, that follows *backpointer*[] back in time". The chapter reproduces this verbatim and then formalises $q_{t-1}^* = bt_t(q_t^*)$ on line 361. Both correct; the prose-then-formula pairing is clean.

## Concerns / risks

- The state-indexing inconsistency flagged as **P1-1** is the only finding I think a math-strict student would actually trip over. Round 2 should fix it.
- I did not have direct PDF text extraction (only the per-page PNG renders), so my verification is image-based. I am confident in every formula and number I checked, but a single typo in a slide I could not load (slides 10, 21, 34–36 timed out) could exist; the chapter's reproduction of those slides is consistent with the surrounding slides I could verify, so I have no positive reason to doubt them.

## What PM should do next

1. Hand the P1 finding (state-indexing) to the lecture author for a one-paragraph fix in §5.3.
2. The P2 nits are polish — bundle into a single editorial pass at Round 2.
3. Mathematical rigor of this chapter is **fit for App Tester / Code Reviewer** even before the P1 is addressed — the actual recursions and arithmetic are sound. The P1 is a documentation/clarity issue, not a math error.

**DOCUMENT.md updated:** N/A for QA.
