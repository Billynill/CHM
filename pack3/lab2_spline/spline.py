def thomas(a, b, c, d):
    n = len(b)
    p = [0.0] * n
    q = [0.0] * n
    for i in range(n):
        denom = b[i] + (a[i] * p[i - 1] if i > 0 else 0.0)
        p[i] = -c[i] / denom
        q[i] = (d[i] - (a[i] * q[i - 1] if i > 0 else 0.0)) / denom

    x = [0.0] * n
    if n == 0:
        return x
    x[-1] = q[-1]
    for i in range(n - 2, -1, -1):
        x[i] = p[i] * x[i + 1] + q[i]
    return x


def build_spline(xs, fs):
    # индексы как в методичке: участки i = 1..n, h_i = x_i - x_(i-1)
    n = len(xs) - 1
    h = [0.0] + [xs[i] - xs[i - 1] for i in range(1, n + 1)]

    # система (3.13) для c_2..c_n
    sub, diag, sup, rhs = [], [], [], []
    for i in range(2, n + 1):
        sub.append(h[i - 1] if i > 2 else 0.0)
        diag.append(2 * (h[i - 1] + h[i]))
        sup.append(h[i] if i < n else 0.0)
        rhs.append(3 * ((fs[i] - fs[i - 1]) / h[i] - (fs[i - 1] - fs[i - 2]) / h[i - 1]))

    c = [0.0, 0.0] + thomas(sub, diag, sup, rhs)

    # формулы (3.14)
    coefs = []
    for i in range(1, n + 1):
        a_i = fs[i - 1]
        if i < n:
            b_i = (fs[i] - fs[i - 1]) / h[i] - h[i] * (c[i + 1] + 2 * c[i]) / 3
            d_i = (c[i + 1] - c[i]) / (3 * h[i])
        else:
            b_i = (fs[n] - fs[n - 1]) / h[n] - 2 * h[n] * c[n] / 3
            d_i = -c[n] / (3 * h[n])
        coefs.append((a_i, b_i, c[i], d_i))

    system = {"sub": sub, "diag": diag, "sup": sup, "rhs": rhs}
    return coefs, system


def find_interval(xs, x):
    if x < xs[0] or x > xs[-1]:
        raise ValueError(f"точка {x} вне отрезка [{xs[0]}, {xs[-1]}]")
    for i in range(1, len(xs)):
        if x <= xs[i]:
            return i
    return len(xs) - 1


def spline_value(xs, coefs, x, i=None):
    if i is None:
        i = find_interval(xs, x)
    a, b, c, d = coefs[i - 1]
    t = x - xs[i - 1]
    return a + b * t + c * t ** 2 + d * t ** 3


def spline_second_derivative(xs, coefs, x, i):
    a, b, c, d = coefs[i - 1]
    return 2 * c + 6 * d * (x - xs[i - 1])
