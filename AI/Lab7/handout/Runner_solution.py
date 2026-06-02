"""
LAB 7: Bayesian Networks (inference) — Runner / entry point
===========================================================

PROBLEM STATEMENT (from Lab 7.pdf):
-----------------------------------
Exercise 1: Familiarize yourself with the code in bn.py, Runner.py and
Variable.py. Complete bn.py and Variable.py to calculate the
probabilities for the Bayesian network below.

    The Sprinkler network:
        Cloudy  (root, P(F)=P(T)=0.5)
          |  \\
          v   v
        Sprinkler   Rain
            \\     /
             v   v
            WetGrass

    CPTs:
        P(Cloudy)        :  F=0.5, T=0.5
        P(Sprinkler|C)   :  C=F -> (F=0.5, T=0.5); C=T -> (F=0.9, T=0.1)
        P(Rain|C)        :  C=F -> (F=0.8, T=0.2); C=T -> (F=0.2, T=0.8)
        P(WetGrass|S,R)  :  (S=F,R=F)->(F=1, T=0)
                            (S=T,R=F)->(F=0.1, T=0.9)
                            (S=F,R=T)->(F=0.1, T=0.9)
                            (S=T,R=T)->(F=0.01, T=0.99)

    The runner prints (i) marginal probabilities of every node,
    (ii) one joint probability of a complete assignment, and
    (iii) one conditional probability of a query given evidence.

Homework Exercise: a 6-node car-diagnosis network.

    Roots:        Damaged Tire (DT)  P(T)=0.3
                  Electronics Malfunctioning (EM)  P(T)=0.3
                  Fuel Tank Leaking (FTL)  P(T)=0.2
    Symptoms:     Vibrations (V) given DT
                  Slow Max Speed (SMS) given DT, EM
                  High Consumption (HC) given DT, FTL, EM
    Evidence:     V=T, SMS=T, HC=F. Question: which root cause is
                  most likely?

MENTAL MODEL (one-line analogy):
--------------------------------
A Bayesian network is a gossip graph: each node's belief depends on the
people upstream of it (its parents). The CPT is "given what my parents
just told me, here are the odds of what I'll say next." Marginals are
"how often does this person say T overall, before anybody hands me a
fact?" Conditional inference is "now that I've been TOLD some people's
answers (the evidence), what should the others believe?" — and in a
diagnostic query, "given the symptoms, which root cause is most
likely?"

REFERENCES:
-----------
- Lecture L09a §3 (Core Concepts): Bayesian network, CPT,
  conditional probability table, Markov condition.
- Lecture L09a §4 (Algorithms): inference by enumeration.
- Glossary: Bayesian network, Conditional probability,
  Conditional probability table (CPT), Joint probability distribution,
  Marginal probability, Markov condition, Chain rule, Bayes' rule.
- See study/lectures/L09a-Bayesian-Networks.md once locked.

HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS:
--------------------------------------------------
EVERY tunable lives in the KNOBs below. No edits to bn_solution.py or
Variable_solution.py are required for any standard exam variant.

1. To switch which network is queried:
     Set NETWORK_CHOICE.
     - "sprinkler" — the lab Exercise 1 (default).
     - "car"       — the homework car-diagnosis network.

2. To change the EVIDENCE you condition on:
     Edit SPRINKLER_EVIDENCE or CAR_EVIDENCE (depending on
     NETWORK_CHOICE). Keys must be variable names, values must be one
     of the variable's assignments ("true"/"false").

3. To change the QUERY node(s) (what probability you want):
     Edit SPRINKLER_QUERY or CAR_QUERY.

4. To change a JOINT-probability assignment (complete assignment of
   every variable):
     Edit SPRINKLER_JOINT or CAR_JOINT.

5. To ADD A NEW VARIABLE to the car network (e.g. an extra symptom
   "Engine Noise" that depends on Electronics Malfunctioning):
     Use the EXTRA_CAR_VARIABLES list — see its KNOB for the schema.
     The runner will splice your variable into the network in
     topological order (parents first) without you touching any other
     code. You can also use this for the sprinkler network via
     EXTRA_SPRINKLER_VARIABLES.

6. To CHANGE A CPT VALUE (e.g. "what if P(Cloudy=T) were 0.8?"):
     Every CPT dict is a top-level KNOB. Edit one of:
       Sprinkler net: SPRINKLER_CLOUDY_CPT, SPRINKLER_SPRINKLER_CPT,
                      SPRINKLER_RAIN_CPT, SPRINKLER_WETGRASS_CPT.
       Car net:       CAR_DT_CPT, CAR_EM_CPT, CAR_FTL_CPT,
                      CAR_V_CPT, CAR_SMS_CPT, CAR_HC_CPT.
     Bonus B1 (e.g. set P(Rain=T | Cloudy=T) to 0.95) is a one-line
     change to SPRINKLER_RAIN_CPT.

7. To DIAGNOSE which root cause is most likely (Variant 2 style):
     Set DIAGNOSTIC_MODE = True. The runner will, for each root,
     compute P(root=true | evidence) and print them ranked.

OUTPUTS WHEN RUN:
-----------------
Prints marginal probabilities of every node, the chosen joint
probability, the chosen conditional probability, and (if
DIAGNOSTIC_MODE is on) a ranked list of root-cause posteriors.

ENTRY POINT: yes
----------------
Run from the lab folder with:
    py -3.12 Runner_solution.py
"""

