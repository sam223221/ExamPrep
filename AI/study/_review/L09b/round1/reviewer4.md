# L09b (HMM) — Round 1 — Reviewer #4 (Exam Readiness)

**Reviewer role:** Lecture Reviewer #4 — Exam Readiness (Spec §7.1)
**Artifact under review:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L09b-HMM.md`
**Source of truth:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture9-Hidden Markov Models.pdf` (slides 1–52)
**Mode:** HARSH. The student gets one shot at this exam — I will not paper over weaknesses.

---

## Part A — 10 Exam Questions on HMMs

These are the questions an exam in this course is most likely to ask, based on the actual slide content. They are graded by what a Bayesian-Inference / NLP-flavoured AI course in this style typically tests. Each question has a *Difficulty* tag, the *Coverage status in the chapter* (Covered / Partially covered / Missing), and a brief justification.

### Q1. Define an HMM by listing its parameters, the two structural assumptions it makes, and explain why it is called "hidden". (Bookwork.)

- **Difficulty:** Easy
- **Coverage status:** Covered. §3.1, §3.3, §8 give the parameter triple $\lambda = (A, B, \pi)$, the Markov + output-independence assumptions, and the slide-22 quote on "hidden".
- **Risk:** Student might forget that the *stationarity* assumption is a third assumption the slides explicitly call out [slide 2]. The chapter mentions it in §3.1 and pitfall #10 but doesn't list it in the "two assumptions" §8 box. If the exam asks for "the assumptions" plural-open, only naming Markov + output-independence is incomplete.

### Q2. Write the joint $P(O, Q \mid \lambda)$ for an HMM in factored form, and state which assumption justifies each product. (Bookwork with derivation flavour.)

- **Difficulty:** Easy–Medium
- **Coverage status:** Covered. §4.1 / §8 give the factorisation. Pitfall #7 makes the assumption-attribution explicit (Markov for transitions, output-independence for emissions).
- **Risk:** None — the chapter handles this well.

### Q3. Given the ice-cream HMM ($\pi_C=0.2, \pi_H=0.8$; $a_{CC}=0.6, a_{CH}=0.4, a_{HC}=0.3, a_{HH}=0.7$; $b_H=(0.2,0.4,0.4), b_C=(0.5,0.4,0.1)$) and observation sequence $O = 3, 1, 3$, run the forward algorithm and report $\alpha_t(j)$ for all $t \in \{1,2,3\}$ and $j \in \{H, C\}$ and the final $P(O \mid \lambda)$. (Computation.)

- **Difficulty:** Medium
- **Coverage status:** Covered. §5.4 walks through this exact computation end-to-end with all intermediates.
- **Risk:** The chapter's worked numbers are correct, but the student must memorise the ice-cream constants (§8 says so explicitly). HARSH NOTE: the chapter never asks the student to do a forward pass on a *different* observation sequence (e.g. $O = 2, 3, 1$) to test transfer of the method. If the exam swaps the observations, a student who only memorised $0.0263$ as "the answer" is sunk.

### Q4. Same HMM as Q3. Run Viterbi on $O = 3, 1, 3$ and produce the most-likely state sequence $Q^*$, the probability $P^*$ of that sequence, AND the back-pointer table. Then explain in one sentence what makes Viterbi's output differ from forward's output. (Computation + concept.)

- **Difficulty:** Medium
- **Coverage status:** Covered. §5.5 and §4.4 nail the algorithm, the result HHH with $P^* = 0.012544$, and the sum-vs-max contrast.
- **Risk:** The chapter's Viterbi worked example only includes back-pointers narratively, not as an explicit table. A student under exam pressure may forget to tabulate $bt_t(j)$ for every (t, j) — especially the back-pointer values that DIDN'T end up on the winning path. The pitfall list #8 flags this but doesn't drill it.

### Q5. State the time and space complexity of (a) brute-force enumeration of state sequences, (b) the forward algorithm, (c) the Viterbi algorithm. Explain in one sentence WHY forward and Viterbi achieve the polynomial bound. (Concept + analysis.)

- **Difficulty:** Easy–Medium
- **Coverage status:** Covered. §4.2 ($O(N^2 T)$ forward), §4.3 ($O(N^2 T)$ Viterbi), §4.1 ($O(N^T)$ brute force), §4.4 comparison table, pitfall #6.
- **Risk:** The chapter is solid here, but a HARSH question might ask "*Why* is it $N^2 T$ and not $N T$?" — the chapter says "each cell requires summing over $N$ predecessors" but doesn't push the student to derive it from first principles. Adequate but not airtight.

