# 04. Firewalls & IDS — Simulated Open-Book Questions

### [EASY] A junior admin proposes the firewall default policy "that which is not expressly prohibited is permitted." For a new corporate perimeter firewall, is this the right choice? Justify in one or two sentences.
**Answer:** No. That sentence is the **default-allow** policy (L04 p.8), which permits anything you forgot to explicitly block. The secure choice for a perimeter firewall is **default-deny** — "that which is not expressly permitted is prohibited" (L04 p.8) — because any unanticipated or newly-introduced service is then closed by default rather than left open. Concretely, a default-deny ruleset starts by blocking everything, adds explicit `allow` rules only for required services, and ends with an explicit `deny all` catch-all, exactly as in the lecture's ACL (L04 p.14).

### [EASY] You are told a packet filter "does not understand the application-layer protocols." A colleague asks it to block only the HTTP requests for URLs containing `/admin`. Can a static packet filter do this? Why or why not?
**Answer:** No. A static packet filter examines **each IP packet with no context** and decides based only on six factors: arrival interface, source address, destination address, transport protocol (TCP/UDP), source port, and destination port (L04 p.11). A URL path like `/admin` lives in the **application layer (HTTP)**, and the filter explicitly **does not understand application-layer protocols** and **cannot perform checks on higher-level protocols** (L04 p.10, p.16). It could block port 80 wholesale, but it cannot distinguish one URL from another. URL filtering requires an **application-level gateway (proxy)**, which provides URL filtering (L04 p.27).

### [EASY] A manager says "our firewall will protect us from all attacks." Give two concrete attack paths from the lecture that the firewall cannot stop, and the one-line reason both succeed.
**Answer:** Two paths the firewall **cannot** protect against (L04 p.6):

1. **Sneaker net / malware on a laptop or USB storage** — data or malware physically carried in or out, infected outside the protected network.
2. **Internal threats** — a disgruntled or colluding employee already inside the network.

The one-line reason both succeed: a firewall only controls **traffic that actually passes through it** (it is a single choke point, L04 p.2). Anything that arrives by another path (sneaker net, an insecure WLAN, or an encrypted SSL/SSH tunnel it cannot inspect) or originates **inside** the network never crosses the choke point and is therefore outside its control.

### [EASY] In the lecture's ACL format, what does the value `>1023` in the source-port field represent, and why does it appear there rather than a fixed number like 80?
**Answer:** `>1023` represents the **ephemeral (client-side) port range** (L04 p.14, and the Gotchas note). Well-known services use fixed ports in the range 0–1023 (e.g., **80** for HTTP, **53** for DNS), but the *client* end of a connection picks a temporary high-numbered port above 1023 for each new session. So in a rule allowing internal users to reach an external web server, the **destination port is the fixed service port (80)** and the **source port is the variable client port (`>1023`)**. On the matching return rule the two swap: source port 80, destination `>1023` (L04 p.14).

### [EASY] Classify each as detect-only or acts-automatically: (a) a passive IDS, (b) an IPS. Give one example action only one of them can take.
**Answer:**

- **(a) Passive IDS — detect-only.** It filters information and extracts relevant events, acting as a "source of distilled information." It **detects and reports**; it does not act (L04 p.41).
- **(b) IPS (reactive system) — acts automatically.** It is designed to **take action** (L04 p.41).

An example action **only the IPS** can take: **changing the firewall rules** to block the attacker (others listed are blocking users and changing network connectivity, L04 p.41). A plain passive IDS would merely raise an alert about the same traffic.

### [MEDIUM] An office wants internal hosts on `10.0.0.0/8` to browse external websites (HTTP), but the firewall is a *static* packet filter. The admin writes only one rule: `allow | 10.0.0.0/8 | outside | TCP | >1023 | 80`. Users report pages never load. Diagnose and fix.
**Answer:** **Diagnosis:** The outbound request leaves fine, but the **return traffic is dropped**. A static packet filter examines each packet with **no context** and has **no session memory**, so it cannot recognise that an inbound packet from the web server belongs to a request it already allowed (L04 p.8, p.14). With a default-deny catch-all, the reply (source port 80 → some ephemeral destination port) matches no allow rule and is denied.

**Fix:** Add the explicit **matching return rule**, then keep the default-deny last:

```
allow | 10.0.0.0/8 | outside       | TCP | >1023 | 80
allow | outside     | 10.0.0.0/8    | TCP | 80    | >1023
deny  | all         | all           | all | all   | all
```

