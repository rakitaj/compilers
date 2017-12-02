import re
from typing import List, Tuple

class Token(object):

    def __init__(self, name: str, regex_pattern: str) -> None:
        self.name = name
        self.regex_pattern = regex_pattern

    def __repr__(self):
        return f"Token name: {self.name} Regex pattern: {self.regex_pattern}"

VALID_TOKENS = [
    Token("{", "{"),
    Token("}", "}"),
    Token("(", "\("),
    Token(")", "\)"),
    Token(";", ";"),
    Token("int", "int"),
    Token("return", "return"),
    Token("identifier", "[a-zA-Z]\w*"),
    Token("integer literal", "[0-9]+")
]

def lex(program: str) -> List[str]:
    """Lexes the input program into a list of tokens."""
    tokens: List[str] = list()
    while(len(program) > 0):
        hit = first_matching_regex(program)
        tokens.append(program[hit[1]:hit[2]])
        program = program[hit[2]:]
    return tokens

def is_token_valid(potential_token: str) -> bool:
    for token in VALID_TOKENS:
        if re.match(token.regex_pattern, potential_token):
            return True
    return False

def first_matching_regex(string) -> Tuple[Token, int, int]:
    all_hits: Tuple[Token, int, int] = list()
    for token in VALID_TOKENS:
        hits = [(token, m.start(0), m.end(0)) for m in re.finditer(token.regex_pattern, string)]
        all_hits.extend(hits)
    first_hit = sorted(all_hits, key = lambda tup: (tup[1], tup[2]))[0]
    return first_hit
