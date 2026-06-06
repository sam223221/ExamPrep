# 09. Cryptography — Simulated Open-Book Questions

### [EASY] For an RSA setup with primes `p = 7` and `q = 13`, compute the modulus `n` and Euler's totient `φ(n)` that the key generation needs.
**Answer:** RSA uses `n = pq` for encryption/decryption and `φ(n) = (p−1)(q−1)` to derive the exponents (L09 p.30–31).

```
n   = p·q       = 7·13      = 91
φ(n)= (p−1)(q−1)= 6·12       = 72
```

**`n = 91`, `φ(n) = 72`.** Note the classic trap: `φ(n)` is `(p−1)(q−1) = 72`, NOT `pq = 91` (L09 p.31).

### [EASY] You are choosing a public exponent `e` for RSA with `φ(n) = 40`. A colleague suggests `e = 4`. Is that a valid choice? Justify with a computation.
**Answer:** `e` must be invertible mod `φ(n)`, i.e. `gcd(e, φ(n)) = 1`, so that a private `d` with `ed ≡ 1 (mod φ(n))` exists (L09 p.31).

```
gcd(4, 40): 4 and 40 share the factor 4  →  gcd = 4 ≠ 1
```

**Invalid.** Since `gcd(4,40) = 4`, no modular inverse of 4 exists mod 40, so no `d` can be found. A valid choice would be e.g. `e = 13` (`gcd(13,40) = 1`).

### [EASY] A Caesar cipher uses the lecture's encryption rule (left-shift the alphabet by KEY positions). With `KEY = 5`, encrypt the plaintext `ATTACK`.
**Answer:** Number letters `A=0 … Z=25`. Left-shift encryption maps each plaintext letter to the letter `KEY` positions *earlier* (subtract 5, mod 26) — this matches the slide's `CRYPTOGRAPHY IS FUN → ZOVMQLDOXMEV...` direction (L09 p.8).

```
A(0)-5 = -5 ≡ 21 → V
T(19)-5= 14      → O
T(19)-5= 14      → O
A(0)-5 = -5 ≡ 21 → V
C(2)-5 = -3 ≡ 23 → X
K(10)-5= 5       → F
```

**Ciphertext: `VOOVXF`.** (Decrypting `VOOVXF` by shifting +5 returns `ATTACK`.)

### [EASY] A One Time Pad encrypts the 7-bit plaintext `1011001` with the random key `0110101` by bitwise XOR. Give the ciphertext, then show that XOR-ing it with the key recovers the plaintext.
**Answer:** OTP encryption is `ciphertext = plaintext ⊕ key`, and because XOR is its own inverse, `plaintext = ciphertext ⊕ key` (L09 p.22, cookbook I).

```
plaintext : 1 0 1 1 0 0 1
key       : 0 1 1 0 1 0 1   (⊕)
————————————————————————————
ciphertext: 1 1 0 1 1 0 0
```

Decrypt — `ciphertext ⊕ key`:

```
ciphertext: 1 1 0 1 1 0 0
key       : 0 1 1 0 1 0 1   (⊕)
————————————————————————————
plaintext : 1 0 1 1 0 0 1   ✓ recovered
```

**Ciphertext = `1101100`.**

### [EASY] A web service must encrypt large volumes of file data quickly on a device that already shares a secret key with the server. Which lecture family — symmetric (e.g. AES) or public-key (e.g. RSA) — fits, and why in one line?
**Answer:** Use **symmetric (AES)**. The two parties already share a secret key, which removes the key-distribution problem that symmetric ciphers have (L09 p.23), and symmetric ciphers are fast bit/byte operations over few rounds (AES: 128-bit key, 10 rounds, L09 p.19) versus public-key schemes doing modular exponentiation on a 2048-bit modulus (L09 p.35). Public-key (RSA) is reserved for *establishing* a key, not bulk data (L09 Q&A, E09 Ex2.1).

### [MEDIUM] Run the full RSA key generation for `p = 3`, `q = 11`, `e = 3`: compute `n`, `φ(n)`, and find the private exponent `d`. State the public and secret keys.
**Answer:** Follow steps ①–⑥ (L09 p.30–31).

