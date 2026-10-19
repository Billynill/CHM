import math

from matrix import identity, matmul, transpose


def is_symmetric(a, tol=1e-12):
    n = len(a)
    return all(abs(a[i][j] - a[j][i]) <= tol for i in range(n) for j in range(i + 1, n))


def off_diagonal_norm(a):
    # t(A) = sqrt(сумма квадратов элементов выше диагонали)
    n = len(a)
    return math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n)))


def max_off_diagonal(a):
    n = len(a)
    best_i, best_j = 0, 1
    for i in range(n):
        for j in range(i + 1, n):
            if abs(a[i][j]) > abs(a[best_i][best_j]):
                best_i, best_j = i, j
    return best_i, best_j


def rotation_angle(a, i, j):
    if a[i][i] == a[j][j]:
        return math.pi / 4
    return 0.5 * math.atan(2 * a[i][j] / (a[i][i] - a[j][j]))


def rotation_matrix(n, i, j, phi):
    u = identity(n)
    c, s = math.cos(phi), math.sin(phi)
    u[i][i] = c
    u[j][j] = c
    u[i][j] = -s
    u[j][i] = s
    return u


def jacobi_rotation(a, eps, max_iter=10000):
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("Матрица должна быть квадратной")
    if not is_symmetric(a):
        raise ValueError("Метод вращений применим только к симметричным матрицам")

    a_k = [row[:] for row in a]
    v = identity(n)
    history = []

    if n == 1:
        return [a_k[0][0]], v, history

    for k in range(1, max_iter + 1):
        i, j = max_off_diagonal(a_k)
        phi = rotation_angle(a_k, i, j)
        u = rotation_matrix(n, i, j, phi)

        # A(k+1) = U^T * A(k) * U,  V = U0 * U1 * ... * Uk
        a_k = matmul(matmul(transpose(u), a_k), u)
        v = matmul(v, u)

        t = off_diagonal_norm(a_k)
        history.append((k, i, j, phi, t))
        if t < eps:
            eigenvalues = [a_k[m][m] for m in range(n)]
            return eigenvalues, v, history

    raise RuntimeError(f"Метод не сошёлся за {max_iter} итераций")
