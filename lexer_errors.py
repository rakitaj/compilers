class LexicalError(Exception):
    def __init__(self, message: str, line: int, col: int):
        self.message = message
        self.line = line
        self.col = col


class UnknownCharError(LexicalError):
    def __init__(self, char: str, line: int, col: int):
        self.char = char
        message = f"Unknown character:[{char}]@{line}:{col}"
        super().__init__(message, line, col)
