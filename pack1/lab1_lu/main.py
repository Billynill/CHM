import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

from io_utils import read_system
from lu import SingularMatrixError, determinant, inverse, lu_decompose, solve
from matrix import format_matrix, format_vector, identity, matmul, matvec, max_abs_diff

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "input.txt"
OUTPUT_FILE = BASE_DIR / "output.txt"


def section(title):
    print(f"\n--- {title} ---")


def process(a, b):
    n = len(a)

    section(f"Матрица A ({n}x{n}) и вектор b")
    print(format_matrix(a))
    print(format_vector(b, name="b"))

    try:
        lu = lu_decompose(a)
    except SingularMatrixError as e:
        print(f"\nОшибка: {e}")
        return

    p = lu.permutation_matrix()

    section("Матрица L")
    print(format_matrix(lu.L))
    section("Матрица U")
    print(format_matrix(lu.U))
    section(f"Матрица перестановок P (перестановок: {lu.swaps})")
    print(format_matrix(p))

    lu_product = matmul(lu.L, lu.U)
    section("L * U")
    print(format_matrix(lu_product))

    x = solve(lu, b)
    section("Решение Ax = b")
    print(format_vector(x))
    residual = max(abs(r - bi) for r, bi in zip(matvec(a, x), b))
    print(f"  Невязка ||Ax - b|| = {residual:.3e}")

    a_inv = inverse(lu)
    section("Обратная матрица A^-1")
    print(format_matrix(a_inv))

    det = determinant(lu)
    section("Определитель")
    print(f"  det A = {det:.6f}")

    section("Проверка A * A^-1 = E")
    a_a_inv = matmul(a, a_inv)
    print(format_matrix(a_a_inv))
    print(f"  ||A * A^-1 - E|| = {max_abs_diff(a_a_inv, identity(n)):.3e}")

    section("Проверка L * U = P * A")
    pa = matmul(p, a)
    print(format_matrix(pa))
    print(f"  ||L * U - P * A|| = {max_abs_diff(lu_product, pa):.3e}")

    compare_with_numpy(a, b, x, a_inv, det)


def compare_with_numpy(a, b, x, a_inv, det):
    # numpy только для проверки
    try:
        import numpy as np
    except ImportError:
        return
    section("Сравнение с NumPy")
    print(f"  max|x - x_np|     = {np.max(np.abs(np.array(x) - np.linalg.solve(a, b))):.3e}")
    print(f"  max|A^-1 - np|    = {np.max(np.abs(np.array(a_inv) - np.linalg.inv(a))):.3e}")
    print(f"  |det - det_np|    = {abs(det - np.linalg.det(a)):.3e}")


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else INPUT_FILE

    try:
        a, b = read_system(input_path)
    except (OSError, ValueError) as e:
        print(f"Ошибка чтения {input_path}: {e}", file=sys.stderr)
        return 1

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print(f"Входной файл: {input_path.name}")
        process(a, b)

    result = buffer.getvalue()
    print(result)
    OUTPUT_FILE.write_text(result, encoding="utf-8")
    print(f"Результат сохранён в {OUTPUT_FILE.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
