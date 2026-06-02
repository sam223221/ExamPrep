# Lecture 8: Safety and Security as Quality Attributes

> **Source:** lecture_8.pdf (85 pages)
> **Lecturer:** Jukka Ruohonen
> **Date (if stated):** April 14, 2026

## Themes covered

1. **Safety as a QA** — its definition relative to security, scenario template, tactics, and the monitor-actuator pattern.
2. **Security scenarios and the tactics tree** (Detect / Resist / React / Recover) with explicit ties to CIA.
3. **SIEM / SOC** as a concrete realisation of the *detect* tactic, including the pipe-and-filter/broker architecture used inside SIEMs.
4. **LLM and Agentic AI threats** — OWASP top-10 for LLMs, gateway placement, supply-chain compromises (litellm/Telnyx), data leakage.
5. **Input validation as the central security tactic** — centralised validator/enforcer, canonicalisation, data-vs-control separation, attack-surface minimisation, trust boundaries (SRI, CSP).
6. **GitHub Actions case study** — least privilege, secure defaults ("deny all"), scoped secrets, egress filtering, revoke-access tactic.
7. **Agentic AI as distributed systems** — new trust boundaries, identity binding, non-repudiation, CB4A credential broker draft, mTLS, zero trust.
8. **Least privilege & privilege separation** — drop vs separate (qmail / Postfix history), Kubernetes `securityContext`, OpenBSD `pledge`, breakglass mechanisms.

## Concepts

### Safety (as a quality attribute)
**Definition:** A system's ability to avoid straying into states that cause or lead to damage, injury, or loss of life to actors in its environment (Bass et al. 2021).
**Why it matters:** Safety is one of the few QAs explicitly defined around *impact on the physical world*, not on the system itself; it sets exam-relevant boundary conditions for tactics like "abort" or "fail-safe".
**Detailed explanation:** The definition deliberately says nothing about *why* the system entered the dangerous state — it could be a sensor fault, a software bug, or a malicious attacker. That neutrality is exactly what separates safety from security: security always presumes an intentional adversarial actor. Many safety tactics overlap with availability/fault-tolerance tactics, so the lecture spends less time on them — but stresses the **impact dimension** (damage, injury, loss of life) as the distinguishing axis.
**Analogy:** A railway-crossing barrier is a safety device whether it fails because of a rusted hinge (no attacker), a sensor glitch (no attacker), or a vandal cutting wires (attacker). All three threaten the same outcome — a car on the track — so safety engineering must cover them all.
**Example:** A medical infusion pump that locks into "stop infusion" if its dose sensor reports an out-of-range value is using the *abort* impact-limiting tactic.
**Common pitfall / nuance:** Students often equate safety with security or with reliability. The relation is asymmetric: insecurity *can* cause safety issues (an attacker turning off a brake), but a safety failure rarely implies a security failure.
**Related diagram:** `![Safety scenarios template](../images/lecture_8/page017_safety_scenarios.png)`

### Safety scenario template
**Definition:** A six-part description (Source, Event, Environment, System, Response, Response Measure) tailored to capture safety-relevant stimuli and required behaviours.
**Why it matters:** Every QA in this course uses a scenario template; safety's variant makes "unsafe state" the central concept that drives both response and measurement.
**Detailed explanation:** Sources are *user action / data source / time source*; events are categorised as **omission** (a value/call never arrives), **commission** (an incorrect execution, spurious event/data), or **timing** (too late, too early, wrong order, wrong rate). Responses include *avoid an unsafe state, recover, continue in degraded/safe mode, shutdown gracefully, switch to manual, switch to backup, notify, log entries into unsafe states.* Measures focus on *share* and *time* in unsafe / degraded / manual / shutdown states.
**Analogy:** Like an aviation incident report template — every field forces you to specify a property you would otherwise hand-wave (who/what/when/where, how the plane responded, how long it took to stabilise).
**Example:** "When a temperature sensor stops sending readings (omission) during normal operation, the boiler controller must enter a safe-stop within 200 ms (response) with at most 0.1 % of such events failing to reach safe-stop (measure)."
**Common pitfall / nuance:** Students conflate "shutdown gracefully" with "abort". Aborting is *one impact-limiting tactic*; graceful shutdown is a response category that may or may not use abort.

