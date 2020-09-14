from typing import Tuple

import numpy as np
import pandas as pd


def passive(data: pd.DataFrame) -> np.ndarray:
    """ Imitates passive investment strategy for the whole data duration. """
    return np.ones(len(data['Price']), dtype=int)


def sma(data: pd.DataFrame) -> np.ndarray:
    """ Uses simple moving averages to determine signals. """
    short: int = 50
    long: int = 200
    data['SMA1'] = data['Price'].rolling(short).mean()
    data['SMA2'] = data['Price'].rolling(long).mean()
    return np.where(data['SMA1'] > data['SMA2'], 1, -1)
