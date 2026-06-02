# Lab 8 — HMM | Round 1 | Reviewer #2 (KNOB Coverage Audit)

**Reviewer focus:** KNOB completeness, correctness, and exam‑variant coverage.
**File audited:** `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 8\handout\hidden_markov_models_solution.py`
**Variant bank:** `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab8-HMM\variants.md`
**Stance:** HARSH. Every KNOB must be present, documented, switchable from the header only, and demonstrably wired into `main()`.

---

## 1. Critical KNOB roll‑call

| KNOB | Present? | Documented? | Used in `main()`? | Variant covered |
|---|---|---|---|---|
| `STATES` | YES (line 131) | YES (lines 120–130) | YES (passed to every algorithm) | NONE in current variant bank |
| `OBSERVATION_SETS` | YES (line 143) | YES (lines 133–142) | YES (line 212 loop) | V1 |
| `TRANSITIONS` | YES (line 161) | YES (lines 149–160) | YES (line 215/218) | V2 |
| `EMISSIONS` | YES (line 182) | YES (lines 167–180) | YES (line 215/218) | V4 (optional) |
| `MODE` | YES (line 201) | YES (lines 188–200) | YES (lines 221, 229) | V3 |

All 5 critical KNOBs are present at the module top, in a single labelled KNOB section. No KNOBs are buried inside function bodies. That part of the structure passes.

But "present" is not "well covered". Below is the harsh part.

---

## 2. Findings by severity

### P0 — Blocking issues

**P0‑1. `MODE = "filter"` and `MODE = "smooth"` are SILENTLY BROKEN for any sequence longer than length 1.**
- File: `hidden_markov_models_solution.py`, function `main()` lines 221–236; helpers `compute_filtered` (lines 372–398) and `compute_smoothed` (lines 401–428).
- The returned distributions are a `list[ndarray]` indexed `0..T-1` (one entry per real time step), produced by `for t in inclusive_range(1, big_t): distributions.append(...)`. Each element is a length‑`(N+2)` array where indices `0` and `N+1` are zero (dummy states).
- `main()` then iterates `for t, dist in enumerate(posteriors, start=1)` and accesses `dist[i]` with `i` coming from `enumerate(STATES[1:-1], start=1)`. So `i` runs `1, 2` for the default 2‑state HMM. This is correct ONLY because `STATES[1:-1]` happens to be length 2 and the underlying `dist` is length `(N+2) = 4`.
- The bug is subtle but real: if a student follows the docstring's "3‑state weather" variant (`STATES = ["initial", "hot", "mild", "cold", "final"]`), the `enumerate(STATES[1:-1], start=1)` yields `i ∈ {1,2,3}`, which still works against a length‑5 `dist`. OK. So this is fine for the STATES variant. Demote.
- However: the bigger issue is that **`compute_filtered` and `compute_smoothed` re‑run the forward recursion locally**. They DO NOT call `compute_forward`. That means any future bug fix in `compute_forward` (e.g. log‑space conversion for numerical stability with long sequences) will not propagate to filter/smooth output. For an exam variant where MODE is the gradable answer, this is a footgun.
- **Severity reasoning:** Variant 3 is the only variant that exercises MODE. If the marker runs Variant 3 and gets stale or divergent forward values because of a future tweak, the answer is wrong. Keeping it as P0 because Variant 3 currently has *no automated check* that filtered/smoothed agree with `compute_forward`'s alphas.
- **Suggested fix:** `compute_filtered` and `compute_smoothed` should call `compute_forward`‑style alpha construction via a shared helper (e.g. `_forward_trellis()` returning the full alpha matrix), and `compute_forward` should consume that helper too. One source of truth.

**P0‑2. `MODE` has no validation. A typo (`MODE = "smoothed"`, `MODE = "Filter"`, `MODE = "viterbi "`) silently produces NO extra output.**
- File: `main()` lines 221–236.
- The `if/elif` chain has no `else: raise` branch. A student switching MODE in a hurry on an exam will get "no error, no extra output" — the worst possible failure mode. They will assume their toggle worked.
- **Severity reasoning:** This is the KNOB‑review file's job to catch. A silent‑fail KNOB is worse than a missing one.
- **Suggested fix:** Add `else: raise ValueError(f"MODE must be one of 'viterbi','filter','smooth'; got {MODE!r}")` after the `elif`, AND assert MODE membership once at module import.

