# Lecture 4: Testability and Deployability as Quality Attributes

> **Source:** lecture_4.pdf (88 pages)
> **Lecturer:** Jukka Ruohonen
> **Date (if stated):** March 3, 2026
> **Course:** Software Architecture (T630019402)

## Themes covered

1. **Testability as a quality attribute** — Bass et al.'s definition ("ease with which software can be made to demonstrate its faults"), Boehm's classic validation-vs-verification distinction, and why testability is itself something an architect must design for.
2. **The oracle problem** — what *is* a "correct answer" against which a test result is judged? Specified, pseudo-, implicit, and derived oracles.
3. **Fuzzing as an architectural concern** — the skeleton fuzzer loop, why it requires controllable input and observable state, and how performance assertions plug into the same loop.
4. **Testability tactics and patterns** — control/observe input and state vs. limit complexity; dependency injection, strategy, intercepting filter, type safety, and the open question of where LLMs fit.
5. **Deployability as a quality attribute** — making deployment predictable in time, effort, and outcome; cycle time, traceability, repeatability as the three measurable sub-attributes.
6. **Continuous integration, continuous deployment, DevOps / GitOps** — the pipeline as the architectural artifact, "X-as-code" as the cultural extension.
7. **Deployability tactics and patterns** — separate builds, scale roll-outs / canary, scripted deployment, rollback, feature toggles, safe-and-secure defaults; microservices, rolling upgrades, A/B testing, semantic versioning.
8. **Legal and resilience pressure on deployment** — EU Cyber Resilience Act (CRA) requirements for automatic, separated security updates; chaos engineering and tabletop disaster-recovery exercises.

## Concepts

### Testability (as a quality attribute)
**Definition:** The ease with which software can be made to demonstrate its faults (Bass et al. 2021), i.e. its susceptibility to being effectively tested.
**Why it matters:** Testability is *not* the same as "we have tests" — it is a property of the system itself that determines whether testing can ever be effective. If the system has low testability, no amount of testing effort will produce confidence.
**Detailed explanation:** Bass et al. frame testability against software *verification* ("building the product right") rather than against *validation* ("building the right product") — the Boehm 1984 distinction. The definition implicitly assumes that a fault exists; testability is then the inverse of the effort required to expose it. Ammann & Offutt (2008) give the practical implication: if testability is low and cannot be raised, the engineer has a defensible case to refuse to certify the artifact. So testability is both a design goal and a risk-management lever.
**Analogy:** Testability is like the *transparency* of an engine bay. Two cars may both have engines that will eventually fail, but one has clearly labelled diagnostic ports, a glass cover, and a "report" button that prints sensor readings — that car is *susceptible to inspection*. The other has a welded hood. Testing both is possible, but only one of them will *actually surface faults* during a workshop visit.
**Example:** A unit that hard-codes `now()`, network calls, and global config is not testable in any meaningful way — every test is non-deterministic. The same unit with `now`, `http_client`, and `config` injected through the constructor becomes testable.
**Common pitfall / nuance:** Students often equate "we have a big test suite" with "we have testability". The opposite can be true: a huge suite may simply paper over an untestable architecture, and the suite itself becomes a maintenance liability (the lecture explicitly notes tests cause maintenance overhead too).
**Related diagram:** `![Testability scenarios](../images/lecture_4/lecture_4_p08_testability_scenarios.png)`

### Verification vs. Validation (Boehm 1984)
**Definition:** *Verification* asks "are we building the product right?" (does the code match the spec); *validation* asks "are we building the right product?" (does the spec match user needs).
**Why it matters:** Testability concerns *verification*. You can have perfect testability and still ship the wrong product. The architect needs both, but the QA "testability" is narrower than it sounds.
**Detailed explanation:** This is the historical distinction students must recognise on the exam. Verification is internal: tests, assertions, fuzzing, static analysis. Validation is external: user research, acceptance tests, requirements review.
**Analogy:** Verification is "the cake matches the recipe". Validation is "the customer wanted a cake at all, not a pie".
**Example:** A microservice with 100 % branch coverage that perfectly implements an obsolete protocol — verified but invalid.
**Common pitfall:** Confusing the two in exam answers about QAs.

