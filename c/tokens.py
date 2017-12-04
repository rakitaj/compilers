class Token(object):

    def __init__(self, name, regex_pattern):
        self.name = name
        self.regex_pattern = regex_pattern

class OpenBrace(Token):

    def __init__(self):
        Token.__init__(self, "{", "{")

class CloseBrace(Token):

    def __init__(self):
        Token.__init__(self, "}", "}")

class OpenParen(Token):

    def __init__(self):
        Token.__init__(self, "(", "\(")

class CloseParen(Token):

    def __init__(self):
        Token.__init__(self, ")", "\)")

class Semicolon(Token):

    def __init__(self):
        Token.__init__(self, ";", ";")

class IntKeyword(Token):

    def __init__(self):
        Token.__init__(self, "int", "int")

class ReturnKeyword(Token):

    def __init__(self):
        Token.__init__(self, "return", "return")

class Identifier(Token):

    def __init__(self):
        Token.__init__(self, "identifier", "[a-zA-Z]\w*")

class IntegerLiteral(Token):

    def __init__(self):
        Token.__init__(self, "integer literal", "[0-9]+")
        