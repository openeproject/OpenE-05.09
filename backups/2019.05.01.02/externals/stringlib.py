"""
Stringlib for OpenE
"""

from lib.opene.lexer import Token
from lib.opene.parser import Parser


class Functions:
    @staticmethod
    def join(parameters: list = None) -> Token:
        final_string = "\""
        for value in parameters:
            if (value.type == "string"):
                final_string += value.value[1:-1]
            else:
                pass  # Todo: Raise error
        final_string += "\""
        return Token("string", final_string)

    @staticmethod
    def string_length(parameters: list = None) -> Token:
        value = parameters[0]
        if (value.type == "string"):
            value_length = str(len(value.value[1:-1]))
            return Token("integer", value_length)
        else:
            pass  # Todo: Raise error

    @staticmethod
    def split_string(parameters: list = None) -> Token:
        value = parameters[0]
        delimiters = []
        if (len(parameters) > 1):
            for delim in parameters[1:]:
                if (delim.type == "string"):
                    delimiters.append(delim.value[1:-1])
                elif (delim.type == "list"):
                    for item in delim.value:
                        if (item.type == "string"):
                            delimiters.append(delim.value[1:-1])
                else:
                    pass  # Todo: Raise error
        else:
            delimiters = list(" .,?!\"$%^&*()-_+=[]{};:'@#~<>\\|")
        strings = []
        current_string = ""
        for character in value.value[1:-1]:
            if (character in delimiters):
                if (len(current_string) > 0):
                    strings.append(Token("string", "\"{}\"".format(current_string)))
                current_string = ""
                character = ""
            current_string += character
        if (len(current_string) > 0):
            strings.append(Token("string", current_string))
        if (value.type == "string"):
            return Token("list", strings)
        else:
            pass  # Todo: Raise error

    @staticmethod
    def replace_string(parameters: list = None) -> Token:
        if (parameters[0].type == "string"
                and parameters[1].type == "string"
                and parameters[2].type == "string"):
            existing_string = parameters[0].value[1:-1]
            old_value = parameters[1].value[1:-1]
            new_value = parameters[2].value[1:-1]
            replaced_string = existing_string.replace(old_value, new_value)
            return Token("string", "\"{}\"".format(replaced_string))
        else:
            pass  # Todo: Raise error

    @staticmethod
    def upper(parameters: list = None) -> Token:
        if (parameters[0].type == "string"):
            return Token("string", parameters[0].value.upper())
        else:
            pass  # Todo: Raise error

    @staticmethod
    def lower(parameters: list = None) -> Token:
        if (parameters[0].type == "string"):
            return Token("string", parameters[0].value.lower())
        else:
            pass  # Todo: Raise error

    @staticmethod
    def invert_case(parameters: list = None) -> Token:
        if (parameters[0].type == "string"):
            old_string = parameters[0].value
            new_string = ''.join(character.lower() if character.isupper()
                                 else character.upper()
                                 for character in old_string)
            return Token("string", new_string)
        else:
            pass  # Todo: Raise error

    @staticmethod
    def reverse_string(parameters: list = None) -> Token:
        if (parameters[0].type == "string"):
            return Token("string", parameters[0].value[::-1])
        else:
            pass  # Todo: Raise error

    @staticmethod
    def strip(parameters: list = None) -> Token:
        if (parameters[0].type == "string"):
            old_string = parameters[0].value[1:-1]
            new_string = old_string  # Prevents any Python errors
            if (len(parameters) == 1):
                new_string = old_string.strip()
            elif (len(parameters) == 2):
                if (parameters[1].type == "string"):
                    value_to_strip = parameters[1].value[1:-1]
                    new_string = old_string.strip(value_to_strip)
                else:
                    pass  # Todo: Raise error
            else:
                pass  # Todo: Raise error
            return Token("string", "\"{}\"".format(new_string))
        else:
            pass  # Todo: Raise error

    @staticmethod
    def strip_left(parameters: list = None) -> Token:
        if (parameters[0].type == "string"):
            old_string = parameters[0].value[1:-1]
            new_string = old_string  # Prevents any Python errors
            if (len(parameters) == 1):
                new_string = old_string.lstrip()
            elif (len(parameters) == 2):
                if (parameters[1].type == "string"):
                    value_to_strip = parameters[1].value[1:-1]
                    new_string = old_string.lstrip(value_to_strip)
                else:
                    pass  # Todo: Raise error
            else:
                pass  # Todo: Raise error
            return Token("string", "\"{}\"".format(new_string))
        else:
            pass  # Todo: Raise error

    @staticmethod
    def strip_right(parameters: list = None) -> Token:
        if (parameters[0].type == "string"):
            old_string = parameters[0].value[1:-1]
            new_string = old_string  # Prevents any Python errors
            if (len(parameters) == 1):
                new_string = old_string.lstrip()
            elif (len(parameters) == 2):
                if (parameters[1].type == "string"):
                    value_to_strip = parameters[1].value[1:-1]
                    new_string = old_string.rstrip(value_to_strip)
                else:
                    pass  # Todo: Raise error
            else:
                pass  # Todo: Raise error
            return Token("string", "\"{}\"".format(new_string))
        else:
            pass  # Todo: Raise error


class ExternalParser(Parser):

    functions = {
        "join": ["0+", Functions.join],
        "string_length": [1, Functions.string_length],
        "split_string": ["0+", Functions.split_string],
        "replace_string": [3, Functions.replace_string],
        "upper": [1, Functions.upper],
        "lower": [1, Functions.lower],
        "invert_case": [1, Functions.invert_case],
        "reverse_string": [1, Functions.reverse_string],
        "strip": ["0+", Functions.strip],
        "strip_left": ["0+", Functions.strip_left],
        "strip_right": ["0+", Functions.strip_right]
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

