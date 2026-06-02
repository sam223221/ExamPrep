# L05 Round 1 — Reviewer 4 (Exam Readiness)

**Reviewer role:** Lecture Reviewer #4 — Exam Readiness gate per spec §7.1.
**Method:** Imagine 10 plausible exam questions drawn from the L05 slide deck (Local Search). For each, judge whether the chapter (`study/lectures/L05-Local-Search.md`) **alone**, without the slides, the textbook, or external context, lets a student produce a full-credit answer. Be harsh: incomplete derivations, missing numbers, hand-waved formulas, or "look at the slide" hedges = fail.

---

## VERDICT

**FAIL — chapter is not exam-ready as a standalone study artifact.**

Headline reasons:
1. The chapter **invents content that contradicts the slides** (a P0 trust failure). Most damaging: the slide-13 pseudocode termination condition (`<`) is overwritten with `≤` and labelled as "what we adopt" — a student answering "reproduce the lecture pseudocode" loses marks. (See P0-1.)
2. Multiple **worked examples are unreliable**: the 8-puzzle slide-5 trace is reconstructed incorrectly and admits it ("the slide takes a side-step"); the GA mutation example contains an internal contradiction ("0→0 in the labelling"); the slide-9 4-queens objective values are wrong vs. the slides. (See P0-2, P0-3, P0-4.)
3. Three of the ten exam-style questions cannot be answered cleanly from the chapter without the student already knowing the answer. (See coverage matrix below.)
4. Several **factual claims are not in the slides and are not flagged as external**: the cooling-schedule menu (linear/geometric/log) with Geman & Geman attribution, the $\binom{n}{2}$ neighbour count, the 86%/7-restarts R&N empirical numbers, and the completeness-of-random-restart claim "as $k \to \infty$" are all editorial additions. They are *plausibly* correct, but a student who memorises them and is then asked "what did the lecture say" will be wrong-footed.

The chapter is *more* than the slides, which is fine, but the additions and substitutions are not labelled, leaving the student unable to distinguish "what the exam can test you on" from "what the author wishes the lecture had said."

---

## P0 — Blockers (must fix before this chapter can be trusted)

### P0-1. Hill-climbing termination condition silently contradicts the slide

**EVIDENCE.** Chapter, §3.3, lines 207–219:

```
if value(next) ≤ value(current):
    return current
```

and the prose: *"The slide-13 pseudocode uses `<`, which terminates only on a strict decrease and would happily traverse plateaux of equal value forever — a known weakness. Most textbooks use `≤` … which is what we adopt above."*

Slide 13 (verbatim): *"If value(next) **<** value(current) return current."*

The chapter knowingly substitutes a different condition and propagates `≤` to §4.1, §8.2 ("Hill climbing termination: value(next) ≤ value(current) ⇒ return current"). On an exam asking "state the hill-climbing termination condition from the lecture," the student will write the wrong one. The author's footnote about textbooks is interesting but does not absolve the substitution — and the substitution is also wrong on its own terms: `≤` returns on equality, which is exactly the *opposite* of "would happily traverse plateaux of equal value forever." The slide-13 `<` is what allows plateau traversal; `≤` shuts it off. The justification given is therefore confused.

**Fix.** Reproduce slide 13's `<` as the primary pseudocode. If the author wants to discuss the textbook alternative, do so in a clearly-flagged sidebar that says "the slide uses `<`; some textbooks use `≤`; here is what changes."

### P0-2. The 8-puzzle hill-climbing trace (§5.1) does not match the slide

**EVIDENCE.** Chapter §5.1 lines 537–545 gives this trace:

| Step | Current $h$ | Successors | Best | Chosen |
|---|---|---|---|---|
| 0 | $-4$ | $-5, -3, -5$ | $-3$ | yes |
| 1 | $-3$ | $-3, -4$ | $-3$ (tie) | side-step |
| 2 | $-3$ | "then a $-2$" | $-2$ | yes |
| 3 | $-2$ | $-1$ | $-1$ | yes |
| 4 | $-1$ | $0$ | $0$ | yes — goal |

