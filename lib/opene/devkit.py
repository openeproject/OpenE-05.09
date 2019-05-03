"""
OpenE Developers Kit
Use this to write custom external modules
"""

from importlib import util
import pip
import socket
import http.client
import sys
from typing import Union

from lib.opene.errors import Errors
from lib.opene.lexer import Token


class DeveloperKit:
    def __init__(self):
        pass

    @staticmethod
    def value_of(item: Token) -> str:
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
                value += DeveloperKit.value_of(current_item)
                if (index + 1 < len(item.value)):
                    value += ", "
            value += "]"
        return value

    @staticmethod
    def install_module(module_name: str,
                       silent: bool = False,
                       additional_args: list = None) -> None:
        pip_arguments = ["install", module_name, "--disable-pip-version-check"]
        if (additional_args):
            for extra_arg in additional_args:
                pip_arguments.append(extra_arg)
        if (silent):
            pass  # Todo: add option to silence pip outputs
        print(pip_arguments)
        pip.main(pip_arguments)

    @staticmethod
    def require_python_module(module_name: str,
                              install_if_not_found: bool = True,
                              pip_install_name: str = None,
                              silence_all: bool = False,
                              silence_connection_check: bool = False,
                              silence_pip: bool = False,
                              pip_args: list = None):
        if (not pip_install_name):
            pip_install_name = module_name
        silence_connection_check = (silence_all or silence_connection_check)

        def decorator(function):
            def wrapper(*args, **kwargs):
                # Check to see if module is already installed
                module_spec = util.find_spec(module_name)
                found = module_spec is not None
                if (not found):
                    if (install_if_not_found):
                        has_connection = DeveloperKit.can_connect(url="files.pythonhosted.org",
                                                                  timeout=5,
                                                                  silence_exceptions=silence_connection_check)
                        if (has_connection):
                            DeveloperKit.install_module(pip_install_name, silence_pip, pip_args)
                        else:
                            if (not silence_all):
                                print("Error: Could to connect to 'files.pythonhosted.org'")
                                sys.exit()
                result = function(*args, **kwargs)
                return result
            return wrapper
        return decorator

    @staticmethod
    def can_connect(url: str,
                    timeout: int = 5,
                    silence_exceptions: bool = False) -> bool:
        connection = http.client.HTTPConnection(url, timeout=timeout)
        try:
            connection.request("HEAD", "/")
            connection.close()
            return True
        except (socket.error,
                socket.herror,
                socket.gaierror,
                socket.timeout,
                http.client.HTTPException,
                http.client.NotConnected,
                http.client.InvalidURL,
                http.client.UnknownProtocol,
                http.client.UnknownTransferEncoding,
                http.client.UnimplementedFileMode,
                http.client.IncompleteRead,
                http.client.ImproperConnectionState,
                http.client.CannotSendRequest,
                http.client.CannotSendHeader,
                http.client.ResponseNotReady,
                http.client.BadStatusLine,
                http.client.LineTooLong,
                http.client.RemoteDisconnected) as e:
            if (not silence_exceptions):
                print(e)
            connection.close()
            return False


class ExternalModule:

    functions = {}

    def __init__(self,
                 errors: Errors = None) -> None:
        self.errors = errors

    def parse(self,
              function_name: str,
              parameters: list = None) -> dict:
        return_values = {
            "ran": False,
            "i_increment": 0,
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
                    self.errors.raise_error("IncorrectParameterQuantity", 0, 0, function_name)
            elif (type(expected_parameters) == str):
                if (expected_parameters[-1] == "+"):
                    if (expected_parameters[-2] == "="):
                        if (len(parameters) >= int(expected_parameters[:-2])):
                            call_function = True
                        else:
                            self.errors.raise_error("IncorrectParameterQuantity", 0, 0, function_name)
                    else:
                        if (len(parameters) > int(expected_parameters[:-1])):
                            call_function = True
                        else:
                            self.errors.raise_error("IncorrectParameterQuantity", 0, 0, function_name)
                elif (expected_parameters[-1] == "-"):
                    if (expected_parameters[-2] == "="):
                        if (len(parameters) <= int(expected_parameters[:-2])):
                            call_function = True
                        else:
                            self.errors.raise_error("IncorrectParameterQuantity", 0, 0, function_name)
                    else:
                        if (len(parameters) < int(expected_parameters[:-1])):
                            call_function = True
                        else:
                            self.errors.raise_error("IncorrectParameterQuantity", 0, 0, function_name)
            if (call_function):
                data_out = callable_function(parameters)
                return_values["ran"] = True
                return_values["returned_data"] = data_out
        return return_values

    def add_function(self, function_name: str, expected_parameters: Union[int, str], function_call: callable) -> None:
        self.functions[function_name] = [expected_parameters, function_call]
