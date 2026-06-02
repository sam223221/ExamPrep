# Reviewer #3 — Pedagogical Clarity (incl. Analogies) — ROUND 2

**Artifact:** `study/lectures/L02-Agents.md` (Round 2, post-revision)
**Source:** `Lecture2-Introduction to Agents.pdf` (slides 1–38)
**Round 1 verdict:** NEEDS_REVISION (8 P0, 10 P1, 8 P2)
**Lens:** Confused-student reader; analogy enforcement per spec §6.1 / §7.1 Reviewer #3.

---

## VERDICT

**APPROVE_WITH_NITS**

Eight P0 items were filed in round 1. Seven are now fully addressed; the eighth (P0.8 — mapping analogy elements onto formal elements at §2→§3 cross-links) is **mostly** addressed but the work was only applied to §3, not §4. §4.2 / §4.3 / §4.4 still say bare "Recall the X analogy" without naming the mapping. Because §3 — where the mapping matters most for a first-time student — was done thoroughly, I am not re-raising this as a blocking P0. It is logged as P1 R2-#1 below.

The Round-2 revision is a substantial improvement on every front my lens cares about:

- **§2 headings now lead with the idea, not the formal name** (P0.2 fixed cleanly).
- **The chess→poker swap** (P0.4) is propagated to §2, §3.3, and the cheat-sheet, with an *explicit* "we deliberately avoid the chess framing" caveat that defends against future confusion. This is exactly the cascade fix I asked for.
- **Expected utility now has a §2 analogy** (folded into the poker player) *and* gets concretely instantiated on the vacuum world in §3.3 with both deterministic (collapse to $U(\text{clean})$) and stochastic ($0.9 U(\text{clean}) + 0.1 U(\text{dirty})$) cases. A confused student can now actually compute it.
- **The broken §4.4 pseudocode is gone**, replaced with prose plus a two-line schematic `SEARCH(state, goal, model); return plan.first()` that honestly says "this is search (L03)". No more contradiction between code and prose.
- **The learning-agent four roles** are now landed in plain English first (judge / update / apply / explore), then mapped to the formal labels, so a student reading §2 linearly actually learns the four roles instead of seeing four bolded jargon-words.
- **The §1 forward-reference avalanche** is gone — the lecture-map table is now at the top of §7 where the vocabulary is in hand, with only a one-line pointer in §1.
- **Table-driven now has a §2 analogy** ("infinite, impossible filing cabinet"), and §2's hierarchy chain now matches the slide-25 six rows.
- **The §2→§3 mapping cross-links** in §3.1–§3.7 are now genuine pedagogical bridges, not just "recall the X analogy" pointers. The §3.3 mapping (poker cards-on-table → percept sequence, cards-still-to-come → $P(o \mid a)$, chip stack → $U$) is especially well-done.

What stops this from being a clean **APPROVE**: a handful of small Round-2-introduced loose ends — §4 cross-link mappings, a stray "scoreboard" analogy in §8 that has no §2 antecedent, a slide-25-name injection into §2 headings that mildly re-clutters them, and a couple of glossary/§2 mismatches. None blocks a confused student from reading top-to-bottom. All are catchable in a one-pass polish.

---

## ROUND-1 P0 VERIFICATION (item-by-item)

### P0.1 — Forward-reference avalanche in §1 — **FIXED ✓**

Lecture-by-lecture map relocated to §7 (lines 1427–1442). §1 now ends with a single forward-pointer: *"The lecture-by-lecture map of which environment slice each one tackles lives in §7 (Connections to Other Lectures) — by then the vocabulary will be in hand."* (lines 56–60). The §1 still references "environment taxonomy" and "architectures" but glosses them in-line ("a term introduced in §3.7 and §4"). Confused-student-readable.

### P0.2 — §2 introduces formal names before defining — **FIXED ✓**

Every §2 heading now leads with the *idea* and ends with the formal name:

- L79  "Sensing-and-acting in a loop — like a thermostat with a job description (formal name: **agent**)"
- L92  "The contract vs the employee — agent function vs agent program"
- L108 "Playing the odds — like a poker player who plays expected value (formal name: **rational agent**)"
- L132 "A frame in a movie vs the whole movie up to now — percept vs percept sequence"
- L145 "What you want, not how the agent should do it — referee, not a coach (formal name: **performance measure**)"
- L161 "A one-page brief for a freelance contractor — PEAS"
- L175 "Six switches on a job description — environment types"
- L198 "An infinite, impossible filing cabinet — table-driven agent"
- L209 "A vending machine — simple reflex agent"
- L224 "A driver in fog — model-based reflex agent (slide 25 calls this 'Agents with memory')"
- L239 "A satnav — goal-based agent (slide 25 calls this 'Agents with goals')"
- L254 "A satnav with preferences — utility-based agent"
- L271 "An apprentice getting feedback — learning / autonomous agent"

The pattern is consistent. **Note (P1 R2-#3 below):** the slide-25 alternative names sneaked into the headings of L224 and L239 partially defeat the "idea first" intent, but I am not raising this above P1 because Reviewer #1 explicitly wanted slide-25-name alignment. Reasonable cross-reviewer trade-off.

### P0.3 — Learning-agent four labels with no plain English first — **FIXED ✓**

Lines 271–284 now read:

> An **apprentice** doesn't just do the job — they get feedback from someone judging their work, internally update their understanding, apply the improvement next time, and occasionally try something risky to learn from. That four-role loop is what we'll formalise in §4.6 as the **learning agent** … The four roles get formal names in §4.6:
> - *the one who judges* → **Critic**
> - *the one who updates understanding* → **Learning element**
> - *the one who applies the improvement* → **Performance element**
> - *the one who tries something risky* → **Problem generator**

Exactly the structure I asked for: intuition → label, not label → intuition.

### P0.4 — Rational-agent analogy uses chess (deterministic later) — **FIXED ✓**

Replaced with poker (lines 108–130). The caveat block (line 127) is **exemplary**: it explicitly says *"We deliberately avoid the 'chess-player' framing here: chess is the canonical *deterministic* example one section later — see §3.6.2. Poker is unambiguously stochastic, where 'playing the odds' actually does work."* This is the level of self-awareness a chapter needs — it forecloses the very mistake that round 1 caught.

The fix cascades correctly:

- Cheat sheet line 1513: *"Like a poker player playing expected value."* ✓
- §3.3 line 444–447: poker-player cross-link with explicit mapping (*cards already on the table* = percept sequence, *cards still to come* = $P(o \mid a)$, *chip stack outcome* = $U$, *choice maximising expected chips* = rational action) ✓
- §3.3 line 501: ends the worked example with "This is exactly the *poker bet* of §2 applied to a vacuum cleaner." ✓

### P0.5 — Expected utility hand-waved on the vacuum example — **FIXED ✓**

Lines 482–501 now ground the formula on the running example, deterministic and stochastic cases both. The 0.9/0.1 motor-failure split that I suggested in round 1 was adopted essentially verbatim. **Pedagogically excellent** — a confused student can now compute expected utility on the chapter's running example without having to wait for L09a.

### P0.6 — Expected utility has no §2 analogy — **FIXED ✓**

Folded into the poker-player entry at lines 114–115: *"That mental sum 'how much do I expect to win, weighted by how likely each card-out is' **is expected utility**."* Then the cheat-sheet (line 1525) closes the loop: *"Like the poker bet: weight each card-out by its probability."* Concept now has the spec-required §2 analogy.

### P0.7 — Broken goal-based pseudocode — **FIXED ✓**

Lines 1004–1014. The misleading "for each action a do … if predicted_state ∈ goal then return a" snippet is gone. Replaced with prose:

> The decision procedure is no longer a fixed rule table. Instead the agent uses its model to *predict* the outcome of each candidate *action sequence* and picks one that reaches a goal state. Choosing **which** sequence to consider is the **search problem** of L03.

…and a two-line schematic:

```text
plan ← SEARCH(state, goal, model)     // produces a sequence of actions
return plan.first()                   // execute the first action; repeat
```

This is exactly the "drop the broken pseudocode entirely, replace with honest prose" recommendation. The student no longer walks away thinking "goal-based = one-step lookahead".

### P0.8 — §2→§3 cross-links don't map elements — **MOSTLY FIXED, downgraded to P1 below**

§3.1–§3.7 all now open with an explicit mapping. The §3.3 poker mapping is the gold-standard exemplar; §3.2 (frame=percept, movie=percept sequence, script=agent function, director's brain=agent program) is also clean. §3.4, §3.5, §3.6, §3.7 all have a "Mapping:" line. **For the §3 sections — where it matters most — this is fully resolved.**

What's left undone: §4.2 (L887), §4.3 (L942), §4.4 (L996) still say only "Recall the X analogy from §2" with no element-by-element mapping. The §2 entries for these agents already do most of the mapping work (the §2 driver-in-fog entry already names internal state and partial observability), so the omission is less harmful than it would have been in §3, but it's still inconsistent. **Logged as P1 R2-#1 below.**

§4.5 (L1037–1039) gets a partial pass: it doesn't do a structured "mapping" block but the one-line essence *"goal-based agents answer yes/no; utility-based agents answer how good"* is itself the essential mapping. §4.6 (L1090–1092) gets a half-pass — "learning agent is the architectural realisation of autonomy" is the cross-link, but the four-role mapping to the apprentice doesn't appear until later in §4.6 at lines 1101–1115 (and is done well there). Acceptable.

---

## ROUND-1 P1 VERIFICATION (spot-checked)

- **P1.1 movie-script replaces snapshot/camera-roll** — FIXED (L132–143). Used to set up the function-vs-program-as-summary distinction, as I asked.
- **P1.2 vending-machine partial-observability tie-back** — FIXED (L219–222).
- **P1.3 referee "what-you-want" warning** — FIXED (L155–159).
- **P1.4 freelance brief sensor-vs-percept trap** — FIXED (L169–173).
- **P1.5 six-switches replaces weather-forecast** — FIXED (L175–196).
- **P1.6 apprentice cross-link autonomy↔learning** — FIXED (L290–292 and L516–523).
- **P1.7 yes/no vs real number essence** — FIXED (L261–264 in §2; L1037–1039 in §4.5).
- **P1.8 expected-utility breakdown-caveat** — FIXED via P0.6.
- **P1.9 cheat-sheet ↔ §2 synchronisation** — **PARTIALLY FIXED**. See R2-#2 below for the residual.
- **P1.10 table-driven §2 entry** — FIXED (L198–207). Also synced to the cheat sheet (L1565).

All P2s from round 1 appear addressed per the revise-summary; I spot-checked the reading-time bump (~60–75 min, L3 ✓), the §6 pitfall-5 cross-link (L724 ✓), and the slide-36 four-role mapping (L1124–1137 ✓ — exactly the explicit mapping I asked for in P2.4).

---

## NEW / RESIDUAL FINDINGS (R2)

### P0 — none.

### P1 — SHOULD FIX

#### P1 R2-#1 — §4 cross-links don't apply the same mapping discipline as §3

The Reviser added an explicit "Mapping:" line at the top of every §3.X. The same discipline did **not** propagate to §4.2, §4.3, §4.4. They each just say "Recall the X analogy from §2" — exactly the bare cross-link Round 1's P0.8 complained about. Examples:

- L887 §4.2: "Recall the **vending-machine analogy** from §2: condition → action, no memory." — okay-ish (the gloss "condition → action, no memory" *is* a partial mapping, but bare).
- L942 §4.3: "Recall the **driver-in-fog analogy** from §2." — no mapping at all.
- L996 §4.4: "Recall the **satnav analogy** from §2." — no mapping at all.

A confused student reading §4.3 doesn't know whether "internal state" maps to "the driver's mental picture of the road" or to "the driver's last-seen frame of road" or to "the driver's prior knowledge of road geometry". Round 1's P0.8 wanted this fixed everywhere; round 2 fixed §3 but not §4.

**Suggested fix (small):** add a 2–3 line "Mapping:" block at the top of §4.2/§4.3/§4.4 in the same style as §3.X. For §4.3:
> *Mapping: the **driver** is the agent; the **driver's mental picture of the road through fog** is the **internal state**; the **driver's experience of how cars move (constant velocity, friction)** is the **transition model**; the **driver's expectation of what they'd see if the fog lifted** is the **sensor model** (R&N 4th-ed addition).*

#### P1 R2-#2 — Cheat-sheet has analogy reminders that don't appear in §2

The Reviser claims (revise-summary line 60) that "every §8 italic reminder now has a matching §2 entry". Checking:

- **Cheat sheet L1500 "Agent function. *Like a one-page contract.*"** — §2 L92 heading is "The contract vs the employee — agent function vs agent program", body uses "the contract" (L94) and "one-page contract" (L98). Match ✓.
- **Cheat sheet L1519 "Utility function. … *Like the score on the scoreboard.*"** — **§2 does not have a dedicated utility-function entry.** §2's "satnav with preferences" entry (L254–269) is about the *utility-based agent*, and uses "preferences" / "sliders" / "real-valued scale" but never "scoreboard". The cheat-sheet analogy is new in §8. **Missing antecedent.**
- **Cheat sheet L1525 "Expected utility. … *Like the poker bet: weight each card-out by its probability.*"** — §2 L114–115 phrasing is "That mental sum 'how much do I expect to win, weighted by how likely each card-out is' **is expected utility**". Same domain, similar phrasing — close enough. Match ✓.
- **Cheat sheet L1542 "Environment types … *Like six switches on a job description.*"** — §2 L175 heading is "Six switches on a job description". Match ✓.
- **Cheat sheet L1565–1570 hierarchy analogies** — all match §2.

So **one residual mismatch**: the cheat-sheet's "score on the scoreboard" analogy for *utility function* has no §2 antecedent. This is the same issue I flagged in round-1 P1.9 — the round-2 fix didn't fully land. Two clean options:

- (a) Add a one-liner to the §2 satnav-with-preferences entry: *"The utility function itself is **like the score on a scoreboard**: a single real number that says how well the agent is doing in this state."* Then the cheat-sheet reminder has a §2 home.
- (b) Drop the "scoreboard" line from the cheat sheet and reuse "satnav-with-preferences" or "preference-slider" for utility function.

Option (a) is mildly preferable because *utility function* and *utility-based agent* are technically two different concepts (the function is a mathematical object; the agent is an architecture that uses it). Distinguishing them in §2 sharpens the chapter.

#### P1 R2-#3 — Slide-25 alternative-names inside §2 headings re-clutter the pedagogical-first headings

The Reviser, presumably to satisfy Reviewer #1's slide-25-mapping demand, injected slide-25 names into two §2 headings:

- L224 "A driver in fog — model-based reflex agent (slide 25 calls this 'Agents with memory')"
- L239 "A satnav — goal-based agent (slide 25 calls this 'Agents with goals')"

The purpose of §2 (per the chapter's own statement at L75–77) is to "meet the intuition before the jargon". A heading that contains *three* jargon items (chapter name + slide-25 name + slide reference) defeats that purpose for the two of the four hierarchy rows that get this treatment. (§2's simple-reflex, table-driven, utility-based and learning entries do *not* get the slide-25 name in the heading — so the chapter is also internally inconsistent.)

**Suggested fix:** move the slide-25 alternative name out of the §2 heading and into the §2 entry's body (one sentence). The §4.X headers (which already say e.g. *"Model-based reflex agent (slide 25 row 3 — 'Agents with memory')"*) are the right place to anchor the slide-25 alignment; §2 should stay analogies-first.

### P2 — NICE TO HAVE

#### P2 R2-#1 — §1 still uses two terms before defining them (mild)

- L51 names "performance measure" before it's defined in §3.3. A one-word forward-link would help: "performance measure (defined in §3.3)".
- L53 names "environment taxonomy". The §1 already glosses "architectures" inline; doing the same for "taxonomy" would symmetric-up the prose.

Strictly minor — these terms are intuitive enough that no first-time reader will choke, but the §1 is otherwise *so* clean that these stand out.

#### P2 R2-#2 — The glossary banner at L5–11 promises "utility function" but §2 has no dedicated entry for it

L5–11: *"Glossary terms introduced: agent, agent function, agent program, percept, percept sequence, rational agent, performance measure, utility function, …"*

§2 has standalone entries for *agent*, *agent function/program*, *rational agent*, *percept/percept sequence*, *performance measure* — but *utility function* is bundled inside "satnav with preferences" (the utility-based agent). If the glossary banner promises it as a top-level concept, §2 should too. Tied to P1 R2-#2 — fixing that fixes this.

#### P2 R2-#3 — Cheat-sheet "Optimal action" entry (L1528) lacks an analogy reminder

Every other cheat-sheet bullet ends with an italic analogy reminder. Optimal action gets the formula but no analogy. Could end with: *"Like picking the bet with the highest expected-value chip stack."* (Re-uses the poker domain — pedagogically consistent.)

#### P2 R2-#4 — §3.2 worked-example block (vacuum-agent if-then code at L426–433) is *both* the analogy demonstration *and* the rationality target for §3.3 — but the chapter never flags the dual role

A small pedagogical fix: at L438 ("Is that the *best* function? Not necessarily — see §3.3.") consider adding "(This same if-then code is the agent we'll evaluate for rationality in §5.1 — Step 1.)" That makes the across-section threading explicit.

#### P2 R2-#5 — The slide-25 name in §4 headers shows up as "slide 25 row 3 — 'Agents with memory'" — fine — but the chapter never explicitly says §4.6's "Learning / autonomous agent" is **not** a row of slide 25

§3.7 line 814 already says this clearly: *"The slide-25 hierarchy has five rows. The learning agent (§4.6) is not a sixth rung."* §4.6's header (L1088) says *"slide 33 title — 'Learning/Autonomous agent'"* but doesn't say "*not* slide 25". A one-clause reminder in §4.6 ("layered orthogonally on top of any §4.2–§4.5 row, not a sixth row of slide 25") would close the loop for a student who jumps straight to §4.6.

#### P2 R2-#6 — The "If you only have 20 minutes" pointer at L62 is excellent, but it skips §5

Reviewer #4's exam-readiness lens cares about §5 worked examples. A student with 20 minutes who reads §2 + §8 + §6 pitfalls 1–3 will get the vocabulary but no PEAS-or-classification practice. Consider: *"If you only have 20 minutes: read §2 (analogies), §8 (cheat sheet), §6 pitfalls 1–3, and **§5.2 (classification table)**."* The classification table is the single most exam-quotable artifact in the chapter.

---

## EVIDENCE — slides re-inspected for round 2

All 38 source slides re-checked; the round-1 evidence list still holds. The two specific slide↔chapter contradictions I called out in round 1 are now resolved:

- **Slide 18 (deterministic / chess) ↔ §2 chess-player analogy** — analogy replaced with poker. ✓
- **Slide 31 (goal-based diagram) ↔ §4.4 pseudocode** — pseudocode dropped, replaced with prose + SEARCH schematic. ✓

The slide-25 hierarchy now matches §3.7 and §4 (P1.10 from round 1 fixed) and the §8 cheat sheet preserves both naming conventions (L1561–1570). Slide-37 summary box is now reproduced verbatim in §8 L1557–1559. Slide-12 design-performance-measure quote appears twice (L508–510 and L1213–1214) — desirable redundancy for the exam-quotable line.

---

## Spec §7.1 Reviewer #3 obligations — round-2 checklist

1. **Every major concept has a §2 analogy.** Round 1 failed for *expected utility* and *table-driven agent*. Both now have §2 entries. ✓ — **modulo** the residual that *utility function* (as a standalone glossary entry — see P1 R2-#2) is bundled rather than standalone.
2. **Each analogy cross-linked from §3.** Round 1 failed because cross-links didn't *do work*. Round 2: §3 cross-links now map analogy elements onto formal elements (✓), §4 cross-links still bare for §4.2/§4.3/§4.4 (✗ — P1 R2-#1).
3. **"Where the analogy breaks down" caveats.** All twelve §2 entries had them in round 1; the new table-driven entry in round 2 also has one (L205–207). ✓
4. **Weak/wrong-vehicle analogies replaced.** Chess→poker (round 1 P0.4 ✓), camera-roll→movie (P1.1 ✓), weather-forecast→six-switches (P1.5 ✓). ✓

---

## Report to PM

**Assignment recap:** Reviewer #3 (Pedagogical Clarity) round 2 on `study/lectures/L02-Agents.md`. Lens: confused-student reader + spec §7.1 analogy enforcement. Verifying that the 8 P0 / 10 P1 / 8 P2 round-1 findings were addressed.

**Status:** **APPROVE_WITH_NITS** (0 new P0, 3 P1, 6 P2)

**Round-1 P0 verification:**
1. Forward-reference avalanche in §1 — FIXED ✓ (table moved to §7, one-line pointer remains)
2. §2 introduces formal names before defining — FIXED ✓ (every §2 heading idea-first, name-last)
3. Learning-agent four labels with no plain English — FIXED ✓ (plain English first, labels second)
4. Chess-player rational analogy → deterministic conflict — FIXED ✓ (poker player, cascade to §3.3 and cheat sheet, with explicit "we deliberately avoid chess" caveat)
5. Expected utility hand-waved — FIXED ✓ (deterministic + stochastic instantiation on the vacuum world, with the 0.9/0.1 motor-failure example I suggested)
6. No §2 analogy for expected utility — FIXED ✓ (folded into poker-player entry)
7. Broken §4.4 goal-based pseudocode — FIXED ✓ (replaced with prose + honest 2-line SEARCH schematic)
8. §2→§3 cross-links don't map elements — MOSTLY FIXED ✓ for §3 (excellent), still bare in §4 — downgraded to P1 R2-#1

**New P1 findings (R2):**
1. §4.2/§4.3/§4.4 cross-links don't propagate the §3 mapping discipline — `L02-Agents.md:887, 942, 996`. Add 2–3 line "Mapping:" blocks in the §3.X style.
2. Cheat-sheet *utility function* analogy ("score on the scoreboard") has no §2 antecedent — `L02-Agents.md:1519`. Add a one-liner to the §2 satnav-with-preferences entry, or change the cheat-sheet phrasing.
3. Slide-25 alternative names injected into two §2 headings re-clutter the "idea-first" intent — `L02-Agents.md:224, 239`. Move slide-25 names into the body of the §2 entry; keep the §4.X headers as the slide-25 anchor.

**New P2 findings (R2):**
1. §1 still uses "performance measure" and "environment taxonomy" before they're defined — `L02-Agents.md:51, 53`. One-word forward-pointer fix.
2. Glossary banner promises "utility function" but §2 has no standalone entry — `L02-Agents.md:5-11` (tied to P1 R2-#2).
3. Cheat-sheet "Optimal action" entry lacks an italic analogy reminder — `L02-Agents.md:1528`. Add a one-liner.
4. §3.2 vacuum-agent code is the same target as §5.1 Step 1; chapter never threads this — `L02-Agents.md:438`.
5. §4.6 header doesn't restate "not a row of slide 25" — relies on the §3.7 reminder. Mild redundancy would help — `L02-Agents.md:1088`.
6. "If you only have 20 minutes" should include §5.2 classification table — `L02-Agents.md:62`.

**QA Checklist (§7) status:** N/A — lecture-chapter review, not feature engineering.

**Acceptance criteria (§1) status:** N/A.

**DOCUMENT.md audit:** N/A — lecture artifact, not a code directory.

**Out-of-scope observations:**
- The chapter is now genuinely strong on my lens. The poker→expected-utility→vacuum-world chain is the kind of pedagogical cascade I rarely see in undergraduate lecture notes — analogy in §2, instantiation in §3.3, application in §5.1, cheat-sheet recall in §8. Once P1 R2-#1 lands (the §4 mapping blocks), this is exemplary.
- The line-count is now ~1594 vs round-1's ~1180. The "If you only have 20 minutes" escape valve at L62 is wise. Consider whether a "§9 30-second exam recap" at the very end (six bullets, no prose) would help the night-before reader — but that's a feature suggestion, not a defect.
- The chess discrete-vs-continuous slide-21 pairing (L735–740) is well-handled — it explicitly names the trap of "discrete vs continuous depends on level of abstraction" and reinforces it in pitfall 6. This is something a careful Reviewer #2 / #4 will appreciate.

**Concerns / risks:**
- The §2→§4 mapping inconsistency (P1 R2-#1) is the *only* remaining systematic gap from round 1 — easy fix, but worth doing because round 1 specifically flagged §2→§3/§4 cross-link quality as the largest pedagogical lift. Leaving §4 half-done is a regression-shaped risk for the next round of changes.
- The Reviser may legitimately push back on P1 R2-#3 (slide-25 names in §2 headings) as a Reviewer-#1 trade-off. If they do, that's a defensible call and I'll accept it — but the chapter should then *also* add the slide-25 alternative names to the §2 headings for simple-reflex / table-driven / utility-based / learning, for internal consistency. Currently it's done for 2 of 6 rows.

**What PM should do next:**
- Dispatch Reviser with this report + the other three round-2 reviewer reports.
- Address P1 R2-#1 (mapping blocks in §4) and P1 R2-#2 (scoreboard antecedent) — both are <10 lines of edits.
- P1 R2-#3 is a soft-block; accept Reviser's call.
- I expect to **APPROVE** unconditionally on round 3 if P1 R2-#1 and P1 R2-#2 land.

**DOCUMENT.md updated:** N/A for lecture review.
