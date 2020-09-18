import pandas as pd


class Universe:
    """ Universe is a class used for close to real life simulations. """

    def __init__(self, data: pd.DataFrame, given: float):
        """
        :param data: must include columns 'Price' and 'Position'.
        :param given: initial amount of money in traded currency.
        """
        self.data: pd.DataFrame = data
        self.given: float = given

    def simulate(self) -> float:
        """ :return: final amount in base currency. """
        prev_pos = self.data['Position'][0]
        instrument, base = (self.given / self.data['Price'][0], 0.0) \
            if prev_pos == 1 else (0.0, self.given)

        for price, position in zip(
                self.data['Price'][1:], self.data['Position'][1:]):
            if position == prev_pos:
                continue

            instrument, base = (base / price, 0) \
                if position == 1 else (0, instrument * price)
            prev_pos = position

        final_price = self.data['Price'][-1]
        final = instrument * final_price if base == 0 else base
        return final
