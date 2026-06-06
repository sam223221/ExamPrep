# 00. Course Overview & Map

> This is the front door to the study guide. Read it first. It explains what the Cybersecurity course (F26, SDU Centre for Industrial Software) is about, summarizes all twelve topics, shows how they fit together as a single offensive-and-defensive story, and tells you which chapter to open when the exam asks about a given thing. Every claim here is a roll-up of the twelve per-topic chapters (`01`–`12`) in this folder — consult them for the grounded detail and citations.

---

## What This Course Is About

This is a hands-on, lab-driven cybersecurity course that teaches you to think like both an attacker and a defender — the stated goal is to build strong **"purple teams"** that combine the offensive "red" mindset with the defensive "blue" one (chapter 01). It opens with the foundational vocabulary and worldview of the field: what cybersecurity *is* (protecting networks, systems, programs, and above all **data** — at rest, in transit, and processed — from unauthorized access, modification, and deletion), why security keeps failing ("a fundamental failure of architecture"), and the **CIA triad** (Confidentiality, Integrity, Availability) that every later topic circles back to. From the very first lecture you stand up a virtualized lab — a **Kali Linux** attacker machine and two intentionally vulnerable targets (**Metasploitable 2** on Linux, **Metasploitable 3** on Windows) — because the course is built on six graded hand-in exercises, and the written exam is built directly on those exercises.

The middle of the course walks the **full offensive workflow** end to end and then pivots to **defense**. On the offensive side you learn reconnaissance and vulnerability assessment (mapping hosts, ports, and service versions with Nmap, Nessus, and OpenVAS/GVM), penetration testing (proving vulnerabilities are real with Netcat shells, the Metasploit Framework, and MSFvenom payloads), and the major exploitation classes: malware and SQL injection, denial of service, and social engineering / phishing. On the defensive side you study firewalls and intrusion detection/prevention systems, cryptography (symmetric and public-key, with by-hand RSA and ElGamal), secure multi-party computation, privacy and the GDPR, and threat modeling — the structured discipline of finding security problems by design rather than after a breach. Threat modeling effectively bookends the technical content (an introductory pass and an applied Kubernetes pass), tying the offensive knowledge back into a defensive engineering process.

The throughline is that **offense informs defense**. You learn how attackers find and exploit weaknesses precisely so you can model, prevent, detect, and respond to those attacks — and you learn the cross-cutting ideas (the CIA triad, defense in depth, the human factor, "keep your systems updated," least privilege) that recur in nearly every lecture. The course is graded by a written exam (MCQ/MAQ + short-answer, 50 questions, 2.5 hours) drawn from the slides and the labs the lecturer explicitly flagged for practice: **Labs 2, 3, 5, 6, 8, and 9** (chapter 12).

---

## The 12 Topics at a Glance

