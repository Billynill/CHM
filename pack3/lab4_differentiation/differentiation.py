def choose_index(xs, x):
    # i такой, что x лежит на [x_i, x_(i+1)] и есть узел x_(i+2)
    if len(xs) < 3:
        raise ValueError("нужно хотя бы 3 узла")
    if x < xs[0] or x > xs[-1]:
        raise ValueError(f"точка {x} вне таблицы [{xs[0]}, {xs[-1]}]")
    i = 0
    for k in range(len(xs)):
        if xs[k] < x:
            i = k
    return min(i, len(xs) - 3)


def first_order(xs, ys, i):
    # (3.18)
    return (ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i])


def first_derivative(xs, ys, i, x):
    # (3.20)
    left = (ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i])
    right = (ys[i + 2] - ys[i + 1]) / (xs[i + 2] - xs[i + 1])
    return left + (right - left) / (xs[i + 2] - xs[i]) * (2 * x - xs[i] - xs[i + 1])


def second_derivative(xs, ys, i):
    # (3.21)
    left = (ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i])
    right = (ys[i + 2] - ys[i + 1]) / (xs[i + 2] - xs[i + 1])
    return 2 * (right - left) / (xs[i + 2] - xs[i])
