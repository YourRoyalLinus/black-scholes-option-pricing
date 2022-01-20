import sys
from BlackScholes.black_scholes import BlackScholes
from CommandLine.command_line_parser import parse_args
from Utils.utils import output_results, get_required_inputs 
from Utils.utils import read_historical_file
from Utils.validator import is_sufficient_sample_size

def main(argv):
    input_data = parse_args(argv)
    get_required_inputs(input_data)
    df = read_historical_file(input_data['historical_data_file'])\
            .sort_values(by=['Date'], ascending=False, ignore_index=True)
    
    close_dates = df["Date"]
    close_prices = df["Close"] 

    sufficient_data_size = is_sufficient_sample_size(close_dates)

    model = BlackScholes(close_prices[0], 
                        input_data["strike_price"], 
                        input_data["expiration_date"], 
                        close_prices, 
                        input_data["risk_free"])
   
    output_results(sufficient_data_size, model, name=input_data['name'])
    #TODO
    #Greeks/Caching/Cool features
    #Mini-Refactor/minor improvements/optimize
    #deadline 1/22/22
    
if __name__ == "__main__":
    main(sys.argv[1:])