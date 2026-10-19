def read_system(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line_no, raw in enumerate(f, start=1):
            line = raw.split("#", 1)[0].replace("|", " ").strip()
            if not line:
                continue
            try:
                rows.append([float(x) for x in line.split()])
            except ValueError:
                raise ValueError(f"строка {line_no}: не удалось прочитать числа: {raw.strip()!r}") from None

    if not rows:
        raise ValueError("файл пустой")

    n = len(rows)
    for i, row in enumerate(rows, start=1):
        if len(row) != n + 1:
            raise ValueError(f"в уравнении {i} должно быть {n + 1} чисел, а получено {len(row)}")

    a = [row[:-1] for row in rows]
    b = [row[-1] for row in rows]
    return a, b
