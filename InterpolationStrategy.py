import numpy as np
class InterpolationStrategy:
    def __init__(self, P:np.array):
        self.P = P
        self.N = self.getSize()
        self.t = np.linspace(0, 1, 500)[:, np.newaxis]

    def getSize(self) -> int:
        return self.P.shape[0]

    def interpolate(self) -> np.array:
        pass

    def __array__(self):
        return self.interpolate()