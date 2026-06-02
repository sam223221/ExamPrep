# Lecture 5: Availability

> **Source:** lecture_5.pdf (80 pages)
> **Lecturer:** Jukka Ruohonen
> **Date (if stated):** March 10, 2026

This lecture treats **availability** as a distinct quality attribute, following the now-familiar pattern from lectures 2–4: definition → 6-slot QA scenario → tactics tree (Detect / Recover / Prevent) → patterns. It deliberately positions availability against the *other* QAs that touch it — security (CIA triad), reliability (fault tolerance), maintainability (planned downtime) — and leaves performance/scalability for a later lecture (likely lecture 6).

## Themes covered

1. **Framing availability** — definitions, faults vs failures vs faulttriggers, the "nines" downtime budget.
2. **Availability QA scenario template** — 6 slots (source, event, environment, system, response, response measure) populated with availability-specific values.
3. **Detect tactics** — monitor, watchdog, heartbeat, ping/echo, timestamps, sanity checking (CRC), voting (replication, functional, analytical, dual/triple modular redundancy), exception detection, self-tests.
4. **Recover-by-Repair tactics** — redundancy + consistency models (eventual / quorum / synchronized / read-after-write), rollback, exception handling, retry (with exponential back-off and circuit breaker), ignore, graceful degradation, reconfigure.
5. **Recover-by-Reintroduce tactics** — shadow, state re-synchronization, escalating restart, non-stop forwarding.
6. **Prevent tactics** — isolation (blast radius, sharding, cascading failure prevention), removal, ACID transactions, predictive models, exception prevention, increase competence.
7. **Availability patterns** — active / passive / spare redundancy (hot/warm/cold spare), FIFO vs LIFO queuing, bulkheads (equitable resource allocation), taint and quarantine, saga.
8. **Over-engineering as new technical debt** — the lecture closes with a Williams (2026) provocation that resilience designed for hypothetical traffic accumulates complexity that quietly degrades systems.

## Concepts

