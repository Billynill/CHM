EPS = 1e-12


def check_diagonal_dominance(a, b, c):
    # |b_i| >= |a_i| + |c_i| для всех i и строго хотя бы для одного
    strict = False
    for i in range(len(b)):
        side = abs(a[i]) + abs(c[i])
        if abs(b[i]) < side:
            return False
        if abs(b[i]) > side:
            strict = True
    return strict


def thomas(a, b, c, d):
    n = len(b)
    p = [0.0] * n
    q = [0.0] * n

    # прямой ход
    for i in range(n):
        denom = b[i] + (a[i] * p[i - 1] if i > 0 else 0.0)
        if abs(denom) < EPS:
            raise ZeroDivisionError(f"Нулевой знаменатель на шаге {i + 1}, прогонка неприменима")
        p[i] = -c[i] / denom
        q[i] = (d[i] - (a[i] * q[i - 1] if i > 0 else 0.0)) / denom

    # обратный ход
    x = [0.0] * n
    x[-1] = q[-1]
    for i in range(n - 2, -1, -1):
        x[i] = p[i] * x[i + 1] + q[i]

    return p, q, x


def multiply(a, b, c, x):
    # A*x, где A задана тремя диагоналями
    n = len(b)
    result = []
    for i in range(n):
        s = b[i] * x[i]
        if i > 0:
            s += a[i] * x[i - 1]
        if i < n - 1:
            s += c[i] * x[i + 1]
        result.append(s)
    return result
