import pytest
from conftest import source_code_loader
from lexer import Lexer, Token
from lexer_errors import InvalidCharError


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


@pytest.mark.parametrize(
    "filename, invalid_char",
    [
        ("at_sign", "@"),
        ("backslash", "\\"),
        ("backtick", "`"),
        ("invalid_identifier_2", "@"),
    ],
)
def test_lexer_against_unknown_char(filename: str, invalid_char: str):
    source_code = source_code_loader(1, "invalid_lex", filename)
    lexer = Lexer(source_code)
    with pytest.raises(InvalidCharError) as ex_info:
        _ = lexer.lex()
    assert ex_info.value.char == invalid_char
