# L05 Local Search — Round 1, Reviewer 3 (Pedagogical Clarity incl. Analogies)

**Artifact under review:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L05-Local-Search.md`
**Source PDF:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture5-Local Search.pdf` (50 slides, read in full)
**Lens:** I read this as a confused student who has done L02 and L03 but has never seen local search. Spec §7.1: enforce §2 analogies — every major concept needs an everyday analogy + breakdown caveat, cross-linked from §3. Be harsh.

---

## VERDICT

**NEEDS_REVISION**

The chapter is, on the whole, a strong pedagogical draft — the analogy set in §2 is genuinely well thought-through and the back-references from §3 land. However, several major concepts the lecture treats as first-class are presented without an analogy (or with an analogy that is *named* but never built out), the worked example for the 8-puzzle (§5.1) contains a confusing internal inconsistency that will actively mis-teach a student, and the GA section glosses two procedural steps (selection-pair construction, replacement) in a way that a confused student cannot reproduce. There are also analogy-caveat misses that violate the spec's hard requirement.

I am withholding approval on the strength of the §5.1 trace error alone (P0). The remaining items are recoverable in one round.

---

## P0 — MUST FIX (blocks approval)

### P0.1 — §5.1 hill-climbing 8-puzzle trace is internally inconsistent and will actively confuse a student

Lines 537–545. The table claims:

| Step | Current $h$ | Successors evaluated | Best successor $h$ | Chosen? |
|---|---|---|---|---|
| 0 (start) | $-4$ | one to the left ($-5$), one down ($-3$), one to the right ($-5$) | $-3$ | yes (climb to $-3$) |
| 1 | $-3$ | $-3$, $-4$ | $-3$ (tie) or back up to a $-4$ neighbour | the slide takes a side-step to a different $-3$ |
| 2 | $-3$ | (then a $-2$ successor) | $-2$ | yes |
| 3 | $-2$ | $-1$ | $-1$ | yes |
| 4 | $-1$ | $0$ | $0$ | yes — **goal reached** |

Multiple problems on a single page:

1. **The "side-step to a different $-3$" at step 1 contradicts the chapter's own hill-climbing rule.** §3.3 line 207 defines the termination as `if value(next) ≤ value(current): return current`. With `≤`, a $-3$ from a $-3$ is **not** an improvement and the algorithm would terminate at step 1. The chapter says "the slide takes a side-step" — but the slide-13 pseudocode uses `<` (strict), which the chapter itself flagged as a weakness in §3.3 lines 215–218. So the student is asked to apply the slide's broken rule to read the worked example, while §3.3 told them to *not* apply that rule. A confused student will spend ten minutes trying to figure out why the trace works and walk away thinking they don't understand hill climbing.
2. **The slide-5 image (fig02) actually shows the heuristic values $h = -4, -3, -3, -2, -1, 0$** (confirmed from the source-text dump of slide 5). The trace in the chapter does correspond to those values, but the chapter never tells the reader that *the lecturer deliberately picked a path with a sideways step* and never tells them which hill-climbing variant this corresponds to (it must be "allow sideways with a budget"). The student is left to infer this — and the wrong inference is "ordinary hill climbing reaches the goal", which is false.
3. **Row "Step 1, Successors evaluated: $-3$, $-4$"** lists only two values but slide 5 shows three successors of the $h = -3$ state. The reader cannot reconstruct what's going on without the slide open beside them, which defeats the spec acceptance criterion (line 44 of the spec) that the chapter must be self-contained.
4. **Sign-convention overload.** Step 0 successors are listed as "$-5, -3, -5$" but the chapter has not yet primed the reader that "$-5$" is *worse* than "$-4$" because we're maximising the negative count. Anyone reading top-to-bottom encounters "-5" right after a "start at -4" and has to slow down to remember the sign convention. A one-sentence anchor at the top of the table ("recall: we maximise, so higher numbers — i.e. *less negative* — are better") would fix it.

**Required fix:** Rewrite the table. Either (a) commit to the slide-13 strict-`<` rule everywhere in the chapter (and add a clear "this is why the slide-5 trace works, the chapter's `≤` rule would terminate at step 1 — this is one of the slide vs textbook inconsistencies"), or (b) keep the `≤` rule and re-narrate the example as "hill climbing with sideways-move budget = N" with the budget made explicit. Either way, the trace must be reconstructable from the chapter alone, every step's successor list must match what slide 5 actually shows, and the sign convention must be re-anchored at the start of §5.1.

This is P0 because §5.1 is the very first worked example a student reads after the algorithm pseudocode, and it directly contradicts the algorithm just defined.

