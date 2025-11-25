"""
Lexical analyzer for PatternLang.
Converts source code into a stream of tokens using regex-based scanning.
"""

import re
from .tokens import Token, TokenType, KEYWORDS
from .utils.errors import LexerError


class Lexer:
    """
    Tokenizes PatternLang source code.
    Uses regex patterns to identify tokens and track line/column positions.
    """

    def __init__(self, source_code):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []

        # Token patterns (order matters!)
        self.token_patterns = [
            # Whitespace (ignored)
            (r"[ \t]+", None),
            # Comments (ignored)
            (r"#[^\n]*", None),
            # Newlines
            (r"\n", "NEWLINE"),
            # Two-character operators (must come before single-char)
            (r"\.\.", "RANGE"),
            (r"==", "EQUAL"),
            (r"!=", "NOT_EQUAL"),
            (r"<=", "LESS_EQUAL"),
            (r">=", "GREATER_EQUAL"),
            # Numbers
            (r"\d+", "NUMBER"),
            # Identifiers and keywords
            (r"[a-zA-Z_][a-zA-Z0-9_]*", "IDENTIFIER"),
            # Single-character operators and symbols
            (r"\+", "PLUS"),
            (r"-", "MINUS"),
            (r"\*", "MULTIPLY"),
            (r"/", "DIVIDE"),
            (r"=", "ASSIGN"),
            (r"<", "LESS_THAN"),
            (r">", "GREATER_THAN"),
            (r";", "SEMICOLON"),
            (r",", "COMMA"),
            (r"\{", "LBRACE"),
            (r"\}", "RBRACE"),
            (r"\(", "LPAREN"),
            (r"\)", "RPAREN"),
        ]

        # Compile all patterns into one master regex
        self.master_pattern = "|".join(
            f"({pattern})" for pattern, _ in self.token_patterns
        )
        self.master_regex = re.compile(self.master_pattern)

    def tokenize(self):
        """
        Main tokenization method.
        Returns a list of tokens.
        """
        while self.position < len(self.source):
            match = self.master_regex.match(self.source, self.position)

            if not match:
                # Invalid character
                char = self.source[self.position]
                raise LexerError(f"Invalid character '{char}'", self.line, self.column)

            # Find which pattern matched
            for i, (pattern, token_name) in enumerate(self.token_patterns):
                if match.group(i + 1) is not None:
                    value = match.group(i + 1)

                    # Handle different token types
                    if token_name is None:
                        # Whitespace or comment - skip
                        pass
                    elif token_name == "NEWLINE":
                        self.line += 1
                        self.column = 1
                        self.position = match.end()
                        continue
                    elif token_name == "NUMBER":
                        token = Token(
                            TokenType.NUMBER, int(value), self.line, self.column
                        )
                        self.tokens.append(token)
                    elif token_name == "IDENTIFIER":
                        # Check if it's a keyword
                        if value in KEYWORDS:
                            token_type = KEYWORDS[value]
                            token = Token(token_type, value, self.line, self.column)
                        else:
                            token = Token(
                                TokenType.IDENTIFIER, value, self.line, self.column
                            )
                        self.tokens.append(token)
                    else:
                        # Other tokens
                        token_type = TokenType[token_name]
                        token = Token(token_type, value, self.line, self.column)
                        self.tokens.append(token)

                    # Update position
                    self.column += len(value)
                    self.position = match.end()
                    break

        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

    def __repr__(self):
        return f"Lexer(tokens={len(self.tokens)})"
