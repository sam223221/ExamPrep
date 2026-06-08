# 04. Firewalls & IDS — Commands & Code Examples

### Set the default-deny policy on a chain (standard syntax)
**What:** Make "that not expressly permitted is prohibited" the baseline by defaulting chains to DROP (L04 p.8).
```bash
# iptables (standard syntax) — drop everything not explicitly allowed
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT
```
**Notes:** `-P` sets the built-in policy applied when no rule matches. Default-deny is the secure choice from the lecture; set OUTPUT to ACCEPT only if you trust internal hosts, otherwise DROP it too. Setting policy to DROP before adding allow rules over SSH can lock you out — add the SSH allow rule first.

### Allow inbound SSH on port 22 (standard syntax)
**What:** Explicitly permit new TCP connections to the SSH service so default-deny does not block admin access.
```bash
# iptables (standard syntax)
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```
**Notes:** `-A INPUT` appends to the INPUT chain; `-p tcp` selects protocol; `--dport 22` matches destination port 22; `-j ACCEPT` is the target action. Order matters — rules apply top to bottom, first match wins (L04 p.14), so add this before a broad deny.

### Drop inbound traffic to a closed port (standard syntax)
**What:** Block a service by dropping packets to its destination port (e.g., deny Telnet on 23).
```bash
# iptables (standard syntax)
iptables -A INPUT -p tcp --dport 23 -j DROP
```
**Notes:** `-j DROP` silently discards the packet (no response); `-j REJECT` would instead send an ICMP refusal. DROP is the lecture's filtering action; it gives an attacker less information than REJECT.

### Block all traffic from one source IP (standard syntax)
**What:** Drop every packet arriving from a single hostile source address.
```bash
# iptables (standard syntax)
iptables -A INPUT -s 203.0.113.66 -j DROP
```
**Notes:** `-s` matches source address; omit `-p`/`--dport` to match all protocols and ports from that host. This is the manual equivalent of an IPS "block user / change firewall rules" reaction (L04 p.41) and of preemptive blocking by IP (L04 p.43) — beware blocking a legitimate user (self-DoS).

### Add stateful connection tracking for return traffic (standard syntax)
**What:** Let replies to connections you started back in automatically, instead of writing explicit return rules — the stateful-filter concept (L04 p.18).
```bash
# iptables (standard syntax) — conntrack module
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
```
**Notes:** `-m conntrack` loads the connection-tracking match; `--ctstate ESTABLISHED,RELATED` matches packets that belong to an existing session (ESTABLISHED) or a related one such as an FTP data channel (RELATED). This replaces the second "return" rule a static filter needs. Older syntax: `-m state --state ESTABLISHED,RELATED`.

### Translate the lecture ACL: allow internal /16 outbound web + DNS, default deny (standard syntax)
**What:** Realize the lecture's ACL (allow `222.22/16` to reach external HTTP/DNS, then deny all) on a Linux router (L04 p.14).
```bash
# iptables (standard syntax) — FORWARD chain on a router
iptables -P FORWARD DROP

# Outbound HTTP (ephemeral src >1023 -> dst 80) and its reply
iptables -A FORWARD -s 222.22.0.0/16 -p tcp --sport 1024:65535 --dport 80 -j ACCEPT
iptables -A FORWARD -d 222.22.0.0/16 -p tcp --sport 80 --dport 1024:65535 -j ACCEPT

# Outbound DNS (UDP 53) and its reply
iptables -A FORWARD -s 222.22.0.0/16 -p udp --sport 1024:65535 --dport 53 -j ACCEPT
iptables -A FORWARD -d 222.22.0.0/16 -p udp --sport 53 --dport 1024:65535 -j ACCEPT
```
**Notes:** `>1023` in the ACL = ephemeral client ports (here `1024:65535`); the service is the well-known port (80, 53). Because this is a static filter with no session memory, each direction needs its own rule. A stateful filter would replace both reply rules with one ESTABLISHED,RELATED rule (L04 p.18).

### Prevent your network being used in a Smurf DoS (standard syntax)
**What:** Drop ICMP destined for a broadcast address, per the lecture policy (L04 p.13).
```bash
# iptables (standard syntax)
iptables -A FORWARD -p icmp -d 222.22.255.255 -j DROP
```
**Notes:** A Smurf attack spoofs your address and pings a broadcast so every host floods the victim with replies. Dropping ICMP to the broadcast address (e.g., `222.22.255.255`) is the lecture's stated mitigation.

### Prevent your network from being tracerouted (standard syntax)
**What:** Drop outgoing ICMP so traceroute cannot map your network (L04 p.13).
```bash
# iptables (standard syntax)
iptables -A OUTPUT -p icmp -j DROP
```
**Notes:** Traceroute relies on ICMP time-exceeded / port-unreachable replies; dropping outgoing ICMP starves it. Trade-off: you also lose useful diagnostics like outbound ping replies.

