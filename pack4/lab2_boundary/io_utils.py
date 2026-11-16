from expression import parse_function, parse_number


def read_keys(path):
    values = {}
    with open(path, encoding="utf-8") as f:
        for line_no, raw in enumerate(f, start=1):
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            if "=" not in line:
                raise ValueError(f"строка {line_no}: ожидается запись вида имя = значение")
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    return values


def numbers(text, count, key):
    try:
        values = [parse_number(v) for v in text.split()]
    except (SyntaxError, ValueError, ZeroDivisionError) as e:
        raise ValueError(f"{key}: не удалось прочитать числа: {e}")
    if len(values) != count:
        raise ValueError(f"{key}: нужно {count} числа, получено {len(values)}")
    return values


def read_task(path):
    values = read_keys(path)
    for key in ("p(x)", "q(x)", "f(x)", "a", "b", "left", "right", "h"):
        if key not in values:
            raise ValueError(f"в файле не хватает строки {key} = ...")

    try:
        p, q, f = (parse_function(values[k]) for k in ("p(x)", "q(x)", "f(x)"))
        exact = parse_function(values["y_exact"]) if "y_exact" in values else None
    except (SyntaxError, ValueError) as e:
        raise ValueError(f"не удалось разобрать формулу: {e}")

    a, = numbers(values["a"], 1, "a")
    b, = numbers(values["b"], 1, "b")
    h, = numbers(values["h"], 1, "h")
    left = numbers(values["left"], 3, "left")
    right = numbers(values["right"], 3, "right")
    eta0, eta1 = numbers(values.get("eta", "1 0.8"), 2, "eta")
    eps, = numbers(values.get("eps", "1e-6"), 1, "eps")

    if a >= b:
        raise ValueError("должно быть a < b")
    if h <= 0 or eps <= 0:
        raise ValueError("h и eps должны быть положительными")
    if left[0] == 0 and left[1] == 0 or right[0] == 0 and right[1] == 0:
        raise ValueError("в граничном условии коэффициенты при y и y' не могут быть оба нулевыми")

    return {"p": p, "q": q, "f": f, "exact": exact, "texts": values, "a": a, "b": b, "h": h,
            "left": left, "right": right, "eta": (eta0, eta1), "eps": eps}
