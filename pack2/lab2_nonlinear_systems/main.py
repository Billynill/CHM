import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

from graph import save_plot, text_map
from io_utils import read_task
from linalg import vector_norm
from methods import newton, simple_iteration

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "input.txt"
OUTPUT_FILE = BASE_DIR / "output.txt"
GRAPH_FILE = BASE_DIR / "graph.png"

EPS_LIST = [1e-1, 1e-2, 1e-3, 1e-4, 1e-6, 1e-8, 1e-10]


def section(title):
    print(f"\n--- {title} ---")


def fmt_vector(x):
    return "(" + ", ".join(f"{v:.8f}" for v in x) + ")"


def print_history(history, x_ref):
    print(f"  {'k':>4}  {'x_k':<{14 * len(x_ref) + 2}}  {'||x_k - x_(k-1)||':>18}  {'||x_k - x*||':>13}")
    for k, x, diff in history:
        diff_str = f"{diff:>18.2e}" if diff is not None else f"{'-':>18}"
        err = vector_norm([x[i] - x_ref[i] for i in range(len(x))])
        print(f"  {k:>4}  {fmt_vector(x):<{14 * len(x_ref) + 2}}  {diff_str}  {err:>13.2e}")


def count_iterations(method, system, x0, eps):
    try:
        return len(method(system, x0, eps)[1]) - 1
    except (RuntimeError, ZeroDivisionError, ValueError, OverflowError):
        return "-"


def process(task):
    system, x0, eps = task["system"], task["x0"], task["eps"]
    n = len(x0)

    print("Система уравнений:")
    for i, text in enumerate(task["texts"], start=1):
        print(f"  f{i} = {text} = 0")
    if task["params"]:
        print("Параметры: " + ", ".join(f"{k} = {v:g}" for k, v in task["params"].items()))
    print(f"Начальное приближение x0 = {fmt_vector(x0)}")
    print(f"Точность eps = {eps}")

    if n == 2 and task["area"]:
        section("Графическое отделение решений")
        print("  '1' — кривая f1 = 0, '2' — кривая f2 = 0, 'X' — пересечение (решение)")
        print("  по вертикали x2, по горизонтали x1\n")
        print(text_map(system, task["area"]))

    try:
        x_ref, _ = newton(system, x0, 1e-13)
    except (RuntimeError, ZeroDivisionError) as e:
        print(f"\nОшибка: {e}. Выберите другое начальное приближение.")
        return

    section("Метод простой итерации")
    print("  phi(x) = x - L * F(x),  L = J(x0)^-1")
    try:
        x_si, hist_si, q = simple_iteration(system, x0, eps)
        print(f"  q = max||phi'(x)|| = {q:.6f}")
        print_history(hist_si, x_ref)
        print(f"\n  x = {fmt_vector(x_si)}, итераций: {len(hist_si) - 1}")
    except (RuntimeError, ZeroDivisionError, OverflowError) as e:
        print(f"  {e}")

    section("Метод Ньютона")
    print("  x(k+1) = x(k) - J(x(k))^-1 * F(x(k))")
    x_nt, hist_nt = newton(system, x0, eps)
    print_history(hist_nt, x_ref)
    print(f"\n  x = {fmt_vector(x_nt)}, итераций: {len(hist_nt) - 1}")

    section("Эталонное решение")
    print(f"  x* = {fmt_vector(x_ref)}")
    print(f"  F(x*) = {fmt_vector(system(x_ref))}")
    if all(v > 0 for v in x_ref):
        print("  Все компоненты решения положительные")

    section("Зависимость числа итераций от точности")
    print(f"  {'eps':>8}  {'Простая итерация':>17}  {'Ньютон':>8}")
    for e in EPS_LIST:
        print(f"  {e:>8.0e}  {count_iterations(simple_iteration, system, x0, e):>17}"
              f"  {count_iterations(newton, system, x0, e):>8}")

    if n == 2 and task["area"]:
        if save_plot(system, task["area"], x_ref, GRAPH_FILE):
            print(f"\n  График сохранён: {GRAPH_FILE.name}")
        else:
            print("\n  matplotlib не установлен, график не построен (pip3 install matplotlib)")


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