---

## P1 — SHOULD FIX (requested, not blocking individually, but together they justify a revision)

### P1.1 — Spec §7.1 hard rule violated: not every major concept has an analogy in §2

The spec says: *"every major concept must have at least one concrete everyday analogy in §2, each cross-linked from its formal definition in §3, with a 'where the analogy breaks down' caveat. Reviewer flags weak or missing analogies and may demand replacement analogies."*

§3 introduces these concepts that I judge "major" by the criterion "the chapter spends ≥1 paragraph defining them or they have their own §3.x subsection":

| §3 concept | Analogy in §2? | Caveat in §2? | Cross-linked from §3? |
|---|---|---|---|
| Objective function (§3.1) | Yes — altimeter (§2.A) | Combined w/ local search caveat | Yes (line 164) |
| State-space landscape (§3.2) | Implicit in §2.A "landscape" | Yes (combinatorial vs continuous) | **No — missing back-link** |
| Hill climbing (§3.3) | Yes (§2.B) | Yes | Yes (line 230) |
| **Random-restart hill climbing (§3.4)** | Only in 2.E table (one line) — **NOT in body of §2** | **No caveat** | **No** |
| **First-choice hill climbing (§3.4)** | **None** | n/a | n/a |
| **Stochastic hill climbing (§3.4)** | **None** | n/a | n/a |
| Simulated annealing (§3.5) | Yes (§2.C) | Yes | Yes (line 266) |
| **Temperature schedule (§3.5)** | Only in 2.E table (one line) — **NOT in body** | **No caveat** | **No** |
| **Population (§3.6)** | Mentioned in §2.D but no standalone analogy beyond "a whole bunch" | No caveat | No |
| Genetic algorithm (§3.6) | Yes (§2.D) | Yes | Yes (line 318) |
| **Selection / roulette-wheel (§3.6.1)** | Only in 2.E table — **NOT in body of §2** | **No caveat** | **No** |
| **Crossover (§3.6.2)** | Only in 2.E table — **NOT in body** | **No caveat** | **No** |
| **Mutation (§3.6.2)** | Only in 2.E table — **NOT in body** | **No caveat** | **No** |
| **Fitness landscape (§3.7)** | **None** — §2.A talks about landscape but never about fitness specifically | n/a | n/a |
| **Elitism (§3.6 selection)** | **None** | n/a | n/a |

Reading the spec strictly, the 2.E "one-line cheat-sheet of the analogy set" table does *not* satisfy "at least one concrete everyday analogy in §2 with a 'where the analogy breaks down' caveat" — a one-line entry in a summary table is not an analogy with a caveat. The spec wants the body, not the index.

**Required fix.** At minimum: add §2.E.1 / §2.F / §2.G subsections (or expand §2.D) with proper everyday analogies + caveats for **roulette-wheel selection, crossover, mutation, and random-restart hill climbing**. Suggestions:

- **Roulette-wheel selection** ≡ "a real carnival roulette wheel where the wheel-slots are wider for the fitter chromosomes — the ball is more likely to fall in a wide slot, but it *can* land in a narrow one." Caveat: real roulette wheels have equal-sized slots; the GA wheel is biased. Already half-developed in the body of §3.6.1 — just lift the intuition into §2.
- **Crossover** ≡ "a child inherits the left half of one parent's chromosome and the right half of the other — like swapping the engine and the body of two prototype cars to make a third." Caveat: real biological crossover happens at many points per chromosome and is not literally a single bit-string cut.
- **Mutation** ≡ "a one-letter typo when copying out a long word — usually catastrophic but occasionally the typo accidentally improves the word." Caveat: most mutations are silent or neutral, not "good or catastrophic".
- **Random-restart** ≡ "every time you hit a foothill in the fog, you helicopter to a totally new spot on the mountain range and try again. Eventually you helicopter into the basin of the highest peak." Caveat: in practice the basin of the global maximum may be tiny relative to the whole space, so the number of restarts can be astronomical.
- **Fitness landscape** ≡ "the topography of all candidate solutions, with elevation = score." Caveat: the "horizontal axis" is artificial — the actual configuration space is high-dimensional and discrete; the 3D plot is a fiction.

And then add the cross-link from §3 the way §3.3 and §3.5 already do it. Pick whichever subset is most exam-relevant — but the four operators (selection, crossover, mutation, restart) are non-negotiable per the spec's "every major concept" rule.

### P1.2 — The "analogy breakdown" caveat is missing or weak on three of the four §2 analogies that *do* exist

