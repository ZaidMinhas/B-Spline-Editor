
import numpy as np
from InterpolationStrategy import InterpolationStrategy


class BSplineStrategy(InterpolationStrategy):

    def __init__(self, P: np.array, t: np.array = None):
        super().__init__(P)
        if t is not None:
            self.t = t[:, np.newaxis]  # Allow custom t values if provided
        self.k = 4  # Cubic B-spline (degree + 1)
        self.knots = self._generate_knots()
        self._basis_cache = {}  # Memoization cache for basis function results

    def _generate_knots(self) -> np.array:
        # Uniform clamped knot vector
        if self.N < 4:
            return None

        n = self.N - 1
        return np.concatenate((np.zeros(3), np.linspace(0, 1, n - 1), np.ones(3)))

    def _basis_function(self, i: int, k: int, t: float) -> float:
        # Check if the result is already cached
        if (i, k, t) in self._basis_cache:
            return self._basis_cache[(i, k, t)]

        if k == 1:
            result = 1.0 if self.knots[i] <= t < self.knots[i + 1] else 0.0
        else:
            left_num = t - self.knots[i]
            left_den = self.knots[i + k - 1] - self.knots[i]
            right_num = self.knots[i + k] - t
            right_den = self.knots[i + k] - self.knots[i + 1]

            left = (left_num / left_den) * self._basis_function(i, k - 1, t) if left_den != 0 else 0.0
            right = (right_num / right_den) * self._basis_function(i + 1, k - 1, t) if right_den != 0 else 0.0

            result = left + right

        # Cache the result
        self._basis_cache[(i, k, t)] = result
        return result

    def interpolate(self) -> np.array:
        if self.knots is None:
            return np.empty((0, 2))  # Handle case with too few control points

        curve = np.zeros((len(self.t), self.P.shape[1]))

        # Vectorize the loop over `t` values
        for j, t in enumerate(self.t.flatten()):
            basis_values = np.array([self._basis_function(i, self.k, t) for i in range(self.N)])
            curve[j] = np.sum(basis_values[:, np.newaxis] * self.P, axis=0)

        return curve
