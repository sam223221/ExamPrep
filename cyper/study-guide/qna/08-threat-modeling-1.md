# 08. Threat Modeling I — Simulated Open-Book Questions

### [EASY] A junior colleague labels a login form's "username/password" arrow in a DFD simply as "Data". Using the DFD conventions, what is wrong, and how should the four element types around that arrow be drawn?

**Answer:** The arrow itself is a **data flow**, and the chapter says data flows must be **labelled with what flows** — "Requests", "Responses", "SQL Query Calls", "Data" etc. (L08 p.17, p.73). "Data" is too vague; the lecture explicitly warns that **vague phrasings indicate a need for more detail** (L08 p.52). It should be labelled with something concrete such as "Login credentials".

The surrounding elements (L08 p.17–18):

1. The **User** is an **external entity** — everything but your code and data, including people — drawn as a **plain rectangle**.
2. The **login form / app logic** is a **process** (your code) — drawn as a **rounded rectangle or circle**.
3. The credentials **arrow** is the **data flow** — an arrow labelled "Login credentials".
4. If the password is checked against a stored table, that table is a **data store** — drawn as a **pair of parallel lines**.

A **trust boundary** (dashed box) should also sit between the user and the app, since they are principals of different privilege (L08 p.21).

### [EASY] An attacker modifies a configuration file on disk so the application loads malicious settings. Which single STRIDE letter is this, and exactly which security property does it violate?

**Answer:** This is **T — Tampering**, defined as "modifying data or code" (L08 p.29). Modifying a file at rest is the textbook tampering example the lecture gives ("Tampering with a file", L08 p.31).

The property it violates is **Integrity** (L08 p.29). A common slip is to call file modification "information disclosure" or to attach it to the wrong property — but the L08 p.29 table fixes the mapping as Tampering ↔ Integrity. The standard mitigation per the lecture is **integrity/permissions**: digital signatures, ACLs/permissions, or crypto tunnels (L08 p.45).

### [EASY] In one sentence each, define the four strategies for addressing a threat, and state which one is the default.

**Answer:** The four strategies (L08 p.43):

1. **Mitigating** — make it *harder* for the attacker to take advantage. **This is the default.**
2. **Eliminating** — remove the functionality responsible (the only true "fix").
3. **Transferring** — let somebody else handle the problem.
4. **Accepting** — used only if the threat cannot be addressed in another reasonable manner.

The chapter also stresses there are **almost always trade-offs** when choosing (L08 p.43).

### [EASY] List the four steps of the threat modeling flow in order, and name one tool the chapter associates with each step.

**Answer:** The four-step framework (L08 p.16):

1. **Model System** — e.g. a **Data Flow Diagram (DFD)** (also swim lanes, state machines, UML) (L08 p.14).
2. **Find Threats** — e.g. **STRIDE** (also attack libraries, attack trees) (L08 p.25).
3. **Address Threats** — e.g. the **mitigate/eliminate/transfer/accept** choice, then prioritize with **DREAD** or a risk matrix (L08 p.43, 46).
4. **Validate** — **quality-assurance** checks on the model and on whether threats are addressed (L08 p.49).

The lecture says the process must be predictable, reliable, scalable and practical, and that it is **continuous**, not one-off (L08 p.13, 53).

### [EASY] A diagram shows a "Client" lane and a "Server" lane exchanging SYN → SYN-ACK → ACK → Data. What kind of diagram is this, and what does the boundary between the lanes represent?

**Answer:** It is a **swim lane diagram** — two or more entities communicating, each "in a lane" (L08 p.22). The chapter uses exactly this **TCP 3-way handshake** as its example (L08 p.22).

The boundary between the lanes is an **implicit trust boundary** (L08 p.22). That is why swim lanes are useful for **network communication**: the lanes double as a way to see where principals of different privilege meet, which is where threats cluster (L08 p.21–22).

### [MEDIUM] You are threat-modeling a web app and a teammate says, "Let's start by listing our assets and thinking like an attacker." Per the chapter, why is each starting point risky, and what does the lecture recommend as the safer default?

**Answer:** Both starting points carry risks the lecture calls out:

