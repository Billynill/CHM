def make_system(f):
    # y'' = f(x, y, y')  ->  y' = z,  z' = f(x, y, z)   (4.21)
    def system(x, v):
        y, z = v
        return [z, f(x, y, z)]
    return system


def grid(a, b, h):
    n = round((b - a) / h)
    if n < 1 or abs(n * h - (b - a)) > 1e-9:
        raise ValueError(f"шаг h = {h} не укладывается целое число раз в [{a}, {b}]")
    return [a + k * h for k in range(n + 1)]


def euler(system, xs, v0, h):
    # (4.2): v(k+1) = v(k) + h * F(x(k), v(k))
    vs = [list(v0)]
    for k in range(len(xs) - 1):
        v = vs[-1]
        dv = system(xs[k], v)
        vs.append([v[i] + h * dv[i] for i in range(len(v))])
    return vs


def rk4_step(system, x, v, h):
    # (4.16)
    n = len(v)
    k1 = [h * d for d in system(x, v)]
    k2 = [h * d for d in system(x + h / 2, [v[i] + k1[i] / 2 for i in range(n)])]
    k3 = [h * d for d in system(x + h / 2, [v[i] + k2[i] / 2 for i in range(n)])]
    k4 = [h * d for d in system(x + h, [v[i] + k3[i] for i in range(n)])]
    return [v[i] + (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6 for i in range(n)]


def runge_kutta(system, xs, v0, h):
    vs = [list(v0)]
    for k in range(len(xs) - 1):
        vs.append(rk4_step(system, xs[k], vs[-1], h))
    return vs


def adams(system, xs, v0, h):
    # первые 3 шага методом Рунге-Кутты, дальше (4.25)
    start = min(4, len(xs))
    vs = runge_kutta(system, xs[:start], v0, h)
    fs = [system(xs[k], vs[k]) for k in range(len(vs))]
    n = len(v0)
    for k in range(3, len(xs) - 1):
        v = [vs[k][i] + h / 24 * (55 * fs[k][i] - 59 * fs[k - 1][i] + 37 * fs[k - 2][i] - 9 * fs[k - 3][i])
             for i in range(n)]
        vs.append(v)
        fs.append(system(xs[k + 1], v))
    return vs


METHODS = [
    ("Эйлер", euler, 1),
    ("Рунге-Кутта 4", runge_kutta, 4),
    ("Адамс 4", adams, 4),
]


def runge_romberg(y_h, y_2h, p):
    # (4.11): R = (y^h - y^(2h)) / (2^p - 1)
    return (y_h - y_2h) / (2 ** p - 1)
