# 07. Social Engineering

> Source material: `L07_Social Engineering.pdf` (52 slides) and `E07.pdf` / Lab 03 (5 pages). All claims below are grounded in these two documents. Inline citations use the form `(L07 p.X)` for the lecture slides and `(E07 p.X)` for the lab. Where the lecture is silent on a detail, this is stated explicitly rather than guessed.

---

## Overview — what this topic covers and why it matters

Social engineering is the human-facing side of cybersecurity. The lecture defines it as "any act that influences a person to take an action that may or may not be in their best interest" and, more pointedly, as "a psychological manipulation technique used to persuade individuals into making decisions or disclosing information they might not otherwise share" (L07 p.7). Rather than breaking into systems through technical vulnerabilities, the attacker exploits the **person** who has legitimate access — tricking them into revealing credentials, running malware, transferring money, or granting physical access. It is "commonly associated with cybersecurity threats such as phishing, pretext, and impersonation," but the same tactics appear in "traditional" scams, and the techniques can even be used ethically (e.g., to drive positive behavioral change) (L07 p.7).

This topic matters because people are frequently the weakest link and the hardest to "patch." The lecture's central worked example is **phishing** — a variant of social engineering where an attacker impersonates a trusted entity over email or another channel (L07 p.25) — and a large part of the material is devoted to how phishing works (credential stealing, malware infiltration, CEO fraud), how attackers disguise malicious URLs, and how defenders fight back with technical controls (SPF, DKIM, DMARC, content blocking) and human controls (user education, simulated phishing campaigns). The accompanying lab (E07) has you both **identify** social-engineering attacks (phishing, vishing, smishing) and **run controlled phishing simulations** using the Social Engineer Toolkit (SET) and GoPhish in a Kali Linux environment (E07 p.1). By the end you should be able to explain the SE attack lifecycle, the psychological principles attackers exploit, how phishing is carried out, and the techniques for detecting and preventing it (L07 p.6).

---

## Key Concepts

### What social engineering is

**What:** Any act that influences a person to take an action that may or may not be in their best interest; equivalently, a psychological manipulation technique used to persuade individuals into making decisions or disclosing information they might not otherwise share (L07 p.7).

**Why it matters:** It targets the human, not the machine. It is commonly tied to cybersecurity threats (phishing, pretext, impersonation) but also appears in everyday scams (L07 p.7).

**How:** The attacker builds a believable context (a *pretext*) and applies *persuasion tactics* to push the target toward the desired action. The lecture stresses that social engineering is "often associated with malicious intent, but it can also be used for positive and ethical purposes," e.g., behavioral change for individual or societal benefit (L07 p.7).

### Methods of attack — digital vs. physical

The lecture splits SE methods into **digital** and **physical** categories (L07 p.8). The umbrella list of attack methods includes: phishing e-mails, spear-phishing emails, credential harvesting, whaling (CEO fraud), smishing, "evil USB," attached files (PDF, Excel, e-mail), and visiting on site (L07 p.8).

**Digital methods (L07 p.9):**
- **Phishing** — a deceptive tactic where attackers impersonate a trusted entity to trick users into revealing sensitive information. Sub-variants:
  - **Vishing (Voice Phishing)** — phishing carried out by voice/phone call.
  - **Smishing (SMS Phishing)** — phishing carried out via SMS text message.
- **Baiting** — luring victims into compromising security by offering something tempting.
- **Waterholing (watering the hole)** — compromising a legitimate website that is frequently visited by a target group, so visitors get attacked.
- **WiFi Spoofing** — setting up fake WiFi hotspots with names that mimic legitimate networks.

**Physical methods (L07 p.10):**
- **Dumpster Diving** — searching trash bins or discarded documents for sensitive information; even shredded documents can sometimes be reconstructed.
- **Tailgating (Piggybacking)** — gaining unauthorized access to a restricted area by following an authorized person, often by pretending to have forgotten an access card or by carrying items to look like an employee.
- **Shoulder Surfing** — physically observing someone enter sensitive information, e.g., watching a person type a password/PIN at an ATM or login screen, overhearing confidential conversations in cafés or on public transport, or observing sensitive documents left open on desks/screens.

### The social engineering attack lifecycle

The lecture presents the attack as a lifecycle with named stages (L07 p.11). The textual stages described in the slides are:

