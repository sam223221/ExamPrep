# 06. Denial of Service

> Source material: `L06_DoS.pdf` (lecture slides, ~57 pages) and `E06_DoS.pdf` (lab/exercise sheet, ~5 pages), by Hiraku Morita, March 2026. Citations point to the lecture slide page printed in the corner of each slide (e.g. `(L06 p.26)`) or to the exercise sheet (e.g. `(E06 Task 2)`).
>
> **Scope note / honesty caveat:** This chapter is grounded *only* in what those two PDFs contain. The lecture is a slide deck, so many slides are short bullet lists plus images (Kaspersky statistics graphics that contain no extractable text). Where the slides only show a chart title without underlying numbers, that is noted explicitly rather than guessed. The deck also briefly covers **Brute Force** at the end (slides 46–53); that material is summarised here because it is part of the same lecture, but the main exam focus of this chapter is DoS/DDoS.

---

## Overview — what this topic covers and why it matters

A **Denial of Service (DoS)** attack aims to **prevent legitimate users from accessing a system or service** (L06 p.8). In terms of the CIA triad (Confidentiality, Integrity, Availability), DoS specifically **targets Availability** (L06 p.8) — it does not try to steal or alter data, it tries to make the service unreachable or unusable. When the attack traffic comes from **many distributed sources at once**, typically a botnet of compromised machines, it is a **Distributed Denial of Service (DDoS)** attack (L06 p.8, p.40).

DoS is described in the lecture as "another very common type of attack" (L06 p.8) and one that is **still extremely common today** (L06 p.22). The reason is structural: every system has **physical or logical limitations that create bottlenecks** — number of users, file sizes, connection bandwidth, number of parallel connection handshakes, and CPU computation bandwidth (L06 p.22). **Exceed any one of these limits and the system's response behaviour breaks down** (L06 p.22). That is the core idea the exercise sheet calls **resource exhaustion** (E06, Learning Objectives). The lecture also notes the threat is *evolving*: attacks are getting more complex, simple **Layer 4 (transport)** attacks are dwindling while **Layer 7 (application)** attacks are on the rise, many easy-to-use attack tools exist, professionals favour advanced attacks, and hacktivists still tend to use simpler ones (L06 p.23). This chapter covers how the classic attacks work, how to mitigate them, the real tools used in the wild, and the hands-on lab where resource exhaustion is observed on a deliberately vulnerable VM. The end of the lecture pivots to **brute force** attacks, included here for completeness.

---

## Key Concepts

### DoS vs DDoS

**What:** A **DoS** attack comes from (typically) a single source and tries to deny legitimate users access to a system. A **DDoS** (Distributed DoS) attack does the same thing but from **many sources simultaneously** (L06 p.8).

**Why it matters:** The lecture is explicit that **"without botnets, DDoS is difficult to achieve"** (L06 p.35) and that a successful flood **"must be sustained"** (L06 p.35). A single attacking machine is limited by its own network bottleneck — **"Simple DoS might suffer from network bottlenecks"** (L06 p.35) — so to overwhelm a well-provisioned target you generally need many machines, i.e. a **botnet** of compromised "zombie" hosts coordinated by a **Command & Control (C&C)** server (L06 p.32, p.40). The summary slide reinforces this: DoS "can be unsophisticated… can be devastating… but require many partners for effective operation (DDoS)" (L06 p.44).

**How:** In a DDoS the attacker controls a **master** which directs many **agents/zombies**; agents flood the designated target while the master can spoof its IP and hide communications (L06 p.40). Defenders can attack the distributed model itself by **taking down C&C servers** and **disinfecting machines** (L06 p.35).

### The Availability target (CIA triad)

**What:** DoS attacks the **Availability** leg of Confidentiality–Integrity–Availability (L06 p.8).

**Why:** This frames every defensive decision. The attacker is not after secrets or data tampering; they want the service *down*. Hence mitigations are about keeping the service reachable (reverse proxies, extra bandwidth, filtering) rather than about encryption or access control.

### Why DoS works — bottlenecks / resource exhaustion

**What:** DoS is possible because real systems have finite resources. The lecture lists concrete bottlenecks (L06 p.22):
- Number of users
- Size of files
- Bandwidth of connection
- Number of parallel connection handshakes
- Bandwidth of CPU computation

**Why:** **"Exceed any limit and response behaviour breaks down"** (L06 p.22). The exercise reframes this as the fundamental concept of DoS being **resource exhaustion** (E06, Learning Objectives) — you observe how a limited-resource system behaves under load until services degrade and the system becomes unstable.

**How (from the lab):** Different attack styles exhaust different resources — **CPU**, **disk I/O**, **network connection tables**, and **web-server worker processes** (E06 Tasks 2–5, §5 Comparison). A port scan stresses the kernel network stack, an HTTP flood exhausts Apache workers, and an internal I/O workload saturates CPU/disk.

### Attack-layer taxonomy (Layer 4 vs Layer 7)

**What:** The lecture distinguishes **Layer 4 (transport-layer)** attacks from **Layer 7 (application-layer)** attacks (L06 p.23).

**Why:** It captures the *trend*: **"Layer 4 attacks dwindle, Layer 7 attacks on the rise"** (L06 p.23). Layer 4 attacks (e.g. SYN flood, UDP flood) hit the transport/network plumbing; Layer 7 attacks (e.g. HTTP flood, Slowloris) hit the application logic and are harder to filter because the requests look legitimate.

