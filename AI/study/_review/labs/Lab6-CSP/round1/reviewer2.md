# Lab 6 — CSP Round 1 — Reviewer #2 (KNOB Coverage)

**Reviewer role:** KNOB coverage and exam-variant adaptability — "can a fresh agent answer every variant in `study/_exam/Lab6-CSP/variants.md` by *only* flipping documented KNOBs?"
**Files reviewed:**
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\constraints_template_solution.py` (739 lines)
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\Colors_solution.py` (75 lines)
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\States_solution.py` (102 lines)

**Variant bank cross-checked:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab6-CSP\variants.md` (Variants 1–5).

**Source PDF:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\Lab 6.pdf` (5 slides — Exercise 1 base, Exercise 2 South America 4-colour, Homework Challenge FC + AC-3).

---

## VERDICT

**PASS WITH CONCERNS** — the solution exposes seven well-documented KNOBs (`MAP_NAME`, `ACTIVE_COLORS`, `USE_MRV`, `USE_DEGREE_TIEBREAK`, `USE_LCV`, `USE_FORWARD_CHECK`, `DISTANCE_THRESHOLD`) and they correctly drive Variants 1–4 with no source edits. Each KNOB carries the prescribed header block (default / range / what / effect / variants), and the runtime trace I ran (Australia default, SA + MRV + degree, SA 3-colour infeasibility, distance_demo at three thresholds, SA + FC) all produced the **expected answer shape** from variants.md. However: **(a)** Variant 5 (AC-3 pre-pass) is *exposed via the public method* `CSP.ac3()` but **NOT controllable via any module-level KNOB**, so a fresh agent reading only KNOB blocks and signatures cannot trigger it without writing a driver script — a documentation gap the variant bank explicitly anticipates ("Call `csp.ac3()` BEFORE `csp.backtracking_search()` in a tiny test script"), but no `USE_AC3` KNOB exists. **(b)** Multiple KNOBs live as **module-level globals** that the solver reads at call time, which means importing the module and mutating attributes works, but a re-import does **not** reset state — there is no documented "reset-between-runs" idiom and no per-instance override. **(c)** `DISTANCE_THRESHOLD` is consumed exclusively inside `create_distance_csp()` at build time; mutating it AFTER `create_csp()` has been called has no effect. The KNOB header does not flag this build-vs-run-time distinction. None of this is shipping-blocking, but the gaps should be closed before round 2 because exam variant 5 cannot be answered KNOB-only as the variant bank promises.

---

## P0 FINDINGS (KNOB coverage — blocks variant answers)

**None.** Variants 1–4 are each answerable by setting only the documented KNOBs at the top of `constraints_template_solution.py`. I verified each by direct execution (see EVIDENCE below). The default Australia 3-colour run reproduces the original lab output. Exercise 2 (SA + 4 colours) works. Forward checking + MRV monotonically reduces backtracks as the variant predicts.

---

## P1 FINDINGS (KNOB coverage — important)

### P1-1. Variant 5 ("AC-3 pre-pass") has NO controlling KNOB — variant cannot be answered KNOB-only

**Location:** `lab6\constraints_template_solution.py` lines 482–527 (`CSP.ac3` and `_revise` methods) and the KNOB block at lines 152–233.

**Claim in variant bank:** `study\_exam\Lab6-CSP\variants.md` lines 136–158 (Variant 5) states the variant should be answered using `csp.ac3()` as a pre-flight check. The variants.md preamble (lines 4–15) commits that **every** variant is answerable by reading "the docstring header", "every `# KNOB:` block", and "the public function/class signatures" — *nothing else*.