A **stateful** filter would not need the second rule, because it tracks the client–server session in a state table and matches the return packet automatically (L04 p.18). This is the canonical "static needs two rules, stateful needs one" point (L04 p.14, p.18).

### [MEDIUM] Translate this plain-English policy into a single firewall setting in the lecture's style, and name the specific attack it defends against: "Our network must never be usable as an amplifier for a flooding attack against a third party."
**Answer:** The policy maps to the **Smurf DoS** defence (L04 p.13). In a Smurf attack, an attacker pings a network's **broadcast address** with a spoofed source set to the victim, and every host replies to the victim, amplifying the flood.

**Firewall setting (lecture style):**

> **Drop all ICMP packets going to a "broadcast" address** (e.g., `222.22.255.255`).

Illustrative standard syntax (not from the slides) for a `/16` broadcast:

```bash
iptables -A FORWARD -p icmp -d 222.22.255.255 -j DROP
```

The specific attack defended against is the **Smurf denial-of-service attack** (L04 p.13). Note this differs from "prevent being tracerouted," which instead drops **all outgoing ICMP** (L04 p.13).

### [MEDIUM] A startup runs a public web server and wants *external* users to reach only that one server (at 222.22.44.203:80) for new connections, while internal users may still initiate connections out freely. Express the inbound rule the lecture would use, and explain the role of the TCP SYN flag in it.
**Answer:** The lecture's mapping for "external connections to public Web server only" is (L04 p.13):

> **Drop all incoming TCP SYN packets to any IP except 222.22.44.203, port 80.**

**Role of the SYN flag:** A TCP connection begins with a packet whose **SYN** flag is set — this is the *connection-initiation* packet. By dropping **incoming SYNs** to every destination *except* the public web server, the firewall blocks anyone outside from **starting a new connection** to internal hosts, while still allowing packets that belong to connections **initiated from the inside** (whose inbound packets are not lone SYNs but ACKs/data of an already-established flow). So internal users keep full outbound freedom, and the only inbound connection the world can open is HTTP to 222.22.44.203 (L04 p.13).

### [MEDIUM] For each of these two situations pick misuse (signature) detection or anomaly detection, and state the weakness you are accepting: (a) a bank that must catch brand-new, never-seen malware fast; (b) a SOC that is drowning in alerts and only has signatures for known exploits.
**Answer:** Using the trade-off from L04 p.40:

- **(a) Bank, must catch novel malware → anomaly detection.** Anomaly detection learns normal patterns (a classical ML task) and flags **deviations**, so it can catch attacks that have **no signature yet**. The weakness accepted: it is **susceptible to false positives** — legitimate-but-unusual activity (e.g., a big quarter-end data export) can look like an attack.
- **(b) Alert-fatigued SOC, only known exploits → misuse (signature) detection.** Signatures match **known attack patterns** reliably and with **fewer false alarms**. The weakness accepted: it is **susceptible to unknown attacks** (false negatives on anything novel), because a brand-new attack has no signature yet (L04 p.40).

In practice the lecture notes you would combine both, since the categories overlap (L04 p.39).

### [MEDIUM] A company puts a circuit-level gateway between trusted internal users and the Internet for general outbound browsing. The security team complains it "lets data through without reading it." Is that a misconfiguration or expected behaviour, and what does the gateway actually validate?
**Answer:** It is **expected behaviour**, not a misconfiguration. A circuit-level gateway **validates the TCP/UDP session before opening the circuit**, then, once the connection is established, **relays traffic without examining its contents** (L04 p.20–21). It is precisely intended for **trusted internal users** making general outbound connections (L04 p.21).

What it *does* validate/track per connection (L04 p.23): a unique **session identifier**, the **connection state** (handshake/established/closing), **sequencing information**, **source IP**, **destination IP**, and the **inbound and outbound physical interfaces**. So its security comes from **limiting which sessions may be set up** and from shielding internal IPs via NAT (L04 p.24) — not from inspecting payloads. If the team needs content inspection (e.g., URL filtering, blocking specific application data), they need an **application-level proxy** instead (L04 p.25–27).

### [HARD] Critique and correct this proposed ACL (static filter, applied top-to-bottom, first match wins) intended to let internal `222.22/16` do web + DNS with default-deny. Identify every defect.
```
1. deny  | all         | all          | all | all   | all
2. allow | 222.22/16   | outside      | TCP | >1023 | 80
3. allow | outside     | 222.22/16    | TCP | >1023 | 80
4. allow | 222.22/16   | outside      | UDP | >1023 | 53
```
**Answer:** Three distinct defects:

