# 09. Cryptography — Commands & Code Examples

### Generate an RSA keypair with OpenSSL
**What:** Create a 2048-bit RSA private key (real-world key length per L09 p.35).
```bash
# (standard syntax)
openssl genrsa -out private.pem 2048      # generate 2048-bit private key
openssl rsa -in private.pem -pubout -out public.pem   # derive the public key
```
**Notes:** L09 p.35 states real RSA uses key length 2048. The private file holds `n,e,d` (and `p,q`); the public file holds only `(n,e)`. Textbook RSA from the lecture uses tiny primes (`p=11,q=13`) — `genrsa` picks large random primes so factoring `n` is infeasible.

### Inspect RSA key components (n, e, d) with OpenSSL
**What:** Dump modulus, public exponent, and private exponent of a key.
```bash
# (standard syntax)
openssl rsa -in private.pem -text -noout
```
**Notes:** Output shows `modulus` (= `n`), `publicExponent` (= `e`, commonly 65537), `privateExponent` (= `d`), plus `prime1/prime2` (= `p,q`). This is the real-tool view of the lecture's `(n,e)` public key and `(n,d)` secret key (L09 p.31, p.34). The relation is always `ed ≡ 1 (mod φ(n))`.

### Encrypt and decrypt a file with an RSA public/secret key
**What:** Public-key encrypt with the public key, decrypt with the private key.
```bash
# (standard syntax)
openssl pkeyutl -encrypt -pubin -inkey public.pem -in msg.txt -out msg.enc
openssl pkeyutl -decrypt -inkey private.pem -in msg.enc -out msg.dec
```
**Notes:** Demonstrates the PKE principle (L09 p.27): anyone with the *public* key can encrypt, only the *secret* key holder can decrypt. By default `openssl pkeyutl -encrypt` uses **PKCS#1 v1.5** padding, NOT OAEP — to get the secure RSA-OAEP padding the lecture recommends (L09 p.35; E09 p.1), add `-pkeyopt rsa_padding_mode:oaep` to BOTH the encrypt and decrypt commands.

### RSA from scratch in Python — lecture numbers (p=11, q=13, e=7, m=9)
**What:** Reproduce the lecture's full RSA round-trip (L09 p.30–34).
```python
def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x, y = egcd(b, a % b)
    return (g, y, x - (a // b) * y)

def modinv(a, m):
    g, x, _ = egcd(a % m, m)
    if g != 1:
        raise ValueError("no inverse")
    return x % m

p, q, e, m = 11, 13, 7, 9
n   = p * q                 # 143
phi = (p - 1) * (q - 1)     # 120
d   = modinv(e, phi)        # 103
c   = pow(m, e, n)          # 48
m2  = pow(c, d, n)          # 9
print(n, phi, d, c, m2)
```
**Notes:** Verified output `143 120 103 48 9`. Matches L09 p.32 (`c = 9^7 mod 143 = 48`) and p.33 (`m = 48^103 mod 143 = 9`). Public key `(143,7)`, secret key `(143,103)`. Gotcha: `d` is found mod `φ(n)=120`, but encrypt/decrypt use mod `n=143` (L09 p.31–33).

### RSA from scratch in Python — exercise numbers (p=5, q=11, e=13, m=9)
**What:** Solve E09 Exercise 3.1: find `d`, the ciphertext, and verify decryption.
```python
p, q, e, m = 5, 11, 13, 9
n   = p * q                 # 55
phi = (p - 1) * (q - 1)     # 40
d   = modinv(e, phi)        # 37
c   = pow(m, e, n)          # 14
m2  = pow(c, d, n)          # 9
print(f"d={d} c={c} dec={m2}")
```
**Notes:** Verified output `d=37 c=14 dec=9`. Check: `13·37 = 481 = 12·40 + 1`, so `481 mod 40 = 1` ✓ (E09 Ex3.1). Reuses `egcd`/`modinv` from the lecture-numbers snippet above.

### Compute the RSA private exponent d by hand (modular inverse)
**What:** Solve `ed ≡ 1 (mod φ(n))` by brute search — the by-hand exam method.
```python
e, phi = 7, 120          # lecture: e=7, phi=120
d = next(d for d in range(1, phi) if (e * d) % phi == 1)
print(d)                 # 103,  since 7*103 = 721 = 6*120 + 1
```
**Notes:** Verified `d = 103`. For the exercise (`e=13, phi=40`) the same loop gives `37`. This is the linear search you do in the margin when no calculator inverse is allowed (L09 p.31; E09 Ex3.1).

### Modular exponentiation in Python (the core RSA/ElGamal operation)
**What:** Compute `a^b mod n` efficiently with the built-in three-arg `pow`.
```python
print(pow(9, 7, 143))    # RSA encrypt m=9 -> 48
print(pow(48, 103, 143)) # RSA decrypt c=48 -> 9
print(pow(5, 7, 23))     # ElGamal c1 -> 17
```
**Notes:** Verified `48`, `9`, `17`. `pow(base, exp, mod)` uses square-and-multiply internally, keeping every intermediate small — the technique used by hand in the study guide (cookbook G). Never compute `9**7` then `% 143` for big exponents; pass the modulus to `pow`.

