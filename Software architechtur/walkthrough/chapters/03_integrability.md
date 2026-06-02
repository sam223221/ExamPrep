# Chapter 3 — Integrability

> *"Integrability is what happens when somebody else's code has to live inside your system, or yours inside theirs."*

## Opening: why integrability is its own quality attribute

Most non-trivial software today is **mostly other people's code**. Your service imports `express`, which pulls in `body-parser`, which pulls in `qs`. Your IoT gateway speaks MQTT to thermostats from three vendors. Your microservice writes logs that an aggregator scrapes and forwards to Elasticsearch. The interesting engineering question is no longer "does our code work in isolation?" but **"how well does our system absorb, swap and wire together components we don't fully control?"** That question is what *integrability* names.

Bass et al. treat integrability as a first-class quality attribute (QA), parallel to modifiability, testability, security and the rest. It has its own scenario template, its own tactics tree, and its own metric — **σ = size × distance** — that we will return to repeatedly in this chapter. The lecturer (Jukka Ruohonen) introduced integrability *before* modifiability not by accident: integrability is the cleanest entry point into the QA-tactics-patterns hierarchy, because almost every concrete design move it suggests (encapsulate, discover, orchestrate, bridge…) reappears later in modifiability, testability and security with only minor variation. Master the integrability tree and you have the visual grammar for the rest of the book.

We start with two definitional ground rules: the **tactic vs pattern** distinction (so the rest of the chapter can refer to either without ambiguity), and the **dependency taxonomy** (because integrability is *defined* in terms of dependencies). From there we build up the **σ metric**, fill out the **6-slot integrability scenario**, draw the **Limit / Adapt / Coordinate tactics tree** — the first tactics tree in the book and the layout convention for every tree to follow — and then walk through the concrete patterns that realise those tactics: **Observer vs Publish-Subscribe**, **Wrapper vs Bridge vs Mediator**, **service discovery**, **OWASP logging**, and **orchestration**. The final concept — orchestration — is also where we meet our first anti-pattern, the **god class**, because every centralising tactic carries the seed of its own anti-pattern.

A note on naming: this course follows Bass et al.'s vocabulary. Fairbanks calls tactics *styles*. If you slip into Fairbanks's "styles" in an exam answer expect a margin note, no more — but be consistent.

![Refining the basic concepts: in-house vs external components on the control / knowledge axis](../images/lecture_3/lecture_3_p08_img1_refining_basic_concepts.png)

The figure above frames the chapter. The horizontal axis is **how much control** you have over a component (you wrote it ↔ someone else did). The vertical axis is **how much you know** about it (full source ↔ black box). Integrability concerns itself most with the top-right quadrant — components you don't control and may not fully understand — because *that* is where σ blows up.

---

## Concept 1 — Tactics vs Patterns (Bass vs Fairbanks)

**Definition.** A **tactic** is a high-level, fairly abstract design choice aimed at one quality attribute. A **pattern** is a smaller, more concrete, reusable design that realises one or more tactics.

**Why it matters.** The vocabulary is not universal — Fairbanks calls tactics "styles" — but inside this course Bass et al.'s usage is the reference, and exam answers must use it consistently.

**Detailed explanation.** Think of tactics as *intentions* ("encapsulate the dependency", "defer the binding to runtime"), while patterns are *blueprints* (Observer, Publish-Subscribe, Wrapper, Bridge, MVC). A single tactic typically has several patterns realising it; conversely the same pattern can serve multiple tactics for different QAs. The Observer pattern, for instance, realises the *encapsulate* tactic (for integrability) and the *reduce-coupling* tactic (for modifiability) simultaneously.

**Analogy.** A tactic is a coach saying *"press high up the pitch"*; a pattern is the *4-3-3 formation* the team actually lines up in. The instruction is the tactic; the diagram on the whiteboard is the pattern.

**Example.** The *encapsulate* tactic is realised by the *Wrapper* pattern — one specific module hides another behind a narrower interface. Same intention, concrete realisation.

**Common pitfall / nuance.** Students mix the two terms freely. On the exam keep tactics abstract ("we should reduce coupling") and patterns concrete ("by introducing a Publish-Subscribe broker").

---

## Concept 2 — Dependencies as the unit of analysis

