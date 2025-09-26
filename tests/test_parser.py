import pytest

from compiler import generate_assembly
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


@pytest.mark.parametrize(
    "source_code",
    [
        # (1, "multi_digit"),
        (1, "valid", "return_0"),
        (1, "valid", "return_2"),
        # (1, "newlines"),
        # (1, "no_newlines"),
        # (1, "spaces"),
        # (1, "tabs"),
    ],
    indirect=True,
)
def test_generate_assembly(source_code: str):
    lexer = Lexer(source_code)
    actual_tokens = lexer.lex()
    ast = Parser(actual_tokens)
    program = ast.parse_program()
    assembly = generate_assembly(program)
    assert len(assembly) == 4
