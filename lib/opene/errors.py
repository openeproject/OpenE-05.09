import json
import os
import sys


class Errors:

    error_file_location = None
    this_location = None
    location = None
    errors = {}

    def __init__(self,
                 cli_mode: bool = False,
                 error_file_location: str = "errors.json",
                 this_location: str = None) -> None:
        self.cli_mode = cli_mode
        if (error_file_location):
            self.error_file_location = error_file_location
        else:
            print("Error: No parameter specified for 'error_file_location'")
        try:
            if (os.path.exists(this_location)):
                self.this_location = this_location
            else:
                print("Error: The file '{}' does not exist".format(this_location))
        except TypeError:
            print("Error: No parameter specified for 'this_location'")
        if (self.error_file_location and self.this_location):
            location = os.path.join(self.this_location, self.error_file_location)
            if (os.path.exists(location)):
                self.location = location
                try:
                    self.errors = json.load(open(self.location, "r"))
                except json.decoder.JSONDecodeError as e:
                    print("JSON Error (from file '{}'): {}".format(self.location, e))
                    sys.exit()
            else:
                print("Error: The file '{}' does not exist".format(location))

    def raise_error(self,
                    error_name: str,
                    line_number: int = 0,
                    col_number: int = 0,
                    *argv) -> bool:
        """

        :param error_name:
        :param line_number:
        :param col_number:
        :param argv:
        :return: This function generally doesn't return, but when it does, it just returns a bool
        """
        if (error_name in self.errors):
            error_message = "{}: {}".format(self.errors[error_name]["error_type"],
                                            self.errors[error_name]["error_text"].format(*argv))
            if (line_number > 0 and col_number > 0):
                error_message += "\n[{}:{}]".format(line_number, col_number)
            print(error_message)
            if (self.errors[error_name]["exit_after"]):
                if (self.cli_mode):
                    return False
                else:
                    sys.exit()
        else:
            developer_error = "DeveloperError"
            if (developer_error in self.errors):
                self.raise_error(developer_error,
                                 line_number,
                                 col_number,
                                 "The error '{}' is not defined in the error file".format(error_name))
                sys.exit()
            else:
                raise KeyError("The error type '{}' could not be find the in the error file".format(developer_error))
