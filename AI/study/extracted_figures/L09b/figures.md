# L09b — Figure Catalogue

This file catalogues every figure extracted from
`Lecture9-Hidden Markov Models.pdf` (52 slides).

## Extraction method

The lecture PDF embeds ~430 image objects, but the vast majority are
per-character glyph fragments inside the lecturer's title artwork, slide
ornaments, and tables-as-images (each character of a probability table is
sometimes stored as its own image object). These individual images are not
informative on their own.

Instead, we used `fitz.Page.get_pixmap(dpi=160)` to render every slide as a
PNG. This preserves the original slide layout (text + math + diagram + tables)
as a coherent unit and is the most reliable representation of the lecture's
visual content. Tagged `EXTRACTION_METHOD: page-render` for every figure
below.

After curation the directory contains 52 `pageNN-render.png` files, one per
slide, plus this catalogue.

## Verdict legend

- **USE** — embedded in the chapter `.md` as a figure.
- **REWORK** — embedded in the chapter AND supplemented with a Mermaid diagram
  or prose description.
- **SKIP** — not embedded; rationale given.

## Per-slide catalogue

| File | Source slide | Caption / contents | Verdict | Rationale |
|---|---|---|---|---|
| `page01-render.png` | 1 | Title slide: "Hidden Markov Models", Serkan Ayvaz, attribution to Jurafsky & Martin. | SKIP | Title-only slide; no informative content. |
| `page02-render.png` | 2 | Text definition: HMM = priors + transition model + observation model; stationary process assumption. | SKIP | Pure text; reproduced as prose in §1 and §3.1 of the chapter. |
| `page03-render.png` | 3 | Noisy Channel Model — generic illustration with a speech waveform. | SKIP | Illustration is purely motivational; chapter motivates HMMs in §1 with the same idea in prose. |
| `page04-render.png` | 4 | Noisy Channel Model (II) — defines `O = o1..ot`, `W = w1..wn`. | SKIP | Pure text; reproduced verbatim as a definition in §1. |
| `page05-render.png` | 5 | Noisy Channel Model (III): `Ŵ = argmax P(O|W) P(W)` derivation using Bayes' rule. | USE | Foundational motivation slide; embedded in §1. |
| `page06-render.png` | 6 | Toward HMMs: WFSA definition. | SKIP | Pure text; covered in §3.2 prose. |
| `page07-render.png` | 7 | Markov chain for weather — 5-state graph (Start, HOT, COLD, WARM, End) with generic `a_ij` arc labels. | USE | First concrete Markov-chain visual; embedded in §3.2. |
| `page08-render.png` | 8 | Markov chain for words — generic state diagram with NLP states. | SKIP | Redundant with weather chain; same structure illustrated differently. |
| `page09-render.png` | 9 | Definition slide: Markov chain = first-order observable Markov model; lists Q, A; sum constraints. | USE | Mathematical definition slide; embedded in §3.2. |
| `page10-render.png` | 10 | Markov Assumption: `P(q_i | q_1..q_{i-1}) = P(q_i | q_{i-1})`. | USE | Embedded in §3.2 next to the definition. |
| `page11-render.png` | 11 | Initial probability vector `π_i = P(q_1 = i)`; constraint `Σπ_j = 1`. | USE | Embedded in §3.2 alongside the definition of π. |
| `page12-render.png` | 12 | Weather Markov chain redrawn with explicit π (initial-distribution arrows replacing the Start node). | SKIP | Redundant with `page13-render.png` which shows the specific numeric example used throughout the chapter. |
| `page13-render.png` | 13 | Weather Markov chain — **specific example**: HOT, COLD, WARM with transition probabilities .5/.5/.6 self-loops, .2/.3/.3/.2/.1/.3 cross-edges, π = [.5, .3, .2]. | USE | This is THE numeric example used in §5 Worked Example A; embedded in §3.2 and §5.1. |
| `page14-render.png` | 14 | Worked example: P(WARM,WARM,WARM,WARM) = π_3 · a_33^3 = 0.2 × 0.6^3 = 0.0432. | USE | Worked example for a Markov chain; embedded in §5.1. |
| `page15-render.png` | 15 | "How about?" Hot hot hot hot vs. Cold hot cold hot — discussion prompt. | SKIP | Discussion prompt without numeric answer; mentioned briefly in §5.1. |
| `page16-render.png` | 16 | "For Markov chains, output = states" → motivation for HMMs (POS tags, NER). | SKIP | Pure text bridge; covered in §1 motivation. |
| `page17-render.png` | 17 | **HMM (HMM) — formal parameter table**: Q, A, O, B, q0/qF with definitions. | USE | The canonical HMM-parameter slide; embedded in §3.3. |
| `page18-render.png` | 18 | HMM Assumptions: Markov assumption + output-independence assumption. | USE | Embedded in §3.3 immediately after the parameter table. |
| `page19-render.png` | 19 | Fair Bet Casino — narrative setup: Fair coin (½/½), Biased coin (¾ heads). | USE | First HMM example; embedded in §5.2. |
| `page20-render.png` | 20 | Fair Bet Casino Problem — formal: input/output, emission probabilities, 10% switch rate. | USE | Embedded in §5.2. |
| `page21-render.png` | 21 | P(o\|fair) vs P(o\|biased) — formulas if dealer never switches. | USE | Embedded in §5.2 (subsection "Why we need transitions"). |
| `page22-render.png` | 22 | Why "Hidden"? — defines Σ, Q for HMMs in general. | USE | Embedded in §3.3 (definition of hidden state). |
| `page23-render.png` | 23 | HMM Parameters for Fair Bet Casino — A matrix (.9/.1/.1/.9) and B matrix (½/½ for Fair, ¼/¾ for Biased). | USE | Embedded in §5.2. |
| `page24-render.png` | 24 | Same A and B as tables. | SKIP | Redundant with page23; same content in table form. |
| `page25-render.png` | 25 | Hidden path example: path q = FFFBBBBBFFF, o = 01011101001, per-step transition and emission probabilities. | USE | Worked example; embedded in §5.2. |
| `page26-render.png` | 26 | Ice cream example narrative: climatologist in 2799, Jason Eisner's diary. | USE | Embedded in §5.3 narrative. |
| `page27-render.png` | 27 | Eisner task: given ice-cream sequence 1,2,3,2,2,2,3,...; produce weather sequence H,C,H,H,H,C,... | USE | Embedded in §5.3. |
| `page28-render.png` | 28 | **HMM for ice cream** — diagram: start → HOT (.8) or COLD (.2); HOT↔COLD transitions .7/.3/.4/.6; emission tables B_1, B_2 for P(k\|HOT) and P(k\|COLD). | USE | This is THE canonical ice-cream HMM diagram referenced throughout §5.3, §5.4 (forward), §5.5 (Viterbi); embedded in §3.3 and §5.3. |
| `page29-render.png` | 29 | The Three Basic Problems for HMMs — Evaluation, Decoding, Learning. | USE | Embedded in §4 (Algorithms / Methods overview). |
| `page30-render.png` | 30 | Problem 1 statement with HMM diagram restated; "How likely is the sequence 3 1 3?" | USE | Embedded in §4.1 / §5.4. |
| `page31-render.png` | 31 | How to compute likelihood — pivot from Markov chain to HMM; introduces P(3 1 3 \| H H C). | USE | Embedded in §5.4. |
| `page32-render.png` | 32 | Computing likelihood of 3 1 3 given H H C: P(O\|Q) = ∏ P(o_i\|q_i) with worked values .4 × .2 × .1. | USE | Embedded in §5.4. |
| `page33-render.png` | 33 | Joint P(O,Q) = ∏ P(o_i\|q_i) × ∏ P(q_i\|q_{i-1}) with worked values for 3 1 3 H H C. | USE | Embedded in §5.4. |
| `page34-render.png` | 34 | Total likelihood = sum over all hidden paths; brute-force is O(N^T). | USE | Embedded in §4.1 / §5.4. |
| `page35-render.png` | 35 | "Instead: the Forward algorithm" — dynamic programming intuition; O(N²T). | USE | Embedded in §4.2. |
| `page36-render.png` | 36 | Forward Algorithm — recursive definition of α_t(j) = P(o_1..o_t, q_t = j \| λ). | USE | Embedded in §4.2 (key definition). |
| `page37-render.png` | 37 | **Forward Recursion**: Initialization α_1(j) = π_j b_j(o_1), Recursion α_t(j) = Σ_i α_{t-1}(i) a_ij b_j(o_t), Termination P(O\|λ) = Σ_i α_T(i). | USE | THE forward-algorithm formula slide; embedded in §4.2. |
| `page38-render.png` | 38 | **Forward Trellis** — fully worked diagram on 3 1 3 with α values: α_1(C)=.02, α_1(H)=.32, α_2(H) = .32·.14 + .02·.08 = 0.0464, α_2(C) = .054, with all transition and emission weights labeled. | USE | THE worked-out forward trellis; embedded in §5.4. |
| `page39-render.png` | 39 | Same forward trellis (slightly different layout). | SKIP | Redundant with page 38. |
| `page40-render.png` | 40 | "We update each cell" — trellis with all cells visible. | SKIP | Redundant with page 38. |
| `page41-render.png` | 41 | **Forward Algorithm pseudocode** — full function FORWARD(observations, state-graph) returning forward-prob. | USE | Pseudocode; embedded in §4.2 as a code block. |
| `page42-render.png` | 42 | Repeat of slide 29 (Three Basic Problems). | SKIP | Duplicate. |
| `page43-render.png` | 43 | Repeat of slide 28 (HMM for ice cream) introducing the decoding section. | SKIP | Duplicate of page 28. |
| `page44-render.png` | 44 | Decoding Problem statement: find argmax_q P(o\|q) via Viterbi; example "find best hidden path for 3 1 3". | USE | Embedded in §4.3. |
| `page45-render.png` | 45 | Naive O(N^T) vs Viterbi DP. | USE | Embedded in §4.3. |
| `page46-render.png` | 46 | Viterbi intuition — joint probability of observation sequence with the best state sequence. | SKIP | Text-only; covered in §4.3 prose. |
| `page47-render.png` | 47 | **Viterbi intuition (II)** — each cell `v_t(j) = max_i v_{t-1}(i) a_ij b_j(o_t)`. | USE | Embedded in §4.3 (key recursion). |
| `page48-render.png` | 48 | **Viterbi Recursion**: Initialization v_1(j) = π_j b_j(o_1), bt_1(j) = 0; Recursion v_t(j) = max_i v_{t-1}(i) a_ij b_j(o_t), bt_t(j) = argmax_i ...; Termination P* = max_i v_T(i), q_T* = argmax_i v_T(i). | USE | THE Viterbi formula slide; embedded in §4.3. |
| `page49-render.png` | 49 | **Viterbi Algorithm pseudocode** — full function VITERBI(observations, state-graph) returning best-path, path-prob. | USE | Pseudocode; embedded in §4.3 as code block. |
| `page50-render.png` | 50 | **Viterbi trellis** worked on 3 1 3: v_1(H) = .32, v_1(C) = .02, v_2(H) = max(.32·.14, .02·.08) = 0.0448, v_2(C) = .048. | USE | THE worked Viterbi trellis; embedded in §5.5. |
| `page51-render.png` | 51 | **Viterbi backtrace** — same trellis with the bold best-path arrows highlighted. | USE | Embedded in §5.5 to show the backtrace step. |
| `page52-render.png` | 52 | "Thank you for your attention". | SKIP | Closing slide; no content. |

## Coverage summary

- 52 page renders catalogued.
- 32 embedded as USE (including 3 figure-pairs where the same diagram appears
  in both a definition section and a worked-example section).
- 20 SKIP, all justified (duplicates, title/closing slides, or pure text
  already reproduced verbatim in the chapter prose).
- No REWORK figures — page-render quality is sufficient and the chapter
  supplements each diagram with explanatory prose anyway.

No informative figure from the source PDF was dropped.
