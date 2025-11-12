from dataclasses import dataclass
from enum import Enum, auto
import json
from typing import Any


class TokenType(Enum):
    OPEN_BRACE = auto()
    CLOSE_BRACE = auto()
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    SEMICOLON = auto()
    IDENTIFIER = auto()
    EOF = auto()
    NEGATION = auto()
    BITWISE_COMPLEMENT = auto()
    LOGICAL_NEGATION = auto()

    KW_RETURN = auto()
    KW_VOID = auto()

    LITERAL_INTEGER = auto()
    LITERAL_FLOAT = auto()

    KW_UNSIGNED = auto()
    KW_SIGNED = auto()

    KW_CHAR = auto()
    KW_SHORT = auto()
    KW_INT = auto()
    KW_LONG = auto()
    KW_FLOAT = auto()
    KW_DOUBLE = auto()


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
    "return": TokenType.KW_RETURN,
    "void": TokenType.KW_VOID,
    "signed": TokenType.KW_SIGNED,
    "unsigned": TokenType.KW_UNSIGNED,
    "char": TokenType.KW_CHAR,
    "short": TokenType.KW_SHORT,
    "int": TokenType.KW_INT,
    "long": TokenType.KW_LONG,
    "float": TokenType.KW_FLOAT,
    "double": TokenType.KW_DOUBLE,
}

UNARY_OP_TOKENS = {TokenType.NEGATION, TokenType.BITWISE_COMPLEMENT, TokenType.LOGICAL_NEGATION}


class TokenEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Token):
            return {"lexeme": o.lexeme, "line": o.line, "column": o.column, "token_type": o.token_type.name}
        return super().default(o)


def token_decoder(obj_dict: dict[Any, Any]) -> Token:
    """Provide this to object_hook"""
    token_type = TokenType[obj_dict["token_type"]]
    column_name = "col" if "col" in obj_dict else "column"
    return Token(token_type, obj_dict["lexeme"], obj_dict["line"], obj_dict[column_name])