1. **The `deny all` is at the top (row 1).** ACLs apply **top to bottom, first match wins** (L04 p.14). A `deny all` in row 1 matches **every** packet, so rows 2–4 are dead code and *all* traffic is blocked. The catch-all `deny all` must be the **last** row.
2. **Row 3's ports are wrong (swapped).** The HTTP **return** rule must have **source port 80** (the server) and **destination `>1023`** (the client's ephemeral port). As written (`source >1023 → dest 80`) it is a *second outbound* rule, not the reply rule, so web replies are still dropped (L04 p.14, Gotchas: "don't swap source/dest ports between request and reply").
3. **The DNS return rule is missing.** Static filters have **no session memory**, so an outbound rule alone is not enough; you need `allow | outside | 222.22/16 | UDP | 53 | >1023` for replies (L04 p.14, p.18).

**Corrected ACL:**

```
allow | 222.22/16 | outside    | TCP | >1023 | 80
allow | outside   | 222.22/16  | TCP | 80    | >1023
allow | 222.22/16 | outside    | UDP | >1023 | 53
allow | outside   | 222.22/16  | UDP | 53    | >1023
deny  | all       | all        | all | all   | all
```

This is exactly the lecture's reference ACL (L04 p.14).

### [HARD] You must place a public web server, an internal database, and a bastion host on a network protected by a firewall. The web server must be reachable from the Internet; the database must never be. Explain how you would partition trust, where the bastion host sits, and why exposing the web server directly on the internal LAN is dangerous. Note any limits of grounding from the lecture.
**Answer:** **Trust partitioning principle.** A firewall interconnects **networks of differing trust** and is a single choke point that allows only authorized traffic (L04 p.2–3). The Internet is untrusted, the internal LAN (with the database) is the most trusted, and the public web server is in between — it must accept anonymous inbound connections, so it cannot be treated as fully trusted.

**Placement reasoning.** The web server and the **bastion host** belong on a separate, semi-trusted segment, isolated from the internal LAN. The bastion host is a **hardened, highly secure host** running circuit/application-level gateways or externally accessible services, deliberately **exposed to hostile elements** and secured to withstand them (hardened OS, only essential services, extra authentication, small non-privileged proxies) (L04 p.30). If it bridges two or more connections it can be **trusted to enforce separation** between them (L04 p.30). The **database stays on the internal LAN** with no inbound path from the Internet — the firewall drops external SYNs to it (cf. "public web server only," L04 p.13).

**Why direct LAN exposure is dangerous.** A public web server is the most likely thing to be compromised (it accepts attacker traffic). If it sits on the internal LAN, a successful exploit gives the attacker a foothold **inside the trusted zone**, next to the database — the firewall can no longer help because the threat is now **internal** (a blind spot, L04 p.6). Isolating it limits the blast radius.

**Grounding limit:** the lecture's **DMZ** slide (p.33) is **image-only** with no extractable detail (L04 p.33, Gotchas). The standard name for this isolated semi-trusted segment is a **DMZ**, but the specifics beyond the bastion-host text must come from the original diagram, not invented.

### [HARD] An IDS team enables aggressive *preemptive blocking* ("banishment vigilance"): any IP that triggers a suspicious signature is auto-blocked at the firewall. Within a day, legitimate customers are locked out. Explain the failure in IDS/IPS terms, classify what they really built, and propose a safer design.
**Answer:** **The failure.** Preemptive blocking seeks to **prevent intrusions before they occur** by noting signs of an impending threat and **blocking the user or IP** (L04 p.43). Its named risk is exactly what happened: blocking **legitimate users**, producing a **self-inflicted denial of service** (L04 p.43). Because the trigger was a **signature**, any **false positive** (legitimate traffic that resembles an attack) becomes an automatic lockout.

**What they really built.** This is not a passive IDS — it **takes action** (changes firewall rules / blocks users), so by definition it is a **reactive system, an IPS** (L04 p.41), operating in the most aggressive **preemptive-blocking** mode (L04 p.43).

**Safer design.**

1. **Tune detection to cut false positives** — combine signature (misuse) detection with anomaly baselining and require higher confidence before acting, since misuse detection alone still misfires on look-alike traffic (L04 p.40).
2. **Demote most responses to passive** — let the IDS **detect/report** (distilled information, L04 p.41) and have a human confirm before a block, reserving automatic blocking for very high-confidence events.
3. **Add safeguards** — allowlist known-good customer ranges, use rate-limited or **temporary** blocks, so a false positive degrades rather than permanently denies service.
4. Optionally add an **intrusion-deflection honeypot** (L04 p.44) to study suspicious actors without blocking real users.

