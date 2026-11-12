import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

from io_utils import read_task
from methods import localize_roots, newton, simple_iteration, tabulate
from plot import save_plots

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "input.txt"
OUTPUT_FILE = BASE_DIR / "output.txt"
GRAPH_FILE = BASE_DIR / "graph.png"
ERROR_FILE = BASE_DIR / "error.png"

EPS_LIST = [1e-1, 1e-2, 1e-3, 1e-4, 1e-6, 1e-8, 1e-10]


def section(title):
    print(f"\n--- {title} ---")


def print_table(points):
    print(f"  {'x':>10}  {'f(x)':>12}")
    prev = None
    for x, y in points:
        mark = ""
        if y is not None and prev is not None and prev * y < 0:
            mark = "  <- смена знака"
        value = f"{y:>12.6f}" if y is not None else f"{'не опр.':>12}"
        print(f"  {x:>10.4f}  {value}{mark}")
        prev = y


def print_history(history, x_ref):
    print(f"  {'k':>4}  {'x_k':>14}  {'|x_k - x_(k-1)|':>16}  {'|x_k - x*|':>12}")
    for k, x, diff in history:
        diff_str = f"{diff:>16.2e}" if diff is not None else f"{'-':>16}"
        print(f"  {k:>4}  {x:>14.10f}  {diff_str}  {abs(x - x_ref):>12.2e}")


def process(task):
    f, a, b, eps, step = task["f"], task["a"], task["b"], task["eps"], task["step"]
    print(f"Уравнение: {task['formula']} = 0")
    print(f"Отрезок поиска: [{a}, {b}], шаг табуляции {step}")
    print(f"Точность eps = {eps}")

    points = tabulate(f, a, b, step)
    section("Отделение корней (табуляция f(x))")
    print_table(points)

    segments = localize_roots(points)
    if not segments:
        print("\n  На отрезке нет смены знака, корни не найдены")
        return
    print(f"\n  Найдено корней: {len(segments)}")

    roots, convergence = [], []
    for num, (left, right) in enumerate(segments, start=1):
        print("\n" + "=" * 70)
        print(f"Корень {num}: отрезок [{left:.4f}, {right:.4f}]")
        print("=" * 70)

        if left == right:
            print(f"  x = {left} — точный корень (f = 0 в узле таблицы)")
            roots.append(left)
            continue

        # эталон: тот же Ньютон, но с машинной точностью
        x_ref, _ = newton(f, left, right, 1e-14)

        section("Метод простой итерации")
        try:
            x_si, hist_si, info = simple_iteration(f, left, right, eps)
            print(f"  phi(x) = x - f(x) / {info['k']:.6f},  q = max|phi'(x)| = {info['q']:.6f}")
            print_history(hist_si, x_ref)
            print(f"\n  x = {x_si:.10f}, итераций: {len(hist_si) - 1}")
        except (ValueError, RuntimeError) as e:
            print(f"  {e}")
            hist_si = None

        section("Метод Ньютона")
        try:
            x_nt, hist_nt = newton(f, left, right, eps)
            print(f"  Начальное приближение x0 = {hist_nt[0][1]} (условие f(x0) * f''(x0) > 0)")
            print_history(hist_nt, x_ref)
            print(f"\n  x = {x_nt:.10f}, итераций: {len(hist_nt) - 1}")
        except (ZeroDivisionError, RuntimeError) as e:
            print(f"  {e}")
            hist_nt = None

        section("Эталонное значение корня")
        print(f"  x* = {x_ref:.12f}")

        section("Зависимость числа итераций от точности")
        print(f"  {'eps':>8}  {'Простая итерация':>17}  {'Ньютон':>8}")
        for e in EPS_LIST:
            n_si = count_iterations(simple_iteration, f, left, right, e)
            n_nt = count_iterations(newton, f, left, right, e)
            print(f"  {e:>8.0e}  {n_si:>17}  {n_nt:>8}")

        roots.append(x_ref)
        if hist_si:
            convergence.append((f"Простая итерация, корень {num}", [(k, abs(x - x_ref)) for k, x, _ in hist_si]))
        if hist_nt:
            convergence.append((f"Ньютон, корень {num}", [(k, abs(x - x_ref)) for k, x, _ in hist_nt]))

    section("Итог")
    for num, r in enumerate(roots, start=1):
        print(f"  x{num} = {r:.6f}")

    if save_plots(f, points, roots, convergence, GRAPH_FILE, ERROR_FILE):
        print(f"\n  Графики сохранены: {GRAPH_FILE.name}, {ERROR_FILE.name}")
    else:
        print("\n  matplotlib не установлен, графики не построены (pip3 install matplotlib)")


def count_iterations(method, f, a, b, eps):
    try:
        result = method(f, a, b, eps)
    except (ValueError, RuntimeError, ZeroDivisionError):
        return "-"
    return len(result[1]) - 1


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
