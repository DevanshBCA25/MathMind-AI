import statistics
import numpy as np
import pandas as pd


def get_numbers(data):

    numbers = [float(i.strip()) for i in data.split(",") if i.strip() != ""]

    return numbers


def mean(data):
    return statistics.mean(get_numbers(data))


def median(data):
    return statistics.median(get_numbers(data))


def mode(data):
    return statistics.mode(get_numbers(data))


def variance(data):
    return statistics.variance(get_numbers(data))


def standard_deviation(data):
    return statistics.stdev(get_numbers(data))


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