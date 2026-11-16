import re

from expression import make_system


def read_task(path):
    equations = {}
    params = {}
    x0 = eps = area = None

    with open(path, encoding="utf-8") as f:
        for line_no, raw in enumerate(f, start=1):
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            if "=" not in line:
                raise ValueError(f"строка {line_no}: ожидается запись вида имя = значение")
            key, value = (s.strip() for s in line.split("=", 1))
            key = key.lower()

            try:
                if re.fullmatch(r"f\d+", key):
                    equations[int(key[1:])] = value
                elif key == "x0":
                    x0 = [float(v) for v in value.split()]
                elif key == "eps":
                    eps = float(value)
                elif key == "area":
                    area = [float(v) for v in value.split()]
                else:
                    params[key] = float(value)
            except ValueError:
                raise ValueError(f"строка {line_no}: не удалось прочитать числа: {raw.strip()!r}")

    if not equations:
        raise ValueError("нет уравнений (строки f1 = ..., f2 = ...)")
    n = len(equations)
    if sorted(equations) != list(range(1, n + 1)):
        raise ValueError("уравнения должны быть пронумерованы f1, f2, ..., fn без пропусков")
    if x0 is None or len(x0) != n:
        raise ValueError(f"x0 должно содержать {n} чисел (начальное приближение)")
    if eps is None or eps <= 0:
        raise ValueError("не задана точность eps")
    if area is not None and len(area) != 4:
        raise ValueError("area задаётся четырьмя числами: x1_min x1_max x2_min x2_max")

    texts = [equations[i] for i in range(1, n + 1)]
    try:
        system = make_system(texts, params)
        system(x0)
    except Exception as e:
        raise ValueError(f"не удалось вычислить систему в x0: {e}")

    return {"system": system, "texts": texts, "params": params, "x0": x0, "eps": eps, "area": area}
