"""
Abstract Syntax Tree (AST) node definitions for PatternLang.
Each node represents a construct in the language.
"""


class ASTNode:
    """Base class for all AST nodes."""

    pass


class Program(ASTNode):
    """Root node representing the entire program."""

    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program({self.statements})"


class VarDecl(ASTNode):
    """Variable declaration: let x = expr;"""

    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __repr__(self):
        return f"VarDecl({self.name}, {self.expression})"


class Assign(ASTNode):
    """Assignment (same as declaration in PatternLang): let x = expr;"""

    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __repr__(self):
        return f"Assign({self.name}, {self.expression})"


class Repeat(ASTNode):
    """Repeat loop: repeat i in start..end { statements }"""

    def __init__(self, variable, start_expr, end_expr, body):
        self.variable = variable
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.body = body

    def __repr__(self):
        return (
            f"Repeat({self.variable}, {self.start_expr}..{self.end_expr}, {self.body})"
        )


class If(ASTNode):
    """Conditional jump: if expr goto label;"""

    def __init__(self, condition, label):
        self.condition = condition
        self.label = label

    def __repr__(self):
        return f"If({self.condition}, goto {self.label})"


class Print(ASTNode):
    """Print statement: print expr;"""

    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"Print({self.expression})"


class BinaryOp(ASTNode):
    """Binary operation: left op right"""

    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinaryOp({self.operator}, {self.left}, {self.right})"


class Identifier(ASTNode):
    """Variable identifier."""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"


class Number(ASTNode):
    """Numeric literal."""

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"
