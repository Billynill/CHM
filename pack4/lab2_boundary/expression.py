import math

ALLOWED = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan, "tg": math.tan,
    "exp": math.exp, "sqrt": math.sqrt, "abs": abs,
    "ln": math.log, "log": math.log, "lg": math.log10,
    "atan": math.atan, "arctg": math.atan,
    "pi": math.pi, "e": math.e,
}


def compile_checked(text, variables):
    code = compile(text.replace("^", "**"), "<expr>", "eval")
    for name in code.co_names:
        if name not in variables and name not in ALLOWED:
            raise ValueError(f"неизвестное имя в формуле: {name}")
    return code


def parse_function(text):
    code = compile_checked(text, ("x",))

    def f(x):
        return eval(code, {"__builtins__": {}}, {**ALLOWED, "x": x})

    return f


def parse_number(text):
    code = compile_checked(text, ())
    return float(eval(code, {"__builtins__": {}}, ALLOWED))
