import csv
import io

from nicegui import ui

from src.llm.provider_health import SUPPORTED_PROVIDERS, check_all_providers
from webapp import state
from webapp.layout import frame

STATUS_STYLE = {
    'CONFIGURED': ('check_circle', 'positive', 'Ready'),
    'MISSING_API_KEY': ('key_off', 'warning', 'API key missing'),
    'UNSUPPORTED': ('block', 'negative', 'Not supported'),
}

COLUMNS = [
    {'name': 'time', 'label': 'Time', 'field': 'time', 'align': 'left', 'sortable': True},
    {'name': 'module', 'label': 'Tool', 'field': 'module', 'align': 'left', 'sortable': True},
    {'name': 'operation', 'label': 'Operation', 'field': 'operation', 'align': 'left'},
    {'name': 'input', 'label': 'Input', 'field': 'input', 'align': 'left',
     'style': 'max-width: 260px; white-space: normal'},
    {'name': 'result', 'label': 'Result', 'field': 'result', 'align': 'left',
     'style': 'max-width: 320px; white-space: normal'},
]


@ui.page('/history')
def history_page():

    with frame('/history', 'My History', 'Everything you solved, saved in this browser', 'history'):

        @ui.refreshable
        def history_view():

            records = list(reversed(state.get_history()))

            if not records:
                with ui.column().classes('w-full items-center py-10 gap-2'):
                    ui.icon('history', size='3rem', color='grey-5')
                    ui.label('No history yet. Use any tool and your work will show up here.').classes('text-grey-7')
                    ui.button('Start with Ask MathMind', icon='psychology',
                              on_click=lambda: ui.navigate.to('/ask')).props('unelevated')
                return

            with ui.row().classes('w-full gap-3'):
                tools = {}
                for record in records:
                    tools[record['module']] = tools.get(record['module'], 0) + 1
                with ui.card().classes('mm-card shadow-none p-4'):
                    ui.label('Total').classes('text-grey-7 text-sm')
                    ui.label(str(len(records))).classes('text-2xl font-bold text-indigo-10')
                for tool, count in sorted(tools.items(), key=lambda t: -t[1])[:5]:
                    with ui.card().classes('mm-card shadow-none p-4'):
                        ui.label(tool).classes('text-grey-7 text-sm')
                        ui.label(str(count)).classes('text-2xl font-bold text-indigo-10')

            table = ui.table(columns=COLUMNS, rows=records, pagination=15).props('flat bordered') \
                .classes('w-full mm-card')
            with table.add_slot('top-right'):
                search = ui.input(placeholder='Search').props('dense outlined clearable')
                search.bind_value(table, 'filter')

            with ui.row().classes('gap-2'):
                ui.button('Download CSV', icon='download', on_click=lambda: download(records)).props('unelevated')
                ui.button('Clear history', icon='delete', on_click=clear).props('flat color=grey-8')

        def download(records):

            buffer = io.StringIO()
            writer = csv.DictWriter(buffer, fieldnames=['time', 'module', 'operation', 'input', 'result'])
            writer.writeheader()
            writer.writerows(records)
            ui.download.content(buffer.getvalue(), 'mathmind_history.csv')

        def clear():

            state.clear_history()
            history_view.refresh()

        history_view()


@ui.page('/status')
def status_page():

    with frame('/status', 'AI Provider Status', 'Which AI models are configured and ready', 'monitor_heart'):

        ui.label('API keys are never shown. Add them as environment variables or Hugging Face Space secrets '
                 '(see the README).').classes('text-grey-8')

        @ui.refreshable
        def providers():

            results = check_all_providers()

            with ui.grid(columns=2).classes('w-full gap-4'):
                for provider in SUPPORTED_PROVIDERS:

                    result = results.get(provider, {})
                    icon, colour, text = STATUS_STYLE.get(result.get('status'), ('help', 'grey', 'Unknown'))

                    with ui.card().classes('mm-card shadow-none p-5 gap-2'):
                        with ui.row().classes('w-full items-center'):
                            ui.label(provider).classes('text-xl font-bold text-indigo-10')
                            ui.space()
                            ui.chip(text, icon=icon, color=colour, text_color='white')
                        ui.label(f"Model: {result.get('model') or 'N/A'}").classes('text-grey-8')
                        ui.label(result.get('message', '')).classes('text-sm text-grey-7')
                        if provider == 'Ollama':
                            ui.label('Ollama runs on your own computer and needs no API key.') \
                                .classes('text-sm text-grey-7')

        providers()

        ui.button('Refresh', icon='refresh', on_click=providers.refresh).props('unelevated')
