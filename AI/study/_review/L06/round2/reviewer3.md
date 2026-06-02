# L06 Round 2 — Reviewer 3 (Pedagogical Clarity incl. Analogies)

**Scope of review:** Spec §7.1 — *Pedagogical clarity*, second pass. My remit:
1. Verify that the **three Round-1 P0** items were genuinely fixed (not papered over).
2. Verify that the **Round-1 P1** items in my pedagogy domain (P1-1 through P1-9) were addressed.
3. Hunt for **new** pedagogical bugs introduced by the revision.
4. Stay harsh. A revision that hides a wrong claim under nicer prose is *worse* than the original bug — the student now has a chapter that *sounds* authoritative while being wrong.

**Method:** I re-read §5.1, §5.2, §4.2/§4.2.1, §1, §2.1/§2.2, §6 line-by-line in the revised file, then cross-checked the slide-28 and slide-35 figures by extracting text from the source PDF (`pdftotext -layout -f 35 -l 35`) and visually inspecting `extracted_figures/L06/page35-render.png` and `page28-render.png`. The revise-summary states the figures were "verified"; I re-verified independently because the strongest claim in the new Figure 8 caption is a factual claim about slide 35.

---

## VERDICT

**MINOR REVISIONS REQUIRED — but one of the new findings is a P0 because the revision *introduced* a verifiably-false factual claim into a worked-example caption.**

Two of the three Round-1 P0 items are **fully fixed** and the fixes are pedagogically excellent. The third (Figure 8 / slide-35 reconciliation) has been "fixed" by *asserting* a claim that is **false on inspection of the source slide** — slide 35 is **not** the same 9-leaf tree as slide 28. The chapter is now confidently wrong where it used to be honestly confused. That is a worse failure mode than Round 1's and must be addressed.

Several Round-1 P1 items are excellently addressed (P1-1 α/β unpacking, P1-4 floor/ceiling mnemonic moved up, P1-5 value-vs-decision distinction, P1-3 L07 dangler, P1-9 cross-links to §6). A handful of P2 polish items remain, but most of the chapter is now in good shape.

---

## Round 1 P0 status

### R1 P0-1 (coins-game backup table) — **FIXED, and well-fixed.**

The replacement table at lines 416–425 is exactly the bottom-up "Sub-state / Player / Options / Recursion / Value" structure I suggested. I traced every row by hand against the slide-18 figure:

- $N{=}1$, MAX → 0 ✓
- $N{=}1$, MIN → 1 ✓
- $N{=}2$, MAX → $\max(1, 0) = 1$ ✓
- $N{=}2$, MIN → $\min(0, 1) = 0$ ✓
- $N{=}3$, MIN → $\min(1, 0, 1) = 0$ ✓ (take-1 / take-2 / take-3 respectively)
- $N{=}4$, MAX → $\max(0, 0, 1) = 1$ ✓ (take-3 wins)

A student can now reproduce every cell without re-segmenting prose. The added parenthetical at line 427 ("slide 18's figure draws MIN's three branches in the order 3, 2, 1 from left to right; the table above lists each branch by what MAX-or-MIN does") correctly acknowledges that the table order and the figure order don't match — *which was P2-1 in my Round-1 report*. Good catch.

**Minor remaining quibble (P2 in this round):** The table omits $N{=}3$, MAX and includes only $N{=}3$, MIN. The reason is that $N{=}3$ MAX never appears in the $N{=}4$ recursion (MAX-at-$N{=}4$ takes 1/2/3 → MIN-at-$N{=}3/2/1$ — never MAX-at-$N{=}3$). But a student who doesn't catch this asymmetry may wonder where $N{=}3$ MAX went. A one-line note "(no $N{=}3$, MAX row needed: the $N{=}4$ root only spawns MIN children)" would close the loop.

### R1 P0-2 (return-value conflict between §4.2.1 pseudocode and §5.2 walkthrough) — **FIXED.**

