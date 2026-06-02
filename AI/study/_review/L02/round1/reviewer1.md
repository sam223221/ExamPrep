# Reviewer #1 — Concept Completeness — L02 Round 1

## VERDICT
NEEDS_REVISION

The chapter is genuinely thorough — every major concept is named and defined, and every USE/REWORK figure is embedded — but there are several **named items from the source slides that are missing or under-covered** and one **non-trivial slide-vocabulary mismatch** between the chapter and slide 25's official hierarchy names. Those are exam-critical because the lecturer's exam will use the slide's vocabulary, not Russell & Norvig's. Flagging as NEEDS_REVISION (one P0 + four P1s).

## P0 — MUST FIX (blocks approval)

1. **Slide 25's official hierarchy names are not reconciled with the chapter's terminology — risks costing marks on a "list the hierarchy" exam question.**
   - Slide 25 names the five rungs verbatim: **(1) Table-driven agents, (2) Simple reflex agents, (3) Agents with memory, (4) Agents with goals, (5) Utility-based agents.** The chapter calls rung (3) "Model-based reflex agent" (§4.3 header and throughout) and never tells the student that the lecturer's slide-25 name for the same thing is **"Agents with memory"**. Similarly rung (4) is named "Goal-based agent" in the chapter but "Agents with goals" on the slide.
   - WHERE: §3.7 (Hierarchy of agent types) and §4 section headers, and the §8 cheat-sheet "Agent hierarchy" block.
   - REQUIRED FIX: in §3.7 add an explicit mapping table — "Slide-25 name ↔ Russell-&-Norvig / chapter name" — covering all five rungs. Then add a parenthetical on each §4.x header (e.g. "§4.3 Model-based reflex agent (slide 25: 'Agents with memory')"). Also fix the cheat sheet (§8) accordingly. SOURCE: slide 25.

## P1 — SHOULD FIX (requested, not blocking)

1. **Slide 16's parenthetical "(unobservable?)" is missing.**
   - WHERE: §3.6 (Environment types) and §3.6.1 (Fully vs partially observable).
   - SOURCE: slide 16 lists "Fully observable vs. partially observable (**unobservable?**)" — the parenthetical hints at a third extreme (no observability at all) that the lecturer may probe in an exam discussion question. The chapter doesn't mention "unobservable" at all.
   - FIX: add one sentence in §3.6.1 noting that the slide explicitly names an "unobservable" extreme — agent gets no useful percepts and must operate entirely on its model — and that this is the degenerate case at the partial-observability end of the spectrum.

2. **Slide 21's note "Time can also evolve in a discrete or continuous fashion" is dropped.**
   - WHERE: §3.6.5 (Discrete vs continuous).
   - SOURCE: slide 21 bullet sub-point.
   - FIX: add a sentence noting that the discrete/continuous distinction also applies to **time** (discrete-time vs continuous-time environments). Important because L09b HMMs use discrete time and L11 regression often uses continuous time, so the student will want this distinction primed here.

3. **Slide 24's compact one-line definitions are nowhere reproduced as a single block.**
   - WHERE: §3.6 or §8 cheat sheet.
   - SOURCE: slide 24 — gives a six-bullet glossary-style summary (Observable, Deterministic, Episodic, Static, Discrete, Single agent) with one-line definitions each. The chapter has a *test-question* table in §3.6 (`Do sensors give the complete state?` etc.) but not the *property-definition* table that slide 24 actually presents.
   - FIX: add an "Environment-type definitions (slide 24)" mini-table in §3.6 with the slide's exact wording — "Observable: access to the complete state of the environment", "Deterministic: the next state is completely determined by the current state", etc. Useful as a verbatim quotation pool for short-answer exam questions.

4. **Slide 33's phrasing "Teach instead of instructing" is not reproduced.**
   - WHERE: §4.6 (Learning agent).
   - SOURCE: slide 33 bullet — one of three "advantages" the slide lists for learning agents. The chapter mentions "robustness in initially unknown environments" but not "Teach instead of instructing" — the latter is the most exam-quotable framing (it captures the philosophical pitch behind ML).
   - FIX: add the phrase to §4.6 with a one-sentence unpack.

5. **Slide 33's lecture-agent name is "Learning/Autonomous agent" but the chapter section is titled "Learning agent" only.**
   - WHERE: §4.6 header.
   - SOURCE: slide 33 (and slides 34, 35 use the same title verbatim).
   - FIX: rename §4.6 header to "Learning / Autonomous agent" (or add the parenthetical) and add a sentence pointing out *why* the slide compound-names them: an agent that learns from its own experience is what we earlier defined (§3.4) as *autonomous*, so the learning architecture IS the architectural realisation of autonomy. Currently this connection is made tangentially in §3.4's cross-reference but not echoed at §4.6's title.

