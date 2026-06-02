# L09b — Round 1 Reviewer 1: Concept Completeness (incl. Figures)

**Spec section:** §7.1
**Reviewer role:** Concept Completeness, with audit of figures and slide coverage. Special focus on the non-standard "Evaluation/Decoding/Learning" naming.
**Artifacts reviewed:**
- Source PDF: `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture9-Hidden Markov Models.pdf`
- Chapter: `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L09b-HMM.md`
- Figure catalogue: `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\extracted_figures\L09b\figures.md`
- Verified slides (visually): 3, 4, 5, 7, 8, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 25, 28, 29, 30, 32, 33, 34, 37, 38, 41, 46, 47, 48, 49, 50, 51

---

## VERDICT

**Status: PASS WITH CONCERNS (Conditional)**

The chapter is strong on the core HMM definitions, the two algorithms (forward and Viterbi), the worked numerical examples on the ice-cream HMM, and the lecture-vs-textbook naming reconciliation that the brief explicitly called out. All numerical values in the worked examples were independently verified against the corresponding source slides and are correct. The Markov-chain weather example, the Fair Bet Casino example, and the ice-cream HMM example all reproduce slide numbers exactly (including the .5/.5/.6 self-loops, the .9/.1/.1/.9 casino matrix, and the .7/.3/.4/.6 ice-cream transitions). The pseudocode for both FORWARD and VITERBI matches slides 41 and 49 character-for-character. The two assumptions are stated correctly.

However, the chapter has a cluster of **broken cross-references to L09a/L02** (P1) and one **content-bearing figure that is missing from §3.4** (P1). There is also one potentially **misleading framing in §3.5** where Problem 1 (slide name: Evaluation) is glossed as "Filtering" in the table header — the chapter's own naming note later concedes this is sloppy, but the header still says it. A reader who skims the table will absorb the wrong equivalence.

None of these are P0 (no mathematical or conceptual errors; no misrepresented slide content; nothing is wrong-and-uncorrectable). The chapter is shippable after one editing pass on cross-references and the §3.5 table header.

---

## P0 — Broken / wrong / shipping blockers

*(none)*

---

## P1 — Important issues

### P1-1. Broken §-anchors on cross-references to L09a and L02

The chapter's "Connections" section and inline "[see L09a §X]" callouts point to section numbers that do not exist or have moved in the linked chapters.

- **Chapter line 45:** `[see L09a §3.7](L09a-Bayesian-Networks.md#37-inference-by-enumeration)` — L09a §3.7 is **"Bayesian network — definition"**, not "Inference by enumeration". The correct section in L09a is **§3.13** (`L09a-Bayesian-Networks.md#313-inference-by-enumeration-exact-inference`).
- **Chapter line 148** (glossary cross-link in §3.2): `([see L09a §3.6](L09a-Bayesian-Networks.md#36-markov-condition))` — L09a §3.6 is **"Conditional independence"**, not "Markov condition". The Markov condition is L09a **§3.9** (`L09a-Bayesian-Networks.md#39-the-markov-condition-aka-d-separation-informal-version`).
- **Chapter line 621** (§7): `[L09a §3.1 — conditional probability](L09a-Bayesian-Networks.md#31-conditional-probability)` — L09a §3.1 is **"Random variables and events"**. Conditional probability is L09a **§3.3**.
- **Chapter line 622** (§7): `[L09a §3.6 — Markov condition](L09a-Bayesian-Networks.md#36-markov-condition)` — again, this should be **§3.9**.
- **Chapter line 625** (§7): `[L02 §3.7 — environment taxonomy](L02-Agents.md#37-environment-types)` — L02 §3.7 is **"Hierarchy of agent types"**. The environment taxonomy is L02 **§3.6**.

These are factual errors in the connections to other lectures and undermine the navigation promise the chapter makes to the reader.

**Suggested fix:** Re-anchor every `L09a §X` and `L02 §X` reference using the actual table-of-contents headings in those files. Both files have stable §-numbering; a five-minute editing pass fixes all five.