import random
from pprint import pformat

from Variable_solution import Variable
from bn_solution import BayesianNetwork


# =============================================================================
# TOP-LEVEL KNOBS
# =============================================================================

# KNOB: NETWORK_CHOICE (default="sprinkler", allowed={"sprinkler", "car"})
#   What it does: selects which Bayesian network the runner will build
#     and exercise. "sprinkler" is the lab Exercise 1 net; "car" is the
#     homework car-diagnosis net (slide 4 of Lab 7.pdf).
#   Effect: changes which network is built, which evidence/query/joint
#     KNOBs apply, and which set of EXTRA_*_VARIABLES is consulted.
#   Exam variants: stay on "sprinkler" for the standard Exercise 1
#     variants; switch to "car" for the homework-style root-cause
#     diagnosis variants.
NETWORK_CHOICE = "sprinkler"

# KNOB: DIAGNOSTIC_MODE (default=False, allowed={True, False})
#   What it does: when True, the runner identifies every ROOT node and
#     prints P(root = true | EVIDENCE) for each one, ranked
#     descending — directly answering "which root cause is most
#     likely?" without you having to set up a per-root query.
#   Effect: extra block of output at the end of the run.
#   Exam variants: typical for car-network variants ("which fault is
#     most likely given the symptoms?"). Cheap to leave on for the
#     sprinkler too (it'll just rank Cloudy).
DIAGNOSTIC_MODE = False

# KNOB: VERBOSE (default=True, allowed={True, False})
#   What it does: controls whether marginals/joint/conditional are
#     printed. Reviewers can flip this off when running batch tests.
#   Effect: silences most prints. Diagnostic mode still prints.
VERBOSE = True

# KNOB: RANDOM_SEED (default=42, allowed=any int or None)
#   What it does: seeds the random sampling that follows the joint
#     distribution at the end of the sprinkler demo (the original
#     Runner.py also drew one random sample). Fixing it makes the
#     output reproducible for reviewers.
#   Effect: changes the printed random-sample line at the end.
#   Exam variants: not exam-relevant on its own; only governs the
#     example sample. Leave at 42 for grading reproducibility.
RANDOM_SEED = 42


# =============================================================================
# SPRINKLER-NETWORK KNOBS (used when NETWORK_CHOICE == "sprinkler")
# =============================================================================

