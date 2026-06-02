# Lecture 9: Cyber Security Engineering (Architecture-Level)

> **Source:** lecture_9.pdf (70 pages)
> **Lecturer:** Jukka Ruohonen
> **Date (stated):** April 21, 2026
> **Position in course:** Second security lecture — L8 covered the agentic / safety-and-security framing (CIA, SIEM, LLM/agentic threats, privilege drop). L9 drops the agentic context and goes deep on classical security engineering: trade-offs, the Microsoft Security Development Lifecycle (SDL), threat modeling, trust boundaries, the kill chain, zero-trust + sidecars, MitM, and cryptography.

## Themes covered

1. **Security trade-offs** — security vs. risk/cost/usability/performance/privacy/reliability (fail-safe vs. fail-secure).
2. **Security as a constraint** across design, architecture and implementation — not just a quality attribute.
3. **Microsoft's Security Development Lifecycle (SDL)** — Design → Implementation → Build → Deploy → Run, with three gates and zero-trust baseline.
4. **Threat modeling as a design activity** — Microsoft's four-step loop and RFC 3552 references.
5. **Trust boundaries revisited** — protection rings, machine/component-level, deployment-level.
6. **The cyber kill chain** — initial exploit → privilege escalation → container escape → reconnaissance → lateral movement → data exfiltration → cleanup + RAT.
7. **Zero-trust architecture and the sidecar pattern** — mTLS everywhere, ingress/egress gateways, honeypots, isolation during incidents.
8. **Data classification, side-channels, confused-deputy** — supplementary security idioms.
9. **Connectors / networking security** — MitM taxonomy, MitM countermeasures, TLS vs. SSH, HTTPS in CI/CD.
10. **Cryptography in design** — minimizing the window during which data is unencrypted in processing.

## Concepts

### Fail-safe vs. fail-secure (security ↔ reliability trade-off)
**Definition:** When a component fails, "fail-safe" (a.k.a. fail-open) keeps the service available — defaulting to "allow"; "fail-secure" (fail-closed) shuts down — defaulting to "deny."
**Why it matters:** Reliability engineering and security engineering pull in opposite directions on the same failure event. You can't pick "both" by default — your organization must decide a non-negotiable posture per asset class.
**Detailed explanation:** Adkins et al. (2020): "to maximize reliability, a system should resist failures and serve as much as possible"; "to maximize security, a system should lock down fully in the face of uncertainty." Architecturally this manifests as default allow-all (firewalls, ACLs, auth checks) vs. default deny-all.
**Analogy:** A bank vault with a fire — fail-safe unlocks the doors so people can evacuate; fail-secure keeps them locked so robbers can't exploit the chaos. Both are defensible, but you must pre-commit.
**Example:** A traffic-light controller fails to flashing-yellow (fail-safe so traffic keeps moving). A nuclear reactor SCRAMs control rods on fault (fail-secure / fail-safe in the safety sense).
**Common pitfall:** Mixing the two ad-hoc — half the system fails open, half fails closed — produces inconsistent, unauditable behavior. Set the posture organisation-wide.
**Related lectures:** L4 (testability & deployability — chaos engineering), L5 (availability — fault tactics).

### Security as a constraint (not just a quality attribute)
**Definition:** Security manifests as a *constraint* placed on Design, Architecture, *and* Implementation simultaneously, in addition to being a quality attribute exhibited by the system.
**Why it matters:** Treating security as "another -ility" measured at runtime is too late; it must shape the design space upfront. Microsoft's SDL embeds it at every gate.
**Detailed explanation:** Lecture's Figures 7-10 build a stack: Requirements → Architecture → Implementation, with "Constraints" and "Security Constraints" feeding into each. Example security constraints: attack-surface minimization (architectural), language/library choices, coding standards, mandatory code review (implementation), threat-modeled requirements (requirements).
**Analogy:** Like building codes — you don't measure fire-resistance after pouring concrete; the code constrains what concrete you may pour, where you may put doors, how wide stairwells must be.
**Example:** A constraint "no eval()-style dynamic code execution in production code" is an implementation-level security constraint; "all inter-service traffic must traverse mTLS" is architectural.
**Common pitfall:** Conflating "security feature" (authn module) with "security constraint" (no plaintext secrets in env vars). Constraints bind the whole solution space; features sit inside it.
**Related diagram:** see L9 figures 7-10 (rendered conceptually; not all kept).