### [HARD] A network defender wants to (a) catch novel attacks, (b) study attacker techniques safely, and (c) keep alert volume manageable. Design a layered detection strategy mapping each goal to a specific mechanism from the lecture, and explain one tension between two of your choices.
**Answer:** Mapping each goal to a lecture mechanism:

- **(a) Catch novel attacks → anomaly detection.** It learns normal patterns and flags deviations, so it can detect attacks with **no existing signature** (L04 p.40). Pair it with **misuse/signature detection** for known attacks (categories overlap, L04 p.39).
- **(b) Study attacker techniques safely → intrusion deflection via a honeypot.** A honeypot is an attractive system with **fake-but-realistic** data/services that **lures the attacker in, monitors activity, learns about new attacks, and collects forensic information** (L04 p.44) — all without risking production systems.
- **(c) Keep alert volume manageable → a passive IDS posture.** A passive system **filters information and extracts relevant events**, acting as a **source of distilled information** rather than firing on everything (L04 p.41); reserve reactive/IPS blocking for high-confidence cases to avoid alert and self-DoS problems (L04 p.43).

**A tension:** goals (a) and (c) pull against each other. **Anomaly detection is susceptible to false positives** (L04 p.40), which **increases** alert volume — directly working against the "manageable alerts" goal. Resolving it requires careful baselining and triage (e.g., feeding anomaly hits through the passive distillation layer and correlating with signatures) so novel-attack coverage does not bury the SOC in noise.

### [HARD] Two firewall options are on the table for a perimeter that must enforce per-application rules (e.g., allow HTTP but block FTP) and authenticate users: a stateful packet filter and an application-level proxy. Compare them on capability, speed, and operational cost, and recommend one with justification.
**Answer:** **Capability.** The requirement is **per-application control and user authentication**. A stateful filter operates at OSI layer 2/3, tracks sessions, and offers **less access control** than a proxy (L04 p.19) — it can match ports but does not natively understand HTTP vs FTP semantics or authenticate users. An **application-level proxy** evaluates packets for **valid data at the application layer**, **understands high-level protocols like HTTP and FTP**, can **deny some services while allowing others**, and provides **user authentication** (plus HTTP caching, URL filtering) (L04 p.26–27). Only the proxy meets the stated requirements.

**Speed.** The stateful filter is **faster** (lower in the stack, application-independent) (L04 p.19). The proxy is **slow** because it must replace the native network stack and fully parse application protocols (L04 p.28).

**Operational cost.** The proxy is more expensive to run: it **requires replacing the native network stack**, **needs modifications to client procedures**, and **relies on OS support so it inherits OS bugs** (L04 p.28). The stateful filter needs no special client configuration.

**Recommendation: the application-level proxy.** Because the explicit requirements — **distinguish HTTP from FTP** and **authenticate users** — are application-layer functions a stateful filter cannot perform (L04 p.19, p.26–27), the proxy is the only option that satisfies them. Accept the slower throughput and higher operational cost as the price of application-level control. (A common real deployment uses a fast stateful filter at the edge *plus* a proxy for the protocols needing deep control, exploiting the strengths of each.)

### [VERY HARD] An auditor finds that an organisation's "fully firewalled" network was breached even though the perimeter firewall logs show no malicious inbound connections. Walk through at least three lecture-grounded mechanisms by which this is entirely possible, and explain why "no malicious inbound traffic in the firewall logs" is weak evidence of safety.
**Answer:** A clean perimeter log only proves nothing malicious **crossed the choke point** — it says nothing about paths that bypass it or threats originating inside. At least three lecture-grounded mechanisms (all L04 p.6):

1. **Bypass via an alternate path.** Data/malware entered by **sneaker net** (USB/laptop carried in from outside) or via an **improperly secured WLAN**, never traversing the firewall. The perimeter log is silent because the traffic never reached it.
2. **Encrypted trusted services the firewall cannot inspect.** Traffic over **SSL/SSH tunnels** is explicitly a firewall blind spot — the firewall may allow the tunnel as a "trusted service" but **cannot see inside it**, so a malicious payload inside an allowed encrypted session appears as ordinary, benign permitted traffic in the logs.
3. **Internal threat.** A **disgruntled or colluding employee** already inside the trusted zone acts entirely behind the firewall; their activity never appears as an inbound perimeter connection at all.

