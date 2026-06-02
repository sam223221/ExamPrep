# Chapter 17 — Exam Preparation: Question Archetypes, Walkthrough Strategies, Drawing Conventions, and the Soft-Skill Section

> **Read this in the 48 hours before the exam.** It is a tactical chapter. It assumes you have already read Chapters 1–16 at least once. If you haven't — close this file, go read at minimum Ch 1 (definitions), Ch 2 (QA scenarios), Ch 7 (availability tactics), Ch 8 (performance/scalability/CAP), and Ch 13 (tactics-tree comparison). Then come back.

---

## 1. Exam logistics (the hard facts)

These come from Lecture 10, page 2 — the lecturer's own briefing.

| Item | Value |
|---|---|
| Number of questions | **16** |
| Total points | **34** |
| Passing threshold (grade 2) | **17 points** (i.e. ~50 %) |
| Per-question worth | **1, 2, 3, 4, or 5 points** |
| Re-exam format | **Same** — 16 / 34 / 17 |
| Smartphones | **Allowed** — but only for digitising your hand-drawn diagrams (photograph the paper, upload). Not for browsing. |
| Allowed source material | Anything that appeared **in the lectures**. |
| **Slides alone are NOT enough** | You must be able to **apply** what is on them. The lecturer said this twice. |

### What "apply" means in practice

The lecturer's pedagogy is built around moving from *recognition* (you can recite a definition) to *application* (you can deploy it on a fresh scenario you've never seen). Concretely:

- You will not be asked "what is a QA scenario?" — you will be asked to **fill the six slots** for a brand-new system you have never seen.
- You will not be asked "what is the saga pattern?" — you will be asked to **walk a flight + hotel booking through one**, including the compensating actions.
- You will not be asked "what is PACELC?" — you will be asked to **classify Cassandra, Spanner, MongoDB, etc.** using it.

### Time and pacing

34 points across ~120 minutes (typical Finnish-Estonian university exam length) ≈ **~3.5 min per point**. Translate that to your per-question budget:

| Worth | Time budget | What that buys you |
|---:|---:|---|
| 1 pt | ~3 min | One definition, one labelled term, one row of a table. |
| 2 pt | ~7 min | A short definition + an example, or a 2-element list with reasoning. |
| 3 pt | ~10 min | A six-slot scenario, or a six-row pattern-comparison table, or a small drawing. |
| 4 pt | ~14 min | A tactics-tree sketch with labels, or a saga walkthrough. |
| 5 pt | ~18 min | A multi-step walkthrough (packet trace, MLOps pipeline), or a small reference architecture. |

### Over-answering = zero points

A recurring lecturer emphasis: a question worth 1 point gets ~3 minutes and ~3 lines. **Do not** write a paragraph for a 1-point definition; you are stealing time from your 5-pointer. Mark each answer's worth in the margin before you start, and budget accordingly.

---

## 2. The soft-skills warning (Lecture 1)

The lecturer boldfaced this:

> **The top three job qualities of a software architect are communication-related** — articulation, stakeholder management, communication/negotiation. Pure technical skill is necessary but insufficient.

This is exam-counted. Expect at least one written-discussion question, almost certainly in the 2–3 point band, on the *non-technical* side of the architect's role. The lecturer's framing is roughly "architects are 70 % communicators." Be ready to defend that claim, with examples.

### Likely soft-skill prompts

- "Why are the top three qualities of a software architect communication-related? Give one technical example per quality."
- "An architect proposes pattern X but the dev team prefers Y. Walk through how the architect should resolve this."
- "Explain why views and viewpoints exist primarily for communication, not for the architect's own use."
- "Give a scenario where the *correct* architectural decision is the *wrong* social move."
- "What is enterprise architecture and why is it more communication-heavy than system architecture?"

### How to answer

Use the **STAR** skeleton — Situation, Task, Action, Result — even when not explicitly asked.

- **Situation:** ground in a concrete scenario from the lectures (flight+hotel, MLOps, Linux network stack, hospital ER system).
- **Task:** state the architect's specific responsibility.
- **Action:** name the artifact produced (a view, a viewpoint declaration, a written ADR, a stakeholder workshop, an ATAM session).
- **Result:** state the trade-off that was made explicit, and who now understands it.

