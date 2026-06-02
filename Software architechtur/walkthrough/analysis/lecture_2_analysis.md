# Lecture 2: Quality Attributes, Requirements Engineering, and Risk-Based Architecture

> **Source:** lecture_2.pdf (76 pages)
> **Lecturer:** Jukka Ruohonen
> **Date (if stated):** February 17, 2026 (from PDF title)

## Themes covered

- Software architecture's relationship to agile development (BDUF vs. Iteration 0 vs. Emergent)
- Quality attributes (QAs) as measurable, testable, falsifiable properties — and the ISO/IEC 25010 taxonomy
- The fuzzy boundary between functional and non-functional requirements
- QA scenarios as a structured way to specify quality requirements
- Risk-based reasoning: probability x impact, cascading risks, defense in depth, positive vs. negative risks
- Requirements engineering for architecture: "sniffing" architecturally significant requirements (ASRs) from documents, ASR workshops, quality gates
- Reference architectures and standards as ASR carriers
- Domain modeling: domain model -> boundary model -> architecture model, designation vs. refinement
- Non-technical (business) QAs: time-to-market, total cost of ownership
- Deployment modeling: components, machines, environments, and the SBOM (CycloneDX) requirement

## Concepts

### Quality Attribute (QA)
**Definition:** A measurable or testable property of a system that indicates how well the system satisfies stakeholder needs *beyond* its basic functions (Bass et al. 2021).
**Why it matters:** A system can implement every functional requirement perfectly and still be a disaster — slow, insecure, unmaintainable. QAs are how architects decide *which* tradeoffs to make in the design.
**Detailed explanation:** A QA is always anchored to a stakeholder need but is distinct from "the basic function" of the system. Crucially, the definition demands measurability or testability — so a QA must eventually be reducible to numbers or pass/fail tests. Many QAs (performance, availability) lend themselves to this; others (security, usability) are harder and require decomposition: QAi -> {SubQAi1, ..., SubQAin}, where each sub-QA is in turn refined into concrete metrics. Many QAs also require understanding *runtime* behavior, not just source code — you cannot read a code listing and conclude "this system has high availability."
**Analogy:** A car's functional requirement is "drives from A to B." Its QAs are how it does so: acceleration (performance), fuel economy (efficiency), crash safety, brake response (availability), how easily a mechanic can swap a part (maintainability). Two cars can both "drive from A to B" yet one is a Ferrari and the other a moped — the QAs are what separates them.
**Example:** "A system should be secure" is a worthless QA (not measurable). "The system shall comply with PCI DSS" is much better. "The system shall scale" is worthless. "The web application shall scale up to ten million users within a year of operation" is much better.
**Common pitfall / nuance:** Students confuse a QA with a feature. "Adds a dashboard button" is a function; "the dashboard renders in under 200 ms at the 99th percentile under 5k concurrent users" is a QA. The mark of a good QA is whether you can write a falsifiable test for it.

### Functional vs. Non-Functional Requirements
**Definition:** Functional requirements specify *what* the system does (concrete behaviors that deliver utility/business value to stakeholders); non-functional requirements specify *how well* it does them, and they map onto QAs.
**Why it matters:** Almost every requirements document is dominated by functional requirements; QAs have to be inferred or "sniffed" out. If you do not actively look for them, your architecture will silently optimize for nothing in particular.
**Detailed explanation:** The line between the two is famously fuzzy. A "function" — say, drive an engine — cannot be designed without immediately invoking QAs (performance, fuel efficiency, emissions). Bass et al. (2021) suggest that the cleanest practical move is to *decompose* non-functional requirements into functional ones whenever possible. The lecture's car-ownership sketch is illustrative: the high-level non-functional requirement "Security" decomposes into "Access controls," which decomposes into the concrete functions "A key unlocks the doors" and "A key starts the car."
**Analogy:** "I want a delicious dinner" is non-functional. "Serves four people, ready in 30 minutes, peanut-free, under 600 calories" is the decomposition into functions you can actually cook against.
**Example:** "Pressing a button shows daily analytics" looks purely functional, but it simultaneously implies *performance* (how fast?), *availability* (how often is it allowed to fail?) and *modifiability* (can you add new algorithms later?). One feature, three overlapping QAs.
**Common pitfall / nuance:** Treating non-functional requirements as second-class citizens. They are often the things that get you fired when they fail.

