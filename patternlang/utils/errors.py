"""
Custom exception classes for the PatternLang compiler.
Each exception corresponds to a specific compiler phase.
"""


class CompilerError(Exception):
    """Base class for all compiler errors."""

    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self.format_message())

    def format_message(self):
        """Format error message with line and column information."""
        if self.line is not None and self.column is not None:
            return f"Line {self.line}, Column {self.column}: {self.message}"
        elif self.line is not None:
            return f"Line {self.line}: {self.message}"
        return self.message


class LexerError(CompilerError):
    """Raised when the lexer encounters invalid characters or tokens."""

    pass


class ParseError(CompilerError):
    """Raised when the parser encounters syntax violations."""

    pass


class SemanticError(CompilerError):
    """Raised for type mismatches, undeclared variables, etc."""

    pass


class IRError(CompilerError):
    """Raised during IR generation."""

    pass


class RuntimeError(CompilerError):
    """Raised during interpreter execution (division by zero, etc.)."""

    pass


class CodeGenError(CompilerError):
    """Raised during assembly code generation."""

    pass
