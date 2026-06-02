# Chapter 13 — Pattern + Tactic Reference

> **How to use this chapter.** Don't read it linearly. During revision: jump to **Part A** when you need the tactics tree for a QA, jump to **Part B** when you remember a pattern name but not the QA it belongs to. Each entry is one line; every entry points back to its canonical home chapter.

---

## Part A — Cross-QA Tactics-Tree Comparison

### A.1 The mega-table

One row per top-level branch slot. Cells contain the named sub-tactics. Empty cells (—) mean that QA does not use that slot in its canonical tree.

| Slot \ QA | **Integrability** (Ch 3) | **Modifiability** (Ch 4) | **Testability** (Ch 5) | **Deployability** (Ch 6) | **Availability** (Ch 7) | **Performance** (Ch 8) | **Safety** (Ch 10) | **Security** (Ch 10-11) | **Scalability** (Ch 9) | **Usability** (Ch 12) |
|---|---|---|---|---|---|---|---|---|---|---|
| **Branch 1** | **Limit dependencies** — avoid, bundle, encapsulate | **Reduce coupling** — split, combine, encapsulate, intermediary, restrict | **Control & observe input/state** — input gen, record/play, special interfaces, localised storage, assertions | **Manage pipeline** — separate builds, canary, scripted deploy, rollback | **Detect faults** — ping/echo, monitor, heartbeat, timestamp, sanity check, condition monitor, voting, exception detection, self-test | **Control demand** — manage work requests, limit event response, prioritize, reduce overhead, bound execution times, increase efficiency | **Avoidance** — substitution, simplification, predictive model | **Detect** — intrusion detection, anomaly detection, integrity check, verify msg, denial-of-service detection | (Bondi) **Load** | (sub-QA) **Discoverability** |
| **Branch 2** | **Adapt** — discover, tailor (translate / transform), configure behavior | **Increase cohesion** — split modules by responsibility, redistribute responsibilities | **Limit complexity** — limit structural / non-determinism, sandboxes, abstract data sources | **Manage deployment** — multi-version, feature toggle, rollback live, secure defaults, blue/green, A/B | **Repair (Recover)** — active redundancy, passive redundancy, spare, exception handling, retry, ignore faulty behaviour, degradation, reconfiguration | **Manage resources** — increase resources, increase concurrency, maintain copies (cache / replicate), bound queue sizes, schedule resources | **Detection** — sanity check, condition monitoring, timeout/watchdog, voting | **Resist** — identify actors, authenticate, authorise, limit access, limit exposure, encrypt, separate entities, validate input, change defaults | **Space** | **Learnability** |
| **Branch 3** | **Coordinate** — orchestrate, manage resources | **Defer binding** — compile, build, deploy, startup, runtime | — | — | **Reintroduce (after repair)** — shadow, state resynchronisation, escalating restart, non-stop forwarding | — | **Containment** — redundancy, limit impact (firewall / barrier), abort | **React** — revoke access, lock computer, inform actors | **Space-time** | **Operability / Efficiency** |
| **Branch 4** | — | — | — | — | **Prevent faults** — removal from service, transactions, predictive model, increase competence set, exception prevention, retry policy, isolate faulty parts | — | **Recovery** — fail-safe, graceful degradation, repair, reconfigure | **Recover** — restore (audit + restore from Ch 7) | **Distance** | **Understandability** |
| **Branch 5** | — | — | — | — | — | — | — | — | **Speed-distance / Structural** | **Flexibility** |
| **Signature mnemonic** | **L-A-C** | **R-I-D** (Reduce / Increase / Defer) | **C-L** (Control / Limit) | **P-D** (Pipeline / Deployment) | **D-R-R-P** | **C-M** (demand / resources) | **A-D-C-R** | **D-R-R-R** | **6 Bondi axes** | **6 sub-QAs** |
| **Source figure** | `lecture_3_p18_img1` | `lecture_3_p58_img1` | `lecture_4_p19` | `lecture_4_p53` | `lecture_5_p16` | `lecture_6_p11` | `page018_safety` | `page025_security` | L7 figures | `fig05_usability` |

