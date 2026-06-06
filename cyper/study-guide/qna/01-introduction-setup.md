# 01. Introduction & Set-up — Simulated Open-Book Questions

### [EASY] A hospital encrypts patient records on disk so that only authorized clinicians can read them. Which CIA pillar does this primarily serve, and name one other mechanism the chapter pairs with that same pillar.
**Answer:** This primarily serves **Confidentiality** — preventing the disclosure of information to unauthorized parties (L01 p.27). Encryption is one of the three mechanisms the slides pair with confidentiality. The other two paired mechanisms are **access control** and **authentication** (L01 p.27).

So a complete answer is: pillar = Confidentiality; encryption is in use; another valid confidentiality mechanism is access control (or authentication). Note that you should not pair encryption with integrity here — the chapter explicitly pairs integrity with **signatures/checksums** instead (L01 p.27), and mixing the pairings up is a flagged gotcha.

### [EASY] You are told "a SQL injection flaw exists in the login form." Using the chapter's vocabulary, is that flaw a vulnerability, a threat, an exploit, or an attack? Justify your choice.
**Answer:** It is a **vulnerability** — "a weakness in a system" (L01 p.35). The SQL injection flaw is the hole/weakness itself; it exists whether or not anyone ever uses it.

For contrast (L01 p.35):
- A **threat** would be the *potential* circumstance that someone could take advantage of that flaw.
- An **exploit** would be the *method/technique* used to abuse it (e.g., the crafted injection string).
- An **attack** would be the *action* of actually submitting that string to compromise the system.

So "a flaw exists" = vulnerability; the other three describe potential, technique, and action respectively.

### [EASY] In the VirtualBox connectivity table, which single networking mode allows VM↔Host, VM1↔VM2, VM→Internet, AND VM←Internet (all four)? State the security caveat the chapter gives for it.
**Answer:** The mode is **Bridged**, which is the only row that is "Yes" across all four columns: VM↔Host = Yes, VM1↔VM2 = Yes, VM→Internet = Yes, VM←Internet = Yes (L01 p.41, E01 p.7).

The caveat: in Bridged mode the VM becomes a node on the local network, and **packet sniffing on the host interface is possible** (L01 p.41). Because the VM is fully exposed to (and from) the real network — including the open Internet — this is a poor choice for the intentionally vulnerable Metasploitable targets, which the chapter insists must be isolated (E01 p.1, p.5).

### [EASY] A student deletes a file from Kali with `rm notes.txt` but actually needed to remove a whole directory `loot/` and all its contents. What single command does the chapter give for that, and what does the `-r` flag do?
**Answer:** The command is:

```
rm -r loot/
```

Per L01 p.45, `rm -r directory` **recursively removes a directory and its sub-directories** (and the files inside them). Plain `rm file` only removes individual files, which is why it failed for a directory. The `-r` (recursive) flag tells `rm` to descend into the directory tree and delete everything under it.

### [EASY] On the attacker machine you need to find out what IP address the system currently has so you can compare it with the target's IP. Which command(s) from the chapter return the IP address?
**Answer:** The chapter lists three equivalent forms (L01 p.45):

```
ip address
ip addr
ip a
```

All three return the IP address on Kali. In the connectivity-verification recipe, Kali's IP is found with `ip addr` (look at `eth0 inet`, e.g., `192.168.64.y`), which you then compare against the Metasploitable target's IP found via `ifconfig` (eth0 inet) before running `ping` (E01 p.9, MAC p.1). If you cannot read the IP directly, `sudo arp-scan -l` can discover hosts on the local network (SOL p.1).

### [MEDIUM] An online banking provider lets customers transfer money. Map each of the three CIA pillars to one concrete banking failure: a customer's balance being altered without authorization, the bank's website being knocked offline, and an attacker reading another customer's statements. Name the matching mechanism the chapter pairs with each pillar.
**Answer:** Mapping each failure to a pillar (L01 p.26–27):

- **Balance altered without authorization → Integrity.** Integrity is protecting information from modification by unauthorized parties. Paired mechanisms: **digital signatures, checksums** (so a tampered transaction record can be detected).
- **Website knocked offline → Availability.** Availability is ensuring authorized parties can access information when needed. Paired mechanisms: **computational redundancy, backups, mitigation strategies** (e.g., redundant servers to absorb a denial-of-service).
- **Reading another customer's statements → Confidentiality.** Confidentiality is preventing disclosure to unauthorized parties. Paired mechanisms: **encryption, access control, authentication**.

