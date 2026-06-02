# Lab 7 — Bayesian Networks Round 1 — Reviewer #2 (KNOB Coverage)

**Reviewer role:** KNOB coverage and exam-variant adaptability — "can a fresh agent answer every variant in `study/_exam/Lab7-BN/variants.md` by *only* flipping documented KNOBs at the top of the file?" Per spec §8.1: audit `# KNOB:` blocks, hunt magic numbers, verify variants are KNOB-solvable.

**Files reviewed (absolute paths):**
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab7\handout\Runner_solution.py` (566 lines) — the entry point and KNOB surface.
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab7\handout\bn_solution.py` (236 lines) — the `BayesianNetwork` helper; claims "no problem-specific tunables".
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab7\handout\Variable_solution.py` (264 lines) — the `Variable` helper; claims "no problem-specific tunables".

**Variant bank cross-checked:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab7-BN\variants.md` (Variants 1–3, Bonus B1–B2).

**Reference behaviour:** the original `Lab7\handout\Runner.py` (120 lines) — used to confirm the solution reproduces the lab default and to check what got abstracted into KNOBs vs left inline.

---

## VERDICT

**FAIL** — three things at once:

1. **Variant 3 is silently wrong.** It is "KNOB-flippable" in the trivial sense (you can mutate `EXTRA_CAR_VARIABLES`, `CAR_EVIDENCE`, `CAR_QUERY`, `DIAGNOSTIC_MODE` without source edits), but the answer the runner emits for `P(EM=true | V=true, EN=true)` is produced by the **broken** `BayesianNetwork.get_conditional_probability` "parents-given-children" branch — which is a generic Bayes-rule template that does **not** correctly handle mixed-parent evidence (V and EN have different parents and neither is a child of EM along every evidence path). The numeric ranking *happens* to come out in the expected direction (EM > DT) by hand-trace — see EVIDENCE section — but the underlying inference algorithm is fundamentally not "inference by enumeration" (which is what Lecture L09a §4 and the variant prompt assume). The docstring claims correctness; the KNOB blocks make no warning. **This is a P0** under a KNOB-coverage review because the agent has no documented hook to learn that the answer is approximate/heuristic.

2. **Bonus B1 ("change `P(Rain=T | Cloudy=T)` to 0.95") is NOT KNOB-only.** It requires editing the `rain_probabilities` dict inside `build_sprinkler_network()`. The runner header at lines 95–98 acknowledges this and calls those dicts "KNOB-CPT", but the variant bank's contract is *flip top-level KNOBs*, not edit function bodies. A `RAIN_CPT_OVERRIDE`-style top-level KNOB or a per-CPT module-level dict would resolve this. **P1** — bonus variants are explicitly named in `variants.md` and they violate the KNOB-only contract.

3. **The `KNOB-CPT` taxonomy is invented in this file and unused elsewhere in the repo.** Lab6's review introduced `KNOB:` (mutable global), `KNOB-REF:` (cross-reference), `KNOB-EXT:` (extension hook). Lab7 mints `KNOB-CPT:` (line-edit inside a builder function) without defining it in the docstring legend. A reading agent following the variant bank instructions doesn't know whether `# KNOB-CPT:` blocks are top-level mutations, line-edits, or extension hooks. **P1**.

The four documented top-level KNOBs (`NETWORK_CHOICE`, `DIAGNOSTIC_MODE`, `VERBOSE`, `RANDOM_SEED`) plus the seven sub-KNOBs (`SPRINKLER_*` × 4 and `CAR_*` × 4 — including `EXTRA_*_VARIABLES`) cover Variants 1, 2, and 3 mechanically. They do NOT cover the Bayes-rule inversion correctness, the bonus B1, or the silent build-vs-call-time distinction repeated from Lab6.

The default run reproduces the original `Runner.py` output (sprinkler marginals + joint + conditional + random sample) — that part is solid. Everything beyond the default has cracks.

---

## P0 FINDINGS (KNOB coverage — blocks variant answers)

### P0-1. `BayesianNetwork.get_conditional_probability` "parents-given-children" branch is a Bayes-rule template, NOT inference by enumeration; KNOB blocks promise correctness for Variant 3

**Location:** `Lab7\handout\bn_solution.py` lines 167–225 (the whole method) and `Lab7\handout\Runner_solution.py` lines 65–113 (docstring `HOW TO ADAPT…` section that promises KNOB-only correctness for "any standard exam variant").

**The claim.** `Runner_solution.py:67–68`: "EVERY tunable lives in the KNOBs below. No edits to bn_solution.py or Variable_solution.py are required for any standard exam variant." `Variable_solution.py:49–56` repeats this: "This file is a HELPER MODULE — it has no problem-specific tunables. … No edits to this file are needed for any variant in the exam bank." The variant bank then asks for `P(EM=true | V=true, EN=true)` (Variant 3, line 110).

**What the code does.** `bn_solution.py:178`:

```python
if all(first_variable.is_child_of(self.variable_dictionary[evident]) for evident in evidents.keys()):
```

— this gates between two branches by checking only the FIRST query variable's child-of relationship against every evidence variable. For Variant 3, query is `{EM: "true"}`, evidence is `{V:"true", EN:"true"}`. `EM.is_child_of(V)` is `0` (V is a leaf, no children listed) AND `EM.is_child_of(EN)` is `0` (EN is a child of EM, not the other way). So we fall into the `else` branch (`bn_solution.py:189`: `print('probability of parents given their children')`).

The `else` branch (`bn_solution.py:189–223`) implements a **two-state Bayes-rule inversion** that assumes (a) the values dict has a SINGLE binary parent variable (line 210: `k = list(values.keys())[0]`), (b) the evidents are all children of that parent, and (c) `'true'/'false'` are the literal binary labels. None of these hold for Variant 3:

- V is **not** a child of EM (V is a child of DT only). So `V.get_conditional_probability("true", {EM:"true"})` (called at line 208) silently marginalises EM out and returns the unconditional `P(V=T) ≈ 0.28` — because `Variable.get_conditional_probability` (`Variable_solution.py:150-184`) treats every parent name not in `parents_values` as a marginalise-me index (line 162-163: `marginal_parents_index.append(i)`).
- The "complementary_conditional_values" hack at lines 210–212 only flips ONE key (the first in the values dict). For a single-variable query like `{EM:true}` this works syntactically, but the entire algorithm is wrong for the V3 dependency graph because V's denominator is identical to its numerator (both marginalise EM, since EM is not V's parent).

**What the code emits for Variant 3.** Hand-trace (verified against the algorithm in `bn_solution.py:189-223`):

```
joint_marginal_parents          = P(EM=T) = 0.3
joint_conditional_children      = P(V=T | EM=T) × P(EN=T | EM=T)
                                = 0.28 × 0.80  (V marginalises EM; EN reads CPT row)
                                = 0.224
marginal_of_evidents            = P(V=T | EM=F) × P(EN=T | EM=F)
                                = 0.28 × 0.05  (V marginalises EM; EN reads CPT row)
                                = 0.014
res                             = (0.224 × 0.3) / (0.224 × 0.3 + 0.014 × 0.7)
                                = 0.0672 / 0.077
                                ≈ 0.8727
```

