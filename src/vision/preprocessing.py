import cv2


def threshold(image):
    _, thresh = cv2.threshold(
        image,
        127,
        255,
        cv2.THRESH_BINARY,
    )
    return thresh


def adaptive_threshold(image):

    return cv2.adaptiveThreshold(
        image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2,
    )


def otsu_threshold(image):

    _, thresh = cv2.threshold(
        image,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )

    return thresh