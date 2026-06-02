# L02 Round 1 — Reviewer #2 (Mathematical Rigor)

**Artifact:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L02-Agents.md`
**Source PDF:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture2-Introduction to Agents.pdf` (38 slides)
**Lens:** Mathematical rigor — every formula, every index, every assumption, every notational reuse, every typeset symbol.

---

## VERDICT

**NEEDS_REVISION**

Several outright factual mismatches with the source slide deck (most critically, the environment-classification table for Chess-with-a-clock on slide 23 is wrong in the chapter), plus a recurring notational sin: the symbol `P` is silently overloaded between "set of percepts," "percept sequence," and "probability" within a few paragraphs of each other. For an exam where math notation will be graded, this is dangerous. Several formulas are introduced by the chapter that do NOT appear in the source PDF and carry hidden assumptions (i.i.d./exhaustive outcomes, deterministic vs. stochastic `Result`, the domain of `U`) that the chapter does not state.

---

## P0 — MUST FIX (blocks approval)

### P0-1. Environment classification table contradicts slide 23 for "Chess with a clock" (Discrete row)
**Location:** L02-Agents.md §5.2, lines 893–902.
**Source:** PDF page 23 (slide 23) table.
**Issue:** Slide 23 lists Chess-with-a-clock as **Continuous** in the Discrete-vs-Continuous row. The chapter's reproduced table says **Discrete**.

Slide 23 row (verbatim left-to-right, columns = Word-jumble | Chess-with-clock | Scrabble | Autonomous-driving):
```
Discrete:  Discrete   Continuous   Discrete   Continuous
```

Chapter (lines 894–902):
```
| Discrete | Discrete | Discrete | Discrete | Continuous |
```
i.e. Chess-with-clock listed as Discrete.

**Why this is P0:** This is the single most exam-likely table in the lecture (the chapter itself says so at line 887: "This is the most exam-likely figure in the lecture"). A student memorising the chapter table will get the exam answer wrong vs. the lecturer's official answer key.

**Fix:** Change the chapter's Chess-with-clock entry in the Discrete row to "Continuous." Then add a clarifying sentence in the discussion explaining *why* the lecturer marks it continuous (the clock's time evolves continuously even though the game state is discrete) — because the chapter's prose at §5.2 line 913 doubles down on the wrong answer.

### P0-2. §5.2 prose claims chess-with-a-clock "flips just one dimension" — it flips two per the slide
**Location:** L02-Agents.md §5.2, lines 913–914.
**Issue:** Chapter states: *"Chess with a clock flips just one dimension compared to chess — dynamic — because the clock changes the state of the world while the agent thinks. Still discrete, deterministic, multi-agent, sequential."*

Per slide 23, Chess-with-a-clock flips TWO dimensions vs. plain chess: Static→Dynamic AND Discrete→Continuous. The chapter explicitly asserts "Still discrete," which contradicts the slide and reinforces the error in P0-1.

**Fix:** Rewrite to: *"Chess with a clock flips two dimensions vs. plain chess: it becomes dynamic (clock ticks during deliberation) and the lecturer also treats it as continuous because time itself evolves continuously. Still deterministic, multi-agent, sequential."*

### P0-3. Symbol `P` is overloaded three times within five sections — no re-declaration
**Location:**
- §3.2 line 283 / 287: `P^*` introduced as "the percept sequence" (but used as a domain set in `f : P^* \to A`).
- §3.3 line 381: `P(\text{outcome} \mid \text{action})` — `P` reused for probability with no re-declaration.
- §4.1 line 617: `|P|^T` — `P` reused as "set of percepts" with no declaration that `P` now means a set.
- §8 line 1126: `P(o \mid a)` — probability again.

**Issue:** A student reading §3.3 immediately after §3.2 sees the same letter `P` carrying three different meanings: a sequence, the domain of all sequences, and a probability mass function. The chapter never re-declares or disambiguates. On an exam math question this kind of overloading is the single fastest way to lose points.