1. **Choosing a target (L07 p.12)** — identify which people have access to the data or system components of interest; this often involves information gathering. The initial target can be a *pivoting point* — a stepping stone for further attacks (e.g., compromising an employee's account to send internal emails). Target specificity comes in three forms:
   - **Explicit target** — focus on specific individuals with valuable access, e.g., a CEO.
   - **Opportunistic target** — target a large group to increase the chance of success, e.g., mass phishing emails.
   - **Hybrid approach** — combine both, e.g., setting up a malicious WiFi network.
2. **Contacting the target (L07 p.13)** — the method of contact depends on the attacker's goal: extract sensitive information (passwords, financial data), deploy malware on the victim's device, or gain physical/remote access to a system or network. Contact can be one-off or a long-term relationship/observation, and manual or automated. Success is increased via personalization (from information gathering) and pretexts/persuasion tactics. (The Social Engineering Toolkit is referenced here as a contact tool.)
3. **Information gathering** runs through the contact phase (covered next).

> Note: slide 11 shows a lifecycle diagram as an image; the slides' text names the "Choosing a target" and "Contacting the target" stages explicitly (L07 pp.11–13). The lecture does not spell out a fixed numbered list (e.g., the classic "reconnaissance → hook → play → exit"), though the learning objectives do say you should be able to explain the stages "from reconnaissance to execution" (L07 p.6).

### Information gathering (reconnaissance / OSINT)

Information gathering feeds personalization and pretexting. The lecture lists sources by category (L07 pp.14–17):

**General sources (L07 p.14):** content from search engines, content from web pages, content accessed anonymously, and the **OSINT Framework**.

**Personal information (L07 p.15):**
- Governmental records (e.g., services like krak.dk).
- Social media, including forums and message boards:
  - Basic information: name, employment, relationship status.
  - Usernames — can be used to identify the same person's other online accounts.
  - Interactions with people/services: likes, check-ins, friends.
- Content posted by *others*: friends/family on social media, the company website, media reports.
- (Reference given: `osintdojo.com/diagrams/person`.)

**Organizations & data breaches (L07 p.16):**
- Public records, e.g., the CVR register, court documents.
- DNS records (e.g., via whois.com).
- Information directly from the company: website, press releases, social media.
- Information from company employees (e.g., their social media).
- Information about user accounts (e.g., passwords/login credentials from breaches).

**Financial information (L07 p.17):**
- Public information, e.g., tax records.
- Leaks, e.g., financial papers, payment-service transactions.
- Cryptocurrency analysis: transaction history of a public key plus network analysis, spending/income patterns, exchange activity and wallet connections, and identities connected to certain accounts (personal/business pages, location).

### Pretexting

**What:** A pretext is the fabricated context/story the attacker uses to make contact believable (L07 pp.13, 18).

**How (examples, L07 p.18):**
- **Work pretext** — use a current event to make conversations convincing.
- **Personal pretext** — leverage personal information.
- **Work + Personal** — combine work and personal information to make the approach more believable and to establish further rapport with the target.

### Persuasion tactics and psychological principles

The lecture gives two overlapping lists of persuasion levers.

**Persuasion tactics: examples (L07 p.19):**
- **Offering or promising a reward** — exploiting people's response to being offered rewards.
- **Liking and social proof** — people do favors for those they like or for members of their own social group.
- **Trustworthiness** — based on appearance (of people, companies, websites).
- **Appeal to authority** — people are likely to follow authority and urgency.

**Psychological techniques (L07 p.20):**
- **Authority** — pretending to be someone important.
- **Fear and Urgency** — creating panic so the victim acts quickly.
- **Scarcity and Urgency** — limited-time offer or "few spots left."
- **Trust and Familiarity** — pretending to be someone the victim knows or trusts.
- **Plausibility** — making the request believable enough that the victim does not question it.
- Also listed: **Curiosity, Reciprocity, Convenience**, etc.

> These map onto Cialdini's classic principles of persuasion (authority, social proof/liking, scarcity, reciprocity, commitment/consistency). The lecture names authority, social proof, liking, reciprocity, scarcity, and trust explicitly but does **not** cite Cialdini by name or list a canonical "six principles" — so for the exam, attribute these to the lecture's own lists (L07 pp.19–20) rather than to Cialdini unless the exam framing asks for the academic source.

### Why decision-making makes people vulnerable

The lecture explains *why* people fall for SE by examining how security decisions get made (L07 p.21):
- **Context-Dependent Decisions** — people make security decisions based on the situation.
- **Emotional Triggers** — decisions made based on emotions.
- **Non-Automatic Decisions** — security actions are often not automatic; they require active thought and decision-making.
- **Cognitive Bias** — security-related tasks are perceived as obstacles.
- **Barriers to Compliance** — security tasks like verifying emails or checking physical security are often viewed as annoyances.

This is reinforced later (L07 p.46): users find phishing hard to detect because there is a gap between "what the user *wants* to do" (process their email and get on with work) and "what the user *needs* to do" (carefully verify each message).

### Social engineering penetration testing (ethics)

SE can be tested like classical pen-testing: let an external team of experts try to attack the organization using SE methods (L07 p.22). Phishing campaigns are themselves considered penetration testing in the SE context (L07 p.22). Key ethical issues to consider (L07 p.22):
- How much information can one get about a person/company? Are illegal/"gray-area" sources (e.g., the contents of leaked data breaches) acceptable to use? Is active social engineering (directly contacting the target or their social circle) acceptable?
- Which pretexts and persuasion tactics are ethical to use?
- How are results reported — should specific people be named? Should information found about them via information gathering be shared with their employer?

**Worked SE scenario (L07 p.23):** A security guard (John) is approached by a visibly pregnant woman who feels unwell and needs to come inside to use a phone and bathroom. Options: *ignore the request* (she might have a real medical emergency) vs. *let her in* (she might plant eavesdropping devices or malware-laden removable media). The lecture's suggested resolution: have a **second security guard** stay at the entrance while John helps her, ensuring she does not do anything suspicious — i.e., balance compassion against security with compensating controls.

### Phishing — definition and indicators

**What:** Phishing is a variant of social engineering where the attacker sends emails (or messages via other channels, e.g., SMS) impersonating a trusted entity (L07 p.25).

**How to tell a message is fake (Nordea example, L07 p.25):**
- **Main indicator:** the link does not lead to the real (Nordea) website.
- **Other possible indicators:** timing of the message (e.g., a Saturday evening), spelling mistakes, and content invoking a sense of urgency.

### How phishing works — three mechanisms

**1. Credential stealing (L07 p.26):**
1. User gets an email with a link to a trusted organization's website.
2. The link goes to a site that *looks* like the real one but is owned by the attacker.
3. The user is prompted to enter credentials.
4. Credentials are forwarded to the attacker.
5. The attacker gains full control over the user's account.

**2. Malware infiltration (L07 p.27):**
1. User gets an email with an attached file.
2. User opens the attachment.
3. The attachment runs a malware script.
4. Malware gains control over the user's system (e.g., exfiltrating data) and/or propagates to other users/devices on the network.
5. In rare cases malware can run *without* the user opening the file — by clicking the link, or even just reading the email — especially dangerous on systems without security updates.

**3. CEO fraud / whaling (L07 p.28):**
1. User gets an email impersonating a trusted person/authority.
2. The email contains instructions: transfer money, share sensitive documents, etc.
3. The user follows the instructions.

**Regular phishing — the attacker's investment (L07 p.29):**
- Register email addresses to use for the phishing mailing.
- Register a website that looks like the one the attacker wants to impersonate, **or** prepare malware to be attached.
- Send out the phishing emails.
- Openly available tools — including **generative AI** — exist to help. (The Social Engineering Toolkit is referenced here.)

### How email enables spoofing (SMTP weaknesses)

Email runs on **SMTP (Simple Mail Transfer Protocol)**, originally designed in 1980 with **no initial security considerations** in mind (L07 p.30). This is what makes spoofing possible.

**Sender spoofing — sender's name (L07 p.31):** The sender's *display name* is falsifiable. Eve sends from a public mail server (mail.com) but sets `From: Alice <eve@mail.com>`. The sender address can be made to look similar enough to be believable — e.g., `alice@mail.com` (if Alice never registered that account) or `alice@eve.com`.

**Sender spoofing — sender's address (L07 p.32):** The sender's actual email *address* is falsifiable if the attacker controls the server, or if the email provider's server is incorrectly configured — Eve sends `From: Alice <alice@alice.com>` from her own eve.com server.

### Website spoofing and URL-disguising tricks

In a website-spoofing email (L07 p.33), the real link destination can be hidden behind the visible link text and only revealed via the tooltip when hovering. Attackers use a graded series of tricks (L07 pp.34–36):

- **Trick 0 — No trick:** raw IP or obvious domain like `evilhacker.org` / `182.15.128.103`. Should be easy to detect, but the user still must pay attention to the URL (L07 p.34).
- **Trick 1 — URL shorteners:** e.g., `https://tinyurl.com/bffte48x`. Hard to distinguish without clicking; services exist to expand/check shortened URLs but must be used explicitly (L07 p.34).
- **Trick 2 — Legitimate website as part of the URL:** `amazon.com.evilhacker.com` or `evilhacker.com/www.facebook.com`. A problem if the user does not know how to identify the *real* domain, or if only part of the URL is shown (e.g., on mobile) (L07 p.35).
- **Trick 3 — Similar domains:** `amazon-shop.com` instead of `amazon.com`. A problem if the user does not know what the real website is (L07 p.35).
- **Trick 4 — (Almost) indistinguishable domains (homoglyphs/typosquatting):** `arnazon.com` (rn≈m), `mircosoft.com`, `fácebook.com` (accented character), `apple.com` with a look-alike character. Especially hard to notice (L07 p.36).
- **Trick 5 — Compromised legitimate websites / open redirects:** `evilhacker.amazon.com`, `amazon.com/evilhacker`, or `amazon.com/login?redirect=https://evilhacker.org`. Impossible to notice from the URL alone — the website owners must take measures (L07 p.36).

### Domain verification defenses: SPF, DKIM, DMARC

These are the technical anti-spoofing controls (L07 pp.38–45).

**SPF (Sender Policy Framework) — defends against sender spoofing (L07 pp.38–39):**
- **Threat:** Eve uses her own server (eve.com) to spoof the sender as `alice@alice.com`.
- **Idea:** Bob's server checks with Alice's domain (alice.com) whether the sending server (eve.com) is *allowed* to send on Alice's behalf.
- **If not allowed:** either **softfail** (email delivered to Bob but marked as failing verification) or **fail** (email not delivered).
- SPF is published as a DNS record, e.g., `v=spf1 a -all` — allow the current server to send; unverified emails are not delivered. Variants can add other servers and IP ranges. Free SPF record generators are available online (L07 p.39).

**DKIM (DomainKeys Identified Mail) — defends against *message* spoofing (L07 pp.40–41):**
- **Threat:** Eve intercepts a message Alice sent and changes its content before it reaches Bob.
- **Solution:** digital signatures via DKIM. The **secret key** of alice.com is needed to sign the message; the **public key** of alice.com (published in DNS) is needed to verify the signature.
- The signature ensures the email was sent via alice.com **and** has not been tampered with in transit (L07 p.41). Bob's server checks: "Has this message been signed with the public key of alice.com?" The public key lives in a DNS record, e.g., `v=DKIM1; t=s; p=MIGfMA0G...` (L07 p.41).

**DMARC** is named on the phishing-detection summary as the umbrella mechanism to "protect against sender spoofing," with the caveat that it may not help if the recipient does not know the valid sender address (L07 pp.44–45). The lecture does not give DMARC its own detailed slide — treat SPF + DKIM as the building blocks and DMARC as the policy layer on top.

### Blocking malicious content and the limits of automation

**Blocking of malicious content (L07 p.42):**
- **Known malicious content:** known malicious domains (e.g., from PhishTank), known malware in attachments.
- **Potentially malicious content:** look-alike domains, dangerous file formats in attachments (e.g., `.exe`), other suspicious indicators such as certain keywords.
- **Alternative — allow-list:** only permit content from an allow-list (e.g., only internal websites) — but this can be too restrictive.
- **Alternative — warn instead of block:** include a warning on a suspicious email rather than blocking it entirely — but this needs manual verification.

**Automatic verification issues (L07 p.43):**
- **False positives** — legitimate emails are blocked.
- **False negatives** — phishing emails reach the user.
- Certain methods need technical know-how (e.g., signing/verifying signatures).
- Threat intelligence can be lacking or outdated (e.g., for malicious-domain lists).
- Manual inspection is sometimes still needed.

### Manual detection indicators (for users)

The lecture's manual-detection checklist, with each indicator's strengths and weaknesses (L07 p.44):
- **Look and feel (e.g., spelling mistakes):** an indicator for poorly made phishing emails — might be enough to repel most attacks — but professional-looking phishing emails can be created.
- **Content (suspicious requests, unusual wording, "Nigerian prince" frauds):** an indicator in some cases (e.g., banks never ask for credit-card data), but hard to detect with personalized emails.
- **Lack of security features (no domain verification / no signature):** an indicator if such features are expected, but false positives are possible and false negatives are not excluded (e.g., if DMARC is set up incorrectly).
- **URL/attachment check:** the **most reliable indicator**, but it requires knowledge on the user's part.

**Detection-methods summary, with the catch for each (L07 p.45):**
- Block phishing websites? — not always reliable to detect or fast enough to act.
- Register all look-alike domains? — requires resources; attackers can invent new tactics.
- Protect against sender spoofing (e.g., DMARC)? — might work, but what if the recipient doesn't know the valid sender address?
- Use digital signatures? — might be too complicated for users to apply.
- Rely on users to detect phishing links? — unavoidable, but challenging.

### User education and simulated phishing campaigns

**Anti-phishing information materials (L07 p.47):** a variety of media (e-learning modules, videos, websites, paper materials); **gamification** for active learning and motivation; anti-phishing games such as **NoPhish** and **Anti-Phishing Phil**; and **embedded learning**. (Reference: `phish-education.apwg.org`.)

**Simulated phishing campaigns — the GoPhish platform (L07 p.48):**
- **Goals:** evaluate how many people click the link / enter credentials; measure how vulnerable the organisation is to phishing; measure how effective the awareness measures are; and teach (e.g., combined with additional awareness materials).
- **Data collected:** the *rate* of clicks or data entries only; the *names* of people clicking or providing data (e.g., entering passwords); and the *specific data* provided on the website.

**Issues with security education (L07 p.49):**
- One-time measures are not enough — habits take time to change, new people join, and threats evolve as attackers get cleverer.
- Putting responsibility solely on the user — are there unreasonable demands? Do users know how to report a phishing link? Are there *consequences* for the user of reporting / of clicking a phishing link?
- Lack of actionable advice — instructions are often unclear ("don't click on suspicious emails") or unrealistic ("don't visit websites you don't know").
- (Reference: `takefive-stopfraud.org.uk`.)

### Lab tools: SET and GoPhish

The lab (E07) uses two open-source phishing-simulation tools, both run from Kali Linux (E07 pp.1, 3–5):
- **SET (Social Engineer Toolkit)** — open-source, designed for security testing and awareness training; lets professionals design, execute, and monitor phishing campaigns safely. Used in Exercise 5 to craft a phishing email (Email Attack feature) and a fake login page (Website Attack feature), then launch and analyze the campaign (E07 pp.1, 3–4).
- **GoPhish** — the framework used in Exercise 6 (and shown in the lecture, L07 p.48): configure SMTP, build a landing page, define a target group, design the email, launch, and track open/click/credential-capture rates via the dashboard (E07 p.5).

---

## Glossary

- **Social engineering** — Any act that influences a person to take an action that may or may not be in their best interest; psychological manipulation to make people disclose information or take actions they otherwise wouldn't (L07 p.7).
- **Phishing** — A deceptive tactic where attackers impersonate a trusted entity (via email or other channels) to trick users into revealing sensitive information (L07 pp.9, 25).
- **Spear-phishing** — A targeted phishing attack aimed at specific individuals (listed among SE methods, L07 p.8; corresponds to the "explicit/personalized" targeting on L07 p.12). *Note: the lecture lists the term but does not give a separate definition slide.*
- **Whaling / CEO fraud** — Phishing that impersonates a senior/trusted authority, instructing the victim to transfer money or share sensitive documents (L07 pp.8, 28).
- **Vishing** — Voice phishing; phishing carried out over a phone call (L07 p.9; E07 p.1).
- **Smishing** — SMS phishing; phishing carried out via text message (L07 pp.8–9; E07 p.1).
- **Credential harvesting / credential stealing** — Collecting victims' login credentials, typically via a fake login page that forwards entered credentials to the attacker (L07 pp.8, 26).
- **Baiting** — Luring victims into compromising security by offering something tempting (L07 p.9).
- **Waterholing (watering hole)** — Compromising a legitimate website frequently visited by a target group so its visitors are attacked (L07 p.9).
- **WiFi spoofing** — Setting up a fake WiFi hotspot with a name mimicking a legitimate network (L07 p.9).
- **Evil USB** — A malicious USB device used as a physical attack vector (listed among SE methods, L07 p.8).
- **Dumpster diving** — Searching trash/discarded documents for sensitive information; even shredded documents can sometimes be reconstructed (L07 p.10).
- **Tailgating (piggybacking)** — Gaining access to a restricted area by following an authorized person, e.g., pretending to have lost an access card (L07 p.10).
- **Shoulder surfing** — Physically observing someone entering sensitive data (passwords, PINs) or overhearing/observing confidential information (L07 p.10).
- **Pretext** — The fabricated story/context an attacker uses to make contact believable; can draw on work, personal, or combined information (L07 pp.13, 18).
- **OSINT (Open-Source Intelligence)** — Gathering information from publicly available sources (search engines, web pages, social media, public records); the lecture references the OSINT Framework (L07 p.14).
- **Pivoting point** — Using an initial compromised target as a stepping stone for further attacks (e.g., a hijacked account used for internal emails) (L07 p.12).
- **Explicit target** — Targeting specific high-value individuals (e.g., a CEO) (L07 p.12).
- **Opportunistic target** — Targeting a large group to increase the chance of success (e.g., mass phishing) (L07 p.12).
- **Hybrid approach** — Combining explicit and opportunistic targeting (e.g., a malicious WiFi network) (L07 p.12).
- **SMTP (Simple Mail Transfer Protocol)** — The email-sending protocol, designed in 1980 with no built-in security, which makes spoofing possible (L07 p.30).
- **Sender spoofing** — Falsifying the sender's display name or address so an email appears to come from a trusted person (L07 pp.31–32).
- **Message spoofing** — Intercepting and altering a message's content in transit (defended by DKIM) (L07 p.40).
- **SPF (Sender Policy Framework)** — A DNS record letting a domain declare which servers may send mail on its behalf; receiving servers check it and softfail/fail unauthorized senders (L07 pp.38–39).
- **DKIM (DomainKeys Identified Mail)** — A digital-signature mechanism: the domain signs outgoing mail with a secret key; recipients verify with the public key in DNS, proving origin and integrity (L07 pp.40–41).
- **DMARC** — The policy layer for protecting against sender spoofing, building on SPF/DKIM (L07 pp.44–45).
- **Softfail / fail** — SPF outcomes: softfail delivers the email but flags it; fail blocks delivery (L07 p.38).
- **PhishTank** — A source of known malicious domains used for content blocking (L07 p.42).
- **False positive / false negative** — A legitimate email wrongly blocked / a phishing email wrongly allowed through (L07 p.43).
- **Homoglyph / look-alike domain** — A domain using visually similar characters (e.g., `arnazon.com`, `fácebook.com`) to impersonate a real one (L07 p.36).
- **Open redirect** — A URL on a legitimate site that forwards to an attacker site (e.g., `amazon.com/login?redirect=https://evilhacker.org`) (L07 p.36).
- **SET (Social Engineer Toolkit)** — Open-source tool for designing, executing, and monitoring phishing campaigns; has Email Attack and Website Attack features (E07 pp.1, 3–4).
- **GoPhish** — Open-source phishing-simulation platform with SMTP config, landing pages, target groups, campaigns, and a tracking dashboard (L07 p.48; E07 p.5).
- **NoPhish / Anti-Phishing Phil** — Gamified anti-phishing training tools/games (L07 p.47).
- **Embedded learning** — Teaching users at the "teachable moment," e.g., immediately after they fall for a simulated phish (L07 p.47).

---

## How-To Cookbook

### A. Spotting phishing indicators in an email (manual detection)

Grounded in L07 pp.25, 33, 44 and the lab's red-flag tasks (E07 pp.1–2).

1. **Check the link before clicking.** Hover over (don't click) every link and read the real destination from the tooltip/status bar. The single most reliable indicator is whether the link actually leads to the real organization's domain (L07 pp.25, 44). Watch for the URL tricks below.
2. **Identify the real domain in the URL.** Read the domain right-to-left to find the true registrable domain. Be alert to: the legit name buried as a subdomain or path (`amazon.com.evilhacker.com`, `evilhacker.com/www.facebook.com`), similar domains (`amazon-shop.com`), homoglyphs (`arnazon.com`, `fácebook.com`), URL shorteners (expand them with a checker), and open redirects (`...?redirect=https://evilhacker.org`) (L07 pp.34–36).
3. **Check the sender.** Remember the display name and even the address can be spoofed (L07 pp.31–32). Look for addresses that are *similar but wrong* (e.g., `yourbank-service@mail.com`).
4. **Look for urgency, fear, and scarcity cues.** "Act immediately," "account compromised," "before 16:00 today to avoid salary delays" are classic pressure tactics (L07 pp.20, 25; E07 p.2).
5. **Scan for look-and-feel problems** — spelling mistakes, odd timing (e.g., Saturday evening), unusual wording (L07 pp.25, 44).
6. **Sanity-check the request itself.** Legitimate banks never ask for credit-card data; legitimate IT never asks you to disclose your password (L07 p.44).
7. **Check for missing security features** when they'd be expected (no domain verification/signature) — but treat this cautiously (false positives/negatives possible) (L07 p.44).
8. **When in doubt, verify out-of-band.** Don't use the link; go directly to the official portal, and confirm via a known phone number/channel (E07 pp.1–2, see scenario answers below).

### B. Responding to a suspicious phone call (vishing) — the "John from IT" scenario

From the lab's Exercise 1 (E07 pp.1–2). Recommended handling:

1. **Do not trust the call on its face.** An unsolicited, urgent caller pressuring you to reset a password is a classic vishing pretext (authority + urgency) (E07 p.1; L07 p.20).
2. **Never act on the link in the email.** Go directly to the company's official portal by typing the known address yourself, not via any link the caller sent (E07 p.1).
3. **Verify legitimacy independently.** Hang up and call IT back on the official internal number; confirm the "company-wide security upgrade" through an official channel; check with your manager/colleagues (E07 p.1).
4. **If unsure,** do not provide any credentials or perform the requested action until verified; legitimate IT does not need your password (E07 p.2; L07 p.44).
5. **If you suspect social engineering,** report the incident to IT/security per company policy so others can be warned (E07 p.2; L07 p.49 stresses users must know *how* to report).

### C. Spotting a smishing message — the SDU payroll SMS

From the lab's Exercise 2 (E07 p.2). The message: "SDU HR: We detected an issue with your payroll details after the system upgrade. Please confirm your information before 16:00 today to avoid salary delays. Verify here: http://hr-payroll-secure.sdu/verify".

1. **Note why it's believable:** it references a real, recent event (HR migrated to a new payroll platform) and impersonates a trusted department — personalization/plausibility (E07 p.2; L07 pp.18, 20).
2. **Find the red flags:** artificial deadline ("before 16:00 today"), fear of financial loss ("avoid salary delays"), and a suspicious link/domain (`hr-payroll-secure.sdu` is not the real SDU domain) (E07 p.2; L07 pp.25, 35).
3. **Do not click.** Instead, access the payroll system through the official, known portal or contact HR directly via a verified channel (E07 p.2).
4. **Organizational mitigations:** train staff, deploy phishing-resistant verification, use official communication channels only, and run awareness campaigns / simulated phishing (E07 p.2; L07 pp.47–48).

### D. Running a phishing simulation with SET (Social Engineer Toolkit)

From the lab's Exercise 5 (E07 pp.3–4). This is for a **controlled, authorized lab only** — the lab note says to use dummy emails/fake profiles (E07 p.5).

1. **Launch SET.** Open a terminal in your Kali machine and launch the Social Engineer Toolkit (E07 p.3).
2. **Choose a target group** (e.g., another student group acting as "Defenders") (E07 p.4).
3. **Craft the phishing email** using SET's **Email Attack** feature. The email should contain: (a) a malicious link redirecting to a fake login page / page requesting sensitive info (username, password, credit card); (b) a sense of urgency or fear (e.g., "Your account has been compromised! Please reset your password immediately!"); and (c) personalization (target's name, company name, or a specific reference) to make it look authentic (E07 p.4).
4. **Create a fake website** using SET's **Website Attack** feature — a fake login page for a well-known site (Gmail, Facebook, an internal portal). Make it look as legitimate as possible (matching colors, logos, fonts, layout) (E07 p.4).
5. **Launch the campaign.** Send the phishing email to the target group and direct them to the fake login page; track whether targets click the link and enter sensitive information (E07 p.4).
6. **Report and analyze.** Determine whether the target provided any information (e.g., login credentials) (E07 p.4).
7. **Defense analysis** (Exercise 5, Task 6 — reused for GoPhish): identify what characteristics of SET-generated emails/cloned sites help users spot them; how security tools detect/block credential-harvesting pages created with SET; and what configurations (email security, domain monitoring) prevent SET-based campaigns from reaching users (E07 p.4).

### E. Running a phishing simulation with GoPhish

From the lab's Exercise 6 (E07 p.5) and the lecture's GoPhish overview (L07 p.48). Controlled lab use only.

1. **Launch GoPhish** from your Kali machine (E07 p.5).
2. **Configure SMTP settings** for sending the phishing emails (E07 p.5).
3. **Create a landing page** (e.g., a fake login page) (E07 p.5).
4. **Create the target group** — keep the same groups as in Exercise 5 (E07 p.5).
5. **Design the email** — write a phishing email with a malicious link (e.g., subject "Urgent: Account Verification") and include the fake login-page link (E07 p.5).
6. **Create the fake landing page** — mimic a legitimate website with a login form to capture credentials (E07 p.5).
7. **Launch the campaign** — send the phishing emails to the target group (E07 p.5).
8. **Track interactions** — monitor email open rates, click rates, and credential captures via GoPhish's dashboard (E07 p.5; L07 p.48).
9. **Review campaign data** — examine open rates, clicks, and credential submissions (E07 p.5).
10. **Defense** — reuse the SET defense questions adapted for GoPhish (E07 p.5).

### F. Hardening a domain against email spoofing (defender)

Grounded in L07 pp.38–42.

1. **Publish an SPF record** in DNS listing exactly which servers/IP ranges may send mail for your domain (e.g., `v=spf1 a -all`). Unauthorized senders then softfail or fail at the recipient (L07 pp.38–39). Free SPF generators exist.
2. **Set up DKIM signing.** Sign outgoing mail with your domain's secret key and publish the matching public key in DNS (e.g., `v=DKIM1; ...`). This proves the message came from your domain and was not tampered with in transit (L07 pp.40–41).
3. **Layer DMARC on top** to define a policy and protect against sender spoofing — noting it may not help recipients who don't know the valid sender address (L07 pp.44–45).
4. **Block known/potentially malicious content** — known malicious domains (e.g., PhishTank), known malware, dangerous attachment formats (`.exe`), look-alike domains, and suspicious keywords; consider allow-listing or warning banners as alternatives (L07 p.42).
5. **Accept the limits** — tune for false positives/negatives and keep threat intelligence fresh; manual inspection is sometimes still needed (L07 p.43).

---

## Exam-Style Q&A

**Q1. Define social engineering and give two reasons it is dangerous in cybersecurity.**
A. Social engineering is "any act that influences a person to take an action that may or may not be in their best interest" — a psychological manipulation technique used to persuade individuals into making decisions or disclosing information they might not otherwise share (L07 p.7). It is dangerous because (1) it bypasses technical controls by targeting the human, who has legitimate access, and (2) it underpins common threats like phishing, pretexting, and impersonation, and even works in non-cyber "traditional" scams (L07 p.7). It is also hard to defend against because security decisions are non-automatic, emotionally driven, and seen as obstacles (L07 p.21).

**Q2. Distinguish digital from physical social-engineering methods, with examples of each.**
A. **Digital methods (L07 p.9):** phishing (incl. vishing/voice and smishing/SMS), baiting (offering something tempting), waterholing (compromising a site the target frequents), and WiFi spoofing (fake hotspots mimicking real networks). **Physical methods (L07 p.10):** dumpster diving (mining discarded documents), tailgating/piggybacking (following an authorized person into a restricted area), and shoulder surfing (observing someone enter passwords/PINs or overhearing confidential talk). Other listed methods include spear-phishing, credential harvesting, whaling/CEO fraud, evil USB, malicious attachments, and on-site visits (L07 p.8).

**Q3. Describe the social-engineering attack lifecycle as covered in the lecture.**
A. The lecture frames it as a lifecycle (L07 p.11). **Choosing a target (L07 p.12):** identify who has the desired access (often via information gathering); the target can be a pivoting point for deeper attacks; targeting is explicit (specific people, e.g., a CEO), opportunistic (a large group, e.g., mass phishing), or hybrid (both, e.g., a malicious WiFi network). **Contacting the target (L07 p.13):** the contact method depends on the goal (extract info, deploy malware, gain access); contact can be one-off or long-term, manual or automated, and is made more effective via personalization (from recon) and pretexts/persuasion tactics. The learning objectives describe this as running "from reconnaissance to execution" (L07 p.6).

**Q4. What is the difference between explicit, opportunistic, and hybrid targeting? Give an example of each.**
A. **Explicit** — the attacker focuses on specific individuals with valuable access (e.g., a CEO). **Opportunistic** — the attacker targets a large group to raise the odds of success (e.g., mass phishing emails). **Hybrid** — combines both (e.g., setting up a malicious WiFi network that both lures many people and may capture a high-value one) (L07 p.12).

**Q5. List and explain four persuasion / psychological techniques attackers use.**
A. From L07 pp.19–20: **Authority** — pretending to be someone important so the victim complies. **Fear and urgency** — creating panic so the victim acts quickly without thinking. **Scarcity and urgency** — limited-time offers or "few spots left" to force a fast decision. **Trust and familiarity** — pretending to be someone the victim knows/trusts. Others named: liking/social proof (doing favors for people one likes or one's in-group), trustworthiness based on appearance, offering rewards, plausibility, curiosity, reciprocity, and convenience. (These align with Cialdini's principles, but the lecture presents them as its own lists, not under Cialdini's name.)

**Q6. Walk through the five steps of a credential-stealing phishing attack.**
A. (L07 p.26) 1) The user gets an email with a link to what looks like a trusted organization's website. 2) The link goes to a site that looks like the real one but is owned by the attacker. 3) The user is prompted to enter credentials. 4) The credentials are forwarded to the attacker. 5) The attacker gains full control of the user's account.

**Q7. Why is email spoofing possible, and what are the two forms of sender spoofing?**
A. Email runs on SMTP, designed in 1980 with no built-in security (L07 p.30). **Sender's name spoofing (L07 p.31):** the display name is falsifiable, so an attacker on a public server can set `From: Alice <eve@mail.com>`; the address can be made to look similar enough to be believable (e.g., `alice@mail.com` or `alice@eve.com`). **Sender's address spoofing (L07 p.32):** the actual address is falsifiable if the attacker controls the sending server or if the provider's server is misconfigured — sending `From: Alice <alice@alice.com>` from eve.com.

**Q8. Explain how SPF and DKIM defend against spoofing, and what each one actually protects.**
A. **SPF (Sender Policy Framework)** defends against *sender* spoofing: the receiving server asks the claimed sender's domain whether the sending server is authorized to send on its behalf; if not, the email softfails (delivered but flagged) or fails (not delivered) (L07 pp.38–39). It's a DNS record like `v=spf1 a -all`. **DKIM (DomainKeys Identified Mail)** defends against *message* spoofing: the sending domain signs the message with its secret key, and the recipient verifies with the domain's public key (in DNS), proving both that the email came from that domain and that it was not tampered with in transit (L07 pp.40–41). In short: SPF = "is this server allowed to send for the domain?"; DKIM = "was this message really signed by the domain and unaltered?". DMARC sits on top as the policy layer (L07 pp.44–45).

**Q9. Give five URL-disguising tricks attackers use and why each is hard to spot.**
A. (L07 pp.34–36) **URL shorteners** (`tinyurl.com/...`) hide the real destination until clicked. **Legitimate site as part of URL** (`amazon.com.evilhacker.com`) fools users who can't identify the true domain, especially on mobile where the URL is truncated. **Similar domains** (`amazon-shop.com`) fool users who don't know the real site. **Indistinguishable/homoglyph domains** (`arnazon.com`, `fácebook.com`) use look-alike characters and are especially hard to notice. **Compromised legitimate sites / open redirects** (`amazon.com/login?redirect=https://evilhacker.org`) are impossible to spot from the URL alone — the site owner must fix it.

**Q10. Which manual indicator does the lecture call the most reliable, and what are its limitations?**
A. The **URL/attachment check** is the most reliable manual indicator, but it requires technical knowledge on the user's part (L07 p.44). Other indicators (spelling/look-and-feel, suspicious content, missing security features) are weaker: professional phishing emails avoid spelling errors, personalized emails hide suspicious content, and security-feature checks can produce false positives/negatives (L07 p.44).

**Q11. What can a simulated phishing campaign (e.g., GoPhish) measure, and what data can it collect? What are the privacy considerations?**
A. Goals (L07 p.48): how many people click the link / enter credentials, how vulnerable the organization is, and how effective awareness measures are — and it can teach when combined with awareness materials. Data collected ranges from just the *rate* of clicks/entries, to the *names* of people who clicked or entered data, to the *specific data* they entered. Collecting names and specific data raises privacy/ethics questions — echoed in the SE pen-test ethics on whether individuals should be named in reports and whether findings should be shared with employers (L07 p.22). Education must also consider whether there are *consequences* for users who click or report (L07 p.49).

**Q12. In the "urgent IT password reset" call (lab Exercise 1), should the employee trust the call, and how should they verify it?**
A. No — an unsolicited, urgent caller pressuring an immediate password reset is a classic vishing pretext combining authority and urgency (E07 p.1; L07 p.20). The employee should not click any link and should go directly to the company's official portal by typing the known address (E07 p.1). To verify: hang up and call IT back on the official internal number, confirm the claimed "company-wide upgrade" through an official channel, and consult a manager/colleagues. If still unsure, provide nothing — legitimate IT never needs your password — and report the incident to security per policy (E07 pp.1–2; L07 pp.44, 49).

**Q13. What are the security risks of accessing sensitive company documents over public/free hotel WiFi, and how can a traveler reduce them?**
A. From lab Exercise 3 (E07 pp.2–3): risks include connecting to an *unsecured or fake hotspot* (WiFi spoofing, L07 p.9) where an attacker can intercept traffic or perform a man-in-the-middle attack, capturing credentials and document contents. Before connecting, the user should confirm the network is legitimate and ensure communications are encrypted; the safest mitigation is a company VPN and only using HTTPS/secured portals. Company-side measures include providing a VPN, enforcing MFA, and policies for accessing systems while traveling (E07 pp.2–3). (The lecture grounds the WiFi-spoofing risk on L07 p.9; the specific traveler mitigations are the lab's discussion questions rather than spelled-out slide answers.)

**Q14. In the "important deadline" email (lab Exercise 4), what social-engineering techniques are at play and how should Bob respond?**
A. (E07 p.3) The request impersonates a known colleague (Alice) and uses urgency/deadline pressure and emotional appeal (her anxiety about missing a deadline) — i.e., trust/familiarity plus fear and urgency (L07 p.20). Bob should not simply send the sensitive document; he should verify out-of-band that the request truly came from Alice (e.g., call her on a known number), be aware the sender could be spoofed (L07 pp.31–32), recognize the risk of emailing sensitive documents, and follow company policy/procedure before sharing (E07 p.3).

**Q15. Why do users find phishing hard to detect, and why are one-time training measures insufficient?**
A. There is a gap between what the user *wants* to do (quickly process email and continue working) and what they *need* to do (carefully verify each message) (L07 p.46). Security decisions are context-dependent, emotionally triggered, non-automatic, and seen as obstacles/annoyances (L07 p.21). One-time training is insufficient because habits take time to change, new people keep joining, and threats evolve as attackers get cleverer; education must also give *actionable* advice (not vague "don't click suspicious emails"), ensure users know how to report, and avoid punishing reporters (L07 p.49).

**Q16. A security guard is asked by a visibly unwell, pregnant stranger to be let into a secured building to use a phone and bathroom. What is the dilemma and a reasonable resolution?**
A. (L07 p.23) The dilemma: ignoring the request risks a real medical emergency, but letting her in risks a tailgating-style physical intrusion where she could plant eavesdropping devices or malware-laden removable media. The lecture's suggested resolution is a **compensating control**: have a second guard remain at the entrance while the first helps her, ensuring she does nothing suspicious — balancing compassion with physical security.

---

## Gotchas

- **SPF vs. DKIM — don't mix them up.** SPF answers "is this *server* allowed to send for the domain?" and protects against *sender* spoofing; DKIM is a *digital signature* that protects against *message* spoofing (tampering) and proves origin. SPF = authorized sender; DKIM = signature/integrity (L07 pp.38–41). A common exam trap is attributing tamper-protection to SPF — that's DKIM's job.
- **SPF outcomes: softfail vs. fail.** Softfail still *delivers* the email but marks it as failing verification; fail blocks delivery entirely (L07 p.38). Don't say SPF always blocks.
- **"The link looks like the real site" is not enough.** The legit name can appear as a subdomain, a path, or a redirect target (`amazon.com.evilhacker.com`, `amazon.com/evilhacker`, `...?redirect=https://evilhacker.org`). Always identify the *true registrable domain*, reading the URL correctly (L07 pp.35–36).
- **The sender address can be fully spoofed.** A "From: alice@alice.com" address can be forged if the attacker controls the server or the provider is misconfigured — so "the address looks right" is not proof of authenticity (L07 p.32).
- **Spelling mistakes are a weak signal.** They catch poorly made phishing, but professional and AI-generated phishing emails have no spelling errors and can be highly personalized (L07 pp.29, 44). The **URL/attachment check** is the most reliable manual indicator (L07 p.44).
- **Malware can trigger without opening the attachment.** In rare cases just clicking a link or even reading the email can execute malware, especially on unpatched systems (L07 p.27). Don't assume "I didn't open it" means safe.
- **Vishing and smishing are still phishing.** They are phishing over voice (vishing) and SMS (smishing), not separate unrelated categories — and the lab tests all three (L07 p.9; E07 p.1).
- **Automated defenses produce both false positives and false negatives.** Blocking legitimate mail (false positive) and letting phishing through (false negative) both happen; misconfigured DMARC can cause false negatives. Automation does not remove the need for manual inspection or user vigilance (L07 pp.43–45).
- **DMARC only helps if the recipient knows the valid sender.** Anti-spoofing controls don't help when the recipient has no idea what the legitimate sender address should be (L07 p.45).
- **Simulated phishing has ethics/privacy strings.** Campaigns can collect names and the specific data users entered; the SE pen-test ethics ask whether individuals should be named in reports and whether findings should be shared with employers — and whether users face consequences for clicking or reporting (L07 pp.22, 48–49). In the lab, use dummy emails/fake profiles and only target your assigned, consenting group (E07 pp.4–5).
- **Don't over-claim Cialdini.** The lecture lists authority, social proof, liking, scarcity, reciprocity, and trust as persuasion levers but never names Cialdini or fixes a "six principles" list. If the exam wants the academic source, flag that the slides present these as their own lists (L07 pp.19–20).
- **Allow-listing and warning banners are trade-offs, not free wins.** Allow-listing only internal/known content can be too restrictive; warning banners shift the burden to manual user verification (L07 p.42).
- **The lifecycle in the slides is not a tidy numbered list.** Slide 11 shows a diagram (image); the explicitly described stages are "Choosing a target" and "Contacting the target" with information gathering throughout (L07 pp.11–14). If asked for a canonical multi-step lifecycle, note that the slides emphasize these stages and "reconnaissance to execution" (L07 p.6) rather than a fixed four-phase model.
