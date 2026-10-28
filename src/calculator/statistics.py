import re
import statistics
import numpy as np
import pandas as pd


def get_numbers(data):

    parts = [i for i in re.split(r"[,\s]+", data.strip()) if i]

    try:
        numbers = [float(i) for i in parts]
    except ValueError as error:
        raise ValueError(
            "Please enter only numbers, separated by commas or spaces."
        ) from error

    if not numbers:
        raise ValueError("Please enter at least one number.")

    return numbers


def mean(data):
    return statistics.mean(get_numbers(data))


def median(data):
    return statistics.median(get_numbers(data))


def mode(data):

    numbers = get_numbers(data)

    modes = statistics.multimode(numbers)

    if len(modes) == len(set(numbers)) and len(set(numbers)) > 1:
        return "No mode (every value appears equally often)"

    return modes[0] if len(modes) == 1 else modes


def variance(data):

    numbers = get_numbers(data)

    if len(numbers) < 2:
        raise ValueError("Variance needs at least two numbers.")

    return statistics.variance(numbers)


def standard_deviation(data):

    numbers = get_numbers(data)

    if len(numbers) < 2:
        raise ValueError("Standard deviation needs at least two numbers.")

    return statistics.stdev(numbers)


def minimum(data):
    return min(get_numbers(data))


def maximum(data):
    return max(get_numbers(data))


def data_range(data):
    numbers = get_numbers(data)
    return max(numbers) - min(numbers)


def quartiles(data):

    numbers = np.array(get_numbers(data))

    return np.percentile(numbers, [25, 50, 75])


def percentile(data, p):

    numbers = np.array(get_numbers(data))

    return np.percentile(numbers, p)


def iqr(data):

    q1, _, q3 = quartiles(data)

    return q3 - q1


def z_score(data):

    numbers = np.array(get_numbers(data))

    return (numbers - numbers.mean()) / numbers.std()


def normalize(data):

    numbers = np.array(get_numbers(data))

    return (numbers - numbers.min()) / (
        numbers.max() - numbers.min()
    )


def standardize(data):

    numbers = np.array(get_numbers(data))

    return (numbers - numbers.mean()) / numbers.std()


def correlation(data1, data2):

    x = get_numbers(data1)

    y = get_numbers(data2)

    return np.corrcoef(x, y)[0][1]


def covariance(data1, data2):

    x = get_numbers(data1)

    y = get_numbers(data2)

    return np.cov(x, y)[0][1]


def dataframe(data):

    numbers = get_numbers(data)

    return pd.DataFrame({"Numbers": numbers})