import math
import unittest

from spline import build_spline, spline_second_derivative, spline_value


class SplineTest(unittest.TestCase):
    def test_example(self):
        xs = [0.0, 1.0, 2.0, 3.0, 4.0]
        fs = [0.0, 1.8415, 2.9093, 3.1411, 3.2432]
        coefs, _ = build_spline(xs, fs)
        expected = [(0.0, 1.9913, 0.0, -0.14983), (1.8415, 1.5418, -0.44949, -0.02450),
                    (2.9093, 0.56934, -0.52299, 0.18548), (3.1411, 0.07978, 0.03344, -0.01115)]
        for got, want in zip(coefs, expected):
            for g, w in zip(got, want):
                self.assertAlmostEqual(g, w, places=3)
        self.assertAlmostEqual(spline_value(xs, coefs, 1.5), 2.4969, delta=1e-4)

    def test_nodes_and_ends(self):
        xs = [0.0, 0.3, 1.1, 1.5, 2.6, 3.0, 4.2]
        fs = [math.sin(x) for x in xs]
        coefs, _ = build_spline(xs, fs)
        n = len(xs) - 1
        for i in range(1, n + 1):
            self.assertAlmostEqual(spline_value(xs, coefs, xs[i - 1], i), fs[i - 1], places=12)
            self.assertAlmostEqual(spline_value(xs, coefs, xs[i], i), fs[i], places=12)
        self.assertAlmostEqual(spline_second_derivative(xs, coefs, xs[0], 1), 0.0, places=12)
        self.assertAlmostEqual(spline_second_derivative(xs, coefs, xs[-1], n), 0.0, places=12)

    def test_two_nodes(self):
        coefs, _ = build_spline([1.0, 3.0], [2.0, 6.0])
        self.assertEqual(coefs[0], (2.0, 2.0, 0.0, 0.0))


if __name__ == "__main__":
    unittest.main()