### Architecturally Significant Requirements (ASRs)
**Definition:** The subset of requirements — usually QA-related — that meaningfully constrain or shape the architecture (Bass et al. 2021).
**Why it matters:** A "perfect" architecture would fulfill *every* QA, but that is impossible (tensions exist). ASRs are the ones you cannot ignore without breaking the architecture. They are what the architect must spend time on.
**Detailed explanation:** Most requirement documents are full of functional details that do not affect the architecture at all (CRUD forms, button colors). To find the ones that do, you "sniff" the documents for signals: named technologies/vendors, integration points to external systems, deployment hints (cloud?), data volumes and rates, networking constraints (TCP/IP? 5G? Bluetooth? custom protocol?), expected user counts and i18n, legal/compliance regimes (GDPR, PCI DSS). Each of these is a clue that an ASR lurks underneath.
**Analogy:** When buying a house you read the listing, but you also walk the neighborhood at 2 a.m., check flood maps, and look up the school district. The listing is the requirements doc; the rest is sniffing for ASRs.
**Example:** The lecture's small interview snippet ("we operate in two European countries… BYOD principle… SAP integration… on-premise servers… 200 employees but only ~3 users") yields ASRs about: SAP integration (interoperability), GDPR (security/compliance), BYOD (security + portability), small scale (no need to over-architect for scalability), on-premise (deployment constraint).
**Common pitfall / nuance:** Confusing "architecturally significant" with "important to the user." A user might desperately want a dark mode toggle; that is important but architecturally trivial. ASRs are about what shapes the *structure*.

### QA Scenario
**Definition:** A structured specification of a quality attribute as a (Source, Event, Environment, Deployment, Response, Response Measure) tuple.
**Why it matters:** It forces vague QAs into a form that is concrete, testable, and easy to share with stakeholders. It also aligns naturally with agile artifacts (user stories, use cases, misuse cases).
**Detailed explanation:** The template asks: who/what is the *source* of the stimulus (a user, attacker, sensor, peer system)? What *event* do they trigger (a fault, a request, an attack, a misconfiguration)? In what *environment* and *deployment* (new deployment, degraded operation, overloaded mode)? What *response* must the system produce (detect, prevent, recover, log)? And what is the *response measure* (time to detect, time to recover, success ratio)? Filling these slots converts the woolly statement "the system should be reliable" into something an engineer can build and a tester can check.
**Analogy:** A QA scenario is the system's equivalent of a fire drill: *given* the building is on fire (event), *with* this many people inside (environment), *the alarm must sound within 10 seconds and everyone must be out within 4 minutes* (response + measure).
**Example:** Source = external user; Event = network packet flood (denial-of-service); Environment = peak business hours; Deployment = current production; Response = detect and rate-limit; Response measure = detection within 30 seconds, throughput retained at >= 80% of nominal for legitimate users.
**Common pitfall / nuance:** Students write scenarios that omit the *response measure*. Without numbers, the scenario is just a story.

### ISO/IEC 25010 QA Taxonomy
**Definition:** An international standard organizing software quality into eight top-level categories: functional suitability, performance (efficiency), compatibility, usability, reliability, security, maintainability, and portability — each with sub-attributes.
**Why it matters:** It is a shared vocabulary. When two teams argue about "availability," they can point to ISO/IEC 25010 to agree on what they mean. It also serves as a checklist so you do not forget whole categories.
**Detailed explanation:** The taxonomy breaks each top-level QA into measurable sub-attributes. For instance: Performance -> {Time behavior, Resource utilization, Capacity}. Reliability -> {Maturity, Availability, Fault tolerance, Recoverability}. Security -> {Confidentiality, Integrity, Non-repudiation, Accountability, Authenticity}. Maintainability -> {Modularity, Reusability, Analyzability, Modifiability, Testability}. The structure mirrors the QAi -> SubQAij -> Metricijk refinement pattern.
**Analogy:** Like the food pyramid for nutrition — nobody eats by literally consulting it during dinner, but it is the backstop ensuring you do not forget vitamins exist.
**Example:** A security review that only checks "is the password hashed" misses non-repudiation (audit logs), accountability (who did what), and authenticity (is the user actually who they claim). ISO/IEC 25010 forces all five sub-attributes into the conversation.
**Common pitfall / nuance:** Treating the taxonomy as exhaustive. It is a useful map, not the territory; specific domains will add their own QAs (e.g., energy efficiency for IoT).

