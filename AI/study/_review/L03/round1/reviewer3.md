# L03 — Uninformed Search — Round 1 — Reviewer #3 (Pedagogical Clarity incl. Analogies)

**Source:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture3-Uninformed Search.pdf` (56 slides)
**Draft under review:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L03-Uninformed-Search.md`
**Lens:** Pedagogical clarity. Read as a confused student. Every major concept must have a concrete everyday analogy in §2 with a "where it breaks down" caveat, cross-linked from §3.
**Disposition:** Harsh. False positives are cheap.

---

## VERDICT: **NEEDS_REVISION**

The chapter is broadly strong on analogies (§2 is unusually good for an AI course chapter — six analogies, each with a caveat). But three classes of pedagogical defect prevent approval: (1) the UCS worked example in §5.3 contains a corrupt step-7 trace, a malformed ASCII graph, and an unanchored edge-list aside that together make the most exam-relevant figure in the lecture *less* clear, not more; (2) the DFS trace in §5.5 contains a literal in-line "wait." correction visible to the student, which is the textual equivalent of crossing out work on a whiteboard mid-explanation; (3) a handful of concepts (transition model, $g(n)$, "graph search" vs "tree search", "depth-limited DFS", admissibility/consistency) are introduced or used without enough scaffolding for a first-time reader. None of these are mathematical errors — they are explanation failures.

The forward reference to A\* is handled cleanly and honestly, which is to the chapter's credit.

---

## P0 — MUST FIX (blocks approval)

### P0-1. The UCS worked example (§5.3) is partially corrupt and self-contradicting.

**Where:** `study/lectures/L03-Uninformed-Search.md` §5.3, the step-by-step trace table and the surrounding ASCII graph + edge-list parenthetical.

**What's broken:**

1. **The ASCII graph (lines ~403–415) is unreadable as a graph.** Edges go in directions that don't line up with the slide. The double-direction arrow on `B`, the broken "E-G also cost 4 not shown directly above" parenthetical, and the dangling `(D → F cost 2, F → G cost 3)` clarification inside the code block all signal the author was unable to draw the slide-37 graph in ASCII and gave up half-way. The reader is then handed a *second* canonical edge-list immediately after that contradicts the picture (e.g. the ASCII graph implies `B → C` edge cost 1 with a back-arrow, but the text says `B → C = 1` with `E → B = 4`).

2. **Step 3 of the trace contradicts itself in writing.** The chapter says:
   > *"pop D (g=3), expand to B (g=3+2=5 via D-E? no — D→E is 2, so g would be 5; D→F is 2, so F has g=5; D's adjacencies on the slide give B (5), E (5), F (5))"*
   This is an author thinking out loud, not an explanation. A student reading this is now in the middle of someone else's confused arithmetic. The parenthetical "via D-E? no — D→E is 2, so g would be 5" is gibberish to anyone who hasn't already solved the example. Step 3's "expand to B" is also wrong wording: D is being expanded, so we're discovering new fringe members; B already exists at cost 5 and is *replaced* (or kept) — the chapter should state which.

3. **Step 7 disagrees with slide 37.** Slide 37's Step 7 explicitly lists the fringe as `Node G, Cost 14` (i.e. the slide shows G at cost 14 in the fringe at this step). The chapter's table shows step-7 fringe as `{G:8}` with the annotation "we already have G at cost 8, so do *not* replace". This is algorithmically what *should* happen with the "replace only if cheaper" rule from slide 21 — but the slide diagram shows the *other* convention (replacing or simply re-adding G:14 anyway). The chapter must either (a) reproduce the slide's trace literally and *then* call out the discrepancy as a slide-vs-correct-algorithm trap, or (b) explicitly state "we depart from the slide's display here because the slide-21 algorithm template demands the cheaper-replace rule". Right now the chapter silently disagrees with its own primary reference figure (Figure 8), which is the most exam-relevant figure of the whole lecture by the chapter's own admission.

