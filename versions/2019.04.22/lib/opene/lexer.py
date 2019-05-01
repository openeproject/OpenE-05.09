class Traceback:
    line = 0
    col = 0


class Token:
    def __init__(self,
                 _type: str,
                 value: str,
                 line: int = 0,
                 col: int = 0,
                 char: str = None):
        """
        :param _type: The type of token
        :param value: The value of the token
        :param line: The current line number
        :param col: The starting col number
        :param char: The character being represented (if type is 'operator')
        """
        self.type = _type
        self.value = value
        self.line = line
        self.col = col
        self.char = char


class Lexer:
    def __init__(self):
        pass

    def tokenise(self, data) -> list:
        stop_characters = list(" \n\t\"")
        replace_characters = {
            "@": "@AT",
            ":": "CL",
            "(": "OB",
            ")": "CB"
        }

        current_token = ""
        tokens = []
        lines = []

        in_string = False
        in_sum = False

        Traceback.line = 0
        Traceback.col = 0

        for character in data:
            Traceback.col += 1
            if (character == "\n"):
                Traceback.line += 1
                Traceback.col = 0

            if (in_string):
                pass
            elif (in_sum):
                pass
            else:
                if (character in stop_characters):
                    if (len(current_token) > 0):
                        tokens.append(Token("command",
                                            current_token,
                                            Traceback.line,
                                            Traceback.col - len(current_token)))
                        current_token = ""
                    if (character == "\""):
                        pass
                    elif (character == ";"):
                        lines.append(tokens)
                        tokens = []
            current_token += character

        return lines
