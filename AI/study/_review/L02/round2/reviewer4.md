# Reviewer #4 — Exam Readiness (Lecture 2, Round 2)

**Reviewer lens:** Same harsh lens as Round 1. I am imagining the 10
plausible exam questions an SDU AI lecturer would ask on this material
and checking whether a student could answer EVERY ONE using ONLY this
chapter. The user said: *"i dont want to come back from the exam and
say that you guys missed something!"* The bar in Round 2 is whether
the 4 P0s of Round 1 are genuinely closed AND no regressions sneaked
in during the revision.

---

## VERDICT: **APPROVE**

All 4 Round-1 P0s are closed cleanly. All 11 Round-1 P1s are also
addressed (most verbatim, a handful pragmatically). The 10-question
coverage rate has moved from 7/10 to **10/10 fully answerable**. The
revisions did not introduce contradictions, scope creep, or fact
regressions against the source PDF (re-verified against slide 7,
slide 11, slide 23, slide 25, slide 27, slide 29, slide 33).

Findings below are all **P2 polish** — none block lock-in for L02.

---

## ROUND-1 P0 VERIFICATION (the four must-fix items)

### P0-1 (Round 1) — deterministic-vs-stochastic ambiguity for one-shot randomness — **CLOSED**

Round-1 finding: §5.2 called Word-jumble deterministic but Solitaire
stochastic without explaining why a one-shot scramble differs from
a one-shot shuffle.

Round-2 evidence:
- §3.6.2 (lines 683–693 of the revised chapter) now has an explicit
  **convention paragraph**: *"randomness in the initial state of a
  one-shot game … only makes the environment stochastic if it
  continues to inject randomness during play."*
- §5.2 (lines 1247–1252) re-cites this when classifying Word-jumble.
- §5.2 Solitaire follow-on (lines 1278–1284) now reads
  *"deterministic by the §3.6.2 convention (the initial shuffle is
  random, but once dealt, state transitions are deterministic)"* —
  consistency restored.
- §6 pitfall 13 (lines 1417–1423) is a third reinforcement. Three
  hits is enough; a student who reads any of the three lands the
  same convention.

**Verdict: closed.** Cross-references between §3.6.2, §5.2 Solitaire
follow-on, and §6 pitfall 13 are mutually consistent.

### P0-2 (Round 1) — `Dump` action undefined — **CLOSED**

Round-1 finding: chapter mentioned slide 11 extends actions with
`Dump` but never said what `Dump` does.

Round-2 evidence: §3.2 Worked example (lines 421–425) now reads:
*"Extended action set (slide 11): … `Dump`. The lecture does not
formally define what `Dump` does; the standard reading is deposit
collected dirt at a designated cell (e.g. a dustbin square). The
exam may define it either way — if asked, note the ambiguity and
pick the most natural reading."*

This is the right move — gives the student a defensible answer plus
the meta-instruction to flag the ambiguity. PEAS for the vacuum
agent in §3.5 (line 592) also lists `Dump` parenthetically as
"in the slide-11 extension", so cross-references are coherent.

**Verdict: closed.**

### P0-3 (Round 1) — table-driven blow-up qualitative only — **CLOSED**

Round-1 finding: §4.1 says "$|P|^T$ rows" but never plugs in numbers
for the vacuum world.

Round-2 evidence: §4.1 (lines 854–867) now has:
- The corrected closed-form formula $\sum_{t=1}^{T} |\mathcal{P}|^{t}
  = \mathcal{O}(|\mathcal{P}|^{T})$ — addresses reviewer #2's P1-4 in
  the same patch.
- A **five-row blow-up table** for $|\mathcal{P}| = 4$ at $T \in \{1,
  2, 4, 10, 20\}$: 4 / 20 / 340 / ≈1.4×10⁶ / ≈1.5×10¹².
- The prose conclusion *"So even a four-percept vacuum cleaner
  running for 20 time steps would need over a trillion table rows."*

I spot-checked the arithmetic: at $T = 4$, $4 + 16 + 64 + 256 = 340$
— correct. At $T = 10$, $\sum_{t=1}^{10} 4^t = (4^{11} - 4)/3 =
(4{,}194{,}304 - 4)/3 = 1{,}398{,}100$ — correct. At $T = 20$,
$4^{21}/3 \approx 4{,}398{,}046{,}511{,}104 / 3 \approx 1.466 \times
10^{12}$ — correct. **All numbers in the table are arithmetically
sound.**

