def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    if len(a[0]) != len(b):
        raise ValueError("Несовместимые размеры матриц")
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def diag(values):
    n = len(values)
    return [[values[i] if i == j else 0.0 for j in range(n)] for i in range(n)]


def max_abs_diff(a, b):
    return max(abs(x - y) for row_a, row_b in zip(a, b) for x, y in zip(row_a, row_b))


def fmt(x, precision=6):
    if abs(x) < 0.5 * 10 ** (-precision):
        x = 0.0
    return f"{x:.{precision}f}"


def format_matrix(a, precision=6):
    cells = [[fmt(x, precision) for x in row] for row in a]
    width = max(len(c) for row in cells for c in row)
    return "\n".join("  [ " + "  ".join(c.rjust(width) for c in row) + " ]" for row in cells)
