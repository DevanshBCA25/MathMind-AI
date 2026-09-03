import cv2
import matplotlib.pyplot as plt


def gray_histogram(image):

    fig, ax = plt.subplots()

    ax.hist(
        image.ravel(),
        bins=256,
        range=[0, 256],
    )

    ax.set_title("Grayscale Histogram")

    return fig


def rgb_histogram(image):

    fig, ax = plt.subplots()

    colors = ("b", "g", "r")

    for i, color in enumerate(colors):

        hist = cv2.calcHist(
            [image],
            [i],
            None,
            [256],
            [0, 256],
        )

        ax.plot(hist, color=color)

    ax.set_title("RGB Histogram")

    return fig