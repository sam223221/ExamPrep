# Reviewer #3 — Pedagogical Clarity (incl. Analogies)

**Artifact:** `study/lectures/L02-Agents.md` (Round 1)
**Source:** `Lecture2-Introduction to Agents.pdf` (slides 1–38)
**Lens:** Confused-student reader; analogy enforcement per spec §6.1 / §7.1 Reviewer #3.

---

## VERDICT

**NEEDS_REVISION**

The chapter is unusually strong on analogies — every major concept gets one, most with "where the analogy breaks down" caveats, and §2 cross-links into §3 are largely present. That is genuine craftsmanship and the chapter is *close* to passing my lens.

But there are blocking pedagogical gaps:

1. A **forward-reference avalanche** in the first three sections: §1 names "PEAS", "five-step hierarchy", "L03–L12", and §2 names "model-based reflex agent" and "Critic/Learning element/Performance element/Problem generator" — all before any of them are defined. A confused first-time student will bounce off this wall.
2. **Expected utility is hand-waved** (§3.3 quotes the formula but never explains what `outcome` ranges over for the vacuum world, and never grounds the analogy "play the odds" in any numeric example).
3. **Rational-agent analogy uses a domain (chess) that hasn't been introduced yet** and that the lecture itself uses as a *different* example (deterministic environment, slide 18). The student will conflate them.
4. **§4.4 Goal-based agent pseudocode is broken** as written ("otherwise plan a sequence of actions" is a comment, not code — and the example only chooses *one* action, contradicting the whole point of "goal-based plans ahead"). The accompanying intuition is therefore wrong: a goal-based agent doesn't just pick the first action whose result is a goal — it *searches*.
5. **Two analogies are too weak / too technical** to fix mis-learning: the "chess-player" rational analogy and the "snapshot / camera-roll" percept analogy each need either a caveat upgrade or replacement (see P1 #1 and #2).
6. **One concept is silently missing an analogy entirely:** "expected utility" is named, formula-dropped, then orphaned. The cheat-sheet adds one bullet but §2 never mentions it. Spec §7.1 requires *every* major concept introduced have an analogy in §2.

Fix the P0s and a confused student can read this top-to-bottom without getting lost. Right now they'll stall at §1 and limp through §3.3 and §4.4.

---

## P0 — MUST FIX (blocks approval)

### P0.1 — Forward-reference avalanche in §1 (lines 41–51)

The "Later lecture" table (lines 41–50) name-drops every later lecture *and* uses jargon students haven't yet learned: "static, deterministic, fully observable, discrete", "stochastic, single-agent", "sequential, partially observable, stochastic", "learning agent of §4.6 made concrete". A confused student opening L02 cold has zero idea what any of those adjectives mean — they get introduced 200+ lines later in §3.6.

**Suggested fix:** either (a) move the table to §7 ("Connections to Other Lectures") where the vocabulary is already in hand, or (b) add a one-line preamble: *"The terms below are introduced in §3.6 — skim the table now, return after reading §3.6."* Option (a) is cleaner.

### P0.2 — §2 introduces "model-based reflex agent" before defining it (lines 178–192)

The analogy section is meant to *precede* formalism. But the "driver in fog" analogy talks about a **model-based reflex agent** as if the reader knows what that is. The full definition isn't until §4.3 (line ~678). A student reading §2 linearly hits "model-based reflex agent" as an opaque label, with no §3 cross-link forward.

**Suggested fix:** in §2 the heading should be *the concept*, not its formal name — e.g. "**Reacting from memory** is like a driver in fog" — and a one-line "we'll formalise this in §4.3 as the **model-based reflex agent**" pointer. Same pattern applies to "simple reflex agent", "goal-based agent", "utility-based agent", "learning agent" (lines 165–232) — all of these label-then-explain. The whole point of §2 is to give intuition *first* and name *second*.

### P0.3 — §2 "learning agent" analogy introduces four technical terms (Critic, Learning element, Performance element, Problem generator) with no prior gloss (lines 220–229)

"That four-part loop is the textbook learning agent" — but the reader has never seen those four labels before. The parenthetical glosses ("**Critic**", "**Learning element**", "**Performance element**", "**Problem generator**") are *terms* not *explanations*. A confused student reads this and learns nothing: they see four bolded words and don't yet know which one judges, which one updates, which one acts.

**Suggested fix:** rewrite as plain-English first: *"An apprentice gets feedback from someone judging their work, internally updates their understanding, applies the improvement next time, and occasionally tries something risky to learn from."* Then in a follow-up sentence: *"These four roles get formal names in §4.6 (Critic, Learning element, Performance element, Problem generator)."* The analogy should land *without* the jargon.

### P0.4 — Rational-agent analogy uses chess as the vehicle, but chess is the canonical *deterministic* example one section later (lines 93–107 vs. line 504)

The §2 analogy says a rational agent "is like a chess player who plays the odds". Two sections later, slide 18 / line 504 declares **checkers** (and by implication chess) **deterministic**: every legal move leads to exactly one resulting position. So the chess-grandmaster-with-odds image actively *misleads* — chess is the domain where you *don't* play the odds (no dice).

A confused student who internalised the chess analogy in §2 will be confused at §3.6.2 ("wait, chess is deterministic — there are no odds?"). The "where the analogy breaks down" caveat doesn't catch this — it talks about psychology and omniscience, not about chess being deterministic.

**Suggested fix:** replace with a stochastic-domain analogy. *"A **rational agent is like a poker player playing the odds**: she makes the bet that has the best expected value given the cards she can see and the cards she has seen, even though any individual hand can still go badly."* Poker is unambiguously stochastic, unambiguously partial-observable, and unambiguously a domain where "expected" matters. Then the breakdown caveat can stay roughly as written.

### P0.5 — §3.3 hand-waves expected utility on the worked vehicle (lines 380–384)

The chapter states:
> Expected utility — the probability-weighted sum of utilities over possible outcomes — is the formal object the rational agent maximises:
> E[U(action)] = sum_outcome P(outcome | action) · U(outcome)

…and stops. For a confused student this is a formula floating in space. What is `outcome` for the vacuum agent? What probabilities? What utilities? The whole chapter so far has used the vacuum world as the running example — and now expected utility is dropped in without instantiating it. The student leaves §3.3 unable to *use* the formula on the vacuum agent.

**Suggested fix:** add a 4–6 line worked instance. Something like: *"In the deterministic vacuum world `Result(state, Suck) = clean(state)` with probability 1, so `E[U(Suck)] = U(clean(state))`. The expectation collapses to the deterministic utility. The expectation only does work once the environment is stochastic — for example if `Suck` succeeds with probability 0.9 and fails (leaves the cell dirty) with probability 0.1: `E[U(Suck)] = 0.9·U(clean) + 0.1·U(dirty)`."* This grounds the formula in the lecture's running example.

Also: the chapter promises "we say more about it in L09a §1" — fine for forward-cross-link, but L09a doesn't exist yet at read-time, so the L02 chapter must stand alone.

### P0.6 — §2 has no analogy for "expected utility" (a major concept)

Concepts named in §1 / §3.3 / §4.5 / cheat-sheet that are introduced in this lecture must each have a §2 analogy (spec §7.1). Expected utility is named (line 380), boxed (line 381), and re-named in the cheat-sheet (line 1126), but never gets a §2 analogy — neither standalone nor folded into the rational-agent analogy. The poker reformulation in P0.4 would naturally cover this (each bet has an expected-value computation), but as the chapter stands the concept is uncovered.

**Suggested fix:** if you take the poker analogy from P0.4, extend it: *"The poker player's mental sum 'how much do I expect to win, weighted by how likely each card-out is' **is expected utility** — the formal version says exactly that."* Then §3.3 can cross-link back.

### P0.7 — §4.4 Goal-based-agent pseudocode is wrong as pedagogy (lines 732–740)

```text
function GOAL-BASED-AGENT(percept) returns an action
    static: state, goal, model
    state ← UPDATE-STATE(state, action, percept, model)
    for each action a do
        predicted_state ← model.predict(state, a)
        if predicted_state ∈ goal then return a
    /* otherwise plan a sequence of actions — that is search (L03) */
```

Three problems for a confused student:

1. **The `static` line names `action` as state, but the function `returns an action` and never assigns one before the predict call** — readers familiar with `REFLEX-AGENT-WITH-STATE` will notice the omission. (You could argue it's the most-recent action, but say so.)
2. **The loop returns the *first* action whose immediate result is a goal state.** That is *not* what a goal-based agent does. A goal-based agent **plans** — it considers sequences. The comment "otherwise plan a sequence of actions — that is search (L03)" admits this but the *code path* never executes it, so the pseudocode contradicts the textual description on line 729 ("asks *what will happen if I take each action?* and *does any of the resulting states match a goal?*"). The lecture itself doesn't show pseudocode for goal-based — slide 31 only shows the block diagram. **Don't invent broken pseudocode that contradicts your own explanation.**
3. The student walks away thinking "goal-based agent = one-step lookahead", which is exactly wrong: it's the architectural setting for *all of search*.

**Suggested fix:** drop the pseudocode entirely (the lecture doesn't have it). Replace with prose: *"The decision procedure is no longer a fixed rule table. Instead the agent uses its model to predict the outcome of each candidate action sequence and picks one that reaches a goal state. Choosing **which** sequence to consider is the search problem of L03."* Or, if pseudocode is wanted, write it honestly as `plan ← SEARCH(state, goal, model); return plan.first()`.

### P0.8 — §2 thermostat analogy and §3.1 don't bridge to the *abstract* loop (lines 64–75 vs. 246–249)

§2 says: "thermostat perceives → decides → acts → senses again" (good). §3.1 says: "An **agent** is anything that can be viewed as perceiving its environment through **sensors** and acting upon that environment through **actuators**." That's a definition not a bridge. The promised "Recall the thermostat analogy" pointer (line 240) doesn't do work — it doesn't say *which part* of the analogy maps to *which part* of the definition.

For a confused student, the bridging move is critical: *"Recall the thermostat: the temperature reading is the **percept**, the thermistor is the **sensor**, the relay command is the **action**, the relay-plus-heater is the **actuator**, and the target temperature is encoded in the **agent function** that maps percept → action."* Without that, §2 and §3.1 read as two unrelated paragraphs.

**Suggested fix:** for each §2 → §3.X cross-link, name the *mapping*, not just the analogy. The same problem exists at §3.2 (line 276), §3.3 (line 350), §3.4 (line 399), §3.5 (line 428), §3.6 (line 463), §4.2 (line 633), §4.3 (line 680), §4.4 (line 726), §4.5 (line 758), §4.6 (line 791) — all of these say "Recall the X analogy from §2" without explaining the mapping. This is the single largest pedagogical lift you can do.

---

## P1 — SHOULD FIX (requested, not blocking)

### P1.1 — "Snapshot / camera roll" analogy is too lossy (lines 109–119)

A camera roll is *literally* a sequence of percepts, so the analogy is barely an analogy — it's just a re-labelling. The "where it breaks down" caveat tries to compensate but ends up saying "nobody really stores the whole camera roll", which is the *point* the analogy was supposed to make vivid. The student gets less intuition than from the formal definition.

**Suggested replacement:** *"A **percept** is like the next frame in a movie — a single instant of input. A **percept sequence** is the whole movie up to now. The agent function is the script the director wrote: 'given the movie so far, here is the next scene'." The mismatch (and the lesson): no agent literally stores the whole movie — it stores a *summary*. The script that works on summaries instead of the full movie is what gets compressed into the agent program (§3.2)."*

This sets up the program-vs-function distinction more naturally.

### P1.2 — "Vending machine" analogy is fine but misses the partial-observability connection (lines 165–177)

The breakdown caveat says "the failure modes are the same — both fail if you need to remember something from earlier (e.g. 'did I already pay?')", which is good. But it doesn't tie back to the formal property that triggers it: *partial observability* (defined later in §3.6.1). A confused student gets the failure mode but not the formal label.

**Suggested addition:** *"In §3.6.1 we'll call this 'partially observable'. The vending machine fails the same way: it can't observe whether you've paid in this transaction — so without memory it can't act correctly."*

### P1.3 — "Performance measure is like a referee" — caveat misses the most common student error (lines 122–134)

The most common student confusion (and the one slide 12 explicitly warns against, line 391) is: *students design performance measures based on what the agent should do (process), not what they want (outcome)*. The §2 caveat talks about "lifetime" and "multiple criteria" — both true — but doesn't flag the design-error trap.

**Suggested addition to caveat:** *"Also: the performance measure must describe **what you want in the world**, not **how the agent should behave**. Saying 'agent should clean every square' is the wrong shape — say 'world should end up with zero dirt'."* This is the exam-quotable warning from slide 12 and deserves to land in §2 too.

### P1.4 — "PEAS is like a one-page brief" caveat is technically true but doesn't help the student (lines 136–146)

The caveat says PEAS is fixed at design time and a freelance brief evolves. Fine — but the trap that students actually hit on exams (and that this chapter warns about at lines 944–950 and 1014–1016) is **confusing sensors with percepts** and **actuators with actions** — the bullets in the freelance brief don't map cleanly onto that, because in a contract you don't usually distinguish "tool" from "what tool produces". So the analogy gives the *labels* P/E/A/S, but doesn't immunise the student against the wrong-column error.

**Suggested addition:** *"Trap: in the freelance brief 'tools' is one entry, but in PEAS we split **devices** (Sensors / Actuators) from **what those devices produce or consume** (percepts / actions). Forgetting this split is the most common PEAS-exam error — see §6 pitfall 8."*

### P1.5 — "Weather forecast" analogy for environment types is weak (lines 148–164)

A weather forecast is fuzzy, multi-dimensional, *and not under your control* — none of which match the six-dimensional formal taxonomy. The caveat acknowledges this. But it leaves the student with *no* mental hook. The whole §3.6 leans on the analogy to organise six independent dimensions, but if the analogy is weak the organisation is weak.

**Suggested replacement:** *"Think of the six environment properties as the **six switches on a job description**: before you can hire (build) the right agent, the recruiter (you) flips each switch left or right. If the 'observability' switch is left ('fully'), a simple-reflex hire might do; if it's right ('partial'), you need a model-based hire (§4.3). Mismatch a switch and the agent will fail in a predictable way." The breakdown caveat: "Real environments sometimes need an intermediate setting (semi-dynamic, see §6 pitfall 5) that the binary switch oversimplifies."*

This gives the student a single mental gesture (flip switches) that maps onto the §3.7 hierarchy choice (which architecture matches which switch positions).

### P1.6 — §3.4 Autonomy: the apprentice analogy isn't recalled correctly (line 399)

The apprentice analogy was originally introduced for the **learning agent** (lines 220–232). Reusing it for *autonomy* (line 399) is fine — autonomy and learning are tightly linked — but the chapter doesn't say so. A student reads §3.4 line 399 and wonders "wait, the apprentice was supposed to map to the learning agent, why is it autonomy now?"

**Suggested fix:** add a sentence: *"The same apprentice analogy works for autonomy because autonomy is exactly the property the learning-agent architecture (§4.6) achieves — see the cross-reference at line 418."*

### P1.7 — §4.5 "When utility-based beats goal-based" is presented as a flat list (lines 774–782); the intuitive *core* is buried

The list of three reasons (multiple goals / conflicting goals / uncertain outcomes) is correct but flat. The intuition is the same in all three: *a goal is a binary yes-no; utility is a real number*. Goal-based answers "did I reach the goal?"; utility-based answers "how good is the state?". The third bullet (expected utility / stochastic) needs `argmax E[U]` to work; the first two only need `argmax U` over reachable goals. The chapter doesn't draw this distinction, but it's the single most exam-quotable shape of the difference.

**Suggested fix:** open §4.5 with the one-sentence essence: *"Goal-based agents answer **yes/no**: did I reach a goal? Utility-based agents answer **how good**: what's the score? That single switch — boolean predicate to real-valued function — is the whole structural difference."*

### P1.8 — "Where the analogy breaks down" is missing for ONE major §2 entry

Re-reading §2:
- Agent (line 71) — ✓ caveat
- Agent function vs program (line 86) — ✓
- Rational agent (line 102) — ✓
- Percept / percept sequence (line 117) — ✓
- Performance measure (line 130) — ✓
- PEAS (line 143) — ✓
- Environment types (line 160) — ✓
- Simple reflex agent (line 172) — ✓
- Model-based reflex agent (line 188) — ✓
- Goal-based agent (line 201) — ✓
- Utility-based agent (line 215) — ✓
- Learning agent (line 230) — ✓

Looks complete. **But none of them appears for "expected utility"** (because expected utility doesn't have its own §2 entry — see P0.6). Fixing P0.6 also fixes this gap.

### P1.9 — Cheat-sheet (§8) analogy reminders don't all match §2

Spec §6.1: *"Each concept on the cheat sheet carries a one-line analogy reminder in italics."*

Check:
- Agent — ✓ "Like a thermostat with a job description"
- Agent function — ✓ "Like a job description"
- Agent program — ✓ "Like the employee doing the job"
- Architecture + Program (line 1110) — **no analogy** (it's a slogan; arguably it doesn't need one)
- Percept / Percept sequence — ✓ "Snapshot / camera roll"
- Rational agent — ✓ "Like a chess player who plays the odds" (must change with P0.4)
- Performance measure — ✓ "Like a referee, not a coach"
- **Utility function — "Like the score on the scoreboard"** ← NEW analogy that wasn't in §2. Inconsistency. Either add to §2 or remove from cheat-sheet.
- **Expected utility (line 1126) — no analogy** ← see P0.6
- Autonomy — ✓ "Like an apprentice who outgrows their training" (note: §2 line 220 said the apprentice maps to *learning agent*; the cheat-sheet maps it to *autonomy*. Same analogy, different concept — confusing.)
- PEAS — ✓ "Like a one-page brief for a contractor"
- Environment types — **no analogy in cheat-sheet** (line 1136). §2 had "weather forecast" / "six switches". Should be added (or removed if intentionally too long).
- Agent hierarchy — each gets its own analogy reminder ✓, but **table-driven** gets "*Like an infinite, impossible filing cabinet*" (line 1154) which **did not appear in §2** (§2 doesn't have a table-driven entry at all).

**Suggested fix:** synchronise §2 and §8. Every analogy reminder in §8 must have appeared verbatim or near-verbatim in §2. Currently table-driven, utility function, and the apprentice-for-autonomy-vs-learning all break that.

### P1.10 — Table-driven agent has NO §2 analogy at all

§2's hierarchy chain (line 575) mentions "vending-machine → driver-in-fog → satnav → satnav-with-preferences → apprentice" — five analogies for five rows. But the lecture's hierarchy on slide 25 has *six* rows including (1) table-driven. §2 skips it. The cheat-sheet (line 1154) sneaks one in. §2 must cover it.

**Suggested addition to §2:** *"A **table-driven agent is like an infinite filing cabinet** keyed by every possible life-history of the robot. Every drawer has the right answer; the only problem is the cabinet is the size of a galaxy. *Where it breaks down:* real agents *compress* the table into a program (§4.1) — see §4.2 onward for the compression schemes."*

---

## P2 — NICE TO HAVE

### P2.1 — Line 41–51 table caption misses a verb
> "Once you have this vocabulary you can read the rest of the course as 'different agent architectures for different environment types':" → grammar OK but a confused student doesn't know what "agent architectures" are yet. Add a forward-pointer: "(architectures are introduced in §3.7 and §4.)".

### P2.2 — §3.6 "Each dimension is independent of the others, so there are 2^6 = 64 *types*" (line 477) — the "independent" claim deserves a sanity check
Some pairings are correlated in practice (continuous environments tend to be dynamic; multi-agent tends to be partially observable). The chapter is technically correct that the formal dimensions are independent, but a curious student will pushback. A one-line caveat would defuse this.

### P2.3 — §3.6.4 "semi-dynamic" (lines 532–535)
Defined parenthetically; useful for exam-trap §6 #5 but never cross-linked. Add a `[see §6 pitfall 5]` pointer.

### P2.4 — §4.6 "Why all four pieces matter — the slide 36 example" (lines 815–822)
Excellent worked instance. Could be even better if you map each of the four components onto the named action: *"Critic = 'shocking language'; Learning element = installs the bad-action rule; Performance element = applies the new rule next time; Problem generator = brake-on-different-surfaces exploration."* Currently the mapping is implicit.

### P2.5 — §5.2 (lines 933–935) classification of "Solitaire (Klondike)" calls it "static" but then "sequential" — fine, but **sequential + episodic** confusion (pitfall #4) is exactly the trap; consider adding a one-line note: "the *sequence of plays inside one game* is sequential; the **game itself** is one episode if you reshuffle for the next deal."

### P2.6 — §5.2 (line 935) "Vacuum world of slide 7" classification has a thoughtful nuance about partial observability — good — but the chapter never circles back to *use* this nuance. Either drop it (it muddies the take-away) or add: "This is why the simple reflex agent of §4.2 only works when the world is small enough that 'local fully observable' covers the global state."

### P2.7 — Pitfall 10 (lines 1023–1029) names three terms (evaluation function, expected utility, utility function) to memorise separately, but the chapter only defined two of them (utility, expected utility). "Evaluation function" comes from L06 which doesn't exist yet. Either define it briefly in-line or replace with a forward-cross-reference: "*The L06 'evaluation function' is a different beast — defined when you get there.*"

### P2.8 — Line 4 prerequisite says "none — this is the foundation"; good. But the **reading time of 45 min** seems short for a chapter this dense (≈1180 lines of prose + figures + cheat-sheet). My back-of-envelope: 60–75 min for a careful first read. Either tighten or re-estimate.

---

## EVIDENCE

**Slides inspected (all 38 of source PDF):**
- Slide 1 (title) — N/A
- Slide 2 (WALL-E) — decorative; correctly not embedded
- Slide 3 (outline) — covered by §1
- Slide 4 (agent-environment loop) — §3.1, figure embedded ✓
- Slide 5 (sensor/actuator examples) — §3.1 table ✓
- Slide 6 (terminologies) — §3.2 ✓; "Agent = architecture + program" slogan present ✓
- Slide 7 (vacuum-cleaner world) — §3.2 worked example ✓
- Slides 8–9 (simple agent function table) — §3.2 figure ✓
- Slide 10 (rational agents) — §3.3 ✓ but expected-utility under-explained (P0.5)
- Slide 11 (vacuum is rational? depends!) — §3.3 / §5.1 ✓
- Slide 12 (design performance measure for what you want) — §3.3 and §5.1 ✓; would be reinforced by P1.3
- Slide 13 (autonomy) — §3.4 ✓
- Slide 14 (PEAS taxi) — §3.5 / §5.3 ✓
- Slide 15 (spam filter) — §3.5 ✓
- Slide 16 (env-types overview) — §3.6 ✓
- Slide 17 (fully vs partial) — §3.6.1 ✓
- Slide 18 (deterministic vs stochastic) — §3.6.2 ✓ — **but contradicts §2 chess-player analogy** (P0.4)
- Slide 19 (episodic vs sequential) — §3.6.3 ✓
- Slide 20 (static vs dynamic) — §3.6.4 ✓
- Slide 21 (discrete vs continuous) — §3.6.5 ✓
- Slide 22 (single vs multi) — §3.6.6 ✓
- Slide 23 (4-environment classification table) — §5.2 ✓
- Slide 24 (env-types recap) — folded into §3.6 ✓
- Slide 25 (hierarchy of agent types) — §3.7 ✓ — **but §2 only analogises 5 of 6 rows** (P1.10)
- Slide 26 (table-driven problems) — §4.1 ✓
- Slide 27 (simple reflex diagram) — §4.2 ✓
- Slide 28 (vacuum reflex code) — §4.2 ✓
- Slide 29 (model-based reflex diagram) — §4.3 ✓
- Slide 30 (model-based reflex code) — §4.3 ✓
- Slide 31 (goal-based diagram) — §4.4 ✓ — **but invented pseudocode misleads** (P0.7)
- Slide 32 (utility-based diagram + "better ways have higher utilities" quote) — §4.5 ✓
- Slides 33–35 (learning agent diagram, repeated frames) — §4.6 ✓
- Slide 36 (automated-taxi learning instance) — §4.6 worked example ✓; could be tighter (P2.4)
- Slide 37 (summary) — folded into §8 ✓
- Slide 38 (thank you) — N/A

**Chapter sections inspected:**
- §1 Overview (lines 15–53) — P0.1
- §2 Analogies (lines 57–233) — P0.2, P0.3, P0.4, P0.6, P0.8, P1.1, P1.2, P1.3, P1.4, P1.5, P1.10
- §3 Core Concepts (lines 236–588) — P0.5, P0.8, P1.6
- §4 Algorithms (lines 592–830) — P0.7, P1.7
- §5 Worked Examples (lines 834–965) — P2.5, P2.6
- §6 Pitfalls (lines 968–1041) — P2.7
- §7 Connections (lines 1044–1093) — clean
- §8 Cheat-sheet (lines 1097–1175) — P1.9

**Spec §7.1 Reviewer #3 obligations checked:**
1. Every major concept has a §2 analogy? — **FAILS** for expected utility (P0.6) and table-driven agent (P1.10).
2. Each analogy cross-linked from §3? — **PARTIALLY**: cross-links exist as "Recall the X analogy" but don't *do work* by mapping analogy elements to formal elements (P0.8).
3. "Where the analogy breaks down" caveats? — **MOSTLY YES**, all twelve §2 entries have caveats. Several caveats are weak (P1.1, P1.2, P1.3, P1.4) but present.
4. Weak / too-abstract / too-technical analogies? — **YES**: chess-player (P0.4 wrong vehicle), snapshot/camera-roll (P1.1 too literal), weather-forecast (P1.5 too vague). Replacements suggested.

---

## Report to PM

**Assignment recap:** Reviewer #3 (Pedagogical Clarity incl. Analogies) on L02-Agents.md, round 1. Lens: confused-student reader + spec §7.1 analogy enforcement.

**Status:** NEEDS_REVISION (8 P0, 10 P1, 8 P2)

**P0 findings:**
1. Forward-reference avalanche in §1 (jargon used 200 lines before defined) — `L02-Agents.md:41-51`
2. §2 model-based reflex analogy uses the formal term before §4.3 defines it — `L02-Agents.md:178-192` (same pattern for simple-reflex, goal-based, utility-based, learning)
3. §2 learning-agent analogy drops 4 technical labels (Critic / Learning element / Performance element / Problem generator) with no plain-English first — `L02-Agents.md:220-229`
4. Rational-agent analogy uses chess, but chess is the canonical *deterministic* example one section later — directly mis-trains the student — `L02-Agents.md:93-107`
5. Expected utility formula dropped without instantiating it on the vacuum world — `L02-Agents.md:380-384`
6. Expected utility has no §2 analogy (spec §7.1 requires one)
7. §4.4 goal-based-agent pseudocode is wrong: it only does one-step lookahead, contradicting the §4.4 prose explaining that goal-based agents search/plan — `L02-Agents.md:732-740`
8. §2→§3 cross-links say "recall the X analogy" but don't map analogy elements onto formal elements — affects every §3 / §4 sub-section

**P1 findings:**
1. Camera-roll percept analogy is too literal — replace with movie/script analogy
2. Vending-machine analogy doesn't tie back to partial observability
3. Referee analogy missing the "what-you-want-not-how-it-behaves" warning
4. Freelance-brief analogy missing the sensor-vs-percept trap
5. Weather-forecast analogy too vague — switch to "six switches on a job description"
6. Apprentice analogy reused for autonomy without explaining why
7. §4.5 utility-vs-goal essence (yes/no → real number) buried in a 3-item list
8. P0.6 fix also covers analogy-breakdown completeness
9. Cheat-sheet introduces analogies not present in §2 (utility = scoreboard, table-driven = filing cabinet)
10. §2 hierarchy chain skips the table-driven row entirely (only 5 of 6 rows)

**P2 findings:** 8 polish items — minor grammar, missing cross-pointers, tighter reading-time estimate.

**QA Checklist (§7) status:** N/A — this is a lecture-chapter review, not a feature-engineering QA pass. The spec routes lecture quality through the four-reviewer loop (§7), not §7-QA-checklist.

**Acceptance criteria (§1) status:** N/A (per above).

**DOCUMENT.md audit:** N/A — lecture artifact, not a code directory.

**Out-of-scope observations:**
- The chapter is materially better than the source slides (the source slides hand-wave expected utility too). The Reviser shouldn't take this as a "the slides do it so we can". Source-PDF fidelity is Reviewer #1's lens; my lens is "would a confused student survive this?".
- The chapter quietly drops "Dump" from the action set after slide 11 introduces it (line 332 reproduces both action sets but never explains the discrepancy — line 332 lists 4, line 333 references slide 11's 5-action extension parenthetically). Minor — possibly a Reviewer #1 catch — but worth flagging.
- §3.1 line 263 "(Lecture 2, slide 4.)" caption is *inside* the image alt-text, which means it'll show up as alt-text in the PDF render and as caption in markdown view. Possibly intentional, possibly redundant.

**Concerns / risks:**
- The chapter is so dense (1180 lines + figures) that the cheat-sheet on its own is ~80 lines. Risk: students who skim only §8 still benefit, but exam-trap items in §6 and worked examples in §5 won't be hit. Suggest adding a "If you only have 20 minutes: read §2 + §8 + §6 pitfalls 1–3" pointer in §1.
- The chess-as-rational-domain mistake (P0.4) is the kind of error that propagates: if it survives review and the student internalises it, they'll then get confused at L06 (adversarial search, which also leans on chess and is *also* deterministic at the rule-level but *stochastic at the position-evaluation level*). Worth fixing here so L06 doesn't inherit the confusion.

**What PM should do next:** dispatch Reviser with this report + the other three reviewer reports. Re-run the four-reviewer loop. Specifically have Reviser address the chess→poker replacement (P0.4) carefully — it cascades into §3.3, cheat-sheet, and the §2→§3 mapping work (P0.8). I expect to APPROVE on round 2 if all P0 items are addressed and at least half the P1 items land.

**DOCUMENT.md updated:** N/A for lecture review.
