from nicegui import run, ui

from webapp import state
from webapp.layout import frame
from webapp.widgets import error_box, math, rich_text, section

EXAMPLES = [
    'what is 25 * 4 + 10',
    'Solve x^2 + 5x + 6 = 0',
    'differentiate x^3 + 2x',
    'Explain why the quadratic formula works',
]

MODES = ['Automatic', 'Calculator', 'Symbolic', 'RAG', 'Agent']

AGENT_STEPS = [
    ('plan', 'Planner', 'psychology'),
    ('solution', 'Solver', 'calculate'),
    ('review', 'Reviewer', 'fact_check'),
    ('explanation', 'Teacher', 'school'),
]


def solve(question, mode, provider, vector_db):

    from src.core.unified_solver import UnifiedSolver

    solver = UnifiedSolver(provider=provider, vector_db=vector_db)

    return solver.solve(
        question=question,
        force_module=None if mode == 'Automatic' else mode.lower(),
    )


@ui.page('/ask')
def ask_page():

    with frame('/ask', 'Ask MathMind', 'One box for every maths question', 'psychology'):

        ui.label(
            'MathMind picks the right engine: calculator, algebra (SymPy), your documents (RAG) '
            'or the Planner → Solver → Reviewer → Teacher agents.'
        ).classes('text-grey-8')

        mode = ui.toggle(MODES, value='Automatic').props('no-caps unelevated toggle-color=primary')

        question = ui.textarea(
            'Your question',
            placeholder='e.g. Solve 2x + 3 = 7',
        ).props('outlined autogrow').classes('w-full text-lg')

        with ui.row().classes('gap-2'):
            for example in EXAMPLES:
                ui.chip(example, icon='lightbulb', on_click=lambda e=example: question.set_value(e)) \
                    .props('outline color=primary clickable')

        button = ui.button('Solve', icon='bolt', on_click=lambda: on_solve()).props('unelevated size=lg')

        result_area = ui.column().classes('w-full gap-3')

        async def on_solve():

            text = (question.value or '').strip()

            result_area.clear()

            if not text:
                with result_area:
                    error_box('Please type a question first.')
                return

            button.props('loading')

            documents = state.get_documents()

            try:
                result = await run.io_bound(
                    solve, text, mode.value, state.get_provider(),
                    documents['db'] if documents else None,
                )
            finally:
                button.props(remove='loading')

            show_result(result_area, result, text)

        question.on('keydown.ctrl.enter', on_solve)


def show_result(container, result, question):

    details = result.get('result', {}) or {}
    module = result.get('module', 'unknown')
    status = result.get('status', 'UNKNOWN')

    state.add_history('Ask MathMind', module, question, result.get('answer', ''))

    with container:

        with ui.row().classes('gap-2'):
            ui.chip(f'Engine: {module}', icon='route').props('color=primary text-color=white')
            ui.chip(f'Status: {status}', icon='info').props('outline color=primary')

        with ui.card().classes('mm-card w-full shadow-none p-5'):

            section('Answer')

            if details.get('latex'):
                math(details['latex'])
            elif result.get('answer'):
                rich_text(str(result['answer']))
            else:
                error_box(details.get('message') or 'No answer was generated. Check the AI model in the top bar.')

        if module == 'agent':
            for key, title, icon in AGENT_STEPS:
                if details.get(key):
                    with ui.expansion(title, icon=icon, value=(key == 'explanation')) \
                            .classes('w-full mm-card bg-white'):
                        rich_text(str(details[key]))

        if module == 'rag':
            for index, source in enumerate(details.get('sources', []), start=1):
                with ui.expansion(f"Source {index}: {source.get('source', '?')} (page {source.get('page_number', '?')})",
                                  icon='description').classes('w-full mm-card bg-white'):
                    ui.label(source.get('content', '')).classes('text-sm whitespace-pre-wrap')
