"""
Intermediate Representation (IR) generator for PatternLang.
Converts AST to three-address code (3AC).
"""

from .ast_nodes import *
from .utils.errors import IRError


class IRInstruction:
    """Represents a single three-address code instruction."""

    def __init__(self, op, arg1=None, arg2=None, result=None):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __repr__(self):
        if self.op == "label":
            return f"{self.result}:"
        elif self.op == "goto":
            return f"goto {self.arg1}"
        elif self.op == "if_false":
            return f"if_false {self.arg1} goto {self.arg2}"
        elif self.op == "print":
            return f"print {self.arg1}"
        elif self.op == "assign":
            return f"{self.result} = {self.arg1}"
        elif self.arg2 is None:
            return f"{self.result} = {self.arg1}"
        else:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"


class IRGenerator:
    """
    Generates three-address code from AST.
    Uses temporary variables and labels.
    """

    def __init__(self):
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0

    def new_temp(self):
        """Generate a new temporary variable name."""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def new_label(self):
        """Generate a new label name."""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label

    def emit(self, op, arg1=None, arg2=None, result=None):
        """Emit a new IR instruction."""
        instruction = IRInstruction(op, arg1, arg2, result)
        self.instructions.append(instruction)
        return instruction

    def generate(self, ast):
        """Main entry point for IR generation."""
        self.visit(ast)
        return self.instructions

    def visit(self, node):
        """Dispatch to appropriate visitor method."""
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Fallback visitor."""
        raise IRError(f"No visit method for {type(node).__name__}")

    def visit_Program(self, node):
        """Visit program node."""
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VarDecl(self, node):
        """
        Visit variable declaration.
        Generates: var = expr_result
        """
        expr_result = self.visit(node.expression)
        self.emit("assign", expr_result, None, node.name)

    def visit_Assign(self, node):
        """Visit assignment (same as VarDecl)."""
        self.visit_VarDecl(node)

    def visit_Repeat(self, node):
        """
        Visit repeat loop.
        Generates:
            loop_var = start
            L_start:
            if_false (loop_var <= end) goto L_end
            ... body ...
            loop_var = loop_var + 1
            goto L_start
            L_end:
        """
        start_result = self.visit(node.start_expr)
        end_result = self.visit(node.end_expr)

        # Initialize loop variable
        self.emit("assign", start_result, None, node.variable)

        # Labels
        start_label = self.new_label()
        end_label = self.new_label()

        # Start of loop
        self.emit("label", None, None, start_label)

        # Condition check: loop_var <= end
        cond_temp = self.new_temp()
        self.emit("<=", node.variable, end_result, cond_temp)
        self.emit("if_false", cond_temp, end_label, None)

        # Body
        for stmt in node.body:
            self.visit(stmt)

        # Increment loop variable
        increment_temp = self.new_temp()
        self.emit("+", node.variable, "1", increment_temp)
        self.emit("assign", increment_temp, None, node.variable)

        # Jump back to start
        self.emit("goto", start_label, None, None)

        # End label
        self.emit("label", None, None, end_label)

    def visit_If(self, node):
        """
        Visit if statement.
        Generates:
            if_false condition goto else_label
            goto target_label
            else_label:
        """
        cond_result = self.visit(node.condition)
        else_label = self.new_label()

        self.emit("if_false", cond_result, else_label, None)
        self.emit("goto", node.label, None, None)
        self.emit("label", None, None, else_label)

    def visit_Print(self, node):
        """Visit print statement."""
        expr_result = self.visit(node.expression)
        self.emit("print", expr_result, None, None)

    def visit_BinaryOp(self, node):
        """
        Visit binary operation.
        Generates: temp = left op right
        Returns the temporary variable.
        """
        left_result = self.visit(node.left)
        right_result = self.visit(node.right)

        temp = self.new_temp()

        # Map operator names to symbols
        op_map = {
            "PLUS": "+",
            "MINUS": "-",
            "MULTIPLY": "*",
            "DIVIDE": "/",
            "EQUAL": "==",
            "NOT_EQUAL": "!=",
            "LESS_THAN": "<",
            "GREATER_THAN": ">",
            "LESS_EQUAL": "<=",
            "GREATER_EQUAL": ">=",
        }

        op_symbol = op_map.get(node.operator, node.operator)
        self.emit(op_symbol, left_result, right_result, temp)

        return temp

    def visit_Identifier(self, node):
        """Visit identifier - return the variable name."""
        return node.name

    def visit_Number(self, node):
        """Visit number - return the value as string."""
        return str(node.value)
