# Lab4-GA Round 1 — Reviewer #4 (Variant Adaptability)

## Report to PM

**Assignment recap:** Lab4-GA Round 1. Reviewer #4 perspective:
**variant adaptability** — can the locked solution answer the three
mandatory exam variants in `variants.md` using ONLY the allowed
surfaces (header docstring + `# KNOB:` comments + `def` lines)?
Plan/spec source = `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab4-GA\variants.md`.
Files inspected (all absolute paths):

- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout_lab_4\ga_solution.py`
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout_lab_4\Number_solution.py`
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout_lab_4\Queen_solution.py`
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout_lab_4\queens_fitness_solution.py`
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout_lab_4\Lab 4.pdf` (cross-checked content against KNOB claims)

**Status:** **Pass with concerns** — all three mandatory gate variants
are solvable using only the surface the spec allows, but several
documentation defects, name mismatches, and one outright incorrect
"HOW TO ADAPT" recipe will trip an exam agent that follows the docs
literally. Two of these are P0 because they will cause an agent to
emit code that crashes or silently picks the wrong fitness function.

---

### P0 findings (block the gate as-currently-written)

**P0-1. `queens_fitness_solution.py` HOW-TO-ADAPT item 2 references a
parameter that does not exist on `fitness_fn_weighted`.**
- File: `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout_lab_4\queens_fitness_solution.py`
- The header docstring (lines 46-50) says: *"call `fitness_fn_weighted`
  with `column_weight = 3` from the Board's `get_fitness()`. The
  default `column_weight = 1` reproduces `fitness_fn_negative`
  exactly"*.
- The actual `def` line (line 153-157) is
  `fitness_fn_weighted(board_view, diag_weight=…, row_weight=…)`. There
  is no `column_weight` keyword.
- The `DEFAULT_DIAG_WEIGHT` KNOB block (lines 78-90) further claims
  "diagonals are by far the most common conflict in this
  representation (one-queen-per-column already eliminates column
  attacks)" — which **contradicts** the HOW-TO-ADAPT item 2 that talks
  about penalising "column conflicts". An agent reading only the
  header docstring will produce a `TypeError: unexpected keyword
  argument 'column_weight'` on the variant 3-adjacent
  weighted-conflict question. Doc spec drift between the header and
  the KNOB blocks within the same file.
- **Suggested fix:** Rewrite item 2 of the HOW-TO-ADAPT block to talk
  about `diag_weight` and `row_weight` and delete the
  `column_weight` reference. Mention that column-conflicts are
  structurally impossible under this gene encoding so there is no
  knob for them.

**P0-2. `Queen_solution.py` HOW-TO-ADAPT item 5 calls out an "Appendix
B variant 3" that does not exist in `variants.md`.**
- File: `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout_lab_4\Queen_solution.py` (header lines 77-85).
- Says *"To penalise diagonals 3x (Appendix B variant 3 …): set
  `QUEENS_FITNESS_VARIANT = 'weighted'`"*. There is no "Appendix B"
  in the locked `variants.md` (mandatory variants 1-3 + optional 4a-4c
  are all there is). The phrasing implies an extra rubric the gate
  does **not** evaluate against, so an exam agent told "do the only
  variant you can identify" may pick this phantom variant and emit
  the wrong answer. It also undermines reviewer trust in the
  variant catalog.
- **Suggested fix:** Either (a) delete item 5 entirely, or (b) move
  the "diagonals 3x" idea into `variants.md` as an explicit optional
  variant 4d so the cross-reference is real.

---

### P1 findings (important — fix before round-2 gate)

**P1-1. `SHOULD_TRIM_POPULATION` / `MAX_POPULATION_SIZE` name mismatch
between `variants.md` (optional 4b) and the locked solution.**
- `variants.md` line 106-107: *"set `TRIM_POPULATION = True` and
  `MAX_POPULATION_SIZE = 30`"*.
- Solution KNOB (`ga_solution.py` line 276-295): the actual name is
  `SHOULD_TRIM_POPULATION`. An exam agent that reads only
  `variants.md` and then greps the KNOB list for `TRIM_POPULATION` will
  hit two candidates and pick the wrong one or fail. Worse, this is
  exactly the kind of needle an exam agent isn't supposed to chase
  outside the allowed surface area.
- **Suggested fix:** Either rename the KNOB to `TRIM_POPULATION` (drops
  the Hungarian-ish `SHOULD_` prefix, less Pythonic anyway) or fix
  `variants.md` 4b to use the exact name. Prefer the latter; the
  current `SHOULD_TRIM_POPULATION` name is descriptive.

**P1-2. Variant 1 "expected MAX_GENERATIONS bump (e.g. 30 to 200 or
500)" disagrees with the solution's actual default of 100.**
- `variants.md` Variant 1 implies default `MAX_GENERATIONS = 30`
  ("bumping e.g. from 30 to 200 or 500"). The locked solution
  has `MAX_GENERATIONS_QUEENS: int = 100` (line 227 of
  `ga_solution.py`). The "30" anchor is the Number demo's default, not
  the queens demo. An exam agent that bumps from 30 to 200 will think
  it changed something when it actually halved the default.
- **Suggested fix:** Edit Variant 1's expected-change paragraph in
  `variants.md` to say "bump from 100 to 500" (or whatever the actual
  default is). Also worth referencing the KNOB name precisely
  (`MAX_GENERATIONS_QUEENS`, not `MAX_GENERATIONS`).

**P1-3. Default `P_MUTATION = 0.8` is well above the standard GA
range (the KNOB doc even says so) and risks Variant 1 failing to
converge on 8-Queens within MAX_GENERATIONS even after the bumps in
the recipe.**
- File: `ga_solution.py` line 245-260. The KNOB block itself
  acknowledges: *"classic GA literature recommends 0.01-0.1 for
  bitstrings; for tiny populations on the n-queens framing the slide
  default 0.8 is fine."* But the variants.md Variant 1 recipe does
  NOT touch P_MUTATION, and with 0.8 on 8-queens the GA destroys
  beneficial substructures every generation.
- Variant 1 acceptance allows "explain why it plateaued" as a
  fallback, so the gate **does not strictly fail** here. But an
  honest agent following the recipe verbatim will produce a
  fitness-not-0 result and call it a "success via explanation",
  which is a weaker proof of variant adaptability than the variant
  intends.
- **Suggested fix:** Either lower the default `P_MUTATION` (0.1 is
  the safer textbook choice) and update KNOB doc, OR amend Variant
  1's recipe in `variants.md` to also suggest lowering `P_MUTATION`
  to ~0.1 for the 8-queens run. The former is a code change with
  ripple effect; the latter is a one-line variant edit.

**P1-4. `RANDOM_SEED` mechanic is single-shot per process — Variant 2
cannot get truly apples-to-apples runs without two separate Python
invocations.**
- `ga_solution.py` lines 130 + 618-619: `random.seed(RANDOM_SEED)` is
  called once at the top of `main()`. Variant 2 asks for "Run A
  (mutation 0.01)" and "Run B (mutation 0.5)" comparison. In one
  process, the seed only re-applies if the user re-runs the script
  (changing `P_MUTATION` between runs). The variants.md does not
  spell this out; an exam agent that imports the module twice and
  flips `P_MUTATION` between runs will get diverged RNG state.
- **Suggested fix:** Either (a) make `RANDOM_SEED` re-apply at the
  start of each demo function (`_run_queens_demo` and
  `_run_number_demo`), or (b) explicitly document in Variant 2 in
  `variants.md` that each run is a separate Python invocation.
  Option (a) is cleaner and a 2-line edit.

**P1-5. Variant 3's "Acceptance" criterion in `variants.md` mentions
`n*(n-1)/2 = 6 for n=4` — the same KNOB block in the solution gives
the same formula, but uses **integer division** (`//`) where the
variant uses arithmetic division (`/`).**
- `ga_solution.py` line 240-243 (the `MINIMAL_FITNESS_QUEENS` KNOB
  block): *"For the 'positive' variant it should be
  `N_QUEENS*(N_QUEENS-1)/2`"* and lower down *"bump to
  `N_QUEENS*(N_QUEENS-1)//2`"*. The first uses `/` (returns float),
  the second uses `//` (returns int). An exam agent that copies the
  first form will set `MINIMAL_FITNESS_QUEENS = 3.0` (float), then
  the `>=` comparison still works because the positive-fitness
  function returns an int — but it's a stylistic split inside the
  same KNOB and shows the doc was not proofread.
