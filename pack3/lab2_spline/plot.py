from spline import spline_value


def save_plot(xs, fs, coefs, x_star, s_star, path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return False

    plt.figure(figsize=(9, 6))
    for i in range(1, len(xs)):
        steps = 100
        grid = [xs[i - 1] + (xs[i] - xs[i - 1]) * k / steps for k in range(steps + 1)]
        plt.plot(grid, [spline_value(xs, coefs, x, i) for x in grid], linewidth=2,
                 label=f"S{i}(x) на [{xs[i - 1]:g}, {xs[i]:g}]")
    plt.plot(xs, fs, "ko", label="Узлы")
    plt.plot([x_star], [s_star], "r*", markersize=14, label=f"(x*, S(x*)) = ({x_star:g}, {s_star:.4f})")
    plt.grid(True)
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("S(x)")
    plt.title("Кубический сплайн")
    plt.savefig(path, dpi=120)
    plt.close()
    return True
