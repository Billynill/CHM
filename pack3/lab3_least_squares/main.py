import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

from io_utils import read_task
from least_squares import fit, poly_string, poly_value, sum_squared_errors
from plot import save_plot

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "input.txt"
OUTPUT_FILE = BASE_DIR / "output.txt"
GRAPH_FILE = BASE_DIR / "graph.png"


def section(title):
    print(f"\n--- {title} ---")


def print_normal_system(matrix, rhs):
    for k in range(len(matrix)):
        terms = " + ".join(f"{matrix[k][i]:.4f}*a{i}" for i in range(len(matrix)))
        print(f"  {terms} = {rhs[k]:.5f}")


def process(task):
    xs, ys = task["x"], task["y"]
    count = len(xs)

    section("Исходные данные")
    print(f"  {'j':>3}  {'x_j':>8}  {'y_j':>10}")
    for j in range(count):
        print(f"  {j:>3}  {xs[j]:>8.4f}  {ys[j]:>10.5f}")

    results, errors = [], []
    for degree in task["degrees"]:
        section(f"Многочлен степени {degree}")
        coefs, matrix, rhs = fit(xs, ys, degree)
        print("  Нормальная система (3.17):")
        print_normal_system(matrix, rhs)

        print("\n  Коэффициенты:")
        for i, a in enumerate(coefs):
            print(f"    a{i} = {a:.6f}")
        print(f"\n  P{degree}(x) = {poly_string(coefs)}")

        print(f"\n  {'j':>3}  {'x_j':>8}  {'y_j':>10}  {'P(x_j)':>10}  {'P(x_j) - y_j':>13}")
        for j, (x, y) in enumerate(zip(xs, ys)):
            p = poly_value(coefs, x)
            print(f"  {j:>3}  {x:>8.4f}  {y:>10.5f}  {p:>10.5f}  {p - y:>13.5f}")

        phi = sum_squared_errors(coefs, xs, ys)
        mse = phi / count
        print(f"\n  Сумма квадратов ошибок  Ф{degree} = {phi:.6f}")
        print(f"  Среднеквадратичная ошибка MSE{degree} = Ф{degree} / {count} = {mse:.6f}")

        results.append((degree, coefs))
        errors.append((degree, phi, mse))

    section("Сравнение")
    print(f"  {'степень':>8}  {'Ф':>12}  {'MSE':>12}")
    for degree, phi, mse in errors:
        print(f"  {degree:>8}  {phi:>12.6f}  {mse:>12.6f}")
    best = min(errors, key=lambda item: item[2])
    print(f"\n  Лучше всего приближает данные многочлен степени {best[0]} (MSE = {best[2]:.6f})")

    if save_plot(xs, ys, results, GRAPH_FILE):
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