### Safety tactics tree
**Definition:** A categorised inventory of design moves for safety, grouped under Avoidance, Detection, Containment, and Recovery.
**Why it matters:** It is the directly-examinable structure that mirrors the QA pattern set up in lectures 3-7.
**Detailed explanation:**
- **Avoidance:** *Substitution*, *Predictive models*.
- **Detection:** *Sanity check, Comparison, Timeout, Monitoring, Timestamps*.
- **Containment:** subdivided into **Redundancy** (Replication, Analytical redundancy, Functional redundancy), **Limit impact** (Masking, Abort, Degradation), and **Barrier** (Firewall, Barrier).
- **Recovery:** *Isolate, Removal from the system, Transactions, Predictive models, Exception prevention, Increase competence*.
Most of these mirror availability/fault-tolerance tactics; what is *new* is the framing of **barrier** as limiting propagation of unsafe states, with firewall as its security-specific variant.
**Analogy:** Castle defence in layers — moat (avoidance), watchtower (detection), inner wall (containment), siege-recovery plan (recovery).
**Example:** A nuclear control room uses *replication* (three independent sensors), *comparison* (voting), *abort* (SCRAM reactor), and *isolate* (separate reactor coolant loops) — one tactic from each branch.
**Common pitfall / nuance:** "Increase competence" is a *recovery* tactic — sometimes the right move is to bring in a human expert, not to reduce the system further.
**Related diagram:** `![Safety tactics tree](../images/lecture_8/page018_safety_tactics_tree.png)`

### Monitor-actuator pattern
**Definition:** A safety pattern where a software actuator's commands are checked by an independent monitor before reaching the hardware actuator; on a faulty check the operation is either dropped (A) or actively aborted (B).
**Why it matters:** Concrete, exam-friendly synthesis of redundancy + sanity check + barrier + assertion tactics.
**Detailed explanation:** Variant A is permissive — the monitor verifies and only forwards on OK. Variant B is active — on FAULT the monitor *aborts* the path, escalating from detection to impact-limiting. Both rely on the *monitor* being a logically independent component, otherwise a single fault knocks out both.
**Analogy:** A second pilot whose only job is to check the captain's commands before the autopilot accepts them.
**Example:** In an industrial robot, the motion controller (software actuator) sends a position command; a watchdog co-processor (monitor) verifies it is within the geometric envelope before the servo amplifier (hardware actuator) drives the motor.
**Common pitfall / nuance:** The monitor and software actuator must not share their failure mode (independent power, independent clock, ideally different code paths) — otherwise it is theatre, not redundancy.
**Related diagram:** `![Monitor-actuator pattern](../images/lecture_8/page021_monitor_actuator_pattern.png)`

### Security (as a quality attribute, distinct from safety)
**Definition:** A QA concerned with system properties under *intentional adversarial action* — typically violations of Confidentiality, Integrity, or Availability (CIA).
**Why it matters:** Distinguishing security from safety justifies a different scenario template (with insider/outsider/AI sources) and a tactic tree centred on Detect/Resist/React/Recover rather than on unsafe-state avoidance.
**Detailed explanation:** The lecture builds security scenarios with sources spanning *insider/outsider, human/machine/AI, known/unknown*; events as CIA violations; responses including *security controls, authn, authz, encryption, logging, incident management, damage control*. Measures move beyond performance latency into *attack detection accuracy, blast radius, time-to-discover, time-to-notify, time-to-recover, financial losses, legal consequences, post-incident analysis*.
**Analogy:** Safety asks "what if the bridge collapses?"; security asks "what if someone is trying to collapse it?"
**Example:** A ransomware attacker exfiltrates database backups (confidentiality violation by an external human) — the response measure includes blast radius (which records were leaked) and time-to-notify (regulator clock under GDPR/CRA).
**Common pitfall / nuance:** Even with AI agents acting as sources, *someone still controls the botnet*. The "actor" abstraction stays human even when the immediate stimulus is machine-generated.
**Related diagram:** `![Security scenarios template](../images/lecture_8/page022_security_scenarios.png)`

### Security tactics tree
**Definition:** Four-branch tree of security design moves: **Detect**, **Resist**, **React**, **Recover**.
**Why it matters:** Maps the CIA-based scenario above to concrete architectural moves the student can name in an exam.
**Detailed explanation:**
- **Detect:** *Intrusions, Service denials, Integrity violations, Anomalies*.
- **Resist:** *Threat modeling, Authentication, Authorization, Isolate, Minimize attack surface, Limit resources, Encrypt, Validate input, Change credentials, Revoke access, Restrict access*.
- **React:** *Inform actors, Audit, Non-repudiation, Inform stakeholders, Minimize damage*.
- **Recover:** plus *Isolate* shared between Recover and Resist.
The course concentrates on **SIEM (detect), input validation, attack-surface minimisation, and authn/authz in the LLM/agentic context**.
**Analogy:** A bank's security: cameras and alarms (detect), vaults and guards (resist), call the police (react), insurance/rebuild (recover).
**Example:** Rate-limiting an API endpoint = *limit resources* (Resist); blocking a host after detection = *revoke access* (Resist) plus *react* responses.
**Common pitfall / nuance:** *Threat modeling* is a tactic — students forget it is itself an architecture-time activity, not a runtime mechanism.
**Related diagram:** `![Security tactics tree](../images/lecture_8/page025_security_tactics_tree.png)`

