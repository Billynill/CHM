from least_squares import poly_value

STYLES = ["-", "--", "-.", ":"]


def save_plot(xs, ys, results, path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return False

    left, right = min(xs), max(xs)
    margin = (right - left) * 0.05
    steps = 300
    grid = [left - margin + (right - left + 2 * margin) * i / steps for i in range(steps + 1)]

    plt.figure(figsize=(9, 6))
    plt.plot(xs, ys, "ko", markersize=7, label="Исходные данные")
    for k, (degree, coefs) in enumerate(results):
        plt.plot(grid, [poly_value(coefs, x) for x in grid], STYLES[k % len(STYLES)], linewidth=2,
                 label=f"P{degree}(x), степень {degree}")
    plt.grid(True)
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Метод наименьших квадратов")
    plt.savefig(path, dpi=120)
    plt.close()
    return True
