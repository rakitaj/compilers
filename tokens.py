from dataclasses import dataclass
from enum import Enum, auto
import json
from typing import Any
from collections.abc import Callable

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
    NEGATION = auto()
    BITWISE_COMPLEMENT = auto()
    LOGICAL_NEGATION = auto()


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
    "-": TokenType.NEGATION,
    "!": TokenType.LOGICAL_NEGATION,
    "~": TokenType.BITWISE_COMPLEMENT,
}

KEYWORD_TOKENS = {
    "int": TokenType.KEYWORD_INT,
    "return": TokenType.KEYWORD_RETURN,
    "void": TokenType.KEYWORD_VOID,
}

class TokenEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Token):
            
            return {
                "lexeme": o.lexeme,
                "line": o.line,
                "column": o.column,
                "token_type": o.token_type.name
            }
        return super().default(o)

def token_decoder(obj_dict: dict[Any, Any]) -> Token:
    """Provide this to object_hook"""
    token_type = TokenType[obj_dict["token_type"]]
    column_name = "col" if "col" in obj_dict else "column"
    return Token(token_type, obj_dict["lexeme"], obj_dict["line"], obj_dict[column_name])
