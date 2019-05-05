import json
import os
import sys


argument_json_location = None


class ArgumentParser:

    argument_file_location = None
    this_location = None
    location = None

    def __init__(self,
                 argument_file_location: str = "arguments.json",
                 this_location: str = None) -> None:
        """
        Setup the custom argument parser for OpenE

        :param argument_file_location: This is the relative location of the file. It is added to this_location
        :param this_location: This is the os.getcwd() value of the opene.py file (usually) although it can be changed
        """
        global argument_json_location
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
                argument_json_location = location
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
                            function_arguments = list(
                                "\"{}\"".format(x) for x in parsed_values[found_argument]["values"]
                            )
                            exec(details["function"].replace("%args%", ", ".join(map(str, function_arguments))))
                        except KeyError:
                            pass
            if (not found_argument):
                print("Error: The argument '{}' is not recognised".format(argv[i]))
                sys.exit()

        return parsed_values


class Functions:
    """
    All the functions that can be called from an argument should be placed in this class
    They can be in subclasses, such as the Help class below
    """
    def __init__(self):
        pass

    class Help:
        """
        This class gives the user help with the potential launch arguments
        """
        def __init__(self):
            pass

        # noinspection PyMethodMayBeStatic
        def help(self):
            try:
                # noinspection PyTypeChecker
                argument_dict = json.load(open(argument_json_location, "r"))
                print("Help Functions:")
                for argument, details in argument_dict.items():
                    show_argument = True
                    try:
                        if (details["hide_in_help"]):
                            show_argument = False
                    except KeyError:
                        pass
                    if (show_argument):
                        print("{}: {}".format(argument, ", ".join(map(str, details["arguments"]))))
                        try:
                            if (len(details["description"]) > 0):
                                print("\t{}".format(details["description"].replace("\n", "\n\t")))
                        except KeyError:
                            pass
            except TypeError:
                pass
