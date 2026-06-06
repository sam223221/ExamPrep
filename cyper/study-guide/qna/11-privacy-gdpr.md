# 11. Privacy, Data Protection & GDPR — Simulated Open-Book Questions

### [EASY] A Danish online shop processes a customer's shipping address to deliver a product the customer just bought. Which Article 6 lawful basis fits best, and why is it not "consent"?

**Answer:** The best fit is **contract** (Art. 6(1)(b)) — processing the address is necessary to perform the sales/delivery contract the customer entered into (L11 p.26).

It is **not** consent because:

1. You must pick **exactly one** lawful basis, not the most convenient-sounding one (L11 p.26).
2. The processing is *required* to fulfil the order, so it is contractual necessity, not a freely-given optional permission.
3. If you relied on consent, the customer could withdraw it (R5) and you could no longer ship the goods — which makes consent the wrong basis where the processing is intrinsic to a contract the user actively requested.

The lecture explicitly gives "contract — e.g., employment" as the canonical contract example; delivery of a purchased good is the same logic (L11 p.26).

### [EASY] A hospital processes a unit's patient's blood type to treat them after they collapsed and are unconscious. Which Article 6 lawful basis applies?

**Answer:** **Vital interests** (Art. 6(1)(d)) applies — the lecture gives "vital interests — e.g., healthcare emergencies" as the textbook example (L11 p.26).

The reasoning is that the patient is unconscious and cannot give consent, there is no contract being performed, but processing the data is necessary to protect the life/physical safety of the natural person. Note that health data is also special-category data under Art. 9, so in a full analysis an Art. 9(2) exemption would be needed *in addition to* the Art. 6 basis (L11 p.20), but among the six Art. 6 bases, vital interests is the correct choice.

### [EASY] A SaaS company stores its EU customers' personal data on AWS, which only runs the servers and never decides why the data is processed. Classify the SaaS company and AWS.

**Answer:**

1. The **SaaS company is the data controller** — it determines the **"why" and "how"** of the processing and is responsible for lawfulness and purpose (Art. 4(7)) (L11 p.22).
2. **AWS is the data processor** — it processes personal data **on behalf of** the controller, typically under a **contract or legally binding arrangement** (Art. 4(8)) (L11 p.22).

The general rule from the lecture is: if you hold personal data, you are a controller, and you may outsource processing to third-party processors down the supply chain (L11 p.22).

### [EASY] A user emails a company asking for a copy of all personal data the company holds about them. Which data-subject right is this, which rights group does it belong to, and roughly how can it be satisfied?

**Answer:** This is the **right to access (R2)** (L11 p.61).

1. It belongs to the **"Data" group RD = {R2, R3, R4, R6, R8}**, which is the group most relevant for engineering (L11 p.62).
2. To satisfy it, you provide a view of the registered data and, where applicable, machine-readable data (L11 p.66). A small operator does not need bespoke software — the GDPR imposes no specific software-engineering requirements, so this can even be handled manually or with a few scripts (L11 p.69).

### [EASY] A controller discovers a personal-data breach. By when must it notify the supervisory authority, and from what moment does that clock start?

**Answer:** Under **Article 33**, the controller must notify the **supervisory authority (DPA)** without undue delay and, where feasible, **not later than 72 hours** after becoming aware of the breach (L11 p.75).

The clock starts from the moment the controller **becomes aware** of the breach, not from when the breach actually occurred. The "72 hours" is qualified by "where feasible," so you record when you became aware and act promptly. If the breach is high-risk, Article 34 additionally requires communicating it to the affected natural persons (L11 p.75).

### [MEDIUM] An EU marketing firm wants to send promotional emails to existing customers, justifying it as good for business. It plans to rely on "legitimate interests." What extra step does the lecture say is required, and what is the risk if the firm skips it?

**Answer:** The firm must perform a **balancing test** (L11 p.26).