### Testability Scenarios (the six-part template)
**Definition:** A Bass-style scenario describing testability using six slots: Source, Stimulus (Event), Environment, System (the artifact under test), Response, Response Measure.
**Why it matters:** Forces an architect to make testability *measurable* and *falsifiable*, not aspirational.
**Detailed explanation:** Source = who runs the test (in-house, external testers, third parties); Stimulus = the test type (unit, fuzz, integration, acceptance, penetration, performance); Environment = where in the lifecycle (development, integration, production); System = scope (entire system / set of machines / modules / classes); Response = pass/fail/timeout/state captured; Response measure = coverage, time, money, stop-criteria heuristics.
**Analogy:** It is a six-axis fingerprint of a test situation, like an aviation pre-flight checklist — every slot must be answered before testability is well-defined.
**Example:** "An in-house developer (source) launches a fuzz test (stimulus) in the integration environment (environment) against the entire system (artifact); execution traces of test failures must be captured (response), with approximate coverage reported and a cap of 4 CPU-hours (response measure)."
**Common pitfall:** Treating the template as paperwork instead of as a design constraint generator.
**Related diagram:** `![Testability scenario template](../images/lecture_4/lecture_4_p08_testability_scenarios.png)`

### The Oracle Problem
**Definition:** The problem of deciding, for a given input, whether the program's output is correct — i.e. of having an authoritative judge ("oracle") for test outcomes.
**Why it matters:** Tests without oracles are theatre. The oracle, not the input, is the limiting reagent in most testing.
**Detailed explanation:** Barr et al. (2015) catalogue four oracle types:
1. **Specified oracles** — the textbook case: `1 + 1 == 2`, `f(x) > 0 ∀ x`.
2. **Pseudo-oracles** — a separate, independent implementation; reference architectures can serve as pseudo-oracles.
3. **Implicit oracles** — what *any* program must not do (crash, buffer-overflow, deadlock). Fuzzers lean heavily on these.
4. **Derived oracles** — extracted from external artifacts: standards, protocols, requirements documents, user feedback, runtime behaviour.
**Analogy:** A spelling bee judge. A specified oracle is a printed dictionary; a pseudo-oracle is a second judge who learned the language independently; an implicit oracle is "if the contestant screams, it's wrong"; a derived oracle is "the regional accent guide says this pronunciation is acceptable".
**Example:** Fuzzing the Linux kernel uses an implicit oracle (kernel oops = bug). Testing an HTTPS implementation uses a derived oracle (the RFC).
**Common pitfall:** Assuming every test can have a specified oracle — most can't, which is why fuzz testing and metamorphic testing exist.

### Stop Criterion (the "when do we stop testing?" problem)
**Definition:** The decision rule for terminating a testing activity, given that exhaustive testing is impossible.
**Why it matters:** Without an explicit stop criterion, testing is either over-invested (diminishing returns) or under-invested (premature ship).
**Detailed explanation:** Heuristics include coverage thresholds (e.g. via `coverage.py`), time budgets, statistical reliability models (non-homogeneous Poisson process for bug arrivals). All are approximations; none are correct.
**Analogy:** It is the testing equivalent of "when is a stew done?" — there is no analytic answer, only experienced cooks with timers and tasting spoons.
**Common pitfall:** Treating 100 % line coverage as a stop criterion. Coverage is necessary, not sufficient — covered lines may still hide bugs along uncovered *paths*.

### Fuzzing (skeleton model)
**Definition:** An automated dynamic testing technique that repeatedly generates inputs from a seed corpus and feeds them to a program, watching for crashes, deadlocks, or other implicit-oracle violations.
**Why it matters:** Fuzzing is the canonical demonstration that testability tactics (controllable input, observable state, assertions) pay off — every successful fuzzer is built on them.
**Detailed explanation:** The skeleton loop is: while true { input = generate(seed); run(program, input); if crash → fail; if time > threshold → fail (deadlock) }. The internal state can feed back to the input generator (coverage-guided fuzzing). Extensions add latency thresholds, load thresholds — performance QAs verified via the same harness.
**Analogy:** A monkey at a typewriter, but the monkey reads the previous page and is rewarded when it crashes the printing press. Add a stopwatch and a fuel gauge — now it also flags slow and overheating runs.
**Example:** Google's OSS-Fuzz, syzkaller for the Linux kernel (used in Ruohonen & Rindell 2019 to study time-to-fix of kernel bugs).
**Common pitfall:** Believing fuzzing replaces unit tests. Fuzzing is excellent at implicit-oracle bugs; it cannot tell you that `tax_total` is off by 0.5 %.
**Related diagram:** `![Fuzzing skeleton](../images/lecture_4/lecture_4_p15_fuzzing_skeleton.png)`