1. **"Think like an attacker" (attacker-centric)** is **risky** because if you get the attacker's knowledge or intent wrong, *your whole threat model goes astray* — and you already know a great deal about your own system anyway. The advice is "don't *start* from attackers (maybe)!" while still keeping them in mind for different scenarios (L08 p.10).
2. **Starting from assets (asset-centric)** has a **"risk of perspective"**: "asset" has three overlapping meanings — something an attacker wants, something you want to protect, or a stepping stone — and it is hard to judge what an attacker will actually want (L08 p.11–12). What an asset list really buys you is knowledge of **how to set up your defences** (L08 p.12).

The **safer default** is the **system/software-centric** approach: model the system itself with a **DFD** and then apply **STRIDE** (L08 p.9, the path the rest of the lecture develops).

### [MEDIUM] A user can delete a health-record entry, but the app keeps no audit log. Map this to a STRIDE category, name the property violated, and give the chapter's recommended mitigation set.

**Answer:** This is **R — Repudiation**: the user can later "claim to have not performed an action" (here, deleting the entry) and there is nothing to prove otherwise (L08 p.29). The lab uses this exact scenario — "user denies deleting an entry (no audit log)" (E08 p.2).

- **Property violated:** **Non-repudiation** (L08 p.29). Note the mapping is Repudiation ↔ Non-repudiation, *not* Integrity — a common slip the chapter flags (L08 p.483 gotcha).
- **Recommended mitigation:** The lecture's repudiation mitigations are **logs** (logging, log-analysis tools, secure log storage), **secure time stamps**, and **trusted third parties** (L08 p.44). The technical-mitigations table lists "fraud prevention, logging, signatures" with customer-history risk management on the developer side and logging on the sysadmin side (L08 p.45).

So: add a secure, tamper-resistant audit log with secure timestamps recording each delete action.

### [MEDIUM] For a denial-of-service threat where an attacker fills the device's local storage so the app can no longer save data, classify the DoS as temporary or persistent, justify it, and give a developer-side mitigation.

**Answer:** This is a **persistent** DoS. The chapter's distinction (L08 p.35): a DoS can be **temporary** — it lasts only "as the attack continues", e.g. flooding the network — or **persist beyond that**, e.g. **fill a disk**. Filling the local storage is precisely the "fill a disk" case, so the damage outlives the attack: even after the attacker stops, the disk stays full and the app still can't save until someone frees space. So it is persistent, not transient.

- **Property violated:** **Availability** (L08 p.29).
- **Developer-side mitigation:** the table maps DoS → **availability**, with the developer example being **elastic cloud design**, and the sysadmin example being **load balancers / more capacity** (L08 p.45). For a local-storage variant, the spirit is the same: design for capacity/quotas so a single source can't exhaust storage. (Don't list **fuzzing** as a mitigation — it is a *testing* technique, not a fix, L08 p.45.)

### [MEDIUM] Your team found an information-disclosure threat and decides "we'll just remove the export-to-CSV feature that leaks the data." Which addressing strategy is this, why does the chapter call it the best kind of fix, and what example does it use?

**Answer:** Removing the feature is the **Eliminate** strategy — "remove the functionality responsible" (L08 p.43).

The chapter calls elimination the **best way to remove a security bug** because it removes the whole bug class rather than just making exploitation harder: *the best way to remove a security bug is to remove the functionality* (L08 p.45). The contrast it draws is "**Fix It!**" — if you don't remove the functionality, **you can only mitigate, not fix** (L08 p.43, 45).

The worked example is **Heartbleed**: "if SSL didn't have a 'heartbeat' message, the Heartbleed bug couldn't exist" (L08 p.45). So eliminating the export feature is the analogue — no feature, no leak through it. The trade-off (always present, L08 p.43) is that you lose the functionality users may want.

### [MEDIUM] Explain the difference between a Data Flow Diagram and an activity diagram, and state two validation rules the chapter gives that follow from a DFD being about data flow.

**Answer:** The distinction (L08 p.23): **activity diagrams show *process / control flow***, whereas **data flow diagrams only represent the *exchange of data***. A DFD captures *what data moves where*, not the program's control logic or decision branches.

Two validation rules that follow from "focus on data flow, not control flow" (L08 p.52):

