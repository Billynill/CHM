EPS_ZERO = 1e-12


def to_iteration_form(a, b):
    # A*x = b  ->  x = alpha*x + beta
    n = len(a)
    alpha = [[0.0] * n for _ in range(n)]
    beta = [0.0] * n
    for i in range(n):
        if abs(a[i][i]) < EPS_ZERO:
            raise ValueError(f"a[{i + 1}][{i + 1}] = 0, привести систему к виду x = alpha*x + beta нельзя")
        for j in range(n):
            if i != j:
                alpha[i][j] = -a[i][j] / a[i][i]
        beta[i] = b[i] / a[i][i]
    return alpha, beta


def norm(m):
    # норма-максимум по строкам
    return max(sum(abs(x) for x in row) for row in m)


def vector_norm(v):
    return max(abs(x) for x in v)


def upper_part(alpha):
    n = len(alpha)
    return [[alpha[i][j] if j > i else 0.0 for j in range(n)] for i in range(n)]


def has_diagonal_dominance(a):
    strict = False
    for i in range(len(a)):
        side = sum(abs(a[i][j]) for j in range(len(a)) if j != i)
        if abs(a[i][i]) < side:
            return False
        if abs(a[i][i]) > side:
            strict = True
    return strict


def stop_coefficient(alpha, seidel):
    # апостериорная оценка: ||x* - x_k|| <= coef * ||x_k - x_(k-1)||
    q = norm(alpha)
    if q >= 1:
        return 1.0
    if seidel:
        return norm(upper_part(alpha)) / (1 - q)
    return q / (1 - q)


def simple_iteration(alpha, beta, eps, max_iter=10000):
    n = len(beta)
    coef = stop_coefficient(alpha, seidel=False)
    x = beta[:]
    history = []

    for k in range(1, max_iter + 1):
        x_new = [beta[i] + sum(alpha[i][j] * x[j] for j in range(n)) for i in range(n)]
        diff = vector_norm([x_new[i] - x[i] for i in range(n)])
        history.append((k, x_new, diff))
        x = x_new
        if coef * diff <= eps:
            return x, history

    raise RuntimeError(f"Метод простых итераций не сошёлся за {max_iter} итераций")


def seidel(alpha, beta, eps, max_iter=10000):
    n = len(beta)
    coef = stop_coefficient(alpha, seidel=True)
    x = beta[:]
    history = []

    for k in range(1, max_iter + 1):
        x_old = x[:]
        for i in range(n):
            # x уже содержит новые значения x_0..x_(i-1)
            x[i] = beta[i] + sum(alpha[i][j] * x[j] for j in range(n))
        diff = vector_norm([x[i] - x_old[i] for i in range(n)])
        history.append((k, x[:], diff))
        if coef * diff <= eps:
            return x, history

    raise RuntimeError(f"Метод Зейделя не сошёлся за {max_iter} итераций")