This also lines up with the asset-protection framing: unauthorized modification ↔ integrity, unauthorized deletion/loss-of-access ↔ availability, unauthorized access ↔ confidentiality (L01 p.25, p.63 mapping in the guide).

### [MEDIUM] A phishing email with a malicious attachment is sent to an HR clerk, who opens it and gives the attacker a foothold. Classify the attack vector category, and explain the chapter's point that "no vulnerability is needed" for some access.
**Answer:** The attachment-laden phishing email targets a person, so the attack vector category is **Human** — one of the four categories (Network, Machine/physical, Software, Human) that sum to the attack surface (L01 p.32). The chapter explicitly notes that **social engineering is often a first step** — "an email to all/selected employees with or without crafted attachments" (L01 p.34).

The "no vulnerability is needed" point: depending on the *kind of access*, an attacker may not need a software vulnerability at all (L01 p.34). With direct access — for example physical access, or a user who is tricked into voluntarily running an attachment — the attacker bypasses the need to find and exploit a technical flaw. Here the human is manipulated into granting the foothold, so the compromise rides on social engineering rather than on exploiting a code-level vulnerability.

### [MEDIUM] A student configures all three lab VMs (Kali, Metasploitable 2, Metasploitable 3) in plain NAT mode and is surprised that `ping` from Kali to Metasploitable 2 fails, even though all three reach the internet. Diagnose the problem and give the fix.
**Answer:** This is the classic **NAT ≠ NAT Network** trap (L01 p.41; E01 p.4, p.7). In **plain NAT**, each VM is hidden behind the host and **VMs cannot communicate with each other** (VM1↔VM2 = No), even though each individually has outbound internet (VM→Internet = Yes). That is exactly why all three can reach the internet but Kali cannot ping the target.

**Fix:** switch every lab VM to **NAT Network**, where VMs on the same network *can* communicate (VM1↔VM2 = Yes), still get DHCP-assigned IPs, and keep internet access (L01 p.41, E01 p.7). Concretely:

1. Power off the VMs (you cannot change a network adapter on a running VM) (E01 p.8).
2. Create a NAT Network (e.g., `NatNetwork`) with DHCP enabled (E01 p.8).
3. For each VM: `Settings → Network → Attached to = NAT Network`, `Name = NatNetwork`, all on the **same** network.
4. Boot and re-test with `ping <target_IP>`.

### [MEDIUM] A teammate insists on running the Metasploitable 2 target under WSL 2 on their work laptop "because it's faster." Give two reasons from the chapter to push back, and one practical requirement if they ignored the warning.
**Answer:** Two reasons to push back (E01 p.2, p.8):

1. **Weak isolation.** WSL (especially WSL 2, which runs a real Linux kernel) is **tightly integrated with the host Windows system**, which reduces isolation between the attacking/target environment and the user's primary work system. Running an intentionally vulnerable, untrusted machine like Metasploitable that close to a production work laptop is exactly the scenario the chapter says to avoid — these VMs must be treated as hostile and kept strictly isolated (E01 p.1, p.5).
2. **Strongly discouraged by the course.** The chapter states outright that running the Metasploitables under WSL is *strongly discouraged*, and that a dedicated virtualization solution provides significantly better isolation and security (E01 p.2, p.8).

Practical requirement if ignored: for WSL 2 to even reach the Metasploitable VMs, **Host-Only Networking** is required (E01 p.8).

### [MEDIUM] During the major-activities discussion, a manager asks which activity is "ethical hacking to find exploitable weaknesses" versus which is just "finding weaknesses." Distinguish the two and name the course tools associated with finding weaknesses (vulnerability assessment).
**Answer:** The two activities are distinct (L01 p.21):

- **Vulnerability Assessment** = *finding weaknesses*. It catalogs/identifies weaknesses but does not necessarily prove they can be exploited.
- **Penetration Testing** = *ethical hacking to find exploitable weaknesses*. It goes further by actually attempting to exploit the weaknesses to demonstrate impact.

So the difference is identify-only (assessment) versus actively-exploit-to-prove (pen testing).

