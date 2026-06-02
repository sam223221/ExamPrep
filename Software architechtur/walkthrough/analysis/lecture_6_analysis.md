# Lecture 6: Performance (Quality Attribute)

> **Source:** lecture_6.pdf (79 pages)
> **Lecturer:** Jukka Ruohonen
> **Date (if stated):** March 17, 2026

## Themes covered

1. **Defining Performance and distinguishing it from Scalability** — "doing more with what you have" versus "adding resources".
2. **Latency vs. Throughput** — units, intuition (CPU caches vs. transatlantic packets), stochastic nature of latency.
3. **The Eight Fallacies of Distributed Computing** (Deutsch / Wilson 2015) as a mental backdrop for everything that follows.
4. **Performance Scenarios** — the 6-slot Bass-style template instantiated for Performance.
5. **Performance Tactics Tree** — two branches: *Control demand* and *Manage resources*, each with six tactics.
6. **Demand-side tactics:** manage requests, limit responses (drop vs. queue), prioritize events, reduce overhead, bound execution, increase efficiency.
7. **Resource-side tactics:** add resources, increase concurrency (threads vs. thread pools), replicate computations, replicate data (CAP / PACELC, cache topologies), bound queues, schedule resources (FIFO, SJF, EDF, rate-monotonic, idle, batch, round-robin).
8. **Performance Patterns:** throttling (implemented via circuit breaker + back-off + jitter), MapReduce, claim-check, static/dynamic content separation, materialized views, and database-specific patterns (sharding, indexing, connection pools).

## Concepts

### Performance (as a distinct QA)
**Definition:** A system's ability to meet its resource requirements — both time (latency, throughput) and space (memory, disk) — under given workload.
**Why it matters:** Performance is what makes a "functionally correct" system actually usable; it is also the QA most commonly violated under unanticipated load.
**Detailed explanation:** Ruohonen frames Performance via algorithmic complexity: time performance (timing requirements) and space performance (memory/disk use). Pure Performance is about *doing more with the resources we have*, not about adding new resources — that "adding resources" angle belongs to Scalability. The two attributes are siblings: Scalability is "proportionally increasing performance by adding resources." Mixing them up leads to the lazy "just throw hardware at it" strategy, which is sometimes correct but is *not* a Performance tactic in the strict sense.
**Analogy:** Performance is making your existing kitchen serve more diners faster (better knife skills, smarter prep order). Scalability is hiring more chefs and adding stoves.
**Example:** A Python service that handles 1k req/s on a single core after switching from a thread-per-request to an async event loop has improved its *Performance*. Bumping the same service to 4 EC2 instances behind a load balancer is *Scalability*.
**Common pitfall:** Treating "buy a bigger box" as a performance improvement. It often is — but architecturally it is a different lever (Scalability) with different cost/availability trade-offs.

### Latency vs. Throughput
**Definition:** Latency is the time to perform a single action or produce one result; throughput is the number of actions/results per unit of time. The optimum is *maximum throughput at minimum latency*.
**Why it matters:** Many architectural decisions optimise one at the expense of the other.
**Detailed explanation:** A pipeline batching 10,000 records before flushing maximises throughput but each individual record sees terrible latency. A non-batching streaming pipeline minimises per-record latency but the per-record overhead caps throughput. The "two basic measures" framing is essential for writing meaningful Performance scenarios — saying "fast" is useless; saying "median latency < 200 ms at 5,000 req/s sustained throughput" is testable.
**Analogy:** Latency is how long it takes one letter to reach a recipient. Throughput is how many letters the postal service moves in a day. A jumbo cargo plane (high throughput) is slower per letter than a courier on a motorbike (low latency).
**Example:** L1 cache reference is sub-nanosecond; sending a TCP/IP packet Denmark→Japan is hundreds of milliseconds — that is a ~9 order-of-magnitude latency gap *within the same software stack*.
**Common pitfall:** Optimising for average latency without looking at tail latency. P99 latency often dominates user experience and is where queues and contention bite.