§2.A (local search ≡ hiking): caveat is given (lines 60–64), but it conflates two separate caveats (combinatorial vs continuous, and "but the slides still call it a landscape, so we will too"). Split into two sentences.

§2.B (hill climbing ≡ blindfolded climbing): caveat (lines 76–79) actually *praises* hill climbing's speed instead of saying where the metaphor breaks. The spec wants "where the analogy is misleading", not "actually hill climbing is great on convex landscapes" (true, but doesn't address the metaphor's accuracy). A real caveat: *the hiker has a finite step-size; in our discrete state spaces there's no notion of "step size" — neighbours are defined by the successor function, which can produce wildly heterogeneous "step sizes" in objective value.* Or: *the blindfold metaphor implies you can only feel the gradient immediately under your feet; the actual algorithm evaluates the objective at every neighbour, which is the equivalent of asking your boot to sniff every spot in a ring around you.*

§2.C (SA ≡ shaking marble): caveat (lines 96–99) is good — mechanism difference flagged.

§2.D (GA ≡ animal breeding): caveat (lines 121–124) is good. ✓

**Required fix.** Reword the §2.B caveat to actually identify a place the analogy *misleads* rather than reassure that hill climbing works on convex problems (which belongs in §3.3 properties, not as a caveat).

### P1.3 — §3.6 selection step never says how many parents are chosen per iteration

Lines 311–394. The "Selection" subsubsection (line 330) says "Pick parents preferentially in proportion to fitness" and then the §4.3 pseudocode reveals "parent1 ← roulette_wheel_select(population, fitness); parent2 ← roulette_wheel_select(...)". A confused student reading §3.6 cold has no idea whether selection is "pick one parent at a time" or "pick a pair". The slide-40 / slide-42 source says "Select the first chromosome ... when all previous fitness's are added — gives you at least the value R" — i.e. *one parent per roulette spin*. The chapter never says this until §4.3 pseudocode three pages later. State it in §3.6.1 step 3: *"to produce a pair of parents for one crossover event, spin the wheel twice (independently)."* This is the single most common GA implementation bug.

### P1.4 — §3.6 "Replacement" subsubsection is procedurally unclear

Lines 358–361. "A 'generational' GA replaces everyone; a 'steady-state' GA replaces only the worst few per iteration." The student does not know what "the new population" *is* when this paragraph begins — the previous paragraph (mutation) operates on individual offspring. There needs to be one explicit sentence: *"Repeat selection + crossover + mutation until you have N offspring; this set of N offspring is the new generation. The old population is discarded (generational GA) or merged-and-truncated (steady-state)."* Without this connective glue, a beginner cannot trace the GA loop from §3.6 alone — they need to flip ahead to §4.3 pseudocode, which the chapter structure says shouldn't be necessary.

### P1.5 — §5.7 mutation example is internally inconsistent with the chapter's own narration

Lines 662–664. Caption reads:

> *"Offspring 1 = `1011011111` mutated to `1011001111` (bit 5 flipped, value 0→0 in the labelling but the highlight marks the position considered); Offspring 2 = `1000000000` mutated to `1010000000` (bit 3 flipped 0→1)."*

The phrase "value 0→0 in the labelling but the highlight marks the position considered" is incomprehensible to a student. Looking at the bitstrings:

- Offspring 1 before: `1011011111` (positions: 1=1, 2=0, 3=1, 4=1, 5=0, 6=1, 7=1, 8=1, 9=1, 10=1)
- Offspring 1 after:  `1011001111` (position 5 stays 0, position 6 changed 1→0)
- Net effect: bit 6 flipped, not bit 5.

The chapter says "bit 5 flipped". That's wrong by the standard 1-indexed left-to-right reading. Either:
- The chapter is 0-indexed (in which case "bit 5" is the 6th bit — but then the parenthetical "value 0→0 in the labelling" is also wrong because the 6th bit went 1→0).
- The chapter is following the slide's highlight which may differ from the bit that flipped.

Either way, the student reading this chapter alone cannot reconstruct which bit changed. This is a P1 because §5.7 is the canonical worked GA example and the mutation step is the simplest of the three. **Required fix:** State the indexing convention (1-indexed, left-to-right) once at the top of §5.7, and re-describe each flip as `position k: 0→1` or `position k: 1→0` consistently. Drop the "value 0→0 in the labelling" parenthetical — it's confusion, not clarification.

### P1.6 — §2.A states the 8-queens state space size wrong (or at least without explanation)

