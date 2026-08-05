import math


def power(a, b):
    return math.pow(a, b)


def square_root(a):
    if a < 0:
        raise ValueError("Negative number is not allowed.")
    return math.sqrt(a)


def sine(angle):
    return math.sin(math.radians(angle))


def cosine(angle):
    return math.cos(math.radians(angle))


def tangent(angle):
    return math.tan(math.radians(angle))