### Anti-spoofing: drop inbound packets claiming an internal source (standard syntax)
**What:** Counter IP address spoofing by dropping external packets that pretend to come from inside (L04 p.17).
```bash
# iptables (standard syntax) — packets arriving on the external NIC but claiming internal src
iptables -A FORWARD -i eth0 -s 222.22.0.0/16 -j DROP
```
**Notes:** `-i eth0` matches the inbound interface (the external one). The lecture's countermeasure to spoofing is "add filters on the router to block" — no legitimate packet from the outside should carry an internal source address.

### Rate-limit new connections to a service (standard syntax)
**What:** Throttle the rate of new inbound connections to blunt flooding / brute-force without a full block.
```bash
# iptables (standard syntax) — allow at most 5 new SSH conns/min, burst 5
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW \
  -m limit --limit 5/min --limit-burst 5 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j DROP
```
**Notes:** `-m limit --limit 5/min` caps the matched rate; `--limit-burst 5` allows an initial burst before throttling. The follow-up DROP catches anything over the limit. This is a measured alternative to outright preemptive blocking (L04 p.43).

### List active rules with numbers, counters, and no DNS lookups (standard syntax)
**What:** Inspect the current ruleset to read/audit it before editing.
```bash
# iptables (standard syntax)
iptables -L -n -v --line-numbers
```
**Notes:** `-L` lists rules; `-n` shows numeric addresses/ports (no slow DNS resolution); `-v` adds packet/byte counters; `--line-numbers` prints the index you need to delete a specific rule. Add a chain name (e.g., `iptables -L INPUT -n -v`) to scope it.

### Delete a single rule and flush a whole chain (standard syntax)
**What:** Remove one rule by its line number, or clear every rule in a chain.
```bash
# iptables (standard syntax)
iptables -D INPUT 3          # delete rule #3 in INPUT (number from --line-numbers)
iptables -D INPUT -p tcp --dport 23 -j DROP   # or delete by exact spec
iptables -F                  # flush ALL rules in all chains
iptables -F INPUT            # flush only the INPUT chain
```
**Notes:** `-D` deletes; you can target by line number or by repeating the rule's exact specification. `-F` flushes (does not change the `-P` default policy) — if the policy is DROP, flushing can cut all traffic, so reset policy first or have console access.

### Persist / restore the ruleset across reboots (standard syntax)
**What:** Save the live ruleset to a file and reload it later (iptables is not persistent by default).
```bash
# iptables (standard syntax)
iptables-save > /etc/iptables/rules.v4     # dump current rules to a file
iptables-restore < /etc/iptables/rules.v4  # reload them
```
**Notes:** `iptables-save`/`iptables-restore` move the entire ruleset as text. Without this (or a service like `netfilter-persistent`), your rules vanish on reboot.

### Write a basic Snort/Suricata signature rule (standard syntax)
**What:** A misuse-detection signature that alerts on known-bad traffic — the lecture names Snort/Suricata but gives no rule syntax (L04 p.40, p.46).
```text
# Snort/Suricata rule (standard syntax) — alert on inbound Telnet to the home net
alert tcp any any -> $HOME_NET 23 (msg:"Telnet connection attempt"; sid:1000001; rev:1;)

# Alert on a content signature (detect a known attack string in HTTP)
alert tcp any any -> $HOME_NET 80 (msg:"Possible /etc/passwd access"; \
  content:"/etc/passwd"; nocase; sid:1000002; rev:1;)
```
**Notes:** Structure is `action proto src_ip src_port -> dst_ip dst_port (options)`. `alert` logs and warns; `msg` is the human label; `content` is the byte pattern matched (misuse/signature detection); `nocase` ignores case; `sid` is a unique rule ID (>=1000000 for local rules) and `rev` its revision. This is signature/misuse detection — it cannot catch attacks with no signature (L04 p.40). Standard syntax; the slides do not provide it (L04 p.46).

### Capture and filter traffic with tcpdump (standard syntax)
**What:** Sniff packets on the wire to feed analysis or a NIDS, filtering to the traffic of interest.
```bash
# tcpdump (standard syntax)
tcpdump -i eth0 -n tcp port 80              # live HTTP on eth0, no name resolution
tcpdump -i eth0 host 203.0.113.66           # only traffic to/from one host
tcpdump -i eth0 'tcp[tcpflags] & (tcp-syn|tcp-ack) == tcp-syn'   # only bare SYN = new conn attempts (excludes SYN-ACK)
tcpdump -i eth0 -w capture.pcap             # write raw packets to a file
tcpdump -r capture.pcap -n                  # read/analyse a saved capture
```
**Notes:** `-i` selects the interface; `-n` skips DNS/port-name lookups; `-w` writes a pcap, `-r` reads one. The SYN filter mirrors the lecture's "incoming TCP SYN" web-server policy (L04 p.13) — bare SYN packets mark new connection attempts; the `== tcp-syn` form excludes SYN-ACK replies (which also have the SYN bit set). This is how a network-based IDS (NIDS) gets its raw data (L04 p.39).

