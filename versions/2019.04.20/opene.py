"""
OpenE Version 2019.04.20
Created by Anthony Provenza
Licensed under the MIT License
Copyright 2019 Anthony Provenza
"""

import os
import sys

from lib.opene.argparser import *


class OpenE:
    pass


# This is where the main code will go
# The line below checks if the file is being run or is being imported as a module
# It is only run on its own and not as a module
if (__name__ == "__main__"):
    ArgumentParser = ArgumentParser(this_location=os.getcwd(),
                                    argument_file_location="./lib/json/arguments.json")
    arguments = ArgumentParser.parse_arguments(sys.argv)
    print(arguments)