# KNOB: SPRINKLER_EVIDENCE (default={"WetGrass": "true"},
#                           allowed: any dict {var_name: "true"|"false"})
#   What it does: the evidence the conditional query is conditioned on.
#     Variable names: Cloudy, Sprinkler, Rain, WetGrass. Values: "true"
#     or "false".
#   Effect: changes the denominator of Bayes' rule in
#     network.get_conditional_probability.
#   Exam variants:
#     - Lab default: {"WetGrass": "true"}.
#     - "Different evidence values" variant: try
#         {"WetGrass": "false"} or {"Cloudy": "true"}.
SPRINKLER_EVIDENCE: dict[str, str] = {"WetGrass": "true"}

# KNOB: SPRINKLER_QUERY (default={"Sprinkler": "true"},
#                        allowed: any dict {var_name: "true"|"false"})
#   What it does: the variable(s) and value(s) you want the conditional
#     probability of. Pair with SPRINKLER_EVIDENCE above.
#   Effect: changes the numerator of the conditional-probability call.
#   Exam variants:
#     - Lab default ("did the sprinkler do it?"):
#         {"Sprinkler": "true"}.
#     - "Query a different node" variant: {"Rain": "true"} or
#         {"Cloudy": "true"}.
SPRINKLER_QUERY: dict[str, str] = {"Sprinkler": "true"}

# KNOB: SPRINKLER_JOINT (default below,
#                       allowed: any dict assigning every Cloudy,
#                       Sprinkler, Rain, WetGrass.)
#   What it does: the assignment whose joint probability is printed.
#   Effect: changes only what get_joint_probability prints.
#   Exam variants: explore P(everything = T) vs. P(everything = F),
#     and the rare combinations.
SPRINKLER_JOINT: dict[str, str] = {
    "Sprinkler": "true",
    "Cloudy": "false",
    "WetGrass": "true",
    "Rain": "false",
}

# KNOB: EXTRA_SPRINKLER_VARIABLES (default=[], allowed: list of dicts as below)
#   What it does: lets you splice extra nodes into the sprinkler net
#     WITHOUT editing build_sprinkler_network().
#   Schema for each dict:
#     {
#       "name":          "Rainbow",           # str, the new node's name
#       "assignments":   ("false", "true"),   # tuple of value labels
#       "parents":       ["Rain"],            # list of EXISTING node names
#       "probability_table": {                # dict keyed by tuples of
#                                             # parent values in the order
#                                             # given by "parents"
#           ("false",): (1.0, 0.0),
#           ("true",):  (0.2, 0.8),
#       },
#     }
#   The new node is appended after all existing nodes (and after any
#   already-listed extras above it) so the topological order is
#   maintained as long as you only declare parents that come earlier
#   in the file.
#   Effect: the new node is included in marginals, in the diagnostic
#     ranking (if it's a root), and is available as a query/evidence
#     name in SPRINKLER_EVIDENCE / SPRINKLER_QUERY.
#   Exam variants: "Add a new variable to the network" (Variant 3).
EXTRA_SPRINKLER_VARIABLES: list[dict] = []


# -----------------------------------------------------------------------------
# SPRINKLER CPT KNOBs — Bonus variant B1 lives here.
# -----------------------------------------------------------------------------
# Every CPT dict that build_sprinkler_network used to declare locally has been
# promoted here. Flipping any single number is a one-line KNOB change — the
# builder reads these globals at construction time.
#
# Row-key convention: parent values listed in the parents-declaration order
# (Cloudy for sprinkler/rain; Sprinkler, Rain for wet_grass). Row value is
# (P(node=false), P(node=true)) matching the assignments tuple
# ("false", "true"). Swapping the two positions is a common bug and produces
# a perfectly valid CPT for the COMPLEMENT random variable.

# KNOB: SPRINKLER_CLOUDY_CPT  (default={(): (0.5, 0.5)})
#   What it does: prior on Cloudy. (P(F), P(T)).
#   Exam variants: "What if P(Cloudy=T) were 0.9?" — set {(): (0.1, 0.9)}.
SPRINKLER_CLOUDY_CPT: dict[tuple[str, ...], tuple[float, ...]] = {
    (): (0.5, 0.5),
}

