import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

from boundary import finite_difference, grid, runge_romberg, shooting
from io_utils import read_task
from plot import save_plot

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "input.txt"
OUTPUT_FILE = BASE_DIR / "output.txt"
GRAPH_FILE = BASE_DIR / "graph.png"


def section(title):
    print(f"\n--- {title} ---")


def print_solution(xs, ys, exact):
    header = f"  {'k':>3}  {'x_k':>6}  {'y_k':>12}"
    if exact is not None:
        header += f"  {'y точн.':>12}  {'|y_k - y|':>11}"
    print(header)
    for k, (x, y) in enumerate(zip(xs, ys)):
        row = f"  {k:>3}  {x:>6.3f}  {y:>12.7f}"
        if exact is not None:
            row += f"  {exact(x):>12.7f}  {abs(y - exact(x)):>11.3e}"
        print(row)


def print_runge(xs2, ys_h, ys_2h, p, exact):
    print(f"\n  Рунге-Ромберг: R = (y^h - y^2h) / (2^{p} - 1)")
    header = f"  {'x':>6}  {'y^h':>12}  {'y^2h':>12}  {'|R|':>11}"
    if exact is not None:
        header += f"  {'|y^h - y|':>11}"
    print(header)
    max_r = 0.0
    for j, x in enumerate(xs2):
        r = runge_romberg(ys_h[2 * j], ys_2h[j], p)
        max_r = max(max_r, abs(r))
        row = f"  {x:>6.3f}  {ys_h[2 * j]:>12.7f}  {ys_2h[j]:>12.7f}  {abs(r):>11.3e}"
        if exact is not None:
            row += f"  {abs(ys_h[2 * j] - exact(x)):>11.3e}"
        print(row)
    return max_r


def process(task):
    t = task["texts"]
    p, q, f, exact = task["p"], task["q"], task["f"], task["exact"]
    a, b, h = task["a"], task["b"], task["h"]
    alpha, beta, A = task["left"]
    delta, gamma, B = task["right"]

    print(f"y'' + ({t['p(x)']})*y' + ({t['q(x)']})*y = {t['f(x)']},  x на [{a:g}, {b:g}]")
    print(f"{alpha:g}*y({a:g}) + {beta:g}*y'({a:g}) = {A:.6g}")
    print(f"{delta:g}*y({b:g}) + {gamma:g}*y'({b:g}) = {B:.6g}")
    print(f"Шаг h = {h:g}")
    if exact is not None:
        print(f"Точное решение: y = {t['y_exact']}")

    try:
        xs = grid(a, b, h)
    except ValueError as e:
        print(f"\nОшибка: {e}")
        return
    try:
        xs2 = grid(a, b, 2 * h)
    except ValueError:
        xs2 = None

    def F(x, y, z):
        return f(x) - p(x) * z - q(x) * y

    summary, plot_data = [], []

    section("Метод стрельбы (задача Коши - Рунге-Кутта 4, eta - метод секущих)")
    eta0, eta1 = task["eta"]
    try:
        ys_s, zs_s, history = shooting(F, xs, h, task["left"], task["right"], eta0, eta1, task["eps"])
    except (ZeroDivisionError, RuntimeError) as e:
        print(f"  Ошибка: {e}")
        ys_s = None
    if ys_s is not None:
        print(f"  Точность eps = {task['eps']:g}")
        print(f"  {'j':>3}  {'eta_j':>14}  {'|Ф(eta_j)|':>14}")
        for j, (eta, value) in enumerate(history):
            print(f"  {j:>3}  {eta:>14.9f}  {abs(value):>14.3e}")
        print()
        print_solution(xs, ys_s, exact)
        plot_data.append(("Метод стрельбы", ys_s))
        if xs2 is not None:
            ys_s2, _, _ = shooting(F, xs2, 2 * h, task["left"], task["right"], eta0, eta1, task["eps"])
            summary.append(("Метод стрельбы", print_runge(xs2, ys_s, ys_s2, 4, exact), ys_s))

    section("Конечно-разностный метод")
    try:
        ys_fd, system = finite_difference(p, q, f, xs, h, task["left"], task["right"])
    except ZeroDivisionError as e:
        print(f"  Ошибка: {e}")
        ys_fd = None
    if ys_fd is not None:
        sub, diag, sup, rhs = system
        print("  Трёхдиагональная система (решается прогонкой):")
        for k in range(len(diag)):
            terms = []
            if k > 0:
                terms.append(f"{sub[k]:+.5f}*y{k - 1}")
            terms.append(f"{diag[k]:+.5f}*y{k}")
            if k < len(diag) - 1:
                terms.append(f"{sup[k]:+.5f}*y{k + 1}")
            print(f"    {' '.join(terms)} = {rhs[k]:.5f}")
        print()
        print_solution(xs, ys_fd, exact)
        plot_data.append(("Конечно-разностный метод", ys_fd))
        if xs2 is not None:
            ys_fd2, _ = finite_difference(p, q, f, xs2, 2 * h, task["left"], task["right"])
            summary.append(("Конечно-разностный", print_runge(xs2, ys_fd, ys_fd2, 1, exact), ys_fd))

    if summary:
        section("Итог: максимальная погрешность на отрезке")
        header = f"  {'Метод':<22}{'оценка Рунге':>14}"
        if exact is not None:
            header += f"{'по точному':>14}"
        print(header)
        for name, max_r, ys in summary:
            row = f"  {name:<22}{max_r:>14.3e}"
            if exact is not None:
                row += f"{max(abs(y - exact(x)) for x, y in zip(xs, ys)):>14.3e}"
            print(row)

    if plot_data and save_plot(xs, plot_data, exact, GRAPH_FILE):
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