### P1-2. §3.5 table headline conflates two distinct concepts (Evaluation ≠ Filtering)

In the §3.5 table (chapter lines ~220-224), the row for Problem 1 reads:

> **Problem 1 — Evaluation** | **Filtering** (also: likelihood evaluation)

The slide-named "Evaluation" computes $P(O \mid \lambda)$ — the **total likelihood of an observation sequence**, a scalar. The textbook concept **"filtering"** is the *posterior over the current hidden state*, $P(q_t \mid o_1, \ldots, o_t)$ — a probability **distribution over states**, one per time step. These are not the same object. They share the forward recursion but normalise differently.

The chapter's own naming note (lines 226-232) correctly explains this: "*Filtering* strictly means computing $P(q_t \mid o_1 \ldots o_t)$… Our glossary uses this stricter sense, while the slides call the *forward-algorithm probability* $P(O \mid \lambda)$ 'filtering'." But a reader who looks at the headline table absorbs **"Evaluation = Filtering"** as the bottom-line takeaway, then has to un-learn it three lines later.

Compounding this: the **lecture itself does NOT use the word "filtering"** for Problem 1 anywhere I could find in the slides. Slide 29 only says "Evaluation". The chapter introduces "filtering" as a textbook synonym, but the equivalence is at best partial. A neutral, less-confusing header would be **"Likelihood / observation-sequence probability"** for the standard-name column, with the filtering distinction relegated entirely to the naming note.

**Suggested fix:** Change the Problem 1 standard-name cell to "Likelihood evaluation (forward algorithm output $P(O \mid \lambda)$); related to but not identical to *filtering*." Then keep the existing naming note as-is for the deeper explanation.

### P1-3. Missing Fair Bet Casino HMM diagram (slide 23)

Slide 23 contains a hand-drawn FSA diagram of the Fair Bet Casino HMM showing the two state nodes (F, B), the self-loops (9/10), the cross-edges (1/10), and the four emission edges to H/T leaves with their probabilities (½, ½, ¾, ¼). The figure catalogue marks `page23-render.png` as **USE** with the rationale "Embedded in §5.2". The chapter §3.4 (Fair Bet Casino walkthrough) embeds only slide 19 (the prose setup) — not the visual model. The numerical A and B matrices are in the §3.4 prose, but the lecture's actual FSA diagram is not embedded anywhere in the chapter.

This is the only place I found where the catalogue's USE verdict is not honoured AND the missing figure carries unique visual content (an FSA topology that prose cannot replace). The Fair Bet Casino diagram and the ice-cream HMM diagram (slide 28, properly embedded) are the two big-picture pictures of "what an HMM looks like as a state machine" in the entire lecture. Skipping one of them costs the chapter a chunk of its motivational scaffolding.

**Suggested fix:** Embed `../extracted_figures/L09b/page23-render.png` in §3.4 right after the numeric A and B matrices, with a caption pointing out the analogous diagram to the ice-cream HMM in §3.3.

### P1-4. §5.3 introduces a state-numbering convention that contradicts §3.3 without flagging it

Chapter §3.3 embeds slide 28 (the ice-cream HMM diagram) which **labels HOT as state 1 and COLD as state 2** ("HOT₁", "COLD₂" in the slide art). The figure caption in §3.3 (line 198) says "Two hidden states (HOT, COLD)" in that order. Reader's natural takeaway after §3.3: state 1 = HOT, state 2 = COLD.

But chapter §5.3 (line 462) abruptly inverts this:

