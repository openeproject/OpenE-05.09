from lib.opene.lexer import Lexer
from lib.opene.parser import Parser


class CLI:
    """
    This is the main CLI (command line interface class)
    It follows a simple REPL (Read Evaluate Print Loop)
    """
    def __init__(self,
                 prompt: str = "OpenE> ",
                 debug_mode: bool = False,
                 parse_mode: bool = False,
                 output_file: str = False):
        """
        Used to set up the CLI class

        :param prompt: The value at the beginning of the line, to prompt the user to enter something
        :param debug_mode: Whether to be in debug mode or not
        :param parse_mode: Should the tokens be parsed if in debug mode
        :param output_file: The location to output to (if data is being outputted)
        """
        self.prompt = prompt
        self.debug_mode = debug_mode
        self.parse_mode = parse_mode
        self.output_location = output_file

    def mainloop(self):
        should_run = True
        while should_run:
            user_input = input(self.prompt)
            tokens = Lexer().tokenise(user_input)
            if (self.debug_mode):
                print(tokens)
            if ((self.parse_mode) or not self.debug_mode):
                Parser(cli_mode=True).parse(tokens)

