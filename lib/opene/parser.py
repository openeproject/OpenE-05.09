import importlib
import os
import sys

from deprecated.sphinx import deprecated
from deprecated.sphinx import versionadded

from lib.opene.devkit import ExternalModule
from lib.opene.errors import Errors
from lib.opene.lexer import Token


errors = Errors(error_file_location="./lib/json/errors.json",
                this_location=os.getcwd())


class DataManager:
    """
    This class stores all the values that a user defines in their code, such as variables, classes, imports and other
    """

    external_files = []
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

    def __init__(self, cli_mode: bool = False, output_file: str = False):
        self.cli_mode = cli_mode
        self.output_location = output_file
        global errors
        errors = Errors(cli_mode=cli_mode,
                        error_file_location="./lib/json/errors.json",
                        this_location=os.getcwd())

    @deprecated(version="2019.04.30", reason="Replaced by 'assign_variable_new'")
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

    @versionadded(version="2019.04.30", reason="Replaces 'assign_variable'")
    def assign_variable_new(self,
                            variable_name: str,
                            variable_type: str,
                            variable_values: list = None,
                            line_number: int = 0,
                            col_number: int = 0,
                            current_class: str = None):
        if (variable_type == "int"):
            variable_type = "integer"  # Allow shorthand int instead of integer, even though they're the same
        if (current_class):
            pass
        else:
            if (variable_values):
                if (len(variable_values) == 1):
                    value = variable_values[0]
                    if (value.type == "command"):  # variable = variable
                        if (value.value in DataManager.global_variables):
                            value = DataManager.global_variables[value.value]
                            if (value.type in DataManager.accepted_variable_types[variable_type]):
                                if (variable_type == "sum"):
                                    value.value = str(eval(value.value)).rstrip(".0")
                                elif (variable_type == "integer"):
                                    value.value = str(int(eval(value.value)))
                                elif (variable_type == "float"):
                                    value.value = str(float(eval(value.value)))
                                DataManager.global_variables[variable_name] = Token(variable_type,
                                                                                    value.value,
                                                                                    line_number,
                                                                                    col_number)
                            else:
                                errors.raise_error("UnexpectedVariableType", value.line, value.col, value.type)
                        else:
                            errors.raise_error("UndefinedVariable", value.line, value.col, value.value)
                    else:
                        if (value.type in DataManager.accepted_variable_types[variable_type]):
                            if (variable_type == "sum"):
                                value.value = str(eval(value.value)).rstrip(".0")  # Remove trailing .0 from decimal
                            elif (variable_type == "integer"):
                                value.value = str(int(eval(value.value)))
                            elif (variable_type == "float"):
                                value.value = str(float(eval(value.value)))
                            DataManager.global_variables[variable_name] = Token(variable_type,
                                                                                value.value,
                                                                                line_number,
                                                                                col_number)
                        else:
                            errors.raise_error("UnexpectedVariableType", value.line, value.col, variable_name, value.type)
                else:
                    if (variable_values[0].type == "operator"):
                        if (variable_values[0].value == "OS"):
                            open_square_brackets = 0
                            i = 0
                            current_list = []
                            while i < len(variable_values[1:]):
                                current_item = variable_values[i+1]
                                if (current_item.type == "operator"):
                                    if (current_item.value == "CM"):
                                        if (variable_values[i].type == "operator"):
                                            errors.raise_error("UnexpectedOperator",
                                                               variable_values[i].line,
                                                               variable_values[i].col,
                                                               variable_values[i].char)
                                        else:
                                            current_list.append(variable_values[i])
                                    elif (current_item.value == "OS"):
                                        open_square_brackets += 1
                                    elif (current_item.value == "CS"):
                                        if (open_square_brackets > 0):
                                            open_square_brackets -= 1
                                        else:
                                            if (variable_values[i].type != "operator"):  # Item immediately before
                                                current_list.append(variable_values[i])
                                            value = current_list
                                            current_list = []
                                    else:
                                        errors.raise_error("UnexpectedOperator",
                                                           current_item.line,
                                                           current_item.col,
                                                           current_item.char)
                                        i = len(variable_values[i:])
                                    i += 1
                                else:
                                    i += 1
                            # Todo: Work on lists, and improve them
                            DataManager.global_variables[variable_name] = Token("list", value, line_number, col_number)
                        elif (variable_values[0].value == "OC"):
                            pass
                        elif (variable_values[0].value == "OB"):
                            pass
                        else:
                            errors.raise_error("UnexpectedOperator",
                                               variable_values[0].line,
                                               variable_values[0].col,
                                               variable_values[0].char)
                    else:
                        function_name = variable_values[0].value
                        value = Functions(cli_mode=self.cli_mode).call_function(function_name,
                                                                                variable_values[2:-1])
                        if (value):
                            try:
                                if (value.type in DataManager.accepted_variable_types[variable_type]):
                                    if (type(value) == list):
                                        value = value[0]
                                    if (variable_type == "sum"):
                                        value.value = str(eval(value.value)).rstrip(".0")
                                    elif (variable_type == "integer"):
                                        value.value = str(int(eval(value.value)))
                                    elif (variable_type == "float"):
                                        value.value = str(float(eval(value.value)))
                                    DataManager.global_variables[variable_name] = Token(variable_type,
                                                                                        value.value,
                                                                                        line_number,
                                                                                        col_number)
                            except KeyError:
                                if (variable_type == value.type):
                                    DataManager.global_variables[variable_name] = Token(variable_type,
                                                                                        value.value,
                                                                                        line_number,
                                                                                        col_number)
                                else:
                                    errors.raise_error("UnexpectedVariableType",
                                                       value.line,
                                                       value.col,
                                                       variable_name,
                                                       value.type)
                        else:
                            errors.raise_error("UndefinedFunction",
                                               variable_values[0].line,
                                               variable_values[0].col,
                                               function_name)
            else:
                variable_value = DataManager.default_variables[variable_type]
                DataManager.global_variables[variable_name] = Token(variable_type,
                                                                    variable_value.value,
                                                                    line_number,
                                                                    col_number)

    def value_of(self, item: Token) -> str:
        value = ""
        if (item.type == "Empty"
                or item.type == "integer"
                or item.type == "float"
                or item.type == "sum"):
            value = item.value
        elif (item.type == "string"):
            value = item.value[1:-1]
        elif (item.type == "list"):
            value = "["
            for index, current_item in enumerate(item.value):
                value += self.value_of(current_item)
                if (index+1 < len(item.value)):
                    value += ", "
            value += "]"
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
            elif (variable_value.type == "list"):
                value_to_return = ""
                value_to_return += "["
                for index, item in enumerate(variable_value.value):
                    value_to_return += item.value
                    if (index+1 < len(variable_value.value)):
                        value_to_return += ", "
                value_to_return += "]"
                return value_to_return
            elif (variable_value.type == "matrix"):
                x_size = len(variable_value.value[0])
                y_size = len(variable_value.value)
                # Todo: More efficient method of getting longest item
                longest_items = {}
                for row in variable_value.value:
                    for column_number, item in enumerate(row):
                        try:
                            # Todo: Convert to string before len() comparison
                            if (len(item.value) > longest_items[column_number]):
                                longest_items[column_number] = len(item.value)
                        except KeyError:
                            longest_items[column_number] = len(item.value)
                value_to_return = "Matrix[{},{}]:\n".format(x_size, y_size)
                for row_number, row_content in enumerate(variable_value.value):
                    value_to_return += "[{}] \t".format(row_number)
                    for column_number, item in enumerate(row_content):
                        value = self.value_of(item)
                        value_to_return += value
                        value_to_return += " " * (longest_items[column_number] - len(value)) + "\t"
                    value_to_return += "\n"
                return value_to_return
        except KeyError:
            return False

    def parse(self,
              lines: list,
              sub_parse: bool = False):
        if (sub_parse):
            values = []
            current_value = None
            error_raised = False
            for tokens in lines:
                i = 0
                if (type(tokens) == Token):
                    tokens = [tokens]
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
                        if (tokens[i].type == "operator"):
                            if (tokens[i].value == "CM"):
                                values.append(current_value)
                                current_value = None
                                i += 1
                            else:
                                errors.raise_error("UnexpectedOperator",
                                                   tokens[i].line,
                                                   tokens[i].col,
                                                   tokens[i].char)
                                i = len(tokens)
                                error_raised = True
                        elif (tokens[i].type == "command"):
                            try:
                                if (tokens[i+1].type == "operator"):
                                    if (tokens[i+1].value == "OB"):
                                        function_name = tokens[i].value
                                        function_out = Functions(cli_mode=self.cli_mode).call_function(function_name,
                                                                                                       tokens[i+2:-1])
                                        if (type(function_out) == list):
                                            function_out = function_out[0]
                                        current_value = function_out
                                        i += len(tokens[i+1:]) + 1
                                    elif (tokens[i+1].value == "CM"):
                                        variable_name = tokens[i].value
                                        if (variable_name in DataManager.global_variables):
                                            current_value = DataManager.global_variables[variable_name]
                                            i += 1
                                        else:
                                            errors.raise_error("UndefinedVariable",
                                                               tokens[i].line,
                                                               tokens[i].col,
                                                               tokens[i].value)
                                            i = len(tokens)
                                            error_raised = True
                                    else:
                                        errors.raise_error("UnexpectedOperator",
                                                           tokens[i].line,
                                                           tokens[i].col,
                                                           tokens[i+1].char)
                                        i = len(tokens)
                                        error_raised = True
                                else:
                                    pass
                            except IndexError:
                                variable_name = tokens[i].value
                                if (variable_name in DataManager.global_variables):
                                    current_value = DataManager.global_variables[variable_name]
                                    i += 1
                                else:
                                    errors.raise_error("UndefinedVariable",
                                                       tokens[i].line,
                                                       tokens[i].col,
                                                       tokens[i].value)
                                    i = len(tokens)
                                    error_raised = True
                        elif (tokens[i].type == "string"
                                or tokens[i].type == "sum"):
                            current_value = tokens[i]
                            i += 1
                if (current_value):  # Add the last value (if there is one), even without a comma
                    values.append(current_value)
                return {"values": values, "i_increment": i, "error_raised": error_raised}
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
                                variable_value = self.debug_variable(tokens[i].value)
                                if (variable_value):
                                    data_out = "{} <- {}".format(tokens[i].value, self.debug_variable(tokens[i].value))
                                    print(data_out)
                                    if (self.output_location):
                                        output_file = open(self.output_location, "a+")
                                        output_file.write(data_out)
                                        output_file.close()
                                else:
                                    errors.raise_error("UndefinedVariable",
                                                       tokens[i].line,
                                                       tokens[i].col,
                                                       tokens[i].value)
                                    i = len(tokens)
                            elif (tokens[i].value in DataManager.imported_modules):
                                pass
                            elif (tokens[i].value in DataManager.external_files):
                                print("External Module: {} (imported)".format(tokens[i].value))
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
                                    function_out = Functions(cli_mode=self.cli_mode).call_function(tokens[i].value,
                                                                                                   tokens[i+2:-1])
                                    if (not function_out):
                                        errors.raise_error("UndefinedFunction",
                                                           tokens[i].line,
                                                           tokens[i].col,
                                                           tokens[i].value)
                                    i = len(tokens)
                                elif (tokens[i+1].value == "EQ"):
                                    variable_name = tokens[i].value
                                    if (variable_name in DataManager.global_variables):
                                        variable_value = tokens[i+2]
                                        try:
                                            if (tokens[i+3].type == "operator"):
                                                if (tokens[i+3].value == "OB"):
                                                    # variable_value = Functions().call_function(variable_value.value,
                                                    #                                            tokens[i+4:-1])
                                                    # i = len(tokens)
                                                    self.assign_variable_new(variable_name,
                                                                             DataManager.global_variables[
                                                                                 variable_name].type,
                                                                             tokens[i+2:])
                                                else:
                                                    errors.raise_error("UnexpectedOperator",
                                                                       tokens[i+3].line,
                                                                       tokens[i+3].col,
                                                                       tokens[i+3].char)
                                                i = len(tokens)
                                        except IndexError:
                                            pass
                                        i = len(tokens)
                                        # Todo: Replace this old function with the new one
                                        # self.assign_variable(variable_name,
                                        #                      DataManager.global_variables[variable_name].type,
                                        #                      variable_value)
                                        i += 3
                                    else:
                                        errors.raise_error("UndefinedVariable",
                                                           tokens[i].line,
                                                           tokens[i].col,
                                                           variable_name)
                                        i = len(tokens)
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
                                                # variable_value = tokens[i+3]
                                                # i_increment = 0
                                                # try:
                                                #     if (tokens[i+4].type == "operator"):
                                                #         if (tokens[i+4].value == "OB"):
                                                #             variable_value = Functions().call_function(
                                                #                 variable_value.value,
                                                #                 tokens[i+5:-1]
                                                #             )
                                                #             i_increment = len(tokens[i+4:])
                                                #         else:
                                                #             errors.raise_error("UnexpectedOperator",
                                                #                                tokens[i+3].line,
                                                #                                tokens[i+3].col,
                                                #                                variable_value.value)
                                                #             i = len(tokens)
                                                # except IndexError:
                                                #     pass
                                                self.assign_variable_new(variable_name,
                                                                         variable_type,
                                                                         tokens[i+3:],
                                                                         tokens[i].line,
                                                                         tokens[i].col)
                                                i = len(tokens)
                                                # if (variable_value):
                                                #     self.assign_variable(variable_name,
                                                #                          variable_type,
                                                #                          variable_value,
                                                #                          tokens[i].line,
                                                #                          tokens[i].col)
                                                # i += 4 + i_increment
                                                # else:
                                                #     errors.raise_error("UndefinedFunction",
                                                #                        tokens[i+3].line,
                                                #                        tokens[i+3].col,
                                                #                        tokens[i+3].value)
                                                #     i = len(tokens)
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
                                        self.assign_variable_new(variable_name,
                                                                 variable_type,
                                                                 None,
                                                                 tokens[i].line,
                                                                 tokens[i].col)
                                        # self.assign_variable(variable_name,
                                        #                      variable_type,
                                        #                      None,
                                        #                      tokens[i].line,
                                        #                      tokens[i].col)
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
                                    pass
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
        self.functions["Matrix"] = self.create_matrix
        self.functions["change"] = self.change
        self.functions["zeros"] = self.zeros

    def call_function(self,
                      function_name: str,
                      tokens: list,
                      existing_parser: Parser.parse = None,
                      errors: Errors = errors):
        values = Parser(cli_mode=self.cli_mode).parse([tokens], sub_parse=True)["values"]
        function_out = {
            "returned_data": None
        }
        if (function_name in self.functions):
            function_out = {
                "returned_data": False
            }
            function_out = self.functions[function_name](values)
            try:
                if (function_out["returned_data"]):
                    return function_out["returned_data"]
                else:
                    return Token("Empty", "Empty")
            except TypeError:  # If the function does not return
                return Token("Empty", "Empty")
        else:
            if (len(DataManager.external_files) > 0):
                ran_external = False
                for external_file in DataManager.external_files:
                    if (not ran_external):
                        function_out = external_file.ExternalParser(errors=errors).parse(function_name=function_name,
                                                                                         parameters=values)
                        if (function_out["ran"]):
                            ran_external = True
                if (ran_external):
                    # print(function_out)
                    return function_out["returned_data"]
                else:
                    return False
            else:
                return False


    def call_at_function(self,
                         function_name: str,
                         tokens: list,
                         implicit: bool = True,
                         explicit: bool = False) -> list:
        if (function_name in self.at_functions):
            values = Parser(cli_mode=self.cli_mode).parse([tokens], sub_parse=True)["values"]
            self.at_functions[function_name](values)
            return [""]
        else:
            return False

    @staticmethod
    def create_matrix(parameters: list = None) -> dict:
        x_size = 0
        y_size = 0
        if (len(parameters) == 0):
            pass  # Todo: Raise error
        elif (len(parameters) == 1):
            size = int(Parser().value_of(parameters[0]))
            x_size = size
            y_size = size
        elif (len(parameters) == 2):
            x_size = int(Parser().value_of(parameters[0]))
            y_size = int(Parser().value_of(parameters[1]))
        created_matrix = [[Token("integer", "0") for x in range(x_size)] for y in range(y_size)]
        return {"returned_data": Token("matrix", created_matrix)}

    @staticmethod
    def change(parameters: list = None) -> dict:
        data = parameters[0]
        if (data.type == "matrix"):
            x_pos = int(Parser().value_of(parameters[1]))
            y_pos = int(Parser().value_of(parameters[2]))
            data.value[y_pos][x_pos] = parameters[3]
        return {"returned_data": Token("matrix", data.value)}

    @staticmethod
    def zeros(parameters: list = None) -> dict:
        if (len(parameters) == 1):  # If size is based on existing matrix
            data = parameters[0]
            if (data.type == "matrix"):
                y_size = len(data.value)
                x_size = len(data.value[0])
            elif (data.type in ["sum", "integer", "float"]):
                new_size = int(eval(data.value))
                x_size = new_size
                y_size = new_size
            else:
                return False
                pass  # Todo: Raise error
            created_matrix = [[Token("integer", "0") for x in range(x_size)] for y in range(y_size)]
            return {"returned_data": Token("matrix", created_matrix)}
        elif (len(parameters) == 2):
            x_size = parameters[0]
            y_size = parameters[1]
            if (x_size.type in ["sum", "integer", "float"]
                    and y_size.type in ["sum", "integer", "float"]):
                x_size = int(eval(x_size.value))
                y_size = int(eval(y_size.value))
                created_matrix = [[Token("integer", "0") for x in range(x_size)] for y in range(y_size)]
                return {"returned_data": Token("matrix", created_matrix)}
            else:
                pass  # Todo: Raise error
        else:
            pass  # Todo: Raise error

    class AtFunctions:
        """
        Contains the @ functions
        """

        def __init__(self):
            pass

        @staticmethod
        def external(values,
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
                        if (hasattr(imported_module, "ExternalParser")):
                            if (issubclass(imported_module.ExternalParser, ExternalModule)):
                                DataManager.external_files.append(imported_module)
                            else:
                                errors.raise_error(
                                    "DeveloperError", 0, 0,
                                    "The external module '{}'".format(os.path.join(external_directory, file_name))
                                    + " has the class 'ExternalParser' but it is not a subclass of 'devkit.ExternalParser'")
                                return False
                        else:
                            errors.raise_error(
                                "DeveloperError", 0, 0,
                                "The external module '{}' does not have the required class 'ExternalParser'".format(
                                    os.path.join(external_directory, file_name)
                                )
                            )
                            return False
                    except ModuleNotFoundError as e:
                        external_name = str(e)[17:-1]
                        errors.raise_error("ExternalNotFound", 0, 0, external_name)
                        return False
                else:
                    return False  # Todo: Raise error

        @staticmethod
        def version(values):
            """
            So originally I was going to put a to do here but I decided not to.
            I don't think I want '@version' to do anything, but rather be a note to the author or anyone else instead.
            It's particularly useful for me, as I have a lot of test files and I want to know when they're all from
            """
            pass

    functions = {}
    at_functions = {
        "external": AtFunctions.external,
        "version": AtFunctions.version
    }
