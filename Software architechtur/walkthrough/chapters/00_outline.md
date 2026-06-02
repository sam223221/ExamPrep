# Software Architecture Walkthrough — Chapter Outline

> Synthesized brief for the chapter writers. Drives the production of a ~120–180-page topic-organized study guide for the Software Architecture exam (course T630019402, Spring 2026, Jukka Ruohonen, SDU). The exam has 16 questions / 34 points / passing at 17; smartphones are allowed for digitising drawings; "anything that appeared in the lectures may appear in the exam — slides alone are not sufficient; you must be able to *apply*". The lecturer's own publications are likely material. The lecturer boldfaces *articulation and transferability of knowledge*, *stakeholder management*, and *communication / presentation / negotiation* as exam-counted soft-skill qualities (L1).

## Course map (one paragraph)

Software Architecture as taught here builds on Bass et al. 2021 ("Software Architecture in Practice") and Fairbanks 2010 ("Just Enough Software Architecture"), supplemented with Ruohonen's own publications (NetBSD test evolution, Linux kernel regression patterns, EU CRA mapping, secure defaults, agentic AI). Ten lectures progress from foundations (L1: vocabulary, views, SOLID-at-component-scope, layering) through the Quality-Attribute framework (L2: ASRs, scenarios, ISO/IEC 25010, risk, SBOM), then march through individual QAs lecture-by-lecture using a consistent definition → 6-slot scenario → tactics tree → patterns rhythm: Integrability + Modifiability (L3), Testability + Deployability (L4), Availability (L5), Performance (L6), Scalability (L7), Safety + Security part 1 (L8), Security part 2 (L9), Usability + Power Consumption + Architecture Evaluation (L10). Two case studies anchor everything: the Linux network stack poster (Case 1, Horvat) as a "find every pattern and tactic in one real system" exercise, and the Kreuzberger et al. MLOps reference architecture (Case 3) as a "design an end-to-end reference architecture" exercise. The course's exam style favours scenario-based answers, drawn diagrams (often photographed via smartphone), and concise *prioritised* discussion of trade-offs.

## Chapter list (one row per chapter)

| # | Title | Target pages | Primary sources | Writer brief file |
|---|---|---|---|---|
| 1 | Foundations — What Architecture Is, the Ten-Term Vocabulary, Views, SOLID at Component Scope, Layering | 14 | L1 + supporting refs from L2 | `01_brief.md` |
| 2 | The Quality-Attribute Framework — ASRs, Scenarios, ISO/IEC 25010, Risk, SBOM, Domain Modeling | 12 | L2 + L1 | `02_brief.md` |
| 3 | Integrability — Dependencies, Size × Distance, Tactics Tree, Observer vs Pub-Sub, Wrapper/Bridge/Mediator | 12 | L3 (integrability half) | `03_brief.md` |
| 4 | Modifiability — Maintenance Economics, Six Planning Questions, Five Moves, Defer Binding, Semantic Versioning, Patterns | 12 | L3 (modifiability half), refs from L4 (semver) | `04_brief.md` |
| 5 | Testability — Oracle Problem, Fuzzing, Control/Observe, Limit Complexity, Patterns, LLM Verification Debt | 10 | L4 (testability half) | `05_brief.md` |
| 6 | Deployability — CI/CD/DevOps/GitOps, Rolling Upgrades, A/B, Chaos, CRA Security Updates | 12 | L4 (deployability half) | `06_brief.md` |
| 7 | Availability — Fault/Failure/Trigger, the Nines, Detect/Repair/Reintroduce/Prevent, Saga, Bulkhead, Spares | 14 | L5 | `07_brief.md` |
| 8 | Performance — Latency vs Throughput, CAP/PACELC, Caching Topologies, Throttling, Scheduling, MapReduce, Claim-Check | 14 | L6 | `08_brief.md` |
| 9 | Scalability — Amdahl, Kubernetes, Gateway/Sidecar, Horizontal vs Vertical, CDN/SDN, Latency Decomposition, Bondi | 13 | L7 | `09_brief.md` |
| 10 | Safety and Security Part 1 — Safety Tactics, Monitor-Actuator, CIA, SIEM, Input Validation, Agentic AI Trust Boundaries, Privilege Drop | 14 | L8 | `10_brief.md` |
| 11 | Security Part 2 — Microsoft SDL, Threat Modeling, Kill Chain, Zero-Trust + Sidecar, MitM, Cryptography Lifecycle | 13 | L9 | `11_brief.md` |
| 12 | Usability and Power Consumption — TAM, Sub-QAs, Dark Patterns, P-States/C-States, Graceful Degradation | 10 | L10 (first 2/3) | `12_brief.md` |
| 13 | Pattern + Tactic Reference — Cross-QA Tactics-Tree Comparison and Alphabetical Pattern Catalog | 10 | All lectures | `13_brief.md` |
| 14 | Architecture Evaluation and Introducing New QAs — Bass Procedure, Falessi Factors, ACM Criteria, Rams' Ten Principles, Evaluation Reports | 6 | L10 (last 1/3) + L2 | `14_brief.md` |
| 15 | Case Study Walkthrough 1 — The Linux Network Stack (Horvat Poster) | 10 | case_1 + L1/L3/L7 | `15_brief.md` |
| 16 | Case Study Walkthrough 2 — MLOps Reference Architecture (Kreuzberger et al.) | 10 | case_3 + L3/L4/L6/L7 | `16_brief.md` |
| 17 | Exam Preparation — Question Archetypes, Walkthrough Strategies, Drawing Conventions, Soft-Skill Section | 8 | All lectures + L10 exam guidance | `17_brief.md` |

**Total estimated pages:** ~184 (front matter + back matter add ~12 more pages — within the 120–180 main-text band when adjusted for diagram density).

## Per-chapter detailed briefs

### Chapter 1: Foundations — What Architecture Is, the Ten-Term Vocabulary, Views, SOLID at Component Scope, Layering

**Target pages:** ~14
**Sources to draw from:** lecture_1_analysis.md (primary); secondary cross-refs to lecture_2 for the QA-tension idea.
**Goal:** After reading, the student can (a) recite Bass-Clements-Kazman's definition of software architecture verbatim, (b) place any decision into the design / architecture / implementation pyramid and justify why it is architectural, (c) use the ten-term vocabulary precisely, (d) draw a Kruchten 4+1 sketch for a sample system, (e) apply the Liskov-style component substitution rule and recognise violations, (f) identify cohesion / segregation / SRP / OCP / no-vendor-lock-in violations on a diagram, (g) explain layered architecture using the OS or manufacturing-automation example, (h) distinguish system from enterprise architecture, and (i) reproduce the lecturer's claim that the top three architect-job qualities are communication-related.

**Concepts to cover (with the source analysis where each is defined):**
- Bass-Clements-Kazman definition of software architecture (elements + relations + properties, plural structures, for *reasoning*) — `lecture_1_analysis.md` §Software architecture (the working definition)
- Six truisms (Bass et al.) — `lecture_1_analysis.md` §Six truisms about software architecture
- Design vs Architecture vs Implementation pyramid, "tensions" — `lecture_1_analysis.md` §Software design, software architecture, and implementation
- Quality attributes as the *prioritised* drivers of architecture (set up here, fully developed in Ch 2) — `lecture_1_analysis.md` §Quality attributes
- Two flavours of constraints (incoming vs imposed; inhibit vs exhibit) — `lecture_1_analysis.md` §Constraints (two flavors)
- Twin Peaks model (Cleland-Huang) including the mountain-range variant — `lecture_1_analysis.md` §The Twin Peaks model
- Ten-term vocabulary: module, interface, component, process, machine, system, deployment, environment, element, connector — `lecture_1_analysis.md` §The ten-term vocabulary
- Component structures (cohesion, encapsulation, reuse, substitutability, deployability, composability) — `lecture_1_analysis.md` §Component structures
- Views & viewpoints, Fairbanks's view operations (projection, partition, composition, classification, generalization, designation, refinement, binding, dependency) — `lecture_1_analysis.md` §Views and viewpoints
- Kruchten 4+1 viewpoints (Logical / Development / Process / Physical / +Scenarios) — `lecture_1_analysis.md` §Views and viewpoints
- The substitution principle for components (Liskov generalised; provided OK to extend, required must not be extended) — `lecture_1_analysis.md` §The substitution principle
- Cohesion + no-vendor-lock-in corollary — `lecture_1_analysis.md` §Cohesion (and the vendor lock-in corollary)
- Segregation (interface segregation) — `lecture_1_analysis.md` §The segregation principle
- Single Responsibility and Open-Closed at component scope — `lecture_1_analysis.md` §Single responsibility and open-closed principles
- Module structures and the data-vs-compute separation — `lecture_1_analysis.md` §Module structures and the data-vs-compute separation
- Layered structures (strict neighbour-only) — OS and manufacturing examples — `lecture_1_analysis.md` §Layered structures
- System architecture vs enterprise architecture — `lecture_1_analysis.md` §System architecture vs. enterprise architecture
- The software architect's role and the top three communication-related qualities — `lecture_1_analysis.md` §Software architect (the role)

**Diagrams to embed (path + caption):**
- `../images/lecture_1/lecture_1_p28_img1_design_arch_implementation_pyramid.png` — Design / architecture / implementation with the "tensions" arrows (requirements, constraints, domain knowledge, QAs). Anchor diagram for "where each decision lives".
- `../images/lecture_1/lecture_1_p33_img1_two_types_of_constraints.png` — The two flavours of constraints (incoming vs imposed on implementation); used to make the inhibit / exhibit distinction stick.
- `../images/lecture_1/lecture_1_p36_img1_twin_peaks_mountain_range.png` — The realistic mountain-range version of Twin Peaks; killer counter-example to waterfall.
- `../images/lecture_1/lecture_1_p40_img1_concepts_components_modules_connectors.png` — The ten-term vocabulary illustrated; reference figure students will return to all course.
- `../images/lecture_1/lecture_1_p46_img1_client_server_component_diagram.png` — The flight + hotel reservation reservation example, UML component form. Running example for the rest of the book.
- `../images/lecture_1/lecture_1_p52_img1_decomposition_vs_clientserver_view.png` — Decomposition view vs client-server view of the same system; concrete instance of "multiple views per architecture".
- `../images/lecture_1/lecture_1_p53_img1_sync_async_notations.png` — Four sync/async notations (Richards 2015); short paragraph saying "any style works as long as you're consistent."
- `../images/lecture_1/lecture_1_p54_img1_kruchten_4plus1_views.png` — Kruchten 4+1 viewpoints with stakeholder labels. Use it as the canonical 4+1 figure that recurs whenever the book mentions a "view".
- `../images/lecture_1/lecture_1_p56_img1_substitution_principle_example.png` — Substitution Q1 (A ↔ B with the same interfaces).
- `../images/lecture_1/lecture_1_p60_img1_liskov_component_substitution.png` — Formal substitution rules (more provided OK, more required NOT OK).
- `../images/lecture_1/lecture_1_p64_img1_segregation_principle.png` — Segregation + vendor-lock-in violation on the Server component (extra "Run ads" and "Do marketing").
- `../images/lecture_1/lecture_1_p69_img1_ensemble_learning_architecture.png` — Data/Algorithm separation in a minimal ensemble-learning sketch; bridges to ML-architecture content of Case 3.
- `../images/lecture_1/lecture_1_p72_img1_layered_operating_system.png` — Classical layered OS (hardware → drivers → kernel → syscalls → libs → programs).
- `../images/lecture_1/lecture_1_p74_img1_layered_manufacturing_automation.png` — Five-layer manufacturing automation (Sensors → PLC → SCADA → MES → ERP); useful contrast to the OS example.
- `../images/lecture_1/lecture_1_p77_img1_healthcare_emergency_system_sketch.png` — Healthcare emergency-system sketch with explicit availability requirement, budget constraint, and team-skill constraint. Use it to introduce QA-tension thinking just before Chapter 2.

**Cross-references to other chapters:** Ch 2 develops "quality attributes" into the full ASR / scenario / 25010 framework. Ch 3-12 each instantiate this Foundations vocabulary for one QA. Ch 9 returns to layering at scale (Kubernetes); Ch 15 (Linux network stack case) is "layering in textbook form, with everything labelled".

**Exam-relevance note:** Verbatim-definition questions ("define software architecture", "list the ten vocabulary terms"), substitution-rule diagram judgement questions, "is this cohesive/segregated/SRP-respecting?" diagram critiques, and the 4+1 viewpoint identification question are all extremely likely. The architect-soft-skills bullet point (page 2) is *explicitly flagged* by the lecturer as exam-counted — students must be able to articulate why architects' top qualities are communication-related.

**Special instructions for the writer:**
- Tone: friendly + precise. This is the chapter that sets the bar for the whole book.
- Each concept must carry the source analyses' definition / why-it-matters / explanation / analogy / example / pitfall sextet. Do not lose any.
- Treat the flight-and-hotel reservation system as the *running example* for definitions; subsequent chapters will reuse it (especially Ch 7 saga).
- When introducing the SOLID-at-component-scope set, note explicitly that these are Lano & Tehrani's lift of the OO principles to the component level — students sometimes recognise the OO version only.
- Emphasise the architect-role section more than the slide count would suggest — the lecturer flagged it as exam-counted.

---

### Chapter 2: The Quality-Attribute Framework — ASRs, Scenarios, ISO/IEC 25010, Risk, SBOM, Domain Modeling

**Target pages:** ~12
**Sources to draw from:** lecture_2_analysis.md (primary); secondary L1 for the QA-tension setup.
**Goal:** After reading, the student can (a) define a quality attribute in Bass et al.'s words, (b) fill all six slots of a QA scenario template, (c) reproduce the ISO/IEC 25010 eight top-level categories with at least one sub-attribute each, (d) explain risk = probability × impact and what cascading risks / defense in depth mean, (e) "sniff" ASRs out of a requirements document, (f) describe Iteration 0 vs BDUF vs Emergent and why Yang et al. (2016) endorse the middle path, (g) explain reference architectures and the over-conformance risk, (h) name the deployment-modelling primitives (machine, environment, internal vs external), and (i) describe what an SBOM is, why CycloneDX is the reference schema, and why the EU CRA makes SBOMs legally mandatory by 2027.

