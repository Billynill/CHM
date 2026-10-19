import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

from io_utils import read_matrix
from matrix import fmt_complex, format_matrix, matmul, max_abs_diff
from qr import qr_algorithm, qr_decompose

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "input.txt"
OUTPUT_FILE = BASE_DIR / "output.txt"


def section(title):
    print(f"\n--- {title} ---")


def process(a, eps):
    n = len(a)
    print(f"Точность eps = {eps}")

    section(f"Исходная матрица A ({n}x{n})")
    print(format_matrix(a))

    q, r = qr_decompose(a)
    section("Матрица Q")
    print(format_matrix(q))
    section("Матрица R")
    print(format_matrix(r))

    qr_product = matmul(q, r)
    section("Q * R")
    print(format_matrix(qr_product))
    print(f"  ||Q * R - A|| = {max_abs_diff(qr_product, a):.3e}")

    eigenvalues, a_k, iterations = qr_algorithm(a, eps)

    section(f"Матрица A_k после {iterations} итераций QR-алгоритма")
    print(format_matrix(a_k))

    section("Собственные значения")
    for i, lam in enumerate(eigenvalues):
        print(f"  lambda{i + 1} = {fmt_complex(lam)}")

    compare_with_numpy(a, eigenvalues)


def compare_with_numpy(a, eigenvalues):
    # numpy только для проверки
    try:
        import numpy as np
    except ImportError:
        return
    expected = list(np.linalg.eigvals(a))
    worst = 0.0
    for lam in eigenvalues:
        closest = min(expected, key=lambda z: abs(z - lam))
        expected.remove(closest)
        worst = max(worst, abs(closest - lam))
    section("Сравнение с NumPy")
    print(f"  max|lambda - lambda_np| = {worst:.3e}")


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
