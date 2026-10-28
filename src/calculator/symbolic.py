from sympy import (
    E,
    symbols,
    simplify,
    expand,
    factor,
    Eq,
    solve,
    diff,
    integrate,
    limit,
)
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

x = symbols("x")

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


def parse_math(expression):
    """
    Parse user input like "2x+3", "x^2 + 3x" or "sin x".
    """

    if expression is None or not str(expression).strip():
        raise ValueError("Please enter an expression.")

    try:
        return parse_expr(
            str(expression).strip(),
            local_dict={"e": E},
            transformations=TRANSFORMATIONS,
        )
    except Exception as error:
        raise ValueError(
            f"Could not understand '{expression}'. "
            "Example: x^2 + 2x + 1"
        ) from error


def main_variable(expr):
    """
    Use x if present, otherwise the expression's only/first variable.
    """

    free = sorted(expr.free_symbols, key=lambda s: s.name)

    if not free or x in free:
        return x

    return free[0]


def simplify_expression(expression):
    return simplify(parse_math(expression))


def expand_expression(expression):
    return expand(parse_math(expression))


def factor_expression(expression):
    return factor(parse_math(expression))


def solve_equation(left_expression, right_expression="0"):
    left = parse_math(left_expression)
    right = parse_math(right_expression or "0")
    return solve(Eq(left, right), main_variable(left - right))


def derivative(expression):
    expr = parse_math(expression)
    return diff(expr, main_variable(expr))


def integration(expression):
    expr = parse_math(expression)
    return integrate(expr, main_variable(expr))


def calculate_limit(expression, value):
    expr = parse_math(expression)
    return limit(expr, main_variable(expr), value)
