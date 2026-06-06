# 07. Social Engineering — Simulated Open-Book Questions

### [EASY] An attacker calls an employee on the phone, claims to be from the IT helpdesk, and pressures them to read out their password to "complete a security upgrade." Classify this attack and name the single defining channel that fixes the classification.

**Answer:** This is **vishing (voice phishing)** — phishing carried out by voice/phone call (L07 p.9; E07 p.1).

The defining feature is the **channel**: phishing is the umbrella technique (impersonating a trusted entity to extract sensitive information), and the sub-variant is determined purely by the medium used to reach the victim:

1. Voice/phone call → **vishing**.
2. SMS text message → **smishing**.
3. Email → plain **phishing**.

Here the contact is a live phone call, so it is vishing — not a separate, unrelated category but phishing over voice (L07 p.9). The "IT helpdesk" claim is an **authority** pretext and the "complete immediately" pressure is **urgency**, but those are persuasion levers, not the classifier. The classifier is the channel.

### [EASY] A receptionist sees the URL `arnazon.com` in an email link. Identify the specific URL-disguising trick and explain in one sentence why it is hard to spot.

**Answer:** This is **Trick 4 — (almost) indistinguishable domains using homoglyphs / typosquatting** (L07 p.36).

The trick works because `rn` placed next to each other (`a-r-n-azon`) visually resembles the single letter `m`, so `arnazon.com` reads as `amazon.com` at a glance. It is hard to spot because the substitution is at the character/glyph level rather than an obvious extra word or wrong domain — the eye auto-corrects look-alike characters, so even an attentive user reading the URL can miss it (L07 p.36). Other examples in the same trick class are `mircosoft.com` (transposed letters) and `fácebook.com` (an accented look-alike character).

### [EASY] An attacker leaves several USB sticks labelled "Salary Review 2026 — Confidential" in a company car park hoping an employee plugs one in. Classify the attack and name the persuasion principle the label exploits.

**Answer:** This is **baiting** — luring victims into compromising security by offering something tempting (L07 p.9). It also corresponds to the **"evil USB"** physical attack vector listed among SE methods (L07 p.8).

The label exploits **curiosity** (the desire to see what is on the confidential drive), which the lecture lists explicitly among its psychological techniques (L07 p.20). There is a secondary pull from **scarcity/exclusivity** — "Confidential" suggests privileged information few people are meant to see. The core mechanic of baiting is offering something tempting that the victim picks up and activates themselves, so the attacker never has to contact them directly.

### [EASY] An employee holds the badge-secured door open for a stranger carrying two coffee cups who says they "forgot their access card." Classify the physical attack and state the category (digital vs physical) it belongs to.

**Answer:** This is **tailgating (also called piggybacking)** — gaining unauthorized access to a restricted area by following an authorized person, often by pretending to have forgotten an access card or by carrying items to look like a busy employee (L07 p.10).

It belongs to the **physical** category of social-engineering methods (L07 p.10), alongside dumpster diving and shoulder surfing. The full coffee cups and the "forgot my card" story are the classic props: they make the attacker look like a legitimate, hands-full colleague so the door-holder feels socially obliged to help. The persuasion levers in play are **liking/social proof** (helping someone who looks like one of us) and **plausibility** (a believable everyday excuse).

### [EASY] A DNS record reads `v=spf1 a -all`. Name the mechanism, state which spoofing it defends against, and say what happens to mail from an unlisted server.

**Answer:** This is an **SPF (Sender Policy Framework)** record (L07 pp.38–39).

- **What it defends against:** **sender spoofing** — it lets the domain declare which servers are allowed to send mail on its behalf (L07 p.38).
- **What `v=spf1 a -all` means:** `a` authorizes the domain's current/own server (its A-record host) to send; `-all` (hard) means any other, unlisted server should **fail**.
- **What happens to mail from an unlisted server:** with `-all` the email **fails** SPF and is not delivered. (If the policy used a softfail `~all` instead, the mail would still be delivered but **marked** as failing verification.) (L07 p.38)

A key reminder: SPF only proves the *server* is authorized; it does not prove the *message* was unaltered — that integrity check is DKIM's job (L07 pp.40–41).