Architecture exams reward **articulation** of trade-offs over recitation of patterns. Always name the QA you are trading away, not just the one you are buying.

---

## 3. Question archetype catalog

Twelve archetypes, sorted high-yield first. For each: example phrasing, the model answer (skeleton), what to write or draw, and the common pitfall.

### 3.1 "Fill the 6 QA scenario slots for [QA]" — VERY HIGH YIELD

> *Example phrasing:* "Write a complete availability scenario for an in-flight booking microservice."

**Model answer** — six slots, label each:

| Slot | Example value |
|---|---|
| **Source of stimulus** | An upstream payment gateway |
| **Stimulus** | Returns HTTP 503 |
| **Artifact** | The booking service's payment-confirmation step |
| **Environment** | Normal operation, peak load |
| **Response** | Circuit-breaker opens; fall back to a queued retry |
| **Response measure** | ≥ 99.9 % bookings still complete within 30 s |

**What to write:** a two-column table. Six rows. Done.
**Pitfall:** Skipping *environment* and *response measure*. Without a quantified measure ("99.9 %", "30 s", "5 req/s"), the scenario is not testable and the lecturer will dock you. Always include numbers in the measure slot.

### 3.2 "Draw the tactics tree for [QA]" — HIGH YIELD

> *Example phrasing:* "Draw the availability tactics tree. Label at least two tactics per branch. Pay particular attention to the Reintroduce branch."

**Model answer (Availability):**

```
                          Availability
                               |
   +---------+--------+--------+-------------+-----------+
   |         |        |        |             |           |
 Detect   Recover-   Recover- Prevent    Reintroduce  Increase
 faults   Preparation Reintro faults     (from L7,    competence
          & Repair                       L13)
   |         |        |        |             |           |
 - Ping    - Voting  - Shadow - Removal   - Shadow    - Training
 - Heart-  - Active  - State   from        - State     - Process
   beat      redund.   resync  service     resync        improve-
 - Timeout - Passive - Escal. - Trans-                   ment
 - Sanity    redund.   restart  actions
   check
```

