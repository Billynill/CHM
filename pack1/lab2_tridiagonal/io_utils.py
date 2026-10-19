def read_tridiagonal(path):
    a, b, c, d = [], [], [], []
    with open(path, encoding="utf-8") as f:
        for line_no, raw in enumerate(f, start=1):
            line = raw.split("#", 1)[0].replace("|", " ").strip()
            if not line:
                continue
            try:
                values = [float(x) for x in line.split()]
            except ValueError:
                raise ValueError(f"строка {line_no}: не удалось прочитать числа: {raw.strip()!r}") from None
            if len(values) != 4:
                raise ValueError(f"строка {line_no}: нужно 4 числа (a b c | d), а получено {len(values)}")
            a.append(values[0])
            b.append(values[1])
            c.append(values[2])
            d.append(values[3])

    if not b:
        raise ValueError("файл пустой")
    if a[0] != 0 or c[-1] != 0:
        raise ValueError("в первой строке a должно быть 0, в последней c должно быть 0")

    return a, b, c, d
