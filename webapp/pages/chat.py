from nicegui import app, run, ui

from webapp import state
from webapp.layout import frame
from webapp.widgets import rich_text

EXAMPLES = [
    'Explain the quadratic formula with an example',
    'What is the derivative of x² sin(x)? Show steps',
    'Why is 0.999... equal to 1?',
]


def ask_model(provider, messages):

    from src.llm.router import LLMRouter
    from src.llm.prompts import build_chat_prompt

    return LLMRouter().ask(provider, build_chat_prompt(messages)).strip()


@ui.page('/chat')
def chat_page():

    messages = app.storage.user.setdefault('chat', [])

    with frame('/chat', 'AI Tutor Chat', 'Ask anything, get step-by-step explanations', 'chat'):

        provider_label = ui.label().classes('text-grey-8')

        def update_provider_label():
            provider_label.set_text(f'Answering with {state.get_provider()}. Change the model in the top bar.')

        update_provider_label()
        ui.timer(1.0, update_provider_label)

        @ui.refreshable
        def conversation():

            if not messages:
                with ui.column().classes('w-full items-center py-8 gap-3'):
                    ui.icon('forum', size='3rem', color='primary')
                    ui.label('Try one of these').classes('text-grey-8')
                    with ui.row().classes('gap-2 justify-center'):
                        for example in EXAMPLES:
                            ui.chip(example, icon='lightbulb', on_click=lambda e=example: send(e)) \
                                .props('outline color=primary clickable')
                return

            for message in messages:
                is_user = message['role'] == 'user'
                with ui.chat_message(
                    name='You' if is_user else 'MathMind',
                    sent=is_user,
                    avatar=None,
                ).classes('w-full'):
                    rich_text(message['content'])

        with ui.card().classes('mm-card w-full shadow-none p-4'):
            conversation()
            thinking = ui.row().classes('items-center gap-2 text-grey-7')
            with thinking:
                ui.spinner(size='sm')
                ui.label('Thinking...')
            thinking.visible = False

        async def send(text=None):

            text = (text or box.value or '').strip()

            if not text:
                return

            box.set_value('')
            messages.append({'role': 'user', 'content': text})
            conversation.refresh()
            thinking.visible = True

            try:
                answer = await run.io_bound(ask_model, state.get_provider(), list(messages))
                messages.append({'role': 'assistant', 'content': answer})
                state.add_history('AI Chat', state.get_provider(), text, 'answered')

            except Exception as error:
                messages.pop()
                ui.notify(str(error), type='negative', multi_line=True)

            finally:
                thinking.visible = False
                app.storage.user['chat'] = messages
                conversation.refresh()

        with ui.row().classes('w-full items-center no-wrap gap-2'):
            box = ui.input(placeholder='Ask a maths question...') \
                .props('outlined rounded').classes('flex-grow') \
                .on('keydown.enter', lambda: send())
            ui.button(icon='send', on_click=lambda: send()).props('round unelevated')

        def clear():
            messages.clear()
            app.storage.user['chat'] = messages
            conversation.refresh()

        def export():
            text = '\n\n'.join(f"{m['role']}:\n{m['content']}" for m in messages)
            ui.download.content(text, 'chat_history.txt')

        with ui.row().classes('gap-2'):
            ui.button('Clear chat', icon='delete', on_click=clear).props('flat color=grey-8')
            ui.button('Export chat', icon='download', on_click=export).props('flat')