### SIEM / SOC
**Definition:** Security Information and Event Management (SIEM) systems centralise security telemetry; a Security Operations Centre (SOC) is the organisational equivalent, often used as a synonym.
**Why it matters:** SIEM is the canonical *Detect-tactic* realisation and a working example of brokers, filters and pipe-and-filter at scale.
**Detailed explanation:** Internal sources (IDS, spam filters, firewall logs, audit trails) and external sources (threat/vulnerability feeds) flow into a *log broker* → *log filter* → *raw archiver / normaliser / enricher / event broker / alert broker / archiver / GUI / email-SMS notifier*. Brokers are drawn because relationships are many-to-many. Vakulov (2026) argues the operator workload has two functions — (1) classify maliciousness and (2) act on true positives — and AI can reduce both via operational autonomy, analytical assistance, and delegated decisions.
**Analogy:** Air traffic control tower: every radar, weather station and pilot transmission funnels into one room where humans (and increasingly software) decide what is anomalous and what action to take.
**Example:** A login attempt from a new country triggers normalisation (parse `auth.log`), enrichment (geo-IP + threat intel lookup), event creation, and an SMS alert to the on-call analyst.
**Common pitfall / nuance:** The lecture asks where the *bottleneck* lies — it is performance, with the GUI/analyst stage being the human throughput limit. The pattern in use is **pipe-and-filter** (or batch-sequential with brokers).
**Related diagram:** `![SIEM architecture](../images/lecture_8/page028_siem_architecture.png)`

### OWASP Top-10 for LLM applications (2024/2025)
**Definition:** A community-curated list of the ten most critical security risks for LLM-based systems.
**Why it matters:** It is the closest thing to a canonical LLM threat catalogue and the launching pad for the rest of the lecture.
**Detailed explanation:** The list: (1) Prompt injection, (2) Information disclosure, (3) Supply-chains, (4) Data and model poisoning, (5) Improper output validation, (6) Excessive agency, (7) Prompt leakage, (8) Embedding weaknesses, (9) Misinformation, (10) Unbounded resource consumption. The lecture immediately notes that these *overlap heavily* — e.g. a prompt-injection payload may also be data poisoning if it persists.
**Analogy:** Like a chef's "top 10 kitchen hazards" — fire and burns aren't really separate problems when the oven explodes.
**Example:** The Telnyx/litellm supply-chain incident from April 2026 (Figure 19) is both #3 (supply-chain) and arguably #4 (model/data poisoning) at the package level.
**Common pitfall / nuance:** Reflexively treating the list as orthogonal categories — Ruohonen explicitly cautions to think in *attack sequences* (Agent → get malicious content → fetch malicious tool → execute) instead.

### LLM gateway placement
**Definition:** A gateway component that mediates between an internal system and external LLM providers (OpenAI, Anthropic, etc.), enforcing rate limits, budget caps, routing, authentication.
**Why it matters:** Reduces attack surface, centralises policy, and makes the *trust boundary* between local code and external LLMs explicit.
**Detailed explanation:** The gateway sits behind firewalls/IDS on the local network and brokers all outbound LLM traffic. Without it, every service that talks to an LLM is a separate trust boundary and a separate place to leak secrets, run prompts, or get poisoned outputs. With it, you have one chokepoint to monitor, rate-limit, and budget — and one place to attack, which is its own risk.
**Analogy:** A corporate VPN concentrator: instead of every laptop calling the internet directly, all traffic threads through one inspected pipe.
**Example:** An internal RAG application routes every request through `llm-gateway.internal`, which checks the calling service's token, enforces a $/day budget, and rewrites prompts to strip PII.
**Common pitfall / nuance:** The gateway can become the bottleneck and a single point of compromise — design it with isolation, replication, and least privilege of its own.
**Related diagram:** `![LLM gateway](../images/lecture_8/page034_llm_gateway.png)`

### Input validation
**Definition:** The architectural tactic of checking all data crossing a trust boundary against a specification before processing.
**Why it matters:** The lecture asserts (~99 % of attacks involve malicious input), so this is *the* central security tactic.
**Detailed explanation:** A TCP/IP packet is input. So is a config file, a CLI argument, an LLM response, an HTTP header, a JSON body. To validate, you must (a) understand external-facing components and (b) trace input propagation through the system. Arce et al. (2014) give five design principles: use a centralised validator (audited, prefer well-known libraries), canonicalise the data (be aware of UTF-8/%-encoding/etc.), recall inputs depend on states, audit nearby code around the input, prefer strongly-typed memory-safe languages.
**Analogy:** Customs at an airport — every traveller is checked once, by trained staff, against a written specification, regardless of how friendly they seem.
**Example:** An "enforcer" component receives input, queries a "specification registry" by data type, dispatches to a "validator", and only forwards data into the system if the validator returns OK; on error, an error response is sent back through the enforcer.
**Common pitfall / nuance:** Validating at the wrong layer (e.g. only the web UI) — by the time data reaches a sub-component, the trust boundary has already been crossed. Also: validate even data from trusted internal sources if it originated externally.
**Related diagram:** `![Input validation with three components](../images/lecture_8/page043_input_validation_three_components.png)`

