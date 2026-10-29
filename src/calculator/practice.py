"""
Practice question generator and answer checker.

Questions are generated with random numbers and checked exactly
with SymPy, so practice works without any AI provider.
"""

import random

from sympy import diff, expand, integrate, latex, simplify, symbols

from src.calculator.symbolic import parse_math

x = symbols("x")

TOPICS = [
    "Arithmetic",
    "Linear equations",
    "Quadratic equations",
    "Derivatives",
    "Integrals",
]

LEVELS = ["Easy", "Medium", "Hard"]


def _num(level, low=1):

    high = {"Easy": 9, "Medium": 20, "Hard": 50}[level]

    return random.randint(low, high)


def _signed(level):

    return random.choice([-1, 1]) * _num(level)


def generate(topic, level, rng=None):
    """
    Return a question dict: topic, prompt, latex, answer (SymPy),
    answer_latex and a hint.
    """

    if rng is not None:
        random.seed(rng)

    if topic == "Arithmetic":

        a, b, c = _num(level), _num(level), _num(level)

        expr_text = random.choice([
            f"{a} + {b} * {c}",
            f"({a} + {b}) * {c}",
            f"{a * c} / {c} + {b}",
            f"{a}^2 - {b}",
        ])

        expr = parse_math(expr_text)

        return {
            "topic": topic,
            "prompt": "Evaluate",
            "latex": latex(
                parse_math(expr_text, evaluate=False),
                mul_symbol="times",
            ),
            "answer": expr,
            "answer_latex": latex(expr),
            "hint": "Brackets first, then powers, then × and ÷, then + and −.",
        }

    if topic == "Linear equations":

        root = _signed(level)
        a = _num(level)
        b = _signed(level)

        left = a * x + b

        return {
            "topic": topic,
            "prompt": "Solve for x",
            "latex": f"{latex(left)} = {a * root + b}",
            "answer": [root],
            "answer_latex": f"x = {root}",
            "hint": "Move the constant to the right side, then divide by the coefficient of x.",
        }

    if topic == "Quadratic equations":

        r1, r2 = _signed(level), _signed(level)
        a = 1 if level == "Easy" else random.randint(1, 3)

        poly = expand(a * (x - r1) * (x - r2))

        roots = sorted({r1, r2})

        return {
            "topic": topic,
            "prompt": "Solve for x (give all solutions, separated by commas)",
            "latex": f"{latex(poly)} = 0",
            "answer": roots,
            "answer_latex": ", ".join(f"x = {r}" for r in roots),
            "hint": "Factorise, or use x = (−b ± √(b² − 4ac)) / 2a.",
        }

    if topic == "Derivatives":

        n = random.randint(2, {"Easy": 3, "Medium": 5, "Hard": 6}[level])
        a, b = _num(level), _signed(level)

        expr = random.choice([
            a * x**n + b * x,
            a * x**n + b * x**2 + _num(level),
            *(
                [a * x**2 * parse_math("sin(x)"), parse_math(f"e^({a}x)") * x]
                if level == "Hard" else []
            ),
        ])

        return {
            "topic": topic,
            "prompt": "Find dy/dx",
            "latex": f"y = {latex(expr)}",
            "answer": diff(expr, x),
            "answer_latex": latex(diff(expr, x)),
            "hint": "Power rule: d/dx xⁿ = n·xⁿ⁻¹. Differentiate term by term.",
            "integrand": None,
        }

    # Integrals
    n = random.randint(1, {"Easy": 2, "Medium": 4, "Hard": 5}[level])
    a, b = _num(level), _signed(level)

    expr = (n + 1) * a * x**n + b

    return {
        "topic": "Integrals",
        "prompt": "Find the indefinite integral (you can leave out + C)",
        "latex": rf"\int \left({latex(expr)}\right)\,dx",
        "answer": integrate(expr, x),
        "answer_latex": latex(integrate(expr, x)) + " + C",
        "hint": "∫ xⁿ dx = xⁿ⁺¹ / (n + 1) + C",
        "integrand": expr,
    }


def _parse_solutions(text):

    cleaned = text.replace("x=", "").replace("x =", "")

    return sorted(
        {parse_math(part) for part in cleaned.split(",") if part.strip()},
        key=lambda value: float(value),
    )


def check(question, user_answer):
    """
    Return True when the user's answer is mathematically correct.
    Raises ValueError when the answer cannot be read.
    """

    if not user_answer or not user_answer.strip():
        raise ValueError("Type an answer first.")

    if question["topic"] in ("Linear equations", "Quadratic equations"):

        given = _parse_solutions(user_answer)

        return (
            len(given) == len(question["answer"])
            and all(
                simplify(g - a) == 0
                for g, a in zip(given, question["answer"])
            )
        )

    given = parse_math(user_answer.replace("+ C", "").replace("+C", ""))

    if question["topic"] == "Integrals":

        # Any antiderivative is correct, whatever its constant.
        return simplify(diff(given, x) - question["integrand"]) == 0

    return simplify(given - question["answer"]) == 0
