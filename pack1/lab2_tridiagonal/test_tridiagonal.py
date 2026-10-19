import random
import unittest

from tridiagonal import check_diagonal_dominance, multiply, thomas


class ThomasTest(unittest.TestCase):
    def test_small(self):
        # 2x1 + x2 = 3, x1 + 2x2 = 3  ->  x = (1, 1)
        _, _, x = thomas([0, 1], [2, 2], [1, 0], [3, 3])
        self.assertAlmostEqual(x[0], 1.0)
        self.assertAlmostEqual(x[1], 1.0)

    def test_random(self):
        rng = random.Random(1)
        for n in (1, 2, 5, 50):
            a = [0.0] + [rng.uniform(-5, 5) for _ in range(n - 1)]
            c = [rng.uniform(-5, 5) for _ in range(n - 1)] + [0.0]
            b = [abs(a[i]) + abs(c[i]) + rng.uniform(1, 5) for i in range(n)]
            x_true = [rng.uniform(-10, 10) for _ in range(n)]
            d = multiply(a, b, c, x_true)

            self.assertTrue(check_diagonal_dominance(a, b, c))
            _, _, x = thomas(a, b, c, d)
            self.assertLess(max(abs(u - v) for u, v in zip(x, x_true)), 1e-9)

    def test_zero_denominator(self):
        with self.assertRaises(ZeroDivisionError):
            thomas([0, 1], [0, 1], [1, 0], [1, 1])


if __name__ == "__main__":
    unittest.main()
