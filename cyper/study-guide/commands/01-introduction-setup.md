# 01. Introduction & Set-up — Commands & Code Examples

### Update and full-upgrade the Kali attacker machine
**What:** Refreshes the package index and upgrades all packages on Kali — the standard "keep your attacker box current" step right after first login (E01 p.4–5, L01 p.44).
```bash
sudo apt update
sudo apt full-upgrade -y
sudo apt autoremove
```
**Notes:** Run as root or with `sudo` (Kali's non-root policy since 2020.1, L01 p.43). `apt autoremove` cleans orphaned dependencies "when suggested" (L01 p.44). NEVER run this against Metasploitable — targets must stay "as outdated as they were designed" (L01 p.44, E01 p.5).

### Become root / act as root on Kali
**What:** Elevates to root for commands that need it (e.g. `nmap` SYN scans, `arp-scan`), the way you do everything privileged on Kali since the non-root policy (L01 p.43).
```bash
sudo -i          # open an interactive root shell
sudo <command>   # run a single command as root
```
**Notes:** Default Kali account is the standard user `kali`/`kali`; there is no root login by default since release 2020.1 (L01 p.43). Change the default password after setup (E01 p.4).

### Show the current IP address(es) of an interface
**What:** Returns the IP address of the Kali (or any Linux) VM — the first thing you check to confirm DHCP gave you an address and to learn your own address before scanning (L01 p.45, recipe H).
```bash
ip address       # full form
ip addr          # short form
ip a             # shortest form
```
**Notes:** Look for `eth0` → `inet`, e.g. `inet 192.168.64.y` (recipe H). All three forms are equivalent (L01 p.45). On the older Metasploitable 2 Linux box you'll more often use `ifconfig` instead (see next block).

### Find the target's IP on Metasploitable 2 with ifconfig
**What:** Reads the IP of the Linux target (Metasploitable 2) from its own console so you know what address to point Kali at (recipe H).
```bash
ifconfig            # show all interfaces
ifconfig eth0       # just the primary interface
```
**Notes:** Look at `eth0` → `inet addr`, e.g. `192.168.64.x` (recipe H). `ifconfig` is the legacy tool still present on the old Metasploitable 2 image; on Kali prefer `ip addr`. Metasploitable 2 login is `msfadmin`/`msfadmin` (E01 p.5).

### Show the kernel routing table
**What:** Displays the routes/default gateway, used to confirm the VM has a path to the rest of the NAT Network and out to the internet (standard syntax; complements the `ip addr` checks in recipe H).
```bash
ip route             # show routing table + default gateway
ip route show
```
**Notes:** (standard syntax — the course names `ip` for address inspection at L01 p.45 but does not print `ip route` explicitly.) The `default via <gateway>` line is your NAT/NAT-Network gateway. Legacy equivalent: `route -n` or `netstat -rn`.

### Test reachability between attacker and target with ping
**What:** Sends ICMP echo requests from Kali to the Metasploitable target to prove the two VMs are on the same network and can talk — the core inter-VM connectivity check (recipe H, E01 p.9).
```bash
ping 192.168.64.10        # ping the target's IP
ping -c 4 192.168.64.10   # send only 4 packets then stop
```
**Notes:** Replies = the network works (recipe H, step 3). No replies on plain **NAT** mode is expected — NAT does not allow VM1↔VM2 traffic; switch to **NAT Network** (L01 p.41, E01 p.7, Gotchas). On Linux `ping` runs forever without `-c`; stop with `Ctrl+C`.

### Discover hosts on the local network with arp-scan
**What:** Lists live hosts on the attached subnet by ARP, used when you can't read the target's IP directly from its console (e.g. headless/crashing Metasploitable 3) (SOL p.1, recipe H step 4).
```bash
sudo arp-scan -l          # scan the local subnet of the default interface
sudo arp-scan --localnet
```
**Notes:** Requires root (`sudo`). The target's IP is often around `192.168.64.10` on the lab network (SOL p.1). This is the fallback when `ip addr`/`ifconfig` on the target isn't accessible.

### First nmap host-discovery / ping sweep of the lab network
**What:** Finds which hosts are up on the lab subnet — your first reconnaissance step from Kali once connectivity is confirmed (Nmap is the course's primary pen-testing tool, L01 p.9).
```bash
nmap -sn 192.168.64.0/24      # ping sweep: discover live hosts, no port scan
nmap 192.168.64.10            # default scan: top 1000 TCP ports on one host
```
**Notes:** (standard syntax — L01 p.9 names Nmap; exact flags not printed in this chapter's slides.) `-sn` ("no port scan") only does host discovery. Adjust `192.168.64.0/24` to match your actual `ip addr` subnet. Some scan types (e.g. SYN scan `-sS`) need `sudo`.

### Read basic system info on a host (uname / os-release / whoami)
**What:** Quick Linux recon to learn the kernel, OS version, and current user — the first things you check after landing on Kali or any Linux host (Linux command set, L01 p.45; standard recon syntax).
```bash
whoami                 # current username
uname -a               # kernel name, hostname, kernel version, architecture
cat /etc/os-release    # distro name and version (Debian/Kali/Ubuntu, etc.)
id                     # uid/gid and group memberships
```
**Notes:** (standard syntax — `whoami`/`uname`/`os-release` are not individually listed in the L01 p.45 command box, but `grep`/`cat`-style file reading is.) `uname -m` alone prints just the architecture (e.g. `x86_64`), useful to confirm you're on an amd64 image vs ARM (E01 p.2–3).

### Core Linux file navigation and management commands (Kali)
**What:** The everyday filesystem commands the lecture lists for working inside Kali during every later exercise (L01 p.45).
```bash
pwd                       # print the current directory
touch file.txt            # create an empty file
cp source.txt dest.txt    # copy a file
mv source.txt dest.txt    # move or rename a file
rm file.txt               # remove a file
rm -r mydir               # recursively remove a directory and its contents
```
**Notes:** Straight from the L01 p.45 command box. `rm -r` is irreversible — no recycle bin. Pair with `vi file` (or `vim`) to edit, also listed on the same slide.

### Search file contents and inspect binaries (grep / strings)
**What:** Find a string inside files, or pull readable text out of a binary — used in later exercises for log/output inspection and quick binary triage (L01 p.45).
```bash
grep "password" config.txt        # find lines containing the string
grep -r "admin" /etc/             # recurse through a directory
strings /bin/ls                   # extract printable strings from a binary
```
**Notes:** Both `grep string file` and `strings` appear in the L01 p.45 command list. `grep -i` makes the match case-insensitive; `strings` is handy for spotting hard-coded creds or version banners in a compiled file.

### Set the Kali keyboard layout (permanent and temporary)
**What:** Fixes a wrong keyboard layout on Kali — a common first-login annoyance when special characters land in the wrong place (L01 p.43).
```bash
sudo dpkg-reconfigure keyboard-configuration   # permanent, menu-driven
setxkbmap gb                                    # temporary: UK layout ('en_UK' on the slide is NOT a valid XKB code — use 'gb')
setxkbmap dk                                    # temporary: Danish layout
```
**Notes:** `dpkg-reconfigure` opens a TUI menu and persists across reboots; `setxkbmap` only lasts the current GUI session (L01 p.43). Useful when typing `|`, `/`, or `@` for commands gives the wrong character.

### Create and enable a VirtualBox internal-network DHCP server (host side)
**What:** Sets up automatic IP assignment on an isolated Internal Network for the advanced (Internal + NAT) lab setup — run from the host OS, not inside a VM (E01 p.9, recipe G).
```bash
VBoxManage list intnets          # list internal networks
VBoxManage list dhcpservers      # list existing DHCP servers
VBoxManage dhcpserver add \
   --network=CyberSecLab \
   --lowerip 172.30.1.20 \
   --upperip 172.30.1.50 \
   --netmask 255.255.255.0 \
   --ip 172.30.1.1 \
   --enable
```
**Notes:** Run on the **host** CLI; Windows users can `cd` to the folder containing `VBoxManage` to avoid full paths (E01 p.9). The `\` continues the command on the next line. The slide prints `--upperip 171.30.1.50` (a `171` typo) — the range should stay inside `172.30.1.0/24`, so use `172` (E01 p.9, Gotchas). Then select `CyberSecLab` as each VM's internal adapter.

### Install Metasploitable 3 (Windows target) via Vagrant (host side)
**What:** Command-line alternative to the GUI import for the Windows target box, run on the host (E01 p.6, recipe E).
```bash
vagrant plugin install vagrant-reload
vagrant plugin install vagrant-vbguest
vagrant box add rapid7/metasploitable3-win2k8
```
**Notes:** If a plugin errors, edit line 84 of `.vagrant.d/gems/3.3.8/gems/vagrant-vbguest-0.32.0/lib/vagrant-vbguest/hosts/virtualbox.rb` and change `File.exists` → `File.exist` (drop the trailing `s`); a `MountDiskImage` error is harmless (E01 p.6). Metasploitable 3 login is `vagrant`/`vagrant`.

### Convert a VirtualBox .vmdk disk to .qcow2 for UTM (Apple Silicon Macs)
**What:** Converts an x86 Metasploitable disk image to the format UTM uses, the required step for running the targets on an Apple Silicon Mac via emulation (MAC p.1, recipe I).
```bash
brew install qemu
qemu-img convert -p -f vmdk -O qcow2 Metasploitable.vmdk Metasploitable.qcow2
```
**Notes:** Apple Silicon (ARM) cannot run the amd64/x86 Metasploitable images natively, so Mac users use UTM + QEMU emulation at reduced performance (E01 p.2–3, MAC p.1). `-p` shows progress, `-f vmdk` is the input format, `-O qcow2` the output. Get the `.vmdk` from NextCloud (MS2) or the Vagrant portal (MS3).

### Fix Metasploitable 3 crashing on UTM by deleting VirtualBox guest drivers
**What:** Removes the VirtualBox Guest Additions drivers that crash the Windows target when it runs under UTM/QEMU instead of VirtualBox — run inside the MS3 Windows `cmd` shell (SOL p.1, recipe J).
```text
del C:\Windows\System32\drivers\VBoxMouse.sys
del C:\Windows\System32\drivers\VBoxGuest.sys
del C:\Windows\System32\drivers\VBoxSF.sys
del C:\Windows\System32\drivers\VBoxVideo.sys
rmdir /s /q "C:\Program Files\Oracle\VirtualBox Guest Additions"
```
**Notes:** Windows `cmd` syntax, not bash. Open `cmd` via Task Manager (`Ctrl+Shift+Esc` → File → New Task → `cmd`) after sending `Ctrl+Alt+Delete` (SOL p.1). Deletion may need several retries through repeated crashes; afterward the mouse won't work but MS3 runs stably (keyboard-only). A "Windows License is expired" screen is fine for lab use.
