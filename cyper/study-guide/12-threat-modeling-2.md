# 12. Threat Modeling II + Revision

> Source: `L12_Threat Modeling II.pdf` (27 slides, delivered 29 Apr 2026 by Sani Abdullahi, SDU Centre for Industrial Software). This is the final lecture of the course and combines (a) a second, applied pass at threat modeling using a real-world **Kubernetes** case study, (b) a whole-course **revision** pointer list, and (c) **mock-test and exam-prep** guidance.
>
> Note on sourcing: the lecture is slide-based and image-heavy. Several slides (the Kubernetes DFD and the attack trees) are diagrams with little extractable text; the descriptions below are read directly from those rendered diagrams and cited by slide. Where a slide only states a heading or a label, this guide says so rather than inventing detail. Citations use the form `(L12 p.N)` where N is the slide number.

---

## Overview — what this topic covers and why it matters

Threat Modeling I (Lecture 08) introduced the *process* of threat modeling — the four canonical steps of model the system, find threats, address threats, and validate `(L12 p.4)`. Threat Modeling II takes that process and **applies it end-to-end to a single, realistic, complex system: a Kubernetes (K8s) cluster** `(L12 p.5)`. The point of the lecture is to show what threat modeling looks like at scale on cloud-native infrastructure: how you draw the system as a data-flow diagram (DFD) with trust boundaries, how you enumerate attack vectors, and how you decompose each high-level attacker goal into a detailed **attack tree** of sub-goals and concrete leaf steps `(L12 pp.8–14)`. It then closes the loop by listing K8s **security features**, hardening **best practices**, and **open-source tooling** that mitigate the modeled threats `(L12 pp.15–17)`.

This matters for the exam for two reasons. First, threat modeling is examinable as a concept (the four steps, the key questions, DFD/trust-boundary notation, attack-tree AND/OR logic) and as an applied skill (reading or sketching a threat model for a given system) `(L12 pp.4, 8–14)`. Second, this lecture is also the **revision + exam-prep** session: it explicitly names the topics to revise, describes the mock test, and gives concrete exam logistics and a "what to study" list `(L12 pp.20–24)`. So the same document tells you both *a* topic that will be tested and *how* the whole exam is structured.

---

## Key Concepts

### Recall: the threat modeling process and its key questions

**What / why:** Threat modeling is a structured way of thinking about what can go wrong in a system *before* (and during) building it, so that defences are designed in rather than bolted on. The lecture re-states the definition implicitly by re-asking "What is threat modelling?" and "What are the key questions to ask when you perform threat modeling?" as a revision prompt `(L12 p.4)`.

**How — the four steps** `(L12 p.4)`:
1. **Model System** — create an application diagram (a DFD) to model the system.
2. **Find Threats** — identify the threats.
3. **Address Threats** — mitigate the threats.
4. **Validate** — validate the model to ensure threats are mitigated.

These four steps form a loop (Model → Find → Address → Validate → back to Model) `(L12 p.4)`. The "key questions" framing the slide alludes to are the standard four threat-modeling questions (What are we building? What can go wrong? What are we going to do about it? Did we do a good job?) — the slide poses the question rather than spelling out the four answers, so treat the four process steps above as the lecture's own concrete enumeration `(L12 p.4)`.

> Exam tie-back: this slide is the bridge from Threat Modeling I. STRIDE and DFDs are the Lecture-08 machinery; here you *use* a DFD (p.8) and attack trees (pp.10–14) to do steps 1–2 on Kubernetes.

### Use case: why Kubernetes for the worked example

**What / why:** Kubernetes is chosen as the worked example because it is a large, distributed, multi-component system with many trust boundaries — exactly the kind of system where a disciplined threat model pays off `(L12 p.5)`. The whole middle of the lecture (pp.5–17) is one extended applied threat model of a K8s cluster.

### The 4Cs of cloud-native security

**What / why:** Before modeling K8s threats, the lecture frames cloud-native security as nested layers — the **4Cs** — so that mitigations can be placed at the right layer `(L12 p.6)`. The layers are nested: an outer layer's weakness undermines everything inside it.

**The 4Cs** `(L12 p.6)`:
1. **Cloud** — security of the cloud infrastructure (the outermost layer).
2. **Cluster** — Kubernetes cluster-level security.
3. **Container** — security of the Dockerfile/Containerfile, the image, etc.
4. **Code** — security of the actual code implementation (the innermost layer).

**How to use it:** map each threat and mitigation to its C. E.g. "don't run as root" and "know your base image" are **Container**-layer controls; RBAC and network policies are **Cluster**-layer controls `(L12 pp.6, 15–16)`.

### Kubernetes architecture (what you are modeling)

**What / why:** You cannot model threats to a system you cannot draw. The lecture gives the cluster architecture so the DFD and attack trees make sense `(L12 p.7)`.