**Fix:** Either
(a) introduce `\mathcal{P}` for the set of percepts so that `P^* = \mathcal{P}^*` (Kleene star) is the set of finite sequences over `\mathcal{P}`, and reserve `P(\cdot)` exclusively for probability; or
(b) introduce `\Pi` for percept and write `\Pi^*` for the set of percept sequences, freeing `P` for probability throughout.
Add a one-line "Notation" footnote in §3.2 making the convention explicit.

### P0-4. `P^*` is conflated with "a single percept sequence" in §3.2, then used as a domain in the very next equation
**Location:** §3.2 lines 281–287.
**Issue:** Line 281–283: "A **percept sequence** is the complete history... Written $P^{*}$." This wording says *one* percept sequence is denoted `P^*`. But the next equation, `f : P^{*} \to A`, uses `P^*` as the *domain* (the set of all percept sequences). These two readings are incompatible: a function maps from a set, not from a single element.

**Fix:** Replace lines 281–287 with:
> Let `\mathcal{P}` denote the set of possible percepts. A **percept sequence** is a finite sequence $p_1 p_2 \dots p_t \in \mathcal{P}^*$ (Kleene star = the set of all finite sequences over `\mathcal{P}`). The **agent function** is then `f : \mathcal{P}^* \to A`, mapping any percept history to a next action.

This also fixes P0-3 in one stroke.

---

## P1 — SHOULD FIX (requested, not blocking)

### P1-1. Expected-utility formula in §3.3 has unstated assumptions (and is not in the source PDF)
**Location:** §3.3 line 381.
**Issue:** The chapter writes
$$\mathbb{E}[U(\text{action})] = \sum_{\text{outcome}} P(\text{outcome} \mid \text{action}) \cdot U(\text{outcome}).$$
Two dropped assumptions a student must know:
1. The sum is implicitly over the **partition** of all possible outcomes (mutually exclusive, exhaustive). The chapter never says this.
2. Outcomes are assumed **discrete/countable**; for continuous outcomes this becomes an integral. Not stated.
3. The sum index is the prose word `outcome`, not a bound variable — ambiguous when later asked "sum over what?"

Additionally, this formula does NOT appear in the source PDF (slide 10 only says "expected to maximize its performance measure"). Adding it is fine pedagogically but it must be airtight.

**Fix:** Rewrite as
$$\mathbb{E}[U \mid a] \;=\; \sum_{o \in \Omega} P(o \mid a)\, U(o), \qquad \text{where } \Omega \text{ is the set of mutually exclusive, exhaustive outcomes of action } a.$$
Add a sentence: "When outcomes are continuous, replace the sum with an integral."