### Attack-surface minimisation
**Definition:** Reducing the number, breadth, and exposure of external-facing components that accept input.
**Why it matters:** Fewer inputs ⇒ fewer places to validate ⇒ fewer places to get wrong.
**Detailed explanation:** The lecture shows successive sketches: a system with many external-facing components → one with fewer → finally one with a single input channel and two validating components. But the principle interacts with complexity: if the one remaining input channel has a million LOC, you have moved the problem rather than solved it.
**Analogy:** A medieval castle with three small, well-guarded gates is safer than a castle with thirty random doorways — but only if each gate is genuinely well-guarded.
**Example:** Closing all unused TCP ports on a host; putting all external HTTP behind one reverse proxy that handles TLS and bot filtering before traffic touches the application.
**Common pitfall / nuance:** Minimising the *number* of channels does not automatically minimise the *attack surface area* — one large complex endpoint can be worse than several small simple ones.

### Trust boundary
**Definition:** A line in the system where data passes between zones of different trust assumptions, requiring explicit validation/authorisation.
**Why it matters:** Most exploits cross a trust boundary without being noticed; making them explicit is a prerequisite for input validation, authn/authz, and least privilege.
**Detailed explanation:** Examples include: between consumer clients (untrusted) and a web app (trusted), between a web app and a CDN that serves third-party JavaScript, between an agentic browser and the user's host, between an agent and a tool, tool and supply-chain, runtime and execution, host and runtime. **Subresource Integrity (SRI)** and **Content Security Policy (CSP)** are W3C standards that harden the web-app/CDN boundary.
**Analogy:** A national border — you don't need a customs officer between two rooms of the same house, but you do at the airport.
**Example:** The Ruohonen et al. (2018) study found ~31 % of external JavaScript on ~35 k popular websites changed within a 10-day polling window — every page load was a re-cross of an under-policed trust boundary.
**Common pitfall / nuance:** *Coarse* trust boundaries (repository-wide secrets, organisation-wide tokens) are worse than no boundary — they look like a control but actually give broad access.

### Data vs control separation
**Definition:** Architectural principle that data inputs from untrusted sources must never be processed as control instructions (commands, code, queries).
**Why it matters:** This is the deep cause of SQL injection, prompt injection, command injection, etc. — and is harder, not easier, with LLMs.
**Detailed explanation:** Arce et al. (2014) recommend an Enforcer between External Input and the System, with two output paths: "Data given OK" (allowed) and "Control / Not trusted" (blocked or quarantined). For LLMs the NCSC blog ("Prompt injection is not SQL injection") notes the analogy breaks down — with SQL you can sanitise/escape because the grammar is fixed; with natural-language prompts no such grammar exists, so the boundary must be enforced by architecture, not by escaping.
**Analogy:** Reading a letter from a stranger is fine; *executing* its instructions verbatim because the envelope says "official" is not.
**Example:** A RAG agent that retrieves a web page and treats text in the page as instructions to call tools — the page is *data*, not *control*; the architecture must prevent the leap.
**Common pitfall / nuance:** Filtering for "bad" tokens is a losing game — the correct design eliminates the channel through which data can become control in the first place.

### Subresource Integrity (SRI) and Content Security Policy (CSP)
**Definition:** W3C web-security standards. SRI adds an `integrity="sha384-…"` hash to `<script>`/`<link>` tags so the browser refuses to execute modified third-party assets. CSP restricts what origins a page may load scripts/styles/images/etc. from.
**Why it matters:** Concrete, examinable instances of trust-boundary enforcement in the web tier and integrity tactic.
**Detailed explanation:** Without SRI, a CDN compromise silently delivers attacker-controlled JS to millions of sites. With SRI, the browser refuses the script unless the hash matches the one the page author baked in. CSP complements this by listing allowed origins (default-deny). The lecture connects this to the empirical finding that ~31 % of external JS changes within 10 days — so SRI must be combined with vendor discipline.
**Analogy:** Tamper-evident seal on a shipping container — even if the warehouse staff (CDN) substitute the contents, the customer (browser) sees the broken seal.
**Example:** `<script src="//cdn.example.com/lib.js" integrity="sha384-XYZ..." crossorigin="anonymous"></script>` — browser computes the hash of the response body and aborts on mismatch.
**Common pitfall / nuance:** SRI doesn't help if you forget to update the hash on a legitimate library bump — leading developers to drop SRI altogether. Tooling and auto-update are essential.