**Main components** `(L12 p.7)`:
- **Control plane (Master Node)** — contains:
  - **API Server** — the central hub; everything talks through it.
  - **etcd** — the cluster key-value store (holds cluster state and secrets).
  - **Scheduler** — decides which node a new pod runs on.
  - **Controller Manager** / **Cloud Controller Manager** — reconcile desired vs. actual state and integrate with the cloud provider.
- **Worker nodes** — each contains:
  - **Kubelet** — node agent that talks to the API server and runs pods.
  - **Container Runtime** (e.g. containerd) — actually runs containers.
  - **Kube-proxy** — handles networking / updates iptables.
  - **K8s Objects** (pods, etc.).
- **Developer** submits work to the API server; the **End User** consumes services via the worker nodes; a **Cloud Provider API** sits at the edge `(L12 p.7)`.

### The Kubernetes DFD and trust boundaries

**What / why:** Slide 8 is a full **data-flow diagram (DFD)** of the cluster, drawn in the CNCF Financial User Group style. This is step 1 (Model System) made concrete `(L12 p.8)`.

**DFD notation (the slide's own key)** `(L12 p.8)`:
- **Solid arrow** = Data Flow.
- **Dashed red line** = **Trust Boundary**.
- **Solid (machine) boundary** = Machine Segregation.
- **Circle** = Process or Component.
- **Shaded rectangle** = Data Store.

**What the DFD shows** `(L12 p.8)`: the **API Server** (process) sits at the centre and reads/writes **etcd** (data store). The **Controller** polls for current/desired state and manages replicas, service accounts and endpoints; the **Scheduler** schedules pods / polls for new pods. A **User** applies a deployment through the API Server. On the worker side, the **Kubelet** gets images, the **ContainerD** runtime pulls images (image manifest + blobs) from the **Image Repository** (with its **Image Repository Data Store**), uses **RunC** to run containers, and checks an **Image Cache** ("available image?" → yes/no). **Kube-proxy** updates **IP Tables**. **Pods** contain **Containers**. Dashed red trust boundaries separate the control plane, the worker components, the image repository, and the pod from one another — these boundaries are where threats concentrate.

> Exam tie-back to STRIDE/DFD: a trust boundary on a DFD is exactly where you apply STRIDE per element. Data flows crossing a boundary are candidates for Tampering and Information Disclosure; the API Server process is a candidate for Spoofing/Elevation of Privilege; etcd (data store) is a candidate for Tampering and Information Disclosure.

### Security boundaries and main attack vectors

**What / why:** Having drawn the DFD, the lecture names the **main attack vectors** — the high-level ways an attacker crosses the cluster's security boundaries `(L12 p.9)`. These become the *roots* of the attack trees that follow.

**Main attack vectors** `(L12 p.9)`:
- **Denial of Service (DoS)** — prevent the system from functioning by **exhausting resources within the cluster**.
- **Compromised Container** — provides a **remote execution point** for an attacker.
- **Service Token Compromise** — allows **unauthorized access to the cluster API**.
- **Network Endpoints** — access to endpoints **if the pod's network policy permits** it.
- **RBAC Issues** — many attack vectors rely on **mis-configuration of RBAC policies**.

### Attack trees (the core technique of this lecture)

**What / why:** An **attack tree** decomposes a single attacker goal (the root) into the sub-goals and concrete steps needed to achieve it. It is the technique used throughout pp.10–14 to turn each attack vector into a detailed, analysable plan. Attack trees make it explicit *which combinations* of steps an attacker must complete `(L12 pp.10–14)`.

**How to read one — the slide's own key** `(L12 p.10)`:
- **AND node** — all child sub-goals must be achieved for the parent to succeed.
- **OR node** — any one child sub-goal is sufficient for the parent.
- **NODE** — an intermediate goal.
- **Label / notes** — annotations (e.g. "May need etcd encryption key (accessible on master node)") `(L12 p.10)`.
- **Subtree** — a goal expanded elsewhere / reused.
- **GOAL** (leaf) — a concrete, actionable step, often referencing a specific finding (e.g. **[D13] Service account has sufficient privilege**, **[D14] Find valid service account token**) `(L12 p.10)`.

The trees are read **top-down from the root goal to the leaves**; the leaves are the concrete things an attacker (or a defender deciding what to block) cares about.

#### Attack tree 1 — DoS, left branch `(L12 p.10)`
Root family: **exhaust compute resources**. Branches include: *add a process to a running pod*; *use a privileged container to start/modify a process on the host (root)* — via importing malicious code, exploiting existing tooling in the container, modifying files on the host filesystem, or starting a process using Docker / in the host PID namespace (leaves like "find Pod/Container with access to host filesystem", "with mounted docker socket", "with HostPID", "with SYS_PTRACE capability enabled"); *write new workloads into the etcd data store* (note: **may need the etcd encryption key, accessible on the master node**; use the **K8s API client cert to authenticate to etcd** → obtain the client certificate from the master node → find privileged workload scheduled on the master node / with unrestricted access to host filesystem); *create a scale deployment using the API server* (via a service-account credential → **[D13]** service account has sufficient privilege, **[D14]** find valid service-account token); and *create an autoscaling event within an existing deployment* (→ find deployment exposed to network). A leaf goal is **Gain access to Container** `(L12 p.10)`.

#### Attack tree 2 — DoS, right branch `(L12 p.11)`
Root: **DoS K8s Cluster** → **Perform DoS attack**. Sub-goals (mostly **OR**) and the *specific ports* they target `(L12 p.11)`:
- **Exhaust compute resources** → reduce worker node pool → bring Kubelet down / render Kubelet healthcheck unresponsive → **DoS Kubelet port 10255 [D10], 10250 [D11], 10248 [D12]**.
- **Disrupt rate/restart scheduling of workloads** → **loss of etcd quorum** / prevent etcd internal consistency / prevent changes to desired cluster state.
- **DoS etcd peer port 2380 [D5]**, **DoS etcd client port 2379 [D5]**.
- **DoS API server port 6443 [D1] / 8080 [D2]**.
- **Bring scheduler down (prevent rescheduling)** → **DoS scheduler port 10251 [D4] / 10259 [D3]**.
- **Bring controller-manager down (lose control loop)** → **DoS controller-manager port 10252 [D6] / 10257 [D7]**.
- **Disrupt networking** → **DoS kube-proxy** (bring kube-proxy down → host) **port 10249 [D8] / 10256 [D9]**; **DoS DNS** (bring K8s DNS down → DNS service down, DNS queries fail) **port 53**; **degrade CNI overlay network** → **DoS exposed CNI ports (TBD/CNI-specific)**; saturate CNI network.
- **Prevent new worker nodes joining the cluster** → DoS the network boot service (e.g. PXE server).

> Exam note: the **[D#] labels and named ports** (2379/2380, 6443/8080, 10250/10251/10252/10255/10256/10257/10259/10248/10249, 53) are the kind of detail that *could* appear in a multiple-choice question. The big idea — *each control-plane and node component listens on a port, and each port is a DoS target* — is the takeaway; memorise the port→component mapping only if you want MCQ insurance.

#### Attack tree 3 — Malicious code execution / pull secret `(L12 p.12)`
Root: **malicious code in workload** → **deploy poisoned container image** → *image deployed as part of normal release* OR *poison image in container registry*. To poison the registry you must **obtain the image pull secret**, which requires **pull-secret has write/overwrite privileges** and one of: *make a K8s API request*, *use the running container with host filesystem access*, or *read the K8s secret from the Kubelet* `(L12 p.12)`.

#### Attack tree 3b — Malicious: gain access to container `(L12 p.12)`
Root: **malicious code in workload** → *execute in running container* OR *use privileged container to start/modify a process on host [M5]*. Leaves: **[M6] import malicious code** (find workload with tools for downloading/executing malicious code); **[M7] modify file on host filesystem** (find Pod/Container with access to host filesystem); **[M8] start process using container runtime** (find Pod/Container with mounted docker socket); **[M9] start child process in host PID namespace** (find Pod/Container with HostPID / with SYS_PTRACE capability enabled). Leaf goal: **Gain access to container** `(L12 p.12)`.

#### Attack tree 4 — Establish persistence / container compromise `(L12 p.13)`
Root: **Establish Foothold & Persistence** `(L12 p.13)`. Major branches:
- **Foothold with no resilience** (start process in running container → exploit existing tooling / import malicious code).
- **Foothold with resilience to container restart** (mis-configure container for app access via NGINX config; write/set config file on volume).
- **Foothold with resilience to pod deletion/creation** (mis-configure container to gain app access via NGINX config; write config file to volume that persists).
- **Foothold with resilience to node restart** (create a restarting container on host using Docker restart-always; create init for init system on join; use running container with mounted docker socket).
- **Foothold with resilience to node rebuild / app deletion** (modify K8s resources via API server; compromise PKI; modify K8s objects stored within etcd → use K8s API client cert to authenticate to etcd → obtain certificates from master node → find privileged workload with unrestricted access to host filesystem; workload on master nodes).

#### Attack tree 5 — Scenarios: compromised container `(L12 p.14)`
Two scenario sub-trees `(L12 p.14)`:
- **Create malicious worker node** → add host to cluster → *manually add worker* (launch kubelet on a new host with autoregistration flag / register-node; **create valid kubelet client certificate** → sign certificate using K8s API / sign certificate offline → sign certificate remotely / exfil K8s CA → container on master node / container has unrestricted access to host filesystem) OR *kubeadm join* (use bootstrap token → create token in K8s secrets / obtain existing token from K8s secrets; launch compute; API server configured to permit bootstrap token auth).
- **Steal / exfiltrate secrets** (highlighted **ATTACK TREE** node, "obtain secrets from RUNNING container"): push poisoned image to / exfiltrate image from image repository (→ use image-registry credential → pull-secret mis-configured to allow pull / exfiltrate image pull secret from K8s → Kubelet get secrets / get all secrets for pods in namespace → **RBAC allow secret retrieval**); unauthorized access / exfiltration of data / perform cryptojacking / ransomware attack on datastore (→ connect to internal datastore with stolen credentials → obtain secrets from running container → start pod with existing image / attach to running container → exploit API service token / user token → have access to API server (kubectl or curl) / get service account or user token **[SC2]** / RBAC permissions open on service token **[SC1]** → remote code execution in container).

> Read these as worked examples of how a single root goal explodes into dozens of concrete, mitigatable leaf conditions. For the exam you need to (a) read AND/OR logic, (b) trace root→leaf, and (c) name a mitigation for a leaf — not memorise every node `(L12 pp.10–14)`.

### Linking attack trees back to mitigations: K8s security features

**What / why:** After enumerating threats, you address them (step 3). The lecture lists the built-in K8s **security features** that mitigate the modeled attack vectors `(L12 p.15)`:
- **Authentication** — many mechanisms: client certs, OpenID, static token file, etc.
- **Authorization** — **RBAC, ABAC, Node, and Webhook** modes (directly counters the "RBAC issues" attack vector).
- **Audit Logging** — periodically watch audit logs (detection / validation).
- **Network Policies** — *all pods can talk to each other by default*; you must **add a network policy** (counters the "network endpoints" vector).
- **Pod Security Policies** — add pod security policies.
- **Kubernetes Secrets** — use K8s Secrets instead of ConfigMaps to store sensitive data.

### Best practices: reduce the attack surface

**What / why:** Defence-in-depth hardening across the **host, container images, and cluster** layers — i.e. shrink what an attacker can reach `(L12 p.16)`:
- **Minimize privilege** to applications running on the host.
- **Know your base image** when building containers.
- **The smaller the image, the better.**
- **Don't rely on the `:latest` tag** (pin versions).
- **Check for vulnerabilities periodically.**
- **Don't run as root.**
- **Limit host mounts.**
- **Ensure TLS checklist for the cluster.**

### Open-source K8s security tooling

**What / why:** Tools automate the validation and vulnerability-finding steps `(L12 p.17)`. The exact tool→purpose mapping from the slide:
- **kube-bench (Aqua)** — checks whether Kubernetes is **securely deployed** (CIS-benchmark conformance).
- **Kubesec** — **security risk analysis** for Kubernetes resources.
- **Clair** — **static analysis of vulnerabilities in containers** (image scanning).
- **Kubescape** — security platform that **scans clusters, Kubernetes manifest files, code repos, container registries and images**.
- **Notary (Notary Project)** — CLI tool to **sign and verify artifacts**; a solution to **secure updates and distribution**; **used in Docker Trusted Registry**.

The lecture also points to the **CNCF Security Landscape** (`https://landscape.cncf.io/`) to keep up with the tooling ecosystem `(L12 p.18)`.

### Revision: the topics the course will test

**What / why:** Slide 20 is the revision menu — the topics the lecturer invites questions on, i.e. the examinable syllabus `(L12 p.20)`:
- Introduction
- Vulnerability Assessment
- Penetration Testing
- Social Engineering, Phishing
- Threat Modeling I
- Threat Modeling II
- IDS, Malware, DoS, Crypto, MPC

(That list mirrors the course plan on slide 2: L01 Intro & Lab Set-up, L02 Vulnerability Assessment, L03 Penetration Testing, L04 Firewalls and IDS, L05 Malware & SQL, L06 Denial of Service, L07 Social Engineering/Phishing, L08 Threat Modelling I, L09 Cryptography, L10 Multi-party Computation, L11 Privacy/Data Protection/GDPR, L12 Threat Modelling II/Revision) `(L12 pp.2, 20)`.

### Mock test and exam logistics

**What / why:** The lecture doubles as exam prep and states the rules `(L12 pp.21–24)`. See **Revision Notes** below for the full list — these are the highest-value facts on the slides.

---

## Glossary

- **Threat modeling** — a structured process of modeling a system, finding threats, addressing them, and validating that they are mitigated `(L12 p.4)`.
- **DFD (Data-Flow Diagram)** — the "model the system" artifact; shows processes, data stores, data flows and trust boundaries `(L12 p.8)`.
- **Trust boundary** — a line (dashed red on the slide's DFD) where the level of trust changes and where threats concentrate `(L12 p.8)`.
- **Data store** — a place data is held at rest (shaded rectangle on the DFD), e.g. etcd, image repository data store `(L12 p.8)`.
- **Process / Component** — an active element on the DFD (circle), e.g. API Server, Kubelet `(L12 p.8)`.
- **Machine segregation** — a boundary (solid line) indicating a separate machine in the DFD `(L12 p.8)`.
- **Attack tree** — a tree decomposing an attacker goal (root) into sub-goals and concrete leaf steps, combined with AND/OR logic `(L12 pp.10–14)`.
- **AND node** — parent goal achieved only if **all** children are achieved `(L12 p.10)`.
- **OR node** — parent goal achieved if **any one** child is achieved `(L12 p.10)`.
- **Leaf / GOAL** — a concrete, actionable attacker step at the bottom of an attack tree `(L12 p.10)`.
- **Subtree** — an attack-tree goal expanded (or reused) elsewhere `(L12 p.10)`.
- **4Cs** — the nested layers of cloud-native security: Cloud, Cluster, Container, Code `(L12 p.6)`.
- **Control plane (Master Node)** — the K8s management layer: API Server, etcd, Scheduler, Controller Manager `(L12 p.7)`.
- **Worker node** — runs the workloads: Kubelet, Container Runtime, Kube-proxy, K8s Objects `(L12 p.7)`.
- **API Server** — central K8s component that all requests pass through; reads/writes etcd `(L12 pp.7–8)`.
- **etcd** — K8s key-value store holding cluster state and secrets `(L12 pp.7–8)`.
- **Kubelet** — node agent that runs pods and pulls images; talks to the API server `(L12 pp.7–8)`.
- **Kube-proxy** — handles node networking; updates iptables `(L12 pp.7–8)`.
- **RBAC (Role-Based Access Control)** — an authorization mode; its **mis-configuration underlies many attack vectors** `(L12 pp.9, 15)`.
- **ABAC / Node / Webhook** — other K8s authorization modes `(L12 p.15)`.
- **Network Policy** — must be added explicitly because **all pods can talk to each other by default** `(L12 p.15)`.
- **Pod Security Policy** — a control restricting what pods may do `(L12 p.15)`.
- **K8s Secret** — the recommended store for sensitive data (use instead of ConfigMaps) `(L12 p.15)`.
- **Service token / service-account token** — credential that, if compromised, allows unauthorized access to the cluster API `(L12 p.9)`.
- **Pull secret** — credential to pull images from a registry; if write/overwrite-capable it lets an attacker poison the registry `(L12 p.12)`.
- **Compromised container** — a container that gives the attacker a remote execution point `(L12 p.9)`.
- **HostPID** — pod setting that puts a container in the host's PID namespace; a leaf condition enabling host-process attacks `(L12 pp.10, 12)`.
- **SYS_PTRACE capability** — a container capability that enables tracing/manipulating other processes; an attack-tree leaf condition `(L12 pp.10, 12)`.
- **Docker socket (mounted)** — exposing the host's Docker socket into a container; a leaf condition enabling runtime abuse `(L12 pp.10, 12)`.
- **etcd encryption key** — key (accessible on the master node) needed to read/write secrets in etcd in some attack paths `(L12 p.10)`.
- **kube-bench** — tool that checks whether K8s is securely deployed (CIS benchmark) `(L12 p.17)`.
- **Kubesec** — security risk analysis for K8s resources `(L12 p.17)`.
- **Clair** — static analysis of vulnerabilities in containers (image scanner) `(L12 p.17)`.
- **Kubescape** — scans clusters, manifests, code repos, registries and images `(L12 p.17)`.
- **Notary** — signs/verifies artifacts; secures update distribution; used in Docker Trusted Registry `(L12 p.17)`.
- **CNCF (Cloud Native Computing Foundation)** — body whose Financial User Group produced the K8s threat model used here; also hosts the security landscape `(L12 pp.8, 18)`.
- **MCQ / MAQ** — Multiple-Choice / Multiple-Answer Questions (some questions have more than one correct option) `(L12 pp.22–23)`.

---

## How-To Cookbook

### Cookbook A — Threat-model a system end to end (the lecture's workflow, applied)

1. **Model the system (DFD).** Draw the system as a data-flow diagram: mark every **process/component** (circle), **data store** (shaded box), **data flow** (arrow), and **trust boundary** (dashed line). For K8s this is the control plane (API Server, etcd, Scheduler, Controller) and worker nodes (Kubelet, ContainerD/RunC, Kube-proxy, Pods) with the Image Repository `(L12 pp.4, 8)`.
2. **Identify trust boundaries.** Anywhere trust changes — between control plane and workers, between the cluster and the image registry, around the pod — draw a boundary. Boundaries are where you concentrate analysis `(L12 p.8)`.
3. **Enumerate the main attack vectors** crossing those boundaries: DoS (resource exhaustion), compromised container (remote execution), service-token compromise (API access), network endpoints (if policy permits), RBAC mis-configuration `(L12 p.9)`.
4. **Build an attack tree per vector.** Put the vector as the **root goal**. Decompose into sub-goals; mark each junction **AND** (all children needed) or **OR** (any child suffices). Continue until each branch ends in a **concrete leaf** — an actionable condition like "find Pod/Container with mounted docker socket" or "find valid service-account token [D14]" `(L12 pp.10–14)`.
5. **Annotate leaves with prerequisites.** Use label/notes nodes for conditions an attacker must meet (e.g. "may need etcd encryption key, accessible on master node") `(L12 p.10)`.
6. **Address the threats (map mitigations to leaves).** For each leaf, name a K8s control that blocks it: RBAC/Authentication for token leaves, Network Policies for network-endpoint leaves, Pod Security Policies for HostPID/privileged-container leaves, K8s Secrets for secret-storage leaves, audit logging for detection `(L12 p.15)`.
7. **Harden to shrink the attack surface.** Apply best practices: least privilege on the host, known/small base images, no `:latest`, periodic vuln scans, don't run as root, limit host mounts, TLS checklist `(L12 p.16)`.
8. **Validate with tooling.** Run kube-bench (secure deployment), Kubesec (resource risk), Clair (image vulns), Kubescape (broad scan), Notary (artifact signing) and review audit logs to confirm the threats are actually mitigated `(L12 pp.15, 17)`.
9. **Iterate.** Re-run the loop (Model → Find → Address → Validate) whenever the system changes `(L12 p.4)`.

### Cookbook B — Read an attack tree under exam conditions

1. **Find the root** (top node) — the attacker's overall goal `(L12 pp.10–14)`.
2. **Classify each junction** using the key: triangle/marker for **AND** (all children) vs **OR** (any child) `(L12 p.10)`.
3. **Trace one path root→leaf.** Read the chain of sub-goals down to a concrete leaf.
4. **Read AND vs OR for difficulty.** An OR-heavy tree means many independent ways in (block them all); an AND chain means the attacker must complete every step (block any one step to break the chain) `(L12 p.10)`.
5. **Map a leaf to a mitigation** (see Cookbook A step 6) — this is the most likely short-answer task.

### Cookbook C — Prioritise mitigations (defender's order of work)

1. **Block AND-chains at their weakest single link first** — breaking one node of an AND chain defeats the whole path cheaply `(L12 p.10)`.
2. **Close the most-reused leaves next** — conditions appearing across many trees (e.g. "container with host filesystem access", "mounted docker socket", "HostPID/SYS_PTRACE") buy the most coverage per fix `(L12 pp.10, 12, 13)`.
3. **Fix the attack vector the lecture flags as pervasive: RBAC mis-configuration** — "many attack vectors rely on mis-configuration of RBAC policies" `(L12 p.9)`.
4. **Add the defaults that are off by default** — add Network Policies (pods talk freely by default) and Pod Security Policies; move secrets out of ConfigMaps into K8s Secrets `(L12 p.15)`.
5. **Harden the surface** per the best-practices checklist `(L12 p.16)`.
6. **Automate validation** with the tooling so regressions are caught `(L12 p.17)`.

> Caveat: the lecture does **not** present a formal quantitative risk-ranking scheme (no DREAD-style scoring or numeric likelihood×impact table is shown on these slides). The prioritisation above is derived from the lecture's own emphasis (AND/OR structure, RBAC being pervasive, off-by-default controls), not from a scoring formula the slides provide. If an exam question asks for a *named* risk-ranking method, note that this lecture's content is qualitative/attack-tree-based.

---

## Exam-Style Q&A

**Q1. List the four steps of the threat modeling process.**
A. (1) **Model the system** — create an application/data-flow diagram; (2) **Find/identify the threats**; (3) **Address/mitigate the threats**; (4) **Validate** the model to ensure threats are mitigated. They form a continuous loop `(L12 p.4)`.

**Q2. What are the 4Cs of cloud-native security, and which layer does "don't run as root" belong to?**
A. **Cloud** (cloud infrastructure security), **Cluster** (K8s cluster-level security), **Container** (Dockerfile/image security), **Code** (application code security) — nested outer-to-inner. "Don't run as root" is a **Container**-layer control `(L12 pp.6, 16)`.

**Q3. In the Kubernetes DFD, what does a dashed red line represent, and why does it matter for threat modeling?**
A. A dashed red line is a **trust boundary**. It matters because threats concentrate where trust changes — data flows crossing a boundary are candidates for tampering/disclosure and components on the boundary for spoofing/elevation — so you apply STRIDE per element across each boundary `(L12 p.8)`.

**Q4. Name the five main attack vectors against a Kubernetes cluster identified in the lecture.**
A. (1) **Denial of Service** — exhaust cluster resources; (2) **Compromised Container** — remote execution point; (3) **Service Token Compromise** — unauthorized cluster-API access; (4) **Network Endpoints** — reachable if the pod's network policy permits; (5) **RBAC Issues** — many vectors rely on RBAC mis-configuration `(L12 p.9)`.

**Q5. Explain the difference between an AND node and an OR node in an attack tree, and what each implies for a defender.**
A. An **AND node** means the parent goal succeeds only if **all** child sub-goals are achieved; an **OR node** means **any one** child suffices. For a defender: to break an **AND** chain you only need to block **one** of its steps (cheap); to defeat an **OR** node you must block **every** alternative `(L12 p.10)`.

**Q6. The DoS attack tree targets specific ports. Why is "each component listens on a port" a threat-modeling insight, and give two example component-port pairs from the lecture.**
A. Each control-plane and node component exposes a network service on a port, so **each port is an independent DoS target** — flooding any one can degrade that component and ripple through the cluster (e.g. killing the scheduler stops rescheduling; killing etcd loses quorum). Examples from the lecture: **etcd client port 2379 / peer port 2380 [D5]**, **API server port 6443 [D1] / 8080 [D2]**, **Kubelet ports 10250/10255/10248 [D11/D10/D12]**, **DNS port 53** `(L12 p.11)`.

**Q7. An attack-tree leaf reads "Find Pod/Container with mounted docker socket." What is the threat, and which K8s control mitigates it?**
A. A mounted Docker socket lets a compromised container drive the host's container runtime — effectively host-level code execution and container escape, used to start arbitrary processes `(L12 pp.10, 12)`. Mitigations from the lecture: **Pod Security Policies** to forbid such mounts, **limit host mounts** and **minimize privilege** (best practices), and don't run privileged/root containers `(L12 pp.15, 16)`.

**Q8. Why does "RBAC issues" deserve special attention when mitigating K8s threats?**
A. Because the lecture states that **many attack vectors rely on mis-configuration of RBAC policies** `(L12 p.9)` — service-token and secret-retrieval paths in the attack trees depend on RBAC permissions (e.g. "RBAC allow secret retrieval", "[SC1] RBAC permissions open on service token") `(L12 p.14)`. Fixing RBAC therefore removes a prerequisite for multiple attack paths at once. The corresponding control is **Authorization (RBAC)** with least-privilege roles `(L12 p.15)`.

**Q9. List the K8s built-in security features named in the lecture and pair each with an attack vector it counters.**
A. **Authentication** (counters service-token/spoofing access), **Authorization: RBAC/ABAC/Node/Webhook** (counters RBAC mis-config), **Audit Logging** (detection/validation), **Network Policies** — needed because pods talk freely by default (counters network-endpoint reachability), **Pod Security Policies** (counters privileged-container/host attacks), **Kubernetes Secrets** instead of ConfigMaps (counters secret disclosure) `(L12 p.15)`.

**Q10. Match each tool to its purpose: kube-bench, Kubesec, Clair, Kubescape, Notary.**
A. **kube-bench** — checks whether K8s is securely deployed (CIS benchmark); **Kubesec** — security risk analysis for K8s resources; **Clair** — static analysis of vulnerabilities in containers (image scanning); **Kubescape** — scans clusters, manifests, code repos, registries and images; **Notary** — signs/verifies artifacts, secures update distribution, used in Docker Trusted Registry `(L12 p.17)`.

**Q11. Give four best practices for reducing the Kubernetes attack surface.**
A. Any four of: minimize privilege to host apps; know your base image; keep images small; don't rely on the `:latest` tag; check for vulnerabilities periodically; don't run as root; limit host mounts; ensure a TLS checklist for the cluster `(L12 p.16)`.

**Q12. Why is etcd a high-value target in the K8s threat model, and what does an attacker need to write to it directly?**
A. **etcd** is the cluster's key-value store holding cluster state and secrets, and the API Server reads/writes it `(L12 p.8)`. To write new workloads directly into etcd, an attacker may need the **etcd encryption key (accessible on the master node)** and/or must **use the K8s API client certificate (obtained from the master node) to authenticate to etcd** `(L12 p.10)`. So compromising the master node / its certificates unlocks etcd tampering.

**Q13. Walk through one root-to-leaf path in the "malicious code execution – pull secret" tree and name a mitigation.**
A. Root **malicious code in workload** → **deploy poisoned container image** → **poison image in container registry** → **obtain image pull secret** (requires pull-secret with **write/overwrite** privilege) → e.g. **use the running container with host filesystem access** to read it `(L12 p.12)`. Mitigations: least-privilege pull secrets (read-only), don't grant containers host filesystem access (limit host mounts, Pod Security Policies), and sign/verify images with **Notary** so a poisoned image is rejected `(L12 pp.15–17)`.

**Q14. What does "Establish Persistence" add over simply "gaining access," and name the persistence levels in the tree.**
A. Persistence is about surviving normal lifecycle events so the foothold isn't lost. The tree layers it by resilience: **no resilience**, **resilient to container restart**, **resilient to pod deletion/creation**, **resilient to node restart**, and **resilient to node rebuild / app deletion** (the deepest, using docker-socket restart-always containers, init-system hooks, or modifying K8s objects in etcd via the API client cert) `(L12 p.13)`.

**Q15. (Exam logistics) How many questions are on the real exam, of what types, and how long is it?**
A. **50 questions total: 35 MCQ/MAQ and 15 short-answer**, in **2.5 hours (3 hours with extra time)** `(L12 p.23)`. Some questions have more than one correct option (MAQ), and you can freely navigate between questions `(L12 p.22)`.

---

## Gotchas

- **"Validate" is not optional and not a one-off.** Step 4 closes the loop back to step 1; the process is iterative, not linear `(L12 p.4)`. A common mistake is treating threat modeling as a one-time document.
- **OR vs AND is the most error-prone reading.** An **OR** node means *any single* child is enough — don't assume the attacker must do all of them. An **AND** node means *all* are required — and for the defender, blocking just one breaks the chain `(L12 p.10)`.
- **Pods are open by default.** "All pods can talk to others by default" — if you forget to add a **Network Policy**, the "network endpoints" attack vector is wide open `(L12 pp.9, 15)`.
- **Use K8s Secrets, not ConfigMaps, for sensitive data.** Storing secrets in ConfigMaps is the mistake the slide explicitly warns against `(L12 p.15)`.
- **`:latest` is a trap.** Relying on the `:latest` tag means you don't know what's actually running and can't reason about vulnerabilities — pin versions `(L12 p.16)`.
- **Running as root / privileged containers / mounted docker socket / HostPID / SYS_PTRACE** are recurring leaf conditions across multiple trees — each is a single mis-config that unlocks host-level attacks. Don't treat them as edge cases `(L12 pp.10, 12, 13)`.
- **etcd compromise often routes through the master node.** Many "write to etcd" / "modify K8s objects in etcd" paths need certificates or the encryption key from the **master node**, so master-node compromise is catastrophic `(L12 pp.10, 13)`.
- **This lecture's risk ranking is qualitative.** Don't expect a DREAD-style numeric formula on these slides; prioritisation here comes from attack-tree structure and the RBAC emphasis, not a scoring table `(L12 pp.9–14)`.
- **Don't conflate the mock test with the real exam.** They have different sizes and durations (see Revision Notes) `(L12 pp.21, 23)`.
- **The threat model shown is the CNCF Financial User Group model**, not a generic one — cite it as such if asked for the source `(L12 p.8)`.

---

## Revision Notes (what the lecture explicitly flags for the exam)

**Topics to revise (slide 20)** `(L12 p.20)` — the lecturer's own revision menu: Introduction; Vulnerability Assessment; Penetration Testing; Social Engineering & Phishing; Threat Modeling I; Threat Modeling II; and IDS, Malware, DoS, Crypto, MPC. (Full course map: L01–L12 on slide 2 `(L12 p.2)`.)

**Mock test (slide 21)** `(L12 p.21)`:
- Password for the mock test: **CSF26MOCKTEST**.
- Duration: **45 minutes**.
- **15 questions total: 10 multiple-choice + 5 short essay.**

**Exam guidelines (slide 22)** `(L12 p.22)`:
- The exam is **on campus** — check your allocated room on the list at "DE" **the day before** the exam.
- Contains **MCQ/MAQ and short-answer** questions.
- You can **freely navigate between questions**.
- You **can select multiple options** — some questions have more than one correct answer (MAQ).

**Exam question paper (slide 23)** `(L12 p.23)`:
- **Total: 50 questions.**
- **35 MCQ/MAQ + 15 short-answer.**
- **Duration: 2.5 hours (3 hours with extra time).**

**Exam preparation guidance (slide 24)** `(L12 p.24)` — the highest-value "what to study" slide:
- **Learn and understand the concepts in the slides and exercises.**
- **Focus on the lecture slides and exercises.**
- **Practice the exercises for Labs 2, 3, 5, 6, 8, and 9.** (i.e. Vulnerability Assessment, Penetration Testing, Malware & SQL, Denial of Service, Threat Modelling I, and Cryptography — based on the L01–L12 mapping `(L12 p.2)`.)

**References for deeper reading on the K8s model (slide 19)** `(L12 p.19)`: Kubernetes Security Cheat Sheet; Kubernetes Threat Model – CNCF Financial User Group; Kubernetes Threat Model – CloudSecDocs; A Deep Dive into Kubernetes Threat Modeling – Trend Micro; Kubernetes Hardening Guidance (DoD). Also the CNCF Security Landscape: `https://landscape.cncf.io/` `(L12 pp.18–19)`.

**Bottom-line exam strategy from this lecture:** master the four-step process and AND/OR attack-tree reading (Threat Modeling is examinable both conceptually and applied); for the Kubernetes case, be able to name the 4Cs, the five attack vectors, the K8s security features, and the tool→purpose mapping; and **drill the labs the lecturer named (2, 3, 5, 6, 8, 9)** since those are explicitly flagged for practice `(L12 pp.4, 6, 9, 10, 15, 17, 24)`.
