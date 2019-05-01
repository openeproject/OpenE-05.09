import os
import sys

from lib.opene.lexer import Lexer
from lib.opene.parser import Parser


class File:
    """
    This is the lexer and parser for files
    """
    def __init__(self,
                 debug_mode: bool = False,
                 parse_mode: bool = False,
                 output_file: str = None,
                 base_directory: str = None):
        """
        Used to set up the File class

        :param debug_mode: Whether to be in debug mode or not
        :param parse_mode: Should the tokens be parsed if in debug mode
        :param output_file: The location to output to (if data is being outputted)
        """
        self.debug_mode = debug_mode
        self.parse_mode = parse_mode
        self.output_file = output_file
        self.base_directory = base_directory

    def main(self, file_location: str):
        if (os.path.exists(os.path.join(self.base_directory, file_location))):
            file_location = os.path.join(self.base_directory, file_location)
        try:
            file_data = open(file_location).read()
        except FileNotFoundError as e:
            error_location = str(e)[38:-1]
            print("Error: The file '{}' could not be found".format(error_location))
            sys.exit()
        tokens = Lexer().tokenise(file_data)
        if (self.debug_mode):
            print(tokens)
        if ((self.parse_mode) or not self.debug_mode):
            Parser().parse(tokens)
