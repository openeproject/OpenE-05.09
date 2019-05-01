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
                            variable_value = str(int(eval(variable_value.value)))
                        elif (variable_type == "float"):
                            variable_value = str(float(eval(variable_value.value)))
                    else:
                        errors.raise_error("UnexpectedVariableType", 0, 0, variable_name, variable_value.type)
            else:
                variable_value = DataManager.default_variables[variable_type]
            DataManager.global_variables[variable_name] = Token(variable_type,
                                                                variable_value,
                                                                line_number,
                                                                col_number)

    def value_of(self, item: Token) -> str:
        value = ""
        if (item.type == "string"):
            return item.value[1:-1]
        return value

    def parse(self,
              lines: list,
              sub_parse: bool = False):
        if (sub_parse):
            pass
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
                                                        DataManager.global_variables[tokens[i].value].value))
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
                                pass
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

    functions = {}
    at_functions = {}

    def __init__(self):
        pass
