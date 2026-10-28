import numpy as np
import pytest

from src.calculator import graph, scientific, statistics, symbolic


def test_implicit_multiplication():

    assert str(symbolic.factor_expression("x^2+2x+1")) == "(x + 1)**2"

    assert symbolic.solve_equation("2x+3", "7") == [2]


def test_other_variables():

    assert str(symbolic.derivative("y^2")) == "2*y"

    assert symbolic.solve_equation("t^2", "9") == [-3, 3]


def test_bad_expression_gives_friendly_error():

    with pytest.raises(ValueError):
        symbolic.simplify_expression("")

    with pytest.raises(ValueError):
        symbolic.simplify_expression("2++*")


def test_graph_constant_and_asymptote():

    x_values = np.linspace(-10, 10, 500)

    assert np.all(graph.evaluate("5", x_values) == 5)

    # The line must break at x = 0 instead of joining -inf to +inf.
    assert np.isnan(graph.evaluate("1/x", x_values)).any()


def test_scientific_edge_cases():

    with pytest.raises(ValueError):
        scientific.tangent(90)

    with pytest.raises(ValueError):
        scientific.power(10, 400)


def test_statistics_input():

    assert statistics.mean("1 2 3") == 2

    assert statistics.mode("1,2,2,3") == 2

    assert statistics.mode("1,2,3").startswith("No mode")

    with pytest.raises(ValueError):
        statistics.variance("5")
