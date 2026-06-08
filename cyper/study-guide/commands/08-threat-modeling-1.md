# 08. Threat Modeling I — Commands & Code Examples

### Sketch the DFD element/notation legend
**What:** Reproduce the five DFD symbols from memory before drawing any diagram — the marker often wants the notation key explicitly (L08 p.17–18).
```text
DFD NOTATION KEY (L08 p.17–18)
+-------------------+-----------------------------------+-------------------------+
| Element           | Meaning                           | Symbol (ASCII)          |
+-------------------+-----------------------------------+-------------------------+
| External Entity   | Everything but YOUR code/data     |  +-----------+          |
|                   | (people, cloud, other systems)    |  |  User     |          |
|                   |                                   |  +-----------+          |
+-------------------+-----------------------------------+-------------------------+
| Process           | YOUR code / a component           |  (  Process  )          |
|                   | (rounded rect OR circle)          |                         |
+-------------------+-----------------------------------+-------------------------+
| Multi-Process     | Process to be decomposed further  |  (( Process ))          |
|                   | (double circle)                   |                         |
+-------------------+-----------------------------------+-------------------------+
| Data Store        | Files, databases, shared memory   |  === Data Store ===     |
|                   | (two parallel lines)              |  (open-ended rectangle) |
+-------------------+-----------------------------------+-------------------------+
| Data Flow         | Data moving between elements      |  ---- "label" ---->     |
|                   | (labelled arrow)                  |                         |
+-------------------+-----------------------------------+-------------------------+
| Trust Boundary    | Where principals of DIFFERENT     |  - - - - - - - - - -    |
|                   | privilege interact                |  (dashed line / box)    |
+-------------------+-----------------------------------+-------------------------+
```
**Notes:** Trust boundary is the "crucial fifth annotation," not one of the four element *types* (L08 p.17). Common mistakes: drawing a single open rectangle for a process (that's an external entity), or forgetting to **label every data flow** with the data it carries (e.g. "Requests", "SQL Query Calls", "Data") (L08 p.73). External entity = "everything *but* your code and data" — your own DB is a data store, not external (L08 p.74).

### Draw a worked DFD (Level 2 College Library Website)
**What:** Reproduce the slide's library example as ASCII when asked to "draw a DFD for system X" — copy this skeleton and swap in your system's names (L08 p.20).
```text
LEVEL 2 DFD — College Library Website (L08 p.20)

  +-----------+                                  +--------------+
  |  Users    |                                  | Librarians   |
  +-----------+                                  +--------------+
        |  Requests                                     |  Requests
        v  ^ Responses                                  v
  - - - - - - - - - - - - - - - - - TRUST BOUNDARY - - - - - - - - - -
        |  ^                                            |
        v  | Pages                                      v
  (( College Library Website ))  <---- Pages ----  === Web Pages on Disk ===
        |  ^
        |  | SQL Query Calls / Data
        v  |
  - - - - - - - - - - - - - - - - - TRUST BOUNDARY - - - - - - - - - -
        |  ^
        v  | Data
  (( College Library Database )) <---- Data ----  === Database Files ===
```
**Notes:** Double circles `(( ... ))` mark *multi-processes* (the website and database, drawn as decomposable processes) (L08 p.86). The two dashed lines separate Users from the website and the website from the database — **threats cluster on these boundaries** (L08 p.21). Every arrow is labelled (Requests/Responses/Pages/SQL Query Calls/Data). The Level 1 → Level 2 jump is *decomposition* (OWASP "Decompose Application", L08 p.13, 88).

### Fill the STRIDE → security-property mapping table
**What:** Write the canonical six-row table — the single most likely STRIDE exam question, "what does each letter violate?" (L08 p.29).
```text
STRIDE TABLE (L08 p.29)
+---+------------------------+----------------------+--------------------------------------+
| - | Threat                 | Property Violated    | Definition                           |
+---+------------------------+----------------------+--------------------------------------+
| S | Spoofing               | Authentication       | Impersonating something/someone else |
| T | Tampering              | Integrity            | Modifying data or code               |
| R | Repudiation            | Non-repudiation      | Claiming to have not performed action|
| I | Information Disclosure  | Confidentiality      | Exposing info to the unauthorized    |
| D | Denial of Service      | Availability         | Deny or degrade service to users     |
| E | Elevation of Privilege | Authorization        | Gain capabilities w/o authorization  |
+---+------------------------+----------------------+--------------------------------------+
```
**Notes:** Memorise the pairing exactly — common slips: Repudiation ↔ **Non-repudiation** (NOT integrity), Spoofing ↔ **Authentication**, EoP ↔ **Authorization** (NOT authentication) (L08 p.483). The order is fixed by the mnemonic S-T-R-I-D-E.

### Build a STRIDE-per-element table
**What:** The deliverable for "apply STRIDE to your DFD" — one row per element, one finding per relevant STRIDE letter (L08 p.37, E08 p.2–3).
```text
STRIDE-PER-ELEMENT TABLE
+----------------------+--------+---------------------------------------------+
| Element (DFD part)   | STRIDE | Threat description                          |
+----------------------+--------+---------------------------------------------+
| User (ext. entity)   | S      | Attacker spoofs another user at login       |
|                      | R      | User denies deleting an entry (no audit log)|
+----------------------+--------+---------------------------------------------+
| Health App (process) | T      | Tamper with locally stored health records   |
|                      | E      | Malicious local app escalates to read DB    |
+----------------------+--------+---------------------------------------------+
| Local DB (store)     | I      | Another app reads the local database         |
|                      | D      | Fill local storage so the app can't save    |
+----------------------+--------+---------------------------------------------+
| Login flow (flow)    | T      | Tamper with credentials in transit          |
+----------------------+--------+---------------------------------------------+
```
**Notes:** Apply **each** STRIDE category to **each** element — it is an exhaustive per-element checklist, not a brainstorm; partial coverage fails validation (L08 p.37, 482). Aim for **multiple examples per category** (E08 p.2). Give boundary-crossing elements the hardest scrutiny (L08 p.21). The rows above are the lab's Android-health-app answers (E08 p.2).

### Lay out an attack-tree (AND/OR) ASCII template
**What:** Skeleton for "draw an attack tree for goal G" — shows root, OR-branches, AND-branches, and leaf nodes (L08 p.38, 41).
```text
ATTACK TREE TEMPLATE (graphical view, L08 p.38)

                 [ROOT = Attacker's GOAL]
                          |
       +------------------+------------------+      <- OR: any branch achieves goal
       |                  |                  |
   (Sub-goal A)      (Sub-goal B)       (Sub-goal C)
       |                  |
   +---+---+          [AND]                          <- AND: ALL children required
   |       |         /     \
 (leaf)  (leaf)  (leaf)   (leaf)

LEGEND:
- ROOT      = the security incident that is the attack goal
- Sub-nodes = ways an attacker could reach the goal
- Leaf node = a concrete way to INITIATE the attack
- OR  node  = goal met if ANY child succeeds (default branching)
- AND node  = goal met only if ALL children succeed
```
**Notes:** Root = goal, leaves = ways to *initiate*, sub-nodes in between (L08 p.38). Mark each junction OR (default) or AND. The same tree can be drawn graphically OR written as an outline — they are interchangeable views (L08 p.39). Create-vs-use distinction: you may *use* an existing tree (web search → "does this apply here?") rather than build one (L08 p.39, 41).

### Write an attack tree as a textual outline
**What:** The interchangeable outline form — fast to type in an exam and equivalent to the diagram (L08 p.39).
```text
Goal: Access to the building
  1. Go through a door
     a. When it's unlocked
        i.   Get lucky
        ii.  Observe the latch plate
        iii. Distract the person
     b. Drill the lock
     c. Pick the lock
     d. Get the key
  2. Go through a window
  3. Go through a wall
```
**Notes:** Numbered/lettered indentation encodes the hierarchy: top-level items (1, 2, 3) are OR sub-goals; deeper items are the ways to initiate (leaves) (L08 p.178). Creation steps: choose representation → create root node ("the goal") → add sub-nodes → consider completeness → prune and check (L08 p.41). Use this when a diagram is awkward to draw by hand.

### Outline the Internet Banking Authentication attack tree
**What:** Reproduce the lecture's worked tree when asked for a realistic example, not the toy "building" one (L08 p.40).
```text
Goal (ROOT): Bank Account Compromise
  1. User credential compromise
     a. User surveillance                         [UV/Cx]
     b. Theft of token and handwritten notes      [UT/Cx]
     c. Malicious software installation
     d. Brute-force with PIN calculators          [BBx]
     e. User communication with attacker
  2. Injection of commands                         [CCx]
  3. User credential guessing
  4. Use of known authenticated session by attacker
     a. Session hijacking                          [SSx]
     b. Normal user auth with specified session ID
```
**Notes:** Leaf nodes are *coded* (UT/Cx, UV/Cx, CCx, BBx, SSx) so each maps back to a specific documented technique (L08 p.180). Root is the incident/goal; the four numbered sub-goals are OR branches. Don't list mitigations here — an attack tree captures *attacker paths*, not defences.

### Build a DREAD scoring table
**What:** The deliverable for "prioritise these threats with DREAD" — five factors, scored, summed, averaged (L08 p.46–47).
```text
DREAD SCORING (score each factor High=3 / Med=2 / Low=1, then average)
+-----------+---+---+---+---+---+-------+---------+
| Threat    | D | R | E | A | D | Sum   | Average |
+-----------+---+---+---+---+---+-------+---------+
| Threat 1  | 1 | 2 | 2 | 1 | 3 |   9   |   1.8   |
| Threat 2  | 3 | 3 | 2 | 3 | 2 |  13   |   2.6   |  <- higher = prioritise
+-----------+---+---+---+---+---+-------+---------+

DREAD factors:
- D  Damage potential       (High=3 run as admin / Med=2 reveal sensitive data / Low=1 reveal data)
- R  Reproducibility
- E  Exploitability
- A  Affected users
- D  Discoverability
```
**Notes:** TWO D's — Damage potential **and** Discoverability; dropping one is the classic error (L08 p.481). Scale each factor high→low, assign points, then **sum and average** (not just count) (L08 p.46–47). The worked slide scored Threat 1's Damage = 1 (Low) using the Damage scale shown above (L08 p.47). Sum/average columns above are illustrative arithmetic on the lecture's scoring scheme.

### Plot a 3x3 risk matrix (Impact x Likelihood)
**What:** The alternative to DREAD — place numbered threats on an Impact × Likelihood grid (L08 p.48).
```text
RISK MATRIX (Shabtai et al. 2010, L08 p.48)
                 LIKELIHOOD ->
                 Unlikely   Possible   Likely
IMPACT  Severe  | MEDIUM   | HIGH     | HIGH   |   <- Severe+Likely = red / top priority
   ^    Moderate| LOW      | MEDIUM   | HIGH   |
   |    Minor   | LOW      | LOW      | MEDIUM |   <- Minor+Unlikely = green / low priority
```
**Notes:** Define a scale for **Impact** (Minor/Moderate/Severe) and **Likelihood** (Unlikely/Possible/Likely), then drop each numbered threat into a cell (L08 p.48). Severe+Likely is red/high priority; Minor+Unlikely is green/low. This is a coarser, faster alternative to DREAD's averaging.

### Track threats → mitigation in a table
**What:** The "Address Threats" deliverable and a validation aid — one row per threat with strategy, mitigation, and test (L08 p.43, 52).
```text
THREAT -> MITIGATION TRACKING
+-----+---------------------------+----------+----------------------+--------------------+--------+
| ID  | Threat (STRIDE)           | Strategy | Mitigation / Tech    | Test               | Status |
+-----+---------------------------+----------+----------------------+--------------------+--------+
| T1  | Spoof user at login (S)   | Mitigate | MFA + crypto tunnel  | auth bypass test   | Closed |
| T2  | Tamper records (T)        | Mitigate | Digital signatures   | integrity check    | Open   |
| T3  | SSL heartbeat bug (I)     | Eliminate| Remove heartbeat fn  | feature absent     | Closed |
| T4  | Card-fraud loss (R)       | Transfer | 3rd-party processor  | n/a (transferred)  | Open   |
| T5  | Rare disk-fill DoS (D)    | Accept   | documented residual  | n/a (accepted)     | Open   |
+-----+---------------------------+----------+----------------------+--------------------+--------+
```
**Notes:** Strategy is one of **Mitigate (default) / Eliminate / Transfer / Accept** (L08 p.43). Eliminate beats mitigate — "if SSL didn't have a heartbeat, Heartbleed couldn't exist"; keep the feature and you "can only mitigate, not fix" (L08 p.45). Validation requires each threat have a documented **risk + strategy + test**, and every issue **closed** (a bug-tracker issue per threat) (L08 p.52). Map mitigations from the STRIDE table: Spoofing→authentication, Repudiation→logging+secure timestamps, Info disclosure→permissions+encryption (L08 p.44–45). **Fuzzing is a *test*, not a mitigation** (L08 p.45).

### Model a system with pytm (standard tooling)
**What:** When asked to "use a tool" or define a DFD as code, the pytm framework expresses elements, dataflows, and boundaries in Python (standard tooling — pytm is OWASP's Pythonic Threat Modeling library; not named in the course, which uses hand-drawn DFDs).
```python
from pytm import TM, Server, Datastore, Actor, Dataflow, Boundary

tm = TM("Android Health App")
tm.description = "User stores health data locally on device"

# Trust boundaries (where principals of different privilege interact)
internet = Boundary("User Zone")
device   = Boundary("Device / OS")

# Elements
user   = Actor("User")
app    = Server("Health App")
localdb = Datastore("Local Health DB")
user.inBoundary    = internet
app.inBoundary     = device
localdb.inBoundary = device

# Data flows (each carries labelled data, like DFD arrows)
login = Dataflow(user, app, "Login credentials")
login.protocol = "HTTPS"
store = Dataflow(app, localdb, "CRUD health data")

if __name__ == "__main__":
    tm.process()   # generates DFD + STRIDE report:  python tm.py --dfd | --report
```
**Notes:** (standard tooling — pytm.) Mirrors the four DFD element types in code: `Actor`=external entity, `Server`=process, `Datastore`=data store, `Dataflow`=labelled flow, `Boundary`=trust boundary (L08 p.17). Running `--dfd` emits Graphviz/PlantUML; `--report` auto-derives STRIDE threats per element — the same per-element walk you'd do by hand (L08 p.37). For an exam, expect to *hand-draw* the DFD (L08 p.14); this snippet shows how the manual process maps to real tooling. Other named tools: **OWASP Threat Dragon** and **Microsoft TMT** (GUI DFD + STRIDE editors — standard tooling), and the **EoP card game** referenced in the lab (E08 p.2).

### Use the validation checklist as a re-walk script
**What:** The "Validate" step deliverable — run this checklist over your finished model to catch gaps (L08 p.50–52).
```text
VALIDATION = QA FOR THREAT MODELS (L08 p.50-52)

A) Validate the MODEL:
   [ ] Is the model complete?
   [ ] Is the model accurate?
   [ ] Does it cover all the security decisions we made?
   [ ] Ready to move to a newer version? (update when necessary)

B) Re-walk the DIAGRAM:
   [ ] Checked EVERY part for threats?
   [ ] Considered relevant attack trees?
   [ ] Gone through the WHOLE STRIDE list?
   [ ] Complete threat list = a bug-tracker issue per threat?
   [ ] Listed ALL assumptions?

C) DFD update rules:
   [ ] Focus on DATA flow, not control flow (every transition = processing)
   [ ] Vague phrasings  ->  need more detail
   [ ] NO dead ends in the data-flow model

D) Validate threats are ADDRESSED:
   [ ] Model matches reality
   [ ] Each threat documented: risk + strategy + test
   [ ] Every threat issue CLOSED; tests folded into dev/deployment
```
**Notes:** Validation is **two-pronged** — validate the *model* AND that *threats are addressed*; people forget the second half (L08 p.50, 484). "Focus on data flow, not control flow" = a DFD shows the *exchange of data*, not program logic (activity diagrams do control flow) (L08 p.23, 52). A valid DFD has **no dead ends** and **lists all assumptions** explicitly (L08 p.52, E08 p.2). Remember it never ends — re-run as the system/threat landscape changes (L08 p.53).