A student now has both a template formula and a worked example.

**Verdict: closed.**

### P0-4 (Round 1) — PEAS of the vacuum agent missing — **CLOSED**

Round-1 finding: chapter wrote PEAS for taxi and spam filter but
never for the lecture's running vacuum example.

Round-2 evidence: §3.5 (lines 585–595) now includes:

> **PEAS — Vacuum agent of slide 7 (chapter-added — not on the
> slides but a likely exam target):**
> - **P** — Amount of dirt cleaned over a fixed horizon, minus
>   weighted penalties for energy used and noise generated.
> - **E** — Two cells `A` and `B`, each in state `Clean` or `Dirty`;
>   the vacuum is in exactly one cell at a time.
> - **A** — `Left`, `Right`, `Suck`, `NoOp` (and `Dump` in the
>   slide-11 extension).
> - **S** — Location sensor (reports `A` or `B`); dirt sensor
>   (reports `Clean` or `Dirty` for the current cell).

A medical-diagnosis PEAS (lines 597–605) is also added per Round-1
P1-8, giving a non-physical-agent template too. Both are flagged as
*chapter-added* so the student knows they are not slide-quoted.

**Verdict: closed.**

---

## 10 EXAM QUESTIONS — ROUND 2 COVERAGE

The same 10 questions as Round 1, re-run against the revised chapter.

1. **Define agent, agent function, agent program. State the slogan
   that connects them.** → §3.1 (lines 306–308), §3.2 (lines 355–
   370), boxed slogan at line 370. **Passes.**
2. **Give the formal definition of a rational agent. Why does this
   not imply omniscience?** → §3.3 (lines 461–475). The phrase
   "rationality is not omniscience" now appears verbatim at line
   474. **Passes.**
3. **Specify the PEAS for a [vacuum cleaner / spam filter / chess
   robot / medical diagnosis agent].** → §3.5 now covers taxi (lines
   571–576), spam filter (578–583), **vacuum (585–595)**, and
   **medical diagnosis (597–605)**. **Passes — fully answerable.**
4. **Classify [Solitaire / Word-jumble / Chess-with-clock / Scrabble
   / driving] along the six environment dimensions.** → §5.2 (lines
   1236–1291). Solitaire and vacuum-world covered as extension
   exercises (1278–1291). Chess-with-clock now has the correct
   "two dimensions flipped" prose plus the semi-dynamic caveat
   (1253–1262). **Passes.**
5. **Why is the table-driven agent infeasible? Quantify the table
   size for a vacuum agent with 4 distinct percepts after T = 4
   time steps.** → §4.1 (lines 854–867) now has the table.
   Answer: 340 rows. **Passes — student has a worked numeric
   example.**
6. **Draw the block diagram of a model-based reflex agent and label
   every box. Explain the role of the transition model and sensor
   model.** → §4.3 (lines 944–986) embeds slide-29 diagram. Sensor
   model now correctly **flagged as a Russell-&-Norvig 4th-ed
   addition not on slide 29** (lines 952–955) so the student knows
   what to write if the exam asks "what does the slide call it?".
   **Passes.**
7. **Distinguish the four components of a learning agent and
   explain the role of each using the automated-taxi example.** →
   §4.6 (lines 1100–1141). The slide-36 taxi annotation is intact
   with all four role mappings. **Passes.**
8. **Is the slide-7 vacuum agent rational? Under which performance
   measures is it rational and under which is it not?** → §5.1
   (lines 1156–1218). Now includes the 5-step quantitative
   cumulative-performance trace (cumulative = 8). **Passes — and
   stronger than Round 1.**
9. **What is the difference between fully observable and "the agent
   knows everything"? Give an example where these come apart.** →
   §6 pitfall 3 (lines 1346–1351). **Passes.**
10. **For each agent type in the hierarchy, state the minimum
    environment requirement.** → §5.4 (lines 1316–1322) AND
    cheat-sheet §8 (lines 1574–1580). Simple-reflex row now
    correctly attributes the "episodic" qualifier as *practical*,
    not *formal*. **Passes.**

**Coverage rate: 10/10 fully answerable** (vs 7/10 in Round 1).