```
① n    = 3·11           = 33
② φ(n) = (3−1)(11−1)    = 2·10 = 20
③ check gcd(3,20) = 1   ✓  (e=3 valid)
④ find d with 3d ≡ 1 (mod 20):
     3·7 = 21 = 1·20 + 1  →  21 mod 20 = 1   ✓
   so d = 7
```

**Public key `(n, e) = (33, 3)`; secret key `(n, d) = (33, 7)`.**

### [MEDIUM] Using the RSA public key `(n, e) = (33, 3)` from the previous setup, encrypt the message `m = 5`. Show the modular exponentiation step by step.
**Answer:** RSA encryption is `c = m^e mod n` (L09 p.32).

```
c = 5^3 mod 33
5^2 = 25
5^3 = 25·5 = 125
125 mod 33 = 125 − 3·33 = 125 − 99 = 26
```

**Ciphertext `c = 26`.**

### [MEDIUM] Continuing the RSA example `(n = 33, d = 7)`, decrypt the ciphertext `c = 26` and confirm it returns `m = 5`. Use square-and-multiply to keep numbers small.
**Answer:** RSA decryption is `m = c^d mod n = 26^7 mod 33` (L09 p.33). Reduce at each step. Note `26 ≡ −7 (mod 33)`, which simplifies the squares.

```
26   ≡ −7            (mod 33)
26^2 ≡ (−7)^2 = 49 ≡ 49 − 33 = 16
26^4 ≡ 16^2 = 256 ≡ 256 − 7·33 = 256 − 231 = 25
26^7 = 26^4 · 26^2 · 26^1
     ≡ 25 · 16 · 26
25·16 = 400 ≡ 400 − 12·33 = 400 − 396 = 4
4·26  = 104 ≡ 104 − 3·33 = 104 − 99 = 5
```

**`m = 5` ✓** — decryption recovers the original plaintext.

### [MEDIUM] Run ElGamal encryption with public parameters `p = 23`, `g = 5`, secret key `x = 6` (so `h = g^x mod p`), randomness `k = 3`, and plaintext `m = 4`. Give `h`, `c1`, and `c2`.
**Answer:** Compute `h`, then the ciphertext pair `c1 = g^k mod p`, `c2 = m·h^k mod p` (L09 p.37–39).

```
h = 5^6 mod 23:
  5^2 = 25 ≡ 2 ;  5^4 = 2^2 = 4 ;  5^6 = 5^4·5^2 = 4·2 = 8     → h = 8

c1 = 5^3 mod 23 = 125 ≡ 125 − 5·23 = 125 − 115 = 10            → c1 = 10

h^k = 8^3 mod 23 = 512 ≡ 512 − 22·23 = 512 − 506 = 6
c2 = m·h^k = 4·6 = 24 ≡ 24 − 23 = 1                            → c2 = 1
```

**`h = 8`, ciphertext `(c1, c2) = (10, 1)`.**

### [MEDIUM] Two ciphertexts were produced by the *same* scheme for the *same* plaintext, and they differ from each other. From the lecture's two public-key schemes, which scheme produced them — RSA or ElGamal — and what single ingredient causes this?
**Answer:** **ElGamal.** Textbook RSA is **deterministic**: `c = m^e mod n` always gives the *same* `c` for the same `m`. ElGamal is **randomized** because the encryptor picks fresh randomness `k` each run, so `c1 = g^k mod p` and `c2 = m·h^k mod p` change every time even for an identical `m` (L09 p.37–39, p.30–34). The single ingredient is the **per-encryption random value `k`** (L09 p.39). This is why an ElGamal ciphertext is a *pair* `(c1,c2)` of roughly double the message size, whereas RSA outputs a single value.

### [HARD] Complete this RSA problem end to end: `p = 7`, `q = 11`, `e = 13`, plaintext `m = 2`. Find `d`, compute the ciphertext `c`, and verify decryption returns `m`.
**Answer:** Steps ①–⑧ (L09 p.30–34).

