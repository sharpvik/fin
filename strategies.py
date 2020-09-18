import numpy as np
import pandas as pd

from . import util


def passive(data: pd.DataFrame) -> np.ndarray:
    """ Imitates passive investment strategy for the whole data duration. """
    return np.ones(len(data['Price']), dtype=int)


def sma(data: pd.DataFrame) -> np.ndarray:
    """ Uses simple moving averages to generate positions. """
    short: int = 50
    long: int = 200
    sma1 = util.sma(data['Price'], short)
    sma2 = util.sma(data['Price'], long)
    return np.where(sma1 > sma2, 1, -1)


def momentum(data: pd.DataFrame) -> np.ndarray:
    """ Uses momentum based signals to generate positions. """
    length: int = 10
    return np.sign(data['Price'].rolling(length).mean())


def mean_reverse(data: pd.DataFrame) -> np.ndarray:
    """ Uses mean reversion to generate positions. """
    period: int = 25
    threshold: float = 3.5
    sma: np.ndarray = util.sma(data['Price'], period)
    distance: np.ndarray = data['Price'] - sma
    return np.where(distance > threshold, -1, 1)
