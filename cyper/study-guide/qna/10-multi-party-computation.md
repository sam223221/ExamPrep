# 10. Multi-Party Computation — Simulated Open-Book Questions

### [EASY] Alice and Bob hold an XOR sharing of a secret bit with shares `a₁ = 1` and `a₂ = 0`. What is the secret `a`, and explain why Alice (holding only `a₁ = 1`) cannot tell whether the secret is 0 or 1.
**Answer:** Reconstruct by XORing the two shares: `a = a₁ ⊕ a₂ = 1 ⊕ 0 = 1` (E10 p.3 Sol.1c).

Alice cannot deduce `a` from her share alone because `a₁` is generated as a **uniformly random** bit, with `a₂ = a ⊕ a₁` filling in the rest. Given `a₁ = 1`:
- If `a = 0`, then `a₂ = 0 ⊕ 1 = 1`.
- If `a = 1`, then `a₂ = 1 ⊕ 1 = 0`.

Both worlds are equally likely, so `Pr[a = 0 | a₁ = 1] = Pr[a = 1 | a₁ = 1] = ½`. A single share is a perfect blind (E10 p.3 Sol.1b; L10 p.37).

### [EASY] You must create a Boolean (XOR) secret sharing of `a = 0` and you draw the random coin `a₁ = 1`. Compute Bob's share `a₂`, and confirm reconstruction.
**Answer:** By the sharing rule `a₂ = a ⊕ a₁` (E10 p.3 Sol.1a):

```
a₂ = a ⊕ a₁ = 0 ⊕ 1 = 1
```

So the shares are `(a₁, a₂) = (1, 1)`. Check reconstruction: `a₁ ⊕ a₂ = 1 ⊕ 1 = 0 = a` ✓. (The other valid sharing of `a = 0` would have been `(0, 0)`.)

### [EASY] Alice holds `a₁ = 1, b₁ = 1` and Bob holds `a₂ = 0, b₂ = 1`. Using the communication-free secure XOR protocol, compute each party's share of `a ⊕ b` and the reconstructed result. How many messages were exchanged?
**Answer:** Each party XORs its own two shares locally (E10 p.3 Sol.2a; L10 p.49):
- Alice: `(a⊕b)₁ = a₁ ⊕ b₁ = 1 ⊕ 1 = 0`.
- Bob: `(a⊕b)₂ = a₂ ⊕ b₂ = 0 ⊕ 1 = 1`.

Reconstruct: `(a⊕b)₁ ⊕ (a⊕b)₂ = 0 ⊕ 1 = 1`. Cross-check against the cleartext: `a = a₁⊕a₂ = 1⊕0 = 1`, `b = b₁⊕b₂ = 1⊕1 = 0`, so `a⊕b = 1⊕0 = 1` ✓.

**Zero** messages were exchanged during the computation — XOR is "free" (only the final opening, if any, costs communication).

### [EASY] In the secure AND protocol the two masked values opened to the public are `d = a ⊕ i` and `e = b ⊕ j`. With inputs `a = 1, b = 0` and triple bits `i = 0, j = 1`, compute `d` and `e`, and state in one sentence why revealing them leaks nothing about `a` or `b`.
**Answer:** Substitute directly (E10 p.1 Ex.3a):
```
d = a ⊕ i = 1 ⊕ 0 = 1
e = b ⊕ j = 0 ⊕ 1 = 1
```
Revealing `d` and `e` leaks nothing because `i` and `j` are **uniformly random secret bits** that one-time-pad-mask `a` and `b`, making `d` and `e` independent of the inputs (E10 p.3 Sol.3a, p.4 Sol.5a).

### [EASY] A Beaver triple is defined by the property `k = i ∧ j`. For the random bits `i = 1, j = 1`, what is the correct `k`? If a faulty preprocessing produced `k = 0` instead, would the triple still be valid?
**Answer:** The defining relation gives:
```
k = i ∧ j = 1 ∧ 1 = 1
```
So the correct triple bit is `k = 1` (L10 p.31; E10 p.1 Ex.3). A triple with `k = 0` would violate `k = i ∧ j` and is therefore **invalid** — the AND identity collapses the term `(i∧j)` into `k`, so a wrong `k` propagates directly into a wrong final result (Gotchas: "`k = i ∧ j` is the defining property").

