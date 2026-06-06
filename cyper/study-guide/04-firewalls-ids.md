# 04. Firewalls and IDS

> Source grounding: This guide is built **only** from the lecture slides `L04_Firewalls_and_IDS.pdf` (50 pages, cited as `L04 p.N`) and the exercise sheet `E04.pdf` (1 page, cited as `E04 p.1`). Where the slides are thin or a slide is image-only (no extractable text), this is flagged explicitly so you do not rely on invented detail.

---

## Overview — what this topic covers and why it matters

This topic covers the two main pillars of **network perimeter and monitoring defense**: **firewalls** (which control *what traffic is allowed* between networks of differing trust) and **Intrusion Detection / Prevention Systems** (which monitor activity to *spot and react to* malicious behavior). A firewall is described in the lecture as "a choke point of control and monitoring" that "interconnects networks with differing trust" and "imposes restrictions on network services" so that "only authorized traffic is allowed" (L04 p.2). It is "a single point of defense between two networks" and can be hardware, software, or both, enforcing access control and allowing/denying traffic to and from a network (L04 p.3). The lecture builds up the family of firewall types by the OSI layer at which they operate, then moves to *where* firewalls are placed (bastion host, host-based, personal, DMZ, VPN, distributed), and finally to IDS/IPS and incident response.

This matters because firewalls and IDS together provide the first line of defense for the **integrity and confidentiality of information in the internal network** (L04 p.3), but each has hard limits: a firewall "cannot protect from attacks bypassing it" and "cannot protect against internal threats" (L04 p.6), and an IDS only *detects* unless paired with a reactive IPS. For the exam, expect to (1) distinguish firewall types and their layer/advantages/disadvantages, (2) read and write packet-filter rules / access control lists, (3) distinguish misuse vs. anomaly detection and passive vs. reactive systems, and (4) reason about IDS approaches (preemptive blocking, deflection/honeypot, deterrence) and incident response. The accompanying exercise (E04) also pivots to a hands-on **password-cracking task** (cracking a bcrypt hash with `rockyou.txt` using Hashcat or John the Ripper), which is included in the cookbook below since it is part of this week's deliverable (E04 p.1).

---

## Key Concepts

### What a firewall is and what it does

A firewall is a **choke point of control and monitoring** that interconnects networks of differing trust and imposes restrictions on network services so that only authorized traffic is allowed; it performs auditing and access control, can implement alarms for abnormal behavior, provides NAT and usage monitoring, can implement VPNs using IPSec, and must itself be **immune to penetration** (L04 p.2). Put plainly, it is "a single point of defense between two networks," realized in hardware and/or software, that protects the resources of a private network from users on other networks, enforces access control between the two networks, and allows or denies traffic to/from the network — making it essential for the **integrity and confidentiality** of internal information (L04 p.3). A firewall can act as a **gateway** and as a **proxy**, and it filters both incoming and outgoing information (L04 p.3). Typical users are organizations, universities, and companies (L04 p.3).

The four stated **main purposes** of a firewall are: **packet filtering**, **analyzing packets**, **proxy service**, and **providing access to other networks** (e.g., the Internet) (L04 p.4).

### Firewall limitations (what a firewall cannot do)

