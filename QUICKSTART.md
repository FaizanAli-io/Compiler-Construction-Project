# 🚀 PatternLang Compiler - Quick Start Guide

## What is PatternLang?

PatternLang is a simple programming language designed for generating numerical patterns. It's perfect for demonstrating compiler construction principles.

## Installation

No installation required! The compiler uses only Python's standard library.

```bash
# Just make sure you have Python 3.8+
python --version
```

## Running Your First Program

1. **Create a PatternLang file** (e.g., `myprogram.pl`):

```patternlang
let n = 5;
let x = 1;

repeat i in 1..n {
    print x;
    let x = x + 2;
}

end;
```

2. **Run it**:

```bash
python main.py myprogram.pl
```

3. **Output**:

```
1
3
5
7
9
```

## Language Features

### Variable Declaration

```patternlang
let x = 10;
let y = x + 5;
```

### Loops

```patternlang
repeat i in 1..10 {
    print i;
}
```

### Arithmetic

```patternlang
let a = 5 + 3;
let b = a * 2;
let c = b - 1;
let d = c / 2;
```

### Comments

```patternlang
# This is a comment
let x = 5;  # Comments can go here too
```

## Example Programs

### Fibonacci Sequence

```patternlang
let n = 10;
let a = 0;
let b = 1;

repeat i in 1..n {
    print a;
    let t = a + b;
    let a = b;
    let b = t;
}

end;
```

### Triangular Numbers

```patternlang
let n = 10;
let sum = 0;

repeat i in 1..n {
    let sum = sum + i;
    print sum;
}

end;
```

## Debugging with Verbose Mode

See what happens at each compiler phase:

```bash
python main.py myprogram.pl --verbose
```

This shows:

1. **Lexical Analysis** - Tokens generated
2. **Syntax Analysis** - Abstract Syntax Tree
3. **Semantic Analysis** - Symbol table
4. **IR Generation** - Three-address code
5. **Optimization** - Optimized IR
6. **Execution** - Final output

## Running Tests

Test all sample programs:

```bash
python tests/run_tests.py
```

## Language Rules

- All programs must end with `end;`
- Variables must be declared with `let` before use
- All values are integers (no floats)
- Variables can be reassigned using `let` again
- Loop ranges are inclusive (1..5 includes 5)

## Common Patterns

**Squares:**

```patternlang
let n = 5;
repeat i in 1..n {
    let square = i * i;
    print square;
}
end;
```

**Countdown:**

```patternlang
let start = 10;
let countdown = start;

repeat i in 1..start {
    print countdown;
    let countdown = countdown - 1;
}
end;
```

## Getting Help

```bash
python main.py --help
```

## Project Structure

```
patternlang/          # Compiler source code
  lexer.py           # Phase 1: Tokenization
  parser.py          # Phase 2: AST generation
  semantic.py        # Phase 3: Type checking
  ir.py              # Phase 4: IR generation
  optimizer.py       # Phase 5: Optimization
  interpreter.py     # Phase 6: Execution
tests/               # Sample programs
main.py              # Entry point
```

## Next Steps

1. Try the sample programs in `tests/`
2. Write your own patterns
3. Use `--verbose` to understand compilation
4. Explore the source code in `patternlang/`

Happy pattern making! 🎨