**How / examples from the deck:**
- Transport/network-layer (Layer 3/4) examples: Ping of Death, SYN flood, Smurf, Teardrop, Land, UDP/ICMP floods (L06 pp.25–29, p.40).
- Application-layer (Layer 7) examples: **Slowloris** — explicitly called "the only Layer 7 tool in this list" (L06 p.42) — and **HTTP flooding** (LOIC/HOIC, L06 p.37, p.39; E06 Task 3).

> Note: The lecture does not use the textbook tripartite "volumetric / protocol / application-layer" naming explicitly; it uses the **Layer 4 vs Layer 7** framing (L06 p.23). The individual attacks below map onto those general categories, but cite the slide's own terminology in the exam.

### Ping of Death (PoD, 1997)

**What:** An attack that crafts an oversized/illegally-fragmented IP packet (L06 p.25).

**Why/How:** TCP/IP IPv4 packets can be up to **65,535 bytes** (L06 p.25). The attacker crafts a **fragmented packet that, when reassembled, goes beyond this limit** (L06 p.25). The result may be a **buffer overflow** — a system crash — **or even remote code execution (RCE)** (L06 p.25). Current OSes handle this, but it resurfaces in CVEs (the slide cites **CVE-2013-3183** and **CVE-2020-16898**) (L06 p.25). The lecture uses it as the **classic example of "why you keep your systems updated"**, noting a Linux patch landed **2:34:10 hours after the report** (L06 p.25). Footnote: modern packets can window-scale up to a gigabyte per **RFC 7323** (L06 p.25).

### SYN Flood (1996)

**What:** A Layer-4 attack that **exploits the TCP 3-way handshake** (L06 p.26). This is the single most exam-relevant attack in the deck.

**How the handshake is abused (L06 p.26):**
1. Attacker sends a **SYN** packet.
2. Receiver replies with **SYN-ACK**.
3. Receiver **waits for the final ACK** (with a timeout) — the connection is "half-open".
4. The attacker **never sends the final ACK**, instead **flooding the target with more SYN packets**.

**Why it works — the bottleneck:** The target keeps a **buffer for incomplete (half-open) TCP connections**, and that buffer fills up (L06 p.26). The slide notes that **in the early 1990s a server might allow only ~5 concurrent connection attempts** (L06 p.26). Once the buffer is full, **the receiver cannot react to valid connection attempts** (L06 p.26) — legitimate users are denied service. (Mitigations: SYN cookies / RST cookies / stack tweaking — see "Mitigating SYN Floods" below.)

### Smurf (IP) attack (1997)

**What:** A **reflection/amplification** attack using ICMP echo (ping) over broadcast (L06 p.27).

**How (L06 p.27):**
1. Attacker sends an **ICMP echo request to a network broadcast address**, with the **source IP spoofed to point at the victim**.
2. Every host on that network (the **intermediaries**) responds with an **ICMP echo reply**.
3. All those replies are directed at the victim, **flooding** it.
4. Net effect: **"The network performs a DDoS on itself."**

**Why it matters:** It is the deck's clearest example of **reflection + amplification** — one spoofed request becomes many replies aimed at the victim. **Defence is at the router level**, and default router behaviour has since been adjusted in the standards to not respond to broadcast pings (L06 p.27).

### Teardrop fragmentation attack (1997)

**What:** An attack using a **crafted, fragmented TCP message** whose **fragments overlap** (L06 p.28).

**How/Why:** The victim system **fails to reconstruct the overlapping fragments correctly**, which **restarts or crashes vulnerable systems** (L06 p.28). Like Ping of Death, it's a malformed-packet attack that breaks the reassembly logic rather than a pure flood.

### Land attack (Local Area Network Denial, 1997)

**What:** An attack that creates an **endless forwarding loop** by setting **identical source and destination IPs and ports** in a packet (L06 p.29).

**How/Why:** The attacker **spoofs the target/victim's own IP and port** as both source and destination; the **victim machine enters a loop replying to itself** (L06 p.29). It is a **very simple setup** (L06 p.29). It was **fixed in 1997** but **resurfaced in Windows Server 2003 and Windows XP SP2** (L06 p.29) — another illustration that old bugs come back.

### UDP / ICMP floods

**What:** Plain volumetric floods of UDP or ICMP traffic. The deck does not give them a dedicated theory slide but references them repeatedly in the tools section: **LOIC does TCP, UDP & ICMP flooding** (L06 p.37); **TFN does SYN flood, UDP flood and Smurf** (L06 p.40); **Stacheldraht does ICMP ping floods, TCP SYN & UDP floods, and Smurf** (L06 p.41).

**Why:** These are the bread-and-butter volumetric attacks a botnet uses to saturate a target's bandwidth or processing.

### Botnets, C&C, and zombies

**What:** A **botnet** is a network of compromised machines ("zombies") controlled by an attacker through a **Command & Control (C&C)** server to mount a DDoS (L06 p.32, p.40).

**How (TFN model, L06 p.40):** A **master controls agents**; **agents flood the designated targets**; **communications are encrypted** and **can be hidden in normal traffic**; the **master can spoof its IP**.