1. Legitimate interests (Art. 6(1)(f)) is described as the **controversial** basis: using it generally requires weighing the firm's claimed legitimate interests against the **rights and interests of the natural persons** (L11 p.26).
2. The lecture's own example for legitimate interests is in fact "marketing," so the basis is plausible — but it is **not a free pass** (L11 p.26, Gotchas).
3. If the firm skips the balancing test, it cannot demonstrate the basis was validly chosen. Because **accountability** (Art. 5 principle 7) makes the controller legally liable and requires it to *demonstrate* compliance (L11 p.28), the firm risks an enforcement fine — and empirically **A5 and A6 are the most-cited articles in fines**, exactly this kind of lawfulness failure (L11 p.29).

The firm should document the balancing outcome as part of accountability (L11 p.405-style cookbook step, p.28).

### [MEDIUM] A company runs a basic analytics page and a separate database holding customers' credit-card data. Using the lecture's architectural guidance, how should it structure storage, and what principle does this serve?

**Answer:** The company should apply **compartmentalization and isolation** (Hjerppe et al. 2019) (L11 p.64).

1. Isolate the **sensitive / most-sensitive personal data** (the credit-card data) into a **separate database** (L11 p.64).
2. Let the **frontend** process the *less*-sensitive data — clicks, A/B testing tied to IP — while the **backend** handles the highly sensitive credit-card data (L11 p.64).

This serves several principles at once: **data minimization** and **security of processing** (Art. 5 principles 3 and 6) (L11 p.28), and it operationalizes **privacy-by-architecture** rather than mere privacy-by-policy (Spiekermann & Cranor 2009) (L11 p.35). It also aligns with NIST's "security" and "data minimization/retention" controls (L11 p.38-39).

### [MEDIUM] A US-based startup has no EU office and no EU servers but runs a website in several EU languages, prices in euros, and ships to EU customers. Is it caught by the GDPR? Justify with the relevant Article.

**Answer:** Yes, it is caught by the GDPR.

1. The GDPR is **extraterritorial** — it applies to organizations controlling or processing personal data **inside or outside the EU** (L11 p.23).
2. Per **Article 3**, **merely offering goods or services to Europeans (European natural persons) suffices** to fall under the GDPR (L11 p.23).
3. Pricing in euros, offering EU-language sites, and shipping to EU customers are clear evidence of *targeting* EU natural persons — so offering goods/services is established.

Having no EU office or servers is irrelevant; the lecture stresses this extraterritorial reach has caused major international schisms and court cases (L11 p.23).

### [MEDIUM] A dataset has direct identifiers replaced by encrypted tokens, but the company keeps the decryption key so it can reverse the mapping when needed. Is this anonymization or pseudonymization, and does the GDPR still apply?

**Answer:** This is **pseudonymization**, not anonymization, and **the GDPR still applies**.

1. Pseudonymization **removes or replaces direct identifiers**, but the data "can no longer be attributed to a specific data subject *without the use of additional information*" (Art. 4) — here the kept decryption key is exactly that additional information, making it **reversible** (L11 p.42).
2. Anonymization is **optimally irreversible** de-identification; keeping the key means re-identification is possible, so this fails the anonymization bar (L11 p.42).
3. **The GDPR does NOT apply only to strictly anonymized data** — pseudonymized data is still personal data, so the GDPR applies in full (L11 p.44).
4. Furthermore, the **accountability criterion still applies to pseudonymization**: the company must be able to **demonstrate** what it did (L11 p.44).

### [MEDIUM] A company is about to deploy a large-scale system that profiles individuals' health and behavior in a way likely to pose high risk to people. Which organizational obligation is triggered before deployment, under which Article, and what must the company do with the result?

**Answer:** A **Data Protection Impact Assessment (DPIA)** is triggered under **Article 35** (L11 p.73).

