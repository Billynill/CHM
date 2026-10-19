def read_matrix(path):
    eps = None
    rows = []
    with open(path, encoding="utf-8") as f:
        for line_no, raw in enumerate(f, start=1):
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            if line.lower().startswith("eps"):
                try:
                    eps = float(line.split("=", 1)[1])
                except (IndexError, ValueError):
                    raise ValueError(f"строка {line_no}: точность пишется так: eps = 0.01") from None
                continue
            try:
                rows.append([float(x) for x in line.split()])
            except ValueError:
                raise ValueError(f"строка {line_no}: не удалось прочитать числа: {raw.strip()!r}") from None

    if eps is None or eps <= 0:
        raise ValueError("не задана точность (строка вида eps = 0.01)")
    if not rows:
        raise ValueError("нет матрицы")

    n = len(rows)
    for i, row in enumerate(rows, start=1):
        if len(row) != n:
            raise ValueError(f"в строке {i} матрицы должно быть {n} чисел, а получено {len(row)}")

    return rows, eps
