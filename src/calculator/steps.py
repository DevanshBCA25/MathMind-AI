"""
Checks and hints that make symbolic answers trustworthy.

Every result is verified with SymPy (substitute solutions back,
differentiate an integral, expand a factorisation) so the app never
shows an answer it could not confirm. The same verified answer is
given to the AI tutor, which only explains it.
"""

from sympy import (
    Add,
    Derivative,
    Function,
    Mul,
    Pow,
    UnevaluatedExpr,
    diff,
    expand,
    latex,
    simplify,
)

from src.calculator.symbolic import main_variable, parse_math


def _is_zero(expr):

    try:
        return simplify(expr) == 0
    except Exception:
        return False


def verify(operation, expression, result, right_side="0"):
    """
    Return a list of (passed, message_latex) checks.
    """

    expr = parse_math(expression)
    var = main_variable(expr)
    checks = []

    if operation == "Solve Equation":

        left = expr
        right = parse_math(right_side or "0")

        for solution in result:

            residual = (left - right).subs(var, solution)

            shown = left.subs(var, UnevaluatedExpr(solution))

            checks.append((
                _is_zero(residual),
                rf"{latex(var)} = {latex(solution)}:\quad "
                rf"{latex(shown)} = "
                rf"{latex(simplify(right.subs(var, solution)))}",
            ))

    elif operation == "Integration":

        back = diff(result, var)

        checks.append((
            _is_zero(back - expr),
            rf"\frac{{d}}{{d{latex(var)}}}\left({latex(result)}\right)"
            rf" = {latex(simplify(back))}",
        ))

    elif operation == "Factor":

        checks.append((
            _is_zero(expand(result) - expand(expr)),
            rf"\text{{Expanding gives back }} {latex(expand(result))}",
        ))

    elif operation in ("Expand", "Simplify"):

        checks.append((
            _is_zero(result - expr),
            r"\text{Same value as the original expression}",
        ))

    return checks


def derivative_rules(expression):
    """
    Name the differentiation rules a student would use.
    """

    expr = parse_math(expression)
    var = main_variable(expr)
    rules = set()

    for node in [expr, *expr.atoms(Add, Mul, Pow, Function)]:

        if not node.has(var):
            continue

        if isinstance(node, Add):
            rules.add("Sum rule: differentiate each term separately")

        elif isinstance(node, Mul):

            parts = [f for f in node.args if f.has(var)]

            if len(parts) >= 2:
                rules.add("Product rule: (uv)' = u'v + uv'")

            if any(isinstance(f, Pow) and f.exp.is_negative for f in parts):
                rules.add("Quotient rule: (u/v)' = (u'v - uv') / v²")

        elif isinstance(node, Pow):

            if not node.exp.has(var):
                rules.add("Power rule: d/dx xⁿ = n·xⁿ⁻¹")
            else:
                rules.add("Exponential rule: d/dx aˣ = aˣ·ln a")

            if node.base != var and node.base.has(var):
                rules.add("Chain rule: multiply by the derivative of the inside")

        elif isinstance(node, Function) and not isinstance(node, Derivative):

            rules.add(
                f"Standard derivative of {node.func.__name__}()"
            )

            if node.args and node.args[0] != var:
                rules.add("Chain rule: multiply by the derivative of the inside")

    return sorted(rules)


def explanation_prompt(operation, expression, result, right_side="0"):
    """
    Prompt for the AI tutor. The answer is already verified,
    so the model only explains the steps.
    """

    task = operation.lower()

    if operation == "Solve Equation":
        task = f"solve the equation {expression} = {right_side}"
    else:
        task = f"find the {task} of {expression}"

    return (
        "You are a friendly maths teacher.\n"
        f"Explain step by step how to {task}.\n"
        f"The correct final answer, verified with SymPy, is: {result}\n"
        "Do not change this answer. Use short numbered steps, "
        "LaTeX between $ signs for formulas, and end with the "
        "final answer."
    )