### Big Ball of Mud (Antonym of QAs)
**Definition:** A system that lacks clear connectors between elements, promotes no single QA, and contains no considered tradeoffs (Fairbanks 2010).
**Why it matters:** It is the architectural failure mode that motivates the entire discipline. Even with all functional requirements met, the system is a maintenance nightmare and is often rewritten — not because it does the wrong thing, but because no one understands how it does anything.
**Detailed explanation:** Related concepts: *technical debt* (decisions today that will cost interest tomorrow), *legacy code* (often a euphemism for big ball of mud). The lecture emphasizes that systems are usually redesigned not because of broken functionality, but because of accumulated quality erosion.
**Analogy:** A house that was added to one room at a time over 40 years by different owners, with no plan: load-bearing walls cut, plumbing rerouted through closets, electrical panels in three different rooms. It "works" but no one dares touch anything.
**Common pitfall / nuance:** Believing that "agile = no architecture" produces clean systems. It produces mud unless someone is consciously preserving structural integrity.

### BDUF vs. Iteration 0 vs. Emergent
**Definition:** Three contrasting models for how much design effort to invest before iterative implementation begins. BDUF ("Big Design Up Front") frontloads almost everything; Iteration 0 frontloads a moderate skeleton then iterates; Emergent contributes near-zero upfront design and lets architecture grow from code.
**Why it matters:** The lecture argues that the BDUF/Emergent dichotomy is a false choice. Yang et al.'s (2016) systematic review found that Iteration 0 — a "skeleton design" or "big picture design" up front, then iterative refinement — best aligns architecture with agile.
**Detailed explanation:** Pure BDUF inhibits agility because architectural decisions freeze before market signal arrives. Pure Emergent collapses for non-trivial systems because architectural choices are the hardest to change later — once you have shipped a monolith to 50k users, refactoring to microservices is a years-long project. Iteration 0 is the pragmatic compromise: enough design to choose a deployment topology, integration boundaries, and ASR-driven structures; then build features iteratively.
**Analogy:** Building a house. BDUF = fully blueprinted before any concrete is poured. Emergent = "start nailing planks, see what we get." Iteration 0 = pour the foundation and frame the load-bearing walls; everything else can shift as you live in the house.
**Example:** The manufacturing automation example the lecturer keeps revisiting: nobody would seriously try to evolve a real-time control system for an industrial line from "we'll figure it out." But once the safety-critical skeleton is fixed, dashboards and analytics can be agile add-ons.
**Common pitfall / nuance:** Treating Iteration 0 as BDUF in disguise. It is *skeletal*, not *complete* — the right amount is "the minimum that lets the team make local choices without breaking the system."

### Risk = Probability x Impact
**Definition:** A quantitative formulation of risk as the product of how likely an undesirable event is and how much damage it would do; sometimes extended to Probability x Severity x Impact.
**Why it matters:** Risk-based reasoning is how architects (especially in security and safety domains) prioritize. You cannot defend everything equally; you defend in proportion to expected loss.
**Detailed explanation:** A risk lurks behind every QA, but the formulation is most explicit in cybersecurity and safety. The architect identifies hot spots (high probability x high impact) and designs them first, using known tactics and patterns rather than ad hoc inventions. The formula also exposes the fallacy of "but the impact would be catastrophic!" — if probability is negligible, the expected loss is too, and the risk can often be parked.
**Analogy:** Insurance pricing. Earthquake insurance in Tokyo is expensive (high prob x high impact); earthquake insurance in Helsinki is cheap (negligible prob).
**Example (from the lecture):** "Our on-premise data center on a mountaintop gets flooded." Probability: negligible. Severity: high. Impact: high. Conclusion: bypass the scenario. The numbers prevent you from wasting design effort on theatrical-but-implausible threats.
**Common pitfall / nuance:** Treating risks as purely negative. The lecture explicitly notes that risks can be positive — "our two-year startup project becomes a unicorn." A positive-risk-aware architecture might deliberately under-scale early (to ship fast) and accept that a full rewrite is the *plan* if success arrives.

