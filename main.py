#!/usr/bin/env python3
"""
PatternLang Compiler - Main Entry Point

Orchestrates all six phases of compilation:
1. Lexical Analysis
2. Syntax Analysis
3. Semantic Analysis
4. IR Generation
5. Optimization
6. Interpretation/Execution
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
from patternlang.utils.errors import CompilerError


def compile_and_run(source_code, verbose=False):
    """
    Compile and execute PatternLang source code.

    Args:
        source_code: String containing PatternLang code
        verbose: If True, print intermediate results from each phase
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

        # Phase 6: Interpretation/Execution
        if verbose:
            print("=" * 60)
            print("PHASE 6: EXECUTION")
            print("=" * 60)
            print("Output:")

        interpreter = Interpreter()
        interpreter.execute(optimized_ir)

        if verbose:
            print()
            print("=" * 60)
            print("EXECUTION COMPLETE")
            print("=" * 60)

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
  python main.py program.pl              # Run program
  python main.py program.pl --verbose    # Show all compilation phases
  python main.py --help                  # Show this help message
        """,
    )

    parser.add_argument("file", type=str, help="PatternLang source file (.pl)")

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed output from each compiler phase",
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

    # Compile and run
    compile_and_run(source_code, verbose=args.verbose)


if __name__ == "__main__":
    main()