1. **A data flow model should have no dead ends** — every flow must connect to something; a flow that goes nowhere signals an incomplete model.
2. **Every transition indicates processing** — so while you focus on data flow, you must remember each transition implies some processing exists (and, relatedly, vague phrasings mean you need more detail).

The chapter folds this into the broader rule "focus on data flow, not control flow (but remember every transition indicates processing)" (L08 p.52).

### [HARD] Build a minimal DFD (as a labelled element list plus an ASCII sketch) for a single-device Android health app: a user logs in with username/password, can create/edit/delete personal data (weight, diet), and data is stored locally on the device. Identify all four element types and every trust boundary.

**Answer:** This mirrors the lab's Exercise 1 (E08 p.2). Elements:

- **External entity (rectangle):** **User**.
- **Process (rounded rectangle/circle):** **Health App** (with an **Auth module** sub-component).
- **Data store (parallel lines):** **Local DB on device**.
- **Data flows (labelled arrows):** "Login credentials", "CRUD data ops" (create/edit/delete weight, diet), "Stored/retrieved records".
- **Trust boundaries (dashed):** (1) between the **User and the app**, and (2) between the **app and the OS / local store** (E08 p.2).

```
        TB1                         TB2
  +------|--------------------------|----------------+
  |      |                          |                |
[User]---|--login credentials------>[ Health App ]   |
(ext.    |                          ( Auth module )   |
 entity) |<--auth result-----------(   process   )    |
  |      |        CRUD data ops --->|                 |
  |      |                          |  store/retrieve |
  |      |                          |       v         |
  |      |                       === Local DB ===     |
  |      |                       (data store on dev.) |
  +------|--------------------------|----------------+
       (User|App)              (App|OS/local store)
```

State the **assumptions** on the diagram (native framework, OS components) — the lab requires assumptions be explicit (E08 p.2). Threats will cluster on **TB1** and **TB2** because that's where principals of different privilege meet (L08 p.21).

### [HARD] Take the DFD from the previous question and apply STRIDE to produce one concrete threat per letter, mapping each to the property it violates. Pay special attention to elements on the trust boundaries.

**Answer:** Walking STRIDE per element, paying attention to the boundaries (L08 p.37; lab E08 p.2):

| STRIDE | Concrete threat on this app | Property violated |
|---|---|---|
| **S** Spoofing | Attacker spoofs another user at the **login** flow (TB1) to impersonate them | **Authentication** |
| **T** Tampering | Attacker **modifies the locally stored health records** in the device DB | **Integrity** |
| **R** Repudiation | A user **denies deleting** an entry; no audit log exists to refute it | **Non-repudiation** |
| **I** Information disclosure | **Another app reads the local DB**, exposing health data | **Confidentiality** |
| **D** Denial of service | Attacker **fills local storage** so the app can't save | **Availability** |
| **E** Elevation of privilege | A **malicious local app escalates** to read/write the health DB | **Authorization** |

Notes:
1. STRIDE is a **per-element checklist** — each category against each part — not a one-off brainstorm (L08 p.37, p.482 gotcha). The table above is one example per letter; the lab asks for **multiple examples per category** (E08 p.2).
2. The S, I and E threats all live at the **trust boundaries** (login at TB1; cross-app reads at TB2), confirming "threats cluster around trust boundaries" (L08 p.21).
3. Use **attack libraries** (OWASP, CAPEC, CVE, Exploit-DB) and the **EoP card game** as inspiration to reach completeness (L08 p.26; E08 p.2–3).

### [HARD] Construct an attack tree (outline form) for the goal "Read another user's health data on the local-storage health app." Use at least one AND relationship and one OR relationship, and label the leaf nodes.

**Answer:** Following the creation steps — choose representation (outline), create root = goal, add subnodes, continue to leaf nodes, consider completeness, prune (L08 p.41) — and the convention that root = goal, subnodes = ways to reach it, leaves = ways to *initiate* (L08 p.38):

```
GOAL (root): Read another user's health data
  OR 1. Read the local DB file directly
        a. [leaf] Install a malicious app that requests storage access
        b. [leaf] Gain physical access + USB debugging to pull the DB
  OR 2. Authenticate as the victim
        AND  (must do BOTH a and b)
        a. [leaf] Obtain the victim's username
        b. [leaf] Obtain the victim's password (phishing OR brute force)
  OR 3. Elevate privilege on the device
        a. [leaf] Exploit a local OS vulnerability to gain root, then read DB
```

