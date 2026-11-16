import math
import unittest

from integration import (grid, left_rectangles, middle_rectangles, right_rectangles, runge_romberg,
                         simpson, trapezoid)


def example(x):
    return x / (3 * x + 4) ** 2


class IntegrationTest(unittest.TestCase):
    def test_example(self):
        g1, g2 = grid(-1, 1, 0.5), grid(-1, 1, 0.25)
        self.assertAlmostEqual(trapezoid(example, g1, 0.5), -0.27663, places=5)
        self.assertAlmostEqual(trapezoid(example, g2, 0.25), -0.19789, places=5)
        self.assertAlmostEqual(simpson(example, g1, 0.5), -0.20558, places=5)
        self.assertAlmostEqual(simpson(example, g2, 0.25), -0.17164, places=5)
        refined, _ = runge_romberg(trapezoid(example, g2, 0.25), trapezoid(example, g1, 0.5), 2, 2)
        self.assertAlmostEqual(refined, -0.17164, places=5)

    def test_simpson_exact_for_cubic(self):
        f = lambda x: x ** 3 - 2 * x + 1
        g = grid(0, 2, 0.5)
        self.assertAlmostEqual(simpson(f, g, 0.5), 4 - 4 + 2, places=12)

    def test_orders(self):
        exact = 1 - math.cos(1)
        errors = {}
        for method in (left_rectangles, right_rectangles, middle_rectangles, trapezoid, simpson):
            e1 = abs(method(math.sin, grid(0, 1, 0.1), 0.1) - exact)
            e2 = abs(method(math.sin, grid(0, 1, 0.05), 0.05) - exact)
            errors[method.__name__] = e1 / e2
        self.assertAlmostEqual(errors["left_rectangles"], 2, delta=0.2)
        self.assertAlmostEqual(errors["middle_rectangles"], 4, delta=0.2)
        self.assertAlmostEqual(errors["trapezoid"], 4, delta=0.2)
        self.assertAlmostEqual(errors["simpson"], 16, delta=1)

    def test_simpson_odd(self):
        with self.assertRaises(ValueError):
            simpson(math.sin, grid(0, 3, 1), 1)


if __name__ == "__main__":
    unittest.main()
