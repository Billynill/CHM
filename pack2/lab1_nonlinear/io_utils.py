from expression import parse_function

REQUIRED = ("f", "a", "b", "eps")


def read_task(path):
    values = {}
    with open(path, encoding="utf-8") as f:
        for line_no, raw in enumerate(f, start=1):
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            if "=" not in line:
                raise ValueError(f"строка {line_no}: ожидается запись вида имя = значение")
            key, value = line.split("=", 1)
            key = key.strip().lower()
            if key.startswith("f("):
                key = "f"
            values[key] = value.strip()

    missing = [k for k in REQUIRED if k not in values]
    if missing:
        raise ValueError(f"в файле не хватает: {', '.join(missing)}")

    try:
        func = parse_function(values["f"])
    except Exception as e:
        raise ValueError(f"не удалось разобрать f(x): {e}")

    try:
        a, b, eps = float(values["a"]), float(values["b"]), float(values["eps"])
        step = float(values["step"]) if "step" in values else (b - a) / 50
    except ValueError:
        raise ValueError("a, b, eps и step должны быть числами")

    if a >= b:
        raise ValueError("должно быть a < b")
    if eps <= 0 or step <= 0:
        raise ValueError("eps и step должны быть положительными")

    return {"f": func, "formula": values["f"], "a": a, "b": b, "eps": eps, "step": step}