### [MEDIUM] An email arrives Saturday at 22:14 reading: "Nordea Security: unusual login detected. Verify your card within 1 hour or your account will be frozen. Click here." The visible link text says `www.nordea.dk` but hovering shows `nordea-verify.secure-login.com`. List the phishing indicators present and name the single most reliable one.

**Answer:** Working through the lecture's manual-detection checklist (L07 pp.25, 44):

1. **Mismatched/false link (most reliable indicator).** The visible text `www.nordea.dk` does not match the real destination `nordea-verify.secure-login.com`; the true registrable domain is `secure-login.com`, not Nordea. This is the **main** and **most reliable** indicator (L07 pp.25, 44).
2. **Suspicious timing.** A bank message at 22:14 on a Saturday is the exact "odd timing" red flag the Nordea example calls out (L07 p.25).
3. **Urgency / fear.** "Within 1 hour or your account will be frozen" manufactures panic to force a fast, unthinking action (L07 pp.20, 25).
4. **Suspicious request / content.** A bank pressing you to "verify your card" is the kind of request the lecture notes legitimate banks never make (L07 p.44).

The **single most reliable** indicator is the **URL/link check** (L07 p.44): timing, urgency and tone can all be faked convincingly in a polished email, but a link that does not lead to the real domain is hard for the attacker to hide and remains the strongest tell. Action: do not click — open the bank's site by typing the known address directly.

### [MEDIUM] Map each of these four lures to the persuasion principle it primarily exploits: (a) "Message from the CEO: wire this payment now, I'm in a meeting and can't talk." (b) "Only 3 license seats left at this price — expires midnight." (c) "Hi, it's Dave from your gym — saw you at spin class, can you confirm your member ID?" (d) "Your colleagues in Finance have already completed the mandatory training; complete yours here."

**Answer:** Using the lecture's persuasion-tactics and psychological-technique lists (L07 pp.19–20):

- **(a) → Authority (plus urgency).** Impersonating a senior figure ("the CEO") so the victim complies without questioning is the **authority** principle — "pretending to be someone important" (L07 p.20). The "in a meeting, can't talk" detail blocks out-of-band verification and adds **urgency**. This is the classic CEO-fraud / whaling lure (L07 p.28).
- **(b) → Scarcity (and urgency).** "Only 3 left" and "expires midnight" are the textbook **scarcity and urgency** lever — limited-time offer / "few spots left" to force a fast decision (L07 p.20).
- **(c) → Liking / trust and familiarity.** Posing as someone the victim knows from a shared social context (the gym) exploits **liking/social proof** and **trust and familiarity** — people do favors for those they like or who feel familiar (L07 pp.19–20).
- **(d) → Social proof.** "Your colleagues have already done it" pressures the victim to conform to the group — the **social proof** principle (people follow what their peers/in-group do) (L07 p.19).

### [MEDIUM] A traveler wants to open confidential company documents from a hotel using the free "Hotel_Guest_WiFi" network. Identify the relevant SE attack class and give two concrete mitigations — one user-side and one company-side.

**Answer:** The relevant attack class is **WiFi spoofing** — an attacker sets up a fake hotspot with a name mimicking a legitimate network (e.g., a rogue "Hotel_Guest_WiFi"), then intercepts traffic or runs a man-in-the-middle attack to capture credentials and document contents (L07 p.9; E07 pp.2–3).

**User-side mitigation:** Before connecting, confirm the network is the genuine hotel network (ask the front desk for the exact SSID), and only access sensitive systems over **encrypted, HTTPS/secured portals** — ideally tunnelled through the **company VPN** so even an attacker on the same network cannot read the traffic (E07 pp.2–3).

**Company-side mitigation:** Provide and **mandate a VPN** for remote access, enforce **MFA** so captured passwords alone are not enough, and publish a clear policy for accessing internal systems while travelling (E07 pp.2–3).

The underlying lesson: on an untrusted network, encryption (VPN/HTTPS) and a second authentication factor (MFA) are what protect you, because you cannot trust the network itself.

### [MEDIUM] A smishing SMS reads: "SDU HR: payroll issue after the system upgrade. Confirm before 16:00 today to avoid salary delays: http://hr-payroll-secure.sdu/verify". Explain why this message is unusually believable, and identify two red flags that still give it away.