| # | Topic | One-line summary | Key skills |
|---|-------|------------------|------------|
| 01 | **Introduction & Set-up** | What cybersecurity is, the core vocabulary and CIA triad, and building the Kali + Metasploitable virtual lab. | CIA triad; risk/vuln/threat/exploit/attack terms; attack surface & vectors; VirtualBox networking modes (NAT vs NAT Network); Kali/Linux basics |
| 02 | **Vulnerability Assessment** | Discover hosts, ports, services, and versions and map them to known vulnerabilities — without exploiting. | Passive vs active recon; whois/DNS; **Nmap** scan types (SYN/Connect/FIN, `-sV`, `-O`); Nessus & OpenVAS/GVM; authenticated scans; CVE-based severity |
| 03 | **Penetration Testing** | Authorized simulated attack that *proves* vulnerabilities are exploitable, end to end. | Hat taxonomy & ethics; pentest methodology; Netcat bind/reverse shells; **Metasploit** (auxiliary→exploit→post); RHOST/LHOST; **MSFvenom** + multi/handler |
| 04 | **Firewalls & IDS** | Perimeter control (what traffic is allowed) and monitoring (spotting/reacting to malicious activity). | Firewall types by OSI layer; ACLs & default-deny; stateful vs static; IDS taxonomy; misuse vs anomaly; passive IDS vs reactive IPS; honeypots; password cracking (bcrypt) |
| 05 | **Malware & SQL Injection** | How malware propagates/hides and how unsanitized input lets an attacker rewrite SQL queries. | Virus vs worm; virus taxonomy; ransomware/Trojan/spyware/rootkit; signature vs heuristic detection; `1=1` & UNION SQLi; prepared statements & least privilege |
| 06 | **Denial of Service** | Make a service unreachable by exhausting a finite resource; the Availability attack. | DoS vs DDoS & botnets/C&C; SYN flood & the half-open buffer; Smurf/PoD/Teardrop/Land; SYN/RST cookies; Layer 4 vs 7; reverse proxies; resource-exhaustion lab; brute force |
| 07 | **Social Engineering** | Attack the human, not the machine — phishing, pretexting, and persuasion. | SE methods (digital/physical); attack lifecycle & OSINT; persuasion tactics; phishing mechanisms; SMTP spoofing & **SPF/DKIM/DMARC**; URL tricks; SET & GoPhish |
| 08 | **Threat Modeling I** | A structured, design-time process to find security issues before they ship. | Model→Find→Address→Validate; **DFDs** & trust boundaries; **STRIDE**; attack trees; mitigate/eliminate/transfer/accept; DREAD & risk matrices |
| 09 | **Cryptography** | Protect the message itself: symmetric and public-key encryption. | SKE vs PKE; substitution ciphers; DES/AES facts; One Time Pad & perfect secrecy; **RSA** and **ElGamal** by hand; modular exponentiation; standardization |
| 10 | **Multi-Party Computation** | Jointly compute on private inputs while revealing only the result. | Secret sharing (XOR/additive/Shamir); secure XOR (free) vs AND (needs comms); **Beaver triples**; semi-honest vs malicious; output-implied leakage; MPC-as-a-service |
| 11 | **Privacy & the GDPR** | Privacy as a right and the GDPR obligations engineers must build for. | Privacy ≠ confidentiality ≠ data protection; lawful bases & Art. 5 principles; controller/processor; data-subject rights; **anonymization vs pseudonymization**; k-anonymity/ℓ-diversity; DPIA/DPO/72h breach |
| 12 | **Threat Modeling II + Revision** | Apply threat modeling end-to-end to a Kubernetes cluster; course revision & exam prep. | 4Cs of cloud-native security; K8s DFD & trust boundaries; **attack trees** (AND/OR); attack vectors & RBAC; K8s controls & hardening tools; exam logistics |

---

## How the Topics Connect

The course has a clear architecture: an **offensive arc**, a **defensive arc**, and a **framing layer** that wraps both. Almost every topic is a node on one of these arcs, and the arcs meet in the middle.

**Chapter 01 is the framing for everything.** It defines the assets we protect (networks, systems, programs, data), the goals (the CIA triad), the vocabulary (vulnerability → threat → exploit → attack → patch → countermeasure), the **attack surface** (the sum of attack vectors: network, machine, software, human), and it stands up the lab every later chapter uses. It also names the six "major activities of cybersecurity" — vulnerability assessment, penetration testing, threat modeling, security monitoring, incident response, hardening — which is essentially the course syllabus in miniature.

**The offensive arc (chapters 02 → 03 → 05/06/07) follows the attacker's path.** Vulnerability assessment (02) is pure reconnaissance and analysis: find the hosts, ports, services, and versions, and map them to CVEs — but it deliberately *stops before exploitation*. Penetration testing (03) picks up exactly where 02 stops, taking the same methodology (recon → threat modeling/scope → vulnerability analysis → **exploitation** → reporting) all the way through proving the weakness is real with Metasploit, shells, and payloads. The "sneak peek" of Metasploit at the end of chapter 02 is the literal bridge into chapter 03. From there the course drills into the major *exploitation classes* an attacker actually uses: **malware and SQL injection** (05, exploiting bad input handling and trust), **denial of service** (06, exhausting resources to attack Availability), and **social engineering** (07, attacking the human who has legitimate access). These four (05, 06, 07, plus the Metasploit exploitation of 03) are the "what can go wrong" catalogue.

