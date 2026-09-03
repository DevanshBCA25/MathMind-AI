import cv2


def gaussian_blur(image):

    return cv2.GaussianBlur(
        image,
        (5, 5),
        0,
    )


def median_blur(image):

    return cv2.medianBlur(
        image,
        5,
    )


def bilateral_filter(image):

    return cv2.bilateralFilter(
        image,
        9,
        75,
        75,
    )