A firewall is not a complete defense. The lecture lists what it **cannot** protect against (L04 p.6):
- Attacks that **bypass** it — e.g., "sneaker net" (physically carrying data), utility modems, trusted organizations, and trusted services such as SSL/SSH (encrypted tunnels the firewall can't inspect).
- **Internal threats** — e.g., disgruntled or colluding employees.
- Access via **WLAN** if it is improperly secured against external use.
- **Malware imported via laptop, PDA, or storage** that was infected outside the protected network.

Why this matters: the firewall only controls the traffic that actually passes through it. Anything that arrives by another path, or originates inside, is outside its control.

### Classifying firewalls by OSI layer

Firewalls are categorized by the **OSI model level at which they operate**. The lecture names **three basic types** (L04 p.7):
- **Network level** — Packet filters.
- **Application level** — Proxy server.
- **Circuit level** — Proxy server.

(Note: the slides also separately discuss **stateful packet** firewalls (L04 p.18–19) as an evolution of packet filters, and "basing" categories — bastion, host, personal (L04 p.30–32, p.36). So the full taxonomy you should be ready to list is: packet-filter (static), stateful inspection, circuit-level, application proxy.)

### Packet-filter firewalls (network level)

This is the **simplest, fastest** firewall component and the **foundation of any firewall system**. It examines **each IP packet with no context** and permits or denies it according to rules, thereby restricting access to services (ports) (L04 p.8). It operates at the **network level** of the OSI model, filtering each incoming packet to decide whether to pass it through (L04 p.9). Packet-filter firewalls use one of two filtering approaches (L04 p.9):
- **Static packet filtering.**
- **Dynamic packet filtering / Stateful inspection.**

**Default policies** — two possible defaults (L04 p.8):
- "That which is **not expressly permitted is prohibited**" (default-deny / whitelist — the secure choice).
- "That which is **not expressly prohibited is permitted**" (default-allow / blacklist).

### Static packet filtering

A static packet filter is one of the **foremost (first-generation)** firewall technologies. It filters incoming and outgoing packets to deny or authorize access based on **rules defined by the administrator**, and those rules are **non-dynamic (static — they do not change)**. Critically, static packet filters **do not understand the application-layer protocols** in the packets (L04 p.10).

The **factors** that allow or deny data flow through a packet filter are (L04 p.11):
1. The **physical network interface** the packet arrives on.
2. The **source address** (where the data is coming from).
3. The **destination address** (where the data is going to).
4. The **transport-layer protocol type** — TCP or UDP.
5. The **transport-layer source port**.
6. The **transport-layer destination port**.

**Advantages** of static packet filtering (L04 p.16):
- Generally **faster** than other firewalls because they perform fewer evaluations.
- **Less complicated** — a single rule controls deny/allow.
- Can provide **NAT** (Network Address Translation).
- **Least expensive.**
- Do **not require client computers to be configured specially.**

**Disadvantages** (L04 p.16):
- **Limited capabilities** — typically only source & destination.
- Cannot address protocol subsets other than IP — most TCP.
- **Cannot perform checks on higher-level protocols.**

### Filtering rules and Access Control Lists (ACLs)

The lecture gives concrete **policy → firewall setting** mappings (L04 p.13):

| Policy | Firewall setting |
|---|---|
| No outside Web access | Drop all **outgoing** packets to any IP address, **port 80** |
| External connections to public Web server only | Drop all **incoming TCP SYN** packets to any IP **except 222.22.44.203, port 80** |
| Prevent IPTV from eating available bandwidth | Drop all **incoming UDP** packets **except DNS and router broadcasts** |
| Prevent your network from being used for a **Smurf DoS** attack | Drop all **ICMP** packets going to a "broadcast" address (e.g., 222.22.255.255) |
| Prevent your network from being **tracerouted** | Drop all **outgoing ICMP** |

The same logic is expressed as an **Access Control List**, applied **from top to bottom** (first match wins). Example ACL (L04 p.14):

| action | source address | dest address | protocol | source port | dest port |
|---|---|---|---|---|---|
| allow | 222.22/16 | outside of 222.22/16 | TCP | > 1023 | 80 |
| allow | outside of 222.22/16 | 222.22/16 | TCP | 80 | > 1023 |
| allow | 222.22/16 | outside of 222.22/16 | UDP | > 1023 | 53 |
| allow | outside of 222.22/16 | 222.22/16 | UDP | 53 | > 1023 |
| deny | all | all | all | all | all |

Reading this ACL: rows 1–2 permit internal hosts (the `222.22/16` network) to make **outbound HTTP** (web) requests and receive the replies — outbound to dest port 80 from an ephemeral source port `>1023`, and the matching return traffic from source port 80 back to an ephemeral port. Rows 3–4 do the same for **DNS** (UDP port 53). The final **deny all** is the explicit **default-deny** catch-all. The `>1023` reflects that client-side ephemeral ports are above the well-known port range (0–1023).

### Attacks on packet filters

Static packet filters are vulnerable to several attacks (L04 p.17):
- **IP address spoofing** — faking a source address to appear trusted; *countermeasure:* add filters on the router to block (e.g., drop inbound packets claiming an internal source).
- **Source routing attacks** — the attacker specifies a route other than the default; *countermeasure:* block source-routed packets.
- **Tiny fragment attacks** — splitting header information over several tiny packets so a filter can't see the full header; *countermeasure:* either discard such fragments or reassemble before checking.

### Stateful packet filters (stateful inspection)

Traditional packet filters do **not examine higher-layer context** — in particular, they don't match return packets with the outgoing flow. **Stateful packet filters** address this: they examine each IP packet **in context**, keep track of **client–server sessions**, and check that each packet **validly belongs to one**. This makes them better at detecting **bogus packets out of context**, and they may even inspect **limited application data** (L04 p.18).

Architecture: a stateful firewall uses an **INSPECT engine** and **state tables** to track connections (L04 p.19).

**Advantages** (L04 p.19):
- Operates at the **2nd/3rd layer** in the OSI stack — **faster than an application proxy**.
- **Application independent.**

**Disadvantages** (L04 p.19):
- **Less access control** than an application proxy.

### Circuit-level gateway

Circuit-level firewalls are **3rd-generation** firewalls. They are similar in operation to packet-filtering firewalls, but the **key difference** is that a circuit-level firewall **validates TCP and UDP sessions before opening a connection (circuit)** through the firewall. When a session is established, the firewall maintains a **table of valid connections** and lets data pass when session info matches a table entry; the entry is removed and the circuit closed when the session terminates (L04 p.20).

Operationally, a circuit-level gateway (L04 p.21):
- **Relays two TCP connections.**
- Imposes security by **limiting which connections are allowed**.
- Once created, usually **relays traffic without examining contents.**
- Is typically used for **trusted internal users**, allowing general outbound connections.
- **SOCKS** is commonly used.

When a connection is set up, the circuit-level firewall stores (L04 p.23):
1. A unique **session identifier**.
2. The **state of the connection** (handshake, established, closing).
3. The **sequencing information.**
4. The **source IP address.**
5. The **destination IP address.**
6. The **physical network interface through which the data arrives.**
7. The **physical network interface through which the data goes out.**

**Advantages** (L04 p.24):
1. Faster than application-layer firewalls.
2. More secure than packet-filter firewalls.
3. Protect against **spoofing** of packets.
4. Shield internal IP addresses from external networks via **NAT**.

**Disadvantages** (L04 p.24):
1. Cannot restrict access to protocol subsets other than **TCP**.
2. Cannot perform security checks on **higher-level protocols**.

### Application-level gateway (proxy)

An application-level gateway has an **application-specific gateway/proxy** with **full access to the protocol**. The flow is: the **user requests a service from the proxy → the proxy validates the request as legal → the proxy actions the request and returns the result to the user**. It can **log/audit traffic at the application level** (L04 p.25).

As an **application-level firewall** (third-generation technology), it evaluates network packets for **valid data at the application layer before allowing a connection**. It maintains a **complete list of connection states and sequencing information**, and validates security items that appear **only in application-layer protocols**, such as **user passwords and service requests**. It uses **special-purpose programs as proxies** to manage data transfer for specific services such as **FTP and HTTP** (L04 p.26).

**Advantages** (L04 p.27):
- Understand **high-level protocols** like HTTP and FTP.
- Can **deny access to certain network services while allowing others.**
- Do **not allow direct communication** between external servers and internal systems → shield internal IP addresses.
- Provide features like **HTTP caching, URL filtering, and user authentication.**

**Disadvantages** (L04 p.28):
- Require **replacing the native network stack** on the firewall server.
- They are **slow.**
- Proxy services **require modifications to client procedures.**
- They **rely on OS support** and are therefore **vulnerable to bugs in the system.**

### Firewall basing — where the firewall lives

**Bastion host** (L04 p.30): a **highly secure host system** with a special entrance for admin. It runs circuit/application-level gateways or provides externally accessible services, is potentially exposed to "hostile" elements, and is therefore secured to withstand this — **hardened OS, only essential services, extra authentication**. Its **proxies are small, secure, independent, and non-privileged**. It may support 2+ network connections and may be **trusted to enforce a policy of trusted separation** between those connections.

**Host-based firewall** (L04 p.31): a **software module used to secure an individual host**, available in many OSes or as an add-on package, often used on servers. Advantages: can **tailor filtering rules to the host environment**, protection is **independent of topology**, and it provides an **additional layer of protection**.

**Personal firewall** (L04 p.32): controls traffic between a **PC/workstation and the Internet or enterprise network**. It is a software module on the personal computer or in a home/office DSL/cable/ISP router, **typically much less complex** than other firewall types. Its primary role is to **deny unauthorized remote access** to the computer and to **monitor outgoing activity for malware**.

### Firewall location and configurations: DMZ, VPN, distributed

The summary slide lists "location and configurations: **DMZ, VPN, distributed, topologies**" (L04 p.36). However, the dedicated slides **"DMZ Networks" (L04 p.33), "Virtual Private Networks" (L04 p.34), and "Distributed Firewalls" (L04 p.35)** contain **only the title text in the extractable content** — the substance is in diagrams/images that did not produce text. From the rest of the lecture we can ground the following minimal definitions:
- **VPN:** the firewall can "implement VPNs using IPSec" (L04 p.2) — i.e., create encrypted tunnels between networks/hosts over an untrusted network.
- **DMZ / VPN / Distributed firewall:** beyond the names and the VPN/IPSec point, the lecture's specific definitions for DMZ and distributed firewalls are **not present in the extractable text** (slides p.33–35 are image-only). *Treat these as needing the original diagrams; do not invent specifics.*

### Intrusion Detection Systems (IDS) — overview

An IDS **monitors network/system activity**, can use **different sources of information**, **tries to identify malicious activities**, **scans for patterns that might indicate a threat or for abnormalities**, and **compiles security-relevant events** (L04 p.38).

### IDS taxonomy

IDS types by information source (L04 p.39):
- **Host-based IDS (HIDS)** — analyse **host-level** information.
- **Network-based IDS (NIDS)** — capture & analyse **network traffic**.
- **Logging-based IDS (LIDS)** — analyse **collected logging**.

Cross-cutting distinctions (L04 p.39):
- **Misuse vs. anomaly** detection.
- **Passive vs. reactive** systems.

The lecture explicitly notes these "**aren't non-overlapping categories**" — a real system can be several at once (L04 p.39).

### What to detect: misuse vs. anomaly detection

**Misuse detection** (L04 p.40):
- Searches for **known attack signatures**.
- ⇒ **Susceptible to unknown attacks** (a brand-new attack has no signature yet).

**Anomaly detection** (L04 p.40):
- A **classical machine-learning** domain.
- **Learns normal patterns** of operation and **detects deviations** from normal.
- ⇒ **Susceptible to false positives** (legitimate-but-unusual activity looks like an attack).

This is the classic trade-off: signatures catch known attacks reliably but miss novel ones; anomaly detection can catch novel attacks but generates more false alarms.

### How to react: passive vs. reactive systems (IDS vs. IPS)

**Passive systems** filter information and extract relevant events ⇒ they are a **source of distilled information** (they detect and report, they do not act) (L04 p.41).

**Reactive systems** — **Intrusion Prevention Systems (IPS)** — are designed to **take action**, e.g. (L04 p.41):
- **Change firewall rules.**
- **Block users.**
- **Change network connectivity.**

So the **IDS vs. IPS** distinction in this course = **passive (detect/report) vs. reactive (detect and actively respond)**.

### IDS approaches: preemptive blocking, deflection, deterrence

Three IDS approaches (L04 p.42):

**Preemptive blocking** ("banishment vigilance") (L04 p.43):
- Seeks to **prevent intrusions before they occur.**
- Notes any sign of impending threats and **blocks the user or IP.**
- **Risk:** blocking **legitimate users** → risk of a self-inflicted **denial of service.**

**Intrusion deflection** (L04 p.44):
- Uses a **honeypot** — an attractive system with **fake but seemingly realistic** data/services.
- **Lures the attacker in and monitors their activity.**
- Detects ongoing attacks, **learns about new attacks**, and **collects information for forensics.**

**Intrusion deterrence** (L04 p.45):
- An attempt to **make the system a less palatable target.**
- E.g., having a **visible** IDS that signals activity might be noticed and that actions might be taken.
- The slide wryly adds "Whom this impresses is another story" — i.e., its effectiveness is uncertain.

### Example IDS/IPS systems

Named examples (all **free and open-source**) (L04 p.46):
- **Suricata**
- **Snort**
- **The Zeek Network Security Monitor**

The slide notes these are "partially not exactly IDSs" and that you should **determine which is best based on system context and requirements** (L04 p.46). *Note: the lecture lists these tools but does not provide Snort/Suricata rule syntax in the extractable slides — see the Gotchas section.*

### Incident response (after detection)

The lecture closes on **what to do when something goes wrong** despite policies, threat-aware development, and monitoring (L04 p.48).

**Immediate incident response** (L04 p.49):
- **Verification** — is the information correct?
- **Interpretation** — what actually happened?
- **Scope of incident** — actual & possible consequences.
- **Classification & prioritisation** — how do you have to act? (e.g., spam vs. scanning vs. compromised system.)
- References given: *ENISA Incident Handling Handbook* and *ENISA Incident Management Guide*.

**Next steps** (L04 p.50):
- **Forensics** — research what went wrong; *how and when do you secure the evidence?*
- **Restore operations** — how to rebuild systems: priorities, backups, a plan for getting things back online.
- These two aims (forensics vs. restore) **can counteract each other** (rebuilding may destroy evidence).
- **Communication** — internal/business partners & investors/customers.

---

## Glossary

- **Firewall** — A choke point of control and monitoring between networks of differing trust; a single point of defense (hardware/software) that enforces access control and allows/denies traffic to/from a network (L04 p.2–3).
- **Choke point** — A single controlled location through which traffic must pass so it can be monitored and restricted (L04 p.2).
- **NAT (Network Address Translation)** — Translates internal addresses so internal IPs are shielded from external networks; provided by packet-filter and circuit-level firewalls (L04 p.16, p.24).
- **VPN (Virtual Private Network)** — A secure connection over an untrusted network; firewalls can "implement VPNs using IPSec" (L04 p.2, p.34).
- **IPSec** — Protocol suite used by firewalls to implement VPNs (L04 p.2).
- **Packet filter (network-level firewall)** — Simplest, fastest firewall; examines each IP packet with no context and permits/denies per rules, restricting access to ports (L04 p.8).
- **Static packet filtering** — First-generation filtering with non-dynamic admin-defined rules that do not understand application-layer protocols (L04 p.10).
- **Dynamic packet filtering / Stateful inspection** — Filtering that tracks connection state (L04 p.9, p.18).
- **Default-deny policy** — "That not expressly permitted is prohibited" (the secure default) (L04 p.8).
- **Default-allow policy** — "That not expressly prohibited is permitted" (L04 p.8).
- **Access Control List (ACL)** — Ordered list of allow/deny rules (action, source/dest address, protocol, source/dest port) applied top to bottom (L04 p.14).
- **Stateful packet filter** — Examines packets in context, tracks client–server sessions using an INSPECT engine and state tables, detects out-of-context packets (L04 p.18–19).
- **Circuit-level gateway** — 3rd-generation firewall that validates TCP/UDP sessions before opening a circuit, relays two TCP connections, maintains a connection table; SOCKS is commonly used (L04 p.20–23).
- **SOCKS** — Protocol commonly used by circuit-level gateways (L04 p.21).
- **Application-level gateway / proxy** — Application-specific proxy with full protocol access; user requests a service from the proxy, which validates and actions it; can log/audit at the application level and provides HTTP caching, URL filtering, user auth (L04 p.25–27).
- **Bastion host** — Highly secure, hardened host running gateways/proxies, potentially exposed to hostile elements; minimal essential services, extra auth, small non-privileged proxies (L04 p.30).
- **Host-based firewall** — Software module securing an individual host; rules tailored to the host, protection independent of topology (L04 p.31).
- **Personal firewall** — Less-complex software module (on a PC or home router) that denies unauthorized remote access and monitors outbound activity for malware (L04 p.32).
- **DMZ (Demilitarized Zone)** — A firewall network configuration (slide p.33 is image-only; specific definition not in extractable lecture text) (L04 p.33, p.36).
- **Distributed firewall** — A firewall configuration/topology (slide p.35 image-only; specifics not in extractable text) (L04 p.35, p.36).
- **IDS (Intrusion Detection System)** — Monitors network/system activity to identify malicious activity, scanning for threat patterns or abnormalities and compiling security-relevant events (L04 p.38).
- **HIDS** — Host-based IDS; analyses host-level information (L04 p.39).
- **NIDS** — Network-based IDS; captures and analyses network traffic (L04 p.39).
- **LIDS** — Logging-based IDS; analyses collected logging (L04 p.39).
- **Misuse detection** — Searches for known attack signatures; susceptible to unknown attacks (L04 p.40).
- **Anomaly detection** — Learns normal patterns (ML) and detects deviations; susceptible to false positives (L04 p.40).
- **Passive system** — Filters/extracts relevant events; a source of distilled information (detect/report only) (L04 p.41).
- **Reactive system / IPS (Intrusion Prevention System)** — Takes action: change firewall rules, block users, change network connectivity (L04 p.41).
- **Preemptive blocking ("banishment vigilance")** — Prevents intrusions before they occur by blocking suspect users/IPs; risks a self-inflicted DoS on legitimate users (L04 p.43).
- **Honeypot** — An attractive system with fake-but-realistic data/services used to lure, monitor, and learn from attackers; used for intrusion deflection and forensics (L04 p.44).
- **Intrusion deterrence** — Making the system a less palatable target, e.g., a visible IDS (L04 p.45).
- **Suricata / Snort / Zeek** — Free, open-source example IDS/IPS / network security monitor tools (L04 p.46).
- **bcrypt** — Password-hashing algorithm; in the exercise, a `$2b$12$...` bcrypt hash must be cracked with `rockyou.txt` (E04 p.1).
- **rockyou.txt** — Wordlist compiled after the 2009 RockYou breach of plaintext passwords; pre-included in Kali Linux (E04 p.1).
- **Sneaker net** — Moving data physically (e.g., on storage media) rather than over the network; one way attacks bypass a firewall (L04 p.6).
- **Smurf DoS attack** — A DoS attack mitigated by dropping ICMP packets sent to a broadcast address (L04 p.13).

---

## How-To Cookbook

> The lecture expresses firewall logic as **policy → rule** and as **ACL rows**, not as `iptables` command syntax (no `iptables`/Snort syntax appears in the slides). The procedures below stay grounded in the lecture's own examples; where a generic command form is shown it is clearly marked as illustrative of the lecture's rule, not quoted from the slide.

### A. Write a packet-filter rule from a plain-English policy (lecture method)

For each policy, identify **direction, protocol, addresses, ports, and the action (drop/allow)**, then write a rule. Using the lecture's worked examples (L04 p.13):

1. **"No outside Web access."** → Drop all **outgoing** packets to **any IP**, **port 80**.
2. **"External connections to public Web server only."** → Drop all **incoming TCP SYN** packets to **any IP except 222.22.44.203, port 80** (i.e., only the public web server may receive new inbound connections).
3. **"Prevent IPTV from eating bandwidth."** → Drop all **incoming UDP** packets **except DNS and router broadcasts**.
4. **"Prevent being used for a Smurf DoS."** → Drop all **ICMP** packets going to a **broadcast address** (e.g., `222.22.255.255`).
5. **"Prevent your network from being tracerouted."** → Drop all **outgoing ICMP**.

General recipe: (a) decide the **default policy** — prefer **default-deny** ("not expressly permitted is prohibited", L04 p.8); (b) add explicit **allow** rules for required services; (c) end with an explicit **deny all**; (d) remember rules apply **top to bottom, first match wins** (L04 p.14).

### B. Build an Access Control List (the lecture's ACL format)

Each ACL row has six fields: **action, source address, dest address, protocol, source port, dest port** (L04 p.14). To allow internal network `222.22/16` to use external **web (TCP 80)** and **DNS (UDP 53)** with a default-deny:

1. **Allow outbound web:** `allow | 222.22/16 | outside 222.22/16 | TCP | >1023 | 80`.
2. **Allow web replies in:** `allow | outside 222.22/16 | 222.22/16 | TCP | 80 | >1023`.
3. **Allow outbound DNS:** `allow | 222.22/16 | outside 222.22/16 | UDP | >1023 | 53`.
4. **Allow DNS replies in:** `allow | outside 222.22/16 | 222.22/16 | UDP | 53 | >1023`.
5. **Default deny:** `deny | all | all | all | all | all`.

Key points: client ephemeral ports are `>1023`; server well-known ports are `80` (HTTP) and `53` (DNS); you need **both** an outbound rule and a matching return rule because a **static** filter has no session memory (a **stateful** filter would track the session and not need the explicit return rule — L04 p.18).

### C. Translate the lecture's ACL into illustrative `iptables` commands (not from the slides)

The slides do not give `iptables` syntax. The following is the standard Linux equivalent of the lecture's "allow internal `222.22.0.0/16` to reach external web/DNS, default deny" ACL, provided only as a practical realization of the lecture's rules (verify exact flags against your tool's manual):

```bash
# Default-deny: "that not expressly permitted is prohibited" (L04 p.8)
iptables -P FORWARD DROP

# Allow internal hosts to make outbound HTTP (dest port 80)
iptables -A FORWARD -s 222.22.0.0/16 -p tcp --sport 1024:65535 --dport 80 -j ACCEPT
# Allow the HTTP replies back in
iptables -A FORWARD -d 222.22.0.0/16 -p tcp --sport 80 --dport 1024:65535 -j ACCEPT

# Allow outbound DNS (UDP 53) and its replies
iptables -A FORWARD -s 222.22.0.0/16 -p udp --sport 1024:65535 --dport 53 -j ACCEPT
iptables -A FORWARD -d 222.22.0.0/16 -p udp --sport 53 --dport 1024:65535 -j ACCEPT

# (Optional) drop ICMP to broadcast to prevent Smurf DoS (L04 p.13)
iptables -A FORWARD -p icmp -d 222.22.255.255 -j DROP
```

A **stateful** equivalent (matching the stateful-filter concept of L04 p.18) would replace the explicit return rules with connection tracking, e.g. `iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT`.

### D. Harden a bastion host (checklist from the lecture)

Following the bastion-host description (L04 p.30):
1. Use a **hardened OS** with only **essential services** running.
2. Add **extra authentication** for access.
3. Run only **small, secure, independent, non-privileged proxies** (circuit/application-level gateways).
4. Provide a **special entrance for admin** only.
5. If it bridges two or more network connections, configure it to **enforce trusted separation** between them.

### E. Choose between misuse and anomaly detection (decision aid)

From L04 p.40:
1. If you mainly face **known attacks** and want **few false alarms** → use **misuse (signature) detection**; accept that it **misses unknown attacks**.
2. If you need to catch **novel/unknown attacks** → use **anomaly detection** (learns normal, flags deviations); accept that it **produces more false positives**.
3. In practice, combine both (the lecture notes the categories overlap — L04 p.39).

### F. Decide passive vs. reactive (IDS vs. IPS)

From L04 p.41:
1. If you only need **alerting / distilled information** → deploy a **passive IDS**.
2. If you need the system to **act automatically** (change firewall rules, block users, change connectivity) → deploy a **reactive IPS**, but weigh the **risk of blocking legitimate users / causing a DoS** (cf. preemptive blocking, L04 p.43).

### G. Crack the bcrypt hash with the rockyou wordlist (Exercise E04)

The exercise asks you to crack `$2b$12$SoreoddaNP22fhRp0ODWpeOD8USnAHjzFjRfKhlQyVzmTxikhL0lm` (bcrypt) using `rockyou.txt`, with any tool such as **Hashcat** or **John the Ripper** (E04 p.1). The exercise does **not** prescribe exact commands; the following are the standard invocations:

**John the Ripper:**
1. Save the hash to a file, e.g. `hash.txt` (one line: the `$2b$12$...` string).
2. Run: `john --format=bcrypt --wordlist=/usr/share/wordlists/rockyou.txt hash.txt`
3. View result: `john --show --format=bcrypt hash.txt`

**Hashcat** (bcrypt = mode **3200**):
1. Save the hash to `hash.txt`.
2. Run: `hashcat -m 3200 -a 0 hash.txt /usr/share/wordlists/rockyou.txt`
3. Show cracked: `hashcat -m 3200 hash.txt --show`

Notes grounded in the exercise: `rockyou.txt` is **pre-included in Kali Linux** (often gzipped at `/usr/share/wordlists/rockyou.txt.gz` — `gunzip` it first) (E04 p.1). bcrypt with a cost factor of **12** (the `$12$` in the hash) is deliberately slow, so cracking is feasible **only** because the password is expected to be a common one present in the wordlist — which is the security lesson of the exercise: short, popular passwords are dangerous (E04 p.1).

### H. Explain firewall types with metaphors (Exercise Task 1)

The exercise asks you to explain **Packet-Filtering, Stateful, and Application-Level Gateway/Proxy** firewalls with a metaphor, and to find other types not covered (E04 p.1). Grounded talking points to attach to your metaphor:
- **Packet filter** = a guard checking each letter's to/from address and "service" stamp (port) with no memory of past letters (no context) (L04 p.8, p.10).
- **Stateful** = a guard who remembers which conversations are already in progress and only lets replies through that belong to one (L04 p.18).
- **Application proxy** = a receptionist who opens, reads, and validates each request at the application level before fetching the result on your behalf (L04 p.25–26).
- **Other types not covered today** (per the exercise's "find others" prompt) that the lecture *does* mention elsewhere: **circuit-level gateway**, **bastion host**, **host-based**, **personal**, and configurations like **DMZ / VPN / distributed** (L04 p.20, p.30–36).

---

## Exam-Style Q&A

**Q1. List the three basic firewall types by OSI level, and add the two refinements the lecture stresses.**
A. The three basic types are (L04 p.7): **network level (packet filters)**, **application level (proxy server)**, and **circuit level (proxy server)**. The lecture additionally stresses **stateful packet filtering** as an evolution of the static packet filter (L04 p.9, p.18) and groups firewalls by **basing** — **bastion, host, personal** (L04 p.30–32, p.36). So a complete answer for "types of firewalls" is: packet-filter (static), stateful inspection, circuit-level, application proxy (L04 p.36 summary).

**Q2. What are the six factors a static packet filter uses to allow or deny a packet?**
A. (L04 p.11) 1) the **physical network interface** the packet arrives on; 2) the **source address**; 3) the **destination address**; 4) the **transport protocol** (TCP or UDP); 5) the **transport-layer source port**; 6) the **transport-layer destination port**. Note it does **not** understand application-layer protocols (L04 p.10).

