# Lecture 10: Usability and Power Consumption (and Architecture Evaluation)

> **Source:** lecture_10.pdf (73 pages)
> **Lecturer:** Jukka Ruohonen
> **Date:** April 28, 2026
> **Course code:** T630019402 — Software Architecture, 10pt
> **Position in course:** Final lecture. Doubles as a meta lecture: it covers two more quality attributes (usability, power consumption), revisits trade-offs across all earlier QAs, ends with an explicit section on **architecture evaluation**, and contains the lecturer's exam guidance.

## Themes covered

1. **Usability as a non-technical QA** — why it does not fit the engineering-centric framework used for the rest of the course.
2. **The TAM model and its critique** — perceived usefulness vs. perceived ease of use, and the missing "abandonment" side of the causal story.
3. **Usability sub-QAs and "usability for whom?"** — sub-attributes (discoverability, learnability, efficiency, simplicity, understandability, flexibility) applied to *different audiences* (end-users, administrators, developers, architects).
4. **Reuse of earlier patterns for usability** — Memento (undo), MVC, Observer (statistics / A/B testing).
5. **Personas and dark patterns** — ethics of usability optimisation; what is actually being maximised?
6. **Power consumption as a QA** — idle vs. computing vs. cooling vs. loss; the hardware-level P-states / C-states machinery on x86.
7. **Tactics for power**: graceful shutdown vs. graceful degradation vs. forceful degradation; preloading, prefetching, offloading; minimising software interference with hardware optimisations.
8. **Trade-offs across QAs** — usability vs. power, responsiveness vs. power, security vs. power, language choice vs. power.
9. **Introducing brand-new QAs** when the existing body of knowledge is silent (e.g., AI/LLM integration), via scenarios and literature triangulation.
10. **Architecture evaluation as a process** — Bass et al.'s scenario-based review, Falessi et al.'s factor list, ACM artifact criteria, Dieter Rams' ten principles, and what an evaluation report should contain.

## Concepts

### Usability (definition)
**Definition:** "How easy it is for the user to accomplish a desired task and the kind of user support that the system provides" (Bass et al. 2021).
**Why it matters:** Usability is fundamentally non-technical — it sits between psychology, design, and engineering, so the QA framework used for performance/availability does not transfer cleanly. The lecturer flags it explicitly as the QA that is "quite distinct" from the others on the course.
**Detailed explanation:** The traditional definition is task-oriented: did the user accomplish their goal cheaply (time, clicks, cognitive load)? Modern framings widen this to include enjoyment, satisfaction, joy — and their antonyms: frustration and anger. So the QA has both positive and negative dimensions to engineer for.
**Analogy:** Performance can be measured with a stopwatch; usability needs a user, and even then half the signal lives inside their head.
**Common pitfall:** Treating usability as "make the UI prettier". The course's frame is broader — it includes the *system's affordances for being learned, recovered from, and adapted to*.

### Computer Frustration Model
**Definition:** A causal model (Hertzum & Hornaek 2023) where a **task** plus an **interruption** combine via situational and dispositional mediators (goal commitment, severity, computer experience, mood) to produce **immediate frustration** and an **emotional outcome**.
**Why it matters:** It is the explicit "negative side" of the usability story — i.e., the model that explains why even functional software causes user anger.
**Example:** A user trying to file a tax return (high goal commitment) hits an opaque error message (severe interruption) on Friday afternoon (bad mood) — the model predicts strong emotional outcome regardless of how many "tasks" the system technically supported.
**Related diagram:** ![Computer Frustration Model](../images/lecture_10/fig01_computer_frustration_model.png)

