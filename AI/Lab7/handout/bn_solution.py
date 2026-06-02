"""
LAB 7: Bayesian Networks (inference) — BayesianNetwork module
=============================================================

PROBLEM STATEMENT (from Lab 7.pdf):
-----------------------------------
Exercise 1: Familiarize yourself with the code in bn.py, Runner.py and
Variable.py. Complete bn.py and Variable.py to calculate the
probabilities for the Bayesian network of the classic Sprinkler /
Cloudy / Rain / Wet Grass example.

The specific TODO in this file is `BayesianNetwork.get_joint_probability`:
given an assignment dict mapping every variable name in the network to
one of its values, return the joint probability of that complete
assignment — i.e.

        P(X1=x1, X2=x2, ..., Xn=xn)

The chain rule + the Markov condition of a Bayesian network says

        P(X1, ..., Xn) = prod_i  P(Xi | Parents(Xi))

so we walk the network and multiply each conditional from the relevant
row of each node's CPT. This is the bedrock of every other inference
operation in the file.

Homework Exercise (also covered): a 6-node car-diagnosis network. See
Runner_solution.py for the full network definition and the queries.

MENTAL MODEL (one-line analogy):
--------------------------------
Joint probability is the gossip-graph "exact transcript" probability:
"what's the chance the WHOLE conversation went exactly this way — that
Cloudy says T, then Sprinkler says F (knowing Cloudy=T), then Rain says
T (knowing Cloudy=T), then WetGrass says T (knowing Sprinkler=F,
Rain=T)?" You multiply each person's odds of saying their line GIVEN
what their parents already said. That is the chain rule of Bayesian
networks (Lecture L09a §3 / §4).

REFERENCES:
-----------
- Lecture L09a §3 (Core Concepts): Bayesian network, CPT, chain rule.
- Lecture L09a §4 (Algorithms): inference by enumeration uses
  get_joint_probability as its inner step.
- Glossary: Bayesian network, Chain rule, Joint probability
  distribution, Conditional probability table (CPT),
  Markov condition, Inference by enumeration.
- See study/lectures/L09a-Bayesian-Networks.md once locked.

HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS:
--------------------------------------------------
This file is a HELPER MODULE — it implements general BN inference and
has no problem-specific tunables. To adapt to a different question:
  - To switch between sprinkler / car-diagnosis / a custom network:
    edit Runner_solution.py (NETWORK_CHOICE knob).
  - To add a new node / change CPT values / change evidence / change
    the query: see the KNOBs in Runner_solution.py.
  - get_conditional_probability is *exact inference by enumeration* — it
    works for any DAG structure, any number of query and evidence
    variables, and correctly handles colliders / explaining-away.
  - The Variable.get_conditional_probability (in Variable_solution.py)
    is a local CPT-marginaliser used internally and supports PARTIAL
    evidence over a node's direct parents.
  - No edits to this file are needed for any variant in the exam bank.

OUTPUTS WHEN RUN:
-----------------
This module is not directly executed. It is imported by
Runner_solution.py.

ENTRY POINT: no
---------------
Helper module. The entry point is Runner_solution.py.
"""

from Variable_solution import Variable