- **Suggested fix:** Make both forms `//` (integer division). The
  type alias on the KNOB itself is `float`, so either form is fine
  at runtime, but pick one and stick to it.

**P1-6. `Number_solution.py` HOW-TO-ADAPT item 4 says "(1,1,1) is
absent from it by design" but does not name that this is the slide-5
seed set.**
- File: `Number_solution.py` lines 61-66 + 145-150. The slide-11
  acceptance ("perfect individual not in initial population") is
  guarded by leaving `NUMBER_USE_HARDCODED_POPULATION = True` and the
  hand-coded seed. This is correct but fragile: an exam agent that
  flips that knob to `False` to "get more diversity" loses the
  guarantee. The KNOB block should explicitly note the dependency
  between `NUMBER_TARGET = 4` and
  `NUMBER_USE_HARDCODED_POPULATION = True`.
- **Suggested fix:** Add one bullet to the `NUMBER_TARGET` KNOB doc
  block saying "If you set this to a target *that the random init
  could accidentally hit*, also force
  `NUMBER_USE_HARDCODED_POPULATION = True`."

**P1-7. No KNOB exists for switching the queens-fitness module from
the 1-based gene representation (rows in [1, n]) to a 0-based one,
even though the lab handout slide 13 explicitly says "Remember in
Python list indices start from 0."**
- `Queen_solution.py` line 302 hard-codes `random.randint(1, n_queens)`
  with a `# WHY randint(1, n)` justification. A variant of the form
  "switch to 0-based rows" (which is a plausible adaptation for a
  printed-board view) cannot be answered without code edits. This is
  out-of-scope for the three mandatory variants but worth noting:
  the lab's own slide 13 footnote uses 0-based, the solution uses
  1-based. Mild adaptability gap.
