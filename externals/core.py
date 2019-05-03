"""
OpenE Core library
"""

import collections

from lib.opene.lexer import Token
from lib.opene.devkit import ExternalModule
from lib.opene.devkit import DeveloperKit


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
            print(DeveloperKit().value_of(parameter), end="")
        print()
        return Token("Empty", "Empty")

    @staticmethod
    def input(parameters: list = []):
        prompt = ""
        for parameter in parameters:
            prompt += DeveloperKit().value_of(parameter)
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

    @staticmethod
    def get_column(parameters: list = None) -> Token:
        if (parameters[0].type == "matrix"):
            matrix = parameters[0]
            column_index = False
            output_list = []
            if (parameters[1].type == "integer"
                    or parameters[1].type == "float"
                    or parameters[1].type == "sum"):
                column_index = int(eval(parameters[1].value))
            elif (parameters[1].type == "string"):
                column_name = parameters[1].value[1:-1]
                for index, name in enumerate(matrix.value[0]):
                    if (not column_index):
                        if (name.value[1:-1] == column_name):
                            column_index = index
            for row in matrix.value:
                for index, current_data in enumerate(row):
                    if (index == column_index):
                        output_list.append(current_data)
            return Token("list", output_list)
        else:
            pass  # Todo: Raise error

    @staticmethod
    def count(parameters: list = None) -> Token:
        # Todo: Allow option to remove the title
        if (parameters[0].type == "list"):
            list_data = parameters[0].value
            counts_dict = {}
            for item in list_data:
                if (item.type == "string"):
                    item.value = item.value[1:-1]
                if (item.value in counts_dict):
                    counts_dict[item.value] = counts_dict[item.value] + 1
                else:
                    counts_dict[item.value] = 1
            # Sort the values from highest to lowest
            counts_dict = collections.OrderedDict(sorted(counts_dict.items(), key=lambda kv: kv[1], reverse=True))
            x_size = 2
            y_size = len(counts_dict)
            count_matrix = [[Token("integer", "0") for x in range(x_size)] for y in range(y_size)]
            i = 0
            for value, count in counts_dict.items():
                count_matrix[i][0] = Token("string", "\"{}\"".format(value))
                count_matrix[i][1] = Token("integer", str(count))
                i += 1
            return Token("matrix", count_matrix)
        else:
            pass  # Todo: Raise error

    @staticmethod
    def remove_items(parameters: list = None) -> Token:
        if (parameters[0].type == "list" and parameters[1].type in ["sum", "integer", "float"]):
            old_list = parameters[0].value
            strip_value = int(eval(parameters[1].value))
            new_list = old_list[int(strip_value):]
            return Token("list", new_list)
        else:
            pass  # Todo: Raise error

    @staticmethod
    def remove_value(parameters: list = None) -> Token:
        if (parameters[0].type == "list"):
            old_list = parameters[0].value
            to_remove = parameters[1]
            new_list = [item for item in old_list
                        if not (item.value == to_remove.value and item.type == to_remove.type)]
            return Token("list", new_list)
        else:
            pass  # Todo: Raise error

    @staticmethod
    def add_row_top(parameters: list = None) -> None:
        matrix = parameters[0].value
        headers = parameters[1].value
        new_matrix = []
        new_matrix.append(headers)
        for row in matrix:
            new_matrix.append(row)
        print(new_matrix)
        return Token("matrix", new_matrix)




class ExternalParser(ExternalModule):
    functions = {
        "HelloWorld": [0, Functions.hello_world],
        "test": [0, Functions.test],
        "print": ["1=+", Functions.print],
        "input": ["1=+", Functions.input],
        "range": ["1=+", Functions.range],
        "to_matrix": [2, Functions.to_matrix],
        "to_column": [3, Functions.to_column],
        "get_column": [2, Functions.get_column],
        "count": [1, Functions.count],
        "remove_items": [2, Functions.remove_items],
        "remove_value": [2, Functions.remove_value],
        "add_row_top": [2, Functions.add_row_top]
    }