**What to draw:** a tree, root at top. **Label every branch**. Sketch ≥ 2 leaves per branch (the lecturer's minimum). Be especially crisp on *Reintroduce* — that branch is the lecture's favourite "did you actually study?" probe.

**Pitfall:** Drawing tactics in a flat list rather than a hierarchy. The structure *is* the answer; without branches you are claiming "all tactics are equal," which is wrong.

### 3.3 "Distinguish Performance vs Scalability" — Mock Q8

> *Example phrasing:* "Mock question 8: distinguish performance from scalability. Two paragraphs maximum."

**Model answer (~4 sentences):**

> *Performance* is about how fast a fixed load is served — latency, throughput, deadlines. *Scalability* is about how performance behaves as load grows — vertically (bigger box) or horizontally (more boxes). A system can be performant but not scalable (e.g. a single fast monolith that falls over at 10× load), and scalable but not performant (e.g. a horizontally elastic system whose per-request latency is high). They share tactics — caching, replication, throttling — but the *response measure* differs: performance asks "how fast for N?", scalability asks "what happens when N becomes 100 N?".

**Pitfall:** Conflating them. The lecturer is allergic to "scaling improves performance" without qualification.

### 3.4 "Compare Observer vs Publish-Subscribe" — six-row table

> *Example phrasing:* "Compare the Observer pattern with the Publish-Subscribe pattern across at least six dimensions."

**Model answer (six-row table):**

| Dimension | Observer | Publish-Subscribe |
|---|---|---|
| Coupling | Subject knows its observers (by reference) | Publisher and subscriber don't know each other |
| Broker | None | Mandatory (event bus, topic) |
| Topology | 1-to-many within one process | many-to-many across processes/machines |
| Filtering | Observers receive everything from their subject | Topics / content-based filtering at broker |
| Delivery guarantee | Synchronous, in-process call | Async; depends on broker QoS (at-most/at-least/exactly-once) |
| Failure mode | Slow observer slows subject | Slow subscriber slows only itself (broker buffers) |

**Pitfall:** Stopping at 3 rows. The lecturer asked for *six*; deliver six.

### 3.5 "Classify [system] under PACELC"

> *Example phrasing:* "Classify Cassandra, Spanner, and DynamoDB under PACELC."

**Model answer:**

| System | Partition behaviour | Else behaviour | Code |
|---|---|---|---|
| Cassandra | AP (favours availability) | EL (favours latency) | **PA/EL** |
| Spanner | CP (favours consistency) | EC (favours consistency) | **PC/EC** |
| DynamoDB (default) | AP | EL | **PA/EL** |
| MongoDB (default) | CP | EC | **PC/EC** |

**Pitfall:** Forgetting the *else* half. CAP is a subset of PACELC; PACELC adds "what about when there's NO partition?" — that's the *EL vs EC* axis. Both halves must be filled.

### 3.6 "Walk through the saga pattern for flight + hotel booking"

> *Example phrasing:* "Walk through a choreographed saga for the flight + hotel booking system. Show happy path and one failure case with compensating actions."

**Model answer (sequence):**

```
Happy path:
  1. BookingService     -> FlightService:  reserveFlight(...)        => OK
  2. BookingService     -> HotelService:   reserveHotel(...)         => OK
  3. BookingService     -> PaymentService: charge(...)               => OK
  4. BookingService     -> User:           confirmation

Failure (hotel unavailable after flight reserved):
  1. reserveFlight(...) => OK
  2. reserveHotel(...)  => FAIL
  3. COMPENSATE:        FlightService.cancelReservation(...)
  4. Notify user: "hotel unavailable; flight released; no charge"
```

Then add one sentence on each: *atomicity is sacrificed for availability*, *compensations are application-level — not database rollbacks*, *idempotency is required because a compensation might be retried*.

**Pitfall:** Forgetting that compensating actions are **business-level inverses**, not technical rollbacks. "We DELETE'd the row" is wrong — the right framing is "we issued a `cancelReservation` which has its own audit trail and may have side effects (refund, seat re-release)".

### 3.7 "Identify the inconsistency in this diagram"

This is the lecturer's favourite pedagogical move: present a diagram with a deliberate flaw and ask you to spot it.

> *Example phrasing:* "Three things are wrong with the component diagram on the next page. Identify and explain each."

**Common planted flaws:**

- Required interface drawn as a full lollipop (it should be half-open / socket).
- A component owns a database **and** the DB has an arrow back to the component — circular ownership.
- A layered diagram with a skip-layer arrow (L4 → L1).
- A microservice diagram with a shared database between two services (violates database-per-service).
- A pub-sub diagram where the publisher has a direct reference to a named subscriber (defeats the decoupling).
- A 4+1 view labelled "logical" but actually showing deployment (process vs node confusion).

**What to write:** A numbered list. One line per flaw: *what* is wrong, *which principle/pattern* it violates, *what should it be instead*.

**Pitfall:** Spotting only one. Read the question — if it says "three things," there are three. Look for the third.

### 3.8 "What's wrong with this LLM-only verification pipeline?"

(From the MLOps / LLMOps thread — Ch 12 / Ch 16.)

> *Example phrasing:* "An ML team proposes that the test stage of their CI/CD pipeline consists solely of asking an LLM 'does this code look correct?'. Critique."

**Model answer points:**

- LLMs hallucinate — no determinism, no reproducibility.
- No oracle: the LLM has no spec to verify against; it pattern-matches against its training distribution.
- No coverage measure: classical tests give branch / line coverage; "looks correct" has none.
- Security blind spot: an LLM may approve code containing CVEs it's never seen.
- Cost / latency: gating every commit on an LLM call is expensive and slow.
- Correct move: LLM as **advisor**, not gate. Real tests (unit, integration, fuzz, SAST) remain the gate.

**Pitfall:** Just saying "LLMs hallucinate" and stopping. That's worth ~1 point of the 3 on offer. Enumerate.

### 3.9 "Trace a TCP segment from socket to wire" — Case 1

> *Example phrasing:* "A user-space program calls `send()`. Trace the TCP segment through the Linux network stack until it leaves the NIC."

**Model answer (skeleton):**

1. `send()` → `sys_sendmsg()` (syscall boundary; user → kernel).
2. Socket layer dispatches by protocol family (AF_INET) → TCP.
3. `tcp_sendmsg()` copies user buffer into `sk_buff` (skb), splits along MSS.
4. TCP transmit queue; congestion-window check; Nagle / TSO.
5. `ip_queue_xmit()` — routing decision, fills IP header, fragments if needed.
6. Netfilter chains (OUTPUT, POSTROUTING) — iptables/nftables hooks.
7. Qdisc (queueing discipline) — pfifo_fast, tc.
8. NIC driver `ndo_start_xmit()` — DMA the skb to the ring buffer.
9. NIC raises descriptor; signals frame complete; interrupt or NAPI poll.
10. Frame on the wire.

**Pitfall:** Missing Netfilter (the lecturer specifically uses Netfilter as the pipe-and-filter example in Ch 15). Always name it.

### 3.10 "Design a reference architecture for [domain]"

> *Example phrasing:* "Sketch a reference architecture for a small online taxi-booking platform. Identify three quality attributes you optimise for."

**Model answer:**

1. **Declare your three prioritised QAs** in one sentence (e.g. *availability > scalability > security > everything else*).
2. **Draw the views** — at minimum a component view (services, databases, brokers) and a deployment view (which node runs what).
3. **Label patterns** explicitly: "Gateway", "Database-per-service", "Saga", "Pub-Sub".
4. **Mark the trade-offs.** Where did you sacrifice consistency? Cost? Modifiability?
5. **One paragraph of justification** — why this shape, given those QAs.

**Pitfall:** Drawing only one view. The whole course is built on "no single diagram is the architecture." Show two.

### 3.11 "Critique this architectural decision against [QA]"

> *Example phrasing:* "A team replaces all REST calls with synchronous gRPC. Critique against availability."

**Model answer skeleton:**

- Restate the QA scenario (one short scenario for the QA).
- Identify the tactics affected (here: tactics for "fault detection" and "recover-preparation"; synchronous coupling defeats *bulkhead* and *circuit-breaker* unless explicitly re-added).
- Identify the *positive* affected QA (likely performance / interoperability).
- State the trade-off in one sentence.
- Recommend a mitigation (per-call deadline, circuit breaker around the gRPC client, async streaming where possible).

**Pitfall:** Only listing downsides. A critique that doesn't acknowledge the gain is not a critique, it's a rant. The lecturer rewards balanced trade-off framing.

### 3.12 "What new QA would you introduce for [scenario]?"

> *Example phrasing:* "A hospital is integrating an LLM into triage. ISO/IEC 25010 has nine top-level QAs. What new one would you propose?"

**Model answer:**

Name a *candidate* QA, justify why none of the 25010 categories cover it cleanly. Examples:

- **Verifiability of generated output** (LLM systems).
- **Energy proportionality** (data-centre / edge ML).
- **Explainability** (any ML-in-the-loop decision system).
- **Auditability** (regulated industries beyond what "security/non-repudiation" covers).
- **Recoverability of meaning** (when the model is replaced and outputs change).

State: definition, candidate sub-QAs, response measure, why it is *not* already covered by an existing 25010 category.

**Pitfall:** Picking a QA that *is* already in 25010 (e.g. "maintainability" — that's already there). Read the list first.

---

## 4. Walkthrough strategies

### 4.1 How to attack a scenario question

1. **Skim** the prompt and underline the QA being asked about.
2. **Draw a 6-row table** with the slot labels in the left column. Even before you know the values, the table earns layout marks.
3. **Fill source / stimulus first** (they're usually the easiest).
4. **Artifact** — name a specific component, not "the system".
5. **Environment** — normal? peak? degraded? boot? Specify.
6. **Response** — verb + object. "Logs the event", "fails over to replica B".
7. **Response measure** — a *number with a unit*. If you only have a vague target, write "within X seconds, X to be determined by SLA" — still gets partial credit.

### 4.2 How to attack a "draw the tactics tree" question

1. Write the QA name in a box at the top centre.
2. Draw **5 branches** for the canonical QAs: Availability, Performance, Modifiability, Security, Testability all have ≥ 4 branches in Bass et al.
3. Label each branch even if you can't fill leaves yet — branches alone earn ~30 % credit.
4. Add ≥ 2 leaves per branch. Pick the ones you remember best, not the ones you "should" know.
5. Anchor on the lecture's tree (Ch 7, Ch 13). If you blank out, *anchor on the Reintroduce branch* for availability — it's the lecturer's pet.
6. Star (★) any leaf that the lecturer reused as a pattern (e.g. circuit breaker under Recover-Preparation).

### 4.3 How to attack a trade-off question

The template is three sentences:

> "Buying **X** costs us **Y**. Specifically, [tactic / pattern] improves [QA-1] by [mechanism] but degrades [QA-2] because [mechanism]. We accept this because [QA-1 priority] > [QA-2 priority] in this system."

Memorise that shape. Then drop the system's specific values into the slots. Every trade-off question in the lecture series fits this template.

### 4.4 How to attack a "what's wrong" question

1. Count what the prompt says ("three things wrong" → look for three).
2. Scan in a fixed order: *interfaces (lollipops), arrows (direction, sync/async), shared resources (DBs, queues), layer violations, missing components (no gateway, no broker)*.
3. Write one line per flaw with the violated principle named.

### 4.5 General tactic — start with the easy points

Walk the paper end-to-end on the first pass and answer everything worth 1–2 points. That secures your floor (you can lock in ~12 points of safe credit fast). Then go back to the 4s and 5s, where points are concentrated but failure modes are bigger.

---

## 5. Drawing conventions (one-page reference)

The exam requires drawing on paper, photographing with your phone, and uploading. Practise these conventions until they are automatic.

### 5.1 Components, connectors, interfaces

```
       provided interface (full lollipop)
              o
              |
        +-----+-----+
        |           |
        | Component |
        |           |
        +-----+-----+
              |
              C            <- required interface (half-open / socket)
       required interface
```

- **Full lollipop ●** = **provided** interface (the component offers this).
- **Half-open lollipop / socket ◖ or `C`** = **required** interface (the component needs this from someone else).

### 5.2 Connectors

```
   Synchronous (solid arrow, filled head)
   A ────────────►  B

   Asynchronous (open / stick arrow)
   A ────────────▻  B

   Bidirectional / data flow
   A ◄──────────►  B
```

Pick **one** convention and use it consistently. The lecturer's exact words from L1: "any style works as long as you're consistent."

### 5.3 Environments and deployments

```
   +─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ +
   .   Kubernetes cluster (environment)         .
   .                                            .
   .   +─ ─ ─ ─ ─ ─ ─ +     +─ ─ ─ ─ ─ ─ ─ +    .
   .   .  Pod: web     .    .  Pod: db     .    .
   .   .  +─────────+  .    .  +────────+  .    .
   .   .  │ nginx   │  .    .  │ pg     │  .    .
   .   .  +─────────+  .    .  +────────+  .    .
   .   +─ ─ ─ ─ ─ ─ ─ +     +─ ─ ─ ─ ─ ─ ─ +    .
   +─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ +
```

- **Dashed boxes** = environments / boundaries (cluster, VM, namespace, network zone).
- **Solid boxes** = concrete elements (components, processes, machines).
- Nest environments freely — the dashed-vs-solid contrast carries the meaning.

### 5.4 Layers

```
   +─────────────────────────────────────────+
   │  L4: Application                        │
   +─────────────────────────────────────────+
   │  L3: Middleware / Framework             │
   +─────────────────────────────────────────+
   │  L2: OS Services                        │
   +─────────────────────────────────────────+
   │  L1: Kernel                             │
   +─────────────────────────────────────────+
   │  L0: Hardware                           │
   +─────────────────────────────────────────+
```

- **Stacked rectangles**, no overlap.
- A strict layered architecture allows **only neighbour-to-neighbour** arrows (L4 ↔ L3 ↔ L2 …). If you draw a skip-layer arrow, you must explicitly label it "relaxed layering".

### 5.5 Sequence diagrams (for sagas, walkthroughs)

```
   User       Booking      Flight     Hotel
    │           │             │         │
    │ book ───► │             │         │
    │           │ reserve ──► │         │
    │           │ ◄──── OK    │         │
    │           │ reserve ──────────► │
    │           │ ◄──── FAIL ─────────│
    │           │ cancel ───►│         │
    │           │ ◄── OK     │         │
    │ ◄── fail  │             │         │
```

- Vertical lines = lifelines.
- Horizontal arrows = messages (sync = solid, async = open head).
- For sagas, **always** show at least one failure path with the compensating action.

### 5.6 Tactics trees

Top-down hierarchy, root QA at top, branches labelled (Detect / Recover-Prepare / Recover-Reintroduce / Prevent / Reintroduce / Competence — the exact set varies by QA), leaves at the bottom.

### 5.7 4+1 views

```
                  +─────────────────+
                  │   Scenarios     │
                  +─────────────────+
                          ╱  │  ╲
                         ╱   │   ╲
   +─────────+   +─────────+ +─────────+   +─────────+
   │ Logical │   │Develop- │ │ Process │   │Physical │
   │ (devs)  │   │ ment    │ │ (ops)   │   │(network)│
   │         │   │ (PM)    │ │         │   │         │
   +─────────+   +─────────+ +─────────+   +─────────+
```

Label which **stakeholder** each view serves — this is the lecturer's emphasised twist.

---

## 6. What to memorise — 1-page cheat-sheet

### 6.1 Bass-Clements-Kazman definition (verbatim)

> "The **software architecture** of a computing system is the set of **structures** needed to reason about the system, which comprise software **elements**, **relations** among them, and **properties** of both."
> — *Bass, Clements & Kazman; quoted in the course via Clements et al. 2010 / Fairbanks 2010*

Lock this down word-for-word. The lecturer will recognise it.

### 6.2 The 10-term vocabulary

**module — interface — component — process — machine — system — deployment — environment — element — connector**

Mini-glosses:
- **module**: a source-code unit; static.
- **interface**: a named contract; provided or required.
- **component**: a runtime unit; black box at its boundaries.
- **process**: an OS-scheduled execution.
- **machine**: physical or virtual host.
- **system**: the set of components+connectors+environment that delivers the service.
- **deployment**: the binding of components to machines/environments.
- **environment**: the context (cluster, network zone, VM) where elements live.
- **element**: superset term (component **or** module — depends on view).
- **connector**: the relation between elements (call, queue, shared memory, network).

### 6.3 The 6-slot QA scenario template

```
Source ─► Stimulus ─► [Artifact under Environment] ─► Response (Response Measure)
```

| Slot | One-line definition |
|---|---|
| Source | Who/what triggers the stimulus |
| Stimulus | The thing that happens to the artifact |
| Artifact | The bit of the system under test |
| Environment | When/where the stimulus arrives |
| Response | How the system reacts |
| Response Measure | The quantified, testable target |

### 6.4 ISO/IEC 25010 top-level categories

1. **Functional Suitability**
2. **Performance Efficiency**
3. **Compatibility**
4. **Usability**
5. **Reliability**
6. **Security**
7. **Maintainability**
8. **Portability**
9. **(2023 revision adds) Safety**

(Note: the 2011 edition has 8; the 2023 revision adds *Safety*. The lecturer references both — be ready to say "8 or 9 depending on edition".)

### 6.5 Eight fallacies of distributed computing (Deutsch / Gosling)

1. The network is reliable.
2. Latency is zero.
3. Bandwidth is infinite.
4. The network is secure.
5. Topology doesn't change.
6. There is one administrator.
7. Transport cost is zero.
8. The network is homogeneous.

Mnemonic: **"R**eliable, **L**atency, **B**andwidth, **S**ecure, **T**opology, **A**dministrator, **C**ost, **H**omogeneous" → *RLBS-TACH*.

### 6.6 The "nines" table

| Availability | Annual downtime |
|---|---|
| 90 % | 36.5 days |
| 99 % | 3.65 days |
| 99.9 % ("three nines") | 8.76 hours |
| 99.99 % ("four nines") | 52.56 minutes |
| 99.999 % ("five nines") | 5.26 minutes |
| 99.9999 % ("six nines") | ~31.5 seconds |

Rule of thumb: each extra nine ≈ **10× less downtime**.

### 6.7 Postel's Robustness Principle

> "**Be conservative in what you send, be liberal in what you accept.**"
> — *Jon Postel, RFC 793 / RFC 1122*

Critique to remember: this principle is now controversial in security contexts (liberal parsing → ambiguity → attack surface). Be ready to discuss both the original argument and the modern pushback.

### 6.8 CAP and PACELC

**CAP (Brewer):** under a network **P**artition, choose **C**onsistency or **A**vailability. (You only choose under partition — without partition, you get both.)

**PACELC (Abadi):** *if* **P**artition then **A**vailability vs **C**onsistency; **e**lse **L**atency vs **C**onsistency.

| Class | Example |
|---|---|
| PA/EL | Cassandra, DynamoDB |
| PC/EC | Spanner, MongoDB (default) |
| PA/EC | (rare) |
| PC/EL | (rare) |

### 6.9 The kill chain (Lockheed Martin)

1. **Reconnaissance**
2. **Weaponisation**
3. **Delivery**
4. **Exploitation**
5. **Installation**
6. **Command & Control (C2)**
7. **Actions on Objectives**

Mnemonic: *"Really Wise Defenders Examine Incidents Carefully — Always."*

### 6.10 Running examples (use these in answers; the lecturer will recognise them)

| Example | Anchored in | Use it for |
|---|---|---|
| **Flight + hotel reservation** | L1, L7 | Saga, compensations, distributed transaction trade-offs |
| **Linux network stack** | Case 1, L15 | Layering, pipe-and-filter (Netfilter), kernel boundaries |
| **MLOps reference architecture** (Kreuzberger et al.) | Case 3, L16 | CI/CD, monitoring, drift, A/B, model registry |
| **Kubernetes cluster** | L9 | Sidecar, gateway, pod-as-deployment-unit, securityContext |
| **Hospital ER system** | L1 | System vs enterprise architecture distinction |

Don't be shy about reusing them. Naming a concrete example anchors your answer and signals that you actually attended.

### 6.11 Other small things worth a one-line recap

- **Twin Peaks** — requirements and architecture co-evolve; neither is finished first.
- **Conway's Law** — system structure mirrors org structure.
- **Liskov substitution for components** — replacement must *preserve* provided interfaces and must *not add* required ones.
- **Five component principles** — cohesion, segregation, single responsibility, open-closed, no vendor lock-in.
- **Fail-safe vs fail-secure** — *fail-safe* defaults to the safe (often open) state on failure (door unlocks in a fire); *fail-secure* defaults to the locked/protected state (vault stays locked on power loss). Give one example of each on the exam.
- **Graceful shutdown ≠ graceful degradation ≠ forceful degradation** — see L10 §Graceful degradation.
- **P-states vs C-states** — P-states scale frequency/voltage while active; C-states are idle/sleep levels. Both come from ACPI / BIOS.

---

## 7. Final pep talk

You are not being tested on whether you can remember slides. You are being tested on whether you can **apply** the architectural vocabulary to systems you have never seen before. That is a different skill, and it is the skill the lecturer cares about. Slides alone are not enough; you must apply.

Architecture exams reward **articulation**. The student who writes a tight six-row trade-off table beats the student who writes three rambling paragraphs. Name the QA you are buying; name the QA you are paying with; name the pattern that mediates between them; name one number that makes it testable. Then stop.

You have done the reading. Walk into the room, sketch your six-slot table on a fresh page before the first question even loads in your head, and **start with the easy points**. The first 17 are within reach; everything beyond that is upside.

Good luck — and remember to charge your phone the night before. You'll need it to photograph the drawings.