1. A DPIA is **mandatory when there is a high risk to natural persons** — large-scale health/behavior profiling clearly qualifies (L11 p.73).
2. This makes data protection (and its security) a **non-functional requirement** in requirements engineering (L11 p.73).
3. The company should use a **risk matrix** (impact × probability), as ENISA (2017) suggests (L11 p.38), and map controls against the NIST control families (L11 p.37-39).
4. Crucially, the assessment must be **kept ready and delivered to regulators in case of incidents** (L11 p.73).

### [HARD] A user who had consented to marketing emails now sends a request to withdraw consent. The marketing data was processed solely on the basis of that consent. Walk through which rights this triggers, the order of operations, and one technical wrinkle around backups.

**Answer:** Step through the logic:

1. The user is exercising **R5 — right to cancel consent** (L11 p.61).
2. Because **consent was the legal basis** for this processing, the lecture's logical implication kicks in: when R5 is exercised and consent was the basis, **deletion (R4) should usually follow** (L11 p.62). So R5 cascades into **R4 — right to erasure**.
3. Order of operations: (a) record/cancel the consent in the consent center, (b) trigger erasure of the personal data, (c) **log** the request initialization and fulfilment to support Art. 30 record-keeping (L11 p.66-68).
4. **Backup wrinkle:** R4 should in principle apply to backups too, which is tricky. The current pragmatic approach is to leave backups intact **only if** they are done **round-robin**, so the deletion eventually propagates as old backups are rotated out and deleted — rather than forcing immediate deletion from every backup (L11 p.67).

A subtle trap: do *not* keep processing the data under a different unstated basis after consent is withdrawn — you must always have exactly one valid basis, and here it has just disappeared (L11 p.26).

### [HARD] You are given a 2-anonymous medical table. Every Copenhagen / income<30000 equivalence class has Condition = Cardiovascular, and every Aarhus class has Condition = Cancer. An attacker knows their target lives in Aarhus. Explain the attack, name the failure, and state the fix precisely.

**Answer:** Step through it:

1. **The attack:** k-anonymity (here k=2) guarantees the target cannot be **singled out** — they are indistinguishable from at least k−1=1 other person, so max re-identification probability is 1/k = 1/2 (L11 p.53). **But** the attacker does not need to single out the exact row. Because every Aarhus equivalence class shares the *same* sensitive value (Cancer), simply knowing the target is in Aarhus reveals their Condition = Cancer (L11 p.56).
2. **The failure name:** this is **attribute disclosure**, the known weakness of k-anonymity. k-anonymity targets **singling out**, but it is **weak against linkability and attribute disclosure** — when an equivalence class is homogeneous in the sensitive attribute, the attribute leaks regardless of k (L11 p.55-56).
3. **The fix:** enforce **ℓ-diversity** (Machanavajjhala et al. 2007): require that each equivalence class contain at least **ℓ distinct values of the sensitive attribute** (L11 p.55). Concretely, apply **2-diversity** so each class (e.g., each Aarhus class) contains **both** Cardiovascular *and* Cancer. Then knowing the location no longer reveals the disease without extra background information (L11 p.56-57).
4. **Residual caveat:** even ℓ-diversity can be undermined by **background data**, which can break k-anonymity-style protections for any k > 1 — so the analyst must still consider what auxiliary information an attacker plausibly has (L11 p.55).

### [HARD] A startup wants to "put its dataset outside GDPR scope" so it never has to honor access/erasure requests on it. Its plan: hash all names and emails with SHA-256 (no key stored) and call it anonymized. Critique this plan against the three de-identification elements and state what would actually be required.

**Answer:** The plan is flawed. Evaluate against the **three elements** the lecture requires (L11 p.43):

1. **Singling out:** Hashing direct identifiers does not stop you from isolating one individual's records — quasi-identifiers (gender, DoB, postal code, income) remain and can still single someone out (L11 p.43, p.47).
2. **Linkability:** A deterministic, keyless hash is **stable** — the same email always hashes to the same value — so records about one person can still be **linked across databases**, and an attacker can hash a known email to find the matching row. Pseudonymization "generally addresses only linkability," and hashing here barely even does that (L11 p.43, p.46).
3. **Inference:** Nothing in this plan prevents inferring sensitive attributes from the remaining quasi-identifiers (L11 p.43).

