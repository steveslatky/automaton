class push_down:

    def __init__(self, Q = None, Sigma = None, Gamma = None, delta = None, q0 = None, Z = None, F = None ):
        self.Q = Q
        self.Sigma = Sigma
        self.Gamma = Gamma
        self.delta = delta
        self.q0 = q0
        self.Z = Z
        self.F = F


    def accept(self):
        pass

# Could I Make an abstact class of automata
