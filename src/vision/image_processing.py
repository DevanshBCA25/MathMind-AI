import cv2
import numpy as np


def read_image(uploaded_file):
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return image


def convert_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def convert_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def resize_image(image, width=800):
    h, w = image.shape[:2]

    ratio = width / w

    height = int(h * ratio)

    return cv2.resize(image, (width, height))


def rotate_image(image, angle):

    h, w = image.shape[:2]

    center = (w // 2, h // 2)

    matrix = cv2.getRotationMatrix2D(center, angle, 1)

    return cv2.warpAffine(image, matrix, (w, h))


def flip_horizontal(image):
    return cv2.flip(image, 1)


def flip_vertical(image):
    return cv2.flip(image, 0)