Conclusion: hashing direct identifiers is a **pseudonymization** technique (one of the four: encryption, hashing, masking, tokenization), not anonymization (L11 p.46). The data therefore **remains personal data and the GDPR still applies** — the startup must still honor access/erasure (L11 p.44).

To actually escape GDPR scope, the data must be **strictly, optimally irreversibly anonymized**, defending against **all three** of singling out, linkability, and inference (L11 p.44, p.50) — e.g., aggregation/re-coding, **k-anonymity plus ℓ-diversity/t-closeness**, randomization, or differential privacy, validated against re-identification attacks and accounting for background data (L11 p.50, p.443-style cookbook).

### [HARD] A controller wants to add Laplace noise to a single income column in a released dataset to "anonymize" it, leaving every other attribute untouched. List the mistakes the lecture warns about and explain why each makes an attack easier.

**Answer:** Randomization releases `f'(x) = f(x) + g(x)`; here `g(·)` is Laplace noise `L(0, λ)` with scale λ > 0 (L11 p.58). The plan commits several of the lecture's named mistakes (L11 p.59):

1. **Adding noise to only one / a few correlated attributes.** Income correlates with untouched attributes (postal code, occupation, age). An attacker can use the clean correlated columns to estimate the true income and effectively cancel the noise. This is the headline mistake the plan makes.
2. **Ignoring linkability / background distributions.** Leaving all other attributes pristine means **background distributions help an attacker** reconstruct or link records; the lecture warns linkability must be explicitly considered (L11 p.59).
3. **Risk of inconsistent or out-of-bounds noise.** Naive additive noise can push income negative or to implausible values, which an attacker spots and corrects, leaking the underlying signal (L11 p.59).
4. **Assuming noise alone is enough — sparsity.** In sparse regions (e.g., very high incomes with few people), a single noisy value is still close to a unique true value, so noise does not hide it (L11 p.59).

The attacker's general strategy is to **reverse-engineer f(·)** by deducing the secret noise `g(·)` and its parameters (L11 p.58). The lecture's recommendation for stronger guarantees is **differential privacy**, today's preferred randomization-based technique (though not detailed in the lecture) (L11 p.59).

### [HARD] A company received an erasure request (R4) yesterday and a restriction request (R6) on the *same* records today. An engineer says "just do both — delete and restrict." Explain why this is logically problematic and how to resolve it.

**Answer:** The two operations are **logically incompatible at the same time**, per the lecture's rights logic.

1. When **R6 (restriction)** is exercised, it implies the data **cannot be deleted, modified, or updated** while restricted — formally **R6 implies ¬(R3 ∨ R4)** (L11 p.62). Restriction is precisely a "freeze": the controller keeps the data but stops actively processing it.
2. Therefore you cannot simultaneously honor R6 (freeze the records) and R4 (erase the records) — erasing is exactly what restriction forbids during the restricted period (L11 p.62).

**Resolution:**

1. Treat the two requests as sequential states, not concurrent operations. Determine the data subject's actual current intent — a restriction request normally means "do not process for now," which supersedes an immediate erasure.
2. Apply the **restriction (R6)** and place the records in a frozen state, logging the request (L11 p.66-68).
3. Only once the restriction is lifted (or the subject clarifies they want erasure instead) can erasure (R4) be carried out. The engineer's "do both at once" instruction violates the R6 ⇒ ¬(R3 ∨ R4) implication and must be rejected.

### [VERY HARD] A research hospital publishes a "k-anonymized, k=5" dataset and claims the GDPR no longer applies because it is "anonymized." A journalist re-identifies a patient using a leaked voter roll. Analyze every flawed assumption in the hospital's claim, citing the relevant lecture points.

