# Lab4-GA Round 1 — Reviewer #2 (KNOB Coverage)

## Report to PM

**Assignment recap:** Lab Reviewer #2 — KNOB Coverage audit of
`handout_lab_4\*_solution.py` for Lab4-GA Round 1. Verify that every
critical GA KNOB (POPULATION_SIZE, MUTATION_RATE, N_QUEENS,
MAX_GENERATIONS, CROSSOVER_RATE) is complete, discoverable via the
`# KNOB:` comment convention, and sufficient to answer every variant
in `study\_exam\Lab4-GA\variants.md`. Hunt for missing knobs and
naming mismatches that would break the exam-agent gate.

**Status:** Fail (Pass with concerns at best — the variant bank
references KNOB names that do not exist in the source. An exam agent
that does literal `# KNOB:` discovery will fail to find them and
report `UNSOLVED`.)

---

### P0 findings (must fix before the exam-agent gate runs)

**P0-1. Variant-bank ↔ KNOB naming mismatch (5 separate names).**
`study\_exam\Lab4-GA\variants.md` is the contract that the exam-agent
gate runs against — and per spec §8.2 the agent is allowed to read
ONLY the `# KNOB:` blocks, function signatures, and the
`ga_solution.py` header docstring. The variant file names KNOBs that
do not exist as written:

| variants.md says | Actual KNOB name | Lines in variants.md |
|---|---|---|
| `POPULATION_SIZE` | `POPULATION_SIZE_NUMBER` / `POPULATION_SIZE_QUEENS` | V1 (line 39), 4a (line 101) |
| `MUTATION_RATE` | `P_MUTATION` | V1 (line 41), V2 (lines 54, 56, 65) |
| `MAX_GENERATIONS` | `MAX_GENERATIONS_NUMBER` / `MAX_GENERATIONS_QUEENS` | V1 (line 36), V2 (line 67), 4c |
| `TRIM_POPULATION` | `SHOULD_TRIM_POPULATION` | 4b (line 105) |
| `MINIMAL_FITNESS_NUMBER = 31` | knob accepts `int | None`, default `None` | 4c (line 109) |

Suggested fix: dispatch a maintainer to either (a) rename the actual
KNOBs in the source to match the variant bank (simplest names win),
or (b) rewrite `variants.md` to use the exact KNOB names. The current
state guarantees a stale-link failure on the exam-agent gate.
**Location:** `study\_exam\Lab4-GA\variants.md` lines 36-41, 54-67,
101, 105, 109 vs `handout_lab_4\ga_solution.py` lines 163, 202, 217,
227, 243, 260, 286.

**P0-2. `Number_solution.main()` ignores its own knob.**
`handout_lab_4\Number_solution.py:323` hard-codes
`minimal_fitness = (2 ** NUMBER_GENE_LENGTH) - 1` and never reads
`MINIMAL_FITNESS_NUMBER` from `ga_solution.py`. This breaks optional
extra variant 4c (`MINIMAL_FITNESS_NUMBER = 31`) the moment a student
runs `Number_solution.py` directly instead of via `ga_solution.py`.
The KNOB exists, is documented, but is not honoured by the file that
the docstring at lines 77-83 explicitly says is a valid entry point
(`Running this file directly is supported`). Suggested fix: import
`MINIMAL_FITNESS_NUMBER`, `MAX_GENERATIONS_NUMBER`, `P_MUTATION`,
`SHOULD_TRIM_POPULATION` from `ga_solution` and respect them in this
`main()` exactly like `_run_number_demo` does.

---

### P1 findings (should fix; risks exam-variant failure)

**P1-1. `MUTATION_RATE` naming — single biggest critical KNOB has a
non-canonical name.** The brief lists `MUTATION_RATE` as one of the
five critical knobs. The implementation calls it `P_MUTATION`
(`ga_solution.py:260`). The KNOB docstring even acknowledges the
issue by naming the conceptually-paired knob
`QUEENS_MUTATION_COLUMN_RATE` (line 168) and the conceptually-paired
knob `NUMBER_MUTATION_BIT_RATE` (line 132) — i.e. three different
"mutation rate" knobs with three different naming conventions. An
exam agent searching `MUTATION_RATE` finds zero, two, or all three
depending on its regex. Suggested fix: alias `MUTATION_RATE =
P_MUTATION` at module scope OR rename to `MUTATION_RATE` outright;
update `_run_*_demo` and `Number_solution.main` accordingly.