### GitHub Actions — secure defaults & scoped secrets (case study)
**Definition:** Architectural treatment of CI/CD as a security problem: who can trigger workflows, with which events, with what permissions, and which secrets.
**Why it matters:** A working example of *restrict access, secure defaults, scoped secrets, least privilege, and egress filtering* all in one familiar system.
**Detailed explanation:** Ose & Glass (2026) recommend (a) define triggering identity and allowed events ("deny all, then allow particular" — secure defaults), (b) increase granularity of permissions and scope secrets to specific workflows/paths (no implicit inheritance), and (c) egress filtering — restrict which domains/IPs the workflow may contact and which TLS/HTTP methods are allowed. Egress filtering is theoretically *output* validation. The CRA also requires that a device not harm its networking environment, so egress filtering meets compliance, not just hygiene.
**Analogy:** A new hire on day one gets only the keys they need for their first task and never inherits the previous tenant's master key — and is also not allowed to wander off to any building they like.
**Example:** A Copilot-triggered workflow that runs `npm install` and `npm test` should NOT have access to deploy secrets, should be triggerable only by pull-request events from trusted authors, and should be allowed egress only to `registry.npmjs.org` and `github.com`.
**Common pitfall / nuance:** Repository-wide secrets feel "convenient" but are exactly the *broad-but-shallow* boundary the lecture warns against — they make every workflow a potential secret exfiltration vector.

### Revoke-access tactic
**Definition:** A Resist-tactic where the system actively removes or downgrades an actor's privileges in response to suspicious behaviour or policy violation.
**Why it matters:** It is the dynamic counterpart to authorisation — authz lets the right people in, revoke-access kicks the wrong ones out.
**Detailed explanation:** The lecture's sketch (Figure 34): an authenticated agent issues requests; a *Validator* checks each request against an *AllowedEvents* list and against a *RequestLimit*. Bad requests are denied; on threshold breach, the AgentID is deleted from the registry, revoking access. The pattern combines authentication, authorisation, validation, and rate-limiting.
**Analogy:** A nightclub bouncer who not only checks IDs at the door (authn) and a guest list (authz) but also ejects anyone who breaks the rules inside (revoke).
**Example:** A SOC playbook that automatically suspends a user account after five failed-login attempts from a new geolocation, plus a Splunk alert.
**Common pitfall / nuance:** Revoke-access without **non-repudiation** (audit log binding actions to identities) means you can't tell whom to revoke. The two tactics are paired.
**Related diagram:** `![Revoke access tactic](../images/lecture_8/page058_revoke_access_tactic.png)`

### Trust boundaries for agentic AI
**Definition:** The set of zone-transitions in an agent-based system where input/authorisation must be re-validated.
**Why it matters:** The list is *much longer* than for classical systems; new boundaries are exactly where new attacks occur.
**Detailed explanation:** Lecture's non-exhaustive enumeration: User↔Agent, Agent↔Tool, Tool↔Supply-chain, Execution↔Tool, Agent↔Content, Execution↔Content, Runtime↔Execution, Host↔Runtime, Memory↔Runtime, Host&Memory↔Kernel, … With agentic *skills*: Agent↔Task, Task↔Skill, Execution↔Skill (Didi & Zavodchik 2026, Akamai). Skill-to-skill propagation creates execution propagation — exactly the failure mode that motivates extending the pipe-and-filter pattern with validation between stages.
**Analogy:** A multinational corporation has more borders to cross than a household — every additional country added means more customs offices, more paperwork, more places to smuggle.
**Example:** A coding agent that retrieves a web page (Agent↔Content), then asks for a "summariser skill" (Agent↔Skill), which calls a remote tool (Skill↔Tool) — a malicious page triggers a malicious skill that runs a malicious tool.
**Common pitfall / nuance:** Don't treat all boundaries as equal — Agent↔Content is *new* and badly understood; User↔Agent is old (an authn problem) and well-understood. The new ones are where research is needed.

### Identity binding and non-repudiation for agents
**Definition:** Mechanisms that bind every agent action to an underlying human or service identity with cryptographically defensible provenance.
**Why it matters:** Sierra (2026) argues authorisation must not depend on the model's *interpretation* of a request and must be enforced by deterministic system controls at trust boundaries — only then can audit logs satisfy non-repudiation.
**Detailed explanation:** The lecture's principles (Figure 38): Agentic identities are *bound* to a Human identity (non-repudiation); the agent receives a **scoped secret (token)** with *no inheritance* and *rapid expiry*; authorisation is *execution gating* via validating identities, sessions, tools, resources, risk-categorised data; mTLS everywhere; minimise reliance on static secrets; assume most inputs lead to execution and become adversarial over time (zero trust); continuous monitoring throughout. The IETF CB4A (Credential Broker for Agents) draft generalises this with a credential vault, privilege vault, audit trail, and authentication/authorisation policy infrastructure.
**Analogy:** A temp worker at a high-security site gets a badge that says "valid 9-17 today, lab B only, photographed and logged" — not the permanent employee's master pass.
**Example:** An agent sub-task is granted a token valid for 60 s, limited to one specific tool, with the request reason logged before the credential is issued.
**Common pitfall / nuance:** "An agent cannot authorise another agent" — sub-agent delegation must pass through deterministic policy infrastructure, not through a model deciding the second agent is trustworthy.
**Related diagram:** `![Principles for securing AI agents](../images/lecture_8/page071_securing_ai_agents.png)`

