# Lab8-HMM — Reviewer #3 (Pedagogical Clarity), Round 1

**Reviewer role:** Lab Reviewer #3 — Pedagogical Clarity
**Assignment recap:** Review `Lab 8/handout/hidden_markov_models_solution.py` against `study/lectures/L09b-HMM.md` for pedagogical clarity. Does a student reading the solution learn what the lecture promised? Are the docstring, MENTAL MODEL section, and code comments **consistent with L09b**? Be harsh.
**Files inspected (absolute paths):**

- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 8\handout\hidden_markov_models_solution.py`
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 8\handout\hidden_markov_models.py` (template, for diff context)
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L09b-HMM.md`

**Status:** **Fail** — multiple P0 pedagogical defects. The MENTAL MODEL borrows the *wrong* lecture analogy, the docstring teaches a lecture-naming convention the lecture *explicitly warns against*, the worked numbers in the printed "Reference output" cannot be reproduced from the lecture (different HMM, never reconciled), and the code uses a Jurafsky-augmented `q_0`/`q_F` dummy-state formulation that L09b §3.5/§4.2 do not teach — yet the docstring claims "lecture pseudocode" verbatim. A student reading this file alongside the lecture will be confused at every alignment point.

---

## P0 Findings (broken pedagogy / actively misleading)

### P0-1. MENTAL MODEL uses the *umbrella* analogy without telling the student the lab is the *ice-cream* example — and then mashes the two together

**Location:** `hidden_markov_models_solution.py:27–34` (MENTAL MODEL block).

```
"You watch someone's umbrella every morning to guess if it's raining inside
their house" — except here you count Jason's ice creams every day (the
visible observation) and infer whether the day was HOT or COLD (the hidden
weather). The Forward algorithm asks "how likely is this whole record of
ice-cream counts under the model?"; Viterbi asks "what single weather
sequence best explains it?".
```

**Problem.** L09b §2.1 builds the **umbrella-and-hidden-weather** analogy as one specific running mental model (`watching the neighbour's umbrella every morning to guess if it's raining inside`). The lecture's "ice cream → HOT/COLD" example is the *concrete worked example* (§5.3–§5.5), **not** an analogy — and crucially the lecture **never blends the two**. The umbrella story has rain (binary observation) inferring rain (binary state); the ice-cream story has counts {1,2,3} inferring HOT/COLD. Smashing them together in one sentence ("watch someone's umbrella every morning to guess if it's raining inside their house — except here you count Jason's ice creams") **breaks the analogy**: the analogy now reads "watch X to infer X-but-actually-Y" which is nonsense. A student who internalises this hybrid will then read §2.1 of the lecture and wonder why the lecture is teaching a *different* analogy. It is not different — the lab is just splicing it incorrectly.

**Pedagogical damage.** The MENTAL MODEL is supposed to be the one-line scaffold a student carries into the exam. This one is a Frankenstein.

**Suggested fix.** Pick one. Either (a) restate L09b §2.1's umbrella analogy *as the analogy* and then say "and in this lab, the concrete instantiation is Jason's ice creams = umbrella (observation), weather = weather (state)"; or (b) ditch the umbrella entirely and write the ice-cream example as its own self-contained mental model. The current half-and-half costs the student the structural insight that the lecture spent §2.1 building.

---

### P0-2. The docstring teaches "Problem 1 = Evaluation = filtering" — which is exactly the naming trap L09b §3.5 spends a full table warning against

**Location:** `hidden_markov_models_solution.py:38–42` (REFERENCES block).

```
The lecture uses the textbook naming convention: Problem 1 = Evaluation
(= filtering in some texts), Problem 2 = Decoding (= most-likely sequence
/ Viterbi), Problem 3 = Learning (= Baum-Welch, not exercised here).
```

**Problem.** This is **almost the exact opposite** of what L09b §3.5 says. The lecture's own naming-note (verbatim, lines 7 and 274–281 of L09b) reads:

> "the slides use the names Evaluation / Decoding / Learning ... Textbooks (and most exams) call the same three problems filtering / smoothing-or-decoding / learning."

L09b is explicit that **slide-name "Evaluation" ≠ textbook "filtering"**. Filtering strictly means $P(q_t \mid o_1..o_t)$ — a *posterior over the current state*; Evaluation means $P(O \mid \lambda)$ — the *likelihood of the whole observation sequence*. They share an algorithm (forward), but they are different outputs. L09b §6 Pitfall #1 spells this out yet again: "Filtering means different things in the slides vs textbooks."

The solution's docstring **collapses the very distinction the lecture exists to make**. It also reverses the attribution: "The lecture uses the textbook naming convention" — no, it does *not*. The lecture uses the slide names (Evaluation / Decoding / Learning) and explicitly contrasts them with textbook names. The docstring is misattributing the source.

**Pedagogical damage.** A student who reads this docstring before reading L09b will arrive at §3.5 already convinced that the four names are interchangeable, miss the trap, and lose a mark on any exam question that says "compute the filtered posterior" (which wants normalisation by $\sum_i \alpha_t(i)$, not the raw forward probability).

**Suggested fix.** Rewrite as: "The slides name the three problems Evaluation / Decoding / Learning. Textbooks call them filtering (loosely) / decoding / learning. L09b §3.5 spells out the distinction — in particular 'filtering' strictly means $P(q_t \mid o_1..o_t)$ (a posterior over the *current* state), which is *not* what `compute_forward` returns. `compute_forward` returns $P(O \mid \lambda)$, the slide-Evaluation quantity. The filtered posterior is `compute_filtered` (KNOB MODE='filter') and is `alpha_t(j) / sum_i alpha_t(i)`."

---

### P0-3. The "Reference output" numbers cannot be reproduced from the lecture — the lab silently swaps the HMM with no flag to the student

**Location:** `hidden_markov_models_solution.py:21–25` (docstring HMM-source caveat) and `:92–105` (reference output).

```
The HMM (Jurafsky & Martin, SLP3 Appendix A — "Jason's ice creams")
parameters used here are TAKEN VERBATIM FROM THE TEMPLATE FILE, not from
the slide diagram. The template's emission matrix differs from the slide
(slide: P(3|H)=.4, P(3|C)=.1; template: P(3|H)=.75, P(3|C)=.1). The
KNOBs section below documents both so a student can switch.
```

```
Observations: 3 1 3
Probability: 0.016809200000000003
Path: ['hot', 'cold', 'hot']
```

**Problem.** The docstring acknowledges *one* discrepancy (the emission matrix), but the divergence from L09b is far worse. **The transition matrix is also wildly different.**

| Parameter | Lecture (L09b §5.3) | Template / Solution | Match? |
|---|---|---|---|
| $\pi_H$ | 0.8 | 0.8 (from `TRANSITIONS[0,1]`) | OK |
| $\pi_C$ | 0.2 | 0.2 | OK |
| $a_{HH}$ | **0.7** | **0.2** (`TRANSITIONS[1,1]`) | **WRONG** |
| $a_{HC}$ | **0.3** | **0.6** (`TRANSITIONS[1,2]`) | **WRONG** |
| $a_{CH}$ | 0.4 | 0.3 | WRONG |
| $a_{CC}$ | 0.6 | 0.5 | WRONG |
| $b_H(3)$ | 0.4 | 0.75 | WRONG |
| $b_C(1)$ | 0.5 | 0.8 | WRONG |

So **none of the transitions and none of the emissions match the lecture's worked example**, yet the docstring frames the divergence as "emissions differ" only. The lecture's worked example (§5.4 forward, §5.5 Viterbi) gives:

- Forward on $O = 3,1,3$: $P(O \mid \lambda) = 0.026264$. Solution prints `0.016809...`.
- Viterbi on $O = 3,1,3$: path $= H, H, H$ with probability $0.012544$. Solution prints `['hot', 'cold', 'hot']`.

**Different probability, different path.** The L09b cheat-sheet (§8) lists the "ice-cream HMM constants to memorise (for the exam)" — and the solution's HMM is *not* those constants. A student who runs the solution to check their hand-computation of §5.4 / §5.5 will discover that the script reports a different answer and conclude the lecture is wrong. Or, more likely, will memorise the solution's HMM by accident and lose marks on the exam.

**Pedagogical damage — severe.** L09b §8 explicitly asks the student to memorise the ice-cream HMM constants. The solution provides a *different* HMM as default and treats the discrepancy as a footnote. The KNOB-EMISSIONS comment at L172–177 notes that the slide values exist but doesn't say *what the default produces is unreproducible from the lecture's §5.4 arithmetic*. The KNOB-TRANSITIONS comment (L149–165) doesn't mention any divergence at all — the lecture's transitions are nowhere documented in this file.

**Suggested fix.** One of:

1. **Make the default match the lecture.** Change `TRANSITIONS` and `EMISSIONS` to L09b §5.3 values. Add a KNOB note "if your lab handout HMM differs, switch to the alternate matrices below." This matches the cheat-sheet the student is meant to memorise.
2. **If the lab-PDF requires the template values for grading**, then at minimum add a giant warning at the top of the MENTAL MODEL block: "WARNING: this HMM differs from L09b's worked example. The lecture's $P(O=3,1,3)=0.0263$ and best-path HHH; this script's HMM gives $0.0168$ and HCH. Both are valid HMMs — the algorithms are the same — but do **not** memorise this script's numbers thinking they are the lecture's."
3. Document *all* the differences in the KNOB block, not just emissions.

As written, the solution silently miseducates.

---

### P0-4. The code uses the Jurafsky-augmented dummy-start / dummy-end formulation, but the docstring claims it is "next to the slide pseudocode" — and L09b §4.2's pseudocode is the textbook $\pi$/$\sum$ form, not the augmented form

**Location:** `hidden_markov_models_solution.py:249–287` (`compute_forward`), `:290–341` (`compute_viterbi`), and the docstring claim at L253–254 ("Mirroring that here keeps the implementation readable next to the slide pseudocode").

**Problem.** L09b §4.2 (Figure 4.4 / slide 41) gives the forward pseudocode as:

```
forward[s, 1] <- pi_s * b_s(o_1)              ; initialization
...
forwardprob <- sum over s from 1 to N of forward[s, T]  ; termination
```

— two real states $1..N$, initial vector $\pi$ multiplied at $t=1$, total likelihood = sum over column $T$. **No dummy start/end states, no `qf`, no extra final-column row.**

The solution implements a *different* formulation: an augmented state graph with `q_0 = "initial"` and `q_F = "final"`, where `pi_s` is encoded as `a_transitions[0, s]` (row 0 of the transition matrix) and the termination sums over `forward[s, big_t] * a_transitions[s, qf]` (with an *additional* end-transition factor). This is the **Jurafsky & Martin SLP3 Appendix A** formulation — the same source the lab's PDF cites — but L09b §4.2 does **not** use it.

Crucially, the augmented form changes the termination arithmetic. L09b's termination is:

$$P(O \mid \lambda) = \sum_{i=1}^{N} \alpha_T(i)$$

The solution's termination is:

$$P(O \mid \lambda) = \sum_{s=1}^{N} \alpha_T(s) \cdot a_{s, q_F}$$

These give **different numerical answers** unless every $a_{s, q_F} = 1$, which isn't the case here ($a_{H, \text{end}} = a_{C, \text{end}} = 0.2$). The solution multiplies by an extra "transition into END" factor that the lecture's worked example *does not include*. (This explains some of the gap between the lecture's $P(O=3,1,3) = 0.0263$ and the solution's $0.0168$ — even if the matrices matched, the augmented termination would scale the answer down by ~$0.2$.)

The comment at L253–254 says:

```
Why the index gymnastics: the lecture's pseudocode is 1-indexed for
both states (1..N, with 0 = start and N+1 = end) and time (1..T,
with a sentinel None at observations[0]). Mirroring that here keeps
the implementation readable next to the slide pseudocode.
```

This is **factually wrong**: L09b §4.2 pseudocode is 1-indexed but **only** for $s \in 1..N$ and $t \in 1..T$. There is no `0 = start` or `N+1 = end` in slide 41's pseudocode. The solution invents a formulation that is *not* in the lecture and then attributes it to the lecture.

**Pedagogical damage — severe.** The student who reads this file with L09b §4.2 open side-by-side will see two different algorithms and have no way to know which is "right" for the exam. The lecture says "this is the slide pseudocode"; the solution says "this is the slide pseudocode"; they are different. A diligent student loses a half-hour to that confusion; a less-diligent student memorises the wrong shape and writes the augmented version on an exam that wanted the textbook version (or vice versa).

**Suggested fix.** Either:

1. **Re-implement in the L09b §4.2 form.** Drop the augmented start/end states. Use an explicit `pi: ndarray` parameter. Termination = `sum(forward[:, T])`. Then the comment "next to the slide pseudocode" is true.
2. **Keep the augmented form but be honest about it.** Rewrite the comment to: "This implementation uses the **Jurafsky augmented formulation** (Jurafsky & Martin SLP3 Appendix A, slide 17's `q_0, q_F` row of the HMM definition). It is *equivalent* to the L09b §4.2 pseudocode *only* when `a_{s, q_F} = 1` for all real states $s$. Here `a_{H,e} = a_{C,e} = 0.2`, so the termination differs from §4.2 by a factor of $\sum_s a_{s, q_F}\alpha_T(s) / \sum_s \alpha_T(s)$. The slide-41 pseudocode is the *simpler* form: `forwardprob = sum_s forward[s, T]`, no end-transition multiplier."

As written, the solution does (1)'s job badly and pretends it did so faithfully.

---

### P0-5. The `compute_forward` recursion in the solution does **not** match L09b's slide-41 pseudocode for the very reason the file claims it does

**Location:** `hidden_markov_models_solution.py:270–272` (Forward initialization).

```python
# Initialization step: alpha_1(s) = a_{0,s} * b_s(o_1) for each real state s.
for s in inclusive_range(1, big_n):
    forward[s, 1] = a_transitions[0, s] * b_emissions[s, observations[1]]