The new §5.2 frame-25 text (line 448) is unambiguous:

> *"Cutoff test (`if v ≤ α: return v` from §4.2.1's pseudocode): $v = 2 \le \alpha = 3$, **yes**. The function returns $v = 2$ immediately, without expanding the middle MIN's remaining two children (the leaves 4 and 6). Those two leaves are *pruned*."*

Followed by the explicit reconciliation:

> *"slide 28 draws the middle MIN annotated '≤2' because, when only the first child has been seen, MIN can only commit to *at most* 2. The actual value returned by the function is the exact running $v = 2$ — the '≤' reflects the partial-information drawing convention on the slide, not a different return value."*

This is exactly the fix I suggested (Option (a) in my Round-1 report). The two mental models are now reconciled in one paragraph. ✓

### R1 P0-3 (frame-5 description treats the same cutoff as "not real pruning") — **PARTIALLY FIXED, plus a NEW factually-wrong claim was introduced; see N1 below.**

The frame 26–27 text at line 449 is now correct:

> *"Cutoff test: $2 \le 3$? **Yes** — the function would return immediately, but in this case all three children have already been examined, so the return value is simply 2. **The same cutoff mechanism fires as in the middle MIN — the only difference is that there are no remaining children left to skip, so the prune saves no work in this particular ordering.**"*

The "same cutoff mechanism" framing is exactly what I asked for. The student now sees that nothing magical happens at the right MIN — the cutoff condition fires in both places, it just happens not to *skip* anything at the right MIN. ✓ for this finding.

But — see **N1 — Figure 8 / slide 35 reconciliation** below. The "same tree" framing introduced in the Figure 8 caption fix is **provably wrong on the source PDF**. This is a P0 in this round.

---

## NEW P0 — INTRODUCED BY THE REVISION

### N1. Figure 8 caption (line 460) and §6 pitfall 4 (line 515) make a factually wrong claim that slide 35 is "the same 9-leaf tree" as slide 28

**The problem.** Line 460 (Figure 8 caption) asserts:

> *"The same 9-leaf tree as Figure 7 (slide 28), re-annotated with explicit $\alpha$/$\beta$ values: root MAX has $\alpha = 3$; the left MIN finishes with $\beta = 3$; the middle MIN ends with $\beta = 2$ followed by 'prune!'; the right MIN ends with $\beta = 1$ followed by 'prune!'. Slide 35 only labels the leaves the sweep actually visits — leaves whose values do not influence the pruning logic are drawn but left unlabelled."*

And line 515 (§6 pitfall 4) reinforces this:

> *"slides 28 and 35 both walk the same 9-leaf abstract tree but make different aspects of the sweep visible."*

And line 462:

> *"Slide 35's annotation reflects the same algorithm on the same tree but emphasises a slightly different sweep where the right MIN's second child also triggers a cutoff at $\beta = 1$ — illustrating that with a different child-ordering at the right MIN, alpha-beta can prune *more* than 2 leaves."*

**Why this is wrong.** I extracted slide 35 directly from the PDF (`pdftotext -layout`) and the leaf labels on slide 35 are: **3, 12, 8, 2, 14, 1** — only six labelled leaves. Slide 28's labelled leaves are: **3, 12, 8, 2, 4, 6, 14, 5, 2** — nine labelled leaves. Inspection of `extracted_figures/L06/page35-render.png` shows the right MIN with **two child-triangles drawn** (labelled 14 and 1), not three. Slide 35 is unambiguously an **8-leaf tree** (or possibly 9 if you count the unlabelled middle-MIN positions, but in any case the *right MIN's children are different*).

