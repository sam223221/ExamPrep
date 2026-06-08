# 07. Social Engineering — Commands & Code Examples

### Launch the Social-Engineer Toolkit (SET)
**What:** Open SET on Kali to begin a controlled phishing-simulation exercise (E07 p.3).

```bash
# Standard launch (needs root because SET binds web/listener ports)
sudo setoolkit
```

**Notes:** Authorized testing only — the lab requires you to use dummy emails / fake profiles and only target your assigned, consenting group (E07 pp.4–5). On first run SET asks you to agree to the terms of service (type `y`). If `setoolkit` is not on PATH, the binary lives at `/usr/share/setoolkit/setoolkit` — running it without `sudo` will fail to start the credential-harvester listener.

### Navigate SET to the spear-phishing attack menu
**What:** Walk SET's menus to the Email Attack / spear-phishing feature used in Exercise 5 to craft the phishing email (E07 p.4).

```text
setoolkit main menu (standard syntax):
  1) Social-Engineering Attacks      -> type 1, Enter
  2) Penetration Testing (Fast-Track)
  3) Third Party Modules
  ...

Social-Engineering Attacks menu:
  1) Spear-Phishing Attack Vectors   -> type 1, Enter

Spear-Phishing menu:
  1) Perform a Mass Email Attack
  2) Create a FileFormat Payload
  3) Create a Social-Engineering Template
  -> choose 1 to send the crafted phishing email to the target group
```

**Notes:** Authorized testing only. Menus are numeric — you type the number and press Enter at each level. The Email Attack feature is what the lab calls for to build the message body containing (a) a malicious link to a fake login page, (b) urgency/fear ("Your account has been compromised!"), and (c) personalization (name, company) (E07 p.4). Press `99` to go back one menu; `Ctrl+C` aborts.

### Clone a login page with SET's credential harvester
**What:** Use SET's Website Attack feature to stand up a fake login page that captures whatever a target types (E07 p.4; credential-stealing mechanism, L07 p.26).

```text
Social-Engineering Attacks menu:
  2) Website Attack Vectors          -> type 2, Enter

Website Attack Vectors menu:
  3) Credential Harvester Attack Method -> type 3, Enter

Credential Harvester menu:
  2) Site Cloner                     -> type 2, Enter

Prompts (standard syntax):
  IP address for the POST back in Harvester/Tabnabbing [<your-Kali-IP>]: 10.0.0.5
  Enter the url to clone: https://accounts.google.com
  -> SET clones the page and starts a listener; captured creds print to the terminal
```

**Notes:** Authorized testing only. The "POST back" IP is where the victim's submitted credentials are sent — use your own Kali IP on the lab network. Make the clone look legitimate (matching colours, logos, fonts, layout) so the exercise is realistic (E07 p.4). For the defense analysis, note what tells (cloned-site artifacts, wrong domain in the address bar) help a user spot it (E07 p.4).

### Launch GoPhish and reach the admin dashboard
**What:** Start the GoPhish server for the Exercise 6 simulation and find the temporary admin login (E07 p.5; L07 p.48).

```bash
# From the GoPhish directory on Kali (standard syntax)
./gophish

# Watch the startup log for the admin URL and one-time password, e.g.:
#   Please login with the username admin and the password <random-temp-pw>
#   admin server started https://127.0.0.1:3333
```

**Notes:** Authorized testing only. The admin UI is at `https://127.0.0.1:3333` (self-signed cert — accept the browser warning); the phishing landing pages are served on the separate phish listener (port 80 by default). On modern GoPhish the temporary admin password is printed to the log on first run — copy it before the log scrolls. You must change it on first login.

### Configure the GoPhish sending profile (SMTP)
**What:** Tell GoPhish which mail server to send the simulated phishing emails through — step 2 of Exercise 6 (E07 p.5).

```text
GoPhish dashboard (standard steps):
  Sending Profiles -> New Profile
    Name:           Lab SMTP
    From:           IT Support <it-support@lab.local>
    Host:           127.0.0.1:25        (your lab SMTP relay host:port)
    Username/Pass:  (if the relay requires auth)
    [ ] Ignore Certificate Errors  (tick only for a self-signed lab relay)
  -> Send Test Email to confirm delivery, then Save Profile
```

**Notes:** Authorized testing only — send only to your assigned group (E07 p.5). The `From:` address is where sender-spoofing concepts bite: a real recipient domain with SPF/DKIM/DMARC would softfail or fail this spoofed sender (L07 pp.38–45). Use a lab/relay address, never a real person's mailbox. "Send Test Email" verifies the SMTP profile before you launch the whole campaign.

### Build a GoPhish landing page, email template, group, and campaign
**What:** The full GoPhish object chain — landing page, email, target group, then the campaign that ties them together (E07 p.5).