**Problem:** `ac3()` is exposed as a public method but there is **no** `USE_AC3` (or `RUN_AC3_FIRST`) KNOB at module scope. The entry-point harness (`if __name__ == "__main__":`, lines 729–735) calls only `create_csp()` and `backtracking_search()`. So an agent following the variant bank's contract — flip KNOBs, don't write code — cannot make the script perform the AC-3 pre-pass. The variant bank concedes this gap in line 151 ("Call `csp.ac3()` BEFORE `csp.backtracking_search()` in a tiny test script"), i.e. requires writing a driver script. That **violates the variant-bank preamble's KNOB-only contract**.

**Severity:** P1 — the implementation is there, but the KNOB surface area is incomplete. A fresh agent reading only the KNOB list will miss Variant 5 entirely (there is no `# KNOB: USE_AC3` to draw their attention to AC-3's existence; only the docstring header at line 26 mentions "Homework Challenge: arc consistency" in passing).

**Suggested fix:**

1. Add a `USE_AC3: bool = False` KNOB to the top-of-file KNOB block, with the standard header (default / range / what / effect / variants → cite Variant 5).
2. In the entry-point harness (or in `backtracking_search`), gate `csp.ac3()` on `USE_AC3` and run it before the search. Print whether AC-3 reduced any domains so the variant's expected-answer shape ("AC-3 does NOT detect infeasibility on its own for the 3-colour South America case") can be observed from console output.
3. Optionally add `USE_AC3_DURING_SEARCH` for the maintain-arc-consistency-during-search (MAC) variant, but that is out of scope for Variant 5.

---

### P1-2. KNOBs are module globals; no documented reset / no per-instance override; `_recursive_calls` / `_backtracks` survive across runs

**Location:** `lab6\constraints_template_solution.py` lines 166, 179, 192, 202, 212, 223, 233 (the seven module-level KNOB declarations) and lines 265–266, 275–276 (instance counters reset inside `backtracking_search`).

**Problem:** All KNOBs are *module globals*, read at call time by `select_unassigned_variable` / `order_domain_values` / `recursive_backtracking` / `_forward_check` etc. This means:

- A driver script that wants to compare configurations (Variant 4 explicitly does this: baseline → MRV+degree → MRV+degree+FC) must mutate `m.USE_MRV = True; m.USE_DEGREE_TIEBREAK = True; m.USE_FORWARD_CHECK = True` between runs. The KNOB header blocks do **not** document this pattern. A reader who skims only the KNOB block sees `USE_MRV: bool = False` and reasonably assumes "I should pass `use_mrv=True` to the constructor", or "I should subclass `CSP`", or "I should re-import the module". None of those work.
- There is **no constructor parameter** or `with`-block for any KNOB. The KNOB header does not say "this knob is read at call time from the module global; mutate the attribute before calling `backtracking_search()`".
- `csp._recursive_calls` and `csp._backtracks` ARE reset inside `backtracking_search` (lines 275–276) — good. But the `domains` dictionary, when `USE_FORWARD_CHECK` is on, is mutated in place AND restored on backtrack snapshot-by-snapshot (`_forward_check` / `_restore_domains`, lines 445–479). If `backtracking_search` ever returned mid-search (e.g. via an external interrupt or a future failure mode), `self.domains` could be left in a pruned state. The KNOB block does not warn callers about this.

**Severity:** P1 — Variant 2 ("compare 5-colour vs 3-colour backtrack counts") and Variant 4 (compare three heuristic configurations) both **require running the solver more than once** in the same Python process. Without a documented reset idiom, a fresh agent will get burned by stale state (e.g. mutating `ACTIVE_COLORS` mid-life will not retroactively shrink `domains`, because `domains` were built when `create_csp()` was called — see P1-3).

**Suggested fix:**

1. Add a short "Usage pattern" section to the file's docstring header showing the canonical driver script for Variant 4: `for cfg in configs: m.USE_MRV, m.USE_DEGREE_TIEBREAK, m.USE_FORWARD_CHECK = cfg; csp = m.create_csp(); m._print_report(csp, csp.backtracking_search())`. Include the *invariant* that `create_csp()` must be called AFTER setting `MAP_NAME`, `ACTIVE_COLORS`, and `DISTANCE_THRESHOLD`, but `USE_*` heuristic knobs may be flipped at any time before `backtracking_search()`.
2. Strongly consider promoting the knobs to constructor parameters (`CSP(..., use_mrv=USE_MRV, use_lcv=USE_LCV, ...)`) so the call-time-read behaviour becomes explicit. This is a bigger refactor; the minimum fix is documentation.
3. In each KNOB block, add a one-line "Read at: import / `create_csp()` / `backtracking_search()`" tag so the build-vs-run-time distinction is mechanical.

---

### P1-3. `DISTANCE_THRESHOLD` is build-time-only; KNOB header omits this

**Location:** `lab6\constraints_template_solution.py` lines 225–233 (`DISTANCE_THRESHOLD` KNOB block) and line 679 (`create_distance_csp` consumes it).

**Problem:** `DISTANCE_THRESHOLD` is referenced *exactly once* (line 679: `if euclid(region_xy[vi], region_xy[vj]) <= DISTANCE_THRESHOLD`) — inside `create_distance_csp()`. This means the threshold is baked into the constraint graph at CSP-construction time. If a driver script does

```
m.DISTANCE_THRESHOLD = 1.5
csp = m.create_csp()
m.DISTANCE_THRESHOLD = 3.5
res = csp.backtracking_search()     # ← uses the 1.5 graph
```

the `3.5` mutation has zero effect. The KNOB block (lines 225–233) says only "Effect: large threshold -> dense graph -> harder problem" and "Exam variants: variant 3". It does NOT say "must be set before `create_csp()` is called".

Variant 3 in `variants.md` (lines 95–106) iterates threshold across `1.5 / 2.5 / 3.5` and asks for three reports. The natural way for a fresh agent to write that driver is the above (set, build, mutate, search, mutate, search) — which silently produces three identical results from the first build.

**Severity:** P1 — silent wrong behaviour. The script doesn't crash; it just returns the same answer three times. Hardest class of bug for a student to debug.

**Suggested fix:** In the `DISTANCE_THRESHOLD` KNOB block, prepend:

> **Read at:** `create_distance_csp()` call time. To change the threshold between runs, you must build a new CSP — set `DISTANCE_THRESHOLD`, then call `create_csp()` again. Mutating this KNOB *after* `create_csp()` has been called has no effect on an already-built CSP.

Same fix applies in principle to `MAP_NAME` and `ACTIVE_COLORS` (both also read at `create_csp()` time, never re-read), but those are less likely to bite because the variants that use them do not change them mid-process.

---

### P1-4. `Colors_solution.Color` enum exposes a "KNOB" header but the KNOB block describes the **module's palette membership**, not a single mutable knob

**Location:** `lab6\Colors_solution.py` lines 56–74.

**Problem:** The comment block at line 56 starts `# KNOB: COLOR palette membership (default = 5 members; ...)`. This is **not** a KNOB in the same sense as the others — `ACTIVE_COLORS` is the actual KNOB (it's described in *both* `Colors_solution.py` lines 56–69 *and* `constraints_template_solution.py` lines 168–179). The `Color` enum block looks like a KNOB header but is really a documentation reference to a KNOB that lives elsewhere.

The variants.md preamble (line 11) explicitly tells fresh agents to read "every `# KNOB:` block in that file *and* in `Colors_solution.py` / `States_solution.py`". So an agent will land on this block and look for a mutable knob to flip — and the answer is "you flip `ACTIVE_COLORS` in the *other* file". The cross-reference is in the prose at line 12 ("KNOB ``ACTIVE_COLORS`` in constraints_template_solution.py decides which subset"), but a tag like `# KNOB-REF: ACTIVE_COLORS lives in constraints_template_solution.py` would be more mechanical.

Similar (lesser) issue at `States_solution.py` line 64: `# KNOB: ADJACENT MEMBERS may be added here.` — this is a "future-extension hook" rather than a runtime knob; the wording invites confusion.

**Severity:** P1 — taxonomic confusion. Agents who use the variant-bank-promised KNOB-blocks-only contract will spend cycles deciding which block is "the" knob.

**Suggested fix:** Distinguish three categories with three prefixes:
- `# KNOB:` — a mutable module global the agent flips.
- `# KNOB-REF:` — a documentation reference pointing to the actual KNOB elsewhere.
- `# KNOB-EXT:` — an extension point (add an enum member, add a builder function) that requires source edits and is *outside* the KNOB-only variant contract.

Apply to `Colors_solution.py:56` (turn into `# KNOB-REF: ACTIVE_COLORS in constraints_template_solution.py controls which of these members become each variable's domain.`) and `States_solution.py:64` (turn into `# KNOB-EXT: ...`).

---

### P1-5. `USE_LCV` and `USE_FORWARD_CHECK` interact silently when both are on; KNOB blocks don't document the interaction

**Location:** `lab6\constraints_template_solution.py` lines 204–223 (`USE_LCV` and `USE_FORWARD_CHECK` KNOB blocks) and lines 373–379, 426–443 (`order_domain_values` + `_lcv_count`).

**Problem:** `_lcv_count` reads `self.domains[neighbour]` (line 433) to compute "how many neighbour-domain values does this candidate rule out?". When `USE_FORWARD_CHECK` is also on, `self.domains` is mutated in place by `_forward_check` and then restored on backtrack. So LCV sees a *pruned* domain when FC has fired earlier in the recursion. This is **a feature, not a bug** (LCV + FC together is the standard textbook combination), but the KNOB header for `USE_LCV` (lines 204–212) does not mention the interaction — it says only "improves the *first-found-solution* runtime".

A fresh agent who turns on both — Variant 4 doesn't, but a homework-extension variant might — will see LCV behave differently with FC than without, with no documentation of why. Two boolean knobs that interact non-trivially is exactly the case where a docstring co-mention is warranted.

**Severity:** P1 — undocumented interaction; not a bug, but a hidden coupling.

**Suggested fix:** Add to `USE_LCV` block:

> **Interaction with `USE_FORWARD_CHECK`:** When both are on, LCV computes its "neighbour values ruled out" count using each neighbour's *currently-pruned* live domain (the domain after upstream FC has already removed clashing colours). This is the standard textbook composition and tends to amplify FC's gains.

And the symmetric note in the `USE_FORWARD_CHECK` block.

---

## P2 FINDINGS (KNOB coverage — polish)

### P2-1. KNOB headers list "Exam variants" but use plain text, not a stable identifier

**Location:** all seven KNOB headers in `lab6\constraints_template_solution.py` lines 158–233.

The headers say e.g. "Exam variants: variant 1; leave off to demonstrate plain chronological backtracking". The variants in `variants.md` are numbered (Variant 1, Variant 2, ..., Variant 5) and named ("Replace the map ... + MRV"). A grep-stable cross-reference like "Exam variants: V1 (south_america + MRV + degree), V4 (homework FC)" would make round-trip discovery (KNOB ↔ variant) mechanical.

### P2-2. `MAP_NAME` allowed values listed in prose; no `Literal` type

**Location:** `lab6\constraints_template_solution.py` line 166 (`MAP_NAME: str = "australia"`).

The header documents the allowed set `{"australia", "south_america", "distance_demo"}` and the dispatch at line 695 raises on unknown values — good defensive code. But the type annotation is plain `str`. A `Literal["australia", "south_america", "distance_demo"]` annotation would let static type-checkers catch typos at edit time and make the allowed set machine-readable. Same for `ACTIVE_COLORS: List[Color]` (could be `List[Color]` with no constraint that the list is non-empty — `Optional`/runtime-check helpful but not type-checkable).

### P2-3. `USE_FORWARD_CHECK` and the test for the "fail-fast" loop interact with an empty-snapshot edge case (untested)

**Location:** `lab6\constraints_template_solution.py` lines 320–337.

When `USE_FORWARD_CHECK` is on but the assigned `variable` has no unassigned neighbours (e.g. Tasmania in Australia), `_forward_check` returns `({}, True)`. Then on backtrack we restore an empty snapshot (no-op) and the next value is tried — correct. There is no bug. But there is no comment showing the maintainer that the empty-snapshot case is intentional. A one-line `# (snapshot may be empty if no unassigned neighbours — that's fine; _restore_domains is a no-op)` near line 333 would help.

### P2-4. `ACTIVE_COLORS` allows duplicates silently

**Location:** `lab6\constraints_template_solution.py` line 179 (`ACTIVE_COLORS: List[Color] = [Color.Red, Color.Green, Color.Blue]`).

The type is `List[Color]` — duplicate entries are silently accepted (`[Red, Red, Blue]` would build domains `[Red, Red, Blue]` per variable, which is *functionally* fine but breaks the LCV count's denominator and inflates `_lcv_count`'s "ruled out" tally. No variant uses duplicates, but a fresh agent who mistypes will get weird counts. A `_dedupe_and_validate(ACTIVE_COLORS)` helper at `create_csp()` time would be safer; or stronger: change the type to a Set / FrozenSet. Minor.

### P2-5. No KNOB controls the print verbosity / output sink

**Location:** `lab6\constraints_template_solution.py` lines 706–726 (`_print_report`).

The harness always prints to `stdout`. For a driver script comparing five configurations (Variants 2 and 4), the printing-heavy harness clutters comparison output. A `VERBOSE: bool = True` KNOB (or a `report_to: TextIO` parameter to `_print_report`) would let driver scripts swap to a quiet collect-and-tabulate pattern. Nice-to-have; not blocking.

### P2-6. `States` enum mixes Australia (`WA, NT, Q, NSW, V, SA, T`) and South America (13 countries) members in the same class; no `# KNOB-EXT` for adding more

**Location:** `lab6\States_solution.py` lines 53–80.

The dual-map enum works because `States.WA.value = 1` and `States.COLOMBIA.value = 11` don't collide, and adjacency is declared in the entry point not the enum. But adding a third map (Variant 3 already does this by reusing the Australia members for the distance demo) is undocumented in the enum file — a fresh agent who wants to add e.g. "Iceland regions" (the variants.md preamble names this exact case in Variant 1's title) has to discover the convention by reading the comments. Not a bug; the `# KNOB-EXT: regions list / neighbours dict / builder function in constraints_template_solution.py` cross-reference suggested in P1-4 would close this.

### P2-7. `_lcv_count` reads `self.constraints[variable]` (per-variable constraint) but `is_consistent` iterates `self.constraints.values()` (every constraint, against every neighbour pair)

**Location:** `lab6\constraints_template_solution.py` lines 388–396 (`is_consistent`) vs lines 440 (`_lcv_count`).

Two slightly different code paths for what is morally the same predicate. For the not-equal map-colouring CSP this is harmless (all entries in the constraints dict are the same `constraint_function`), but it is an inconsistency that future maintainers will trip on. A future variant that uses *per-variable* constraints (e.g. "Brazil cannot be Red") would behave differently under LCV vs `is_consistent`. Not exercised by current variants; flag for hardening.

### P2-8. No KNOB documents the random-seed / determinism story

**Location:** `lab6\constraints_template_solution.py` line 37 (`# shuffle(all_values)` — commented out in template; the solution does not enable it either).

The template has `# shuffle(all_values)` left commented at line 37 of `constraints_template.py`. The solution does not enable randomisation, so output is deterministic (the variant bank assumes this — Variant 1 says "Brazil is the single highest-degree node ... so the degree tie-break forces it first"). But there is no `RANDOM_SEED` KNOB and no "Deterministic output: yes" docstring guarantee. A future variant that adds shuffling would need both. Nice-to-have.

### P2-9. KNOB headers don't follow a strict template; minor wording variation

**Location:** all seven KNOB blocks.

Some headers use "Effect:" + "Exam variants:"; some use "What it does:" + "Effect:" + "Exam variants:". `USE_MRV` (line 181) includes a "mental-model line" sub-bullet; others don't. Standardising to `# KNOB: <NAME> (default=..., range=...)` / `# What it does:` / `# Effect:` / `# Read at: <import|create_csp|search>` / `# Exam variants:` would aid grep-driven discovery. Minor.

---

## EVIDENCE — runtime checks

I ran the solver in five configurations against the expected-answer shapes in `variants.md` and confirmed the KNOB-only contract holds for Variants 1–4 (Variant 5 documented as P1-1):

| Variant | KNOBs flipped | Result | `_recursive_calls` | `_backtracks` | Matches expected shape? |
|---|---|---|---|---|---|
| Default (Australia 3-colour) | none | SOLVED — 7 regions coloured | 8 | 0 | Yes — original lab output |
| Exercise 2 (SA 4-colour) | `MAP_NAME='south_america'`, `ACTIVE_COLORS=4` | SOLVED — 13 regions | (see V1 run) | (see V1 run) | Yes |
| Variant 1 (SA + MRV + degree) | + `USE_MRV=True`, `USE_DEGREE_TIEBREAK=True` | SOLVED, Brazil = Red (highest-degree first) | 14 | 0 | Yes — Brazil's degree-10 dominates first pick |
| Variant 2 (SA 3-colour) | `ACTIVE_COLORS=[R,G,B]`, no heuristics | **NO SOLUTION** | 310 | 309 | Yes — infeasible as predicted by 4-colour theorem |
| Variant 3 (distance_demo, 3 colours) | `MAP_NAME='distance_demo'`, threshold ∈ {1.5, 2.5, 3.5} | 1.5 → OK (0 bt); 2.5 → OK (0 bt); 3.5 → NO SOLUTION (15 bt) | 6 / 6 / 16 | 0 / 0 / 15 | Yes — variants.md predicts "Run A & B succeed; Run C fails" exactly |
| Variant 4 (SA + FC, 4 colours) | + `USE_FORWARD_CHECK=True` | SOLVED, 0 backtracks | 14 | 0 | Yes — FC fail-fast prevents all dead-ends |

All variants ran by mutating only documented KNOBs at module scope (no source edits to `_solution.py` files). The "KNOB-only" contract holds end-to-end for Variants 1–4.

Variant 5 (AC-3 pre-pass) **cannot** be triggered by mutating any documented KNOB — see P1-1. It is reachable only by importing the module and calling `csp.ac3()` from a hand-written driver, which the variant bank acknowledges but which violates the variant-bank preamble's KNOB-only contract.

---

## KNOB INVENTORY — what's documented vs what exists

| Module-global | KNOB block present? | Read at | Drives which variant | Tested? |
|---|---|---|---|---|
| `MAP_NAME` | Yes (`constraints_template_solution.py:158`) | `create_csp()` build time | V1, V2, V3, V4, V5 | Yes |
| `ACTIVE_COLORS` | Yes (line 168) + reference in `Colors_solution.py:56` | `create_csp()` build time | V1, V2, V4, V5 | Yes |
| `USE_MRV` | Yes (line 181) | `select_unassigned_variable` call time | V1, V4 | Yes |
| `USE_DEGREE_TIEBREAK` | Yes (line 194) | `_select_mrv` call time | V1, V4 | Yes |
| `USE_LCV` | Yes (line 204) | `order_domain_values` call time | (none in current bank) | No (no variant exercises it) |
| `USE_FORWARD_CHECK` | Yes (line 214) | `recursive_backtracking` call time | V4 | Yes |
| `DISTANCE_THRESHOLD` | Yes (line 225) | `create_distance_csp()` build time | V3 | Yes |
| **(missing) `USE_AC3`** | **No** | — | V5 (BLOCKED) | No |
| **(missing) `RANDOM_SEED`** | No | — | (potential future) | No |
| **(missing) `VERBOSE`** | No | — | (driver-script ergonomics) | No |

---

## Report to PM

**Assignment recap:** Lab 6 — Constraint Satisfaction Problems, Round 1, Reviewer #2 — KNOB coverage focus. Solution files: `lab6\constraints_template_solution.py`, `lab6\Colors_solution.py`, `lab6\States_solution.py`. Variant bank: `study\_exam\Lab6-CSP\variants.md` (Variants 1–5).

**Status:** Pass with concerns.

**P0 findings:** None.

**P1 findings:**
1. **`constraints_template_solution.py:482-527 + KNOB block`** — Variant 5 ("AC-3 pre-pass") has the implementation (`CSP.ac3()`) but **no controlling KNOB**. The variant bank's KNOB-only contract is violated for V5. Fix: add `USE_AC3: bool = False` to the KNOB block; gate `csp.ac3()` in the entry-point harness.
2. **`constraints_template_solution.py:166-233`** — KNOBs are module globals read at call time; no documented reset / per-instance override / "set this knob at this lifecycle moment" idiom. Variants 2 and 4 require multiple runs in one process and will silently get stale state. Fix: docstring "Usage pattern" section + per-KNOB "Read at: import / create_csp / search" tag.
3. **`constraints_template_solution.py:225-233 + 679`** — `DISTANCE_THRESHOLD` is build-time-only; mutating it after `create_csp()` is a silent no-op. KNOB header omits this. Fix: prepend "Read at: `create_distance_csp()` call time — rebuild CSP after changing" to the header.
4. **`Colors_solution.py:56`, `States_solution.py:64`** — Both files have `# KNOB:` headers that are actually documentation references / extension points, not mutable knobs. Taxonomic confusion. Fix: introduce `# KNOB-REF:` and `# KNOB-EXT:` prefixes and apply.
5. **`constraints_template_solution.py:204-223`** — `USE_LCV` × `USE_FORWARD_CHECK` interact silently (LCV reads pruned domains). KNOB blocks don't document the interaction. Fix: cross-mention in both blocks.

**P2 findings:**
1. KNOB headers' "Exam variants" entries use prose rather than stable Vn identifiers (line 191 etc.).
2. `MAP_NAME` typed as plain `str` instead of `Literal["australia","south_america","distance_demo"]` (line 166).
3. Empty-snapshot edge case in FC backtrack is correct but uncommented (line 333).
4. `ACTIVE_COLORS` accepts duplicates silently (line 179).
5. No `VERBOSE` KNOB to quiet `_print_report` for multi-run driver scripts (lines 706–726).
6. `States_solution.py` mixes Australia & South America members; no `# KNOB-EXT` for adding a third map.
7. `_lcv_count` (line 440) and `is_consistent` (lines 388–396) iterate constraints differently — diverges if per-variable constraints are introduced.
8. No `RANDOM_SEED` KNOB / determinism guarantee in the docstring (line 37 has commented-out `shuffle`).
9. KNOB header wording is not strictly templated; standardise.

**QA Checklist (§7) status:** N/A — this is a KNOB-coverage / exam-variant adaptability review, not a feature-shipping QA. Treating the role brief's checklist as the per-review KNOB-coverage checklist:

- Every variant in `variants.md` answerable by KNOB-only mutation: **Fail** for V5; **Pass** for V1–V4.
- Every KNOB carries the standard header (default / range / what / effect / variants): **Pass** (modulo P2-9 template drift).
- Every KNOB documents its lifecycle moment (build-time vs call-time): **Fail** (P1-2, P1-3).
- No KNOB has undocumented interactions with another KNOB: **Fail** (P1-5 — `USE_LCV` × `USE_FORWARD_CHECK`).
- Taxonomy of KNOB / KNOB-REF / KNOB-EXT is clear and applied: **Fail** (P1-4).
- Default configuration reproduces the original lab output: **Pass** (Australia 3-colour produces a valid 7-region colouring).

**Acceptance criteria (§1) status:** N/A — same reason. As KNOB-coverage acceptance criteria:
- Variants 1–4 answerable by reading KNOB blocks + signatures only: **Met**.
- Variant 5 (AC-3 pre-pass) answerable by reading KNOB blocks + signatures only: **Not met** (P1-1).
- Multi-run driver scripts can compare configurations without source edits: **Met in practice but undocumented** (P1-2).

**DOCUMENT.md audit:** N/A for this lab solution (no per-directory DOCUMENT.md convention is established for `lab6/`; the solution files' module docstrings serve the same role and they ARE present in all three `_solution.py` files. If the project later imposes DOCUMENT.md, `lab6/DOCUMENT.md` would need to enumerate the seven KNOBs + the entry point + the three solver heuristics — about 30 lines.)

**Out-of-scope observations:**
- The `# shuffle(all_values)` line at `constraints_template.py:37` is a known template comment carried over unchanged. The solution's `order_domain_values` (line 373) does not even retain the comment. If the lab is ever reissued with shuffling enabled, the solution will silently lose determinism unless P2-8's `RANDOM_SEED` is added.
- The solution's `CSP.ac3()` is genuinely correct — I traced it on the South-America 3-colour case and it returns `True` (every binary not-equal constraint with `|D_i| ≥ 2` is arc-consistent, matching the variant bank's "AC-3 does NOT detect infeasibility on its own" prediction). The bug is *exposure*, not implementation (P1-1).
- The `States_solution.py` `__eq__` / `__hash__` / `__lt__` implementation is preserved from the template and works for both maps. Cross-map sorting is well-defined because Australia uses values 1–7 and South America uses 11–23, with no overlap. This is fragile but currently safe — a third map with values 1–23 would collide.

**Concerns / risks:**
- The Variant 5 gap (P1-1) is the only finding that *blocks* a documented exam variant from being answered as the variant bank promises. If round 2 ships without a `USE_AC3` KNOB, the variants.md preamble's promise becomes a half-truth — must be fixed or the preamble must be amended.
- The build-time-vs-call-time KNOB lifecycle confusion (P1-2, P1-3) is the kind of issue that produces *silently wrong* exam answers — driver scripts that look right and return numbers, but the numbers reflect stale state. Highest-priority fix after P1-1.
- The KNOB taxonomy issue (P1-4) is small in code-edit terms (rename 2 comments) but has outsized exam impact because the variants.md preamble explicitly instructs agents to "read every `# KNOB:` block in Colors_solution.py / States_solution.py". An ambiguous taxonomy at the entry point of the agent's reading list is a force multiplier for confusion.

**What PM should do next:**
1. Dispatch `pm-backend` (or whichever agent owns the lab solution) to make these targeted edits, in priority order:
   - Add `USE_AC3: bool = False` KNOB + harness gate (P1-1) — ~15 lines, including a new `# KNOB:` header block.
   - Add "Read at:" tags to every existing KNOB header (P1-2, P1-3) — one line each, 7 lines total.
   - Introduce `# KNOB-REF:` / `# KNOB-EXT:` prefixes in `Colors_solution.py:56` and `States_solution.py:64` (P1-4) — two line edits.
   - Cross-mention LCV × FC interaction in both KNOB blocks (P1-5) — two short paragraphs.
2. Re-dispatch Reviewer #2 with the same KNOB-coverage brief for Round 2 — focused spot-check on (a) the new `USE_AC3` knob actually drives `csp.ac3()` from the harness and (b) the lifecycle tags match the actual code paths.
3. P2 items can be batched into Round 2 or deferred; none are individually exam-blocking.

**DOCUMENT.md updated:** N/A for QA.
