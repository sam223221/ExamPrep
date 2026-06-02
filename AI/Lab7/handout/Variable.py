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
        """ calculates and stores the marginal probabilities of this node.
            this function should be called before any other calculation is done.
        """

        # return, if already done
        if self.ready:
            return

        # TODO: COMPLETE THIS FUNCTION
        # Set self.marginal_probabilities
        raise NotImplementedError("calculate_marginal_probability not implemented yet.")

        # set this Node`s state to ready
        self.ready = True

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

    def is_child_of(self, node):
        """ return boolean, indicating whether this Node is a child of a given
            Node
        """
        for var in self.parents:
            if var.name == node.name:
                return 1
        return 0