- **Suggested fix:** Add a `QUEENS_ROW_BASE: int = 1` KNOB or
  acknowledge in the header that the choice is cosmetic and that
  changing it requires only the two lines in `create_random` and the
  doc-comment of `Board.__init__`.

---

### P2 findings (polish / nice-to-have)

**P2-1.** The `CROSSOVER_RATE` KNOB in `ga_solution.py` (lines 262-274)
is documented but not exercised by any variant in `variants.md`. Extra
surface area an exam agent may waste time on. Either delete it (and
hard-code crossover-always) or add an optional variant that exercises
it.

**P2-2.** The `QUEENS_CROSSOVER_RETURN_CHILD` KNOB (lines 170-187 of
`Queen_solution.py`) defaults to `"random"`, which makes Variant 2's
"compare two runs deterministically" harder even with `RANDOM_SEED`
pinned — flipping a coin per call burns extra RNG state. For
seed-pinned variants the deterministic options (`"left"` /
`"right"`) would yield cleaner reproduction. Worth a one-line note in
the KNOB doc telling exam agents to use `"left"` when pairing with
`RANDOM_SEED`.

**P2-3.** Header docstring of `ga_solution.py` lines 60-74 enumerates
the three exam variants with their KNOB recipes verbatim. This is
extremely friendly to an exam agent — possibly too friendly. The
spec (§8.2) implies the variants are graded on *adaptation skill*,
not *recipe recall*. Recommend reframing this section as "principles
of adapting the solver" rather than a literal variant-by-variant
recipe. (Sub-style: a reviewer might call this *teaching to the
test*.)

