import datetime
from typing import Iterable
from BlackScholes import calculations
from BlackScholes.calculations import std_dev_returns, adj_time 
from BlackScholes.calculations import probability_density_function_d1 
from BlackScholes.calculations import square_root_time, std_dev_returns 
from BlackScholes.calculations import distribution_one, distribution_two 
from BlackScholes.calculations import normalize_distribution
from BlackScholes.calculations import present_value_strike

class BlackScholes:
    def __init__(self, underlying_price :float, 
                target_strike :float, target_exp_date :datetime.datetime,  
                closing_prices :Iterable, risk_free_rate=00.0013):
        self.underlying_price = underlying_price
        self.target_strike = target_strike
        self.risk_free_rate = risk_free_rate
        self.exp_date = target_exp_date
        self.time_to_exp = adj_time(target_exp_date)
        self.std_dev_of_returns = std_dev_returns(closing_prices)
    
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
        return bool(self.underlying_price and 
                    self.target_strike and 
                    self.time_to_exp and 
                    self.std_dev_of_returns)
    
    def call_price(self) -> float:
        d1 = distribution_one(self)
        nd1 = normalize_distribution(d1)
        d2 = distribution_two(d1, self)
        nd2 = normalize_distribution(d2)
        pvk = present_value_strike(self)

        return round(self.underlying_price * nd1 - (pvk*nd2), 4)

    def put_price(self) -> float:
        pvk = present_value_strike(self)

        d1 = distribution_one(self)
        d2 = distribution_two(d1, self)
        nd2 = normalize_distribution(d2)
        nd1 = normalize_distribution(d1)

        _nd1 = 1 - nd1
        _nd2 = 1 - nd2
        
        return round(pvk * _nd2 - self.underlying_price * _nd1, 4)

    def call_delta(self) -> float:
        d1 = distribution_one(self)

        return round(normalize_distribution(d1), 4)
    
    def put_delta(self) -> float:
        d1 = distribution_one(self)
        nd1 = normalize_distribution(d1)

        return round(nd1 - 1, 4)

    def call_rho(self) -> float:
        pvk = present_value_strike(self)
        d1 = distribution_one(self)
        d2 = distribution_two(d1, self)
        nd2 = normalize_distribution(d2)

        return round((1 / 100) * pvk * self.time_to_exp * nd2, 4)
        
    def put_rho(self) -> float:
        d1 = distribution_one(self)
        pvk = present_value_strike(self)
        d2 = distribution_two(d1, self)
        nd2 = normalize_distribution(d2)
        _nd2 = 1 - nd2

        return round((1 / 100) * -(pvk * self.time_to_exp * _nd2), 4)

    def call_theta(self) -> float:
        d1 = distribution_one(self)
        d2 = distribution_two(d1, self)
        nd2 = normalize_distribution(d2)
        pvk = present_value_strike(self)

        pdf = probability_density_function_d1(d1)
        sqrt_t = square_root_time(self.time_to_exp)
        
        return round (  (1 / calculations.AVERAGE_OPEN_MARKET_DAYS)
                        * (-(((self.underlying_price * self.std_dev_of_returns)
                        / (2 * sqrt_t)) * pdf)             
                        - (self.risk_free_rate * pvk * nd2)), 4)

    def put_theta(self) -> float:
        d1 = distribution_one(self)
        d2 = distribution_two(d1, self)
        nd2 = normalize_distribution(d2)
        _nd2 = 1 - nd2
        pvk = present_value_strike(self)

        pdf = probability_density_function_d1(d1)
        sigma = std_dev_returns(self.std_dev_of_returns)
        sqrt_t = square_root_time(self.time_to_exp)

        return round (  (1 / calculations.AVERAGE_OPEN_MARKET_DAYS)
                        * (- ((self.underlying_price * sigma * 1) 
                        / (2 * (sqrt_t))* pdf)
                        + (self.risk_free_rate * pvk) * _nd2
                        - 0), 4)

    
    def gamma(self) -> float:
        d1 = distribution_one(self)
        pdf = probability_density_function_d1(d1)
        sqrt_t = square_root_time(self.time_to_exp)
        return round(pdf / (self.underlying_price
                    * self.std_dev_of_returns * sqrt_t), 4)

    def vega(self) -> float:
        d1 = distribution_one(self)
        pdf = probability_density_function_d1(d1)
        sqrt_t = square_root_time(self.time_to_exp)
        return round ((1 / 100) * self.underlying_price * sqrt_t * pdf , 4)
    
    