```
① n    = 7·11 = 77
② φ(n) = 6·10 = 60          (gcd(13,60)=1 ✓)
③ find d: 13d ≡ 1 (mod 60)
     13·37 = 481 = 8·60 + 1 → 481 mod 60 = 1   →  d = 37
```

Encrypt `c = 2^13 mod 77`:

```
2^6  = 64
2^7  = 128 ≡ 128 − 77 = 51
2^13 = 2^7 · 2^6 = 51·64 = 3264
3264 mod 77 = 3264 − 42·77 = 3264 − 3234 = 30
```

**`c = 30`.** Verify decryption `m = 30^37 mod 77`:

```
30^2  = 900 ≡ 900 − 11·77 = 900 − 847 = 53
30^4  = 53^2 = 2809 ≡ 2809 − 36·77 = 2809 − 2772 = 37
30^8  = 37^2 = 1369 ≡ 1369 − 17·77 = 1369 − 1309 = 60
30^16 = 60^2 = 3600 ≡ 3600 − 46·77 = 3600 − 3542 = 58
30^32 = 58^2 = 3364 ≡ 3364 − 43·77 = 3364 − 3311 = 53
37 = 100101₂ = 32 + 4 + 1
30^37 = 30^32 · 30^4 · 30^1 ≡ 53 · 37 · 30
53·37 = 1961 ≡ 1961 − 25·77 = 1961 − 1925 = 36
36·30 = 1080 ≡ 1080 − 14·77 = 1080 − 1078 = 2
```

**`m = 2` ✓.** So `d = 37`, `c = 30`, decryption recovers `m = 2`.

### [HARD] An RSA public key is `(n, e) = (33, 3)` and you intercept the ciphertext `c = 26`. Recover the private key `d` *from scratch* (you may factor the small `n`), then decrypt to find `m`.
**Answer:** RSA's security rests on `n` being hard to factor; with a tiny `n` we can factor by hand (L09 p.35).

```
Factor n = 33 = 3 · 11   →  p = 3, q = 11
φ(n) = (3−1)(11−1) = 2·10 = 20
Find d: 3d ≡ 1 (mod 20)
  3·7 = 21 ≡ 1 (mod 20)   →  d = 7
```

Decrypt `m = c^d mod n = 26^7 mod 33`:

```
26 ≡ −7 (mod 33)
26^2 ≡ 49 ≡ 16
26^4 ≡ 16^2 = 256 ≡ 256 − 7·33 = 25
26^7 = 26^4·26^2·26 ≡ 25·16·26
  25·16 = 400 ≡ 4 ;  4·26 = 104 ≡ 104 − 3·33 = 5
```

**`d = 7`, `m = 5`.** This demonstrates the lecture's point: small primes make `n` factorable, breaking the scheme — real RSA needs large primes and a 2048-bit `n` (L09 p.35).

### [HARD] Decrypt the ElGamal ciphertext `(c1, c2) = (10, 1)` given the secret key `x = 6` and modulus `p = 23`. Show the shared secret `s`, its modular inverse, and the recovered `m`.
**Answer:** Decrypt with `s = c1^x mod p`, then `m = c2 · s^(−1) mod p` (L09 p.40). You must use the *modular inverse* of `s`, not ordinary division.

```
s = 10^6 mod 23:
  10^2 = 100 ≡ 100 − 4·23 = 8
  10^4 = 8^2 = 64 ≡ 64 − 2·23 = 18
  10^6 = 10^4·10^2 = 18·8 = 144 ≡ 144 − 6·23 = 144 − 138 = 6
  → s = 6

s^(−1) mod 23: need 6·t ≡ 1 (mod 23)
  6·4 = 24 ≡ 1   →  s^(−1) = 4

m = c2 · s^(−1) = 1 · 4 = 4 (mod 23)
```

**`s = 6`, `s^(−1) = 4`, `m = 4` ✓** — matches the plaintext from the encryption with `k = 3` (the prior MEDIUM problem).

### [HARD] A symmetric cipher uses a 56-bit key (like DES's effective key length). An attacker tries `2^30` keys per second. Estimate the worst-case brute-force time in years (order of magnitude), and explain in one line why this — combined with cryptanalysis — made DES insecure.
**Answer:** Worst case = exhaust the whole key space `2^56` at `2^30` keys/s (L09 p.16–17, cookbook H).

