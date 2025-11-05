from dataclasses import dataclass
from abc import ABC
from tokens import Token, TokenType, UNARY_OP_TOKENS
from cerrors import CSyntaxError


class Expression(ABC):
    pass


@dataclass
class ConstantInt(Expression):
    value: int


@dataclass
class UnaryOp(Expression):
    operator: TokenType
    inner_expr: Expression

    def __init__(self, operator: TokenType, operand: Expression):
        if operator not in UNARY_OP_TOKENS:
            raise ValueError(f"Invalid token type for unary operation {operator}.")
        self.operator = operator
        self.inner_expr = operand


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
    def __init__(self, functions: list[Function] | None = None) -> None:
        self.functions: list[Function] = functions or []


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

    def expect(self, token_type: TokenType) -> Token:
        token = self.consume()
        if token.token_type == token_type:
            return token
        else:
            raise CSyntaxError(token_type, token)

    def parse_program(self) -> Program:
        functions = self.parse_functions()
        program = Program(functions)
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
                _ = self.expect(TokenType.CLOSE_BRACE)
                # if is_valid_function := self.expect(TokenType.CLOSE_BRACE):
                #     self.idx += 1
                # else:
                #     raise ValueError(is_valid_function[1])
                functions.append(function)
        return functions

    def parse_statements(self) -> list[Statement]:
        statements: list[Statement] = []
        while self.get().token_type == TokenType.KEYWORD_RETURN:
            self.idx += 1
            statement = Statement(self.parse_expression())
            _ = self.expect(TokenType.SEMICOLON)
            statements.append(statement)
            # if is_valid_statement := self.expect(TokenType.SEMICOLON):
            #     statements.append(statement)
            #     self.idx += 1
            # else:
            #     raise ValueError(is_valid_statement[1])
        return statements

    def parse_expression(self) -> Expression:
        token = self.consume()
        if token.token_type in UNARY_OP_TOKENS:
            operator = token
            inner_expr = self.parse_expression()
            return UnaryOp(operator.token_type, inner_expr)
        elif token.token_type == TokenType.OPEN_PAREN:
            inner_expr = self.parse_expression()
            _ = self.expect(TokenType.CLOSE_PAREN)
        else:
            integer = int(token.lexeme)
            return ConstantInt(integer)


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