**Concepts to cover:**
- Quality Attribute (Bass et al. definition, measurability/testability) — `lecture_2_analysis.md` §Quality Attribute (QA)
- Functional vs Non-functional requirements (and why the boundary is fuzzy) — `lecture_2_analysis.md` §Functional vs. Non-Functional Requirements
- ASRs — Architecturally Significant Requirements, and how to sniff them — `lecture_2_analysis.md` §Architecturally Significant Requirements
- The 6-slot QA scenario template (Source / Stimulus / Environment / Artifact / Response / Response Measure) — `lecture_2_analysis.md` §QA Scenario
- ISO/IEC 25010 taxonomy (functional suitability, performance, compatibility, usability, reliability, security, maintainability, portability) — `lecture_2_analysis.md` §ISO/IEC 25010 QA Taxonomy
- Big Ball of Mud as the anti-QA — `lecture_2_analysis.md` §Big Ball of Mud
- BDUF vs Iteration 0 vs Emergent — `lecture_2_analysis.md` §BDUF vs. Iteration 0 vs. Emergent
- Risk = Probability × Impact, including positive risks — `lecture_2_analysis.md` §Risk = Probability x Impact
- Cascading risks + defense in depth (independent layered reducers) — `lecture_2_analysis.md` §Cascading Risks and Defense in Depth
- Quality gates as signals (not stop-the-line) — `lecture_2_analysis.md` §Quality Gates
- Reference architectures (definition, bidirectional derivation, over-conformance risk; CPython example) — `lecture_2_analysis.md` §Reference Architecture
- Standards as ASR carriers (RFC 1958 principles incl. Postel's robustness principle) — `lecture_2_analysis.md` §Standards as ASR Carriers
- Domain modeling (Fairbanks's Domain → Boundary → Architecture → Design → Code chain) — `lecture_2_analysis.md` §Domain Modeling
- Designation vs Refinement — `lecture_2_analysis.md` §Designation vs. Refinement
- Business / non-technical QAs (time-to-market, TCO) — `lecture_2_analysis.md` §Non-Technical (Business) QAs
- Deployment modeling (machine, internal vs external environment) — `lecture_2_analysis.md` §Deployment Modeling
- SBOM (CycloneDX schema; EU CRA mandate by 2027; transitive deps) — `lecture_2_analysis.md` §Software Bill of Materials
- Falsifiable QA (strongest form of measurability) — `lecture_2_analysis.md` §Falsifiable QA

**Diagrams to embed (path + caption):**
- `../images/lecture_2/lecture_2_p72_img1_xkcd_dependency.png` — XKCD 2347 ("Dependency"). The motivation slide for SBOMs; one paragraph caption explaining the joke and its supply-chain implication.

(Note: the analyses note L2 contains many figures rendered as vector primitives — QA scenario template, ISO/IEC 25010 tree, risk cascades, defense-in-depth picture, domain-modeling chain, deployment metamodel, CycloneDX schema. Where the writer needs a diagram for those, they should render the conceptual content prose-side or commission a clean redraw. The XKCD 2347 raster is the only L2 raster.)

**Cross-references to other chapters:** The QA scenario template is the *single most reused artifact in the book* — every QA chapter (3-12) opens by populating its slots with QA-specific value menus. Ch 11 and Ch 12 return to defense in depth (security) and to reference architectures (Case 3 in particular). Ch 14 develops Bass's evaluation procedure further.

**Exam-relevance note:** Filling the six scenario slots for a given QA is a near-guaranteed question type. "Define ASR" and "name the ISO/IEC 25010 categories" are recall layups. The risk formula and the SBOM/CycloneDX answer are both fair game. Ruohonen 2025 cited.

**Special instructions for the writer:**
- This chapter is the *machinery* the rest of the book uses. Spend disproportionate effort on making the scenario template render beautifully (ideally as a clean redrawn diagram with all six slots labelled).
- When teaching ISO/IEC 25010, give one concrete sub-attribute example per top-level category — students must memorise at least one each.
- Defense in depth: write the example as a stack (WAF → rate limit → input validation → parameterized SQL → least-priv DB user → encryption at rest). It will be referenced again in Ch 10–11.
- Postel's Robustness Principle is *also* a recurring touchstone — quote it verbatim ("be conservative in what you send, liberal in what you accept").

---

### Chapter 3: Integrability — Dependencies, Size × Distance, Tactics Tree, Observer vs Pub-Sub, Wrapper/Bridge/Mediator

**Target pages:** ~12
**Sources to draw from:** lecture_3_analysis.md (integrability half — concepts 1 through ~10).
**Goal:** After reading, the student can (a) distinguish tactics from patterns in Bass's vocabulary, (b) classify a dependency along the run-time / dev / install + depth + syntactic/semantic axes, (c) compute the σ = Σ size and reason about *distance* along five sub-axes, (d) fill the 6-slot integrability scenario, (e) draw Bass's Limit / Adapt / Coordinate tactics tree from memory with at least 2 sub-tactics per branch, (f) compare Observer to Publish-Subscribe across six rows (latency, logging, coupling, communication, fault tolerance, domain), (g) distinguish Wrapper from Bridge from Mediator, (h) explain service discovery (DHCP / DNS / Consul) as the canonical Adapt-Discover tactic, and (i) recognise orchestration's "god-class" risk.

**Concepts to cover:**
- Tactics vs Patterns (Bass terminology vs Fairbanks "styles") — `lecture_3_analysis.md` §Architectural tactics vs architectural patterns
- Dependency taxonomy (when × depth × syntactic/semantic + temporal + shared-resource) — `lecture_3_analysis.md` §Dependency (general)
- Size × Distance (the σ metric); the five distance sub-axes — `lecture_3_analysis.md` §Size and distance (the σ metric)
- Integrability scenario template — `lecture_3_analysis.md` §Integrability scenario template
- Limit / Adapt / Coordinate tactics tree (with avoid/bundle/encapsulate/discover/tailor/configure/orchestrate/manage-resources) — `lecture_3_analysis.md` §Integrability tactics taxonomy
- Bundling vs package-management, pinned dependencies, OpenSSF Scorecard, fake stars — `lecture_3_analysis.md` §Bundling vs package-management
- Observer vs Publish-Subscribe (the canonical compare table) — `lecture_3_analysis.md` §Observer pattern vs Publish-Subscribe pattern
- OWASP logging architecture as encapsulation in practice — `lecture_3_analysis.md` §Logging design for microservices
- Wrapper vs Bridge vs Mediator — `lecture_3_analysis.md` §Wrapper vs Bridge vs Mediator
- Service discovery (DHCP / DNS / Consul / Kubernetes Services) — `lecture_3_analysis.md` §Service discovery
- Orchestration and its god-class danger — `lecture_3_analysis.md` §Orchestration (and its god-class danger)

**Diagrams to embed (path + caption):**
- `../images/lecture_3/lecture_3_p08_img1_refining_basic_concepts.png` — In-house vs external components on the control / knowledge axis. Motivates why integrability matters.
- `../images/lecture_3/lecture_3_p16_img1_integrability_scenario_template.png` — The 6-slot integrability scenario template populated.
- `../images/lecture_3/lecture_3_p18_img1_integrability_tactics_tree.png` — The full Limit / Adapt / Coordinate tactics tree. Anchor figure of the chapter.
- `../images/lecture_3/lecture_3_p26_img1_publish_subscribe_pattern.png` — Pub-sub broker pattern with decoupled publishers/subscribers.
- `../images/lecture_3/lecture_3_p29_img1_observer_vs_pubsub_table.png` — The six-row comparison table (latency / logging / coupling / communication / fault-tolerance / domain). High-yield exam fodder.
- `../images/lecture_3/lecture_3_p31_img1_logging_microservices_design.png` — OWASP logging stack as encapsulation + broker + isolated storage; ask students to identify the inconsistency in the figure as the lecturer did.

**Cross-references to other chapters:** Ch 4 (Modifiability) and Ch 5 (Testability) reuse encapsulation and dependency-reduction tactics. Ch 10 (Security) reuses the broker pattern for SIEM and the encapsulation tactic for input validation. Ch 13 (catalog) lists Observer, Pub-Sub, Wrapper, Bridge, Mediator. The orchestration discussion bridges to Ch 9 (Kubernetes is orchestration at scale).

**Exam-relevance note:** Observer-vs-Pub-Sub is high-yield (the lecturer drew a six-row table specifically for it). The σ = size × distance question — "list the five distance sub-axes and give an example of each" — is a near-guaranteed recall question. The Mars Climate Orbiter example (data-semantic distance) is quote-worthy. Identifying Wrapper vs Bridge vs Mediator from a diagram is also likely.

**Special instructions for the writer:**
- Draw the tactics tree as a clean visual hierarchy; this is the first of *many* tactics trees in the book and the layout convention you choose here is the convention for the whole book.
- The Observer-vs-Pub-Sub table must be reproduced exactly (six rows). Do not paraphrase.
- The "noisy publisher" gotcha (one publisher starving the broker, no global scheduler) is exam-relevant.

---

### Chapter 4: Modifiability — Maintenance Economics, Six Planning Questions, Five Moves, Defer Binding, Semantic Versioning, Patterns

**Target pages:** ~12
**Sources to draw from:** lecture_3_analysis.md (modifiability half — concepts 11 onward); lecture_4_analysis.md §Release Engineering and Semantic Versioning for the semver companion treatment.
**Goal:** After reading, the student can (a) explain the maintenance phase + 80% rule, (b) recall the six modifiability planning questions, (c) describe ripple effects across artifact and component boundaries, (d) draw the reduce-coupling / increase-cohesion / defer-binding tactics tree, (e) apply the five canonical modifiability moves (split / combine / encapsulate / intermediary / restrict), (f) describe the three binding timings (compile / startup / runtime) and pick the appropriate one for a given change, (g) recite the four modifiability principles (least surprise, small interface, DRY, uniform access) with one example each, (h) explain semantic versioning MAJOR.MINOR.PATCH and the five Lübke alternatives for incompatible changes, and (i) compare the modifiability-promoting patterns (publish-subscribe / layering / client-server / MVC / plugin (micro-kernel) / pipe-and-filter / batch-sequential).

**Concepts to cover:**
- Maintenance phase, staging trees, 80% rule — `lecture_3_analysis.md` §Maintenance phase and the 80% rule
- Six modifiability planning questions — `lecture_3_analysis.md` §Six modifiability planning questions
- Ripple effects across artifact + component boundaries — `lecture_3_analysis.md` §Ripple effects
- Backwards compatibility, semantic versioning, Lübke's five alternatives (experimental / aggressive obsolescence / two-in-production / limited lifetime / lifetime) — `lecture_3_analysis.md` §Backwards compatibility and semantic versioning + cross-check with `lecture_4_analysis.md` §Release Engineering and Semantic Versioning
- Five canonical modifiability moves (split, combine, encapsulate, intermediary, restrict) — `lecture_3_analysis.md` §Five core modifiability moves
- Defer-binding tactic (compile-time #ifdef / startup config / runtime parameter & polymorphism) — `lecture_3_analysis.md` §Defer-binding tactic
- Four modifiability principles: least surprise, small interface, DRY, uniform access (Eiffel) — `lecture_3_analysis.md` §Modifiability principles
- Plugin / micro-kernel pattern with its security caveat — `lecture_3_analysis.md` §Plugin / micro-kernel pattern
- Pipe-and-filter vs batch-sequential — `lecture_3_analysis.md` §Pipe-and-filter vs batch-sequential
- Modifiability via layering, client-server, MVC — `lecture_3_analysis.md` §Modifiability via other patterns

**Diagrams to embed (path + caption):**
- `../images/lecture_3/lecture_3_p53_img1_incompatible_change_alternatives.png` — Lübke et al.'s five alternatives for incompatible changes. Reference for "how do you ship breaking changes?"
- `../images/lecture_3/lecture_3_p58_img1_modifiability_tactics_tree.png` — Reduce-coupling / increase-cohesion / defer-binding taxonomy. Anchor figure of the chapter.
- `../images/lecture_3/lecture_3_p61_img1_five_modifiability_tactics.png` — The five-move cohesion/coupling palette (split / combine / encapsulate / intermediary / restrict).
- `../images/lecture_3/lecture_3_p75_img1_plugin_micro_kernel_pattern.png` — Core + plugins + registry diagram; flag the privilege/security caveat.
- `../images/lecture_3/lecture_3_p77_img1_pipe_and_filter_pattern.png` — Five-filter pipeline; the canonical pipe-and-filter visual the book reuses in Ch 10 for SIEM.
- `../images/lecture_4/lecture_4_p77_semantic_versioning.png` — Semver / release engineering timeline with major / minor / patch cadences. Embedded here (the canonical home for semver), with cross-ref from Ch 6.

**Cross-references to other chapters:** Ch 6 (Deployability) discusses release engineering and CD; that chapter cross-refs this one for semver. Ch 7 references the batch-sequential vs saga comparison. Ch 13 (catalog) makes plugin + pipe-and-filter + MVC pattern entries pointing back here. Ch 15 (Linux network stack) is a *pipe-and-filter* example at scale (Netfilter).

**Exam-relevance note:** "Maintenance is 60-80% of total lifetime cost" — quotable. The five modifiability moves are exam-friendly recall items. Semver MAJOR.MINOR.PATCH and the Lübke five-alternative list are both fair game. Identifying a defer-binding stage in a diagram is also likely.

**Special instructions for the writer:**
- Pair every modifiability move with a concrete refactoring example (e.g., "Extract UserAuthService from UserService" = split).
- The defer-binding three-bucket model is best taught via three side-by-side code snippets (`#ifdef`, config.xml, runtime parameter).
- The "Don't go overboard" Spring-XML caveat is *itself* a memorable exam quote — keep it in.

---

### Chapter 5: Testability — Oracle Problem, Fuzzing, Control/Observe, Limit Complexity, Patterns, LLM Verification Debt

**Target pages:** ~10
**Sources to draw from:** lecture_4_analysis.md (testability half — concepts 1 through ~11).
**Goal:** After reading, the student can (a) define testability as a property of the system (not "we have tests"), (b) explain Boehm's verification vs validation distinction, (c) fill a testability scenario, (d) name and example the four oracle types (specified / pseudo / implicit / derived), (e) describe fuzzing's skeleton loop, (f) recite the two branches of the testability tactics tree and the six control/observe sub-tactics, (g) explain dependency injection / strategy / intercepting filter / type safety / LLM independence as testability patterns, and (h) describe Bouzoukas's "verification debt" and Chou et al.'s vibe-coder vignette.

**Concepts to cover:**
- Testability (Bass et al. definition: "ease with which software can be made to demonstrate its faults") — `lecture_4_analysis.md` §Testability (as a quality attribute)
- Verification vs Validation (Boehm 1984) — `lecture_4_analysis.md` §Verification vs. Validation
- Testability scenario (6-slot) — `lecture_4_analysis.md` §Testability Scenarios
- The Oracle Problem with the four oracle types (specified / pseudo / implicit / derived) — `lecture_4_analysis.md` §The Oracle Problem
- Stop criterion (coverage, time, statistical reliability models, NHPP for bug arrival) — `lecture_4_analysis.md` §Stop Criterion
- Fuzzing skeleton loop (seed → generate → run → detect implicit-oracle violation) — `lecture_4_analysis.md` §Fuzzing
- Testability tactics — Control & Observe Input/State: input generation, record & play, special interfaces, localised storage, assertions, sandboxes — `lecture_4_analysis.md` §Testability Tactics: Control and Observe Input & State
- Testability tactics — Limit Complexity (encapsulation, dependency reduction, NetBSD's flagged oracles) — `lecture_4_analysis.md` §Testability Tactics: Limit Complexity
- Regression testing (Ruohonen & Alami 2024: Linux drivers/fs subsystems dominate regression bugs) — `lecture_4_analysis.md` §Regression Testing
- Dependency Injection pattern — `lecture_4_analysis.md` §Testability Pattern: Dependency Injection
- Strategy pattern — `lecture_4_analysis.md` §Testability Pattern: Strategy Pattern
- Intercepting Filter pattern — `lecture_4_analysis.md` §Testability Pattern: Intercepting Filter
- Type Safety pattern (and taint analysis) — `lecture_4_analysis.md` §Testability Pattern: Type Safety
- LLMs and Verification Debt (Bouzoukas 2026; Chou et al. 2025 vibe coder) — `lecture_4_analysis.md` §Testability Pattern: LLMs and Verification Debt

**Diagrams to embed (path + caption):**
- `../images/lecture_4/lecture_4_p08_testability_scenarios.png` — 6-slot testability scenario template with example values.
- `../images/lecture_4/lecture_4_p15_fuzzing_skeleton.png` — The canonical fuzzing loop including the deadlock-detection-by-timeout arm.
- `../images/lecture_4/lecture_4_p19_testability_tactics_tree.png` — Two-branch testability tactics tree.
- `../images/lecture_4/lecture_4_p41_llm_with_independent_validation.png` — The "safe" LLM coding pipeline (LLM generates → independent static + unit + integration tests verify → re-generate on failure). Anchor for the LLM/verification-debt discussion.

**Cross-references to other chapters:** Ch 4 (Modifiability) shares the encapsulation / dependency-reduction tactics. Ch 6 (Deployability) reuses fuzzing in the context of chaos engineering. Ch 10 (Safety) reuses assertions for safety-tactic detection.

**Exam-relevance note:** "Testability ≠ tests" is one of the lecturer's quotable distinctions. The four-oracle taxonomy is a recall item. The six control/observe sub-tactics list is likely to appear as a "name three" question. LLM verification debt is fresh material from Bouzoukas (2026) and likely a current topic.

**Special instructions for the writer:**
- Include the `#ifdef TESTING` snippet for special interfaces; the lecture used it explicitly.
- The "ASSERT_FUTURE_STATE(10s) == SHUTDOWN" speculative assertion is a memorable hook.
- Make the LLM pipeline diagram large and clean — it is *new* material and likely to be on the exam.

---

### Chapter 6: Deployability — CI/CD/DevOps/GitOps, Rolling Upgrades, A/B, Chaos, CRA Security Updates

**Target pages:** ~12
**Sources to draw from:** lecture_4_analysis.md (deployability half — concepts 12 onward).
**Goal:** After reading, the student can (a) define deployability with its three measurable sub-attributes (cycle time, traceability, repeatability), (b) describe CI / CD / DevOps / GitOps and the "X-as-code" family, (c) draw and populate a deployability tactics tree (manage pipeline / manage deployment), (d) compare rolling upgrades in two flavours (instance-replacement vs traffic-split), (e) describe A/B testing as the same machinery with measurement intent, (f) characterise microservices *as a deployment pattern*, (g) explain the CRA's automatic-separated-security-update mandate (mandatory by 2027), (h) describe chaos engineering's design loop (steady state / hypothesis / blast radius / fault / observe), (i) explain safe-and-secure defaults (Ruohonen 2025: functional off / security on).

**Concepts to cover:**
- Deployability (Bass et al. definition; cycle time, traceability, repeatability) — `lecture_4_analysis.md` §Deployability
- CI, CD, DevOps, GitOps, X-as-code — `lecture_4_analysis.md` §Continuous Integration, Continuous Deployment, DevOps, GitOps
- Deployability tactics — Manage Pipeline (separate builds, scale roll-outs / canary, scripted deployment, rollback) — `lecture_4_analysis.md` §Deployability Tactics: Manage Pipeline
- Deployability tactics — Manage Deployment (multi-version interaction, feature toggle, secure defaults) — `lecture_4_analysis.md` §Deployability Tactics: Manage Deployment
- Microservices as a deployment pattern (benefits + 5 drawbacks: connector overhead, transactions, heterogeneity, granularity, SBOM/catalog overhead) — `lecture_4_analysis.md` §Deployability Pattern: Microservices
- Rolling upgrades (in-place instance replacement vs traffic split) — `lecture_4_analysis.md` §Deployability Pattern: Rolling Upgrades
- A/B testing as measurement-flavoured rolling upgrade — `lecture_4_analysis.md` §Deployability Pattern: A/B Testing
- EU Cyber Resilience Act (CRA) — automatic + separated security updates by 2027 (Ruohonen et al. 2025) — `lecture_4_analysis.md` §Cyber Resilience Act
- Chaos engineering + tabletop exercises (steady state, hypothesis, blast radius) — `lecture_4_analysis.md` §Chaos Engineering and Tabletop Exercises
- Safe and secure defaults (Ruohonen 2025) — `lecture_4_analysis.md` §Safe and Secure Defaults

**Diagrams to embed (path + caption):**
- `../images/lecture_4/lecture_4_p48_ci_cd_pipeline.png` — CI/CD pipeline: commit → merge → integrate/build → tests → deploy → feedback.
- `../images/lecture_4/lecture_4_p53_deployability_tactics_tree.png` — Manage Pipeline / Manage Deployment tactics tree.
- `../images/lecture_4/lecture_4_p54_separate_builds.png` — Refactoring a big-ball-of-mud component into independently-built modules.
- `../images/lecture_4/lecture_4_p58_multi_server_versions.png` — Multiple server versions behind a bridge/proxy. The substrate for rolling upgrade and A/B testing.
- `../images/lecture_4/lecture_4_p64_rolling_upgrade_start.png` — Starting state of a rolling upgrade.
- `../images/lecture_4/lecture_4_p72_ab_testing_split.png` — A/B split: 50/50 traffic for time *t* before statistical decision.
- `../images/lecture_4/lecture_4_p75_cra_security_updates.png` — CRA decision flow: security vs functional updates, automatic vs manual delivery, integrity gate.
- `../images/lecture_4/lecture_4_p80_chaos_engineering_setup.png` — Chaos engineering loop (steady state / hypothesis / blast radius / fault / observe).

**Cross-references to other chapters:** Ch 4 already homes semver (semver figure embedded there; this chapter cross-refs). Ch 7 (Availability) reuses the multi-version / rolling-upgrade substrate for shadow deployments and the canary→shadow morph. Ch 11 (Security part 2) re-examines CI/CD as a security target (OWASP CI/CD Top-10, SDL Gate 2). Ch 16 (MLOps case) is the *full deployability story* for ML systems.

**Exam-relevance note:** The three deployability sub-attributes (cycle time / traceability / repeatability) is a recall question. Drawing or explaining a canary deployment with health metrics + abort criterion is likely. The CRA "automatic + separated security updates" is timely and quotable. Chaos engineering's three "experiment design" inputs (steady state / hypothesis / blast radius) is a recall trio.

**Special instructions for the writer:**
- Make sure students walk away knowing that "deploy frequently" ≠ deployability — predictability and effort are the QA.
- Highlight Ruohonen's secure-defaults paper (Ruohonen 2025) — likely material from the lecturer.
- Embed the CRA flow figure prominently — this is one of the few raster diagrams of L4 and likely an exam image.

---

### Chapter 7: Availability — Fault/Failure/Trigger, the Nines, Detect/Repair/Reintroduce/Prevent, Saga, Bulkhead, Spares

**Target pages:** ~14
**Sources to draw from:** lecture_5_analysis.md (primary).
**Goal:** After reading, the student can (a) define availability and contrast it with security and reliability, (b) precisely distinguish fault / failure / trigger, (c) reproduce the "nines" downtime budgets table (90 → 99.9999), (d) fill the 6-slot availability scenario, (e) draw the *four*-branch availability tactics tree (Detect / Repair / Reintroduce / Prevent) with at least 2 sub-tactics per branch, (f) explain watchdog vs heartbeat and why threshold tuning matters, (g) distinguish replication / functional / analytical redundancy, (h) explain the consistency-vs-availability trade-off (eventual / quorum / synchronized / read-after-write), (i) draw the circuit breaker state machine and pair it with exponential backoff + jitter, (j) describe shadow / state re-sync / escalating restart, (k) explain isolation, blast radius, bulkheads, hot/warm/cold spare, (l) walk through the saga pattern using the flight + hotel booking example (compensating transactions), and (m) state Williams 2026's over-engineering / "resilience as debt" critique.

**Concepts to cover:**
- Availability (Bass et al. definition; CIA-A; reliability; maintainability intersection) — `lecture_5_analysis.md` §Availability
- Fault / Failure / Trigger — `lecture_5_analysis.md` §Fault vs Failure vs Trigger
- The Nines table (with downtime budgets) — `lecture_5_analysis.md` §The "Nines" of Availability
- Availability scenario (6-slot, availability-flavoured values) — `lecture_5_analysis.md` §Availability QA Scenario
- Availability tactics tree (Detect / Repair / Reintroduce / Prevent) — `lecture_5_analysis.md` §Availability Tactics Tree
- Watchdog & heartbeat (timer tuning, GC-pause false positives) — `lecture_5_analysis.md` §Watchdog and Heartbeat
- Timestamps vs sequence numbers (monotonicity, clock drift) — `lecture_5_analysis.md` §Timestamps vs Sequence Numbers
- Sanity checking & CRC (integrity, not security — caveat!) — `lecture_5_analysis.md` §Sanity Checking and CRC
- Voting: replication / functional / analytical redundancy; majority gate; Boeing 737 MAX MCAS anti-pattern — `lecture_5_analysis.md` §Voting and §Majority Gate
- Active-active vs Active-passive load balancing — `lecture_5_analysis.md` §Active vs Active-Passive Load Balancing
- Consistency vs availability axis (eventual / quorum / synchronized / read-after-write) — `lecture_5_analysis.md` §Consistency vs Availability Trade-Off
- Retry with exponential back-off + jitter — `lecture_5_analysis.md` §Retry with Exponential Back-Off
- Circuit breaker state machine (Closed / Open / Half-open; Hystrix; Montesi & Weber 2016) — `lecture_5_analysis.md` §Circuit Breaker
- Graceful degradation — `lecture_5_analysis.md` §Graceful Degradation
- Shadow / state re-sync / escalating restart (Reintroduce branch) — `lecture_5_analysis.md` §Shadow / State Re-synchronization / Escalating Restart
- Isolation, blast radius, cascading failure, sharding (Adkins et al. 2020) — `lecture_5_analysis.md` §Isolation and Blast Radius
- Hot / warm / cold spare — `lecture_5_analysis.md` §Hot / Warm / Cold Spare
- Bulkheads / equitable resource allocation — `lecture_5_analysis.md` §Bulkheads
- Saga pattern (local transactions + compensating transactions; flight+hotel) — `lecture_5_analysis.md` §Saga Pattern
- Taint and quarantine — `lecture_5_analysis.md` §Taint and Quarantine
- Over-engineering as new technical debt (Williams 2026) — `lecture_5_analysis.md` §Over-engineering as the New Technical Debt

**Diagrams to embed (path + caption):**
- `../images/lecture_5/lecture_5_p11_page_fault_to_failure_flow.png` — Fault → Trigger → (Repair | Failure) flowchart. Anchor for the QA's central distinction.
- `../images/lecture_5/lecture_5_p13_page_availability_scenario_template.png` — Populated 6-slot availability scenario.
- `../images/lecture_5/lecture_5_p16_page_availability_tactics_tree.png` — Master Detect / Repair / Reintroduce / Prevent tactics tree (~26 named tactics).
- `../images/lecture_5/lecture_5_p18_page_watchdog_heartbeat.png` — Watchdog timer mechanics.
- `../images/lecture_5/lecture_5_p28_page_load_balancing_active_active_vs_passive.png` — Active-active 50/50 vs active-passive 100/0.
- `../images/lecture_5/lecture_5_p38_page_consistency_vs_availability_tradeoff.png` — Eventual / quorum / synchronized / read-after-write axis chart.
- `../images/lecture_5/lecture_5_p44_page_circuit_breaker_state_diagram.png` — Closed / Open / Half-open state machine. Canonical figure; cross-ref from Ch 8 (Performance) for throttling.
- `../images/lecture_5/lecture_5_p50_page_escalating_restart.png` — 5% → 25% → 60% → 100% restart staircase.
- `../images/lecture_5/lecture_5_p55_page_blast_radius_failure_domains.png` — Failure domain 15% vs 85% partitioning.
- `../images/lecture_5/lecture_5_p67_page_spare_redundancy_cold_spare.png` — Cold-spare lifecycle.
- `../images/lecture_5/lecture_5_p69_page_bulkheads_equitable_allocation.png` — Separate request pools (small vs large requests).
- `../images/lecture_5/lecture_5_p73_page_saga_pattern.png` — Saga: local transactions + notify-on-success + compensate-on-failure. Use the flight + hotel example.
- `../images/lecture_5/lecture_5_p75_page_patterns_summary_table.png` — Closing 2-column table mapping scenarios to recommended patterns. Place at the end of the chapter as a cheat-sheet.

**Cross-references to other chapters:** Ch 8 (Performance) reuses the circuit breaker for throttling and the consistency-vs-availability axis for CAP/PACELC. Ch 10 (Security) reuses isolation and blast radius. Ch 11 (Security part 2) reuses fail-safe vs fail-secure (a security-flavoured availability trade-off). Ch 15 (Linux network stack) demonstrates bonding/LACP as concrete redundancy. Ch 16 (MLOps) reuses circuit-breaker thinking for model-quality drift detection.

**Exam-relevance note:** Drawing the 4-branch tactics tree is a likely high-points question — *Reintroduce* is the branch students forget. The fault/failure/trigger trichotomy is a precision-vocabulary question. Saga with compensating transactions on the flight+hotel example is the lecturer's running illustration. The Boeing MCAS anti-pattern (no analytical redundancy) is quotable.

**Special instructions for the writer:**
- Pair the "nines" table with one concrete domain example per row (telecoms = 5 nines, banking = 4 nines, hobby blog = 99%, etc.).
- The saga walkthrough must use the flight+hotel example — it is the *running example* of the course.
- Highlight that Reintroduce is its own branch — students drop it consistently.
- Williams 2026 over-engineering critique is the closing slide of L5 — give it pride of place at the end of the chapter (one short subsection).

---

### Chapter 8: Performance — Latency vs Throughput, CAP/PACELC, Caching Topologies, Throttling, Scheduling, MapReduce, Claim-Check

**Target pages:** ~14
**Sources to draw from:** lecture_6_analysis.md (primary); cross-refs to Ch 7 for the circuit breaker reused as throttling.
**Goal:** After reading, the student can (a) define performance and *contrast it precisely with scalability*, (b) distinguish latency from throughput, (c) recite the eight fallacies of distributed computing, (d) fill the 6-slot performance scenario with Bass's value menus, (e) draw the two-branch tactics tree (Control demand / Manage resources) with all twelve tactics, (f) compare drop vs queue limit-response, (g) distinguish priority from stochastic-fairness queueing, (h) reason about concurrency vs parallelism, thread-pool vs spawn-per-request, (i) state the CAP theorem and the PACELC extension (e.g., classify a system as PA/EL or PC/EC), (j) compare the five named cache patterns (local/distributed × cache-aside / refresh-ahead / write-through / write-back / write-around), (k) reason about scheduler choice (FIFO / SJF / EDF / rate-monotonic / round-robin / idle / batch / semantic-importance), (l) describe throttling implemented via circuit breaker + back-off + jitter, (m) describe MapReduce and Claim-Check as named patterns.

**Concepts to cover:**
- Performance vs Scalability ("do more with what you have" vs "add resources") — `lecture_6_analysis.md` §Performance
- Latency vs Throughput (units, tail latency, P99) — `lecture_6_analysis.md` §Latency vs. Throughput
- Units-of-time intuition (L1 cache to satellite networks) — `lecture_6_analysis.md` §Units-of-Time Intuition
- Eight Fallacies of Distributed Computing (Deutsch/Wilson) — `lecture_6_analysis.md` §Eight Fallacies of Distributed Computing
- Performance scenario (6-slot template, performance-specific values) — `lecture_6_analysis.md` §Performance Scenario
- Performance Tactics Tree (Control demand × 6 + Manage resources × 6) — `lecture_6_analysis.md` §Performance Tactics Tree
- Demand-side: manage requests, limit responses (drop vs queue), prioritize events (priority/stochastic-fairness), reduce overhead, bound execution, increase efficiency — `lecture_6_analysis.md` §Tactic — Manage requests through §Tactic — Increase efficiency
- Resource-side: increase concurrency (vs parallelism; thread pool vs spawn-per-request), multiple copies of computations, multiple copies of data, bound queues, schedule resources — `lecture_6_analysis.md` §Tactic — Increase concurrency through §Tactic — Schedule resources
- CAP Theorem (Brewer 2000); CP vs AP — `lecture_6_analysis.md` §CAP Theorem
- PACELC Theorem (Abadi 2010); classify systems as PA/EL or PC/EC — `lecture_6_analysis.md` §PACELC Theorem
- Caching topologies: local vs distributed; cache-aside / refresh-ahead / write-through / write-back / write-around — `lecture_6_analysis.md` §Caching topologies
- Scheduling family: FIFO / SJF / EDF / rate-monotonic / idle / batch / round-robin / semantic-importance; `irqbalance` — `lecture_6_analysis.md` §Tactic — Schedule resources
- Throttling pattern via circuit breaker + back-off + jitter; Brooker 2019 — `lecture_6_analysis.md` §Throttling Pattern
- MapReduce (Dean & Ghemawat 2008) — `lecture_6_analysis.md` §MapReduce
- Claim-check pattern (token + shared store) — `lecture_6_analysis.md` §Claim-Check Pattern
- Static/Dynamic content separation + materialized views — `lecture_6_analysis.md` §Static/Dynamic Content Separation
- Database performance patterns: caching, read replicas, sharding, indexing, locking debug, batched writes, connection pools — `lecture_6_analysis.md` §Database Performance Patterns

**Diagrams to embed (path + caption):**
- `../images/lecture_6/lecture_6_p06_page_performance_scenario_template.png` — 6-slot scenario template with performance value lists.
- `../images/lecture_6/lecture_6_p11_page_performance_tactics_tree.png` — Two-branch × six-tactic taxonomy.
- `../images/lecture_6/lecture_6_p15_page_limit_responses_drop_vs_queue.png` — Drop vs queue side-by-side.
- `../images/lecture_6/lecture_6_p18_page_priority_vs_stochastic_fairness_queueing.png` — Priority vs stochastic fairness.
- `../images/lecture_6/lecture_6_p27_page_concurrency_vs_parallelism_reality.png` — Multi-core CPUs running threads both concurrently and in parallel.
- `../images/lecture_6/lecture_6_p28_page_spawn_thread_vs_thread_pool.png` — Spawn-per-request vs fixed-size pool.
- `../images/lecture_6/lecture_6_p35_page_cap_theorem.png` — CAP trade-off (CP vs AP under partition).
- `../images/lecture_6/lecture_6_p38_page_pacelc_theorem.png` — PACELC decision tree.
- `../images/lecture_6/lecture_6_p40_page_cache_aside_vs_refresh_ahead.png` — Cache-aside vs refresh-ahead.
- `../images/lecture_6/lecture_6_p41_page_write_back_through_around.png` — Write-back / write-through / write-around.
- `../images/lecture_6/lecture_6_p47_page_better_cpu_scheduler.png` — A better CPU scheduler (longer slices, fewer context switches).
- `../images/lecture_6/lecture_6_p53_page_earliest_deadline_first.png` — EDF scheduling.
- `../images/lecture_6/lecture_6_p61_page_throttling_with_circuit_breaker.png` — Resource utilisation curve crossing threshold into half-open throttling. (NOTE: the circuit breaker state diagram itself lives in Ch 7; this chapter shows the *application* curve.)
- `../images/lecture_6/lecture_6_p63_page_throttling_plus_dynamic_scaling.png` — Throttling combined with dynamic scaling (the cloud alternative).
- `../images/lecture_6/lecture_6_p71_page_mapreduce.png` — MapReduce reference: main process, mappers, remote writes, output file.
- `../images/lecture_6/lecture_6_p72_page_claim_check_pattern.png` — Claim-check: send token, not payload.

**Cross-references to other chapters:** Ch 7 (Availability) houses the *circuit breaker state diagram itself*; this chapter cross-refs. Ch 9 (Scalability) extends throttling with dynamic scaling, latency decomposition, and CDNs. Ch 10 (Safety+Security pt 1) reuses the pipe-and-filter pattern for SIEM. Ch 15 (Linux network stack) is an *enormous* showcase of performance tactics (NAPI, RSS, RPS, RFS, GRO/GSO, XDP, qdisc scheduling).

**Exam-relevance note:** "Performance ≠ Scalability" is exam material (lecturer flagged in mock Q8). PACELC classification (PA/EL, PC/EC) is the kind of crisp question the lecturer favours. The five cache patterns table is a high-yield recall question. Drawing the throttling + circuit breaker + jitter combination is realistic. The eight fallacies of distributed computing is a list-recall fair game.

**Special instructions for the writer:**
- Resolve duplications carefully: *Throttling* appears in both L5 and L6 — make this chapter the canonical home; cross-ref from Ch 7. The *circuit breaker state diagram* lives in Ch 7; this chapter shows its *application* to throttling.
- The PACELC classification table should be redrawn with at least 4 real systems (Cassandra = PA/EL, Spanner-like = PC/EC, DynamoDB = PA/EL, single-region SQL = PC/EC).
- Make the eight fallacies a one-page sidebar; students will memorise the list.
- Include the Python thread-pool snippet (Parent class with 500 daemon workers, `queue.Queue`, `threading.Lock`) from L6 — concrete code makes the abstraction stick.

---

### Chapter 9: Scalability — Amdahl, Kubernetes, Gateway/Sidecar, Horizontal vs Vertical, CDN/SDN, Latency Decomposition, Bondi

**Target pages:** ~13
**Sources to draw from:** lecture_7_analysis.md (primary); cross-refs to Ch 8 for performance-scalability boundary.
**Goal:** After reading, the student can (a) define scalability (proportional capacity gain from added resources), (b) apply Amdahl's law to compute the 1/a speedup ceiling, (c) walk fluently in Kubernetes vocabulary (cluster, node, pod, container, kubelet, kube-proxy, autoscaler, securityContext anticipation), (d) distinguish pod-to-pod TCP/IP from container-to-container IPC, (e) draw and explain the Gateway and Sidecar patterns and their trade-offs, (f) place an example in the 2×2 of horizontal/vertical × workload/infrastructure, (g) describe CDN multi-tier architecture and SDN/L7 routing in OpenStack, (h) decompose total latency into a + b + c (network + compute + I/O), (i) recite Bondi's six scalability dimensions and apply them (e.g., Bluetooth fails distance and speed/distance), (j) describe Bondi's 6-point diagnosis checklist plus the statistical-debugging approach for cluster performance.

**Concepts to cover:**
- Scalability (Ruohonen working definition; "proportionally" is the key word) — `lecture_7_analysis.md` §Scalability
- Amdahl's law (y = 1 / (a + (1-a)/p); maximum speedup = 1/a; Gustafson refinement) — `lecture_7_analysis.md` §Amdahl's law
- Service mesh ≈ cluster computing — `lecture_7_analysis.md` §Service mesh
- Kubernetes anatomy: cluster / node / pod / container — `lecture_7_analysis.md` §Kubernetes anatomy
- kubelet vs kube-proxy — `lecture_7_analysis.md` §kubelet vs kube-proxy
- Pod-to-pod TCP/IP vs container-to-container IPC — `lecture_7_analysis.md` §Pod-to-pod vs container-to-container communication
- Gateway pattern — `lecture_7_analysis.md` §Gateway pattern
- Sidecar pattern (with the Google 2024 image-size warning) — `lecture_7_analysis.md` §Sidecar pattern
- Horizontal vs Vertical scaling at workload vs infrastructure viewpoints (2×2) — `lecture_7_analysis.md` §Horizontal vs vertical scaling
- Autoscaler limits (110 pods/node, 5,000 nodes, 150,000 pods, 300,000 containers) — `lecture_7_analysis.md` §Autoscaler and the cluster size limits
- Geofencing + eventual consistency at hyperscale — `lecture_7_analysis.md` §Geofencing and eventual consistency
- Static vs dynamic load-balancing algorithms — `lecture_7_analysis.md` §Static vs dynamic load-balancing algorithms
- DNS-based load balancing (A/MX records) — `lecture_7_analysis.md` §DNS-based load balancing
- CDN (multi-tier; aliased DNS; bundled DDoS/WAF) — `lecture_7_analysis.md` §Content Delivery Network
- SDN (OpenStack example; network segmentation reuses L3 isolation) — `lecture_7_analysis.md` §Software-Defined Networking
- L7 load balancing (OpenStack REJECT / REDIRECT_TO_URL / REDIRECT_TO_POOL on HEADER/PATH/FILE_TYPE) — `lecture_7_analysis.md` §Layer-7 load balancing
- Latency decomposition y = a + b + c — `lecture_7_analysis.md` §Latency decomposition
- Bondi's six scalability dimensions — `lecture_7_analysis.md` §Bondi's scalability dimensions
- Bondi's 6-point performance/scalability diagnosis — `lecture_7_analysis.md` §Performance/scalability diagnosis
- Statistical debugging + retrospective triaging (Bansal et al. 2020) — `lecture_7_analysis.md` §Statistical debugging and log triaging

**Diagrams to embed (path + caption):**
- `../images/lecture_7/page018_amdahls_law_chart.png` — Speedup curves for serial fractions; visualises the 1/a ceiling.
- `../images/lecture_7/page021_kubernetes_core_parts.png` — Cluster / Node / Pod / Container hierarchy with kubelet + kube-proxy roles.
- `../images/lecture_7/page023_kubernetes_kubelet_kubeproxy.png` — User-to-pod path through master + kube-proxy.
- `../images/lecture_7/page024_kubernetes_pod_to_pod.png` — Two worker nodes, each with two pods, on node-level bridge subnets.
- `../images/lecture_7/page027_gateway_pattern.png` — Before/after gateway refactor (3 high-latency hops → 1 high-latency + N local).
- `../images/lecture_7/page029_sidecar_pattern.png` — Sidecar variant (in-pod vs standalone-pod).
- `../images/lecture_7/page033_scaling_horizontal_vertical.png` — 2×2 of horizontal/vertical × workload/infrastructure.
- `../images/lecture_7/page040_prometheus_monitoring.png` — Prometheus monitoring loop with service-discovery + alert manager.
- `../images/lecture_7/page044_dns_mx_query.png` — DNS MX/A query flow then SMTP.
- `../images/lecture_7/page049_cdn_reference_architecture.png` — CDN tiered topology with DDoS/DNS/cache/WAF per tier.
- `../images/lecture_7/page053_sdn_openstack_example.png` — OpenStack SDN topology.
- `../images/lecture_7/page058_openstack_redirect_pool.png` — L7 policy: PATH `/web-api` → REDIRECT_TO_POOL Pool A.
- `../images/lecture_7/page059_latency_decomposition.png` — Total latency y = a + b + c (network + compute + I/O).

**Cross-references to other chapters:** Ch 8 cross-refs throttling-with-dynamic-scaling. Ch 10 reuses Kubernetes vocabulary for securityContext / privilege drop. Ch 11 reuses sidecar for zero-trust. Ch 15 (Linux network stack) shows the *base* of OpenStack SDN (br-int, br-tun, qbr, qvb, qvo). Ch 16 (MLOps) uses Kubernetes for serving + GPU compute.

**Exam-relevance note:** Mock Q8 (the L7 mock-up) is *explicitly* "what is the difference between performance and scalability?" — this is high-yield. Amdahl's formula `y = 1 / (a + (1-a)/p)` is a recall item. Kubernetes terminology (cluster / node / pod / container / kubelet / kube-proxy) appears in both Case #7 and likely the exam. Identifying gateway vs sidecar in a diagram is high probability. Bondi's six dimensions is a recall list.

**Special instructions for the writer:**
- The 2×2 horizontal/vertical × workload/infrastructure matrix is the cleanest "exam-friendly mental model" in L7 — make it shine.
- Include the LUMI supercomputer side-note (Finland, 362k cores) — Ruohonen flags it.
- The mock-up Q-style "identify the pattern in this diagram with `?` marks" warning from L7 is worth a sidebar: *over-answering = zero points*.

---

### Chapter 10: Safety and Security Part 1 — Safety Tactics, Monitor-Actuator, CIA, SIEM, Input Validation, Agentic AI Trust Boundaries, Privilege Drop

**Target pages:** ~14
**Sources to draw from:** lecture_8_analysis.md (primary).
**Goal:** After reading, the student can (a) define safety vs security and contrast the *intentional adversary* axis, (b) fill safety and security scenario templates, (c) draw the safety tactics tree (Avoidance / Detection / Containment / Recovery) with at least 2 sub-tactics per branch, (d) draw the security tactics tree (Detect / Resist / React / Recover) with at least 2 sub-tactics per branch, (e) describe the monitor-actuator pattern and its two variants, (f) describe the SIEM/SOC architecture as a pipe-and-filter with brokers and identify its bottleneck (the GUI/analyst), (g) explain the OWASP Top-10 for LLMs and the LLM gateway placement, (h) recite Arce et al.'s five input-validation principles, (i) explain SRI and CSP as trust-boundary enforcement, (j) list ≥5 *new* trust boundaries that agentic AI introduces, (k) explain Sierra (2026)'s identity-binding / non-repudiation principles, (l) describe CB4A as a broker pattern for short-lived scoped credentials, (m) distinguish privilege drop from privilege separation (qmail/Postfix), (n) describe Kubernetes `securityContext` and OpenBSD `pledge`, and (o) describe egress filtering as output validation (CRA-required).

**Concepts to cover:**
- Safety as a QA (Bass et al.; impact dimension; agnostic to *why* unsafe state was entered) — `lecture_8_analysis.md` §Safety
- Safety scenario template (omission / commission / timing events) — `lecture_8_analysis.md` §Safety scenario template
- Safety tactics tree (Avoidance / Detection / Containment {Redundancy, Limit impact, Barrier} / Recovery) — `lecture_8_analysis.md` §Safety tactics tree
- Monitor-actuator pattern (variant A: drop on fault; variant B: abort on fault) — `lecture_8_analysis.md` §Monitor-actuator pattern
- Security as a QA (CIA-anchored; intentional adversary) — `lecture_8_analysis.md` §Security
- Security tactics tree (Detect / Resist / React / Recover) — `lecture_8_analysis.md` §Security tactics tree
- SIEM / SOC architecture (pipe-and-filter with brokers; bottleneck = GUI/analyst stage; Vakulov 2026 AI assistance) — `lecture_8_analysis.md` §SIEM / SOC
- OWASP Top-10 for LLMs (prompt injection, info disclosure, supply chain, data/model poisoning, improper output validation, excessive agency, prompt leakage, embedding weaknesses, misinformation, unbounded resource consumption) — `lecture_8_analysis.md` §OWASP Top-10 for LLM applications
- LLM gateway placement — `lecture_8_analysis.md` §LLM gateway placement
- Input validation principles (Arce et al. 2014: centralised validator, canonicalisation, state-aware, audit nearby code, strongly-typed memory-safe languages) — `lecture_8_analysis.md` §Input validation
- Attack-surface minimisation — `lecture_8_analysis.md` §Attack-surface minimisation
- Trust boundary (SRI + CSP; ~31% of external JS changes within 10 days) — `lecture_8_analysis.md` §Trust boundary
- Data vs control separation; "Prompt injection is not SQL injection" (NCSC) — `lecture_8_analysis.md` §Data vs control separation
- SRI and CSP standards — `lecture_8_analysis.md` §Subresource Integrity and Content Security Policy
- GitHub Actions case study: secure defaults, scoped secrets, egress filtering — `lecture_8_analysis.md` §GitHub Actions
- Revoke-access tactic (with non-repudiation pairing) — `lecture_8_analysis.md` §Revoke-access tactic
- Trust boundaries for agentic AI (User↔Agent, Agent↔Tool, Tool↔Supply-chain, Execution↔Tool, Agent↔Content, Runtime↔Execution, Host↔Runtime, Memory↔Runtime, Host&Memory↔Kernel, plus Agent↔Task / Task↔Skill / Execution↔Skill from Didi & Zavodchik 2026) — `lecture_8_analysis.md` §Trust boundaries for agentic AI
- Identity binding & non-repudiation for agents (Sierra 2026) — `lecture_8_analysis.md` §Identity binding and non-repudiation
- CB4A (Credential Broker for Agents) IETF draft — `lecture_8_analysis.md` §Credential Broker for Agents
- Least privilege (Adkins et al. 2020; test of privileges / with privileges; breakglass) — `lecture_8_analysis.md` §Least-privilege principle
- Privilege drop vs privilege separation (qmail 1997 = first drop; Postfix = textbook separation) — `lecture_8_analysis.md` §Privilege drop vs privilege separation
- Kubernetes `securityContext.runAsUser` / `runAsGroup` — `lecture_8_analysis.md` §Kubernetes securityContext
- OpenBSD pledge (one-way ratchet); Linux seccomp-bpf / Landlock — `lecture_8_analysis.md` §OpenBSD pledge
- Egress filtering as output validation (CRA-required) — `lecture_8_analysis.md` §Egress filtering
- Agentic AI as a distributed system (CAP / availability / consistency apply directly) — `lecture_8_analysis.md` §Agentic AI as a distributed system

**Diagrams to embed (path + caption):**
- `../images/lecture_8/page017_safety_scenarios.png` — Safety scenario template.
- `../images/lecture_8/page018_safety_tactics_tree.png` — Safety tactics tree.
- `../images/lecture_8/page021_monitor_actuator_pattern.png` — Monitor-actuator pattern (both variants).
- `../images/lecture_8/page022_security_scenarios.png` — Security scenario template.
- `../images/lecture_8/page025_security_tactics_tree.png` — Security tactics tree (Detect / Resist / React / Recover).
- `../images/lecture_8/page028_siem_architecture.png` — Full SIEM architecture (brokers, filters, GUI, alert/notifier).
- `../images/lecture_8/page034_llm_gateway.png` — LLM gateway placement behind firewalls/IDS.
- `../images/lecture_8/page043_input_validation_three_components.png` — Enforcer + Validator + Specification registry input-validation pattern.
- `../images/lecture_8/page058_revoke_access_tactic.png` — Revoke-access via request limits + event allow-lists.
- `../images/lecture_8/page071_securing_ai_agents.png` — Sierra 2026 principles: human↔agentic-identity, scoped tokens, mTLS, zero trust.
- `../images/lecture_8/page073_cb4a_agent_security.png` — CB4A architecture: agent runtime → policy infrastructure → tokens + audit.
- `../images/lecture_8/page077_postfix_privilege.png` — Postfix privilege separation (privileged vs ~16 unprivileged workers).
- `../images/lecture_8/page079_k8s_privilege_drop.png` — Kubernetes privilege drop with `runAsUser` / `runAsGroup` + mTLS + message queue.

**Cross-references to other chapters:** Ch 11 deepens security into Microsoft SDL, threat modeling, kill chain, zero-trust + sidecar, MitM, crypto. Ch 9 (Scalability) is the prerequisite Kubernetes lecture. Ch 7 (Availability) covers fault/failure that safety tactics often share. Ch 13 (catalog) houses SIEM, broker, monitor-actuator entries. The L8 mock questions on pages 7-13 revisit Amdahl, circuit breakers, service discovery, DNS MX, CAP — useful pre-exam pointers.

**Exam-relevance note:** Safety vs security on the *intentional adversary* axis is exam material. Drawing the two tactics trees is high-yield. Input validation 5-point recipe (Arce et al.) is recall-friendly. Privilege drop vs privilege separation (qmail / Postfix) is precision vocab. Kubernetes `securityContext` ties L7+L8 together. Sierra's "authorisation must not depend on the model's interpretation" is quotable.

**Special instructions for the writer:**
- Keep safety and security parallel: same scenario-template + tactics-tree + pattern rhythm; the *difference* is the intentional adversary.
- The OWASP LLM Top-10 list is worth a one-page sidebar that names all ten.
- Privilege drop and privilege separation deserve a clean side-by-side diagram (small redraw if needed).
- The K8s `securityContext` YAML snippet (`runAsUser: 1000, runAsGroup: 2000`) from L8 is the concrete artifact.

---

### Chapter 11: Security Part 2 — Microsoft SDL, Threat Modeling, Kill Chain, Zero-Trust + Sidecar, MitM, Cryptography Lifecycle

**Target pages:** ~13
**Sources to draw from:** lecture_9_analysis.md (primary).
**Goal:** After reading, the student can (a) explain fail-safe vs fail-secure with examples, (b) explain why security is a *constraint* across requirements / architecture / implementation, (c) draw the Microsoft SDL 5-stage / 3-gate pipeline with the zero-trust baseline, (d) describe each SDL gate's coverage (dev-time, CI/CD-time, deploy-time), (e) describe OWASP CI/CD Top-10 risks and the auto-merge restriction recommendations, (f) walk through Microsoft's 4-task threat-modeling loop including the *deviations register*, (g) describe trust boundaries at 3 scales (hardware rings, machine/component, deployment), (h) walk through the cyber kill chain in 8 stages and identify which defences interrupt which links, (i) draw the 3-layer zero-trust architecture (Access / Policy / Resource) and explain why DMZ is insufficient, (j) describe the sidecar pattern *for zero-trust* with its three variants (shared sidecar pod / per-pod / ingress-egress gateway), (k) explain honeypots and deception, (l) describe egress filtering as output validation against C2/exfil, (m) describe the confused-deputy anti-pattern, (n) describe data classification and side-channel attacks, (o) list Conti & Dragoni's 7 MitM countermeasures (and the key caveat that encryption is meaningless without mutual authn + secure key exchange + CA), and (p) explain crypto lifecycle (at rest / in transit / processing window minimisation).

**Concepts to cover:**
- Fail-safe (open) vs fail-secure (closed) — `lecture_9_analysis.md` §Fail-safe vs. fail-secure
- Security as a constraint (not just a QA) — `lecture_9_analysis.md` §Security as a constraint
- Microsoft SDL (Design → Implementation → Build → Deploy → Run) + 3 gates + zero-trust baseline — `lecture_9_analysis.md` §Microsoft Security Development Lifecycle
- Operational security of developers (Zimmermann et al. 2019 npm "small world with high risks") — `lecture_9_analysis.md` §Operational security of developers
- OWASP CI/CD Top-10 + auto-merge restrictions — `lecture_9_analysis.md` §OWASP CI/CD Top-10 risks
- Threat modeling: Microsoft's 4-task loop (assets → architecture overview → threats → countermeasures + deviations register) — `lecture_9_analysis.md` §Threat modeling
- Trust boundaries at 3 scales: hardware/protection rings (ring 0 ↔ ring 3), machine/component, deployment (cloud ↔ on-prem ↔ LAN ↔ WiFi ↔ Internet) — `lecture_9_analysis.md` §Trust boundaries
- Cyber kill chain (8 stages: initial exploit → priv-esc → escape → recon → lateral → exfil → tamper → persist RAT) — `lecture_9_analysis.md` §The cyber kill chain
- Zero-trust architecture (3 layers per NCSC 2025: Access / Policy / Resource) — `lecture_9_analysis.md` §Zero-trust architecture
- Sidecar pattern for zero-trust (shared sidecar pod / per-pod sidecar / ingress-egress gateway) — `lecture_9_analysis.md` §Sidecar pattern for zero-trust
- Honeypots and deception — `lecture_9_analysis.md` §Honeypots and deception
- Egress filtering recap — `lecture_9_analysis.md` §Egress filtering
- Confused deputy (Norm Hardy 1988) + SSRF — `lecture_9_analysis.md` §Confused deputy
- Data classification (GDPR personal-data modules from Hjerppe 2019) — `lecture_9_analysis.md` §Data classification
- Side-channel attacks (Spectre/Meltdown; cache; timing; EM; multi-tenancy) — `lecture_9_analysis.md` §Side-channel attacks
- MitM taxonomy (Conti & Dragoni 2016: impersonation × channel × network location) + 7 countermeasures (mutual authn, secure key exchange, few-secure-channel integrity, CA-signed PKI, cert pinning, encryption, continuous protocol monitoring); caveat that encryption is null without 1, 2, 4 — `lecture_9_analysis.md` §MitM attacks and Conti-Dragoni countermeasures
- Designing for cryptography (in-transit / at-rest / minimise processing window; confidential computing) — `lecture_9_analysis.md` §Designing for cryptography
- CI/CD networking hardening (HTTP → SSH → SSH+HTTPS) — `lecture_9_analysis.md` §CI/CD networking hardening
- Hardening tools for Kubernetes (Checkov, Kubeaudit, KubeLinter, kube-score, Kubesec, Kube-bench, Trivy, NeuVector, StackRox) — `lecture_9_analysis.md` §Hardening tools for Kubernetes

**Diagrams to embed (path + caption):**
- `../images/lecture_9/page013_security_tradeoffs.png` — Security ↔ risk / cost / usability / performance / privacy trade-off pentagon.
- `../images/lecture_9/page020_microsoft_sdl_model.png` — SDL pipeline with 3 gates and zero-trust baseline.
- `../images/lecture_9/page023_owasp_cicd_top10.png` — OWASP CI/CD Top-10.
- `../images/lecture_9/page032_threat_modeling_tasks.png` — Microsoft's 4-task threat modeling loop.
- `../images/lecture_9/page034_protection_rings.png` — CPU/kernel/userland protection rings.
- `../images/lecture_9/page036_trust_boundaries.png` — Deployment-level trust boundaries (cloud / on-prem / LAN / WiFi / Internet).
- `../images/lecture_9/page038_killchain_privesc.png` — Kill-chain stage 2: in-container privilege escalation.
- `../images/lecture_9/page044_dmz_firewall_ids.png` — Why naïve DMZ + firewall + IDS is insufficient given the kill chain.
- `../images/lecture_9/page047_validation_egress_filter.png` — Sidecar validation + egress filter at the cluster edge.
- `../images/lecture_9/page048_zero_trust_architecture.png` — 3-layer zero-trust per NCSC 2025.
- `../images/lecture_9/page049_sidecar_zero_trust.png` — Sidecar pattern with shared authn/authz pod and mTLS everywhere.
- `../images/lecture_9/page052_sidecar_honeypot.png` — Sidecar routing suspicious clients to a honeypot.
- `../images/lecture_9/page062_mitm_protocol_table.png` — MitM × OSI layer table (BGP/DHCP/DNS/TLS/IP/ARP).
- `../images/lecture_9/page068_encryption_lifecycle.png` — Encryption lifecycle (at rest, in transit, minimise processing window).

**Cross-references to other chapters:** Ch 10 set up safety + agentic security + privilege drop + input validation + SBOM handoff — this chapter picks up and deepens. Ch 5 (Testability) connects to Adkins's "test of privileges / with privileges" idea. Ch 6 (Deployability) connects to SDL Gate 2 / CI/CD pipeline integrity. Ch 9 (Scalability) provides Kubernetes prerequisite for the security-context / sidecar discussion. Ch 13 (catalog) houses sidecar, threat-modeling, kill-chain entries.

**Exam-relevance note:** Fail-safe vs fail-secure is an exam-friendly compare/contrast. Drawing the SDL pipeline with the 3 gates is likely. Walking the kill-chain stages is a likely 4-5-point question. Identifying a sidecar variant on a diagram is high probability. The MitM 7-principle list with the encryption-without-authn caveat is recall fodder.

**Special instructions for the writer:**
- The fail-safe / fail-secure split is the section's hook — give it a memorable opening.
- Make the kill-chain a *vertical sequence diagram* with the lessons drawn from each step labelled on the right.
- The MitM countermeasures must list all 7 *with* the caveat that 6 is null without 1, 2, 4 — this caveat is itself an exam point.

---

### Chapter 12: Usability and Power Consumption — TAM, Sub-QAs, Dark Patterns, P-States/C-States, Graceful Degradation

**Target pages:** ~10
**Sources to draw from:** lecture_10_analysis.md (first two-thirds: usability + power consumption sections).
**Goal:** After reading, the student can (a) define usability per Bass et al. and explain why it is a "non-technical" QA, (b) explain the Computer Frustration Model, (c) draw the TAM model (perceived usefulness + perceived ease of use → attitude → intention → use) and identify Bass tactics that target each branch (cancel/undo/pause-resume/automation on usefulness; personalisation on ease of use), (d) name the UZ/UI/UX layering and what can be measured directly vs by proxy, (e) recite the usability sub-QAs (discoverability, learnability, efficiency, simplicity, understandability, flexibility), (f) reapply sub-QAs to *different audiences* (end-user / sysadmin / developer / architect), (g) state Silva et al.'s reference-architecture suitability metric, (h) recall MVC + Observer + Memento as usability-supporting patterns, (i) explain dark patterns and the ethical dimension, (j) decompose machine power = computing + idle + cooling + loss, (k) explain throttling vs P-states vs C-states with their tactic-equivalents (resource scaling) and contradiction (low-latency responsiveness), (l) explain the rule of thumb "minimise software interference with hardware optimisations", (m) distinguish graceful shutdown / graceful degradation / forceful degradation, (n) describe preloading / prefetching / offloading, and (o) summarise language-choice as a power lever (C ≪ Python).

**Concepts to cover:**
- Usability (Bass et al. definition; non-technical QA) — `lecture_10_analysis.md` §Usability
- Computer Frustration Model (Hertzum & Hornaek 2023) — `lecture_10_analysis.md` §Computer Frustration Model
- Technology Acceptance Model (Davis 1989) — `lecture_10_analysis.md` §Technology Acceptance Model
- TAM's missing side: intention to abandon — `lecture_10_analysis.md` §TAM's missing side
- UZ / UI / UX layering and direct vs proxy measurement — `lecture_10_analysis.md` §UZ / UI / UX layering
- Usability sub-QAs (discoverability, learnability, efficiency, simplicity, understandability, flexibility) — `lecture_10_analysis.md` §Usability sub-QAs
- Usability for whom? (end-user / sysadmin / developer / architect; DevOps as a blur) — `lecture_10_analysis.md` §Usability for whom?
- Silva et al.'s suitability metric for reference architectures y = A/B — `lecture_10_analysis.md` §Suitability metric for reference architectures
- Memento pattern for undo (link to L4 rollback and L6 claim-check) — `lecture_10_analysis.md` §Memento pattern
- MVC as a usability pattern (1—* between Controller and View) — `lecture_10_analysis.md` §MVC as a usability pattern
- Observer pattern for statistics / A/B testing — `lecture_10_analysis.md` §Observer pattern for statistics
- Personas (LLM-fit) — `lecture_10_analysis.md` §Personas
- Dark patterns and the ethics of usability — `lecture_10_analysis.md` §Dark patterns
- Power consumption decomposition (computing + idle + cooling + loss) — `lecture_10_analysis.md` §Power consumption — analytical decomposition
- Throttling vs P-states vs C-states (ACPI; P0 = full speed / Pm = lowest; C0 = full performance / Cm = deepest sleep) — `lecture_10_analysis.md` §Throttling vs. P-states vs. C-states
- Hardware wake-ups and "minimise software interference" rule of thumb — `lecture_10_analysis.md` §Hardware wake-ups
- Display dominance — `lecture_10_analysis.md` §Display dominance
- Graceful shutdown vs graceful degradation vs forceful degradation — `lecture_10_analysis.md` §Graceful shutdown vs. degradation
- Preloading (escalating restart in reverse), offloading, prefetching — `lecture_10_analysis.md` §Preloading + §Offloading and prefetching
- Language choice as a power lever — `lecture_10_analysis.md` §Language choice

**Diagrams to embed (path + caption):**
- `../images/lecture_10/fig01_computer_frustration_model.png` — Hertzum & Hornaek (2023) causal model from task + interruption → emotional outcome.
- `../images/lecture_10/fig02_tam_model.png` — Davis (1989) TAM model.
- `../images/lecture_10/fig04_uz_ui_ux_layers.png` — UZ/UI/UX vagueness stack.
- `../images/lecture_10/fig05_usability_subqas.png` — Decomposition of usability into sub-QAs.
- `../images/lecture_10/fig07_mvc_recap.png` — MVC with 1—* cardinality.
- `../images/lecture_10/fig10_usability_for_whom.png` — Audience taxonomy.
- `../images/lecture_10/fig12_reference_architecture_eval.png` — Sub-QAs reapplied to evaluating a reference architecture from an architect's POV.
- `../images/lecture_10/fig21_usability_vs_power.png` — Usability vs power trade-off picture.
- `../images/lecture_10/fig23_per_package_p_states.png` — P-states P0…Pm per CPU package.
- `../images/lecture_10/fig26_c_states.png` — C-states C0…Cm.
- `../images/lecture_10/fig30_power_redundancy.png` — Power decomposition with redundant machines.
- `../images/lecture_10/fig31_graceful_degradation.png` — Graceful degradation 100% → 60% → 25% → shutdown.
- `../images/lecture_10/fig33_preloading.png` — Preloading as escalating restart in reverse.
- `../images/lecture_10/fig34_offloading_prefetching.png` — Offloading vs prefetching directions.

**Cross-references to other chapters:** Ch 3 (Integrability) MVC + Observer recap. Ch 6 (Deployability) connects rollback (Memento). Ch 7 (Availability) connects graceful degradation. Ch 8 (Performance) connects throttling and the responsiveness vs power trade-off. Ch 9 (Scalability) connects offloading as the same primitive. Ch 14 develops "introducing a brand-new QA" (the meta-skill).

**Exam-relevance note:** Define usability + contrast with a technical QA. Draw TAM + identify which Bass tactics target which branch. Sub-QAs list + "usability for whom?" Distinguish graceful shutdown / degradation / forceful degradation (the lecturer asks for an example of forceful degradation from past lectures). P-states vs C-states + which earlier tactic they instantiate + which they contradict. Power decomposition formula. Preloading / prefetching / offloading.

**Special instructions for the writer:**
- The forceful-degradation question is explicitly a "from past lectures" question — provide examples from the dark-patterns slide and the L8 revoke-access tactic.
- Display brightness as the dominant power draw is a quotable factoid.
- Bridge the chapter back to L1's reference-architecture suitability metric (Silva et al.) — it connects to Ch 16 (MLOps reference architecture).

---

### Chapter 13: Pattern + Tactic Reference — Cross-QA Tactics-Tree Comparison and Alphabetical Pattern Catalog

**Target pages:** ~10
**Sources to draw from:** All lecture analyses; this is a synthesizer chapter.
**Goal:** Single canonical reference table for every tactics tree in the course, and an alphabetical pattern catalog with each pattern's canonical home chapter.

**Concepts to cover:**

#### 13.1 Tactics-tree comparison table

One row per QA. Columns: QA, source lecture/chapter, top-level branches, total named tactics, signature pattern, source figure.

| QA | Chapter | Branches | Notable sub-tactics | Signature diagram |
|---|---|---|---|---|
| Integrability | Ch 3 | Limit / Adapt / Coordinate | avoid, bundle, encapsulate; discover, tailor, configure; orchestrate, manage-resources | `lecture_3_p18_img1_integrability_tactics_tree.png` |
| Modifiability | Ch 4 | Reduce coupling / Increase cohesion / Defer binding | split, combine, encapsulate, intermediary, restrict; compile/startup/runtime binding | `lecture_3_p58_img1_modifiability_tactics_tree.png` |
| Testability | Ch 5 | Control & observe input/state / Limit complexity | input gen, record & play, special interfaces, localised storage, assertions, sandboxes | `lecture_4_p19_testability_tactics_tree.png` |
| Deployability | Ch 6 | Manage pipeline / Manage deployment | separate builds, canary, scripted, rollback; multi-version, feature toggle, secure defaults | `lecture_4_p53_deployability_tactics_tree.png` |
| Availability | Ch 7 | Detect / Repair / Reintroduce / Prevent | watchdog, heartbeat, voting; retry+CB, graceful degrade; shadow, restart; isolate, sharding | `lecture_5_p16_page_availability_tactics_tree.png` |
| Performance | Ch 8 | Control demand / Manage resources | manage/limit/prioritize/reduce/bound/efficient; resources, concurrency, copies, queues, schedule | `lecture_6_p11_page_performance_tactics_tree.png` |
| Safety | Ch 10 | Avoidance / Detection / Containment / Recovery | substitution, predictive; sanity, timeout; redundancy, abort, firewall, barrier | `page018_safety_tactics_tree.png` |
| Security | Ch 10–11 | Detect / Resist / React / Recover | intrusions, anomalies; threat modeling, authn, authz, isolate, validate input, encrypt, revoke | `page025_security_tactics_tree.png` |
| Scalability | Ch 9 | (Bondi dimensions instead of tactic tree) load, space, space-time, distance, speed/distance, structural | autoscaler, gateway, sidecar, CDN, SDN | various L7 figures |
| Usability | Ch 12 | (sub-QAs instead of tactic tree) | discoverability, learnability, efficiency, simplicity, understandability, flexibility | `fig05_usability_subqas.png` |
| Power | Ch 12 | (rule of thumb instead of tactic tree) | minimise sw interference; preload, prefetch, offload; graceful degrade | `fig31_graceful_degradation.png` |

#### 13.2 Pattern catalog (alphabetical)

Each entry: pattern name, one-sentence summary, canonical home chapter, cross-refs, source lectures.

- **Active-active / Active-passive load balancing** — Ch 7 (Availability). Refs: Ch 9 (scalability uses same).
- **A/B Testing** — Ch 6 (Deployability). Same machinery as rolling upgrade.
- **Batch-sequential** — Ch 4 (Modifiability). Cousin of pipe-and-filter; cousin of saga (Ch 7).
- **Blue/Green deployment** — Ch 6 (Deployability) — variant of rolling upgrade.
- **Bridge** — Ch 3 (Integrability). General, design-time encapsulation.
- **Broker** — Ch 3 + Ch 10 (SIEM is broker-heavy).
- **Bulkhead** — Ch 7 (Availability). Equitable resource pools.
- **Cache-aside / Refresh-ahead / Write-through / Write-back / Write-around** — Ch 8 (Performance).
- **Canary deployment** — Ch 6 (Deployability). Also referenced for *shadow* recovery in Ch 7.
- **CB4A (Credential Broker for Agents)** — Ch 10 (Safety+Security pt 1). Broker pattern application.
- **Circuit Breaker** — Ch 7 (Availability) is canonical home (state diagram lives there). Ch 8 reuses for throttling.
- **Claim-check** — Ch 8 (Performance). Structurally similar to Memento (Ch 12).
- **Client-Server** — Ch 4 (Modifiability) treats it as a modifiability pattern.
- **Compensating transaction** — Ch 7 (Availability) — saga companion.
- **Decoy / Honeypot** — Ch 11 (Security pt 2).
- **Dependency Injection** — Ch 5 (Testability).
- **Escalating restart** — Ch 7 (Availability). Used "in reverse" as preloading in Ch 12.
- **Feature toggle** — Ch 6 (Deployability).
- **Functional / Analytical redundancy** — Ch 7 (Availability). Cross-ref Ch 10 (safety reuses).
- **Gateway** — Ch 9 (Scalability). Cross-ref Ch 10 (LLM gateway is application of this).
- **Hot / Warm / Cold spare** — Ch 7 (Availability).
- **Intercepting Filter** — Ch 5 (Testability). Conceptually related to Netfilter in Ch 15.
- **Layered architecture** — Ch 1 (Foundations) introduces; Ch 15 (Linux network stack) is a paradigmatic instance.
- **Majority gate / TMR** — Ch 7 (Availability).
- **MapReduce** — Ch 8 (Performance).
- **Materialized View** — Ch 8 (Performance).
- **Mediator** — Ch 3 (Integrability). Runtime general encapsulation.
- **Memento** — Ch 12 (Usability — for undo). Cross-ref Ch 6 (rollback) and Ch 8 (claim-check).
- **Microservices** — Ch 6 (Deployability) treats as a deployment pattern. Cross-ref Ch 9 (scalability), Ch 16 (MLOps).
- **Monitor-Actuator** — Ch 10 (Safety+Security pt 1).
- **MVC** — Ch 4 (Modifiability) is canonical home; Ch 12 (Usability) re-skinning use case.
- **NAPI (kernel hybrid IRQ+polling)** — Ch 15 (Case 1).
- **Observer** — Ch 3 (Integrability) is canonical home; Ch 12 (Usability) reuses for A/B statistics.
- **Pipe-and-filter** — Ch 4 (Modifiability) is canonical home; Ch 10 (SIEM) and Ch 15 (Netfilter, Linux net stack) re-instantiate.
- **Plugin / Micro-kernel** — Ch 4 (Modifiability).
- **Publish-Subscribe** — Ch 3 (Integrability) is canonical home; Ch 7 reuses for quorum/Observer link.
- **Reverse proxy / Ingress gateway** — Ch 11 (Security pt 2). Cross-ref Ch 9 (CDN, L7 LB).
- **Rolling Upgrade** — Ch 6 (Deployability).
- **Saga** — Ch 7 (Availability). Flight+hotel running example.
- **Sandbox** — Ch 5 (Testability) is canonical home; Ch 15 (Linux namespaces) is a deployment-scale instance.
- **Service discovery** — Ch 3 (Integrability) is canonical home; Ch 9 (Kubernetes Services) re-instantiates.
- **Service mesh** — Ch 9 (Scalability). Cross-ref Ch 11 (sidecar variant for zero-trust).
- **Sharding** — Ch 7 (Availability isolation) + Ch 8 (Performance).
- **Sidecar** — Ch 9 (Scalability) canonical home; Ch 11 (Security pt 2) zero-trust variant; Ch 16 (MLOps) optional.
- **SIEM (broker + pipe-and-filter)** — Ch 10 (Safety+Security pt 1).
- **Strategy** — Ch 5 (Testability).
- **Throttling** — Ch 8 (Performance) is canonical home. Cross-refs from Ch 7 (uses circuit breaker), Ch 12 (P-states).
- **VirtIO front-end/back-end (Bridge variant)** — Ch 15 (Case 1).
- **Watchdog / Heartbeat** — Ch 7 (Availability).
- **Wrapper** — Ch 3 (Integrability). Cross-ref Ch 8 (reduce overhead may delete wrappers).

#### 13.3 Cross-cutting concept resolutions (where multi-lecture concepts live)

- **Throttling**: L5 (introduced as availability tactic) + L6 (canonical home as a performance pattern via circuit breaker) + L10 (CPU emergency throttling vs P/C-states). → Canonical home: Ch 8 (Performance). Cross-refs from Ch 7 and Ch 12.
- **Circuit breaker**: L5 (Availability) + L6 (used for throttling). → Canonical home for *state diagram and definition*: Ch 7. Cross-ref Ch 8 reuses.
- **Semver / release engineering**: L3 (modifiability/versioning) + L4 (deployability/release lines). → Canonical home: Ch 4 (the semver figure is embedded there). Ch 6 cross-refs.
- **Privilege drop / Kubernetes securityContext**: L7 (k8s anatomy) + L8 (privilege drop) + L9 (Microsoft SDL Gate 3). → Canonical home: Ch 10. Ch 9 sets up vocabulary; Ch 11 frames as SDL Gate 3.
- **Kubernetes**: L7 (anatomy) + L8 (securityContext) + L9 (hardening tools). → Canonical home for *anatomy*: Ch 9. Ch 10 and Ch 11 extend for security. Ch 16 uses for serving.
- **Sidecar**: L7 (scalability/cross-cutting concerns) + L9 (zero-trust). → Canonical home for *pattern definition*: Ch 9. Ch 11 explicitly covers zero-trust variant.
- **Gateway**: L7 (cluster gateway) + L8 (LLM gateway). → Canonical home: Ch 9. Ch 10 covers LLM-specific application.
- **Defense in depth / cascading risks**: L2 (introduced) + L9 (kill chain motivates). → Canonical home: Ch 2. Ch 11 references in kill chain context.
- **Pipe-and-filter**: L3 (modifiability pattern) + L8 (SIEM realization) + Case 1 (Netfilter at scale). → Canonical home: Ch 4. Cross-refs from Ch 10 and Ch 15.
- **Observer / Pub-Sub**: L3 (integrability) + L10 (A/B usability). → Canonical home: Ch 3. Ch 12 reuses.
- **MVC**: L3 (modifiability) + L10 (usability re-skinning). → Canonical home: Ch 4. Ch 12 reuses.
- **Microservices**: L4 (deployability) + L6 (resilience implicit) + Case 3 (MLOps serving). → Canonical home: Ch 6.
- **Graceful degradation**: L5 (availability tactic) + L10 (power tactic). → Canonical home: Ch 7. Ch 12 reuses.
- **Egress filtering**: L8 (output validation) + L9 (anti-C2/exfil). → Canonical home: Ch 10. Ch 11 reframes with kill chain.
- **CRA (Cyber Resilience Act)**: L2 (mentioned wrt SBOM) + L4 (mandates separated security updates) + L8 (egress filtering compliance). → Canonical home for full mandate: Ch 6. Cross-refs from Ch 2 and Ch 10.

**Special instructions for the writer:**
- This is a reference chapter — design it to be *flippable* (tables, side margins, bold anchor headings).
- Do NOT re-explain the patterns; cross-link only.
- The tactics-tree comparison must use the same column structure throughout, so a student can visually scan across QAs.

---

### Chapter 14: Architecture Evaluation and Introducing New QAs — Bass Procedure, Falessi Factors, ACM Criteria, Rams' Ten Principles, Evaluation Reports

**Target pages:** ~6
**Sources to draw from:** lecture_10_analysis.md (last third); cross-refs to Ch 2 (ATAM-style).
**Goal:** After reading, the student can (a) define architecture evaluation as a risk-reduction action, (b) walk through Bass et al.'s 4-step evaluation procedure, (c) recite Falessi et al.'s 7 evaluation factors, (d) explain the ACM artifact-evaluation 4 axes (documentation, consistency, completeness, execution), (e) describe Dieter Rams' 8 listed principles (especially honesty, environmental friendliness, "as little design as possible"), (f) describe the recommended structure of an evaluation report (6 sections), and (g) explain how to introduce a brand-new QA when no body of knowledge exists (scenarios → transferability check → literature/standards → stakeholders).

**Concepts to cover:**
- Architecture evaluation as risk reduction (Bass et al. 2021) — `lecture_10_analysis.md` §Architecture evaluation as risk reduction
- Bass et al.'s 4-step evaluation procedure — `lecture_10_analysis.md` §Bass et al.'s evaluation procedure
- Falessi et al.'s 7 evaluation factors — `lecture_10_analysis.md` §Falessi et al.'s evaluation factors
- ACM artifact-evaluation criteria — `lecture_10_analysis.md` §ACM artifact-evaluation criteria
- Dieter Rams' ten principles for good design — `lecture_10_analysis.md` §Dieter Rams' ten principles
- Evaluation report content (Bass et al.'s 6-section structure; tabular format) — `lecture_10_analysis.md` §Evaluation report content
- Introducing brand-new QAs (Bass et al.'s 4-step recipe) — `lecture_10_analysis.md` §Introducing brand-new QAs

**Diagrams to embed:** None from L10 specifically — this section is text-heavy. Optionally re-embed `fig12_reference_architecture_eval.png` from Ch 12 to show the evaluator's reuse of usability sub-QAs.

**Cross-references to other chapters:** Ch 2 introduces ASR scenarios that drive evaluation. Ch 15 + Ch 16 are *case studies* the student can imagine evaluating with this machinery.

**Exam-relevance note:** Walking through Bass's evaluation procedure is a likely 3-4-point question. The Rams' principles list (8 of 10 in the slides) is recall-friendly — especially #5 (honest, anti dark-pattern) and #7 (environmentally friendly, ties to power consumption). The "introducing a new QA" 4-step recipe is meta-skill material the lecturer flagged as durable.

**Special instructions for the writer:**
- Keep this chapter tight (6 pages) — it is conceptual scaffolding, not deep content.
- The "introducing a brand-new QA" recipe is the meta-message of the course. Highlight it.
- Tie Rams principle #7 ("environmentally friendly") back to Ch 12's power consumption discussion explicitly.

---

### Chapter 15: Case Study Walkthrough 1 — The Linux Network Stack (Horvat Poster)

**Target pages:** ~10
**Sources to draw from:** case_1_analysis.md (primary); cross-refs to Ch 1 (layered), Ch 4 (pipe-and-filter), Ch 8 (performance tactics), Ch 9 (k8s SDN), Ch 10 (sandbox).
**Goal:** After reading, the student can (a) name the four "worlds" stacked into the poster (host stack / virtualization / container / SDN), (b) trace a packet end-to-end through any one world, (c) identify three patterns + three tactics + one trade-off in any cropped region of the poster, (d) map QAs to mechanisms (performance → NAPI+offloads; modifiability → pluggable congestion-control/qdisc/bridge; security → Netfilter + namespaces + VLAN/VxLAN; availability → bonding/LACP), and (e) articulate the canonical trade-offs (bufferbloat, isolation strength vs cost, offload speed vs debuggability, layering modularity vs cross-layer overhead).

**Concepts to cover (case-specific):**
- The four-worlds poster overview — `case_1_analysis.md` §Scenario
- Strict layering as the spine of the host stack — `case_1_analysis.md` §Architectural decision 1
- Pipe-and-filter with hooks (Netfilter at PREROUTING/INPUT/FORWARD/OUTPUT/POSTROUTING) — `case_1_analysis.md` §Architectural decision 2
- Virtualization via VirtIO paravirtual driver (front-end/back-end split) — `case_1_analysis.md` §Architectural decision 3
- Namespaces as isolation tactic (mount, PID, UTS, user, network, cgroup) + cgroups + VETH pair — `case_1_analysis.md` §Architectural decision 4
- Linux bridge vs Open vSwitch (br-int / br-tun, VLAN/VxLAN, patch ports) — `case_1_analysis.md` §Architectural decision 5
- Hardware acceleration at the boundary (RSS, aRFS, LRO, TSO, GSO, checksum offload, scatter-gather, multi-queue, XDP) — `case_1_analysis.md` §Architectural decision 6
- Buffering at every queueing point (SKB, tcp_rmem/wmem, netdev_max_backlog, qdisc, txqueuelen, driver ring buffers); bufferbloat trade-off — `case_1_analysis.md` §Architectural decision 7
- NAPI hybrid interrupt + polling — `case_1_analysis.md` §Architectural decision 8

Packet-trace walkthrough exercise: walk a packet from a VM on one OpenStack compute node to a VM on another — guest app → guest socket/TCP/IP → virtio_net front-end → virtio_net back-end (host) → TAP → qbr Linux bridge → qvb/qvo VETH pair → OVS br-int (VLAN tag) → patch port → OVS br-tun (VxLAN encapsulate) → eth0 qdisc → driver → NIC.

**Diagrams to embed (path + caption):**
- `../images/case_1/case1_full_diagram.png` — Full Linux network stack poster (Horvat v1.45). Use as the chapter opener; one *very* large reproduction, full page if needed.
- `../images/case_1/case1_host_stack_socket_tcp_ip.png` — Host stack: applications → socket → TCP/UDP → IP → qdisc → driver with sysctl tunables labelled. Use to illustrate layering.
- `../images/case_1/case1_vm_virtio_kvm.png` — VM, VirtIO front-end / back-end, KVM hypervisor + full emulation alternative.
- `../images/case_1/case1_ovs_bridge_namespaces.png` — Linux bridge vs OVS (br-int / br-tun, VLAN, VxLAN). Use for the SDN section.
- `../images/case_1/case1_nic_hw_offload.png` — NIC hardware offload (RSS, aRFS, LRO, TSO), IRQ affinity, XDP entry. Use for the performance-tactic section.

**Cross-references to other chapters:** Ch 1 (layering), Ch 4 (pipe-and-filter / pluggability), Ch 7 (bonding/LACP redundancy), Ch 8 (performance tactics — NAPI, scheduling, multi-queue), Ch 9 (Kubernetes / SDN / OpenStack), Ch 10 (sandbox via namespaces, isolation), Ch 13 (catalog).

**Exam-relevance note:** The lecturer explicitly framed this case as "look at this diagram and identify three architectural patterns, three tactics, and one trade-off." The packet-trace walkthrough is extremely likely as a 4-5-point question. Identifying which subsystem a cropped region belongs to is also likely.

**Special instructions for the writer:**
- This chapter is *visual-first*. Make the poster the dominant artifact.
- Write the packet-trace walkthrough as numbered steps with the poster region highlighted alongside each step.
- For every architectural decision, name a concrete sysctl / ethtool / `/proc/net/*` tunable — the lecturer values "every QA leaves a fingerprint as a tunable".
- Cross-link aggressively back to the lecture chapters; this is where the *applications* live.

---

### Chapter 16: Case Study Walkthrough 2 — MLOps Reference Architecture (Kreuzberger et al.)

**Target pages:** ~10
**Sources to draw from:** case_3_analysis.md (primary); cross-refs to Ch 2 (reference architecture), Ch 4 (DAGs as modifiability), Ch 6 (CI/CD), Ch 7 (control loop), Ch 9 (Kubernetes serving).
**Goal:** After reading, the student can (a) define MLOps and explain why most ML POCs fail, (b) name the 7 roles (R1–R7) and the cross-functional ML/MLOps engineer, (c) name the 9 components (C1–C9), (d) sketch the end-to-end MLOps architecture from memory (Fig 4), (e) explain the principles ↔ components ↔ roles mapping, (f) identify each component's primary QA driver and trade-off, (g) explain the feature-store dual-DB pattern (offline + online; training/serving skew), (h) explain the model registry + metadata store + versioning approach (P3, P4, P7), (i) describe the monitoring → retraining feedback loop as a control-loop / circuit-breaker-style pattern (drift → retrain), (j) describe CI/CD for ML and its differences from classical CI/CD, and (k) explain why MLOps is a *technology-agnostic reference architecture* and the over-conformance trade-off.

**Concepts to cover (case-specific):**
- MLOps scenario (the recurring industrial failure mode) — `case_3_analysis.md` §Scenario
- 7 roles (R1 Business / R2 Architect / R3 Data Scientist / R4 Data Engineer / R5 Software Engineer / R6 DevOps / R7 ML/MLOps Engineer) — `case_3_analysis.md` §Stakeholders & context
- QA parade (deployability, testability, modifiability, integrability, reproducibility, observability, scalability, availability, governance) — `case_3_analysis.md` §Quality attributes in play
- Decision 1: Pipelines as the unit of work (DAG orchestration: Airflow, Kubeflow, SageMaker Pipelines) — `case_3_analysis.md` §Decision 1
- Decision 2: Feature store with offline + online DBs — `case_3_analysis.md` §Decision 2
- Decision 3: Model as a first-class versioned artifact (registry + metadata store) — `case_3_analysis.md` §Decision 3
- Decision 4: Continuous training driven by monitoring feedback loops (drift → retrain) — `case_3_analysis.md` §Decision 4
- Decision 5: CI/CD for both code and model artifacts — `case_3_analysis.md` §Decision 5
- Decision 6: Serving via containerised REST APIs (real-time / batch / serverless; champion-challenger A/B) — `case_3_analysis.md` §Decision 6
- Decision 7: Technology-agnostic reference architecture — `case_3_analysis.md` §Decision 7
- Decision 8: Cross-functional ML/MLOps engineer role — `case_3_analysis.md` §Decision 8

**Diagrams to embed (path + caption):**
- `../images/case_3/fig1_methodology.png` — Methodology overview (SLR + tool review + expert interviews).
- `../images/case_3/fig2_principles_to_components.png` — Principles realised by technical components (P × C mapping).
- `../images/case_3/fig3_roles_intersection.png` — Roles and their intersections.
- `../images/case_3/fig4_end_to_end_architecture.png` — End-to-end MLOps architecture and workflow. *Anchor figure of the chapter — give it a full page.*
- `../images/case_3/fig5_disciplines_intersection.png` — Intersection of disciplines defining MLOps.
- `../images/case_3/table1_tools.png` — Evaluated technologies.

**Cross-references to other chapters:** Ch 2 (reference architectures), Ch 4 (DAGs as modifiability, MVC analogy to model-data-controller), Ch 6 (CI/CD pipeline structure), Ch 7 (monitoring → retraining as control-loop / circuit-breaker), Ch 9 (Kubernetes serving), Ch 13 (microservices, sidecar, broker entries).

**Exam-relevance note:** "Design an end-to-end reference architecture for X" with Fig 4 as the implicit template is high-probability. Mapping QAs to components is high-probability. The roles ↔ Conway's law connection ties to L1's stakeholder-management emphasis. CI/CD for ML differences from classical CI/CD is a likely contrast question. The feature-store offline+online pattern explains training/serving skew — quotable.

**Special instructions for the writer:**
- Build the chapter around Fig 4 — refer back to it for every decision.
- For each component (C1-C9), name at least one concrete tool example from Table 1.
- The control-loop framing (monitoring → drift → retrain → redeploy) is the chapter's intellectual climax — make it sing.
- Conclude with the "you can't *buy* MLOps; the cultural/role shift is the hard part" lesson.

---

### Chapter 17: Exam Preparation — Question Archetypes, Walkthrough Strategies, Drawing Conventions, Soft-Skill Section

**Target pages:** ~8
**Sources to draw from:** lecture_10_analysis.md (lecturer's exam guidance, page 2); all lecture analyses' "Exam-relevant takeaways" sections; the running mock-up Q1–Q8 questions seen in L7 and L8.
**Goal:** After reading, the student is psychologically and tactically ready for the exam: knows the format (16 / 34 / 17 to pass), knows what kind of question to expect, knows what *not* to do (over-answer), and has a one-page cheat-sheet for last-minute review.

**Concepts to cover:**
- Exam format from L10 p2: 16 questions worth 34 points total; passing at 17; question worths are 1/2/3/4/5; smartphones allowed for digitising drawings; "anything that appeared in the lectures may appear in the exam — slides alone are not sufficient; you must be able to *apply*."
- The soft-skill section (Ch 1 already covered): articulation, stakeholder management, communication / negotiation are *exam-counted* qualities of architects. Be prepared to discuss why architects are 70% communicators.
- "Over-answering = zero points" warning (from L7 mock-Q style): keep answers brief and prioritised.
- Drawing conventions: students must draw on paper, photograph, and submit. Practice 4+1 viewpoint sketches, tactics-tree sketches, circuit breaker state diagram, saga sequence, Kubernetes pod hierarchy, MLOps Fig 4 from memory.
- Likely exam archetypes (one per row in a recall table):

| Archetype | Example phrasing | Source chapters | Points |
|---|---|---|---|
| Verbatim definition | "Define software architecture (Bass et al.)" | Ch 1 | 1-2 |
| Vocabulary trio | "Distinguish fault / failure / trigger" | Ch 7 | 2-3 |
| Scenario fill | "Fill the 6-slot availability scenario for X" | Ch 2 + relevant QA chapter | 3-4 |
| Tactics tree | "Draw and label the availability tactics tree with at least 2 tactics per branch" | Ch 7 / Ch 13 | 4-5 |
| Pattern comparison | "Compare Observer to Pub-Sub across six rows" | Ch 3 | 3 |
| Identify pattern in diagram | "Identify three patterns in this cropped poster region" | Ch 15 | 3-4 |
| QA trade-off | "Explain the security ↔ availability trade-off using CIA-A" | Ch 7 + Ch 10 | 2-3 |
| Walkthrough | "Walk a packet from VM-A to VM-B in an OpenStack 2-node deployment" | Ch 15 | 4-5 |
| Saga / compensating | "Walk through saga for flight + hotel booking" | Ch 7 | 3-4 |
| CAP/PACELC classification | "Classify Cassandra and Spanner by PACELC" | Ch 8 | 2-3 |
| Kubernetes vocab | "What is the difference between kubelet and kube-proxy?" | Ch 9 | 1-2 |
| Soft-skill discussion | "Why are architects' top job qualities communication-related?" | Ch 1 / Ch 17 | 2-3 |
| Architecture evaluation | "Outline Bass et al.'s evaluation procedure and report structure" | Ch 14 | 3 |
| Brand-new QA | "How would you introduce a new QA for LLM-integration?" | Ch 12 / Ch 14 | 3-4 |
| Quotable trade-off | "Fail-safe vs fail-secure — give one example of each" | Ch 11 | 2 |

**Diagrams to embed:** Optionally reproduce the 4+1 viewpoint figure (Ch 1) and the circuit-breaker state diagram (Ch 7) as drawing exemplars.

**Special instructions for the writer:**
- This chapter is a *strategy* chapter. Keep it short, punchy, listy.
- The "over-answering = zero points" warning is a recurring lecturer emphasis (from L7 mock-up framing). Lead with it.
- Include 2-3 worked sample answers to the highest-yield archetypes (saga walkthrough; pattern identification on a diagram; CAP/PACELC classification).
- End with a one-page "What to memorise" cheat-sheet (cross-ref to back-matter).

---

## Cross-cutting elements (NOT chapters)

### Tactics-tree comparison table

Lives in Chapter 13. Every tactics tree from L3-L10 is collected into one cross-QA table that lets the student scan across QAs in a single page. Branches and sub-tactic counts are normalised.

### Pattern catalog (alphabetical)

Lives in Chapter 13. Each pattern has one canonical home chapter with cross-refs to others where the same pattern is reused. Resolutions of the multi-lecture patterns:

- **Throttling** — canonical home Ch 8 (Performance); L5 introduces, L6 finalises, L10 contrasts with P-states.
- **Circuit Breaker** — canonical home Ch 7 (Availability); L6 reuses for throttling.
- **Semver** — canonical home Ch 4 (Modifiability); L4 cross-refs.
- **Privilege drop / K8s securityContext** — canonical home Ch 10; L7 sets up Kubernetes anatomy; L9 ties to SDL Gate 3.
- **Sidecar** — canonical home Ch 9 (Scalability); Ch 11 covers zero-trust variant.
- **Gateway** — canonical home Ch 9; Ch 10 covers LLM-gateway application.
- **Pipe-and-filter** — canonical home Ch 4 (Modifiability); Ch 10 (SIEM) and Ch 15 (Netfilter) reuse.
- **Observer / Pub-Sub** — canonical home Ch 3; Ch 12 reuses for A/B statistics.
- **MVC** — canonical home Ch 4 (Modifiability); Ch 12 reuses for re-skinning.
- **Microservices** — canonical home Ch 6 (Deployability); used heavily in Case 3.
- **Saga** — canonical home Ch 7; flight+hotel running example.
- **Bulkhead** — canonical home Ch 7.
- **Sandbox** — canonical home Ch 5; Ch 15 (Linux namespaces) is the deployment-scale instance.
- **Broker** — canonical home Ch 3; Ch 10 (SIEM) and Ch 11 (CB4A) reuse.
- **Bridge / Wrapper / Mediator** — canonical home Ch 3.
- **Hot-Warm-Cold spare** — canonical home Ch 7.
- **Plugin / Micro-kernel** — canonical home Ch 4.
- **Defense in depth** — canonical home Ch 2 (Risk); Ch 11 references in kill chain context.
- **Layered architecture** — canonical home Ch 1; Ch 15 (Linux net stack) is the paradigmatic instance.

### Running examples used by the lecturer

- **Flight-and-hotel reservation** — introduced L1 (vocabulary), runs as the canonical saga example in L5 (Ch 7). Use it in any chapter that needs a worked example.
- **Linux network stack (Horvat poster)** — full case study in Ch 15. Implicitly referenced throughout the QA chapters.
- **MLOps reference architecture (Kreuzberger et al.)** — full case study in Ch 16.
- **Netflix Hystrix** — L6's Case #5; canonical circuit-breaker / throttling example in Ch 7 and Ch 8.
- **Healthcare emergency system** — L1's tensions-illustration sketch; used in Ch 1.
- **Manufacturing automation (5-layer)** — L1's layering example; used in Ch 1.
- **Ruohonen's own publications**:
  - NetBSD test evolution (flagged oracles) — Ch 5.
  - Linux kernel regression patterns (Ruohonen & Alami 2024) — Ch 5.
  - EU CRA mapping (Ruohonen et al. 2025) — Ch 6 + Ch 2 + Ch 10.
  - Secure defaults (Ruohonen 2025) — Ch 6 + Ch 10.
  - External JS / SRI study (Ruohonen et al. 2018) — Ch 10.
- **CrowdStrike (2024) + Cloudflare (2025) incidents** — opens L5; used as bridge in Ch 5 / Ch 6 / Ch 7.

### Likely exam question patterns (passed to chapter writers in Ch 17)

12 archetypes derived from the analyses (full list lives in Ch 17). The chapter writers can use these to *focus* their content:

1. Define an architectural term verbatim (e.g., software architecture, QA, ASR, tactic, pattern, saga, circuit breaker, bulkhead).
2. Fill the 6-slot QA scenario for a given QA + given situation.
3. Draw a tactics tree from memory (most likely candidates: availability, security, performance).
4. Compare two patterns (most likely: Observer vs Pub-Sub; Wrapper vs Bridge vs Mediator; rolling upgrade vs A/B).
5. Identify the pattern in an unlabeled diagram and explain its rationale in brief, prioritised sentences (lecturer warns: over-answering = zero points).
6. Walk a packet / saga / kill chain step by step.
7. Reason about a trade-off (performance vs availability; security vs usability; modifiability vs performance).
8. Classify a system by CAP / PACELC.
9. Explain a Ruohonen publication (CRA, secure defaults, NetBSD oracles, Linux regressions).
10. Discuss the architect's role and soft-skill emphasis.
11. Outline Bass et al.'s evaluation procedure / evaluation report structure.
12. Introduce a brand-new QA (4-step recipe).

## Front matter

- **Cover page text:** "Software Architecture — A Walkthrough for the Spring 2026 Exam (Course T630019402, Jukka Ruohonen, SDU). Topic-organised study guide synthesised from 10 lectures and 2 case studies."
- **Table of contents:** Auto-generated from chapter headings, two levels deep.
- **"How to use this guide" intro (~1 page):** Explain the topic-organisation philosophy (vs lecture-by-lecture), how to use the running examples, how the QA chapters share a common structure (definition → 6-slot scenario → tactics tree → patterns → trade-offs), how to cross-reference, and how Chapter 17 ties everything to the exam.
- **Course map (~1 page):** Single-page visual showing how the chapters map to lectures, with case-study placement.

## Back matter

- **Concept glossary** (alphabetical, ~3-5 pages). Every term from the analyses that has a Bass-or-Fairbanks definition, plus the lecturer's idiosyncratic vocabulary (twin peaks mountain range, verification debt, "the new technical debt", etc.).
- **Acronym index** — list every acronym found in the analyses:
  - 4+1 (Kruchten viewpoints), ACID, ACPI, ACL, aRFS, ARP, ASR (Architecturally Significant Requirement), ASRs, ATAM, AWS
  - BDUF, BGP, BIOS
  - C2 (Command & Control), CA (Certificate Authority), CAP (Consistency Availability Partition), CB4A (Credential Broker for Agents), CD (Continuous Deployment), CDN, CI (Continuous Integration), CIA (Confidentiality Integrity Availability), CRA (Cyber Resilience Act), CRC, CSP (Content Security Policy), CVE
  - DAG, DevOps, DHCP, DMZ, DNS, DoS, DRY (Don't Repeat Yourself)
  - EDF (Earliest Deadline First), eBPF, ELK, EM (Electromagnetic), ETL
  - FIFO, FQ_codel
  - GC (Garbage Collection), GDPR, GitOps, GPU, GRO/GSO
  - HPA (Horizontal Pod Autoscaler), HPC, HTTPS
  - IaaS, IDS, IETF, IPC, IRQ, ISO/IEC 25010
  - JSON
  - K8s (Kubernetes), KPI
  - L7 (Layer 7), LACP, LB (Load Balancer), LCM, LRO, LSP (Liskov Substitution Principle), LTS
  - mTLS, MFA, MitM (Man-in-the-Middle), MLOps, MTBF, MTTR, MTTF, MTBF, MVC, MX (Mail Exchange)
  - NAPI, NCSC, NHPP (Non-Homogeneous Poisson Process), NIC, NIST CSF, NTP
  - OCP (Open-Closed Principle), OIDC, OS, OSI, OSS, OWASP, OVS (Open vSwitch)
  - P0/Pm, P99, PA/EL, PACELC (Partition-Availability/Consistency-Else-Latency/Consistency), PC (Protection-Consistency), PCI DSS, PKI, PoC, POSIX
  - QA (Quality Attribute), QoS, qdisc
  - RAM, RAT (Remote Access Trojan), RCE, REST, RFC, RFS, RPS, ROI, RSS, RBAC, ROI
  - SaaS, SBOM, SCADA, SDK, SDL (Microsoft Security Development Lifecycle), SDN (Software-Defined Networking), seccomp, semver, SIEM, SLA, SLO, SOAP, SOC (Security Operations Center), SOLID, SPIFFE, SPIRE, SQL, SRE, SRI (Subresource Integrity), SRP (Single Responsibility Principle), SSD, SSH, SSL, SSRF, STIX, SVM, SVN
  - TAM (Technology Acceptance Model), TAP, TCO (Total Cost of Ownership), TCP/IP, TLS, TMR (Triple Modular Redundancy), TTP
  - UDP, UI, UTS, UX, UZ
  - VLAN, VxLAN, VM, VPN, VRRP
  - WAF (Web Application Firewall), WSDL
  - X-as-code, XDP, XML
- **Bibliography of cited works:**
  - Books: Bass / Clements / Kazman (2021); Fairbanks (2010); Lano & Tehrani; Adkins et al. (2020, Google "Building Secure & Reliable Systems"); Richards (2015).
  - Standards: IETF RFC 1958; RFC 3552; ISO/IEC 25010; OWASP Top-10 for LLM applications; OWASP CI/CD Top-10; CycloneDX 1.7; NCSC Zero Trust Architecture (2025); EU CRA.
  - Key papers: Ammann & Offutt (2008); Bondi (2000); Cleland-Huang et al. (2013); Davis (1989); Dean & Ghemawat (2008 — MapReduce); Hill & Marty (2008); Kruchten (1995); Latendresse et al. (2022); Lübke et al. (2019); Yang et al. (2016 — Iteration 0); Zimmermann et al. (2019 — npm); Kreuzberger / Kühl / Hirschl (2023 — MLOps); Conti & Dragoni (2016); Barr et al. (2015 — oracles); Brewer (2000 — CAP); Abadi (2010 — PACELC); Brooker (2019 — jitter); Cho (1999 — stochastic fairness queueing); Hertzum & Hornaek (2023 — frustration); Wei et al. (2025 — X-as-code).
  - Ruohonen's own publications: Ruohonen & Rindell (2019 — kernel syzkaller); Ruohonen & Alami (2024 — Linux regressions); Ruohonen et al. (2018 — external JS / SRI); Ruohonen et al. (2025 — CRA mapping); Ruohonen (2025 — secure defaults); Hjerppe (2019 — GDPR personal-data modules); Vakulov (2026 — SIEM AI); Sierra (2026 — agentic identity); Williams (2026 — resilience as debt); Bouzoukas (2026 — verification debt); Chou et al. (2025 — vibe coding); Ose & Glass (2026 — GitHub Actions); Didi & Zavodchik (2026 — agentic skill boundaries).
- **"What to memorize" — 1-page final cheat-sheet:**
  - Bass-Clements-Kazman definition of software architecture (verbatim).
  - The 10-term vocabulary (one line each).
  - The 6-slot QA scenario template.
  - The 5 component-design principles (cohesion, segregation, SRP, OCP, no-vendor-lock-in).
  - The Liskov substitution rule (more provided OK, more required not).
  - ISO/IEC 25010 — 8 top-level categories.
  - Risk = Probability × Impact.
  - The 4 oracle types (specified / pseudo / implicit / derived).
  - The 5 distance sub-axes (syntactic / data-semantic / behavioural-semantic / temporal / resource).
  - Limit / Adapt / Coordinate (integrability tactics tree).
  - Five modifiability moves (split / combine / encapsulate / intermediary / restrict).
  - Semver = MAJOR.MINOR.PATCH; Lübke's 5 alternatives.
  - Detect / Repair / Reintroduce / Prevent (availability tactics tree).
  - Circuit breaker = Closed / Open / Half-open.
  - CAP = at most 2 of {C, A, P}; PACELC adds the Else (L vs C) when no partition.
  - 5 cache patterns: cache-aside / refresh-ahead / write-through / write-back / write-around.
  - Performance scheduler family: FIFO / SJF / EDF / rate-monotonic / round-robin / idle / batch / semantic-importance.
  - Amdahl's law: y = 1 / (a + (1-a)/p); max = 1/a.
  - Kubernetes anatomy: cluster / node / pod / container; kubelet (health) vs kube-proxy (TCP/IP).
  - Bondi's 6 scalability dimensions.
  - Safety tactics tree: Avoidance / Detection / Containment / Recovery.
  - Security tactics tree: Detect / Resist / React / Recover.
  - Microsoft SDL: 5 stages, 3 gates, zero-trust baseline.
  - Cyber kill chain: 8 stages from initial exploit to RAT.
  - MitM 7 countermeasures (and the caveat that #6 is null without #1, #2, #4).
  - TAM = perceived usefulness + perceived ease of use → attitude → intention → use.
  - Usability sub-QAs: discoverability / learnability / efficiency / simplicity / understandability / flexibility.
  - Power = computing + idle + cooling + loss.
  - Graceful shutdown ≠ graceful degradation ≠ forceful degradation.
  - Bass et al.'s evaluation procedure: 4 steps + 6-section report.
  - Architect's top 3 qualities: articulation, stakeholder management, communication/negotiation.
