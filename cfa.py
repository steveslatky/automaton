#!./mac_env/bin/python3

import csv


class transition:

    def __init__(self, val, tmp=True):
        self.isTmp = tmp
        self.val = val
        self.str = None



class cfa:

    def __init__(self):
        self.q = None
        self.in_alpha = None
        self.out_alpha = None
        self.delta = None
        self.lam = None
        self.initial_state = None
        self.rewards = None
        self.punish = []
        self.confidence = None
        self.expect = None

        self.q_curr = 0
        self.q_last = 0
        self.a_last = 'e'
        self.o = 'e'
        self.o_last = 'e'

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
        for e,conn in enumerate(self.delta[self.q_curr]):
            if conn.val == t:
                return e
        raise ValueError("Could not find transition index, Program failed")

    def create_new_transition(self, I):
        if self.is_trans_defined((self.q_curr, 'e')):
            del (self.delta[self.q_curr][self.delta[self.q_curr].index(tt)])




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
                self.q_last = self.q_curr
                self.q_curr = (self.q_curr, 'e')

            q_anchor = self.q_curr
            self.a_last = 'e'
            self.o_last = 'e'

            # TODO Unmark All symbols b and distributions p ^ delta _ q,a
            # TODO Loop back to STEP 2

            # Step 3
            # Get list of strength Symbols. IN this case a list of transition objects
            I_last = I
            I = self.delta[self.q_curr]

            # Step 4
            I = sorted(I, key=lambda x : x.str, reverse=True)

            # Step 5
            # Create New Transition




def main():
    t = cfa()
    t.run()


if __name__ == "__main__":
    main()