### [MEDIUM] Demonstrate a full Boolean sharing of two bits `a = 1` and `b = 0`, then use the secure XOR protocol to produce a sharing of `a ⊕ b`. Give every share value and verify the result.
**Answer:** Pick random first shares for each secret, then derive the second share via `x₂ = x ⊕ x₁`.

**Share `a = 1`** — pick `a₁ = 1` ⇒ `a₂ = 1 ⊕ 1 = 0`. So `(a₁, a₂) = (1, 0)`.
**Share `b = 0`** — pick `b₁ = 1` ⇒ `b₂ = 0 ⊕ 1 = 1`. So `(b₁, b₂) = (1, 1)`.

Alice holds `a₁ = 1, b₁ = 1`; Bob holds `a₂ = 0, b₂ = 1` (E10 p.1 Ex.2).

**Secure XOR (local only):**
- Alice: `(a⊕b)₁ = a₁ ⊕ b₁ = 1 ⊕ 1 = 0`.
- Bob: `(a⊕b)₂ = a₂ ⊕ b₂ = 0 ⊕ 1 = 1`.

**Verify:** `(a⊕b)₁ ⊕ (a⊕b)₂ = 0 ⊕ 1 = 1`. True value: `a ⊕ b = 1 ⊕ 0 = 1` ✓ (E10 p.3 Sol.2a).

### [MEDIUM] Expand `(a₁ ⊕ a₂) ∧ (b₁ ⊕ b₂)` into its four product terms. Label which party can compute each term locally and which terms force communication, justifying the claim "AND is not free."
**Answer:** Distributing AND over XOR (AND = multiplication mod 2, XOR = addition mod 2):
```
(a₁ ⊕ a₂) ∧ (b₁ ⊕ b₂)
  = (a₁∧b₁) ⊕ (a₁∧b₂) ⊕ (a₂∧b₁) ⊕ (a₂∧b₂)
```
(E10 p.3 Sol.2b). Recall Alice holds `a₁, b₁` and Bob holds `a₂, b₂`:

| Term | Who can compute it | Local? |
|------|--------------------|--------|
| `a₁∧b₁` | Alice (both values hers) | yes |
| `a₂∧b₂` | Bob (both values his) | yes |
| `a₁∧b₂` | mixes Alice's `a₁` with Bob's `b₂` | **no** |
| `a₂∧b₁` | mixes Bob's `a₂` with Alice's `b₁` | **no** |

The two **cross terms** each need one secret value from each party, and neither party may reveal its value, so they cannot be computed without interaction. Hence AND requires communication, unlike XOR (E10 p.3 Sol.2c; L10 p.49).

### [MEDIUM] Build a `(2,3)` Shamir sharing of the secret `s = 3` over `GF(5)` using the random coefficient `c = 2`. Give the three parties' shares. (Reconstruction is treated in a later question.)
**Answer:** For threshold `t = 2`, use a degree-`(t−1) = 1` polynomial with constant term equal to the secret:
```
f(x) = s + c·x = 3 + 2x   (mod 5)
```
Evaluate at `x = 1, 2, 3` (each party gets one point), reducing mod 5:
- Party 1: `f(1) = 3 + 2·1 = 5 ≡ 0`.
- Party 2: `f(2) = 3 + 2·2 = 7 ≡ 2`.
- Party 3: `f(3) = 3 + 2·3 = 9 ≡ 4`.

Shares: `(1, 0), (2, 2), (3, 4)`. The secret sits at `f(0) = 3`, which no single share reveals (one point lies on infinitely many lines) (cookbook Recipe G; L10 p.9, p.37).

