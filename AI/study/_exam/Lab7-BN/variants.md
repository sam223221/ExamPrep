# Lab 7 — Bayesian Networks — Variant Bank

Curated exam-style variants for `Lab7/handout/Runner_solution.py`.
Each variant is self-contained: an examiner with access to ONLY the
docstring header + KNOB comments + function signatures must be able to
solve it by changing KNOB values, then running

    py -3.12 Lab7/handout/Runner_solution.py

and reading the printed output.

The reference network is the **Sprinkler net** (Exercise 1, Lab 7.pdf):

    Cloudy --> Sprinkler, Rain
    Sprinkler, Rain --> WetGrass
    Variables: each is binary, values "false" / "true".
    CPTs as given in slide 2 of Lab 7.pdf — see Runner_solution.py.

The homework **Car-diagnosis net** is also wired in (`NETWORK_CHOICE="car"`).

Each variant lists:
- the question verbatim
- the relevant KNOB(s) the examiner should change
- the expected answer / what to look for in the printed output

---

## Variant 1 — Different evidence values

**Question (Sprinkler net).** A neighbour reports that the grass is
**dry** today (WetGrass = false). Given only that observation, what is
the probability that the sprinkler was on (Sprinkler = true)? Report
the probability to 4 decimal places.

**KNOBs to change.**

```python
NETWORK_CHOICE  = "sprinkler"   # already the default
SPRINKLER_EVIDENCE = {"WetGrass": "false"}     # change from "true"
SPRINKLER_QUERY    = {"Sprinkler": "true"}     # already the default
```

**Expected output (exact enumeration).** The line after
`conditional probability of {'Sprinkler': 'true'}` should print
`is 0.062057` (≈ 0.0621). Substantially **lower** than the default
P(S=T | W=T) = **0.4298** — dry grass is evidence AGAINST the
sprinkler having been on.

**Stretch.** Re-run with `SPRINKLER_EVIDENCE = {"Cloudy": "true"}`.
Expected: P(S=T | C=T) = **0.1000** exactly (direct parent → child;
this is the CPT entry P(Sprinkler=T | Cloudy=T) = 0.1).

---

## Variant 2 — Query a different node (and a diagnostic ranking)

**Question (Car-diagnosis net, slide 4 of Lab 7.pdf).** You suspect a
fault in your car. You have noticed **vibrations while driving** and it
is **difficult to reach top speed**. Your car does **not consume more
than usual**. Which of the three root causes — Damaged Tire (DT),
Electronics Malfunctioning (EM), or Fuel Tank Leaking (FTL) — is the
most likely?

**KNOBs to change.**

```python
NETWORK_CHOICE   = "car"
CAR_EVIDENCE     = {"V": "true", "SMS": "true", "HC": "false"}  # default
DIAGNOSTIC_MODE  = True   # prints P(root=true | evidence) for each root
```

**Expected output (exact enumeration).** The `Diagnostic ranking`
block lists the three root nodes ranked descending:

    DT   P(true | evidence) = 0.634276
    FTL  P(true | evidence) = 0.077228
    EM   P(true | evidence) = 0.070475

**Answer:** **Damaged Tire (DT)** is the most likely cause. Note that
FTL slightly outranks EM here — without HC firing, the FTL prior+
SMS-evidence path edges out EM.

**Stretch.** Re-run with `CAR_EVIDENCE = {"HC": "true"}`:

    FTL  P(true | evidence) = 0.620248
    DT   P(true | evidence) = 0.525210
    EM   P(true | evidence) = 0.399160

With only "high consumption" observed, FTL becomes the most likely
cause (FTL is the strongest predictor of HC in the CPT).

---

## Variant 3 — Add a new variable to the network

**Question (Car-diagnosis net, extended).** Add a new observable
symptom **Engine Noise (EN)** with parent Electronics Malfunctioning
(EM) and the CPT

    P(EN=T | EM=F) = 0.05
    P(EN=T | EM=T) = 0.80.

If you now observe Vibrations = T and Engine Noise = T (but no other
symptoms), what is the probability that EM is the cause? What is the
probability that DT is the cause? Which is more likely?

**KNOBs to change.**

