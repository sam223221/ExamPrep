from enum import Enum, auto


class States(Enum):
    WA = 1
    NT = 2
    Q = 3
    NSW = 4
    V = 5
    SA = 6
    T = 7

    def __lt__(self, other):
        if type(other) != type(self):
            return False

        return self.value < other.value

    def __eq__(self, other):
        if type(other) != type(self):
            return False

        return self.value == other.value

    def __hash__(self):
        return hash(repr(self))