### [MEDIUM] Reconstruct the secret from the `(2,3)` Shamir sharing of the previous question using only Parties 2 and 3, whose points are `(2, 2)` and `(3, 4)` over `GF(5)`. Show the Lagrange interpolation at `x = 0`.
**Answer:** Lagrange interpolation to recover `f(0)` from points `(x₁,y₁) = (2,2)` and `(x₂,y₂) = (3,4)`, all mod 5:
```
s = f(0) = y₁·(0−x₂)/(x₁−x₂) + y₂·(0−x₁)/(x₂−x₁)
         = 2·(0−3)/(2−3) + 4·(0−2)/(3−2)   (mod 5)
         = 2·(−3)/(−1)   + 4·(−2)/(1)
         = 2·3           + 4·(−2)            [since (−3)/(−1) = 3]
         = 6             − 8
         = −2 ≡ 3 (mod 5) ✓
```
This matches the secret `s = 3` from the construction. Any 2 of the 3 points recover it; 1 point reveals nothing (cookbook Recipe G).

### [MEDIUM] Suppose two parties additively share integers modulo `N = 16`: `x = 7` is shared as `(x₁, x₂) = (11, 12)` and `y = 5` as `(y₁, y₂) = (9, 12)`. Show that addition of additively-shared values is also communication-free, and reconstruct `x + y`.
**Answer:** First sanity-check the input shares mod 16: `x₁ + x₂ = 11 + 12 = 23 ≡ 7 = x` ✓ and `y₁ + y₂ = 9 + 12 = 21 ≡ 5 = y` ✓ (L10 p.41 additive sharing).

Each party adds its own shares **locally** (no messages):
- Party 1: `z₁ = x₁ + y₁ = 11 + 9 = 20 ≡ 4 (mod 16)`.
- Party 2: `z₂ = x₂ + y₂ = 12 + 12 = 24 ≡ 8 (mod 16)`.

Reconstruct: `z₁ + z₂ = 4 + 8 = 12 (mod 16)`. True value: `x + y = 7 + 5 = 12` ✓. Just as XOR is free for Boolean sharing, **addition is free for additive sharing** — both are linear operations the parties apply to their own shares (L10 p.41, p.49).

### [HARD] Run the complete secure AND protocol for `a = 0, b = 1` (Alice does not like Bob, Bob likes Alice) using the Beaver triple `i = 1, j = 0`. Compute `k`, the masked values `d, e`, evaluate the AND identity, and confirm the result equals `a ∧ b`.
**Answer:** **Triple:** `k = i ∧ j = 1 ∧ 0 = 0`.

**Masked values (opened publicly):**
```
d = a ⊕ i = 0 ⊕ 1 = 1
e = b ⊕ j = 1 ⊕ 0 = 1
```

**AND identity** `a ∧ b = k ⊕ (d∧j) ⊕ (e∧i) ⊕ (d∧e)` (E10 p.3 Sol.3b):
```
= 0 ⊕ (1∧0) ⊕ (1∧1) ⊕ (1∧1)
= 0 ⊕   0   ⊕   1   ⊕   1
= 0
```
Step XORs: `0⊕0 = 0`, `0⊕1 = 1`, `1⊕1 = 0`. **Result = 0.**

True value: `a ∧ b = 0 ∧ 1 = 0` ✓. The output `0` reveals "not mutual"; since Bob knows `b = 1`, he can further deduce `a = 0` — inherent, allowed leakage (L10 p.35; E10 p.4 Sol.4c).

### [HARD] Run the secure AND protocol for `a = 1, b = 1` with the Beaver triple `i = 1, j = 1` (so `k = 1`). Evaluate the identity term-by-term and verify. Then state what would happen if BOTH parties — not just Bob — added the public term `d∧e` to their shares.
**Answer:** **Triple:** `k = i ∧ j = 1 ∧ 1 = 1`.

**Masked values:**
```
d = a ⊕ i = 1 ⊕ 1 = 0
e = b ⊕ j = 1 ⊕ 1 = 0
```

**Identity:**
```
a ∧ b = k ⊕ (d∧j) ⊕ (e∧i) ⊕ (d∧e)
      = 1 ⊕ (0∧1) ⊕ (0∧1) ⊕ (0∧0)
      = 1 ⊕   0   ⊕   0   ⊕   0
      = 1
```
True value `a ∧ b = 1 ∧ 1 = 1` ✓.

