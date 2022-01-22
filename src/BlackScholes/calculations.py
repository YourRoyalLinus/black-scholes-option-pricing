import math
import datetime
import statistics
from typing import Iterable
from scipy import stats
from BlackScholes import black_scholes

AVERAGE_OPEN_MARKET_DAYS = 253
    
def _days_to_experation(target_exp_date :datetime.datetime) -> int:
    return target_exp_date - datetime.datetime.today() 

def _price_returns(closing_prices :Iterable) -> Iterable:
    return [(closing_prices[i]/closing_prices[i+1]) - 1  #Optimize w/ dict?
                        for i in range(0, len(closing_prices)-1)]

def _price_returns_plus_one(price_returns :Iterable) -> map:
    
    def add_one(value):
        return value+1
    
    return map(add_one, price_returns)

def _natural_log_price_returns(price_returns_plus_one :Iterable) -> map:

    def natural_log(value):
        return math.log(value)

    return map(natural_log, price_returns_plus_one)

def std_dev_returns(closing_prices :Iterable) -> float:
    price_returns_ln = _natural_log_price_returns(
                        _price_returns_plus_one(
                            _price_returns(closing_prices)
                        )
                    )
    return (math.sqrt(statistics.variance(price_returns_ln)) 
            * math.sqrt(AVERAGE_OPEN_MARKET_DAYS))

def adj_time(target_exp_date :datetime.datetime) -> float:
    days_to_exp = _days_to_experation(target_exp_date)
    return days_to_exp/datetime.timedelta(days=365)

def square_root_time(time :float) -> float:
    return math.sqrt(time)

def distribution_one(model :'black_scholes.BlackScholes') -> float:
    num = (math.log(model.underlying_price/model.target_strike) 
        + (model.risk_free_rate + ((model.std_dev_of_returns ** 2) / 2)) 
        * model.time_to_exp)
    denom = model.std_dev_of_returns * math.sqrt(model.time_to_exp)
    return num/denom
        
def distribution_two(d1 :float, model :'black_scholes.BlackScholes') -> float:
    return d1 - (model.std_dev_of_returns * math.sqrt(model.time_to_exp))

def normalize_distribution(d :float) -> float:
    return stats.norm.cdf(d)

def probability_density_function_d1(d1 :float) -> float:
    return stats.norm.pdf(d1)

def present_value_strike(model: 'black_scholes.BlackScholes') -> float:
    return (model.target_strike 
            * math.exp(-model.risk_free_rate * model.time_to_exp))
