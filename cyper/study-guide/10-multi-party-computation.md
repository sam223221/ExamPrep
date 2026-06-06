# 10. Multi-Party Computation

> **Sources for this chapter:** `L10_MPCnote.pdf` (lecture slide deck, 49 slides — cited as `L10 p.N`) and `E10_MPC.pdf` (exercise sheet with full solutions, 4 pages — cited as `E10 p.N`).
>
> **Extraction note:** The lecture is a slide deck whose *technical derivations* (the XOR protocol, the AND/Beaver-triple protocol, the per-server share computation, and the reconstruction check) were written **by hand on the slides** (L10 p.27–34). The text layer of those handwritten pages OCR's to garbled fragments and cannot be read reliably from the PDF. Fortunately the **same protocols are written out cleanly and completely in the exercise solutions** (E10 p.3–4), so the worked math below is grounded in E10 and cross-referenced to the lecture's conceptual slides. Where a detail appears only as handwriting that could not be recovered, this is flagged explicitly rather than guessed.

---

## Overview — what this topic covers and why it matters

**Secure Multi-Party Computation (MPC)** is the field of cryptography that lets several mutually distrusting parties jointly compute a function of their private inputs while learning **nothing beyond the agreed output** — in particular, no party learns another party's input (L10 p.1, p.35). The lecture motivates this with three running examples: two people who want to know **who earns more without revealing their salaries** (L10 p.3), two people who want to know whether they **mutually like each other without revealing their individual preferences** (L10 p.4), and a hospital and police force who want to know whether **a suspect is hospitalized without either revealing its whole list** (private set intersection) (L10 p.5–6). The unifying claim is that **any function can be computed** under MPC — comparison `x > y`, AND `a ∧ b`, set intersection `X ∩ Y`, average `(x₁+…+xₙ)/n`, winner determination `argmax(s₁,…,sₙ)`, and even ML activations like `ReLU(x) = max(0,x)` (L10 p.7).

This chapter focuses on the concrete two-party building blocks the lecture actually works through: **Boolean (XOR) secret sharing**, the **secure XOR protocol** (which needs no communication), and the **secure AND protocol** built from a **Beaver (multiplication) triple** (L10 p.26–39; E10 p.1–4). It also covers the **security model** (semi-honest / "honest-but-curious," and the principle that leakage implied by the output itself is unavoidable and allowed), the **historical milestones** (Shamir 1979, Yao's millionaires' problem 1982, GMW 1987), the **MPC-as-a-service** deployment picture, and the **real-world standardization and industry** context (NIST threshold cryptography; Partisia, Zama, Curv, Unbound) (L10 p.9, p.13–17, p.41–49). MPC matters because it is "the backbone of modern secure computation systems" and is being deployed in the real world for health-care analysis, fault detection, genome matching, voting, and auctions (L10 p.17, p.48–49).

---

## Key Concepts

### Secure Multi-Party Computation (MPC)

**What:** A protocol that lets parties `P₁,…,Pₙ`, each holding a private input, jointly compute `f(input₁,…,inputₙ)` so that everyone learns the output but **nobody learns anything more than the result** (L10 p.35). **Two-party computation (2PC)** is the special case `n = 2` (L10 p.24).

**Why:** Many valuable computations require combining data that the data owners are unwilling or legally unable to share in the clear — salaries, romantic preferences, patient lists, exam scores, ML model inputs (L10 p.3–7, p.14). MPC removes the need for a trusted party to see the raw data.

**How (high level):** Inputs are **secret-shared** among the computing parties (or among servers), the function is evaluated on the shares using local operations plus a small amount of communication, and only the final shares are recombined to reveal the output (L10 p.14, p.27–34). The lecture's worked instance is computing `a ∧ b` (mutual liking) between two servers (L10 p.18–35).

**Key security principle:** MPC's security definition only guarantees that **nobody learns anything more than the result** — any information that is *logically implied by the output* is not a violation. Example: if the public result is `a ∧ b = 0` and Bob knows his own input `b = 1`, he can deduce `a = 0` (Alice does not like him). "Even in multi-party computation, this is inevitable" (L10 p.35; E10 p.4 Sol.4c).

### The Millionaires' Problem (Yao, 1982)

**What:** The original motivating problem for 2PC: two millionaires want to learn **which of them is richer (`x > y`) without revealing their actual wealth** (L10 p.9). This is exactly the lecture's "salary comparison" motivation (L10 p.3).

**Why:** It is the canonical example showing a useful joint computation (a comparison) that both parties want, yet neither is willing to expose the input. It launched the field of secure two-party computation (L10 p.9).

**How:** Introduced by **Andrew Yao in 1982** as 2PC for the comparison function; in **1986 Yao generalized it to general functions/circuits** (the basis of what is now called **garbled circuits**, named after Yao) (L10 p.9). *Note: the lecture lists garbled circuits only via this historical reference to Yao's general-circuit 2PC (L10 p.9); it does not give a step-by-step garbled-circuit construction. The construction the lecture actually details is the secret-sharing + Beaver-triple approach, not garbling.*

### History / Milestones of MPC

