# L09a Bayesian Networks — Figure Catalogue

This file catalogues every image and page-render extracted from
`Lecture9-Bayesian Networks.pdf` (67 slides, by Serkan Ayvaz). Two extraction
methods were used:

1. **Image extraction** (`PyMuPDF.Document.extract_image`) — embedded raster
   images (decorative photos, the few diagrams that were inserted as bitmaps,
   slide ornaments).
2. **Page render** (`PyMuPDF.Page.get_pixmap(dpi=200)`) — used for slides whose
   *content* is a composite of vector text + drawn boxes + tables (e.g. all
   the Bayesian-network diagrams with their CPTs). The native PowerPoint
   shapes are not extractable as separate images, so we render the whole
   slide.

Both kinds of files live in this directory:
- `fig{NN}-xref{X}-slide{S}.{ext}` — embedded raster images.
- `page{SS}-{slug}.png` — page-render fallbacks.

Verdict legend: **USE** (embed as-is), **REWORK** (embed + add Mermaid /
prose), **SKIP** (decorative / redundant; not embedded in the chapter).

---

## Embedded raster images

| # | File | Slide | Size | Verdict | Context / rationale |
|---|---|---|---|---|---|
| 1 | `fig01-xref9-slide1.png` | 1 | 290x161, 527 B | SKIP | Cover-slide ornament (tiny). Decorative; nothing for a student to learn from. |
| 2 | `fig02-xref25-slide2.jpeg` | 2 | 750x937 | SKIP | Stock photo of an airport/aircraft. Illustrates the "leave for the airport" example but adds no technical content. |
| 3 | `fig03-xref32-slide4.jpeg` | 4 | 1095x1365 | SKIP | Stock photo of coin tosses (frequentism illustration). Decorative. |
| 4 | `fig04-xref57-slide8.jpeg` | 8 | 1127x1407 | SKIP | Stock photo of teeth (toothache/cavity motif). Decorative. |
| 5 | `fig05-xref100-slide20.jpeg` | 20 | 273x293 | SKIP | Portrait of Rev. Thomas Bayes. Historical interest only; small and not on the exam. |
| 6 | `fig06-xref103-slide21.png` | 21 | 1024x127, 915 B | SKIP | Decorative banner / divider. |
| 7 | `fig07-xref107-slide22.jpeg` | 22 | 1095x1365 | SKIP | Stock photo of a wedding (Marie's wedding example). Decorative. |
| 8 | `fig08-xref124-slide26.jpeg` | 26 | 1111x837 | SKIP | Stock illustration for "diagnose from symptoms / classify content". Decorative. |
| 9 | `fig09-xref131-slide29.png` | 29 | 568x627 | REWORK | The Naive-Bayes example training table (Refund / Marital Status / Taxable Income / Class). Useful as the data source for the worked example — embedded via the page render below for higher fidelity. |
| 10 | `fig10-xref133-slide29.png` | 29 | 1024x65, 520 B | SKIP | Slide ornament near the example table. |
| 11 | `fig11-xref137-slide30.jpeg` | 30 | 1110x837 | SKIP | Stock illustration of correlated variables. Decorative. |
| 12 | `fig12-xref165-slide41.jpeg` | 41 | 1220x1024 | SKIP | Stock illustration for the rain/umbrella/traffic conditional-independence example. The diagram on the same slide (rendered below) carries the actual content. |
| 13 | `fig13-xref180-slide48.png` | 48 | 1079x81, 633 B | SKIP | Slide ornament. |
| 14 | `fig14-xref182-slide48.png` | 48 | 1403x72 | SKIP | Slide ornament. |
| 15 | `fig15-xref215-slide63.jpeg` | 63 | 1600x1082 | USE | A real-world Bayes-net diagram (large medical-diagnosis network from the slide "Bayes Nets for Real-world problems can be large"). Worth showing to motivate the scalability discussion in §6 / §4. |
| 16 | `fig16-xref227-slide66.jpeg` | 66 | 1470x321 | SKIP | Summary-slide ornament. |

## Page-render fallbacks (composite slides)

These slides combine vector-drawn DAG nodes, arrows, and CPT tables.
Image-level extraction loses the structure; page-render captures everything.

| # | File | Slide | Verdict | Content / rationale |
|---|---|---|---|---|
| P1 | `page08-atomic-events.png` | 8 | USE | The four atomic events for the (Cavity, Toothache) world. Foundation example for §3.1. |
| P2 | `page09-joint-distribution-table.png` | 9 | USE | First joint distribution table (Cavity, Toothache). Anchors the joint-distribution definition in §3.2. |
| P3 | `page11-marginal-prob-tables.png` | 11 | USE | Joint table with the empty marginal tables side-by-side. Used as the "before" picture of marginalisation. |
| P4 | `page17-conditional-distributions.png` | 17 | USE | All four conditional distributions derived from the (Cavity, Toothache) joint. Reference image for the conditional-distribution definition. |
| P5 | `page18-normalization-trick.png` | 18 | USE | The normalisation-trick worked example: select rows where Cavity=false, renormalise to get P(Toothache \| Cavity=false). |
| P6 | `page24-marie-wedding-bayes-calculation.png` | 24 | USE | Bayes-rule worked calculation for Marie's wedding example. Embedded in §5 worked examples. |
| P7 | `page29-naive-bayes-example.png` | 29 | USE | Full Naive-Bayes training data plus the worked classification for the test record. Embedded in §3 (Naive Bayes) and §5. |
| P8 | `page33-anthrax-bn.png` | 33 | USE | First *intuitive* Bayes-net diagram of the lecture (HasAnthrax causes Cough, Fever, Difficulty Breathing, Wide Mediastinum). Motivates the BN section. |
| P9 | `page34-joint-table-2k.png` | 34 | USE | The "joint distribution has 2^k entries" pain-point table (A, B, C). Motivates the BN factorisation. |
| P10 | `page35-abcd-bayesnet-cpts.png` | 35 | USE | The canonical A→B→{C,D} BN with all CPTs visible. This is the reference network for slides 35–45. Embedded in §3.5 (Bayesian Network definition). |
| P11 | `page36-abcd-bayesnet-structure.png` | 36 | USE | Same network with annotations on parents and the "encodes conditional independence + is a compact joint" framing. |
| P12 | `page37-abcd-bayesnet-cpt-set.png` | 37 | USE | Same network re-shown with explicit "each CPT is P(Xi \| Parents(Xi))". A slight redundancy with P10 but the annotations differ. |
| P13 | `page38-cpt-detail.png` | 38 | USE | Zoom on a single CPT (P(C \| B)) explaining "2^(k+1) entries" and the row-sum-to-1 rule. Anchor image for §3.4 (CPT). |
| P14 | `page39-markov-condition-diagram.png` | 39 | USE | The generic "Markov condition" diagram with a node X, its parents (P1, P2), children (C1, C2), and non-descendants (ND1, ND2). Anchor for §3.6. |
| P15 | `page41-rain-umbrella-traffic-cond-indep.png` | 41 | USE | The Rain → {Umbrella, Traffic} conditional-independence example with the formula U ⟂ T \| R. Anchor analogy for §2. |
| P16 | `page42-joint-from-chain-rule.png` | 42 | USE | The derivation: chain rule + Markov condition ⇒ BN factorisation. Reference math for §4. |
| P17 | `page45-abcd-joint-calculation.png` | 45 | USE | Worked computation of P(A=T, B=T, C=T, D=T) on the A→B→{C,D} network with all CPTs visible. §5 worked example. |
| P18 | `page46-alarm-network-structure.png` | 46 | USE | Alarm-network DAG (Burglary, Earthquake → Alarm → JohnCalls, MaryCalls). Cornerstone example. |
| P19 | `page47-alarm-network-cpts.png` | 47 | USE | Alarm-network DAG with all five CPTs. The "complete" reference for §5 worked example. |
| P20 | `page48-alarm-network-clean.png` | 48 | SKIP | The DAG itself is redundant with P18 (alarm-network structure already embedded). Slide 48's unique content — the factorisation $P(B)P(E)P(A \mid B,E)P(J \mid A)P(M \mid A)$ written out in the network's variables, plus the sample joint $P(+b, \neg e, +a, \neg j, +m)$ — is covered in the chapter's §3.10 (factorisation derivation) and §5.6 (Slide 48 worked sample joint subsection). The page-render image is not embedded; the slide-48 content is reproduced inline. |
| P21 | `page51-lecture-bn-step-add-vars.png` | 51 | USE | Lecture-late example, Step 1: add variables only. Sequence step for §4 ("Building a Bayes Net" algorithm). |
| P22 | `page52-lecture-bn-step-add-links.png` | 52 | USE | Lecture-late example, Step 2: add directed edges. Sequence step for §4. |
| P23 | `page53-lecture-bn-step-add-tables.png` | 53 | USE | Lecture-late example, Step 3: add CPT numbers. Sequence step for §4. |
| P24 | `page55-compute-joint-entry-example.png` | 55 | USE | Computing the joint entry P(S, ~M, L, ~R, T) on the lecture-late network. §5 worked example. |
| P25 | `page56-compute-joint-derivation.png` | 56 | USE | Step-by-step derivation of the joint entry P(T, ~R, L, ~M, S) using the chain rule + conditional independence. §5. |
| P26 | `page58-compute-conditional-from-joint.png` | 58 | USE | The query P(R \| T, ~S) reduced to a sum-and-divide over joint entries. Anchor for §3 / §4 (inference by enumeration). |
| P27 | `page60-compute-conditional-numbers.png` | 60 | USE | Same query annotated with the "4 joint computes / 4 joint computes" cost — primes the NP-completeness discussion. |
| P28 | `page63-large-bayes-nets-realworld.png` | 63 | SKIP | Page render of the same real-world network already captured at higher fidelity by `fig15-xref215-slide63.jpeg`; using the JPEG (USE) avoids redundancy. |

---

## Summary

- Extracted raster images: 16 — of which **1 USE**, 1 REWORK (absorbed into
  page-render P7), 14 SKIP (decorative photos, ornaments, the Bayes portrait).
- Page renders: 28 — of which **26 USE**, 0 REWORK, 2 SKIP (redundant with
  embedded images or content covered inline).
- **Total USE (embedded in the chapter)**: 27 figures, all embedded.
- **No informative figure was dropped**: every BN diagram and every CPT table
  on the slides is captured by at least one USE figure.
- Decorative stock photos (people, weddings, airports, coin tosses, teeth) are
  intentionally SKIP — they convey no exam content.
- Slide 48's unique factorisation content (the formula and the sample joint)
  is reproduced inline in the chapter (§3.10 and §5.6), not embedded as a
  separate image; the page-render of slide 48 is SKIP because the DAG itself
  duplicates P18.