### Cascading Risks and Defense in Depth
**Definition:** A cascading risk is one whose realization raises the probability (or impact) of subsequent risks; cascading impacts are the downstream damages those subsequent realizations cause. Defense in depth is the security principle of layering independent countermeasures so that no single failure cascades.
**Why it matters:** Real-world failures rarely have a single cause. A power failure crashes servers, which routes traffic to backups, which overloads them, which triggers throttling, which makes customers think the site is down and they hammer reload, which... Modeling these chains lets you place safeguards at multiple layers.
**Detailed explanation:** Modeling cascades formally requires conditional probability (P(Risk2 | Risk1 realized)). When the cascade compounds rather than fizzles, the system has tipped from a cascade into an *escalation*. The defense in depth answer is to insert layered, independent reducers — IDS, firewalls, network segmentation, hardening, exploit prevention — each lowering the probability of one link in the chain so the chain breaks.
**Analogy:** A castle. The moat reduces the probability attackers reach the wall; the wall reduces the probability they reach the keep; the keep's locked doors reduce the probability they reach the throne room. Any single layer can fail without the kingdom falling.
**Example:** A web app might have: a WAF (layer 1), rate limiting (layer 2), input validation (layer 3), parameterized SQL (layer 4), least-privilege DB user (layer 5), encrypted at-rest data (layer 6). An SQL-injection attempt must beat *all six*; the cascade is interrupted at every layer.
**Common pitfall / nuance:** Defenders sometimes layer *correlated* mechanisms (e.g., three different firewalls, all configured by the same admin with the same blind spot) — they look like depth but fail together.

### Quality Gates
**Definition:** Checkpoints throughout development at which a defined subset of ASRs/QAs must be passing.
**Why it matters:** They give project owners visibility — without halting agile flow. Unlike waterfall gates, they signal rather than block (except in catastrophic situations).
**Detailed explanation:** A typical QG table maps QAs to gates: e.g., at QG1, Performance/Throughput and Security/Availability are checked; at QG3, Confidentiality and Integrity are also enforced. Gates are most useful for large projects where the temptation to defer QA verification to "the end" is greatest.
**Analogy:** Routine doctor checkups during a long illness. You don't stop the treatment if a number is slightly off; you adjust. But persistent failure at multiple gates means something is structurally wrong.
**Example:** Sprints 1-3 must pass throughput gates; sprints 4-6 add latency gates; sprints 7-end add confidentiality and integrity gates. If throughput silently regresses at sprint 5, you catch it then, not at release.
**Common pitfall / nuance:** Quality gates with non-falsifiable QAs ("Security: pass/fail?") are theater. The QAs must be measurable for the gates to mean anything.

### Reference Architecture
**Definition:** A "guardrail" or "blueprint" architecture for a domain, technology, or standard, used as a reference for designing actual architectures.
**Why it matters:** It encodes domain expertise into reusable form, promotes best practices, facilitates interoperability between vendors, and conveys intent in standards/regulations.
**Detailed explanation:** Reference architectures are derived bidirectionally: bottom-up from existing architectures plus patterns/styles/tactics, and top-down from a domain, standard, or technology's ASRs. The result evolves through change triggers and is consumed by stakeholders/organizations to seed new concrete architectures. Cloud providers (AWS, Azure) publish reference architectures for "cloud-native ML platform," "secure VPC web app," etc., as both engineering and business artifacts (marketing the platform).
**Analogy:** IKEA assembly instructions for a class of furniture. The instructions are not the chair; they are the reference, allowing many factories to build many chairs that interoperate (same Allen key, same screw threads).
**Example:** CPython is the reference *architecture and implementation* for the Python interpreter. Other implementations (PyPy, Jython, MicroPython) must conform to its semantics; deviations are bugs or explicit dialects.
**Common pitfall / nuance:** The lecture poses this as an in-class question: a risk of reference architectures is *over-conformance* — every team builds the same blueprint, innovation dies, and weaknesses in the blueprint propagate across the whole industry. They can also become outdated more slowly than the technology they reference.