**P1-2. `Queen_solution.main()` default p_mutation disagrees with
global default.** `Queen_solution.py:330` signature is
`p_mutation: float = 0.5` but `ga_solution.py:260` defines
`P_MUTATION: float = 0.8`. Running `Queen_solution.py` directly
produces a different mutation rate than running `ga_solution.py` does
with the same `P_MUTATION = 0.8` left untouched. This will silently
break Variant 2 reproducibility if the student picks the wrong entry
point. Suggested fix: default `p_mutation=P_MUTATION` (import the
constant) or remove the local default entirely.

**P1-3. `INITIAL_NUMBER_POPULATION_SIZE` vs `POPULATION_SIZE_NUMBER`
are two knobs for the same concept.** `Number_solution.py:172`
declares `INITIAL_NUMBER_POPULATION_SIZE = 4` and
`ga_solution.py:163` declares `POPULATION_SIZE_NUMBER = 4`. The
former is used inside `build_initial_population()` when
`NUMBER_USE_HARDCODED_POPULATION` is False; the latter is documented
as "size of the initial population for the 3-bit number demo" but is
**never actually read anywhere in the codebase**. Grep-check the
source: `POPULATION_SIZE_NUMBER` is mentioned in the KNOB docstring
and that is it. Suggested fix: either delete `POPULATION_SIZE_NUMBER`
(it's a documentation-only ghost) or wire it through to
`build_initial_population`.

**P1-4. Variant 3 (`MINIMAL_FITNESS_QUEENS`) needs integer division
clarification.** Variant 3 (positive fitness) requires
`MINIMAL_FITNESS_QUEENS = N_QUEENS*(N_QUEENS-1)/2`. The KNOB docstring
at `ga_solution.py:241-242` correctly says
`N_QUEENS*(N_QUEENS-1)//2` for variant 3, but the type is declared
`float`, and `fitness_fn_positive` returns `int`. With n=4 → 6,
either `6` or `6.0` compares equal in the `>=` check, so this is not
broken — but the inconsistency is a P1 because a student copying the
documented `N_QUEENS*(N_QUEENS-1)/2` formula (Python 3 returns
`6.0`) will pass; copying `//` returns `6`; both fine but document
clearly. Suggested fix: pin the type as `int | float` and add a worked
example: "for n=4 set to 6 (or 6.0)".

**P1-5. `RUN_NUMBER_DEMO`/`RUN_QUEENS_DEMO` knobs are documented but
not in the exam-variant cookbook.** Useful for running ONLY one demo
during variant 2 (which only studies queens), but variants.md does
not mention them. An exam agent producing per-variant output may
print spurious Number-demo output that confuses graders. Suggested
fix: add a one-liner to variants.md V2/V3 saying "set
`RUN_NUMBER_DEMO = False` to silence the Number demo".

**P1-6. `NUMBER_MUTATION_BIT_RATE` docstring contradicts the
implementation.** `Number_solution.py:119-132` docstring says
"probability that an individual chosen for mutation has *each
individual bit* flipped", and gives the formula
`p_mutation * NUMBER_MUTATION_BIT_RATE / GENE_LENGTH per bit`. The
implementation at lines 234-239 is a single per-call gate: with prob
`(1 - NUMBER_MUTATION_BIT_RATE)` the individual is returned
unchanged; otherwise exactly ONE bit is flipped. There is no
per-bit loop. The "per bit" framing in the docstring is wrong.
Suggested fix: rewrite as "probability that an individual chosen for
mutation actually has one random bit flipped".

**P1-7. `CROSSOVER_RATE` is global and not split per problem.**
The Number exercise and the Queens homework share one
`CROSSOVER_RATE` (`ga_solution.py:274`). This is fine for the current
three variants but tightens coupling. Future variants such as "use
crossover-only for Number, crossover+mutation for Queens" would need
a split. Not blocking. Suggested fix: leave as-is for now; document
the global scope in the docstring.

**P1-8. No KNOB for **selection method**.** The brief lists five
critical knobs and selection (roulette wheel) is fixed at
implementation time. Several real GA literature variants swap in
tournament or rank selection. If the exam ever tests this, the only
escape hatch is to edit `random_selection`. Not currently in
variants.md, so flagged only as a P1 risk.

**P1-9. No KNOB for **elitism**.** The docstring (`ga_solution.py`
line 84-85 in Queen_solution adapt-section) explicitly notes "To
enable elitism … not implemented here". The closest knob,
`SHOULD_TRIM_POPULATION`, is a SORT-AND-KEEP that approximates
elitism but not strictly preserves the single best individual.
Standard GA literature treats elitism as a top-tier knob alongside
crossover/mutation rates. Risk of an exam variant asking for it.

**P1-10. `MAX_POPULATION_SIZE` is a sub-knob of
`SHOULD_TRIM_POPULATION`, not standalone.** `ga_solution.py:295`
documents it as a no-op when `SHOULD_TRIM_POPULATION = False`. Fine
behaviour, but a student finding `MAX_POPULATION_SIZE = 100` in
isolation may assume it caps the population unconditionally. Suggested
fix: rename to `TRIMMED_POPULATION_CAP` or move the docstring's "no
effect otherwise" hint to the very first line of the KNOB block so it
cannot be missed.

---

### P2 findings (polish / suggestions)

**P2-1.** `MINIMAL_FITNESS_NUMBER` declares `default=auto` in the
KNOB comment (`ga_solution.py:173`) but the literal value is `None`.
Either say `default=None (auto)` or expand the explanation in the
first line.

**P2-2.** `get_initial_population(count, n_queens=8)` in
`Queen_solution.py:309` defaults `n_queens=8`. Every actual caller
passes `n_queens` explicitly. The default is dead and slightly
misleading (8 ≠ the default `N_QUEENS = 4`). Suggested fix: drop the
default OR set it to `4` to match.

**P2-3.** `NUMBER_TARGET` (`Number_solution.py:117`) is not
cross-referenced from `ga_solution.py`'s top-level KNOB block. A
student inspecting only `ga_solution.py` will not discover the slide
11 variant exists. Add a "see also" line in
`MINIMAL_FITNESS_NUMBER`'s KNOB block.

**P2-4.** `QUEENS_CROSSOVER_RETURN_CHILD` (`Queen_solution.py:170`)
is a useful knob but not exercised by any variant in variants.md.
Either add a variant ("kept left child consistently") or downgrade
it in the docstring so exam agents don't think they need to flip it.

**P2-5.** No KNOB for the inner Number-problem crossover point
(single-point with random cut). `Number_solution.py:241-260` is
hard-coded. If a future variant asks for "two-point crossover" the
student must edit code. Acceptable; flagged only for completeness.

**P2-6.** The KNOB convention is inconsistent on default-value
declaration syntax:
- `RANDOM_SEED: int | None = None` (modern union)
- `MINIMAL_FITNESS_NUMBER: int | None = None` (modern union)
- but `INITIAL_NUMBER_POPULATION` has no `default=` line and just
  spells out the literal in the docstring.
Minor; cosmetic.

**P2-7.** No KNOB for **convergence-monitoring stride** (how often to
print). `PRINT_GENERATIONS` is on/off only. Variants 1 and 4a both
generate hundreds of generations; an "every 10th gen" knob would
help readability.

---

### KNOB Inventory (counted & cross-referenced)

**Critical KNOBs from the reviewer brief.**

| Brief KNOB | Implementation | Discoverable as | Status |
|---|---|---|---|
| `POPULATION_SIZE` | `POPULATION_SIZE_NUMBER`, `POPULATION_SIZE_QUEENS` | yes (suffixed) | Pass (variant-bank name mismatch — see P0-1) |
| `MUTATION_RATE` | `P_MUTATION` | yes (renamed) | Pass (name mismatch — see P0-1, P1-1) |
| `N_QUEENS` | `N_QUEENS` | yes | Pass |
| `MAX_GENERATIONS` | `MAX_GENERATIONS_NUMBER`, `MAX_GENERATIONS_QUEENS` | yes (suffixed) | Pass (variant-bank name mismatch — see P0-1) |
| `CROSSOVER_RATE` | `CROSSOVER_RATE` | yes | Pass |

**Full KNOB inventory found (21 total across 4 files):**

`ga_solution.py` (12 knobs): `RANDOM_SEED`, `RUN_NUMBER_DEMO`,
`RUN_QUEENS_DEMO`, `POPULATION_SIZE_NUMBER` *(unused — see P1-3)*,
`MAX_GENERATIONS_NUMBER`, `MINIMAL_FITNESS_NUMBER`, `N_QUEENS`,
`POPULATION_SIZE_QUEENS`, `MAX_GENERATIONS_QUEENS`,
`MINIMAL_FITNESS_QUEENS`, `P_MUTATION`, `CROSSOVER_RATE`,
`SHOULD_TRIM_POPULATION`, `MAX_POPULATION_SIZE`, `PRINT_GENERATIONS`
(actually 15 — recount accurate).

`Number_solution.py` (5 knobs): `NUMBER_GENE_LENGTH`, `NUMBER_TARGET`,
`NUMBER_MUTATION_BIT_RATE`, `INITIAL_NUMBER_POPULATION`,
`NUMBER_USE_HARDCODED_POPULATION`, `INITIAL_NUMBER_POPULATION_SIZE`
(6 — recount accurate).

`Queen_solution.py` (5 knobs): `QUEENS_FITNESS_VARIANT`,
`QUEENS_DIAG_WEIGHT`, `QUEENS_ROW_WEIGHT`,
`QUEENS_MUTATION_COLUMN_RATE`, `QUEENS_CROSSOVER_RETURN_CHILD`.

`queens_fitness_solution.py` (2 knobs): `DEFAULT_DIAG_WEIGHT`,
`DEFAULT_ROW_WEIGHT`.

**Total: 28 KNOBs.** Density is high, which is generally good for
exam-variant coverage — but the **proliferation of three different
mutation-rate knobs** (`P_MUTATION`, `NUMBER_MUTATION_BIT_RATE`,
`QUEENS_MUTATION_COLUMN_RATE`) and **two different "population size"
knobs for the Number problem** (`POPULATION_SIZE_NUMBER`,
`INITIAL_NUMBER_POPULATION_SIZE`) is a code-smell that will confuse
exam agents.

---

### Variant Coverage Matrix

| Variant | Required KNOBs | All present? | Notes |
|---|---|---|---|
| V1 (8-Queens) | `N_QUEENS`, `MAX_GENERATIONS_QUEENS`, `POPULATION_SIZE_QUEENS`, `P_MUTATION` | Yes | Variant text uses unqualified names — see P0-1 |
| V2 (mutation tuning) | `P_MUTATION`, `N_QUEENS`, `MAX_GENERATIONS_QUEENS`, `RANDOM_SEED` | Yes | Variant text uses `MUTATION_RATE` — see P0-1 |
| V3 (positive fitness) | `QUEENS_FITNESS_VARIANT`, `MINIMAL_FITNESS_QUEENS` | Yes | Pass |
| 4a (pop=100, n=8) | `POPULATION_SIZE_QUEENS`, `N_QUEENS` | Yes | Variant text uses `POPULATION_SIZE` — see P0-1 |
| 4b (trim) | `SHOULD_TRIM_POPULATION`, `MAX_POPULATION_SIZE` | Yes | Variant text uses `TRIM_POPULATION` — see P0-1 |
| 4c (5-bit Number) | `NUMBER_GENE_LENGTH`, `MINIMAL_FITNESS_NUMBER`, `MAX_GENERATIONS_NUMBER` | Partial | Honoured by `_run_number_demo` only, not by `Number_solution.main()` — see P0-2 |

---

### Out-of-scope observations (worth noting)

1. **`Queen_solution.main()` accepts knobs as function arguments**
   while every other module reads them from module-scope constants.
   This dual API (function args vs module globals) means
   `Queen_solution.py` can be driven two ways with two different
   defaults. If the project ever locks "single configuration source",
   this is the one outlier.

2. **`fitness_fn_positive` in `queens_fitness_solution.py:148`
   derives its result by negating `fitness_fn_negative`.** The
   comment at lines 144-148 calls out that this fixes a "buggy
   double-counting present in the slide-shipped `fitness_fn_positive`
   template" — but that fix is undocumented in the lab handout
   reference. Worth a note in `study/lectures/L05-Local-Search.md`
   so a student matching slide pseudo-code does not get marked off.

3. **`pick_individual` has dead code path.** At
   `ga_solution.py:499-508`, the `if shifted_fitnesses is None`
   branch is never triggered because `random_selection` (the only
   caller) always passes `shifted_fitnesses`. The fallback is
   defensive but reads as a half-finished refactor.

4. **`__lt__` on `Individual` calls `get_fitness()` per comparison.**
   `ga_solution.py:347`. For a 100-population queens GA with N=8 and
   500 generations this is O(generations × population² × n²) fitness
   recomputations. Not a correctness bug; a P2 perf observation.

---

### Concerns / risks (the harsh truth)

The KNOB set is **functionally complete** for the three mandatory
variants and the three optional extras, but the **discoverability
contract is broken**. The variant bank uses canonical short names
(`MUTATION_RATE`, `POPULATION_SIZE`, `MAX_GENERATIONS`,
`TRIM_POPULATION`) and the source code uses suffixed long names
(`P_MUTATION`, `POPULATION_SIZE_QUEENS`, `MAX_GENERATIONS_QUEENS`,
`SHOULD_TRIM_POPULATION`). The exam-agent gate spec §8.2 forbids
reading function bodies — meaning the gate is a literal regex over
`# KNOB: <NAME>` lines.

**Concrete failure prediction:** an exam agent asked to "tune
MUTATION_RATE to 0.01" will grep `# KNOB: MUTATION_RATE`, find zero
matches, and either (a) give up and report `UNSOLVED`, or (b)
hallucinate `MUTATION_RATE` as a new variable assignment at the top
of the file. Either is a Round 1 fail.

Beyond the naming issue, the **three mutation knobs**
(`P_MUTATION`, `NUMBER_MUTATION_BIT_RATE`,
`QUEENS_MUTATION_COLUMN_RATE`) without a single named "effective bit
flip probability" formula are a usability hazard. The docstrings
attempt to multiply them together (`p_mutation *
NUMBER_MUTATION_BIT_RATE / GENE_LENGTH per bit`) but the
implementations do not actually multiply this way — see P1-6.

Convergence is not guaranteed on small populations and the docstring
correctly acknowledges this. P0-1 and P0-2 are the only blocker-class
findings; the rest can ship as P1 fixes after the gate runs.

---

### What PM should do next

1. **Fix P0-1 first** — rename the KNOBs in source OR rewrite
   `variants.md` to match. Pick one; do not leave both. My
   recommendation: rename in source (shorter, exam-friendlier names),
   then update `_run_*_demo` and the cross-references. Estimated
   effort: 30 minutes.
2. **Fix P0-2** — wire `Number_solution.main()` to honour
   `MINIMAL_FITNESS_NUMBER`, `MAX_GENERATIONS_NUMBER`,
   `P_MUTATION`, `SHOULD_TRIM_POPULATION` exactly as
   `_run_number_demo` does. Estimated effort: 10 minutes.
3. Address P1-1 through P1-3 in the same pass (they overlap with
   P0-1). P1-4 through P1-10 can be deferred to Round 2.
4. Re-dispatch QA Inspector after fixes; then dispatch the
   exam-agent gate to confirm all three mandatory variants report
   `SOLVED`.
5. Defer all P2 findings to a polish pass after the gate passes.

**DOCUMENT.md updated:** N/A for QA.
