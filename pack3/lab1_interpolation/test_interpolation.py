import math
import unittest

from interpolation import divided_differences, lagrange, newton


class InterpolationTest(unittest.TestCase):
    def test_example_lagrange(self):
        xs = [0.1, 0.5, 0.9, 1.3]
        ys = [math.log(x) for x in xs]
        self.assertAlmostEqual(lagrange(xs, ys, 0.8), -0.20036, places=5)

    def test_example_newton(self):
        xs = [0.0, 1.0, 2.0, 3.0]
        ys = [math.sin(math.pi / 6 * x) for x in xs]
        table = divided_differences(xs, ys)
        self.assertAlmostEqual(table[3][0], -0.01635, places=5)
        self.assertAlmostEqual(newton(xs, table, 1.5), 0.70589, places=5)

    def test_methods_equal(self):
        xs = [-2.0, -0.5, 1.0, 2.5, 4.0, 5.0]
        ys = [math.exp(x / 3) for x in xs]
        table = divided_differences(xs, ys)
        for x in (-1.0, 0.3, 3.7):
            self.assertAlmostEqual(lagrange(xs, ys, x), newton(xs, table, x), places=10)

    def test_polynomial_exact(self):
        xs = [0.0, 1.0, 2.0, 3.0]
        ys = [x ** 3 - 2 * x for x in xs]
        self.assertAlmostEqual(lagrange(xs, ys, 1.7), 1.7 ** 3 - 3.4, places=10)


if __name__ == "__main__":
    unittest.main()
