import math

FUNCTIONS = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan, "tg": math.tan,
    "exp": math.exp, "sqrt": math.sqrt, "abs": abs,
    "ln": math.log, "log": math.log, "lg": math.log10,
    "pi": math.pi, "e": math.e,
}


def parse_expression(text, allowed_names):
    # строка из файла -> скомпилированное выражение; ^ разрешаем как степень
    code = compile(text.replace("^", "**"), "<expr>", "eval")
    for name in code.co_names:
        if name not in allowed_names and name not in FUNCTIONS:
            raise ValueError(f"неизвестное имя в формуле: {name}")
    return code


def make_system(texts, params):
    # список строк f1..fn -> функция F(x), возвращающая вектор значений
    n = len(texts)
    var_names = [f"x{i + 1}" for i in range(n)]
    codes = [parse_expression(t, set(var_names) | set(params)) for t in texts]

    def system(x):
        scope = {**FUNCTIONS, **params, **dict(zip(var_names, x))}
        return [eval(code, {"__builtins__": {}}, scope) for code in codes]

    return system
