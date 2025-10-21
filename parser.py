from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from tokens import Token, TokenType


class Expression(ABC):
    @abstractmethod
    def evaluate(self) -> int:
        pass


@dataclass
class ConstantInt(Expression):
    value: int

    def evaluate(self) -> int:
        return self.value


@dataclass
class UnaryOp(Expression):
    operator: TokenType
    inner_expr: Expression

    def __init__(self, operator: TokenType, operand: Expression):
        if operator not in {TokenType.BITWISE_COMPLEMENT, TokenType.LOGICAL_NEGATION, TokenType.NEGATION}:
            raise ValueError(f"Invalid token type for unary operation {operator}.")
        self.operator = operator
        self.inner_expr = operand

    def evaluate(self) -> int:
        return super().evaluate()


@dataclass
class Statement:
    expr: Expression


@dataclass
class Parameter:
    type: Token
    identifier: str


class Function:
    def __init__(
        self, name: str, statements: list[Statement] | None = None, parameters: list[Parameter] | None = None
    ) -> None:
        self.name = name
        self.statements: list[Statement] = statements or []
        self.parameters: list[Parameter] = parameters or []


class Program:
    def __init__(self) -> None:
        self.functions: list[Function] = []


def is_statement_start(tokens: list[Token], idx: int) -> bool:
    return tokens[idx].token_type == TokenType.KEYWORD_RETURN


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.idx = 0

    def get(self, n: int = 0) -> Token:
        return self.tokens[self.idx + n]

    def get_safe(self, n: int = 0) -> Token | None:
        if self.idx + n >= len(self.tokens):
            return None
        else:
            return self.get(n)

    def check_sequence(self, *token_types: TokenType) -> bool:
        i = 0
        for token_type in token_types:
            if (t := self.get_safe(i)) is not None:
                if t.token_type != token_type:
                    return False
            i += 1
        return True

    def consume(self) -> Token:
        token = self.get()
        self.idx += 1
        return token

    def expect(self, token_type: TokenType) -> tuple[bool, str]:
        token = self.get(0)
        if token.token_type == token_type:
            return (True, "")
        else:
            msg = f"Expected {token_type} at i:{self.idx}. Found: {token}"
            return (False, msg)

    def parse_program(self) -> Program:
        program = Program()
        program.functions.extend(self.parse_functions())
        return program

    def parse_functions(self) -> list[Function]:
        functions: list[Function] = []
        while self.get().token_type != TokenType.EOF:
            if self.check_sequence(TokenType.KEYWORD_INT, TokenType.IDENTIFIER, TokenType.OPEN_PAREN):
                name = self.get(1).lexeme
                self.idx += 3
                parameters: list[Parameter] = []
                if self.check_sequence(TokenType.KEYWORD_VOID):
                    param = Parameter(self.get(), "")
                    parameters.append(param)
                    self.idx += 1
                self.idx += 2
                # self.idx += 5
                statements = self.parse_statements()
                function = Function(name, statements)
                if is_valid_function := self.expect(TokenType.CLOSE_BRACE):
                    self.idx += 1
                else:
                    raise ValueError(is_valid_function[1])
                functions.append(function)
        return functions

    def parse_statements(self) -> list[Statement]:
        statements: list[Statement] = []
        while self.get().token_type == TokenType.KEYWORD_RETURN:
            self.idx += 1
            statement = Statement(self.parse_expression())
            if is_valid_statement := self.expect(TokenType.SEMICOLON):
                statements.append(statement)
                self.idx += 1
            else:
                raise ValueError(is_valid_statement[1])
        return statements

    def parse_expression(self) -> Expression:
        token = self.consume()
        if token.token_type == TokenType.INTEGER:
            integer = int(token.lexeme)
            return ConstantInt(integer)
        else:
            op = token.token_type
            inner_expr = self.parse_expression()
            return UnaryOp(op, inner_expr)
        # number_str = self.get().lexeme
        # self.idx += 1
        # return Expression(int(number_str))


def pretty_print(node: Program | Function | Statement | Expression, indent: int = 0) -> None:
    padding = " " * indent
    if isinstance(node, Program):
        print(f"\n{padding}Program begins:")
        for function in node.functions:
            pretty_print(function, indent + 2)

    elif isinstance(node, Function):
        print(f"{padding}Function - {node.name}")
        for statement in node.statements:
            pretty_print(statement, indent + 2)

    elif isinstance(node, Statement):
        print(f"{padding}Statement - {node.expr}")
        # Hack! A statement can only have one expr right now.
        pretty_print(node.expr, indent + 2)

    else:  # Always an expression by this point
        print(f"{padding}Expr value - {node}")
