def gauss_solve(a, b):
    n = len(a)
    m = [a[i][:] + [b[i]] for i in range(n)]

    for k in range(n):
        pivot = max(range(k, n), key=lambda i: abs(m[i][k]))
        if abs(m[pivot][k]) < 1e-14:
            raise ZeroDivisionError("Матрица Якоби вырождена")
        m[k], m[pivot] = m[pivot], m[k]
        for i in range(k + 1, n):
            factor = m[i][k] / m[k][k]
            for j in range(k, n + 1):
                m[i][j] -= factor * m[k][j]

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = sum(m[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (m[i][n] - s) / m[i][i]
    return x


def inverse(a):
    n = len(a)
    columns = [gauss_solve(a, [1.0 if i == j else 0.0 for i in range(n)]) for j in range(n)]
    return [[columns[j][i] for j in range(n)] for i in range(n)]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def matvec(a, x):
    return [sum(a_ij * x_j for a_ij, x_j in zip(row, x)) for row in a]


def vector_norm(v):
    return max(abs(x) for x in v)


def matrix_norm(m):
    return max(sum(abs(x) for x in row) for row in m)
