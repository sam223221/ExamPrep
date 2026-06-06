# 06. Denial of Service — Simulated Open-Book Questions

### [EASY] A monitoring dashboard shows your e-commerce site is fully online and serving pages, but a security alert claims an attacker "succeeded against the Availability leg of the CIA triad." A colleague insists this means customer data was stolen. Why is the colleague wrong, and what does the alert actually imply?
**Answer:** The colleague is conflating Availability with Confidentiality. A DoS attack does **not** try to steal or alter data — it tries to make the service unreachable or unusable (L06 p.8). Of the three CIA legs:

1. **Confidentiality** — about secrets/data theft (not the DoS target).
2. **Integrity** — about data tampering (not the DoS target).
3. **Availability** — about the service being reachable/usable. **This is what DoS attacks** (L06 p.8).

So an alert citing the Availability leg implies the attacker is trying to **deny legitimate users access** to the service, not exfiltrate data. If the dashboard currently shows the site online, the attack either failed or has not yet exhausted a bottleneck. Nothing in "Availability was targeted" implies a data breach.

### [EASY] You launch the Low Orbit Ion Cannon (LOIC) from a single laptop against a well-provisioned target and tell a friend "I just ran a DDoS." Based on the lecture's definitions, correct the terminology and explain the distinction.
**Answer:** One laptop running LOIC is a **DoS**, not a DDoS. The defining feature of a **D**DoS is that the traffic comes from **many sources simultaneously** (L06 p.8), typically a botnet. A single machine is a single source.

The lecture is explicit on two points that make this correction matter:

- **"Without botnets, DDoS is difficult to achieve"** (L06 p.35).
- **LOIC "cannot do DDoS by itself"** — that requires many volunteers (L06 p.38).

So the correct statement is: "I ran a single-source DoS." It only becomes a DDoS if many coordinated machines (or volunteers) flood the target at once.

### [EASY] A packet capture shows a stream of inbound TCP **SYN** packets to your server, the server replying with **SYN-ACK**, and then no final **ACK** ever arriving — just more SYNs. Name the attack and state the one specific resource it exhausts.
**Answer:** This is a **SYN flood** (L06 p.26). The signature is exactly what is described: SYN in, SYN-ACK out, and the final ACK never sent, while more SYNs keep arriving.

The specific resource it exhausts is the server's **buffer for incomplete (half-open) TCP connections** (L06 p.26). Each SYN that never completes leaves a half-open connection holding a slot in that buffer. Once the buffer is full, **the receiver cannot react to valid connection attempts** (L06 p.26) — legitimate users are denied service.

### [EASY] During an exam you must classify Slowloris as either a Layer 4 (transport) or a Layer 7 (application) attack, and say whether it is high-bandwidth or low-bandwidth. Give both answers with the one-line justification the lecture provides.
**Answer:** Slowloris is a **Layer 7 (application-layer)** attack and it is **low-bandwidth**.

Justification from the deck: Slowloris is explicitly called **"the only Layer 7 tool in this list"** (L06 p.42), and it is described as a **slow, low-bandwidth** attack. It ties up the web server's sockets by opening many connections and keeping them open with **partial HTTP requests**, exhausting the connection pool rather than the bandwidth (L06 p.42). That is why it is the odd one out and must **not** be described as a volumetric/bandwidth flood.

### [EASY] Your firewall already filters ICMP and UDP ports. According to the lecture, which class of tool/attack does this specifically help against, and what is the one-line reason this kind of rule works at all?
**Answer:** Filtering **ICMP and UDP ports** specifically helps prevent **some LOIC-style DDoS attacks** (L06 p.32), because LOIC does TCP, UDP and ICMP flooding (L06 p.37) — blocking those ports drops that flood traffic at the firewall.

The reason simple rules like this work at all is that **"simple firewall rules help against a uniform attack pattern"** (L06 p.35). A flood that all looks the same (same protocol, same port) is easy to match and drop with one rule. The limitation, implied by that same slide, is that non-uniform or application-layer traffic that looks legitimate is much harder to filter this way.