**Why this matters pedagogically:** §5.3 is explicitly highlighted as the most exam-relevant example. A student trying to learn UCS by reading this section will (a) be unable to reconstruct the graph, (b) be confused by the author's in-line debugging in step 3, and (c) get a different answer than the slide's trace and not know which is right.

**Suggested fix:**
- Replace the ASCII graph with either a Mermaid `graph LR` diagram or a clean edge-list table (Source → Target | Cost) before the trace begins. No prose parentheticals inside the code block.
- Rewrite step 3 as a clean statement: *"Pop D. Its successors are B (path 3+2=5), E (3+2=5), F (3+2=5). Since B already exists in the fringe at cost 5 — equal, not lower — we do not replace. Push E and F."*
- Either reconcile the step-7 cost mismatch with slide 37 by reproducing the slide's `G:14` and explaining why the algorithm template says we should not replace, *or* explicitly flag that the chapter follows slide 21's rule and the slide-37 visual shows the pre-deduplication state. Whichever choice — make it explicit, not silent.

### P0-2. The DFS trace in §5.5 contains visible in-line author confusion ("wait. *Standard convention:* ...").

**Where:** §5.5, lines ~462–469 of the table, specifically Step 2:

> *"pop C (top), push F, G | `[B, F, G]` — wait. *Standard convention:* push children in *reverse* order so left child is on top. We follow the slide's left-first traversal, so we push children right-first: C then B → frontier becomes `[C, B]` with B on top."*

**What's broken:** This is a "thinking aloud" mid-table that no student should ever see. The reader of a textbook chapter should not have to watch the author realise mid-explanation that the convention is different from what they were about to write. Worse: the row labelled "Step 2" then *isn't* Step 2 at all — the actual left-first trace begins in a *second* table immediately below ("Left-first trace assuming G is the goal"). The first table never recovers; it just trails off.

**Why this matters pedagogically:** A student reading two tables for the same trace, with the first one annotated "wait, I got it backwards", does not learn DFS — they learn that the chapter is unreliable. This is exactly the "hand-waving / unjustified leaps" lens of Reviewer #3.

**Suggested fix:** Delete the first table entirely. Keep only the "Left-first trace assuming G is the goal" table. Add a single sentence above it: *"Convention: push children in right-to-left order so the leftmost child ends up on top of the stack and gets popped next; this matches the slide's left-first traversal."* That is all the student needs.

### P0-3. "Graph search" vs "tree search" is named as a distinction, then never explained.

**Where:** §3.4, immediately after the algorithm box (lines ~167–168):

> *"**The 'tree' name is slightly misleading** when the state space has loops. As written above with the explored set and the 'replace if cheaper' check on the frontier, we are doing graph search, not pure tree search. The deck blurs the two; in this chapter we use 'search tree' to mean ..."*

**What's broken:** The chapter raises a distinction (tree search vs graph search) that *Russell & Norvig and every AI exam* treat as a load-bearing concept. It then resolves the ambiguity by redefining "search tree" for this chapter's local use — but never *teaches* the underlying distinction. A student who has heard "graph search" elsewhere is left with no clear picture of what changes between the two and why the changes matter (e.g. that pure tree search can re-expand the same state via different paths, blowing up the time complexity).

**Why this matters pedagogically:** This is one of the most common exam pitfalls in the entire search topic. The lecturer's slide deck does blur it (as the chapter correctly notes), which means the chapter is the *only* place a student will get clarity — and the chapter is opting out.

**Suggested fix:** Add a 4–6-line callout box defining (a) tree search (no explored set, no fringe-dedup), (b) graph search (with explored set, with fringe-dedup), (c) which one the §3.4 pseudocode actually implements, and (d) why the difference matters in finite cyclic state spaces. This is half a paragraph; it does not bloat the chapter.

---

## P1 — SHOULD FIX (requested, not blocking)

### P1-1. "Depth-limited DFS" is used in §4.4 without ever being defined as a named concept.

