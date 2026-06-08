# 10. Multi-Party Computation — Commands & Code Examples

### Create a Boolean (XOR) secret sharing of a bit
**What:** Split a secret bit `a` into two shares `a = a₁ ⊕ a₂` so neither party alone learns `a`.
```python
import secrets

def share_bit(a):
    """Boolean-share a bit a into (a1, a2) with a1 ^ a2 == a."""
    a1 = secrets.randbits(1)      # Alice's share: a uniform fair coin
    a2 = a ^ a1                   # Bob's share fixed by the constraint
    return a1, a2

def reconstruct_bit(a1, a2):
    return a1 ^ a2

# Share a = 1
a1, a2 = share_bit(1)
print(a1, a2, reconstruct_bit(a1, a2))   # e.g. 0 1 1  (or 1 0 1)
```
**Notes:** `a₁` is a uniform fair coin, so `Pr[a=0 | a₁] = Pr[a=1 | a₁] = ½` — a single share leaks nothing about `a` (E10 p.3 Sol.1b). For `a = 1` the valid pairs are `(0,1)` and `(1,0)`; for `a = 0` they are `(0,0)` and `(1,1)`. Reconstruction needs both parties to exchange shares (E10 p.3 Sol.1c).

### Compute a sharing of a ⊕ b with NO communication (secure XOR)
**What:** Each party XORs its own two shares locally to get a share of `a ⊕ b`.
```python
# Setup: Alice holds (a1, b1); Bob holds (a2, b2).
# a = 1 shared as (a1,a2) = (1,0);  b = 1 shared as (b1,b2) = (0,1)
a1, a2 = 1, 0
b1, b2 = 0, 1

axb1 = a1 ^ b1     # Alice computes locally  -> 1
axb2 = a2 ^ b2     # Bob   computes locally  -> 1
# NO messages exchanged.

result = axb1 ^ axb2          # reconstruct -> 0
print(result, (a1 ^ a2) ^ (b1 ^ b2))   # 0 0  -> both equal a ⊕ b
```
**Notes:** Correctness: `(a₁⊕b₁) ⊕ (a₂⊕b₂) = (a₁⊕a₂) ⊕ (b₁⊕b₂) = a ⊕ b` (E10 p.3 Sol.2a). XOR is "free" — zero communication — which is why MPC circuits are designed to minimise the expensive AND gates (L10 p.49).

### Show why AND CANNOT be done locally (the cross-term check)
**What:** Expand `(a₁⊕a₂) ∧ (b₁⊕b₂)` and confirm cross terms mix both parties' secrets.
```python
import itertools

def lhs(a1, a2, b1, b2):
    return (a1 ^ a2) & (b1 ^ b2)

def rhs(a1, a2, b1, b2):
    return (a1 & b1) ^ (a1 & b2) ^ (a2 & b1) ^ (a2 & b2)

# Verify the identity holds for every share assignment
print(all(lhs(*v) == rhs(*v) for v in itertools.product((0,1), repeat=4)))  # True
```
**Notes:** `a∧b = (a₁∧b₁) ⊕ (a₁∧b₂) ⊕ (a₂∧b₁) ⊕ (a₂∧b₂)`. Alice can make `a₁∧b₁`, Bob can make `a₂∧b₂`, but the cross terms `a₁∧b₂` and `a₂∧b₁` each combine one of Alice's bits with one of Bob's — neither can compute them alone, so AND **needs communication** (E10 p.3 Sol.2b–2c).

### Generate a Beaver (multiplication) triple in the offline phase
**What:** Produce shared random bits `(i, j, k)` with `k = i ∧ j`, independent of the inputs.
```python
import secrets

def make_beaver_triple():
    """Preprocessing: input-independent. Returns Alice's and Bob's share tuples."""
    i = secrets.randbits(1)
    j = secrets.randbits(1)
    k = i & j                       # defining property of the triple

    # XOR-share each of i, j, k between the two parties
    i1 = secrets.randbits(1); i2 = i ^ i1
    j1 = secrets.randbits(1); j2 = j ^ j1
    k1 = secrets.randbits(1); k2 = k ^ k1

    alice = (i1, j1, k1)
    bob   = (i2, j2, k2)
    return alice, bob

print(make_beaver_triple())
```
**Notes:** `k = i ∧ j` is the **defining property** — a triple with `k ≠ i∧j` gives a wrong AND result (E10 p.1 Ex.3). Triples are expensive to make, so they are produced **offline, before the inputs are known**; this keeps the online phase cheap (L10 p.39; E10 p.4 Sol.5b). The triple is the only correlated randomness the AND protocol consumes.

