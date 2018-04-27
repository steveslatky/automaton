#!./mac_env/bin/python3


class cfa:

    def __init__(self):
        q = None
        in_alpha = []
        out_alpha = []
        trans_fun = None
        lam = None
        initial_state = None
        rewards = None
        punish = []
        confidence = None
        expect = None



    def setup(self):
        f = open("../data/test.csv")
        steps = []
        done = False
        for row in f:
            if row[0:2] == "in":
                tmp_alpha = row[3:].strip("\n").lstrip(' ')
                self.in_alpha = tmp_alpha.split(',')
            if row[0:3] == "out":
                tmp_alpha = row[4:].strip("\n").lstrip(" ")
                self.out_alpha = tmp_alpha.split(',')
                done = True
            if done:
                steps.append(row)
        return steps




if __name__ == "__main__":
    t = cfa()
    print(t.setup())



