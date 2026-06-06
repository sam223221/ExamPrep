# 08. Threat Modeling I

> Source material: `L08_Threat Modeling 1.pdf` (54 slides) and `E08.pdf` (Lab 08, 4 pages), Cybersecurity (F26), SDU Centre for Industrial Software, lecturer Sani Abdullahi, 25th March 2026. All citations point back to these two files: lecture slides are cited as `(L08 p.N)` and the lab as `(E08 p.N)`.

---

## Overview — what this topic covers and why it matters

Threat modeling is a **structured, repeatable process for finding security issues early** — ideally before a single line of code is written — rather than discovering them after release through bug reports or breaches (L08 p.7). The lecture frames it as a defensive engineering discipline, not "hacking": security is a *structured process (defense, not offence)*, with multiple roles beyond breaking into systems and soft skills that matter (L08 p.3). The central question the whole topic answers is: **"how can we ensure more secure software/systems?"** (L08 p.8). The claim is that you are *already* threat modeling whenever you develop or operate a system, just often implicitly; the goal of this discipline is to make that reasoning explicit, structured, and efficient (L08 p.8–9).

The lecture organises the material around a **four-step framework — Model System → Find Threats → Address Threats → Validate** (L08 p.16) — and fills each step with concrete tools: data flow diagrams (DFDs), swim lanes, state machines and other UML diagrams for *modelling*; attack libraries, STRIDE and attack trees for *finding* threats; mitigation strategies (mitigate / eliminate / transfer / accept) and prioritization (DREAD, risk matrices) for *addressing* threats; and quality-assurance checks for *validating*. It matters because threat modeling needs an **engineering approach — predictable, reliable, scalable to a large product, and practical** (L08 p.13), and because it is an ongoing process: you never cover every angle, systems change, and attack patterns evolve, so the process continues even for a deployed product (L08 p.53). The companion lab (E08) puts this into practice on an Android health app, asking students to build a DFD, apply STRIDE per element, and evolve both as the system grows into a cloud-connected fitness tracker.

---

## Key Concepts

### What threat modeling is and why do it early

**What:** Threat modeling is "a tool to improve security … by addressing predictable threats" (L08 p.9). Its success depends on how thorough you are, and structure plus efficiency are essential — you should focus on the big picture and not get lost in details (L08 p.9).

**Why:** The motivating rhetorical question is "Wouldn't it be better to find security issues *before* you write a single line of code?" (L08 p.7). Doing it early lets you think about security issues up front, understand your requirements better, avoid coding security issues in the first place, and informs how you monitor your system/deployment (L08 p.8).

**How (where it sits among other techniques):** Common ways to find security issues include static code analysis, fuzzing / dynamic testing, penetration testing / red team, attack–defence (red team / blue team) training, and waiting for bug reports after release (L08 p.7). Threat modeling is "Common ways to find security issues II" — the proactive, design-time complement to those reactive/testing methods (L08 p.8). Note: **fuzzing/fault injection is *not* a mitigation but a great testing technique** (L08 p.45).

**Threat modeling vs. penetration testing (from the lab):** Both involve threat assessment, but pen testers must *infer* system details through active and passive reconnaissance, whereas threat modeling is performed **with full system knowledge**, allowing a more structured and comprehensive evaluation of risks (E08 p.1).

### The three common threat-modeling approaches (attacker / asset / system)

The lecture lists three common approaches by what they focus on (L08 p.9):

1. **Models that focus on the attackers** — "Think like an attacker": what do they know, what will they do? (L08 p.10).
2. **Models that focus on the assets** — the valuable things the business cares about (L08 p.11).
3. **Models that focus on the software/system** — model the system itself (this is the approach the rest of the lecture develops via DFDs + STRIDE) (L08 p.9).

**Problems with "think like an attacker" (attacker-centric):** It is *risky* — if you get the attacker's knowledge/intent wrong, your whole threat model goes astray; and you already know a great deal about the system anyway. The advice is "don't *start* from attackers (maybe)!" but still keep them in mind for different scenarios (L08 p.10).

**Problems with starting from assets (asset-centric):** Assets are valuable things the business cares about, but there is a "risk of perspective" — do you *really* know the asset? An asset can be (a) something an attacker wants, (b) something you want to protect, or (c) a stepping stone — these are **overlapping definitions** (L08 p.11). It is hard to judge what an attacker will want (e.g., maybe they just want a random computer to serve pirated music — so what do you protect?). It depends on the attacker/scenario, and you might decide *everything inside the perimeter* matters because every computer is a stepping stone to the inner sanctum. What you actually learn from making an asset list is **how to set up your defences** (L08 p.12).

### The four-step threat modeling framework (Threat Modeling Flow)

**What:** The core process the lecture uses is a four-step framework (L08 p.16):

1. **Model System** — rewrite/represent your system to enable analysis.
2. **Find Threats** — identify threats in the model.
3. **Address Threats** — decide how to deal with each threat found.
4. **Validate** — quality assurance for the threat model.

This is repeated as the spine of the whole lecture (L08 p.13, 16, 24, 42, 49, 53). It "needs an engineering approach": **predictable, reliable, scalable (to a large product), and practical** (L08 p.13).

**OWASP variant:** The slides also present the OWASP Threat Modeling cycle as a loop: **start → Application Overview → Decompose Application → Identify Threats → Identify Vulnerabilities →** (back to Application Overview) (L08 p.13). This is a cyclic, continuous version of the same idea.

**Key reminder:** It is a *process* — you never cover every angle, your system changes over time, attack patterns change, and new attacks come into focus; the process can continue even for the deployed product (L08 p.53).

