def save_plot(xs, results, exact, path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return False

    plt.figure(figsize=(9, 6))
    if exact is not None:
        steps = 300
        fine = [xs[0] + (xs[-1] - xs[0]) * i / steps for i in range(steps + 1)]
        plt.plot(fine, [exact(x) for x in fine], color="black", linewidth=2, label="Точное решение")
    for (name, ys), style in zip(results, ("o--", "s-.")):
        plt.plot(xs, ys, style, markersize=4, label=name)
    plt.grid(True)
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Решение краевой задачи")
    plt.savefig(path, dpi=120)
    plt.close()
    return True
