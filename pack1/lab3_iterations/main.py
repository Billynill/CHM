import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

from gauss import gauss
from io_utils import read_system
from iterative import has_diagonal_dominance, norm, seidel, simple_iteration, to_iteration_form

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "input.txt"
OUTPUT_FILE = BASE_DIR / "output.txt"


def fmt(x, precision=6):
    if abs(x) < 0.5 * 10 ** (-precision):
        x = 0.0
    return f"{x:>12.{precision}f}"


def section(title):
    print(f"\n--- {title} ---")


def print_history(history):
    n = len(history[0][1])
    header = "  ".join(f"{'x' + str(i + 1):>12}" for i in range(n))
    print(f"  {'k':>4}  {header}  {'||x_k - x_(k-1)||':>18}")
    for k, x, diff in history:
        print(f"  {k:>4}  {'  '.join(fmt(v) for v in x)}  {diff:>18.6f}")


def print_vector(x):
    for i, v in enumerate(x):
        print(f"  x{i + 1} = {fmt(v).strip()}")


def max_error(x, x_ref):
    return max(abs(u - v) for u, v in zip(x, x_ref))


def process(a, b, eps):
    n = len(a)
    print(f"Точность eps = {eps}")
    print(f"Размерность n = {n}")

    alpha, beta = to_iteration_form(a, b)
    q = norm(alpha)

    section("Условия сходимости")
    print(f"  ||alpha|| = {q:.6f}")
    dominance = has_diagonal_dominance(a)
    print(f"  Диагональное преобладание: {'есть' if dominance else 'нет'}")
    if q < 1:
        print("  ||alpha|| < 1 — достаточное условие сходимости выполнено")
        print("  Остановка по оценке: ||alpha|| / (1 - ||alpha||) * ||x_k - x_(k-1)|| <= eps")
    else:
        print("  ||alpha|| >= 1 — достаточное условие по норме не выполнено")
        if dominance:
            print("  Но есть диагональное преобладание, поэтому оба метода сходятся")
        else:
            print("  Сходимость не гарантирована")
        print("  Остановка по условию: ||x_k - x_(k-1)|| <= eps")

    x_ref = gauss(a, b)

    results = {}
    for name, method in (("Метод простых итераций", simple_iteration), ("Метод Зейделя", seidel)):
        section(name)
        try:
            x, history = method(alpha, beta, eps)
        except RuntimeError as e:
            print(f"  {e}")
            continue
        print_history(history)
        print(f"\n  Решение за {len(history)} итераций:")
        print_vector(x)
        print(f"  Отклонение от эталона: {max_error(x, x_ref):.6f}")
        results[name] = len(history)

    section("Эталонное решение (метод Гаусса)")
    print_vector(x_ref)

    section("Сравнение методов")
    for name, iters in results.items():
        print(f"  {name:<24} {iters:>4} итераций")
    if len(results) == 2:
        simple_iters, seidel_iters = results.values()
        if seidel_iters < simple_iters:
            print(f"\n  Зейдель сошёлся быстрее в {simple_iters / seidel_iters:.2f} раза")
        elif seidel_iters > simple_iters:
            print(f"\n  Простые итерации сошлись быстрее в {seidel_iters / simple_iters:.2f} раза")
        else:
            print("\n  Методы сошлись за одинаковое число итераций")


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else INPUT_FILE

    try:
        a, b, eps = read_system(input_path)
    except (OSError, ValueError) as e:
        print(f"Ошибка чтения {input_path}: {e}", file=sys.stderr)
        return 1

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print(f"Входной файл: {input_path.name}")
        try:
            process(a, b, eps)
        except ValueError as e:
            print(f"\nОшибка: {e}")

    result = buffer.getvalue()
    print(result)
    OUTPUT_FILE.write_text(result, encoding="utf-8")
    print(f"Результат сохранён в {OUTPUT_FILE.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
