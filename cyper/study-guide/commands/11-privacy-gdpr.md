# 11. Privacy, Data Protection & GDPR — Commands & Code Examples

### Pick the single Article 6 lawful basis (decision checklist)
**What:** Reproduce when an exam asks "what is the lawful basis for processing X, and how do you justify it?" (L11 p.26).
```text
STEP 0  Is this PERSONAL DATA? (Art. 4(1): any info on an identified/identifiable
        natural person; manual processing counts too) ............ if NO -> GDPR n/a
STEP 1  Is it SENSITIVE / special-category? (Art. 9: race/ethnicity, political,
        religious/philosophical, trade-union, genetic, biometric-for-ID, health,
        sex life/orientation) .................. if YES -> need an Art. 9(2) exemption
        (e.g. separate/explicit consent, or person made it public) IN ADDITION
STEP 2  Pick EXACTLY ONE Art. 6 basis (always one, and only one):
        [ ] (1) Consent            -> must be INFORMED
        [ ] (2) Contract           -> e.g. employment
        [ ] (3) Legal obligation   -> e.g. law enforcement
        [ ] (4) Vital interests    -> e.g. healthcare emergency
        [ ] (5) Public interest    -> e.g. education
        [ ] (6) Legitimate interest-> e.g. marketing  *** controversial ***
STEP 3  If you chose (6): run a BALANCING TEST (your interest vs. the natural
        persons' rights/interests) and DOCUMENT the outcome
STEP 4  Record the chosen basis (accountability, Art. 5 principle 7 -> must demonstrate)
```
**Notes:** The classic exam trap is assuming consent. You must pick **exactly one** basis, not several, and consent is just one of six (L11 p.26). Sensitive data needs an Art. 9(2) exemption **on top of** the Art. 6 basis, not instead of it (L11 p.20).

### Audit processing against the seven Article 5 principles (checklist)
**What:** Reproduce when asked to list/apply the Art. 5 principles, or to argue why a regulator would fine an operation (L11 p.28).
```text
[ ] 1. LAWFUL, FAIR & TRANSPARENT processing
[ ] 2. PURPOSE LIMITATION   -> only for specific stated purposes, no other use
[ ] 3. DATA MINIMIZATION    -> collect/process only what is necessary
[ ] 4. ACCURACY             -> only accurate personal data processed
[ ] 5. STORAGE LIMITATION   -> identifiable only for a limited amount of time
[ ] 6. SECURITY OF PROCESSING -> integrity & confidentiality guaranteed
[ ] 7. ACCOUNTABILITY       -> controller/processor legally liable; must demonstrate
```
**Notes:** These are high-level, but **their violations drive most fines**: empirically **A5 (principles) and A6 (lawfulness) are the most-cited articles** in enforcement decisions, followed by **A32 (security of processing)** (L11 p.28–29). Quote that ranking if asked what regulators actually cite.

### Run the de-identification three-element test
**What:** Reproduce when asked to judge whether a dataset is anonymized, pseudonymized, or still re-identifiable (L11 p.43).
```text
Evaluate the released data against ALL THREE elements:
  1. SINGLING OUT  -> can you still isolate the records of ONE individual?
  2. LINKABILITY   -> can you link >=2 records of an individual across databases?
  3. INFERENCE     -> can you infer an attribute value from other attributes
                      (with significant probability)?

Pseudonymization  -> generally addresses ONLY linkability (focus = security)
                  -> singling out + inference may remain -> STILL personal data
Anonymization     -> must defend against ALL THREE -> optimally IRREVERSIBLE
                  -> only then does the GDPR NOT apply
```
**Notes:** Critical exam point: **pseudonymization != anonymization**. Pseudonymized data is still personal data (GDPR applies, accountability still requires you to **demonstrate** it); only **strictly anonymized** data escapes GDPR scope (L11 p.43–44).

