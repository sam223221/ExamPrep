"""
LAB 7: Bayesian Networks (inference) — Variable module
======================================================

PROBLEM STATEMENT (from Lab 7.pdf):
-----------------------------------
Exercise 1: Familiarize yourself with the code in bn.py, Runner.py and
Variable.py. Complete bn.py and Variable.py to calculate the probabilities
for the Bayesian network of the classic "Sprinkler / Cloudy / Rain / Wet
Grass" example. The Sprinkler network is defined as:

    Cloudy:    P(Cloudy=F)=0.5, P(Cloudy=T)=0.5
    Sprinkler: P(S | Cloudy=F)=(0.5, 0.5);  P(S | Cloudy=T)=(0.9, 0.1)
    Rain:      P(R | Cloudy=F)=(0.8, 0.2);  P(R | Cloudy=T)=(0.2, 0.8)
    WetGrass:  P(W | R=F,S=F)=(1, 0);   P(W | R=F,S=T)=(0.1, 0.9)
               P(W | R=T,S=F)=(0.1, 0.9); P(W | R=T,S=T)=(0.01, 0.99)

The required computations are:
    - Marginal probability P(X)        for each variable X
    - Joint probability   P(X1, ..., Xn) of any complete assignment
    - Conditional         P(query | evidence)

Homework Exercise (also covered): a 6-node car-diagnosis network with
roots Damaged Tire (DT), Electronics Malfunctioning (EM), Fuel Tank
Leaking (FTL) and observable symptoms Vibrations (V), Slow Max Speed
(SMS), High Consumption (HC). See Runner_solution.py.

MENTAL MODEL (one-line analogy):
--------------------------------
A Bayesian network is a gossip graph: each person (node) hears rumors
only from their direct parents (the CPT says "given what my parents
believe, here's how likely I am to believe X"). The marginal P(X) is
"how often does X end up believing it overall, before we ask anyone for
evidence?" — computed by summing over every parent rumor weighted by
how likely that rumor is. The conditional P(X | evidence) is "now that
we KNOW some people in the graph, what should X believe?"

REFERENCES:
-----------
- Lecture L09a §3 (Core Concepts): Bayesian network, CPT, chain rule.
- Lecture L09a §4 (Algorithms): inference by enumeration.
- Glossary: Bayesian network, Conditional probability table (CPT),
  Joint probability distribution, Marginal probability,
  Conditional probability, Chain rule, Markov condition.
- See study/lectures/L09a-Bayesian-Networks.md once locked.

HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS:
--------------------------------------------------
This file is a HELPER MODULE — it has no problem-specific tunables.
It implements the math of marginal probability for any node in any
Bayesian network. To adapt to a different question:
  - To switch which Bayesian network is queried: edit Runner_solution.py
    (NETWORK_CHOICE knob).
  - To add a new node / change CPT values / change evidence / change
    the query: see the KNOBs in Runner_solution.py.
  - No edits to this file are needed for any variant in the exam bank.

OUTPUTS WHEN RUN:
-----------------
This module is not directly executed. It is imported by bn_solution.py
and Runner_solution.py.

ENTRY POINT: no
---------------
Helper module. The entry point is Runner_solution.py.
"""

from typing import Self
import functools


def multiply_vector_elements(vector):
    """ return the multiplication of the vector elements """

    def mult(x, y):
        return x * y

    return functools.reduce(mult, vector, 1)