---

## ROUND-1 P1 VERIFICATION (selected — the ones with exam-risk)

| Round-1 P1 | Status | Evidence |
|---|---|---|
| P1-1 simple reflex "episodic" overclaim | **Closed** | §5.4 line 1318 reads *"Fully observable (slide 27); in practice also easiest when episodic"* — strict slide claim separated from textbook gloss. |
| P1-2 sensor model not on slide | **Closed** | §4.3 lines 952–955 explicitly tag the sensor model as R&N 4th-ed. |
| P1-3 cheat-sheet missing agent-type → env mapping | **Closed** | §8 lines 1572–1580 add the table. |
| P1-4 cheat-sheet missing 2⁶ = 64 | **Closed** | §8 line 1553. |
| P1-5 cooperative vs competitive missing | **Closed** | §3.6.6 (lines 767–775) + §6 pitfall 7 (lines 1380–1386) — two hits. |
| P1-6 semi-dynamic missing | **Closed** | §6 pitfall 5 (lines 1361–1366) + §8 (no explicit one-liner but §5.2 chess-with-clock cell makes the point — acceptable). |
| P1-7 chess-with-clock dynamic-vs-semi-dynamic contradiction | **Closed** | §5.2 lines 1253–1262 now say "flips **two** dimensions" and explicitly reconcile with semi-dynamic textbook reading. |
| P1-8 PEAS for non-trivial agent | **Closed** | Medical diagnosis PEAS added. |
| P1-9 slide-9 table needs explanation | **Closed** | §3.2 lines 390–402 add the variable-length / history-keying / reflex-realisability explainer. |
| P1-10 §5.1 no quantitative trace | **Closed** | Five-row cumulative-performance table added (lines 1198–1209). |
| P1-11 single-agent qualifier misplaced | **Closed** | §3.6.6 line 762 now leads with the *"must affect performance measure"* qualifier. |

All eleven P1s closed.

---

## P0 — MUST FIX (blocks approval)

**None.** All four Round-1 P0s are cleanly closed. No new P0s
introduced.

---

## P1 — SHOULD FIX (requested, not blocking)

**None for this round.** Every Round-1 P1 is now addressed.

---

## P2 — NICE TO HAVE (residual polish, all minor)

### P2-1. Cheat-sheet (§8) could echo *semi-dynamic* as a one-liner.

§5.2 carries the chess-with-clock semi-dynamic note, and §6 pitfall 5
defines the term, but a quick-revision reader on the cheat-sheet
won't see "semi-dynamic" at all. The Static/Dynamic row of the §8
environment-types table (line 1549) could be footnoted *"(textbook
variant: semi-dynamic — world static, score depends on time, e.g.
chess-with-clock)"*. Eight words. Already 99% addressed via the
existing two locations, so this is genuinely P2.

### P2-2. Slide-7 worked PEAS conventionally drops `Dump`.

§3.5 vacuum PEAS lists `Left, Right, Suck, NoOp` and parenthetically
"(and `Dump` in the slide-11 extension)" — consistent with §3.2.
Pedantic note: some exam graders might prefer two PEAS spec lines
(slide-7 baseline vs slide-11 extension). Not necessary, just very-
careful-student-pleasing.

### P2-3. §4.1 row-count table could carry one more "humanise the
number" line.

The blow-up table ends at $1.5 \times 10^{12}$ at $T = 20$. A throw-
away gloss like *"by comparison, the observable universe contains
roughly $10^{80}$ atoms"* would burn the lesson in. (Reviewer #2
will probably tell me this is gratuitous; I'll mark it P2 and let
the PM decide.)

### P2-4. §5.1 cumulative-performance trace assumes the reader knows
the rule is the slide-7 if-then.

Lines 1196–1205: the trace is correct, but explicitly opening with
*"Following the rule of slide 7"* would help students who skipped
§3.2's worked example. P2 — purely a discoverability thing.

### P2-5. The medical-diagnosis PEAS in §3.5 (lines 597–605) is
slightly thinner than the taxi PEAS.

The taxi PEAS gives five Performance items; medical diagnosis gives
two. A single extra example item (e.g. "minimise time-to-diagnosis"
for **P**, or "Electronic Health Records" for **E**) would bring
parity. Minor.

