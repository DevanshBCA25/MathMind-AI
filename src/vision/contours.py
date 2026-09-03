import cv2


def detect_contours(image):

    contours, _ = cv2.findContours(
        image,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    output = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    cv2.drawContours(
        output,
        contours,
        -1,
        (0, 255, 0),
        2,
    )

    return output


def largest_contour(image):

    contours, _ = cv2.findContours(
        image,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    output = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    if contours:

        largest = max(contours, key=cv2.contourArea)

        cv2.drawContours(
            output,
            [largest],
            -1,
            (255, 0, 0),
            3,
        )

    return output