from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    OPEN_BRACE = auto()
    CLOSE_BRACE = auto()
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    SEMICOLON = auto()
    KEYWORD_INT = auto()
    KEYWORD_RETURN = auto()
    KEYWORD_VOID = auto()
    IDENTIFIER = auto()
    INTEGER = auto()
    EOF = auto()


@dataclass(frozen=True)
class Token:
    token_type: TokenType
    lexeme: str
    line: int
    column: int


SINGLE_CHAR_TOKENS = {
    "{": TokenType.OPEN_BRACE,
    "}": TokenType.CLOSE_BRACE,
    "(": TokenType.OPEN_PAREN,
    ")": TokenType.CLOSE_PAREN,
    ";": TokenType.SEMICOLON,
}

KEYWORD_TOKENS = {
    "int": TokenType.KEYWORD_INT,
    "return": TokenType.KEYWORD_RETURN,
    "void": TokenType.KEYWORD_VOID,
}