**Where:** §4.4 algorithm box and prose. The chapter writes `DEPTH-LIMITED-DFS(problem, ℓ)` as if the reader already knows what it is, then describes it in one sentence after the code: *"`DEPTH-LIMITED-DFS` is plain DFS modified to refuse to expand a node at depth ≥ ℓ; it returns `cutoff`/`failure`/solution path."*

**What's broken:** "Depth-Limited" appears in the comparison table on slide 54 *and* in the chapter's own Figure 5 table. It deserves to be a named sub-concept (3.x or a numbered paragraph inside §4.4), not a forward reference that is satisfied one line later. The current treatment also leaves the `cutoff` vs `failure` distinction implicit, which is exam-fodder: students confuse "we hit the depth limit without finding a goal at this depth" (cutoff → try deeper) with "we explored everything and there is genuinely no solution" (failure → stop).

**Suggested fix:** Promote DL-DFS to a numbered sub-section §4.4.1 (or a paragraph titled "Depth-limited DFS, the subroutine"). Define the three return values explicitly. Mention that slide 54 lists DL-DFS as a strategy in its own right with the same $O(b^\ell)$ time profile as raw DFS but with the cutoff.

### P1-2. The "Romania route planning" trace in §5.2 fails to commit to a search strategy.

**Where:** §5.2, especially the step-2 paragraph:

> *"What happens next depends on the strategy: BFS picks `Timisoara` next (next in FIFO order after `Sibiu`'s siblings), UCS picks the city with the lowest g-value (probably `Zerind` at 75 if Arad→Sibiu were 140), DFS picks the most recently added (`Rimnicu Vilcea`)."*

**What's broken:** Two things. First, "probably Zerind at 75" with "if Arad→Sibiu were 140" is conditional-mood storytelling that doesn't belong in a worked example — Arad→Sibiu *is* 140 (it's on the map in Figure 6). Either compute the real UCS next-pick (Zerind: g=75 < Timisoara: g=118 < Sibiu: g=140 — so UCS pops Zerind), or remove the UCS speculation entirely. Second, the "BFS picks Timisoara next" claim is questionable: after expanding Arad → {Sibiu, Timisoara, Zerind} and then expanding Sibiu (which adds Arad, Fagaras, Oradea, Rimnicu Vilcea), a FIFO pops *Timisoara* (the second of Arad's original children), so this is technically right — but the chapter doesn't explain *why* Timisoara comes next, only asserts it.

**Why this matters pedagogically:** A student looking at §5.2 to understand the difference between BFS, DFS, and UCS gets a single sentence of "BFS picks X, UCS picks Y, DFS picks Z" with no anchoring back to *which slot in the FIFO/LIFO/PQ they're picking from*. This is the moment where the chapter could have nailed "search strategy = order on the frontier", and it doesn't.