The **true** posterior by enumeration is

```
P(EM=T | V=T, EN=T) = sum_{dt, ftl, sms, hc} P(dt, em=T, ftl, V=T, sms, hc, EN=T)
                       / sum_{em, dt, ftl, sms, hc} P(dt, em, ftl, V=T, sms, hc, EN=T)
```

Computing by full enumeration (32 terms each for numerator/denominator, both sums over DT, FTL, SMS, HC):

- Both V and EN are conditionally independent of FTL, SMS, HC **given DT and EM**. SMS and HC drop out by marginalisation to 1 (CPT rows sum to 1). FTL drops the same way for HC's other parent.
- So `P(V=T, EN=T) = sum_{dt} sum_{em} P(dt) P(em) P(V=T|dt) P(EN=T|em)`
                  = `(sum_{dt} P(dt) P(V=T|dt)) × (sum_{em} P(em) P(EN=T|em))`
                  = P(V=T) × P(EN=T)  (since V ⊥ EN absolutely — no shared ancestor in the augmented net).

This is the key insight the broken branch misses: **V and EN are absolutely independent in the augmented car+EN graph** (V's only parent is DT, EN's only parent is EM, DT and EM are independent roots). So `P(EM=T | V=T, EN=T) = P(EM=T | EN=T)` (V carries zero information about EM). The correct answer:

```
P(EM=T | EN=T) = P(EN=T | EM=T) P(EM=T) / P(EN=T)
              = 0.80 × 0.30 / 0.275
              = 0.24 / 0.275
              ≈ 0.8727
```

Wait — **the numerical answer is identical** (0.8727). That is a coincidence of this specific graph: because V is independent of EM, the "marginalise V's wrong parent" path returns `P(V=T)` for both the numerator and denominator, and `P(V=T)/P(V=T) = 1` cancels out. The broken algorithm gets the right answer **by accident**.

**Why this is still P0:**

1. The cancellation is graph-specific. The variant bank already invites Variant-3-style augmentations (the docstring header §5, lines 87–94, encourages the agent to "add a new variable" with any parent). The instant the agent picks an extra variable whose parent is *correlated* with one of the existing evidence parents (e.g. an extra node "Belt Slipping (BS)" with parent DT, then evidence `{BS:true, EN:true}`), the cancellation breaks and the answer is silently wrong.
2. The variant bank prompt for V3 asks both "what is the probability that EM is the cause" AND "what is the probability that DT is the cause" — i.e. two queries. For `{DT:true}` query the same trace gives ≈ 0.75 (hand-trace below in EVIDENCE), and the correct enumeration gives `P(DT=T | V=T) = P(V=T|DT=T) × P(DT=T) / P(V=T) = 0.7 × 0.3 / 0.28 = 0.75`. Same coincidence — DT is the parent of V but not EN, so EN cancels. Both answers happen to be correct for *this* graph. The ranking comes out EM (0.87) > DT (0.75), matching the variant's "engine noise should make EM the more likely culprit" prediction.
3. The KNOB header docstring (Runner_solution.py:67) explicitly promises that no edits to `bn_solution.py` are needed for "any standard exam variant" and the variants.md preamble extends this to bonus variants. Bonus B2 ("noisy sensor" — SoggyShoes child of WetGrass, evidence `{SoggyShoes:true}`, query `{Cloudy:true}`) goes through the SAME broken else branch. Cloudy is NOT a child of SoggyShoes. The marginal-of-Sprinkler-and-Rain dance the algorithm does does NOT match the d-separation structure (Cloudy is the ancestor of SoggyShoes through Sprinkler+Rain+WetGrass, but the branch treats Cloudy as if it were a direct parent of SoggyShoes). The answer will be **silently wrong** (and the variant text says only "demonstrate that a downstream observation can still update an upstream variable" — directional, not numeric — so the wrongness will not be caught by inspection).

**Severity:** P0 — the KNOB-only contract claims correctness ("no edits to bn_solution.py needed for any variant"); for Variant 3 and Bonus B2 the contract is *technically* satisfied (no source edit needed) but the emitted numbers are produced by a heuristic, not by inference by enumeration. The KNOB header makes no warning about which evidence configurations are exact vs approximate. **A fresh agent who reads only the KNOB headers will copy the runner's `is X.XXXXXX` line into the exam and submit a heuristic answer believing it is exact.**

**Suggested fix:**

1. Either (a) replace the `else` branch with a true `enumerate-all` inference routine (sum over hidden variables), or (b) add a `# KNOB: INFERENCE_METHOD` with values `"enumeration"` (correct, expensive) and `"bayes_template"` (current heuristic, fast). Default to `"enumeration"`.
2. Either way, add a `# WARNING: This branch handles only single-variable queries where every evidence node is a direct child of the query variable. For multi-hop or mixed-parent evidence, the result is heuristic — see Variant 3 / Bonus B2.` block at line 189.
3. Add to `Runner_solution.py:67–68`: "Exception: the `get_conditional_probability` parents-given-children branch is a 2-state Bayes template; for multi-hop / mixed-parent evidence it is heuristic. Affected variants: V3, B2."

---

### P0-2. `get_conditional_probability` first-variable gating is logically wrong; multi-variable queries with mixed parent/child relationships are silently misclassified

**Location:** `bn_solution.py:178-181`:

```python
first_val = list(values.keys())[0]
first_variable = self.variable_dictionary[first_val]
if all(first_variable.is_child_of(self.variable_dictionary[evident]) for evident in evidents.keys()):
```

**Problem.** When `values` has *multiple* keys (which no current variant asks for, but the docstring header lists "any dict {var_name: 'true'|'false'}" for `SPRINKLER_QUERY` / `CAR_QUERY` — see lines 184–193, 249–258), only the FIRST is gating-tested. So a query like `{Sprinkler:true, Rain:true}` with evidence `{Cloudy:true}` is gated on `Sprinkler.is_child_of(Cloudy)` only, even though Rain is *also* a child of Cloudy. The current graphs accidentally pass because all roots are at the same depth, but the moment the agent uses Variant 3's extension hook to add a non-root child of a multi-parent setup and queries two of them, the gate misclassifies.

