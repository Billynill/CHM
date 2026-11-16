import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

from differentiation import choose_index, first_derivative, first_order, second_derivative
from io_utils import read_task

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "input.txt"
OUTPUT_FILE = BASE_DIR / "output.txt"


def section(title):
    print(f"\n--- {title} ---")


def process(task):
    xs, ys, x_star = task["x"], task["y"], task["x_star"]

    section("Исходная таблица")
    print(f"  {'i':>3}  {'x_i':>8}  {'y_i':>10}")
    for i in range(len(xs)):
        print(f"  {i:>3}  {xs[i]:>8.4f}  {ys[i]:>10.5f}")

    print(f"\nТочка вычисления: x* = {x_star:g}")

    try:
        i = choose_index(xs, x_star)
    except ValueError as e:
        print(f"\nОшибка: {e}")
        return

    section("Использованные узлы")
    for k in (i, i + 1, i + 2):
        print(f"  x{k} = {xs[k]:g},  y{k} = {ys[k]:.5f}")
    print(f"  x* лежит на отрезке [x{i}, x{i + 1}] = [{xs[i]:g}, {xs[i + 1]:g}]")

    section("Первая производная, первый порядок точности (3.18)")
    print(f"  на отрезке [x{i}, x{i + 1}]:  y' = (y{i + 1} - y{i}) / (x{i + 1} - x{i}) = {first_order(xs, ys, i):.5f}")
    print(f"  на отрезке [x{i + 1}, x{i + 2}]:  y' = (y{i + 2} - y{i + 1}) / (x{i + 2} - x{i + 1})"
          f" = {first_order(xs, ys, i + 1):.5f}")

    d1 = first_derivative(xs, ys, i, x_star)
    d2 = second_derivative(xs, ys, i)

    section("Результат")
    print(f"  Первая производная, второй порядок (3.20):  y'({x_star:g}) = {d1:.5f}")
    print(f"  Вторая производная (3.21):                 y''({x_star:g}) = {d2:.5f}")


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
