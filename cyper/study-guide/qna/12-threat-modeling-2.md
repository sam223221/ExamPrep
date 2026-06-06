# 12. Threat Modeling II — Simulated Open-Book Questions

### [EASY] A junior engineer draws a Kubernetes DFD and uses a solid arrow between the API Server and etcd, then a dashed red line wrapping the control plane. Translate both symbols into what they mean and explain which one a threat modeler cares about most.

**Answer:** Using the slide's own DFD key `(L12 p.8)`:

1. The **solid arrow** between API Server and etcd is a **Data Flow** — it shows data moving from one element to another (here, the API Server reading/writing cluster state and secrets in the etcd data store).
2. The **dashed red line** wrapping the control plane is a **Trust Boundary** — a line where the level of trust changes.

For a threat modeler, the **trust boundary** is the higher-value symbol. Threats concentrate where trust changes `(L12 p.8)`. A data flow that *crosses* a boundary is a candidate for Tampering and Information Disclosure, and a process sitting on the boundary (the API Server) is a candidate for Spoofing/Elevation of Privilege. The arrow alone is neutral; the boundary tells you *where to point STRIDE*.

### [EASY] Your team labels "don't run as root" and "use a small base image" as Cluster-layer controls. Using the 4Cs, correct them and place each control in the right layer.

**Answer:** Both labels are wrong; both belong to the **Container** layer, not Cluster `(L12 pp.6, 16)`.

The 4Cs are nested outer-to-inner `(L12 p.6)`:

1. **Cloud** — the underlying cloud infrastructure (outermost).
2. **Cluster** — Kubernetes cluster-level security (e.g. RBAC, Network Policies).
3. **Container** — security of the Dockerfile/Containerfile and the image itself.
4. **Code** — the application code (innermost).

"Don't run as root" and "the smaller the image, the better" are both about the **container image / its runtime configuration**, so they are **Container**-layer controls. Cluster-layer controls would be things like RBAC modes and Network Policies `(L12 pp.6, 15)`. The reason layering matters: an outer layer's weakness undermines everything inside it, so you must place each fix at its correct C `(L12 p.6)`.

### [EASY] You see an attack-tree node where the parent is reached only if every one of its three children is achieved. Name the node type, and state the single cheapest thing a defender can do to break that path.

**Answer:** This is an **AND node** — the parent goal succeeds only if **all** child sub-goals are achieved `(L12 p.10)`.

The cheapest defensive move is to **block just one** of the three children. Because an AND chain requires the attacker to complete *every* step, breaking any single link defeats the whole path `(L12 p.10)`. You do not need to neutralise all three — pick the one that is easiest/cheapest to block (e.g. the one with an off-the-shelf K8s control like a Network Policy or an RBAC restriction) and the attacker's path collapses. (Contrast: an **OR** node would force you to block *every* alternative, which is more expensive.)

### [EASY] A new Kubernetes cluster is deployed with default settings and no Network Policy. A teammate says "pods are isolated by default, so we're fine." Apply the lecture's fact to judge this claim.

**Answer:** The teammate is **wrong**. The lecture explicitly states that **all pods can talk to each other by default**; isolation is *not* the default `(L12 pp.15, 9)`.

Concretely:

1. With no Network Policy, every pod can reach every other pod's network endpoints — this is exactly the **"Network Endpoints"** attack vector ("access to endpoints if the pod's network policy permits it") `(L12 p.9)`.
2. The mitigation is a **Cluster**-layer control: you must **explicitly add a Network Policy** to restrict pod-to-pod traffic `(L12 p.15)`.

So the correct judgement is: a default cluster is wide open at the network layer, and the "isolated by default" assumption is a classic gotcha `(L12 p.325-style gotcha, p.15)`. Add Network Policies before claiming isolation.

### [EASY] Match the right tool to each task: (a) confirm the cluster was deployed per the CIS benchmark, (b) scan a container image for known vulnerabilities. Pick from kube-bench, Kubesec, Clair, Kubescape, Notary.

**Answer:** From the lecture's tool→purpose mapping `(L12 p.17)`:

- **(a) Confirm CIS-benchmark/secure deployment → kube-bench.** kube-bench (Aqua) checks whether Kubernetes is securely deployed against the CIS benchmark.
- **(b) Scan a container image for known vulnerabilities → Clair.** Clair performs static analysis of vulnerabilities in containers (image scanning).