**Definition.** A **dependency** is any relation between two software elements such that one cannot fulfil its purpose without the other.

**Why it matters.** Integrability is *defined* in terms of counting and weighting dependencies; you cannot measure or improve it until you can name them.

**Detailed explanation.** Latendresse et al. (2022) classify dependencies along two axes — **when** they bite and **how deep** they go:

- **When (lifecycle phase):** *run-time* (loaded into the running process), *development-time* (test frameworks, type checkers, formatters), *install-time* (compiled into the build artefact but never imported at run).
- **Depth (tree position):** *direct* (you wrote its name in `package.json`) or *transitive* (it was pulled in by something else, anywhere from depth 2 down). Anything below the first level is transitive — you didn't pick it but you carry it.

Bass et al. add a **type** axis:

- *Syntactic dependency* — a call, an inheritance edge, an implemented interface. Tooling can detect these.
- *Semantic dependency* — a shared protocol, file format, or meta-data convention. Tooling generally cannot.

And on top of those, two components can also be coupled:

- *Temporally* — they must agree on time/order ("the auth service must start before the gateway").
- *By shared resources* — CPU, RAM, disk, file handles, network bandwidth.

**Analogy.** A dependency tree is a Russian doll. The outermost doll is *your* code; one level in is a direct dependency; everything nested inside is transitive — you didn't pick it, but you carry it everywhere it goes.

**Example.** Your Node.js project lists `express` (direct, run-time, depth 1). `express` itself pulls in `body-parser`, which pulls in `qs` — both transitive, both still loaded in production, both able to crash your server with the same blast radius as your own code.

**Common pitfall / nuance.** "Dev dependency" doesn't mean "harmless". A compromised test framework can inject a supply-chain attack at build time that ships into production. The `event-stream` incident (2018) is the textbook case.

---

## Concept 3 — Size × Distance: the σ metric

