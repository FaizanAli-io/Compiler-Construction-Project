"""
Assembly Code Generator for PatternLang.
Converts three-address code (3AC) to x86-64 NASM assembly.
Phase 7: Code Generation (Assembly)
"""

import os
from .ir import IRInstruction
from .utils.errors import CodeGenError


class AssemblyGenerator:
    """
    Generates x86-64 NASM assembly code from three-address code.
    Handles register allocation, stack management, and system calls.
    """

    def __init__(self):
        self.assembly = []
        self.data_section = []
        self.variables = {}  # Maps variable names to stack offsets
        self.stack_offset = 0
        self.label_mapping = {}  # Maps IR labels to assembly labels
        self.current_function = None
        self.function_stack_size = {}

    def generate(self, instructions):
        """
        Generate complete x86-64 NASM assembly from IR instructions.
        Returns assembly code as a string.
        """
        self._analyze_instructions(instructions)
        self._emit_header()
        self._emit_data_section()
        self._emit_text_section()
        self._generate_instructions(instructions)
        self._emit_footer()

        return "\n".join(self.assembly)

    def _analyze_instructions(self, instructions):
        """
        Pre-process instructions to collect variables and labels.
        """
        for instr in instructions:
            # Collect labels
            if instr.op == "label":
                self.label_mapping[instr.result] = instr.result

            # Collect variables
            for arg in [instr.arg1, instr.arg2, instr.result]:
                if arg and isinstance(arg, str) and not arg.isdigit():
                    if arg.startswith("t") or arg.startswith("_") or arg[0].isalpha():
                        if arg not in self.variables and not arg.startswith("L"):
                            self.stack_offset += 8
                            self.variables[arg] = self.stack_offset

    def _emit_header(self):
        """Emit assembly file header and external declarations."""
        self.assembly.append("; PatternLang Compiler Output")
        self.assembly.append("; x86-64 NASM Assembly")
        self.assembly.append("")
        self.assembly.append("global _start")
        self.assembly.append("extern printf")
        self.assembly.append("")

    def _emit_data_section(self):
        """Emit data section with format strings for printing."""
        self.assembly.append("section .data")
        self.assembly.append(
            "    fmt_int: db '%d', 10, 0  ; Integer format with newline"
        )
        self.assembly.append("")

    def _emit_text_section(self):
        """Emit text section header."""
        self.assembly.append("section .text")
        self.assembly.append("")
        self.assembly.append("_start:")
        self.assembly.append(f"    push rbp")
        self.assembly.append(f"    mov rbp, rsp")
        if self.stack_offset > 0:
            self.assembly.append(
                f"    sub rsp, {self.stack_offset}  ; Allocate stack space for variables"
            )
        self.assembly.append("")

    def _emit_footer(self):
        """Emit program exit code."""
        self.assembly.append("")
        self.assembly.append("_exit:")
        self.assembly.append("    mov rsp, rbp")
        self.assembly.append("    pop rbp")
        self.assembly.append("    mov rax, 60      ; sys_exit")
        self.assembly.append("    xor rdi, rdi     ; exit code 0")
        self.assembly.append("    syscall")

    def _generate_instructions(self, instructions):
        """Generate assembly for each IR instruction."""
        for instr in instructions:
            self._generate_instruction(instr)

    def _generate_instruction(self, instr):
        """Generate assembly for a single IR instruction."""
        op = instr.op

        if op == "label":
            self.assembly.append(f"{instr.result}:")

        elif op == "assign":
            # result = arg1
            self._load_operand(instr.arg1, "rax")
            self._store_variable(instr.result, "rax")

        elif op == "+":
            self._binary_op(instr, "add")

        elif op == "-":
            self._binary_op(instr, "sub")

        elif op == "*":
            self._binary_op(instr, "imul")

        elif op == "/":
            self._division(instr)

        elif op == "==":
            self._comparison(instr, "sete")

        elif op == "!=":
            self._comparison(instr, "setne")

        elif op == "<":
            self._comparison(instr, "setl")

        elif op == ">":
            self._comparison(instr, "setg")

        elif op == "<=":
            self._comparison(instr, "setle")

        elif op == ">=":
            self._comparison(instr, "setge")

        elif op == "goto":
            self.assembly.append(f"    jmp {instr.arg1}")

        elif op == "if_false":
            self._load_operand(instr.arg1, "rax")
            self.assembly.append(f"    test rax, rax")
            self.assembly.append(f"    jz {instr.arg2}")

        elif op == "print":
            self._print_value(instr.arg1)

        elif op == "param":
            # For function calls - not implemented yet
            pass

        elif op == "call":
            # Function calls - simplified for now
            self.assembly.append(
                f"    ; call {instr.arg1} (function calls not fully implemented)"
            )

        elif op == "return":
            self._load_operand(instr.arg1, "rax")
            self.assembly.append(f"    jmp _exit")

        else:
            self.assembly.append(f"    ; Unknown operation: {op}")

    def _binary_op(self, instr, asm_op):
        """Generate assembly for binary arithmetic operations."""
        # Load first operand into rax
        self._load_operand(instr.arg1, "rax")

        # Load second operand into rbx
        self._load_operand(instr.arg2, "rbx")

        # Perform operation
        self.assembly.append(f"    {asm_op} rax, rbx")

        # Store result
        self._store_variable(instr.result, "rax")

    def _division(self, instr):
        """Generate assembly for division (requires rdx:rax setup)."""
        # Load dividend into rax
        self._load_operand(instr.arg1, "rax")

        # Sign extend rax into rdx:rax
        self.assembly.append(f"    cqo")

        # Load divisor into rbx
        self._load_operand(instr.arg2, "rbx")

        # Divide rdx:rax by rbx, quotient in rax
        self.assembly.append(f"    idiv rbx")

        # Store result
        self._store_variable(instr.result, "rax")

    def _comparison(self, instr, set_instruction):
        """Generate assembly for comparison operations."""
        # Load operands
        self._load_operand(instr.arg1, "rax")
        self._load_operand(instr.arg2, "rbx")

        # Compare
        self.assembly.append(f"    cmp rax, rbx")

        # Set result (0 or 1)
        self.assembly.append(f"    {set_instruction} al")
        self.assembly.append(f"    movzx rax, al")

        # Store result
        self._store_variable(instr.result, "rax")

    def _print_value(self, operand):
        """Generate assembly to print an integer value."""
        # Load value into rsi (second argument for printf)
        self._load_operand(operand, "rsi")

        # Set up printf call
        self.assembly.append(
            f"    lea rdi, [rel fmt_int]  ; First argument: format string"
        )
        self.assembly.append(f"    xor rax, rax            ; No floating-point args")
        self.assembly.append(f"    push rbp                ; Align stack")
        self.assembly.append(f"    call printf")
        self.assembly.append(f"    pop rbp")

    def _load_operand(self, operand, register):
        """Load an operand (constant or variable) into a register."""
        if isinstance(operand, int) or (isinstance(operand, str) and operand.isdigit()):
            # Immediate value
            self.assembly.append(f"    mov {register}, {operand}")
        elif operand in self.variables:
            # Variable on stack
            offset = self.variables[operand]
            self.assembly.append(f"    mov {register}, [rbp - {offset}]")
        else:
            # Assume it's a constant or special value
            self.assembly.append(f"    mov {register}, {operand}")

    def _store_variable(self, var_name, register):
        """Store register value to a variable on the stack."""
        if var_name in self.variables:
            offset = self.variables[var_name]
            self.assembly.append(f"    mov [rbp - {offset}], {register}")


