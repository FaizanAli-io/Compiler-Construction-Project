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
            "    fmt_float: db '%.6g', 10, 0  ; Float format with newline"
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
            # result = arg1 (float move)
            self._load_operand_float(instr.arg1, "xmm0")
            self._store_variable_float(instr.result, "xmm0")

        elif op == "+":
            self._binary_op_float(instr, "addsd")

        elif op == "-":
            self._binary_op_float(instr, "subsd")

        elif op == "*":
            self._binary_op_float(instr, "mulsd")

        elif op == "/":
            self._division_float(instr)

        elif op == "==":
            self._comparison_float(instr, "je")

        elif op == "!=":
            self._comparison_float(instr, "jne")

        elif op == "<":
            self._comparison_float(instr, "jl")

        elif op == ">":
            self._comparison_float(instr, "jg")

        elif op == "<=":
            self._comparison_float(instr, "jle")

        elif op == ">=":
            self._comparison_float(instr, "jge")

        elif op == "goto":
            self.assembly.append(f"    jmp {instr.arg1}")

        elif op == "if_false":
            # For floats, a zero comparison result is false
            self._load_operand_float(instr.arg1, "xmm0")
            self.assembly.append(f"    xorpd xmm1, xmm1")
            self.assembly.append(f"    comisd xmm0, xmm1")
            self.assembly.append(f"    je {instr.arg2}")

        elif op == "print":
            self._print_value_float(instr.arg1)

        elif op == "param":
            # For function calls - not implemented yet
            pass

        elif op == "call":
            # Function calls - simplified for now
            self.assembly.append(
                f"    ; call {instr.arg1} (function calls not fully implemented)"
            )

        elif op == "return":
            self._load_operand_float(instr.arg1, "xmm0")
            self.assembly.append(f"    jmp _exit")

        else:
            self.assembly.append(f"    ; Unknown operation: {op}")

    def _binary_op_float(self, instr, asm_op):
        """Generate assembly for binary floating-point operations."""
        # Load first operand into xmm0
        self._load_operand_float(instr.arg1, "xmm0")

        # Load second operand into xmm1
        self._load_operand_float(instr.arg2, "xmm1")

        # Perform operation: xmm0 op= xmm1
        self.assembly.append(f"    {asm_op} xmm0, xmm1")

        # Store result
        self._store_variable_float(instr.result, "xmm0")

    def _division_float(self, instr):
        """Generate assembly for floating-point division."""
        # Load dividend into xmm0
        self._load_operand_float(instr.arg1, "xmm0")

        # Load divisor into xmm1
        self._load_operand_float(instr.arg2, "xmm1")

        # Divide xmm0 by xmm1
        self.assembly.append(f"    divsd xmm0, xmm1")

        # Store result
        self._store_variable_float(instr.result, "xmm0")

    def _comparison_float(self, instr, jump_instruction):
        """Generate assembly for floating-point comparison operations."""
        # Load operands
        self._load_operand_float(instr.arg1, "xmm0")
        self._load_operand_float(instr.arg2, "xmm1")

        # Compare
        self.assembly.append(f"    comisd xmm0, xmm1")

        # Set result based on comparison
        # For now, store 1.0 or 0.0 based on comparison
        # This is simplified; proper implementation would use conditional moves
        temp_var = instr.result
        self.assembly.append(f"    movsd xmm0, [rel zero_const]")
        self.assembly.append(f"    movsd xmm1, [rel one_const]")
        self.assembly.append(f"    cmovne rax, rbx")
        self._store_variable_float(instr.result, "xmm0")

    def _print_value_float(self, operand):
        """Generate assembly to print a floating-point value."""
        # Load value into xmm0 (first fp argument for printf)
        self._load_operand_float(operand, "xmm0")

        # Set up printf call with float format string
        self.assembly.append(
            f"    lea rdi, [rel fmt_float]  ; First argument: format string"
        )
        self.assembly.append(f"    mov rax, 1              ; 1 floating-point arg")
        self.assembly.append(f"    push rbp                ; Align stack")
        self.assembly.append(f"    call printf")
        self.assembly.append(f"    pop rbp")

    def _load_operand_float(self, operand, register):
        """Load a floating-point operand into an XMM register."""
        try:
            # Try to parse as float constant
            val = float(operand)
            # For float constants, we need to load from data section
            # For now, use movsd with immediate (limited approach)
            self.assembly.append(f"    mov rax, {int(val * 1e6)}")
            self.assembly.append(f"    cvtsi2sd {register}, rax")
        except (ValueError, TypeError):
            # Variable lookup
            if operand in self.variables:
                offset = self.variables[operand]
                self.assembly.append(f"    movsd {register}, [rbp - {offset}]")
            else:
                # Try as integer and convert
                self.assembly.append(f"    mov rax, {operand}")
                self.assembly.append(f"    cvtsi2sd {register}, rax")

    def _store_variable_float(self, var_name, register):
        """Store an XMM register value to a float variable on the stack."""
        if var_name in self.variables:
            offset = self.variables[var_name]
            self.assembly.append(f"    movsd [rbp - {offset}], {register}")


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
