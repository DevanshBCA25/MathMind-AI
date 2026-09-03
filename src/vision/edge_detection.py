import cv2


def canny(image):

    return cv2.Canny(
        image,
        100,
        200,
    )


def sobel(image):

    return cv2.Sobel(
        image,
        cv2.CV_64F,
        1,
        1,
        ksize=3,
    )


def laplacian(image):

    return cv2.Laplacian(
        image,
        cv2.CV_64F,
    )