> **Power** (Ch 12) has no tactic tree — only a rule of thumb: *minimise software interference; preload / prefetch / offload to lower-energy components; degrade gracefully.* Use the **graceful-degradation** ladder figure as substitute.

### A.2 Tactics trees as side-by-side ASCII

**Integrability — Limit · Adapt · Coordinate**
```
Integrability
├── Limit dependencies
│   ├── Avoid
│   ├── Bundle (versions)
│   └── Encapsulate
├── Adapt
│   ├── Discover
│   ├── Tailor (translate / transform)
│   └── Configure behaviour
└── Coordinate
    ├── Orchestrate
    └── Manage resources
```

**Modifiability — Reduce · Increase · Defer**
```
Modifiability
├── Reduce coupling
│   ├── Split / Combine modules
│   ├── Encapsulate
│   ├── Use intermediary
│   └── Restrict dependencies
├── Increase cohesion
│   └── Redistribute responsibilities
└── Defer binding
    ├── Compile-time
    ├── Build-time
    ├── Deploy-time
    ├── Startup-time
    └── Runtime
```

**Testability — Control & Observe · Limit Complexity**
```
Testability
├── Control & observe state/inputs
│   ├── Input generation (fuzzing)
│   ├── Record / playback
│   ├── Special test interfaces
│   ├── Localised state storage
│   ├── Abstract data sources
│   └── Built-in assertions / monitors
└── Limit complexity
    ├── Limit structural complexity
    ├── Limit non-determinism
    └── Sandboxes
```

**Deployability — Manage Pipeline · Manage Deployment**
```
Deployability
├── Manage pipeline
│   ├── Separate build / test / deploy
│   ├── Canary
│   ├── Scripted deploy
│   └── Pipeline rollback
└── Manage deployment
    ├── Multi-version
    ├── Feature toggle
    ├── Live rollback (blue/green)
    └── Secure defaults
```

**Availability — Detect · Repair · Reintroduce · Prevent**  (the big one)
```
Availability
├── Detect faults
│   ├── Ping/echo · Heartbeat · Monitor · Timestamp
│   ├── Sanity check · Condition monitor · Self-test
│   └── Voting (TMR / replication / functional+analytical)
├── Repair (recover)
│   ├── Active / Passive redundancy
│   ├── Hot / Warm / Cold spare
│   ├── Exception handling · Retry · Ignore faulty
│   ├── Degradation · Reconfiguration
│   └── Rollback (memento / saga)
├── Reintroduce
│   ├── Shadow operation
│   ├── State resynchronisation
│   ├── Escalating restart
│   └── Non-stop forwarding
└── Prevent
    ├── Removal from service
    ├── Transactions
    ├── Predictive model
    ├── Increase competence set
    ├── Exception prevention
    └── Isolate faulty parts (bulkhead / sharding)
```

**Performance — Control Demand · Manage Resources**
```
Performance
├── Control demand
│   ├── Manage work requests
│   ├── Limit event response (throttling)
│   ├── Prioritise events
│   ├── Reduce overhead
│   ├── Bound execution times
│   └── Increase efficiency
└── Manage resources
    ├── Increase resources
    ├── Increase concurrency
    ├── Maintain multiple copies (cache / replicate)
    ├── Bound queue sizes
    └── Schedule resources
```

**Safety — Avoidance · Detection · Containment · Recovery**
```
Safety
├── Avoidance      → substitution, simplification, predictive model
├── Detection      → sanity check, condition monitor, timeout/watchdog, voting
├── Containment    → redundancy (analytical / functional), limit impact (firewall / barrier), abort
└── Recovery       → fail-safe, graceful degradation, repair, reconfigure
```

**Security — Detect · Resist · React · Recover**
```
Security
├── Detect    → intrusion / anomaly / integrity / msg-delay / DoS
├── Resist    → identify · authn · authz · limit access · limit exposure · encrypt · separate · validate input · change defaults
├── React     → revoke access · lock computer · inform actors
└── Recover   → audit + restore (reuses Availability)
```

