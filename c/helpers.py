from typing import List

"""
Class containing functions to make testing easier.
Ex: Load a text file into one string.
"""

class ExampleProgram(object):

    def __init__(self, name: str, source_location: str):
        self.name = name
        self.source_location = source_location
        self.source = self.get_text(self.source_location)

    def get_text(self, location) -> str:
        with open(location) as file:
            program = file.read()
            return program


class ExampleProgramWithTokens(ExampleProgram):
    """
    A combination of program souce and its already known tokens.
    """

    def __init__(self, name: str, source_location: str, tokens_location: List[str]):
        ExampleProgram.__init__(self, name, source_location)
        self.tokens = self.get_text(tokens_location).split()