### P1-2. `Result(state, a)` in §4.5 utility-based argmax is undeclared and its determinism is unspecified
**Location:** §4.5 line 765:
$$a^{*} = \arg\max_{a \in A} \mathbb{E}\bigl[U(\text{Result}(\text{state}, a))\bigr].$$
**Issue:**
- `Result` is not introduced anywhere in L02 (it's an L03 concept — a transition function).
- If `Result` is deterministic, the outer `\mathbb{E}[\cdot]` is redundant and confusing. If stochastic, then `Result(state, a)` is a random variable and that fact must be stated.
- The signature of `Result` is missing: `Result : S \times A \to S` (deterministic) or `Result : S \times A \to \Delta(S)` (stochastic).

**Fix:** Add a one-line preface:
> Let `Result(s, a)` denote the (possibly stochastic) successor state when action `a` is taken in state `s`. If the environment is deterministic, `\mathbb{E}[\cdot]` is a no-op. If stochastic, `Result(s, a)` is a random variable distributed according to the transition model `P(s' \mid s, a)`, and the expectation expands to $\sum_{s'} P(s' \mid s, a)\, U(s')$.

### P1-3. Utility function signature `U : S \to \mathbb{R}` — `S` is never declared in L02
**Location:** §4.5 line 760, cheat-sheet §8 line 1123.
**Issue:** Both places write `U : S \to \mathbb{R}` but `S` is undefined in this lecture. (`S` = set of environment states is the convention, but the chapter never says so.)
**Fix:** In §4.5, write "Let $S$ denote the set of environment states." Then `U : S \to \mathbb{R}`. Note that slide 32 says U may take "(sequence of) state(s)" as input — so strictly the chapter should write `U : S \cup S^* \to \mathbb{R}` or explicitly flag that the slide is ambiguous on whether the domain is single-states or state-sequences.

### P1-4. Table-driven agent size formula `|P|^T` understates the count by ignoring shorter sequences
**Location:** §4.1 line 617:
> With $|P|$ possible percepts and $T$ time steps, the table has $|P|^T$ rows — exponential in time.

**Issue:** A table-driven agent stores actions for *all* percept sequences of length **1 through T**, not only sequences of length exactly T. The correct count is
$$\sum_{t=1}^{T} |P|^t \;=\; |P| \cdot \frac{|P|^T - 1}{|P| - 1}$$
(geometric series). The chapter's `|P|^T` is the dominant term but is technically wrong — an exam question asking for the exact size would reject `|P|^T`.

Additionally, `P` here is being used as "the set of percepts" — a different meaning from the `P^*` defined earlier in §3.2. (See P0-3.)

**Fix:** Rewrite as
> With $|\mathcal{P}|$ distinct percepts and a lifespan of $T$ steps, the table must store one action per percept sequence of length 1, 2, …, T. The total row count is
$$\sum_{t=1}^{T} |\mathcal{P}|^t \;=\; \mathcal{O}\bigl(|\mathcal{P}|^T\bigr)$$
— exponential in $T$.

### P1-5. Inconsistent argument naming in UPDATE-STATE between prose and pseudocode
**Location:** §4.3 line 693 (prose) vs line 705 (pseudocode).
**Issue:** The prose equation writes
$$\text{state} \leftarrow \text{UPDATE-STATE}(\text{state}, \text{last action}, \text{percept}, \text{model})$$
but the pseudocode immediately below writes `UPDATE-STATE(state, action, percept, model)` — `action` vs. `last action`. The pseudocode then declares the static var as `action, the most recent action`, so semantically they agree, but textually the names differ.

**Fix:** Use one name consistently. Either rename the pseudocode static var to `last_action`, or change the prose equation argument to `action` (and keep the gloss "(= the most recent action)").

### P1-6. PDF uses lowercase `p*`, chapter silently capitalises to `P^*` without flagging
**Location:** §3.2 line 287; §8 line 1107.
**Issue:** Slide 6 of the PDF literally writes `f: p* → A` (lowercase p). The chapter uses `f : P^* \to A` (capital P with Kleene star). The modernisation is fine, but a student cross-referencing the slide text will be confused, especially because the chapter never flags that it has normalised the notation.
**Fix:** Add a footnote at the first occurrence: "Slide 6 of the source writes this as `f: p* → A`; we use the conventional capital-letter notation `\mathcal{P}^*` for the Kleene closure of the percept set."

### P1-7. Cheat-sheet expected-utility formula reuses bound variable `o` and `a` without declaration
**Location:** §8 line 1126:
$$\mathbb{E}[U(a)] = \sum_o P(o \mid a)\,U(o)$$
**Issue:** `o` never introduced, `a` overloaded with §4.5's `a^*`, summation index not bound to a set. Cheat sheets are exactly where students copy formulas verbatim — this needs to be the cleanest formula in the chapter.
**Fix:**
$$\mathbb{E}[U \mid a] \;=\; \sum_{o \in \Omega(a)} P(o \mid a)\, U(o)$$
where `\Omega(a)` is the set of possible outcomes when action `a` is taken.

### P1-8. §5.4 "minimum environment requirements" table adds claims not in the source
**Location:** §5.4 lines 956–961.
**Issue:** The chapter attributes specific environment requirements to each agent type (e.g. "Simple reflex | Fully observable, episodic"). The PDF (slide 27) only says simple reflex requires "fully-observable" — "episodic" is the chapter's addition (from the Russell & Norvig textbook). This is a *mathematical* claim about preconditions and the chapter sources it to slides 27/29/31/32/33, but slide 27 does not state the episodic requirement.

**Fix:** Either drop "episodic" from the simple-reflex row, or change the attribution from "the mapping comes directly from slides 27, 29, 31, 32, 33" to "the mapping is the standard Russell & Norvig synthesis; slides 27/29/31/32/33 give the partial constraints."

---

## P2 — NICE TO HAVE

### P2-1. `\arg\max` rendering
**Location:** §4.5 line 765.
The chapter uses `\arg\max_{a \in A}`. KaTeX and MathJax render this correctly, but for the safest cross-renderer behaviour prefer `\operatorname*{arg\,max}_{a \in A}` (which guarantees the subscript ends up below the operator in display mode).

### P2-2. `\mathbb{E}[U(\text{action})]` vs `\mathbb{E}[U \mid \text{action}]`
**Location:** §3.3 line 381.
Conditional-expectation notation `\mathbb{E}[U \mid a]` is more idiomatic when conditioning on a chosen action and reads better on the exam. Optional but cleaner.

### P2-3. State-set declaration
**Location:** §4.5.
When you fix P1-3, consider extending: introduce $S$ globally (it's reused in L03, L06, L09a, L09b, L10). A one-line shared-notation footnote at the top of §3 would prevent the same issue from recurring in every later chapter.

### P2-4. §4.1 lookup-table pseudocode comment "initially fully specified" is silently ambitious
**Location:** §4.1 line 609.
The static var `table` is described as "initially fully specified" — but the whole point of §4.1 is that a full specification is infeasible. A sentence acknowledging "in principle fully specified, in practice impossible — see below" would soften the contradiction.

### P2-5. §4.4 goal-based pseudocode mixes OO and procedural style
**Location:** §4.4 lines 736–739.
`model.predict(state, a)` uses dot-notation; the rest of the chapter uses procedural pseudocode (`UPDATE-STATE(...)`, `RULE-MATCH(...)`). Pick one style. Suggest `PREDICT(state, a, model)` for consistency.

### P2-6. Slide 28 pseudocode bug inherited silently
**Location:** §4.2 lines 655–661.
The PDF's slide 28 pseudocode reads `rule ← RULE-MATCH(state, rules)` but never assigns `state` inside the function. The chapter copies this verbatim and offers no remark. A two-line footnote — "Slide 28 omits the `state ← INTERPRET-INPUT(percept)` line that appears in slide 27's version; we treat them as equivalent" — would save a careful student five minutes of confusion.

### P2-7. §3.6 "$2^6 = 64$ environment types"
**Location:** §3.6 line 476.
True but glib — the six dimensions are not perfectly independent in practice (e.g. fully-observable + multi-agent + stochastic is *common*; fully-observable + stochastic + episodic + multi-agent + continuous + single-agent is essentially empty). A throwaway "in principle" before "$2^6 = 64$" would forestall an exam answer that quotes 64 as a meaningful number.

---

## EVIDENCE

**Sections of the chapter inspected against the source:**

| Chapter section | Source slides | Math/notation cross-checked |
|---|---|---|
| §3.1 Agent and environment | Slides 4–5 | Definition prose only; no formulas. |
| §3.2 Percept / agent function | Slide 6 (terminology), slides 7–9 (example) | **P0-3, P0-4, P1-6**: `P^*` notation. |
| §3.3 Rationality, performance measure | Slide 10–12 | **P1-1**: expected-utility formula (not in PDF). |
| §3.4 Autonomy | Slide 13 | Definition synthesis OK. |
| §3.5 PEAS | Slides 14–15 | Verbatim. |
| §3.6 Environment types | Slides 16–22, 24 | $2^6 = 64$ check (P2-7). |
| §4.1 Table-driven | Slides 25–26 | **P1-4**: $|P|^T$ formula. |
| §4.2 Simple reflex | Slides 27–28 | Pseudocode `state` undefined (P2-6). |
| §4.3 Model-based reflex | Slides 29–30 | **P1-5**: UPDATE-STATE arg names. |
| §4.4 Goal-based | Slide 31 | Pseudocode style (P2-5). |
| §4.5 Utility-based | Slide 32 | **P1-2, P1-3**: `Result`, `U:S→ℝ`. |
| §4.6 Learning agent | Slides 33–36 | No formulas; OK. |
| §5.1 Vacuum worked example | Slides 7, 11–12 | 4-row table matches slide 9. |
| **§5.2 Four-environment table** | **Slide 23** | **P0-1, P0-2**: Chess-with-clock = Continuous, not Discrete. |
| §5.4 Agent type → environment | Slides 27, 29, 31, 32, 33 | **P1-8**: extra "episodic" claim. |
| §8 Cheat sheet | Recap | **P1-3, P1-7**: formulas. |

**Specific PDF cross-references performed:**
- Slide 6 (PDF page 6): "Agent function: maps any given percept sequence to an action [f: p* → A]" — lowercase `p*`. Chapter uses `P^*`.
- Slide 10 (PDF page 10): "Select actions expected to maximize its performance measure" — no probability formula given. Chapter adds expected-utility sum.
- Slide 23 (PDF page 23): Discrete row reads `Discrete  Continuous  Discrete  Continuous` left-to-right. Chapter table has Chess-with-clock as Discrete (wrong).
- Slide 30 (PDF page 30): pseudocode argument is `action` not `last action`. Chapter prose calls it `last action`.
- Slide 32 (PDF page 32): "mapping (sequence of) state(s) onto a real number" — chapter writes `U : S \to \mathbb{R}` only, dropping the sequence option without flagging.

---

## Report to PM

**Assignment recap:** Reviewed L02-Agents.md round 1 under the Mathematical Rigor lens, per spec §7.1 reviewer #2.
**Status:** NEEDS_REVISION (verdict above).
**P0 findings:** 4 — most importantly the slide-23 environment-classification table is reproduced incorrectly for Chess-with-a-clock (P0-1, P0-2), and the symbol `P` is overloaded three times within §3–§4 without re-declaration (P0-3, P0-4).
**P1 findings:** 8 — covering unstated assumptions on the expected-utility sum, missing/undeclared sets (`S`, `\Omega`, `Result`), off-by-one in the table-driven row count, prose↔pseudocode argument-name mismatch, silent capitalisation of `p*` → `P^*`, cheat-sheet bound-variable laxness, and an "episodic" attribution to slide 27 that the slide does not make.
**P2 findings:** 7 — typographic/style nits and one inherited slide-28 pseudocode bug worth a footnote.
**Files inspected:** chapter `study/lectures/L02-Agents.md` (1181 lines), source PDF (38 slides), spec §7.1.
**Out-of-scope observations:** The same `S` / `\mathcal{P}` / probability-`P` notation collision will almost certainly recur in L03 (state set), L06 (utility), L09a (probability + utility together), L09b (HMM transition model). Recommend adding a global notation footnote to `study/_shared/glossary.md` to head this off.
**Concerns / risks:** The Chess-with-clock error is the single highest-impact finding — that table is the exam's most photogenic figure and will likely appear on the test verbatim. If the chapter ships uncorrected, the student gets the question wrong even after studying. P0-1 must land before render.
**What PM should do next:** Dispatch the Reviser with this report (+ reviewers 1, 3, 4). Once P0/P1 items are addressed, re-run the 4-reviewer gate. Particular attention on P0-1/P0-2 cross-checking against slide 23 character-by-character.
**DOCUMENT.md updated:** N/A (Reviewer role; produces review file only).
