from typing import Callable

import numpy as np
import pandas as pd

from . import strategies as sts


class Backtester:
    """
    Backtester receives data series in a DataFrame object and allows you to test
    your trading strategy without having to write too much boilerplate code.
    """

    def __init__(self, data: pd.DataFrame,
                 strategy: Callable, benchmark: Callable = sts.passive) -> None:
        """
        :param data: historic data used by strategy and benchmark.
        :param strategy: returns numpy.array or pandas.core.series.Series
                made of 1(long) and -1(short) position signals for each date.
        :param benchmark: returns numpy.array or pandas.core.series.Series
                made of 1(long) and -1(short) position signals for each date.

        The data DataFrame must contain a column named 'Price' which will be
        used for assessment.
        """
        self.data: pd.DataFrame = data
        self.strategy: Callable = strategy
        self.benchmark: Callable = benchmark
        self.returns: pd.DataFrame = pd.DataFrame(
            columns=['Strategy', 'Benchmark'])

    def test(self) -> float:
        """
        :return: alpha value generated by the strategy compared to benchmark.
        """
        self._run_strategy_and_benchmark()
        self.returns.dropna(inplace=True)
        results = self.returns[['Strategy', 'Benchmark']].sum().apply(np.exp)
        return (results['Strategy'] - results['Benchmark']) * 100

    def _run_strategy_and_benchmark(self) -> None:
        price_swing = np.log(self.data['Price'] / self.data['Price'].shift(1))
        self.returns['Strategy'] = self._calculate_returns(
            price_swing, self.strategy(self.data))
        self.returns['Benchmark'] = self._calculate_returns(
            price_swing, self.benchmark(self.data))

    @staticmethod
    def _calculate_returns(swing: np.ndarray, signal: np.ndarray) -> np.ndarray:
        return signal * swing