# KNOB: SPRINKLER_SPRINKLER_CPT  (default below)
#   Rows: ('false',) is P(Sprinkler | Cloudy=F);
#         ('true',)  is P(Sprinkler | Cloudy=T).
SPRINKLER_SPRINKLER_CPT: dict[tuple[str, ...], tuple[float, ...]] = {
    ('false',): (0.5, 0.5),
    ('true',):  (0.9, 0.1),
}

# KNOB: SPRINKLER_RAIN_CPT  (default below)
#   Rows: ('false',) is P(Rain | Cloudy=F);
#         ('true',)  is P(Rain | Cloudy=T).
#   Exam variants: Bonus B1 — set ('true',) to (0.05, 0.95) so that
#     P(Rain=T | Cloudy=T) = 0.95.
SPRINKLER_RAIN_CPT: dict[tuple[str, ...], tuple[float, ...]] = {
    ('false',): (0.8, 0.2),
    ('true',):  (0.2, 0.8),
}

# KNOB: SPRINKLER_WETGRASS_CPT  (default below)
#   Row key: (Sprinkler, Rain). Row value: (P(W=F), P(W=T)).
SPRINKLER_WETGRASS_CPT: dict[tuple[str, ...], tuple[float, ...]] = {
    ('false', 'false'): (1, 0),
    ('true',  'false'): (0.1, 0.9),
    ('false', 'true'):  (0.1, 0.9),
    ('true',  'true'):  (0.01, 0.99),
}


# =============================================================================
# CAR-NETWORK KNOBS (used when NETWORK_CHOICE == "car")
# =============================================================================

# KNOB: CAR_EVIDENCE (default={"V": "true", "SMS": "true", "HC": "false"})
#   What it does: the symptoms observed.
#   Effect: drives the conditional / diagnostic query results.
#   Exam variants:
#     - Lab homework default: {"V":"true","SMS":"true","HC":"false"}
#       ("vibrations and slow max speed but no extra consumption").
#     - "Different evidence" variant: e.g. {"HC":"true"} alone, or
#       {"V":"false","SMS":"true"}.
CAR_EVIDENCE: dict[str, str] = {"V": "true", "SMS": "true", "HC": "false"}

# KNOB: CAR_QUERY (default={"DT": "true"}, allowed: any dict over roots
#                  {DT, EM, FTL} or symptoms {V, SMS, HC})
#   What it does: which probability to display in the regular
#     "conditional probability of" line. DIAGNOSTIC_MODE handles the
#     "rank all root causes" version.
#   Exam variants:
#     - "Most likely cause" with DIAGNOSTIC_MODE=True.
#     - Or directly query one cause: {"EM": "true"} / {"FTL": "true"}.
CAR_QUERY: dict[str, str] = {"DT": "true"}

# KNOB: CAR_JOINT (default below, allowed: dict assigning every variable
#                  in the car network)
#   What it does: assignment whose joint probability gets printed.
#   Exam variants: try the most likely full assignment, then the least
#     likely, to build intuition.
CAR_JOINT: dict[str, str] = {
    "DT": "true",
    "EM": "false",
    "FTL": "false",
    "V": "true",
    "SMS": "true",
    "HC": "false",
}

# KNOB: EXTRA_CAR_VARIABLES (default=[], allowed: list of dicts; same
#                             schema as EXTRA_SPRINKLER_VARIABLES)
#   What it does: splice extra nodes into the car network.
#   Effect: same as EXTRA_SPRINKLER_VARIABLES.
#   Exam variants: "Add a new variable to the network" (Variant 3),
#     e.g. an extra observation node "Engine Noise (EN)" that depends
#     on EM.
EXTRA_CAR_VARIABLES: list[dict] = []


