import importlib
import os
import sys

from lib.opene.errors import Errors
from lib.opene.lexer import Token


errors = Errors(error_file_location="./lib/json/errors.json",
                this_location=os.getcwd())


class DataManager:
    """
    This class stores all the values that a user defines in their code, such as variables, classes, imports and other
    """

    external_files = {}
    imported_modules = {}
    global_variables = {}
    classes = {}
    functions = {}
    default_variables = {
        "*": Token("Empty", "Empty"),
        "string": Token("string", "\"\""),
        "sum": Token("sum", "0"),
        "integer": Token("integer", "0"),
        "int": None,  # Doesn't need a value as it just uses the 'integer' values instead
        "float": Token("float", "0.0"),
        "boolean": Token("boolean", "false"),
        "list": Token("list", []),
        "matrix": Token("matrix", {})
    }
    accepted_variable_types = {
        "string": ["string"],
        "sum": ["sum", "integer", "float"],
        "integer": ["sum", "integer", "float"],
        "float": ["sum", "integer", "float"],
        "boolean": ["boolean"]
    }


class Parser:
    """
    This is the main parser class
    External modules should extend it in the future, when it is slightly better made
    """

    def __init__(self, cli_mode: bool = False):
        self.cli_mode = cli_mode
        global errors
        errors = Errors(cli_mode=cli_mode,
                        error_file_location="./lib/json/errors.json",
                        this_location=os.getcwd())

    def assign_variable(self,
                        variable_name: str,
                        variable_type: str,
                        variable_value: str = None,
                        line_number: int = 0,
                        col_number: int = 0,
                        current_class: str = None):
        if (current_class):
            pass
        else:
            if (variable_value):
                if (variable_type == "list"):
                    pass
                elif (variable_type == "matrix"):
                    pass
                else:
                    if (variable_type == "int"):  # Allow shorthand 'int' instead of 'integer'
                        variable_type = "integer"
                    if (variable_value.type in DataManager.accepted_variable_types[variable_type]):
                        if (variable_type == "integer"):
                            variable_value = Token(variable_value.type,
                                                   str(int(eval(variable_value.value))),
                                                   variable_value.line,
                                                   variable_value.col)
                        elif (variable_type == "float"):
                            variable_value = Token(variable_value.type,
                                                   str(float(eval(variable_value.value))),
                                                   variable_value.line,
                                                   variable_value.col)
                    else:
                        errors.raise_error("UnexpectedVariableType", 0, 0, variable_name, variable_value.type)
            else:
                variable_value = DataManager.default_variables[variable_type]
            DataManager.global_variables[variable_name] = Token(variable_type,
                                                                variable_value.value,
                                                                line_number,
                                                                col_number)

    def value_of(self, item: Token) -> str:
        value = ""
        if (item.type == "string"):
            return item.value[1:-1]
        return value

    # noinspection PyMethodMayBeStatic
    def debug_variable(self, variable_name: str) -> str:
        """
        Returns the value of a variable, if it is written in the program

        :param variable_name: The name of the variable
        :return: The value of the variable, or False if it does not exist
        """
        try:
            variable_value = DataManager.global_variables[variable_name]
            if (variable_value.type in ["sum", "integer", "float"]):
                return eval(variable_value.value)
            elif (variable_value.type == "string"):
                return variable_value.value
        except KeyError:
            return False

    def parse(self,
              lines: list,
              sub_parse: bool = False):
        if (sub_parse):
            values = []
            for tokens in lines:
                i = 0
                while i < len(tokens):
                    if (len(tokens) == 1):
                        if (tokens[i].type == "string"
                                or tokens[i].type == "integer"
                                or tokens[i].type == "float"):
                            values.append(tokens[i])
                            i += 1
                        elif (tokens[i].type == "sum"):
                            tokens[i].value = str(eval(tokens[i].value))
                            values.append(tokens[i])
                            i += 1
                        elif (tokens[i].type == "command"):
                            if (tokens[i].value in DataManager.classes):
                                print("Class: {}".format(tokens[i].value))
                            elif (tokens[i].value in DataManager.functions):
                                print("Function: {}".format(tokens[i].value))
                            elif (tokens[i].value in DataManager.global_variables):
                                values.append(DataManager.global_variables[tokens[i].value])
                            elif (tokens[i].value in DataManager.imported_modules):
                                pass
                            elif (tokens[i].value in DataManager.external_files):
                                pass
                            else:
                                errors.raise_error("UndefinedValue", tokens[i].line, tokens[i].col, tokens[i].value)
                                i = len(tokens)
                            i += 1
                    else:
                        pass
                return values
        else:
            for tokens in lines:
                i = 0
                while i < len(tokens):
                    if (len(tokens) == 1):
                        if (tokens[i].type == "command"):
                            if (tokens[i].value in DataManager.classes):
                                print("Class: {}".format(tokens[i].value))
                            elif (tokens[i].value in DataManager.functions):
                                print("Function: {}".format(tokens[i].value))
                            elif (tokens[i].value in DataManager.global_variables):
                                print("{} <- {}".format(tokens[i].value,
                                                        self.debug_variable(tokens[i].value)))
                            elif (tokens[i].value in DataManager.imported_modules):
                                pass
                            elif (tokens[i].value in DataManager.external_files):
                                pass
                            else:
                                errors.raise_error("UndefinedValue", tokens[i].line, tokens[i].col, tokens[i].value)
                                i = len(tokens)
                            i += 1
                        else:
                            print(self.value_of(tokens[i]))
                            i += 1
                    else:
                        if (tokens[i].type == "command"):
                            if (tokens[i+1].type == "operator"):
                                if (tokens[i+1].value == "OB"):
                                    pass
                                else:
                                    errors.raise_error("UnexpectedOperator",
                                                       tokens[i+1].line,
                                                       tokens[i+1].col,
                                                       tokens[i+1].char)
                                    i = len(tokens)
                            else:
                                if (tokens[i].value in DataManager.default_variables):
                                    variable_type = tokens[i].value
                                    variable_name = tokens[i+1].value
                                    try:
                                        if (tokens[i+2].type == "operator"):
                                            if (tokens[i+2].value == "EQ"):
                                                variable_value = tokens[i+3]
                                                self.assign_variable(variable_name,
                                                                     variable_type,
                                                                     variable_value,
                                                                     tokens[i].line,
                                                                     tokens[i].col)
                                                i += 4
                                            else:
                                                errors.raise_error("UnexpectedOperator",
                                                                   tokens[i+2].line,
                                                                   tokens[i+2].col,
                                                                   tokens[i+2].char)
                                                i = len(tokens)
                                        else:
                                            errors.raise_error("UnexpectedType",
                                                               tokens[i+2].line,
                                                               tokens[i+2].col,
                                                               tokens[i+2].type)
                                            i = len(tokens)
                                    except IndexError:
                                        self.assign_variable(variable_name,
                                                             variable_type,
                                                             None,
                                                             tokens[i].line,
                                                             tokens[i].col)
                                        i += 2
                                else:
                                    errors.raise_error("UndefinedItem",
                                                       tokens[i].line,
                                                       tokens[i].col,
                                                       tokens[i].value)
                                    i = len(tokens)
                        elif (tokens[i].type == "operator"):
                            if (tokens[i].value == "AT"):
                                if (tokens[i+1].value == "external"
                                        or tokens[i+1].value == "import"):
                                    if (tokens[i+2].value == "explicit"):
                                        out = Functions(cli_mode=self.cli_mode).call_at_function(
                                            function_name=tokens[i+1].value,
                                            tokens=tokens[i+3:],
                                            explicit=True,
                                            implicit=False)
                                    elif (tokens[i+2].value == "implicit"):
                                        out = Functions(cli_mode=self.cli_mode).call_at_function(
                                            function_name=tokens[i+1].value,
                                            tokens=tokens[i+3:])
                                    else:
                                        out = Functions(cli_mode=self.cli_mode).call_at_function(
                                            function_name=tokens[i+1].value,
                                            tokens=tokens[i+2:])
                                else:
                                    out = Functions(cli_mode=self.cli_mode).call_at_function(
                                        function_name=tokens[i+1].value, tokens=tokens[i+2:])
                                if (out):
                                    print(out)
                                else:
                                    errors.raise_error("UndefinedFunction",
                                                       tokens[i].line,
                                                       tokens[i].col,
                                                       "@{}".format(tokens[i+1].value))
                                i = len(tokens)
                            else:
                                errors.raise_error("UnexpectedOperator",
                                                   tokens[i].line,
                                                   tokens[i].col,
                                                   tokens[i].char)
                                i = len(tokens)
                        else:
                            errors.raise_error("UnexpectedType",
                                               tokens[i].line,
                                               tokens[i].col,
                                               tokens[i].type)
                            i = len(tokens)