For completeness, the others: **Kubesec** does security risk analysis of K8s resources; **Kubescape** is a broad platform that scans clusters, manifests, code repos, registries and images; **Notary** signs and verifies artifacts to secure update distribution `(L12 p.17)`. Note Kubescape *could* also cover image scanning, but the precise, single-purpose answer for "known vulns in an image" is **Clair**.

### [MEDIUM] An attacker has compromised a pod and wants to start an arbitrary process directly on the worker-node host. List two distinct leaf conditions from the lecture's trees that would enable this, and give the matching mitigation for each.

**Answer:** From the malicious-code / host-process branches `(L12 pp.10, 12)`, two distinct enabling leaf conditions are:

1. **Pod/Container with a mounted Docker socket [M8 — start process using container runtime].** A mounted Docker socket lets the compromised container drive the host's container runtime, effectively giving host-level code execution / container escape.
   - **Mitigation:** **Pod Security Policy** forbidding such mounts, plus **limit host mounts** and **minimize privilege** (best practices) `(L12 pp.15, 16)`.
2. **Pod/Container with HostPID (or SYS_PTRACE capability) [M9 — start child process in host PID namespace].** HostPID places the container in the host's PID namespace; SYS_PTRACE lets it trace/manipulate other processes — both enable manipulating host processes.
   - **Mitigation:** **Pod Security Policy** to deny HostPID and drop the SYS_PTRACE capability; **don't run privileged/root containers** `(L12 pp.15, 16)`.

Both leaves are recurring single mis-configurations that unlock host-level attacks, so they are high-value to close `(L12 p.328-style gotcha)`.

### [MEDIUM] You are reviewing the DoS attack tree. Explain why "bring etcd down" and "bring the scheduler down" produce different cluster symptoms, and name the ports each targets.

**Answer:** The two sub-goals hit different control-plane functions, so the cluster fails in different ways `(L12 p.11)`:

1. **Bring etcd down →** etcd is the key-value store holding cluster state. DoSing it causes **loss of etcd quorum**, preventing the cluster from maintaining/changing its desired state and breaking internal consistency `(L12 p.11)`. Ports: **etcd peer port 2380 [D5]** and **etcd client port 2379 [D5]**.
2. **Bring the scheduler down →** the scheduler assigns pods to nodes. DoSing it **prevents rescheduling of workloads** — existing pods may keep running, but nothing new gets placed and failed pods are not re-placed `(L12 p.11)`. Ports: **scheduler port 10251 [D4] / 10259 [D3]**.

The unifying insight: each control-plane component listens on its own port, so **each port is an independent DoS target**, and which component you kill determines the symptom (lost quorum vs. stalled scheduling) `(L12 pp.11, 120-style note)`.

### [MEDIUM] A leaf in the persistence tree says "create a restarting container on the host using Docker restart-always." Which persistence level is this, and why does the attacker prefer it over simply "start a process in a running container"?

**Answer:** This leaf belongs to **"Foothold with resilience to node restart"** `(L12 p.13)`.

Why it is preferred over a plain in-container process:

1. A process merely started **in a running container** is **"Foothold with no resilience"** — it dies the moment the container, pod, or node restarts `(L12 p.13)`.
2. A **Docker `restart-always` container on the host** survives a **node restart**: when the host comes back up, the runtime automatically re-launches the malicious container, re-establishing the foothold without any further attacker action `(L12 p.13)`.

So the attacker climbs the resilience ladder — from no resilience → container-restart → pod deletion → **node restart** → node rebuild — to make the foothold survive progressively more disruptive lifecycle events `(L12 pp.13, 314-style)`. The trade-off is that deeper persistence usually needs more privilege (e.g. host access / docker socket), which is exactly where the defender should apply Pod Security Policies and limit host mounts.

### [MEDIUM] Translate this short attack-tree fragment into prose and identify the AND/OR logic: root "poison image in container registry" requires "obtain image pull secret", which requires "pull-secret has write/overwrite privileges" together with ONE of {make a K8s API request, use a container with host filesystem access, read the secret from the Kubelet}.

**Answer:** In prose `(L12 p.12)`:

To **poison the image in the container registry**, the attacker must **obtain the image pull secret**. Obtaining that secret has two requirements combined as an **AND**:

1. The **pull-secret must have write/overwrite privileges** (a read-only pull secret cannot poison the registry), **AND**
2. The attacker must retrieve the secret by **any one** of three alternatives (an **OR** node):
   - make a **K8s API request** for it, **OR**
   - use a running container that has **host filesystem access** to read it, **OR**
   - **read the K8s secret from the Kubelet**.

So the logic is: `write-privilege AND (API request OR host-FS access OR Kubelet read)`. For a defender this is useful — the **AND** on "write/overwrite privilege" is the single cheapest cut: make pull secrets **read-only** and the whole "poison the registry" branch is broken regardless of the three OR alternatives `(L12 pp.12, 311-style)`.

### [MEDIUM] During validation you run kube-bench and it passes, but a teammate concludes "the cluster is therefore secure against the modeled attack trees." Critique this conclusion and name two other tools that close the gap.

**Answer:** The conclusion **overstates** what kube-bench proves. kube-bench only checks whether **Kubernetes is securely deployed against the CIS benchmark** — i.e. cluster configuration conformance `(L12 p.17)`. It says nothing about vulnerable container images, risky resource manifests, or RBAC over-permissioning in the way the attack trees exploit them.

Gaps and the tools that close them `(L12 p.17)`:

1. **Vulnerable images** (the "poisoned/exploitable image" leaves) → **Clair** for static vulnerability analysis of container images.
2. **Risky resource definitions** (e.g. privileged pods, host mounts that appear as attack-tree leaves) → **Kubesec** for security risk analysis of K8s resources; or **Kubescape** for a broad scan across clusters, manifests, registries and images.

Also, validation is not a single tool run — it is **step 4 of an iterative loop** (Model → Find → Address → Validate → back to Model) and includes reviewing **audit logs** `(L12 pp.4, 15)`. A single passing scan is necessary but not sufficient.

### [HARD] Build an attack tree (root → leaves, with AND/OR) for the goal "Write a new workload directly into etcd," grounded in the lecture, then identify the single highest-leverage mitigation.

**Answer:** Reconstructing the etcd branch of the DoS tree `(L12 pp.10, 308-style)`:

```
GOAL: Write new workload directly into etcd data store
  AND
  ├── Obtain/authenticate to etcd          (OR)
  │     ├── Have the etcd encryption key
  │     │     (note: accessible on the master node)
  │     └── Use the K8s API client certificate to authenticate to etcd
  │           AND
  │           └── Obtain the client certificate from the master node
  │                 OR
  │                 ├── Find privileged workload scheduled on master node
  │                 └── Find workload with unrestricted host filesystem access
  └── Ability to reach / write the etcd store
```

Reading the logic: writing to etcd needs **both** a way to authenticate **AND** reachability; authentication is an **OR** between the encryption key and the API client cert, and getting that cert is itself an **AND/OR** rooted on **master-node compromise** `(L12 p.10)`.

**Highest-leverage mitigation:** every authentication path funnels through artifacts **on the master node** (encryption key, client certificate, privileged master-node workloads). So **protecting the master node and forbidding privileged/host-filesystem-access workloads from being scheduled there** (Pod Security Policies + minimize privilege + RBAC/scheduling restrictions) cuts the shared prerequisite of *both* OR branches at once `(L12 pp.10, 15, 16)`. This is the "close the most-reused leaf" prioritisation principle `(L12 p.262-style cookbook)`.

### [HARD] You must threat-model a brand-new internal CI/CD service (developers push code; it builds images and deploys them to a shared K8s namespace). Run the lecture's four-step workflow and produce concrete artifacts for steps 1–2.

**Answer:** Applying the four-step loop `(L12 pp.4, 241-style cookbook)`:

**Step 1 — Model the system (DFD).** Draw components, stores, flows, boundaries:

```
[Developer] --push--> (CI/CD Build Service) --image--> [Image Registry / data store]
                              |                                  |
                         (uses pull/push secret)            (image manifest+blobs)
                              v                                  v
                       (API Server) --reads/writes--> [etcd data store]
                              |
                         (Kubelet) --pulls image--> runs (Pods/Containers)
- - - - dashed red trust boundaries: dev↔CI, CI↔registry, cluster↔registry, around the pod - - - -
```

