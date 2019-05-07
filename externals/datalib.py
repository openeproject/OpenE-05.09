"""
DataLib for OpenE
Todo: Add a function to read other file types, such as xlsx
"""

import csv
import os

from lib.opene.lexer import Token
from lib.opene.devkit import ExternalModule
from lib.opene.devkit import DeveloperKit


class Functions:
    @staticmethod
    def read_csv(parameters: list = None) -> Token:
        if (parameters[0].type == "string"):
            csv_location = parameters[0].value[1:-1]
            if (os.path.exists(csv_location)):
                with open(csv_location, "r") as csv_file_data:
                    reader = csv.reader(csv_file_data)
                    data = list(reader)
                x_size = len(data[0])  # Set the x size to the number of entries in the first row
                y_size = len(data)
                new_matrix = [["" for x in range(x_size)] for y in range(y_size)]
                for y, row in enumerate(data):
                    for x, item in enumerate(row):
                        new_matrix[y][x] = Token("string", "\"{}\"".format(data[y][x]))
                return Token("matrix", new_matrix)
            else:
                print("The specified CSV file does not exist")
                return Token("Empty", "Empty")
                # Todo: Fix this :|
        else:
            pass  # Todo: Raise error


class ExternalParser(ExternalModule):
    functions = {
        "read_csv": [1, Functions.read_csv]
    }