### [MEDIUM] Two captures land on your desk. Capture A: a single crafted packet whose **source IP and source port equal the destination IP and destination port** (both the victim's own), after which the victim appears to loop replying to itself. Capture B: an **ICMP echo request sent to a broadcast address with the source IP spoofed to the victim**, after which dozens of hosts send echo replies to the victim. Identify both attacks and explain how the spoofing differs.
**Answer:** **Capture A is a Land attack** (L06 p.29). **Capture B is a Smurf attack** (L06 p.27). These are easy to mix up because both involve spoofing, but the spoofing serves different purposes:

- **Land** spoofs **the victim's own IP and port as both source and destination** of a single packet. The victim machine ends up in an endless loop replying to itself (L06 p.29). The spoofing creates a self-referential loop on one machine.
- **Smurf** spoofs only **the victim's IP in the source field** of a broadcast ICMP echo request. Every host on the network (the intermediaries) replies, and all those replies are aimed at the victim, so **"the network performs a DDoS on itself"** (L06 p.27). The spoofing redirects many third-party replies at the victim.

In short: Land = victim spoofed as **both ends of one packet** (self-loop); Smurf = victim spoofed as the **source** of a broadcast request (reflection by intermediaries).

### [MEDIUM] A junior engineer enables **stack tweaking** (shorter ACK timeout, larger half-open buffer) against an ongoing SYN flood and declares the problem "solved." Quote and explain the lecture's caveat, then name a mitigation that actually addresses the root cause.
**Answer:** The engineer is wrong. The lecture's caveat is explicit: stack tweaking **"delays the effect, but is not fixing the bottleneck"** (L06 p.31). Increasing the buffer and shortening the ACK timeout just lets the server absorb a bit more before it fills up — a determined flood still exhausts the half-open buffer; you have only bought time.

A mitigation that actually addresses the root cause is the **SYN cookie** (L06 p.31): instead of allocating buffer state for each half-open connection, the server **encodes the connection information into the sequence number** it puts in the SYN-ACK. No half-open buffer is consumed at all. When the client's final ACK returns, the encoded cookie lets the server reconstruct the state and verify the client. Because the bottleneck (the half-open buffer) is never filled, this removes the exhaustion mechanism rather than merely delaying it.

### [MEDIUM] On a Metasploitable 2 victim, three separate workloads each cause DoS-like symptoms: (a) `nmap -T4 -p-` launched from Kali, (b) `for i in {1..200}; do curl -s http://victim/ & done` from Kali, (c) `for i in {1..20}; do cat /dev/urandom | md5sum & done` run on the victim itself. For each, state which resource is exhausted and whether the target is the network, the application, or the host.
**Answer:** Each workload deliberately exhausts a different resource (E06 §5 comparison):

1. **(a) Port scan (`nmap -T4 -p-`)** — exhausts the **kernel network stack**. Thousands of inbound TCP connection attempts force the kernel to handle SYNs, update connection tables and generate responses, raising CPU/software interrupts (E06 Task 2). **Target: the network.**
2. **(b) HTTP request flood (`curl` ×200)** — exhausts **Apache worker processes**. Unlike the scan, this overloads the web server itself, causing worker exhaustion, delayed responses and `curl` timeouts (E06 Task 3). **Target: the application.**
3. **(c) `cat /dev/urandom | md5sum` ×20 on the victim** — saturates **CPU and disk I/O internally**. The load is generated on the victim, not from Kali (E06 Task 4). **Target: the host.**

So: (a) network stack, (b) application/workers, (c) host CPU/I-O — three different bottlenecks producing the same superficial "service is slow/unresponsive" effect.

### [MEDIUM] Investigators arrested several Operation Payback participants who had used LOIC. A defendant argues "the tool must have hidden our IPs since it's a hacking tool." Using the lecture's facts about LOIC, explain why that argument fails.
**Answer:** The argument fails because **LOIC has no IP spoofing** (L06 p.38). It does not hide the attacker's IP, so **the source is traceable** (L06 p.38). The tool sends floods directly from the user's real address.