**Suggested fix:** Rewrite the paragraph as three short trace continuations:
- *BFS: FIFO order is `[Timisoara, Zerind, Arad', Fagaras, Oradea, Rimnicu Vilcea]`. Next pop = Timisoara.*
- *UCS: PQ ordered by g. Frontier after Sibiu's expansion: Zerind:75, Timisoara:118, Sibiu's children (Arad:280, Fagaras:239, Oradea:291, Rimnicu Vilcea:220). Next pop = Zerind (g=75).*
- *DFS: LIFO. Last-pushed = Rimnicu Vilcea (assuming Sibiu's children were pushed in given order). Next pop = Rimnicu Vilcea.*

Each line takes one sentence and *anchors the strategy to the data structure*, which is the whole pedagogical point.

### P1-3. The §3.8 forward reference to admissibility/consistency overshoots.

**Where:** §3.8 "A\* and admissibility (forward reference)".

**What's broken:** §3.8 introduces both *admissibility* ($h$ never overestimates) and *consistency* (triangle inequality on $h$), then says these condition A\*'s optimality. A confused student now believes these terms came from L03. They did not. The chapter's own honest-note in §1 says A\* is "mentioned by name only — it has no slides of its own in L03", so dropping new terminology in §3.8 directly violates the chapter's own stated scope. Worse, §6 pitfall #10 (line ~543) reminds the student: *"Claiming the lecture covers A\*. It does not."* — and then §3.8 quietly *does* cover A\*-adjacent material.

**Why this matters pedagogically:** Either A\*'s prerequisites belong in this chapter or they don't. The chapter has, for the most part, made the right choice (defer to L05+). §3.8 leaks the deferred material back in.

**Suggested fix:** Trim §3.8 to its first sentence ("the symbol $f(n) = g(n) + h(n)$ should be in your head as a forward reference; A\* is derived in a later lecture"). Move "admissibility" and "consistency" to the glossary's A\* entry, with a "FWD-REF: L05" tag (the glossary already uses this tag pattern). Remove them from L03's running text.

### P1-4. The "transition model" term appears once, in passing, and is never used again.

**Where:** §3.2 line 112: *"The implicit *transition model* $\mathrm{Result}(s, a)$ tells us 'what state do we end up in if we apply action $a$ in state $s$'."*

**What's broken:** "Transition model" is a Russell & Norvig term that *isn't* on the slides (the slides use only "successor function" / "operator"). The chapter introduces it as a parenthetical, then never uses `Result(s, a)` notation again. A student reading the chapter will wonder why they were taught this term. Either it earns its keep (used in pseudocode, used in worked examples) or it's noise.

**Suggested fix:** Either (a) delete the parenthetical entirely — the slides don't need it — or (b) use `Result(s, a)` in the §3.4 pseudocode where I currently see `(a, s') in SUCC(n.state)`, *and* in the worked examples. Right now it's the worst of both worlds: introduced, not used.

### P1-5. The maze "where it breaks down" caveat in §2.1 is correct but understated.

**Where:** §2.1, the "Where it breaks down" paragraph.

**What's broken:** *"In a real maze you can backtrack physically — you walk back. In a *search algorithm* you don't move at all; you only keep a list of 'states I could be in' (the frontier)."* This is *the* most important conceptual subtlety in the whole lecture — the agent doesn't move during search — and the chapter buries it in one sentence as a footnote to the maze analogy. The slide-9 quote about "close his/her eyes" later picks this up but the linkage isn't made explicit. A first-time reader needs both bits in one place: *the agent doesn't move during search (no percepts being processed), and it doesn't move during execution either (no percepts being used, eyes closed). That's why it works only in observable+deterministic+known environments.*

**Suggested fix:** In §2.1 "where it breaks down", add a second sentence connecting the maze-walker to slide 9: *"This is also why the agent can close its eyes during execution (slide 9) — the plan is fixed in advance because the environment is deterministic and known."* Then cross-reference §2.1 from §3.1's recall-block (already present) so the loop is closed.

### P1-6. The cheat sheet (§8) drops the analogy reminders on three of four rows.

**Where:** §8's strategy table.

**What's broken:** The chapter's own §8 introduction says: *"Each major concept carries a one-line analogy reminder (italicised) so you can re-anchor without flipping back."* The four-row strategy table delivers on this — every row has an italicised analogy. Good. But the rows above the table ("Setup", "Search-tree mechanics") drop the analogies for everything else — *frontier*, *explored set*, *branching factor*, *problem-solving agent*. The cheat-sheet's promise to the reader is "you can re-anchor on every concept without flipping back". It isn't quite kept.

**Suggested fix:** Add one-line analogies in the cheat-sheet for:
- *Frontier / fringe: "to-do list" / "people I plan to call".*
- *Explored set: "already-done list".*
- *Branching factor b: "how many corridors leave each junction".*
- *Problem-solving agent: "closes its eyes once the plan is fixed".*

Each is 6–10 words; total cost to the chapter is 4 inline italic phrases.

### P1-7. §4.2 algorithm box uses goal-test-on-pop without saying "this is a UCS-specific subtlety" *in the algorithm box*.

**Where:** §4.2, UCS pseudocode and surrounding prose.

**What's broken:** The chapter has a great paragraph above the algorithm explaining *why* goal-test-on-pop matters for UCS — but the pseudocode itself doesn't visually distinguish this from the BFS box. A skim-reader who compares the BFS box (§4.1) and the UCS box (§4.2) side by side sees nearly identical code and misses the point. Pitfall #2 in §6 ("UCS goal-tests on expansion, not on generation") repeats the warning, which means the chapter knows this is exam-fodder — but the algorithm box is the place to surface it.

**Suggested fix:** Add an inline comment in the UCS pseudocode at the `if goal-test(n.state)` line: `# UCS-SPECIFIC: test on POP, not on push — otherwise sub-optimal goals can sneak in`. One comment, one place where the student is already looking.

