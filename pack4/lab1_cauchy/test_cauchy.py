import math
import unittest

from cauchy import adams, euler, grid, make_system, runge_kutta


def exact(x):
    return math.cos(x) + 11 / 8 * math.sin(x) - math.sin(3 * x) / 8


class CauchyTest(unittest.TestCase):
    def setUp(self):
        self.system = make_system(lambda x, y, z: math.sin(3 * x) - y)

    def max_error(self, method, h):
        xs = grid(0, 1, h)
        vs = method(self.system, xs, [1.0, 1.0], h)
        return max(abs(v[0] - exact(x)) for x, v in zip(xs, vs))

    def test_orders(self):
        self.assertAlmostEqual(self.max_error(euler, 0.02) / self.max_error(euler, 0.01), 2, delta=0.2)
        self.assertAlmostEqual(self.max_error(runge_kutta, 0.1) / self.max_error(runge_kutta, 0.05), 16, delta=2)
        self.assertAlmostEqual(self.max_error(adams, 0.02) / self.max_error(adams, 0.01), 16, delta=3)

    def test_accuracy(self):
        self.assertLess(self.max_error(runge_kutta, 0.1), 1e-5)
        self.assertLess(self.max_error(adams, 0.1), 1e-3)

    def test_harmonic(self):
        system = make_system(lambda x, y, z: -y)
        xs = grid(0, math.pi, math.pi / 100)
        vs = runge_kutta(system, xs, [0.0, 1.0], math.pi / 100)
        self.assertAlmostEqual(vs[-1][0], 0.0, places=7)
        self.assertAlmostEqual(vs[-1][1], -1.0, places=7)


if __name__ == "__main__":
    unittest.main()
