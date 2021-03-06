from ccompiler import *
import pytest
from helpers import *

class TestTokenValidity(object):
    
    @pytest.mark.parametrize("token_input,expected", [
        ("int", True),
        ("main", True),
        ("(", True),
        (")", True),
        ("return", True),
        ("2", True),
        (";", True),
        ("#$%", False)
    ])
    def test_token_validity(self, token_input, expected):
        actual = is_token_valid(token_input)
        assert actual == expected

    def test_simple_token_validity(self):
        actual = is_token_valid("int")
        assert actual is True

class TestLexer(object):

    def test_first_matching_regex(self):
        program = "int main()"
        actual = first_matching_regex(program)
        print(actual)
        assert actual[0].name == "int"
        assert actual[1] == 0 and actual[2] == 3

    def test_lexing_simple_program(self):
        simple_program = """
int main() {
    return 2;
}
"""
        result = lex(simple_program)
        #assert result == ["int", "main", "(", ")", "{", "return", "2", ";", "}"]
        assert result == [
            IntKeyword("int"),
            Identifier("main"),
            OpenParen("("),
            CloseParen(")"),
            OpenBrace("{"),
            ReturnKeyword("return"),
            IntegerLiteral("2"),
            Semicolon(";"),
            CloseBrace("}")]

    @pytest.mark.parametrize("name,source_location,tokens_location", [
        create_test_tuple("simple01"),
        create_test_tuple("multi_digit")
    ])
    def test_lexing(self, name, source_location, tokens_location):
        program = ExampleProgramWithTokens(name, source_location, tokens_location)
        actual_tokens = lex(program.source)
        assert actual_tokens == program.tokens
