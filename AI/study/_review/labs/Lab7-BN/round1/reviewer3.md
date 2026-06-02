# Lab7-BN — Reviewer #3 (Pedagogical Clarity), Round 1

**Reviewer role:** Lab Reviewer #3 — Pedagogical Clarity. I am NOT checking
correctness of the math, function signatures, or whether the engine runs
(those are #1 / #2). I am checking whether a student preparing for the AI
exam can read these solutions and *learn from them* — whether the docstrings,
WHY comments, MENTAL-MODEL framing, and lecture-alignment match what
`study/lectures/L09a-Bayesian-Networks.md` actually teaches, and whether
the prose answers the questions a confused student would ask at exam
pressure.

**Spec reference:** §8.1 (pedagogical clarity rubric).

**Assignment recap:** Review the Lab7-BN solutions for pedagogical clarity
against the L09a lecture.

**Files inspected (absolute paths):**

- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab7\handout\bn_solution.py`        (236 lines)
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab7\handout\Variable_solution.py`  (264 lines)
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab7\handout\Runner_solution.py`    (566 lines)

**Cross-checked against (diff context / canonical material):**

- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab7\handout\bn.py`            (handout template)
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab7\handout\Variable.py`      (handout template)
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab7\handout\Runner.py`        (handout template)
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L09a-Bayesian-Networks.md`
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab7-BN\variants.md`

**Status:** **Fail — Pass with concerns at best.** The headline docstrings
are competent (better than Lab 6's) and the gossip-graph analogy is
consistently echoed from L09a §2. But the *body* of every file is largely
inherited template code with no WHY comments at exactly the lines that
confuse students; the conditional-probability implementation in
`bn_solution.py` is mathematically wrong-by-design AND undocumented as
such; and the lecture-alignment lies in two places (Markov condition,
inference by enumeration) — the docstrings claim concepts the code does
not demonstrate. A student studying this solution will leave with a
*fragile* understanding of BN inference at best and an *actively
miscalibrated* understanding of `get_conditional_probability` at worst.

---

## P0 Findings (broken pedagogy / actively misleading)

### P0-1. `get_conditional_probability` in `bn_solution.py` is not inference by enumeration, lies about its assumptions, and contains a debug `print` left in

**Location:** `bn_solution.py:167–225` (the entire `get_conditional_probability` method); the docstring at L168–174; the live `print('probability of parents given their children')` at L190.

**Problem.** The lecture's *entire* §3.13 / §4.4 section sells **inference
by enumeration** as the canonical exact-inference algorithm: write the
query in terms of the joint, sum over hidden variables, normalise. The
lecture even forward-references Lab 7 explicitly at L09a §7 "Forward-
reference for Lab 7", line 1179 of the lecture:

> Implement inference by enumeration as in §4.4, including the
> normalisation step in §3.13.

The solution does **not** implement inference by enumeration. It
implements a special-case hack with two branches:

1. *"probability of children given their parents"* (L181–185): products
   of per-child `get_conditional_probability` calls, assuming every
   evidence node is a parent of every query node.
2. *"probability of parents given their children"* (L189–224): a
   bespoke Bayes-rule inversion that only works when (i) `values` is a
   single Boolean parent, (ii) `evidents` are direct children, (iii)
   the complement trick at L210–215 actually produces a meaningful
   denominator.

The docstring at L168–174 admits "I do not introduce advanced algorithms
for inference (e.g. junctions trees)" and "the joint probability of
children given their parents or the probability of parents given their
children" — but it does **not** warn the student that:

- The "parents-given-children" branch silently invokes a complement trick
  that assumes **binary** variables (L212: `'false' if values[k] == 'true' else 'true'`). For any non-Boolean variable, the answer is garbage.
- The denominator construction at L221–223 is **not Bayes' rule**. It
  reads `joint_conditional_children * joint_marginal_parents /
  (joint_conditional_children * joint_marginal_parents +
  marginal_of_evidents * (1 - joint_marginal_parents))`. The
  `marginal_of_evidents` variable is *itself* a conditional
  (L213–215 computes `get_conditional_probability(c_val, complementary)`)
  — so the denominator is conflating $P(\mathrm{evidence} \mid
  \neg\mathrm{cause}) \cdot P(\neg\mathrm{cause})$ with
  `marginal_of_evidents * (1 - joint_marginal_parents)`. This is the
  "total probability for the denominator" idiom of L09a §6.2 — but
  variable-named so badly that a student can't see the connection.
- The branch at L181–185 silently assumes that conditional probabilities
  over children are mutually independent given the evidence (L173:
  "assumption: variables in each level are independent, or independent
  given their parents"). The lecture (§3.6, §3.6 caveat) is explicit
  that this is the *Naive Bayes* assumption — not a property of the
  general BN. The docstring does not say "this branch is Naive-Bayes;
  the other branch is bespoke Bayes' rule". A student reads
  `BayesianNetwork.get_conditional_probability` and thinks "this is how
  BN conditional inference works" — it is not.

The docstring also makes no reference to the **inference-by-enumeration
recipe** of L09a §3.13, §4.4. There is no comment explaining "the
correct general algorithm is to sum the joint over hidden variables,
this implementation is a shortcut that only works on the sprinkler /
car network shape because…". The student walks away thinking this is
how BN inference is done in general.

**On top of the pedagogy:** the line `print('probability of parents
given their children')` at L190 is a leftover debug print that fires
on every call to the slower branch. This is not a "why" comment; it is
console-spam that will appear unexplained in every variant 2 / variant
3 examiner run.

**Pedagogical damage — catastrophic.** The lab's headline exam-relevant
deliverable IS inference. A student who runs Variant 1 ("dry grass →
sprinkler?") gets the right number for the wrong reason: the answer
comes out of the children-given-parents branch on a single-evidence,
single-query case where the bespoke formula happens to coincide with
Bayes' rule. The student then turns to the next exam problem (say, an
alarm-network query `P(+b | +j, +m)` like L09a §5.6) and either (a)
reuses this code and gets garbage, or (b) tries to re-derive inference
from scratch with zero scaffolding from the solution.

**Suggested fix.**

1. Either rewrite `get_conditional_probability` as the §4.4 enumeration
   algorithm — at minimum 30 lines, but well within scope — and delete
   the two-branch hack; or
2. Keep the hack but prepend a 40-line WHY comment explaining: (i) this
   is a shortcut, (ii) the *correct* general algorithm is inference by
   enumeration as in L09a §4.4, (iii) what specific network shapes the
   two branches assume, (iv) why the complement trick at L210–215 is
   binary-only, (v) why this code is **not** what the lecture means by
   "BN inference". Then map the formula at L221–223 onto Bayes' rule
   $P(C \mid E) = P(E \mid C) P(C) / P(E)$ symbol-by-symbol.
3. Either way: **delete the `print` at L190** and replace with a comment.

---

### P0-2. The MENTAL MODEL block contradicts the code: there is no chain-rule walk anywhere except `get_joint_probability`

**Location:** Module docstrings of `bn_solution.py:30–38`, `Variable_solution.py:28–36`, `Runner_solution.py:44–53`. All three repeat the gossip-graph analogy and explicitly invoke "chain rule of Bayesian networks (Lecture L09a §3 / §4)".

**Problem.** The chain rule + Markov condition factorisation is the
*centrepiece* of the lecture (§3.10, the boxed formula on slide 42 / page
504 of the lecture). The MENTAL MODEL blocks in all three files lean
hard on it — the `bn_solution.py` block actually walks the student
through "Cloudy says T, then Sprinkler says F (knowing Cloudy=T), then
Rain says T…" as the analogy for joint probability.

But **only one function in the codebase actually executes the chain
rule**: `BayesianNetwork.get_joint_probability` at L137–165. Everything
else — `calculate_marginal_probability` (Variable_solution L186–234),
`get_conditional_probability` (bn_solution L167–225, Variable_solution
L150–184) — uses a *different* derivation (sum-over-CPT-rows weighted
by parent marginals). A confused student who internalises the gossip-
graph picture and goes looking for the "for each node, multiply its
CPT entry" pattern finds it once, in `get_joint_probability`. The
other 200+ lines of inference code are doing something else, with no
MENTAL MODEL bridge explaining the discrepancy.

The lecture's §3.13 actually *does* tie these together: marginals are
the special case of the joint summed over all variables except one, and
inference by enumeration is the joint summed over hidden variables.
Both reduce to "multiply CPTs in topological order, then sum". The
solution implements both via a different recurrence (parent-marginals
times row-prob) without ever connecting it back to the chain-rule
mental model. The result: the student has *one* analogy in their head
and *two* unrelated code shapes in the file.

**Pedagogical damage.** Mental-model coherence is the headline
deliverable of Reviewer #3. A student who reads the docstrings sees
"this code is chain-rule + Markov". A student who reads the code sees
"this code computes marginals by an unexplained recurrence". The
docstring lies (by omission) about the code.

**Suggested fix.** Add a WHY comment at the top of
`Variable.calculate_marginal_probability` (L186) explaining:

> The marginal P(X = v) equals the joint summed over every other
> variable. By the BN factorisation (L09a §3.10), that joint is a
> product of CPTs in topological order. If we already know each
> parent's marginal (topological-order assumption, enforced by
> `BayesianNetwork.calculate_marginal_probabilities`), we can collapse
> the sum: for each row of this node's CPT, the probability of that
> parent-row is `prod_i parent_i.marginal(row[i])` and the contribution
> to `P(X = v)` is `row[v_idx] * prod_i parent_i.marginal(row[i])`.
> This is the chain-rule mental model — chain rule applied to one
> level of the gossip graph at a time.

The existing 8-line comment at L192–197 starts to do this but
hand-waves through the parent-marginal step. Make it explicit. Then
add a similar bridge comment to `get_conditional_probability` in both
files.

---

### P0-3. The "MARKOV CONDITION" — the single most important concept of L09a after the chain rule — is never named or explained anywhere in the solution

**Location:** Absent. Search all three `_solution.py` files for "Markov".
You will find it only in three places, all citation-only:

- `bn_solution.py:18` ("Markov condition" in PROBLEM STATEMENT prose).
- `bn_solution.py:142` (one passing mention in the WHY comment for `get_joint_probability`).
- `Variable_solution.py:43` (a glossary list entry).

The word never appears in any code comment that *explains* the
condition or links it to specific lines of code.

**Problem.** L09a §3.9 explicitly says "This is *the* assumption that
makes the network worth drawing." It is the foundation of:

- the BN joint factorisation (§3.10 derivation, Step 4);
- why `calculate_marginal_probability` can use parents-only as a
  conditioning set;
- why `get_probability` in Variable_solution.py L144–148 takes only
  `parents_values` (and not the entire prefix of the topological
  ordering).

The lecture also flags it as a §6 pitfall trap: students confuse
$X \perp Y$ with $X \perp Y \mid Z$ (L09a §6.6), and conditioning on a
collider creates *dependence* rather than independence (L09a §6.11,
"explaining away"). None of this appears in the solution. There is no
warning that the network's structure encodes a non-trivial conditional-
independence claim. There is no comment at the line `parents_values =
self.sub_vals(variable, values)` (bn_solution.py L161) saying "we use
*only* the parents, not the full prefix, because the Markov condition
guarantees that conditioning on parents is sufficient — this is L09a
§3.9".

**Pedagogical damage — severe.** A student studying for the exam
encounters the question "in a BN, is $X$ conditionally independent of
its grandparent given its parent?" (a textbook §3.9 question) and has
*nothing* in the solution to anchor the answer to. Worse, the student
encounters the explaining-away trap (§6.11) on the alarm network — a
canonical exam question per L09a §5.6 — and finds no warning anywhere
in the solution code that conditioning on a child of two parents
*increases* their mutual information.

**Suggested fix.** Add a 10-line comment block at the top of
`BayesianNetwork.get_joint_probability` (or in the module docstring of
`bn_solution.py`) explicitly naming the Markov condition, stating it
formally, and pointing to the lines of code that depend on it
(`sub_vals` at L228–235, `get_probability` at Variable_solution.py
L144–148). Add a separate comment block somewhere prominent (probably
the Runner docstring) warning about explaining-away: "if you condition
on a collider (e.g. WetGrass) the parents (Sprinkler, Rain) become
*dependent* — the gossip-graph analogy breaks down here, see L09a
§3.9.1 / §6.11."

---

### P0-4. The "WHY" comment on `calculate_marginal_probability` is decorative and skips the actual computation

**Location:** `Variable_solution.py:186–234`. Specifically the docstring/WHY at L192–197 and the body at L208–231.

**Problem.** The WHY block at L192–197 promises:

> in a Bayesian network the marginal P(X = v) is obtained by summing
> the CPT entry for value v across every parent configuration,
> weighted by the joint marginal of that parent configuration.

That's correct. But then look at L222–231: the code multiplies the
*per-parent marginals* (line 228: `parent.get_marginal_probability(row_key[i])`) to construct the "joint marginal of that parent configuration". **This is wrong in general.** The joint marginal of a
parent configuration is $P(\text{Parents} = \text{row})$, which equals
$\prod_i P(\text{Parent}_i)$ only if the parents are *marginally
independent*. They are not, in any BN with shared ancestors.

In the sprinkler net, Sprinkler and Rain share parent Cloudy. So their
joint marginal $P(\text{Sprinkler} = s, \text{Rain} = r)$ is **not**
$P(\text{Sprinkler} = s) \cdot P(\text{Rain} = r)$ — they are
positively correlated through Cloudy. The line at L228 silently
computes the *wrong* joint marginal.

I verified this matters: for the wet-grass marginal, the code computes

$P(\text{WG} = \text{true}) = \sum_{(s, r)} P(\text{WG} = T \mid s, r) \cdot P(\text{S} = s) \cdot P(\text{R} = r)$,

which uses **independent** marginals for S and R. The correct value is

$P(\text{WG} = \text{true}) = \sum_{c, s, r} P(\text{WG} = T \mid s, r) \cdot P(\text{S} = s \mid c) \cdot P(\text{R} = r \mid c) \cdot P(\text{C} = c)$.

For the lab's specific CPTs, these happen to be **numerically close
but not equal**. The students cannot detect this from the printed
output unless they re-derive by hand, which is exactly what L09a §4.2
asks them to be able to do.

**This may also be Reviewer #1's beat (correctness)** — but it is a P0
pedagogical issue because the WHY comment at L192–197 explicitly
**promises** "weighted by the joint marginal of that parent
configuration" and the code does **not** compute the joint marginal.
The comment is lying. A student trusting the comment will internalise
the wrong recurrence.

**Pedagogical damage — high.** This is the marginal-computation step
of every BN inference. The student takes this pattern away and applies
it to the alarm network (§5.6) or the lecture-late network (§5.7) and
gets numerically wrong answers, with no warning.

**Suggested fix.** Either:

1. Compute the marginal correctly via joint enumeration over **all**
   ancestors (cleanest, matches lecture §3.10 + §3.13 — and requires
   the §3.10 chain-rule walk that is missing); or
2. Acknowledge in the comment that this implementation **assumes
   parents are marginally independent** — which holds for chain
   networks but not for the sprinkler net's `Cloudy → {S, R}` fork —
   and add a worked example showing the numerical discrepancy on the
   sprinkler net.

Whichever fix is chosen, the comment at L192–197 must match the
code's actual semantics. As written, comment and code disagree.

---

### P0-5. `Variable.get_conditional_probability` (the partial-evidence helper) repeats the marginal-independence bug AND has no WHY comment at all

**Location:** `Variable_solution.py:150–184`.

**Problem.** Same bug as P0-4, in a different routine. The "marginal
parents" branch (L162–163, L179–181) multiplies `self.parents[mpi].get_marginal_probability(...)` to construct the marginal of
the un-given parents — again assuming they are independent, again
wrong when parents share ancestors.

But the worse pedagogical issue is that **this function has no WHY
comment at all** beyond the inherited template prose at L150–155.
There is no:

- statement of what mathematical operation this is computing
  (it's "marginalise out the un-given parents", but you won't know
  that from the code);
- citation back to L09a §3.13 (inference by enumeration);
- warning about the marginal-independence assumption;
- explanation of why "partial evidence over parents" is needed
  (because `bn_solution.py:181–185` calls it with the entire
  evidence dict, which may not be the complete parent set);
- linkage to the docstring header in `Variable_solution.py:50–57`
  that brags "already supports PARTIAL evidence over the parents
  of the queried node".

Compare to the careful, multi-paragraph WHY at `bn_solution.py:137–164`
(`get_joint_probability`). The asymmetry is glaring: the one function
that was a TODO in the handout gets a full WHY treatment; the other
function (which existed in the template) gets none.

**Pedagogical damage.** A student opening `Variable_solution.py` and
reading top-to-bottom hits a 35-line function with no explanation,
two cryptic loops, and a "what does `valid_row` mean?" naming
problem (L173). The student moves on without learning what partial-
evidence marginalisation is. Then the variant 1 question (dry-grass)
asks them to reason about exactly that, and they have no scaffold.

**Suggested fix.** Add the same 8-paragraph WHY treatment that
`get_joint_probability` enjoys. Map the routine line-by-line onto
"P(X = v | given) = sum over un-given parent configs of P(X = v |
parents=row) * P(un-given_parents = row | given)". Note the
marginal-independence shortcut (and its limits, per P0-4).

---

### P0-6. Three `_solution.py` files duplicate identical 50-line MENTAL MODEL / REFERENCES / HOW TO ADAPT blocks at the top — drowning the actual lesson

**Locations:**
- `bn_solution.py:1–73`     (73-line docstring header)
- `Variable_solution.py:1–66` (66-line docstring header)
- `Runner_solution.py:1–114` (114-line docstring header)

**Problem.** Combined header weight: **253 lines of prose before any
code**, across files whose total code length is ~700 lines. Worse,
the three MENTAL MODEL blocks (each ~10 lines) are *near-identical
gossip-graph analogies* — same metaphor, three times, with minor
phrasing variation. The HOW TO ADAPT block in Runner_solution.py
(L65–113) is **49 lines** of variant-knob instructions, longer than
any function in the file except the inference proper.

A student opening `Runner_solution.py` to learn how the lab's
exercise is wired must scroll past 114 lines before reaching `import
random` at L116. The actual main() entry point is at L523 — page 12
of the file in a normal editor. The pedagogical signal-to-noise
ratio is upside-down.

Lab 6 reviewer 3's report (P1-3 of that round) already flagged the
same issue. Lab 7 doubles down on it.

**Pedagogical damage.** Two distinct kinds:

1. **Information overload.** A student trying to grok BN inference
   has to wade through three slightly-different gossip-graph
   metaphors before reading a single line of code.
2. **The variant-knob manual is exam scaffolding, not a lesson.**
   `HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS` is useful to
   the *examiner* answering variant questions; it teaches the
   *student* nothing about Bayesian networks. It belongs in
   `study/_exam/Lab7-BN/variants.md` (which already exists and
   already covers the same material) — not in the solution file.

**Suggested fix.** Pick one file to host the canonical MENTAL MODEL
block (probably `Runner_solution.py` since it's the entry point) and
have the other two say "see Runner_solution.py for the mental model"
in two lines. Move the HOW TO ADAPT block out of the source code
entirely and into the existing variants file. Cap each module
docstring at ≤30 lines. Apply Lab 6's reviewer 3 P1-3 advice
retroactively.

---

## P1 Findings (important pedagogical / convention issues)

### P1-1. The `Runner_solution.py` Sprinkler ASCII diagram is wrong/misleading

**Location:** `Runner_solution.py:11–18`.

```
    Cloudy  (root, P(F)=P(T)=0.5)
      |  \
      v   v
    Sprinkler   Rain
        \     /
         v   v
        WetGrass
```

The diagram is *almost* right but it omits the WetGrass labelling
showing the direction of the arrows from Sprinkler and Rain (the
`\     /` line uses two slashes with no `v` indicators) — and the
backslash-escape produces ambiguous rendering inside Python source.
More importantly, the diagram does not mark *which arrow head goes
where*: a reader unfamiliar with the network might think Sprinkler →
WetGrass and Rain → WetGrass are *forks* of WetGrass, not *colliders*.
This matters: the WetGrass node is a textbook **collider** in
explaining-away territory (cf. L09a §3.9.1, §6.11). The
solution should *call this out* to set up understanding of why
`SPRINKLER_EVIDENCE = {"WetGrass": "true"}` re-couples Sprinkler and
Rain (which are independent given Cloudy alone).

**Suggested fix.** Annotate the diagram: "Cloudy is a fork (→ S, → R);
WetGrass is a collider (S →, R →). Conditioning on WetGrass induces
dependence between S and R via explaining away (L09a §3.9.1)."

---

### P1-2. The "HOW TO ADAPT" docstring's KNOB list inconsistently overlaps with the actual KNOB comments in the body

**Location:** `Runner_solution.py:65–113` (the meta-list) vs.
`Runner_solution.py:127–280` (the actual KNOB comments).

The header list at L70–113 enumerates seven adaptation paths (network
choice, evidence, query, joint, extra variables, CPT values,
diagnostic mode). The body has KNOB comments for **eleven** distinct
named knobs (NETWORK_CHOICE, DIAGNOSTIC_MODE, VERBOSE, RANDOM_SEED,
SPRINKLER_EVIDENCE, SPRINKLER_QUERY, SPRINKLER_JOINT,
EXTRA_SPRINKLER_VARIABLES, CAR_EVIDENCE, CAR_QUERY, CAR_JOINT,
EXTRA_CAR_VARIABLES, plus the KNOB-CPT entries in the builders).
Counts don't match. VERBOSE and RANDOM_SEED are not in the meta-list.
The meta-list's "1. switch network" / "2. evidence" / etc. numbering
implies *only seven paths exist*. A student who reads the header and
trusts the numbering will miss four knobs.

**Suggested fix.** Either (a) generate the meta-list from the actual
KNOB blocks (one source of truth), or (b) prune the meta-list to a
"see KNOB blocks below" pointer.

---

### P1-3. The "OUTPUTS WHEN RUN" claim in `Runner_solution.py` does not match the actual output

**Location:** `Runner_solution.py:104–108`.

The header says:

> Prints marginal probabilities of every node, the chosen joint
> probability, the chosen conditional probability, and (if
> DIAGNOSTIC_MODE is on) a ranked list of root-cause posteriors.

But for `NETWORK_CHOICE = "sprinkler"` and `VERBOSE = True`, the
runner ALSO prints `create_random_sample(...)`'s joint probability at
the very end (L555–561). The header gives no hint of this. A student
running the file and seeing a mystery second joint-probability line
("why is `WetGrass: true, Sprinkler: false, ...` printed twice?")
has nothing in the docstring to explain it.

The original `Runner.py` printed this for backward-compat; the
docstring should say so. The comment at L555–559 actually explains
this in code-comment form, but the *header* section that's supposed
to be the "what does this print?" reference does not mention it.

**Suggested fix.** Add one line: "For NETWORK_CHOICE == 'sprinkler',
also prints the joint probability of a single random sample drawn
from the network — preserved from the original Runner.py for
backward compatibility (seed: RANDOM_SEED)."

---

### P1-4. `create_random_sample` is presented as "creates random sample" with no pedagogical framing — and is in fact the canonical *forward sampling* / *prior sampling* algorithm

**Location:** `Runner_solution.py:287–305`.

**Problem.** This function implements **prior sampling** from a BN
— a textbook approximate-inference primitive that L09a §3.13 flags
as "Approximate-inference techniques (likelihood weighting, MCMC,
variable elimination) are out of scope for this course but flagged
so you know what comes next." So *technically* out of scope. But the
function is right there in the file, computing a sample from the
joint by walking the topological order and rolling a uniform random
number against the CPT row for each node's parent values. That **is**
the prior-sampling algorithm, and the file does not name it.

The handout's original `Runner.py` (line 8–26) has the same
function, also unnamed. The `_solution.py` inherits the silence.
This is a missed teaching moment: the file could spend three lines
saying "this is *forward / prior sampling* — the simplest BN
sampling algorithm. The probability that this function returns
assignment $a$ equals $P(a)$ exactly, because each step samples
from the CPT row and the joint is the product. Not used by the
inference machinery above; printed only as a demo."

**Pedagogical damage.** Low-to-medium — the function is not on the
exam, but a student who *reads* the file will pick up the algorithm
unconsciously without ever learning its name. When they later see
"likelihood weighting" or "Gibbs sampling" they will not connect
those to this routine. (Bridge-to-L09b risk: HMM forward
algorithm shares some structure.)

**Suggested fix.** 3-line WHY comment at L287 naming the algorithm
("forward / prior sampling — L09a §3.13 calls this an
'approximate-inference technique' but only this one, drawing a single
unweighted sample from the joint, is in the lab"). Done.

---

### P1-5. `_splice_extra_variables` is documented but the connection to lecture material is fluff, not substance

**Location:** `Runner_solution.py:349–371`.

The docstring at L350–355 says:

> Why: lets exam-variant questions add a node ("Variant 3 — add a new
> variable") with no edits to the build function.

That's a tooling reason, not a lecture reason. The actual *pedagogical
content* of "add a variable" is L09a §4.1 — the slide-49 algorithm
for *building a BN* (choose variable, choose minimal parent set,
fill in CPT). The splice helper IS the runtime version of that
algorithm. The WHY comment should say so.

**Suggested fix.** Replace the existing comment with:

> Implements the variable-addition step of L09a §4.1 slide 49:
> "(1) Add node $X_i$ to the network. (2) Choose Parents($X_i$).
> (3) Fill in the CPT P($X_i$ | Parents($X_i$))." This helper does
> all three at runtime from a declarative spec; the order matters —
> parents must already exist (caller is responsible for topological
> declaration order).

---

### P1-6. `is_child_of` returns `0` / `1` (int), not `True` / `False` — and the docstring even calls it a "boolean"

**Location:** `Variable_solution.py:256–263`.

```python
def is_child_of(self, node):
    """ return boolean, indicating whether this Node is a child of a given
        Node
    """
    for var in self.parents:
        if var.name == node.name:
            return 1
    return 0
```

The function returns Python int `1` / `0`. The docstring says "return
boolean". Python conflates 0/1 with False/True at truthiness checks,
so the bug is invisible. But a student who studies the type signature
(none given) and writes `assert is_child_of(...) is True` will fail.

This is template-inherited (the original `Variable.py` has the same
pattern), so it's also P1-class because the solution preserves the
template's lie without flagging it.

**Pedagogical damage — low to medium.** A student learning Python
discipline alongside BN concepts picks up the wrong idiom. Easy fix.

**Suggested fix.** Return `True` / `False`; update no callers because
truthiness checks still work; remove "return boolean" → "return bool"
in docstring (already correct intent).

---

### P1-7. The KNOB-CPT comments in `build_sprinkler_network` use the row-ordering convention `(false, true)` for the row key but the tuple values `(F-prob, T-prob)` — and never warn the student that mixing these up silently produces wrong answers

**Location:** `Runner_solution.py:382–401` (sprinkler), L437–461 (car).

The comment at L387–390 says:

> KNOB-CPT: sprinkler_probabilities
>   (false, true) rows are P(Sprinkler | Cloudy=F) and
>                  P(Sprinkler | Cloudy=T).

But the dict literal at L390 is `{('false',): (0.5, 0.5), ('true',): (0.9, 0.1)}` — i.e. the **key** is `('false',)` meaning Cloudy=F, and
the **value** is `(P(S=F | C=F), P(S=T | C=F)) = (0.5, 0.5)`. Two
tuples with *the same string values* but *different positional
semantics*. A student copy-pasting this for a new variant and writing
`('false',): (0.9, 0.1)` would produce a network where "given
Cloudy = false, P(Sprinkler = false) = 0.9" — flipping the prior.

There is no comment anywhere in the file warning about this. The
KNOB-CPT block is a knob, sure — but a knob with a footgun.

For the car network, the same pattern (and same footgun) is repeated
six times.

The CPT-ordering trap is also L09a §6.4 ("Reading the wrong direction
of a CPT"), specifically called out as "the single most common BN
error". The solution does not draw the line between the lecture's
warning and the code's representation.

**Suggested fix.** A 4-line comment at the top of the
`build_sprinkler_network` body explaining:

> CPT row-key convention: each tuple `(value,)` (or `(v1, v2, ...)`)
> in the dict key lists the parent values in *parent declaration
> order*. The tuple value is the row, with positions matching the
> child's `assignments` tuple — here `('false', 'true')`, so
> position 0 is P(node = false) and position 1 is P(node = true).
> Swapping the two — a common bug — produces a perfectly valid CPT
> for the *complement* of the intended random variable.

---

### P1-8. The `multiply_vector_elements` helper at the top of `Variable_solution.py` is dead code

**Location:** `Variable_solution.py:72–78`.

```python
def multiply_vector_elements(vector):
    """ return the multiplication of the vector elements """

    def mult(x, y):
        return x * y

    return functools.reduce(mult, vector, 1)
```

Grep shows zero callers — neither in `Variable_solution.py` nor in
`bn_solution.py` nor in `Runner_solution.py`. The function exists,
imports `functools` (line 69) for its sake, and is never used.

This is inherited from the template (`Variable.py` L4-10), where it
is also unused. The `_solution.py` carries it forward without
comment.

**Pedagogical damage — low.** A student wondering "what does this
do? Where is it called?" finds no caller, no doc-link to lecture
material, no explanation. Cognitive overhead for zero gain.

**Suggested fix.** Delete the function and the `functools` import.
If something downstream actually depends on it (I don't think
anything does), add an `__all__` declaration or move it to a
clearly-marked "unused but kept for template-compat" section with
a deprecation comment.

---

### P1-9. The `print_diagnostic_ranking` function reuses `get_conditional_probability` (which is broken — P0-1) but presents itself confidently

**Location:** `Runner_solution.py:483–516`.

The function says:

> Each root probability is computed independently of the other
> roots' posteriors — this is the simple, per-root inversion of
> Bayes' rule the lecture covers (no junction trees).

But the per-root call at L505 (`network.get_conditional_probability({root.name: 'true'}, evidence)`) lands in the **"parents-given-children" branch** of
`bn_solution.py:189–224` — the bespoke Bayes-rule branch that
silently assumes binary variables, that uses an idiosyncratic
denominator construction, and that does not implement inference by
enumeration. So the diagnostic ranking is computed by *the broken
algorithm*. The docstring at L484–491 frames it as "the lecture
covers (no junction trees)" — but the lecture does **not** cover
this particular formula; the lecture covers inference by
enumeration.

Variant 2 of the exam bank (`variants.md` §Variant 2) leans on
exactly this output. If the underlying inference is wrong-by-design,
the printed ranking is unreliable on any non-sprinkler / non-car
variant the student tries.

**Suggested fix.** After fixing P0-1 (rewrite or document
`get_conditional_probability` honestly), update this function's WHY
comment to match. At minimum, the phrasing "the simple, per-root
inversion of Bayes' rule the lecture covers" should be
"the per-root computation; see `BayesianNetwork.get_conditional_probability`
for the caveats about what 'inference' actually means here (L09a
§3.13 covers the general algorithm; this implementation is a
shortcut — see WHY comment in `bn_solution.py`)."

---

### P1-10. Three different `false / true` string conventions coexist in the codebase with no rationale comment

**Location:** Throughout. Examples:

- `Variable_solution.py:212` uses lowercase strings `'false'`, `'true'` for assignment keys.
- `bn_solution.py:212` uses the same.
- `Runner_solution.py:181` mixes `"false"` / `"true"` (double-quoted) with the surrounding code's mostly single-quoted style.
- The lecture (L09a §5.6) uses `+a` / `¬a` notation; §5.7 uses bare `T` / `F`; the diagrams use `True` / `False`.

A student trying to map from the lecture's notation to the lab's code
has no Rosetta stone. The lecture's `+b` and the code's `"true"` are
the same thing; nothing in the solution says so.

**Pedagogical damage — low.** Cosmetic, but irritating when paired
with the variant questions that say things like "WetGrass = true"
without specifying string vs. boolean.

**Suggested fix.** Add a 5-line block at the top of `Runner_solution.py`
(or in the lecture-to-lab Rosetta in `study/_exam/Lab7-BN/variants.md`)
documenting: "Throughout this codebase, variable values are *strings*
"false" / "true" (lowercase). Lecture notation `+b` / `¬b` / T / F
all map onto this; the exam variants accept either form. Domain
support is binary only — see P0-1 caveat."

---

## P2 Findings (polish, suggestions)

### P2-1. The L09a §6.11 "explaining-away" trap is invisible in the solution

The most counter-intuitive concept of the lecture is **explaining
away** — conditioning on a collider creates dependence between its
parents. The sprinkler net has a textbook collider (WetGrass with
parents Sprinkler, Rain). The default `SPRINKLER_EVIDENCE =
{"WetGrass": "true"}` and `SPRINKLER_QUERY = {"Sprinkler": "true"}`
together *demonstrate* explaining-away in action (knowing it's wet,
the probability the sprinkler explains the wetness depends on
whether Rain also fired).

But the code never points this out. A 6-line comment in the runner
saying "the default Sprinkler query is the textbook explaining-away
example — see L09a §3.9.1 / §6.11 / §5.6 for the alarm-network
counterpart" would do enormous pedagogical work for zero code
volume.

### P2-2. The phrase "junctions trees" (sic, plural) at `bn_solution.py:170` is a typo and the only mention of an advanced algorithm anywhere

Either "junction tree" (singular, standard CS term) or "junction-tree
algorithm" (qualified). "Junctions trees" is neither. Minor, but the
file goes to lengths to cite lecture references and then drops the
ball on the *single* mention of an out-of-scope algorithm.

### P2-3. The `ENTRY POINT: yes / no` line in the docstrings (e.g. `bn_solution.py:70-72`, `Variable_solution.py:63-65`) is novel and useful but inconsistently formatted

The cap-followed-by-colon convention reads like a section header but
the content is one line. Either commit to it as a real section
(with the value on the next line, padded) or inline it
("**Entry point.** No — this is a helper module.")

### P2-4. The `sub_vals` helper has a WHY comment but it does not explain *why a tuple* (vs a list)

`bn_solution.py:228–235`. The function returns `tuple(sub)` because
the CPT keys are tuples (Python dicts can only use hashable keys; a
list isn't hashable). The comment at L229–231 explains "all the
relevant assignments" but doesn't motivate the tuple choice. A
student reading "return a tuple, contain all the relevant
assignments" wonders why not a list. One sentence ("Returns a tuple
— dict keys must be hashable, and Python tuples are.") fixes this.

### P2-5. `Variable_solution.py:103–106` constructs `self.assignments` as `dict[str, int]` mapping value → index, which is clever but unexplained

A student reads:

```python
self.assignments: dict[str, int] = {}
for i in range(len(assignments)):
    self.assignments[assignments[i]] = i
```

…and wonders why it's a dict instead of a list. The answer is that
elsewhere (L148, L183) the code uses `self.assignments[value]` as
the column index into a CPT row, so the dict provides O(1) name→index
lookup. Worth a one-line comment.

### P2-6. The `ready` flag on both `BayesianNetwork` and `Variable` is documented but the *invariant* it protects (parents-must-be-ready-before-child) is not stated

The Markov-condition application in `calculate_marginal_probability`
*depends* on the parents' marginals being computed first
(Variable_solution.py L226–228). This is a topological-order
requirement. The comment at L223–225 says "topological-order
requirement, enforced by BayesianNetwork.calculate_marginal_probabilities"
— good — but `BayesianNetwork.calculate_marginal_probabilities`
itself (bn_solution.py L90–96) does not enforce topological order; it
just walks `self.variables` in list order. The invariant is enforced
by *the caller* (the `build_*_network` functions ordering vars
correctly), not by the BN class. The comment is mislocated.

### P2-7. Inconsistent docstring quoting and indentation

`bn_solution.py` docstrings use 3-double-quote style with body indented
inconsistently (e.g. L91–93 vs L108–110). Cosmetic.

### P2-8. The `pad` helper in `Runner_solution.py:308–311` is undocumented

It's a 3-line helper, but the surrounding code is heavily commented
elsewhere. One-line docstring ("Indent every line of `string` by
`pad` spaces; used to format pretty-printed dict output.") would
restore consistency.

### P2-9. The car network docstring promises root-cause diagnosis but `CAR_QUERY` default is `{"DT": "true"}` — a single-root query, not a comparative one

Variant 2 of the exam bank asks "which root cause is most likely?"
That's the `DIAGNOSTIC_MODE = True` path, not the `CAR_QUERY` path.
The default `CAR_QUERY = {"DT": "true"}` answers "what's the
probability DT is broken?" — useful, but not the homework question.
A 2-line comment at L257 saying "for the actual 'which root?'
diagnostic, set DIAGNOSTIC_MODE = True and ignore this knob" would
help.

### P2-10. The lecture cross-references all point to L09a but the lab itself sits at the boundary between L09a and L09b — and there's no forward pointer

The lecture-late example (L09a §4.1) and the alarm network (§5.6) are
both BN exam staples but the lab covers neither. The Bonus stretch
variants (B1, B2 in `variants.md`) start to compensate by suggesting
"a noisy sensor" — close to HMM territory (L09b). A pointer in the
solution to "L09b will reuse this scaffolding for sequential
observation" would frame the lab properly.

---

## Lecture-Alignment Audit (does the solution teach what L09a promises?)

| Lecture concept | L09a reference | Solution coverage | Verdict |
|---|---|---|---|
| Random variable, atomic event, domain | §3.1, §3.2 | `Variable.__init__` parameters | OK |
| Joint distribution & spreadsheet analogy | §2 "master spreadsheet", §3.2 | `get_joint_probability` WHY at bn_solution.py L137–147 | OK — best block in the codebase |
| Marginal "sum-out" projection | §2 "project the spreadsheet", §3.2 | `calculate_marginal_probability` body | **BROKEN by parent-marginal independence assumption** (P0-4) |
| Conditional probability + select-then-renormalise | §2 "restrict to one office", §3.3 | `get_conditional_probability` in both files | **BROKEN — not the algorithm the lecture teaches** (P0-1, P0-5) |
| Bayes' rule + total-probability denominator | §3.3 boxed, §6.2 trap | `get_conditional_probability` parents-given-children branch | half-broken — implementation present, formula mismatched, no comment ties to lecture (P0-1) |
| Chain rule | §3.3, §3.10 | `get_joint_probability` body | OK |
| Independence vs conditional independence | §3.5, §3.6 | Not addressed in code or comments | **MISSED TEACHING** (no warning, no example) |
| Bayesian network = DAG + CPTs | §3.7 | `BayesianNetwork` + `Variable` classes | OK structurally — diagram in runner is ambiguous (P1-1) |
| CPT row-sum-to-1, row-by-parent-combo | §3.8 | `probability_table` validation at Variable_solution.py L109–112 | OK — but value/row-key footgun unwarned (P1-7) |
| **Markov condition** | §3.9 | Cited 3× by name; **never explained** in any code comment | **MAJOR GAP** (P0-3) |
| Three connection patterns: chain / fork / **collider** | §3.9.1 | Sprinkler net IS a fork + collider; the solution never names this | **MISSED TEACHING** (P2-1) |
| **Explaining away** | §3.9.1, §6.11 | Default query exhibits it; never pointed out | **MISSED TEACHING** (P2-1) |
| BN factorisation as joint product | §3.10 | `get_joint_probability` WHY block | OK |
| Naive Bayes | §3.11 | Out-of-scope, but the "children given parents" branch SILENTLY assumes Naive-Bayes-style independence | undocumented (P0-1) |
| Inference by enumeration | §3.13, §4.4 | NOT IMPLEMENTED — see P0-1 | **BROKEN — the lab's headline deliverable is wrong-by-design or wrong-by-documentation** |
| Forward / prior sampling | §3.13 footnote ("out of scope") | `create_random_sample` IS prior sampling, unnamed | minor (P1-4) |
| Approximate inference is out of scope | §3.13 | Acknowledged in `bn_solution.py:170` ("junctions trees [sic]") | half-OK — typo, no actual link |

**Net pedagogical verdict.** The solution scores well on the *headline
docstrings* and the joint-probability function (the single TODO that
the engineer actually completed for this lab). It scores poorly on
*every other concept* the lecture promised: marginals are computed via
a wrong assumption, conditionals don't use the lecture's algorithm,
Markov condition is name-dropped without explanation, the
explaining-away trap is on the default page of output but never
called out. A student who memorises `get_joint_probability`'s
WHY block walks away with one good idea; a student who memorises
anything else walks away miseducated.

---

## Concerns / Risks

1. **Pre-existing template bugs preserved without comment.** The
   `get_conditional_probability` two-branch hack (P0-1), the
   marginal-independence assumption in `calculate_marginal_probability`
   (P0-4), the dead `multiply_vector_elements` helper (P1-8), the int
   1/0 in `is_child_of` (P1-6), the silent CPT-row-key footgun (P1-7)
   — all inherited from the handout template and *not* flagged in the
   solution. A student studying this assumes everything they read is
   intentional pedagogy.
2. **Pedagogical liability concentrates in the conditional-probability
   code.** Three of the six P0 findings are about
   `get_conditional_probability` (P0-1, P0-2, P0-5). The variant bank
   (`study/_exam/Lab7-BN/variants.md`) puts five questions through
   this code path. Fix this function or rewrite the variants to avoid
   it.
3. **The MENTAL MODEL block is well-crafted but oversold.** All three
   docstrings claim the gossip-graph analogy explains the code; in
   fact it explains *one function* (the joint). The other inference
   routines use a different mathematical structure that the analogy
   doesn't cover.
4. **There is no DOCUMENT.md anywhere.** Lab 6 reviewer 3 also flagged
   missing DOCUMENT.md. The convention isn't being followed.
5. **The lab is the bridge from L09a to L09b (HMMs).** Several
   concerns above — the marginal-independence bug (P0-4), the
   missing explaining-away framing (P2-1), the unnamed prior-sampling
   routine (P1-4) — propagate forward: a student who internalises
   these will struggle on the HMM lab too.

---

## What the PM should do next

1. **Dispatch the engineer to fix P0-1, P0-2, P0-3, P0-4, P0-5 first.**
   These five P0s are the difference between "a solution that teaches
   BN inference" and "a solution that runs but does the wrong thing
   under nice docstrings". P0-1 is the highest priority because it
   affects every variant question except the joint-probability ones.
2. **Decide whether `get_conditional_probability` is a rewrite or a
   well-documented shortcut.** A rewrite (inference by enumeration,
   ~30 lines) is the clean answer and matches the lecture. A
   documented shortcut needs ≥40 lines of WHY comment, plus warnings
   in the function header and in every caller (including
   `print_diagnostic_ranking`).
3. **Then address P1-1 through P1-10** — these are the difference
   between "correct code" and "code a confused student can learn
   from".
4. **Re-run Reviewer #3** after the P0 fixes. The lecture-alignment
   table above is the rubric: every "BROKEN" / "MISSED TEACHING" /
   "MAJOR GAP" row must move to "OK" before this solution is fit to
   ship as canonical study material.
5. **Do not proceed to App Tester until at least P0-1 is fixed.** The
   conditional-probability code path is exercised by variant questions
   that App Tester will run; the results will either spuriously pass
   (because the sprinkler-net shape happens to give numerically-correct
   answers in the children-given-parents branch) or fail in ways that
   won't reveal the real defect.
6. **Reconsider P0-6 (docstring-bloat) at the same time as the engineer
   is in these files anyway.** 253 lines of header prose vs ~700 lines
   of code is an inversion; cleanup is cheap during the same pass.

---

## Report to PM

**Assignment recap:** Lab Reviewer #3 (Pedagogical Clarity), Lab7-BN, Round 1. Reviewed `Lab7/handout/*_solution.py` against `study/lectures/L09a-Bayesian-Networks.md` per spec §8.1. Output deposited at `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_review\labs\Lab7-BN\round1\reviewer3.md`.

**Status:** **Fail.** Six P0 pedagogical defects (one of them — P0-1 — affects the lab's headline deliverable, conditional-probability inference). The docstrings and MENTAL MODEL blocks are well-written but the code does not honor them; the lecture's central concepts (Markov condition, inference by enumeration, explaining-away) are either name-dropped without explanation or absent entirely.

**P0 findings:**

1. **P0-1** — `bn_solution.py:167–225`. `get_conditional_probability` is not inference by enumeration (which L09a §3.13 / §4.4 / §7 explicitly says the lab will implement); it's a two-branch hack with undocumented assumptions, plus a leftover debug `print` at L190. **Fix:** rewrite as enumeration OR add a 40-line WHY comment explaining the shortcut and its limits; delete the print.
2. **P0-2** — Module docstrings of all three files. MENTAL MODEL claims gossip-graph / chain rule explain the code; only `get_joint_probability` actually uses the chain rule directly. The other inference routines use a different mathematical structure. **Fix:** add bridge WHY comments at `calculate_marginal_probability` and both `get_conditional_probability` methods.
3. **P0-3** — Markov condition (L09a §3.9, the structural foundation) is never named or explained in any code comment. **Fix:** add explicit comment block at `BayesianNetwork.get_joint_probability` and at `sub_vals` linking the parents-only conditioning to L09a §3.9, plus a warning about explaining-away.
4. **P0-4** — `Variable_solution.py:186–234`. `calculate_marginal_probability` multiplies parent marginals to construct "joint marginal of parents" — wrong when parents share ancestors (e.g. Sprinkler & Rain both have parent Cloudy). The WHY comment at L192–197 promises the correct algorithm; the code does not deliver it. **Fix:** recompute joint marginal via topological enumeration over ancestors OR add a comment honestly documenting the marginal-independence assumption.
5. **P0-5** — `Variable_solution.py:150–184`. `Variable.get_conditional_probability` (the partial-evidence helper) repeats the marginal-independence bug AND has no WHY comment. **Fix:** add the same 8-paragraph WHY treatment that `get_joint_probability` has; document the partial-evidence semantics.
6. **P0-6** — Headers of all three files combine to 253 lines of prose before any code (vs ~700 lines of code). HOW TO ADAPT meta-list duplicates `study/_exam/Lab7-BN/variants.md`. **Fix:** move HOW TO ADAPT to the existing variants doc; cap module docstrings at ≤30 lines; consolidate the MENTAL MODEL block in one file.

**P1 findings:**

1. **P1-1** Sprinkler ASCII diagram in `Runner_solution.py:11–18` is ambiguous about arrow direction and never identifies WetGrass as a *collider* (the conceptually critical pattern for explaining-away).
2. **P1-2** Header's HOW TO ADAPT meta-list (7 items) does not match body's actual KNOB count (11+).
3. **P1-3** "OUTPUTS WHEN RUN" docstring section omits the trailing random-sample print at L555–561.
4. **P1-4** `create_random_sample` IS prior sampling — neither named nor connected to L09a §3.13 footnote.
5. **P1-5** `_splice_extra_variables` docstring talks about exam tooling, not about L09a §4.1 slide-49 algorithm (the actual lecture material it implements).
6. **P1-6** `Variable.is_child_of` returns `1`/`0` (int); docstring says "boolean".
7. **P1-7** KNOB-CPT comments use "(false, true)" for both row keys and row values with no warning — silent footgun against L09a §6.4 (wrong-direction CPT).
8. **P1-8** `multiply_vector_elements` at top of `Variable_solution.py` is dead code, drags `functools` import along.
9. **P1-9** `print_diagnostic_ranking` calls into the broken `get_conditional_probability` (P0-1) while its docstring says "the simple, per-root inversion of Bayes' rule the lecture covers". Lecture does NOT cover the formula at bn_solution.py L221–223.
10. **P1-10** Three different `false/true` quoting / naming conventions coexist with no Rosetta from lecture notation.

**P2 findings:**

1. **P2-1** The L09a §6.11 explaining-away trap is *visible in the default output* but never called out.
2. **P2-2** Typo "junctions trees" at `bn_solution.py:170`.
3. **P2-3** `ENTRY POINT: yes / no` style is novel but inconsistently formatted.
4. **P2-4** `sub_vals` returns tuple — never explains *why a tuple* (hashable, for dict-key lookup).
5. **P2-5** `Variable.__init__`'s assignments-as-dict[str,int] is clever, unexplained.
6. **P2-6** The `ready`-flag topological-order invariant is enforced by the caller, not the class — comment at L223–225 mislocates the enforcement.
7. **P2-7** Inconsistent docstring quoting / indentation across the files.
8. **P2-8** `pad` helper at `Runner_solution.py:308–311` is undocumented in a heavily-commented file.
9. **P2-9** `CAR_QUERY` default doesn't match what Variant 2 of the exam bank actually asks for.
10. **P2-10** No forward pointer from the lab to L09b (HMMs), where this scaffolding gets reused.

**QA Checklist (§8.1 pedagogical-clarity items) status:**

- Docstrings present and frame the problem: **Pass with concerns** (oversized — P0-6).
- WHY comments at non-trivial code: **Fail** (present only in `get_joint_probability`; missing from `calculate_marginal_probability`, `get_conditional_probability` in both files, `print_diagnostic_ranking`, and `_splice_extra_variables` — P0-2, P0-4, P0-5, P1-5).
- MENTAL MODEL consistent with L09a: **Fail** (the analogy is honored only in `get_joint_probability`; other inference functions break the analogy without warning — P0-2).
- Lecture cross-references accurate: **Pass with concerns** (citations to §3, §4 are correct; but they're decorative — the corresponding *concepts* aren't drawn out in the code commentary — P0-3, P0-1).
- Headlines / module overview: **Pass** (the PROBLEM STATEMENT blocks are competent).
- Adaptation guidance (KNOBs): **Pass with concerns** (KNOB blocks are thorough; the meta-list at the top is inconsistent — P1-2; convention footgun unwarned — P1-7).

**Acceptance criteria (§1 Scope) status (from Reviewer #3 lens):**

- Implements joint probability per L09a §3.10: **Met** (`get_joint_probability` is correct and well-commented).
- Implements marginal probability per L09a §3.2: **Not met as a pedagogical artifact** — implementation has a marginal-independence assumption the lecture does not endorse (P0-4); WHY comment does not match code semantics.
- Implements conditional probability per L09a §3.13 / §4.4 (inference by enumeration): **Not met** (P0-1).
- Demonstrates BN concepts for exam variant bank: **Partial** — variants 1, 2, 3 each touch broken or under-documented code paths.

**DOCUMENT.md audit:** Absent from `Lab7/handout/`. The PM convention requires one per directory with new/modified files; the solution adds three modified files without a DOCUMENT.md. (Same finding as Lab 6 reviewer 3 — see that revise-summary.md.) — N/A in the strict sense because I'm Reviewer #3, but worth flagging.

**Out-of-scope observations:**

- The `pad` helper at `Runner_solution.py:308–311` exists in `Runner.py` already — preserving it makes sense for backward-compat but is undocumented (P2-8).
- The `multiply_vector_elements` dead-code (P1-8) also exists in the template; the solution carries it forward verbatim. If kept, it should be commented as "template-compat, unused".
- The `is_child_of` returning 1/0 (P1-6) is inherited from the template; the solution preserves the lie without flagging it.
- The "junctions trees" typo (P2-2) is inherited from the original `bn.py:71`. The solution faithfully reproduces the typo.

**Concerns / risks:**

1. Three of six P0 findings are about `get_conditional_probability`. Fix this function or the variant bank will break in pedagogically embarrassing ways.
2. The marginal-independence bug (P0-4) is the kind of mistake that "passes the visible test" (sprinkler-net marginals are *close* to right, not wildly wrong) but fails on harder networks (alarm net, lecture-late net). Reviewer #2 will need to actually compute the correct marginal by hand to detect this.
3. The solution is over-engineered relative to a teaching artifact (Lab 6 reviewer 3 saw the same pattern). Cap the docstring bloat now; the alternative is to apply the same fix to Lab 8 and so on, forever.
4. The lecture-to-lab Rosetta is silently missing (P1-10). When `study/_exam/Lab7-BN/variants.md` says "WetGrass = true", the student has to figure out it means `"true"` (lowercase string). Document the convention once.
5. The MENTAL MODEL is over-claimed: the docstrings sell a chain-rule mental model; the code uses three different mathematical structures. Pick one analogy per function or generalise the analogy to cover all three.

**What PM should do next:** Send the report back to the engineer with the six P0 findings prioritised. Specifically:

1. Fix P0-1 (`get_conditional_probability` — rewrite as enumeration OR document honestly). Highest impact.
2. Fix P0-4 (`calculate_marginal_probability` — marginal-independence bug or correct comment). Second highest.
3. Fix P0-5 (Variable.get_conditional_probability WHY comment).
4. Fix P0-3 (add Markov-condition comment block).
5. Fix P0-2 (add mental-model bridge comments at non-joint inference functions).
6. Fix P0-6 (docstring deduplication — move HOW TO ADAPT to variants.md).
7. Address P1 findings P1-1 through P1-10 in the same pass.
8. Then re-dispatch Reviewer #3 (me) for Round 2.

**Do not proceed to App Tester until P0-1 is fixed.** The conditional-probability code path is exercised by every non-joint variant; App Tester results will be unreliable until then.

**DOCUMENT.md updated:** N/A for QA / Reviewer #3.