```
time = 2^56 / 2^30 = 2^26 seconds
2^26 = 67,108,864 s
in years: 67,108,864 / (60·60·24·365)
        = 67,108,864 / 31,536,000
        ≈ 2.13 years
```

**About 2 years on a single `2^30` keys/s machine** — and only ~1 year on average (you expect to hit the key after searching half the space). That is *feasible* for a well-resourced attacker (and trivial when parallelized across many machines), so the **short 56-bit key allowed brute force**; combined with differential cryptanalysis (Biham & Shamir, late 1980s) and linear cryptanalysis (Matsui, 1994), DES was broken (L09 p.16–17). Contrast AES's 128-bit key, where `2^128/2^30 = 2^98 s ≈ 10^22 years` — infeasible (L09 p.19–20).

### [HARD] You captured a ciphertext you believe is a Caesar cipher: `WKLV LV HDVB`. Break it without knowing the key, showing the reasoning, then give the key and plaintext.
**Answer:** Caesar has only 25 useful keys, so brute force is trivial; decryption shifts each letter *forward* by the trial key (`A=0…Z=25`) (L09 p.8, cookbook A). The first word `WKLV` has 4 letters and the third looks like it should form a common word. Try small shifts:

```
shift +3:  W(22)+3=25→Z ... no (gives 'ZNOY')
shift +23 (= encrypt key 3): W(22)+23=45 mod26=19→T
  W→T  K(10)+23=33 mod26=7→H  L(11)+23=34 mod26=8→I  V(21)+23=44 mod26=18→S
  →  WKLV → THIS
  LV   → L(11)+23=8→I  V→S        → IS
  HDVB → H(7)+23=4→E D(3)+23=0→A V→S B(1)+23=24→Y → EASY
```

The matching decryption shift is **+23**, i.e. the message was encrypted with **KEY = 3** (left-shift by 3; decrypting adds 3, equivalently +23 forward).

**Key = 3, plaintext = `THIS IS EASY`.** Caesar falls instantly because it is a *monoalphabetic* substitution with only 25 keys (L09 p.11).

### [VERY HARD] An ElGamal user, to "save effort," reuses the SAME randomness `k` to encrypt two different messages `m1` and `m2` under public key `(p, g, h)`. Show with the formulas why an attacker who learns `m1` can recover `m2` from the two ciphertexts. Reference the lecture rule this violates.
**Answer:** ElGamal encryption is `c1 = g^k mod p`, `c2 = m·h^k mod p` (L09 p.37–39). Encrypting `m1` and `m2` with the *same* `k`:

```
Ciphertext 1: (c1,  c2a) = (g^k,  m1·h^k)
Ciphertext 2: (c1,  c2b) = (g^k,  m2·h^k)   ← same c1, since same k
```

The `c1` values are identical (a dead giveaway that `k` was reused). Divide the two `c2` components — the secret factor `h^k` cancels:

```
c2a / c2b = (m1·h^k) / (m2·h^k) = m1 / m2   (mod p)
```

So `m2 ≡ m1 · (c2a / c2b)^(−1) ≡ m1 · c2b · c2a^(−1) (mod p)`. If the attacker knows `m1`, they compute `m2` directly with one modular inverse — **no discrete log, no secret key `x` needed**. Concretely with the lecture's `p=23, g=5, x=6` (`h=8`), `k=7` (`h^k≡12`): if `m1=9` then `c2a = 9·12 = 16`; if `m2` is unknown with `c2b`, then `m2 = m1·c2b·c2a^(−1) = 9·c2b·16^(−1) mod 23`. This mirrors the **OTP rule** the lecture stresses — *the key (here the randomness) must not be reused* (L09 p.23) — because reuse leaks the relationship between plaintexts. Lesson: ElGamal's per-message `k` must be fresh and random every time (L09 p.39).

