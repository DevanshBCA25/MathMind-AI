import math


def power(a, b):
    try:
        return math.pow(a, b)
    except OverflowError as error:
        raise ValueError("Result is too large to calculate.") from error
    except ValueError as error:
        raise ValueError(
            "Power is not defined for these numbers."
        ) from error


def square_root(a):
    if a < 0:
        raise ValueError("Negative number is not allowed.")
    return math.sqrt(a)


def sine(angle):
    return math.sin(math.radians(angle))


def cosine(angle):
    return math.cos(math.radians(angle))


def tangent(angle):
    if (angle - 90) % 180 == 0:
        raise ValueError(f"tan({angle}°) is undefined.")
    return math.tan(math.radians(angle))