### Technology Acceptance Model (TAM)
**Definition:** Davis (1989) model: external variables → **perceived usefulness** + **perceived ease of use** → attitude → intention to use → actual use.
**Why it matters:** One of the few information-systems theories that "stood the test of time". On this course it provides the vocabulary for distinguishing the *task* dimension (usefulness) from the *usability* dimension (ease of use).
**Detailed explanation:** TAM splits the user's reasoning into two paths: does the tool help me get my work done (usefulness)? and is it pleasant/cheap to operate (ease of use)? Both feed attitude, which feeds intention, which feeds actual use. The lecturer stresses that the causality assumption in TAM is not obvious — actual use can feed back into perceived usefulness.
**Common pitfall:** Treating "ease of use" as the whole of usability. TAM's usefulness branch is *task-driven* and lines up with all the rollback/undo/pause tactics; the ease-of-use branch is where the GUI-style design problems live.
**Related diagram:** ![TAM model](../images/lecture_10/fig02_tam_model.png)

### TAM's missing side: customer retention / abandonment
**Definition:** The lecturer's own extension: alongside "intention to use" there should be an **intention to abandon use** path, fed by frequent incomprehensible errors, outdated docs, LLM-powered customer service, and frequent interruptions.
**Why it matters:** Retention is an architectural concern. Bass et al. (2021) recommend tactics like **cancel, undo, pause/resume, and automation** on the usefulness branch; and **personalisation** on the ease-of-use branch — these are exactly the affordances whose absence drives users away.

### UZ / UI / UX layering
**Definition:** A conceptual stack from concrete to vague — UZ (low-level computer interaction), UI (the interface), UX (broader experience), with philosophy/theoretical roots at the top.
**Why it matters:** Software-engineering techniques can directly measure things at the UZ/UI level; UX and above can only be measured by **proxy variables** (likes, clicks, time spent). The TAM model "operates here" near the middle of the stack, and the frustration model feeds back into the psychological dimension at the top.
**Common pitfall:** Reporting clicks as if they were UX. They are proxies, not ground truth.
**Related diagram:** ![UZ/UI/UX layering](../images/lecture_10/fig04_uz_ui_ux_layers.png)

### Usability sub-QAs
**Definition:** Decomposition of usability into smaller qualities: **discoverability, learnability, efficiency, simplicity, understandability, flexibility (adaptability)**. The "..." in the slide is deliberate — the list is open-ended.
**Why it matters:** Each sub-QA has its own tactics. Flexibility includes error recovery (the lecturer notes this explicitly).
**Nuance:** The sub-QAs correlate with each other heavily ("maybe even all of them"). Optimising one rarely happens in isolation.
**Related diagram:** ![Usability sub-QAs](../images/lecture_10/fig05_usability_subqas.png)

### Usability for whom? (audience taxonomy)
**Definition:** Usability is always defined relative to a user *class*: end-users (consumers vs. professionals), system administrators, developers (programmers vs. architects). DevOps blurs these — developers "are also" administrators.
**Why it matters:** A change that improves usability for end-users can simultaneously *degrade* it for administrators or developers. Architects should know the audience before optimising.
**Example:** The same sub-QAs (discoverability, learnability, ...) reapplied to an **architect** evaluating a **reference architecture** — i.e., how discoverable is the documentation? how learnable is the pattern? This gives a usability-style yardstick for architectural artifacts themselves.
**Related diagrams:**
![Usability audience taxonomy](../images/lecture_10/fig10_usability_for_whom.png)
![Sub-QAs applied to evaluating a reference architecture](../images/lecture_10/fig12_reference_architecture_eval.png)

### Suitability metric for reference architectures
**Definition:** Silva et al. (2023): y = A / B, where A = number of components in a reference architecture that fit well into the given domain, B = total components in the actual implemented architecture.
**Why it matters:** A first concrete, quantitative way to evaluate "did this reference architecture serve us?" Useful when reusing established patterns in a new domain.

### Memento pattern (for undo)
**Definition:** A usability pattern that snapshots a state so the user (or the system) can roll back. The slide shows a simple serialisation-based memento in R: persist an expensive partial computation, so a re-run reloads it instead of recomputing.
**Why it matters:** Implements the **undo** tactic from TAM's usefulness branch. The lecturer explicitly links it to the **rollback tactic** from lecture 4 and notes a structural similarity to the **claim-check pattern** from lecture 6.
**Pitfall:** Mementos can balloon storage; tune what gets snapshotted.