**Why the evidence is weak.** The firewall is a **single choke point** that controls only the traffic passing **through** it (L04 p.2). "No malicious inbound connections logged" therefore covers only one of several attack surfaces. It cannot speak to bypass paths, encrypted-tunnel contents, malware imported on devices, or insider action. This is precisely why the lecture pairs firewalls with **IDS/host monitoring** (HIDS/NIDS/LIDS, L04 p.39) and incident response — defence in depth, not a single perimeter.

### [VERY HARD] Reason about false positives vs false negatives for a NIDS guarding a hospital. (a) Which error type is more dangerous if the NIDS is wired to an IPS that auto-blocks? (b) How does the misuse-vs-anomaly choice shift the balance of the two error types? (c) Propose a concrete configuration that hedges both, and name a residual risk.
**Answer:** **(a) With an auto-blocking IPS, false positives are the acute danger.** A false positive on a hospital network that is wired to a reactive IPS causes the IPS to **change firewall rules / block users / change connectivity** (L04 p.41) against legitimate clinical traffic — a **self-inflicted denial of service** (L04 p.43). In a hospital, cutting off access to patient records or devices is potentially life-threatening, so the cost of a false positive can exceed that of a single missed alert. (False negatives remain serious, but they do not, by themselves, take down clinical systems.)

**(b) The detection choice shifts the error mix (L04 p.40):**

- **Misuse/signature detection → more false negatives.** It is **susceptible to unknown attacks**; a novel attack has no signature and slips through. Its false-positive rate on look-alike traffic is comparatively low.
- **Anomaly detection → more false positives.** It is **susceptible to false positives**; unusual-but-legitimate clinical activity (a new device, a batch export) deviates from the learned baseline and trips an alarm.

So choosing anomaly detection buys novel-attack coverage at the price of *more* of the very error type that is most dangerous under auto-blocking.

**(c) A hedging configuration:**

1. Run **both** detection methods (the categories overlap — L04 p.39): signatures for reliable known-attack catches, anomaly detection for novel ones.
2. Make the IDS mostly **passive** — detect/report distilled information for human triage (L04 p.41) — and let the **IPS auto-block only on high-confidence signature hits**, not on anomaly scores alone.
3. **Allowlist** critical clinical systems and use **temporary/rate-limited** blocks so any mistaken block degrades rather than severs access (mitigating the preemptive-blocking self-DoS risk, L04 p.43).

**Residual risk:** the gap between "anomaly flags it" and "signature confirms it" is exactly where a **novel attack** lives — by demoting anomaly hits to human review you reintroduce **false-negative exposure** (delayed response to a genuine zero-day) as the price of protecting availability.

### [VERY HARD] A team claims they can replace their perimeter firewall entirely with host-based firewalls on every server plus a honeypot. Evaluate this architecture: what does it gain, what does it lose versus a perimeter firewall, and is the honeypot a substitute for either? Ground each point in the lecture.
**Answer:** **What host-based firewalls gain (L04 p.31).** A host-based firewall is a software module securing an **individual host**, with three lecture-stated advantages: rules can be **tailored to that host's environment**, protection is **independent of network topology**, and it provides an **additional layer of protection**. Distributing them means a compromise of one segment does not automatically expose every host, and policy travels with the host — useful for the firewall's known blind spot where threats are **already inside** (L04 p.6).

**What is lost versus a perimeter firewall.**

1. **No single choke point.** The perimeter firewall's core value is being **one controlled point of monitoring and access control** between networks of differing trust (L04 p.2–3). Spreading enforcement across every host removes the central vantage point for **auditing, alarms, NAT, and usage monitoring** (L04 p.2) and multiplies the places a misconfiguration can occur.
2. **Each host is now directly exposed.** Without a perimeter, external traffic reaches each host's stack directly; the protection now depends on every host being configured and patched correctly — a much larger, error-prone attack surface than hardening a single bastion/perimeter (L04 p.30).
3. **Personal/host firewalls are typically less capable.** Host and personal firewalls are described as comparatively **less complex** modules focused on denying unauthorized remote access and watching outbound activity (L04 p.31–32) — not a full replacement for, say, an application-level proxy's protocol-aware control (L04 p.26–27).