**Q3. State the two possible default policies and say which is more secure and why.**
A. (L04 p.8) Either "**that not expressly permitted is prohibited**" (default-deny) or "**that not expressly prohibited is permitted**" (default-allow). Default-**deny** is more secure: it blocks everything unless explicitly allowed, so a forgotten or unknown service is closed by default rather than open. The lecture's example ACL ends with an explicit `deny all`, demonstrating default-deny (L04 p.14).

**Q4. Read this ACL row and explain it: `allow | 222.22/16 | outside 222.22/16 | TCP | >1023 | 80`.**
A. (L04 p.14) It **allows** traffic **from** the internal network `222.22/16` **to** any host outside `222.22/16`, over **TCP**, from an **ephemeral source port (>1023)** to **destination port 80**. In short: it permits **internal users to make outbound web (HTTP) requests**. A matching return rule (`source port 80 → dest >1023`) is needed because a static filter has no session memory.

**Q5. Why does a static packet filter need two rules (out and return) for one web session, while a stateful filter does not?**
A. A static filter examines each packet with **no context** (L04 p.8), so it cannot know a return packet belongs to a request it already allowed — you must write an explicit return rule (L04 p.14). A **stateful** filter examines packets **in context**, keeps a **state table** of client–server sessions, and checks each packet validly belongs to one, so return packets are matched automatically and out-of-context packets are detected (L04 p.18–19).

