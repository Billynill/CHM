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
    for key in ("y''", "a", "b", "y(a)", "y'(a)", "h"):
        if key not in values:
            raise ValueError(f"в файле не хватает строки {key} = ...")

    try:
        f = parse_function(values["y''"], ("x", "y", "z"))
        exact = parse_function(values["y_exact"], ("x",)) if "y_exact" in values else None
    except (SyntaxError, ValueError) as e:
        raise ValueError(f"не удалось разобрать формулу: {e}")

    try:
        a, b = float(values["a"]), float(values["b"])
        y0, z0 = float(values["y(a)"]), float(values["y'(a)"])
        h = float(values["h"])
    except ValueError:
        raise ValueError("a, b, y(a), y'(a), h должны быть числами")

    if a >= b:
        raise ValueError("должно быть a < b")
    if h <= 0:
        raise ValueError("шаг h должен быть положительным")

    return {"f": f, "formula": values["y''"], "exact": exact, "exact_formula": values.get("y_exact"),
            "a": a, "b": b, "y0": y0, "z0": z0, "h": h}