```

**Problem.** The comment says "$\alpha_1(s) = a_{0,s} \cdot b_s(o_1)$". L09b §4.2's slide-41 form is "$\alpha_1(s) = \pi_s \cdot b_s(o_1)$". The solution's `a_{0,s}` is *equivalent* to $\pi_s$ ONLY IF the user understands that `TRANSITIONS[0, :]` is being repurposed as $\pi$. The file does say this at L151–153 ("Row 0 is the initial distribution: A[0, j] = P(q_1 = j)") — but in the **TRANSITIONS knob comment**, not in the `compute_forward` body. A student reading the algorithm alone sees `a_transitions[0, s]` and asks "wait, what is transition-from-the-zero-state?". The lecture has no zero state.

**Pedagogical damage.** Compounding P0-4. The init uses `a_{0,s}`; the lecture uses $\pi_s$. They are numerically the same (because of the encoding choice), but the *form* of the algorithm reads differently. A student who learned from L09b §4.2 and looks at this code will struggle to map line-for-line.

**Suggested fix.** Either rename the parameter / unpack a real `pi` variable inside `compute_forward` so the line reads `forward[s, 1] = pi[s] * b_emissions[s, observations[1]]`, or aggressively annotate the equivalence in the body comment.

---

### P0-6. "Pseudocode mapping" comments in `compute_forward` / `compute_viterbi` are too terse to do their job

**Location:** `hidden_markov_models_solution.py:270–286` (Forward) and `:309–341` (Viterbi).

**Problem.** The lecture's L09b §4.2 forward pseudocode is reproduced **verbatim** in the lecture (lines 372–382 of L09b-HMM.md). A pedagogically clear solution would put each line of that pseudocode beside its Python counterpart so a student can see "this Python line *is* this pseudocode line". The solution instead writes one-line "Initialization step", "Recursion step", "Termination" comments without quoting the pseudocode.

Compare to how the Lab 6 (CSP) solution's `recursive_backtracking` body is annotated line-for-line against L07's backtracking pseudocode — that's the standard. This file falls short.

**Suggested fix.** Above each section of the algorithm, paste a 2-3 line excerpt of the slide-41 pseudocode in a comment. Example:

```python
# Slide 41 pseudocode:
#     for each state s from 1 to N do
#         forward[s, 1] <- pi_s * b_s(o_1)
for s in inclusive_range(1, big_n):
    forward[s, 1] = a_transitions[0, s] * b_emissions[s, observations[1]]
