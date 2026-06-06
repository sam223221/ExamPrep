# 11. Privacy, Data Protection & the GDPR

> Source: Guest lecture by Jukka Ruohonen, "Cybersecurity (T510039402)", 22 April 2026 (L11). The lecture is 80 slides. Citations below use `(L11 p.N)` where N is the slide number printed in the PDF (`N / 80`). This was a guest lecture with **no accompanying exercise PDF**. Everything here is grounded in that lecture only; where the lecture does not cover something, that is stated explicitly.

---

## Overview — what this topic covers and why it matters

This chapter is about **privacy and data protection**, with the EU's **General Data Protection Regulation (GDPR)** as the central legal instrument (L11 p.2). The lecture frames privacy first as a *philosophical and legal* concept — a fundamental human right made up of several distinct properties — and then narrows toward the parts that matter most to computer scientists and software engineers: confidentiality, anonymization, and the concrete obligations the GDPR places on the people who build and run systems that process personal data (L11 p.4–5). A recurring message is that **security and data protection are both necessary for privacy, but neither alone is sufficient**, and that **confidentiality is a component of privacy, not the same thing** (L11 p.5).

Why it matters for the exam and for practice: the GDPR is **directly applicable EU law** (a regulation, not a directive), it is **extraterritorial**, and it is **risk-based** (L11 p.11, p.16, p.23). It increased data subjects' rights, increased controllers' and processors' duties, increased data protection authorities' powers, and improved European harmonization (L11 p.15). For an engineer, the regulation translates into functional requirements (consent control, access, rectification, erasure, restriction, logging), non-functional requirements (security, data minimization), and organizational obligations (DPIAs, a Data Protection Officer, 72-hour breach notification, record-keeping) (L11 p.63–76). The second half of the lecture covers the **technical privacy toolkit** — pseudonymization, anonymization, k-anonymity, ℓ-diversity, randomization — and stresses that anonymization is genuinely hard and often done badly (L11 p.42–60).

---

## Key Concepts

### What privacy is (the six properties)

**What/why:** The lecture defines privacy not with a single sentence but via **six properties (P1–P6)** that recur in the legal literature (from Solove 2002) (L11 p.4):

- **P1:** The right to be left alone
- **P2:** The ability to shield oneself from unwanted access
- **P3:** The concealment of certain matters from others
- **P4:** Control over personal information
- **P5:** The protection of personality, individuality, and dignity
- **P6:** Control over intimate relationships and aspects of life

**How it maps:** Each property looks simple but is "extremely difficult philosophically, legally, and politically" (L11 p.4). Roughly, the *whole set* P = {P1 … P6} is what makes privacy a **fundamental human right** (L11 p.4). Privacy is a **subjective right given by objective law** — a philosophical and legal concept (L11 p.5). Different fields emphasize different properties (L11 p.5):

- **Human rights** perspective → P1, P5, P6
- **Computer science** → typically P2 and P3 (confidentiality, encryption, anonymization). Note: **confidentiality ≠ privacy, but it is a component of privacy** (L11 p.5).
- **Data protection** → P4, P5, P6 in particular. **Both security and data protection are necessary for privacy** (L11 p.5).

### Privacy vs. confidentiality vs. data protection

**What/why:** These three are related but distinct, and the exam may test the distinctions (L11 p.6–7):

- **Privacy vs. confidentiality** (Figure 1, "superset and subset"): privacy concerns **humans / personal data**; confidentiality concerns **humans and everything else**. They overlap but confidentiality is broader in what it protects (it is not limited to people) (L11 p.6).
- **Privacy vs. data protection** (Figure 2, "overlapping but not the same"): **data protection requirements (e.g., accuracy and security of personal data processing) apply even when there is no privacy violation or interference** (L11 p.7). So you can be in breach of data protection law without anyone's privacy being "invaded."

### Fundamental-rights basis

**What/why:** Privacy has a strong legal pedigree (L11 p.8):

- **Universal Declaration of Human Rights (UN 1948), Article 12:** "No one shall be subjected to arbitrary interference with his privacy, family, home or correspondence…" (L11 p.8).
- Many national constitutions include privacy (L11 p.8).
- In the **EU**, both a right to "private life" and **data protection** are fundamental rights — **Articles 7 and 8 of the EU Charter (EU 2012)** (L11 p.8).
- Legal scholars argue that defining **data protection as a fundamental right was perhaps more important than enacting the GDPR itself** (L11 p.8).

Further dimensions exist (spatial and physiological privacy, genetics ⊆ P6); workplace/employment privacy is covered by **separate laws**, and some issues fall under **criminal law** (L11 p.9).

### The "seven privacy sins" and the GDPR's purpose

**What/why:** Shastri et al. (2019) list seven commonplace **"privacy sins" in software engineering** (L11 p.11):

1. Storing data forever
2. Reusing data indiscriminately
3. Walled gardens and black markets
4. Risk-agnostic data processing
5. Hidden data breaches
6. Unexplainable decisions
7. Security as a secondary goal

**The GDPR addresses all of these sins, and is a risk-based regulation** (L11 p.11). Its goals are **twofold**: (1) protect natural persons, and (2) **facilitate the free flow of personal data across the union** — so it can be seen as an *enabler for a fair European data economy*, not only a restriction (L11 p.14).

### What the GDPR changed (big picture) + national adaptation

**What/why:** Four big shifts (L11 p.15):

1. Data subjects' rights increased
2. Data controllers' (and processors') duties increased
3. Data protection authorities' powers increased
4. European harmonization improved

**Regulation vs. directive:** the GDPR is a **regulation** → **directly applicable EU law** in member states' jurisdictions (unlike a directive), which underlines harmonization (L11 p.16). But member states retain **leeway**, so most made/updated a national data protection law. Flexibility is allowed especially around: **legal obligations and public interests (Art. 6), sensitive personal data (Art. 9), criminal matters (Art. 10)**, and scope restrictions for **national security, defense, judicial independence, etc. (Art. 23)** (L11 p.16).

**Politics:** the GDPR was "allegedly the EU's most lobbied law" in the late 2010s; heavy lobbying (private sector, civil society, third countries) **decreased its overall legitimacy** (Hildén 2019). Enforcement problems and SME compliance issues have been on the political agenda. At lecture time, parts are being renegotiated via the **"digital omnibus"**, so some legal details may change (though probably not the fundamentals) (L11 p.13, p.14).