### Microsoft Security Development Lifecycle (SDL) with three gates
**Definition:** A five-stage pipeline — **Design → Implementation → Build → Deploy → Run** — with three security gates, on a zero-trust foundation.
**Why it matters:** Gives architects a vocabulary for where each control lives and who owns it. Each gate prevents a different class of compromise.
**Detailed explanation:** Gate 1 (between Implementation and Build) audits dev-time security — vulnerability scanning, secure-coding compliance, *operational security of developers themselves* (account/credential hygiene). Gate 2 (between Build and Deploy) audits CI/CD pipelines and their infrastructure. Gate 3 (between Deploy and Run) covers hardening and secure configuration of the deployed system. Baseline assumption underneath all of it: zero-trust (assume compromise, explicit trust boundaries, least privilege).
**Analogy:** Airport security: pre-flight check (Gate 1: passport, ticket), baggage screening (Gate 2: pipeline contents), boarding gate (Gate 3: matching person to seat at point of deployment).
**Example:** Gate 2 catches a poisoned CI runner that's been compromised by a phishing attack on the maintainer. Gate 3 catches a Kubernetes deployment shipped with default service-account tokens enabled.
**Common pitfall:** Treating "shift-left" as moving every check to Gate 1 — runtime hardening (Gate 3) is still essential because configs drift after deployment.
**Related diagram:** `![SDL pipeline with gates](../images/lecture_9/page020_microsoft_sdl_model.png)`

### Operational security of developers (social engineering)
**Definition:** Protecting the *humans* who build the software — their accounts, keys, repository credentials — from social-engineering attacks aimed at package or account takeover.
**Why it matters:** Zimmermann et al. (2019) showed that the npm ecosystem has a "small world with high risks" topology — compromising one heavily-depended-on maintainer cascades into thousands of downstream apps. The architecture is irrelevant if a maintainer's PAT is phished.
**Detailed explanation:** Two attack patterns are explicit: package takeovers (attacker becomes a co-maintainer, then ships malicious release) and account takeovers (stealing keys/credentials directly). Defences are mostly non-technical: maintainer hygiene, MFA, hardware tokens, signed commits, and limiting auto-merge.
**Analogy:** A vault is irrelevant if the bank manager hands over the combination after a phone call.
**Example:** event-stream npm incident (2018); ua-parser-js (2021); xz-utils (2024) — all began with social/credential compromise, not code-level exploits.
**Common pitfall:** Architects who design beautiful zero-trust diagrams while leaving the GitHub org with no SSO enforcement.
**Related lectures:** L8's SBOM and supply-chain discussion explicitly hands off to this.

### OWASP CI/CD Top-10 risks + auto-merge restrictions
**Definition:** OWASP's enumeration of the most common security risks specific to CI/CD pipelines (poisoned pipeline execution, insufficient flow control, inadequate IAM, etc.).
**Why it matters:** CI/CD pipelines are increasingly the highest-privilege component in a system — they sign artifacts, hold cloud credentials, and push to production. They're also the least scrutinized.
**Detailed explanation:** Lecture's concrete recommendations: (i) limit auto-merge, (ii) require prior approval of a CI/CD account for artifacts to flow end-to-end, (iii) prevent non-authorized accounts from triggering production builds/deployments, (iv) require approvals + reviews on production branches.
**Analogy:** Treating the build robot like an unsupervised intern with the master key.
**Example:** A PR that bumps a dep version auto-merges and triggers a production deploy; the new dep version was tampered with after publishing.
**Common pitfall:** Adding "approvals required" only to `main` while leaving the deploy workflow triggerable by tags any maintainer can push.
**Related diagram:** `![OWASP CI/CD Top-10](../images/lecture_9/page023_owasp_cicd_top10.png)`