Reading the operators:

- **Node 1 vs 2 vs 3** are joined by **OR** — *any* path achieves the goal.
- **Node 2** is an **AND** — the attacker needs **both** the username **and** the password; missing either fails the path.
- Inside 2b, "phishing OR brute force" is a nested **OR** (either initiation works).
- **Leaf nodes** (1a, 1b, 2a, 2b, 3a) are the concrete ways to *initiate* the attack (L08 p.38).

This is interchangeable with a graphical AND/OR tree diagram — the chapter stresses the outline and the tree are two views of the same hierarchy (L08 p.39). To use it well, also pull from an existing tree (e.g. the Internet Banking Authentication tree, L08 p.40) and ask "does this apply here?" (L08 p.41).

### [HARD] You have three threats on the health app. Using DREAD, score Threat A = "local app reads health DB" with a defined scale and compute its priority. Then explain how the result would change your ordering versus a risk matrix.

**Answer:** DREAD's five factors, each scored high→low, then **summed and averaged** (L08 p.46–47). Using the chapter's Damage scale (High=3 attacker runs as admin; Medium=2 reveal sensitive data; Low=1 reveal data, L08 p.47) and applying the same 1–3 high→low logic to the rest:

| Factor | Reasoning for Threat A | Score |
|---|---|---|
| **D**amage potential | Reveals **sensitive** health data (not admin) → Medium | **2** |
| **R**eproducibility | Works every time once the malicious app is installed → High | **3** |
| **E**xploitability | Needs a malicious app installed + permission → Medium | **2** |
| **A**ffected users | Only users on that one device → Low | **1** |
| **D**iscoverability | Local DB location is well known → High | **3** |

Sum = 2+3+2+1+3 = **11**; average = 11 / 5 = **2.2**.

Repeat for Threats B and C, then **rank by average** — higher average = higher priority (L08 p.47).

How this differs from a **risk matrix** (L08 p.48): the matrix plots each threat on a **3×3 Impact (Minor/Moderate/Severe) × Likelihood (Unlikely/Possible/Likely)** grid, so it collapses everything into two axes and reads priority by *colour zone* (severe+likely = red/high). DREAD's five factors give a finer-grained numeric ranking and can separate threats the 3×3 grid would land in the same cell — but it can also obscure a single catastrophic factor by averaging it away. So DREAD might rank A above B on the *average*, while a risk matrix could tie them if both are "Moderate × Possible." Reconcile by checking whether any single high-Damage threat deserves to jump the queue regardless of its average ("easy fixes first" / "bug bar", L08 p.46).

### [HARD] A reviewer claims your threat model is "done" because you produced a DFD and a STRIDE table. Per the chapter's validation step, list what still needs checking and what "validate threats are addressed" specifically requires.

**Answer:** A DFD + STRIDE table is only the *find* stage. Validation = **"Quality Assurance for Threat Models"** and has **two prongs** (L08 p.49–50):

**(1) Validate the threat model itself** — gather everyone involved and ask (L08 p.50): Is it **complete**? **accurate**? Does it cover **all the security decisions** we made? Should we move to a newer version? Then **re-walk the diagram** asking (L08 p.51):

- Have we checked **every part** for threats?
- Have we considered relevant **attack trees**?
- Have we gone through the **whole STRIDE list**?
- Is there a **bug-tracker issue for each threat** (complete list)?
- Have we **listed all assumptions**?

Also apply the update rules: focus on data flow not control flow, vague phrasing → more detail, **no dead ends** (L08 p.52).

**(2) Validate that identified threats are addressed** (the half people forget, L08 p.52):

- Does the model **match reality**?
- For **each** threat, is there documentation of the **risk**, the **strategy** addressing it, and a **test**?
- Has **every threat issue been closed**, and are the tests folded into the dev/deployment procedure?

So "done" is wrong: the reviewer has skipped both prongs. The model needs the completeness re-walk **and** evidence that each threat has a strategy + test + closed issue.

