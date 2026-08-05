from sympy import (
    symbols,
    simplify,
    expand,
    factor,
    Eq,
    solve,
    sympify,
    diff,
    integrate,
    limit,
)

x = symbols("x")


def simplify_expression(expression):
    return simplify(sympify(expression))


def expand_expression(expression):
    return expand(sympify(expression))


def factor_expression(expression):
    return factor(sympify(expression))


def solve_equation(left_expression, right_expression="0"):
    equation = Eq(sympify(left_expression), sympify(right_expression))
    return solve(equation, x)


def derivative(expression):
    expr = sympify(expression)
    return diff(expr, x)


def integration(expression):
    expr = sympify(expression)
    return integrate(expr, x)


def calculate_limit(expression, value):
    expr = sympify(expression)
    return limit(expr, x, value)