**Scalability (Bondi) — six axes, no tree**
```
Scalability dimensions: Load · Space · Space-time · Distance · Speed-distance · Structural
```

**Usability — six sub-QAs**
```
Discoverability · Learnability · Operability/Efficiency · Understandability · Flexibility · ( + Aesthetics)
```

### A.3 Recurring pattern across the trees

| Family | QAs that use it | Branch labels |
|---|---|---|
| **Detect → Recover** loop | Availability, Safety, Security | D-R-R-P / A-D-C-R / D-R-R-R |
| **Reduce / Adapt / Coordinate** triad | Integrability, Modifiability | L-A-C ≈ R-I-D |
| **Demand vs Resources** duality | Performance, Scalability (load axis) | C-M; horizontal/vertical |
| **No tactic tree** | Usability, Power | sub-QAs / rules-of-thumb |

**Exam tip.** The four-branch *Detect-Repair-Reintroduce-Prevent* tree is the most-asked draw question. **Reintroduce** is the branch most students forget.

---

## Part B — Alphabetical Pattern Catalog

**Legend.** *Primary QA* = canonical home; *Secondary* = where it re-appears; *Use* = one-liner trigger; *Avoid* = one-liner anti-trigger.

### A

- **Active-Active / Active-Passive** — Two (or more) replicas share or stand by for load. *Primary:* Availability. *Secondary:* Scalability, Performance. *Use:* downtime budget tight, replicas affordable. *Avoid:* state can't be replicated cheaply. → See **Ch 7 §Repair**.
- **Auto-Scaler** — Controller that adds/removes resources from a pool against a target metric. *Primary:* Scalability. *Secondary:* Performance, Availability. *Use:* bursty load with elastic infra. *Avoid:* stateful nodes without rebalancing. → See **Ch 9 §Horizontal scaling**.

### B

- **Batch-Sequential** — Stage produces a complete dataset before the next stage starts. *Primary:* Modifiability. *Secondary:* Performance (offline jobs), Availability (saga cousin). *Use:* large records, no streaming need. *Avoid:* latency-sensitive flows. → See **Ch 4 §Patterns**.
- **Bridge** — Decouples an abstraction from its implementation so both vary independently. *Primary:* Integrability (design-time encapsulation). *Secondary:* Modifiability. *Use:* multiple back-ends, multiple front-ends. *Avoid:* exactly one implementation in sight. → See **Ch 3 §Wrapper/Bridge/Mediator**.
- **Broker (incl. SIEM)** — Intermediary that routes requests / events between producers and consumers. *Primary:* Integrability. *Secondary:* Safety+Security (SIEM is broker + pipe-and-filter). *Use:* many-to-many comms, location transparency. *Avoid:* hot path with strict latency budget. → See **Ch 3 §Mediator/Broker** and **Ch 10 §SIEM**.
- **Bulkhead** — Partition resources into pools so failure in one pool can't drain the others. *Primary:* Availability (Prevent / Isolate). *Secondary:* Performance, Scalability. *Use:* one noisy tenant must not starve others. *Avoid:* uniform workload, partitioning adds waste. → See **Ch 7 §Prevent**.

### C

- **CDN (Content Delivery Network)** — Edge caches geographically close to users. *Primary:* Scalability (distance axis). *Secondary:* Performance (latency), Availability (origin offload). *Use:* read-heavy static / cacheable content, global audience. *Avoid:* highly personalised, write-heavy traffic. → See **Ch 9 §CDN/SDN**.
- **Circuit Breaker** — Watches failure rate of a downstream call and trips open to fail fast. *Primary:* Availability (Repair). *Secondary:* Performance (throttling), Security (limit blast radius). *Use:* remote dependency with known failure modes. *Avoid:* no fallback exists — tripping just hides the bug. → See **Ch 7 §Repair, state diagram**.
- **Claim-Check** — Replace a large payload on the wire with a small token; consumer fetches blob by token. *Primary:* Performance (reduce overhead). *Secondary:* Integrability (smaller messages = looser coupling). *Use:* messages too big for the bus / queue. *Avoid:* small payloads — extra round trip costs more than it saves. → See **Ch 8 §Reduce overhead**.
- **Client-Server** — Roles fixed: clients initiate, server responds. *Primary:* Modifiability (separation of concerns at deploy boundary). *Secondary:* Integrability, Scalability. *Use:* multiple uniform clients, central authority. *Avoid:* peer roles, low-latency mesh. → See **Ch 4 §Patterns**.

