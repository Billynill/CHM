def gauss_solve(a, b):
    n = len(a)
    m = [a[i][:] + [b[i]] for i in range(n)]

    for k in range(n):
        pivot = max(range(k, n), key=lambda i: abs(m[i][k]))
        if abs(m[pivot][k]) < 1e-14:
            raise ZeroDivisionError("Нормальная система вырождена")
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


def normal_system(xs, ys, degree):
    # (3.17): sum_i a_i * sum_j x_j^(k+i) = sum_j y_j * x_j^k,  k = 0..n
    matrix = [[sum(x ** (k + i) for x in xs) for i in range(degree + 1)] for k in range(degree + 1)]
    rhs = [sum(y * x ** k for x, y in zip(xs, ys)) for k in range(degree + 1)]
    return matrix, rhs


def fit(xs, ys, degree):
    matrix, rhs = normal_system(xs, ys, degree)
    return gauss_solve(matrix, rhs), matrix, rhs


def poly_value(coefs, x):
    return sum(a * x ** i for i, a in enumerate(coefs))


def sum_squared_errors(coefs, xs, ys):
    # (3.15)
    return sum((poly_value(coefs, x) - y) ** 2 for x, y in zip(xs, ys))


def poly_string(coefs):
    text = f"{coefs[0]:.5f}"
    for i, a in enumerate(coefs[1:], start=1):
        power = "x" if i == 1 else f"x^{i}"
        text += f" {'-' if a < 0 else '+'} {abs(a):.5f}{power}"
    return text