### MVC as a usability pattern
**Definition:** Model–View–Controller separates the data (Model) from the presentation (View) and input handling (Controller). Recap from lecture 3.
**Why it matters:** Re-skinning (WordPress templates, themes) is a usability affordance enabled by MVC — the model and controller stay untouched while the view varies. The cardinality `1—*` between Controller and View is "there for a reason".
**Related diagram:** ![MVC recap](../images/lecture_10/fig07_mvc_recap.png)

### Observer pattern for statistics / A/B testing
**Definition:** Recap from lecture 3. Views attach themselves to the Model via `attach(this)`/`detach(this)`; the Model can then call `statistics()` on every attached observer to gather data — including A/B-testing variants (View A vs. View B).
**Why it matters:** Observer is the architectural enabler for the *measurement* side of usability — without it you cannot do statistical comparison of UI variants.

### Personas
**Definition:** Fictional "characters" that mimic future users, modelled with attributes (age, nationality, OS, preferences, prior reading...). Used when surveys are infeasible or the customer segment is unknown.
**Why it matters:** A lightweight requirements-elicitation tactic for usability. The lecturer notes that LLMs are a natural fit for generating them. Concrete worked example in the slides: building a scientific-paper recommender for "me" (Linux, CLI) vs. "someone else" (Windows, GUI) immediately surfaces different feature sets.

