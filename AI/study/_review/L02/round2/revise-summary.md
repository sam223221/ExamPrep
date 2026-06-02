# L02 Round 2 → Round 3 — Revise Summary

**Artifact revised:** `study/lectures/L02-Agents.md`
**Trigger:** Reviewer #3 (Pedagogical Clarity) APPROVE_WITH_NITS — 3 P1
findings. Reviewers #1, #2, #4 all APPROVED in round 2.
**Goal:** Round 3 will be APPROVED across all four lenses.

---

## P1 findings addressed (Reviewer #3)

### P1 R2-#1 — §4.2 / §4.3 / §4.4 cross-links need element-by-element mapping

**Reviewer's complaint:** §3.x sections all got nice "Mapping:" blocks
in round 2, but §4.2 / §4.3 / §4.4 still said only "Recall the X
analogy from §2" with no element mapping. Inconsistent with §3.

**Fix applied:** Added 2-3 line italic "Mapping:" extension to the
opening blockquote of each of §4.2, §4.3, §4.4, in the same style as
§3.x. Each mapping names the analogy-element ↔ formal-element pairs
the reviewer asked for.

- **§4.2 (line 887):** vending-machine **button press** ↔ **current
  percept**; **internal wiring** ↔ **condition-action rule**; the
  **lack of state between transactions** ↔ why the architecture needs
  **fully observable** environments (forward-link to §3.6.1).
- **§4.3 (line 942):** **driver** ↔ agent; **mental picture through
  fog** ↔ **internal state**; **experience of how cars move** ↔
  **transition model**; **expectation of what they'd see if the fog
  lifted** ↔ **sensor model** (R&N 4th-ed addition flagged).
- **§4.4 (line 996):** **destination address** ↔ **goal state**;
  **road graph** ↔ **transition model** (inherited from §4.3);
  **route computed ahead** ↔ **action sequence** produced by SEARCH;
  **next-turn instruction** ↔ `plan.first()` — the first action of
  that sequence.

The reviewer specifically suggested the §4.3 mapping verbatim; we
adopted the suggested phrasing (slight rewording: "driver's experience
of how cars move" rather than "constant velocity, friction" since the
chapter's analogy in §2 uses "model of how the world evolves" — kept
consistent).

### P1 R2-#2 — Cheat-sheet "scoreboard" analogy for utility function had no §2 antecedent

**Reviewer's complaint:** Cheat sheet line 1519 says *"Utility
function. … Like the score on the scoreboard."* but §2 never says
"scoreboard" anywhere. The §2 "satnav with preferences" entry covers
the *utility-based agent* — an architecture — but the utility function
itself (a mathematical object) didn't get its own scoreboard line.

**Fix applied (option (a) from the reviewer's suggestion):** Reworked
the §2 "A satnav with preferences" entry to:

1. Rename the heading to "**A satnav with preferences — utility-based
   agent (and utility function)**" so the entry now carries both
   concepts.
2. Add a sentence that gives the utility function its own analogy:
   *"The utility function itself is like the score on a scoreboard:
   a single real-valued number attached to each state that says how
   well things are going there, independent of which agent
   architecture reads the scoreboard."*
3. Reframe the next sentence so it is clear that the utility-based
   agent is the architecture that *reads* the scoreboard, while the
   utility function is the scoreboard itself.

This both creates a §2 antecedent for the cheat-sheet reminder *and*
fixes Reviewer #3 P2 R2-#2 (the glossary banner promises "utility
function" as a top-level concept but §2 bundled it; now it has a
dedicated sentence). Two birds, one stone.

### P1 R2-#3 — Slide-25 alternative names in §2 headings re-clutter the "idea-first" intent

**Reviewer's complaint:** L224 and L239 had slide-25 names injected
into the §2 headings ("model-based reflex agent (slide 25 calls this
'Agents with memory')"). Only 2 of 6 hierarchy rows got this
treatment — inconsistent. And the chapter explicitly says (L75-77)
that §2 should "meet the intuition before the jargon"; three jargon
items in a heading defeats that.

