# 🌀 PatternLang Compiler

### _A Mini-Compiler in Python for PatternLang — An Arithmetic Pattern Generation Language_

---

## 📘 Overview

This project is a fully functional **mini-compiler** for **PatternLang**, a small domain-specific language designed to generate numerical patterns using arithmetic logic, loops, and control structures.

The compiler demonstrates all **seven phases of compiler construction**:

1. **Lexical Analysis**
2. **Syntax Analysis**
3. **Semantic Analysis**
4. **Intermediate Code Generation (3AC)**
5. **Basic Optimization**
6. **Assembly Code Generation**
7. **Interpretation / Execution**

PatternLang is intentionally minimalistic, making it perfect for learning compiler design while still producing expressive and interesting numerical results such as Fibonacci sequences, factorial growth patterns, custom progressions, and more.

---

## 👨‍💻 Project Authors

This compiler was developed as a semester project for **Compiler Construction**.

- **Faizan Ali — 22i-2496**
- **Hamail Rehman — 22k-4443**
- **Sameed Rehman — 22k-xxxx**

---

## 🧩 What is PatternLang?

PatternLang is a small scripting language designed for:

- Arithmetic pattern generation
- Simple looping
- Declarative variable definitions
- Printing results
- Basic conditional jumps

A sample PatternLang program to print the Fibonacci sequence looks like this:

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

---

## 🛠️ Compiler Architecture

The project is structured according to standard compiler pipeline design:

### **1. Lexical Analysis**

- Converts source code into tokens
- Handles identifiers, numbers, operators, and keywords

### **2. Syntax Analysis**

- Implements a recursive-descent parser
- Builds an Abstract Syntax Tree (AST)

### **3. Semantic Analysis**

- Constructs a symbol table
- Ensures variables are declared before use
- Enforces PatternLang's integer-only type system

### **4. Intermediate Representation (IR)**

- Generates three-address code (3AC)
- Includes temporary variables, labels, and jumps

### **5. Optimization**

- Constant folding
- Simple algebraic simplifications
- Dead-code elimination when possible

### **6. Assembly Code Generation**

- Converts three-address code to x86-64 NASM assembly
- Generates .asm files that can be assembled into object files
- Optional: Creates executables with NASM and GCC

### **7. Interpretation / Execution**

- Executes the IR on a simple Python-based virtual machine
- Alternative to assembly generation for rapid testing
- Produces the output required by the PatternLang program

---

## 📁 Repository Structure

A typical structure for this compiler:

```
patternlang/
    lexer.py              # Lexical analyzer
    tokens.py             # Token definitions
    parser.py             # Recursive descent parser
    ast_nodes.py          # AST node classes
    semantic.py           # Semantic analyzer
    ir.py                 # Three-address code generator
    optimizer.py          # IR optimizer
    assembler.py          # Assembly code generator (NEW)
    interpreter.py        # Virtual machine executor
    utils/
        errors.py         # Custom exceptions
        symbol_table.py   # Symbol table management
tests/
    sample_*.pl           # Sample programs (13 tests)
    conditional_*.pl      # Conditional logic tests
    run_tests.py          # Interpreter test runner
    test_assembly.py      # Assembly generation tests
outputs/
    *.asm                 # Generated assembly files
    *.o                   # Object files (if NASM installed)
docs/
    ASSEMBLY_GENERATION.md
main.py
README.md
GRAMMAR.md
.github/copilot-instructions.md
```

---

## ▶️ Running the Compiler

Install dependencies (if any):

```bash
pip install -r requirements.txt
```

Run a PatternLang program:

```bash
# Basic execution (interpret)
python main.py tests/sample_fibonacci.pl

# Show all compiler phases (verbose mode)
python main.py tests/sample_fibonacci.pl --verbose

# Compile to assembly (NEW)
python main.py tests/sample_fibonacci.pl --compile

# Compile with specific output path
python main.py tests/sample_fibonacci.pl -c -o outputs/fib
```

Run all test programs:

```bash
# Test interpreter
python tests/run_tests.py

# Test assembly generation
python tests/test_assembly.py
```

---

## 🧪 Example Outputs

PatternLang can generate a wide variety of arithmetic sequences such as:

- Fibonacci
- Triangular numbers
- Factorial-based patterns
- Custom linear and non-linear progressions

---

## 📚 Educational Purpose

This project is intended to:

- Demonstrate practical implementation of compiler phases
- Show how simple languages are designed
- Provide hands-on understanding of parsing, IR, and interpretation
- Serve as a clean, minimal compiler framework for students

---

## 🏁 Status

🚧 **Active Development**
New patterns, optimizations, and features may be added throughout the semester.

---

## 📜 License

This project is created for educational purposes and may be reused or extended with attribution.

Just tell me!
