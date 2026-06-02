import numpy as np
from numpy import ndarray

"""
Hidden Markov Model using Viterbi algorithm to find most
likely sequence of hidden states.

The problem is to find out the most likely sequence of states
of the weather (hot, cold) from a description of the number
of ice cream eaten by a boy in the summer.
"""


def main():
    np.set_printoptions(suppress=True)

    states = np.array(["initial", "hot", "cold", "final"])

    # To simulate starting from index 1, we add a dummy value at index 0
    # observation_sets = [
    #     [None, 3, 1, 3],
    #     [None, 3, 3, 1, 1, 2, 2, 3, 1, 3],
    #     [None, 3, 3, 1, 1, 2, 3, 3, 1, 2],
    # ]
    observation_sets = [
        [None, 3, 1, 3],
        [None, 3, 3, 1, 1, 2, 2, 3, 1, 3],
        [None, 3, 3, 1, 1, 2, 3, 3, 1, 2],
    ]

    # Markov transition matrix
    #
    # prob_of_next = transitions[current][next]
    # index 0 = start
    # index 1 = hot
    # index 2 = cold
    # index 3 = end      to:  S   h   c   e     from:
    transitions = np.array([[.0, .8, .2, .0],  # Initial state
                            [.0, .2, .6, .2],  # Hot state
                            [.0, .3, .5, .2],  # Cold state
                            [.0, .0, .0, .0],  # Final state
                            ])

    # P(v|q)
    # emission[state][observation]
    # probality_of_this_amount_of_icecreams_given_weather = emission[state (weather)][observation (number of icecreams)]
    #                      0    1   2   3
    emissions = np.array([[.0, .0, .0, .0],  # Initial state
                          [.0, .1, .15, .75],  # Hot state
                          [.0, .8, .1, .1],  # Cold state
                          [.0, .0, .0, .0],  # Final state
                          ])

    for observations in observation_sets:
        print("Observations: {}".format(' '.join(map(str, observations[1:]))))

        probability = compute_forward(states, observations, transitions, emissions)
        print("Probability: {}".format(probability))

        path = compute_viterbi(states, observations, transitions, emissions)
        print(f"Path: {convert_path_states_to_observations(path, states)}")

        print('')


def convert_path_states_to_observations(path: list[int], states: ndarray[str]) -> list[str]:
    return [states[p] for p in path]


def inclusive_range(a: int, b: int) -> range:
    return range(a, b + 1)


def compute_forward(states: ndarray, observations: list[int | None], a_transitions: ndarray,
                    b_emissions: ndarray[float]) -> float:
    # number of states - subtract two because "initial" and "final" doesn't count.
    big_n = len(states) - 2

    # number of observations - subtract one, because a dummy "None" is added on index 0.
    big_t = len(observations) - 1

    # final state
    qf: int = big_n + 1

    # probability matrix - all values initialized to 5, as 0 has meaning in the matrix
    forward: ndarray = np.ones((big_n + 2, big_t + 1)) * 5

    raise NotImplementedError("compute_forward is not finished")


def compute_viterbi(states: ndarray, observations: list[int | None], a_transitions: ndarray, b_emissions: ndarray):
    # number of states - subtract two because "initial" and "final" doesn't count.
    big_n = len(states) - 2

    # number of observations - subtract one, because a dummy "None" is added on index 0.
    big_t = len(observations) - 1

    # final state
    qf = big_n + 1

    # probability matrix - all values initialized to 5, as 0 is valid value in matrix
    viterbi = np.ones((big_n + 2, big_t + 1)) * 5

    # Must be of type int, otherwise it is tricky to use its elements to index
    # the states
    # all values initialized to 5, as 0 is valid value in matrix
    backpointers = np.ones((big_n + 2, big_t + 1), dtype=int) * 5

    raise NotImplementedError("Compute viterbi is not finished")


def argmax(sequence: list[tuple[float, float]]):
    '''
    This takes in a list, that provides its own keys as tuples.
    As such the following must hold true:
    sequence[i] = tuple(key, value)
    '''
    # I have rewritten this function slightly, to make it make better sense in my head
    return max(sequence, key=lambda x: x[1])[0]


if __name__ == '__main__':
    main()
