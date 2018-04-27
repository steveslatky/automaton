#!./mac_env/bin/python3

import csv


class cfa:

    def __init__(self):
        q = None
        in_alpha = None
        out_alpha = None
        trans_fun = None
        lam = None
        initial_state = None
        rewards = None
        punish = []
        confidence = None
        expect = None

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


if __name__ == "__main__":
    t = cfa()
    print(t.setup)
    print(t.in_alpha)
    print(t.out_alpha)
