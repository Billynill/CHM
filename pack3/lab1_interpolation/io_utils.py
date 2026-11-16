import re

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


def parse_numbers(text):
    try:
        return [parse_number(v) for v in text.split()]
    except (SyntaxError, ValueError, ZeroDivisionError) as e:
        raise ValueError(f"не удалось прочитать числа '{text}': {e}")


def read_task(path):
    values = read_keys(path)
    if "f(x)" not in values or "x*" not in values:
        raise ValueError("в файле должны быть строки f(x) = ... и x* = ...")

    try:
        f = parse_function(values["f(x)"])
    except (SyntaxError, ValueError) as e:
        raise ValueError(f"не удалось разобрать f(x): {e}")

    x_star = parse_numbers(values["x*"])[0]

    node_sets = []
    for key, value in values.items():
        match = re.fullmatch(r"x(_\w+)?", key)
        if not match:
            continue
        name = match.group(1)[1:] if match.group(1) else ""
        xs = parse_numbers(value)
        if len(xs) < 2:
            raise ValueError(f"в наборе {key} нужно хотя бы 2 узла")
        if len(set(xs)) != len(xs):
            raise ValueError(f"в наборе {key} узлы не должны совпадать")
        try:
            ys = [f(x) for x in xs]
        except (ValueError, ZeroDivisionError) as e:
            raise ValueError(f"f(x) не вычисляется в узлах набора {key}: {e}")
        node_sets.append({"name": name, "x": xs, "y": ys})

    if not node_sets:
        raise ValueError("нет узлов интерполяции (строка x = ... или x_a = ...)")

    return {"f": f, "formula": values["f(x)"], "x_star": x_star, "sets": node_sets}
