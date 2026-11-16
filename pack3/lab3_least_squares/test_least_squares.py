import unittest

from least_squares import fit, poly_value, sum_squared_errors


class LeastSquaresTest(unittest.TestCase):
    def setUp(self):
        self.xs = [0.0, 1.7, 3.4, 5.1, 6.8, 8.5]
        self.ys = [0.0, 1.3038, 1.8439, 2.2583, 2.6077, 2.9155]

    def test_example_degree1(self):
        coefs, _, _ = fit(self.xs, self.ys, 1)
        expected = [0.4713, 1.0114, 1.5515, 2.0916, 2.6317, 3.1718]
        for x, want in zip(self.xs, expected):
            self.assertAlmostEqual(poly_value(coefs, x), want, places=3)

    def test_example_degree2(self):
        coefs, _, _ = fit(self.xs, self.ys, 2)
        expected = [0.1295, 1.0798, 1.8250, 2.3651, 2.7000, 2.8299]
        for x, want in zip(self.xs, expected):
            self.assertAlmostEqual(poly_value(coefs, x), want, places=3)

    def test_exact_polynomial(self):
        xs = [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0]
        ys = [2 - x + 0.5 * x ** 3 for x in xs]
        coefs, _, _ = fit(xs, ys, 3)
        for got, want in zip(coefs, (2, -1, 0, 0.5)):
            self.assertAlmostEqual(got, want, places=9)
        self.assertAlmostEqual(sum_squared_errors(coefs, xs, ys), 0.0, places=12)


if __name__ == "__main__":
    unittest.main()
