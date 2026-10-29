import io

from nicegui import events, run, ui
from PIL import Image

from webapp import state
from webapp.layout import frame
from webapp.pages.ask import show_result, solve
from webapp.widgets import error_box

IMAGE_TYPES = '.png,.jpg,.jpeg,.bmp,.webp'


def read_image(data):

    from src.ocr.ocr_engine import extract_text

    return extract_text(Image.open(io.BytesIO(data)).convert('RGB'))


def read_pdf(data):
    """
    Use the PDF's own text when it has some; fall back to OCR for scans.
    """

    import fitz

    with fitz.open(stream=data, filetype='pdf') as document:
        text = '\n\n'.join(page.get_text().strip() for page in document).strip()

    if text:
        return text

    from src.ocr.ocr_engine import extract_text
    from src.ocr.pdf_reader import read_pdf as render_pages

    pages = render_pages(io.BytesIO(data))

    return '\n\n'.join(
        f'--- Page {number} ---\n{text}'
        for number, page in enumerate(pages, start=1)
        if (text := extract_text(page)).strip()
    )


@ui.page('/scan')
def scan_page():

    with frame('/scan', 'Scan & Solve', 'Read a question from a photo or PDF, check the text, then solve it',
               'document_scanner'):

        with ui.row().classes('w-full gap-4 no-wrap items-start'):

            with ui.card().classes('mm-card shadow-none p-5 gap-3 w-96'):

                ui.label('1. Upload a photo or PDF').classes('font-semibold')

                ui.upload(
                    label='Drop a file here or click +',
                    auto_upload=True,
                    max_files=1,
                    on_upload=lambda e: on_upload(e),
                ).props(f'accept={IMAGE_TYPES},.pdf flat bordered color=primary').classes('w-full')

                preview = ui.column().classes('w-full')

                ui.label('Tip: on a phone the + button opens the camera. Crop to just the question '
                         'and use good light.').classes('text-sm text-grey-7')

            with ui.card().classes('mm-card shadow-none p-5 gap-3 flex-1'):

                ui.label('2. Check the text and solve').classes('font-semibold')

                question = ui.textarea('Extracted text', placeholder='The text read from your file appears here. '
                                                                     'You can also type or correct it.') \
                    .props('outlined autogrow').classes('w-full')

                with ui.row().classes('gap-2'):
                    solve_button = ui.button('Solve with MathMind', icon='bolt', on_click=lambda: on_solve()) \
                        .props('unelevated')
                    ui.button('Download text', icon='download',
                              on_click=lambda: ui.download.content(question.value or '', 'scanned_text.txt')) \
                        .props('flat')

        result_area = ui.column().classes('w-full gap-3')

        async def on_upload(event: events.UploadEventArguments):

            name = (event.file.name or '').lower()
            data = await event.file.read()

            preview.clear()
            with preview:
                if not name.endswith('.pdf'):
                    ui.image(Image.open(io.BytesIO(data))).classes('w-full rounded-lg')
                else:
                    ui.chip(event.file.name, icon='picture_as_pdf').props('outline color=primary')

            notice = ui.notification('Reading text (the first scan downloads the OCR model)...',
                                     spinner=True, timeout=None)
            try:
                text = await run.io_bound(read_pdf if name.endswith('.pdf') else read_image, data)
            except Exception as error:
                ui.notify(f'Could not read this file: {error}', type='negative', multi_line=True)
                return
            finally:
                notice.dismiss()

            if not text.strip():
                ui.notify('No text found. Try a clearer or closer photo.', type='warning')
                return

            question.set_value(text)
            state.add_history('Scan & Solve', 'OCR', event.file.name, text[:120])

        async def on_solve():

            text = (question.value or '').strip()
            result_area.clear()

            if not text:
                with result_area:
                    error_box('Upload a file or type the question first.')
                return

            solve_button.props('loading')
            documents = state.get_documents()

            try:
                result = await run.io_bound(solve, text, 'Automatic', state.get_provider(),
                                            documents['db'] if documents else None)
            finally:
                solve_button.props(remove='loading')

            show_result(result_area, result, text)
