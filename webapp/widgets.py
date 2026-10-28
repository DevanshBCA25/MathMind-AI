"""
Small reusable UI pieces.
"""

from nicegui import ui


def math(latex, block=True):
    """
    Render LaTeX as MathML. Falls back to showing the source if the
    expression is too exotic for the converter.
    """

    try:
        from latex2mathml.converter import convert

        mathml = convert(latex, display='block' if block else 'inline')

    except Exception:
        return ui.code(latex).classes('w-full')

    if block:
        return ui.html(mathml).classes('w-full text-center overflow-x-auto')

    return ui.html(mathml, tag='span')


def rich_text(text):
    """
    Markdown that also renders $...$ maths, for AI answers.
    """

    try:
        return ui.markdown(text, extras=['fenced-code-blocks', 'tables', 'latex'])
    except Exception:
        return ui.markdown(text)


def section(title):

    return ui.label(title).classes('text-lg font-semibold text-indigo-10 mt-2')


def error_box(message):

    with ui.row().classes('w-full items-center gap-2 bg-red-1 text-red-9 rounded-lg px-4 py-3'):
        ui.icon('error_outline')
        ui.label(str(message))


def success_box(message):

    with ui.row().classes('w-full items-center gap-2 bg-green-1 text-green-9 rounded-lg px-4 py-3'):
        ui.icon('check_circle')
        ui.label(str(message))