This is precisely why prosecution was possible: participants in the Anonymous campaigns (the Church of Scientology action in 2010 and Operation Payback in 2010) ran LOIC from their own machines, and because the tool offered no source-address forgery, their IPs were recorded by the targets (L06 pp.37–39). Contrast this with botnet toolkits like **TFN** and **Stacheldraht**, which explicitly support **IP spoofing / source-address forgery** (L06 p.40, p.41). LOIC simply does not, so "it must have hidden our IPs" is false on the facts.

### [MEDIUM] You receive three malformed-packet reports from 1997-era CVE write-ups: one reassembles to **66,000 bytes**, one contains **overlapping TCP fragments**, and one was "fixed years ago but reappeared in Windows Server 2003 / XP SP2." Identify each attack and state the single defensive lesson all three share.
**Answer:** The three reports map to:

1. **Reassembles to ~66,000 bytes** → **Ping of Death**. IPv4 packets can be up to **65,535 bytes**; the attacker crafts a fragmented packet that, when reassembled, **exceeds that limit**, causing buffer overflow / crash / possible RCE (L06 p.25). (Note: individual fragments are legal-sized; it is the *reassembled* size that is illegal.)
2. **Overlapping TCP fragments** → **Teardrop**. The victim fails to reconstruct the overlapping fragments correctly, restarting or crashing vulnerable systems (L06 p.28).
3. **Fixed years ago, reappeared in Windows Server 2003 / XP SP2** → **Land attack** (L06 p.29).

The shared defensive lesson is **keep your systems patched/updated** (L06 p.25, p.29, p.32). All three are malformed-packet attacks that break packet-handling logic, all were fixed long ago, and all resurfaced — so "an old bug is fixed" is never a safe assumption. This is the lecture's recurring "why you keep your systems updated" point.

### [HARD] You run a small network of 200 hosts that all reply to broadcast pings, and an attacker uses it for a Smurf attack against an external victim. Each spoofed 64-byte ICMP echo request triggers a 64-byte reply from every responding host. Walk through the amplification, give the rough amplification factor, and explain the two router-level changes that defeat this — and which side (your network or the victim) implements which.
**Answer:** Step through the reflection/amplification (L06 p.27):

1. The attacker sends **one** ICMP echo request to your network's **broadcast address**, with the **source IP spoofed to the victim**.
2. All 200 hosts that respond to broadcast pings each send back **one ICMP echo reply**.
3. Every reply is directed at the victim (because the spoofed source was the victim).
4. **Net effect:** one inbound request becomes ~200 replies at the victim — the network "performs a DDoS on itself" toward the victim.

**Rough amplification math:** 1 request in → 200 replies out, each the same 64-byte size, so the amplification factor is roughly **200×** in both packet count and bytes (200 × 64 = 12,800 bytes generated per 64-byte trigger). Multiply by the attacker's sustained request rate to get the flood aimed at the victim. The key insight is that the attacker spends a fraction of the bandwidth the victim receives — that is the whole point of amplification.

**Router-level defences (L06 p.27):**

- **Your (intermediary) network:** configure routers/hosts to **not respond to broadcast pings** — the default behaviour has since been changed in the standards precisely for this reason. This stops your network from being used as the amplifier in the first place.
- **The victim's side (and ingress points generally):** **ingress/egress filtering of spoofed source addresses** at the router level so spoofed-source packets cannot enter or leave; the lecture frames defence as being "at the router level." Removing either the amplifier (no broadcast replies) or the spoofing (anti-spoofing filtering) breaks the attack.

### [HARD] A defender wants to dismantle a DDoS rather than just absorb it. Using the TFN model of master/agents and the lecture's "Weaknesses of (D)DoS" slide, lay out a takedown strategy and explain at which moments the attacker becomes exposed.
**Answer:** Start from the TFN structure (L06 p.40): a **master controls agents**; **agents flood the designated targets**; **communications are encrypted and can be hidden in normal traffic**; and the **master can spoof its IP**. The DDoS depends entirely on this botnet infrastructure.

A takedown strategy that attacks the model rather than the symptom (L06 p.35):

