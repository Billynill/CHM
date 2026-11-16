import math
import unittest

from expression import make_system
from methods import newton, simple_iteration


class SystemsTest(unittest.TestCase):
    def test_circle_and_line(self):
        system = make_system(["x1^2 + x2^2 - 2", "x1 - x2"], {})
        for method in (newton, simple_iteration):
            x = method(system, [1.5, 0.5], 1e-10)[0]
            self.assertAlmostEqual(x[0], 1.0, places=7)
            self.assertAlmostEqual(x[1], 1.0, places=7)

    def test_three_equations(self):
        system = make_system(["x1 + x2 + x3 - 6", "x1*x2 - 2", "x3^2 - 9"], {})
        x, _ = newton(system, [1.2, 1.8, 2.5], 1e-10)
        for got, want in zip(x, (1, 2, 3)):
            self.assertAlmostEqual(got, want, places=7)

    def test_params(self):
        system = make_system(["x1 - cos(x2) - a", "x2 - sin(x1) - a"], {"a": 1})
        x, _ = newton(system, [1.0, 1.0], 1e-12)
        self.assertAlmostEqual(x[0] - math.cos(x[1]), 1, places=9)
        self.assertAlmostEqual(x[1] - math.sin(x[0]), 1, places=9)


if __name__ == "__main__":
    unittest.main()
