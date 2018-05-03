#!./mac_env/bin/python3

import csv


class transition:

    def __init__(self, val, str=None, out=None, tmp=False):
        self.isTmp = tmp
        self.val = val
        self.str = str
        self.output = out
        self.C = None
        self.P = None
        self.R = None
        self.E = None


class cfa:

    def __init__(self):
        self.q = None
        self.in_alpha = None
        self.out_alpha = None
        self.delta = dict()
        self.lam = None
        self.initial_state = None
        self.reward = []
        self.punish = []
        self.confidence = None
        self.expect = None

        self.q_curr = 0
        self.q_last = 0
        self.a_last = 'e'
        self.o = 'e'
        self.o_last = 'e'
        self.q_anchor = 0

        self.state_count = 0

    # Get data
    # Set alphabet
    # Return: Steps
    @property
    def setup(self):
        f = open("data/test.csv", newline='')
        steps = []
        done = False  # To help get the steps when it gets past the header
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if done:
                steps.append(row)
            if row[0] == "delta":
                self.parse_delta(row)
                # Make sure always count after you enter the state into Delta so th b
                # So the count will stay true.
                self.state_count += 1
            if row[0] == "in":
                self.in_alpha = row[1:]
            if row[0] == "out":
                self.out_alpha = row[1:]
                done = True
        return steps

    def is_trans_defined(self, t):
        for conn in self.delta[self.q_curr]:
            if conn.val == t:
                return True
        return False

    def get_trans_index(self, t):
        for e, conn in enumerate(self.delta[self.q_curr]):
            if conn.val == t:
                return e
        raise ValueError("Could not find transition index, Program failed")

    def create_new_transition(self, I):
        if self.is_trans_defined((self.q_curr, 'e')):
            del (self.delta[self.q_curr][self.get_trans_index((self.q_curr, 'e'))])
        for input in I:
            if not self.is_trans_defined((self.q_curr, input[0])):
                try:
                    self.delta[self.q_curr].append(transition((self.q_curr, input[0]), input[1], self.state_count))
                except:
                    self.delta[self.q_curr] = [transition((self.q_curr, input[0]), input[1], self.state_count)]

                self.delta[self.state_count] = [transition((self.state_count, 'e'), 50, self.q_anchor, True)]

                # Loop through State_count implicit so you don't look at the just created state
                index = len(self.delta[self.q_curr]) - 1
                found = False
                for n in range(self.state_count):
                    for state in self.delta[n]:
                        if state.val[1] == input[0]:
                            self.delta[self.q_curr][index].C = state.C
                            #self.delta[self.q_curr][index].P = state.P
                            if state in self.punish:
                                self.punish.append(self.delta[self.q_curr][index])
                            elif state in self.reward:
                                self.reward.append(self.delta[self.q_curr][index])
                            found = True
                            break
                # Final Else in create new Trans
                if not found:
                    self.delta[self.q_curr][index].C = 0.1
                # This needs to be at the end. You finally Crated a new state.
                self.state_count += 1



    # In source file, to create a inital transition function the template looks as follows
    # delta, state, input, output, strength
    # This function parses that out and creates a transition object out of it.
    def parse_delta(self, row):
        try:
            self.delta[int(row[1])].append(transition((row[1], row[2]), row[4], row[3]))
        except:
            self.delta[int(row[1])] = [transition((row[1], row[2]), row[4], row[3])]

    def run(self):
        I = []
        # Abstraction of time for the use of simulation.
        time = 0
        steps = self.setup
        gamma = 15  # TODO I don't know what this should equal at start

        for s in steps:
            s_time = s[0]

            # STEP 2
            if (int(s_time) - time) > gamma:
                if self.is_trans_defined((self.q_curr, 'e')):
                    # Get the 'e' Transition and marks it permanent
                    self.delta[self.q_curr][self.get_trans_index((self.q_curr, 'e'))].isTmp = False
                self.q_anchor = self.q_curr
                self.q_curr = (self.q_curr, 'e')

            q_anchor = self.q_curr
            self.a_last = 'e'
            self.o_last = 'e'

            # TODO Unmark All symbols b and distributions p ^ delta _ q,a
            # TODO Loop back to STEP 2

            t = steps[0][0]
            I = []
            I_last = I
            # Step 3
            # Get list of strength Symbols. IN this case a list of transition objects
            for e, s in enumerate(steps):
                if s[0] is t:
                    I.append((s[1], s[2]))
                else:
                    del steps[0:e]
                    break

            # Step 4
            I = sorted(I, key=lambda x: x[1], reverse=True)

            # Step 5
            # Create New Transition TODO <---
            self.create_new_transition(I)

            self.o_last = self.o





def main():
    t = cfa()
    t.run()


if __name__ == "__main__":
    main()
