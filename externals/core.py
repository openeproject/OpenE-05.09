"""
OpenE Core library
"""

import collections

from lib.opene.lexer import Token
from lib.opene.devkit import ExternalModule
from lib.opene.devkit import DeveloperKit


# noinspection PyUnusedLocal
class Functions:
    @staticmethod
    def hello_world(parameters: list = None) -> Token:
        """
        Returns a simple string, good for testing
        :param parameters:
        :return:
        """
        return Token("string", "\"Hello World! - From OpenE\"")

    @staticmethod
    def test(parameters: list = None) -> Token:
        """
        Returns a simple string. Good for testing
        :param parameters:
        :return:
        """
        return Token("string", "\"The external module 'core' was imported successfully\"")

    @staticmethod
    def print(parameters: list = None) -> Token:
        """
        Ouputs the values given
        :param parameters:
        :return:
        """
        for parameter in parameters:
            print(DeveloperKit().value_of(parameter), end="")
        print()
        return Token("Empty", "Empty")

    @staticmethod
    def input(parameters: list = None) -> Token:
        """
        Gets the user to input a value. Uses the parameters as a prompt, similar to the print function
        :param parameters:
        :return:
        """
        prompt = ""
        for parameter in parameters:
            prompt += DeveloperKit().value_of(parameter)
        user_input = input(prompt)
        return Token("string", "\"{}\"".format(user_input))

    @staticmethod
    def range(parameters: list = None) -> Token:
        """
        Generates a list between 2 values
        :param parameters:
        :return:
        """
        start_value = 0
        end_value = 0
        step = 1
        values = []
        try:
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
            for value in range(start_value, end_value, step):
                values.append(Token("integer", str(value)))
            return Token("list", values)
        except ValueError:
            pass  # Todo: Raise error

    @staticmethod
    def first(parameters: list = None) -> Token:
        """
        Gets the first value of a list
        :param parameters:
        :return:
        """
        return parameters[0].value[0]

    @staticmethod
    def last(parameters: list = None) -> Token:
        """
        Gets the last value of a list
        :param parameters:
        :return:
        """
        return parameters[0].value[-1]

    @staticmethod
    def drop(parameters: list = None) -> Token:
        """
        Drops the first/last items of a list
        - Positive values are the first items of a list
        - Negative values are the last items of a list
        :param parameters:
        :return:
        """
        list_data = parameters[0].value
        drop_value = int(DeveloperKit.value_of(parameters[1]))
        if (drop_value > 0):
            new_list = list_data[drop_value:]
        elif (drop_value < 0):
            new_list = list_data[:drop_value]
        else:
            new_list = list_data
        return Token("list", new_list)

    @staticmethod
    def take(parameters: list = None) -> Token:
        """
        Takes the first/last items of a list
        - Positive values are the first items of a list
        - Negative values are the last items of a list
        :param parameters:
        :return:
        """
        list_data = parameters[0].value
        take_value = int(DeveloperKit.value_of(parameters[1]))
        if (take_value > 0):
            new_list = list_data[:take_value]
        elif (take_value < 0):
            new_list = list_data[take_value:]
        else:
            new_list = list_data
        return Token("list", new_list)

    @staticmethod
    def single(parameters: list = None) -> Token:
        """
        Takes a single item from a list, with the specififed position
        :param parameters:
        :return:
        """
        list_data = parameters[0].value
        data_index = int(DeveloperKit.value_of(parameters[1]))
        return list_data[data_index]

    @staticmethod
    def append(parameters: list = None) -> Token:
        """
        Adds the values to the end of the list
        :param parameters:
        :return:
        """
        list_data = parameters[0].value
        for item in parameters[1:]:
            list_data.append(item)
        return Token("list", list_data)

    @staticmethod
    def remove(parameters: list = None) -> Token:
        """
        Removes an item based on its value
        :param parameters:
        :return:
        """
        list_data = parameters[0].value
        value_to_remove = parameters[1]
        new_list = list()
        for item in list_data:
            if (item.value != value_to_remove.value):
                new_list.append(item)
        return Token("list", new_list)

    @staticmethod
    def join(parameters: list = None) -> Token:
        """
        Joins together 1 or more lists
        :param parameters:
        :return:
        """
        final_list = list()
        for current_list in parameters:
            if (current_list.type == "list"):
                for list_item in current_list.value:
                    final_list.append(list_item)
            else:
                pass  # Todo: Raise error
        return Token("list", final_list)

    @staticmethod
    def to_matrix(parameters: list = None) -> Token:
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
    def to_column(parameters: list = None) -> Token:
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
        """
        Removes the first x items from a list
        :param parameters:
        :return:
        """
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
    def add_row_top(parameters: list = None) -> Token:
        matrix = parameters[0].value
        headers = parameters[1].value
        new_matrix = list()
        new_matrix.append(headers)
        for row in matrix:
            new_matrix.append(row)
        return Token("matrix", new_matrix)


class ExternalParser(ExternalModule):
    functions = {
        "HelloWorld": [0, Functions.hello_world],
        "test": [0, Functions.test],
        "print": ["1=+", Functions.print],
        "input": ["1=+", Functions.input],
        "range": ["1=+", Functions.range],

        "first": [1, Functions.first],
        "last": [1, Functions.last],
        "drop": [2, Functions.drop],
        "take": ["2=+", Functions.take],
        "single": [2, Functions.single],
        "append": ["2=+", Functions.append],
        "remove": ["2=+", Functions.remove],
        "join": ["1=+", Functions.join],

        "to_matrix": [2, Functions.to_matrix],
        "to_column": [3, Functions.to_column],
        "get_column": [2, Functions.get_column],
        "count": [1, Functions.count],
        "remove_items": [2, Functions.remove_items],
        "remove_value": [2, Functions.remove_value],
        "add_row_top": [2, Functions.add_row_top]
    }