### Testability Tactics: Control and Observe Input & State
**Definition:** A family of architectural tactics that make a program's inputs controllable from outside and its internal state observable from outside.
**Why it matters:** Every testing technique above — unit tests, fuzzing, integration tests — relies on these. They are the architectural prerequisites of testing.
**Detailed explanation:** Six concrete tactics from Bass et al. 2021:
1. **Input generation** — automated input creation (fuzz, mutation, model-based).
2. **Record and play** — capture inputs/state so a failure can be replayed; reproducibility is "one of the grand challenges", especially for distributed systems and LLM-based tests.
3. **Special interfaces** — `get()`, `set()`, `report()`, `print_debug()`, `reset()` exposed only under a testing flag. The lecture's `#ifdef TESTING` snippet is the canonical example. Warning: special interfaces enlarge the attack surface.
4. **Localized storage** — put state somewhere it can be snapshotted (especially important in distributed systems).
5. **Assertions** — preconditions, postconditions, intermediate-state checks. Fuzzers love assertions because each one is a free implicit oracle. The lecture shows speculative extensions like `ASSERT_FUTURE_STATE(10s) == SHUTDOWN` or `ASSERT_PROBABILITY(model, test_set) > 0.7`.
6. **Sandboxes** — run tests in isolation (VM, container, jail) so they cannot disturb the host or production state.
**Analogy:** A chemistry lab bench with calibrated burettes (input generation), CCTV (record and play), dedicated probe ports (special interfaces), labelled reagent cabinets (localized storage), pH paper at every step (assertions), and a fume hood (sandbox). Take any one away and the lab becomes untestable.
**Common pitfall:** Adding `get_`/`set_` for *everything* without conditional compilation — production binaries then ship with debugging back-doors.
**Related diagram:** `![Testability tactics tree](../images/lecture_4/lecture_4_p19_testability_tactics_tree.png)`

### Testability Tactics: Limit Complexity (and Determinism)
**Definition:** Tactics that reduce the number of states, dependencies, and non-deterministic interactions in a system, with the explicit goal of making tests reproducible.
**Why it matters:** Complex systems contain more bugs *and* are harder to test for them — a multiplicative penalty. Determinism, in particular, is what makes tests trustworthy.
**Detailed explanation:** Carries over earlier-lecture techniques: encapsulation, dependency reduction. Adds: large systems have an irreducible stochastic element, which is why the NetBSD test suite uses *flagged oracles* — tests can be tagged "expected failure due to a known difficult bug" or "sometimes fails on ARM64/MIPS for unknown reason". This is honest acknowledgement that perfect determinism is unattainable.
**Analogy:** A clockmaker reduces a watch to as few moving parts as possible — not because they enjoy minimalism, but because each gear they remove is one fewer thing that can stick.
**Common pitfall:** Treating flaky tests as "ignore the red light" rather than as evidence of insufficient complexity-limitation.

### Regression Testing
**Definition:** A test whose explicit purpose is to detect that a previously-fixed bug has returned.
**Why it matters:** Bridges testing with documentation and complexity management — regression tests are organisational memory.
**Detailed explanation:** A *regression* in testing terminology is "something that used to work and no longer works". Convention: when you fix a bug, add a regression test. Ruohonen & Alami (2024) show that in the Linux kernel between 2021–2024 the bulk of regression bugs concentrates in `drivers` and `fs` subsystems — useful intelligence about where to focus regression effort.
**Analogy:** A vaccination scar. The body remembers the previous attack and rejects it on sight.
**Example:** A bug that NetBSD developers fixed in 2012; without a regression test recording the failure mode, no one in 2026 would remember it exists.
**Common pitfall:** Treating regression tests as second-class; they are arguably the most valuable tests because each one is a documented "lesson learned".

### Testability Pattern: Dependency Injection
**Definition:** A construction technique in which a function or object receives the collaborators it needs (services, configs, clocks) as parameters instead of constructing them itself.
**Why it matters:** It is the single highest-leverage testability pattern. Without it, controllable inputs and observable state are essentially impossible to retrofit.
**Detailed explanation:** Trade-off: a small amount of boilerplate and indirection in exchange for the ability to swap in test doubles, mocks, spies. The lecture's Python `__init__(self, x)` example shows the minimum viable form.
**Analogy:** A power tool with interchangeable bits vs. a power tool with a welded bit. The first is universal; the second is a museum piece.
**Common pitfall:** Going to the other extreme — every collaborator passed through several layers of injection container — until the configuration *itself* becomes untestable.

