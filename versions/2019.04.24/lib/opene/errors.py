import json
import os
import sys


class Errors:

    error_file_location = None
    this_location = None
    location = None
    errors = {}

    def __init__(self,
                 error_file_location: str = "errors.json",
                 this_location: str = None) -> None:
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
                    *argv) -> None:
        pass