**The defensive arc (chapters 04, 09, 10, 11, 08/12) answers each offensive move.** Firewalls and IDS/IPS (04) are the direct counter to network attacks and DoS — they control what traffic is allowed and detect/react to malicious activity (the SYN-flood and Smurf mitigations in chapter 06 lean directly on firewall/IPS concepts). Cryptography (09) defends the **data itself**, providing the confidentiality and integrity that firewalls and threat-modeling mitigations repeatedly call for (e.g., "cryptography is required over a network"). Multi-party computation (10) extends cryptography to let mutually distrusting parties compute on private data, and it reuses the One Time Pad idea from chapter 09. Privacy & the GDPR (11) is the legal-and-ethical defensive layer — it turns abstract security goals into concrete obligations (security of processing, breach notification, data minimization, privacy-by-design) and even has its own threat-modeling framework (LINDDUN). And **threat modeling (08 and 12) is the meta-defense** that organizes all of this: it is where the offensive knowledge gets *used* defensively. STRIDE's six categories are literally the CIA triad plus authentication, non-repudiation, and authorization; its attack trees encode the very attacks taught in 03/05/06/07; and chapter 12 applies the whole apparatus to a real Kubernetes cluster.

**Where they meet.** The arcs are two views of the same coin, and the course makes the link explicit in several places. Threat modeling appears *inside* the pentest methodology (03) as the scoping step, and again as its own discipline (08, 12). Social engineering (07) is framed both as an attack and as a form of penetration testing. The CVE/OWASP/CAPEC/Exploit-DB knowledge repositories introduced in chapter 01 are used offensively in 02/03 and defensively as attack libraries in 08. And "keep your systems updated," "least privilege," and "defense in depth" surface as both the lesson of specific attacks (06's recurring old bugs, 05's privilege-chaining lab) and as standing defensive principles. The student who has done the offensive arc can read an attack tree in chapter 12 and immediately name the mitigation — which is exactly the purple-team skill the course is built to produce.

---

## The Attacker's Workflow

If you thread the practical chapters together, you get a single kill-chain-style narrative. This is the consolidated walkthrough an attacker (or an authorized pentester) follows, with the chapter that covers each stage.

1. **Get authorization & set scope (ethics first).** Before anything, a white-hat tester gets permission and defines what the test covers — the "getting permission" and "threat modeling/scope" steps of the pentest methodology. Without this, the same actions are illegal (chapters 01 ethics, 03 methodology, 07 SE ethics).

2. **Reconnaissance — passive first.** Gather intel *without touching the target*: whois/DNS records, Netcraft/archive.org, Shodan, job ads, and OSINT on people and organizations. This is the stealthy, low-risk groundwork (chapter 02 passive scanning; chapter 07 OSINT/information gathering).

3. **Active scanning & enumeration.** Now probe the target: discover live hosts (NetDiscover), then map open ports, services, versions, and OS with **Nmap** (`-sS` stealthy SYN, `-sV` versions, `-O` OS, `-p-` all ports). Enumerate services and fingerprint them (chapters 02, 03).

4. **Vulnerability analysis.** Connect the discovered service/version intel to known weaknesses via CVE and Exploit-DB, and run automated scanners (**Nessus**, **OpenVAS/GVM**) — using authenticated scans where possible for deeper, local/config findings. Remember: *not every open port is a vulnerability*. Assessment ends here (chapter 02).

5. **Initial exploitation — get a foothold.** Cross the line from assessment to pentest: prove the weakness with a working exploit. Use **Metasploit** (auxiliary scanner → exploit module, e.g., vsFTPd 2.3.4 backdoor or EternalBlue), get a shell (Netcat bind/reverse shells, Meterpreter), or come in through an *application* bug — a **SQL injection** that escalates from reading records to dumping every credential (chapters 03, 05). The human path is equally valid: a **phishing** email or vishing/smishing call that harvests credentials or runs malware (chapter 07).

6. **Deliver a payload / weaponize.** Where needed, craft a custom payload with **MSFvenom** (e.g., a reverse-TCP Meterpreter EXE/ELF) and catch it with `multi/handler` — getting the victim to *run* it is the social-engineering/delivery problem (chapters 03, 07). **Malware** is the broader weaponization toolkit: Trojans, droppers, ransomware staging (chapter 05).

7. **Privilege escalation & post-exploitation.** Once inside, escalate (e.g., `sudo -s` to root, EoP exploits), then harvest: dump password hashes, enumerate users/processes/network, locate sensitive files, find persistence mechanisms, and assess **lateral movement**. The SQLi lab's chain — directory listing → unsanitized input → DB root with no password → broad `sudo` → host root → direct MySQL — is the canonical "one bug cascades into total compromise" story (chapters 03 post-exploitation, 05 lab chain).

