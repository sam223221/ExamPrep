# L05 Round 1 — Reviewer #2 (Mathematical Rigor)

**Reviewer role:** Lecture Reviewer #2 — Mathematical Rigor.
**Scope:** Verify every formula, derivation step, index, notation, assumption, and LaTeX expression in `study/lectures/L05-Local-Search.md` against the canonical source `Lecture5-Local Search.pdf` (slides 1–50). Special focus on the simulated-annealing `exp(Δ/T)` sign convention and the hill-climbing `<` vs `≤` plateau handling.

---

## VERDICT

**FAIL — must revise before Round 2.**

The chapter generally reproduces the formulas with correct mathematical content, but it contains **one P0 contradiction that breaks the cheat sheet against the chapter body** (hill-climbing termination), **one P0 misreading of the slide-12 trace** (numerical values fabricated and inconsistent with the source), plus several P1 issues that mis-state convergence claims, mis-cite slides, and introduce numbers that do not appear in the source (Russell & Norvig anecdote, "$8^{8} \approx 16.7$ million" for 8-queens, etc.). Until the body/cheat-sheet collision and the slide-12 trace are corrected, students reading the chapter will be trained on inconsistent material.

---

## P0 — BLOCKING

### P0-1. Internal contradiction: hill-climbing termination rule (`<` vs `≤`)

The chapter promises in §3.3 that "we adopt above" the `≤` (less-than-or-equal) variant. Section 4.1 then *also* uses `≤`. But **§8.2 (the cheat sheet, the page students will memorise) writes the rule as `≤` too** — so far consistent. The contradiction is with the *source*:

- **Slide 13 (verbatim, source PDF):** *"If value(next) **<** value(current) return current"* — strict less-than.
- **Chapter §3.3 pseudocode (line 207):** `if value(next) ≤ value(current):` — non-strict.
- **Chapter §3.3 prose (line 213–218):** explicitly says "The slide-13 pseudocode uses `<`, which terminates only on a *strict* decrease and would happily traverse plateaux of equal value forever — a known weakness. Most textbooks use `≤` (return on equal or worse), which is what we adopt above."
- **Chapter §4.1 pseudocode (line 427):** `if value(next) ≤ value(current):` — non-strict, matching §3.3 but NOT the slide.

**Why this is P0, not P1:**
1. The pseudocode at line 207 and line 427 is **labelled in the heading "(slide 13)"** (line 420: `### 4.1 Hill climbing (slide 13)`) but it does NOT match slide 13. A student cross-checking the slide will see a mismatch with no warning at the line they are looking at.
2. The §3.3 disclaimer is correct in calling out the variants — but the *exam* will mark students on the slide's `<` rule, not on what "most textbooks use". The chapter changes the algorithm under cover of "we adopt", which is a pedagogically dangerous overreach for an exam-prep document.
3. The author's own pitfall §6 ("Re-introducing the goal test", line 776) writes `value(next) ≤ value(current)` as the canonical termination — entrenching the deviation.
4. Slide 13's `<` rule is actually defensible in the slide's universe: the slide also says `next = highest-valued successor`, so on a plateau every neighbour is equal-valued, not strictly less; with `<` the algorithm would *infinite-loop on the plateau* (not "happily traverse plateaux of equal value forever" — that would require strict improvement). The chapter's prose mis-characterises what `<` does: with `<`, `value(next) < value(current)` is *false* on a plateau, so the algorithm does NOT return — it sets `current ← next` and continues. This is exactly the plateau pathology the slide is meant to expose. The chapter has flipped the diagnostic.

**Fix (one of):**
- (a) **Match the slide.** Replace `≤` with `<` in both §3.3 and §4.1 pseudocode, then add a footnote: *"Slide 13 uses `<`; this terminates on strict decrease and so the algorithm walks indefinitely on a plateau (no improving move but no strict worsening either). Russell & Norvig's textbook adds a sideways-move budget; some variants use `≤` to terminate on a plateau immediately."* This is exam-faithful.
- (b) **Keep `≤` but** (i) change the §4.1 heading from "(slide 13)" to "(adapted from slide 13)", (ii) remove the incorrect prose at lines 213–218 about what `<` does on a plateau, (iii) add a clearer side-by-side: "Slide rule: `<` → infinite-loops on plateau. Textbook rule: `≤` → exits on plateau (but cannot escape shoulders without a sideways budget)."

Either way, the cheat sheet §8.2 must agree with whichever rule is canonical and must explicitly tag it.