**If both parties added `d∧e`:** the public constant would enter the reconstructed total **twice**. Since reconstruction is an XOR of the two shares, `(d∧e) ⊕ (d∧e) = 0` — the term **cancels**. The protocol relies on `d∧e` surviving exactly once, so doubling it gives the wrong result. The convention "**only Bob adds `d∧e`**" injects it once into the total `share_Alice ⊕ share_Bob` (E10 p.1 Ex.3c, p.3 Sol.3c; Gotchas).

### [HARD] Carry out the secure AND for `a = 1, b = 1` with triple `i = 0, j = 1`, but this time compute Alice's and Bob's individual `c`-shares separately (Bob adds `d∧e`), using share assignments `k₁ = 0`, `i₁ = 1`, `j₁ = 1` for Alice. Show that `c₁ ⊕ c₂ = a ∧ b`.
**Answer:** **Triple bits:** `k = i ∧ j = 0 ∧ 1 = 0`. Derive Bob's shares from Alice's (since each value XOR-shares to its true value):
- `k`: `k₁ = 0` ⇒ `k₂ = k ⊕ k₁ = 0 ⊕ 0 = 0`.
- `i`: `i₁ = 1` ⇒ `i₂ = i ⊕ i₁ = 0 ⊕ 1 = 1`.
- `j`: `j₁ = 1` ⇒ `j₂ = j ⊕ j₁ = 1 ⊕ 1 = 0`.

**Public masked values:** `d = a⊕i = 1⊕0 = 1`, `e = b⊕j = 1⊕1 = 0`. Open `d = 1, e = 0`.

**Alice's share** (no `d∧e`): `c₁ = k₁ ⊕ (d∧j₁) ⊕ (e∧i₁) = 0 ⊕ (1∧1) ⊕ (0∧1) = 0 ⊕ 1 ⊕ 0 = 1`.

**Bob's share** (adds `d∧e`): `c₂ = k₂ ⊕ (d∧j₂) ⊕ (e∧i₂) ⊕ (d∧e) = 0 ⊕ (1∧0) ⊕ (0∧1) ⊕ (1∧0) = 0 ⊕ 0 ⊕ 0 ⊕ 0 = 0`.

**Reconstruct:** `c₁ ⊕ c₂ = 1 ⊕ 0 = 1`. True value `a ∧ b = 1 ∧ 1 = 1` ✓. (Cross-check via the combined identity: `k ⊕ (d∧j) ⊕ (e∧i) ⊕ (d∧e) = 0 ⊕ (1∧1) ⊕ (0∧0) ⊕ (1∧0) = 0⊕1⊕0⊕0 = 1` ✓.) The split is correct because Boolean sharing only constrains the XOR of the two shares, not the individual pieces (E10 p.3 Sol.3c).

### [HARD] You must securely compute `(a ∧ b) ∧ c` for `a = b = c = 1`. Explain why this needs two Beaver triples, then evaluate it: use triple `i = 1, j = 0` for the first AND and triple `i' = 0, j' = 1` for the second AND. Show all steps.
**Answer:** Each AND gate is the "expensive" gate and consumes **one fresh Beaver triple** (XOR gates are free and consume none). A circuit with two AND gates therefore needs **two independent triples** prepared in the offline phase (L10 p.39, p.49). Triples must be independent so the masks of one gate don't correlate with another.

**First AND, `t = a ∧ b`** with `i = 1, j = 0` ⇒ `k = 1∧0 = 0`:
```
d = a⊕i = 1⊕1 = 0,   e = b⊕j = 1⊕0 = 1
t = k ⊕ (d∧j) ⊕ (e∧i) ⊕ (d∧e)
  = 0 ⊕ (0∧0) ⊕ (1∧1) ⊕ (0∧1)
  = 0 ⊕   0   ⊕   1   ⊕   0  = 1
```
So `t = a ∧ b = 1`. ✓ (`1 ∧ 1 = 1`.)