### Threat modeling (Microsoft's four-task loop)
**Definition:** A structured design-phase activity to enumerate threats and design countermeasures before code is written.
**Why it matters:** Threats found at design cost orders-of-magnitude less to fix than threats found in production. Threat modeling produces traceable security requirements.
**Detailed explanation:** Four tasks: (1) Identify use cases, scenarios, and assets — *what are the business functions and inputs; what assets must be protected?* (2) Create an architecture overview — *at minimum, subsystems, trust boundaries, and data flows via connectors.* (3) Identify threats — *analyze from the attacker's perspective, then rate and prioritize.* (4) Identify, apply, and track countermeasures — *review, document, apply, test; document and accept any deviations.*
**Analogy:** A war-game / red-team table-top exercise on paper before the system exists.
**Example:** For an AI bug-fix agent (Case #8), assets = source code repo, CI credentials, PR-merge permission; threats include prompt injection, agent-to-agent collusion, supply-chain takeover; countermeasures include human-in-the-loop merge, scoped tokens, output validation.
**Common pitfall:** Stopping at task 3 — threats listed but countermeasures never tracked. The "deviations accepted" register is what makes the model auditable.
**Related diagram:** `![Threat modeling tasks](../images/lecture_9/page032_threat_modeling_tasks.png)`

### Trust boundaries (three scales)
**Definition:** Lines in the design across which authentication, authorization, or data validation must be re-established because the level of trust changes.
**Why it matters:** Every boundary is an enforcement point — and every missing boundary is a weakness. The kill chain is largely the story of an attacker crossing boundaries that weren't enforced.
**Detailed explanation:** Three scales discussed:
- **Hardware / protection rings** — kernel ↔ userland; CPU/memory privilege levels (ring 0 ↔ ring 3); the darker the colour in the slide, the higher the privilege.
- **Component / machine level** — components inside a machine trust each other; cross-machine they shouldn't unless an explicit trust relationship is declared.
- **Deployment level** — cloud cluster ↔ on-premise ↔ local LAN ↔ WiFi access point ↔ Internet. Each transition is a boundary.
**Analogy:** A castle has the moat, curtain wall, inner bailey, keep, and finally the king's chamber — each line crossed should require reauthentication.
**Example:** A microservice running in pod A on cluster X talking to pod B on cluster Y crosses cluster, possibly network, and definitely service-mesh boundaries — each should enforce mTLS + policy.
**Common pitfall:** Treating "inside the firewall" as one big trust zone (the "M&M model" — crunchy outside, soft inside). The kill chain destroys this assumption.
**Related diagrams:** `![Protection rings](../images/lecture_9/page034_protection_rings.png)`, `![Deployment-level trust boundaries](../images/lecture_9/page036_trust_boundaries.png)`

### The cyber kill chain (worked example, 8 steps)
**Definition:** A canonical staged attack model: initial exploit → privilege escalation → boundary escape → reconnaissance → lateral movement → data exfiltration → log tampering → persistence (RAT).
**Why it matters:** It teaches architects *why* defense-in-depth matters: stopping any single link breaks the whole chain. It also reveals which design tactics matter at which step.
**Detailed explanation:** Lecture's worked example:
1. Attacker exploits a vulnerability inside `Container_j`, gaining control of `Process_j` (uid=1000).
2. Privilege-escalation exploit raises uid to 0 (root) *inside the container*.
3. A *container-escape* exploit lets the rooted process escape the container; attacker now controls `Machine_i`.
4. Reconnaissance: scan for other machines, build a topology.
5. Lateral movement: re-use the same exploit chain on `Machine_1`.
6. Data exfiltration: establish encrypted tunnel via a compromised proxy machine in the dark web; transfer data; close tunnel.
7. Tampering: clean logs on both compromised machines.
8. Persistence: install Remote Access Trojan (RAT) for re-entry.
**Lessons drawn explicitly in the lecture:**
1. Exploitation **chains** (plural) are needed for a full compromise.
2. Privilege escalation is usually required.
3. Isolation mechanisms (containers, VMs) are breakable but raise the cost.
4. Reconnaissance is the prerequisite for lateral movement.
5. Logging must be designed defensively — *log tampering is itself a stage*.
6. Zero-trust matters because simple DMZs are insufficient.
**Analogy:** A burglary that begins with picking a window lock, then finding the gun safe combination, then ramming the safe, then casing other houses on the street.
**Example:** SolarWinds / xz-utils / Volt Typhoon campaigns all follow recognisable kill-chain stages.
**Common pitfall:** Designing only against initial-access vectors and ignoring later stages (escalation, exfiltration, tamper-resistant logging).
**Related diagrams:** `![Kill-chain priv-esc step](../images/lecture_9/page038_killchain_privesc.png)`, `![Inadequate DMZ + firewall + IDS](../images/lecture_9/page044_dmz_firewall_ids.png)`

### Zero-trust architecture (layered)
**Definition:** Architectural style with the explicit assumption *"compromise has already happened, somewhere"* — no implicit trust based on network location; every request authenticated, authorized, encrypted.
**Why it matters:** It is the modern alternative to the DMZ / perimeter model the kill chain exposes as inadequate.
**Detailed explanation:** Slide adopted from NCSC 2025 shows three layers: **Access layer** (where users/devices enter — VPN gateway, reverse proxy), **Policy layer** (authn/authz decisions, possibly per-request), **On-premise / resource layer** (the protected assets). Crucially, the policy layer sits between Internet and the resource layer for every flow — even from already-authenticated cloud workloads.
**Analogy:** A nightclub where the bouncer rechecks ID at every door inside, not just the front.
**Example:** Google's BeyondCorp — engineers access internal services from the open internet, with per-request device + identity verification, no VPN required.
**Common pitfall:** Reading "zero trust = mTLS" and stopping there. ZT is a policy + continuous-verification model; mTLS is one mechanism.
**Related diagram:** `![Zero-trust three layers](../images/lecture_9/page048_zero_trust_architecture.png)`

### Sidecar pattern for zero-trust
**Definition:** A deployment pattern where each business-logic container in a pod gets an adjacent "sidecar" container that handles cross-cutting security concerns: authentication, authorization, mTLS, monitoring, routing.
**Why it matters:** Lets you centralize ZT enforcement *without* coupling it to business code. Underpins service meshes (Istio, Linkerd) — see L7.
**Detailed explanation:** Three depicted variants:
- **Shared sidecar pod (Pod_4):** one pod containing authn/authz proxies that all business pods route through; mTLS everywhere.
- **Per-pod sidecar:** every pod gets its own authn/authz sidecar — more isolation, more resources.
- **Ingress/egress gateway:** sidecars at the cluster edge enforce mTLS internally and TLS externally; clients are categorised (consumer / business / internal) — this is *scoping* from L8.
**Analogy:** A bodyguard assigned to every guest at a party — they don't change what the guest does, but they verify every interaction.
**Example:** Istio's Envoy proxy injected into every pod; SPIFFE/SPIRE identities.
**Common pitfall:** Adding sidecars but forgetting *egress* filtering — exfiltration through unmonitored outbound DNS or HTTP remains possible (cf. DNS tunneling from L8).
**Related diagrams:** `![Sidecar with shared pod](../images/lecture_9/page049_sidecar_zero_trust.png)`, `![Sidecar with honeypot routing](../images/lecture_9/page052_sidecar_honeypot.png)`

### Honeypots and deception
**Definition:** A deliberate decoy resource that looks like a real target, used to attract, observe, and forensically study attackers.
**Why it matters:** Cyber security is also about *deception*, not only defense. A honeypot turns reconnaissance into an early-warning signal.
**Detailed explanation:** Sidecar routes suspicious clients to a honeypot environment that runs forensics + monitoring. Attackers waste effort on a fake; defenders gain TTP intel (tactics, techniques, procedures).
**Analogy:** A dummy safe in a museum stocked with fake jewels and a hidden camera.
**Example:** SSH honeypot (Cowrie) on a public IP — collects credential-spray attempts and post-exploit commands.
**Common pitfall:** Honeypots leaking into real infrastructure (shared logging, shared accounts) — the attacker pivots from the decoy into the real system. The honeypot must itself be isolated.
**Related diagram:** `![Sidecar honeypot routing](../images/lecture_9/page052_sidecar_honeypot.png)`

### Egress filtering / output validation
**Definition:** Inspecting and restricting *outbound* traffic from a system, symmetrical to inbound input validation.
**Why it matters:** Reduces blast radius — if an attacker is already inside, egress filtering blocks data exfiltration and command-and-control (C2) callbacks.
**Detailed explanation:** Just as input validation prevents bad data from entering a component, output (egress) validation prevents bad data from leaving the system. Applies to networking via egress filters at the firewall, sidecar, or gateway. Required because techniques like DNS tunnelling (L8) bypass naïve outbound rules.
**Analogy:** Customs check on the way *out* of a country, not just on arrival.
**Example:** Allowlist of outbound destinations for production pods; drop everything else (default-deny outbound).
**Common pitfall:** Allowing wide outbound DNS or HTTP to "the internet" for "package updates" — used by both legitimate apt and exfiltration.
**Related diagram:** `![Validation w/ egress filter](../images/lecture_9/page047_validation_egress_filter.png)`

### Confused deputy
**Definition:** A program that holds authority on behalf of multiple principals and is tricked into misusing its authority for one principal at the expense of another.
**Why it matters:** A classic architectural anti-pattern — your monitoring/proxy/middleware ends up performing privileged actions on behalf of untrusted callers.
**Detailed explanation:** Original example (Norm Hardy 1988): a compiler that could write to a billing file *and* accept user-specified output files — a user names the billing file as their output, the compiler writes to it. Modern analogue: a monitoring service with read-everything privileges that exposes an HTTP query interface — any caller becomes effectively privileged.
**Analogy:** Giving your bank manager (deputy) power-of-attorney, then anyone who walks in and asks them to "do this for me" gets your full authority.
**Example:** SSRF (Server-Side Request Forgery) — the web app has internal-network access, an attacker tricks it into fetching `http://169.254.169.254/...` (AWS metadata).
**Common pitfall:** Granting a monitoring/agent component broad privileges "to make it work." Use capability tokens or scoped tokens instead — tactic relevant to the lecture's Q on page 55.
**Related lectures:** L8's privilege-drop / least-privilege tactic is the direct mitigation.

### Data classification
**Definition:** Categorising data by type, sensitivity, and risk so that controls (encryption, retention, access) can be applied proportionally.
**Why it matters:** "Encrypt everything" is unaffordable and useless if the keys live next to the data; classification tells you *what* must be encrypted, *where*, and *who* may decrypt.
**Detailed explanation:** Microsoft (2026b) explicit recommendation. Lecture's example: GDPR personal-data classification (Hjerppe 2019) — separate modules for *core personal data* (R5-R7), *event log* (R4), *consent center* (R3), *restriction center* (R8), behind a GDPR-request service interface. Each gets its own controls.
**Analogy:** Libraries classifying books by sensitivity — open stacks vs. closed stacks vs. archives requiring an appointment.
**Example:** Tagging columns in a data warehouse as PII / financial / public and applying column-level encryption only on the PII columns.
**Common pitfall:** Classifying at one snapshot and never re-classifying as the system evolves. Personal data leaks into log files, etc.
**Related lectures:** L2's quality attributes — privacy / compliance scenarios drive classification.

### Side-channel attacks
**Definition:** Attacks that exfiltrate information from a system through unintended physical/timing channels rather than the official interface.
**Why it matters:** Cloud multi-tenancy means an attacker can be on the same hardware as you. Spectre/Meltdown/Foreshadow/Hertzbleed are not theoretical.
**Detailed explanation:** Side channels include timings, cache state, power consumption, acoustic emanations, EM emissions. Many bypass protection rings (CPU/memory/cache). Lecture's slide shows a malicious Node_6 in a cluster *inferring* about Node_1 without direct interaction.
**Analogy:** Listening to a safe-dial click pattern to infer the combination — never touching the dial yourself.
**Example:** Spectre-style cross-process cache attacks; AWS co-residency attacks (Ristenpart 2009).
**Common pitfall:** "We don't run untrusted code" — multi-tenant cloud nodes do, by definition, from your provider's perspective. Defences: dedicated tenancy; or accept the risk and minimise sensitive computations on shared hosts. General mitigations: plug the leak (constant-time code) or add noise (jittering).
**Related diagrams:** referenced page 59 (rendered but not kept; protection rings page 34 covers the underlying hardware boundaries).

### MitM attacks and Conti-Dragoni countermeasures
**Definition:** Man-in-the-Middle: an attacker interposed between two endpoints intercepting, modifying, or destroying traffic — violates all of CIA.
**Why it matters:** Networking is itself an attack surface; secure-design at the *connector* layer (L1's term) is mandatory.
**Detailed explanation:** Conti & Dragoni (2016) classify MitM along three axes: (a) impersonation type, (b) communication channel, (c) network location. Documented historically against many OSI layers — BGP / DHCP / DNS (L7 Application), TLS (L6 Presentation), IP (L4 Transport), ARP (L2 Data link). Seven defensive design principles:
1. Strong **mutual** authentication for all endpoints.
2. Exchange private keys over a secure channel.
3. Use *few* secure channels for integrity verification.
4. Sign public keys via a certified authority (PKI / CA).
5. Use **certificate pinning**.
6. Encrypt communication.
7. Continuously examine endpoint behaviour against an agreed protocol.
**Important caveat from the lecture:** Principle 6 (encryption) is *meaningless* if 1-2 (or even 4) are broken. Encrypting to the wrong (or attacker's) key gives the attacker your data with confidence.
**Analogy:** Sealing a letter with wax but handing it to the spy at the post office because you never verified his uniform.
**Example:** ARP spoofing on a LAN; rogue DHCP server; BGP route hijack (e.g. Pakistan-YouTube 2008).
**Common pitfall:** Adding TLS without certificate pinning on a mobile client — a corporate proxy with a CA-trusted MitM cert sees everything.
**Related diagram:** `![MitM protocol table](../images/lecture_9/page062_mitm_protocol_table.png)`

### Designing for cryptography (data in transit / at rest / in processing)
**Definition:** Crypto-as-design-discipline: choose where data is encrypted at rest, in transit, and *minimise* the window in which it is unencrypted during processing.
**Why it matters:** Most production breaches exploit the *processing window* — memory dumps, debug logs, swap files, third-party API calls passing through plaintext.
**Detailed explanation:** "Robust techniques exist for encryption at rest and in transit" — design's job is to ensure the *plaintext processing window* is as short and isolated as possible. Implies enclaves, ephemeral memory, secret rotation, secrets-managers fetching just-in-time.
**Analogy:** Cash-in-transit security: armoured truck (transit), bank vault (rest); inside the till during a sale (processing) is the brief vulnerable moment — minimise it.
**Example:** Homomorphic encryption / confidential computing (Intel SGX, AMD SEV) keep data encrypted even during processing. For most apps: TLS termination at the application boundary, decrypt only into a short-lived buffer, scrub after use.
**Common pitfall:** Encrypting at rest with the key in the same config file as the DB connection string — equivalent to no encryption.
**Related diagram:** `![Encryption lifecycle](../images/lecture_9/page068_encryption_lifecycle.png)`

### CI/CD networking hardening (HTTP → SSH → SSH+HTTPS)
**Definition:** A progressive hardening exercise for the network layer of a small build/deploy/analytics topology.
**Why it matters:** Most teams' CI/CD inherits weak defaults that are catastrophic if exposed.
**Detailed explanation:** Lecture walks three iterations:
- **Fig 44 (bad):** Build/test/deploy servers connected by plain **HTTP** + a "shared secret"; the certificate "for establishing TLS" is unused. Wide-open MitM target.
- **Fig 45 (better):** Replace HTTP with **SSH** for all hops. Still: SSH is for control, not necessarily for HTTP-based service traffic; clients still need HTTPS.
- **Fig 46/47 (good):** **SSH for control plane, HTTPS for use plane**, plus *integrity checks* before pushing to production.
**Analogy:** Locking the office (SSH for admin) and locking the cash register (HTTPS for sales) — two different locks for two different threat models.
**Example:** Jenkins controller ↔ agents over SSH; service users hit the deployed app over HTTPS; final artifact hash is verified pre-deploy.
**Common pitfall:** Using HTTPS for everything *including* admin — works, but loses the audit/keypair semantics of SSH for human operators.

### Hardening tools for Kubernetes (architectural awareness)
**Definition:** Specialised scanners that check a cluster's *configuration* for security weaknesses (not its code or images).
**Why it matters:** Configuration drift after deploy is where Gate 3 fails silently.
**Detailed explanation:** Lecture names a dozen for Kubernetes alone — Checkov, Kubeaudit, KubeLinter, Kube-score, Kubesec, SLI-KUBE, Kube-bench, Kubescape, Trivy, NeuVector, StackRox. Two architectural placements for scanning: (a) in-cluster scanner/audit nodes filtering new pods before they reach a worker; (b) registry-pull-and-scan loop comparing images to vulnerability DBs and updating affected nodes.
**Analogy:** A building inspector who returns every quarter to recheck the wiring — code hasn't changed, but the building's risk profile has.
**Example:** A nightly Trivy scan flags that an image you deployed a month ago now has a critical CVE.
**Common pitfall:** Scanning only at admission and never on the running fleet (Gate-3 blindness once configs drift or new CVEs land).

## Important diagrams (catalog)

- `page013_security_tradeoffs.png` — Five canonical trade-offs that bound security: risk, cost, usability, performance, privacy.
- `page020_microsoft_sdl_model.png` — Microsoft SDL pipeline (Design→Implementation→Build→Deploy→Run) with Gates 1/2/3 over a zero-trust baseline.
- `page023_owasp_cicd_top10.png` — OWASP CI/CD Top-10 risks (screenshot of OWASP project).
- `page032_threat_modeling_tasks.png` — Microsoft's 4-task threat-modeling loop: assets → arch overview → threats → countermeasures.
- `page034_protection_rings.png` — CPU/kernel/userland protection rings; "ring 0" terminology.
- `page036_trust_boundaries.png` — Deployment-level trust boundaries across cloud cluster, on-prem, LAN, WiFi, Internet.
- `page038_killchain_privesc.png` — Kill-chain stage 2: in-container privilege escalation to root.
- `page044_dmz_firewall_ids.png` — Why a naïve DMZ + firewall + IDS deployment is insufficient given the kill chain.
- `page047_validation_egress_filter.png` — Sidecar validation + egress (output) network filter on the cluster edge.
- `page048_zero_trust_architecture.png` — Three-layer zero-trust architecture (Access / Policy / On-premise) per NCSC 2025.
- `page049_sidecar_zero_trust.png` — Sidecar pattern with shared authn/authz pod and mTLS everywhere.
- `page052_sidecar_honeypot.png` — Sidecar routing suspicious clients to a honeypot for forensics.
- `page062_mitm_protocol_table.png` — Table: OSI layers and Internet protocols historically attacked via MitM (BGP/DHCP/DNS/TLS/IP/ARP).
- `page068_encryption_lifecycle.png` — Designing for encryption: at-rest, in-transit, and minimising the unencrypted processing window.

## Exam-relevant takeaways

1. **Fail-safe vs. fail-secure** is a non-negotiable organisational decision — be ready to explain when you'd pick each (reliability- vs. security-critical assets), with examples.
2. **Security is a constraint** that crosscuts requirements, architecture and implementation — not "just another quality attribute." Be ready to list constraints at each layer (attack-surface min, lang choice, coding standards, mTLS).
3. **Microsoft SDL = 5 stages + 3 gates + zero-trust baseline.** Know which gate catches what: Gate 1 dev/SCA, Gate 2 CI/CD pipeline integrity, Gate 3 deployment hardening.
4. **The four-step threat-modeling loop** (assets → arch → threats → countermeasures) including the *deviations register* — easy to draw and explain.
5. **The kill chain has 6+ stages** beyond initial access (priv-esc, escape, recon, lateral, exfil, tamper, persist). Defense-in-depth means breaking any one link.
6. **Trust boundaries exist at three scales** — hardware rings, machine/component, deployment. Be ready to draw all three.
7. **Zero-trust = "assume compromise + verify every request"**, not "VPN replacement." Three-layer architecture (Access/Policy/Resource); sidecar pattern is the canonical implementation.
8. **Egress (output) validation matters as much as input validation** — symmetric to it; needed against C2 + exfil; DNS tunnelling defeats naïve filters.
9. **Confused deputy** = a privileged component duped into misusing its privileges; mitigated by least-privilege + scoped capabilities (L8 tactic).
10. **MitM countermeasures** = 7 principles; principle 6 (encrypt) is null without 1, 2, 4 (mutual authn, secure key exchange, CA-signed keys).
11. **Cryptographic design** minimises the *plaintext processing window*; "encrypted at rest" with the key in the same env is meaningless.
12. **Side-channel attacks** evade protection rings entirely; defences are limited (constant-time code, noise injection, dedicated tenancy).

## Cross-references

- **L1 (Foundations):** "Connectors" terminology used throughout L9 for networking links; the Components-Connectors-Constraints triple is referenced when discussing security as a *constraint*. Trust-boundary diagrams use 4+1-deployment-view notation.
- **L2 (Quality Attributes):** L9 reframes security as both a quality attribute *and* a constraint — extends L2's scenario template by adding "deviations register" and "acceptable risk level." ISO/IEC 25010's security characteristic (confidentiality, integrity, non-repudiation, accountability, authenticity) maps onto MitM countermeasures.
- **L3 (Integrability/Modifiability):** Sidecar pattern is an integration tactic; mentioned here as the security-policy enforcement point. Plugin/sidecar separation enables swappable authz policies.
- **L4 (Testability/Deployability):** SDL Gate 2 (CI/CD pipeline integrity) directly extends L4's CI/CD discussion. Blue-green/canary deployments must themselves be hardened.
- **L5 (Availability):** Fail-safe vs. fail-secure trade-off ties to L5's reliability tactics (watchdog, voting, sagas). Bulkheads/isolation in L5 are the same architectural primitive that limits kill-chain blast radius.
- **L6 (Performance):** Encryption introduces compute cost (CAP/PACELC + crypto overhead); side-channels exploit timing — both are perf×security trade-offs. Caching at rest interacts with "encryption at rest."
- **L7 (Scalability):** k8s + service-mesh material from L7 returns — sidecars are the security side of the same architecture. Egress gateway = ingress controller's twin.
- **L8 (Safety+Security, agentic):** L8 is the explicit predecessor. L9's mock-up questions (slides 4-10) re-test L8 concepts (fail-safe/fail-fast, sanitizers, fault vs. failure, container UID isolation, throttling/circuit-breaker). L8's privilege-drop tactic is the direct mitigation for the confused-deputy problem. L8's SBOM/supply-chain handoff lands directly on L9's SDL Gate-1 + Zimmermann npm study.
- **Likely L10 (final):** Given L9 ends with cryptography + CI/CD networking, L10 is likely either (a) a course-wrap / exam-prep / case-study lecture, or (b) one final theme such as DevSecOps, formal methods, or sustainability/green software. To be confirmed by the L10 analyzer.
