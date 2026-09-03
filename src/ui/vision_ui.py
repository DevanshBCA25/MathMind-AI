import streamlit as st
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

from src.vision.image_processing import (
    read_image,
    convert_rgb,
    convert_gray,
    resize_image,
    rotate_image,
    flip_horizontal,
    flip_vertical,
)

from src.vision.preprocessing import (
    threshold,
    adaptive_threshold,
    otsu_threshold,
)

from src.vision.filters import (
    gaussian_blur,
    median_blur,
    bilateral_filter,
)

from src.vision.edge_detection import (
    canny,
    sobel,
    laplacian,
)

from src.vision.morphology import (
    erosion,
    dilation,
    opening,
    closing,
)

from src.vision.contours import (
    detect_contours,
    largest_contour,
)

from src.vision.histogram import (
    gray_histogram,
    rgb_histogram,
)

from src.utils.helpers import (
    save_operation,
    log_error,
)


def show():

    st.title("🖼️ Computer Vision")

    uploaded_file = st.file_uploader(
        "Upload Image",
        type=["png", "jpg", "jpeg", "bmp"],
    )

    if uploaded_file is None:
        st.info("Upload an image to continue.")
        return

    image = read_image(uploaded_file)

    image = resize_image(image)

    operation = st.selectbox(
        "Select Operation",
        [
            "Original",
            "RGB",
            "Grayscale",
            "Gaussian Blur",
            "Median Blur",
            "Bilateral Filter",
            "Binary Threshold",
            "Adaptive Threshold",
            "Otsu Threshold",
            "Canny Edge",
            "Sobel Edge",
            "Laplacian Edge",
            "Rotate 90°",
            "Flip Horizontal",
            "Flip Vertical",
            "Erosion",
            "Dilation",
            "Opening",
            "Closing",
            "Detect Contours",
            "Largest Contour",
            "Gray Histogram",
            "RGB Histogram",
        ],
    )

    output = image.copy()

    try:

        if operation == "Original":

            output = image

        elif operation == "RGB":

            output = convert_rgb(image)

        elif operation == "Grayscale":

            output = convert_gray(image)

        elif operation == "Gaussian Blur":

            gray = convert_gray(image)

            output = gaussian_blur(gray)

        elif operation == "Median Blur":

            gray = convert_gray(image)

            output = median_blur(gray)

        elif operation == "Bilateral Filter":

            gray = convert_gray(image)

            output = bilateral_filter(gray)

        elif operation == "Binary Threshold":

            gray = convert_gray(image)

            output = threshold(gray)

        elif operation == "Adaptive Threshold":

            gray = convert_gray(image)

            output = adaptive_threshold(gray)

        elif operation == "Otsu Threshold":

            gray = convert_gray(image)

            output = otsu_threshold(gray)

        elif operation == "Canny Edge":

            gray = convert_gray(image)

            output = canny(gray)

        elif operation == "Sobel Edge":

            gray = convert_gray(image)

            output = sobel(gray)

        elif operation == "Laplacian Edge":

            gray = convert_gray(image)

            output = laplacian(gray)

        elif operation == "Rotate 90°":

            output = rotate_image(image, 90)

        elif operation == "Flip Horizontal":

            output = flip_horizontal(image)

        elif operation == "Flip Vertical":

            output = flip_vertical(image)

        elif operation == "Erosion":

            gray = convert_gray(image)

            output = erosion(gray)

        elif operation == "Dilation":

            gray = convert_gray(image)

            output = dilation(gray)

        elif operation == "Opening":

            gray = convert_gray(image)

            output = opening(gray)

        elif operation == "Closing":

            gray = convert_gray(image)

            output = closing(gray)

        elif operation == "Detect Contours":

            gray = convert_gray(image)

            binary = threshold(gray)

            output = detect_contours(binary)

        elif operation == "Largest Contour":

            gray = convert_gray(image)

            binary = threshold(gray)

            output = largest_contour(binary)

        elif operation == "Gray Histogram":

            gray = convert_gray(image)

            fig = gray_histogram(gray)

            st.pyplot(fig)

            output = gray

        elif operation == "RGB Histogram":

            fig = rgb_histogram(image)

            st.pyplot(fig)

            output = image
        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Original Image")

            st.image(
                convert_rgb(image),
                use_container_width=True,
            )

        with col2:

            st.subheader("Processed Image")

            if len(output.shape) == 2:

                st.image(
                    output,
                    clamp=True,
                    use_container_width=True,
                )

            else:

                st.image(
                    convert_rgb(output),
                    use_container_width=True,
                )

        save_operation(
            module="Computer Vision",
            operation=operation,
            input_data=uploaded_file.name,
            result="Success",
        )

        st.divider()

        if len(output.shape) == 2:

            download_image = Image.fromarray(output)

        else:

            download_image = Image.fromarray(
                convert_rgb(output)
            )

        buffer = BytesIO()

        download_image.save(
            buffer,
            format="PNG",
        )

        st.download_button(
            label="📥 Download Processed Image",
            data=buffer.getvalue(),
            file_name="processed_image.png",
            mime="image/png",
        )

    except Exception as e:

        log_error(str(e))

        st.error(f"Error : {e}")