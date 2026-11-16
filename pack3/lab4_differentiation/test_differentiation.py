import unittest

from differentiation import choose_index, first_derivative, first_order, second_derivative


class DifferentiationTest(unittest.TestCase):
    def test_example(self):
        xs = [0.0, 0.1, 0.2, 0.3, 0.4]
        ys = [1.0, 1.1052, 1.2214, 1.3499, 1.4918]
        i = choose_index(xs, 0.2)
        self.assertEqual(i, 1)
        self.assertAlmostEqual(first_order(xs, ys, i), 1.1620, places=4)
        self.assertAlmostEqual(first_order(xs, ys, i + 1), 1.2850, places=4)
        self.assertAlmostEqual(first_derivative(xs, ys, i, 0.2), 1.2235, places=4)
        self.assertAlmostEqual(second_derivative(xs, ys, i), 1.2300, places=4)

    def test_quadratic_exact(self):
        xs = [0.0, 0.5, 1.5, 2.0, 3.0]
        ys = [3 * x * x - x + 2 for x in xs]
        for x in (0.3, 1.0, 1.7, 2.5):
            i = choose_index(xs, x)
            self.assertAlmostEqual(first_derivative(xs, ys, i, x), 6 * x - 1, places=10)
            self.assertAlmostEqual(second_derivative(xs, ys, i), 6.0, places=10)

    def test_edges(self):
        xs = [0.0, 1.0, 2.0, 3.0]
        self.assertEqual(choose_index(xs, 0.0), 0)
        self.assertEqual(choose_index(xs, 3.0), 1)
        with self.assertRaises(ValueError):
            choose_index(xs, 3.5)


if __name__ == "__main__":
    unittest.main()
