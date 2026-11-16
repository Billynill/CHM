def grid(a, b, h):
    n = round((b - a) / h)
    if n < 1 or abs(n * h - (b - a)) > 1e-9:
        raise ValueError(f"шаг h = {h} не укладывается целое число раз в [{a}, {b}]")
    return [a + i * h for i in range(n + 1)]


def left_rectangles(f, xs, h):
    return h * sum(f(x) for x in xs[:-1])


def right_rectangles(f, xs, h):
    return h * sum(f(x) for x in xs[1:])


def middle_rectangles(f, xs, h):
    # (3.23)
    return h * sum(f((xs[i - 1] + xs[i]) / 2) for i in range(1, len(xs)))


def trapezoid(f, xs, h):
    # (3.25)
    ys = [f(x) for x in xs]
    return h * (ys[0] / 2 + sum(ys[1:-1]) + ys[-1] / 2)


def simpson(f, xs, h):
    # (3.28): h/3 * [y0 + 4y1 + 2y2 + 4y3 + ... + 4y(N-1) + yN], N чётное
    n = len(xs) - 1
    if n % 2 != 0:
        raise ValueError("для метода Симпсона число отрезков должно быть чётным")
    ys = [f(x) for x in xs]
    total = ys[0] + ys[-1]
    for i in range(1, n):
        total += (4 if i % 2 == 1 else 2) * ys[i]
    return h / 3 * total


METHODS = [
    ("Левые прямоугольники", left_rectangles, 1),
    ("Правые прямоугольники", right_rectangles, 1),
    ("Средние прямоугольники", middle_rectangles, 2),
    ("Трапеции", trapezoid, 2),
    ("Симпсон", simpson, 4),
]


def runge_romberg(f_h, f_kh, k, p):
    # (3.30): F = F_h + (F_h - F_kh) / (k^p - 1)
    correction = (f_h - f_kh) / (k ** p - 1)
    return f_h + correction, abs(correction)
