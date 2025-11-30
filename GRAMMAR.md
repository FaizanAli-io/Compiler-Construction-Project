# PatternLang Grammar Specification

## Formal Grammar (EBNF)

### Program Structure

```ebnf
program        ::= stmt_list 'end' ';'

stmt_list      ::= { statement }

statement      ::= var_decl
                 | repeat_stmt
                 | if_stmt
                 | print_stmt
                 | func_def
                 | call_stmt
                 | return_stmt
                 | label_stmt
```

### Declarations and Assignments

```ebnf
var_decl       ::= 'let' IDENT '=' expr ';'
```

### Control Flow

```ebnf
repeat_stmt    ::= 'repeat' IDENT 'in' expr '..' expr '{' stmt_list '}'

if_stmt        ::= 'if' expr 'goto' IDENT ';'

label_stmt     ::= IDENT ':'
```

### Functions

```ebnf
func_def       ::= 'func' IDENT '(' [param_list] ')' '{' stmt_list '}'

param_list     ::= IDENT { ',' IDENT }

call_stmt      ::= IDENT '(' [arg_list] ')' ';'

arg_list       ::= expr { ',' expr }

return_stmt    ::= 'return' expr ';'
```

### I/O

```ebnf
print_stmt     ::= 'print' expr ';'
```

### Expressions

```ebnf
expr           ::= term { ('+' | '-' | '==' | '!=' | '<' | '>' | '<=' | '>=') term }

term           ::= factor { ('*' | '/') factor }

factor         ::= NUMBER
                 | IDENT
                 | '(' expr ')'
                 | IDENT '(' [arg_list] ')'
```

## Tokens

### Keywords

```
let, repeat, in, print, if, goto, end, return, func
```

### Operators

```
Arithmetic:  +  -  *  /  =
Comparison:  ==  !=  <  >  <=  >=
Range:       ..
```

### Symbols

```
;  ,  {  }  (  )  :
```

### Literals and Identifiers

```
IDENT      ::= [a-zA-Z_][a-zA-Z0-9_]*
NUMBER     ::= [0-9]+
```

### Comments

```
# Single-line comments (ignored by lexer)
```

## Operator Precedence

From highest to lowest:

1. **Parentheses**: `( )`
2. **Function calls**: `func(args)`
3. **Multiplicative**: `*` `/`
4. **Additive**: `+` `-`
5. **Comparison**: `==` `!=` `<` `>` `<=` `>=`

## Grammar Notes

### Variable Scoping

- Variables declared with `let` are scoped to their containing block
- Function parameters create new variables in function scope
- Loop variables (`repeat i in ...`) are scoped to the loop body

### Type System

- PatternLang is integer-only (no floats, strings, or other types)
- All operations result in integer values
- Comparison operators return 1 (true) or 0 (false)

### Statement vs Expression Distinction

- **Statements**: Must end with `;` (except labels which end with `:`)
- **Expressions**: Can appear within statements or other expressions
- **Function calls**: Can be used both as statements and as expressions

### Special Cases

#### Function Call Disambiguation

```ebnf
# As statement:
call_stmt      ::= IDENT '(' [arg_list] ')' ';'

# As expression (in factor):
factor         ::= IDENT '(' [arg_list] ')'
```

#### Label vs Identifier Disambiguation

The parser uses lookahead to distinguish:

- `IDENT ':'` → Label statement
- `IDENT '(' ...` → Function call
- `IDENT` (alone) → Identifier expression

## Example Program Demonstrating Grammar

```patternlang
# Function definition
func add(a, b) {
    return a + b;
}

# Variable declarations
let x = 10;
let y = 20;

# Function call in expression
let sum = add(x, y);

# Print statement
print sum;

# Repeat loop with label and conditional
repeat i in 1..10 {
    let mod = i / 2;
    let doubled = mod * 2;
    let is_odd = i - doubled;

    if is_odd goto skip;
    print i;
    skip:
}

# Program terminator
end;
```

## Grammar Properties

### LL(1) Compatibility

The grammar is mostly LL(1) with lookahead needed for:

- Distinguishing labels (`IDENT :`) from function calls (`IDENT (`)
- Distinguishing function call expressions from identifiers

### Left Recursion

The grammar avoids left recursion by using right-recursive rules:

```ebnf
expr ::= term { operator term }
```

### Operator Associativity

- All binary operators are left-associative
- Implemented through iterative parsing in `expr()` and `term()` methods

### First and Follow Sets

**First(statement)**:
`{ let, repeat, if, print, func, return, IDENT }`

**Follow(statement)**:
`{ let, repeat, if, print, func, return, IDENT, end, } }`

**First(expr)**:
`{ NUMBER, IDENT, ( }`

**Follow(expr)**:
`{ ;, ), ,, .., {, goto }`