### Run the secure AND protocol with a Beaver triple (full worked code)
**What:** Compute a sharing of `c = a ∧ b` by opening `d = a⊕i`, `e = b⊕j` then combining locally.
```python
def secure_and(a1, b1, i1, j1, k1,      # Alice's shares
               a2, b2, i2, j2, k2):     # Bob's shares
    # 1. Each party forms its share of d = a^i and e = b^j  (free XOR, no comms yet)
    d1, d2 = a1 ^ i1, a2 ^ i2
    e1, e2 = b1 ^ j1, b2 ^ j2

    # 2. OPEN d and e: both parties send these shares and reconstruct the public bits
    d = d1 ^ d2          # public
    e = e1 ^ e2          # public

    # 3. Each party computes its share of c using
    #    a∧b = k ⊕ (d∧j) ⊕ (e∧i) ⊕ (d∧e)
    cA = k1 ^ (d & j1) ^ (e & i1)                 # Alice
    cB = k2 ^ (d & j2) ^ (e & i2) ^ (d & e)       # Bob ALSO adds the public d∧e
    return cA, cB, d, e

# Worked example: a=0, b=1 (true a∧b = 0). Triple i=1, j=0 -> k=0.
a, b, i, j = 0, 1, 1, 0
a1, b1, i1, j1, k1 = 1, 0, 0, 1, 1          # Alice's shares (arbitrary)
a2, b2, i2, j2, k2 = a^a1, b^b1, i^i1, j^j1, (i&j)^k1   # Bob's shares
cA, cB, d, e = secure_and(a1,b1,i1,j1,k1, a2,b2,i2,j2,k2)
print(d, e, cA ^ cB)        # 1 1 0   -> reconstructs to a∧b = 0
```
**Notes:** Identity: `a∧b = (d⊕i)∧(e⊕j) = (d∧e)⊕(d∧j)⊕(e∧i)⊕(i∧j) = k ⊕ (d∧j) ⊕ (e∧i) ⊕ (d∧e)` since `k = i∧j` (E10 p.3 Sol.3b). After `d, e` are public, `d∧j` and `e∧i` are *public-bit-AND-shared-bit* (purely local), `k` is already shared, and `d∧e` is a public constant. Online cost: 2 bits opened + local XORs.

### Verify the Beaver-triple AND for every input and every triple (exhaustive)
**What:** Brute-force every `a,b,i,j` and every share split to prove the protocol always reconstructs `a∧b`.
```python
import itertools

def secure_and_reconstruct(a, b, i, j, a1, b1, i1, j1, k1):
    k = i & j
    a2,b2,i2,j2,k2 = a^a1, b^b1, i^i1, j^j1, k^k1
    d = (a1^i1) ^ (a2^i2)
    e = (b1^j1) ^ (b2^j2)
    cA = k1 ^ (d & j1) ^ (e & i1)
    cB = k2 ^ (d & j2) ^ (e & i2) ^ (d & e)
    return cA ^ cB

ok = all(
    secure_and_reconstruct(a, b, i, j, a1, b1, i1, j1, k1) == (a & b)
    for a, b, i, j in itertools.product((0,1), repeat=4)
    for a1, b1, i1, j1, k1 in itertools.product((0,1), repeat=5)
)
print("AND correct for all 16 inputs x 32 share splits:", ok)   # True
```
**Notes:** This passes for all `2⁴ × 2⁵ = 512` combinations, confirming correctness is independent of which random shares the parties hold — Boolean sharing only constrains the **XOR of the two shares**, not the individual shares (E10 p.3 Sol.3c).