**The decisive disproof.** The chapter claims the slide-35 "$\beta = 1$" prune at the right MIN is what you'd get with a different child-ordering of the same slide-28 right-MIN children $\{14, 5, 2\}$. **But no permutation of $\{14, 5, 2\}$ produces a running $\min$ of 1.** $\min(14, 5, 2) = 2$, and no prefix-min over any permutation of those three numbers can ever reach 1. The $\beta = 1$ value on slide 35 *requires* a leaf with value 1 to exist under the right MIN. The slide-28 tree has no such leaf. **Therefore slide 35 is a *different* tree, not "the same tree with a different ordering".**

This is the *exact* bug I flagged as R1 P1-6, and the revision has now buried it under a stronger (and falsifiable) factual claim. Round 1 said the trees were different; the chapter author then "fixed" the issue by *asserting* they are the same. A student who tries to reconstruct slide 35's prune count from the slide-28 leaves will fail and conclude the chapter is unreliable.

**Suggested fix (the only honest one).** Roll back to the Round-1-pre-revision honesty: present slide 35 as a **variation** of the example with a *different right-MIN child set* (14, 1, possibly one or two more). Either:

- **(a) Be explicit:** "Slide 35 modifies the example so the right MIN's children are $(14, 1, ?)$ instead of $(14, 5, 2)$; the leaf labelled '1' is what triggers $\beta = 1$ and the prune. The leaves 5 and 2 of slide 28 do not appear on slide 35."
- **(b) Drop Figure 8 entirely.** One walkthrough on slide 28 is enough for the worked-example role.
- **(c) Keep Figure 8 but reframe it:** "An alternative tree (with right-MIN children including a leaf valued 1) where the cutoff is even sharper; compare to Figure 7."

The revise-summary's "Slide 35 verified" line ("six labelled, with three child-positions drawn under each MIN") is **internally inconsistent** with itself — six labelled leaves cannot be drawn under three MINs each with three children unless three children are unlabelled (one per MIN), but the right MIN in the rendered figure has only *two* child slots, not three. I urge whoever signed off on the verification line to re-open the PNG.

**EVIDENCE.** Line 460 (Figure 8 caption), line 462 ("how many leaves were visited" paragraph), line 515 (§6 pitfall 4); `extracted_figures/L06/page35-render.png`; pdftotext output of slide 35: `3   12 8  2          14 1`.

---

## Round 1 P1 status

| # | Finding | Status |
|---|---|---|
| P1-1 | α/β "used vs assigned" jargon copied without unpacking | **FIXED.** Line 262 now unpacks "used" as "the cutoff test reads α from a MAX ancestor" and "assigned" as "MAX nodes update α via `α ← max(α, v)`." Exactly the disambiguation I requested. |
| P1-2 | Forward-references in §1 question list pointed to wrong subsections | **FIXED.** Lines 23–26 now correctly route Q2 → §3.3 + §4.1; Q3 → §4.2 + §4.3; Q4 → §3.4 + §5.3. |
| P1-3 | §1 references nonexistent L07 CSP chapter | **FIXED.** Line 13 now reads "in upcoming material on Constraint-Satisfaction Problems"; no broken link. |
| P1-4 | Floor/ceiling mnemonic introduced after the algorithm, not before | **FIXED.** Line 60 now leads §2.2 with the mnemonic: *"$\alpha$ is the floor MAX has already guaranteed; $\beta$ is the ceiling MIN has already imposed."* The formal definitions follow as unpacking. Excellent. |
| P1-5 | §2.1 sibling analogy didn't distinguish minimax value from minimax decision | **FIXED.** Lines 44–48 now explicitly call out: *"Two things come out of this mental simulation … the value [recursion returns] and the first move [decision wrapper picks by argmax]."* Tight, clear, and tied to the recursion in §3.3. |
| P1-6 | §5.2 presents two different trees as "the same tree" | **REGRESSED.** See N1 above. Round 1's honest "(note that slide 35 uses a slightly different right-MIN child set than slide 28)" parenthetical has been *replaced* with a flat assertion that the trees are the same. This is now factually wrong. |
| P1-7 | Figure 9 "remaining children" never quantified | **PARTIALLY FIXED.** Line 487 now says "in the full game the right MIN would have one candidate per legal O-move from its parent position." Good enough — quantifies the saving in principle without invoking a specific number that the slide doesn't show. |
| P1-8 | "Open line" definition ambiguous on empty board | **FIXED.** Line 194 now has the worked sanity check: empty board → 8 − 8 = 0; after X-centre → 8 − 4 = 4. Pitfall 6 (line 517) also rewritten with the precise definition. |
| P1-9 | §6 pitfalls not cross-linked from §4 / §5 | **FIXED.** §4.2 cutoff intro (line 254) now says "(see also §6 pitfall 2 if floor/ceiling direction is unclear)"; §4.3 closing (line 315) says "(See §6 pitfall 4.)"; §5.3 closing (line 489) says "(See §6 pitfall 5 …)". Three one-line additions, exactly as requested. |

