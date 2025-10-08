class LexicalError(Exception):
    def __init__(self, message: str, line: int, col: int):
        self.message = message
        self.line = line
        self.col = col


class InvalidCharError(LexicalError):
    def __init__(self, char: str, line: int, col: int):
        self.char = char
        message = f"Unknown character:[{char}]@{line}:{col}"
        super().__init__(message, line, col)

class InvalidIdentifier(LexicalError):
    def __init__(self, ident: str, line: int, col: int):
        self.ident = ident
        message = f"Invalid identifier:[{ident}]@{line}:{col}"
        super().__init__(message, line, col)