# 01. Introduction & Set-up

> Sources for this chapter: `L01_Introduction.pdf` (46 pages, lecture slides), `E01.pdf` (9 pages, Lab 01 instructions), `labsetup4mac.pdf` (1 page, Apple Silicon setup), `solution4metasploitable3.pdf` (1 page, Metasploitable 3 on UTM fix). Course: Cybersecurity F26, SDU Centre for Industrial Software (CIS), taught by Sani Abdullahi and Hiraku Morita. Citations use `(L01 p.X)`, `(E01 p.X)`, `(MAC p.1)`, `(SOL p.1)`.

---

## Overview — what this topic covers and why it matters

This first chapter sets up the whole course. It has two halves. The **conceptual half** introduces what cybersecurity *is* — the body of technologies, processes and practices that protect networks, computers, programs, digital assets, and data (whether processed, stored, or in transit) from attack, damage, or unauthorized access (L01 p.22). It frames *why* security keeps failing ("a fundamental failure of architecture", security not considered early in software design), what we protect (networks, systems/devices, programs, and most importantly data), the goals we protect for (the CIA triad), the idea of the **attack surface** as the sum of attack vectors, and the core vocabulary (risk, vulnerability, threat, exploit, attack, patch, countermeasure) (L01 p.18–35).

The **practical half** is the lab environment that every later lecture and the six graded hand-in exercises build on. You stand up a virtualized network in VirtualBox containing one **attacker** machine (Kali Linux) and two intentionally vulnerable **target** machines (Metasploitable 2 on Linux, Metasploitable 3 on Windows), connect them so they can talk to each other, and learn the basic Linux commands and tooling you will use throughout (L01 p.39–45, E01 p.1–9). This matters because the written exam is built directly on the six hands-in exercises (L01 p.11), so the lab is not optional scaffolding — it is the exam material. The chapter also stresses **ethics**: all skills are for educational purposes only, unauthorized access is prohibited, and you must sign the Ethical Statement Form (L01 p.10).

---

## Key Concepts

### What cybersecurity is (and how it relates to information security)

Cybersecurity is defined in the lecture as "the body of technologies, processes and practices designed to protect networks, computers, programs, digital assets, and data (processed, stored and/or in transit) from attack, damage or unauthorized access" (L01 p.22). The slides also give the NIST formal definition: "Measures and controls that ensure confidentiality, integrity, and availability of information system assets including hardware, software, firmware, and information being processed, stored, and communicated" — from NIST Internal/Interagency Report NISTIR 7298 Rev. 3, the Glossary of Key Information Security Terms, July 2019 (L01 p.23). The slides present **Information Security** and **Cyber Security** as related/overlapping ideas (L01 p.22) but do not give a precise boundary between them in the text, so do not overstate the distinction on the exam — anchor to the two definitions above.

**Why it matters:** the definition directly names *what* is protected and *what* it's protected against, which feeds straight into the attack-surface and CIA discussions later.

### Why security fails ("Where are we getting it wrong?")

The lecture frames the root problem from a software-engineer's perspective: "The cybersecurity crisis is a fundamental failure of architecture" — security *should* be, but often is *not*, considered during early software design (attributed to Mowbray, T. J., *Cybersecurity: Managing Systems, conducting Testing, and Investigating Intrusions*) (L01 p.18). It cites a figure that cyber criminals are responsible for about **11.36 trillion USD per year** in financial losses, business downtime, and other assets (source: "83 Cybersecurity Statistics 2026: Worldwide Data & Trends") (L01 p.18).

The concrete causes given are (L01 p.19):
- Simple bugs in software and firmware.
- Mis-configuration across systems and services.
- Unintended side effects caused by system complexity (interconnectedness).
- Human factors (from unintentional errors to malicious actions).

A key takeaway here: "Many security issues can be either accidental or intentional" (L01 p.19).

### How to counter it (defenses and the major security activities)

Possible ways to counter these issues (L01 p.20):
- Best practices & security policies.
- Checks for known bad patterns.
- **Defense-in-depth.**
- **Secure by design** principles.
- Training and awareness.
- Experience and continuous learning.

These are operationalized as the **major topics / activities** of cybersecurity (L01 p.21):
- **Vulnerability Assessment** — finding weaknesses.
- **Penetration Testing** — ethical hacking to find exploitable weaknesses.
- **Threat Modelling** — understanding what can go wrong, how it can be attacked, and what to do about it.
- **Security Monitoring** — SIEM, firewalls, intrusion detection, intrusion prevention, etc.
- **Incident Response** — handling breaches when they occur.
- **Hardening** — improving system security: two-factor authentication, patches, updates, etc.

**Why it matters:** these six activities map onto the course plan (vulnerability assessment, pen testing, firewalls/IDS, threat modelling, etc.), so they are a likely "list the major cybersecurity activities" exam question.

### What to protect — against what

We protect four categories of assets (L01 p.25):
- **Networks** — all networks that interconnect our digital assets.
- **Systems and devices** — all systems and devices connected to the networks.
- **Programs** — all programs or source code that build up the systems connected to the networks.
- **Data** (most important) — all data whether **in transit, at rest, or processed**.

We protect these **against unauthorized access, modification, and deletion** (L01 p.25). Note how cleanly this maps to the CIA triad: unauthorized access ↔ confidentiality, unauthorized modification ↔ integrity, unauthorized deletion ↔ availability.

### The CIA triad (security goals)

