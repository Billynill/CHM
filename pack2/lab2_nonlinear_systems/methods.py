from linalg import gauss_solve, inverse, matmul, matrix_norm, matvec, vector_norm

H = 1e-6


def jacobian(system, x):
    n = len(x)
    jac = [[0.0] * n for _ in range(n)]
    for j in range(n):
        x_plus, x_minus = x[:], x[:]
        x_plus[j] += H
        x_minus[j] -= H
        f_plus, f_minus = system(x_plus), system(x_minus)
        for i in range(n):
            jac[i][j] = (f_plus[i] - f_minus[i]) / (2 * H)
    return jac


def newton(system, x0, eps, max_iter=100):
    x = list(x0)
    history = [(0, x[:], None)]
    for k in range(1, max_iter + 1):
        f = system(x)
        dx = gauss_solve(jacobian(system, x), [-v for v in f])
        x = [x[i] + dx[i] for i in range(len(x))]
        diff = vector_norm(dx)
        history.append((k, x[:], diff))
        if diff <= eps:
            return x, history
    raise RuntimeError("Метод Ньютона не сошёлся")


def simple_iteration(system, x0, eps, max_iter=10000):
    # phi(x) = x - L*F(x), L = J(x0)^-1
    n = len(x0)
    lam = inverse(jacobian(system, x0))

    def phi(x):
        step = matvec(lam, system(x))
        return [x[i] - step[i] for i in range(n)]

    def phi_derivative_norm(x):
        lj = matmul(lam, jacobian(system, x))
        return matrix_norm([[(1.0 if i == j else 0.0) - lj[i][j] for j in range(n)] for i in range(n)])

    x = list(x0)
    q = phi_derivative_norm(x)
    history = [(0, x[:], None)]
    for k in range(1, max_iter + 1):
        x_new = phi(x)
        diff = vector_norm([x_new[i] - x[i] for i in range(n)])
        x = x_new
        q = max(q, phi_derivative_norm(x))
        history.append((k, x[:], diff))

        factor = (1 - q) / q if 0 < q < 1 else 1.0
        if diff <= min(factor, 1.0) * eps:
            return x, history, q
        if diff > 1e10:
            break
    raise RuntimeError("Метод простой итерации не сошёлся (выберите x0 ближе к решению)")