Course tools listed under **Vulnerability Assessment** (L01 p.9): **Nessus, OpenVAS / Greenbone, and Rapid7 InsightVM** (formerly Nexpose). (By contrast, pen-testing tools include Nmap, Netcat, Metasploit Framework, Burp Suite, Wireshark, etc.)

### [HARD] A company's risk register lists, for one system: an unpatched Apache service (entry A), the published Metasploit module that abuses it (entry B), the possibility that an internet-based group decides to target the company (entry C), and the actual intrusion that occurred last Tuesday (entry D). Label A–D with the chapter's terms and state what a patch and a countermeasure each neutralize.
**Answer:** Labelling each entry against L01 p.35:

- **A — Vulnerability.** The unpatched Apache service is "a weakness in a system."
- **B — Exploit.** The published Metasploit module is "a method of taking advantage of a vulnerability." It is the technique/tooling, not the act.
- **C — Threat.** An internet-based group that *could* decide to target the company is "a circumstance/event that has the potential to exploit a vulnerability." It is potential, not action.
- **D — Attack.** Last Tuesday's actual intrusion is "an action that uses a threat to exploit a vulnerability."

What each defense neutralizes (L01 p.35):
- A **patch** is "a fix for a vulnerability" — it removes/neutralizes **A** (the weakness). Once A is patched, exploit B has nothing to act on.
- A **countermeasure** is "a means of preventing an attack" — it is aimed at stopping **D** (the attack) and, by extension, frustrating the threat C from succeeding even if the vulnerability has not yet been patched.

The trap here is swapping B and C (exploit vs threat) — the exploit is the *method*, the threat is the *potential actor/event* (a flagged gotcha).

### [HARD] A student building the "advanced" lab topology wants the targets isolated from the wider network but still wants Kali to reach the internet for updates. Describe the configuration the chapter recommends, why it beats plain NAT Network for this goal, and the DHCP option it suggests.
**Answer:** The recommended advanced configuration is **Internal Network + NAT (Advanced Setup)**: combine **Internal Networking** for inter-VM communication with a **separate NAT adapter** for controlled internet access (E01 p.7–8). Kali gets a second adapter (NAT) so it can still run `sudo apt update`/`full-upgrade`, while the inter-VM traffic rides the isolated Internal network.

Why it beats plain **NAT Network** for isolation (E01 p.7–8):
- NAT Network is the *simple* setup — it gives internet + automatic DHCP + communication between **all** VMs on the network, but its downside is **limited control over which machines can communicate** (it is "easy but leaky").
- Internal + NAT lets you **restrict communication to selected VMs**, **better isolate the vulnerable targets**, and **model realistic topologies**. Since Metasploitables are deliberately vulnerable and must be treated as hostile (E01 p.1, p.5), this stronger isolation is the whole point — the trade-off is functionality/convenience vs. isolation/realism.

DHCP option suggested (E01 p.9): rather than static IPs or a DHCP server on Kali, **enable a VirtualBox DHCP server** for the internal network (the recommended option), e.g. via `VBoxManage dhcpserver add --network=CyberSecLab ...` assigning from the `172.30.1.0/24` range. (Watch the flagged `--upperip 171.30.1.50` typo — it should be `172`.)

### [HARD] Analyze the "Defense in Depth and Attack Surface" slide as a small system: a SaaS vendor exposes a web API, opens an SSH port for admins, and leaves a USB port active on the rack server. For each interface, give its attack-vector category, and explain the opposing goals of attacker, operator, and designer for this surface.
**Answer:** Each interface maps to an attack-vector category (the four are Network, Machine/physical, Software, Human — L01 p.32):

- **Web API** → primarily **Software** (and **Network**, since it is reached over the network). It is application code exposed for access.
- **SSH port for admins** → **Network** (a network-reachable service/end point).
- **Active USB port on the rack server** → **Machine (physically)** — physical access to the device.

Each of these is an attack vector, and **Attack Surface = Σ of Attack Vectors** (L01 p.32), so all three add to the total exposed surface.

Opposing goals of the three entities around that surface (L01 p.33):
- **Attacker** — wants to *expand* the exposed interface (find/enlarge more vectors, e.g., abuse the USB or a forgotten API endpoint).
- **Operator** — wants to *limit* the surface open to attacks (e.g., close the USB port, restrict SSH to a bastion, minimize exposed API).
- **Designer** — should design the system accordingly, i.e., to meet the operators' requirements for a minimal surface (build it so the operator *can* keep the surface small).

