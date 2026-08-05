import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify

x = symbols("x")


def plot_function(expression):
    expr = sympify(expression)
    f = lambdify(x, expr, "numpy")

    x_values = np.linspace(-10, 10, 500)
    y_values = f(x_values)

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

        expr = sympify(exp)

        f = lambdify(x, expr, "numpy")

        y = f(x_values)

        ax.plot(x_values, y, label=exp)

    ax.grid(True)

    ax.legend()

    ax.set_title("Multiple Function Plot")

    return fig