### Credential Broker for Agents (CB4A)
**Definition:** An IETF draft (draft-hartman-credential-broker-4-agents) proposing an architecture in which agents obtain short-lived, scoped credentials from a central policy infrastructure rather than carrying long-lived secrets.
**Why it matters:** Concrete proposal for solving the agent-identity problem with classical architecture (broker pattern) and security tactics.
**Detailed explanation:** Components: Agent runtime (Agent1/original, Agent2/specified) issues a request including who/what/why/time-to-live; the request goes to a Policy Infrastructure with Authentication, Authorization, and Audit Trail components, plus a Credential Vault and Privilege Vault. The policy infrastructure issues a short-lived scoped token, performs scoping/risk-scoring/expiry-management, and writes an audit record. The agent uses the token; afterwards the credential expires.
**Analogy:** A movie-set day-pass office: actors collect a wristband good only for their scene, good only for that day, with the office keeping a log of who entered which set.
**Example:** Agent A wants to call tool T on behalf of user U for reason R for at most 5 min — broker checks policy, mints token, logs everything.
**Common pitfall / nuance:** Don't reinvent — OAuth/OIDC, SPIFFE/SPIRE, and Kubernetes service-account tokens already solve pieces of this. CB4A is a unifying *broker pattern*, not a brand-new protocol.
**Related diagram:** `![CB4A agent security](../images/lecture_8/page073_cb4a_agent_security.png)`

### Least-privilege principle
**Definition:** A software (or process, or token) should operate with the minimum privileges required for its function.
**Why it matters:** It is simultaneously an attack-surface minimisation technique, a blast-radius reducer, and a foundation for privilege drop/separation.
**Detailed explanation:** Especially important when processing input from untrusted sources. Adkins et al. (2020, Google) recommend testing your implementation both **of privileges** (does the code actually drop what it claims?) and **with privileges** (does runtime execution behave correctly under the reduced set?). They also recommend a **breakglass** mechanism — sometimes an authorised operator must intentionally break security to handle emergencies (a physician accessing locked records to save a patient).
**Analogy:** Giving each employee a key to only their own office instead of a master key to the whole building.
**Example:** A web server runs as `www-data` (UID 33), not as root; even a successful RCE only owns the web tier, not the host.
**Common pitfall / nuance:** Untested privilege drop is theatre. Test that the lower-privilege process actually fails to do the high-privilege actions it should not be able to do.

### Privilege drop vs privilege separation
**Definition:** Two related but distinct security techniques. *Privilege drop:* a process starts as superuser, performs initialisation that requires root, then drops to a restricted user. *Privilege separation:* a process starts as superuser and *forks* a restricted child process; the restricted child handles risky operations (network input), the privileged parent only handles the few operations that actually need root, with IPC between them.
**Why it matters:** It is the classical, battle-tested architectural pattern for safely processing untrusted input, with decades of real-world track record (qmail 1997, Postfix, OpenSSH).
**Detailed explanation:** First used by Bernstein in qmail (1997). Postfix is the canonical separation example: privileged components only handle local mail pickup, queue, and external transports; ~16 other processes run as unprivileged "several users", split by function (network input, core, output). The pattern combines isolation + least privilege + IPC.
**Analogy:** A surgeon's scrub-in protocol — the doctor (root) prepares the operating room, but inside the OR everything is touched only by the masked, gloved version (dropped privileges). For separation: a small isolated room where the dirty work happens, with a sealed pass-through to the clean side.
**Example:** Postfix's `local` runs as `_postfix:_postfix`; `smtpd` runs as `_smtpd`; the privileged `pickup` daemon stays root only for the operations it cannot avoid.
**Common pitfall / nuance:** Not all programs *can* drop root entirely — some need privileged ports or hardware access — and that's exactly why separation exists.
**Related diagrams:**
`![Privilege drop and separation](../images/lecture_8/page077_postfix_privilege.png)`

