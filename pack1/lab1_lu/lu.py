from dataclasses import dataclass
from typing import List

from matrix import copy_matrix, identity, zeros

EPS = 1e-12


class SingularMatrixError(ValueError):
    pass


@dataclass
class LUDecomposition:
    L: list
    U: list
    perm: List[int]
    swaps: int

    @property
    def size(self):
        return len(self.U)

    def permutation_matrix(self):
        n = self.size
        p = zeros(n, n)
        for i, j in enumerate(self.perm):
            p[i][j] = 1.0
        return p


def lu_decompose(a):
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("Матрица должна быть квадратной")

    u = copy_matrix(a)
    l = zeros(n, n)
    perm = list(range(n))
    swaps = 0

    for k in range(n):
        # выбор главного элемента по столбцу
        pivot_row = max(range(k, n), key=lambda i: abs(u[i][k]))## выбор опорного эл-та
        if abs(u[pivot_row][k]) < EPS:
            raise SingularMatrixError("Матрица вырождена")

        if pivot_row != k: # перестановка строк
            u[k], u[pivot_row] = u[pivot_row], u[k]
            l[k][:k], l[pivot_row][:k] = l[pivot_row][:k], l[k][:k]
            perm[k], perm[pivot_row] = perm[pivot_row], perm[k]
            swaps += 1

        for i in range(k + 1, n): #прямой ход гаусса
            factor = u[i][k] / u[k][k]
            l[i][k] = factor
            for j in range(k, n):
                u[i][j] -= factor * u[k][j]
            u[i][k] = 0.0

    for i in range(n):
        l[i][i] = 1.0

    return LUDecomposition(L=l, U=u, perm=perm, swaps=swaps)


def forward_substitution(l, b): 
    # L*y = b
    n = len(l)
    y = [0.0] * n
    for i in range(n):
        y[i] = b[i] - sum(l[i][j] * y[j] for j in range(i))
    return y


def back_substitution(u, y):
    # U*x = y
    n = len(u)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = sum(u[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (y[i] - s) / u[i][i]
    return x


def solve(lu, b):
    if len(b) != lu.size:
        raise ValueError("Размер b не совпадает с размером матрицы")
    pb = [b[p] for p in lu.perm]
    y = forward_substitution(lu.L, pb)
    return back_substitution(lu.U, y)


def inverse(lu):
    n = lu.size
    e = identity(n)
    columns = [solve(lu, e[i]) for i in range(n)]
    return [[columns[j][i] for j in range(n)] for i in range(n)]


def determinant(lu):
    det = -1.0 if lu.swaps % 2 else 1.0
    for i in range(lu.size):
        det *= lu.U[i][i]
    return det
