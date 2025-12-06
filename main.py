#!/usr/bin/env python3
"""
PatternLang Compiler - Main Entry Point

Orchestrates all seven phases of compilation:
1. Lexical Analysis
2. Syntax Analysis
3. Semantic Analysis
4. IR Generation
5. Optimization
6. Code Generation (Assembly)
7. Interpretation/Execution
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from patternlang import (
    Lexer,
    Parser,
    SemanticAnalyzer,
    IRGenerator,
    Optimizer,
    Interpreter,
)
from patternlang.assembler import generate_assembly, assemble_to_object, link_executable
from patternlang.utils.errors import CompilerError


def compile_and_run(source_code, verbose=False, output_path=None, compile_only=False):
    """
    Compile and execute PatternLang source code.

    Args:
        source_code: String containing PatternLang code
        verbose: If True, print intermediate results from each phase
        output_path: If provided, generate assembly/object files at this path
        compile_only: If True, generate assembly without executing

    Returns:
        Tuple of (asm_path, obj_path, exe_path) if compiling, None if interpreting
    """
    try:
        # Phase 1: Lexical Analysis
        if verbose:
            print("=" * 60)
            print("PHASE 1: LEXICAL ANALYSIS")
            print("=" * 60)

        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        if verbose:
            print(f"Generated {len(tokens)} tokens:")
            for token in tokens[:20]:  # Show first 20 tokens
                print(f"  {token}")
            if len(tokens) > 20:
                print(f"  ... and {len(tokens) - 20} more")
            print()

        # Phase 2: Syntax Analysis
        if verbose:
            print("=" * 60)
            print("PHASE 2: SYNTAX ANALYSIS")
            print("=" * 60)

        parser = Parser(tokens)
        ast = parser.parse()

        if verbose:
            print("Abstract Syntax Tree:")
            print(f"  {ast}")
            print()

        # Phase 3: Semantic Analysis
        if verbose:
            print("=" * 60)
            print("PHASE 3: SEMANTIC ANALYSIS")
            print("=" * 60)

        semantic_analyzer = SemanticAnalyzer()
        symbol_table = semantic_analyzer.analyze(ast)

        if verbose:
            print("Symbol Table:")
            print(f"  {symbol_table}")
            print()

        # Phase 4: IR Generation
        if verbose:
            print("=" * 60)
            print("PHASE 4: INTERMEDIATE REPRESENTATION")
            print("=" * 60)

        ir_generator = IRGenerator()
        ir_code = ir_generator.generate(ast)

        if verbose:
            print("Three-Address Code:")
            for instr in ir_code:
                print(f"  {instr}")
            print()

        # Phase 5: Optimization
        if verbose:
            print("=" * 60)
            print("PHASE 5: OPTIMIZATION")
            print("=" * 60)

        optimizer = Optimizer()
        optimized_ir = optimizer.optimize(ir_code)

        if verbose:
            print("Optimized IR:")
            for instr in optimized_ir:
                print(f"  {instr}")
            print()

        # Phase 6: Code Generation (if requested)
        if output_path or compile_only:
            if verbose:
                print("=" * 60)
                print("PHASE 6: CODE GENERATION (ASSEMBLY)")
                print("=" * 60)

            # Generate assembly file
            asm_path = output_path or "output.asm"
            if not asm_path.endswith(".asm"):
                asm_path = asm_path.replace(".pl", ".asm")

            generate_assembly(optimized_ir, asm_path)

            if verbose:
                print(f"Assembly file generated: {asm_path}")

            # Assemble to object file
            obj_path = asm_path.replace(".asm", ".o")
            obj_result = assemble_to_object(asm_path, obj_path)

            if obj_result and verbose:
                print(f"Object file generated: {obj_path}")

            # Link to executable (optional)
            exe_path = None
            if obj_result:
                exe_path = asm_path.replace(
                    ".asm", ".exe" if sys.platform == "win32" else ""
                )
                exe_result = link_executable(obj_path, exe_path)
                if exe_result and verbose:
                    print(f"Executable generated: {exe_path}")

            if verbose:
                print()

            return (asm_path, obj_result, exe_path)

        # Phase 7: Interpretation/Execution (default mode)
        if not compile_only:
            if verbose:
                print("=" * 60)
                print("PHASE 7: EXECUTION")
                print("=" * 60)
                print("Output:")

            interpreter = Interpreter()
            interpreter.execute(optimized_ir)

            if verbose:
                print()
                print("=" * 60)
                print("EXECUTION COMPLETE")
                print("=" * 60)

        return None

    except CompilerError as e:
        print(f"Compiler Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PatternLang Compiler - Compile and execute PatternLang programs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py program.pl                      # Run program (interpret)
  python main.py program.pl --verbose            # Show all compilation phases
  python main.py program.pl --compile            # Generate assembly and compile
  python main.py program.pl -c -o outputs/prog   # Compile to specific output
  python main.py --help                          # Show this help message
        """,
    )

    parser.add_argument("file", type=str, help="PatternLang source file (.pl)")

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed output from each compiler phase",
    )

    parser.add_argument(
        "-c",
        "--compile",
        action="store_true",
        help="Generate assembly and object files instead of interpreting",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output path for assembly file (default: outputs/<filename>.asm)",
    )

    args = parser.parse_args()

    # Read source file
    source_path = Path(args.file)

    if not source_path.exists():
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        sys.exit(1)

    if not source_path.suffix == ".pl":
        print(f"Warning: File extension is not .pl", file=sys.stderr)

    try:
        source_code = source_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    # Determine output path if compiling
    output_path = None
    if args.compile or args.output:
        if args.output:
            output_path = args.output
        else:
            # Default: outputs/<filename>.asm
            outputs_dir = Path("outputs")
            outputs_dir.mkdir(exist_ok=True)
            output_path = str(outputs_dir / source_path.stem) + ".asm"

    # Compile and run
    result = compile_and_run(
        source_code,
        verbose=args.verbose,
        output_path=output_path,
        compile_only=args.compile,
    )

    if result and not args.verbose:
        asm_path, obj_path, exe_path = result
        print(f"Generated: {asm_path}")
        if obj_path:
            print(f"Generated: {obj_path}")
        if exe_path:
            print(f"Generated: {exe_path}")


if __name__ == "__main__":
    main()