**Why it matters for defence:** Because DDoS depends on the botnet, defenders can strike the infrastructure: **take down C&C servers** and **disinfect machines** (L06 p.35). The lecture also warns the *attacker* is exposed at these moments — **"When the C&C server is taken over, the attacker might be at risk of discovery"**, and **"same when packets can be tracked"** (L06 p.35). Keeping your own systems updated prevents your machines from **becoming zombies in a botnet used for an attack** (L06 p.32).

### Mitigating SYN Floods (SYN cookies, RST cookies, stack tweaking)

Three specific SYN-flood mitigations (L06 p.31):

- **SYN Cookie:** Instead of allocating buffer state on the half-open connection, the server **encodes the relevant connection information into the sequence number** it sends in the SYN-ACK. When the client's final ACK comes back, that ACK **verifies the client's response** and the encoded cookie lets the server reconstruct state. This means **no buffer is consumed by half-open connections**.
- **RST Cookie:** The **server replies with a deliberately bad SYN-ACK**, which **forces a legitimate client to send a RST**. That RST **verifies the client's genuine interest** in establishing a connection — bots that just flood SYNs won't complete this.
- **Stack Tweaking:** Operating-system-level tuning — **reduce the timeout for accepting the final ACK**, **increase the buffer size**, etc.

**Critical caveat (exam point):** Stack tweaking **"delays the effect, but is not fixing the bottleneck"** (L06 p.31). It buys time, it doesn't solve the problem.

### Generic mitigations

For DoS in general, the deck lists (L06 p.32):

- **Firewalls** — e.g. **filtering ICMP and UDP ports prevents some LOIC DDoS attacks**.
- **Intrusion Detection / Prevention Systems (IDS/IPS)** — detect and block attacks, e.g. **blocking the attacked service in the firewall**.
- **Updated systems** — keep AV signatures, OS and software patches current, both to fix vulnerabilities (Ping of Death, Teardrop, Land) and to **prevent your machines becoming zombies** in a botnet.

The Weaknesses slide adds: **"Simple firewall rules help against a uniform attack pattern"** (L06 p.35) — uniform/repetitive attack traffic is the easiest to filter.

### Third-party / web-security services (reverse proxies)

**What:** Outsourced DDoS protection via providers that put **reverse proxies as frontends to your service** (L06 p.33). Cloudflare is named as an example (L06 p.33).

**Why/How (L06 p.33):** Many bottlenecks are *real and physical* — "try freeing up your internet connection" once it's saturated, you can't. So these services **reroute traffic via data centres at multiple locations**; **if one reverse proxy is attacked, others can take over**, and **your service stays available**. This is the practical answer to bandwidth-exhaustion DDoS that no single server can defend on its own.

### Weaknesses of (D)DoS attacks (the defender's leverage)

The lecture lists why DoS attacks are not invincible (L06 p.35):
- The **flood must be sustained** (stop flooding, service recovers).
- **Counter-measures include taking down C&C servers** and **disinfecting machines**.
- Taking over a **C&C server puts the attacker at risk of discovery**; same if **packets can be tracked**.
- **Simple DoS suffers from network bottlenecks** (the attacker has limits too).
- **Without botnets, DDoS is difficult to achieve.**
- **Simple firewall rules help against a uniform attack pattern.**

### (D)DoS tools seen in the wild

The lecture surveys real "network stress testing" / attack tools (L06 pp.37–42):

- **LOIC — Low Orbit Ion Cannon** (L06 p.37–38): open-source stress-test/DoS tool with an **easy GUI**; targets a **URL or IP**; does **TCP, UDP & ICMP flooding** and **HTTP flooding**. **Limitations: no IP spoofing → doesn't hide your IP → source is traceable; and it can't do DDoS by itself** — that **requires many volunteers**. Used by **Anonymous** with volunteers against the **Church of Scientology (2010)** and in **Operation Payback (2010)** against companies opposing WikiLeaks.
- **HOIC — High Orbit Ion Cannon** (L06 p.39): performs **HTTP flood** attacks; developed by Anonymous members (prosecuted during Operation Payback); **designed to be effective with ~50 users**, more needed against protected servers.
- **TFN / TFN2K — Tribal Flood Network (1999)** (L06 p.40): a set of programs for **DDoS** doing **SYN flood, UDP flood and Smurf**, with **C&C support** (master/agents, encrypted and hideable comms, master can spoof IP).
- **Stacheldraht (1999, "barbed wire")** (L06 p.41): **ICMP ping floods, TCP SYN & UDP floods, Smurf**, **source address forgery (IP spoofing)**, **encryption**; **combines features of Trinoo & TFN**.
- **Slowloris** (L06 p.42): the **only Layer 7 tool in the list**; a **slow, low-bandwidth** attack that **ties up the web server's sockets** by **opening many connections and keeping them open as long as possible** while **making partial HTTP requests**. Original **Perl script from 2009**, also a Python implementation.

### Brute Force (the lecture's second half)

The lecture pivots from DoS to **brute force** (L06 pp.46–53). Key points:

- **What:** A technique that **lacks sophistication** — **trial and error to determine invisible entities** like **usernames, passwords, and web-server directories** (L06 p.46). Can run **locally** (e.g. **John the Ripper** on a copy of the hashes) or **remotely over a network** (L06 p.46).
- **Remote tools (L06 p.47):** **Hydra** — a **parallelised login cracker** supporting parallelisation and many protocols; **Crowbar** for **OpenVPN, RDP, SSH private keys, VNC keys**. Note Windows 11 RDP got **default protection in July '22**: a **10-minute account lock after 10 invalid sign-in attempts** — the slide asks pointedly "what could possibly go wrong?" (a lockout policy can itself be abused for DoS).
- **Reducing the search space (L06 p.48):** **dictionary attacks**, **personal info** (birthdays, names), and **rule-based permutations of dictionaries**. History: passwords were once protected by a **slow `crypt()` routine**, until **optimised crackers (Crack 3.2a, 1991; rule-based Crack 4.x, 1991)** changed the rules. **John the Ripper is a successor of Crack.**
- **"A noisy affair" (L06 p.49):** Brute force is an **attack against the odds (combinatorics)**; repeated trial-and-error **produces lots of noise** and **floods a good system's logs** — but it still wins **if the attacker can sneak away with the information**.
- **Attacker vs defender (L06 p.50–51):** Attacker **modulates patterns, distributes & delays, reduces search space, uses statistics on common phrases**, and chooses **broad sweep vs targeted**. Defender **picks up on patterns, disrupts ongoing attacks, makes combinatorics work against the attacker, evens the odds (password policies), and checks passwords against the same lists attackers use.**
- **Relevance — IoT (L06 p.53):** Especially dangerous for **IoT devices/routers with default usernames/passwords**. Prediction of **29 billion IoT devices by 2023**; brute force is typically against **telnet and ssh**; tracked with **IoT honeypots**. In **H1 2023, 97.91% of attacks were against telnet**. Aims include **DDoS, ransomware, DNS redirection, proxies**; the dark-net "services" include **DDoS attacks, botnets, and zero-day IoT vulnerabilities** (cited to Kaspersky IoT threat report 2023). Note the loop back to DoS: brute-forced IoT devices become the zombies that power DDoS.

### "Insecurity of the Week" — the MitID DoS case

The lecture's news item (L06 pp.5–6) is a **MitID DoS** incident. Known details were sparse (little media detail despite lurid coverage from Version2), but the issues raised were (L06 p.6):
- **Username guessing was possible** — a non-existent UID was **immediately confirmed** as non-existent (an enumeration oracle).
- **~11,000 usernames harvested in one night without being blocked.**
- A **DoS against 17 users** (who had given consent for the test).
- The possibility of **socially engineering someone into "swiping"** (approving) a login.
- **Lacking logging & surveillance.**

**Exam relevance:** It ties DoS to real-world identity systems and shows that **weak rate-limiting and missing logging** enable both enumeration and DoS.

---

## Glossary