**Answer:** **Why it is believable (the dangerous part):**

1. **Plausibility via a real recent event.** It references a genuine change — HR migrating to a new payroll platform — so it fits the victim's mental model of what is currently happening (L07 pp.18, 20). This is a **work pretext** built on a current event.
2. **Trusted-source impersonation.** It poses as a known internal department ("SDU HR"), invoking **authority** and **trust/familiarity** (L07 p.20).

**The red flags that still give it away (E07 p.2; L07 pp.25, 35):**

1. **Artificial deadline + fear of loss.** "Confirm before 16:00 today to avoid salary delays" manufactures **urgency and fear** to short-circuit careful thinking.
2. **Suspicious domain.** `http://hr-payroll-secure.sdu/verify` is **not** the real SDU domain — `hr-payroll-secure.sdu` is a fabricated, reassuring-sounding name (a similar-domain trick, L07 p.35), and it is plain `http`, not the official portal.

**Correct response:** do not click; reach the payroll system through the known official portal or contact HR via a verified channel (E07 p.2).

### [MEDIUM] A company has SPF configured but staff still receive emails where the display name reads "CEO Jane Smith" while the address is `jane.smith.ceo@gmail.com`. Explain why SPF did not stop this, and what control would address it.

**Answer:** **Why SPF did not stop it:** SPF only answers one narrow question — *"is the sending server authorized to send mail for the domain in the envelope/From address?"* (L07 pp.38–39). Here the attacker is **not spoofing the company's domain at all**: they are sending from a genuine Gmail account (`...@gmail.com`) and merely **falsifying the display name** to read "CEO Jane Smith" (L07 p.31). Because gmail.com is legitimately allowed to send for gmail.com, SPF passes cleanly. SPF protects the company's *own* domain from being forged; it does nothing about a lookalike address on a *different*, real domain.

**What would address it:** Technical email controls cannot fully solve display-name spoofing from a third-party domain. The realistic defenses are:

1. **Content/heuristic blocking** — flag external mail whose display name impersonates an internal executive, and add a **warning banner** on external/suspicious mail (L07 p.42).
2. **User awareness** — train staff that the **display name and even the address can be spoofed**, so they must check the actual domain and **verify any payment/data request out-of-band** through a known channel (L07 pp.31–32, 44; E07 p.3).

SPF/DKIM/DMARC harden *your* domain against being impersonated; a Gmail lookalike sidesteps all three (L07 p.45).

### [HARD] An attacker spends a week on OSINT before targeting a finance clerk: they read the CFO's LinkedIn (currently at a conference abroad), find the clerk's name on the company website, and learn from a press release that a new supplier was just onboarded. They then email the clerk "from" the CFO requesting an urgent wire to the new supplier. Trace this through the SE attack lifecycle and name every persuasion lever used.

**Answer:** **Lifecycle trace (L07 pp.11–19, 28):**

1. **Choosing a target (L07 p.12).** The clerk is an **explicit target** — a specific individual with valuable access (payment authority). The CFO is effectively a **pivoting identity**: rather than compromising the CFO's account, the attacker impersonates them to exploit the clerk.
2. **Information gathering / OSINT (L07 pp.14–17).** Three sources feed the attack: the CFO's **social media** (LinkedIn — reveals they are abroad and unreachable), the **company website** (clerk's name and role), and a **press release** (the new supplier). This is reconnaissance turned into personalization.
3. **Pretexting (L07 p.18).** A **work pretext built on a current event** — the genuinely just-onboarded supplier makes a wire request look routine and expected.
4. **Contacting the target (L07 p.13).** Email impersonating a trusted authority, with instructions to transfer money — i.e., **CEO fraud / whaling** (L07 p.28).

**Persuasion levers used (L07 pp.19–20):**

- **Authority** — the request appears to come from the CFO.
- **Urgency / fear** — "urgent wire," exploiting fear of disappointing a senior or delaying a deal.
- **Plausibility** — the real supplier and the CFO's real absence make the story believable enough not to question.
- **Trust/familiarity** — impersonating a known internal figure.