This is the defense-in-depth framing: layered, intentional reduction of the summed attack vectors.

### [HARD] A student successfully imports Kali and Metasploitable 2 but their downloaded Metasploitable 3 archive will not appear in VirtualBox's import dialog. Walk through the chapter's expected cause and the exact fix, including a trap to avoid.
**Answer:** Expected cause (E01 p.6): the extracted Metasploitable 3 file is **technically a tar archive** with no extension VirtualBox recognizes. VirtualBox filters importable files by extension, so the file simply does not show up in the import list.

Exact fix (E01 p.6):
1. **Rename the extracted file to end in `.ova`.** This makes VirtualBox recognize it (it lists `.ova` automatically). Alternatively, clear/disable the file-type filter in the import dialog and select the file manually.
2. Import using the same `File → Import Appliance` procedure as Metasploitable 2.
3. Log in with default credentials `vagrant` / `vagrant`.

Trap to avoid (flagged gotcha, E01 p.6): **do not rename it to `.ova.gz`.** That makes the file *appear* in the list, but VirtualBox will **refuse to complete the import** — it looks like progress but fails. Use `.ova`, not `.ova.gz`.

(Bonus pitfall from the same recipe: a Vagrant-based install may throw a plugin error fixable by changing `File.exists` to `File.exist` on line 84 of `virtualbox.rb`; a `MountDiskImage` error can be ignored.)

### [HARD] During a CTF-style class exercise, a student boasts they scanned a classmate's personal laptop "to practice." Using the chapter's ethics/authorization stance, explain why this is unacceptable and what the student was actually supposed to do, plus the legal frameworks cited.
**Answer:** The chapter's ethics stance is explicit (L01 p.10): knowledge and skills are **solely for educational purposes**; **any unauthorized access, manipulation, or misuse of data/systems is prohibited**; participants must uphold cybersecurity ethical standards; and each student is **responsible for their own actions**. Scanning a classmate's personal laptop is **unauthorized access against a system the student has no permission to touch** — it is not the sanctioned lab target, so it violates every one of those points regardless of intent to "practice."

What the student *should* do: practice only inside the **isolated, sanctioned lab** — Kali attacking the **intentionally vulnerable Metasploitable 2/3 targets** the course provides (L01 p.40, E01 p.5). Those machines exist precisely so skills can be exercised legally and safely; the classmate's laptop does not. The student must also have **signed the Ethical Statement Form in ItsLearning** acknowledging exactly this (L01 p.10).

Legal frameworks cited (L01 p.38): the **Computer Security Act of 1987 & 1992**, **OMB Circular A-130**, **US state computer laws**, **HIPAA (1996)**, and the **EU GDPR (2018)** — several of which can make unauthorized scanning/access a legal offence, not merely a course violation.

### [VERY HARD] Two teammates set up the lab on different hosts: Alice on an Intel laptop using VirtualBox + NAT Network, Bob on an Apple Silicon MacBook. Both run `ping` from Kali to Metasploitable. Predict whose setup is more likely to "just work," explain the architectural reason Bob struggles, and give Bob a viable path that still lets him reach a working Metasploitable target.
**Answer:** **Alice's setup is more likely to just work.** Intel/AMD systems support x86 natively, so the x86 Metasploitable images run with no architecture problem, and NAT Network gives Kali↔Metasploitable connectivity by design (E01 p.3; L01 p.41). Her `ping` should succeed once both VMs are on the same NAT Network with DHCP.

**Why Bob struggles — the architectural reason:** the NextCloud/Metasploitable images are built for **amd64/x86**, but Apple Silicon (M1/M2/M3) is **ARM**. Kali has ARM builds that run efficiently, but **equivalent ARM Metasploitable images are not readily available**, so the x86 Metasploitable image is **not natively compatible** with Bob's ARM CPU (E01 p.2–3). Without emulation there is no running x86 target for Kali to ping.