### Standards as ASR Carriers
**Definition:** Industry/government standards encode ASRs into binding form, often with backwards-compatibility commitments that propagate decisions for decades.
**Why it matters:** Designing against a standard means inheriting all of its QAs — and you cannot easily renegotiate them later.
**Detailed explanation:** The lecture cites IETF RFC 1958 ("Architectural Principles of the Internet") as a paradigmatic example. Its principles double as ASRs: heterogeneity must be supported (compatibility QA); designs must scale to many millions of sites (scalability QA); performance and cost must be considered (two QAs + a constraint); keep it simple (a QA of its own); modularity is good; prefer "almost complete now" over "perfect later"; avoid options (configurability is a tax); "be strict when sending and tolerant when receiving" (Postel's Law); discard faulty input silently. These principles still shape Internet protocol design 30+ years later.
**Analogy:** A constitutional amendment. Once ratified, every law that follows must respect it, regardless of how fashion changes. Standards bake ASRs into the architectural equivalent of constitutional law.
**Example:** TCP/IP's robustness principle (Postel's Law) is itself an ASR: implementations must accept malformed input without crashing. That ASR has shaped every networking stack since.
**Common pitfall / nuance:** Designing against an outdated standard because "we have to." Sometimes the right move is to deviate explicitly and document the deviation rather than inherit a 1996 assumption that no longer fits.

### Domain Modeling
**Definition:** The discipline of explicitly modeling the problem domain (its "enduring facts… not in our control") to inform architectural decisions, distinct from model-driven engineering's generative use of models.
**Why it matters:** A lot of software is built without explicit stakeholders (consumer products, COTS software). Even when stakeholders exist, "the architecture is *not* latent in the domain" — you cannot extract it by introspection. Modeling makes implicit domain assumptions visible.
**Detailed explanation:** Fairbanks (2010) proposes a layered chain: Domain model -> Boundary model -> Architecture model -> Design model -> Code model, with *designation* as the ideal (clean correspondence at each layer) and *refinement* as what actually happens in practice (messier, iterative). The architect provides multiple *views* of each model: concept views, snapshot views, scenario views, statistics, deployment views, component views, spanning views (cross-cutting concerns like security or QA tradeoffs).
**Analogy:** Cartography before exploration. You map the coastline (domain) before deciding where to build the harbor (architecture). The harbor design is *not* hidden in the coastline; the coastline only constrains what is possible.
**Example:** Modeling the airline-booking domain reveals enduring facts: aircraft have finite seats, time zones exist, fares are non-symmetric, passenger names are governmental identity, weather causes cancellation. These facts constrain — but do not determine — whether you build a monolithic reservation system or a microservices mesh.
**Common pitfall / nuance:** Fairbanks lists five common objections to modeling and rebuts each: "You already know your domain" (less true than you think, especially in "boring" domains); "Domain is too simple" (rarely); "Domain is irrelevant to architecture" (false — it influences architecture without determining it); "Someone else's job" (no); "Best way to learn is to write code" (sometimes, but often "overwhelmingly cost-effective to model on paper first"); "Analysis paralysis" (a real danger — model just enough). The right amount of modeling is *just enough* for ASRs and tradeoffs to become visible.

### Designation vs. Refinement
**Definition:** *Designation* is the ideal mapping where high-level model elements have clean correspondences to lower-level model elements. *Refinement* is the messier reality where lower layers expand, reinterpret, or partially deviate from the higher layer.
**Why it matters:** Knowing the difference keeps the architect honest. Pretending designation has happened when refinement has actually occurred hides drift between intent and reality.
**Analogy:** Translation between languages. Designation = perfect 1:1 word translation (rare). Refinement = the translator paraphrased, expanded idioms, dropped untranslatable bits — useful but lossy.
**Common pitfall / nuance:** Teams claim their architecture diagrams "match" the code when they actually refined past designation years ago. The fix is either to update the diagrams or to accept the refinement and document it.