### Availability
**Definition:** The ability of a system to be available to serve, use, deliver, or otherwise function whenever it is needed.
**Why it matters:** Even brief outages of high-traffic services have severe revenue, safety, and trust consequences (CrowdStrike July 2024 and Cloudflare December 2025 are the lecture's running case study).
**Detailed explanation:** Availability sits at the intersection of three other domains. From the *security* side, the CIA triad's "A" requires the system be available to *authorized* parties only — adding security checks costs availability. From the *reliability* side, availability becomes "the ability of a system to prevent, mask, and repair faults so they do not become failures." From the *maintainability* side, scheduled downtime for upgrades cuts into the same budget.
**Analogy:** A 24/7 supermarket. Security wants ID checks at the door (slows entry), reliability wants the freezers to keep running through power dips (needs backup generators), maintenance wants the floor waxed (closes a lane). All three reduce the hours customers can shop — that overlap is what availability is.
**Example:** Bass et al. table — a 99.999% ("five nines") system can be down only 5 min 15 sec per year. A 90% system can be down 3 days 15.6 hours per year.
**Common pitfall / nuance:** Availability is *not* uptime alone — a system that is "up" but returning wrong answers or refusing authorized users is not available. The definition is anchored in *functioning whenever needed*.

### Fault vs Failure vs Trigger
**Definition:** A **failure** is a deviation of the system from its specification. A **fault** is the internal or external *cause* that could become a failure. A **trigger** is the event that activates a latent fault.
**Why it matters:** Almost every availability tactic targets a specific link in this chain — prevent the fault, stop the trigger, mask the failure, or repair fast.
**Detailed explanation:** Faults can sit dormant for years (a null-pointer code path never executed) until a trigger fires (a particular input arrives). Fault-tolerant design tries to maximize the *route* fault → trigger → repair → recovery and minimize the *route* fault → trigger → failure (or, if failure does happen, minimize time-to-repair).
**Analogy:** A fault is a crack in a dam. The trigger is a flood. Failure is the dam breaking. Repair is the patch and re-fill. The whole game is keeping cracks small and re-filling fast.
**Example:** Lecture's Figure 2 — two parallel arrows leaving "fault + trigger": route (a) goes to repair; route (b) goes to failure.
**Common pitfall / nuance:** Beginners equate "bug" with "failure"; a bug is a fault. It only becomes a failure if user-visible specification is violated.
**Related diagram:** `![Fault to failure flow](../images/lecture_5/lecture_5_p11_page_fault_to_failure_flow.png)`

### The "Nines" of Availability
**Definition:** Availability targets expressed as a percentage of total time the system must function, conventionally written with 9s (90%, 99%, 99.9% = "three nines", 99.99% = "four nines", 99.999% = "five nines", 99.9999% = "six nines").
**Why it matters:** Each extra nine is roughly a 10× cost increase in redundancy and engineering effort, so it is the cleanest way to quantify availability requirements in QA scenarios.
**Detailed explanation:** "Five nines" — the de-facto telecom and high-availability cloud standard — allows ~5 minutes downtime per year. "Six nines" allows 32 seconds per year, which essentially demands geographically distributed active-active redundancy. The lecture asks the audience what is a "sensible requirement for a general-purpose high-availability system" — the implicit answer is *four nines for most web apps; five is reserved for critical infrastructure*.
**Analogy:** A bathroom-stall lock that fails once a year (8760 h availability budget × 0.99999 ≈ 0.09 h downtime) — feels safe. A heart pacemaker with the same SLA — terrifying.
**Example:** 99.999% = 5 min 15 sec downtime per year, per the lecture table.
**Common pitfall / nuance:** Nines must be defined against a *measurement window* (per year vs. per quarter vs. per 90 days) and a *what counts as up* definition (full feature set vs. degraded mode).

### Availability QA Scenario (6 slots)
**Definition:** A structured template for stating an availability requirement so it is measurable and testable: Source → Event → Environment → System (deployment) → Response → Response Measure.
**Why it matters:** Forces stakeholders to convert vague "the system must be reliable" into auditable acceptance criteria with concrete time bounds.
**Detailed explanation:** Same template family used in lectures 2-4 (testability, modifiability, integrability), populated with availability-flavored values: **Source** = external/internal, people/hardware/software/physical; **Event** = fault, crash, omission, incorrect timing, incorrect response; **Environment** = normal/startup/repair/degraded/overloaded; **System** = entire/machines/components/connectors/modules/classes; **Response** = log/notify/recover/disable/postpone/degrade/fix; **Response Measure** = uptime %, time-to-detect, time-to-repair, time in degraded mode, proportion of faults prevented.
**Analogy:** A medical incident report — instead of "patient got worse", the form requires *who*, *what symptom*, *under what conditions*, *which organ*, *what the response was*, and *how it was measured*.
**Example:** "When (source) an external user request triggers (event) a database connection timeout in (environment) overloaded operation, (system) the order-service component must (response) retry with exponential back-off and degrade by serving cached results, with (response measure) time-to-recover < 5 s in 99.9% of cases."
**Common pitfall / nuance:** Don't conflate Source with Event — the Source is the *origin* of the stimulus (a person, a sensor, the OS), the Event is the *nature* of the disturbance (a crash, a timing violation).
**Related diagram:** `![Availability scenario template](../images/lecture_5/lecture_5_p13_page_availability_scenario_template.png)`

### Availability Tactics Tree
**Definition:** A four-branch taxonomy of design moves that improve availability: **Detect faults**, **Recover by Repair**, **Recover by Reintroduce**, and **Prevent faults**.
**Why it matters:** Acts as the master menu for the rest of the lecture and the cognitive scaffold for exam questions ("name three Detect tactics", "which tactic is a circuit breaker?").
**Detailed explanation:** The same shape as the integrability, modifiability, testability, and deployability tactics trees from earlier lectures — Ruohonen is consistent. Detect = sense that something is wrong; Recover (Repair) = put the system back into a working state with the existing components; Recover (Reintroduce) = bring a *repaired* component back into service safely; Prevent = stop faults from happening in the first place.
**Analogy:** Hospital ER workflow. Detect = triage and vital-sign monitors. Repair = treat the patient. Reintroduce = post-op recovery ward and discharge. Prevent = public-health campaigns.
**Example:** "Heartbeat" is Detect; "exponential back-off retry" is Repair; "shadow phase before promotion" is Reintroduce; "isolation by failure domain" is Prevent.
**Common pitfall / nuance:** *Recover* has two sub-branches in this tactics tree (Repair and Reintroduce), unlike the simpler trees in earlier lectures — students often miss "Reintroduce" entirely.
**Related diagram:** `![Availability tactics tree](../images/lecture_5/lecture_5_p16_page_availability_tactics_tree.png)`

### Watchdog and Heartbeat
**Definition:** A **watchdog** is a separate component (often a hardware timer) that resets the monitored component if a periodic "I'm alive" signal is not received within a threshold. A **heartbeat** is the same idea inverted: the monitored component proactively pings the monitor on a schedule.
**Why it matters:** Cheapest way to detect a fully hung component that is no longer responding even to itself.
**Detailed explanation:** Watchdog timers were originally hardware in embedded systems (a counter on the motherboard that the OS must reset before it overflows, otherwise it triggers a hard reboot). Heartbeats generalize the idea to distributed systems: every N seconds, "I'm still here" — silence implies death. Both are paired with a *threshold* (how many missed beats = dead?) which trades responsiveness against false positives during GC pauses or network blips.
**Analogy:** A diver's surface line. The boat captain expects a tug every 2 minutes. Three missed tugs = pull up.
**Example:** Linux kernel `/dev/watchdog`; Kubernetes liveness probes; Kafka consumer group heartbeats.
**Common pitfall / nuance:** Set the threshold too tight and a stop-the-world GC pause reboots a healthy node; too loose and a real crash goes undetected for minutes.
**Related diagram:** `![Watchdog and heartbeat](../images/lecture_5/lecture_5_p18_page_watchdog_heartbeat.png)`

### Timestamps vs Sequence Numbers
**Definition:** Both attach monotonically increasing markers to events so that out-of-order or missing events can be detected. Sequence numbers are integers (1, 2, 3...); timestamps are wall-clock or monotonic-clock readings.
**Why it matters:** In distributed systems, clocks drift, jump backwards on NTP correction, and disagree across machines — so sequence numbers are usually safer for ordering.
**Detailed explanation:** "Why might sequence numbers be preferred over timestamps?" is the slide's framing question. Answers: monotonic by construction, no clock-skew problem, smaller (integers vs nanosecond timestamps), and easy to detect gaps (n+1 should follow n). Timestamps have the advantage of being meaningful for *latency* analysis.
**Analogy:** Numbered tickets at the deli (sequence) vs writing the time the customer arrived (timestamp). Tickets never tie or run backwards; clocks can.
**Example:** TCP sequence numbers; Kafka offsets; Lamport clocks.
**Common pitfall / nuance:** Sequence numbers wrap (32-bit will eventually overflow); long-running flows need *sequence number + epoch* or 64-bit counters.

### Sanity Checking and CRC
**Definition:** Verification of operations, states, inputs and outputs at runtime against expected properties. **Cyclic Redundancy Check** (CRC) is a classical error-correction code that appends a checksum to a payload so that corruptions in transit can be detected.
**Why it matters:** Catches a huge class of detectable faults (bit flips, malformed packets, off-by-one offsets) before they propagate.
**Detailed explanation:** A firewall receiving an ICMP echo verifies the packet type (8 bits), checksum (16 bits), identifier (16 bits), sequence number (16 bits), and payload — mismatches → drop the packet and log. CRC "appends a check value without adding new information"; if recomputation at the receiver does not match, the receiver knows the data is corrupted but typically *not* by whom. **Crucially, CRC is for integrity, not security** — it is trivially forgeable; do not use it as a hash for authentication.
**Analogy:** The last digit of an ISBN — designed to catch single-digit typos and most adjacent-digit swaps. Useless against deliberate fraud.
**Example:** Ethernet frame CRC; ZIP-file CRC-32; ICMP checksums.
**Common pitfall / nuance:** Students reach for CRC when they should reach for SHA-256 or HMAC; the lecture flags this explicitly.

### Voting (Replication, Functional, Analytical)
**Definition:** Comparing outputs from multiple components that should produce the same answer and choosing the right output by some rule (majority, unanimity, weighted).
**Why it matters:** Lets a system survive *any* single component fault, and — with diversity — also design or implementation faults that would defeat plain replication.
**Detailed explanation:** Three flavors of escalating diversity: **Replication** — identical copies, vulnerable to identical bugs but trivial to operate. **Functional redundancy** — components do the same job by the same broad approach but written differently (different teams, different languages); resists common-mode software bugs. **Analytical redundancy** — components compute the same quantity by *different methods entirely* (e.g., altitude from GPS, radar altimeter, and inertial-navigation cross-check) — the slide explicitly cites the Boeing 737 MAX MCAS disaster as an *anti-pattern* where this was missing. **Dual / triple modular redundancy** is the hardware version (2 or 3 identical logic gates voted by a majority gate).
**Analogy:** A jury. A single judge can be biased (replication of one). Three judges from the same law school may share blind spots (replication of N). Three judges from law, medicine, and engineering analyzing the same case in their own framework (analytical) catches errors none would catch alone.
**Example:** Triple-modular-redundancy in avionics; raft/paxos quorum reads in Etcd/Consul; cross-checking sensor data.
**Common pitfall / nuance:** Replication does **not** protect against design or implementation errors — three identical copies all have the identical bug. Diversity is the only fix.

### Majority Gate
**Definition:** A logic gate that outputs 1 iff at least 2 of its 3 inputs are 1 — the canonical triple modular redundancy voter.
**Why it matters:** Mechanical, exam-ready way to reason about how voting tolerates one faulty component.
**Detailed explanation:** Truth table — rows (0,0,0), (1,0,0), (0,1,0), (0,0,1) output 0; rows (1,1,0), (1,0,1), (0,1,1), (1,1,1) output 1. Survives any one input being wrong.
**Analogy:** Best 2-out-of-3 in a tie-breaker game.
**Example:** Lecture's Table 2 (rows 4, 6, 7, 8 pass the gate).
**Common pitfall / nuance:** Tolerates one failure only — if two voters disagree with reality, the gate confidently outputs the wrong answer.

### Active vs Active-Passive Load Balancing
**Definition:** **Active-active** spreads load across two or more live components (each carries a share, e.g., 50/50). **Active-passive** (a.k.a. "standby") routes 100% to one and keeps the others warm but idle until takeover.
**Why it matters:** Trades cost and complexity for failover speed and capacity.
**Detailed explanation:** Active-active doubles capacity at steady state but requires every replica to handle full load if its sibling dies (so you must over-provision by 50% to survive one loss). Active-passive wastes the standby's compute during normal operation, but the failover semantics are simpler (no live state divergence to merge).
**Analogy:** A two-engine plane in active-active uses both engines all the time, can fly on one with reduced performance. An aircraft with one main engine and an APU in active-passive mode keeps the APU spun down until needed.
**Example:** Two PostgreSQL primaries with logical replication (active-active, hard); one primary + one warm standby with streaming replication (active-passive, common).
**Common pitfall / nuance:** Active-active is only safe when writes are commutative or the system tolerates eventual consistency — otherwise the divergence is worse than the failover delay you saved.
**Related diagram:** `![Load balancing scenarios](../images/lecture_5/lecture_5_p28_page_load_balancing_active_active_vs_passive.png)`

### Consistency vs Availability Trade-Off (CAP echo)
**Definition:** Four consistency models on a single trade-off axis: **eventual** (high availability, low consistency) — replicas converge eventually if no new writes; **quorum** — write succeeds only if a majority of replicas ack; **synchronized** — simultaneous writes everywhere with conflict resolution; **read-after-write** — every read after a write reflects that write regardless of which replica answers.
**Why it matters:** Direct application of the CAP theorem to availability tactic choice.
**Detailed explanation:** As consistency strength increases (eventual → quorum → synchronized / read-after-write), availability decreases because you must wait for more replicas to agree. The lecture draws this as a simple 2-axis chart — eventual top-left (high avail, low cons), synchronized bottom-right (low avail, high cons).
**Analogy:** A group chat. "Eventual" = everyone sees messages whenever they happen to open the app. "Quorum" = the message is only considered "sent" after 3 of 5 people open it. "Synchronized" = the message only goes out when *everyone* has the app open. Faster vs. more agreed-upon.
**Example:** DynamoDB default = eventual; quorum reads (R+W>N) = quorum; Spanner global transactions = synchronized; "read your own writes" mode in many cloud databases = read-after-write.
**Common pitfall / nuance:** "Eventual" does not mean "soon" — under network partition it can mean "after the partition heals", which may be hours.
**Related diagram:** `![Consistency vs availability](../images/lecture_5/lecture_5_p38_page_consistency_vs_availability_tradeoff.png)`

### Retry with Exponential Back-Off
**Definition:** Reattempt a failed operation a bounded number of times with an exponentially increasing sleep between attempts.
**Why it matters:** Solves transient faults (a packet drop, a momentary overload) without overwhelming the very system you are retrying against.
**Detailed explanation:** Naive `while i < max_retries: sleep(constant)` causes thundering-herd retries that prolong outages. Exponential back-off (`sleep = base * 2^i`) gives the downstream room to recover. Typically combined with **jitter** (random ±20%) so synchronized clients don't all retry on the same beat. The lecture's pseudocode (page 42) is the naive form; page 43 names the improvement.
**Analogy:** Calling a friend whose phone is dead. Calling every 5 seconds drains your battery; calling at 1, 2, 4, 8, 16 minutes is gentler on both phones and still catches them when they're back.
**Example:** AWS SDK default retry; HTTP Retry-After respecting clients.
**Common pitfall / nuance:** Without jitter, exponential back-off still produces synchronized retry storms after wide outages.

### Circuit Breaker
**Definition:** A three-state pattern (Closed / Open / Half-open) wrapping calls to a downstream service to **fail fast** when the downstream is repeatedly unhealthy.
**Why it matters:** Stops cascading failures by refusing to keep loading a clearly broken downstream — protects both caller resources and downstream's recovery.
**Detailed explanation:**
- **Closed**: requests flow through; failures increment a counter; threshold reached → trip to Open.
- **Open**: requests fail immediately without hitting the downstream; after a cool-down or successful ping, transition to Half-open.
- **Half-open**: allow a *limited* number of probe requests; if they succeed → back to Closed; if any fail → back to Open.

Pairs naturally with retry, timeout, and bulkheads. Source: Montesi & Weber (2016).
**Analogy:** A house electrical circuit breaker. When too many devices short out, the breaker trips (Open) — flipping it back without unplugging anything just trips it again. After unplugging, you carefully flip it on (Half-open) and test one device at a time before plugging the rest back in (Closed).
**Example:** Hystrix (Netflix, used to be the canonical example — and is the lecture's Case #5!); Resilience4J; Polly (.NET).
**Common pitfall / nuance:** Setting the failure threshold by error *count* rather than error *rate* misfires under variable traffic; use rate + minimum-volume threshold.
**Related diagram:** `![Circuit breaker state diagram](../images/lecture_5/lecture_5_p44_page_circuit_breaker_state_diagram.png)`

### Graceful Degradation
**Definition:** Maintain the availability of critical functions while suspending, slowing, or dropping less critical ones.
**Why it matters:** Lets a stressed system stay *useful* instead of going dark entirely.
**Detailed explanation:** Picks a sacrificable surface so the core function survives. Variants include: priority-based (only critical functions), geographic (only some regions), demographic (majority over minority), drain-mode (finish in-flight work, refuse new). The lecture's example: under a DoS attack on a public-transport site, drop maps and timetables but keep the payment system running.
**Analogy:** An overloaded airplane. To keep flying, the captain dumps fuel, sheds non-essential systems, and drops to a lower altitude — gracefully degrades rather than crashing.
**Example:** YouTube serving 240p instead of 1080p under load; banking apps disabling new transfers but still showing balances.
**Common pitfall / nuance:** Requires up-front classification of "critical" functions — done in cold blood at design time, not in panic during the incident.

### Shadow / State Re-synchronization / Escalating Restart (Reintroduce)
**Definition:** Three tactics for safely returning a repaired component to service:
- **Shadow** — repaired component is brought up but its outputs are *not* used; observed in parallel with the live one for a probation period.
- **State re-synchronization** — repaired component pulls (or is pushed) the latest state, often via checksums or hashes, before it carries production traffic. Traffic is then migrated incrementally (e.g., 0 → 30% → 70%).
- **Escalating restart** — restart progressively wider scopes of functionality (5% → 25% → 60% → 100%) so that the smallest-blast-radius restart is tried first.

**Why it matters:** A naïve "just put it back in" often re-triggers the very fault that caused the failure, or floods the just-repaired component with traffic it cannot yet handle.
**Detailed explanation:** Shadow is the recovery analogue of the *canary* deployment from lecture 4 — same idea, different point in the lifecycle. Escalating restart applies KISS to recovery: try the cheapest reset first (restart just the affected thread), only if that fails escalate to process, container, host, cluster.
**Analogy:** A pilot who has been grounded for medical reasons doesn't go straight to long-haul. They fly with an instructor (shadow), then short domestic routes (escalating), then full duty.
**Example:** Erlang/OTP "let it crash" supervisor trees implement escalating restart by design.
**Common pitfall / nuance:** Shadow needs a way to *compare* shadow output to live output and *not* let the shadow's writes hit production storage.
**Related diagram:** `![Escalating restart](../images/lecture_5/lecture_5_p50_page_escalating_restart.png)`

### Isolation and Blast Radius
**Definition:** **Isolation** is partitioning a system so a failure in one part cannot reach another part. **Blast radius** is the set of components a single fault actually affects.
**Why it matters:** The whole point of isolation is to bound the blast radius — to ensure no single fault can take down the entire system.
**Detailed explanation:** Adkins et al. (2020), the lecture's main reference here, recommend two practices: **functional separation** (different failure domains do different things) and **data isolation** (each failure domain has *its own* data so corrupted data in one cannot poison the others — including configurations, not just user data). The companion concept is **cascading failure** — without isolation a single fault can ripple through the whole system. **Sharding** is one common implementation.
**Analogy:** Watertight compartments in a ship. The Titanic sank because the bulkheads weren't tall enough — water spilled over from one flooded compartment to the next. Real isolation means each compartment can flood completely without flooding its neighbors.
**Example:** AWS regions and availability zones; Kubernetes namespaces and resource quotas; per-tenant database sharding in multi-tenant SaaS.
**Common pitfall / nuance:** "Isolation" reuses lecture 1's coupling discussion but is *not* the same — two components can be loosely coupled in interface and still share a failure domain (same host).
**Related diagram:** `![Blast radius and failure domains](../images/lecture_5/lecture_5_p55_page_blast_radius_failure_domains.png)`

### Hot / Warm / Cold Spare (Active / Passive / Spare Redundancy)
**Definition:** Three redundancy patterns distinguished by how synchronized the standby is.
- **Active (hot spare)** — spare receives every input in parallel with the active component and maintains state *synchronously*. Failover is near-instant.
- **Passive (warm spare)** — spare's state is updated *periodically* by the active component. Failover involves catching up the gap.
- **Spare (cold spare)** — spare is dormant and only initialized when needed. Failover is slow but cheapest to run.

**Why it matters:** Choosing the right shade of redundancy is the single biggest cost-vs-availability lever in most architectures.
**Detailed explanation:** Hot spare gives sub-second failover but doubles compute and network costs and risks the spare diverging in subtle ways from the active. Warm spare amortizes cost (state sync is bulk-async) at the price of a recovery point objective gap. Cold spare is essentially "we have the same hardware in the closet, ready to be configured" — used where minutes-to-hours of downtime are acceptable.
**Analogy:** A goalie. Hot spare = a second goalie on the ice watching every shot — instant in if the first goes down. Warm spare = a backup on the bench warming up between periods. Cold spare = the practice goalie at home — has to drive to the rink.
**Example:** Hot: synchronous PostgreSQL replication; Warm: streaming async replicas; Cold: nightly backups + provisioned-but-stopped EC2 AMI.
**Common pitfall / nuance:** "Active-active" in the load-balancing slide is a special case of hot-spare where *both* sides carry production load instead of one being idle.
**Related diagram:** `![Cold spare redundancy](../images/lecture_5/lecture_5_p67_page_spare_redundancy_cold_spare.png)`

### Bulkheads / Equitable Resource Allocation
**Definition:** Separate resource pools for different request classes so heavy use of one pool cannot starve the others.
**Why it matters:** Without bulkheads a single misbehaving client (or query type) can monopolize the connection pool / thread pool / queue and bring down the whole service for everyone.
**Detailed explanation:** Lecture's example: many small frequent requests + a few rare large requests both hitting a shared handler is fragile — the large ones can monopolize threads. Splitting into a small-request pool and a large-request pool quarantines the damage. The pattern is named after the watertight bulkheads in a ship's hull.
**Analogy:** Two checkout lanes at a supermarket — one for ≤10 items, one for full carts. Without the split, a single full cart blocks every quick shopper.
**Example:** Hystrix thread-pool isolation; per-tenant connection-pool quotas in databases; Kubernetes resource requests/limits per namespace.
**Common pitfall / nuance:** Bulkheads only help if the resource being partitioned is the bottleneck — partitioning CPU when the bottleneck is the database connection achieves nothing.
**Related diagram:** `![Bulkheads equitable allocation](../images/lecture_5/lecture_5_p69_page_bulkheads_equitable_allocation.png)`

### Saga Pattern
**Definition:** A long-lived business transaction decomposed into a sequence of local transactions, each in a different service, where each step has a corresponding **compensating** transaction that undoes its effect if a later step fails.
**Why it matters:** Distributed transactions across microservices cannot use traditional two-phase commit (too slow, too coupled); the saga is the de-facto microservices answer.
**Detailed explanation:** Each local transaction is atomic within its own service, and on success it *notifies* the next step. On failure of step N, the saga rolls back by invoking compensating transactions for steps N-1, N-2, ... 1 in reverse. Reference: Dürr et al. (2021). The lecture's worked example is the course's running flight + hotel booking case (Figure 35): begin saga → book hotel → start booking flight → flight fails → abort saga → cancel flight → cancel hotel → end saga.
**Analogy:** Erecting a multi-stage rocket. Each stage fires and reports back; if stage 3 fails, mission control fires reverse-thrust on the already-flying stages instead of trying to re-merge them mid-flight.
**Example:** Travel booking (the lecture's recurring example); e-commerce order with inventory, payment, shipping each in their own service.
**Common pitfall / nuance:** Compensating transactions are *not* the inverse of the original transaction — they are *semantic* undo (e.g., refund + email), and side-effects already visible to users (an email already sent) cannot be unsent.
**Related diagrams:** `![Saga pattern](../images/lecture_5/lecture_5_p73_page_saga_pattern.png)`

### Taint and Quarantine
**Definition:** When corruption is detected, mark the affected data as "tainted" so no downstream action depends on it, and move it to a quarantine area for offline analysis.
**Why it matters:** Stops a single bad record from being amplified into a cascading bad output.
**Detailed explanation:** Closely related to data isolation (lecture's prevent-isolate tactic) — if data is poisoned, the worst response is to act on it. File systems and disk firmware do this routinely (bad-block remapping, ZFS scrub-and-quarantine). Similar dynamic in security: tainted input → don't sink to database/UI.
**Analogy:** A blood bank's positive-screening sample is moved to a quarantine fridge, never thrown back into the donor pool, and analyzed separately.
**Example:** ZFS putting checksum-mismatched blocks into a "degraded" pool state; SMTP greylisting and spam quarantine.
**Common pitfall / nuance:** Quarantine is only useful if someone reviews the quarantine — write-only quarantines become silent data loss.

### Over-engineering as the New Technical Debt
**Definition:** The lecture's closing argument (Williams 2026): designing for hypothetical scale and edge cases adds operational complexity that itself degrades the system.
**Why it matters:** Counterweight to a lecture that just spent 70 slides showing you tactics you could deploy. The message: each tactic has a cost; resilience for resilience's sake is debt.
**Detailed explanation:** Williams's three claims: (1) traces look fine and dashboards stay green while performance quietly erodes; (2) teams build resilience against hypothetical traffic patterns while ignoring the cost of running today's system; (3) services exist to justify their own abstractions, configuration replaces code, and the architecture technically works "only because people avoid touching it."
**Analogy:** A house with a backup generator, a backup-backup generator, two sump pumps, a battery bank, three smoke alarms, and a tornado shelter. If the homeowner has to spend 6 hours a month maintaining all of it, the *house* is now less reliable than a plain house with one good generator.
**Example:** Microservice topologies where 80% of incidents trace to the inter-service plumbing rather than business logic.
**Common pitfall / nuance:** Don't confuse this with YAGNI for features — it is YAGNI for resilience. Sometimes the right answer is a monolith on one big VM with daily backups.

## Important diagrams (catalog)

- `lecture_5_p11_page_fault_to_failure_flow.png` — the canonical fault → trigger → (repair | failure) flowchart with time-to-repair as the loss metric.
- `lecture_5_p13_page_availability_scenario_template.png` — full 6-slot QA scenario template populated with availability-specific values for each slot.
- `lecture_5_p16_page_availability_tactics_tree.png` — master Detect / Repair / Reintroduce / Prevent tactics tree (4 branches, ~26 named tactics).
- `lecture_5_p18_page_watchdog_heartbeat.png` — watchdog timer mechanics; threshold reached → reset signal.
- `lecture_5_p28_page_load_balancing_active_active_vs_passive.png` — side-by-side active-active (50/50) vs active-passive (100/0) load balancer scenarios.
- `lecture_5_p38_page_consistency_vs_availability_tradeoff.png` — 2-axis chart placing eventual / quorum / synchronized / read-after-write consistency on the trade-off curve.
- `lecture_5_p44_page_circuit_breaker_state_diagram.png` — Closed / Open / Half-open state machine with transition conditions and the "fail fast" annotation.
- `lecture_5_p50_page_escalating_restart.png` — staircase showing 5% → 25% → 60% → 100% scope of restart over time.
- `lecture_5_p55_page_blast_radius_failure_domains.png` — illustrates that with proper isolation, failure domain A contributes 15% and B 85% rather than 100% of the system going down.
- `lecture_5_p67_page_spare_redundancy_cold_spare.png` — cold-spare lifecycle (initialization, dormant operation, failure-triggered activation).
- `lecture_5_p69_page_bulkheads_equitable_allocation.png` — separate request pools for small vs large requests sharing a request handler.
- `lecture_5_p73_page_saga_pattern.png` — chain of local transactions with notify-on-success and compensating-transactions-on-failure.
- `lecture_5_p75_page_patterns_summary_table.png` — closing 2-column table mapping scenarios (unstable network, fickle network, bandwidth limited, inconsistent transactions, cascading failures, high availability priority) to recommended patterns.

## Exam-relevant takeaways

1. **Know the 4-branch tactics tree by heart**: Detect, Recover-by-Repair, Recover-by-Reintroduce, Prevent — and at least 2–3 tactics per branch. *Reintroduce* is the branch students forget.
2. **Be able to draw the 6-slot availability scenario template** and populate every slot with availability-flavored values (source = ext/int, event = fault/crash/omission/incorrect-timing/incorrect-response, etc.).
3. **Fault ≠ failure ≠ trigger**: be precise with these three terms; an exam question can hinge on calling a bug a "failure" when it is only a "fault."
4. **The "nines" cost roughly 10× per nine**: 99.9% to 99.99% is a big jump in architecture, not just one digit.
5. **Replication ≠ functional redundancy ≠ analytical redundancy**. Only analytical/functional diversity survives design defects. Boeing 737 MAX MCAS is the cautionary tale.
6. **Circuit breaker has 3 states** (Closed, Open, Half-open) and "fails fast" in the Open state. Know which transitions are triggered by failures vs successes vs timeouts.
7. **Consistency vs availability** is the CAP-flavored trade-off chart — eventual is most available, synchronized/read-after-write is least.
8. **Active-active vs active-passive vs cold spare** — be able to compare on (cost, failover time, capacity, state-divergence risk).
9. **Bulkheads = ship's bulkheads = separate resource pools**. The pattern name comes from naval architecture and the analogy is the point.
10. **Saga = local transactions + compensating transactions**, not 2PC. Compensation is *semantic* undo, not byte-level rollback. Lecture's worked example is flight + hotel booking.
11. **Isolation bounds blast radius**, which prevents cascading failures. Adkins et al. recommend functional separation *and* data isolation.
12. **Williams 2026 / over-engineering critique** is fair game — the lecture ends on it for emphasis. The message: resilience tactics have an *operational* cost that itself eats availability.

## Cross-references

- **Lecture 1 (foundations)**: Isolation in this lecture (page 53) explicitly recalls lecture 1's coupling discussion ("isolation is related to coupling but not equal to it"). The running flight + hotel example resurfaces in the Saga pattern (Figure 35).
- **Lecture 2 (Quality Attributes)**: The 6-slot scenario template, ASR framing, and ISO 25010 mapping all apply directly — availability is a QA, same machinery as security/reliability/maintainability. The trade-off between security and availability (CIA-A) is a direct continuation of lecture 2's QA trade-off thinking.
- **Lecture 3 (Integrability + Modifiability)**: Quorum consistency explicitly references the **Observer pattern** from lecture 3 ("something akin the Observer pattern could be used"). The Saga pattern is described as similar to the **batch-sequential** pattern from lecture 3 "but with an addition of error correction." The dependency advice (Adkins et al., page 70) recalls lecture 3's dependency types.
- **Lecture 4 (Testability + Deployability)**: Several explicit back-references: rollback was "introduced already in the previous lecture"; assertions and **sanity checking** are "what was said the fourth lecture about assertions"; upgrade as a recovery tactic refers back to lecture 4's deployment material; **blast radius** is described as a concept from lecture 4; the **shadow** reintroduce tactic is essentially the *canary* deployment idea from lecture 4 applied at recovery time rather than release time. Case #4 (CrowdStrike, Cloudflare) opens lecture 5 as a testability/deployability bridge into availability.
- **Likely connects to lecture 6**: The lecture closes by noting availability "will be revisited in later lectures addressing performance and scalability in particular" — caching is explicitly punted to next lecture. Expect lecture 6 = Performance and/or Scalability, with the same definition → scenario → tactics → patterns structure. **Hystrix Case #5** is the bridging assignment.
- **Likely connects to a later lecture on Security**: The CIA-triad and "availability for authorized parties only" framing on page 7 hints that Security gets its own dedicated lecture later; the lecture deliberately defers the security/availability trade-off to that future treatment.
