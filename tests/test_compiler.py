import pytest
from compiler import generate_assembly
from conftest import known_assembly_loader, source_code_loader
from lexer import Lexer
from parser import Parser

def tokenize_assembly_line(line: str) -> list[str]:
    """
    Split assembly line into tokens, preserving strings as single tokens.
    """
    tokens = line.strip().split(" ,")
    return tokens

def assert_assembly_equal(actual: list[str], expected: list[str]) -> tuple[bool, list[str]]:
    """
    Check if both sets of assembly are equal. Return a result type of (bool, list[str]).
    If there are any issues the list contains human readable output for them.
    """
    if len(actual) != len(expected):
        return (False, [f"Number of assembly lines do not match. Actual:{len(actual)} vs Expected:{len(expected)}"])
    
    issues: list[str] = []
    for i, (actual_line, expected_line) in enumerate(zip(actual, expected)):
        # Normalize both lines
        actual_tokens = tokenize_assembly_line(actual_line)
        expected_tokens = tokenize_assembly_line(expected_line)

        
        if len(actual_tokens) != len(expected_tokens):
            issues.append(f"Line {i+1}: Different number of tokens - Actual: {actual_tokens} vs Expected: {expected_tokens}")
            continue
        
        # Compare each token
        for j, (a_token, e_token) in enumerate(zip(actual_tokens, expected_tokens)):
            if a_token != e_token:
                issues.append(f"Line {i+1}, Token {j+1}: '{a_token}' != '{e_token}'")
    
    return (len(issues) == 0, issues)

# Enhanced test that uses the comparison function
@pytest.mark.parametrize(
    "stage, folder, name",
    [
        (1, "valid", "return_0"),
        (1, "valid", "return_2"),
        (1, "valid", "multi_digit"),
    ]
)
def test_generate_assembly_matches_expected(stage: int, folder: str, name: str):
    source_code = source_code_loader(stage, folder, name)
    expected_assembly = known_assembly_loader(stage, folder, name)

    # Generate actual assembly
    lexer = Lexer(source_code)
    actual_tokens = lexer.lex()
    ast = Parser(actual_tokens)
    program = ast.parse_program()
    actual_assembly = generate_assembly(program)
    
    # Compare
    is_equal, issues = assert_assembly_equal(actual_assembly, expected_assembly)
    
    # if not is_equal:
    #     error_msg = "Assembly mismatch:\n" + "\n".join(issues)
    #     pytest.fail(error_msg)
    assert is_equal is True, issues