- **Denial of Service (DoS)** — An attack whose goal is **preventing legitimate users from accessing the system**; it **targets Availability** of the CIA triad (L06 p.8).
- **Distributed Denial of Service (DDoS)** — A DoS launched from **many sources at once**, generally requiring a **botnet**; "without botnets, DDoS is difficult to achieve" (L06 p.8, p.35).
- **Availability** — The CIA-triad property that a service is reachable/usable; the property DoS attacks (L06 p.8).
- **Resource exhaustion** — The core mechanism of DoS: consuming a finite resource (CPU, memory, I/O, bandwidth, connection slots, workers) until the service degrades or fails (E06, Learning Objectives; L06 p.22).
- **Bottleneck** — A finite limit (users, file size, connection bandwidth, parallel handshakes, CPU bandwidth) that, once exceeded, breaks response behaviour (L06 p.22).
- **Layer 4 attack** — A transport/network-layer DoS (e.g. SYN flood, UDP flood); the lecture says these are **dwindling** (L06 p.23).
- **Layer 7 attack** — An application-layer DoS (e.g. HTTP flood, Slowloris); these are **on the rise** (L06 p.23).
- **SYN flood** — Exploits the TCP 3-way handshake by sending SYNs and never the final ACK, filling the **half-open connection buffer** (L06 p.26).
- **Half-open connection** — A TCP connection where SYN-ACK was sent but the final ACK never arrived; these consume the buffer the SYN flood targets (L06 p.26).
- **3-way handshake** — TCP connection setup: SYN → SYN-ACK → ACK (L06 p.26).
- **Ping of Death (PoD)** — Crafting a fragmented IP packet that reassembles beyond **65,535 bytes**, causing buffer overflow / crash / possible RCE (L06 p.25).
- **Smurf attack** — Broadcast ICMP echo request with the **victim's IP spoofed as source**; all intermediaries reply to the victim, so the **network DDoSes itself**; defended at router level (L06 p.27).
- **Reflection / amplification** — Technique (illustrated by Smurf) where a spoofed request triggers many larger/numerous responses aimed at the victim (L06 p.27).
- **Teardrop attack** — Crafted **overlapping TCP fragments** that break the victim's reassembly logic, causing restart/crash (L06 p.28).
- **Land attack** — Packet with **identical source and destination IP and port** (the victim's own), causing the victim to loop replying to itself (L06 p.29).
- **Botnet** — A network of compromised "zombie" machines controlled by an attacker to mount DDoS (L06 p.32, p.40).
- **Zombie** — A compromised machine enrolled in a botnet; keeping systems updated prevents your machine becoming one (L06 p.32).
- **Command & Control (C&C / C2) server** — The infrastructure that directs botnet agents; taking it down is a key counter-measure (L06 p.35, p.40).
- **IP spoofing / source address forgery** — Faking the source IP of packets; used by Smurf, Land, TFN, Stacheldraht (L06 pp.27, 29, 40, 41).
- **SYN cookie** — SYN-flood mitigation: encode connection state into the sequence number instead of allocating buffer; the returning ACK verifies the client (L06 p.31).
- **RST cookie** — SYN-flood mitigation: server sends a bad SYN-ACK to force a legitimate client to RST, verifying its interest (L06 p.31).
- **Stack tweaking** — OS tuning (shorter ACK timeout, bigger buffer) that **delays but does not fix** the SYN-flood bottleneck (L06 p.31).
- **Reverse proxy** — A front-end (e.g. from Cloudflare) that absorbs/distributes traffic across data centres so the protected service stays available (L06 p.33).
- **IDS / IPS** — Intrusion Detection / Prevention Systems that detect and block attacks, e.g. blocking the attacked service in the firewall (L06 p.32).
- **LOIC (Low Orbit Ion Cannon)** — GUI stress/DoS tool; TCP/UDP/ICMP + HTTP flooding; **no IP spoofing (traceable)**, **can't DDoS alone** (L06 pp.37–38).
- **HOIC (High Orbit Ion Cannon)** — HTTP-flood tool; effective with ~50 users (L06 p.39).
- **TFN / TFN2K (Tribal Flood Network)** — 1999 DDoS toolkit: SYN/UDP floods + Smurf, encrypted C&C, IP spoofing (L06 p.40).
- **Stacheldraht** — 1999 DDoS tool combining Trinoo & TFN: ICMP/SYN/UDP floods, Smurf, IP spoofing, encryption (L06 p.41).
- **Slowloris** — Layer-7, low-bandwidth attack that holds web-server sockets open with partial HTTP requests (L06 p.42).
- **Fork bomb** — A self-replicating process that exhausts the process table and freezes the system: `:(){ :|:& };:` (E06 Task 5).
- **Metasploitable 2** — Intentionally vulnerable VM (no system updates) used as the DoS lab victim (E06, Purpose).
- **Brute force** — Unsophisticated trial-and-error to discover usernames, passwords, or directories (L06 p.46).
- **Hydra** — Parallelised remote login cracker supporting many protocols (L06 p.47).
- **John the Ripper** — Password cracker, successor of Crack; can run locally on a copy of hashes (L06 p.46, p.48).
- **Dictionary attack** — Brute force restricted to a wordlist (plus rule-based permutations) to shrink the search space (L06 p.48).

---

## How-To Cookbook

> These procedures are taken directly from the **E06 exercise sheet** (the DoS lab on Metasploitable 2 from Kali Linux) plus the conceptual mitigations from the lecture. Run only against systems you own/are authorised to test — the lab environment is the deliberately vulnerable Metasploitable 2 VM (E06, Purpose). The lecture does **not** include an `hping3` SYN-flood walkthrough; the SYN-flood material is conceptual (L06 p.26) and the lab suggests building one as an extension (E06 §8). See "Gotchas" before assuming an exact `hping3` command from this lecture.

### A. Set up the lab environment (E06, Environment Setup)
1. Provision two VMs: **Victim = Metasploitable 2**, **Attacker = Kali Linux**.
2. Put **both on the same virtual network** (NAT or Host-Only).
3. On Metasploitable 2, find its IP address:
   ```
   ifconfig
   ```
4. Note that IP — it replaces `<METASPLOITABLE IP>` in every command below.

### B. Task 1 — Baseline observation (E06 Task 1)
1. Open a terminal **inside Metasploitable 2** and run:
   ```
   top
   ```
2. Observe and record: **CPU usage, Memory usage**, and the running services **Apache, Tomcat, vsftpd, MySQL**.
3. List the listening services:
   ```
   netstat -tulnp
   ```
4. To leave `top`, **press `q`** to return to the shell.
5. This baseline is what every later stress test is compared against.

### C. Task 2 — Network-layer stress via port scan (E06 Task 2)
1. From **Kali**, run a full TCP port scan against the victim:
   ```
   nmap -T4 -p- <METASPLOITABLE IP>
   ```
   (`-T4` = aggressive timing; `-p-` = all 65,535 ports.)
2. On **Metasploitable 2**, watch `top` and observe: **CPU activity — especially Idle (`id`) and Software Interrupt (`si`)**, **slower terminal responses**, and **occasional spikes from Apache/Tomcat**.
3. **Stronger variant — parallel scans:** launch 10 scans at once:
   ```
   for i in {1..10}; do nmap -T4 -p- <METASPLOITABLE IP> & done
   ```
   Watch `top` again — degradation should be more pronounced.
4. **Stop the scans:**
   ```
   pkill nmap
   ```
*Why it stresses the victim:* each scan forces the kernel to handle thousands of incoming TCP connection attempts — handling SYN packets, updating connection tables, generating responses — raising software interrupts and reducing responsiveness (E06 Task 2).

### D. Task 3 — Application-layer stress via HTTP flood (E06 Task 3)
1. From **Kali**, send a single request first to confirm the service:
   ```
   curl http://<METASPLOITABLE IP>/
   ```
2. Flood Apache with **200 parallel** background requests:
   ```
   for i in {1..200}; do curl -s http://<METASPLOITABLE IP>/ >/dev/null & done
   ```
3. On **Metasploitable 2**, observe: **Apache workers increasing, CPU spikes, and `curl` delays or timeouts**.
4. **Stronger variant — 500 parallel requests:**
   ```
   for i in {1..500}; do curl -s http://<METASPLOITABLE IP>/ >/dev/null & done
   ```
5. **Stop the flood:**
   ```
   pkill curl
   ```
*Why:* unlike the port scan (network stack), this **overloads the Apache web server itself**, causing **worker exhaustion**, delayed responses, and service degradation (E06 Task 3).

### E. Task 4 — Internal I/O / CPU exhaustion (E06 Task 4)
1. **On Metasploitable 2 itself**, launch 20 parallel I/O+CPU-heavy jobs:
   ```
   for i in {1..20}; do cat /dev/urandom | md5sum & done
   ```
2. Observe with:
   ```
   top
   ```
   Look for **CPU and I/O saturation, system lag or partial freeze, and service response degradation** (also rising software interrupts, processes entering **D-state**, increased I/O wait).
3. **Stop the workload:**
   ```
   pkill md5sum
   ```
*Why it differs:* the load is generated **internally on the victim**, not from Kali, exhausting CPU and disk directly (E06 Task 4).

### F. (Optional) Task 5 — Full system freeze with a fork bomb (E06 Task 5)
1. **Warning: this will freeze the VM** (E06 Task 5). Only run on a disposable VM you can hard-reset.
2. On Metasploitable 2:
   ```
   :(){ :|:& };:
   ```
   This defines a function `:` that calls itself twice (piping one copy into another and backgrounding), recursively, until the process table is exhausted.

### G. Inspect log evidence (E06 §6)
1. On Metasploitable 2, examine the Apache logs for evidence of the floods:
   ```
   /var/log/apache2/access.log
   /var/log/apache2/error.log
   ```
2. Look for whether the DoS attempts are visible, any **unusual or repeated entries**, and what they reveal about service stress.

### H. Recognising attack traffic (symptoms to look for)
Per the lecture and exercise, the tell-tale signs of a DoS in progress:
1. **CPU**: high usage, low **Idle (`id`)**, rising **Software Interrupt (`si`)** and I/O wait (E06 Tasks 2 & 4).
2. **Network/connection state**: many **half-open TCP connections** for a SYN flood (conceptually, the half-open buffer fills — L06 p.26); thousands of inbound connection attempts during scans (E06 Task 2).
3. **Web server**: rising **worker process** count, delayed responses, **timeouts** on `curl` (E06 Task 3).
4. **Logs**: floods of repeated entries; brute force in particular "floods a good system's logs" (L06 p.49).
5. **Traffic shape**: a **uniform attack pattern** is the giveaway that simple firewall rules can block (L06 p.35).

### I. Mitigation procedure (conceptual, from the lecture)
1. **Against SYN floods specifically (L06 p.31):** enable **SYN cookies** (encode state in the sequence number, no half-open buffer used); use **RST cookies** (force legitimate clients to RST); apply **stack tweaking** (shorter ACK timeout, bigger buffer) — but remember this **only delays, doesn't fix**.
2. **Filter at the firewall (L06 p.32):** block/filter **ICMP and UDP ports** (stops some LOIC-style floods) and block the attacked service.
3. **Deploy IDS/IPS (L06 p.32):** detect and automatically block attack sources.
4. **Keep systems updated (L06 p.32):** patch OS/software (closes PoD/Teardrop/Land-class bugs) and keep AV signatures current so your hosts don't become **zombies**.
5. **Use a third-party reverse-proxy service (L06 p.33):** e.g. Cloudflare — reroute traffic across multiple data centres so an attack on one proxy is absorbed and the service stays up.
6. **Attack the botnet (L06 p.35):** where possible, **take down C&C servers** and **disinfect machines**; remember the flood **must be sustained**, so disruption restores service.

---

## Exam-Style Q&A

**Q1. What is the goal of a DoS attack, and which part of the CIA triad does it target?**
A. The goal is to **prevent legitimate users from accessing the system** (L06 p.8). It targets **Availability** of the CIA triad (L06 p.8) — it does not aim at confidentiality or integrity (it neither steals nor alters data), only at making the service unreachable/unusable.

**Q2. Distinguish DoS from DDoS. Why is a botnet usually necessary for DDoS?**
A. A **DoS** typically originates from a single source; a **DDoS** comes from **many sources simultaneously** (L06 p.8). A botnet is usually necessary because a single attacking machine is constrained by its own network bottleneck — "Simple DoS might suffer from network bottlenecks" — and the lecture states outright that **"without botnets, DDoS is difficult to achieve"** (L06 p.35). The flood also **must be sustained** (L06 p.35), which many coordinated zombies make possible.

**Q3. Explain the mechanism of a SYN flood step by step. What is the bottleneck it exhausts?**
A. It exploits the **TCP 3-way handshake** (L06 p.26): (1) the attacker sends a **SYN**; (2) the receiver replies **SYN-ACK** and (3) **waits (with a timeout) for the final ACK**; (4) the attacker **never sends the ACK** and instead **floods more SYNs**. The exhausted bottleneck is the **buffer for incomplete (half-open) TCP connections** — once it is full, **the receiver cannot react to valid connection attempts** (L06 p.26). The slide notes early-1990s servers might allow only ~5 concurrent connection attempts.

**Q4. Name and explain three mitigations specific to SYN floods. Which one only delays the problem?**
A. (1) **SYN cookie** — encode connection info in the **sequence number** instead of allocating buffer state; the client's returning ACK verifies it, so no half-open buffer is consumed. (2) **RST cookie** — the server sends a **bad SYN-ACK** to force a legitimate client to send a **RST**, verifying genuine interest. (3) **Stack tweaking** — reduce the ACK timeout and increase the buffer. **Stack tweaking only delays the effect — it "is not fixing the bottleneck"** (L06 p.31).

**Q5. How does the Smurf attack work, and why is it described as the network "performing a DDoS on itself"?**
A. The attacker sends an **ICMP echo request to a broadcast address with the source IP spoofed to the victim's address** (L06 p.27). Every host on the network (the intermediaries) **replies**, and all those **ICMP echo replies flood the victim**. Because the network's own hosts generate the flood toward the victim, **"the network performs a DDoS on itself."** It is an example of **reflection/amplification**, and defence is at the **router level** (default behaviour has been changed in the standards).

**Q6. Compare Ping of Death, Teardrop, and Land. What category of attack do they share, and what do their defences have in common?**
A. All three are **malformed-/crafted-packet attacks from 1997** that break a victim's packet-handling logic rather than simply flooding bandwidth. **Ping of Death** sends a fragmented IP packet that reassembles **beyond 65,535 bytes**, causing buffer overflow/crash/possible RCE (L06 p.25). **Teardrop** sends **overlapping TCP fragments** that break reassembly, crashing the system (L06 p.28). **Land** sends a packet with **identical source/destination IP and port** (the victim's), so the victim **loops replying to itself** (L06 p.29). Their defences share a theme: **keep systems patched** — all three were fixed long ago but resurfaced (Land in Windows Server 2003 / XP SP2; PoD as later CVEs), which is the lecture's "why you keep your systems updated" lesson (L06 p.25, p.29).

