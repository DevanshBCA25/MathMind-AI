from nicegui import app, ui

from src.calculator.practice import LEVELS, TOPICS, check, generate
from webapp import state
from webapp.layout import frame
from webapp.widgets import math


@ui.page('/practice')
def practice_page():

    score = app.storage.user.setdefault('practice_score', {'correct': 0, 'attempted': 0})
    current = {'question': None, 'answered': False}

    with frame('/practice', 'Practice Mode', 'Unlimited questions, checked instantly. No AI key needed.', 'track_changes'):

        with ui.row().classes('w-full items-center gap-4'):
            topic = ui.select(TOPICS, value=TOPICS[0], label='Topic').props('outlined').classes('w-64')
            level = ui.toggle(LEVELS, value='Easy').props('no-caps unelevated toggle-color=primary')

        with ui.row().classes('w-full gap-4'):
            for key, title, icon in [('correct', 'Correct', 'check_circle'), ('attempted', 'Attempted', 'edit_note')]:
                with ui.card().classes('mm-card shadow-none flex-1 p-4'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon(icon, color='primary')
                        ui.label(title).classes('text-grey-8')
                    ui.label().classes('text-3xl font-bold').bind_text_from(score, key, backward=str)
            with ui.card().classes('mm-card shadow-none flex-1 p-4'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('insights', color='primary')
                    ui.label('Accuracy').classes('text-grey-8')
                ui.label().classes('text-3xl font-bold').bind_text_from(
                    score, 'correct',
                    backward=lambda _: f"{100 * score['correct'] // score['attempted']}%" if score['attempted'] else '–',
                )

        with ui.card().classes('mm-card w-full shadow-none p-6 gap-3'):
            prompt = ui.label().classes('font-semibold text-lg')
            question_view = ui.column().classes('w-full')
            answer = ui.input('Your answer', placeholder='e.g. 3x^2 + 2   or   x = 2, -3') \
                .props('outlined').classes('w-full')
            feedback = ui.column().classes('w-full')

            with ui.row().classes('gap-2'):
                check_button = ui.button('Check answer', icon='done').props('unelevated')
                ui.button('Hint', icon='lightbulb', on_click=lambda: ui.notify(current['question']['hint'])) \
                    .props('outline')
                ui.button('Next question', icon='arrow_forward', on_click=lambda: new_question()).props('flat')

        def new_question():

            current['question'] = generate(topic.value, level.value)
            current['answered'] = False

            prompt.set_text(current['question']['prompt'])
            question_view.clear()
            with question_view:
                math(current['question']['latex'])

            answer.set_value('')
            feedback.clear()

        def on_check():

            question = current['question']

            try:
                correct = check(question, answer.value)
            except Exception as error:
                ui.notify(f'Could not read your answer: {error}', type='warning')
                return

            if not current['answered']:
                score['attempted'] += 1
                score['correct'] += int(correct)
                current['answered'] = True
                app.storage.user['practice_score'] = score
                state.add_history('Practice', question['topic'], question['latex'], 'Correct' if correct else 'Wrong')

            feedback.clear()
            with feedback:
                if correct:
                    with ui.row().classes('items-center gap-2 text-positive text-lg'):
                        ui.icon('celebration')
                        ui.label('Correct! Well done.')
                else:
                    with ui.row().classes('items-center gap-2 text-negative text-lg'):
                        ui.icon('cancel')
                        ui.label('Not quite. The correct answer is:')
                    math(question['answer_latex'])

        check_button.on_click(on_check)
        answer.on('keydown.enter', on_check)
        topic.on_value_change(new_question)
        level.on_value_change(new_question)

        new_question()