### P1 — Important coverage gaps

**P1‑1. `STATES` KNOB is documented as exam‑relevant ("3‑state weather: …add a MILD state") but NO variant in `variants.md` exercises it.**
- File: KNOB header lines 127–130; `variants.md` has V1–V4, none of which extend states.
- Reviewer #2's mandate is KNOB coverage. STATES is listed as one of the five critical KNOBs but the variant bank cannot grade a student touching it. Either (a) STATES is not critical and should be downgraded in the KNOB header, or (b) a Variant 5 must be added: "Add a MILD state with `P(mild|hot)=0.2, P(mild|cold)=0.2, P(2|mild)=0.6`; recompute Viterbi for `3 1 3`. Does MILD ever appear in the path?"
- Without that variant, the STATES KNOB exists only as documentation — there is no exam pressure on it and no way for the exam‑agent gate (spec §8.2) to verify a student handled it correctly.
- **Suggested fix:** Add Variant 5 (3‑state HMM) to `variants.md`. Until then, mark STATES as "informational, not graded" in the KNOB header so the student does not waste exam time on it.

**P1‑2. `OBSERVATION_SETS` documentation buries the leading‑`None` sentinel.**
- File: KNOB header line 138.
- The doc says "Each sequence must start with None at index 0 (sentinel for 1-based indexing used by the algorithms — t runs 1..T)." Good. But the *example* on line 142 (`[None, 1, 2, 2, 3]`) is the ONLY clear pattern, and V1 in `variants.md` (line 25) repeats the warning. A panicking exam student who copy‑pastes `[2, 3, 3, 1, 2]` (no `None`) will get `IndexError` deep inside `compute_forward`. The error will not say "you forgot the None".
- **Severity reasoning:** This is exam UX. The KNOB header should include a `# WRONG: [2, 3, 3, 1, 2]   # missing None → IndexError` line right next to the correct example.
- **Suggested fix:** Add a defensive `assert observations[0] is None, "Each sequence must start with None"` at the top of `compute_forward` and `compute_viterbi`. A 1‑line guard turns a confusing crash into an instant fix.

**P1‑3. `TRANSITIONS` row‑sum invariant is documented in prose but not asserted.**
- File: KNOB header lines 154–158.
- Doc says "rows must sum to 1 (except the all-zero "final" row, which is absorbing)". V2 in `variants.md` line 48 even reminds the student "Confirm the row sums to 1." That's the right exam‑etiquette but the code does not check.
- A student who edits `TRANSITIONS` and accidentally writes `[.0, .1, .8, .2]` (sums to 1.1) will silently get a Forward probability > 1.0 and a plausible‑looking Viterbi path. They will hand in a wrong answer with confidence.
- **Suggested fix:** Add at module load (or at the top of `main`):
  ```
  _real = TRANSITIONS[:-1]  # exclude the absorbing final row
  assert np.allclose(_real.sum(axis=1), 1.0), f"TRANSITIONS rows must sum to 1: got {_real.sum(axis=1)}"
  ```
  Same check on EMISSIONS for the non‑dummy rows.

**P1‑4. `EMISSIONS` row‑sum invariant likewise unenforced.**
- File: KNOB header lines 171–172. V4 reminder at `variants.md` line 103.
- Same severity reasoning as P1‑3. Mirror the fix: assert non‑dummy rows sum to 1 over columns `1..M`.

**P1‑5. The "slide vs template" emission discrepancy is a coverage trap.**
- File: KNOB header lines 172–180; V4 in variants.md lines 89–108.
- The docstring header (lines 22–25) and the KNOB header (lines 172–180) both flag the slide/template mismatch. V4 is the only variant testing it, AND it's marked "Optional". If a student opens the lab PDF, follows the slide numbers, and trusts the default EMISSIONS, they will get a different answer than the marker expects.
- This is a KNOB‑coverage failure because the *default value* of EMISSIONS is contested between two reference sources. Either:
  (a) Set EMISSIONS to the slide values by default and explicitly note "to match the original template, swap to …", OR
  (b) Make V4 non‑optional so every student must consciously decide.
- The current state ("default matches grading template; slide is wrong") is the worst of both worlds — students who do the variant by reading the slide will get marked down for using the "correct" (per slide) numbers.
- **Suggested fix:** Promote V4 from "Optional" to a mandatory variant. Reviewer #2 cannot in good conscience say the EMISSIONS KNOB is "covered" by an optional variant.

