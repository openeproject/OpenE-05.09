from opene import lexer


class CLI:
    def __init__(self, prompt: str = "OpenE> ", debug: bool = False):
        self.prompt = prompt
        self.debug = debug

    def mainloop(self, debug: bool = False):
        user_input = input(self.debug)
        tokens = lexer.Lexer().tokenise(user_input)
        if (debug or self.debug):
            print(tokens)
