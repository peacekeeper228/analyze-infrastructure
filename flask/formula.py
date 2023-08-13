class FormulaPNQD(object):
    def __init__(self, P : float, N: float, Q : float, D : float) -> None:
        self.P = P
        self.N = N
        self.Q = Q
        self.D = D

class calculateD(FormulaPNQD):
    def __init__(self, P : float, N: float, Q : float) -> None:
        super().__init__(P, N, Q, 0.0)

    def calculate(self) -> float:
        return self.P - (self.N * self.Q) / 1000

class calculateP(FormulaPNQD):
    def __init__(self, N: float, Q: float, D: float) -> None:
        super().__init__(0.0, N, Q, D)
    def calculate(self) -> float:
        return (self.N * self.Q) / 1000 + self.D
    