**Evidence:** Slide 13 PDF text, lines 207, 213–218, 427, 776, 850 of chapter.

---

### P0-2. Fabricated/mis-traced numbers in §5.4 (slide-12 trace)

**§5.4 "Two-step trace to the global minimum" (lines 602–610)** describes slide 12 as taking the "move-the-bottom-right-column-queen branch", noting per-row $h$ scores and claiming "the best row gives $h = 0$".

**What slide 12 actually shows:**
- **Left board:** annotated rows from top to bottom **2, 2, 1, 2, 3, 1, 2, 2** (per source PDF, page 12). The bottom queen is the one being moved; the annotations show the $h$ value if that queen moves to each row.
- **Slide caption:** *"Queen in lower right of first figure in conflict with 2 others by moving up one row. Moving to a row with 1 conflict would be a local minima."*
- **Middle board:** annotated rows **3, 3, [highlighted box], 2, 3, 2, 3, 0**. The highlighted box (queen moved into one of the upper rows) and the lone "0" near the bottom show where the move leads.
- **Right board:** the final solved configuration ($h=0$).

The chapter claims the *first* board's best row gives $h=0$. **That is wrong.** Slide 12 left board's best row is $h=1$ (which the caption explicitly calls a **local minimum trap**, NOT a global minimum) — and the slide explains that picking that 1-conflict row would *trap* the algorithm. The slide's narrative is: *moving up one row reduces conflicts by 2, but moving to the 1-conflict row would be a local-min trap; some other move (highlighted in the second figure) reaches $h=0$.*

The chapter has inverted the slide's pedagogical point. Worse, it then editorialises: *"The fact that we did reach $h = 0$ here is a happy accident of the tie-breaking rule"* — but the slide is precisely **warning** about that not being a guarantee, and the chapter has the values wrong that would support the warning.

**Why this is P0:** A student studying slide 12 from this chapter will mis-state which board has which $h$, will confuse "1 conflict = local min trap" with "1 conflict = improvement", and may write nonsense on an exam question asking to trace slide 12.

