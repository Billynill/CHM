import random
import unittest

from matrix import identity, matmul, max_abs_diff
from qr import qr_algorithm, qr_decompose


def transpose(a):
    return [list(row) for row in zip(*a)]


class QRTest(unittest.TestCase):
    def test_decompose_random(self):
        rng = random.Random(5)
        for n in (1, 2, 4, 7):
            a = [[rng.uniform(-10, 10) for _ in range(n)] for _ in range(n)]
            q, r = qr_decompose(a)
            self.assertLess(max_abs_diff(matmul(q, r), a), 1e-10)
            self.assertLess(max_abs_diff(matmul(transpose(q), q), identity(n)), 1e-10)
            for i in range(n):
                for j in range(i):
                    self.assertLess(abs(r[i][j]), 1e-10)

    def test_real_eigenvalues(self):
        values, _, _ = qr_algorithm([[2.0, 1.0], [1.0, 2.0]], 1e-8)
        self.assertEqual(sorted(round(v.real, 6) for v in values), [1.0, 3.0])

    def test_complex_eigenvalues(self):
        # [[0, -1], [1, 0]] — поворот на 90 градусов, lambda = ±i
        values, _, _ = qr_algorithm([[0.0, -1.0], [1.0, 0.0]], 1e-8)
        self.assertEqual(sorted(round(v.imag, 6) for v in values), [-1.0, 1.0])


if __name__ == "__main__":
    unittest.main()