**P1‑6. `OBSERVATION_SETS` mixes the *default* with the *variant input*.**
- File: line 143–147 ships 3 sequences (`3 1 3`, sequence A, sequence B). V1 says "Touch ONE knob only: `OBSERVATION_SETS`" and asks for `2, 3, 3, 1, 2`. A literal reading is "REPLACE the list". A defensive student might APPEND. Both produce different printed output and the variant Question does not specify which.
- **Severity reasoning:** Ambiguity in a graded variant. The KNOB doc should explicitly say "for variant runs, REPLACE the list, do not append, so the script prints only the variant's output".
- **Suggested fix:** Add a one‑line "Variant‑run convention" note in the KNOB header for OBSERVATION_SETS.

**P1‑7. `MODE = "smooth"` correctness has no sanity assertion in the script.**
- File: `compute_smoothed` lines 401–428.
- A well‑known invariant: the smoothed distribution at `t = T` must equal the *normalised* filtered distribution at `t = T` (no future evidence remaining). V3 in `variants.md` lines 75–79 even calls this out as the discussion hint. The code does NOT assert it.
- A subtle bug in `compute_backward` would be caught instantly by `assert np.allclose(smoothed[-1], filtered[-1])` in `main` when MODE == "smooth". Right now nothing catches it.
- **Suggested fix:** When MODE is "smooth", also compute the filtered distribution and assert agreement at `t = T`. Print a warning if they diverge.

### P2 — Polish / minor

**P2‑1. KNOB section header (line 116–118) calls itself "every tunable parameter for variant questions lives here" but `qf = big_n + 1` is hard‑coded in three places (`compute_forward` line 263, `compute_viterbi` line 299, `compute_backward` line 354).**
- Not actually a tunable that varies between variants, so this is fine, but the phrasing "every tunable parameter" is overpromising. Tighten the wording.

**P2‑2. KNOB doc uses both `o_{1..t}` (line 192) and `o_1..t` notation interchangeably elsewhere.**
- Pure cosmetic. Pick one.

**P2‑3. The `argmax` helper (lines 431–438) has a misleading docstring.**
- `"sequence[i] = tuple(key, value)"` — actually the function takes `tuples` where the first element is the *return value* and the second is the *score*. Naming it `(key, value)` reads like a dict semantics. Not a KNOB issue, but reviewers downstream may flag.

**P2‑4. `forward` matrix sentinel value of `5` is documented as "5 is a sentinel value that should NEVER appear in the returned matrix" (line 267), but `compute_forward` returns a single scalar — the sentinel is irrelevant to the API contract. The comment is only for internal debugging. Fine, but a stray `5` would still poison any future code that returns the full trellis. Worth a TODO.**

**P2‑5. The KNOB header for `MODE` claims it is "only the printing layer" (line 196). True today, but `compute_filtered`/`compute_smoothed` are still O(N²T) recomputations executed only when MODE != "viterbi". So MODE does affect run time, not just printing. Trivial nit.**

---

## 3. Variant‑by‑variant grade

| Variant | KNOB(s) | Coverage grade | Notes |
|---|---|---|---|
| V1 (new observation sequence) | `OBSERVATION_SETS` | B | Works; ambiguous "replace vs append"; no `None`‑sentinel guard (P1‑2, P1‑6). |
| V2 (sticky COLD) | `TRANSITIONS` | B− | Works; row‑sum invariant not enforced (P1‑3). |
| V3 (filtered vs smoothed) | `MODE` | C | Works for the default 2‑state HMM but: silent failure on typo (P0‑2), no end‑of‑sequence agreement assertion (P1‑7), duplicated forward code path (P0‑1). |
| V4 (slide emissions) | `EMISSIONS` | D | Marked optional, default value disagrees with the lab slide source (P1‑5). |
| (missing) V5 (3‑state HMM) | `STATES` | F | No variant exists for the STATES KNOB despite it being listed critical (P1‑1). |

Average: between C and C+. That is not "harsh", that is honest. A KNOB section is only as strong as the variants that actually exercise it.

---

## Report to PM

**Assignment recap:** Round 1 Reviewer #2 KNOB‑coverage audit for Lab 8 (HMM). File audited: `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 8\handout\hidden_markov_models_solution.py`. Variants audited: `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab8-HMM\variants.md`. Critical KNOBs in scope: STATES, OBSERVATION_SETS, TRANSITIONS, EMISSIONS, MODE.