### P2-6. The hierarchy table in §3.7 (lines 802–808) and the
cheat-sheet hierarchy table (§8, lines 1563–1570) are very nearly
the same.

Slight DRY concern. The §8 version adds the analogy column, but
neither version cross-references the other. A note like *"see §8
for the same table with one-line analogies"* on §3.7 would help
mid-study readers find their bearings. Trivial.

### P2-7. §6 pitfall 13 (lines 1417–1423) could repeat the magic
phrase *"transition randomness vs initial-state randomness"*
verbatim.

The convention is established in §3.6.2 (lines 691–693) as
*"randomness in state transitions vs randomness in the initial
setup"* and pitfall 13 paraphrases as *"randomness in *state
transitions*"*. Same idea, slightly different phrasing. Either
phrase is fine on the exam, but using identical wording in both
places makes it easier to memorise.

### P2-8. Cheat-sheet §8 omits the slide-37 summary box's
"perceives and acts" sentence as a separate quotable line.

The summary at line 1582 is there (one-liner takeaway). But the
slide-37 line *"the most challenging environments are partially
observable, stochastic, sequential, dynamic, continuous, and
contain multiple intelligent agents"* (line 1557) is *already*
quoted in §8. Good. P2-1 from Round 1 fully addressed. No further
action.

---

## EVIDENCE

**Source PDF re-checked:** slide 7 (vacuum), slide 11 (Dump appears),
slide 23 (classification table — re-verified pixel-by-pixel against
`study/extracted_figures/L02/slide23-page-render.png`), slide 25
(five-row hierarchy), slide 27 (simple reflex requirement), slide 29
(model-based — confirmed source slide names *one* model, chapter
correctly flags the second as R&N addition), slide 33–36 (learning
agent four roles).

**Chapter sections inspected for revisions:**
- Notation block (lines 13–27): new, correct, addresses reviewer #2's
  P-overload issue while not breaking exam-readiness.
- §1 (lines 31–65): "If you only have 20 minutes" pointer is a nice
  addition.