### Q6. Given the weather Markov chain (slide 13 numbers, $\pi=[0.5, 0.3, 0.2]$ for (H, C, W); $a_{HH}=0.5, a_{HC}=0.2, a_{HW}=0.3, a_{CH}=0.2, a_{CC}=0.5, a_{CW}=0.3, a_{WH}=0.3, a_{WC}=0.1, a_{WW}=0.6$), compute (a) $P(\text{H,H,H,H})$, (b) $P(\text{C,H,C,H})$, (c) interpret the ratio in terms of what the model "thinks" about weather. (Computation + interpretation.)

- **Difficulty:** Easy
- **Coverage status:** Covered. §5.1 does parts (a) and (b) and the interpretation.
- **Risk:** Acceptable. Note however the chapter's §5.1 transitions only include H↔C and H↔W in the figure caption — the WARM↔COLD self-loops/cross-arcs are partly stated as $a_{WC} = 0.1, a_{WW} = 0.6, a_{WH} = 0.3$. Slide 13's actual diagram shows the cross-transitions but the chapter's verbal listing in §3.2 Figure 3.2 caption lists "HOT→COLD .2, HOT→WARM .3, COLD→HOT .2, COLD→WARM .3, WARM→COLD .1, WARM→HOT .3" — but does NOT list a COLD→COLD self-loop value, instead writing "Self-loops are .5 (HOT), .5 (COLD), .6 (WARM)". So the student can reconstruct the row-stochastic matrix, but only if they remember to add the self-loops separately. HARSH: this is fragile.

### Q7. Distinguish "filtering", "smoothing", "decoding", and "prediction" in the standard HMM terminology, and say which (if any) the slides cover. Which of the three lecture-slide names (Evaluation / Decoding / Learning) does each textbook task map to? (Concept / terminology — common exam trap.)

- **Difficulty:** Medium
- **Coverage status:** Partially covered. §3.5 has the naming-note callout and pitfall #1 flags this. BUT "prediction" ($P(q_{t+k} \mid o_1 \ldots o_t)$ for $k > 0$) is never named. A real exam in this course or its textbook (Jurafsky & Martin / Russell & Norvig) regularly asks the four-way distinction (filtering, smoothing, prediction, most-likely-explanation). If the exam includes "prediction" the student is in unknown territory.
- **Risk:** HIGH. This is a textbook-style exam question and the chapter is missing one of the four standard names.

### Q8. The Fair Bet Casino: state $\Sigma$, $Q$, the transition matrix $A$, the emission matrix $B$. Given the observed sequence $o = 0,1,0,1,1,1,0,1,0,0,1$ and hypothesised hidden path $q = F,F,F,B,B,B,B,B,F,F,F$, compute $\log P(o, q \mid \lambda)$ assuming $\pi_F = \pi_B = 0.5$. (Computation.)

- **Difficulty:** Medium
- **Coverage status:** Covered. §3.4 and §5.2 give the parameters and the table of factors. The chapter does NOT actually multiply out the joint (it says "the joint probability of this observation+path is the product of all the entries in those two columns") — it leaves the arithmetic to the student. That's pedagogically fine but if the exam asks for a numerical answer the student has to be confident enough to grind through 11 factors.
- **Risk:** Medium. The chapter could have done the final multiply once to anchor the student.

### Q9. Define the forward variable $\alpha_t(j)$ in words AND in probability notation. Then derive the recursion $\alpha_t(j) = \sum_i \alpha_{t-1}(i) a_{ij} b_j(o_t)$ from the definition, citing which HMM assumption justifies each step. (Derivation — most demanding question type.)

- **Difficulty:** Hard
- **Coverage status:** Partially covered. §4.2 gives the definition and the recursion verbatim but does NOT actually derive the recursion from the definition — it says "Why the definition has that exact shape. It is the joint with the future not yet integrated, marginalised over all earlier hidden states." That's a hand-wave, not a derivation. A rigorous derivation would: (i) start from $\alpha_t(j) = P(o_1, \ldots, o_t, q_t = j)$, (ii) condition on $q_{t-1}$, (iii) sum over $q_{t-1}$, (iv) apply Markov to separate $P(q_t \mid q_{t-1})$, (v) apply output-independence to separate $P(o_t \mid q_t)$, (vi) recognise the inner factor as $\alpha_{t-1}(q_{t-1})$.
- **Risk:** HIGH if the exam is derivation-style. The student will mimic the recursion but not be able to *explain* it.

