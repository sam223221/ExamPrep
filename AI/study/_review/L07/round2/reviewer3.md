# L07 — Round 2 — Reviewer 3 (Pedagogical Clarity incl. Analogies)

**Scope:** Spec §7.1. Re-verify Round 1 findings (3 P0, 7 P1, 7 P2) after reviser produced §2.8 / §2.9 / §2.10, restored cross-links, and reformatted breakdown caveats. Be harsh.

**Source:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture7-Constraint Satisfaction Problem.pdf`
**Chapter:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L07-CSP.md`
**Round 1 review:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_review\L07\round1\reviewer3.md`
**Round 1 summary:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_review\L07\round1\revise-summary.md`

---

## VERDICT

**PASS (with minor concerns).**

All three Round 1 P0 findings have been **genuinely closed**. §2 now contains ten subsections — one analogy per glossary concept on the front-matter line — every analogy has a dedicated "Where it breaks down" blockquote, and the cross-link audit is now bidirectional: each §3/§4 section pointing to its §2.x home, and the new §2 preamble carries a `§2.x → §3/§4` table for analogy-side discoverability. The previously orphan §2.1 (Sudoku) now has explicit recalls from §3.1 (L141), §3.4.4 (L301), and §4.1 (L364). §2.7 (outfit-trying) is now recalled from §4.1 (L364) in addition to the prior §4.2 recall. The "maiden aunt" sentence has been extracted out of §2.2 into its own §2.9 with a dedicated degree-heuristic-specific breakdown caveat, leaving §2.2 cleanly about the constraint graph only.