### Crack a bcrypt hash with Hashcat using rockyou.txt (standard syntax)
**What:** Dictionary-attack the exercise's `$2b$12$...` bcrypt hash with the rockyou wordlist (E04 p.1).
```bash
# Hashcat (standard syntax) — bcrypt is mode 3200, -a 0 is straight wordlist
hashcat -m 3200 -a 0 hash.txt /usr/share/wordlists/rockyou.txt

# Show the cracked plaintext afterwards
hashcat -m 3200 hash.txt --show
```
**Notes:** `-m 3200` = bcrypt ($2*$) hash mode; `-a 0` = straight dictionary attack; `hash.txt` holds the single `$2b$12$...` line. The `$12$` cost makes bcrypt deliberately slow, so success depends on the password being common and present in rockyou — the exercise's lesson on weak passwords. On Kali the wordlist may be gzipped: `gunzip /usr/share/wordlists/rockyou.txt.gz` first.

### Crack the same bcrypt hash with John the Ripper (standard syntax)
**What:** The alternative cracking tool named in the exercise, run in dictionary mode (E04 p.1).
```bash
# John the Ripper (standard syntax)
john --format=bcrypt --wordlist=/usr/share/wordlists/rockyou.txt hash.txt

# Display recovered passwords
john --show --format=bcrypt hash.txt
```
**Notes:** `--format=bcrypt` forces the correct hash type (John may otherwise guess wrong); `--wordlist=` points at rockyou. Cracked results are cached in `~/.john/john.pot`, so a re-run of the crack command may say "No password hashes left to crack" — use `--show` to see them.

### Example ACL table (lecture format)
**What:** The lecture's six-field ACL allowing internal `222.22/16` to use external web + DNS with a default deny, applied top to bottom, first match wins (L04 p.14).
```text
action | source address       | dest address          | protocol | source port | dest port
-------|----------------------|-----------------------|----------|-------------|----------
allow  | 222.22/16            | outside of 222.22/16  | TCP      | > 1023      | 80
allow  | outside of 222.22/16 | 222.22/16             | TCP      | 80          | > 1023
allow  | 222.22/16            | outside of 222.22/16  | UDP      | > 1023      | 53
allow  | outside of 222.22/16 | 222.22/16             | UDP      | 53          | > 1023
deny   | all                  | all                   | all      | all         | all
```
**Notes:** Rows 1-2 permit outbound HTTP and its replies; rows 3-4 do the same for DNS; the final `deny all` is the explicit default-deny catch-all. Each service needs an out rule AND a return rule because a static filter has no session memory (L04 p.18). Put specific allows first; a `deny all` placed too high blocks everything beneath it.

### Map a plain-English policy to a packet-filter setting (lecture method)
**What:** The lecture's policy-to-firewall-setting translations you may be asked to reproduce (L04 p.13).
```text
Policy: No outside Web access
  -> Drop all OUTGOING packets to any IP address, port 80

Policy: External connections to public Web server only
  -> Drop all INCOMING TCP SYN packets to any IP EXCEPT 222.22.44.203, port 80

Policy: Prevent IPTV from eating bandwidth
  -> Drop all INCOMING UDP packets EXCEPT DNS and router broadcasts

Policy: Prevent your network being used for a Smurf DoS
  -> Drop all ICMP packets going to a broadcast address (e.g. 222.22.255.255)

Policy: Prevent your network from being tracerouted
  -> Drop all OUTGOING ICMP
```
**Notes:** Method: identify direction, protocol, addresses, ports, action (drop/allow). Prefer default-deny, add explicit allows for required services, end with deny all. "Public web server only" uses TCP SYN because SYN marks a new inbound connection attempt (L04 p.13).

### Reactive IPS action: insert a block rule at the top of the chain (standard syntax)
**What:** Simulate an IPS "change firewall rules / block user" response by inserting a deny ahead of existing allows (L04 p.41).
```bash
# iptables (standard syntax) — -I inserts at position 1 (evaluated first)
iptables -I INPUT 1 -s 198.51.100.23 -j DROP
```
**Notes:** `-I INPUT 1` inserts at the top so it is matched before any allow rule below — essential because first match wins (L04 p.14). This is exactly the reactive behavior of an IPS versus a passive IDS that only reports (L04 p.41); preemptive blocking like this risks a self-inflicted DoS on a misidentified legitimate user (L04 p.43).
