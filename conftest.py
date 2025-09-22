import json
from pathlib import Path
import pytest
from lexer import Token, TokenType


@pytest.fixture
def source_to_known_tokens(request: pytest.FixtureRequest) -> tuple[str, list[Token]]:
    stage, name = request.param
    script_path = Path(__file__).resolve()
    script_directory = script_path.parent

    # Load program source
    program_path = f"{script_directory}/test-programs/chapter-{stage:02}/valid/{name}.c"
    with open(program_path, "r") as fp:
        program_source = fp.read()

    # Load expected tokens
    tokens_path = f"{script_directory}/test-programs/chapter-{stage:02}/valid/{name}.tokens"
    with open(tokens_path, "r") as fp:
        lines = fp.readlines()

    tokens: list[Token] = []
    for line in lines:
        token = parse_known_token(line)
        tokens.append(token)

    return program_source, tokens


@pytest.fixture
def source_code(request: pytest.FixtureRequest) -> str:
    stage, name = request.param
    script_path = Path(__file__).resolve()
    script_directory = script_path.parent

    # Load program source
    program_path = f"{script_directory}/test-programs/chapter-{stage:02}/valid/{name}.c"
    with open(program_path, "r") as fp:
        program_source = fp.read()

    return program_source


def parse_known_token(token_str: str) -> Token:
    data = json.loads(token_str.strip())
    token_type = TokenType[data["type"]]
    return Token(token_type, data["lexeme"], data["line"], data["col"])
