"""
Semantic analyzer for PatternLang.
Performs type checking and ensures variables are declared before use.
"""

from .ast_nodes import *
from .utils.symbol_table import SymbolTable
from .utils.errors import SemanticError


class SemanticAnalyzer:
    """
    Validates the AST and builds a symbol table.
    Ensures PatternLang's integer-only type system is enforced.
    """

    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []

    def analyze(self, ast):
        """
        Main entry point for semantic analysis.
        Returns the symbol table if successful.
        """
        self.visit(ast)

        if self.errors:
            # Report all errors
            error_messages = "\n".join(str(e) for e in self.errors)
            raise SemanticError(f"Semantic errors found:\n{error_messages}")

        return self.symbol_table

    def visit(self, node):
        """Dispatch to appropriate visitor method."""
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Fallback visitor."""
        raise SemanticError(f"No visit method for {type(node).__name__}")

    def visit_Program(self, node):
        """Visit program node."""
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VarDecl(self, node):
        """
        Visit variable declaration.
        Ensures variable is not already declared in current scope.
        """
        # Check if already declared
        if not self.symbol_table.declare(node.name, "int"):
            self.errors.append(
                SemanticError(f"Variable '{node.name}' already declared in this scope")
            )

        # Visit the expression
        self.visit(node.expression)

    def visit_Assign(self, node):
        """Visit assignment (same as VarDecl in PatternLang)."""
        self.visit_VarDecl(node)

    def visit_Repeat(self, node):
        """
        Visit repeat loop.
        Creates a new scope for the loop variable.
        """
        # Visit start and end expressions
        self.visit(node.start_expr)
        self.visit(node.end_expr)

        # Enter new scope for loop
        self.symbol_table.enter_scope()

        # Declare loop variable
        if not self.symbol_table.declare(node.variable, "int"):
            self.errors.append(
                SemanticError(
                    f"Loop variable '{node.variable}' conflicts with existing variable"
                )
            )

        # Visit loop body
        for stmt in node.body:
            self.visit(stmt)

        # Exit loop scope
        self.symbol_table.exit_scope()

    def visit_If(self, node):
        """Visit if statement."""
        self.visit(node.condition)
        # Note: We don't validate label existence here (could be added)

    def visit_Print(self, node):
        """Visit print statement."""
        self.visit(node.expression)

    def visit_BinaryOp(self, node):
        """
        Visit binary operation.
        Ensures both operands are valid.
        """
        self.visit(node.left)
        self.visit(node.right)
        # Type checking: all operations result in integers

    def visit_Identifier(self, node):
        """
        Visit identifier.
        Ensures variable has been declared.
        """
        symbol = self.symbol_table.lookup(node.name)
        if symbol is None:
            self.errors.append(
                SemanticError(f"Variable '{node.name}' used before declaration")
            )

    def visit_Number(self, node):
        """Visit number literal (always valid)."""
        pass

    def visit_FunctionDef(self, node):
        """Register function and check its body in a new scope."""
        # Functions share global namespace for names; record name to prevent duplicates
        if not hasattr(self, "functions"):
            self.functions = {}
        if node.name in self.functions:
            self.errors.append(SemanticError(f"Function '{node.name}' redeclared"))
        else:
            self.functions[node.name] = node
        # Enter function scope
        self.symbol_table.enter_scope()
        # Declare parameters
        for p in node.params:
            if not self.symbol_table.declare(p, "int"):
                self.errors.append(SemanticError(f"Parameter '{p}' redeclared"))
        # Visit body
        for stmt in node.body:
            self.visit(stmt)
        # Exit scope
        self.symbol_table.exit_scope()

    def visit_Return(self, node):
        """Validate return expression."""
        self.visit(node.expression)

    def visit_Call(self, node):
        """Validate call arguments (assume function exists for now)."""
        # Verify function exists if registry available and arity matches
        if hasattr(self, "functions") and node.name in self.functions:
            func = self.functions[node.name]
            if len(node.args) != len(func.params):
                self.errors.append(
                    SemanticError(
                        f"Function '{node.name}' expects {len(func.params)} argument(s), got {len(node.args)}"
                    )
                )
        for arg in node.args:
            self.visit(arg)

    def visit_Label(self, node):
        """Label statement - no validation needed."""
        pass
