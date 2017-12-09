class Token(object):
    """
    Base class for token type.
    """

    def __init__(self, name: str, regex_pattern: str, value: str = None) -> str:
        self.name = name
        self.regex_pattern = regex_pattern
        self.value = value

    def __eq__(self, other):
        return self.name == other.name and self.regex_pattern == other.regex_pattern and self.value == other.value

    def __hash__(self):
        return hash((self.name, self.regex_pattern, self.value))

    def __repr__(self):
        return f"{self.name} - {self.regex_pattern} - {self.value}"

class OpenBrace(Token):

    def __init__(self, value: str = None):
        Token.__init__(self, "{", "{", value)

class CloseBrace(Token):

    def __init__(self, value: str = None):
        Token.__init__(self, "}", "}", value)

class OpenParen(Token):

    def __init__(self, value: str = None):
        Token.__init__(self, "(", "\(", value)

class CloseParen(Token):

    def __init__(self, value: str = None):
        Token.__init__(self, ")", "\)", value)

class Semicolon(Token):

    def __init__(self, value: str = None):
        Token.__init__(self, ";", ";", value)

class IntKeyword(Token):

    def __init__(self, value: str = None):
        Token.__init__(self, "int", "int", value)

class ReturnKeyword(Token):

    def __init__(self, value: str = None):
        Token.__init__(self, "return", "return", value)

class Identifier(Token):

    def __init__(self, value: str = None):
        Token.__init__(self, "identifier", "[a-zA-Z]\w*", value)

class IntegerLiteral(Token):

    def __init__(self, value: str = None):
        Token.__init__(self, "integer literal", "[0-9]+", value)
        