**Second AND, `t ∧ c`** with `i' = 0, j' = 1` ⇒ `k' = 0∧1 = 0`. Inputs are now `t = 1`, `c = 1`:
```
d' = t⊕i' = 1⊕0 = 1,   e' = c⊕j' = 1⊕1 = 0
result = k' ⊕ (d'∧j') ⊕ (e'∧i') ⊕ (d'∧e')
       = 0 ⊕ (1∧1) ⊕ (0∧0) ⊕ (1∧0)
       = 0 ⊕   1   ⊕   0   ⊕   0  = 1
```
**Final result = 1.** True value `(a∧b)∧c = 1∧1∧1 = 1` ✓. Note the intermediate `t` stays secret-shared between the two gates; it is never opened (only `d, e, d', e'` are opened, each masked by fresh random triple bits).

### [HARD] A `(2,3)` Shamir sharing over `GF(11)` distributes the points `(1, 0), (2, 7), (3, 3)`. Reconstruct the secret using Parties 1 and 3, showing the Lagrange weights and the modular inverse you need.
**Answer:** Recover `f(0)` from `(x₁,y₁) = (1,0)` and `(x₂,y₂) = (3,3)`, all arithmetic mod 11:
```
s = y₁·(0−x₂)/(x₁−x₂) + y₂·(0−x₁)/(x₂−x₁)
  = 0·(0−3)/(1−3)     + 3·(0−1)/(3−1)
```
The first term vanishes because `y₁ = 0`. For the second term compute the Lagrange weight `L₂ = (0−1)/(3−1) = (−1)/(2) (mod 11)`:
- `−1 ≡ 10 (mod 11)`.
- `2⁻¹ (mod 11)`: since `2·6 = 12 ≡ 1`, the inverse is `6`.
- `L₂ = 10 · 6 = 60 ≡ 5 (mod 11)` (because `60 = 5·11 + 5`).

Then:
```
s = 0 + y₂·L₂ = 3·5 = 15 ≡ 4 (mod 11)
```
**Secret `s = 4`.** (Construction was `f(x) = 4 + 7x mod 11`; indeed `f(0) = 4`, `f(1) = 11 ≡ 0`, `f(3) = 25 ≡ 3` ✓.) One point alone is consistent with every possible secret, so it leaks nothing.

### [VERY HARD] In the matching scenario the secure AND outputs `a ∧ b = 0` publicly. Alice knows her own input `a = 1`. Analyze precisely what Alice learns about Bob's input `b`, and whether this constitutes a break of MPC security. Contrast with the case where the public output is `1`.
**Answer:** **Case output = 0, Alice knows `a = 1`.** Since `a ∧ b = 0` and `a = 1`, we need `1 ∧ b = 0`, which forces `b = 0`. Alice therefore learns Bob's private input **exactly** (`b = 0`).

This is **not** a security break. MPC's definition guarantees only that no party learns anything **beyond what the output reveals**; information *logically implied by the output itself* is "inherent and allowed" (L10 p.35; E10 p.4 Sol.4c). Here `b = 0` is a logical consequence of the (intended) public output combined with Alice's own input — the protocol's messages (`d`, `e`) leaked nothing; the deduction comes purely from the result.

**Contrast, output = 1.** Then `a ∧ b = 1` forces both `a = 1` and `b = 1`. Each party learns the other's input — but again this is unavoidable: AND-equals-1 *means* both liked each other, which is the very information the function is meant to compute. In general, whenever a party's own input plus the output pins down the other input, that leakage is part of the function's semantics, not a flaw in the protocol (Gotchas: "MPC does not hide output-implied information").

### [VERY HARD] An adversary controls one of the two servers in the AND protocol but acts only as a semi-honest (honest-but-curious) party. Identify every value this corrupted server observes during the online phase, and argue why none of them — individually or jointly — reveals the honest party's input. Then explain why this argument collapses if the adversary becomes malicious.
**Answer:** **What the corrupted server sees online** (say it is Bob, holding `a₂, b₂` and his shares `i₂, j₂, k₂`):
1. Its own input/triple shares: `a₂, b₂, i₂, j₂, k₂` — random masks, independent of the secrets.
2. The two **opened** public values `d = a ⊕ i` and `e = b ⊕ j`.