### Governance: DPAs and the EDPB

**What/why:** Data-protection governance follows the same model as cybersecurity governance (L11 p.17):

- Each country has a **public-sector Data Protection Authority (DPA)** (in **Germany there are many DPAs**) (L11 p.17).
- EU-level coordination is via the **European Data Protection Board (EDPB)** (L11 p.17).
- **Governance has itself been an obstacle to GDPR enforcement** (Ruohonen & Hjerppe 2022) (L11 p.17).
- There are **alternative data-protection EU laws** for law enforcement and for EU institutions (L11 p.17).
- The Danish DPA example given is **Datatilsynet** (datatilsynet.dk) (L11 p.18).

### Personal data and processing (Article 4)

**What/why:** Definitions are deliberately broad (L11 p.19):

- **Personal data (Art. 4(1)):** "*any information relating to an identified or identifiable natural person.*" This scope is **much wider than the US notion of "personally identifiable information" (PII)** (L11 p.19).
- **Processing (Art. 4(2)):** "*any operation or set of operations … performed on personal data … whether or not by automated means*" — collection, recording, organisation, structuring, storage, adaptation/alteration, retrieval, consultation, use, disclosure by transmission, dissemination, alignment/combination, restriction, erasure, destruction (L11 p.19). **Manual processing is in scope too** (L11 p.19).

### Sensitive (special-category) personal data (Article 9)

**What/why:** Some data is "special category" and its processing is **prohibited by default** (Art. 9(1)) (L11 p.20). The categories: data revealing **racial or ethnic origin, political opinions, religious or philosophical beliefs, trade union membership**, plus **genetic data, biometric data** (for uniquely identifying a person), **health data**, and data concerning a person's **sex life or sexual orientation** (L11 p.20).

**Exemptions (Art. 9(2)):** apart from legal obligations of public-sector bodies, **another/separate consent may be required** to process sensitive data; it may also be lawful to process such data if the **person has made it public** (e.g., on social media) (L11 p.20).

### Controllers and processors

**What/why:** (Articles 4(7), 4(8), 24, 26, 28, 29) (L11 p.22):

- **Data controller:** responsible for the **lawfulness and purpose** — the **"why" and "how"** of processing (L11 p.22).
- **Data processor:** processes personal data **on behalf of** the controller — usually under **a contract or legally binding arrangement** (L11 p.22).
- **Joint controllers** also exist (L11 p.22).
- Tied to **supply chains**: if you hold personal data, **you are a controller** and may outsource processing to third-party processors (L11 p.22).

### Extraterritoriality and international transfers

**What/why:** (L11 p.23–24):

- The GDPR is an **extraterritorial law**: it applies to organizations controlling or processing personal data **inside or outside the EU** (L11 p.23).
- Per **Article 3**, **merely offering goods or services to Europeans (European natural persons) suffices** to be caught by the GDPR (L11 p.23). This has caused major international schisms and court cases (L11 p.23).
- **International transfers:** transferring personal data to a non-EU country is generally lawful **only if EU-level authorities have determined that country has an adequate level of data protection** (an "adequacy" decision) (L11 p.24).

### Informational self-determination

**What/why:** The GDPR is **primarily a data-protection regulation**; data protection (DP) is **necessary but not sufficient** for privacy (L11 p.25). Properties **P4, P5, P6** are emphasized → the concept of **informational self-determination**: everyone has a **fundamental (but not absolute) right to determine how their data is collected and used** (L11 p.25). This concept **provides the foundation for consent** in the DP context, and became famous via the **1983 decision of the German Constitutional Court** (L11 p.25).

### Lawful bases for processing (Article 6)

**What/why:** Consent is **only one** of six legal bases, and **you must always pick exactly one** legal basis (L11 p.26). The six (Art. 6) (L11 p.26):

1. **Consent** — note it **must be informed**
2. **Contract** — e.g., employment
3. **Legal obligations** — e.g., law enforcement
4. **Vital interests** — e.g., healthcare emergencies
5. **Public interests** — e.g., education
6. **Legitimate interests** — e.g., marketing

The **last (legitimate interests) is controversial**: using it generally requires a **balancing test** weighing natural persons' interests against the claimed "legitimate interests" (L11 p.26).

### The seven principles of processing (Article 5)

**What/why:** Recital 4 frames the spirit: processing should "serve mankind," and data protection is **not absolute** — it must be balanced against other fundamental rights under **proportionality** (L11 p.27). **Article 5 lists seven principles** (L11 p.28):

1. **Lawful, fair, and transparent** processing
2. Only for **specific purposes** and not for other purposes (*purpose limitation*)
3. **Data minimization** — only what is necessary
4. **Accuracy** — only accurate personal data should be processed
5. **Identifiability only for a limited amount of time** (*storage limitation*)
6. **Security of processing** must be guaranteed (*integrity & confidentiality*)
7. **Accountability** — controllers and processors are **legally liable**

These are high-level, but **their violations are frequently used by regulators to justify enforcement fines** (L11 p.28).

### What gets cited in enforcement fines

**What/why:** Empirically (Ruohonen & Hjerppe 2022, across 294 decisions with 525 article references), the **most-referenced articles** in fines are, in order, around (L11 p.29):

- **A5** (principles) and **A6** (lawfulness) — the most frequent
- **A32** (security of processing / information security)
- **A13, A15** (information rights/access), **A58** (DPA powers), **A12, A14**, etc.

Takeaway: **breaches of the high-level principles (A5) and lawfulness (A6) dominate enforcement**, followed by security (A32) (L11 p.29). The Facebook–Cambridge Analytica scandal is given as a case to analyze (L11 p.30).

### Security perspective and Article 32

**What/why:** Security risks and privacy risks overlap but differ (L11 p.31): security risks → disruption to an organization's functioning, unavailability, integrity violations; privacy risks → data leaking to unauthorized parties and an **individual's rights and liberties being violated**. There can be a **seemingly artificial conflict** between security and privacy (e.g., **technical monitoring / log files / accounting** require keeping data, but **data minimization** wants to keep less) — you must **balance** them (L11 p.32).

**Article 32(1)** requires "*appropriate technical and organisational measures to ensure a level of security appropriate to the risk*," taking into account **state of the art, cost of implementation, and the nature/scope/context/purposes of processing, plus the risk** to rights and freedoms (L11 p.33). It then mentions **pseudonymization, encryption, the CIA triad, resilience, and testing** — but **gives no technical details**; it is up to engineers to choose appropriate solutions (L11 p.33).

