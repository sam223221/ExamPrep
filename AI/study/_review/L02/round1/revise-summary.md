# Revise Summary — L02 Round 1

## Changes Made

### Reviewer #1 — Concept Completeness

- **Added slide-25 ↔ chapter-name mapping table in §3.7** and parenthetical slide-25 names in §4.3, §4.4, §4.5, §4.6 section headers, plus a mapping column in the §8 cheat-sheet "Agent hierarchy" block — addresses reviewer1 P0: *"Slide 25's official hierarchy names are not reconciled with the chapter's terminology — risks costing marks on a 'list the hierarchy' exam question."*
- **Added the slide-16 "(unobservable?)" parenthetical** as a new sentence in §3.6.1 — addresses reviewer1 P1-1: *"Slide 16's parenthetical '(unobservable?)' is missing."*
- **Added "Time can also evolve discretely or continuously" sub-point** to §3.6.5, with cross-link to L09b HMMs and L11 regression — addresses reviewer1 P1-2: *"Slide 21's note 'Time can also evolve in a discrete or continuous fashion' is dropped."*
- **Added a slide-24 verbatim-definitions mini-table** at the top of §3.6 — addresses reviewer1 P1-3: *"Slide 24's compact one-line definitions are nowhere reproduced as a single block."*
- **Added "Teach instead of instructing" call-out** to §4.6 with a one-line unpacking — addresses reviewer1 P1-4: *"Slide 33's phrasing 'Teach instead of instructing' is not reproduced."*
- **Renamed §4.6 header to "Learning / autonomous agent"** and added a sentence at the top of §4.6 explicitly linking the architecture to autonomy from §3.4 — addresses reviewer1 P1-5: *"Slide 33's lecture-agent name is 'Learning/Autonomous agent' but the chapter section is titled 'Learning agent' only."*
- **Added disclaimer to §5.2 follow-on** marking the Solitaire / vacuum-world classifications as "extension exercise — not on the slides" — addresses reviewer1 P2-1.
- **Added slide-2 "Intelligent Agents" acknowledgement** in §1 — addresses reviewer1 P2-2.
- **Added slide-27 "if (I sense a certain input) then (I apply a specific rule)" gloss** to §4.2 — addresses reviewer1 P2-3.
- **Made the "performance measure (utility function)" equivalence prominent** in §3.3's first paragraph — addresses reviewer1 P2-4.
- **Made cooperative-vs-competitive multi-agent split more prominent** in §3.6.6 (own bulleted block) — addresses reviewer1 P2-5.
- **Wrapped slide-13 autonomy bullets as a verbatim fenced quote** in §3.4 — addresses reviewer1 P2-6.
- **Wrapped slide-12 performance-measure-design line in italicised block-quote** in §3.3 and §5.1 — addresses reviewer1 P2-7.

### Reviewer #2 — Mathematical Rigor

