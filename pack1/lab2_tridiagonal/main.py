import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

from io_utils import read_tridiagonal
from tridiagonal import check_diagonal_dominance, multiply, thomas

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "input.txt"
OUTPUT_FILE = BASE_DIR / "output.txt"


def fmt(x, width=12, precision=6):
    if abs(x) < 0.5 * 10 ** (-precision):
        x = 0.0
    return f"{x:>{width}.{precision}f}"


def section(title):
    print(f"\n--- {title} ---")


def process(a, b, c, d):
    n = len(b)

    section(f"Диагонали матрицы (n = {n})")
    print(f"  {'i':>3} {'a_i':>10} {'b_i':>10} {'c_i':>10} {'d_i':>10}")
    for i in range(n):
        print(f"  {i + 1:>3} {a[i]:>10.4f} {b[i]:>10.4f} {c[i]:>10.4f} {d[i]:>10.4f}")

    if check_diagonal_dominance(a, b, c):
        print("\n  Диагональное преобладание выполняется, метод устойчив")
    else:
        print("\n  Внимание: нет диагонального преобладания, устойчивость не гарантируется")

    try:
        p, q, x = thomas(a, b, c, d)
    except ZeroDivisionError as e:
        print(f"\nОшибка: {e}")
        return

    section("Прогоночные коэффициенты")
    print(f"  {'i':>3} {'P_i':>12} {'Q_i':>12}")
    for i in range(n):
        print(f"  {i + 1:>3} {fmt(p[i])} {fmt(q[i])}")

    section("Решение")
    for i in range(n):
        print(f"  x{i + 1} = {fmt(x[i], width=0)}")

    residual = max(abs(r - di) for r, di in zip(multiply(a, b, c, x), d))
    print(f"\n  Невязка ||Ax - d|| = {residual:.3e}")


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else INPUT_FILE

    try:
        a, b, c, d = read_tridiagonal(input_path)
    except (OSError, ValueError) as e:
        print(f"Ошибка чтения {input_path}: {e}", file=sys.stderr)
        return 1

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print(f"Входной файл: {input_path.name}")
        process(a, b, c, d)

    result = buffer.getvalue()
    print(result)
    OUTPUT_FILE.write_text(result, encoding="utf-8")
    print(f"Результат сохранён в {OUTPUT_FILE.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
