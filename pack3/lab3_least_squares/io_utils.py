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
    for key in ("x", "y"):
        if key not in values:
            raise ValueError(f"в файле не хватает строки {key} = ...")

    try:
        xs = [float(v) for v in values["x"].split()]
        ys = [float(v) for v in values["y"].split()]
        degrees = [int(v) for v in values.get("degrees", "1 2 3").split()]
    except ValueError:
        raise ValueError("x и y должны быть числами, degrees - целыми числами")

    if len(xs) != len(ys):
        raise ValueError(f"количество x ({len(xs)}) и y ({len(ys)}) не совпадает")
    if not degrees or min(degrees) < 0:
        raise ValueError("степени должны быть неотрицательными")
    if len(set(xs)) <= max(degrees):
        raise ValueError(f"для степени {max(degrees)} нужно хотя бы {max(degrees) + 1} разных точек")

    return {"x": xs, "y": ys, "degrees": degrees}
