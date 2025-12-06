# 🚀 Compiler Project – Copilot Instructions

These instructions tell GitHub Copilot **how to assist in building the PatternLang compiler** in Python.
The compiler must follow the **seven standard phases** of compilation, follow a **simple and minimalistic architecture**, and generate **clean, readable, well-commented code**.

---

# 📌 1. Project Overview

This repository contains the **PatternLang compiler**, written in Python.
Copilot should help generate code that is:

- Simple
- Modular
- Easy to read
- Easy to demo in a viva
- Matches compiler theory concepts (lexer → parser → AST → semantic analysis → IR → optimizer → assembly codegen → interpreter)

PatternLang is a **numerical pattern generation language** with:

- Variable declarations
- Integer arithmetic
- Repetition loops
- If-statements
- Print statements

Example program:

```
let n = 5;
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

# 📌 2. Project Structure (Copilot must follow)

Copilot must generate code in this directory structure:

```
patternlang/
    lexer.py
    tokens.py
    parser.py
    ast_nodes.py
    semantic.py
    ir.py
    optimizer.py
    assembler.py
    interpreter.py
    main.py
    utils/
        errors.py
        symbol_table.py
tests/
    sample_*.pl
    conditional_*.pl
    run_tests.py
    test_assembly.py
outputs/
    *.asm
    *.o
docs/
    ASSEMBLY_GENERATION.md
GRAMMAR.md
DEMO.md
README.md
.github/copilot-instructions.md
```

Copilot should **never** merge phases into a single file.

---

# 📌 3. Language Specification (Copilot Reference)

### ✔ Keywords

- `let`
- `repeat`
- `in`
- `print`
- `if`
- `goto`
- `end`

### ✔ Tokens

- Identifiers (`[a-zA-Z_][a-zA-Z0-9_]*`)
- Integers
- Operators: `+ - * / = == != < > <= >=`
- Symbols: `; , { } ( ) ..`

### ✔ Grammar (EBNF)

Copilot must follow this grammar exactly:

```
program        ::= stmt_list "end" ";"

stmt_list      ::= { statement }

statement      ::= var_decl
                  | assignment
                  | repeat_stmt
                  | if_stmt
                  | print_stmt

var_decl       ::= "let" IDENT "=" expr ";"
assignment     ::= "let" IDENT "=" expr ";"

repeat_stmt    ::= "repeat" IDENT "in" expr ".." expr "{" stmt_list "}"

if_stmt        ::= "if" expr "goto" IDENT ";"

print_stmt     ::= "print" expr ";"