### D

- **Dependency Injection** — A component receives its collaborators from the outside instead of constructing them. *Primary:* Testability (swap stubs / mocks). *Secondary:* Modifiability (defer binding), Integrability. *Use:* unit testing, multiple environments. *Avoid:* simple value objects — over-engineering. → See **Ch 5 §Patterns**.

### G

- **Gateway** — Single entry point that routes / authenticates / rate-limits incoming requests. *Primary:* Scalability. *Secondary:* Security (TLS termination, authn), Performance (caching, compression), Availability (LB). *Use:* you have multiple back-end services and one public surface. *Avoid:* single internal monolith — gateway becomes redundant hop. → See **Ch 9 §Gateway**.

### H

- **Hot / Warm / Cold Spare** — Standby replicas with progressively more state preloaded. *Primary:* Availability (Repair). *Secondary:* Scalability. *Use:* recovery-time target drives cost/state trade. *Avoid:* downtime tolerable — spend the money elsewhere. → See **Ch 7 §Spare types**.

### I

- **Intercepting Filter** — Chain of filters runs before / after the main handler (logging, auth, decoration). *Primary:* Testability (control & observe). *Secondary:* Security (input validation), Modifiability (cross-cutting). *Use:* cross-cutting concerns over many handlers. *Avoid:* one handler, one filter — direct call is clearer. → See **Ch 5 §Patterns**.

### L

- **Layered** — Stack of layers; each only depends on the layer below. *Primary:* Modifiability (Foundations introduce it in Ch 1). *Secondary:* Integrability, Testability. *Use:* clear vertical separation (UI / domain / data). *Avoid:* cross-layer optimisations (skip-layer calls erode the discipline). → See **Ch 1 §Layering**, instance in **Ch 15 §Linux network stack**.

### M

- **MapReduce** — Split workload into parallel `map` tasks then aggregate with `reduce`. *Primary:* Performance (manage resources / concurrency). *Secondary:* Scalability. *Use:* embarrassingly parallel, large dataset, commutative aggregate. *Avoid:* low-latency online queries — overhead dominates. → See **Ch 8 §MapReduce**.
- **Mediator** — Centralises runtime interactions between objects so they don't refer to each other directly. *Primary:* Integrability (runtime encapsulation). *Secondary:* Modifiability. *Use:* N-to-N runtime coupling. *Avoid:* simple 1-to-1 collaboration. → See **Ch 3 §Wrapper/Bridge/Mediator**.
- **Memento** — Capture and externalise an object's state without violating encapsulation. *Primary:* Usability (undo). *Secondary:* Deployability (rollback), Performance (claim-check cousin). *Use:* user-facing undo / time travel. *Avoid:* huge state — memory blows up. → See **Ch 12 §Undo**.
- **Microservices** — Independently deployable, separately owned services around bounded contexts. *Primary:* Deployability. *Secondary:* Scalability, Modifiability, Integrability. *Use:* independent release cadence, team autonomy. *Avoid:* small team, low scale — monolith ships faster. → See **Ch 6 §Microservices**, scale follow-up in **Ch 9**.
- **Monitor-Actuator** — Independent monitor watches the system and an actuator forces a safe state on alarm. *Primary:* Safety. *Secondary:* Availability. *Use:* control system with fail-safe state. *Avoid:* no defined safe state. → See **Ch 10 §Monitor-Actuator**.
- **MVC (Model-View-Controller)** — Splits domain model, presentation, and input handling. *Primary:* Modifiability. *Secondary:* Usability (re-skinning), Testability. *Use:* UI app with multiple views over one model. *Avoid:* no UI, no presentation logic. → See **Ch 4 §MVC**.

### O

