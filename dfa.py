from utils import *


class DFA:

    def __init__(self, d, q0, f):
        self.delta = d  # Transition function
        self.q_0 = q0  # Initial State
        self.F = f  # Final State

    def accepts(self, input):
        state = self.q_0
        for c in input:
            state = self.delta[state][c]
        return state in self.F

if __name__ == '__main__':

    dfa = {0: {'0': 0, '1': 1},
           1: {'0': 2, '1': 0},
           2: {'0': 1, '1': 2}}

    z = DFA(dfa, 0, {0})
    print(z.accepts('101101'))

    print(z.accepts('101101011'))

    print(z.accepts('00'))

    ps = powerset(['a', 'b'])

    for i in ps:
        print(i)

    dfa2 = {0: {'a': 0, 'b': 1},
            1: {'a': 0, 'b': 2},
            2: {'a': 3, 'b': 0},
            3: {'a': 3, 'b': 3}}

    abba_test = DFA(dfa2, 0, {3})

    print(abba_test.accepts('abbbbbbbbbbbbbbbbbbbbbbb'))