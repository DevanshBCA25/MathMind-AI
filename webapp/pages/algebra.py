from nicegui import run, ui
from sympy import latex

from src.calculator.steps import derivative_rules, explanation_prompt, verify
from src.calculator.symbolic import (
    calculate_limit,
    derivative,
    expand_expression,
    factor_expression,
    integration,
    parse_math,
    simplify_expression,
    solve_equation,
)
from webapp import state
from webapp.layout import frame
from webapp.widgets import error_box, math, rich_text, section

EXAMPLES = {
    'Simplify': '(x^2 - 1)/(x - 1)',
    'Expand': '(x + 2)^3',
    'Factor': 'x^2 + 5x + 6',
    'Solve Equation': '2x^2 + 3x - 5',
    'Derivative': 'x^2 sin(x)',
    'Integration': 'x e^x',
    'Limit': 'sin(x)/x',
}


def calculate(operation, expression, right_side, limit_value):

    if operation == 'Simplify':
        return simplify_expression(expression)
    if operation == 'Expand':
        return expand_expression(expression)
    if operation == 'Factor':
        return factor_expression(expression)
    if operation == 'Solve Equation':
        return solve_equation(expression, right_side)
    if operation == 'Derivative':
        return derivative(expression)
    if operation == 'Integration':
        return integration(expression)
    return calculate_limit(expression, limit_value)


def question_latex(operation, expression, right_side, limit_value):

    expr = latex(parse_math(expression))

    if operation == 'Solve Equation':
        return rf"{expr} = {latex(parse_math(right_side or '0'))}"
    if operation == 'Derivative':
        return rf'\frac{{d}}{{dx}}\left({expr}\right)'
    if operation == 'Integration':
        return rf'\int {expr}\,dx'
    if operation == 'Limit':
        return rf'\lim_{{x \to {limit_value}}} {expr}'
    return expr


def answer_latex(operation, result):

    if operation == 'Solve Equation':
        if not result:
            return r'\text{No solution}'
        return r',\quad '.join(f'x = {latex(r)}' for r in result)
    if operation == 'Integration':
        return latex(result) + ' + C'
    return latex(result)


def explain(provider, prompt):

    from src.llm.router import LLMRouter

    return LLMRouter().ask(provider, prompt)


@ui.page('/algebra')
def algebra_page():

    with frame('/algebra', 'Algebra & Calculus', 'Write maths naturally: 2x^2 + 3x - 5, sin(x)/x', 'functions'):

        with ui.card().classes('mm-card w-full shadow-none p-5 gap-3'):

            operation = ui.toggle(list(EXAMPLES), value='Solve Equation') \
                .props('no-caps unelevated toggle-color=primary')

            with ui.row().classes('w-full items-end gap-3 no-wrap'):
                expression = ui.input('Expression').props('outlined').classes('flex-grow')
                equals = ui.label('=').classes('text-2xl pb-3')
                right_side = ui.input('Right side', value='0').props('outlined').classes('w-40')
                limit_value = ui.number('x tends to', value=0).props('outlined').classes('w-40')

            def update_inputs():
                expression.props(f'placeholder="e.g. {EXAMPLES[operation.value]}"')
                equals.visible = right_side.visible = operation.value == 'Solve Equation'
                limit_value.visible = operation.value == 'Limit'

            operation.on_value_change(update_inputs)
            update_inputs()

            calculate_button = ui.button('Calculate', icon='calculate').props('unelevated')

        output = ui.column().classes('w-full gap-3')

        async def on_calculate():

            op = operation.value
            expr = expression.value or EXAMPLES[op]
            right = right_side.value or '0'
            limit_at = limit_value.value or 0

            output.clear()

            try:
                result = await run.io_bound(calculate, op, expr, right, limit_at)
            except Exception as error:
                with output:
                    error_box(error)
                return

            state.add_history('Algebra & Calculus', op, expr, result)

            with output:

                with ui.card().classes('mm-card w-full shadow-none p-5'):
                    section('Question')
                    math(question_latex(op, expr, right, limit_at))
                    section('Answer')
                    math(answer_latex(op, result))

                    if op == 'Derivative':
                        rules = derivative_rules(expr)
                        if rules:
                            with ui.row().classes('gap-2'):
                                for rule in rules:
                                    ui.chip(rule, icon='rule').props('outline color=primary dense')

                try:
                    checks = verify(op, expr, result, right)
                except Exception:
                    checks = []

                if checks:
                    with ui.expansion('Verification (checked with SymPy)', icon='verified', value=True) \
                            .classes('w-full mm-card bg-white'):
                        for passed, text in checks:
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('check_circle' if passed else 'warning', color='positive' if passed else 'warning')
                                ui.label('Verified' if passed else 'Could not verify')
                            math(text)

                explanation = ui.column().classes('w-full')

                async def on_explain():
                    explain_button.props('loading')
                    try:
                        text = await run.io_bound(
                            explain, state.get_provider(), explanation_prompt(op, expr, result, right),
                        )
                        explanation.clear()
                        with explanation:
                            with ui.card().classes('mm-card w-full shadow-none p-5'):
                                section('Step-by-step explanation')
                                rich_text(text)
                    except Exception as error:
                        ui.notify(f'AI explanation is not available: {error}', type='negative', multi_line=True)
                    finally:
                        explain_button.props(remove='loading')

                explain_button = ui.button('Explain the steps with AI', icon='school', on_click=on_explain) \
                    .props('outline')

        calculate_button.on_click(on_calculate)
        expression.on('keydown.enter', on_calculate)
