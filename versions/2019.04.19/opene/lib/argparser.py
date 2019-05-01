import os


class ArgumentParser:

    argument_file_location = None
    this_location = None
    location = None

    def __init__(self, argument_file_location: str = "arguments.json", this_location: str = None):
        if (os.path.exists(self.argument_file_location)):
            self.argument_file_location = argument_file_location
        else:
            print("Error: The file '{}' does not exist".format(argument_file_location))
        if (os.path.exists(self.this_location)):
            self.this_location = this_location
        else:
            print("Error: The file '{}' does not exist".format(this_location))
        if (self.argument_file_location and self.this_location):
            self.location = os.path.join(self.this_location, self.argument_file_location)

    def parse_arguments(self, argv: list) -> dict:
        pass