8. **Impact / objective.** Depending on goal: exfiltrate or destroy data (SQLi `DROP TABLE`), deny service by exhausting resources (**DoS/DDoS** — SYN floods, HTTP floods, botnets), recruit the host into a botnet, or deploy ransomware. DoS specifically attacks **Availability** rather than stealing data (chapter 06).

9. **Report (the deliverable).** The legitimate workflow ends not with damage but with a report: an executive summary of business impact plus a technical write-up of critical vulnerabilities (root cause, method, impact, CVE, remediation). Assessment and pentest both culminate in reporting (chapters 02, 03).

The defender reads this same chain backwards: firewalls/IDS (04) catch stages 3–8 at the network, cryptography (09) blunts stage 8's data theft, threat modeling (08/12) anticipates the whole chain by design, and the GDPR (11) governs what happens when stage 8 succeeds (breach notification).

---

## Cross-Cutting Themes

A handful of ideas recur across nearly every chapter. Recognizing them is worth more on the exam than memorizing any single tool.

- **The CIA triad (Confidentiality, Integrity, Availability).** Introduced in chapter 01 as *the* security-goals model, it reappears everywhere: DoS is defined as an attack on **Availability** (06); cryptography provides **Confidentiality** and **Integrity** (09); SQLi and information disclosure break Confidentiality; **STRIDE** (08) is essentially the CIA triad expanded — Spoofing↔Authentication, Tampering↔Integrity, Repudiation↔Non-repudiation, Information Disclosure↔Confidentiality, DoS↔Availability, Elevation of Privilege↔Authorization; and the GDPR's Art. 5 "security of processing" principle is "integrity & confidentiality" (11).

- **Defense in depth (layered defense).** No single control is sufficient. Chapter 01 names it as a core countermeasure; firewalls + IDS + IPS + antivirus form layers (04, 05); the GDPR demands organizational *and* technical measures (11); the Kubernetes "4Cs" (Cloud/Cluster/Container/Code) are explicitly nested layers (12); and threat modeling's mitigate/eliminate/transfer/accept choices are layered defenses per threat (08).

- **The human factor.** People are the weakest link and hardest to "patch." Chapter 01 lists human factors as a root cause of insecurity; social engineering (07) is the entire chapter devoted to it; phishing appears as early as chapter 02; payload *delivery* in pentesting depends on tricking a user (03); and the GDPR frames data subjects as humans with rights (11). "Security as a secondary goal" is one of the GDPR's "seven privacy sins."

- **Keep your systems updated / patching.** A standing lesson: Ping of Death, Teardrop, and Land are old bugs that resurface (06); malware exploits unpatched systems (05); but Metasploitable targets are *deliberately* kept outdated for the lab (01). Patching closes vulnerabilities and prevents your machine becoming a botnet zombie.

- **Least privilege & access control.** A recurring mitigation: the SQLi lab's DB-root-with-no-password is the anti-pattern (05); RBAC mis-configuration is "many attack vectors" in Kubernetes (12); least privilege is an explicit SQLi defense (05) and an EoP mitigation (08); and access control is a CIA confidentiality mechanism (01).

- **Authorization, ethics, and the law.** Offensive skills are for authorized use only. The ethical statement and hat taxonomy (01, 03), Kant's categorical imperative (03), SE pen-test ethics (07), and the entire legal layer of GDPR (11) and NIS2 (03) all insist that *getting permission* is the line between white-hat and black-hat.

- **Find problems early / by design.** "Wouldn't it be better to find security issues before you write a single line of code?" Threat modeling (08, 12), secure-by-design (01), and privacy-by-design (11) all push security upstream rather than bolting it on after a breach.

- **Know your tooling and its limits.** Across chapters the message is consistent: tools (Nessus/GVM severity, automated phishing filters, signature scanners, k-anonymity) are useful but fallible — false positives/negatives abound, and human judgment (reviewing the CVE, verifying out-of-band, checking the math) is still required (02, 04, 05, 07, 11).

---

## Where to Look

A quick index — if the exam asks about **X**, open chapter **Y**.