# -----------------------------------------------------------------------------
# CAR-NETWORK CPT KNOBs — every prior and CPT promoted to module scope.
# -----------------------------------------------------------------------------
# Row-key convention: parents in declaration order (DT for V; DT, EM for SMS;
# DT, FTL, EM for HC). Row value is (P(node=false), P(node=true)).

# KNOB: CAR_DT_CPT  (default={(): (0.7, 0.3)})  — prior on Damaged Tire.
CAR_DT_CPT: dict[tuple[str, ...], tuple[float, ...]] = {
    (): (0.7, 0.3),
}

# KNOB: CAR_EM_CPT  (default={(): (0.7, 0.3)})  — prior on Electronics Malfunctioning.
CAR_EM_CPT: dict[tuple[str, ...], tuple[float, ...]] = {
    (): (0.7, 0.3),
}

# KNOB: CAR_FTL_CPT  (default={(): (0.8, 0.2)})  — prior on Fuel Tank Leaking.
CAR_FTL_CPT: dict[tuple[str, ...], tuple[float, ...]] = {
    (): (0.8, 0.2),
}

# KNOB: CAR_V_CPT  P(V | DT). Row key = (DT,).
CAR_V_CPT: dict[tuple[str, ...], tuple[float, ...]] = {
    ('false',): (0.9, 0.1),
    ('true',):  (0.3, 0.7),
}

# KNOB: CAR_SMS_CPT  P(SMS | DT, EM). Row key = (DT, EM).
CAR_SMS_CPT: dict[tuple[str, ...], tuple[float, ...]] = {
    ('false', 'false'): (0.3, 0.7),
    ('false', 'true'):  (0.7, 0.3),
    ('true',  'false'): (0.4, 0.6),
    ('true',  'true'):  (0.95, 0.05),
}

# KNOB: CAR_HC_CPT  P(HC | DT, FTL, EM). Row key = (DT, FTL, EM).
CAR_HC_CPT: dict[tuple[str, ...], tuple[float, ...]] = {
    ('false', 'false', 'false'): (0.99, 0.01),
    ('false', 'false', 'true'):  (0.9, 0.1),
    ('false', 'true',  'false'): (0.5, 0.5),
    ('false', 'true',  'true'):  (0.4, 0.6),
    ('true',  'false', 'false'): (0.8, 0.2),
    ('true',  'false', 'true'):  (0.7, 0.3),
    ('true',  'true',  'false'): (0.2, 0.8),
    ('true',  'true',  'true'):  (0.1, 0.9),
}


# =============================================================================
# Helper functions (originals — unchanged from Runner.py)
# =============================================================================

def create_random_sample(network: BayesianNetwork) -> dict[str, str]:
    """ creates random sample for the given network.
        the distribution of the samples follows the joint probability function.
        assumes binary variables. """
    sample: dict[str, str] = {}
    for var in network.variables:

        samp = random.random()
        assignment1 = list(var.assignments.keys())[0]
        assignment2 = list(var.assignments.keys())[1]

        parents_values = network.sub_vals(var, sample)
        prob = var.get_probability(assignment1, parents_values)

        if samp <= prob:
            sample[var.name] = assignment1
        else:
            sample[var.name] = assignment2
    return sample


def pad(string: str, pad: int = 4) -> str:
    lines = string.split('\n')
    padded_lines = (' ' * pad + line for line in lines)
    return '\n'.join(padded_lines)


def print_conditional_probability(network: BayesianNetwork, conditionals_vars: dict[str, str],
                                  conditionals_evidents: dict[str, str]) -> None:
    print('Given')
    print(pad(pformat(conditionals_evidents)))
    print('conditional probability of')
    print(pad(pformat(conditionals_vars)))
    print("is {:f}".format(
        network.get_conditional_probability(
            conditionals_vars,
            conditionals_evidents
        )))
    print()


def print_joint_probability(network: BayesianNetwork, values: dict[str, str]) -> None:
    print('Joint probability of')
    print(pad(pformat(values)))
    print("is {:f}".format(network.get_joint_probability(values)))


