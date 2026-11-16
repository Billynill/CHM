import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

from integration import METHODS, grid, runge_romberg
from io_utils import read_task

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "input.txt"
OUTPUT_FILE = BASE_DIR / "output.txt"


def section(title):
    print(f"\n--- {title} ---")


def fmt(value, width=12):
    return f"{value:>{width}.6f}" if value is not None else f"{'-':>{width}}"


def print_grid(y, xs, h):
    section(f"Узлы при шаге h = {h:g}")
    print(f"  {'i':>3}  {'x_i':>8}  {'y_i':>10}")
    for i, x in enumerate(xs):
        print(f"  {i:>3}  {x:>8.4f}  {y(x):>10.5f}")


def process(task):
    y, a, b, h1, h2 = task["y"], task["a"], task["b"], task["h1"], task["h2"]
    print(f"Интеграл от y = {task['formula']} на [{a:g}, {b:g}]")
    print(f"Шаги: h1 = {h1:g}, h2 = {h2:g}")

    try:
        grid1, grid2 = grid(a, b, h1), grid(a, b, h2)
    except ValueError as e:
        print(f"\nОшибка: {e}")
        return

    print_grid(y, grid1, h1)
    print_grid(y, grid2, h2)

    k = h1 / h2
    rows = []
    for name, method, p in METHODS:
        try:
            f1 = method(y, grid1, h1)
            f2 = method(y, grid2, h2)
            refined, estimate = runge_romberg(f2, f1, k, p)
        except ValueError as e:
            print(f"\n  {name}: {e}")
            continue
        rows.append((name, f1, f2, p, refined, estimate))

    section(f"Результаты (Рунге-Ромберг: k = h1/h2 = {k:g})")
    print(f"  {'Метод':<24}{'F(h1)':>12}{'F(h2)':>12}{'p':>4}{'F уточн.':>12}{'оценка погр.':>14}")
    for name, f1, f2, p, refined, estimate in rows:
        print(f"  {name:<24}{fmt(f1)}{fmt(f2)}{p:>4}{fmt(refined)}{estimate:>14.2e}")
    print("\n  F уточн. = F(h2) + (F(h2) - F(h1)) / (k^p - 1)")
    print("  оценка погрешности F(h2) = |F(h2) - F(h1)| / (k^p - 1)")

    if task["F"] is None:
        print("\n  Первообразная не задана, точное значение не вычисляется")
        return

    exact = task["F"](b) - task["F"](a)
    section("Сравнение с точным значением")
    print(f"  F(x) = {task['F_formula']}")
    print(f"  Точное значение: F(xk) - F(x0) = {exact:.6f}\n")
    print(f"  {'Метод':<24}{'|F(h1) - F|':>14}{'|F(h2) - F|':>14}{'|F уточн. - F|':>16}")
    for name, f1, f2, p, refined, estimate in rows:
        print(f"  {name:<24}{abs(f1 - exact):>14.2e}{abs(f2 - exact):>14.2e}{abs(refined - exact):>16.2e}")

    best_h2 = min(rows, key=lambda row: abs(row[2] - exact))
    best_refined = min(rows, key=lambda row: abs(row[4] - exact))
    print(f"\n  Точнее всех с шагом h2: {best_h2[0]} (погрешность {abs(best_h2[2] - exact):.2e})")
    print(f"  Точнее всех после уточнения: {best_refined[0]} (погрешность {abs(best_refined[4] - exact):.2e})")


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
