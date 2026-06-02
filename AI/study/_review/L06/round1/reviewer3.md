# L06 Round 1 — Reviewer 3 (Pedagogical Clarity incl. Analogies)

**Scope of review:** Spec §7.1 — *Pedagogical clarity*. I judged the chapter against three questions:

1. Do the explanations build intuition before they hit symbols? (analogies, motivating mini-examples, plain-English glosses)
2. Are worked examples reproducible by a student following only the text? (no hand-wave, no jump in granularity, no ambiguous wording)
3. Are the analogies precise enough to be useful, and honestly bounded so they don't mislead?

I was harsh. The chapter is *good* but it has real pedagogical bugs — most of them in the worked examples and in places where the prose makes claims the reader cannot verify from the text alone.

---

## VERDICT

**MAJOR REVISIONS REQUIRED.**

The chapter is well-structured, the analogies in §2 are genuinely illustrative (the "divide the weekend with a devious sibling" analogy and the "stop reading a bad chess line" gloss are both excellent), and the cheat-sheet is unusually well-crafted. **But** the chapter contains:

- Two reproducibility failures in the worked examples (§5.1 coins game, §5.2 alpha-beta walkthrough — see P0-1 and P0-2),
- A bogus pedagogical statement of the alpha-beta cutoff conditions that conflates two different uses of α/β (P1-1),
- A forward-reference to a non-existent §6 "Pitfalls" section that is actually numbered §6 *but* labelled "Common Pitfalls / Exam Traps" in the chapter, *and* a forward reference to §7 from §4.7 that is wrong — there is no §7 expectiminimax preview, the preview is §4.6 (P1-2),
- A forward reference to a non-existent "L07" CSP chapter in §1 motivation (P1-3),
- Several analogies that break down in ways the chapter does not flag (P2),
- A missing "where to look in the slides" callout for the most-confusing slide (slide 21's α-is-used-in-MIN convention, P1-4).

None of these are pure factual errors that another reviewer might not catch (those are §7.2's job). They are pedagogical bugs: places where a smart student following the chapter end-to-end will get *stuck*, *misled*, or *unable to reproduce the figure*. Listed below from worst to least bad.

---

## P0 — BLOCKING

### P0-1. §5.1 Coins-game backup table is unreadable / wrong granularity (lines 393-402)

**The problem.** The "Backing up the minimax values" table on lines 394-401 mixes two levels of the recursion in a way no student can follow. Row 1 backs up MIN-at-$N=3$ but to do so it needs the value of MAX-at-$N=2$ — and the table puts that helper *below* row 1, with the parenthetical "(helper)". A reader following the rows top-to-bottom hits a forward reference on the very first line.

**Worse**, the prose inside row 1 of the table is so dense it is almost unparseable:

> *"MIN's options: take 1 → MAX at $N{=}2$ (value 1, see next line); take 2 → MAX at $N{=}1$ (forced take 1 → MAX took last → $F(S){=}0$, so MAX-at-$N{=}1$ value is 0); take 3 → leaf $N{=}0$, MIN just took last → $F(S){=}1$. MIN picks min(1, 0, 1) = 0."*

This is six layers of nested reasoning in one sentence. A student trying to *verify* this — which is the whole point of a worked example — has to mentally re-segment it. The slide-18 figure also numbers the moves on the edges (1, 2, 3); the table never refers to those edges, so the reader can't cross-check against the figure.

**What's correct.** I traced the recursion by hand and the final answer (root value = 1, optimal first move = take 3) IS correct. The intermediate values are also correct. The pedagogical failure is purely in presentation.

**EVIDENCE.** Lines 393-402 of `L06-Adversarial-Search.md`.

**Suggested fix.** Replace the single confusing table with a bottom-up backup, in this order:

1. Start at the smallest subtree value and build up.
2. State each sub-value on its own row with the recursion shown explicitly:

```
N=1, MAX to move: MAX forced to take 1 → reaches N=0, MAX took last → F=0. value = 0.
N=1, MIN to move: MIN forced to take 1 → reaches N=0, MIN took last → F=1. value = 1.
N=2, MAX to move: take 1 → MIN-at-N=1 (=1); take 2 → N=0, MAX took last (F=0). max(1,0) = 1.
N=2, MIN to move: take 1 → MAX-at-N=1 (=0); take 2 → N=0, MIN took last (F=1). min(0,1) = 0.
N=3, MIN to move: take 1 → MAX-at-N=2 (=1); take 2 → MAX-at-N=1 (=0); take 3 → N=0, MIN took last (F=1). min(1,0,1) = 0.
Root N=4, MAX: take 1 → MIN-at-N=3 (=0); take 2 → MIN-at-N=2 (=0); take 3 → MIN-at-N=1 (=1). max(0,0,1) = 1. → take 3.
```

This is reproducible. The current table is not.

### P0-2. §5.2 alpha-beta walkthrough makes an off-by-one error in the description of when the middle MIN gets pruned (lines 422-423)

**The problem.** The frame-3 prose says:

> *"DFS descends into the middle MIN. First leaf is 2 → middle MIN's $\beta$ drops to 2. Now check the alpha-cutoff condition at this MIN: is $\beta = 2 \le \alpha = 3$ of the MAX root? **Yes.** Therefore the remaining two children of the middle MIN (the ones whose leaves are 4 and 6) are **pruned**."*

This says the cutoff fires *after the first leaf*, having seen only the value 2. That is correct for slide 25 (which shows the middle MIN with $\le 2$ after one child). **But** the chapter's own §4.2 alpha-beta pseudocode (lines 272-279) has the cutoff condition as `if v ≤ α: return v` *before* the inner-loop `β ← min(β, v)` update. With $\alpha = 3$, $v = 2$ at the first leaf: $v \le \alpha$ is true, so the function returns 2 — meaning the middle MIN's "backed-up value" is 2, *not* "$\le 2$". The chapter then asserts in Figure 7's caption that the middle MIN's value is "≤ 2" because two leaves "were never visited" — but by the pseudocode the function returned the exact value 2 on the first child. **The "$\le$" notation comes from the slide's *partial-information drawing convention*, not from the algorithm.**

This is a serious pedagogical bug: the chapter teaches one cutoff convention in §4.2 (return the running $v$ immediately) and then uses a different convention in §5.2 (record "$\le 2$" as if the function returned a bound). A student trying to implement alpha-beta from the chapter will get confused about what value to return on a cutoff.

**Suggested fix.** Either:
- (a) Acknowledge that the slide's "$\le 2$" notation reflects *the partial information available before the cutoff*, but the function actually returns $v = 2$ when the cutoff fires. Add one sentence in §5.2 frame 3.
- (b) Or change the pseudocode in §4.2 to use a fail-soft convention (return a true upper bound instead of $v$).

Option (a) is the cheaper fix and matches the lecture slides. But the chapter must call this out, or it leaves students with two contradictory mental models of alpha-beta.

**EVIDENCE.** Lines 272-279 (pseudocode), lines 422-423 (walkthrough frame 3), line 430 (Figure 7 caption "value is shown only as ≤ 2").

### P0-3. §5.2 Frame 4–5 description contradicts itself about whether the right MIN's last leaf triggers a "real" cutoff (lines 424)

**The problem.** Frame 4–5 prose says:

> *"Next leaf is 2 → $\beta$ drops to 2. Now: $\beta = 2 \le \alpha = 3$ at root — alpha-cutoff! But there are no remaining children to prune, so this just finalises the right MIN's value as 2."*

By the chapter's own pseudocode (line 277, `if v ≤ α: return v`), when the right MIN finds $v = 2$ on its third child, with $\alpha = 3$ from the root, the function returns $v = 2$ immediately — same as the middle MIN case in P0-2 above. The phrasing "this just finalises the right MIN's value as 2" is technically correct but is doing pedagogical sleight-of-hand: it's the same cutoff mechanism, but the chapter describes it differently because there happen to be no more children. A student reading frames 3 and 5 side-by-side will not see that the *same algorithmic step* is happening in both; they'll think one is "real" pruning and the other isn't.

**Suggested fix.** Add a single sentence at the end of frame 4–5: "Mechanically the same cutoff fires here as in frame 3; the only difference is that there are no remaining children for the cutoff to *skip*. The function still returns immediately with $v = 2$."

**EVIDENCE.** Line 424.

---

## P1 — IMPORTANT

### P1-1. §4.2 "convention often confused on exams" callout is the very thing that will confuse students (lines 241-245)

**The problem.** Lines 242-244:

> - *"$\alpha$ is used in MIN nodes and is assigned in MAX nodes."*
> - *"$\beta$ is used in MAX nodes and is assigned in MIN nodes."*

This is **verbatim copied from slide 21** without the pedagogical scaffolding that the slide also lacks. It is a famously confusing piece of jargon (slide 21 itself flags it: *"convention often confused on exams"*). The chapter reproduces the confusion instead of unpacking it.

A student reading this asks: "What does 'used in MIN nodes' even mean? Used how? Used to *check* a cutoff? Used to *update* something? Both?" The chapter never answers this. The §4.2.1 pseudocode shows that:

- In `MAX-VALUE` the cutoff test is `if v ≥ β`, so $\beta$ is *read* in MAX nodes ✓
- In `MAX-VALUE` the line `α ← max(α, v)` *updates* $\alpha$ in MAX nodes ✓
- Symmetric in `MIN-VALUE`.

So "used" means "read for the cutoff test" and "assigned" means "updated as the running best". The chapter has the information needed to disambiguate but **never makes the link explicit**. The exam-trap warning in §6 (lines 487-488) repeats the jargon ("$\alpha$ is *assigned* (updated) at MAX nodes ... and *used* (read for cutoff decisions) at MIN nodes") and this is the first time "used = read for cutoff" appears in the text — buried in the pitfalls section.

**Suggested fix.** In §4.2, immediately after lines 243-244, add:

> "Concretely: '$\alpha$ is used in MIN nodes' means *the MIN-node cutoff test reads $\alpha$ from a MAX ancestor*. '$\alpha$ is assigned in MAX nodes' means *only MAX nodes update $\alpha$ (with $\alpha \leftarrow \max(\alpha, v)$)*. Symmetric for $\beta$ at MIN/MAX swapped. Trace the §4.2.1 pseudocode to confirm."

This converts the slide's confusing one-liner into something a student can actually use.

**EVIDENCE.** Lines 241-245 (§4.2), lines 487-488 (§6 pitfall 1).

### P1-2. Forward-reference confusion in §1 Overview (lines 21-26) and §4.7 (line 339)

**Problem A** (lines 21-26). The overview promises:

> *"This chapter answers four questions:
> 1. **What kind of environment are games?** (§3.1)
> 2. **What is the optimal strategy against a perfect opponent?** → Minimax. (§3.3, §4)
> 3. **How do we make it fast enough to be useful?** → Alpha-beta pruning. (§4)
> 4. **What do we do when the tree is still too deep to search to the end?** → Evaluation functions and depth-limited search. (§3.4, §5.3)"*

But the chapter actually has §3.4 *before* §4 — so question 4 is answered before question 3. More importantly, "(§3.3, §4)" for minimax is wrong: minimax-the-algorithm lives in §4.1, not "§4" as a whole. The current pointer sends the reader to §4.2 (alpha-beta) when they wanted §4.1 (minimax).

**Problem B** (line 339, §4.6). The expectiminimax preview links to "L09a's *expected utility*" via the parenthetical:

> *"(This connects to L09a's *expected utility*: a CHANCE node *is* an expected-utility computation over a discrete distribution.)"*

There is no §3 of L09a defined yet (it's a future lecture). This is fine as a forward-pointer, but the bare "L09a §3" with no chapter title is jarring after the chapter has been so careful with cross-links elsewhere.

**Problem C** (line 26 says "§5.3" for question 4). §5.3 is the *worked example*, not the *explanation*. The explanation is §3.4. The chapter's own §1 sends students to the wrong section.

**Suggested fix.** Renumber the forward references in §1:
- Q1 → §3.1 ✓
- Q2 → §3.3 (definition) + §4.1 (algorithm)
- Q3 → §4.2 (algorithm) + §4.3 (properties)
- Q4 → §3.4 (definition) + §5.3 (worked example)

**EVIDENCE.** Lines 21-26, line 339.

### P1-3. §1 references "L07 — CSPs" but no such chapter exists yet (line 13)

**The problem.** Line 13: *"in L07 the constraints are fixed and we get to choose every variable."* This is a forward-reference to a lecture/chapter that, given the course numbering, presumably covers Constraint Satisfaction. But the chapter's prereq line (line 3) lists only L02, L03, L05 — no L07. If L07 doesn't exist as a written chapter, the reference is broken; if it does, it should be in the prereq list with a link.

**Suggested fix.** Either link to `L07-CSPs.md` (if it exists) or rephrase to "Constraint-Satisfaction Problems (a topic we haven't covered yet)" so the reader doesn't go looking.

**EVIDENCE.** Line 13.

### P1-4. The α-floor / β-ceiling mnemonic is introduced *after* the algorithm, not before (lines 245, 488)

**The problem.** The clearest mental model for α/β in the whole chapter is the slide-21 mnemonic *"$\alpha$ = at least; $\beta$ = at most"* (line 245) and the §6 "$\alpha$ is the floor, $\beta$ is the ceiling" (line 488). This is *the* sentence that makes α/β click for a student. But:

- In §2.4 the analogy section, where mnemonics belong, the mnemonic is absent. §2.2 introduces α/β by saying "$\alpha$ = the best value MAX is *already guaranteed* to achieve, somewhere above" (line 55) — accurate, but heavy.
- The mnemonic finally appears in §4.2 as a parenthetical (line 245), after the full algorithm has been stated.
- It reappears, restated, in §6 pitfalls (line 488).

A pedagogical chapter should put the mnemonic **first**, then derive the formal definition. The chapter does it backwards.

**Suggested fix.** Move the floor/ceiling mnemonic into §2.2 as the *opening* gloss before the bullet-list definitions of α and β:

> *"The whole alpha-beta bookkeeping rests on one mnemonic: **$\alpha$ is the floor MAX has already guaranteed; $\beta$ is the ceiling MIN has already imposed.** Whenever a node sees the other side's bound cross its own, the rest of the subtree can't matter."*

Then keep the formal definitions below it as the unpacking.

**EVIDENCE.** Lines 55-56, 245, 488.

### P1-5. §2.1 "weekend with a devious sibling" analogy is great but mis-describes what minimax *returns* (line 40)

**The problem.** Line 40 says the mental model is:

> *"For each of your candidate first moves, you assume your sibling will pick the worst-for-you reply ... You then take the first move whose imagined endgame leaves you happiest **assuming both of you play perfectly throughout**."*

This is correct but conflates the *minimax value of a state* (a number) with the *minimax decision* (an action). The recursion in §3.3 (lines 124-132) returns the *value*; the *decision* requires `argmax`. The chapter does eventually distinguish these (lines 137, 216-217 with `MINIMAX-DECISION`) but the analogy in §2.1 erases the distinction and the student never gets the "value vs. decision" framing tied to the analogy.

This matters because the most common student bug is to write `MINIMAX(state)` and try to return the best action from it — confusing the two.

**Suggested fix.** Add one sentence at the end of §2.1:

> *"Two things come out of this mental simulation: (a) the **value** you'd end up with (the number bubbled up from the leaves), and (b) the **first move** that achieves that value. Most students conflate the two. Minimax-the-recursion computes (a); the decision wrapper at the root picks (b) by argmax."*

**EVIDENCE.** Lines 38-40, lines 137, 216-217.

### P1-6. §5.2's two-figure switcheroo (slide 28 vs slide 35) is poorly explained (lines 432-437)

**The problem.** Lines 432-437 introduce Figure 8 as "the same abstract tree" — but the parenthetical on line 435 admits:

> *"Note that slide 35 uses a slightly different right-MIN child set than slide 28 (it shows leaves 14, 1 instead of 14, 5, 2 — both illustrate the same algorithm; the slide-35 version triggers an even earlier prune because the first leaf already drops $\beta$ to 1.)"*

So it's *not* the same tree. The student is told it is, then told (in parenthesis) that it isn't. That's a pedagogical fail. The whole point of revisiting an example is to consolidate one mental model; presenting a *different* tree under "the same tree" undermines that.

Worse, the prune *count* line 437 mixes the two trees:

> *"On slide 28's frame ordering: 3 + 1 + 3 = 7 of the 9 leaves were visited; 2 were pruned. On slide 35's ordering: 3 + 1 + 1 = 5 of the (now 8) leaves; 3 were pruned."*

For the slide-35 tree (which the student has just been told is "the same tree"), the leaf count is now 8 instead of 9. The student now has to mentally reconstruct which tree has 8 leaves vs 9. Either present them as two distinct examples or stick to one.

**Suggested fix.** Either:
- (a) Remove Figure 8 entirely; one walkthrough on the slide-28 tree is enough.
- (b) Or present slide 35 as a *separate* "variation" example: "Now consider a *modified* tree where the right MIN's children are (14, 1) instead of (14, 5, 2). What changes?" — making the variation explicit rather than smuggling it in.

**EVIDENCE.** Lines 432-437.

### P1-7. Figure 9 caption (line 462) refers to a result *not* shown in the figure

**The problem.** Figure 9 caption says:

> *"Root MAX has $\alpha = 1$ from the left subtree; the right MIN's first leaf yields evaluation −1, dropping $\beta$ to −1, which immediately triggers an alpha-cutoff so the remaining children of the right MIN are pruned."*

But the §5.3 walkthrough has only described **one** child being expanded for the right MIN (slide 33-34). The student doesn't know *how many* children the right MIN had — the slide draws only one. So "the remaining children" is vacuous: were there 1, 5, or 20? The pedagogical point of "look how much we saved!" is lost because the student can't quantify the saving.

**Suggested fix.** Either:
- (a) State explicitly: "The right MIN had $k$ candidate children corresponding to $k$ possible O-moves; after the first leaf triggered the cutoff, the other $k - 1$ were skipped."
- (b) Or de-emphasize the "remaining children" phrasing and instead say "we don't expand the right MIN any further."

**EVIDENCE.** Lines 461-462 (Figure 9), §5.3 walkthrough lines 451-459.

### P1-8. §6 Pitfall 6 — "Misreading the evaluation function for tic-tac-toe" — defines "open line" inconsistently with itself (line 492)

**The problem.** Line 492:

> *"The slide formula is 'X's open lines − O's open lines', where 'open' means **no opponent marks yet**. A line with exactly one X is open for X; a line with both X and O is open for neither. A common error is to count 'lines that contain an X' — that's not what 'open' means."*

This says "open" means "no opponent marks yet". But for a totally empty line (no marks at all), is it open for X or for O? By the rule "no opponent marks yet" it is **open for both** — and the chapter's own §3.4 (line 177) and the cheat-sheet (line 542) describe Eval as the *difference* (X open lines − O open lines). If empty lines are counted in both terms, they cancel out — which is the intended behavior. But the chapter never says this explicitly. A student computing Eval on an empty 3×3 board will get 8 − 8 = 0 (8 lines: 3 rows + 3 cols + 2 diagonals) and not know if that's right.

**Suggested fix.** Add a worked example to §3.4 or §6 pitfall 6:

> *"Sanity check: on an empty 3×3 board there are 8 lines (3 rows, 3 columns, 2 diagonals), all open for both X and O. Eval = 8 − 8 = 0. After X plays the centre, Eval = 8 − 4 = 4 (X's lines now include all 4 lines through the centre as open-for-X; O's open lines are the 4 lines not through the centre)."*

Without this, the formula is technically defined but operationally vague.

**EVIDENCE.** Lines 177, 492, 542.

### P1-9. The §6 pitfall list is the most useful part of the chapter but is not cross-linked from §4 / §5 (lines 483-498)

**The problem.** §6 is a goldmine — pitfalls 1, 2, 3, 4 are all things the §4 algorithm description glosses over. But §4.2 / §4.3 / §5.2 / §5.3 never say "if you find this confusing, see §6 pitfall N". A student doesn't know §6 exists until they reach it.

**Suggested fix.** Add forward-reference callouts in §4 and §5:

- §4.2 cutoff direction → "(see §6 pitfall 2 if floor/ceiling is unclear)"
- §4.3 best-case complexity → "(see §6 pitfall 4 on move ordering)"
- §5.3 evaluation function usage → "(see §6 pitfall 5 on never using Eval at terminals)"

This is a one-line-per-section fix.

**EVIDENCE.** Lines 483-498 (§6); lines 228-300 (§4); lines 441-466 (§5.3).

---

## P2 — POLISH / SUGGESTIONS

### P2-1. §2.2 analogy "stop reading a bad chess line" is excellent but conflates two cases (line 52)

Line 52 says:

> *"Halfway through, you see one reply your opponent could make that *already* drops you to a payoff of 2. You don't need to look at any more of B's branches — your opponent will pick that reply (or something even worse for you), so **B is already worse than A**."*

The "or something even worse for you" hedge is doing important work — it's the reason you can prune *all* remaining replies, not just the one bad one. The chapter could lean into this: "MIN's job is to find the worst-for-you reply, so any reply at $\le 2$ guarantees MIN's final pick is also $\le 2$." One added clause makes the logic airtight.

### P2-2. §3.3.1 properties list doesn't explain *why* minimax is "complete on finite game trees" (line 158)

Line 158 says minimax is "Complete on finite game trees (every branch eventually hits a terminal)." But L03 §3's definition of completeness is *"the algorithm finds a solution if one exists"*. Game trees don't have "solutions" — they have minimax values. The reuse of L03's "completeness" terminology here is sloppy. Either define what completeness means for minimax (every node gets a value) or drop the bullet.

### P2-3. §4.4 comparison table includes "Depth-limited alpha-beta + evaluation function" but never names this algorithm (line 304)

The table on line 304 lists a third row "Depth-limited alpha-beta + evaluation function". The body of §4 never gives this combined algorithm a pseudocode block or a section heading — it's spread across §3.4 (Eval) + §4.2 (alpha-beta). A student looking up "how do you actually code a depth-limited game player?" gets sent to two different sections with no glue. Consider adding a §4.2.2 "Putting it together — depth-limited alpha-beta" with a single 12-line pseudocode block that combines both, since this is the algorithm Lab 5 actually asks the student to implement.

### P2-4. The "$O(b^{3d/4})$ average case" claim (line 291) has no source

Line 291 states:

> *"**Average case** with random child ordering: roughly $O(b^{3d/4})$ — still a substantial saving."*

This number doesn't appear in the slides. It's a Russell & Norvig result, but the chapter doesn't cite anything. If the chapter is taking it from R&N, say so; otherwise drop it or hedge ("roughly $b^{3d/4}$ under some assumptions").

### P2-5. §3.1 environment-property list (line 94) drops "competitive" between bullets without defining it relative to L02

Line 94:

> *"In L02's vocabulary this corner is: **multi-agent, competitive, deterministic, fully observable, sequential, static, discrete**."*

"Competitive" is the new vocabulary the chapter is supposedly adding. The chapter introduces it casually mid-list. Calling it out — "the new property is *competitive* (= utilities sum to zero)" — would land harder.

### P2-6. §2.4 says "Negotiation can be win-win" — true but undercuts §1's motivation (line 74)

§1 line 19 says minimax models "negotiation, auctions, ad bidding" but §2.4 line 74 says "Negotiation can be win-win" — so the §1 motivation is actually a *misapplication* of minimax that §2.4 corrects. Either soften §1 ("competitive negotiation, e.g. zero-sum bidding") or have §1 forward-reference §2.4.

### P2-7. §5.3 result statement (line 459) gives the value but not the move

Line 459: *"MAX plays the left move (the one whose subtree had value 1)."* Good. But the original §3.3 worked example (§5.2) ended with the value AND identified the move by edge label ($a_1$). §5.3's "left move" is vague — was that placing X in the corner? In the centre? The slide-29 figure draws the candidate moves but the prose never refers to them by position. A student writing exam notes would want "MAX plays X-in-corner (left subtree)" rather than "MAX plays the left move".

### P2-8. The "where the analogy breaks down" sections are excellent and should be more prominent

The "*Where the analogy breaks down:*" italicised paragraphs in §2.1, §2.2, §2.3, §2.4 are the chapter's pedagogical highlight. They model intellectual honesty (every analogy lies a little). Consider promoting them to bold-italic or boxing them, so a re-reader can find them at a glance.

### P2-9. §1 line 13 "$10^{123}$ continuations" is good but unsourced/unverified at that point in the chapter

The reader sees "$10^{123}$" in §1 before §3.1 explains where it comes from. A small parenthetical "(we'll derive this in §3.1: $35^{80} \approx 10^{123}$)" would make the reader trust the number.

### P2-10. The cheat-sheet (§8) Pseudocode at line 549-563 uses a *third* style different from §4.1 and §4.2.1

The chapter has now shown three pseudocode styles:
- §4.1 (lines 201-218): split MAX/MIN versions, with `MINIMAX` and `MINIMAX-DECISION`
- §4.2.1 (lines 260-280): `MAX-VALUE` / `MIN-VALUE` / `ALPHA-BETA-DECISION`
- §8 (lines 549-563): combined `ALPHA-BETA-VALUE(state, α, β, is_max)`

The third version is cleaner but the student now has to mentally translate between them. Either use one canonical style throughout or call out explicitly that §8's compact form unifies §4.2.1's split form.

---

## EVIDENCE TABLE (quick lookup)

| Finding | File | Line(s) |
|---|---|---|
| P0-1 Coins backup table | L06-Adversarial-Search.md | 393-402 |
| P0-2 Cutoff return-value conflict | L06-Adversarial-Search.md | 272-279, 422-423, 430 |
| P0-3 Frame-5 cutoff phrasing | L06-Adversarial-Search.md | 424 |
| P1-1 α/β "used vs assigned" jargon | L06-Adversarial-Search.md | 241-245, 487-488 |
| P1-2 §1 / §4.7 forward-refs | L06-Adversarial-Search.md | 21-26, 339 |
| P1-3 L07 dangling reference | L06-Adversarial-Search.md | 13 |
| P1-4 Floor/ceiling mnemonic late | L06-Adversarial-Search.md | 55-56, 245, 488 |
| P1-5 Value vs decision analogy gap | L06-Adversarial-Search.md | 38-40, 137 |
| P1-6 Slide-28/35 same-tree fib | L06-Adversarial-Search.md | 432-437 |
| P1-7 Figure 9 "remaining children" | L06-Adversarial-Search.md | 461-462 |
| P1-8 "Open line" ambiguity | L06-Adversarial-Search.md | 177, 492, 542 |
| P1-9 §6 not cross-linked | L06-Adversarial-Search.md | 483-498 |
| P2-1 Analogy hedge "or worse" | L06-Adversarial-Search.md | 52 |
| P2-2 Completeness terminology | L06-Adversarial-Search.md | 158 |
| P2-3 No combined pseudocode | L06-Adversarial-Search.md | 304 |
| P2-4 Average-case unsourced | L06-Adversarial-Search.md | 291 |
| P2-5 "Competitive" introduced silently | L06-Adversarial-Search.md | 94 |
| P2-6 Negotiation contradiction | L06-Adversarial-Search.md | 19, 74 |
| P2-7 §5.3 vague move name | L06-Adversarial-Search.md | 459 |
| P2-8 Promote "breaks down" sections | L06-Adversarial-Search.md | 44-47, 58-60, 66-68, 73-74 |
| P2-9 $10^{123}$ unsourced in §1 | L06-Adversarial-Search.md | 13 |
| P2-10 Three pseudocode styles | L06-Adversarial-Search.md | 201-218, 260-280, 549-563 |

---

## Things the chapter does well (so the next round doesn't accidentally break them)

1. **§2 analogies before §3 formalism** is the right structure. The "weekend with a devious sibling" and the "stop reading a bad chess line" glosses are genuinely illustrative and would survive contact with a real student.
2. **"Where the analogy breaks down" paragraphs** in every §2 subsection are the best pedagogical move in the document. Don't remove them.
3. **The cheat-sheet (§8)** is unusually well-crafted, especially the symbol glossary table and the exam-night checklist. Keep both.
4. **The §6 pitfalls list** is the single most useful section for an exam-prep audience. The only flaw is that it's hidden — see P1-9.
5. **Cross-links to L02/L03/L05** at the top of the chapter are properly scoped and accurate (modulo P1-3's L07 issue).
6. **Worked example §5.4 (chess magnitude)** is short, vivid, and gives the right scale-of-the-problem intuition.

---

## Report to PM

**Assignment recap:** Pedagogical-clarity review (Spec §7.1) of `study/lectures/L06-Adversarial-Search.md`, Round 1, Reviewer 3.

**Status:** Major revisions required before this chapter is exam-ready.

**P0 findings:**
1. §5.1 coins-game backup table mixes recursion levels in unparseable prose (lines 393-402) — student cannot reproduce the figure.
2. §5.2 alpha-beta walkthrough conflicts with §4.2.1 pseudocode about whether a cutoff returns `v` or "≤ v" (lines 272-279 vs 422-423, 430).
3. §5.2 frame-5 prose treats the same cutoff mechanism as a "non-prune" because no children remain — gives student a wrong mental model of what counts as pruning (line 424).

**P1 findings:**
1. α/β "used vs assigned" jargon copied from slide 21 without unpacking (lines 241-245).
2. §1 forward-references to wrong subsections, plus a §7 / L09a §3 reference inconsistency (lines 21-26, 339).
3. §1 references nonexistent "L07" CSP chapter (line 13).
4. Floor/ceiling mnemonic introduced late — it should be the lead analogy, not buried in pitfalls (lines 55-56, 245, 488).
5. §2.1 sibling analogy doesn't distinguish minimax value from minimax decision (lines 38-40).
6. §5.2 presents two *different* trees (slide 28 and slide 35) as "the same tree" (lines 432-437).
7. Figure 9 caption says "remaining children pruned" but never says how many children there were (lines 461-462).
8. §6 pitfall 6 on "open lines" doesn't disambiguate empty-line case (lines 177, 492, 542).
9. §6 pitfalls list has no inbound cross-links from §4 / §5 (lines 483-498).

**P2 findings:** 10 polish items, see main report — most are 1-line fixes.

**QA Checklist (§7) status:** Not applicable to a lecture-chapter review; this review evaluates Spec §7.1 (pedagogical clarity) of the lecture-chapter spec, not a Feature Plan's QA checklist.

**Acceptance criteria (§1) status:** N/A — lecture chapter, not a code feature.

**DOCUMENT.md audit:** N/A — lecture chapter, not a code feature.

**Out-of-scope observations:**
- The coins-game minimax answer (root value = 1, optimal move = take 3) is *factually correct* — I verified the full backup by hand. So §7.2 (factual accuracy) will not catch P0-1; it's a pure pedagogy bug. Flag this for Reviewer 4 (Exam-Readiness).
- The chapter relies heavily on `extracted_figures/L06/page*-render.png` figures that I did not verify exist on disk — Reviewer 2 (assets) should confirm.
- The text contains 9 distinct cross-references to other lecture markdown files (L02, L03, L05, L09a, L10, plus Lab 5 handout). At least one (L07) is dangling. Reviewer 5 (cross-link integrity) should sweep all of them.

**Concerns / risks:**
- The chapter is on the *verge* of being excellent. The P0 items are structural in the worked examples — fixing them is mechanical, not creative. The P1 items are mostly forward-reference housekeeping plus one prose unpacking (P1-1). Two hours of editing fixes this whole list.
- Specific worry: P0-2 (return-value conflict) is the kind of bug that makes a student fail a coding lab. Lab 5 is downstream of this chapter; the inconsistency between the pseudocode and the walkthrough must be resolved before Lab 5 students touch this material.

**What PM should do next:** Send back to the lecture-chapter author with the P0/P1 list. Re-QA after fixes. Then proceed to Reviewer 4 (Exam-Readiness) and Reviewer 5 (Cross-link integrity). Do *not* publish or share until at least the P0 items are fixed.

**DOCUMENT.md updated:** N/A for QA.
