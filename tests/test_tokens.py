import pytest
import json
from tokens import Token, TokenType, token_decoder

@pytest.mark.parametrize(
    "known_token, expected",
    [
        (
            """{"token_type": "KEYWORD_INT", "lexeme": "int", "line": 0, "col": 0}""",
            Token(TokenType.KEYWORD_INT, "int", 0, 0),
        ),
        (
            """{"token_type": "IDENTIFIER", "lexeme": "main", "line": 0, "col": 4}""",
            Token(TokenType.IDENTIFIER, "main", 0, 4),
        ),
    ],
)
def test_known_token_parsing(known_token: str, expected: Token) -> None:
    obj_dict = json.loads(known_token)
    actual_token = token_decoder(obj_dict)
    assert actual_token == expected
