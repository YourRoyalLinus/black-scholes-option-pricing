import sys
import pandas as pd
from BlackScholes.black_scholes import BlackScholes
from CommandLine.command_line_parser import parse_args
from Utils.utils import validate_input_data, read_historical_file, is_sufficient_sample_size

def main(argv):
    input_data = parse_args(argv)
    validate_input_data(input_data)
    
    df = read_historical_file(input_data['historical_data_file'])
    close_dates = df["Date"]
    close_prices = df["Close"]

    sufficient_data_size = is_sufficient_sample_size(close_dates)

    model = BlackScholes(close_prices[0], input_data["strike_price"], input_data["expiration_date"], close_prices, input_data["risk_free"])
   
    print(model.price())


    
if __name__ == "__main__":
    main(sys.argv[1:])