1. **Take down the C&C servers.** Because the agents are directed by the master/C&C, removing that control plane stops new flood commands and fragments the botnet.
2. **Disinfect the compromised machines (zombies).** Cleaning the agents shrinks the flood capacity and keeps them from rejoining.
3. **Exploit the "must be sustained" property.** The flood **must be sustained** to deny service (L06 p.35) — so any disruption to C&C or agents lets the service recover. You do not need to clean everything at once; you need to break sustainment.
4. **Apply simple firewall rules where the pattern is uniform** (L06 p.35) to blunt the flood while infrastructure takedown proceeds.

**Where the attacker is exposed (L06 p.35):**

- **When the C&C server is taken over,** "the attacker might be at risk of discovery" — seizing the control server can reveal the operator's identity/infrastructure.
- **When packets can be tracked** — traceable traffic exposes the attacker (note that toolkits add IP spoofing and encryption specifically to avoid this; a tool like LOIC, lacking spoofing, leaves the operator traceable — L06 p.38).

So the defender's leverage is structural: the botnet is both the attack's strength and its weak point.

### [HARD] Your single, well-provisioned server is being hit by a sustained volumetric DDoS that saturates its upstream internet link. You have already enabled SYN cookies, tuned the stack, and added firewall rules, yet users still cannot reach the site. Explain why your on-box mitigations cannot help here and what the lecture recommends instead, including how that solution survives an attack on one of its nodes.
**Answer:** Your on-box mitigations cannot help because the exhausted resource is **the upstream internet link itself**, and that bottleneck is **real and physical** — the lecture's point is that you cannot "free up your internet connection" once it is saturated (L06 p.33). SYN cookies fix the half-open buffer, stack tweaking and firewall rules act on the server, but none of them add bandwidth or move the flood off your saturated pipe. The packets have already consumed the link before your server logic ever runs.

What the lecture recommends is a **third-party web-security service that puts reverse proxies as frontends to your service** (e.g. **Cloudflare**) (L06 p.33). The mechanism (L06 p.33):

1. Traffic is **rerouted via data centres at multiple locations** instead of all arriving at your single link.
2. The aggregate capacity of those distributed proxies absorbs/distributes a volumetric flood that no single server could.
3. **If one reverse proxy is attacked, others can take over**, so the load is spread and the attack on one node does not take the service down.
4. **Your service stays available** behind the proxy frontend.

This is the practical answer to bandwidth-exhaustion DDoS precisely because it moves the absorption off your one physical link and onto a distributed, redundant frontend — defeating the attack at the layer where you, on one box, are powerless.

### [HARD] A security team must explain the through-line connecting the lecture's brute-force material to its DoS material. Trace the causal chain from default IoT credentials all the way to a DDoS, citing the specific statistics and aims the lecture gives.
**Answer:** The through-line is that **brute force recruits the zombies that power DDoS**. Trace it step by step:

1. **Default credentials on IoT devices/routers.** Brute force is especially dangerous against **IoT devices and routers with default usernames/passwords** (L06 p.53). With a predicted **29 billion IoT devices by 2023**, the attack surface is enormous.
2. **Brute force over telnet/ssh.** The attacks are typically against **telnet and ssh** (L06 p.53). The lecture's figure: in **H1 2023, 97.91% of attacks were against telnet** (L06 p.53). Brute force is "unsophisticated trial-and-error" (L06 p.46) but it wins against weak/default credentials.
3. **Compromise → zombie.** Once credentials fall, the device is compromised. Keeping systems updated is exactly what prevents a machine **becoming a zombie in a botnet** (L06 p.32). Unpatched, default-credentialed IoT devices have no such protection.
4. **Zombies → botnet → DDoS.** The stated **aims** of these IoT compromises include **DDoS, ransomware, DNS redirection, and proxies** (L06 p.53), and the dark-net "services" on offer include **DDoS attacks, botnets, and zero-day IoT vulnerabilities** (L06 p.53). The brute-forced devices become the agents a C&C directs to flood targets.

So the causal chain is: **default IoT credentials → telnet/ssh brute force (97.91% telnet in H1 2023) → compromised zombie → botnet under C&C → DDoS**. The lecture even closes the loop explicitly: brute-forced IoT devices are the zombies that power DDoS — which is why the two halves of the lecture belong together.