### Square-and-multiply by hand in Python (show your work)
**What:** Reproduce the manual `9^13 mod 55` computation step by step (E09 Ex3.1).
```python
base, exp, n = 9, 13, 55
result = 1
for bit in bin(exp)[2:]:          # 13 = '1101'
    result = (result * result) % n
    if bit == '1':
        result = (result * base) % n
    print(bit, result)
print("answer", result)           # 14
```
**Notes:** Verified final `answer 14`. Trace matches the guide: `9²≡26, 9⁴≡16, 9⁸≡36`, recombined to `36·16·9 mod 55 = 14`. Scan exponent bits MSB→LSB: square every step, multiply by base on a `1` bit (cookbook D, G).

### ElGamal from scratch in Python — lecture numbers (p=23, g=5, x=6, m=9, k=7)
**What:** Reproduce the lecture's randomized public-key round-trip (L09 p.37–40).
```python
p, g, x, m, k = 23, 5, 6, 9, 7
h    = pow(g, x, p)            # 8   public-key component h = g^x mod p
c1   = pow(g, k, p)            # 17  c1 = g^k mod p
c2   = (m * pow(h, k, p)) % p  # 16  c2 = m * h^k mod p
s    = pow(c1, x, p)           # 12  s  = c1^x mod p
sinv = modinv(s, p)            # 2   s^(-1) mod 23
m2   = (c2 * sinv) % p         # 9   m = c2 * s^(-1) mod p
print(h, (c1, c2), s, sinv, m2)
```
**Notes:** Verified output `8 (17, 16) 12 2 9`. Public key `(p,g,h)=(23,5,8)`, secret key `x=6`. Decryption needs the modular inverse `12^(-1) ≡ 2 (mod 23)` — you invert `s`, never divide (L09 p.40). Reuses `modinv` defined above.

### ElGamal from scratch in Python — exercise numbers (p=23, g=5, m=10)
**What:** Solve E09 Ex3.2 with self-chosen `x=6, k=7` and plaintext `m=10`.
```python
p, g, x, k, m = 23, 5, 6, 7, 10
h    = pow(g, x, p)            # 8
c1   = pow(g, k, p)            # 17
c2   = (m * pow(h, k, p)) % p  # 5
s    = pow(c1, x, p)           # 12
m2   = (c2 * modinv(s, p)) % p # 10
print((c1, c2), m2)
```
**Notes:** Verified output `(17, 5) 10`. `c2 = 10·12 = 120 ≡ 5 (mod 23)`; decrypts back to `10` ✓ (E09 Ex3.2). Any valid `x,k` work; reusing the lecture's keeps arithmetic easy. Because ElGamal is randomized, a different `k` gives a different `(c1,c2)` for the same `m`.

### Find a generator g of Z*_p in Python (ElGamal setup)
**What:** Confirm `g=5` generates the multiplicative group mod 23 (L09 p.38).
```python
p = 23
g = 5
powers = {pow(g, i, p) for i in range(1, p)}
print(len(powers) == p - 1, sorted(powers))
```
**Notes:** Verified `True` with all 22 nonzero residues `1..22` produced — so `5` is a generator of `ℤ*_23`. A generator's powers cycle through every nonzero element mod `p`; that property is what ElGamal's `h = g^x` relies on (L09 p.38).

### Caesar cipher encrypt/decrypt in Python
**What:** Left-shift encryption and its inverse, matching the lecture rule (L09 p.8).
```python
def caesar(text, key, decrypt=False):
    k = key if decrypt else -key       # encrypt = left-shift (subtract)
    out = []
    for ch in text:
        if ch.isalpha():
            out.append(chr((ord(ch.upper()) - 65 + k) % 26 + 65))
        else:
            out.append(ch)
    return "".join(out)

print(caesar("CRYPTOGRAPHY IS FUN", 3))            # encrypt, KEY=3
print(caesar("IWXH XH P KTGN DAS RXEWTG", 11, True))  # decrypt, key=11
```
**Notes:** Verified: encrypt gives `ZOVMQLDOXMEV FP CRK` (exact slide example, L09 p.8); decrypt gives `THIS IS A VERY OLD CIPHER` (E09 Ex1.1 — "the key is not 3", it is 11). Encryption shifts *left* (subtract `key`), decryption shifts *right* (add `key`).

### Brute-force a Caesar cipher (all 25 keys) in Python
**What:** Print every shift so you can eyeball the readable English (E09 Ex1.1).
```python
ct = "IWXH XH P KTGN DAS RXEWTG"
for key in range(1, 26):
    pt = "".join(
        chr((ord(c) - 65 + key) % 26 + 65) if c.isalpha() else c
        for c in ct
    )
    print(key, pt)
```
**Notes:** Key `11` yields `THIS IS A VERY OLD CIPHER`. Caesar is a monoalphabetic substitution with only 25 useful keys, so brute force is trivial (L09 p.11; E09 p.1). Don't assume key 3 — the exercise deliberately picks another.