**P1 summary:** Eight of nine P1 items fully addressed; **P1-6 regressed**, which is the basis of N1 above.

---

## NEW findings (introduced by the Round-1 revision or surfaced on second read)

### N2 (P1). §2.2 alpha-beta intuition paragraph (line 58) — improved hedge, but the math is still slightly imprecise

Line 58 now reads:

> *"MIN's job is to find the worst-for-you reply, so MIN's eventual pick will be the minimum across all replies, which is at most 2 (any further reply only pushes MIN's pick *down*, never up)."*

The "at most 2" is correct, but a careful student parses "minimum across all replies … at most 2" and asks: *why* is the minimum at most 2? Because **one** of the replies we've already seen is 2, and `min` of any set containing 2 is at most 2. The current prose is correct but doesn't show the one-step argument. One more half-sentence — "(the minimum of any set containing 2 is at most 2)" — would close the inference. P1 because it lands on the analogy paragraph that is meant to *build intuition*; a leaky inference here undoes the work.

### N3 (P1). §4.2 "$\alpha$ used / assigned" unpacking is great, but the closing prompt at line 266 ("Trace the §4.2.1 pseudocode to confirm" — was the suggested fix from R1 P1-1) is missing

My Round-1 suggestion ended with "Trace the §4.2.1 pseudocode to confirm." The revised text (line 266) says:

> *"A quick read of the §4.2.1 pseudocode below confirms all four claims. If the wording feels abstract, trace the pseudocode by hand on Figure 4 — the four '$\alpha$/$\beta$ × read/write' cells will become concrete."*

This is *better* than my original suggestion. Cleared. (Demote to P2.)

### N4 (P2). §5.2 frame numbering (lines 446–450) mixes "Frame 23/24/25/26–27/28" with "slide 23/slide 24/…" and refers to a single object two ways

The new walkthrough at lines 446–450 uses **both** "Frame 23 (slide 23)" and "Frame 26–27 (slides 26–27)" formats. A student reading the bullet list sees "Frame 26–27" as one item and might think there are *two* frames being collapsed. There is one cohesive narrative — the slides happen to spread it across multiple drawings. The cleaner choice is "Frame 4 (slides 26–27)" or "Step 4 …" — a sequential frame number that matches the *narrative* step, not the *slide* number.

(My original Round-1 finding flagged frame numbers as well; the revision swapped to slide-numbered frames, which is one of two valid choices but creates the "26–27" stutter.) Polish.

### N5 (P2). The "Pedagogy note on notation" callout in §5.2 frame 25 (line 448) is buried inside a numbered list

Line 448's "Pedagogy note on notation:" is one of the *single most important* sentences in the chapter for a student trying to reconcile the slide drawing with the pseudocode return-value convention. It is currently part of a numbered list item and shows up as ordinary running text. Promoting it to its own bullet, or to a **bold callout**, would make it findable for the student re-reading just before an exam.

### N6 (P2). The §6 pitfall 4 paragraph (line 515) is now self-contradictory after N1's bug

