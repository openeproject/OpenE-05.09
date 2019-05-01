"""
OpenE Version 2019.04.22
Created by Anthony Provenza
Licensed under the MIT License
Copyright 2019 Anthony Provenza
"""

import os
import sys

from lib.opene.argparser import *
from lib.opene.cli import *
from lib.opene.file import *


# This is where the main code will go
# The line below checks if the file is being run or is being imported as a module
# It is only run on its own and not as a module
if (__name__ == "__main__"):
    ArgumentParser = ArgumentParser(this_location=os.getcwd(),
                                    argument_file_location="./lib/json/arguments.json")
    parsed_arguments = ArgumentParser.parse_arguments(sys.argv)
    if ("input_file" in parsed_arguments):
        file = File(debug_mode="debug" in parsed_arguments,
                    parse_mode="parse" in parsed_arguments,
                    output_file=parsed_arguments["output_file"] if "output_file" in parsed_arguments else False,
                    base_directory=os.getcwd())
        file.main(parsed_arguments["input_file"]["values"][0])
    else:
        cli = CLI(debug_mode="debug" in parsed_arguments,
                  parse_mode="parse" in parsed_arguments,
                  output_file=parsed_arguments["output_file"] if "output_file" in parsed_arguments else False)
        cli.mainloop()
