import cv2


def gray(image):

    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY,
    )


def binary(image):

    gray_image = gray(image)

    _, thresh = cv2.threshold(
        gray_image,
        150,
        255,
        cv2.THRESH_BINARY,
    )

    return thresh


def adaptive(image):

    gray_image = gray(image)

    return cv2.adaptiveThreshold(
        gray_image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2,
    )


def denoise(image):

    return cv2.fastNlMeansDenoisingColored(
        image,
        None,
        10,
        10,
        7,
        21,
    )