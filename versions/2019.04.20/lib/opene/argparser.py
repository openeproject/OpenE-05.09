import json
import os
import sys

import pprint


class ArgumentParser:

    argument_file_location = None
    this_location = None
    location = None

    def __init__(self, argument_file_location: str = "arguments.json", this_location: str = None) -> None:
        """
        Setup the custom argument parser for OpenE

        :param argument_file_location: This is the relative location of the file. It is added to this_location
        :param this_location: This is the os.getcwd() value of the opene.py file (usually) although it can be changed
        """
        if (argument_file_location):
            self.argument_file_location = argument_file_location
        else:
            print("Error: No parameter specified for 'argument_file_location'")
        try:
            if (os.path.exists(this_location)):
                self.this_location = this_location
            else:
                print("Error: The file '{}' does not exist".format(this_location))
        except TypeError:
            print("Error: No parameter specified for 'this_location'")
        if (self.argument_file_location and self.this_location):
            location = os.path.join(self.this_location, self.argument_file_location)
            if (os.path.exists(location)):
                self.location = location
            else:
                print("Error: The file '{}' does not exist".format(location))

    def parse_arguments(self, argv: list) -> dict:
        """
        Get a dict of the sys.argv arguments parsed

        :param argv: The sys.argv values that the program is run with
        :return: A dict of parsed arguments and their values
        """
        try:
            argument_dict = json.load(open(self.location, "r"))
        except FileNotFoundError as e:
            error_location = str(e)[38:-1]
            print("Error: The file '{}' could not be found".format(error_location))
            sys.exit()
        except json.decoder.JSONDecodeError as e:
            print("JSON Error (from file '{}'): {}".format(self.location, e))
            sys.exit()
        argv = argv[1:]  # Remove the first item from the argv as it is the Python file location

        i = 0
        parsed_values = {}
        while i < len(argv):
            current_argument = argv[i]
            found_argument = False
            this_argument_values = []
            for name, details in argument_dict.items():
                if (not found_argument):
                    if (details["case_sensitive"]):
                        if (current_argument in details["arguments"]):
                            found_argument = name
                    else:
                        if (current_argument.upper() in [x.upper() for x in details["arguments"]]):
                            found_argument = name
                    if (found_argument):
                        this_argument_values = argv[i+1:i+1+details["expected_values"]]
                        parsed_values[found_argument] = {"values": this_argument_values}
                        i += 1+details["expected_values"]
                        try:
                            exec(details["function"])
                        except KeyError:
                            pass
            if (not found_argument):
                print("Error: The argument '{}' is not recognised".format(argv[i]))
                sys.exit()

        return parsed_values


class Functions:
    def __init__(self):
        pass

    class Help:
        def __init__(self):
            pass

        def help(self):
            print("Help functions")

    class HB:
        def __init__(self):
            pass

        def hb(self):
            print("I miss the person I could talk to about anything at any given time.")
            print("I miss being able to be goofy and be 100% myself around you all the time.")
            print("I miss having you there for me when no one else would even understand.")
            print("I miss dancing together.")
            print("I miss losing ourselves in each other and forgetting the rest of the world even existed.")
            print("I miss loving you more than I loved anyone else.")
            print("I miss talking to you and hearing your soothing voice.")
            print("I miss hearing about your day and being proud of what you do.")
            print("I miss telling everyone how madly in love I was with you.")
            print("I miss planning non stop adventures together.")
            print("I have many amazing friends but none of them resemble my bond with you...")
            print("I miss my best friend")
            print("\tWritten by u/CalogeroS")
            print("\tSorry for that. I'm kinda going through some stuff right now :(")
            print(("=" * 64) + "\n")
            # Source: https://www.reddit.com/r/BreakUp/comments/bef6jl/i_miss/