**Q6. Give three attacks on packet filters and one countermeasure each.**
A. (L04 p.17) **IP spoofing** (fake trusted source) → add router filters to block; **source-routing attacks** (attacker sets a non-default route) → block source-routed packets; **tiny fragment attacks** (header split across tiny packets) → discard such fragments or reassemble before checking.

**Q7. Compare the advantages and disadvantages of a stateful filter vs. an application proxy.**
A. Stateful (L04 p.19): operates at the 2nd/3rd OSI layer → **faster than an application proxy**, and is **application independent**; but offers **less access control** than a proxy. Application proxy (L04 p.27–28): **understands high-level protocols** (HTTP, FTP), can selectively deny services, shields internal IPs, and offers caching/URL filtering/auth; but is **slow**, requires replacing the native network stack, needs client-procedure modifications, and depends on (and inherits bugs from) the OS.

**Q8. What is a bastion host and what makes it secure?**
A. (L04 p.30) A **highly secure host** running circuit/application-level gateways or externally accessible services, potentially exposed to hostile elements. It is secured by a **hardened OS, only essential services, extra authentication**, and **small, secure, independent, non-privileged proxies**. It may support multiple network connections and be **trusted to enforce trusted separation** between them.

**Q9. Distinguish misuse detection from anomaly detection, including the weakness of each.**
A. (L04 p.40) **Misuse detection** searches for **known attack signatures** and is therefore **susceptible to unknown (new) attacks**. **Anomaly detection** is an ML approach that **learns normal patterns and flags deviations**, and is therefore **susceptible to false positives**. Trade-off: signatures = reliable on known attacks but blind to novel ones; anomaly = can catch novel attacks but raises more false alarms.

