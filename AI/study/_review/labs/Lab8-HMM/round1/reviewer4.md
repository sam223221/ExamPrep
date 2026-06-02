# Lab8-HMM Round 1 — Reviewer #4 (Variant Adaptability)

## Report to PM

**Assignment recap:** Lab8-HMM Round 1. Reviewer #4 perspective:
**variant adaptability** — can the locked solution at
`C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 8\handout\hidden_markov_models_solution.py`
answer the variants in
`C:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab8-HMM\variants.md`
using ONLY the surfaces the spec (§8.2) permits an exam agent to read:
the **module-level docstring**, the **`# KNOB:` comment blocks**, the
**`def ...:` signatures**, plus any **data files** the lab consumes
(none for Lab 8).

Files inspected (absolute paths):

- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 8\handout\hidden_markov_models_solution.py`
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 8\handout\hidden_markov_models.py` (original template, for delta comparison)
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 8\handout\Lab 8.pdf` (handout — only cross-checked for slide-vs-template emission diff claim in V4)
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab8-HMM\variants.md`
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\docs\superpowers\specs\2026-05-22-ai-exam-prep-study-package-design.md` §8.2, §8.3

Sanity runs performed (allowed-surface re-execution by hand-injecting
KNOB-equivalent values into a Python harness that imports the solution
module without modifying the file). Baseline default `py -3.12
hidden_markov_models_solution.py` reproduced the three docstring
"OUTPUTS WHEN RUN" lines verbatim (modulo cosmetic `np.str_(...)`
wrappers around the path strings).

**Status:** **Pass with concerns** — all three mandatory gate variants
(V1, V2, V3) and the optional V4 are solvable using only the documented
surface, BUT there are several documentation rough edges, one
**factually overreaching claim** in V3's hint, and one **scope-drift
risk** in V1's hint that an exam agent following the docs literally
will trip over. Two are P1 (block APPROVED but not the gate).

---

### P0 findings (block the gate as-currently-written)

None. The four variants all execute to a believable answer when the
KNOB recipes are applied verbatim. No exam agent will get
`NotImplementedError` or a `TypeError` from following the docs.

---

### P1 findings (important — fix before round-2 gate)

**P1-1. Variant 3's "the last time step must agree exactly" claim is
only true because the default HMM happens to have equal end-transitions
(`A[hot, qf] = A[cold, qf] = 0.2`). The variant presents this as a
universal property of forward-backward — that is wrong.**

- File: `study\_exam\Lab8-HMM\variants.md` lines 76-79.
  > *"For the discussion: at the *last* time step the filtered and
  > smoothed distributions must agree exactly (no future evidence to
  > add). Any divergence at earlier steps is the contribution of future
  > observations."*
- The math: smoothed posterior γ_T(s) ∝ α_T(s)·β_T(s); per the
  solution's `compute_backward` (line 359-360), `β_T(s) = a[s, qf]`.
  Filtered posterior at T is α_T(s) / Σ_s' α_T(s'). These agree iff
  `a[s, qf]` is the **same constant** across all real states s — only
  then does β_T(s) factor out of the normalisation. In the default
  HMM that constant is 0.2 (TRANSITIONS lines 161-164). In **Variant
  2**'s modified HMM that constant is still 0.2 (cold-row
  `[.0, .1, .7, .2]`), so the property survives by coincidence. The
  moment a future variant tweaks one row's end-transition (which is a
  legal KNOB edit per the TRANSITIONS doc), the V3 hint becomes a lie.
- The exam agent — reading only the variants.md + the KNOB blocks —
  will accept this as a general fact and may carry it into a later
  variant where it breaks.
- **Suggested fix:** Replace lines 76-79 of `variants.md` with: *"For
  the discussion: at the *last* time step the filtered and smoothed
  distributions agree exactly **whenever all real states share the
  same end-transition probability a[s, qf]** (true for the default
  HMM, since hot→end = cold→end = 0.2). Any divergence at earlier
  steps is the contribution of future observations."* Even better,
  add a one-line "Property" note inside the `compute_backward` or
  `compute_smoothed` docstring noting this dependency, so the agent
  reading the function signature/docstring can verify the claim
  themselves without seeing the body.

**P1-2. Variant 1's hint tells the agent "Touch ONE knob only:
`OBSERVATION_SETS`" but never says whether to REPLACE the list or
APPEND to it.**

- File: `study\_exam\Lab8-HMM\variants.md` lines 23-27.
  > *"Touch ONE knob only: OBSERVATION_SETS. … The script will print
  > both the Forward probability and the Viterbi path."*
- The solution's `OBSERVATION_SETS` KNOB doc (lines 133-142) says:
  *"list of observation sequences to decode … Variant 1 (new
  sequence): e.g. [None, 1, 2, 2, 3] — **set it here**."* The phrase
  "set it here" is ambiguous: an agent that interprets "set" as
  "add" will end up with 4 sequences, and the variant's expected
  answer shape ("Probability is a single positive float; Path is a
  length-5 list") doesn't make it obvious which of the four printed
  blocks is the answer. The agent has to manually count
  `len(observations) == 5` to identify the right block — that's a
  fragile inference.
- An agent that interprets "set" as "replace" gets exactly one block
  printed and the answer is unambiguous. Both interpretations
  produce *correct* numbers, but only one produces a *clean* run log
  for the `examiner{1-3}-attempt.md` `RUN OUTPUT` section.
- **Suggested fix:** Add to variant 1's hints: *"Replace the entire
  list, so `OBSERVATION_SETS = [[None, 2, 3, 3, 1, 2]]`. This keeps
  the printed output to a single block matching the expected
  answer."* Or amend the `OBSERVATION_SETS` KNOB doc itself to say
  "replace with the variant sequence" instead of the ambiguous "set
  it here".

**P1-3. Variant 2's expected-answer shape demands "two probabilities,
two 3-element paths, and one sentence comparing them" but the variant
hints tell the agent to set `OBSERVATION_SETS = [[None, 3, 1, 3]]`
and modify TRANSITIONS — i.e. ONE run of the script, which produces ONE
probability + ONE path.**

- File: `study\_exam\Lab8-HMM\variants.md` lines 46-55. The hint says
  "Keep `OBSERVATION_SETS = [[None, 3, 1, 3]]` to isolate this
  comparison from the longer sequences." But the same hint says
  "Report: original Viterbi path vs new Viterbi path; original
  probability vs new probability." The agent must somehow know to
  EITHER:
  - run the script twice (once with default TRANSITIONS, once with
    modified), OR
  - read the original-default value from the docstring "OUTPUTS WHEN
    RUN" section (lines 95-97 of the solution: `0.016809…` and
    `['hot', 'cold', 'hot']`).
- The variant does not spell out either method. An exam agent
  following the literal hints will produce ONE run and call it done,
  then realise the answer shape demands two and either (a) hand-wave
  the original from memory or (b) revert the KNOB and re-run (which
  is a second run not documented in `KNOB CHANGES`).
- **Suggested fix:** Add one bullet to V2 hints: *"You will need two
  runs to populate this comparison. EITHER (a) run once with default
  TRANSITIONS, save output; then modify TRANSITIONS and run again,
  OR (b) read the original-default `Probability: 0.016809200...`
  and `Path: ['hot', 'cold', 'hot']` directly from the OUTPUTS WHEN
  RUN block in the solution docstring (it is part of the allowed
  surface)."* Option (b) is cleaner because it makes the
  `KNOB CHANGES` diff in the examiner-attempt file unambiguous (one
  diff, not two).

**P1-4. The `MODE` KNOB doc claims "filter" prints "the normalised
forward column" but `main()` only prints columns for the real states
(STATES[1:-1] via the `enumerate(STATES[1:-1], start=1)` loop on lines
224-228 and 232-236), NOT a full normalised column over all `len(states)`
entries. The KNOB documentation glosses over which rows are visible to
the student.**

- File: `hidden_markov_models_solution.py` lines 188-201 (MODE KNOB
  doc) and 221-236 (the printing layer in `main()`).
- The KNOB block reads: *"'filter': for each t, print P(q_t = k |
  o_{1..t}), the normalised forward column."* This implies the
  caller will see a length-N+2 vector with the initial/final entries
  set to zero. They will only see the HOT and COLD entries (the
  real-state slice) — the dummy initial/final probabilities are
  silently dropped from print. This is a print-layer detail, not a
  semantics bug, and for V3's purposes it's fine: the agent only
  cares about HOT and COLD. But the wording invites confusion.
- More importantly, an exam agent who sees the `compute_filtered`
  return annotation `list[ndarray]` (line 372 in the def signature
  — they can see this) and then reads the KNOB doc may believe the
  printed dict-shaped output covers all N+2 states. When they only
  see HOT and COLD, they may wonder if their KNOB change was
  applied at all.
- **Suggested fix:** Rewrite MODE KNOB lines 192-194 as: *"'filter':
  for each t, print P(q_t = HOT | o_{1..t}) and P(q_t = COLD |
  o_{1..t}) — the two real-state entries of the normalised forward
  column. The dummy initial/final entries are zero by construction
  and are not printed."* Same edit for 'smooth'.

**P1-5. The expected-answer shape for Variant 3 says "Two tables (one
for filter, one for smooth) of three rows (t=1, t=2, t=3)" — but the
script's actual print format is one line per t with two
`name=prob` fields, not a tabular layout.**

- File: `study\_exam\Lab8-HMM\variants.md` lines 81-85.
- The actual stdout for MODE = "smooth" on `3 1 3` (verified by
  running an in-process harness):
  ```
  Smoothed P(q_t | o_{1..T}):
    t=1: hot=0.9723, cold=0.0277
    t=2: hot=0.0315, cold=0.9685
    t=3: hot=0.8149, cold=0.1851
  ```
  That is one row per t — not the two-column "table" the variant
  prompt describes. An exam agent will produce the right *numbers*
  but a literal-reading agent may waste tokens hand-formatting them
  into a Markdown table that the rubric didn't actually demand. The
  spec §8.2's `RUN OUTPUT:` field is captured stdout — so the agent
  should just paste the script's output, not reformat it.
- **Suggested fix:** Replace "Two tables (one for filter, one for
  smooth) of three rows (t=1, t=2, t=3), each with the HOT / COLD
  probability" with "Two stdout blocks (one for filter, one for
  smooth), each with three `t=…: hot=…, cold=…` lines". Brings the
  rubric in line with what the script actually emits.

---

### P2 findings (polish / nice-to-have)

**P2-1.** The `MODE` KNOB doc says *"Effect: only the printing layer;
compute_forward and compute_viterbi always run."* — but for V3 the
exam agent must perform TWO script invocations (one with MODE =
"filter", one with MODE = "smooth"). The variant's "two runs" note is
in V3's hints, not in the MODE KNOB block itself. An exam agent
reading the MODE doc in isolation may not realise that comparison
requires two runs rather than a single "show both" mode. Suggest
adding to MODE KNOB doc: *"Note: to compare filter vs smooth, run the
script twice — once with each value."* Or — better — add a
`MODE = "both"` option that prints both panels in one run, then V3
becomes a one-edit variant.

**P2-2.** The header docstring's "HOW TO ADAPT THIS FOR DIFFERENT
QUESTION VARIANTS" section (lines 52-83) enumerates **five**
adaptation recipes (1-5), while `variants.md` defines **four**
variants (V1 + V2 + V3 + optional V4). The mapping is
roughly 1→V1, 2→V2, 3→V4, 5→V3 — adaptation recipe 4 ("More hidden
states") has NO corresponding variant in `variants.md`. Either add a
variant 5 ("3-state HOT/MILD/COLD") to `variants.md` or remove
adaptation recipe 4 from the docstring. Extra documented surface
that an exam agent may waste tokens exploring.

**P2-3.** The header `OUTPUTS WHEN RUN` block (lines 92-105) shows the
**default** outputs for `3 1 3`, `3 3 1 1 2 2 3 1 3`, and `3 3 1 1 2
3 3 1 2`. None of the **variant** outputs (V1's `2 3 3 1 2`, V2's
modified-cold result on `3 1 3`, V3's filter/smooth tables, V4's
slide-emission result) is shown. An exam agent who wants to
**self-verify** their KNOB change had an effect has nothing to
compare against. Adding a `VARIANT REFERENCE OUTPUTS` block (gated
behind something like `# For self-check only — do NOT consult before
solving`) would let an honest agent confirm and a cheating one find
their cheat — same problem the GA reviewer flagged at P2-3 in
`Lab4-GA\round1\reviewer4.md`. Spec is ambivalent on this; flag
as nice-to-have.

**P2-4.** `OBSERVATION_SETS` KNOB doc (lines 138-142) lists "Variant 1
(new sequence): e.g. `[None, 1, 2, 2, 3]`" as an example — but
`variants.md` V1 uses `[None, 2, 3, 3, 1, 2]`. These are
inconsistent example payloads; both are valid Variant 1 framings, but
mixing them looks like doc drift. Pick one (the variants.md sequence
is the gate-tested one, so use it).

**P2-5.** The `EMISSIONS` KNOB doc (lines 167-186) hard-codes the
slide-vs-template discrepancy as the Variant 4 example. The slide
emissions are buried at line 174: *"slide hot row would be
`[.0, .2, .4, .4]`"*. An exam agent reading top-to-bottom is told
twice that the slide values are `[.0, .2, .4, .4]` / `[.0, .5, .4,
.1]` (once in the docstring header lines 22-24, once in the KNOB
block line 174). This is fine, but it does mean V4 is the *most
hand-held* of the four variants — the agent can essentially copy the
matrix verbatim. The spec (§8.2) implies grading on adaptation
skill, not recipe recall (per the GA reviewer's P2-3). V4 is the
weakest demonstration of "variant adaptability" because the answer
is pre-typed in the KNOB doc. Not blocking — V4 is optional — but
worth noting that V4 effectively tests reading comprehension, not
HMM adaptation.

**P2-6.** Variant 3's "intuitively why?" question asks the agent to
name **which future observation drove the largest filtered→smoothed
shift**. The biggest shift is at t=2 (≈+0.9 percentage points for
COLD, smoothed value 0.9685 vs filtered 0.9592 — verified by
in-process harness). The driver is the o_3 = 3 observation, which
pulls the t=2 posterior slightly toward COLD-then-HOT-transition
intuition. The variant hint never says "expect a small shift"; an
agent expecting a dramatic shift may think their forward-backward
implementation is broken. Recommend adding to V3 hints: *"Expected
shift magnitude is ~1 percentage point for this short sequence —
do not expect dramatic divergence between filter and smooth on a
T=3 chain."* Builds the right expectation.

**P2-7.** The `compute_filtered` and `compute_smoothed` `def` lines
(372, 401) are visible to exam agents per spec §8.2 (function
signatures are allowed). Their **docstrings** (lines 374-378 and
403-407) are inside the function body and are NOT explicitly listed
as "allowed surface" in §8.2. Strictly, the spec says "the docstring
header" (singular, module-level) is allowed — not per-function
docstrings. If the spec is read strictly, the per-function
docstrings should be moved up into the module-level header (or into
their own KNOB block) so the exam agent can legitimately consult
them. As written, an agent in compliance with the spec letter has
to infer the meaning of `compute_filtered` from just its name + the
MODE KNOB block. That works here because the MODE block explains
filter vs smooth in plain English, but is fragile across
labs. Coordination point with the spec author, not a Lab 8 bug per
se.

**P2-8.** V1's expected-answer shape says *"Path is a length-5 list of
state-name strings (each is 'hot' or 'cold')"*. The actual script
output is `Path: [np.str_('hot'), np.str_('cold'), …]` — i.e. the
strings are wrapped in `np.str_(...)` repr because they came from a
NumPy `ndarray[str]`. This is a cosmetic artefact of how
`convert_path_states_to_observations` (line 241-242) returns
`states[p]` items as `np.str_` rather than plain `str`. An exam
agent comparing their RUN OUTPUT to the expected shape literally may
flag this as a discrepancy. The fix is one line: `return [str(states[p]) for p in path]`.

---

### Variant-by-variant adaptability table

| Variant | Allowed-surface adaptable? | Notes |
|---|---|---|
| V1 — Different observation sequence (`2 3 3 1 2`) | **Yes** | `OBSERVATION_SETS` KNOB is documented, leading-`None` sentinel called out twice (header + KNOB block). Caveat P1-2 (replace vs append ambiguity) + P2-4 (example mismatch) + P2-8 (`np.str_` cosmetics). |
| V2 — Sticky cold transitions | **Yes** | `TRANSITIONS` KNOB explicitly names this variant in its example block (lines 156-159). Cold-row `[.0, .1, .7, .2]` row-sums to 1.0 (verified). Caveat P1-3 (two-runs ambiguity). |
| V3 — Filtered vs smoothed | **Yes** | `MODE` KNOB documents both modes and references V3 by name (line 198-200). `compute_filtered` and `compute_smoothed` signatures are visible. Caveats P1-1 (overreaching last-step claim), P1-4 (print layer ambiguity), P1-5 (table-vs-stdout rubric mismatch), P2-1 (single-MODE-per-run), P2-6 (expect small shift), P2-7 (per-function docstring outside strict allowed surface). |
| Optional V4 — Slide emission values | **Yes** | `EMISSIONS` KNOB literally types out the slide-row values (line 174). The variant is essentially copy-paste. P2-5 notes this is the weakest "adaptability" demonstration of the four. |

### Acceptance criteria — mandatory variants

- **V1** ("probability is a single positive float much less than 1; path is length-5 list of 'hot'/'cold'"):
  In-process harness produces `Probability: 6.3812e-05` and
  `Path: ['hot', 'hot', 'hot', 'cold', 'cold']`. **Met** (modulo
  `np.str_` cosmetic, P2-8).
- **V2** ("two probabilities, two paths, one comparison sentence"):
  Original `3 1 3` baseline = `0.016809…`, path `[hot, cold, hot]`.
  Modified-cold = `0.009189…`, path `[hot, cold, hot]` (verified
  in-process). The path **does not change** under the sticky-cold
  modification — that's the comparison sentence the variant invites
  the agent to make. **Met** (modulo P1-3 two-runs ambiguity).
- **V3** ("two tables / two stdout blocks of three rows, plus one
  sentence identifying the largest-shift step and the future
  observation that drove it"):
  Filtered: t=1 hot=0.9677, t=2 hot=0.0408, t=3 hot=0.8149.
  Smoothed: t=1 hot=0.9723, t=2 hot=0.0315, t=3 hot=0.8149
  (verified in-process). t=2 has the largest filtered→smoothed
  shift (~0.9 pp toward cold). Driver: the future observation o_3=3
  raises the retrospective probability of hot at t=3, which under
  the transition matrix slightly raises the joint plausibility of
  the "cold at t=2 → hot at t=3" path relative to "hot at t=2 →
  hot at t=3". **Met** (modulo P1-1 overreaching last-step claim,
  P1-4/P1-5 rubric/print wording).

### Acceptance — optional variant

- **V4** ("probability under slide emissions for `3 1 3`; does the
  most-likely sequence change?"):
  In-process harness produces `Probability: 0.003826…`,
  `Path: [hot, cold, hot]` — same path as default, lower probability
  (because the slide hot row gives `P(3|hot) = 0.4` instead of the
  template's `0.75`). **Met**.

### DOCUMENT.md audit

N/A — this is a lab solution dir, not a project feature ship. No
DOCUMENT.md is required by the variants spec.

### Out-of-scope observations

1. **`forward[qf, big_t]` is written but never used after termination.**
   `compute_forward` lines 283-287 store the sum into
   `forward[qf, big_t]` and immediately return its float cast. The
   intermediate write is wasted; `return float(sum(...))` would do.
   No effect on correctness or on variant adaptability. Cosmetic.

2. **`compute_filtered` re-runs the forward pass instead of accepting
   a precomputed `forward` trellis.** Lines 383-391 duplicate the
   recursion already in `compute_forward`. For a T=3 sequence this is
   negligible; for a hypothetical "longer-sequence" variant (e.g. the
   T=9 Exercise 2 sequences) the duplication becomes O(N²·T) extra
   work per MODE = "filter" run. Not a blocker — Lab 8 sequences are
   tiny. But a refactor opportunity for round 2: factor out a
   `_run_forward_pass(states, observations, A, B) -> ndarray` helper
   and call it from `compute_forward`, `compute_filtered`,
   `compute_smoothed`. Three-way DRY.

3. **`compute_smoothed` likewise duplicates the forward pass** (lines
   411-419). Same fix as out-of-scope obs 2.

4. **`argmax` helper (lines 431-438) returns the *key* element of the
   max-tuple, not its NumPy index.** The `def` line of `argmax` is
   visible to exam agents but the docstring inside (the convention
   note about `sequence[i] = tuple(key, value)`) is *not* allowed by
   strict §8.2 reading. An agent that wants to extend with a custom
   variant (e.g. "argmax over a numpy array directly") may not
   realise this helper is tuple-list-specific. Same as P2-7 — a
   per-function-docstring vs strict-spec coordination issue.

5. **`STATES = np.array(["initial", "hot", "cold", "final"])`** uses
   a NumPy array of Python strings. `states[1:-1]` therefore yields
   `np.str_` items, which is the source of P2-8. The dtype is
   intentional (the array also indexes into `np.ndarray[str]` returns
   from `convert_path_states_to_observations`), so changing it costs
   a downstream type ripple. Worth a `str(...)` cast in
   `convert_path_states_to_observations` only.

### Concerns / risks

1. **The Variant 3 hint at variants.md lines 76-79 carries a wrong
   universal claim** (P1-1). Of all the issues above this is the
   one that hurts trust in the variant bank as a teaching tool: an
   exam agent that internalises "last step always agrees" carries
   that misconception into BN / future-HMM material. Highest fix
   priority of the P1s.

2. **Two of the four variants (V1, V2) ship with one-or-more
   ambiguous instructions** (P1-2 replace-vs-append, P1-3
   one-run-vs-two). Either ambiguity is recoverable from common
   sense, but the gate is supposed to test the *docs*, not the
   agent's common sense. A strict reading of §8.2 says an agent who
   gets stuck on ambiguity should report `STUCK`, not heroically
   resolve it — and these are exactly the ambiguities that produce
   a non-deterministic `SOLVED` / `STUCK` split across the three
   exam agents.

3. **V4 (optional) is functionally a recipe-recall exercise**
   (P2-5). The locked KNOB doc literally types out the slide-emission
   row vector that V4 asks for. Useful as a smoke test but does not
   strongly demonstrate adaptability. Consider replacing V4 with a
   harder optional variant (e.g. "make initial-distribution
   uniform: change TRANSITIONS row 0 to `[.0, .5, .5, .0]` and
   re-decode `3 1 3`; how does the path change?") which exercises
   a different KNOB area.

4. **No automated test asserts that the variants.md recipes actually
   produce the expected outputs against the locked solution.** Same
   gap noted in `Lab4-GA\round1\reviewer4.md` concern #3. The gate
   is testing the docs by eye; the docs will rot. Worth a
   `pytest test_variants.py` that imports the solution, mutates
   each KNOB to the variant value, calls the four entry points, and
   asserts the expected numbers (V1 prob ≈ 6.38e-5, V2 prob ≈
   9.19e-3 + path equality with V0, V3 t=2 smoothed cold ≈ 0.9685,
   V4 prob ≈ 3.83e-3).

5. **Cross-lab convention drift on per-function docstrings.** Spec
   §8.2 names "the docstring header" (singular) as readable. Lab 8's
   `compute_filtered`, `compute_smoothed`, `compute_backward`,
   `argmax` all carry their own short docstrings INSIDE the function
   body. Strict reading: an exam agent should NOT read these. In
   practice they will, and the variant bank effectively assumes they
   do (V3 leans on the MODE block which is in the header — fine —
   but `compute_backward` is described nowhere else). Coordinate
   with spec author on whether to (a) hoist per-function docstrings
   into the header KNOB blocks, or (b) explicitly amend §8.2 to
   allow per-function docstrings.

### What PM should do next

1. **Fix P1-1 immediately** — one-line correction to
   `variants.md` lines 76-79 about the last-step agreement
   condition. Most-impactful edit on this list. Delegate to whoever
   owns `study\_exam\Lab8-HMM\variants.md`.
2. **Fix P1-2 and P1-3** — add explicit "replace the whole list" and
   "two runs needed" sentences to V1 and V2 hints respectively.
   Both are one-line edits in `variants.md`.
3. **Fix P1-4 and P1-5** — clean up the MODE KNOB doc wording about
   which rows are printed, and align V3's expected-answer shape
   with the script's actual stdout format. One edit in the
   solution file, one in `variants.md`.
4. **Re-run the gate** (three exam agents in parallel, then
   reviewer round 2). After P1-1..P1-5 land, the variant bank
   should pass cleanly with all three agents reaching `SOLVED`.
5. **Defer P2-1..P2-8 to round 2 or later.** They are polish items;
   the gate can pass without them. P2-7 (per-function docstring
   spec drift) is the only one with cross-lab implications and
   should be raised with the spec author separately.
6. **Long-term**: add `study\_exam\Lab8-HMM\test_variants.py` (or
   equivalent harness) so the variant outputs are asserted
   automatically. Same recommendation as Lab4-GA round-1
   reviewer4.

**DOCUMENT.md updated:** N/A for QA.
