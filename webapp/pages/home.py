from nicegui import ui

from webapp.layout import frame

FEATURES = [
    ('psychology', 'Ask MathMind', '/ask',
     'Type any question. It picks the calculator, algebra engine or AI agents for you.'),
    ('chat', 'AI Tutor Chat', '/chat',
     'A maths tutor that explains every step and remembers the conversation.'),
    ('menu_book', 'Document Q&A', '/documents',
     'Upload your notes or textbook PDF and ask questions about it (RAG).'),
    ('functions', 'Algebra & Calculus', '/algebra',
     'Answers in proper maths notation, verified with SymPy, explained by AI.'),
    ('track_changes', 'Practice Mode', '/practice',
     'Endless practice questions with instant checking and a score.'),
    ('show_chart', 'Graph Plotter', '/graph',
     'Interactive graphs with zoom, hover and derivative curves.'),
    ('document_scanner', 'Scan & Solve', '/scan',
     'Take a photo of a question, read it with OCR and solve it.'),
    ('bar_chart', 'Statistics', '/statistics',
     'Mean, median, variance, quartiles, z-scores and charts.'),
    ('image', 'Image Lab', '/image-lab',
     'Filters, edge detection, thresholds and contours with OpenCV.'),
]

BADGES = ['SymPy', 'Multi-agent reasoning', 'RAG over PDFs', 'OCR', 'OpenCV', 'Gemini · Groq · OpenAI']


@ui.page('/')
def home():

    with frame('/'):

        with ui.column().classes('mm-hero w-full px-8 py-10 gap-3'):
            ui.label('🧠 MathMind AI').classes('text-3xl sm:text-4xl font-bold')
            ui.label(
                'Your AI maths companion: solve, explain and visualise problems from basic '
                'arithmetic to calculus, matrices, statistics and your own study material.'
            ).classes('text-lg opacity-90 max-w-3xl')
            with ui.row().classes('gap-2 mt-2'):
                for badge in BADGES:
                    ui.chip(badge).props('outline color=white text-color=white dense')
            with ui.row().classes('gap-3 mt-4'):
                ui.button('Ask a question', icon='psychology', on_click=lambda: ui.navigate.to('/ask')) \
                    .props('unelevated color=white text-color=primary')
                ui.button('Start practising', icon='track_changes', on_click=lambda: ui.navigate.to('/practice')) \
                    .props('outline color=white')

        ui.label('What would you like to do?').classes('text-2xl font-bold text-indigo-10 mt-4')

        with ui.grid().classes('w-full gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3'):
            for icon, title, path, text in FEATURES:
                with ui.card().classes('mm-card cursor-pointer p-5 gap-2 shadow-none') \
                        .on('click', lambda p=path: ui.navigate.to(p)):
                    ui.icon(icon, size='2rem', color='primary')
                    ui.label(title).classes('text-lg font-semibold')
                    ui.label(text).classes('text-sm text-grey-8')
                    ui.label('Open →').classes('text-primary text-sm font-medium mt-auto')

        ui.label('How it works').classes('text-2xl font-bold text-indigo-10 mt-4')

        with ui.row().classes('w-full gap-4'):
            for number, title, text in [
                ('1', 'You ask', 'Type, chat, upload a PDF or scan a photo.'),
                ('2', 'It routes', 'Arithmetic, algebra, documents or reasoning?'),
                ('3', 'It solves', 'Exact maths with SymPy, or AI agents.'),
                ('4', 'It verifies & teaches', 'Answers are checked, then explained step by step.'),
            ]:
                with ui.card().classes('mm-card shadow-none flex-1 min-w-[200px] p-4'):
                    with ui.avatar(color='primary', text_color='white', size='md'):
                        ui.label(number).classes('text-base font-bold')
                    ui.label(title).classes('font-semibold mt-2')
                    ui.label(text).classes('text-sm text-grey-8')
