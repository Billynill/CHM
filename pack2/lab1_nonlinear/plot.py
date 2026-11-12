def save_plots(f, points, roots, convergence, path_graph, path_error):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return False

    xs = [x for x, y in points if y is not None]
    ys = [y for x, y in points if y is not None]

    plt.figure(figsize=(8, 5))
    plt.plot(xs, ys, label="f(x)")
    plt.axhline(0, color="black", linewidth=0.8)
    for r in roots:
        plt.plot(r, f(r), "ro")
        plt.annotate(f"{r:.4f}", (r, 0), textcoords="offset points", xytext=(5, 10))
    plt.grid(True)
    plt.legend()
    plt.title("График f(x)")
    plt.savefig(path_graph, dpi=120)
    plt.close()

    plt.figure(figsize=(8, 5))
    for label, errors in convergence:
        ks = [k for k, err in errors if err > 0]
        es = [err for k, err in errors if err > 0]
        plt.semilogy(ks, es, "o-", label=label)
    plt.xlabel("Номер итерации k")
    plt.ylabel("|x_k - x*|")
    plt.grid(True, which="both")
    plt.legend()
    plt.title("Зависимость погрешности от числа итераций")
    plt.savefig(path_error, dpi=120)
    plt.close()
    return True
