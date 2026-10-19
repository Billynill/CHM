import random
import unittest

from gauss import gauss
from iterative import seidel, simple_iteration, to_iteration_form


class IterativeTest(unittest.TestCase):
    def test_random_dominant(self):
        rng = random.Random(7)
        for n in (1, 3, 6, 15):
            a = [[rng.uniform(-5, 5) for _ in range(n)] for _ in range(n)]
            for i in range(n):
                a[i][i] = sum(abs(a[i][j]) for j in range(n) if j != i) + rng.uniform(1, 5)
            x_true = [rng.uniform(-10, 10) for _ in range(n)]
            b = [sum(a[i][j] * x_true[j] for j in range(n)) for i in range(n)]

            alpha, beta = to_iteration_form(a, b)
            for method in (simple_iteration, seidel):
                x, _ = method(alpha, beta, 1e-6)
                self.assertLess(max(abs(u - v) for u, v in zip(x, x_true)), 1e-5)
            self.assertLess(max(abs(u - v) for u, v in zip(gauss(a, b), x_true)), 1e-9)

    def test_zero_diagonal(self):
        with self.assertRaises(ValueError):
            to_iteration_form([[0, 1], [1, 0]], [1, 1])


if __name__ == "__main__":
    unittest.main()
