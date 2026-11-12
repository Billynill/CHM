H = 1e-5


def derivative(f, x):
    return (f(x + H) - f(x - H)) / (2 * H)


def second_derivative(f, x):
    return (f(x + H) - 2 * f(x) + f(x - H)) / (H * H)


def safe(f, x):
    try:
        return f(x)
    except (ValueError, ZeroDivisionError, OverflowError):
        return None


def tabulate(f, a, b, step):
    points = []
    x = a
    while x <= b + 1e-12:
        points.append((x, safe(f, x)))
        x = round(x + step, 12)
    return points


def localize_roots(points):
    # отрезки, на концах которых f меняет знак
    segments = []
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        if y1 is None or y2 is None:
            continue
        if y1 == 0:
            segments.append((x1, x1))
        elif y1 * y2 < 0:
            segments.append((x1, x2))
    return segments


def derivative_bounds(f, a, b, samples=200):
    values = [derivative(f, a + (b - a) * i / samples) for i in range(samples + 1)]
    return min(values), max(values)


def simple_iteration(f, a, b, eps, max_iter=10000):
    # x = phi(x),  phi(x) = x - f(x) / k
    d_min, d_max = derivative_bounds(f, a, b)
    if d_min * d_max <= 0:
        raise ValueError("f'(x) меняет знак на отрезке, phi построить нельзя")

    m, big_m = min(abs(d_min), abs(d_max)), max(abs(d_min), abs(d_max))
    k = big_m if d_max > 0 else -big_m
    q = 1 - m / big_m  # max|phi'(x)| на отрезке

    def phi(x):
        return x - f(x) / k

    x = (a + b) / 2
    history = [(0, x, None)]
    for i in range(1, max_iter + 1):
        x_new = phi(x)
        diff = abs(x_new - x)
        history.append((i, x_new, diff))
        x = x_new
        if q == 0 or diff <= (1 - q) / q * eps:
            return x, history, {"k": k, "q": q}
    raise RuntimeError("Метод простой итерации не сошёлся")


def newton_start(f, a, b):
    # x0 выбираем там, где f(x0) * f''(x0) > 0
    for x in (a, b):
        if f(x) * second_derivative(f, x) > 0:
            return x
    return (a + b) / 2


def newton(f, a, b, eps, max_iter=1000):
    x = newton_start(f, a, b)
    history = [(0, x, None)]
    for i in range(1, max_iter + 1):
        d = derivative(f, x)
        if abs(d) < 1e-14:
            raise ZeroDivisionError("f'(x) = 0, метод Ньютона неприменим")
        x_new = x - f(x) / d
        diff = abs(x_new - x)
        history.append((i, x_new, diff))
        x = x_new
        if diff <= eps:
            return x, history
    raise RuntimeError("Метод Ньютона не сошёлся")
