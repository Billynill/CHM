def omega_derivative(xs, i):
    # w'(x_i) = (x_i - x_0)...(x_i - x_(i-1))(x_i - x_(i+1))...(x_i - x_n)
    result = 1.0
    for j in range(len(xs)):
        if j != i:
            result *= xs[i] - xs[j]
    return result


def lagrange(xs, ys, x):
    total = 0.0
    for i in range(len(xs)):
        term = ys[i] / omega_derivative(xs, i)
        for j in range(len(xs)):
            if j != i:
                term *= x - xs[j]
        total += term
    return total


def divided_differences(xs, ys):
    # table[k][i] = f(x_i, ..., x_(i+k))
    n = len(xs)
    table = [list(ys)]
    for k in range(1, n):
        prev = table[k - 1]
        table.append([(prev[i] - prev[i + 1]) / (xs[i] - xs[i + k]) for i in range(n - k)])
    return table


def newton(xs, table, x):
    total = 0.0
    product = 1.0
    for k in range(len(xs)):
        total += table[k][0] * product
        product *= x - xs[k]
    return total


def factor(x0):
    if x0 == 0:
        return "x"
    sign = "-" if x0 > 0 else "+"
    return f"(x {sign} {abs(x0):g})"


def join_terms(terms):
    text = ""
    for coef, body in terms:
        sign = "-" if coef < 0 else "+"
        part = f"{abs(coef):.5f}{body}"
        if not text:
            text = f"-{part}" if coef < 0 else part
        else:
            text += f" {sign} {part}"
    return text


def lagrange_string(xs, ys):
    terms = []
    for i in range(len(xs)):
        coef = ys[i] / omega_derivative(xs, i)
        body = "".join(factor(xs[j]) for j in range(len(xs)) if j != i)
        terms.append((coef, body))
    return join_terms(terms)


def newton_string(xs, table):
    terms = []
    for k in range(len(xs)):
        body = "".join(factor(xs[j]) for j in range(k))
        terms.append((table[k][0], body))
    return join_terms(terms)