### [VERY HARD] The health app evolves into a fitness tracker: it now ingests data from third-party Bluetooth devices, processes/cleans the data, users can no longer edit manually, and data is stored both locally and in the cloud. Describe how the DFD changes (new elements and trust boundaries) and give one new STRIDE threat for each of the three new attack surfaces.

**Answer:** This is the lab's Exercise 4 evolution (E08 p.3). DFD changes:

**New elements:**

- **External entities:** the **third-party Bluetooth device(s)** (everything but your code/data, incl. cloud software counts as external) and the **cloud service**.
- **Processes:** a **data processing/cleaning/computation** process (steps, distance, calories, sleep). The previous "manual edit" CRUD flow is **removed** (users can no longer edit).
- **Data stores:** now **two** — the **local DB** *and* **cloud storage**.
- **Data flows:** "sensor data over Bluetooth", "cleaned/computed metrics", "sync to cloud", "fetch from cloud".

**New trust boundaries (dashed):** (1) the **Bluetooth wireless link** (device ↔ app) and (2) the **device ↔ cloud link**. These are the new high-risk zones since they introduce new principals of different privilege (L08 p.21; E08 p.3).

```
[BT Device]==BT link==>[ Fitness App ]--sync-->[ Cloud Svc ]
   (ext)    : TB(BT)   ( process: clean/  : TB(cloud)  (ext)
            :           compute )    |                  |
            :                        v               == Cloud
            :                    == Local DB ==          Store ==
```

**One new STRIDE threat per new surface** (E08 p.3 says STRIDE must now cover external devices, wireless comms, and cloud storage):

1. **Bluetooth device (external device):** **Spoofing** — an attacker **spoofs a paired Bluetooth device** to feed fake sensor data (violates Authentication).
2. **Wireless link (Bluetooth in transit):** **Tampering / Information disclosure** — **tamper with or sniff data in transit** over the air (violates Integrity / Confidentiality); also DoS by **flooding the wireless channel** (Availability).
3. **Cloud storage:** **Information disclosure** — health data **leaks from cloud storage**; or **Elevation** via the cloud service to other tenants' data (Confidentiality / Authorization).

Because the model changed, the chapter requires re-running the flow — threat modeling is **continuous**: the system changed, so re-validate the DFD and STRIDE (L08 p.53; E08 p.3–4).

### [VERY HARD] For the spoofed-Bluetooth-device threat in the fitness tracker, work through all four addressing strategies (mitigate/eliminate/transfer/accept), state which the chapter would favour and why, and name the concrete mitigation technology STRIDE maps to spoofing.

**Answer:** The threat: an attacker **spoofs a paired Bluetooth device** to inject fake/malicious sensor data (a **Spoofing** threat → violates **Authentication**, L08 p.29). Working all four strategies (L08 p.43), remembering **trade-offs always exist**:

1. **Eliminate** — remove the responsible functionality, i.e. drop third-party Bluetooth ingestion entirely. This is the chapter's *best* fix ("remove the functionality" → the Heartbleed logic, L08 p.45): no Bluetooth pairing, no spoofing of it. **Trade-off:** you lose the tracker's core value proposition (it *is* a Bluetooth fitness tracker), so elimination is usually not viable here.
2. **Mitigate (the default)** — make spoofing harder by **authenticating the device**. STRIDE maps **Spoofing → Authentication**, with concrete technologies being **digital signatures, Active Directory/LDAP** (developer) and **passwords / crypto tunnels** (sysadmin) (L08 p.45). The lecture also states **cryptography is required over a network** — use SSL/TLS-style authentication and **authenticate the bits** with signatures/hashes (L08 p.44). Concretely: cryptographic pairing/bonding and signed/authenticated sensor payloads.
3. **Transfer** — let someone else handle it, e.g. rely on the **device vendor's / OS Bluetooth stack's** authenticated pairing, or use a managed BLE security layer, shifting responsibility for link authentication (L08 p.43).
4. **Accept** — only if it "cannot be addressed in another reasonable manner" (L08 p.43); not justified here since strong mitigation exists.

**Which the chapter favours:** *Eliminate* is theoretically best, but since removing Bluetooth guts the product, the realistic favourite is **Mitigate** — it is the **default**, and the spoofing-specific mitigation technology is **Authentication** (cryptographic pairing + authenticated/signed payloads over a crypto tunnel) (L08 p.43–45).