### P1-8. "Slide 21's 'replace if cheaper' check" is referenced four times, but the actual algorithmic effect is never made vivid.

**Where:** §3.4 pseudocode (line ~163), §4.2 UCS pseudocode (line ~257), §6 pitfall #11 (line ~545), and the cheat-sheet doesn't mention it.

**What's broken:** The "replace if a cheaper path to the same state shows up in the fringe" rule is referenced four times but never illustrated with a 3-line trace. A student doesn't internalise an algorithmic rule from prose; they internalise it from *seeing it fire*. The UCS worked example in §5.3 is the natural place — but the trace there says "we do not replace" (a non-fire) without ever showing a "we *do* replace" case.

**Suggested fix:** In §5.3, after the main trace, add a 4-line "what if D→F cost were 1 instead of 2" mini-trace where F's fresh cost (4) is cheaper than F's existing fringe cost (5), so the replace rule fires and F's fringe entry is updated. Three rows of a table. Concrete demonstration of the rule.

---

## P2 — NICE TO HAVE

### P2-1. The §2 analogies are good but slightly uneven in tone.

Six analogies, six "where it breaks down" caveats. The maze (§2.1), BFS-postman (§2.2), and DFS-leftmost-corridor (§2.3) analogies are excellent — concrete, physical, and the caveats are sharp. The UCS-grocery-cart (§2.4) analogy is fine but the cart-pushing visual is a touch laboured ("Picture several grocery carts being pushed simultaneously through a network of paths with different lengths"). The IDS-restart-each-depth (§2.5) analogy is the weakest — it amounts to "do BFS but in DFS clothing", which doesn't really land as an *everyday* analogy. The frontier/explored-set (§2.6) phone-list analogy is fine.

**Suggestion:** Consider replacing the grocery-cart analogy with the more common "Dijkstra is a flooding wavefront" mental model — UCS *is* essentially Dijkstra with a fringe instead of a relaxation step, and the flooding-water image is more compact and memorable. For IDS, consider the "rehearsal" analogy: each pass is a rehearsal that goes one beat deeper than the last; the wasted shallow-rehearsal time is dwarfed by the final dress rehearsal. Neither is mandatory.

### P2-2. The "Properties of …" headers in §4 could carry the relevant slide reference inline.

§4.1 says "Properties (slide 35):", §4.2 "Properties (slide 36):", §4.3 "Properties (slide 47):", §4.4 "Properties (slide 53):". Good. But the *idea* statements ("Idea. Expand the shallowest unexpanded node first.") don't carry a slide reference, even though they paraphrase slides 30 / 36 / 38 / 48. Adding `[slide 30]` to each Idea line tightens the audit trail.

### P2-3. The cheat-sheet "When to pick which" decision tree could be a flowchart.

§8's bullet list of four "if you're in this situation → pick X" is fine but a 4-leaf decision tree (uniform costs? → BFS or IDS depending on memory budget; non-uniform costs? → UCS; etc.) would be easier to consult under exam time pressure. Not a blocker; cosmetic.

