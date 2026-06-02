# Reviewer 4 — L09a Bayesian Networks — Round 1

**Role:** Lecture Reviewer #4 (Exam Readiness), Spec §7.1
**Source PDF:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture9-Bayesian Networks.pdf` (67 slides, content slides 1–66)
**Chapter under review:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L09a-Bayesian-Networks.md` (933 lines)
**Mode:** HARSH. Imagine 10 exam questions on BNs. Could a student who reads ONLY this chapter answer them?

---

## VERDICT

**Pass with Concerns.** The chapter is the strongest of the lecture series I have reviewed so far — wide coverage, derivations that go beyond slide-restatement, the gossip-graph and umbrella-rain analogies are durable, all six worked Bayes-rule and joint-entry calculations verify numerically, and the §5.8 walk-through of $P(R \mid T, \neg S)$ on the lecture-late network adds material the slides only sketched. A student who genuinely absorbs §3, §4 and §5 will pass an exam built on slides 1–66.

But the chapter has gaps that will cost exam marks. Most critically:

- **No d-separation explanation beyond a parenthetical** — slide 54 says "you can deduce many other conditional independence relations from a Bayes net", and the chapter punts on the question of how. The promised glossary entry does not exist in the chapter; it is a forward reference.
- **The "common-cause" / "common-effect" / "chain" trichotomy** (V-structure, fork, chain) is missing entirely — slide 41 explicitly shows a *fork* (Rain → Umbrella, Rain → Traffic) and slide 46 explicitly shows a *V-structure / explaining-away* (Burglary → Alarm ← Earthquake), but the chapter never names these patterns nor discusses that conditioning on a *common effect* makes parents *dependent* (the explaining-away direction). This is the single highest-yield BN exam topic and the chapter omits it.
- **Slide 48's explicit computation of $P(+b, -e, +a, -j, +m)$ is silently replaced** with the chapter's own different query, so a student who sits an exam asking "compute the slide-48 joint entry" gets no walk-through.
- **§3.11 Naive Bayes slide-29 worked example reproduces but does not explain** where the income column's Gaussian densities (0.0072 and $1.2 \times 10^{-9}$) come from — the chapter labels them "the value of the Gaussian density" but never shows the formula $\mathcal{N}(120 \mid \mu=110, \sigma^2=2975)$ that slide 29 expects the student to be comfortable with.

These are P1, not P0 — the chapter is largely correct. But each one is a probable exam-question class the student will lose marks on.

---

## P0 — MUST FIX (factually wrong / will lose exam marks)

### P0-1. §3.10 / §3.9 — "non-parent ancestors are non-descendants, hence conditionally independent" is **circular as written**

**Location:** L09a-Bayesian-Networks.md lines 345.

The derivation in §3.10 says:

> Combining the chain rule with the Markov condition collapses each chain-rule factor $P(X_i \mid X_1, \dots, X_{i-1})$ down to $P(X_i \mid \text{Parents}(X_i))$ (because the non-parent ancestors are non-descendants, hence conditionally independent of $X_i$ given its parents).

The bracket-clause "non-parent ancestors are non-descendants, hence conditionally independent" is the Markov condition itself stated again — it is not a step in the proof. A student reading this for the first time will not see why the previous-in-topological-order set $\{X_1, \dots, X_{i-1}\}$ decomposes into "parents + non-descendants". The actual argument is:

1. In topological order, the set $\{X_1, \dots, X_{i-1}\}$ contains all of $X_i$'s ancestors (since every ancestor precedes $X_i$).
2. Every ancestor is either a parent of $X_i$ or a non-descendant of $X_i$ that is not a parent.
3. A node that is in the topological prefix but is *not* an ancestor of $X_i$ is also a non-descendant (it cannot be a descendant since descendants come after in topological order).
4. Therefore $\{X_1, \dots, X_{i-1}\}$ = parents($X_i$) ∪ (non-descendant non-parents).
5. The Markov condition then gives the collapse.

The chapter compresses steps 1–4 into a clause that uses the conclusion to justify itself. A careful student preparing for a "derive the BN factorisation from the chain rule" question will not be able to reconstruct the proof. The two-line derivation needs four lines.

**Fix:** spell out steps 1–4 above. Slide 42 itself does compress this, so I would have downgraded if the chapter had simply mirrored the slide — but the chapter explicitly *claims to derive* this and the derivation as written is incomplete.

---

## P1 — IMPORTANT FIXES (gaps a student WILL notice in exam prep)

### P1-1. D-separation / the three connection patterns (chain, fork, collider) are MISSING

**Location:** L09a-Bayesian-Networks.md §3.9 lines 330–350, §4.1 line 555.

The chapter says (line 348):

> The general graph-theoretic criterion that decides whether *any* set of variables is conditionally independent of another given a third — by checking every undirected path between them and seeing whether it is "blocked" — is called **d-separation**. The slides only present the Markov-condition special case (parents block non-descendants) and use the phrase "Markov condition" rather than "d-separation". For exam purposes, the Markov condition is the form you'll be asked to apply.

This is correct in letter and wrong in spirit. The lecture *does* implicitly use two non-trivial d-separation patterns:

1. **Fork (common cause).** Slide 41: Rain → Umbrella and Rain → Traffic. Umbrella and Traffic are independent *given* Rain. The chapter mentions this and uses it as the canonical example, but does not name the pattern.
2. **Collider / V-structure (common effect / explaining away).** Slide 46: Burglary → Alarm ← Earthquake. Burglary and Earthquake are **marginally independent** (the priors are independent), but **dependent given Alarm** — the explaining-away phenomenon. Slide 47 sets up this exact structure with priors $P(+b)=0.001$, $P(+e)=0.002$ independent, but the structure is silent on what conditioning on Alarm does.