The CIA triad is the core "how to protect" model (L01 p.26–27):
- **Confidentiality** — preventing the disclosure of information to unauthorized parties. Mechanisms: encryption, access control, authentication (L01 p.27).
- **Integrity** — protecting information from being modified by unauthorized parties. Mechanisms: signatures, checksums (L01 p.27).
- **Availability** — making sure that authorized parties are able to access the information when needed. Mechanisms: computational redundancies, backups, mitigation strategies (L01 p.27).

**Why it matters:** the triad is the single most exam-likely definition set in this chapter. Be able to define each pillar *and* give at least one example mechanism for each, exactly as the slides pair them.

### Why cybersecurity now / what to consider first

"Why cybersecurity?" is answered by three escalating trends plus the rise of ransomware (L01 p.24):
- Ever increasing information sharing.
- Ever increasing interconnectedness.
- Ever increasing vulnerabilities & exploits → ever increasing cyber attacks (e.g., ransomware).

"Where to begin?" asks whether the involved technologies implement effective security measures, broken out by technology (L01 p.28):
- **Networks** — transmission security (secure protocols), access control, etc.
- **Desktop devices** — OS fragmentation, timely security updates, licensed software.
- **Mobile devices** — OS fragmentation, outdated hardware without security support, keeping user devices in a secure environment.
- **Storage** — localized vs mobile, data encrypted, biometric, etc.

### Attack surface and attack vectors

- **Attack surface** = "a sum of all points where an attacker could try to enter, interact with, or extract data from a system" (L01 p.30). Equivalently: the attack vectors or end points an attacker can use to negatively affect resources or data, e.g., an unauthorized user accessing/editing/deleting data (L01 p.31).
- The slides give the formula **Attack Surface = Σ of Attack Vectors** (L01 p.32). The four attack-vector categories — i.e., how the data/system can be accessed — are (L01 p.32):
  - **Network**
  - **Machine (physically)**
  - **Software**
  - **Human**