The three new analogies — §2.8 *Tetris board mid-game* for consistent assignment, §2.9 *Seating the maiden aunt first* for the degree heuristic, §2.10 *Newton's cradle cascade* for constraint propagation — are well-pitched, each with a meaningful breakdown caveat, and the Newton's cradle / customs queue pairing for constraint propagation vs. arc consistency is genuinely clever (the cradle captures the *cascade shape*, the customs queue captures the *directionality*, and §2.10's caveat explicitly hands the directionality back to §2.6 with `for that, return to §2.6's customs queue`). All seven prior analogies have been upgraded from bulleted-italic to `> **Where it breaks down.** …` blockquote, satisfying P1-6. The §8 cheat-sheet's "Seat the maiden aunt first" entry now cross-links to §2.9 (L828), closing the P1-7 inconsistency from a second angle. P1-2 (the "clipboard" typo in §2.5) and P1-3 (customs queue directionality) and P1-4 (MRV caveat self-contradiction) are all resolved cleanly. P2-7 and P2-3 (stale section pointers) are fixed: §2.1 now points to "§4.6 (forward checking) and §4.8 (arc consistency)" and §2.5 now points to "§4.8".

The few remaining concerns are P2-grade: §2.5's caveat is now two paragraphs (one for the formulation mismatch, one for the look-ahead horizon) and the *visual* break between them as blockquote-followed-by-blockquote-continuation is correct but slightly cramped; §2.10's "asymmetric and lossy" caveat is accurate but the *lossy* point will not land for a student who hasn't yet encountered the §4.8 cascade — the chapter could either re-order to put §2.10 immediately after §2.6 instead of after §2.9, or accept that §2 is sequenced by glossary-front-matter order. Neither blocks shipping.

---

## P0 — Blocking

(none — all three Round 1 P0s closed)

---

## P1 — Important

(none — all seven Round 1 P1s closed)

---

## P2 — Polish

### P2-1. §2.6 customs-queue blockquote is now two stacked blockquotes — the rendering may collapse them

L92–94 of the revised chapter ships the §2.6 caveat as:

> **Where it breaks down (analogy-level).** First, *values* are the passport-pages, not the passport itself; you tear out pages, not whole passports. Second, the cascade does not *modify* $Z$'s claims by edict of $X$ — $Z$ only loses pages via its own consistency re-check against $X$'s now-reduced domain. This subtle directionality is exactly what §6 pitfall #7 warns about: when $X$ shrinks, you re-add arcs $Z \to X$ (not $X \to Z$) to the worklist.
>
> **Where it breaks down (theory-level).** Arc consistency only checks *pairs*. There exist CSPs where every pair is arc-consistent yet the global problem has no solution; you need stronger consistency (path consistency, $k$-consistency) for those. Outside the scope of this course, but worth knowing exists.

The substance is correct and addresses the P1-3 directionality concern from Round 1, but markdown renderers will collapse the two blockquotes into one visually-continuous block (the `>` on the blank line creates a soft break, not a hard separator). On a quick skim a student will see one large blockquote and may miss that *analogy-level* and *theory-level* are distinct concerns. This is the only §2 caveat that has two parts; the rest are single blockquotes.

**Suggested fix:** either split into two adjacent blockquotes with a non-`>` blank line between them (`> **Where it breaks down (analogy-level).** …\n\n> **Where it breaks down (theory-level).** …`), or fold into one blockquote with explicit bold-led sub-bullets (`> **Analogy-level:** …  **Theory-level:** …`). Either way is a minor render-quality fix.

### P2-2. §2.10 (Newton's cradle) "lossy" caveat is forward-looking — moot at first read

L118: "*Where it breaks down.* A Newton's cradle is symmetric and lossless; constraint propagation is asymmetric (arcs are directed) and lossy (every pruning step shrinks the search space, you never 'get values back')."

This is correct, but a student reading §2 in linear order encounters §2.10 *before* §4.8 — they have no concrete picture of "shrinks the search space" yet. The caveat works at second read; on first read it asserts properties the reader cannot evaluate. The customs-queue analogy in §2.6 has the same problem in theory, but its caveat is anchored on the more concrete "passport pages" image. §2.10's caveat is more abstract.

**Suggested fix:** insert a concrete one-clause example before the abstract claim: "*Where it breaks down.* A Newton's cradle is symmetric and lossless; constraint propagation is asymmetric (e.g. in §2.6's customs analogy, $X$ shrinking forces re-checking $Z \to X$, but *not* $X \to Z$) and lossy (once a value is pruned it never returns)." The reference back to §2.6 ties the two analogies together and grounds the otherwise-abstract claim.

### P2-3. §2 mapping table at L42–55 lists §2.9 → §4.4 but the in-text recall at §4.4 is single-target

L429: `*Recall §2.9: degree heuristic = seating the maiden aunt first.*`

This is fine, but §4.4 is a single section covering *both* MRV and degree heuristic, and §2.3 (MRV) is also pointed at §4.4 in the mapping table. The §4.4 in-text intuition lines are:

- L419: `Intuition (§2.3): pick the most-cornered square.` — for MRV.
- L429: `*Recall §2.9: degree heuristic = seating the maiden aunt first.*` — for degree heuristic.

So the two analogies map to two paragraphs of §4.4, and the mapping table is correct in pointing both at "§4.4" — but a reader following the table from §2.9 will land at the top of §4.4 (MRV) and have to scroll to find the degree-heuristic paragraph. Likewise §2.3 → §4.4 lands on MRV, which is correct.

**Suggested fix:** if a future revision becomes possible, refine the table entries to `§4.4 (MRV paragraph)` and `§4.4 (degree heuristic paragraph)` — or split §4.4 into §4.4.1 (MRV) and §4.4.2 (degree heuristic). Currently merely cosmetic; do not block.

### P2-4. §2.5 (forward checking) now has two stacked breakdown blockquotes — same rendering caveat as P2-1

L85–86:

> **Where it breaks down.** This analogy maps cleanly only onto the compact n-queens formulation (§3.4.2 alternative), where each future row's *domain* is the candidate list. In the slide-12 formulation (one Boolean per cell) forward checking still works, but in terms of cell-variable domains shrinking from `{0,1}` to `{0}`, not in terms of "future queens with no square left". The principle — prune unassigned variables' domains, backtrack when one empties — is identical; the picture differs.
> Also, forward checking only looks one step ahead. It cannot see that two *currently legal* values, in two *currently unassigned* variables, are mutually inconsistent — e.g. NT and SA both having only `{blue}` left after assignment of WA and Q. **Arc consistency** (§4.8) closes this gap.

Same issue as P2-1: two distinct concerns in the same caveat (formulation-mismatch and look-ahead-horizon), and the second is *not* led by a `**Where it breaks down.**` cue — it appears as continuation prose. A student skimming will read "domain shrinking from `{0,1}` to `{0}`" and then jump straight to §2.6 without noticing the look-ahead-horizon limit. The look-ahead-horizon point is **the** intellectual bridge to arc consistency; it should not be a tail.

**Suggested fix:** lead the second paragraph with its own bolded cue, e.g. `> **Where it also breaks down.** Forward checking only looks one step ahead. …`. Or restructure as a bulleted list inside the blockquote.

### P2-5. §2 preamble mapping table (L44–55) is incomplete vs. the recall-link audit

The mapping table lists each §2.x with one or two formal section homes, but several §2.x are recalled from *more* sections than the table shows. For instance:

- §2.1 (Sudoku) is recalled from §3.1 (L141), §3.4.4 (L301), §4.1 (L364) — three places — but the table at L46 lists only "§3.1, §3.4.4". §4.1 is missing.
- §2.7 (outfit-trying) is recalled from §4.1 (L364) and §4.2 (L399) — but the table at L52 lists only "§4.1". §4.2 is missing.
- §2.10 (Newton's cradle) is recalled from §4.6 (L473) and §4.8 (L595) — table at L55 lists both correctly. ✓

These are minor undercounts; the directionality of the table (analogy → formal) is intact, just not exhaustive.

**Suggested fix:** expand the entries that have two recall targets to list both, e.g. `§2.1 Sudoku grid | CSP | §3.1, §3.4.4, §4.1`. Not blocking.

### P2-6. §2.8 (Tetris) cross-link from §3.1 is correct but §6 pitfall #1 (the table at L741–747) doesn't recall §2.8

§6 pitfall #1 (L741) is the *exam-trap consequence* of the consistent-vs-complete distinction, and §2.8 (Tetris) is the *analogy*. A reader scanning §6 for exam traps would benefit from a `*Recall §2.8: Tetris board mid-game.*` line beneath the table. The Round 1 review explicitly observed that the consistent/complete confusion is exam-trap #1 — and now §2.8 exists, but §6 doesn't cite it.

**Suggested fix:** add `*Recall §2.8: a Tetris board mid-game is the canonical consistent partial assignment — partial-and-clean, contrasted against the all-red Australia row above which is complete-and-dirty.*` after the table at L749. Symmetric with the §3 and §4 italic recall pattern.

### P2-7. §2.9 (maiden aunt) "feuds with guests who already have their tables decided" — minor analogy strain

L112: "*Where it breaks down.* The maiden aunt may have many feuds but also be irrelevant to the actual seating problem if those feuds are with guests who already have their tables decided — degree counts *edges to unassigned neighbours*, not their tightness."

The "feuds with guests who already have their tables decided" clause is semantically close-but-not-quite to the degree-heuristic definition: degree counts edges to *unassigned* neighbours, so a feud with an *already-seated* guest does **not** contribute to degree. The caveat is therefore saying: "even after counting only unassigned-neighbour edges, degree may still over-rank the aunt because edge-count doesn't measure constraint tightness". This is correct but the phrasing — "feuds with guests who already have their tables decided" — slightly muddles the picture: those feuds are *already* not counted, so they're not the reason degree mis-ranks. The real failure mode is: among *unassigned* neighbours, the aunt's feuds may all be slack (e.g. dietary preferences that any table can satisfy) while a different guest's three feuds may all be hard.

**Suggested fix:** rephrase to: "*Where it breaks down.* Even counting only edges to still-unassigned neighbours, degree measures **how many** constraints a variable participates in — not **how tight** any individual constraint is. The maiden aunt may have five mild dietary feuds and lose to a guest with three irreconcilable seating constraints. Also, on its own (as the primary variable selector) the degree heuristic is **only a tie-breaker** for MRV; slide 27 explicitly frames it as such."

### P2-8. §3.1 italic recall block at L141 concatenates three recalls — visually dense

L141: `*Recall §2.1: the Sudoku grid is the canonical CSP — variable = cell, domain = {1..9}, constraint = no duplicate in row/column/box. Recall §2.2: variables = guests, domains = tables, constraints = "do not seat together". Recall §2.8: a Tetris board mid-game is the picture of a *consistent partial* assignment.*`

Three recalls concatenated into one italic sentence. This is the densest recall block in the chapter and pedagogically the most important (it ties the CSP definition to three analogies at once). A bulleted list would read more easily:

```
- *Recall §2.1: Sudoku grid — variable = cell, domain = {1..9}, constraint = no duplicate in row/column/box.*
- *Recall §2.2: wedding seating — variables = guests, domains = tables, constraints = "do not seat together".*
- *Recall §2.8: Tetris board mid-game — the canonical picture of a consistent partial assignment.*
```

**Suggested fix:** apply the bulleted format above at L141. Cosmetic, but the block is the densest cross-link cluster in the chapter and worth the visual breathing room.

---

## EVIDENCE

Direct quotations from the revised chapter and how they discharge the Round 1 findings.

**E1. Front-matter glossary line is unchanged** (L4): same set of 14 glossary terms. The Round 1 audit-list is therefore stable.

**E2. §2 now contains ten subsections** (L57–119): §2.1 Sudoku, §2.2 seating chart, §2.3 most-cornered square, §2.4 leaving doors open, §2.5 attacked squares (now "candidate list" — not "clipboard"), §2.6 customs queue, §2.7 outfit-trying, §2.8 Tetris board, §2.9 maiden aunt, §2.10 Newton's cradle. Every glossary term has a §2.x home. (P0-1 closed.)

**E3. New §2 preamble mapping table** (L42–55) explicitly maps each §2.x to its §3/§4 home. This is a clean addition that goes beyond the Round 1 P2-1 suggestion. (P2-1 closed, with minor undercount noted in this round's P2-5.)

**E4. Cross-link audit — `grep §2` over the revised chapter:**

- L141 (in §3.1): three recalls — `§2.1`, `§2.2`, `§2.8`. ✓ (P0-2 partially, P0-1 confirmation.)
- L193 (in §3.3): `Recall the "seating chart" analogy in §2.2`. ✓
- L301 (in §3.4.4): `Recall §2.1: the pencil-marks-and-erase loop…`. ✓ (P0-2 closed for this target.)
- L364 (in §4.1, immediately under the pseudocode): `Recall §2.7: backtracking is shirt → trousers → shoes… Recall §2.1: it is also the Sudoku-pencil-marks loop…`. ✓ (P0-2 and P0-3 both closed at the canonical §4.1 home.)
- L399 (in §4.2): `Recall §2.7: the wedding-outfit analogy.` ✓
- L419 (in §4.4): `Intuition (§2.3): pick the most-cornered square.` ✓
- L429 (in §4.4): `Recall §2.9: degree heuristic = seating the maiden aunt first.` ✓
- L439 (in §4.5): `Intuition (§2.4): leave doors open.` ✓
- L473 (in §4.6): `Recall §2.5: place a queen, cross out attacked squares… Recall §2.10: forward checking is the first hop of the Newton's-cradle cascade…`. ✓ (multi-recall.)
- L595 (in §4.8): `Recall §2.6: arc consistency = customs queue… Recall §2.10: arc consistency is the *full* Newton's-cradle cascade…`. ✓

Every §2.x has at least one recall from §3 or §4, and the three most exam-relevant analogies (§2.1, §2.7, §2.10) have multiple recalls. (P0-2, P0-3, P1-5 all closed.)

**E5. "Maiden aunt" has been extracted from §2.2.** §2.2 body now reads (L65):

> Each guest is a variable; each "these two people cannot sit at the same table" is an edge. To assign tables you walk the graph and see who conflicts with whom. Isolated guests (no edges) can be placed anywhere, and any "must sit at table 3" edict is a unary constraint that simply shrinks one guest's choices in advance.

— no maiden-aunt sentence. The maiden-aunt content lives in §2.9 (L108–112) with its own breakdown caveat. (P1-1 closed.)

**E6. "Clipboard" typo gone.** §2.5 now (L81–83) frames forward checking as "**crossing off attacked squares on a candidate list**" and says "If the candidate list of any future row becomes empty…". The chessboard/clipboard mismatch is resolved by reframing the whole analogy onto the candidate-list image, which also addresses Reviewer #4's P0-A on the same line. (P1-2 closed.)

**E7. All seven prior §2 caveats are now `> **Where it breaks down.** …` blockquotes.** Spot-check at L61 (§2.1), L67 (§2.2), L73 (§2.3), L79 (§2.4), L85 (§2.5), L92 (§2.6), L100 (§2.7), L106 (§2.8), L112 (§2.9), L118 (§2.10). Visual weight is now consistent with the chapter's exam-prep claim. (P1-6 closed.)

**E8. §8 cheat-sheet "Seat the maiden aunt first" entry now cites §2.9.** L828: `**Degree heuristic.** Tie-breaker for MRV: among ties, pick the variable in the **most constraints on yet-unassigned neighbours**. [Slide 27, §2.9.] *Seat the maiden aunt first.*` The cheat-sheet's diagnostic that §2 was missing a subsection is now reconciled. (P1-7 closed.)

**E9. §2.3 MRV caveat now correctly characterises the degree heuristic.** L73: "*Where it breaks down.* MRV is silent at the very start of the search when every variable has its full domain — at that point all variables tie. The **degree heuristic** (§2.9, §4.4) breaks this tie by picking the variable with the most unassigned neighbours, but it is *only* a tie-breaker — not a correction to MRV's selection logic." This matches §4.4 body (L423: "explicitly frames it as a 'Tie-breaker among most constrained variables'"). (P1-4 closed.)

**E10. §2.6 customs-queue caveat expanded to cover directionality.** L92: explicit "values are the passport-pages, not the passport itself" and "the cascade does not *modify* $Z$'s claims by edict of $X$ — $Z$ only loses pages via its own consistency re-check against $X$'s now-reduced domain. This subtle directionality is exactly what §6 pitfall #7 warns about". The Round 1 P1-3 directionality concern is addressed. (P1-3 closed, with a P2-1 rendering nit raised this round.)

**E11. Stale section pointers in §2.1 and §2.5 corrected.** L61: "we cover it in §4.6 (forward checking) and §4.8 (arc consistency)" — matches the actual chapter structure. L86: "**Arc consistency** (§4.8) closes this gap" — corrected from §4.6 to §4.8. (P2-3 and P2-7 closed.)

**E12. §2.3 (MRV) now contains the quantitative contrast suggested in Round 1.** L71: "Compare that to a cell whose row/column/box still admit `{1,2,4,5,6,8,9}` (seven candidates): assigning the {3,7} cell first gives a binary branch with ~50% failure rate on the first wrong guess, while assigning the 7-candidate cell averages out across seven branches and may hide its failure deep below." (P2-4 closed.)

**E13. §2.7 (outfit-trying) DFS-vs-BFS clarification added.** L98: "Notice that the *shirt* stays on while you cycle through trousers — backtracking holds onto the prefix of decisions, only undoing the most recent one when it fails. That last-in-first-out undo is what makes this DFS, not BFS." (P2-5 closed.)

**E14. §2.4 (LCV) caveat tightened.** L79: "For over-constrained CSPs with no solution, LCV's per-value support counting is paid on every node and yields nothing, since *every* branch is doomed and reordering them only changes which doomed branch is explored first." (P2-2 closed.)

---

## PM REPORT

```
## Report to PM

**Assignment recap:** L07 (Constraint Satisfaction Problems) Round 2 — Reviewer 3 (Pedagogical Clarity incl. Analogies). Re-verify the three Round 1 P0 findings (missing §2 analogies for Consistent assignment, Degree heuristic, Constraint propagation) and seven P1 findings (maiden-aunt misplacement, clipboard typo, customs-queue directionality, MRV caveat self-contradiction, §3.4.4 missing recall, caveat-format visibility, §8 cheat-sheet mismatch).

**Status:** Pass with minor concerns. All three Round 1 P0s and all seven Round 1 P1s are closed. Eight P2 polish items are raised this round (all rendering / cosmetic / consistency tweaks) — none of them block shipping, but the customs-queue and forward-checking caveats now have two stacked blockquotes each that may render flatter than intended, and §2.10 (Newton's cradle) has a forward-looking caveat that lands better on second read than first.

**P0 findings:** none.

**P1 findings:** none.

**P2 findings:**
1. §2.6 customs-queue caveat is now two stacked blockquotes (`> **analogy-level**` then `>` then `> **theory-level**`); markdown will collapse them visually. Split or fold-with-bold-sub-cues.
2. §2.10 (Newton's cradle) "asymmetric and lossy" caveat is abstract — reader hasn't seen §4.8 yet. Anchor with one concrete reference back to §2.6's directional asymmetry.
3. §2 preamble mapping table at L46/L52 undercounts cross-links: §2.1 is also recalled from §4.1, §2.7 is also recalled from §4.2. Expand entries.
4. §2.5 (forward checking) caveat now has two paragraphs in one blockquote and the second (look-ahead horizon — the key bridge to arc consistency) is not bold-led. Promote with a second `> **Where it also breaks down.**` cue.
5. §2 mapping-table entries §2.3 → §4.4 and §2.9 → §4.4 both land on §4.4 top; a reader following §2.9's link arrives at MRV not at the degree-heuristic paragraph. Cosmetic only.
6. §6 pitfall #1 (consistent-vs-complete table at L741) doesn't recall §2.8 (Tetris) even though §2.8 was added specifically to analogise this distinction. Add an italic recall under the table.
7. §2.9 (maiden aunt) caveat says "feuds with guests who already have their tables decided" — those feuds are already excluded by the degree definition; the real failure mode is *tightness vs. count*. Rephrase.
8. §3.1 italic recall block at L141 concatenates three recalls into one dense italic sentence. Bullet-list format would read better.

**QA Checklist (§7) status:** N/A — this review covers Spec §7.1 (pedagogical clarity / analogies), not the chapter-internal §7.

**Acceptance criteria (§1) status:** N/A — Reviewer 3 evaluates §2-analogy compliance, not the chapter's own §1 acceptance criteria.

**DOCUMENT.md audit:** N/A — this review changes no project files.

**Out-of-scope observations (worth noting):**
- §4.7 "Note on the slide-35 picture" (L479) is well-written and addresses what was a Round 1 P0 for Reviewer #4 (separate scope, but worth flagging that the K4 clarification reads cleanly).
- §5.6 worklist trace (L716–733) is now a strong concrete exhibit of arc-consistency cascade behaviour, with both a "failure on first pop" table and a hypothetical-cascade table for pedagogical contrast. Good addition.
- §3.4.2 alternative formulation now explicitly notes "Lab 4 uses this formulation for a genetic algorithm, not for CSP backtracking; Lab 6 — see §7 — is the CSP lab" (L254), resolving what would have been a Reviewer #4 P1.
- One small nit not raised as P2: the chapter still contains a "�" mojibake in the slide-18 verbatim quotes at L327 and L332. Probably a UTF-8 encoding artifact when the slide bullet character was pasted. Worth a single character fix on next pass.

**Concerns / risks:**
- The two-stacked-blockquote rendering issue (P2-1 and P2-4) is the only finding that could materially affect comprehension at scale. If the chapter is rendered to PDF or shipped via a markdown engine that hard-collapses adjacent blockquotes, the two parts will look like one continuous block and the second cue (the more important pedagogical claim in each case) will be visually de-emphasised. Easy fix; flag for whichever rendering target the study package finally ships against.
- Round 2 brief mentioned that Reviewer 1's file is still not present in `study/_review/L07/round1/`. I treated the absence as Round 1 metadata, not as a Round 2 deliverable to chase down.
- The §2 → §3/§4 cross-link discipline is now solid in §2 → §3/§4 direction, but the reverse (§3/§4 → §2) is uneven: §4.4 and §4.6 have multiple recalls, §4.3 and §4.5 have only one each; §3.4.1, §3.4.2, §3.4.3, §3.4.5 have zero. This is acceptable because the Round 1 spec only required §2 → §3 cross-links (analogy must be findable from the formal side), but if a future pass tightens the spec to "every §3/§4 section recalls its analogies", several §3.4.* and §4.3 will need touch-ups.

**What PM should do next:** treat this as PASS. The chapter is ready to be unblocked from the Reviewer #3 axis. The eight P2 findings can be (a) deferred to a final polish pass, (b) handed to the chapter author for a quick batched edit (each fix is one to three lines), or (c) ignored — none of them affect correctness or exam value. Do not re-dispatch Reviewer #3 for these unless polish becomes a separate workflow stage.

**DOCUMENT.md updated:** N/A for QA / Reviewer.
```