**Step 2 — Find threats (attack vectors crossing those boundaries)** `(L12 p.9)`:

1. **Compromised container** — a malicious build step gives a remote execution point inside the cluster.
2. **Service Token Compromise** — the CI service's service-account token grants API access; if leaked → unauthorized cluster control.
3. **Pull/push-secret abuse** — if the registry credential has **write/overwrite** privilege, an attacker can poison images `(L12 p.12)`.
4. **Network Endpoints** — without a Network Policy, the CI pod reaches every other pod `(L12 pp.9, 15)`.
5. **RBAC mis-configuration** — over-broad roles let the CI service do more than build/deploy `(L12 p.9)`.

**Step 3 — Address** (preview): read-only pull secrets, least-privilege RBAC for the CI service account, Network Policy scoping the CI pod, Pod Security Policy (no host mounts/HostPID), K8s Secrets not ConfigMaps `(L12 pp.15, 16)`.

**Step 4 — Validate:** kube-bench (deployment), Kubesec/Kubescape (manifests), Clair (built images), Notary (sign images), audit logs — then **iterate** when the pipeline changes `(L12 pp.4, 15, 17)`.

### [HARD] A penetration tester reports three independent findings: (A) a service-account token with broad RBAC was found in a pod, (B) a container mounts the docker socket, (C) the registry pull-secret is write-capable. Using the lecture's qualitative prioritisation, order the fixes and justify the order.

**Answer:** The lecture gives **no DREAD-style numeric scoring** — prioritisation is qualitative, driven by attack-tree structure and the RBAC emphasis `(L12 pp.268, 330-style; 259-263 cookbook)`. Recommended order:

1. **Fix (A) the broad RBAC service-account token first.** The lecture flags that **"many attack vectors rely on mis-configuration of RBAC policies"** `(L12 p.9)`, and tokens like **[D13]/[D14]/[SC1]/[SC2]** are shared prerequisites across the scale-deployment, secret-exfiltration and API-access trees `(L12 pp.10, 14)`. Tightening RBAC to least privilege removes a prerequisite for *multiple* paths at once — maximum coverage per fix.
2. **Fix (C) the write-capable pull-secret next.** It is the single **AND** cut on the entire "poison image in registry" subtree `(L12 p.12)`; making it read-only collapses that whole branch cheaply.
3. **Fix (B) the mounted docker socket last of these three** — still important (it is a recurring host-escape leaf `(L12 pp.10, 12)`), but it primarily unlocks *one* class of host-process attacks, whereas (A) and (C) each defuse broader, multi-tree paths.

**Justification principle:** close the most-reused leaves and the pervasive-RBAC vector first, then the single-branch AND cut, then the localized host leaf `(L12 pp.9, 262-263)`. Mitigations for all three: least-privilege RBAC; read-only pull secret; Pod Security Policy + limit host mounts.

### [HARD] Compare how a defender should approach an OR-heavy attack tree versus an AND-chain attack tree, then apply this to the "DoS K8s Cluster" tree, which is described as mostly OR.

**Answer:** General principle `(L12 pp.10, 256-style)`:

1. **AND-chain:** the attacker must complete **every** step, so the defender wins by **breaking any one link** — find the cheapest single node to block. Low defender cost.
2. **OR-tree:** **any one** child suffices for the attacker, so the defender must **block every alternative** (or block a *shared* deeper prerequisite that all branches funnel through). High defender cost unless a common root exists.

**Applied to "DoS K8s Cluster → Perform DoS attack"** (mostly OR) `(L12 p.11)`: the attacker can independently DoS etcd (2379/2380), the API server (6443/8080), the scheduler (10251/10259), the controller-manager (10252/10257), the Kubelet (10250/10255/10248), kube-proxy (10249/10256), DNS (53), the CNI overlay, or block new-node joins. Because these are **OR** alternatives, blocking only one (say, the API server port) does **not** stop the others — the cluster can still be degraded via any remaining component.

**Defender strategy:** since there is no single AND link to cut, you must reduce reachability across *all* exposed ports — e.g. **Network Policies / firewalling so component ports are not exposed to untrusted networks**, rate-limiting, and resource quotas `(L12 pp.15, 16)`. The shared prerequisite to attack is *network reachability of each port*, so hardening network exposure is the closest thing to a single high-leverage control for an OR-heavy DoS tree.