def print_marginal_probabilities(network: BayesianNetwork) -> None:
    print("Marginal probabilities:")
    for variable in network.get_variables():
        print("    {}".format(variable.get_name()))
        for assignment in variable.get_assignments():
            print("        {}: {:f}".format(
                assignment,
                variable.get_marginal_probability(assignment))
            )


# =============================================================================
# Network builders
# =============================================================================

def _splice_extra_variables(network: BayesianNetwork, extras: list[dict]) -> None:
    """Append the user-declared EXTRA_*_VARIABLES list to a network.

    Why: lets exam-variant questions add a node ("Variant 3 — add a new
    variable") with no edits to the build function. We resolve each
    declared parent name against the nodes already in the network, so
    the user only needs to list parents that come earlier."""
    for spec in extras:
        parent_nodes = [network.get_variable(p) for p in spec.get("parents", [])]
        new_var = Variable(
            name=spec["name"],
            assignments=spec["assignments"],
            probability_table=spec["probability_table"],
            parents=parent_nodes,
        )
        # Wire each parent to know about the new child (used by is_child_of /
        # diagnostic walks). The base BN add_variable does the dictionary
        # bookkeeping and resets `ready`.
        for parent_node in parent_nodes:
            parent_node.add_child(new_var)
        network.add_variable(new_var)
    if extras:
        network.calculate_marginal_probabilities()


def build_sprinkler_network() -> BayesianNetwork:
    """Build the Sprinkler / Cloudy / Rain / WetGrass network.

    Every CPT is sourced from a top-level KNOB (SPRINKLER_*_CPT) so that
    exam variants can override a single CPT without touching this
    function. See the KNOB block in the module header.
    """

    cloudy = Variable('Cloudy', ('false', 'true'), SPRINKLER_CLOUDY_CPT)
    sprinkler = Variable('Sprinkler', ('false', 'true'), SPRINKLER_SPRINKLER_CPT, [cloudy])
    rain = Variable('Rain', ('false', 'true'), SPRINKLER_RAIN_CPT, [cloudy])
    wetgrass = Variable('WetGrass', ('false', 'true'), SPRINKLER_WETGRASS_CPT, [sprinkler, rain])
    # Wire children explicitly so diagnostic walks and `is_child_of` see the graph.
    cloudy.add_child(sprinkler)
    cloudy.add_child(rain)
    sprinkler.add_child(wetgrass)
    rain.add_child(wetgrass)

    network = BayesianNetwork()
    network.set_variables([cloudy, sprinkler, rain, wetgrass])
    network.calculate_marginal_probabilities()
    return network


def build_car_network() -> BayesianNetwork:
    """Build the car-diagnosis network from Lab 7.pdf homework.

    Roots: DT, EM, FTL.
    Children: V (parents=DT), SMS (parents=DT, EM),
              HC (parents=DT, FTL, EM).

    Every CPT is sourced from a top-level KNOB (CAR_*_CPT) so exam
    variants can override priors / CPTs by editing a single global.
    """

    dt = Variable('DT', ('false', 'true'), CAR_DT_CPT)
    em = Variable('EM', ('false', 'true'), CAR_EM_CPT)
    ftl = Variable('FTL', ('false', 'true'), CAR_FTL_CPT)
    v = Variable('V', ('false', 'true'), CAR_V_CPT, [dt])
    sms = Variable('SMS', ('false', 'true'), CAR_SMS_CPT, [dt, em])
    hc = Variable('HC', ('false', 'true'), CAR_HC_CPT, [dt, ftl, em])
    dt.add_child(v); dt.add_child(sms); dt.add_child(hc)
    em.add_child(sms); em.add_child(hc)
    ftl.add_child(hc)

    network = BayesianNetwork()
    network.set_variables([dt, em, ftl, v, sms, hc])
    network.calculate_marginal_probabilities()
    return network


