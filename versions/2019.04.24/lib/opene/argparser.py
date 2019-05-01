import hashlib
import json
import os
import sys

from Cryptodome.Cipher import AES


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
                            function_arguments = list(
                                "\"{}\"".format(x) for x in parsed_values[found_argument]["values"]
                            )
                            exec(details["function"].replace("%args%", ", ".join(map(str, function_arguments))))
                            # exec(details["function"].replace("%args%", ", ".join(map(str, details[""]))))
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

        def help(self):
            try:
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

    class HB:
        """
        This is a random easter egg
        If you read the source code then you'll probably be able to guess what it does
        """
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

    class Flower:
        """
        This is a stupid thing I wanted to add
        There's a reason the file it reads is encrypted
        I really have no idea why I added this but I did anyways
        """
        def __init__(self):
            pass

        def flower(self, *argv):
            given_key = bytes(hashlib.md5(argv[0].encode("utf-8")).hexdigest(), "utf-8")
            data_to_decrypt = open("./lib/opene/flower.bin", "rb").read()
            x = self.decrypt(given_key, data_to_decrypt)
            print(x)

        def rewrite_file(self, key):
            key = bytes(hashlib.md5(key.encode("utf-8")).hexdigest(), "utf-8")
            unencrypted_data = open("./lib/opene/to_encrypt.txt", "r").read()
            encrypted_data = self.encrypt(key, unencrypted_data)
            f = open("./lib/opene/flower.bin", "wb+")
            f.write(encrypted_data)
            f.close()

        def pad(self,
                data: str,
                block_size: int = 16,
                padding: str = "{"):
            return data + (block_size - len(data) % block_size) * padding

        def encrypt(self,
                    key: bytes,
                    data: str,
                    iv: bytes = bytes(("0" * 16).encode("utf-8"))):
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            return cipher.encrypt(bytes(self.pad(data), "utf-8"))

        def decrypt(self,
                    key: bytes,
                    data: bytes,
                    iv: bytes = bytes(("0" * 16).encode("utf-8"))):
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            temp = cipher.decrypt(data)
            return temp.decode("utf-8", errors="ignore").rstrip("{")