### Pseudonymize direct identifiers via hashing + tokenization
**What:** Reproduce when asked to show a small code example of pseudonymization (reversible de-identification) (L11 p.42, p.46).
```python
import hashlib, secrets

# Pseudonymization = remove/replace DIRECT identifiers; relies on a SECRET.
# Reversible: with the additional info (salt / token map) you can re-link.

SECRET_SALT = secrets.token_bytes(16)          # the "additional information"

def pseudonym(direct_id: str) -> str:
    # (b) hashing technique: keyed/salted so it is not a plain dictionary lookup
    return hashlib.sha256(SECRET_SALT + direct_id.encode()).hexdigest()

# (d) tokenization technique: replace value with a token, keep a secret map
token_map = {}                                 # the secret (kept separate, secured)
def tokenize(value: str) -> str:
    if value not in token_map:
        token_map[value] = "tok_" + secrets.token_hex(8)
    return token_map[value]

print(pseudonym("john.doe@example.com"))       # stable pseudonym
print(tokenize("4111 1111 1111 1111"))         # card -> token (reversible via map)
```
**Notes:** The four common pseudonymization techniques are **(a) encryption, (b) hashing, (c) masking, (d) tokenization** — in practice several may be combined, and **all rely on a secret** (L11 p.46). Because the salt/token map can reverse it, this is **pseudonymization, not anonymization** — keep the secret protected and remember accountability still applies (L11 p.44).

### Mask direct identifiers (and generalize quasi-identifiers)
**What:** Reproduce when asked to show masking — the generic, old-fashioned pseudonymization method — on a record (L11 p.47).
```python
# At MINIMUM, all DIRECT identifiers must be masked:
#   names, addresses, social security numbers, license plates,
#   IP addresses, device fingerprints, ...
def mask_name(name: str) -> str:
    first, _, last = name.partition(" ")
    return "**** " + last                      # "John Doe" -> "**** Doe"

# Quasi-identifiers (gender, date of birth, postal code, income, ...) are not
# direct IDs but can aid re-identification -> apply anonymization (e.g. generalize)
def generalize_postcode(pc: str) -> str:
    return pc[:2] + "***"                       # "8200" -> "82***"

print(mask_name("John Doe"))                    # **** Doe
print(generalize_postcode("8200"))             # 82***
```
**Notes:** Masking handles **direct identifiers**; quasi-identifiers need anonymization-style generalization because, combined, they can re-identify someone (L11 p.47). Masking alone is pseudonymization (mainly linkability) — it does not by itself defeat singling out or inference (L11 p.43).

### Achieve k-anonymity then fix it with l-diversity (before/after table)
**What:** Reproduce the worked k-anonymity / l-diversity example when asked to show the table transformation and why l-diversity is needed (L11 p.54–57).
```text
RAW (identifies individuals)               | ID    | Location    | X     | Condition
                                           | 1001  | Lystrup     | 41000 | Cardiovascular
                                           | 1002  | Solbjerg    | 38000 | Cancer
                                           | 1003  | Dragor      | 22000 | Cardiovascular
                                           | 1004  | Frederiksbg | 19000 | Cancer

STEP 1 - mask ID + re-code Location to city + bucket X (<30000 / >=30000)
=> 2-ANONYMITY (each quasi-identifier combo appears >= 2 times; re-id prob <= 1/k = 1/2)
   | ID | Location   | X       | Condition
   | ** | Aarhus     | >=30000 | Cardiovascular
   | ** | Aarhus     | >=30000 | Cancer
   | ** | Copenhagen | <30000  | Cardiovascular
   | ** | Copenhagen | <30000  | Cancer

PROBLEM (attribute disclosure): if EVERY Copenhagen/<30000 row had Condition=Cancer,
knowing someone's location would REVEAL their disease -> k-anonymity leaks it.

STEP 2 - enforce 2-DIVERSITY: each equivalence class must hold >= l distinct
sensitive values. Now each (Location,X) class contains BOTH conditions, so
location no longer reveals the condition (without extra background data).
```
**Notes:** **k-anonymity** = a subject cannot be distinguished from at least **k-1** others, so max re-identification probability is **1/k**; it targets **singling out** and is done via masking/re-coding (L11 p.53). It is **weak against linkability with background data** and against **attribute disclosure** — that is exactly what **l-diversity** (Machanavajjhala et al. 2007) fixes by requiring l distinct sensitive values per class (L11 p.55–57).

### Add randomization noise (Gaussian vs. Laplace) the way the lecture frames it
**What:** Reproduce when asked to write the noise-addition formula or a small randomization snippet (L11 p.58).
```python
import numpy as np

# Released value:  f'(x) = f(x) + g(x)   where g(.) is the secret noise
def gaussian_noise(x, sigma):
    return x + np.random.normal(0.0, sigma)     # f(x) + N(0, sigma^2)

def laplace_noise(x, lam):
    return x + np.random.laplace(0.0, lam)      # f(x) + L(0, lambda), lambda > 0

# COMMON MISTAKES that make reverse-engineering g(.) easy (L11 p.59):
#   - adding noise to only ONE / a few CORRELATED attributes
#   - INCONSISTENT or OUT-OF-BOUNDS noise
#   - assuming noise ALONE is enough (sparsity is a big issue)
#   - POORLY considering linkability (background distributions help the attacker)
```
**Notes:** Attacks try to **reverse-engineer f(.)** by deducing the secret noise g(.) and its parameters (L11 p.58). The lecture names **differential privacy** as today's *preferred* randomization-based technique but **does not cover it in detail** — don't over-claim depth on it (L11 p.59). Laplace uses scale/"diversity" parameter **lambda > 0**; Gaussian uses variance **sigma^2** (L11 p.58).

