import pytest
from lexer import Lexer
from parser import Parser, Program


@pytest.mark.parametrize(
    "source_code",
    [
        (1, "valid", "multi_digit"),
        (1, "valid", "return_0"),
        (1, "valid", "return_2"),
        (1, "valid", "newlines"),
        (1, "valid", "no_newlines"),
        (1, "valid", "spaces"),
        (1, "valid", "tabs"),
    ],
    indirect=True,
)
def test_parser_generate_ast(source_code: str):
    lexer = Lexer(source_code)
    actual_tokens = lexer.lex()
    ast = Parser(actual_tokens)
    program = ast.parse_program()
    assert type(program) is Program