The slide-5 figure shows the start board at $h=-4$, with successor labels $-5, -3, -5$ at the top; then $h=-3$ → with successor labels $-3, -4$; then $h=-3$ again; then $h=-2$, $h=-1$, $h=0$. The chapter's step 1 says "best successor $h=-3$ (tie) or back up to a $-4$ neighbour" and then writes "the slide takes a side-step to a different $-3$." That is **not a hill-climbing move** — it is a *sideways* move from $-3$ to $-3$, which the slide-13 termination rule (`if value(next) < value(current) return current`) permits, but the chapter's own adopted rule (`≤`) **forbids**. So the chapter's own worked example violates the chapter's own pseudocode. A student who tries to reproduce the trace using the §3.3 pseudocode will terminate at step 1 and never reach the goal.

This is a textbook self-contradiction and it cannot be papered over.

**Fix.** Either (a) restore the slide-13 `<` condition (preferred — see P0-1) and explain that sideways moves are allowed, then the trace works, or (b) admit explicitly that the slide demonstrates a *first-improving-or-equal* variant, not the strict best-successor algorithm.

### P0-3. The 4-queens slide-9 figure is misrepresented

**EVIDENCE.** Chapter §5.3 lines 574–579:

> *"**Left:** $h = 5$ — five attacking pairs … **Middle:** after one local improvement, $h = 2$. **Right:** after another, $h = 0$ — solved."*

Slide 9 verbatim labels the three boards $h=5$, $h=2$, $h=0$. So far so good. But the figure on slide 9 shows the **left board with four queens on the same row (bottom row)** and the attacking-pair lines drawn between the four bottom-row queens plus another queen on row 3 — five pairs total, all in conflict via row/diagonal lines that are explicitly drawn. The chapter says "Move = within a column, move the queen to a different row" — but the slide-9 left figure shows several queens *in the same row*, which is not a one-per-column configuration. The slide-9 example actually uses the **complete state-space formulation** (queens can be anywhere), not the **complete-state per-column formulation** introduced for 8-queens later on slides 10–12. The chapter conflates the two and tells the student they are the same.

A student asked "describe the state space and move set used in the 4-queens slide" will get this wrong.

**Fix.** Either drop the §5.3 commentary about "move = within a column" or explicitly say slide 9 uses a different state space than slides 10–12.

### P0-4. GA mutation example (§5.7 step 4) contains a self-contradicting sentence

**EVIDENCE.** Chapter §5.7 line 664:

> *"the slide shows Offspring 1 = `1011011111` mutated to `1011001111` (bit 5 flipped, value 0→0 in the labelling but the highlight marks the position considered)"*

"bit 5 flipped, value 0→0" is a nonsense flip — a flip changes the bit. Compare the two strings:
- Offspring 1 before: `1011011111`
- Offspring 1 after:  `1011001111`

The change is at position 5 (counting from 1), where `1` → `0`. The chapter says "0→0" which is wrong. The slide itself is clear (slide 44: the mutated offspring `1011001111` differs from `1011011111` at one bit). The author has misread their own slide.

Also Offspring 2: `1000000000` → `1010000000`. The change is position 3: `0` → `1`. The chapter says "bit 3 flipped 0→1." That one is right.

A student copying the §5.7 description into an exam answer will write something incoherent.

**Fix.** Replace with: "Offspring 1: bit 5 flipped `1` → `0`, giving `1011001111`. Offspring 2: bit 3 flipped `0` → `1`, giving `1010000000`."

### P0-5. The "completeness" row of the §4.4 comparison table is misleading and contradicts the chapter's own pitfalls section

**EVIDENCE.** §4.4 (line 514):

| | Hill climbing | Random-restart HC | Simulated annealing | Genetic algorithm |
| **Complete?** | No | **Yes (in finite spaces, as $k \to \infty$)** | **Yes in the limit of slow cooling** | **Yes in the limit of infinite generations + mutation** |

But §6 ("Hill climbing is complete" — false) line 712: *"Plain hill climbing is **not complete**, period."* — that part agrees. However the slides (slide 49, summary): "Simulated annealing escapes local optima, and is **optimal** given a 'long enough' cooling schedule." Slide 20: *"global optimum with probability approaching one."* The slides say **optimal**, not **complete**, and they specifically do **not** claim GA completeness at all. The chapter's "Yes in the limit of infinite generations + mutation" for GAs has no slide basis. This is editorial.