### Q10. Suppose you receive an HMM and an observation sequence and are asked "what is the probability that the hidden state at time $t = 5$ is HOT, given observations $o_1, \ldots, o_{10}$?". Name the task in standard terminology, name the algorithm(s) required, and identify which (if any) of those algorithms the lecture taught. (Concept / synthesis.)

- **Difficulty:** Hard
- **Coverage status:** Partially covered. The chapter flags this in §3.5 ("If it says 'smoothing', flag that the lecture didn't cover it and you would need a backward pass") and pitfall #1. BUT nowhere does the chapter actually state that the answer requires forward × backward (the forward-backward algorithm). A student reading the chapter learns the *name* "smoothing" and learns that it's "the lecture-uncovered backward pass" but doesn't learn that the smoothed posterior is computed as $P(q_t \mid O) \propto \alpha_t(q_t) \beta_t(q_t)$ where $\beta_t$ is the backward variable.
- **Risk:** HIGH. If the exam asks "how would you compute the smoothed posterior?" the student can name the task but not sketch the method. The chapter takes the position "Lab 8 doesn't require it, don't worry about it" — that's risky for an exam.

---

## Part B — Coverage Summary Per Question

| # | Topic | Chapter coverage | Verdict |
|---|---|---|---|
| Q1 | HMM definition + assumptions + "why hidden" | §3.1, §3.3, §8 | OK; stationarity is buried |
| Q2 | Joint factorisation | §4.1, §8 | OK |
| Q3 | Forward pass numerical | §5.4 | OK (but only ONE worked example) |
| Q4 | Viterbi numerical + concept | §5.5, §4.4 | OK (back-pointer table is implicit, not tabulated) |
| Q5 | Complexity | §4.2, §4.3, §4.4, pitfall #6 | OK |
| Q6 | Markov chain numerical | §5.1 | OK but transition matrix is fragmented |
| Q7 | 4-way terminology (filtering/smoothing/prediction/decoding) | §3.5, pitfall #1 | **Prediction not named — gap** |
| Q8 | Fair Bet Casino joint | §3.4, §5.2 | OK but final multiply omitted |
| Q9 | Derive forward recursion from definition | §4.2 — hand-waved | **No real derivation — gap** |
| Q10 | Smoothing task naming + method | §3.5, pitfall #1 | **Task named, method (forward-backward) not stated — gap** |

**Quick tally:** 6 of 10 exam-likely questions are well-supported. 4 of 10 have material gaps the student would feel in an exam.

---

## Part C — Harsh Findings (severity-tagged)

### P0 — Exam-Blocking

None. The chapter is competent. A student who reads it carefully will pass this lecture's questions on a typical exam. No question is *unanswerable* from the chapter; the gaps are about depth and breadth, not correctness.

### P1 — Important Gaps

1. **Forward-backward / smoothing method is named but not described.** §3.5 + pitfall #1 say "smoothing needs a backward pass we didn't cover". A serious exam-prep chapter should at minimum sketch the backward variable $\beta_t(j) = P(o_{t+1}, \ldots, o_T \mid q_t = j, \lambda)$ and the formula $P(q_t = j \mid O) \propto \alpha_t(j) \beta_t(j)$, even as a single-paragraph "for reference, smoothing combines these as follows". The chapter chooses to punt. If the exam asks even a *conceptual* "how would you compute…" question, the student has nothing to say beyond "it's a backward pass". **Fix:** add a §4.x callout box with the backward recursion in three lines and the smoothing-formula.

2. **No derivation of the forward recursion from the definition of $\alpha_t(j)$.** §4.2 states the recursion and gives the "reading the recursion as a sentence" English version, which is good for intuition but useless for a derivation-style exam question. Pitfall #7 flags that "the HMM uses both assumptions" — but the chapter never *uses* both assumptions in a derivation. **Fix:** add a 6-step derivation under §4.2 ("Where the recursion comes from") that explicitly invokes Markov at step (iv) and output-independence at step (v).

3. **Only ONE worked observation sequence ($O = 3, 1, 3$) for both forward and Viterbi.** Pedagogically this is anaemic. Lab 8's exam variants (chapter §7 mentions them) test *different* observation sequences and *different* transition matrices. A student who only saw $3,1,3$ twice has muscle-memory for that exact trellis but no fluency. **Fix:** add at least one additional worked sequence (e.g., $O = 1, 1, 3$ or $O = 2, 3, 2$) in §5.4 / §5.5 OR an end-of-section "try this yourself" with answer.