**P2-4.** `_run_queens_demo` (lines 585-613 of `ga_solution.py`) does
not honour a `MINIMAL_FITNESS_QUEENS = None` "auto-pick" the way
`_run_number_demo` does for `MINIMAL_FITNESS_NUMBER`. Variant 3
needs the user to set `MINIMAL_FITNESS_QUEENS` to `n*(n-1)/2` by
hand. An auto-pick path
(`if MINIMAL_FITNESS_QUEENS is None and QUEENS_FITNESS_VARIANT ==
"positive": minimal = N_QUEENS * (N_QUEENS - 1) // 2`) would be
both safer and a stronger demonstration of "variant adaptability".

**P2-5.** Variant 1 acceptance text uses "`(no conflicts)` OR
explains via KNOB inspection why convergence plateaued". The KNOB
descriptions in `ga_solution.py` use the words *exploration*,
*premature convergence*, *near-random walk* — good. But the
`P_MUTATION` KNOB doc does not actually use *premature convergence*
verbatim; it only says "slowly or get trapped in local optima". For
an exam agent trying to grep the KNOB blocks for the exact words the
variant acceptance criteria use, this is a small lexical gap.

**P2-6.** `queens_fitness_solution.py` ships a `_smoke_test` for the
slide-14 boards (`(5,6,2,3,5,8,6,1)` and `(7,3,6,6,4,6,8,1)`) that
asserts they score `-6` and `-7` respectively per the slide. But
running the smoke test is an `__main__` printout — no `assert`. Not
a defect for variant adaptability but a missed sanity-check
opportunity. Worth one assert.

---

### QA Checklist (§7-equivalent) — variant adaptability

| Variant | Allowed-surface adaptable? | Notes |
|---|---|---|
| Variant 1 — 8-Queens scaling | Yes (with caveats P1-2, P1-3) | KNOBs `N_QUEENS`, `MAX_GENERATIONS_QUEENS`, `POPULATION_SIZE_QUEENS` are all named + documented in the header AND in their KNOB blocks. |
| Variant 2 — Mutation tuning | Yes (with caveat P1-4) | `P_MUTATION` KNOB doc explicitly names this variant. `RANDOM_SEED` mechanic is single-shot — fine for the gate, suboptimal for in-process A/B. |
| Variant 3 — Positive fitness | Yes (with caveat P1-5) | Cross-file KNOB pair `QUEENS_FITNESS_VARIANT` + `MINIMAL_FITNESS_QUEENS` correctly cross-referenced in both files' KNOB blocks. |
| Optional 4a — larger pop, 8-queens | Yes | Same KNOBs as Variant 1. |
| Optional 4b — population trimming | Partial — name mismatch P1-1 | `variants.md` says `TRIM_POPULATION`, solution says `SHOULD_TRIM_POPULATION`. |
| Optional 4c — 5-bit Number | Yes | `NUMBER_GENE_LENGTH`, `MINIMAL_FITNESS_NUMBER` documented; `MAX_GENERATIONS_NUMBER` KNOB doc explicitly mentions "5-bit may need ~60". |

### Acceptance criteria — mandatory variants