### Privacy engineering and Privacy-by-Design

**What/why:** **Privacy engineering** is "a field of research and practice that designs, implements, adapts, and evaluates theories, methods, techniques, and tools to systematically capture and address privacy issues when developing sociotechnical systems" (Gürses & del Alamo 2016) (L11 p.35). Spiekermann & Cranor (2009) urge moving from **"privacy-by-policy"** to **"privacy-by-architecture"** — design the architecture itself with privacy in mind (L11 p.35).

**Privacy-by-Design (PbD)** — introduced by **Ann Cavoukian (1995)**, with seven foundational principles (Cavoukian 2009) (L11 p.36):

- **P1:** Proactive not reactive; preventative not remedial
- **P2:** Privacy as the **default setting**
- **P3:** Privacy **embedded into design**
- **P4:** **Full functionality** — positive-sum, not zero-sum
- **P5:** **End-to-end security** — full lifecycle protection
- **P6:** **Visibility and transparency** — keep it open
- **P7:** **Respect for user privacy** — keep it user-centric

PbD is closely related to the GDPR and to **privacy enhancing technologies (PETs)** (L11 p.36).

### Privacy frameworks (NIST and LINDDUN)

**What/why:** **NIST (2021) privacy control framework** — eight high-level controls that align closely with GDPR obligations (L11 p.37–39):

1. **Authority and purpose** — collect only with granted authority (= legal basis) and only for a specific purpose (= purpose limitation) (L11 p.37)
2. **Accountability, auditing, and risk management** — you are accountable; do audits and risk management (≈ **DPIA**, Art. 35); ENISA (2017) suggests risk matrices (impact × probability) (L11 p.38)
3. **Data quality and integrity** — data should be correct and immutable to unauthorized parties (L11 p.38)
4. **Data minimization and data retention** — collect only what you need; don't store indefinitely (L11 p.38)
5. **Participation and redress** — access to one's data, right to correct, right to lodge complaints (L11 p.39)
6. **Security** (L11 p.39)
7. **Transparency** — at minimum, accessible privacy policies (L11 p.39)
8. **Use limitation** — third-party sharing only under specific conditions (L11 p.39)

**LINDDUN** (Wuyts 2015) — a popular privacy threat-modeling framework based on **six properties** (each asset relating to natural persons is assessed against them) (L11 p.40):

1. **Linkability** — whether two objects are related
2. **Identifiability** — possibility to identify an object
3. **Non-repudiation** — evidence a party cannot deny
4. **Detectability** — whether an object exists
5. **Disclosure** — exposure of information to unauthorized subjects
6. **Unawareness** — user is unaware of data submitted

(Used much like threat modeling — e.g., linkability based on biometrics, session ID, IP/MAC address, behavioral patterns) (L11 p.41).

### De-identification: anonymization vs. pseudonymization

**What/why:** Key definitions (L11 p.42):

- **Identification** := ability to identify a data subject
- **De-identification** := a method that prevents re-identification
- **Anonymization** := **optimally irreversible** de-identification
- **Pseudonymization** := a de-identification method that **removes or replaces direct identifiers**; per Art. 4, the data "can no longer be attributed to a specific data subject without the use of additional information" (L11 p.42)

**Critical exam point: pseudonymization ≠ anonymization** (L11 p.43). Evaluate de-identification against **three elements** (L11 p.43):

1. **Singling out** — can you still isolate records relating to one individual?
2. **Linkability** — can you still link ≥2 records relating to an individual across databases?
3. **Inference** — can you infer (with significant probability) an attribute value from other attributes?

**Pseudonymization generally addresses only linkability**; **inference is not guaranteed**, so its focus is more on **security** (L11 p.43).

**GDPR consequences (L11 p.44):**

- The GDPR **emphasizes pseudonymization** in several articles.
- **The GDPR does NOT apply to strictly anonymized data** (L11 p.44).
- **Article 11:** if a controller no longer needs to identify a data subject, it is **not obliged to acquire/keep additional identifying information just to comply** with the regulation (L11 p.44).
- **But the accountability criterion still applies to pseudonymization** — you must be able to **demonstrate** it (L11 p.44).

**Levels of de-identification (Hintze 2017, Table 1)** range from *directly linked / identified* → *identifiable* → *Article 11 (pseudonymized, identified flag)* → *anonymous*; only the fully anonymous level escapes "personal data" (L11 p.45).

### Pseudonymization techniques

**What/why:** Pseudonymization relates to **reversible privacy** — you can securely switch between privacy-preserving and original representations (L11 p.46). **Four common techniques** (L11 p.46):

- **(a) Encryption, (b) hashing, (c) masking, (d) tokenization**
- In practice **all four may be required**; all typically rely on a **secret**. Example: credit-card transactions use **encryption + tokenization** (the card security code) (L11 p.46).

**Masking** is the generic, old-fashioned method: at minimum **all direct identifiers should be masked** — names, addresses, social security numbers, license plates, IP addresses, device fingerprints, etc. (L11 p.47). **Anonymization may be applied to quasi-identifiers** — gender, date of birth, postal code, income, etc. (Example: "John Doe" → "**** Doe") (L11 p.47).

### Anonymity (formal view)

**What/why:** Classic definition (Pfitzmann & Köhntopp 2001) (L11 p.48): "**Anonymity is the state of being not identifiable within a set of subjects, the anonymity set.**" Corollary: anonymity is **stronger the larger the anonymity set is, and the more evenly distributed the subjects within it are** (L11 p.48).

Key nuances (L11 p.49):

- A larger anonymity set |A| → more anonymity for any object in A.
- But **size alone does not guarantee anonymity** — the **probability distribution matters** (anonymity is also a **probability concept**) (L11 p.49).
- Classic measures include **Shannon information entropy**; can be applied to networks/graphs too (L11 p.49).

### Anonymization methods

**What/why:** Anonymization aims for **irreversible** de-identification and should defend against **singling out, linkability, and inference** (L11 p.50). Many classic methods build on pseudonymization ideas and **often ignore probability aspects** (L11 p.50). Common methods (L11 p.50):

