import random
import unittest

from jacobi import jacobi_rotation
from matrix import diag, matmul, max_abs_diff


class JacobiTest(unittest.TestCase):
    def test_diagonal(self):
        values, _, history = jacobi_rotation([[2.0, 0.0], [0.0, 5.0]], 1e-6)
        self.assertEqual(sorted(values), [2.0, 5.0])

    def test_known_2x2(self):
        # собственные значения [[2, 1], [1, 2]] равны 1 и 3
        values, _, _ = jacobi_rotation([[2.0, 1.0], [1.0, 2.0]], 1e-9)
        self.assertAlmostEqual(sorted(values)[0], 1.0)
        self.assertAlmostEqual(sorted(values)[1], 3.0)

    def test_random_symmetric(self):
        rng = random.Random(3)
        for n in (1, 3, 5, 8):
            a = [[0.0] * n for _ in range(n)]
            for i in range(n):
                for j in range(i, n):
                    a[i][j] = a[j][i] = rng.uniform(-10, 10)
            values, v, _ = jacobi_rotation(a, 1e-10)
            self.assertLess(max_abs_diff(matmul(a, v), matmul(v, diag(values))), 1e-8)

    def test_not_symmetric(self):
        with self.assertRaises(ValueError):
            jacobi_rotation([[1.0, 2.0], [3.0, 4.0]], 0.01)


if __name__ == "__main__":
    unittest.main()