### Units-of-Time Intuition (latency scale)
**Definition:** A mental scale ordering the cost of fundamental operations from L1 cache (<1 ns) up through main memory, SSD, intra-data-centre TCP, transcontinental TCP, and streaming services.
**Why it matters:** Architectural choices that move work across a tier in this scale (cache → memory → disk → network) change latency by *orders of magnitude*, not percentages.
**Detailed explanation:** Ruohonen's listing emphasises that "latency" without context is meaningless. Kernels schedule in nanoseconds; HTTP services live in milliseconds; satellite networks (Handley 2018) can spike to *100 seconds*. Hence latency is "stochastic rather than deterministic in its nature" — a critical insight for designing timeouts and SLAs.
**Analogy:** It is like distance scales in physics: nm, mm, m, km, light-years. Treating them as interchangeable produces nonsense.
**Example:** Moving a hot-path lookup from main memory (~100 ns) to an out-of-process Redis call (~500 µs) is a 5,000× slowdown — even when both feel "fast."

### Eight Fallacies of Distributed Computing
**Definition:** Eight false assumptions distributed-system developers reflexively make (Deutsch, popularised by Wilson 2015): networks are reliable; latency is zero; bandwidth is infinite; networks are secure; topology does not change; there is one administrator; transport cost is zero; network is homogeneous.
**Why it matters:** Every Performance tactic for distributed systems is in some sense a refutation of one or more fallacies.
**Detailed explanation:** When you replicate data, you are admitting that networks are unreliable. When you add retries with back-off, you admit latency is non-zero and stochastic. When you shard by region, you admit topology and administration differ.
**Analogy:** They are the "I assumed my keys would always be on the hook" of distributed systems — silent assumptions you only notice when they fail.
**Example:** Default HTTP client timeouts of "forever" implicitly assume latency is zero — fine in tests, catastrophic in production.

### Performance Scenario (6-slot template)
**Definition:** Bass-style scenario template specialised for Performance with six slots: Source, Stimulus (Event), Artifact (System under deployment), Environment, Response, Response Measure.
**Why it matters:** Without a written scenario, "the system should be fast" can never be tested or argued about in a review.
**Detailed explanation:** Each slot has typical Performance values. *Source*: external (users, sensors, external systems) or internal (timers, watchdogs). *Stimulus*: periodic, stochastic, sporadic, or cyclic events with some weight. *Environment*: normal/peak/overload/emergency/degraded mode. *Artifact*: entire system or specific machines/components/connectors/modules/classes. *Response*: respond, error, no return, ignore, switch mode, prioritise. *Response measure*: latency (with scale + statistic), share of failed/rejected requests, jitter, resource levels.
**Analogy:** A Mad-Libs sheet for non-functional requirements — fill all six blanks and you have something testable.
**Example:** *"During Black Friday peak load mode (10× normal traffic) the checkout component must respond to user payment-submit events with P99 latency < 800 ms and < 0.1 % rejected requests."*
**Common pitfall:** Specifying only an *average* response measure; the interesting failures live in the tail.
**Related diagram:** `![Performance scenario template](../images/lecture_6/lecture_6_p06_page_performance_scenario_template.png)`

### Performance Tactics Tree (two branches)
**Definition:** A taxonomy with two top-level branches: *Control demand* (six tactics) and *Manage resources* (six tactics).
**Why it matters:** It is the menu of architectural levers. Every Performance review should be able to point at which tactic(s) were chosen and which were rejected.
**Detailed explanation:** *Demand* tactics: 1. Manage requests, 2. Limit responses, 3. Prioritize events, 4. Reduce overhead, 5. Bound execution, 6. Increase efficiency. *Resources* tactics: 1. Increase resources, 2. Increase concurrency, 3. Multiple copies of computations, 4. Multiple copies of data, 5. Bound queues, 6. Schedule resources. The demand side tries to *do less*; the resource side tries to *use what you have better*.
**Analogy:** Either eat fewer calories (control demand) or burn them more efficiently (manage resources). Both work; both have trade-offs.
**Related diagram:** `![Performance tactics tree](../images/lecture_6/lecture_6_p11_page_performance_tactics_tree.png)`

### Tactic — Manage requests (demand)
**Definition:** Bounding the arrival rate or sampling frequency of requests, often externally via ToS or SLAs.
**Why it matters:** The cheapest performance fix is the work you do not do.
**Detailed explanation:** Examples include rate-limit clauses in B2B service-level agreements, reducing video-stream fidelity, sampling sensor data periodically instead of continuously. There is always a QoS trade-off: fewer/smaller requests means lower fidelity for the client.
**Example:** Cloudflare's "I'm under attack" mode is essentially manage-requests applied as a wholesale traffic filter; the AI-scraping discussion on page 13 is the same pattern at policy level.

