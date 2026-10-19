def gauss(a, b):
    # метод Гаусса с выбором главного элемента, нужен для эталонного решения
    n = len(a)
    m = [a[i][:] + [b[i]] for i in range(n)]

    for k in range(n):
        pivot = max(range(k, n), key=lambda i: abs(m[i][k]))
        if abs(m[pivot][k]) < 1e-12:
            raise ValueError("Матрица вырождена")
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
