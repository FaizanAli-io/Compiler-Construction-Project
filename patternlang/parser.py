"""
Recursive descent parser for PatternLang.
Builds an Abstract Syntax Tree (AST) from tokens.
"""

from .tokens import TokenType
from .ast_nodes import *
from .utils.errors import ParseError


class Parser:
    """
    Parses tokens into an AST using recursive descent.
    One method per grammar rule.
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None

    def advance(self):
        """Move to the next token."""
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]

    def expect(self, token_type):
        """
        Consume a token of the expected type.
        Raises ParseError if token doesn't match.
        """
        if self.current_token.type != token_type:
            raise ParseError(
                f"Expected {token_type.name}, got {self.current_token.type.name}",
                self.current_token.line,
                self.current_token.column,
            )
        token = self.current_token
        self.advance()
        return token

    def parse(self):
        """Entry point: parse the entire program."""
        return self.program()

    def program(self):
        """program ::= stmt_list 'end' ';'"""
        statements = self.stmt_list()
        self.expect(TokenType.END)
        self.expect(TokenType.SEMICOLON)
        return Program(statements)

    def stmt_list(self):
        """stmt_list ::= { statement }"""
        statements = []

        while self.current_token.type not in [
            TokenType.END,
            TokenType.RBRACE,
            TokenType.EOF,
        ]:
            stmt = self.statement()
            statements.append(stmt)

        return statements

    def statement(self):
        """
        statement ::= var_decl | assignment | repeat_stmt | if_stmt | print_stmt

        Note: var_decl and assignment both start with 'let', so they're the same.
        """
        if self.current_token.type == TokenType.LET:
            return self.var_decl()
        elif self.current_token.type == TokenType.REPEAT:
            return self.repeat_stmt()
        elif self.current_token.type == TokenType.IF:
            return self.if_stmt()
        elif self.current_token.type == TokenType.PRINT:
            return self.print_stmt()
        else:
            raise ParseError(
                f"Unexpected token {self.current_token.type.name}",
                self.current_token.line,
                self.current_token.column,
            )

    def var_decl(self):
        """var_decl ::= 'let' IDENT '=' expr ';'"""
        self.expect(TokenType.LET)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        expr = self.expr()
        self.expect(TokenType.SEMICOLON)
        return VarDecl(name, expr)

    def repeat_stmt(self):
        """repeat_stmt ::= 'repeat' IDENT 'in' expr '..' expr '{' stmt_list '}'"""
        self.expect(TokenType.REPEAT)
        var_name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.IN)
        start_expr = self.expr()
        self.expect(TokenType.RANGE)
        end_expr = self.expr()
        self.expect(TokenType.LBRACE)
        body = self.stmt_list()
        self.expect(TokenType.RBRACE)
        return Repeat(var_name, start_expr, end_expr, body)

    def if_stmt(self):
        """if_stmt ::= 'if' expr 'goto' IDENT ';'"""
        self.expect(TokenType.IF)
        condition = self.expr()
        self.expect(TokenType.GOTO)
        label = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.SEMICOLON)
        return If(condition, label)

    def print_stmt(self):
        """print_stmt ::= 'print' expr ';'"""
        self.expect(TokenType.PRINT)
        expr = self.expr()
        self.expect(TokenType.SEMICOLON)
        return Print(expr)

    def expr(self):
        """expr ::= term { ('+' | '-') term }"""
        left = self.term()

        while self.current_token.type in [
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.EQUAL,
            TokenType.NOT_EQUAL,
            TokenType.LESS_THAN,
            TokenType.GREATER_THAN,
            TokenType.LESS_EQUAL,
            TokenType.GREATER_EQUAL,
        ]:
            op = self.current_token.type.name
            self.advance()
            right = self.term()
            left = BinaryOp(op, left, right)

        return left

    def term(self):
        """term ::= factor { ('*' | '/') factor }"""
        left = self.factor()

        while self.current_token.type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            op = self.current_token.type.name
            self.advance()
            right = self.factor()
            left = BinaryOp(op, left, right)

        return left

    def factor(self):
        """factor ::= NUMBER | IDENT | '(' expr ')'"""
        if self.current_token.type == TokenType.NUMBER:
            value = self.current_token.value
            self.advance()
            return Number(value)

        elif self.current_token.type == TokenType.IDENTIFIER:
            name = self.current_token.value
            self.advance()
            return Identifier(name)

        elif self.current_token.type == TokenType.LPAREN:
            self.advance()
            expr = self.expr()
            self.expect(TokenType.RPAREN)
            return expr

        else:
            raise ParseError(
                f"Expected NUMBER, IDENTIFIER, or '(', got {self.current_token.type.name}",
                self.current_token.line,
                self.current_token.column,
            )