**Why nothing leaks (semi-honest):** Each opened value is the honest input one-time-padded by a uniformly random, secret triple bit. `d = a ⊕ i` with `i` uniform and unknown to Bob ⇒ `d` is uniform and independent of `a`; likewise `e` is independent of `b` (E10 p.4 Sol.5a). Bob's own shares `a₂, i₂, …` are also uniform and carry no information about the honest party's actual `a₁`/secret, because a single Boolean share is a perfect blind (E10 p.3 Sol.1b). Jointly, `(a₂, i₂, d)` still don't pin down `a`: knowing `a₂` and `d = a ⊕ i` would require `i₁` (Alice's share of `i`) to invert, which Bob never sees. So the view is simulatable from random bits alone — the semi-honest guarantee.

**Why it collapses under a malicious adversary:** The proof assumed the corrupted party **follows the protocol**. A malicious Bob can deviate: e.g., lie about his share when opening `d`/`e`, or input a doctored share so the reconstructed output is a function he chooses. He could open a wrong `d` to make the final `c` reveal the honest input, or simply corrupt correctness undetectably. The masking argument only shows the *honest-execution transcript* is uninformative; it gives **no integrity guarantee**. Defending against deviation needs extra machinery such as MACs to authenticate shares (L10 p.41; E10 p.3–4 Sol.5a; Gotchas: "Semi-honest assumption").

### [VERY HARD] A student proposes "optimizing" the AND protocol by reusing a single Beaver triple `(i, j, k)` for two different AND gates instead of generating a fresh triple for each. Explain concretely what goes wrong, using the masked values, and tie your answer to why preprocessing must be input-independent yet per-gate.
**Answer:** **The leak from reuse.** Each AND gate opens `d = x ⊕ i` and `e = y ⊕ j`. If the *same* `(i, j)` masks two gates with inputs `(x, y)` and `(x', y')`, the adversary sees `d = x⊕i`, `d' = x'⊕i`, hence:
```
d ⊕ d' = (x⊕i) ⊕ (x'⊕i) = x ⊕ x'
```
The random mask `i` **cancels**, revealing the XOR of the two secret inputs `x ⊕ x'` — information that is *not* implied by the gate outputs and is therefore a genuine break, not allowed output leakage. Identically, `e ⊕ e' = y ⊕ y'`. A one-time pad must be used **once**; a Beaver triple is exactly a one-time correlated mask, so each AND gate needs its **own fresh** triple (Gotchas: masking security rides on `i, j` being random *and* used once; L10 p.39).

**Reconciling "input-independent" with "per-gate."** Preprocessing is **input-independent** in the sense that the triples' *values* (`i, j, k = i∧j`) are sampled before any real input is known — that is what lets the expensive generation run offline and keeps the online phase cheap (E10 p.4 Sol.5b; L10 p.39). But the *quantity* of triples is determined by the circuit's structure: one per AND gate. So the offline phase must produce **as many independent triples as there are AND gates** (here, two), all without seeing inputs. Reusing one triple breaks the one-time-mask property even though the triple itself was generated input-independently. This is also why circuits are engineered to minimize AND gates — fewer triples to precompute (L10 p.49; E10 p.3 Sol.2).

### [VERY HARD] The lecture's history lists Yao's millionaires' problem (1982) and "general-function 2PC" / garbled circuits (1986), yet the protocol actually constructed in the course is secret-sharing with Beaver triples — not garbled circuits. Suppose an exam asks you to "solve the millionaires' problem with the techniques from this course." Outline how you would express `x > y` as a circuit the Beaver-triple machinery can evaluate, and identify the one resource cost that dominates.
**Answer:** **Why this is even possible.** MPC's universality claim is that *any* function — including comparison `x > y` — can be computed securely (L10 p.7). The course builds two primitives that are functionally complete for Boolean circuits: free XOR (secure XOR protocol) and AND-via-Beaver-triple (secure AND). Since `{XOR, AND, constant-1}` is a complete basis, any comparison circuit can be evaluated with exactly these gates — no garbled circuits needed (garbled circuits are only named historically, L10 p.9; the constructed approach is secret-sharing + triples, Gotchas: "Garbled circuits ≠ the protocol taught here").