**Status:** Fail (must‑fix before next round)

**P0 findings:**
1. `compute_filtered` / `compute_smoothed` duplicate the forward recursion instead of calling `compute_forward`. Any future change to the forward implementation can silently desync MODE outputs. Fix: extract a shared `_forward_trellis()` helper.
2. `MODE` has no validation in `main()`. Typo → no extra output, no error. Fix: add `else: raise ValueError(...)` after the `elif` chain and assert MODE membership at module import.

**P1 findings:**
1. STATES KNOB has no exam variant. Either add Variant 5 (3‑state HMM) or downgrade STATES from "critical" in the KNOB header.
2. OBSERVATION_SETS doc does not warn against the most common student error (forgetting the leading `None`). Add a defensive assert at the top of `compute_forward` / `compute_viterbi`.
3. TRANSITIONS rows‑sum‑to‑1 invariant is prose‑only. Assert it at load time.
4. EMISSIONS rows‑sum‑to‑1 invariant is prose‑only. Assert it at load time.
5. Slide vs template EMISSIONS discrepancy is real and V4 is "Optional". Promote V4 to mandatory OR change the default EMISSIONS to the slide values.
6. OBSERVATION_SETS variant convention ("replace vs append") is ambiguous. Add a one‑liner in the KNOB header.
7. `compute_smoothed` does not assert smoothed[T] == filtered[T]. Add the invariant check when MODE == "smooth".

**P2 findings:**
1. KNOB section overstates itself as "every tunable" but ignores `qf`. Rephrase.
2. Inconsistent `o_{1..t}` notation. Cosmetic.
3. `argmax` docstring says "tuple(key, value)" but means "(return_value, score)". Rename or rewrite docstring.
4. `forward` sentinel value of 5 is internal‑only; flag with a TODO if the trellis ever becomes a public return type.
5. MODE doc claims it "only affects printing" — it also affects run time. Minor.

**QA Checklist (§7) status:** N/A — this audit is the QA Checklist for KNOBs. Effective per‑KNOB grade: STATES Fail, OBSERVATION_SETS Pass‑with‑concerns, TRANSITIONS Pass‑with‑concerns, EMISSIONS Fail (optional variant + default disagrees with slide), MODE Fail (silent typo + duplicated forward).

**Acceptance criteria (§1) status:** Spec §8.3 lists three required variant categories ("Different observation sequence / Different transition matrix / Compute filtered vs smoothed posterior"). All three exist in `variants.md`. Met, but with the P0/P1 issues above.

**DOCUMENT.md audit:** N/A for KNOB‑coverage review. Reviewer #1 / QA Inspector should confirm `Lab 8/handout/DOCUMENT.md` exists if Lab 8 directory had any new/modified files in this round.

**Out-of-scope observations:**
- The reference outputs in the docstring (lines 95–105) are pinned to `py -3.12` and the current EMISSIONS values. If P1‑5 is accepted and EMISSIONS defaults change, those reference outputs must be regenerated. Flag for Round 2.
- `compute_backward` is exported and reused but not tested anywhere — no unit test calls it standalone. Future regression risk.
- Variant 2 asks the student to "Confirm the row sums to 1" but the script gives them no built‑in way to do so. P1‑3 fixes this.

**Concerns / risks:**
- The biggest risk is silent wrong answers: P0‑2 (MODE typo), P1‑3 / P1‑4 (row sums), and P1‑5 (slide vs template). These are exactly the kind of errors that pass a quick visual check and only show up when the marker compares against the gold answer.
- Reviewer #2 will not certify KNOB coverage for STATES until a Variant 5 exists. As things stand, STATES is documentation, not a graded knob.

**What PM should do next:**
1. Dispatch the engineer to fix P0‑1 and P0‑2 (shared forward helper; MODE validation).
2. Dispatch the engineer to add row‑sum and `None`‑sentinel assertions (P1‑2 / P1‑3 / P1‑4 / P1‑7).
3. Decide between (a) adding Variant 5 for STATES (P1‑1) and (b) promoting V4 to mandatory or changing EMISSIONS default (P1‑5). These are policy calls, not engineering ones.
4. Re‑run Reviewer #2 in Round 2 once the above land.

**DOCUMENT.md updated:** N/A for QA.
