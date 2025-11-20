from tokens import TokenType, Token


class CompilerError(Exception):
    def __init__(self, message: str, line: int, col: int):
        self.message = message
        self.line = line
        self.col = col

    def __str__(self) -> str:
        return f"{self.message} // Embedded position @ line:{self.line} col:{self.col}"


class InvalidCharError(CompilerError):
    def __init__(self, char: str, line: int, col: int):
        self.char = char
        message = f"Unknown character:[{char}]@{line}:{col}"
        super().__init__(message, line, col)


class InvalidIdentifier(CompilerError):
    def __init__(self, ident: str, line: int, col: int):
        self.ident = ident
        message = f"Invalid identifier:[{ident}]@{line}:{col}"
        super().__init__(message, line, col)


class CSyntaxError(CompilerError):
    def __init__(self, expected: TokenType, actual: Token):
        message = f"Expected token type [{expected}] and found [{actual}]"
        super().__init__(message, actual.column, actual.line)
