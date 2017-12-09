import re
from typing import List, Tuple
from tokens import Token, OpenParen, CloseParen, OpenBrace, CloseBrace, Semicolon, ReturnKeyword, Identifier, IntegerLiteral, IntKeyword

class Token(object):

    def __init__(self, name: str, regex_pattern: str) -> None:
        self.name = name
        self.regex_pattern = regex_pattern

    def __repr__(self):
        return f"Token name: {self.name} Regex pattern: {self.regex_pattern}"

VALID_TOKENS = {
    OpenBrace().name : OpenBrace,
    CloseBrace().name: CloseBrace,
    OpenParen().name: OpenParen,
    CloseParen().name: CloseParen,
    Semicolon().name: Semicolon,
    IntKeyword().name: IntKeyword,
    IntegerLiteral().name: IntegerLiteral,
    Identifier().name: Identifier,
    ReturnKeyword().name: ReturnKeyword
}


def lex(program: str) -> List[Token]:
    """Lexes the input program into a list of tokens."""
    tokens: List[Token] = list()
    while len(program) > 0:
        hit = first_matching_regex(program)
        if hit is None:
            break
        else:
            value = program[hit[1]:hit[2]]
            token = VALID_TOKENS[hit[0].name](value)
            tokens.append(token)
            program = program[hit[2]:]
    return tokens

def is_token_valid(potential_token: str) -> bool:
    for key, value in VALID_TOKENS.items():
        if re.match(value().regex_pattern, potential_token):
            return True
    return False

def first_matching_regex(string) -> Tuple[Token, int, int]:
    """Find the earliest matching regex out of all valid tokens in the string."""
    all_hits: List[Tuple[str, int, int]] = list()
    for key, value in VALID_TOKENS.items():
        hits = [(key, m.start(0), m.end(0)) for m in re.finditer(value().regex_pattern, string)]
        all_hits.extend(hits)
    if len(all_hits) > 0:
        first_hit = sorted(all_hits, key=lambda tup: (tup[1], tup[2]))[0]
        return (Token(first_hit[0], VALID_TOKENS[first_hit[0]]), first_hit[1], first_hit[2])
    else:
        # If there are no valid tokens left in the program return None to signal the caller
        # there is nothing left.
        return None