### Non-Technical (Business) QAs
**Definition:** Quality attributes anchored in business outcomes rather than runtime behavior — e.g., time-to-market, total cost of ownership (TCO), market share, company reputation.
**Why it matters:** Business QAs can outweigh technical QAs. A technically gorgeous architecture that misses the market window is a failure.
**Detailed explanation:** Like technical QAs, business QAs should be measurable. They map onto the domain model alongside ASRs/QAs. AWS/Azure being "expensive" can still win on TCO if scalability is a business-critical QA, because the operations cost of building equivalent infrastructure in-house is higher. Technical debt has a direct business equivalent: an architecture that is hard to modify slows feature delivery, costing market share.
**Analogy:** A restaurant whose food is technically perfect but takes 90 minutes to serve will lose to a competitor with merely-good food served in 20. Time-to-market is the QA.
**Example:** A startup choosing Heroku over building a custom Kubernetes stack — Heroku is technically inferior on most QAs but vastly superior on time-to-market and operational TCO until ~50 employees.
**Common pitfall / nuance:** Architects who treat business QAs as "marketing's problem." They are *your* problem because they constrain technical choices.

### Deployment Modeling
**Definition:** Modeling how a system's components are placed onto machines, within internal environments, surrounded by external environments — the runtime view of architecture.
**Why it matters:** Many QAs (performance, availability, scalability, security) are only meaningful at runtime, so a static component diagram is insufficient. You need to know where things actually run.
**Detailed explanation:** The lecture's deployment metamodel: a *Deployment* contains one or more *Machines* (1..*); each Machine contains one or more *Components* (1..*); components *execute in* an internal Environment (OS, runtime, container); the system *operates in* an external Environment (datacenter, building, network, regulatory jurisdiction). Key questions then become: What machines run our components? How capable are they? How many are there? Where physically/legally? Answers vary wildly by domain — a mobile app and a cloud-native ML platform have nothing in common at this level.
**Analogy:** A restaurant menu (components) versus where the kitchens, suppliers, and delivery drivers actually are (deployment). A pizza chain with 500 locations is a deployment story, not a recipe story.
**Common pitfall / nuance:** Drawing only "logical" architecture diagrams. They look elegant but cannot answer "will it stay up during a regional outage" or "are we GDPR-compliant for European users." Deployment modeling is what makes those questions answerable.