- **CIA triad; risk vs vulnerability vs threat vs exploit vs attack; attack surface & vectors; the lab setup; VirtualBox networking (NAT vs NAT Network); Kali/Metasploitable credentials** → **01**
- **Nmap scan types and flags (`-sS`/`-sT`/`-sF`, `-sV`, `-O`, `-Pn`/`-sn`, `-p-`, timing `-T0..T5`); passive vs active scanning; whois/DNS; Nessus vs OpenVAS/GVM; authenticated scans; "is an open port a vulnerability?"; CVE/severity** → **02**
- **Pentest methodology & ethics; hacker hat colours; Netcat bind vs reverse shells; Metasploit module types & RHOST/LHOST; EternalBlue/vsFTPd backdoor; Meterpreter & post-exploitation; MSFvenom & multi/handler; lateral movement** → **03**
- **Firewall types by OSI layer; static vs stateful; ACLs & default-deny; circuit-level/application proxy; bastion host/DMZ/VPN; IDS vs IPS; misuse vs anomaly detection; honeypots; cracking a bcrypt hash (Hashcat/John, rockyou)** → **04**
- **Virus vs worm; virus taxonomy (macro/polymorphic/armored…); ransomware/Trojan/spyware/rootkit; signature vs heuristic detection; SQL injection (`1=1`, UNION, batch/DROP); SQLi defenses (prepared statements, least privilege); dirb/nikto/sqlmap; the DVWA→root lab chain** → **05**
- **DoS vs DDoS; botnets/C&C/zombies; SYN flood & half-open buffer; Smurf/Ping of Death/Teardrop/Land; SYN cookies/RST cookies/stack tweaking; Layer 4 vs Layer 7; Slowloris; LOIC/HOIC/TFN; reverse proxies (Cloudflare); resource-exhaustion lab; brute force / Hydra / fork bomb** → **06**
- **Social engineering methods (digital/physical); attack lifecycle & targeting; OSINT; pretexting & persuasion tactics; phishing mechanisms (credential/malware/CEO fraud); SMTP spoofing; SPF vs DKIM vs DMARC; URL-disguising tricks; vishing/smishing; SET & GoPhish** → **07**
- **Threat-modeling process (Model→Find→Address→Validate); DFDs & trust boundaries; STRIDE & its property mapping; attack trees; mitigate/eliminate/transfer/accept; DREAD & risk matrices; "think like an attacker" caveats** → **08**
- **Symmetric vs public-key; substitution ciphers (Caesar/Vigenère/Enigma); DES vs AES facts; One Time Pad & perfect secrecy; RSA by hand (`m^e mod n`); ElGamal by hand; modular exponentiation; brute-force time estimates; standardization (FIPS/NIST)** → **09**
- **Secure multi-party computation; secret sharing (XOR/additive/Shamir); secure XOR (free) vs AND (needs comms); Beaver/multiplication triples; semi-honest vs malicious adversaries; output-implied leakage; millionaires' problem; MPC-as-a-service** → **10**
- **Privacy vs confidentiality vs data protection; GDPR lawful bases (Art. 6); Art. 5 principles; controller vs processor; data-subject rights (R1–R10); personal vs sensitive data; anonymization vs pseudonymization; k-anonymity/ℓ-diversity; DPIA/DPO; 72-hour breach notification; privacy-by-design/LINDDUN** → **11**
- **Applied threat modeling on Kubernetes; the 4Cs; K8s DFD & trust boundaries; attack trees (AND vs OR nodes); K8s attack vectors & RBAC; K8s security features & hardening; security tooling (kube-bench/Clair/Kubescape/Notary); exam logistics & what to revise** → **12**

> **Exam strategy reminder (from chapter 12):** the exam is 50 questions (35 MCQ/MAQ + 15 short-answer, 2.5 hours), drawn from the slides and exercises. The lecturer explicitly flagged **Labs 2, 3, 5, 6, 8, and 9** for practice — Vulnerability Assessment, Penetration Testing, Malware & SQLi, Denial of Service, Threat Modeling I, and Cryptography. Master the four-step threat-modeling process and AND/OR attack-tree reading, the CIA→STRIDE mapping, and be able to *do* the Nmap scans, the SQLi payloads, and the RSA/ElGamal arithmetic by hand.

---

*End of overview. Continue to chapter 01 for the foundations, or jump straight to the chapter the index above points you to.*