### [HARD] A company's helpdesk reports that legitimate users are being locked out of RDP en masse, with no flood of network traffic visible. The brute-force slide hints at the cause. Explain the mechanism, why it counts as a DoS against Availability, and the trade-off the lecture is flagging with "what could possibly go wrong?"
**Answer:** The mechanism is **abuse of an account-lockout policy** as a denial-of-service vector. The lecture notes that Windows 11 RDP got default protection in July '22: a **10-minute account lock after 10 invalid sign-in attempts**, and pointedly asks **"what could possibly go wrong?"** (L06 p.47). The answer the question implies: an attacker who does **not** need to guess the password can simply submit **10 deliberately wrong attempts per account** to trip the lockout, locking the real user out for 10 minutes — and repeat to keep them out indefinitely.

Why it is a DoS against Availability:

- No data is stolen or altered; the goal is purely to **prevent legitimate users from accessing the system** (L06 p.8) — the Availability leg of the CIA triad.
- It also explains the symptom: **no large traffic flood is needed**, because the resource exhausted is *the user's right to authenticate*, not bandwidth or CPU. A handful of bad logins per account is enough.

The trade-off the lecture flags is the classic security tension: a lockout policy is a **defence against brute force** (it caps guesses), but the very same mechanism becomes an **offensive DoS tool** — the control designed to protect Availability can be weaponised to destroy it. That is the "what could possibly go wrong?" point: aggressive lockouts can backfire.

### [VERY HARD] You are triaging two simultaneous incidents. Incident X: low inbound packet rate, but the web server's connection pool is fully consumed by many connections that send a few HTTP header bytes every several seconds and never finish their requests. Incident Y: a massive inbound packet rate of small UDP datagrams saturating the link. Classify each as Layer 4 vs Layer 7, name the most likely attack, explain why a "uniform-pattern" firewall rule helps one far more than the other, and tie this to the lecture's stated trend.
**Answer:** **Classification and naming:**

- **Incident X** — **Layer 7 (application-layer)**, most likely **Slowloris**. The signature is exact: low bandwidth, many connections held open with **partial HTTP requests** that never complete, exhausting the server's **sockets/connection pool** (L06 p.42). It is the only Layer 7 tool in the lecture's list.
- **Incident Y** — **Layer 4 (transport-layer)**, a **UDP flood** (volumetric). High packet rate of small UDP datagrams saturating the link is the bread-and-butter volumetric attack a botnet uses (L06 p.102 framing: UDP/ICMP floods saturate bandwidth/processing; LOIC/TFN/Stacheldraht all do UDP flooding — L06 pp.37, 40, 41).

**Why a uniform-pattern firewall rule helps Y far more than X:**

- The lecture states **"simple firewall rules help against a uniform attack pattern"** (L06 p.35). Incident Y *is* uniform — a torrent of similar UDP datagrams on identifiable ports — so a single rule (e.g. **filter UDP ports**, the same lever that blunts LOIC floods — L06 p.32) drops the bulk of it. The flood looks nothing like legitimate traffic.
- Incident X resists this because Slowloris requests **look like legitimate, if slow, HTTP traffic**. There is no uniform malicious pattern to match: each connection is a valid-looking partial request at the application layer. A port/protocol firewall rule cannot distinguish a slow-but-legitimate client from Slowloris, so the uniform-pattern rule that crushes Y barely touches X. (Defending X needs application-aware measures — connection timeouts, per-IP connection limits, a reverse proxy — not a simple L4 filter.)

**Tie to the trend:** This is exactly why the lecture reports that **"Layer 4 attacks dwindle, Layer 7 attacks are on the rise"** (L06 p.23). The easily-filtered, uniform Layer-4 floods (Incident Y) are losing favour, while the harder-to-filter, legitimate-looking Layer-7 attacks (Incident X) are rising — because they defeat the cheap defences that stop volumetric floods.

