def grid(a, b, h):
    n = round((b - a) / h)
    if n < 2 or abs(n * h - (b - a)) > 1e-9:
        raise ValueError(f"шаг h = {h} не укладывается целое число раз в [{a}, {b}]")
    return [a + k * h for k in range(n + 1)]


def rk4(F, xs, y0, z0, h):
    # (4.16) для системы y' = z, z' = F(x, y, z)
    ys, zs = [y0], [z0]
    for k in range(len(xs) - 1):
        x, y, z = xs[k], ys[-1], zs[-1]
        k1, l1 = h * z, h * F(x, y, z)
        k2, l2 = h * (z + l1 / 2), h * F(x + h / 2, y + k1 / 2, z + l1 / 2)
        k3, l3 = h * (z + l2 / 2), h * F(x + h / 2, y + k2 / 2, z + l2 / 2)
        k4, l4 = h * (z + l3), h * F(x + h, y + k3, z + l3)
        ys.append(y + (k1 + 2 * k2 + 2 * k3 + k4) / 6)
        zs.append(z + (l1 + 2 * l2 + 2 * l3 + l4) / 6)
    return ys, zs


def shooting(F, xs, h, left, right, eta0, eta1, eps, max_iter=100):
    alpha, beta, A = left
    delta, gamma, B = right

    def start(eta):
        # из левого условия alpha*y(a) + beta*y'(a) = A одно значение известно, второе = eta
        if beta == 0:
            return A / alpha, eta
        return eta, (A - alpha * eta) / beta

    def phi(eta):
        # (4.33): невязка правого граничного условия
        ys, zs = rk4(F, xs, *start(eta), h)
        return delta * ys[-1] + gamma * zs[-1] - B

    history = [(eta0, phi(eta0)), (eta1, phi(eta1))]
    for _ in range(max_iter):
        (e_prev, f_prev), (e_cur, f_cur) = history[-2], history[-1]
        if abs(f_cur) < eps:
            break
        if f_cur == f_prev:
            raise ZeroDivisionError("Ф(eta_j+1) = Ф(eta_j), метод секущих неприменим")
        # (4.34)
        e_new = e_cur - (e_cur - e_prev) / (f_cur - f_prev) * f_cur
        history.append((e_new, phi(e_new)))
    else:
        raise RuntimeError("Метод стрельбы не сошёлся")

    ys, zs = rk4(F, xs, *start(history[-1][0]), h)
    return ys, zs, history


def thomas(a, b, c, d):
    n = len(b)
    p = [0.0] * n
    q = [0.0] * n
    for i in range(n):
        denom = b[i] + (a[i] * p[i - 1] if i > 0 else 0.0)
        if abs(denom) < 1e-14:
            raise ZeroDivisionError(f"Нулевой знаменатель в прогонке на шаге {i + 1}")
        p[i] = -c[i] / denom
        q[i] = (d[i] - (a[i] * q[i - 1] if i > 0 else 0.0)) / denom
    x = [0.0] * n
    x[-1] = q[-1]
    for i in range(n - 2, -1, -1):
        x[i] = p[i] * x[i + 1] + q[i]
    return x


def finite_difference(p, q, f, xs, h, left, right):
    alpha, beta, A = left
    delta, gamma, B = right
    n = len(xs) - 1
    sub, diag, sup, rhs = [], [], [], []

    # левая граница: alpha*y0 + beta*(y1 - y0)/h = A   (4.40)
    sub.append(0.0)
    diag.append(alpha - beta / h)
    sup.append(beta / h)
    rhs.append(A)

    # внутренние узлы (4.38)
    for k in range(1, n):
        x = xs[k]
        sub.append(1 - p(x) * h / 2)
        diag.append(-2 + h * h * q(x))
        sup.append(1 + p(x) * h / 2)
        rhs.append(h * h * f(x))

    # правая граница: delta*yN + gamma*(yN - y(N-1))/h = B   (4.40)
    sub.append(-gamma / h)
    diag.append(delta + gamma / h)
    sup.append(0.0)
    rhs.append(B)

    ys = thomas(sub, diag, sup, rhs)
    return ys, (sub, diag, sup, rhs)


def runge_romberg(y_h, y_2h, p):
    return (y_h - y_2h) / (2 ** p - 1)
