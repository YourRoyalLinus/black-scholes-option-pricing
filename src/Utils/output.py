from BlackScholes.black_scholes import BlackScholes

_HELP_MESSAGE = (
        "This program will estimate the theoretical value of an "
        "European option contract using Black-Scholes modeling.\n"
        "If you leave the command line empty, the program will prompt you "
        "for a historical financial data file, strike price, and "
        "expiration date.\n\n"
        "The file should be a financial file (comma delimited) of at least "
        "100 days containing the following fields:\n"
        "\t -Date\n"
        "\t -Close\n\n"
        "The program will also prompt you for the strike price to be "
        "used. You can specifc the risk free rate using the -r or "
        "--risk_free flag.\n"
        "If no risk free rate is provided, the default will be the "
        "coupon rate of the 3-month T-Bill as of 1/14/22 = .13%. \n"
        "You can also specific a name or ticker using the -n or "
        "--name flag. \n\n"
        "Program Flags: \n"
        "\t {0:<30}Strike price of the option (Required).\n"
        "\t {1:<30}Path to a CSV file containing "
        "historical financial data for the stock with above "
        "requisite fields (Required)\n"
        "\t {2:<30}Expiration date of "
        "the option contract <YYYY-MM-DD> (Required)\n"
        "\t {3:<30}Option Type, \"c\" for Call or \"p\" for Put (Optional). "
        "Can be postfixed to the strike price - 0.00c OR 0.00p. "
        "If not specified, option type defaults to Call.\n"
        "\t {4:<30}Risk free rate to be used."
        "Default risk free rate = 3-month Treasure Bills "
        "as of Jan 14th 2022: .13% (Optional)\n"
        "\t {5:<30}Name or ticker symbol "
        "(Optional)\n"
        "\t {6:<30}Print this message and exit\n".format(
                                                "-s, --strike_price <STRIKE>",
                                                "-f, --file <FILE>",
                                                "-x, --expiration_date <DATE>",
                                                "-o, --option_type <C/P>",
                                                "-r, --risk_free <RATE>",
                                                "-n, --name <NAME>",
                                                "-h, --help")
) 

_RESULT_OUTPUT_LEN = 132

def _line_break() -> None:
    print()

    return None

def _table_border(symbol: str) -> None:
    print(symbol*_RESULT_OUTPUT_LEN)

    return None

def display_results(sufficient_sample :bool, option_type :str, 
                    model :BlackScholes, name=None) -> None:
    if not sufficient_sample:
        display_warning()
    
    display_model(option_type, model, name)
    display_greeks(option_type, model)

    return None

def display_help_message() -> None:
    print(_HELP_MESSAGE)

    return None
 
def display_warning() -> None:
    warning_line_one = "* " + (" * " * 20) + "WARNING " + (" * " * 20) + " *"
    warning_line_two ="\n* {0:^128} *".format(
                                    "Fewer than 100 close prices provided; "
                                    "data will be less reliable as a result"
                                )
    warning_line_three="\n" + "*  " + (" * "*42) + "  *"
    warning_msg = warning_line_one + warning_line_two + warning_line_three

    _line_break()
    print(warning_msg)
    _line_break()
    
    return None

def display_model(option_type :str, model : BlackScholes, name :str) -> None:
    name_formatted = (name[:30] + "...") if len(name) > 30\
                                         else name if name else "N/A"
    price_formatted = round(model.underlying_price, 2)
    date_formatted = model.exp_date.strftime('%Y-%m-%d')
    model_funcs = (model.put() if option_type == "Put" else
                        model.call())

    header_fmt = "| {0:^33} | {1:^15} | {2:^15} |".format("Company",
                                                          "Underlying Price",
                                                          "Target Strike") \
                + " {0:^15} | {1:^14} | {2:^16} |".format("Risk Free Rate", 
                                                         "Expiration Date",
                                                         "Expected " 
                                                         + option_type +
                                                         " Price")

    body_fmt = "| {0:^33} | ${1:^15} |".format(name_formatted, 
                                               price_formatted) \
                + " ${0:^14} | {1:^14}% |".format(model.target_strike,
                                                  model.risk_free_rate) \
                + " {0:^15} | ${1:^18} |".format(date_formatted, 
                                                 model_funcs["price"])

    _table_border('~')
    print(header_fmt)
    print(body_fmt)
    _table_border('~')

    return None

def display_greeks(option_type :str, model : BlackScholes) -> None:
    model_funcs = (model.put() if option_type == "Put" else
                        model.call())

    header_fmt =  "| {0:^33} | {1:^15} | {2:^16} |".format("Greeks", "Delta", 
                                                            "Gamma") \
                + " {0:^15} | {1:^15} | {2:^19} |".format("Theta", "Vega", 
                                                            "Rho")

    body_fmt = "| {0:^33} | {1:^15} | {2:^16} |".format(f"{option_type}", 
                                                        model_funcs["delta"], 
                                                        model_funcs['gamma']) \
                + " {0:^15} | {1:^15} | {2:^19} |".format(model_funcs['theta'],
                                                        model_funcs['vega'],
                                                        model_funcs['rho'])
    _table_border('~')                                                    
    print(header_fmt)
    print(body_fmt)
    _table_border('~')

    return None