- **Observer** — Subject notifies registered observers on state change; tight 1-to-N runtime link. *Primary:* Integrability. *Secondary:* Usability (A/B statistics), Availability. *Use:* in-process, known observer set. *Avoid:* distributed, anonymous subscribers — use Pub-Sub. → See **Ch 3 §Observer vs Pub-Sub**.

### P

- **Pipe-and-Filter** — Stream of data flows through stateless filter stages connected by pipes. *Primary:* Modifiability. *Secondary:* Safety+Security (SIEM), Case study (**Ch 15** Netfilter + network stack). *Use:* stream processing, composable transforms. *Avoid:* cross-stage state, branching control flow. → See **Ch 4 §Pipe-and-Filter**.
- **Plugin / Micro-Kernel** — Small fixed core + late-bound extensions discovered at runtime. *Primary:* Modifiability (defer binding). *Secondary:* Integrability, Testability. *Use:* extension points known, third parties extend. *Avoid:* one team, one binary — adds indirection. → See **Ch 4 §Plugin**.
- **Publish-Subscribe** — Producers publish topics; subscribers register interest; broker decouples them. *Primary:* Integrability. *Secondary:* Availability (quorum / event sourcing), Scalability. *Use:* distributed event flows, unknown subscribers. *Avoid:* synchronous request / response. → See **Ch 3 §Observer vs Pub-Sub**.

### R

- **Reference Architecture** — Domain-specific, prescriptive blueprint (components, connectors, decisions) re-used across products. *Primary:* Integrability + Modifiability (shapes the whole product line). *Secondary:* every QA. *Use:* family of related systems in a domain (e.g. MLOps in **Ch 16**). *Avoid:* one-off prototype. → See **Ch 16 §MLOps reference architecture** and **Ch 1 §Foundations**.

### S

- **Saga** — Long-running business transaction split into local steps, each with a compensating action. *Primary:* Availability. *Secondary:* Integrability (across services), Deployability. *Use:* distributed transaction without 2PC. *Avoid:* short, single-DB transaction — plain ACID is fine. → See **Ch 7 §Saga (flight+hotel)**.
- **SDN (Software-Defined Networking)** — Decouple network control plane from data plane; programmable routing. *Primary:* Scalability. *Secondary:* Security (segmentation), Availability. *Use:* dynamic topology, multi-tenant. *Avoid:* small fixed LAN. → See **Ch 9 §CDN/SDN**.
- **Service Mesh** — Sidecar-per-service network plane for mTLS, retries, telemetry, traffic policy. *Primary:* Scalability. *Secondary:* Security (zero-trust), Availability (retries / circuit breaking), Deployability. *Use:* dozens of services, polyglot stack. *Avoid:* 1-2 services — mesh overhead dwarfs benefit. → See **Ch 9 §Service mesh** + zero-trust in **Ch 11**.
- **Sidecar** — Helper process / container deployed alongside the main service sharing its lifecycle. *Primary:* Scalability. *Secondary:* Security (zero-trust proxy), Deployability, Observability. *Use:* cross-cutting concern injected without changing service code. *Avoid:* extreme low-latency hot path — extra hop costs. → See **Ch 9 §Sidecar**.
- **Strategy** — Encapsulates interchangeable algorithms behind a common interface. *Primary:* Testability (swap algorithm for stub / mock). *Secondary:* Modifiability (defer binding), Performance (pick algorithm by load). *Use:* multiple algorithms for the same problem. *Avoid:* one algorithm ever. → See **Ch 5 §Patterns**.

### T

- **Throttling** — Cap the rate of accepted requests; reject / queue / shed excess. *Primary:* Performance (limit event response). *Secondary:* Availability (overload protection), Security (DoS resist), Power (P-states cousin in Ch 12). *Use:* downstream capacity finite, bursts likely. *Avoid:* surplus capacity — throttling wastes it. → See **Ch 8 §Throttling**.
- **Type Safety** — Compile-time / static guarantees that values match their declared types. *Primary:* Modifiability (defer binding shifted to compile time). *Secondary:* Testability, Security (whole bug-class removed). *Use:* refactor confidence, large team. *Avoid:* throwaway scripts. → See **Ch 4 §Patterns** and **Ch 5 §Limit complexity**.