**Q10. What is the difference between a passive IDS and a reactive IPS? Give examples of reactive actions.**
A. (L04 p.41) A **passive** system filters information and extracts relevant events — it is a **source of distilled information** (detect/report only). A **reactive** system (an **IPS**) is designed to **take action**, e.g., **change firewall rules, block users, or change network connectivity**.

**Q11. Describe the three IDS approaches and a key risk or benefit of each.**
A. (L04 p.42–45) **Preemptive blocking ("banishment vigilance")** prevents intrusions before they occur by blocking suspect users/IPs — **risk:** blocking legitimate users (self-DoS). **Intrusion deflection** uses a **honeypot** (fake-but-realistic system) to lure and monitor attackers — **benefit:** learn about new attacks and gather forensics. **Intrusion deterrence** makes the system a less palatable target, e.g., a **visible IDS** signaling that activity may be noticed — benefit is psychological/uncertain.

**Q12. Name four things a firewall cannot protect against.**
A. (L04 p.6) Attacks that **bypass** it (e.g., sneaker net, utility modems, trusted services like SSL/SSH); **internal threats** (disgruntled/colluding employees); access via **WLAN** if improperly secured; and **malware imported** on a laptop/PDA/storage infected outside the network.

**Q13. Write firewall settings for: (a) prevent your network being used in a Smurf DoS attack; (b) prevent your network from being tracerouted.**
A. (L04 p.13) (a) **Drop all ICMP packets going to a broadcast address** (e.g., 222.22.255.255). (b) **Drop all outgoing ICMP.**