```text
GoPhish dashboard order (standard steps):
  1) Landing Pages -> New Page
       - Import Site (paste a real login page's HTML) OR write the form
       - tick "Capture Submitted Data" and "Capture Passwords"
       - set "Redirect to" a real site after submit (less suspicious)
  2) Email Templates -> New Template
       - Subject: "Urgent: Account Verification"
       - Body includes the tracking link variable {{.URL}}
  3) Users & Groups -> New Group
       - add the target group's dummy addresses (same group as Exercise 5)
  4) Campaigns -> New Campaign
       - pick the Email Template, Landing Page, Sending Profile, and Group
       - set the "URL" to your Kali phish-listener address
       - Launch
```

**Notes:** Authorized testing only. `{{.URL}}` is the per-recipient tracking link GoPhish injects — that is how it knows who clicked. "Capture Passwords" is exactly the privacy-sensitive data the lecture flags: simulations can record the specific data a user entered, not just click rates (L07 p.48). Keep the same target group as Exercise 5 so results are comparable (E07 p.5).

### Track open, click, and credential-capture rates in GoPhish
**What:** Read the campaign dashboard to measure how vulnerable the group is — the goal of a simulated campaign (E07 p.5; L07 p.48).

```text
GoPhish dashboard -> Campaigns -> <your campaign>:
  - Timeline events per recipient:
      Email Sent -> Email Opened -> Clicked Link -> Submitted Data
  - Summary funnel shows counts/percentages for each stage
  - "Submitted Data" rows reveal the exact credentials entered (if captured)
```

**Notes:** Authorized testing only. These three rates (open / click / credential-capture) are the core campaign metrics named in both the lab and lecture (E07 p.5; L07 p.48). The "Submitted Data" view is privacy-sensitive: the SE pen-test ethics ask whether individuals should be named and whether findings go to their employer (L07 p.22) — handle results accordingly.

### Look up a domain's SPF record with dig
**What:** Read the SPF TXT record to see which servers a domain authorizes to send its mail (L07 pp.38–39).

```bash
# SPF lives in the root-domain TXT record (standard syntax)
dig TXT example.com +short

# Filter to just the SPF line if there are several TXT records
dig TXT example.com +short | grep "v=spf1"
```

**Notes:** A result like `"v=spf1 a -all"` means "only this domain's A-record server may send; everything else fails" (L07 p.39). The trailing mechanism is the policy: `-all` = hard **fail** (block), `~all` = **softfail** (deliver but flag), `?all` = neutral (L07 p.38). No `v=spf1` line at all means the domain published no SPF — spoofing is not checked. Read-only DNS query; safe to run against any domain.

### Look up a domain's DMARC policy with dig
**What:** Fetch the DMARC record, which always sits at the `_dmarc` subdomain (L07 pp.44–45).

```bash
# DMARC is published at _dmarc.<domain> (standard syntax)
dig TXT _dmarc.example.com +short
```

**Notes:** A reply such as `"v=DMARC1; p=reject; rua=mailto:dmarc@example.com"` means the domain's policy on SPF/DKIM failure is `p=reject` (also `p=quarantine` or `p=none` for monitor-only). DMARC is the policy layer built on SPF + DKIM and protects against sender spoofing — but only helps if the recipient knows the valid sender address (L07 p.45). Empty result = no DMARC, so failing mail is handled by SPF/DKIM defaults alone.

### Look up a DKIM public key by selector with dig
**What:** Retrieve a domain's DKIM public key so signatures can be verified — note DKIM keys are stored under a selector (L07 pp.40–41).

```bash
# DKIM record lives at <selector>._domainkey.<domain> (standard syntax)
dig TXT default._domainkey.example.com +short

# The selector is taken from the s= tag of a real DKIM-Signature header, e.g. s=google
dig TXT google._domainkey.example.com +short
```

**Notes:** You must know the **selector** — it is not guessable. Find it in a received email's `DKIM-Signature:` header (`s=<selector>`), then query `<selector>._domainkey.<domain>`. A hit looks like `"v=DKIM1; k=rsa; p=MIGfMA0G..."` — the `p=` value is the public key Bob's server uses to verify the signature, proving the message came from the domain and was not altered in transit (L07 p.41). Read-only query.

### Send a spoofed test email with swaks (authorized lab only)
**What:** Use swaks to send a test message with a forged sender, demonstrating SMTP's lack of built-in sender authentication (L07 pp.30–32).

```bash
# Standard syntax — forge the From header through a lab relay
swaks --to victim@lab.local \
      --from "IT Support <it-support@lab.local>" \
      --server 127.0.0.1:25 \
      --header "Subject: Urgent: Account Verification" \
      --body "Please verify your account: http://10.0.0.5/login"
```