**Q7. Why are DoS attacks "still so common"? Give the structural reason.**
A. Because every system has **physical/logical limitations that create bottlenecks** — number of users, file sizes, connection bandwidth, number of parallel connection handshakes, CPU computation bandwidth — and **exceeding any limit makes response behaviour break down** (L06 p.22). Additionally, attacks are getting more complex, **Layer 7 attacks are rising**, and there are **many easy-to-use attack tools** (L06 p.23).

**Q8. What is the difference between a Layer 4 and a Layer 7 DoS attack, and what trend does the lecture report? Give an example of each.**
A. **Layer 4** attacks hit the transport/network plumbing (e.g. **SYN flood**, UDP flood); **Layer 7** attacks hit the application (e.g. **HTTP flood**, and **Slowloris**, "the only Layer 7 tool in this list" — L06 p.42). The trend: **Layer 4 attacks are dwindling while Layer 7 attacks are on the rise** (L06 p.23).

**Q9. How does Slowloris achieve denial of service with very little bandwidth?**
A. Slowloris is a **slow, low-bandwidth Layer-7 attack** that **ties up the web server's sockets** by **opening many connections and keeping them open as long as possible**, sending only **partial HTTP requests** so the server keeps each connection waiting (L06 p.42). It exhausts the connection pool rather than the bandwidth, which is why it works on low bandwidth.

