import random
from pprint import pformat

from Variable import Variable
from bn import BayesianNetwork


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


def sprinkler_network():
    # the values kept as dictionary
    cloudy_probabilities = {(): (0.5, 0.5)}
    sprinkler_probabilities = {('false',): (0.5, 0.5), ('true',): (0.9, 0.1)}
    rain_probabilities = {('false',): (0.8, 0.2), ('true',): (0.2, 0.8)}
    wet_grass_probabilities = {
        ('false', 'false'): (1, 0),
        ('true', 'false'): (0.1, 0.9),
        ('false', 'true'): (0.1, 0.9),
        ('true', 'true'): (0.01, 0.99)
    }

    # creation of Nodes objects
    cloudy = Variable('Cloudy', ('false', 'true'), cloudy_probabilities)
    sprinkler = Variable('Sprinkler', ('false', 'true'), sprinkler_probabilities, [cloudy])
    rain = Variable('Rain', ('false', 'true'), rain_probabilities, [cloudy])
    wetgrass = Variable('WetGrass', ('false', 'true'), wet_grass_probabilities, [sprinkler, rain])

    variables = [cloudy, sprinkler, rain, wetgrass]

    # creation of Network
    network = BayesianNetwork()
    network.set_variables(variables)

    # pre-calculate marginals
    network.calculate_marginal_probabilities()

    print_marginal_probabilities(network)

    print('')

    joint_values = {
        'Sprinkler': 'true',
        'Cloudy': 'false',
        'WetGrass': 'true',
        'Rain': 'false'
    }
    print_joint_probability(network, joint_values)

    print('')

    conditionals_vars = {'Sprinkler': 'true'}
    conditionals_evidents = {'WetGrass': 'true'}

    print_conditional_probability(network, conditionals_vars, conditionals_evidents)

    print('')

    sample = create_random_sample(network)
    print_joint_probability(network, sample)


if __name__ == '__main__':
    sprinkler_network()