Line 62: *"e.g. 8-queens has $8^{8} \approx 16.7$ million states"*. This is correct for the *unrestricted* state space (8 queens on an 8×8 board) but the chapter elsewhere (§3.4, §5.4, §5.5) describes the one-queen-per-column state space, which has $8^{8} \approx 16.7M$ also (each of 8 columns picks one of 8 rows). So the number happens to come out the same, but the chapter never reconciles which state space it's actually using. A confused student trying to match this against §5.4's "56 successors total" will compute $8 \times 7$ neighbours per state and ask: *but if the state space is $8^8$, what does "$8 \times 7$ successors" mean — shouldn't it be more?* — and won't easily realise that the "one queen per column" constraint is implicit. State this once, in §2.A's analogy-breakdown caveat or at the start of §5.4.

### P1.7 — The §3.3 / §3.6 cross-link to the analogy isn't always given the same form

§3.3 line 230 says: *"Recall the 'always step uphill, blindfolded' analogy from §2.B: the agent has no plan, only the local gradient."* ✓

§3.5 line 266 says: *"Recall the 'shaking a settling marble' analogy from §2.C: when 'temperature' is high, the marble can hop out of small dips; as temperature falls toward zero, hops become smaller and rarer."* ✓

§3.1 line 164 says: *"Recall the 'altimeter on a hilly landscape' analogy from §2.A: $f(s)$ is the altimeter reading at configuration $s$."* ✓

§3.6 line 319 says: *"Recall the 'animal breeding' analogy from §2.D."* — and then just lists the biological dictionary. The cross-link doesn't actually re-deploy the analogy. It would be much better to say: *"Recall the 'animal breeding' analogy from §2.D: the population is the kennel, the fitness function is the breeder's eye, selection is choosing which dogs to breed, crossover is mating two parents, and mutation is the unavoidable copying error in DNA replication."* That kind of cross-link is what §3.3 and §3.5 do for their sections and what §3.6 currently fails to do.

§3.2 (state-space landscape), §3.4 (hill-climbing variants), and §3.7 (fitness landscapes) have **no cross-link to §2 at all**. The spec requires every §3.x to cross-link back; this is missing.

### P1.8 — Hard-to-parse single-paragraph caveat in §2.A

Line 60–64 is a single long sentence with two nested clauses, a parenthetical with a slide number, and the phrase *"the slides call it exactly that, 'the state-space landscape', on slide 15."* The student reading top-to-bottom is asked to keep three things in mind at once. Split into 2–3 sentences.

### P1.9 — Sign-convention pitfall §6 says "h is smaller for the goal" / "h is larger for the goal" — backwards for one of them

Lines 701–702:

> *"Exam tip: ... 'h is smaller for the goal' is the safest guess for n-queens; 'h is larger for the goal' is safer for 8-puzzle."*

Look at the 8-puzzle convention the chapter uses: $f(n) = -(\text{tiles out of place})$, so the goal has $f = 0$ and all other states have $f < 0$. So the goal value is the *largest* (least negative) — consistent with "h is larger". ✓

n-queens: $h = $ number of attacking pairs, goal has $h = 0$, other states have $h > 0$. So goal is the *smallest*. ✓

OK, that's actually correct on re-reading. But the §6 paragraph above (lines 692–698) confusingly says of 8-puzzle "all other states have $h < 0$" (using the variable name $h$ even though the chapter defined this as $f(n) = -h(n)$, with $h(n)$ being the L03 sense — i.e. positive). The chapter is silently mixing two conventions:
- L03 sense: $h(n) \ge 0$, smaller is better.
- §5.1 / slide 5: writes "$h = -4$" on the board — using $h$ for what the chapter elsewhere calls $f(n) = -h(n)$.

A confused student reading "all other states have $h < 0$" in §6 will rightfully think the chapter has just contradicted itself, because in §3.1 we said $h(n)$ (the L03 heuristic) is non-negative. The chapter has to commit to one naming convention. I recommend: keep $h$ for the L03-style non-negative heuristic; use $f$ everywhere for the objective being maximised; in worked examples that show "$h = -4$" on a slide, explicitly say "the slide labels what we are calling $f$ as $h$ — read the minus sign accordingly."

This is the actual sign-convention trap the §6 paragraph promised to clear up, and it currently *adds* to the trap instead of resolving it.

### P1.10 — §3.5 acceptance rule formula presented before the intuition of "what is $\Delta$"

Lines 270–272 introduce $\Delta = f(\text{next}) - f(\text{current})$ correctly. Lines 271–272 then have a parenthetical: *"For maximisation: $\Delta > 0$ is improvement; $\Delta < 0$ is worsening."* This parenthetical is in fact the single most useful intuition for the entire SA section and should be its own bulleted line, not a parenthetical. A student tired by mid-page-30 will gloss over it.

