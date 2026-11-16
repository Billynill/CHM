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
    for key in ("x", "f", "x*"):
        if key not in values:
            raise ValueError(f"в файле не хватает строки {key} = ...")

    try:
        xs = [float(v) for v in values["x"].split()]
        fs = [float(v) for v in values["f"].split()]
        x_star = float(values["x*"])
    except ValueError:
        raise ValueError("x, f и x* должны быть числами")

    if len(xs) != len(fs):
        raise ValueError(f"количество x ({len(xs)}) и f ({len(fs)}) не совпадает")
    if len(xs) < 2:
        raise ValueError("нужно хотя бы 2 узла")
    if any(xs[i] >= xs[i + 1] for i in range(len(xs) - 1)):
        raise ValueError("узлы x должны идти строго по возрастанию")

    return {"x": xs, "f": fs, "x_star": x_star}
