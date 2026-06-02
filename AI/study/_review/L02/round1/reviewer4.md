# Reviewer #4 — Exam Readiness (Lecture 2, Round 1)

**Reviewer lens:** I read this chapter as someone walking into a final exam. My job is to imagine the 10 plausible exam questions a SDU AI lecturer would ask on this material, then check whether a student could answer EVERY ONE of them using ONLY this chapter — no slides, no textbook, no Google. I am being deliberately harsh. The user said: *"i dont want to come back from the exam and say that you guys missed something!"*

---

## VERDICT: **NEEDS_REVISION**

The chapter is broadly good and pedagogically strong, but has several exam-relevant gaps:
a real ambiguity in the §5.2 classification table that contradicts the source slide,
a missing worked PEAS example (spam filter PEAS is given but never *worked* end-to-end as a template the way the taxi one is),
no quantitative worked example of the table-driven blow-up (students will be asked "how many rows in the table for T=4 steps?"),
no concrete cheat-sheet entry for the *agent-type ↔ minimum-environment* mapping (despite §5.4 being explicitly labelled "exam-quotable"),
and several common-pitfall holes around things every SDU past-exam-style question loves to hammer (action set inconsistency Suck/Dump/NoOp, "semi-dynamic" terminology, the *competitive vs cooperative* multi-agent split).

The cheat sheet also drops two facts that students will be asked about: the 64-environment-type count, and the agent-type → environment mapping.

Below: 10 imagined exam questions, then P0/P1/P2 findings, then evidence.

---

## 10 EXAM QUESTIONS I SIMULATED

1. **Define agent, agent function, agent program. State the slogan that connects them.** → Answerable from §3.1, §3.2, §8.
2. **Give the formal definition of a rational agent. Why does this not imply omniscience?** → Answerable from §3.3, §6 pitfall 1.
3. **Specify the PEAS for a [vacuum cleaner / spam filter / chess robot / medical diagnosis agent].** → Partially answerable. Two PEAS examples (taxi, spam filter) given. But **no PEAS is given for the running vacuum agent itself** — a glaring omission given the vacuum is the running example.
4. **Classify [Solitaire / Poker / Sudoku / a robot soccer match / a thermostat] along the six environment dimensions.** → Answerable for the four slide-23 examples and Solitaire (§5.2). Borderline for other plausible exam targets.
5. **Why is the table-driven agent infeasible? Quantify the table size for a vacuum agent with 4 distinct percepts after T = 5 time steps.** → **Not answerable.** The chapter says "$|P|^T$ rows" but never plugs in numbers. Students will trip on this.
6. **Draw the block diagram of a model-based reflex agent and label every box. Explain the role of the transition model and sensor model.** → Answerable from §4.3 (figure embedded). But "sensor model" is introduced in the chapter even though the slide does NOT use that term — a divergence from source that could cost marks if exam wording is "what does the source slide call the second model?". Flagged below.
7. **Distinguish the four components of a learning agent and explain the role of each using the automated-taxi example.** → Answerable from §4.6 with the slide-36 taxi example. Good.
8. **Is the slide-7 vacuum agent rational? Under which performance measures is it rational and under which is it not?** → Answerable from §3.3 and §5.1. Good.
9. **What is the difference between fully observable and "the agent knows everything"? Give an example where these come apart.** → Answerable from §6 pitfall 3. Good.
10. **For each agent type in the hierarchy, state the minimum environment requirement.** → Answerable from §5.4 — **but the table contains a debatable claim (simple reflex needs "episodic")** that doesn't match the source slides verbatim. Flagged below as P1.

**Coverage rate: 7/10 fully answerable, 3/10 partial or with traps.** Not good enough.

---

## P0 — MUST FIX (blocks approval)

### P0-1. §5.2 classification of "Word-jumble" contradicts slide 23 on Observability AND Episodicity, in a way students WILL be tested on.

Lines 895–902 of `study/lectures/L02-Agents.md`. The chapter's table says:

| Word-jumble | Chess-clock | Scrabble | Driving |
|---|---|---|---|
| Fully | Fully | Partially | Partially |
| ...Episodic | Sequential | Sequential | Sequential |