### P1.11 — §3.6 mutation rate range vs §6 "Crossover-rate $c$ vs mutation-rate $m$" disagree on the upper end of $m$

Line 354: *"with probability $m$ (the mutation rate), flip it. The mutation rate is small — typically $0.001$–$0.1$"*.

Line 751: *"$m$ is the probability that a single gene flips. Typically 0.001–0.1."* ✓

But slide 44 (and the chapter §5.7 line 663) says *"typical values between 0.1 and 0.001"* — same range, ✓. So consistent. **Disregard this item** — I include it to document I checked. (Withdrawn.)

### P1.12 — §6 "Forgetting to mutate" pitfall undercuts the §3.6.4 mutation rate guidance

Line 736–739 says: *"A GA without mutation can converge to a population where every chromosome has the same bit at some position — crossover can never reintroduce diversity at that position."* ✓ Excellent intuition for *why* you need mutation, but a student is left wondering: *"if mutation is so essential, why is the rate so small (0.05)?"* Add one sentence: *"Mutation must be small because it is destructive on average — only occasionally beneficial. Crossover does the bulk of the actual *building*; mutation just keeps the population from going genetically stale."*

### P1.13 — §3.7 fitness landscape needs a §2 analogy AND a §3 ↔ §2 cross-link

The fitness-landscape concept (lines 397–411) is treated as if the §2.A "altimeter" analogy already covers it, but §2.A spoke of a *single* state's altimeter, not the *landscape of fitnesses across a whole population*. The shape-of-the-landscape concept is genuinely new to §3.7 and deserves its own one-paragraph analogy — e.g. *"if every possible chromosome is a point on a 3-D surface, with elevation = fitness, then a 'smooth' landscape is gentle hills you can walk up, a 'rugged' landscape is the Himalayas where you have to teleport between peaks, and a 'white-noise' landscape is the random static on an off-air TV channel — no algorithm can climb static."* Then cross-link back to it the way §3.3 and §3.5 do.

### P1.14 — §2.E one-line analogy table omits at least three §3 concepts

The table (lines 128–142) lists 13 concepts. Missing:
- **First-choice hill climbing**
- **Stochastic hill climbing**
- **Elitism**
- **Tournament selection** (mentioned in §3.6 selection)
- **Population** (it's in §3.6 but absent from §2.E)
- **Generation** (used in §5.7, §6, never analogised)
- **Phenotype / Genotype** (these *are* in §8.5 dictionary but the cheat-sheet of analogies in §2.E ignores them)

Add what's missing or split the omitted ones out into a "minor concepts" note.

---

## P2 — NICE TO HAVE

### P2.1 — Use the same hill-climbing termination operator everywhere

§3.3 pseudocode: `≤`. §4.1 pseudocode: `≤`. §6 first pitfall (line 702 area) uses "smaller for the goal" language. §8.2 cheat sheet: `≤`. Slide-13 source: `<`. The chapter rightly notes the discrepancy once in §3.3 lines 215–218. A reader-friendly footnote at every subsequent re-display of the pseudocode ("we use ≤; the source slides write <") would prevent the same student from having the same "wait, which one is it?" moment three times in 60 pages.

### P2.2 — §2.A "16.7 million" is a weak motivator

The number is correct but doesn't actually motivate "memory-light is important". The point of citing it is "you can't enumerate the state space, you can't even store it". One sentence linking the two: *"BFS on this would need to keep 16.7 million nodes in the frontier — local search keeps **one**."*

### P2.3 — §5.8 numerical SA example uses suggestive numbers but no comparison column

Lines 672–682. Compute $\exp(-5/10) \approx 0.607$ ✓ and $\exp(-5/1) \approx 0.0067$ ✓. A row-style table comparing these two T values plus a third (e.g. $T = 100$ giving $\exp(-0.05) \approx 0.95$) would let the student *see* the temperature → 0 collapse to greedy hill-climbing.

### P2.4 — §5.6 "drilling for oil" caption (line 632) misses the chance to say *why* 10 bits

Line 632 mentions "$2^{10} = 1024 > 1000$" but doesn't say "and we picked the smallest power of two that exceeds the maximum position so every position is encodeable and we don't waste a bit." A confused student will wonder "why not 11 bits?" — answer with the smallest-such-power rule.

### P2.5 — Mermaid diagrams promised by the figure protocol §6.1.1 are absent

Section 6.1.1 of the spec says REWORK figures get a Mermaid diagram alongside, and even USE figures may merit one. The chapter has zero Mermaid diagrams. The lecture's "landscape" figure (fig09) and the "fitness landscape regimes" figure (fig14) could both be elegantly captured with a small Mermaid line/area sketch as a backup. Optional but would help the WeasyPrint render quality if a PNG fails to embed.

### P2.6 — §8.5 (cheat-sheet GA vocabulary) re-introduces all biology terms but doesn't cite §3.6 (the biology→CS dictionary they came from)

A one-line cross-ref at the top of §8.5 ("Expanded from §3.6 line 318 onwards") would help students who want the full definition.

### P2.7 — §2.D includes a long blockquote from slide 22 that duplicates §3.6 line 322 onwards

The pedagogical blockquote at lines 110–116 is good, but it's then immediately re-listed in bullet form in §3.6 lines 322–326. Pick one: keep the blockquote in §2.D as the prose first introduction, and turn the §3.6 listing into a one-line ref ("see §2.D"); or keep the §3.6 bullets and drop the blockquote down to one line.

### P2.8 — §2.E table column "Concept" has inconsistent capitalisation

"Local search" / "Hill climbing" / "Simulated annealing" — sentence case. "Mutation" / "Crossover" — sentence case. "Roulette-wheel selection" — sentence case. ✓ But "Random-restart hill climbing" has its hyphen treatment different from the body text where it's introduced. Standardise.

### P2.9 — §2 (Big Picture) lacks a one-line statement of *when* this lecture's methods help

§2.A explains "where you are on a landscape". §2.B/C/D explain the methods. None of §2 says *when you'd reach for local search over the L03 methods*: when path doesn't matter and you have a cheap evaluator. That decision rule lives in §8.7 but should also surface as a closing line of §2.A or as a §2.0 prelude.

### P2.10 — "Reading time ~55 min" front-matter is unverifiable

Frontmatter line 3 says ~55 min. Is this calibrated to anything? L03's chapter (I'd need to read it) presumably has a different number. Either calibrate (word count / typical reading rate) or remove the spurious-precision number.

