def safe_values(system, x, y):
    try:
        return system([x, y])
    except (ValueError, ZeroDivisionError, OverflowError):
        return None


def text_map(system, area, cols=60, rows=24):
    # отмечаем клетки, через которые проходит кривая f1 = 0 ('1'), f2 = 0 ('2') или обе ('X')
    x_min, x_max, y_min, y_max = area
    dx = (x_max - x_min) / cols
    dy = (y_max - y_min) / rows

    grid = [[safe_values(system, x_min + c * dx, y_max - r * dy) for c in range(cols + 1)] for r in range(rows + 1)]

    lines = []
    for r in range(rows):
        y = y_max - (r + 0.5) * dy
        row = []
        for c in range(cols):
            corners = [grid[r][c], grid[r][c + 1], grid[r + 1][c], grid[r + 1][c + 1]]
            crosses = []
            for eq in range(2):
                if any(v is None for v in corners):
                    crosses.append(False)
                    continue
                values = [v[eq] for v in corners]
                crosses.append(min(values) <= 0 <= max(values))
            if all(crosses):
                row.append("X")
            elif crosses[0]:
                row.append("1")
            elif crosses[1]:
                row.append("2")
            else:
                row.append(".")
        lines.append(f"  {y:>7.2f} |{''.join(row)}")
    lines.append(f"  {'':>7}  {x_min:<{cols // 2}.2f}{x_max:>{cols // 2}.2f}")
    return "\n".join(lines)


def save_plot(system, area, solution, path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return False

    x_min, x_max, y_min, y_max = area
    steps = 300
    xs = [x_min + (x_max - x_min) * i / steps for i in range(steps + 1)]
    ys = [y_min + (y_max - y_min) * i / steps for i in range(steps + 1)]
    z1, z2 = [], []
    for y in ys:
        row1, row2 = [], []
        for x in xs:
            v = safe_values(system, x, y)
            row1.append(v[0] if v else float("nan"))
            row2.append(v[1] if v else float("nan"))
        z1.append(row1)
        z2.append(row2)

    plt.figure(figsize=(7, 6))
    plt.contour(xs, ys, z1, levels=[0], colors="blue")
    plt.contour(xs, ys, z2, levels=[0], colors="red")
    plt.plot(solution[0], solution[1], "ko")
    plt.annotate(f"({solution[0]:.4f}, {solution[1]:.4f})", solution, textcoords="offset points", xytext=(5, 8))
    plt.plot([], [], color="blue", label="f1 = 0")
    plt.plot([], [], color="red", label="f2 = 0")
    plt.axhline(0, color="black", linewidth=0.6)
    plt.axvline(0, color="black", linewidth=0.6)
    plt.grid(True)
    plt.legend()
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.savefig(path, dpi=120)
    plt.close()
    return True