**Q14. What information does a circuit-level firewall store when a connection is set up, and what is its defining behavior?**
A. (L04 p.20, p.23) Defining behavior: it **validates TCP/UDP sessions before opening the circuit**, maintains a **table of valid connections**, and tears the entry down when the session ends. It stores: a unique **session ID**, the **connection state** (handshake/established/closing), **sequencing info**, **source IP**, **destination IP**, and the **inbound and outbound physical network interfaces**. It relays two TCP connections and commonly uses **SOCKS** (L04 p.21).

**Q15. (Exercise) You must crack a `$2b$12$...` bcrypt hash with rockyou.txt. Which tools and why is it feasible?**
A. (E04 p.1) Use **Hashcat** (mode `-m 3200` for bcrypt) or **John the Ripper** (`--format=bcrypt`) with `--wordlist=rockyou.txt`. bcrypt with cost 12 is deliberately slow, so a pure brute force is infeasible; it is crackable **only** because the password is expected to be a **common one present in rockyou.txt** — illustrating the lesson that short/popular passwords are dangerous. `rockyou.txt` itself came from a 2009 plaintext-password breach and ships with Kali Linux.

---

## Gotchas

- **"Three types" vs. the full list.** The slides say there are **three basic types** by OSI level (network/packet-filter, application/proxy, circuit-level) (L04 p.7), but the **summary** lists **packet-filter, stateful inspection, application proxy, circuit-level** (L04 p.36). If an exam asks "types of firewalls," give the four from the summary; if it asks "three basic types by OSI level," give exactly the three from p.7.
- **Static vs. stateful return traffic.** A common mistake is writing a single outbound rule on a **static** filter and assuming replies are allowed. They are not — a static filter has no session memory, so you need an explicit **return rule** (L04 p.14). Only a **stateful** filter tracks the session (L04 p.18).
- **ACLs are order-dependent.** Rules apply **top to bottom, first match wins** (L04 p.14). A broad `deny all` placed too early would block everything below it. Put specific `allow` rules first, the `deny all` last.
- **`>1023` ports.** The `>1023` in the ACL refers to **ephemeral client ports**, not the service. The service is identified by the **well-known** port (80 for HTTP, 53 for DNS). Don't swap source/dest ports between the request and the reply rule.
- **Default policy choice is a security decision.** "Not expressly prohibited is permitted" (default-allow) is convenient but insecure; prefer default-deny (L04 p.8).
- **Firewall ≠ complete defense.** It does nothing about internal threats, bypass paths (sneaker net, SSL/SSH tunnels it can't inspect), insecure WLAN, or malware carried in on devices (L04 p.6). Encrypted "trusted services" are explicitly a blind spot.
- **Misuse = false negatives on new attacks; anomaly = false positives.** Mixing these up is a classic error. Signatures miss the unknown; anomaly detection over-alerts (L04 p.40).
- **IDS detects, IPS acts.** Don't claim a plain (passive) IDS blocks attacks — only a reactive **IPS** changes firewall rules / blocks users / changes connectivity (L04 p.41). And preemptive blocking can cause a **self-inflicted DoS** by blocking legitimate users (L04 p.43).
- **Categories overlap.** HIDS/NIDS/LIDS, misuse/anomaly, and passive/reactive are **not mutually exclusive** — the lecture explicitly says so (L04 p.39). A single product can be several of these.
- **No Snort/iptables syntax in the slides.** The lecture **names** Snort, Suricata, and Zeek (L04 p.46) but gives **no rule syntax**; it expresses firewall logic as policy→rule and ACL rows, not as `iptables` commands. The `iptables`/Snort/Hashcat command lines in this guide's cookbook are **standard tool syntax provided for the practical task**, not quotations from the slides — verify exact flags against the tool manual in an open-book setting.
- **Image-only slides (no extractable detail).** Slides **p.5, p.12, p.15, p.22, p.29** (figures), and the configuration slides **p.33 (DMZ), p.34 (VPN), p.35 (Distributed Firewalls)** contained **only titles / images** with no body text. The only grounded fact for VPN is that firewalls "implement VPNs using IPSec" (L04 p.2). Do **not** invent DMZ/VPN/distributed-firewall specifics from these slides; if the exam needs them, rely on the original diagrams.
- **bcrypt cost factor.** The `$12$` in the exercise hash is the **cost factor** — higher = slower hashing. The crack succeeds via the **dictionary** (rockyou), not brute force; that's the intended point about weak/common passwords (E04 p.1).
```