```

---

### P0-7. KNOB block conflates two different notational conventions and never tells the student which one the lecture uses

**Location:** `hidden_markov_models_solution.py:131` (`STATES = ["initial", "hot", "cold", "final"]`) versus L09b §3.3 / §5.3.

**Problem.** L09b §3.3 (line 211 — the "Notation caveat" callout) explicitly says:

> "Slide 29 writes the parameters as $\Phi = (A, B)$, folding $\pi$ in implicitly with the start state $q_0$ (and the $a_{0j}$ transitions are *another* way of writing $\pi_j$ — the two notations are equivalent for the math but the $\pi$-vector form is the textbook standard). The chapter keeps $\pi$ explicit and uses $\lambda$ throughout."

The lab chooses the **non-textbook-standard** form (start/end states, no explicit $\pi$) and never references the caveat. A student opening L09b §3.3 has the warning sign; the lab's KNOB block at L120–131 doesn't even mention $\pi$ as a name, nor does it tell the student "this convention is the slide-29 / Jurafsky-SLP3 form, not the $\lambda = (A, B, \pi)$ form the lecture defaults to". The KNOB comment at L122–125 ("the first ('initial') and last ('final') are *dummy* start/end markers used by the augmented Jurafsky formulation") gets close — but doesn't connect to L09b's own warning.

**Suggested fix.** Cite L09b §3.3 line 211. Add: "this lab follows the augmented `q_0`/`q_F` formulation. L09b §3.3's 'Notation caveat' calls this equivalent-but-not-textbook-standard."

---

## P1 Findings (important pedagogical / convention issues)

### P1-1. MODE = "filter" is described as a posterior, but the implementation only normalises the forward column — same forward-vs-filtering confusion as P0-2

**Location:** `hidden_markov_models_solution.py:188–201` (MODE knob), `:372–398` (`compute_filtered`).

The KNOB comment at L188–197 says:
```
"filter":  for each t, print P(q_t = k | o_{1..t}), the
           normalised forward column.
