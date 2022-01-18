import datetime
import os, sys


def is_valid_file(file_path :str) -> bool:
    return os.path.exists(file_path) and os.path.splitext(file_path)[1] == ".csv"

def validate_input_data(input_data :dict) -> None:
    if not input_data["historical_data_file"]:
        input_data["historical_data_file"] = get_historical_file()
    if not input_data["strike_price"]:
        input_data["strike_price"] = get_strike_price()
    if not input_data["expiration_date"]:
        input_data["expiration_date"] = get_expiration_date()

def get_historical_file() -> str:
    user_input = input('Please enter a historical data file to build the Black-Scholes model (Rerun with flag -h or --help to for more information): ')
    while is_valid_file(user_input) == False:
        user_input = input(f'{user_input} is not a valid file. Would you like to try again? ')
        if user_input and user_input[0].upper() == 'Y':
            user_input = get_historical_file()
        else:
            sys.exit()

    return user_input

def get_strike_price() -> float:
    user_input = input('Please enter a targeted strike price (Rerun with flag -h or --help to for more information): ')
    try:
        user_input = float(user_input)
    except ValueError as e: #its own func?
        invalid_input = user_input
        user_input = 0

    while not user_input:
        user_input = input(f'{invalid_input} is not a valid strike price. Would you like to try again? ')
        if user_input and user_input[0].upper() == 'Y':
            user_input = get_strike_price()
        else:
            sys.exit()

    return user_input

def get_expiration_date() -> datetime.datetime:
    _valid_date = False
    user_input = input('Please enter an expiration date of the contract in <YYYY-MM-DD> format (Rerun with flag -h or --help to for more information): ')
    try:
        user_input = datetime.datetime.strptime(user_input, '%Y-%m-%d')
        _valid_date = True
    except ValueError as e: #its own func?
        _valid_date  = False

    while not _valid_date:
        user_input = input(f'{user_input} is not a valid date. Would you like to try again? ')
        if user_input and user_input[0].upper() == 'Y':
            user_input = get_expiration_date()
        else:
            sys.exit()

    return user_input