- **(a) aggregation and re-coding**
- **(b) k-anonymity**
- **(c) ℓ-diversity and t-closeness**
- **(d) permutation and randomization**
- **(e) differential privacy** (named as today's preferred randomization-based technique but **not covered in detail** in this lecture) (L11 p.50, p.59)

**Aggregation:** replace individual rows with group statistics (e.g., age groups 0–9, 30–39, with mean of X per group) (L11 p.51). **Re-coding:** generalize values (e.g., specific towns Lystrup/Solbjerg → "Aarhus"; Dragør/Frederiksberg → "Copenhagen") (L11 p.52).

### k-anonymity

**What/why:** **k-anonymity is more a property than a method** (L11 p.53). There is **no universal method** to achieve it; **masking and re-coding** are the most common techniques. **Definition:** data about each subject **cannot be distinguished from at least k − 1 other subjects** → the **maximum probability of re-identification is 1/k** (L11 p.53). It is explicitly framed toward **singling out**. Robustness is often unclear due to the **lack of well-defined methods** (L11 p.53). Example: re-coding Location and bucketing X (`< 30000` / `≥ 30000`) and masking ID yields **2-anonymity** (each combination appears ≥ 2 times) (L11 p.54).

### ℓ-diversity (and t-closeness)

**What/why:** **k-anonymity is weak against linkability**: with **background data**, it may be easy to break k-anonymity for any k > 1 (L11 p.55). **ℓ-diversity** (Machanavajjhala et al. 2007) fixes this: a k-anonymous dataset should also contain **ℓ different values for any given sensitive attribute** (L11 p.55).

Worked illustration (L11 p.56–57): a 2-anonymous table where every Copenhagen/`X<30000` row has Condition = *Cardiovascular* and every Aarhus row has *Cancer* leaks the sensitive attribute — knowing someone's location reveals their disease. After enforcing **2-diversity**, each equivalence class contains **both conditions**, so knowing the location no longer reveals the disease (without extra background info) (L11 p.56–57). (**t-closeness** is named alongside ℓ-diversity as another method but not detailed) (L11 p.50).

### Permutation and randomization

**What/why:** **Randomization adds noise** to attributes (L11 p.58). If the released value is `f'(x) = f(x) + g(x)`, typical noise choices `g(·)` are:

- **Gaussian noise:** `f(x) + N(0, σ²)` (normal distribution, variance σ²) (L11 p.58)
- **Laplace noise:** `f(x) + L(0, λ)`, zero-location Laplace with scale ("diversity") parameter λ > 0 (L11 p.58)

Attacks try to **reverse-engineer f(·)** by deducing the secret noise `g(·)` and its parameters (analogy: MCAR vs. MAR in ML) (L11 p.58). **Common mistakes that make attacks easy** (L11 p.59):

- Adding noise to **only one / a few correlated attributes**
- **Inconsistent or out-of-bounds** noise
- Assuming **noise alone is enough** — **sparsity is a big issue**
- **Poorly considering linkability** (background distributions help an attacker)

**Differential privacy** is named as today's preferred randomization-based anonymization technique but **is not covered** in this lecture (L11 p.59). Anonymization is genuinely hard (Figure 17 references a Nature paper on the difficulty) (L11 p.60).

### Data subject rights (the ten rights)

**What/why:** The GDPR grants ten rights (L11 p.61):

- **R1:** Right to be informed
- **R2:** Right to access
- **R3:** Right to rectification
- **R4:** Right to erasure
- **R5:** Right to cancel consent
- **R6:** Right to place restrictions
- **R7:** Right to object to processing
- **R8:** Right to portability
- **R9:** Right to (human, not automated) individual decision-making
- **R10:** Right to be informed about data breaches

**Grouping (L11 p.62):**

- **"Informing" RI = {R1, R10}**
- **"Data" RD = {R2, R3, R4, R6, R8}** — **most relevant for engineering**
- **"Lawfulness" RL = {R5, R7, R9}**

There are **overlaps and logical implications** (L11 p.62):

- If consent is the legal basis and **R5** (cancel consent) is exercised, **deletion (R4)** should usually follow.
- If **R6** (restriction) is exercised, then **R3 ∨ R4 cannot occur simultaneously** — restricting data implies it **cannot be deleted, modified, or updated** at the same time.
- **R9** means a right to have important decisions made by a **human**, not an automated AI/ML system (still debated) (L11 p.63).
- **R8 portability** is still unclear; currently **JSON/CSV dumps on request** seem sufficient (L11 p.63).
- Hadar et al. (2018): developers **overemphasize security and downplay rights** (L11 p.62).

### Rights → software requirements

**What/why:** The **RD** group implies concrete functional requirements: persistence-layer operations (consent control, access, rectification, erasure, restriction) plus **user interfaces** for them (L11 p.63). Architectural guidance from Hjerppe et al. (2019) (L11 p.64–68):

- Apply **compartmentalization and isolation**: e.g., isolate **sensitive personal data** into a separate database; frontends process less-sensitive data (clicks, A/B testing tied to IP) than backends (credit-card data) (L11 p.64).
- A reference architecture maps rights to a **Core Personal Data Module (CPDM)**, a **GDPR-request service**, a **personal-data event log**, consent/restriction centers, and business-logic services, coordinated via a **messaging server / broadcast topic** so each service logs its own changes (L11 p.65, p.68).
- **Article 30** mandates **extensive record-keeping** of all processing: transfers to third parties, security measures, purpose, categories of data, etc. — but recall the **balancing trade-off** with minimization (L11 p.67).
- **Backups** are tricky because RD should apply to them too; currently it seems sufficient to leave backups intact **only if** done **round-robin** so changes eventually propagate as old backups are deleted (L11 p.67).
- Important caveat: **the GDPR imposes no specific software-engineering requirements** — a small company might satisfy RD **manually or with a few scripts**; and architecture can double as the **documentation** required for record-keeping (L11 p.69).

### Organizational obligations: DPIA, DPO, breach notification, documentation

**What/why:** The risk-based approach reaches into requirements engineering (L11 p.73):

- **Data Protection Impact Assessment (DPIA) — Article 35:** mandatory when there is a **high risk to natural persons**. Data protection becomes a **non-functional requirement** (as does its security). Assessments must be **delivered to regulators in case of incidents** (L11 p.73).
- **Data Protection Officer (DPO) — Article 37:** obligation to **designate a DPO**. The DPO is **not personally liable** but has legally imposed tasks (**Articles 38 and 39**), including **coordinating with the DPA** in case of incidents. Ciclosi & Massacci (2023) recommend studying the **EDPB's guidelines** for this role (L11 p.74).
- **Breach notification — Article 33:** "*the controller shall without undue delay and, where feasible, not later than **72 hours** after having become aware of it, notify the personal data breach to the supervisory authority.*" (L11 p.75)
- **Article 34:** a **high-risk** breach must **also be communicated to the affected natural persons** without further delay. A prior risk analysis helps decide what is "high risk"; otherwise the GDPR gives **no clear guidance** (L11 p.75).
- **Documentation:** logging/record-keeping (p.67) implies an obligation to **document all processing**. External communication is via **privacy policies** (who processes, where, what, retention period, etc.). Research shows privacy policies are **generally poor quality** — either too short/vague or 10,000-word legalese (L11 p.76).

### Broader data governance

**What/why:** New EU laws enable pooling data into **data spaces (data lakes)** — mostly non-personal (manufacturing, cultural heritage) but with ambitious **personal-data** plans, including the EU's **digital wallet** (L11 p.71). NGOs like **MyData** push user-controlled personal-data ecosystems, **building on R8 (portability)** (L11 p.71). In practice, developers **seldom need raw personal data** — **synthetic data** is a good idea; keep personal data out of development, only in deployment/production (L11 p.72).

---

## Glossary

- **Privacy** — A philosophical and legal concept; a subjective right given by objective law, captured by six properties P1–P6 (Solove 2002); a fundamental human right (L11 p.4–5).
- **Confidentiality** — Protection of information broadly (humans *and everything else*); a **component** of privacy, **not equal** to privacy (L11 p.5–6).
- **Data protection (DP)** — Requirements (accuracy, security of processing, etc.) that apply even without a privacy violation; **necessary but not sufficient** for privacy (L11 p.7, p.25).
- **Personal data** — "Any information relating to an identified or identifiable natural person" (Art. 4(1)); broader than US "PII" (L11 p.19).
- **PII (personally identifiable information)** — Narrower US/other-jurisdiction notion than GDPR "personal data" (L11 p.19).
- **Processing** — Any operation on personal data, automated or **manual** (Art. 4(2)) (L11 p.19).
- **Sensitive / special-category data** — Race/ethnicity, political opinions, religious/philosophical beliefs, trade-union membership, genetic/biometric (for ID), health, sex life/orientation; processing prohibited by default (Art. 9) (L11 p.20).
- **Data controller** — Decides the **why and how**; responsible for lawfulness and purpose (Art. 4(7)) (L11 p.22).
- **Data processor** — Processes on the controller's behalf, usually under a contract (Art. 4(8)) (L11 p.22).
- **Joint controllers** — Multiple controllers jointly determining purposes/means (L11 p.22).
- **Extraterritoriality** — GDPR applies to processing inside or outside the EU; merely offering goods/services to Europeans suffices (Art. 3) (L11 p.23).
- **Adequacy decision** — EU determination that a non-EU country has adequate data protection, enabling lawful transfers (L11 p.24).
- **Informational self-determination** — The (non-absolute) fundamental right to determine how one's data is collected and used; foundation for consent; 1983 German Constitutional Court (L11 p.25).
- **Lawful basis** — One of six grounds (Art. 6) for processing; exactly one must be chosen (L11 p.26).
- **Legitimate interests** — A controversial lawful basis requiring a balancing test (L11 p.26).
- **Purpose limitation** — Process only for specific stated purposes (Art. 5 principle 2) (L11 p.28).
- **Data minimization** — Collect/process only what is necessary (Art. 5 principle 3) (L11 p.28).
- **Storage limitation** — Keep data identifiable only for a limited time (Art. 5 principle 5) (L11 p.28).
- **Accountability** — Controllers/processors are legally liable and must demonstrate compliance (Art. 5 principle 7) (L11 p.28).
- **DPA (Data Protection Authority)** — National supervisory authority (Germany has several) (L11 p.17).
- **EDPB (European Data Protection Board)** — EU-level coordination body (L11 p.17).
- **DPO (Data Protection Officer)** — Designated role (Art. 37); not personally liable; tasks in Arts. 38–39; liaises with DPA (L11 p.74).
- **DPIA (Data Protection Impact Assessment)** — Mandatory risk assessment when high risk to natural persons (Art. 35) (L11 p.73).
- **Privacy engineering** — Field designing/implementing/evaluating methods and tools to address privacy in sociotechnical systems (Gürses & del Alamo 2016) (L11 p.35).
- **Privacy-by-Design (PbD)** — Cavoukian's 7 foundational principles; privacy proactive and as default (L11 p.36).
- **Privacy-by-policy vs. privacy-by-architecture** — Shift from relying on policies to embedding privacy in software architecture (Spiekermann & Cranor 2009) (L11 p.35).
- **PETs (Privacy Enhancing Technologies)** — Technologies related to PbD/the GDPR (L11 p.36).
- **LINDDUN** — Privacy threat-modeling framework with six properties: Linkability, Identifiability, Non-repudiation, Detectability, Disclosure, Unawareness (Wuyts 2015) (L11 p.40).
- **De-identification** — A method that prevents re-identification (L11 p.42).
- **Anonymization** — Optimally **irreversible** de-identification; GDPR does not apply to strictly anonymized data (L11 p.42, p.44).
- **Pseudonymization** — Removing/replacing direct identifiers; reversible with additional info (Art. 4); ≠ anonymization (L11 p.42–43).
- **Singling out** — Isolating records of one individual (L11 p.43).
- **Linkability** — Linking ≥2 records of an individual across databases (L11 p.43).
- **Inference** — Deducing an attribute value from other attributes (L11 p.43).
- **Masking / Tokenization / Hashing / Encryption** — The four common pseudonymization techniques; all rely on a secret (L11 p.46).
- **Quasi-identifier** — Non-direct identifier (gender, DoB, postal code, income) that can aid re-identification (L11 p.47).
- **Anonymity set** — The set of subjects within which one is not identifiable; larger and more evenly distributed = stronger anonymity (Pfitzmann & Köhntopp 2001) (L11 p.48).
- **k-anonymity** — Each subject is indistinguishable from ≥ k−1 others; max re-identification probability = 1/k (L11 p.53).
- **ℓ-diversity** — A k-anonymous dataset also has ℓ distinct values per sensitive attribute; defends against linkage/attribute disclosure (L11 p.55).
- **t-closeness** — Named alongside ℓ-diversity as an anonymization refinement (not detailed) (L11 p.50).
- **Aggregation / Re-coding** — Replacing values with group statistics / generalized categories (L11 p.51–52).
- **Differential privacy** — Preferred modern randomization-based anonymization (named, not covered in detail) (L11 p.50, p.59).
- **Article 30 record-keeping** — Mandatory extensive records of all processing (L11 p.67).
- **Article 32** — Security of processing: "appropriate technical and organisational measures" (L11 p.33).
- **Article 33 / 34** — 72-hour breach notification to DPA / communication of high-risk breaches to affected persons (L11 p.75).
- **Digital omnibus** — EU process renegotiating parts of the GDPR at lecture time (L11 p.13).
- **MyData** — NGO promoting user-controlled personal-data ecosystems, building on R8 (L11 p.71).
- **Data spaces / data lakes** — EU data-pooling initiatives, including a planned EU digital wallet (L11 p.71).

---

## How-To Cookbook

### A. Determine the correct lawful basis (Article 6)

1. Confirm you are processing **personal data** as defined in Art. 4(1) — any info relating to an identified/identifiable natural person; remember manual processing counts (L11 p.19).
2. Check whether the data is **sensitive/special-category** (Art. 9). If so, processing is **prohibited by default**; you need an Art. 9(2) exemption (e.g., explicit/separate consent, or the data was made public by the person) **in addition to** an Art. 6 basis (L11 p.20).
3. Pick **exactly one** of the six Art. 6 bases — **you must always pick one and only one** (L11 p.26): consent (informed), contract, legal obligation, vital interests, public interest, legitimate interests.
4. Prefer the basis that matches the situation (e.g., **contract** for employment, **legal obligation** for law enforcement, **vital interests** for a medical emergency, **public interest** for education) (L11 p.26).
5. If you choose **legitimate interests**, perform a **balancing test**: weigh your legitimate interests against the rights and interests of the natural persons; document the outcome (L11 p.26).
6. Record the chosen basis as part of **accountability** (Art. 5 principle 7) — you must be able to demonstrate it (L11 p.28).

### B. Respond to a data subject rights request (RD group)

1. Identify which right is being exercised (R2 access, R3 rectification, R4 erasure, R6 restriction, R8 portability) (L11 p.61–62).
2. For **access (R2)**: provide a view of the registered data and, where applicable, **machine-readable data** (L11 p.66).
3. For **rectification (R3)**: update the personal data via the consent/data center (L11 p.66).
4. For **erasure (R4)**: delete the personal data and log the request; note **backups** — currently acceptable to leave them intact if done **round-robin** so changes propagate as old backups are deleted (L11 p.67).
5. For **restriction (R6)**: place a restriction; remember that while restricted, the data **cannot simultaneously be rectified or erased** (R6 implies ¬(R3 ∨ R4)) (L11 p.62).
6. For **portability (R8)**: deliver a **JSON/CSV (or similar) dump** on request — currently sufficient (L11 p.63).
7. If **consent (R5)** is cancelled and consent was the legal basis, **follow up with deletion (R4)** in most cases (L11 p.62).
8. **Log** the request initialization and fulfillment (this supports Art. 30 record-keeping); use UIs for each operation (L11 p.66, p.68).
9. Pragmatic check first: decide whether you even need bespoke software — a small company may handle RD **manually or with a few scripts**; the GDPR imposes **no specific SE requirements** (L11 p.69).

### C. Conduct a DPIA (Article 35)

1. Trigger: assess whether the processing poses a **high risk to natural persons**; if so, a DPIA is **mandatory** (L11 p.73).
2. Treat data protection (and its security) as **non-functional requirements** affecting requirements engineering (L11 p.73).
3. Use a **risk matrix** (impact × probability), as ENISA (2017) suggests and as discussed for cybersecurity risk (L11 p.38).
4. Map controls against, e.g., the NIST control families (authority/purpose, accountability/auditing, data quality, minimization/retention, participation/redress, security, transparency, use limitation) (L11 p.37–39).
5. Keep the assessment ready: it must be **delivered to regulators in case of incidents** (L11 p.73).

### D. Handle a personal-data breach (Articles 33 & 34)

1. Detect and confirm the breach; record when you **became aware** of it (L11 p.75).
2. Notify the **supervisory authority (DPA)** without undue delay, **and within 72 hours** where feasible (Art. 33) (L11 p.75).
3. Determine severity using your **prior risk analysis**; if **high-risk**, also **communicate to affected natural persons** without further delay (Art. 34) (L11 p.75).
4. The DPO **coordinates with the DPA** during incidents (Arts. 38–39) (L11 p.74).
5. Have your **DPIA/risk analysis** available for regulators (L11 p.73).

### E. Pseudonymize vs. anonymize a dataset

1. Decide your goal. If you want the data **outside GDPR scope**, you must achieve **strict anonymization** (irreversible) — the GDPR does not apply to strictly anonymized data (L11 p.44).
2. For **pseudonymization** (reversible), remove/replace **direct identifiers** using encryption, hashing, masking, and/or tokenization (often a combination); protect the secret (L11 p.46–47).
3. **Mask all direct identifiers** (names, addresses, SSNs, license plates, IP addresses, device fingerprints) (L11 p.47).
4. Remember pseudonymization only really addresses **linkability**; **singling out and inference** may remain — still personal data, accountability still applies (you must demonstrate it) (L11 p.43–44).
5. For **anonymization**, defend against **all three**: singling out, linkability, inference (L11 p.50). Apply methods like aggregation/re-coding, **k-anonymity**, **ℓ-diversity / t-closeness**, randomization, or differential privacy (L11 p.50).
6. Validate against re-identification attacks; account for **probability/distribution** (size of anonymity set alone is insufficient) and **background data** that breaks k-anonymity (L11 p.49, p.55).

### F. Apply k-anonymity then ℓ-diversity (worked recipe)

1. Identify the **quasi-identifiers** and the **sensitive attribute** (L11 p.47, p.56).
2. Use **masking** (e.g., mask ID) and **re-coding/bucketing** (e.g., Location → city, X → `<30000` / `≥30000`) so each combination of quasi-identifiers appears **≥ k** times → **k-anonymity** (max re-identification prob. 1/k) (L11 p.53–54).
3. Check for **attribute disclosure**: if every record in an equivalence class shares the same sensitive value, k-anonymity leaks it (L11 p.56).
4. Enforce **ℓ-diversity**: ensure each equivalence class contains at least **ℓ distinct values** of the sensitive attribute, so location no longer reveals the condition (L11 p.55, p.57).
5. Beware **linkability with background data** — it can still break k-anonymity for any k > 1 (L11 p.55).

### G. Randomize attributes safely (noise addition)

1. Choose a noise function `g(·)`: **Gaussian** `N(0, σ²)` or **Laplace** `L(0, λ)` with scale λ > 0, releasing `f'(x) = f(x) + g(x)` (L11 p.58).
2. Avoid the common mistakes: do **not** add noise to only one / a few **correlated** attributes; avoid **inconsistent or out-of-bounds** noise; do not assume noise alone suffices (**sparsity**); explicitly consider **linkability** (L11 p.59).
3. For stronger guarantees, prefer **differential privacy** (modern preferred technique; not detailed in this lecture) (L11 p.59).

---

## Exam-Style Q&A

**Q1. Define privacy as presented in the lecture. Why is it considered difficult?**
A. Privacy is presented not as one definition but as **six recurring properties** (Solove 2002): P1 right to be left alone, P2 ability to shield oneself from unwanted access, P3 concealment of certain matters, P4 control over personal information, P5 protection of personality/individuality/dignity, P6 control over intimate relationships/aspects of life (L11 p.4). Roughly the whole set P = {P1…P6} constitutes a **fundamental human right**. It is difficult because each property is "extremely difficult philosophically, legally, and politically," and privacy is a **subjective right given by objective law** — a philosophical and legal concept (L11 p.4–5).

**Q2. How do privacy, confidentiality, and data protection relate?**
A. **Confidentiality is a component of privacy, not the same thing** — and it is broader in scope (it protects "humans and everything else," whereas privacy concerns humans/personal data) (L11 p.5–6). **Data protection** overlaps with privacy but is "not the same": DP requirements (accuracy, security of processing) apply **even when there is no privacy violation** (L11 p.7). DP is **necessary but not sufficient** for privacy, and **both security and data protection are necessary for privacy** (L11 p.5, p.25).

**Q3. The GDPR is a "regulation," not a "directive." Why does that matter, and how much national variation remains?**
A. A **regulation is directly applicable EU law** in all member states (a directive would need national transposition), which underlines **harmonization** (L11 p.16). Variation remains because the GDPR gives member states **leeway** — most made/updated a national data-protection law. Flexibility is allowed especially for legal obligations/public interests (Art. 6), sensitive data (Art. 9), criminal matters (Art. 10), and scope restrictions for national security/defense/judicial independence (Art. 23) (L11 p.16).

**Q4. What are the six lawful bases for processing, and what is special about choosing one?**
A. Article 6 lists: (1) **consent** (must be informed), (2) **contract**, (3) **legal obligation**, (4) **vital interests**, (5) **public interest**, (6) **legitimate interests** (L11 p.26). You must **always pick exactly one** legal basis. The sixth, **legitimate interests**, is controversial and generally requires a **balancing test** between the natural persons' interests and the claimed legitimate interests (L11 p.26).

**Q5. List and briefly explain the seven Article 5 principles. Why are they important for enforcement?**
A. (1) Lawful, fair, transparent; (2) purpose limitation (specific purposes only); (3) data minimization (only what is necessary); (4) accuracy; (5) storage limitation (identifiable only for limited time); (6) security of processing; (7) accountability (controllers/processors legally liable) (L11 p.28). They are high-level, but **violations of them are frequently used by regulators to justify fines** — empirically **A5 and A6 are the most-cited articles** in enforcement decisions, followed by **A32** (security) (L11 p.28–29).

**Q6. Distinguish data controller from data processor. Why does it matter for supply chains?**
A. A **controller** determines the **why and how** of processing and is responsible for lawfulness and purpose (Art. 4(7)). A **processor** processes personal data **on behalf of** the controller, usually under a **contract/legally binding arrangement** (Art. 4(8)). **Joint controllers** also exist (L11 p.22). It matters for supply chains because **if you hold personal data you are a controller** who can **outsource processing to third-party processors** — responsibilities follow the chain (L11 p.22).

**Q7. What is "personal data" under the GDPR, and how does it compare to US "PII"?**
A. "Any information relating to an identified or identifiable natural person" (Art. 4(1)). This scope is **much wider than the US notion of PII** (L11 p.19). Also, **processing** includes automated *and manual* operations of essentially any kind (Art. 4(2)) (L11 p.19).

**Q8. What is sensitive (special-category) personal data, and how can it be processed?**
A. Data revealing racial/ethnic origin, political opinions, religious/philosophical beliefs, trade-union membership, plus genetic data, biometric data (to uniquely identify), health data, and sex life/sexual orientation. Its processing is **prohibited by default (Art. 9(1))** (L11 p.20). Exemptions (Art. 9(2)) include legal obligations of public-sector bodies, possibly a **separate/explicit consent**, or that the **person made the data public** (e.g., social media) (L11 p.20).

**Q9. Explain extraterritoriality and the rule for international data transfers.**
A. The GDPR is **extraterritorial**: it applies to controllers/processors **inside or outside the EU**, and per **Article 3**, **merely offering goods or services to Europeans suffices** (L11 p.23). For **transfers** to a non-EU country, it is generally lawful **only if EU authorities determined that country has an adequate level of data protection** (adequacy) (L11 p.24).

**Q10. List the ten GDPR data subject rights and the three groups. Which group matters most for engineering?**
A. R1 informed, R2 access, R3 rectification, R4 erasure, R5 cancel consent, R6 restriction, R7 object, R8 portability, R9 human decision-making, R10 informed about breaches (L11 p.61). Groups: **Informing RI = {R1, R10}**, **Data RD = {R2, R3, R4, R6, R8}**, **Lawfulness RL = {R5, R7, R9}** (L11 p.62). **RD is most relevant for engineering** (it implies persistence-layer operations plus UIs) (L11 p.62–63).

**Q11. Give two examples of logical implications/overlaps among the rights.**
A. (1) If **consent** is the basis and **R5** (cancel consent) is exercised, **deletion R4** should follow in most cases. (2) If **R6** (restriction) is exercised, **R3 ∨ R4 cannot occur simultaneously** — restricting implies the data cannot be deleted, modified, or updated at the same time (L11 p.62).

**Q12. What does Article 32 require about security, and what is notable about how it specifies it?**
A. Art. 32(1) requires "appropriate technical and organisational measures to ensure a level of security appropriate to the risk," considering **state of the art, cost, and the nature/scope/context/purposes of processing** plus the risk to rights and freedoms (L11 p.33). Notably, it **does not give technical details** — it mentions pseudonymization, encryption, the CIA triad, resilience, and testing, but leaves the *how* to engineers (L11 p.33).

**Q13. Pseudonymization vs. anonymization — define both and explain the GDPR consequence.**
A. **Anonymization** is *optimally irreversible* de-identification; **pseudonymization** removes/replaces direct identifiers but is **reversible with additional information** (Art. 4) (L11 p.42). They are **not equal**. Evaluate against **singling out, linkability, inference**; pseudonymization generally addresses **only linkability** (L11 p.43). Consequence: **the GDPR does not apply to strictly anonymized data**, but it **does** apply to pseudonymized data, and **accountability still requires you to demonstrate** the pseudonymization (Art. 11 relieves you of acquiring extra identifying info solely to comply) (L11 p.44).

**Q14. Explain k-anonymity and why ℓ-diversity is needed.**
A. **k-anonymity:** each subject is indistinguishable from at least **k−1 others**, so the **maximum re-identification probability is 1/k**; it targets **singling out**, achieved via masking/re-coding (L11 p.53). It is weak against **linkability with background data** and against **attribute disclosure** — if every record in an equivalence class shares the same sensitive value, the sensitive attribute leaks. **ℓ-diversity** (Machanavajjhala et al. 2007) requires each equivalence class to contain **ℓ distinct values of the sensitive attribute**, so knowing the quasi-identifiers no longer reveals the sensitive value (L11 p.55–57).

**Q15. What are the breach-notification obligations under Articles 33 and 34?**
A. **Article 33:** the controller must notify the **supervisory authority (DPA)** without undue delay and, where feasible, **not later than 72 hours** after becoming aware of the breach. **Article 34:** a **high-risk** breach must **also be communicated to the affected natural persons** without further delay; a prior risk analysis helps decide what counts as high-risk (the GDPR gives no clear guidance otherwise) (L11 p.75).

**Q16. What are the GDPR's twofold goals, and why is this politically significant?**
A. The goals are **(1) to protect natural persons** and **(2) to facilitate the free flow of personal data across the union** — making the GDPR also an **enabler for a fair European data economy** (L11 p.14). Politically it was the EU's most lobbied law; heavy lobbying **decreased its legitimacy** (Hildén 2019), and enforcement/SME-compliance problems remain on the agenda (L11 p.14).

---

## Gotchas

- **Confidentiality ≠ privacy.** Confidentiality is a *component* of privacy and is actually *broader* in scope (protects humans and everything else). Don't equate the two (L11 p.5–6).
- **Data protection is not the same as privacy.** DP requirements (accuracy, security) can apply *even with no privacy violation*; DP is necessary but not sufficient for privacy (L11 p.7, p.25).
- **Exactly one lawful basis.** You must always pick **one and only one** Art. 6 basis — not several, and consent is just one option (often over-assumed) (L11 p.26).
- **Consent must be informed**, and for **sensitive data** you may need a **separate/additional** consent under Art. 9(2) on top of an Art. 6 basis (L11 p.20, p.26).
- **Legitimate interests is controversial** and needs a **balancing test** — it is not a free pass (L11 p.26).
- **Personal data ≠ PII.** GDPR "personal data" is *much broader* than the US PII concept (L11 p.19).
- **Manual processing is in scope.** Processing is not limited to automated/computerized operations (L11 p.19).
- **Pseudonymization ≠ anonymization.** Pseudonymized data is **still personal data** (GDPR applies); only **strictly anonymized** data is out of scope. Pseudonymization mainly addresses **linkability**, not singling out or inference (L11 p.43–44).
- **Accountability still applies to pseudonymization** — you must be able to *demonstrate* it (L11 p.44).
- **Article 11 nuance:** if you no longer need to identify a subject, you are *not obliged* to keep/acquire extra identifying info just to comply — but this does not exempt you from accountability (L11 p.44).
- **Anonymity-set size alone is not enough.** Anonymity is also a *probability* concept; an evenly distributed, large set is needed; distribution matters (Shannon entropy) (L11 p.48–49).
- **k-anonymity is fragile.** Background data can break it for any k > 1, and it does not prevent **attribute disclosure** — that is what **ℓ-diversity** addresses (L11 p.55).
- **Randomization mistakes.** Adding noise to only one/few correlated attributes, inconsistent/out-of-bounds noise, ignoring sparsity, and ignoring linkability all make attacks easy (L11 p.59).
- **Restriction (R6) conflicts with rectification/erasure.** While restricted, data cannot be simultaneously deleted/modified/updated (¬(R3 ∨ R4)) (L11 p.62).
- **Cancelling consent (R5) usually triggers erasure (R4)** when consent was the legal basis (L11 p.62).
- **Backups are tricky.** RD should apply to backups; current pragmatic approach is round-robin backups so deletions propagate over time — not immediate deletion from every backup (L11 p.67).
- **72-hour breach clock** is "where feasible" and starts when the controller **becomes aware** — and high-risk breaches *also* require notifying the **affected individuals** (Art. 34), not just the DPA (L11 p.75).
- **The GDPR imposes no specific software-engineering requirements.** Don't over-engineer — small operators can satisfy RD manually or with scripts; architecture can double as required documentation (L11 p.69).
- **Security can conflict with minimization.** Logging/monitoring keep more data; minimization wants less — you must *balance* (L11 p.32, p.67).
- **Developers' bias.** Research (Hadar et al. 2018) shows developers **overemphasize security and downplay rights** — a known blind spot (L11 p.62).
- **Differential privacy and t-closeness are named but not covered in detail** in this lecture; don't over-claim depth on them from this source (L11 p.50, p.59).
- **Legal flux:** parts of the GDPR are being renegotiated via the **"digital omnibus,"** so specific details may change (fundamentals likely stable) (L11 p.13).
- **Workplace/employment privacy and some criminal matters are governed by separate laws**, not solely the GDPR (L11 p.9).