### P2-4. §6 pitfall #7's "graph with one cheap edge of cost 0.01" example is good but never drawn.

The pitfall *describes* a UCS pathological case ("one cheap edge of cost 0.01 and many expensive edges of cost 10") but doesn't draw it. A 4-node 5-edge sketch would make the $C^*/\epsilon$ exponent vivid. Optional.

### P2-5. The §7 cross-reference to L09b HMM ("Viterbi is structured search over a trellis... HMM-flavoured cousin of UCS") is creative but unsupported.

This is a real and useful connection, but a confused L03 student isn't ready for it. Consider moving this cross-reference to L09b's chapter (where the Viterbi material lives) rather than introducing it as a forward link from L03. The L03 cross-reference can stay limited to L05, L06, L07 — all of which directly extend search machinery.

### P2-6. The opening "Honest note on scope" callout in §1 is a strength.

Worth flagging this *positively*: §1's blockquote acknowledging that the slides advertise A\* in the objectives but never derive it, and stating that this chapter therefore restricts itself to uninformed search only, is exactly the kind of honesty a confused student needs. Keep this callout. No change needed.

### P2-7. Figure 7c's caption mentions the duplicate "Arad" — could be louder.

In §5.2 Figure 7c the caption notes "Notice the duplicate 'Arad' — that's why we need the repeated-state check." This is a great teaching moment. Consider promoting it from caption to a one-sentence inline note above the figure: a student who skips captions (many do) will miss this otherwise.

### P2-8. The chapter is currently 633 lines / ~55-minute reading time as stated. That's at the long end.

Not a defect per se. The cheat-sheet in §8 is the main escape hatch for time-pressed students. Worth verifying with the App Tester / examiners that the cheat-sheet alone is sufficient for the slide-54-style "BFS vs DFS vs UCS vs IDS" exam question.

---

## EVIDENCE — what I read

**Slides inspected:** 1 (title), 2–6 (motivation), 7 (objectives), 8–9 (search setting), 10 (search-problem components), 11 (Romania), 12 (state space), 13–14 (vacuum world), 15–17 (8-puzzle and goal-based agents), 18 (Romania route planning), 19 (8-queens), 20 (tree search picture), 21 (tree-search algorithm outline), 22–26 (Romania tree-search trace frames), 27–28 (search-strategy evaluation dimensions and b/d/m), 29 (uninformed strategies list), 30–34 (BFS animation), 35 (BFS properties), 36 (UCS properties), 37 (UCS worked example with 8-step trace), 38–46 (DFS animation), 47 (DFS properties), 48 (IDS intro), 49–52 (IDS animation passes), 53 (IDS properties), 54 (comparison table), 55–56 (next class / closing).

**Chapter sections inspected:**
- §1 Overview & Motivation — checked completeness and honest-scope note. **Pass.**
- §2 Analogies (§2.1–§2.6) — checked existence of analogy + "where it breaks down" caveat for every major concept. **Pass with cosmetic P2-1 nit on grocery-cart and IDS choices.**
- §3 Core Concepts (§3.1–§3.8) — checked definitions, cross-links to §2 analogies, and forward-reference discipline. **Three P1 issues + the §3.8 leakage of admissibility/consistency (P1-3) + transition-model orphan (P1-4) + tree-vs-graph deferred (P0-3).**
- §4 Algorithms — checked algorithm boxes, when-to-use guidance, and side-by-side comparison. **One P1 (UCS pop-vs-push not surfaced in pseudocode comment, P1-7).**
- §5 Worked Examples — line-by-line traced §5.3 (UCS) and §5.5 (DFS) against the slides. **§5.3 has P0-1 (graph + step 3 + step 7), §5.5 has P0-2 (in-line "wait" mid-table), §5.2 has P1-2 (Romania trace conditional speculation).**
- §6 Common Pitfalls — 12 pitfalls; checked each against the slides. **No defects; this is the strongest section.**
- §7 Connections — checked every cross-link target name against the glossary. **One P2 (HMM/Viterbi forward link, P2-5).**
- §8 Cheat-Sheet — checked the analogy-coverage promise made in §8's intro. **One P1 (P1-6: rows above the table drop analogies).**