### Modeling the system (diagramming methods)

**What/Why:** "What are you building/developing?" — you create a *model* of the software/system/technology. A model **abstracts away detail so you can look at the whole**, and **diagramming is the key approach**. Mathematical/formal models are rare in commercial environments (L08 p.14).

**How — structured "formal" diagram types** (L08 p.14):

- **Data flow diagrams (DFDs)** — the primary method (detailed below).
- **Swim lanes** — entities communicating, each in a lane.
- **State machines** — what changes the *security state*.
- **Other UML diagrams** — any UML diagram can be adapted.

### Data Flow Diagrams (DFDs)

**What:** A DFD abstracts a program into four element types (L08 p.17). DFDs were developed in the early 1970s and are still useful because they are **simple (easy to learn and sketch)** and because **threats often follow data** (L08 p.17).

**The four DFD element types** (L08 p.17):

- **Processes** — *your code*. (Drawn as a rounded rectangle or a circle; a *multi-process* uses a double circle.)
- **Data stores** — files, databases, shared memory. (Drawn as two parallel horizontal lines / open-ended rectangle.)
- **Data flows** — connect processes to other elements. (Drawn as arrows; labelled with what flows, e.g. "Requests", "Responses", "SQL Query Calls", "Data".)
- **External entities** — everything *but* your code and data, including people and cloud software. (Drawn as a plain rectangle.)

Plus the crucial fifth annotation:

- **Trust boundary** — drawn as a dashed line/box (see next concept).

**DFD notation key (from the Acme example):** External Entity = rectangle; Process = rounded rectangle; Data flow = double-headed/single arrow labelled with the data; Data Store = pair of parallel lines; Trust Boundary = dashed box (L08 p.18).

**DFD levels / examples in the slides:**

- **Example 1 — Acme Database** (L08 p.18): External entities = Web Clients, SQL Clients, DBA (human), DB Users (human). Processes inside a "DB Cluster / Acme SQL Account" trust boundary = Front End(s), Database, DB Admin, Log analysis. Data stores = Data, Management, Logs. Data flows connect clients ↔ front end ↔ database ↔ admin ↔ logs.
- **Example 2 — Level 1 DFD: Store Database** (L08 p.19): labels each element type explicitly — *Actor* (User, rectangle), *Process* (App Back-end, circle), *Multi Process* (Other Services, double circle), *Data store/Asset* (App Database), *Data Flow* (e.g. "Modify report", "Store modification", "Retrieve details from other services"), with dashed *Trust Boundaries* between zones.
- **Example 3 — Level 2 DFD: College Library Website** (L08 p.20): External entities Users and Librarians; processes "College Library Website" and "College Library Database" (drawn as double circles = multi-processes); data stores "Web Pages on Disk" and "Database Files"; flows labelled Requests, Responses, SQL Query Calls, Pages, Data; trust boundaries shown as dashed lines separating users from the website and the website from the database.

The progression Level 1 → Level 2 illustrates **decomposition** (OWASP "Decompose Application", L08 p.13): higher-level processes are expanded into more detailed sub-diagrams.

### Trust boundaries

**What:** A **trust boundary is where two (or more) principals interact — i.e., where entities with *different privileges* interact** (L08 p.21). Example: apps on mobile platforms (two or more principals).

**Why they matter:** They are sometimes left implicit during development, but **effective threat modeling requires making boundaries explicit** (L08 p.21). The headline rule: **threats tend to cluster around trust boundaries** (L08 p.21) — so they are where you should look hardest.

**How they are enforced:** They "need to be enforced in some way." It is **best to rely on the OS**, though sometimes that is not possible (e.g., when building a database) (L08 p.21). In diagrams they are drawn as dashed lines/boxes separating zones of different trust (L08 p.18–20).

### Swim lane diagrams

**What:** Show two or more entities communicating, **each "in a lane"** (L08 p.22).

**Why/How:** Useful for **network communication**; the lanes have **implicit boundaries between them** (so they double as a way to see trust boundaries in a protocol). The lecture's example shows the **TCP 3-way handshake**: Client and Server lanes exchanging SYN → SYN-ACK → ACK → Data (L08 p.22).

### State machines

**What/Why:** Helpful for considering **what changes the security state** of a system — for example moving from **unauthenticated to authenticated**, or from **user to root/admin** (L08 p.23).

**Other UML diagrams:** Any UML diagram can be adapted. UML = **Unified Modeling Language**; these can be quite complex. Example: **activity diagrams** show *process flow*, whereas **data flow diagrams only represent the exchange of data** (L08 p.23). (This contrast — data flow vs. control flow — recurs at validation, where the advice is to focus on data flow, not control flow, while remembering every transition indicates processing; see Validation below, L08 p.52.)

### Tools to guide the threat search

To achieve **completeness and predictability** when finding threats, the lecture gives three categories of structuring tools (L08 p.25):

- **Attack libraries** — existing threats/categories used as inspiration.
- **STRIDE, PASTA, etc.** — a general search structure/technique.
- **Attack trees** — connecting a process and its possible threats.

### Attack libraries

**What:** Collections of threats and vulnerabilities — structured, up-to-date information that helps **structure thinking toward completeness and predictability** (L08 p.26).

**Examples named in the lecture** (L08 p.26):

- **OWASP** — Open Web Application Security Project; category: *Top Ten risks*.
- **CAPEC** — Common Attack Pattern Enumeration and Classification.
- **CVE** — Common Vulnerabilities and Exposures.
- **CMU** — Vulnerability Notes Database.
- **Exploit-DB** — https://www.exploit-db.com/.
- The NVD vulnerability description database: https://nvd.nist.gov/vuln.

