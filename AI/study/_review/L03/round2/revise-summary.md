# L03 Round 2 → Round 3 — Revise Summary

**Artifact revised:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L03-Uninformed-Search.md`
**Reports consumed:** `study/_review/L03/round2/reviewer{1,2,3,4}.md`
**Date:** 2026-05-22

This pass closes one P0 and seven P1 items raised across the four Round 2 reviewers. All edits are localised; no architectural restructuring.

---

## Summary table of edits

| # | Section | Issue source | Defect | Fix |
|---|---------|-------------|--------|-----|
| 1 | Line 4 (chapter header) | R3 P1-1 | Glossary-terms list still advertised `transition model (search)` despite §3.2 removing the term. | Deleted `transition model (search), ` from the glossary-terms-introduced list. |
| 2 | §3.8 (A\* forward reference) | R3 P1-2 | Still named "admissibility, consistency" despite Round 1 P1-3 asking to defer those terms to the glossary. | Reworded "the conditions on $h$ that make those guarantees hold (admissibility, consistency)" → "the conditions on $h$ that make those guarantees hold". The terms now live only in the glossary's A\* entry. |
| 3 | §7 forward-references list | R3 P1-2 | Same — "admissibility and consistency" named in the L05 heuristic-function bullet. | Reworded to "properties of $h$ that condition A\*'s optimality (covered in L05)". |
| 4 | §4.2.1 goal-test-on-pop counter-example | R3 P1-3 | Counter-example assumed an unstated successor order ($G_1$ before $A$). | Added explicit "**Assumption.** The successor function returns $S$'s children in declaration order: $G_1$ first, then $A$." Locked the PUSH-test trace down. |
| 5 | §5.1.1 vacuum-world BFS trace | R3 P0-1, R4 P1-1, R4 P1-2 | (a) Step 1 had stream-of-consciousness narration "self-loop already in frontier? actually new, in explored after pop". (b) Step 4 incorrectly generated $(B,0,0)$ from $(B,1,0)$ under $S$ — physically impossible (S in cell B cannot clean A). | Full rewrite of the trace. Added a "Successor reminder" paragraph above the table making the S-cleans-only-current-cell rule explicit. Step 1 narration is now a clean declarative sentence: "$L$→`(A,1,1)` (self-loop, already in explored, skip). $R$→`(B,1,1)`. $S$→`(A,0,1)`." Step 4 now correctly produces only $(A,1,0)$ as a new state ($S$ on $(B,1,0)$ leaves it unchanged). Step 5 (expanding $(B,0,1)$) is now where the goal candidate $(B,0,0)$ first appears. Step 7 walks the corrected parent chain $(B,0,0) \leftarrow S\ (B,0,1) \leftarrow R\ (A,0,1) \leftarrow S\ (A,1,1)$, confirming the claimed return path $S, R, S$. |
| 6 | §5.2.1 generic tree-search strategy-pick block | R4 P1-5 | Strategy-pick framing (BFS=Timisoara, UCS=Zerind, DFS=Rimnicu Vilcea after Sibiu's expansion) risked misleading the student into thinking UCS actually expanded Sibiu before Zerind. | Added an **Important framing** paragraph stating this is a *hypothetical* "if the tree had grown to this shape, what would each strategy pick next?" exercise and that UCS would in fact pop Zerind ($g=75$) before Sibiu ($g=140$). Cross-referenced §5.2.2 for the real trace. Reworded the UCS bullet to "if we *were* at this point". |
| 7 | §5.3 edge-list note ($E \to G$) | R2 P1-NEW, R4 P1-3 | §5.3 followed slide-37 trace (skipping $E \to G$ at step 5) while §5.7 used the edge to compute $A \to D \to E \to G = 9$. Internally inconsistent. | Replaced the old "Note on slide image" with **Canonical interpretation of $E \to G$**: $E \to G = 4$ IS a graph edge; §5.3 reproduces the slide-37 trace verbatim (skipping the edge at step 5 to match the slide for exam-reproduction); §5.7 uses the full edge list including $E \to G$. Exam advice: follow slide-37 for trace questions, use full edge list for BFS-vs-UCS questions. |
| 8 | §5.3 step-7 pedagogical note | R3 P1-4 | The "what to write on the exam" three-line ladder was buried at the end of a long paragraph. | Reordered: the three-line exam ladder now leads (reproduce-slide → `G:14`; explain-UCS → `G:8` retained; optimal-path → cost 8). The slide-vs-algorithm reconciliation prose follows as the second blockquote under the heading "Why the slide and the algorithm disagree at Step 7." |
| 9 | §5.7 BFS-vs-UCS contrast | R2 P1-NEW-3, R4 P1-3, R4 P1-4 | (a) Used "if we allowed it" hedge on $E \to G$, contradicting §5.3. (b) Justified BFS cost-14 result with vague "FIFO tie-breaking" framing rather than the graph-search frontier-dedup rule. (c) Tie-break convention not explicitly anchored. | Full rewrite. Opens with a **Graph used** paragraph committing to the full edge list (including $E \to G = 4$, the canonical interpretation from §5.3). BFS analysis is now a step-by-step bullet list showing exactly how $G$ enters the frontier first via $C$ (parent of the cost-14 path), and how subsequent attempts to push $G$ via $E$ and via $F$ are **blocked** by the graph-search "$s' \notin$ frontier" check. Concluding sentence makes the lesson explicit: "it is not 'FIFO tie-breaking' between three depth-3 goals — only the *first* push of $G$ survives, and the edge-list child ordering decides which path that is." |
| 10 | §6 pitfall #5 (DFS in cycles) | R4 P1-6 | Claim "DFS will oscillate $A, B, C, A, B, C, \ldots$ forever" contradicts the chapter's §3.4 algorithm template, which includes an explored set. | Rewrote pitfall #5 as a three-bullet hierarchy: (a) pure DFS with no repeated-state check at all → infinite loop on cycles; (b) DFS with the slide-47 current-path check → terminates with **failure** in disconnected components (incompleteness, not non-termination); (c) DFS with the chapter's graph-search explored set → also reports failure by incompleteness. Stated explicitly: "the canonical exam-relevant DFS failure mode for cyclic state spaces with the chapter's algorithm template is *incompleteness in disconnected components*, not infinite looping". |
| 11 | §8 cheat-sheet pitfall line | R4 P1-6 | Cheat-sheet still asserted "DFS without repeated-state check loops forever in cyclic graphs" without distinguishing the two variants. | Rewrote the cheat-sheet line to mirror the new pitfall #5 split: DFS with graph-search explored set is incomplete in cyclic-plus-disconnected state spaces; DFS with no repeated-state check at all loops forever. |

---

## Not addressed in this round (deliberately deferred)

These were P2-tier or otherwise out of the round's brief:

- R1 P2-1: `§5.3 step-7 G:14` cell could be made self-explanatory inside the cell. The accompanying pedagogical note already covers it, and we just reordered the note to put the exam ladder up front (edit #8). Defer to polish round.
- R1 P2-3: §3.3.1 parity sentence could use the words "permutation parity" / "even permutations" explicitly. Optional sharpening only.
- R2 P1-NEW-2: §4.1 BFS pseudocode could acknowledge the goal-test-on-pop deviation from standard R&N. Internally consistent and mathematically sound; one-line note can wait.
- R3 P2-1 through P2-8 (column-header rename, IDS analogy strength, counterfactual graph naming, Romania trace footnote, cheat-sheet bullet parallelism, glossary-list note, etc.) — pure polish.
- R4 P1-7 (slide-49–52 IDS $b=2$ counting), R4 P1-8 (end-of-chapter self-test), R4 P2-1 through P2-10 — deferred to a final polish round per R4's own recommendation.

---

## Files modified

- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L03-Uninformed-Search.md` — 11 localized edits per the table above. No section deletions, no architectural changes.