### [VERY HARD] Compare three "exhaustion" attacks the lecture/lab treat as distinct: a classic SYN flood, the Slowloris attack, and the lab's HTTP `curl` flood against Apache. For each, identify the precise resource exhausted, the OSI layer, the rough bandwidth profile, and why a SYN cookie would or would not help. Then state the single mitigation that best fits each.
**Answer:** All three exhaust a finite resource (the core DoS mechanism — L06 p.22), but at different layers and with different profiles:

1. **SYN flood**
   - **Resource:** the **half-open (incomplete) TCP connection buffer** (L06 p.26).
   - **Layer:** Layer 4 (transport) — it abuses the TCP 3-way handshake.
   - **Bandwidth:** moderate; the attacker just sprays SYNs and never completes, so it is cheaper than a full volumetric flood but still needs a steady SYN rate.
   - **SYN cookie?** **Yes — directly applicable.** SYN cookies encode state in the sequence number so no half-open buffer is consumed (L06 p.31); this is the textbook fix for this exact bottleneck.
   - **Best mitigation:** **SYN cookies** (with RST cookies as a complement; stack tweaking only delays — L06 p.31).

2. **Slowloris**
   - **Resource:** the **web server's sockets / connection pool**, held open by partial HTTP requests (L06 p.42).
   - **Layer:** Layer 7 (application) — the only Layer 7 tool in the list.
   - **Bandwidth:** **very low** — that is its defining trait.
   - **SYN cookie?** **No.** The TCP handshakes *complete* (the connections are real, fully-open), so the half-open buffer is never the bottleneck. SYN cookies solve a Layer-4 problem Slowloris does not create.
   - **Best mitigation:** application-aware controls — aggressive **connection/request timeouts**, **per-IP connection limits**, or fronting with a **reverse proxy** (L06 p.33) that buffers/normalises slow clients.

3. **Lab HTTP `curl` flood (×200/×500) against Apache**
   - **Resource:** **Apache worker processes** — worker exhaustion, delayed responses, timeouts (E06 Task 3).
   - **Layer:** Layer 7 (application) — it overloads the web server, not the network stack (contrast with the port scan, which hits the kernel — E06 Task 2).
   - **Bandwidth:** higher than Slowloris — it is a genuine flood of complete requests, though far smaller than a link-saturating volumetric attack.
   - **SYN cookie?** **No.** Again the connections complete; the bottleneck is the worker pool, not the half-open buffer. SYN cookies are irrelevant.
   - **Best mitigation:** **rate limiting** at the server/reverse proxy and adequate worker provisioning; the lab's root-cause analysis notes Metasploitable 2 has **no modern protections such as rate limiting** (E06 §7), which is exactly why it falls over.

**Synthesis:** SYN cookies are a precise, Layer-4 answer to *one* bottleneck (half-open buffers). Both Layer-7 attacks complete their handshakes, so they slip past SYN cookies entirely and demand application-layer mitigations (timeouts, per-IP limits, rate limiting, reverse proxies). This is the practical reason the lecture stresses that the rising Layer-7 attacks are harder to defend — the cheap L4 fixes do not apply.

### [VERY HARD] The MitID "Insecurity of the Week" case combined three weaknesses: a username-enumeration oracle, missing rate-limiting/blocking (≈11,000 usernames harvested in one night), and a DoS against 17 consenting users, plus lacking logging. Construct a defense-in-depth response that addresses each weakness, and explain how one missing control — rate limiting — sits at the intersection of enumeration, brute force, and DoS.
**Answer:** Recall the case facts (L06 p.6): **username guessing was possible** (a non-existent UID was *immediately confirmed* as non-existent — an enumeration oracle); **~11,000 usernames were harvested in one night without being blocked**; there was a **DoS against 17 users** (who had consented); and there was **lacking logging & surveillance**.

**Defense-in-depth response, weakness by weakness:**

