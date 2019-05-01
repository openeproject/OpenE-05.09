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
    default_variables = {
        "*": Token("Empty", "Empty"),
        "string": Token("string", "\"\""),
        "sum": Token("sum", "0"),
        "integer": Token("integer", "0"),
        "float": Token("float", "0.0"),
        "boolean": Token("boolean", "false"),
        "list": Token("list", [])
    }


class Parser:
    """
    This is the main parser class
    External modules should extend it in the future, when it is slightly better made
    """

    def __init__(self):
        pass

    def parse(self,
              lines: list,
              sub_parse: bool = False):
        if (sub_parse):
            pass
        else:
            for tokens in lines:
                i = 0
                while i < len(tokens):
                    if (tokens[i].type == "command"):
                        if (tokens[i+1].type == "operator" and
                                tokens[i+1].value == "OB"):
                            pass
                        else:
                            errors.raise_error("UnexpectedOperator", tokens[i+1].line, tokens[i+1].col)
                    print(tokens[i].type)
                    i += 1