4. **"Prediction" is never named.** §3.5's naming-note covers filtering, smoothing, decoding, MLE — but standard 4-way HMM-task taxonomy includes *prediction* ($P(q_{t+k} \mid o_{1:t})$). If the exam asks the full taxonomy, the student is missing a quarter of it. **Fix:** add "prediction" as a fourth bullet in the §3.5 naming-note.

5. **Stationarity assumption is buried.** The chapter lists "Markov + output-independence" as "the two assumptions" in the §8 cheat sheet, but slide 2 explicitly lists *three* (priors + transitions + emissions) plus stationarity. Pitfall #10 mentions stationarity but it never makes the §8 summary. A student writing "the HMM makes two assumptions" loses a mark when the right answer is three. **Fix:** rename §8's "Two assumptions" to "Three assumptions" and add stationarity as a third bullet.

6. **Back-pointer table in Viterbi is implicit, never tabulated.** §5.5 says "Back-pointer: $bt_2(\text{HOT}) = \text{HOT}$" inline but never draws the full $bt$ table. A student under exam pressure may forget to record back-pointers for *both* states at every time step. Pitfall #8 flags the concept but doesn't drill the practice. **Fix:** add a 2×3 back-pointer table alongside the Viterbi values table in §5.5.

### P2 — Polish

7. **Slide-13 weather transition matrix is fragmented.** §3.2 Figure 3.2 caption lists cross-transitions but the self-loops are mentioned as a separate sentence. Tabulate it as a clean 3×3 matrix once for easy reference. The student should be able to copy a row-stochastic A in 5 seconds, not reconstruct it from prose.

8. **The Fair Bet Casino joint is never multiplied out.** §5.2 builds the table of 11 factors and stops. Finish the arithmetic once so the student has a concrete answer to compare against. (Even an approximation like "$\approx 1.5 \times 10^{-7}$" would anchor.)

9. **No mention that $\pi$ and the $a_{0j}$ "start state" representation are equivalent.** Slide 11 says "instead of start state" + "special initial probability vector". The chapter uses both ($\pi$ in §3.2 and $q_0$ in §3.3 Figure 3.3 table) without explicitly stating the equivalence. A student might wonder if they're two different things. Add one sentence.

10. **The "operator-swap" claim deserves a tighter proof sketch.** §4.4 says "two algorithms, one trellis structure, one operator-swap apart". True. But why is max-plus-product the right operator for argmax and sum-product the right operator for marginalising? The semiring connection (max-product semiring vs sum-product semiring) is one sentence. It elevates "they look similar" to "they're instances of the same generic DP". Optional polish.

11. **Log-space underflow is a footnote but should be elevated.** Pitfall #11 says "the exam may not test this directly, but Lab 8's implementation may". Lab 8 *will* test it. A student who implements Viterbi in raw probability for $T = 50$ will get all zeros. The chapter should have a §4.x callout: "In practice work in log-space; the recursion becomes $\log v_t(j) = \max_i [\log v_{t-1}(i) + \log a_{ij} + \log b_j(o_t)]$".

12. **No mention of how ties are broken in Viterbi argmax.** If two predecessor states give exactly the same product, the back-pointer is ambiguous. Real implementations break ties (lower index, or first-seen). Minor but a HARSH grader might ask.

---

## Part D — Concerns Beyond the Question Set

- **The chapter doesn't connect Viterbi to log-likelihood scoring of *test* sequences in tagging tasks.** POS tagging is mentioned in §1 as motivation but never re-visited with a concrete tagging example. If the exam asks "given a trained HMM for POS tagging and a sentence, what is the tag sequence?" the student has the Viterbi algorithm but no concrete tagging-style example to anchor on. The ice-cream example is doing all the heavy lifting.

- **Baum–Welch / Problem 3 is hand-waved.** §4.5 says "the lecture does not require you to derive it". Fine. But the exam *may* ask "name the algorithm used to estimate HMM parameters from unlabelled observations" or "is HMM training supervised or unsupervised?" The chapter says EM/Baum–Welch but doesn't drill *supervised vs unsupervised*. The answer is "unsupervised" (we only see observations, not states) — but a student who misses this distinction loses easy marks.

- **No discussion of when an HMM is the WRONG model.** When does the Markov assumption break? When does output-independence break? Real exam questions sometimes ask "given this scenario, is an HMM appropriate?" The chapter touches on this in the §2.1 "where the analogy breaks down" but never frames it as a modelling-choice question.