### Dark patterns and the ethics of usability
**Definition:** Design patterns that deliberately manipulate the user against their own interest — illustrated via deceptive.design and the social-media addiction trial referenced in the slides.
**Why it matters:** "Maximising usability" is not value-neutral. The exercise paper (https://dl.acm.org/doi/pdf/10.1145/3359183) catalogues these patterns in Table 2 and links them to cognitive biases. Honesty appears later in Dieter Rams' ten principles as the opposite of this.

### Power consumption — analytical decomposition
**Definition:** Following Ahmad & Vijaykumar (2010), for machine *i* in a system of *n*:
`Total power_i = computing_power_i + idle_power_i + cooling_power_i + power_loss_i`
**Why it matters:** Makes the optimisation problem concrete. Idle power has a **lower bound** — you cannot shut a device to zero while keeping it usable. Cooling varies non-linearly with hardware utilisation, so trade-offs are not local to one machine.
**Related diagram:** ![Power consumption with redundant machines](../images/lecture_10/fig30_power_redundancy.png)

### Throttling vs. P-states vs. C-states
**Definition:**
- **Throttling** (lecture 9 sense): an emergency action — the CPU bluntly cuts its clock when overheating.
- **P-states (Performance states):** scaled performance levels P0…Pm, where P0 = full performance (e.g., 2.9 GHz) and Pm = lowest (e.g., 500 MHz). Supplied by the BIOS via ACPI. On modern hardware they can apply **per CPU package** *or* **per CPU core**.
- **C-states (Idle/sleep states):** C0…Cm, where C0 = full performance (nothing disabled) and Cm = deepest sleep (timers, caches, etc. disabled).

**Why it matters:** The mental model for "how does my laptop save power?" The lecturer asks the class explicitly: *Which earlier tactic do P/C-states correspond to?* (Hint: scaling resources / resource throttling.) And: *Which tactic do they contradict?* (Hint: anything that demands constant low latency — high responsiveness will keep cores out of deep C-states.)
**Related diagrams:**
![P-states per package](../images/lecture_10/fig23_per_package_p_states.png)
![C-states per package](../images/lecture_10/fig26_c_states.png)

### Hardware wake-ups and the power-tuning rule of thumb
**Definition:** Things that prevent CPUs from entering deeper C-states: user input, but also "seldom-used hardware" (USB devices etc.) being 100% powered, kernel polling, network/disk activity.
**Why it matters:** Yields the lecturer's **general rule of thumb**: *try to minimise software actions that interfere with optimisations already done for hardware.* Concrete don'ts:
- Don't fire unnecessary interrupts (notifications, polling).
- Don't hit disk and network needlessly (e.g., mount `/tmp` and `/var/tmp` as `tmpfs` on Linux laptops).
- Avoid GC runs where possible (Hort et al. 2022).
- Memory leaks are also *power* bugs because RAM is hardware.

### Display dominance
**Definition:** Empirical observation (from PowerTOP screenshots): on a laptop, the **display** is the most power-hungry component — more than the CPU. So setting display brightness to 0% saves power but destroys usability.
**Why it matters:** Concrete instance of the usability vs. power trade-off.
**Related diagram:** ![Usability vs. power trade-off](../images/lecture_10/fig21_usability_vs_power.png)

### Graceful shutdown vs. graceful degradation vs. forceful degradation
**Definition:**
- **Graceful shutdown:** the system warns the user, finishes/persists in-flight work, then powers off cleanly.
- **Graceful degradation:** as resources (battery) shrink, the system disables non-essential functionality in steps (e.g., 100% → 60% → 25% of functions, then graceful shutdown).
- **Forceful degradation:** the system is *made* worse against user intent (often the dark-pattern side).
**Why it matters:** Three commonly confused terms; the lecturer separates them explicitly with `!=`. The exam-style "what example of forceful degradation can you give from past lectures?" question is posed to the class.
**Related diagram:** ![Graceful degradation](../images/lecture_10/fig31_graceful_degradation.png)

### Preloading (and its link to escalating restart)
**Definition:** Start things earlier than strictly needed so they are warm when wanted. Modelled here as the *escalating restart* tactic in reverse: levels A/B/C of preload (25%, 60%, 100%) before full restart.
**Why it matters:** Startup is power-expensive; amortising it via preload saves power AND helps responsiveness (Hort et al. 2022). Use predictive analytics (e.g., frequent-app history on phones) to decide *what* to preload.
**Pitfall:** Preloading the wrong things wastes both power and memory.
**Related diagram:** ![Preloading](../images/lecture_10/fig33_preloading.png)

### Offloading and prefetching
**Definition:**
- **Offloading:** move computation away from the local (often power-constrained) machine to a more capable / power-rich machine.
- **Prefetching:** pull data toward the local machine before it is asked for.
**Why it matters:** Both are general-purpose power and performance tactics. Note their *direction* is opposite (offload pushes work out, prefetch pulls data in).
**Related diagram:** ![Offloading and prefetching](../images/lecture_10/fig34_offloading_prefetching.png)

### Language choice as a power lever
**Definition:** Research (referenced in slides) shows C consumes much less power than Python for equivalent computation.
**Why it matters:** Drags the "language wars" into the architecture evaluation. The lecturer immediately asks: *is the power saving worth the security and productivity trade-offs of writing C?* This is a setup for the trade-off-analysis section.

### Introducing brand-new QAs
**Definition:** When no existing body of knowledge exists for a quality (e.g., "how to integrate AI/LLMs/Agents into an existing enterprise architecture?"), Bass et al. (2021) recommend:
1. Start with **scenarios** (sources, events, environments, systems/deployments, responses, response measures).
2. Ask: are existing scenarios/tactics/patterns transferable, possibly with modifications?
3. Triangulate with **academic literature**, industry "gray literature", standards.
4. Talk to **stakeholders and experts**.

**Why it matters:** This is the meta-skill the lecturer wants students to leave the course with — frameworks decay, but the *process for inventing one* is durable. Bonus: solving a new QA first or better can be a business advantage; for industry-wide QAs, a reference architecture may emerge.

### Architecture evaluation as risk reduction
**Definition:** "The process of determining the degree to which an architecture is fit for the purpose for which it is intended" (Bass et al. 2021). It is **a risk-reduction action** — identify risks, then decide which are acceptable and which are not (cost/benefit, with "cost" understood loosely).
**Why it matters:** Pulls together everything from QA prioritisation (lecture 2) to scenario-based reviewing.

### Bass et al.'s evaluation procedure
1. Reviewers individually understand the current state of the architecture.
2. The group agrees on evaluation **criteria (and metrics, if possible)** beforehand.
3. For each scenario, each reviewer decides whether the scenario is satisfied.
4. Reviewers capture potential problems and identify risks.

A single architect can perform reviews; peer review by outsiders is also allowed.

### Falessi et al.'s evaluation factors
Beyond scenarios, the literature offers richer criteria:
1. Is the design documented and reviewed?
2. What business factors influenced it?
3. What is its return on investment?
4. Were security implications addressed?
5. How useful is it to other engineers?
6. How much implementation freedom does it constrain?
7. How was the development team composed?

These cross-link to almost every other lecture (security → L8/L9, ROI/business → L1, team composition → L1).

### ACM artifact-evaluation criteria
**Definition:** ACM evaluates research artifacts on four axes: **documentation, consistency, completeness, execution**.
**Why it matters:** Pulls software architecture into the realm of scientific evaluation — these are also useful internal heuristics for "is this design report any good?"

### Dieter Rams' ten principles for good design
Eight of the ten are listed in the slides (the implication is the remaining two are similar in spirit):
1. **Innovative** — design aligns with technology, never an end in itself.
2. **Useful** — functional, aesthetic, psychological.
3. **Aesthetic** — beauty matters.
4. **Understandable** — clarifies goals, structure, functionality.
5. **Honest** — does not manipulate users (anti dark-patterns).
6. **Thorough** to the last detail.
7. **Environmentally friendly** (resonates with the power-consumption thread!).
8. **As little design as possible** (resonates with "simplicity" sub-QA).

**Why it matters:** Some of these resonate strongly with software design (1, 4, 5, 8) and one (7) ties directly back into the power/sustainability thread of this very lecture.

### Evaluation report content
**Definition:** Bass et al.'s recommended structure for the *output* of an architecture evaluation:
1. A concise overall presentation of the architecture.
2. Articulation of business or other goals.
3. Prioritisation of quality attributes based on scenarios.
4. A set of risks — including acceptable risks and non-risks.
5. Mapping of architectural decisions to quality attributes.
6. Articulation of trade-offs and the decisions taken.

**Tabular form** is recommended for reusability and rigour — architectural decisions as rows; risks, trade-offs, impacts as columns.

## Important diagrams (catalog)

- `fig01_computer_frustration_model.png` — Hertzum & Hornaek (2023) causal model from task + interruption + mediators to emotional outcome.
- `fig02_tam_model.png` — Davis (1989) Technology Acceptance Model showing the usefulness vs. ease-of-use split.
- `fig04_uz_ui_ux_layers.png` — UZ/UI/UX vagueness stack showing where direct vs. proxy measurement is possible.
- `fig05_usability_subqas.png` — Decomposition of usability into discoverability/learnability/efficiency/simplicity/understandability/flexibility.
- `fig07_mvc_recap.png` — MVC with 1—* cardinality between controller and view, explaining the re-skinning use case.
- `fig10_usability_for_whom.png` — Audience taxonomy (end-users vs. administrators vs. developers, with DevOps as a blur).
- `fig12_reference_architecture_eval.png` — Usability sub-QAs reapplied to evaluating a reference architecture from an architect's point of view.
- `fig21_usability_vs_power.png` — The trade-off picture: power-consumption optimisation affects responsiveness and efficiency, which are part of usability.
- `fig23_per_package_p_states.png` — P-states P0…Pm scaled per CPU package, supplied by BIOS via ACPI.
- `fig26_c_states.png` — C-states C0…Cm idle/sleep levels, also supplied via ACPI.
- `fig30_power_redundancy.png` — Power-decomposition example with one active machine and two redundancy machines, showing variable cooling cost.
- `fig31_graceful_degradation.png` — Three-level graceful degradation (100% → 60% → 25%) culminating in graceful shutdown as the battery drains.
- `fig33_preloading.png` — Preloading framed as escalating restart in reverse — levels 25%/60%/100% preload before full functionality.
- `fig34_offloading_prefetching.png` — Naive arrow diagram showing the opposite directions of offloading (work out) and prefetching (data in).

## Exam-relevant takeaways

**Lecturer's own exam guidance (from page 2):**
- Exam and re-exam both have **16 questions worth a total of 34 points**; **17 points** = passing grade 2.
- Questions are worth 1, 2, 3, 4 or 5 points.
- **Smartphones are allowed** for digitising drawings.
- Anything that appeared *in the lectures* may appear in the exam — slides alone are not sufficient; you must be able to **apply** what is in them.

**Likely exam content from L10 specifically:**
- Define usability and contrast it with a "technical" QA like performance.
- Draw / explain the **TAM model** and identify which of its dimensions Bass et al.'s tactics (cancel, undo, pause/resume, automation, personalisation) target.
- List **usability sub-QAs** and explain why "usability for whom?" matters.
- Distinguish **graceful shutdown, graceful degradation, forceful degradation** — with examples.
- Explain **P-states vs. C-states** and identify which earlier tactic they instantiate (resource throttling / scaling) and which they contradict (low-latency responsiveness).
- Give the **power-consumption decomposition** (computing + idle + cooling + loss) and reason about why idle power has a lower bound.
- Recommend **preloading, prefetching, offloading** as power tactics and explain the trade-offs they help with.
- Walk through **Bass et al.'s evaluation procedure** and the **contents of an evaluation report**.
- Recognise **dark patterns** as the ethical dimension of usability.
- Discuss **how to introduce a brand-new QA** when no body of knowledge exists (scenarios → transferability check → literature → stakeholders).

## Cross-references

- **Lecture 1 (foundations):** "design always aligns with technology" (Rams principle 1) and the business-factors / ROI items from Falessi et al. echo the project-level concerns introduced at the start of the course.
- **Lecture 2 (QA framework):** Lecture 10 *uses* the QA framework — sources/events/environments/responses/response-measures — to introduce both usability and power consumption. The "Bass et al. evaluation procedure" section is the natural conclusion of that framework.
- **Lecture 3 (Integrability + Modifiability):** MVC and Observer come straight back from L3, re-cast as **usability** patterns (re-skinning, A/B testing).
- **Lecture 4 (Testability + Deployability):** The Memento pattern is explicitly linked to the **rollback tactic** from L4. Graceful shutdown / degradation also resonate with deployability.
- **Lecture 5 (Availability):** Graceful degradation is a redundancy/availability tactic reused here for power. The "redundancy machines" picture (Fig. 30) is an availability diagram repurposed for power decomposition.
- **Lecture 6 (Performance):** The claim-check pattern from L6 is structurally similar to Memento. Preloading/prefetching tactics overlap with performance tactics; the responsiveness vs. power trade-off is the explicit bridge.
- **Lecture 7 (Scalability):** Offloading is the same primitive used for scaling; here it is repurposed for power. P-states / C-states are the hardware analogue of "scale resources" / "resource pooling".
- **Lecture 8 (Safety + Security pt 1):** Security tactics may *contradict* power tactics (encryption, validation cost CPU cycles); explicit trade-off discussed on page 61.
- **Lecture 9 (likely Security pt 2 / performance-throttling):** L10 explicitly re-frames "throttling" relative to what the previous lecture meant by it — on x86 throttling is now emergency-only; the everyday lever is P/C-states. This strongly suggests L9 covered throttling in a different (performance or thermal-protection) sense.
- **Course-wide:** The "introducing a new QA" section (pp. 62-63) is meta-advice that applies to *all* the QAs covered across the course — students should leave knowing the *process* of QA work, not just the QA catalogue.