**Slide cross-references confirmed:** every `[Lecture 3, slide N]` block at section ends matches the slide content. No fabricated slide references.

**Figures embedded vs catalogue:** 15 figures embedded in the chapter (Figures 1–13, with 7a/7b/7c and 11–13 covering animations). Cross-checked against `study/extracted_figures/L03/figures.md` — every USE/REWORK figure in the catalogue is embedded; every SKIP figure has a justification. **No figure pedagogy defect from this lens.** (Reviewer #1 owns figure-coverage scrutiny.)

**External corroboration:**
- Slide 37 (UCS example) — chapter step-7 row contradicts the slide image's Step 7 (`Node G, Cost 14`); see P0-1 item 3.
- Slide 21 (algorithm template) — chapter pseudocode matches the slide's "replace if cheaper" rule.
- Slide 54 (comparison table) — chapter Figure 5 + typeset table match. Footnotes match. **Pass.**
- Slide 53 IDS arithmetic — chapter §5.6's $b=10, d=5 \Rightarrow 123{,}456$ worked example arithmetic verified by hand: $6 + 50 + 400 + 3000 + 20000 + 100000 = 123{,}456$. **Pass.**

---

## Report to PM

**Assignment recap:** Round-1 pedagogical-clarity review of `L03-Uninformed-Search.md`, Reviewer #3 of 4, lens = §7.1 of the spec (pedagogical clarity + analogy enforcement).

**Status:** **Fail (NEEDS_REVISION).** 3 × P0, 8 × P1, 8 × P2.

**P0 findings:**

1. **`study/lectures/L03-Uninformed-Search.md` §5.3 (UCS worked example).** The ASCII graph is unreadable, step 3 contains visible author thinking-aloud, and step 7's fringe `{G:8}` silently contradicts slide 37's `{G:14}`. Fix by replacing the ASCII graph with a Mermaid diagram or clean edge-table, rewriting step 3 as a single declarative sentence, and either reconciling step 7 with slide 37 or explicitly flagging that the chapter follows the slide-21 "replace if cheaper" template and slide 37 displays a pre-deduplication state.
2. **`study/lectures/L03-Uninformed-Search.md` §5.5 (DFS trace).** The first table contains a literal in-line "— wait. *Standard convention:* ..." mid-row, then trails off and is replaced by a second table below. Fix by deleting the first table entirely and replacing with a single clean "Left-first trace" table preceded by one sentence stating the push convention.
3. **`study/lectures/L03-Uninformed-Search.md` §3.4 (tree-search vs graph-search).** The chapter names the distinction, points out the slides blur it, then resolves only locally without teaching the underlying concept. Fix by adding a 4–6-line callout box defining tree search, graph search, which one the §3.4 pseudocode implements, and why the difference is exam-critical in finite cyclic state spaces.

**P1 findings:**

1. `study/lectures/L03-Uninformed-Search.md` §4.4 — depth-limited DFS used in code box without being promoted to a named concept; cutoff vs failure return values left implicit.
2. `study/lectures/L03-Uninformed-Search.md` §5.2 — Romania step-2 paragraph speculates ("probably Zerind at 75 if Arad→Sibiu were 140") instead of stating the actual successor picks for BFS / UCS / DFS.
3. `study/lectures/L03-Uninformed-Search.md` §3.8 — admissibility and consistency are introduced in L03 despite the chapter's own §1 and §6 pitfall #10 saying A\* is *not* covered. Trim §3.8 to one forward-reference sentence and push admissibility/consistency to the glossary's A\* entry.
4. `study/lectures/L03-Uninformed-Search.md` §3.2 — `transition model` and `Result(s, a)` introduced once, never used. Either use them consistently in §3.4 pseudocode and worked examples, or remove.
5. `study/lectures/L03-Uninformed-Search.md` §2.1 — maze "where it breaks down" caveat undersells the "agent doesn't move during search" subtlety. Cross-link to slide-9 "close his/her eyes" in one extra sentence.
6. `study/lectures/L03-Uninformed-Search.md` §8 — cheat-sheet promises italic-analogy reminders on every concept but only delivers on the four-strategy table rows. Add 4 one-line analogies for frontier, explored set, branching factor, problem-solving agent.
7. `study/lectures/L03-Uninformed-Search.md` §4.2 — UCS pseudocode does not visually distinguish goal-test-on-pop from BFS's; add an inline `# UCS-SPECIFIC` comment at the goal-test line.
8. `study/lectures/L03-Uninformed-Search.md` §5.3 — the "replace if cheaper" rule referenced four times but never illustrated firing in a trace. Add a 3-line counterfactual mini-trace where the rule fires.

**P2 findings:**

1. §2 — IDS and UCS analogies are weaker than the maze/postman/leftmost-corridor analogies; consider Dijkstra-as-flood for UCS and rehearsal-passes for IDS.
2. §4 — add slide references on the "Idea." statements at the top of each strategy subsection.
3. §8 — convert "When to pick which" bullets into a small decision flowchart.
4. §6 pitfall #7 — draw the pathological-UCS graph in 4 nodes / 5 edges.
5. §7 — consider relocating the HMM-Viterbi-as-UCS cross-reference to L09b rather than introducing it here.
6. §1 — the honest-scope note is a strength; flagged for preservation.
7. §5.2 Figure 7c — promote the "duplicate Arad" observation from caption to inline.
8. Reading time of 55 min is at the long end; verify the cheat-sheet alone is exam-sufficient via App Tester.

**Acceptance criteria status against §7.1 spec:**

- **"flag hand-waving"** — flagged §3.4 graph-vs-tree, §3.8 forward-overshoot. **Action required.**
- **"flag unjustified leaps"** — flagged §5.3 step-3 thinking-aloud, §5.5 step-2 wait-redo. **Action required.**
- **"flag undefined terms"** — flagged `transition model` (§3.2), `depth-limited DFS` (§4.4), `admissibility/consistency` (§3.8 leak). **Action required.**
- **"flag missing intuition"** — flagged §2.1 maze breakdown and §8 cheat-sheet analogy gaps. **Action required.**
- **"enforce analogies, every major concept needs concrete everyday analogy + 'where it breaks down' caveat, cross-linked from §3"** — §2 delivers six analogies + six caveats, and §3 does cross-reference back to them at §3.1 (maze), §3.6 (postman + leftmost). **Pass with P2 nits on analogy strength.**

**DOCUMENT.md audit:** N/A for this review (no engineer-modified directories).

**Out-of-scope observations:** None of the lecture content reviewed; this is a textbook chapter, not engineered code. One forensic note: the figure catalogue at `study/extracted_figures/L03/figures.md` is unusually thorough and well-justified — a credit to whoever extracted figures, but outside Reviewer #3's lens.

**Concerns / risks:** The §5.3 UCS worked example is the lecture's flagship example. If the round-2 reviser does not fix all three sub-defects (graph + step 3 + step 7) together, the chapter will continue to confuse the student in the single most exam-relevant location. Recommend that the reviser produce a fresh-from-scratch §5.3 in round 2 rather than patch the current text.

**What PM should do next:** Dispatch a Reviser with all 4 reviewer reports (after Reviewers 1, 2, 4 also land) to address the 3 × P0 + 8 × P1 in a single round-2 pass. Re-run Reviewer #3 in round 2 with explicit instructions to re-trace §5.3 against slide 37 line-by-line and to confirm the §5.5 DFS table is clean.

**DOCUMENT.md updated:** N/A for QA / Reviewer.