- **Fixed Chess-with-clock entry in §5.2 classification table from "Discrete" to "Continuous"**, and rewrote the prose to note this flips *two* dimensions (Static→Dynamic AND Discrete→Continuous) — addresses reviewer2 P0-1: *"Environment classification table contradicts slide 23 for 'Chess with a clock' (Discrete row)"* and P0-2: *"§5.2 prose claims chess-with-a-clock 'flips just one dimension' — it flips two per the slide."*
- **Disambiguated `P` overloading globally**: added a Notation convention block at the top of the chapter introducing $\mathcal{P}$ for percept set, $A$ for actions, $S$ for state set, $P(\cdot)$ reserved for probability, $\mathbb{E}[\cdot]$ for expectation, $U(\cdot)$ for utility. Applied $\mathcal{P}^{*}$ consistently throughout §3.2, §4.1 (where $|P|^T$ became $|\mathcal{P}|^T$), §8 — addresses reviewer2 P0-3.
- **Rewrote §3.2 percept-sequence definition** to make `\mathcal{P}^*` clearly the *set* (Kleene star) and the agent function $f : \mathcal{P}^* \to A$ a map *from* that set — addresses reviewer2 P0-4: *"`P^*` is conflated with 'a single percept sequence' in §3.2, then used as a domain in the very next equation."*
- **Tightened §3.3 expected-utility formula** to $\mathbb{E}[U \mid a] = \sum_{o \in \Omega(a)} P(o \mid a) U(o)$ with $\Omega(a)$ declared as mutually exclusive exhaustive outcome set, plus a sentence saying "replace sum with integral for continuous outcomes" and a note that slide 10 does not give the formula — addresses reviewer2 P1-1: *"Expected-utility formula in §3.3 has unstated assumptions (and is not in the source PDF)."*
- **Declared `Result(s, a)` in §4.5** explicitly as the (possibly stochastic) successor state, with both deterministic and stochastic expansions written out and a $P(s' \mid s, a)$ form — addresses reviewer2 P1-2: *"`Result(state, a)` in §4.5 utility-based argmax is undeclared and its determinism is unspecified."*
- **Declared $S$ globally** in the chapter-top notation block and re-emphasised in §4.5: "Let $S$ denote the set of environment states (set here; reused in L03/L06/L09a/L09b/L10)." Also flagged the slide-32 ambiguity about $U$ taking single states vs sequences — addresses reviewer2 P1-3.
- **Rewrote §4.1 row-count formula** as $\sum_{t=1}^{T} |\mathcal{P}|^{t} = \mathcal{O}(|\mathcal{P}|^{T})$ with the closed-form geometric-series step shown — addresses reviewer2 P1-4: *"Table-driven agent size formula `|P|^T` understates the count by ignoring shorter sequences."*
- **Made UPDATE-STATE argument naming consistent** in both prose and pseudocode (both use `last_action`) in §4.3 — addresses reviewer2 P1-5.
- **Added footnote in §3.2** flagging that slide 6 writes `f: p* → A` with lowercase `p` while the chapter uses $\mathcal{P}^*$ — addresses reviewer2 P1-6.
- **Rewrote cheat-sheet expected-utility formula** in §8 to use bound variable $o \in \Omega(a)$ — addresses reviewer2 P1-7.
- **Re-attributed §5.4 episodic claim** as "standard Russell-&-Norvig synthesis" with strict slide-27 claim called out separately; row reads "Fully observable (slide 27); in practice also easiest when episodic" — addresses reviewer2 P1-8.
- **Used `\operatorname*{arg\,max}`** in §4.5 and §8 — addresses reviewer2 P2-1.
- **Used $\mathbb{E}[U \mid a]$ conditional form** consistently — addresses reviewer2 P2-2.
- **Introduced $S$ as shared notation** at the top of the chapter — addresses reviewer2 P2-3.
- **Added "in principle" caveat** before "$2^6 = 64$ types" in §3.6 — addresses reviewer2 P2-7.
- **Added footnote to §4.1 pseudocode** clarifying "fully specified" is the in-principle assumption that the rest of §4.1 demolishes — addresses reviewer2 P2-4.
- **Added footnote in §4.2** noting that slide 28's pseudocode is missing the `INTERPRET-INPUT` line — addresses reviewer2 P2-6.
- P2-5 (procedural vs OO pseudocode style in §4.4) addressed indirectly because §4.4 pseudocode was deleted entirely per reviewer3 P0.7 and replaced with prose + a schematic two-line SEARCH/return.first().

### Reviewer #3 — Pedagogical Clarity

- **Moved the lecture-map table from §1 to §7** (now appears at the top of §7 where the vocabulary is already in hand). §1 retains a one-line "by the end of this chapter you'll be able to read every later lecture in these terms" pointer — addresses reviewer3 P0.1: *"Forward-reference avalanche in §1 (lines 41–51)."*
- **Rewrote every §2 heading to lead with the *idea*, then name the formal concept at the end of the line**: "Sensing-and-acting in a loop — like a thermostat with a job description (formal name: **agent**)", "A driver in fog — model-based reflex agent (slide 25 calls this 'Agents with memory')", etc. Cross-link forward to the §3/§4 formalisation in each entry — addresses reviewer3 P0.2: *"§2 introduces 'model-based reflex agent' before defining it."*
- **Rewrote the learning-agent §2 entry** to land the four roles in plain English first, *then* drop the formal names (Critic / Learning element / Performance element / Problem generator) as labels — addresses reviewer3 P0.3.
- **Replaced the chess-player rational-agent analogy with poker-player** throughout §2 and §3.3, with explicit cross-reference noting chess is the deterministic example one section later. Updated cheat-sheet (§8) to match — addresses reviewer3 P0.4: *"Rational-agent analogy uses chess as the vehicle, but chess is the canonical *deterministic* example one section later."*
- **Instantiated the expected-utility formula on the vacuum world** in §3.3: deterministic case ($\mathbb{E}[U \mid \text{Suck}] = U(\text{clean})$) and stochastic case ($0.9 \cdot U(\text{clean}) + 0.1 \cdot U(\text{dirty})$) — addresses reviewer3 P0.5.
- **Folded expected utility into the §2 poker-player analogy explicitly**: "That mental sum 'how much do I expect to win, weighted by how likely each card-out is' **is expected utility**." — addresses reviewer3 P0.6.
- **Replaced the broken goal-based pseudocode in §4.4** with the slide-31 prose description plus a two-line schematic (`plan ← SEARCH(state, goal, model); return plan.first()`) — addresses reviewer3 P0.7: *"§4.4 Goal-based-agent pseudocode is wrong as pedagogy."*
- **Added explicit analogy-element ↔ formal-element mappings** at the top of every "Recall the X analogy" cross-link in §3.1, §3.2, §3.3, §3.4, §3.5, §3.6, §3.7, §4.2, §4.3, §4.4, §4.5, §4.6 — addresses reviewer3 P0.8.
- **Replaced the "snapshot / camera roll" analogy with "next frame in a movie / whole movie up to now"** and used it to set up the function-vs-program-as-summary distinction — addresses reviewer3 P1.1.
- **Extended the vending-machine analogy** to flag the failure mode as "partial observability (§3.6.1)" — addresses reviewer3 P1.2.
- **Added the "what-you-want-not-how-it-behaves" warning** into the referee analogy's caveat — addresses reviewer3 P1.3.
- **Added the sensor-vs-percept trap** into the freelance-brief analogy's caveat — addresses reviewer3 P1.4.
- **Replaced the weather-forecast analogy with "six switches on a job description"** in §2 and re-used it as the §3.6 lead-in — addresses reviewer3 P1.5.
- **Added a sentence linking the apprentice analogy across autonomy (§3.4) and learning agent (§4.6)** — addresses reviewer3 P1.6.
- **Added the one-sentence essence** to §4.5 opening: "goal-based agents answer **yes/no**; utility-based agents answer **how good**" — addresses reviewer3 P1.7.
- **§2 now includes table-driven agent ("infinite, impossible filing cabinet")**, with caveat — addresses reviewer3 P1.10 and reviewer3 P1.9 (the cheat-sheet analogy now appears in §2 too).
- **Synchronised cheat-sheet analogies with §2** — every §8 italic reminder now has a matching §2 entry. Updated table-driven, utility function, expected utility, environment types — addresses reviewer3 P1.9.
- **Reading-time estimate updated** from "~45 min" to "~60–75 min" — addresses reviewer3 P2.8.
- **Added §2 caveat for environment types about $2^6 = 64$ being formal**, noting practical correlations — addresses reviewer3 P2.2.
- **Added a `[see §6 pitfall 5]` pointer for semi-dynamic** in §3.6.4 — addresses reviewer3 P2.3.
- **Mapped each learning-agent role to the slide-36 taxi example explicitly** — addresses reviewer3 P2.4.
- **Added the sequential-within-episodic clarification** to the §5.2 Solitaire follow-on (game-internal sequence vs episodes between deals) — addresses reviewer3 P2.5.
- **Added a "this is why simple reflex only works..."** sentence to the §5.2 vacuum-world nuance — addresses reviewer3 P2.6.
- **Annotated pitfall 10** that "evaluation function" is an L06 term not yet defined — addresses reviewer3 P2.7.
- **Added "If you only have 20 minutes" pointer to §1** — concession to "chapter is dense" concern.
- §1 forward-references the term "architectures" with a brief gloss pointing to §3.7/§4 — addresses reviewer3 P2.1.

### Reviewer #4 — Exam Readiness

- **Added §6 pitfall 13 plus a §3.6.2 convention paragraph** distinguishing one-shot initial randomness (deterministic transitions) from ongoing transition-randomness (stochastic). Reconciled Word-jumble (deterministic) with Solitaire (also deterministic, per the same convention). Updated §5.2 Solitaire follow-on to match — addresses reviewer4 P0-1: *"§5.2 classification ... contradicts slide 23 on Observability AND Episodicity, in a way students WILL be tested on."*
- **Added a one-sentence definition of `Dump`** in §3.2's vacuum-world bullet (deposit collected dirt at a designated cell) plus the note that the lecture itself does not formally define it — addresses reviewer4 P0-2.
- **Added a numeric blow-up table in §4.1** for $|\mathcal{P}| = 4$ at $T \in \{1, 2, 4, 10, 20\}$, showing $\approx 1.5 \times 10^{12}$ rows at $T = 20$ — addresses reviewer4 P0-3.
- **Added PEAS for the vacuum agent** in §3.5 as a third worked PEAS — addresses reviewer4 P0-4.
- **Added PEAS for a medical diagnosis agent** in §3.5 as a textbook-style non-physical example — addresses reviewer4 P1-8.
- **Re-attributed §5.4 simple-reflex "episodic" claim** as a practical convenience, with the strict slide-27 claim being just "Fully observable" — addresses reviewer4 P1-1.
- **Flagged the sensor-model addition in §4.3** as a Russell-&-Norvig 4th-ed addition not on slide 29 — addresses reviewer4 P1-2.
- **Added the agent-type → minimum-environment mapping table to §8** — addresses reviewer4 P1-3.
- **Added "$2^6 = 64$ in principle; only a handful matter" line to §8** under Environment types — addresses reviewer4 P1-4.
- **Added cooperative-vs-competitive split to §6 pitfall 7** with Pac-Man-vs-ghosts (competitive) example — addresses reviewer4 P1-5.
- **Added semi-dynamic to §6 pitfall 5 and to §8** (Chess-with-clock canonical example) — addresses reviewer4 P1-6.
- **Reconciled §5.2 Chess-with-clock prose with semi-dynamic terminology**: noted slide 23 calls it Dynamic for simplicity while the textbook says semi-dynamic — addresses reviewer4 P1-7.
- **Added a paragraph under the slide-9 figure** in §3.2 explaining variable-length rows, history-keying, and why this particular table is realisable by a reflex agent — addresses reviewer4 P1-9.
- **Added a 5-step quantitative cumulative-performance trace to §5.1** — addresses reviewer4 P1-10.
- **Moved the "affects performance measure" qualifier into §3.6.6 itself** (was only in §6 pitfall 7 before) — addresses reviewer4 P1-11.
- **Boxed the slide-37 summary** in §8 ("the most challenging environments..." quote retained verbatim) — addresses reviewer4 P2-1.
- **Added a "memorise this table" callout** at the top of §5.2 — addresses reviewer4 P2-2.
- **Added "learning agent is not row six" note** to §3.7 — addresses reviewer4 P2-3.
- **Glossed `Result(s, a)`** at first introduction in §4.5 — addresses reviewer4 P2-4.
- **Added the agent-boundary modelling-choice line** to §3.1 — addresses reviewer4 P2-5.
- **"Rationality is not omniscience" used verbatim** in §3.3 and §6 pitfall 1 — addresses reviewer4 P2-7.

### Cross-reviewer arbitrations (stricter interpretation applied)

- **Chess-with-clock Discrete-vs-Continuous**: reviewer2 P0-1 (Continuous per slide) is stricter than reviewer4 P1-7 (semi-dynamic note). Applied both — table corrected to Continuous, prose explicitly says "flips two dimensions" and adds the semi-dynamic textbook caveat.
- **Russell-&-Norvig "sensor model"**: reviewer4 P1-2 (flag as R&N addition) is the stricter interpretation than reviewer1's implicit acceptance. Applied — §4.3 explicitly tags the sensor model as an R&N addition not on slide 29.
- **Apprentice analogy reuse for autonomy and learning**: reviewer3 P1.6 (explain the reuse) is stricter than just leaving it implicit. Applied — both §2 learning-agent entry and §3.4 autonomy section now explicitly cross-reference each other and explain why the same analogy fits both.
- **Episodic claim for simple reflex**: reviewer2 P1-8 + reviewer4 P1-1 agree — strict slide-27 claim ("Fully observable") separated from the R&N textbook synthesis ("plus episodic in practice"). Applied that split in §5.4.
- **Notation overloading of P**: reviewer2 P0-3 is the strictest. Applied a top-of-chapter notation block (also satisfies reviewer2 P2-3 and reviewer3 P1.9 globally).

## P2s Deferred (if any)

None — every reviewer P2 has been applied. The only P2 not addressed verbatim is reviewer2 P2-5 (procedural vs OO pseudocode style in §4.4) because the entire pseudocode for §4.4 was deleted in response to reviewer3 P0.7 — the style-mixing issue no longer exists.

## Round 2 pending
