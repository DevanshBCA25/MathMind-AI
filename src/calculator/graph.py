import numpy as np
import matplotlib.pyplot as plt
from sympy import lambdify

from src.calculator.symbolic import parse_math, main_variable


def evaluate(expression, x_values):
    """
    Evaluate an expression on x_values.

    Handles constant functions and breaks the line at
    asymptotes (e.g. 1/x) instead of joining them.
    """

    expr = parse_math(expression)

    f = lambdify(main_variable(expr), expr, "numpy")

    with np.errstate(all="ignore"):
        y_values = np.asarray(f(x_values), dtype=complex)

    y_values = np.broadcast_to(y_values, x_values.shape)

    # Keep only real values (sqrt/log of negatives become gaps).
    y_values = np.where(
        np.abs(y_values.imag) < 1e-9,
        y_values.real,
        np.nan,
    )

    finite = y_values[np.isfinite(y_values)]

    if finite.size > 1:

        low, high = np.percentile(finite, [1, 99])

        spread = max(high - low, 1e-9)

        jumps = np.abs(np.diff(y_values)) > spread

        y_values[1:][jumps] = np.nan

    return y_values


def plot_function(expression):

    x_values = np.linspace(-10, 10, 500)
    y_values = evaluate(expression, x_values)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(x_values, y_values, label=expression)

    ax.set_title("Function Plot")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    ax.grid(True)
    ax.legend()

    return fig


def plot_multiple(expressions):

    fig, ax = plt.subplots(figsize=(8, 5))

    x_values = np.linspace(-10, 10, 500)

    for exp in expressions:

        if not exp.strip():
            continue

        y = evaluate(exp, x_values)

        ax.plot(x_values, y, label=exp)

    ax.grid(True)

    ax.legend()

    ax.set_title("Multiple Function Plot")

    return fig