### Tactic — Limit responses (drop vs. queue)
**Definition:** When a resource threshold is reached, either *drop* new requests immediately or *queue* them for later processing.
**Why it matters:** "Limit responses" is the system's behaviour when it cannot keep up — and it must be a *design choice*, not an accident.
**Detailed explanation:** Dropping (A) protects the system but cuts off availability; queueing (B) preserves availability but trades it for latency and memory pressure. Linux's OOM killer is a brutal example of limit-by-drop ("kill the most memory-hungry process"); setting `/proc/sys/vm/panic_on_oom = 1` chooses the even more uncompromising "crash loudly" variant.
**Analogy:** A nightclub that has hit capacity can either turn people away at the door (drop) or have them wait in line outside (queue). Both are bouncer policies — neither is "no policy."
**Common pitfall:** Unbounded queues. They look like "graceful degradation" but actually convert a CPU problem into a memory problem and hide load.
**Related diagram:** `![Drop vs queue limiting](../images/lecture_6/lecture_6_p15_page_limit_responses_drop_vs_queue.png)`

### Tactic — Prioritize events (FIFO/LIFO/priority/fairness queues)
**Definition:** Assigning priority values to events so that higher-priority work runs first.
**Why it matters:** Without prioritisation, important and trivial work share a FIFO and the important work suffers from head-of-line blocking.
**Detailed explanation:** Examples include OS network stacks that support priority queues and stochastic fairness queueing (Cho 1999). Trade-offs: fairness (who decides priority?) and overhead (if you never exceed capacity, prioritisation is pure cost).
**Analogy:** Hospital triage — green/yellow/red tags. Necessary because some patients can wait, others cannot.
**Common pitfall:** Static priorities cause starvation of low-priority work; pure fairness causes critical work to miss deadlines. Stochastic fairness queueing is a compromise — random queue selection per event.
**Related diagram:** `![Priority and fairness queues](../images/lecture_6/lecture_6_p18_page_priority_vs_stochastic_fairness_queueing.png)`

### Tactic — Reduce overhead
**Definition:** Cut intermediaries — wrappers, filters, pipe stages, network hops — between request and answer.
**Why it matters:** Every layer adds latency; over time architectures accrete intermediaries that nobody can later justify.
**Detailed explanation:** Ruohonen explicitly calls out "maybe numerous wrappers were not a good idea after all" and "maybe you had too many filters in your pipe-and-filter pattern." Co-locating components on the same machine (vs. spread across machines with network hops in between) is the classic illustration. Trade-off: against maintainability and modifiability (Lecture 3) — flat code is faster but harder to evolve.
**Analogy:** Removing speed bumps from a road. Faster commute, more accidents.
**Common pitfall:** Reducing overhead by inlining everything until the codebase becomes unmaintainable. Performance gains die the next time someone refactors blindly.

### Tactic — Bound execution
**Definition:** Capping the time, memory, or other resource a unit of work is allowed to consume.
**Why it matters:** Bounds are reserve capacity, an interpretability tool, and a security control all at once.
**Detailed explanation:** A machine-learning training loop with `max_iterations=10000` is bound-execution. NetBSD's `setrlimit(2)` (referenced on page 22) lets you cap CPU time, file size, address space, and stack size per process. The same primitive that prevents an algorithm from running forever also prevents fork-bomb attacks.
**Example:** Lambda functions have a default execution timeout — it is a bound-execution tactic applied at the infrastructure layer.

### Tactic — Increase efficiency (better algorithms)
**Definition:** Replacing an algorithm or implementation with a faster equivalent.
**Why it matters:** Sometimes the only way to break out of an O(n²) cliff.
**Detailed explanation:** Trade-offs are with maintainability and portability — Ruohonen notes that some kernel routines once hand-written in x86 assembly were later removed because nobody else understood them, and that x86 game-engine assembly does not survive a port to ARM.
**Common pitfall:** Premature micro-optimisation before profiling; equally, refusing to optimise hot paths because "the compiler will figure it out."

