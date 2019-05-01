"""
OpenE Core library
"""

from lib.opene.lexer import Token
from lib.opene.parser import Parser


class Functions:
    @staticmethod
    def hello_world(parameters: list = []):
        return Token("string", "\"Hello World! - From OpenE\"")

    @staticmethod
    def test(parameters: list = []):
        return Token("string","\"The external module 'core' was imported successfully\"")

    @staticmethod
    def print(parameters: list = []):
        for parameter in parameters:
            print(Parser().value_of(parameter), end="")
        print()
        return Token("Empty", "Empty")

    @staticmethod
    def input(parameters: list = []):
        prompt = ""
        for parameter in parameters:
            prompt += Parser().value_of(parameter)
        user_input = input(prompt)
        return Token("string", "\"{}\"".format(user_input))

    @staticmethod
    def range(parameters: list = []):
        start_value = 0
        end_value = 0
        step = 1
        values = []
        if (len(parameters) == 1):
            end_value = int(parameters[0].value)
        elif (len(parameters) == 2):
            start_value = int(parameters[0].value)
            end_value = int(parameters[1].value)
        elif (len(parameters) == 3):
            start_value = int(parameters[0].value)
            end_value = int(parameters[1].value)
            step = int(parameters[2].value)
        else:
            pass  # Todo: Raise error
        for value in range(start_value, end_value, step ):
            values.append(Token("integer", str(value)))
        return Token("list", values)

    @staticmethod
    def to_matrix(parameters: list = []):
        if (parameters[0].type == "matrix"):
            matrix = parameters[0].value
            new_value = parameters[1]
            if (new_value.type == "list"):
                values_to_use = new_value.value
                i = 0
                for current_y, row in enumerate(matrix):
                    for current_x, item in enumerate(row):
                        matrix[current_y][current_x] = values_to_use[i]
                        if (i+1 < len(values_to_use)):
                            i += 1
                        else:
                            i = 0
            # print(matrix)
            return Token("matrix", matrix)
        else:
            pass  # Todo: Raise error

    @staticmethod
    def to_column(parameters: list = []):
        if (parameters[0].type == "matrix"):
            matrix = parameters[0].value
            if (parameters[1].type == "list"):
                values_to_use = parameters[1].value
                column_number = int(parameters[2].value)
                i = 0
                for current_y, row in enumerate(matrix):
                    for current_x, item in enumerate(row):
                        if (current_x == column_number):
                            matrix[current_y][current_x] = values_to_use[i]
                            if (i+1 < len(values_to_use)):
                                i += 1
                            else:
                                i = 0
                return Token("matrix", matrix)
            else:
                pass  # Todo: Raise error
        else:
            pass  # Todo: Raise error


class ExternalParser(Parser):
    def __init__(self, *argv):
        super().__init__(*argv)

    # noinspection PyMethodOverriding
    def parse(self, function_name: str, parameters: list = [], errors = None):
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

    functions = {
        "HelloWorld": [0, Functions.hello_world],
        "test": [0, Functions.test],
        "print": ["1=+", Functions.print],
        "input": ["1=+", Functions.input],
        "range": ["1=+", Functions.range],
        "to_matrix": [2, Functions.to_matrix],
        "to_column": [3, Functions.to_column]
    }