```

This is correct in formula but the docstring at L75–83 says:

```
"Filtered" P(q_t = k | o_{1..t}) is alpha_t(k) / sum_j alpha_t(j) — set
KNOB MODE = "filter" and the script prints the normalised forward
trellis column at each t.
```

Both statements use "filter" / "Filtered" in the strict-textbook sense (good!). But the docstring's MENTAL MODEL and the REFERENCES block (P0-2) use "filtering" in the *loose slide* sense. Within a single file, "filtering" refers to two different things. L09b's §6 Pitfall #1 is *exactly* the warning against this mixing.

**Pedagogical damage.** The student is fed both definitions and given no way to disambiguate. The lab is meant to dispel the confusion; instead it embodies it.

**Suggested fix.** Standardise on one definition (the strict-textbook one is the safer exam answer). Update the REFERENCES block to match.

---

### P1-2. `compute_smoothed` is silently introduced as "Variant 3" with no lecture cross-reference, even though L09b §4.6 covers it

**Location:** `hidden_markov_models_solution.py:344–369` (`compute_backward`), `:401–428` (`compute_smoothed`).

**Problem.** The lecture's §4.6 is the **explicit** section on the backward recursion and smoothing — it even calls out "We include it here so that 'how would you compute $P(q_5 \mid o_1 \ldots o_{10})$?' is not a question this chapter leaves unanswered." The solution implements `compute_backward` and `compute_smoothed` but cites only "Used only by `compute_smoothed` (Variant 3)" (L350). No reference to L09b §4.6, no formula citation, no mention of the standard forward-backward identity (`alpha * beta / P(O|lambda)`).

The implementation also uses the *augmented* termination (line 360: `backward[s, big_t] = a_transitions[s, qf]`), which is *not* the L09b §4.6 backward initialization $\beta_T(j) = 1$. Same pattern as P0-4: lecture says one thing, code does another, comment doesn't flag the divergence.

**Suggested fix.** Add a docstring reference: "L09b §4.6 defines $\beta_T(j) = 1$ in the non-augmented formulation; this implementation uses the augmented $\beta_T(s) = a_{s, q_F}$ — equivalent under the augmented HMM." And cite the smoothing formula explicitly.

---

### P1-3. `argmax` is renamed/rewritten with a "make better sense in my head" comment that has no pedagogical justification

**Location:** `hidden_markov_models_solution.py:431–438`.

```python
def argmax(sequence: list[tuple[float, float]]):
    '''
    This takes in a list, that provides its own keys as tuples.
    As such the following must hold true:
    sequence[i] = tuple(key, value)
    '''
    # I have rewritten this function slightly, to make it make better sense in my head
    return max(sequence, key=lambda x: x[1])[0]
