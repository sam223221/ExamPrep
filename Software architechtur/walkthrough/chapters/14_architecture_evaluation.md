# Chapter 14 — Architecture Evaluation and Introducing New QAs

> *"The process of determining the degree to which an architecture is fit for the purpose for which it is intended."* — Bass, Clements & Kazman, 2021

## 14.1 Why evaluate? Architecture review as a risk-reduction action

Every chapter up to this one has been a recipe for *making* architectural decisions: pick a pattern, apply a tactic, write a scenario, draw a deployment view. This chapter is the recipe for *checking* them. Architecture evaluation is the deliberate, scheduled act of asking, *"is what we have actually going to do what we said it would?"* — before the cost of being wrong becomes catastrophic.

Bass et al. frame the activity precisely: evaluation is **a risk-reduction action**. You enumerate risks (places where the architecture might fail to satisfy a QA, a business goal, or a constraint), classify them as *acceptable* or *unacceptable*, and decide where to invest mitigation effort. The cost vs. benefit calculation is loose — "cost" can be money, time, agility, reputation, or carbon — but the discipline is rigid: no opinion-by-opinion arguments, no taste contests; every claim is anchored to a scenario, a measurable response, or a documented decision.

This matters because architecture is the layer of the system where mistakes are most expensive to undo. Code can be refactored in an afternoon; a fundamental misfit between, say, a layered host stack and a real-time control loop is a six-month rewrite. Evaluation buys cheap, early evidence that an expensive commitment is sound. It also surfaces *implicit* risks — the architect built mental contracts the team never wrote down — and forces them into the open so they can be argued about, mitigated, or knowingly accepted.

A second, less obvious benefit: evaluation produces a written **evaluation report** (Section 14.6), which becomes the artefact that downstream maintainers, security auditors, certification bodies, and your future self will consult. The act of evaluation thus does double duty as documentation. An architecture without an evaluation report is folklore; an architecture *with* one is engineering.

Evaluation is also recursive. The QA framework from Chapter 2 (Source / Event / Environment / Artifact / Response / Response Measure) is the *input* to evaluation — and, as Section 14.7 shows, the same framework is the engine you crank when you need to invent a brand-new QA from scratch. So the rest of this chapter is, in effect, instructions for using the Chapter 2 machine in two modes: *checking* (evaluation proper) and *bootstrapping* (introducing a new QA).

Finally, a who-does-it note. A single architect can self-review; Bass et al. explicitly allow this. But the higher-leverage form is **outside peer review** — fresh eyes that have not been entangled in the decisions for months. The procedure below works for both, with the same checklist.

---

## 14.2 Bass et al.'s 4-step evaluation procedure

Bass, Clements and Kazman boil decades of ATAM-style reviewing down to four steps that fit on an index card:

1. **Reviewers individually understand the current state of the architecture.**
   Read the documentation, view diagrams, browse the C&C and deployment views, internalise the business goals. Done *before* the group meets. No discussion yet — the goal is independent comprehension so that subsequent disagreement is signal, not noise.

2. **The group agrees on evaluation criteria (and metrics, if possible) beforehand.**
   Pick the QA scenarios that matter — typically the ASRs (Architecturally Significant Requirements) — and attach response measures to each. If a scenario has no measure, fix it now; an unmeasurable scenario cannot be evaluated, only opined about. This is also the moment to bring in Falessi's broader factors (Section 14.3) or ACM-style artefact criteria (Section 14.4) if relevant.

3. **For each scenario, each reviewer decides whether the scenario is satisfied.**
   Walk the architecture against the scenario. Does the proposed pipe-and-filter actually achieve the latency target under the specified load? Does the chosen authentication tactic actually defeat the threat model? "Satisfied", "not satisfied", or "uncertain — needs prototype/measurement" are the three legal answers. Uncertain is *not* a failure mode; it is a flag for follow-up work.

4. **Reviewers capture potential problems and identify risks.**
   For every "not satisfied" or "uncertain", write a risk: *what could go wrong, how likely, how impactful, who owns mitigation*. Also record **non-risks** (scenarios that look scary but are demonstrably fine — explicit non-risks prevent re-litigation later) and **trade-offs** (decisions that improve one QA at the cost of another, documented so the trade is informed).