## P2 — NICE TO HAVE

1. **Worked Example 5.2's "exam-style follow-on" (Solitaire, vacuum world classification) is not from the slides** — pedagogically useful but a student could mistake it for an official lecture example. Add a one-line "extension exercise — not on the slides" disclaimer at the top of the follow-on.

2. **Slide 2's "Intelligent Agents" section header** is treated as decorative SKIP. Reasonable, but a one-sentence acknowledgement in §1 ("Russell & Norvig and this course use 'intelligent agent' and 'rational agent' interchangeably — slide 2's title makes this implicit") would tie the terminology together.

3. **Slide 27 footnote: "Examples of classic if-then algorithms: if (I sense a certain input) then (I apply a specific rule)"** — this exact gloss is missing from §4.2. Including the slide's literal phrasing helps with recognition on exam day.

4. **Slide 10 uses "Performance measure (utility function)"** — i.e. *parenthetically equates them*. The chapter does flag this in §3.3 and Pitfall #10, but a more prominent inline reminder at first mention (§3.3 first paragraph) would help. Currently the equivalence is buried in a long paragraph.

5. **Slide 22 mentions cooperative vs competitive multi-agent split implicitly via L06 cross-ref.** Chapter §3.6.6 does flag this. The pitfall list (item 7) also touches it. Could be slightly more prominent given how often it appears on exam questions about adversarial search.

6. **Slide 13's three bullets are reproduced in §3.4 but not as a compact verbatim quote-bank.** Consider adding the slide's literal wording as a fenced quote in §3.4 — Russell & Norvig phrase autonomy slightly differently than the slide, and the slide wording is what the exam will use.

7. **Quote precision check** — §3.3 line: *"Design performance measures according to what you want in the environment, rather than how you think the agent should behave"* is a verbatim slide-12 quote. Match — good. But the chapter renders it without quote marks in §3.3 / §5.1 take-away — adding emphasis would help mark it as a "memorise this" line.

## EVIDENCE

**Slides reviewed:** all 38 pages of `Lecture2-Introduction to Agents.pdf` — i.e. slides 1–38. Specifically verified slide-by-slide:
- Slides 1–3: front matter, outline.
- Slides 4–6: agent definition, sensors/actuators table, terminologies (P, P*, f: P*→A, program, architecture+program=agent).
- Slides 7–9: vacuum-cleaner world, simple agent function, percept-sequence/action table.
- Slides 10–12: rational agent, performance measure (= utility function), vacuum example, design slogan.
- Slide 13: autonomy.
- Slides 14–15: PEAS examples (taxi, spam filter).
- Slides 16–22: six environment-type dimensions (one slide each).
- Slide 23: four-environment classification table.
- Slide 24: environment-type definitions glossary.
- Slide 25: agent-type hierarchy (5 rungs with verbatim names).
- Slide 26: table-driven agent problems.
- Slides 27–28: simple reflex agent (diagram + REFLEX-VACUUM-AGENT pseudocode).
- Slides 29–30: model-based reflex (diagram + REFLEX-AGENT-WITH-STATE pseudocode).
- Slide 31: goal-based agent diagram.
- Slide 32: utility-based agent diagram.
- Slides 33–36: learning/autonomous agent diagram with three call-out builds + automated-taxi example.
- Slide 37: summary.
- Slide 38: thank-you (N/A).

**Chapter sections inspected:** §1 (Overview), §2 (Analogies — all 12 listed), §3.1–§3.7 (core concepts), §4.1–§4.6 (algorithms / methods), §5.1–§5.4 (worked examples), §6 (12 pitfalls), §7 (cross-refs), §8 (cheat sheet).

**Figures verified:**
- All 10 USE figures embedded in chapter at sensible sections (fig03 §3.1, fig05 §3.2 / §5.1, fig07 §3.2, slide23-page-render §5.2, slide25-page-render §3.7, fig27 §4.2, fig29 §4.3, fig30 §4.4, fig31 §4.5, fig32 §4.6).
- All 12 REWORK figures embedded as paired-side-by-side under §3.6.1–§3.6.6.
- All 13 SKIPs cross-checked: duplicates (fig04, fig06, fig08, fig09, fig10, fig28), thumbnails subsumed by page-render (fig23, fig24, fig25, fig26, slide09-page-render), decoratives (fig01, fig02) — all justified in figures.md.
- Filesystem audit: all 35 PNGs catalogued exist on disk in `study/extracted_figures/L02/`. No catalogue↔chapter mismatch. No referenced figure missing from disk. No figure on disk silently dropped from the catalogue.
- No informative figure from the source PDF appears to have been missed: the only slides without a corresponding figure entry are pure-text slides (1, 3, 5, 10, 13, 14, 15, 16, 24, 26, 30, 34, 35, 37, 38) — confirmed against the PDF.

