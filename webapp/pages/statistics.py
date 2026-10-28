import numpy as np
import plotly.graph_objects as go
from nicegui import ui

from src.calculator import statistics as st
from webapp import state
from webapp.layout import frame
from webapp.widgets import error_box, section

SUMMARY = [
    ('Count', lambda d: len(st.get_numbers(d))),
    ('Mean', st.mean),
    ('Median', st.median),
    ('Mode', st.mode),
    ('Std deviation', st.standard_deviation),
    ('Variance', st.variance),
    ('Minimum', st.minimum),
    ('Maximum', st.maximum),
    ('Range', st.data_range),
    ('IQR', st.iqr),
]

TRANSFORMS = {
    'Z score': st.z_score,
    'Normalize (0 to 1)': st.normalize,
    'Standardize': st.standardize,
}


def fmt(value):

    if isinstance(value, (list, tuple, np.ndarray)):
        return ', '.join(fmt(v) for v in value)

    try:
        return f'{float(value):.6g}'
    except (TypeError, ValueError):
        return str(value)


def charts(numbers):

    histogram = go.Figure(go.Histogram(x=numbers, marker_color='#4f46e5', opacity=0.85))
    histogram.update_layout(title='Distribution', height=320, margin={'l': 40, 'r': 10, 't': 40, 'b': 40},
                            plot_bgcolor='white', bargap=0.08)

    box = go.Figure(go.Box(x=numbers, marker_color='#db2777', boxpoints='all', jitter=0.4, name=''))
    box.update_layout(title='Box plot (quartiles and outliers)', height=320,
                      margin={'l': 40, 'r': 10, 't': 40, 'b': 40}, plot_bgcolor='white')

    return histogram, box


@ui.page('/statistics')
def statistics_page():

    with frame('/statistics', 'Statistics', 'Paste numbers separated by commas, spaces or new lines', 'bar_chart'):

        with ui.card().classes('mm-card w-full shadow-none p-5 gap-3'):

            data = ui.textarea('Data', value='12, 15, 11, 18, 21, 15, 30, 14, 16, 15') \
                .props('outlined autogrow').classes('w-full')

            with ui.row().classes('items-center gap-4'):
                percentile = ui.number('Percentile', value=90, min=0, max=100).props('outlined').classes('w-32')
                second = ui.input('Second data set (optional, for correlation)') \
                    .props('outlined').classes('w-96')

            ui.button('Analyse', icon='insights', on_click=lambda: analyse()).props('unelevated')

        output = ui.column().classes('w-full gap-4')

        def analyse():

            text = data.value or ''
            output.clear()

            try:
                numbers = st.get_numbers(text)
                results = [(name, function(text)) for name, function in SUMMARY[:4]]
                if len(numbers) > 1:
                    results += [(name, function(text)) for name, function in SUMMARY[4:]]
                q1, q2, q3 = st.quartiles(text)
                results += [('Q1 · Q2 · Q3', [q1, q2, q3]),
                            (f'{fmt(percentile.value)}th percentile', st.percentile(text, percentile.value or 0))]

                if (second.value or '').strip():
                    results += [('Correlation', st.correlation(text, second.value)),
                                ('Covariance', st.covariance(text, second.value))]

            except Exception as error:
                with output:
                    error_box(error)
                return

            with output:

                with ui.grid(columns=4).classes('w-full gap-3'):
                    for name, value in results:
                        with ui.card().classes('mm-card shadow-none p-4 gap-1'):
                            ui.label(name).classes('text-grey-7 text-sm')
                            ui.label(fmt(value)).classes('text-xl font-bold text-indigo-10 break-all')

                if len(numbers) > 1:
                    histogram, box = charts(numbers)
                    with ui.row().classes('w-full gap-4 no-wrap'):
                        with ui.card().classes('mm-card shadow-none flex-1 p-2'):
                            ui.plotly(histogram).classes('w-full h-80')
                        with ui.card().classes('mm-card shadow-none flex-1 p-2'):
                            ui.plotly(box).classes('w-full h-80')

                    with ui.card().classes('mm-card w-full shadow-none p-4'):
                        section('Transformed values')
                        rows = [{'value': fmt(v), **{name: fmt(f(text)[i]) for name, f in TRANSFORMS.items()}}
                                for i, v in enumerate(numbers)]
                        columns = [{'name': 'value', 'label': 'Value', 'field': 'value', 'align': 'left'}] + \
                                  [{'name': n, 'label': n, 'field': n, 'align': 'left'} for n in TRANSFORMS]
                        ui.table(columns=columns, rows=rows, pagination=10).props('flat dense').classes('w-full')

            state.add_history('Statistics', 'Analyse', text, f'mean {fmt(st.mean(text))}')

        analyse()