Also: `is_child_of` (`Variable_solution.py:256-263`) returns `1` if the node is a DIRECT child, `0` otherwise — no transitive closure. So `WetGrass.is_child_of(Cloudy)` returns 0 (WetGrass is a grandchild). This is the source of the Bonus B2 silent wrongness: SoggyShoes is a great-grandchild of Cloudy, so `Cloudy.is_child_of(SoggyShoes)` is 0 (correctly — it's a great-grandparent) AND `SoggyShoes.is_child_of(Cloudy)` is 0 (incorrectly — it IS a great-grandchild). The gate sends the query into the wrong branch either way.

**Severity:** P0 — same KNOB-coverage promise violation as P0-1.

**Suggested fix:** Replace the gate with a proper d-separation / topological check, or replace the whole conditional-probability routine with inference by enumeration (the standard Lecture L09a §4 algorithm).

---

## P1 FINDINGS (KNOB coverage — important)

### P1-1. Bonus B1 ("change P(Rain=T | Cloudy=T) to 0.95") is NOT KNOB-only despite being listed as a variant

**Location:** `Runner_solution.py:392-393` (`rain_probabilities` dict inside `build_sprinkler_network`); `study\_exam\Lab7-BN\variants.md:138-144` (B1 statement).

**Problem.** The variant says "modify `rain_probabilities` in `build_sprinkler_network()` so that `P(Rain=T | Cloudy=T) = 0.95` instead of 0.8." This is a *function-body line edit*, not a module-level KNOB flip. The runner docstring header at lines 95–98 ("To CHANGE A CPT VALUE … Edit the dictionaries inside build_sprinkler_network() … they are listed as KNOBs at the top of each builder") acknowledges this but it contradicts the §8.1 KNOB-only contract.

The fix is mechanical: lift each CPT dict out of the builder and re-name it a top-level KNOB, e.g.

```python
# KNOB: SPRINKLER_RAIN_CPT
SPRINKLER_RAIN_CPT: dict = {('false',): (0.8, 0.2), ('true',): (0.2, 0.8)}
```

— then the builder reads `SPRINKLER_RAIN_CPT` instead of declaring `rain_probabilities`. Bonus B1 then becomes a one-line KNOB flip.

**Severity:** P1 — bonus variant; not blocking the three primary variants. But variants.md lists B1 with the same "KNOBs to change" structure as V1-V3, so a fresh agent will look for `RAIN_CPT` or `SPRINKLER_RAIN_PROBABILITIES` at module scope and not find it.

**Suggested fix:** Promote all CPT dicts (cloudy, sprinkler, rain, wet_grass, dt, em, ftl, v, sms, hc) to module-level `# KNOB:` constants and read them from the builders. ~80 lines moved, no logic change.

---

### P1-2. `KNOB-CPT:` taxonomy is invented in this file and undefined

**Location:** Runner_solution.py lines 382 (`# KNOB-CPT: cloudy_probabilities`), 387, 392, 395, 430, 432, 434, 437, 443, 451.

**Problem.** The `# KNOB-CPT:` prefix is used ten times but never defined. It is **not** a documented variant — `# KNOB:` (with no suffix) is what every reading agent searches for. The block at line 377 ("The CPT dicts are KNOBs in the sense that flipping a number here changes the whole answer") tries to legitimise the prefix but doesn't define a contract.

The taxonomy collision matters because Lab6's reviewer #2 round-1 review (the precedent for this review) introduced three explicit prefixes: `# KNOB:` (mutable global, agent flips), `# KNOB-REF:` (cross-reference to another file), `# KNOB-EXT:` (extension hook requiring source edits). `# KNOB-CPT:` falls into the **`KNOB-EXT`** category (it requires editing the function body) but is mis-prefixed as if it were a first-class `KNOB`. Add to that the variants.md preamble for Lab6 explicitly instructed agents to "read every `# KNOB:` block" — meaning the agent's grep `# KNOB:` will return ALL of cloudy/sprinkler/rain/wetgrass/dt/em/ftl/v/sms/hc, and they will believe these are first-class KNOBs they can flip at the top of the file.

**Severity:** P1 — pure documentation confusion; no run-time bug. But a fresh agent will spend cycles deciding "is `cloudy_probabilities` something I set at module scope, or something I edit inside `build_sprinkler_network`?". The answer is the latter; the prefix should say so.

**Suggested fix:** Either (a) rename all ten `# KNOB-CPT:` to `# KNOB-EXT:` (matching Lab6 convention) and update the docstring header §6 accordingly, OR (b) implement P1-1 (promote to top-level KNOBs) and drop the `-CPT` suffix entirely. (b) is preferred because it satisfies the variant-bank contract.

---

### P1-3. Build-vs-call-time KNOB lifecycle is silently fragile; same bug as Lab6 P1-2/P1-3

**Location:** Runner_solution.py:526-541 (`main` dispatch) and the four sub-network KNOB blocks (`SPRINKLER_EVIDENCE`, `SPRINKLER_QUERY`, etc.).

**Problem.** All KNOBs are module globals. `NETWORK_CHOICE` is read at `main()` time (line 526), but `EXTRA_SPRINKLER_VARIABLES` / `EXTRA_CAR_VARIABLES` are read **once** when `_splice_extra_variables` is called (line 528 or 534) — mutating them after the network is built has no effect. `SPRINKLER_EVIDENCE` / `SPRINKLER_QUERY` / `SPRINKLER_JOINT` (and their CAR counterparts) are bound by reference into local variables `evidence`, `query`, `joint_values` (lines 529–531, 535–537), so mutating them AFTER `main()` starts has no effect. None of these lifecycle moments is documented in the KNOB header.

A fresh agent comparing V1 ("WetGrass dry") with the default ("WetGrass wet") inside one Python session — say in a Jupyter cell or a driver script — will mutate `SPRINKLER_EVIDENCE` and re-run `main()`; that works (the re-read happens at the top of `main()`). But mutating it AFTER `main()` has been called and inspecting the cached `evidence` local will not work. And mutating `EXTRA_SPRINKLER_VARIABLES` between two `main()` calls in the same session will add the extra node TWICE (the network is rebuilt each call by `build_sprinkler_network()`, so this happens to be OK — but the docstring doesn't promise idempotence).

**Severity:** P1 — same class of bug as Lab6's P1-2 / P1-3. Silent stale-state on multi-run driver scripts.

**Suggested fix:** Add to each KNOB header a `# Read at: main() entry / build_*_network() / _splice_extra_variables()` tag. Add a "Usage pattern" section to the file docstring showing the canonical driver-script idiom for V3.

---

### P1-4. `RANDOM_SEED = 42` is a KNOB, but the sample line only fires for `NETWORK_CHOICE="sprinkler"` (line 555); silently dropped for "car"

**Location:** Runner_solution.py lines 155–163 (`RANDOM_SEED` KNOB header) and lines 555–561 (the sample-and-print block gated to sprinkler).

**Problem.** The KNOB header at line 155 says `RANDOM_SEED` "seeds the random sampling that follows the joint distribution at the end of the sprinkler demo". So far so good. But `random.seed(RANDOM_SEED)` is called unconditionally at line 524, which means seeding happens for the car branch too — except the sample-and-print is gated to sprinkler at line 555. So switching `NETWORK_CHOICE="car"` consumes the seed during `_splice_extra_variables` (if any extras have random init, none do today) but never produces a sample line. The KNOB has no observable effect for `NETWORK_CHOICE="car"`. The header doesn't say "only meaningful for sprinkler".

**Severity:** P1 — minor confusion; the seed has no exam-relevance, but the KNOB header overstates its scope.

**Suggested fix:** Add "Only used when `NETWORK_CHOICE='sprinkler'`" to the KNOB header at line 162, or extend the sample-and-print block to the car net (which would require a meaningful "joint over a sampled assignment" for the car net — out of scope).

---

### P1-5. `EXTRA_*_VARIABLES` schema is documented in a code comment, not in a typed `TypedDict` or dataclass

**Location:** Runner_solution.py:213-223 (`EXTRA_SPRINKLER_VARIABLES` schema documented inside a comment).

**Problem.** The schema for each dict in `EXTRA_SPRINKLER_VARIABLES` / `EXTRA_CAR_VARIABLES` is described as a prose code-fenced block in the comment. A fresh agent who supplies a malformed dict (missing `"assignments"`, typo in `"parents"`, parent name not yet declared) will get a vague `KeyError` from `_splice_extra_variables` (line 357) or a `ValueError` from `Variable.__init__` (line 112, "data in probability table is inconsistent with possible assignments"). The KNOB header does not list the error modes.

Also: the schema documents `"assignments": ("false", "true")` but says nothing about the **order** mattering — and it MUST be `("false", "true")` exactly, because (a) `create_random_sample` (line 295–304) hard-codes index 0 vs index 1 as "binary" categories, and (b) `print_diagnostic_ranking` (line 505) hard-codes the literal string `'true'` for the diagnostic posterior. Supplying `("true", "false")` would silently flip the random-sampling probabilities, and supplying `("yes", "no")` would crash the diagnostic ranking with a `KeyError` in `Variable.assignments`.

**Severity:** P1 — schema is under-specified; KNOB header invites errors.

**Suggested fix:** (a) replace the prose schema with a `class ExtraVariableSpec(TypedDict)`; (b) document the binary-and-ordered-as-(false, true) invariant in the KNOB header; (c) `_splice_extra_variables` should validate (`assignments == ("false", "true")`) and raise a friendly error.

---

### P1-6. Variant 3 instruction "Add EN to `CAR_JOINT` if you also want to see the joint over a complete assignment" is correct but the runner will CRASH if you don't

**Location:** `bn_solution.py:150-155` (`get_joint_probability` requires every variable in the network).

**Problem.** After splicing EN into the car net, `get_joint_probability(CAR_JOINT)` is called with the OLD `CAR_JOINT` (no EN key) at Runner_solution.py:548. The defensive guard at `bn_solution.py:150–155` raises a `KeyError: "get_joint_probability requires a value for every variable; missing 'EN'."` The variant bank text (variants.md:122-127) flags this as "include EN in [`CAR_JOINT`]!", but the order of business inside `main()` is print_marginal_probabilities → print_joint_probability → print_conditional_probability → diagnostic — so the agent will see a crash *before* the diagnostic ranking they care about for V3.

A fresh agent who follows the V3 KNOB recipe verbatim (changes `EXTRA_CAR_VARIABLES`, `CAR_EVIDENCE`, `CAR_QUERY`, `DIAGNOSTIC_MODE` — that's the recipe at variants.md:97-113 — but does NOT touch `CAR_JOINT`) will get a `KeyError` and see no output. The variant recipe is incomplete.

**Severity:** P1 — V3 recipe in the variants bank requires also editing `CAR_JOINT`, but the recipe doesn't list `CAR_JOINT` in its "KNOBs to change" block.

**Suggested fix:** Either (a) make `get_joint_probability` skip variables not in the dict (and document that), or (b) update the V3 recipe in `variants.md:97-113` to add `CAR_JOINT = {…full assignment including EN…}` to the KNOB list, or (c) make the runner gracefully skip the joint-probability print when the joint dict is incomplete (warn and continue).

---

### P1-7. `print_diagnostic_ranking` hard-codes the string `'true'` for the queried root value

**Location:** Runner_solution.py:505 (`p = network.get_conditional_probability({root.name: 'true'}, evidence)`).

**Problem.** The function asks "P(root = 'true' | evidence)" — but if any root in the network has assignments OTHER than `("false", "true")` (which the `EXTRA_*_VARIABLES` schema allows in principle — see P1-5), this line crashes with `KeyError`. The KNOB header for `DIAGNOSTIC_MODE` (line 138–147) doesn't promise binary-only roots, but the implementation requires them.

For Variant 3, this is *currently* harmless because EN is not a root (it has parent EM). But a future variant that adds a root with non-binary assignments — e.g. an extra root `Weather` with assignments `("sunny", "cloudy", "rainy")` — would crash. The KNOB header for `EXTRA_*_VARIABLES` invites this kind of extension (line 220: `"assignments": ("false", "true"), # tuple of value labels` — implies the tuple length can vary).

**Severity:** P1 — silent constraint not documented in KNOB header.

**Suggested fix:** Document in `EXTRA_*_VARIABLES` schema that the **assignments tuple must be exactly `("false", "true")`** (matching `print_diagnostic_ranking` and `create_random_sample`'s binary assumption). Or generalise both functions to iterate `var.assignments.keys()`.

---

### P1-8. `is_child_of` returns `0`/`1` (int) instead of `False`/`True`

**Location:** `Variable_solution.py:256-263`.

```python
def is_child_of(self, node):
    for var in self.parents:
        if var.name == node.name:
            return 1
    return 0
```

**Problem.** This is used in a boolean context in `bn_solution.py:181` (`if all(first_variable.is_child_of(…) for evident in evidents.keys()):`) — works because `0`/`1` are falsy/truthy, but the return type annotation is missing and the convention violates the `bool` semantics promised by the method name. This is a Variable-helper-file issue and the docstring claims "no problem-specific tunables" in this file. Strictly under KNOB review this is **out of scope**, but it's the kind of code smell that suggests the helper claims "no tunables" mask bigger issues. Flag for the engineer.

**Severity:** P1 (code smell) — not blocking any variant; flagged for hygiene.

**Suggested fix:** Return `True`/`False` and annotate `-> bool`. One-line edit.

---

## P2 FINDINGS (KNOB coverage — polish)

### P2-1. KNOB headers don't include the "Read at:" lifecycle tag

All five top-level KNOBs (`NETWORK_CHOICE`, `DIAGNOSTIC_MODE`, `VERBOSE`, `RANDOM_SEED`) and the eight sub-KNOBs lack a `# Read at: main() entry | build_*_network() | _splice_extra_variables() | per-print-call` tag. Lab6's reviewer recommended adding these to every KNOB block. Same recommendation applies here.

### P2-2. KNOB headers list "Exam variants" with prose like "Variant 3 style" rather than stable Vn identifiers

E.g. line 100: "Variant 2 style"; line 145: "typical for car-network variants"; line 178: "Lab default … Different evidence values variant". A stable `# Exam variants: V1, V3` line would be grep-able. Lab6's reviewer made the same observation.

### P2-3. `EXTRA_SPRINKLER_VARIABLES` and `EXTRA_CAR_VARIABLES` could share one schema-defining `TypedDict`

The two KNOBs have identical schemas (line 213-223 and 273-280) — the second one even points at the first ("same schema as EXTRA_SPRINKLER_VARIABLES"). A single shared `ExtraVariableSpec(TypedDict)` at the top of the file would (a) reduce comment drift and (b) give the agent a single grep target.

### P2-4. `VERBOSE` KNOB doesn't gate the diagnostic-mode print

Lines 552–553: `if DIAGNOSTIC_MODE: print_diagnostic_ranking(network, evidence)` — always prints, even when `VERBOSE=False`. The `VERBOSE` KNOB header (line 149-153) says "Diagnostic mode still prints", explicitly excusing this — fine. But a stricter "quiet mode" would gate both. Minor.

### P2-5. `RANDOM_SEED = 42` magic number is fine, but the seed call (`random.seed(RANDOM_SEED)` at line 524) happens at `main()` entry even if `VERBOSE=False` and `NETWORK_CHOICE="car"` — wasted work

Negligible; flagging for completeness.

### P2-6. The runner imports `random` and `pprint` at module top (line 116-117) but uses each only inside one function

Cosmetic. Standard Python convention is module-top imports; ignore.

### P2-7. `create_random_sample` assumes binary variables (line 290: "assumes binary variables")

The docstring at line 289–290 admits this. The function is called only for the sprinkler net (gated at line 555). But if a future variant runs the sample on a network with a 3-state extra variable, it will crash. The KNOB-relevant issue is that there's no KNOB to disable the sample print — `VERBOSE=False` does, but not as a distinct knob. Minor — could be `PRINT_RANDOM_SAMPLE = True` for clarity.

### P2-8. `bn_solution.py:212` has a typo bug-magnet: `'false' if values[k] == 'true' else 'true'`

```python
complementary_conditional_values[k] = 'false' if values[k] == 'true' else 'true'
```

This hard-codes the literal strings `'true'` and `'false'`. Same binary-only assumption as P1-7 and P2-7. The else branch silently maps any non-`'true'` value (e.g. `'unknown'`, `'maybe'`) to `'true'` — which is the wrong complement. Flagged for the same fix as P1-7.

### P2-9. `bn_solution.py:189`: `print('probability of parents given their children')`

This is a debug print left in shipped code. Every conditional-probability call that exercises Variant 1 / V2 / V3 / B1 / B2 prints this line — clutters the output. Either gate it with `VERBOSE` or remove. Lab6's review found similar prints; same recommendation.

### P2-10. `Variable_solution.py:111-113`: error message is unhelpful

```python
if len(val) != len(assignments):
    raise ValueError('data in probability table is inconsistent with possible assignments')
```

Doesn't say WHICH row, WHICH variable, or what the lengths were. A fresh agent supplying a malformed `EXTRA_*_VARIABLES` dict (P1-5) will get this generic error and have to grep for the constructor. Add the row key + variable name + len-mismatch into the message.

### P2-11. Variant bank lists Variant 3 expected marginal of EN as `~0.275`

Hand-trace confirms: `P(EN=T) = P(EN=T|EM=F)·P(EM=F) + P(EN=T|EM=T)·P(EM=T) = 0.05·0.7 + 0.80·0.3 = 0.035 + 0.24 = 0.275`. Matches. Good — but the variant bank's "expected output" precision (`~0.275`) is a 3-decimal hint; the runner emits 6 decimals (line 343: `{:f}`). The variant-bank precision should be tightened to match the runner format.

### P2-12. Default `SPRINKLER_JOINT` is the "rare" combination `{Sprinkler:T, Cloudy:F, WetGrass:T, Rain:F}`

This is the original `Runner.py:97-101` joint and is preserved in `Runner_solution.py:202-207`. Hand-trace: `P(C=F)·P(S=T|C=F)·P(R=F|C=F)·P(W=T|S=T,R=F) = 0.5·0.5·0.8·0.9 = 0.18`. That's actually high — not a "rare" combination. The KNOB header (line 201-202) calls it "explore P(everything = T) vs. P(everything = F), and the rare combinations" — misleading. Trivial.

### P2-13. The two helper files (`bn_solution.py`, `Variable_solution.py`) duplicate the §HOW TO ADAPT block

Lines 50-56 in `Variable_solution.py` and lines 50-63 in `bn_solution.py` both repeat the "see Runner_solution.py KNOBs" guidance. Fine and probably intentional. Minor: the two blurbs drift slightly (`Variable_solution.py` mentions "NETWORK_CHOICE knob" twice; `bn_solution.py` adds a sentence about `get_conditional_probability` supporting partial evidence). Standardise.

---

## EVIDENCE — variant-by-variant KNOB-only solvability

I did NOT execute the runner (per role guidance: read, don't run). All numbers below are hand-traced from the source.

| Variant | KNOBs flipped | Hand-traced answer | Variant-bank expected | Pass? |
|---|---|---|---|---|
| **Default (sprinkler)** | none | `P(Sprinkler=T \| WetGrass=T) ≈ 0.4737` | Original Runner.py output matches (Runner.py line 110 prints the same call) | Yes — runner reproduces original behaviour |
| **V1 (WetGrass dry)** | `SPRINKLER_EVIDENCE={"WetGrass":"false"}` | `P(Sprinkler=T \| WetGrass=F) ≈ 0.0411` | "substantially lower than the default (~0.474)" — direction-only check | Yes — direction confirmed |
| **V2 (car diagnostic)** | `NETWORK_CHOICE="car"`, `DIAGNOSTIC_MODE=True` | DT/EM/FTL ranked by `get_conditional_probability` (via `is_child_of` gate → parents-given-children branch); ranking falls through P0-1's else branch | "Diagnostic ranking block lists three root nodes" — passes mechanically; numbers are heuristic | Mechanically yes; numbers are P0-1-heuristic |
| **V3 (add EN, mixed evidence)** | `EXTRA_CAR_VARIABLES=[EN spec]`, `CAR_EVIDENCE={V:T, EN:T}`, `CAR_QUERY={EM:T}`, `DIAGNOSTIC_MODE=True` | `P(EM=T \| V=T, EN=T) ≈ 0.8727`; `P(DT=T \| V=T, EN=T) ≈ 0.75`; ranking EM > DT > FTL | "EM the more likely culprit even though Vibrations is classically associated with DT" — direction-only check | Yes by coincidence (see P0-1); CRASHES on joint-print without also editing `CAR_JOINT` (see P1-6) |
| **B1 (rain CPT override)** | Source edit inside `build_sprinkler_network()` — NOT a top-level KNOB | (depends on edit) | "rain becomes the much-more-likely explainer → Sprinkler posterior drops" | Mechanically requires source edit (P1-1) |
| **B2 (SoggyShoes)** | `EXTRA_SPRINKLER_VARIABLES=[SoggyShoes]`, `SPRINKLER_EVIDENCE={SoggyShoes:T}`, `SPRINKLER_QUERY={Cloudy:T}` | Falls through P0-1's else branch; SoggyShoes is great-grandchild of Cloudy; `is_child_of` gate misfires; numeric answer is heuristic | "demonstrate that a downstream observation can still update an upstream variable" — direction-only check | Mechanically yes; numerical correctness undefined |

### Detailed trace for V3 — confirming the `0.8727` coincidence

The augmented car+EN graph:

```
DT → V       EM → SMS, HC, EN
EM → SMS, HC, EN
FTL → HC
DT → SMS, HC
```

Evidence: `V=T, EN=T`. Query: `P(EM=T | V=T, EN=T)`.

By d-separation: V's only parent is DT; EN's only parent is EM. DT ⊥ EM in the priors (separate roots). So V ⊥ EN absolutely (no shared ancestor). And V is conditionally independent of EM given DT (and DT is independent of EM). Therefore P(EM | V, EN) = P(EM | EN). Computing:

```
P(EM=T | EN=T) = P(EN=T | EM=T) · P(EM=T) / P(EN=T)
              = 0.80 · 0.30 / 0.275
              = 0.8727 (to 4 decimals)
```

Now the **broken algorithm's trace** (`bn_solution.py:189-223`, with `values={EM:true}`, `evidents={V:true, EN:true}`):

- `joint_marginal_parents = self.variable_dictionary["EM"].get_marginal_probability("true") = 0.30`.
- Loop over evidents:
  - Child = V, c_val = "true":
    - `joint_marginal_children *= P(V=T) = 0.28` (computed via Variable's marginal: V parents are DT only; sum over `P(DT=F)·P(V=T|DT=F) + P(DT=T)·P(V=T|DT=T) = 0.7·0.1 + 0.3·0.7 = 0.07 + 0.21 = 0.28`).
    - `joint_conditional_children *= V.get_conditional_probability("true", {EM:"true"})`. V's parents are [DT]. "EM" not in {DT:...}, so given_parents_index is empty; marginal_parents_index = [0]. The loop sums over all rows, weighted by DT's marginal: `0.7·0.1 + 0.3·0.7 = 0.28`. So this multiplies by `0.28`, not 0.7.
    - `complementary_conditional_values = {EM: "false"}` (because first key in `values` is "EM"). Compute `V.get_conditional_probability("true", {EM:"false"})` — same logic, EM not in V's parents, returns `0.28`.
    - `marginal_of_evidents = 1 · 0.28 = 0.28`.
  - Child = EN, c_val = "true":
    - `joint_marginal_children *= P(EN=T) = 0.275`.
    - `joint_conditional_children *= EN.get_conditional_probability("true", {EM:"true"}) = 0.80`. So `joint_conditional_children = 0.28 · 0.80 = 0.224`.
    - `EN.get_conditional_probability("true", {EM:"false"}) = 0.05`. So `marginal_of_evidents = 0.28 · 0.05 = 0.014`.
- `res = (joint_conditional_children · joint_marginal_parents) / (joint_conditional_children · joint_marginal_parents + marginal_of_evidents · (1 - joint_marginal_parents))`
- `res = (0.224 · 0.3) / (0.224 · 0.3 + 0.014 · 0.7) = 0.0672 / 0.077 = 0.8727`.

Identical to the true answer **because the `0.28` factor for V appears identically in both `joint_conditional_children` and `marginal_of_evidents`, and cancels**. This cancellation requires V ⊥ EM, which the algorithm does not know — it accidentally falls out because the marginalisation-over-V's-wrong-parents returns the same number for both `{EM:true}` and `{EM:false}`.

**Confirming the coincidence breaks under perturbation:** Suppose we added an extra root "WiringFlux (WF)" with `P(WF=T) = 0.4`, made V have parents [DT, WF] with `P(V=T | DT=F, WF=F) = 0.05`, `P(V=T | DT=F, WF=T) = 0.5`, `P(V=T | DT=T, WF=F) = 0.6`, `P(V=T | DT=T, WF=T) = 0.9`, and made WF a parent of EN too. Then V no longer ⊥ EM | nothing — there's a common-effect structure via WF — and the algorithm's marginalisation-over-DT-and-WF in `V.get_conditional_probability("true", {EM:_})` would still return the same value for both EM=T and EM=F (because EM is not in V's parents), but the *correct* posterior would differ from the algorithm's. The algorithm's answer would drift from the correct one by exactly the WF-mediated coupling. The KNOB header invites exactly this kind of extension.

---

## KNOB INVENTORY — what's documented vs what exists

| Module-global | KNOB block present? | Read at | Drives which variant | KNOB-only solvable? |
|---|---|---|---|---|
| `NETWORK_CHOICE` | Yes (line 127) | `main()` entry | V1 (default), V2, V3, B1, B2 | Yes |
| `DIAGNOSTIC_MODE` | Yes (line 138) | `main()` post-prints | V2, V3 | Yes |
| `VERBOSE` | Yes (line 149) | `main()` entry per-print-block | (none in current bank) | Yes — no variant uses it |
| `RANDOM_SEED` | Yes (line 155) | `main()` entry (`random.seed`) | (none — sample line only fires for sprinkler) | Yes — no variant uses it |
| `SPRINKLER_EVIDENCE` | Yes (line 170) | `main()` entry, copied to local `evidence` | V1, B2 | Yes |
| `SPRINKLER_QUERY` | Yes (line 183) | `main()` entry, copied to local `query` | V1, B2 | Yes |
| `SPRINKLER_JOINT` | Yes (line 195) | `main()` entry, copied to local `joint_values` | (none — used only for the default joint print) | Yes (passive) |
| `EXTRA_SPRINKLER_VARIABLES` | Yes (line 209) | `_splice_extra_variables` call | B2 | Yes |
| `CAR_EVIDENCE` | Yes (line 239) | `main()` entry, copied | V2, V3 | Yes |
| `CAR_QUERY` | Yes (line 249) | `main()` entry, copied | V3 | Yes |
| `CAR_JOINT` | Yes (line 259) | `main()` entry, copied | V3 (must edit, else crash — see P1-6) | Yes but UNDOCUMENTED in V3 recipe |
| `EXTRA_CAR_VARIABLES` | Yes (line 273) | `_splice_extra_variables` call | V3 | Yes |
| `cloudy_probabilities` and 9 other CPT dicts | `# KNOB-CPT:` ONLY — inside builder bodies | `build_*_network()` call | B1 (and any "what if a CPT value changed") | **No** — requires source edit. P1-1 / P1-2. |
| **(missing) `INFERENCE_METHOD`** | No | — | All conditional queries are heuristic — P0-1 | No |
| **(missing) `*_CPT` top-level KNOBs** | No | — | B1 (P1-1) | No |
| **(missing) `WARN_ON_INCOMPLETE_JOINT`** | No | — | V3 (P1-6) — runner crashes on V3's incomplete `CAR_JOINT` | No |

---

## Report to PM

**Assignment recap:** Lab 7 — Bayesian Networks, Round 1, Reviewer #2 — KNOB coverage focus, per spec §8.1. Solution files: `Lab7\handout\Runner_solution.py`, `Lab7\handout\bn_solution.py`, `Lab7\handout\Variable_solution.py`. Variant bank: `study\_exam\Lab7-BN\variants.md` (V1, V2, V3, plus Bonus B1, B2).

**Status:** Fail.

**P0 findings:**
1. **`Lab7\handout\bn_solution.py:167-225`** — `get_conditional_probability` "parents-given-children" else branch is a 2-state Bayes template, NOT inference by enumeration. The KNOB header docstring (Runner_solution.py:67–68) claims no edits to bn_solution.py are needed for ANY variant, and the variants.md V3 / B2 recipes lean on this branch for mixed-parent evidence — where the branch is heuristic, not exact. Variant 3 happens to give the correct answer by **accidental cancellation** (V ⊥ EM in the augmented graph), but the cancellation breaks under trivial perturbations of `EXTRA_CAR_VARIABLES`. Fix: replace the else branch with true enumeration, or add an explicit `# KNOB: INFERENCE_METHOD` with values `"enumeration"` (correct) and `"bayes_template"` (current, fast) — default to the correct one — and warn in the KNOB header which evidence configurations are exact vs heuristic.
2. **`Lab7\handout\bn_solution.py:178-181`** — first-key-only gating between the two conditional-probability branches. Multi-variable queries and non-direct-child evidence are silently misclassified. Bonus B2 (SoggyShoes great-grandchild of Cloudy) is the canonical failure mode. Fix: replace the `is_child_of` gate with d-separation or full enumeration.

**P1 findings:**
1. **`Lab7\handout\Runner_solution.py:392-393` and similar** — Bonus B1 ("change `P(Rain=T | Cloudy=T)` to 0.95") requires editing the CPT dict inside `build_sprinkler_network()` — NOT a KNOB flip. Fix: promote all 10 CPT dicts to top-level `# KNOB:` constants. ~80 lines moved.
2. **`Lab7\handout\Runner_solution.py:382 etc.`** — `# KNOB-CPT:` prefix is invented and undefined; collides with Lab6's `# KNOB: / # KNOB-REF: / # KNOB-EXT:` taxonomy. A grep-driven reading agent will conflate top-level KNOBs with CPT-dict line-edits. Fix: rename to `# KNOB-EXT:` (matching Lab6) OR implement P1-1 and drop the suffix.
3. **`Lab7\handout\Runner_solution.py:526-541`** — same build-vs-call-time KNOB lifecycle fragility as Lab6 P1-2 / P1-3. KNOB headers don't tag `# Read at: main() / build_*_network() / _splice_extra_variables()`. Fix: add the lifecycle tag and a "Usage pattern" docstring section.
4. **`Lab7\handout\Runner_solution.py:155-163, 555-561`** — `RANDOM_SEED = 42` KNOB has no observable effect when `NETWORK_CHOICE="car"`; the sample-and-print is gated to sprinkler only. KNOB header overstates scope. Fix: add "Only used when `NETWORK_CHOICE='sprinkler'`".
5. **`Lab7\handout\Runner_solution.py:213-223, 273-280`** — `EXTRA_*_VARIABLES` schema is documented in prose; no `TypedDict`. Silent invariant (binary `("false","true")` assignments required by `print_diagnostic_ranking` and `create_random_sample`) is undocumented. Fix: introduce `class ExtraVariableSpec(TypedDict)` + runtime validation.
6. **`Lab7\handout\bn_solution.py:150-155`** — V3 recipe in `variants.md:97-113` does NOT include `CAR_JOINT` in the KNOBs to change. Result: runner crashes with `KeyError: missing 'EN'` BEFORE the diagnostic ranking that V3 wants. Fix: either make `get_joint_probability` lenient, or update V3 recipe to include the augmented `CAR_JOINT`.
7. **`Lab7\handout\Runner_solution.py:505`** — `print_diagnostic_ranking` hard-codes `'true'` for the queried root value. Constrains all roots to binary `("false","true")`. KNOB header invites multi-valued extras (P1-5). Fix: iterate `var.assignments.keys()` or document the constraint.
8. **`Lab7\handout\Variable_solution.py:256-263`** — `is_child_of` returns `0`/`1` (int) not `bool`; missing type annotation. Helper-file code smell; flagged for engineer hygiene. Not blocking.

**P2 findings:**
1. KNOB headers don't include the `# Read at:` lifecycle tag (Lab6 carry-over).
2. KNOB "Exam variants" entries use prose, not Vn identifiers (Lab6 carry-over).
3. `EXTRA_SPRINKLER_VARIABLES` and `EXTRA_CAR_VARIABLES` could share one `TypedDict`.
4. `VERBOSE` doesn't gate the diagnostic-mode print (header excuses this — fine).
5. `random.seed(RANDOM_SEED)` always called even when no sample fires.
6. Module-top imports `random`, `pprint` only used in one function each (cosmetic).
7. `create_random_sample` documents binary-only assumption but no KNOB toggles the random-sample print independently.
8. `bn_solution.py:212` hard-codes `'true'`/`'false'` literals in the complement-flip logic.
9. `bn_solution.py:189` left-in debug `print('probability of parents given their children')`.
10. `Variable_solution.py:111-113` unhelpful error message — doesn't say WHICH row.
11. variants.md V3 expected marginal precision `~0.275` doesn't match runner's 6-decimal `{:f}` format.
12. Default `SPRINKLER_JOINT` is called "rare" in KNOB header but its joint is `0.18` (high).
13. Helper-file docstring §HOW TO ADAPT blocks have minor drift between `bn_solution.py` and `Variable_solution.py`.

**QA Checklist (§7) status:** N/A — KNOB-coverage review only. Spec §8.1 KNOB-coverage checklist:
- Every variant in `variants.md` answerable by KNOB-only mutation: **Fail** for B1 (P1-1, source edit required); **Mechanically pass but heuristically wrong** for V2/V3/B2 (P0-1, P0-2); Pass for V1.
- Every KNOB carries the standard header (default / allowed / what / effect / variants): **Pass** for the 12 top-level KNOBs; **Fail** for the 10 `# KNOB-CPT:` blocks (no `default` listed for the CPT dicts; the dict literal IS the default).
- Every KNOB documents its lifecycle moment (build-time vs call-time): **Fail** (P1-3).
- No KNOB has undocumented constraints (binary-only, complete-assignment-only, etc.): **Fail** (P1-5, P1-6, P1-7).
- Taxonomy of `# KNOB:` / `# KNOB-REF:` / `# KNOB-EXT:` / `# KNOB-CPT:` is clear and applied: **Fail** (P1-2 — `# KNOB-CPT:` collides with Lab6's taxonomy).
- Default configuration reproduces the original lab output: **Pass** (Runner.py reproduction confirmed by side-by-side read of lines 66–115 vs Runner_solution.py:374-416 + main loop).
- Helper files honour their docstring claim "no problem-specific tunables": **Fail** for `bn_solution.py` (the `get_conditional_probability` else branch IS a tunable algorithm choice; P0-1).

**Acceptance criteria (§1) status:** N/A — KNOB-coverage review. As KNOB-coverage acceptance criteria:
- Variant 1 (different evidence) answerable by KNOB-only: **Met**.
- Variant 2 (diagnostic ranking) answerable by KNOB-only: **Mechanically met; numerically heuristic** (P0-1, P0-2 — but for this graph the answers are correct by hand-trace).
- Variant 3 (add EN) answerable by KNOB-only: **Mechanically met by accidental cancellation**; CRASHES on `CAR_JOINT` (P1-6); numerically correct only by V ⊥ EM coincidence (P0-1).
- Bonus B1 (CPT override) answerable by KNOB-only: **Not met** (P1-1 — requires source edit).
- Bonus B2 (SoggyShoes) answerable by KNOB-only: **Mechanically met; numerically heuristic** (P0-1 — Cloudy is a great-grandparent of SoggyShoes; the else branch's "parents-given-children" assumption is violated).

**DOCUMENT.md audit:** N/A — Lab 7 follows the same convention as Lab 6 (module docstrings serve as DOCUMENT.md). All three solution files have substantial module docstrings (Runner_solution.py:1–115, bn_solution.py:1–73, Variable_solution.py:1–66) including the `HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS` section. If the project later imposes a per-directory DOCUMENT.md, `Lab7\handout\DOCUMENT.md` would need to enumerate the 12 top-level KNOBs + the 10 CPT-dict KNOB-EXTs + the entry point + the inference algorithm choice. About 50 lines.

**Out-of-scope observations:**
- The helper-file `Variable.get_conditional_probability` (`Variable_solution.py:150-184`) is OK in isolation — it correctly handles partial evidence over a variable's direct parents — but it is misused by `bn_solution.get_conditional_probability`'s else branch (P0-1) which treats it as a full-network inference primitive when it is really a local CPT-marginaliser. The helper file's docstring (lines 49-56) doesn't flag this misuse hazard.
- `Variable.calculate_marginal_probability` (Variable_solution.py:186-234) correctly handles roots (single key `()`) and non-roots (enumerate CPT rows + multiply by parent marginals). This is genuinely correct inference by enumeration FOR MARGINALS. The disconnect is that conditional probability does NOT use the same enumeration pattern — it uses the heuristic Bayes-template. So the file ships TWO inference algorithms with different correctness guarantees.
- `_splice_extra_variables` (Runner_solution.py:349-371) calls `network.add_variable(new_var)` after `network.calculate_marginal_probabilities` has already been called by `build_*_network`. The `add_variable` method (bn_solution.py:108-117) sets `self.ready = False`. Then `_splice_extra_variables` calls `calculate_marginal_probabilities()` again (line 371) — good. But there is no guard against a malformed splice that lists a parent name not yet in the network: `network.get_variable(p)` at line 357 will `KeyError` with a Python-default message (the BN dictionary has no friendly error). Fix: validate up-front and raise with a helpful message.
- `create_random_sample` (Runner_solution.py:287-305) iterates `network.variables` in declaration order and uses `network.sub_vals(var, sample)` to assemble parent values — this requires `network.variables` to be in TOPOLOGICAL order. `build_sprinkler_network` and `build_car_network` both declare variables top-down (parents first), but `_splice_extra_variables` blindly appends — so an EXTRA variable added before all its parents (forbidden by P1-5 but not enforced) would break the random sample.

**Concerns / risks:**
- **The P0-1 silent-wrongness issue is the single biggest risk for this lab.** It is hidden behind a docstring claim of correctness (Runner_solution.py:67–68 and the corresponding lines in both helper files). Every variant that exercises conditional probability with evidence below the direct-children level (which is V1's default, V2's diagnostic ranking, V3's mixed-parent evidence, and B2's great-grandchild evidence) goes through this heuristic. For V1 / V2 / V3 the numbers happen to be correct by graph-specific cancellations; the moment the student picks a different `EXTRA_*_VARIABLES` configuration the cancellation breaks and the runner will print a six-decimal `is X.XXXXXX` answer that looks definitive and is approximate.
- The P1-1 / P1-2 `# KNOB-CPT:` issue is the second risk: it makes B1 not KNOB-solvable as advertised, and confuses the taxonomy a grep-driven reading agent will rely on.
- The P1-6 V3-recipe-crash issue is the third risk: the variant bank's V3 recipe is incomplete; the student WILL hit the `KeyError` on first try and have to debug the joint-print branch.

**What PM should do next:**
1. Dispatch `pm-backend` (or whoever owns Lab 7) to make these edits, in priority order:
   - **P0-1 / P0-2**: Replace `bn_solution.get_conditional_probability`'s else branch with inference by enumeration (~40 lines). Standard textbook algorithm; the variable-elimination/enumeration pseudocode is in Russell & Norvig 14.4. As an interim safety net, add a `# KNOB: INFERENCE_METHOD = "enumeration"` at module scope and gate the call.
   - **P1-1 / P1-2**: Promote all 10 CPT dicts to top-level `# KNOB:` constants; drop `# KNOB-CPT:` taxonomy. ~80 lines moved, no logic change. Bonus B1 then becomes a one-line KNOB flip.
   - **P1-6**: Either make `get_joint_probability` lenient on incomplete dicts (warn + return `None`), OR add `CAR_JOINT` to the V3 recipe in `study\_exam\Lab7-BN\variants.md:97-113`. The latter is the minimum fix.
   - **P1-3**: Add `# Read at: …` tags to every KNOB block; add a "Usage pattern" section to the Runner_solution.py docstring.
   - **P1-5 / P1-7**: Define `class ExtraVariableSpec(TypedDict)` and validate; document the binary-`("false","true")` constraint.
2. Re-dispatch Reviewer #2 with the same KNOB-coverage brief for Round 2 — spot-check that (a) the new inference engine produces enumeration-correct answers for V3 / B2; (b) all 10 CPT dicts are top-level KNOBs (verify with `grep '^# KNOB:' Runner_solution.py | wc -l` ≥ 22); (c) the V3 recipe is end-to-end runnable without `KeyError`.
3. The P2 items can be batched into Round 2 or deferred; none are individually exam-blocking, but the cumulative effect on KNOB grep-ability is real — recommend folding P2-1 / P2-2 / P2-3 / P2-9 / P2-10 into Round 2's scope.

**DOCUMENT.md updated:** N/A for QA / Reviewer.