### Kubernetes securityContext (privilege drop in containers)
**Definition:** A pod/container spec field that pins the container's runtime UID/GID and other privilege constraints.
**Why it matters:** Translates classical Unix privilege drop into the container/Kubernetes era — exam-relevant because lecture 7 covered Kubernetes itself.
**Detailed explanation:** Example YAML:
```yaml
kind: Pod
metadata:
  name: example-pod
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 2000
```
The lecture's deployment diagram (Figure 43) shows a Cluster with Node1 (Pod11 → Agent11, Agent12 as `runAsUser: 1000, runAsGroup: 2000`) and Node2 (Pod21 → Agent21 as `runAsUser: 2000, runAsGroup: 2000`) communicating via a Message queue over mTLS — every classical principle (least privilege, isolation, mTLS) operationalised in YAML.
**Analogy:** Like setting the "Standard User" account on a freshly imaged laptop instead of leaving it as Administrator.
**Example:** A LangChain agent container running as UID 1000 with no `CAP_NET_RAW`, no `privileged: true`, and a read-only root filesystem.
**Common pitfall / nuance:** `runAsUser: 0` (i.e., root) is the default for many base images — silently undoing the entire safeguard.
**Related diagram:** `![K8s privilege drop](../images/lecture_8/page079_k8s_privilege_drop.png)`

### OpenBSD pledge (system-call sandboxing)
**Definition:** A POSIX-ish primitive (`pledge(2)`) by which a process voluntarily restricts the system calls and capabilities it can subsequently use; future syscalls outside the pledged set kill the process.
**Why it matters:** Mentioned as an OS-level example of attack-surface minimisation and least privilege — the program drops capabilities it knows it will never need.
**Detailed explanation:** A program might `pledge("stdio rpath", NULL)` after opening its files, meaning "from now on I only need stdio and read-only paths" — any attempt at network/exec/wpath terminates the program. It is a one-way ratchet.
**Analogy:** A trapeze artist who, after climbing to the platform, throws away the ladder — they can only go forward, not back to dangerous ground.
**Example:** Many OpenBSD base utilities call `pledge` shortly after argument parsing; an exploit gaining RCE in `vmd` simply cannot make network calls because the process has already pledged not to.
**Common pitfall / nuance:** Pledge is OpenBSD-specific; Linux equivalents are seccomp-bpf / Landlock / capabilities — same idea, different syntax and weaker default ergonomics.

### Egress filtering (output validation)
**Definition:** Architectural restriction of *outbound* connections from a component — what destinations, what protocols, what TLS configurations, what HTTP methods are permitted.
**Why it matters:** It is the lecture's main worked example of *output validation* and is increasingly required (CRA: a device should not harm its operating networking environment).
**Detailed explanation:** Most controls focus on inputs; egress filtering acknowledges that even with perfect input validation, a compromised component may try to reach a C2 server, exfiltrate data, or pivot. By default-denying outbound and explicitly allow-listing destinations, you bound the *blast radius*.
**Analogy:** A hotel that, after a burglar gets inside, locks the *exits* so the loot cannot leave.
**Example:** GitHub Actions workflows in 2026 moving to egress allow-lists; ChatGPT exfiltration via DNS (The Register, March 2026 article) is exactly the failure mode egress filtering blocks.
**Common pitfall / nuance:** DNS itself can be the exfiltration channel — egress allow-lists must include the *resolver*, not just the destination IPs.

### Agentic AI as a distributed system
**Definition:** Treating multi-agent setups as distributed systems makes all the QAs and tactics of lectures 4-7 directly applicable.
**Why it matters:** It collapses the apparent novelty of "AI architecture" into ground the course has already covered — and surfaces the hard, unsolved problems honestly.
**Detailed explanation:** Open questions: how do peer agents detect a crashed agent and continue (availability/fault detection)? Synchronisation between agents writing/reading shared files (locking, consistency)? CAP theorem under partition (an agent goes offline mid-task — does the team prefer consistency or availability)? Ruohonen flags that these are "still unsolved issues (from a scientific perspective) at the time of lecturing."
**Analogy:** A football team where each player can disappear without warning, every formation requires re-negotiation, and there is no referee — you don't need a new theory of sport, you need to apply the classical theory hard.
**Example:** Case #8 (final assignment): three collaborating agents (bug-finder, fixer, merger) wired faulty over a network, designed to demonstrate at least three security weaknesses + two non-security weaknesses.
**Common pitfall / nuance:** Don't try to invent new vocabulary for agentic systems — apply the existing CAP, availability, recoverability, and consistency tactics first; only then identify what is genuinely novel (e.g., Agent↔Content trust boundary).

## Important diagrams (catalog)

