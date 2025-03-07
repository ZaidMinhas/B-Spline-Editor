import numpy as np
from InterpolationStrategy import InterpolationStrategy

class LinearStrategy(InterpolationStrategy):
    def interpolate(self) -> np.array:
        t = self.t
        all_points = np.empty((0,2))
        for i in range(self.N-1):
            P1 = self.P[i+1]
            P0 = self.P[i]

            points = P1*t + P0*(1-t)
            all_points = np.vstack((all_points, points))

        return all_points