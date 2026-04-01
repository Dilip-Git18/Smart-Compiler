# ClearCom - Mini C-like Smart Error Detecting Compiler

ClearCom is a beginner-friendly compiler built with Python and PLY (Lex/Yacc).
It performs lexical analysis, parsing, semantic checks, and prints an AST.

## Features

- Lexer using PLY Lex
- Parser using PLY Yacc
- AST generation and tree printing
- Symbol table for declarations and lookup
- Smart error reporting with line numbers
- Interactive mode and file mode

## Language Definition

Supported syntax:

```c
int a;
float b;
a = 5;
b = a + 2;
```

Supported operators: `+`, `-`, `*`, `/`, `%`

Not supported (full C features):

- `#include`
- `printf(...)`
- `int main() { ... }`
- braces `{}` and function definitions

## AST: Where It Is Created

- AST node class: `parser.py` (`ASTNode`)
- AST built in parser rules such as `p_program`, `p_declaration`, `p_assignment`
- AST printed in `main.py` and `interactive.py` using `ast.print_tree()`

AST is shown only when compilation succeeds with no errors.

## Project Structure

```text
Mini-Compiler/
├── lexer.py
├── parser.py
├── symbol_table.py
├── main.py
├── interactive.py
├── requirements.txt
├── input.mc
├── error_input.mc
├── error_test2.mc
├── README.md
├── HOW_TO_RUN.md
├── START_HERE.md
└── PRESENTATION.md
```

## Installation

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
```

## Run

File mode:

```bash
./.venv/bin/python main.py input.mc
```

Interactive mode:

```bash
./.venv/bin/python interactive.py
```

## Troubleshooting

If Pylance shows `Import "ply.lex" could not be resolved`:

1. Install dependencies in your selected environment:

```bash
./.venv/bin/python -m pip install -r requirements.txt
```

2. In VS Code select the same interpreter:
   - Cmd+Shift+P
   - Python: Select Interpreter
   - choose the interpreter used above