But on slide 23 of the source PDF (verified by direct PDF read), Scrabble is listed as **Static**, while the chapter table (line 900) also says Scrabble is **Static** — that part is correct. **However**, the more important issue is the chapter's narrative on Solitaire (line 928): the chapter calls Solitaire *"partially observable, stochastic, sequential, static, discrete, single-agent"* but says shuffle gives stochasticity — this is fine **but inconsistent with the chapter's own claim about Word-jumble being deterministic**. A word jumble's *initial scramble* is just as random as a Klondike shuffle; the chapter must explain why one counts as "deterministic" and the other as "stochastic". As written, a student following the chapter's own reasoning will get either answer marked wrong depending on which the examiner privileges.

**Fix:** add an explicit "what counts as randomness for environment-typing purposes" note: by convention, randomness in the *initial state* (one-shot scramble or shuffle, known to the agent once revealed) is **not** what makes an environment stochastic — only randomness in the *transition* from state to state is. Then state explicitly that under this convention both word-jumble and solitaire-after-deal are deterministic. The chapter currently calls one deterministic and the other stochastic without explaining the discrepancy.

### P0-2. The action set Suck / Right / Left / NoOp / **Dump** is inconsistently presented and never explained.

- Slide 7 (source): actions are `Left, Right, Suck, NoOp` (four).
- Slide 11 (source): actions become `Left, Right, Suck, Dump, NoOp` (five — `Dump` appears).
- Chapter line 330: lists `Left, Right, Suck, NoOp` and parenthetically says *"on slide 11 the action set is extended with `Dump`"*.

`Dump` is never defined anywhere. The chapter does not say what `Dump` *does*. A student asked "list the action set of the slide-11 vacuum agent and define each action" will fail on `Dump`. The lecturer clearly thinks dumping (= depositing collected dirt in a designated cell) is part of the world — this is a totally plausible variant exam question.

**Fix:** add a one-sentence definition of `Dump` (best guess: empty the dust container at a designated location) AND flag that the lecture is silent on its semantics so the exam might define it either way. A reader should not need to guess what an action does.

### P0-3. The table-driven blow-up is qualitative only — no numbers, no worked example.

§4.1 (lines 598–628) says "the table has $|P|^T$ rows — exponential in time" and "out of memory." This is the kind of slide that gets paraphrased into "calculate the table size for the vacuum agent over 4 time steps" on an exam. The chapter never does this calculation.

**Fix:** add a worked numeric example. For the slide-7 vacuum world, $|P| = 4$ (percepts `[A,Clean], [A,Dirty], [B,Clean], [B,Dirty]`). After $T$ steps the table has $\sum_{t=1}^{T} 4^t$ rows (one row per possible sequence of length up to T). Show e.g. $T=4 \Rightarrow 4 + 16 + 64 + 256 = 340$ rows; $T=10 \Rightarrow \approx 1.4$M rows; $T=20$ blows past $10^{12}$. This makes "astronomical" concrete and gives the student a template for the exam variant.

### P0-4. Missing: PEAS of the vacuum agent — the lecture's running example.

The chapter writes PEAS for the taxi (§3.5) and the spam filter (§3.5). It never writes PEAS for the **vacuum agent**, even though the vacuum is the running example of §3.2, §3.3, §4.2, §4.3, §5.1. A frequent exam question is *"specify the PEAS of the vacuum agent of slide 7"*. A student would have to fabricate this from scratch under exam pressure.

**Fix:** add a third PEAS box in §3.5 for the vacuum agent. P: amount of dirt cleaned over horizon, possibly minus energy and noise. E: two cells A and B, each clean or dirty. A: Left, Right, Suck (optionally Dump, NoOp). S: location sensor + dirt sensor.

---

## P1 — SHOULD FIX (requested, not blocking)

### P1-1. §5.4 "Minimum environment requirements" table contains a claim that isn't supported by the slides.

Line 957: *"Simple reflex (§4.2) | Fully observable, episodic"*. The source slide 27 says "environment needs to be fully-observable" but does NOT add "episodic". A simple reflex agent can work fine in a *sequential* but fully-observable environment as long as the reflex is correct for every state (e.g. a chess-playing reflex agent that has the full board state). The chapter adds "episodic" without justification.

**Fix:** drop "episodic" from the simple-reflex row, or add a justifying sentence ("we require episodic because otherwise past percepts would matter") and be honest that this is a *practical* requirement, not a *formal* one.

### P1-2. "Sensor model" appears in §4.3 (line 689) but the source slide 29/30 does not use this term.