**What & when** (L10 p.9):
- **1979 — Shamir Secret Sharing** (Adi Shamir).
- **1982 — Millionaires' problem, 2PC** by Andrew Yao.
- **1986 — General functions / circuit 2PC** by Yao (the garbled-circuit idea).
- **1987 — Multi-party computation** (general `n`-party) by **Goldreich, Micali, Wigderson (GMW)**.

**Why it matters for the exam:** The progression is *secret sharing → two-party comparison → two-party general circuits → multi-party general computation*. Denmark/Aarhus is a hub: **Ivan Damgård** (Aarhus, IACR Fellow) and the broader Danish MPC community are highlighted (L10 p.10–11). **Lars Knudsen** (SDU Sønderborg, IACR Fellow) is also featured (L10 p.12).

### Secret Sharing (general idea)

**What:** A secret value is split into **shares** distributed among parties such that the shares *together* reconstruct the secret, but **no single share (or insufficient subset) reveals anything** about it (L10 p.37; E10 p.3 Sol.1).

**Why:** Secret sharing is the data representation that makes MPC possible — parties compute on shares, never on plaintext inputs (L10 p.36–37).

**How — the two forms the lecture uses:**
- **Boolean / XOR sharing** of a bit: `a = a₁ ⊕ a₂` (L10 p.37; E10 p.1). Makes **XOR free** (no communication).
- **Additive sharing** over integers: `x = x₁ + x₂`, used "for more complicated arithmetic functions" and secure ML (L10 p.41).

### Shamir Secret Sharing (1979)

**What:** A `(t, n)` threshold secret-sharing scheme due to Adi Shamir (L10 p.9). The secret is the value of a degree-`(t−1)` polynomial at `0`; each of the `n` parties gets one point on the polynomial. Any `t` points reconstruct the polynomial (and hence the secret) via interpolation; any `t−1` points reveal nothing.

**Why:** Historically the first secret-sharing scheme and the foundation of threshold cryptography and many MPC protocols (L10 p.9). It is the named "1979 Shamir Secret Sharing" milestone.

**How:** *The lecture names Shamir Secret Sharing as the 1979 milestone (L10 p.9) but does not include the polynomial construction on the readable slides; the two-party scheme the lecture develops in detail is the simpler XOR/additive sharing above.* A self-contained worked example of Shamir sharing (using small numbers) is given in the **How-To Cookbook** below, clearly marked as standard scheme background rather than lecture-specific content.

### Boolean Secret Sharing (XOR sharing)

**What:** A secret bit `a ∈ {0,1}` is represented as `a = a₁ ⊕ a₂`; `a₁` and `a₂` are the **shares** of `a` (L10 p.37; E10 p.1). Likewise `b = b₁ ⊕ b₂`. Alice holds `a₁, b₁`; Bob holds `a₂, b₂` (E10 p.1 Ex.2).

**Why secure:** Each share is **uniformly random in {0,1}**, so a single share gives `Pr[a = 0 | a₁] = Pr[a = 1 | a₁] = ½` — observing one share leaks **no information** about `a` (E10 p.3 Sol.1b).

**How to share:** Pick `a₁ ← {0,1}` uniformly at random, then set `a₂ = a ⊕ a₁`. For `a = 1`, valid pairs include `(a₁,a₂) = (0,1)` or `(1,0)` since `0⊕1 = 1⊕0 = 1` (E10 p.3 Sol.1a).

**How to reconstruct:** The two parties exchange their shares and compute `a = a₁ ⊕ a₂` (E10 p.3 Sol.1c).

### Secure XOR Protocol (XOR is "free")

**What:** Computing a sharing of `a ⊕ b` from sharings of `a` and `b` (L10 p.26–28; E10 p.1 Ex.2a).

**Why important:** XOR (addition mod 2) requires **no communication at all** — each party just XORs its own shares locally. This is why "Boolean sharing makes XOR trivial" (L10 p.49) and why circuits are designed to use as few AND gates as possible.

**How (the local rule):** Each party computes its share of `a ⊕ b` from the shares it already holds:
- Alice: `(a ⊕ b)₁ = a₁ ⊕ b₁`
- Bob: `(a ⊕ b)₂ = a₂ ⊕ b₂`