**Viable paths for Bob** (E01 p.3; MAC p.1; SOL p.1):
1. **Hardware emulation of x86** — run the x86 VMs under emulation (reduced performance). The Mac follow-up recommends **UTM instead of VirtualBox**, using `brew` + **QEMU** to convert images: `qemu-img convert -p -f vmdk -O qcow2 <file>.vmdk <file>.qcow2`, then create an emulated `x86_64` VM in UTM. Metasploitable 3 may need the SOL-doc fix (uncheck UEFI Boot; delete the VBox guest-addition drivers) to stop crashing, after which it runs keyboard-only.
2. **Team up** with someone on an Intel/AMD machine (i.e., use Alice's host).
3. **Use a cloud-based solution.**

After emulating, Bob verifies the same way as Alice: `ifconfig`/`ip addr` to get IPs, then `ping`; if the target IP is hard to read, `sudo arp-scan -l` from Kali finds it (often around `192.168.64.10`).

### [VERY HARD] A student argues: "We should patch and fully update the Metasploitable targets just like we update Kali — keeping software current is best practice (defense-in-depth)." Critique this using the chapter, distinguishing where 'keep current' applies versus where it deliberately does not, and tie it to the CIA/attack-surface rationale of the lab.
**Answer:** The student is conflating two machines with **opposite roles**, and the chapter handles them differently (L01 p.44; E01 p.5):

- **Kali (the attacker/toolbox)** — you *do* keep it current: `sudo apt update; sudo apt full-upgrade -y` (and `apt autoremove` when suggested). Updating Kali keeps your tooling working and your own attacking environment secure. Here "keep current / defense-in-depth" genuinely applies.
- **Metasploitable 2/3 (the targets)** — you *deliberately do NOT patch them*. The course says to keep them "**as outdated as they were designed**" (L01 p.44). Patching them would close the very vulnerabilities that the six graded hands-in exercises (and therefore the exam) depend on. They exist **intentionally vulnerable** for practice (E01 p.5).

So "keep current is always best practice" is a category error: best-practice patching applies to systems you are *defending*, not to a lab target whose entire purpose is to be exploitable.

The CIA/attack-surface tie-in: in the *real* world, patching is a countermeasure/hardening step that shrinks the attack surface and protects the CIA triad of production systems. In the lab, the Metasploitables are **not** production assets to protect — they are deliberately broken practice rigs, treated as **hostile and isolated** from the host and production networks (E01 p.1, p.5). The correct way to honor defense-in-depth here is not to patch the targets but to **isolate** them (e.g., Internal + NAT), so their large, intentional attack surface cannot leak onto real networks. Real defense-in-depth is applied to the *boundary around* the lab, while the targets themselves stay vulnerable by design.

### [VERY HARD] Reconcile two statements from the chapter that seem to conflict: (1) "no vulnerability is needed" for some access, and (2) the formal definitions where an attack "uses a threat to exploit a vulnerability." Use a physical-access and a social-engineering example, and explain what this implies for an organization's attack-surface defense.
**Answer:** The two statements operate at **different scopes**, so they do not actually conflict.

Statement (2) — "an attack is an action that uses a threat to exploit a vulnerability" (L01 p.35) — is the formal definition in the *technical/software* sense: a software-level weakness being abused. Statement (1) — "depending on the kind of access, no vulnerability is needed; social engineering is often a first step" (L01 p.34) — broadens what counts as a way in. The reconciliation: the **vulnerability being exploited may be human or physical, not just a software flaw.** The four attack-vector categories are **Network, Machine (physical), Software, Human** (L01 p.32) — software is only one of four.

- **Physical-access example:** an attacker walks up to an unlocked rack and copies data off it. No software exploit is required, but the "weakness" is still real — it is a **Machine (physical)** vector. Direct physical access is the path; the missing physical control (open USB / unlocked rack) is the weakness.
- **Social-engineering example:** an attacker emails a clerk a crafted attachment and the clerk runs it (L01 p.34). No code vulnerability is needed; the **Human** vector is the weakness — the person is manipulated into granting access.

What this implies for attack-surface defense: because **Attack Surface = Σ of Attack Vectors** across all four categories (L01 p.32), defending only the *Software* and *Network* vectors (patching, firewalls) leaves the **Human** and **physical** vectors wide open. A defender who equates "vulnerability" purely with software bugs will under-count the surface. True surface reduction (the operator's goal of *limiting* the surface, L01 p.33) and defense-in-depth must therefore also cover physical controls and human factors (training and awareness, a named counter at L01 p.20) — not just patches.

### [VERY HARD] A lab group must justify their network design choice in a one-paragraph rationale. They will run Kali plus both Metasploitables and want (a) inter-VM attacks to work, (b) internet for Kali updates, (c) the strongest isolation of the vulnerable targets from the host/production LAN. Compare all five VirtualBox modes against these three requirements and recommend a design with reasoning.
**Answer:** Evaluating each mode against (a) inter-VM, (b) internet for Kali, (c) isolation from host/production (L01 p.41; E01 p.7):

- **Bridged** — (a) Yes, (b) Yes, but **fails (c)**: the VM is a full node on the real LAN and is reachable *from* the internet (VM←Internet = Yes), exposing the hostile targets to production. Reject.
- **Host-Only** — (a) Yes inter-VM and VM↔Host = Yes, but (b) **No internet** (VM→Internet = No), so Kali can't update; and VM↔Host = Yes weakens host isolation. Fails (b).
- **Internal** — (a) Yes inter-VM, (c) strongest isolation (No host, No internet — VMs are fully sealed), but (b) **No internet** on its own. Meets (a) and (c) but not (b) by itself.
- **NAT (plain)** — (b) Yes internet, but (a) **No inter-VM** (VM1↔VM2 = No), so Kali can't reach the targets. Fails (a) — the classic trap.
- **NAT Network** — (a) Yes, (b) Yes, partial (c): isolates from the host (VM↔Host = No) and inbound needs port forwarding, but its weakness is **limited control over which machines can communicate** — it is "easy but leaky" (E01 p.7).

**Recommendation — Internal Network + a separate NAT adapter on Kali (the Advanced Setup):** put all three VMs on a shared **Internal** network to satisfy (a) inter-VM attacks with the strongest isolation (c) — the targets touch nothing but the sealed Internal net — and give **only Kali a second NAT adapter** for (b) internet updates. This is exactly the chapter's Advanced Setup, preferred "when working with untrusted VMs or when stronger isolation is required," letting you restrict communication to selected VMs and isolate the deliberately vulnerable targets (E01 p.7–8). Use a VirtualBox DHCP server on the Internal network for automatic IPs (E01 p.9). If the group instead just needs to get running fast and accepts the leak, plain **NAT Network** is the simple fallback that still meets (a) and (b) (E01 p.7) — but it does not give the strongest isolation the group asked for in (c).

### [VERY HARD] An auditor is handed the lab's advanced DHCP recipe and told to "run it exactly as written." The command sets `--lowerip 172.30.1.20` and `--upperip 171.30.1.50` on `--netmask 255.255.255.0` with `--ip 172.30.1.1`. Predict what goes wrong if run verbatim, explain why, correct it, and state the broader lesson about trusting course materials.
**Answer:** **What goes wrong:** run verbatim, the DHCP server is almost certainly broken/inconsistent because the **lower and upper bounds of the pool are not in the same /24 subnet**. `--lowerip 172.30.1.20` sits in `172.30.1.0/24`, but `--upperip 171.30.1.50` sits in `171.30.1.0/24` — a completely different network (the second octet differs: `172` vs `171`). With `--netmask 255.255.255.0` and the server `--ip 172.30.1.1`, the gateway/server and the pool's lower bound are on `172.30.1.0/24`, while the upper bound points into `171.30.1.0/24`, so the range is invalid or the VMs cannot get a usable, routable lease on the intended `CyberSecLab` internal network (E01 p.9).

**Why:** a DHCP pool must lie within a single subnet defined by the netmask. A /24 mask freezes the first three octets; changing the second octet (`172`→`171`) leaves the subnet, so `--lowerip` and `--upperip` no longer bracket a coherent address range.

**Correction:** change the `171` to `172` so the whole range is inside `172.30.1.0/24`:

```
VBoxManage dhcpserver add \
   --network=CyberSecLab \
   --lowerip 172.30.1.20 \
   --upperip 172.30.1.50 \
   --netmask 255.255.255.0 \
   --ip 172.30.1.1 \
   --enable
```

**Broader lesson:** the chapter itself flags this as "almost certainly a typo in the lab" and deliberately leaves it *visible* rather than silently fixing it (E01 p.9, and the matching Gotcha). The lesson is that **course slides/labs contain errors** — the guide also notes spelling slips like "Burp Suit" for Burp Suite and "Social Engineer Toolset" for the Social-Engineer Toolkit (L01 p.9), and the `.ova` vs `.ova.gz` import trap (E01 p.6). An auditor (or exam student) must apply judgment and verify commands against the intended subnet/behaviour, not reproduce material blindly just because it is "official."