- Three entities have opposing interests around the attack surface (this is the "Defense in Depth and Attack Surface" slide) (L01 p.33):
  - **Attacker** — wants to *expand* the exposed interface.
  - **Operator** — wants to *limit* the surface open to attacks.
  - **Designer** — should design the system accordingly (to meet the operators' requirements).
- **Access to the target:** depending on the kind of access, *no vulnerability is needed* (direct access). **Social engineering is often a first step** — e.g., an email to all/selected employees with or without crafted attachments (L01 p.34).

**Why it matters:** "define attack surface and list the four attack vectors" and "who wants to expand vs limit the attack surface" are both clean, high-probability exam items.

### Key cybersecurity terms (the vocabulary you must not confuse)

From L01 p.35:
- **Risk** — a measure of the extent to which an entity is threatened by a potential circumstance/event.
- **Vulnerability** — a weakness in a system.
- **Threat** — a circumstance/event that has the potential to exploit a vulnerability.
- **Exploit** — a method of taking advantage of a vulnerability.
- **Attack** — an action that uses a threat to exploit a vulnerability.
- **Patch** — a fix for a vulnerability.
- **Countermeasure** — a means of preventing an attack, which tries to exploit one or more vulnerabilities.

The relationships chain together: a **threat** exploits a **vulnerability**; an **exploit** is the *method*, an **attack** is the *action* that uses a threat to carry out that exploitation; a **patch** fixes the vulnerability; a **countermeasure** prevents the attack. Mixing up "threat" vs "exploit" vs "attack" is a classic exam trap (see Gotchas).

### Key takeaways / mindset

The lecture's stated takeaways (L01 p.36):
- Security is a wide field; **there is no silver bullet.**
- The process can be **domain specific** … and **iterative**.
- But there are procedures & best practices.
- The recurring questions to ask: What do we want to protect? How to protect it safely? Where and how can it be attacked? How can these attacks be mitigated? What next when the worst case occurs?

### Standards bodies and legal issues

**Standards** organizations that cover management practices and the overall architecture of security mechanisms/services (L01 p.37):
- **NIST** — National Institute of Standards and Technology.
- **ISOC** — Internet Society.
- **ITU-T** — International Telecommunication Union.
- **ISO** — International Organization for Standardization.

**Legal issues** named (L01 p.38):
- The Computer Security Act of 1987 & 1992.
- OMB Circular A-130.
- US state computer laws (reference link in slides).
- **HIPAA** — Health Insurance Portability and Accountability Act of 1996.
- **EU Data Protection Regulations (GDPR 2018).**

### Knowledge repositories and learning platforms

Knowledge repositories (described as "not exhaustive") (L01 p.8):
- **CVE** — Common Vulnerabilities and Exposures.
- **Exploit Database.**
- **CWE** — Common Weakness Enumeration.
- **MITRE ATT&CK Framework.**
- **OWASP** — Open Web Application Security Project.
- **CVE Details.**

Online training platforms (L01 p.8): **TryHackMe, Hack The Box, OverTheWire.**

### The course toolset

Tools introduced by category (L01 p.9):
- **Penetration testing:** Nmap, Netcat, Metasploit Framework, Burp Suite (slide: "Burp Suit"), Kali Linux toolset, Wireshark, Scapy (mostly advanced testing & research), Social Engineer Toolkit (slide: "Social Engineer Toolset").
- **Vulnerability Assessment:** Nessus, OpenVAS / Greenbone, Rapid7 InsightVM (formerly Nexpose).
- **Virtualization platforms:** VirtualBox / VMware.
- **Vulnerable machines:** Metasploitable 2 & Metasploitable 3.
- **Firewall/IDS/IPS:** Snort.
- **SIEM (incl. Extended Detection & Response):** Wazuh.

### The lab architecture (attacker + two targets, virtualized)

The exercise lab is three VMs (L01 p.40, E01 p.2):
- **Attacker / tester:** Kali Linux.
- **Targets / victims:** Metasploitable 2 (Linux) and Metasploitable 3 (Windows).
- **Everything is virtualized in VirtualBox.**

Kali Linux is a Debian-based Linux distribution designed for penetration testing; it is an open-source project maintained and funded by Offensive Security, and you download a VirtualBox image from kali.org (L01 p.42). Since release **2020.1**, Kali follows a **non-root user policy** — default user/password is `kali`/`kali`, and you use `sudo [-i]` to become or act as root (L01 p.43). Kali "is not intended to be used as a desktop OS, but as a pen testing tool box" (L01 p.44).

Metasploitable 2 & 3 are **intentionally vulnerable and contain untrusted software by design** — they must be treated as hostile and kept strictly isolated from your host system and any production networks (E01 p.1, p.5). The course-recommended counterpoint: keep the vulnerable machines "as outdated as they were designed" (don't patch them) (L01 p.44).

### VirtualBox networking modes (the connectivity table)

This table appears in both the lecture and the lab and is highly exam-likely. It shows, per networking mode, what connectivity is allowed (L01 p.41, E01 p.7):

| Mode | VM ↔ Host | VM1 ↔ VM2 | VM → Internet | VM ← Internet |
|------|-----------|-----------|---------------|----------------|
| **HostOnly** | Yes | Yes | No | No |
| **Internal** | No | Yes | No | No |
| **Bridged** | Yes | Yes | Yes | Yes |
| **NAT** | No | No | Yes | Port forwarding |
| **NAT Network** | No | Yes | Yes | Port forwarding |

Mode descriptions (L01 p.41):
- **Host Only** — limits the VM to a local private network; can communicate with host or other VMs; can neither send to nor receive from the Internet.
- **Bridged** — the VM is a node on the local network; packet sniffing on the host interface is possible.
- **Internal Networking** — VMs are assigned to virtual private networks (isolated; no host, no Internet).
- **NAT** — VM is hidden by the host; VMs *cannot* communicate with each other; traffic from the VM appears as if it came from the host.
- **NAT Network** — assigns VMs to virtual private networks; the assigned VMs *can* communicate; traffic from the VMs appears as if from the host.

The single most important contrast to memorize: **plain NAT does NOT let VM1 talk to VM2**, but **NAT Network DOES**. That is exactly why NAT Network is the recommended simple setup for the attacker-to-target lab (E01 p.4, p.7–8).

### Choosing a network configuration for the lab

For inter-VM communication, the attacker (Kali) and targets (Metasploitable) must be on the **same virtual network** (E01 p.6–7). Two configurations are presented (E01 p.7):
- **NAT Network (Simple Setup)** — simplest; gives internet access, automatic IP via DHCP, and communication between all VMs on the same NAT Network. Downside: limited control over which machines can communicate. Recommended for getting the environment working quickly (E01 p.7).
- **Internal Network + NAT (Advanced Setup)** — combines **Internal Networking** for inter-VM communication with a **separate NAT adapter** for controlled internet access. Lets you restrict communication to selected VMs, better isolate vulnerable targets, and model realistic topologies. Preferable when working with untrusted VMs or when stronger isolation is required (E01 p.7–8).

The trade-off is **functionality/convenience vs. isolation/realism** — NAT Network is easy but leaky; Internal+NAT is more work but isolates the deliberately vulnerable targets from the wider network.

### Platform compatibility (x86 vs Apple Silicon, WSL)

- All NextCloud VM images, and Metasploitable images in general, are built for **amd64/x86** architecture (E01 p.2).
- **Intel/AMD systems** — x86 is supported natively; no issue for most users (E01 p.3).
- **Apple Silicon (M1/M2/M3)** — ARM, **not natively compatible** with x86 Metasploitable images. Kali has ARM versions that run efficiently, but equivalent Metasploitable images are not readily available. Apple Silicon users must either (a) use **hardware emulation** to run x86 VMs (reduced performance), (b) team up with someone on an Intel/AMD machine, or (c) use a cloud-based solution (E01 p.3). The Mac follow-up doc recommends **UTM instead of VirtualBox**, plus `brew` and QEMU to convert images (MAC p.1).
- **WSL (Windows Subsystem for Linux)** — WSL (especially WSL 2, which runs a real Linux kernel) *can* install Kali, but it is tightly integrated with the host Windows system, which **reduces isolation** between the attacking environment and your primary work system — so a dedicated virtualization solution is preferred. GUI apps are supported (native GUI from Windows 11; earlier Windows needs an external X11 server) (E01 p.2). For WSL 2, **Host-Only Networking** is required to talk to Metasploitable VMs, but running the intentionally vulnerable Metasploitables under WSL is **strongly discouraged** due to weak isolation (E01 p.8).

### Basic Linux commands (Kali)

From L01 p.45:
- `apt` — package manager (e.g., `apt upgrade`).
- `pwd` — show the location of the current directory.
- `touch file` — create a file.
- `vi file` — low-bandwidth text editor (use `vim` for more comfort).
- `cp source destination` — copy a file.
- `mv source destination` — move a file.
- `rm file` — remove files.
- `rm -r directory` — recursively remove a directory and its sub-directories.
- `grep string file` — look for occurrences of a string in one or more files.
- `strings` — extract printable strings from a binary file.
- `ip address` / `ip addr` / `ip a` — return the IP address.

---

## Glossary

- **Cybersecurity** — the body of technologies, processes and practices designed to protect networks, computers, programs, digital assets, and data (processed, stored and/or in transit) from attack, damage, or unauthorized access (L01 p.22).
- **Confidentiality** — preventing the disclosure of information to unauthorized parties (L01 p.26).
- **Integrity** — protecting information from being modified by unauthorized parties (L01 p.26).
- **Availability** — making sure authorized parties can access the information when needed (L01 p.26).
- **CIA Triad** — Confidentiality, Integrity, Availability; the three core security goals (L01 p.26–27).
- **Risk** — a measure of the extent to which an entity is threatened by a potential circumstance/event (L01 p.35).
- **Vulnerability** — a weakness in a system (L01 p.35).
- **Threat** — a circumstance/event that has the potential to exploit a vulnerability (L01 p.35).
- **Exploit** — a method of taking advantage of a vulnerability (L01 p.35).
- **Attack** — an action that uses a threat to exploit a vulnerability (L01 p.35).
- **Patch** — a fix for a vulnerability (L01 p.35).
- **Countermeasure** — a means of preventing an attack which tries to exploit one or more vulnerabilities (L01 p.35).
- **Attack Surface** — the sum of all points where an attacker could try to enter, interact with, or extract data from a system; Attack Surface = Σ of Attack Vectors (L01 p.30, p.32).
- **Attack Vector** — an end point / path of access an attacker can use to affect resources or data; the four categories are Network, Machine (physical), Software, Human (L01 p.31–32).
- **Defense-in-Depth** — a counter-measure approach using layered defenses; presented alongside the attack-surface discussion (L01 p.20, p.33).
- **Secure by Design** — designing systems with security considered from the start (L01 p.20).
- **Vulnerability Assessment** — the activity of finding weaknesses (L01 p.21).
- **Penetration Testing** — ethical hacking to find exploitable weaknesses (L01 p.21).
- **Threat Modelling** — understanding what can go wrong, how it can be attacked, and what to do about it (L01 p.21).
- **Hardening** — improving system security (e.g., two-factor authentication, patches, updates) (L01 p.21).
- **Incident Response** — handling breaches when they occur (L01 p.21).
- **Kali Linux** — a Debian-based Linux distribution designed for penetration testing; open-source, maintained and funded by Offensive Security; the course's attacker machine (L01 p.42).
- **Metasploitable 2 / 3** — intentionally vulnerable target VMs (Metasploitable 2 = Linux, Metasploitable 3 = Windows) used as victims in the lab (L01 p.40, E01 p.5–6).
- **VirtualBox** — the course's chosen virtualization platform (cross-platform availability, not technical superiority) (E01 p.2).
- **VirtualBox Extension Pack** — add-on required for full functionality, including USB support and improved device handling (E01 p.3).
- **NAT** — networking mode where the VM is hidden by the host; VMs cannot communicate with each other; outbound traffic appears as if from the host (L01 p.41).
- **NAT Network** — networking mode where VMs on the same network can communicate with each other and reach the internet; recommended simple lab setup (L01 p.41, E01 p.7).
- **Host-Only / Internal / Bridged** — other VirtualBox networking modes (see the connectivity table) (L01 p.41).
- **DHCP** — automatic IP-address assignment; used by NAT Network, or run via a VirtualBox DHCP server for an internal network (E01 p.7, p.9).
- **WSL / WSL 2** — Windows Subsystem for Linux; WSL 2 runs a real Linux kernel; usable for Kali but discouraged for vulnerable targets due to weak isolation (E01 p.2, p.8).
- **UTM** — virtualization app recommended for Apple Silicon Macs instead of VirtualBox (MAC p.1).
- **QEMU / `qemu-img`** — emulator/tooling used on Mac to convert `.vmdk` images to `.qcow2` for UTM (MAC p.1).
- **CVE / CWE / Exploit-DB / MITRE ATT&CK / OWASP** — knowledge repositories of vulnerabilities, weaknesses, exploits, attack techniques, and web-app security guidance (L01 p.8).
- **SIEM** — Security Information and Event Management (with Extended Detection & Response); course tool: Wazuh (L01 p.9).
- **Purple Team** — the course's stated goal: building strong purple teams (combining offensive "red" and defensive "blue" mindsets) of cybersecurity experts (L01 p.12).

---

## How-To Cookbook

### A. Install VirtualBox (Windows/macOS) (E01 p.3)
1. On **Linux**: install VirtualBox via your distribution's package manager (`apt`, `dnf`, `pacman`) for proper OS integration and easy updates.
2. On **Windows/macOS**: go to the VirtualBox website and download the installer matching your OS under "VirtualBox Platform Packages".
3. Run the installer and follow the prompts.
4. Install the **VirtualBox Extension Pack** from the same page: click "All supported platforms" to download the `.vbox-extpack` file, then double-click it — VirtualBox launches and completes the install. (Required for full functionality, including USB support and improved device handling.)

### B. Install and configure Kali Linux in VirtualBox (E01 p.3–5, L01 p.43–44)
1. **Download the VM image** — preferred: the updated Kali VM image from the course NextCloud share; alternative: the official Kali VM image from kali.org. Select the **VirtualBox** image and a version compatible with your OS and CPU architecture.
2. **Import** — In VirtualBox: `File → Import Appliance`, or double-click the downloaded image file; review and import in the dialog.
3. **Configure RAM** — Select the Kali VM → `Settings → System` → set Base Memory. 1 GB is the minimum; allocate more for better performance if your host has the memory.
4. **Configure CPU** — `Settings → System → Processor`. Default is 2 CPUs; 1 CPU is sufficient for most exercises. Do not allocate more CPUs than your host can comfortably support.
5. **Network** — `Settings → Network` → set "Attached to" = **NAT Network** for a simple setup (gives internet + inter-VM connectivity). (For the controlled option, see recipe E.)
6. **Finalize** — Click `OK`, then double-click the Kali VM to start it.
7. **Log in** — default credentials `kali` / `kali`. **Change the default password** after setup.
8. **Update Kali** — in a terminal:
   ```
   sudo apt update
   sudo apt full-upgrade -y
   ```
   (The lecture also mentions `apt autoremove` when suggested, and that updates are run as root or with sudo) (L01 p.44).
9. **(Optional) Non-Kali distro** — if you use another Linux distro, manually install at minimum: `nmap`, `netcat`, `metasploit`, `whois`, `host`, `etherape`, `pnscan`, `legion`, `nessus`, `mysql`, `john` (John the Ripper), `openvas` / Greenbone Security Assistant (E01 p.5).

### C. Configure Kali keyboard layout (L01 p.43)
- Permanently reconfigure the keyboard:
  ```
  $ dpkg-reconfigure keyboard-configuration
  ```
- Temporarily switch the GUI keyboard layout at runtime:
  ```
  $ setxkbmap en_UK
  $ setxkbmap dk
  ```

### D. Install Metasploitable 2 (Linux target) (E01 p.5)
1. Download Metasploitable 2 from Rapid7 or from the course NextCloud share.
2. Unzip it into the desired directory.
3. In VirtualBox: `File → Import Appliance`, or double-click the `.vmdk` file, and follow the import wizard.
4. Log in with default credentials: `msfadmin` / `msfadmin`.
5. Configure the network per section 4 of the lab (or use **NAT Network** for the simple setup).
> Security note: treat Metasploitable as hostile; keep it strictly isolated from your host and production networks (E01 p.5).

### E. Install Metasploitable 3 (Windows target) (E01 p.6)
1. Download the image from VagrantUp, or from NextCloud via the provided Vagrant.
2. Unzip the archive.
3. **Rename the extracted file to end in `.ova`** — it is technically a tar archive; the extension lets Windows/VirtualBox recognize it. (VirtualBox filters importable files by extension and lists `.ova` automatically.) Alternatively, clear the file-type filter in the import dialog and select the file manually. *Note: renaming to `.ova.gz` makes it appear in the list but VirtualBox will not allow the import to proceed.*
4. Import using the same procedure as Metasploitable 2.
5. Log in with default credentials: `vagrant` / `vagrant`.
6. Configure the network the same as Metasploitable 2.

**Command-line install of Metasploitable 3 via Vagrant** (E01 p.6):
```
vagrant plugin install vagrant-reload
vagrant plugin install vagrant-vbguest
vagrant box add rapid7/metasploitable3-win2k8
```
If you hit a plugin error, edit (from the user folder):
```
.vagrant.d/gems/3.3.8/gems/vagrant-vbguest-0.32.0/lib/vagrant-vbguest/hosts/virtualbox.rb
```
On line 84, change `path && File.exists` to `path && File.exist` (drop the trailing `s`). A `MountDiskImage` error may also appear but has no effect on the machine (E01 p.6).

### F. Simple network setup — create a NAT Network (E01 p.8)
1. In VirtualBox: `File → Tools → Network Manager` (or `File → Preferences → Network`, depending on version).
2. Click **Add** to create a network named `NatNetwork`.
3. Verify **DHCP is enabled** for this network (so IPs are assigned automatically).
4. Assign it to each VM: select the VM → `Settings → Network` → "Attached to" = **NAT Network** → "Name" = `NatNetwork`.
5. Repeat for the Kali, Metasploitable 2, and Metasploitable 3 VMs, all on the **same** NAT Network.
> VMs must be **powered off** to modify network settings (E01 p.8).

### G. Advanced network setup — Internal Network + VirtualBox DHCP server (E01 p.9)
1. Choose one IP method for the internal network: assign static IPs to both VMs, run a DHCP server on the Kali VM, or **enable a VirtualBox DHCP server (recommended)**.
2. From the **host** command line (Windows users may `cd` to the directory containing `VBoxManage` to avoid full paths):
   - List internal networks: `VBoxManage list intnets`
   - List existing DHCP servers: `VBoxManage list dhcpservers`
   - Create and enable the DHCP server:
     ```
     VBoxManage dhcpserver add \
        --network=CyberSecLab \
        --lowerip 172.30.1.20 \
        --upperip 171.30.1.50 \
        --netmask 255.255.255.0 \
        --ip 172.30.1.1 \
        --enable
     ```
     This creates a DHCP server for the internal network `CyberSecLab`, assigning IPs from the `172.30.1.0/24` range. The `\` means the command continues on the next line. Remember to select `CyberSecLab` when configuring each VM's internal network adapter.
     > ⚠️ The slide's `--upperip` reads `171.30.1.50` (note `171`, not `172`) — this is almost certainly a typo in the lab; the intended range is within `172.30.1.0/24`. Flagged so you don't reproduce it blindly (E01 p.9).
3. **Verify**: start all three VMs, log into the Metasploitables with their default creds, confirm each got an IP, and confirm they're reachable from Kali.

### H. Verify inter-VM connectivity (MAC p.1, E01 p.9)
1. On Metasploitable 2, find its IP: run `ifconfig` (look at `eth0 inet`, e.g., `192.168.64.x`).
2. On Kali, find its IP: run `ip addr` (e.g., `eth0 inet 192.168.64.y`).
3. From Kali, run `ping <Metasploitable2_IP>`. If you get replies, the network is working.
4. If you can't get the target's IP directly, from Kali run `sudo arp-scan -l` to discover hosts on the local network (default IP often around `192.168.64.10`) (SOL p.1).

### I. Apple Silicon Mac setup with UTM (MAC p.1)
1. Requirements: `brew` and **UTM** (use UTM instead of VirtualBox).
2. Install Kali under UTM — easiest from the community UTM mirror (the doc author chose "Kali Linux 2025 UTM (Apple Silicon) (community image)").
3. Obtain Metasploitable `.vmdk` files: Metasploitable 2 from NextCloud (download `Metasploitable.vmdk`); Metasploitable 3 from the HashiCorp Vagrant portal (download the ~7.01 GB "virtualbox" file, add the `.zip` extension, unzip).
4. Convert each `.vmdk` to `.qcow2` in Terminal:
   ```
   brew install qemu
   qemu-img convert -p -f vmdk -O qcow2 <filename>.vmdk <filename>.qcow2
   ```
5. Create the VM in UTM: `Create a New Virtual Machine → Emulate → Other → Expert Mode [X86_64] [Standard PC (Q35 + …)] → Boot Device [None]`, then follow the linked tutorial.
6. Connection between Kali and Metasploitable should work by default; verify with `ifconfig` / `ip addr` / `ping` as in recipe H.

### J. Fix Metasploitable 3 crashing on UTM / Apple Silicon (SOL p.1)
1. In the VM's settings (UTM): set System → `Standard PC (i440X …)`; under QEMU, **uncheck "UEFI Boot"**.
2. In UTM, `View → Custom Toolbar` → add a **"Send Key"** button to the Metasploitable 3 toolbar; configure `Ctrl + Shift + Esc` (and ensure `Ctrl + Alt + Delete` exists).
3. Start the VM, send `Ctrl + Alt + Delete`, and log in. You may see "Windows License is expired". Send `Ctrl + Shift + Esc` to open Task Manager (may take time), then `File → New Task (Run…) → cmd`. (If the mouse is stuck, press `Ctrl + option` to escape.)
4. In `cmd`, delete the VirtualBox-related files that cause the crash:
   ```
   del C:\Windows\System32\drivers\VBoxMouse.sys
   del C:\Windows\System32\drivers\VBoxGuest.sys
   del C:\Windows\System32\drivers\VBoxSF.sys
   del C:\Windows\System32\drivers\VBoxVideo.sys
   rmdir /s /q "C:\Program Files\Oracle\VirtualBox Guest Additions"
   ```
   (You may need to retry the deletion through repeated crashes — be patient.)
5. Reopen the VM. The mouse/touchpad won't work, but Metasploitable 3 runs stably; use it via keyboard only.
6. Check the IP from the command prompt (same as the PDF), or from Kali with `sudo arp-scan -l` (default IP often `192.168.64.10`). Running with a "Windows License is expired" screen is fine for lab use.

---

## Exam-Style Q&A

**Q1. Define cybersecurity and state the CIA triad with one example mechanism for each pillar.**
A. Cybersecurity is "the body of technologies, processes and practices designed to protect networks, computers, programs, digital assets, and data (processed, stored and/or in transit) from attack, damage or unauthorized access" (L01 p.22). The CIA triad is the set of security goals (L01 p.26–27):
- **Confidentiality** — preventing disclosure of information to unauthorized parties; e.g., **encryption, access control, authentication**.
- **Integrity** — protecting information from modification by unauthorized parties; e.g., **digital signatures, checksums**.
- **Availability** — ensuring authorized parties can access information when needed; e.g., **computational redundancy, backups, mitigation strategies**.

**Q2. Distinguish between vulnerability, threat, exploit, and attack.**
A. A **vulnerability** is a weakness in a system. A **threat** is a circumstance/event that has the potential to exploit that vulnerability. An **exploit** is a *method* of taking advantage of a vulnerability. An **attack** is an *action* that uses a threat to exploit a vulnerability (L01 p.35). In short: the vulnerability is the hole; the threat is the possibility someone uses it; the exploit is the technique; the attack is the act of actually doing it. A **patch** fixes the vulnerability and a **countermeasure** prevents the attack (L01 p.35).

**Q3. What is an attack surface, and what are its components?**
A. The attack surface is "a sum of all points where an attacker could try to enter, interact with, or extract data from a system" (L01 p.30) — equivalently the set of attack vectors/end points an attacker can use to affect resources or data (L01 p.31). Formally, **Attack Surface = Σ of Attack Vectors** (L01 p.32). The four attack-vector categories (how the system/data can be accessed) are **Network, Machine (physically), Software, and Human** (L01 p.32).

**Q4. In the context of the attack surface, what are the goals of the attacker, the operator, and the designer?**
A. The **attacker** wants to *expand* the exposed interface (enlarge the attack surface). The **operator** wants to *limit* the surface open to attacks. The **designer** should design the system accordingly — i.e., to meet the operators' requirements for a minimal surface (L01 p.33). This is the "Defense in Depth and Attack Surface" framing.

**Q5. Why do many security failures occur, and how can they be countered?**
A. The lecture frames the crisis as "a fundamental failure of architecture" — security is often not considered during early software design (L01 p.18). Specific causes: simple bugs in software/firmware, mis-configuration across systems and services, unintended side effects from system complexity (interconnectedness), and human factors (unintentional errors to malicious actions); and these issues can be accidental or intentional (L01 p.19). Counters include best practices & security policies, checks for known bad patterns, **defense-in-depth**, **secure-by-design** principles, training and awareness, and experience/continuous learning (L01 p.20).

**Q6. Name the major activities of cybersecurity covered by the course and what each does.**
A. (L01 p.21) **Vulnerability Assessment** — finding weaknesses; **Penetration Testing** — ethical hacking to find exploitable weaknesses; **Threat Modelling** — understanding what can go wrong, how it can be attacked, and what to do about it; **Security Monitoring** — SIEM, firewalls, intrusion detection/prevention; **Incident Response** — handling breaches when they occur; **Hardening** — improving system security (two-factor authentication, patches, updates).

**Q7. Compare the VirtualBox NAT and NAT Network modes. Which is recommended for the lab and why?**
A. In plain **NAT**, the VM is hidden behind the host, VMs **cannot communicate with each other**, traffic appears as if from the host, and inbound from the Internet requires port forwarding (L01 p.41). In **NAT Network**, VMs are placed on a shared virtual private network so they **can communicate with each other**, get DHCP-assigned IPs, and have internet access (L01 p.41, E01 p.7). For the lab the attacker (Kali) must reach the targets (Metasploitable), so **NAT Network is the recommended simple setup** — it enables inter-VM connectivity that plain NAT does not (E01 p.4, p.7).

**Q8. Fill in the VirtualBox networking connectivity table for HostOnly, Internal, Bridged, NAT, and NAT Network.**
A. (L01 p.41, E01 p.7) — columns are VM↔Host, VM1↔VM2, VM→Internet, VM←Internet:
- **HostOnly:** Yes, Yes, No, No
- **Internal:** No, Yes, No, No
- **Bridged:** Yes, Yes, Yes, Yes
- **NAT:** No, No, Yes, Port forwarding
- **NAT Network:** No, Yes, Yes, Port forwarding

**Q9. Describe the lab architecture and the default credentials for each machine.**
A. Three virtualized machines in VirtualBox (L01 p.40, E01 p.5–6): one **attacker** — **Kali Linux** (default `kali` / `kali`, L01 p.43); two **targets** — **Metasploitable 2** (Linux, default `msfadmin` / `msfadmin`) and **Metasploitable 3** (Windows, default `vagrant` / `vagrant`). The Metasploitables are intentionally vulnerable and must be isolated from the host and production networks (E01 p.5).

**Q10. What is Kali Linux, and what is significant about its user policy since release 2020.1?**
A. Kali Linux is a **Debian-based** Linux distribution designed for **penetration testing**; it is an open-source project maintained and funded by **Offensive Security** (L01 p.42). Since release **2020.1**, Kali adheres to a **non-root user policy**: the default account is the standard user `kali` (password `kali`), and you use `sudo [-i]` to act as root (L01 p.43). Kali is meant to be used as a pen-testing toolbox, not a daily desktop OS (L01 p.44).

**Q11. Why are Apple Silicon Macs problematic for this lab, and what are the options?**
A. NextCloud/Metasploitable images are built for **amd64/x86**, and Apple Silicon (M1/M2/M3) is **ARM**, so the x86 Metasploitable images are not natively compatible. Kali has ARM versions, but equivalent Metasploitable images are not readily available (E01 p.2–3). Options: (a) use **hardware emulation** to run x86 VMs at reduced performance, (b) work with a teammate on an Intel/AMD machine, or (c) use a cloud-based solution (E01 p.3). The Mac follow-up recommends **UTM** (with `brew`/QEMU to convert `.vmdk` → `.qcow2`) instead of VirtualBox (MAC p.1).

**Q12. Why is using WSL discouraged for running the Metasploitable targets?**
A. WSL (especially WSL 2, which runs a real Linux kernel) can install Kali, but it is **tightly integrated with the host Windows system**, which reduces isolation between the attacking environment and your primary work system. Running intentionally vulnerable machines like Metasploitable under WSL is strongly discouraged; a dedicated virtualization environment provides significantly better isolation and security (and WSL 2 requires Host-Only Networking to even reach the targets) (E01 p.2, p.8).

**Q13. What are the ethical and legal expectations set out in this lecture?**
A. Ethically: participants must uphold cybersecurity ethical standards; knowledge and skills are solely for educational purposes; any unauthorized access, manipulation, or misuse of data/systems is prohibited; you are responsible for your own actions; and you must **sign the Ethical Statement Form in ItsLearning** (L01 p.10). Legally, the slides cite the Computer Security Act of 1987 & 1992, OMB Circular A-130, US state computer laws, **HIPAA (1996)**, and the **EU GDPR (2018)** (L01 p.38).

**Q14. List the four asset categories cybersecurity protects and what it protects them against.**
A. (L01 p.25) **Networks** (all networks interconnecting digital assets), **Systems and devices** (all connected systems/devices), **Programs** (all programs/source code building the systems), and — most importantly — **Data** (in transit, at rest, or processed). They are protected against **unauthorized access, modification, and deletion** — which map to confidentiality, integrity, and availability respectively.

**Q15. How is the course graded, and how does the exam relate to the lab exercises?**
A. There is a **written exam** based on **6 selected hands-in exercises**, which serve as the materials for the final exam (L01 p.11). The exam combines **MCQ (multiple-choice)**, **MCA (multiple-correct-answer)**, and **short essay questions (SEQ)** (L01 p.11, p.13). It is **120 minutes**, in **English**, graded on the Danish **−3 to 12** scale (L01 p.11). Students form groups (4–6 welcome) for the exercises (L01 p.11). The stated course goal is to build strong **purple teams** of cybersecurity experts (L01 p.12).

**Q16. Name the standards bodies and at least three knowledge repositories introduced.**
A. Standards bodies: **NIST**, **ISOC** (Internet Society), **ITU-T**, and **ISO** (L01 p.37). Knowledge repositories: **CVE** (Common Vulnerabilities and Exposures), **Exploit Database**, **CWE** (Common Weakness Enumeration), **MITRE ATT&CK Framework**, **OWASP**, and **CVE Details**; plus training platforms **TryHackMe**, **Hack The Box**, and **OverTheWire** (L01 p.8).

---

## Gotchas

- **NAT ≠ NAT Network.** The most common trap from the connectivity table: under plain **NAT** the two VMs **cannot** see each other (No for VM1↔VM2), so a Kali→Metasploitable ping fails. **NAT Network** is what enables inter-VM communication. If your attacker can't reach the target, this is the first thing to check (L01 p.41, E01 p.4, p.7).
- **You must power off a VM to change its network adapter.** VirtualBox won't let you reassign the network on a running VM (E01 p.8).
- **Don't confuse threat, exploit, and attack.** Threat = the *potential*; exploit = the *method/technique*; attack = the *action* that actually uses a threat to exploit a vulnerability (L01 p.35). Exam questions deliberately swap these.
- **No vulnerability is needed for some access.** With direct (e.g., physical) access, an attacker may not need any software vulnerability at all; and **social engineering is often the first step**, not a technical exploit (L01 p.34).
- **Keep the targets outdated, not patched.** You update *Kali* regularly (`sudo apt update; sudo apt full-upgrade -y`) but you deliberately keep Metasploitable "as outdated as they were designed" — patching them defeats the purpose (L01 p.44, E01 p.5).
- **Treat Metasploitable as hostile.** These VMs contain intentionally vulnerable, untrusted software; isolate them strictly from the host and any production/external networks. This is the security rationale for the Internal+NAT advanced setup over plain NAT Network (E01 p.1, p.5, p.7–8).
- **Metasploitable 3 file-extension trick.** The extracted Metasploitable 3 file is a tar archive; you must **rename it to `.ova`** for VirtualBox to recognize it. Renaming to `.ova.gz` makes it *appear* in the list but the import will **fail** — don't do that (E01 p.6).
- **Metasploitable 3 Vagrant plugin error.** If installation errors out, the `File.exists` → `File.exist` one-character edit on line 84 of `virtualbox.rb` is the fix; a `MountDiskImage` error can be ignored (E01 p.6).
- **The Internal-Network DHCP example contains a likely typo.** The lab's `VBoxManage dhcpserver add` uses `--upperip 171.30.1.50` while everything else is in `172.30.1.0/24`. The `171` is almost certainly meant to be `172`; reproducing it verbatim could break the range (E01 p.9).
- **Default credentials differ per machine.** Kali = `kali`/`kali`; Metasploitable 2 = `msfadmin`/`msfadmin`; Metasploitable 3 = `vagrant`/`vagrant`. And change the Kali password after setup (E01 p.5–6, L01 p.43).
- **Disk space.** At least **100 GB free** is required for the full lab (Kali with databases + Metasploitable 2 + Metasploitable 3) — provision before you start (E01 p.1).
- **Apple Silicon needs a different toolchain.** VirtualBox/x86 Metasploitable images won't run natively on M-series Macs; use UTM + QEMU conversion (`.vmdk` → `.qcow2`), emulate x86_64, or collaborate/use cloud. Expect reduced performance under emulation (E01 p.3, MAC p.1, SOL p.1).
- **Minor slide spellings.** The slides write "Burp Suit" (Burp Suite), "Social Engineer Toolset" (Social-Engineer Toolkit / SET), and ".va"/".vmdk" in places — recognize the intended tools/files; don't let the typos throw you on the exam (L01 p.9, E01 p.6).
- **CIA mechanism pairing.** When asked for examples, give the *paired* ones from the slides: confidentiality → encryption/access control/authentication; integrity → signatures/checksums; availability → redundancy/backups/mitigation. Listing a firewall under "integrity" would lose the point (L01 p.27).

---

*End of Chapter 01 study guide. All facts above are grounded in the four provided PDFs; where a slide value looked like a typo (e.g., the `171.30.1.50` IP) it is flagged rather than silently corrected.*