- §2 (lines 69–293): analogy headings now lead with the *idea* then
  the formal name. Poker player replaces chess for rational agent —
  good move (reviewer #3 P0.4 and Round-1 reviewer #4's "playing the
  odds" angle).
- §3.2 (lines 338–438): worked vacuum example now includes the
  `Dump` definition (P0-2). Slide-9 table explainer added (P1-9).
- §3.5 (lines 550–612): vacuum PEAS (P0-4) and medical PEAS (P1-8)
  added.
- §3.6.2 (lines 673–697): convention paragraph (P0-1).
- §3.6.6 (lines 755–779): cooperative/competitive split + performance-
  measure qualifier moved up (P1-5, P1-11).
- §3.7 (lines 783–820): slide-25 ↔ chapter-name mapping table,
  learning agent flagged as orthogonal extension.
- §4.1 (lines 832–882): row-count formula corrected + blow-up table
  (P0-3).
- §4.3 (lines 940–992): sensor-model R&N tag (P1-2).
- §4.6 (lines 1088–1149): "Teach instead of instructing" call-out
  and four-roles ↔ apprentice ↔ taxi mapping in place.
- §5.1 (lines 1155–1218): cumulative-performance trace (P1-10).
- §5.2 (lines 1220–1291): chess-with-clock two-dimension fix,
  semi-dynamic caveat, Solitaire-deterministic consistency check.
- §5.4 (lines 1309–1328): simple-reflex episodic-qualifier
  re-attribution (P1-1).
- §6 (lines 1332–1423): pitfall 5 (semi-dynamic), pitfall 7
  (cooperative/competitive), pitfall 13 (one-shot randomness)
  — all added or beefed up.
- §8 (lines 1491–1587): agent-type→env table added, 64 figure
  added, slide-37 summary boxed, hierarchy analogies in place.

**10-question coverage test post-revision: 10/10.**

**Spot-checked arithmetic in §4.1 blow-up table — all correct.**

**No regressions detected against source PDF on:** slide 7 actions
(Left/Right/Suck/NoOp), slide 11 actions (adds Dump), slide 23 table
(matches verbatim), slide 25 hierarchy (5 rows, not 6), slide 27
simple-reflex environment requirement (Fully observable), slide 33
four-role learning agent.

---

## Report to PM

**Assignment recap:** Lecture Reviewer #4 (Exam Readiness lens), L02
Round 2. Chapter at `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L02-Agents.md`
verified against source `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture2-Introduction to Agents.pdf`
and Round-1 reviewer #4 report at `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_review\L02\round1\reviewer4.md`.

**Status:** APPROVE. All 4 Round-1 P0s closed. All 11 Round-1 P1s
closed. 10/10 exam-question coverage (up from 7/10 in Round 1). Only
P2 polish remains; none of it gates lock-in.

**Key verifications:**
- P0-1 (det vs stochastic ambiguity): closed via §3.6.2 convention
  paragraph + §5.2 + §6 pitfall 13 — three consistent reinforcements.
- P0-2 (`Dump` undefined): closed in §3.2 worked example + §3.5 PEAS
  cross-reference.
- P0-3 (no numeric table blow-up): closed — five-row table with
  arithmetic-correct 4 / 20 / 340 / 1.4M / 1.5T row counts at
  T ∈ {1, 2, 4, 10, 20}.
- P0-4 (vacuum PEAS missing): closed — PEAS added in §3.5, with
  medical-diagnosis PEAS also added per Round-1 P1-8.
- P1-7 (chess-with-clock self-contradiction): closed — §5.2 now says
  "flips **two** dimensions" and reconciles with semi-dynamic
  textbook reading.

**P0 findings:** None.

**P1 findings:** None.

**P2 findings (residual polish, all optional):**
1. §8 could add a one-line "semi-dynamic" footnote under the Static
   row of the environment-types table — currently buried in §5.2 and
   §6 pitfall 5. *Optional polish.*
2. Vacuum PEAS could list slide-7 baseline and slide-11 extension as
   two separate lines for graders who want strict-source quoting.
   *Optional polish.*
3. §4.1 blow-up table could carry a "for comparison, 10⁸⁰ atoms in
   the universe" gloss. *Reviewer #2 may dislike; defer to PM.*
4. §5.1 trace could open with "Following the rule of slide 7" to aid
   discoverability for skim-readers. *Pure UX.*
5. Medical-diagnosis PEAS slightly thinner than taxi PEAS — add one
   more Performance item for parity. *Cosmetic.*
6. §3.7 hierarchy table and §8 cheat-sheet hierarchy table could
   cross-reference each other. *DRY-cosmetic.*
7. §6 pitfall 13 could use the exact phrase "transition randomness
   vs initial-state randomness" verbatim (matching §3.6.2 wording).
   *Wording polish.*

**Concerns / risks:** None remaining for L02. The chapter is exam-
ready by the exam-readiness lens. If anything, it's *more* coverage
than the slides themselves provide (vacuum PEAS, medical PEAS,
numeric blow-up, cumulative-performance trace) — which is correct
behaviour for a study chapter but should be **flagged** to students
that those extras are *not on the slides* (and the chapter does so
consistently: "chapter-added", "not on the slides but a likely exam
target", etc. — good discipline).

**What PM should do next:** Lock L02. None of the P2s block release.
Update PM/history.md with the L02-lock event and dispatch reviewers
on L03 (next lecture in queue) when ready. Consider applying P2-1
(semi-dynamic cheat-sheet footnote) on the next batch update if a
quick polish pass is scheduled — but it is not required.

**Out-of-scope observations:**
- The chapter cross-refs L03 §3 (transition model), L06 §3.1
  (perfect vs imperfect information), L06 §3.2 (terminal utility),
  L09a §1 (decision under uncertainty), L09a §2–§3 (expected utility
  formalisation), L09b §3 (HMM filtering agent), L10 §1 (learning
  element / RL), L10 slides 5–7 (autonomous example), L11
  (regression / continuous time), L12 (clustering distance). When
  those lectures are written, the L02 cross-refs should be verified.
  Worth handing to the Index Builder as a follow-up.
- The PEAS bin **for `Dump`** is left ambiguous (chapter wisely says
  "the exam may define it either way"). If the lecturer publishes
  a model answer or past-paper rubric that pins `Dump` semantics
  one way, the chapter should be updated to match.
- §6 pitfall 10 ("evaluation function" defined in L06) is a forward
  reference. When L06 is locked, verify the term is defined there
  with a matching cross-link.

**DOCUMENT.md updated:** N/A for review work.