1. **Enumeration oracle (immediate "no such user" confirmation).** Make responses **indistinguishable** for valid vs invalid UIDs — uniform messaging and uniform timing so the system never functions as an oracle. This removes the "is this a real account?" signal at the source.
2. **11,000 harvested unblocked → no rate limiting.** Introduce **rate limiting and blocking** on enumeration/login attempts (per-IP, per-account, per-session), with **CAPTCHAs / progressive delays** so an attacker cannot make thousands of probes in a night. This maps directly onto the lecture's general mitigations — **rate limiting / IDS-IPS / firewall filtering** of abusive sources (L06 pp.31–33; E06 §7 notes the lab victim's downfall was "no modern protections such as rate limiting").
3. **DoS against 17 users.** Defend Availability with the lecture's tooling: detect abusive patterns (**IDS/IPS**), apply rate limits, and — critically — design lockout/blocking so it **cannot itself be weaponised** (the "what could possibly go wrong?" lockout-as-DoS trap from L06 p.47). Use per-source throttling rather than blanket account locks that an attacker could trigger against legitimate users.
4. **Lacking logging & surveillance.** Add **comprehensive logging and monitoring** so enumeration sweeps and DoS bursts are visible and alertable. The lecture repeatedly ties detection to logs — brute force "floods a good system's logs" (L06 p.49) and the lab inspects `access.log`/`error.log` for the attack signature (E06 §6). Without logging, none of the above is detectable after the fact.

**Why rate limiting sits at the intersection:** The single missing control of **rate limiting** would have blunted all three threat types at once:

- **Enumeration:** caps how many UIDs an attacker can test, so 11,000 probes in a night becomes impossible — the oracle is only dangerous if you can query it at scale.
- **Brute force:** the lecture frames brute force as "an attack against the odds (combinatorics)" that needs **many attempts** (L06 p.49); rate limiting directly "makes the combinatorics work against the attacker" (the defender's move at L06 p.50–51) by starving it of attempts.
- **DoS:** abusive request volume — whether enumeration, brute force, or a flood — is exactly what rate limiting throttles, protecting Availability (L06 p.8).

So rate limiting is the keystone control: enumeration, brute force, and DoS are all **volume-of-attempts** problems, and rate limiting attacks the volume directly. Its absence in MitID is why a single gap manifested as three distinct vulnerabilities — and why defense-in-depth must pair it with non-oracle responses and thorough logging so the remaining edges are covered.

### [VERY HARD] An attacker boasts of a "next-gen" DDoS that combines: (1) reflected/amplified ICMP via Smurf, (2) a SYN flood, and (3) a Slowloris layer — all from a botnet with spoofed sources and encrypted C&C. As defender, prioritise your countermeasures, explain which single defensive action degrades the most attack components at once, and identify the one component that survives most of your defenses and why.
**Answer:** Decompose the blended attack and map each component to the lecture's countermeasures, then prioritise.

**Component-by-component defenses:**

1. **Smurf (reflection/amplification, spoofed source).** Defeated at the **router level**: stop responding to **broadcast pings** (now the standard default) and apply **anti-spoofing ingress/egress filtering** (L06 p.27). Anti-spoofing filtering also undercuts the botnet's spoofed sources generally.
2. **SYN flood (Layer 4, half-open buffer).** Defeated by **SYN cookies** (root-cause fix — no half-open buffer consumed), with **RST cookies** as a complement; stack tweaking only delays (L06 p.31).
3. **Slowloris (Layer 7, low-bandwidth, sockets held open).** Needs **application-aware** defenses — connection timeouts, per-IP connection limits, and ideally a **reverse proxy** frontend that normalises/buffers slow clients (L06 pp.33, 42).
4. **Botnet with spoofed sources + encrypted C&C (the substrate).** Attack the model itself: **take down C&C servers** and **disinfect machines** (L06 p.35); the flood **must be sustained**, so disruption restores service. Taking over the C&C also risks **exposing the attacker** (L06 p.35).

**Prioritised plan:**

1. **First, deploy a third-party reverse-proxy / web-security service (e.g. Cloudflare).** This is the **single action that degrades the most components at once**. Its distributed data centres (L06 p.33) absorb and distribute the **volumetric Smurf reflection** and the **SYN flood** across many nodes (so no single link saturates and per-node SYN handling is spread/cookied at the edge), **and** the proxy frontend is exactly where you enforce the **timeouts and per-IP connection limits that blunt Slowloris**. One deployment touches all three traffic-facing components, and "if one reverse proxy is attacked, others take over" (L06 p.33).
2. **Enable SYN cookies** on origin and edge to remove the half-open-buffer bottleneck regardless of how much SYN traffic the proxy passes through.
3. **Push anti-spoofing and no-broadcast-reply at the router level** to kill the Smurf amplifier and reduce spoofed-source effectiveness (L06 p.27).
4. **In parallel, attack the botnet substrate** — C&C takedown and disinfection (L06 p.35) — to end sustainment and potentially expose the operator.

**The component that survives most defenses, and why: Slowloris.** Every defense above that relies on a **uniform pattern or Layer-4 mechanics** misses it. SYN cookies do not apply (its handshakes complete). Anti-spoofing and no-broadcast-reply do not apply (it does not spoof or use broadcast). Simple firewall rules fail because **"simple firewall rules help against a uniform attack pattern"** (L06 p.35) and Slowloris traffic **looks like legitimate, slow HTTP** — there is no uniform malicious signature. Even bandwidth-absorbing capacity barely helps, since Slowloris is **low-bandwidth by design** (L06 p.42); it exhausts **sockets**, not the link. Only the application-aware controls (timeouts, per-IP connection caps, the reverse proxy's slow-client handling) actually touch it — which is precisely why the lecture warns that **Layer 7 attacks are on the rise** (L06 p.23): they slip past the cheap, uniform-pattern, Layer-4 defenses that crush the volumetric and protocol-layer components of the very same blended attack.

### [VERY HARD] A red-team report claims their botnet "achieves a sustained 50× amplification using Smurf, so we don't even need many zombies — one attacker box is enough for a real DDoS." Evaluate this claim on three independent grounds (the amplification math, the lecture's definition of DDoS, and the durability/traceability of the approach), and state whether the claim holds.
**Answer:** The claim conflates *amplification* with *distribution* and ignores both durability and traceability. Evaluate it on three independent grounds:

**1. The amplification math is real but bounded — and it is reflection, not distribution.** Smurf genuinely amplifies: one spoofed broadcast ICMP echo request triggers a reply from every responding host, so on a network of ~50 responders you get roughly **50× more reply traffic at the victim than the attacker sent** (L06 p.27). So the *50×* figure is plausible. But amplification multiplies **volume**, not **sources of origination**. The replies still come from a finite, fixed amplifier network whose default behaviour has since been changed in the standards to **not respond to broadcast pings** (L06 p.27), and anti-spoofing router filtering blocks the spoofed source. The math gives bandwidth, not a botnet.

**2. By the lecture's own definition, this is not a real DDoS.** A DDoS is defined by traffic from **many sources simultaneously** (L06 p.8), and the lecture states flatly that **"without botnets, DDoS is difficult to achieve"** (L06 p.35) and that **"simple DoS might suffer from network bottlenecks"** (L06 p.35). "One attacker box + a reflector" is still a *single originating source* constrained by its own uplink to send the trigger stream; reflection borrows a third party's bandwidth but does not make the attack distributed. It is a (amplified) DoS, not a DDoS.

**3. Durability and traceability undercut it further.** The lecture's "Weaknesses" slide notes the flood **must be sustained** (L06 p.35) — the moment the single box stops (or its uplink is throttled, or the reflector is fixed), the victim recovers. And reflection through a known amplifier plus a single origin makes **packets trackable**, which the lecture flags as a moment the attacker **"might be at risk of discovery"** (L06 p.35). Contrast genuine botnet toolkits (TFN, Stacheldraht) that add **IP spoofing across many agents and encrypted, hideable C&C** precisely to gain distribution, durability and stealth (L06 pp.40–41) — none of which a single reflector box provides.

**Verdict: the claim does not hold.** The 50× number is legitimately *amplification*, but amplification is not distribution. By the lecture's definitions it remains a single-source DoS — bandwidth-constrained at origin, easily defeated at the router (no-broadcast-reply + anti-spoofing), non-durable once flooding stops, and traceable. "One box is enough for a real DDoS" fails on all three independent grounds.