**Fix applied:** Removed the slide-25 parenthetical from the §2
headings of "A driver in fog" and "A satnav". Moved the alternative
name into one sentence at the **end** of the §2 entry's body so
slide-25 cross-reference is preserved (so Reviewer #1's slide-25
alignment is still honored) but the heading stays idea-first:

- §2 model-based reflex entry now ends with: *"(slide 25 of the source
  calls this row 'Agents with memory' — the §4.3 heading anchors both
  names)."*
- §2 goal-based entry: same treatment, anchored to §4.4.

The §4.x headers continue to carry both names (§4.3, §4.4), so the
slide-25 anchor is intact — just relocated from §2 (analogies-first)
to §4 (formal-name-first), which is exactly the reviewer's
recommendation.

---

## Low-cost P2 polish also applied

### Reviewer #3 P2 R2-#1 — One-word forward-pointers in §1

**Fix:** L51 "performance measure" now reads "performance measure
(defined formally in §3.3)"; L53 "environment taxonomy" now reads
"environment taxonomy — formalised in §3.6". Symmetric with the
existing inline gloss of "architectures".

### Reviewer #3 P2 R2-#3 — "Optimal action" cheat-sheet bullet lacked an analogy reminder

**Fix:** §8 cheat-sheet "Optimal action" now ends with: *"Like picking
the bet with the highest expected-value chip stack — the action whose
scoreboard reading you'd most like to land on."* Re-uses both the
poker domain (consistent with the expected-utility analogy two bullets
up) and the new scoreboard analogy (consistent with the utility-function
analogy).

### Reviewer #3 P2 R2-#6 — "If you only have 20 minutes" should include §5.2

**Fix:** §1 pointer at L62 now includes §5.2 as the fourth must-read:
"§2 (analogies), §8 (cheat sheet), §6 pitfalls 1–3, and **§5.2 (the
four-environment classification table — the single most exam-quotable
artifact in the chapter)**."

### Reviewer #2 P2-1 — Deterministic-only argmax framing in §4.5

**Fix:** §4.5 line 1080 now reads: *"The first two cases only need
$\arg\max_{a} U(\text{Result}(s, a))$ (in the deterministic special
case, where $\text{Result}(s, a)$ is a single state, so
$U(\text{Result}(s, a))$ is a single real number); the third needs the
full expected-utility argmax above."* Type-checks now: the bare argmax
form is only valid in the deterministic special case, which the prose
now explicitly says.

### Reviewer #2 P2-2 — "string" → "sequence" in the notation block

**Fix:** Notation block (L15) now says "finite sequence" instead of
"finite string" — matches §3.2 L350 internal phrasing.

### Reviewer #4 P2-1 — Semi-dynamic footnote on the §8 cheat-sheet Static/Dynamic row

**Fix:** Extended the "Static vs dynamic" test-question cell in the
§8 environment-types table with a parenthetical: *"(textbook variant:
**semi-dynamic** — world static but score depends on time, e.g.
chess-with-clock)"*. Adds the term to the quick-revision reader's eye
without enlarging the table footprint.

---

## P2 findings NOT applied (and why)

The following round-2 P2s from various reviewers were considered and
deferred — they are either purely stylistic or risk introducing new
material that wasn't requested:

| Reviewer | P2 | Why deferred |
|---|---|---|
| R#1 P2-1 | Slide-33 canonical learning-agent component order vs chapter's apprentice-temporal order | The chapter's order is pedagogically defensible (the reviewer agrees) and Reviewer #4 verified all 10 exam questions are answerable. Adding a slide-order note would add jargon to §4.6 without changing answers. |
| R#1 P2-2 | §5.2 chess-with-clock "Dynamic (semi)" annotation vs byte-for-byte slide-23 "Dynamic" | The chapter explicitly flags this deviation in the prose (lines 1258–1262); moving the annotation into the prose only would lose a memorisable cell. Reviewer #2 also approved this current form. |
| R#2 P2-3 | One-line `^*` (Kleene vs argmax) disambiguation | Pure style; the notation block introduces both uses individually and the field-standard reuse is unambiguous in context. |
| R#3 P2 R2-#4 | §3.2 vacuum-agent code "(same agent we evaluate in §5.1)" thread | Nice-to-have; chapter already cross-links §5.1 from §3.3. |
| R#3 P2 R2-#5 | §4.6 header reminder "not a row of slide 25" | Already stated clearly in §3.7 L814-818. Adding a duplicate to §4.6 risks redundancy without new information. |
| R#4 P2-2 | Two-line vacuum PEAS (slide-7 baseline + slide-11 extension) | Chapter parenthetically notes the extension already; splitting into two PEAS specs is gratuitous for a study chapter. |
| R#4 P2-3 | "10⁸⁰ atoms in the universe" gloss on row-count table | Reviewer #4 themselves flagged this as something Reviewer #2 would dislike; deferring. |
| R#4 P2-4 | §5.1 "Following the rule of slide 7" preface | The step-1 table already shows the rule; redundant. |
| R#4 P2-5 | Beef up medical-diagnosis PEAS with more Performance items | The medical PEAS is chapter-added and intentionally compact as a counterpoint to the slide-quoted taxi PEAS. |
| R#4 P2-6 | §3.7 ↔ §8 hierarchy table cross-reference | DRY-cosmetic; both tables are titled identically and easy to find. |
| R#4 P2-7 | Verbatim "transition randomness vs initial-state randomness" in pitfall 13 | Current paraphrase is fine; reviewer noted it. |

---

## Verification notes

- Reviewer #3's specific concern (lines 274-277): *"I expect to
  APPROVE unconditionally on round 3 if P1 R2-#1 and P1 R2-#2 land."*
  Both have landed.
- Reviewer #3's P1 R2-#3 (slide-25 names in §2 headings): the reviewer
  flagged this as a "soft-block; accept Reviser's call". We chose the
  reviewer's preferred resolution (remove from heading, keep in body)
  rather than the alternative (add slide-25 names to all 6 §2 rows for
  consistency). This is the cleaner pedagogical outcome — §2 stays
  idea-first; §4.x headers remain the slide-25 anchor.
- No other reviewer flagged any P0 or P1, so no work is required for
  R#1, R#2, R#4. Their P2s that were low-cost have been applied; the
  rest are documented above with rationale.
- Notation block "string" → "sequence" is consistent with §3.2 line 350.
- No new figures referenced; no figures removed.
- No formulas changed; one formula's prose framing was tightened (the
  deterministic-only argmax in §4.5).
- The §2 "satnav with preferences" entry now has a sub-heading that
  reads "(and utility function)" — this is a deliberate two-concept
  entry (Reviewer #3 explicitly wanted this distinction made clear).

---

## Expected round-3 outcome

- **Reviewer #1 (Concept Completeness):** Was APPROVED in R2 with 2
  trivial P2s. None of our R3 edits regress or affect those P2s.
  Expect APPROVED.
- **Reviewer #2 (Mathematical Rigor):** Was APPROVED in R2 with 3 P2s;
  P2-1 and P2-2 are now applied. P2-3 (the optional `^*` note) is the
  only one outstanding and is purely cosmetic. Expect APPROVED.
- **Reviewer #3 (Pedagogical Clarity):** All 3 P1s applied. Reviewer
  explicitly said "I expect to APPROVE unconditionally on round 3 if
  P1 R2-#1 and P1 R2-#2 land." Both have. Expect APPROVED.
- **Reviewer #4 (Exam Readiness):** Was APPROVED in R2 with 8 P2s; one
  (P2-1, the semi-dynamic cheat-sheet footnote) is now applied. The
  other 7 are documented as deferred. Expect APPROVED.

L02 should LOCK after round 3.
