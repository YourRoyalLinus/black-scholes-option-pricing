import datetime 
import sys
import pandas as pd
from BlackScholes.black_scholes import BlackScholes
from .validator import is_valid_file, is_valid_float, is_valid_date 
from .validator import is_valid_dataset

def get_historical_file() -> str:
    user_input = input("Please enter a historical data file to build the  "
                        "Black-Scholes model (Rerun with flag "
                        "-h or --help to for more information): ")
    while not is_valid_file(user_input):
        user_input = input(f"{user_input} is not a valid file. "
                            "Would you like to try again? ")
        if user_input and user_input[0].upper() == 'Y':
            user_input = get_historical_file()
        else:
            sys.exit()

    return user_input

def get_strike_price() -> float:
    user_input = input("Please enter a targeted strike price (Rerun with flag "
                        "-h or --help to for more information): ")
    while not is_valid_float(user_input):
        user_input = input(f"{user_input} is not a valid strike price. "
                            "Would you like to try again? ")
        if user_input and user_input[0].upper() == 'Y':
            user_input = get_strike_price()
        else:
            sys.exit()

    return float(user_input)

def get_expiration_date() -> datetime.datetime:
    user_input = input("Please enter an expiration date of the contract in "
                        "<YYYY-MM-DD> format (Rerun with flag -h or --help to "
                        "for more information): ")
            
    while not is_valid_date(user_input):
        user_input = input(f"{user_input} is not a valid date or has already " 
                            "passed. Would you like to try again? ")
        if user_input and user_input[0].upper() == 'Y':
            user_input = get_expiration_date().strftime('%Y-%m-%d')
        else:
            sys.exit()

    return datetime.datetime.strptime(user_input, '%Y-%m-%d')

def get_required_inputs(input_data :dict) -> None:
    if not input_data["historical_data_file"]:
        input_data["historical_data_file"] = get_historical_file()
    if not input_data["strike_price"]:
        input_data["strike_price"] = get_strike_price()
    if not input_data["expiration_date"]:
        input_data["expiration_date"] = get_expiration_date()
    return None

def read_historical_file(file_path :str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    if is_valid_dataset(df):
        return df
    else:
        print(f"Historical file is missing mandatory column(s): \"Date\" "
                "and/or \"Close\". Ensure that the mandatory columns "
                "conform to these names.")
        print(f"Columns Found: {df.columns}")
        sys.exit()

def output_results(sufficient_sample :bool, model :BlackScholes, 
                    name=None) -> None:
    output_len = 132

    warning_line_one = "* " + (" * " * 20) + "WARNING " + (" * " * 20) + " *"
    warning_line_two ="\n* {0:^128} *".format(
                                    "Fewer than 100 close prices provided; "
                                    "data will be less reliable as a result"
                                )
    warning_line_three="\n" + "*  " + (" * "*42) + "  *"
    warning_msg = warning_line_one + warning_line_two + warning_line_three

    if not sufficient_sample:
        print()
        print(warning_msg)
        print()
    
    name_formatted = (name[:30] + "...") if len(name) > 30\
                                         else name if name else "N/A"
    price_formatted = round(model.underlying_price, 2)
    date_formatted = model.exp_date.strftime('%Y-%m-%d')

    border = '~'*output_len
    header_fmt = "| {0:^33} | {1:^15} | {2:^15} |".format("Company",
                                                          "Underlying Price",
                                                          "Target Strike") \
                + " {0:^15} | {1:^14} | {2:^16} |".format("Risk Free Rate", 
                                                         "Expiration Date",
                                                         "Expected Call Price")

    body_fmt = "| {0:^33} | ${1:^15} |".format(name_formatted, 
                                               price_formatted) \
                + " ${0:^14} | {1:^14}% |".format(model.target_strike,
                                                  model.risk_free_rate) \
                + " {0:^15} | ${1:^18} |".format(date_formatted, 
                                                 model.call_price())
    
    print(border)
    print(header_fmt)
    print(body_fmt)
    print(border)

    return None 
