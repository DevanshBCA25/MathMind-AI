import tempfile
from pathlib import Path

from nicegui import events, run, ui

from webapp import state
from webapp.layout import frame
from webapp.widgets import error_box, rich_text, section, success_box

SAMPLE_DIR = Path(__file__).resolve().parents[2] / 'data' / 'documents'


def ask_documents(vector_db, provider, question, method, top_k):

    from src.rag.pipeline import RAGPipeline

    pipeline = RAGPipeline(
        vector_db=vector_db,
        provider=provider,
        retrieval_method=method,
        top_k=top_k,
    )

    return pipeline.ask(question)


@ui.page('/documents')
def documents_page():

    uploaded = {}

    with frame('/documents', 'Document Q&A', 'Upload PDFs and ask questions about them', 'menu_book'):

        status = ui.column().classes('w-full')

        @ui.refreshable
        def show_status():

            loaded = state.get_documents()

            if loaded:
                success_box(f"Ready: {', '.join(loaded['names'])}. Ask below, or use RAG mode on Ask MathMind.")
            else:
                ui.label('No documents loaded yet.').classes('text-grey-7')

        with status:
            show_status()

        with ui.card().classes('mm-card w-full shadow-none p-5 gap-3'):

            section('1. Add PDFs')

            file_list = ui.label('').classes('text-sm text-grey-8')

            async def on_upload(event: events.UploadEventArguments):
                uploaded[event.file.name] = await event.file.read()
                file_list.set_text('Selected: ' + ', '.join(uploaded))

            ui.upload(
                label='Drop PDFs here or click +',
                multiple=True,
                auto_upload=True,
                on_upload=on_upload,
            ).props('accept=.pdf flat bordered color=primary').classes('w-full')

            use_samples = ui.checkbox('Also include the sample maths PDFs', value=not uploaded)

            async def build():

                with tempfile.TemporaryDirectory() as folder:

                    paths = []

                    for name, data in uploaded.items():
                        path = Path(folder) / Path(name).name
                        path.write_bytes(data)
                        paths.append(path)

                    if use_samples.value:
                        paths.extend(sorted(SAMPLE_DIR.glob('*.pdf')))

                    if not paths:
                        ui.notify('Upload a PDF or tick the sample PDFs.', type='warning')
                        return

                    build_button.props('loading')
                    notice = ui.notification('Reading PDFs and building the search index (first run downloads a model)...',
                                             spinner=True, timeout=None)

                    try:
                        from src.rag.builder import build_vector_database
                        vector_db, report = await run.io_bound(build_vector_database, paths)
                    except Exception as error:
                        ui.notify(f'Could not build the search index: {error}', type='negative', multi_line=True)
                        return
                    finally:
                        notice.dismiss()
                        build_button.props(remove='loading')

                for problem in report['problems']:
                    ui.notify(problem, type='warning')

                if vector_db is None:
                    ui.notify('No text could be read from these PDFs.', type='negative')
                    return

                state.set_documents(vector_db, [Path(p).name for p in paths])
                ui.notify(f"Indexed {report['files']} PDF(s) into {report['chunks']} chunks.", type='positive')
                show_status.refresh()

            build_button = ui.button('Build search index', icon='construction', on_click=build).props('unelevated')

        with ui.card().classes('mm-card w-full shadow-none p-5 gap-3'):

            section('2. Ask a question')

            question = ui.input('Question', placeholder='e.g. What is the Pythagorean theorem according to the document?') \
                .props('outlined').classes('w-full')

            with ui.row().classes('items-center gap-6'):
                method = ui.toggle({'similarity': 'Similarity', 'mmr': 'MMR (diverse)'}, value='similarity') \
                    .props('no-caps unelevated toggle-color=primary')
                with ui.row().classes('items-center gap-2'):
                    ui.label('Chunks:')
                    top_k = ui.slider(min=1, max=10, value=4).props('label-always').classes('w-40')

            answer_area = ui.column().classes('w-full gap-2')

            async def ask():

                loaded = state.get_documents()
                text = (question.value or '').strip()

                if not loaded:
                    ui.notify('Build the search index first.', type='warning')
                    return

                if not text:
                    ui.notify('Type a question.', type='warning')
                    return

                ask_button.props('loading')

                try:
                    result = await run.io_bound(
                        ask_documents, loaded['db'], state.get_provider(), text, method.value, int(top_k.value),
                    )
                finally:
                    ask_button.props(remove='loading')

                answer_area.clear()

                with answer_area:

                    if result.get('answer'):
                        rich_text(result['answer'])
                        state.add_history('Document Q&A', method.value, text, result['answer'])
                    else:
                        error_box(result.get('message') or result.get('status'))

                    for index, source in enumerate(result.get('sources', []), start=1):
                        with ui.expansion(f"Source {index}: {source.get('source')} · page {source.get('page_number', '?')}",
                                          icon='description').classes('w-full mm-card bg-white'):
                            ui.label(source.get('content', '')).classes('text-sm whitespace-pre-wrap')

            ask_button = ui.button('Ask', icon='send', on_click=ask).props('unelevated')
