# L05 Local Search — Round 2, Reviewer 3 (Pedagogical Clarity incl. Analogies)

**Artifact under review:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L05-Local-Search.md` (revised after Round 1)
**Source PDF:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture5-Local Search.pdf` (50 slides, re-verified key slides 5, 11, 12, 13, 14, 17, 18, 41, 42, 43, 44)
**Round 1 verdict:** NEEDS_REVISION — 1 P0 (§5.1 silent rule switch), 13 P1 (most prominent: spec §7.1 violation — ~7 major concepts without §2 analogies).
**Lens:** I read this as the confused student who has done L02 + L03 but never seen local search. Spec §7.1: every major concept needs an everyday analogy + breakdown caveat, cross-linked from §3. Be harsh.

---

## VERDICT

**APPROVED with minor P2s outstanding** (one residual P1 — a wording slip in §2.E's "Temperature schedule" caveat — discussed below; recoverable in a five-minute touch-up by the Reviser without a full new revision pass).

The revision is **a substantial improvement** on Round 1. Every P0 and the major P1s I flagged in Round 1 have been addressed in a substantive, not just cosmetic, way. The §2.E new sub-section is well-pitched (concrete, short, with real "breaks-down" caveats rather than re-praising the algorithm), the §3 ↔ §2 cross-link discipline is now consistent across all seven §3.x subsections, and the §5.1 / §5.7 worked examples are now traceable from the chapter alone. The chapter has crossed the line from "75% there" to "ready, modulo nits".

I am downgrading my one residual finding to P1 (was-P0 territory by impact on a careful reader, but it's a single mis-attribution that the Reviser can fix in one line without re-architecting anything). Everything else is P2 polish or items deferred in the revise summary that I agree are out-of-scope for this pass.

---

## Round 1 → Round 2 audit (every P0/P1 I raised, verified)

### Round 1 P0 — VERIFIED FIXED

**P0.1 — §5.1 trace silent rule switch.** Fixed correctly.
- The chapter now commits to **`<` strict comparison everywhere** (§3.3 line 335, §4.1 line 611, §8.2 line 1156).
- §5.1 lines 729–759 anchor the sign convention at the top ("higher (i.e. less negative) is better; goal has $h = 0$; start has $h = -4$"), re-narrate the trace under the `<` rule with **plateau-step explicitly labelled** (line 751, "plateau (equal value) | continue (`<` is false)"), and add line 745–746 explaining that the textbook `≤` rule would terminate at the first plateau.
- The successor lists in the trace table now show $\{-5, -3, -5\}$ and $\{-3, -4\}$ explicitly so the reader can reconstruct without flipping to the slide.
- The §3.3 narrative (lines 343–355) correctly walks through the three cases (improvement / plateau / strict decrease) and what `<` does in each — this was the Round 1 inversion bug that R2 and R4 also flagged. **Resolved correctly: `<` does NOT terminate on plateaux; it walks them indefinitely.** (Note: R1's reviser-summary says this was previously "inverted"; I confirm the current text is correct.)

### Round 1 P1.1 — VERIFIED FIXED (with one residual nit)

**Spec §7.1 violation: ~7 major concepts without §2 analogies + caveats.** Fixed.

New §2.E (lines 145–224) contains eight full analogies, each with its own "where it breaks down" caveat:

| Concept | §2.E location | Analogy | Caveat present? |
|---|---|---|---|
| Random-restart HC | §2.E lines 151–159 | "helicopter ride after every foothill" | ✓ (basin of global may be tiny) |
| First-choice HC | §2.E lines 161–169 | "pick the first step that goes up" | ✓ (parallel sniff is human-only) |
| Stochastic HC | §2.E lines 171–176 | "roll a die among improving directions" | ✓ (randomisation is artificial) |
| Temperature schedule | §2.E lines 178–185 | "dimmer-switch on the shaker" | ✓ — **but caveat has a wording bug, see P1.r1 below** |
| Roulette-wheel selection | §2.E lines 187–195 | "casino roulette with rigged slot widths" | ✓ (wheel is laid out on a line) |
| Crossover | §2.E lines 197–204 | "swap engine and body of two prototype cars" | ✓ (real biology cuts at many points) |
| Mutation | §2.E lines 206–213 | "one-letter typo when copying a long word" | ✓ (real mutation is mostly silent) |
| Fitness landscape | §2.E lines 215–223 | "topography of all candidate solutions" | ✓ (3-D plot is a low-dim fiction) |

Each analogy is one paragraph (target: not just a one-line table entry, which the spec rejected), each has a real breakdown caveat (not a re-praise of the algorithm).

**The §2.F cheat-sheet table** (lines 226–256) has also been expanded to cover: first-choice HC, stochastic HC, plateau, shoulder, ridge, population, generation, chromosome, gene, genotype, phenotype, tournament selection, elitism — all of the omissions I flagged in Round 1 P1.14. ✓

### Round 1 P1.2 — VERIFIED FIXED

§2.B "where the analogy breaks down" caveat (lines 91–98). The Round 1 version praised hill climbing's convex-landscape performance instead of identifying a metaphor breakdown. The Round 2 version correctly says:

> *"The 'blindfold' image suggests you can only feel the immediate gradient under your boot, but hill climbing actually evaluates the objective at every neighbouring state before choosing the best — closer to asking your boot to sniff every spot in a ring around you, then committing to the deepest sniff. Also, real hikers have a finite step size; in a discrete state space 'step size' is defined by the successor function, which can produce wildly heterogeneous jumps in objective value with no smooth in-between."*

Both my suggested breakdown points (step-size mismatch; feet-only vs all-neighbours) are present. ✓

### Round 1 P1.3 — VERIFIED FIXED

§3.6 Selection (lines 500–510). Now contains the explicit:

> ***"To produce one pair of parents for one crossover event, spin the wheel twice independently — once for Parent 1 and once for Parent 2. This is the single most common GA implementation bug: spinning once and reusing the parent."***

Bolded, prominent, before the alternatives are listed. ✓

### Round 1 P1.4 — VERIFIED FIXED

§3.6 Replacement (lines 533–537). Now contains the connective glue:

> *"After repeating selection + crossover + mutation until you have $N$ offspring, this set of $N$ offspring is the new generation. The old population is then discarded (generational GA, the lecture form) or merged with the offspring and truncated by fitness (steady-state GA)."*

A student can now trace the GA loop from §3.6 alone without flipping to §4.3 pseudocode. ✓

### Round 1 P1.5 — VERIFIED FIXED

§5.7 mutation step (lines 934–941). The indexing convention is stated at the top of §5.7 (line 898: *"Throughout this section bits are 1-indexed left-to-right"*), and the mutation step is now:

- **Offspring 1:** `1011011111` → `1011001111`. **Bit 6 flips $1 \to 0$.** ← Verified against the bitstrings. ✓
- **Offspring 2:** `1000000000` → `1010000000`. **Bit 3 flips $0 \to 1$.** ← Verified against the bitstrings. ✓

The Round 1 incomprehensible "(value 0→0 in the labelling but the highlight marks the position considered)" parenthetical is gone. ✓

### Round 1 P1.6 — VERIFIED FIXED

§2.A breaks-down caveat (1) at lines 67–73 now explicitly states the per-column parameterisation:

> *"For the canonical n-queens parameterisation we'll use in §5.4 — one queen per column, free to occupy any of the n rows — the 8-queens state space has $8^8 = 16{,}777{,}216 \approx 1.68 \times 10^7$ states..."*

§5.4 line 808–810 has a matching anchor: *"From here on we use the per-column parameterisation..."* ✓

### Round 1 P1.7 — VERIFIED FIXED

Cross-links from §3 to §2.A/B/C/D/E exist in **every** §3.x subsection (lines 276, 295, 366, 386, 416, 484, 578). Specifically:

- §3.1 (line 276) → §2.A — *"Recall the 'altimeter on a hilly landscape' analogy from §2.A: $f(s)$ is the altimeter reading at configuration $s$."* ✓
- §3.2 (line 295) → §2.A — newly added; redeploys the landscape analogy. ✓
- §3.3 (line 366) → §2.B — *"Recall the 'always step uphill, blindfolded' analogy from §2.B..."* ✓
- §3.4 (line 386) → §2.E — *"Recall §2.E's mini-analogies — each variant has its own one-paragraph picture."* ✓ (somewhat brief but acceptable since §2.E is right there)
- §3.5 (line 416) → §2.C — *"Recall the 'shaking a settling marble' analogy from §2.C..."* ✓
- §3.6 (line 484) → §2.D — newly **deploys** the analogy in full (population = kennel, fitness = breeder's eye, selection = choosing which dogs to breed, crossover = mating, mutation = copying error). Round 1 critique was that this cross-link was a "name-drop only"; Round 2 it's a full redeployment. ✓
- §3.7 (line 578) → §2.E (fitness landscape) — *"Recall §2.E's 'topography of all candidate solutions' analogy — a fitness landscape is the GA analogue of §3.2's state-space landscape, but now with one dimension per gene."* ✓

All seven §3.x subsections now have a §2 cross-link. ✓

### Round 1 P1.8 — VERIFIED FIXED

§2.A caveat split into two cleanly-labelled sub-caveats: "(1 — geometry)" and "(2 — terminology)", lines 67–78. The two ideas no longer share one nested sentence. ✓

### Round 1 P1.9 — VERIFIED FIXED

§6 sign-convention pitfall (lines 978–995) rewritten. The chapter now commits to:

- **$f$** for the maximised objective (sign-corrected).
- **$h$** for the L03-style non-negative heuristic.
- Slide-5's collision (where slide 5 *labels* the maximised objective as $h$) is footnoted at §3.1 line 281 AND at §5.1 lines 731–734.

The "all other states have $h < 0$" wording that R1 flagged as silently mixing two conventions is gone; the current §6 says "$f < 0$" for the 8-puzzle and "$h > 0$" for n-queens — internally consistent and matching the chapter's primary convention. ✓

### Round 1 P1.10 — VERIFIED FIXED

§3.5 lines 420–424. The Δ definition is now its own bulleted block, not buried in a parenthetical:

> *"$\Delta > 0$ means the proposed move is an **improvement** (uphill).
> $\Delta < 0$ means the proposed move is a **worsening** (downhill).
> $\Delta = 0$ is a **lateral** move (no change in objective)."*

Promoted out of the parenthetical. ✓

### Round 1 P1.13 — VERIFIED FIXED

Fitness landscape now has its own analogy in §2.E (lines 215–223), and §3.7 cross-links to it at line 578. ✓

### Round 1 P1.14 — VERIFIED FIXED

§2.F cheat-sheet table now includes: first-choice HC, stochastic HC, elitism, tournament selection, population, generation, plateau, shoulder, ridge, genotype, phenotype. ✓

(Glossary terms in front-matter at line 4 also include these. ✓)

---

## P0 — none.

(All Round 1 P0 issues are fixed.)

---

## P1 — one residual issue

### P1.r1 — §2.E "Temperature schedule" caveat misattributes the schedule type to GA instead of SA

`L05-Local-Search.md:178-185`. The §2.E "Temperature schedule" sub-section reads:

> *"Where it breaks down: real cooling is physical (heat dissipates exponentially); **GA schedulers** can use any monotone-decreasing function, including ones with no physical analogue."*

**Bug.** Temperature schedules are a feature of **simulated annealing**, not genetic algorithms. The word "GA" here is wrong — should be "SA" (or "annealing schedulers", or simply "the algorithm").

This is exactly the kind of slip a confused student will *notice* because the schedule was just introduced in §2.C (the marble analogy, which is SA) — and the student will then question their own understanding ("wait, do GAs also have temperature schedules? Did I miss something?"). It's a minor but real pedagogical-clarity issue, and it's *new* to the Round 2 revision (the Round 1 §2 didn't have this paragraph at all).

**Required fix.** One-word edit. Replace "GA schedulers" with "SA schedulers" (or "annealing schedulers" for plain-English consistency with the §2.C marble analogy). Five seconds for the Reviser.

I would not block approval on this. Flagging as P1 because it directly violates §7.1 (analogy must be technically accurate) and because it's trivially fixable.

---

## P2 — nice to have

### P2.r1 — §3.4 cross-link to §2.E is briefer than its peers

Line 386 reads: *"Recall §2.E's mini-analogies — each variant has its own one-paragraph picture."* Compare to the much fuller §3.6 cross-link at line 484 ("the population is the kennel, the fitness function is the breeder's eye, selection is choosing..."). The §3.4 cross-link could redeploy the helicopter / first-step-up / die-roll images in one sentence for each variant before the bullet list, instead of just pointing. Optional polish.

### P2.r2 — §2.E "Temperature schedule" lives alone, oddly placed between HC variants and GA operators

The §2.E sub-sections are ordered: random-restart HC → first-choice HC → stochastic HC → **temperature schedule** → roulette-wheel → crossover → mutation → fitness landscape. The temperature schedule is the only SA item in the list; everything else is HC-or-GA. Either move it to sit right after §2.C, or note in a one-line preamble to §2.E that the analogies are grouped by *§3.x location*, not by algorithm. Optional.

### P2.r3 — §2.E.X mini-analogies are not cross-linked back from their respective §3 subsubsections

§3.6.1 (roulette-wheel) does not contain "Recall the casino-roulette analogy from §2.E…". §3.6.2 (crossover and mutation) does not contain "Recall the prototype-cars analogy from §2.E…". These exist at §3.6 (line 484) only at the parent-section level; the operator-level sub-sub-sections have no individual cross-link. Adding one per operator would mirror the §3.3 / §3.5 / §3.6 discipline. Optional, but completes the cross-link grid.

### P2.r4 — §5.7 mutation prose says "all other bits unchanged" but doesn't say *why* only one bit flipped

§5.7 lines 938–939. Each bullet ends with "(all other bits unchanged)". A student wondering why slide 44 flipped only ONE bit per offspring (when the mutation rate is $m \in [0.001, 0.1]$ and 10 bits per offspring → expected $\approx 0.5$ flips per offspring) will not find the answer here. One sentence — *"Slide 44 illustrates each offspring with exactly one bit flipped; in practice the expected number of flips per offspring is $m \cdot L$, which is fractional and often 0 or 1 per offspring."* — would close the loop.

### P2.r5 — §6 "Forgetting to mutate" pitfall has the destructive-on-average note but doesn't number the §3.6 mutation paragraph as the source

Lines 1043–1045 read: *"Conversely, mutation must stay small (typically 0.05) because it is destructive on average — only occasionally beneficial. Crossover does the bulk of the building; mutation just prevents stagnation."* — good (matches R1 P1.12 request). Add a "(see §3.6 Mutation)" cross-ref so a student can find the rate-range and indexing convention again from §6. Optional.

### P2.r6 — §5.6 oil-drilling "smallest power of 2" rule is now explicit; could add the exam-relevant alternative

Line 879: *"$2^{10} = 1024 > 1000$ — we pick the smallest power of 2 that exceeds the maximum integer position, so every position is encodeable without wasting a bit."* ✓ (Closes R1 P2.4.)

For a student wondering "what if the position count is exactly a power of 2?", a one-line follow-up — *"If the max position were exactly 1024, 10 bits would still suffice (positions 0–1023); if it were 1025, you would need 11 bits."* — adds an exam-style off-by-one reminder. Optional.

### P2.r7 — Reading-time "~55 min" front-matter still uncalibrated (R1 P2.10 deferred)

Line 3 still says ~55 min. The revise summary documents this was intentionally deferred; I record it here for the verifier.

---

## EVIDENCE — what I re-inspected

1. **Round 1 review file** read in full.
2. **Revise summary** read in full; every "P1 fix applied" item cross-checked against the chapter.
3. **Chapter** read line-by-line, focusing on §2 (entirely rewritten), §3 cross-links (all seven), §5.1 (P0 area), §5.7 (P1.5 area), §6 (P1.9 sign-convention rewrite).
4. **PDF source slides 5, 11, 12, 13, 14, 17, 18, 41–44** re-extracted via `fitz` and compared verbatim:
   - Slide 5: heuristic chain $h = -4 \to -3 \to -3 \to -2 \to -1 \to 0$ confirmed; trace in §5.1 matches ✓
   - Slide 13: pseudocode uses strict `<` — chapter now matches ✓
   - Slide 14: "h = 1 local optimum for 8-queens" — chapter §5.5 matches ✓
   - Slide 17: SA pseudocode `if Δ > 0 then current = next; else current = next with probability exp(Δ/T)` — chapter §4.2 matches verbatim ✓
   - Slide 18: "Picks random rather than best state move as in hill-climbing" — chapter §3.5 line 410–414 matches ✓
   - Slide 41: 8 chromosomes, fitnesses (1, 2, 3, 1, 3, 5, 1, 2), total 18 — §5.7 lines 902–904 match ✓
   - Slide 42: R=7 → Chromosome 4; R=12 → Chromosome 6 — §5.7 lines 920–921 match ✓
   - Slide 43: parents `1010000000` and `1001011111`; offspring `1011011111` and `1000000000` — §5.7 line 930–932 matches ✓
   - Slide 44: offspring 1 `1011011111` → `1011001111`; offspring 2 `1000000000` → `1010000000` — §5.7 lines 938–939 match; bit positions 6 and 3 verified by manual position-by-position diff. ✓
5. **§2.E new sub-section** read closely for accuracy of each analogy + caveat. Eight analogies, eight caveats, one analogy (Temperature schedule) misattributes the schedule type — flagged as P1.r1.
6. **§2.F cheat-sheet table** read row-by-row for omissions (R1 P1.14 closeout); all R1-flagged omissions now present. ✓

---

## SUMMARY ASSESSMENT

This is a strong revision. Every P0 from Round 1 is fixed correctly (not just acknowledged but **traceable in the chapter prose**), the spec §7.1 hard rule on analogies + caveats is now satisfied for every concept I judged "major" in Round 1, and the §3 ↔ §2 cross-link discipline is now uniform across all seven §3.x subsections.

The one residual issue (P1.r1 — "GA schedulers" should read "SA schedulers" in §2.E's temperature-schedule analogy) is a single-word fix and not a structural problem.

Recommend the PM:
1. Dispatch the Reviser for the one P1.r1 fix (~30 seconds of work).
2. Treat the P2s as backlog — none of them block PDF render or exam-prep use.
3. Proceed to render once the one-word fix lands.

The chapter is now ready for student use modulo that one word.

---

## Report to PM

**Assignment recap:** L05 Local Search — Round 2 Pedagogical-Clarity review (Reviewer #3 of 4), post-revision audit against `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L05-Local-Search.md`. Round 1 returned 1 P0 + 13 P1; checked all of them against the revised chapter and the PDF source.

**Status:** Pass with one minor concern (one-word fix) — **APPROVED WITH P1 NOTE**.

**P0 findings:** None.

**P1 findings:**
1. `L05-Local-Search.md:178-185` — §2.E "Temperature schedule" caveat says *"**GA schedulers** can use any monotone-decreasing function"* — should be **"SA schedulers"** (or "annealing schedulers"). Temperature schedules are a feature of simulated annealing, not genetic algorithms. New error introduced in this revision (§2.E is new). Single-word fix.

**P2 findings:**
1. `L05-Local-Search.md:386` — §3.4 cross-link to §2.E is briefer than the §3.3 / §3.5 / §3.6 cross-links; could redeploy the helicopter / first-step / die-roll images in one sentence each.
2. `L05-Local-Search.md:145-224` — §2.E ordering puts "Temperature schedule" (SA) between HC variants and GA operators; either reorder or add a one-line preamble explaining the grouping is by §3.x location not by algorithm.
3. `L05-Local-Search.md:540-571` — §3.6.1 (roulette-wheel) and §3.6.2 (crossover, mutation) sub-subsections lack their own §2.E cross-links; only the parent §3.6 has one. Completing the grid would mirror §3.3 / §3.5 discipline.
4. `L05-Local-Search.md:934-941` — §5.7 mutation prose says "all other bits unchanged" but doesn't say *why* only one bit flipped given $m \approx 0.05$ and $L = 10$. One sentence on $E[\text{flips}] = mL$ would close the intuition gap.
5. `L05-Local-Search.md:1043-1045` — §6 "Forgetting to mutate" pitfall could add "(see §3.6 Mutation)" cross-ref.
6. `L05-Local-Search.md:879` — §5.6 "smallest power of 2" rule could note the off-by-one when max position equals exactly $2^k$.
7. Line 3 — Reading-time "~55 min" front-matter still uncalibrated; deferred per revise summary, recorded here.

**QA Checklist (§7) status:** Reviewer #3 lens only.
- Hand-waving in worked examples: **Pass** (P0.1 closed; §5.1 trace + §5.7 mutation now reconstructable from chapter alone).
- Every major concept has an everyday analogy in §2 with caveat: **Pass** (R1.P1.1 closed; §2.E has 8 new analogies + caveats; §2.F table covers minor concepts).
- Cross-links from §3 to §2: **Pass** (all 7 §3.x have §2 cross-links; the §3.6 cross-link now redeploys the analogy rather than name-dropping).
- Confused-student readability of §5.7 mutation: **Pass** (1-indexed convention stated; bit positions verified by manual diff).
- Comparison table §4.4: **Pass**.
- Cheat sheet §8: **Pass**.

**Acceptance criteria (§1) status:**
- "Self-contained chapter" (spec line 44): **Met** (the §5.1 trace and §5.7 mutation are now reconstructable from chapter alone; the GA loop in §3.6 has the connective tissue Round 1 said was missing).
- "Every major concept has an everyday analogy with caveat" (spec §6.1 lecture-chapter template + §7.1 Reviewer #3 mandate): **Met**, modulo the one P1.r1 wording slip.

**DOCUMENT.md audit:** N/A — this is a content review against a single `.md` artifact; the spec does not require `DOCUMENT.md` for `study/lectures/`.

**Out-of-scope observations:** None for Reviewer #3's lens. (R1, R2, R4 should re-audit their own checklists; I noticed the chapter now correctly attributes Geman & Geman to $c / \log(1+t)$ and tags it "not on slides", which fixes R2's P1.2; I noticed the §4.4 completeness column now reads "No formal claim" for GA which fixes R4's P0; I noticed §5.4 slide-12 caption is now the lecturer's verbatim "local minima" warning which fixes R1's P0 — but these are not my territory to formally sign off.)

**Concerns / risks:**
- The §2.E "Temperature schedule" mis-attribution (P1.r1) is *exactly* the kind of error a careful student notices — the schedule was just introduced in §2.C (SA, marble analogy) and the §2.E caveat says "GA schedulers" two paragraphs later. A student will doubt themselves rather than the chapter. Fix it.
- The §2.E sub-section is long (~80 lines) and dense; a future revision might consider whether the eight mini-analogies should be split into "HC operators" (random-restart, first-choice, stochastic), "SA operator" (temperature schedule), "GA operators" (roulette, crossover, mutation, fitness landscape). Not a blocker.

**What PM should do next:**
1. Dispatch Reviser for the **one-word fix** in §2.E (P1.r1: "GA schedulers" → "SA schedulers"). Five-minute touch-up, no full revision pass needed.
2. After that fix, this reviewer (#3) signs off; PM should poll R1, R2, R4 for their Round 2 verdicts before final approval.
3. If all four reviewers approve Round 2, the chapter is ready for PDF render.
4. P2 items go to backlog; none block render or exam-prep use.

**DOCUMENT.md updated:** N/A for lecture-chapter reviewer.