A student asked "in the alarm network, are Burglary and Earthquake independent? Are they independent given Alarm?" — which is precisely the kind of question a Bayesian-networks exam asks — gets no help from this chapter. The chapter does not state:

- Marginally, $B \perp E$ (parents of a collider are independent without conditioning).
- Given Alarm, $B \not\perp E$ (explaining-away makes parents dependent when their common child is observed).

Slide 54 line 555 explicitly says "*Two unconnected variables may still be correlated*", which is the same observation in a different network. The chapter quotes the line but does not unpack it.

**Fix:** add a section §3.9.1 "Three building blocks: chain, fork, collider" listing the patterns and what happens with/without conditioning on the middle node. Even one paragraph would close the gap. The Naive Bayes structure of §3.11 is itself a *fork from C* (which the chapter notes implicitly), so the vocabulary already exists in the lecture.

### P1-2. Slide 48 worked example REPLACED with a different query

**Location:** L09a-Bayesian-Networks.md lines 720–726.

Slide 48 explicitly computes:

$$P(+b, -e, +a, -j, +m) = P(+b)\,P(-e)\,P(+a \mid +b, -e)\,P(-j \mid +a)\,P(+m \mid +a)$$

and stops without the numerical value. The chapter writes (lines 722–726):

> $$P(+j, +m, +a, \neg b, \neg e) = P(+j \mid +a)\,P(+m \mid +a)\,P(+a \mid \neg b, \neg e)\,P(\neg b)\,P(\neg e) = 0.9 \times 0.7 \times 0.001 \times 0.999 \times 0.998 = 0.000\,628\ldots$$

This is a *different query* (Burglary FALSE vs Burglary TRUE; JohnCalls TRUE vs FALSE). Both are valid sample computations, but a student preparing the exam by "redoing the slide examples" will look for the slide-48 query and not find it. Worse, the slide-48 query is the one that demonstrates **a real burglary with no earthquake and one neighbour not calling** — the "informative" diagnostic case — whereas the chapter's query is **no burglary, no earthquake, but the alarm still went off and both neighbours called** — the "false-positive" case. These tell different stories.

Verified numerically: slide 48's $P(+b, -e, +a, -j, +m) = 0.001 \times 0.998 \times 0.94 \times 0.1 \times 0.7 = 6.57 \times 10^{-5}$. Chapter's $P(+j, +m, +a, \neg b, \neg e) = 6.28 \times 10^{-4}$. Different by an order of magnitude. Slide 48 explicitly says "$P(+b, -e, +a, -j, +m) = P(+b)P(-e)P(+a|+b,-e)P(-j|+a)P(+m|+a) =$" — the equality sign suggests the lecturer intended the student to fill in the number.

**Fix:** add slide 48's actual computation. Keep the chapter's "false positive" example if useful, but label it as supplementary; the slide-derived example must come first.

### P1-3. Naive Bayes — the Gaussian density values are unjustified

**Location:** L09a-Bayesian-Networks.md lines 411–416.

The chapter copies slide 29's values:

- $P(\text{Income} = 120K \mid C = \text{No}) = 0.0072$
- $P(\text{Income} = 120K \mid C = \text{Yes}) = 1.2 \times 10^{-9}$

with the gloss "the 0.0072 is the value of the Gaussian density for the income column at $x = 120$K, conditional on Class = No". Slide 29 *provides* the parameters: sample mean = 110, sample variance = 2975 for Class=No; sample mean = 90, sample variance = 25 for Class=Yes. The chapter does NOT spell out the formula:

$$f(x \mid \mu, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$$

Plug in: for Class=No, $\mu=110, \sigma^2=2975, x=120$:
$\frac{1}{\sqrt{2\pi \cdot 2975}} e^{-100/5950} = \frac{1}{\sqrt{18691}} e^{-0.01681} \approx 0.00732 \cdot 0.983 \approx 0.00720$. ✓

For Class=Yes, $\mu=90, \sigma^2=25, x=120$:
$\frac{1}{\sqrt{2\pi \cdot 25}} e^{-900/50} = \frac{1}{\sqrt{157.08}} e^{-18} \approx 0.0798 \cdot 1.52 \times 10^{-8} \approx 1.21 \times 10^{-9}$. ✓

Both match. **But the chapter never tells the student where these came from.** A student asked "given mean=110, variance=2975, compute $P(X=120 \mid \text{class=No})$" cannot do it from this chapter. The chapter should include the Gaussian formula explicitly with one worked plug-in — slide 29 *provides* the parameters in a side-box, so the lecturer clearly expected the student to know how to use them.

**Fix:** add one paragraph in §3.11 or §5.4 with the Gaussian density formula and the worked plug-in for one of the two values. Note: this is also where the chapter could flag that mixing discrete features (Refund, Marital) with a continuous feature (Income) is standard Naive-Bayes practice and is *not* an extra assumption.

### P1-4. Explaining away — not mentioned anywhere

**Location:** Should be in §3.6 (conditional independence) or §3.9 (Markov condition), but absent.

Closely related to P1-1 but worth its own line item. The phenomenon: if $X \to Z \leftarrow Y$ (V-structure), then $X$ and $Y$ are *independent* marginally but *dependent* given $Z$. This is the inverse of all the other conditional-independence examples in the chapter, which all show conditioning *creating* independence. A student who only sees fork-style examples ("rain explains away umbrella–traffic correlation") will write on the exam "conditioning always creates independence", which is exactly wrong for colliders.

The chapter's chain rule + Markov derivation makes no room for this asymmetry. The alarm network (§5.6) is a perfect explaining-away example — burglary and earthquake are independent priors, but if you hear the alarm you should consider both, and learning that an earthquake just hit *decreases* the probability of a burglary (the alarm is already "explained"). The chapter shows the structure but never names or uses the phenomenon.

**Fix:** one paragraph in §3.6 or §3.9.1 (the new section suggested in P1-1) naming "explaining away" and computing the explanatory shift on the alarm network. Example: compute $P(+b \mid +a)$ and $P(+b \mid +a, +e)$; the second is lower — that is explaining-away.

### P1-5. Inference by enumeration cost formula in §4.4 and §3.13 contradicts itself

**Location:** L09a-Bayesian-Networks.md line 469 vs lines 647–650.

§3.13 (line 469):

> Each joint computation multiplies $n$ CPT entries. The number of joint entries we must sum is $\prod_{Y_j \in Y} |\text{Domain}(Y_j)|$ — exponential in $|Y|$.

§4.4 (lines 647–650):

> - Joint computation per entry: $O(n)$ (where $n$ = number of variables, ignoring CPT lookup cost).
> - Number of entries summed: $\prod_{Y_j \in Y} |\text{Domain}(Y_j)|$ — exponential in $|Y|$.
> - Total: $O(n \cdot d^{|Y|})$ where $d$ is the maximum domain size.

Two issues:

1. **"Joint computation per entry: $O(n)$"** — this assumes CPT lookup is $O(1)$, which is *almost* true but ignores the CPT-row indexing cost. Fine, this is standard.
2. **The cost $O(n \cdot d^{|Y|})$** is wall-time for *one query value* $P(X = x \mid e)$. For the full distribution over $X$ you multiply by $|Domain(X)|$, giving $O(n \cdot d^{|Y|+1})$. The chapter does not address this — slide 60 says "4 joint computes / 4 joint computes" for the *two* query values $P(R, T, \neg S)$ and $P(\neg R, T, \neg S)$, so the lecturer knows you sum over both. The chapter's formula in §4.4 silently drops this factor.

Minor in absolute terms (a factor of 2 for Boolean queries) but it is the kind of detail an exam will ask about. **Fix:** either say "per value of $X$" explicitly, or include $|D_X|$ in the formula.

### P1-6. Slide 30's "What if variables are not independent?" — chapter does not bridge to BN

**Location:** L09a-Bayesian-Networks.md lines 425–429 vs slide 30.

Slide 30 is the *transition slide* between Naive Bayes (slides 27–29) and Bayesian networks proper (slides 31+). It asks "What if variables are not independent?" — and the lecturer's answer (implicit in the next slide) is "use a Bayesian network with the actual dependency structure encoded in the DAG". The chapter handles this in two lines (§3.11 "When the assumption fails"):

> Many real attributes are causally or statistically dependent on each other even after conditioning on the class — height and weight given "is athlete", word frequencies in a document given "is spam", etc. Bayesian networks let us encode whatever dependence structure we actually believe; Naive Bayes is the special case "all features are conditionally independent given the class", which is fast and surprisingly hard to beat.

This is correct but understated. Slide 30's whole pedagogical move — "Naive Bayes is a special case; the general thing is a Bayesian network where the leaves can have edges *between* them too" — is the conceptual hinge of the lecture. A student asked "what is the relation between Naive Bayes and a Bayesian network?" should be able to draw the Naive Bayes graph, add some edges between the leaves, and explain that this lets the model capture feature dependencies. The chapter does not invite this.

**Fix:** one paragraph showing the Naive Bayes graph and then "the same graph with $A_1 \to A_2$ added" with the change in factorisation:
- Naive Bayes: $P(C) \prod_i P(A_i \mid C)$.
- Extended BN: $P(C) P(A_1 \mid C) P(A_2 \mid C, A_1) \prod_{i \ge 3} P(A_i \mid C)$.

### P1-7. Slide 65 "Where does the BN come from?" — completely skipped

**Location:** Slide 65 not addressed in chapter.

Slide 65 says: "Where do we get the Bayesian network from? Two options: Get an expert to design it / Learn it from data". The chapter has no §3.15 or §4.5 on this. It is one slide of content (not deep), but if the exam asks "name two ways to obtain a Bayesian network" the student who only has this chapter has nothing to write.

**Fix:** one sentence in §4.1 (Building a BN) or as §3.15. The two options are: (i) elicit from domain experts who supply the structure and the CPTs; (ii) learn structure and/or parameters from data (out of scope of L09a, glance forward to L10). Should also mention that the slide-49 algorithm assumes (i) — the structure is being designed by hand.

### P1-8. Slide 66 summary content (sparse/strict/Naive Bayes/joint sliding scale) — not in cheat sheet

**Location:** Slide 66's summary figure shows four BN structures on a *trade-off spectrum*: Strict Independence (no edges) → Naive Bayes (star from C) → Sparse Bayes Net → Full joint distribution. The visual captures the entire **flexible trade-off between model accuracy and compute efficiency** point of the lecture.

The chapter mentions "flexible trade off between model accuracy and compute efficiency" in §3.11 and §3.10 ("compactness") but never reproduces the *spectrum picture* or the explicit comparison Strict ⇒ Naive ⇒ Sparse ⇒ Full. This is a high-yield exam concept ("explain the trade-off Bayes nets enable") and the chapter answers it only piecemeal.

**Fix:** add a small section in §4.5 or §8 (cheat-sheet) with the four-structure spectrum as a comparison table:

| Structure | Edges | Parameters (Boolean, n=5) | Expressiveness |
|---|---|---|---|
| Strict independence | 0 | 5 | very low (all independent) |
| Naive Bayes (n-1 leaves, 1 root) | n-1 | 2n-1 | moderate (features indep given class) |
| Sparse BN (max in-degree k) | varies | $O(n \cdot 2^k)$ | high |
| Full joint | $\binom{n}{2}$ | $2^n - 1$ | full |

This is one of the most likely exam questions and the chapter currently fails to set it up.

### P1-9. §3.8 — CPT size formula gives $2^{k+1}$ but the chapter's commentary is muddled

**Location:** L09a-Bayesian-Networks.md lines 311–314.

The chapter writes:

> **Size.** A Boolean variable with $k$ Boolean parents has $2^{k+1}$ probability entries in total — though only $2^k$ of them are *independent* numbers, the rest follow from row-sum-to-1. Slide 38 phrases this as "$2^{k+1}$ probabilities" (counting both columns of the Boolean table).

This is correct but confusing under exam pressure. The student should be able to answer two questions cleanly:

1. **"How many cells in the CPT?"** $2^{k+1}$ (slide 38's number).
2. **"How many independent parameters?"** $2^k$ (the count for parameter-budget purposes).

The chapter's prose has both numbers but a panicking student in an exam will not parse "though only $2^k$ of them are independent numbers, the rest follow from row-sum-to-1" quickly. Bold the two numbers and contrast them explicitly. Also, for non-Boolean variables with domain size $d$ and parent domain sizes $d_1, \dots, d_k$:

- Cells: $d \cdot \prod_j d_j$.
- Independent parameters: $(d - 1) \cdot \prod_j d_j$.

The chapter has the parameter-count formula on line 322 but does not put it next to the slide-38 cell-count formula. Two consecutive sentences would solve this; right now they are 11 lines apart.

### P1-10. Alarm network — explicit explaining-away calculation absent

**Location:** §5.6, lines 691–727.

The chapter computes a sample joint $P(+j, +m, +a, \neg b, \neg e)$ but does not compute the *posterior* $P(+b \mid +j, +m)$, which is **the** canonical question asked about the alarm network in every textbook and likely exam. Russell & Norvig spend an entire section on this query. The slide doesn't compute it either, but a chapter on Bayesian networks that doesn't end with "given that both neighbours called, what's the chance there's a burglary?" is missing the punchline. Inference by enumeration would give about $0.284$ (from R&N).

**Fix:** §5.6 should end with a paragraph: "An exam-style query: given both neighbours called, what's $P(+b \mid +j, +m)$? By inference by enumeration over hidden variables $E$ and $A$..." and walk it through. The chapter has the §3.13 algorithm and the §5.8 lecture-late walkthrough — applying the same machinery to the alarm network is a natural sixth worked example and closes the loop on inference + alarm net.

### P1-11. §3.9 — "Markov condition" is presented but the slide also uses "d-separation" implicitly

**Location:** L09a-Bayesian-Networks.md lines 347–349.

The chapter says (line 348): "The slides only present the Markov-condition special case (parents block non-descendants) and use the phrase 'Markov condition' rather than 'd-separation'." Then claims the glossary will handle d-separation. The PDF source confirms: slides use "Markov condition" but slide 54 says "you can deduce many other conditional independence relations from a Bayes net" — that "many other relations" *is* d-separation. The chapter punts to the glossary without giving the student any tools to deduce those relations.

This is the same fix-direction as P1-1; including for the slide-citation discipline angle. A student asked "list one conditional-independence relation in the alarm network that does not follow directly from the Markov condition" has nothing.

### P1-12. §3.6 — slide 41's diagram includes "independent" as a dashed bidirectional arrow between Umbrella and Traffic, with the word "independent" on the line. The chapter does not warn that this *graph annotation* is conceptual, not part of the BN.

**Location:** L09a-Bayesian-Networks.md line 268.

Figure 9.6 in the chapter (slide 41) shows Rain → Umbrella and Rain → Traffic with a *dashed line* between Umbrella and Traffic labelled "independent". A naive student will look at this and conclude that BN diagrams sometimes have *dashed undirected edges meaning "conditionally independent"*. They do not — that dashed line is a pedagogical annotation on the slide, not part of the BN syntax. The actual BN over those three variables has only two solid directed edges; the conditional independence is a *derived property* of the structure, not an extra edge.

**Fix:** one sentence ("The dashed line in Figure 9.6 is a pedagogical annotation labelling the *consequence* of conditioning on Rain; it is not part of the Bayesian-network syntax.").

---

## P2 — POLISH / SUGGESTIONS

- **P2-1.** §1 line 14 lists three sources of uncertainty (partial observability, stochastic outcomes, modelling complexity). Slide 2 verbatim uses the words "Partial observability", "Uncertainty in action outcomes", "Complexity of modeling and predicting traffic". The chapter's bullet "Stochastic action outcomes" is a paraphrase that loses the slide's exact phrasing. Use the slide phrasing.
- **P2-2.** §3.1 line 99 worked coin-flip example reproduces slide 6 cleanly, but the chapter does not mention that this random variable is the *sum* of three Bernoulli RVs — a useful link to multivariate joint distributions. One-sentence addition.
- **P2-3.** §3.3 line 165 "≈ 0.059" — slide 16 says "0.059" without the "≈". Minor, but the chapter uses ≈ throughout where the slide does not.
- **P2-4.** §3.4 wedding example line 235 says "the actual chance of rain at the wedding is only about 11%". Slide 24 says 0.111. Verified $\approx 0.1133$. The chapter rounds down; slide rounds to the displayed value. Both fine but a student writing "11.3%" on exam should also be fine; the chapter does not say "round to slide's value".
- **P2-5.** §3.5 line 250 "Conversely, $P(A \cup B) = P(A) + P(B)$" — this is for *mutually exclusive*, not "conversely". The word "conversely" suggests it derives from independence; it does not. Replace with "For mutually exclusive events,".
- **P2-6.** §3.6 introduces *both* a child-development example (height/vocabulary given age) and a meteorology example (umbrella/traffic given rain). One example would suffice; two slow the chapter. Suggest keeping the slide-41 example only (rain/umbrella/traffic) since it is the one with a figure.
- **P2-7.** §3.7 line 287 lists "Vocabulary on slide 36" — including "Descendants of X — children, grandchildren, etc." This is fine but slide 36 also implicitly uses "ancestors" (everything that can reach X by following arrows backward). Add the "ancestors" entry; it appears later in §3.10's derivation discussion.
- **P2-8.** §3.10 line 373 — the chapter says "exponential only in the *local* parent count, not in the network size". Should clarify: the *storage* is $O(n \cdot d^k)$. The chapter says "$O(n \cdot 2^k)$ entries" but then in §4.5 the comparison table says "$O(n \cdot d^{|Y|})$" for inference. Use consistent notation; the difference between $2^k$ (storage, Boolean) and $d^k$ (storage, generic) matters.
- **P2-9.** §3.11 line 379 graphical depiction of Naive Bayes is an ASCII tree. Add a sentence noting that this is also called a *star graph* or *root-and-leaves* structure; both names show up in textbooks.
- **P2-10.** §3.12 line 440 "**Most-likely explanation.** 'Given the observations, which combination of unobserved variables is most probable?' — beyond this lecture (touched on in L09b)." — slide 43 only mentions the conditional-probability query $P(X \mid E)$. MLE/MAP queries are *not* in this lecture and adding them here without slide support is editorial scope creep. Remove or tag clearly as "not on this lecture's slides".
- **P2-11.** §4.1 line 506 "If you choose the variable ordering well — *causes before effects* — you typically get few parents and a small CPT." Slide 49 says only "minimal subset"; the chapter's editorial is correct but should cite Russell & Norvig (where the causes-before-effects heuristic comes from), not the slide.
- **P2-12.** §4.5 line 663 — the comparison table includes "Approximate inference" tagged "Out of scope". Slide 64 says "we resort to approximate inference techniques which are much faster". Out-of-scope is fine but the chapter should give one named example (likelihood weighting, MCMC) so the student has a vocabulary word. The chapter does name these in passing on line 472; reference that line from §4.5.
- **P2-13.** §5.1 to §5.5 reuse §3 examples without reformatting. Fine, but the section header "5.X Bayes' rule — meningitis" is misleading because there's no new content beyond §3.4. Consider deleting §5.1, §5.2, §5.3, §5.4 entirely (just leave a §5 intro saying "all worked examples appear inline in §3 and §4; this section adds two new ones") and renumbering §5.6, §5.7, §5.8.
- **P2-14.** Reading time "~75 min" on line 3 is reasonable for the chapter as written (933 lines + figures). After P1 fixes it will go to ~90 min. Update.
- **P2-15.** §6 (Pitfalls) is 10 items, well organized. But it doesn't include "forgetting to normalise after computing the joint sum" — a P3 trap in inference by enumeration. Step 3 of the §3.13 enumeration is the normalisation; students often compute the numerator and stop.

---

## EVIDENCE — Section-by-section spot checks against the PDF

| Section | Claim in chapter | PDF slide | Verdict |
|---|---|---|---|
| §1 lines 14–18 | 3 sources of uncertainty (partial obs / stochastic / modelling) | Slide 2 verbatim | ✓ (P2-1 wording) |
| §1 lines 22–24 | $P(A_{25})=0.04$, $P(A_{90})=0.70$, etc. | Slide 3 verbatim | ✓ |
| §1 lines 24–26 | EU formula | Slide 3 | ✓ |
| §3.1 line 99 | 3-coin worked example $P(X=2) = 3/8$, etc. | Slide 6 verbatim | ✓ |
| §3.2 lines 121–124 | 4 atomic events of (Cavity, Toothache) | Slide 8 | ✓ |
| §3.2 figure 9.1 | Joint table 0.8/0.1/0.05/0.05 | Slide 9 | ✓ |
| §3.2 line 141 | Marginals $P(C{=}f)=0.9$, $P(T{=}t)=0.15$, etc. | Slide 12 | ✓ |
| §3.3 line 165 | $P(C{=}t \mid T{=}f) = 0.05/0.85 \approx 0.059$ | Slide 16 | ✓ (verified numerically 0.0588) |
| §3.3 line 167 | $P(C{=}f \mid T{=}t) = 0.1/0.15 = 0.667$ | Slide 16 | ✓ |
| §3.3 figure 9.3 | All 4 conditional distributions | Slide 17 | ✓ |
| §3.3 line 182 | $P(T{=}f \mid C{=}f) = 0.8/0.9 \approx 0.889$ | Slide 18 | ✓ |
| §3.3 lines 156–159 | Chain rule | Slide 19 | ✓ |
| §3.3 line 191 | Bayes' rule | Slide 20 | ✓ |
| §3.4 line 212 | Meningitis $P(M \mid S) = 0.0002$ | Slide 21 | ✓ (verified numerically) |
| §3.4 line 233 | Wedding $P(R \mid \text{Predict}) = 0.111$ | Slide 24 | ✓ (verified 0.1133) |
| §3.5 line 246 | Independence definitions | Slide 25 | ✓ |
| §3.5 line 250 | Mutually exclusive ≠ independent | Slide 25 verbatim | ✓ (P2-5 wording) |
| §3.6 lines 256–259 | Conditional independence definitions | Slide 41 + general | ✓ |
| §3.6 line 264 | Height/vocabulary example | Slide 40 | ✓ |
| §3.6 line 265 | Rain/umbrella/traffic | Slide 41 | ✓ (P1-12 caveat) |
| §3.7 line 280 | DAG + CPTs definition | Slide 35 | ✓ |
| §3.7 line 287 | Parent/child/descendant vocab | Slide 36 | ✓ (P2-7 add "ancestor") |
| §3.8 lines 311–314 | CPT size $2^{k+1}$ | Slide 38 | ✓ (P1-9 clarity) |
| §3.8 line 322 | Parameter count formula | not on slide | added by chapter, correct |
| §3.8 line 323 | Alarm 10 vs 31 params | Slide 46 asks "How many?" — chapter answers 10 | ✓ |
| §3.9 line 334 | Markov condition | Slide 39 verbatim | ✓ |
| §3.9 line 345 | Derivation of factorisation | Slide 42 | ✓ but P0-1 circular |
| §3.9 lines 347–349 | D-separation punt | Slide 54 implicit | ✓ but P1-1 / P1-11 |
| §3.10 line 356 | BN joint factorisation | Slide 42 | ✓ |
| §3.11 line 391 | Naive Bayes independence assumption | Slide 28 | ✓ |
| §3.11 lines 397–399 | Argmax classification | Slide 28 + 29 | ✓ |
| §3.11 lines 410–414 | Worked NB example numbers | Slide 29 | ✓ but P1-3 unjustified Gaussians |
| §3.13 line 452 | Enumeration formula | Slide 58–62 | ✓ |
| §3.13 line 469 | Cost analysis | Slide 64 implicit | ✓ (P1-5 minor) |
| §3.13 line 471 | NP-complete | Slide 64 verbatim | ✓ |
| §4.1 line 503 | Build-a-BN algorithm | Slide 49 | ✓ exact |
| §4.1 line 506 | "Causes before effects" | not on slide | added by chapter (P2-11) |
| §4.1 lines 511–544 | Lecture-late network construction | Slides 50–53 | ✓ all CPTs match |
| §4.1 lines 552–555 | 3 properties from slide 54 | Slide 54 verbatim | ✓ |
| §4.2 lines 581–584 | A→B→{C,D} CPTs | Slide 35 | ✓ |
| §4.2 line 590 | Joint = 0.4·0.3·0.1·0.95 = 0.0114 | Slide 45 | ✓ (verified) |
| §4.3 lines 599–615 | Derivation of $P(T, \neg R, L, \neg M, S)$ | Slide 56 verbatim | ✓ |
| §4.3 line 623 | Numeric 0.00144 | not on slide (slide stops at the symbolic factorisation) | ✓ (verified numerically) |
| §4.4 lines 633–650 | Enumeration pseudocode | Slides 58–62 verbal | ✓ |
| §5.6 lines 694–711 | Alarm priors & CPTs | Slides 46–47 | ✓ all values match |
| §5.6 lines 716–718 | Parameter count 10 vs 31 | Slide 46 asks the question | ✓ |
| §5.6 lines 720–726 | $P(+j, +m, +a, \neg b, \neg e)$ | NOT slide 48's query | ✗ P1-2 |
| §5.6 — | $P(+b, -e, +a, -j, +m)$ (slide 48 query) | Slide 48 | missing |
| §5.6 — | $P(+b \mid +j, +m)$ (canonical alarm query) | not on slide | missing P1-10 |
| §5.8 lines 745–765 | $P(R \mid T, \neg S) \approx 0.415$ | not on slide; slide stops at "4 joint computes / 4 joint computes" | ✓ (verified numerically) chapter's own work |
| §6.5 line 795 | "No loops of any length are allowed" | Slide 35 verbatim | ✓ |
| §6 — | Explaining away / V-structures | nowhere | missing P1-4 |
| Slide 30 ("What if not indep") | bridged to BN | §3.11 closing paragraph | weak (P1-6) |
| Slide 65 ("Where does BN come from") | expert vs learn from data | nowhere | missing P1-7 |
| Slide 66 (sparse/strict spectrum) | trade-off spectrum | mentioned but no figure/table | missing P1-8 |

---

## EXAM-READINESS — 10 IMAGINED EXAM QUESTIONS

Could a student who reads ONLY this chapter answer each of these 10 plausible 20–25 mark exam questions?

| # | Imagined exam question | Pass? | Why |
|---|---|---|---|
| 1 | "Define joint distribution, marginal, conditional probability. Compute $P(C{=}t \mid T{=}f)$ given the slide-9 table." | **Pass** | §3.2–3.3 covers it exactly. |
| 2 | "State Bayes' rule. A doctor knows $P(S|D) = 0.5$, $P(D) = 10^{-4}$, $P(S) = 0.05$. Compute $P(D|S)$." | **Pass** | §3.4 meningitis example covers this exactly. |
| 3 | "Marie's wedding: $P(R) = 0.014$, $P(\text{Pred}|R)=0.9$, $P(\text{Pred}|\neg R)=0.1$. Find $P(R|\text{Pred})$." | **Pass** | §3.4 worked example. |
| 4 | "Define a Bayesian network. List its two components. Sketch the alarm network of slides 46–48 and label all CPTs." | **Pass** | §3.7, §5.6 covers it. |
| 5 | "Build a BN from the lecture-late statements (slide 50). Specify variable ordering, draw the DAG, list the CPT sizes (without numbers)." | **Pass** | §4.1 walks this step by step. |
| 6 | "State the Markov condition. In the alarm network, is Burglary independent of Earthquake? Is it independent given Alarm?" | **Fail** | Marginal answer ✓ from independence of priors (§5.6 implicit). But "is it independent given Alarm?" needs **explaining away** — the chapter does not cover this. P1-4. |
| 7 | "Compute $P(T, \neg R, L, \neg M, S)$ on the lecture-late network. Show the factorisation step by step (citing the Markov condition each time)." | **Pass** | §4.3 covers this exactly (slide 56). |
| 8 | "Define inference by enumeration. Trace it on the lecture-late net to compute $P(R \mid T, \neg S)$." | **Pass** with caveats | §5.8 walks the whole calculation. P1-5 cost-formula nitpick. |
| 9 | "What is a Naive Bayes classifier? Apply it to the slide-29 record $X = (\text{Refund=No, Married, Income=120K})$. Show the Gaussian densities for income." | **Borderline** | §3.11 covers the classification but P1-3 — the Gaussian density formula is never given. Student copies the slide values without being able to derive them. |
| 10 | "List the four BN structures on the spectrum from slide 66 (strict independence → Naive Bayes → sparse BN → full joint) and compare parameter counts for n=5 Boolean variables." | **Fail** | §3.11 and §3.10 mention compactness in passing but the chapter has no spectrum table. P1-8. |

**Net: 7 Pass, 1 Borderline, 2 Fail across 10 imagined questions.**

The two Fails (Q6 explaining-away and Q10 spectrum) are *exactly* the kind of conceptual questions a BN exam asks at the highest mark band. The borderline (Q9 Gaussian density) loses partial marks for students who cannot reproduce the density formula.

**Verdict refined:** the chapter is **strong on the lower-band questions** (Bayes' rule, joint entry, build-a-BN, inference by enumeration on a small net) but **weak on the upper-band conceptual synthesis questions** (V-structures, explaining away, the BN-as-trade-off-spectrum). For a Round 1 lecture chapter intended to be a complete exam-prep document, this is Pass-with-Concerns: fix P1-1 / P1-4 / P1-8 and the chapter is ready for Round 2.

---

## DOCUMENT.md audit

N/A for study chapter. The `study/lectures/` directory should have a `DOCUMENT.md` index but that is out of scope for this review.

---

## Out-of-scope observations

- The chapter cites `_shared/glossary.md` for the d-separation entry (line 348) and `_shared/cross-references.md` for the L09b/L10 cross-link table (line 837). Reviewer 4 has not verified those files exist or contain the cited content; recommend a separate sanity check.
- Lab 7 is forward-referenced (line 854–862) — make sure Lab 7 actually exists at `AI/Lab7/handout/` before students follow the link.
- L09b cross-references (HMM as "BN with a chain") in §7 (line 832) — needs L09b chapter to exist with the cited §3.
- L10 cross-references (Naive Bayes among classifiers) in §7 (line 833) — same concern.
- The Mermaid graph convention is not used in this chapter — only PNG figures from `extracted_figures/L09a/`. This is fine because the slides are figure-heavy, but a reader without those PNGs available will lose much of the network-structure content. Make sure the PNGs are committed.

---

## Concerns / Risks

- The chapter's heavy reliance on extracted figures from the PDF means a student rendering this on a plain Markdown viewer (e.g., GitHub mobile) will miss critical content. The §3.7 Bayesian-network definition has 2 PNG figures and almost no in-text equivalent for the DAG structure. Consider adding ASCII or Mermaid fallbacks.
- The §5.8 walkthrough is *new content* not in the slides. It is mathematically correct (verified to ≈ 0.415) but the chapter declares (line 769) "make sure you can reproduce it" — if the exam doesn't ask this particular query, the student wasted prep time. Better to flag it as illustrative rather than required.
- The explaining-away omission (P1-4) is the single most consequential defect because it shows up implicitly in every collider-shaped network the student will see (alarm network, medical diagnosis with multiple causes). Without naming it, the student will misapply the Markov condition on exam questions involving V-structures.
- The chapter spends ~75 minutes of reading time but the gossip-graph analogy in §2 carries the conceptual weight — if the student skips §2 to "save time", they lose the analogical scaffolding for the rest. Maybe move §2 inline at the top of §3 to make it harder to skip.

---

## What PM should do next

1. **Do NOT block release to Round 2.** The chapter is strong enough that Round 2 reviewers can read it productively. Tag P1-1, P1-4, P1-8 as must-fix-before-final.
2. **Dispatch the L09a chapter author (Extractor or whichever agent) for a targeted revision pass:**
   - Add a §3.9.1 covering chain/fork/collider patterns and explaining-away. (P1-1, P1-4, P1-12.)
   - Add slide-48's specific computation to §5.6. (P1-2.)
   - Add the Gaussian density formula with one worked plug-in to §3.11. (P1-3.)
   - Add the alarm-network posterior $P(+b \mid +j, +m)$ as a sixth worked example. (P1-10.)
   - Add a "where does the BN come from?" paragraph (P1-7) and a spectrum table (P1-8).
   - Spell out the §3.10 derivation in 4 steps rather than 1 clause. (P0-1.)
3. **Defer P2 items to the polish pass after Round 2.**
4. **Re-run Reviewer 4** after the revision pass, specifically on the 3 imagined-exam-question failures (Q6, Q9, Q10).

---

## Report to PM

**Assignment recap:** Lecture Reviewer #4 (Exam Readiness, Spec §7.1) for L09a Bayesian Networks, Round 1. Source: `Lecture9-Bayesian Networks.pdf` (67 slides, content slides 1–66). Chapter: `study/lectures/L09a-Bayesian-Networks.md` (933 lines).

**Status:** Pass with concerns. The chapter is largely correct and unusually rich; 10 numerical spot-checks all verify; 7 of 10 imagined exam questions pass cleanly. But explaining-away / V-structures / the slide-66 trade-off spectrum are omitted, and the slide-48 worked example is silently replaced.

**P0 findings:**
1. **P0-1** `L09a-Bayesian-Networks.md:345` — The §3.10 derivation of the BN factorisation from chain rule + Markov is compressed into a single clause that uses the Markov condition to justify itself; it is circular as written. Expand into the 4-step ancestor-decomposition argument.

**P1 findings:**
1. **P1-1** `L09a-Bayesian-Networks.md:330-350` — Chain/fork/collider patterns (d-separation building blocks) are entirely missing. Add §3.9.1.
2. **P1-2** `L09a-Bayesian-Networks.md:720-726` — Slide 48's explicit $P(+b, -e, +a, -j, +m)$ calculation is replaced with a different query. Restore the slide example.
3. **P1-3** `L09a-Bayesian-Networks.md:411-416` — Naive Bayes Gaussian density values (0.0072 and $1.2 \times 10^{-9}$) are copied from slide 29 without showing the formula $\mathcal{N}(x \mid \mu, \sigma^2)$ that produces them.
4. **P1-4** `L09a-Bayesian-Networks.md` — Explaining-away phenomenon (parents of a collider are independent marginally but dependent given the collider) is never named or computed. Add to §3.9 or new §3.9.1.
5. **P1-5** `L09a-Bayesian-Networks.md:647-650` — Inference-by-enumeration cost formula $O(n \cdot d^{|Y|})$ silently drops the $|D_X|$ factor for full-distribution queries.
6. **P1-6** `L09a-Bayesian-Networks.md:425-429` — Slide 30's "what if variables are not independent?" transition is treated in two lines; the conceptual bridge from Naive Bayes to general BN deserves a proper paragraph with the modified factorisation.
7. **P1-7** `L09a-Bayesian-Networks.md` — Slide 65 ("Where do we get the BN from? Expert / data") is not mentioned anywhere. Add one sentence to §4.1.
8. **P1-8** `L09a-Bayesian-Networks.md` — Slide 66's 4-structure spectrum (Strict / Naive Bayes / Sparse / Full) is absent; the trade-off-spectrum exam question has no source.
9. **P1-9** `L09a-Bayesian-Networks.md:311-314` — $2^{k+1}$ cells vs $2^k$ independent parameters distinction is correct but spread across 11 lines; collapse to consecutive sentences.
10. **P1-10** `L09a-Bayesian-Networks.md:691-727` — Alarm network has a joint-entry example but no canonical $P(+b \mid +j, +m)$ posterior query; the punchline-question is missing.
11. **P1-11** `L09a-Bayesian-Networks.md:347-349` — D-separation is punted to a glossary that the reviewer cannot verify; the chapter gives the student no tools for slide 54's "you can deduce many other conditional-independence relations".
12. **P1-12** `L09a-Bayesian-Networks.md:268` — Slide 41's dashed "independent" line in Figure 9.6 is a pedagogical annotation, not BN syntax; the chapter doesn't disambiguate.

**P2 findings:** 15 polish items including: slide-verbatim wording in §1; "conversely" misused in §3.5; mixing $2^k$ and $d^k$ between §3.10 and §4.5; §5.1-5.5 are redundant restatements of §3 examples; reading-time estimate; etc. See P2-1 through P2-15.

**QA Checklist (§7.1 exam-readiness) status:**
- Coverage of slide material — **Pass with gaps** (slides 30, 48, 65, 66 underserved).
- Factual accuracy — **Pass** (10/10 numerical spot-checks verify).
- Slide-citation discipline — **Pass** (cites correctly; non-slide claims are mostly tagged).
- Exam-question coverage — **Pass with concerns** (7/10 imagined questions pass; 2 fail on V-structures and spectrum).
- Pseudocode fidelity — **Pass** (build-a-BN, enumeration, joint-entry all match slide content).
- Pitfalls / Exam traps — **Pass** in coverage (10 items including base-rate fallacy, CPT direction, cycles), but missing explaining-away.
- Glossary / terminology — **Concerns** (d-separation punted, "explaining away" not introduced).

**Acceptance criteria (exam-readiness §7.1) status:**
- "Student reading only this chapter can answer slide-derived exam questions" — **Mostly met** (7/10 imagined questions pass).
- "Every slide claim is reproduced or paraphrased accurately" — **Mostly met** (slide 48's query replaced; slides 30, 65, 66 underserved).
- "Worked traces match the slide animations" — **Met** for slides 21, 24, 38, 42, 45, 51-56; **gap** at slide 48.

**DOCUMENT.md audit:** N/A for study chapter.

**Out-of-scope observations:**
- `_shared/glossary.md` and `_shared/cross-references.md` are heavily referenced but not verified by this reviewer.
- L09b and L10 cross-references in §7 dangle until those chapters exist.
- Lab 7 forward-reference in §7 dangles until `AI/Lab7/handout/` exists.
- Extracted-figures dependency: chapter loses much of §3.7's content if PNGs are missing.

**Concerns / risks:**
- Highest-impact defect: P1-4 (explaining away omitted) — students will misapply the Markov condition on collider-shaped exam questions.
- Second-highest: P1-8 (slide-66 trade-off spectrum missing) — high-yield "describe what BNs give you" question has no source.
- Third: P1-3 (Gaussian density formula missing) — partial-credit risk on Naive Bayes with continuous features.
- Lower-impact: P1-2, P1-7, P1-10 — slide-coverage gaps; fixable in one revision pass.

**What PM should do next:**
1. Dispatch L09a chapter author for one targeted revision pass covering P0-1 plus P1-1, P1-2, P1-3, P1-4, P1-7, P1-8, P1-10. These 7 items together close the most-likely exam-question gaps; the rest can wait for a polish pass.
2. Allow this chapter to proceed to Round 2 in parallel — Round 2 reviewers can read it productively right now even with the gaps.
3. After revision, re-run Reviewer 4 specifically on imagined-exam-questions Q6, Q9, Q10 (explaining-away, Gaussian density, spectrum).
4. Verify `_shared/glossary.md` has the d-separation entry the chapter promises (line 348).

**DOCUMENT.md updated:** N/A for QA.