### [VERY HARD] Two trust boundaries cross the same data flow in your model: "sensor data" travels Bluetooth (device→app) and is then synced to the cloud (app→cloud). Explain why this single flow can carry threats from multiple STRIDE letters, and how validation rules ("no dead ends", "list assumptions", "data flow not control flow") would catch a sloppy model here.

**Answer:** A single labelled flow can carry **multiple STRIDE threats** because STRIDE is applied **per element against every category** (L08 p.37), and this flow physically crosses **two trust boundaries** — exactly where threats cluster (L08 p.21). On one "sensor data" flow you can find:

- **S**poofing — a fake device or fake cloud endpoint impersonates a legitimate one (Authentication).
- **T**ampering — data altered in transit over BT or over the cloud link (Integrity).
- **I**nformation disclosure — sniffing the wireless link or the device→cloud channel (Confidentiality).
- **D**enial of service — flooding the channel so data can't sync (Availability).

So one arrow legitimately yields four-plus threats; treating it as "one threat" is the partial-coverage failure the chapter warns about (L08 p.482).

How the validation rules catch a sloppy version (L08 p.51–52):

1. **"No dead ends"** — if the diagram shows "sensor data" arriving at the app but never reaching a store or the cloud, that dangling flow is a **dead end**, signalling an incomplete data flow model. The reviewer must trace it through to the local DB / cloud store.
2. **"List all assumptions"** — the model implicitly assumes the Bluetooth pairing is authenticated and the cloud channel is TLS. If those assumptions aren't **written on the diagram**, validation fails (L08 p.51; E08 p.2, p.4). Unlisted assumptions hide the very trust the spoofing/disclosure threats target.
3. **"Focus on data flow, not control flow"** — if the modeler drew *control* logic ("if device connected then sync") instead of the data exchange, they've drawn an activity diagram, not a DFD (L08 p.23, p.52). The fix is to model *what data moves across each boundary*, since "every transition indicates processing" — which forces them to expose the cross-boundary hop where the threats live.

Because the model spans two boundaries with shared data, the chapter's mandate to **re-walk every part with the whole STRIDE list** and keep the process **continuous** is what surfaces the full threat set rather than a single under-counted entry (L08 p.51, 53).

### [VERY HARD] A stakeholder wants to "transfer" all health-data confidentiality risk to the cloud provider and "accept" everything else to ship faster. Critique this plan using the chapter's guidance on strategy trade-offs, validation, and the nature of threat modeling as a process.

**Answer:** The plan misuses two of the four strategies and skips validation. Critique grounded in the chapter:

1. **"Transfer everything to the cloud provider" is incomplete.** Transferring is legitimately "let somebody else handle the problem" (L08 p.43), but confidentiality risk doesn't fully leave you: the data still crosses **your** trust boundaries (device→cloud) and sits in **your** local store too (the evolved app stores **both locally and in the cloud**, E08 p.3). Information disclosure can occur at the local DB or in transit before the provider ever sees the data, so transfer covers only part of the surface. The lecture's mitigation for information disclosure is **permissions + encryption** (PGP/SSL/crypto tunnels) (L08 p.45) — you can't outsource the in-transit and at-rest-on-device pieces. And there are **almost always trade-offs** (L08 p.43): transferring shifts responsibility but adds dependency and contractual/residual risk.

2. **"Accept everything else" violates the strategy rule.** Accepting is only for threats that **cannot be addressed in another reasonable manner** (L08 p.43). Spoofing, tampering and elevation here *can* be addressed cheaply (authentication, signatures, isolation per the L08 p.45 table), so blanket acceptance is improper — especially for **Elevation of Privilege**, which would let an attacker reach the whole health DB. The chapter's prioritization tools (DREAD, risk matrix) exist precisely so you accept *low* Impact×Likelihood items, not high ones (L08 p.46–48). A severe+likely threat parked as "accepted" lands in the red zone of the risk matrix (L08 p.48).

3. **Validation would reject this.** Validating "threats are addressed" requires, for **each** threat, a documented **risk + strategy + test**, with **every threat issue closed** (L08 p.52). "Accept to ship faster" with no analysis means there is no per-threat documentation or test — a validation failure on its face (L08 p.50, 52). You'd also have skipped re-walking STRIDE and listing assumptions (L08 p.51).