### Software Bill of Materials (SBOM)
**Definition:** A systematic catalog of a system's primary (typically top-level) external dependencies — frameworks, libraries, containers, OS packages, ML models, data, cryptographic assets, firmware.
**Why it matters:** SBOMs are *mandated* by recent law in the EU (by 2027 under the Cyber Resilience Act) and in the US. Having an SBOM is now a mandatory ASR for many domains.
**Detailed explanation:** The lecture references the OWASP CycloneDX schema (v1.7), which classifies dependencies by type ({application, framework, library, container, platform, operating-system, device, device-driver, firmware, file, machine-learning-model, data, cryptographic-asset}) and tracks Supplier and Manufacturer metadata (bom-ref, name, address, url, contact). SBOMs make supply-chain risk visible: when CVE-2024-XXXX hits library Y, every system with Y in its SBOM can be located in minutes rather than weeks.
**Analogy:** A food ingredients label. You cannot prove a meal is peanut-free without knowing every ingredient; you cannot prove a system is vulnerability-free without knowing every dependency.
**Example:** The famous XKCD 2347 cartoon: a giant tower of "all modern digital infrastructure" balanced on a single tiny block labeled "a project some random person in Nebraska has been thanklessly maintaining since 2003." Without an SBOM, no one knows about the tiny block until it breaks.
**Common pitfall / nuance:** Cataloging only direct dependencies. Transitive dependencies (your library's libraries) are often where the vulnerabilities actually live. Modern SBOM tools traverse the full graph.
**Related diagram:** ![XKCD 2347 - Dependency](../images/lecture_2/lecture_2_p72_img1_xkcd_dependency.png)

### Falsifiable QA
**Definition:** A QA expressed such that it can be conclusively tested as either true or false (Fairbanks 2010).
**Why it matters:** It is the strongest form of measurability — not just "we can measure it" but "we can definitively pass or fail it."
**Detailed explanation:** Performance QAs are easily falsifiable ("throughput >= 100 tx/sec at peak"). Security QAs are usually only partially falsifiable ("passes the OWASP Top 10 scan" — yes/no, but absence of known attacks does not prove security). Usability QAs are hardest. The discipline still helps: a falsifiable usability QA ("a new student completes onboarding in under one hour") is much more useful than the woolly directive to "make it user-friendly."
**Analogy:** "Make a tall building" is unfalsifiable. "Building shall exceed 200 meters" is falsifiable with a tape measure.
**Common pitfall / nuance:** Insisting on falsifiability for QAs where it is impossible. Sometimes "measurable" is the best you can get; do not let perfect be the enemy of good.

## Important diagrams (catalog)

- `lecture_2_p72_img1_xkcd_dependency.png` — XKCD 2347 ("Dependency"): the iconic comic showing all modern digital infrastructure as a tower precariously balanced on one obscure unmaintained dependency. Cited by the lecture as the motivation for SBOMs.

*Note: Lecture 2 contains many useful conceptual figures (QA scenario template, ISO/IEC 25010 trees, risk cascades, defense-in-depth model, domain modeling chain, deployment metamodel, CycloneDX schema), but these are vector-drawn directly in the PDF (not embedded as raster images), so they are described in prose within the relevant Concept sections above rather than included as image files. The SDU logo on page 1 was extracted but discarded as decorative.*

## Exam-relevant takeaways

- A QA is "a measurable or testable property… beyond the basic function" — memorize the Bass et al. definition verbatim.
- ISO/IEC 25010 has eight top-level QA categories: functional suitability, performance, compatibility, usability, reliability, security, maintainability, portability. Know at least one sub-attribute per category.
- The QA scenario template has six slots: Source, Stimulus/Event, Environment, Artifact/Deployment, Response, Response Measure. Be able to fill all six for a given QA.
- Risk = Probability x Impact (sometimes also x Severity). Negligible probability often justifies skipping otherwise scary scenarios. Risks can be positive too.
- Defense in depth answers cascading risk by inserting *independent* layered reducers; correlated layers don't count.
- BDUF and pure Emergent both fail for non-trivial systems; Iteration 0 (skeleton design + iterative refinement) is the pragmatic agile-compatible choice.
- ASRs are "sniffed" from requirement documents by looking for named technologies/vendors, integration points, deployment hints, data volumes, networking constraints, scale/i18n expectations, compliance regimes.
- Quality gates are *signals*, not stop-the-line authority, and require falsifiable QAs to be meaningful.
- Reference architectures encode domain expertise but risk over-conformance and slow obsolescence; CPython is the canonical example.
- IETF RFC 1958's ten principles are ASRs of the Internet (heterogeneity, scalability, simplicity, modularity, Postel's robustness principle, etc.).
- Domain modeling layers: Domain -> Boundary -> Architecture -> Design -> Code; designation is the ideal, refinement is the reality.
- SBOM (CycloneDX schema) becomes a legally mandatory ASR in the EU by 2027; it catalogs typed external dependencies including ML models and cryptographic assets.
- Falsifiability is stronger than measurability; aim for it where possible.
- Business QAs (time-to-market, TCO) can outweigh technical QAs and must also be measurable.

## Cross-references

- Likely connects to Lecture 1: foundational definitions of "architecture" vs. "detailed design," diagrams as syntactic/semantic artifacts, and the manufacturing automation case study that recurs here.
- Likely connects to later lectures on **performance** and **scalability** — explicitly flagged on page 68 ("deployment diagrams are discussed in more detail" when those QAs are addressed).
- Likely connects to later lectures on **safety and security** — risk-based reasoning, cascading risks, and defense in depth are introduced here as foundational.
- Likely connects to later lectures on **maintainability** — SBOMs, modifiability, and the "components in/out of our control" distinction motivate later maintenance discussions.
- Likely connects to a lecture on **architecture evaluation** — quality gates and ASRs naturally lead to ATAM-style evaluation methods.
- Likely connects to lectures on **patterns and tactics** — Fairbanks's advice to "reduce risk with known tactics and patterns instead of rolling your own" foreshadows pattern catalogs.