# ---------------------------------------------------------------------------
# Template-compatibility aliases
# ---------------------------------------------------------------------------
#
# The original `Runner.py` template defines `sprinkler_network()` (no
# `build_` prefix) as a *combined* "build + print" routine. We split the
# concerns in the solution: `build_sprinkler_network` returns the network,
# `main()` does the printing. To preserve the spec's contract that every
# template top-level callable still exists as a same-named attribute on the
# solution module (so rubrics, IDE renames, and `from Runner_solution import
# sprinkler_network` calls all keep working), we expose aliases.
#
# `car_network` was never in the template — it is introduced by the Lab 7
# homework. We still expose the alias under the symmetric short name so
# downstream consumers can use either `build_car_network` or `car_network`
# interchangeably, mirroring the sprinkler pair.
sprinkler_network = build_sprinkler_network
car_network = build_car_network


# =============================================================================
# Diagnostic-mode helper
# =============================================================================

def print_diagnostic_ranking(network: BayesianNetwork, evidence: dict[str, str]) -> None:
    """Compute P(root = true | evidence) for every root and rank them.

    Why: the homework asks "which fault is most likely given the
    symptoms?" — that's a separate conditional query per root cause.
    We loop the roots, call network.get_conditional_probability for
    {root: true} | evidence, and print sorted.
    """
    roots = [v for v in network.get_variables() if not v.parents]
    if not roots:
        print("No root nodes — nothing to diagnose.")
        return

    print("Diagnostic ranking (P(root = 'true' | evidence)):")
    print("    Evidence:")
    print(pad(pformat(evidence), pad=8))
    results: list[tuple[str, float]] = []
    for root in roots:
        # Each root probability is computed independently of the other
        # roots' posteriors — this is the simple, per-root inversion of
        # Bayes' rule the lecture covers (no junction trees).
        try:
            p = network.get_conditional_probability({root.name: 'true'}, evidence)
        except Exception as exc:  # pragma: no cover - defensive logging
            p = float('nan')
            print(f"    [warning] {root.name}: conditional query failed: {exc}")
        results.append((root.name, p))

    # Sort descending so the most-likely cause is first — easy to read
    # at the exam.
    results.sort(key=lambda kv: (kv[1] if kv[1] == kv[1] else -1.0), reverse=True)
    for name, prob in results:
        print(f"    {name:6s}  P(true | evidence) = {prob:.6f}")
    print()


# =============================================================================
# Main entry point
# =============================================================================

def main() -> None:
    random.seed(RANDOM_SEED)

    if NETWORK_CHOICE == "sprinkler":
        network = build_sprinkler_network()
        _splice_extra_variables(network, EXTRA_SPRINKLER_VARIABLES)
        evidence = SPRINKLER_EVIDENCE
        query = SPRINKLER_QUERY
        joint_values = SPRINKLER_JOINT
    elif NETWORK_CHOICE == "car":
        network = build_car_network()
        _splice_extra_variables(network, EXTRA_CAR_VARIABLES)
        evidence = CAR_EVIDENCE
        query = CAR_QUERY
        joint_values = CAR_JOINT
    else:
        raise ValueError(
            f"NETWORK_CHOICE must be 'sprinkler' or 'car', got {NETWORK_CHOICE!r}"
        )

    if VERBOSE:
        print(f"Network: {NETWORK_CHOICE}")
        print()
        print_marginal_probabilities(network)
        print()
        print_joint_probability(network, joint_values)
        print()
        print_conditional_probability(network, query, evidence)

    if DIAGNOSTIC_MODE:
        print_diagnostic_ranking(network, evidence)

    if VERBOSE and NETWORK_CHOICE == "sprinkler":
        # Original Runner.py printed one random sample's joint probability;
        # keep this behaviour for backward compatibility, gated to the
        # sprinkler net (the car net's joint over partial assignments
        # would need extension and is out of scope).
        sample = create_random_sample(network)
        print_joint_probability(network, sample)


if __name__ == '__main__':
    main()