Line 515: *"slides 28 and 35 both walk the same 9-leaf abstract tree but make different aspects of the sweep visible."* If you fix N1 (the trees are not the same), this sentence also has to be rewritten. Mention this so the patch is complete.

### N7 (P2). The §3.4 "open lines" empty-board sanity check (line 194) is excellent but uses the phrase "open-for-X = 8" which the formula at line 190 calls "X's open lines"

Minor — but two different terms (`open-for-X` and `X's open lines`) for the same quantity in adjacent sentences slow the reader down. Pick one and use it consistently. Polish.

### N8 (P2). The reading-time estimate at line 3 jumped from "~35 min" to "~60–90 min" (per revise-summary). Good — but the "consider splitting into two sittings: §1–§4 first, §5–§8 second" advice splits at §4/§5, while my own re-read found the natural seam at §3/§4 (concepts vs algorithms). Pedagogically, "§1–§3 first, §4–§8 second" is the more natural cut because the §4 algorithm pseudocode is where the chapter's difficulty spikes

Subjective; ignore if you disagree. Polish only.

### N9 (P2). The Round-1 fix to §5.4 — labelling the "twice as deep" claim as R&N supplementary — works in §4.3 (line 311) but in §5.4 the wording at line 504 is slightly different ("the standard R&N best-case result $O(b^{d/2})$ (supplementary, §4.3)")

This is fine, but the §4.3 wording itself doesn't sit under a "§4.3" header in the chapter (it's "§4.3 Properties of alpha-beta"). The cross-reference would be more findable as "(supplementary; see §4.3's complexity table)" or similar. Pure polish.

### N10 (P2). The expanded glossary line at line 5 lists "depth-limited search / search horizon / cut-off node" as three terms, but the chapter body only uses "search depth or search horizon" and "cut-off node" once each (lines 181, 191)

If the glossary is going to enumerate three closely-related terms, the body should use each at least once in a defining sentence. Otherwise, drop the slash-list down to a single term ("search horizon (also: depth limit, cut-off depth)"). Polish.

---

## P2 items from Round 1 that remain unfixed (mostly OK)

- **R1 P2-2** "Completeness terminology" — addressed via the L03 cross-reference (line 171). Fine.
- **R1 P2-3** "Combined depth-limited alpha-beta pseudocode" — the §8 cheat-sheet pseudocode (line 574) now serves this purpose. Fine.
- **R1 P2-5** "Competitive" property — still introduced casually in the §3.1 vocabulary line. Minor.
- **R1 P2-8** "Promote breaks-down paragraphs" — not done, but the italic styling is enough. Optional.
- **R1 P2-9** "$10^{123}$ at §1 unsourced" — line 50 now anchors the derivation in §3.1; fine.
- **R1 P2-10** "Three pseudocode styles" — the §8 pseudocode is the unified version. Fine.

No new P2 fixes required from these.

---

## Things the revision did right (so the next round doesn't accidentally undo them)

1. **The §5.1 coins backup table** is now exactly the bottom-up sub-state table I suggested. Reproducible by hand from first read. Don't revert.
2. **The floor/ceiling mnemonic** in §2.2 is now the lead, not buried. The change works — the §3 formalism that follows now has a hook to hang on. Don't revert.
3. **The value-vs-decision distinction** at §2.1 closing is clean and the cross-reference to §3.3 + the MINIMAX-DECISION wrapper is correct. Don't revert.
4. **The α/β read/write unpacking** in §4.2 (line 262) makes the slide-21 jargon usable. Don't revert.
5. **The empty-board Eval sanity check** at §3.4 (line 194) is exactly the operational test a student would run. Don't revert.
6. **The §5.2 frame 25 reconciliation** of "slide draws ≤2; function returns exact 2" is the cleanest possible fix to the cutoff-return-value contradiction. Don't revert.

---

## EVIDENCE TABLE

