"""
Interpreter for PatternLang IR.
Executes three-address code instructions.
"""


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
        self.call_stack = []  # stack of frames: {return_ip, locals}
        self.arg_stack = []  # argument stack for calls
        self.return_value = 0

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

        elif instr.op in ["+", "-", "*", "/", "%", "==", "!=", "<", ">", "<=", ">="]:
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
        elif instr.op == "push":
            # Push argument value onto arg stack
            value = self.get_value(instr.arg1)
            self.arg_stack.append(value)
        elif instr.op == "call":
            # arg1: target label, arg2: arg count
            target = instr.arg1
            argc = instr.arg2 or 0
            # Save current frame
            self.call_stack.append(
                {"return_ip": self.ip, "locals": self.variables.copy()}
            )
            # Bind parameters: interpreter will map by reading parameter names from function label context
            # Since IR doesn't carry parameter names, we'll set special array _args
            self.variables = {"_args": list(self.arg_stack[-argc:])}
            # Consume args
            for _ in range(argc):
                self.arg_stack.pop()
            # Jump to function label
            if target in self.labels:
                self.ip = self.labels[target]
            else:
                raise RuntimeError(f"Undefined function label: {target}")
        elif instr.op == "ret":
            # Set return value and restore previous frame
            self.return_value = self.get_value(instr.arg1)
            if not self.call_stack:
                # return from top-level: ignore
                return
            frame = self.call_stack.pop()
            self.variables = frame["locals"]
            # Set ip to return_ip (will increment to next instruction)
            self.ip = frame["return_ip"]
        elif instr.op == "getret":
            # Move return_value into a variable
            self.variables[instr.result] = self.return_value

        else:
            raise RuntimeError(f"Unknown instruction: {instr.op}")

    def get_value(self, operand):
        """
        Get the value of an operand.
        Returns float value for constants or variables.
        """
        # Try to parse as constant
        try:
            return float(operand)
        except (ValueError, TypeError):
            pass

        # Look up variable
        if operand in self.variables:
            return self.variables[operand]

        # Undefined variable
        # Special case: arguments array lookup _args[i]
        if (
            isinstance(operand, str)
            and operand.startswith("_args[")
            and operand.endswith("]")
        ):
            idx = int(operand[6:-1])
            args = self.variables.get("_args", [])
            if 0 <= idx < len(args):
                return args[idx]
            return 0.0
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
            return val1 / val2  # Float division
        elif op == "%":
            return val1 % val2
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
            raise RuntimeError(f"Unknown operator: {op}")
