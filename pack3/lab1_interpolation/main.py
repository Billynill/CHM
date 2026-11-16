import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

from interpolation import (divided_differences, lagrange, lagrange_string, newton, newton_string,
                           omega_derivative)
from io_utils import read_task
from plot import save_plot

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "input.txt"
OUTPUT_FILE = BASE_DIR / "output.txt"


def section(title):
    print(f"\n--- {title} ---")


def process_set(f, xs, ys, x_star, graph_path):
    n = len(xs) - 1
    print(f"Степень многочленов: n = {n}")

    section("Узлы интерполяции")
    print(f"  {'i':>3}  {'x_i':>10}  {'y_i':>12}")
    for i in range(len(xs)):
        print(f"  {i:>3}  {xs[i]:>10.5f}  {ys[i]:>12.5f}")

    section("Многочлен Лагранжа")
    print(f"  {'i':>3}  {'x_i':>8}  {'f_i':>10}  {'w`(x_i)':>10}  {'f_i/w`(x_i)':>12}  {'x* - x_i':>9}")
    for i in range(len(xs)):
        w = omega_derivative(xs, i)
        print(f"  {i:>3}  {xs[i]:>8.4f}  {ys[i]:>10.5f}  {w:>10.5f}  {ys[i] / w:>12.5f}  {x_star - xs[i]:>9.4f}")
    print(f"\n  L{n}(x) = {lagrange_string(xs, ys)}")

    table = divided_differences(xs, ys)
    section("Таблица разделённых разностей")
    header = f"  {'i':>3}  {'x_i':>8}  {'f(x_i)':>11}"
    for k in range(1, len(xs)):
        header += f"  {'порядок ' + str(k):>11}"
    print(header)
    for i in range(len(xs)):
        row = f"  {i:>3}  {xs[i]:>8.4f}"
        for k in range(len(xs)):
            row += f"  {table[k][i]:>11.5f}" if i < len(table[k]) else f"  {'':>11}"
        print(row)

    section("Многочлен Ньютона")
    print(f"  P{n}(x) = {newton_string(xs, table)}")

    l_value = lagrange(xs, ys, x_star)
    n_value = newton(xs, table, x_star)
    exact = f(x_star)

    section(f"Значения в точке x* = {x_star:.6f}")
    print(f"  L{n}(x*)  = {l_value:.6f}")
    print(f"  P{n}(x*)  = {n_value:.6f}")
    print(f"  f(x*)    = {exact:.6f}")
    print(f"\n  Абсолютная погрешность интерполяции |f(x*) - L{n}(x*)| = {abs(exact - l_value):.6f}")
    print(f"  Разность методов |L{n}(x*) - P{n}(x*)| = {abs(l_value - n_value):.3e}")

    if save_plot(f, xs, ys, lambda x: lagrange(xs, ys, x), lambda x: newton(xs, table, x), x_star, graph_path):
        print(f"\n  График сохранён: {graph_path.name}")
    else:
        print("\n  matplotlib не установлен, график не построен (pip3 install matplotlib)")

    return abs(exact - l_value)


def process(task):
    print(f"Функция: f(x) = {task['formula']}")
    print(f"Точка x* = {task['x_star']:.6f}")

    errors = []
    for node_set in task["sets"]:
        name = node_set["name"]
        suffix = f"_{name}" if name else ""
        print("\n" + "=" * 70)
        print(f"Набор узлов {name}" if name else "Узлы интерполяции")
        print("=" * 70)
        error = process_set(task["f"], node_set["x"], node_set["y"], task["x_star"],
                            BASE_DIR / f"graph{suffix}.png")
        errors.append((name, error))

    if len(errors) > 1:
        section("Сравнение наборов узлов")
        for name, error in errors:
            print(f"  набор {name}: погрешность в x* = {error:.6f}")
        best = min(errors, key=lambda item: item[1])
        print(f"\n  Точнее приближает набор {best[0]}")


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
