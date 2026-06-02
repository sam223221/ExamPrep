# `study/lectures/` — Lecture Chapters

This directory contains one Markdown chapter per lecture in the AI exam preparation package. Each chapter is the canonical study-friendly write-up of the corresponding Lecture PDF.

## Files

| File | Lecture | Topic |
|---|---|---|
| `L02-Agents.md` | Lecture 2 | Rational agents, environments, performance measures |
| `L03-Uninformed-Search.md` | Lecture 3 | Uninformed search algorithms (BFS, DFS, UCS, IDS) |
| `L05-Local-Search.md` | Lecture 5 | Local search (hill climbing, simulated annealing, genetic algorithms) |
| `L06-Adversarial-Search.md` | Lecture 6 | Adversarial search (minimax, alpha-beta pruning) |
| `L07-CSP.md` | Lecture 7 | Constraint satisfaction problems |
| `L09a-Bayesian-Networks.md` | Lecture 9a | Probability, conditional independence, Bayesian networks, inference by enumeration, Naive Bayes |
| `L09b-HMM.md` | Lecture 9b | Hidden Markov models |
| `L10-Intro-to-ML.md` | Lecture 10 | Introduction to machine learning |
| `L11-Regression.md` | Lecture 11 | Regression |
| `L12-Clustering.md` | Lecture 12 | Clustering |

## Chapter conventions

Each chapter follows the template defined in `docs/superpowers/specs/2026-05-22-ai-exam-prep-study-package-design.md` §6.1:

1. **Overview & Motivation** — why the topic matters.
2. **The Big Picture — Analogies** — one concrete everyday analogy per major concept, with "where the analogy breaks down" caveats. Concepts in subsequent sections back-link to these.
3. **Core Concepts** — formal definitions, theorems, and derivations.
4. **Algorithms / Methods** — pseudocode and complexity for the procedural content.
5. **Worked Examples** — fully solved instances, with numbers.
6. **Common Pitfalls / Exam Traps** — the mistakes graders see most often.
7. **Connections to Other Lectures** — explicit inputs and outputs.
8. **Cheat-Sheet Summary** — one-page recap for rapid revision.

Figures are embedded from the per-lecture `study/extracted_figures/L{NN}{a,b,...}/` subdirectory; each lecture's `figures.md` catalogue records the USE/REWORK/SKIP verdict per extracted image.

## Recent changes

- **2026-05-23 (Phase 3.2 — PDF rendering):** Ten lecture PDFs generated in-place by `study/render.py` (WeasyPrint primary path). Sizes range 996 KB (L11) to 7155 KB (L09a); every PDF is >50 KB. Markdown source is untouched. PDFs are reproducible — re-running `render.py` overwrites them with identical content (idempotent).
- **2026-05-22 (Round 1 revision):** L09a revised to embed four missing USE figures (page08, page33, page34, page55); add the slide 31–33 anthrax motivating narrative; add §3.9.1 covering chain/fork/collider patterns and explaining-away; rewrite the §3.10 BN-factorisation derivation with a four-step ancestor-decomposition argument; add §2 analogies for Bayes' rule, joint/atomic event, marginal, Markov condition, CPT, chain rule, unconditional independence, prior/posterior/evidence, and random variable; add §3.X back-links to §2 analogies in every subsection; add the slide-48 explicit factorisation; add the canonical $P(+b \mid +j, +m) \approx 0.284$ alarm-network query; add the Gaussian density formula in §3.11; add §4.6 (BN trade-off spectrum) and §4.7 (expert vs data). See `study/_review/L09a/round1/revise-summary.md` for the full change log.
