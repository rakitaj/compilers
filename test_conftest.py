import pytest

from conftest import parse_known_token
from lexer import Token, TokenType


@pytest.mark.parametrize(
    "known_token, expected",
    [  # type: ignore
        (
            """{"type": "KEYWORD_INT", "lexeme": "int", "line": 0, "col": 0}""",
            Token(TokenType.KEYWORD_INT, "int", 0, 0),
        ),
        (
            """{"type": "IDENTIFIER", "lexeme": "main", "line": 0, "col": 4}""",
            Token(TokenType.IDENTIFIER, "main", 0, 4),
        ),
    ],
)
def test_known_token_parsing(known_token: str, expected: Token) -> None:
    actual_token = parse_known_token(known_token)
    assert actual_token == expected