def generate_assembly(ir_instructions, output_path):
    """
    Generate assembly file from IR instructions.

    Args:
        ir_instructions: List of IRInstruction objects
        output_path: Path to write .asm file

    Returns:
        Path to generated assembly file
    """
    generator = AssemblyGenerator()
    asm_code = generator.generate(ir_instructions)

    # Write assembly to file
    with open(output_path, "w") as f:
        f.write(asm_code)

    return output_path


def assemble_to_object(asm_path, obj_path):
    """
    Assemble .asm file to .o object file using NASM.

    Args:
        asm_path: Path to .asm file
        obj_path: Path to output .o file

    Returns:
        Path to generated object file, or None if assembly failed
    """
    import subprocess

    try:
        # Use NASM to assemble
        result = subprocess.run(
            ["nasm", "-f", "elf64", "-o", obj_path, asm_path],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise CodeGenError(f"NASM assembly failed: {result.stderr}")

        return obj_path

    except FileNotFoundError:
        print("Warning: NASM not found. Install NASM to generate object files.")
        print("Assembly file generated successfully, but object file not created.")
        return None
    except Exception as e:
        raise CodeGenError(f"Assembly failed: {e}")


def link_executable(obj_path, exe_path):
    """
    Link object file to create executable.

    Args:
        obj_path: Path to .o file
        exe_path: Path to output executable

    Returns:
        Path to generated executable, or None if linking failed
    """
    import subprocess

    try:
        # Use ld to link (on Linux) or gcc (more portable)
        result = subprocess.run(
            ["gcc", "-no-pie", "-o", exe_path, obj_path, "-lc"],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise CodeGenError(f"Linking failed: {result.stderr}")

        return exe_path

    except FileNotFoundError:
        print("Warning: GCC not found. Object file created but not linked.")
        return None
    except Exception as e:
        raise CodeGenError(f"Linking failed: {e}")
