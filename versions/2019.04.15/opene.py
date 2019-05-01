"""
OpenE version 2019.04.15
Created by Anthony Provenza
Licensed under the MIT License
Copyright 2019 Anthony Provenza
"""

import sys

from opene import arparse, cli


if (__name__ == "__main__"):
    arguments = {}
    if (len(sys.argv) == 1):
        arguments = {"input_file": False}
    else:
        pass
    if (arguments["input_file"]):
        cli.CLI().mainloop()