---

## EVIDENCE — what I inspected and how

**Source PDF (`Lecture5-Local Search.pdf`):** Extracted full text of all 50 slides via `fitz` page text dump. Key slides cross-checked against chapter:
- Slide 2 "objective function" definition → chapter §1 quote ✓
- Slide 4 "amnesia" quote → chapter §2.B line 71 ✓
- Slide 5 "$f(n) = -(\text{tiles out of place})$" + the heuristic sequence $h = -4, -3, -3, -2, -1, 0$ → chapter §5.1 table — **trace inconsistency, see P0.1**
- Slide 7 ABDEC → ABCED pairwise exchange → chapter §5.2 ✓
- Slides 10–12 8-queens $h = 17 \to 12 \to 0$ trace → chapter §5.4 ✓
- Slide 13 pseudocode with `<` strict comparison → chapter §3.3 with `≤`, flagged ✓ (but §5.1 reverts to slide-13 behaviour without re-flagging — see P0.1)
- Slide 15 "the state space landscape" with global maximum / local maximum / flat local maximum / shoulder / current state → chapter §3.2 captures four of five (ridge added in chapter, sourced from slide 14 footnote per chapter's own note)
- Slide 16 annealing physical analogy → chapter §2.C ✓
- Slide 17 SA pseudocode → chapter §4.2 ✓ (textbook-style "track best so far" addition is flagged, which is correct)
- Slide 19 $\exp(\Delta/T)$ curves at $T \in \{100, 50, 10, 1\}$ → chapter §3.5 figure embed ✓
- Slide 20 Geman & Geman log-cooling guarantee → chapter §3.5 ✓
- Slide 22 biology dictionary → chapter §2.D blockquote ✓ (overlap with §3.6, see P2.7)
- Slide 31 binary table for 900 / 300 / 1023 → chapter §5.6 ✓
- Slide 35 three fitness-landscape regimes → chapter §3.7 ✓
- Slides 41–44 worked GA example → chapter §5.7 (mutation step inconsistency — see P1.5)
- Slides 45 / 48 GA pseudocode → chapter §4.3 ✓
- Slide 46 GA variants → chapter §3.6 selection / crossover subsubsections ✓
- Slide 47 typical parameter values N=50, m=0.05, c=0.9 → chapter §6 and §8.6 ✓

**Chapter (`L05-Local-Search.md`):** Read in full, line by line. Cross-checked every §3.x for §2 cross-link presence. Audited §2 analogy roster against §3 concept roster.

**Figure catalogue (`study/extracted_figures/L05/figures.md`):** Read in full. All 18 USE figures embedded; SKIP rationales reasonable. (Not Reviewer #1's territory, but I checked because P1.1's solution touches §2/§3 figure-cross-link positioning.)

**Glossary (`study/_shared/glossary.md`):** Spot-checked terms `A* search`, `Action` for cross-lecture continuity (chapter §7 references `L03 §3` and the glossary's `A*` entry mentions L05 slide 4 — consistent).

---

## SUMMARY ASSESSMENT

This chapter is in the "75% there" zone. The §2 analogy framework is more thoughtfully constructed than most AI textbooks bother with. The flaws are:

1. One genuine **trace error** in §5.1 (P0.1) — must be fixed.
2. A systematic **failure to give every major concept a §2 analogy + caveat** (P1.1) — the spec is explicit and the chapter fails it; the §2.E cheat-sheet table is *not* the analogy.
3. **Cross-link gaps** between §3 and §2 in three of seven §3 subsections (P1.7).
4. **Procedural opacity** in the GA section that forces the reader to flip ahead to pseudocode (P1.3, P1.4).
5. One **inconsistent worked-example caption** in §5.7 (P1.5).

A revision that addresses P0.1 + P1.1 + P1.5 + P1.7 will land at "APPROVED with P2 outstanding".

---

## Report to PM

**Assignment recap:** L05 Local Search — Round 1 Pedagogical-Clarity review (Reviewer #3 of 4) against `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L05-Local-Search.md`, cross-checked against `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture5-Local Search.pdf` (full 50-slide text extraction).
**Status:** Fail — NEEDS_REVISION
**P0 findings:**
1. `L05-Local-Search.md:537-545` — §5.1 8-puzzle hill-climbing trace silently uses the slide-13 strict-`<` rule even though §3.3 line 207 defines termination with `≤`; trace includes an undeclared sideways move ("the slide takes a side-step to a different $-3$") that the chapter's own pseudocode would disallow. Trace successor lists also don't match slide 5. Fix: either commit to `<` and flag the discrepancy in §3.3, or commit to `≤` and re-narrate the example as "hill climbing with sideways budget = N". State this convention once and re-anchor the sign convention at the top of §5.1.

**P1 findings:**
1. `L05-Local-Search.md:49-145` — Spec §7.1 violated: ~7 major §3 concepts (random-restart, first-choice, stochastic hill climbing; temperature schedule; selection, crossover, mutation; fitness landscape) have no proper §2 analogy with caveat. The §2.E one-line table is not a substitute. Add §2.E.1 / §2.F / §2.G subsections with everyday analogies + caveats for selection, crossover, mutation, random-restart, and fitness landscape at minimum.
2. `L05-Local-Search.md:76-79` — §2.B "where the analogy breaks down" caveat for hill climbing praises the algorithm instead of identifying a way the metaphor is misleading. Rewrite to identify a real metaphor breakdown (step-size mismatch, or all-neighbours-evaluated vs feet-only).
3. `L05-Local-Search.md:330-335` — §3.6 Selection paragraph never says you spin the wheel twice (once per parent) to assemble a pair for crossover. Confused students will spin once and reuse the same parent. Add the explicit "spin twice independently" sentence.
4. `L05-Local-Search.md:358-361` — §3.6 Replacement subsubsection has no clear connective tissue linking offspring-generation to "new population replaces old". Add one sentence: "Repeat selection + crossover + mutation until you have N offspring; this set is the new generation; the old population is discarded (generational) or merged-and-truncated (steady-state)."
5. `L05-Local-Search.md:662-664` — §5.7 mutation caption has incomprehensible "(bit 5 flipped, value 0→0 in the labelling but the highlight marks the position considered)" and the bitstring before/after diff suggests bit 6, not bit 5, changed in Offspring 1. State indexing convention once and re-describe each flip as `position k: 0→1` or `position k: 1→0`.
6. `L05-Local-Search.md:60-64` — §2.A: "$8^{8} \approx 16.7$ million states" needs a brief note that the chapter uses the one-queen-per-column parameterisation (which also happens to give $8^8$). Currently silent.
7. `L05-Local-Search.md:319` — §3.6 cross-link to §2.D analogy doesn't redeploy the analogy the way §3.3 and §3.5 do; §3.2, §3.4, §3.7 have no §2 back-link at all. Add proper "Recall the … analogy" sentences in every §3.x subsection.
8. `L05-Local-Search.md:60-64` — §2.A caveat is a single 5-line sentence with nested clauses. Split for readability.
9. `L05-Local-Search.md:692-702` — §6 sign-convention pitfall silently mixes "$h$ in the L03 non-negative sense" with "$h = -(\text{tiles out of place})$ in the slide-5 sense". Commit to $f$ for the maximised objective and $h$ for the L03 heuristic, and footnote slide-5's naming.
10. `L05-Local-Search.md:271-272` — §3.5 "$\Delta > 0$ is improvement; $\Delta < 0$ is worsening" buried in a parenthetical. Promote to a standalone bullet.
13. `L05-Local-Search.md:397-411` — §3.7 fitness landscape lacks its own §2 analogy (the §2.A altimeter analogy is for a single state, not a landscape *of fitnesses*). Add one.
14. `L05-Local-Search.md:128-142` — §2.E one-line analogy table omits first-choice HC, stochastic HC, elitism, tournament selection, population, generation, phenotype/genotype. Add or note as out-of-scope.

(Item P1.11 withdrawn after re-reading; item P1.12 is minor and could be P2 but kept here as it directly affects pedagogical clarity of §6.)

**P2 findings:**
1. Standardise hill-climbing termination operator everywhere; add a one-line footnote at every pseudocode re-display flagging the slide vs chapter difference.
2. §2.A "16.7 million states" needs the BFS-comparison sentence to motivate memory-light.
3. §5.8 numerical SA example would benefit from a 3-row comparison table over $T \in \{100, 10, 1\}$.
4. §5.6 "10 bits because $2^{10} > 1000$" — add the "smallest such power" rule.
5. Mermaid backup diagrams for fig09 and fig14 (per spec §6.1.1) would help.
6. §8.5 cheat-sheet should cite §3.6 as the source dictionary.
7. §2.D blockquote duplicates §3.6 bullet list; pick one location for the biology dictionary.
8. §2.E table capitalisation/hyphenation drift — standardise.
9. §2 lacks a one-line "when to reach for local search vs L03" decision rule (§8.7 has it; bring it forward).
10. Front-matter "Reading time ~55 min" is unverifiable; calibrate or remove.

**QA Checklist (§7) status:** Not my lens. Reviewer #1 handles concept completeness / figure audit; Reviewer #2 handles math rigor; Reviewer #4 handles exam readiness. From my (pedagogical) angle:
- Hand-waving in §5.1 trace: **Fail** (P0.1).
- Every major concept gets an everyday analogy in §2 with caveat: **Fail** (P1.1).
- Cross-links from §3 to §2: **Partial** (4 of 7 §3.x subsections cross-link; P1.7).
- Confused-student readability of §5.7 mutation: **Fail** (P1.5).
- Comparison table §4.4: Pass — student-friendly.
- Cheat sheet §8: Pass — each row carries one-line analogy reminder per spec template.

**Acceptance criteria (§1) status:**
- "Self-contained chapter" (spec line 44): **Not met** due to P0.1 (§5.1 trace requires the slide to interpret) and P1.3/P1.4 (GA section requires flipping to §4.3 pseudocode to know how the loop assembles).
- "Every major concept has an everyday analogy with caveat" (spec §6.1 lecture-chapter template + §7.1 Reviewer #3 mandate): **Not met** (P1.1).

**DOCUMENT.md audit:** N/A — this is a content review, not a code review; the chapter is a single `.md` artifact and the spec does not require `DOCUMENT.md` for `study/lectures/`. (Note for PM: `study/lectures/DOCUMENT.md` is not present and Reviewer #1 or the Verifier should decide whether it's expected.)

**Out-of-scope observations:** None affecting Reviewer #3's lens. (Reviewer #2 should check the §3.5 acceptance-probability formula's case-split definition — I parsed it but didn't verify the math.)

**Concerns / risks:**
- The chapter is currently strong enough that a reader will *trust* it and won't notice §5.1's silent rule-switch — which means the bug propagates undetected into exam preparation. P0.1 is the highest-impact finding by far.
- The analogy-coverage gap (P1.1) is mechanical to close but the chapter is already long (~55 min stated reading time); adding more §2 content risks bloating it. Recommendation: pack the new analogies into a §2.E.1 "Mini-analogies for the GA operators" subsection of ~150 words, rather than expanding each into a full §2.x.

**What PM should do next:** Dispatch Reviser with this report + the other three reviewers' P0/P1 sets. After revision, re-dispatch all 4 reviewers for Round 2. Do not proceed to PDF render until P0.1 is fixed and §2 analogy coverage closes the gap.

**DOCUMENT.md updated:** N/A for QA / lecture reviewer.