```

The comment "I have rewritten this function slightly, to make it make better sense in my head" is a **first-person artefact of the original student template**. The solution file is supposed to be a polished teaching artefact — first-person diary comments don't belong. Worse, the type annotation `list[tuple[float, float]]` is wrong — the actual callers pass `list[tuple[int, float]]` (the first element is a state index, not a float).

This is a hangover from the template (`hidden_markov_models.py:112–119` — identical comment). The solution preserved it without re-evaluation.

**Suggested fix.** Replace docstring with: "Given a list of `(state_index, score)` tuples, return the `state_index` with the highest score. Used as the backpointer-stash in Viterbi (§4.3)." Fix the type annotation. Drop the diary comment.

---

### P1-4. The 5-as-sentinel pattern is in the code AND the comment, but the *reason* it survives in `compute_forward` is unstated

**Location:** `hidden_markov_models_solution.py:265–268`.

```python
# probability matrix - all values initialized to 5, as 0 has meaning in the matrix
# (5 is a sentinel value that should NEVER appear in the returned matrix; it
# would indicate an un-touched cell — useful during development.)
forward: ndarray = np.ones((big_n + 2, big_t + 1)) * 5
```

**Problem.** The comment correctly identifies why the sentinel exists (so an un-touched cell is visible) but the algorithm **leaves multiple cells un-touched in production runs**. Specifically: `forward[0, :]` (the initial state row) is never overwritten, and `forward[qf, :T-1]` is never overwritten. After the function runs, `forward[0, 1]`, `forward[0, 2]`, `forward[0, 3]`, etc., are all `5.0`. So the sentinel *does* survive in returned-state contexts (e.g. if anyone inspects `forward` after-the-fact via `compute_filtered`).

Compare to `compute_filtered` (L383), which uses `np.zeros(...)` for the same matrix — a more sensible default. Why does `compute_forward` use 5 and `compute_filtered` use 0? Different developer instincts, no comment reconciliation. The L09b §6 Pitfall #1 student is going to look at both and wonder which is "the right way".

**Suggested fix.** Pick `np.zeros(...)` everywhere. The "sentinel for development" justification belonged in the template; once the implementation is correct it adds noise.

---

### P1-5. The TRANSITIONS comment teaches an end-transition column without ever explaining *why* this lab uses one

**Location:** `hidden_markov_models_solution.py:149–165`.

```
A[i,j] = P(q_{t+1}=j | q_t=i). Row 0 is the *initial*
distribution: A[0, j] = P(q_1 = j). The last column is the
end-transition probability A[i, qf] = P(q_T+1 = end | q_t = i).
```

**Problem.** L09b §3.3 / §5.3 does **not** use end-transition probabilities. The augmented form (`a_{i,F}` end-transitions) appears nowhere in the lecture's worked numbers — L09b's §5.4 forward computation terminates at `sum_i alpha_T(i)`, period.

A student reading the KNOB will ask: "the lecture doesn't have this column — why does the lab?" The KNOB never answers. It's just there.

Even worse: the row sums of TRANSITIONS for "Hot" are `[.0, .2, .6, .2] = 1.0` (good, valid distribution). But that means *with probability 0.2 per step the sequence terminates regardless of observation*, which is a model assumption the lecture never discusses. The lab silently adopts an HMM where the sequence has a per-step termination probability — a substantively different model from §3.3.

**Pedagogical damage.** A student internalises "HMMs have per-step termination probabilities" and writes that on an exam question about §3.3.

**Suggested fix.** Add a paragraph: "this HMM uses the **augmented start/end** convention (Jurafsky & Martin SLP3 Appendix A). The end column `A[i, qf]` is a Jurafsky-only convention; L09b §3.3 does **not** include it. The lecture's HMM treats observation sequences as ending exogenously (no per-step end probability). Both are valid HMMs; the algorithms below match the augmented variant."

---

### P1-6. The MENTAL MODEL doesn't include any of the `sum vs max` insight L09b §2.5 builds

**Location:** `hidden_markov_models_solution.py:27–34` (MENTAL MODEL).

**Problem.** L09b §2.5 is one of the highest-value analogies in the lecture — **"Forward vs Viterbi as sum vs max"** — and the lecture's §8 cheat-sheet repeats it as "$\sum$ vs $\max$ on the same trellis". The lab's MENTAL MODEL skips it entirely: it tells the student what Forward and Viterbi *each ask*, but not the structural insight that they are the same trellis, same numbers, one operator apart. This is the *exam-ready one-liner*.

**Suggested fix.** Add to MENTAL MODEL: "Forward and Viterbi share the same trellis and the same per-cell weights ($\alpha_{t-1}(i) \cdot a_{ij} \cdot b_j(o_t)$). They differ in **one** operator: Forward uses $\sum_i$, Viterbi uses $\max_i$ (plus a backpointer). L09b §2.5 / §4.4."

---

### P1-7. Comments inside `compute_viterbi` recursion say "the *single best* path, not the marginal" — good — but never define "marginal"

**Location:** `hidden_markov_models_solution.py:315–317`.

```
# Recursion: instead of summing over the previous column we take the
# argmax — Viterbi keeps the *single best* path, not the marginal.
```

**Problem.** "Marginal" is a probability-theory term L09b uses sparingly (§4.6 mentions "per-time-step marginal posteriors"). A student who hasn't internalised what "marginal" means in this context — i.e. the sum over hidden state histories — will read "best path, not marginal" and be lost. The comment is technically correct but pedagogically opaque.

**Suggested fix.** "Recursion: instead of summing over previous-state choices (which gives the *total* probability of reaching here — what Forward computes) we take the argmax — Viterbi keeps the *probability of the single best path* that reaches here." Avoid "marginal" without unpacking.

---

### P1-8. No reference to L09b §6 Pitfall #2 — "Confusing forward $\alpha$ with Viterbi $v$"

**Location:** Throughout `compute_forward` (L249–287) and `compute_viterbi` (L290–341).

**Problem.** The lecture lists this confusion as the #2 most common exam mistake. The solution names the variables `forward` and `viterbi` (sensible) but uses identical-shape arrays, identical initialization (lines 271–272 vs 311–313), and identical inclusive_range loops. A student staring at `compute_forward` and `compute_viterbi` side-by-side will see two functions that look 90% the same — perfect breeding ground for the §6 Pitfall #2 confusion. Yet no comment in either function flags "the ONLY difference from compute_forward is the `max`-over-`sum` swap and the backpointer". The lecture's §4.4 side-by-side comparison table is the canonical pedagogical tool here, and it's nowhere referenced.

**Suggested fix.** At the top of `compute_viterbi`, add: "This function is identical to `compute_forward` except: (a) `sum(...)` → `max(... for ...)`; (b) we additionally record `backpointers[s, t]`. See L09b §4.4 side-by-side and §6 Pitfall #2."

---

### P1-9. The reference output for sequence A / B is presented without any sanity-check the student can do by hand

**Location:** `hidden_markov_models_solution.py:99–105`.

**Problem.** The reference outputs for the longer sequences A and B (length 9) have probabilities `~1.5e-6` and `~1.3e-6`. These are completely unverifiable by inspection. Worse, L09b §6 Pitfall #11 warns: "Numerical underflow. Probabilities multiply across many time steps; for long sequences $\alpha$ and $v$ values quickly underflow floating-point. In practice we work in log space." The lab's solution **doesn't** work in log space and the docstring **doesn't** mention this is a concern. At sequence length 9 with $b$ values around $0.1$, you are 9 multiplications by ≤1 deep — fine for float64, but the lab provides no guidance on when it would stop being fine. L09b §6 Pitfall #11 explicitly says "Lab 8's implementation may [hit underflow]; flag it if asked about implementation concerns."

**Suggested fix.** Add to the docstring (or as a comment near the recursion): "This implementation uses raw probabilities (multiplications). For sequences much longer than ~50 steps, expect underflow — switch to log-space (L09b §6 Pitfall #11). The lab's reference sequences are short enough that float64 is safe."

---

### P1-10. "ENTRY POINT: yes" is a `pm-setup` / Reviewer #1 convention but isn't explained for the student

**Location:** `hidden_markov_models_solution.py:107–110`.

**Problem.** `ENTRY POINT: yes` is a flag that means something to a tool (or a grader using a script) but is undocumented in the file. A student reading the solution sees an unexplained marker and assumes it's important. The convention should either be (a) consistent with how other lab solutions tag entry-points, or (b) replaced with prose ("Run directly with `python hidden_markov_models_solution.py`").

**Suggested fix.** Leave only the prose line and drop the marker, or document the convention in a header comment.

---

### P1-11. DOCUMENT.md missing

**Location:** `c:/Users/samgl/Documents/GitHub/ExamPrep/AI/Lab 8/handout/`.

**Problem.** Global CLAUDE.md requires every directory with modified files to ship a `DOCUMENT.md`. The handout directory was modified (the `_solution.py` was added) and there is no `DOCUMENT.md` in `Lab 8/handout/`. Reviewer #3's lens: a student opening the directory has no entry-point document explaining "here is the lab handout, here is the template you fill in, here is the reference solution to consult after you try yourself." That document is part of the pedagogy.

**Suggested fix.** Add `Lab 8/handout/DOCUMENT.md` covering: (a) the lab task (forward + Viterbi on Jason's ice creams); (b) which file is template vs solution; (c) the HMM-divergence-from-lecture caveat (P0-3); (d) link to L09b §4.2 / §4.3.

---

## P2 Findings (polish, suggestions)

### P2-1. Inconsistent indexing-comment style between `compute_forward` and `compute_viterbi`

The Forward initialization (L270–272) comments the formula `alpha_1(s) = a_{0,s} * b_s(o_1)`. The Viterbi initialization (L309–313) just says "Initialization: same as Forward but we *also* set a backpointer of 0". Inconsistent: either both spell out the formula, or both refer.

### P2-2. The KNOB block (L116–201) is 85 lines for a 200-line algorithm file

The L09b lecture is the source of truth; the file's KNOBs are a useful "what to change for variants" guide but are disproportionate. Move the "Exam variants" sub-bullets to a sibling `DOCUMENT.md` to keep the algorithm body the headline.

### P2-3. `convert_path_states_to_observations` is a misleading function name

The function turns `[1, 2, 1]` into `['hot', 'cold', 'hot']` — i.e. *state indices* to *state names*, NOT to *observations*. Observations are the ice-cream counts. The function name should be `convert_path_indices_to_state_names` or similar. Inherited from the template (`hidden_markov_models.py:66`).

### P2-4. The Jurafsky URL at the bottom of the REFERENCES block is well-meaning but unused in the file's body

L48–50 references `https://web.stanford.edu/~jurafsky/slp3/A.pdf`. A pedagogically tighter file would either cite specific page numbers (Jurafsky Appendix A pp. 5–7 for the forward derivation) or omit the URL.

