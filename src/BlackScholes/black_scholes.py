import datetime
from typing import Iterable
from BlackScholes.calculations import adj_stdev_returns, adj_time, distribution_one, distribution_two, normalize_distribution, present_value_strike

class BlackScholes:
    def __init__(self, underlying_price :float, target_strike :float, target_exp_date :datetime.datetime,  closing_prices :Iterable, risk_free_rate=00.13):
        self.underlying_price = underlying_price
        self.target_strike = target_strike
        self.risk_free_rate = risk_free_rate
        self.exp_date = target_exp_date
        self.time_to_exp = adj_time(target_exp_date)
        self.std_dev_of_returns = adj_stdev_returns(closing_prices)
    
    def __repr__(self):
        cls = type(self).__name__
        return "{}({})".format(cls, self.__dict__)
    
    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, BlackScholes):
            return (self.__dict__ == other.__dict__)
        return False

    def __bool__(self):
        return bool(self.underlying_price and self.target_strike and self.time_to_exp and self.std_dev_of_returns)
    
    def price(self) -> float:
        D1 = distribution_one(self)
        ND1 = normalize_distribution(D1)
        D2 = distribution_two(D1, self)
        ND2 = normalize_distribution(D2)
        PvK = present_value_strike(self)

        return round(self.underlying_price * ND1 - (PvK*ND2), 4)



