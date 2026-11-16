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
    for key in ("x", "y", "x*"):
        if key not in values:
            raise ValueError(f"в файле не хватает строки {key} = ...")

    try:
        xs = [float(v) for v in values["x"].split()]
        ys = [float(v) for v in values["y"].split()]
        x_star = float(values["x*"])
    except ValueError:
        raise ValueError("x, y и x* должны быть числами")

    if len(xs) != len(ys):
        raise ValueError(f"количество x ({len(xs)}) и y ({len(ys)}) не совпадает")
    if any(xs[i] >= xs[i + 1] for i in range(len(xs) - 1)):
        raise ValueError("узлы x должны идти строго по возрастанию")

    return {"x": xs, "y": ys, "x_star": x_star}