### Tactic — Increase concurrency (and the concurrency vs. parallelism distinction)
**Definition:** Doing multiple things during overlapping time windows. Conventional simplification: *concurrency = threads = single CPU interleaving*; *parallelism = processes = multiple CPUs at the same instant*.
**Why it matters:** The terminology distinction is exam-relevant *and* practically relevant: multi-core CPUs blur the line, and getting the model right informs whether you reach for threads, processes, or async event loops.
**Detailed explanation:** In a single-CPU world, processes are switched by context switches; threads inside one process share heap/code/data and are cheaper to switch. With multi-core CPUs the simplification breaks down: kernel-level threads on different cores actually run *in parallel*. The first design choice is whether threads are even the right tool — Apache uses a thread pool, but Lighttpd and Nginx use a single async event-driven thread (made possible by 2000s-era OS innovations like `kqueue`).
**Analogy:** Concurrency is one cook juggling several pans on one stove (interleaving). Parallelism is several cooks each at their own stove.
**Common pitfall:** Throwing threads at I/O-bound workloads when an async event loop would handle it with a fraction of the memory and zero contention.
**Related diagram:** `![Concurrency in reality on multi-core](../images/lecture_6/lecture_6_p27_page_concurrency_vs_parallelism_reality.png)`

### Tactic — Thread pool vs. spawn-per-request
**Definition:** Two thread-management strategies: (A) spawn a fresh thread for every request, (B) maintain a fixed-size pool and dispatch requests to idle workers.
**Why it matters:** Spawning is conceptually simple but creates unbounded resource consumption under load; pools cap the parallelism level and reuse expensive thread state.
**Detailed explanation:** Classical Apache and the Python code on pages 29–30 (the `Parent` class with 500 daemon worker threads, a `queue.Queue`, and a `threading.Lock`) implement pattern B. Pattern A is simpler to code but a known footgun under DoS — every malicious request is a new thread.
**Analogy:** Pool = a stable kitchen brigade. Spawn-per-request = hiring a new chef each time a customer walks in.
**Related diagram:** `![Spawn vs thread pool](../images/lecture_6/lecture_6_p28_page_spawn_thread_vs_thread_pool.png)`

### Tactic — Multiple copies of computations (read replicas, load balancers)
**Definition:** Duplicating the result of work, or the workers that do it, so that reads scale independently of writes.
**Why it matters:** It is the single most-used resource-side performance tactic in modern web stacks.
**Detailed explanation:** Read-write replica patterns (writes go to a primary, reads go to many read-only replicas) work well because read/write ratios are typically extremely skewed. ML inference is a textbook case: train rarely, serve predictions millions of times. Load balancers and server pools generalise the idea to whole servers.
**Example:** PostgreSQL streaming replication with a primary and three read replicas behind PgBouncer.

### CAP Theorem (Brewer 2000)
**Definition:** A distributed system can simultaneously guarantee *at most two* of: Consistency (every read sees the latest write or an error), Availability (every request gets some response), Partition tolerance (the system keeps working despite network partitions).
**Why it matters:** When a partition happens — and partitions *do* happen, that is fallacy #1 — you must consciously pick C or A.
**Detailed explanation:** Partition tolerance is non-negotiable in any real distributed system, so the practical choice is CP vs. AP. CP: refuse requests or time out under a partition (good for atomic reads/writes — e.g. payments). AP: serve possibly-stale data (good when eventual consistency is acceptable — e.g. Instagram feed). Segregation is the practical resolution: different components within the same product can sit on different sides — payment in CP, social feed in AP.
**Analogy:** During a power cut you have to choose: keep the freezer running (consistency of food state, no availability of light) or keep one light on (availability) but spoil some food (consistency lost).
**Common pitfall:** Treating CAP as a single global choice for "the system." It is per-component.
**Related diagram:** `![CAP theorem trade-off](../images/lecture_6/lecture_6_p35_page_cap_theorem.png)`

### PACELC Theorem (Abadi 2010)
**Definition:** An extension of CAP: if there *is* a Partition (P), choose Availability or Consistency (A/C); *Else* (E) — i.e. in normal operation — choose Latency or Consistency (L/C).
**Why it matters:** Even *without* a partition, replicated systems trade latency against consistency. PACELC names that always-on trade-off that CAP elides.
**Detailed explanation:** Synchronous replication waits for ack from N replicas (CE — strong consistency, higher latency). Asynchronous replication returns immediately (LE — low latency, stale reads possible). Classifying a system as e.g. "PA/EL" (Cassandra) or "PC/EC" (a single-region SQL DB) is a more honest description than just "AP" or "CP."
**Analogy:** CAP is "during an emergency, do you save the cat or the dog?" PACELC adds "...and *also*, on a normal Tuesday afternoon, are you spending money on cat food or dog food?"
**Related diagram:** `![PACELC theorem](../images/lecture_6/lecture_6_p38_page_pacelc_theorem.png)`