expr           ::= term { ("+" | "-") term }
term           ::= factor { ("*" | "/") factor }
factor         ::= NUMBER | IDENT | "(" expr ")"
```

---

# 📌 4. Compiler Phases – What Copilot Must Generate

## 4.1 Lexical Analysis (`lexer.py`)

Copilot must:

- Build a simple manual lexer
- Use regex groups for tokens
- Emit tokens as `(type, value, line, column)`
- Ignore whitespace & comments

---

## 4.2 Syntax Analysis (`parser.py`)

Copilot must create:

- A **recursive descent parser** (simple, nothing fancy)
- One method per grammar rule
- Return **AST nodes** (defined in `ast_nodes.py`)
- Raise readable syntax errors

---

## 4.3 AST Nodes (`ast_nodes.py`)

Copilot must define minimalistic classes:

```
Program
VarDecl
Assign
Repeat
If
Print
BinaryOp
Identifier
Number
```

Each node must have:

- Fields
- A readable `__repr__`

---

## 4.4 Semantic Analysis (`semantic.py`)

Copilot must:

- Build a **symbol table**
- Ensure variables declared before use
- Ensure no redeclaration in the same scope
- Ensure types are integers (PatternLang is integer-only)
- Produce typed AST (attach "int" type)

Symbol table is in `utils/symbol_table.py`.

---

## 4.5 Intermediate Representation (`ir.py`)

Copilot must emit **three-address code (3AC)**:

Example IR instruction formats:

```
t1 = a + b
t2 = 1
if t1 < t2 goto L3
goto L4
label L3
```

---

## 4.6 Optimization (`optimizer.py`)

Copilot must support:

- Constant folding (`3 + 4 → 7`)
- Algebraic simplification (`x + 0 → x`)
- Dead code elimination where possible

Keep it simple.

---

## 4.7 Assembly Code Generation (`assembler.py`)

Copilot must generate:

- x86-64 NASM assembly from TAC
- Proper stack frame management (rbp, rsp)
- Register allocation for operations
- System calls for I/O (printf)
- Proper exit sequence

Assembly generator should:

- Map TAC instructions to assembly
- Handle arithmetic (+, -, \*, /)
- Handle comparisons (==, !=, <, >, <=, >=)
- Handle jumps and labels
- Handle print statements (via printf)
- Store variables on stack with rbp-relative addressing

---

## 4.8 Interpreter (`interpreter.py`)

Copilot must generate:

- A simple stack-based interpreter
- Direct execution of IR (alternative to assembly)

Interpreter must support:

- Variables
- Labels
- Arithmetic
- Jumps
- Loops
- Print

---

## 4.9 Command Line Interface (`main.py`)

Copilot must implement:

```
python main.py program.pl              # Interpret
python main.py program.pl --compile    # Generate assembly
```

Steps:

1. Load file
2. Lex
3. Parse
4. Semantic check
5. Convert to IR
6. Optimize
7. Generate assembly (if --compile) OR interpret/run

---

# 📌 5. Copilot Coding Rules (Important)

Copilot must follow these constraints:

### ✔ **Keep code simple**

Avoid overly abstract class hierarchies.

### ✔ **Every module must be short and readable**

Prefer clarity over cleverness.

### ✔ **Every function must have docstrings**

Explain purpose and phase.

### ✔ **All errors must be readable**

Use `utils/errors.py`.

### ✔ **Do not create unnecessary features**

No floats
No nested scopes (except functions)
No arrays
No type coercion

### ✔ **Use Python only**

No external dependencies except `re`.
Optional external tools: NASM for assembly, GCC for linking.

---

# 📌 6. Prompts Copilot Should Respond To (For You to Use)

Inside VS Code you can trigger Copilot with prompts like:

### **For lexer**

> "Generate the token specification and basic lexer class for PatternLang based on COPILOT_INSTRUCTIONS.md."

### **For parser**

> "Implement recursive descent methods for all grammar rules listed in COPILOT_INSTRUCTIONS.md."

### **For AST**

> "Create minimal AST node classes for each construct defined in PatternLang."

### **For semantic analysis**

> "Implement a symbol table and semantic checker enforcing integer-only rules."

### **For IR**

> "Generate three-address code classes and basic instruction formats."

### **For optimizer**

> "Implement constant folding and algebraic simplification."

### **For assembly generator**

> "Generate x86-64 NASM assembly code from three-address code with proper stack management."

### **For interpreter**

> "Write a simple stack-based interpreter to execute the IR instructions."

### **For CLI**

> "Generate main.py that processes PatternLang code through all compiler phases and executes it."

---

# 📌 7. Definition of DONE (Copilot must work toward this)

The compiler is complete when:

- It reads `.pl` files
- No crashes or unhandled exceptions
- Lexing, parsing, semantic analysis work on at least 3 test programs
- IR generated and optimized
- Interpreter runs correctly
- Assembly generation produces valid x86-64 NASM code
- Code is clean, modular, commented
- Tests in `tests/` pass
- Tests in `tests/` pass

---

# 📌 8. What Copilot Should Avoid

- Avoid excessive abstraction
- Avoid adding features outside the spec
- Avoid generating huge files
- Avoid introducing missing grammar constructs
- Avoid writing code in one file
- Avoid global variables (except simple counters for temporary names)
