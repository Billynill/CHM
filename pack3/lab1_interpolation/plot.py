def save_plot(f, xs, ys, lagrange_f, newton_f, x_star, path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return False

    left = min(min(xs), x_star)
    right = max(max(xs), x_star)
    margin = (right - left) * 0.05
    steps = 400
    grid = [left - margin + (right - left + 2 * margin) * i / steps for i in range(steps + 1)]

    fx, gx = [], []
    for x in grid:
        try:
            fx.append(f(x))
            gx.append(x)
        except (ValueError, ZeroDivisionError):
            pass

    plt.figure(figsize=(9, 6))
    plt.plot(gx, fx, color="black", linewidth=2, label="f(x)")
    plt.plot(grid, [lagrange_f(x) for x in grid], color="blue", label="Многочлен Лагранжа")
    plt.plot(grid, [newton_f(x) for x in grid], color="orange", linestyle="--", label="Многочлен Ньютона")
    plt.plot(xs, ys, "ko", label="Узлы интерполяции")
    plt.plot([x_star], [lagrange_f(x_star)], "r*", markersize=14, label=f"x* = {x_star:g}")
    plt.axvline(x_star, color="red", linestyle=":", linewidth=0.8)
    plt.grid(True)
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Интерполяция многочленами Лагранжа и Ньютона")
    plt.savefig(path, dpi=120)
    plt.close()
    return True