---

## Report to PM

**Assignment recap:** Reviewer #1 (Concept Completeness incl. Figures) for L02 (Agents), Round 1. Spec lens: `docs/superpowers/specs/2026-05-22-ai-exam-prep-study-package-design.md` §7.1.

**Status:** NEEDS_REVISION (1 P0, 5 P1, 7 P2).

**P0 findings:**
1. Slide-25 hierarchy names ("Agents with memory", "Agents with goals", etc.) are never reconciled with the chapter's Russell-&-Norvig terminology ("Model-based reflex", "Goal-based") — exam-critical vocabulary mismatch. WHERE: §3.7, §4 headers, §8 cheat sheet.

**P1 findings:**
1. Slide 16 "(unobservable?)" parenthetical missing — §3.6.1.
2. Slide 21 "Time can also evolve in a discrete or continuous fashion" dropped — §3.6.5.
3. Slide 24's verbatim one-line environment-type definitions not reproduced in one block — §3.6.
4. Slide 33 "Teach instead of instructing" not reproduced — §4.6.
5. Slide 33 / 34 / 35 title is "Learning / Autonomous agent" but chapter §4.6 header is "Learning agent" only — autonomy↔learning link weakened.

**P2 findings:**
1. Worked-Example 5.2 "exam-style follow-on" is not from slides — needs disclaimer.
2. Slide 2 "Intelligent Agents" title could earn a one-line acknowledgement in §1.
3. Slide 27 "if (I sense a certain input) then (I apply a specific rule)" footnote not reproduced — §4.2.
4. Slide 10's "performance measure (utility function)" equivalence could be more prominent at first mention — §3.3.
5. Slide 22 cooperative-vs-competitive multi-agent split could be slightly more prominent — §3.6.6.
6. Slide 13's three autonomy bullets could appear as a fenced verbatim quote in §3.4.
7. Slide 12 "Design performance measures according to what you want…" should be marked as a verbatim exam-quotable line, ideally with quote marks.

**QA Checklist (§7.1) status:**
- Cross-checked every slide against chapter: **partially pass** (one P0 vocabulary mismatch, four P1 verbatim-content gaps).
- Every named concept defined: **pass** — all glossary terms are named and defined.
- Every formula reproduced: **pass** — `f: P* → A`, `Agent = architecture + program`, expected utility sum, `a* = argmax E[U(Result(s,a))]` all present. (Slide 10 has no formal formula; chapter adds the expected-utility one as a forward link to L09a — appropriate.)
- Figures catalogue audit: **pass** — every USE/REWORK embedded, every SKIP justified, no informative figure dropped, no chapter↔catalogue mismatch.

**Acceptance criteria (§1 of plan) status:**
- "Cover every slide": **partially met** — P0 + P1s flag missing/under-covered slide content.
- "Name and define every named concept": **met** — all are present (the P0 is a *naming* alignment issue, not a *missing* concept).
- "Every formula reproduced": **met.**

**DOCUMENT.md audit:** N/A — `study/_review/` and `study/lectures/` are not directories with new feature-engineering code; no DOCUMENT.md is required by the lecture-extractor protocol. The figures catalogue `figures.md` is the analogous artifact for the figures directory and is present and complete.

**Out-of-scope observations:**
- The chapter's cross-reference forward to L09a §1 / §2-§3 should be verified when L09a is locked — currently it's a hopeful link. Not a Round 1 issue.
- §5.2 "exam-style follow-on" extension exercises (Solitaire, vacuum) are pedagogically useful but should ideally have answer keys; not the lecture-extractor's job, but worth noting for the App Tester / Verifier phase.

**Concerns / risks:**
- The single P0 (slide-25 vocabulary alignment) is real exam exposure: a student answering "list the five agent types in the hierarchy" who writes "Model-based reflex" instead of "Agents with memory" may be marked partially wrong if the lecturer grades strictly to the slide. This is exactly the kind of thing the user said they don't want to come back from the exam and find missed.

**What PM should do next:** Dispatch Reviser with this report (plus the other three reviewers' reports). The P0 fix is a localised insert (one mapping table + five parenthetical updates) — should take one revision pass. After revision, re-dispatch the four-reviewer batch for Round 2.

**DOCUMENT.md updated:** N/A for QA.
