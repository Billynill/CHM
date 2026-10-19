import io
import math
import sys
from contextlib import redirect_stdout
from pathlib import Path

from io_utils import read_matrix
from jacobi import jacobi_rotation
from matrix import diag, fmt, format_matrix, identity, matmul, max_abs_diff, transpose

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "input.txt"
OUTPUT_FILE = BASE_DIR / "output.txt"


def section(title):
    print(f"\n--- {title} ---")


def process(a, eps):
    n = len(a)
    print(f"Точность eps = {eps}")

    section(f"Матрица A ({n}x{n})")
    print(format_matrix(a))

    eigenvalues, v, history = jacobi_rotation(a, eps)

    section("Итерации")
    print(f"  {'k':>4}  {'(i, j)':>8}  {'phi':>10}  {'t(A_k)':>12}")
    for k, i, j, phi, t in history:
        print(f"  {k:>4}  {f'({i + 1}, {j + 1})':>8}  {phi:>10.6f}  {t:>12.6f}")
    print(f"\n  Число итераций: {len(history)}")

    section("Собственные значения")
    for m, lam in enumerate(eigenvalues):
        print(f"  lambda{m + 1} = {fmt(lam)}")

    section("Собственные векторы")
    for m in range(n):
        h = [v[r][m] for r in range(n)]
        print(f"  h{m + 1} = ({', '.join(fmt(x) for x in h)})")

    section("Матрица собственных векторов V")
    print(format_matrix(v))

    lam = diag(eigenvalues)
    av = matmul(a, v)
    vl = matmul(v, lam)

    section("Проверка A * V = V * Lambda")
    print("  A * V =")
    print(format_matrix(av))
    print("  V * Lambda =")
    print(format_matrix(vl))
    print(f"  ||A * V - V * Lambda|| = {max_abs_diff(av, vl):.3e}")

    section("Проверка ортогональности V^T * V = E")
    print(f"  ||V^T * V - E|| = {max_abs_diff(matmul(transpose(v), v), identity(n)):.3e}")

    compare_with_numpy(a, eigenvalues)


def compare_with_numpy(a, eigenvalues):
    # numpy только для проверки
    try:
        import numpy as np
    except ImportError:
        return
    expected = sorted(np.linalg.eigvalsh(a))
    section("Сравнение с NumPy")
    print(f"  max|lambda - lambda_np| = {max(abs(x - y) for x, y in zip(sorted(eigenvalues), expected)):.3e}")


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else INPUT_FILE

    try:
        a, eps = read_matrix(input_path)
    except (OSError, ValueError) as e:
        print(f"Ошибка чтения {input_path}: {e}", file=sys.stderr)
        return 1

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print(f"Входной файл: {input_path.name}")
        try:
            process(a, eps)
        except (ValueError, RuntimeError) as e:
            print(f"\nОшибка: {e}")

    result = buffer.getvalue()
    print(result)
    OUTPUT_FILE.write_text(result, encoding="utf-8")
    print(f"Результат сохранён в {OUTPUT_FILE.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