### Handle a data-subject-rights request (RD group)
**What:** Reproduce when asked how an engineer/operator fulfills an access/rectification/erasure/restriction/portability request (L11 p.61–67).
```text
0. Pragmatic check first: do you even need bespoke software? A small operator may
   satisfy RD MANUALLY or with a few scripts -- GDPR imposes NO specific SE reqs.
1. Identify which right (the engineering-relevant RD group = {R2,R3,R4,R6,R8}):
   R2 ACCESS       -> provide a view of the data; machine-readable where applicable
   R3 RECTIFICATION-> update the personal data (via consent/data center)
   R4 ERASURE      -> delete + LOG the request
   R6 RESTRICTION  -> place restriction; while restricted, data CANNOT be
                      simultaneously rectified or erased  (R6 -> NOT(R3 OR R4))
   R8 PORTABILITY  -> deliver a JSON/CSV dump on request (currently sufficient)
2. Overlap rule: if CONSENT was the basis and R5 (cancel consent) is exercised,
   FOLLOW UP WITH DELETION (R4) in most cases.
3. LOG initialization + fulfillment (supports Art. 30 record-keeping).
4. Backups: leave intact only if ROUND-ROBIN, so deletions propagate as old
   backups are deleted (immediate deletion from every backup not required).
```
**Notes:** The 10 rights split into **Informing RI={R1,R10}, Data RD={R2,R3,R4,R6,R8}, Lawfulness RL={R5,R7,R9}**; **RD is most relevant for engineering** (L11 p.62). Watch the logic traps: **R6 restriction blocks simultaneous R3/R4**, and **cancelling consent (R5) usually triggers erasure (R4)** (L11 p.62).

### Decide whether a DPIA is required (Article 35 trigger checklist)
**What:** Reproduce when asked when a Data Protection Impact Assessment is mandatory and what it involves (L11 p.73).
```text
[ ] TRIGGER: does the processing pose a HIGH RISK to natural persons?
        -> if YES, a DPIA is MANDATORY (Art. 35)
[ ] Treat data protection (and its security) as NON-FUNCTIONAL REQUIREMENTS
[ ] Use a RISK MATRIX: impact x probability (ENISA 2017)
[ ] Map controls (e.g. NIST families): authority/purpose, accountability/auditing,
    data quality, minimization/retention, participation/redress, security,
    transparency, use limitation
[ ] KEEP IT READY: must be DELIVERED TO REGULATORS in case of incidents
```
**Notes:** The DPIA is the GDPR's **risk-based approach** reaching into requirements engineering (L11 p.73). The accountability NIST control is roughly the DPIA itself (Art. 35), and ENISA's impact x probability risk matrix is the suggested scoring tool (L11 p.38).

### Run the breach-notification timeline (Articles 33 & 34)
**What:** Reproduce when asked what to do after detecting a personal-data breach, including the 72-hour clock (L11 p.75).
```text
T0   BECOME AWARE of the breach  <-- the 72h clock STARTS here (record this time)
     |
     v  (without undue delay)
[Art. 33] NOTIFY the SUPERVISORY AUTHORITY (DPA)
          "without undue delay and, where feasible, NOT LATER THAN 72 HOURS
           after having become aware of it"
     |
     +--> DPO coordinates with the DPA during the incident (Arts. 38-39)
     |
     v  assess severity using your PRIOR RISK ANALYSIS / DPIA
[Art. 34] If HIGH-RISK breach:
          ALSO COMMUNICATE to the AFFECTED NATURAL PERSONS, without further delay
          (no clear GDPR guidance on "high risk" -> rely on prior risk analysis)
```
**Notes:** Two common slips: the **72h is "where feasible"** and starts when the controller **becomes aware** (not at breach time); and a **high-risk** breach requires notifying the **affected individuals too (Art. 34)**, not just the DPA (L11 p.75). The DPO is not personally liable but coordinates with the DPA (L11 p.74).
