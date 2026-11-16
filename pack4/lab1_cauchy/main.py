import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

from cauchy import METHODS, grid, make_system, runge_romberg
from io_utils import read_task
from plot import save_plot

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "input.txt"
OUTPUT_FILE = BASE_DIR / "output.txt"
GRAPH_FILE = BASE_DIR / "graph.png"


def section(title):
    print(f"\n--- {title} ---")


def process(task):
    a, b, h, exact = task["a"], task["b"], task["h"], task["exact"]
    print(f"y'' = {task['formula']}   (z = y')")
    print(f"y({a:g}) = {task['y0']:g}, y'({a:g}) = {task['z0']:g}, x на [{a:g}, {b:g}], h = {h:g}")
    if exact is not None:
        print(f"Точное решение: y = {task['exact_formula']}")
    print("\nСистема (4.21):  y' = z,  z' = f(x, y, z)")

    try:
        xs = grid(a, b, h)
    except ValueError as e:
        print(f"\nОшибка: {e}")
        return
    try:
        xs2 = grid(a, b, 2 * h)
    except ValueError:
        xs2 = None

    system = make_system(task["f"])
    v0 = [task["y0"], task["z0"]]

    plot_data, summary = [], []
    for name, method, p in METHODS:
        vs = method(system, xs, v0, h)
        ys = [v[0] for v in vs]
        plot_data.append((name, ys))

        section(f"{name} (порядок p = {p}), шаг h = {h:g}")
        header = f"  {'k':>3}  {'x_k':>6}  {'y_k':>12}  {'y`_k':>12}"
        if exact is not None:
            header += f"  {'y точн.':>12}  {'|y_k - y|':>11}"
        print(header)
        for k, (x, v) in enumerate(zip(xs, vs)):
            row = f"  {k:>3}  {x:>6.3f}  {v[0]:>12.7f}  {v[1]:>12.7f}"
            if exact is not None:
                row += f"  {exact(x):>12.7f}  {abs(v[0] - exact(x)):>11.3e}"
            print(row)

        if xs2 is None:
            print("\n  Рунге-Ромберг: (b - a) / (2h) не целое, сетку с шагом 2h построить нельзя")
            continue

        vs2 = method(system, xs2, v0, 2 * h)
        print(f"\n  Рунге-Ромберг (4.11): R = (y^h - y^2h) / (2^{p} - 1)")
        header = f"  {'x':>6}  {'y^h':>12}  {'y^2h':>12}  {'|R|':>11}  {'уточн. y':>12}"
        if exact is not None:
            header += f"  {'|y^h - y|':>11}"
        print(header)
        max_r = max_err = 0.0
        for j, x in enumerate(xs2):
            y_h, y_2h = vs[2 * j][0], vs2[j][0]
            r = runge_romberg(y_h, y_2h, p)
            max_r = max(max_r, abs(r))
            row = f"  {x:>6.3f}  {y_h:>12.7f}  {y_2h:>12.7f}  {abs(r):>11.3e}  {y_h + r:>12.7f}"
            if exact is not None:
                err = abs(y_h - exact(x))
                max_err = max(max_err, err)
                row += f"  {err:>11.3e}"
            print(row)
        summary.append((name, max_r, max_err if exact is not None else None))

    if summary:
        section("Итог: максимальная погрешность на отрезке")
        header = f"  {'Метод':<16}{'оценка Рунге':>14}"
        if exact is not None:
            header += f"{'по точному':>14}"
        print(header)
        for name, max_r, max_err in summary:
            row = f"  {name:<16}{max_r:>14.3e}"
            if max_err is not None:
                row += f"{max_err:>14.3e}"
            print(row)

    if save_plot(xs, plot_data, exact, GRAPH_FILE):
        print(f"\n  График сохранён: {GRAPH_FILE.name}")


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else INPUT_FILE

    try:
        task = read_task(input_path)
    except (OSError, ValueError) as e:
        print(f"Ошибка чтения {input_path}: {e}", file=sys.stderr)
        return 1

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print(f"Входной файл: {input_path.name}")
        process(task)

    result = buffer.getvalue()
    print(result)
    OUTPUT_FILE.write_text(result, encoding="utf-8")
    print(f"Результат сохранён в {OUTPUT_FILE.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
