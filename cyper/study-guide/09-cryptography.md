# 09. Cryptography

> Source material: `L09_cryptography.pdf` (47 slides) and `E09_Cryptography.pdf` (2-page exercise sheet).
> Citations point at the lecture slide page (`L09 p.X`) or the exercise sheet (`E09 p.X`). Anything **not** stated in these two PDFs is flagged explicitly as "not covered in the lecture".

---

## Overview — what this topic covers and why it matters

Cryptography is the part of the course that operates **on the data level**: it provides **secure transmission over insecure channels** and can be used to ensure **confidentiality and integrity** of data (L09 p.46). Where earlier topics (firewalls, IDS, threat modeling, DoS, SQL injection) defended the *system* and the *network*, cryptography protects the *message itself*, so that even an attacker who reads or tampers with traffic cannot understand or undetectably alter it. It sits in the "Bigger Picture" of the course alongside Multi-party Computation and EU Cybersecurity Law (L09 p.2).

The lecture is organized around two families. **Symmetric Key Encryption (SKE)** uses one shared secret key for both encryption and decryption — historical ciphers (Caesar, Vigenère, Enigma), DES, AES, the One Time Pad, and ChaCha20-Poly1305 (L09 p.4, p.6). **Public Key Encryption (PKE)** uses a published public key for encryption and a separate secret key for decryption — RSA and ElGamal (L09 p.4, p.26). The course also covers the move **from classic to modern cryptography** (ad-hoc letter ciphers → scientific, bit-level, openly developed schemes) (L09 p.13) and the **standardization** of schemes (FIPS/NIST, ANSI), including a cautionary example where a standardized scheme was later broken (L09 p.43–44). Mastering this chapter means being able to (a) classify a scheme as symmetric vs asymmetric, (b) state the key facts about DES/AES/RSA/ElGamal/OTP, and (c) actually run the RSA and ElGamal arithmetic by hand — which the exercise sheet directly requires (E09 p.1).

---

## Key Concepts

### Types of cryptography: Symmetric vs Public Key

**What.** The lecture splits cryptography into two top-level types: **Symmetric Key Encryption (SKE)** and **Public Key Encryption (PKE)** (L09 p.4).

- **Symmetric (SKE):** one key is shared and used for *both* encryption and decryption. Examples taught: historical ciphers (Caesar, Vigenère, Enigma), DES, AES, One Time Pad, and ChaCha20-Poly1305 (L09 p.6, p.24).
- **Public Key (PKE):** there is a **public key** that is *published and can be used by anyone* to encrypt, and a separate **secret key** that only the owner holds to decrypt. The lecture's analogy: "once the paddle lock is locked, only the person who owns the secret key can unlock it" (L09 p.27). Examples taught: RSA and ElGamal; also mentioned (not studied) are Digital Signatures, Elliptic Curve Encryption, and Post-quantum cryptography (L09 p.26).

**Why it matters.** Symmetric ciphers are fast but require both parties to already share a secret key — and "it is hard to share the same key" (L09 p.23). Public key schemes solve the key-distribution problem because the encryption key can be made public. (The exercise asks you to compare AES vs RSA on speed/cost — see Q&A — but the *lecture slides themselves* do not give a numeric speed comparison; that is an exercise discussion point, E09 p.1.)

### Historical cipher: Caesar Cipher (monoalphabetic substitution)

**What.** A substitution cipher from ~1st century BC (L09 p.8). The encryption rule is **left-shift the alphabet KEY times**.

**How.**
- Initial alphabet: `ABCDEFGHIJKLMNOPQRSTUVWXYZ`
- Encrypting alphabet (KEY = 3): `XYZABCDEFGHIJKLMNOPQRSTUVW` (L09 p.8)
- KEY = 3 is what Caesar used, but "any number 0 < x < 26 is fine" (L09 p.8).
- Worked slide example (KEY = 3): plaintext `CRYPTOGRAPHY IS FUN` → ciphertext `ZOVMQLDOXMEV FP CRK` (L09 p.8).

**Why it matters.** It is a **monoalphabetic substitution cipher** — every plaintext letter always maps to the same ciphertext letter (L09 p.11). With only 25 useful keys it is trivially brute-forced (see the cookbook for the full decryption of the exercise ciphertext).

### Historical cipher: Vigenère Cipher (polyalphabetic substitution)

**What.** A 16th-century cipher (L09 p.9). The encryption rule uses the **Vigenère table** with a repeating keyword.

**How.** Key = a word, e.g. `CAFE` (you can choose). Write the key repeatedly under the plaintext and look up each pair in the Vigenère table (L09 p.9):

```
Plaintext:  C R Y P T O G R A P H Y ...
Key:        C A F E C A F E C A F E ...
Ciphertext: E R D T V O K V C P M C ...   (slide example, L09 p.9)
```

**Why it matters.** Because the same plaintext letter can encrypt to *different* ciphertext letters depending on its position under the key, Vigenère is a **polyalphabetic substitution cipher** (L09 p.11). This frustrates the simple letter-frequency analysis that breaks Caesar.

### Historical cipher: Enigma

**What.** An electromechanical cipher machine, ~1918–1940s, used mostly during WWII (L09 p.10). The encryption rule is "use the Enigma machine"; the **key is the combination of rotors and plugboard** settings (L09 p.10).

