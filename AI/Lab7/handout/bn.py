from Variable import Variable


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
        """ return the joint probability of the Nodes """
        # TODO: COMPLETE THIS FUNCTION
        # Return join probability
        raise NotImplementedError("get_joint_probability not implemented yet.")

    def get_conditional_probability(self, values: dict[str, str], evidents: dict[str, str]) -> float:
        """ returns the conditional probability.
            Here I do not introduce advanced algorithms for inference (e.g. junctions trees)
            this method implement only simple inference, namely: the joint probability of children given their parents
            or the probability of parents given their children.
            assumption: variables in each level are independent, or independent given their parents
            (i.e vars in values are independent, as well as vars in evidents
        """
        res: float = 1

        # when we want probability of children given their parents
        # if self.varsMap[list(values.keys())[0]].is_child_of(self.varsMap[list(evidents.keys())[0]]):
        first_val = list(values.keys())[0]
        first_variable = self.variable_dictionary[first_val]
        if all(first_variable.is_child_of(self.variable_dictionary[evident]) for evident in evidents.keys()):
            # print('probability of children given their parents')
            for child, c_val in values.items():
                res *= self.variable_dictionary[child].get_conditional_probability(c_val, evidents)

        # when we want probability of parents given their children
        # make use of Bayes rule
        # assumption: nodes in each level are independent, given their parents
        else:
            print('probability of parents given their children')

            joint_marginal_parents = 1
            joint_marginal_children = 1
            joint_conditional_children = 1
            marginal_of_evidents = 1

            # calculating the joint probability of the parents
            for parent, p_val in values.items():
                joint_marginal_parents *= self.variable_dictionary[parent].get_marginal_probability(p_val)

            # calculating the joint probability of the children, and the joint probability
            # of the children given their parents
            for child, c_val in evidents.items():
                joint_marginal_children *= self.variable_dictionary[child].get_marginal_probability(c_val)

                # children given their parents. here the values become the
                # evidents!
                joint_conditional_children *= self.variable_dictionary[child].get_conditional_probability(c_val, values)

                k = list(values.keys())[0]
                complementary_conditional_values = values.copy()
                complementary_conditional_values[k] = 'false' if values[k] == 'true' else 'true'
                marginal_of_evidents = marginal_of_evidents * self.variable_dictionary[
                    child].get_conditional_probability(c_val,
                                                       complementary_conditional_values)

                # print("Child: {}".format(child))
                # print("    Given: {}".format(complementary_conditional_values))

            # uses Bayes rule, for calculating the conditional probability
            res = (joint_conditional_children * joint_marginal_parents) / (
                    (joint_conditional_children * joint_marginal_parents) + marginal_of_evidents *
                    (1 - joint_marginal_parents))

        return res

    # helper method
    def sub_vals(self, var: Variable, values: dict[str, str]) -> tuple[str, ...]:
        """ return a tuple, contain all the relevant
            assignments for the given variable (i.e - the assignments
            pertaining to the variable`s parents."""
        sub = []
        for p in var.parents:
            sub.append(values[p.name])
        return tuple(sub)



