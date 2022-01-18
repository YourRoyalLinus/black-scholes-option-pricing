import sys
from CommandLine.command_line_parser import parse_args
from Utils.utils import validate_input_data

def main(argv):
    input_data = parse_args(argv)
    validate_input_data(input_data)
    print(input_data)

   



    
if __name__ == "__main__":
    main(sys.argv[1:])