The chapter introduces *transition model* (which the slide does name as "model" / "how the next state depends on current state and action") AND a separate *sensor model* (which is in textbook Russell-Norvig but not in *this* lecture's slides). If the exam asks "what are the two models maintained by a model-based reflex agent according to the lecture?" the chapter answer (transition + sensor) might be marked partially wrong because the slide only names one.

**Fix:** mark the sensor-model addition as *"(introduced in Russell-Norvig 4th ed., not on slide 29 — included here for clarity)"* so the student knows which is slide-quotable and which is auxiliary.

### P1-3. Cheat sheet (§8) omits the agent-type → minimum-environment mapping table.

§5.4 is explicitly described as "exam-quotable" (line 963) but its content is not echoed in the cheat sheet. A one-page cheat sheet review just before the exam is when this table is most useful. It should appear in §8.

**Fix:** add the §5.4 table to §8.

### P1-4. Cheat sheet omits the $2^6 = 64$ environment-types count.

§3.6 (line 476) notes "$2^6 = 64$ types of environment". This is a one-line fact that exam writers love. Not in the cheat sheet.

**Fix:** add a one-liner in §8 under "Environment types".

### P1-5. Common Pitfalls §6 is missing "competitive vs cooperative" multi-agent split.

§3.6.6 (line 562) mentions *cooperative* vs *competitive* multi-agent in one sentence. This distinction is exam-targetable ("classify Pac-Man vs the ghosts: cooperative or competitive?"). The Pitfalls section never reinforces it.

**Fix:** add to §6 pitfall 7 (or as new pitfall 13): *"Multi-agent is not the end of the question — the examiner may then ask cooperative vs competitive. Same environment dimensions, different sub-classification. Adversarial search (L06) lives in the competitive corner; multi-robot warehouse logistics is the cooperative corner."*

### P1-6. Common Pitfalls §6 is missing "semi-dynamic" terminology.

§3.6.4 (line 533–535) parenthetically introduces "semi-dynamic" (world static but performance measure time-dependent, e.g. chess with a clock). This is a textbook term and a likely exam trap ("is chess-with-clock dynamic or static? — actually it's *semi-dynamic*, depending on convention used"). It is buried in §3.6.4 and never echoed in §6 or §8.

**Fix:** add a pitfall in §6 and a one-liner in §8: *"semi-dynamic = world static, but score depends on elapsed time. Chess-with-clock is the canonical example."*

### P1-7. Worked example §5.2 — "Chess-with-clock" cell explanation contradicts itself.

Line 911–914: *"Chess with a clock flips just one dimension compared to chess — dynamic — because the clock changes the state of the world while the agent thinks."* But the chapter has just defined the more nuanced term "semi-dynamic" in §3.6.4 for exactly this case. So the §5.2 description ("dynamic") and the §3.6.4 description ("semi-dynamic") of the same example are inconsistent.

**Fix:** in §5.2 add: *"Slide 23 calls it 'Dynamic' for simplicity; the textbook would say 'semi-dynamic'. Either answer is defensible on the exam if you cite the convention."*

### P1-8. No worked PEAS for a non-trivial robotics agent.

The two PEAS examples (taxi, spam filter) are both "easy to imagine" agents. SDU exams in this course have historically asked for PEAS of agents like *"medical diagnosis system"*, *"interactive English tutor"*, or *"part-picking robot"* — drawing on Russell-Norvig's PEAS table (which the lecturer almost certainly has in mind). The chapter gives no template for these less-physical agents.

**Fix:** add at least one extra PEAS example in §5.3 — e.g. a medical diagnosis agent (P: maximise correct diagnoses; E: patient records, lab results, patients; A: questions to ask, tests to order, treatments to recommend; S: keyboard input from patient and clinician). This is a textbook example and is exam-likely.

### P1-9. The agent function table on slide 9 should be discussed as a *partial* specification, not just shown.

Lines 308–316 (figure embed) show slide 9's table but never address the obvious question: *"why does the table show duplicate rows like `[A,Clean]` and `[A,Clean], [A,Clean]` mapping to `Right`?"*. The answer is that the agent function is keyed on the *entire history* (not just the current percept), and these rows happen to map to the same action — which is what makes this *particular* function expressible as a simple reflex. A student looking at the table will be confused without this clarification.

**Fix:** add a one-paragraph note under the slide-9 figure explaining (a) why the table has rows of variable length, (b) why two rows with the same current percept can disagree (they would, in a non-reflex function), (c) that the slide-9 table happens to ignore history, making it realisable by a reflex agent.

### P1-10. Worked Example 5.1 doesn't actually evaluate rationality formally.

§5.1 says the rule "does well" under one measure and is "mediocre" under another, but never writes down an expected-utility calculation or even a counting argument. An exam variant might ask "compute the expected performance of the rule under measure M over horizon T=5". Chapter gives no template for this.

**Fix:** add a numeric mini-calculation. E.g. starting state `(A,Dirty,B,Dirty)`, performance = (#clean-cells at t=5) summed: t1 Suck→(A,clean,B,dirty), t2 Right→(B,dirty), t3 Suck→(B,clean), then Left,Right,Left,... = 2 clean cells from t3 onward; total performance = 0+1+2+2+2 = 7 (or whatever the metric is). Make the student practice the type of arithmetic the exam will ask for.

### P1-11. The "single-agent vs multi-agent" criterion is under-specified.

§3.6.6 (line 559) defines multi-agent as "an agent operating by itself" / "many independent decision-makers." But the pitfall (§6 pitfall 7, line 1007–1012) qualifies this with "must affect the performance measure". The pitfall is the correct definition; the §3.6.6 main text is wrong-ish. Students reading §3.6 first will lock in the wrong criterion.

**Fix:** move/duplicate the "affects performance measure" qualifier into §3.6.6 itself, not just §6.

---

## P2 — NICE TO HAVE

### P2-1. The summary slide 37 quotation is the most likely "fill in the blank" exam question on this lecture. Worth bolding harder.

Lines 1147–1149 already include it. Could be boxed/emphasised. Suggest a callout block at the very top and very bottom of §8.

### P2-2. Add a one-line "exam tip" pointing out that the lecturer's table on slide 23 is essentially a memorisation target.

Students should be told: "if you remember nothing else from this lecture, memorise slide 23's table." The chapter shows it (line 891) but doesn't flag its importance.

### P2-3. The §3.7 hierarchy figure (slide 25) is described but the §3.7 prose doesn't quite match it.

Slide 25 has FIVE rows: (1) Table-driven, (2) Simple reflex, (3) Agents with memory, (4) Agents with goals, (5) Utility-based. The chapter §4 has SIX subsections (§4.1–§4.6) because it adds Learning agent. The chapter should mention that Learning agent is **not in the slide-25 hierarchy** — it is added separately on slide 33+ and is "orthogonal" (correctly noted in cheat sheet line 1165, but not in §3.7).

**Fix:** add to §3.7: *"Note: the slide-25 hierarchy has five rows. The learning agent of §4.6 is an orthogonal extension introduced on slide 33, not a sixth rung of the ladder."*

### P2-4. The expected-utility formula in §3.3 uses $\mathbb{E}[U(\text{action})]$ but in §4.5 uses $\arg\max_a \mathbb{E}[U(\text{Result}(s,a))]$.

The notation `Result(state, a)` is introduced without definition. It's standard Russell-Norvig but should be glossed in this lecture's chapter for clarity. A student asked to write the rational-action equation might use either form.

**Fix:** one-line gloss after equation (line 765): "where `Result(s,a)` is the random variable describing the state resulting from taking action $a$ in state $s$."

### P2-5. No explicit mention that "the agent boundary is a modelling choice".

This is a Russell-Norvig classic. Whether the *sensor*'s noise is "inside the agent" or "inside the environment" is a design choice; the same physical setup can be modelled either way. Not asked often, but a "discuss" question could target it.

### P2-6. The lecture's slide 36 example ("a quick left turn across three lanes... shocking language") is funny and memorable — the chapter quotes it. Good. Keep.

### P2-7. The pitfall "rational ≠ omniscient" is implicit in pitfall 1 but not labelled with the standard textbook phrase "rationality is not omniscience".

Russell-Norvig students will recognise the phrase. Worth using verbatim.

---

## EVIDENCE

**Source PDF read:** all 38 slides via direct PDF read (slides 1–38, including blank title/closing slides).

**Chapter sections inspected:**
- §1 Overview (lines 15–53): adequate.
- §2 Analogies (lines 57–233): strong, no findings.
- §3.1 Agent and environment (lines 238–271): no findings.
- §3.2 Percept/sequence/function/program (lines 273–346): see P1-9.
- §3.3 Rationality and performance measure (lines 348–393): no major findings.
- §3.4 Autonomy (lines 396–423): no findings.
- §3.5 PEAS (lines 426–459): see P0-4 (missing vacuum PEAS), P1-8 (need extra example).
- §3.6 Environment types (lines 462–569): see P1-5, P1-6, P1-11.
- §3.7 Hierarchy (lines 572–588): see P2-3.
- §4.1 Table-driven (lines 598–628): see P0-3.
- §4.2 Simple reflex (lines 631–676): no findings.
- §4.3 Model-based reflex (lines 678–721): see P1-2.
- §4.4 Goal-based (lines 723–753): no findings.
- §4.5 Utility-based (lines 755–787): see P2-4.
- §4.6 Learning agent (lines 789–830): no findings (strong section).
- §5.1 Worked: designing vacuum (lines 836–878): see P1-10.
- §5.2 Worked: classifying environments (lines 880–935): see P0-1, P1-7.
- §5.3 PEAS — taxi (lines 937–951): no new findings beyond P0-4/P1-8.
- §5.4 Agent-type ↔ environment (lines 953–964): see P1-1.
- §6 Common Pitfalls (lines 968–1041): see P1-5, P1-6, P2-7. 12 pitfalls is decent count; quality good.
- §7 Connections (lines 1044–1093): adequate.
- §8 Cheat sheet (lines 1097–1174): see P1-3, P1-4, P2-1.

**Cross-checked against source slides:**
- Slide 7 action set vs slide 11 action set: confirmed `Dump` appears on slide 11 only (P0-2).
- Slide 23 table: chapter reproduces correctly but explanatory prose has P0-1 inconsistency.
- Slide 25 hierarchy: chapter §3.7 reproduces; learning agent correctly *not* on slide 25 (P2-3 about clarifying this).
- Slide 27 simple-reflex requirement: source says "fully observable" — chapter §5.4 adds "episodic" without warrant (P1-1).
- Slide 29/30 model-based: source says one *model*; chapter adds sensor model (P1-2).
- Slide 37 summary: quoted faithfully in chapter §8 (good).

**10-question coverage test:** 7/10 fully passable, 3/10 partial/risky. After all P0/P1 fixes I project 10/10.

---

## Report to PM

**Assignment recap:** Lecture Reviewer #4 (Exam Readiness lens) on artifact L02 Round 1 — chapter at `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L02-Agents.md` against source `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture2-Introduction to Agents.pdf`.

**Status:** NEEDS_REVISION. 4 P0, 11 P1, 7 P2. Most fixes are short additions, not rewrites — chapter is structurally sound.

**Key concerns / risks:**
- **P0-1 (deterministic vs stochastic for one-shot randomness):** real ambiguity that will cost students marks. Must be resolved before lock.
- **P0-2 (Dump action undefined):** chapter mentions Dump but never says what it does — naked gap.
- **P0-3 (no numeric table blow-up):** an obvious exam-prep gap; trivial to add.
- **P0-4 (vacuum PEAS missing):** the *running example* of the lecture has no PEAS write-up. Add it.
- **P1-1 (simple reflex needs "episodic"):** chapter overclaims; trim or justify.
- **P1-2 (sensor model not in source):** flag as auxiliary so students don't write slide-non-quotable material as gospel.
- **P1-7 (chess-with-clock dynamic vs semi-dynamic):** chapter inconsistent with itself.

**What PM should do next:** dispatch Reviser with all 4 reviewer reports (this is reviewer #4 of 4); priority is P0-1 through P0-4 and P1-1, P1-2, P1-7 since those create genuine exam-mark risk. P1-3, P1-4, P1-5, P1-6 are cheat-sheet additions and very fast. After revision, re-run all 4 reviewers on round 2.

**Out-of-scope observations:**
- The cross-reference into L06 §3.1 "perfect-information vs imperfect-information games" (chapter line 1061) presumes L06 has that section structure. Worth verifying with L06 reviewer once L06 chapter lands.
- The chapter cites slide 36's "shocking language from other drivers" verbatim — fine and memorable, but verify the cross-reference graph notes that this is L02's only direct mention of "exploration vs exploitation" (the precursor to L10's RL coverage). Worth flagging to Index Builder.

**DOCUMENT.md updated:** N/A (review-only).