**Why it matters / trivia.** It is also a (poly­alphabetic) substitution cipher (L09 p.11). The lecture notes an Enigma machine sold for €487,000 at a 2025 French auction, and that the 2014 film *The Imitation Game* depicts **Alan Turing**, who broke Enigma (L09 p.10).

### Substitution ciphers in general

**What.** Caesar, Vigenère, and Enigma are all **substitution ciphers**: the input plaintext (alphabet) is substituted under certain rules (L09 p.11).

- **Monoalphabetic** substitution: Caesar (one fixed mapping for the whole message).
- **Polyalphabetic** substitution: Vigenère, Enigma (the mapping changes through the message).

**Key design lesson.** "Complex and well-distributed substitution is necessary" — i.e. a good cipher needs the substitution to be complicated and to spread/mix data evenly (L09 p.11). This idea reappears in AES, whose substitution is "well-thought-out to be distributed randomly" (L09 p.19).

### From classic to modern cryptography

**What changed.** Modern cryptography (L09 p.13–14):
- Moved from **ad-hoc designs** to a more **scientific approach**.
- Works with **bits and bytes**, not letters/alphabets.
- Is developed **in the open** (to a large degree).
- Intersects mathematics, theoretical CS, software & hardware engineering; is practiced in academia, industry, and intelligence services; and continuously develops new areas and applications (L09 p.14).

**Why it matters.** This is the conceptual bridge from toy letter ciphers to DES/AES/RSA. The takeaway for the exam: modern schemes are designed against *known attack classes* and published for public scrutiny rather than relying on secrecy of the algorithm.

### DES (Data Encryption Standard)

**What / facts to memorize (L09 p.16):**
- **64-bit input** and **64-bit output** (a block cipher with a 64-bit block).
- **64-bit key = 56 effective bits + 8 parity bits.**
- **16 rounds.**
- Uses **F = the Feistel function** = Substitution + Permutation + other operations, "which mixes the data".
- Its **short key length allows an attack** (L09 p.16).

**Why it is no longer secure (L09 p.17):**
- **Late 1980s:** *Differential cryptanalysis* re-discovered by **Biham and Shamir** (IBM and NSA already knew the attack and kept it secret).
- **1994:** *Linear cryptanalysis* (a more efficient attack) by **Mitsuru Matsui**.
- **2000:** a variant of linear cryptanalysis using *less data* by **Knudsen and Mathiassen** (Prof. Lars Ramkilde Knudsen at SDU teaches the MSc "Cryptology" course).

**Why it matters.** DES is the canonical example of a once-standard cipher killed by (a) a too-short key (brute-force) and (b) cryptanalytic attacks. It motivates AES.

### AES (Advanced Encryption Standard)

**What / facts to memorize (L09 p.19):**
- **128-bit input** and **128-bit output** (128-bit block).
- **128-bit key** (options: **192 or 256 bits**).
- Original name **Rijndael**, invented by **Rijmen and Daemen**.
- **10 rounds.**
- Specifically **constructed to avoid differential and linear cryptanalysis** (the very attacks that broke DES).
- Its **substitution is well-thought-out to be distributed randomly** (L09 p.19).

**Why it is "not broken… yet" (L09 p.20):**
- Key length is 128 bits (nicely long) → brute force is infeasible.
- The substitution operations mix the data well, making the protocol stronger.
- **No attacks are known.** "You can become famous if you find an attack on AES."

**Standardization (L09 p.43):** AES was standardized / FIPS-approved in **2002** under **FIPS PUB 197**. During the process **15 designs were submitted**, **5 finalists** were selected, and the **runner-up was Serpent** (by Anderson, Biham, and Knudsen).

### One Time Pad (OTP)

**What / facts (L09 p.22):**
- Provides **perfect secrecy = information-theoretic security** — "one of the most secure protocols when the key is randomly generated."
- The **key must be equal to or longer than the plaintext.**
- Encryption is **bitwise XOR** of plaintext and key:

```
Plaintext:  1001011…0001011
Key:        1100010…0101110
———————————————————————————(xor)
Ciphertext: 0101001…0100101     (L09 p.22)
```

