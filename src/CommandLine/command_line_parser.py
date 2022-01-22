import sys, getopt, datetime
from Utils.validator import is_valid_file, is_valid_date, is_valid_float
from Utils.output import display_help_message

_OPTIONS = "hs:f:x:o:r:n:"
_LONG_OPTIONS = ["help", "strike_price=", "file=", "expiration_date=",
                 "option_type=", "risk_free=", "name="]
   
def parse_args(argv=None, *args) -> dict:
    input_data = {"historical_data_file": '', "strike_price": 0.00,
                "expiration_date": None, "option_type": 'Call', 
                "risk_free": 00.0013, "name": ''}

    try:
        _opts, _args = getopt.getopt(argv, _OPTIONS, _LONG_OPTIONS)
    except getopt.GetoptError as e:
        print(e)
        sys.exit(-1)

    for o, a in _opts:
        if o in ("-h", "--help"):
            display_help_message()
            sys.exit()
        elif o in ("-s", "--strike_price"):
            if a.lower().endswith('c'):
                input_data["option_type"] = "Call"
                a = a[:-1]
            elif a.lower().endswith('p'):
                input_data["option_type"] = "Put"
                a = a[:-1]

            if(is_valid_float(a)):
                input_data["strike_price"] = float(a)
            else:
                print(f'{a} is not a valid strike price.')
                sys.exit(-1)
        elif o in ("-f", "--file"):
            if is_valid_file(a):
                input_data["historical_data_file"] = a
            else:
                print(f"{a} is not a valid file.")
                sys.exit(-1)
        elif o in ("-x", "--expiration_date"):
            if(is_valid_date(a)):
                input_data["expiration_date"] = datetime.datetime\
                                                .strptime(a, '%Y-%m-%d')
            else:
                print(f"{a} is not a valid date.")
                sys.exit(-1)
        elif o in ("-r", "--risk_free"):
            if(is_valid_float(a)):
                input_data["risk_free"] = float(a)
            else:
                print(f'{a} is not a valid rate value.')
                sys.exit(-1)
        elif o in ("-n", "--name"):
            input_data["name"] = a
        elif o in ("-o", "--option_type"):
            if a.lower() =='c':
                input_data["option_type"] = "Call"
            elif a.lower() == 'p':
                input_data["option_type"] = "Put"
    return input_data

    
