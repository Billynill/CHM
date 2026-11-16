import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

from io_utils import read_task
from plot import save_plot
from spline import build_spline, find_interval, spline_second_derivative, spline_value

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "input.txt"
OUTPUT_FILE = BASE_DIR / "output.txt"
GRAPH_FILE = BASE_DIR / "graph.png"


def section(title):
    print(f"\n--- {title} ---")


def poly_string(xs, coef, i):
    a, b, c, d = coef
    shift = xs[i - 1]
    t = "x" if shift == 0 else f"(x {'-' if shift > 0 else '+'} {abs(shift):g})"
    text = f"{a:.5f}"
    for value, power in ((b, ""), (c, "^2"), (d, "^3")):
        text += f" {'-' if value < 0 else '+'} {abs(value):.5f}{t}{power}"
    return text


def process(task):
    xs, fs, x_star = task["x"], task["f"], task["x_star"]
    n = len(xs) - 1

    section("Исходные узлы")
    print(f"  {'i':>3}  {'x_i':>8}  {'f_i':>10}")
    for i in range(len(xs)):
        print(f"  {i:>3}  {xs[i]:>8.4f}  {fs[i]:>10.5f}")

    coefs, system = build_spline(xs, fs)

    section("Система (3.13) относительно c_2 ... c_n")
    if not system["diag"]:
        print("  Один участок, система пустая: c_1 = 0")
    for k in range(len(system["diag"])):
        terms = []
        if system["sub"][k]:
            terms.append(f"{system['sub'][k]:g}*c{k + 1}")
        terms.append(f"{system['diag'][k]:g}*c{k + 2}")
        if system["sup"][k]:
            terms.append(f"{system['sup'][k]:g}*c{k + 3}")
        print(f"  {' + '.join(terms)} = {system['rhs'][k]:.5f}")

    section("Коэффициенты сплайна")
    print(f"  {'i':>3}  {'[x_(i-1), x_i]':>16}  {'a_i':>10}  {'b_i':>10}  {'c_i':>10}  {'d_i':>10}")
    for i in range(1, n + 1):
        a, b, c, d = coefs[i - 1]
        interval = f"[{xs[i - 1]:g}, {xs[i]:g}]"
        print(f"  {i:>3}  {interval:>16}  {a:>10.5f}  {b:>10.5f}  {c:>10.5f}  {d:>10.5f}")

    section("Многочлены на участках")
    for i in range(1, n + 1):
        print(f"  S{i}(x) = {poly_string(xs, coefs[i - 1], i)},   {xs[i - 1]:g} <= x <= {xs[i]:g}")

    try:
        k = find_interval(xs, x_star)
    except ValueError as e:
        print(f"\nОшибка: {e}")
        return
    s_star = spline_value(xs, coefs, x_star, k)

    section(f"Значение в точке x* = {x_star:g}")
    print(f"  x* принадлежит участку {k}: [{xs[k - 1]:g}, {xs[k]:g}]")
    print(f"  S(x*) = S{k}({x_star:g}) = {s_star:.5f}")

    section("Проверка прохождения через узлы")
    print(f"  {'i':>3}  {'x_i':>8}  {'f_i':>10}  {'S(x_i)':>10}  {'|S - f|':>10}")
    for i in range(len(xs)):
        piece = max(i, 1)
        s = spline_value(xs, coefs, xs[i], piece)
        print(f"  {i:>3}  {xs[i]:>8.4f}  {fs[i]:>10.5f}  {s:>10.5f}  {abs(s - fs[i]):>10.2e}")

    section("Граничные условия (нулевая кривизна)")
    print(f"  S''(x_0) = 2*c_1 = {spline_second_derivative(xs, coefs, xs[0], 1):.2e}")
    print(f"  S''(x_n) = 2*c_n + 6*d_n*h_n = {spline_second_derivative(xs, coefs, xs[-1], n):.2e}")

    if save_plot(xs, fs, coefs, x_star, s_star, GRAPH_FILE):
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