class BayesianNetwork(object):
    """ Bayesian Network implementation. This implementation incorporates few
        assumptions (see comments).
    """

    def __init__(self):
        """ Initialize connectivity matrix. """
        self.variables: list[Variable] = []  # list of variables (Nodes)
        self.variable_dictionary: dict[
            str, Variable] = {}  # a mapping of variable name to the actual node, for easy access
        self.ready: bool = False  # indication of this net state

    def calculate_marginal_probabilities(self) -> None:
        """ pre-calculate and stores the marginal probabilities of all the nodes """

        # iterate over the Nodes, from parents to children
        for variable in self.variables:
            variable.calculate_marginal_probability()
        self.ready = True

    def get_variables(self) -> list[Variable]:
        """ returns the variables """

        return self.variables

    def get_variable(self, variable_name: str) -> Variable:
        """ returns the variable with the given name """

        return self.variable_dictionary[variable_name]

    def add_variable(self, var: Variable, index: int = -1) -> None:  # len(variables)):
        """ add a single Node to the net """

        if index < 0:
            self.variables.append(var)
        else:
            self.variables.insert(index, var)

        self.variable_dictionary[var.name] = var
        self.ready = False  # we need to re-calculate marginals

    def set_variables(self, new_variables: list[Variable]) -> None:
        """ quick assignment: set the given Node list to be the Nodes of this
            net
        """

        self.variables = new_variables
        for variable in self.variables:
            self.variable_dictionary[variable.name] = variable
        self.ready = False  # we need to re-calculate marginals

        self.calculate_marginal_probabilities()

    def get_marginal_probability(self, var: Variable, val: str) -> float:
        """ returns the marginal probability of a given node """

        return var.get_marginal_probability(val)

    # values is dictionary
    def get_joint_probability(self, values: dict[str, str]) -> float:
        """ return the joint probability of the Nodes.

            Why: the Bayesian-network factorisation is the entire reason BNs
            are tractable. By the chain rule + the Markov condition,
                P(X1=x1, ..., Xn=xn) = prod_i  P(Xi=xi | Parents(Xi)=values).
            For every node in the network we look up the row of its CPT
            indexed by the values its parents take in `values`, read off the
            cell for the node's own value, and multiply everything together.
            For a root node the parent-tuple is the empty tuple `()`.
        """
        # Defensive: require an assignment for every variable in the network.
        # Without this guarantee we can't apply the chain rule end-to-end.
        for variable in self.variables:
            if variable.name not in values:
                raise KeyError(
                    f"get_joint_probability requires a value for every "
                    f"variable; missing '{variable.name}'."
                )

        joint = 1.0
        for variable in self.variables:
            # Gather the values its parents take in this complete assignment.
            # sub_vals returns a tuple ordered to match variable.probability_table keys.
            parents_values = self.sub_vals(variable, values)
            # CPT cell: P(variable = values[variable.name] | parents = parents_values).
            joint *= variable.get_probability(values[variable.name], parents_values)

        return joint

    def get_conditional_probability(self, values: dict[str, str], evidents: dict[str, str]) -> float:
        """ Return P(values | evidents) by exact INFERENCE BY ENUMERATION.

            Algorithm (Lecture L09a §3.13 / §4.4, Russell & Norvig §14.4):

                P(Q = q | E = e) = sum_h P(Q = q, E = e, H = h)
                                   ---------------------------------------------
                                   sum_{q', h} P(Q = q', E = e, H = h)

            where Q are the query variables, E are the evidence variables, and
            H are the *hidden* variables (everything else). Each term in the
            numerator and denominator is a complete joint probability from
            `get_joint_probability` — the Bayesian-network chain-rule
            factorisation.

            Why this replaces the prior 2-state Bayes-template:
                - It is exact for any network structure (chains, forks,
                  colliders, V-structures with shared ancestors).
                - It correctly demonstrates "explaining away" (collider) and
                  the canonical Sprinkler answer P(S=T | W=T) = 0.4298.
                - It handles multi-variable queries, multi-variable evidence
                  with arbitrary positions in the DAG, and any non-binary
                  domain.

            Complexity: O(d^h) where d is the max domain size and h is the
            number of hidden variables. Fine for the lab's <= 8 nodes.
        """
        # Identify which variables are query, evidence, and hidden.
        query_names = set(values.keys())
        evidence_names = set(evidents.keys())
        if query_names & evidence_names:
            raise ValueError(
                "A variable cannot appear in both query and evidence: "
                f"{query_names & evidence_names}"
            )

        # Hidden = all network variables that are neither queried nor observed.
        hidden_vars = [
            v for v in self.variables
            if v.name not in query_names and v.name not in evidence_names
        ]

        # Build the fixed part of the assignment (query+evidence) once.
        fixed_assignment: dict[str, str] = {}
        fixed_assignment.update(values)
        fixed_assignment.update(evidents)

        # Numerator: sum_h P(query=values, evidence=evidents, hidden=h).
        numerator = self._sum_joint_over_hidden(fixed_assignment, hidden_vars)

        # Denominator: P(evidence=evidents) = sum over EVERY query assignment
        # AND every hidden assignment. We enumerate the query domain too.
        query_vars = [self.variable_dictionary[name] for name in values.keys()]
        denominator = 0.0
        for query_assignment in self._enumerate_assignments(query_vars):
            qe_assignment: dict[str, str] = {}
            qe_assignment.update(query_assignment)
            qe_assignment.update(evidents)
            denominator += self._sum_joint_over_hidden(qe_assignment, hidden_vars)

        if denominator == 0.0:
            raise ZeroDivisionError(
                "Evidence has probability zero under the network; "
                "conditional probability is undefined."
            )
        return numerator / denominator

    def _sum_joint_over_hidden(
        self,
        fixed_assignment: dict[str, str],
        hidden_vars: list[Variable],
    ) -> float:
        """ Sum the joint probability over every assignment of the hidden
            variables, holding the fixed_assignment (query+evidence) constant.
            Returns sum_h P(fixed_assignment, hidden=h).
        """
        total = 0.0
        for hidden_assignment in self._enumerate_assignments(hidden_vars):
            complete = dict(fixed_assignment)
            complete.update(hidden_assignment)
            total += self.get_joint_probability(complete)
        return total

    def _enumerate_assignments(
        self,
        variables: list[Variable],
    ) -> list[dict[str, str]]:
        """ Yield every dict {var.name: value} over the full Cartesian product
            of the given variables' assignments. Returns [{}] when the list
            is empty (the "no variables to sum over" base case).
        """
        if not variables:
            return [{}]
        # Recursive Cartesian product (small networks — recursion depth bounded).
        head, *tail = variables
        tail_assignments = self._enumerate_assignments(tail)
        out: list[dict[str, str]] = []
        for value in head.assignments.keys():
            for tail_a in tail_assignments:
                row = {head.name: value}
                row.update(tail_a)
                out.append(row)
        return out

    # helper method
    def sub_vals(self, var: Variable, values: dict[str, str]) -> tuple[str, ...]:
        """ return a tuple, contain all the relevant
            assignments for the given variable (i.e - the assignments
            pertaining to the variable`s parents."""
        sub = []
        for p in var.parents:
            sub.append(values[p.name])
        return tuple(sub)