> States: Q = {HOT, COLD}, labelled q₁ = COLD and q₂ = HOT in the trellis convention. (The lecture's trellis numbers states with COLD as q₁ and HOT as q₂…)

And then chapter §5.3 builds the A matrix with COLD as row 1:

$$A = \begin{pmatrix} a_{CC} & a_{CH} \\ a_{HC} & a_{HH} \end{pmatrix} = \begin{pmatrix} 0.6 & 0.4 \\ 0.3 & 0.7 \end{pmatrix}.$$

The chapter is **correct about the slide-internal inconsistency** — slide 28 does say HOT=1 and slide 38 (trellis) does say q₂=HOT, q₁=COLD. But a reader walking from §3.3 → §5.4 may carry the wrong mental indexing and miscompute the worked example. The discrepancy deserves a more prominent flag, not just a parenthetical remark, because if the reader had already started constructing a matrix with HOT as state 1, the entire §5.4 arithmetic will look like it has reversed indices.

**Suggested fix:** Add a one-sentence callout box in §5.3 before the A matrix: *"⚠️ Indexing flip: slide 28 draws HOT as state 1 and COLD as state 2, but the lecture's own trellis (slide 38) inverts this. The §5.4 worked example below follows the trellis convention (q₁=COLD, q₂=HOT). If you tabulate with the slide-28 ordering, your $\alpha$ values will look right per cell but your matrix columns will appear swapped from what slide 38 shows."*

### P1-5. Notation: chapter uses λ = (A, B, π) but slide 29 uses Φ = (A, B)

Chapter §3.3 line 171 introduces "$\lambda = (A, B, \pi)$" as the compact notation, and uses $\lambda$ throughout. Slide 29 (the Three Basic Problems slide, embedded as referenced in §3.5) actually writes the model parameters as **Φ = (A, B)**. The chapter does not mention this notational divergence anywhere.

Two issues:
1. The lecture uses Φ = (A, B) in slide 29 but λ = (A, B) in slide 30 — so the lecture itself is inconsistent. The chapter silently picks λ.
2. The lecture uses (A, B) (no π) in the model tuple, while the chapter uses (A, B, π). This is the conventional textbook form, but it deviates from the slide notation — and the chapter does not flag the deviation.

This is a P1 because an exam question may copy the slide's Φ notation, and a reader who has only seen λ may briefly stall.

**Suggested fix:** In §3.3 line 171, add: *"Caveat: slide 29 writes the parameters as Φ = (A, B), suppressing π. We retain π in the tuple (standard textbook convention) and use λ throughout this chapter. Treat λ, Φ, (A, B, π), and (A, B) as the same model for exam purposes."*

---

## P2 — Polish / suggestions

### P2-1. Catalogue claims 32–36 figures as USE; chapter embeds only 17

The figure catalogue at `figures.md` marks 36 slides as USE (slides 5, 7, 9, 10, 11, 13, 14, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 44, 45, 47, 48, 49, 50, 51). The chapter actually embeds 17 (`grep` confirms: slides 5, 7, 13, 14, 17, 19, 28, 32, 33, 37, 38, 41, 47, 48, 49, 50, 51). The "Coverage summary" at the bottom of `figures.md` further claims "32 embedded as USE (including 3 figure-pairs…)" — neither number matches the 17 actually embedded.

The catalogue's coverage summary is wrong by a factor of ~2x. Most of the unembedded USE figures are slides whose content is text-only (e.g., slide 9 is the formal Q/A definition; slide 10 is the Markov assumption formula; slide 18 is the HMM Assumptions formulas) and the chapter has correctly reproduced them as prose. So the **chapter is fine**; the catalogue is the document that is misleading.

**Suggested fix:** Reconcile `figures.md`'s coverage summary with the actual embedded count, OR demote the text-only USE entries to SKIP (with a "reproduced as prose" rationale) so that USE actually means "image embedded in the chapter". Slide 23 (the Fair Bet Casino FSA diagram) is the one true USE-but-missing — see P1-3.

### P2-2. §1's Lab 8 forward-ref to handout uses a relative path that may fail in the rendered HTML

Line 629: `[handout \`Lab 8/handout/Lab 8.pdf\`](../../Lab%208/handout/Lab%208.pdf)`. The double-`../` assumes the chapter lives at `study/lectures/L09b-HMM.md` and the lab at `Lab 8/handout/`. If the rendered docs flatten directory structure, this link breaks. Low impact (paper handout, not exam-critical), so P2.

### P2-3. §3.5 "Naming note for the exam" speculates about "smoothing" but doesn't define it well

Chapter line 229: *"Smoothing means computing $P(q_t \mid o_1 \ldots o_T)$ — the posterior using all observations, including the ones after $t$. This needs a backward pass that the lecture does not teach."* Good. But two paragraphs earlier the table row for Problem 2 says "Decoding | Most-likely state sequence (also: Viterbi decoding; closely related to *smoothing* which gives marginal posteriors at each time)". That parenthetical "closely related to smoothing" is inaccurate — Viterbi (single-best-path argmax) and smoothing (per-time-step marginal posterior) are NOT closely related, they answer different questions. A student following the breadcrumb will conflate them.

**Suggested fix:** Drop "(also: Viterbi decoding; closely related to *smoothing* which gives marginal posteriors at each time)" or rephrase to "*not* the same as smoothing, which gives marginal posteriors instead of the joint argmax".

### P2-4. §3.5 table column "Algorithm" omits the operator difference

The table at §3.5 lists the algorithm but doesn't reinforce the §2.5 / §4.4 punchline that Problem 1 uses $\sum$ and Problem 2 uses $\max$. Adding a fourth column "Operator" with "$\sum$" / "$\max$" / "EM" would let a student answer "which operator does each problem use" without scrolling.

### P2-5. §6 pitfall 9 is correct but mid-stated

Pitfall 9 says: *"For B, the rows correspond to the state and the columns to the observation vocabulary; row j of B (b_j(v_1), b_j(v_2), …) must sum to 1."* True, but the lecture's slide 17 actually writes $B = b_j(o_t)$ — i.e., as a function, not as a matrix with rows-and-columns. A student who memorises the pitfall in matrix form might get confused if the exam writes B as a function. Minor; consider mentioning both forms.

### P2-6. §6 pitfall 4 is the right warning but the example would help

Pitfall 4 warns about $a_{ij}$ vs $a_{ji}$ orientation. A one-line example would cement it: *"In our ice-cream HMM, $a_{HC} = 0.3$ (HOT→COLD), $a_{CH} = 0.4$ (COLD→HOT). They are different."*

### P2-7. §2.4 GPS analogy says "highest-probability final cell" — minor

"At the end you find the highest-probability final cell and follow back-pointers". The slide actually uses $q_T^* = \arg\max v_T(i)$ — i.e., highest-probability cell at *time T*, not "final" in the path-traversal sense. The chapter does state this correctly in §4.3 formal recursion; the §2.4 prose is fine but could say "highest-probability cell at the last time step T" for absolute clarity.

### P2-8. §5.5 ratio interpretation is correct but rounds awkwardly

Chapter line 577: "Their ratio is $0.012544 / 0.026264 \approx 0.478$, meaning the most-likely sequence (HHH) accounts for about 48% of the total observation probability." The number is correct (I verified). Minor: spell out that "the rest is distributed across the other 7 state sequences" — it slightly demystifies what "48%" means in context.

### P2-9. §3.4 Fair Bet Casino mentions "the switch happens with probability 0.1 per flip" but doesn't reconcile with slide 20

Slide 20 reads "The crooked dealer chages between Fair and Biased coins with probability 10%" (sic — typo in slide). The chapter says "with probability 0.1 per flip". Per-flip is the standard interpretation but slide 20 doesn't say "per flip" — it says "10%". The chapter's interpretation IS correct (A_FF=0.9 → a_FB=0.1 means 10% switch chance per step), but a careful reader might notice the chapter is sharpening the slide. Not wrong, just worth flagging.

### P2-10. §5.2 introduces π_F = ½ without source attribution

Chapter line 436: "$\pi_F = \tfrac{1}{2}$ (assuming uniform prior)". The slide 25 table indeed shows the first transition probability as ½, which justifies this — but the chapter calls it an assumption ("uniform prior") rather than a slide value. Mild — the reader can verify against slide 25, which IS the cited source.

---

## EVIDENCE — slide-by-slide spot checks

| Slide | Content | Chapter location | Verified |
|---|---|---|---|
| 2 | HMM = priors + transition + observation; stationarity | §1 (line 21), §3.1 (line 109) | ✓ quoted verbatim |
| 5 | Noisy Channel Ŵ = argmax P(O\|W)P(W) | §1 line 29-31 | ✓ math matches |
| 7 | Weather Markov chain (Start, HOT₁, COLD₂, WARM₃, End) | §3.2 figure 3.1 | ✓ |
| 13 | Specific weather example π=[.5,.3,.2] | §3.2 figure 3.2 | ✓ all numbers verified |
| 14 | P(WARM⁴) = π₃·a₃₃³ = 0.0432 | §5.1 line 418 + figure 5.1 | ✓ 0.2 × 0.216 = 0.0432 |
| 15 | Discussion: HHHH vs CHCH | §5.1 lines 423-426 | ✓ computed 0.0625 vs 0.0024 |
| 17 | HMM parameter table Q/A/O/B/q₀,q_F | §3.3 figure 3.3 | ✓ verbatim transcription |
| 18 | Markov + output-independence assumptions | §3.3 line 188-191, §6 pitfall 7 | ✓ formulas match |
| 19 | Fair Bet Casino narrative | §3.4 figure 3.5 | ✓ |
| 20 | Fair Bet Casino formal: P(H\|F)=½, P(H\|B)=¾, 10% switch | §3.4 line 202-204 | ✓ |
| 21 | P(o\|fair) = (½)ⁿ, P(o\|biased) = 3ᵏ/4ⁿ | §5.2 lines 452-454 | ✓ |
| 22 | "Why hidden?" — Σ, Q definitions | §3.3 line 174-185 | ✓ quoted verbatim |
| 23 | Fair Bet Casino HMM diagram (FSA) | **NOT embedded** (P1-3) | ✗ |
| 25 | Hidden Paths: q=FFFBBBBBFFF, o=01011101001 | §5.2 lines 432-447 | ✓ row-by-row table matches |
| 28 | Ice cream HMM diagram | §3.3 figure 3.4 | ✓ all 8 numbers verified |
| 29 | Three Basic Problems (Eval/Decod/Learn) | §3.5 table line 220-224 | ⚠ table header conflates Eval with Filtering (P1-2) |
| 32 | P(O\|Q) = ∏P(o\|q): .4×.2×.1 | §4.1 figure 4.1 | ✓ |
| 33 | P(O,Q) joint = .8·.7·.3·.4·.2·.1 | §4.1 figure 4.2 + caption math | ✓ |
| 34 | Σ_Q P(O,Q): brute force is O(N^T) | §4.1 line 261-266 | ✓ |
| 35 | Forward = DP, O(N²T) | §4.2 line 271 onwards | ✓ |
| 36 | α_t(j) = P(o_1..o_t, q_t = j \| λ) | §4.2 line 276-278 | ✓ |
| 37 | Forward recursion (Init/Recurse/Term) | §4.2 figure 4.3 + formulas | ✓ |
| 38 | Forward trellis on 3 1 3: α₁(H)=.32, α₂(H)=.0464 | §5.4 figure 5.2 | ✓ all 4 cells verified, plus α₃ values |
| 41 | FORWARD pseudocode | §4.2 code block + figure 4.4 | ✓ character-for-character |
| 46 | Viterbi intuition: v_t(j) = max_i v_{t-1}(i) a_ij b_j(o_t) | §4.3 line 336-340 | ✓ |
| 47 | Viterbi cell formula | §4.3 figure 4.5 | ✓ |
| 48 | Viterbi recursion (Init/Recurse/Term, with bt) | §4.3 figure 4.6 + formulas | ✓ |
| 49 | VITERBI pseudocode | §4.3 code block + figure 4.7 | ✓ character-for-character |
| 50 | Viterbi trellis on 3 1 3: v₁(H)=.32, v₂(H)=.0448, v₂(C)=.048 | §5.5 figure 5.3 | ✓ all cells verified |
| 51 | Viterbi backtrace highlighting | §5.5 figure 5.4 | ✓ HOT-HOT-HOT path correct |

---

## NAMING / TERMINOLOGY AUDIT (focus per brief)

The brief calls out L09b's non-standard "Evaluation / Decoding / Learning" naming and asks whether the chapter gives both the lecture's and the textbook's names.

**Verdict on the naming audit: mostly good, one polish issue.**

- ✓ The chapter explicitly flags the naming divergence in the **frontmatter "Naming note"** (lines 7-8): *"the slides use the names Evaluation / Decoding / Learning … Textbooks (and most exams) call the same three problems filtering / smoothing-or-decoding / learning. We use both names side-by-side."*
- ✓ §3.5 has a side-by-side table with "Slide name" and "Standard / textbook name(s)" columns.
- ✓ §3.5 has a "Naming note for the exam" callout that distinguishes filtering, smoothing, and decoding.
- ✓ §4.4 comparison table includes both "Lecture slide names" and "Textbook names" rows.
- ✓ §8 cheat-sheet repeats the dual naming.
- ✗ The Problem 1 row in the §3.5 table reads "Evaluation | Filtering (also: likelihood evaluation)". This is misleading — see P1-2. Evaluation is *likelihood*, not *filtering* in the strict sense. The chapter then has to spend a paragraph un-confusing the reader.
- ✗ Problem 2 row says "Decoding | Most-likely state sequence (also: Viterbi decoding; closely related to *smoothing*…)". Smoothing is not closely related — see P2-3.

Net assessment: the **author understands the naming issue and treats it with respect**, but the §3.5 table headline currently undoes some of the good work by half-equating Evaluation with Filtering. A two-line edit (per P1-2 and P2-3) resolves this fully.

---

## CONCEPT COMPLETENESS — checklist against the lecture

| Lecture concept | Covered? | Where |
|---|---|---|
| Motivation: speech recognition, POS, NER, genomics, casino | ✓ | §1 |
| Noisy Channel Model derivation | ✓ | §1 (figure 1.1, slide 5) |
| Markov chain definition (Q, A, row-sums-to-1, start/end states) | ✓ | §3.2 |
| Weighted finite-state automaton (WFSA) framing | ✓ | §3.2 line 146 |
| Markov assumption (first-order) | ✓ | §3.2 line 133, §6 pitfall 7 |
| Initial distribution π | ✓ | §3.1, §3.2 |
| Markov chain weather example with specific numbers | ✓ | §3.2 figure 3.2 |
| Worked Markov-chain example (WARM⁴) | ✓ | §5.1 |
| Discussion: HHHH vs CHCH | ✓ | §5.1 |
| HMM formal definition (Q, A, O, B, q₀, q_F) | ✓ | §3.3 figure 3.3 |
| Vocabulary V | ✓ | §3.3 |
| "Why hidden?" — Σ, Q + emission distribution per state | ✓ | §3.3 |
| Output-independence assumption | ✓ | §3.3, §6 |
| Stationarity | ✓ | §3.1, §6 pitfall 10 |
| HMM diagram (ice cream) | ✓ | §3.3 figure 3.4 |
| HMM diagram (Fair Bet Casino) | **✗** | **Missing — P1-3** |
| Fair Bet Casino numerical setup | ✓ | §3.4 |
| Hidden paths walkthrough | ✓ | §5.2 |
| Three Basic Problems | ✓ | §3.5 (caveat: header confusing, P1-2) |
| Lecture-vs-textbook naming | ✓ | §3.5 naming note + §4.4 table |
| Joint factorisation P(O,Q) | ✓ | §4.1 |
| Brute-force O(N^T) | ✓ | §4.1, §6 pitfall 6 |
| Forward variable α definition | ✓ | §4.2 |
| Forward recursion (Init/Recurse/Term) | ✓ | §4.2 + figure 4.3 |
| Forward complexity O(N²T) | ✓ | §4.2, §8 |
| Forward pseudocode | ✓ | §4.2 code block |
| Forward worked example on 3 1 3 | ✓ | §5.4 (numerically correct) |
| Viterbi variable v definition | ✓ | §4.3 |
| Viterbi recursion | ✓ | §4.3 + figure 4.6 |
| Viterbi backpointers | ✓ | §4.3, §6 pitfall 8 |
| Viterbi pseudocode | ✓ | §4.3 code block |
| Viterbi worked example on 3 1 3 + backtrace | ✓ | §5.5 (numerically correct) |
| Forward vs Viterbi sum/max comparison | ✓ | §2.5, §4.4 |
| Problem 3 (Learning) — Baum-Welch / EM | ✓ (brief, as the lecture does) | §4.5 |
| Numerical underflow warning | ✓ (extra value-add) | §6 pitfall 11 |
| Connection to Bayes nets | ✓ | §7 (caveat: broken anchors, P1-1) |
| Connection to partial observability / L02 agents | ✓ | §7 (caveat: broken anchors) |
| Lab 8 forward-reference | ✓ | §7 |

**Coverage = 38/39 = 97%.** The single miss is the Fair Bet Casino HMM diagram (slide 23). Every other lecture concept is covered, often with extra value-add (analogies, exam pitfalls, cheat sheet).

---

## OUT-OF-SCOPE OBSERVATIONS

- The chapter occasionally **enriches beyond the lecture** (e.g., §6 pitfall 11 introduces log-space underflow, which is not in the slides; §7's DP-pattern remark connects forward/Viterbi to value iteration). These are good pedagogical adds — flagging only because reviewer 1's mandate is concept-completeness against the LECTURE specifically, and a paranoid reader might ask "is this in scope?" The author has been careful to caveat these ("the exam may not test this directly, but Lab 8's implementation may"), so I'd keep them.
- §6 has 12 pitfalls — generous. None are wrong; pitfall 11 (numerical underflow) and pitfall 12 (Problem 3 not derived) are outside the lecture but useful.
- The "where this analogy breaks down" boxes in §2 are not in the slides at all — pure value-add. These are excellent and should stay.
- The Mermaid/figure embedding strategy is consistent: every embedded figure has a caption with section reference and source slide number. Good.

---

## CONCERNS / RISKS

- **Risk that broken cross-references propagate** if other lecture chapters were similarly written by another author without checking the L09a / L02 section numbers. Recommend a global sweep of anchors across `study/lectures/*.md` as a follow-up task.
- **Risk that figures.md's coverage summary stays out of sync** with what is actually embedded. Recommend either (a) the catalogue tightens its USE definition or (b) the chapter embeds the additional figures the catalogue claims are USE. Whichever direction, the catalogue should not lie about coverage.
- **Risk that the §3.5 table reader skims past the naming note** and walks away thinking Evaluation === Filtering. This is the single most likely real-world misunderstanding the chapter could induce. Fix the header.
- The chapter is otherwise **technically rigorous, numerically verified, and pedagogically generous**. The author clearly understood the lecture material in depth.

---

## WHAT THE PM SHOULD DO NEXT

1. **Required (P1) fixes before Round 2:**
   - Fix all five broken §-anchor cross-references (P1-1). Five line edits.
   - Rewrite the §3.5 table header for Problem 1 to stop equating Evaluation with Filtering (P1-2). One-line edit.
   - Embed `page23-render.png` in §3.4 (P1-3). One markdown image insertion + a caption.
   - Add a callout in §5.3 about the state-numbering convention flip (P1-4). One callout box.
   - Add a notation caveat about λ vs Φ in §3.3 (P1-5). One sentence.
2. **Optional (P2) polish** for Round 2 or a later pass — they're all small, none are blockers.
3. **Reconcile figures.md coverage summary** with what the chapter actually embeds (P2-1). One paragraph edit in `figures.md`.
4. After P1 edits, **proceed to other §7.1 reviewers** (style, exam-readiness, etc.). No need to re-QA the math — the worked examples were independently verified and are all correct.

---

## Report to PM

**Assignment recap:** Concept-completeness + figure audit on L09b (HMM), Round 1, Reviewer 1, per Spec §7.1. Special focus: the slides' non-standard "Evaluation/Decoding/Learning" naming.
**Status:** Pass with concerns — the chapter is mathematically correct and conceptually thorough, but has 5 P1 issues (4 broken cross-references, 1 misleading table header, 1 missing slide-23 figure, 1 state-numbering convention flip, 1 notation deviation that should be flagged) that should be fixed before declaring it shippable.
**P0 findings:** None.
**P1 findings:**
1. P1-1 — Broken §-anchors on cross-references to L09a §3.7 (should be §3.13), L09a §3.6 (should be §3.9, twice), L09a §3.1 (should be §3.3), L02 §3.7 (should be §3.6). Suggested fix: editing pass on five lines.
2. P1-2 — §3.5 table headline conflates "Evaluation" with "Filtering". Suggested fix: rename column to "Likelihood evaluation"; keep the naming note clarification.
3. P1-3 — Slide 23 (Fair Bet Casino FSA diagram) not embedded despite catalogue's USE verdict. Suggested fix: add `page23-render.png` to §3.4.
4. P1-4 — State-numbering convention flip between §3.3 (HOT=1) and §5.3 (COLD=1) is treated only as a parenthetical, not a callout. Suggested fix: add a warning box at the start of §5.3.
5. P1-5 — Chapter silently uses λ = (A, B, π) but slide 29 uses Φ = (A, B). Suggested fix: one sentence note in §3.3.
**P2 findings:** P2-1 figures.md coverage summary is wrong; P2-2 relative path to Lab 8 handout fragile; P2-3 "smoothing" mis-equated with decoding in §3.5 parenthetical; P2-4 §3.5 table could add an Operator column; P2-5 §6 pitfall 9 row/column phrasing; P2-6 §6 pitfall 4 needs an example; P2-7 §2.4 wording polish; P2-8 §5.5 ratio could be unpacked; P2-9 §3.4 sharpens slide 20 wording without noting it; P2-10 §5.2 π_F=½ should cite slide 25.
**Concept completeness:** 38 of 39 lecture concepts covered (97%). The miss is the Fair Bet Casino HMM diagram (slide 23). All numerical worked examples were independently verified against the source slides and are correct.
**Naming-discipline audit (per brief):** Largely successful — the frontmatter, §3.5 dual-name table, §3.5 exam note, §4.4 comparison table, and §8 cheat sheet all give both names side-by-side. One slip in the §3.5 table headline (see P1-2) and one in the Problem-2 parenthetical (see P2-3).
**Figure audit:** 17/36 catalogue-USE slides actually embedded in the chapter. Most omissions are text-only definition slides correctly reproduced as prose (acceptable). One genuinely missing diagram (slide 23, see P1-3). Catalogue's coverage summary is out of sync with reality (see P2-1).
**Out-of-scope observations:** Chapter has thoughtful pedagogical extras (analogies, log-space, DP-pattern connection) that go beyond the lecture but are properly caveated. Multiple cross-references to other lecture chapters (L09a, L02, L03, Lab 8) suggest a global anchor-correctness sweep would catch similar issues elsewhere.
**Concerns / risks:** (a) broken cross-references may indicate a project-wide pattern; (b) §3.5 table is the single most likely place a reader gets the wrong takeaway; (c) figures.md catalogue lies about coverage and should be reconciled.
**What PM should do next:** Dispatch a writer to apply the five P1 edits (estimated <30 min of work), then re-run this reviewer or move to the next §7.1 reviewer. No need to re-verify numerical content — all worked examples passed independent verification.
**DOCUMENT.md updated:** N/A for QA.