### [HARD] An attack-tree leaf reads "[SC1] RBAC permissions open on service token" and feeds a branch ending in "remote code execution in container." Trace the path from leaf to impact and propose a layered mitigation using at least three distinct lecture controls.

**Answer:** Tracing the secret-exfiltration / datastore-attack subtree `(L12 p.14)`:

```
[SC1] RBAC permissions open on service token
   -> get service account / user token [SC2]
   -> have access to API server (kubectl or curl)
   -> exploit API service token / user token
   -> attach to running container / start pod with existing image
   -> remote code execution in container
   -> connect to internal datastore with stolen credentials
   -> unauthorized data access / cryptojacking / ransomware on datastore
```

So an over-permissioned RBAC token is the *root enabler*: it yields a valid token, which yields API access, which yields code execution and ultimately a datastore compromise `(L12 p.14)`.

**Layered mitigation (defence-in-depth, ≥3 distinct controls)** `(L12 pp.15, 16)`:

1. **Authorization — least-privilege RBAC:** scope the service account so the token cannot retrieve secrets or attach to pods (kills [SC1]/[SC2] at the source) `(L12 p.15)`.
2. **Kubernetes Secrets + don't store creds in ConfigMaps:** so even with API access the datastore credentials aren't trivially readable `(L12 p.15)`.
3. **Pod Security Policy + minimize privilege:** prevent "start pod with existing image / attach to running container" from yielding host-level RCE; limit host mounts `(L12 pp.15, 16)`.
4. **Audit Logging:** detect the anomalous token use / API calls for validation `(L12 p.15)`.

The key insight: fixing the **RBAC leaf** is the highest-leverage cut because every downstream node depends on it `(L12 pp.9, 14)`.

### [VERY HARD] Two engineers disagree. Engineer X says "we should compute a DREAD score for each attack-tree leaf and fix the highest-scoring ones." Engineer Y says "the slides don't give us a scoring method." Adjudicate using the lecture, and then give the actual prioritisation method the lecture supports.

**Answer:** **Engineer Y is correct on the facts.** The lecture explicitly does **not** present a formal quantitative risk-ranking scheme — there is no DREAD-style scoring or numeric likelihood×impact table in these slides; the content is **qualitative and attack-tree-based** `(L12 pp.268, 330)`. If an exam question asks for a *named* risk-ranking method, the honest answer is that this lecture provides none `(L12 p.268)`.

However, Engineer X's *instinct* (prioritise) is right — the lecture supports a **qualitative** prioritisation derived from tree structure and emphasis `(L12 pp.259-266 cookbook)`:

1. **Break AND-chains at their weakest single link first** — cheapest defeat of a whole path `(L12 pp.10, 261)`.
2. **Close the most-reused leaves next** — conditions appearing across many trees (container with host-FS access, mounted docker socket, HostPID/SYS_PTRACE) buy the most coverage per fix `(L12 pp.10, 12, 13, 262)`.
3. **Fix the pervasive vector the lecture names: RBAC mis-configuration** ("many attack vectors rely on" it) `(L12 pp.9, 263)`.
4. **Turn on the off-by-default controls** — add Network Policies and Pod Security Policies; move secrets out of ConfigMaps `(L12 pp.15, 264)`.
5. **Harden the surface, then automate validation** with kube-bench/Kubesec/Clair/Kubescape/Notary `(L12 pp.16, 17, 265-266)`.

**Adjudication:** don't fabricate DREAD numbers the slides never provided; use the structural/qualitative ordering above, which is defensible from the lecture's own emphasis.

### [VERY HARD] A single mis-configuration — a pod running privileged with the host filesystem mounted — appears as a leaf in the DoS tree, the malicious-code tree, the persistence tree, and the create-malicious-worker-node tree. Explain why this one leaf is so pervasive, trace its role in two of those trees, and argue what fixing it buys you.

**Answer:** **Why pervasive:** a privileged container with host-filesystem access is a *capability multiplier* — it lets the attacker read host certs/keys, write host files, drive the runtime, and reach master-node artifacts. The lecture repeatedly reuses "find Pod/Container with access to host filesystem" / "unrestricted access to host filesystem" as a leaf because it is a single mis-config that unlocks host-level attacks `(L12 pp.328, 10, 12, 13)`.