| Finding | File | Line(s) | Status |
|---|---|---|---|
| R1 P0-1 | L06-Adversarial-Search.md | 416-427 | Fixed (excellent) |
| R1 P0-2 | L06-Adversarial-Search.md | 448 | Fixed |
| R1 P0-3 | L06-Adversarial-Search.md | 449 | Fixed (the cutoff-mechanism framing) |
| **N1 (new P0)** — slide 35 ≠ slide 28 | L06-Adversarial-Search.md | 460, 462, 515 + page35-render.png | **New factual error introduced by revision** |
| R1 P1-1 | L06-Adversarial-Search.md | 262 | Fixed |
| R1 P1-2 | L06-Adversarial-Search.md | 23-26 | Fixed |
| R1 P1-3 | L06-Adversarial-Search.md | 13 | Fixed |
| R1 P1-4 | L06-Adversarial-Search.md | 60 | Fixed |
| R1 P1-5 | L06-Adversarial-Search.md | 44-48 | Fixed |
| R1 P1-6 | L06-Adversarial-Search.md | 460 ff. | **Regressed (see N1)** |
| R1 P1-7 | L06-Adversarial-Search.md | 487 | Fixed |
| R1 P1-8 | L06-Adversarial-Search.md | 194, 517 | Fixed |
| R1 P1-9 | L06-Adversarial-Search.md | 254, 315, 489 | Fixed |
| N2 | L06-Adversarial-Search.md | 58 | New P1 |
| N3 | L06-Adversarial-Search.md | 266 | New P2 (cleared) |
| N4 | L06-Adversarial-Search.md | 446-450 | New P2 |
| N5 | L06-Adversarial-Search.md | 448 | New P2 |
| N6 | L06-Adversarial-Search.md | 515 | New P2 (entailed by N1 fix) |
| N7 | L06-Adversarial-Search.md | 194 | New P2 |
| N8 | L06-Adversarial-Search.md | 3 | New P2 |
| N9 | L06-Adversarial-Search.md | 504 | New P2 |
| N10 | L06-Adversarial-Search.md | 5 | New P2 |

---

## Report to PM

**Assignment recap:** Pedagogical-clarity review (Spec §7.1), L06 Round 2, post-revision. Verifying the three Round-1 P0 items (R3 P0-1 coins table, R3 P0-2 cutoff return value, R3 P0-3 frame-5 cutoff phrasing) plus all Round-1 P1 items in this domain.

**Status:** **Minor revisions required, but ONE P0 issue must be fixed before publication** — the revision *introduced* a factually-wrong claim into the Figure 8 caption and §6 pitfall 4. The student can disprove the chapter with three slides of arithmetic; this is worse than the Round-1 bug it was meant to fix.

**P0 findings:**
1. **N1 — Figure 8 caption (line 460), the "How many leaves were visited" paragraph (line 462), and §6 pitfall 4 (line 515) all claim slide 35 is "the same 9-leaf tree" as slide 28. It is not.** Slide 35's labelled leaves are 3, 12, 8, 2, 14, 1 (six leaves, with the right MIN's children including a leaf valued 1); no permutation of slide 28's right-MIN children {14, 5, 2} can produce slide 35's β = 1. **Suggested fix:** present slide 35 explicitly as a *variation* with a different right-MIN child set, OR drop Figure 8 entirely. **EVIDENCE:** `extracted_figures/L06/page35-render.png`, `pdftotext -layout -f 35 -l 35 "Lecture6-Adversarial Search.pdf"` outputs leaf labels `3 12 8 2 14 1`. Lines 460, 462, 515.

**P1 findings:**
1. **N2** — §2.2 line 58: the hedge "minimum across all replies … which is at most 2" works but doesn't show the one-step inference. Add a half-sentence: "(the minimum of any set containing 2 is at most 2)". Lands on the analogy paragraph and matters because it's where intuition is built.

