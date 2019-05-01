"""
DataLib for OpenE
Todo: Add a function to read other file types, such as xlsx
"""

import csv
import os

import pprint

from lib.opene.lexer import Token
from lib.opene.parser import Parser


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


class ExternalParser(Parser):

    functions = {
        "read_csv": [1, Functions.read_csv]
    }

    def __init__(self, *argv):
        super().__init__(*argv)

    def parse(self, function_name: str, parameters: list = None, errors=None) -> dict:
        return_value = {
            "ran": False,
            "i_increment": 0,
            "global_variables": {},
            "returned_data": None,
            "data_out": None
        }
        if (function_name in self.functions):
            expected_parameters, callable_function = self.functions[function_name]
            call_function = False
            if (type(expected_parameters) == int
                    or type(expected_parameters) == float):
                if (len(parameters) == expected_parameters):
                    call_function = True
                else:
                    errors.raise_error("IncorrectParameterQuantity", 0, 0, function_name)
            elif (type(expected_parameters) == str):
                if (expected_parameters[-1] == "+"):
                    if (expected_parameters[-2] == "="):
                        if (len(parameters) >= int(expected_parameters[:-2])):
                            call_function = True
                        else:
                            errors.raise_error("IncorrectParameterQuantity", 0, 0, function_name)
                    else:
                        if (len(parameters) > int(expected_parameters[:-1])):
                            call_function = True
                        else:
                            errors.raise_error("IncorrectParameterQuantity", 0, 0, function_name)
                elif (expected_parameters[-1] == "-"):
                    if (expected_parameters[-2] == "="):
                        if (len(parameters) <= int(expected_parameters[:-2])):
                            call_function = True
                        else:
                            errors.raise_error("IncorrectParameterQuantity", 0, 0, function_name)
                    else:
                        if (len(parameters) < int(expected_parameters[:-1])):
                            call_function = True
                        else:
                            errors.raise_error("IncorrectParameterQuantity", 0, 0, function_name)
            if (call_function):
                data_out = callable_function(parameters)
                return_value["ran"] = True
                return_value["returned_data"] = data_out
        return return_value
