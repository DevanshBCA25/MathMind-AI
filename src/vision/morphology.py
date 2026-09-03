import cv2
import numpy as np


def erosion(image):

    kernel = np.ones((3, 3), np.uint8)

    return cv2.erode(image, kernel, iterations=1)


def dilation(image):

    kernel = np.ones((3, 3), np.uint8)

    return cv2.dilate(image, kernel, iterations=1)


def opening(image):

    kernel = np.ones((3, 3), np.uint8)

    return cv2.morphologyEx(
        image,
        cv2.MORPH_OPEN,
        kernel,
    )


def closing(image):

    kernel = np.ones((3, 3), np.uint8)

    return cv2.morphologyEx(
        image,
        cv2.MORPH_CLOSE,
        kernel,
    )