from expression import parse_function


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


def read_task(path):
    values = read_keys(path)
    for key in ("y(x)", "x0", "xk", "h1", "h2"):
        if key not in values:
            raise ValueError(f"в файле не хватает строки {key} = ...")

    try:
        y = parse_function(values["y(x)"])
        antiderivative = parse_function(values["F(x)"]) if "F(x)" in values else None
    except (SyntaxError, ValueError) as e:
        raise ValueError(f"не удалось разобрать формулу: {e}")

    try:
        a, b = float(values["x0"]), float(values["xk"])
        h1, h2 = float(values["h1"]), float(values["h2"])
    except ValueError:
        raise ValueError("x0, xk, h1, h2 должны быть числами")

    if a >= b:
        raise ValueError("должно быть x0 < xk")
    if h1 <= 0 or h2 <= 0:
        raise ValueError("шаги должны быть положительными")
    if h2 >= h1:
        raise ValueError("h2 должен быть меньше h1 (метод Рунге-Ромберга уточняет результат с мелким шагом)")

    return {"y": y, "formula": values["y(x)"], "F": antiderivative, "F_formula": values.get("F(x)"),
            "a": a, "b": b, "h1": h1, "h2": h2}