### [VERY HARD] An RSA implementer picks `p = 5`, `q = 7`, `e = 5`, `m = 10` and computes `d`, then notices the ciphertext `c` equals the plaintext `m`. Verify `d`, compute `c`, and explain whether this "fixed point" reveals a flaw in *the math* or just in *the chosen parameters*.
**Answer:** Run the scheme (L09 p.30–34).

```
n    = 5·7 = 35
φ(n) = 4·6 = 24             (gcd(5,24)=1 ✓)
find d: 5d ≡ 1 (mod 24)
  5·5 = 25 ≡ 1 (mod 24)     →  d = 5   (here e = d = 5, self-inverse mod 24)

Encrypt c = 10^5 mod 35:
  10^2 = 100 ≡ 100 − 2·35 = 30
  10^4 = 30^2 = 900 ≡ 900 − 25·35 = 900 − 875 = 25
  10^5 = 10^4·10 = 25·10 = 250 ≡ 250 − 7·35 = 250 − 245 = 5 ... recheck:
```

Recompute carefully: `250 − 7·35 = 250 − 245 = 5`. But let us verify the round trip — decrypt `c` with `d = 5`: it must give 10. Test the claim directly: `10^5 mod 35`.

```
10^1 ≡ 10
10^2 ≡ 30
10^3 = 10^2·10 = 30·10 = 300 ≡ 300 − 8·35 = 300 − 280 = 20
10^4 = 20·10 = 200 ≡ 200 − 5·35 = 200 − 175 = 25
10^5 = 25·10 = 250 ≡ 5
```

So **`c = 5`** (not equal to `m = 10`), and decryption `c^d = 5^5 mod 35`:

```
5^2 = 25 ; 5^3 = 125 ≡ 125 − 3·35 = 20 ; 5^4 = 20·5 = 100 ≡ 30 ; 5^5 = 30·5 = 150 ≡ 150 − 4·35 = 10  ✓
```

**`d = 5`, `c = 5`, decryption returns `m = 10`.** The premise that `c = m` was false for `m = 10`. However, *some* messages ARE fixed points of textbook RSA (e.g. `m = 0, 1`, and `m ≡ ±1`), and with `e` self-inverse mod `φ(n)` here, encryption and decryption use the *same* exponent. This is a flaw of **textbook RSA / chosen parameters**, not the underlying math: tiny `n`, deterministic encryption, and structured messages are exactly why the lecture says **textbook RSA is insecure** and must be combined with padding/hashing such as **RSA-OAEP** (L09 p.35, E09 p.1).

### [VERY HARD] A vendor proposes a "stream OTP" that derives a 256-bit key from a password and reuses that same key to XOR-encrypt every message. Two intercepted ciphertexts are `C1 = P1 ⊕ K` and `C2 = P2 ⊕ K`. Show what `C1 ⊕ C2` reveals, why this destroys OTP's perfect secrecy, and which lecture rules are broken.
**Answer:** OTP gives perfect (information-theoretic) secrecy *only* when the key is truly random, at least as long as the message, and **never reused** (L09 p.22–23). XOR the two ciphertexts — the shared key `K` cancels because `K ⊕ K = 0`:

```
C1 ⊕ C2 = (P1 ⊕ K) ⊕ (P2 ⊕ K)
        = P1 ⊕ P2 ⊕ (K ⊕ K)
        = P1 ⊕ P2 ⊕ 0
        = P1 ⊕ P2
```

The attacker now holds `P1 ⊕ P2` — the **XOR of the two plaintexts**, with the key entirely removed. This leaks real information (e.g. where the plaintexts agree the result is 0), and with any crib or known plaintext `P1`, the other follows instantly: `P2 = (C1 ⊕ C2) ⊕ P1`. Numeric illustration with one byte, `K = 0xAA`:

```
P1 = 'H' = 0x48 → C1 = 0x48 ⊕ 0xAA = 0xE2
P2 = 'I' = 0x49 → C2 = 0x49 ⊕ 0xAA = 0xE3
C1 ⊕ C2 = 0xE2 ⊕ 0xE3 = 0x01 = 0x48 ⊕ 0x49   (= P1 ⊕ P2, K gone)
```