**Why the OSINT makes it deadly:** each fact (CFO abroad → can't be reached to verify; real supplier → request seems normal; clerk's name → personalized) closes a verification path. The correct defense is **out-of-band verification** of any payment request through a known channel, independent of the email (E07 p.3; L07 p.44), since the email's authority and plausibility are exactly what the attacker engineered.

### [HARD] Design a layered defense stack for an organization against email-based phishing. For each layer, name the control, state what it stops, and name its key limitation.

**Answer:** A defense-in-depth stack spanning technical and human controls (L07 pp.38–49):

1. **SPF (DNS record).** *Stops:* sender spoofing of your own domain by checking whether the sending server is authorized (L07 pp.38–39). *Limitation:* softfail only flags rather than blocks; does nothing about lookalike or third-party domains, and proves nothing about message integrity.
2. **DKIM (digital signature).** *Stops:* message spoofing/tampering and proves the mail genuinely originated from your domain via secret-key signing verified by the public key in DNS (L07 pp.40–41). *Limitation:* may be "too complicated for users to apply/understand," and signing must be set up correctly (L07 p.45).
3. **DMARC (policy layer).** *Stops:* sender spoofing by enforcing a policy on top of SPF/DKIM (L07 pp.44–45). *Limitation:* "might not help if the recipient does not know the valid sender address," and a misconfiguration can cause false negatives (L07 pp.45, 428-style trap).
4. **Content blocking / filtering.** *Stops:* known malicious domains (e.g., PhishTank), known malware, dangerous attachment types (`.exe`), lookalike domains, suspicious keywords (L07 p.42). *Limitation:* threat intelligence can be outdated; produces **false positives and false negatives** (L07 p.43). Allow-listing is too restrictive; warning banners shift burden to manual verification.
5. **User education & awareness.** *Stops:* the residual phishing that gets through, by training users to check URLs/attachments — the most reliable manual indicator (L07 pp.44, 47). *Limitation:* one-time measures don't stick (habits, new joiners, evolving threats), advice is often vague, and over-burdening users is unfair (L07 p.49).
6. **Simulated phishing campaigns (GoPhish/SET).** *Stops:* nothing directly, but **measures** vulnerability and reinforces training at the teachable moment via embedded learning (L07 p.48). *Limitation:* raises privacy/ethics issues (naming who clicked; consequences for users) (L07 pp.22, 49).

**Synthesis:** no single layer suffices — SPF/DKIM/DMARC harden *your* domain, content blocking catches *known* threats, and education plus simulation address the *human residual* that automation always leaves (L07 pp.43–46).

### [HARD] A user receives an email with the link `https://amazon.com/login?redirect=https://evilhacker.org`. They correctly read the domain as `amazon.com`, hover to confirm, and conclude it is safe. Explain why their reasoning is flawed, classify the trick, and explain why this trick defeats the lecture's "most reliable" manual indicator.

**Answer:** **Why the reasoning is flawed:** The user applied the right method (identify the true registrable domain — it genuinely is `amazon.com`) but the danger lives in the **query string**, not the domain. The `?redirect=https://evilhacker.org` parameter instructs the legitimate Amazon page to **forward the browser to the attacker's site** after loading. So the link starts at a real, trusted domain and *then* sends the victim somewhere malicious.

**Classification:** This is **Trick 5 — compromised legitimate websites / open redirects** (L07 pp.36, 183-style). Related forms are `evilhacker.amazon.com` (attacker-controlled subdomain) and `amazon.com/evilhacker` (a path on a compromised site).

**Why it defeats the "most reliable" indicator:** The lecture calls the **URL/attachment check** the most reliable *manual* indicator (L07 p.44) — but it also explicitly warns that open redirects are **"impossible to notice from the URL alone"** because the visible domain *is* the real one (L07 p.36). The user's verification step passes precisely because there is nothing wrong with the domain; the malicious behaviour is in the redirect parameter, which most users won't recognize. This is the gotcha that "the link looks like the real site is not enough" (L07 p.36) — even correctly identifying the registrable domain does not save you here. Responsibility shifts to the **site owner**, who must disable open redirects; the user's only safe move is to navigate to Amazon directly rather than via any link.

