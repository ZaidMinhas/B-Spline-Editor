import numpy as np
from InterpolationStrategy import InterpolationStrategy


def Lerp(P0, P1, t):
    return P0*(1-t) + P1*t

class BezierStrategy(InterpolationStrategy):
    def interpolate(self) -> np.array:
        all_points = np.empty((0, 2))
        if (self.N -4) % 3 != 0:
            return all_points

        for i in range(0, self.N, 4):
            if i > 3:
                i -= 1
            t = self.t
            P0 = self.P[i]
            P1 = self.P[i+1]
            P2 = self.P[i+2]
            P3 = self.P[i+3]

            points = ((1-t)**3)*P0 + 3*((1-t)**2)*t*P1 + 3*(1-t)*(t**2)*P2 + (t**3)*P3
            all_points = np.vstack((all_points, points))

        return all_points