The lab repeats these as reference sources for inspiration when applying STRIDE: OWASP, CAPEC, CVE, Exploit-DB, CMU materials (E08 p.3).

### STRIDE

**What:** STRIDE is **a methodology for identifying and categorizing threats** (L08 p.28). It is a mnemonic for six threat categories, each of which violates a specific security property (L08 p.28–29):

| Letter | Threat | Property violated | Definition |
|---|---|---|---|
| **S** | **Spoofing** | Authentication | Impersonating something or someone else |
| **T** | **Tampering** | Integrity | Modifying data or code |
| **R** | **Repudiation** | Non-repudiation | Claiming to have not performed an action |
| **I** | **Information Disclosure** | Confidentiality | Exposing information to someone not authorized to see it |
| **D** | **Denial of Service** | Availability | Deny or degrade service to users |
| **E** | **Elevation of Privilege** | Authorization | Gain capabilities without proper authorization |

(L08 p.29 — the slide gives exactly this Threat / Property Violated / Definition table.)

**Why it's useful** (L08 p.28):

- **Business oriented** — easier for non-technical people to relate to.
- **Expands (and can replace)** a "may by mechanisms and subsystems" approach.
- **Can also be used to identify threats** — e.g., as a pentest checklist.

**Per-category illustrations in the slides** (L08 p.30–36):

- **Spoofing over a network** (L08 p.30) — impersonating a machine/identity across the network.
- **Tampering with a file** (L08 p.31) — modifying data at rest.
- **Repudiation attacks on logs** (L08 p.32) — denying actions, attacking the audit trail.
- **Information disclosure (process)** and **information disclosure (data flow)** (L08 p.33–34) — leaking from a running process or from data in transit.
- **Denial of service** (L08 p.35) — "Can be **temporary** (as the attack continues; e.g. fill the network) or **persist beyond that** (e.g. fill a disk)."
- **Elevation of privilege (EoP)** (L08 p.36) — gaining higher rights than authorized.

**How to use STRIDE** (L08 p.37): Consider how **each** STRIDE threat could impact **each** part of the model — "How could a clever attacker spoof a certain part of the system? Could the attacker tamper with it? … etc." Use aids: all available information at your disposal, **attack trees**, and experience.

> Note on naming: the slide also references the **EoP card game** (Elevation of Privilege) as lab material to review — a card game built around STRIDE categories (E08 p.2).

### Attack trees

**What:** An attack tree is **a branching, hierarchical data structure that represents a set of potential techniques for exploiting security vulnerabilities** (L08 p.38). Structure (L08 p.38):

- **Root node** = the security incident that is the *goal* of the attack.
- **Branches and subnodes** = the ways an attacker could reach that goal.
- **Leaf nodes** (final nodes on paths outward from the root) = different ways to *initiate* an attack.
- **Motivation:** to effectively exploit the information available on attack patterns.

**Why:** They express the **structured relationship between attack details** — "this is a subcategory of that" — and can be presented as an *outline* (for the big picture) (L08 p.39). The lecture notes there is a difference between **creation vs. use** of an attack tree (L08 p.39).

