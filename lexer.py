from collections.abc import Callable

from tokens import KEYWORD_TOKENS, SINGLE_CHAR_TOKENS, Token, TokenType
from cerrors import InvalidCharError

PredicateType = Callable[[str], bool]
NEWLINE_CHARS = {"\n", "\r", "\r\n"}


class Lexer:
    def __init__(self, text: str, tab_size: int = 4):
        self.text = text
        self.line = 1
        self.col = 0
        self.idx = 0
        self.tab_size = tab_size

    def reset(self):
        self.line = 1
        self.col = 0
        self.idx = 0

    def get(self) -> str:
        return self.text[self.idx]

    def peek(self, n: int) -> str:
        """Return the character n ahead of the current index. This is unsafe and doesn't check array bounds."""
        return self.text[self.idx + n]

    def consume(self) -> str:
        """Get the current character, return it, and advance the lexer one char."""
        char = self.get()
        self.idx += 1
        self.col += 1
        if char in NEWLINE_CHARS:
            self.line += 1
            self.col = 0
        return char

    def is_at_end(self) -> bool:
        return self.idx >= len(self.text)

    def get_lexeme(self, length: int) -> str:
        return self.text[self.idx : self.idx + length]

    def take_while(self, pred: PredicateType) -> str:
        """Returns the lexeme."""
        start = self.idx
        while pred(self.get()):
            _ = self.consume()

        return self.text[start : self.idx]

    def take_keyword_or_identifier(self) -> str:
        """Once the first character is alpha then others are allowed."""

        def _is_keyword_or_ident(char: str) -> bool:
            return char.isalnum() or char in {"-", "_"}

        return self.take_while(_is_keyword_or_ident)

    def take_number(self) -> str:
        """Works for both integers and floats."""

        def _is_number(c: str) -> bool:
            return c.isnumeric() or c == "."

        return self.take_while(_is_number)

    def lex(self) -> list[Token]:
        tokens: list[Token] = list()
        while not self.is_at_end():
            char = self.get()
            start = self.col

            if char == "/" and self.peek(1) == "/":
                # Single line comment. Discard the lexeme.
                _ = self.take_while(lambda x: x not in NEWLINE_CHARS)
                continue
            elif char == "/" and self.peek(1) == "*":
                # When it starts I need to consume the opening token.
                _ = self.consume()
                _ = self.consume()

                while self.get() != "*" or self.peek(1) != "/":
                    _ = self.consume()

                # When the loop exits we still need to consume the final slash.
                _ = self.consume()
                _ = self.consume()
                continue
            elif char == " ":
                # Spaces
                self.idx += 1
                self.col += 1
                continue
            elif char == "\t":
                # Tabs. Size configurable, calculate to the next tab stop.
                self.idx += 1
                self.col += self.tab_size - (self.col % self.tab_size)
                continue
            elif char in NEWLINE_CHARS:
                self.idx += 1
                self.line += 1
                self.col = 0
                continue

            token_type: TokenType
            lexeme: str
            if char in SINGLE_CHAR_TOKENS:
                token_type = SINGLE_CHAR_TOKENS[char]
                lexeme = self.get_lexeme(1)
                self.idx += 1
                self.col += 1
            elif char.isalpha():
                # Keyword or identifier
                lexeme = self.take_keyword_or_identifier()
                if lexeme in KEYWORD_TOKENS:
                    token_type = KEYWORD_TOKENS[lexeme]
                else:
                    token_type = TokenType.IDENTIFIER
            elif char.isnumeric():
                # Integer or float
                token_type = TokenType.LITERAL_INTEGER
                lexeme = self.take_number()
            else:
                raise InvalidCharError(char, self.line, self.col)
            token = Token(token_type, lexeme, self.line, start)
            tokens.append(token)
        tokens.append(Token(TokenType.EOF, "", self.line, self.col))
        return tokens