### Caching topologies (local vs. distributed; cache-aside vs. refresh-ahead; write-through vs. write-back vs. write-around)
**Definition:** A family of patterns for placing copies of data closer to readers and managing how those copies are filled and invalidated.
**Why it matters:** Caching is the dominant tactic for hiding read latency in modern systems, but each variant has a distinct consistency / data-loss trade-off.
**Detailed explanation:**
- **Local cache:** same machine, no network, fast but un-shared, limited scalability.
- **Distributed cache:** different machines, network required, shareable, scalable but slower per-access.
- **Cache-aside:** reads check cache; on miss, fetch from DB and write to cache. Writes go directly to DB (cache may be stale until next read). Read-heavy workloads; simple.
- **Refresh-ahead:** cache proactively refreshed on a schedule; reads always hit cache; designed to avoid latency spikes for trending data; only minimises misses for *hot* data.
- **Write-through:** writes go to cache *and* DB simultaneously; strong consistency, but slower writes.
- **Write-back:** writes go to cache only; DB updated later; fastest writes; risk of data loss if cache crashes.
- **Write-around:** writes bypass cache and go straight to DB; first read is slow (miss), subsequent reads are cached; good for write-heavy with rare reads.
**Analogy:** Cache-aside = "I only restock the fridge when I find it empty." Refresh-ahead = "I restock every Sunday whether or not the fridge is empty." Write-through = "I always write the same recipe in *both* my notebook and the fridge label." Write-back = "I only write the fridge label and update the notebook later." Write-around = "I always write the notebook and let the fridge label catch up when I next open the fridge."
**Common pitfall:** Choosing write-back without budgeting for the data-loss risk; choosing write-through without budgeting for the latency cost.
**Related diagrams:**
- `![Cache-aside vs refresh-ahead](../images/lecture_6/lecture_6_p40_page_cache_aside_vs_refresh_ahead.png)`
- `![Write-back / write-through / write-around](../images/lecture_6/lecture_6_p41_page_write_back_through_around.png)`

### Tactic — Bound queues
**Definition:** Capping the maximum number of queued events; deciding policy when the cap is exceeded.
**Why it matters:** An unbounded queue under sustained overload becomes a memory leak that fails much harder than a bounded queue would have.
**Detailed explanation:** Simple to implement but the *overflow policy* is the real design choice: drop, drop-stochastically (Cho 1999), shed lowest-priority, or apply back-pressure to upstream. Ruohonen's snippet:
```python
def enqueue(self, events, max=1000):
    k = max(len(events), max)
    for i in range(k):
        self.queue.put_nowait(events[i])
```
**Common pitfall:** Bounded *with no policy* — just throwing an exception that the caller does not handle gracefully.

