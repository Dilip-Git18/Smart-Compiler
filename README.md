# ClearCom - Mini C-like Smart Error Detecting Compiler

A beginner-friendly compiler that can tokenize, parse, and perform semantic analysis on a simple C-like language.

## Features

- **Lexer**: Tokenizes source code and detects invalid characters
- **Parser**: Validates syntax using yacc (parser generator)
- **Symbol Table**: Tracks variable declarations and types
- **Semantic Analysis**: Detects:
  - Undeclared variables
  - Duplicate variable declarations
  - Missing semicolons
  - Invalid syntax

## Supported Language

**Data Types:**
- `int`
- `float`

**Statements:**
- Variable declaration: `int a;`
- Assignment: `a = 5;`
- Expressions with operators: `a = b + 5;`

## Project Structure

```
Mini-Compiler/
├── lexer.py           # Tokenizer (PLY Lex)
├── parser.py          # Syntax parser (PLY Yacc)
├── symbol_table.py    # Variable management
├── main.py            # Entry point
├── input.mc           # Sample input (valid)
├── error_input.mc     # Sample input (with errors)
└── README.md          # This file
```

## Installation

### Prerequisites
- Python 3.6+
- pip (Python package manager)

### Step 1: Install PLY
```bash
pip install ply
```

## How to Run

### Compile a file
```bash
python main.py input.mc
```

### Test with error file
```bash
python main.py error_input.mc
```

## Sample Input and Output

### Good Example (`input.mc`)
```c
int a;
float b;
a = 5;
b = 3 + 2;
```

**Output:**
```
==================================================
ClearCom Compiler
==================================================

Source Code:
--------------------------------------------------
int a;
float b;
a = 5;
b = 3 + 2;

--------------------------------------------------

Compiling...

Symbol Table:
------------------------------
  a              : int
  b              : float
------------------------------

COMPILATION SUCCESSFUL
--------------------------------------------------
No errors found!
--------------------------------------------------
```

### Bad Example (`error_input.mc`)
```c
int x
x = 10;
y = 5;
int y;
```

**Output:**
```
==================================================
ClearCom Compiler
==================================================

Source Code:
--------------------------------------------------
int x
x = 10;
y = 5;
int y;

--------------------------------------------------

Compiling...

Symbol Table:
------------------------------
  y              : int
------------------------------

COMPILATION FAILED
--------------------------------------------------
Errors:
  ✗ Line 1: Missing ';' after variable declaration
  ✗ Line 3: Undeclared variable 'y'
  ✗ Line 4: Duplicate variable 'y' (previously declared)
--------------------------------------------------
```

## Error Messages

The compiler provides smart error messages including:

| Error Type | Example Message |
|------------|-----------------|
| Syntax Error | `Line 1: Missing ';' after variable declaration` |
| Undeclared Variable | `Line 3: Undeclared variable 'y'` |
| Duplicate Variable | `Line 4: Duplicate variable 'y' (previously declared)` |
| Invalid Character | `Line 2: Invalid character '$'` |
| Syntax Error | `Line 2: Syntax error at 'value'` |

## Code Structure

### lexer.py
- Defines tokens: keywords, identifiers, numbers, operators
- Uses PLY Lex for tokenization
- Reports invalid characters

### parser.py
- Defines grammar rules for the language
- Uses PLY Yacc for parsing
- Performs semantic analysis using the symbol table

### symbol_table.py
- Manages variable declarations
- Checks for duplicate declarations
- Checks for undeclared variable usage

### main.py
- Entry point for the compiler
- Reads source files
- Calls lexer, parser, and displays results

## Learning Points

This project teaches:
- **Lexical Analysis**: How tokenization works
- **Syntax Analysis**: Understanding grammar and parsing
- **Semantic Analysis**: Type checking and scope validation
- **Error Reporting**: User-friendly error messages
- **Symbol Tables**: Variable tracking and management

## Extending the Compiler

You can extend ClearCom to support:
- More operators: `-`, `*`, `/`, `%`
- Comparison operators: `==`, `!=`, `<`, `>`
- Logical operators: `&&`, `||`, `!`
- Control flow: `if`, `else`, `while`, `for`
- Functions: function declarations and calls
- Arrays

## Troubleshooting

### ImportError: No module named 'ply'
```bash
pip install ply
```

### File not found
Make sure the `.mc` file exists in the same directory or provide the correct path:
```bash
python main.py ./path/to/file.mc
```

### Parser tables not updating
Delete `parser.out` and `parsetab.py` if they exist:
```bash
rm -f parser.out parsetab.py
```

## License
This is a learning project. Feel free to modify and use as you like!