**Q10. Compare LOIC and HOIC. What is a key limitation of LOIC for an attacker?**
A. **LOIC** is an easy-GUI tool that floods via **TCP, UDP, ICMP and HTTP** against a URL/IP (L06 p.37). **HOIC** focuses on **HTTP flood** attacks and was **designed to be effective with ~50 users** (L06 p.39). A key LOIC limitation: it has **no IP spoofing**, so it **does not hide the attacker's IP and the source is traceable**, and it **cannot do DDoS on its own** — that requires many volunteers (L06 p.38). Both were used by Anonymous (e.g. Operation Payback, 2010).

**Q11. What roles exist in a botnet-based DDoS (using TFN as the model), and how can defenders exploit the model's weaknesses?**
A. In the TFN model a **master controls agents**; **agents flood the targets**; **communications are encrypted and can be hidden in traffic**, and the **master can spoof its IP** (L06 p.40). Defenders exploit weaknesses (L06 p.35): the **flood must be sustained**; **taking down C&C servers** and **disinfecting machines** disrupts it; **taking over a C&C server or tracking packets risks exposing the attacker**; and **without botnets DDoS is hard to achieve**, while **simple firewall rules defeat a uniform attack pattern**.

**Q12. Your service is being hit by a bandwidth-saturating DDoS that your single server cannot absorb. What does the lecture recommend, and why?**
A. Use a **third-party web-security service that provides reverse proxies as a frontend** (e.g. **Cloudflare**) (L06 p.33). Because **many bottlenecks are real and physical** — once your internet connection is saturated you cannot free it locally — these services **reroute traffic via data centres at multiple locations**, so **if one reverse proxy is attacked, others take over** and **your service stays available** (L06 p.33).

**Q13. In the Metasploitable 2 lab, three external/internal techniques caused DoS-like effects. Identify which resource each one exhausted and which targets the application versus the network versus the host.**
A. (1) **Port scan from Kali** (`nmap -T4 -p-`, optionally ×10 in parallel) stresses the **network stack** — thousands of inbound TCP connection attempts raise CPU/software interrupts and connection-table work (E06 Task 2). (2) **HTTP request flood** (`curl` ×200/×500 in parallel) overloads the **Apache web server**, exhausting **worker processes** (E06 Task 3). (3) **I/O exhaustion** (`cat /dev/urandom | md5sum` ×20, run on the victim) saturates **CPU and disk I/O** internally (E06 Task 4). So: Task 2 = network, Task 3 = application/workers, Task 4 = host CPU/I/O (E06 §5).