### [HARD] You are planning an *authorized* phishing simulation against your own organization using GoPhish. Lay out the campaign steps in order, state what metrics you will collect, and identify the ethical/privacy considerations you must address before launch.

**Answer:** **Campaign steps in order (L07 p.48; E07 p.5):**

1. **Launch GoPhish** and **configure SMTP** so the simulated emails can be sent.
2. **Create the landing page** — a fake login page that mimics a legitimate site, with a form to capture (and log) credential submissions.
3. **Define the target group** — the assigned, consenting population.
4. **Design the email** — a phishing lure with a malicious link (e.g., subject "Urgent: Account Verification") pointing at the landing page.
5. **Launch the campaign** — send to the target group.
6. **Track interactions** via the dashboard: email **open rates**, **click rates**, and **credential captures**.
7. **Review campaign data** — open rates, clicks, and submissions, then pair with awareness materials (embedded learning).

**Metrics collected (L07 p.48):** the simulation can capture, in increasing sensitivity: the **rate** of clicks/data entries; the **names** of people who clicked or entered data; and the **specific data** they entered on the page.

**Ethical / privacy considerations to address before launch (L07 pp.22, 48–49; E07 pp.4–5):**

1. **Scope & consent** — only target the assigned/consenting group; use **dummy emails and fake profiles**, never real third-party data (E07 pp.4–5).
2. **Naming individuals** — collecting names raises the pen-test ethics question of whether specific people should be identified in the report or to their employer (L07 p.22).
3. **Consequences for users** — decide in advance whether clicking or reporting carries consequences; punishing clickers (or reporters) undermines the security culture (L07 p.49).
4. **Data handling** — captured credentials/specific data are sensitive; store and dispose of them responsibly.
5. **Purpose limitation** — the goal is to *measure and teach* vulnerability and awareness effectiveness, not to entrap (L07 p.48).

### [HARD] A junior analyst argues: "Spelling mistakes are our best phishing detector — if an email is well written, it's safe." Refute this with reference to the lecture's manual-detection hierarchy, and explain what makes the spelling signal unreliable today.

**Answer:** The claim inverts the lecture's actual hierarchy of manual indicators (L07 p.44).

1. **Spelling/look-and-feel is the *weakest* signal, not the best.** The lecture lists "look and feel (e.g., spelling mistakes)" as an indicator only for **poorly made** phishing — it "might be enough to repel most attacks, but professional-looking phishing emails can be created" (L07 p.44). So a well-written email is *not* evidence of safety; it is exactly what a competent attacker produces.
2. **Why the signal degraded.** The lecture notes attackers now have **openly available tools, including generative AI**, to help craft campaigns (L07 p.29). AI-generated phishing has no spelling errors and can be highly **personalized**, which also defeats the *content* indicator ("hard to detect with personalized emails," L07 p.44).
3. **What the actual best indicator is.** The lecture names the **URL/attachment check** as the **most reliable** manual indicator — though it requires technical knowledge on the user's part (L07 p.44). Sender, security-feature, and content checks are intermediate and each have false-positive/false-negative weaknesses.

**Refutation in one line:** absence of spelling errors says nothing about authenticity; the analyst should check the **link/attachment destination** (and verify out-of-band for sensitive requests), because that is the indicator attackers find hardest to fake (L07 p.44; E07 p.3).

### [VERY HARD] A "fail-closed" trap: a company sets a strict SPF policy (`-all`) but does NOT publish DKIM, and a phishing email still reaches an employee, passes SPF, has no spelling errors, and uses the employee's real name and a current project reference. The employee asks "if all our security checks passed, isn't it safe?" Construct a rigorous rebuttal addressing each false assumption.

**Answer:** The employee has chained several plausible-but-wrong assumptions. Dismantling each:

1. **"SPF passing means the sender is who they claim."** False. SPF only confirms the **sending server is authorized for the domain in the From address** (L07 pp.38–39). A phishing email sent from a *different* domain the attacker legitimately controls (or a lookalike domain) **passes its own SPF** — SPF protects *your* domain from being forged, not you from a forged-looking message on another domain (L07 p.31). And display-name spoofing isn't covered at all.
2. **"No DKIM failure means the message is intact and trustworthy."** False on two counts. First, the company **doesn't publish DKIM**, so there is no signature to verify — absence of a DKIM failure is not a DKIM pass. DKIM's job is **message integrity and proof of origin** (L07 pp.40–41), and it simply isn't operating here. Second, even a valid DKIM signature would only prove the message came unaltered from *some* signing domain, not that the content is honest.
3. **"No spelling errors means it's legitimate."** False — the **weakest** signal. Spelling mistakes catch only poorly made phishing; **professional and AI-generated phishing emails have no spelling errors** and can be highly personalized (L07 pp.29, 44). The lecture explicitly warns not to rely on look-and-feel.
4. **"My real name and a real project reference prove authenticity."** False — this is the **opposite** of reassuring. Personalization is the product of **OSINT/reconnaissance** (L07 pp.14–17) and *defeats* the content indicator: the lecture notes suspicious-content detection is "hard to detect with personalized emails" (L07 p.44). A targeted, personalized message is **spear-phishing**, the more dangerous form.
5. **The deeper point — passing automated checks is not proof of safety.** Automated verification yields **false negatives** (phishing reaching the user), threat intel can be outdated, and a misconfigured/absent control gives a false sense of security (L07 pp.43, 45). The lecture's hierarchy says the **URL/attachment check** is the most reliable manual indicator (L07 p.44), and any payment/data request should be **verified out-of-band** (E07 p.3).

**Conclusion:** "All checks passed" here means *one* partial control (SPF) didn't flag a message that was never going to be flagged, while the stronger control (DKIM) doesn't exist and the human-facing signals were deliberately engineered away. The correct action is to verify the request through a known channel before acting.

### [VERY HARD] Two emails arrive. Email A: from `it-support@yourcompany.com` (your real domain), asking you to reset your password via a link to `yourcompany.com/login?next=https://creds-collect.io`. Email B: from `it-supp0rt@yourcompany.com` (zero for 'o'), with a link to `yourcompany.com.account-check.net`. Both claim a "company-wide security upgrade." Compare which defenses (SPF/DKIM/DMARC, content blocking, user check) catch each, and explain why one is harder to stop.

**Answer:** **Email B — the lookalike + external link.** This is the more *conventional* phish and the easier to catch:

- **Sender:** `it-supp0rt@yourcompany.com` uses a **homoglyph/typo** ("supp0rt" with a zero) — actually a spoof of, or a lookalike of, your domain (L07 pp.31, 36, Trick 4).
- **Link:** `yourcompany.com.account-check.net` — the true registrable domain is **`account-check.net`**, with your name buried as a subdomain (**Trick 2**, L07 p.35).
- **Defenses that catch it:** if the attacker forges your actual domain, **SPF/DKIM/DMARC** should fail because the sending server isn't authorized and the message isn't signed by your domain (L07 pp.38–45). **Content blocking** can flag the lookalike domain `account-check.net` and the suspicious external link (L07 p.42). **User URL check** works — reading right-to-left exposes `account-check.net` as foreign (L07 p.44).

**Email A — the real domain + open redirect.** This is **harder to stop**:

- **Sender:** `it-support@yourcompany.com` is your **genuine** domain. If the attacker has compromised an internal account or relay, the mail can **pass SPF, DKIM, and DMARC** — every domain-authentication control reports "legitimate," because it *is* from your domain (L07 pp.38–45).
- **Link:** `yourcompany.com/login?next=https://creds-collect.io` is an **open redirect (Trick 5)** — it starts on your real site and forwards to `creds-collect.io`. The lecture says this is **"impossible to notice from the URL alone"** (L07 p.36).
- **Why defenses struggle:** SPF/DKIM/DMARC all pass (authentic domain). Content blocking sees a link to *your own* trusted domain and is unlikely to block it. The **user URL check — the "most reliable" indicator (L07 p.44) — also fails**, because the visible domain is genuinely yours; the danger is hidden in the `next=` parameter, which most users won't parse.

