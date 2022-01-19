import sys, getopt, datetime
from Utils.utils import is_valid_file

options = "hs:f:x:r:n:"
long_options = ["help", "strike_price=", "file=", "risk_free=", "name="]
help_message = "This program will estimate the theoretical value of an option contract using Black-Scholes modeling.\n"\
                "If you leave the command line empty, the program will prompt you for a historical financial data file, strike price, and expiration date.\n\n"\
                "The file should be a financial file (comma delimited) of at least 100 days containing the following fields:\n"\
                    "\t -Date\n" \
                    "\t -Close\n\n"\
                "The program will also prompt you for the strike price to be used. You can specifc the risk free rate using the -r or --risk_free flag.\n" \
                "If no risk free rate is provided, the default will be the coupon rate of the 3-month T-Bill as of 1/14/22 = .13% \n" \
                "You can also specific a name or ticker using the -n or --name flag \n\n" \
                "Program Flags: \n" \
                "\t -s, --strike_price <STRIKE> \t Strike price of the option (Required)\n"\
                "\t -f, --file <FILE> \t Path to a CSV file containing historical financial data for the stock with above requisite fields (Required)\n" \
                "\t -x, --expiration_date <DATE> \t Expiration date of the option contract <YYYY-MM-DD> (Required)\n"\
                "\t -r, --risk_free <RATE> \t Risk free rate to be used. Default risk free rate = 3-month Treasure Bills as of Jan 14th 2022: .13% (Optional)\n" \
                "\t -n, --name <NAME> \t Name or ticker symbol (Optional)\n" \
                "\t -h, --help \t Print this message and exit\n"
    
def parse_args(argv=None, *args) -> dict:
    input_data = {"historical_data_file": '', "strike_price" : 0.00, "expiration_date": None, "risk_free" : 00.13, "name" : ''}

    try:
        _opts, _args = getopt.getopt(argv, options, long_options)
    except getopt.GetoptError as e:
        print(e)
        sys.exit(-1)

    for o, a in _opts:
        if o in ("-h", "--help"):
            print(help_message,)
            sys.exit()
        elif o in ("-s", "--strike_price"):
            try:
                input_data["strike_price"] = float(a)
            except ValueError as e:
                print(e)
                sys.exit(-1)
        elif o in ("-f", "--file"):
            if is_valid_file(a):
                input_data["historical_data_file"] = a
            else:
                print(f"{a} is not a valid file.")
                sys.exit(-1)
        elif o in ("-x", "--expiration_date"):
            try:
                input_data["expiration_date"] = datetime.datetime.strptime(a, '%Y-%m-%d')
            except ValueError as e:
                print(f"{a} is not a valid date.")
                sys.exit(-1)
        elif o in ("-r", "--risk_free"):
            try:
                input_data["risk_free"] = float(a)
            except ValueError as e:
                print(e)
                sys.exit(-1)    
        elif o in ("-n", "--name"):
            input_data["name"] = a
        else:
            print(f"No program flag for {o} with arg {a}")
            sys.exit(-1)
    return input_data

    
