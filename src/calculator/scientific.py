import math


def power(a, b):
    try:
        return math.pow(a, b)
    except OverflowError as error:
        raise ValueError("Result is too large to calculate.") from error
    except ValueError as error:
        raise ValueError(
            "Power is not defined for these numbers."
        ) from error


def square_root(a):
    if a < 0:
        raise ValueError("Negative number is not allowed.")
    return math.sqrt(a)


def sine(angle):
    return math.sin(math.radians(angle))


def cosine(angle):
    return math.cos(math.radians(angle))


def tangent(angle):
    if (angle - 90) % 180 == 0:
        raise ValueError(f"tan({angle}°) is undefined.")
    return math.tan(math.radians(angle))

def evaluate_expression(text, degrees=False):
    """
    Evaluate a typed calculation like "2(3+4)^2", "sin 30" or "√2 × π".

    Returns (exact, decimal): the exact SymPy value and a float.
    """

    import sympy

    from src.calculator.symbolic import TRANSFORMATIONS

    if text is None or not str(text).strip():
        raise ValueError("Please enter a calculation.")

    cleaned = (
        str(text)
        .replace("×", "*")
        .replace("÷", "/")
        .replace("−", "-")
        .replace("π", "pi")
        .replace("√", "sqrt ")
        .replace("%", "/100")
    )

    if degrees:
        to_radians = sympy.pi / 180
        trig = {
            "sin": lambda a: sympy.sin(a * to_radians),
            "cos": lambda a: sympy.cos(a * to_radians),
            "tan": lambda a: sympy.tan(a * to_radians),
            "asin": lambda a: sympy.asin(a) / to_radians,
            "acos": lambda a: sympy.acos(a) / to_radians,
            "atan": lambda a: sympy.atan(a) / to_radians,
        }
    else:
        trig = {}

    names = {
        "e": sympy.E,
        "pi": sympy.pi,
        "ln": sympy.log,
        "log": lambda a: sympy.log(a, 10),
        **trig,
    }

    try:
        value = sympy.parse_expr(
            cleaned,
            local_dict=names,
            transformations=TRANSFORMATIONS,
        )
    except Exception as error:
        raise ValueError(f"Could not understand '{text}'.") from error

    if getattr(value, "free_symbols", None):
        raise ValueError(
            "Use numbers only here. For x, y ... use Algebra & Calculus."
        )

    value = sympy.nsimplify(value) if value.is_Float else sympy.simplify(value)

    if value in (sympy.zoo, sympy.oo, -sympy.oo, sympy.nan):
        raise ValueError("The result is undefined (for example, division by zero).")

    decimal = complex(value.evalf()) if not value.is_real else float(value.evalf())

    return value, decimal