4. **It treats threat modeling as one-off.** The chapter is explicit that it is a **continuous process** — the system changes, attack patterns change, new attacks appear, and it continues even for the deployed product (L08 p.53). "Ship faster and accept" freezes the model at a single point and abandons the loop.

**Better plan:** Eliminate where feasible; **mitigate** spoofing/tampering/EoP with the STRIDE-mapped technologies (authentication, signatures, encryption, isolation, L08 p.45); **transfer** only the parts genuinely owned by the provider while keeping local/in-transit encryption yourself; **accept** only low-ranked residual items after DREAD/risk-matrix scoring; then **validate** (risk + strategy + test + closed issue per threat) and keep re-running the flow as the product evolves.

### [VERY HARD] A teammate decomposes the "College Library Website" process (a multi-process / double circle) into a Level-2 DFD, but applies STRIDE only to the top-level Level-1 box, not the new sub-elements. Explain, using the chapter's notions of decomposition, trust boundaries, "think like an attacker" risk, and validation, why this under-models the system — and outline the correct procedure.

**Answer:** The error conflates *modelling* completeness with *threat-finding* completeness across DFD levels.

1. **Decomposition creates new elements that STRIDE has never seen.** A **double circle = multi-process**, signalling a component meant to be **expanded into a lower-level sub-diagram** (L08 p.17, 19). The Level-1 → Level-2 progression *is* decomposition (the OWASP "Decompose Application" step, L08 p.13; the College Library example, L08 p.20). When the multi-process is expanded, it yields new **processes, data stores, data flows and external entities** — e.g. "Web Pages on Disk", "Database Files", flows labelled Requests/Responses/SQL Query Calls/Pages/Data (L08 p.20). STRIDE is a **per-element checklist — each category against each part** (L08 p.37, p.482). Applying it only to the collapsed Level-1 box means none of these sub-elements were checked, so whole threat classes are silently dropped (e.g. tampering with "Database Files", information disclosure on the SQL Query Call flow).

2. **Decomposition exposes *new* trust boundaries.** The College Library Level-2 diagram shows dashed trust boundaries separating users↔website and website↔database (L08 p.20). Those inner boundaries don't exist at Level 1 — and **threats cluster around trust boundaries** (L08 p.21). Skipping the sub-elements means skipping exactly the highest-risk zones the decomposition was meant to reveal.

3. **It is *not* rescued by "thinking like an attacker."** One might argue "an attacker only sees the website, so the inner boundary doesn't matter." But the chapter warns that **"think like an attacker" is risky** — guess the attacker's knowledge/intent wrong and the whole model goes astray (L08 p.10). The system-centric DFD+STRIDE method exists precisely so completeness doesn't depend on a guessed attacker viewpoint; under-applying STRIDE re-introduces that fragility.

4. **Validation will (and should) fail this.** Re-walking the diagram asks: have we checked **every part** for threats? gone through the **whole STRIDE list**? made a **complete list** (a bug-tracker issue per threat)? listed all assumptions? (L08 p.51). A Level-2 diagram with Level-1-only STRIDE fails "every part." Also, a DFD must have **no dead ends** and **vague labels signal missing detail** (L08 p.52) — if the decomposed flows are present but unanalyzed, the model is internally inconsistent.

**Correct procedure:**

```
1. Decompose the multi-process into its Level-2 DFD
   (new processes, stores, flows, external entities, inner trust boundaries).
2. List EVERY element at the level you intend to analyze,
   flagging those on/crossing the new trust boundaries.
3. Apply ALL SIX STRIDE letters to EACH element
   (use attack libraries + the relevant attack tree as inspiration).
4. Record each threat in the STRIDE table; open a bug-tracker issue per threat.
5. Validate: every part checked? whole STRIDE list? all assumptions listed?
   no dead ends? Then confirm each threat has risk + strategy + test + closed issue.
6. Treat as continuous — re-run when the model decomposes further or changes.
```

The principle: **the level you analyze with STRIDE must match the level you decomposed to** — modelling deeper without finding threats deeper just hides risk behind a more detailed picture (L08 p.13, 19–20, 37, 51).