### Testability Pattern: Strategy Pattern
**Definition:** A design pattern in which a behaviour is selected at runtime from a family of interchangeable implementations behind a common abstract interface.
**Why it matters:** Lets a test substitute a known, simple strategy for a complex production one. Same hook as dependency injection, but at the algorithm level.
**Detailed explanation:** Lecture's example: a `switch(type)` over `RANDOM_FOREST`, `SUPPORT_VECTOR_MACHINE`, etc. Readability can suffer when the number of strategies grows.
**Analogy:** Camera lenses — same body, swappable optics. Tests can fit a "lens cap" lens.

### Testability Pattern: Intercepting Filter
**Definition:** A pattern in which pre- and post-processing filters are injected around a function's primary method.
**Why it matters:** Provides a uniform place to add cross-cutting concerns — logging, assertions, instrumentation — without modifying the primary method.
**Detailed explanation:** Code shape: `if pre: pre(x); z = g(x); if post: post(z)`. The pre-filter is where you assert preconditions and capture inputs; the post-filter is where you assert postconditions and capture outputs.
**Analogy:** Airport security and customs — every passenger goes through the same checks before and after the flight, without the airline having to embed them in flight operations.

### Testability Pattern: Type Safety
**Definition:** Using a strongly typed language, or type annotations in a weakly typed one, so that static analysis can catch defects before runtime.
**Why it matters:** Shifts entire classes of bugs (wrong-type arguments, null-deref) into the compile phase, dramatically reducing what dynamic tests must cover.
**Detailed explanation:** Type information also enables taint analysis (tracking "tainted" user input across the program). The lecture warns: Python's annotations are *not enforced* — `assert type(x) == int` is needed for actual runtime checking.
**Analogy:** A jigsaw puzzle where pieces only physically fit in the correct slots; you cannot construct a wrong picture even if you try.
**Common pitfall:** Believing type annotations equal type *enforcement* in Python.

### Testability Pattern: LLMs and Verification Debt
**Definition:** The emerging practice (and risk) of using LLMs to generate, verify, or repair test artifacts; "verification debt" (Bouzoukas 2026) is the accumulating burden of un-verified LLM output.
**Why it matters:** LLMs are eroding the assumption that the developer has actually read what they shipped. The architect now needs deliberate independence between LLM-generated code and the things that verify it.
**Detailed explanation:** The lecture is sceptical of the "LLM generates, another LLM verifies" loop — both can be wrong in correlated ways. The safer pattern is to keep validation *outside* the LLM: static analysis, unit tests written by humans, integration tests with deterministic oracles. The Chou et al. (2025) vignette captures the problem: a vibe coder caught the LLM writing tests so that "all the tests are passing, but it probably wrote the tests [so it can pass]". Security debt is called out as a sub-debt of verification debt because LLMs ship insecure code with high probability and that code propagates through supply chains.
**Analogy:** Asking a student to mark their own exam — and then asking a second copy of the same student to mark it again. Two reviews, one bias.
**Example:** The "safe" pipeline (lecture Fig. 18): LLM generates → static analysis + unit tests + integration tests → fail back to re-generate or manual fix. Validation stays human/deterministic.
**Common pitfall:** Trusting LLM-generated tests as ground truth without an independent oracle.
**Related diagram:** `![LLM generation with independent validation](../images/lecture_4/lecture_4_p41_llm_with_independent_validation.png)`

### Deployability (as a quality attribute)
**Definition:** The property that a developed system can actually be deployed into production with a predictable and acceptable amount of time and effort (Bass et al. 2021).
**Why it matters:** Traditional release engineering was slow, manual, and unpredictable. Deployability turns "release" into a measurable QA — and the pipeline into an architectural artifact in its own right.
**Detailed explanation:** Note Ruohonen's pedagogical aside: "deployability" is not in dictionaries; treat it operationally. The QA has three measurable sub-attributes (Bass et al.):
1. **Cycle time** — time from a developer commit to production deployment.
2. **Traceability** — can you trace forward (commit → production) and backward (production → commit)?
3. **Repeatability** — given the same artifacts, does the pipeline always produce the same outcome? ("Easier said than done even with respect to builds alone!" — reproducible-builds.org exists exactly because this is hard.)
**Analogy:** Deployability is the *logistics* discipline of software. The product (code) might be great, but if shipping takes six weeks and packages arrive damaged 30 % of the time, the business fails.
**Common pitfall:** Equating "we deploy frequently" with deployability. Frequency is the *result*; predictability and effort are the QA.