The deliverable of the four steps is the **evaluation report** of Section 14.6 — a single living document that the team, auditors, and future maintainers all share.

---

## 14.3 Falessi et al.'s seven evaluation factors

Scenarios cover the QA dimension; Falessi et al. add seven cross-cutting factors that catch the things scenarios miss. Use them as a second pass after the Bass procedure, or as the first pass when you are evaluating a *decision* (e.g., "we chose Kafka over RabbitMQ") rather than a whole architecture.

1. **Is the design documented and reviewed?** — Folklore architecture cannot be evaluated. If the C&C diagram exists only in the lead's head, that is the first risk.
2. **What business factors influenced it?** — Ties back to Chapter 1. A decision that ignores its business driver will outlive the driver and become technical debt.
3. **What is its return on investment?** — Architecture is an investment. The expensive tactic must pay back in QA terms commensurate with the spend.
4. **Were security implications addressed?** — Security is the QA most often retrofitted and most painful when omitted (see Chapters 8–9).
5. **How useful is it to other engineers?** — Reusability, both intra-team (will the next service benefit?) and across projects (does this become a reference architecture, Chapter 12?).
6. **How much implementation freedom does it constrain?** — Over-constraint kills agility; under-constraint kills coherence. Both are risks.
7. **How was the development team composed?** — Conway's law in checklist form: the team shape that built it influences what it is, and the team shape that *maintains* it determines whether it survives.

These cross-link to almost every chapter so far: factor 4 to Chapters 8–9, factor 5 to Chapter 12, factor 2 to Chapter 1, factor 7 to Chapter 1's team-and-process material.

---

## 14.4 ACM Artifact Review criteria

ACM evaluates research artifacts (code, datasets, reproducible studies) on four axes. They double as excellent internal heuristics for *"is this design report any good?"*:

- **Documentation** — Is everything that matters written down, with enough context that a reader who was not in the room can act on it?
- **Consistency** — Do claims in one section match claims in another? Does the deployment view actually realise the C&C view? Are the QA priorities in §2 reflected in the decisions in §5?
- **Completeness** — Does the artefact contain everything needed to support its claims? Missing measurements, missing rationale, missing alternatives considered.
- **Execution** — Does it *run*? For research, can the experiments be re-executed? For architecture, can a prototype actually demonstrate the contested tactic? Did anyone build the spike to prove the claim?

ACM further classifies artefacts as **Functional / Reusable / Available / Reproduced / Replicated** — a useful ladder for thinking about *how strong* a piece of evaluation evidence is. A working prototype on the architect's laptop is *Functional*; a published reference architecture another team has independently re-instantiated is *Replicated*. Aim higher than Functional whenever the decision warrants it.

**Why it matters:** these criteria pull software architecture into the orbit of scientific evaluation. "We tried it and it felt fast" is *not* an evaluation; a documented, consistent, complete, executable scenario walk-through is.

---

## 14.5 Dieter Rams' ten principles of good design

Rams was an industrial designer (Braun, Vitsoe). His ten principles are not a software framework, but they map onto architecture surprisingly well. The slides list eight; the remaining two are similar in spirit. Each principle is given an architectural analogy.

1. **Innovative** — design aligns with technology, never an end in itself.
   *Architecture analogy:* don't introduce a service mesh because it is fashionable; introduce it because the network-layer QAs (observability, mTLS, retry policy) demand it.

2. **Useful** — functional, aesthetic, psychological.
   *Architecture analogy:* an architecture must serve the QAs that matter to its actual stakeholders, not the QAs the architect finds intellectually pleasing.

3. **Aesthetic** — beauty matters.
   *Architecture analogy:* a clean module-decomposition diagram is not vanity; clarity of structure correlates with maintainability and onboarding speed.

4. **Understandable** — clarifies goals, structure, functionality.
   *Architecture analogy:* a stranger reading the C&C view should infer the system's purpose. If they cannot, the documentation has failed.