**Sketch of the `x > y` circuit on shared bits.** Write `x` and `y` as `n`-bit numbers, Boolean-secret-shared bit by bit. A standard comparator processes bits from most-significant to least-significant, carrying a "decided" flag. At each bit position `i` it needs equality/greater tests such as `xᵢ ∧ ¬yᵢ` and `¬(xᵢ ⊕ yᵢ)` (equality), combined with the running result. Concretely each bit-slice uses a handful of XORs (free) plus a small constant number of AND gates; chaining `n` slices yields `O(n)` AND gates total. Negation `¬z = z ⊕ 1` is a free constant-XOR. The final 1-bit output is opened to reveal who is richer — and, like all MPC, it inherently leaks only what `x > y` implies (e.g., if the answer is "Alice richer," nothing about the gap is revealed beyond that).

**Dominant cost.** The **AND gates** dominate, because each one consumes a fresh Beaver triple that must be produced in the expensive offline preprocessing phase (and each needs a round of communication to open `d, e`). XOR gates are free. Therefore the resource cost is essentially **the number of multiplication triples ≈ the number of AND gates ≈ O(n)** for an `n`-bit comparison — which is exactly why minimizing AND-gate count is the central optimization goal in MPC circuit design (L10 p.39, p.49; E10 p.4 Sol.5b).

### [VERY HARD] A secret `s` is shared with a `(t, n) = (3, 5)` Shamir scheme over `GF(7)`. Two of the five share-holders secretly collude. Using the polynomial `f(x) = 2 + 3x + x²` as the underlying (to them unknown) sharing, demonstrate numerically why their 2 pooled shares reveal nothing about `s`, yet any 3 honest parties recover it. Relate this to the threshold guarantee that ordinary XOR sharing lacks.
**Answer:** For threshold `t = 3` the dealer uses a degree-`(t−1) = 2` polynomial; the secret is `s = f(0) = 2`. The five shares are `f(1..5) mod 7`:
- `f(1) = 2 + 3 + 1 = 6`
- `f(2) = 2 + 6 + 4 = 12 ≡ 5`
- `f(3) = 2 + 9 + 9 = 20 ≡ 6`
- `f(4) = 2 + 12 + 16 = 30 ≡ 2`
- `f(5) = 2 + 15 + 25 = 42 ≡ 0`

**Two colluders learn nothing.** Suppose Parties 1 and 2 pool their points `(1, 6)` and `(2, 5)`. A degree-2 polynomial has 3 unknown coefficients; 2 points leave **one degree of freedom**. For *every* candidate secret `s ∈ GF(7)`, the three points `(0, s), (1, 6), (2, 5)` determine exactly one degree-≤2 polynomial through them (3 points ⇒ unique). So each of the 7 possible secrets is equally consistent with what they see: `Pr[s = σ | two shares] = 1/7` for all `σ`. The pooled view is independent of `s` — **2 < t reveals nothing**.

**Three honest parties recover it.** With 3 points, say `(1,6), (2,5), (3,6)`, Lagrange interpolation at `x = 0` yields a unique answer. Carrying out the interpolation mod 7 gives `f(0) = 2 = s` ✓ (3 = t points suffice; the polynomial is now fully pinned down).

**Relation to XOR sharing.** Plain Boolean XOR sharing `a = a₁ ⊕ a₂` is effectively a `(2, 2)` scheme — it needs **all** parties to reconstruct and tolerates **no** missing or colluding share beyond `t−1 = 1`. Shamir generalizes this to an arbitrary threshold: any `t−1` shares (here 2) leak nothing, any `t` (here 3) reconstruct, and up to `n − t` parties can be unavailable. This tunable `(t, n)` resilience — fault tolerance plus collusion resistance below threshold — is exactly what the simple two-party XOR/additive sharing used in the lecture's protocols does not provide (L10 p.9, p.37; cookbook Recipe G).
