import math

ALLOWED = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan, "tg": math.tan,
    "exp": math.exp, "sqrt": math.sqrt, "abs": abs,
    "ln": math.log, "log": math.log, "lg": math.log10,
    "pi": math.pi, "e": math.e,
}


def parse_function(text):
    # строка из файла -> функция f(x); ^ разрешаем как степень
    source = text.replace("^", "**")
    code = compile(source, "<f(x)>", "eval")
    for name in code.co_names:
        if name != "x" and name not in ALLOWED:
            raise ValueError(f"неизвестное имя в формуле: {name}")

    def f(x):
        return eval(code, {"__builtins__": {}}, {**ALLOWED, "x": x})

    f(1.0)  # проверка, что формула вообще считается
    return f