### Continuous Integration (CI), Continuous Deployment (CD), DevOps, GitOps
**Definition:** Practices for continuously building, testing, and deploying a system. CI = continuous build + test, CD = continuous deployment to production, DevOps = the cultural/operational umbrella, GitOps = Git as the single source of truth for both code *and* operational state.
**Why it matters:** They are the implementation of deployability — the mechanism by which cycle time, traceability, repeatability are achieved in practice.
**Detailed explanation:** Requires *separating environments*: development → integration → staging → production. The pipeline picture (Fig. 21) is commit → merge → integrate/build → run tests, deploy → generate feedback, with longer-running tests deferred to later stages. "Rapid releases" is a related (older) term. The extension is "X-as-code" — pipeline-as-code, infrastructure-as-code, and the newer family (Wei et al. 2025): compliance-as-code, security-as-code, configuration-as-code, network-as-code. Lecture's provocation: "Do you think 'everything as code' might be the future?"
**Analogy:** A factory conveyor belt. You don't ship the prototype the engineer just finished; you ship whatever just rolled off the end of the belt, having passed every QC station automatically.
**Common pitfall:** Confusing CI with CD. CI ensures *a* working build always exists; CD pushes it to users.
**Related diagram:** `![CI/CD pipeline](../images/lecture_4/lecture_4_p48_ci_cd_pipeline.png)`

### Deployability Tactics: Manage Pipeline
**Definition:** Architectural moves that shape the build/deploy machinery itself.
**Why it matters:** Without these, the pipeline becomes the bottleneck.
**Detailed explanation:** Four tactics:
1. **Separate builds** — refactor a "big ball of mud" component into modules built in parallel; any module change triggers only its own build. (Lecture Fig. 26 / p54.)
2. **Scale roll-outs (canary)** — deploy to a small subset of users first, watch health metrics, then expand. With very large systems, define multiple subsets by geography or configuration. Sheehy & Reed (2025) recommend pre-defined health metrics and a documented verification plan.
3. **Script deployment** — automate everything possible; manual config should be a last resort.
4. **Rollback** — be able to revert to the previous version. Requires traceability and repeatability — every config and variability axis must be tracked so the previous state is reconstructible. The lecture shows ZFS rollback as a filesystem-level analogue.
**Analogy:** A factory's continuous-improvement (kaizen) toolkit: break monoliths into stations, test new methods on one line before rolling fleet-wide, automate the line, and keep a quick "undo" lever.
**Common pitfall:** Treating canary as "deploy and pray". Canary without health metrics and an abort criterion is just slow blast-radius.
**Related diagram:** `![Deployability tactics tree](../images/lecture_4/lecture_4_p53_deployability_tactics_tree.png)` and `![Separate builds tactic](../images/lecture_4/lecture_4_p54_separate_builds.png)`

### Deployability Tactics: Manage Deployment
**Definition:** Tactics governing the *target* side of deployment — the running system.
**Why it matters:** Even with a perfect pipeline, runtime interactions, version mixes, and on/off feature states can wreck a deployment.
**Detailed explanation:**
- **Multi-version interaction** — clients reach servers through a proxy/bridge, and different server instances may run different versions/configurations simultaneously. This is the substrate for rolling upgrades.
- **Feature toggle** — runtime switch to enable or disable a feature; "kill-switch" is a special case.
- **Secure defaults** — Ruohonen 2025: functional features off by default, security features on by default. Trade-off-free heuristic for the *default* state.
**Analogy:** A theatre rigged so each light, sound cue, and prop can be turned on or off live without rebuilding the set. Defaults: house lights on, fire suppression armed.
**Common pitfall:** Shipping features behind toggles and never deleting the dead branches — the toggle graveyard becomes its own complexity tax.
**Related diagram:** `![Multi-version servers behind a bridge](../images/lecture_4/lecture_4_p58_multi_server_versions.png)`