**Role in two trees:**

1. **etcd / DoS tree** `(L12 p.10)`: "write new workloads into etcd" needs the API client cert → "obtain certificate from master node" → **"find privileged workload with unrestricted access to host filesystem."** Host-FS access is the means of *exfiltrating the certificate* that unlocks etcd tampering.
2. **Create-malicious-worker-node tree** `(L12 p.14)`: to "create a valid kubelet client certificate" the attacker must "sign certificate offline → exfil K8s CA," which requires a **"container with unrestricted access to host filesystem"** on the master node. Same leaf, different goal — here it exfiltrates the **CA** to forge a node identity.

**What fixing it buys:** because the leaf is a **shared prerequisite** across the etcd-write, malicious-image, persistence-to-node-rebuild, and rogue-node paths, removing it (via **Pod Security Policy** denying privileged + host mounts, **limit host mounts**, **minimize privilege**, **don't run as root**) simultaneously severs *multiple* attack trees `(L12 pp.15, 16)`. This is the textbook "close the most-reused leaf" move — maximum coverage per single fix `(L12 p.262)`, far more efficient than patching each tree's downstream nodes individually.

### [VERY HARD] You inherit a cluster where: (i) etcd is unencrypted, (ii) the API server exposes the legacy insecure port 8080, (iii) audit logging is off, and (iv) images use the :latest tag. Map each issue to the attack vector / tree it enables, the 4Cs layer, and a mitigation, then state which single fix you'd do first and why.

**Answer:** Issue-by-issue mapping `(L12 pp.9-17)`:

| Issue | Enables (vector/tree) | 4C layer | Mitigation |
|---|---|---|---|
| (i) etcd unencrypted | "write/read workloads in etcd" tree — secrets readable without the encryption key; tampering with cluster state `(L12 pp.8, 10)` | **Cluster** | Encrypt etcd at rest; protect/rotate the etcd encryption key; restrict master-node access `(L12 pp.10, 16)` |
| (ii) API server port 8080 [D2] exposed | **DoS** vector (DoS API server [D2]) and unauthenticated API access → Service-Token/RBAC paths `(L12 p.11)` | **Cluster** | Disable the insecure port; require Authentication + RBAC; Network Policy/firewall the port `(L12 pp.11, 15)` |
| (iii) audit logging off | No detection/validation — every tree runs unobserved; breaks step-4 Validate `(L12 pp.4, 15)` | **Cluster** | Enable **Audit Logging**; periodically review logs `(L12 p.15)` |
| (iv) :latest images | Unknown running version → can't reason about vulns; aids poisoned/exploitable-image leaves `(L12 pp.12, 16)` | **Container** | Pin versions (no :latest); scan with Clair; sign with Notary `(L12 pp.16, 17)` |

**Do first: (ii) close the insecure API server port 8080.** Justification:

1. The **API Server is the central hub** — everything talks through it `(L12 p.7)` — so an unauthenticated insecure port is the broadest single exposure, enabling both a DoS target [D2] and an authentication-bypass that feeds the RBAC/service-token trees `(L12 pp.9, 11)`.
2. It is a one-config change with cluster-wide blast-radius reduction, and it gates many downstream leaves — consistent with "close the most-reused / most-pervasive exposure first" `(L12 pp.9, 262-263)`.

(ii) before (i) because etcd tampering paths still route through credentials normally obtained *via* the API server/master node, so shutting the open API door cuts the more immediate, broader access first; (iii) audit logging follows so you can *detect* attempts during remediation `(L12 pp.4, 15)`.

### [VERY HARD] A skeptic argues "STRIDE belongs to Threat Modeling I; this Kubernetes lecture is just attack trees, so STRIDE is irrelevant here." Refute this by showing concretely how STRIDE-per-element maps onto the K8s DFD, and explain how that mapping and the attack trees are two views of the same model.

**Answer:** The skeptic is **wrong**: the lecture explicitly bridges the two. Slide 8's DFD is described as the place where "you apply STRIDE per element" across each trust boundary `(L12 pp.8, 31, 79-style tie-backs)`. STRIDE (the Lecture-08 machinery) and attack trees are not competing — they are complementary views of one model.

**STRIDE-per-element on the K8s DFD** `(L12 pp.8, 79)`:

1. **Spoofing →** the **API Server** process and identity/token flows: a forged service-account token spoofs a legitimate client (counter: **Authentication**) `(L12 p.15)`.
2. **Tampering →** the **etcd data store** and any **data flow crossing a trust boundary** (e.g. writing workloads into etcd) (counter: etcd encryption, integrity controls) `(L12 pp.8, 10)`.
3. **Repudiation →** absence of **Audit Logging** lets actions be denied (counter: enable audit logs) `(L12 p.15)`.
4. **Information Disclosure →** secrets in etcd or in ConfigMaps, and boundary-crossing flows (counter: **K8s Secrets**, encrypt etcd) `(L12 pp.8, 15)`.
5. **Denial of Service →** every component process/port (the entire DoS attack tree) (counter: Network Policies, resource quotas) `(L12 pp.9, 11, 15)`.
6. **Elevation of Privilege →** the **API Server** and RBAC mis-configuration; privileged containers (counter: least-privilege **RBAC**, Pod Security Policies) `(L12 pp.9, 15)`.

**How the two views connect:** STRIDE tells you, *per DFD element*, **what category** of thing can go wrong (it is breadth-first over the diagram). An **attack tree** then takes one such concern (e.g. the **DoS** or **Elevation** finding on a given element) as its **root goal** and decomposes it depth-first into the concrete AND/OR leaf steps an attacker would actually perform `(L12 pp.9-14)`. So STRIDE-on-the-DFD *generates the roots*; the attack trees *expand the roots into mitigatable leaves*. They are the "Find Threats" step seen at two zoom levels of the same model `(L12 p.4)` — which is exactly why the lecture draws the DFD first (p.8), names the attack vectors next (p.9), and only then builds the trees (pp.10–14).

### [VERY HARD] Critique this candidate attack tree a student drew for "Exfiltrate secrets from a running container," then redraw a corrected version with proper AND/OR logic grounded in the lecture. Student's tree: root → "get token" → "use token" → "read secrets" (a single straight chain of ANDs, no alternatives).

**Answer:** **Critique:** the student's straight AND chain is structurally impoverished and does not match the lecture's secret-exfiltration subtree `(L12 p.14)`, which is **OR-rich** (multiple independent routes) and includes prerequisites the chain omits:

1. It ignores the **image-exfiltration** route entirely (push/pull poisoned image via the registry credential) `(L12 p.14)`.
2. It collapses "get token" into one node, hiding the real **OR** between obtaining a service-account/user token **[SC2]** and exploiting **open RBAC on the service token [SC1]** `(L12 p.14)`.
3. It omits the **RBAC-allow-secret-retrieval** prerequisite and the Kubelet "get all secrets for pods in namespace" path `(L12 p.14)`.
4. Treating everything as AND wrongly implies the attacker must do *all* of it; in reality any *one* route suffices (OR), which is the harder situation for a defender `(L12 p.10)`.

**Corrected tree** `(L12 p.14)`:

```
GOAL: Obtain/exfiltrate secrets from running container
  OR
  ├── Route A: Exfiltrate via image registry
  │     AND
  │     ├── Use image-registry credential
  │     │     OR
  │     │     ├── Pull-secret mis-configured to allow pull
  │     │     └── Exfiltrate image pull secret from K8s
  │     │           OR
  │     │           ├── Kubelet "get secrets"
  │     │           └── Kubelet "get all secrets for pods in namespace"
  │     │                 AND
  │     │                 └── RBAC allow secret retrieval
  │     └── Push poisoned / pull image from repository
  │
  └── Route B: Direct via API/runtime
        AND
        ├── Have access to API server (kubectl or curl)
        ├── Obtain credential
        │     OR
        │     ├── Get service-account / user token [SC2]
        │     └── RBAC permissions open on service token [SC1]
        └── Start pod with existing image / attach to running container
              -> remote code execution in container
```

**Key corrections:** the root is an **OR** (image route vs. API route), each route is an internal **AND** of prerequisites, and the credential acquisition is itself an **OR** — with **RBAC-allow-secret-retrieval** and **[SC1] open RBAC** as the recurring gating leaves a defender should cut first `(L12 pp.9, 14)`.
