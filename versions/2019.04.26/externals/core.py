"""
OpenE Core library
"""

from lib.opene.parser import Parser


class ExternalParser(Parser):
    def __init__(self, *argv):
        super().__init__(*argv)

    def parse(self, tokens: list, i: int):
        pass
