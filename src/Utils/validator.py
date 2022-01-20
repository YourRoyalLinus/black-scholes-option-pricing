import os
import datetime
from pandas import Series, DataFrame

def is_valid_file(file_path :str) -> bool:
    return (os.path.exists(file_path) 
            and os.path.splitext(file_path)[1] == ".csv")

def is_valid_float(input :str) -> bool:
    try:
        float(input)
    except ValueError:
        return False
    return True

def is_valid_date(input :str) -> bool:  
    try:
        date_ = datetime.datetime.strptime(input, '%Y-%m-%d')
    except ValueError:
        return False

    today = datetime.datetime.today()
    if(date_ < today):
        return False
    else:
        return True

def is_sufficient_sample_size(dates :Series) -> bool:
    if(len(set(dates)) < 100):
        return False
    else:
        return True

def is_valid_dataset(df :DataFrame) -> bool:
    if "Date" in df.columns and "Close" in df.columns:
        return True
    else:
        return False