```python
NETWORK_CHOICE = "car"
EXTRA_CAR_VARIABLES = [
    {
        "name":        "EN",
        "assignments": ("false", "true"),
        "parents":     ["EM"],
        "probability_table": {
            ("false",): (0.95, 0.05),
            ("true",):  (0.20, 0.80),
        },
    },
]
CAR_EVIDENCE    = {"V": "true", "EN": "true"}
CAR_QUERY       = {"EM": "true"}
DIAGNOSTIC_MODE = True   # also see DT, FTL for completeness

# REQUIRED: get_joint_probability requires every variable to be in the
# joint assignment dict. After splicing EN into the network you MUST
# also include "EN" in CAR_JOINT — otherwise the runner crashes with
# KeyError before reaching the diagnostic ranking.
CAR_JOINT = {
    "DT": "true",
    "EM": "false",
    "FTL": "false",
    "V": "true",
    "SMS": "true",
    "HC": "false",
    "EN": "false",
}
```

**Expected output (exact enumeration).**

- Marginal of EN: **P(EN=T) = 0.275000**.
- Conditional `P(EM=true | V=true, EN=true)` = **0.872727**.
- Diagnostic ranking:

      EM   P(true | evidence) = 0.872727
      DT   P(true | evidence) = 0.750000
      FTL  P(true | evidence) = 0.200000

**Answer:** **EM** is the more likely culprit (0.873 vs 0.750 for DT).
The engine-noise observation flips the ranking — without EN the
ranking would be led by DT. (Note: V and EN are conditionally
independent given the roots — V's only parent is DT, EN's only parent
is EM — so V tells you nothing about EM and EN tells you nothing about
DT. Each evidence node only updates its own parent.)

**Notes for the examiner.**
- The KNOB schema is documented in the comment block above
  `EXTRA_CAR_VARIABLES` in Runner_solution.py.
- Parents listed in `"parents": [...]` MUST already be variables in
  the chosen network.
- `CAR_JOINT` MUST include the new variable EN (see KNOB block above).
  Forgetting this is the #1 crash mode for this variant.

---

## Bonus stretch variants (Lab Solver-suggested)

These weren't in the §8.3 starter list but follow naturally from the
KNOBs already exposed.

**B1.** "**What if the prior on rain changed?**" Sprinkler net,
flip the top-level KNOB `SPRINKLER_RAIN_CPT` so that
`P(Rain=T | Cloudy=T) = 0.95` instead of 0.8. One-line KNOB change:

```python
SPRINKLER_RAIN_CPT = {
    ('false',): (0.8, 0.2),
    ('true',):  (0.05, 0.95),   # was (0.2, 0.8)
}
```

Re-run with the default evidence/query. Expected:
`P(Sprinkler=T | WetGrass=T)` drops from **0.4298** to **0.3935** —
rain becomes the more likely explainer of wet grass, so the sprinkler
posterior shrinks (the classic *explaining-away* flavour: stronger
alternative cause → query cause less needed).

**B2.** "**A noisy sensor.**" Sprinkler net, add a new node
`SoggyShoes` with parent `WetGrass` via `EXTRA_SPRINKLER_VARIABLES`,
CPT `P(SoggyShoes=T | WetGrass=F)=0.02`, `P(SoggyShoes=T | WetGrass=T)=0.9`.
Set evidence to `{"SoggyShoes": "true"}` and query `{"Cloudy": "true"}`.

```python
NETWORK_CHOICE = "sprinkler"
EXTRA_SPRINKLER_VARIABLES = [
    {
        "name":        "SoggyShoes",
        "assignments": ("false", "true"),
        "parents":     ["WetGrass"],
        "probability_table": {
            ("false",): (0.98, 0.02),
            ("true",):  (0.10, 0.90),
        },
    },
]
SPRINKLER_EVIDENCE = {"SoggyShoes": "true"}
SPRINKLER_QUERY    = {"Cloudy": "true"}

# REQUIRED: SPRINKLER_JOINT must include SoggyShoes — otherwise the
# joint-probability print at the top of main() crashes with KeyError.
SPRINKLER_JOINT = {
    "Cloudy": "false",
    "Sprinkler": "true",
    "Rain": "false",
    "WetGrass": "true",
    "SoggyShoes": "true",
}
```

**Expected output (exact enumeration).**
`P(Cloudy = true | SoggyShoes = true)` = **0.573228** — strictly
above the prior 0.5. This demonstrates that a downstream observation
DOES update an upstream variable: soggy shoes are evidence for wet
grass, which is evidence for sprinkler or rain having fired, which is
evidence that it was cloudy. The gossip-graph passes information both
ways through the chain.