- `page017_safety_scenarios.png` — Safety scenario template (source/event/environment/system/response/measure) adapted from Bass et al. 2021.
- `page018_safety_tactics_tree.png` — Safety tactics tree: Avoidance / Detection / Containment (Redundancy, Limit impact, Barrier) / Recovery.
- `page021_monitor_actuator_pattern.png` — Two variants of the Monitor-Actuator pattern (verify-then-send vs verify-then-abort-on-fault).
- `page022_security_scenarios.png` — Security scenario template with CIA-oriented events and security-specific measures (blast radius, time-to-discover, etc.).
- `page025_security_tactics_tree.png` — Security tactics tree: Detect / Resist / React / Recover with sub-tactics.
- `page028_siem_architecture.png` — Full SIEM architecture (log/normalised/enriched/event/alert brokers, archivers, filters, GUI) as pipe-and-filter.
- `page034_llm_gateway.png` — LLM gateway placement between local-area system and external LLM providers behind firewalls/IDS.
- `page043_input_validation_three_components.png` — Enforcer + Validator + Specification registry input-validation pattern.
- `page058_revoke_access_tactic.png` — Authorisation enforcer + Validator + Specification registry illustrating revoke-access via request limits and event allow-lists.
- `page071_securing_ai_agents.png` — Sierra (2026) principles diagram: human↔agentic-identity binding, scoped tokens, authentication, authorization, mTLS, zero trust, continuous monitoring.
- `page073_cb4a_agent_security.png` — CB4A draft: agent runtime → policy infrastructure (authn/authz/audit + credential & privilege vaults) issuing short-lived scoped tokens.
- `page077_postfix_privilege.png` — Postfix's privilege separation (privileged pickup/queue/local-delivery/external-transport vs ~16 unprivileged worker processes).
- `page079_k8s_privilege_drop.png` — Kubernetes deployment view applying `runAsUser`/`runAsGroup` per pod with mTLS and a message queue.

## Exam-relevant takeaways

1. **Safety vs security**: same tactics often, but the *impact dimension* (damage/injury/loss of life) and the *intentional adversary* distinction are what separate them — be ready to draw both scenario templates and explain the difference.
2. **Memorise the security tactics tree's four branches**: Detect / Resist / React / Recover. Know at least two sub-tactics per branch and be ready to map them to CIA.
3. **SIEM = pipe-and-filter with brokers** (because of many-to-many relations). The bottleneck is the GUI/analyst stage — a performance/usability concern, not a security one.
4. **Input validation principles (Arce et al. 2014)**: centralised validator (well-known libraries), canonicalisation, state-aware inputs, audit nearby code, prefer strongly-typed memory-safe languages — these are exam-quotable.
5. **Prompt injection ≠ SQL injection** — the natural-language input channel has no grammar to sanitise, so architecture (separation of data and control, gateways, validators) is the only defence.
6. **Trust boundaries multiply with agentic AI** — be able to list at least 5 new ones (Agent↔Tool, Agent↔Content, Tool↔Supply-chain, Execution↔Skill, Skill↔Skill, etc.).
7. **Authorisation must NOT depend on the model's interpretation** of a request; it must be enforced by deterministic controls at trust boundaries (Sierra 2026). Quotable.
8. **Privilege drop vs separation**: drop = downgrade after init; separation = fork an unprivileged child for risky work via IPC. Postfix = textbook separation; qmail (1997) = first privilege drop.
9. **Kubernetes `securityContext.runAsUser` / `runAsGroup`** is privilege drop translated into container land — connects lecture 7 to lecture 8.
10. **Egress filtering = output validation** and is also a CRA compliance requirement (a device must not harm its networking environment).
11. **Breakglass mechanisms** (Adkins et al. 2020) are a deliberate exception to least privilege — emergencies trump policy, but the breakglass action must itself be audited.
12. **Always pair revoke-access with non-repudiation** (logs binding actions to identities) — otherwise you can't know who to revoke.

## Cross-references

- **Lecture 2 (QAs)**: Continues the QA-coverage pattern — definition → scenario template → tactics tree → patterns. Builds on the firewall and isolation tactics first mentioned in L2.
- **Lecture 3 (Integrability/Modifiability)**: SIEM brokers and the pipe-and-filter SIEM design are direct uses of L3's mediator/broker patterns. Trust boundaries reuse L3's interface and dependency concepts.
- **Lecture 4 (Testability/Deployability)**: Adkins et al.'s "test of privileges / with privileges" inherits L4's testability tactics; egress filtering and revoke-access tie into deployability and monitoring.
- **Lectures 4–7 (distributed systems / fault tolerance / scalability / Kubernetes)**: The safety tactics tree's *Detection*, *Redundancy*, *Recovery* branches overlap heavily with the availability/fault-tolerance content from L4–L6 (sanity check, comparison, timeout, replication, monitoring, timestamps). The Kubernetes `securityContext` example explicitly extends L7's container/pod content; the multi-agent CAP discussion explicitly references the CAP theorem (lecture 5 or 6 on distributed systems).
- **Mock questions on pages 7–13** revisit Amdahl's law (scalability — earlier lecture), circuit breakers (likely L4 fault tolerance), service discovery (L7 distributed/Kubernetes), DNS MX priority as a pattern (L7), and CAP CP/AP trade-offs (distributed lecture) — useful exam revision spanning the whole course.
- **Lecture 9 (next)**: page 14 announces that cyber security continues into the next lecture — so lecture 9 likely deepens this material rather than pivoting away.