### One Time Pad encrypt/decrypt by XOR in Python
**What:** XOR plaintext with a same-length random key; XOR again to decrypt (L09 p.22).
```python
import os

msg = b"ATTACK AT DAWN"
key = os.urandom(len(msg))                 # key length >= plaintext, random
ct  = bytes(a ^ b for a, b in zip(msg, key))
pt  = bytes(a ^ b for a, b in zip(ct, key))
print(ct.hex())
print(pt == msg)                           # True
```
**Notes:** Verified `pt == msg` is `True`. XOR is its own inverse, so `ciphertext XOR key = plaintext` (cookbook I). Rules: key must be truly random, at least as long as the message, and NEVER reused — reuse destroys the perfect-secrecy guarantee (L09 p.22–23).

### Estimate brute-force time for an 80-bit key in Python
**What:** Compute years to exhaust 2^80 keys at 2^30 keys/second (E09 Ex4).
```python
keys      = 2**80
rate      = 2**30                 # keys per second
seconds   = keys // rate          # 2^50
years     = seconds / (60 * 60 * 24 * 365)
print(seconds, round(years))      # 1125899906842624  35702052
```
**Notes:** Verified `1125899906842624` seconds ≈ `35,702,052` ≈ 35.7 million years on one machine. This is an *optimistic* estimate (it understates a real attacker): adversaries parallelize and only need ~half the keyspace (`2⁷⁹`) on average (E09 Ex4, cookbook H).

### Symmetric encryption with AES-256-CBC in OpenSSL
**What:** Encrypt/decrypt a file with a single shared key (symmetric / SKE).
```bash
# (standard syntax)
openssl enc -aes-256-cbc -salt -pbkdf2 -in msg.txt -out msg.enc
openssl enc -d -aes-256-cbc -pbkdf2 -in msg.enc -out msg.dec
```
**Notes:** Tooling demo of AES (L09 p.19). `enc` prompts for one passphrase used for *both* directions — the defining trait of symmetric key encryption (L09 p.4, p.6). `-pbkdf2` derives the key from the passphrase. (Mode/internals like CBC are not covered by the lecture — this is just the tool's default; L09 keeps to AES facts, not modes.)

### Hash a file with SHA-256 in OpenSSL
**What:** Produce a fixed-length digest (the "hash function" the lecture references).
```bash
# (standard syntax)
openssl dgst -sha256 msg.txt
```
**Notes:** Standard crypto tooling. The lecture names hashing only as part of the "padding / hash function" idea that hardens textbook RSA into RSA-OAEP (L09 p.35; E09 p.1). It does NOT teach hash internals, so treat this as tooling, not exam theory.

### Generate cryptographic randomness with OpenSSL
**What:** Produce random bytes for keys, OTP pads, or ElGamal's `k`.
```bash
# (standard syntax)
openssl rand -hex 32        # 32 random bytes as hex (256-bit key)
openssl rand -base64 16     # 16 random bytes, base64-encoded
```
**Notes:** OTP requires a truly random key at least as long as the plaintext (L09 p.22); ElGamal needs fresh randomness `k` per encryption (L09 p.39). `openssl rand` is the practical source. Pair with the base64 example below to inspect output as text.

### Base64-encode and decode in Python
**What:** Make raw ciphertext/keys printable and reverse it losslessly.
```python
import base64

raw = b"\x01\x9a\xff hello"
enc = base64.b64encode(raw).decode()   # text-safe representation
dec = base64.b64decode(enc)
print(enc)
print(dec == raw)                      # True
```
**Notes:** Verified `dec == raw` is `True`. Base64 is encoding, NOT encryption — it provides no secrecy. Useful for transporting binary ciphertext (from RSA/AES/OTP above) through text channels; pairs with `openssl rand -base64` and `openssl enc -base64`.

### Generate a GPG keypair and encrypt a message
**What:** Real-world public-key workflow (PKE) with GnuPG.
```bash
# (standard syntax)
gpg --full-generate-key                          # interactive: pick RSA, 2048+ bits
gpg --export -a "Alice" > alice_pub.asc          # share this public key
gpg --encrypt --recipient "Alice" msg.txt        # -> msg.txt.gpg (anyone can do this)
gpg --decrypt msg.txt.gpg > msg.dec              # only Alice's secret key works
```
**Notes:** End-to-end PKE example (L09 p.26–27): the public key is published so anyone can encrypt, but only the secret-key holder decrypts. GPG defaults to a hybrid scheme (public key wraps a random symmetric session key) — the standard reason real systems combine PKE (key setup) with fast symmetric AES for bulk data (cf. E09 Ex2.1).