- Variant 1 acceptance ("gene tuple length 8 with fitness 0, OR
  explain via KNOB inspection why it plateaued"): **Met** with
  fallback. Direct convergence requires bumping `P_MUTATION` lower
  than the variant recipe says (see P1-3).
- Variant 2 acceptance ("two best-fitness numbers + sentence using
  vocabulary 'exploration', 'premature convergence', 'near-random
  walk'"): **Met**. Note P2-5: "premature convergence" not used
  verbatim in `P_MUTATION` KNOB doc, only its synonym "trapped in
  local optima". Minor lexical gap, vocab is recoverable from
  ga_solution header.
- Variant 3 acceptance ("concrete gene tuple, positive fitness,
  sentence linking to `n*(n-1)/2`"): **Met**. The
  `MINIMAL_FITNESS_QUEENS` KNOB doc spells the formula explicitly.

### DOCUMENT.md audit

N/A — this is a lab solution dir, not a project feature ship. No
DOCUMENT.md is required by the variants spec. (If the PM's
overarching convention demands DOCUMENT.md in `handout_lab_4/`, that's
a separate review thread.)

### Out-of-scope observations

- The negative-fitness `fitness_fn_negative` is the only place where
  `dy == 0` (same row) is checked first; for boards with both
  same-row AND same-diagonal it counts only once (the `if … or …`
  short-circuits). Slide 14 expects this. Correct.
- `fitness_fn_positive` is derived as `total_pairs - conflicts`
  instead of re-iterating — the inline comment correctly flags that
  the slide-shipped template had a "buggy double-counting" version
  and this solution fixed it. Out of variants' scope, but worth
  remembering: an exam agent that *re-derives* `fitness_fn_positive`
  by iterating pairs may rediscover the same bug.
- `genetic_algorithm` returns `Individual | None` but only `None` if
  the input population is empty. The KNOB doc never mentions an
  empty-population path. Out-of-scope but a tiny robustness check.

### Concerns / risks

1. The biggest risk is **doc rot**: between `variants.md` and the
   four `*_solution.py` headers there are at least three name/value
   mismatches (P1-1, P1-2, P0-2). For a gate that depends on
   "variant agents reach SOLVED using only documented surface",
   even one mismatch is enough to fail.
2. The `P_MUTATION = 0.8` default is a *latent failure mode*. The
   gate will pass when an exam agent invokes the "or explains why
   it plateaued" fallback, but a strict grader could read that as
   not-actually-solved.
3. There is **no automated unit test** that asserts the variant
   recipes (in `variants.md`) actually produce expected outputs
   against the locked solution. The smoke_test in
   `queens_fitness_solution.py` is the closest thing and it does
   not assert. The whole gate is testing the docs, not the code —
   so the docs need a self-test.
4. Variant 1's recipe + the default `P_MUTATION` interact badly.
   This is a *system-level* risk: the variant text, the KNOB
   defaults, and the header HOW-TO-ADAPT recipe each look fine in
   isolation but together produce a brittle gate.

### What PM should do next

1. **Fix P0-1 immediately** — the `column_weight` reference in
   `queens_fitness_solution.py` header is a literal bug-in-docs that
   any agent following the docs will hit. Delegate to
   `pm-backend` (or whichever owns the lab solution lockset) for a
   1-line header rewrite.
2. **Fix P0-2** — either delete the "Appendix B variant 3" reference
   in `Queen_solution.py` header item 5, or add a real Appendix B
   to `variants.md`. One or the other; not both nor neither.
3. **Fix P1-1** — pick a single name (`SHOULD_TRIM_POPULATION` is
   fine; rename the variants.md optional 4b to match). One-line
   edit in `variants.md`.
4. **Fix P1-2** — update `variants.md` Variant 1's expected-change
   paragraph to use the correct default (`MAX_GENERATIONS_QUEENS =
   100`) and reference the KNOB by its full name.
5. **Re-run the gate** (three variants in parallel) after the above
   four edits land. P1-3 through P1-7 and all P2s can be
   addressed in round-2 or later.
6. **Long-term**: add an actual variant-runner test
   (`pytest test_variants.py`) that imports the solution with each
   variant's KNOB settings injected and asserts the expected
   acceptance output. Without this the gate is testing the docs by
   eye, which is exactly the kind of thing that decays.

**DOCUMENT.md updated:** N/A for QA.
