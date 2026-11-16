import math
import unittest

from boundary import finite_difference, grid, shooting


class BoundaryTest(unittest.TestCase):
    def test_shooting_example(self):
        # пример 4.9: y'' = e^x + sin(y), y(0) = 1, y(1) = 2
        xs = grid(0, 1, 0.1)
        ys, _, history = shooting(lambda x, y, z: math.exp(x) + math.sin(y), xs, 0.1,
                                  (1, 0, 1), (1, 0, 2), 1.0, 0.8, 1e-6)
        self.assertAlmostEqual(history[-1][0], -0.1608625, places=4)
        self.assertAlmostEqual(ys[5], 1.17434, places=4)
        self.assertAlmostEqual(ys[-1], 2.0, places=5)

    def test_finite_difference_example(self):
        # пример 4.10 (в методичке фактически p(x) = x): y(0) = 1, y'(1) + 2y(1) = 0, h = 0.2
        xs = grid(0, 1, 0.2)
        ys, _ = finite_difference(lambda x: x, lambda x: -1, lambda x: 0, xs, 0.2, (1, 0, 1), (2, 1, 0))
        for got, want in zip(ys, (1.0, 0.77191, 0.58303, 0.43111, 0.31265, 0.22332)):
            self.assertAlmostEqual(got, want, places=4)

    def test_variant_accuracy(self):
        exact = lambda x: math.exp(x) / x
        left, right = (0, 1, 0), (1.5, 1, math.exp(2))
        xs = grid(1, 2, 0.1)
        ys, _, _ = shooting(lambda x, y, z: y - 2 / x * z, xs, 0.1, left, right, 1.0, 0.8, 1e-10)
        self.assertLess(max(abs(y - exact(x)) for x, y in zip(xs, ys)), 1e-5)

        errors = []
        for h in (0.02, 0.01):
            xs = grid(1, 2, h)
            ys, _ = finite_difference(lambda x: 2 / x, lambda x: -1, lambda x: 0, xs, h, left, right)
            errors.append(max(abs(y - exact(x)) for x, y in zip(xs, ys)))
        self.assertAlmostEqual(errors[0] / errors[1], 2, delta=0.3)


if __name__ == "__main__":
    unittest.main()
