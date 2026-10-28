import streamlit as st
from sympy import latex

from src.ui.common import current_provider, page_header
from src.utils.helpers import save_operation

from src.calculator.symbolic import (
    parse_math,
    simplify_expression,
    expand_expression,
    factor_expression,
    solve_equation,
    derivative,
    integration,
    calculate_limit,
)
from src.calculator.steps import (
    derivative_rules,
    explanation_prompt,
    verify,
)


EXAMPLES = {
    "Simplify": "(x^2 - 1)/(x - 1)",
    "Expand": "(x + 2)^3",
    "Factor": "x^2 + 5x + 6",
    "Solve Equation": "2x^2 + 3x - 5",
    "Derivative": "x^2 sin(x)",
    "Integration": "x e^x",
    "Limit": "sin(x)/x",
}


def _calculate(operation, expression, right_side, limit_value):

    if operation == "Simplify":
        return simplify_expression(expression)

    if operation == "Expand":
        return expand_expression(expression)

    if operation == "Factor":
        return factor_expression(expression)

    if operation == "Solve Equation":
        return solve_equation(expression, right_side)

    if operation == "Derivative":
        return derivative(expression)

    if operation == "Integration":
        return integration(expression)

    return calculate_limit(expression, limit_value)


def _question_latex(operation, expression, right_side, limit_value):

    expr = latex(parse_math(expression))

    if operation == "Solve Equation":
        return rf"{expr} = {latex(parse_math(right_side or '0'))}"

    if operation == "Derivative":
        return rf"\frac{{d}}{{dx}}\left({expr}\right)"

    if operation == "Integration":
        return rf"\int {expr}\,dx"

    if operation == "Limit":
        return rf"\lim_{{x \to {limit_value}}} {expr}"

    return expr


def _result_latex(operation, result):

    if operation == "Solve Equation":

        if not result:
            return r"\text{No solution}"

        return r",\quad ".join(f"x = {latex(r)}" for r in result)

    if operation == "Integration":
        return latex(result) + " + C"

    return latex(result)


def show():

    page_header(
        "∫",
        "Algebra & Calculus",
        "Write maths naturally: 2x^2 + 3x - 5, sin(x)/x",
    )

    operation = st.selectbox(
        "Choose Operation",
        list(EXAMPLES),
        key="symbolic_operation",
    )

    expression = st.text_input(
        "Enter Expression",
        placeholder=f"e.g. {EXAMPLES[operation]}",
        key="expression",
    )

    right_side = "0"

    if operation == "Solve Equation":
        right_side = st.text_input(
            "Right Side",
            value="0",
            key="right_side",
        )

    limit_value = 0

    if operation == "Limit":
        limit_value = st.number_input(
            "x tends to",
            value=0,
            key="limit_value",
        )

    just_ran = st.button(
        "Calculate",
        key="symbolic_button",
        type="primary",
    )

    if just_ran:

        st.session_state.symbolic_run = (
            operation,
            expression or EXAMPLES[operation],
            right_side,
            limit_value,
        )

        st.session_state.pop("symbolic_explanation", None)

    run = st.session_state.get("symbolic_run")

    if not run or run[0] != operation:
        return

    operation, expression, right_side, limit_value = run

    try:

        result = _calculate(operation, expression, right_side, limit_value)

    except Exception as error:

        st.error(f"Error: {error}")

        return

    if just_ran:

        save_operation(
            module="Algebra & Calculus",
            operation=operation,
            input_data=expression,
            result=result,
        )

    st.markdown("#### Question")
    st.latex(_question_latex(operation, expression, right_side, limit_value))

    st.markdown("#### Answer")
    st.latex(_result_latex(operation, result))

    if operation == "Derivative":

        rules = derivative_rules(expression)

        if rules:
            st.markdown("**Rules used:** " + " · ".join(rules))

    try:
        checks = verify(operation, expression, result, right_side)
    except Exception:
        checks = []

    if checks:

        with st.expander("✅ Verification (checked with SymPy)", expanded=True):

            for passed, text in checks:

                st.markdown("✔️ Verified" if passed else "⚠️ Could not verify")

                st.latex(text)

    if st.button("🧑‍🏫 Explain the steps with AI"):

        try:

            from src.llm.router import LLMRouter

            with st.spinner(f"Asking {current_provider()}..."):

                st.session_state.symbolic_explanation = LLMRouter().ask(
                    current_provider(),
                    explanation_prompt(
                        operation, expression, result, right_side
                    ),
                )

        except Exception as error:

            st.error(
                f"AI explanation is not available: {error}"
            )

    if st.session_state.get("symbolic_explanation"):

        st.markdown("#### Step-by-step explanation")

        st.markdown(st.session_state.symbolic_explanation)
