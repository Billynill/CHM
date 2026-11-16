import math
import unittest

from expression import parse_function
from methods import localize_roots, newton, simple_iteration, tabulate


class MethodsTest(unittest.TestCase):
    def test_sqrt2(self):
        f = lambda x: x * x - 2
        x, _, _ = simple_iteration(f, 1, 2, 1e-8)
        self.assertAlmostEqual(x, math.sqrt(2), places=6)
        x, _ = newton(f, 1, 2, 1e-10)
        self.assertAlmostEqual(x, math.sqrt(2), places=9)

    def test_localize(self):
        f = parse_function("sin(x)")
        segments = localize_roots(tabulate(f, 1, 10, 0.5))
        self.assertEqual(len(segments), 3)

    def test_parser(self):
        f = parse_function("2^x - x^2 - 0.5")
        self.assertAlmostEqual(f(2), -0.5)
        with self.assertRaises(ValueError):
            parse_function("__import__('os')")

    def test_newton_faster(self):
        f = lambda x: math.cos(x) + 0.25 * x - 0.5
        _, hist_si, _ = simple_iteration(f, 0.5, 2, 1e-8)
        _, hist_nt = newton(f, 0.5, 2, 1e-8)
        self.assertLess(len(hist_nt), len(hist_si))


if __name__ == "__main__":
    unittest.main()