**Rules broken:** (1) the key is *reused* across messages — the lecture's explicit "the key must not be reused" (L09 p.23); (2) a password-derived key is *not* truly random and is *shorter* than the combined message stream, violating "the key must be equal to or longer than the plaintext" and "randomly generated" (L09 p.22). Any one of these voids the perfect-secrecy guarantee — what remains is no longer a One Time Pad but a reused keystream, trivially attackable.

### [VERY HARD] An RSA key uses a 2048-bit modulus. Explain, with order-of-magnitude reasoning, why brute-forcing the *private key directly* (guessing `d`) is hopeless — and clarify why this brute-force estimate is NOT actually how RSA would be attacked, per the lecture.
**Answer:** Two separate points — the brute-force bound, then the real attack surface.

**Brute force on `d`.** With a 2048-bit modulus, `d` is an integer up to roughly `n ≈ 2^2048`. Even an absurdly fast attacker at `2^60` guesses/second would need:

```
2^2048 / 2^60 = 2^1988 seconds
1 year ≈ 2^25 seconds (≈ 3.15×10^7 s)
years ≈ 2^1988 / 2^25 = 2^1963
```

For scale, `2^1963` dwarfs the number of atoms in the observable universe (`≈ 2^266`) by hundreds of orders of magnitude. Compare the lecture's modest 80-bit *symmetric* example: `2^80/2^30 = 2^50 s ≈ 35.7 million years` on one PC (E09 Ex4, cookbook H) — and 2048-bit `d` is astronomically beyond even that. So guessing `d` is utterly infeasible.

**The catch (lecture point).** RSA is **not** designed to be attacked by guessing `d`, and a key isn't "2048 bits of brute-force strength." Its security is tied to the difficulty of **factoring `n = pq`** (L09 p.35). If an attacker factors `n` into `p` and `q`, they compute `φ(n) = (p−1)(q−1)` and then `d = e^(−1) mod φ(n)` *directly* — no search at all (exactly the method used in the small-`n` HARD problem above). 2048 bits is chosen so that *factoring* `n` (using algorithms far better than trial division, like the number field sieve) stays infeasible — the bit length resists factoring, not naive key search. The lecture also stresses textbook RSA still needs padding/hashing (RSA-OAEP) on top, since key size alone does not make it secure (L09 p.35, E09 p.1).

### [VERY HARD] An ElGamal public key is `(p, g, h) = (11, 2, 3)` with `g = 2` a generator of `ℤ*_11`. You intercept the ciphertext `(c1, c2) = (5, 6)`. Recover the secret key `x` by solving the small discrete log, then decrypt to find `m`. Explain which underlying hard problem you just (illegitimately) solved.
**Answer:** ElGamal's secret key satisfies `h = g^x mod p`, and recovering `x` from `h` is the **discrete-logarithm problem** — infeasible for large `p`, but solvable by a tiny table here (L09 p.38–40, p.183). Tabulate powers of `g = 2 mod 11`:

```
2^1=2  2^2=4  2^3=8  2^4=5  2^5=10
2^6=9  2^7=7  2^8=3  2^9=6  2^10=1
```

`h = 3` appears at exponent 8, so the secret key is **`x = 8`**. Now decrypt with `s = c1^x mod p`, then `m = c2·s^(−1) mod p` (L09 p.40):

```
s = 5^8 mod 11:
  5^2 = 25 ≡ 3 ; 5^4 = 3^2 = 9 ; 5^8 = 9^2 = 81 ≡ 81 − 7·11 = 4
  → s = 4
s^(−1) mod 11: 4·3 = 12 ≡ 1   →  s^(−1) = 3
m = c2·s^(−1) = 6·3 = 18 ≡ 18 − 11 = 7
```

**`x = 8`, `s = 4`, `m = 7`.** The break worked only because `p = 11` makes the discrete log a trivial lookup. With a real prime (hundreds of digits), computing `x` from `h = g^x mod p` is the intractable **discrete-logarithm problem** that ElGamal's security rests on — the analogue of factoring `n` for RSA (L09 p.40 note on hardness; contrast L09 p.35).