**P2 findings:**
1. **N4** — §5.2 frame numbering mixes "Frame 26–27 (slides 26–27)" — unify to sequential narrative-step numbers.
2. **N5** — promote the "Pedagogy note on notation:" sentence in §5.2 frame 25 (line 448) out of the numbered list into a bolded callout.
3. **N6** — §6 pitfall 4 line 515 must be rewritten when N1 is fixed (entailed).
4. **N7** — §3.4 line 194: pick one of "open-for-X" or "X's open lines" and use it consistently in the sanity-check paragraph.
5. **N8** — reading-time split at §4/§5 — consider §3/§4 instead.
6. **N9** — cross-reference "(supplementary, §4.3)" at line 504 — make it a real chapter-section reference.
7. **N10** — glossary at line 5 lists three closely related terms; one (cut-off node) is used only once in the body. Either define each or collapse the list.
8. **P0-1 follow-up** — the new coins-game table is missing a note that "$N{=}3$, MAX never appears" (since the $N{=}4$ root only spawns MIN children). One line of explanation closes the asymmetry-detector loop.

**QA Checklist (§7) status:** N/A — lecture-chapter review against Spec §7.1, not a code Feature Plan.

**Acceptance criteria (§1) status:** N/A — lecture chapter.

**DOCUMENT.md audit:** N/A — lecture chapter.

**Out-of-scope observations:**
- The revise-summary's "Slide 35 verified … six labelled, with three child-positions drawn under each MIN" is internally inconsistent with itself. Whoever signed off on that verification should re-open `page35-render.png` — the right MIN there has only **two** child triangles, not three. This sign-off error is what let N1 slip through.
- The factual content of §3.3.1 (completeness, optimality, time complexity) is correctly re-attributed to L03 / R&N supplementary throughout. Reviewer 2 (factual accuracy) should still spot-check these against the source.
- The new pseudocode in §8 (line 575 onward) is the most cohesive version in the chapter, but it now uses `is_max` as a boolean parameter where §4.1's split form uses separate MAX-VALUE / MIN-VALUE functions. A student doing Lab 5 will see one style in the chapter body and another in the cheat-sheet. Not a P0 — flag for Reviewer 4 (Exam Readiness) whether this is the canonical form Lab 5 expects.

**Concerns / risks:**
- **The Figure 8 regression is the most serious finding of this round.** It is the only place in the chapter where a confidently-stated factual claim is verifiably wrong. Round 1 had three P0 *muddles*; Round 2 fixed two of them clean and replaced the third with a P0 *falsehood*. Fixing the falsehood costs one paragraph of editing, so the cost-to-fix is low — but it must be fixed before any further review round, because Reviewers 2 (factual) and 4 (exam-readiness) will both pick this up independently and re-write history.
- Beyond N1, the chapter is in genuinely good pedagogical shape. The Round-1 P1 fixes are *better than what I asked for* in at least three places (P1-1 added the Figure-4 hand-trace prompt; P1-4 mnemonic now leads §2.2; P1-5 ties the value-vs-decision split directly to the recursion + MINIMAX-DECISION).
- Specific worry: the revise-summary verification claims that didn't hold up (slide 35's "three child-positions") suggest the verification step was *visual* rather than *arithmetic*. For future rounds, the cleanest verification of a worked-example figure is to re-derive its key numbers from the leaf values — that is what would have caught N1 in 30 seconds (the β = 1 on slide 35 is impossible from the slide-28 leaf set).

**What PM should do next:** Send back to the lecture-chapter author with **N1 as the single mandatory fix** for this round. The N2 (§2.2 inference gap) is a P1 cleanup that should be done in the same pass. The remaining P2 items can be batched into a final polish pass after the cross-link / factual-accuracy reviewers have weighed in. Once N1 is fixed, this chapter is publication-ready from a pedagogical-clarity standpoint.

**DOCUMENT.md updated:** N/A for QA.
