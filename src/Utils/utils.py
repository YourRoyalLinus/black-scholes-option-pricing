import datetime 
import sys
import pandas as pd
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