**Is the honeypot a substitute?** No. A honeypot is an **intrusion-deflection** tool — a fake-but-realistic system that **lures attackers, monitors them, learns new attacks, and gathers forensics** (L04 p.44). It is a **detection/intelligence** mechanism, not an access-control enforcement point: it neither filters production traffic nor authenticates users, so it cannot replace a firewall (perimeter or host) or an IDS/IPS. It complements them by diverting and studying attackers.

**Verdict.** Host-based firewalls are a valid **defence-in-depth layer** and partly address the internal-threat blind spot, but removing the perimeter sacrifices the central choke point, monitoring, and protocol-aware control, while the honeypot adds visibility but enforces nothing. The lecture's framing favours **layering** (perimeter + host-based + IDS/IPS + honeypot), not substitution (L04 p.2–3, p.31, p.44).

### [VERY HARD] Forensics-vs-restore tension: a production server has been compromised and is actively serving customers. Using the lecture's incident-response model, lay out the immediate response steps, then explain the conflict between forensics and restoring operations and how you would decide.
**Answer:** **Immediate incident response (L04 p.49)** — work through the four steps in order:

1. **Verification** — confirm the alert is real (is the information correct?), not a false positive, before tearing anything down.
2. **Interpretation** — determine **what actually happened**: which host, which service, what the attacker did.
3. **Scope of incident** — assess actual and possible **consequences**: is it one server or has it spread, what data is exposed?
4. **Classification & prioritisation** — decide **how urgently you must act** (e.g., is this spam, a scan, or a fully compromised system?). A confirmed compromise of a live customer-facing server is high priority.

**Next steps and the conflict (L04 p.50).** The two follow-on aims are **Forensics** (research what went wrong; **secure the evidence** — how and when) and **Restore operations** (rebuild systems by priority, from backups, with a plan to get back online). The lecture states these **can counteract each other**: **rebuilding or wiping the server to restore service destroys the very evidence** forensics needs (memory state, attacker artefacts, logs). You also owe **communication** internally and to business partners/customers.

**How to decide.** Resolve the tension by **preserving before restoring**:

1. First **capture evidence** — image the disk and memory and copy logs to a secure store — so forensics is not foreclosed.
2. Then **restore from clean backups onto separate hardware/VM** to bring customers back online, rather than rebuilding in place over the evidence.
3. Let **scope and priority (step 3–4)** set the balance: if customer-facing availability is critical and the breach is contained, lean toward fast restore *after* a quick forensic snapshot; if the incident is severe or legally sensitive, weight forensics more heavily and accept longer downtime. Throughout, keep stakeholders informed (communication). This sequencing satisfies both aims instead of sacrificing one — the explicit goal given the warning that they counteract each other (L04 p.50).

### [VERY HARD] An attacker defeats a static packet filter using a tiny fragment attack, and separately a second attacker spoofs an internal source address to slip past it. Explain why a *static* filter is vulnerable to each, what countermeasures the lecture gives, and why upgrading to a *stateful* filter helps in one case more than the other.
**Answer:** Both attacks exploit the same root weakness: a static packet filter examines **each IP packet with no context** (L04 p.8) and makes its decision from a fixed set of header fields with no session memory (L04 p.11).

**Tiny fragment attack.** The attacker **splits the header information over several tiny packets** so the filter never sees the full transport header (e.g., the port/flags) in any single fragment and therefore cannot match its rules correctly (L04 p.17). **Lecture countermeasure:** either **discard such fragments** or **reassemble the packet before checking** it (L04 p.17).

**IP spoofing.** The attacker **fakes a source address to appear trusted** — e.g., forges an internal source IP on packets arriving from outside — and the static filter, trusting the address field at face value, lets it through (L04 p.17). **Lecture countermeasure:** add **filters on the router to block** spoofed packets, e.g. drop inbound packets that claim an internal source address (L04 p.17).

**Where a stateful upgrade helps more.** A **stateful** filter tracks **client–server sessions** in a state table and verifies that each packet **validly belongs to one**, detecting **bogus packets out of context** (L04 p.18–19). This **directly defeats spoofing of unsolicited inbound packets**: a forged "internal" packet that matches no established outbound session is out of context and dropped — the stateful engine's core strength. The **tiny fragment attack benefits less**: statefulness is about session validity, not header reassembly, so the filter must still **reassemble or discard fragments** to inspect them properly (L04 p.17). In short, statefulness substantially closes the **spoofing/out-of-context** gap but does **not** by itself solve fragmentation — that still needs explicit fragment handling. (Note also that statefulness adds context, but neither static nor stateful filters inspect **application-layer** content; that remains a proxy's job — L04 p.19, p.26.)
