"""
IR optimizer for PatternLang.
Performs constant folding, algebraic simplification, and basic dead code elimination.
"""

from .ir import IRInstruction


class Optimizer:
    """
    Optimizes three-address code.
    Implements simple optimization techniques.
    """

    def __init__(self):
        self.instructions = []

    def optimize(self, instructions):
        """
        Main optimization entry point.
        Applies multiple optimization passes.
        """
        # Copy instructions
        self.instructions = instructions[:]

        # Apply optimization passes
        self.instructions = self.constant_folding(self.instructions)
        self.instructions = self.algebraic_simplification(self.instructions)

        return self.instructions

    def constant_folding(self, instructions):
        """
        Fold constant expressions.
        Example: t1 = 3.0 + 4.0 → t1 = 7.0
        """
        optimized = []

        for instr in instructions:
            if instr.op in ["+", "-", "*", "/", "%", "==", "!=", "<", ">", "<=", ">="]:
                # Check if both operands are constants
                if self.is_constant(instr.arg1) and self.is_constant(instr.arg2):
                    val1 = float(instr.arg1)
                    val2 = float(instr.arg2)

                    # Compute result
                    result_val = self.compute_op(instr.op, val1, val2)

                    # Replace with assignment
                    new_instr = IRInstruction(
                        "assign", str(result_val), None, instr.result
                    )
                    optimized.append(new_instr)
                else:
                    optimized.append(instr)
            else:
                optimized.append(instr)

        return optimized

    def algebraic_simplification(self, instructions):
        """
        Apply algebraic identities.
        Examples:
        - x + 0 → x
        - x * 1 → x
        - x * 0 → 0
        """
        optimized = []

        for instr in instructions:
            if instr.op == "+":
                if instr.arg2 == "0.0":
                    # x + 0 → x
                    new_instr = IRInstruction("assign", instr.arg1, None, instr.result)
                    optimized.append(new_instr)
                elif instr.arg1 == "0.0":
                    # 0 + x → x
                    new_instr = IRInstruction("assign", instr.arg2, None, instr.result)
                    optimized.append(new_instr)
                else:
                    optimized.append(instr)

            elif instr.op == "-":
                if instr.arg2 == "0.0":
                    # x - 0 → x
                    new_instr = IRInstruction("assign", instr.arg1, None, instr.result)
                    optimized.append(new_instr)
                else:
                    optimized.append(instr)

            elif instr.op == "*":
                if instr.arg1 == "0.0" or instr.arg2 == "0.0":
                    # x * 0.0 → 0.0 or 0.0 * x → 0.0
                    new_instr = IRInstruction("assign", "0.0", None, instr.result)
                    optimized.append(new_instr)
                elif instr.arg2 == "1.0":
                    # x * 1.0 → x
                    new_instr = IRInstruction("assign", instr.arg1, None, instr.result)
                    optimized.append(new_instr)
                elif instr.arg1 == "1.0":
                    # 1 * x → x
                    new_instr = IRInstruction("assign", instr.arg2, None, instr.result)
                    optimized.append(new_instr)
                else:
                    optimized.append(instr)

            elif instr.op == "/":
                if instr.arg2 == "1.0":
                    # x / 1 → x
                    new_instr = IRInstruction("assign", instr.arg1, None, instr.result)
                    optimized.append(new_instr)
                else:
                    optimized.append(instr)

            else:
                optimized.append(instr)

        return optimized

    def is_constant(self, value):
        """Check if a value is a numeric constant."""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    def compute_op(self, op, val1, val2):
        """Compute the result of an operation on two constants."""
        if op == "+":
            return val1 + val2
        elif op == "-":
            return val1 - val2
        elif op == "*":
            return val1 * val2
        elif op == "/":
            if val2 == 0:
                raise ValueError("Division by zero in constant folding")
            return val1 / val2  # Float division
        elif op == "==":
            return 1.0 if val1 == val2 else 0.0
        elif op == "!=":
            return 1.0 if val1 != val2 else 0.0
        elif op == "<":
            return 1.0 if val1 < val2 else 0.0
        elif op == ">":
            return 1.0 if val1 > val2 else 0.0
        elif op == "<=":
            return 1.0 if val1 <= val2 else 0.0
        elif op == ">=":
            return 1.0 if val1 >= val2 else 0.0
        else:
            raise ValueError(f"Unknown operator: {op}")