**Three representations of a tree** (L08 p.39): the same tree can be drawn as (1) a graphical AND/OR tree diagram, or (2) written as a textual **outline** (e.g., *Goal: Access to the building* → 1. Go through a door → a. When it's unlocked → i. Get lucky; ii. Observe the latch plate; iii. Distract the person …; b. Drill the lock; c. Pick the lock; d. Get the key …; 2. Go through a window; 3. Go through a wall) — illustrating that an attack tree and a structured outline are interchangeable views of the same hierarchy.

**Worked example in the slides:** *An Attack Tree for Internet Banking Authentication* (L08 p.40) — root **"Bank Account Compromise,"** branching into sub-goals such as *User credential compromise* (→ user surveillance, theft of token and handwritten notes, malicious software installation, brute-force attacks with PIN calculators, user communication with attacker, …), *Injection of commands*, *User credential guessing*, and *Use of known authenticated session by attacker* (e.g., session hijacking, normal user authentication with specified session ID). Leaf nodes are coded (e.g. UT/Cx, UV/Cx, CCx, BBx, SSx) to map back to specific techniques.

**How to use an attack tree** (L08 p.41):

- **Find an appropriate (existing) tree** — e.g., via web search.
- **Iterate through your diagram and the tree**, asking "Does this apply here?" More precise iteration is more useful when you're learning, or for high-stakes analysis.

**How to create an attack tree** (L08 p.41) — for a project or general use, the steps are:

1. **Choose a representation** (graphical tree or outline).
2. **Create a root node** (the goal, e.g., "Get root").
3. **Add subnodes** (the ways to reach the goal).
4. **Consider completeness.**
5. **Prune and check.**

### Addressing threats — the four mitigation strategies

**What:** Once threats are found, **for each threat in your list you need to find a strategy** (L08 p.43). The four options:

1. **Mitigating** — make it harder for the attacker to take advantage. *This is the default.*
2. **Eliminating** — remove the functionality responsible.
3. **Transferring** — let somebody else handle the problem.
4. **Accepting** — used if the threat cannot be addressed in another reasonable manner.

**Key caveat:** **There are almost always trade-offs** when deciding how to deal with a threat (L08 p.43).

**"Fix It!" — eliminate beats mitigate** (L08 p.45): The *best* way to remove a security bug is to **remove the functionality**. The lecture's example: if SSL didn't have a "heartbeat" message, the **Heartbleed** bug couldn't exist. If you don't remove it, **you can only mitigate, not fix.**

### Mitigation techniques mapped to STRIDE

The lecture gives concrete mitigations per category.

**Addressing Integrity / Spoofing issues** (L08 p.44):

- Use permissions as provided.
- **Cryptography is required over a network** — e.g., SSL/TLS for authenticating computers.
- **Authenticating bits** (files, messages, etc.) — digital signatures, hashes (appropriately managed).
- Implementing a permission system is hard — many documented mistakes; passwords, MFA, etc.

**Addressing Repudiation** (L08 p.44):

- **Logs** — logging, log-analysis tools, secure log storage.
- **Secure time stamps.**
- **Trusted third parties.**

**Full "More Technical Mitigations" table** (L08 p.45) — columns: Threat / Mitigation Technology / Developer Example / Sysadmin Example:

| Threat | Mitigation Technology | Developer Example | Sysadmin Example |
|---|---|---|---|
| **Spoofing** | Authentication | Digital signatures, Active Directory, LDAP | Passwords, crypto tunnels |
| **Tampering** | Integrity, permissions | Digital signatures | ACLs/permissions, crypto tunnels |
| **Repudiation** | Fraud prevention, logging, signatures | Customer history risk management | Logging |
| **Information disclosure** | Permissions, encryption | Permissions (local), PGP, SSL | Crypto tunnels |
| **Denial of service** | Availability | Elastic cloud design | Load balancers, more capacity |
| **Elevation of privilege** | Authorization, isolation | Roles, privileges, input validation for purpose, (fuzzing\*) | Sandboxes, firewalls |

\* **Fuzzing/fault injection is *not* a mitigation, but a great testing technique** (see chapter 8, *Threat Modeling*) (L08 p.45).

### Prioritizing threats (DREAD and risk matrices)

**What/Why:** Not all threats are equal; you need a way to prioritize. Strategies listed (L08 p.46): **wait to see; easy fixes first; threat ranking with a "bug bar"; cost/damage estimation approaches; DREAD.**

**DREAD** is a scoring model with five factors (L08 p.46):

- **D — Damage Potential**
- **R — Reproducibility**
- **E — Exploitability**
- **A — Affected Users**
- **D — Discoverability**

**How DREAD works:** For each factor, scale from **high to low severity** and **assign a point for each score** (L08 p.46). Worked example for "Damage" of Threat 1 (L08 p.47):

- **3 points — High:** an attacker can run as administrator.
- **2 points — Medium:** revealing sensitive data.
- **1 point — Low:** revealing data.

For this example system, Damage for Threat 1 is given **1 point (Low)**. Then you **sum the scores and take the average** for Threat 1, and similarly define scores for the remaining "READ" factors (Reproducibility, Exploitability, Affected users, Discoverability) for each threat (L08 p.47).

**Another approach — a risk matrix** (L08 p.48): For each threat define a scale for:

- **Impact to system/data** — e.g., Minor, Moderate, Severe.
- **Likelihood of occurrence** — e.g., Unlikely, Possible, Likely.

Then **plot** threats on a 3×3 Impact × Likelihood grid (numbered threats land in coloured cells — severe+likely = red/high priority; minor+unlikely = green/low priority). This matrix is from the paper *"Google Android: A comprehensive security assessment"* (Shabtai et al., 2010) (L08 p.48).

### Validating the threat model

**What:** Validation = **"Quality Assurance for Threat Models"** (L08 p.49). There are **two things to validate** (L08 p.50):

1. **The threat model itself.**
2. **That the identified threats are addressed.**

**Validating the model** — gather expertise (everyone involved) and ask (L08 p.50):

- Is the model **complete**?
- Is the model **accurate**?
- Does it cover **all the security decisions** we made?
- Can we move on to a newer version of the model? Update when necessary.

**Go through the diagram again, asking** (L08 p.51):

- Have we checked **every part** for threats?
- Have we considered relevant **attack trees**?
- Have we gone through the **whole STRIDE list**?
- Have we made a **complete list of threats** — i.e., is there an issue in the bug tracker for *each* threat?
- Have we **listed all assumptions**?

**Updating the model** (L08 p.52):

- **Focus on data flow, not control flow** (but remember every transition indicates processing).
- **Vague phrasings indicate a need for more detail.**
- When explaining the diagram, do you add information? A discussion could indicate an **incomplete diagram**.
- **A data flow model should have no dead ends.**

**Validating all threats are addressed** (L08 p.52):

- Check that the model **matches reality**.
- Do you have documentation for each threat covering: **risks, the strategy addressing the risk, and a test** available for each one?
- Has **every threat issue been closed**? Are the tests part of the development and/or deployment procedure?

---

## Glossary

- **Threat modeling** — A tool/process to improve security by addressing predictable threats; structured, efficient, big-picture analysis to ensure more secure software/systems (L08 p.8–9).
- **Asset** — A valuable thing the business cares about; overlapping definitions: something an attacker wants, something you want to protect, or a stepping stone (L08 p.11).
- **Stepping stone** — A resource (e.g., any computer inside the perimeter) valuable not for itself but as a route to a more valuable target ("inner sanctum") (L08 p.12).
- **Trust boundary** — Where two or more principals (entities with *different privileges*) interact; threats cluster here; best enforced by the OS (L08 p.21).
- **Principal** — An entity (user, process, machine) with a particular privilege level that interacts across a trust boundary (L08 p.21).
- **Data Flow Diagram (DFD)** — A model abstracting a program into processes, data stores, data flows, and external entities; threats follow data (L08 p.17).
- **Process** — In a DFD, *your code*; drawn as a rounded rectangle or circle (double circle = multi-process) (L08 p.17).
- **Data store** — In a DFD, files, databases, or shared memory (L08 p.17).
- **Data flow** — In a DFD, a connection (arrow) carrying data between processes and other elements (L08 p.17).
- **External entity** — In a DFD, everything but your code and data, including people and cloud software (L08 p.17).
- **DFD level (Level 1 / Level 2)** — Successively decomposed DFDs; higher-level processes are expanded into more detailed sub-diagrams (L08 p.19–20).
- **Swim lane diagram** — Diagram showing two or more entities communicating, each in a lane, with implicit boundaries between lanes; good for network protocols (e.g., TCP 3-way handshake) (L08 p.22).
- **State machine** — A model of what changes a system's *security state* (e.g., unauthenticated → authenticated, user → root) (L08 p.23).
- **UML (Unified Modeling Language)** — A modelling notation; any UML diagram (e.g., activity diagram for process flow) can be adapted for threat modeling (L08 p.23).
- **Attack library** — A structured, up-to-date collection of threats/vulnerabilities used to drive completeness (OWASP, CAPEC, CVE, CMU, Exploit-DB) (L08 p.26).
- **OWASP** — Open Web Application Security Project; provides the Top Ten risks (L08 p.26).
- **CAPEC** — Common Attack Pattern Enumeration and Classification (L08 p.26).
- **CVE** — Common Vulnerabilities and Exposures (L08 p.26).
- **STRIDE** — Methodology to identify/categorize threats: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege (L08 p.28).
- **Spoofing** — Impersonating something or someone else; violates Authentication (L08 p.29).
- **Tampering** — Modifying data or code; violates Integrity (L08 p.29).
- **Repudiation** — Claiming to have not performed an action; violates Non-repudiation (L08 p.29).
- **Information Disclosure** — Exposing information to someone not authorized to see it; violates Confidentiality (L08 p.29).
- **Denial of Service (DoS)** — Deny or degrade service to users; violates Availability; can be temporary or persistent (L08 p.29, 35).
- **Elevation of Privilege (EoP)** — Gain capabilities without proper authorization; violates Authorization (L08 p.29, 36).
- **Attack tree** — A branching, hierarchical structure: root = attack goal, branches/subnodes = ways to reach it, leaf nodes = ways to initiate the attack (L08 p.38).
- **Root node** — The attack goal at the top of an attack tree (L08 p.38).
- **Leaf node** — A final node on a path out from the root; a concrete way to initiate the attack (L08 p.38).
- **Mitigating** — Making it harder for an attacker to exploit a threat; the default strategy (L08 p.43).
- **Eliminating** — Removing the functionality responsible for a threat (the best "fix") (L08 p.43, 45).
- **Transferring** — Letting someone else handle the problem (L08 p.43).
- **Accepting** — Tolerating a threat when it can't reasonably be addressed otherwise (L08 p.43).
- **DREAD** — Prioritization scoring: Damage potential, Reproducibility, Exploitability, Affected users, Discoverability; score each high→low and average (L08 p.46–47).
- **Bug bar** — A threat-ranking threshold used to prioritize threats (L08 p.46).
- **Risk matrix** — A grid plotting threats by Impact (Minor/Moderate/Severe) × Likelihood (Unlikely/Possible/Likely) (L08 p.48).
- **Heartbleed** — An example bug in SSL's heartbeat message; cited to show that removing functionality eliminates whole bug classes (L08 p.45).
- **Fuzzing / fault injection** — A testing technique (*not* a mitigation) (L08 p.45).
- **EoP card game** — Elevation of Privilege card game; STRIDE-based lab material to review before the exercise (E08 p.2).

---

## How-To Cookbook

### A. Run the full four-step threat-modeling flow (L08 p.16)

1. **Model the system.** Draw a DFD (see B). Abstract away detail so you can see the whole; make trust boundaries explicit (L08 p.14, 21).
2. **Find threats.** Walk every element with STRIDE (see C) and consult attack libraries and relevant attack trees (see D) (L08 p.25, 37).
3. **Address threats.** For each threat choose Mitigate / Eliminate / Transfer / Accept, then prioritize with DREAD or a risk matrix (see E, F) (L08 p.43, 46).
4. **Validate.** QA the model and confirm every threat is documented, tracked, and tested (see G) (L08 p.49–52).
5. **Repeat.** Treat it as a continuous process — re-run as the system or threat landscape changes (L08 p.53).

### B. Build a Data Flow Diagram (DFD) (L08 p.17–21)

1. **Identify external entities** — everything outside your code/data: users, other systems, cloud services. Draw each as a **rectangle**.
2. **Identify processes** — your code/components. Draw each as a **rounded rectangle or circle** (use a **double circle** for a multi-process that you will decompose further).
3. **Identify data stores** — files, databases, shared memory. Draw each as a **pair of parallel lines**.
4. **Draw data flows** — arrows connecting the elements; **label each with the data that moves** (e.g., "Requests", "Responses", "SQL Query Calls", "Data").
5. **Add trust boundaries** — draw **dashed lines/boxes** wherever principals of different privilege interact (e.g., user ↔ app, app ↔ database, device ↔ cloud). These are where you'll focus threat-finding.
6. **State your assumptions** on the diagram (platform, framework, components) (E08 p.2).
7. **Sanity-check:** no dead ends; every transition implies processing; vague labels mean you need more detail (L08 p.52). If a process is too coarse, **decompose** it into a lower-level DFD (Level 1 → Level 2) (L08 p.19–20).

### C. Apply STRIDE per element (L08 p.28–37)

1. List every DFD element (each process, data store, data flow, external entity) — paying special attention to elements **on or crossing trust boundaries** (L08 p.21).
2. For **each** element, ask **each** STRIDE question (L08 p.37):
   - **S**poofing — can the element/identity be impersonated? (Authentication)
   - **T**ampering — can its data/code be modified? (Integrity)
   - **R**epudiation — can an actor deny an action? (Non-repudiation)
   - **I**nformation disclosure — can data leak to the unauthorized? (Confidentiality)
   - **D**enial of service — can it be made unavailable/degraded? (Availability)
   - **E**levation of privilege — can someone gain rights they shouldn't have? (Authorization)
3. Record each identified threat in a structured **list or table** keyed by STRIDE category; aim for **multiple examples per category** (E08 p.2–3).
4. Use **attack libraries** (OWASP, CAPEC, CVE, Exploit-DB, CMU) and **attack trees** as inspiration to reach completeness (L08 p.26, 37).

### D. Construct an attack tree (L08 p.41)

1. **Choose a representation** — a graphical tree or a textual outline (they're interchangeable) (L08 p.39).
2. **Create the root node** = the attacker's goal (e.g., "Bank Account Compromise" or "Get root").
3. **Add subnodes** = the ways an attacker could reach that goal; expand each into more specific child nodes.
4. **Continue to leaf nodes** = concrete ways to *initiate* the attack.
5. **Consider completeness** — have you captured the main paths? Consult existing trees via web search and ask "Does this apply here?" (L08 p.41).
6. **Prune and check** — remove irrelevant branches and verify against your DFD/STRIDE results.

### E. Choose a mitigation strategy per threat (L08 p.43–45)

For each threat in your list, pick one (remembering trade-offs always exist):
1. **Eliminate** if you can — remove the responsible functionality (the only true "fix"; cf. Heartbleed) (L08 p.45).
2. Otherwise **Mitigate** (default) — apply the STRIDE-mapped mitigation technology (e.g., Spoofing → authentication/crypto; Repudiation → logging + secure timestamps; Information disclosure → permissions + encryption) (L08 p.44–45).
3. **Transfer** — hand the risk to a third party where appropriate.
4. **Accept** — only if it cannot reasonably be addressed otherwise.

### F. Prioritize with DREAD (worked example) (L08 p.46–47)

1. For a given threat, score each factor high→low: **D**amage, **R**eproducibility, **E**xploitability, **A**ffected users, **D**iscoverability.
2. Use defined scales, e.g. for **Damage**: High = attacker runs as administrator (3); Medium = revealing sensitive data (2); Low = revealing data (1).
3. **Worked example — Threat 1:** Damage scored **1 (Low)**. Then score R, E, A, D the same way.
4. **Sum the scores and take the average** to get Threat 1's overall priority; repeat for every threat and rank them (L08 p.47).
5. *(Alternative)* Plot each threat on a **risk matrix** (Impact × Likelihood) and treat Severe+Likely as top priority (L08 p.48).

### G. Validate the threat model (L08 p.50–52)

1. **Validate the model:** gather everyone involved; confirm it is complete and accurate and covers all security decisions; produce a newer version if needed.
2. **Re-walk the diagram:** every part checked for threats? relevant attack trees considered? whole STRIDE list covered? complete threat list (a bug-tracker issue per threat)? all assumptions listed?
3. **Update rules:** focus on data flow not control flow; vague phrasing → add detail; no dead ends.
4. **Validate threats are addressed:** model matches reality; each threat has documented risk + mitigation strategy + a test; every threat issue closed; tests folded into dev/deployment.

### Worked example — lab walkthrough (Android health app) (E08 p.2–4)

1. **Model (Exercise 1):** Build a DFD for an **Android health app**: user authenticates with username/password; can manually enter/edit/delete personal data (height, weight, activity, diet); data stored **locally on the device** (E08 p.2). Elements: External entity = *User*; Process = *Health App / Auth module*; Data store = *Local DB on device*; Data flows = login credentials, CRUD data operations; Trust boundary = between the user and the app, and between the app and the OS/local store. State assumptions (native framework, OS components) on the diagram (E08 p.2).
2. **Find threats (Exercise 2):** Apply STRIDE to each element, multiple examples per category — e.g. **S**: spoof another user at login; **T**: tamper with locally stored health records; **R**: user denies deleting an entry (no audit log); **I**: another app reads the local DB (confidentiality); **D**: fill local storage so the app can't save; **E**: a malicious local app escalates to read the health DB (E08 p.2). Use the Acme case study, the EoP card game, OWASP/CAPEC/CVE/Exploit-DB for inspiration (E08 p.2–3).
3. **Discuss & refine (Exercise 3):** Cross-check with another group; finalise the DFD (with a brief description of key components) and a STRIDE table (E08 p.3).
4. **Evolve the system (Exercise 4):** Turn it into a **fitness tracker** — now it collects data from **third-party devices via Bluetooth** (steps, distance, calories, activity, sleep), **processes/cleans/computes** on the data, users **can no longer edit manually**, and data is stored **both locally and in a cloud service**. Update the DFD with the new components, data flows, and **trust boundaries** (Bluetooth link, cloud), and revise STRIDE to cover **external devices, wireless communication, and cloud storage** (E08 p.3).
5. **Discuss & refine again (Exercise 5):** Re-validate the updated DFD + STRIDE with another group (E08 p.4).
   - **Hint from the lab:** clearly define assumptions, focus on trust boundaries, apply STRIDE, keep diagrams/tables structured, and update the analysis as the system evolves (E08 p.4).

---

## Exam-Style Q&A

**Q1. List the four steps of the threat modeling flow and say what each does.**
A. (1) **Model System** — represent/rewrite the system (e.g., a DFD) to enable analysis. (2) **Find Threats** — identify threats in the model using STRIDE, attack libraries, and attack trees. (3) **Address Threats** — decide how to deal with each (mitigate/eliminate/transfer/accept) and prioritize. (4) **Validate** — QA the model and confirm every threat is addressed, documented, and tested (L08 p.16, 24, 42, 49). The lecture stresses it must be predictable, reliable, scalable, and practical — and that it's a continuous process (L08 p.13, 53).

**Q2. What does STRIDE stand for, and which security property does each category violate?**
A. **S**poofing → Authentication; **T**ampering → Integrity; **R**epudiation → Non-repudiation; **I**nformation Disclosure → Confidentiality; **D**enial of Service → Availability; **E**levation of Privilege → Authorization (L08 p.28–29). Definitions: impersonation; modifying data/code; denying an action; exposing data to the unauthorized; denying/degrading service; gaining capabilities without proper authorization (L08 p.29).

**Q3. What are the four element types of a Data Flow Diagram, and what symbol represents each?**
A. **Process** (your code) — rounded rectangle / circle (double circle = multi-process); **Data store** (files, databases, shared memory) — parallel lines; **Data flow** (connects elements) — labelled arrow; **External entity** (everything but your code/data, incl. people and cloud software) — rectangle (L08 p.17–18). Trust boundaries are added as dashed boxes (L08 p.18).

**Q4. Define a trust boundary and explain why threat modelers care about them.**
A. A trust boundary is **where two or more principals — entities with different privileges — interact** (L08 p.21). They matter because **threats tend to cluster around trust boundaries**, and effective threat modeling requires making these (often implicit) boundaries **explicit**. They should be enforced somehow, ideally by the OS (L08 p.21).

**Q5. Why does the lecture caution against starting threat modeling by "thinking like an attacker"?**
A. Because it is **risky** — if you misjudge what attackers know or will do, the whole model goes astray; and you already know a lot about your own system. The advice is not to *start* from attackers, though you should still keep them in mind for different scenarios (L08 p.10). Asset-centric starts are also tricky due to "risk of perspective" and overlapping asset definitions (L08 p.11–12).

**Q6. Describe the structure of an attack tree and what the root and leaf nodes mean.**
A. An attack tree is a **branching, hierarchical** structure of techniques for exploiting vulnerabilities. The **root node** is the attack's goal (e.g., "Bank Account Compromise"); **branches and subnodes** are ways to reach that goal; **leaf nodes** are concrete ways to *initiate* the attack. Its purpose is to exploit available information on attack patterns (L08 p.38, 40).

**Q7. Give the steps to *create* an attack tree.**
A. Choose a representation (tree or outline) → create a **root node** (the goal, e.g., "Get root") → **add subnodes** (ways to reach it) → **consider completeness** → **prune and check** (L08 p.41). To *use* an existing tree: find an appropriate one (web search) and iterate through your diagram asking "Does this apply here?" (L08 p.41).

**Q8. What are the four strategies for addressing a threat, and which is the default?**
A. **Mitigate** (make exploitation harder — *the default*), **Eliminate** (remove the responsible functionality — the best true fix), **Transfer** (let someone else handle it), and **Accept** (if it can't reasonably be addressed otherwise). There are almost always **trade-offs** (L08 p.43). Example of eliminating: removing SSL's heartbeat would have prevented Heartbleed entirely (L08 p.45).

**Q9. What is DREAD and how is it used to prioritize threats?**
A. DREAD = **Damage potential, Reproducibility, Exploitability, Affected users, Discoverability**. For each factor you scale from high to low severity and assign a point; then **sum and average** the scores per threat to rank them (L08 p.46–47). Example: Damage scored High=3 (run as admin), Medium=2 (reveal sensitive data), Low=1 (reveal data); Threat 1's Damage = 1 (Low) (L08 p.47).

**Q10. Besides DREAD, what prioritization approaches does the lecture mention?**
A. Wait-to-see, easy-fixes-first, threat ranking with a **bug bar**, and cost/damage estimation (L08 p.46). It also shows a **risk matrix** plotting each threat by **Impact** (Minor/Moderate/Severe) × **Likelihood** (Unlikely/Possible/Likely), from Shabtai et al.'s Android security assessment (L08 p.48).

**Q11. Give one mitigation technology for each STRIDE category (per the lecture's table).**
A. Spoofing → **Authentication** (digital signatures, AD/LDAP; passwords, crypto tunnels); Tampering → **Integrity/permissions** (digital signatures; ACLs, crypto tunnels); Repudiation → **fraud prevention, logging, signatures**; Information disclosure → **permissions, encryption** (PGP, SSL, crypto tunnels); Denial of service → **availability** (elastic cloud design; load balancers, more capacity); Elevation of privilege → **authorization, isolation** (roles, input validation; sandboxes, firewalls) (L08 p.45).

**Q12. What two things must be validated, and what questions does the lecture suggest when re-walking the diagram?**
A. Validate (1) **the threat model itself** and (2) **that identified threats are addressed** — "QA for your model" (L08 p.50). Re-walk asking: have we checked every part for threats? considered relevant attack trees? gone through the whole STRIDE list? made a complete threat list (a bug-tracker issue per threat)? listed all assumptions? (L08 p.51). For each threat there should be documented risks, a mitigation strategy, and a test, and every threat issue should be closed (L08 p.52).

**Q13. The lecture says to "focus on data flow, not control flow." What does that mean, and what makes a DFD valid?**
A. A DFD represents the **exchange of data**, not the program's control logic (activity diagrams handle control flow) (L08 p.23, 52). When updating, focus on data flow, but remember every transition implies processing; vague phrasings need more detail; and a valid data flow model has **no dead ends** (L08 p.52).

**Q14. Name four attack libraries/resources the lecture recommends and what they're for.**
A. **OWASP** (Top Ten risks), **CAPEC** (attack pattern catalogue), **CVE** (known vulnerabilities/exposures), **CMU Vulnerability Notes Database**, and **Exploit-DB** — structured, up-to-date collections that help drive **completeness and predictability** when searching for threats (L08 p.26).

**Q15. In the lab, how does the threat model change when the health app becomes a fitness tracker, and what new STRIDE concerns appear?**
A. New components: third-party Bluetooth devices feeding data; data processing/cleaning/computation; cloud storage in addition to local; manual editing removed (E08 p.3). New trust boundaries: the Bluetooth wireless link and the device↔cloud link. STRIDE must now cover **external devices, wireless communication, and cloud storage** — e.g., spoofing a paired Bluetooth device, tampering with data in transit over Bluetooth, information disclosure from cloud storage, DoS by flooding the wireless channel, and elevation via the cloud service (E08 p.3).

**Q16. How does threat modeling differ from penetration testing?**
A. Both perform threat assessment, but penetration testers must **infer** system details via active/passive reconnaissance, whereas threat modeling is done with **full system knowledge**, enabling a more structured and comprehensive evaluation of risks (E08 p.1). Threat modeling is also a *design-time/proactive* technique, complementing reactive methods like pen testing, fuzzing, and waiting for bug reports (L08 p.7–8).

---

## Gotchas

- **Eliminating ≠ mitigating.** Mitigating only makes exploitation *harder*; the only way to truly *fix* a security bug is to **remove the functionality** (eliminate). If you keep the feature, "you can only mitigate, not fix" (L08 p.43, 45). The Heartbleed example exists to drive this home.
- **Don't blindly start from the attacker.** "Think like an attacker" is risky — get the attacker model wrong and your whole analysis goes astray. The system-centric DFD+STRIDE path is the safer default; keep attackers in mind only for scenarios (L08 p.10).
- **"Asset" has three overlapping meanings** (attacker wants it / you want to protect it / stepping stone). Picking the wrong perspective skews your defences; what an asset list really buys you is *setting up your defences* (L08 p.11–12).
- **Trust boundaries are easy to leave implicit — and that's exactly where threats cluster.** Always draw them as dashed boundaries; STRIDE should be hammered hardest at elements crossing them (L08 p.21).
- **DFD = data flow, not control flow.** Don't draw an activity/flowchart and call it a DFD; DFDs only represent the *exchange of data*. A valid DFD has **no dead ends**, and vague labels signal missing detail (L08 p.23, 52).
- **Fuzzing/fault injection is a *testing* technique, not a mitigation.** Don't list it as a fix in the "Address Threats" step (L08 p.45).
- **DREAD has two D's.** Damage potential *and* Discoverability — easy to drop one. The other letters are Reproducibility, Exploitability, Affected users; score high→low and **average**, not just count (L08 p.46–47).
- **STRIDE must be applied to *every element*, exhaustively.** It's a per-element checklist (each STRIDE category × each model part), not a one-off brainstorm; partial coverage fails validation (L08 p.37, 51).
- **Map each STRIDE letter to its property.** A common slip is mismatching, e.g. Repudiation ↔ Non-repudiation (not Integrity), Spoofing ↔ Authentication, EoP ↔ Authorization. The exact mapping is the L08 p.29 table.
- **Validation is two-pronged.** Validate the *model* **and** that *threats are addressed* (documented risk + strategy + test, issues closed). People forget the second half (L08 p.50, 52).
- **It never ends.** Treating threat modeling as a one-time deliverable is a mistake — systems change, attack patterns change, new attacks appear; the process continues for the deployed product (L08 p.53).
- **State assumptions explicitly.** Both the slides (list all assumptions, L08 p.51) and the lab (clearly define assumptions, ensure they're reflected in the diagram, E08 p.2, p.4) require this — unlisted assumptions are a validation failure.
- **DoS can be temporary or persistent.** Temporary = lasts only while the attack continues (e.g., flooding the network); persistent = lasts beyond it (e.g., filling a disk). Don't treat all DoS as transient (L08 p.35).

---

### Coverage note / what's not fully specified

- A few slides are title-only or heavily image-based; their content has been captured from the rendered figures: the STRIDE property table (L08 p.29), the DFD examples and their notation key (L08 p.18–20), the swim-lane TCP handshake (L08 p.22), the attack-tree representations and the Internet Banking Authentication tree (L08 p.39–40), the technical-mitigations table (L08 p.45), and the Impact×Likelihood risk matrix (L08 p.48).
- The lecture references **PASTA** only by name as another STRIDE-like search technique (L08 p.25); the slides give no detail on PASTA's steps, so it is not elaborated here.
- The **Learning Objectives** slide (L08 p.6) is truncated in the deck (it ends at "Understand"), so the full stated objectives are not available from the source.
- The **Acme case study** and **EoP card game** are referenced as lab Resources (E08 p.2) but are packaged separately (`Resources.zip`); their internal content is outside the two PDFs read and is therefore not summarized here.