**Why A is harder:** every layer that catches B (domain auth, content filter, manual URL check) is **defeated by A's use of a legitimate, authenticated domain plus an open redirect**. Stopping A requires the **site owner to eliminate open redirects** (L07 p.36) and, failing that, strict out-of-band verification — automated and manual link-checking both pass. B fails at least one external signal; A passes them all.

### [VERY HARD] Critically evaluate the claim: "If we deploy SPF, DKIM, and DMARC correctly, plus a content filter, we no longer need to spend money on user phishing training." Argue both why this is tempting and why the lecture's material refutes it, citing the specific attack classes that survive a fully technical stack.

**Answer:** **Why the claim is tempting:** SPF/DKIM/DMARC plus content filtering is a genuinely strong stack — it hardens your domain against being spoofed (SPF authorizes servers, DKIM proves integrity/origin, DMARC enforces policy) and blocks *known* malicious domains, malware, and dangerous attachments (L07 pp.38–42). Training is recurring, hard to measure, and the lecture itself admits one-time measures don't stick (L07 p.49), so cutting it looks efficient.

**Why the lecture refutes it — attack classes that survive a fully technical stack:**

1. **Lookalike / homoglyph domains (Tricks 3–4).** `amazon-shop.com`, `arnazon.com`, `fácebook.com` are *not* your domain, so SPF/DKIM/DMARC are irrelevant — they correctly authenticate as their own (attacker-owned) domains. Content filters need fresh, complete lookalike lists, and "registering all lookalike domains requires resources; attackers invent new tactics" (L07 pp.36, 45).
2. **Display-name spoofing from real third-party providers.** "CEO Jane Smith `<...@gmail.com>`" passes Gmail's own SPF/DKIM; no control on *your* side stops it (L07 p.31). DMARC "might not help if the recipient does not know the valid sender address" (L07 p.45).
3. **Open redirects / compromised legitimate sites (Trick 5).** Links through trusted, authenticated domains pass authentication and content filters and are "impossible to notice from the URL alone" (L07 p.36).
4. **Spear-phishing / personalized content.** OSINT-driven, error-free, personalized emails defeat the look-and-feel and content indicators (L07 pp.29, 44). Automated verification yields **false negatives** by design (L07 p.43).
5. **Non-email channels.** **Vishing** (phone) and **smishing** (SMS) bypass email controls entirely (L07 p.9; E07 p.1), as do **physical** vectors (tailgating, baiting, shoulder surfing) (L07 p.10).

**Synthesis:** the technical stack closes the *domain-authentication* and *known-threat* gaps but leaves the entire **human and out-of-channel residual** — exactly the cases the lecture flags as "unavoidable" reliance on the user (L07 p.45) and resolvable only by the **URL/attachment check (most reliable manual indicator)** plus **out-of-band verification** (L07 p.44; E07 p.3). The lecture's decision-making analysis explains *why* this residual is real: security choices are non-automatic, emotionally triggered, and treated as obstacles (L07 p.21), and there is a permanent gap between what users *want* and *need* to do (L07 p.46). Cutting training therefore removes the only defense against the attacks that the technical stack structurally cannot stop. **Verdict: the claim is false** — technical controls and training are complementary, not substitutes; the right model is defense-in-depth with recurring, actionable education (L07 pp.47–49).

### [VERY HARD] An ethics review board reviews a completed internal GoPhish campaign. The report names the 12 employees who entered credentials and recommends sending the list to their managers. Using the lecture's ethics and education material, argue what is defensible, what is problematic, and propose a policy that balances measurement against fairness.

**Answer:** **What is defensible:**

- **Running the simulation at all.** Phishing campaigns are a recognized form of SE penetration testing (L07 p.22), and GoPhish exists precisely to measure how vulnerable an organization is and how effective awareness measures are (L07 p.48). Collecting **rates** of clicks/credential entries is squarely within the legitimate measurement goal.
- **Using the results to teach.** Pairing the campaign with awareness materials / embedded learning at the teachable moment is exactly the recommended use (L07 pp.47–48).

**What is problematic:**