### Tactic — Schedule resources (CPU schedulers, FIFO, SJF, EDF, rate-monotonic, idle, batch, round-robin)
**Definition:** Deciding *which* runnable task gets a resource (CPU, disk, IRQ) *when*.
**Why it matters:** Context switches are expensive; the scheduler choice directly determines tail latency.
**Detailed explanation:**
- **Poor CPU scheduler:** rotates Tasks A→E in lockstep across all CPUs — every CPU does context switch at the same moment.
- **Better CPU scheduler:** keeps each task on one CPU for a longer slice; fewer context switches; better cache locality.
- **Overlapping execution:** while Task B uses Disk, Task A and C run on CPU — overlap I/O and compute.
- **FIFO:** trivial, fair-ish, but a long job blocks the queue.
- **SJF (Shortest Job First):** minimises average waiting time when job durations are known.
- **EDF (Earliest Deadline First) / deadline-monotonic:** higher priority for shorter deadlines — basis of real-time schedulers.
- **Rate-monotonic:** priority based on task *period* (shorter period = higher priority).
- **Idle scheduler:** runs non-time-critical work only when system is idle.
- **Batch scheduler:** maximises throughput of background jobs (e.g. backups) at low priority.
- **Round-robin:** equal circular time slices per task — simple and used widely (e.g. DNS round-robin).
- **Semantic-importance scheduler:** priorities from domain (audio over video, say).
Granularity matters: DB writes scheduled in seconds, OS kernels schedule interrupts and processes in nanoseconds; `irqbalance` (page 56) does the latter.
**Analogy:** FIFO = the supermarket queue; SJF = the express lane; EDF = the ER triage on imminent-death basis; round-robin = a kindergarten taking turns on the swing.
**Common pitfall:** Fair scheduling is the default but is the *wrong* default for hard real-time systems where missing a deadline = system failure (Ruohonen's car-brake example).
**Related diagrams:**
- `![Better CPU scheduler](../images/lecture_6/lecture_6_p47_page_better_cpu_scheduler.png)`
- `![Earliest-Deadline-First](../images/lecture_6/lecture_6_p53_page_earliest_deadline_first.png)`

### Throttling Pattern (via Circuit Breaker)
**Definition:** A performance pattern that limits resource usage when a measured load crosses a threshold, typically implemented with a circuit breaker state machine: Closed (normal) → Half-open (throttling / graceful degradation) → Open (errors only).
**Why it matters:** It is the most common production answer to "we cannot serve all this traffic" — and it has subtle failure modes if used naively.
**Detailed explanation:** In the Closed state the breaker passively measures load. When the threshold is crossed the breaker moves to Half-open, where load is reduced via graceful degradation (lower fidelity, fewer features, sampling). If degradation succeeds the breaker returns to Closed; if load worsens it trips Open and clients receive errors immediately. With cloud computing the breaker can be combined with *dynamic scaling*: instead of throttling at threshold crossing, allocate more capacity. Both halves of the dual ("scale up vs. throttle down") have costs: scaling up costs money and time; scaling down or throttling costs QoS and may cut off availability.
**Critical refinements:**
- **Exponential back-off:** every retry by a client waits exponentially longer; absorbs retry storms.
- **Jitter:** add randomness to back-off (and even normal requests) so that retrying clients do not synchronise into a thundering herd. (Brooker 2019.)
- **Layered queries:** internal layers also retry; a single user-facing failure may produce many internal retries, multiplying load.
**Analogy:** A nightclub bouncer. Closed door = normal operation. "Slow down, only ten at a time" = half-open / throttling. "Closed for the night" = open. Adding a second bouncer is dynamic scaling.
**Common pitfall:** Naive retries without back-off + jitter — the classic retry storm that turns a partial outage into a full one.
**Related diagrams:**
- `![Throttling via circuit breaker](../images/lecture_6/lecture_6_p61_page_throttling_with_circuit_breaker.png)`
- `![Throttling combined with dynamic scaling](../images/lecture_6/lecture_6_p63_page_throttling_plus_dynamic_scaling.png)`

### MapReduce (Dean & Ghemawat 2008)
**Definition:** A parallel-processing pattern where a *Map* step distributes work over many workers (each reading a split of input and emitting key/value pairs) and a *Reduce* step aggregates the per-key intermediate results into a final dataset.
**Why it matters:** Even with effectively unlimited cloud resources, algorithmic discipline still matters — MapReduce is the canonical example of using simple primitives (map, reduce) to make big data tractable.
**Detailed explanation:** The main process forks N workers; each worker locally reads its split of the input files, processes it, and writes intermediate results remotely. A reducer worker reads the remote intermediates and writes a single output file. The pattern scales horizontally because workers don't depend on each other within a phase.
**Analogy:** Counting votes in a national election: each polling station (mapper) counts its own ballots and reports a tally; a central office (reducer) sums the tallies.
**Common pitfall:** Applying MapReduce to problems where the dependencies between records are not key-aligned — most graph problems, for example, fight the model.
**Related diagram:** `![MapReduce](../images/lecture_6/lecture_6_p71_page_mapreduce.png)`

### Claim-Check Pattern
**Definition:** Instead of sending a large payload over a network, send a small "claim-check" token that points to the payload in a shared store; the receiver retrieves the payload from the store using the token.
**Why it matters:** Triple win — performance (less network), reliability (network unreliability sidestepped), security (token can be cryptographically signed).
**Detailed explanation:** MapReduce aligns with this pattern: input data lives in a shared store, workers read locally and write intermediates that other workers later retrieve. More generally, any message bus that transports references to a blob store (e.g. S3) instead of the blob itself implements claim-check.
**Analogy:** A coat-check at a restaurant — you carry a paper tag, not the coat.
**Example:** An Azure Service Bus message carrying a SAS URL to a blob in Azure Storage; the receiver fetches the blob with the URL.
**Related diagram:** `![Claim-check pattern](../images/lecture_6/lecture_6_p72_page_claim_check_pattern.png)`

### Static/Dynamic Content Separation and Materialized Views
**Definition:** A web-tier performance pattern: serve static assets (images, JS, CSS, HTML) from one tier (often a CDN) and dynamic content from another. Materialized views additionally pre-compute heavy results and store them as separate tables.
**Why it matters:** Static content has different scaling, caching, and security profiles than dynamic content; mixing them on the same server wastes both.
**Detailed explanation:** CDNs (next lecture) push static content close to the user. Materialized views trade write latency / staleness for read latency — a costly SQL query becomes a row lookup.
**Example:** A dashboard whose "daily sales by region" tile is backed by a nightly-refreshed materialized view, not a live aggregate query.

### Database Performance Patterns
**Definition:** A catalogue of database-specific tactics: caching, read replicas, sharding, indexing, lock debugging, batched simultaneous writes, connection pools, query optimisation.
**Why it matters:** "Databases are a commonplace bottleneck" (page 74). Ruohonen flags this as a separate sub-area because most of the other tactics interact with database behaviour.
**Detailed explanation:**
- **Sharding:** horizontal partitioning by key (e.g. European users on one shard, Asian on another).
- **Indexing:** secondary B-tree / hash structures that turn O(n) scans into O(log n) lookups — at the cost of slower writes.
- **Locking debug:** know how your DB takes row vs. table locks, when deadlocks form, and how the engine resolves them.
- **Batched writes:** amortise per-statement overhead.
- **Connection pools:** TCP + auth handshake per request is expensive; pool and reuse.
- **Query optimisation:** read query plans, fix N+1s, push predicates down.

## Important diagrams (catalog)

- `lecture_6_p06_page_performance_scenario_template.png` — Bass-style 6-slot Performance scenario template with Source/Stimulus/Artifact/Environment/Response/Response-Measure value lists.
- `lecture_6_p11_page_performance_tactics_tree.png` — The full Performance Tactics taxonomy: Control demand (6 tactics) vs. Manage resources (6 tactics).
- `lecture_6_p15_page_limit_responses_drop_vs_queue.png` — Two basic limit-responses solutions: drop new excess events vs. queue them for later.
- `lecture_6_p18_page_priority_vs_stochastic_fairness_queueing.png` — Priority queueing vs. stochastic fairness queueing (random queue selection per event).
- `lecture_6_p27_page_concurrency_vs_parallelism_reality.png` — How multi-core CPUs actually run threads both concurrently *and* in parallel, undermining the conventional simplification.
- `lecture_6_p28_page_spawn_thread_vs_thread_pool.png` — Spawn-per-request thread strategy vs. fixed-size thread pool with worker selection.
- `lecture_6_p35_page_cap_theorem.png` — The CAP theorem trade-off diagram: under a network partition, choose CP (refuse / time out) or AP (serve stale).
- `lecture_6_p38_page_pacelc_theorem.png` — The PACELC decision tree: Partition? Yes → C or A; No (Else) → L or C.
- `lecture_6_p40_page_cache_aside_vs_refresh_ahead.png` — Cache-aside vs. refresh-ahead caching strategies with read/write/consistency/use-case rows.
- `lecture_6_p41_page_write_back_through_around.png` — Write-back / write-through / write-around cache write strategies side-by-side.
- `lecture_6_p47_page_better_cpu_scheduler.png` — A better CPU scheduler that keeps a task on one CPU longer to reduce context switches.
- `lecture_6_p53_page_earliest_deadline_first.png` — Earliest-Deadline-First (deadline-monotonic) scheduling: event `b` runs before `a` because `b`'s deadline is sooner.
- `lecture_6_p61_page_throttling_with_circuit_breaker.png` — Resource utilisation over time hitting a threshold and entering the half-open throttling period.
- `lecture_6_p63_page_throttling_plus_dynamic_scaling.png` — Combining throttling with dynamic resource allocation: when threshold is re-crossed, scale capacity up rather than open the breaker.
- `lecture_6_p71_page_mapreduce.png` — MapReduce reference diagram with main process, mappers reading input splits locally, remote writes to reducer, and the output file.
- `lecture_6_p72_page_claim_check_pattern.png` — Claim-check pattern: sender stores payload locally, sends only a token over the network, receiver retrieves payload using the token.

## Exam-relevant takeaways

- **Performance ≠ Scalability.** Performance is "do more with what you have"; Scalability is "add resources proportionally." A purist Performance answer never says "add servers."
- **Two basic measures are Latency and Throughput.** Any Performance scenario without a *statistic* (median, P99, mean) and a *unit/scale* is incomplete.
- **The six-slot scenario template is universal across QAs**, but the value menus on page 6 are Performance-specific. Memorise the value lists for Stimulus (periodic/stochastic/sporadic/cyclic + weight), Environment (normal/peak/overload/emergency/degraded), and Response Measure (latency + jitter + failed-share + resource levels).
- **Performance Tactics Tree has two branches × six tactics each.** Know all twelve and be able to give a one-sentence example of each.
- **Limit-responses is a choice: drop vs. queue.** "Unbounded queue" is not an alternative — it is a deferred crash.
- **CAP forces a partition-time pick; PACELC names the always-on latency/consistency pick.** Classify systems by both letters (e.g. PA/EL, PC/EC).
- **There are five named cache patterns to be able to distinguish:** cache-aside, refresh-ahead, write-through, write-back, write-around. Each has a different consistency / data-loss / latency profile.
- **Scheduler choice is a performance tactic.** Know at minimum: FIFO, SJF, EDF (deadline-monotonic), rate-monotonic, idle, batch, round-robin, semantic-importance.
- **Throttling is normally implemented via the Circuit Breaker pattern** with Closed → Half-open (throttling) → Open states; pair it with exponential back-off + jitter to absorb retry storms.
- **Layered architectures amplify retry storms.** Internal layers also retry, so one client failure can spawn many internal calls.
- **MapReduce is the canonical algorithmic counter-example** to "just add resources" — even with infinite cloud capacity, the right map/reduce decomposition still wins.
- **Claim-check pattern**: send the token, not the payload. Improves performance, reliability, *and* security.
- **The Eight Fallacies of Distributed Computing** underlie virtually every Performance tactic for distributed systems — be able to list them.
- **Databases are the bottleneck**: caching, read replicas, sharding, indexing, locking debug, batched writes, connection pools, query optimisation.

## Cross-references

- **Lecture 2 (Quality Attributes / scenarios / ASRs / ISO 25010):** The 6-slot scenario template introduced in L2 is reused verbatim here with Performance-specific value menus. The "Performance Efficiency" characteristic in ISO 25010 (sub-characteristics: time behaviour, resource utilisation, capacity) maps directly onto this lecture.
- **Lecture 1 (Layered architecture / SOLID):** The page-65 remark that "layered architectures contribute to the [retry-storm] problem" connects directly to layering as introduced in L1 — performance is one of the costs of strict layering.
- **Lecture 3 (Modifiability / Integrability):** "Reduce overhead" explicitly trades against maintainability (wrappers, filters, pipe stages); "Increase efficiency" trades against portability (assembly vs. C). Every Performance tactic should be reviewed for its Modifiability impact.
- **Lecture 4 (Testability / Deployability):** Deployment patterns (blue-green, canary, rolling) interact with throttling because half the strategy during an incident is "back out the change" — and that requires testable, observable, deployable rollback.
- **Lecture 5 (presumed — fault tolerance / availability):** Circuit breaker state diagram on page 57–58 and the consistency-types recap on page 33 are explicitly described as "from the previous lecture", so Lecture 5 must have covered availability, fault tolerance, circuit breakers, and consistency classes (eventual / quorum / synchronised). Lecture 6 leans on all of those.
- **Lecture 7 (next, implied):** Scalability patterns (service meshes, load balancers, CDNs) and dynamic resource allocation are deferred. Throttling-with-dynamic-scaling on page 63 already foreshadows it.
- **Case studies:** Case #5 (Hystrix as Netflix fault tolerance) primes the circuit-breaker / throttling material; Case #6 (online auction in India) is explicitly a Performance scenario + CAP exercise — exactly the framework introduced in pages 6, 11, and 34.
