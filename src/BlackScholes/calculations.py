import math
import datetime
import statistics
from typing import Iterable
from scipy import stats as stats
from BlackScholes import black_scholes

def _days_to_experation(target_exp_date :datetime.datetime) -> int:
    return target_exp_date - datetime.datetime.today() 

def price_return(closing_prices :Iterable) -> map:
    _previous_closing_prices = [
            price for (i, price) in enumerate(closing_prices) if i % 2 != 0
    ]

    def previous_closing(current_day_close_price, previous_day_close_price):
        return (current_day_close_price/previous_day_close_price) - 1

    return map(previous_closing, closing_prices, _previous_closing_prices)

def price_returns_plus_one(price_returns :Iterable) -> map:
    
    def add_one(value):
        return value+1
    
    return map(add_one, price_returns)

def natural_log_price_returns(price_returns_plus_one :Iterable) -> map:

    def natural_log(value):
        return math.log(value)

    return map(natural_log, price_returns_plus_one)

def adj_stdev_returns(closing_prices :Iterable) -> float:
    average_open_market_days = 253
    price_returns_ln = natural_log_price_returns(
                        price_returns_plus_one(
                            price_return(closing_prices)
                        )
                    )
    return (statistics.stdev(list(price_returns_ln))
            * math.sqrt(average_open_market_days))

def adj_time(target_exp_date :datetime.datetime) -> float:
    days_to_exp = _days_to_experation(target_exp_date)
    return days_to_exp/datetime.timedelta(days=365)

def distribution_one(model :'black_scholes.BlackScholes') -> float:
    return (math.log((model.underlying_price/model.target_strike)) 
                    + ((model.risk_free_rate 
                    + (model.std_dev_of_returns**2) / 2) * model.time_to_exp) 
                    / (model.std_dev_of_returns * math.sqrt(model.time_to_exp))
            )
        
def distribution_two(D1 :float, model :'black_scholes.BlackScholes') -> float:
    return D1 - (model.std_dev_of_returns * math.sqrt(model.time_to_exp))

def normalize_distribution(d :float) -> float:
    return stats.norm.cdf(d)

def present_value_strike(model: 'black_scholes.BlackScholes') -> float:
    return (model.target_strike 
            * math.exp(-model.risk_free_rate * model.time_to_exp))