1. **Naming the 12 individuals and forwarding to managers.** The lecture's SE pen-test ethics explicitly raise the questions of **whether specific people should be named in reports** and **whether information found about them should be shared with their employer** (L07 p.22). Treating the name list as an automatic management hand-off skips that deliberation.
2. **Creating consequences for clicking.** The education material warns to consider whether there are **consequences for the user of clicking** (or reporting) (L07 p.49). Sending a "wall of shame" to managers manufactures punitive consequences, which discourages the very behavior you want — **reporting** future phishing — and shifts blame onto users for a systemic problem (L07 p.49).
3. **Privacy of specific data.** The campaign can capture the **specific data entered** (L07 p.48); retaining and circulating that is a privacy risk needing justification and limits.
4. **Misplaced responsibility.** Putting responsibility *solely on the user* ignores that security decisions are non-automatic, emotional, and obstacle-perceived (L07 pp.21, 49) — the 12 clickers are a signal about controls and training, not 12 culpable individuals.

**Proposed balanced policy:**

1. **Report aggregate metrics by default** (click rate, credential-entry rate, trend vs. prior campaigns) — names are *not* shared with managers (L07 pp.22, 48).
2. **Non-punitive, embedded learning.** Anyone who clicks is auto-enrolled in a short just-in-time training module at the teachable moment, framed as help, not discipline (L07 pp.47–49).
3. **Protect reporters.** Explicitly reward/normalize reporting and guarantee no penalty, so users learn *how* and feel safe to report (L07 p.49).
4. **Data minimization.** Capture only what the measurement needs; do not retain real credentials/specific data beyond analysis, and use dummy data where possible (L07 p.48; E07 pp.4–5).
5. **Repeat and improve.** Treat results as input to better controls and recurring training, since one-time measures and individual blame don't work (L07 p.49).

**Conclusion:** measuring and teaching is defensible; **naming-and-shaming to managers is not** — it violates the report-ethics and consequences cautions and would degrade reporting culture. A fairness-preserving policy keeps results aggregate, makes learning non-punitive, protects reporters, and minimizes data (L07 pp.22, 47–49).

### [VERY HARD] An attacker compromises a low-level employee's email account, then over two weeks quietly reads internal threads before emailing the finance team to change a real supplier's bank details. Explain why this "pivoting + long-term contact" approach defeats both technical email controls and user awareness, and identify the one control that could still catch it.

**Answer:** This combines several of the lecture's most dangerous ideas into one chain.

1. **Pivoting point (L07 p.12).** The compromised junior account is a **pivoting point** — a stepping stone used to launch the real attack from the *inside*. The attacker is no longer impersonating anyone externally; they are sending from a genuine internal mailbox.
2. **Why technical email controls fail.** SPF, DKIM, and DMARC all answer "is this mail genuinely from our domain?" — and here it **is** (L07 pp.38–45). The mail originates from the company's real server, signed by the real domain, fully authenticated. **Every domain-authentication control passes**, because the message is authentic; only the *intent* is malicious. Content filters also see normal internal traffic with no lookalike domain or known-bad link.
3. **Why user awareness fails.** The attacker spent two weeks in **long-term contact / observation** (L07 p.13), reading real threads to mirror tone, names, and context. The resulting request is maximally **plausible** and **personalized**, which the lecture says defeats the content indicator (L07 p.44). It comes from a known colleague (**trust/familiarity**, L07 p.20) on a real, in-progress topic — there is no spelling error, no suspicious URL, no external domain, and no obvious urgency. The "URL/attachment check," normally the most reliable manual indicator, has **nothing to flag** (L07 p.44).
4. **Why decision-making makes it worse.** Security verification is non-automatic and seen as an obstacle (L07 p.21); a routine-looking internal request about a real supplier is precisely the case where a busy user won't pause to verify (L07 p.46).

**The one control that could still catch it:** **out-of-band verification of the high-impact action itself** — i.e., a mandatory process to confirm any **change of supplier bank details / payment instruction** through an independent, pre-established channel (a known phone number, in person), never by replying to the email (E07 p.3; L07 p.44). Because every signal *inside* the email channel is authentic, the only remaining defense is to **break out of the channel** and verify the action against a second source. (Supporting controls: detect the original account compromise via MFA and anomalous-login monitoring, and apply least-privilege/segregation so a junior account cannot authorize payment changes — but for the email itself, out-of-band verification is the decisive catch.)
