import cmath
import math

from matrix import identity, matmul


def sign(x):
    return -1.0 if x < 0 else 1.0


def householder_matrix(a, k):
    # H = E - 2 * v * v^T / (v^T * v), обнуляет столбец k под диагональю
    n = len(a)
    v = [0.0] * n
    col_norm = math.sqrt(sum(a[i][k] ** 2 for i in range(k, n)))
    v[k] = a[k][k] + sign(a[k][k]) * col_norm
    for i in range(k + 1, n):
        v[i] = a[i][k]

    vv = sum(x * x for x in v)
    h = identity(n)
    if vv == 0:
        return h
    for i in range(n):
        for j in range(n):
            h[i][j] -= 2 * v[i] * v[j] / vv
    return h


def qr_decompose(a):
    n = len(a)
    q = identity(n)
    r = [row[:] for row in a]
    for k in range(n - 1):
        h = householder_matrix(r, k)
        r = matmul(h, r)
        q = matmul(q, h)
    return q, r


def column_norm_below(a, col, start_row):
    return math.sqrt(sum(a[i][col] ** 2 for i in range(start_row, len(a))))


def block_eigenvalues(a, i):
    # собственные значения блока 2x2 в строках/столбцах i, i+1
    p = a[i][i] + a[i + 1][i + 1]
    q = a[i][i] * a[i + 1][i + 1] - a[i][i + 1] * a[i + 1][i]
    d = cmath.sqrt(p * p - 4 * q)
    return (p + d) / 2, (p - d) / 2


def extract_eigenvalues(a, eps):
    # возвращает список собственных значений или None, если структура ещё не сошлась
    n = len(a)
    values = []
    i = 0
    while i < n:
        if i == n - 1 or column_norm_below(a, i, i + 1) < eps:
            values.append(complex(a[i][i]))
            i += 1
        elif column_norm_below(a, i, i + 2) < eps:
            lam1, lam2 = block_eigenvalues(a, i)
            if lam1.imag == 0:
                # корни вещественные — блок должен распасться, итерируем дальше
                return None
            values.extend((lam1, lam2))
            i += 2
        else:
            return None
    return values


def qr_algorithm(a, eps, max_iter=10000):
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("Матрица должна быть квадратной")

    a_k = [row[:] for row in a]
    prev = None

    for k in range(1, max_iter + 1):
        q, r = qr_decompose(a_k)
        a_k = matmul(r, q)

        current = extract_eigenvalues(a_k, eps)
        if current is not None and prev is not None and len(current) == len(prev):
            if all(abs(x - y) < eps for x, y in zip(current, prev)):
                return current, a_k, k
        prev = current

    raise RuntimeError(f"QR-алгоритм не сошёлся за {max_iter} итераций")
