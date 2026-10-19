import random
import unittest

from lu import SingularMatrixError, determinant, inverse, lu_decompose, solve
from matrix import identity, matmul, matvec, max_abs_diff


class LUTest(unittest.TestCase):
    def test_zero_on_diagonal(self):
        a = [[0.0, 1.0], [2.0, 3.0]]
        lu = lu_decompose(a)
        self.assertEqual(lu.swaps, 1)
        self.assertAlmostEqual(determinant(lu), -2.0)
        x = solve(lu, [1.0, 8.0])
        self.assertAlmostEqual(x[0], 2.5)
        self.assertAlmostEqual(x[1], 1.0)

    def test_singular(self):
        with self.assertRaises(SingularMatrixError):
            lu_decompose([[1.0, 2.0], [2.0, 4.0]])

    def test_random(self):
        rng = random.Random(42)
        for n in (1, 3, 5, 10):
            a = [[rng.uniform(-10, 10) for _ in range(n)] for _ in range(n)]
            x_true = [rng.uniform(-5, 5) for _ in range(n)]
            b = matvec(a, x_true)
            lu = lu_decompose(a)

            pa = matmul(lu.permutation_matrix(), a)
            self.assertLess(max_abs_diff(matmul(lu.L, lu.U), pa), 1e-9)
            self.assertLess(max(abs(p - q) for p, q in zip(solve(lu, b), x_true)), 1e-7)
            self.assertLess(max_abs_diff(matmul(a, inverse(lu)), identity(n)), 1e-7)


if __name__ == "__main__":
    unittest.main()