class Functions:
    """
    Contains all the builtin functions that can be called from the code
    """

    def __init__(self, cli_mode: bool = False):
        self.cli_mode = cli_mode

    def call_function(self, function_name, tokens):
        pass

    def call_at_function(self,
                         function_name: str,
                         tokens: list,
                         implicit: bool = True,
                         explicit: bool = False) -> list:
        if (function_name in self.at_functions):
            values = Parser(cli_mode=self.cli_mode).parse([tokens], sub_parse=True)
            self.at_functions[function_name](values)
            return [""]
        else:
            return False

    class AtFunctions:
        """
        Contains the @ functions
        """

        def __init__(self):
            pass

        def external(self,
                     values,
                     implicit: bool = True,
                     explicit: bool = False):
            # Todo: Make implicit/explicit do stuff
            for value in values:
                if (value.type == "string"):
                    value.value = value.value[1:-1]
                    if (value.value[0] == "~"):
                        external_directory = os.path.join(os.getcwd(), "externals")
                        file_name = value.value[1:]
                        if (external_directory not in sys.path):
                            sys.path.append(external_directory)
                    else:
                        external_directory, file_name = os.path.split(value.value)
                        if (external_directory not in sys.path):
                            sys.path.append(external_directory)
                    try:
                        imported_module = importlib.import_module(file_name)
                    except ModuleNotFoundError as e:
                        external_name = str(e)[17:-1]
                        errors.raise_error("ExternalNotFound", 0, 0, external_name)
                        return False  # Todo: Raise error
                else:
                    return False  # Todo: Raise error

    functions = {}
    at_functions = {
        "external": AtFunctions().external
    }