### Show why "only Bob adds d∧e" is correct (and what breaks otherwise)
**What:** Inject the public constant `d∧e` into the total exactly once; both-add or neither-add is a bug.
```python
def reconstruct(d, e, k1, k2, j1, j2, i1, i2, who_adds_de):
    cA = k1 ^ (d & j1) ^ (e & i1)
    cB = k2 ^ (d & j2) ^ (e & i2)
    if who_adds_de in ("bob", "both"):
        cB ^= (d & e)
    if who_adds_de in ("alice", "both"):
        cA ^= (d & e)
    return cA ^ cB

# a=1,b=1,i=0,j=0 -> k=0; so d=1, e=1 and d∧e=1 (the term actually matters here).
d, e = 1, 1
i1,j1,k1 = 1,1,0 ; i2,j2,k2 = 1,1,0   # one valid split of i=0,j=0,k=0
for mode in ("bob", "alice", "both", "neither"):
    print(mode, reconstruct(d,e,k1,k2,j1,j2,i1,i2,mode))
# bob 1 | alice 1 | both 0 (WRONG) | neither 0 (WRONG)   true a∧b = 1
```
**Notes:** `d∧e` is a public constant that must appear in the reconstructed total **once**. Adding it on **both** shares cancels it (`x⊕x = 0`); adding it on **neither** drops it. Either error gives the wrong answer here. Which party adds it is arbitrary — Bob is just the lecture/exercise convention (E10 p.1 Ex.3c; p.3 Sol.3c).

### Additive secret sharing of an integer mod p (split and reconstruct)
**What:** Share `x` as `x = (x₁ + … + xₙ) mod p`; reconstruct by summing all shares mod p.
```python
import secrets

def additive_share(x, n, p):
    """n-party additive sharing of integer x over Z_p."""
    shares = [secrets.randbelow(p) for _ in range(n - 1)]
    shares.append((x - sum(shares)) % p)      # last share fixes the sum
    return shares

def additive_reconstruct(shares, p):
    return sum(shares) % p

p = 31
shares = additive_share(23, n=3, p=p)
print(shares, additive_reconstruct(shares, p))   # e.g. [5, 19, 30] -> 23
```
**Notes:** Additive sharing over the integers (mod `p`) is the form used "for more complicated arithmetic functions" and secure machine learning (L10 p.41). Any `n−1` shares are uniformly random and reveal nothing about `x`; only the full set sums back to `x`. This generalises Boolean XOR sharing (which is additive sharing mod 2).

### Secure addition of additively-shared values (free, like XOR)
**What:** Add two shared integers by having each party add its own shares locally — no communication.
```python
p = 97
x, y = 40, 73            # secrets, true sum (x+y) mod p = 16
x1, x2 = 15, (x - 15) % p     # shares of x
y1, y2 = 60, (y - 60) % p     # shares of y

# Each party adds locally
s1 = (x1 + y1) % p       # Alice's share of x+y
s2 = (x2 + y2) % p       # Bob's share of x+y

print((s1 + s2) % p, (x + y) % p)    # 16 16
```
**Notes:** Additive sharing makes addition (and addition by a public constant, and multiplication by a public scalar) **local/free**, exactly as XOR is free in the Boolean setting. Only **multiplication of two shared values** needs a Beaver triple and communication — the arithmetic analogue of the XOR-free/AND-expensive split (L10 p.41, p.49).

### Run a secure-sum protocol over many parties
**What:** `n` parties learn `Σ vᵢ` without revealing any individual `vᵢ`, using additive sharing.
```python
import secrets

def secure_sum(values, p):
    n = len(values)
    # Each party i splits its value into n shares and sends share j to party j
    cols = [[0] * n for _ in range(n)]       # cols[j] = shares received by party j
    for i, v in enumerate(values):
        sh = [secrets.randbelow(p) for _ in range(n - 1)]
        sh.append((v - sum(sh)) % p)
        for j in range(n):
            cols[j][i] = sh[j]
    # Each party j publishes the sum of the shares it holds
    partials = [sum(cols[j]) % p for j in range(n)]
    return sum(partials) % p

p = 101
vals = [12, 7, 23, 4]
print(secure_sum(vals, p), sum(vals))     # 46 46
```
**Notes:** Each party splits its value into `n` random additive shares and routes one to every party; each party adds the shares it received and announces only that partial sum. The partials reveal nothing about individual inputs (each is a sum of uniformly random shares), yet `Σ partials = Σ vᵢ` (mod `p`). This realises the "average / sum" function from the MPC function zoo (L10 p.7) under the semi-honest model.

