"""
Token definitions for PatternLang.
Each token has a type and an optional value.
"""

from enum import Enum, auto


class TokenType(Enum):
    """Enumeration of all token types in PatternLang."""

    # Keywords
    LET = auto()
    REPEAT = auto()
    IN = auto()
    PRINT = auto()
    IF = auto()
    RETURN = auto()
    FUNC = auto()
    GOTO = auto()
    END = auto()

    # Literals and identifiers
    IDENTIFIER = auto()
    NUMBER = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    ASSIGN = auto()

    # Comparison operators
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()

    # Symbols
    SEMICOLON = auto()
    COMMA = auto()
    LBRACE = auto()
    RBRACE = auto()
    LPAREN = auto()
    RPAREN = auto()
    RANGE = auto()  # ..

    # Special
    EOF = auto()
    NEWLINE = auto()
    COLON = auto()


class Token:
    """
    Represents a single token from the source code.
    """

    def __init__(self, token_type, value, line, column):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, {self.line}:{self.column})"

    def __str__(self):
        return self.__repr__()


# Keyword mapping
KEYWORDS = {
    "let": TokenType.LET,
    "repeat": TokenType.REPEAT,
    "in": TokenType.IN,
    "print": TokenType.PRINT,
    "if": TokenType.IF,
    "goto": TokenType.GOTO,
    "end": TokenType.END,
    "return": TokenType.RETURN,
    "func": TokenType.FUNC,
}