**Fix:** Re-read slide 12 carefully. Restate the trace as: *"From the $h=12$ successor, slide 12 picks a particular queen-move. Most of the rows the bottom queen could move to give $h \in \{2, 3\}$; one row gives $h=1$ (which would be a local-minimum trap, per caption); one row gives $h=0$ (the global minimum). Slide 12 illustrates the tie-broken choice that leads to $h=0$, while explicitly warning that the $h=1$ option would have terminated the algorithm one step short."* The current line 602–605 table is too vague and the "best row gives $h=0$" claim about the *first* board is factually wrong against the slide layout (the first board's best annotated value is $h=1$; the $h=0$ outcome belongs to the second/middle board after a specific move).

**Evidence:** Slide 12 (PDF page 12), lines 602–610 of chapter.

---

## P1 — IMPORTANT

### P1-1. Slide 19 chart re-described with wrong intercept

Lines 287 (§3.5 caption): *"At $T = 100$ even a $\Delta = -100$ move is accepted with probability $\exp(-1) \approx 0.37$."*

Mathematically this is correct: $\exp(-100/100) = \exp(-1) \approx 0.3679$. **But the slide-19 chart (PDF page 19) shows the blue $T=100$ curve crossing $\Delta = -100$ at approximately $0.37$, not at exactly $\exp(-1)$**, and the chart's left edge intercept (at $\Delta = -100$) reads off as approximately $0.36$–$0.37$ — consistent. So the *math* is right. The issue: line 287 also says *"At $T = 1$ the curve is essentially zero except in a tiny sliver near $\Delta = 0$ — the algorithm has become indistinguishable from greedy hill climbing."* This is fine. But the chapter omits the **$T = 50$** and **$T = 10$** curves from the slide entirely. The slide has four curves; the caption describes only two. Add a sentence about $T=50$ (green) intercept at $\exp(-2) \approx 0.135$ and $T=10$ (red) at $\exp(-10) \approx 4.5 \times 10^{-5}$.

**Fix:** Expand the caption to cover all four temperatures from the slide, or explicitly say "of the four curves on slide 19, this caption discusses the extremes ($T=100$ and $T=1$)".

---

### P1-2. Convergence claim cites Geman & Geman without source attribution on the slides

Line 297: *"**Logarithmic (the theoretical optimum):** $T(t) = c / \log(t + 2)$, due to Geman & Geman 1984."*

The Geman & Geman 1984 paper proves a stronger and slightly different result: convergence in probability for a *Gibbs sampler* (Markov random field image restoration), with the cooling schedule $T(t) \ge c / \log(1+t)$ (note: $1+t$, not $t+2$; the $+2$ is just to avoid $\log(1)=0$ when $t=0$ but the paper's canonical form uses $1+t$). The chapter does not flag that **this result is NOT on the slides** — slide 20 only says *"If temperature decreases slowly enough"* without giving the schedule.

**Why P1, not P2:** The chapter is presenting itself as a faithful expansion of the slides. Forward-references to material the slides do not cover should be marked as "out of scope" or "background". The Geman & Geman attribution is a load-bearing citation if a student writes it on the exam — and the constant $c$ has a precise meaning (depth of the deepest local minimum the chain must escape) that the chapter glosses entirely.

**Fix:** Either drop the Geman & Geman citation OR add a one-line footnote: *"Not on the slides; included for context. The constant $c$ in $T(t) = c/\log(1+t)$ must exceed the depth of the deepest local optimum to be escaped (Hajek 1988 sharpened the original result)."*

---

### P1-3. Random-restart completeness claim is over-strong

Line 252: *"Random-restart is the simplest defence against local maxima. It is **complete with probability 1** in finite spaces because, given enough restarts, one of them will start in the basin of the global maximum."*

This requires two assumptions the chapter does not state:
1. The random initial-state distribution has **positive probability on every state** (or at least on every basin of the global maximum). Uniform random over a finite state space gives this; an arbitrary restart distribution does not.
2. Hill climbing from a state in the basin of the global maximum must actually reach it (i.e. the basin is path-connected under the neighbour relation). For convex objectives this is automatic; for n-queens it usually holds but is not guaranteed by the chapter's setup.

Without those assumptions, "complete with probability 1" is a slogan, not a theorem.

**Fix:** Add: *"Assuming the restart distribution has positive probability on the global maximum's basin and hill climbing from that basin always reaches the global maximum, $k$ independent restarts succeed with probability $1 - (1-p)^k \to 1$ as $k \to \infty$."*

---

### P1-4. "$8^{8} \approx 16.7$ million" — wrong arithmetic

Line 62 (§2.A): *"8-queens has $8^{8} \approx 16.7$ million states arranged as a graph"*.

$8^8 = 16{,}777{,}216 \approx 16.78$ million (call it 16.8 million). 16.7 million is closer to $8^8 \times 0.995$, off by about 70,000 — not a rounding error a clean source would make. Minor, but the chapter elsewhere parades precision (e.g. $\exp(-0.5) \approx 0.607$, $\exp(-5) \approx 0.0067$, both correct to 3 sf).

**Fix:** Either write $8^8 = 16{,}777{,}216 \approx 16.8$ million, or write $\approx 1.68 \times 10^7$. Also: this number does not appear on the slides at all — flag it as an aside.

Also, "8-queens has $8^8$" is the *one-queen-per-column-without-row-uniqueness* state space. If the chapter's local-improvement strategy (slide 9, slide 11) is "move within a column", then the actual reachable state space is one queen per column with 8 row choices per column = $8^8 = 16{,}777{,}216$. That's consistent with the strategy. Fine — but the chapter does not say this; it just drops $8^8$ without telling the reader why the exponent is 8 (and not, say, $\binom{64}{8}$ for all placements). Worth one clarifying sentence.

---

### P1-5. "Russell & Norvig report that random-restart hill climbing for 8-queens finds a solution in about 7 restarts on average" — uncited, not on slides

Line 613 (§5.4 "Empirical aside"). The R&N AIMA textbook does report some specific 8-queens numbers — but they are: "starting from a random state, steepest-ascent hill climbing solves only 14% of problem instances; it takes 4 steps on average when it succeeds and 3 when it gets stuck — not a bad result for a state space with $8^8 \approx 17$ million states. […] Random-restart hill climbing […] finds a goal state after a mean of roughly 7 iterations."

The chapter writes "about 7 restarts on average" — this conflates "iterations" (which in R&N's sentence includes both successful runs and failed ones; the expected number is $1/0.14 \approx 7$) with "restarts". The 86% local-minimum number is R&N's (it's $1 - 14\%$). So the math is *coincidentally* correct, but the wording will confuse students who actually read R&N: "iterations" in R&N's sentence means "one run of hill climbing", and the slide does not discuss this empirical result at all.

**Fix:** If this aside is kept, cite the AIMA edition (e.g. Russell & Norvig, AIMA 3e §4.1.1, p. 122) and use R&N's wording: *"Random-restart hill climbing finds a goal state after a mean of roughly 7 iterations" (Russell & Norvig, AIMA 3e, §4.1.1).* Otherwise drop the paragraph — it is not slide content.

---

### P1-6. Acceptance-rule case split: the boundary $\Delta = 0$

Lines 274–279 (§3.5 formula box):

$$P[\text{accept}] = \begin{cases}
  1 & \text{if } \Delta > 0 \\
  \exp(\Delta / T) & \text{if } \Delta \le 0
\end{cases}$$

Note that this writes `Δ ≤ 0` for the second branch. Slide 17 writes: *"if Δ > 0 then let current = next; else let current = next with probability exp(Δ/T(i))"* — so the slide's "else" covers $\Delta \le 0$ (including $\Delta = 0$), exactly as the chapter. So *the math is fine*, but the chapter does not note that **at $\Delta = 0$, $\exp(0) = 1$ — the move is always accepted** in either case, so the case split at $\Delta = 0$ is mathematically a free choice. Slide 17's "if Δ > 0 then accept" plus "else accept w.p. exp(Δ/T)" handles $\Delta = 0$ via the second branch, with probability $\exp(0) = 1$ — i.e. always accepts. Same outcome as putting $\Delta = 0$ in the first branch.

**Why this matters:** A finicky exam might ask: "What is $P[\text{accept}]$ when $\Delta = 0$?" The chapter's formula gives $\exp(0) = 1$ via branch 2; the answer is the same either way, but the chapter never flags this. Worth a one-sentence aside: *"At $\Delta = 0$ (lateral move), the second branch gives $\exp(0) = 1$ — the move is always accepted. This is identical to placing $\Delta = 0$ in the first branch."*

---

### P1-7. §3.2 calls "Ridge" out of slide-14's footnote — but the footnote does NOT describe a ridge

Line 189 (§3.2): *"**Ridge:** (slide 14's *'problems w/ choosing step size, slow convergence'* footnote) a sequence of locally-maximal states whose neighbours within one step are not improvements, yet a chain of moves diagonally up the ridge would improve."*

The slide-14 footnote actually says: *"In continuous spaces, problems w/ choosing step size, slow convergence."* This is about **continuous-space step-size choice**, not about ridges. Ridges as the chapter defines them are a *discrete* phenomenon (alignment of neighbour relation vs. line of maxima). The chapter has misattributed the ridge definition to a slide that does not discuss ridges at all. Slide 15's landscape figure also doesn't label a ridge.

**Fix:** Either remove the (slide 14) parenthetical and admit the ridge definition is supplementary (not on slides), OR replace with a correct attribution to AIMA's discussion of ridges (R&N §4.1.1).

---

### P1-8. "Best-first reading of the slide" — §5.1 8-puzzle trace numbers do not match slide 5

Lines 538–545 (§5.1 trace table):

| Step | Current $h$ | Successors evaluated | Best successor $h$ | Chosen? |
|---|---|---|---|---|
| 0 (start) | $-4$ | one to the left ($-5$), one down ($-3$), one to the right ($-5$) | $-3$ | yes (climb to $-3$) |
| 1 | $-3$ | $-3$, $-4$ | $-3$ (tie) or back up to a $-4$ neighbour | the slide takes a side-step to a different $-3$ |
| 2 | $-3$ | (then a $-2$ successor) | $-2$ | yes |
| 3 | $-2$ | $-1$ | $-1$ | yes |
| 4 | $-1$ | $0$ | $0$ | yes — **goal reached** |

Compare to slide 5 (PDF page 5) annotations:
- **Start** $h=-4$ with three labelled successors at $-5, h=-3, -5$ (the chapter has this right).
- **Step 1** result is $h=-3$, with two labelled successors at $-3$ and $-4$ (chapter correct).
- **Step 2** is $h=-3$ (chapter says step 2 is at $h=-3$, then evaluates a $-2$ — this is correct in spirit but the slide shows the diagram going *right* into a board at $h=-2$, then an additional $-4$ branch off the $h=-3$ middle node).
- **Step 3** $h=-2$, successor $h=-1$ (chapter correct).
- **Step 4** $h=-1$, successor $h=0$ shown via an arrow labelled $-2$ to a $h=-1$ board, then up to the goal $h=0$ (chapter correct).

So the trace is *almost* right but the column "Successors evaluated" at step 1 lists only two ($-3, -4$); slide 5 shows the middle board has children labelled $-3$ and $-4$ on the left arrow and the right arrow respectively. Fine. The step-2 row uses an ambiguous phrasing — "$-3$ (tie) or back up to a $-4$ neighbour" — but the slide shows a single chosen child (the $h=-3$ on the right). And step 2's "(then a $-2$ successor)" is unclear: which successors of the $h=-3$ board? Slide 5 shows a horizontal arrow to a board labelled $h=-2$. The chapter could be clearer that the chosen path is start→$h=-3$ (down child)→$h=-3$ (lateral child? or another step?)→$h=-2$→$h=-1$→$h=0$, which is 5 hops. The chapter is more compressed than the slide and risks a student mis-counting moves.

**Fix:** Re-do the trace as a *node-by-node* walk, listing the board state diagram from slide 5 explicitly. Drop the "or" ambiguity in row 1.

---

### P1-9. Goal-state $h = 0$ claim about 8-puzzle — minor sign/notation slip

Line 534: *"The goal state has $f = 0$."*

Correct *if* $f(n) = -h(n) = -(\text{tiles out of place})$, then goal has 0 tiles out of place and $f = 0$. But the trace uses $h$ values like $-4, -3, ..., 0$ — these are values of $f$, not values of $h$ in the L03 sense. Line 543 starts "Step 0 (start) | $-4$" — labelled "Current $h$", but $h$ in the L03 sense is positive (number of misplaced tiles), so $h = 4$ at the start. The chapter has conflated $h$ (positive distance estimate) with $f = -h$ (its negation for maximisation).

Slide 5 itself writes $h = -4$ at the start, $h = -3$ etc., which strictly is using $h$ for what should be $f$. The chapter inherits the slide's notation collision rather than fixing it.

**Fix:** Add a one-line note at the top of §5.1: *"Slide 5 writes $h = -k$ where $k$ is the number of misplaced tiles. We follow that convention here; strictly, $f(n) = -h(n)$ would be more consistent with §3.1, but to match the slide we use the negative values directly under the label $h$."*

---

### P1-10. Cheat-sheet completeness claims contradict main text

§8.1 cheat-sheet table (line 842):

| Complete? | No | Yes in limit of slow cooling | No (in general) |

§4.4 main comparison table (line 514):

| Complete? | No | Yes (in finite spaces, as $k \to \infty$) | Yes in the limit of slow cooling | Yes in the limit of infinite generations + mutation |

So §4.4 says GA is "Yes in the limit of infinite generations + mutation"; §8.1 says "No (in general)". Both are defensible (the limit claim depends on mutation visiting every state with positive probability), but **the chapter contradicts itself between §4.4 and §8.1**. Also: §4.4 includes a 4-algorithm comparison (random-restart HC as its own column); §8.1 drops random-restart HC entirely. A student switching between the two tables will be confused.

**Fix:** Pick one stance. The exam-safe answer is: GA is *not* complete in the standard sense; "complete in the limit of mutation" is a theoretical curiosity. State that clearly in both tables.

---

### P1-11. "Number of iterations until termination is problem-dependent but typically small" — unjustified

Line 433: *"Complexity: each iteration evaluates $b$ neighbours (where $b$ is the branching factor of the neighbour relation), giving $O(b)$ per step. […] Number of iterations until termination is problem-dependent but typically small."*

"Typically small" is not a property. Hill climbing on an objective with range $[0, M]$ over integers terminates in at most $M$ iterations (each step strictly improves), so an upper bound is the *diameter* of the objective's image — not "typically small". For 8-queens with $h$ ranging over $\{0, 1, \dots, 28\}$, the bound is 28 iterations.

**Fix:** Replace with: *"Number of iterations is bounded by the diameter of the objective's image (each step strictly improves), which is at most $\max f - \min f$ over the reachable set."*

---

## P2 — POLISH / MINOR

### P2-1. LaTeX `\!` thin-negative-space inside `\Big(...\Big)` is overkill (line 277)
The `\exp\!\Big(\dfrac{\Delta}{T}\Big)` is fine but the `\!` adds a thin negative space between `\exp` and the bracket that some renderers (MathJax v2) interpret oddly. Use `\exp\bigl(\Delta/T\bigr)` or `\exp(\Delta/T)`. Cosmetic only.

### P2-2. `\operatorname*{arg\,max}` in line 155 — `\operatorname*{}` puts subscripts below; not all MathJax/KaTeX setups respect the `*`. Use `\mathop{\mathrm{arg\,max}}\limits_{s \in \mathcal{S}}` for portability. Cosmetic.

### P2-3. Line 367–370 roulette-wheel pseudocode index off-by-one
"Compute cumulative fitness: $F_0 = 0$, $F_i = F_{i-1} + f_i$ for $i = 1, \dots, N$. Sample a uniform random number $R \in [0, F]$. Return the smallest $i$ such that $F_i \ge R$."

This works for $R \in (0, F]$ — but at $R = 0$ the smallest $i$ with $F_i \ge 0$ is $i = 0$ (since $F_0 = 0 \ge 0$), and the algorithm would return *index 0*, which is not a chromosome. The standard fix is $R \in (0, F]$ (half-open) or "smallest $i \ge 1$ such that $F_i \ge R$". The chapter says $[0, F]$ (closed both ends). Minor edge case — but a careful exam might test it.

**Fix:** $R \in (0, F]$ OR "smallest $i \in \{1, \dots, N\}$ such that $F_i \ge R$".

### P2-4. Slide-42 cumulative ranges in line 656 are correct but redundant
The chapter writes out chromosome 1 covers $[0,1)$, etc. Slide 42 only writes the chromosome boundaries; the half-open vs. closed convention is the chapter's add-on. Verify against §3.6.1's "smallest $i$ such that $F_i \ge R$" rule: with that rule, $R = 1$ would select chromosome 1 (since $F_1 = 1 \ge 1$), not chromosome 2 — so chromosome 1's slice is $(0, 1]$, not $[0, 1)$. The chapter's intervals are inconsistent with its own selection rule. Minor.

### P2-5. Genetic-algorithm pseudocode at line 478 — `while |new_population| < N` plus appending two children per iteration produces $N+1$ when $N$ is odd
Standard issue. Fix with `while |new_population| < N - 1` plus a single-child fallback, or note "assume $N$ even".

### P2-6. §4.4 comparison-table per-step cost claim "GA: $O(N)$ per generation in fitness evaluations" is *probably* wrong dimensionally
A generation produces $N$ offspring and evaluates $N$ fitnesses; if fitness costs $F$ each then cost is $O(NF)$. Selection is $O(N)$ per parent draw via the naïve linear scan, $2N$ draws ⇒ $O(N^2)$ total per generation. Crossover and mutation are $O(L)$ per offspring ⇒ $O(NL)$ per generation. So the dominant per-generation cost is $O(N^2 + N(F + L))$, not $O(N)$. Acceptable shorthand for an exam-prep chapter, but worth flagging.

### P2-7. Line 287 — "essentially zero except in a tiny sliver near $\Delta = 0$" describing $T=1$
$\exp(-1/1) = \exp(-1) \approx 0.37$ at $\Delta = -1$; $\exp(-2) \approx 0.135$ at $\Delta = -2$; $\exp(-5) \approx 0.0067$ at $\Delta = -5$. So the "tiny sliver" is roughly $\Delta \in [-3, 0]$ (where $\exp(\Delta) > 0.05$). The chapter could be quantitative here. Polish.

### P2-8. §5.6 oil example — chromosome 900 = 1110000100 — is this 900?
Binary 1110000100 = $512 + 256 + 128 + 4 = 900$. ✓ Verified.
Chromosome 300 = 0100101100 = $256 + 32 + 8 + 4 = 300$. ✓ Verified.
Chromosome 1023 = 1111111111 = $1023$. ✓ Verified.

Good — math is right.

### P2-9. Line 664 (§5.7 mutation example) — "bit 5 flipped, value 0→0 in the labelling but the highlight marks the position considered"
This is incoherent. Slide 44 shows Offspring 1 mutating from `1011011111` → `1011001111`. Comparing bit-by-bit: positions are (1)1011011111 vs (2)1011001111 — bits differ at position 5 (counting from 1, left to right): position 5 is `0` in original and `0` in mutated. Wait, let me re-count:

```
1 0 1 1 0 1 1 1 1 1
1 0 1 1 0 0 1 1 1 1
```

Position 6 changes from `1` to `0`. So bit 6 flipped 1→0, NOT bit 5 flipped 0→0. The chapter is wrong about which bit changed AND wrong about the direction. The slide-44 highlight in the source PDF is on position 6 of Offspring 1 (where the `1` became `0`).

For Offspring 2: `1000000000` → `1010000000`. Position 3 changes from `0` to `1`. Chapter says "bit 3 flipped 0→1" — ✓ correct.

**Fix:** Change line 664 from "bit 5 flipped, value 0→0" to "bit 6 flipped 1→0".

### P2-10. §3.4 first-choice hill climbing description (line 250)
"Cheap when the branching factor is huge (e.g. continuous spaces, $\infty$ neighbours)." A continuous space has uncountably many neighbours; "first-choice" still requires *sampling* neighbours. The description is fine but "$\infty$ neighbours" is imprecise. Polish.

### P2-11. The "MENTAL MODEL" reference in line 802 to Lab 4 is an in-codebase reference whose existence I cannot verify from this review; flag for cross-doc check.

---

## EVIDENCE

| Issue | Source location | Chapter location |
|---|---|---|
| Hill-climbing `<` vs `≤` | Slide 13 (PDF p. 13) | Lines 207, 213–218, 427, 776, 850 |
| 8-queens slide-12 trace | Slide 12 (PDF p. 12), caption + per-row $h$ annotations | Lines 602–610 |
| Slide-19 chart | Slide 19 (PDF p. 19), 4 curves: $T \in \{100, 50, 10, 1\}$ | Line 287 |
| Geman & Geman | Not on slides; slide 20 is silent on schedule form | Line 297 |
| Random-restart completeness | Slide 15 (PDF p. 15) — no formal claim made | Line 252 |
| $8^8$ value | Not on slides | Line 62 |
| R&N "7 restarts" | Not on slides | Line 613 |
| Acceptance at $\Delta = 0$ | Slide 17 (PDF p. 17), branch covers $\Delta \le 0$ | Lines 274–279 |
| Ridge definition | Slide 14 footnote is about continuous step-size, not ridges | Line 189 |
| 8-puzzle $h$ vs $f$ notation | Slide 5 writes $h = -4, -3, \dots, 0$ | Lines 534, 538–545 |
| Completeness cheat-sheet vs §4.4 | — | Lines 514 vs 842 |
| Hill-climbing iteration bound | Slide 13 has no such claim | Line 433 |
| Roulette wheel $R \in [0, F]$ edge | Slide 40 says "in that range" — ambiguous | Lines 367–370, 656 |
| Mutation bit-flip slide 44 | Slide 44 (PDF p. 44): Offspring 1 bit 6 flipped 1→0 | Line 664 |

---

## Report to PM

**Assignment recap:** L05 Local Search — Round 1 mathematical-rigor review of `study/lectures/L05-Local-Search.md` vs. `Lecture5-Local Search.pdf`. Special focus per brief: SA `exp(Δ/T)` sign convention; hill-climbing `<` vs `≤`.

**Status:** Fail. Two P0 issues block re-publication; eleven P1 issues degrade exam-faithfulness; eleven P2 issues are polish-tier.

**P0 findings:**
1. **Lines 207/213–218/427/776/850 (Hill-climbing termination):** Chapter pseudocode uses `≤` but is labelled "(slide 13)" while slide 13 unambiguously writes `<`. Chapter prose explaining what `<` does on a plateau is **factually backwards** (`<` does not "terminate" on a plateau — it loops forever; that *is* the slide's pedagogical point and the chapter has inverted it). Fix: either match the slide (`<` everywhere with a footnote on the plateau pathology) or keep `≤` with explicit "adapted from slide 13" labelling and corrected prose. The cheat sheet at §8.2 must then match.
2. **Lines 602–610 (slide-12 8-queens trace):** The "best row gives $h = 0$" claim about the slide-12 left board is wrong; the slide's left board annotations are `{2, 2, 1, 2, 3, 1, 2, 2}` and its caption explicitly warns that the $h=1$ row is a **local-minimum trap**. The chapter has inverted the slide's pedagogical point. Fix: re-read slide 12; rewrite the trace; preserve the slide caption's warning.

**P1 findings:**
1. Line 287 — slide-19 caption omits $T=50$ and $T=10$ curves entirely.
2. Line 297 — Geman & Geman 1984 attribution is not on the slides and the schedule form $c/\log(t+2)$ is slightly off the canonical $c/\log(1+t)$.
3. Line 252 — random-restart "complete with probability 1" claim omits two required assumptions (positive-probability restart distribution; basin reachability under neighbour relation).
4. Line 62 — "$8^8 \approx 16.7$ million" should be 16.8 million ($8^8 = 16{,}777{,}216$); also state space size needs one sentence of justification.
5. Line 613 — R&N "7 restarts" anecdote is paraphrased imprecisely (iterations vs restarts) and uncited.
6. Lines 274–279 — SA acceptance formula at $\Delta = 0$ boundary should be noted as $\exp(0) = 1$ ⇒ always accepted.
7. Line 189 — Ridge definition mis-attributed to slide 14's continuous-step-size footnote.
8. Lines 538–545 — §5.1 8-puzzle trace is compressed and ambiguous ("$-3$ (tie) or back up to a $-4$ neighbour").
9. Line 534 — $h$ vs $f$ notation collision in §5.1 (slide 5 writes $h = -k$; chapter inherits without flagging).
10. Lines 514 vs 842 — comparison tables contradict on GA completeness (Yes-in-limit vs No-in-general).
11. Line 433 — "typically small" iteration-count claim should be replaced by the diameter-of-image bound.

**P2 findings:**
1. P2-1 LaTeX `\!` cosmetic issue (line 277).
2. P2-2 `\operatorname*{}` portability (line 155).
3. P2-3 Roulette-wheel edge case at $R = 0$ (lines 367–370).
4. P2-4 Slide-42 interval-convention inconsistency with §3.6.1 (line 656).
5. P2-5 GA pseudocode off-by-one when $N$ is odd (line 478).
6. P2-6 §4.4 per-step-cost is $O(N^2 + N(F+L))$, not $O(N)$.
7. P2-7 "$T=1$ tiny sliver" could be quantitative.
8. P2-8 §5.6 oil example binary values — verified correct.
9. P2-9 Line 664 mutation example — bit 6 flipped 1→0, not "bit 5 flipped 0→0".
10. P2-10 Continuous-space "$\infty$ neighbours" imprecise.
11. P2-11 Lab 4 cross-reference unverified by this review.

**QA Checklist (§7) status (math-rigor lens only — other reviewers cover the rest):**
- [x] Every formula vs source — **Fail** (P0-1 hill-climbing `<` vs `≤`; P1-2 Geman & Geman schedule)
- [x] Missing derivation steps — **Pass with concerns** (P1-3 random-restart completeness assumptions missing)
- [x] Wrong indices — **Fail** (P2-3 roulette-wheel index, P2-9 mutation bit number)
- [x] Ambiguous notation — **Fail** (P1-9 $h$ vs $f$; P2-4 interval conventions)
- [x] Dropped assumptions — **Fail** (P1-3 random-restart; P1-6 $\Delta = 0$ boundary)
- [x] LaTeX errors — **Pass with concerns** (P2-1, P2-2 portability only)
- [x] SA sign convention — **Pass** (the formula and case-split are mathematically correct; only $\Delta = 0$ boundary nit)
- [x] Hill-climbing `<` vs `≤` — **Fail** (P0-1)

**Acceptance criteria (§1) status:** N/A — this is a lecture chapter, not a feature.

**DOCUMENT.md audit:** Out of scope for math-rigor review; defer to Reviewer #1 / structural reviewer.

**Out-of-scope observations:**
- The chapter has a strong rhetorical voice ("the lecturer's master landscape diagram", "the single most-tested trap", "shaking a settling marble") that is great for retention but in three places (§5.4 slide-12 trace, §3.2 ridge definition, §6 "Empirical aside") it lets editorial flourish run ahead of source fidelity. A copy-editing pass focused on "does this sentence claim something that is on a slide?" would catch most P1s.
- The chapter cites the slide for many statements that are *not* on the slide (Geman & Geman, R&N 8-queens numbers, the geometric/logarithmic schedules). Either move these to a "supplementary" subsection or remove the slide attribution.
- The §6 "Common Pitfalls" section is genuinely well-curated — but its own pseudocode at line 776 entrenches the `≤` choice that contradicts the slide. Fix as part of P0-1.

**Concerns / risks:**
- A student memorising the chapter cheat sheet (§8.2) verbatim will write the wrong termination rule for slide-13-style exam questions. This is the chapter's highest-stakes error.
- The slide-12 inverted trace (P0-2) is the kind of error a sharp examiner could write a trap question around: "Why is the move to the $h=1$ row a problem?" — the chapter as currently written has no clean answer because it has the values wrong.

**What PM should do next:**
1. Dispatch the lecture-author agent to fix P0-1 and P0-2 first. These two changes alone unblock Round 2.
2. After P0 fixes, address P1-1 through P1-11 in one editing pass.
3. Defer P2-1 through P2-11 to a final-polish pass or batch them into a "minor cleanup" issue.
4. Do NOT proceed to App Tester / Code Reviewer equivalents (pedagogical-tester / structural-reviewer) until P0s are clear — the cheat sheet currently teaches a rule the slide does not have.

**DOCUMENT.md updated:** N/A for QA.