**Definition.** Bass et al. evaluate each component *C* in a system *S* by **size** (number of potential dependencies between *C*'s interfaces and the rest of *S*) and **distance** (how hard it is to *resolve* each dependency). **σ = Σ Cᵢ** sums size across all components — the only quantitative handle the textbook offers for integrability.

**Why it matters.** Expect a slide-style question asking you to recite *size*, *distance*, and the **five distance sub-dimensions**. The instructor wrote them out explicitly; they are near-guaranteed exam material.

**Detailed explanation.** Size is mostly objective: count the public methods, count the interfaces, count the message types. Distance is subjective and decomposes into **five sub-distances**:

1. **Syntactic distance** — agreement on data *shape* (XML vs JSON, `int` vs `float`, big-endian vs little-endian, snake_case vs camelCase).
2. **Data-semantic distance** — agreement on the *meaning* of the data (seconds vs nanoseconds, km vs miles, Celsius vs Kelvin, UTC vs local time).
3. **Behavioural-semantic distance** — agreement on *protocol and state* (who initiates the handshake, three-way vs four-way teardown, client vs server roles, REST vs RPC semantics).
4. **Temporal distance** — agreement on *timing* (10 Hz vs 100 Hz publish rate, 10 ms vs 100 ms acceptable latency, request-response vs fire-and-forget).
5. **Resource distance** — agreement on shared *resources* (memory budgets, CPU cores, disk quotas, bandwidth allotments).

**Analogy.** Plugging an appliance into a foreign wall socket. *Size* = how many prongs the plug has. *Syntactic distance* = "do the prong shapes match?" *Data-semantic* = "is 230 V the same number my appliance reads as 230 V?" *Behavioural* = "does the outlet expect a switch flip before delivering power?" *Temporal* = "50 Hz vs 60 Hz?" *Resource* = "is enough amperage available?"

**Example — the Mars Climate Orbiter (1999).** NASA's spacecraft disintegrated on entry because its on-board software spoke **newton-seconds** while the ground software at Lockheed Martin sent **pound-seconds**. The JSON wire format (or its 1990s equivalent) was a perfect *syntactic* match — both sides agreed numbers were numbers. The integration failed on **data-semantic distance**: same shape, different units, $327 million spacecraft lost. It is the canonical reason "interface compatibility" is *not* the same as "integration works".

**Common pitfall / nuance.** Two components passing the same JSON schema can still have *huge* semantic distance. Never declare integrability solved by interface matching alone. Conversely, two systems with completely different syntactic shapes (XML ↔ Protobuf) but identical semantics can be glued together cheaply with a bridge.

---

## Concept 4 — The integrability scenario template (6 slots)

**Definition.** A six-slot template — *source, event/stimulus, environment, system part, response, response measure* — used to elicit concrete, testable integrability requirements.

**Why it matters.** It turns vague "should be integrable" requirements into something you can verify. Bass-style 6-slot scenarios are a recurring exam format across *every* QA chapter, so internalising the structure here pays compound interest later.

**Detailed explanation.** Each slot maps to a question:

| Slot | Question | Typical answers |
|---|---|---|
| **Source** | Where does the change request originate? | Vendor, internal stakeholder, marketplace, regulator |
| **Event / stimulus** | What does it ask for? | Add a new component; integrate a new version; integrate in a new way |
| **Environment** | In what lifecycle phase? | Development, integration, deployment, production |
| **System part** | Against which part of the system? | Entire system, set of components, meta-data, configuration |
| **Response** | How should the system behave? | Change completed / integrated / tested / deployed; configuration honours all existing guarantees |
| **Response measure** | How do we *measure* success? | Components changed, % code changed, tests pass/fail, money, time, downtime |

**Analogy.** Like a press-release template before launching a product: it forces the team to write the headline, audience, key benefit and success metric *before* coding.

**Example.** "When a **vendor** *(source)* releases **new sensor firmware** *(event)* during **production** *(environment)*, the **sensor adapter component** *(system part)* shall be **deployed without disrupting data collection** *(response)*, with **zero dropped readings over a 24-hour window** *(measure)*."

**Common pitfall / nuance.** Skipping the *response measure* slot produces unfalsifiable requirements ("the system shall be integrable"). Always write a number, or a yes/no condition that can be observed.

![The six-slot integrability scenario template populated with example values](../images/lecture_3/lecture_3_p16_img1_integrability_scenario_template.png)

---

## Concept 5 — The Limit / Adapt / Coordinate tactics tree

**Definition.** Bass et al.'s three-branch tactic tree:

- **Limit** the number/strength of dependencies in the first place.
- **Adapt** to differences between components you can't change.
- **Coordinate** the activities of components at runtime.

**Why it matters.** Almost every concrete integrability move maps cleanly to one of three branches. Memorising the tree gives you a structured way to answer the open-ended exam question "what tactics would you apply?" — you walk the three branches in order and read off candidates.

**Detailed explanation.** This is **the anchor diagram of the chapter** and the first tactics tree in the book. The visual convention used here — root QA on the left, branches fanning right, leaves as named sub-tactics — is the convention used by every subsequent tactics tree (modifiability, testability, availability, security…). Learn to redraw it from memory.

```
                                    ┌─ avoid
                                    │   (don't introduce the dependency)
                                    │
                       ┌── Limit ───┼─ bundle
                       │            │   (copy the dep into your tree — Russ Cox 2019)
                       │            │
                       │            └─ encapsulate
                       │                ├─ isolate
                       │                ├─ abstract
                       │                └─ use standards
                       │
                       │            ┌─ discover
                       │            │   (DNS, DHCP, Consul, K8s Services)
                       │            │
   Integrability ──────┼── Adapt ───┼─ tailor interface
                       │            │   (add / remove capabilities — wrapper, bridge)
                       │            │
                       │            └─ configure behaviour
                       │                ├─ build-time flags
                       │                ├─ start-up config
                       │                └─ runtime parameters
                       │
                       │            ┌─ orchestrate
                       │            │   (centralised conductor — Kubernetes, Airflow)
                       └── Coordinate ┤
                                    └─ manage resources
                                        (thread pools, quotas, rate limiters)
```

- **Limit** = reduce the number or strength of dependencies → *avoid* (the strongest move: don't add the dep at all), *bundle* (vendor a copy into your tree, the Russ Cox 2019 argument), *encapsulate* (isolate, abstract, or use a standard so the dep is replaceable).
- **Adapt** = bridge differences without changing the components themselves → *discover* (service discovery), *tailor* the interface (add or remove capabilities — typically via a wrapper or bridge), *configure* behaviour (via build, start-up or runtime flags).
- **Coordinate** = manage interactions among components → *orchestrate* (a centralised conductor decides what runs where and when), *manage resources* (thread pools, connection pools, rate limiters, quota arbiters).

**Analogy.** Hosting a dinner party. *Limit* = invite fewer people, or make sure the loud cousin sits in another room. *Adapt* = put labels on dishes for the vegan guest, translate the menu into the visitor's language. *Coordinate* = a host who decides who speaks when and serves the wine in turn.

**Example.** Bundling `lodash` directly into your repo (limit/bundle) ↔ publishing a discovery endpoint that lists active microservices (adapt/discover) ↔ running Kubernetes (coordinate/orchestrate). One real-world system typically combines moves from all three branches.

**Common pitfall / nuance.** The branches *overlap*. Using a standard is a Limit/encapsulate tactic but it also avoids Adapt work later. Tactics combine, they don't compete; exam answers should reach for *several* branches when defending a design.

![The full Limit / Adapt / Coordinate integrability tactics tree — anchor figure of the chapter](../images/lecture_3/lecture_3_p18_img1_integrability_tactics_tree.png)

---

## Concept 6 — Bundling vs package management

**Definition.** *Bundling* means copying a dependency directly into your repository's tree. *Package management* means listing the dependency as a manifest entry and letting a tool resolve and download it from a registry.

**Why it matters.** Russ Cox (2019) argues bundling is often the safer default for high-trust contexts; package managers expose you to supply-chain attacks (typosquatting, fake stars, malicious updates injected mid-stream).

**Detailed explanation.** Bundling trades reproducibility-and-isolation for storage and update-friction. Package management trades convenience for *trust in the registry*. Two refinements split the difference:

- **Pinned dependencies** — lock to a version identified by a cryptographic hash, not just a version string. `npm`'s `package-lock.json`, `pip`'s `--hash`, `cargo`'s `Cargo.lock`, Go modules' `go.sum` all implement this. A pinned dep is a managed dep that *can't be silently swapped*.
- **OpenSSF Scorecard** — an automated audit (known vulnerabilities, code reviews on commits, signed releases, branch protection rules, …) you run against an open-source package before adopting it. Gives a grade you can record in design review.

**Analogy.** Bundling = freezing your own meals at home. Package manager = ordering takeout — fast and convenient, but you must trust the kitchen.

**Example.** Go's `vendor/` directory bundles dependencies into the repo (Cox's home turf). `npm`'s `package-lock.json` with integrity hashes is closer to *pinning*.

**Common pitfall / nuance.** "Many GitHub stars" ≠ "trustworthy". The CMU 2026 ICSE paper on **fake GitHub stars** (cited in the lecture) shows star counts can be cheaply gamed by paid services; signed releases and verified maintainers are stronger signals.

---

## Concept 7 — Observer vs Publish-Subscribe

This is the **highest-yield comparison in the integrability chapter**. The lecturer drew a six-row table specifically for it. The exam can reasonably ask for *any* of the six rows.

**Definition.**

- **Observer** is a *module-level* pattern. A *subject* keeps direct references to its *observer* instances and calls `update()` on each when something changes.
- **Publish-Subscribe** is a *distributed* pattern. Publishers and subscribers communicate through an intermediary *broker* (event bus), unaware of each other.

**Why it matters.** They look near-identical in textbook diagrams — "one thing notifies many things" — but they have **opposite coupling, latency and failure profiles**. Conflating them is the most common Observer/Pub-Sub mistake in design reviews and on exams.

**Detailed explanation.** Observer is *tight*: the subject holds direct references, so adding an observer means *attaching* to the subject. Latency is low (often a direct synchronous method call), failure of an observer can propagate back into the subject, and it lives in GUI/MVC code where you control all parties.

Publish-Subscribe is *loose*: publishers and subscribers don't know about each other; the broker dispatches messages asynchronously. Latency is higher (broker overhead, queueing), fault tolerance is better (broker isolates publisher failures from subscriber failures), but determinism, end-to-end encryption, testability and delivery guarantees suffer because **nothing knows the full route**.

![Publish-Subscribe pattern with publishers and subscribers decoupled through a broker](../images/lecture_3/lecture_3_p26_img1_publish_subscribe_pattern.png)

**The canonical six-row comparison table — reproduce exactly.**

| Aspect | Observer | Publish-Subscribe |
|---|---|---|
| **Latency** | Low (direct call). | Higher (broker hop, queueing, async dispatch). |
| **Logging** | Trivial — subject sees every notification. | Harder — needs broker-side logging; no single party sees the full route. |
| **Coupling** | Tight — subject holds direct references to observers. | Loose — publishers and subscribers don't know each other. |
| **Communication** | Direct, usually synchronous. | Indirect, through broker; typically asynchronous. |
| **Fault tolerance** | Low — a failing observer can propagate failure to the subject. | Higher — broker isolates publisher and subscriber failures. |
| **Domain** | GUI / MVC / in-process event handling. | Microservices, IoT (MQTT), distributed systems. |

![Observer vs Publish-Subscribe — the six-row comparison table](../images/lecture_3/lecture_3_p29_img1_observer_vs_pubsub_table.png)

**Analogy.** Observer is a teacher with a class roster — when something changes she calls each named student in turn. Publish-Subscribe is a radio station — anyone tuned in hears the broadcast; the DJ doesn't know who's listening.

**Example.** Observer = a Java Swing button firing `ActionEvent` to registered `ActionListener`s. Publish-Subscribe = Apache Kafka over TCP for a transactional event log, or MQTT for an IoT swarm of temperature sensors reporting to a backend.

**Common pitfall / nuance — the noisy publisher.** A typical broker has **no global scheduler**. One publisher flooding the bus can starve other subscribers because the broker dispatches as fast as it can in arrival order. The lecturer's slide 28 illustrates this exactly: a misbehaving sensor that decides to publish at 10 kHz instead of 10 Hz can knock out a whole pipeline that was provisioned for the lower rate. There is no "fair queueing" guarantee unless you add one explicitly (rate limiting at the publisher, per-publisher quotas at the broker, or topic-level back-pressure). **Expect this gotcha on the exam** — it's the most lecturer-flagged piece of integrability nuance in the deck.

---

## Concept 8 — OWASP logging for microservices (encapsulation in practice)

**Definition.** An OWASP-recommended logging architecture: each service writes locally through a logging library; log aggregators periodically pull and forward via a message broker to isolated permanent storage.

**Why it matters.** It's a small case study in **stacking integrability tactics**. You will see this exact shape again in the security chapter (SIEM) and the deployability chapter (observability).

**Detailed explanation.** Three tactics combine in one architecture:

- **Encapsulation (Limit branch)** — services log only through the library; storage is hidden.
- **Publish-Subscribe (Adapt-ish, but mostly a pattern realising the broker tactic)** — aggregators publish to a broker that fans out to storage shards.
- **Manage resources (Coordinate branch)** — aggregators publish at a low frequency to bound bandwidth, instead of every log line being shipped synchronously.

The lecturer's deliberate-mismatch exercise was this: the slide *itself* contains an inconsistency — one container writes to disk while another publishes directly via the broker, mixing semantics. Real designs often produce small mismatches like this when tactics are combined under deadline pressure. Spotting them is part of the skill.

**Analogy.** A hospital with each ward keeping its own paper log (local file), a clerk visiting periodically (aggregator), and a central archive behind a single locked door (permanent storage).

**Example.** The ELK stack (Elasticsearch + Logstash + Kibana) with Fluentd shippers, or Loki + Promtail, mirrors this exact shape. So does the OpenTelemetry collector pattern.

**Common pitfall / nuance.** Direct writes from a service to permanent storage skip the encapsulation layer entirely. It works *today*, but on the day you want to swap Elasticsearch for ClickHouse every service has to be redeployed instead of just the aggregators.

![OWASP logging architecture for microservices — encapsulation + broker + isolated storage](../images/lecture_3/lecture_3_p31_img1_logging_microservices_design.png)

> **Exercise (as posed in the lecture).** Look at the figure above and identify the inconsistency. *(Hint: not every service is talking to the same layer; one is talking past the aggregator.)*

---

## Concept 9 — Wrapper vs Bridge vs Mediator

Three encapsulation patterns that look the same at first glance and differ in **scope** and **binding time**. Exam classics.

**Definition.**

- **Wrapper** — module-specific; exposes fewer interfaces than the wrapped module; routes all calls to the wrapped module. Binding to the wrapped module is hard-coded.
- **Bridge** — more general; *translates* the "required" assumptions of one component into the "provided" assumptions of another; the translation table is fixed at design or build time.
- **Mediator** — like a bridge, but determines the "required" assumptions **at runtime**.

**Why it matters.** They are very easy to confuse on the exam. The two differentiators are:
1. **Generality**: wrapper is module-bound; bridge and mediator are general.
2. **Binding time**: wrapper and bridge resolve at build/design time; mediator resolves at runtime.

**Detailed explanation.** A *wrapper* is bound to its target module — you write `LoggingFileWrapper` around `java.io.File` and that wrapper exists for `File` only. A *bridge* is independent of either side — a PCI bridge connects any host bus to any PCI device using a published translation table. A *mediator* centralises *runtime* coordination — `object_1` asks the mediator for `object_2`'s current state instead of holding a reference; the mediator decides each request individually.

The **god-class anti-pattern** lurks specifically inside the mediator slot. When the mediator grows to know about every object in the system and decide every interaction, it becomes a single point of change, failure and review bottleneck. We will meet this risk again under orchestration.

**Analogy.**
- *Wrapper* = a translator who only ever interprets between English and your one specific cousin from Mexico.
- *Bridge* = a phonebook converter that translates area codes between *any* two countries using a published table.
- *Mediator* = a live operator who, when you call, decides on the fly whom to connect you to.

**Example.**
- *Wrapper*: `java.io.BufferedReader` around a `Reader`.
- *Bridge*: a RESTful gateway that translates mobile-client requests into backend microservice calls (slide 43 in the lecture deck).
- *Mediator*: a chat-room server that, when a message arrives, decides at message time who else is currently in the room and routes accordingly.

**Common pitfall / nuance.** *Wrappers don't translate; they restrict and route.* If your design says "the wrapper converts XML to JSON", you actually have a bridge — call it that.

---

## Concept 10 — Service discovery (the canonical Adapt → Discover tactic)

**Definition.** An architectural pattern where clients learn the address and/or capabilities of services **dynamically**, rather than via hard-coded references.

**Why it matters.** It is the canonical realisation of the *Adapt → Discover* tactic and the foundation of every cloud-native system. If "where is service X?" has a static answer in your design, you have no discovery; if the answer is "ask the registry", you do.

**Detailed explanation.** Three layers of classical examples build the intuition:

- **DNS** — *name → address.* `api.example.com` resolves to whatever IP currently hosts the API. The client doesn't care which.
- **DHCP** — *host → network configuration.* A new device on the LAN gets its IP and gateway without manual setup. The four-step handshake is **D-O-R-A**: *Discover* (client broadcasts), *Offer* (server proposes a config), *Request* (client accepts), *Acknowledge* (server confirms).
- **Microservice registries (Consul, etcd, Kubernetes Services)** — the same idea pushed inside the data centre. A new pod registers itself; downstream services find it via a virtual service IP that the registry maintains, not a hard-coded one.

**Analogy.** Walking into a hotel lobby and asking the concierge where the gym is, instead of memorising every floor plan in advance. The hotel can renovate the gym to a new floor and the concierge will simply tell the next guest the new location.

**Example.** A new Kubernetes pod starts up, registers itself in the kube-apiserver, and gets endpoint records attached to its Service. Downstream pods resolve `payments.svc.cluster.local`, get a virtual IP, and the kube-proxy load-balances to a live pod — without anyone shipping a config change.

**Common pitfall / nuance.** Discovery solves *location coupling* but adds a **new dependency on the registry**. If the registry dies, nothing finds anything. The fix is to either replicate the registry (Consul's Raft consensus, etcd's Raft consensus, DNS's hierarchical authority model) or to cache locally with a TTL so short outages are absorbed.

---

## Concept 11 — Orchestration (and its god-class danger)

**Definition.** A *Coordinate* branch tactic that **centralises decisions** about *what runs where and when* in a dedicated component — the **orchestrator**.

**Why it matters.** Orchestration is the model behind Kubernetes, Airflow, Nomad, and most container platforms. The trade-off it introduces — central coordination at the cost of central risk — is one of the chapter's headline lessons.

**Detailed explanation.** The orchestrator stacks three sub-tactics from the tree: service discovery + configuration + resource management. The flow on slide 37 of the lecture goes:

1. An **event** arrives at the orchestrator (e.g. "schedule this job").
2. The orchestrator consults **service discovery** to enumerate available executors.
3. It reads **meta-data** (resource requests, affinity rules, taints, tolerations).
4. It **provisions resources** on a chosen machine.
5. It **forwards data** (the actual workload) to that machine.

Meta-data drives every step. Slide 39 shows an example record:

```json
{ "tag": "(a)", "id": "machine_2", "cpus": "4", "ram": "16GB", "ram_min": "8GB" }
```

Read aloud: *"there is a machine tagged (a), id `machine_2`, with 4 CPUs and 16 GB of RAM available, requiring at least 8 GB to host this kind of workload."* The orchestrator joins this with the workload's own meta-data ("I need 2 CPUs and 4 GB minimum") to pick a fit.

**Analogy.** An air-traffic control tower. Pilots could in principle radio each other, but the tower centralises sequencing — at the cost of being a *single point of failure*. Lose the tower and the airspace becomes uncoordinated.

**Example.** Kubernetes' scheduler picks nodes for new pods based on resource requests, node capacity, taints/tolerations and affinity rules. The exact pattern as slide 37, just at industrial scale.

**Common pitfall / nuance — the god class.** Pushing too much logic into the orchestrator yields the *god-class anti-pattern*: every change in the system ripples through the orchestrator, every failure investigation starts at the orchestrator, every feature lands as a new orchestrator flag. The same risk we flagged for the *mediator* pattern in Concept 9 — the difference is that orchestration applies it to the whole system instead of one interaction point. Mitigations: keep the orchestrator's vocabulary small (meta-data + resource requests, *not* business logic), push policy decisions to plug-ins/operators, and treat the orchestrator's config surface as a public API governed by semver.

---

## Takeaways

By the end of this chapter you should be able to do the following from memory:

1. **Use Bass's vocabulary precisely.** *Tactics* are abstract intentions; *patterns* are concrete designs. Fairbanks's "styles" mean the same thing — but in this course use Bass.
2. **Classify a dependency** along three axes: *when* (run-time / dev / install), *depth* (direct / transitive), *type* (syntactic / semantic) — plus temporal and shared-resource coupling.
3. **Compute σ = Σ size** and list the **five distance sub-axes**: *syntactic, data-semantic, behavioural-semantic, temporal, resource* — with one example each. The Mars Climate Orbiter is the canonical *data-semantic* failure.
4. **Fill a six-slot integrability scenario** (source / event / environment / system part / response / response measure). Always include a measurable number in the last slot.
5. **Draw the Limit / Adapt / Coordinate tactics tree** with at least two sub-tactics per branch. *Limit*: avoid, bundle, encapsulate. *Adapt*: discover, tailor, configure. *Coordinate*: orchestrate, manage resources.
6. **Compare Observer to Publish-Subscribe** across the six rows: *latency, logging, coupling, communication, fault tolerance, domain.* The "noisy publisher" gotcha (no global scheduler at the broker) is a likely exam item.
7. **Distinguish Wrapper / Bridge / Mediator** by *generality* and *binding time.* Wrapper restricts and routes; bridge translates; mediator translates *at runtime*.
8. **Explain service discovery** as the canonical Adapt → Discover tactic, naming DNS, DHCP (with D-O-R-A) and Consul/Kubernetes Services as the three lineage levels.
9. **Recognise the god-class anti-pattern** as the price of centralising coordination — equally present in over-grown mediators and over-grown orchestrators.

Two cross-references worth carrying forward:

- The *encapsulate* and *dependency-reduction* tactics here are reused near-verbatim in Chapter 4 (Modifiability) and Chapter 5 (Testability) — internalise them once now.
- The *broker* pattern reappears in Chapter 10 (Security) as the spine of a SIEM, and the *orchestration* discussion threads into Chapter 9 (Kubernetes is orchestration at industrial scale).

> **One-line summary.** Integrability is **σ = size × distance** — and tactics live on three branches: **Limit** the dependencies you have, **Adapt** to the ones you can't avoid, and **Coordinate** the ones you keep.
