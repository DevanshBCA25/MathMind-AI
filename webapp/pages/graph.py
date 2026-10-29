import numpy as np
import plotly.graph_objects as go
from nicegui import ui
from sympy import diff, latex

from src.calculator.graph import evaluate
from src.calculator.symbolic import main_variable, parse_math
from webapp import state
from webapp.layout import frame
from webapp.widgets import error_box, math

COLOURS = ['#4f46e5', '#db2777', '#059669', '#d97706', '#0891b2', '#7c3aed']

EXAMPLES = {
    'Parabola & sine': 'x^2/4 - 3\n3sin(x)',
    'Hyperbola': '1/x',
    'Exponential & log': 'e^x\nln(x)',
    'Damped wave': 'e^(-x/5) cos(2x)',
}


def build_figure(expressions, x_min, x_max, show_derivative):

    x_values = np.linspace(x_min, x_max, 800)

    fig = go.Figure()

    for index, text in enumerate(expressions):

        colour = COLOURS[index % len(COLOURS)]

        fig.add_trace(go.Scatter(
            x=x_values.tolist(),
            y=[None if not np.isfinite(y) else float(y) for y in evaluate(text, x_values)],
            mode='lines',
            name=f'y = {text}',
            line={'color': colour, 'width': 3},
        ))

        if show_derivative:

            expr = parse_math(text)
            slope = str(diff(expr, main_variable(expr)))

            fig.add_trace(go.Scatter(
                x=x_values.tolist(),
                y=[None if not np.isfinite(y) else float(y) for y in evaluate(slope, x_values)],
                mode='lines',
                name=f"y' = {slope}",
                line={'color': colour, 'dash': 'dash', 'width': 2},
            ))

    fig.update_layout(
        height=520,
        margin={'l': 60, 'r': 20, 't': 20, 'b': 40},
        legend={'orientation': 'h', 'y': -0.15},
        hovermode='x unified',
        plot_bgcolor='white',
        xaxis={'zeroline': True, 'zerolinewidth': 2, 'zerolinecolor': '#94a3b8', 'gridcolor': '#eef2ff', 'title': 'x'},
        yaxis={'zeroline': True, 'zerolinewidth': 2, 'zerolinecolor': '#94a3b8', 'gridcolor': '#eef2ff', 'title': 'y'},
    )

    return fig


@ui.page('/graph')
def graph_page():

    with frame('/graph', 'Graph Plotter', 'Plot functions of x. Zoom, pan and hover over the graph.', 'show_chart'):

        with ui.card().classes('mm-card w-full shadow-none p-5 gap-3'):

            with ui.row().classes('w-full gap-4 no-wrap items-start'):
                functions = ui.textarea('Functions (one per line)', value=EXAMPLES['Parabola & sine']) \
                    .props('outlined autogrow').classes('flex-grow')
                with ui.column().classes('gap-2 w-72'):
                    ui.label('x range').classes('text-grey-8 text-sm')
                    x_range = ui.range(min=-50, max=50, step=0.5, value={'min': -10, 'max': 10}) \
                        .props('label-always')
                    derivative = ui.switch('Show derivative (dashed)')

            with ui.row().classes('gap-2'):
                for name, text in EXAMPLES.items():
                    ui.chip(name, icon='insights', on_click=lambda t=text: (functions.set_value(t), draw())) \
                        .props('outline color=primary clickable')

            ui.button('Plot', icon='show_chart', on_click=lambda: draw()).props('unelevated')

        output = ui.column().classes('w-full gap-3')

        def draw():

            expressions = [line.strip() for line in (functions.value or '').splitlines() if line.strip()]
            x_min, x_max = x_range.value['min'], x_range.value['max']

            output.clear()

            with output:

                if not expressions:
                    error_box('Enter at least one function.')
                    return

                if x_min >= x_max:
                    error_box('Choose a range where the start is less than the end.')
                    return

                try:
                    equations = r',\quad '.join(f'y = {latex(parse_math(e))}' for e in expressions)
                    figure = build_figure(expressions, x_min, x_max, derivative.value)
                except Exception as error:
                    error_box(f'Could not plot: {error}')
                    return

                with ui.card().classes('mm-card w-full shadow-none p-4'):
                    math(equations)
                    ui.plotly(figure).classes('w-full h-[520px]')

            state.add_history('Graph Plotter', 'Plot', '; '.join(expressions), f'x from {x_min} to {x_max}')

        x_range.on('change', lambda: draw())
        derivative.on_value_change(lambda: draw())
        draw()