**Q14. What symptoms in `top` indicate the victim is under network or I/O stress, and what would you check in the logs?**
A. In `top`: falling **Idle (`id`)**, rising **Software Interrupt (`si`)** and I/O wait, **slower terminal response**, spikes from Apache/Tomcat, rising **worker** counts, and processes entering **D-state** (E06 Tasks 2–4). In the logs, check `/var/log/apache2/access.log` and `error.log` for whether the flood is visible, **unusual or repeated entries**, and signs of service stress (E06 §6). Note the lecture's parallel point that brute force "floods a good system's logs" (L06 p.49).

**Q15. Why is Metasploitable 2 so easily disrupted, and what general lessons does that teach about DoS defence?**
A. Per the exercise's root-cause analysis (E06 §7), it has **outdated/poorly-optimised services**, **no modern protections such as rate limiting**, **limited CPU/memory**, and **architectural weaknesses** — and it intentionally **does not support updates** (E06, Purpose). The lessons map onto the lecture's mitigations: **rate limiting / IDS-IPS / firewall filtering**, **keeping systems updated**, and **provisioning enough resources or offloading to reverse proxies** all directly address those weaknesses (L06 pp.31–33).

**Q16 (bonus — brute force). What is brute force, what makes it "noisy," and how does it connect back to DoS?**
A. Brute force is **unsophisticated trial-and-error to find usernames, passwords, or directories** (L06 p.46). It is "noisy" because it is an **attack against combinatorial odds** that **produces many failed attempts**, **flooding the logs** — though it succeeds if the attacker can **sneak away with the information** (L06 p.49). It connects to DoS via **IoT**: brute-forcing default telnet/ssh credentials (97.91% of H1-2023 IoT attacks were against telnet) recruits devices into **botnets whose stated aim includes DDoS** (L06 p.53).

---

## Gotchas

- **DoS attacks Availability, not Confidentiality/Integrity.** A common exam trap is to associate any attack with data theft. DoS specifically targets **Availability** (L06 p.8).
- **Stack tweaking is not a fix.** For SYN floods, increasing the buffer and shortening the ACK timeout **only delays the effect — it does not fix the bottleneck** (L06 p.31). Don't list it as a solution without that caveat.
- **DDoS ≠ a bigger DoS from one machine.** The defining feature is *many* sources; the lecture stresses **"without botnets, DDoS is difficult to achieve"** (L06 p.35). A single host running LOIC is a DoS, not a real DDoS — LOIC explicitly **cannot DDoS alone** (L06 p.38).
- **LOIC does not spoof IPs.** Its users are **traceable** — this is *why* Operation Payback participants could be prosecuted (L06 p.38–39). Don't claim LOIC hides the attacker.
- **Smurf is reflection/amplification, not a direct flood.** The attacker sends *one* spoofed broadcast ping; the *intermediaries* generate the flood at the victim (L06 p.27). The victim's address is in the **source** field (spoofed), not the destination.
- **Land vs Smurf spoofing differ.** Land spoofs **the victim's own IP and port as both source and destination** to make it loop on itself (L06 p.29); Smurf spoofs **the victim as source** of a broadcast request (L06 p.27). Easy to mix up.
- **Ping of Death is about reassembled size, not a single huge packet.** The attack uses **fragmentation** so the reassembled packet exceeds 65,535 bytes (L06 p.25); the individual fragments are legal-sized.
- **Old attacks resurface.** PoD, Teardrop, and Land were all fixed in the 1990s but came back (Land in Windows Server 2003 / XP SP2; PoD as later CVEs) (L06 p.25, p.29). The recurring lesson is **patching**, and "an old bug is fixed" is not a safe assumption.
- **Slowloris is the odd one out.** It is the **only Layer 7 tool** in the tool list and is **low-bandwidth** (L06 p.42) — don't describe it as a volumetric/bandwidth flood.
- **The lab's "DoS" is mostly resource exhaustion, not classic network attacks.** Tasks 2–5 stress CPU/I/O/workers; a true **SYN flood is not provided as a ready command** — it's suggested as an extension to build yourself (E06 §8). Don't claim the exercise ran an `hping3` SYN flood; the lecture/lab don't give that command.
- **Fork bomb will freeze the VM.** `:(){ :|:& };:` is destructive — the sheet warns it freezes the machine (E06 Task 5). Only on a disposable VM.
- **Account-lockout defences can backfire.** The brute-force slide flags Windows 11 RDP's "10-min lock after 10 bad attempts" with "what could possibly go wrong?" (L06 p.47) — an aggressive lockout policy can itself be abused to **lock out legitimate users (a DoS)**.
- **Citing the Kaspersky statistics:** many lecture slides (pp.9–21) are **image-only charts** (attacked resources/targets/duration/C&C distribution/frequency/types by country and quarter). Their *titles* are extractable but the **underlying numbers are in the graphics, not in text** — the one explicit figure the text gives is that **attacks shorter than 4h accounted for 60.65% of total duration in Q3 2022** (L06 p.12). Do not invent specific percentages from those chart slides.
- **"Layer 4 vs Layer 7," not "volumetric/protocol/application."** The slides use the OSI-layer framing (L06 p.23). If the exam asks in the lecture's own terms, answer with Layer 4 / Layer 7.