5. **Honest** — does not manipulate users (anti dark-pattern).
   *Architecture analogy:* don't bury defaults that work against the user (auto-renew, opt-out tracking, sneaky telemetry). The architecture *enables* policy; honest architecture refuses to enable predatory policy.

6. **Thorough** to the last detail.
   *Architecture analogy:* the deployment view names the actual VM types, the actual quotas, the actual retry budgets — not the words "auto-scaling group, sized appropriately".

7. **Environmentally friendly.**
   *Architecture analogy:* explicitly tie this to Chapter 12's power-consumption thread. An architecture that ignores energy per request, idle power, and cooling overhead is incomplete by 2026 standards. Sustainability is a QA — and Rams put it on the list in the 1970s.

8. **As little design as possible.**
   *Architecture analogy:* every component is a liability. The smallest architecture that meets the ASRs is the best architecture. This is the architectural form of "simplicity" as a usability sub-QA.

9. **(Long-lasting)** — does not become dated quickly.
   *Architecture analogy:* favour decisions that age well — open standards over proprietary, stable abstractions over fashionable ones.

10. **(Unobtrusive)** — leaves the user room to express themselves.
    *Architecture analogy:* the framework that vanishes into the background and lets domain code shine through is the better framework.

**Why it matters:** principles 5 (honesty), 7 (environment), and 8 (least design) are the three most quotable in an evaluation report. #7 in particular links back to Chapter 12: an architecture review in 2026 that does not consider power consumption is failing its own age.

---

## 14.6 The evaluation report — Bass et al.'s six sections

The deliverable of a Section-14.2 evaluation is a written report. Bass et al. recommend exactly six sections:

1. **A concise overall presentation of the architecture.** Top-level views (C&C, deployment, module decomposition), no more than a few pages — enough that the reader understands *what is being evaluated*.
2. **Articulation of business or other goals.** Why does this system exist? Falessi factor 2 lives here.
3. **Prioritisation of quality attributes based on scenarios.** The ASRs, with their full scenario specifications and response measures. Chapter 2 machinery, applied.
4. **A set of risks — including acceptable risks and non-risks.** Explicit list. Acceptable risks are documented so they remain conscious choices. Non-risks are documented so they cannot be re-litigated by a future skeptic.
5. **Mapping of architectural decisions to quality attributes.** Which decision serves which QA? The reverse mapping (which QA is *un*-served, or served only weakly) is equally important.
6. **Articulation of trade-offs and the decisions taken.** Where two QAs were in tension (e.g., security vs. performance, power vs. responsiveness), what was traded for what, and on what evidence.

**Tabular form is strongly recommended.** A typical layout has *architectural decisions* as rows, with columns for: served QAs, risks introduced, trade-offs accepted, mitigation owner. This format is reusable across reviews, supports diff-style updates as the architecture evolves, and forces every cell to be filled — a blank cell is itself a finding.

A figure that doubles as an evaluation aid (originally from Chapter 12) is reproduced below, showing how usability sub-QAs are reapplied when evaluating a *reference architecture* from the architect-as-user perspective. The same trick — *evaluator reuses an existing QA decomposition* — is the cheap path to credible criteria when no domain-specific evaluation framework yet exists.

![Reference-architecture evaluation reusing usability sub-QAs](../images/lecture_10/fig12_reference_architecture_eval.png)

---

## 14.7 Introducing a brand-new QA — the meta-procedure

This is the meta-message of the course: frameworks decay, but the *process for inventing one* is durable. Examples in 2026 include integrating LLMs and autonomous agents into enterprise architectures; in 2010 it was the same problem for cloud, in 1995 for the web. New QAs keep arriving — knowing how to bootstrap one is more valuable than memorising any specific catalogue.

### When do you need a new QA?

You need a new QA when:

- Stakeholders care about a property the existing catalogue cannot name precisely.
- Existing scenarios cannot articulate the property's *response measure* (the symptom is hand-waving in requirements documents).
- A new technology class (LLMs, ambient computing, sustainability budgets) introduces concerns that don't decompose cleanly into known QAs.
- Regulatory or ethical pressure invents a new acceptance criterion (e.g., "auditability of an AI decision").

