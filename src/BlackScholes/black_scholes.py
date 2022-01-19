import datetime
from typing import Iterable
from BlackScholes.calculations import adj_stdev_returns, adj_time, distribution_one, distribution_two, normalize_distribution, present_value_strike

class BlackScholes:
    def __init__(self, underlying_price :float, target_strike :float, target_exp_date :datetime.datetime,  closing_prices :Iterable, risk_free_rate=00.13):
        self.underlying_price = underlying_price
        self.target_strike = target_strike
        self.risk_free_rate = risk_free_rate
        self.time_to_exp = adj_time(target_exp_date)
        self.std_dev_of_returns = adj_stdev_returns(closing_prices)
    
    def price(self) -> float:
        D1 = distribution_one(self)
        ND1 = normalize_distribution(D1)
        D2 = distribution_two(D1, self)
        ND2 = normalize_distribution(D2)
        PvK = present_value_strike(self)

        return round(self.underlying_price * ND1 - (PvK*ND2), 4)