Worse, the §4.4 row makes both *completeness* and *optimality* "yes in the limit" for SA, while the chapter's §6 pitfall says: *"The exam-safe formulation is: 'simulated annealing converges to the global optimum if the schedule cools sufficiently slowly; standard practical schedules do not satisfy this condition.'"* — i.e., do not claim completeness on the exam. The chapter has it both ways depending on which section you read.

An exam question "Is hill climbing complete? Is simulated annealing complete? Is GA complete?" will produce different answers depending on whether the student studied the table or the pitfalls.

**Fix.** Pick one story and propagate it. The slide-accurate version: hill climbing is **incomplete**; simulated annealing finds the **global optimum with probability → 1** under slow-enough cooling (do not call this "complete" without qualification); GA — slides make no formal completeness claim.

---

## P1 — Important issues (will cost marks on the exam)

### P1-1. The cooling-schedule menu is not in the slides and is not flagged as external

**EVIDENCE.** §3.5 lines 294–298 lists Linear, Geometric, Geometric with $\alpha \in [0.85, 0.99]$, and "Logarithmic (the theoretical optimum) $T(t) = c/\log(t+2)$, due to Geman & Geman 1984." None of these formulas appear on the slides — slide 18 only says "T gradually decreased to 0 over time t." Slide 20 says "If temperature decreases slowly enough" without a formula. The chapter quietly adds three formulas and attributes one to Geman & Geman.

Adding canonical content is reasonable for an exam-prep guide, but here it is not marked as "outside the slides." A student writing "the lecture says the geometric schedule is $T(t+1) = \alpha T(t)$ with $\alpha \in [0.85, 0.99]$" will be wrong — the lecture said no such thing.

**Fix.** Tag the box with "(not on slides — standard reference)" or move it to a clearly-labelled appendix.

### P1-2. The slide-7 TSP neighbour count is editorialised