**Notes:** Authorized testing only — this forges a sender and must never be aimed at real mailboxes outside your consenting lab group. It works because SMTP (designed 1980) has no built-in sender verification (L07 p.30); the `--from` value is whatever you claim. If the recipient domain has SPF set to `-all` (and DMARC `p=reject`), this spoofed mail will **fail** and be blocked — running it both demonstrates the attack and lets you observe the defense (L07 pp.38–45). swaks is a simple SMTP test tool; `--server` points at your lab relay.

### Inspect an email's headers to spot a phishing message
**What:** Read the raw `Received`, `Authentication-Results`, and `DKIM-Signature` headers to judge whether a message is spoofed (L07 pp.30–32, 41, 44).

```text
What to read in the raw headers (standard fields):
  Received:                bottom-up chain of relays — does the originating
                           server belong to the claimed sender's domain?
  Return-Path:             the real envelope sender (often differs from "From:")
  Authentication-Results:  spf=pass/fail, dkim=pass/fail, dmarc=pass/fail
  DKIM-Signature:          d=<signing domain>  s=<selector>
                           -> does d= match the From: domain?
  From:                    display name vs. actual address (both spoofable)
```

```bash
# In a mailbox you can save the raw .eml and grep the auth verdict
grep -iE "^(Received|Return-Path|From|Authentication-Results|DKIM-Signature):" message.eml
```

**Notes:** The single most reliable manual indicators are the auth verdicts plus a `From:`/`d=` mismatch. `spf=fail` or `dmarc=fail` in `Authentication-Results`, a `Received` chain that does not originate from the claimed domain, or a `DKIM-Signature` whose `d=` differs from the `From:` domain all point to spoofing (L07 pp.31–32, 41). Remember both the display name and the address can be forged, so "the From line looks right" is not proof (L07 p.32). Read-only inspection.

### Extract every URL from a suspicious message
**What:** Pull all links out of a saved email so you can examine the true destinations instead of clicking — the most reliable phishing check (L07 pp.34–36, 44).

```bash
# Extract http/https links from a raw .eml (standard syntax)
grep -oE "https?://[^\"'<> ]+" message.eml | sort -u
```

**Notes:** Inspect each URL for the lecture's URL-disguising tricks: a legit name buried as a subdomain/path (`amazon.com.evilhacker.com`), look-alike/homoglyph domains (`arnazon.com`, `fácebook.com`), URL shorteners, and open redirects (`...?redirect=https://evilhacker.org`) (L07 pp.34–36). Read the domain right-to-left to find the true registrable domain. Never paste extracted URLs into a live browser on a production machine — copy them into a checker / expand shorteners explicitly (L07 p.34). The URL/attachment check is the most reliable manual indicator but requires user knowledge (L07 p.44).

### Expand a shortened URL without visiting it
**What:** Reveal where a `tinyurl`-style short link actually points (Trick 1, URL shorteners, L07 p.34).

```bash
# Follow redirects with curl but DON'T download the body (standard syntax)
curl -sIL "https://tinyurl.com/bffte48x" | grep -i "^location:"
```

**Notes:** `-I` does a HEAD request (no page body), `-L` follows redirects, and grepping `Location:` prints each hop so you see the final destination without rendering attacker content. URL shorteners are hard to judge by eye because the real target is hidden until you follow it (L07 p.34). For an unknown/untrusted link, prefer a dedicated URL-expansion/checker service over hitting it yourself, and run it from an isolated environment.

### Spot the URL-disguising tricks (reference cheat sheet)
**What:** Quick reference mapping each disguise trick to what the true domain really is (L07 pp.34–36).

```text
Trick 0  No trick:           182.15.128.103  / evilhacker.org   -> obvious
Trick 1  Shortener:          tinyurl.com/bffte48x               -> expand it
Trick 2  Legit name in URL:  amazon.com.evilhacker.com          -> real domain = evilhacker.com
                             evilhacker.com/www.facebook.com    -> real domain = evilhacker.com
Trick 3  Similar domain:     amazon-shop.com                    -> NOT amazon.com
Trick 4  Homoglyph/typo:     arnazon.com (rn->m), fácebook.com  -> look-alike characters
Trick 5  Open redirect:      amazon.com/login?redirect=https://evilhacker.org
                             -> real site, but forwards to attacker
```

**Notes:** Tricks 0–4 are spottable by carefully reading the registrable domain (right-to-left); Trick 5 (compromised site / open redirect) is impossible to detect from the URL alone — the site owner must fix it (L07 p.36). Mobile clients truncate URLs, which makes Tricks 2–3 more dangerous (L07 p.35). This is a reading aid for the header/URL-extraction steps above, not a command to run.