**Critical rules / context (L09 p.23):**
- **The key must not be reused.**
- Hard to share the key, but "once 2 people have the same key, OTP is the most secure way to communicate."
- Historically used for the (Telegram) **hotline between Moscow and Washington, D.C. in the 1960s.**
- The OTP idea is reused in **multi-party computation** (next week's topic).

**Why it matters.** OTP is the theoretical gold standard ("most safest", L09 p.6/p.24) — *unconditionally* secure, not merely computationally secure — but is impractical because of the long, single-use, securely-shared key.

### ChaCha20-Poly1305

**What.** A modern symmetric scheme listed alongside the historical ciphers, DES, AES, and OTP (L09 p.6, p.24). The lecture states it is **used in the modern internet: TLS/HTTPS, VPN, SSH, and mobile networks** (L09 p.6, p.24). The slides give no further internal detail — that is all the lecture says about it.

### Public Key Encryption (concept)

**What.** PKE uses a **public key** (published, usable by anyone, for encryption) and a **secret key** (held only by the owner, for decryption) (L09 p.27). Analogy: a padlock anyone can snap shut, but only the secret-key holder can open (L09 p.27).

**Schemes taught:** RSA and ElGamal. Mentioned but **not studied** this lecture: Digital Signatures, Elliptic Curve Encryption, Post-quantum cryptography (L09 p.26).

> Note: the lecture does **not** give a worked treatment of **Diffie-Hellman key exchange**, **hashing algorithms**, or **digital signatures** beyond *naming* digital signatures as "more (we don't study today)" (L09 p.26). ElGamal's structure does rest on the same discrete-log / `g^x mod p` idea that underlies Diffie-Hellman, but DH itself is not presented. Treat DH/hashing/signatures as **not covered in depth** by this lecture.

### RSA

**Who / history (L09 p.29):** Invented by **Rivest, Shamir, and Adleman** in **1977**; they won the **ACM Turing Award in 2002**. (Shamir also invented Shamir Secret Sharing, used in multi-party computation.)

**The scheme (Textbook RSA), step labels from the slides (L09 p.30–34):**
1. ① Pick two primes `p`, `q` (lecture: `p=11, q=13`).
2. ② Compute `n = pq` (`= 143`).
3. ③ Compute Euler's function `φ(n) = (p−1)(q−1)` (`= 10×12 = 120`).
4. ④ Pick public value `e` under a certain rule (`e = 7`).
5. ⑤ Obtain `d` with `ed ≡ 1 (mod φ(n))` (`d = 103`, since `7×103 = 721 ≡ 1 mod 120`).
6. ⑥ **Public Key `(n, e) = (143, 7)`**; **Secret Key `(n, d) = (143, 103)`**.
7. ⑦ **Encrypt:** `c = m^e mod n`. For `m = 9`: `c = 9^7 mod 143 = 48` (L09 p.32).
8. ⑧ **Decrypt:** `m = c^d mod n`. `48^103 mod 143 = 9` (L09 p.33).

Once steps ①–⑥ are set up, you can run encrypt/decrypt as many times as you like (L09 p.30/34).

**Real-world RSA (L09 p.35):**
- Primes must be **large**, and it must be **hard to factorize `n`**.
- RSA's security is "somewhat related to how difficult it is to factorize `n (= pq)`."
- **Key length is 2048** (bits).
- **Textbook RSA is not secure** even when constructed as above — an additional smart idea must be combined, "such as padding, usage of hash function etc." The exercise hint names **RSA-OAEP** as that idea (E09 p.1).

### ElGamal encryption

**The scheme (Textbook ElGamal), step labels from the slides (L09 p.37–41):**
1. ① Pick a prime `p` (lecture: `p = 23`).
2. ② Choose a **generator** `g` of `ℤ*_p` (`g = 5`).
3. ③ Pick **secret key** `x` (`x = 6`).
4. ④ Compute `h = g^x mod p` (`= 5^6 mod 23 = 8`).
5. ⑤ **Public Key `(p, g, h) = (23, 5, 8)`**; **Secret Key `x = 6`**.
6. ⑥ Encryptor picks **randomness** `k` (`k = 7`).
7. ⑦ **Encrypt** (output the pair `(c1, c2)`):
   - `c1 = g^k mod p = 5^7 mod 23 = 17`
   - `c2 = m · h^k mod p = 9 · 8^7 mod 23 = 16` (for plaintext `m = 9`)
8. ⑧ **Decrypt:**
   - `s = c1^x mod p = 17^6 mod 23 = 12`
   - `m = c2 · s^(−1) mod p = 16 · 2 mod 23 = 9` (using the fact `12^(−1) ≡ 2 (mod 23)`) (L09 p.40).

**Why it matters / how it differs from RSA.** ElGamal is **randomized**: the same plaintext encrypts to different ciphertexts each run because of the fresh randomness `k`, and the ciphertext is a **pair `(c1, c2)`** that is twice the size of the message. RSA (textbook) is **deterministic** (same `m` → same `c`) and outputs a single value. RSA's hardness rests on **integer factorization** of `n`; ElGamal's rests on the **discrete logarithm / `g^x mod p`** problem. (The exercise asks you to argue this difference, E09 p.1.)

### Standardization of cryptographic schemes

**What (L09 p.43):** Popular schemes are standardized, e.g. **FIPS by NIST**, and **ANSI**. AES was FIPS-approved in 2002 (FIPS PUB 197) after a 15-design / 5-finalist competition (runner-up: Serpent).

**It is not always perfect (L09 p.44):**
- **EAX′ (EAXprime)** was standardized in **ANSI C12.22** for transporting electricity-meter data over a network.
- In **2012**, **Minematsu, Lucks, Morita, and Iwata broke EAX′** and warned against using the vulnerable protocol. (Hiraku Morita is the lecturer.)
- **Iwata** is famous for **CMAC**, standardized in **NIST SP 800-38B (2005)**; CMAC is used in low-power devices and wireless protocols like **WiFi and Bluetooth**.

**Why it matters.** Standardization gives interoperability and public vetting, but a standardized scheme is not automatically unbreakable forever — EAX′ is the worked counterexample.

---

## Glossary

- **Cryptography** — techniques working on the data level for secure transmission over insecure channels, ensuring confidentiality and integrity (L09 p.46).
- **Symmetric Key Encryption (SKE)** — encryption where one shared secret key is used for both encrypting and decrypting (L09 p.4, p.6).
- **Public Key Encryption (PKE)** — encryption with a published public key (anyone can encrypt) and a separate secret key (only the owner can decrypt) (L09 p.4, p.27).
- **Substitution cipher** — a cipher where the plaintext alphabet is replaced under certain rules; Caesar, Vigenère, Enigma are examples (L09 p.11).
- **Monoalphabetic substitution** — one fixed letter-to-letter mapping for the whole message (e.g. Caesar) (L09 p.11).
- **Polyalphabetic substitution** — the mapping varies through the message (e.g. Vigenère, Enigma) (L09 p.11).
- **Caesar cipher** — left-shift the alphabet by KEY positions; Caesar used KEY=3, any `0 < x < 26` works (L09 p.8).
- **Vigenère cipher** — polyalphabetic cipher using a keyword and the Vigenère table (L09 p.9).
- **Enigma** — WWII-era electromechanical cipher machine; key = rotor + plugboard combination (L09 p.10).
- **Key** — for Caesar a shift amount; for Vigenère a keyword; for Enigma rotor/plugboard settings; for DES/AES a bit string; for RSA/ElGamal the (public, secret) key pair.
- **DES (Data Encryption Standard)** — 64-bit block cipher, 64-bit key (56 effective + 8 parity), 16 Feistel rounds; insecure due to short key and cryptanalysis (L09 p.16–17).
- **Feistel function (F)** — DES's round function = substitution + permutation + other operations that mix the data (L09 p.16).
- **Differential cryptanalysis** — attack re-discovered by Biham and Shamir in the late 1980s; AES is designed to resist it (L09 p.17, p.19).
- **Linear cryptanalysis** — more efficient attack by Matsui (1994); AES is designed to resist it (L09 p.17, p.19).
- **AES (Advanced Encryption Standard / Rijndael)** — 128-bit block, 128/192/256-bit key, 10 rounds; designed against differential & linear cryptanalysis; "not broken yet" (L09 p.19–20).
- **One Time Pad (OTP)** — XOR of plaintext with a random key at least as long as the plaintext, never reused; gives perfect/information-theoretic secrecy (L09 p.22–23).
- **Perfect secrecy / information-theoretic security** — security that holds regardless of attacker computing power; provided by OTP with a random key (L09 p.22).
- **ChaCha20-Poly1305** — modern symmetric scheme used in TLS/HTTPS, VPN, SSH, mobile networks (L09 p.6, p.24).
- **RSA** — public-key scheme by Rivest, Shamir, Adleman (1977); encrypt `c = m^e mod n`, decrypt `m = c^d mod n`; security tied to factoring `n = pq` (L09 p.29–35).
- **Euler's totient `φ(n)`** — for `n = pq` (distinct primes), `φ(n) = (p−1)(q−1)`; used to derive RSA's `d` (L09 p.31).
- **Public exponent `e` / private exponent `d`** — RSA values with `ed ≡ 1 (mod φ(n))` (L09 p.31).
- **RSA-OAEP** — the "smart idea" (padding / hash-based) needed to make RSA secure beyond textbook RSA (E09 p.1; cf. L09 p.35).
- **ElGamal encryption** — randomized public-key scheme: `c1 = g^k mod p`, `c2 = m·h^k mod p`, with `h = g^x mod p`; security tied to discrete logarithm (L09 p.37–40).
- **Generator `g` of `ℤ*_p`** — an element whose powers generate the multiplicative group mod `p`; the base for ElGamal (L09 p.38).
- **Randomness `k` (ElGamal)** — a fresh per-encryption value that makes ElGamal probabilistic; can be freely chosen (L09 p.39, E09 p.1).
- **Modular inverse `a^(−1) mod p`** — value with `a · a^(−1) ≡ 1 (mod p)`; used in ElGamal decryption (e.g. `12^(−1) ≡ 2 mod 23`) (L09 p.40).
- **Standardization (FIPS/NIST/ANSI)** — formal approval of schemes; AES = FIPS PUB 197 (2002) (L09 p.43).
- **EAX′ (EAXprime)** — ANSI C12.22 scheme for meter data, broken in 2012 (L09 p.44).
- **CMAC** — message-authentication code standardized in NIST SP 800-38B (2005); used in WiFi/Bluetooth (L09 p.44).

---

## How-To Cookbook

### A. Decrypt a Caesar cipher by brute force (E09 Exercise 1.1)

**Ciphertext:** `IWXH XH P KTGN DAS RXEWTG` — "the key is not 3" (E09 p.1).

**Procedure.**
1. Number the alphabet `A=0 … Z=25`.
2. Decryption is the inverse of left-shift encryption: shift each ciphertext letter *forward* by the trial key (or try every key 1–25).
3. Try keys until readable English appears.

Worked: at decryption shift **11** the text becomes readable:
```
I(8)+11=19→T   W(22)+11=33 mod26=7→H   X(23)+11=34 mod26=8→I   H(7)+11=18→S
```
**Result: `THIS IS A VERY OLD CIPHER`** (key = 11, which is indeed not 3). ✓

### B. Decrypt a monoalphabetic substitution cipher (E09 Exercise 1.2 — the "challenge")

The challenge ciphertext begins `Wpmxdl gfa efhza hs b wpzz, wbmc, bdw ihpdwzaii wbq …` (E09 p.1). It is a **random monoalphabetic substitution** (not a Caesar — the per-letter shifts are not uniform).

**Procedure (frequency / crib analysis).**
1. Note structural cribs: the 3-letter word `gfa` recurs constantly → almost certainly **THE**, so `g→T, f→H, a→E`.
2. The single-letter word `b` → **A**; single `X` → **I**.
3. Propagate these guesses into longer words and fill the rest by matching English words (`wpzz`→`DULL`, `kzhpwi`→`CLOUDS`, `yaad`→`BEEN`, `Fhpia`→`HOUSE`).

**Recovered substitution (plain → cipher):**
```
plain : a b c d e f g h i j k l m n o p q r s t u v w x y z
cipher: b y k w a s l f x ? c z t d h j ? m i g p v e ? q ?
```
**Decrypted plaintext** (the opening of Edgar Allan Poe's *The Fall of the House of Usher*):

> "During the whole of a dull, dark, and soundless day in the autumn of the year, when the clouds hung oppressively low in the heavens, I had been passing alone, on horseback, through a singularly dreary tract of country; and at length found myself, as the shades of the evening drew on, within view of the melancholy House of Usher. I know not how it was — but, with the first glimpse of the building, a sense of insufferable gloom pervaded my spirit."

(The source ciphertext has a tiny typo near the end — `wdw` should encode "ded" in "pervaded"; the intended word is clearly "pervaded".) This illustrates the lecture's point that a monoalphabetic substitution, though it has `26! ≈ 4×10²⁶` keys, falls instantly to frequency analysis because the mapping is fixed (L09 p.11).

### C. RSA key generation + encrypt + decrypt — LECTURE numbers (L09 p.30–34)

**Setup.** `p = 11`, `q = 13`.
1. `n = p·q = 11·13 = 143`.
2. `φ(n) = (p−1)(q−1) = 10·12 = 120`.
3. Choose `e = 7` (must be invertible mod 120; `gcd(7,120)=1` ✓).
4. Find `d` with `7d ≡ 1 (mod 120)`. Try multiples: `7·103 = 721 = 6·120 + 1 = 721`, and `721 mod 120 = 1`. So **`d = 103`**.
5. **Public key `(n,e) = (143, 7)`; secret key `(n,d) = (143, 103)`.**

**Encrypt `m = 9`:** `c = 9^7 mod 143`.
- `9² = 81`
- `9⁴ = 81² = 6561 = 45·143 + 126 → 6561 mod 143 = 126`
- `9⁶ = 9⁴·9² = 126·81 = 10206 = 71·143 + 53 → 53`
- `9⁷ = 9⁶·9 = 53·9 = 477 = 3·143 + 48 → 48`
- **`c = 48`** ✓ (matches L09 p.32).

**Decrypt `c = 48`:** `m = 48^103 mod 143`. Using `ed ≡ 1 (mod 120)` the result must return the plaintext; computing `48^103 mod 143 = 9`. **`m = 9`** ✓ (L09 p.33).

### D. RSA — EXERCISE numbers (E09 Exercise 3.1): `p=5, q=11, e=13, m=9`

1. `n = 5·11 = 55`.
2. `φ(n) = (5−1)(11−1) = 4·10 = 40`.
3. Find `d` with `13d ≡ 1 (mod 40)`. Test `d = 37`: `13·37 = 481 = 12·40 + 1 → 481 mod 40 = 1`. **`d = 37`.**
   - (Quick check via extended Euclid: `13·37 = 481`, `481 − 480 = 1`. ✓)
4. **Encrypt `m = 9`:** `c = 9^13 mod 55`.
   - `9² = 81 ≡ 26`
   - `9⁴ = 26² = 676 ≡ 676 − 12·55 = 676 − 660 = 16`
   - `9⁸ = 16² = 256 ≡ 256 − 4·55 = 256 − 220 = 36`
   - `9^13 = 9⁸·9⁴·9¹ = 36·16·9`. `36·16 = 576 ≡ 576 − 10·55 = 26`; `26·9 = 234 ≡ 234 − 4·55 = 234 − 220 = 14`.
   - **`c = 14`.**
5. **Decrypt `c = 14`:** `m = 14^37 mod 55 = 9`. ✓ (decrypts back to the plaintext).

**Answer:** `d = 37`, `c = 14`, and decryption returns `m = 9`. ✓

### E. ElGamal — LECTURE numbers (L09 p.37–40): `p=23, g=5, x=6, m=9, k=7`

1. `h = g^x mod p = 5^6 mod 23`.
   - `5² = 25 ≡ 2`; `5⁴ = 2² = 4`; `5⁶ = 5⁴·5² = 4·2 = 8`. **`h = 8`.**
2. **Public key `(p,g,h) = (23,5,8)`; secret key `x = 6`.**
3. **Encrypt with `k = 7`:**
   - `c1 = g^k mod p = 5^7 mod 23 = 5⁶·5 = 8·5 = 40 ≡ 40 − 23 = 17`. **`c1 = 17`.**
   - `h^k = 8^7 mod 23`: `8² = 64 ≡ 18`; `8⁴ = 18² = 324 ≡ 324 − 14·23 = 324 − 322 = 2`; `8⁷ = 8⁴·8²·8 = 2·18·8 = 288 ≡ 288 − 12·23 = 288 − 276 = 12`.
   - `c2 = m·h^k mod p = 9·12 = 108 ≡ 108 − 4·23 = 108 − 92 = 16`. **`c2 = 16`.**
   - **Ciphertext `(c1,c2) = (17,16)`** ✓ (L09 p.39).
4. **Decrypt:**
   - `s = c1^x mod p = 17^6 mod 23`. `17 ≡ −6`; `17² ≡ 36 ≡ 13`; `17⁴ ≡ 13² = 169 ≡ 169 − 7·23 = 8`; `17⁶ = 17⁴·17² = 8·13 = 104 ≡ 104 − 4·23 = 12`. **`s = 12`.**
   - `s^(−1) mod 23`: need `12·t ≡ 1`. `12·2 = 24 ≡ 1`, so **`s^(−1) = 2`** (the slide states `12^(−1) ≡ 2 (mod 23)`, L09 p.40).
   - `m = c2·s^(−1) mod p = 16·2 = 32 ≡ 32 − 23 = 9`. **`m = 9`** ✓.

### F. ElGamal — EXERCISE numbers (E09 Exercise 3.2): `p=23, g=5`, choose `x` and `k` freely, `m=10`

Pick `x = 6` (so `h = 8` as above) and `k = 7` (so `5^7 ≡ 17`, `8^7 ≡ 12`).
1. `c1 = 5^7 mod 23 = 17`.
2. `c2 = m·h^k mod p = 10·12 = 120 ≡ 120 − 5·23 = 120 − 115 = 5`. So **`(c1,c2) = (17,5)`.**
3. **Decrypt:** `s = c1^x = 17^6 = 12`; `s^(−1) = 2`; `m = c2·s^(−1) = 5·2 = 10`. ✓ Returns `m = 10`.

*(Any valid `x`, `k` work; this just reuses the lecture's `x=6, k=7` for easy arithmetic. The point is the round-trip recovers `m=10`.)*

### G. Modular exponentiation by square-and-multiply (the technique used above)

To compute `a^b mod n`:
1. Write `b` in binary.
2. Start with `result = 1`. Scan the bits of `b` from most significant to least: square `result` each step, and multiply by `a` whenever the bit is 1, reducing mod `n` every time.
   - Example `9^13 mod 55`, `13 = 1101₂`: `1 → 9 (bit1) → 81≡26 → 26²=16 (bit0, square only) → 16²=36, ·9=26 (bit1)`… combining the precomputed powers gives `14` (see cookbook D). This keeps every intermediate number small.

### H. Estimate brute-force time for an 80-bit key (E09 Exercise 4)

Computer tries `2³⁰` keys/second; key space is `2⁸⁰`.
1. Time to try all keys `= 2⁸⁰ / 2³⁰ = 2⁵⁰` seconds.
2. `2⁵⁰ = 1,125,899,906,842,624 ≈ 1.13×10¹⁵ seconds.`
3. In years: `2⁵⁰ / (60·60·24·365) ≈ 2⁵⁰ / 3.15×10⁷ ≈ 3.57×10⁷ years ≈ 35.7 million years.`
4. **Conservative vs optimistic?** This is an **optimistic** estimate *for the attacker* (i.e. it under-states the real difficulty) because a single machine at `2³⁰` keys/s is slow; real adversaries parallelize across many machines/GPUs/ASICs, and on average you find the key after searching *half* the space (`2⁷⁹`), so a realistic attacker could be far faster than "35.7 M years on one PC" suggests. The huge number nonetheless shows why even an 80-bit key resists a lone computer — and why modern keys (AES-128, RSA-2048) are far larger (L09 p.19, p.35).

### I. One Time Pad encrypt/decrypt (XOR)

1. Generate a random key at least as long as the message; never reuse it (L09 p.22–23).
2. **Encrypt:** `ciphertext = plaintext XOR key`.
3. **Decrypt:** `plaintext = ciphertext XOR key` (XOR is its own inverse).
   - Example bit columns from the slide: `1⊕1=0, 0⊕1=1, 0⊕0=0, 1⊕0=1, …` (L09 p.22).

---

## Exam-Style Q&A

**Q1. State the two top-level types of cryptography in the lecture and the defining difference.**
A. **Symmetric Key Encryption (SKE)** — one shared secret key used for both encryption and decryption (e.g. Caesar, Vigenère, Enigma, DES, AES, OTP, ChaCha20-Poly1305). **Public Key Encryption (PKE)** — a *published* public key encrypts and a separate *secret* key decrypts (e.g. RSA, ElGamal). Difference: SKE shares one secret key (key-distribution problem); PKE makes the encryption key public so anyone can encrypt but only the secret-key owner can decrypt (L09 p.4, p.6, p.27).

**Q2. Decrypt the Caesar ciphertext `IWXH XH P KTGN DAS RXEWTG` (the key is not 3).**
A. Brute-force the 25 shifts. At decryption shift 11 the text reads **`THIS IS A VERY OLD CIPHER`** (key = 11). Because Caesar is a *monoalphabetic* substitution with only 25 keys, brute force is trivial (E09 p.1; method in cookbook A).

**Q3. Compare DES and AES on every parameter the lecture gives.**
A.
| | DES (L09 p.16) | AES (L09 p.19) |
|---|---|---|
| Block (in/out) | 64-bit / 64-bit | 128-bit / 128-bit |
| Key | 64-bit (56 effective + 8 parity) | 128-bit (option 192/256) |
| Rounds | 16 | 10 |
| Round function | Feistel `F` = sub + perm + ops | substitution distributed randomly |
| Status | Insecure — short key + cryptanalysis | "Not broken yet"; no known attacks |
AES was explicitly designed to resist the differential and linear cryptanalysis that broke DES (L09 p.17, p.19).

**Q4. Why is DES no longer secure? List the attacks with dates and people.**
A. (i) Its **key is too short** (56 effective bits), enabling brute force (L09 p.16). (ii) **Differential cryptanalysis** — re-discovered late 1980s by **Biham and Shamir** (IBM/NSA already knew it). (iii) **Linear cryptanalysis** — 1994, **Matsui**, more efficient. (iv) A **variant of linear cryptanalysis using less data** — 2000, **Knudsen and Mathiassen** (L09 p.17).

**Q5. Why is AES "not broken yet"? (an exercise question, E09 Ex2.2)**
A. Three lecture reasons (L09 p.20): its **128-bit key is long enough** to defeat brute force; its **substitution operations mix the data well**, making it stronger; and **no attacks are known**. Additionally AES was *constructed* to avoid differential and linear cryptanalysis (L09 p.19). ("You can become famous if you find an attack on AES.")

**Q6. RSA worked problem (E09 Ex3.1): `p=5, q=11, e=13, m=9`. Find `d`, `c`, and verify decryption.**
A. `n = 55`, `φ(n) = 4·10 = 40`. Solve `13d ≡ 1 (mod 40)` → **`d = 37`** (since `13·37 = 481 = 12·40 + 1`). Encrypt: `c = 9^13 mod 55 = ` … using `9²≡26, 9⁴≡16, 9⁸≡36`, `9^13 = 36·16·9 mod 55 = ` **`14`**. Decrypt: `14^37 mod 55 = 9` ✓. (Full arithmetic in cookbook D.)

**Q7. RSA worked problem (lecture): `p=11, q=13, e=7, m=9`. Show encryption and decryption.**
A. `n = 143`, `φ = 120`, `d = 103` (`7·103 = 721 ≡ 1 mod 120`). `c = 9^7 mod 143 = 48`; `m = 48^103 mod 143 = 9`. Public key `(143,7)`, secret key `(143,103)` (L09 p.30–34; cookbook C).

**Q8. ElGamal worked problem (lecture): `p=23, g=5, x=6, m=9, k=7`. Give `h`, `(c1,c2)`, and decrypt.**
A. `h = 5^6 mod 23 = 8`. `c1 = 5^7 mod 23 = 17`; `c2 = 9·8^7 mod 23 = 9·12 = 16`, so `(c1,c2) = (17,16)`. Decrypt: `s = 17^6 mod 23 = 12`, `s^(−1) = 2`, `m = 16·2 mod 23 = 9` ✓ (L09 p.37–40; cookbook E).

**Q9. ElGamal worked problem (E09 Ex3.2): `p=23, g=5`, choose your own `x`,`k`, `m=10`. Give `(c1,c2)` and decrypt.**
A. Choose `x=6` (→ `h=8`) and `k=7`. `c1 = 5^7 mod 23 = 17`; `c2 = 10·8^7 mod 23 = 10·12 = 120 ≡ 5`, so `(c1,c2) = (17,5)`. Decrypt: `s = 17^6 = 12`, `s^(−1) = 2`, `m = 5·2 mod 23 = 10` ✓ (cookbook F).

**Q10. Explain the difference between RSA and ElGamal encryption (E09 Ex2.3).**
A. **RSA** (textbook) is **deterministic** — same `m` always gives the same `c = m^e mod n`, a single value — and its security rests on the hardness of **factoring `n = pq`** (L09 p.29–35). **ElGamal** is **randomized/probabilistic** — it injects fresh randomness `k` each time, so the same `m` yields different ciphertexts, and the ciphertext is a **pair `(c1,c2)`** (≈ double size); its security rests on the **discrete-logarithm problem** in `ℤ*_p` (`h = g^x mod p`) (L09 p.37–40). (Both are public-key schemes.)

**Q11. What "smart idea" makes RSA actually secure (E09 Ex3.3)?**
A. Textbook RSA is *not* secure on its own; you must add **padding and/or a hash function** before encrypting (L09 p.35). The exercise's hint names this construction **RSA-OAEP** (Optimal Asymmetric Encryption Padding) (E09 p.1). Padding makes encryption probabilistic and removes the algebraic structure attackers exploit in textbook RSA. (The lecture states the *need* for padding/hashing; the specific internals of OAEP are not detailed in the slides.)

**Q12. Brute-forcing an 80-bit key at `2³⁰` keys/s (E09 Ex4): how long, and is it conservative or optimistic?**
A. `2⁸⁰ / 2³⁰ = 2⁵⁰ ≈ 1.13×10¹⁵ s ≈ 35.7 million years` on one machine. It is **optimistic** (it *under*states attacker capability): real attackers parallelize across many machines and find a key after ~half the search (`2⁷⁹`) on average, so the practical effort is much less than "one PC for 35.7 M years." Either way it shows why short keys are dangerous and modern keys are large (cookbook H).

**Q13. What is a One Time Pad and why is it the "most secure"? What are its catches?**
A. OTP XORs the plaintext with a random key at least as long as the message; this gives **perfect secrecy / information-theoretic security** (secure against *any* computing power) (L09 p.22). Catches: the **key must equal or exceed the plaintext length**, **must be truly random**, and **must never be reused**; sharing such a key is hard. It was used for the Moscow–Washington hotline in the 1960s (L09 p.23).

**Q14. Classify Caesar, Vigenère, and Enigma; what design lesson do they teach?**
A. All three are **substitution ciphers**: Caesar is **monoalphabetic**, while Vigenère and Enigma are **polyalphabetic** (L09 p.11). Lesson: "complex and well-distributed substitution is necessary" — a fixed, simple mapping (Caesar) is broken by frequency analysis, which is why modern ciphers like AES use carefully randomized substitution (L09 p.11, p.19).

**Q15. Give an example where a standardized scheme was later broken.**
A. **EAX′ (EAXprime)**, standardized in **ANSI C12.22** for electricity-meter data, was **broken in 2012 by Minematsu, Lucks, Morita, and Iwata**, who warned against using it (L09 p.44). This shows standardization aids interoperability and review but does not guarantee permanent security. (Contrast: AES, FIPS PUB 197 (2002), remains unbroken — L09 p.20, p.43.)

**Q16. Is AES or RSA faster / more computation-costly (E09 Ex2.1)?**
A. The lecture does **not give numbers** for this; it is an exercise discussion point. Grounded reasoning from the slides: AES is a **symmetric** cipher with a short (128-bit) key doing fast bit/byte mixing over 10 rounds (L09 p.19), whereas RSA is **public-key** with a **2048-bit** modulus and modular exponentiation of huge numbers (L09 p.35). General principle: symmetric encryption (AES) is far cheaper/faster than public-key encryption (RSA), which is why real systems use RSA/PKE only to set up a key and then use AES for bulk data. *(Flagged: the speed claim is standard knowledge / exercise reasoning, not a numeric slide statement.)*

---

## Gotchas

- **"The key is not 3" (Caesar).** Don't assume the classic shift of 3 — the exercise deliberately uses a different key (it's 11). Brute-force all shifts (E09 p.1; cookbook A).
- **A substitution cipher is not a Caesar.** The Ex1.2 challenge is a *random* monoalphabetic substitution, so no single shift decodes it — you need frequency/crib analysis (e.g. `gfa`→THE). It decrypts to Poe's *Fall of the House of Usher* (E09 p.1; cookbook B).
- **RSA modulus for exponentiation is `n`, but `d` is computed mod `φ(n)`.** Encrypt/decrypt use `mod n` (`m^e mod n`, `c^d mod n`), while the key relation is `ed ≡ 1 (mod φ(n))`. Mixing up `n` and `φ(n)` is the classic mistake (L09 p.31–33).
- **`φ(n) = (p−1)(q−1)`, not `(p)(q)` or `(p−1)(q)`.** For lecture numbers `10·12=120`; for exercise numbers `4·10=40` (L09 p.31; E09 p.1).
- **DES key size: 56 *effective* + 8 parity = 64.** If asked "key length", note both: stored 64, but only 56 contribute to security — that short length is *why* it's attackable (L09 p.16).
- **AES has 10 rounds for the 128-bit key**; the slide gives 10 rounds with the 128-bit option (192/256 keys exist but the slide's round count is stated for the base case) (L09 p.19).
- **Textbook RSA is insecure.** Even with correctly chosen `p,q,e,d` it must be combined with padding/hashing (RSA-OAEP). Don't write "RSA = `m^e mod n` is secure" — the lecture explicitly says it is not (L09 p.35; E09 p.1).
- **ElGamal needs a modular inverse in decryption.** `m = c2·s^(−1) mod p`, where `s = c1^x mod p`. You must invert `s` (e.g. `12^(−1) ≡ 2 mod 23`), not divide normally (L09 p.40).
- **ElGamal is randomized; RSA (textbook) is deterministic.** Same plaintext → different ElGamal ciphertexts (because of `k`) but identical textbook-RSA ciphertexts. This is the heart of the "difference" exercise question (L09 p.37–40 vs p.30–34).
- **OTP: never reuse the key, and the key must be random and ≥ plaintext length.** Reusing a pad destroys the perfect-secrecy guarantee (L09 p.23).
- **Brute-force estimate is "optimistic," not "conservative."** A lone machine giving "35.7 M years" *understates* a real, parallelized attacker (who also only needs ~half the keyspace on average) (E09 p.2).
- **Not covered in this lecture (don't over-claim on the exam):** Diffie-Hellman key exchange, hashing algorithms, block-cipher modes of operation (ECB/CBC/CTR etc.), and the internals of digital signatures are **not** presented in L09 — digital signatures are only *named* as "we don't study today" (L09 p.26). If a question demands these, state that they were outside this lecture's scope.