### P2-5. The `inclusive_range` helper (L245–246) is fine but the comment-free presentation hides a potential student trap

`range(a, b+1)` is the idiom; `inclusive_range(1, big_n)` reads as "1 to big_n inclusive". A one-line docstring `"""Yields a, a+1, ..., b — i.e. inclusive of both endpoints (in contrast to Python's half-open range)."""` would help.

### P2-6. `print(f"Path: ...")` mixes f-strings and `.format()` in the same `main` function

L213 uses `.format`; L219 uses an f-string. Cosmetic, but a teaching file should pick one.

### P2-7. The MENTAL MODEL block is 10 lines; L09b §2 builds *eight* mental-model analogies

Some — like §2.4 GPS-breadcrumbs for Viterbi, §2.7 climatological-prior for $\pi$ — are very strong exam-ready hooks. The lab's MENTAL MODEL section could reference §2 instead of inventing its own truncated one.

---

## Lecture-Alignment Audit (does the solution teach what L09b promises?)

| Lecture concept | L09b reference | Solution coverage | Verdict |
|---|---|---|---|
| HMM = $\lambda = (A, B, \pi)$ definition | §3.3 | KNOBs introduce A, B, but no explicit $\pi$ — bundled into row 0 of A | **half-broken** (P0-7, P1-5) |
| Umbrella mental model | §2.1 | Mangled — fused with ice-cream | **broken** (P0-1) |
| Sum vs max insight | §2.5 / §4.4 | Absent from MENTAL MODEL; uncited in code | **broken** (P1-6, P1-8) |
| Forward recursion (slide-41 pseudocode) | §4.2 | Code uses *augmented* form, not slide-41 form | **broken** (P0-4, P0-5, P0-6) |
| Forward worked numbers on $O=3,1,3$ | §5.4 | Solution prints **0.0168**, lecture gives **0.0263** | **broken** (P0-3) |
| Viterbi recursion + backpointers | §4.3 | Implemented (correctly in shape), but comments don't cite §4.3 / §6 Pitfall #2 | half-broken (P1-7, P1-8) |
| Viterbi worked numbers on $O=3,1,3$ | §5.5 | Solution prints **HCH**, lecture gives **HHH** | **broken** (P0-3) |
| Three problems (Eval / Decoding / Learning) vs four task names (filter / smooth / predict / decode) | §3.5 + naming-note | REFERENCES collapses the distinction the lecture spends a page making | **broken** (P0-2) |
| Backward recursion + smoothing | §4.6 | Implemented in `compute_backward` / `compute_smoothed`; **un-cited** | half-broken (P1-2) |
| First-order Markov assumption + output-independence | §3.3, §6 Pitfall #7 | Not mentioned in code or comments | missed teaching opportunity |
| Numerical underflow / log-space (§6 Pitfall #11) | §6 | Implementation uses raw probs; not flagged | half-broken (P1-9) |
| $O(N^T)$ vs $O(N^2 T)$ complexity (§6 Pitfall #6) | §4.2 / §6 | Not referenced anywhere | missed teaching opportunity |
| Ice-cream HMM constants for the exam | §8 cheat-sheet | Solution **contradicts** the cheat-sheet constants | **broken** (P0-3) |

**Net pedagogical verdict.** Roughly half of the lecture's headline pedagogical structure (the umbrella analogy, the sum-vs-max insight, the slide-41 forward pseudocode, the §5.4/§5.5 worked numbers, the naming-note about filtering, the §8 cheat-sheet ice-cream constants) is either misrepresented, swapped for a different formulation, or contradicted by the solution's reference output. A student who studies this file in lieu of the lecture will arrive at the exam with the wrong analogies, the wrong numbers for the canonical example, and the wrong understanding of what "filtering" means.

---

## Out-of-scope observations

1. **The template file** (`hidden_markov_models.py`) inherits most of P1-3 (first-person `argmax` comment) and P2-3 (function-name confusion). Both files would benefit from the same cleanup.
2. **`__pycache__` directory in the handout** — student artefacts should not be checked in. Add to `.gitignore`. (Not Reviewer #3's primary concern.)
3. **The `Lab 8.pdf`** likely specifies the template HMM (since the solution uses it). If the PDF is the grading source, the solution's HMM is *correct for grading* — but then the lecture is the *odd one out* and the lab should bridge that gap explicitly. Cross-checking the PDF is outside Reviewer #3's lane; recommend the PM dispatch an Investigator to confirm.

---

## Concerns / Risks

1. **Most damaging issue is P0-3** (wrong HMM, unreproducible against lecture). Everything else cascades — once a student learns the wrong numbers, all the §5.4/§5.5 cross-check value of the lecture is gone. Fix this first.
2. **P0-2 (filtering naming)** is the highest-leverage exam-loss risk. The lecture spends an entire callout warning against this collapse; the solution embodies the collapse. Any exam question that uses "filtering" in the strict sense will catch students who memorised the solution's gloss.
3. **P0-4 (augmented vs slide pseudocode)** is the highest-leverage *understanding* risk. A student who memorises the augmented forward termination (`sum_s alpha_T(s) * a_{s, qf}`) will be marked wrong on any exam question that uses the lecture's `sum_s alpha_T(s)` form, and vice versa. The lab needs to *pick* one form (with documented equivalence) — not slip silently between them.
4. **The file has good intentions.** The KNOB block, the MENTAL MODEL header, the variant-adaptation manual — these are pedagogically thoughtful patterns. The execution misses on the alignment-with-lecture axis. Reviewer #3's call is not "throw this away", it's "fix the lecture-alignment defects and the rest is a strong solution scaffold".
5. **Pre-existing template warts were preserved.** The `argmax` "make better sense in my head" comment (P1-3), the `5`-as-sentinel pattern (P1-4), the function-name confusion `convert_path_states_to_observations` (P2-3) are all from `hidden_markov_models.py`. The solution adds nothing flagging them.

---

## What the PM should do next

1. **Dispatch the engineer to fix P0-1 through P0-7 first**, in that order. P0-3 (HMM mismatch with lecture) is the single most damaging issue — pick a path: change defaults to match L09b §5.3, OR add a giant warning, OR refactor the KNOBs so the lecture-canonical HMM is the default and the template HMM is the override. Then P0-2 (filtering-name collapse), P0-4/P0-5/P0-6 (pseudocode-form misattribution), P0-7 (notation convention).
2. **Then P1-1 to P1-11**, especially the missing `DOCUMENT.md` (P1-11), the un-cited backward/smoothing (P1-2), and the missing `sum vs max` insight in MENTAL MODEL (P1-6) / Viterbi (P1-8).
3. **Re-dispatch Reviewer #3** after fixes. The Lecture-Alignment Audit table above is the rubric: every "broken" row must move to "OK" before this file is fit to ship as a study artefact.
4. **Do not proceed to App Tester yet.** App Tester would run the file and compare outputs against the docstring's reference values — those values match the *template HMM*, not the lecture's HMM, and App Tester wouldn't know to flag the divergence. Reviewer #3's concern is structural pedagogy; App Tester would pass without catching any of the P0 issues.
5. **Recommend the PM also dispatch an Investigator** to confirm whether the grading rubric (the `Lab 8.pdf`) requires the template HMM. If yes, P0-3's fix becomes "add a warning and reconcile in DOCUMENT.md" rather than "swap defaults". This determines which of the two P0-3 fix paths is correct.

**DOCUMENT.md updated:** N/A for QA / Reviewer #3.