**Answer:** The hospital made several layered errors:

1. **k-anonymity is a property, not a guaranteed anonymization method.** The lecture stresses k-anonymity "is more a property than a method," with **no universal method** to achieve it and robustness "often unclear due to the lack of well-defined methods" (L11 p.53). Claiming k=5 alone equals "anonymized" overstates the guarantee.
2. **k-anonymity only targets singling out, not the full bar for anonymization.** Anonymization must defend against **all three** of singling out, linkability, and inference (L11 p.50). k-anonymity is explicitly framed toward **singling out** and is **weak against linkability** (L11 p.53, p.55).
3. **Background data breaks it.** The lecture warns that "with background data, it may be easy to break k-anonymity for any k > 1" (L11 p.55). The leaked voter roll is exactly such background data, enabling **linkage** to re-identify the patient — the textbook failure mode.
4. **No ℓ-diversity / t-closeness.** Even setting aside linkage, plain k-anonymity does not prevent **attribute disclosure**; the hospital should have layered **ℓ-diversity** (and possibly t-closeness) on top (L11 p.55).
5. **The legal consequence is wrong.** The GDPR is out of scope **only for strictly, optimally irreversibly anonymized data** (L11 p.42, p.44). Because re-identification succeeded, the data was never truly anonymous (only "identifiable" in Hintze's levels), so it remained **personal data** and the GDPR applied the whole time (L11 p.45).
6. **Probability was ignored.** Anonymity is also a probability concept — set size alone is insufficient; distribution matters (Shannon entropy) (L11 p.48-49). A homogeneous or sparse k=5 class can still be effectively identifying.

**Bottom line:** the hospital confused a fragile statistical property for legal anonymity, ignored linkability against auxiliary datasets, and as a result likely suffered a reportable personal-data breach still governed by the GDPR.

### [VERY HARD] A company processes EU users' political opinions (special-category data) for a public-education campaign run on behalf of a government ministry. Build the full lawful-processing analysis: Article 9 status, the needed Article 6 basis, any additional requirement, and the controller/processor split.

**Answer:** Work it as a layered analysis:

1. **Article 9 status — sensitive data.** Political opinions are explicitly **special-category data**, whose processing is **prohibited by default** under Art. 9(1) (L11 p.20). So you cannot proceed on an Art. 6 basis alone.
2. **Need an Article 9(2) exemption.** You must find an Art. 9(2) exemption *in addition to* an Art. 6 basis (L11 p.20, cookbook p.402). The lecture notes exemptions such as legal obligations of public-sector bodies, a **separate/additional explicit consent**, or that the **person made the data public** (e.g., on social media) (L11 p.20). For a government education campaign, either explicit separate consent or a public-sector legal-obligation route would be candidates — but Art. 9 must be satisfied regardless.
3. **Exactly one Article 6 basis.** You still must pick **exactly one** Art. 6 basis (L11 p.26). "Public interests — e.g., education" is the lecture's own education example (L11 p.26), making **public interest** the natural Art. 6 choice for an education campaign run for a ministry. (If instead relying on consent, recall consent must be informed and could be withdrawn.)
4. **Controller / processor split.** The **ministry** determines the "why and how" (the campaign's purpose) and is therefore the **controller**; the **company** processing on the ministry's behalf under a contract/legally binding arrangement is the **processor** (Art. 4(7)/(8)) (L11 p.22). Depending on how purposes are co-decided, they could also be **joint controllers** (L11 p.22).
5. **Member-state leeway flag.** Note that Art. 6 public-interest grounds and Art. 9 sensitive-data handling are exactly the areas where member states retain **leeway** and have national data-protection laws (L11 p.16) — so the national DP law must also be checked.

**Summary:** Art. 9(1) prohibition lifted via an Art. 9(2) exemption, **plus** one Art. 6 basis (public interest fits), with the ministry as controller and the company as processor (or joint controllers), and accountability documentation throughout (L11 p.28).

### [VERY HARD] An engineer argues: "We encrypt all personal data and have a strong infosec program, so we are fully privacy-compliant — confidentiality is privacy." Dismantle this in terms of the lecture's privacy/confidentiality/data-protection distinctions and the developer-bias research.

**Answer:** The argument conflates three distinct concepts and reflects a documented bias.

1. **Confidentiality is not privacy.** The lecture is explicit: **confidentiality is a *component* of privacy, not the same thing**, and it is actually *broader* in scope — confidentiality protects "humans and everything else," whereas privacy concerns humans/personal data (L11 p.5-6). So even perfect confidentiality does not equal privacy.
2. **Security alone is insufficient.** "Both security and data protection are necessary for privacy, but neither alone is sufficient" (L11 p.5). Encryption/infosec addresses security; it does nothing for, e.g., data minimization, purpose limitation, or honoring data-subject rights.
3. **Data protection ≠ privacy, and applies even without a privacy violation.** DP requirements such as accuracy and security of processing apply **even when there is no privacy violation** (L11 p.7). You can fully breach DP law (e.g., processing without a lawful basis, ignoring R2/R4 requests) while keeping data perfectly confidential — and **A5/A6 violations, not encryption failures, dominate enforcement fines** (L11 p.29).
4. **The rights dimension is missing.** Encryption does nothing to satisfy the **RD** engineering rights (access, rectification, erasure, restriction, portability), which require persistence-layer operations and UIs (L11 p.62-63).
5. **This is a textbook developer bias.** Hadar et al. (2018) found developers **overemphasize security and downplay rights** — exactly the blind spot this engineer exhibits (L11 p.62). The lecture even notes a "seemingly artificial conflict" between security and privacy, since logging/monitoring (security) keeps *more* data while **data minimization** wants *less* — so a security-maximizing program can actively *harm* a privacy principle (L11 p.32).

**Conclusion:** strong encryption is one valid Art. 32 security measure, but it is neither necessary-and-sufficient for privacy nor a substitute for lawful basis, the Art. 5 principles, or data-subject rights.

### [VERY HARD] A breach exposes a pseudonymized customer table (direct identifiers tokenized; the token-mapping vault was NOT exposed). Management says "it's pseudonymized, so no notification is needed." Evaluate this claim and lay out the correct breach-handling decision process.

**Answer:** Management's claim is wrong as stated — pseudonymization does **not** automatically exempt a breach from notification. Work the decision process:

1. **It is still personal data, so it is still a personal-data breach.** Pseudonymized data remains personal data under the GDPR (L11 p.44); a breach of it is a breach within Art. 33's scope. Pseudonymization "generally addresses only linkability" and its focus is on **security** — it reduces, but does not eliminate, risk (L11 p.43).
2. **Article 33 notification is the default.** The controller must notify the **DPA** without undue delay and, where feasible, **within 72 hours** of becoming aware (L11 p.75). Record when awareness occurred; the clock starts there.
3. **Assess risk for Article 34.** Whether the *affected individuals* must also be told depends on whether it is a **high-risk** breach (Art. 34) (L11 p.75). Here pseudonymization is *relevant* to that risk assessment: because the **token-mapping vault was not exposed**, re-identification requires the missing "additional information," which lowers the risk to individuals. Use your **prior risk analysis / DPIA** to make this determination — the GDPR gives no clear guidance otherwise (L11 p.75, p.73).
4. **Possible outcome.** A defensible analysis might conclude: notify the DPA under Art. 33 (or at least document the reasoning if you judge no risk to rights/freedoms), but the un-exposed vault may justify *not* triggering Art. 34 individual communication if risk is genuinely low. The key is that this is a *reasoned risk decision*, not an automatic exemption.
5. **Roles and records.** The **DPO coordinates with the DPA** during the incident (Arts. 38-39) (L11 p.74), and the **DPIA/risk analysis must be available to regulators** (L11 p.73). **Accountability** means you must be able to *demonstrate* the reasoning behind whatever decision you make (L11 p.28, p.44).

**Bottom line:** pseudonymization is a mitigating factor in the *risk assessment for Art. 34*, not a blanket excuse to skip the Art. 33 notification analysis.

### [VERY HARD] A Brazilian fintech with no EU office runs a euro-priced app aimed at EU residents. It fully automates loan approvals/rejections with an ML model, and it routes all EU users' data to its São Paulo servers for processing. A rejected EU user demands (a) that a human review the decision and (b) a copy of their data. Management replies: "We're not in the EU, the model decides, and the data lives in Brazil, so the GDPR doesn't reach us." Dismantle every layer of this defense, citing the lecture.

**Answer:** Management is wrong on all three layers (scope, the automated-decision right, and the transfer), and the two demands are both enforceable. Work it layer by layer:

1. **"We're not in the EU" — extraterritoriality defeats this.** The GDPR is an **extraterritorial law**: it applies to organizations controlling or processing personal data **inside or outside the EU** (L11 p.23). Per **Article 3**, **merely offering goods or services to Europeans (European natural persons) suffices** to be caught (L11 p.23). A euro-priced app *aimed at* EU residents is textbook targeting, so the fintech is fully within scope despite having no EU office and no EU servers. Having a Brazilian establishment is irrelevant.

2. **"The model decides" — demand (a) is the R9 right.** The user is exercising **R9 — the right to (human, not automated) individual decision-making**, i.e., the right to have important decisions made by a **human, not an automated AI/ML system** (L11 p.61, p.63). A fully automated loan **approval/rejection** is exactly such an important individual decision, so the fintech cannot hide behind "the model decided" — it must provide human review. (The lecture flags R9 as still debated, but it is an enumerated right, and it sits in the **"Lawfulness" group RL = {R5, R7, R9}**) (L11 p.62).

3. **"The data lives in Brazil" — this triggers the transfer rule, it does not escape the law.** Routing all EU users' data to São Paulo is an **international transfer** to a non-EU country. Such a transfer is generally lawful **only if EU-level authorities have determined that country has an adequate level of data protection** (an **adequacy decision**) (L11 p.24). So shipping data to Brazil is not a loophole — it is itself a regulated act that requires an adequacy basis; absent one, the transfer is *unlawful*, compounding the violation rather than escaping it.

4. **Demand (b) is the R2 access right and is unaffected by data location.** "A copy of their data" is the **right to access (R2)**, part of the engineering-critical **Data group RD = {R2, R3, R4, R6, R8}** (L11 p.61–62). It is satisfied by providing a view of the registered data and, where applicable, machine-readable data (L11 p.66); if the user also wanted a transferable export that would be **portability (R8)**, currently a **JSON/CSV dump** is treated as sufficient (L11 p.63). Crucially, the obligation attaches to the **controller** regardless of which jurisdiction the servers physically sit in — the fintech here determines the **why and how** of processing and is therefore the **controller** (Art. 4(7)) (L11 p.22), so it owns these duties.

5. **The trap to avoid.** Do not treat "automated processing" as removing accountability: the fintech remains liable under **accountability** (Art. 5 principle 7) and must be able to **demonstrate** compliance (L11 p.28). And empirically, lawfulness/principle breaches (**A5/A6**) dominate enforcement fines (L11 p.29) — a controller that both processed without honoring rights *and* transferred data without an adequacy basis is exposed on exactly the most-fined grounds.

**Bottom line:** extraterritoriality (Art. 3) pulls the fintech into scope, R9 forces human review of the automated rejection, R2 (and possibly R8) compels the data copy regardless of where servers live, and the Brazil routing is a *regulated transfer requiring adequacy* — not an exit from the GDPR.