### Deployability Pattern: Microservices
**Definition:** An architectural style where the system is decomposed into many small, independently deployable services.
**Why it matters:** Treated here primarily as a *deployment* pattern: it optimises for distributed development and deployability rather than for run-time efficiency.
**Detailed explanation:** Benefits (in the lecture's framing): (1) distributed development and deployment — teams can pick languages and deploy independently as long as interfaces stay compatible, reducing integration errors and time-to-market; (2) elastic scaling — instances added dynamically to match demand. Drawbacks: (1) overhead larger than in-memory connectors; (2) complex transactions are hard to synchronise; (3) heterogeneity raises whole-system complexity; (4) deciding service granularity is hard; (5) service catalogs and SBOMs (Software Bill of Materials) cause overhead.
**Analogy:** A food court vs. a single full-service restaurant. The food court can swap vendors, scale popular stalls, and let each kitchen choose its tools — but ordering one meal across several stalls is awkward, and the management of vendor contracts (SBOMs) becomes a job in itself.
**Common pitfall:** Adopting microservices for the deployability benefit without paying the complexity cost — common at small organisations.

### Deployability Pattern: Rolling Upgrades
**Definition:** Upgrading a fleet of server instances incrementally — replace some, watch, replace more — so that the system remains available throughout.
**Why it matters:** Combines deployability with availability; no maintenance window required.
**Detailed explanation:** Two flavours shown:
1. **In-place rolling upgrade** — at each step, a percentage of *server instances* is moved to the new version. Step 1: 100 % old. Step 2: 50 % new (instances). Step 3: 100 % new (instances). Step 4: old removed. Bridge/proxy routes uniformly.
2. **Traffic-split rolling upgrade** — both versions run, the *proxy* sends a percentage of *traffic* (10 %, 50 %, 90 %, 100 %) to the new version; old instances are drained later. This is the more flexible variant and is what blue-green and canary deployments inherit from.
**Analogy:** Replacing the wheels on a moving lorry one at a time vs. taking detours through a new lorry parked alongside until everyone has migrated.
**Common pitfall:** Forgetting backward compatibility of data formats — during a rolling upgrade, old and new versions read/write the same database.
**Related diagram:** `![Rolling upgrade start state](../images/lecture_4/lecture_4_p64_rolling_upgrade_start.png)`

### Deployability Pattern: A/B Testing
**Definition:** Routing different subsets of traffic to two feature variants for a fixed time, then deciding which to keep using statistical tests.
**Why it matters:** Couples deployment with experimentation; turns the production system into an evidence-producing instrument.
**Detailed explanation:** Phase 1: 50 % to Feature A, 50 % to Feature B for time *t*. Phase 2: after t-tests (or similar), 100 % to the winner. The same machinery (multi-version interaction, proxy routing) underlies rolling upgrades and A/B testing; the difference is intent — rollout vs. measurement.
**Analogy:** Two recipes served in alternating sittings, then the kitchen keeps whichever got more clean plates.
**Common pitfall:** Stopping the test as soon as A looks better ("peeking") — statistical validity demands the test run for the pre-declared duration.
**Related diagram:** `![A/B testing split](../images/lecture_4/lecture_4_p72_ab_testing_split.png)`

### Cyber Resilience Act (CRA) — security updates as a deployment requirement
**Definition:** EU regulation enforceable from 2027 mandating security update delivery throughout a product's life cycle, automatic by default when technically feasible and opted into, and separated from functional updates.
**Why it matters:** External legal pressure now drives deployability architecture — a system that cannot deliver security updates separately is illegal to sell in the EU.
**Detailed explanation:** The lecture's Fig. 5 from Ruohonen et al. 2025 shows the decision tree: an update is classified Security vs. Functional; security updates take the automatic-delivery route when (1) applicable, (2) opted in, (3) no postponing has ended, otherwise the manual route; both routes require secure delivery (integrity). Functional updates take the manual route by default; the two streams must be separated where technically feasible.
**Analogy:** Like food labelling — the regulator dictates not what you cook, but how you package and ship it, and "I forgot" is no longer a defence.
**Example:** Operating system updates today often bundle features and security fixes; the CRA pushes for separate "security-only" packages that can be opted into independently.
**Common pitfall:** Treating CRA as a documentation issue; it is an *architecture* issue (separate channels, automatic delivery, integrity).
**Related diagram:** `![CRA security update flow](../images/lecture_4/lecture_4_p75_cra_security_updates.png)`

### Release Engineering and Semantic Versioning
**Definition:** The discipline of structuring releases over time: major, minor, and patch releases, with long-term-support (LTS) and short-support branches running in parallel.
**Why it matters:** Continuous deployment does not mean "one moving target". Most real systems must support multiple parallel release lines with different cadences and lifespans.
**Detailed explanation:** Lecture's mental model (Fig. 41):
- **Major release** (e.g. 1 → 2) every ~5 years; potentially breaking.
- **Minor release** (1.x) every ~6 months; backward-compatible additions.
- **Patch release** (1.x.y) "whenever necessary"; bug/security only.
Each version has a release date and an end-of-life. LTS versions typically do not receive new features.
**Analogy:** A car model line — the 1998 model is still serviced (LTS) with safety recalls, but no one is adding a touchscreen to it; new features go into the 2024 model.
**Common pitfall:** Believing CD makes versioning obsolete. It doesn't — it makes patch versions trivial, not unnecessary.
**Related diagram:** `![Semantic versioning over time](../images/lecture_4/lecture_4_p77_semantic_versioning.png)`

### Chaos Engineering and Tabletop Exercises
**Definition:** Deliberately injecting faults or stressors into a production-like system (chaos engineering) or walking through disaster scenarios on paper (tabletop) to test deployability and resilience.
**Why it matters:** Closes the loop on deployability — "we can deploy" must also mean "we can survive things going wrong during/after deployment".
**Detailed explanation:** Process (Fig. 44): Experiment design — declare (1) steady state, (2) hypothesis, (3) blast radius; choose a fault/stressor; execute; observe and analyse. The "principles of chaos" (principlesofchaos.org) and tooling (chaostoolkit.org) operationalise this; tabletop exercises (USENIX ;login: article cited) are the paper-based dry-run analogue.
**Analogy:** Fire drills for software. You don't wait for a real fire to discover that the alarm is broken.
**Example:** Netflix's Chaos Monkey terminates random instances in production. Tabletop: "what if the primary database is unreachable for 30 minutes during a deploy?"
**Common pitfall:** Running chaos exercises with no blast-radius cap — turning a drill into the disaster.
**Related diagram:** `![Chaos engineering setup](../images/lecture_4/lecture_4_p80_chaos_engineering_setup.png)`

### Safe and Secure Defaults
**Definition:** The design heuristic that out-of-the-box, functional/optional features are OFF and security/protective features are ON.
**Why it matters:** Most users never change defaults. Defaults *are* the policy.
**Detailed explanation:** Drawn from Ruohonen 2025. Pairs naturally with feature toggles — the toggle exists, but its default is conservative.
**Analogy:** A new car comes with seatbelts engaged and the panic alarm armed; the heated steering wheel is off.
**Common pitfall:** Inverting the heuristic to make demos look good — features ON, security OFF — and then forgetting to flip them for shipping.

## Important diagrams (catalog)

- `lecture_4_p08_testability_scenarios.png` — six-part Bass-style template for testability scenarios (Source / Event / Environment / Artifact / Response / Response measure), with example values in each slot.
- `lecture_4_p15_fuzzing_skeleton.png` — the canonical fuzzing loop: seed → input generator → program → crash/panic; plus a deadlock-detection arm via a time threshold.
- `lecture_4_p19_testability_tactics_tree.png` — Bass et al.'s testability tactics tree: two branches (control/observe input and state with six sub-tactics; limit complexity with source-code and determinism).
- `lecture_4_p41_llm_with_independent_validation.png` — the "safe" LLM-coding pipeline: LLM generates → independent static analysis + unit + integration tests verify → re-generate or manual fix on failure. Keeps validation outside the LLM.
- `lecture_4_p48_ci_cd_pipeline.png` — continuous-integration/deployment pipeline: commit → merge → integrate/build → run tests / deploy / defer longer tests → feedback.
- `lecture_4_p53_deployability_tactics_tree.png` — deployability tactics tree: manage pipeline (separate builds, scale roll-outs, script deployment, rollback) vs. manage deployment (interactions, feature toggle, secure defaults).
- `lecture_4_p54_separate_builds.png` — refactoring a "big ball of mud" component into independently-built modules so any single module change triggers only its own parallel build.
- `lecture_4_p58_multi_server_versions.png` — multiple server instances behind a bridge/proxy, each running a different version or configuration — the substrate for rolling upgrades and A/B testing.
- `lecture_4_p64_rolling_upgrade_start.png` — starting state of a rolling upgrade: 100 % of traffic on the old version, single server class behind the proxy.
- `lecture_4_p72_ab_testing_split.png` — A/B testing routing: 50 % of requests to Feature A, 50 % to Feature B for a fixed time t, before a statistical decision.
- `lecture_4_p75_cra_security_updates.png` — EU Cyber Resilience Act decision flow: security updates vs. functional updates, automatic vs. manual delivery routes, secure-delivery (integrity) and opt-in/notification gates.
- `lecture_4_p77_semantic_versioning.png` — release-engineering timeline showing major / minor / patch releases with their typical cadences and end-of-life markers.
- `lecture_4_p80_chaos_engineering_setup.png` — chaos-engineering and tabletop experiment loop: design (steady state, hypothesis, blast radius) → choose fault/stressor → execute → observe and analyse.

## Exam-relevant takeaways

- **Testability ≠ tests.** Testability is a *property of the system* — its susceptibility to having faults exposed. The architect designs *for* testability; the tester exploits it.
- **Verification vs. validation (Boehm 1984)**: testability concerns verification ("building the product right"), not validation ("building the right product").
- **Six-slot scenario template** applies to both testability (lecture Fig. 1) and deployability (Fig. 24). Memorise the slots and example values.
- **Oracle taxonomy (Barr et al. 2015)**: specified, pseudo, implicit, derived. Fuzzers rely on implicit; standards-conformance testing relies on derived.
- **Testability tactics tree**: two branches — control/observe input & state (input generation, record & play, special interfaces, localized storage, assertions, sandboxes) and limit complexity (source code + determinism). Know all six sub-tactics.
- **Special interfaces and conditional compilation**: useful for testing but enlarge attack surface — guard with `#ifdef TESTING` or equivalent.
- **Testability patterns**: dependency injection, strategy, intercepting filter, type safety. Each one creates a hook where a test can substitute or observe.
- **LLM-aware testing**: verification debt is real (Bouzoukas 2026). Keep validation independent of generation; do not let an LLM mark its own homework.
- **Deployability** is measurable via three sub-attributes: **cycle time, traceability, repeatability**. Reproducible builds and rollback both depend on traceability + repeatability.
- **Continuous practices (CI/CD/DevOps/GitOps)** require *separated environments*: dev → integration → staging → production. "X-as-code" is the cultural extension.
- **Deployability tactics tree**: manage pipeline (separate builds, scale roll-outs / canary, script deployment, rollback) and manage deployment (interactions, feature toggle, secure defaults).
- **Rolling upgrades** come in two flavours: instance-replacement vs. traffic-split. A/B testing is the same machinery used for measurement rather than rollout.
- **Microservices** are presented here as a *deployment* pattern: gains distributed deployability and elastic scaling; pays in connector overhead, transaction synchronisation, heterogeneity, granularity decisions, and SBOM/catalog overhead.
- **CRA (2027)**: automatic + separated security updates with secure delivery and opt-in — a legal force on deployment architecture.
- **Release engineering**: parallel LTS and short-support branches; semantic versioning of major / minor / patch with distinct cadences and lifespans. CD does not abolish versioning.
- **Chaos engineering and tabletop exercises** validate deployability end-to-end — steady state, hypothesis, blast radius, execute, observe.
- **Safe and secure defaults**: functional features off by default, security features on by default (Ruohonen 2025).

## Cross-references

- Likely connects to **Lecture 3** (other QAs) — testability and deployability are presented as a *continuation* of the previous lecture's QA framework; the six-slot scenario template is reused.
- Likely connects to **Lecture 2 / earlier lectures** on **encapsulation, dependency reduction, modularity** — these are restated as foundations of both "limit complexity" (testability tactic) and "separate builds" (deployability tactic).
- Likely connects to a lecture on **architectural styles and patterns** — microservices appears here as a deployment pattern, but is independently treated as a structural style; the proxy/bridge of rolling-upgrade diagrams overlaps with **broker / mediator** patterns.
- Connects to **security as a QA** — the lecture deliberately threads in safe-and-secure defaults, the CRA, the attack-surface cost of special interfaces, security debt as a sub-debt of verification debt.
- Connects to **release engineering and product lines** — the "recall what was said about product lines and branching" reference points back to an earlier lecture (likely 2 or 3) on release lines.
- Likely connects to a later lecture on **observability / monitoring** — health metrics for canary, monitoring for rollback triggers, log-analysis and analytics for GitOps.
- Connects to **Case 4** assignments: syzkaller/syzbot (continuous fuzzing of the Linux kernel) and the CrowdStrike (2024) / Cloudflare (2025) incidents — applied case studies of testability and deployability failures and the lessons drawn from them.