### Reproduce Shamir secret sharing over GF(7) — share and recover (standard construction)
**What:** A `(t,n) = (2,3)` Shamir sharing of `s = 5`: evaluate a degree-1 polynomial, recover via Lagrange at 0.
```python
P = 7          # field GF(7)
s = 5          # secret = f(0)
c = 3          # random coefficient (degree t-1 = 1 polynomial)

def f(x):
    return (s + c * x) % P

shares = [(x, f(x)) for x in (1, 2, 3)]
print(shares)        # [(1, 1), (2, 4), (3, 0)]

def lagrange_at_zero(points, P):
    """Recover f(0) from t points over GF(P)."""
    total = 0
    for xi, yi in points:
        num = den = 1
        for xj, _ in points:
            if xj != xi:
                num = (num * (0 - xj)) % P
                den = (den * (xi - xj)) % P
        total = (total + yi * num * pow(den, -1, P)) % P    # modular inverse
    return total

print(lagrange_at_zero(shares[:2], P))     # 5  (from parties 1,2)
print(lagrange_at_zero(shares[1:], P))     # 5  (from parties 2,3)
```
**Notes:** **(standard construction)** — the lecture only *names* Shamir Secret Sharing as the 1979 milestone (L10 p.9); the polynomial construction is not on the readable slides. The secret is `f(0)`; each party gets one point. Any `t = 2` points determine the line and recover `s`; any `t−1 = 1` point lies on infinitely many lines and reveals nothing. Hand-check from `(1,1),(2,4)`: `s = 1·(0−2)/(1−2) + 4·(0−1)/(2−1) = 1·2 + 4·(−1) = −2 ≡ 5 (mod 7)`.

### Check the semi-honest adversary's view leaks nothing beyond the output
**What:** Confirm that the only opened values `d, e` are uniform regardless of the inputs (perfect masking).
```python
import itertools
from collections import Counter

# For a fixed input (a,b), enumerate all triples (i,j) uniformly and record (d,e)
for (a, b) in [(0,0), (0,1), (1,0), (1,1)]:
    view = Counter()
    for i, j in itertools.product((0,1), repeat=2):
        d = a ^ i
        e = b ^ j
        view[(d, e)] += 1
    print(f"a={a} b={b}: opened (d,e) distribution = {dict(view)}")
# Every input gives the SAME uniform distribution over (d,e): {(0,0):1,(0,1):1,(1,0):1,(1,1):1}
```
**Notes:** Because `i, j` are uniformly random and secret, `d = a⊕i` and `e = b⊕j` are uniform and **identically distributed for every input** — a curious party's view is independent of `a, b`, so it learns nothing beyond the output (E10 p.3 Sol.3a; p.4 Sol.5a). This is the semi-honest security argument. If the masks were biased or known, opening `d` would leak `a` — the whole protocol rides on uniform random masks.

### Verify the inherent output leakage that MPC does NOT hide
**What:** Show that the public result plus a party's own input can determine the other's input — allowed by definition.
```python
def deduce_other_input(result, my_input):
    """Matching: result = a AND b. If you know your own bit and the result..."""
    if result == 1:
        return "other input must be 1 (result=1 forces both inputs=1)"
    # result == 0
    if my_input == 1:
        return "other input must be 0 (since 1 AND other = 0)"
    return "other input unknown (could be 0 or 1)"

print(deduce_other_input(result=0, my_input=1))   # 'other input must be 0'
print(deduce_other_input(result=0, my_input=0))   # 'unknown'
print(deduce_other_input(result=1, my_input=1))   # 'other input must be 1'
```
**Notes:** MPC only guarantees that no party learns anything **beyond the agreed output** (L10 p.35). Information *logically implied by the output* is not a break: if `a∧b = 0` is revealed and Bob knows `b = 1`, he deduces `a = 0`. "Even in multi-party computation, this is inevitable" (E10 p.4 Sol.4c). Do not claim MPC keeps inputs "fully secret".
