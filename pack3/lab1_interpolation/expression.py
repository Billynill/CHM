import math

ALLOWED = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan, "tg": math.tan,
    "exp": math.exp, "sqrt": math.sqrt, "abs": abs,
    "ln": math.log, "log": math.log, "lg": math.log10,
    "pi": math.pi, "e": math.e,
}


def parse_function(text):
    code = compile(text.replace("^", "**"), "<f(x)>", "eval")
    for name in code.co_names:
        if name != "x" and name not in ALLOWED:
            raise ValueError(f"неизвестное имя в формуле: {name}")

    def f(x):
        return eval(code, {"__builtins__": {}}, {**ALLOWED, "x": x})

    return f


def parse_number(text):
    code = compile(text.replace("^", "**"), "<number>", "eval")
    for name in code.co_names:
        if name not in ALLOWED:
            raise ValueError(f"неизвестное имя в числе: {name}")
    return float(eval(code, {"__builtins__": {}}, ALLOWED))
