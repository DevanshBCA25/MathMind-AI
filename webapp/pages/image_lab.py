import io

import cv2
import numpy as np
from nicegui import events, ui
from PIL import Image

from src.vision.contours import detect_contours, largest_contour
from src.vision.edge_detection import canny, laplacian, sobel
from src.vision.filters import bilateral_filter, gaussian_blur, median_blur
from src.vision.histogram import gray_histogram, rgb_histogram
from src.vision.image_processing import convert_gray, convert_rgb, flip_horizontal, flip_vertical, resize_image, rotate_image
from src.vision.morphology import closing, dilation, erosion, opening
from src.vision.preprocessing import adaptive_threshold, otsu_threshold, threshold
from webapp import state
from webapp.layout import frame
from webapp.widgets import error_box

GRAY = convert_gray

OPERATIONS = {
    'Basics': {
        'Grayscale': GRAY,
        'Rotate 90°': lambda i: rotate_image(i, 90),
        'Flip Horizontal': flip_horizontal,
        'Flip Vertical': flip_vertical,
    },
    'Filters': {
        'Gaussian Blur': lambda i: gaussian_blur(GRAY(i)),
        'Median Blur': lambda i: median_blur(GRAY(i)),
        'Bilateral Filter': lambda i: bilateral_filter(GRAY(i)),
    },
    'Thresholds': {
        'Binary Threshold': lambda i: threshold(GRAY(i)),
        'Adaptive Threshold': lambda i: adaptive_threshold(GRAY(i)),
        'Otsu Threshold': lambda i: otsu_threshold(GRAY(i)),
    },
    'Edges': {
        'Canny Edge': lambda i: canny(GRAY(i)),
        'Sobel Edge': lambda i: sobel(GRAY(i)),
        'Laplacian Edge': lambda i: laplacian(GRAY(i)),
    },
    'Morphology': {
        'Erosion': lambda i: erosion(GRAY(i)),
        'Dilation': lambda i: dilation(GRAY(i)),
        'Opening': lambda i: opening(GRAY(i)),
        'Closing': lambda i: closing(GRAY(i)),
    },
    'Shapes': {
        'Detect Contours': lambda i: detect_contours(threshold(GRAY(i))),
        'Largest Contour': lambda i: largest_contour(threshold(GRAY(i))),
    },
}

ALL_OPERATIONS = {name: f for group in OPERATIONS.values() for name, f in group.items()}


def to_pil(image):
    """
    OpenCV arrays (BGR or grayscale, any dtype) to a displayable PIL image.
    """

    if image.dtype != np.uint8:
        image = cv2.convertScaleAbs(image)

    if image.ndim == 2:
        return Image.fromarray(image)

    return Image.fromarray(convert_rgb(image))


def figure_to_pil(figure):

    import matplotlib.pyplot as plt

    buffer = io.BytesIO()
    figure.savefig(buffer, format='png', bbox_inches='tight', dpi=110)
    plt.close(figure)

    return Image.open(buffer)


def sample_image():
    """
    A generated test picture, so the page works before anything is uploaded.
    """

    image = np.full((360, 560, 3), 245, np.uint8)
    cv2.rectangle(image, (40, 50), (230, 300), (229, 70, 79), -1)
    cv2.circle(image, (380, 170), 110, (237, 58, 124), -1)
    cv2.putText(image, 'x^2 + 1', (250, 330), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (60, 30, 30), 3)

    return image


@ui.page('/image-lab')
def image_lab_page():

    current = {'image': sample_image(), 'name': 'sample', 'output': None}

    with frame('/image-lab', 'Image Lab', 'Image processing with OpenCV: filters, edges, thresholds and contours',
               'image'):

        with ui.card().classes('mm-card w-full shadow-none p-5 gap-3'):

            with ui.row().classes('w-full items-center gap-4'):
                ui.upload(label='Upload your own image', auto_upload=True, max_files=1,
                          on_upload=lambda e: on_upload(e)) \
                    .props('accept=.png,.jpg,.jpeg,.bmp,.webp flat bordered color=primary').classes('w-80')
                operation = ui.select(
                    {name: name for name in ALL_OPERATIONS} | {'Gray Histogram': 'Gray Histogram',
                                                               'RGB Histogram': 'RGB Histogram'},
                    value='Canny Edge', label='Operation',
                ).props('outlined').classes('w-64')
                ui.button('Download result', icon='download', on_click=lambda: download()).props('flat')

            with ui.row().classes('gap-1'):
                for group, names in OPERATIONS.items():
                    with ui.button(group, icon='expand_more').props('outline dense no-caps'):
                        with ui.menu():
                            for name in names:
                                ui.menu_item(name, on_click=lambda n=name: operation.set_value(n))

        with ui.row().classes('w-full gap-4 no-wrap'):
            with ui.card().classes('mm-card shadow-none p-3 flex-1 gap-2'):
                ui.label('Original').classes('font-semibold')
                original_view = ui.image().classes('w-full rounded-lg')
            with ui.card().classes('mm-card shadow-none p-3 flex-1 gap-2'):
                result_title = ui.label().classes('font-semibold')
                result_view = ui.image().classes('w-full rounded-lg')

        errors = ui.column().classes('w-full')

        def process():

            image = current['image']
            name = operation.value
            errors.clear()

            try:
                if name == 'Gray Histogram':
                    output = figure_to_pil(gray_histogram(GRAY(image)))
                elif name == 'RGB Histogram':
                    output = figure_to_pil(rgb_histogram(image))
                else:
                    output = to_pil(ALL_OPERATIONS[name](image))
            except Exception as error:
                with errors:
                    error_box(error)
                return

            current['output'] = output
            original_view.set_source(to_pil(image))
            result_view.set_source(output)
            result_title.set_text(name)

            if current['name'] != 'sample':
                state.add_history('Image Lab', name, current['name'], 'Success')

        async def on_upload(event: events.UploadEventArguments):

            data = np.frombuffer(await event.file.read(), np.uint8)
            image = cv2.imdecode(data, cv2.IMREAD_COLOR)

            if image is None:
                ui.notify('This file is not an image I can read.', type='negative')
                return

            current['image'] = resize_image(image) if image.shape[1] > 800 else image
            current['name'] = event.file.name
            process()

        def download():

            if current['output'] is None:
                return

            buffer = io.BytesIO()
            current['output'].save(buffer, format='PNG')
            ui.download.content(buffer.getvalue(), 'processed_image.png')

        operation.on_value_change(process)
        process()