## Files created

- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_review\L03\round2\revise-summary.md` — this file.

---

## Verification spot-checks

- `transition model` no longer appears in the glossary-terms header (line 4 retains all other terms in their order).
- `admissibility`, `consistency` no longer appear anywhere in the L03 chapter (verified by re-read; both terms removed from §3.8 and §7).
- §5.1.1 BFS trace: step 4 now produces only $(A,1,0)$ as a new state from $(B,1,0)$. Step 5 (expanding $(B,0,1)$) is where $(B,0,0)$ first appears as a goal candidate. Step 7 walks the corrected parent chain and confirms the **$S, R, S$** sequence.
- §5.1.1 step 1 narration: no question marks, no "actually new", no mid-cell hesitation — single declarative voice.
- §5.3 canonical interpretation paragraph now anchors both §5.3 and §5.7 to a single coherent rule for the $E \to G$ edge.
- §5.7 BFS analysis: bullet-by-bullet expansion order; graph-search dedup is the named mechanism for the cost-14 result; no "if we allowed it" hedge anywhere.
- §5.3 step-7 pedagogical note: exam ladder leads, slide-vs-algorithm reconciliation follows.
- §5.2.1 strategy-pick now framed as hypothetical with explicit cross-reference to §5.2.2 for the real trace.
- §6 pitfall #5: three-variant breakdown (no-check, current-path-check, explored-set), with the canonical exam-relevant DFS failure mode named as incompleteness in disconnected components.
- §8 cheat-sheet pitfall line aligned with the new pitfall #5.

All 11 edits are localised to existing sections; no new sections were added.