### W

- **Wrapper** — Thin adapter that translates one interface to another without changing behaviour. *Primary:* Integrability. *Secondary:* Performance (Ch 8 may *delete* wrappers to reduce overhead), Modifiability. *Use:* third-party API, version drift, legacy boundary. *Avoid:* hot path — wrapper hop adds cost. → See **Ch 3 §Wrapper/Bridge/Mediator**.

---

### B.1 Quick "by QA" inverted index

| QA | Patterns most often associated |
|---|---|
| Integrability (Ch 3) | Observer, Pub-Sub, Wrapper, Bridge, Mediator, Broker, Service discovery |
| Modifiability (Ch 4) | Layered, Client-Server, MVC, Pipe-and-Filter, Batch-Sequential, Plugin/Micro-Kernel, Type Safety |
| Testability (Ch 5) | Strategy, Dependency Injection, Intercepting Filter, Sandbox |
| Deployability (Ch 6) | Microservices, Rolling Upgrade, Blue/Green, Canary, A/B, Feature Toggle |
| Availability (Ch 7) | Circuit Breaker, Saga, Bulkhead, Hot/Warm/Cold Spare, Active-Active / Active-Passive, Watchdog/Heartbeat, TMR, Shadow |
| Performance (Ch 8) | Throttling, MapReduce, Claim-Check, Cache-aside / Refresh-ahead / Write-through |
| Scalability (Ch 9) | Gateway, Sidecar, Service Mesh, Auto-Scaler, CDN, SDN |
| Safety (Ch 10) | Monitor-Actuator, Functional / Analytical Redundancy, Barrier, Fail-Safe |
| Security (Ch 10-11) | Broker (SIEM), Reverse Proxy, Zero-Trust Sidecar, Honeypot, Privilege Drop |
| Usability (Ch 12) | Memento (undo), Observer (telemetry), MVC (re-skin) |
| Power (Ch 12) | Graceful Degradation, Preloading (escalating restart in reverse) |

### B.2 Cross-cutting "this looks like that" mini-map

| Pattern A | Pattern B | Why they rhyme |
|---|---|---|
| Observer | Publish-Subscribe | Both = N observers of state changes; PS adds broker + late binding |
| Wrapper | Bridge | Both decouple — Wrapper one-sided, Bridge two-sided |
| Pipe-and-Filter | Batch-Sequential | Both stage-based; PF streams, BS batches |
| Pipe-and-Filter | SIEM | SIEM = pipe-and-filter inside a broker |
| Saga | Batch-Sequential | Stage-based with compensation instead of restart |
| Claim-Check | Memento | Both externalise state behind a token |
| Circuit Breaker | Throttling | Both limit downstream load; CB is reactive, throttling is proactive |
| Sidecar | Service Mesh | Mesh = network of sidecars cooperating |
| Bulkhead | Sharding | Both partition for isolation; bulkhead isolates *resources*, sharding isolates *data* |
| Escalating Restart | Preloading | Same machinery in opposite direction (Ch 7 vs Ch 12) |
| Hot/Warm/Cold Spare | Active-Active / Active-Passive | Spare = how much state is preloaded; A-A/A-P = how traffic is split |

---

## Part C — Two-step exam recall drill

When the exam says **"draw the X tactics tree"**:

1. Write the **branch mnemonic** first (e.g. *D-R-R-P* for availability).
2. Under each branch, write **at least 2 named tactics** (the grading rubric in Ch 17 expects 2-per-branch minimum).
3. Add the **signature pattern** that visualises each branch (e.g. *circuit breaker* under Repair, *bulkhead* under Prevent).

When the exam says **"name a pattern for QA Y and justify"**:

1. Pick from the **B.1 inverted index** above.
2. State the **branch of the tactic tree** it implements.
3. State **one secondary QA** it also affects (positive or negative trade-off) — the rubric rewards trade-off awareness.

> Cross-references in this chapter follow the canonical TOC; if a chapter says it owns a pattern, *that* chapter is where the worked example, state diagram, or running scenario lives.