**EVIDENCE.** Chapter §5.2 line 564: *"The neighbours of a tour with $n$ cities number $\binom{n}{2}$ pairwise swaps."* Not on the slides. Slide 7 shows ABDEC → ABCED, one specific 2-opt move, and nothing about how many neighbours a tour has. The claim is also technically debatable — 2-opt produces $\binom{n}{2} - n$ distinct neighbours for an $n$-city cycle (you can't swap adjacent edges in the obvious way without producing the same tour). The chapter has overreached.

**Fix.** Either drop the count or pin it correctly with a derivation.

### P1-3. Russell & Norvig empirical numbers presented as fact

**EVIDENCE.** Chapter §5.4 lines 612–615: *"Russell & Norvig report that random-restart hill climbing for 8-queens finds a solution in about 7 restarts on average; plain hill climbing terminates at a local minimum (typically $h = 1$ to $h = 3$) about 86% of the time."* Not in the slides. Sourced from R&N AIMA. Useful, but if the exam asks "according to the lecture, how often does hill climbing solve 8-queens," the answer "86% failure rate, 7 restarts on average" comes from a textbook the lecture did not assign as primary reading.

**Fix.** Tag as "(AIMA aside, not on slides)" or remove.

### P1-4. The "ridge" pathology is asserted in §3.2 and §6 with no slide support

**EVIDENCE.** §3.2 line 189 introduces "ridge" as one of five named features. Slide 15 labels only **four** features (global maximum, local maximum, flat local maximum, shoulder) plus the "current state" annotation. There is no "ridge" on slide 15. The chapter's slide-14 reference (*"slide 14's 'problems w/ choosing step size, slow convergence' footnote"*) is a stretch — slide 14 says only "In continuous spaces, problems w/ choosing step size, slow convergence," nothing about ridges.

A student asked "list the named features of the state-space landscape from slide 15" will list five and get marked down to four.

**Fix.** Remove "ridge" or move it to §6 (Pitfalls) flagged as "common pathology not named in slide 15."

### P1-5. Acceptance-rule branch boundary inconsistent

**EVIDENCE.** §3.5 line 275–278:

```
P[accept] = 1            if Δ > 0
          = exp(Δ/T)     if Δ ≤ 0
```

But the slide-17 pseudocode says: *"if Δ > 0 then let current = next; else let current = next with probability exp(Δ/T)."* The "else" includes $\Delta = 0$, which is fine in both formulations — but the chapter's §4.2 pseudocode says:

```
if Δ > 0:
    current ← next                # uphill: accept
else:
    with probability exp(Δ / T):
        current ← next            # downhill: maybe accept
```

When $\Delta = 0$, $\exp(0/T) = 1$, so the move is accepted with probability 1 — same outcome. Fine. But the *labels* are wrong: the chapter calls the $\Delta = 0$ case "downhill: maybe accept" when in fact it is "lateral: always accept." This is a small thing but pedagogically misleading on an exam where precision counts.

**Fix.** Either fold $\Delta = 0$ into the "always accept" branch (matching common practice and being unambiguous) or relabel the comment.

### P1-6. Slide-attribution in §5.7 is wrong for the slide-42 ranges

**EVIDENCE.** Chapter §5.7 line 656 describes the roulette wheel as: *"chromosome 1 covers $[0,1)$, chromosome 2 covers $[1,3)$, chromosome 3 covers $[3,6)$, chromosome 4 covers $[6,7)$, chromosome 5 covers $[7,10)$, chromosome 6 covers $[10,15)$, chromosome 7 covers $[15,16)$, chromosome 8 covers $[16,18)$."*

Slide 42 shows a horizontal bar segmented by fitness values 1, 2, 3, 1, 3, 5, 1, 2 (sum 18). The chapter's ranges are correct (cumulative sums of the fitnesses). But the slide-42 caption shows draw $R=7$ selecting **chromosome 4** and $R=12$ selecting **chromosome 6**. Per the chapter's own ranges, $R=7$ falls in chromosome 5's slice $[7, 10)$, not chromosome 4's $[6, 7)$ — unless the convention is "select the first $i$ such that $F_i \ge R$," in which case $F_4 = 7 \ge 7$ → chromosome 4. The chapter's §3.6.1 selection rule says exactly that ("smallest $i$ such that $F_i \ge R$"), so the slide-42 outcome is consistent — but only with the boundary convention "closed on the right." The chapter's prose ranges $[0,1), [1,3), \dots$ are **left-closed, right-open** which means $R=7$ falls in $[7,10)$ = chromosome 5, contradicting the slide's "chromosome 4" answer.

A student walking through §5.7 with the chapter's ranges will get a different answer than the slide. The rule and the ranges are not in sync.

**Fix.** Make the ranges left-open, right-closed: $(F_{i-1}, F_i]$, so $R=7$ falls in $(6, 7]$ = chromosome 4. This matches the §3.6.1 rule and the slide-42 outcome.

### P1-7. Hill-climbing complexity row in §4.4 mis-states per-step cost

**EVIDENCE.** §4.4 (line 512): "Per-step cost: $O(b)$ — evaluate all neighbours." For 8-queens, slide 11 makes explicit that the number of neighbours is $8 \times 7 = 56$, not "branching factor $b$." For the 8-puzzle, slide 5, the branching factor is at most 4 (blank can move at most 4 directions). The chapter never tells the student that "branching factor of the neighbour relation" is problem-defined and is not the same as the L03 branching factor of the successor function. A student answering "what is the per-iteration time complexity of hill climbing on 8-queens?" should write $O(n(n-1)) = O(n^2)$, not $O(b)$. The chapter does not teach this.

**Fix.** Add a one-line note: "for $n$-queens, $b = n(n-1)$; for the 8-puzzle, $b \le 4$."

### P1-8. "Simulated annealing acceptance" cheat-sheet formula uses the wrong branch label

**EVIDENCE.** §8.2 (line 851): the cheat-sheet repeats the §3.5 formulation including the labelling problem from P1-5. If the cheat sheet is "what to memorise," it should be unambiguous.

**Fix.** Same as P1-5.

### P1-9. Coverage gap: the chapter never works through a worked simulated-annealing trace using a specific cooling schedule

**EVIDENCE.** §5.8 (lines 672–683) has a single arithmetic example: $T=10$, $\Delta=-5$, $P = e^{-0.5} \approx 0.607$; $T=1$, $\Delta=-5$, $P = e^{-5} \approx 0.0067$. That confirms a student can plug numbers in. But none of:

- A 3- or 4-step trace
- An actual schedule (e.g., $T_0=100$, $\alpha=0.9$) and what happens over 5 iterations
- A worked decision: "$T=20$, $\Delta=-3$, random draw $u=0.85$ — do we accept?"

are present. The slide deck does not provide this either, so the omission is partly the lecturer's, but the chapter is supposed to be a study artifact more comprehensive than the slides. Exam Q (see Q5 below) is unanswerable without this.

**Fix.** Add a multi-step worked example with a concrete schedule.

### P1-10. The chapter does not actually define "successor function" for the 8-queens problem in a way that lets the student compute it

**EVIDENCE.** §5.4 line 588–589: *"For each of 8 columns, the queen in that column can move to any of the other 7 rows. So 56 successors total."* Good. But the chapter never asks: "is the queen-on-its-current-row counted as a successor?" The slide-11 says "8\*7 = 56 states reachable after a given move in a column," implying the current row is *excluded*. The chapter agrees by arithmetic ($8 \times 7$, not $8 \times 8$) but never tells the student why — and a question "how many successors does a board with 8 queens have?" will get $8 \times 8 = 64$ from a student who hasn't been told to exclude the current row.

**Fix.** One sentence: "a queen does not move to its own row, so each column contributes 7 successors, not 8."

---

## P2 — Polish / minor

### P2-1. "Geman & Geman 1984" is cited without a real reference list
The chapter has no bibliography. P1-1 already flags the content issue; P2 here is the missing reference.

### P2-2. Forward references to L06, L10, L11, L12 in §7 are speculative
Lines 796–822 link to lectures that may not exist yet at the same level of detail. If a student clicks and the link is dead, trust erodes. Either gate these behind "if available" or remove until the dependent lectures exist.

### P2-3. The "8-queens has $8^8 \approx 16.7$ million states" claim (§2.A)
This assumes the complete-state per-column formulation ($8^8 = 16{,}777{,}216$). The chapter never tells the student this is the assumption — and the slide-9 figure uses a different formulation (see P0-3). A student asked "how big is the 8-queens state space?" can give multiple answers (with/without "one per column" / "no two same row" constraints) and the chapter doesn't disambiguate.

### P2-4. "Heuristic function (concretised here)" in §1 glossary list
The chapter lists "heuristic function (concretised here)" but the L03 lecture is supposed to introduce it. The glossary intro is unclear about whether L05 introduces it for the first time or merely reuses it.

### P2-5. Figure references to `../extracted_figures/L05/figXX-*.png` cannot be validated from text alone
A student reading the chapter offline (no figures) loses important slide-15 landscape, slide-19 temperature curves, slide-32 oil-yield curve. Not the chapter's fault if the figures exist on disk, but the prose should be self-contained enough that a no-figure read still works. Currently §5.4–§5.7 lean heavily on "see fig08" / "see fig18."

### P2-6. §8.7 ("When to use which") presents GA for "Combinatorial space with a meaningful crossover operator"
The slide deck makes no such recommendation. This is editorial. Useful, but not exam-defensible.

---

## EVIDENCE: 10 Imagined Exam Questions and Coverage Verdict

For each question, I score whether the chapter (no slides, no textbook) lets a typical student produce a full-credit answer.

| # | Imagined Exam Question | Chapter coverage | Pass? |
|---|---|---|---|
| **Q1** | *"State the pseudocode for hill-climbing search as given in the lecture. Specify the termination condition."* | §3.3 and §4.1 give a pseudocode with `≤` termination. **Slide-13 uses `<`.** Student will lose marks. | **FAIL** (P0-1) |
| **Q2** | *"Walk through the 8-puzzle hill-climbing trace from slide 5, listing each state's $h$ value and the chosen successor."* | §5.1 trace contradicts the slide-5 path (the chapter's `≤` rule terminates at step 1; the slide allows sideways). | **FAIL** (P0-2) |
| **Q3** | *"Define the objective function and move/neighbour relation for 8-queens. How many successors does an 8-queens board have?"* | §3.1 (objective), §5.4 (move = one queen, within column, to a different row), and "8\*7 = 56 successors." | **PASS** (with note: the chapter never explains *why* 56 not 64 — P1-10) |
| **Q4** | *"Write the simulated-annealing acceptance probability formula and explain each symbol."* | §3.5 and §8.2 give $P = \exp(\Delta/T)$ for $\Delta \le 0$. Symbols defined: $\Delta = f(\text{next}) - f(\text{current})$, $T = T(t)$. | **PASS** |
| **Q5** | *"Given $T_0 = 100$, geometric cooling with $\alpha = 0.9$, and a sequence of three proposed moves with $\Delta = +2, -3, -10$, decide which moves are accepted with the given uniform draws $u_1 = 0.4, u_2 = 0.8, u_3 = 0.6$."* | §5.8 has one numeric example with no schedule and no random draw. **No multi-step trace, no acceptance test using a $u$ draw.** | **FAIL** (P1-9) |
| **Q6** | *"Given the slide-41 GA population (fitnesses 1,2,3,1,3,5,1,2 totalling 18) and a uniform draw $R=7$, which chromosome is selected? Show the cumulative sums."* | §5.7 cumulative ranges contradict the slide-42 answer due to a half-open-interval boundary issue (P1-6). Student following the chapter answers "chromosome 5"; slide says "chromosome 4." | **FAIL** (P1-6) |
| **Q7** | *"Apply single-point crossover at position 3 to parents `1010000000` and `1001011111`. Then mutate Offspring 1 at position 5. Give the final two offspring."* | §5.7 (slides 43–44) walks through this — though with the bit-flip mislabelled (P0-4). The crossover step is fine; the mutation prose is broken. | **PASS with concerns** (student must ignore §5.7's broken sentence) |
| **Q8** | *"Is hill climbing complete? Is simulated annealing complete? Is GA complete? Justify."* | §4.4 says "Yes in the limit" for SA and GA completeness — but §6 walks it back to "exam-safe formulation: not complete in practice." Internal contradiction (P0-5). | **FAIL** (P0-5) |
| **Q9** | *"Name and define four features of the state-space landscape from slide 15."* | §3.2 lists five (global max, local max, flat local max, shoulder, ridge). Slide 15 has four — ridge is not on the slide. (P1-4) | **PASS** (student can pick 4 of 5; the extra is wrong but recoverable) |
| **Q10** | *"State the GA loop. Give typical values for population size $N$, mutation rate $m$, crossover rate $c$."* | §4.3 pseudocode and §8.6 cheat sheet both give $N=50, m=0.05, c=0.9$. Matches slide 47. | **PASS** |

**Score: 5 PASS, 1 PASS-with-concerns, 4 FAIL.** A study artifact that fails 40% of plausible exam questions is not ready.

---

## Recommendations to PM (priority-ordered)

1. **(P0-1, P0-2 combined)** Restore the slide-13 `<` termination and refit the §5.1 trace to it. Both are the same bug — the chapter changed the algorithm and broke its own example.
2. **(P0-3)** Fix the slide-9 / 4-queens move-set commentary; clarify that the slide-9 board is not in the per-column formulation.
3. **(P0-4)** Fix the §5.7 mutation bit-flip prose ("0→0" is wrong).
4. **(P0-5, P1-5, P1-8)** Pick one completeness/optimality story and propagate to §4.4, §6, §8.1, §8.2.
5. **(P1-6)** Fix the roulette-wheel boundary convention so §5.7 matches slide 42.
6. **(P1-1, P1-3, P1-4, P1-2, P2-6)** Tag every editorial addition with "(not on slides)" so students know what the lecture actually said. This is a single editorial pass and would resolve a significant trust problem.
7. **(P1-9)** Add a real multi-step SA trace with a concrete schedule.

After these are addressed, re-run Reviewer 4 (Round 2).

---

## Report to PM

**Assignment recap:** L05 (Local Search) Round 1 — Reviewer 4 (Exam Readiness, spec §7.1). Imagined 10 exam questions; checked whether `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L05-Local-Search.md` answers them on its own. Read against `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture5-Local Search.pdf` (slides 1–50) for ground truth.

**Status:** FAIL — chapter is not exam-ready.

**Score:** 5/10 exam questions cleanly answerable, 1 borderline, 4 fail.

**P0 findings (must fix):**
1. **P0-1** — Hill-climbing termination silently swapped from `<` (slide 13) to `≤` (chapter §3.3 / §4.1 / §8.2). Justification given is also internally confused.
2. **P0-2** — 8-puzzle slide-5 trace (chapter §5.1) does not work under the chapter's own pseudocode; trace requires a sideways move that `≤` forbids.
3. **P0-3** — Slide-9 4-queens commentary (chapter §5.3) describes the wrong state-space formulation (claims "move within column" for a slide that shows multiple queens per row).
4. **P0-4** — Chapter §5.7 mutation example contains nonsense ("bit 5 flipped, value 0→0"); the bit actually flipped 1→0.
5. **P0-5** — Completeness story is inconsistent between §4.4 table and §6 pitfalls. SA and GA called "complete in the limit" in the table; §6 pitfalls explicitly says don't claim that on the exam.

**P1 findings (will cost marks):**
1. **P1-1** — Cooling-schedule menu (linear/geometric/log + Geman & Geman 1984) is not on the slides, not flagged.
2. **P1-2** — TSP "$\binom{n}{2}$ neighbours" claim invented, not on slides, possibly off by $n$.
3. **P1-3** — R&N empirical "86% / 7 restarts" claim presented as lecture content, not on slides.
4. **P1-4** — "Ridge" listed as a named feature of the slide-15 landscape; slide 15 has only four named features, no ridge.
5. **P1-5** — SA acceptance: $\Delta = 0$ branch labelled "downhill: maybe accept" when it is actually "always accept" ($e^0 = 1$).
6. **P1-6** — Roulette-wheel intervals in §5.7 use half-open $[F_{i-1}, F_i)$ which contradicts the slide-42 answer for $R=7$.
7. **P1-7** — Comparison-table per-step cost "O(b)" is opaque; $b$ is never given problem-specific values.
8. **P1-8** — Cheat-sheet §8.2 inherits the P1-5 mislabel.
9. **P1-9** — No multi-step worked SA example with a concrete schedule.
10. **P1-10** — Why "56 = 8×7, not 64 = 8×8" never explained.

**P2 findings:**
1. **P2-1** — No bibliography for Geman & Geman 1984.
2. **P2-2** — Speculative forward links to L06/L10/L11/L12.
3. **P2-3** — "$8^8 = 16.7$M states" given without specifying the state-space convention.
4. **P2-4** — Glossary "heuristic function (concretised here)" framing unclear.
5. **P2-5** — Prose leans on figures; offline read degrades.
6. **P2-6** — §8.7 "when to use which" GA recommendation is editorial.

**Acceptance criteria (§7.1 of spec — "Can student answer 10 imagined exam questions from chapter alone?"):** **NOT MET.** 4/10 fail outright, 1/10 borderline.

**Concerns / risks:** The chapter consistently mixes lecture content with editorial additions without labelling. This is the deepest problem; the individual P0/P1 items are symptoms. A student using this as their primary study artifact will memorise things the lecture never said and will not memorise things the lecture did say (e.g., the strict-`<` termination). Trust is binary — once the student catches one substitution, they cannot rely on the chapter for anything.

**Out-of-scope observations:**
- The chapter assumes a glossary at `study/_shared/glossary.md` and a cross-references file at `study/_shared/cross-references.md`. I did not validate these.
- Lab 4 references at line 802 assume a `handout_lab_4/` directory exists; not validated.
- Figure paths assume `../extracted_figures/L05/figXX.png` exist; not validated.

**What PM should do next:** Dispatch the engineer who authored L05 to fix the five P0 findings and the ten P1 findings, in priority order above. Then re-dispatch Reviewer 4 for Round 2. Do not advance to Round 2 of other reviewers (e.g., glossary linter, coverage checker) until P0s are resolved — they will be invalidated by the rewrites.

**DOCUMENT.md updated:** N/A for QA.
