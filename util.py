import numpy as np
import pandas as pd


def sma(price: np.ndarray, period: int) -> np.ndarray:
    return price.rolling(period).mean()
