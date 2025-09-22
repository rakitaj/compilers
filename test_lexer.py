import pytest

from lexer import Lexer, Token


@pytest.mark.parametrize(
    "source_to_known_tokens",
    [
        (1, "multi_digit"),
        (1, "return_0"),
        (1, "return_2"),
        (1, "newlines"),
        (1, "no_newlines"),
        (1, "spaces"),
        (1, "tabs"),
    ],
    indirect=True,
)
def test_lexer_against_known_tokens(source_to_known_tokens: tuple[str, list[Token]]):
    source, known_tokens = source_to_known_tokens
    lexer = Lexer(source)
    actual_tokens = lexer.lex()
    assert known_tokens == actual_tokens
