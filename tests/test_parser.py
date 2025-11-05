import pytest
from conftest import source_code_loader
from lexer import Lexer
from parser import Parser, Program


@pytest.mark.parametrize(
    "stage, folder, name",
    [
        (1, "valid", "multi_digit"),
        (1, "valid", "return_0"),
        (1, "valid", "return_2"),
        (1, "valid", "newlines"),
        (1, "valid", "no_newlines"),
        (1, "valid", "spaces"),
        (1, "valid", "tabs"),
        (2, "valid", "bitwise_int_min"),
        (2, "valid", "bitwise_zero"),
        (2, "valid", "bitwise"),
        (2, "valid", "neg_zero"),
        (2, "valid", "neg"),
        (2, "valid", "negate_int_max"),
        (2, "valid", "nested_ops_2"),
        (2, "valid", "nested_ops"),
        (2, "valid", "parens_2"),
        (2, "valid", "parens_3"),
        (2, "valid", "parens"),
        (2, "valid", "redundant_parens"),
    ],
)
def test_parser_generate_ast(stage: int, folder: str, name: str):
    source_code = source_code_loader(stage, folder, name)
    lexer = Lexer(source_code)
    actual_tokens = lexer.lex()
    ast = Parser(actual_tokens)
    program = ast.parse_program()
    assert type(program) is Program
