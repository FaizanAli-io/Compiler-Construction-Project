"""
Interpreter for PatternLang IR.
Executes three-address code instructions.
"""

from .ir import IRInstruction


class Interpreter:
    """
    Executes three-address code on a simple virtual machine.
    Maintains runtime state including variables and instruction pointer.
    """

    def __init__(self):
        self.variables = {}
        self.instructions = []
        self.ip = 0  # Instruction pointer
        self.labels = {}  # Map label names to instruction indices

    def execute(self, instructions):
        """
        Main execution entry point.
        Runs all instructions sequentially.
        """
        self.instructions = instructions
        self.ip = 0
        self.variables = {}

        # Build label map
        self.build_label_map()

        # Execute instructions
        while self.ip < len(self.instructions):
            instr = self.instructions[self.ip]
            self.execute_instruction(instr)
            self.ip += 1

    def build_label_map(self):
        """Build a mapping of label names to instruction indices."""
        self.labels = {}
        for i, instr in enumerate(self.instructions):
            if instr.op == "label":
                self.labels[instr.result] = i

    def execute_instruction(self, instr):
        """Execute a single instruction."""
        if instr.op == "assign":
            # result = arg1
            value = self.get_value(instr.arg1)
            self.variables[instr.result] = value

        elif instr.op in ["+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="]:
            # result = arg1 op arg2
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            result = self.compute_op(instr.op, val1, val2)
            self.variables[instr.result] = result

        elif instr.op == "print":
            # Print arg1
            value = self.get_value(instr.arg1)
            print(value)

        elif instr.op == "goto":
            # Jump to label
            label = instr.arg1
            if label in self.labels:
                self.ip = self.labels[label] - 1  # -1 because ip will be incremented
            else:
                raise RuntimeError(f"Undefined label: {label}")

        elif instr.op == "if_false":
            # if_false condition goto label
            condition = self.get_value(instr.arg1)
            if not condition:
                label = instr.arg2
                if label in self.labels:
                    self.ip = self.labels[label] - 1
                else:
                    raise RuntimeError(f"Undefined label: {label}")

        elif instr.op == "label":
            # Label marker - no operation
            pass

        else:
            raise RuntimeError(f"Unknown instruction: {instr.op}")

    def get_value(self, operand):
        """
        Get the value of an operand.
        Returns integer value for constants or variables.
        """
        # Try to parse as constant
        try:
            return int(operand)
        except (ValueError, TypeError):
            pass

        # Look up variable
        if operand in self.variables:
            return self.variables[operand]

        # Undefined variable
        raise RuntimeError(f"Undefined variable: {operand}")

    def compute_op(self, op, val1, val2):
        """Compute the result of an operation."""
        if op == "+":
            return val1 + val2
        elif op == "-":
            return val1 - val2
        elif op == "*":
            return val1 * val2
        elif op == "/":
            if val2 == 0:
                raise RuntimeError("Division by zero")
            return val1 // val2  # Integer division
        elif op == "==":
            return 1 if val1 == val2 else 0
        elif op == "!=":
            return 1 if val1 != val2 else 0
        elif op == "<":
            return 1 if val1 < val2 else 0
        elif op == ">":
            return 1 if val1 > val2 else 0
        elif op == "<=":
            return 1 if val1 <= val2 else 0
        elif op == ">=":
            return 1 if val1 >= val2 else 0
        else:
            raise RuntimeError(f"Unknown operator: {op}")
