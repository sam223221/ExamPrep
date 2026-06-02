from enum import Enum
from typing import Self


class Symbols(Enum):
    X = "X"
    O = "O"
    UNPLACED = "i"

    def __str__(self):
        return self.value

    @classmethod
    def placed(cls) -> tuple[Self, Self]:
        return cls.X, cls.O


type Board = list[Symbols]


def minmax_decision(state: Board) -> int:
    """
    returns the action of the opponent for the current state of board
    :param state: State of the checkerboard. Ex: [Unplaced; Unplaced; Unplaced; Unplaced; X; Unplaced; Unplaced; Unplaced; Unplaced]
    :return: the action number in range [0-8]
    """
    def max_value(state_option: Board) -> int:
        if is_terminal(state_option):
            return utility_of(state_option)
        expected_value = -infinity
        for (a, s) in successors_of(state_option):
            expected_value = max(expected_value, min_value(s))
        return expected_value

    def min_value(state_option: Board) -> int:
        if is_terminal(state_option):
            return utility_of(state_option)
        expected_value = infinity
        for (a, s) in successors_of(state_option):
            expected_value = min(expected_value, max_value(s))
        return expected_value

    infinity = float('inf')
    action, state = max(successors_of(state), key=lambda a: min_value(a[1]))
    return action


def is_terminal(state: Board) -> bool:
    """
    returns True if the state is either a win or a tie (board full)
    :param state: State of the checkerboard. Ex: [Unplaced; Unplaced; Unplaced; Unplaced; X; Unplaced; Unplaced; Unplaced; Unplaced]
    :return:
    """
    ## TODO ##
    # A state is terminal if someone has won OR the board is full.
    # Use the two helper functions below.
    # return ____(state) is not None or ____(state)
    ##########
    raise NotImplementedError("Implement this function")


def utility_of(state: Board) -> int:
    """
    returns +1 if winner is X (MAX player), -1 if winner is O (MIN player), or 0 otherwise
    :param state: State of the checkerboard.  Ex: [Unplaced; Unplaced; Unplaced; Unplaced; X; Unplaced; Unplaced; Unplaced; Unplaced]
    :return:
    """
    ## TODO ##
    # winner = ____(state)
    # if winner == ____:
    #     return +1
    # elif winner == ____:
    #     return -1
    # else:
    #     return ____
    ##########
    raise NotImplementedError("Implement this function")


# ---------- HELPER: check for a winner ----------

def winner_of(state: Board):
    """
    Returns the winning symbol (Symbols.X or Symbols.O) if someone has three
    in a row, or None if no one has won yet.

    Board layout (positions 0-8):
        0 | 1 | 2
        ---------
        3 | 4 | 5
        ---------
        6 | 7 | 8

    Checks all 8 winning lines:
      - 3 rows:      [0,1,2], [3,4,5], [6,7,8]
      - 3 columns:   [0,3,6], [1,4,7], [2,5,8]
      - 2 diagonals: [0,4,8], [2,4,6]
    """
    ## TODO ##
    # Check rows — starting indices are 0, 3, 6
    # for c in [0, 3, 6]:
    #     if state[c] == state[____] == state[____] and state[c] != Symbols.UNPLACED:
    #         return state[c]
    #
    # Check columns — starting indices are 0, 1, 2  (hint: stride is 3)
    #
    # Check diagonals — positions [0,4,8] and [2,4,6]
    #
    # return None
    ##########
    raise NotImplementedError("Implement this function")


# ---------- HELPER: check if board is full ----------

def is_full_board(state: Board) -> bool:
    """
    Returns True if every cell on the board has been filled (no UNPLACED left).
    A full board with no winner means the game is a draw.
    """
    ## TODO ##
    # return all(____ for cell in state)
    ##########
    raise NotImplementedError("Implement this function")


# ---------- STUDENT IMPLEMENTATIONS ----------

def successors_of(state: Board) -> list[tuple[int, Board]]:
    """
    returns a list of tuples (move, state) as shown in the exercise slides
    :param state: State of the checkerboard. Ex: [Unplaced; Unplaced; Unplaced; Unplaced; X; Unplaced; Unplaced; Unplaced; Unplaced]
    :return: [(move, state),...]
    """
    ## TODO ##
    # Step 1: Count how many cells are UNPLACED
    # open_count = sum(1 for cell in state if cell == ____)
    #
    # Step 2: Determine whose turn it is
    #   X goes first (9 open = odd). After X plays, 8 open = even → O's turn.
    # if open_count % 2 == 1:
    #     player = ____   # X makes odd-numbered moves
    # else:
    #     player = ____   # O makes even-numbered moves
    #
    # Step 3: For each UNPLACED position, create a successor
    # successors = []
    # for move in range(9):
    #     if state[move] == ____:
    #         successor = state[:]          # copy the board!
    #         successor[move] = ____        # place the current player
    #         successors.append((move, successor))
    # return successors
    ##########
    raise NotImplementedError("Implement this function")


def display(state: list[Symbols]) -> None:
    print("-----")
    for i in range(0, 3):
        for c in range(i * 3, i * 3 + 3):
            print("|", end="")
            symbol = c if state[c] == Symbols.UNPLACED else state[c]
            print(symbol, end="")
        print("|")


def main():
    board = [Symbols.UNPLACED] * 9
    while not is_terminal(board):
        board[minmax_decision(board)] = Symbols.X
        if not is_terminal(board):
            display(board)
            board[int(input('Your move? '))] = Symbols.O
    display(board)

    result = winner_of(board)
    if result is None:
        print("Game is over. No winner")
    else:
        print("Game is over. The winner is:", result)


if __name__ == '__main__':
    main()