### Bass et al.'s 4-step recipe for deriving a new QA

1. **Start with scenarios.** Use the Chapter 2 framework — Source, Event/Stimulus, Environment, Artifact/Deployment, Response, Response Measure — even before you have a clean name for the new QA. Concrete scenarios force the property into the open. *Example:* for "LLM groundedness", a scenario might be: *Source = a customer-support query referencing real entitlement data; Event = the LLM generates an answer; Environment = production with retrieval-augmented generation; Response = the answer cites the source documents it relied on; Response measure = ≥ 95% of factual claims cite a retrieved document, ≤ 1% hallucinated entitlement amounts.*

2. **Ask: are existing scenarios / tactics / patterns transferable, possibly with modifications?** Many "new" QAs are reskinned older ones. Groundedness leans heavily on auditability (Chapter 8/9 security tactics). Sustainability reuses Chapter 7 scalability mechanisms in reverse. The cheapest new QA is one that inherits 80% from an existing one.

3. **Triangulate with academic literature, industry "gray" literature, and standards.** Papers (often via tools like Hugging Face hub or Google Scholar), vendor whitepapers, draft ISO/IEC standards, NIST publications. The point is *not* to find a name and copy it; the point is to discover what response measures other people have already proposed, so you can either adopt or critique them.

4. **Talk to stakeholders and experts.** Architects pay for QAs in design effort; the *people who experience the lack of the QA* pay for it in failures. Both perspectives are needed. Stakeholder interviews surface the un-articulated; expert interviews surface the precedent.

### Why this recipe matters

Two reasons. First, it is reusable across an entire career: every five years a new QA arrives and the Bass recipe still applies. Second, *being early on a new QA is a business advantage.* The first team to articulate clean scenarios for "LLM evaluability" (or "carbon per request", or whatever 2030 brings) sets the response measures the rest of the industry will adopt — and may write the reference architecture (Chapter 12) the rest of the industry will copy.

---

## 14.8 Takeaways

- **Evaluation is risk reduction**, not a verdict. The output is a list of risks (acceptable, unacceptable), non-risks, and trade-offs — *not* a pass/fail.
- **Bass's 4 steps**: individual understanding → agreed criteria → per-scenario satisfaction check → captured risks. Memorise the four; they are highly exam-likely.
- **Falessi's 7 factors** widen the lens beyond scenarios: documentation, business, ROI, security, usefulness, freedom-constraint, team composition.
- **ACM's 4 axes** (documentation / consistency / completeness / execution) and ladder (Functional → Reusable → Available → Reproduced → Replicated) turn evaluation into something defensible to scientific standards.
- **Rams' ten principles** translate to architecture; principle 5 (honesty, anti dark-patterns) is the ethical dimension, principle 7 (environmentally friendly) ties directly to Chapter 12's power consumption, principle 8 ("as little design as possible") is the architectural form of simplicity.
- **The evaluation report has six sections** (architecture overview / goals / prioritised QAs / risks / decision-to-QA mapping / trade-offs), best expressed in tabular form.
- **Introducing a new QA** follows a 4-step recipe (scenarios → transferability check → literature/standards → stakeholders) and is the durable meta-skill of the course. Chapter 2's QA framework is the engine; Chapter 14 tells you when and how to crank it for unmapped territory.
- **Cross-refs:** Chapter 2 supplies the scenario template every step here consumes. Chapters 15 and 16 are case studies the student can practice evaluating with the Section-14.2 procedure — try walking each one of those architectures through the four steps and producing a one-page risk table.

> **Exam tips.** The Bass 4-step procedure and the 6-section evaluation report structure are both 3- to 4-point recall questions. Rams' #5 (honesty / dark-patterns) and #7 (environmental friendliness) are the two principles the lecturer flagged for memorability. The "introducing a new QA" recipe is the durable meta-skill — expect at least one question framed as *"a stakeholder asks you to ensure the system has property X, which is not in any catalogue. How do you proceed?"*
