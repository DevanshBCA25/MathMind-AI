from nicegui import ui
from sympy import latex

from src.calculator.scientific import evaluate_expression
from webapp import state
from webapp.layout import frame
from webapp.widgets import math

BASIC_KEYS = [
    ['C', '(', ')', '÷'],
    ['7', '8', '9', '×'],
    ['4', '5', '6', '-'],
    ['1', '2', '3', '+'],
    ['%', '0', '.', '⌫'],
]

SCIENTIFIC_KEYS = [
    ['sin', 'cos', 'tan', 'π', 'C'],
    ['asin', 'acos', 'atan', 'e', '⌫'],
    ['√', 'x²', '^', '!', '÷'],
    ['ln', '7', '8', '9', '×'],
    ['log', '4', '5', '6', '-'],
    ['(', '1', '2', '3', '+'],
    [')', '%', '0', '.', 'Ans'],
]

FUNCTION_KEYS = {'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'ln', 'log', '√'}
OPERATOR_KEYS = {'÷', '×', '-', '+', '^'}


def keypad_calculator(module, keys, scientific):
    """
    A calculator with a display and on-screen keys. The display can also
    be typed into directly; Enter or = calculates.
    """

    memory = {'answer': None}

    with ui.card().classes('mm-card shadow-none p-5 w-full max-w-xl self-center gap-3'):

        degrees = None
        if scientific:
            degrees = ui.toggle({'deg': 'Degrees', 'rad': 'Radians'}, value='deg') \
                .props('no-caps unelevated dense toggle-color=primary')

        display = ui.input(placeholder='Type or tap, e.g. 2(3+4)^2') \
            .props('outlined input-class="text-right text-2xl"').classes('w-full')
        result_area = ui.column().classes('w-full items-end gap-0 min-h-[4.5rem]')

        def press(key):

            text = display.value or ''

            if key == 'C':
                display.set_value('')
                result_area.clear()
            elif key == '⌫':
                display.set_value(text[:-1])
            elif key == 'x²':
                display.set_value(text + '^2')
            elif key == 'Ans':
                if memory['answer'] is not None:
                    display.set_value(text + f'({memory["answer"]})')
            elif key in FUNCTION_KEYS:
                display.set_value(text + key + '(')
            else:
                display.set_value(text + key)

            display.run_method('focus')

        def calculate():

            text = (display.value or '').strip()
            if not text:
                return

            result_area.clear()

            try:
                exact, decimal = evaluate_expression(text, degrees=bool(degrees and degrees.value == 'deg'))
            except Exception as error:
                with result_area:
                    ui.label(str(error)).classes('text-negative')
                return

            shown = f'{decimal:.10g}' if isinstance(decimal, float) else str(decimal)
            memory['answer'] = str(exact)

            with result_area:
                ui.label(f'{text} =').classes('text-grey-7')
                ui.label(shown).classes('text-4xl font-bold text-indigo-10')
                if not exact.is_Integer and latex(exact) != shown:
                    with ui.row().classes('items-center gap-1 text-grey-8'):
                        ui.label('Exact:')
                        math(latex(exact), block=False)

            state.add_history(module, 'Calculate', text, shown)

        display.on('keydown.enter', calculate)

        with ui.grid(columns=len(keys[0])).classes('w-full gap-2'):
            for row in keys:
                for key in row:
                    if key in OPERATOR_KEYS:
                        props = 'unelevated color=indigo-1 text-color=indigo-10'
                    elif key in ('C', '⌫'):
                        props = 'unelevated color=pink-1 text-color=pink-10'
                    elif key.isdigit() or key == '.':
                        props = 'unelevated color=white text-color=grey-10'
                    else:
                        props = 'unelevated color=deep-purple-1 text-color=deep-purple-10'
                    ui.button(key, on_click=lambda k=key: press(k)) \
                        .props(f'{props} no-caps').classes('text-lg h-12 border')

        ui.button('=', on_click=calculate).props('unelevated size=lg').classes('w-full text-xl')


@ui.page('/basic')
def basic_page():

    with frame('/basic', 'Basic Calculator', 'Tap the keys or type a whole calculation like 12 × (3 + 4)', 'calculate'):
        keypad_calculator('Basic Calculator', BASIC_KEYS, scientific=False)


@ui.page('/scientific')
def scientific_page():

    with frame('/scientific', 'Scientific Calculator',
               'Trigonometry, logs, roots, powers and factorials with exact answers', 'science'):
        keypad_calculator('Scientific Calculator', SCIENTIFIC_KEYS, scientific=True)
        ui.label('Tip: answers are shown exactly too, e.g. √8 = 2√2 and sin 60° = √3/2.') \
            .classes('text-grey-7 self-center')
