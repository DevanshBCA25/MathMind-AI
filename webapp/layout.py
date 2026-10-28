"""
Shared page frame: header, navigation drawer, page title banner.
"""

from contextlib import contextmanager

from nicegui import ui

from webapp import state

BRAND = '#4f46e5'

NAVIGATION = [
    ('', [
        ('Home', 'home', '/'),
    ]),
    ('AI Solver', [
        ('Ask MathMind', 'psychology', '/ask'),
        ('AI Tutor Chat', 'chat', '/chat'),
        ('Document Q&A', 'menu_book', '/documents'),
    ]),
    ('Learn', [
        ('Practice Mode', 'track_changes', '/practice'),
    ]),
    ('Calculators', [
        ('Basic Calculator', 'calculate', '/basic'),
        ('Scientific Calculator', 'science', '/scientific'),
        ('Algebra & Calculus', 'functions', '/algebra'),
        ('Graph Plotter', 'show_chart', '/graph'),
        ('Matrices', 'grid_on', '/matrices'),
        ('Linear Algebra', 'view_module', '/linear-algebra'),
        ('Statistics', 'bar_chart', '/statistics'),
    ]),
    ('Vision', [
        ('Scan & Solve', 'document_scanner', '/scan'),
        ('Image Lab', 'image', '/image-lab'),
    ]),
    ('Insights', [
        ('My History', 'history', '/history'),
        ('AI Provider Status', 'monitor_heart', '/status'),
    ]),
]

CSS = '''
.mm-banner {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 55%, #db2777 100%);
    color: white;
    border-radius: 16px;
}
.mm-hero {
    background:
        radial-gradient(circle at 85% 20%, rgba(255,255,255,.18), transparent 40%),
        linear-gradient(135deg, #312e81 0%, #4f46e5 45%, #7c3aed 100%);
    color: white;
    border-radius: 22px;
}
.mm-card { border: 1px solid rgba(79,70,229,.15); border-radius: 16px; }
.mm-card:hover { box-shadow: 0 8px 24px rgba(79,70,229,.15); }
math[display="block"] { font-size: 1.35em; margin: .4em 0; }
.nicegui-markdown math { font-size: 1.1em; }
mtd { padding: .25em .6em; }
mtable { margin: .3em .2em; border-left: 2px solid currentColor; border-right: 2px solid currentColor; border-radius: 5px; }
.q-drawer .q-item.mm-active { background: rgba(79,70,229,.12); color: #4f46e5; font-weight: 600; }
'''


def _navigation(current):

    with ui.list().props('dense padding').classes('w-full'):

        for group, items in NAVIGATION:

            if group:
                ui.item_label(group).props('header').classes('text-xs uppercase text-grey-7 q-mt-sm')

            for title, icon, path in items:

                with ui.item(on_click=lambda p=path: ui.navigate.to(p)) \
                        .props('clickable') \
                        .classes('rounded-lg mx-2' + (' mm-active' if path == current else '')):
                    with ui.item_section().props('avatar'):
                        ui.icon(icon, size='sm')
                    with ui.item_section():
                        ui.item_label(title)


def _provider_select():

    def changed(event):
        state.set_provider(event.value)
        ui.notify(f'AI model: {event.value}')

    ui.select(
        state.provider_options(),
        value=state.get_provider(),
        on_change=changed,
    ).props('dense outlined dark options-dense').classes('w-36 sm:w-44').tooltip('AI model used by the AI pages')


@contextmanager
def frame(current, title=None, subtitle='', icon='functions'):
    """
    Wrap a page: header with menu and model selector, navigation
    drawer, and an optional gradient banner with the page title.
    """

    ui.colors(primary=BRAND, secondary='#7c3aed', accent='#db2777')
    ui.add_css(CSS)
    ui.query('body').classes('bg-[#fafaff]')
    ui.page_title(f'{title} · MathMind AI' if title else 'MathMind AI')

    with ui.header(elevated=False).classes('items-center no-wrap bg-white text-indigo-10 border-b px-4 py-2'):
        ui.button(icon='menu', on_click=lambda: drawer.toggle()).props('flat round color=primary')
        with ui.link(target='/').classes('no-underline text-inherit flex flex-nowrap items-center gap-2 whitespace-nowrap'):
            ui.label('🧠').classes('text-2xl')
            ui.label('MathMind AI').classes('text-lg font-bold text-indigo-10')
        ui.space()
        with ui.element('div').classes('bg-primary rounded-lg'):
            _provider_select()

    with ui.left_drawer(bordered=True).classes('bg-[#f4f3ff] p-0') as drawer:
        _navigation(current)

    with ui.column().classes('w-full max-w-6xl mx-auto p-4 gap-4'):

        if title:
            with ui.row().classes('mm-banner w-full items-center gap-4 px-6 py-4 no-wrap'):
                ui.icon(icon, size='2.2rem')
                with ui.column().classes('gap-0'):
                    ui.label(title).classes('text-2xl font-bold')
                    if subtitle:
                        ui.label(subtitle).classes('opacity-90')

        yield
