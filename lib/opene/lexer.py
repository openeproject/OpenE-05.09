class Traceback:
    """
    This is the Traceback class
    It is used for debugging errors and finding stuff in the code (if that makes sense)
    """
    line = 0
    col = 0


class Token:
    """
    This class stores tokens
    It's an easier way to keep data of a token together
    """
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

    def __repr__(self):
        return "Token(type: {}, value: {}, line: {}, col: {}, char: {})".format(
            self.type,
            self.value,
            self.line,
            self.col,
            self.char
        )


class Lexer:
    def __init__(self):
        pass

    def tokenise(self, data) -> list:
        stop_characters = list(" \n\t\";")
        replace_characters = {
            "@": "AT",
            "=": "EQ",
            ",": "CM",
            ":": "CL",
            "(": "OB",
            ")": "CB",
            "[": "OS",
            "]": "CS",
            "{": "OC",
            "}": "CC"
        }
        numbers = list(str(num) for num in range(10))
        mathematical_operators = list("+-*/^%")
        last_character_space = False
        open_parentheses = 0

        current_token = ""
        tokens = []
        lines = []

        in_string = False
        in_sum = False
        escape_character = False

        Traceback.line = 0
        Traceback.col = 0

        for character in data:
            Traceback.col += 1
            if (character == "\n"):
                Traceback.line += 1
                Traceback.col = 0

            if (in_string):
                if (escape_character):
                    # if (character == "\\"):
                    #     current_token += "\\"
                    # elif (character == "\""):
                    #     current_token += "\""
                    # else:
                    #     current_token += "\\{}".format(character)
                    current_token += "\\{}".format(character)
                    character = ""
                    escape_character = False
                else:
                    if (character == "\\"):
                        escape_character = True
                        character = ""
                    elif (character == "\""):
                        tokens.append(Token("string",
                                            "\"{}\"".format(current_token),
                                            Traceback.line,
                                            Traceback.col - len(current_token) - 2))  # The -2 if for the quote marks
                        current_token = ""
                        character = ""
                        in_string = False
                if (character == "\\"):
                    if (escape_character):
                        current_token += "\\"
                    else:
                        escape_character = True
                if (character == "\""):
                    pass
            elif (in_sum):
                if (character == " "):
                    if (last_character_space):
                        tokens.append(Token("sum", current_token, Traceback.line, Traceback.col))
                        last_character_space = False
                        in_sum = False
                        current_token = ""
                        character = ""
                    else:
                        last_character_space = True
                        character = ""
                elif (character == "("):
                    open_parentheses += 1
                elif (character == ")"):
                    if (open_parentheses > 0):
                        open_parentheses -= 1
                    else:
                        tokens.append(Token("sum",
                                            current_token,
                                            Traceback.line,
                                            Traceback.col - len(current_token)))
                        last_character_space = False
                        in_sum = False
                        current_token = ""
                        tokens.append(Token("operator",
                                            replace_characters[character],
                                            Traceback.line,
                                            Traceback.col,
                                            character))
                        character = ""
                else:
                    if (character in numbers or character in mathematical_operators or character == "."):
                        last_character_space = False
                    else:
                        tokens.append(Token("sum",
                                            current_token,
                                            Traceback.line,
                                            Traceback.col-len(current_token)))
                        last_character_space = False
                        in_sum = False
                        current_token = ""
                        if (character in stop_characters or character in replace_characters):
                            if (character in stop_characters):
                                if (character == "\""):
                                    in_string = True
                                elif (character == ";"):
                                    lines.append(tokens)
                                    tokens = []
                            elif (character in replace_characters):
                                tokens.append(Token("operator",
                                                    replace_characters[character],
                                                    Traceback.line,
                                                    Traceback.col,
                                                    character))
                            character = ""
            else:
                if (character in stop_characters or character in replace_characters):
                    if (len(current_token) > 0):
                        tokens.append(Token("command",
                                            current_token,
                                            Traceback.line,
                                            Traceback.col - len(current_token) - 1))  # The -1 is for the stop character
                        current_token = ""
                    if (character in stop_characters):
                        if (character == "\""):
                            in_string = True
                        elif (character == ";"):
                            lines.append(tokens)
                            tokens = []
                    elif (character in replace_characters):
                        tokens.append(Token("operator",
                                            replace_characters[character],
                                            Traceback.line,
                                            Traceback.col,
                                            character))
                    character = ""
                elif (character in numbers):
                    if (len(current_token) == 0):
                        in_sum = True
                    elif (len(current_token) == 1 and current_token[0] == "-"):
                        in_sum = True
            current_token += character

        return lines
