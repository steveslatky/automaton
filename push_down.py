from collections import deque


class push_down:

    def accept(self, delta, q0, F, stack, input):
        state = q0
        for c in input:
            state = delta[state][c]
            if state[1] is not 'e':
                stack.append(state[1])
            elif state[1] is 'e':
                stack.pop()

        return state in F


if __name__ == '__main__':
    z = push_down()
    s = deque()

    # dfa = {0: {'0': 0, '1': 1},
    #        1: {'0': 2, '1': 0},
    #        2: {'0': 1, '1': 2}}

    # L = {0^n1^n | n >= 0}
    delta = {0: {'e': (1('e', 'z'))},
             1: {'0': (1.('e', '0')), '1': (2, ('0', 'e'))},
             2: {'1': (2, ('0', 'e')), 'e': (3, ('z', 'e'))},
             3: {}}