Then `(a⊕b)₁ ⊕ (a⊕b)₂ = (a₁⊕b₁) ⊕ (a₂⊕b₂) = (a₁⊕a₂) ⊕ (b₁⊕b₂) = a ⊕ b` (E10 p.3 Sol.2a). **No messages are exchanged.** (The lecture's handwritten XOR slides on L10 p.27–28 develop the same protocol with random masks for the input-sharing/reconstruction steps, but that handwriting does not extract cleanly.)

### Why AND Needs Communication

**What:** Unlike XOR, computing a sharing of `a ∧ b` (AND = multiplication mod 2) **cannot** be done with purely local operations (L10 p.29–34; E10 p.1 Ex.2c).

**Why:** Expanding the product exposes **cross terms** that mix shares held by different parties:
```
(a₁ ⊕ a₂) ∧ (b₁ ⊕ b₂) = (a₁∧b₁) ⊕ (a₁∧b₂) ⊕ (a₂∧b₁) ⊕ (a₂∧b₂)
```
The terms `a₁∧b₂` and `a₂∧b₁` each combine one of Alice's secret values with one of Bob's. Neither party can compute these alone, so **communication is required** (E10 p.3 Sol.2b–2c). This is the fundamental reason AND/multiplication gates are the "expensive" gates in MPC.

### Beaver Triple (Multiplication Triple)

**What:** A precomputed triple of secret-shared random bits `(i, j, k)` with the property `k = i ∧ j` (L10 p.31, p.37–39; E10 p.1 Ex.3). The lecture also calls it a **"multiplication triple"** (L10 p.31).

**Why:** It is the resource that makes secure AND/multiplication efficient. The expensive, correlated randomness (`k = i ∧ j`) is generated **offline, in a preprocessing phase**, *independent of the actual inputs*. Then the **online phase** (once the real inputs arrive) is cheap — just masking, opening two values, and local XORs. "Beaver triples enable efficient AND/multiplication" (L10 p.49).

**Why offline:** Producing triples is **expensive**; separating preprocessing from the online phase "allows efficient secure computation during execution" (E10 p.4 Sol.5b; L10 p.39).

**How it's used:** See the secure AND protocol below and the **How-To Cookbook**.

### Secure AND Protocol (using a Beaver Triple)

**What:** Computing a sharing of `c = a ∧ b` from sharings of `a`, `b` and a Beaver triple `(i, j, k = i ∧ j)`, all Boolean and XOR secret-shared (L10 p.30–34; E10 p.1 Ex.3).

**How — the masked values:** Define and **open (reveal)**:
```
d = a ⊕ i        e = b ⊕ j
```
Revealing `d` and `e` is safe because `i, j` are **uniformly random bits** that mask `a, b`. Hence `d` and `e` are statistically independent of `a, b` and **leak nothing** about the inputs (E10 p.3 Sol.3a, p.4 Sol.5a; L10 p.39).

**How — the identity (the heart of the protocol):**
```
a ∧ b = (d ⊕ i) ∧ (e ⊕ j)
      = (d∧e) ⊕ (d∧j) ⊕ (e∧i) ⊕ (i∧j)
      = k ⊕ (d∧j) ⊕ (e∧i) ⊕ (d∧e)          [since k = i ∧ j]
```
(E10 p.3 Sol.3b.)

After `d` and `e` are public, every remaining term is something the parties can produce as a **sharing using only local operations**, because `d, e` are public constants and each party holds its own shares of `i, j, k`:
- `k` is already shared (from preprocessing).
- `d∧j` and `e∧i` are a *public bit ANDed with a shared bit* → each party just ANDs the public bit into its own share (local).
- `d∧e` is a *public constant*.

**How — handling the public constant `d∧e`:** A public constant must be added to the shared value **exactly once** (so it survives the final XOR-reconstruction). In the lecture/exercise convention, **only Bob adds `(d∧e)` to his share** (E10 p.1 Ex.3c). This asymmetric assignment is correct because Boolean secret sharing only requires that the **XOR of both shares** equals the true value — it does not matter *which* party holds which piece, as long as the total XORs to `c = a ∧ b` (E10 p.3 Sol.3c). If *both* parties added `d∧e`, it would XOR to `0` and cancel — a classic bug.

*(The lecture's handwritten slides L10 p.31–34 derive the per-server shares `c_A` and `c_B` and verify `c_A ⊕ c_B = a ∧ b` by direct expansion; the handwriting does not OCR cleanly, but the clean version is exactly the E10 derivation above.)*

### Security Model: Honest-but-Curious (Semi-Honest) vs Malicious

**What:** The two standard adversary models for MPC.
- **Honest-but-curious / semi-honest:** Corrupted parties **follow the protocol exactly** but try to **learn extra information** from the messages they see. The protocols in this lecture (XOR, AND-with-Beaver-triple) are presented in this setting — security rests on the messages being uniformly masked so they reveal nothing (E10 p.3–4 Sol.3a, Sol.5a; L10 p.39).
- **Malicious / active:** Corrupted parties may **deviate arbitrarily** from the protocol (send wrong values, abort, etc.). Defending against this requires additional machinery (e.g., MACs). *The lecture mentions "Message Authentication Code (MAC) by MPC" as an application/extension (L10 p.41) but does not develop a full malicious-secure protocol on the readable slides.*

**Why the masking gives security here:** In the AND protocol, the only values revealed are `d = a⊕i` and `e = b⊕j`. Because `i, j` are uniformly random and unknown to the other party, they **perfectly mask** `a` and `b` — so a curious party gains nothing (E10 p.4 Sol.5a). This is precisely the semi-honest guarantee.

**What security does NOT hide:** Anything implied by the output. `a∧b = 0` plus `b = 1` ⇒ `a = 0`. This leakage is "inherent and allowed" (E10 p.4 Sol.4c; L10 p.35).

### MPC as a Service

**What:** A deployment pattern where **clients** send *shares/encrypted inputs* to a set of **computing servers**; the servers run the MPC protocol and return *shares/encrypted results*; only the client recombines to get the plaintext result (L10 p.13–17).

**Why needed:** A service provider may **not want to store** clients' sensitive info (liability), and clients **do not want to send** their data in plaintext (privacy). MPC lets the computation happen on protected data: "encrypted input → encrypted function → encrypted result," and the provider never sees plaintext (L10 p.14–17). Example given: **PDTE — Private Decision Tree Evaluation**, where a tree owner has a model, clients have queries, and computing servers evaluate the tree on shared inputs returning a shared result (L10 p.14).

**Applications listed:** Health-care analysis, fault detection, NLP / pattern matching, genome matching, random forest, and more (L10 p.17).

### Standardization and Real-World MPC

**What & why:** Just as encryption schemes are standardized (e.g., **AES — FIPS PUB 197, FIPS-approved 2002**, selected from 15 submissions, 5 finalists; runner-up **Serpent** by Anderson, Biham, and **Knudsen**) (L10 p.43), MPC is now undergoing standardization via **NIST's Multi-Party Threshold Cryptography** project (L10 p.45–46). The 1st round had **26 "Preview Writeup" submissions**, with **3 rounds** planned (L10 p.46).

**Why standardization matters** (L10 p.44): **Interoperability** (different vendors' implementations must work together), **security assurance** (public expert review reduces hidden weaknesses), **deployment at scale** (regulation, certification, procurement require standardized crypto), and **longevity** (a standardized algorithm like AES can be used worldwide for decades).

**Industry (L10 p.48):** **Partisia** (MPC platform — data sharing, voting, auctions; Aarhus), **Zama** (privacy-preserving computation using MPC and FHE; confidential cloud/AI), **Curv** (MPC-based private-key management, acquired by PayPal), **Unbound Security** (MPC-based key protection, acquired by Coinbase).

### Other Applications of Secret Sharing (Additive Sharing)

**What:** Beyond Boolean bits, values can be **additively shared** as `x = x₁ + x₂` over the integers for "more complicated arithmetic functions" (L10 p.41).

**Why:** Additive sharing is "useful for secure machine learning" and underlies MPC versions of larger cryptographic primitives: **AES by MPC, hash functions by MPC, MAC by MPC, and many more cryptographic functions by MPC** (L10 p.41). It also supports the function zoo on L10 p.7 (averages, argmax, ReLU).

---

## Glossary

- **MPC (Secure Multi-Party Computation)** — protocol letting `n` mutually distrusting parties compute `f` of their private inputs, revealing only the output and nothing more (L10 p.1, p.35).
- **2PC (Two-Party Computation)** — MPC with `n = 2`; the lecture's worked setting (e.g., two servers computing `a ∧ b`) (L10 p.24).
- **Millionaires' problem** — Yao's 1982 problem: learn who is richer (`x > y`) without revealing wealth; origin of 2PC (L10 p.9, p.3).
- **Garbled circuits** — Yao's 1986 technique for general-function 2PC; named in the lecture's history only (L10 p.9). No step-by-step construction is given in the readable lecture.
- **GMW (Goldreich–Micali–Wigderson, 1987)** — first general multi-party (n-party) computation (L10 p.9).
- **Secret sharing** — splitting a secret into shares that jointly reconstruct it but individually reveal nothing (L10 p.37; E10 p.3).
- **Share** — one piece of a secret-sharing; e.g., `a₁`, `a₂` are the shares of `a` where `a = a₁ ⊕ a₂` (L10 p.37; E10 p.1).
- **Boolean / XOR secret sharing** — sharing a bit as `a = a₁ ⊕ a₂` (E10 p.1).
- **Additive secret sharing** — sharing an integer as `x = x₁ + x₂` for arithmetic functions (L10 p.41).
- **Shamir Secret Sharing (1979)** — polynomial-based `(t, n)` threshold secret sharing by Adi Shamir (L10 p.9).
- **Reconstruction (opening)** — parties exchange shares and recombine, e.g., `a = a₁ ⊕ a₂` (E10 p.3 Sol.1c).
- **Secure XOR protocol** — compute a sharing of `a ⊕ b` with **no communication**, each party XORing its own shares (E10 p.3 Sol.2a; L10 p.26–28).
- **Secure AND protocol** — compute a sharing of `a ∧ b`; requires communication and a Beaver triple (L10 p.29–34; E10 p.1 Ex.3).
- **Cross terms** — the mixed products `a₁∧b₂`, `a₂∧b₁` in the AND expansion that force communication (E10 p.3 Sol.2b).
- **Beaver triple / multiplication triple** — shared random `(i, j, k)` with `k = i ∧ j`, used to evaluate AND/multiplication (L10 p.31, p.37–39; E10 p.1 Ex.3).
- **Masked values** `d, e` — `d = a ⊕ i`, `e = b ⊕ j`; opened during the AND protocol, leak nothing because `i, j` are random (E10 p.1 Ex.3a; p.3 Sol.3a).
- **Preprocessing / offline phase** — input-independent phase that generates Beaver triples (expensive) (L10 p.39; E10 p.4 Sol.5b).
- **Online phase** — input-dependent phase that uses the triples for cheap secure computation (L10 p.39).
- **Honest-but-curious / semi-honest** — adversary follows the protocol but tries to learn extra info; the model these protocols target (E10 p.3–4).
- **Malicious / active adversary** — adversary may deviate arbitrarily; needs extra protection (e.g., MACs) (context from L10 p.41).
- **Trusted Third Party (TTP)** — an ideal party that could compute `a ∧ b` and just return the result; MPC's goal is to *emulate* the TTP without anyone playing it (L10 p.23, handwritten "Trusted Third Party Setting (TTP)").
- **MPC as a Service** — clients submit shares/encrypted inputs to computing servers that run MPC and return shares/encrypted results (L10 p.13–17).
- **PDTE (Private Decision Tree Evaluation)** — example MPC service: evaluating a decision tree on a client's private query (L10 p.14).
- **NIST Multi-Party Threshold Cryptography** — NIST standardization project for threshold/MPC schemes; 1st round had 26 submissions, 3 rounds planned (L10 p.45–46).
- **Inherent/output leakage** — information implied by the output itself (e.g., deducing the other input from the result); allowed by MPC's definition (L10 p.35; E10 p.4 Sol.4c).

---

## How-To Cookbook

### Recipe A — Create a Boolean (XOR) secret sharing of a bit

**Goal:** Share a secret bit `a` between Alice and Bob so neither alone learns it.

1. Choose `a₁ ← {0,1}` uniformly at random (this is Alice's share).
2. Compute Bob's share: `a₂ = a ⊕ a₁`.
3. Give `a₁` to Alice, `a₂` to Bob.

**Worked example — share `a = 1`:**
- Flip a coin → say `a₁ = 0`. Then `a₂ = 1 ⊕ 0 = 1`. Shares `(a₁,a₂) = (0,1)`.
- Different coin → `a₁ = 1`. Then `a₂ = 1 ⊕ 1 = 0`. Shares `(1,0)`.
- Check: `0⊕1 = 1` ✓ and `1⊕0 = 1` ✓ (E10 p.3 Sol.1a).
- Either share alone is a fair coin → `Pr[a=0│share] = Pr[a=1│share] = ½` → zero leakage (E10 p.3 Sol.1b).

**Reconstruct:** Alice and Bob exchange shares; both compute `a = a₁ ⊕ a₂` (E10 p.3 Sol.1c).

### Recipe B — Secure XOR (no communication)

**Goal:** From shares of `a` and `b`, get shares of `a ⊕ b`.

Setup: Alice holds `a₁, b₁`; Bob holds `a₂, b₂` (E10 p.1 Ex.2).

1. Alice computes locally: `(a⊕b)₁ = a₁ ⊕ b₁`.
2. Bob computes locally: `(a⊕b)₂ = a₂ ⊕ b₂`.
3. Done — **no messages sent.**

**Worked example:** Let `a = 1` shared as `(a₁,a₂) = (1,0)`, and `b = 1` shared as `(b₁,b₂) = (0,1)`.
- Alice: `(a⊕b)₁ = 1 ⊕ 0 = 1`.
- Bob: `(a⊕b)₂ = 0 ⊕ 1 = 1`.
- Reconstruct: `1 ⊕ 1 = 0`. And indeed `a ⊕ b = 1 ⊕ 1 = 0` ✓ (E10 p.3 Sol.2a).

### Recipe C — Why you CANNOT do AND locally (the cross-term check)

Expand the product of the two shared bits:
```
a ∧ b = (a₁ ⊕ a₂) ∧ (b₁ ⊕ b₂)
      = (a₁∧b₁) ⊕ (a₁∧b₂) ⊕ (a₂∧b₁) ⊕ (a₂∧b₂)
```
- `a₁∧b₁` — Alice can compute (both hers).
- `a₂∧b₂` — Bob can compute (both his).
- `a₁∧b₂` and `a₂∧b₁` — **mix one value from each party** → neither can compute alone → **communication required** (E10 p.3 Sol.2b–2c).

### Recipe D — Secure AND with a Beaver triple (full procedure)

**Preprocessing (offline, input-independent):**
1. Generate uniformly random bits `i, j ← {0,1}` and set `k = i ∧ j`.
2. Boolean-secret-share each of `i, j, k` between Alice and Bob. (Expensive — done offline, before inputs are known) (L10 p.39; E10 p.4 Sol.5b).

**Online (once inputs `a, b` are shared):**
3. Each party locally forms its share of `d = a ⊕ i` and `e = b ⊕ j` (this is a free XOR, Recipe B).
4. **Open** `d` and `e` (each party reveals its `d`- and `e`-shares; both reconstruct the public bits `d`, `e`). Safe: `i, j` random ⇒ `d, e` leak nothing about `a, b` (E10 p.3 Sol.3a).
5. Each party computes its share of `c = a ∧ b` using the identity
   ```
   a ∧ b = k ⊕ (d∧j) ⊕ (e∧i) ⊕ (d∧e)
   ```
   - `k`: use your existing share of `k`.
   - `d∧j`: AND the **public** bit `d` into your share of `j`.
   - `e∧i`: AND the **public** bit `e` into your share of `i`.
   - `d∧e`: a **public constant** — add it to **exactly one** party's share. By convention **only Bob** adds `(d∧e)` (E10 p.1 Ex.3c; p.3 Sol.3b–3c).
6. The two `c`-shares now XOR to `c = a ∧ b`. Open them only if the output is meant to be revealed.

**Worked example — `a = 0`, `b = 1` (Alice doesn't like Bob; Bob likes Alice), so the true answer is `a ∧ b = 0`:**

Pick a triple: `i = 1`, `j = 0` → `k = i∧j = 1∧0 = 0`.
- Masked values: `d = a ⊕ i = 0 ⊕ 1 = 1`; `e = b ⊕ j = 1 ⊕ 0 = 1`. Open `d = 1`, `e = 1`.
- Plug into the identity:
  ```
  k ⊕ (d∧j) ⊕ (e∧i) ⊕ (d∧e)
  = 0 ⊕ (1∧0) ⊕ (1∧1) ⊕ (1∧1)
  = 0 ⊕ 0 ⊕ 1 ⊕ 1
  = 0
  ```
- Result `= 0 = a ∧ b` ✓ (matches E10 p.3 Sol.3b's identity).

**Second worked example — `a = 1`, `b = 1` (mutual liking), true answer `a ∧ b = 1`:**

Pick a triple: `i = 0`, `j = 1` → `k = 0∧1 = 0`.
- `d = a ⊕ i = 1 ⊕ 0 = 1`; `e = b ⊕ j = 1 ⊕ 1 = 0`. Open `d = 1`, `e = 0`.
- Identity: `k ⊕ (d∧j) ⊕ (e∧i) ⊕ (d∧e) = 0 ⊕ (1∧1) ⊕ (0∧0) ⊕ (1∧0) = 0 ⊕ 1 ⊕ 0 ⊕ 0 = 1`.
- Result `= 1 = a ∧ b` ✓.

### Recipe E — Why "only Bob adds `d∧e`" is correct (and what breaks otherwise)

Boolean sharing only requires **`share_Alice ⊕ share_Bob = true value`**. A public constant `d∧e` must be injected into the *total* exactly once:
- **Only Bob adds it** → total includes `d∧e` once → correct (E10 p.3 Sol.3c).
- **Both add it** → it appears twice → `(d∧e) ⊕ (d∧e) = 0` → it cancels → **wrong result** (common bug; follows from XOR self-cancellation).
- **Neither adds it** → missing term → wrong result.

The choice of *which* party adds it is arbitrary; Bob is just the convention here (E10 p.1 Ex.3c).

### Recipe F — Secure "do they like each other?" (matching) end-to-end

**Function:** mutual liking `= a ∧ b` (Alice's preference `a`, Bob's preference `b`) (E10 p.4 Sol.4a; L10 p.18).
1. Alice secret-shares `a`; Bob secret-shares `b` (Recipe A).
2. Run the secure AND protocol with a Beaver triple (Recipe D) to get a sharing of `a ∧ b` (E10 p.4 Sol.4b).
3. Open the result. If `1` → mutual liking; if `0` → not mutual.
4. **Leakage note:** if the result is `0` and Bob knows `b = 1`, Bob learns `a = 0`. This is inherent and allowed by MPC's definition (E10 p.4 Sol.4c; L10 p.35).

### Recipe G — Shamir Secret Sharing with small numbers (standard-scheme background)

> **Source note:** The lecture *names* Shamir Secret Sharing as the 1979 milestone (L10 p.9) but the polynomial construction is **not** on the readable lecture slides. The following is the standard textbook scheme included for completeness; treat it as background, not as lecture-quoted content.

**Goal:** A `(t, n) = (2, 3)` sharing of secret `s = 5` over `GF(7)` (work mod 7).

1. Secret is `f(0) = s = 5`. For threshold `t = 2`, use a degree-`1` polynomial `f(x) = s + c·x` with random `c`. Pick `c = 3`: `f(x) = 5 + 3x (mod 7)`.
2. Hand each party a point:
   - Party 1: `f(1) = 5 + 3 = 8 ≡ 1`.
   - Party 2: `f(2) = 5 + 6 = 11 ≡ 4`.
   - Party 3: `f(3) = 5 + 9 = 14 ≡ 0`.
3. **Reconstruct from any 2 points** by Lagrange interpolation at `x = 0`. Using parties 1 and 2, `(1,1)` and `(2,4)`:
   ```
   s = f(0) = 1·(0−2)/(1−2) + 4·(0−1)/(2−1)  (mod 7)
            = 1·(−2)/(−1) + 4·(−1)/(1)
            = 1·2 + 4·(−1) = 2 − 4 = −2 ≡ 5 (mod 7) ✓
   ```
4. **Security:** any single point lies on infinitely many lines, so one share alone reveals nothing about `s` — matching the general secret-sharing guarantee (L10 p.37).

---

## Exam-Style Q&A

**Q1. State, in one sentence, the security guarantee of MPC, and give the one kind of information it does NOT hide.**
**A.** MPC guarantees that no party learns anything beyond the agreed output of the function (L10 p.35). It does **not** hide information that is logically implied by the output itself — e.g., if `a ∧ b = 0` is revealed and Bob knows `b = 1`, he deduces `a = 0`; this output-induced leakage is inherent and allowed (E10 p.4 Sol.4c; L10 p.35).

**Q2. Give three real-world motivations for MPC from the lecture and the function each computes.**
**A.** (1) **Salary/wealth comparison** — learn who earns more without revealing salaries, function `x > y` (L10 p.3, p.7; the millionaires' problem, p.9). (2) **Matching** — learn whether two people like each other without revealing preferences, function `a ∧ b` (L10 p.4, p.7). (3) **Private set intersection** — hospital and police learn whether a suspect is hospitalized without revealing their full lists, function `X ∩ Y` (L10 p.5–6, p.7). (Others on L10 p.7: average `(x₁+…+xₙ)/n`, winner `argmax`, `ReLU` for ML.)

**Q3. In Boolean secret sharing `a = a₁ ⊕ a₂`, why does holding only `a₁` reveal nothing about `a`? How do the parties reconstruct `a`?**
**A.** Each share is uniformly random in `{0,1}`, so `Pr[a=0│a₁] = Pr[a=1│a₁] = ½` — a single share is independent of `a` and leaks nothing (E10 p.3 Sol.1b). Reconstruction: the parties exchange shares and compute `a = a₁ ⊕ a₂` (E10 p.3 Sol.1c).

**Q4. Show that two parties can compute a sharing of `a ⊕ b` with no communication.**
**A.** Alice holds `a₁,b₁`, Bob holds `a₂,b₂`. Each computes locally: `(a⊕b)₁ = a₁⊕b₁`, `(a⊕b)₂ = a₂⊕b₂`. Then `(a⊕b)₁ ⊕ (a⊕b)₂ = (a₁⊕a₂)⊕(b₁⊕b₂) = a⊕b`. No messages are exchanged, so XOR is "free" (E10 p.3 Sol.2a; L10 p.49).

**Q5. Expand `(a₁ ⊕ a₂) ∧ (b₁ ⊕ b₂)` and explain why AND requires communication.**
**A.** `(a₁⊕a₂)∧(b₁⊕b₂) = (a₁∧b₁) ⊕ (a₁∧b₂) ⊕ (a₂∧b₁) ⊕ (a₂∧b₂)` (E10 p.3 Sol.2b). The cross terms `a₁∧b₂` and `a₂∧b₁` each combine a value held by Alice with a value held by Bob; neither party can compute them alone, so communication is required (E10 p.3 Sol.2c).

**Q6. Define a Beaver triple and prove the AND identity `a∧b = k ⊕ (d∧j) ⊕ (e∧i) ⊕ (d∧e)`.**
**A.** A Beaver (multiplication) triple is shared random bits `(i,j,k)` with `k = i∧j` (L10 p.31; E10 p.1). With `d = a⊕i`, `e = b⊕j`, so `a = d⊕i` and `b = e⊕j`:
```
a∧b = (d⊕i)∧(e⊕j)
    = (d∧e) ⊕ (d∧j) ⊕ (e∧i) ⊕ (i∧j)
    = k ⊕ (d∧j) ⊕ (e∧i) ⊕ (d∧e),  since k = i∧j.
```
(E10 p.3 Sol.3b.)

**Q7. Why is it safe to reveal `d = a⊕i` and `e = b⊕j` during the AND protocol?**
**A.** Because `i` and `j` are uniformly random bits, unknown to the other party. They perfectly mask `a` and `b`, so `d` and `e` are statistically independent of the inputs and reveal nothing about `a` or `b` (E10 p.3 Sol.3a, p.4 Sol.5a).

**Q8. In the AND protocol only Bob adds the public term `(d∧e)` to his share. Why is the result still a correct sharing of `c`? What would go wrong if both parties added it?**
**A.** Boolean sharing only requires that the XOR of the two shares equals the true value; it doesn't matter which party holds which piece, so injecting the public constant into one share (Bob's) makes the total correct (E10 p.3 Sol.3c). If both added it, `(d∧e)⊕(d∧e) = 0` would cancel and the result would be wrong; if neither added it, the term would be missing — also wrong.

**Q9. Why are Beaver triples generated in an offline preprocessing phase?**
**A.** Producing triples is expensive. Generating them offline (before inputs are known) lets the online phase — once real inputs arrive — be cheap (only masking, opening two bits, and local XORs), enabling efficient secure computation during execution (E10 p.4 Sol.5b; L10 p.39).

**Q10. Distinguish honest-but-curious from malicious adversaries. Which model do the lecture's protocols target, and on what does their security rest?**
**A.** Honest-but-curious (semi-honest) adversaries follow the protocol but try to learn extra info from the messages; malicious adversaries deviate arbitrarily. The XOR and Beaver-triple AND protocols are presented for the semi-honest model: security rests on every revealed value (`d`, `e`) being uniformly masked by random `i, j`, so a curious party learns nothing beyond the output (E10 p.3–4 Sol.3a, Sol.5a). Malicious security needs extra tools such as MACs (cf. L10 p.41).

**Q11. Give the historical milestones of MPC with years and names.**
**A.** 1979 Shamir Secret Sharing (Adi Shamir); 1982 millionaires' problem / 2PC (Andrew Yao); 1986 general-function/circuit 2PC, i.e., garbled circuits (Yao); 1987 general multi-party computation (Goldreich, Micali, Wigderson — GMW) (L10 p.9).

**Q12. What is "MPC as a Service" and why is it needed?**
**A.** Clients send shares/encrypted inputs to computing servers, which run the MPC protocol and return shares/encrypted results that only the client can recombine (L10 p.13–17). It is needed because service providers often don't want the liability of storing sensitive data and clients don't want to send data in plaintext; MPC lets useful computation (e.g., Private Decision Tree Evaluation, health-care analysis, genome matching) run without exposing plaintext (L10 p.14, p.17).

**Q13. Why does standardization matter for cryptography/MPC, and what is NIST doing for MPC?**
**A.** Standardization gives interoperability across vendors, security assurance via public expert review, deployment at scale (regulation/certification/procurement), and longevity (an algorithm like AES can be used for decades) (L10 p.44). For MPC, NIST runs the **Multi-Party Threshold Cryptography** project; its 1st round had 26 "Preview Writeup" submissions, with 3 rounds planned (L10 p.45–46).

**Q14. Walk through computing `a∧b` for `a = 1, b = 0` using a Beaver triple `i = 1, j = 1` (so `k = 1`). Verify the answer.**
**A.** `d = a⊕i = 1⊕1 = 0`; `e = b⊕j = 0⊕1 = 1`. Open `d = 0, e = 1`. Then `k ⊕ (d∧j) ⊕ (e∧i) ⊕ (d∧e) = 1 ⊕ (0∧1) ⊕ (1∧1) ⊕ (0∧1) = 1 ⊕ 0 ⊕ 1 ⊕ 0 = 0`. The true value `a∧b = 1∧0 = 0` ✓ (identity from E10 p.3 Sol.3b).

**Q15. Name two MPC-related companies from the lecture and what they do.**
**A.** Any two of: **Partisia** — MPC platform for data sharing, voting, auctions (Aarhus); **Zama** — privacy-preserving computation using MPC and FHE for confidential cloud/AI; **Curv** — MPC-based private-key management (acquired by PayPal); **Unbound Security** — MPC-based cryptographic key protection (acquired by Coinbase) (L10 p.48).

**Q16. What does the secure AND protocol let two people compute privately in the "matching" scenario, and what residual leakage is unavoidable?**
**A.** It computes mutual liking `a ∧ b` without either revealing their own preference (E10 p.4 Sol.4a–4b; L10 p.18). Unavoidable leakage: if the result is `0` and one party knows their own input is `1`, they deduce the other's input is `0` — MPC only hides information beyond the result (E10 p.4 Sol.4c; L10 p.35).

---

## Gotchas

- **XOR is free; AND is not.** A very common exam point: XOR needs zero communication (local share XOR), while AND needs communication and a Beaver triple. Designing circuits to minimize AND gates is the whole reason this distinction matters (E10 p.3 Sol.2; L10 p.49).
- **The `d∧e` public constant must be added exactly once.** Adding it on both shares cancels it (`x⊕x = 0`); adding it on neither drops it. Convention: only Bob adds it (E10 p.1 Ex.3c, p.3 Sol.3c).
- **MPC does not hide output-implied information.** Don't claim MPC keeps inputs "fully secret." If your input plus the public output determines the other's input, that's allowed leakage, not a break (`a∧b=0`, `b=1` ⇒ `a=0`) (L10 p.35; E10 p.4 Sol.4c).
- **`d` and `e` are safe to open only because `i, j` are uniformly random and secret.** If the masks weren't random/secret, revealing `d = a⊕i` would leak `a`. Security of the whole AND protocol rides on this (E10 p.4 Sol.5a).
- **Preprocessing must be input-independent.** Beaver triples are generated *before* and *independent of* the actual inputs. If triple generation depended on inputs, it couldn't be done offline and the online efficiency benefit would vanish (L10 p.39; E10 p.4 Sol.5b).
- **`k = i ∧ j` is the defining property of a triple.** The AND identity collapses `(i∧j)` into `k`. A triple with `k ≠ i∧j` gives a wrong result. (E10 p.1 Ex.3; p.3 Sol.3b.)
- **Boolean sharing only constrains the XOR of shares, not individual shares.** This is why asymmetric tricks (one party holds an extra constant) are valid — what matters is the reconstructed total (E10 p.3 Sol.3c).
- **Each share must be uniformly random for security.** If `a₁` were biased (not a fair coin), it would leak information about `a`. Uniform randomness is what makes a single share a perfect blind (E10 p.3 Sol.1b).
- **Garbled circuits ≠ the protocol taught here.** The lecture mentions garbled circuits only as Yao's 1986 historical contribution (L10 p.9); the protocol it actually develops is secret-sharing + Beaver triples. Don't conflate them in an answer.
- **Semi-honest assumption.** These protocols assume parties follow the steps honestly (just curious). A malicious party who lies about its shares can corrupt the result — defending against that needs extra mechanisms (e.g., MACs, cf. L10 p.41) not covered in detail by the readable lecture.
- **Reconstruction requires exchanging shares.** Even though XOR computation is communication-free, *revealing the final output* still requires the parties to send each other their result-shares (E10 p.3 Sol.1c).
- **Handwritten-slide caveat for the exam.** The lecture's exact per-server share formulas `c_A`, `c_B` and their reconstruction check (L10 p.31–34) are handwritten and not cleanly readable from the PDF; the clean, equivalent derivation is the Beaver-triple identity in E10 p.3 Sol.3b. If an exam question asks for the lecture's specific `c_A`/`c_B` split, reproduce the identity `a∧b = k ⊕ (d∧j) ⊕ (e∧i) ⊕ (d∧e)` with `d∧e` placed on Bob's share.
```