class Variable(object):
    """ Node in the network. Represent a random Variable """

    def __init__(self, name: str, assignments: tuple[str, ...],
                 probability_table: dict[tuple[str, ...], tuple[float, ...]], parents: list[Self] = None,
                 children: list[Self] = None):
        """ Node initialization
            params:
            name: name of this random variable.
            assignments: possible values this variable can have.
            probability_table: the causal probability table of this variable.
            parents: list of references to this Node`s parents.
            children: list of references to this Node`s children.
        """

        if parents is None:
            parents = []

        # the name of this random variable
        self.name = name

        # holds the possible assignments of this random variable
        # assume certain order
        self.assignments: dict[str, int] = {}
        for i in range(len(assignments)):
            self.assignments[assignments[i]] = i

        # holds the distribution table of this random variable
        for key, val in probability_table.items():
            if len(val) != len(assignments):
                # self = None
                raise ValueError('data in probability table is inconsistent with possible assignments')

        self.probability_table: dict[tuple[str, ...], tuple[float, ...]] = probability_table

        # list of dependent variables
        self.children: list[Variable] = children if children is not None else []

        # list of variables which this variable depends upon
        self.parents: list[Variable] = parents

        # holds the marginal, pre-calculated probability to obtain each
        # possible value
        self.marginal_probabilities: list[float] = len(assignments) * [0]

        # indicates whether this node is ready to use
        # true when the marginal probabilities were calculated
        self.ready: bool = False

        self.calculate_marginal_probability()

    def get_name(self) -> str:
        """ return the name of this random variable """
        return self.name

    def get_assignments(self) -> dict[str, int]:
        """ return the possible values this variable can have """
        return self.assignments

    def get_assignment_index(self, assignment: str) -> int:
        """ returns the index of a given possible assignment within the assignments list """
        return self.assignments[assignment]

    def get_probability(self, value: str, parents_values: tuple[str, ...]) -> float:
        """ read from the distribution table and return the probability of having a
            certain value (value) given the values of the parents.
        """
        return self.probability_table[parents_values][self.assignments[value]]

    def get_conditional_probability(self, value: str, parents_values: dict[str, str]) -> float:
        """ read from the distribution table and return the probability of having a
            certain value (value) given the values of the parents.
            here the parents assignments can be partial
            parent_vals is a dictionary: { parent: value }
        """
        res: float = 0
        given_parents_index = []
        marginal_parents_index = []
        for i, v in enumerate(self.parents):
            if v.name in parents_values:
                given_parents_index.append((i, parents_values[v.name]))
            else:
                marginal_parents_index.append(i)

        # go over the rows in the distribution table
        for row_key, row_val in self.probability_table.items():
            valid_row = 1

            # check if this row should count for the marginal conditional
            # probability
            for gpi in given_parents_index:
                if row_key[gpi[0]] != gpi[1]:
                    valid_row = 0
                    break

            # if this row is valid, add the corresponding conditional
            # probability
            if valid_row:
                parents_probability = 1
                for mpi in marginal_parents_index:
                    parents_probability *= self.parents[mpi].get_marginal_probability(row_key[mpi])

                res += row_val[self.assignments[value]] * parents_probability
        return res

    def calculate_marginal_probability(self):
        """ Calculate and store the marginal probabilities of this node by
            EXACT enumeration over all ancestors.

            Algorithm (Lecture L09a §3.13):
                P(X = v) = sum_{a in ancestor-assignments} P(X = v, A = a)
            where the inner term is the chain-rule product of the relevant
            CPT cells (this node's row plus each ancestor's row, given that
            ancestor's parents within the assignment).

            Why this replaces "product of parent marginals":
                When two parents share an ancestor (e.g. Sprinkler and Rain
                both have parent Cloudy), the joint marginal P(parent1,
                parent2) is NOT the product P(parent1) * P(parent2). The old
                approach silently assumed marginal independence between
                parents and produced wrong numbers on the canonical Sprinkler
                example. Enumerating ancestors makes the calculation exact.

            Topological-order assumption: the caller (BayesianNetwork.
            calculate_marginal_probabilities) walks the variable list in
            declaration order, which the builders guarantee is topological.
            Each ancestor is therefore `ready` by the time we look at it.
        """

        # return, if already done — marginals are stable once computed
        if self.ready:
            return

        # Re-initialise the accumulator (defensive in case of re-computation).
        n_values = len(self.assignments)
        self.marginal_probabilities = [0.0] * n_values

        # Root nodes: their CPT has the single key () and IS the marginal.
        if not self.parents:
            row = next(iter(self.probability_table.values()))
            for value, idx in self.assignments.items():
                self.marginal_probabilities[idx] = row[idx]
            self.ready = True
            return

        # Non-root nodes: enumerate every assignment of this node's full
        # ancestor set, build the joint P(this=value, ancestors=assignment)
        # via the chain rule, and accumulate.
        ancestors = self._collect_ancestors()
        # Order ancestors topologically (each appears after all of its own
        # parents) so chain-rule lookups always have their parents resolved.
        ancestors_topo = self._topological_sort(ancestors)

        for ancestor_assignment in self._enumerate(ancestors_topo):
            # Joint probability of the ancestor assignment by chain rule.
            ancestor_joint = 1.0
            for anc in ancestors_topo:
                anc_parents_vals = tuple(
                    ancestor_assignment[p.name] for p in anc.parents
                )
                ancestor_joint *= anc.probability_table[anc_parents_vals][
                    anc.assignments[ancestor_assignment[anc.name]]
                ]

            # This node's row given its own parents in this assignment.
            row_key = tuple(ancestor_assignment[p.name] for p in self.parents)
            row_val = self.probability_table[row_key]
            for value, idx in self.assignments.items():
                self.marginal_probabilities[idx] += row_val[idx] * ancestor_joint

        # set this Node`s state to ready
        self.ready = True

    def _collect_ancestors(self) -> list["Variable"]:
        """ Return every ancestor of this node (parents, grandparents, ...).
            Used by exact marginal enumeration so that shared ancestors are
            counted once and parent correlations are honoured.
        """
        seen: dict[str, "Variable"] = {}
        stack: list["Variable"] = list(self.parents)
        while stack:
            node = stack.pop()
            if node.name in seen:
                continue
            seen[node.name] = node
            stack.extend(node.parents)
        return list(seen.values())

    @staticmethod
    def _topological_sort(nodes: list["Variable"]) -> list["Variable"]:
        """ Order the given nodes so that every node appears AFTER all its
            parents within the set. Standard Kahn-style ordering.
        """
        names = {n.name for n in nodes}
        ordered: list[Variable] = []
        placed: set[str] = set()
        remaining = list(nodes)
        while remaining:
            progress = False
            for node in list(remaining):
                # Only count parents that are within the ancestor set.
                if all(p.name not in names or p.name in placed for p in node.parents):
                    ordered.append(node)
                    placed.add(node.name)
                    remaining.remove(node)
                    progress = True
            if not progress:
                # Cycle — shouldn't happen in a DAG. Append what's left.
                ordered.extend(remaining)
                break
        return ordered

    @staticmethod
    def _enumerate(variables: list["Variable"]) -> list[dict[str, str]]:
        """ Yield every dict {var.name: value} over the Cartesian product
            of the given variables' assignments. Returns [{}] for an empty
            input (the base case for the recursion).
        """
        if not variables:
            return [{}]
        head, *tail = variables
        tail_rows = Variable._enumerate(tail)
        out: list[dict[str, str]] = []
        for value in head.assignments.keys():
            for tail_a in tail_rows:
                row = {head.name: value}
                row.update(tail_a)
                out.append(row)
        return out

    def get_marginal_probability(self, val: str) -> float:
        """ returns the marginal probability, to have a certain value """
        return self.marginal_probabilities[self.assignments[val]]

    def add_child(self, node):
        """ add dependent Variable to this variable """
        self.children.append(node)

    def add_parent(self, node):
        """ add a parent to this Variable """
        self.parents.append(node)

    def get_parents(self):
        """ returns the parent list """
        return self.parents

    def get_children(self):
        """ returns the children list """
        return self.children

    def is_child_of(self, node) -> bool:
        """ return True iff this Node is a DIRECT child of the given Node
            (i.e. node is in self.parents). Does not check transitive
            ancestry — use a full d-separation walk for that.
        """
        for var in self.parents:
            if var.name == node.name:
                return True
        return False