- **The chapter never asks the student to identify $a_{ij}$ from a transition diagram.** All slides show transition diagrams (slides 7, 12, 13, 28). A common exam style is "read off $a_{HC}$ from this diagram" — the chapter teaches the algorithms but not the diagram-reading skill.

---

## Part E — What I'd Tell the PM

**Status: Pass with concerns.** This is a solid, exam-readable chapter. A student who reads it will not fail the HMM portion of the exam. But the chapter currently optimises for "explain the lecture" rather than "exam-proof the student". The four P1 gaps (forward-backward / derivation / single-example fluency / 4-way taxonomy) are all places where a harsh exam will catch a student who only read this chapter.

**Recommended fixes before final lock-down:**

1. Add a 1-paragraph backward-variable + smoothing callout in §4.x (addresses Q10 + pitfall #1 gap).
2. Add a real derivation of the forward recursion (6 lines) — addresses Q9.
3. Add at least ONE additional worked numerical example (different $O$ or different $A$) — addresses Q3/Q4 fluency gap.
4. Add "prediction" to the §3.5 naming-note — addresses Q7 gap.
5. Promote stationarity to a third assumption in the §8 cheat sheet — closes Q1's stationarity ambiguity.
6. Add a tabulated $bt$ back-pointer matrix in §5.5 — addresses Q4 polish.

If you only have time for ONE: do #1 (backward / smoothing). That's the most likely "I didn't see this coming" exam moment.

---

## Report to PM

**Assignment recap:** Lecture Reviewer #4 (Exam Readiness) for L09b (HMM), Round 1. Produced 10 exam questions per Spec §7.1, mapped to chapter coverage, and graded gaps.

**Status:** Pass with concerns.

**P0 findings:** None.

**P1 findings:**
1. Forward-backward / smoothing method is named but not described — chapter punts on the backward variable. (§3.5, pitfall #1)
2. Forward recursion is stated but never derived from the definition of $\alpha_t(j)$. (§4.2)
3. Only one worked observation sequence ($3,1,3$) exists for both forward and Viterbi — no transfer practice. (§5.4, §5.5)
4. "Prediction" is missing from the 4-way HMM-task taxonomy. (§3.5)
5. Stationarity assumption is buried in pitfalls instead of the §8 assumptions list.
6. Viterbi back-pointer table is narrated inline, never tabulated.

**P2 findings:**
7. Weather transition matrix in §3.2 is fragmented (self-loops in prose, cross-arcs in caption).
8. Fair Bet Casino joint never multiplied out in §5.2.
9. Equivalence of start-state and $\pi$ representations is not stated.
10. Operator-swap claim in §4.4 could be tightened with semiring framing (optional).
11. Log-space underflow flagged in pitfalls but not elevated — Lab 8 will hit this.
12. Tie-breaking in Viterbi argmax is unspecified.

**QA Checklist (§7) status:** N/A — this is a study-chapter review, not a software feature.

**Acceptance criteria (§1) status:** Met. 10 exam questions delivered, mapped to chapter coverage, with severity-tagged findings.

**DOCUMENT.md audit:** N/A for study-chapter review.

**Out-of-scope observations:**
- POS tagging is motivated in §1 but never reused as a concrete worked example. The ice-cream toy is doing 100% of the work — a student may struggle to map from ice cream to a "real" NLP task without help.
- Baum–Welch supervised-vs-unsupervised distinction is missing. Easy mark to lose.
- Diagram-reading skill (extract $a_{ij}$ from a state diagram) is never directly practised; only matrix-reading is.

**Concerns / risks:**
- The chapter optimises for explaining the lecture, not exam-proofing the student. The four P1 content gaps (smoothing method / derivation / single-example fluency / 4-way taxonomy) are the exam-day risks.
- Numerical fluency on ONE sequence ($3,1,3$) is not the same as fluency. If the exam swaps in $O = 2, 3, 2$ the student will be slow.
- If the exam is derivation-style rather than computation-style, Q9 is a real risk.

**What PM should do next:**
- Dispatch a follow-up engineer to add: (a) backward / smoothing callout, (b) forward-recursion derivation, (c) one additional worked numerical example, (d) "prediction" in §3.5, (e) stationarity in §8, (f) tabulated back-pointer matrix.
- Then re-QA against this finding list.
- The chapter is shippable as-is for a low-stakes review; for an actual final-exam-prep artefact, push the six P1 fixes first.

**DOCUMENT.md updated:** N/A for QA.
